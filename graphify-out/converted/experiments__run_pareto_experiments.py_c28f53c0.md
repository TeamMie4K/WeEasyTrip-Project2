<!-- converted from experiments__run_pareto_experiments.py.docx -->

คู่มือโค้ด: experiments/run_pareto_experiments.py
การทดลอง Pareto: NSGA-II เทียบ Hybrid แบบถ่วงน้ำหนัก
ไฟล์ต้นฉบับ: experiments/run_pareto_experiments.py (95 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สร้างตาราง 4.8 ในรายงาน เทียบ ➜ nsga2_solve() ใน algorithm/pareto.py กับ Hybrid ที่ตั้งน้ำหนักความหลากหลาย 4 ค่า (เลือกเฉพาะแผนที่ไม่ถูกครอบงำ) ด้วย hypervolume แบบ Monte Carlo และจำนวนแผนทางเลือก ใช้ตัวช่วยจาก ➜ experiments/run_province_experiments.py ผลบันทึกที่ results/pareto_results.json และ pareto_stats.txt

บรรทัด 1–21  หัวไฟล์ นำเข้า และค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  run_pareto_experiments.py — Project 2: เทียบ NSGA-II (Pareto front) กับ Hybrid แบบ weighted-sum
4  วัตถุประสงค์ 3 ข้อ: คะแนน(max) / ความหลากหลายของหมวดต่อวัน(max) / ระยะทางรวม(min)
5  baseline = Hybrid ที่ตั้งน้ำหนักความหลากหลาย w ∈ {0, 1.5, 3, 6} (4 แผน) แล้วเอาเฉพาะแผนที่ non-dominated
6  เทียบด้วย hypervolume (Monte Carlo, จุดอ้างอิงและกล่องร่วมกันของแต่ละ trial) และจำนวนแผนที่ผู้ใช้เลือกได้
7  ผลลัพธ์: results/pareto_results.json, results/pareto_stats.txt
8  """
9  import sys, os, json, random, statistics, time
10  HERE = os.path.dirname(__file__)
11  sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
12  sys.argv = [sys.argv[0], '15'] + sys.argv[1:]
13  import run_province_experiments as E
14  from scipy import stats as st
15  from hybrid import hybrid_solve
16  from pareto import nsga2_solve, evaluate_objectives, _dominates
17
18  TRIALS = int(os.environ.get('PARETO_TRIALS', 8))
19  SC = E.SCENARIOS[1]          # S2: 5 วัน 15,000 บาท
20  WEIGHTS = [0.0, 1.5, 3.0, 6.0]
21  OUT = os.path.join(HERE, 'results')
บรรทัด 1–8: docstring: เทียบ NSGA-II กับ Hybrid weighted-sum (w ∈ {0, 1.5, 3, 6}) ด้วย hypervolume ที่ใช้กล่องและจุดอ้างอิงร่วมกันในแต่ละ trial และจำนวนแผนที่ผู้ใช้ได้เลือก
บรรทัด 9: นำเข้าโมดูลมาตรฐาน
บรรทัด 10–11: เพิ่มโฟลเดอร์ algorithm/ เข้า path
บรรทัด 12: ตั้ง sys.argv ให้โมดูลทดลองหลักอ่านจำนวนรอบ 15
บรรทัด 13: นำเข้า ➜ experiments/run_province_experiments.py (ใช้ PROVINCES SCENARIOS setup HYBRID_PARAMS)
บรรทัด 14: นำเข้า scipy.stats สำหรับการทดสอบ Wilcoxon
บรรทัด 15: นำเข้า ➜ hybrid_solve() ใน algorithm/hybrid.py
บรรทัด 16: นำเข้าจาก ➜ algorithm/pareto.py ฟังก์ชันประเมินวัตถุประสงค์และการครอบงำ
บรรทัด 18: TRIALS จำนวนรอบต่อจังหวัด (ตั้งต้น 8)
บรรทัด 19: SC สถานการณ์ S2 (5 วัน 15,000 บาท)
บรรทัด 20: WEIGHTS น้ำหนักความหลากหลายที่ใช้เป็น baseline
บรรทัด 21: โฟลเดอร์ผลลัพธ์
บรรทัด 24–25  กรองคำตอบที่ไม่ถูกครอบงำ
24  def nondominated(items):
25      return [a for a in items if not any(_dominates(b, a) for b in items if b is not a)]
บรรทัด 24–25: nondominated เก็บเฉพาะรายการที่ไม่มีรายการอื่นครอบงำด้วย ➜ _dominates() ใน algorithm/pareto.py
บรรทัด 28–34  เตรียมตารางผล
28  def main():
29      res, lines = {}, ['=' * 92, f'PARETO EXPERIMENTS — NSGA-II vs weighted-sum Hybrid, S2 (5 days), trials={TRIALS}', '=' * 92,
30                        f"{'Province':<11}{'HV NSGA':>10}{'HV WS':>10}{'ratio':>8}{'ratio2D':>9}{'#plans N':>10}{'#plans WS':>11}{'ms N':>8}{'ms WS':>8}{'p(HV)':>9}"]
31      for prov in E.PROVINCES:
32          pois, hotel, act = E.setup(prov, SC)
33          hv_n, hv_w, nn, nw, tn, tw = [], [], [], [], [], []
34          h2_n, h2_w = [], []   # hypervolume เฉพาะ 2 ด้าน (คะแนน, ความหลากหลาย) ซึ่งตรงกับสิ่งที่ weighted-sum ปรับให้
บรรทัด 28–30: ประกาศ main และเตรียมหัวตารางข้อความ
บรรทัด 31: วนทีละจังหวัด
บรรทัด 32: ตั้งค่าจังหวัด สถานการณ์ ด้วย E.setup (คืนจุด โรงแรม งบกิจกรรม)
บรรทัด 33–34: ตัวเก็บผลต่อ trial: hypervolume 3 มิติ จำนวนแผน เวลา และ hypervolume 2 มิติ (คะแนน × ความหลากหลาย)
บรรทัด 35–60  รันแต่ละ trial
35          for t in range(TRIALS):
36              random.seed(t)
37              t0 = time.perf_counter()
38              front = nsga2_solve(pois, hotel, SC['days'], act, scoring_mode='quality', pop_size=40, generations=40)
39              tn.append((time.perf_counter() - t0) * 1000)
40              ws = []
41              t0 = time.perf_counter()
42              for w in WEIGHTS:
43                  random.seed(t)
44                  routes, _ = hybrid_solve(pois, hotel, SC['days'], act, scoring_mode='quality', diversity_weight=w, **E.HYBRID_PARAMS)
45                  e = evaluate_objectives(routes, hotel, act)
46                  if e['viol'] == 0:
47                      ws.append(e)
48              tw.append((time.perf_counter() - t0) * 1000)
49              ws = nondominated(ws)
50              nn.append(len(front)); nw.append(len(ws))
51              pts_n = [s['obj'] for s in front]
52              pts_w = [s['obj'] for s in ws]
53              allp = pts_n + pts_w
54              if not allp:
55                  hv_n.append(0.0); hv_w.append(0.0)
56                  continue
57              ref = tuple(max(p[m] for p in allp) + 0.05 * (max(p[m] for p in allp) - min(p[m] for p in allp) + 1e-9) for m in range(3))
58              # กล่องเดียวกันทั้งสองวิธี: ใช้ min ร่วมโดยเพิ่มจุด 'กำหนดกล่อง' ไม่ได้ จึงคำนวณ HV ด้วยกล่องจาก min ร่วม
59              lo = tuple(min(p[m] for p in allp) for m in range(3))
60
บรรทัด 35–36: วนตามจำนวนรอบ ตั้ง seed ตามหมายเลขรอบ
บรรทัด 37–39: รัน NSGA-II (ประชากร 40 รุ่น 40) และจับเวลา
บรรทัด 40–48: รัน Hybrid ทีละน้ำหนัก (ใช้ seed เดียวกัน) เก็บเฉพาะแผนที่ไม่ละเมิดข้อจำกัด และจับเวลารวม
บรรทัด 49–50: กรองแผน weighted-sum ให้เหลือที่ไม่ถูกครอบงำ และบันทึกจำนวนแผนของทั้งสองวิธี
บรรทัด 51–53: รวมจุดวัตถุประสงค์ของสองวิธี
บรรทัด 54–56: ถ้าไม่มีจุดเลย บันทึก hypervolume เป็น 0 แล้วข้ามรอบ
บรรทัด 57: จุดอ้างอิง = ค่าสูงสุดของแต่ละมิติ บวก 5% ของช่วง
บรรทัด 58–59: มุมล่างของกล่อง = ค่าต่ำสุดของแต่ละมิติ (ใช้กล่องเดียวกันทั้งสองวิธีเพื่อเทียบได้)
บรรทัด 61–76  ฟังก์ชัน hypervolume ในกล่องร่วม
61              def hv(points, dims=3):
62                  # Monte Carlo ในกล่อง [lo, ref] เดียวกัน (dims=2: เฉพาะคะแนนและความหลากหลาย)
63                  rng = random.Random(t)
64                  hit = 0
65                  S = 40000
66                  for _ in range(S):
67                      q = [rng.uniform(lo[m], ref[m]) for m in range(dims)]
68                      if any(all(p[m] <= q[m] for m in range(dims)) for p in points):
69                          hit += 1
70                  vol = 1.0
71                  for m in range(dims):
72                      vol *= max(ref[m] - lo[m], 1e-12)
73                  return vol * hit / S
74
75              hv_n.append(hv(pts_n)); hv_w.append(hv(pts_w) if pts_w else 0.0)
76              h2_n.append(hv(pts_n, 2)); h2_w.append(hv(pts_w, 2) if pts_w else 0.0)
บรรทัด 61–73: hv ประมาณ hypervolume แบบ Monte Carlo ในกล่อง [lo, ref] (40,000 จุด) รองรับ 3 มิติหรือ 2 มิติ (คะแนนและความหลากหลาย) นับสัดส่วนจุดที่ถูกครอบงำ คูณปริมาตรกล่อง
บรรทัด 75: เก็บ hypervolume 3 มิติของ NSGA-II และ weighted-sum
บรรทัด 76: เก็บ hypervolume 2 มิติ
บรรทัด 77–91  สรุปผลและบันทึก
77          try:
78              p = st.wilcoxon(hv_n, hv_w, alternative='greater').pvalue
79          except ValueError:
80              p = float('nan')
81          ratio = statistics.mean(hv_n) / max(statistics.mean(hv_w), 1e-9)
82          res[prov] = {'hv_nsga': statistics.mean(hv_n), 'hv_ws': statistics.mean(hv_w), 'ratio': ratio,
83                       'plans_nsga': statistics.mean(nn), 'plans_ws': statistics.mean(nw),
84                       'ms_nsga': statistics.mean(tn), 'ms_ws': statistics.mean(tw), 'p': p, 'n': TRIALS,
85                       'hv2_nsga': statistics.mean(h2_n), 'hv2_ws': statistics.mean(h2_w), 'ratio2': statistics.mean(h2_n) / max(statistics.mean(h2_w), 1e-9)}
86          r = res[prov]
87          lines.append(f"{prov:<11}{r['hv_nsga']:>10.0f}{r['hv_ws']:>10.0f}{ratio:>8.2f}{r['ratio2']:>9.2f}{r['plans_nsga']:>10.1f}{r['plans_ws']:>11.1f}{r['ms_nsga']:>8.0f}{r['ms_ws']:>8.0f}{p:>9.4f}")
88          print(lines[-1], flush=True)
89      json.dump({'trials': TRIALS, 'weights': WEIGHTS, 'results': res}, open(os.path.join(OUT, 'pareto_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
90      open(os.path.join(OUT, 'pareto_stats.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
91      print('\n'.join(lines))
บรรทัด 77–80: ทดสอบ Wilcoxon (ทางเดียว NSGA-II มากกว่า) ถ้าข้อมูลทดสอบไม่ได้ ให้ค่า nan
บรรทัด 81: อัตราส่วน hypervolume = ค่าเฉลี่ย NSGA-II ÷ ค่าเฉลี่ย weighted-sum
บรรทัด 82–85: เก็บผลของจังหวัดนี้ (hypervolume จำนวนแผน เวลา ค่า p และอัตราส่วน 2 มิติ)
บรรทัด 86–88: เพิ่มบรรทัดผลลงตารางและพิมพ์
บรรทัด 89: เขียน results/pareto_results.json
บรรทัด 90–91: เขียน pareto_stats.txt และพิมพ์ตาราง ซึ่งถูกนำไปเติมในตาราง 4.8 ของรายงาน
บรรทัด 94–95  จุดเริ่มต้น
94  if __name__ == '__main__':
95      main()
บรรทัด 94–95: เรียก main() เมื่อรันไฟล์ตรง ๆ

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/hybrid.py
algorithm/pareto.py
experiments/run_province_experiments.py