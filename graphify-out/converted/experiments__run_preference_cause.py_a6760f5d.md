<!-- converted from experiments__run_preference_cause.py.docx -->

คู่มือโค้ด: experiments/run_preference_cause.py
ทดสอบสาเหตุที่ความชอบไม่เพิ่มสัดส่วน
ไฟล์ต้นฉบับ: experiments/run_preference_cause.py (67 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: หาสาเหตุที่การตั้งความชอบ (ชอบกิจกรรม/จุดชมวิว) ไม่เพิ่มสัดส่วนสถานที่หมวดนั้นอย่างมีนัยสำคัญใน 8 จังหวัดที่มีสถานที่หมวดนั้นเพียง 6-10 จุด ตรวจสองสมมติฐาน คือน้ำหนักถ่วง LIKE_BOOST (ค่าปัจจุบัน 1.0) น้อยเกินไปเมื่อเทียบกับช่วงคะแนนสถานที่ หรือสถานที่ในหมวดที่ชอบมีคะแนนต่ำหรืออยู่ไกลโรงแรม วิธีคือรัน ➜ hybrid_solve() ใน algorithm/hybrid.py ด้วย LIKE_BOOST 1.0 เทียบ 3.0 และ 5.0 ผ่านฟังก์ชันของ ➜ backend/main.py ผลคือ results/preference_cause.json ที่ใช้อธิบายผลความชอบในรายงาน

บรรทัด 1–24  หัวไฟล์ ค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  run_preference_cause.py — หาสาเหตุที่ความชอบ (ชอบกิจกรรม/จุดชมวิว) ไม่เพิ่มสัดส่วนอย่างมีนัยสำคัญใน 8 จังหวัดที่มีสถานที่หมวดนั้น 6-10 จุด
4  ตรวจ 2 สมมติฐาน: (H1) น้ำหนักถ่วง LIKE_BOOST = 1.0 น้อยเกินไปเมื่อเทียบกับช่วงคะแนนสถานที่  (H2) สถานที่ในหมวดที่ชอบมีคะแนนต่ำหรืออยู่ไกลโรงแรม
5  วิธี: S2, Hybrid+Div, 15 รอบ, LIKE_BOOST = 1.0 (ค่าปัจจุบัน) เทียบ 3.0 และ 5.0; วัดสัดส่วนจุดหมวดที่ชอบ (Wilcoxon ทางเดียวเทียบเงื่อนไขปกติ)
6        พร้อมสถิติของสถานที่ในหมวดที่ชอบ: คะแนนเฉลี่ยเทียบสถานที่ท่องเที่ยวทั้งหมด และระยะเฉลี่ยถึงโรงแรมที่ใช้
7  ผลลัพธ์: results/preference_cause.json
8  """
9  import sys, os, json, random, statistics
10  HERE = os.path.dirname(__file__)
11  sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
12  sys.path.insert(0, os.path.join(HERE, '..', 'backend'))
13  from scipy import stats as st
14  import main as api
15  from utils import evaluate_route, set_travel_profile, haversine_km
16  from hybrid import hybrid_solve
17
18  OUT = os.path.join(HERE, 'results')
19  PROVS = ['buengkan', 'phangnga', 'phayao', 'phrae', 'prachuapkhirikhan', 'ranong', 'saraburi', 'suratthani']
20  LIKE = ['activity', 'viewpoint']
21  SC = {'days': 5, 'budget': 15_000, 'hotel_frac': 0.35, 'mode': 'ratio'}
22  HY = dict(pop_size=30, generations=60, mutation_rate=0.3)
23  TRIALS = 15
24  PREF = api.Preferences(liked=LIKE)
บรรทัด 1–8: docstring อธิบายสมมติฐาน วิธี และที่เก็บผล
บรรทัด 9–16: นำเข้าโมดูลมาตรฐาน scipy.stats ➜ backend/main.py (ชื่อ api) ➜ algorithm/utils.py และ ➜ algorithm/hybrid.py
บรรทัด 18: โฟลเดอร์เก็บผลลัพธ์
บรรทัด 19: PROVS 8 จังหวัดที่ตรวจ
บรรทัด 20: LIKE หมวดที่ชอบ (activity viewpoint)
บรรทัด 21–22: สถานการณ์ S2 และพารามิเตอร์ Hybrid
บรรทัด 23–24: จำนวนรอบ (15) และอ็อบเจ็กต์ความชอบ
บรรทัด 27–29  สัดส่วนหมวดที่ชอบ
27  def share(routes):
28      a = [p for day in routes for p in day if p['category'] != 'restaurant']
29      return (sum(p['category'] in LIKE for p in a) / len(a)) if a else 0.0
บรรทัด 27–29: share สัดส่วนสถานที่ท่องเที่ยวที่อยู่ในหมวดที่ชอบของแผน
บรรทัด 32–50  รันหนึ่งจังหวัดต่อหนึ่งค่า `LIKE_BOOST`
32  def run(prov, boost):
33      d = api.DATA[prov]; pv = api.PROVINCES[prov]
34      set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
35      hs = sorted(d['hotels'], key=lambda h: h['cost']); hotel = hs[int(len(hs) * SC['hotel_frac'])]
36      act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
37      api.LIKE_BOOST = boost
38      base, like = [], []
39      for t in range(TRIALS):
40          for pref, store in ((None, base), (PREF, like)):
41              pool, _ = api.apply_preferences(d['pois'], pref, SC['days'])
42              random.seed(t)
43              r, _ = hybrid_solve(pool, hotel, SC['days'], act, scoring_mode=SC['mode'], diversity_weight=api.DIVERSITY_WEIGHT, **HY)
44              r = api.restore_originals(r, d['poi_by_id'])
45              store.append(share(r))
46      try:
47          p = st.wilcoxon(like, base, alternative='greater').pvalue
48      except ValueError:
49          p = float('nan')
50      return statistics.mean(base), statistics.mean(like), p
บรรทัด 32–38: run ตั้งโปรไฟล์เดินทาง เลือกโรงแรม คำนวณงบกิจกรรม และตั้งค่า api.LIKE_BOOST
บรรทัด 39–45: ทุกรอบ รันแบบไม่มีความชอบและแบบมีความชอบด้วย seed เดียวกัน ผ่าน apply_preferences และ restore_originals ของ backend แล้วเก็บสัดส่วน
บรรทัด 46–50: ทดสอบ Wilcoxon ทางเดียวว่าสัดส่วนเมื่อชอบสูงกว่าปกติหรือไม่ (ถ้าทุกค่าเท่ากันได้ค่า p ไม่นิยาม) คืนสัดส่วนเฉลี่ยทั้งสองแบบและค่า p
บรรทัด 53–67  วนทุกจังหวัดและบันทึกผล
53  res = {}
54  for prov in PROVS:
55      d = api.DATA[prov]
56      att = [p for p in d['pois'] if p['category'] != 'restaurant']
57      liked = [p for p in att if p['category'] in LIKE]
58      hs = sorted(d['hotels'], key=lambda h: h['cost']); hotel = hs[int(len(hs) * SC['hotel_frac'])]
59      km = lambda ps: statistics.mean(haversine_km(p['lat'], p['lng'], hotel['lat'], hotel['lng']) for p in ps)
60      res[prov] = {'attractions': len(att), 'liked': len(liked),
61                   'score_liked': round(statistics.mean(p['score'] for p in liked), 2), 'score_all': round(statistics.mean(p['score'] for p in att), 2),
62                   'km_liked': round(km(liked), 1), 'km_all': round(km(att), 1), 'boost': {}}
63      for b in (1.0, 3.0, 5.0):
64          base, like, p = run(prov, b)
65          res[prov]['boost'][str(b)] = {'base': round(base, 3), 'like': round(like, 3), 'p': None if p != p else round(p, 4)}
66      print(prov, json.dumps(res[prov], ensure_ascii=False), flush=True)
67  json.dump(res, open(os.path.join(OUT, 'preference_cause.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
บรรทัด 53–62: ต่อจังหวัด นับสถานที่ทั้งหมดและในหมวดที่ชอบ คะแนนเฉลี่ยของสถานที่ในหมวดที่ชอบเทียบทั้งหมด และระยะเฉลี่ยถึงโรงแรม
บรรทัด 63–66: รัน LIKE_BOOST 1.0 3.0 และ 5.0 แล้วพิมพ์ผล
บรรทัด 67: เขียน preference_cause.json

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/hybrid.py
algorithm/utils.py
backend/main.py