<!-- converted from algorithm__rl.py.docx -->

คู่มือโค้ด: algorithm/rl.py
Reinforcement Learning (REINFORCE) สร้างแผนเริ่มต้นแทน Greedy
ไฟล์ต้นฉบับ: algorithm/rl.py (117 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ตัวแทน (agent) ที่เรียนรู้นโยบายเลือกสถานที่ในแต่ละช่องของวัน ใช้ตรรกะกรองผู้สมัครเดียวกับ ➜ _find_best_for_slot() ใน algorithm/greedy.py (ผ่านพารามิเตอร์ chooser) นโยบายคือซอฟต์แมกซ์เชิงเส้นบนลักษณะเฉพาะ 9 ตัว ฝึกด้วย REINFORCE ผลการทดลองในรายงานคือ Hybrid+RL ไม่ได้ดีกว่า Hybrid อย่างสม่ำเสมอ จึงเป็นทางเลือกสำหรับโหมด Developer ถูกเรียกจาก ➜ hybrid_solve() ใน algorithm/hybrid.py เมื่อส่ง rl_theta ฝึกโดย ➜ experiments/train_rl.py

บรรทัด 1–19  หัวไฟล์และการนำเข้า
1  # -*- coding: utf-8 -*-
2  """
3  rl.py - Reinforcement Learning agent สำหรับสร้างแผนเริ่มต้น (แทน Greedy seed)
4
5  ปัญหาแบบ sequential decision: ในแต่ละ slot ของวัน (attr, attr, lunch, attr, attr, dinner)
6  agent เลือก 1 สถานที่จากรายการ candidate ที่ผ่านข้อจำกัด (เวลาเปิด-ปิด งบ เวลาต่อวัน) แล้วเดินต่อ
7  policy: softmax เชิงเส้น  pi(a|s) ∝ exp(theta · phi(s,a))
8  ฝึกด้วย REINFORCE (baseline = ค่าเฉลี่ยรางวัลของ scenario) ใน "สภาพแวดล้อมจำลอง" (ตัวอัลกอริทึมเอง)
9  รางวัล = คะแนนรวมของแผนที่ผ่านข้อจำกัด (ลบเมื่อเกินงบ/ผิดเวลา) — ไม่ใช้ประวัติผู้ใช้จริง เพราะระบบยังไม่มีข้อมูลนั้น
10  """
11  from typing import Dict, List
12
13  import numpy as np
14
15  from utils import haversine_km, travel_cost, DAY_TIME_BUDGET, DAY_START_MIN, evaluate_route
16  from utils import MAX_SIGHT_MIN
17  from greedy import (_find_best_for_slot, DAY_PATTERN, LUNCH_TRIGGER, DINNER_TRIGGER, DINNER_BUFFER_MIN)
18
19  N_FEATURES = 9
บรรทัด 1–9: docstring อธิบายแนวคิด: ปัญหาตัดสินใจต่อเนื่อง ในแต่ละช่อง agent เลือก 1 สถานที่จากผู้สมัครที่ผ่านข้อจำกัด นโยบายเป็น softmax เชิงเส้น π(a|s) ∝ exp(θ·φ(s,a)) ฝึกด้วย REINFORCE (baseline คือค่าเฉลี่ยรางวัลของ scenario) รางวัลคือคะแนนรวมของแผนที่ผ่านข้อจำกัด
บรรทัด 11: นำเข้าชนิดข้อมูลสำหรับ type hint
บรรทัด 13: นำเข้า numpy สำหรับคำนวณเมทริกซ์ลักษณะเฉพาะและเวกเตอร์ θ
บรรทัด 15–16: นำเข้าฟังก์ชันและค่าคงที่จาก ➜ algorithm/utils.py รวม ➜ evaluate_route() ใน algorithm/utils.py
บรรทัด 17: นำเข้าจาก ➜ algorithm/greedy.py ตัวเลือกจุดต่อช่อง แพตเทิร์นวัน และเวลาตั้งต้นมื้อ
บรรทัด 19: N_FEATURES = 9 จำนวนลักษณะเฉพาะ (ขนาดของ θ)
บรรทัด 22–38  สร้างลักษณะเฉพาะของผู้สมัคร
22  def features(cands: List[tuple], budget_left: float) -> np.ndarray:
23      """เมทริกซ์ลักษณะเฉพาะ (n_candidates x N_FEATURES) ของ candidate ที่ _find_best_for_slot ส่งมา"""
24      rows = []
25      for (_s, poi, d_to, arrive, add_cost, slack, wait, cat_count) in cands:
26          frac = min(add_cost / (budget_left + 1.0), 1.0)
27          rows.append([
28              poi['score'] / 10.0,
29              frac,
30              min(d_to / 20.0, 2.0),
31              min(wait / 60.0, 1.0),
32              1.0 if cat_count == 0 else 0.0,
33              1.0 if poi['cost'] == 0 else 0.0,
34              max(min(slack / DAY_TIME_BUDGET, 1.0), 0.0),
35              (poi['score'] / 10.0) * (1.0 - frac),
36              min((poi['score'] / (add_cost + 80.0)) * 100.0, 5.0) / 5.0,
37          ])
38      return np.array(rows, dtype=float)
บรรทัด 22–23: ประกาศ features แปลงรายการผู้สมัครที่ _find_best_for_slot ส่งมาเป็นเมทริกซ์ (จำนวนผู้สมัคร × 9)
บรรทัด 24: เตรียมรายการแถว
บรรทัด 25: แกะค่าของผู้สมัครแต่ละตัว (คะแนนดิบ จุด ระยะ เวลาถึง ค่าใช้จ่าย เวลาเหลือ เวลารอ จำนวนหมวดเดิม)
บรรทัด 26: สัดส่วนค่าใช้จ่ายต่องบที่เหลือ (ไม่เกิน 1)
บรรทัด 27–37: ลักษณะเฉพาะ 9 ตัว: (1) คะแนน ÷ 10 (2) สัดส่วนค่าใช้จ่าย (3) ระยะ ÷ 20 กม. จำกัด 2 (4) เวลารอ ÷ 60 จำกัด 1 (5) เป็นหมวดใหม่ของวันหรือไม่ (6) เป็นจุดฟรีหรือไม่ (7) เวลาเหลือ ÷ เพดานเวลา (8) คะแนน × (1 − สัดส่วนค่าใช้จ่าย) (9) อัตราส่วนคะแนนต่อต้นทุนปรับสเกล
บรรทัด 38: คืนเป็นอาร์เรย์ numpy
บรรทัด 41–61  `rl_solve`: ตัวเลือกตามนโยบาย
41  def rl_solve(pois: List[Dict], hotel: Dict, days: int, budget: float, theta: np.ndarray,
42               day_time: float = DAY_TIME_BUDGET, sample: bool = True, temperature: float = 1.0,
43               record: list = None) -> List[List[Dict]]:
44      """สร้างแผนด้วย policy (sample=False → เลือกค่าสูงสุดแบบ deterministic)
45      record: ถ้าส่ง list มา จะเก็บ (phi, chosen_index) ของทุกการตัดสินใจไว้ใช้ฝึก"""
46      used_ids = set()
47      remaining = float(budget)
48      routes = [[] for _ in range(days)]
49      per_day_budget = (budget / max(days, 1)) * 1.1
50      state = {'budget_left': remaining}
51
52      def chooser(cands):
53          phi = features(cands, state['budget_left'])
54          logits = phi @ theta / max(temperature, 1e-6)
55          logits -= logits.max()
56          p = np.exp(logits)
57          p /= p.sum()
58          idx = int(np.random.choice(len(p), p=p)) if sample else int(np.argmax(p))
59          if record is not None:
60              record.append((phi, idx))
61          return idx
บรรทัด 41–43: ประกาศ rl_solve รับจุด โรงแรม จำนวนวัน งบ θ เพดานเวลา ธง sample (สุ่มตามนโยบาย หรือเลือกค่าสูงสุด) อุณหภูมิ และ record
บรรทัด 44–45: docstring: record ใช้เก็บ (φ, ดัชนีที่เลือก) ของทุกการตัดสินใจเพื่อฝึก
บรรทัด 46–50: เตรียมตัวแปรแบบเดียวกับ ➜ greedy_solve() ใน algorithm/greedy.py (จุดที่ใช้แล้ว งบเหลือ แผนว่าง งบต่อวัน) และ state เก็บงบของช่องปัจจุบัน
บรรทัด 52: ฟังก์ชัน chooser ที่ส่งให้ _find_best_for_slot เพื่อให้ RL เป็นผู้เลือกแทนการเรียงคะแนน
บรรทัด 53: คำนวณลักษณะเฉพาะ
บรรทัด 54: logits = φ·θ ÷ อุณหภูมิ
บรรทัด 55–57: ลบค่าสูงสุดเพื่อความเสถียรเชิงตัวเลข แล้วคำนวณซอฟต์แมกซ์
บรรทัด 58: เลือกดัชนีด้วยการสุ่มตามความน่าจะเป็น หรือเลือกค่าสูงสุดถ้า sample=False
บรรทัด 59–60: ถ้ามี record เก็บ (φ, ดัชนี)
บรรทัด 61: คืนดัชนีที่เลือก
บรรทัด 63–89  วนวัน/ช่อง และ fallback
63      for day_idx in range(days):
64          pos, t = hotel, float(DAY_START_MIN)
65          cats = {}
66          day_left = min(per_day_budget, remaining)
67          past_lunch = dinner_done = False
68          sight_left = MAX_SIGHT_MIN
69          for slot in DAY_PATTERN:
70              if slot == 'lunch' and t < LUNCH_TRIGGER:
71                  t = float(LUNCH_TRIGGER)
72              elif slot == 'dinner' and t < DINNER_TRIGGER:
73                  t = float(DINNER_TRIGGER)
74              db = DINNER_BUFFER_MIN if (slot == 'attr' and past_lunch and not dinner_done) else 0
75              state['budget_left'] = day_left
76              res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, day_left, cats, slot,
77                                        dinner_buffer=db, chooser=chooser, sight_left=sight_left)
78              if res is None and slot in ('lunch', 'dinner'):          # fallback เหมือน Greedy: มื้อเป็น hard requirement
79                  state['budget_left'] = max(300.0, remaining * 0.5)
80                  res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, state['budget_left'], cats, slot, chooser=chooser, sight_left=sight_left)
81              if res is None and slot in ('lunch', 'dinner'):
82                  state['budget_left'] = 1e9
83                  res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, 1e9, cats, slot, chooser=chooser, sight_left=sight_left)
84              if res is None and slot in ('lunch', 'dinner'):
85                  res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, 1e9, cats, slot, chooser=chooser, relax_meal=True, sight_left=sight_left)
86              if res is None:
87                  state['budget_left'] = 1e9
88                  res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, 1e9, cats, slot,
89                                            free_only=True, dinner_buffer=db, chooser=chooser, sight_left=sight_left)
บรรทัด 63–68: ตั้งต้นรายวันเหมือน greedy: ตำแหน่ง เวลา หมวด งบวัน ธงมื้อ เวลาเที่ยวคงเหลือ
บรรทัด 69–73: วนตามแพตเทิร์น และเลื่อนเวลาเข้าช่วงมื้อ
บรรทัด 74: กันเวลา 150 นาทีให้มื้อเย็นเมื่อเป็นช่องเที่ยวหลังมื้อกลางวัน
บรรทัด 75–77: เรียก _find_best_for_slot พร้อม chooser ของ RL
บรรทัด 78–80: ถ้าหาไม่ได้ในช่องมื้อ ขยายงบมื้อ (fallback เหมือน greedy)
บรรทัด 81–83: ถ้ายังไม่ได้ ไม่จำกัดงบ
บรรทัด 84–85: ถ้ายังไม่ได้ ผ่อนช่วงเวลามื้อ
บรรทัด 86–89: ถ้ายังไม่ได้ ลองเฉพาะจุดฟรี
บรรทัด 90–108  บันทึกจุดที่เลือก
90              if slot == 'lunch':
91                  past_lunch = True
92              if slot == 'dinner':
93                  dinner_done = True
94              if res is None:
95                  continue
96              poi, d_to, arrive = res
97              used_ids.add(poi['id'])
98              routes[day_idx].append(poi)
99              if poi['category'] != 'restaurant': sight_left -= poi['duration_min']
100              t = arrive + poi['duration_min']
101              pos = poi
102              spent = travel_cost(d_to) + poi['cost']
103              remaining -= spent
104              day_left = max(0.0, day_left - spent)
105              cats[poi['category']] = cats.get(poi['category'], 0) + 1
106          if routes[day_idx]:
107              remaining -= travel_cost(haversine_km(pos['lat'], pos['lng'], hotel['lat'], hotel['lng']))
108      return routes
บรรทัด 90–93: ตั้งธงเมื่อผ่านช่องมื้อกลางวัน/เย็น
บรรทัด 94–95: ถ้าไม่มีจุด ข้ามช่องนี้
บรรทัด 96–101: บันทึกจุดว่าใช้แล้ว ต่อท้ายเส้นทาง หักเวลาท่องเที่ยว และเลื่อนเวลา/ตำแหน่ง
บรรทัด 102–105: หักค่าใช้จ่ายออกจากงบทริปและงบวัน และนับหมวด
บรรทัด 106–107: เมื่อวันนั้นมีจุด หักค่าเดินทางกลับโรงแรม
บรรทัด 108: คืนแผน
บรรทัด 111–117  รางวัลของหนึ่ง episode
111  def episode_reward(routes, hotel, budget, days) -> float:
112      """รางวัล = คะแนนรวมต่อวัน (ปรับสเกล) ลบโทษเมื่อผิดข้อจำกัด"""
113      ev = evaluate_route(routes, hotel, budget)
114      r = ev['total_score'] / max(days, 1) / 10.0
115      if not ev['valid']:
116          r -= 0.5 * len(ev['violations'])
117      return r
บรรทัด 111–112: ประกาศ episode_reward
บรรทัด 113: ประเมินแผนด้วย ➜ evaluate_route() ใน algorithm/utils.py
บรรทัด 114: รางวัลตั้งต้น = คะแนนรวม ÷ จำนวนวัน ÷ 10
บรรทัด 115–116: ถ้าแผนผิดข้อจำกัด หักรางวัล 0.5 ต่อข้อความผิด
บรรทัด 117: คืนรางวัล

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/greedy.py
algorithm/hybrid.py
algorithm/utils.py
experiments/train_rl.py