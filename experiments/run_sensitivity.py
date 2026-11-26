# -*- coding: utf-8 -*-
"""
run_sensitivity.py — Project 2: วิเคราะห์ความไวของพารามิเตอร์ที่ผู้พัฒนาเลือกเอง
พารามิเตอร์: DIST_WEIGHT (หักคะแนนต่อ กม. ใน Hybrid/GA/ILS), GREEDY_KM_PENALTY (บาทต่อ กม. ของ Greedy),
             TRAFFIC_FACTOR (ตัวคูณเวลาเดินทาง), TIME_WEIGHT (หักคะแนนต่อนาทีของเวลาทั้งวัน)
สถานการณ์ S2 (5 วัน 15,000 บาท) 4 จังหวัด; ปรับทีละพารามิเตอร์ ตัวอื่นคงค่าเดิม
ตัวชี้วัด: คะแนนเฉลี่ย (ไม่รวมตัวหัก), กม./วัน, ชม./วัน, ผ่านข้อจำกัด+มื้อครบ, Hybrid เทียบ GA (Mann-Whitney ทางเดียว)
รัน:  python run_sensitivity.py <dist|greedy|traffic|time> [trials]
ผลลัพธ์: results/sensitivity_<name>.json
"""
import sys, os, json, statistics
NAME = sys.argv[1]
TRIALS = int(sys.argv[2]) if len(sys.argv) > 2 else 8
sys.argv = [sys.argv[0], str(TRIALS)]
import run_province_experiments as E
import hybrid, ils, genetic, greedy, utils
from utils import evaluate_route
from scipy import stats as st

SC = E.SCENARIOS[1]
GRID = {'dist': [0.0, 0.1, 0.3, 0.6, 1.0], 'greedy': [0.0, 10.0, 30.0, 100.0],
        'traffic': [1.0, 1.25, 1.5], 'time': [0.0, 0.01, 0.03]}
BASE = {'dist': 0.3, 'greedy': 10.0, 'traffic': 1.25, 'time': 0.01}


def apply(v):
    if NAME == 'dist':
        hybrid.DIST_WEIGHT = ils.DIST_WEIGHT = genetic.DIST_WEIGHT = v
    elif NAME == 'greedy':
        greedy.GREEDY_KM_PENALTY = v
    elif NAME == 'traffic':
        utils.TRAFFIC_FACTOR = v
    else:
        utils.TIME_WEIGHT = v


def one(prov, algo):
    pois, hotel, act = E.setup(prov, SC)
    n = 1 if algo == 'Greedy' else TRIALS
    rows = []
    for t in range(n):
        routes, m = E.run_algo(algo, pois, hotel, SC['days'], act, SC['mode'], seed=t)
        ev = evaluate_route(routes, hotel, act)
        hrs = statistics.mean(d['time_min'] for d in ev['days_detail']) / 60
        rows.append({**m, 'hours_day': hrs, 'ok': m['valid'] and m['meals_ok']})
    return rows


def main():
    res = {}
    for v in GRID[NAME]:
        apply(v)
        cell = {}
        for algo in ('Greedy', 'GA', 'Hybrid'):
            if NAME == 'greedy' and algo != 'Greedy':
                continue
            per, allrows = {}, []
            for prov in E.PROVINCES:
                rows = one(prov, algo)
                per[prov] = [r['score'] for r in rows]
                allrows += rows
            cell[algo] = {'score': statistics.mean(r['score'] for r in allrows),
                          'km_day': statistics.mean(r['km_day'] for r in allrows),
                          'hours_day': statistics.mean(r['hours_day'] for r in allrows),
                          'ok': sum(r['ok'] for r in allrows), 'n': len(allrows),
                          'per_prov': {p: statistics.mean(x) for p, x in per.items()}, 'raw': per}
        if 'GA' in cell:
            h = [s for p in E.PROVINCES for s in cell['Hybrid']['raw'][p]]
            g = [s for p in E.PROVINCES for s in cell['GA']['raw'][p]]
            cell['hybrid_vs_ga_p'] = float(st.mannwhitneyu(h, g, alternative='greater').pvalue)
        for a in cell:
            if isinstance(cell[a], dict):
                cell[a].pop('raw', None)
        res[str(v)] = cell
        print(NAME, v, json.dumps({a: (round(c['score'], 1), round(c['km_day'], 1), round(c['hours_day'], 1)) for a, c in cell.items() if isinstance(c, dict)}),
              cell.get('hybrid_vs_ga_p'), flush=True)
        json.dump({'param': NAME, 'base': BASE[NAME], 'trials': TRIALS, 'scenario': SC['label'], 'results': res},
                  open(os.path.join(E.OUT_DIR, f'sensitivity_{NAME}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
