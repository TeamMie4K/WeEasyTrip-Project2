<!-- converted from experiments__make_results_json.py.docx -->

คู่มือโค้ด: experiments/make_results_json.py
สรุปผลทดลองเป็น JSON สำหรับหน้าผลทดลอง
ไฟล์ต้นฉบับ: experiments/make_results_json.py (45 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: อ่านไฟล์ผลทดลองทั้งหมดใน experiments/results/ (json และ stats.txt) แล้วรวมเป็น frontend/results.json ขนาดเล็ก เพื่อให้หน้า ➜ frontend/results.html (แสดงเฉพาะโหมด Developer) แสดงตารางผลทดลองได้ รันเป็นขั้นสุดท้ายของ experiments/run_all_chapter4.sh

บรรทัด 1–16  ส่วน A และ B จากผลจังหวัด
1  # -*- coding: utf-8 -*-
2  """สรุปผลทดลองทั้งหมด (experiments/results/*) เป็นไฟล์เล็กสำหรับหน้า frontend/results.html (แสดงเฉพาะโหมด Developer)"""
3  import json, os, re
4  HERE = os.path.dirname(os.path.abspath(__file__))
5  RES = os.path.join(HERE, 'results')
6  rd = lambda n: open(os.path.join(RES, n), encoding='utf-8').read().splitlines()
7  R = json.load(open(os.path.join(RES, 'province_results.json'), encoding='utf-8'))
8
9  rows = []
10  for k, v in R['part_a'].items():
11      prov, sc = k.split('/')
12      g = lambda a: {'score': v[a]['score']['mean'], 'ms': v[a]['time_ms'], 'valid': v[a]['valid'], 'n': v[a]['n'], 'km': v[a]['km_day'], 'div': v[a]['diversity']}
13      rows.append({'province': prov, 'scenario': sc, 'Greedy': g('Greedy'), 'GA': g('GA'), 'Hybrid': g('Hybrid'), 'HybridDiv': g('HybridDiv'),
14                   'p_vs_ga': v['hybrid_vs_ga']['mwu_greater_p']})
15  reopt = [{'province': k, 'n': v['n'], 'recompute_valid': v['recompute']['valid'], 'reoptimize_valid': v['reoptimize']['valid'],
16            'recompute_meals': v['recompute']['meals_ok'], 'reoptimize_meals': v['reoptimize']['meals_ok'], 'p': v['wilcoxon_greater_p']} for k, v in R['part_b'].items()]
บรรทัด 1–2: docstring
บรรทัด 3–5: นำเข้าโมดูลมาตรฐาน และกำหนดโฟลเดอร์ results
บรรทัด 6: rd ฟังก์ชันอ่านไฟล์ข้อความเป็นรายการบรรทัด
บรรทัด 7: โหลดผลจังหวัด (province_results.json) ซึ่งสร้างโดย ➜ experiments/run_province_experiments.py
บรรทัด 9–14: สร้างแถวของส่วน A: ทุกชุด (จังหวัด/สถานการณ์) เก็บคะแนน เวลา ความถูกต้อง ระยะขับ ความหลากหลายของ 4 อัลกอริทึม และค่า p เทียบ GA
บรรทัด 15–16: สร้างแถวของส่วน B (ปรับแผนหลังผู้ใช้แก้): จำนวนที่ใช้งานได้ มื้อครบ และค่า p
บรรทัด 18–33  ILS RL และ Pareto
18  ils = []
19  for l in rd('ils_stats.txt'):
20      m = re.match(r'(\w+)/(S\d)_\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\S+\s+(\d+)\s+(\d+)\s+(\S+)', l)
21      if m: ils.append({'province': m[1], 'scenario': m[2], 'w': float(m[3]), 'base': float(m[4]), 'ils': float(m[5]), 'gain': float(m[6]), 'ms_base': int(m[7]), 'ms_ils': int(m[8]), 'p': float(m[9])})
22
23  rl = []
24  for l in rd('rl_stats.txt'):
25      m = re.match(r'(\w+)/(\S+?)\s+(train|held-out)\s+(\S+)\s+(\S+)\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)', l)
26      if m: rl.append({'province': m[1], 'scenario': m[2][:2], 'group': m[3], 'greedy': float(m[4]), 'rl': float(m[5]), 'hybrid': float(m[6]), 'hybrid_rl': float(m[7]), 'p': float(m[8])})
27
28  pareto = []
29  for l in rd('pareto_stats.txt'):
30      p = l.split()
31      if p and p[0] in ('phuket', 'chiangmai', 'krabi', 'samui'):
32          pareto.append({'province': p[0], 'hv_nsga': float(p[1]), 'hv_ws': float(p[2]), 'ratio': float(p[3]), 'plans_nsga': float(p[5]), 'plans_ws': float(p[6]),
33                         'ms_nsga': float(p[7]), 'ms_ws': float(p[8]), 'p': float(p[9])})
บรรทัด 18–21: อ่าน ils_stats.txt (จาก ➜ experiments/run_ils_experiments.py) แยกคอลัมน์ด้วย regex เก็บ น้ำหนัก คะแนนก่อน/หลัง ร้อยละที่เพิ่ม เวลา และค่า p
บรรทัด 23–26: อ่าน rl_stats.txt (จาก ➜ experiments/run_rl_experiments.py) แยกกลุ่ม train/held-out และคะแนน
บรรทัด 28–33: อ่าน pareto_stats.txt (จาก ➜ experiments/run_pareto_experiments.py) เก็บ hypervolume จำนวนแผน เวลา และค่า p ต่อจังหวัด
บรรทัด 35–45  ผลจังหวัดข้อมูลน้อยและบันทึก
35  sparse = {}
36  for key, fn in (('S1', 'sparse_stats.txt'), ('S2', 'sparse_stats_S2.txt'), ('S3', 'sparse_stats_S3.txt')):
37      out = []
38      for l in rd(fn)[1:]:
39          m = re.match(r'(\S+)\s+POI=(\d+)\s+H=(\d+)\s+rest=(\d+)\s+Greedy=(\S+)\s+GA=(\S+)\s+Hybrid=(\S+)\s+valid=(\S+)\s+p=(\S+)', l.replace('\t', ' '))
40          if m: out.append({'area': m[1], 'pois': int(m[2]), 'hotels': int(m[3]), 'rest': int(m[4]), 'Greedy': float(m[5]), 'GA': float(m[6]), 'Hybrid': float(m[7]), 'valid': m[8], 'p': float(m[9])})
41      sparse[key] = out
42
43  json.dump({'trials': R['trials'], 'rows': rows, 'reopt': reopt, 'ils': ils, 'rl': rl, 'pareto': pareto, 'sparse': sparse},
44            open(os.path.join(HERE, '..', 'frontend', 'results.json'), 'w', encoding='utf-8'), ensure_ascii=False)
45  print(len(rows), 'rows,', len(reopt), 'reopt,', len(ils), 'ils,', len(rl), 'rl,', len(pareto), 'pareto,', {k: len(v) for k, v in sparse.items()})
บรรทัด 35–41: อ่านผลสามสถานการณ์ของ ➜ experiments/run_sparse_experiments.py (S1 S2 S3) แยกคอลัมน์ด้วย regex
บรรทัด 43–44: เขียนทุกส่วนรวมเป็น frontend/results.json
บรรทัด 45: พิมพ์จำนวนแถวของแต่ละส่วนไว้ตรวจ

ไฟล์ที่เชื่อมกับไฟล์นี้
experiments/run_ils_experiments.py
experiments/run_pareto_experiments.py
experiments/run_province_experiments.py
experiments/run_rl_experiments.py
experiments/run_sparse_experiments.py
frontend/results.html