<!-- converted from experiments__run_diagnose.py.docx -->

คู่มือโค้ด: experiments/run_diagnose.py
วินิจฉัยผลที่ผิดคาด
ไฟล์ต้นฉบับ: experiments/run_diagnose.py (81 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: หาสาเหตุของสองผลที่ไม่เป็นไปตามคาดในการทดลองหลัก ส่วนที่ 1 ทำไม Hybrid ไม่ชนะ GA ในจังหวัดข้อมูลน้อย 4 จังหวัด (พิจิตร ชัยภูมิ กาฬสินธุ์ สิงห์บุรี) โดยวัดคะแนนดิบ ระยะขับ จำนวนสถานที่และมื้อต่อวัน และค่าเป้าหมายที่หักระยะและเวลา เทียบกับเพดานคะแนน ส่วนที่ 2 ทำไมความชอบหมวดกิจกรรม/จุดชมวิวไม่เพิ่มสัดส่วนในบางจังหวัด โดยนับจำนวนสถานที่ในหมวดที่ชอบของแต่ละจังหวัด ผลคือ results/diagnose.json ที่ใช้ในตารางที่ 4.9-4.10 และหัวข้อวินิจฉัยของรายงาน ใช้ผลของ ➜ experiments/run_preference_experiments.py เป็นข้อมูลนำเข้า

บรรทัด 1–17  หัวไฟล์ ค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  run_diagnose.py — Project 2: ตรวจหาสาเหตุของผลที่ผิดคาด (จังหวัดข้อมูลน้อย S2 และความชอบของผู้ใช้)
4  ส่วน 1: Greedy/GA/Hybrid ใน S2 ของพิจิตร ชัยภูมิ กาฬสินธุ์ สิงห์บุรี: คะแนนดิบ, ระยะขับ, จำนวนมื้อ/วัน,
5          จำนวนวันที่มื้อไม่ครบ, ค่าเป้าหมายหักระยะและเวลา (score - DIST_WEIGHT*km - TIME_WEIGHT*นาที) และเพดานคะแนนเชิงทฤษฎี
6  ส่วน 2: ความชอบ: จำนวนสถานที่ท่องเที่ยวหมวดที่ชอบ (activity+viewpoint) ต่อจังหวัด เทียบกับที่ต้องใช้ 20 จุด (5 วัน x 4)
7          และสัดส่วนเดิมใน baseline; จัดกลุ่มตามความมีนัยสำคัญใน preference_results.json
8  ผลลัพธ์: results/diagnose.json
9  """
10  import sys, os, json, statistics
11  sys.argv = [sys.argv[0], '5']
12  import run_province_experiments as E
13  from utils import evaluate_route
14  import hybrid
15
16  SC = E.SCENARIOS[1]
17  PROVS = ['phichit', 'chaiyaphum', 'kalasin', 'singburi']
บรรทัด 1–9: docstring อธิบายสองส่วนและที่เก็บผล
บรรทัด 10–14: นำเข้าโมดูลมาตรฐาน ➜ experiments/run_province_experiments.py (ชื่อ E) ➜ evaluate_route() ใน algorithm/utils.py และ ➜ algorithm/hybrid.py
บรรทัด 16: ใช้สถานการณ์ S2
บรรทัด 17: PROVS 4 จังหวัดที่ Hybrid ไม่ชนะ GA ใน S2
บรรทัด 20–29  โหลดข้อมูลหนึ่งจังหวัด
20  def load(prov):
21      import utils
22      from utils import load_data, set_travel_profile
23      cfg = E.PROV_CFG[prov]
24      set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
25      pois, hotels = load_data(os.path.join(E.ROOT, 'data', 'provinces', f'{prov}.json'))
26      hs = sorted(hotels, key=lambda h: h['cost'])
27      hotel = hs[int(len(hs) * SC['hotel_frac'])]
28      act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
29      return pois, hotel, act
บรรทัด 20–29: load ตั้งโปรไฟล์เดินทาง โหลดสถานที่และโรงแรม เลือกโรงแรมตามตำแหน่งของสถานการณ์ และคำนวณงบกิจกรรม
บรรทัด 32–55  ส่วนที่ 1: เทียบสามอัลกอริทึม
32  def part1():
33      out = {}
34      for prov in PROVS:
35          pois, hotel, act = load(prov)
36          attr = sorted((p['score'] for p in pois if p['category'] != 'restaurant'), reverse=True)
37          rest = sorted((p['score'] for p in pois if p['category'] == 'restaurant'), reverse=True)
38          out[prov] = {'attractions': len(attr), 'restaurants': len(rest), 'meals_needed': 2 * SC['days'],
39                       'ceiling': sum(attr[:4 * SC['days']]) + sum(rest[:2 * SC['days']]), 'algo': {}}
40          for algo in ('Greedy', 'GA', 'Hybrid'):
41              n = 1 if algo == 'Greedy' else 5
42              rows = []
43              for t in range(n):
44                  routes, m = E.run_algo(algo, pois, hotel, SC['days'], act, SC['mode'], seed=t)
45                  ev = evaluate_route(routes, hotel, act)
46                  km = sum(d['distance_km'] for d in ev['days_detail'])
47                  mins = sum(d['time_min'] for d in ev['days_detail'])
48                  meals = [sum(1 for p in day if p['category'] == 'restaurant') for day in routes]
49                  rows.append({'score': m['score'], 'km_day': km / SC['days'], 'sights_day': statistics.mean(
50                      sum(1 for p in day if p['category'] != 'restaurant') for day in routes),
51                      'meals_day': statistics.mean(meals), 'days_short_meals': sum(1 for x in meals if x < 2),
52                      'objective': m['score'] - hybrid.DIST_WEIGHT * km - 0.01 * mins})
53              out[prov]['algo'][algo] = {k: round(statistics.mean(r[k] for r in rows), 2) for k in rows[0]}
54          print(prov, json.dumps(out[prov], ensure_ascii=False), flush=True)
55      return out
บรรทัด 32–39: ต่อจังหวัด หาจำนวนสถานที่ท่องเที่ยว จำนวนร้านอาหาร จำนวนมื้อที่ต้องการ และเพดานคะแนนที่เป็นไปได้ (สถานที่คะแนนสูงสุด 4 จุดและร้านคะแนนสูงสุด 2 ร้านต่อวัน)
บรรทัด 40–47: รัน Greedy (ครั้งเดียว) GA และ Hybrid (5 รอบ) แล้วคำนวณระยะขับและเวลารวมจาก evaluate_route
บรรทัด 48–52: นับมื้อต่อวัน จำนวนวันที่มื้อไม่ครบ และค่าเป้าหมาย = คะแนน − DIST_WEIGHT × กม. − 0.01 × นาที
บรรทัด 53–55: เฉลี่ยทุกรอบ พิมพ์ผลและคืนค่า
บรรทัด 58–74  ส่วนที่ 2: ความชอบ
58  def part2():
59      pref = json.load(open(os.path.join(E.OUT_DIR, 'preference_results.json'), encoding='utf-8'))['results']
60      like = {'activity', 'viewpoint'}
61      rows = []
62      for prov, r in pref.items():
63          slug = prov
64          f = os.path.join(E.ROOT, 'data', 'provinces', f'{slug}.json')
65          if not os.path.exists(f):
66              continue
67          from utils import load_data
68          pois, _ = load_data(f)
69          attr = [p for p in pois if p['category'] != 'restaurant']
70          n_like = sum(p['category'] in like for p in attr)
71          rows.append({'prov': prov, 'attractions': len(attr), 'liked_avail': n_like,
72                       'base_share': r['baseline']['liked_share'], 'like_share': r['like']['liked_share'],
73                       'p_like': r['like']['p_liked'], 'sig': bool(r['like']['p_liked'] == r['like']['p_liked'] and r['like']['p_liked'] < 0.05)})
74      return rows
บรรทัด 58–61: อ่านผลการทดลองความชอบ (preference_results.json) และกำหนดหมวดที่ชอบ (activity viewpoint)
บรรทัด 62–70: ต่อจังหวัด นับสถานที่ท่องเที่ยวทั้งหมดและที่อยู่ในหมวดที่ชอบ (ข้ามถ้าไม่มีไฟล์ข้อมูล)
บรรทัด 71–74: เก็บจำนวนสถานที่ สัดส่วนก่อนและหลังตั้งความชอบ ค่า p และธงว่ามีนัยสำคัญ (p < 0.05)
บรรทัด 77–81  จุดเริ่มต้น
77  if __name__ == '__main__':
78      p1 = part1()
79      p2 = part2()
80      json.dump({'part1': p1, 'part2': p2}, open(os.path.join(E.OUT_DIR, 'diagnose.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
81      print('saved', len(p2))
บรรทัด 77–81: รันสองส่วน เขียน diagnose.json และพิมพ์จำนวนแถวส่วนที่ 2

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/hybrid.py
algorithm/utils.py
experiments/run_preference_experiments.py
experiments/run_province_experiments.py