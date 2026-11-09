# -*- coding: utf-8 -*-
"""
run_sparse_experiments.py — WeEasyTrip Project 2
ทดลอง Greedy / GA / Hybrid (1) บนจังหวัดข้อมูลน้อย (sparse) และ (2) บนทริปข้ามจังหวัดข้างเคียง (รวมข้อมูลหลายจังหวัด)
ใช้ฟังก์ชันจาก run_province_experiments.py (กติกาและพารามิเตอร์เดียวกัน) — สถานการณ์ S1 (3 วัน 10,000 บาท)
ผลลัพธ์: results/sparse_results.json, results/sparse_stats.txt
รัน:  python run_sparse_experiments.py [trials]
"""
import sys, os, json, statistics
sys.argv = [sys.argv[0]] + sys.argv[1:2]      # ให้ run_province_experiments อ่าน trials จาก argv[1] เท่านั้น
import run_province_experiments as R
from utils import load_data, set_travel_profile
from scipy import stats as st

TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 10
SPARSE = ['nongbualamphu', 'phichit', 'lamphun', 'nakhonnayok', 'singburi', 'kalasin', 'chaiyaphum', 'loei']
COMBOS = [('chiangmai', 'lamphun'), ('bangkok', 'nonthaburi'), ('phuket', 'phangnga'), ('phuket', 'krabi')]
SC = R.SCENARIOS[int(os.environ.get('SC_IDX', 0))]
SUF = '' if SC is R.SCENARIOS[0] else '_' + SC['label'].split('_')[0]
R.TRIALS = TRIALS


def load(slug):
    parts = slug.split('+')
    pois, hotels = [], []
    for s in parts:
        p, h = load_data(os.path.join(R.ROOT, 'data', 'provinces', f'{s}.json'))
        pre = (lambda x: {**x, 'id': f'{s}.{x["id"]}'}) if len(parts) > 1 else (lambda x: x)
        pois += [pre(x) for x in p]; hotels += [pre(x) for x in h]
    cfg = R.PROV_CFG[parts[0]]
    set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
    return pois, hotels


def run(slug):
    pois, hotels = load(slug)
    hs = sorted(hotels, key=lambda h: h['cost'])
    hotel = hs[int(len(hs) * SC['hotel_frac'])]
    act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
    out, groups = {'pois': len(pois), 'hotels': len(hotels), 'restaurants': sum(p['category'] == 'restaurant' for p in pois)}, {}
    for algo in ('Greedy', 'GA', 'Hybrid'):
        n = 1 if algo == 'Greedy' else TRIALS
        tr = [R.run_algo(algo, pois, hotel, SC['days'], act, SC['mode'], seed=t)[1] for t in range(n)]
        groups[algo] = [t['score'] for t in tr]
        out[algo] = {'n': n, 'score': R.summarize(groups[algo]), 'time_ms': R.summarize([t['time_ms'] for t in tr])['mean'],
                     'valid': sum(t['valid'] for t in tr), 'meals_ok': sum(t['meals_ok'] for t in tr), 'km_day': round(statistics.mean(t['km_day'] for t in tr), 1)}
    out['hybrid_vs_ga_p'] = float(st.mannwhitneyu(groups['Hybrid'], groups['GA'], alternative='greater').pvalue)
    return out


if __name__ == '__main__':
    res = {}
    for slug in SPARSE + ['+'.join(c) for c in COMBOS]:
        res[slug] = run(slug)
        r = res[slug]
        print(f"{slug:24s} POI={r['pois']:4d} H={r['hotels']:3d} rest={r['restaurants']:3d}  Greedy={r['Greedy']['score']['mean']:6.1f}  GA={r['GA']['score']['mean']:6.1f}  Hybrid={r['Hybrid']['score']['mean']:6.1f}  valid {r['Hybrid']['valid']}/{r['Hybrid']['n']}  p={r['hybrid_vs_ga_p']:.4f}", flush=True)
    json.dump({'trials': TRIALS, 'scenario': SC['label'], 'results': res}, open(os.path.join(R.OUT_DIR, f'sparse_results{SUF}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(R.OUT_DIR, f'sparse_stats{SUF}.txt'), 'w', encoding='utf-8') as f:
        f.write(f"SPARSE / CROSS-PROVINCE EXPERIMENTS — trials={TRIALS}, scenario={SC['label']}\n")
        for slug, r in res.items():
            f.write(f"{slug}\tPOI={r['pois']}\tH={r['hotels']}\trest={r['restaurants']}\tGreedy={r['Greedy']['score']['mean']}\tGA={r['GA']['score']['mean']}\tHybrid={r['Hybrid']['score']['mean']}\tvalid={r['Hybrid']['valid']}/{r['Hybrid']['n']}\tp={r['hybrid_vs_ga_p']:.4f}\n")
    print('saved')
