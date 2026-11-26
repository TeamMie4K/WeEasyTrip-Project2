<!-- converted from experiments__run_experiments.py.docx -->

คู่มือโค้ด: experiments/run_experiments.py
การทดลองของ Project 1: Greedy / GA / Hybrid บนภูเก็ต (30 รอบ × 3 สถานการณ์)
ไฟล์ต้นฉบับ: experiments/run_experiments.py (335 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์ทดลองรุ่น Project 1 ที่สร้างตาราง 4.1 และภาคผนวก ข ในรายงาน (ผลของ Project 1 ไม่ถูกแทนที่ด้วยผลของ Project 2) รัน 3 อัลกอริทึม × 3 สถานการณ์ ทดสอบ Kruskal-Wallis ที่เขียนสูตรเอง เขียนสถิติลง results/stats.txt และวาดกราฟ convergence ใช้ ➜ algorithm/greedy.py ➜ algorithm/genetic.py ➜ algorithm/hybrid.py และตัวตรวจแผนจาก ➜ algorithm/utils.py ฉบับ Project 2 ใช้ ➜ experiments/run_province_experiments.py แทน

บรรทัด 1–19  หัวไฟล์ นำเข้า และค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  run_experiments.py — WeEasyTrip (Thesis)
4  Runs 30 trials × 3 algorithms × 3 scenarios
5  Outputs: results/results.json, results/stats.txt, results/convergence.png
6  """
7  import sys, os, time, json, random, statistics, math
8  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'algorithm'))
9
10  from utils import load_data, evaluate_route
11  from greedy import greedy_solve
12  from genetic import genetic_solve
13  from hybrid import hybrid_solve
14
15  DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'provinces', 'phuket.json')
16  OUT_DIR   = os.path.join(os.path.dirname(__file__), 'results')
17  os.makedirs(OUT_DIR, exist_ok=True)
18
19  TRIALS = 30
บรรทัด 1–6: docstring: รัน 30 รอบ × 3 อัลกอริทึม × 3 สถานการณ์ ผลที่ results.json stats.txt และ convergence.png
บรรทัด 7–8: นำเข้าโมดูลมาตรฐานและเพิ่มโฟลเดอร์ algorithm/ เข้า path
บรรทัด 10–13: นำเข้า ➜ load_data() ใน algorithm/utils.py ➜ evaluate_route() ใน algorithm/utils.py ➜ greedy_solve() ใน algorithm/greedy.py ➜ genetic_solve() ใน algorithm/genetic.py และ ➜ hybrid_solve() ใน algorithm/hybrid.py
บรรทัด 15–17: พาธข้อมูลภูเก็ต โฟลเดอร์ผลลัพธ์ และสร้างโฟลเดอร์ถ้ายังไม่มี
บรรทัด 19: TRIALS = 30 จำนวนรอบของอัลกอริทึมที่สุ่ม
บรรทัด 21–52  นิยามสถานการณ์และพารามิเตอร์
21  # ============================================================
22  # Scenarios (ชุดการทดลอง)
23  # ============================================================
24  # S1: งบน้อย 3 วัน  — Hotel idx 2 (Anchalee Inn, 400/คืน × 2 = 800)
25  # S2: งบกลาง 5 วัน  — Hotel idx 7 (Ibis Phuket Patong, 1100/คืน × 4 = 4400)
26  # S3: งบสูง  7 วัน  — Hotel idx 12 (Novotel Surin, 2400/คืน × 6 = 14400)
27  SCENARIOS = [
28      {
29          'label':        'S1_Short_Budget',
30          'total_budget': 10_000,
31          'days':         3,
32          'hotel_idx':    2,
33          'scoring_mode': 'ratio',
34      },
35      {
36          'label':        'S2_Medium_Standard',
37          'total_budget': 15_000,
38          'days':         5,
39          'hotel_idx':    7,
40          'scoring_mode': 'ratio',
41      },
42      {
43          'label':        'S3_Long_Premium',
44          'total_budget': 25_000,
45          'days':         7,
46          'hotel_idx':    12,
47          'scoring_mode': 'quality',
48      },
49  ]
50
51  GA_PARAMS     = dict(pop_size=50, generations=100, mutation_rate=0.3)
52  HYBRID_PARAMS = dict(pop_size=30, generations=60,  mutation_rate=0.3)
บรรทัด 21–26: คอมเมนต์อธิบายโรงแรมของแต่ละสถานการณ์ (ดัชนีในรายการและค่าห้องรวม)
บรรทัด 27–49: SCENARIOS สามสถานการณ์: S1 งบน้อย 3 วัน 10,000 บาท S2 งบกลาง 5 วัน 15,000 บาท S3 งบสูง 7 วัน 25,000 บาท พร้อมดัชนีโรงแรมและโหมดคะแนน (ratio หรือ quality)
บรรทัด 51–52: พารามิเตอร์ GA (ประชากร 50 รุ่น 100) และ Hybrid (ประชากร 30 รุ่น 60)
บรรทัด 59–62  งบกิจกรรม
59  def activity_budget(sc, hotel):
60      """คำนวณงบกิจกรรม = total_budget − ค่าโรงแรมทั้งทริป"""
61      nights = max(1, sc['days'] - 1)
62      return max(0.0, sc['total_budget'] - hotel['cost'] * nights)
บรรทัด 59–62: activity_budget งบกิจกรรม = งบรวม − ค่าโรงแรมทั้งทริป
บรรทัด 65–87  รันหนึ่งรอบ
65  def run_one(algo, pois, hotel, days, act_budget, scoring_mode, seed):
66      """รัน 1 trial สำหรับ algorithm ที่กำหนด คืน dict (score, cost, valid, time_ms, history)"""
67      random.seed(seed)
68      t0 = time.perf_counter()
69
70      if algo == 'Greedy':
71          routes = greedy_solve(pois, hotel, days, act_budget, scoring_mode=scoring_mode)
72          history = None
73      elif algo == 'GA':
74          routes, history = genetic_solve(pois, hotel, days, act_budget, **GA_PARAMS)
75      else:  # Hybrid
76          routes, history = hybrid_solve(pois, hotel, days, act_budget,
77                                         scoring_mode=scoring_mode, **HYBRID_PARAMS)
78
79      elapsed_ms = (time.perf_counter() - t0) * 1000
80      ev = evaluate_route(routes, hotel, act_budget)
81      return {
82          'score':   ev['total_score'],
83          'cost':    ev['total_cost'],
84          'valid':   ev['valid'],
85          'time_ms': round(elapsed_ms, 1),
86          'history': history,
87      }
บรรทัด 65–67: ประกาศ run_one และตั้ง seed
บรรทัด 68: เริ่มจับเวลา
บรรทัด 70–72: Greedy: เรียก greedy_solve ไม่มีประวัติ
บรรทัด 73–74: GA: เรียก genetic_solve ได้แผนและประวัติ fitness
บรรทัด 75–77: Hybrid: เรียก hybrid_solve ได้แผนและประวัติ
บรรทัด 79–80: คำนวณเวลาและประเมินแผน
บรรทัด 81–87: คืนคะแนน ค่าใช้จ่าย ความถูกต้อง เวลา และประวัติ
บรรทัด 90–100  สถิติพื้นฐาน
90  def stats_summary(values):
91      """คำนวณสถิติพื้นฐาน (mean, median, stdev, min, max) ของชุดค่า float"""
92      if not values:
93          return {'mean': 0, 'median': 0, 'stdev': 0, 'min': 0, 'max': 0}
94      return {
95          'mean':   round(statistics.mean(values), 3),
96          'median': round(statistics.median(values), 3),
97          'stdev':  round(statistics.stdev(values) if len(values) > 1 else 0.0, 3),
98          'min':    round(min(values), 3),
99          'max':    round(max(values), 3),
100      }
บรรทัด 90–100: stats_summary คืนค่าเฉลี่ย มัธยฐาน ส่วนเบี่ยงเบนมาตรฐาน ต่ำสุด สูงสุด (คืนศูนย์ถ้าไม่มีข้อมูล)
บรรทัด 103–151  Kruskal-Wallis ที่เขียนเอง
103  def kruskal_wallis(groups):
104      """Kruskal-Wallis H-test (one-way ANOVA แบบ non-parametric)
105      ใช้เปรียบเทียบ distribution ของ 3 algorithm โดยไม่สมมติการแจกแจงปกติ
106      """
107      all_vals = []
108      group_labels = []
109      for gi, g in enumerate(groups):
110          all_vals.extend(g)
111          group_labels.extend([gi] * len(g))
112      n = len(all_vals)
113      if n < 3:
114          return 0.0, 1.0
115
116      # กำหนด rank ให้แต่ละค่า (ค่าเท่ากันใช้ rank เฉลี่ย)
117      sorted_idx = sorted(range(n), key=lambda i: all_vals[i])
118      ranks = [0.0] * n
119      i = 0
120      while i < n:
121          j = i
122          while j < n and all_vals[sorted_idx[j]] == all_vals[sorted_idx[i]]:
123              j += 1
124          avg_rank = (i + 1 + j) / 2.0
125          for k in range(i, j):
126              ranks[sorted_idx[k]] = avg_rank
127          i = j
128
129      # คำนวณค่าสถิติ H
130      H = 0.0
131      offset = 0
132      for g in groups:
133          if not g:
134              continue
135          group_ranks = ranks[offset:offset + len(g)]
136          R = sum(group_ranks)
137          H += (R ** 2) / len(g)
138          offset += len(g)
139      H = (12.0 / (n * (n + 1))) * H - 3 * (n + 1)
140
141      # ประมาณ p-value ด้วย chi-squared distribution, df = k-1
142      df = len([g for g in groups if g]) - 1
143      p = 1.0
144      if df > 0 and H > 0:
145          # ประมาณ chi-squared survival function
146          p = math.exp(-H / 2) * sum(
147              (H / 2) ** k / math.factorial(k)
148              for k in range(df)
149          ) if df <= 10 else max(0.0, 1.0 - (1 - math.exp(-H / 2)))
150          p = max(0.0, min(1.0, p))
151      return round(H, 4), round(p, 6)
บรรทัด 103–106: ประกาศ kruskal_wallis ทดสอบความต่างของการแจกแจงโดยไม่สมมติว่าปกติ
บรรทัด 107–115: รวมค่าทุกกลุ่มและจดว่ากลุ่มใด ถ้าข้อมูลน้อยกว่า 3 ค่าคืน (0, 1)
บรรทัด 116–127: จัดอันดับ (rank) ค่าเท่ากันใช้อันดับเฉลี่ย
บรรทัด 129–139: คำนวณสถิติ H จากผลรวมอันดับของแต่ละกลุ่ม
บรรทัด 141–150: ประมาณค่า p จากการแจกแจงไคกำลังสอง (df = จำนวนกลุ่ม − 1) ด้วยสูตรปิดสำหรับ df น้อย
บรรทัด 151: คืน (H, p)
บรรทัด 154–160  เฉลี่ยประวัติ fitness
154  def _avg_history(histories):
155      """เฉลี่ย fitness history จากหลาย trials ให้เป็น series เดียวสำหรับ plot"""
156      if not histories:
157          return []
158      max_len = max(len(h) for h in histories)
159      return [round(statistics.mean([h[i] for h in histories if i < len(h)]), 3)
160              for i in range(max_len)]
บรรทัด 154–160: _avg_history เฉลี่ย fitness ต่อรุ่นจากหลายรอบให้เป็นเส้นเดียวสำหรับวาดกราฟ
บรรทัด 167–238  ลูปทดลองหลัก
167  def main():
168      """รัน experiments ทั้งหมด: 3 scenarios × 3 algorithms × 30 trials
169      บันทึกผลเป็น results.json, stats.txt, convergence.png
170      """
171      pois, hotels = load_data(DATA_PATH)
172      print(f"Loaded {len(pois)} POIs, {len(hotels)} hotels\n")
173
174      all_results = {}
175      algos = ['Greedy', 'GA', 'Hybrid']
176
177      for sc in SCENARIOS:
178          hotel = hotels[sc['hotel_idx']]
179          act_b = activity_budget(sc, hotel)
180          nights = sc['days'] - 1
181          print(f"{'=' * 60}")
182          print(f"Scenario : {sc['label']}")
183          print(f"Hotel    : {hotel['id']} {hotel['name_en']} ({hotel['cost']}/night × {nights} = {hotel['cost'] * nights})")
184          print(f"Act.Bdgt : {act_b:.0f}  (total={sc['total_budget']})")
185          print(f"Days     : {sc['days']}")
186          sc_res = {}
187
188          for algo in algos:
189              n_trials = 1 if algo == 'Greedy' else TRIALS
190              print(f"  [{algo:6s}] ", end='', flush=True)
191              trials, histories = [], []
192
193              for t in range(n_trials):
194                  r = run_one(algo, list(pois), hotel, sc['days'],
195                              act_b, sc['scoring_mode'], seed=t)
196                  trials.append(r)
197                  if r['history']:
198                      histories.append(r['history'])
199                  print('.', end='', flush=True)
200
201              scores = [r['score'] for r in trials]
202              valid  = [r for r in trials if r['valid']]
203              times  = [r['time_ms'] for r in trials]
204              print(f"  score={statistics.mean(scores):.1f}"
205                    f"±{statistics.stdev(scores) if len(scores) > 1 else 0:.1f}"
206                    f"  valid={len(valid)}/{n_trials}"
207                    f"  time={statistics.mean(times):.0f}ms")
208
209              sc_res[algo] = {
210                  'n_trials':    n_trials,
211                  'valid_count': len(valid),
212                  'score_stats': stats_summary(scores),
213                  'time_stats':  stats_summary(times),
214                  'avg_history': _avg_history(histories),
215                  'trials': [{k: v for k, v in r.items() if k != 'history'} for r in trials],
216              }
217
218          # ทดสอบ Kruskal-Wallis เปรียบเทียบทั้ง 3 algorithm
219          groups = [[r['score'] for r in sc_res[a]['trials']] for a in algos]
220          H, p = kruskal_wallis(groups)
221          sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
222          print(f"  KW: H={H:.3f} p={p:.4f} {sig}\n")
223          sc_res['kruskal'] = {'H': H, 'p': p, 'sig': sig}
224          all_results[sc['label']] = sc_res
225
226      # บันทึกผลลัพธ์ทั้งหมดเป็น JSON
227      with open(os.path.join(OUT_DIR, 'results.json'), 'w', encoding='utf-8') as f:
228          json.dump(all_results, f, ensure_ascii=False, indent=2)
229
230      write_stats_report(all_results, algos, OUT_DIR)
231
232      try:
233          plot_convergence(all_results, algos, OUT_DIR)
234          print("Saved: results/convergence.png")
235      except Exception as e:
236          print(f"Plot skipped: {e}")
237
238      print_summary(all_results, algos)
บรรทัด 167–175: ประกาศ main โหลดข้อมูลภูเก็ตและเตรียมรายการอัลกอริทึม
บรรทัด 177–186: วนทุกสถานการณ์ เลือกโรงแรม คำนวณงบกิจกรรม และพิมพ์รายละเอียด
บรรทัด 188–199: วนทุกอัลกอริทึม (Greedy รันครั้งเดียว) ทุกรอบเรียก run_one ด้วย seed ตามลำดับและเก็บผล
บรรทัด 201–207: สรุปคะแนนเฉลี่ย ± ส่วนเบี่ยงเบน จำนวนที่ valid และเวลา
บรรทัด 209–216: เก็บสถิติคะแนน เวลา ประวัติเฉลี่ย และผลทุกรอบ
บรรทัด 218–224: ทดสอบ Kruskal-Wallis ระหว่างสามอัลกอริทึม แปลง p เป็นระดับนัยสำคัญ (***, **, *, ns)
บรรทัด 226–228: เขียน results/results.json
บรรทัด 230: เรียก write_stats_report
บรรทัด 232–236: วาดกราฟ convergence ถ้าล้มเหลวข้ามไป
บรรทัด 238: พิมพ์สรุปท้าย
บรรทัด 245–277  เขียนรายงานสถิติ
245  def write_stats_report(all_results, algos, out_dir):
246      """เขียนตารางสถิติเปรียบเทียบ algorithm ลงไฟล์ results/stats.txt"""
247      lines = [
248          "=" * 70,
249          "EXPERIMENT RESULTS — WeEasyTrip (Phuket B-TOPTW)",
250          f"Stochastic trials: {TRIALS}  |  Greedy: 1 (deterministic)",
251          f"GA params: pop=50, gen=100, mut=0.3",
252          f"Hybrid params: pop=30, gen=60, mut=0.3 + early-stop(15) + 2-opt",
253          "=" * 70,
254      ]
255      for sc_label, sc_data in all_results.items():
256          lines.append(f"\n[ {sc_label} ]")
257          lines.append(f"{'Algorithm':<10} {'Mean':>8} {'Std':>8} {'Max':>8} "
258                       f"{'Min':>8} {'Time(ms)':>10} {'Valid':>6}")
259          lines.append("-" * 62)
260          for algo in algos:
261              d  = sc_data[algo]
262              ss = d['score_stats']
263              ts = d['time_stats']
264              lines.append(
265                  f"{algo:<10} {ss['mean']:>8.2f} {ss['stdev']:>8.2f} "
266                  f"{ss['max']:>8.2f} {ss['min']:>8.2f} "
267                  f"{ts['mean']:>10.1f} {d['valid_count']:>3}/{d['n_trials']:<3}"
268              )
269          kw = sc_data['kruskal']
270          lines.append(f"  Kruskal-Wallis: H={kw['H']:.3f}  p={kw['p']:.4f}  {kw['sig']}")
271
272      report = "\n".join(lines)
273      print("\n" + report)
274      path = os.path.join(out_dir, 'stats.txt')
275      with open(path, 'w', encoding='utf-8') as f:
276          f.write(report)
277      print(f"\nSaved: results/stats.txt")
บรรทัด 245–254: ประกาศ write_stats_report และหัวรายงาน (พารามิเตอร์ GA และ Hybrid)
บรรทัด 255–270: ต่อสถานการณ์ เขียนตารางค่าเฉลี่ย ส่วนเบี่ยงเบน สูงสุด ต่ำสุด เวลา และจำนวน valid พร้อมผล Kruskal-Wallis
บรรทัด 272–277: รวมเป็นข้อความ พิมพ์ และบันทึกเป็น results/stats.txt ซึ่งเป็นแหล่งตัวเลขของตาราง 4.1
บรรทัด 280–314  กราฟ convergence
280  def plot_convergence(all_results, algos, out_dir):
281      """วาดกราฟ convergence (fitness per generation) ของ GA และ Hybrid เทียบกับ Greedy baseline
282      บันทึกเป็น results/convergence.png
283      """
284      import matplotlib
285      matplotlib.use('Agg')
286      import matplotlib.pyplot as plt
287
288      scenarios = list(all_results.keys())
289      n = len(scenarios)
290      fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))
291      if n == 1:
292          axes = [axes]
293      colors = {'GA': '#e74c3c', 'Hybrid': '#2980b9'}
294
295      for ax, sc_label in zip(axes, scenarios):
296          sc = all_results[sc_label]
297          g_score = sc['Greedy']['score_stats']['mean']
298          for algo in ['GA', 'Hybrid']:
299              hist = sc[algo].get('avg_history', [])
300              if hist:
301                  ax.plot(hist, label=algo, color=colors[algo], lw=1.8)
302          ax.axhline(g_score, color='#27ae60', ls='--', lw=1.4,
303                     label=f'Greedy ({g_score:.1f})')
304          ax.set_title(sc_label.replace('_', ' '), fontsize=9, fontweight='bold')
305          ax.set_xlabel('Generation', fontsize=8)
306          ax.set_ylabel('Fitness (Score)', fontsize=8)
307          ax.legend(fontsize=7)
308          ax.grid(True, alpha=0.3)
309
310      fig.suptitle('Convergence — GA vs Hybrid vs Greedy Baseline',
311                   fontsize=11, fontweight='bold')
312      plt.tight_layout()
313      plt.savefig(os.path.join(out_dir, 'convergence.png'), dpi=150, bbox_inches='tight')
314      plt.close()
บรรทัด 280–286: ประกาศ plot_convergence นำเข้า matplotlib แบบไม่ใช้หน้าจอ
บรรทัด 288–293: สร้างแผงย่อยหนึ่งแผงต่อสถานการณ์
บรรทัด 295–303: วาดเส้นเฉลี่ย fitness ของ GA และ Hybrid และเส้นประของ Greedy
บรรทัด 304–308: ตั้งชื่อ แกน คำอธิบาย และกริด
บรรทัด 310–314: ใส่ชื่อรวม จัดวาง บันทึก convergence.png (ภาพ 4.1 ในรายงาน) และปิดรูป
บรรทัด 317–331  สรุปท้าย
317  def print_summary(all_results, algos):
318      """แสดงตารางสรุป: แต่ละ scenario — algorithm ที่ดีที่สุด, score, และ improvement เทียบ Greedy"""
319      print(f"\n{'=' * 55}")
320      print(f"{'Scenario':<25} {'Best':^8} {'Score':>8} {'vs Greedy':>10}")
321      print("-" * 53)
322      for sc_label, sc_data in all_results.items():
323          g_score = sc_data['Greedy']['score_stats']['mean']
324          best_algo, best_score = 'Greedy', g_score
325          for algo in ['GA', 'Hybrid']:
326              s = sc_data[algo]['score_stats']['mean']
327              if s > best_score:
328                  best_score, best_algo = s, algo
329          delta = best_score - g_score
330          print(f"{sc_label:<25} {best_algo:^8} {best_score:>8.1f} "
331                f"{'+' if delta >= 0 else ''}{delta:>9.1f}")
บรรทัด 317–331: print_summary พิมพ์อัลกอริทึมที่ดีที่สุดของแต่ละสถานการณ์ คะแนน และส่วนต่างเทียบ Greedy
บรรทัด 334–335  จุดเริ่มต้น
334  if __name__ == '__main__':
335      main()
บรรทัด 334–335: เรียก main() เมื่อรันไฟล์ตรง ๆ

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
algorithm/utils.py
experiments/run_province_experiments.py