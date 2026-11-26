<!-- converted from experiments__run_phichit_objective.py.docx -->

คู่มือโค้ด: experiments/run_phichit_objective.py
ตรวจค่าเป้าหมายของ Hybrid ในพิจิตร
ไฟล์ต้นฉบับ: experiments/run_phichit_objective.py (65 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: หาว่าทำไมใน S2 ของพิจิตร Hybrid ได้ค่าเป้าหมาย (คะแนน − 0.3 × กม. − 0.01 × นาที) ต่ำกว่า GA แม้แก้ขั้นซ่อมแผนแล้ว เทียบ Greedy GA Hybrid และ Hybrid ที่ปิด ILS ด้วยกติกาและพารามิเตอร์ของ ➜ experiments/run_province_experiments.py 10 รอบ แล้วแยกค่าเป้าหมายเป็นส่วนของคะแนน ระยะทาง และเวลา ผลคือ results/phichit_objective.json ที่ใช้ในหัวข้อ 4.2.9 ของรายงาน ต่อด้วย ➜ experiments/run_seed_penalty_check.py ที่ทดสอบสาเหตุที่พบ

บรรทัด 1–22  หัวไฟล์ ค่าคงที่ และโหลดข้อมูล
1  # -*- coding: utf-8 -*-
2  """
3  run_phichit_objective.py — Project 2: หาว่าทำไมใน S2 ของพิจิตร Hybrid ได้ "ค่าเป้าหมาย" (คะแนน - 0.3 x กม. - 0.01 x นาที) ต่ำกว่า GA
4  แม้แก้ขั้นซ่อมแผนแล้ว (คะแนนดิบสูงขึ้นแต่ยังขับไกลกว่า) จังหวัดนี้มีร้านอาหารเพียง 8 ร้านแต่ต้องใช้ 10 มื้อ (5 วัน)
5  วิธี: เทียบ GA, Greedy, Hybrid ปัจจุบัน และ Hybrid ที่ปิดทีละขั้น (ไม่ใช้ ILS; ซ่อมมื้อแต่ไม่ซ่อมงบ) 10 รอบ วัดคะแนนดิบ กม./วัน
6        จำนวนสถานที่และมื้อต่อวัน และค่าเป้าหมาย พร้อมแยกค่าเป้าหมายเป็นส่วนของคะแนน ระยะทาง และเวลา
7  ผลลัพธ์: results/phichit_objective.json
8  """
9  import sys, os, json, random, statistics
10  sys.argv = [sys.argv[0], '10']
11  import run_province_experiments as E
12  import hybrid
13  from utils import evaluate_route
14
15  SC = E.SCENARIOS[1]
16  TRIALS = 10
17  SEED = [0]   # seed ของรอบปัจจุบัน (run_algo ตั้ง random.seed เอง)
18
19
20  def load(prov):
21      pois, hotel, act = E.setup(prov, SC)
22      return pois, hotel, act
บรรทัด 1–8: docstring อธิบายคำถาม วิธีเทียบ และที่เก็บผล
บรรทัด 9–13: นำเข้าโมดูลมาตรฐาน ➜ experiments/run_province_experiments.py (ชื่อ E) ➜ algorithm/hybrid.py และ ➜ evaluate_route() ใน algorithm/utils.py
บรรทัด 15–17: ใช้สถานการณ์ S2 จำนวน 10 รอบ และตัวเก็บ seed ของรอบปัจจุบัน
บรรทัด 20–22: load โหลดข้อมูลจังหวัด เลือกโรงแรม และคำนวณงบกิจกรรมด้วย E.setup
บรรทัด 25–34  วัดแผนหนึ่งแผน
25  def measure(routes, hotel, act):
26      ev = evaluate_route(routes, hotel, act)
27      km = sum(d['distance_km'] for d in ev['days_detail'])
28      mins = sum(d['time_min'] for d in ev['days_detail'])
29      meals = [sum(1 for p in day if p['category'] == 'restaurant') for day in routes]
30      return {'score': ev['total_score'], 'km_day': km / SC['days'], 'hours_day': mins / 60 / SC['days'],
31              'sights_day': statistics.mean(sum(1 for p in day if p['category'] != 'restaurant') for day in routes),
32              'meals_day': statistics.mean(meals), 'short_days': sum(1 for m in meals if m < 2),
33              'obj_score': ev['total_score'], 'obj_dist': -hybrid.DIST_WEIGHT * km, 'obj_time': -0.01 * mins,
34              'objective': ev['total_score'] - hybrid.DIST_WEIGHT * km - 0.01 * mins, 'valid': bool(ev['valid'])}
บรรทัด 25–34: measure ประเมินแผนด้วย evaluate_route แล้วคืนคะแนนดิบ กม./วัน ชม./วัน จำนวนสถานที่และมื้อต่อวัน จำนวนวันที่มื้อไม่ครบ และค่าเป้าหมายแยกเป็นส่วนของคะแนน ระยะ และเวลา
บรรทัด 37–45  รันหลายรอบ
37  def run(prov, label, fn):
38      pois, hotel, act = load(prov)
39      rows = []
40      for s in range(TRIALS):
41          SEED[0] = s
42          random.seed(s)
43          routes = fn(pois, hotel, act)
44          rows.append(measure(routes, hotel, act))
45      return {k: round(statistics.mean(r[k] for r in rows), 2) for k in rows[0] if k != 'valid'} | {'valid': sum(r['valid'] for r in rows)}
บรรทัด 37–45: run รันอัลกอริทึมหนึ่งตัวด้วย seed 0-9 แล้วเฉลี่ยทุกตัวชี้วัด พร้อมนับจำนวนแผนที่ผ่านข้อจำกัด
บรรทัด 48–54  รายการอัลกอริทึมที่เทียบ
48  def make_fns():
49      hp = E.HYBRID_PARAMS
50      by_runner = lambda algo: (lambda p, h, a: E.run_algo(algo, p, h, SC['days'], a, SC['mode'], seed=SEED[0])[0])
51      return {
52          'Greedy': by_runner('Greedy'), 'GA': by_runner('GA'), 'Hybrid': by_runner('Hybrid'),
53          'Hybrid_noILS': lambda p, h, a: hybrid.hybrid_solve(p, h, SC['days'], a, scoring_mode=SC['mode'], ils=False, **hp)[0],
54      }
บรรทัด 48–54: make_fns กำหนด Greedy GA และ Hybrid ผ่าน E.run_algo และ Hybrid ที่ปิด ILS (ils=False) เพื่อดูว่า ILS ช่วยลดช่องว่างได้เท่าใด
บรรทัด 57–65  จุดเริ่มต้น
57  if __name__ == '__main__':
58      out = {}
59      for prov in ('phichit', 'chaiyaphum'):
60          out[prov] = {}
61          for label, fn in make_fns().items():
62              out[prov][label] = run(prov, label, fn)
63              print(prov, label, json.dumps(out[prov][label], ensure_ascii=False), flush=True)
64      json.dump(out, open(os.path.join(E.OUT_DIR, 'phichit_objective.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
65      print('saved')
บรรทัด 57–63: รันกับพิจิตรและชัยภูมิ ทุกอัลกอริทึม แล้วพิมพ์ผลทีละบรรทัด
บรรทัด 64–65: เขียน phichit_objective.json

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/hybrid.py
algorithm/utils.py
experiments/run_province_experiments.py
experiments/run_seed_penalty_check.py