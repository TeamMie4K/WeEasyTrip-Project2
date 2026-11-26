<!-- converted from algorithm__pareto.py.docx -->

คู่มือโค้ด: algorithm/pareto.py
NSGA-II หลายวัตถุประสงค์ (Pareto front)
ไฟล์ต้นฉบับ: algorithm/pareto.py (175 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สร้างชุดแผนทางเลือกที่ "ไม่มีแผนใดดีกว่าทุกด้าน" ตามวัตถุประสงค์ 3 ข้อ คือคะแนนรวม (มากสุด) ความหลากหลายของหมวดต่อวัน (มากสุด) และระยะขับรวม (น้อยสุด) ให้ผู้ใช้เลือก trade-off เอง ยืมตัวดำเนินการ GA และตัวซ่อมแผนจาก ➜ algorithm/hybrid.py เริ่มประชากรด้วย ➜ greedy_solve() ใน algorithm/greedy.py และตรวจแผนด้วย ➜ evaluate_route() ใน algorithm/utils.py ถูกเรียกจาก ➜ backend/main.py และ ➜ experiments/run_pareto_experiments.py

บรรทัด 1–20  หัวไฟล์และการนำเข้า
1  # -*- coding: utf-8 -*-
2  """
3  pareto.py - Multi-objective optimization (NSGA-II) สำหรับ B-TOPTW
4
5  วัตถุประสงค์ 3 ข้อ (ผู้ใช้เลือก trade-off เองจาก Pareto front):
6    1) total score            (มากที่สุด)
7    2) ความหลากหลาย            (จำนวนหมวด attraction ที่ต่างกันเฉลี่ยต่อวัน — มากที่สุด)
8    3) ระยะทางรวม (km)         (น้อยที่สุด)
9  ข้อจำกัด (งบ, เวลา, เวลาปิด, มื้ออาหาร 2 มื้อต่อวัน) จัดการด้วย constraint-domination ของ Deb:
10    คำตอบที่ผ่านข้อจำกัดชนะคำตอบที่ไม่ผ่านเสมอ; ถ้าไม่ผ่านทั้งคู่ เทียบค่าความละเมิดรวม
11  ผลลัพธ์สุดท้ายผ่าน meal_fill / 2-opt / ซ่อมเวลาและงบ แล้วกรองให้เหลือเฉพาะ front ที่ผ่านข้อจำกัด
12  """
13  import copy
14  import random
15  from typing import Dict, List
16
17  from utils import evaluate_route, DAY_TIME_BUDGET
18  from greedy import greedy_solve
19  from hybrid import (_crossover, _mutate, two_opt_day, meal_fill,
20                      _time_repair, diversity_stats)
บรรทัด 1–12: docstring อธิบายวัตถุประสงค์ 3 ข้อ การจัดการข้อจำกัดด้วย constraint-domination ของ Deb (คำตอบที่ผ่านชนะคำตอบที่ไม่ผ่านเสมอ ถ้าไม่ผ่านทั้งคู่เทียบค่าความละเมิดรวม) และขั้นสุดท้ายที่ซ่อมแผนแล้วกรอง front
บรรทัด 13–15: นำเข้า copy random และ type hint
บรรทัด 17: นำเข้า ➜ evaluate_route() ใน algorithm/utils.py และเพดานเวลาต่อวัน
บรรทัด 18: นำเข้า ➜ greedy_solve() ใน algorithm/greedy.py
บรรทัด 19–20: นำเข้าตัวดำเนินการและตัวซ่อมจาก ➜ algorithm/hybrid.py: _crossover _mutate two_opt_day meal_fill _time_repair และ diversity_stats
บรรทัด 23–40  วัดวัตถุประสงค์และค่าความละเมิด
23  def evaluate_objectives(routes: List[List[Dict]], hotel: Dict, budget: float) -> Dict:
24      """คืน objectives (ยิ่งน้อยยิ่งดีทุกตัว) + ค่าความละเมิดข้อจำกัด (0 = ผ่าน) + ค่าดิบสำหรับแสดงผล"""
25      ev = evaluate_route(routes, hotel, float('inf'))
26      div, _ = diversity_stats(routes)
27      dist = sum(d['distance_km'] for d in ev['days_detail'])
28      # งบประมาณนับเฉพาะค่าเข้า+ค่าอาหาร (ต่อคน) ตรงกับ _trim_to_budget — ค่าเดินทางถือเป็น overhead ไม่นับในงบกิจกรรม
29      poi_cost = sum(p['cost'] for day in routes for p in day)
30      viol = float(len(ev['violations']))
31      if poi_cost > budget:
32          viol += (poi_cost - budget) / max(budget, 1.0) * 10.0
33      for d in ev['days_detail']:
34          if d['time_min'] > DAY_TIME_BUDGET:
35              viol += (d['time_min'] - DAY_TIME_BUDGET) / 60.0
36      for day in routes:
37          if day and sum(1 for p in day if p['category'] == 'restaurant') < 2:
38              viol += 1.0
39      return {'obj': (-ev['total_score'], -div, dist), 'viol': viol, 'score': ev['total_score'],
40              'diversity': div, 'distance_km': dist, 'cost': poi_cost, 'valid': viol == 0}
บรรทัด 23–24: ประกาศ evaluate_objectives คืนวัตถุประสงค์ (ยิ่งน้อยยิ่งดีทุกตัว) ค่าความละเมิดข้อจำกัด (0 = ผ่าน) และค่าดิบ
บรรทัด 25: ประเมินแผนโดยตั้งงบเป็นอนันต์ เพื่อแยกคำนวณงบเอง
บรรทัด 26: ความหลากหลายเฉลี่ยจาก ➜ diversity_stats() ใน algorithm/hybrid.py
บรรทัด 27: ระยะขับรวมทุกวัน
บรรทัด 28–29: ค่าใช้จ่ายนับเฉพาะค่าเข้าและค่าอาหาร (ตรงกับนิยามงบของระบบ)
บรรทัด 30: เริ่มค่าความละเมิดจากจำนวนข้อความผิดข้อจำกัด
บรรทัด 31–32: ถ้าเกินงบ เพิ่มความละเมิดตามสัดส่วนส่วนเกิน × 10
บรรทัด 33–35: ถ้าวันใดใช้เวลาเกิน เพิ่มความละเมิดตามชั่วโมงที่เกิน
บรรทัด 36–38: ถ้าวันใดมีร้านอาหารน้อยกว่า 2 ร้าน เพิ่มความละเมิด 1
บรรทัด 39–40: คืน dict: obj = (−คะแนน, −ความหลากหลาย, ระยะ) เพื่อให้ทุกตัวเป็นแบบยิ่งน้อยยิ่งดี และค่าอื่น ๆ พร้อมธง valid
บรรทัด 43–55  ความ "ชนะ" แบบ constraint-domination
43  def _dominates(a: Dict, b: Dict) -> bool:
44      """a constraint-dominates b"""
45      if a['viol'] == 0 and b['viol'] > 0:
46          return True
47      if a['viol'] > 0:
48          return b['viol'] > 0 and a['viol'] < b['viol']
49      better = False
50      for x, y in zip(a['obj'], b['obj']):
51          if x > y:
52              return False
53          if x < y:
54              better = True
55      return better
บรรทัด 43–44: ประกาศ _dominates ว่า a ชนะ b หรือไม่
บรรทัด 45–46: ถ้า a ผ่านข้อจำกัดแต่ b ไม่ผ่าน a ชนะ
บรรทัด 47–48: ถ้า a ไม่ผ่าน ชนะได้เฉพาะเมื่อ b ก็ไม่ผ่านและ a ละเมิดน้อยกว่า
บรรทัด 49–55: ถ้าทั้งคู่ผ่าน a ชนะเมื่อไม่แย่กว่าในทุกวัตถุประสงค์ และดีกว่าอย่างน้อยหนึ่งข้อ
บรรทัด 58–83  จัดอันดับแบบไม่ถูกครอบงำ
58  def _nondominated_sort(evals: List[Dict]) -> List[List[int]]:
59      n = len(evals)
60      dominated_by = [[] for _ in range(n)]
61      count = [0] * n
62      fronts = [[]]
63      for i in range(n):
64          for j in range(n):
65              if i == j:
66                  continue
67              if _dominates(evals[i], evals[j]):
68                  dominated_by[i].append(j)
69              elif _dominates(evals[j], evals[i]):
70                  count[i] += 1
71          if count[i] == 0:
72              fronts[0].append(i)
73      k = 0
74      while fronts[k]:
75          nxt = []
76          for i in fronts[k]:
77              for j in dominated_by[i]:
78                  count[j] -= 1
79                  if count[j] == 0:
80                      nxt.append(j)
81          k += 1
82          fronts.append(nxt)
83      return fronts[:-1]
บรรทัด 58–62: ประกาศ _nondominated_sort เตรียมรายการ "ใครถูกครอบงำโดยใคร" ตัวนับ และ front แรก
บรรทัด 63–72: เทียบทุกคู่: ถ้า i ชนะ j เก็บ j ไว้ในรายการของ i ถ้า j ชนะ i เพิ่มตัวนับของ i ตัวที่ไม่มีใครชนะเข้า front แรก
บรรทัด 73–82: สร้าง front ถัดไปโดยลดตัวนับของตัวที่ถูกครอบงำ ตัวที่ตัวนับเป็น 0 ย้ายเข้า front ใหม่
บรรทัด 83: คืนทุก front ยกเว้นอันสุดท้ายที่ว่าง
บรรทัด 86–98  ระยะแออัด (crowding distance)
86  def _crowding(front: List[int], evals: List[Dict]) -> Dict[int, float]:
87      dist = {i: 0.0 for i in front}
88      if len(front) <= 2:
89          return {i: float('inf') for i in front}
90      for m in range(3):
91          order = sorted(front, key=lambda i: evals[i]['obj'][m])
92          lo, hi = evals[order[0]]['obj'][m], evals[order[-1]]['obj'][m]
93          dist[order[0]] = dist[order[-1]] = float('inf')
94          if hi - lo < 1e-12:
95              continue
96          for a in range(1, len(order) - 1):
97              dist[order[a]] += (evals[order[a + 1]]['obj'][m] - evals[order[a - 1]]['obj'][m]) / (hi - lo)
98      return dist
บรรทัด 86–89: ประกาศ _crowding ถ้า front มี 2 ตัวหรือน้อยกว่า ให้ค่าอนันต์ (ต้องเก็บไว้)
บรรทัด 90–93: วนทีละวัตถุประสงค์ เรียงตามค่า แล้วให้จุดสุดขอบทั้งสองข้างได้ค่าอนันต์
บรรทัด 94–95: ถ้าช่วงค่าเท่ากันหมด ข้ามวัตถุประสงค์นี้
บรรทัด 96–97: จุดตรงกลางสะสมระยะห่างระหว่างเพื่อนบ้านที่ปรับสเกลแล้ว
บรรทัด 98: คืนระยะแออัดของทุกตัว (ยิ่งมากยิ่งอยู่ในที่โล่ง ควรเก็บไว้เพื่อกระจายคำตอบ)
บรรทัด 101–114  ซ่อมขั้นสุดท้ายของแต่ละคำตอบ
101  def _repair_final(routes, pois, hotel, budget, scoring_mode):
102      """ขั้นสุดท้ายของแต่ละคำตอบใน front: 2-opt, เติมมื้อ, ซ่อมเวลา/งบ (ลำดับเดียวกับ Hybrid)"""
103      r = [two_opt_day(day, hotel) for day in routes]
104      r = meal_fill(r, pois, hotel, budget, scoring_mode)
105      r = _time_repair(r, hotel)
106      for _ in range(60):   # ซ่อมงบ (เฉพาะค่าเข้า+ค่าอาหาร): ลบ attraction ที่แพงที่สุดจนอยู่ในงบ
107          if sum(p['cost'] for day in r for p in day) <= budget:
108              break
109          cands = [(d, i, p) for d, day in enumerate(r) for i, p in enumerate(day) if p['category'] != 'restaurant']
110          if not cands:
111              break
112          d, i, _p = max(cands, key=lambda c: (c[2]['cost'], -c[2]['score']))
113          r[d] = [p for j, p in enumerate(r[d]) if j != i]
114      return meal_fill(r, pois, hotel, budget, scoring_mode)
บรรทัด 101–102: ประกาศ _repair_final ซ่อมคำตอบบน front ด้วยลำดับเดียวกับ Hybrid
บรรทัด 103: ปรับลำดับรายวันด้วย two_opt_day
บรรทัด 104: เติมมื้อด้วย meal_fill
บรรทัด 105: ซ่อมเวลาด้วย _time_repair
บรรทัด 106–113: ซ่อมงบ (เฉพาะค่าเข้า+ค่าอาหาร) วนไม่เกิน 60 รอบ ลบที่เที่ยวที่แพงที่สุด (ถ้าราคาเท่ากันลบคะแนนต่ำก่อน) จนอยู่ในงบ
บรรทัด 114: เติมมื้อซ้ำอีกครั้งแล้วคืนผล
บรรทัด 117–128  `nsga2_solve`: ประชากรเริ่มต้น
117  def nsga2_solve(pois: List[Dict], hotel: Dict, days: int, budget: float, scoring_mode: str = 'quality',
118                  pop_size: int = 40, generations: int = 40, mutation_rate: float = 0.5,
119                  seeds: List[List[List[Dict]]] = None) -> List[Dict]:
120      """คืนรายการคำตอบบน Pareto front (ผ่านข้อจำกัด) เรียงตามคะแนนมากไปน้อย
121      แต่ละรายการ: {'routes', 'score', 'diversity', 'distance_km', 'cost'}"""
122      pop = [copy.deepcopy(s) for s in (seeds or [])]
123      while len(pop) < pop_size:   # ประชากรเริ่มต้น: greedy หลายแบบ (สุ่มสลับลำดับ + noise ต่างกันเพื่อกระจายคำตอบ)
124          shuffled = list(pois)
125          random.shuffle(shuffled)
126          pop.append(greedy_solve(shuffled, hotel, days, budget, scoring_mode=random.choice(['ratio', 'quality']),
127                                  random_factor=random.choice([0.05, 0.15, 0.4])))
128      evals = [evaluate_objectives(c, hotel, budget) for c in pop]
บรรทัด 117–121: ประกาศ nsga2_solve (ประชากร 40 รุ่น 40 อัตรากลายพันธุ์ 0.5) docstring: คืนคำตอบบน Pareto front ที่ผ่านข้อจำกัด เรียงตามคะแนน
บรรทัด 122: นำ seed ที่ส่งมาเข้าประชากร (เช่น แผนจาก Hybrid)
บรรทัด 123–127: เติมประชากรด้วย greedy หลายแบบ สุ่มสลับลำดับ สุ่มโหมดคะแนน (ratio หรือ quality) และ noise (0.05, 0.15, 0.4) เพื่อกระจายคำตอบ
บรรทัด 128: ประเมินวัตถุประสงค์ของทุกตัว
บรรทัด 130–159  ลูปวิวัฒนาการของ NSGA-II
130      for _ in range(generations):
131          fronts = _nondominated_sort(evals)
132          rank, crowd = {}, {}
133          for r, f in enumerate(fronts):
134              c = _crowding(f, evals)
135              for i in f:
136                  rank[i], crowd[i] = r, c[i]
137
138          def pick():
139              a, b = random.sample(range(len(pop)), 2)
140              return a if (rank[a], -crowd[a]) < (rank[b], -crowd[b]) else b
141
142          children = []
143          while len(children) < pop_size:
144              child = _crossover(pop[pick()], pop[pick()])
145              child = _mutate(child, pois, mutation_rate)
146              children.append(child)
147          cevals = [evaluate_objectives(c, hotel, budget) for c in children]
148          allpop, allev = pop + children, evals + cevals
149          fronts = _nondominated_sort(allev)
150          nxt = []
151          for f in fronts:
152              if len(nxt) + len(f) <= pop_size:
153                  nxt += f
154              else:
155                  c = _crowding(f, allev)
156                  nxt += sorted(f, key=lambda i: -c[i])[:pop_size - len(nxt)]
157                  break
158          pop = [allpop[i] for i in nxt]
159          evals = [allev[i] for i in nxt]
บรรทัด 130: วนตามจำนวนรุ่น
บรรทัด 131: จัดอันดับ front ของประชากรปัจจุบัน
บรรทัด 132–136: คำนวณอันดับ (rank) และระยะแออัดของแต่ละตัว
บรรทัด 138–140: ฟังก์ชัน pick เลือกพ่อแม่แบบ binary tournament: เลือก rank ดีกว่า ถ้าเท่ากันเลือกตัวที่แออัดน้อยกว่า
บรรทัด 142–146: สร้างลูกจนครบ: _crossover และ _mutate จาก ➜ algorithm/hybrid.py
บรรทัด 147: ประเมินลูก
บรรทัด 148: รวมพ่อแม่กับลูก
บรรทัด 149: จัดอันดับ front ของประชากรรวม
บรรทัด 150–157: คัด front ทีละชั้นจนเต็มขนาดประชากร ถ้า front ใดล้น เลือกตัวที่ระยะแออัดมากสุดมาเติม
บรรทัด 158–159: ตั้งประชากรและค่าประเมินของรุ่นใหม่
บรรทัด 161–175  สรุปคำตอบบน front
161      front0 = _nondominated_sort(evals)[0]
162      out = []
163      for i in front0:
164          routes = _repair_final(pop[i], pois, hotel, budget, scoring_mode)
165          e = evaluate_objectives(routes, hotel, budget)
166          if e['valid']:
167              out.append({'routes': routes, 'score': e['score'], 'diversity': e['diversity'],
168                          'distance_km': e['distance_km'], 'cost': e['cost'], 'obj': e['obj'], 'viol': 0.0})
169      # กรองซ้ำและเหลือเฉพาะ non-dominated หลังซ่อม
170      keep = []
171      for a in out:
172          if not any(_dominates(b, a) for b in out if b is not a):
173              if not any(abs(a['score'] - k['score']) < 1e-9 and abs(a['distance_km'] - k['distance_km']) < 1e-6 and abs(a['diversity'] - k['diversity']) < 1e-9 for k in keep):
174                  keep.append(a)
175      return sorted(keep, key=lambda s: -s['score'])
บรรทัด 161: เอา front แรกของรุ่นสุดท้าย
บรรทัด 162–168: ซ่อมแต่ละคำตอบด้วย _repair_final ประเมินใหม่ เก็บเฉพาะที่ผ่านข้อจำกัด
บรรทัด 169–174: กรองให้เหลือเฉพาะคำตอบที่ไม่ถูกครอบงำหลังซ่อม และตัดคำตอบที่ซ้ำกันทุกค่า
บรรทัด 175: คืนรายการเรียงตามคะแนนมากไปน้อย

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/greedy.py
algorithm/hybrid.py
algorithm/utils.py
backend/main.py
experiments/run_pareto_experiments.py