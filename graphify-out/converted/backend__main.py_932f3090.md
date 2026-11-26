<!-- converted from backend__main.py.docx -->

คู่มือโค้ด: backend/main.py
FastAPI Backend ของ WeEasyTrip (API สร้างแพ็กเกจ ปรับแผน เซสชันร่วมกัน และให้บริการหน้าเว็บ)
ไฟล์ต้นฉบับ: backend/main.py (991 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: จุดรวมของระบบฝั่งเซิร์ฟเวอร์: โหลดข้อมูลจังหวัดทั้งหมดเข้าหน่วยความจำ รับคำขอจากหน้าเว็บ (➜ frontend/app.js และ ➜ frontend/extras.js) แล้วเรียกอัลกอริทึมใน algorithm/ ได้แก่ ➜ greedy_solve() ใน algorithm/greedy.py ➜ genetic_solve() ใน algorithm/genetic.py ➜ hybrid_solve() ใน algorithm/hybrid.py ➜ reoptimize_solve() ใน algorithm/hybrid.py และ ➜ nsga2_solve() ใน algorithm/pareto.py จากนั้นจัดงบ ตรวจและซ่อมแผนฝั่งเซิร์ฟเวอร์ก่อนส่ง JSON กลับ เซิร์ฟเวอร์ยังให้บริการไฟล์หน้าเว็บแบบ static ด้วย

บรรทัด 1–48  นำเข้าและตั้งค่าเริ่มต้น
1  # -*- coding: utf-8 -*-
2  """
3  main.py - FastAPI Backend สำหรับระบบ WeEasyTrip
4
5  Endpoints:
6    GET  /api/health    — ตรวจสอบสถานะ API
7    GET  /api/pois      — ดึงข้อมูล POI และโรงแรมทั้งหมด
8    POST /api/packages  — สร้าง 3 แพ็กเกจ (Budget / Standard / Premium)
9    POST /api/recompute — คำนวณใหม่หลังผู้ใช้แก้ไข route
10  """
11  import sys, os, time, random, secrets, threading, asyncio
12  from typing import List, Optional
13
14  THIS_DIR = os.path.dirname(os.path.abspath(__file__))
15  sys.path.insert(0, os.path.join(os.path.dirname(THIS_DIR), 'algorithm'))
16
17  from fastapi import FastAPI, HTTPException, Header, Request
18  from fastapi.middleware.cors import CORSMiddleware
19  from fastapi.responses import JSONResponse
20  from fastapi.staticfiles import StaticFiles
21  from pydantic import BaseModel, Field
22
23  from utils import load_data, evaluate_route, set_travel_profile, haversine_km, MAX_ATTRS
24  from greedy import greedy_solve
25  from genetic import genetic_solve
26  from hybrid import hybrid_solve, reoptimize_solve, infeasible_locks
27  from pareto import nsga2_solve
28
29  import json
30  import math
31  DATA_DIR = os.path.join(os.path.dirname(THIS_DIR), 'data')
32  with open(os.path.join(DATA_DIR, 'provinces.json'), encoding='utf-8') as _f:
33      PROVINCES = json.load(_f)
34  DEFAULT_PROVINCE = 'phuket'
35  try:   # จังหวัดที่ผ่านเกณฑ์ผ่อนปรน (ข้อมูลน้อย) — ใช้แสดงป้ายเตือนที่หน้าเว็บ
36      with open(os.path.join(DATA_DIR, 'provinces_status.json'), encoding='utf-8') as _f:
37          SPARSE = {k for k, v in json.load(_f).items() if v.get('sparse')}
38  except Exception:
39      SPARSE = set()
40  sys.path.insert(0, DATA_DIR)
41  from thai_provinces import PROVINCES_77, EXTRA_AREAS   # รายชื่อ 77 จังหวัด (ใช้แสดงรายการที่ยังไม่พร้อม)
42  # นโยบาย RL ที่ฝึกแล้ว (algorithm/rl_policy.json) ใช้เป็น seed เพิ่มของ Hybrid เมื่อเลือก algorithm='hybrid_rl' (โหมด Developer)
43  try:
44      import numpy as _np
45      RL_THETA = _np.array(json.load(open(os.path.join(os.path.dirname(THIS_DIR), 'algorithm', 'rl_policy.json'), encoding='utf-8'))['theta'])
46  except Exception:
47      RL_THETA = None
48  DIVERSITY_WEIGHT = 1.5   # น้ำหนักความหลากหลายของหมวดใน fitness ของ Hybrid (0 = แบบ Project 1)
บรรทัด 1–10: docstring ระบุ endpoint หลัก (health, pois, packages, recompute) ส่วน endpoint อื่น ๆ ดูด้านล่างของไฟล์
บรรทัด 11: นำเข้าโมดูลมาตรฐาน (sys, os, time, random, secrets, threading, asyncio)
บรรทัด 12: นำเข้า type hint
บรรทัด 14: THIS_DIR โฟลเดอร์ของไฟล์นี้
บรรทัด 15: เพิ่มโฟลเดอร์ algorithm/ เข้า sys.path เพื่อให้ import utils import hybrid ทำงานได้
บรรทัด 17–21: นำเข้า FastAPI, ตัวจัดการ CORS, JSONResponse, StaticFiles (เสิร์ฟหน้าเว็บ) และ Pydantic (BaseModel, Field) สำหรับตรวจรูปแบบคำขอ
บรรทัด 23: นำเข้าจาก ➜ algorithm/utils.py ได้แก่ load_data evaluate_route set_travel_profile haversine_km MAX_ATTRS
บรรทัด 24–27: นำเข้าอัลกอริทึมทั้งหมด ➜ algorithm/greedy.py ➜ algorithm/genetic.py ➜ algorithm/hybrid.py ➜ algorithm/pareto.py
บรรทัด 29–30: นำเข้า json math
บรรทัด 31: DATA_DIR โฟลเดอร์ data/
บรรทัด 32–33: โหลด provinces.json (ข้อมูลโปรไฟล์ของแต่ละจังหวัด เช่น ตัวคูณถนน ความเร็ว ชื่อ) เป็น PROVINCES
บรรทัด 34: DEFAULT_PROVINCE = 'phuket'
บรรทัด 35–39: โหลดสถานะจังหวัด provinces_status.json เก็บชุด SPARSE (จังหวัดข้อมูลน้อย) ใช้แสดงป้ายเตือนที่หน้าเว็บ ถ้าอ่านไม่ได้ใช้ชุดว่าง
บรรทัด 40: เพิ่ม DATA_DIR เข้า path
บรรทัด 41: นำเข้ารายชื่อ 77 จังหวัดจาก ➜ data/thai_provinces.py (ใช้แสดงจังหวัดที่ยังไม่พร้อม)
บรรทัด 42–47: โหลดนโยบาย RL ที่ฝึกแล้วจาก algorithm/rl_policy.json เป็น RL_THETA (ใช้เมื่อเลือก hybrid_rl ในโหมด Developer ดู ➜ algorithm/rl.py) ถ้าโหลดไม่ได้เป็น None
บรรทัด 48: DIVERSITY_WEIGHT = 1.5 น้ำหนักความหลากหลายของหมวดใน fitness ของ Hybrid (0 = แบบ Project 1)
บรรทัด 50–60  โหลดข้อมูลทุกจังหวัดเข้าหน่วยความจำ
50  # slug -> {'pois','hotels','poi_by_id','hotel_by_id'} (เฉพาะจังหวัดที่มีไฟล์ข้อมูลแล้ว)
51  DATA = {}
52  for _slug in list(PROVINCES):
53      _path = os.path.join(DATA_DIR, 'provinces', f'{_slug}.json')
54      if not os.path.exists(_path):
55          del PROVINCES[_slug]
56          continue
57      _pois, _hotels = load_data(_path)
58      DATA[_slug] = {'pois': _pois, 'hotels': _hotels,
59                     'poi_by_id': {p['id']: p for p in _pois},
60                     'hotel_by_id': {h['id']: h for h in _hotels}}
บรรทัด 50–51: DATA dict จาก slug เป็น {จุด โรงแรม ดัชนีตาม id}
บรรทัด 52–56: วนทุกจังหวัดใน PROVINCES ถ้าไม่มีไฟล์ data/provinces/<slug>.json ลบจังหวัดนั้นออกจากรายการ
บรรทัด 57: โหลดจุดและโรงแรมด้วย ➜ load_data() ใน algorithm/utils.py
บรรทัด 58–60: เก็บจุด โรงแรม และดัชนี poi_by_id hotel_by_id เพื่อค้นหาด้วย id ได้เร็ว
บรรทัด 63–88  รวมหลายจังหวัดและเลือกจังหวัด
63  COMBO = {}   # 'a+b' -> ข้อมูลรวมหลายจังหวัด (ทริปข้ามจังหวัดข้างเคียง)
64
65
66  def _combo(slug):
67      parts = slug.split('+')
68      if len(parts) > 3 or len(set(parts)) != len(parts) or any(p not in DATA for p in parts):
69          return None
70      if slug not in COMBO:
71          pois = [{**x, 'id': f'{s}.{x["id"]}'} for s in parts for x in DATA[s]['pois']]   # id ซ้ำข้ามจังหวัด (P01) จึงใส่ prefix
72          hotels = [{**x, 'id': f'{s}.{x["id"]}'} for s in parts for x in DATA[s]['hotels']]
73          COMBO[slug] = {'pois': pois, 'hotels': hotels, 'poi_by_id': {p['id']: p for p in pois},
74                         'hotel_by_id': {h['id']: h for h in hotels}}
75      return COMBO[slug]
76
77
78  def get_province(slug):
79      if slug not in DATA:
80          d = _combo(slug)
81          if d is None:
82              raise HTTPException(status_code=404, detail=f'Province {slug} not found')
83          pv = PROVINCES[slug.split('+')[0]]   # โปรไฟล์เวลาเดินทางใช้ของจังหวัดแรก
84          set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
85          return d
86      pv = PROVINCES[slug]   # ตั้งโปรไฟล์ระยะ/เวลาเดินทางของจังหวัดให้ request นี้
87      set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
88      return DATA[slug]
บรรทัด 63: COMBO แคชข้อมูลทริปข้ามจังหวัด (slug รูปแบบ a+b)
บรรทัด 66–75: _combo รวมข้อมูลของ 2-3 จังหวัดที่ไม่ซ้ำกันและมีข้อมูลครบ ใส่คำนำหน้า slug. ที่ id (เพราะ id เช่น P01 ซ้ำข้ามจังหวัด) แล้วแคชไว้ คืน None ถ้าไม่ถูกต้อง
บรรทัด 78–88: get_province คืนข้อมูลของ slug ที่ขอ ถ้าไม่ใช่จังหวัดเดี่ยวลอง _combo ไม่พบตอบ 404 และ **ตั้งโปรไฟล์เวลาเดินทางของจังหวัดนั้นให้ request ปัจจุบัน** ด้วย ➜ set_travel_profile() ใน algorithm/utils.py (กรณีรวมจังหวัดใช้โปรไฟล์ของจังหวัดแรก)
บรรทัด 95–165  โมเดลข้อมูลคำขอ/คำตอบ (Pydantic)
95  class Preferences(BaseModel):
96      """ความชอบของผู้ใช้ — กรอง/ถ่วงน้ำหนัก POI ก่อนส่งให้อัลกอริทึม"""
97      liked: List[str] = []      # หมวดที่ชอบ (beach, temple, ...) ได้คะแนนถ่วงเพิ่มตอนเลือก
98      avoided: List[str] = []    # หมวดที่ไม่ต้องการ (ตัดออกจากตัวเลือก; ไม่รวม restaurant)
99      diet: str = 'none'         # 'none' | 'vegetarian' | 'halal' (กรองร้านอาหารตามแท็กใน OSM)
100
101
102  class PackageRequest(BaseModel):
103      province: str = Field(DEFAULT_PROVINCE, description="slug ของจังหวัด (ดู /api/provinces)")
104      preferences: Optional[Preferences] = None
105      budget: float = Field(..., ge=1000, le=100000)
106      days: int = Field(..., ge=1, le=7)
107      travelers: int = Field(1, ge=1, le=10)
108      seed: Optional[int] = Field(None, description="Random seed; None = random every call")
109      algorithm: Optional[str] = Field('hybrid', description="'greedy' | 'ga' | 'hybrid' | 'hybrid_rl'")
110      include_hotel: Optional[bool] = Field(True, description="รวมค่าโรงแรมในงบหรือไม่")
111
112
113  class RecomputeRequest(BaseModel):
114      province: str = DEFAULT_PROVINCE
115      hotel_id: str
116      days: int
117      budget: float
118      routes: List[List[str]]
119      travelers: int = 1
120
121
122  class ReoptimizeRequest(BaseModel):
123      province: str = DEFAULT_PROVINCE
124      tier: str = 'Custom'
125      hotel_id: str
126      days: int = Field(..., ge=1, le=7)
127      budget: float = Field(..., ge=1000, le=100000)   # งบรวมของผู้ใช้ (บาท)
128      travelers: int = Field(1, ge=1, le=10)
129      include_hotel: bool = True
130      routes: List[List[str]]
131      locked: List[str] = []      # POI ที่ผู้ใช้เลือกเอง ต้องคงไว้
132      excluded: List[str] = []    # POI ที่ผู้ใช้ลบ ห้ามกลับมา
133      preferences: Optional[Preferences] = None
134      seed: Optional[int] = None
135
136
137  class DayDetail(BaseModel):
138      day: int
139      pois: List[dict]
140      distance_km: float
141      time_min: float
142      cost: float
143      score: float
144      arrivals: List[list] = []   # [[poi_id, นาทีที่ถึง (นับจาก 00:00)], ...] ใช้สร้างตารางเวลา/ไฟล์ปฏิทิน
145
146
147  class Package(BaseModel):
148      tier: str
149      hotel: dict
150      days: List[DayDetail]
151      total_score: float
152      total_activity_cost: float
153      total_hotel_cost: float
154      total_cost: float
155      runtime_ms: float
156      valid: bool
157      violations: List[str]
158      notes: List[str] = []   # ข้อความแจ้งผู้ใช้ เช่น จุดที่เลือกแต่ใส่ในแผนไม่ได้
159      objectives: dict = {}   # Pareto: score / diversity / distance_km / cost ของแผนนี้
160
161
162  class PackageResponse(BaseModel):
163      request: dict
164      packages: List[Package]
165
บรรทัด 95–99: Preferences ความชอบ: หมวดที่ชอบ (liked) หมวดที่ไม่เอา (avoided) และอาหาร (diet: none, vegetarian, halal) ใช้ที่ apply_preferences
บรรทัด 102–110: PackageRequest คำขอสร้างแพ็กเกจ: จังหวัด ความชอบ งบ (1,000–100,000) จำนวนวัน (1–7) จำนวนคน (1–10) seed อัลกอริทึม และธงรวมโรงแรมหรือไม่
บรรทัด 113–119: RecomputeRequest คำขอคำนวณใหม่หลังผู้ใช้แก้ลำดับ: จังหวัด โรงแรม วัน งบ แผนเป็นรายการ id จำนวนคน
บรรทัด 122–134: ReoptimizeRequest คำขอปรับแผนใหม่ด้วย Hybrid: เพิ่ม locked (จุดที่ผู้ใช้เลือก ต้องคงไว้) และ excluded (จุดที่ลบ ห้ามกลับ) ใช้กับ ➜ reoptimize_solve() ใน algorithm/hybrid.py
บรรทัด 137–144: DayDetail รายละเอียดวัน (จุด ระยะ เวลา ค่าใช้จ่าย คะแนน เวลาถึงแต่ละจุดสำหรับตารางเวลา/ปฏิทิน)
บรรทัด 147–159: Package แพ็กเกจหนึ่งระดับ: โรงแรม รายวัน คะแนน ค่าใช้จ่ายกิจกรรม/โรงแรม/รวม เวลารัน ธง valid ข้อความผิดข้อจำกัด หมายเหตุถึงผู้ใช้ และวัตถุประสงค์แบบ Pareto
บรรทัด 162–164: PackageResponse ห่อคำขอกับแพ็กเกจที่ได้
บรรทัด 171–191  แปลงแผนเป็นรายละเอียดรายวัน
171  def make_day_details(routes_per_day, hotel, travelers=1):
172      """แปลง routes เป็น List[DayDetail] พร้อม metadata (ระยะทาง, เวลา, ค่าใช้จ่าย, score)"""
173      eval_result = evaluate_route(routes_per_day, hotel, budget=float('inf'))
174      days = []
175      for i, day_pois in enumerate(routes_per_day):
176          det = eval_result['days_detail'][i]
177          days.append(DayDetail(
178              day=i + 1,
179              pois=[{
180                  'id': p['id'], 'name_th': p['name_th'], 'name_en': p['name_en'],
181                  'category': p['category'], 'lat': p['lat'], 'lng': p['lng'],
182                  'score': p['score'], 'cost': p['cost'] * travelers,
183                  'duration_min': p['duration_min'],
184              } for p in day_pois],
185              distance_km=det['distance_km'],
186              time_min=det['time_min'],
187              cost=det['cost'] * travelers,
188              score=det['score'],
189              arrivals=[list(a) for a in det.get('arrivals', [])]
190          ))
191      return days, eval_result
บรรทัด 171–172: ประกาศ make_day_details แปลงแผน (รายการ POI รายวัน) เป็น DayDetail
บรรทัด 173: ประเมินด้วย ➜ evaluate_route() ใน algorithm/utils.py (งบเป็นอนันต์เพราะต้องการแค่ตัวเลข)
บรรทัด 174–190: วนทีละวัน ใส่ข้อมูลจุด (id ชื่อไทย/อังกฤษ หมวด พิกัด คะแนน ค่าใช้จ่ายคูณจำนวนคน ระยะเวลา) ระยะทาง เวลา ค่าใช้จ่ายคูณจำนวนคน คะแนน และเวลาถึง
บรรทัด 191: คืนรายละเอียดรายวันและผลประเมินดิบ
บรรทัด 194–272  `_prioritize_sights` จัดลำดับความสำคัญเมื่องบไม่พอ
194  def _prioritize_sights(routes, hotel, sight_pool, rest_pool, budget_pp):
195      """จัดลำดับความสำคัญเมื่องบไม่พอ: สถานที่ท่องเที่ยวต้องครบ (MAX_ATTRS ต่อวัน) ทุกวัน ส่วนมื้ออาหารเป็นรอง
196         1) ถ้าเกินงบ ตัดร้านอาหารของวันท้ายสุดก่อน (แล้วค่อยตัดสถานที่ที่มีค่าเข้าชม)
197         2) เติมสถานที่ท่องเที่ยวที่ยังไม่ได้ใช้ (ฟรี/ถูกก่อน) จนครบทุกวันเท่าที่เวลาและเวลาเปิด-ปิดอนุญาต
198         3) ถ้างบเหลือ เติมร้านอาหารคืนให้วันแรกก่อน (ร้านที่เพิ่มระยะทางน้อยที่สุด)"""
199      from utils import evaluate_route as _ev
200      routes = [list(d) for d in routes]
201      cost = lambda: sum(p['cost'] for d in routes for p in d)
202      ok = lambda day: _ev([day], hotel, float('inf'))['valid']
203      dist = lambda day: _ev([day], hotel, float('inf'))['days_detail'][0]['distance_km'] if day else 0.0
204
205      if cost() > budget_pp:
206          # งบตึง: ถอดร้านอาหารทั้งหมดออกก่อน (ร้านเดิมมักไกลกันและกินงบ) แล้วเติมสถานที่ท่องเที่ยวให้ครบ จากนั้นค่อยเติมร้านที่ใกล้ที่สุดเท่าที่งบเหลือ
207          routes = [[p for p in day if p['category'] != 'restaurant'] for day in routes]
208          while cost() > budget_pp:
209              paid = [(p['cost'], d, i) for d, day in enumerate(routes) for i, p in enumerate(day) if p['cost'] > 0]
210              if not paid:
211                  break
212              _, d, i = max(paid); routes[d].pop(i)
213
214      def add_best(d, pool, want_cat):
215          used = {p['id'] for day in routes for p in day}
216          left = budget_pp - cost()
217          base = dist(routes[d]); best = None
218          for c in pool:
219              if c['id'] in used or c['cost'] > left or (c['category'] == 'restaurant') != want_cat:
220                  continue
221              for pos in range(len(routes[d]) + 1):
222                  trial = routes[d][:pos] + [c] + routes[d][pos:]
223                  if not ok(trial):
224                      continue
225                  key = ((dist(trial) - base) + 0.1 * c['cost'], c['cost']) if want_cat else ((dist(trial) - base) - 0.1 * c['score'], c['cost'])
226                  if best is None or key < best[0]:
227                      best = (key, trial)
228          if best:
229              routes[d] = best[1]
230          return best is not None
231
232      def nearer_meals(d):
233          # ร้านที่ไกลจนวันเต็มเวลาแล้วใส่ที่เที่ยวไม่ได้ (เช่น สตูลวันละ 300 กม.): สลับเป็นร้านที่ทำให้ระยะขับของวันนั้นสั้นลงมากที่สุด ถ้าราคาไม่เกินงบ
234          for _ in range(4):
235              base = dist(routes[d]); best = None
236              used = {p['id'] for day in routes for p in day}
237              for i, p in enumerate(routes[d]):
238                  if p['category'] != 'restaurant':
239                      continue
240                  for c in rest_pool:
241                      if c['id'] in used or cost() - p['cost'] + c['cost'] > budget_pp:
242                          continue
243                      trial = routes[d][:i] + [c] + routes[d][i + 1:]
244                      if ok(trial) and (best is None or dist(trial) < best[0]):
245                          best = (dist(trial), trial)
246              if best and best[0] < base - 1.0:
247                  routes[d] = best[1]
248              else:
249                  break
250
251      for d in range(len(routes)):
252          if sum(1 for p in routes[d] if p['category'] != 'restaurant') < MAX_ATTRS:
253              nearer_meals(d)
254          if sum(1 for p in routes[d] if p['category'] != 'restaurant') < MAX_ATTRS and dist(routes[d]) > 120:
255              routes[d] = []   # วันที่เต็มเวลาเพราะขับไกลมาก (ร้านและที่เที่ยวอยู่ห่างโรงแรมเป็นร้อยกิโลเมตร): ล้างแล้วสร้างวันใหม่จากสถานที่ใกล้โรงแรม
256      for d in range(len(routes)):
257          while sum(1 for p in routes[d] if p['category'] != 'restaurant') < MAX_ATTRS and add_best(d, sight_pool, False):
258              pass
259      # วันที่ยังขาดสถานที่เพราะงบหมด: ถอดร้านอาหารของวันท้ายสุด (ราคาแพงสุดก่อน) เพื่อเอางบมาเติมสถานที่ท่องเที่ยว (สถานที่ครบสำคัญกว่ามื้ออาหาร)
260      for d in range(len(routes)):
261          for _ in range(8):
262              if sum(1 for p in routes[d] if p['category'] != 'restaurant') >= MAX_ATTRS or add_best(d, sight_pool, False):
263                  continue
264              cands = [(dd, i, p['cost']) for dd in range(len(routes) - 1, d - 1, -1) for i, p in enumerate(routes[dd]) if p['category'] == 'restaurant' and p['cost'] > 0]
265              if not cands:
266                  break
267              dd, i, _c = max(cands, key=lambda c: (c[0], c[2]))
268              routes[dd].pop(i)
269      for d in range(len(routes)):
270          while sum(1 for p in routes[d] if p['category'] == 'restaurant') < 2 and add_best(d, rest_pool, True):
271              pass
272      return routes
บรรทัด 194–198: ประกาศและ docstring: ที่เที่ยวต้องครบ 4 จุดต่อวันก่อน มื้ออาหารเป็นรอง: (1) ถ้าเกินงบตัดร้านอาหารก่อน (2) เติมที่เที่ยวที่ยังไม่ใช้จนครบ (3) ถ้างบเหลือเติมร้านคืนให้วันแรกก่อน ใช้กับแพ็กเกจที่สร้างผ่านหน้าเว็บเท่านั้น (ไม่ได้ใช้ในการทดลองบทที่ 4)
บรรทัด 199–203: ตั้งฟังก์ชันย่อย: cost ค่าใช้จ่ายรวม ok ตรวจวันนั้น valid ด้วย ➜ evaluate_route() ใน algorithm/utils.py และ dist ระยะของวัน
บรรทัด 205–212: ถ้าเกินงบ ถอดร้านอาหารทั้งหมด แล้วถอดจุดที่มีค่าเข้าแพงสุดจนอยู่ในงบ
บรรทัด 214–230: ฟังก์ชัน add_best เพิ่มจุดที่ดีที่สุดให้วันที่ d: ลองแทรกจุดที่ยังไม่ใช้ทุกตำแหน่ง ที่ผ่านข้อจำกัดและอยู่ในงบ เลือกตามระยะที่เพิ่มน้อยที่สุด (ที่เที่ยวมีโบนัสตามคะแนน ร้านมีโทษตามราคา)
บรรทัด 232–249: ฟังก์ชัน nearer_meals สลับร้านที่ไกลมากเป็นร้านที่ทำให้ระยะขับของวันสั้นลงมากที่สุดถ้างบพอ (เช่น สตูลวันละ 300 กม.) วนไม่เกิน 4 รอบ
บรรทัด 251–255: สำหรับแต่ละวัน ถ้าที่เที่ยวไม่ครบให้ลอง nearer_meals และถ้ายังไม่ครบและขับเกิน 120 กม. ให้ล้างวันนั้นแล้วสร้างใหม่จากสถานที่ใกล้โรงแรม
บรรทัด 256–258: เติมที่เที่ยวให้ครบทุกวัน
บรรทัด 259–268: วันที่ยังขาดเพราะงบหมด ถอดร้านอาหารของวันท้ายสุด (แพงสุดก่อน) เอางบมาเติมที่เที่ยว
บรรทัด 269–271: เติมร้านอาหารให้วันแรก ๆ ให้ครบ 2 ร้านเท่าที่งบเหลือ
บรรทัด 272: คืนแผน
บรรทัด 275–340  `_trim_to_budget` ตัดให้อยู่ในงบ (เฟส 1-3)
275  def _trim_to_budget(routes, hotel, max_activity_budget, travelers, pois):
276      """4-phase budget + time-window enforcement:
277         1) Swap expensive restaurants → cheaper unused
278         2) Remove paid attractions (highest cost first)
279         3) Remove any POI (incl. restaurants) if still over budget
280         4) Remove POIs causing time-window violations
281      """
282      import re as _re
283      from utils import evaluate_route as _eval
284
285      def _check(rts):
286          r = _eval(rts, hotel, budget=float('inf'))
287          # Budget ครอบคลุมเฉพาะ ค่าเข้า + ค่าอาหาร (per-person × travelers)
288          # ค่าเดินทาง (transportation) ถือเป็น overhead ไม่นับในงบกิจกรรม
289          poi_cost = sum(p['cost'] for day in rts for p in day) * travelers
290          return poi_cost, r
291
292      used_ids = {p['id'] for day in routes for p in day}
293      unused_rest = sorted(
294          [p for p in pois if p['category'] == 'restaurant' and p['id'] not in used_ids],
295          key=lambda x: (not x.get('_diet'), x['cost']))   # ร้านที่ตรงความต้องการด้านอาหารเป็นตัวสลับก่อน
296
297      # Phase 1: สลับร้านอาหารแพงด้วยร้านที่ถูกกว่า
298      for cheap_rest in unused_rest:
299          total_act, _ = _check(routes)
300          if total_act <= max_activity_budget:
301              break
302          worst_d, worst_i, worst_cost = None, None, cheap_rest['cost']
303          for di, day in enumerate(routes):
304              for pi, p in enumerate(day):
305                  if p['category'] == 'restaurant' and p['cost'] > worst_cost:
306                      worst_cost = p['cost']; worst_d, worst_i = di, pi
307          if worst_d is None:
308              break
309          old_id = routes[worst_d][worst_i]['id']
310          routes[worst_d][worst_i] = cheap_rest
311          used_ids.discard(old_id)
312          used_ids.add(cheap_rest['id'])
313
314      # Phase 2: ลบ attraction ที่มีค่าเข้าชม (เริ่มจากแพงสุด)
315      while True:
316          total_act, _ = _check(routes)
317          if total_act <= max_activity_budget:
318              break
319          worst_d, worst_i, worst_cost = None, None, 0
320          for di, day in enumerate(routes):
321              for pi, p in enumerate(day):
322                  if p['category'] != 'restaurant' and p['cost'] > worst_cost:
323                      worst_cost = p['cost']; worst_d, worst_i = di, pi
324          if worst_d is None:
325              break
326          routes[worst_d].pop(worst_i)
327
328      # Phase 3: ลบ POI ใดก็ได้รวมถึงร้านอาหาร ถ้ายังเกินงบ
329      while True:
330          total_act, _ = _check(routes)
331          if total_act <= max_activity_budget:
332              break
333          worst_d, worst_i, worst_cost = None, None, -1
334          for di, day in enumerate(routes):
335              for pi, p in enumerate(day):
336                  if p['cost'] > worst_cost:
337                      worst_cost = p['cost']; worst_d, worst_i = di, pi
338          if worst_d is None:
339              break
340          routes[worst_d].pop(worst_i)
บรรทัด 275–281: ประกาศและ docstring: 4 เฟส (1) สลับร้านแพงเป็นร้านถูก (2) ลบที่เที่ยวมีค่าเข้า (3) ลบจุดใดก็ได้ (4) ลบจุดที่ผิดเวลา
บรรทัด 282–283: นำเข้า re และ evaluate_route
บรรทัด 285–290: ฟังก์ชัน _check คืนค่าใช้จ่าย (ค่าเข้า+ค่าอาหาร) × จำนวนคน และผลประเมิน (ค่าเดินทางไม่นับในงบ)
บรรทัด 292–295: เตรียมร้านอาหารที่ยังไม่ใช้ เรียงให้ร้านที่ตรงความต้องการด้านอาหาร (_diet) ก่อน แล้วตามราคา
บรรทัด 297–312: เฟส 1 สลับร้านที่แพงกว่าด้วยร้านถูกที่ยังไม่ใช้ จนอยู่ในงบ
บรรทัด 314–326: เฟส 2 ลบที่เที่ยวที่มีค่าเข้าชม เริ่มจากแพงสุดจนอยู่ในงบ
บรรทัด 328–340: เฟส 3 ถ้ายังเกินงบ ลบจุดใดก็ได้ (รวมร้านอาหาร) เริ่มจากแพงสุด
บรรทัด 342–365  `_trim_to_budget` เฟส 4 และคืนผล
342      # Phase 4: ลบ POI ที่ไปถึงหลังเวลาปิด
343      for _ in range(30):
344          _, result = _check(routes)
345          tw = [v for v in result['violations'] if 'หลังเวลาปิด' in v]
346          if not tw:
347              break
348          removed = False
349          for viol in tw:
350              m = _re.search(r'ไปถึง (\S+) หลังเวลาปิด', viol)
351              if not m:
352                  continue
353              bad_id = m.group(1)
354              for di, day in enumerate(routes):
355                  for pi, p in enumerate(day):
356                      if p['id'] == bad_id:
357                          routes[di].pop(pi)
358                          removed = True
359                          break
360                  if removed:
361                      break
362          if not removed:
363              break
364
365      return routes
บรรทัด 342–363: เฟส 4 วนไม่เกิน 30 รอบ: ดึง id ของจุดที่ไปถึงหลังเวลาปิดจากข้อความผิดข้อจำกัดด้วย regex แล้วลบจุดนั้นออกจากแผน ถ้าไม่มีอะไรให้ลบหยุด
บรรทัด 365: คืนแผนที่ตัดให้อยู่ในงบและเวลาแล้ว
บรรทัด 368–401  ตัวเลือกตามความชอบ
368  LIKE_BOOST = 1.0   # คะแนนถ่วงเพิ่มให้ POI ในหมวดที่ผู้ใช้ชอบ (ใช้เลือกเท่านั้น ไม่นับในคะแนนที่รายงาน)
369  DIET_BOOST = 4.0   # ถ่วงร้านที่ตรงความต้องการด้านอาหารเมื่อร้านที่ตรงมีไม่พอทั้งทริป
370
371
372  def apply_preferences(pois, prefs, days):
373      """สร้างกลุ่ม POI สำหรับอัลกอริทึมตามความชอบ คืน (pool, notes)
374         - avoided: ตัด POI หมวดนั้นออก (ไม่แตะร้านอาหาร)
375         - diet: ใช้เฉพาะร้านที่มีแท็ก ถ้าน้อยกว่าจำนวนมื้อที่ต้องใช้ จะเสริมร้านทั่วไปและแจ้งผู้ใช้
376         - liked: คัดลอก POI พร้อมบวกคะแนน LIKE_BOOST เพื่อให้ถูกเลือกบ่อยขึ้น
377         pool คือสำเนา — ต้อง restore_scores() กลับเป็นออบเจ็กต์ต้นฉบับก่อนสร้างแพ็กเกจ"""
378      notes = []
379      if prefs is None:
380          return pois, notes
381      cats = {p['category'] for p in pois}
382      avoided = {c for c in prefs.avoided if c in cats and c != 'restaurant'}
383      liked = {c for c in prefs.liked if c in cats and c != 'restaurant'} - avoided
384      pool = [p for p in pois if p['category'] not in avoided]
385      if liked:
386          # _base = คะแนนจริง ใช้กำหนดช่วงคะแนนของแต่ละ tier ไม่ให้ที่ชอบหลุดจาก tier ประหยัด
387          pool = [dict(p, score=round(p['score'] + LIKE_BOOST, 2), _base=p['score']) if p['category'] in liked else p for p in pool]
388      if prefs.diet in ('vegetarian', 'halal'):
389          need = 2 * days + 2
390          match = [p for p in pool if p['category'] == 'restaurant' and prefs.diet in p.get('tags', [])]
391          label = 'มังสวิรัติ' if prefs.diet == 'vegetarian' else 'ฮาลาล'
392          if len(match) >= need:
393              pool = [p for p in pool if p['category'] != 'restaurant' or p in match]
394          elif match:
395              # ไม่พอทั้งทริป: ถ่วงคะแนนร้านที่ตรงให้ถูกเลือกก่อน ที่เหลือเสริมด้วยร้านทั่วไป
396              ids = {p['id'] for p in match}
397              pool = [dict(p, score=round(p['score'] + DIET_BOOST, 2), _base=p.get('_base', p['score']), _diet=True) if p['id'] in ids else p for p in pool]
398              notes.append(f'ร้านอาหาร{label}ในฐานข้อมูลมีเพียง {len(match)} ร้าน ไม่พอสำหรับทั้งทริป จึงใช้ร้านเหล่านี้ก่อนแล้วเสริมด้วยร้านทั่วไป (ไม่รับประกันว่ารองรับอาหาร{label})')
399          else:
400              notes.append(f'ไม่พบข้อมูลร้านอาหาร{label}ของจังหวัดนี้ในฐานข้อมูล จึงใช้ร้านทั่วไป (ไม่รับประกันว่ารองรับอาหาร{label})')
401      return pool, notes
บรรทัด 368: LIKE_BOOST = 1.0 คะแนนที่บวกให้หมวดที่ผู้ใช้ชอบ (ใช้เลือกเท่านั้น ไม่นับในคะแนนที่รายงาน)
บรรทัด 369: DIET_BOOST = 4.0 คะแนนถ่วงร้านที่ตรงความต้องการด้านอาหารเมื่อร้านที่ตรงมีไม่พอ
บรรทัด 372–377: ประกาศ apply_preferences และ docstring: คืน (กลุ่มจุด ข้อความแจ้งผู้ใช้) ตัดหมวดที่ไม่เอา เสริมร้านตามอาหารที่เลือก และบวกคะแนนหมวดที่ชอบ ผลเป็นสำเนา ต้องคืนวัตถุต้นฉบับก่อนสร้างแพ็กเกจ
บรรทัด 378–380: ถ้าไม่มีความชอบ คืนจุดเดิมทั้งหมด
บรรทัด 381–384: คำนวณชุดหมวดที่มีอยู่ หมวดที่ไม่เอา (ไม่รวมร้านอาหาร) หมวดที่ชอบ (ตัดหมวดที่ขัดกัน) และตัดจุดหมวดที่ไม่เอาออก
บรรทัด 385–387: ถ้ามีหมวดที่ชอบ ทำสำเนาจุดในหมวดนั้นพร้อมบวกคะแนน LIKE_BOOST และเก็บคะแนนจริงใน _base (ใช้กำหนดช่วงคะแนนของแต่ละ tier)
บรรทัด 388–391: ถ้าเลือกมังสวิรัติหรือฮาลาล คำนวณจำนวนมื้อที่ต้องใช้ (2 มื้อ/วัน + 2) และหาร้านที่มีแท็กตรง
บรรทัด 392–393: ถ้าร้านที่ตรงมีพอ ใช้เฉพาะร้านที่ตรง
บรรทัด 394–398: ถ้ามีไม่พอ บวกคะแนนร้านที่ตรง (_diet) ให้ถูกเลือกก่อน เสริมร้านทั่วไป และเพิ่มข้อความแจ้งผู้ใช้
บรรทัด 399–400: ถ้าไม่มีร้านที่ตรงเลย ใช้ร้านทั่วไปและแจ้งผู้ใช้
บรรทัด 401: คืนกลุ่มจุดและข้อความ
บรรทัด 404–432  คืนวัตถุต้นฉบับและสร้างแพ็กเกจ
404  def restore_originals(routes, originals):
405      """แทนที่ POI ที่ถูกถ่วงคะแนนด้วยออบเจ็กต์ต้นฉบับ (คะแนนที่รายงานต้องเป็นคะแนนจริง)"""
406      return [[originals.get(p['id'], p) for p in day] for day in routes]
407
408
409  def build_package(tier, hotel, routes, days, budget, runtime_ms, travelers, pois,
410                    max_total_budget=None, hotel_cost_override=None):
411      """สร้าง Package object จาก routes และตัดงบประมาณให้อยู่ใน max_total_budget ที่กำหนด"""
412      nights = max(0, days - 1)
413      hotel_cost = hotel_cost_override if hotel_cost_override is not None else hotel['cost'] * nights
414      # ถ้ากำหนด max_total_budget ให้ตัดงบตาม
415      if max_total_budget is not None:
416          max_activity = max(0, max_total_budget - hotel_cost)
417          routes = _trim_to_budget(routes, hotel, max_activity, travelers, pois)
418      day_details, eval_result = make_day_details(routes, hotel, travelers)
419      activity_cost = sum(d.cost for d in day_details)
420      total = activity_cost + hotel_cost
421      violations = list(eval_result['violations'])
422      valid = eval_result['valid']
423      return Package(
424          tier=tier, hotel=hotel, days=day_details,
425          total_score=eval_result['total_score'] if valid else 0,
426          total_activity_cost=activity_cost,
427          total_hotel_cost=hotel_cost,
428          total_cost=total,
429          runtime_ms=runtime_ms,
430          valid=valid,
431          violations=violations
432      )
บรรทัด 404–406: restore_originals แทนจุดที่ถูกบวกคะแนนด้วยออบเจ็กต์ต้นฉบับ เพื่อให้คะแนนที่รายงานเป็นคะแนนจริง
บรรทัด 409–411: ประกาศ build_package และ docstring
บรรทัด 412–413: จำนวนคืน = วัน − 1 และค่าโรงแรม (คูณจำนวนคืน หรือใช้ค่าที่กำหนดทับ)
บรรทัด 415–417: ถ้ามีงบรวมสูงสุด คำนวณงบกิจกรรมที่เหลือจากค่าโรงแรม และตัดแผนด้วย _trim_to_budget
บรรทัด 418–420: แปลงแผนเป็นรายละเอียดรายวันด้วย make_day_details และรวมค่ากิจกรรมกับค่าโรงแรม
บรรทัด 421–422: ดึงข้อความผิดข้อจำกัดและธง valid
บรรทัด 423–432: คืนวัตถุ Package (คะแนนเป็น 0 ถ้าแผนไม่ valid)
บรรทัด 439–478  สร้างแอปและ middleware
439  app = FastAPI(title='WeEasyTrip API', version='1.0.0')
440  # ---------- จำกัดคำขอหนัก (Hybrid/GA ใช้ CPU 2–4 วินาที): 20 ครั้ง/นาที/IP และรันพร้อมกันได้ 2 งาน ----------
441  _HEAVY = ('/api/packages', '/api/pareto', '/api/reoptimize')   # /api/recompute คำนวณเบา ใช้ตอนลากวางบ่อย จึงไม่จำกัด
442  _HITS = {}                                  # ip -> [เวลาของคำขอล่าสุด]
443  _SLOTS = asyncio.Semaphore(2)
444  RATE_PER_MIN = int(os.environ.get('WET_RATE_PER_MIN', '20'))
445
446
447  @app.middleware('http')
448  async def revalidate_static(request: Request, call_next):
449      """ไฟล์หน้าเว็บ (html/css/js) ให้เบราว์เซอร์ตรวจเวอร์ชันใหม่ทุกครั้ง (ใช้ ETag/Last-Modified ไม่โหลดซ้ำถ้าไม่เปลี่ยน)
450      ไม่งั้นแก้ CSS/JS แล้วผู้ใช้ยังเห็นของเก่าจากแคช"""
451      resp = await call_next(request)
452      if not request.url.path.startswith('/api'):
453          resp.headers['Cache-Control'] = 'no-cache'
454      return resp
455
456
457  @app.middleware('http')
458  async def limit_heavy(request: Request, call_next):
459      if request.method == 'POST' and request.url.path in _HEAVY:
460          ip = request.client.host if request.client else '?'
461          now = time.time()
462          hits = [t for t in _HITS.get(ip, []) if now - t < 60]
463          if len(hits) >= RATE_PER_MIN:
464              return JSONResponse({'detail': 'ส่งคำขอถี่เกินไป รอสักครู่แล้วลองใหม่'}, status_code=429)
465          _HITS[ip] = hits + [now]
466          try:
467              await asyncio.wait_for(_SLOTS.acquire(), timeout=20)
468          except asyncio.TimeoutError:
469              return JSONResponse({'detail': 'เซิร์ฟเวอร์กำลังประมวลผลหลายงาน ลองใหม่อีกครั้ง'}, status_code=503)
470          try:
471              return await call_next(request)
472          finally:
473              _SLOTS.release()
474      return await call_next(request)
475
476
477  app.add_middleware(CORSMiddleware, allow_origins=['*'],
478                     allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
บรรทัด 439: สร้างแอป FastAPI ชื่อ WeEasyTrip API
บรรทัด 440–444: ตั้งตัวจำกัดคำขอหนัก: _HEAVY รายการ endpoint ที่ใช้ CPU มาก _HITS ประวัติคำขอต่อ IP _SLOTS สัญญาณจำกัดการรันพร้อมกัน 2 งาน และ RATE_PER_MIN 20 ครั้ง/นาที (ปรับได้ด้วยตัวแปรแวดล้อม)
บรรทัด 447–454: middleware revalidate_static ตั้ง Cache-Control: no-cache ให้ไฟล์หน้าเว็บ (ไม่ใช่ /api) เพื่อให้เบราว์เซอร์ตรวจเวอร์ชันใหม่ทุกครั้ง แก้ CSS/JS แล้วไม่ติดแคชเก่า
บรรทัด 457–474: middleware limit_heavy สำหรับ POST ที่หนัก: นับคำขอต่อ IP ใน 60 วินาที ถ้าเกินตอบ 429 รอสัญญาณคิวได้ไม่เกิน 20 วินาที ไม่ทันตอบ 503 และคืนสัญญาณหลังเสร็จ
บรรทัด 477–478: เปิด CORS ให้ทุกที่มา (ใช้ตอนเปิดหน้าเว็บจากพอร์ตอื่น)
บรรทัด 485–533  endpoint พื้นฐาน
485  BUILD = '2026-11-09-travelcost0-distw0.3-retry-mealfloor-autonohotel-sightsfirst-nocache-nearmeals-rebuilddays-dropmeals-hotelreuse'
486
487
488  @app.get('/api/health')
489  def health():
490      """ตรวจสอบสถานะ API — คืนจำนวน POI และโรงแรมที่โหลดไว้ (ทุกจังหวัดรวมกัน)"""
491      return {'status': 'ok', 'build': BUILD,   # เปลี่ยน BUILD ทุกครั้งที่แก้อัลกอริทึม เพื่อเช็กว่าเซิร์ฟเวอร์รันโค้ดล่าสุด
492              'pois': sum(len(d['pois']) for d in DATA.values()),
493              'hotels': sum(len(d['hotels']) for d in DATA.values()),
494              'provinces': len(DATA)}
495
496
497  def _max_days(slug):
498      """จำนวนวันสูงสุดที่ข้อมูลรองรับ: สถานที่ ≥ 3 จุด/วัน และร้านอาหาร ≥ 2 ร้าน/วัน (มื้อกลางวัน+เย็น ไม่ซ้ำร้าน) (ไม่งั้นมีวันว่าง)"""
499      pois = DATA[slug]['pois']
500      rest = sum(1 for p in pois if p['category'] == 'restaurant')
501      return max(1, min(7, (len(pois) - rest) // 3, rest // 2))
502
503
504  def _neighbors(slug, km=110, top=4):
505      """จังหวัดข้างเคียง (ศูนย์กลางห่างไม่เกิน km กม.) เรียงจากใกล้สุด — ใช้ทำทริปข้ามจังหวัด"""
506      c = PROVINCES[slug]['center']
507      def dist(o):   # กม. เส้นตรงโดยประมาณ (ไม่ผ่าน haversine_km เพราะคูณ road_factor ของ request ก่อนหน้า)
508          b = PROVINCES[o]['center']
509          return 111 * ((c[0] - b[0]) ** 2 + ((c[1] - b[1]) * math.cos(math.radians(c[0]))) ** 2) ** 0.5
510      ds = sorted((dist(o), o) for o in DATA if o != slug and o != 'samui')
511      return [o for d, o in ds if d <= km][:top]
512
513
514  @app.get('/api/provinces')
515  def get_provinces():
516      """รายการจังหวัดที่มีข้อมูล พร้อมศูนย์กลางแผนที่และจำนวน POI/โรงแรม"""
517      region = {p[0]: p[3] for p in PROVINCES_77}
518      region.update({k: v[2] for k, v in EXTRA_AREAS.items()})
519      return {'default': DEFAULT_PROVINCE,
520              'provinces': [{'slug': s, **PROVINCES[s], 'region': region.get(s, PROVINCES[s].get('region', '')),
521                             'pois': len(DATA[s]['pois']), 'hotels': len(DATA[s]['hotels']), 'sparse': s in SPARSE,
522                             'max_days': _max_days(s), 'neighbors': _neighbors(s)}
523                            for s in DATA],
524              'planned': [{'slug': p[0], 'name_th': p[1], 'name_en': p[2], 'region': p[3]}
525                          for p in PROVINCES_77 if p[0] not in DATA]}
526
527
528
529  @app.get('/api/pois')
530  def get_pois(province: str = DEFAULT_PROVINCE):
531      """ดึงรายการ POI และโรงแรมทั้งหมดของจังหวัด"""
532      d = get_province(province)
533      return {'pois': d['pois'], 'hotels': d['hotels']}
บรรทัด 485: BUILD สตริงรุ่นของโค้ด เปลี่ยนทุกครั้งที่แก้อัลกอริทึม เพื่อเช็กว่าเซิร์ฟเวอร์รันโค้ดล่าสุด
บรรทัด 488–494: GET /api/health คืนสถานะ รุ่น จำนวน POI โรงแรม และจังหวัด
บรรทัด 497–501: _max_days จำนวนวันสูงสุดที่ข้อมูลรองรับ: ที่เที่ยวไม่น้อยกว่า 3 จุดต่อวัน และร้านอาหารไม่น้อยกว่า 2 ร้านต่อวัน
บรรทัด 504–511: _neighbors จังหวัดข้างเคียงภายใน 110 กม. (สูงสุด 4) เรียงจากใกล้ ใช้สร้างทริปข้ามจังหวัด คำนวณระยะแบบเส้นตรงเองเพราะ haversine_km คูณตัวคูณถนนของ request ก่อนหน้า
บรรทัด 514–525: GET /api/provinces รายการจังหวัดที่มีข้อมูล พร้อมศูนย์กลางแผนที่ จำนวนจุด/โรงแรม ธง sparse จำนวนวันสูงสุด จังหวัดข้างเคียง และรายชื่อจังหวัดที่ยังไม่พร้อม
บรรทัด 529–533: GET /api/pois คืนจุดและโรงแรมของจังหวัด ผ่าน get_province
บรรทัด 536–567  โหมด Developer
536  # ---------- โหมด Developer: รหัสผ่านตรวจที่ backend (ตั้งค่าได้ด้วยตัวแปรแวดล้อม WET_DEV_PASSWORD) ----------
537  DEV_PASSWORD = os.environ.get('WET_DEV_PASSWORD', '007')
538  DEV_TOKENS = set()          # shortcut: เก็บในหน่วยความจำ — รีสตาร์ทเซิร์ฟเวอร์แล้วต้องใส่รหัสใหม่
539  _UNLOCK_FAILS = {}          # ip -> [เวลาที่ใส่ผิด] จำกัด 5 ครั้ง/นาที กันเดารหัส
540
541
542  class UnlockRequest(BaseModel):
543      password: str
544
545
546  @app.post('/api/dev/unlock')
547  def dev_unlock(body: UnlockRequest, request: Request):
548      ip = request.client.host if request.client else '?'
549      now = time.time()
550      fails = [t for t in _UNLOCK_FAILS.get(ip, []) if now - t < 60]
551      if len(fails) >= 5:
552          raise HTTPException(status_code=429, detail='ลองรหัสผิดหลายครั้ง รอ 1 นาทีแล้วลองใหม่')
553      if not secrets.compare_digest(body.password, DEV_PASSWORD):
554          _UNLOCK_FAILS[ip] = fails + [now]
555          raise HTTPException(status_code=403, detail='รหัสผ่านไม่ถูกต้อง')
556      token = secrets.token_hex(16)
557      DEV_TOKENS.add(token)
558      return {'token': token}
559
560
561  def is_dev(token: Optional[str]) -> bool:
562      return bool(token) and token in DEV_TOKENS
563
564
565  @app.get('/api/dev/check')
566  def dev_check(x_dev_token: Optional[str] = Header(None)):
567      return {'ok': is_dev(x_dev_token)}
บรรทัด 536–539: รหัสผ่านโหมด Developer จากตัวแปรแวดล้อม WET_DEV_PASSWORD เก็บโทเค็นในหน่วยความจำ และบันทึกการใส่รหัสผิดต่อ IP
บรรทัด 542–543: UnlockRequest รับรหัสผ่าน
บรรทัด 546–558: POST /api/dev/unlock จำกัดใส่ผิด 5 ครั้ง/นาที เทียบรหัสด้วย secrets.compare_digest (กัน timing attack) ถ้าถูกสร้างโทเค็นสุ่มเก็บไว้
บรรทัด 561–562: is_dev ตรวจโทเค็น
บรรทัด 565–567: GET /api/dev/check ตรวจว่าโทเค็นยังใช้ได้
บรรทัด 570–647  `POST /api/packages`: เตรียมและตัวช่วยของ tier
570  @app.post('/api/packages', response_model=PackageResponse)
571  def create_packages(req: PackageRequest, x_dev_token: Optional[str] = Header(None)):
572      """สร้าง 3 แพ็กเกจ (Budget / Standard / Premium) ด้วย algorithm ที่เลือก"""
573      # ใช้ seed ที่กำหนดเพื่อ reproduce ผล; None → สุ่มใหม่ทุกครั้ง
574      if (req.algorithm or 'hybrid').lower() != 'hybrid' and not is_dev(x_dev_token):   # เลือกอัลกอริทึมอื่นได้เฉพาะโหมด Developer
575          raise HTTPException(status_code=403, detail='ต้องเข้าโหมด Developer เพื่อเลือกอัลกอริทึมอื่นนอกจาก Hybrid')
576      random.seed(req.seed)
577      data = get_province(req.province)
578      HOTELS = data['hotels']
579      originals = data['poi_by_id']
580      POIS, pref_notes = apply_preferences(data['pois'], req.preferences, req.days)
581
582      # tier: (ชื่อ, สัดส่วนงบโรงแรม, สัดส่วนงบรวม, scoring_mode, score_pct, max_rest_cost)
583      # score_pct: percentile สูงสุดของ score ที่อนุญาตสำหรับ tier นั้น
584      # max_rest_cost: ราคาร้านอาหารสูงสุด (None = ไม่จำกัด)
585      tier_specs = [
586          ('Budget',   0.20, 0.40, 'ratio',   0.50,  150),  # ร้านถูก + attr ระดับกลาง
587          ('Standard', 0.45, 0.75, 'quality', 0.80,  400),  # ร้านกลาง + attr ระดับดี
588          ('Premium',  0.55, 1.00, 'quality', None,  None), # ทุกอย่าง เน้น score สูงสุด
589      ]
590      all_pois = POIS
591      sorted_hotels = sorted(HOTELS, key=lambda h: h['cost'])
592
593      # คำนวณ score threshold จาก non-restaurant POIs
594      _attr_scores = sorted(p.get('_base', p['score']) for p in all_pois if p['category'] != 'restaurant')
595      def _percentile(lst, pct):
596          idx = max(0, int(len(lst) * pct) - 1)
597          return lst[idx]
598
599      def make_tier_pois(score_pct, max_rest_cost=None, hotel=None):
600          """กรอง POI ตาม tier:
601             - attr: กรองตาม score percentile
602             - restaurant: กรองตาม max_rest_cost เพื่อให้ tier ต่างกันชัดเจน
603          """
604          result = []
605          attr_max = _percentile(_attr_scores, score_pct) if score_pct is not None else float('inf')
606          for p in all_pois:
607              if p['category'] == 'restaurant':
608                  if max_rest_cost is None or p['cost'] <= max_rest_cost:
609                      result.append(p)
610              else:
611                  if p.get('_base', p['score']) <= attr_max:
612                      result.append(p)
613          # ร้านที่ผ่านเพดานราคาของ tier น้อยเกินไป (เช่น กรองตามอาหารมังสวิรัติแล้วเหลือแต่ร้านแพง): เติมร้านที่ถูกที่สุดจนครบมื้อ
614          need = 2 * req.days + 2
615          chosen = [p for p in result if p['category'] == 'restaurant']
616          if len(chosen) < need:
617              rest_ids = {p['id'] for p in chosen}
618              extra = sorted((p for p in all_pois if p['category'] == 'restaurant' and p['id'] not in rest_ids),
619                             key=lambda p: (not p.get('_diet'), p['cost']))[:need - len(chosen)]
620              result += extra
621          # เพดานราคาตัดร้านใกล้โรงแรมทิ้งได้ จนต้องวิ่งไปร้านไกลซึ่งค่าเดินทางแพงกว่าส่วนต่างราคาอาหาร: คงร้านที่ใกล้โรงแรมที่สุดไว้เสมอ
622          if hotel is not None:
623              have = {p['id'] for p in result}
624              near = sorted((p for p in all_pois if p['category'] == 'restaurant' and p['id'] not in have),
625                            key=lambda p: haversine_km(hotel['lat'], hotel['lng'], p['lat'], p['lng']))[:need]
626              result += near
627          return result
628
629      _dist_cache = {}
630
631      def _median_dist(h):
632          if h['id'] not in _dist_cache:
633              ds = sorted(haversine_km(h['lat'], h['lng'], p['lat'], p['lng']) for p in all_pois if p['category'] != 'restaurant')
634              rs = sorted(haversine_km(h['lat'], h['lng'], p['lat'], p['lng']) for p in all_pois if p['category'] == 'restaurant')[:8]
635              # ระยะกลางถึงแหล่งเที่ยว + ระยะเฉลี่ยถึงร้านอาหาร 8 ร้านที่ใกล้สุด (ทุกวันต้องกิน 2 มื้อ ร้านอยู่ไกลโรงแรมทำให้ค่าเดินทางกินงบ)
636              _dist_cache[h['id']] = (ds[len(ds) // 2] if ds else 0.0) + (sum(rs) / len(rs) if rs else 0.0)
637          return _dist_cache[h['id']]
638
639      def find_best_hotel(max_per_night, exclude):
640          cands = [h for h in sorted_hotels
641                   if h['cost'] <= max_per_night and h['id'] not in exclude]
642          if not cands:
643              free = [h for h in sorted_hotels if h['id'] not in exclude]
644              return free[0] if free else sorted_hotels[0]   # โรงแรมไม่พอสำหรับ 3 ระดับ (จังหวัดข้อมูลน้อย) → ใช้ซ้ำได้
645          # คะแนนโรงแรมหักตามระยะเฉลี่ยถึงสถานที่ท่องเที่ยว: โรงแรมที่ไกลแหล่งเที่ยวทำให้ค่าเดินทางและเวลาเสียทุกวัน
646          return max(cands, key=lambda h: h['score'] - 0.08 * _median_dist(h))
647
บรรทัด 570–575: ประกาศ endpoint สร้างแพ็กเกจ 3 ระดับ ถ้าเลือกอัลกอริทึมอื่นนอกจาก hybrid ต้องเป็นโหมด Developer
บรรทัด 576–580: ตั้ง seed ดึงข้อมูลจังหวัด (ตั้งโปรไฟล์เวลาเดินทางด้วย get_province) และปรับจุดตามความชอบ
บรรทัด 582–589: tier_specs กำหนดแต่ละระดับ: สัดส่วนงบโรงแรม สัดส่วนงบรวม โหมดคะแนน เพดาน percentile คะแนนที่เที่ยว และเพดานราคาร้านอาหาร (Budget, Standard, Premium)
บรรทัด 590–597: เรียงโรงแรมตามราคา และคำนวณคะแนนที่เที่ยวไว้หา percentile
บรรทัด 599–627: make_tier_pois กรองจุดตามระดับ: ที่เที่ยวตาม percentile ร้านอาหารตามเพดานราคา ถ้าร้านน้อยกว่าจำนวนมื้อที่ต้องใช้ เติมร้านที่ถูกสุด และคงร้านที่ใกล้โรงแรมที่สุดไว้เสมอ
บรรทัด 629–637: _median_dist ระยะกลางจากโรงแรมถึงที่เที่ยว + ระยะเฉลี่ยถึงร้านอาหาร 8 ร้านที่ใกล้สุด (แคชไว้)
บรรทัด 639–646: find_best_hotel เลือกโรงแรมที่ราคาไม่เกินงบต่อคืนและยังไม่ถูกเลือก คะแนนโรงแรมหักตามระยะ (0.08 × ระยะ) ถ้าไม่มีที่เหมาะใช้ซ้ำได้
บรรทัด 648–669  โรงแรมอัตโนมัติ (ไม่รวมโรงแรม)
648      packages = []
649      picked = set()
650      algo = (req.algorithm or 'hybrid').lower()
651
652      nights = max(0, req.days - 1)
653      include_hotel = req.include_hotel if req.include_hotel is not None else True
654      auto_no_hotel = False
655      _min_meals = sum(sorted(p['cost'] for p in all_pois if p['category'] == 'restaurant')[:2 * req.days]) * req.travelers
656      if include_hotel and nights > 0:
657          # ที่พักถูกสุด + ค่าอาหารขั้นต่ำเกินงบ: สร้างแผนแบบไม่รวมโรงแรมให้แทน (ไม่งั้นแผนไม่มีร้านอาหารและเกินงบ)
658          if sorted_hotels[0]['cost'] * nights + _min_meals > req.budget:
659              include_hotel = False
660              auto_no_hotel = True
661
662      for tier, hotel_r, total_r, mode, score_pct, max_rest_cost in tier_specs:
663          if include_hotel:
664              max_per_night = req.budget * hotel_r / max(nights, 1) if nights > 0 else 0
665              hotel = find_best_hotel(max_per_night, picked) if nights > 0 else sorted_hotels[0]
666              if nights > 0 and hotel['cost'] * nights + _min_meals > req.budget >= sorted_hotels[0]['cost'] * nights + _min_meals:
667                  hotel = sorted_hotels[0]   # โรงแรมที่ไม่ซ้ำกันแพงเกินงบ แต่โรงแรมถูกสุดยังพอ: ใช้ซ้ำได้ (ไม่งั้นระดับสูงเกินงบ)
668          else:
669              # ไม่รวมโรงแรม: ใช้โรงแรมที่อยู่ใกล้แหล่งเที่ยวที่สุดเป็นจุดเริ่ม/จบของ routing เท่านั้น (ไม่คิดค่าห้อง)
บรรทัด 648–651: ตัวแปรเริ่มต้น: รายการแพ็กเกจ โรงแรมที่เลือกแล้ว และอัลกอริทึม
บรรทัด 652–655: จำนวนคืน ธงรวมโรงแรม ธงสลับเป็นไม่รวมโรงแรมอัตโนมัติ และค่าอาหารขั้นต่ำของทริป
บรรทัด 656–660: ถ้าที่พักถูกสุดรวมค่าอาหารขั้นต่ำเกินงบ สร้างแผนแบบไม่รวมโรงแรมให้แทน (ไม่งั้นแผนไม่มีร้านอาหารและเกินงบ)
บรรทัด 662–667: วนทีละระดับ ถ้ารวมโรงแรม เลือกโรงแรมตามงบต่อคืน และใช้โรงแรมถูกสุดซ้ำได้ถ้าโรงแรมที่ไม่ซ้ำแพงเกินแต่ถูกสุดยังพอ
บรรทัด 668–669: ถ้าไม่รวมโรงแรม ใช้โรงแรมที่ใกล้แหล่งเที่ยวที่สุดเป็นจุดเริ่ม/จบการจัดเส้นทางเท่านั้น (ไม่คิดค่าห้อง)
บรรทัด 670–724  เลือกโรงแรมและคำนวณงบกิจกรรมของแต่ละระดับ
670              # เดิมเลือกโรงแรมถูกสุด ซึ่งอาจอยู่ไกลจนค่าเดินทางกินงบ แผนเหลือแต่ร้านอาหาร
671              avail = [h for h in sorted_hotels if h['id'] not in picked]
672              hotel = min(avail or sorted_hotels, key=_median_dist)
673
674          if hotel is None:
675              packages.append(Package(
676                  tier=tier, hotel=sorted_hotels[0],
677                  days=[DayDetail(day=i+1, pois=[], distance_km=0, time_min=0,
678                                  cost=0, score=0) for i in range(req.days)],
679                  total_score=0, total_activity_cost=0, total_hotel_cost=0,
680                  total_cost=0, runtime_ms=0, valid=False,
681                  violations=[f'No hotel for {tier}']
682              ))
683              continue
684          picked.add(hotel['id'])
685
686          # คำนวณค่าโรงแรม (0 ถ้าไม่รวมโรงแรม หรือทริปวันเดียว)
687          hotel_total = hotel['cost'] * nights if include_hotel else 0
688
689          # งบสำหรับกิจกรรม
690          # ไม่รวมโรงแรม: งบทั้งหมดเป็นของกิจกรรม จึงไม่ลดงบ Budget เหลือ 40% (เดิมงบน้อยจนเหลือแต่ร้านอาหาร)
691          if not include_hotel:
692              total_r = {'Budget': 0.60, 'Standard': 0.85}.get(tier, 1.0)
693          target_total = req.budget * total_r
694          if include_hotel and nights > 0 and hotel_total > req.budget * hotel_r:
695              # โรงแรมถูกสุดของจังหวัดแพงกว่าสัดส่วนที่ระดับนี้จัดไว้ งบกิจกรรมจึงเหลือน้อยจนแผนมีแต่ร้านอาหาร:
696              # รับประกันงบกิจกรรมอย่างน้อย 40% ของเงินที่เหลือหลังหักค่าโรงแรม
697              target_total = hotel_total + max(target_total - hotel_total, 0.4 * max(0.0, req.budget - hotel_total))
698          budget_for_act = max(0, target_total - hotel_total) / req.travelers
699          # งบต่อคนต้องพอค่าอาหารขั้นต่ำของทริป (ร้านถูกที่สุด 2 มื้อ/วัน x 1.25) ไม่งั้นระดับ Budget ของทริปหลายคนงบไม่พอแม้แต่มื้ออาหาร
700          # อัลกอริทึมจึงทิ้งสถานที่ฟรีเกือบทั้งหมด (ผู้ใช้เห็นแผนมีแต่ร้านอาหาร) — จำกัดไม่เกินเงินที่ผู้ใช้มีจริง
701          _meal_min = sum(sorted(p['cost'] for p in all_pois if p['category'] == 'restaurant')[:2 * req.days])
702          _avail = max(0.0, req.budget - hotel_total) / req.travelers
703          budget_for_act = min(max(budget_for_act, 1.25 * _meal_min), _avail)
704          target_total = max(target_total, hotel_total + budget_for_act * req.travelers)
705
706          # Dynamic restaurant cap สำหรับ quality mode:
707          # ป้องกันร้านอาหารแพงกินงบหมดในทริปงบต่ำ
708          # Budget tier ใช้ ratio scoring ซึ่ง penalize ร้านแพงอยู่แล้ว → ไม่ต้องแตะ
709          if mode == 'quality':
710              # จัดสรรสูงสุด 1/5 ของงบต่อวันต่อมื้อ
711              # floor=150 ensures >= 21 restaurants in pool (7 days x 2 meals = 14 slots needed)
712              dyn_rest_cap = max(150.0, budget_for_act / (max(req.days, 1) * 5.0))
713              if max_rest_cost is not None:
714                  effective_rest_cap = min(max_rest_cost, dyn_rest_cap)
715              else:
716                  # Premium: ใช้ dynamic cap เฉพาะเมื่องบต่ำ; งบสูง (dyn≥500) ไม่จำกัด
717                  effective_rest_cap = dyn_rest_cap if dyn_rest_cap < 500 else None
718          else:
719              # Budget (ratio mode): ใช้ tier cap เดิม
720              effective_rest_cap = max_rest_cost
721
722          # กรอง POI pool ตาม tier (ทำให้แต่ละ tier ต่างกัน)
723          tier_pois = make_tier_pois(score_pct, effective_rest_cap, hotel)
724
บรรทัด 670–672: กรณีไม่รวมโรงแรม เลือกโรงแรมที่ใกล้แหล่งเที่ยวที่สุดจากที่ยังไม่ถูกเลือก (เดิมเลือกโรงแรมถูกสุด ซึ่งอาจไกลจนค่าเดินทางกินงบ แผนเหลือแต่ร้านอาหาร)
บรรทัด 674–683: ถ้าไม่มีโรงแรมเลย สร้างแพ็กเกจว่างที่ไม่ valid แล้วข้ามระดับนี้
บรรทัด 684: จดว่าโรงแรมนี้ถูกเลือกแล้ว
บรรทัด 687: ค่าโรงแรมรวม (0 ถ้าไม่รวมโรงแรม)
บรรทัด 691–693: ถ้าไม่รวมโรงแรม ใช้สัดส่วนงบกิจกรรม 60% (Budget) 85% (Standard) แล้วคำนวณงบเป้าหมาย target_total
บรรทัด 694–697: ถ้าโรงแรมแพงเกินสัดส่วนที่ระดับนั้นจัดไว้ รับประกันงบกิจกรรมอย่างน้อย 40% ของเงินที่เหลือ
บรรทัด 698: งบกิจกรรมต่อคน
บรรทัด 699–704: ปรับงบต่อคนให้พอค่าอาหารขั้นต่ำ (ร้านถูกสุด 2 มื้อต่อวัน × 1.25) แต่ไม่เกินเงินที่ผู้ใช้มีจริง กันแผนที่เหลือแต่ร้านอาหารเมื่อทริปหลายคนงบน้อย
บรรทัด 706–720: เพดานราคาร้านอาหารแบบพลวัตสำหรับโหมด quality (ไม่เกิน 1/5 ของงบต่อวัน ขั้นต่ำ 150) ระดับ Budget ใช้เพดานเดิมเพราะโหมด ratio หักราคาแพงอยู่แล้ว
บรรทัด 723: กรองจุดตามระดับด้วย make_tier_pois
บรรทัด 725–745  เรียกอัลกอริทึมและจัดลำดับความสำคัญ
725          t0 = time.time()
726          if algo == 'greedy':
727              routes = greedy_solve(tier_pois, hotel, req.days, budget_for_act,
728                                    scoring_mode=mode, random_factor=0.15)
729          elif algo == 'ga':
730              routes, _hist = genetic_solve(tier_pois, hotel, req.days, budget_for_act,
731                                            pop_size=30, generations=40,
732                                            mutation_rate=0.3, verbose=False)
733          else:  # hybrid
734              routes, _hist = hybrid_solve(tier_pois, hotel, req.days, budget_for_act,
735                                           scoring_mode=mode, pop_size=20,
736                                           generations=40, mutation_rate=0.3,
737                                           verbose=False, diversity_weight=DIVERSITY_WEIGHT,
738                                           rl_theta=RL_THETA if algo == 'hybrid_rl' else None,
739                                           ils=True)  # ILS: ดีขึ้นอย่างมีนัยสำคัญ 24/24 (experiments/results/ils_stats.txt)
740          runtime_ms = (time.time() - t0) * 1000.0
741          if algo != 'hybrid_rl':
742              routes = _prioritize_sights(routes, hotel, sorted((p for p in tier_pois if p['category'] != 'restaurant'), key=lambda p: -p['score'])
743                                          + sorted((p for p in all_pois if p['category'] != 'restaurant' and p not in tier_pois), key=lambda p: -p['score']),
744                                          sorted((p for p in all_pois if p['category'] == 'restaurant'), key=lambda p: p['cost']), budget_for_act)
745          routes = restore_originals(routes, originals)   # คะแนนที่รายงานต้องเป็นคะแนนจริง ไม่รวมตัวถ่วงความชอบ
บรรทัด 725–740: จับเวลาแล้วเรียกอัลกอริทึมตามที่เลือก: greedy เรียก ➜ greedy_solve() ใน algorithm/greedy.py; ga เรียก ➜ genetic_solve() ใน algorithm/genetic.py; ที่เหลือ (hybrid) เรียก ➜ hybrid_solve() ใน algorithm/hybrid.py ด้วยประชากร 20 รุ่น 40 น้ำหนักความหลากหลาย ILS เปิด และ RL seed เมื่อเลือก hybrid_rl
บรรทัด 741–744: ถ้าไม่ใช่ hybrid_rl ใช้ _prioritize_sights จัดลำดับความสำคัญเมื่องบไม่พอ (ที่เที่ยวครบก่อนมื้อ)
บรรทัด 745: คืนวัตถุต้นฉบับเพื่อให้คะแนนที่รายงานเป็นคะแนนจริง
บรรทัด 746–785  สร้างแพ็กเกจและลองใหม่เมื่อผิดข้อจำกัด
746          # ใช้ target_total เป็น cap แต่ละ tier เพื่อให้งบแตกต่างกันชัดเจน
747          pkg = build_package(tier, hotel, routes, req.days,
748                              req.budget, runtime_ms, req.travelers, POIS,
749                              max_total_budget=target_total,
750                              hotel_cost_override=hotel_total)
751          cap_total = max(0.0, req.budget - hotel_total)
752          if algo == 'hybrid':
753              # ไม่ยอมแสดงแผนที่ผิดข้อจำกัด (เช่น ถึงร้านสายเกินช่วงมื้อ) หรือเกินงบ: ลองสร้างใหม่ด้วยตัวเลือกทั้งหมด (ร้านทุกราคา) และสุ่มใหม่ สูงสุด 3 ครั้ง
754              # เลือกแผนที่ผ่านข้อจำกัดและคะแนนสูงสุด ถ้ายังไม่ผ่านใช้แผนที่ผิดน้อยที่สุด
755              def _bad(pk):
756                  return (0 if pk.valid else 1, 1 if pk.total_activity_cost > cap_total * 1.05 + 1 else 0)
757              for attempt in range(3):
758                  if _bad(pkg) == (0, 0):
759                      break
760                  t0 = time.time()
761                  random.seed(None if req.seed is None else req.seed + attempt + 1)
762                  r2, _h = hybrid_solve(make_tier_pois(None, None, hotel), hotel, req.days, cap_total / req.travelers,
763                                        scoring_mode='quality', pop_size=20, generations=40, mutation_rate=0.3,
764                                        verbose=False, diversity_weight=DIVERSITY_WEIGHT, ils=True)
765                  r2 = _prioritize_sights(r2, hotel, sorted((p for p in all_pois if p['category'] != 'restaurant'), key=lambda p: -p['score']),
766                                          sorted((p for p in all_pois if p['category'] == 'restaurant'), key=lambda p: p['cost']), cap_total / req.travelers)
767                  r2 = restore_originals(r2, originals)
768                  pkg2 = build_package(tier, hotel, r2, req.days, req.budget, runtime_ms + (time.time() - t0) * 1000.0,
769                                       req.travelers, POIS, max_total_budget=req.budget, hotel_cost_override=hotel_total)
770                  if (_bad(pkg2), -pkg2.total_score) < (_bad(pkg), -pkg.total_score):
771                      pkg = pkg2
772          pkg.notes = list(pref_notes)
773          if auto_no_hotel:
774              pkg.notes.append(f'งบ {req.budget:,.0f} บาท ไม่พอทั้งค่าที่พักและค่าอาหาร ระบบจึงสร้างแผนแบบไม่รวมค่าโรงแรมให้ (ที่พักถูกสุดของจังหวัดนี้ {sorted_hotels[0]["cost"]:,.0f} บาทต่อคืน) หากต้องการรวมที่พัก ลองเพิ่มงบหรือลดจำนวนวัน')
775          if _avail < 1.1 * _meal_min and hotel_total <= req.budget:
776              pkg.notes.append(f'งบต่อคน {_avail:,.0f} บาท แทบไม่พอค่าอาหารขั้นต่ำของ {req.days} วัน (ราว {_meal_min:,.0f} บาท) แผนจึงมีสถานที่ท่องเที่ยวน้อย ลองเพิ่มงบหรือลดจำนวนวัน')
777          if hotel_total > req.budget:   # ที่พักถูกสุดของจังหวัดแพงกว่างบทั้งหมด: ไม่มีเงินเหลือค่าอาหาร/ค่าเข้าชม
778              pkg.notes.append(f'งบ {req.budget:,.0f} บาท ไม่พอแม้แต่ค่าที่พัก {hotel_total:,.0f} บาท ({nights} คืน) แผนจึงไม่มีร้านอาหารและเกินงบ ลองเพิ่มงบ ลดจำนวนวัน หรือเลือก "ไม่รวมค่าโรงแรม"')
779          elif pkg.total_cost > req.budget * 1.05 + 1:
780              pkg.notes.append(f'งบ {req.budget:,.0f} บาท ไม่พอสำหรับ {req.days} วันในจังหวัดนี้ แผน{tier}มีค่าใช้จ่ายประมาณ {pkg.total_cost:,.0f} บาท ลองเพิ่มงบหรือลดจำนวนวัน')
781          empty = sum(1 for d in pkg.days if not d.pois)
782          if empty:   # จังหวัดข้อมูลน้อย: สถานที่ไม่พอเติมทุกวัน
783              pkg.notes.append(f'จังหวัดนี้มีข้อมูลสถานที่น้อย แผน{tier}มี {empty} วันที่ไม่มีกิจกรรม ลองลดจำนวนวันหรือเลือกจังหวัดอื่น')
784          packages.append(pkg)
785      return PackageResponse(request=req.dict(), packages=packages)
บรรทัด 746–750: สร้างแพ็กเกจด้วย build_package โดยใช้ target_total เป็นเพดานของระดับ
บรรทัด 751: งบกิจกรรมสูงสุดที่ผู้ใช้มีจริง cap_total
บรรทัด 752–756: ถ้าเป็น hybrid ฟังก์ชัน _bad ให้คะแนนความไม่ดี: (ไม่ valid, เกินงบเกิน 5%)
บรรทัด 757–771: ลองสร้างใหม่ไม่เกิน 3 ครั้งด้วยตัวเลือกทั้งหมดและ seed ใหม่ ถ้าแผนใหม่ดีกว่า (ผ่านข้อจำกัดและคะแนนสูงกว่า) จึงใช้แทน
บรรทัด 772–783: เพิ่มหมายเหตุถึงผู้ใช้: ข้อความจากความชอบ งบไม่พอทั้งที่พักและอาหาร (สร้างแผนไม่รวมโรงแรมให้) งบต่อคนแทบไม่พอค่าอาหาร ที่พักแพงกว่างบ แผนเกินงบ และวันที่ไม่มีกิจกรรมเพราะข้อมูลน้อย
บรรทัด 784–785: เพิ่มแพ็กเกจและคืน PackageResponse (ทั้ง 3 ระดับ)
บรรทัด 788–816  เซสชันร่วมกัน (Collaborative planning)
788  # ============================================================
789  # Collaborative planning: เซสชันที่แชร์ลิงก์ให้เพื่อนร่วมดู/แก้แผนเดียวกัน
790  # เก็บในหน่วยความจำและบันทึกลงไฟล์ data/sessions.json (กลับมาหลัง restart) — ใช้ version ทำ optimistic concurrency, ฝั่ง client โพลลิ่งทุก 2 วินาที
791  # ============================================================
792  SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sessions.json')
793
794
795  def _session_load():
796      try:
797          with open(SESSION_FILE, encoding='utf-8') as f:
798              return json.load(f)
799      except (OSError, ValueError):
800          return {}
801
802
803  def _session_save():   # เรียกขณะถือ SESSION_LOCK; เขียนไฟล์ชั่วคราวแล้ว replace กันไฟล์พังกลางคัน
804      try:
805          tmp = SESSION_FILE + '.tmp'
806          with open(tmp, 'w', encoding='utf-8') as f:
807              json.dump(SESSIONS, f, ensure_ascii=False)
808          os.replace(tmp, SESSION_FILE)
809      except OSError:
810          pass   # shortcut: บันทึกไม่ได้ก็ยังทำงานในหน่วยความจำต่อ
811
812
813  SESSIONS = _session_load()
814  SESSION_LOCK = threading.Lock()
815  SESSION_TTL_S = 24 * 3600
816  SESSION_MAX = 300
บรรทัด 788–791: คอมเมนต์: เซสชันที่แชร์ลิงก์ให้เพื่อนร่วมดู/แก้แผนเดียวกัน เก็บในหน่วยความจำและบันทึกลง data/sessions.json ใช้ version ทำ optimistic concurrency ฝั่ง client โพลลิ่งทุก 2 วินาที (ดู ➜ frontend/extras.js)
บรรทัด 792: SESSION_FILE พาธไฟล์เซสชัน
บรรทัด 795–800: _session_load โหลดเซสชันจากไฟล์ ถ้าอ่านไม่ได้เริ่มจากว่าง
บรรทัด 803–810: _session_save เขียนไฟล์ชั่วคราวแล้ว os.replace กันไฟล์พังกลางคัน ถ้าบันทึกไม่ได้ยังทำงานในหน่วยความจำต่อ
บรรทัด 813–816: ตัวแปรเซสชัน: SESSIONS ตัวล็อกเธรด อายุ 24 ชั่วโมง และจำนวนสูงสุด 300
บรรทัด 819–878  โมเดลและ endpoint ของเซสชัน
819  class SessionCreate(BaseModel):
820      province: str = DEFAULT_PROVINCE
821      package: dict
822      settings: dict = {}          # budget, travelers, include_hotel, start_date, preferences, locked, excluded
823
824
825  class SessionUpdate(BaseModel):
826      base_version: int
827      package: dict
828      settings: dict = {}
829
830
831  def _session_gc():
832      now = time.time()
833      for k in [k for k, v in SESSIONS.items() if now - v['updated'] > SESSION_TTL_S]:
834          del SESSIONS[k]
835
836
837  def _session_view(sid):
838      v = SESSIONS[sid]
839      return {'id': sid, 'version': v['version'], 'province': v['province'], 'package': v['package'], 'settings': v['settings']}
840
841
842  @app.post('/api/sessions')
843  def create_session(req: SessionCreate):
844      get_province(req.province)
845      if not isinstance(req.package.get('days'), list) or len(req.package['days']) > 7:
846          raise HTTPException(status_code=422, detail='invalid package')
847      with SESSION_LOCK:
848          _session_gc()
849          if len(SESSIONS) >= SESSION_MAX:
850              raise HTTPException(status_code=503, detail='too many sessions')
851          sid = secrets.token_urlsafe(6)
852          SESSIONS[sid] = {'version': 1, 'province': req.province, 'package': req.package,
853                           'settings': req.settings, 'updated': time.time()}
854          _session_save()
855          return _session_view(sid)
856
857
858  @app.get('/api/sessions/{sid}')
859  def get_session(sid: str, since: int = 0):
860      with SESSION_LOCK:
861          if sid not in SESSIONS:
862              raise HTTPException(status_code=404, detail='session not found or expired')
863          if since and SESSIONS[sid]['version'] == since:
864              return {'id': sid, 'version': since, 'changed': False}
865          return {**_session_view(sid), 'changed': True}
866
867
868  @app.put('/api/sessions/{sid}')
869  def update_session(sid: str, req: SessionUpdate):
870      with SESSION_LOCK:
871          if sid not in SESSIONS:
872              raise HTTPException(status_code=404, detail='session not found or expired')
873          cur = SESSIONS[sid]
874          if req.base_version != cur['version']:      # มีคนอื่นแก้ไปก่อน → ส่งสถานะล่าสุดกลับให้ client รวมเข้ากับของตัวเอง
875              raise HTTPException(status_code=409, detail=_session_view(sid))
876          cur.update(version=cur['version'] + 1, package=req.package, settings=req.settings or cur['settings'], updated=time.time())
877          _session_save()
878          return _session_view(sid)
บรรทัด 819–822: SessionCreate จังหวัด แพ็กเกจ และตั้งค่า (งบ จำนวนคน ไม่รวมโรงแรม วันเริ่ม ความชอบ จุดล็อก/ลบ)
บรรทัด 825–828: SessionUpdate เวอร์ชันฐาน แพ็กเกจใหม่ และตั้งค่า
บรรทัด 831–834: _session_gc ลบเซสชันที่เกินอายุ
บรรทัด 837–839: _session_view สร้างข้อมูลที่ส่งกลับ
บรรทัด 842–855: POST /api/sessions ตรวจแพ็กเกจ (รายการวัน ไม่เกิน 7) ล้างเซสชันเก่า จำกัดจำนวน สร้างรหัสสั้นแบบสุ่ม เวอร์ชัน 1 และบันทึกไฟล์
บรรทัด 858–865: GET /api/sessions/{sid} คืนเซสชัน ถ้าเวอร์ชันเท่ากับที่ client ถือ (since) คืน changed: False ลดข้อมูลที่ส่ง
บรรทัด 868–878: PUT /api/sessions/{sid} ถ้าเวอร์ชันฐานไม่ตรง (มีคนแก้ก่อน) ตอบ 409 พร้อมสถานะล่าสุดให้ client รวมเข้ากับของตัวเอง ถ้าตรง เพิ่มเวอร์ชันและบันทึก
บรรทัด 881–923  `POST /api/pareto` ทางเลือกหลายเป้าหมาย
881  @app.post('/api/pareto', response_model=PackageResponse)
882  def pareto(req: PackageRequest):
883      """หา Pareto front (NSGA-II) ระหว่าง คะแนน / ความหลากหลายของหมวด / ระยะทางรวม คืนแผนตัวแทนไม่เกิน 8 แผน
884      ใช้การตั้งค่าระดับ Standard (โรงแรม <=45% ใช้รวม <=75% ของงบ) ให้ผู้ใช้เลือก trade-off เอง"""
885      random.seed(req.seed)
886      data = get_province(req.province)
887      pool, pref_notes = apply_preferences(data['pois'], req.preferences, req.days)
888      nights = max(0, req.days - 1)
889      include_hotel = req.include_hotel if req.include_hotel is not None else True
890      hotels = sorted(data['hotels'], key=lambda h: h['cost'])
891      max_per_night = req.budget * 0.45 / max(nights, 1) if nights > 0 else 0
892      cands = [h for h in hotels if h['cost'] <= max_per_night] or hotels[:1]
893      hotel = max(cands, key=lambda h: h['score']) if include_hotel and nights > 0 else hotels[0]
894      hotel_total = hotel['cost'] * nights if include_hotel else 0
895      target_total = req.budget * 0.75
896      budget_for_act = max(0, target_total - hotel_total) / req.travelers
897      # เพดานราคาร้านอาหารเหมือนระดับ Standard (ไม่ให้ร้านแพงกินงบทั้งทริป) และเติมร้านถูกสุดถ้าไม่พอมื้อ
898      cap = min(400.0, max(150.0, budget_for_act / (max(req.days, 1) * 5.0)))
899      rests = [p for p in pool if p['category'] == 'restaurant']
900      ok_rests = [p for p in rests if p['cost'] <= cap]
901      need = 2 * req.days + 2
902      if len(ok_rests) < need:
903          ids = {p['id'] for p in ok_rests}
904          ok_rests += sorted((p for p in rests if p['id'] not in ids), key=lambda p: (not p.get('_diet'), p['cost']))[:need - len(ok_rests)]
905      keep_ids = {p['id'] for p in ok_rests}
906      pool = [p for p in pool if p['category'] != 'restaurant' or p['id'] in keep_ids]
907      t0 = time.time()
908      front = nsga2_solve(pool, hotel, req.days, budget_for_act, scoring_mode='quality', pop_size=40, generations=40)
909      runtime_ms = (time.time() - t0) * 1000.0
910      if len(front) > 8:   # เลือกตัวแทน 8 แผนกระจายตามระยะทาง (รวมสองปลาย)
911          by_dist = sorted(front, key=lambda s: s['distance_km'])
912          idx = sorted({round(i * (len(by_dist) - 1) / 7) for i in range(8)})
913          front = [by_dist[i] for i in idx]
914      packages = []
915      for i, sol in enumerate(sorted(front, key=lambda s: s['distance_km']), 1):
916          routes = restore_originals(sol['routes'], data['poi_by_id'])
917          pkg = build_package(f'Pareto {i}', hotel, routes, req.days, req.budget, runtime_ms / max(len(front), 1),
918                              req.travelers, pool, max_total_budget=target_total, hotel_cost_override=hotel_total)
919          pkg.objectives = {'score': round(sol['score'], 1), 'diversity': round(sol['diversity'], 2),
920                            'distance_km': round(sol['distance_km'], 1), 'cost': round(sol['cost'])}
921          pkg.notes = list(pref_notes)
922          packages.append(pkg)
923      return PackageResponse(request=req.dict(), packages=packages)
บรรทัด 881–884: ประกาศ endpoint คืนแผนตัวแทนไม่เกิน 8 แผนจาก Pareto front ด้วยการตั้งค่าระดับ Standard
บรรทัด 885–887: ตั้ง seed ดึงข้อมูลจังหวัด และปรับจุดตามความชอบ
บรรทัด 888–896: คำนวณจำนวนคืน เลือกโรงแรม (คะแนนสูงสุดภายใต้งบต่อคืน 45%) ค่าโรงแรม งบเป้าหมาย 75% และงบกิจกรรมต่อคน
บรรทัด 897–906: จำกัดราคาร้านอาหารเหมือนระดับ Standard และเติมร้านถูกสุดถ้าไม่พอมื้อ
บรรทัด 907–909: เรียก ➜ nsga2_solve() ใน algorithm/pareto.py (ประชากร 40 รุ่น 40)
บรรทัด 910–913: ถ้ามีเกิน 8 แผน เลือกตัวแทน 8 แผนกระจายตามระยะทาง (รวมสองปลาย)
บรรทัด 914–923: สร้างแพ็กเกจของแต่ละแผนเรียงตามระยะทาง ใส่วัตถุประสงค์ (คะแนน ความหลากหลาย ระยะ ค่าใช้จ่าย) และคืนผล
บรรทัด 926–942  `POST /api/recompute`
926  @app.post('/api/recompute', response_model=Package)
927  def recompute(req: RecomputeRequest):
928      data = get_province(req.province)
929      HOTEL_BY_ID, POI_BY_ID = data['hotel_by_id'], data['poi_by_id']
930      if req.hotel_id not in HOTEL_BY_ID:
931          raise HTTPException(status_code=404, detail=f'Hotel {req.hotel_id} not found')
932      hotel = HOTEL_BY_ID[req.hotel_id]
933      routes_per_day = []
934      for day in req.routes:
935          day_pois = []
936          for pid in day:
937              if pid not in POI_BY_ID:
938                  raise HTTPException(status_code=404, detail=f'POI {pid} not found')
939              day_pois.append(POI_BY_ID[pid])
940          routes_per_day.append(day_pois)
941      return build_package('Custom', hotel, routes_per_day, req.days,
942                           req.budget, 0, req.travelers, data['pois'])
บรรทัด 926–932: คำนวณแพ็กเกจใหม่หลังผู้ใช้ลากเรียง/สลับ ดึงข้อมูลจังหวัด ตรวจโรงแรมมีจริง (ไม่พบตอบ 404)
บรรทัด 933–940: แปลงรายการ id รายวันเป็นวัตถุจุด ถ้าไม่พบ id ตอบ 404
บรรทัด 941–942: สร้างแพ็กเกจ Custom จากแผนที่ผู้ใช้จัด (ไม่เรียกอัลกอริทึม เป็นการคำนวณเบา จึงไม่ถูกจำกัดอัตราคำขอ)
บรรทัด 946–977  `POST /api/reoptimize`
946  @app.post('/api/reoptimize', response_model=Package)
947  def reoptimize(req: ReoptimizeRequest):
948      """ปรับแผนใหม่ด้วย Hybrid หลังผู้ใช้ swap/เพิ่ม/ลบ POI โดยคงจุดที่ผู้ใช้เลือก (locked) และไม่ใส่จุดที่ลบ (excluded)"""
949      random.seed(req.seed)
950      data = get_province(req.province)
951      if req.hotel_id not in data['hotel_by_id']:
952          raise HTTPException(status_code=404, detail=f'Hotel {req.hotel_id} not found')
953      hotel = data['hotel_by_id'][req.hotel_id]
954      poi_by_id = data['poi_by_id']
955      for pid in [i for day in req.routes for i in day] + req.locked + req.excluded:
956          if pid not in poi_by_id:
957              raise HTTPException(status_code=404, detail=f'POI {pid} not found')
958      routes = [[poi_by_id[i] for i in day if i not in req.excluded] for day in req.routes]
959      nights = max(0, req.days - 1)
960      hotel_total = hotel['cost'] * nights if req.include_hotel else 0
961      budget_for_act = max(0, req.budget - hotel_total) / req.travelers
962      # POI ที่ผู้ใช้เลือกแต่ใส่ในแผนใดไม่ได้ (เช่น เปิดดึกเกินเวลาต่อวัน/เกินงบ) → นำออกและแจ้งผู้ใช้
963      bad = set(infeasible_locks(data['pois'], hotel, req.locked, budget_for_act))
964      routes = [[p for p in day if p['id'] not in bad] for day in routes]
965      pool, _ = apply_preferences(data['pois'], req.preferences, req.days)
966      t0 = time.time()
967      new_routes = reoptimize_solve(pool, hotel, routes, budget_for_act,
968                                    locked_ids=[i for i in req.locked if i not in bad], excluded_ids=req.excluded,
969                                    diversity_weight=DIVERSITY_WEIGHT)
970      new_routes = restore_originals(new_routes, poi_by_id)
971      runtime_ms = (time.time() - t0) * 1000.0
972      pkg = build_package(req.tier, hotel, new_routes, req.days, req.budget, runtime_ms,
973                           req.travelers, data['pois'], max_total_budget=req.budget,
974                           hotel_cost_override=hotel_total)
975      in_plan = {p['id'] for day in new_routes for p in day}
976      pkg.notes = [f"ใส่ {poi_by_id[i]['name_th']} ในแผนไม่ได้ (เวลาเปิด-ปิด งบ หรือเวลาต่อวันไม่พอ)" for i in req.locked if i not in in_plan]
977      return pkg
บรรทัด 946–948: ประกาศ endpoint ปรับแผนใหม่ด้วย Hybrid หลังผู้ใช้สลับ/เพิ่ม/ลบ โดยคงจุดล็อกและไม่ใส่จุดที่ลบ
บรรทัด 949–957: ตั้ง seed ดึงข้อมูลจังหวัด ตรวจโรงแรมและ id ทุกตัว
บรรทัด 958: แปลง id เป็นจุดและตัดจุดที่ลบ
บรรทัด 959–961: ค่าโรงแรมและงบกิจกรรมต่อคน
บรรทัด 962–964: หาจุดล็อกที่ใส่ไม่ได้ด้วย ➜ infeasible_locks() ใน algorithm/hybrid.py แล้วถอดออกจากแผน (แจ้งผู้ใช้ภายหลัง)
บรรทัด 965: ปรับจุดตามความชอบ
บรรทัด 966–971: เรียก ➜ reoptimize_solve() ใน algorithm/hybrid.py แล้วคืนวัตถุต้นฉบับและจับเวลา
บรรทัด 972–974: สร้างแพ็กเกจ
บรรทัด 975–977: เพิ่มหมายเหตุสำหรับจุดล็อกที่ใส่ในแผนไม่ได้
บรรทัด 980–991  เสิร์ฟหน้าเว็บและรันเซิร์ฟเวอร์
980  # เสิร์ฟหน้าเว็บจากบริการเดียวกัน (ตอน deploy) — ต้อง mount หลังประกาศ API ทั้งหมด
981  _FRONT = os.path.join(os.path.dirname(THIS_DIR), 'frontend')
982  if os.path.isdir(_FRONT):
983      app.mount('/', StaticFiles(directory=_FRONT, html=True), name='frontend')
984
985
986  if __name__ == '__main__':
987      import uvicorn
988      print('Starting WeEasyTrip API...')
989      for _s, _d in DATA.items():
990          print(f"Loaded {_s}: {len(_d['pois'])} POIs, {len(_d['hotels'])} hotels")
991      uvicorn.run(app, host='0.0.0.0', port=8000)
บรรทัด 980–983: ถ้ามีโฟลเดอร์ frontend ให้ mount เป็นเว็บไฟล์ static ที่ราก / (ต้อง mount หลังประกาศ API ทั้งหมด ไม่งั้นจะบังเส้นทาง API) ดูหน้าเว็บที่ ➜ frontend/index.html
บรรทัด 986–991: เมื่อรันไฟล์ตรง ๆ พิมพ์จำนวนจุด/โรงแรมที่โหลดของแต่ละจังหวัด และเปิด uvicorn ที่พอร์ต 8000

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
algorithm/pareto.py
algorithm/rl.py
algorithm/utils.py
data/thai_provinces.py
frontend/app.js
frontend/extras.js
frontend/index.html