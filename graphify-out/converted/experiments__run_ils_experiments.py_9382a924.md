<!-- converted from experiments__run_ils_experiments.py.docx -->

คู่มือโค้ด: experiments/run_ils_experiments.py
การทดลอง ILS: Hybrid เทียบ Hybrid+ILS
ไฟล์ต้นฉบับ: experiments/run_ils_experiments.py (58 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: วัดว่า Insertion Local Search ช่วยเพิ่มคะแนนของ Hybrid จริงหรือไม่ ใน 4 จังหวัด × 3 สถานการณ์ × น้ำหนักความหลากหลาย 2 ค่า × 15 รอบ (seed เดียวกัน) ผลคือตาราง 4.6 ในรายงาน ใช้ ➜ hybrid_solve() ใน algorithm/hybrid.py ซึ่งเปิด/ปิด ILS ผ่านพารามิเตอร์ ils ตัว ILS อยู่ที่ ➜ algorithm/ils.py และใช้ตัวช่วยจาก ➜ experiments/run_province_experiments.py

บรรทัด 1–18  หัวไฟล์ นำเข้า และค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  run_ils_experiments.py — Project 2: วัดผล insertion local search (algorithm/ils.py) ด้วยโปรโตคอลเดิม
4  4 จังหวัด × 3 scenarios × 15 รอบ (seed เดียวกัน), เทียบ Hybrid (w=0) / Hybrid+ILS และ Hybrid+Div (w=1.5) / Hybrid+Div+ILS
5  ทดสอบ Wilcoxon แบบจับคู่ (ทางเดียว: ILS > ปกติ) และวัดเวลาที่เพิ่ม
6  ผลลัพธ์: results/ils_results.json, results/ils_stats.txt
7  """
8  import sys, os, json, random, statistics, time
9  HERE = os.path.dirname(__file__)
10  sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
11  sys.argv = [sys.argv[0], '15']
12  from scipy import stats as st
13  import run_province_experiments as E
14  from utils import evaluate_route
15  from hybrid import hybrid_solve
16
17  TRIALS = int(os.environ.get('ILS_TRIALS', 15))
18  OUT = os.path.join(HERE, 'results')
บรรทัด 1–7: docstring: เทียบ Hybrid กับ Hybrid+ILS (ทั้ง w=0 และ w=1.5) ทดสอบ Wilcoxon แบบจับคู่ทางเดียวว่า ILS ดีกว่า และวัดเวลาที่เพิ่ม ผลที่ results/ils_results.json และ ils_stats.txt
บรรทัด 8–10: นำเข้าโมดูลมาตรฐานและเพิ่มโฟลเดอร์ algorithm/ เข้า path
บรรทัด 11: ตั้ง sys.argv ให้โมดูลทดลองหลักอ่านจำนวนรอบ 15
บรรทัด 12–15: นำเข้า scipy.stats ➜ experiments/run_province_experiments.py (ในชื่อ E) ➜ evaluate_route() ใน algorithm/utils.py และ ➜ hybrid_solve() ใน algorithm/hybrid.py
บรรทัด 17–18: TRIALS จำนวนรอบ (ตั้งต้น 15) และโฟลเดอร์ผลลัพธ์
บรรทัด 21–28  รันหนึ่งครั้ง
21  def run(pois, hotel, sc, act, w, ils, t):
22      random.seed(t)
23      t0 = time.perf_counter()
24      routes, _ = hybrid_solve(pois, hotel, sc['days'], act, scoring_mode=sc['mode'], diversity_weight=w, ils=ils, **E.HYBRID_PARAMS)
25      ms = (time.perf_counter() - t0) * 1000
26      ev = evaluate_route(routes, hotel, act)
27      meals = all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in routes if day)
28      return (ev['total_score'] if ev['valid'] and meals else 0.0), ev['valid'] and meals, ms
บรรทัด 21–22: ประกาศ run และตั้ง seed ตามรอบ
บรรทัด 23–25: จับเวลาและเรียก hybrid_solve โดยเปิดหรือปิด ILS ตามพารามิเตอร์ ils
บรรทัด 26: ประเมินแผน
บรรทัด 27: ตรวจว่าทุกวันมีร้านอาหารอย่างน้อย 2 ร้าน
บรรทัด 28: คืน (คะแนน ถ้าผ่านข้อจำกัดและมื้อครบ ไม่งั้น 0, ธงผ่าน, เวลา)
บรรทัด 31–52  ลูปทดลอง
31  def main():
32      res, lines = {}, ['=' * 100, f'ILS EXPERIMENTS — trials={TRIALS}', '=' * 100,
33                        f"{'Province/Scenario':<30}{'w':>4}{'base':>8}{'+ILS':>8}{'gain%':>7}{'valid b/i':>11}{'ms b':>7}{'ms i':>7}{'p(ILS>b)':>10}"]
34      for prov in E.PROVINCES:
35          for sc in E.SCENARIOS:
36              pois, hotel, act = E.setup(prov, sc)
37              for w in (0.0, 1.5):
38                  b, i, vb, vi, mb, mi = [], [], 0, 0, [], []
39                  for t in range(TRIALS):
40                      s0, ok0, m0 = run(pois, hotel, sc, act, w, False, t)
41                      s1, ok1, m1 = run(pois, hotel, sc, act, w, True, t)
42                      b.append(s0); i.append(s1); vb += ok0; vi += ok1; mb.append(m0); mi.append(m1)
43                  try:
44                      p = st.wilcoxon(i, b, alternative='greater').pvalue
45                  except ValueError:
46                      p = float('nan')
47                  key = f'{prov}/{sc["label"]}/w={w}'
48                  gain = 100 * (statistics.mean(i) - statistics.mean(b)) / statistics.mean(b)
49                  res[key] = {'w': w, 'base': statistics.mean(b), 'ils': statistics.mean(i), 'gain_pct': gain, 'valid_base': vb, 'valid_ils': vi,
50                              'ms_base': statistics.mean(mb), 'ms_ils': statistics.mean(mi), 'p': p, 'n': TRIALS}
51                  lines.append(f"{prov+'/'+sc['label']:<30}{w:>4}{res[key]['base']:>8.1f}{res[key]['ils']:>8.1f}{gain:>7.2f}{str(vb)+'/'+str(vi):>11}{res[key]['ms_base']:>7.0f}{res[key]['ms_ils']:>7.0f}{p:>10.4f}")
52                  print(lines[-1], flush=True)
บรรทัด 31–33: ประกาศ main และเตรียมหัวตาราง
บรรทัด 34–36: วนทุกจังหวัดและสถานการณ์ ตั้งค่าด้วย E.setup
บรรทัด 37–38: วนน้ำหนักความหลากหลาย 0.0 และ 1.5 และเตรียมตัวเก็บผล
บรรทัด 39–42: วนทุกรอบ รันแบบไม่ใช้ ILS และแบบใช้ ILS ด้วย seed เดียวกัน เก็บคะแนน ความถูกต้อง และเวลา
บรรทัด 43–46: ทดสอบ Wilcoxon แบบจับคู่ (ILS มากกว่าปกติ) ถ้าทดสอบไม่ได้ ให้ nan
บรรทัด 47–48: สร้างคีย์และคำนวณร้อยละที่เพิ่มขึ้น
บรรทัด 49–50: เก็บผลของชุดนี้
บรรทัด 51–52: เพิ่มบรรทัดผลและพิมพ์
บรรทัด 53–58  บันทึกผล
53      json.dump({'trials': TRIALS, 'results': res}, open(os.path.join(OUT, 'ils_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
54      open(os.path.join(OUT, 'ils_stats.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
55
56
57  if __name__ == '__main__':
58      main()
บรรทัด 53: เขียน results/ils_results.json
บรรทัด 54: เขียน ils_stats.txt ซึ่งถูกนำไปเติมตาราง 4.6 ในรายงาน
บรรทัด 57–58: เรียก main() เมื่อรันไฟล์ตรง ๆ

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/hybrid.py
algorithm/ils.py
algorithm/utils.py
experiments/run_province_experiments.py