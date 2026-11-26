<!-- converted from algorithm__hybrid.py.docx -->

คู่มือโค้ด: algorithm/hybrid.py
Hybrid Algorithm: Greedy seed + GA + 2-opt + ซ่อมแผน + ILS
ไฟล์ต้นฉบับ: algorithm/hybrid.py (753 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: อัลกอริทึมหลักของโครงงาน ขั้นตอนคือ (1) สร้าง seed ด้วย ➜ greedy_solve() ใน algorithm/greedy.py (2) วิวัฒนาการด้วย GA แบบรักษารูปแบบช่อง (slot) (3) ปรับลำดับในวันด้วย 2-opt (4) เติมมื้อด้วย meal_fill (5) ซ่อมเวลาและงบ (6) ปรับปรุงด้วย Insertion Local Search ใน ➜ algorithm/ils.py ใช้ตัวตรวจแผนจาก ➜ evaluate_route() ใน algorithm/utils.py และถูกเรียกจาก ➜ backend/main.py และสคริปต์ทดลองใน experiments/

บรรทัด 1–20  หัวไฟล์และการนำเข้า
1  ﻿# -*- coding: utf-8 -*-
2  """
3  hybrid.py - Hybrid Algorithm: Greedy seed + GA refinement + 2-opt local search
4
5  Workflow:
6    1) Greedy slot-based → ได้ initial solution ที่ใช้งานได้ทันที
7    2) GA refinement → ลองสับเปลี่ยน POIs ระหว่างวันเพื่อหา global optima
8    3) 2-opt local search → ปรับลำดับ attractions ในแต่ละวันให้ travel distance น้อยสุด
9
10  ออกแบบให้รักษา slot pattern (slot 3 = lunch, slot 6 = dinner) ตลอดกระบวนการ
11  """
12  import random
13  import copy
14  import time
15  import utils
16  from typing import List, Dict, Tuple
17  from utils import (split_attrs, MAX_ATTRS, haversine_km, travel_time_min, travel_cost,
18                     evaluate_route, DAY_TIME_BUDGET, DAY_START_MIN)
19  from greedy import (greedy_solve, _find_best_for_slot,
20                      LUNCH_TRIGGER, DINNER_TRIGGER)
บรรทัด 1–11: docstring สรุปขั้นตอนทั้งสามของ Hybrid และเน้นว่ารักษารูปแบบช่อง (ช่อง 3 = มื้อกลางวัน ช่อง 6 = มื้อเย็น)
บรรทัด 12–14: นำเข้า random copy time
บรรทัด 15: นำเข้า utils ทั้งโมดูล (ใช้อ้าง utils.TIME_WEIGHT ที่บรรทัด 252)
บรรทัด 16: นำเข้า type hint
บรรทัด 17–18: นำเข้าจาก ➜ algorithm/utils.py ได้แก่ ตัวแบ่งช่วง split_attrs จำนวนที่เที่ยวสูงสุด MAX_ATTRS ฟังก์ชันระยะทาง/เวลา/ค่าเดินทาง evaluate_route และค่าคงที่เวลา
บรรทัด 19–20: นำเข้าจาก ➜ algorithm/greedy.py ได้แก่ greedy_solve ตัวเลือกจุดต่อช่อง _find_best_for_slot และเวลาตั้งต้นของมื้อกลางวัน/เย็น
บรรทัด 26–35  ระยะทางของเส้นทางหนึ่งวัน
26  def _route_distance(day_pois: List[Dict], hotel: Dict) -> float:
27      """ระยะทางรวมของเส้นทางใน 1 วัน (โรงแรม → POIs → โรงแรม)"""
28      if not day_pois:
29          return 0.0
30      path = [hotel] + day_pois + [hotel]
31      total = 0.0
32      for i in range(len(path) - 1):
33          total += haversine_km(path[i]['lat'], path[i]['lng'],
34                                path[i + 1]['lat'], path[i + 1]['lng'])
35      return total
บรรทัด 26: ประกาศ _route_distance
บรรทัด 27: docstring: ระยะรวมโรงแรม → จุดทั้งหมด → โรงแรม
บรรทัด 28–29: ถ้าวันว่าง คืน 0
บรรทัด 30: สร้างเส้นทางเต็มรวมโรงแรมหัวท้าย
บรรทัด 31: ตัวสะสมระยะ
บรรทัด 32–34: บวกระยะแต่ละช่วงด้วย haversine_km จาก ➜ haversine_km() ใน algorithm/utils.py
บรรทัด 35: คืนระยะรวม
บรรทัด 38–80  2-opt ภายในวัน
38  def two_opt_day(day_pois: List[Dict], hotel: Dict) -> List[Dict]:
39      """2-opt swap optimization within a day.
40      รักษาตำแหน่ง slot 3 (lunch) และ slot 6 (dinner) ไว้
41      Only accepts swaps that don't create time-window violations.
42      """
43      n = len(day_pois)
44      if n < 3:
45          return day_pois
46
47      # หา positions ที่เป็น restaurant - ห้ามขยับ
48      fixed_positions = set()
49      for idx, p in enumerate(day_pois):
50          if p['category'] == 'restaurant':
51              fixed_positions.add(idx)
52
53      current = list(day_pois)
54      current_dist = _route_distance(current, hotel)
55      improved = True
56      iters = 0
57      while improved and iters < 50:
58          improved = False
59          iters += 1
60          for i in range(n - 1):
61              if i in fixed_positions:
62                  continue
63              for j in range(i + 1, n):
64                  if j in fixed_positions:
65                      continue
66                  # ลอง swap ตำแหน่ง i และ j
67                  trial = list(current)
68                  trial[i], trial[j] = trial[j], trial[i]
69                  trial_dist = _route_distance(trial, hotel)
70                  if trial_dist < current_dist - 0.01:
71                      # ตรวจสอบ: ไม่มี time violation หลัง swap
72                      ev = evaluate_route([trial], hotel, float('inf'))
73                      if ev['valid']:
74                          current = trial
75                          current_dist = trial_dist
76                          improved = True
77                          break
78              if improved:
79                  break
80      return current
บรรทัด 38: ประกาศ two_opt_day รับจุดของวันและโรงแรม
บรรทัด 39–42: docstring: สลับตำแหน่งเพื่อลดระยะ โดยไม่ขยับร้านอาหาร และรับเฉพาะการสลับที่ไม่ทำให้เวลาผิดข้อจำกัด
บรรทัด 43–45: ถ้าจุดน้อยกว่า 3 ไม่ต้องปรับ
บรรทัด 47–51: จดตำแหน่งที่เป็นร้านอาหารไว้ใน fixed_positions (ห้ามขยับ)
บรรทัด 53–54: เริ่มจากลำดับปัจจุบันและระยะเดิม
บรรทัด 55–56: ธงว่ามีการปรับปรุงและตัวนับรอบ
บรรทัด 57–59: วนต่อตราบที่ยังปรับปรุงได้และไม่เกิน 50 รอบ
บรรทัด 60–65: วนทุกคู่ตำแหน่ง (i, j) ที่ไม่ใช่ร้านอาหาร
บรรทัด 67–69: ลองสลับ i กับ j แล้วคำนวณระยะใหม่
บรรทัด 70: รับเมื่อระยะสั้นลงเกิน 0.01 กม.
บรรทัด 72–73: ตรวจด้วย ➜ evaluate_route() ใน algorithm/utils.py ว่ายัง valid (ไม่มีผิดเวลา)
บรรทัด 74–77: ถ้าผ่าน ยอมรับลำดับใหม่ ตั้งธง และเริ่มรอบใหม่ทันที (break)
บรรทัด 78–79: ออกจากลูปนอกเพื่อเริ่มสแกนใหม่เมื่อมีการปรับปรุง
บรรทัด 80: คืนลำดับที่ดีที่สุด
บรรทัด 86–117  ซ่อมรูปแบบช่อง
86  def _slot_repair(chromosome: List[List[Dict]]) -> List[List[Dict]]:
87      """แก้ chromosome ให้ตรงรูปแบบ slot:
88         attractions ใน slots 1,2,4,5  +  restaurants ใน slots 3,6
89         ถ้าไม่มี restaurant ในวัน → leave gap (skip slot)
90      """
91      repaired = []
92      for day in chromosome:
93          attrs = [p for p in day if p['category'] != 'restaurant']
94          rests = [p for p in day if p['category'] == 'restaurant']
95
96          # จำกัด attractions สูงสุด MAX_ATTRS / restaurants สูงสุด 2; แบ่งเช้า/บ่ายตามเวลาที่ใช้จริง
97          attrs = attrs[:MAX_ATTRS]
98          rests = rests[:2]
99          morning, afternoon, evening = split_attrs(attrs)
100          new_day = list(morning)
101          if len(rests) >= 1:
102              new_day.append(rests[0])          # มื้อกลางวัน
103          new_day.extend(afternoon)
104          if len(rests) >= 2:
105              new_day.append(rests[1])          # มื้อเย็น
106          new_day.extend(evening)               # จุดที่เปิดค่ำ (โชว์/ตลาดกลางคืน) หลังมื้อเย็น
107          repaired.append(new_day)
108
109      # ลบ POI ที่ซ้ำข้ามวัน
110      seen = set()
111      final = [[] for _ in repaired]
112      for d, day in enumerate(repaired):
113          for poi in day:
114              if poi['id'] not in seen:
115                  seen.add(poi['id'])
116                  final[d].append(poi)
117      return final
บรรทัด 86: ประกาศ _slot_repair
บรรทัด 87–90: docstring: ให้เป็นรูปแบบ ที่เที่ยวช่อง 1,2,4,5 + ร้านอาหารช่อง 3,6
บรรทัด 91: รายการแผนที่ซ่อมแล้ว
บรรทัด 92: วนทีละวัน
บรรทัด 93–94: แยกที่เที่ยวกับร้านอาหารของวัน
บรรทัด 96–98: จำกัดที่เที่ยวไม่เกิน MAX_ATTRS (4) และร้านอาหารไม่เกิน 2
บรรทัด 99: แบ่งที่เที่ยวเป็นเช้า บ่าย ค่ำด้วย ➜ split_attrs() ใน algorithm/utils.py
บรรทัด 100: เริ่มวันด้วยช่วงเช้า
บรรทัด 101–102: ถ้ามีร้านอย่างน้อยหนึ่งร้าน ใส่เป็นมื้อกลางวัน
บรรทัด 103: ต่อด้วยช่วงบ่าย
บรรทัด 104–105: ถ้ามีสองร้าน ใส่ร้านที่สองเป็นมื้อเย็น
บรรทัด 106: ปิดท้ายด้วยจุดที่เปิดค่ำ (หลังมื้อเย็น)
บรรทัด 107: เก็บวันนี้
บรรทัด 109–117: ลบจุดซ้ำข้ามวันโดยเก็บจุดที่เจอก่อน แล้วคืนแผน
บรรทัด 120–129  Crossover ระดับวัน
120  def _crossover(p1: List[List[Dict]], p2: List[List[Dict]]) -> List[List[Dict]]:
121      """Day-level crossover: แต่ละวันสุ่มรับจาก p1 หรือ p2 แล้ว slot_repair"""
122      days = len(p1)
123      child = []
124      for d in range(days):
125          if random.random() < 0.5:
126              child.append([dict(x) for x in p1[d]])
127          else:
128              child.append([dict(x) for x in p2[d]])
129      return _slot_repair(child)
บรรทัด 120: ประกาศ _crossover
บรรทัด 121: docstring
บรรทัด 122–128: ทุกวัน สุ่ม 50% ว่าจะรับวันจากพ่อหรือแม่
บรรทัด 129: ซ่อมรูปแบบช่องหลังผสม
บรรทัด 132–185  Mutation แบบรู้จักช่อง
132  def _mutate(chromosome: List[List[Dict]], all_pois: List[Dict],
133              mutation_rate: float = 0.3) -> List[List[Dict]]:
134      """Mutation operators (slot-aware):
135         - swap_attr: swap attraction with unused
136         - swap_rest: swap restaurant with unused
137         - move_across_days: move POI from one day to another
138      """
139      if random.random() > mutation_rate:
140          return chromosome
141
142      used_ids = {p['id'] for day in chromosome for p in day}
143      unused_attrs = [p for p in all_pois if p['category'] != 'restaurant' and p['id'] not in used_ids]
144      unused_rests = [p for p in all_pois if p['category'] == 'restaurant' and p['id'] not in used_ids]
145
146      op = random.choice(['swap_attr', 'swap_rest', 'cross_day', 'remove'])
147
148      if op == 'swap_attr' and unused_attrs:
149          days_with_attr = [(d, [i for i, p in enumerate(chromosome[d])
150                                  if p['category'] != 'restaurant'])
151                            for d in range(len(chromosome))]
152          days_with_attr = [(d, idxs) for d, idxs in days_with_attr if idxs]
153          if days_with_attr:
154              d, idxs = random.choice(days_with_attr)
155              i = random.choice(idxs)
156              chromosome[d][i] = random.choice(unused_attrs)
157
158      elif op == 'swap_rest' and unused_rests:
159          days_with_rest = [(d, [i for i, p in enumerate(chromosome[d])
160                                  if p['category'] == 'restaurant'])
161                            for d in range(len(chromosome))]
162          days_with_rest = [(d, idxs) for d, idxs in days_with_rest if idxs]
163          if days_with_rest:
164              d, idxs = random.choice(days_with_rest)
165              i = random.choice(idxs)
166              chromosome[d][i] = random.choice(unused_rests)
167
168      elif op == 'cross_day' and len(chromosome) >= 2:
169          non_empty = [d for d in range(len(chromosome)) if chromosome[d]]
170          if len(non_empty) >= 2:
171              d1, d2 = random.sample(non_empty, 2)
172              i = random.randrange(len(chromosome[d1]))
173              j = random.randrange(len(chromosome[d2]))
174              # สลับเฉพาะ POI ประเภทเดียวกัน
175              if chromosome[d1][i]['category'] == chromosome[d2][j]['category']:
176                  chromosome[d1][i], chromosome[d2][j] = chromosome[d2][j], chromosome[d1][i]
177
178      elif op == 'remove':
179          non_empty = [d for d in range(len(chromosome)) if chromosome[d]]
180          if non_empty:
181              d = random.choice(non_empty)
182              i = random.randrange(len(chromosome[d]))
183              chromosome[d].pop(i)
184
185      return _slot_repair(chromosome)
บรรทัด 132–133: ประกาศ _mutate (อัตรา 0.3)
บรรทัด 134–138: docstring: สลับที่เที่ยว/ร้านอาหารกับจุดที่ยังไม่ใช้ และย้ายข้ามวัน
บรรทัด 139–140: สุ่มว่าจะกลายพันธุ์หรือไม่
บรรทัด 142–144: หาจุดที่ใช้แล้ว ที่เที่ยวที่ยังไม่ใช้ และร้านอาหารที่ยังไม่ใช้
บรรทัด 146: สุ่มตัวดำเนินการ
บรรทัด 148–156: swap_attr แทนที่เที่ยวหนึ่งจุดด้วยจุดที่ยังไม่ใช้
บรรทัด 158–166: swap_rest แทนร้านอาหารหนึ่งร้านด้วยร้านที่ยังไม่ใช้
บรรทัด 168–176: cross_day สลับจุดสองวัน เฉพาะเมื่อเป็นหมวดเดียวกัน
บรรทัด 178–183: remove ลบจุดสุ่มหนึ่งจุด
บรรทัด 185: ซ่อมรูปแบบช่องแล้วคืนแผน
บรรทัด 191–201  สถิติความหลากหลาย
191  def diversity_stats(chromosome: List[List[Dict]]) -> Tuple[float, int]:
192      """(จำนวนหมวด attraction ที่ต่างกันเฉลี่ยต่อวัน, จำนวนครั้งที่หมวดเดียวซ้ำเกิน 2 จุดต่อวัน)"""
193      distinct, over = [], 0
194      for day in chromosome:
195          cats = [p['category'] for p in day if p['category'] != 'restaurant']
196          if not cats:
197              continue
198          counts = {c: cats.count(c) for c in set(cats)}
199          distinct.append(len(counts))
200          over += sum(max(0, n - 2) for n in counts.values())
201      return (sum(distinct) / len(distinct) if distinct else 0.0), over
บรรทัด 191: ประกาศ diversity_stats
บรรทัด 192: docstring: คืนจำนวนหมวดต่างกันเฉลี่ยต่อวัน และจำนวนครั้งที่หมวดเดียวซ้ำเกิน 2 จุด/วัน ใช้ในการทดลองบทที่ 4
บรรทัด 193: ตัวสะสม
บรรทัด 194–197: วนทุกวัน เก็บหมวดของที่เที่ยว (ข้ามวันที่ไม่มีที่เที่ยว)
บรรทัด 198–199: นับจำนวนจุดต่อหมวด และเก็บจำนวนหมวดที่ต่างกัน
บรรทัด 200: สะสมส่วนที่ซ้ำเกิน 2
บรรทัด 201: คืนค่าเฉลี่ยและจำนวนส่วนเกิน
บรรทัด 204–254  ฟังก์ชัน fitness ของ Hybrid
204  DIST_WEIGHT = 0.3    # คะแนนที่หักต่อ km ที่ต้องขับ (แผนสมจริงขึ้น: ไม่ซิกแซกข้ามเกาะ/จังหวัด)
205
206
207  def _fitness(chromosome: List[List[Dict]], hotel: Dict, budget: float,
208               scoring_mode: str = 'ratio', diversity_weight: float = 0.0) -> float:
209      result = evaluate_route(chromosome, hotel, budget)
210      score = result['total_score']
211      penalty = 0.0
212
213      if result['total_cost'] > budget:
214          penalty += (result['total_cost'] - budget) * 0.03
215      for v in result['violations']:
216          if 'งบประมาณเกิน' in v: pass
217          elif 'ใช้เวลาเกิน' in v: penalty += 50.0
218          elif 'หลังเวลาปิด' in v or 'เกินช่วงมื้อ' in v: penalty += 25.0
219          elif 'เวลาท่องเที่ยวเกิน' in v: penalty += 50.0
220          else: penalty += 10.0
221
222      # Slot pattern bonus: reward valid 6-slot days
223      slot_bonus = 0.0
224      for day in chromosome:
225          n = len(day)
226          if n == 0:
227              continue
228          # ให้ bonus วันที่มีครบ 6 จุด
229          if n >= 6:
230              slot_bonus += 3.0
231          # ให้ bonus วันที่มีมื้ออาหาร
232          rests = [p for p in day if p['category'] == 'restaurant']
233          if len(rests) >= 1:
234              slot_bonus += 1.0
235          if len(rests) >= 2:
236              slot_bonus += 1.0
237          # penalize วันที่มีร้านอาหารมากเกิน
238          if len(rests) > 2:
239              penalty += (len(rests) - 2) * 5.0
240
241      if diversity_weight:
242          # หลายวัตถุประสงค์ (weighted-sum): score + ความหลากหลายของหมวดต่อวัน − การซ้ำหมวดเกิน 2 จุด/วัน
243          for day in chromosome:
244              cats = [p['category'] for p in day if p['category'] != 'restaurant']
245              if not cats:
246                  continue
247              counts = {c: cats.count(c) for c in set(cats)}
248              score += diversity_weight * (len(counts) - 1)
249              score -= diversity_weight * sum(max(0, n - 2) for n in counts.values())
250
251      penalty += 0.02 * sum(d.get('idle_min', 0) for d in result['days_detail'])   # เวลานั่งรอก่อนมื้อ
252      penalty += utils.TIME_WEIGHT * sum(d['time_min'] for d in result['days_detail'])   # เวลาทั้งวัน (เที่ยว+เดินทาง+มื้อ+รอ)
253      penalty += DIST_WEIGHT * sum(d['distance_km'] for d in result['days_detail'])      # ระยะขับรวม: ให้แผนจัดกลุ่มตามพื้นที่
254      return score + slot_bonus - penalty
บรรทัด 204: DIST_WEIGHT = 0.3 คะแนนที่หักต่อกิโลเมตรที่ขับ ทำให้แผนจัดกลุ่มตามพื้นที่ ค่านี้ถูกนำเข้าไปใช้ที่ ➜ fitness() ใน algorithm/genetic.py ด้วย และเป็นค่าเดียวกับ ➜ algorithm/ils.py
บรรทัด 207–208: ประกาศ _fitness รับแผน โรงแรม งบ โหมดคะแนน และน้ำหนักความหลากหลาย
บรรทัด 209–211: ประเมินแผน เริ่มที่คะแนนรวม และตั้งตัวสะสมโทษ
บรรทัด 213–214: ถ้าเกินงบ โทษ = ส่วนเกิน × 0.03
บรรทัด 215–220: โทษตามชนิดข้อผิด: ใช้เวลาเกิน 50, หลังเวลาปิดหรือเกินช่วงมื้อ 25, เวลาท่องเที่ยวเกิน 50, อื่น ๆ 10 (เกินงบไม่ซ้ำโทษ)
บรรทัด 222–239: โบนัสช่อง: วันที่มี 6 จุดขึ้นไป +3, มีร้าน 1 ร้าน +1, 2 ร้าน +1 อีก และโทษ 5 ต่อร้านที่เกิน 2
บรรทัด 241–249: ถ้ามีน้ำหนักความหลากหลาย (diversity_weight) เพิ่มคะแนน w × (จำนวนหมวดต่างกัน − 1) และหักการซ้ำหมวดเกิน 2 จุด
บรรทัด 251: โทษเวลารอก่อนมื้อ 0.02 ต่อนาที
บรรทัด 252: โทษเวลาทั้งวันด้วย utils.TIME_WEIGHT (0.01 ต่อนาที) จาก ➜ algorithm/utils.py
บรรทัด 253: โทษระยะขับรวม DIST_WEIGHT × กม.
บรรทัด 254: คืนคะแนน + โบนัสช่อง − โทษทั้งหมด
บรรทัด 260–288  `meal_fill`: เตรียมตัวแปรและกรณีมีมื้อครบ
260  def meal_fill(routes: List[List[Dict]], pois: List[Dict], hotel: Dict,
261                budget: float, scoring_mode: str = 'ratio') -> List[List[Dict]]:
262      """Post-process GA/Hybrid result: use greedy slot logic to insert
263      missing lunch and dinner into every day that lacks them.
264
265      GA controls attraction selection (better global search);
266      this ensures realistic meal slots are always present.
267      """
268      used_ids = {p['id'] for day in routes for p in day}
269      ev = evaluate_route(routes, hotel, budget)
270      remaining = max(0.0, budget - ev['total_cost'])
271
272      new_routes = []
273      for day_idx, day in enumerate(routes):
274          attrs  = [p for p in day if p['category'] != 'restaurant']
275          e_rest = [p for p in day if p['category'] == 'restaurant']
276
277          # มี lunch + dinner ครบแล้ว — จัดลำดับ slot เท่านั้น
278          if len(e_rest) >= 2:
279              mo, af, ev_ = split_attrs(attrs[:MAX_ATTRS])
280              new_day = mo + [e_rest[0]] + af + [e_rest[1]] + ev_
281              new_routes.append(new_day)
282              continue
283
284          # แบ่ง attractions เป็นช่วงเช้า (slots 1-2) และช่วงบ่าย (slots 4-5)
285          morning, afternoon, evening = split_attrs(attrs[:MAX_ATTRS])
286          days_left = max(1, len(routes) - day_idx)
287          day_bgt   = remaining / days_left
288          day_cats  = {}
บรรทัด 260–261: ประกาศ meal_fill รับแผน จุดทั้งหมด โรงแรม งบ
บรรทัด 262–267: docstring: ใช้ตรรกะช่องของ greedy ใส่มื้อกลางวัน/เย็นที่ขาดในทุกวัน GA ควบคุมการเลือกที่เที่ยว ส่วนฟังก์ชันนี้รับประกันมื้อ
บรรทัด 268: ชุด id จุดที่ใช้แล้ว
บรรทัด 269–270: ประเมินแผนและคำนวณงบคงเหลือ
บรรทัด 272: รายการแผนใหม่
บรรทัด 273: วนทีละวัน
บรรทัด 274–275: แยกที่เที่ยวกับร้านอาหารที่มีอยู่แล้ว
บรรทัด 277–282: ถ้ามีร้านครบ 2 ร้านแล้ว แค่จัดลำดับช่อง (เช้า มื้อกลางวัน บ่าย มื้อเย็น ค่ำ) แล้วข้ามวัน
บรรทัด 284–285: แบ่งที่เที่ยวเป็นเช้า บ่าย ค่ำ
บรรทัด 286–288: งบต่อวัน = งบคงเหลือ ÷ จำนวนวันที่เหลือ และตัวนับหมวด
บรรทัด 290–336  `meal_fill`: จำลองช่วงเช้าและหามื้อกลางวัน
290          # --- จำลองเวลาผ่าน attractions ช่วงเช้า ---
291          cur_t   = float(DAY_START_MIN)
292          cur_pos = hotel
293          for poi in morning:
294              d = haversine_km(cur_pos['lat'], cur_pos['lng'],
295                               poi['lat'], poi['lng'])
296              cur_t += travel_time_min(d)
297              if cur_t < poi['open_min']:
298                  cur_t = float(poi['open_min'])
299              cur_t += poi['duration_min']
300              cur_pos = poi
301              day_cats[poi['category']] = day_cats.get(poi['category'], 0) + 1
302              day_bgt -= travel_cost(d) + poi['cost']
303
304          # เลื่อนเวลาเข้าสู่ช่วง lunch
305          if cur_t < LUNCH_TRIGGER:
306              cur_t = float(LUNCH_TRIGGER)
307
308          # --- หาร้านอาหาร lunch ---
309          lunch = None
310          if e_rest:
311              # ใช้ restaurant ที่มีอยู่แล้วเป็น lunch
312              lunch = e_rest[0]
313              d = haversine_km(cur_pos['lat'], cur_pos['lng'],
314                               lunch['lat'], lunch['lng'])
315              cur_t = max(cur_t + travel_time_min(d), float(lunch['open_min']))
316              cur_t += lunch['duration_min']
317              cur_pos = lunch
318          else:
319              r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
320                                      DAY_TIME_BUDGET, day_bgt, day_cats,
321                                      'lunch', scoring_mode)
322              if r is None:   # มื้อเป็น hard requirement: ขยายงบและช่วงเวลาเข้าร้าน
323                  r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
324                                          DAY_TIME_BUDGET, 1e9, day_cats,
325                                          'lunch', scoring_mode, relax_meal=True)
326              if r:
327                  lunch, d_l, arr_l = r
328                  used_ids.add(lunch['id'])
329                  cost_l = travel_cost(d_l) + lunch['cost']
330                  day_bgt   -= cost_l
331                  remaining -= cost_l
332                  cur_t      = arr_l + lunch['duration_min']
333                  cur_pos    = lunch
334
335          if lunch:
336              day_cats['restaurant'] = day_cats.get('restaurant', 0) + 1
บรรทัด 290–302: จำลองเวลาเดินผ่านที่เที่ยวช่วงเช้า: เดินทาง รอเปิด อยู่ที่จุด เลื่อนตำแหน่ง นับหมวด หักงบ
บรรทัด 304–306: เลื่อนเวลาเข้าช่วงมื้อกลางวัน (ถึง 11:30 ถ้ายังไม่ถึง)
บรรทัด 308–312: ถ้ามีร้านอยู่แล้ว ใช้เป็นมื้อกลางวัน
บรรทัด 313–317: คำนวณเดินทางไปร้านและเวลาที่เสร็จมื้อ
บรรทัด 318–321: ถ้ายังไม่มีร้าน เรียก ➜ _find_best_for_slot() ใน algorithm/greedy.py หาร้านมื้อกลางวันที่ดีที่สุด
บรรทัด 322–325: ถ้าหาไม่ได้ ขยายงบเป็นไม่จำกัดและผ่อนช่วงเวลา (มื้อเป็นข้อบังคับ)
บรรทัด 326–333: ถ้าได้ร้าน บันทึกว่าใช้แล้ว หักงบ และเลื่อนเวลา/ตำแหน่ง
บรรทัด 335–336: นับหมวดร้านอาหารของวันนี้
บรรทัด 338–378  `meal_fill`: จำลองช่วงบ่ายและหามื้อเย็น
338          # --- จำลองเวลาผ่าน attractions ช่วงบ่าย ---
339          for poi in afternoon:
340              d = haversine_km(cur_pos['lat'], cur_pos['lng'],
341                               poi['lat'], poi['lng'])
342              cur_t += travel_time_min(d)
343              if cur_t < poi['open_min']:
344                  cur_t = float(poi['open_min'])
345              cur_t += poi['duration_min']
346              cur_pos = poi
347              day_cats[poi['category']] = day_cats.get(poi['category'], 0) + 1
348              day_bgt -= travel_cost(d) + poi['cost']
349
350          # เลื่อนเวลาเข้าสู่ช่วง dinner
351          if cur_t < DINNER_TRIGGER:
352              cur_t = float(DINNER_TRIGGER)
353
354          # --- หาร้านอาหาร dinner ---
355          dinner = None
356          r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
357                                  DAY_TIME_BUDGET, day_bgt, day_cats,
358                                  'dinner', scoring_mode)
359          if r is None:
360              # Fallback: ขยายงบ — dinner เป็น hard requirement
361              meal_cap = max(500, budget * 0.08)
362              r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
363                                      DAY_TIME_BUDGET, meal_cap, day_cats,
364                                      'dinner', scoring_mode)
365          if r is None:
366              # Last resort: ร้านอาหารฟรีเท่านั้น
367              r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
368                                      DAY_TIME_BUDGET, 1e9, day_cats,
369                                      'dinner', scoring_mode, free_only=True)
370          if r is None:
371              r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
372                                      DAY_TIME_BUDGET, 1e9, day_cats,
373                                      'dinner', scoring_mode, relax_meal=True)
374          if r:
375              dinner, d_d, _ = r
376              used_ids.add(dinner['id'])
377              remaining -= travel_cost(d_d) + dinner['cost']
378
บรรทัด 338–348: จำลองผ่านที่เที่ยวช่วงบ่ายเหมือนช่วงเช้า
บรรทัด 350–352: เลื่อนเวลาเข้าช่วงมื้อเย็น (17:00)
บรรทัด 354–358: หาร้านมื้อเย็นด้วย _find_best_for_slot
บรรทัด 359–364: ถ้าหาไม่ได้ ขยายงบมื้อเป็น 500 บาทหรือ 8% ของงบ
บรรทัด 365–369: ถ้ายังไม่ได้ ลองเฉพาะร้านฟรี
บรรทัด 370–373: ถ้ายังไม่ได้ ผ่อนช่วงเวลาเข้าร้าน
บรรทัด 374–377: ถ้าได้ร้าน บันทึกว่าใช้แล้วและหักงบ
บรรทัด 379–387  ประกอบแผนของวันและคืนผล
379          # --- ประกอบ route ของวันตามลำดับ slot ---
380          new_day = list(morning)
381          if lunch:    new_day.append(lunch)
382          new_day.extend(afternoon)
383          if dinner:   new_day.append(dinner)
384          new_day.extend(evening)
385          new_routes.append(new_day)
386
387      return new_routes
บรรทัด 379–385: ประกอบวันตามลำดับช่อง: ที่เที่ยวช่วงเช้า → มื้อกลางวัน (ถ้ามี) → ช่วงบ่าย → มื้อเย็น (ถ้ามี) → จุดค่ำ แล้วเก็บเข้าแผน
บรรทัด 387: คืนแผนที่เติมมื้อแล้วของทุกวัน
บรรทัด 393–431  `_time_repair` ซ่อมเวลา
393  def _time_repair(routes: List[List[Dict]], hotel: Dict, protect=()) -> List[List[Dict]]:
394      """Remove violating non-restaurant POIs from days that:
395        (a) exceed DAY_TIME_BUDGET, or
396        (b) contain POIs visited after their closing time.
397      Preserves restaurant (meal) slots and POIs whose id is in `protect` (เลือกโดยผู้ใช้)."""
398      import re as _re
399      routes = [list(d) for d in routes]
400      for d_idx in range(len(routes)):
401          for _ in range(10):  # max 10 removals per day
402              ev = evaluate_route([routes[d_idx]], hotel, float('inf'))
403              day_viols = [v for v in ev['violations'] if f'Day 1:' in v]
404              time_ok = ev['days_detail'][0]['time_min'] <= DAY_TIME_BUDGET
405              if time_ok and not day_viols:
406                  break
407
408              # รวบรวม ID ของ POI ที่ไปถึงหลังเวลาปิด
409              late_ids = set()
410              for v in day_viols:
411                  if 'หลังเวลาปิด' in v:
412                      m = _re.search(r'ไปถึง (\S+) หลังเวลาปิด', v)
413                      if m:
414                          late_ids.add(m.group(1))
415
416              # Priority: ลบ POI ที่ไปถึงสายก่อน ถ้าไม่มีให้ลบ attr score ต่ำสุด
417              worst_i = None
418              if late_ids:
419                  for i, p in enumerate(routes[d_idx]):
420                      if p['id'] in late_ids and p['category'] != 'restaurant' and p['id'] not in protect:
421                          worst_i = i
422                          break
423              if worst_i is None:
424                  worst_score = float('inf')
425                  for i, p in enumerate(routes[d_idx]):
426                      if p['category'] != 'restaurant' and p['id'] not in protect and p['score'] < worst_score:
427                          worst_score = p['score']; worst_i = i
428              if worst_i is None:
429                  break
430              routes[d_idx].pop(worst_i)
431      return routes
บรรทัด 393: ประกาศ _time_repair มีพารามิเตอร์ protect คือ id ของจุดที่ผู้ใช้เลือกซึ่งห้ามลบ
บรรทัด 394–397: docstring: ลบที่เที่ยวที่ทำให้วันเกินเวลา หรือไปถึงหลังเวลาปิด โดยไม่แตะร้านอาหาร
บรรทัด 398: นำเข้า re ในชื่อ _re (ใช้ดึง id จากข้อความผิดข้อจำกัด)
บรรทัด 399: คัดลอกแผนไม่ให้แก้ของเดิม
บรรทัด 400–401: วนทีละวัน ลบได้สูงสุด 10 จุดต่อวัน
บรรทัด 402: ประเมินวันนั้นด้วย ➜ evaluate_route() ใน algorithm/utils.py (ประเมินวันเดียว จึงข้อความขึ้นต้น Day 1:)
บรรทัด 403: เก็บข้อความผิดข้อจำกัดของวันนั้น
บรรทัด 404: ตรวจว่าเวลารวมไม่เกินเพดาน
บรรทัด 405–406: ถ้าเวลาผ่านและไม่มีข้อผิด หยุดซ่อมวันนี้
บรรทัด 408–414: รวบรวม id ของจุดที่ไปถึงหลังเวลาปิดจากข้อความผิดข้อจำกัดด้วย regex
บรรทัด 416–422: ลำดับความสำคัญแรก: ลบจุดที่ไปถึงสายก่อน (ถ้าไม่ใช่ร้านอาหารและไม่ถูกป้องกัน)
บรรทัด 423–427: ถ้าไม่มี ลบที่เที่ยวที่คะแนนต่ำสุด
บรรทัด 428–429: ถ้าไม่มีจุดให้ลบ หยุด
บรรทัด 430: ลบจุดที่เลือก
บรรทัด 431: คืนแผนที่ซ่อมเวลาแล้ว (ใช้ที่ ➜ genetic_solve() ใน algorithm/genetic.py ด้วย)
บรรทัด 437–448  `hybrid_solve`: ประกาศ
437  def hybrid_solve(pois: List[Dict], hotel: Dict, days: int, budget: float,
438                   scoring_mode: str = 'ratio',
439                   pop_size: int = 30, generations: int = 60,
440                   mutation_rate: float = 0.3,
441                   verbose: bool = False,
442                   diversity_weight: float = 0.0, rl_theta=None, ils: bool = True) -> Tuple[List[List[Dict]], List[float]]:
443      """Hybrid Algorithm:
444         Step 1: Greedy slot-based seed (multiple random starts)
445         Step 2: GA refinement
446         Step 3: 2-opt local search per day
447         Returns: (best_chromosome, fitness_history)
448      """
บรรทัด 437–442: ประกาศ hybrid_solve รับจุดทั้งหมด โรงแรม จำนวนวัน งบ โหมดคะแนน ขนาดประชากร 30 จำนวนรุ่น 60 อัตรากลายพันธุ์ 0.3 น้ำหนักความหลากหลาย พารามิเตอร์ RL และธง ILS (เปิดเป็นค่าเริ่มต้น)
บรรทัด 443–448: docstring: Step 1 seed จาก greedy หลายชุด Step 2 GA Step 3 2-opt คืน (แผนที่ดีที่สุด ประวัติ fitness) ถูกเรียกจาก ➜ backend/main.py
บรรทัด 449–477  ขั้นที่ 1: สร้างประชากรเริ่มต้น
449      # ขั้นที่ 1: สร้างประชากรเริ่มต้นจาก greedy seeds หลายชุด (POI order ต่างกัน)
450      population = []
451      seed_pois = list(pois)
452      random.shuffle(seed_pois)
453      population.append(greedy_solve(seed_pois, hotel, days, budget, scoring_mode=scoring_mode))
454      population.append(greedy_solve(pois, hotel, days, budget, scoring_mode=scoring_mode))
455      if rl_theta is not None:   # RL seed: policy ที่ฝึกแล้ว 1 แผน deterministic + ครึ่งหนึ่งของที่เหลือสุ่มตาม policy (temperature ต่ำ)
456          from rl import rl_solve
457          population.append(rl_solve(pois, hotel, days, budget, rl_theta, sample=False))
458      while len(population) < pop_size:
459          random.shuffle(seed_pois)
460          if rl_theta is not None and len(population) % 2 == 0:
461              import numpy as _np
462              _np.random.seed(random.randrange(1 << 30))
463              cand = rl_solve(seed_pois, hotel, days, budget, rl_theta, sample=True, temperature=0.4)
464          else:
465              # โหมด quality ไม่คิดค่าเดินทางตอนเลือก — ผสม seed แบบ ratio (คำนึงถึงต้นทุน) เพื่อให้มีแผนที่อยู่ในงบเมื่อโรงแรมอยู่ไกลแหล่งท่องเที่ยว
466              cand = greedy_solve(seed_pois, hotel, days, budget,
467                                  scoring_mode='ratio' if (scoring_mode == 'quality' and len(population) % 3 == 0) else scoring_mode)
468          population.append(cand)
469
470      fitnesses = [_fitness(c, hotel, budget, scoring_mode, diversity_weight) for c in population]
471
472      best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
473      best = copy.deepcopy(population[best_idx])
474      best_fit = fitnesses[best_idx]
475      history = [best_fit]
476      no_improve = 0
477      EARLY_STOP = 15
บรรทัด 449–452: เตรียมรายการ population และสลับลำดับ POI
บรรทัด 453–454: สร้าง seed 2 ชุดแรกด้วย ➜ greedy_solve() ใน algorithm/greedy.py (ลำดับสลับ และลำดับเดิม)
บรรทัด 455–457: ถ้ามีนโยบาย RL ใส่ seed จาก RL แบบกำหนดแน่นอน 1 แผน ด้วย ➜ rl_solve() ใน algorithm/rl.py
บรรทัด 458–468: เติมประชากรจนครบ: ครึ่งหนึ่งใช้ RL แบบสุ่มตามนโยบาย (ถ้ามี) ที่เหลือใช้ greedy และในโหมด quality ผสม seed แบบ ratio ทุกตัวที่ 3 เพื่อให้มีแผนที่อยู่ในงบเมื่อโรงแรมไกล
บรรทัด 470: คำนวณ fitness ของทุกตัว
บรรทัด 472–475: เก็บตัวที่ดีที่สุดและประวัติ
บรรทัด 476–477: ตัวนับ no_improve และเกณฑ์หยุดเร็ว 15 รุ่น
บรรทัด 479–514  ขั้นที่ 2: ลูป GA
479      # ขั้นที่ 2: วิวัฒนาการด้วย Genetic Algorithm
480      for gen in range(generations):
481          new_pop = [copy.deepcopy(best)]  # elitism
482
483          # ปรับ mutation rate ลดลงตาม generation
484          cur_mut_rate = mutation_rate * (1.0 - gen / (2.0 * generations))
485
486          while len(new_pop) < pop_size:
487              # Tournament selection k=3 (เลือก best จาก 3 ตัวสุ่ม)
488              c1 = random.sample(range(len(population)), 3)
489              p1 = population[max(c1, key=lambda i: fitnesses[i])]
490              c2 = random.sample(range(len(population)), 3)
491              p2 = population[max(c2, key=lambda i: fitnesses[i])]
492              child = _crossover(p1, p2)
493              child = _mutate(child, pois, cur_mut_rate)
494              new_pop.append(child)
495
496          population = new_pop
497          fitnesses = [_fitness(c, hotel, budget, scoring_mode, diversity_weight) for c in population]
498
499          cur_best = max(range(len(population)), key=lambda i: fitnesses[i])
500          if fitnesses[cur_best] > best_fit:
501              best_fit = fitnesses[cur_best]
502              best = copy.deepcopy(population[cur_best])
503              no_improve = 0
504          else:
505              no_improve += 1
506
507          history.append(best_fit)
508          if verbose and gen % 10 == 0:
509              print(f"  Gen {gen}: fitness={best_fit:.2f}")
510          # หยุดเร็วถ้าไม่มี improvement
511          if no_improve >= EARLY_STOP:
512              if verbose:
513                  print(f"  Early stop at gen {gen} (no improvement for {EARLY_STOP} gens)")
514              break
บรรทัด 480: วนตามจำนวนรุ่น
บรรทัด 481: elitism เก็บตัวที่ดีที่สุด
บรรทัด 483–484: ลดอัตรากลายพันธุ์ลงตามรุ่น (เหลือครึ่งหนึ่งตอนท้าย)
บรรทัด 486–494: สร้างลูกจนครบประชากร: tournament k=3 สองครั้ง _crossover แล้ว _mutate
บรรทัด 496–497: แทนประชากรและคำนวณ fitness ใหม่
บรรทัด 499–505: อัปเดตตัวที่ดีที่สุดถ้าดีขึ้น และนับรุ่นที่ไม่ดีขึ้น
บรรทัด 507: บันทึกประวัติ
บรรทัด 508–509: พิมพ์ทุก 10 รุ่นถ้า verbose
บรรทัด 510–514: หยุดเร็วถ้าไม่ดีขึ้น 15 รุ่นติด
บรรทัด 516–550  ขั้นที่ 3-7: ปรับแต่งแผนสุดท้าย
516      # ขั้นที่ 3: 2-opt local search บน best solution
517      refined = []
518      for day in best:
519          refined.append(two_opt_day(day, hotel))
520
521      # ขั้นที่ 4: รับประกัน lunch + dinner ครบทุกวัน
522      refined = meal_fill(refined, pois, hotel, budget, scoring_mode)
523
524      # ขั้นที่ 5: ลบ attr ออกจากวันที่ยังเกิน time budget
525      refined = _time_repair(refined, hotel)
526
527      # ขั้นที่ 6: การเติมมื้อ/ซ่อมเวลาอาจดันงบเกิน (พบ 2 จาก 960 รอบทดสอบ) — ซ่อมงบแล้วตรวจมื้อและเวลาซ้ำ
528      for _ in range(3):
529          refined = _budget_repair(refined, hotel, budget, pool=pois)
530          if all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in refined if day):
531              break
532          for d, day in enumerate(refined):   # วันที่แน่นจนไม่มีเวลาใส่มื้อ: ถอด attraction คะแนนต่ำสุดออกก่อนเติมมื้อ
533              if day and sum(1 for p in day if p['category'] == 'restaurant') < 2:
534                  cands = [(i, p) for i, p in enumerate(day) if p['category'] != 'restaurant']
535                  if cands:
536                      refined[d] = [p for i, p in enumerate(day) if i != min(cands, key=lambda c: c[1]['score'])[0]]
537          refined = _time_repair(meal_fill(refined, pois, hotel, budget, scoring_mode), hotel)
538      refined = _budget_repair(refined, hotel, budget, pool=pois)
539
540      if ils:   # ขั้นที่ 7 (ทดลอง): insertion local search — รับผลเฉพาะเมื่อยังผ่านข้อจำกัดและ fitness ไม่แย่ลง
541          from ils import insertion_local_search
542          improved = insertion_local_search(refined, pois, hotel, budget, diversity_weight)
543          improved = [two_opt_day(day, hotel) for day in improved]
544          ev = evaluate_route(improved, hotel, budget)
545          meals_ok = all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in improved if day)
546          if ev['valid'] and meals_ok and (_fitness(improved, hotel, budget, scoring_mode, diversity_weight)
547                                           >= _fitness(refined, hotel, budget, scoring_mode, diversity_weight)):
548              refined = improved
549
550      return refined, history
บรรทัด 516–519: ขั้นที่ 3: 2-opt ทุกวันด้วย two_opt_day
บรรทัด 521–522: ขั้นที่ 4: รับประกันมื้อกลางวัน+เย็นด้วย meal_fill
บรรทัด 524–525: ขั้นที่ 5: ลบที่เที่ยวจากวันที่ยังเกินเวลาด้วย _time_repair
บรรทัด 527–538: ขั้นที่ 6: การเติมมื้อและซ่อมเวลาอาจดันงบเกิน จึงวนไม่เกิน 3 รอบ ซ่อมงบด้วย _budget_repair ตรวจมื้อครบ ถ้าไม่ครบถอดที่เที่ยวคะแนนต่ำสุดของวันนั้นแล้วเติมมื้อและซ่อมเวลาใหม่ แล้วซ่อมงบอีกครั้งท้ายสุด
บรรทัด 540–548: ขั้นที่ 7: ถ้าเปิด ILS เรียก ➜ insertion_local_search() ใน algorithm/ils.py แล้ว 2-opt ทุกวัน ตรวจว่า valid มีมื้อครบ และ fitness ไม่แย่ลง จึงรับแผนใหม่
บรรทัด 550: คืนแผนและประวัติ fitness
บรรทัด 553–607  `_budget_repair` ซ่อมงบ
553  def _budget_repair(routes: List[List[Dict]], hotel: Dict, budget: float, protect=(), pool=None) -> List[List[Dict]]:
554      """ถ้าแผนเกินงบ แทนที่ attraction (ไม่ได้ล็อก) ที่แพงสุดในวันที่มีสถานที่มากที่สุด ด้วยสถานที่ที่ถูกกว่าและคะแนนสูงสุดที่ยังไม่ได้ใช้ในวันเดียวกัน
555         ถ้าไม่มีตัวแทนที่ใช้ได้จึงลบทิ้ง จนอยู่ในงบ (เดิมลบอย่างเดียว ทำให้บางวันเหลือจุดน้อยเมื่อกำหนดงบต่ำ)"""
556      routes = [list(d) for d in routes]
557      for _ in range(60):
558          if evaluate_route(routes, hotel, float('inf'))['total_cost'] <= budget:
559              break
560          # ก่อนตัดสถานที่: สลับร้านอาหารเป็นร้านที่ทำให้ค่าใช้จ่ายรวม (ค่าอาหาร+ค่าเดินทาง) ลดมากที่สุด
561          # ร้านที่ไกลโรงแรมกินงบจนแผนเหลือแต่ร้านอาหาร (เช่น นครนายก งบ 2,000 บาท ไม่รวมโรงแรม)
562          if pool:
563              used = {p['id'] for day in routes for p in day}
564              rests = [p for p in pool if p['category'] == 'restaurant' and p['id'] not in used and p['id'] not in protect]
565              best = None
566              for d, day in enumerate(routes):
567                  base = evaluate_route([day], hotel, float('inf'))['total_cost']
568                  for i, p in enumerate(day):
569                      if p['category'] != 'restaurant' or p['id'] in protect:
570                          continue
571                      for u in rests:
572                          trial = day[:i] + [u] + day[i + 1:]
573                          ev = evaluate_route([trial], hotel, float('inf'))
574                          gain = base - ev['total_cost']
575                          if ev['valid'] and gain > 0.5 and (best is None or gain > best[0]):
576                              best = (gain, d, i, trial)
577              if best:
578                  routes[best[1]] = best[3]
579                  continue
580          cands = [(d, i, p) for d, day in enumerate(routes) for i, p in enumerate(day)
581                   if p['category'] != 'restaurant' and p['id'] not in protect]
582          if not cands:
583              break
584          # ถ้าตัดสถานที่ทั้งหมดแล้วก็ยังเกินงบ (ร้านอาหารไกลกันเกินไป) การตัดไม่ช่วยอะไร ให้คงสถานที่ไว้ ผู้ใช้จะได้แจ้งว่างบไม่พอ
585          floor = [[p for p in day if p['category'] == 'restaurant' or p['id'] in protect] for day in routes]
586          if evaluate_route(floor, hotel, float('inf'))['total_cost'] > budget:
587              break
588          # ลบเฉพาะสถานที่ที่ลบแล้วค่าใช้จ่ายรวมลดลงจริง (ค่าเข้า+ค่าเดินทาง): สถานที่ฟรีที่อยู่ระหว่างทางลบแล้วไม่ช่วยงบ
589          # และถ้าเหตุที่เกินงบคือร้านอาหารอยู่ไกล การลบสถานที่ทิ้งหมดจะได้แผนที่มีแต่ร้านอาหารและยังเกินงบอยู่ดี
590          cands = [c for c in cands
591                   if evaluate_route([routes[c[0]]], hotel, float('inf'))['total_cost']
592                   - evaluate_route([routes[c[0]][:c[1]] + routes[c[0]][c[1] + 1:]], hotel, float('inf'))['total_cost'] > 0.5]
593          if not cands:
594              break
595          sights = [sum(1 for p in day if p['category'] != 'restaurant') for day in routes]
596          d, i, old = max(cands, key=lambda c: (sights[c[0]], c[2]['cost'], -c[2]['score']))   # ตัดจากวันที่มีสถานที่มากที่สุดก่อน เพื่อให้แต่ละวันเหลือจำนวนใกล้เคียงกัน
597          used = {p['id'] for day in routes for p in day}
598          subs = sorted((p for p in (pool or []) if p['category'] != 'restaurant' and p['id'] not in used and p['id'] not in protect
599                         and p['cost'] < old['cost']), key=lambda p: -p['score'])[:30]
600          for u in subs:
601              trial = routes[d][:i] + [u] + routes[d][i + 1:]
602              if evaluate_route([trial], hotel, float('inf'))['valid']:
603                  routes[d] = trial
604                  break
605          else:
606              routes[d].pop(i)
607      return routes
บรรทัด 553: ประกาศ _budget_repair รับ protect (จุดล็อก) และ pool (จุดที่ใช้เป็นตัวแทนได้)
บรรทัด 554–555: docstring: ถ้าเกินงบ แทนที่ที่เที่ยวที่แพงสุดด้วยจุดที่ถูกกว่าและคะแนนสูงสุด ถ้าไม่มีตัวแทนจึงลบทิ้ง
บรรทัด 556: คัดลอกแผน
บรรทัด 557–559: วนไม่เกิน 60 รอบ หยุดเมื่อค่าใช้จ่ายรวมอยู่ในงบ
บรรทัด 560–579: ก่อนตัดที่เที่ยว ลองสลับร้านอาหารเป็นร้านที่ประหยัดสุด (ร้านไกลโรงแรมกินงบจนเหลือแต่ร้านอาหาร เช่น นครนายก งบ 2,000) เลือกคู่ที่ประหยัดสุดที่ยัง valid
บรรทัด 580–583: รวบรวมที่เที่ยวที่ลบได้ (ไม่ใช่ร้านและไม่ถูกป้องกัน) ถ้าไม่มี หยุด
บรรทัด 584–587: ถ้าตัดที่เที่ยวหมดแล้วก็ยังเกินงบ การตัดไม่ช่วย จึงหยุด (ผู้ใช้จะได้รับแจ้งว่างบไม่พอ)
บรรทัด 588–594: กรองให้เหลือเฉพาะที่ลบแล้วค่าใช้จ่ายลดลงจริง (ที่เที่ยวฟรีลบแล้วไม่ช่วยงบ)
บรรทัด 595–596: เลือกจุดจากวันที่มีที่เที่ยวมากที่สุดก่อน เพื่อให้แต่ละวันเหลือจำนวนใกล้เคียงกัน
บรรทัด 597–599: หาตัวแทนที่ยังไม่ใช้ ถูกกว่าจุดเดิม คะแนนสูงสุด สูงสุด 30 ตัว
บรรทัด 600–604: ลองแทนที่ ถ้าวันนั้นยัง valid ใช้ตัวแทนนั้น
บรรทัด 605–606: ถ้าไม่มีตัวแทนที่ใช้ได้ ลบจุดทิ้ง
บรรทัด 607: คืนแผน
บรรทัด 610–626  `_final_validity` ซ่อมขั้นสุดท้ายสำหรับจุดล็อก
610  def _final_validity(routes: List[List[Dict]], hotel: Dict, locked, tried=None) -> List[List[Dict]]:
611      """วันที่ยังผิดเวลา/เวลาปิดหลังซ่อมแล้ว (มักเกิดจากจุดที่ผู้ใช้ล็อกเปิดดึก ชนกับมื้อเย็น):
612         1) ลองย้ายจุดล็อกที่เปิดหลัง 17:00 ไปท้ายวัน  2) ถ้ายังไม่ผ่าน ถอดจุดล็อกของวันนั้นออก (ผู้ใช้จะได้รับแจ้ง)"""
613      routes = [list(d) for d in routes]
614      for d, day in enumerate(routes):
615          if not day or evaluate_route([day], hotel, float('inf'))['valid']:
616              continue
617          late = [p for p in day if p['id'] in locked and p['open_min'] >= 1020]
618          trial = [p for p in day if p not in late] + late
619          # ย้ายไปท้ายวันได้ครั้งเดียวต่อวัน (meal_fill อาจจัดลำดับกลับ) — ถ้ายังไม่ผ่านรอบถัดไปถอดจุดล็อกออก
620          if late and (tried is None or d not in tried) and evaluate_route([trial], hotel, float('inf'))['valid']:
621              routes[d] = trial
622              if tried is not None:
623                  tried.add(d)
624          else:
625              routes[d] = [p for p in day if p['id'] not in locked]
626      return routes
บรรทัด 610–612: ประกาศและอธิบาย: วันที่ยังผิดหลังซ่อม (มักเพราะจุดล็อกที่เปิดดึกชนกับมื้อเย็น) ลองย้ายจุดล็อกที่เปิดหลัง 17:00 ไปท้ายวัน ถ้ายังไม่ผ่านถอดจุดล็อกออก
บรรทัด 613: คัดลอกแผน
บรรทัด 614–616: ข้ามวันว่างหรือวันที่ valid อยู่แล้ว
บรรทัด 617–618: แยกจุดล็อกที่เปิดหลัง 17:00 ไปต่อท้ายวัน
บรรทัด 619–623: ย้ายได้ครั้งเดียวต่อวัน (tried) และต้อง valid จึงยอมรับ
บรรทัด 624–625: ไม่ผ่านก็ถอดจุดล็อกของวันนั้น
บรรทัด 626: คืนแผน
บรรทัด 629–640  `infeasible_locks` จุดล็อกที่ใส่ไม่ได้
629  def infeasible_locks(pois: List[Dict], hotel: Dict, locked_ids, budget: float) -> List[str]:
630      """POI ที่ผู้ใช้เลือกแต่ใส่ในแผนใดก็ไม่ได้ (เปิดดึกเกินวัน/เกินงบ/เกินเวลาต่อวัน) — คืน id เพื่อไม่ล็อกและแจ้งผู้ใช้"""
631      by_id = {p['id']: p for p in pois}
632      bad = []
633      for pid in locked_ids:
634          p = by_id.get(pid)
635          if p is None:
636              continue
637          ev = evaluate_route([[p]], hotel, budget)
638          if not ev['valid']:
639              bad.append(pid)
640      return bad
บรรทัด 629–630: ประกาศและ docstring: จุดที่ผู้ใช้เลือกแต่ใส่แผนใดก็ไม่ได้ (เปิดดึกเกินวัน เกินงบ เกินเวลา)
บรรทัด 631: ทำดัชนี id → จุด
บรรทัด 632–640: ทดลองใส่แต่ละจุดเป็นแผนวันเดียว ถ้าไม่ valid ถือว่าไม่ได้ คืนรายการ id ให้ผู้เรียก (➜ backend/main.py) แจ้งผู้ใช้
บรรทัด 643–685  `reoptimize_solve` เริ่มต้นและวิวัฒนาการ
643  def reoptimize_solve(pois: List[Dict], hotel: Dict, routes: List[List[Dict]], budget: float,
644                       locked_ids=(), excluded_ids=(), scoring_mode: str = 'quality',
645                       pop_size: int = 20, generations: int = 30,
646                       mutation_rate: float = 0.6, diversity_weight: float = 0.0) -> List[List[Dict]]:
647      """Re-optimization หลังผู้ใช้แก้แผน: เริ่มจาก routes ปัจจุบัน (ไม่สร้างใหม่ทั้งหมด)
648         - locked_ids:   POI ที่ผู้ใช้เลือกเอง (สลับเข้า/เพิ่ม) ต้องอยู่ในแผนเสมอ
649         - excluded_ids: POI ที่ผู้ใช้ลบ ห้ามกลับเข้ามา
650         ใช้ evolutionary search แบบ (mu+lambda) เฉพาะ mutation แล้วตามด้วย 2-opt, meal_fill, time_repair
651         เพื่อปรับ POI ที่ไม่ล็อกให้ score สูงขึ้นภายใต้งบ/เวลาเดิม
652      """
653      locked, excluded = set(locked_ids), set(excluded_ids)
654      locked -= set(infeasible_locks(pois, hotel, locked, budget))
655      locked_all = set(locked)
656      pool = [p for p in pois if p['id'] not in excluded]
657      start = [[p for p in day if p['id'] not in excluded] for day in routes]
658
659      def respects(ch):
660          ids = {p['id'] for day in ch for p in day}
661          return locked <= ids and not (ids & excluded)
662
663      population = [start]
664      fits = [_fitness(start, hotel, budget, scoring_mode, diversity_weight)]
665      for _ in range(generations):
666          children = []
667          for _ in range(pop_size):
668              parent = population[random.randrange(len(population))]
669              child = _mutate(copy.deepcopy(parent), pool, mutation_rate)
670              if respects(child):
671                  children.append(child)
672          population += children
673          fits += [_fitness(c, hotel, budget, scoring_mode, diversity_weight) for c in children]
674          order = sorted(range(len(population)), key=lambda i: fits[i], reverse=True)[:pop_size]
675          population = [population[i] for i in order]
676          fits = [fits[i] for i in order]
677
678      refined = [two_opt_day(day, hotel) for day in population[0]]
679      before = refined
680      refined = meal_fill(refined, pool, hotel, budget, scoring_mode)
681      kept = {p['id'] for day in refined for p in day}
682      for d, day in enumerate(before):          # meal_fill ตัด attr เกิน 4 ต่อวัน — คืนจุดที่ผู้ใช้ล็อกไว้
683          for p in day:
684              if p['id'] in locked and p['id'] not in kept:
685                  refined[d].insert(max(0, len(refined[d]) - 1), p)
บรรทัด 643–646: ประกาศ reoptimize_solve รับแผนปัจจุบัน งบ จุดล็อก จุดที่ห้ามกลับ โหมด ขนาดประชากร 20 รุ่น 30 อัตรากลายพันธุ์ 0.6
บรรทัด 647–652: docstring: ปรับแผนหลังผู้ใช้แก้ เริ่มจากแผนปัจจุบัน ใช้การค้นหาแบบ (mu+lambda) เฉพาะ mutation แล้ว 2-opt, meal_fill, time_repair
บรรทัด 653–654: เตรียมชุดจุดล็อกและจุดที่ถูกลบ และตัดจุดล็อกที่ใส่ไม่ได้ด้วย infeasible_locks
บรรทัด 655: เก็บสำเนาจุดล็อกทั้งหมดไว้ใช้ตอนใส่คืน
บรรทัด 656–657: ตัดจุดที่ถูกลบออกจากชุดจุดและแผนตั้งต้น
บรรทัด 659–661: ฟังก์ชัน respects ตรวจว่าแผนมีจุดล็อกครบและไม่มีจุดที่ห้าม
บรรทัด 663–664: ประชากรเริ่มต้นคือแผนตั้งต้น และ fitness ของมัน
บรรทัด 665–676: วนตามรุ่น: สร้างลูกด้วย _mutate เฉพาะที่เคารพจุดล็อก/ห้าม รวมกับประชากรเดิม เรียงด้วย fitness แล้วเก็บ 20 ตัวดีสุด
บรรทัด 678–680: 2-opt ในทุกวันของตัวดีที่สุด แล้ว meal_fill
บรรทัด 681–685: คืนจุดล็อกที่ meal_fill ตัดออกเมื่อมีที่เที่ยวเกิน 4 ต่อวัน
บรรทัด 686–720  `reoptimize_solve` ซ่อมซ้ำจนผ่าน
686      # รอบซ่อมวนซ้ำจนแผนผ่านทุกข้อจำกัดและมีมื้อครบ (การเติมมื้ออาจทำให้เวลา/งบเสียอีก จึงต้องตรวจหลังเติมเสมอ)
687      def meals_ok(rs):
688          return all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in rs)
689
690      tried_days = set()
691      for _ in range(5):
692          refined = _time_repair(refined, hotel, protect=locked)
693          refined = _budget_repair(refined, hotel, budget, protect=locked)
694          refined = _final_validity(refined, hotel, locked, tried_days)
695          locked = locked & {p['id'] for day in refined for p in day}      # จุดล็อกที่ยังอยู่ในแผน
696          lacking = [d for d, day in enumerate(refined)
697                     if sum(1 for p in day if p['category'] == 'restaurant') < 2]
698          for d in lacking:           # วันที่แน่นจนไม่มีเวลาใส่มื้อ: ลบ attraction คะแนนต่ำสุดที่ไม่ได้ล็อกก่อนเติมมื้อ
699              cands = [(i, p) for i, p in enumerate(refined[d])
700                       if p['category'] != 'restaurant' and p['id'] not in locked]
701              if cands:
702                  refined[d].pop(min(cands, key=lambda c: c[1]['score'])[0])
703          refined = meal_fill(refined, pool, hotel, budget, scoring_mode)
704          ev = evaluate_route(refined, hotel, budget)
705          if ev['valid'] and meals_ok(refined):
706              break
707      if not meals_ok(refined):    # ทางสุดท้าย: วันที่ยังไม่มีมื้อครบ เก็บเฉพาะจุดที่ผู้ใช้ล็อก แล้วเติมมื้อใหม่ (ได้แผนสั้นแต่ใช้ได้จริง)
708          for d, day in enumerate(refined):
709              if sum(1 for p in day if p['category'] == 'restaurant') < 2:
710                  refined[d] = [p for p in day if p['id'] in locked and p['category'] != 'restaurant']
711          refined = _time_repair(meal_fill(refined, pool, hotel, budget, scoring_mode), hotel, protect=locked)
712          refined = _budget_repair(refined, hotel, budget, protect=locked)
713      for _ in range(2):    # วันที่ยังผิดข้อจำกัดอยู่ (เช่น มื้อสายเกินช่วง): ล้างเหลือเฉพาะจุดที่ล็อก แล้วสร้างวันนั้นใหม่
714          bad = {int(v.split()[1].rstrip(':')) - 1 for v in evaluate_route(refined, hotel, budget)['violations'] if v.startswith('Day ')}
715          if not bad:
716              break
717          for d in bad:
718              refined[d] = [p for p in refined[d] if p['id'] in locked and p['category'] != 'restaurant']
719          refined = _time_repair(meal_fill(refined, pool, hotel, budget, scoring_mode), hotel, protect=locked)
720          refined = _budget_repair(refined, hotel, budget, protect=locked)
บรรทัด 687–688: ฟังก์ชัน meals_ok ตรวจว่าทุกวันมีร้านอย่างน้อย 2 ร้าน
บรรทัด 690–694: วนไม่เกิน 5 รอบ: ซ่อมเวลา ซ่อมงบ ซ่อมความถูกต้องสุดท้ายโดยป้องกันจุดล็อก
บรรทัด 695: ปรับชุดจุดล็อกให้เหลือเฉพาะที่ยังอยู่ในแผน
บรรทัด 696–702: วันที่ไม่มีเวลาใส่มื้อ ลบที่เที่ยวคะแนนต่ำสุดที่ไม่ได้ล็อกก่อน
บรรทัด 703–706: เติมมื้อใหม่ ถ้า valid และมื้อครบ ออกจากลูป
บรรทัด 707–712: ทางสุดท้าย: วันที่ยังขาดมื้อ เก็บเฉพาะจุดล็อกแล้วเติมมื้อใหม่ ได้แผนสั้นแต่ใช้ได้จริง
บรรทัด 713–720: อีกสองรอบสำหรับวันที่ยังผิดข้อจำกัด (เช่น มื้อสายเกินช่วง): ล้างเหลือเฉพาะจุดล็อกแล้วสร้างวันนั้นใหม่
บรรทัด 721–735  ใส่จุดล็อกกลับและคืนผล
721      # จุดล็อกที่ใส่ได้จริงแต่ถูกถอดระหว่างซ่อม: ใส่กลับในตำแหน่งที่ทำให้แผนยังผ่านทุกข้อจำกัด (ระยะเพิ่มน้อยสุด)
722      by_id = {p['id']: p for p in pois}
723      for pid in locked_all - {p['id'] for day in refined for p in day}:
724          best = None
725          for d, day in enumerate(refined):
726              for i in range(len(day) + 1):
727                  trial = refined[:d] + [day[:i] + [by_id[pid]] + day[i:]] + refined[d + 1:]
728                  ev = evaluate_route(trial, hotel, budget)
729                  if ev['valid']:
730                      km = sum(x['distance_km'] for x in ev['days_detail'])
731                      if best is None or km < best[0]:
732                          best = (km, trial)
733          if best:
734              refined = best[1]
735      return refined
บรรทัด 721–723: จุดล็อกที่ใส่ได้จริงแต่ถูกถอดระหว่างซ่อม ให้ใส่กลับ
บรรทัด 724–732: ลองแทรกที่ทุกตำแหน่งของทุกวัน เลือกตำแหน่งที่แผนยัง valid และระยะรวมเพิ่มน้อยสุด
บรรทัด 733–734: ใช้ตำแหน่งที่ดีที่สุด
บรรทัด 735: คืนแผน (เรียกจาก /api/reoptimize ใน ➜ backend/main.py)
บรรทัด 738–753  ฟังก์ชันทดสอบ
738  def main():
739      from utils import load_data, print_result
740      pois, hotels = load_data('../data/provinces/phuket.json')
741      h = next(h for h in hotels if h['id'] == 'H11')
742      print(f"Hotel: {h['name_en']}")
743      t0 = time.time()
744      routes, history = hybrid_solve(pois, h, 6, 6800, verbose=True)
745      elapsed = (time.time() - t0) * 1000
746      print(f"\nElapsed: {elapsed:.0f} ms")
747      print(f"History: gen0={history[0]:.1f} → final={history[-1]:.1f}")
748      result = evaluate_route(routes, h, 6800)
749      print_result(result, label='Hybrid')
750
751
752  if __name__ == '__main__':
753      main()
บรรทัด 738–741: main สำหรับทดสอบตรง ๆ: โหลดข้อมูลภูเก็ตด้วย ➜ load_data() ใน algorithm/utils.py และเลือกโรงแรม H11
บรรทัด 742–744: พิมพ์ชื่อโรงแรม จับเวลา และรัน hybrid_solve 6 วัน งบ 6,800
บรรทัด 745–749: พิมพ์เวลา ประวัติ fitness และผลด้วย ➜ print_result() ใน algorithm/utils.py
บรรทัด 752–753: เรียก main() เมื่อรันไฟล์นี้โดยตรง

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/ils.py
algorithm/rl.py
algorithm/utils.py
backend/main.py