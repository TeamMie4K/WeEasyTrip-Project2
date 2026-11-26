<!-- converted from algorithm__greedy.py.docx -->

คู่มือโค้ด: algorithm/greedy.py
Greedy แบบแบ่งช่อง (slot-based) สร้างแผนเริ่มต้น
ไฟล์ต้นฉบับ: algorithm/greedy.py (215 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สร้างแผนรายวันโดยเติมทีละช่องตามแพตเทิร์น [เที่ยว, เที่ยว, มื้อกลางวัน, เที่ยว, เที่ยว, มื้อเย็น] เลือกจุดที่ "คะแนนต่อต้นทุน" ดีที่สุดในแต่ละช่อง เป็นทั้งอัลกอริทึมเส้นฐาน (baseline) ในบทที่ 4 และเป็น seed เริ่มต้นให้ ➜ initial_population() ใน algorithm/genetic.py กับ ➜ hybrid_solve() ใน algorithm/hybrid.py ฟังก์ชันตรวจแผนมาจาก ➜ evaluate_route() ใน algorithm/utils.py

บรรทัด 1–23  นำเข้าและค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  greedy.py - Slot-based Greedy Algorithm สำหรับปัญหา B-TOPTW
4
5  Workflow ต่อหนึ่งวัน: [attr, attr, lunch, attr, attr, dinner]
6    - เลือก POI ที่มี score/cost ratio สูงสุดในแต่ละ slot
7    - มี fallback หลายระดับ (ขยายงบมื้อ, ร้านใดก็ได้, ขยายเวลาเข้าร้าน, เฉพาะของฟรี) เพื่อรับประกัน lunch + dinner ทุกวัน
8    - random_factor เพิ่ม diversity เพื่อใช้เป็น seed ใน GA/Hybrid
9  """
10  import random
11  from utils import (haversine_km, travel_time_min, travel_cost,
12                     DAY_TIME_BUDGET, DAY_START_MIN, evaluate_route, LUNCH_WIN, DINNER_WIN, MAX_SIGHT_MIN)
13
14  DAY_PATTERN    = ['attr', 'attr', 'lunch', 'attr', 'attr', 'dinner']   # 6 จุด/วัน (เที่ยว 4 + อาหาร 2) เหมือน Project 1
15  LUNCH_TRIGGER  = 690
16  DINNER_TRIGGER = 1020
17  LUNCH_ARRIVE   = LUNCH_WIN
18  DINNER_ARRIVE  = DINNER_WIN
19  LUNCH_RELAXED  = LUNCH_WIN      # ไม่ผ่อนช่วงเวลามื้อแล้ว (ต้องตรงเวลาจริง)
20  DINNER_RELAXED = DINNER_WIN
21  MAX_MEAL_WAIT  = 90
22  GREEDY_KM_PENALTY = 10.0   # บาทเทียบเท่าต่อ km ใน ranking ของ greedy (ให้เลือกจุดใกล้กัน เหมือน DIST_WEIGHT ของ Hybrid/GA)
23  DINNER_BUFFER_MIN = 150
บรรทัด 1–9: หัวไฟล์ และ docstring สรุปแนวคิด: 1 วัน = 6 ช่อง เลือกจุดที่ score/cost สูงสุด มี fallback หลายระดับ (ขยายงบมื้อ ร้านใดก็ได้ ขยายเวลาเข้าร้าน เฉพาะของฟรี) เพื่อให้มีมื้อกลางวัน+เย็นทุกวัน และมี random_factor เพื่อสร้างความหลากหลายสำหรับ seed
บรรทัด 10: นำเข้า random ใช้สุ่มลำดับ POI และใส่ noise
บรรทัด 11–12: นำเข้าฟังก์ชันและค่าคงที่จาก ➜ algorithm/utils.py (ระยะทาง เวลาเดินทาง ค่าเดินทาง เวลาเริ่ม/เพดานเวลา ช่วงเวลามื้อ เพดานเวลาท่องเที่ยว และ evaluate_route)
บรรทัด 14: DAY_PATTERN แพตเทิร์น 6 ช่องต่อวัน (เที่ยว 4 + อาหาร 2) เหมือน Project 1
บรรทัด 15: LUNCH_TRIGGER = 690 เวลา 11:30 ถ้าถึงช่องมื้อกลางวันก่อนเวลานี้ ให้เลื่อนเวลาเป็นเวลานี้
บรรทัด 16: DINNER_TRIGGER = 1020 เวลา 17:00 ใช้กับมื้อเย็นแบบเดียวกัน
บรรทัด 17–18: ช่วงเวลาที่ยอมให้ไปถึงร้านสำหรับมื้อกลางวัน/เย็น ใช้ค่าเดียวกับ LUNCH_WIN DINNER_WIN
บรรทัด 19–20: ค่า "ผ่อน" ช่วงมื้อ ตอนนี้ตั้งเท่าค่าปกติ เพราะต้องตรงเวลามื้อจริง
บรรทัด 21: MAX_MEAL_WAIT = 90 รอร้านเปิดได้สูงสุด 90 นาที (สำหรับมื้ออาหาร)
บรรทัด 22: GREEDY_KM_PENALTY = 10.0 ค่าปรับเทียบเท่า 10 บาทต่อ กม. ในการจัดอันดับ เพื่อให้ Greedy เลือกจุดใกล้กัน เป็นการถ่วงระยะขับให้ Greedy เทียบเท่า DIST_WEIGHT ของ ➜ algorithm/hybrid.py และ ➜ fitness() ใน algorithm/genetic.py (เพิ่มเมื่อ 18 พ.ย. 2569 ค่านี้ตั้งเองไม่ได้ปรับจูน)
บรรทัด 23: DINNER_BUFFER_MIN = 150 กันเวลาไว้ให้มื้อเย็นเมื่อเลือกจุดเที่ยวช่วงบ่าย
บรรทัด 30–38  ฟังก์ชันเลือกจุดต่อช่อง: ประกาศและเอกสาร
30  def _find_best_for_slot(pois, used_ids, current_pos, current_time, hotel,
31                          day_time, budget_left, day_categories,
32                          slot_type, scoring_mode='ratio',
33                          free_only=False, dinner_buffer=0, random_factor=0.0, relax_meal=False, chooser=None, sight_left=1e9):
34      """เลือก POI ที่เหมาะสมที่สุดสำหรับ slot ประเภท attr / lunch / dinner
35      คืน (poi, distance_km, arrive_time) หรือ None ถ้าหาไม่ได้
36      chooser: ฟังก์ชันเลือก candidate แทนการเรียงคะแนน (ใช้กับ RL) รับ list ของ
37               (score, poi, d_to, arrive, add_cost, time_slack, wait, cat_count) คืน index ที่เลือก
38      """
บรรทัด 30–33: ประกาศ _find_best_for_slot พารามิเตอร์หลักคือจุดทั้งหมด จุดที่ใช้แล้ว ตำแหน่งและเวลาปัจจุบัน โรงแรม เพดานเวลา งบที่เหลือ หมวดที่ใช้แล้วในวัน ชนิดช่อง (attr lunch dinner) โหมดคะแนน และตัวเลือกพิเศษ (เฉพาะฟรี กันเวลามื้อเย็น noise ผ่อนมื้อ chooser และเวลาเที่ยวที่เหลือ)
บรรทัด 34–38: docstring: คืน (จุด ระยะ เวลาถึง) หรือ None ถ้าหาไม่ได้ chooser เป็นฟังก์ชันเลือกแทนการเรียงคะแนน ใช้กับการเรียนรู้แบบเสริมกำลังใน ➜ rl_solve() ใน algorithm/rl.py
บรรทัด 39–66  กรองผู้สมัครตามชนิดช่อง งบ และเวลาเปิด
39      candidates = []
40      for poi in pois:
41          if poi['id'] in used_ids: continue
42          if slot_type == 'attr' and poi['category'] == 'restaurant': continue
43          if slot_type in ('lunch', 'dinner') and poi['category'] != 'restaurant': continue
44          if free_only and poi['cost'] > 0: continue
45          if slot_type == 'attr' and (poi['duration_min'] > 240 or poi['duration_min'] > sight_left): continue
46          d_to   = haversine_km(current_pos['lat'], current_pos['lng'], poi['lat'], poi['lng'])
47          d_back = haversine_km(poi['lat'], poi['lng'], hotel['lat'], hotel['lng'])
48          travel_t = travel_time_min(d_to)
49          back_t   = travel_time_min(d_back)
50          arrive_raw = current_time + travel_t
51          if arrive_raw < poi['open_min']:
52              wait = poi['open_min'] - arrive_raw
53              max_wait = MAX_MEAL_WAIT if slot_type in ('lunch', 'dinner') else 60
54              if wait > max_wait: continue
55              arrive = float(poi['open_min'])
56          else:
57              arrive = arrive_raw
58          if arrive > poi['close_min']: continue
59          lw = LUNCH_RELAXED if relax_meal else LUNCH_ARRIVE
60          dw = DINNER_RELAXED if relax_meal else DINNER_ARRIVE
61          if slot_type == 'lunch' and not (lw[0] <= arrive <= lw[1]): continue
62          if slot_type == 'dinner' and not (dw[0] <= arrive <= dw[1]): continue
63          finish = arrive + poi['duration_min']
64          if (finish + back_t + dinner_buffer) - DAY_START_MIN > day_time: continue
65          add_cost = travel_cost(d_to) + poi['cost']
66          if poi['cost'] > 0 and add_cost > budget_left: continue
บรรทัด 39: candidates รายการผู้สมัครของช่องนี้
บรรทัด 40: วนทุกสถานที่
บรรทัด 41: ข้ามจุดที่ใช้ไปแล้ว
บรรทัด 42: ช่องเที่ยวห้ามเป็นร้านอาหาร
บรรทัด 43: ช่องมื้อต้องเป็นร้านอาหารเท่านั้น
บรรทัด 44: ถ้าเป็นโหมดเฉพาะของฟรี ข้ามจุดที่มีค่าเข้า
บรรทัด 45: ช่องเที่ยว: ข้ามจุดที่ใช้เวลาเกิน 4 ชั่วโมงหรือเกินเวลาเที่ยวที่เหลือของวัน
บรรทัด 46: ระยะจากตำแหน่งปัจจุบันถึงจุด d_to
บรรทัด 47: ระยะจากจุดกลับโรงแรม d_back
บรรทัด 48–49: เวลาเดินทางไปและกลับ
บรรทัด 50: เวลาที่ไปถึงถ้าไม่ต้องรอ
บรรทัด 51–55: ถ้ามาก่อนเปิด ให้รอ แต่รอได้ไม่เกิน 90 นาทีสำหรับมื้อ หรือ 60 นาทีสำหรับที่เที่ยว เกินแล้วข้ามจุดนี้ แล้วตั้งเวลาถึงเป็นเวลาเปิด
บรรทัด 56–57: ถ้ามาหลังเปิดอยู่แล้ว ใช้เวลาที่ถึงตามจริง
บรรทัด 58: ข้ามถ้าไปถึงหลังเวลาปิด
บรรทัด 59–60: เลือกช่วงเวลามื้อตามว่าผ่อนหรือไม่
บรรทัด 61–62: ช่องกลางวัน/เย็นต้องไปถึงอยู่ในช่วงเวลาของมื้อนั้น
บรรทัด 63: เวลาเสร็จ = ถึง + ระยะเวลาที่อยู่
บรรทัด 64: ข้ามถ้าเวลารวมของวัน (รวมกลับโรงแรมและเผื่อมื้อเย็น) เกินเพดาน
บรรทัด 65: ค่าใช้จ่ายที่เพิ่ม = ค่าเดินทาง (ตอนนี้ 0) + ค่าเข้า/ค่าอาหาร
บรรทัด 66: ข้ามถ้าจุดนั้นมีค่าใช้จ่ายและเกินงบที่เหลือ
บรรทัด 67–87  ให้คะแนนผู้สมัครและเลือกตัวที่ดีที่สุด
67          cat_count = day_categories.get(poi['category'], 0)
68          diversity_bonus = 1.0 if cat_count == 0 else (1.0 / (1 + cat_count * 0.5))
69          if scoring_mode == 'quality':
70              base_score = poi['score'] * diversity_bonus
71          else:
72              # ratio mode: ใช้ floor 80 เพื่อป้องกัน POI ฟรีใกล้ๆ ชนะจากระยะทางเสมอ
73              # → POI ฟรีทุกอันแข่งกันด้วย score เป็นหลัก + noise กระจาย diversity
74              # ค่าเดินทางไม่นับในงบ (COST_PER_KM=0) แต่ถ่วงระยะขับใน ranking เท่ากับค่าเดิม 10 บาท/km
75              effective_cost = max(add_cost, 80.0) + GREEDY_KM_PENALTY * d_to
76              base_score = (poi['score'] * diversity_bonus) / (effective_cost + 1.0)
77          noise = 1.0 + random.uniform(-random_factor, random_factor) if random_factor > 0 else 1.0
78          score = base_score * noise
79          candidates.append((score, poi, d_to, arrive, add_cost,
80                             (DAY_START_MIN + day_time) - (finish + back_t), arrive - arrive_raw, cat_count))
81      if not candidates: return None
82      if chooser is not None:
83          c = candidates[chooser(candidates)]
84          return (c[1], c[2], c[3])
85      candidates.sort(key=lambda x: x[0], reverse=True)
86      best, best_d_to, best_arrive = candidates[0][1], candidates[0][2], candidates[0][3]
87      return (best, best_d_to, best_arrive)
บรรทัด 67: นับจำนวนจุดหมวดเดียวกันที่เลือกไปแล้วในวันนี้
บรรทัด 68: โบนัสความหลากหลาย: หมวดใหม่ได้ 1.0 หมวดซ้ำลดลงตามจำนวนที่ซ้ำ
บรรทัด 69–70: โหมด quality ใช้คะแนนสถานที่คูณโบนัสโดยไม่สนต้นทุน
บรรทัด 71–76: โหมด ratio ใช้อัตราส่วนคะแนนต่อต้นทุน โดยใช้ต้นทุนขั้นต่ำ 80 กันจุดฟรีใกล้ ๆ ชนะตลอด และบวกค่าปรับระยะ GREEDY_KM_PENALTY × d_to ให้เลือกจุดใกล้กัน
บรรทัด 77: ถ้ามี random_factor ให้ใส่ noise ±ค่านั้นเพื่อสร้างความหลากหลาย ไม่เช่นนั้น noise = 1
บรรทัด 78: คะแนนสุดท้ายของผู้สมัคร
บรรทัด 79–80: เก็บผู้สมัครเป็นทูเพิลพร้อมข้อมูลที่ chooser (RL) ต้องใช้ เช่น เวลาเหลือ เวลารอ และจำนวนหมวด
บรรทัด 81: ถ้าไม่มีผู้สมัครเลย คืน None
บรรทัด 82–84: ถ้ามี chooser ให้ให้ฟังก์ชันนั้นเลือก index แล้วคืนค่า
บรรทัด 85: ไม่มี chooser ก็เรียงคะแนนจากมากไปน้อย
บรรทัด 86–87: คืนจุดที่คะแนนสูงสุด พร้อมระยะและเวลาถึง
บรรทัด 94–115  ฟังก์ชันหลัก `greedy_solve`: เตรียมตัวแปร
94  def greedy_solve(pois, hotel, days, budget, day_time=DAY_TIME_BUDGET,
95                   scoring_mode='ratio', random_factor=0.15, _alt=True):
96      """สร้าง routes ด้วย slot-based greedy (วนทุกวัน × ทุก slot ตาม DAY_PATTERN)
97      คืน routes: List[List[Dict]]  — routes[วัน][ลำดับ POI]
98      """
99      used_ids = set()
100      remaining_budget = float(budget)
101      routes = [[] for _ in range(days)]
102      per_day_budget = (budget / max(days, 1)) * 1.1
103
104      pois_shuffled = list(pois)
105      random.shuffle(pois_shuffled)
106
107      for day_idx in range(days):
108          current_pos = hotel
109          current_time = float(DAY_START_MIN)
110          day_categories = {}
111          day_budget_left = min(per_day_budget, remaining_budget)
112          past_lunch = False
113          sight_left = MAX_SIGHT_MIN
114          dinner_done = False
115
บรรทัด 94–95: ประกาศ greedy_solve รับจุดทั้งหมด โรงแรม จำนวนวัน งบ เพดานเวลา โหมดคะแนน (ratio หรือ quality) และ noise
บรรทัด 96–98: docstring: คืนแผนรายวัน routes[วัน][ลำดับ]
บรรทัด 99: used_ids จุดที่เลือกไปแล้วทั้งทริป (ห้ามซ้ำ)
บรรทัด 100: งบที่เหลือทั้งทริป
บรรทัด 101: เตรียมรายการว่างของแต่ละวัน
บรรทัด 102: งบต่อวันที่ยอมใช้ = งบรวม ÷ จำนวนวัน × 1.1
บรรทัด 104–105: สุ่มลำดับจุดเพื่อให้ผลต่างกันเมื่อรันหลายครั้ง (ใช้สร้าง seed หลากหลายให้ GA/Hybrid)
บรรทัด 107: วนทีละวัน
บรรทัด 108–109: เริ่มที่โรงแรม เวลา 08:00
บรรทัด 110: ตัวนับหมวดที่ใช้แล้วในวัน
บรรทัด 111: งบของวันนี้ = ค่าที่น้อยกว่าระหว่างงบต่อวันกับงบคงเหลือ
บรรทัด 112: ธงว่าผ่านมื้อกลางวันแล้วหรือยัง
บรรทัด 113: เวลาเที่ยวคงเหลือของวัน (เริ่ม 480 นาที)
บรรทัด 114: ธงว่ามื้อเย็นเสร็จแล้วหรือยัง
บรรทัด 116–127  วนทีละช่องของวัน
116          for slot_type in DAY_PATTERN:
117              if slot_type == 'lunch' and current_time < LUNCH_TRIGGER:
118                  current_time = float(LUNCH_TRIGGER)
119              elif slot_type == 'dinner' and current_time < DINNER_TRIGGER:
120                  current_time = float(DINNER_TRIGGER)
121
122              db = DINNER_BUFFER_MIN if (slot_type == 'attr' and past_lunch and not dinner_done) else 0
123
124              result = _find_best_for_slot(
125                  pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
126                  day_budget_left, day_categories, slot_type, scoring_mode,
127                  dinner_buffer=db, random_factor=random_factor, sight_left=sight_left)
บรรทัด 116: วนตามแพตเทิร์น 6 ช่อง
บรรทัด 117–120: ถ้าถึงช่องมื้อแต่เวลายังไม่ถึงเวลาตั้งต้นของมื้อ ให้เลื่อนเวลาไปที่ 11:30 (กลางวัน) หรือ 17:00 (เย็น)
บรรทัด 122: ถ้าเป็นช่องเที่ยวหลังมื้อกลางวันและยังไม่ทำมื้อเย็น ให้กันเวลา 150 นาทีไว้ให้มื้อเย็น
บรรทัด 124–127: เรียก _find_best_for_slot เป็นครั้งแรกด้วยเงื่อนไขปกติ
บรรทัด 129–162  กลไก fallback เพื่อให้มีมื้อครบ
129              if result is None and slot_type in ('lunch', 'dinner'):
130                  # Fallback 1: ขยายงบสำหรับมื้ออาหาร
131                  meal_cap = max(300, remaining_budget * 0.5)
132                  result = _find_best_for_slot(
133                      pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
134                      meal_cap, day_categories, slot_type, scoring_mode,
135                      dinner_buffer=0, random_factor=random_factor, sight_left=sight_left)
136
137              if result is None and slot_type in ('lunch', 'dinner'):
138                  # Fallback 2: ร้านอาหารใดก็ได้โดยไม่สนงบ (ต้องมีมื้ออาหาร)
139                  result = _find_best_for_slot(
140                      pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
141                      1e9, day_categories, slot_type, scoring_mode,
142                      dinner_buffer=0, random_factor=random_factor, sight_left=sight_left)
143
144              if result is None and slot_type in ('lunch', 'dinner'):
145                  # Fallback 3: ขยายช่วงเวลาเข้าร้าน (มื้ออาหารเป็น hard requirement)
146                  result = _find_best_for_slot(
147                      pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
148                      1e9, day_categories, slot_type, scoring_mode,
149                      dinner_buffer=0, random_factor=random_factor, sight_left=sight_left, relax_meal=True)
150
151              if result is None:
152                  # Fallback: เลือกเฉพาะ POI ฟรี
153                  result = _find_best_for_slot(
154                      pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
155                      1e9, day_categories, slot_type, scoring_mode,
156                      free_only=True, dinner_buffer=db, random_factor=random_factor, sight_left=sight_left)
157
158              if result is None and slot_type == 'attr' and not past_lunch:
159                  result = _find_best_for_slot(
160                      pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
161                      day_budget_left, day_categories, 'attr', scoring_mode,
162                      dinner_buffer=0, random_factor=random_factor, sight_left=sight_left)
บรรทัด 129–135: Fallback 1 (เฉพาะช่องมื้อ): ถ้าหาไม่ได้ ขยายงบมื้อเป็นมากกว่าของ 300 บาท หรือครึ่งหนึ่งของงบที่เหลือ
บรรทัด 137–142: Fallback 2: ถ้ายังไม่ได้ ร้านอาหารใดก็ได้โดยไม่สนงบ (มื้ออาหารเป็นข้อบังคับ)
บรรทัด 144–149: Fallback 3: ถ้ายังไม่ได้ ขยายช่วงเวลาเข้าร้าน (relax_meal=True)
บรรทัด 151–156: ถ้ายังไม่ได้ (ทุกช่อง) ลองเฉพาะจุดฟรี
บรรทัด 158–162: ช่องเที่ยวก่อนมื้อกลางวันที่ยังหาไม่ได้ ลองใหม่โดยไม่กันเวลามื้อเย็น
บรรทัด 164–182  บันทึกจุดที่เลือกและอัปเดตสถานะ
164              if slot_type == 'lunch': past_lunch = True
165              if slot_type == 'dinner': dinner_done = True
166              if result is None: continue
167
168              poi, d_to, arrive = result
169              used_ids.add(poi['id'])
170              routes[day_idx].append(poi)
171              if poi['category'] != 'restaurant': sight_left -= poi['duration_min']
172              current_time = arrive + poi['duration_min']
173              current_pos = poi
174              spent = travel_cost(d_to) + poi['cost']
175              remaining_budget -= spent
176              day_budget_left = max(0, day_budget_left - spent)
177              day_categories[poi['category']] = day_categories.get(poi['category'], 0) + 1
178
179          if routes[day_idx]:
180              d_back = haversine_km(current_pos['lat'], current_pos['lng'],
181                                    hotel['lat'], hotel['lng'])
182              remaining_budget -= travel_cost(d_back)
บรรทัด 164–165: ตั้งธงเมื่อผ่านช่องมื้อกลางวัน/เย็น
บรรทัด 166: ถ้าไม่มีจุดเลย ข้ามช่องนี้
บรรทัด 168: แกะค่า (จุด ระยะ เวลาถึง)
บรรทัด 169–170: บันทึกจุดว่าใช้แล้วและต่อท้ายเส้นทางของวัน
บรรทัด 171: ถ้าเป็นที่เที่ยว หักเวลาท่องเที่ยวคงเหลือ
บรรทัด 172–173: เลื่อนเวลาและตำแหน่งปัจจุบันไปที่จุดนั้น
บรรทัด 174–176: หักค่าใช้จ่ายออกจากงบทริปและงบวัน
บรรทัด 177: นับหมวดของจุดนั้น
บรรทัด 179–182: เมื่อวันนี้มีจุด หักค่าเดินทางกลับโรงแรม (ตอนนี้เป็น 0)
บรรทัด 183–190  เลือกระหว่างแผนโหมด quality และ ratio แล้วซ่อมงบ
183      if _alt and scoring_mode == 'quality' and evaluate_route(routes, hotel, float('inf'))['total_cost'] > budget:
184          # quality ไม่คิดค่าเดินทางตอนเลือก (โรงแรมไกลทำให้เกินงบแล้วต้องตัดจนแผนสั้น) — ลองแบบ ratio แล้วเก็บแผนที่คะแนนสูงกว่า
185          alt = greedy_solve(pois, hotel, days, budget, day_time, 'ratio', random_factor, _alt=False)
186          base = routes
187          s_alt = evaluate_route(alt, hotel, budget)
188          s_base = evaluate_route(_repaired(base, hotel, budget), hotel, budget)
189          return alt if (s_alt['valid'] and s_alt['total_score'] > s_base['total_score']) else _repaired(base, hotel, budget)
190      return _repaired(routes, hotel, budget)
บรรทัด 183: ถ้าเป็นโหมด quality แล้วแผนเกินงบ (เพราะไม่คิดต้นทุนตอนเลือก)
บรรทัด 185: ลองสร้างแผนโหมด ratio เทียบ (ปิด _alt กันวนซ้ำ)
บรรทัด 186–188: ประเมินคะแนนของแผนทั้งสอง (แผนเดิมผ่านการซ่อมงบก่อน)
บรรทัด 189: เก็บแผน ratio ถ้าผ่านข้อจำกัดและคะแนนสูงกว่า ไม่เช่นนั้นเก็บแผนเดิมที่ซ่อมแล้ว
บรรทัด 190: กรณีปกติคืนแผนที่ซ่อมงบแล้ว
บรรทัด 193–215  ซ่อมงบ
193  def _repaired(routes, hotel, budget):
194      routes = [list(d) for d in routes]
195      # ซ่อมงบ: ถ้ารวมแล้วเกินงบ (ค่ามื้อ/เดินทางกลับ) ถอด attraction ที่แพงสุดจนอยู่ในงบ — ใช้ได้กับทุกโหมด
196      # ซ่อมงบ: ถ้ารวมแล้วเกินงบ (ค่ามื้อ/ค่าเดินทาง) ถอด attraction ที่ถอดแล้วประหยัดได้มากที่สุดต่อคะแนนที่เสีย
197      total = lambda rs: evaluate_route(rs, hotel, float('inf'))['total_cost']
198      cur = total(routes)
199      for _ in range(60):
200          if cur <= budget:
201              break
202          best = None
203          for d, day in enumerate(routes):
204              for i, p in enumerate(day):
205                  if p['category'] == 'restaurant':
206                      continue
207                  c = total(routes[:d] + [day[:i] + day[i + 1:]] + routes[d + 1:])
208                  save = cur - c
209                  if save > 0 and (best is None or save / p['score'] > best[0]):
210                      best = (save / p['score'], d, i, c)
211          if best is None:
212              break
213          _r, d, i, cur = best
214          routes[d].pop(i)
215      return routes
บรรทัด 193: ประกาศ _repaired รับแผน โรงแรม งบ
บรรทัด 194: คัดลอกแผนไม่ให้แก้ของเดิม
บรรทัด 195–196: คอมเมนต์: ถ้ารวมเกินงบ ให้ถอดที่เที่ยวที่ถอดแล้วประหยัดได้มากที่สุดต่อคะแนนที่เสีย
บรรทัด 197: ฟังก์ชันย่อย total คำนวณค่าใช้จ่ายรวมของแผนด้วย ➜ evaluate_route() ใน algorithm/utils.py
บรรทัด 198: ค่าใช้จ่ายปัจจุบัน
บรรทัด 199: วนไม่เกิน 60 รอบ
บรรทัด 200–201: ถ้าอยู่ในงบแล้ว หยุด
บรรทัด 202: best เก็บทางเลือกถอดที่ดีที่สุด
บรรทัด 203–204: วนทุกจุดของทุกวัน
บรรทัด 205–206: ไม่ถอดร้านอาหาร
บรรทัด 207: คำนวณค่าใช้จ่ายถ้าถอดจุดนี้
บรรทัด 208: ประหยัดได้เท่าไร
บรรทัด 209–210: เก็บจุดที่ประหยัดต่อคะแนนที่เสียมากที่สุด
บรรทัด 211–212: ถ้าไม่มีทางถอดที่ประหยัดได้ หยุด
บรรทัด 213–214: ถอดจุดที่ดีที่สุดแล้ววนต่อ
บรรทัด 215: คืนแผนที่ซ่อมแล้ว (ฝั่ง Hybrid มีตัวซ่อมงบของตัวเอง ดู ➜ _budget_repair() ใน algorithm/hybrid.py)

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/hybrid.py
algorithm/rl.py
algorithm/utils.py