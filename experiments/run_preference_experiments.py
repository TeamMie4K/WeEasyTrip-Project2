# -*- coding: utf-8 -*-
"""
run_preference_experiments.py — WeEasyTrip Project 2 เฟส 3 (User Preference)
วัดผลของความชอบต่อแผนที่ Hybrid+Div สร้าง: 4 จังหวัด × scenario S2 × 15 รอบ (seed เดียวกันทุกเงื่อนไข)
เงื่อนไข: baseline | avoid{temple,market} | like{activity,viewpoint} | like+avoid
ตัวชี้วัด: จำนวนจุดหมวดที่ไม่เอา (ต้อง 0), สัดส่วนจุดหมวดที่ชอบ, คะแนนจริง (ไม่รวมตัวถ่วง), ผ่านข้อจำกัด, มื้อครบ
ผลลัพธ์: results/preference_results.json, results/preference_stats.txt
"""
import sys, os, json, random, statistics
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
sys.path.insert(0, os.path.join(HERE, '..', 'backend'))
from scipy import stats as st
import main as api                      # ใช้ apply_preferences / restore_originals ตัวเดียวกับ backend
from utils import evaluate_route, set_travel_profile
from hybrid import hybrid_solve

OUT = os.path.join(HERE, 'results')
TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 15
SC = {'days': 5, 'budget': 15_000, 'hotel_frac': 0.35, 'mode': 'ratio'}
LIKE, AVOID = ['activity', 'viewpoint'], ['temple', 'market']
CONDS = {
    'baseline':   None,
    'avoid':      api.Preferences(avoided=AVOID),
    'like':       api.Preferences(liked=LIKE),
    'like+avoid': api.Preferences(liked=LIKE, avoided=AVOID),
}
HYBRID = dict(pop_size=30, generations=60, mutation_rate=0.3)


def run(prov):
    d = api.DATA[prov]
    pv = api.PROVINCES[prov]
    set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
    hs = sorted(d['hotels'], key=lambda h: h['cost'])
    hotel = hs[int(len(hs) * SC['hotel_frac'])]
    act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
    rows = {c: [] for c in CONDS}
    for t in range(TRIALS):
        for name, pref in CONDS.items():
            pool, _ = api.apply_preferences(d['pois'], pref, SC['days'])
            random.seed(t)
            routes, _ = hybrid_solve(pool, hotel, SC['days'], act, scoring_mode=SC['mode'],
                                     diversity_weight=api.DIVERSITY_WEIGHT, **HYBRID)
            routes = api.restore_originals(routes, d['poi_by_id'])
            ev = evaluate_route(routes, hotel, act)
            pois = [p for day in routes for p in day if p['category'] != 'restaurant']
            rows[name].append({
                'avoided': sum(p['category'] in AVOID for p in pois),
                'liked_share': (sum(p['category'] in LIKE for p in pois) / len(pois)) if pois else 0.0,
                'score': ev['total_score'], 'valid': ev['valid'],
                'meals': all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in routes if day)})
    return rows


def main_():
    res, lines = {}, ['=' * 96, f'PREFERENCE EXPERIMENTS — Hybrid+Div, S2 (5 days, 15,000 THB), trials={TRIALS}', '=' * 96,
                      f"{'Province':<11}{'Condition':<12}{'avoided#':>9}{'liked%':>8}{'score':>8}{'Δscore%':>9}{'valid':>7}{'meals':>7}{'p(score)':>10}{'p(liked)':>10}"]
    for prov in api.DATA:
        rows = run(prov)
        base = [r['score'] for r in rows['baseline']]
        bl = [r['liked_share'] for r in rows['baseline']]
        res[prov] = {}
        for name, rs in rows.items():
            sc = [r['score'] for r in rs]
            try:
                p_sc = st.wilcoxon(sc, base).pvalue if name != 'baseline' else float('nan')
                p_lk = st.wilcoxon([r['liked_share'] for r in rs], bl, alternative='greater').pvalue if 'like' in name else float('nan')
            except ValueError:
                p_sc = p_lk = float('nan')
            m = {'avoided_mean': statistics.mean(r['avoided'] for r in rs),
                 'liked_share': statistics.mean(r['liked_share'] for r in rs),
                 'score': statistics.mean(sc), 'delta_pct': 100 * (statistics.mean(sc) - statistics.mean(base)) / statistics.mean(base),
                 'valid': sum(r['valid'] for r in rs), 'meals': sum(r['meals'] for r in rs), 'n': len(rs),
                 'p_score': p_sc, 'p_liked': p_lk}
            res[prov][name] = m
            lines.append(f"{prov:<11}{name:<12}{m['avoided_mean']:>9.2f}{100*m['liked_share']:>8.1f}{m['score']:>8.1f}{m['delta_pct']:>9.1f}"
                         f"{str(m['valid'])+'/'+str(m['n']):>7}{str(m['meals'])+'/'+str(m['n']):>7}{p_sc:>10.4f}{p_lk:>10.4f}")
        print(prov, 'done', flush=True)
    json.dump({'trials': TRIALS, 'like': LIKE, 'avoid': AVOID, 'results': res},
              open(os.path.join(OUT, 'preference_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    txt = '\n'.join(lines)
    open(os.path.join(OUT, 'preference_stats.txt'), 'w', encoding='utf-8').write(txt)
    print(txt)


if __name__ == '__main__':
    main_()
