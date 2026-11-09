# -*- coding: utf-8 -*-
"""สรุปผลทดลองทั้งหมด (experiments/results/*) เป็นไฟล์เล็กสำหรับหน้า frontend/results.html (แสดงเฉพาะโหมด Developer)"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results')
rd = lambda n: open(os.path.join(RES, n), encoding='utf-8').read().splitlines()
R = json.load(open(os.path.join(RES, 'province_results.json'), encoding='utf-8'))

rows = []
for k, v in R['part_a'].items():
    prov, sc = k.split('/')
    g = lambda a: {'score': v[a]['score']['mean'], 'ms': v[a]['time_ms'], 'valid': v[a]['valid'], 'n': v[a]['n'], 'km': v[a]['km_day'], 'div': v[a]['diversity']}
    rows.append({'province': prov, 'scenario': sc, 'Greedy': g('Greedy'), 'GA': g('GA'), 'Hybrid': g('Hybrid'), 'HybridDiv': g('HybridDiv'),
                 'p_vs_ga': v['hybrid_vs_ga']['mwu_greater_p']})
reopt = [{'province': k, 'n': v['n'], 'recompute_valid': v['recompute']['valid'], 'reoptimize_valid': v['reoptimize']['valid'],
          'recompute_meals': v['recompute']['meals_ok'], 'reoptimize_meals': v['reoptimize']['meals_ok'], 'p': v['wilcoxon_greater_p']} for k, v in R['part_b'].items()]

ils = []
for l in rd('ils_stats.txt'):
    m = re.match(r'(\w+)/(S\d)_\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\S+\s+(\d+)\s+(\d+)\s+(\S+)', l)
    if m: ils.append({'province': m[1], 'scenario': m[2], 'w': float(m[3]), 'base': float(m[4]), 'ils': float(m[5]), 'gain': float(m[6]), 'ms_base': int(m[7]), 'ms_ils': int(m[8]), 'p': float(m[9])})

rl = []
for l in rd('rl_stats.txt'):
    m = re.match(r'(\w+)/(\S+?)\s+(train|held-out)\s+(\S+)\s+(\S+)\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)', l)
    if m: rl.append({'province': m[1], 'scenario': m[2][:2], 'group': m[3], 'greedy': float(m[4]), 'rl': float(m[5]), 'hybrid': float(m[6]), 'hybrid_rl': float(m[7]), 'p': float(m[8])})

pareto = []
for l in rd('pareto_stats.txt'):
    p = l.split()
    if p and p[0] in ('phuket', 'chiangmai', 'krabi', 'samui'):
        pareto.append({'province': p[0], 'hv_nsga': float(p[1]), 'hv_ws': float(p[2]), 'ratio': float(p[3]), 'plans_nsga': float(p[5]), 'plans_ws': float(p[6]),
                       'ms_nsga': float(p[7]), 'ms_ws': float(p[8]), 'p': float(p[9])})

sparse = {}
for key, fn in (('S1', 'sparse_stats.txt'), ('S2', 'sparse_stats_S2.txt'), ('S3', 'sparse_stats_S3.txt')):
    out = []
    for l in rd(fn)[1:]:
        m = re.match(r'(\S+)\s+POI=(\d+)\s+H=(\d+)\s+rest=(\d+)\s+Greedy=(\S+)\s+GA=(\S+)\s+Hybrid=(\S+)\s+valid=(\S+)\s+p=(\S+)', l.replace('\t', ' '))
        if m: out.append({'area': m[1], 'pois': int(m[2]), 'hotels': int(m[3]), 'rest': int(m[4]), 'Greedy': float(m[5]), 'GA': float(m[6]), 'Hybrid': float(m[7]), 'valid': m[8], 'p': float(m[9])})
    sparse[key] = out

json.dump({'trials': R['trials'], 'rows': rows, 'reopt': reopt, 'ils': ils, 'rl': rl, 'pareto': pareto, 'sparse': sparse},
          open(os.path.join(HERE, '..', 'frontend', 'results.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(len(rows), 'rows,', len(reopt), 'reopt,', len(ils), 'ils,', len(rl), 'rl,', len(pareto), 'pareto,', {k: len(v) for k, v in sparse.items()})
