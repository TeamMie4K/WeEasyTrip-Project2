<!-- converted from experiments__run_province_experiments.py.docx -->

คู่มือโค้ด: experiments/run_province_experiments.py
การทดลองหลักบทที่ 4: เปรียบเทียบอัลกอริทึมใน 4 จังหวัด และจำลองผู้ใช้แก้แผน
ไฟล์ต้นฉบับ: experiments/run_province_experiments.py (199 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์ทดลองหลักที่สร้างตาราง 4.2 4.3 และ 4.4 ในรายงาน ส่วน A เปรียบเทียบ Greedy GA Hybrid และ Hybrid+Div ใน 4 จังหวัด × 3 สถานการณ์ ส่วน B จำลองผู้ใช้ลบ 2 จุดและสลับ 1 จุด แล้วเทียบ "คำนวณใหม่แบบเดิม" กับ "ปรับแผนด้วย Hybrid" ไฟล์นี้ยังเป็นโมดูลช่วย (setup, SCENARIOS, PROVINCES, HYBRID_PARAMS) ที่สคริปต์ทดลองอื่นนำเข้าไปใช้ เช่น ➜ experiments/run_pareto_experiments.py ➜ experiments/train_rl.py ผลบันทึกที่ results/province_results.json และ province_stats.txt

บรรทัด 1–33  หัวไฟล์ นำเข้า และตั้งค่าการทดลอง
1  # -*- coding: utf-8 -*-
2  """
3  run_province_experiments.py — WeEasyTrip Project 2
4  ส่วน A: Greedy / GA / Hybrid × 3 scenarios × 4 จังหวัด (ขยายจาก run_experiments.py ของ Project 1)
5  ส่วน B: จำลองผู้ใช้แก้แผน (ลบ 2 จุด + สลับ 1 จุด) เทียบ recompute เดิม (ไม่ปรับเส้นทาง) กับ reoptimize_solve ใหม่
6          ทดสอบด้วย Wilcoxon signed-rank (paired)
7  ผลลัพธ์: results/province_results.json, results/province_stats.txt
8  รัน:  python run_province_experiments.py [trials]
9  """
10  import sys, os, time, json, random, statistics
11  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'algorithm'))
12  from scipy import stats as st
13
14  from utils import load_data, evaluate_route, set_travel_profile
15  from greedy import greedy_solve
16  from genetic import genetic_solve
17  from hybrid import hybrid_solve, reoptimize_solve, diversity_stats
18
19  ROOT = os.path.join(os.path.dirname(__file__), '..')
20  OUT_DIR = os.path.join(os.path.dirname(__file__), 'results')
21  os.makedirs(OUT_DIR, exist_ok=True)
22  PROVINCES = ['phuket', 'chiangmai', 'krabi', 'samui']
23  TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 15
24
25  # hotel_frac = ตำแหน่งโรงแรมในรายการที่เรียงตามราคา (เทียบเท่า index 2/7/12 จาก 20 โรงแรมของ Project 1)
26  SCENARIOS = [
27      {'label': 'S1_Short_Budget',    'budget': 10_000, 'days': 3, 'hotel_frac': 0.10, 'mode': 'ratio'},
28      {'label': 'S2_Medium_Standard', 'budget': 15_000, 'days': 5, 'hotel_frac': 0.35, 'mode': 'ratio'},
29      {'label': 'S3_Long_Premium',    'budget': 25_000, 'days': 7, 'hotel_frac': 0.60, 'mode': 'quality'},
30  ]
31  DIV_W = 1.5   # น้ำหนักความหลากหลายใน Hybrid+Div (ตรงกับ DIVERSITY_WEIGHT ใน backend)
32  GA_PARAMS = dict(pop_size=50, generations=100, mutation_rate=0.3)
33  HYBRID_PARAMS = dict(pop_size=30, generations=60, mutation_rate=0.3)
บรรทัด 1–9: docstring: ส่วน A เทียบอัลกอริทึม ส่วน B จำลองผู้ใช้แก้แผน ทดสอบด้วย Wilcoxon แบบจับคู่ ผลอยู่ใน results/ วิธีรัน python run_province_experiments.py [จำนวนรอบ]
บรรทัด 10: นำเข้าโมดูลมาตรฐาน
บรรทัด 11: เพิ่มโฟลเดอร์ algorithm/ เข้า path
บรรทัด 12: นำเข้า scipy.stats สำหรับการทดสอบทางสถิติ
บรรทัด 14: นำเข้า ➜ load_data() ใน algorithm/utils.py ➜ evaluate_route() ใน algorithm/utils.py และ ➜ set_travel_profile() ใน algorithm/utils.py
บรรทัด 15–17: นำเข้าอัลกอริทึม ➜ greedy_solve() ใน algorithm/greedy.py ➜ genetic_solve() ใน algorithm/genetic.py ➜ hybrid_solve() ใน algorithm/hybrid.py ➜ reoptimize_solve() ใน algorithm/hybrid.py และ ➜ diversity_stats() ใน algorithm/hybrid.py
บรรทัด 19–21: ROOT ราก repo OUT_DIR โฟลเดอร์ผลลัพธ์ และสร้างโฟลเดอร์ถ้ายังไม่มี
บรรทัด 22: PROVINCES 4 จังหวัดหลักที่ทดลอง
บรรทัด 23: TRIALS จำนวนรอบต่อชุด (จากอาร์กิวเมนต์แรก ตั้งต้น 15)
บรรทัด 25–30: SCENARIOS สามสถานการณ์ S1 (3 วัน 10,000 บาท) S2 (5 วัน 15,000 บาท) S3 (7 วัน 25,000 บาท) พร้อมตำแหน่งโรงแรมในรายการเรียงตามราคา (hotel_frac) และโหมดคะแนน
บรรทัด 31: DIV_W = 1.5 น้ำหนักความหลากหลายของ Hybrid+Div (ตรงกับ DIVERSITY_WEIGHT ใน ➜ backend/main.py)
บรรทัด 32–33: พารามิเตอร์ของ GA (ประชากร 50 รุ่น 100) และของ Hybrid (ประชากร 30 รุ่น 60)
บรรทัด 36–51  โปรไฟล์จังหวัดและฟังก์ชัน `setup`
36  PROV_CFG = json.load(open(os.path.join(ROOT, 'data', 'provinces.json'), encoding='utf-8'))
37  USE_TRAVEL_PROFILE = '--no-profile' not in sys.argv
38
39
40  def setup(prov, sc):
41      cfg = PROV_CFG[prov]
42      if USE_TRAVEL_PROFILE:
43          set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
44      else:
45          set_travel_profile()
46      pois, hotels = load_data(os.path.join(ROOT, 'data', 'provinces', f'{prov}.json'))
47      hs = sorted(hotels, key=lambda h: h['cost'])
48      hotel = hs[int(len(hs) * sc['hotel_frac'])]
49      nights = max(1, sc['days'] - 1)
50      act = max(0.0, sc['budget'] - hotel['cost'] * nights)
51      return pois, hotel, act
บรรทัด 36: โหลดโปรไฟล์จังหวัดจาก data/provinces.json (ตัวคูณถนน ความเร็ว) ที่ได้จาก ➜ data/calibrate_travel.py
บรรทัด 37: ธง USE_TRAVEL_PROFILE ปิดได้ด้วย --no-profile เพื่อเทียบแบบเส้นตรง
บรรทัด 40–41: ประกาศ setup รับชื่อจังหวัดและสถานการณ์
บรรทัด 42–45: ตั้งโปรไฟล์เดินทางของจังหวัดด้วย ➜ set_travel_profile() ใน algorithm/utils.py (หรือใช้ค่าตั้งต้นถ้าปิดโปรไฟล์)
บรรทัด 46: โหลดจุดและโรงแรมของจังหวัด
บรรทัด 47–48: เรียงโรงแรมตามราคาและเลือกตามตำแหน่ง hotel_frac
บรรทัด 49–50: จำนวนคืนและงบกิจกรรม = งบรวม − ค่าโรงแรม
บรรทัด 51: คืน (จุด โรงแรม งบกิจกรรม)
บรรทัด 54–73  ตัวช่วยรันอัลกอริทึม
54  def min_meals(routes):
55      return min((sum(1 for p in d if p['category'] == 'restaurant') for d in routes), default=0)
56
57
58  def run_algo(algo, pois, hotel, days, act, mode, seed):
59      random.seed(seed)
60      t0 = time.perf_counter()
61      if algo == 'Greedy':
62          routes = greedy_solve(pois, hotel, days, act, scoring_mode=mode)
63      elif algo == 'GA':
64          routes, _ = genetic_solve(pois, hotel, days, act, **GA_PARAMS)
65      else:   # 'Hybrid' = แบบ Project 1 (ไม่มี diversity), 'HybridDiv' = เพิ่ม diversity ใน fitness
66          w = DIV_W if algo == 'HybridDiv' else 0.0
67          routes, _ = hybrid_solve(pois, hotel, days, act, scoring_mode=mode, diversity_weight=w, **HYBRID_PARAMS)
68      ms = (time.perf_counter() - t0) * 1000
69      ev = evaluate_route(routes, hotel, act)
70      dv, over = diversity_stats(routes)
71      return routes, {'score': ev['total_score'], 'valid': ev['valid'], 'time_ms': round(ms, 1),
72                      'meals_ok': min_meals(routes) >= 2, 'diversity': dv, 'over': over,
73                      'km_day': sum(d['distance_km'] for d in ev['days_detail']) / max(days, 1)}
บรรทัด 54–55: min_meals จำนวนร้านอาหารน้อยที่สุดต่อวัน (ใช้ตรวจว่ามื้อครบ)
บรรทัด 58–60: run_algo ตั้ง seed แล้วเริ่มจับเวลา
บรรทัด 61–62: ถ้าเป็น Greedy เรียก ➜ greedy_solve() ใน algorithm/greedy.py
บรรทัด 63–64: ถ้าเป็น GA เรียก ➜ genetic_solve() ใน algorithm/genetic.py
บรรทัด 65–67: อื่น ๆ คือ Hybrid (w=0 แบบ Project 1) หรือ HybridDiv (w=1.5) เรียก ➜ hybrid_solve() ใน algorithm/hybrid.py
บรรทัด 68–70: คำนวณเวลาและประเมินแผนด้วย ➜ evaluate_route() ใน algorithm/utils.py พร้อมสถิติความหลากหลาย
บรรทัด 71–73: คืนแผนและตัวชี้วัด: คะแนน ความถูกต้อง เวลา มื้อครบหรือไม่ ความหลากหลาย การซ้ำหมวดเกิน และระยะขับเฉลี่ยต่อวัน
บรรทัด 76–79  สรุปสถิติ
76  def summarize(vals):
77      return {'mean': round(statistics.mean(vals), 2),
78              'stdev': round(statistics.stdev(vals), 2) if len(vals) > 1 else 0.0,
79              'min': round(min(vals), 2), 'max': round(max(vals), 2)}
บรรทัด 76–79: summarize คืนค่าเฉลี่ย ส่วนเบี่ยงเบนมาตรฐาน ต่ำสุด สูงสุด ของรายการค่า
บรรทัด 82–107  ส่วน A: เทียบอัลกอริทึม
82  def part_a():
83      res = {}
84      for prov in PROVINCES:
85          for sc in SCENARIOS:
86              pois, hotel, act = setup(prov, sc)
87              key = f"{prov}/{sc['label']}"
88              res[key] = {'hotel': hotel['id'], 'act_budget': act}
89              groups = {}
90              for algo in ('Greedy', 'GA', 'Hybrid', 'HybridDiv'):
91                  n = 1 if algo == 'Greedy' else TRIALS
92                  trials = [run_algo(algo, pois, hotel, sc['days'], act, sc['mode'], seed=t)[1] for t in range(n)]
93                  groups[algo] = [t['score'] for t in trials]
94                  res[key][algo] = {
95                      'n': n, 'score': summarize(groups[algo]),
96                      'time_ms': summarize([t['time_ms'] for t in trials])['mean'],
97                      'valid': sum(t['valid'] for t in trials), 'meals_ok': sum(t['meals_ok'] for t in trials),
98                      'km_day': round(statistics.mean(t['km_day'] for t in trials), 1),
99                      'diversity': round(statistics.mean(t['diversity'] for t in trials), 2),
100                      'over': round(statistics.mean(t['over'] for t in trials), 2)}
101              h = st.kruskal(groups['GA'], groups['Hybrid'])
102              mw = st.mannwhitneyu(groups['Hybrid'], groups['GA'], alternative='greater')
103              res[key]['hybrid_vs_ga'] = {'kruskal_p': float(h.pvalue), 'mwu_greater_p': float(mw.pvalue)}
104              dv = st.mannwhitneyu(groups['HybridDiv'], groups['Hybrid'], alternative='two-sided')
105              res[key]['div_vs_hybrid'] = {'mwu_two_sided_p': float(dv.pvalue)}
106              print(key, {a: res[key][a]['score']['mean'] for a in ('Greedy', 'GA', 'Hybrid', 'HybridDiv')}, flush=True)
107      return res
บรรทัด 82–86: ประกาศ part_a วนทุกจังหวัดและสถานการณ์ ตั้งค่าด้วย setup
บรรทัด 87–88: คีย์ผลลัพธ์ จังหวัด/สถานการณ์ พร้อมโรงแรมและงบกิจกรรม
บรรทัด 89–93: วนสี่อัลกอริทึม (Greedy รันครั้งเดียวเพราะกำหนดแน่นอน ที่เหลือรันตามจำนวนรอบ ใช้ seed ตามลำดับรอบ) เก็บคะแนนของแต่ละรอบ
บรรทัด 94–100: สรุปผลของอัลกอริทึมนั้น: คะแนน เวลา จำนวนรอบที่ valid และมื้อครบ ระยะขับ ความหลากหลาย
บรรทัด 101–103: ทดสอบ Kruskal-Wallis และ Mann-Whitney ทางเดียว (Hybrid มากกว่า GA)
บรรทัด 104–105: ทดสอบสองทาง Hybrid+Div เทียบ Hybrid
บรรทัด 106: พิมพ์คะแนนเฉลี่ย
บรรทัด 107: คืนผลทั้งหมด
บรรทัด 110–164  ส่วน B: จำลองผู้ใช้แก้แผน
110  def part_b():
111      res = {}
112      for prov in PROVINCES:
113          for sc in SCENARIOS:
114              pois, hotel, act = setup(prov, sc)
115              rows = []
116              for t in range(TRIALS):
117                  routes, _ = run_algo('HybridDiv', pois, hotel, sc['days'], act, sc['mode'], seed=t)
118                  rng = random.Random(1000 + t)
119                  flat = [(d, p['id']) for d, day in enumerate(routes) for p in day]
120                  removed = [pid for _, pid in rng.sample(flat, min(2, len(flat)))]
121                  edited = [[p for p in day if p['id'] not in removed] for day in routes]
122                  used = {p['id'] for day in edited for p in day} | set(removed)
123                  attrs_free = [p for p in pois if p['category'] != 'restaurant' and p['id'] not in used]
124                  slots = [(d, i) for d, day in enumerate(edited) for i, p in enumerate(day) if p['category'] != 'restaurant']
125                  locked = []
126                  if slots and attrs_free:
127                      d, i = rng.choice(slots)
128                      new = rng.choice(attrs_free)
129                      edited[d][i] = new
130                      locked = [new['id']]
131                  # A) ระบบเดิม: ใช้แผนที่แก้ตรง ๆ ไม่ปรับเส้นทาง
132                  evA = evaluate_route(edited, hotel, act)
133                  A = {'score': evA['total_score'], 'valid': evA['valid'], 'meals_ok': min_meals(edited) >= 2}
134                  A['adj'] = A['score'] if A['valid'] else 0.0   # แผนที่ผิดข้อจำกัดใช้งานไม่ได้ → นับเป็น 0
135                  # B) ใหม่: reoptimize
136                  random.seed(t)
137                  t0 = time.perf_counter()
138                  newr = reoptimize_solve(pois, hotel, edited, act, locked_ids=locked, excluded_ids=removed,
139                                          scoring_mode=sc['mode'], diversity_weight=DIV_W)
140                  ms = (time.perf_counter() - t0) * 1000
141                  evB = evaluate_route(newr, hotel, act)
142                  ids = {p['id'] for day in newr for p in day}
143                  B = {'score': evB['total_score'], 'valid': evB['valid'], 'meals_ok': min_meals(newr) >= 2,
144                       'adj': evB['total_score'] if evB['valid'] else 0.0,
145                       'locked_kept': set(locked) <= ids, 'excluded_absent': not (set(removed) & ids), 'time_ms': ms}
146                  rows.append({'A': A, 'B': B})
147              sa = [r['A']['score'] for r in rows]; sb = [r['B']['score'] for r in rows]
148              aa = [r['A']['adj'] for r in rows]; ab = [r['B']['adj'] for r in rows]
149              try:
150                  w = st.wilcoxon(ab, aa, alternative='greater').pvalue
151              except ValueError:
152                  w = 1.0
153              key = f"{prov}/{sc['label']}"
154              res[key] = {
155                  'recompute': {'score': summarize(sa), 'adj_mean': round(statistics.mean(aa), 2), 'valid': sum(r['A']['valid'] for r in rows),
156                                'meals_ok': sum(r['A']['meals_ok'] for r in rows)},
157                  'reoptimize': {'score': summarize(sb), 'adj_mean': round(statistics.mean(ab), 2), 'valid': sum(r['B']['valid'] for r in rows),
158                                 'meals_ok': sum(r['B']['meals_ok'] for r in rows),
159                                 'locked_kept': sum(r['B']['locked_kept'] for r in rows),
160                                 'excluded_absent': sum(r['B']['excluded_absent'] for r in rows),
161                                 'time_ms': round(statistics.mean(r['B']['time_ms'] for r in rows), 1)},
162                  'n': len(rows), 'wilcoxon_greater_p': float(w)}
163              print('B', key, 'recompute', res[key]['recompute']['score']['mean'], 'reopt', res[key]['reoptimize']['score']['mean'], flush=True)
164      return res
บรรทัด 110–115: ประกาศ part_b วนทุกจังหวัดและสถานการณ์ เตรียมดัชนีจุด
บรรทัด 116–117: วนแต่ละรอบ สร้างแผนด้วย HybridDiv
บรรทัด 118–121: จำลองการแก้: สุ่มลบ 2 จุด (seed ตามรอบ) ได้แผนที่ถูกแก้
บรรทัด 122–130: สุ่มสลับที่เที่ยวหนึ่งจุดเป็นจุดใหม่ที่ยังไม่ใช้ และจดเป็นจุดล็อก (ผู้ใช้เลือกเอง)
บรรทัด 131–134: วิธี A (ระบบเดิม) ใช้แผนที่แก้ตรง ๆ ไม่ปรับเส้นทาง ถ้าผิดข้อจำกัดนับคะแนนเป็น 0
บรรทัด 135–145: วิธี B ใหม่ เรียก ➜ reoptimize_solve() ใน algorithm/hybrid.py พร้อมจุดล็อกและจุดที่ลบ เก็บคะแนน ความถูกต้อง มื้อครบ จุดล็อกยังอยู่ และจุดที่ลบไม่กลับมา
บรรทัด 146: เก็บผล A และ B ของรอบนี้
บรรทัด 147–152: ทดสอบ Wilcoxon แบบจับคู่ (B มากกว่า A) ถ้าข้อมูลทดสอบไม่ได้ให้ p = 1
บรรทัด 153–163: สรุปผลของชุดนี้ลงพจนานุกรมและพิมพ์
บรรทัด 164: คืนผลทั้งหมด
บรรทัด 167–190  เขียนรายงานข้อความ
167  def write_report(a, b):
168      L = ['=' * 100, f'PROJECT 2 EXPERIMENTS — 4 provinces, trials={TRIALS} (Greedy deterministic = 1), travel profile={USE_TRAVEL_PROFILE}', '=' * 100,
169           '', 'PART A: mean score  |  Hybrid = Project 1 fitness, Hybrid+Div = + diversity (w=%.1f)' % DIV_W, '']
170      L.append(f"{'Province/Scenario':<28}{'Greedy':>7}{'GA':>7}{'Hybrid':>8}{'Hyb+Div':>8}{'valid':>7}{'meals':>7}{'div H':>7}{'div HD':>7}{'ms HD':>7}{'p(H>GA)':>9}{'p(HD~H)':>9}")
171      for k, v in a.items():
172          L.append(f"{k:<28}{v['Greedy']['score']['mean']:>7.1f}{v['GA']['score']['mean']:>7.1f}{v['Hybrid']['score']['mean']:>8.1f}{v['HybridDiv']['score']['mean']:>8.1f}"
173                   f"{str(v['HybridDiv']['valid'])+'/'+str(v['HybridDiv']['n']):>7}{str(v['HybridDiv']['meals_ok'])+'/'+str(v['HybridDiv']['n']):>7}"
174                   f"{v['Hybrid']['diversity']:>7.2f}{v['HybridDiv']['diversity']:>7.2f}{v['HybridDiv']['time_ms']:>7.0f}"
175                   f"{v['hybrid_vs_ga']['mwu_greater_p']:>9.4f}{v['div_vs_hybrid']['mwu_two_sided_p']:>9.4f}")
176      L += ['', 'PART A2: ระยะขับเฉลี่ยต่อวัน (km/วัน) — ยิ่งน้อยยิ่งสมจริง/ปฏิบัติตามได้', f"{'Province/Scenario':<28}{'Greedy':>8}{'GA':>8}{'Hybrid':>8}{'Hyb+Div':>9}"]
177      for k, v in a.items():
178          L.append(f"{k:<28}{v['Greedy']['km_day']:>8.1f}{v['GA']['km_day']:>8.1f}{v['Hybrid']['km_day']:>8.1f}{v['HybridDiv']['km_day']:>9.1f}")
179      L += ['', 'PART B: after user edit (delete 2 + swap 1): recompute-only (A) vs reoptimize (B); adj = score if valid else 0', '']
180      L.append(f"{'Province/Scenario':<30}{'adjA':>8}{'adjB':>8}{'valid A':>9}{'valid B':>9}{'meals A':>9}{'meals B':>9}{'lock':>6}{'excl':>6}{'ms':>7}{'p(B>A)':>9}")
181      for k, v in b.items():
182          n = v['n']
183          L.append(f"{k:<30}{v['recompute']['adj_mean']:>8.1f}{v['reoptimize']['adj_mean']:>8.1f}"
184                   f"{str(v['recompute']['valid'])+'/'+str(n):>9}{str(v['reoptimize']['valid'])+'/'+str(n):>9}"
185                   f"{str(v['recompute']['meals_ok'])+'/'+str(n):>9}{str(v['reoptimize']['meals_ok'])+'/'+str(n):>9}"
186                   f"{str(v['reoptimize']['locked_kept'])+'/'+str(n):>6}{str(v['reoptimize']['excluded_absent'])+'/'+str(n):>6}"
187                   f"{v['reoptimize']['time_ms']:>7.0f}{v['wilcoxon_greater_p']:>9.4f}")
188      txt = '\n'.join(L)
189      print('\n' + txt)
190      open(os.path.join(OUT_DIR, 'province_stats.txt'), 'w', encoding='utf-8').write(txt)
บรรทัด 167–170: ประกาศ write_report เตรียมหัวตารางส่วน A
บรรทัด 171–175: เพิ่มบรรทัดของแต่ละชุดในส่วน A (คะแนน 4 อัลกอริทึม ความถูกต้อง มื้อครบ ความหลากหลาย เวลา ค่า p)
บรรทัด 176–178: ส่วน A2 ระยะขับเฉลี่ยต่อวัน (ใช้สร้างตาราง 4.3)
บรรทัด 179–187: ส่วน B (ใช้สร้างตาราง 4.4): คะแนนปรับ ความถูกต้อง มื้อครบ จุดล็อก/จุดลบ เวลา และค่า p
บรรทัด 188–190: รวมเป็นข้อความ พิมพ์ และบันทึกเป็น results/province_stats.txt ซึ่งถูกนำไปเติมตารางของรายงาน
บรรทัด 193–199  จุดเริ่มต้น
193  if __name__ == '__main__':
194      only_b = 'b' in sys.argv[2:]
195      a = json.load(open(os.path.join(OUT_DIR, 'province_results.json'), encoding='utf-8'))['part_a'] if only_b else part_a()
196      b = part_b()
197      json.dump({'trials': TRIALS, 'part_a': a, 'part_b': b},
198                open(os.path.join(OUT_DIR, 'province_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
199      write_report(a, b)
บรรทัด 193–196: ถ้าสั่งรันเฉพาะส่วน B (อาร์กิวเมนต์ b) อ่านผลส่วน A เดิมจากไฟล์ ไม่เช่นนั้นรันส่วน A ใหม่ แล้วรันส่วน B
บรรทัด 197–199: บันทึก results/province_results.json และเขียนรายงานข้อความ

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
algorithm/utils.py
backend/main.py
data/calibrate_travel.py
experiments/run_pareto_experiments.py
experiments/train_rl.py