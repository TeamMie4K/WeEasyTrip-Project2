<!-- converted from experiments__train_rl.py.docx -->

คู่มือโค้ด: experiments/train_rl.py
ฝึกนโยบาย RL ในสภาพแวดล้อมจำลอง
ไฟล์ต้นฉบับ: experiments/train_rl.py (49 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์ที่ฝึกตัวแทน RL ของ ➜ algorithm/rl.py ด้วย REINFORCE บน 4 จังหวัด × 3 สถานการณ์ แล้วบันทึกพารามิเตอร์ θ ลง algorithm/rl_policy.json ซึ่ง ➜ backend/main.py อ่านเป็น RL_THETA ใช้ฟังก์ชันตั้งค่าสภาพแวดล้อมจาก ➜ setup() ใน experiments/run_province_experiments.py

บรรทัด 1–19  นำเข้าและสร้างสภาพแวดล้อม
1  # -*- coding: utf-8 -*-
2  """ฝึก RL agent ในสภาพแวดล้อมจำลอง (4 จังหวัด × 3 scenarios, seed ฝึก 1000+) แล้วบันทึก theta ที่ algorithm/rl_policy.json"""
3  import sys, os, json, random, time
4  HERE = os.path.dirname(__file__)
5  sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
6  sys.argv = [sys.argv[0], '15']
7  import numpy as np
8  import run_province_experiments as E
9  import rl
10
11  EPISODES = int(os.environ.get('RL_EPISODES', 2400))
12  envs = []
13  for prov in E.PROVINCES:
14      for sc in E.SCENARIOS:
15          pois, hotel, act = E.setup(prov, sc)   # ตั้งโปรไฟล์เดินทางของจังหวัดด้วย
16          envs.append((prov, sc, pois, hotel, sc['days'], act))
17  # หมายเหตุ: โปรไฟล์เดินทางเป็น ContextVar ตั้งตอน setup() ล่าสุดเท่านั้น จึงฝึกทีละ env โดยตั้งโปรไฟล์ใหม่ก่อนทุก episode
18  from utils import set_travel_profile
19  cfg = E.PROV_CFG
บรรทัด 1–2: docstring: ฝึกใน 4 จังหวัด × 3 scenarios (seed ฝึก 1000 ขึ้นไป) แล้วบันทึก theta
บรรทัด 3: นำเข้าโมดูลมาตรฐาน
บรรทัด 4–5: เพิ่มโฟลเดอร์ algorithm/ เข้า path
บรรทัด 6: ตั้ง sys.argv ให้ run_province_experiments ซึ่งอ่านจำนวนรอบจากอาร์กิวเมนต์ใช้ค่า 15 (ไม่ได้รันการทดลองจริง เพียงนำเข้าฟังก์ชัน)
บรรทัด 7–9: นำเข้า numpy โมดูลทดลอง ➜ experiments/run_province_experiments.py และ ➜ algorithm/rl.py
บรรทัด 11: EPISODES จำนวน episode (ตั้งต้น 2,400 ปรับด้วยตัวแปรแวดล้อม)
บรรทัด 12–16: สร้างรายการสภาพแวดล้อมจากทุกจังหวัดและสถานการณ์ด้วย E.setup (ซึ่งตั้งโปรไฟล์เดินทางของจังหวัดด้วย)
บรรทัด 17: คอมเมนต์: โปรไฟล์เดินทางเป็น ContextVar ตั้งตอน setup() ล่าสุดเท่านั้น จึงต้องตั้งซ้ำก่อนรันแต่ละ episode
บรรทัด 18: นำเข้า ➜ set_travel_profile() ใน algorithm/utils.py
บรรทัด 19: cfg โปรไฟล์จังหวัดจากโมดูลทดลอง
บรรทัด 20–45  ลูปฝึก REINFORCE
20  theta = np.zeros(rl.N_FEATURES)
21  rng = random.Random(0)
22  np.random.seed(0)
23  t0 = time.time()
24  hist = []
25  window = []
26  base = {}
27  for ep in range(EPISODES):
28      prov, sc, pois, hotel, days, act = envs[rng.randrange(len(envs))]
29      set_travel_profile(cfg[prov].get('road_factor', 1.0), cfg[prov].get('speed_kmh', 40))
30      rec = []
31      routes = rl.rl_solve(pois, hotel, days, act, theta, sample=True, record=rec)
32      R = rl.episode_reward(routes, hotel, act, days)
33      key = (prov, sc['label'])
34      base[key] = R if key not in base else 0.95 * base[key] + 0.05 * R
35      adv = R - base[key]
36      grad = np.zeros(rl.N_FEATURES)
37      for phi, idx in rec:
38          lg = phi @ theta; lg -= lg.max(); p = np.exp(lg); p /= p.sum()
39          grad += phi[idx] - p @ phi
40      if rec:
41          theta += 0.8 * adv * grad / len(rec)
42      window.append(R)
43      if (ep + 1) % 300 == 0:
44          hist.append(float(np.mean(window))); window = []
45          print(ep + 1, 'mean reward', round(hist[-1], 4), 'theta', np.round(theta, 2).tolist(), round(time.time() - t0), 's', flush=True)
บรรทัด 20–22: θ เริ่มที่ศูนย์ ตั้ง seed ของ random และ numpy
บรรทัด 23–26: จับเวลา hist window และ base (baseline แยกตามจังหวัด/สถานการณ์)
บรรทัด 27: วนตามจำนวน episode
บรรทัด 28: สุ่มสภาพแวดล้อมหนึ่งชุด
บรรทัด 29: ตั้งโปรไฟล์เดินทางของจังหวัดนั้นใหม่
บรรทัด 30–31: สร้างแผนด้วยนโยบายปัจจุบัน และบันทึกการตัดสินใจ (rec) ด้วย ➜ rl_solve() ใน algorithm/rl.py
บรรทัด 32: คำนวณรางวัลด้วย ➜ episode_reward() ใน algorithm/rl.py
บรรทัด 33–35: ปรับ baseline แบบค่าเฉลี่ยเคลื่อนที่ และหา advantage
บรรทัด 36–39: คำนวณ gradient ของ log-policy (ใช้เองในสคริปต์นี้ ไม่ได้เรียกผ่านโมดูล ➜ algorithm/rl.py)
บรรทัด 40–41: ปรับ θ ด้วยอัตราเรียนรู้ 0.8
บรรทัด 42: เก็บรางวัลลงหน้าต่าง
บรรทัด 43–45: ทุก 300 episode บันทึกและพิมพ์ค่าเฉลี่ยรางวัล θ และเวลา
บรรทัด 46–49  บันทึกผล
46  json.dump({'theta': theta.tolist(), 'episodes': EPISODES, 'reward_history': hist,
47             'features': ['score', 'cost_frac', 'dist', 'wait', 'new_category', 'free', 'time_slack', 'score*(1-cost)', 'score/cost']},
48            open(os.path.join(HERE, '..', 'algorithm', 'rl_policy.json'), 'w', encoding='utf-8'), indent=1)
49  print('saved')
บรรทัด 46–48: เขียน θ จำนวน episode ประวัติรางวัล และชื่อลักษณะเฉพาะ 9 ตัวลง algorithm/rl_policy.json
บรรทัด 49: พิมพ์ saved

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/rl.py
algorithm/utils.py
backend/main.py
experiments/run_province_experiments.py