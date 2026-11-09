# -*- coding: utf-8 -*-
"""
run_province_experiments.py — WeEasyTrip Project 2
ส่วน A: Greedy / GA / Hybrid × 3 scenarios × 4 จังหวัด (ขยายจาก run_experiments.py ของ Project 1)
ส่วน B: จำลองผู้ใช้แก้แผน (ลบ 2 จุด + สลับ 1 จุด) เทียบ recompute เดิม (ไม่ปรับเส้นทาง) กับ reoptimize_solve ใหม่
        ทดสอบด้วย Wilcoxon signed-rank (paired)
ผลลัพธ์: results/province_results.json, results/province_stats.txt
รัน:  python run_province_experiments.py [trials]
"""
import sys, os, time, json, random, copy, statistics
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'algorithm'))
from scipy import stats as st

from utils import load_data, evaluate_route, set_travel_profile
from greedy import greedy_solve
from genetic import genetic_solve
from hybrid import hybrid_solve, reoptimize_solve, diversity_stats

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'results')
os.makedirs(OUT_DIR, exist_ok=True)
PROVINCES = ['phuket', 'chiangmai', 'krabi', 'samui']
TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 15

# hotel_frac = ตำแหน่งโรงแรมในรายการที่เรียงตามราคา (เทียบเท่า index 2/7/12 จาก 20 โรงแรมของ Project 1)
SCENARIOS = [
    {'label': 'S1_Short_Budget',    'budget': 10_000, 'days': 3, 'hotel_frac': 0.10, 'mode': 'ratio'},
    {'label': 'S2_Medium_Standard', 'budget': 15_000, 'days': 5, 'hotel_frac': 0.35, 'mode': 'ratio'},
    {'label': 'S3_Long_Premium',    'budget': 25_000, 'days': 7, 'hotel_frac': 0.60, 'mode': 'quality'},
]
DIV_W = 1.5   # น้ำหนักความหลากหลายใน Hybrid+Div (ตรงกับ DIVERSITY_WEIGHT ใน backend)
GA_PARAMS = dict(pop_size=50, generations=100, mutation_rate=0.3)
HYBRID_PARAMS = dict(pop_size=30, generations=60, mutation_rate=0.3)


PROV_CFG = json.load(open(os.path.join(ROOT, 'data', 'provinces.json'), encoding='utf-8'))
USE_TRAVEL_PROFILE = '--no-profile' not in sys.argv


def setup(prov, sc):
    cfg = PROV_CFG[prov]
    if USE_TRAVEL_PROFILE:
        set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
    else:
        set_travel_profile()
    pois, hotels = load_data(os.path.join(ROOT, 'data', 'provinces', f'{prov}.json'))
    hs = sorted(hotels, key=lambda h: h['cost'])
    hotel = hs[int(len(hs) * sc['hotel_frac'])]
    nights = max(1, sc['days'] - 1)
    act = max(0.0, sc['budget'] - hotel['cost'] * nights)
    return pois, hotel, act


def min_meals(routes):
    return min((sum(1 for p in d if p['category'] == 'restaurant') for d in routes), default=0)


def run_algo(algo, pois, hotel, days, act, mode, seed):
    random.seed(seed)
    t0 = time.perf_counter()
    if algo == 'Greedy':
        routes = greedy_solve(pois, hotel, days, act, scoring_mode=mode)
    elif algo == 'GA':
        routes, _ = genetic_solve(pois, hotel, days, act, **GA_PARAMS)
    else:   # 'Hybrid' = แบบ Project 1 (ไม่มี diversity), 'HybridDiv' = เพิ่ม diversity ใน fitness
        w = DIV_W if algo == 'HybridDiv' else 0.0
        routes, _ = hybrid_solve(pois, hotel, days, act, scoring_mode=mode, diversity_weight=w, **HYBRID_PARAMS)
    ms = (time.perf_counter() - t0) * 1000
    ev = evaluate_route(routes, hotel, act)
    dv, over = diversity_stats(routes)
    return routes, {'score': ev['total_score'], 'valid': ev['valid'], 'time_ms': round(ms, 1),
                    'meals_ok': min_meals(routes) >= 2, 'diversity': dv, 'over': over,
                    'km_day': sum(d['distance_km'] for d in ev['days_detail']) / max(days, 1)}


def summarize(vals):
    return {'mean': round(statistics.mean(vals), 2),
            'stdev': round(statistics.stdev(vals), 2) if len(vals) > 1 else 0.0,
            'min': round(min(vals), 2), 'max': round(max(vals), 2)}


def part_a():
    res = {}
    for prov in PROVINCES:
        for sc in SCENARIOS:
            pois, hotel, act = setup(prov, sc)
            key = f"{prov}/{sc['label']}"
            res[key] = {'hotel': hotel['id'], 'act_budget': act}
            groups = {}
            for algo in ('Greedy', 'GA', 'Hybrid', 'HybridDiv'):
                n = 1 if algo == 'Greedy' else TRIALS
                trials = [run_algo(algo, pois, hotel, sc['days'], act, sc['mode'], seed=t)[1] for t in range(n)]
                groups[algo] = [t['score'] for t in trials]
                res[key][algo] = {
                    'n': n, 'score': summarize(groups[algo]),
                    'time_ms': summarize([t['time_ms'] for t in trials])['mean'],
                    'valid': sum(t['valid'] for t in trials), 'meals_ok': sum(t['meals_ok'] for t in trials),
                    'km_day': round(statistics.mean(t['km_day'] for t in trials), 1),
                    'diversity': round(statistics.mean(t['diversity'] for t in trials), 2),
                    'over': round(statistics.mean(t['over'] for t in trials), 2)}
            h = st.kruskal(groups['GA'], groups['Hybrid'])
            mw = st.mannwhitneyu(groups['Hybrid'], groups['GA'], alternative='greater')
            res[key]['hybrid_vs_ga'] = {'kruskal_p': float(h.pvalue), 'mwu_greater_p': float(mw.pvalue)}
            dv = st.mannwhitneyu(groups['HybridDiv'], groups['Hybrid'], alternative='two-sided')
            res[key]['div_vs_hybrid'] = {'mwu_two_sided_p': float(dv.pvalue)}
            print(key, {a: res[key][a]['score']['mean'] for a in ('Greedy', 'GA', 'Hybrid', 'HybridDiv')}, flush=True)
    return res


def part_b():
    res = {}
    for prov in PROVINCES:
        for sc in SCENARIOS:
            pois, hotel, act = setup(prov, sc)
            by_id = {p['id']: p for p in pois}
            rows = []
            for t in range(TRIALS):
                routes, _ = run_algo('HybridDiv', pois, hotel, sc['days'], act, sc['mode'], seed=t)
                rng = random.Random(1000 + t)
                flat = [(d, p['id']) for d, day in enumerate(routes) for p in day]
                removed = [pid for _, pid in rng.sample(flat, min(2, len(flat)))]
                edited = [[p for p in day if p['id'] not in removed] for day in routes]
                used = {p['id'] for day in edited for p in day} | set(removed)
                attrs_free = [p for p in pois if p['category'] != 'restaurant' and p['id'] not in used]
                slots = [(d, i) for d, day in enumerate(edited) for i, p in enumerate(day) if p['category'] != 'restaurant']
                locked = []
                if slots and attrs_free:
                    d, i = rng.choice(slots)
                    new = rng.choice(attrs_free)
                    edited[d][i] = new
                    locked = [new['id']]
                # A) ระบบเดิม: ใช้แผนที่แก้ตรง ๆ ไม่ปรับเส้นทาง
                evA = evaluate_route(edited, hotel, act)
                A = {'score': evA['total_score'], 'valid': evA['valid'], 'meals_ok': min_meals(edited) >= 2}
                A['adj'] = A['score'] if A['valid'] else 0.0   # แผนที่ผิดข้อจำกัดใช้งานไม่ได้ → นับเป็น 0
                # B) ใหม่: reoptimize
                random.seed(t)
                t0 = time.perf_counter()
                newr = reoptimize_solve(pois, hotel, edited, act, locked_ids=locked, excluded_ids=removed,
                                        scoring_mode=sc['mode'], diversity_weight=DIV_W)
                ms = (time.perf_counter() - t0) * 1000
                evB = evaluate_route(newr, hotel, act)
                ids = {p['id'] for day in newr for p in day}
                B = {'score': evB['total_score'], 'valid': evB['valid'], 'meals_ok': min_meals(newr) >= 2,
                     'adj': evB['total_score'] if evB['valid'] else 0.0,
                     'locked_kept': set(locked) <= ids, 'excluded_absent': not (set(removed) & ids), 'time_ms': ms}
                rows.append({'A': A, 'B': B})
            sa = [r['A']['score'] for r in rows]; sb = [r['B']['score'] for r in rows]
            aa = [r['A']['adj'] for r in rows]; ab = [r['B']['adj'] for r in rows]
            try:
                w = st.wilcoxon(ab, aa, alternative='greater').pvalue
            except ValueError:
                w = 1.0
            key = f"{prov}/{sc['label']}"
            res[key] = {
                'recompute': {'score': summarize(sa), 'adj_mean': round(statistics.mean(aa), 2), 'valid': sum(r['A']['valid'] for r in rows),
                              'meals_ok': sum(r['A']['meals_ok'] for r in rows)},
                'reoptimize': {'score': summarize(sb), 'adj_mean': round(statistics.mean(ab), 2), 'valid': sum(r['B']['valid'] for r in rows),
                               'meals_ok': sum(r['B']['meals_ok'] for r in rows),
                               'locked_kept': sum(r['B']['locked_kept'] for r in rows),
                               'excluded_absent': sum(r['B']['excluded_absent'] for r in rows),
                               'time_ms': round(statistics.mean(r['B']['time_ms'] for r in rows), 1)},
                'n': len(rows), 'wilcoxon_greater_p': float(w)}
            print('B', key, 'recompute', res[key]['recompute']['score']['mean'], 'reopt', res[key]['reoptimize']['score']['mean'], flush=True)
    return res


def write_report(a, b):
    L = ['=' * 100, f'PROJECT 2 EXPERIMENTS — 4 provinces, trials={TRIALS} (Greedy deterministic = 1), travel profile={USE_TRAVEL_PROFILE}', '=' * 100,
         '', 'PART A: mean score  |  Hybrid = Project 1 fitness, Hybrid+Div = + diversity (w=%.1f)' % DIV_W, '']
    L.append(f"{'Province/Scenario':<28}{'Greedy':>7}{'GA':>7}{'Hybrid':>8}{'Hyb+Div':>8}{'valid':>7}{'meals':>7}{'div H':>7}{'div HD':>7}{'ms HD':>7}{'p(H>GA)':>9}{'p(HD~H)':>9}")
    for k, v in a.items():
        L.append(f"{k:<28}{v['Greedy']['score']['mean']:>7.1f}{v['GA']['score']['mean']:>7.1f}{v['Hybrid']['score']['mean']:>8.1f}{v['HybridDiv']['score']['mean']:>8.1f}"
                 f"{str(v['HybridDiv']['valid'])+'/'+str(v['HybridDiv']['n']):>7}{str(v['HybridDiv']['meals_ok'])+'/'+str(v['HybridDiv']['n']):>7}"
                 f"{v['Hybrid']['diversity']:>7.2f}{v['HybridDiv']['diversity']:>7.2f}{v['HybridDiv']['time_ms']:>7.0f}"
                 f"{v['hybrid_vs_ga']['mwu_greater_p']:>9.4f}{v['div_vs_hybrid']['mwu_two_sided_p']:>9.4f}")
    L += ['', 'PART A2: ระยะขับเฉลี่ยต่อวัน (km/วัน) — ยิ่งน้อยยิ่งสมจริง/ปฏิบัติตามได้', f"{'Province/Scenario':<28}{'Greedy':>8}{'GA':>8}{'Hybrid':>8}{'Hyb+Div':>9}"]
    for k, v in a.items():
        L.append(f"{k:<28}{v['Greedy']['km_day']:>8.1f}{v['GA']['km_day']:>8.1f}{v['Hybrid']['km_day']:>8.1f}{v['HybridDiv']['km_day']:>9.1f}")
    L += ['', 'PART B: after user edit (delete 2 + swap 1): recompute-only (A) vs reoptimize (B); adj = score if valid else 0', '']
    L.append(f"{'Province/Scenario':<30}{'adjA':>8}{'adjB':>8}{'valid A':>9}{'valid B':>9}{'meals A':>9}{'meals B':>9}{'lock':>6}{'excl':>6}{'ms':>7}{'p(B>A)':>9}")
    for k, v in b.items():
        n = v['n']
        L.append(f"{k:<30}{v['recompute']['adj_mean']:>8.1f}{v['reoptimize']['adj_mean']:>8.1f}"
                 f"{str(v['recompute']['valid'])+'/'+str(n):>9}{str(v['reoptimize']['valid'])+'/'+str(n):>9}"
                 f"{str(v['recompute']['meals_ok'])+'/'+str(n):>9}{str(v['reoptimize']['meals_ok'])+'/'+str(n):>9}"
                 f"{str(v['reoptimize']['locked_kept'])+'/'+str(n):>6}{str(v['reoptimize']['excluded_absent'])+'/'+str(n):>6}"
                 f"{v['reoptimize']['time_ms']:>7.0f}{v['wilcoxon_greater_p']:>9.4f}")
    txt = '\n'.join(L)
    print('\n' + txt)
    open(os.path.join(OUT_DIR, 'province_stats.txt'), 'w', encoding='utf-8').write(txt)


if __name__ == '__main__':
    only_b = 'b' in sys.argv[2:]
    a = json.load(open(os.path.join(OUT_DIR, 'province_results.json'), encoding='utf-8'))['part_a'] if only_b else part_a()
    b = part_b()
    json.dump({'trials': TRIALS, 'part_a': a, 'part_b': b},
              open(os.path.join(OUT_DIR, 'province_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    write_report(a, b)
