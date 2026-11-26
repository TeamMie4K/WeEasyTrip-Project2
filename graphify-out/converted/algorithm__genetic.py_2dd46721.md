<!-- converted from algorithm__genetic.py.docx -->

คู่มือโค้ด: algorithm/genetic.py
Genetic Algorithm (GA) สำหรับ B-TOPTW
ไฟล์ต้นฉบับ: algorithm/genetic.py (302 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: วิวัฒนาการแผนทริปด้วยประชากร (population) ของแผน เริ่มจาก seed ของ ➜ greedy_solve() ใน algorithm/greedy.py แล้วใช้ selection, crossover, mutation, repair และ elitism วนหลายรุ่น ตัววัดคือ fitness ซึ่งอิง ➜ evaluate_route() ใน algorithm/utils.py เป็นทั้งอัลกอริทึมเปรียบเทียบในบทที่ 4 และเป็นแกนกลางที่ ➜ hybrid_solve() ใน algorithm/hybrid.py ต่อยอด

บรรทัด 1–26  หัวไฟล์ นำเข้า
1  # -*- coding: utf-8 -*-
2  """
3  genetic.py - Genetic Algorithm สำหรับปัญหา B-TOPTW
4
5  โครงสร้าง chromosome: list of list ของ POI dict
6    chromosome = [
7        [poi_a, poi_b, ...],   # day 1
8        [poi_c, poi_d, ...],   # day 2
9        ...
10    ]
11
12  Operators:
13    - Initialization: greedy seed + random
14    - Selection:      tournament (k=3)
15    - Crossover:      day-level swap (เลือก parent ของแต่ละวันแบบสุ่ม)
16    - Mutation:       swap / insert / remove
17    - Repair:         ลบ POI ที่แย่ที่สุดออกถ้าละเมิด constraint
18    - Replacement:    elitism (เก็บ best ไว้ทุก gen)
19  """
20  import random
21  import time
22  import copy
23  from typing import List, Dict, Tuple
24  from utils import evaluate_route
25  from greedy import greedy_solve
26  from hybrid import meal_fill, DIST_WEIGHT
บรรทัด 1–19: docstring อธิบายโครงสร้าง chromosome (list ของวัน แต่ละวันคือ list ของ POI) และตัวดำเนินการทั้งหมด: เริ่มต้นจาก greedy, tournament k=3, crossover ระดับวัน, mutation แบบ swap/insert/remove, repair และ elitism
บรรทัด 20–22: นำเข้า random time copy (สุ่ม จับเวลา และคัดลอกลึก)
บรรทัด 23: ชนิดข้อมูลสำหรับ type hint
บรรทัด 24: นำเข้าตัวตรวจแผน evaluate_route จาก ➜ evaluate_route() ใน algorithm/utils.py
บรรทัด 25: นำเข้า greedy_solve สำหรับสร้างประชากรเริ่มต้น
บรรทัด 26: นำเข้า meal_fill และ DIST_WEIGHT จาก ➜ algorithm/hybrid.py (ค่าถ่วงระยะ 0.3 ใช้ร่วมกับ Hybrid เพื่อเปรียบเทียบอย่างเท่าเทียม — แก้เมื่อ 18 พ.ย. 2569)
บรรทัด 32–81  ฟังก์ชัน fitness
32  def fitness(chromosome: List[List[Dict]], hotel: Dict, budget: float) -> float:
33      """fitness = total_score - penalty(violations + schedule imbalance)
34      soft constraint: penalize budget, time/window, and unrealistic schedule"""
35      result = evaluate_route(chromosome, hotel, budget)
36      score = result['total_score']
37      penalty = 0.0
38
39      if result['total_cost'] > budget:
40          penalty += (result['total_cost'] - budget) * 0.005
41
42      for v in result['violations']:
43          if 'งบประมาณเกิน' in v:
44              pass
45          elif 'ใช้เวลาเกิน' in v:
46              penalty += 5.0
47          elif 'หลังเวลาปิด' in v:
48              penalty += 3.0
49          else:
50              penalty += 2.0
51
52      # ตรวจสอบความสมดุลของแต่ละวัน (เหมือนการท่องเที่ยวจริง)
53      for day in chromosome:
54          if not day:
55              continue
56          cats = [p['category'] for p in day]
57          n_rest = sum(1 for c in cats if c == 'restaurant')
58          n_attr = sum(1 for c in cats if c != 'restaurant')
59
60          # 1) จำกัดร้านอาหาร 2 ต่อวัน (lunch + dinner)
61          if n_rest > 2:
62              penalty += (n_rest - 2) * 12.0
63          # 1b) ขาดร้านอาหาร = penalty หนัก
64          if n_rest == 0:
65              penalty += 20.0
66          elif n_rest == 1:
67              penalty += 10.0
68          # 2) วันที่มีแต่ร้านอาหาร ไม่มีที่เที่ยว = penalty หนัก
69          if n_rest > 0 and n_attr == 0:
70              penalty += 25.0
71          # 3) จุดท่องเที่ยวน้อยเกิน
72          if n_attr < 2 and len(day) > 0:
73              penalty += 4.0
74          # 4) วันที่ทุกจุดเป็นหมวดเดียวกัน
75          unique_cats = len(set(cats))
76          if len(day) >= 3 and unique_cats < 2:
77              penalty += 6.0
78
79      # ระยะขับรวม: ใช้ค่าถ่วงเดียวกับ Hybrid/ILS เพื่อเปรียบเทียบอย่างเท่าเทียม
80      penalty += DIST_WEIGHT * sum(d['distance_km'] for d in result['days_detail'])
81      return score - penalty
บรรทัด 32: ประกาศ fitness รับแผน โรงแรม งบ คืนตัวเลข ยิ่งสูงยิ่งดี
บรรทัด 33–34: docstring: fitness = คะแนนรวม − โทษของการผิดข้อจำกัด และความไม่สมดุลของตาราง
บรรทัด 35: ประเมินแผนด้วย evaluate_route
บรรทัด 36: เริ่มจากคะแนนรวมของแผน
บรรทัด 37: penalty ตัวสะสมโทษ
บรรทัด 39–40: ถ้าค่าใช้จ่ายรวมเกินงบ โทษ = ส่วนเกิน × 0.005
บรรทัด 42–50: วนทุกข้อความที่ผิดข้อจำกัด: เกินงบ (บรรทัด 43-44) ไม่ซ้ำโทษเพราะคิดไปแล้ว; ใช้เวลาเกิน โทษ 5; ไปหลังเวลาปิด โทษ 3; แบบอื่น โทษ 2
บรรทัด 52–56: ตรวจความสมดุลของแต่ละวัน: แยกหมวดของจุดในวัน นับร้านอาหาร (n_rest) กับที่เที่ยว (n_attr)
บรรทัด 60–62: ถ้ามีร้านอาหารเกิน 2 ต่อวัน โทษ 12 ต่อร้านที่เกิน
บรรทัด 63–67: ถ้าไม่มีร้านอาหารเลย โทษ 20 ถ้ามีร้านเดียว โทษ 10
บรรทัด 68–70: วันที่มีแต่ร้านอาหารไม่มีที่เที่ยว โทษ 25
บรรทัด 71–73: จุดท่องเที่ยวน้อยกว่า 2 จุด โทษ 4
บรรทัด 74–77: ถ้ามี 3 จุดขึ้นไปแต่ทุกจุดหมวดเดียวกัน โทษ 6
บรรทัด 79–80: ถ่วงระยะขับรวมด้วย DIST_WEIGHT (0.3 ต่อกม.) เท่ากับที่ ➜ algorithm/hybrid.py ใช้
บรรทัด 81: คืนค่า fitness = คะแนน − โทษทั้งหมด
บรรทัด 87–104  สร้างประชากรเริ่มต้น
87  def initial_population(pois: List[Dict], hotel: Dict, days: int,
88                         budget: float, pop_size: int = 50) -> List[List[List[Dict]]]:
89      """สร้าง population เริ่มต้นจาก greedy seeds ที่ shuffle POI order ต่างกัน
90      วิธีนี้ทำให้ทุก chromosome มี meal structure ครบ (lunch + dinner) ตั้งแต่ต้น
91      ทำให้ GA วิ่งจาก valid starting points แทนที่จะเริ่มจาก random ที่ไม่มีร้านอาหาร"""
92      population = []
93
94      # Greedy seed แรก (ลำดับ POI เดิม)
95      population.append(greedy_solve(pois, hotel, days, budget))
96
97      # Greedy seeds with shuffled POI orders (เหมือน Hybrid)
98      seed_pois = list(pois)
99      while len(population) < pop_size:
100          random.shuffle(seed_pois)
101          cand = greedy_solve(seed_pois, hotel, days, budget)
102          population.append(cand)
103
104      return population
บรรทัด 87–89: ประกาศ initial_population ขนาด pop_size (ค่าตั้งต้น 50)
บรรทัด 89–91: docstring: ใช้ seed จาก greedy ที่สลับลำดับ POI ต่างกัน ทำให้ทุกตัวมีมื้อครบตั้งแต่ต้น ดีกว่าเริ่มจากแผนสุ่มที่ไม่มีร้านอาหาร
บรรทัด 92: population รายการว่าง
บรรทัด 95: ตัวแรกใช้ลำดับ POI เดิม
บรรทัด 98: ทำสำเนารายการ POI ไว้สลับลำดับ
บรรทัด 99–102: วนจนครบขนาดประชากร: สลับลำดับ POI แล้วสร้างแผนด้วย ➜ greedy_solve() ใน algorithm/greedy.py
บรรทัด 104: คืนประชากร
บรรทัด 110–118  การเลือกพ่อแม่ (Tournament)
110  def tournament_select(population: List, fitnesses: List[float],
111                        k: int = 3) -> List[List[Dict]]:
112      """Tournament selection - เลือก k ตัวสุ่ม คืนตัวที่ fitness สูงสุด"""
113      contestants = random.sample(range(len(population)), k)
114      best_idx = contestants[0]
115      for c in contestants[1:]:
116          if fitnesses[c] > fitnesses[best_idx]:
117              best_idx = c
118      return copy.deepcopy(population[best_idx])
บรรทัด 110–111: ประกาศ tournament_select ขนาดการแข่ง k=3
บรรทัด 112: docstring
บรรทัด 113: สุ่มผู้เข้าแข่ง k ตัว
บรรทัด 114–117: เก็บตัวที่ fitness สูงสุด
บรรทัด 118: คืนสำเนาลึกของผู้ชนะ (กันการแก้ไขกระทบประชากรเดิม)
บรรทัด 124–144  Crossover ระดับวัน
124  def crossover(parent1: List[List[Dict]],
125                parent2: List[List[Dict]]) -> List[List[Dict]]:
126      """Day-level crossover: แต่ละวันสุ่มเอามาจาก p1 หรือ p2
127      แล้วลบ duplicate ข้ามวัน (POI ห้ามซ้ำ)"""
128      days = len(parent1)
129      child: List[List[Dict]] = []
130      for d in range(days):
131          if random.random() < 0.5:
132              child.append([dict(p) for p in parent1[d]])
133          else:
134              child.append([dict(p) for p in parent2[d]])
135
136      # ลบ POI ที่ซ้ำข้ามวัน
137      seen = set()
138      new_child: List[List[Dict]] = [[] for _ in range(days)]
139      for d in range(days):
140          for poi in child[d]:
141              if poi['id'] not in seen:
142                  seen.add(poi['id'])
143                  new_child[d].append(poi)
144      return new_child
บรรทัด 124–125: ประกาศ crossover รับพ่อและแม่
บรรทัด 126–127: docstring: แต่ละวันสุ่มเอามาจากพ่อหรือแม่ แล้วลบจุดซ้ำข้ามวัน
บรรทัด 128: จำนวนวัน
บรรทัด 129: child รายการลูกว่าง
บรรทัด 130–134: ทุกวัน สุ่ม 50% ว่าจะเอาวันจากพ่อหรือแม่ (คัดลอกแต่ละ POI)
บรรทัด 136–143: ลบจุดที่ซ้ำข้ามวัน โดยเก็บจุดแรกที่พบ ใช้ชุด seen
บรรทัด 144: คืนลูก
บรรทัด 150–187  Mutation
150  def mutate(chromosome: List[List[Dict]], all_pois: List[Dict],
151             mutation_rate: float = 0.3) -> List[List[Dict]]:
152      """3 mutations: swap (สลับใน-ระหว่างวัน), insert, remove"""
153      if random.random() > mutation_rate:
154          return chromosome
155
156      days = len(chromosome)
157      used_ids = set(p['id'] for day in chromosome for p in day)
158      op = random.choice(['swap', 'insert', 'remove', 'cross_day_swap'])
159
160      if op == 'swap':
161          days_with_2 = [i for i, day in enumerate(chromosome) if len(day) >= 2]
162          if days_with_2:
163              d = random.choice(days_with_2)
164              i, j = random.sample(range(len(chromosome[d])), 2)
165              chromosome[d][i], chromosome[d][j] = chromosome[d][j], chromosome[d][i]
166      elif op == 'cross_day_swap' and days >= 2:
167          non_empty = [i for i, day in enumerate(chromosome) if day]
168          if len(non_empty) >= 2:
169              d1, d2 = random.sample(non_empty, 2)
170              i = random.randrange(len(chromosome[d1]))
171              j = random.randrange(len(chromosome[d2]))
172              chromosome[d1][i], chromosome[d2][j] = chromosome[d2][j], chromosome[d1][i]
173      elif op == 'insert':
174          unused = [p for p in all_pois if p['id'] not in used_ids]
175          if unused:
176              poi = random.choice(unused)
177              d = random.randrange(days)
178              pos = random.randint(0, len(chromosome[d]))
179              chromosome[d].insert(pos, poi)
180      elif op == 'remove':
181          non_empty = [i for i, day in enumerate(chromosome) if day]
182          if non_empty:
183              d = random.choice(non_empty)
184              idx = random.randrange(len(chromosome[d]))
185              chromosome[d].pop(idx)
186
187      return chromosome
บรรทัด 150–151: ประกาศ mutate ด้วยอัตรา mutation_rate (ค่าตั้งต้น 0.3)
บรรทัด 152: docstring: 4 ตัวดำเนินการ (swap, insert, remove, cross_day_swap)
บรรทัด 153–154: สุ่มว่าจะกลายพันธุ์หรือไม่ ถ้าไม่ คืนแผนเดิม
บรรทัด 156–158: เตรียมจำนวนวัน ชุด id ที่ใช้แล้ว และเลือกตัวดำเนินการแบบสุ่ม
บรรทัด 160–165: swap สลับสองจุดภายในวันเดียวกัน (เลือกจากวันที่มี 2 จุดขึ้นไป)
บรรทัด 166–172: cross_day_swap สลับจุดระหว่างสองวันที่ต่างกัน
บรรทัด 173–179: insert แทรกจุดที่ยังไม่ใช้ลงตำแหน่งสุ่มของวันสุ่ม
บรรทัด 180–185: remove ลบจุดสุ่มหนึ่งจุด
บรรทัด 187: คืนแผนที่กลายพันธุ์แล้ว
บรรทัด 193–213  ซ่อมแผนที่ผิดข้อจำกัด
193  def repair(chromosome: List[List[Dict]], hotel: Dict,
194             budget: float) -> List[List[Dict]]:
195      """ลบ POI ที่ ratio score/cost ต่ำที่สุดออก จนกว่าจะ valid
196      หรือ chromosome ว่าง"""
197      result = evaluate_route(chromosome, hotel, budget)
198      max_iter = 50
199      while not result['valid'] and max_iter > 0:
200          worst_d, worst_i = None, None
201          worst_ratio = float('inf')
202          for d, day in enumerate(chromosome):
203              for i, poi in enumerate(day):
204                  ratio = poi['score'] / (poi['cost'] + 1.0)
205                  if ratio < worst_ratio:
206                      worst_ratio = ratio
207                      worst_d, worst_i = d, i
208          if worst_d is None:
209              break
210          chromosome[worst_d].pop(worst_i)
211          result = evaluate_route(chromosome, hotel, budget)
212          max_iter -= 1
213      return chromosome
บรรทัด 193–194: ประกาศ repair
บรรทัด 195–196: docstring: ลบจุดที่อัตราส่วนคะแนนต่อต้นทุนต่ำสุดจนกว่าแผนจะ valid
บรรทัด 197: ประเมินแผน
บรรทัด 198: จำกัดไม่เกิน 50 รอบ
บรรทัด 199: วนตราบที่ยังไม่ valid และยังมีรอบเหลือ
บรรทัด 200–201: ตั้งค่าตัวติดตามจุดที่แย่ที่สุด
บรรทัด 202–207: ไล่ทุกจุด คำนวณ score/(cost+1) เก็บจุดที่ต่ำสุด
บรรทัด 208–209: ถ้าไม่มีจุดให้ลบ หยุด
บรรทัด 210–212: ลบจุดนั้น ประเมินใหม่ ลดตัวนับรอบ
บรรทัด 213: คืนแผนที่ซ่อมแล้ว
บรรทัด 219–265  ลูปหลักของ GA
219  def genetic_solve(pois: List[Dict], hotel: Dict, days: int, budget: float,
220                    pop_size: int = 50, generations: int = 100,
221                    mutation_rate: float = 0.3, verbose: bool = False
222                    ) -> Tuple[List[List[Dict]], List[float]]:
223      """แก้ปัญหา B-TOPTW ด้วย Genetic Algorithm
224
225      Returns: (best_chromosome, history of best_fitness per gen)
226      """
227      population = initial_population(pois, hotel, days, budget, pop_size)
228      fitnesses = [fitness(c, hotel, budget) for c in population]
229
230      best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
231      best_chromosome = copy.deepcopy(population[best_idx])
232      best_fitness = fitnesses[best_idx]
233      history = [best_fitness]
234
235      for gen in range(generations):
236          new_pop = [copy.deepcopy(best_chromosome)]  # elitism — เก็บ best chromosome ไว้
237
238          while len(new_pop) < pop_size:
239              p1 = tournament_select(population, fitnesses)
240              p2 = tournament_select(population, fitnesses)
241              child = crossover(p1, p2)
242              child = mutate(child, pois, mutation_rate)
243              child = repair(child, hotel, budget)
244              new_pop.append(child)
245
246          population = new_pop
247          fitnesses = [fitness(c, hotel, budget) for c in population]
248
249          cur_best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
250          if fitnesses[cur_best_idx] > best_fitness:
251              best_fitness = fitnesses[cur_best_idx]
252              best_chromosome = copy.deepcopy(population[cur_best_idx])
253
254          history.append(best_fitness)
255          if verbose and gen % 20 == 0:
256              print(f"  Gen {gen:3d}: best fitness = {best_fitness:.2f}")
257
258      # รับประกัน lunch + dinner ครบทุกวัน
259      best_chromosome = meal_fill(best_chromosome, pois, hotel, budget)
260
261      # ลบ attr ออกจากวันที่ยังเกินเวลา
262      from hybrid import _time_repair
263      best_chromosome = _time_repair(best_chromosome, hotel)
264
265      return best_chromosome, history
บรรทัด 219–222: ประกาศ genetic_solve (ประชากร 50 รุ่นละ 100 mutation 0.3 ตามค่าตั้งต้น) คืนแผนที่ดีที่สุดและประวัติ fitness
บรรทัด 223–226: docstring
บรรทัด 227: สร้างประชากรเริ่มต้น
บรรทัด 228: คำนวณ fitness ของทุกตัว
บรรทัด 230–233: เก็บตัวที่ดีที่สุดเริ่มต้น (best chromosome) และ fitness ของมัน
บรรทัด 233: history เก็บ fitness ที่ดีที่สุดของแต่ละรุ่น
บรรทัด 235: วนตามจำนวนรุ่น
บรรทัด 236: elitism: ใส่ตัวที่ดีที่สุดไว้ในรุ่นถัดไปเสมอ
บรรทัด 238–244: สร้างลูกจนครบประชากร: เลือกพ่อแม่ด้วย tournament สองครั้ง crossover แล้ว mutate แล้ว repair
บรรทัด 246–247: แทนที่ประชากรด้วยรุ่นใหม่ และคำนวณ fitness ใหม่
บรรทัด 249–252: ถ้ารุ่นนี้มีตัวที่ดีกว่าเดิม ปรับ best
บรรทัด 254: บันทึกประวัติ
บรรทัด 255–256: ถ้าเปิด verbose พิมพ์ผลทุก 20 รุ่น
บรรทัด 258–259: รับประกันมื้ออาหารด้วย ➜ meal_fill() ใน algorithm/hybrid.py
บรรทัด 261–263: ถอดจุดเที่ยวที่ทำให้เกินเวลาด้วย ➜ _time_repair() ใน algorithm/hybrid.py
บรรทัด 265: คืนแผนและประวัติ
บรรทัด 268–302  ฟังก์ชันทดสอบ (main)
268  def main():
269      from utils import load_data, print_result
270      random.seed(42)
271      pois, hotels = load_data('../data/provinces/phuket.json')
272      hotel = hotels[1]  # Novotel Karon
273
274      print(f"\n{'=' * 60}")
275      print(f"  Genetic Algorithm Test")
276      print(f"{'=' * 60}")
277      print(f"  Hotel:  {hotel['name_en']}")
278      print(f"  POIs:   {len(pois)}")
279      print(f"  Days:   3")
280      print(f"  Budget: 15,000 บาท")
281      print(f"  Population: 50, Generations: 100, Mutation: 0.3")
282      print(f"\n  Running GA...")
283
284      days = 3
285      budget = 15000
286
287      t0 = time.time()
288      routes, history = genetic_solve(pois, hotel, days, budget,
289                                      pop_size=50, generations=100,
290                                      mutation_rate=0.3, verbose=True)
291      elapsed_ms = (time.time() - t0) * 1000
292
293      result = evaluate_route(routes, hotel, budget)
294      print_result(result, label='GA Result', elapsed_ms=elapsed_ms)
295
296      print(f"\n  Convergence: gen 0 fitness = {history[0]:.1f}, "
297            f"final = {history[-1]:.1f}, "
298            f"improvement = {history[-1] - history[0]:.1f}")
299
300
301  if __name__ == '__main__':
302      main()
บรรทัด 268–271: ประกาศ main สำหรับรันไฟล์นี้ตรง ๆ ทดสอบ GA
บรรทัด 272–274: เตรียม seed สุ่ม 42 โหลดข้อมูลภูเก็ตด้วย ➜ load_data() ใน algorithm/utils.py และเลือกโรงแรมที่ 2
บรรทัด 276–283: พิมพ์ข้อมูลการทดสอบ
บรรทัด 284–285: ตั้งจำนวนวัน 3 และงบ 15,000 บาท
บรรทัด 287–291: จับเวลาและรัน genetic_solve
บรรทัด 293–294: ประเมินและพิมพ์ผลด้วย ➜ print_result() ใน algorithm/utils.py
บรรทัด 296–298: พิมพ์การลู่เข้า (fitness รุ่นแรกเทียบรุ่นสุดท้าย)
บรรทัด 301–302: เรียก main() เมื่อรันไฟล์นี้โดยตรง

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/greedy.py
algorithm/hybrid.py
algorithm/utils.py