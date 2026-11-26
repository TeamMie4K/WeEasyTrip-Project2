<!-- converted from experiments__run_rl_experiments.py.docx -->

คู่มือโค้ด: experiments/run_rl_experiments.py
การทดลอง RL: คุณภาพ seed และ Hybrid ที่ใช้ RL seed
ไฟล์ต้นฉบับ: experiments/run_rl_experiments.py (70 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ประเมินตัวแทน RL ของ ➜ algorithm/rl.py (ค่า θ จาก ➜ experiments/train_rl.py) สองส่วน คือ (1) คุณภาพของแผนเริ่มต้น Greedy เทียบ RL แบบ deterministic (2) Hybrid ปกติเทียบ Hybrid ที่ใช้ RL เป็น seed (Wilcoxon แบบจับคู่) ครอบคลุมสถานการณ์ที่เคยฝึก (S1–S3) และที่ไม่เคยฝึก (H1 H2) ผลคือตาราง 4.7 ในรายงาน

บรรทัด 1–26  หัวไฟล์ นำเข้า และสถานการณ์
1  # -*- coding: utf-8 -*-
2  """
3  run_rl_experiments.py — Project 2: ประเมิน RL agent (algorithm/rl.py, theta จาก train_rl.py)
4  ส่วน 1  คุณภาพของแผนเริ่มต้น: Greedy (ตามโหมดของ scenario) เทียบ RL แบบ deterministic
5  ส่วน 2  ใช้เป็น seed ใน Hybrid: Hybrid ปกติ เทียบ Hybrid ที่มี RL seed (Wilcoxon แบบจับคู่, 15 รอบ)
6  scenario ที่ฝึก: S1-S3 (ตำแหน่งโรงแรมเดียวกับตอนฝึก); scenario ที่ไม่เคยเห็น: H1 (4 วัน 12,000 โรงแรมตำแหน่ง 0.25), H2 (6 วัน 30,000 ตำแหน่ง 0.75)
7  """
8  import sys, os, json, random, statistics, time
9  HERE = os.path.dirname(__file__)
10  sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
11  sys.argv = [sys.argv[0], '15']
12  import numpy as np
13  from scipy import stats as st
14  import run_province_experiments as E
15  import rl
16  from utils import evaluate_route
17  from greedy import greedy_solve
18  from hybrid import hybrid_solve
19
20  TRIALS = int(os.environ.get('RL_TRIALS', 15))
21  theta = np.array(json.load(open(os.path.join(HERE, '..', 'algorithm', 'rl_policy.json'), encoding='utf-8'))['theta'])
22  SCEN = [dict(s, group='train') for s in E.SCENARIOS] + [
23      {'label': 'H1_4d_12k', 'budget': 12_000, 'days': 4, 'hotel_frac': 0.25, 'mode': 'ratio', 'group': 'held-out'},
24      {'label': 'H2_6d_30k', 'budget': 30_000, 'days': 6, 'hotel_frac': 0.75, 'mode': 'quality', 'group': 'held-out'},
25  ]
26  OUT = os.path.join(HERE, 'results')
บรรทัด 1–7: docstring อธิบายสองส่วนของการทดลองและนิยามสถานการณ์ที่ฝึก/ไม่เคยฝึก
บรรทัด 8–10: นำเข้าโมดูลมาตรฐานและเพิ่มโฟลเดอร์ algorithm/ เข้า path
บรรทัด 11: ตั้ง sys.argv ให้โมดูลทดลองหลักอ่านจำนวนรอบ
บรรทัด 12–18: นำเข้า numpy scipy ➜ experiments/run_province_experiments.py ➜ algorithm/rl.py ➜ evaluate_route() ใน algorithm/utils.py ➜ greedy_solve() ใน algorithm/greedy.py และ ➜ hybrid_solve() ใน algorithm/hybrid.py
บรรทัด 20: TRIALS จำนวนรอบ (ตั้งต้น 15)
บรรทัด 21: โหลดค่า θ จาก algorithm/rl_policy.json
บรรทัด 22–25: SCEN สถานการณ์ทั้งหมด: S1–S3 ที่ฝึก (กลุ่ม train) และ H1 (4 วัน 12,000 บาท) กับ H2 (6 วัน 30,000 บาท) ที่ไม่เคยเห็น (กลุ่ม held-out)
บรรทัด 26: โฟลเดอร์ผลลัพธ์
บรรทัด 29–31  ฟังก์ชันให้คะแนน
29  def score(routes, hotel, act):
30      ev = evaluate_route(routes, hotel, act)
31      return ev['total_score'] if ev['valid'] else 0.0, ev['valid']
บรรทัด 29–31: score ประเมินแผน คืนคะแนน (หรือ 0 ถ้าไม่ผ่านข้อจำกัด) และธงผ่าน
บรรทัด 34–64  ลูปทดลอง
34  def main():
35      res, lines = {}, ['=' * 104, f'RL EXPERIMENTS — trials={TRIALS}; seed quality (Greedy vs RL-argmax) and Hybrid with/without RL seeds', '=' * 104,
36                        f"{'Province/Scenario':<30}{'grp':<9}{'Greedy':>8}{'RL':>8}{'valid G/R':>11}{'Hybrid':>9}{'Hyb+RL':>9}{'p(RL>H)':>9}{'ms H':>7}{'ms HR':>7}"]
37      for prov in E.PROVINCES:
38          for sc in SCEN:
39              pois, hotel, act = E.setup(prov, sc)
40              g, r, gv, rv, h0, h1, t0s, t1s = [], [], 0, 0, [], [], [], []
41              for t in range(TRIALS):
42                  random.seed(t)
43                  sg, ok = score(greedy_solve(pois, hotel, sc['days'], act, scoring_mode=sc['mode']), hotel, act)
44                  g.append(sg); gv += ok
45                  np.random.seed(t)
46                  sr, ok = score(rl.rl_solve(pois, hotel, sc['days'], act, theta, sample=False), hotel, act)
47                  r.append(sr); rv += ok
48                  for lst, th, tl in ((h0, None, t0s), (h1, theta, t1s)):
49                      random.seed(t); np.random.seed(t)
50                      t0 = time.perf_counter()
51                      routes, _ = hybrid_solve(pois, hotel, sc['days'], act, scoring_mode=sc['mode'], rl_theta=th, **E.HYBRID_PARAMS)
52                      tl.append((time.perf_counter() - t0) * 1000)
53                      lst.append(score(routes, hotel, act)[0])
54              try:
55                  p = st.wilcoxon(h1, h0, alternative='greater').pvalue
56              except ValueError:
57                  p = float('nan')
58              key = f'{prov}/{sc["label"]}'
59              res[key] = {'group': sc['group'], 'greedy': statistics.mean(g), 'rl': statistics.mean(r), 'valid_g': gv, 'valid_r': rv,
60                          'hybrid': statistics.mean(h0), 'hybrid_rl': statistics.mean(h1), 'p_rl_gt_h': p,
61                          'ms_h': statistics.mean(t0s), 'ms_hr': statistics.mean(t1s), 'n': TRIALS}
62              x = res[key]
63              lines.append(f"{key:<30}{sc['group']:<9}{x['greedy']:>8.1f}{x['rl']:>8.1f}{str(gv)+'/'+str(rv):>11}{x['hybrid']:>9.1f}{x['hybrid_rl']:>9.1f}{p:>9.4f}{x['ms_h']:>7.0f}{x['ms_hr']:>7.0f}")
64              print(lines[-1], flush=True)
บรรทัด 34–36: ประกาศ main และเตรียมหัวตาราง
บรรทัด 37–39: วนทุกจังหวัดและสถานการณ์ ตั้งค่าด้วย E.setup
บรรทัด 40: เตรียมตัวเก็บผล (Greedy RL Hybrid Hybrid+RL เวลา และจำนวนที่ผ่าน)
บรรทัด 41–47: ทุกรอบ: วัดแผนเริ่มต้นของ Greedy และของ RL แบบ deterministic (sample=False)
บรรทัด 48–53: รัน Hybrid สองแบบด้วย seed เดียวกัน (ไม่มี RL seed และมี RL seed) จับเวลาและเก็บคะแนน
บรรทัด 54–57: ทดสอบ Wilcoxon แบบจับคู่ (Hybrid+RL มากกว่า Hybrid) ถ้าทดสอบไม่ได้ให้ nan
บรรทัด 58–62: สรุปผลของชุดนี้
บรรทัด 63–64: เพิ่มบรรทัดผลและพิมพ์
บรรทัด 65–70  บันทึกผล
65      json.dump({'trials': TRIALS, 'theta': theta.tolist(), 'results': res}, open(os.path.join(OUT, 'rl_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
66      open(os.path.join(OUT, 'rl_stats.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
67
68
69  if __name__ == '__main__':
70      main()
บรรทัด 65: เขียน results/rl_results.json (รวม θ ที่ใช้)
บรรทัด 66: เขียน rl_stats.txt ซึ่งใช้เติมตาราง 4.7
บรรทัด 69–70: เรียก main() เมื่อรันไฟล์ตรง ๆ

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/greedy.py
algorithm/hybrid.py
algorithm/rl.py
algorithm/utils.py
experiments/run_province_experiments.py
experiments/train_rl.py