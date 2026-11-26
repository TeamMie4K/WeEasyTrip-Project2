# -*- coding: utf-8 -*-
"""
run_diagnose.py — Project 2: ตรวจหาสาเหตุของผลที่ผิดคาด (จังหวัดข้อมูลน้อย S2 และความชอบของผู้ใช้)
ส่วน 1: Greedy/GA/Hybrid ใน S2 ของพิจิตร ชัยภูมิ กาฬสินธุ์ สิงห์บุรี: คะแนนดิบ, ระยะขับ, จำนวนมื้อ/วัน,
        จำนวนวันที่มื้อไม่ครบ, ค่าเป้าหมายหักระยะและเวลา (score - DIST_WEIGHT*km - TIME_WEIGHT*นาที) และเพดานคะแนนเชิงทฤษฎี
ส่วน 2: ความชอบ: จำนวนสถานที่ท่องเที่ยวหมวดที่ชอบ (activity+viewpoint) ต่อจังหวัด เทียบกับที่ต้องใช้ 20 จุด (5 วัน x 4)
        และสัดส่วนเดิมใน baseline; จัดกลุ่มตามความมีนัยสำคัญใน preference_results.json
ผลลัพธ์: results/diagnose.json
"""
import sys, os, json, statistics
sys.argv = [sys.argv[0], '5']
import run_province_experiments as E
from utils import evaluate_route
import hybrid

SC = E.SCENARIOS[1]
PROVS = ['phichit', 'chaiyaphum', 'kalasin', 'singburi']


def load(prov):
    import utils
    from utils import load_data, set_travel_profile
    cfg = E.PROV_CFG[prov]
    set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
    pois, hotels = load_data(os.path.join(E.ROOT, 'data', 'provinces', f'{prov}.json'))
    hs = sorted(hotels, key=lambda h: h['cost'])
    hotel = hs[int(len(hs) * SC['hotel_frac'])]
    act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
    return pois, hotel, act


def part1():
    out = {}
    for prov in PROVS:
        pois, hotel, act = load(prov)
        attr = sorted((p['score'] for p in pois if p['category'] != 'restaurant'), reverse=True)
        rest = sorted((p['score'] for p in pois if p['category'] == 'restaurant'), reverse=True)
        out[prov] = {'attractions': len(attr), 'restaurants': len(rest), 'meals_needed': 2 * SC['days'],
                     'ceiling': sum(attr[:4 * SC['days']]) + sum(rest[:2 * SC['days']]), 'algo': {}}
        for algo in ('Greedy', 'GA', 'Hybrid'):
            n = 1 if algo == 'Greedy' else 5
            rows = []
            for t in range(n):
                routes, m = E.run_algo(algo, pois, hotel, SC['days'], act, SC['mode'], seed=t)
                ev = evaluate_route(routes, hotel, act)
                km = sum(d['distance_km'] for d in ev['days_detail'])
                mins = sum(d['time_min'] for d in ev['days_detail'])
                meals = [sum(1 for p in day if p['category'] == 'restaurant') for day in routes]
                rows.append({'score': m['score'], 'km_day': km / SC['days'], 'sights_day': statistics.mean(
                    sum(1 for p in day if p['category'] != 'restaurant') for day in routes),
                    'meals_day': statistics.mean(meals), 'days_short_meals': sum(1 for x in meals if x < 2),
                    'objective': m['score'] - hybrid.DIST_WEIGHT * km - 0.01 * mins})
            out[prov]['algo'][algo] = {k: round(statistics.mean(r[k] for r in rows), 2) for k in rows[0]}
        print(prov, json.dumps(out[prov], ensure_ascii=False), flush=True)
    return out


def part2():
    pref = json.load(open(os.path.join(E.OUT_DIR, 'preference_results.json'), encoding='utf-8'))['results']
    like = {'activity', 'viewpoint'}
    rows = []
    for prov, r in pref.items():
        slug = prov
        f = os.path.join(E.ROOT, 'data', 'provinces', f'{slug}.json')
        if not os.path.exists(f):
            continue
        from utils import load_data
        pois, _ = load_data(f)
        attr = [p for p in pois if p['category'] != 'restaurant']
        n_like = sum(p['category'] in like for p in attr)
        rows.append({'prov': prov, 'attractions': len(attr), 'liked_avail': n_like,
                     'base_share': r['baseline']['liked_share'], 'like_share': r['like']['liked_share'],
                     'p_like': r['like']['p_liked'], 'sig': bool(r['like']['p_liked'] == r['like']['p_liked'] and r['like']['p_liked'] < 0.05)})
    return rows


if __name__ == '__main__':
    p1 = part1()
    p2 = part2()
    json.dump({'part1': p1, 'part2': p2}, open(os.path.join(E.OUT_DIR, 'diagnose.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('saved', len(p2))
