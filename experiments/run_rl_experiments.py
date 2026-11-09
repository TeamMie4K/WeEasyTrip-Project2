# -*- coding: utf-8 -*-
"""
run_rl_experiments.py — Project 2: ประเมิน RL agent (algorithm/rl.py, theta จาก train_rl.py)
ส่วน 1  คุณภาพของแผนเริ่มต้น: Greedy (ตามโหมดของ scenario) เทียบ RL แบบ deterministic
ส่วน 2  ใช้เป็น seed ใน Hybrid: Hybrid ปกติ เทียบ Hybrid ที่มี RL seed (Wilcoxon แบบจับคู่, 15 รอบ)
scenario ที่ฝึก: S1-S3 (ตำแหน่งโรงแรมเดียวกับตอนฝึก); scenario ที่ไม่เคยเห็น: H1 (4 วัน 12,000 โรงแรมตำแหน่ง 0.25), H2 (6 วัน 30,000 ตำแหน่ง 0.75)
"""
import sys, os, json, random, statistics, time
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
sys.argv = [sys.argv[0], '15']
import numpy as np
from scipy import stats as st
import run_province_experiments as E
import rl
from utils import evaluate_route
from greedy import greedy_solve
from hybrid import hybrid_solve

TRIALS = int(os.environ.get('RL_TRIALS', 15))
theta = np.array(json.load(open(os.path.join(HERE, '..', 'algorithm', 'rl_policy.json'), encoding='utf-8'))['theta'])
SCEN = [dict(s, group='train') for s in E.SCENARIOS] + [
    {'label': 'H1_4d_12k', 'budget': 12_000, 'days': 4, 'hotel_frac': 0.25, 'mode': 'ratio', 'group': 'held-out'},
    {'label': 'H2_6d_30k', 'budget': 30_000, 'days': 6, 'hotel_frac': 0.75, 'mode': 'quality', 'group': 'held-out'},
]
OUT = os.path.join(HERE, 'results')


def score(routes, hotel, act):
    ev = evaluate_route(routes, hotel, act)
    return ev['total_score'] if ev['valid'] else 0.0, ev['valid']


def main():
    res, lines = {}, ['=' * 104, f'RL EXPERIMENTS — trials={TRIALS}; seed quality (Greedy vs RL-argmax) and Hybrid with/without RL seeds', '=' * 104,
                      f"{'Province/Scenario':<30}{'grp':<9}{'Greedy':>8}{'RL':>8}{'valid G/R':>11}{'Hybrid':>9}{'Hyb+RL':>9}{'p(RL>H)':>9}{'ms H':>7}{'ms HR':>7}"]
    for prov in E.PROVINCES:
        for sc in SCEN:
            pois, hotel, act = E.setup(prov, sc)
            g, r, gv, rv, h0, h1, t0s, t1s = [], [], 0, 0, [], [], [], []
            for t in range(TRIALS):
                random.seed(t)
                sg, ok = score(greedy_solve(pois, hotel, sc['days'], act, scoring_mode=sc['mode']), hotel, act)
                g.append(sg); gv += ok
                np.random.seed(t)
                sr, ok = score(rl.rl_solve(pois, hotel, sc['days'], act, theta, sample=False), hotel, act)
                r.append(sr); rv += ok
                for lst, th, tl in ((h0, None, t0s), (h1, theta, t1s)):
                    random.seed(t); np.random.seed(t)
                    t0 = time.perf_counter()
                    routes, _ = hybrid_solve(pois, hotel, sc['days'], act, scoring_mode=sc['mode'], rl_theta=th, **E.HYBRID_PARAMS)
                    tl.append((time.perf_counter() - t0) * 1000)
                    lst.append(score(routes, hotel, act)[0])
            try:
                p = st.wilcoxon(h1, h0, alternative='greater').pvalue
            except ValueError:
                p = float('nan')
            key = f'{prov}/{sc["label"]}'
            res[key] = {'group': sc['group'], 'greedy': statistics.mean(g), 'rl': statistics.mean(r), 'valid_g': gv, 'valid_r': rv,
                        'hybrid': statistics.mean(h0), 'hybrid_rl': statistics.mean(h1), 'p_rl_gt_h': p,
                        'ms_h': statistics.mean(t0s), 'ms_hr': statistics.mean(t1s), 'n': TRIALS}
            x = res[key]
            lines.append(f"{key:<30}{sc['group']:<9}{x['greedy']:>8.1f}{x['rl']:>8.1f}{str(gv)+'/'+str(rv):>11}{x['hybrid']:>9.1f}{x['hybrid_rl']:>9.1f}{p:>9.4f}{x['ms_h']:>7.0f}{x['ms_hr']:>7.0f}")
            print(lines[-1], flush=True)
    json.dump({'trials': TRIALS, 'theta': theta.tolist(), 'results': res}, open(os.path.join(OUT, 'rl_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(os.path.join(OUT, 'rl_stats.txt'), 'w', encoding='utf-8').write('\n'.join(lines))


if __name__ == '__main__':
    main()
