# -*- coding: utf-8 -*-
"""
sweep_provinces.py — กวาดทดสอบ API /api/packages กับทุกชุดข้อมูลจังหวัด หลายเงื่อนไขงบ/จำนวนวัน/รวมโรงแรม
ตรวจทุกแพ็กเกจ: ผ่านข้อจำกัด (valid), ไม่เกินงบ, ทุกวันมีสถานที่ท่องเที่ยว, ครบ 4 แห่งต่อวัน, มีมื้อ 2 มื้อต่อวัน
จำนวนวันถูกจำกัดตาม max_days ของจังหวัดเหมือนหน้าเว็บ
รัน:  python tests/sweep_provinces.py [จำนวน process]      ผลลัพธ์: experiments/results/sweep_provinces.json
"""
import os, sys, json, time
from multiprocessing import Pool
os.environ['WET_RATE_PER_MIN'] = '1000000'      # ปิดตัวจำกัดอัตราคำขอเฉพาะการทดสอบ
ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.join(ROOT, 'algorithm')); sys.path.insert(0, os.path.join(ROOT, 'backend'))

# (งบรวม, วัน, จำนวนคน, รวมโรงแรมในงบ)
CASES = [(1000, 1, 1, False), (1000, 2, 1, False), (1000, 3, 1, False), (2000, 3, 1, False), (5000, 3, 2, False),
         (3000, 2, 1, False), (10000, 4, 2, True), (2000, 4, 2, False), (1000, 2, 1, True)]


def work(slugs):
    from fastapi.testclient import TestClient
    import main as api
    api.SESSION_FILE = os.path.join(os.environ.get('TEMP', '.'), f'sweep_sessions_{os.getpid()}.json')
    c = TestClient(api.app)
    out = []
    for slug in slugs:
        mx = api._max_days(slug)
        for ci, (budget, days, trav, hotel) in enumerate(CASES):
            d = min(days, mx)
            r = c.post('/api/packages', json={'province': slug, 'budget': budget, 'days': d, 'travelers': trav, 'seed': 1, 'include_hotel': hotel})
            if r.status_code != 200:
                out.append({'slug': slug, 'case': ci, 'status': r.status_code, 'detail': str(r.text)[:120]}); continue
            for pkg in r.json()['packages']:
                sights = [sum(1 for p in day['pois'] if p['category'] != 'restaurant') for day in pkg['days']]
                meals = [sum(1 for p in day['pois'] if p['category'] == 'restaurant') for day in pkg['days']]
                out.append({'slug': slug, 'case': ci, 'tier': pkg['tier'], 'status': 200, 'days': d, 'clamped': d != days, 'valid': pkg['valid'],
                            'over_budget': pkg['total_cost'] > budget + 1e-6, 'cost': pkg['total_cost'], 'budget': budget,
                            'no_sights': sum(sights) == 0, 'empty_days': sum(1 for s in sights if s == 0), 'short_days': sum(1 for s in sights if s < 4),
                            'short_meals_days': sum(1 for m in meals if m < 2), 'notes': len(pkg.get('notes', [])), 'violations': pkg.get('violations', [])})
    return out


if __name__ == '__main__':
    import main as api
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    slugs = sorted(api.DATA)
    chunks = [slugs[i::nproc] for i in range(nproc)]
    t0 = time.time()
    with Pool(nproc) as pool:
        res = [x for part in pool.map(work, chunks) for x in part]
    ok = [r for r in res if r['status'] == 200]
    summary = {'datasets': len(slugs), 'cases': len(CASES), 'plans': len(ok), 'http_errors': [r for r in res if r['status'] != 200],
               'invalid': sum(not r['valid'] for r in ok), 'over_budget': sum(r['over_budget'] for r in ok), 'no_sights': sum(r['no_sights'] for r in ok),
               'plans_with_empty_day': sum(r['empty_days'] > 0 for r in ok), 'plans_with_short_sight_days': sum(r['short_days'] > 0 for r in ok),
               'plans_with_short_meals': sum(r['short_meals_days'] > 0 for r in ok), 'plans_with_notes': sum(r['notes'] > 0 for r in ok),
               'clamped_requests': sum(1 for r in ok if r['clamped']) // 3, 'seconds': round(time.time() - t0)}
    json.dump({'summary': summary, 'plans': ok}, open(os.path.join(ROOT, 'experiments', 'results', 'sweep_provinces.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(json.dumps({k: v for k, v in summary.items() if k != 'http_errors'}, ensure_ascii=False, indent=1), 'http_errors', len(summary['http_errors']))
