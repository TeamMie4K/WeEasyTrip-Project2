# -*- coding: utf-8 -*-
"""
run_phichit_objective.py — Project 2: หาว่าทำไมใน S2 ของพิจิตร Hybrid ได้ "ค่าเป้าหมาย" (คะแนน - 0.3 x กม. - 0.01 x นาที) ต่ำกว่า GA
แม้แก้ขั้นซ่อมแผนแล้ว (คะแนนดิบสูงขึ้นแต่ยังขับไกลกว่า) จังหวัดนี้มีร้านอาหารเพียง 8 ร้านแต่ต้องใช้ 10 มื้อ (5 วัน)
วิธี: เทียบ GA, Greedy, Hybrid ปัจจุบัน และ Hybrid ที่ปิดทีละขั้น (ไม่ใช้ ILS; ซ่อมมื้อแต่ไม่ซ่อมงบ) 10 รอบ วัดคะแนนดิบ กม./วัน
      จำนวนสถานที่และมื้อต่อวัน และค่าเป้าหมาย พร้อมแยกค่าเป้าหมายเป็นส่วนของคะแนน ระยะทาง และเวลา
ผลลัพธ์: results/phichit_objective.json
"""
import sys, os, json, random, statistics
sys.argv = [sys.argv[0], '10']
import run_province_experiments as E
import hybrid
from utils import evaluate_route

SC = E.SCENARIOS[1]
TRIALS = 10
SEED = [0]   # seed ของรอบปัจจุบัน (run_algo ตั้ง random.seed เอง)


def load(prov):
    pois, hotel, act = E.setup(prov, SC)
    return pois, hotel, act


def measure(routes, hotel, act):
    ev = evaluate_route(routes, hotel, act)
    km = sum(d['distance_km'] for d in ev['days_detail'])
    mins = sum(d['time_min'] for d in ev['days_detail'])
    meals = [sum(1 for p in day if p['category'] == 'restaurant') for day in routes]
    return {'score': ev['total_score'], 'km_day': km / SC['days'], 'hours_day': mins / 60 / SC['days'],
            'sights_day': statistics.mean(sum(1 for p in day if p['category'] != 'restaurant') for day in routes),
            'meals_day': statistics.mean(meals), 'short_days': sum(1 for m in meals if m < 2),
            'obj_score': ev['total_score'], 'obj_dist': -hybrid.DIST_WEIGHT * km, 'obj_time': -0.01 * mins,
            'objective': ev['total_score'] - hybrid.DIST_WEIGHT * km - 0.01 * mins, 'valid': bool(ev['valid'])}


def run(prov, label, fn):
    pois, hotel, act = load(prov)
    rows = []
    for s in range(TRIALS):
        SEED[0] = s
        random.seed(s)
        routes = fn(pois, hotel, act)
        rows.append(measure(routes, hotel, act))
    return {k: round(statistics.mean(r[k] for r in rows), 2) for k in rows[0] if k != 'valid'} | {'valid': sum(r['valid'] for r in rows)}


def make_fns():
    hp = E.HYBRID_PARAMS
    by_runner = lambda algo: (lambda p, h, a: E.run_algo(algo, p, h, SC['days'], a, SC['mode'], seed=SEED[0])[0])
    return {
        'Greedy': by_runner('Greedy'), 'GA': by_runner('GA'), 'Hybrid': by_runner('Hybrid'),
        'Hybrid_noILS': lambda p, h, a: hybrid.hybrid_solve(p, h, SC['days'], a, scoring_mode=SC['mode'], ils=False, **hp)[0],
    }


if __name__ == '__main__':
    out = {}
    for prov in ('phichit', 'chaiyaphum'):
        out[prov] = {}
        for label, fn in make_fns().items():
            out[prov][label] = run(prov, label, fn)
            print(prov, label, json.dumps(out[prov][label], ensure_ascii=False), flush=True)
    json.dump(out, open(os.path.join(E.OUT_DIR, 'phichit_objective.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('saved')
