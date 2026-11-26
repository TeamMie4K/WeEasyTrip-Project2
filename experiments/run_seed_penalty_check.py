# -*- coding: utf-8 -*-
"""
run_seed_penalty_check.py — Project 2: ตรวจผลของค่าปรับระยะของ Greedy seed (GREEDY_KM_PENALTY) ต่อ Hybrid
เพื่อทดสอบสมมติฐานว่า Hybrid ได้ค่าเป้าหมายต่ำกว่า GA ในพิจิตรเพราะเริ่มจาก seed ที่ขับไกล (ค่าปรับ 10 บาทต่อกม.)
วิธี: S2, Hybrid ค่าปรับ 10 (ค่าในระบบ) เทียบ 50 และ 200 ใน 6 จังหวัด (พิจิตร ชัยภูมิ และ 4 จังหวัดหลัก) 10 รอบ
      วัดคะแนนดิบ ระยะขับ/วัน และค่าเป้าหมาย (คะแนน - 0.3 x กม. - 0.01 x นาที) ค่าปรับนี้เปลี่ยนเฉพาะในการทดลองนี้
ผลลัพธ์: results/seed_penalty_check.json
"""
import sys, os, json, random, statistics
sys.argv = [sys.argv[0], '10']
import run_province_experiments as E
import greedy, hybrid
from utils import evaluate_route

SC = E.SCENARIOS[1]
TRIALS = 10
out = {}
for prov in ('phichit', 'chaiyaphum', 'phuket', 'chiangmai', 'krabi', 'samui'):
    pois, hotel, act = E.setup(prov, SC)
    out[prov] = {}
    for pen in (10.0, 50.0, 200.0):
        greedy.GREEDY_KM_PENALTY = pen
        rows = []
        for s in range(TRIALS):
            random.seed(s)
            r, _ = hybrid.hybrid_solve(pois, hotel, SC['days'], act, scoring_mode=SC['mode'], **E.HYBRID_PARAMS)
            ev = evaluate_route(r, hotel, act)
            km = sum(d['distance_km'] for d in ev['days_detail']); mins = sum(d['time_min'] for d in ev['days_detail'])
            rows.append((ev['total_score'], km / SC['days'], ev['total_score'] - hybrid.DIST_WEIGHT * km - 0.01 * mins, bool(ev['valid'])))
        out[prov][str(pen)] = {'score': round(statistics.mean(x[0] for x in rows), 1), 'km_day': round(statistics.mean(x[1] for x in rows), 1),
                               'objective': round(statistics.mean(x[2] for x in rows), 1), 'valid': sum(x[3] for x in rows)}
    print(prov, json.dumps(out[prov]), flush=True)
json.dump(out, open(os.path.join(E.OUT_DIR, 'seed_penalty_check.json'), 'w', encoding='utf-8'), indent=1)
