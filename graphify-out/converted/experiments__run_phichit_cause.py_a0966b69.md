<!-- converted from experiments__run_phichit_cause.py.docx -->

คู่มือโค้ด: experiments/run_phichit_cause.py
ทดสอบสาเหตุที่ Hybrid แพ้ในพิจิตร
ไฟล์ต้นฉบับ: experiments/run_phichit_cause.py (58 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ทดสอบสมมติฐานว่าทำไม Hybrid ได้คะแนนต่ำกว่า GA และ Greedy ในจังหวัดที่ร้านอาหารไม่พอ (พิจิตร) สมมติฐานคือขั้นซ่อมแผนใน ➜ hybrid_solve() ใน algorithm/hybrid.py ถอดสถานที่ท่องเที่ยวคะแนนต่ำสุดเมื่อวันนั้นมีมื้อไม่ครบ แม้สาเหตุคือไม่มีร้านให้เติม จึงเสียสถานที่โดยไม่ได้มื้อเพิ่ม สคริปต์เทียบ Hybrid ปัจจุบันกับ Hybrid ที่แก้ให้ถอดเฉพาะเมื่อร้านอาหารพอสำหรับทั้งทริป ผลคือ results/phichit_cause.json (เป็นที่มาของการแก้ใน hybrid.py ที่ใช้อยู่ตอนนี้ และตารางที่ 4.10)

บรรทัด 1–24  หัวไฟล์ และสร้าง Hybrid ฉบับแก้
1  # -*- coding: utf-8 -*-
2  """
3  run_phichit_cause.py — ทดสอบสมมติฐานว่าทำไม Hybrid ได้คะแนนต่ำกว่า GA/Greedy ในจังหวัดที่ร้านอาหารไม่พอ (พิจิตร S2)
4  สมมติฐาน: ขั้น 6 ของ hybrid_solve ถอดสถานที่ท่องเที่ยวคะแนนต่ำสุดวันละ 1 จุด (สูงสุด 3 รอบ) เมื่อวันนั้นมีมื้อไม่ครบ
5            แม้สาเหตุคือ "ไม่มีร้านอาหารให้เติม" (ไม่ใช่เวลาไม่พอ) จึงเสียสถานที่ท่องเที่ยวโดยไม่ได้มื้อเพิ่ม
6  วิธี: (A) Hybrid ปัจจุบัน  (B) Hybrid ที่แก้ให้ไม่ถอดสถานที่เมื่อจำนวนร้านอาหารทั้งหมดน้อยกว่า 2 x จำนวนวัน
7        เทียบคะแนนดิบ จำนวนสถานที่ท่องเที่ยว/วัน มื้อ/วัน ระยะขับ และค่าเป้าหมาย (คะแนน - 0.3 x กม. - 0.01 x นาที)
8        ใน 4 จังหวัดข้อมูลน้อย (พิจิตร ชัยภูมิ กาฬสินธุ์ สิงห์บุรี) สถานการณ์ S2 รอบละ 10 รอบ
9  ผลลัพธ์: results/phichit_cause.json
10  """
11  import sys, os, json, random, statistics
12  sys.argv = [sys.argv[0], '10']
13  import run_province_experiments as E
14  import hybrid
15  from utils import evaluate_route
16
17  SC = E.SCENARIOS[1]
18  src = open(hybrid.__file__, encoding='utf-8-sig').read()
19  OLD = "            if day and sum(1 for p in day if p['category'] == 'restaurant') < 2:\n                cands"
20  NEW = "            if day and sum(1 for p in day if p['category'] == 'restaurant') < 2 and sum(1 for p in pois if p['category'] == 'restaurant') >= 2 * days:\n                cands"
21  assert OLD in src
22  ns = dict(hybrid.__dict__)
23  exec(compile(src.replace(OLD, NEW), 'hybrid_patched', 'exec'), ns)
24  hybrid_fixed = ns['hybrid_solve']
บรรทัด 1–10: docstring อธิบายสมมติฐาน วิธีเทียบ จังหวัดที่ทดสอบ และที่เก็บผล
บรรทัด 11–17: นำเข้า ➜ experiments/run_province_experiments.py (ชื่อ E) ➜ algorithm/hybrid.py และ ➜ evaluate_route() ใน algorithm/utils.py และใช้สถานการณ์ S2
บรรทัด 18–20: อ่านซอร์สของ hybrid.py แล้วกำหนดข้อความเดิมและข้อความใหม่ที่เพิ่มเงื่อนไขว่าร้านอาหารทั้งหมดต้องมีอย่างน้อย 2 ร้านต่อวัน
บรรทัด 21–24: รันซอร์สที่แก้ในเนมสเปซแยก เพื่อได้ hybrid_fixed โดยไม่แก้ไฟล์จริง (ปัจจุบันการแก้นี้อยู่ใน hybrid.py แล้ว จึงเหลือไว้เป็นหลักฐานการทดลอง)
บรรทัด 27–34  โหลดข้อมูลหนึ่งจังหวัด
27  def load(prov):
28      from utils import load_data, set_travel_profile
29      cfg = E.PROV_CFG[prov]
30      set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
31      pois, hotels = load_data(os.path.join(E.ROOT, 'data', 'provinces', f'{prov}.json'))
32      hs = sorted(hotels, key=lambda h: h['cost'])
33      hotel = hs[int(len(hs) * SC['hotel_frac'])]
34      return pois, hotel, max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
บรรทัด 27–34: load ตั้งโปรไฟล์เดินทาง โหลดข้อมูล เลือกโรงแรมตามสถานการณ์ และคำนวณงบกิจกรรม
บรรทัด 37–45  รันหนึ่งรอบ
37  def run(fn, pois, hotel, act, seed):
38      random.seed(seed)
39      routes, _ = fn(pois, hotel, SC['days'], act, scoring_mode=SC['mode'], **E.HYBRID_PARAMS)
40      ev = evaluate_route(routes, hotel, act)
41      km = sum(d['distance_km'] for d in ev['days_detail']); mins = sum(d['time_min'] for d in ev['days_detail'])
42      meals = [sum(1 for p in day if p['category'] == 'restaurant') for day in routes]
43      return {'score': ev['total_score'], 'sights': statistics.mean(sum(1 for p in day if p['category'] != 'restaurant') for day in routes),
44              'meals': statistics.mean(meals), 'short': sum(1 for m in meals if m < 2), 'km_day': km / SC['days'],
45              'obj': ev['total_score'] - hybrid.DIST_WEIGHT * km - 0.01 * mins, 'valid': ev['valid']}
บรรทัด 37–45: run รันอัลกอริทึมหนึ่งรอบด้วย seed วัดคะแนนดิบ จำนวนสถานที่และมื้อต่อวัน จำนวนวันที่มื้อไม่ครบ ระยะขับต่อวัน ค่าเป้าหมาย และธง valid
บรรทัด 48–58  วนทุกจังหวัดและบันทึกผล
48  out = {}
49  for prov in ('phichit', 'chaiyaphum', 'kalasin', 'singburi'):
50      pois, hotel, act = load(prov)
51      rest = sum(1 for p in pois if p['category'] == 'restaurant')
52      out[prov] = {'restaurants': rest}
53      for name, fn in (('current', hybrid.hybrid_solve), ('fixed', hybrid_fixed)):
54          rows = [run(fn, pois, hotel, act, s) for s in range(10)]
55          out[prov][name] = {k: round(statistics.mean(r[k] for r in rows), 2) for k in rows[0] if k != 'valid'}
56          out[prov][name]['valid'] = sum(r['valid'] for r in rows)
57      print(prov, json.dumps(out[prov], ensure_ascii=False), flush=True)
58  json.dump(out, open(os.path.join(E.OUT_DIR, 'phichit_cause.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
บรรทัด 48–57: สำหรับพิจิตร ชัยภูมิ กาฬสินธุ์ สิงห์บุรี รัน 10 รอบทั้งรุ่นปัจจุบันและรุ่นแก้ แล้วเฉลี่ย
บรรทัด 58: เขียน phichit_cause.json

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/hybrid.py
algorithm/utils.py
experiments/run_province_experiments.py