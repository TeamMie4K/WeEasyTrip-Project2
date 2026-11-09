# -*- coding: utf-8 -*-
"""
run_ils_experiments.py — Project 2: วัดผล insertion local search (algorithm/ils.py) ด้วยโปรโตคอลเดิม
4 จังหวัด × 3 scenarios × 15 รอบ (seed เดียวกัน), เทียบ Hybrid (w=0) / Hybrid+ILS และ Hybrid+Div (w=1.5) / Hybrid+Div+ILS
ทดสอบ Wilcoxon แบบจับคู่ (ทางเดียว: ILS > ปกติ) และวัดเวลาที่เพิ่ม
ผลลัพธ์: results/ils_results.json, results/ils_stats.txt
"""
import sys, os, json, random, statistics, time
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
sys.argv = [sys.argv[0], '15']
from scipy import stats as st
import run_province_experiments as E
from utils import evaluate_route
from hybrid import hybrid_solve

TRIALS = int(os.environ.get('ILS_TRIALS', 15))
OUT = os.path.join(HERE, 'results')


def run(pois, hotel, sc, act, w, ils, t):
    random.seed(t)
    t0 = time.perf_counter()
    routes, _ = hybrid_solve(pois, hotel, sc['days'], act, scoring_mode=sc['mode'], diversity_weight=w, ils=ils, **E.HYBRID_PARAMS)
    ms = (time.perf_counter() - t0) * 1000
    ev = evaluate_route(routes, hotel, act)
    meals = all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in routes if day)
    return (ev['total_score'] if ev['valid'] and meals else 0.0), ev['valid'] and meals, ms


def main():
    res, lines = {}, ['=' * 100, f'ILS EXPERIMENTS — trials={TRIALS}', '=' * 100,
                      f"{'Province/Scenario':<30}{'w':>4}{'base':>8}{'+ILS':>8}{'gain%':>7}{'valid b/i':>11}{'ms b':>7}{'ms i':>7}{'p(ILS>b)':>10}"]
    for prov in E.PROVINCES:
        for sc in E.SCENARIOS:
            pois, hotel, act = E.setup(prov, sc)
            for w in (0.0, 1.5):
                b, i, vb, vi, mb, mi = [], [], 0, 0, [], []
                for t in range(TRIALS):
                    s0, ok0, m0 = run(pois, hotel, sc, act, w, False, t)
                    s1, ok1, m1 = run(pois, hotel, sc, act, w, True, t)
                    b.append(s0); i.append(s1); vb += ok0; vi += ok1; mb.append(m0); mi.append(m1)
                try:
                    p = st.wilcoxon(i, b, alternative='greater').pvalue
                except ValueError:
                    p = float('nan')
                key = f'{prov}/{sc["label"]}/w={w}'
                gain = 100 * (statistics.mean(i) - statistics.mean(b)) / statistics.mean(b)
                res[key] = {'w': w, 'base': statistics.mean(b), 'ils': statistics.mean(i), 'gain_pct': gain, 'valid_base': vb, 'valid_ils': vi,
                            'ms_base': statistics.mean(mb), 'ms_ils': statistics.mean(mi), 'p': p, 'n': TRIALS}
                lines.append(f"{prov+'/'+sc['label']:<30}{w:>4}{res[key]['base']:>8.1f}{res[key]['ils']:>8.1f}{gain:>7.2f}{str(vb)+'/'+str(vi):>11}{res[key]['ms_base']:>7.0f}{res[key]['ms_ils']:>7.0f}{p:>10.4f}")
                print(lines[-1], flush=True)
    json.dump({'trials': TRIALS, 'results': res}, open(os.path.join(OUT, 'ils_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(os.path.join(OUT, 'ils_stats.txt'), 'w', encoding='utf-8').write('\n'.join(lines))


if __name__ == '__main__':
    main()
