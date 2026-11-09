# -*- coding: utf-8 -*-
"""
run_pareto_experiments.py — Project 2: เทียบ NSGA-II (Pareto front) กับ Hybrid แบบ weighted-sum
วัตถุประสงค์ 3 ข้อ: คะแนน(max) / ความหลากหลายของหมวดต่อวัน(max) / ระยะทางรวม(min)
baseline = Hybrid ที่ตั้งน้ำหนักความหลากหลาย w ∈ {0, 1.5, 3, 6} (4 แผน) แล้วเอาเฉพาะแผนที่ non-dominated
เทียบด้วย hypervolume (Monte Carlo, จุดอ้างอิงและกล่องร่วมกันของแต่ละ trial) และจำนวนแผนที่ผู้ใช้เลือกได้
ผลลัพธ์: results/pareto_results.json, results/pareto_stats.txt
"""
import sys, os, json, random, statistics, time
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
sys.argv = [sys.argv[0], '15'] + sys.argv[1:]
import run_province_experiments as E
from scipy import stats as st
from hybrid import hybrid_solve
from pareto import nsga2_solve, evaluate_objectives, hypervolume, _dominates

TRIALS = int(os.environ.get('PARETO_TRIALS', 8))
SC = E.SCENARIOS[1]          # S2: 5 วัน 15,000 บาท
WEIGHTS = [0.0, 1.5, 3.0, 6.0]
OUT = os.path.join(HERE, 'results')


def nondominated(items):
    return [a for a in items if not any(_dominates(b, a) for b in items if b is not a)]


def main():
    res, lines = {}, ['=' * 92, f'PARETO EXPERIMENTS — NSGA-II vs weighted-sum Hybrid, S2 (5 days), trials={TRIALS}', '=' * 92,
                      f"{'Province':<11}{'HV NSGA':>10}{'HV WS':>10}{'ratio':>8}{'ratio2D':>9}{'#plans N':>10}{'#plans WS':>11}{'ms N':>8}{'ms WS':>8}{'p(HV)':>9}"]
    for prov in E.PROVINCES:
        pois, hotel, act = E.setup(prov, SC)
        hv_n, hv_w, nn, nw, tn, tw = [], [], [], [], [], []
        h2_n, h2_w = [], []   # hypervolume เฉพาะ 2 ด้าน (คะแนน, ความหลากหลาย) ซึ่งตรงกับสิ่งที่ weighted-sum ปรับให้
        for t in range(TRIALS):
            random.seed(t)
            t0 = time.perf_counter()
            front = nsga2_solve(pois, hotel, SC['days'], act, scoring_mode='quality', pop_size=40, generations=40)
            tn.append((time.perf_counter() - t0) * 1000)
            ws = []
            t0 = time.perf_counter()
            for w in WEIGHTS:
                random.seed(t)
                routes, _ = hybrid_solve(pois, hotel, SC['days'], act, scoring_mode='quality', diversity_weight=w, **E.HYBRID_PARAMS)
                e = evaluate_objectives(routes, hotel, act)
                if e['viol'] == 0:
                    ws.append(e)
            tw.append((time.perf_counter() - t0) * 1000)
            ws = nondominated(ws)
            nn.append(len(front)); nw.append(len(ws))
            pts_n = [s['obj'] for s in front]
            pts_w = [s['obj'] for s in ws]
            allp = pts_n + pts_w
            if not allp:
                hv_n.append(0.0); hv_w.append(0.0)
                continue
            ref = tuple(max(p[m] for p in allp) + 0.05 * (max(p[m] for p in allp) - min(p[m] for p in allp) + 1e-9) for m in range(3))
            # กล่องเดียวกันทั้งสองวิธี: ใช้ min ร่วมโดยเพิ่มจุด 'กำหนดกล่อง' ไม่ได้ จึงคำนวณ HV ด้วยกล่องจาก min ร่วม
            lo = tuple(min(p[m] for p in allp) for m in range(3))

            def hv(points, dims=3):
                # Monte Carlo ในกล่อง [lo, ref] เดียวกัน (dims=2: เฉพาะคะแนนและความหลากหลาย)
                rng = random.Random(t)
                hit = 0
                S = 40000
                for _ in range(S):
                    q = [rng.uniform(lo[m], ref[m]) for m in range(dims)]
                    if any(all(p[m] <= q[m] for m in range(dims)) for p in points):
                        hit += 1
                vol = 1.0
                for m in range(dims):
                    vol *= max(ref[m] - lo[m], 1e-12)
                return vol * hit / S

            hv_n.append(hv(pts_n)); hv_w.append(hv(pts_w) if pts_w else 0.0)
            h2_n.append(hv(pts_n, 2)); h2_w.append(hv(pts_w, 2) if pts_w else 0.0)
        try:
            p = st.wilcoxon(hv_n, hv_w, alternative='greater').pvalue
        except ValueError:
            p = float('nan')
        ratio = statistics.mean(hv_n) / max(statistics.mean(hv_w), 1e-9)
        res[prov] = {'hv_nsga': statistics.mean(hv_n), 'hv_ws': statistics.mean(hv_w), 'ratio': ratio,
                     'plans_nsga': statistics.mean(nn), 'plans_ws': statistics.mean(nw),
                     'ms_nsga': statistics.mean(tn), 'ms_ws': statistics.mean(tw), 'p': p, 'n': TRIALS,
                     'hv2_nsga': statistics.mean(h2_n), 'hv2_ws': statistics.mean(h2_w), 'ratio2': statistics.mean(h2_n) / max(statistics.mean(h2_w), 1e-9)}
        r = res[prov]
        lines.append(f"{prov:<11}{r['hv_nsga']:>10.0f}{r['hv_ws']:>10.0f}{ratio:>8.2f}{r['ratio2']:>9.2f}{r['plans_nsga']:>10.1f}{r['plans_ws']:>11.1f}{r['ms_nsga']:>8.0f}{r['ms_ws']:>8.0f}{p:>9.4f}")
        print(lines[-1], flush=True)
    json.dump({'trials': TRIALS, 'weights': WEIGHTS, 'results': res}, open(os.path.join(OUT, 'pareto_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(os.path.join(OUT, 'pareto_stats.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
