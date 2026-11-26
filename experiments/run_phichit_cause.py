# -*- coding: utf-8 -*-
"""
run_phichit_cause.py — ทดสอบสมมติฐานว่าทำไม Hybrid ได้คะแนนต่ำกว่า GA/Greedy ในจังหวัดที่ร้านอาหารไม่พอ (พิจิตร S2)
สมมติฐาน: ขั้น 6 ของ hybrid_solve ถอดสถานที่ท่องเที่ยวคะแนนต่ำสุดวันละ 1 จุด (สูงสุด 3 รอบ) เมื่อวันนั้นมีมื้อไม่ครบ
          แม้สาเหตุคือ "ไม่มีร้านอาหารให้เติม" (ไม่ใช่เวลาไม่พอ) จึงเสียสถานที่ท่องเที่ยวโดยไม่ได้มื้อเพิ่ม
วิธี: (A) Hybrid ปัจจุบัน  (B) Hybrid ที่แก้ให้ไม่ถอดสถานที่เมื่อจำนวนร้านอาหารทั้งหมดน้อยกว่า 2 x จำนวนวัน
      เทียบคะแนนดิบ จำนวนสถานที่ท่องเที่ยว/วัน มื้อ/วัน ระยะขับ และค่าเป้าหมาย (คะแนน - 0.3 x กม. - 0.01 x นาที)
      ใน 4 จังหวัดข้อมูลน้อย (พิจิตร ชัยภูมิ กาฬสินธุ์ สิงห์บุรี) สถานการณ์ S2 รอบละ 10 รอบ
ผลลัพธ์: results/phichit_cause.json
"""
import sys, os, json, random, statistics
sys.argv = [sys.argv[0], '10']
import run_province_experiments as E
import hybrid
from utils import evaluate_route

SC = E.SCENARIOS[1]
src = open(hybrid.__file__, encoding='utf-8-sig').read()
OLD = "            if day and sum(1 for p in day if p['category'] == 'restaurant') < 2:\n                cands"
NEW = "            if day and sum(1 for p in day if p['category'] == 'restaurant') < 2 and sum(1 for p in pois if p['category'] == 'restaurant') >= 2 * days:\n                cands"
assert OLD in src
ns = dict(hybrid.__dict__)
exec(compile(src.replace(OLD, NEW), 'hybrid_patched', 'exec'), ns)
hybrid_fixed = ns['hybrid_solve']


def load(prov):
    from utils import load_data, set_travel_profile
    cfg = E.PROV_CFG[prov]
    set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
    pois, hotels = load_data(os.path.join(E.ROOT, 'data', 'provinces', f'{prov}.json'))
    hs = sorted(hotels, key=lambda h: h['cost'])
    hotel = hs[int(len(hs) * SC['hotel_frac'])]
    return pois, hotel, max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))


def run(fn, pois, hotel, act, seed):
    random.seed(seed)
    routes, _ = fn(pois, hotel, SC['days'], act, scoring_mode=SC['mode'], **E.HYBRID_PARAMS)
    ev = evaluate_route(routes, hotel, act)
    km = sum(d['distance_km'] for d in ev['days_detail']); mins = sum(d['time_min'] for d in ev['days_detail'])
    meals = [sum(1 for p in day if p['category'] == 'restaurant') for day in routes]
    return {'score': ev['total_score'], 'sights': statistics.mean(sum(1 for p in day if p['category'] != 'restaurant') for day in routes),
            'meals': statistics.mean(meals), 'short': sum(1 for m in meals if m < 2), 'km_day': km / SC['days'],
            'obj': ev['total_score'] - hybrid.DIST_WEIGHT * km - 0.01 * mins, 'valid': ev['valid']}


out = {}
for prov in ('phichit', 'chaiyaphum', 'kalasin', 'singburi'):
    pois, hotel, act = load(prov)
    rest = sum(1 for p in pois if p['category'] == 'restaurant')
    out[prov] = {'restaurants': rest}
    for name, fn in (('current', hybrid.hybrid_solve), ('fixed', hybrid_fixed)):
        rows = [run(fn, pois, hotel, act, s) for s in range(10)]
        out[prov][name] = {k: round(statistics.mean(r[k] for r in rows), 2) for k in rows[0] if k != 'valid'}
        out[prov][name]['valid'] = sum(r['valid'] for r in rows)
    print(prov, json.dumps(out[prov], ensure_ascii=False), flush=True)
json.dump(out, open(os.path.join(E.OUT_DIR, 'phichit_cause.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
