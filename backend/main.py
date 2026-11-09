# -*- coding: utf-8 -*-
"""
main.py - FastAPI Backend สำหรับระบบ WeEasyTrip

Endpoints:
  GET  /api/health    — ตรวจสอบสถานะ API
  GET  /api/pois      — ดึงข้อมูล POI และโรงแรมทั้งหมด
  POST /api/packages  — สร้าง 3 แพ็กเกจ (Budget / Standard / Premium)
  POST /api/recompute — คำนวณใหม่หลังผู้ใช้แก้ไข route
"""
import sys, os, time, random, secrets, threading, asyncio
from typing import List, Optional

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(THIS_DIR), 'algorithm'))

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from utils import load_data, evaluate_route, set_travel_profile, haversine_km
from greedy import greedy_solve
from genetic import genetic_solve
from hybrid import hybrid_solve, reoptimize_solve, infeasible_locks
from pareto import nsga2_solve

import json
import math
DATA_DIR = os.path.join(os.path.dirname(THIS_DIR), 'data')
with open(os.path.join(DATA_DIR, 'provinces.json'), encoding='utf-8') as _f:
    PROVINCES = json.load(_f)
DEFAULT_PROVINCE = 'phuket'
try:   # จังหวัดที่ผ่านเกณฑ์ผ่อนปรน (ข้อมูลน้อย) — ใช้แสดงป้ายเตือนที่หน้าเว็บ
    with open(os.path.join(DATA_DIR, 'provinces_status.json'), encoding='utf-8') as _f:
        SPARSE = {k for k, v in json.load(_f).items() if v.get('sparse')}
except Exception:
    SPARSE = set()
sys.path.insert(0, DATA_DIR)
from thai_provinces import PROVINCES_77, EXTRA_AREAS   # รายชื่อ 77 จังหวัด (ใช้แสดงรายการที่ยังไม่พร้อม)
# นโยบาย RL ที่ฝึกแล้ว (algorithm/rl_policy.json) ใช้เป็น seed เพิ่มของ Hybrid เมื่อเลือก algorithm='hybrid_rl' (โหมด Developer)
try:
    import numpy as _np
    RL_THETA = _np.array(json.load(open(os.path.join(os.path.dirname(THIS_DIR), 'algorithm', 'rl_policy.json'), encoding='utf-8'))['theta'])
except Exception:
    RL_THETA = None
DIVERSITY_WEIGHT = 1.5   # น้ำหนักความหลากหลายของหมวดใน fitness ของ Hybrid (0 = แบบ Project 1)

# slug -> {'pois','hotels','poi_by_id','hotel_by_id'} (เฉพาะจังหวัดที่มีไฟล์ข้อมูลแล้ว)
DATA = {}
for _slug in list(PROVINCES):
    _path = os.path.join(DATA_DIR, 'provinces', f'{_slug}.json')
    if not os.path.exists(_path):
        del PROVINCES[_slug]
        continue
    _pois, _hotels = load_data(_path)
    DATA[_slug] = {'pois': _pois, 'hotels': _hotels,
                   'poi_by_id': {p['id']: p for p in _pois},
                   'hotel_by_id': {h['id']: h for h in _hotels}}


COMBO = {}   # 'a+b' -> ข้อมูลรวมหลายจังหวัด (ทริปข้ามจังหวัดข้างเคียง)


def _combo(slug):
    parts = slug.split('+')
    if len(parts) > 3 or len(set(parts)) != len(parts) or any(p not in DATA for p in parts):
        return None
    if slug not in COMBO:
        pois = [{**x, 'id': f'{s}.{x["id"]}'} for s in parts for x in DATA[s]['pois']]   # id ซ้ำข้ามจังหวัด (P01) จึงใส่ prefix
        hotels = [{**x, 'id': f'{s}.{x["id"]}'} for s in parts for x in DATA[s]['hotels']]
        COMBO[slug] = {'pois': pois, 'hotels': hotels, 'poi_by_id': {p['id']: p for p in pois},
                       'hotel_by_id': {h['id']: h for h in hotels}}
    return COMBO[slug]


def get_province(slug):
    if slug not in DATA:
        d = _combo(slug)
        if d is None:
            raise HTTPException(status_code=404, detail=f'Province {slug} not found')
        pv = PROVINCES[slug.split('+')[0]]   # โปรไฟล์เวลาเดินทางใช้ของจังหวัดแรก
        set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
        return d
    pv = PROVINCES[slug]   # ตั้งโปรไฟล์ระยะ/เวลาเดินทางของจังหวัดให้ request นี้
    set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
    return DATA[slug]



# ============================================================
# โมเดลข้อมูล
# ============================================================
class Preferences(BaseModel):
    """ความชอบของผู้ใช้ — กรอง/ถ่วงน้ำหนัก POI ก่อนส่งให้อัลกอริทึม"""
    liked: List[str] = []      # หมวดที่ชอบ (beach, temple, ...) ได้คะแนนถ่วงเพิ่มตอนเลือก
    avoided: List[str] = []    # หมวดที่ไม่ต้องการ (ตัดออกจากตัวเลือก; ไม่รวม restaurant)
    diet: str = 'none'         # 'none' | 'vegetarian' | 'halal' (กรองร้านอาหารตามแท็กใน OSM)


class PackageRequest(BaseModel):
    province: str = Field(DEFAULT_PROVINCE, description="slug ของจังหวัด (ดู /api/provinces)")
    preferences: Optional[Preferences] = None
    budget: float = Field(..., ge=1000, le=100000)
    days: int = Field(..., ge=1, le=7)
    travelers: int = Field(1, ge=1, le=10)
    seed: Optional[int] = Field(None, description="Random seed; None = random every call")
    algorithm: Optional[str] = Field('hybrid', description="'greedy' | 'ga' | 'hybrid' | 'hybrid_rl'")
    include_hotel: Optional[bool] = Field(True, description="รวมค่าโรงแรมในงบหรือไม่")


class RecomputeRequest(BaseModel):
    province: str = DEFAULT_PROVINCE
    hotel_id: str
    days: int
    budget: float
    routes: List[List[str]]
    travelers: int = 1


class ReoptimizeRequest(BaseModel):
    province: str = DEFAULT_PROVINCE
    tier: str = 'Custom'
    hotel_id: str
    days: int = Field(..., ge=1, le=7)
    budget: float = Field(..., ge=1000, le=100000)   # งบรวมของผู้ใช้ (บาท)
    travelers: int = Field(1, ge=1, le=10)
    include_hotel: bool = True
    routes: List[List[str]]
    locked: List[str] = []      # POI ที่ผู้ใช้เลือกเอง ต้องคงไว้
    excluded: List[str] = []    # POI ที่ผู้ใช้ลบ ห้ามกลับมา
    preferences: Optional[Preferences] = None
    seed: Optional[int] = None


class DayDetail(BaseModel):
    day: int
    pois: List[dict]
    distance_km: float
    time_min: float
    cost: float
    score: float
    arrivals: List[list] = []   # [[poi_id, นาทีที่ถึง (นับจาก 00:00)], ...] ใช้สร้างตารางเวลา/ไฟล์ปฏิทิน


class Package(BaseModel):
    tier: str
    hotel: dict
    days: List[DayDetail]
    total_score: float
    total_activity_cost: float
    total_hotel_cost: float
    total_cost: float
    runtime_ms: float
    valid: bool
    violations: List[str]
    notes: List[str] = []   # ข้อความแจ้งผู้ใช้ เช่น จุดที่เลือกแต่ใส่ในแผนไม่ได้
    objectives: dict = {}   # Pareto: score / diversity / distance_km / cost ของแผนนี้


class PackageResponse(BaseModel):
    request: dict
    packages: List[Package]



# ============================================================
# ฟังก์ชันต่างๆ
# ============================================================
def make_day_details(routes_per_day, hotel, travelers=1):
    """แปลง routes เป็น List[DayDetail] พร้อม metadata (ระยะทาง, เวลา, ค่าใช้จ่าย, score)"""
    eval_result = evaluate_route(routes_per_day, hotel, budget=float('inf'))
    days = []
    for i, day_pois in enumerate(routes_per_day):
        det = eval_result['days_detail'][i]
        days.append(DayDetail(
            day=i + 1,
            pois=[{
                'id': p['id'], 'name_th': p['name_th'], 'name_en': p['name_en'],
                'category': p['category'], 'lat': p['lat'], 'lng': p['lng'],
                'score': p['score'], 'cost': p['cost'] * travelers,
                'duration_min': p['duration_min'],
            } for p in day_pois],
            distance_km=det['distance_km'],
            time_min=det['time_min'],
            cost=det['cost'] * travelers,
            score=det['score'],
            arrivals=[list(a) for a in det.get('arrivals', [])]
        ))
    return days, eval_result


def _trim_to_budget(routes, hotel, max_activity_budget, travelers, pois):
    """4-phase budget + time-window enforcement:
       1) Swap expensive restaurants → cheaper unused
       2) Remove paid attractions (highest cost first)
       3) Remove any POI (incl. restaurants) if still over budget
       4) Remove POIs causing time-window violations
    """
    import re as _re
    from utils import evaluate_route as _eval

    def _check(rts):
        r = _eval(rts, hotel, budget=float('inf'))
        # Budget ครอบคลุมเฉพาะ ค่าเข้า + ค่าอาหาร (per-person × travelers)
        # ค่าเดินทาง (transportation) ถือเป็น overhead ไม่นับในงบกิจกรรม
        poi_cost = sum(p['cost'] for day in rts for p in day) * travelers
        return poi_cost, r

    used_ids = {p['id'] for day in routes for p in day}
    unused_rest = sorted(
        [p for p in pois if p['category'] == 'restaurant' and p['id'] not in used_ids],
        key=lambda x: (not x.get('_diet'), x['cost']))   # ร้านที่ตรงความต้องการด้านอาหารเป็นตัวสลับก่อน

    # Phase 1: สลับร้านอาหารแพงด้วยร้านที่ถูกกว่า
    for cheap_rest in unused_rest:
        total_act, _ = _check(routes)
        if total_act <= max_activity_budget:
            break
        worst_d, worst_i, worst_cost = None, None, cheap_rest['cost']
        for di, day in enumerate(routes):
            for pi, p in enumerate(day):
                if p['category'] == 'restaurant' and p['cost'] > worst_cost:
                    worst_cost = p['cost']; worst_d, worst_i = di, pi
        if worst_d is None:
            break
        old_id = routes[worst_d][worst_i]['id']
        routes[worst_d][worst_i] = cheap_rest
        used_ids.discard(old_id)
        used_ids.add(cheap_rest['id'])

    # Phase 2: ลบ attraction ที่มีค่าเข้าชม (เริ่มจากแพงสุด)
    while True:
        total_act, _ = _check(routes)
        if total_act <= max_activity_budget:
            break
        worst_d, worst_i, worst_cost = None, None, 0
        for di, day in enumerate(routes):
            for pi, p in enumerate(day):
                if p['category'] != 'restaurant' and p['cost'] > worst_cost:
                    worst_cost = p['cost']; worst_d, worst_i = di, pi
        if worst_d is None:
            break
        routes[worst_d].pop(worst_i)

    # Phase 3: ลบ POI ใดก็ได้รวมถึงร้านอาหาร ถ้ายังเกินงบ
    while True:
        total_act, _ = _check(routes)
        if total_act <= max_activity_budget:
            break
        worst_d, worst_i, worst_cost = None, None, -1
        for di, day in enumerate(routes):
            for pi, p in enumerate(day):
                if p['cost'] > worst_cost:
                    worst_cost = p['cost']; worst_d, worst_i = di, pi
        if worst_d is None:
            break
        routes[worst_d].pop(worst_i)

    # Phase 4: ลบ POI ที่ไปถึงหลังเวลาปิด
    for _ in range(30):
        _, result = _check(routes)
        tw = [v for v in result['violations'] if 'หลังเวลาปิด' in v]
        if not tw:
            break
        removed = False
        for viol in tw:
            m = _re.search(r'ไปถึง (\S+) หลังเวลาปิด', viol)
            if not m:
                continue
            bad_id = m.group(1)
            for di, day in enumerate(routes):
                for pi, p in enumerate(day):
                    if p['id'] == bad_id:
                        routes[di].pop(pi)
                        removed = True
                        break
                if removed:
                    break
        if not removed:
            break

    return routes


LIKE_BOOST = 1.0   # คะแนนถ่วงเพิ่มให้ POI ในหมวดที่ผู้ใช้ชอบ (ใช้เลือกเท่านั้น ไม่นับในคะแนนที่รายงาน)
DIET_BOOST = 4.0   # ถ่วงร้านที่ตรงความต้องการด้านอาหารเมื่อร้านที่ตรงมีไม่พอทั้งทริป


def apply_preferences(pois, prefs, days):
    """สร้างกลุ่ม POI สำหรับอัลกอริทึมตามความชอบ คืน (pool, notes)
       - avoided: ตัด POI หมวดนั้นออก (ไม่แตะร้านอาหาร)
       - diet: ใช้เฉพาะร้านที่มีแท็ก ถ้าน้อยกว่าจำนวนมื้อที่ต้องใช้ จะเสริมร้านทั่วไปและแจ้งผู้ใช้
       - liked: คัดลอก POI พร้อมบวกคะแนน LIKE_BOOST เพื่อให้ถูกเลือกบ่อยขึ้น
       pool คือสำเนา — ต้อง restore_scores() กลับเป็นออบเจ็กต์ต้นฉบับก่อนสร้างแพ็กเกจ"""
    notes = []
    if prefs is None:
        return pois, notes
    cats = {p['category'] for p in pois}
    avoided = {c for c in prefs.avoided if c in cats and c != 'restaurant'}
    liked = {c for c in prefs.liked if c in cats and c != 'restaurant'} - avoided
    pool = [p for p in pois if p['category'] not in avoided]
    if liked:
        # _base = คะแนนจริง ใช้กำหนดช่วงคะแนนของแต่ละ tier ไม่ให้ที่ชอบหลุดจาก tier ประหยัด
        pool = [dict(p, score=round(p['score'] + LIKE_BOOST, 2), _base=p['score']) if p['category'] in liked else p for p in pool]
    if prefs.diet in ('vegetarian', 'halal'):
        need = 2 * days + 2
        match = [p for p in pool if p['category'] == 'restaurant' and prefs.diet in p.get('tags', [])]
        label = 'มังสวิรัติ' if prefs.diet == 'vegetarian' else 'ฮาลาล'
        if len(match) >= need:
            pool = [p for p in pool if p['category'] != 'restaurant' or p in match]
        elif match:
            # ไม่พอทั้งทริป: ถ่วงคะแนนร้านที่ตรงให้ถูกเลือกก่อน ที่เหลือเสริมด้วยร้านทั่วไป
            ids = {p['id'] for p in match}
            pool = [dict(p, score=round(p['score'] + DIET_BOOST, 2), _base=p.get('_base', p['score']), _diet=True) if p['id'] in ids else p for p in pool]
            notes.append(f'ร้านอาหาร{label}ในฐานข้อมูลมีเพียง {len(match)} ร้าน ไม่พอสำหรับทั้งทริป จึงใช้ร้านเหล่านี้ก่อนแล้วเสริมด้วยร้านทั่วไป (ไม่รับประกันว่ารองรับอาหาร{label})')
        else:
            notes.append(f'ไม่พบข้อมูลร้านอาหาร{label}ของจังหวัดนี้ในฐานข้อมูล จึงใช้ร้านทั่วไป (ไม่รับประกันว่ารองรับอาหาร{label})')
    return pool, notes


def restore_originals(routes, originals):
    """แทนที่ POI ที่ถูกถ่วงคะแนนด้วยออบเจ็กต์ต้นฉบับ (คะแนนที่รายงานต้องเป็นคะแนนจริง)"""
    return [[originals.get(p['id'], p) for p in day] for day in routes]


def build_package(tier, hotel, routes, days, budget, runtime_ms, travelers, pois,
                  max_total_budget=None, hotel_cost_override=None):
    """สร้าง Package object จาก routes และตัดงบประมาณให้อยู่ใน max_total_budget ที่กำหนด"""
    nights = max(0, days - 1)
    hotel_cost = hotel_cost_override if hotel_cost_override is not None else hotel['cost'] * nights
    # ถ้ากำหนด max_total_budget ให้ตัดงบตาม
    if max_total_budget is not None:
        max_activity = max(0, max_total_budget - hotel_cost)
        routes = _trim_to_budget(routes, hotel, max_activity, travelers, pois)
    day_details, eval_result = make_day_details(routes, hotel, travelers)
    activity_cost = sum(d.cost for d in day_details)
    total = activity_cost + hotel_cost
    violations = list(eval_result['violations'])
    valid = eval_result['valid']
    return Package(
        tier=tier, hotel=hotel, days=day_details,
        total_score=eval_result['total_score'] if valid else 0,
        total_activity_cost=activity_cost,
        total_hotel_cost=hotel_cost,
        total_cost=total,
        runtime_ms=runtime_ms,
        valid=valid,
        violations=violations
    )



# ============================================================
# FastAPI app และ CORS
# ============================================================
app = FastAPI(title='WeEasyTrip API', version='1.0.0')
# ---------- จำกัดคำขอหนัก (Hybrid/GA ใช้ CPU 2–4 วินาที): 20 ครั้ง/นาที/IP และรันพร้อมกันได้ 2 งาน ----------
_HEAVY = ('/api/packages', '/api/pareto', '/api/reoptimize')   # /api/recompute คำนวณเบา ใช้ตอนลากวางบ่อย จึงไม่จำกัด
_HITS = {}                                  # ip -> [เวลาของคำขอล่าสุด]
_SLOTS = asyncio.Semaphore(2)
RATE_PER_MIN = int(os.environ.get('WET_RATE_PER_MIN', '20'))


@app.middleware('http')
async def limit_heavy(request: Request, call_next):
    if request.method == 'POST' and request.url.path in _HEAVY:
        ip = request.client.host if request.client else '?'
        now = time.time()
        hits = [t for t in _HITS.get(ip, []) if now - t < 60]
        if len(hits) >= RATE_PER_MIN:
            return JSONResponse({'detail': 'ส่งคำขอถี่เกินไป รอสักครู่แล้วลองใหม่'}, status_code=429)
        _HITS[ip] = hits + [now]
        try:
            await asyncio.wait_for(_SLOTS.acquire(), timeout=20)
        except asyncio.TimeoutError:
            return JSONResponse({'detail': 'เซิร์ฟเวอร์กำลังประมวลผลหลายงาน ลองใหม่อีกครั้ง'}, status_code=503)
        try:
            return await call_next(request)
        finally:
            _SLOTS.release()
    return await call_next(request)


app.add_middleware(CORSMiddleware, allow_origins=['*'],
                   allow_credentials=True, allow_methods=['*'], allow_headers=['*'])



# ============================================================
# API endpoints
# ============================================================
@app.get('/api/health')
def health():
    """ตรวจสอบสถานะ API — คืนจำนวน POI และโรงแรมที่โหลดไว้ (ทุกจังหวัดรวมกัน)"""
    return {'status': 'ok',
            'pois': sum(len(d['pois']) for d in DATA.values()),
            'hotels': sum(len(d['hotels']) for d in DATA.values()),
            'provinces': len(DATA)}


def _max_days(slug):
    """จำนวนวันสูงสุดที่ข้อมูลรองรับ: สถานที่ ≥ 3 จุด/วัน และร้านอาหาร ≥ 2 ร้าน/วัน (มื้อกลางวัน+เย็น ไม่ซ้ำร้าน) (ไม่งั้นมีวันว่าง)"""
    pois = DATA[slug]['pois']
    rest = sum(1 for p in pois if p['category'] == 'restaurant')
    return max(1, min(7, (len(pois) - rest) // 3, rest // 2))


def _neighbors(slug, km=110, top=4):
    """จังหวัดข้างเคียง (ศูนย์กลางห่างไม่เกิน km กม.) เรียงจากใกล้สุด — ใช้ทำทริปข้ามจังหวัด"""
    c = PROVINCES[slug]['center']
    def dist(o):   # กม. เส้นตรงโดยประมาณ (ไม่ผ่าน haversine_km เพราะคูณ road_factor ของ request ก่อนหน้า)
        b = PROVINCES[o]['center']
        return 111 * ((c[0] - b[0]) ** 2 + ((c[1] - b[1]) * math.cos(math.radians(c[0]))) ** 2) ** 0.5
    ds = sorted((dist(o), o) for o in DATA if o != slug and o != 'samui')
    return [o for d, o in ds if d <= km][:top]


@app.get('/api/provinces')
def get_provinces():
    """รายการจังหวัดที่มีข้อมูล พร้อมศูนย์กลางแผนที่และจำนวน POI/โรงแรม"""
    region = {p[0]: p[3] for p in PROVINCES_77}
    region.update({k: v[2] for k, v in EXTRA_AREAS.items()})
    return {'default': DEFAULT_PROVINCE,
            'provinces': [{'slug': s, **PROVINCES[s], 'region': region.get(s, PROVINCES[s].get('region', '')),
                           'pois': len(DATA[s]['pois']), 'hotels': len(DATA[s]['hotels']), 'sparse': s in SPARSE,
                           'max_days': _max_days(s), 'neighbors': _neighbors(s)}
                          for s in DATA],
            'planned': [{'slug': p[0], 'name_th': p[1], 'name_en': p[2], 'region': p[3]}
                        for p in PROVINCES_77 if p[0] not in DATA]}



@app.get('/api/pois')
def get_pois(province: str = DEFAULT_PROVINCE):
    """ดึงรายการ POI และโรงแรมทั้งหมดของจังหวัด"""
    d = get_province(province)
    return {'pois': d['pois'], 'hotels': d['hotels']}


# ---------- โหมด Developer: รหัสผ่านตรวจที่ backend (ตั้งค่าได้ด้วยตัวแปรแวดล้อม WET_DEV_PASSWORD) ----------
DEV_PASSWORD = os.environ.get('WET_DEV_PASSWORD', '007')
DEV_TOKENS = set()          # shortcut: เก็บในหน่วยความจำ — รีสตาร์ทเซิร์ฟเวอร์แล้วต้องใส่รหัสใหม่
_UNLOCK_FAILS = {}          # ip -> [เวลาที่ใส่ผิด] จำกัด 5 ครั้ง/นาที กันเดารหัส


class UnlockRequest(BaseModel):
    password: str


@app.post('/api/dev/unlock')
def dev_unlock(body: UnlockRequest, request: Request):
    ip = request.client.host if request.client else '?'
    now = time.time()
    fails = [t for t in _UNLOCK_FAILS.get(ip, []) if now - t < 60]
    if len(fails) >= 5:
        raise HTTPException(status_code=429, detail='ลองรหัสผิดหลายครั้ง รอ 1 นาทีแล้วลองใหม่')
    if not secrets.compare_digest(body.password, DEV_PASSWORD):
        _UNLOCK_FAILS[ip] = fails + [now]
        raise HTTPException(status_code=403, detail='รหัสผ่านไม่ถูกต้อง')
    token = secrets.token_hex(16)
    DEV_TOKENS.add(token)
    return {'token': token}


def is_dev(token: Optional[str]) -> bool:
    return bool(token) and token in DEV_TOKENS


@app.get('/api/dev/check')
def dev_check(x_dev_token: Optional[str] = Header(None)):
    return {'ok': is_dev(x_dev_token)}


@app.post('/api/packages', response_model=PackageResponse)
def create_packages(req: PackageRequest, x_dev_token: Optional[str] = Header(None)):
    """สร้าง 3 แพ็กเกจ (Budget / Standard / Premium) ด้วย algorithm ที่เลือก"""
    # ใช้ seed ที่กำหนดเพื่อ reproduce ผล; None → สุ่มใหม่ทุกครั้ง
    if (req.algorithm or 'hybrid').lower() != 'hybrid' and not is_dev(x_dev_token):   # เลือกอัลกอริทึมอื่นได้เฉพาะโหมด Developer
        raise HTTPException(status_code=403, detail='ต้องเข้าโหมด Developer เพื่อเลือกอัลกอริทึมอื่นนอกจาก Hybrid')
    random.seed(req.seed)
    data = get_province(req.province)
    HOTELS = data['hotels']
    originals = data['poi_by_id']
    POIS, pref_notes = apply_preferences(data['pois'], req.preferences, req.days)

    # tier: (ชื่อ, สัดส่วนงบโรงแรม, สัดส่วนงบรวม, scoring_mode, score_pct, max_rest_cost)
    # score_pct: percentile สูงสุดของ score ที่อนุญาตสำหรับ tier นั้น
    # max_rest_cost: ราคาร้านอาหารสูงสุด (None = ไม่จำกัด)
    tier_specs = [
        ('Budget',   0.20, 0.40, 'ratio',   0.50,  150),  # ร้านถูก + attr ระดับกลาง
        ('Standard', 0.45, 0.75, 'quality', 0.80,  400),  # ร้านกลาง + attr ระดับดี
        ('Premium',  0.55, 1.00, 'quality', None,  None), # ทุกอย่าง เน้น score สูงสุด
    ]
    all_pois = POIS
    sorted_hotels = sorted(HOTELS, key=lambda h: h['cost'])

    # คำนวณ score threshold จาก non-restaurant POIs
    _attr_scores = sorted(p.get('_base', p['score']) for p in all_pois if p['category'] != 'restaurant')
    def _percentile(lst, pct):
        idx = max(0, int(len(lst) * pct) - 1)
        return lst[idx]

    def make_tier_pois(score_pct, max_rest_cost=None):
        """กรอง POI ตาม tier:
           - attr: กรองตาม score percentile
           - restaurant: กรองตาม max_rest_cost เพื่อให้ tier ต่างกันชัดเจน
        """
        result = []
        attr_max = _percentile(_attr_scores, score_pct) if score_pct is not None else float('inf')
        for p in all_pois:
            if p['category'] == 'restaurant':
                if max_rest_cost is None or p['cost'] <= max_rest_cost:
                    result.append(p)
            else:
                if p.get('_base', p['score']) <= attr_max:
                    result.append(p)
        # ร้านที่ผ่านเพดานราคาของ tier น้อยเกินไป (เช่น กรองตามอาหารมังสวิรัติแล้วเหลือแต่ร้านแพง): เติมร้านที่ถูกที่สุดจนครบมื้อ
        need = 2 * req.days + 2
        chosen = [p for p in result if p['category'] == 'restaurant']
        if len(chosen) < need:
            rest_ids = {p['id'] for p in chosen}
            extra = sorted((p for p in all_pois if p['category'] == 'restaurant' and p['id'] not in rest_ids),
                           key=lambda p: (not p.get('_diet'), p['cost']))[:need - len(chosen)]
            result += extra
        return result

    _dist_cache = {}

    def _median_dist(h):
        if h['id'] not in _dist_cache:
            ds = sorted(haversine_km(h['lat'], h['lng'], p['lat'], p['lng']) for p in all_pois if p['category'] != 'restaurant')
            _dist_cache[h['id']] = ds[len(ds) // 2] if ds else 0.0
        return _dist_cache[h['id']]

    def find_best_hotel(max_per_night, exclude):
        cands = [h for h in sorted_hotels
                 if h['cost'] <= max_per_night and h['id'] not in exclude]
        if not cands:
            free = [h for h in sorted_hotels if h['id'] not in exclude]
            return free[0] if free else sorted_hotels[0]   # โรงแรมไม่พอสำหรับ 3 ระดับ (จังหวัดข้อมูลน้อย) → ใช้ซ้ำได้
        # คะแนนโรงแรมหักตามระยะเฉลี่ยถึงสถานที่ท่องเที่ยว: โรงแรมที่ไกลแหล่งเที่ยวทำให้ค่าเดินทางและเวลาเสียทุกวัน
        return max(cands, key=lambda h: h['score'] - 0.08 * _median_dist(h))

    packages = []
    picked = set()
    algo = (req.algorithm or 'hybrid').lower()

    nights = max(0, req.days - 1)
    include_hotel = req.include_hotel if req.include_hotel is not None else True

    for tier, hotel_r, total_r, mode, score_pct, max_rest_cost in tier_specs:
        if include_hotel:
            max_per_night = req.budget * hotel_r / max(nights, 1) if nights > 0 else 0
            hotel = find_best_hotel(max_per_night, picked) if nights > 0 else sorted_hotels[0]
        else:
            # ไม่รวมโรงแรม: เลือกโรงแรมถูกสุดสำหรับ routing เท่านั้น
            avail = [h for h in sorted_hotels if h['id'] not in picked]
            hotel = avail[0] if avail else sorted_hotels[0]

        if hotel is None:
            packages.append(Package(
                tier=tier, hotel=sorted_hotels[0],
                days=[DayDetail(day=i+1, pois=[], distance_km=0, time_min=0,
                                cost=0, score=0) for i in range(req.days)],
                total_score=0, total_activity_cost=0, total_hotel_cost=0,
                total_cost=0, runtime_ms=0, valid=False,
                violations=[f'No hotel for {tier}']
            ))
            continue
        picked.add(hotel['id'])

        # คำนวณค่าโรงแรม (0 ถ้าไม่รวมโรงแรม หรือทริปวันเดียว)
        hotel_total = hotel['cost'] * nights if include_hotel else 0

        # งบสำหรับกิจกรรม
        target_total = req.budget * total_r
        budget_for_act = max(0, target_total - hotel_total) / req.travelers

        # Dynamic restaurant cap สำหรับ quality mode:
        # ป้องกันร้านอาหารแพงกินงบหมดในทริปงบต่ำ
        # Budget tier ใช้ ratio scoring ซึ่ง penalize ร้านแพงอยู่แล้ว → ไม่ต้องแตะ
        if mode == 'quality':
            # จัดสรรสูงสุด 1/5 ของงบต่อวันต่อมื้อ
            # floor=150 ensures >= 21 restaurants in pool (7 days x 2 meals = 14 slots needed)
            dyn_rest_cap = max(150.0, budget_for_act / (max(req.days, 1) * 5.0))
            if max_rest_cost is not None:
                effective_rest_cap = min(max_rest_cost, dyn_rest_cap)
            else:
                # Premium: ใช้ dynamic cap เฉพาะเมื่องบต่ำ; งบสูง (dyn≥500) ไม่จำกัด
                effective_rest_cap = dyn_rest_cap if dyn_rest_cap < 500 else None
        else:
            # Budget (ratio mode): ใช้ tier cap เดิม
            effective_rest_cap = max_rest_cost

        # กรอง POI pool ตาม tier (ทำให้แต่ละ tier ต่างกัน)
        tier_pois = make_tier_pois(score_pct, effective_rest_cap)

        t0 = time.time()
        if algo == 'greedy':
            routes = greedy_solve(tier_pois, hotel, req.days, budget_for_act,
                                  scoring_mode=mode, random_factor=0.15)
        elif algo == 'ga':
            routes, _hist = genetic_solve(tier_pois, hotel, req.days, budget_for_act,
                                          pop_size=30, generations=40,
                                          mutation_rate=0.3, verbose=False)
        else:  # hybrid
            routes, _hist = hybrid_solve(tier_pois, hotel, req.days, budget_for_act,
                                         scoring_mode=mode, pop_size=20,
                                         generations=40, mutation_rate=0.3,
                                         verbose=False, diversity_weight=DIVERSITY_WEIGHT,
                                         rl_theta=RL_THETA if algo == 'hybrid_rl' else None,
                                         ils=True)  # ILS: ดีขึ้นอย่างมีนัยสำคัญ 24/24 (experiments/results/ils_stats.txt)
        runtime_ms = (time.time() - t0) * 1000.0
        routes = restore_originals(routes, originals)   # คะแนนที่รายงานต้องเป็นคะแนนจริง ไม่รวมตัวถ่วงความชอบ
        # ใช้ target_total เป็น cap แต่ละ tier เพื่อให้งบแตกต่างกันชัดเจน
        pkg = build_package(tier, hotel, routes, req.days,
                            req.budget, runtime_ms, req.travelers, POIS,
                            max_total_budget=target_total,
                            hotel_cost_override=hotel_total)
        pkg.notes = list(pref_notes)
        empty = sum(1 for d in pkg.days if not d.pois)
        if empty:   # จังหวัดข้อมูลน้อย: สถานที่ไม่พอเติมทุกวัน
            pkg.notes.append(f'จังหวัดนี้มีข้อมูลสถานที่น้อย แผน{tier}มี {empty} วันที่ไม่มีกิจกรรม ลองลดจำนวนวันหรือเลือกจังหวัดอื่น')
        packages.append(pkg)
    return PackageResponse(request=req.dict(), packages=packages)


# ============================================================
# Collaborative planning: เซสชันที่แชร์ลิงก์ให้เพื่อนร่วมดู/แก้แผนเดียวกัน
# เก็บในหน่วยความจำและบันทึกลงไฟล์ data/sessions.json (กลับมาหลัง restart) — ใช้ version ทำ optimistic concurrency, ฝั่ง client โพลลิ่งทุก 2 วินาที
# ============================================================
SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sessions.json')


def _session_load():
    try:
        with open(SESSION_FILE, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _session_save():   # เรียกขณะถือ SESSION_LOCK; เขียนไฟล์ชั่วคราวแล้ว replace กันไฟล์พังกลางคัน
    try:
        tmp = SESSION_FILE + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(SESSIONS, f, ensure_ascii=False)
        os.replace(tmp, SESSION_FILE)
    except OSError:
        pass   # shortcut: บันทึกไม่ได้ก็ยังทำงานในหน่วยความจำต่อ


SESSIONS = _session_load()
SESSION_LOCK = threading.Lock()
SESSION_TTL_S = 24 * 3600
SESSION_MAX = 300


class SessionCreate(BaseModel):
    province: str = DEFAULT_PROVINCE
    package: dict
    settings: dict = {}          # budget, travelers, include_hotel, start_date, preferences, locked, excluded


class SessionUpdate(BaseModel):
    base_version: int
    package: dict
    settings: dict = {}


def _session_gc():
    now = time.time()
    for k in [k for k, v in SESSIONS.items() if now - v['updated'] > SESSION_TTL_S]:
        del SESSIONS[k]


def _session_view(sid):
    v = SESSIONS[sid]
    return {'id': sid, 'version': v['version'], 'province': v['province'], 'package': v['package'], 'settings': v['settings']}


@app.post('/api/sessions')
def create_session(req: SessionCreate):
    get_province(req.province)
    if not isinstance(req.package.get('days'), list) or len(req.package['days']) > 7:
        raise HTTPException(status_code=422, detail='invalid package')
    with SESSION_LOCK:
        _session_gc()
        if len(SESSIONS) >= SESSION_MAX:
            raise HTTPException(status_code=503, detail='too many sessions')
        sid = secrets.token_urlsafe(6)
        SESSIONS[sid] = {'version': 1, 'province': req.province, 'package': req.package,
                         'settings': req.settings, 'updated': time.time()}
        _session_save()
        return _session_view(sid)


@app.get('/api/sessions/{sid}')
def get_session(sid: str, since: int = 0):
    with SESSION_LOCK:
        if sid not in SESSIONS:
            raise HTTPException(status_code=404, detail='session not found or expired')
        if since and SESSIONS[sid]['version'] == since:
            return {'id': sid, 'version': since, 'changed': False}
        return {**_session_view(sid), 'changed': True}


@app.put('/api/sessions/{sid}')
def update_session(sid: str, req: SessionUpdate):
    with SESSION_LOCK:
        if sid not in SESSIONS:
            raise HTTPException(status_code=404, detail='session not found or expired')
        cur = SESSIONS[sid]
        if req.base_version != cur['version']:      # มีคนอื่นแก้ไปก่อน → ส่งสถานะล่าสุดกลับให้ client รวมเข้ากับของตัวเอง
            raise HTTPException(status_code=409, detail=_session_view(sid))
        cur.update(version=cur['version'] + 1, package=req.package, settings=req.settings or cur['settings'], updated=time.time())
        _session_save()
        return _session_view(sid)


@app.post('/api/pareto', response_model=PackageResponse)
def pareto(req: PackageRequest):
    """หา Pareto front (NSGA-II) ระหว่าง คะแนน / ความหลากหลายของหมวด / ระยะทางรวม คืนแผนตัวแทนไม่เกิน 8 แผน
    ใช้การตั้งค่าระดับ Standard (โรงแรม <=45% ใช้รวม <=75% ของงบ) ให้ผู้ใช้เลือก trade-off เอง"""
    random.seed(req.seed)
    data = get_province(req.province)
    pool, pref_notes = apply_preferences(data['pois'], req.preferences, req.days)
    nights = max(0, req.days - 1)
    include_hotel = req.include_hotel if req.include_hotel is not None else True
    hotels = sorted(data['hotels'], key=lambda h: h['cost'])
    max_per_night = req.budget * 0.45 / max(nights, 1) if nights > 0 else 0
    cands = [h for h in hotels if h['cost'] <= max_per_night] or hotels[:1]
    hotel = max(cands, key=lambda h: h['score']) if include_hotel and nights > 0 else hotels[0]
    hotel_total = hotel['cost'] * nights if include_hotel else 0
    target_total = req.budget * 0.75
    budget_for_act = max(0, target_total - hotel_total) / req.travelers
    # เพดานราคาร้านอาหารเหมือนระดับ Standard (ไม่ให้ร้านแพงกินงบทั้งทริป) และเติมร้านถูกสุดถ้าไม่พอมื้อ
    cap = min(400.0, max(150.0, budget_for_act / (max(req.days, 1) * 5.0)))
    rests = [p for p in pool if p['category'] == 'restaurant']
    ok_rests = [p for p in rests if p['cost'] <= cap]
    need = 2 * req.days + 2
    if len(ok_rests) < need:
        ids = {p['id'] for p in ok_rests}
        ok_rests += sorted((p for p in rests if p['id'] not in ids), key=lambda p: (not p.get('_diet'), p['cost']))[:need - len(ok_rests)]
    keep_ids = {p['id'] for p in ok_rests}
    pool = [p for p in pool if p['category'] != 'restaurant' or p['id'] in keep_ids]
    t0 = time.time()
    front = nsga2_solve(pool, hotel, req.days, budget_for_act, scoring_mode='quality', pop_size=40, generations=40)
    runtime_ms = (time.time() - t0) * 1000.0
    if len(front) > 8:   # เลือกตัวแทน 8 แผนกระจายตามระยะทาง (รวมสองปลาย)
        by_dist = sorted(front, key=lambda s: s['distance_km'])
        idx = sorted({round(i * (len(by_dist) - 1) / 7) for i in range(8)})
        front = [by_dist[i] for i in idx]
    packages = []
    for i, sol in enumerate(sorted(front, key=lambda s: s['distance_km']), 1):
        routes = restore_originals(sol['routes'], data['poi_by_id'])
        pkg = build_package(f'Pareto {i}', hotel, routes, req.days, req.budget, runtime_ms / max(len(front), 1),
                            req.travelers, pool, max_total_budget=target_total, hotel_cost_override=hotel_total)
        pkg.objectives = {'score': round(sol['score'], 1), 'diversity': round(sol['diversity'], 2),
                          'distance_km': round(sol['distance_km'], 1), 'cost': round(sol['cost'])}
        pkg.notes = list(pref_notes)
        packages.append(pkg)
    return PackageResponse(request=req.dict(), packages=packages)


@app.post('/api/recompute', response_model=Package)
def recompute(req: RecomputeRequest):
    data = get_province(req.province)
    HOTEL_BY_ID, POI_BY_ID = data['hotel_by_id'], data['poi_by_id']
    if req.hotel_id not in HOTEL_BY_ID:
        raise HTTPException(status_code=404, detail=f'Hotel {req.hotel_id} not found')
    hotel = HOTEL_BY_ID[req.hotel_id]
    routes_per_day = []
    for day in req.routes:
        day_pois = []
        for pid in day:
            if pid not in POI_BY_ID:
                raise HTTPException(status_code=404, detail=f'POI {pid} not found')
            day_pois.append(POI_BY_ID[pid])
        routes_per_day.append(day_pois)
    return build_package('Custom', hotel, routes_per_day, req.days,
                         req.budget, 0, req.travelers, data['pois'])



@app.post('/api/reoptimize', response_model=Package)
def reoptimize(req: ReoptimizeRequest):
    """ปรับแผนใหม่ด้วย Hybrid หลังผู้ใช้ swap/เพิ่ม/ลบ POI โดยคงจุดที่ผู้ใช้เลือก (locked) และไม่ใส่จุดที่ลบ (excluded)"""
    random.seed(req.seed)
    data = get_province(req.province)
    if req.hotel_id not in data['hotel_by_id']:
        raise HTTPException(status_code=404, detail=f'Hotel {req.hotel_id} not found')
    hotel = data['hotel_by_id'][req.hotel_id]
    poi_by_id = data['poi_by_id']
    for pid in [i for day in req.routes for i in day] + req.locked + req.excluded:
        if pid not in poi_by_id:
            raise HTTPException(status_code=404, detail=f'POI {pid} not found')
    routes = [[poi_by_id[i] for i in day if i not in req.excluded] for day in req.routes]
    nights = max(0, req.days - 1)
    hotel_total = hotel['cost'] * nights if req.include_hotel else 0
    budget_for_act = max(0, req.budget - hotel_total) / req.travelers
    # POI ที่ผู้ใช้เลือกแต่ใส่ในแผนใดไม่ได้ (เช่น เปิดดึกเกินเวลาต่อวัน/เกินงบ) → นำออกและแจ้งผู้ใช้
    bad = set(infeasible_locks(data['pois'], hotel, req.locked, budget_for_act))
    routes = [[p for p in day if p['id'] not in bad] for day in routes]
    pool, _ = apply_preferences(data['pois'], req.preferences, req.days)
    t0 = time.time()
    new_routes = reoptimize_solve(pool, hotel, routes, budget_for_act,
                                  locked_ids=[i for i in req.locked if i not in bad], excluded_ids=req.excluded,
                                  diversity_weight=DIVERSITY_WEIGHT)
    new_routes = restore_originals(new_routes, poi_by_id)
    runtime_ms = (time.time() - t0) * 1000.0
    pkg = build_package(req.tier, hotel, new_routes, req.days, req.budget, runtime_ms,
                         req.travelers, data['pois'], max_total_budget=req.budget,
                         hotel_cost_override=hotel_total)
    in_plan = {p['id'] for day in new_routes for p in day}
    pkg.notes = [f"ใส่ {poi_by_id[i]['name_th']} ในแผนไม่ได้ (เวลาเปิด-ปิด งบ หรือเวลาต่อวันไม่พอ)" for i in req.locked if i not in in_plan]
    return pkg


# เสิร์ฟหน้าเว็บจากบริการเดียวกัน (ตอน deploy) — ต้อง mount หลังประกาศ API ทั้งหมด
_FRONT = os.path.join(os.path.dirname(THIS_DIR), 'frontend')
if os.path.isdir(_FRONT):
    app.mount('/', StaticFiles(directory=_FRONT, html=True), name='frontend')


if __name__ == '__main__':
    import uvicorn
    print('Starting WeEasyTrip API...')
    for _s, _d in DATA.items():
        print(f"Loaded {_s}: {len(_d['pois'])} POIs, {len(_d['hotels'])} hotels")
    uvicorn.run(app, host='0.0.0.0', port=8000)
