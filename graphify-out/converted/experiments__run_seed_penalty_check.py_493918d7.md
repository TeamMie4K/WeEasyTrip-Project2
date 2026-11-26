<!-- converted from experiments__run_seed_penalty_check.py.docx -->

คู่มือโค้ด: experiments/run_seed_penalty_check.py
ตรวจผลของค่าปรับระยะของ Greedy seed
ไฟล์ต้นฉบับ: experiments/run_seed_penalty_check.py (33 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ทดสอบสมมติฐานที่ได้จาก ➜ experiments/run_phichit_objective.py ว่า Hybrid ได้ค่าเป้าหมายต่ำในพิจิตรเพราะเริ่มจาก seed ของ Greedy ที่ขับไกล (ค่าปรับระยะ GREEDY_KM_PENALTY = 10 บาทต่อกม.) โดยรัน ➜ hybrid_solve() ใน algorithm/hybrid.py ที่ค่าปรับ 10 (ค่าในระบบ) 50 และ 200 ใน 6 จังหวัด สถานการณ์ S2 จังหวัดละ 10 รอบ ค่าปรับนี้เปลี่ยนเฉพาะในการทดลองนี้ ไม่ได้เปลี่ยนค่าในระบบ ผลคือ results/seed_penalty_check.json ที่ใช้ในหัวข้อ 4.2.9 ของรายงาน

บรรทัด 1–16  หัวไฟล์ ค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  run_seed_penalty_check.py — Project 2: ตรวจผลของค่าปรับระยะของ Greedy seed (GREEDY_KM_PENALTY) ต่อ Hybrid
4  เพื่อทดสอบสมมติฐานว่า Hybrid ได้ค่าเป้าหมายต่ำกว่า GA ในพิจิตรเพราะเริ่มจาก seed ที่ขับไกล (ค่าปรับ 10 บาทต่อกม.)
5  วิธี: S2, Hybrid ค่าปรับ 10 (ค่าในระบบ) เทียบ 50 และ 200 ใน 6 จังหวัด (พิจิตร ชัยภูมิ และ 4 จังหวัดหลัก) 10 รอบ
6        วัดคะแนนดิบ ระยะขับ/วัน และค่าเป้าหมาย (คะแนน - 0.3 x กม. - 0.01 x นาที) ค่าปรับนี้เปลี่ยนเฉพาะในการทดลองนี้
7  ผลลัพธ์: results/seed_penalty_check.json
8  """
9  import sys, os, json, random, statistics
10  sys.argv = [sys.argv[0], '10']
11  import run_province_experiments as E
12  import greedy, hybrid
13  from utils import evaluate_route
14
15  SC = E.SCENARIOS[1]
16  TRIALS = 10
บรรทัด 1–8: docstring อธิบายสมมติฐาน วิธี และที่เก็บผล
บรรทัด 9–13: นำเข้าโมดูลมาตรฐาน ➜ experiments/run_province_experiments.py (ชื่อ E) ➜ algorithm/greedy.py ➜ algorithm/hybrid.py และ ➜ evaluate_route() ใน algorithm/utils.py
บรรทัด 15–16: ใช้สถานการณ์ S2 จำนวน 10 รอบ
บรรทัด 17–33  วนทุกจังหวัดและทุกค่าปรับ
17  out = {}
18  for prov in ('phichit', 'chaiyaphum', 'phuket', 'chiangmai', 'krabi', 'samui'):
19      pois, hotel, act = E.setup(prov, SC)
20      out[prov] = {}
21      for pen in (10.0, 50.0, 200.0):
22          greedy.GREEDY_KM_PENALTY = pen
23          rows = []
24          for s in range(TRIALS):
25              random.seed(s)
26              r, _ = hybrid.hybrid_solve(pois, hotel, SC['days'], act, scoring_mode=SC['mode'], **E.HYBRID_PARAMS)
27              ev = evaluate_route(r, hotel, act)
28              km = sum(d['distance_km'] for d in ev['days_detail']); mins = sum(d['time_min'] for d in ev['days_detail'])
29              rows.append((ev['total_score'], km / SC['days'], ev['total_score'] - hybrid.DIST_WEIGHT * km - 0.01 * mins, bool(ev['valid'])))
30          out[prov][str(pen)] = {'score': round(statistics.mean(x[0] for x in rows), 1), 'km_day': round(statistics.mean(x[1] for x in rows), 1),
31                                 'objective': round(statistics.mean(x[2] for x in rows), 1), 'valid': sum(x[3] for x in rows)}
32      print(prov, json.dumps(out[prov]), flush=True)
33  json.dump(out, open(os.path.join(E.OUT_DIR, 'seed_penalty_check.json'), 'w', encoding='utf-8'), indent=1)
บรรทัด 17–20: ต่อจังหวัด (พิจิตร ชัยภูมิ ภูเก็ต เชียงใหม่ กระบี่ สมุย) โหลดข้อมูลด้วย E.setup
บรรทัด 21–22: ตั้งค่า GREEDY_KM_PENALTY ของโมดูล greedy เป็น 10 50 หรือ 200 ซึ่ง seed ของ Hybrid อ่านค่านี้ตอนสร้างแผน
บรรทัด 23–29: รัน Hybrid ด้วย seed 0-9 วัดคะแนนดิบ ระยะขับต่อวัน ค่าเป้าหมาย และธง valid
บรรทัด 30–32: เฉลี่ยผลของแต่ละค่าปรับแล้วพิมพ์
บรรทัด 33: เขียน seed_penalty_check.json

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/greedy.py
algorithm/hybrid.py
algorithm/utils.py
experiments/run_phichit_objective.py
experiments/run_province_experiments.py