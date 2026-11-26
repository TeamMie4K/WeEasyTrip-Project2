<!-- converted from algorithm__utils.py.docx -->

คู่มือโค้ด: algorithm/utils.py
ฟังก์ชันพื้นฐาน: ระยะทาง เวลาเดินทาง และตัวตรวจสอบแผน
ไฟล์ต้นฉบับ: algorithm/utils.py (220 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ไฟล์ฐานที่ทุกอัลกอริทึมเรียกใช้ เก็บค่าคงที่ของกติกาการเที่ยว (เวลามื้อ เพดานเวลาต่อวัน จำนวนจุดต่อวัน) ฟังก์ชันคำนวณระยะทาง/เวลาเดินทาง และ evaluate_route ซึ่งเป็นตัววัดคะแนนและตรวจข้อจำกัดของแผนทุกแผน ใช้ร่วมกับ ➜ algorithm/greedy.py ➜ algorithm/genetic.py ➜ algorithm/hybrid.py ➜ algorithm/ils.py ➜ algorithm/pareto.py ➜ algorithm/rl.py และ ➜ backend/main.py

บรรทัด 1–14  หัวไฟล์และการนำเข้า
1  # -*- coding: utf-8 -*-
2  """
3  utils.py - Helper functions for distance, time, cost, and route evaluation
4
5  Provides:
6    - load_data:     โหลด POI + hotel จาก JSON
7    - haversine_km:  คำนวณระยะทาง
8    - evaluate_route: ตรวจสอบ constraint ทั้งหมดของ routes
9    - print_result:  แสดงผลสรุป
10  """
11  import json
12  import math
13  from contextvars import ContextVar
14  from typing import Dict, List, Tuple
บรรทัด 1: บรรทัดแรกประกาศว่าไฟล์เก็บเป็นอักขระ UTF-8 เพื่อให้ภาษาไทยในคอมเมนต์ไม่เพี้ยน
บรรทัด 2–10: docstring อธิบายว่าไฟล์นี้ให้ฟังก์ชันอะไรบ้าง (โหลดข้อมูล คำนวณระยะทาง ตรวจแผน แสดงผล)
บรรทัด 11: นำเข้า json สำหรับอ่านไฟล์ข้อมูลจังหวัด
บรรทัด 12: นำเข้า math สำหรับ sin cos asin ในสูตรระยะทาง
บรรทัด 13: นำเข้า ContextVar ที่ใช้เก็บโปรไฟล์การเดินทางแยกตาม request (ดูบรรทัด 48)
บรรทัด 14: นำเข้าชนิดข้อมูล Dict List Tuple เพื่อใส่ type hint ให้อ่านง่าย
บรรทัด 16–33  ค่าคงที่ของกติกาการเที่ยว
16  # ============================================================
17  # ค่าคงที่
18  # ============================================================
19  AVG_SPEED_KMH = 40
20  COST_PER_KM = 0     # ไม่นับค่าเดินทางในงบ (ผู้ใช้กำหนด: งบ = ค่าเข้าชม + ค่าอาหาร); เดิม 10 บาท/กม. ทำให้งบน้อยไปที่เที่ยวไกลกันไม่ได้
21  DAY_TIME_BUDGET = 840       # 14 hours (8:00 - 22:00)
22  DAY_START_MIN = 480         # 8:00
23
24  # โปรไฟล์การเดินทางรายจังหวัด: (road_factor, speed_kmh) — ปรับเทียบจาก OSRM ใน data/calibrate_travel.py
25  # ใช้ ContextVar เพื่อให้ API ที่ประมวลผลหลาย request พร้อมกันไม่ปนกัน; ค่าเริ่มต้นคือแบบเดิม (เส้นตรง, 40 km/h)
26  # กติกาความสมจริงของวัน: ช่วงเวลาเริ่มมื้อ (นาทีจากเที่ยงคืน), เวลาเที่ยวต่อวันไม่เกิน MAX_SIGHT_MIN
27  LUNCH_WIN = (660, 870)      # 11:00-14:30
28  DINNER_WIN = (1020, 1200)   # 17:00-20:00
29  MEAL_SPLIT = 930            # ร้านที่ถึงก่อน 15:30 นับเป็นมื้อกลางวัน ไม่งั้นมื้อเย็น
30  MAX_SIGHT_MIN = 480         # เวลาท่องเที่ยว (ไม่รวมมื้อ/เดินทาง) สูงสุดต่อวัน 8 ชม.
31  TIME_WEIGHT = 0.01         # คะแนนที่หักต่อนาทีของเวลาทั้งวัน (ให้แผน 6 จุดใช้เวลาคุ้มขึ้น) — ปรับด้วยการทดลอง
32  MAX_ATTRS = 4              # สถานที่เที่ยวสูงสุดต่อวัน (+ มื้ออาหาร 2 = 6 จุด/วัน ตรงกับ Project 1: attr-attr-lunch-attr-attr-dinner)
33  MORNING_SPAN = 190          # นาทีที่ใช้ได้ก่อนมื้อกลางวัน (08:00 -> ~11:10)
บรรทัด 19: AVG_SPEED_KMH ความเร็วเฉลี่ยตั้งต้น 40 กม./ชม. ใช้เมื่อยังไม่มีโปรไฟล์ของจังหวัด
บรรทัด 20: COST_PER_KM = 0 ค่าเดินทางต่อกิโลเมตร ตั้งเป็น 0 หมายถึงไม่นับค่าเดินทางในงบ (งบ = ค่าเข้าชม + ค่าอาหาร) เดิมเคยเป็น 10 บาท/กม. แต่ทำให้งบน้อยไปที่เที่ยวไกลไม่ได้
บรรทัด 21: DAY_TIME_BUDGET = 840 เวลาทั้งวันสูงสุด 840 นาที (14 ชั่วโมง คือ 08:00–22:00) ใช้เป็นค่าเริ่มต้นของ evaluate_route
บรรทัด 22: DAY_START_MIN = 480 เริ่มเที่ยว 08:00 (นับเป็นนาทีจากเที่ยงคืน)
บรรทัด 24–26: คอมเมนต์อธิบายว่าโปรไฟล์การเดินทางรายจังหวัดปรับเทียบจาก OSRM (ดู ➜ data/calibrate_travel.py) และใช้ ContextVar กันค่าปนกันระหว่าง request
บรรทัด 27: LUNCH_WIN ช่วงเวลาเริ่มมื้อกลางวัน 11:00–14:30 (660–870 นาที)
บรรทัด 28: DINNER_WIN ช่วงเวลาเริ่มมื้อเย็น 17:00–20:00 (1020–1200 นาที)
บรรทัด 29: MEAL_SPLIT = 930 ร้านที่ไปถึงก่อน 15:30 นับเป็นมื้อกลางวัน ไม่เช่นนั้นเป็นมื้อเย็น
บรรทัด 30: MAX_SIGHT_MIN = 480 เวลาท่องเที่ยวจริงต่อวัน (ไม่รวมมื้อและเดินทาง) ไม่เกิน 8 ชั่วโมง
บรรทัด 31: TIME_WEIGHT = 0.01 คะแนนที่หักต่อนาทีของเวลาทั้งวัน ทำให้แผน 6 จุดที่ใช้เวลาน้อยกว่าได้เปรียบ ค่านี้ได้จากการทดลองเล็ก ๆ (ใช้ใน ➜ day_objective() ใน algorithm/ils.py)
บรรทัด 32: MAX_ATTRS = 4 สถานที่ท่องเที่ยวสูงสุดต่อวัน รวมมื้ออาหาร 2 มื้อเป็น 6 จุดต่อวัน
บรรทัด 33: MORNING_SPAN = 190 เวลาช่วงเช้าที่ใช้ได้ก่อนมื้อกลางวัน (ประมาณ 08:00 ถึง 11:10) ใช้แบ่งจุดเช้า/บ่าย
บรรทัด 36–45  แบ่งสถานที่เป็นเช้า บ่าย ค่ำ
36  def split_attrs(attrs: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
37      """แบ่ง attraction เป็นช่วงเช้า/บ่าย/ค่ำ: จุดที่เปิดหลัง 17:00 (โชว์, ตลาดกลางคืน) ไปหลังมื้อเย็น
38      ที่เหลือแบ่งเช้า/บ่ายตามเวลาที่ใช้จริง (ประมาณ: duration + 25 นาทีเดินทางต่อจุด)"""
39      evening = [p for p in attrs if p['open_min'] >= 1020]
40      day = [p for p in attrs if p['open_min'] < 1020]
41      t, k = 0, 0
42      while k < len(day) and t < MORNING_SPAN:
43          t += day[k]['duration_min'] + 25
44          k += 1
45      return day[:k], day[k:], evening
บรรทัด 36: ประกาศ split_attrs รับรายการสถานที่ท่องเที่ยว คืน 3 กลุ่ม (เช้า บ่าย ค่ำ)
บรรทัด 37–38: docstring: จุดที่เปิดหลัง 17:00 (โชว์ ตลาดกลางคืน) ไปช่วงค่ำ ที่เหลือแบ่งเช้า/บ่ายตามเวลาที่ใช้จริง
บรรทัด 39: evening เก็บจุดที่เปิดตั้งแต่ 17:00 (1020 นาที) ขึ้นไป
บรรทัด 40: day เก็บจุดที่เปิดก่อน 17:00
บรรทัด 41: ตั้งตัวสะสมเวลา t และตัวนับจุด k เป็น 0
บรรทัด 42: วนต่อตราบที่ยังมีจุดและเวลาสะสมยังไม่ถึง MORNING_SPAN
บรรทัด 43: บวกเวลาของจุดนั้น (ระยะเวลาเที่ยว + 25 นาทีประมาณเวลาเดินทาง) เข้าเวลาสะสม
บรรทัด 44: เลื่อนไปจุดถัดไป
บรรทัด 45: คืนค่า (จุดช่วงเช้า = day[:k], ช่วงบ่าย = day[k:], ช่วงค่ำ) ผู้เรียกหลักคือ ➜ greedy_solve() ใน algorithm/greedy.py
บรรทัด 48–53  โปรไฟล์การเดินทางรายจังหวัด
48  _PROFILE: ContextVar = ContextVar('travel_profile', default=(1.0, AVG_SPEED_KMH))
49
50
51  def set_travel_profile(road_factor: float = 1.0, speed_kmh: float = AVG_SPEED_KMH) -> None:
52      """ตั้งค่าตัวคูณระยะทางถนน/เส้นตรง และความเร็วเฉลี่ย สำหรับ context ปัจจุบัน"""
53      _PROFILE.set((float(road_factor), float(speed_kmh)))
บรรทัด 48: _PROFILE ตัวแปรชนิด ContextVar เก็บคู่ (ตัวคูณระยะถนน, ความเร็ว) ค่าตั้งต้น (1.0, 40) แต่ละ request/เธรดมีค่าของตัวเอง
บรรทัด 51: ประกาศ set_travel_profile ให้โค้ดอื่นตั้งโปรไฟล์ของจังหวัดก่อนคำนวณ
บรรทัด 52: docstring: ตั้งตัวคูณระยะถนนต่อเส้นตรงและความเร็วเฉลี่ยของ context ปัจจุบัน
บรรทัด 53: เก็บค่าเป็น float ลงใน _PROFILE ฟังก์ชันนี้ถูกเรียกจาก ➜ get_province() ใน backend/main.py และสคริปต์ทดลองเช่น ➜ experiments/run_province_experiments.py
บรรทัด 60–64  โหลดข้อมูลจังหวัด
60  def load_data(path: str) -> Tuple[List[Dict], List[Dict]]:
61      """โหลด POI และโรงแรมจากไฟล์ JSON"""
62      with open(path, 'r', encoding='utf-8') as f:
63          data = json.load(f)
64      return data['pois'], data['hotels']
บรรทัด 60: ประกาศ load_data รับพาธไฟล์ JSON คืน (รายการ POI, รายการโรงแรม)
บรรทัด 61: docstring
บรรทัด 62: เปิดไฟล์แบบอ่านด้วย UTF-8
บรรทัด 63: แปลง JSON เป็น dict
บรรทัด 64: คืนค่า pois และ hotels จากข้อมูล
บรรทัด 71–80  ระยะทางระหว่างพิกัด (Haversine)
71  def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
72      """ระยะทางระหว่างสองพิกัด (km): Haversine (เส้นตรง) × road_factor ของจังหวัด = ประมาณระยะทางถนน"""
73      R = 6371.0
74      dlat = math.radians(lat2 - lat1)
75      dlng = math.radians(lng2 - lng1)
76      a = (math.sin(dlat / 2) ** 2 +
77           math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
78           math.sin(dlng / 2) ** 2)
79      c = 2 * math.asin(math.sqrt(a))
80      return R * c * _PROFILE.get()[0]
บรรทัด 71: ประกาศ haversine_km รับ lat/lng สองจุด
บรรทัด 72: docstring: ระยะเส้นตรงคูณตัวคูณถนนของจังหวัด เป็นการประมาณระยะทางถนน
บรรทัด 73: R รัศมีโลก 6,371 กม.
บรรทัด 74–75: แปลงผลต่างละติจูดและลองจิจูดเป็นเรเดียน
บรรทัด 76–78: คำนวณค่า a ตามสูตร Haversine
บรรทัด 79: คำนวณมุมศูนย์กลาง c
บรรทัด 80: คืนระยะทาง = R × c × ตัวคูณถนน (_PROFILE.get()[0])
บรรทัด 83–93  เวลาเดินทาง
83  # เวลาเดินทางสมจริงขึ้น: ความเร็วที่ปรับเทียบด้วย OSRM เป็นแบบรถไม่ติด (free-flow) ไม่รวมการจราจรและเวลาหาที่จอด/เดินเข้าจุด
84  # จึงคูณตัวคูณการจราจร (TRAFFIC_FACTOR) และบวกเวลาเผื่อต่อการย้ายจุดที่ไกลกว่า 0.3 กม. (TRANSFER_BUFFER_MIN) — สองค่านี้เป็นสมมติฐาน ไม่ได้วัดจริง
85  TRAFFIC_FACTOR = 1.25
86  TRANSFER_BUFFER_MIN = 10.0
87  BUFFER_MIN_KM = 0.3
88
89
90  def travel_time_min(dist_km: float) -> float:
91      """เวลาเดินทางเป็นนาที = ระยะทาง/ความเร็วเฉลี่ยตามโปรไฟล์จังหวัด × ตัวคูณการจราจร + เวลาเผื่อจอด/เดิน (ถ้าย้ายไกลกว่า 0.3 กม.)"""
92      t = (dist_km / _PROFILE.get()[1]) * 60.0 * TRAFFIC_FACTOR
93      return t + (TRANSFER_BUFFER_MIN if dist_km >= BUFFER_MIN_KM else 0.0)
บรรทัด 83–84: คอมเมนต์อธิบายว่าความเร็วจาก OSRM เป็นแบบรถไม่ติด จึงคูณตัวคูณการจราจรและบวกเวลาเผื่อจอดรถ สองค่านี้เป็นสมมติฐานที่ไม่ได้วัดจริง
บรรทัด 85: TRAFFIC_FACTOR = 1.25 เวลาเดินทางจริงนานกว่าแบบรถไม่ติด 25%
บรรทัด 86: TRANSFER_BUFFER_MIN = 10.0 เวลาเผื่อหาที่จอด/เดินเข้าจุด 10 นาทีต่อการย้ายจุด
บรรทัด 87: BUFFER_MIN_KM = 0.3 ย้ายจุดที่ใกล้กว่า 0.3 กม. ไม่ต้องบวกเวลาเผื่อ
บรรทัด 90: ประกาศ travel_time_min รับระยะทาง (กม.) คืนนาที
บรรทัด 92: เวลา = ระยะ ÷ ความเร็ว × 60 นาที × ตัวคูณการจราจร
บรรทัด 93: บวกเวลาเผื่อ 10 นาทีถ้าระยะตั้งแต่ 0.3 กม. ขึ้นไป
บรรทัด 96–98  ค่าเดินทางเป็นเงิน
96  def travel_cost(dist_km: float) -> float:
97      """ค่าเดินทางเป็นบาท จากระยะทาง km (อัตรา COST_PER_KM; ตั้งเป็น 0 = ไม่นับ)"""
98      return dist_km * COST_PER_KM
บรรทัด 96: ประกาศ travel_cost
บรรทัด 97: docstring: อัตรา COST_PER_KM ตั้งเป็น 0 แปลว่าไม่นับ
บรรทัด 98: คืนระยะ × อัตรา (ตอนนี้ได้ 0 เสมอ)
บรรทัด 105–131  ประเมินแผน: ตั้งต้นและเตรียมข้อมูลรายวัน
105  def evaluate_route(routes_per_day: List[List[Dict]], hotel: Dict,
106                     budget: float, day_time: float = DAY_TIME_BUDGET) -> Dict:
107      """ประเมินคุณภาพ routes พร้อมตรวจสอบ constraint ทั้งหมด (งบ / เวลา / เวลาปิด)"""
108      total_score = 0.0
109      total_cost = 0.0
110      days_detail = []
111      violations = []
112
113      for day_idx, day_pois in enumerate(routes_per_day):
114          day_dist = 0.0
115          day_cost_local = 0.0
116          day_score_local = 0.0
117          current_time = float(DAY_START_MIN)
118          arrivals = []
119          sight = 0
120          meals_seen = 0
121          idle = 0.0
122
123          if not day_pois:
124              days_detail.append({
125                  'pois': [], 'distance_km': 0.0, 'time_min': 0.0,
126                  'cost': 0.0, 'score': 0.0, 'arrivals': []
127              })
128              continue
129
130          path = [hotel] + day_pois + [hotel]
131
บรรทัด 105–106: ประกาศ evaluate_route รับแผนรายวัน (list ของ list ของ POI) โรงแรม งบ และเวลาสูงสุดต่อวัน
บรรทัด 107: docstring: ประเมินคุณภาพและตรวจข้อจำกัดงบ เวลา เวลาปิด
บรรทัด 108–109: ตัวสะสมคะแนนรวมและค่าใช้จ่ายรวมของทั้งทริป
บรรทัด 110: days_detail เก็บรายละเอียดรายวันไว้คืนให้ผู้เรียก
บรรทัด 111: violations เก็บข้อความที่ผิดข้อจำกัด
บรรทัด 113: วนทีละวัน
บรรทัด 114–116: ตัวสะสมระยะทาง ค่าใช้จ่าย และคะแนนของวันนั้น
บรรทัด 117: เวลาปัจจุบันเริ่มที่ 08:00
บรรทัด 118: arrivals เก็บเวลาที่ไปถึงแต่ละจุด
บรรทัด 119: sight สะสมเวลาท่องเที่ยวจริง (ไม่รวมมื้อ)
บรรทัด 120: meals_seen นับจำนวนมื้อที่ผ่านมา ใช้แยกกลางวัน/เย็น
บรรทัด 121: idle สะสมเวลารอก่อนมื้อ
บรรทัด 123–128: ถ้าวันนั้นว่าง ใส่รายละเอียดวันว่างแล้วข้ามไปวันถัดไป
บรรทัด 130: สร้างเส้นทางของวัน: โรงแรม → จุดต่าง ๆ → กลับโรงแรม
บรรทัด 132–163  ไล่ทีละช่วงของเส้นทาง
132          for i in range(len(path) - 1):
133              d = haversine_km(path[i]['lat'], path[i]['lng'],
134                               path[i + 1]['lat'], path[i + 1]['lng'])
135              t = travel_time_min(d)
136              c = travel_cost(d)
137              day_dist += d
138              day_cost_local += c
139              current_time += t
140
141              if i + 1 < len(path) - 1:
142                  poi = path[i + 1]
143                  if current_time < poi['open_min']:
144                      current_time = float(poi['open_min'])
145                  if poi['category'] == 'restaurant':
146                      lo, hi = LUNCH_WIN if (meals_seen == 0 and current_time < MEAL_SPLIT) else DINNER_WIN
147                      meals_seen += 1
148                      if current_time < lo:
149                          idle += lo - current_time
150                          current_time = float(lo)          # รอ/พักจนถึงเวลามื้อ (เวลาที่รอนับรวมในเวลาต่อวัน)
151                      elif current_time > hi:
152                          violations.append(f"Day {day_idx + 1}: ถึง {poi['id']} สายเกินช่วงมื้อ")
153                  else:
154                      sight += poi['duration_min']
155                  if current_time > poi['close_min']:      # ตรวจหลังรอช่วงมื้อ: ร้านที่ปิดก่อน 17:00 ใช้เป็นมื้อเย็นไม่ได้
156                      violations.append(
157                          f"Day {day_idx + 1}: ไปถึง {poi['id']} หลังเวลาปิด"
158                      )
159                  arrivals.append((poi['id'], int(current_time)))
160                  day_score_local += poi['score']
161                  day_cost_local += poi['cost']
162                  current_time += poi['duration_min']
163
บรรทัด 132: วนทีละช่วง (จากจุด i ไป i+1)
บรรทัด 133–134: คำนวณระยะทางช่วงนั้นด้วย haversine_km
บรรทัด 135: เวลาเดินทางช่วงนั้น
บรรทัด 136: ค่าเดินทางช่วงนั้น (0 ตามค่าปัจจุบัน)
บรรทัด 137–139: สะสมระยะทาง ค่าใช้จ่าย และเลื่อนเวลาปัจจุบัน
บรรทัด 141: ตรวจว่าจุดปลายทางเป็นสถานที่จริง ไม่ใช่การกลับโรงแรม
บรรทัด 142: poi คือจุดที่กำลังไปถึง
บรรทัด 143–144: ถ้าไปถึงก่อนเวลาเปิด ให้รอจนเปิด
บรรทัด 145: ถ้าเป็นร้านอาหาร
บรรทัด 146: เลือกช่วงมื้อ: มื้อแรกที่ถึงก่อน 15:30 เป็นมื้อกลางวัน นอกนั้นเป็นมื้อเย็น
บรรทัด 147: นับมื้อ
บรรทัด 148–150: ถ้าไปถึงก่อนช่วงมื้อ ให้รอ (นับเป็นเวลา idle) แล้วเลื่อนเวลาไปที่ต้นช่วงมื้อ
บรรทัด 151–152: ถ้าไปถึงสายกว่าช่วงมื้อ บันทึกว่าผิดข้อจำกัด
บรรทัด 153–154: ถ้าไม่ใช่ร้านอาหาร สะสมเวลาท่องเที่ยวจริงของจุดนั้น
บรรทัด 155–158: ถ้าเวลาปัจจุบันเกินเวลาปิด บันทึกผิดข้อจำกัด (ตรวจหลังรอมื้อ ร้านที่ปิดก่อน 17:00 จึงเป็นมื้อเย็นไม่ได้)
บรรทัด 159: บันทึกเวลาที่ไปถึงจุดนี้
บรรทัด 160–161: บวกคะแนนและค่าใช้จ่ายของจุดเข้าตัวสะสมของวัน
บรรทัด 162: เลื่อนเวลาตามระยะเวลาที่อยู่ที่จุดนั้น
บรรทัด 164–195  ตรวจเวลารวมของวันและสรุปผล
164          if sight > MAX_SIGHT_MIN:
165              violations.append(f"Day {day_idx + 1}: เวลาท่องเที่ยวเกิน ({sight} > {MAX_SIGHT_MIN} นาที)")
166          day_time_total = current_time - DAY_START_MIN
167          if day_time_total > day_time:
168              violations.append(
169                  f"Day {day_idx + 1}: ใช้เวลาเกิน ({day_time_total:.0f} > {day_time} นาที)"
170              )
171
172          days_detail.append({
173              'pois': [p['id'] for p in day_pois],
174              'distance_km': round(day_dist, 2),
175              'time_min': round(day_time_total, 1),
176              'cost': round(day_cost_local, 0),
177              'score': round(day_score_local, 1),
178              'idle_min': round(idle),
179              'arrivals': arrivals
180          })
181          total_score += day_score_local
182          total_cost += day_cost_local
183
184      if total_cost > budget:
185          violations.append(f"งบประมาณเกิน: {total_cost:.0f} > {budget}")
186
187      return {
188          'total_score': round(total_score, 1),
189          'total_cost': round(total_cost, 0),
190          'days_detail': days_detail,
191          'valid': len(violations) == 0,
192          'violations': violations
193      }
194
195
บรรทัด 164–165: ถ้าเวลาท่องเที่ยวจริงเกิน 480 นาที บันทึกผิดข้อจำกัด
บรรทัด 166: เวลาทั้งวัน = เวลาตอนกลับถึง ลบเวลาเริ่ม
บรรทัด 167–170: ถ้าเกินเพดานเวลาต่อวัน บันทึกผิดข้อจำกัด
บรรทัด 172–180: เก็บรายละเอียดของวันนี้ (รายชื่อจุด ระยะทาง เวลา ค่าใช้จ่าย คะแนน เวลารอ เวลาถึง) ใช้โดย ➜ day_objective() ใน algorithm/ils.py และหน้าเว็บ
บรรทัด 181–182: บวกคะแนนและค่าใช้จ่ายของวันเข้ายอดรวมทริป
บรรทัด 184–185: ถ้าค่าใช้จ่ายรวมเกินงบ บันทึกผิดข้อจำกัด
บรรทัด 187–193: คืนผลรวมคะแนน ค่าใช้จ่าย รายละเอียดรายวัน ธง valid (ไม่มีการผิดข้อจำกัด) และรายการข้อความผิดข้อจำกัด ผู้ใช้หลักคือ ➜ fitness() ใน algorithm/genetic.py และ ➜ hybrid_solve() ใน algorithm/hybrid.py
บรรทัด 200–220  แสดงผลทางหน้าจอ
200  def print_result(result: Dict, label: str = '', elapsed_ms: float = None):
201      """แสดงผลสรุป: score, cost, valid, violations และรายละเอียดแต่ละวัน"""
202      print('=' * 60)
203      if label:
204          print(f"  {label}")
205          print('=' * 60)
206      print(f"  Total score : {result['total_score']}")
207      print(f"  Total cost  : {result['total_cost']:.0f}")
208      print(f"  Valid       : {result['valid']}")
209      if elapsed_ms is not None:
210          print(f"  Runtime     : {elapsed_ms:.1f} ms")
211      if result['violations']:
212          print(f"  Violations  : {len(result['violations'])}")
213          for v in result['violations'][:3]:
214              print(f"    - {v}")
215      print('  Days:')
216      for i, d in enumerate(result['days_detail']):
217          print(f"    Day {i + 1}: {len(d['pois'])} จุด - "
218                f"score={d['score']}, time={d['time_min']:.0f}m, "
219                f"cost={d['cost']:.0f}, dist={d['distance_km']}km")
220          print(f"      {d['pois']}")
บรรทัด 200: ประกาศ print_result สำหรับพิมพ์ผลตอนทดลองเอง
บรรทัด 201: docstring
บรรทัด 202–205: พิมพ์เส้นคั่นและชื่อป้ายกำกับ
บรรทัด 206–208: พิมพ์คะแนนรวม ค่าใช้จ่าย และสถานะ valid
บรรทัด 209–210: ถ้ามีเวลารัน ให้พิมพ์เป็นมิลลิวินาที
บรรทัด 211–214: ถ้ามีการผิดข้อจำกัด พิมพ์จำนวนและ 3 รายการแรก
บรรทัด 215–220: พิมพ์สรุปแต่ละวัน (จำนวนจุด คะแนน เวลา ค่าใช้จ่าย ระยะทาง และรายชื่อจุด)

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
algorithm/ils.py
algorithm/pareto.py
algorithm/rl.py
backend/main.py
data/calibrate_travel.py
experiments/run_province_experiments.py