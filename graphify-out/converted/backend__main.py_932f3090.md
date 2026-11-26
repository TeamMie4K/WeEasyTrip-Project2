<!-- converted from backend__main.py.docx -->

คู่มือโค้ด: backend/main.py
FastAPI Backend ของ WeEasyTrip (API สร้างแพ็กเกจ ปรับแผน เซสชันร่วมกัน และให้บริการหน้าเว็บ)
ไฟล์ต้นฉบับ: backend/main.py (960 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: จุดรวมของระบบฝั่งเซิร์ฟเวอร์: โหลดข้อมูลจังหวัดทั้งหมดเข้าหน่วยความจำ รับคำขอจากหน้าเว็บ (➜ frontend/app.js และ ➜ frontend/extras.js) แล้วเรียกอัลกอริทึมใน algorithm/ ได้แก่ ➜ greedy_solve() ใน algorithm/greedy.py ➜ genetic_solve() ใน algorithm/genetic.py ➜ hybrid_solve() ใน algorithm/hybrid.py ➜ reoptimize_solve() ใน algorithm/hybrid.py และ ➜ nsga2_solve() ใน algorithm/pareto.py จากนั้นจัดงบ ตรวจและซ่อมแผนฝั่งเซิร์ฟเวอร์ก่อนส่ง JSON กลับ เซิร์ฟเวอร์ยังให้บริการไฟล์หน้าเว็บแบบ static ด้วย

บรรทัด 1–47  นำเข้าและตั้งค่าเริ่มต้น
1  # -*- coding: utf-8 -*-
2  """
3  main.py - FastAPI Backend สำหรับระบบ WeEasyTrip
4
5  Endpoints:
6    GET  /api/health    — ตรวจสอบสถานะ API
7    GET  /api/pois      — ดึงข้อมูล POI และโรงแรมทั้งหมด
8    POST /api/packages  — สร้าง 3 แพ็กเกจ (Budget / Standard / Premium)
9    POST /api/recompute — คำนวณใหม่หลังผู้ใช้แก้ไข route
10  """
11  import sys, os, time, random, secrets, threading, asyncio
12  from typing import List, Optional
13
14  THIS_DIR = os.path.dirname(os.path.abspath(__file__))
15  sys.path.insert(0, os.path.join(os.path.dirname(THIS_DIR), 'algorithm'))
16
17  from fastapi import FastAPI, HTTPException, Header, Request
18  from fastapi.middleware.cors import CORSMiddleware
19  from fastapi.responses import JSONResponse
20  from fastapi.staticfiles import StaticFiles
21  from pydantic import BaseModel, Field
22
23  from utils import load_data, evaluate_route, set_travel_profile, haversine_km, MAX_ATTRS
24  from greedy import greedy_solve
25  from genetic import genetic_solve
26  from hybrid import hybrid_solve, reoptimize_solve, infeasible_locks
27  from pareto import nsga2_solve
28
29  import json
30  DATA_DIR = os.path.join(os.path.dirname(THIS_DIR), 'data')
31  with open(os.path.join(DATA_DIR, 'provinces.json'), encoding='utf-8') as _f:
32      PROVINCES = json.load(_f)
33  DEFAULT_PROVINCE = 'phuket'
34  try:   # จังหวัดที่ผ่านเกณฑ์ผ่อนปรน (ข้อมูลน้อย) — ใช้แสดงป้ายเตือนที่หน้าเว็บ
35      with open(os.path.join(DATA_DIR, 'provinces_status.json'), encoding='utf-8') as _f:
36          SPARSE = {k for k, v in json.load(_f).items() if v.get('sparse')}
37  except Exception:
38      SPARSE = set()
39  sys.path.insert(0, DATA_DIR)
40  from thai_provinces import PROVINCES_77, EXTRA_AREAS   # รายชื่อ 77 จังหวัด (ใช้แสดงรายการที่ยังไม่พร้อม)
41  # นโยบาย RL ที่ฝึกแล้ว (algorithm/rl_policy.json) ใช้เป็น seed เพิ่มของ Hybrid เมื่อเลือก algorithm='hybrid_rl' (โหมด Developer)
42  try:
43      import numpy as _np
44      RL_THETA = _np.array(json.load(open(os.path.join(os.path.dirname(THIS_DIR), 'algorithm', 'rl_policy.json'), encoding='utf-8'))['theta'])
45  except Exception:
46      RL_THETA = None
47  DIVERSITY_WEIGHT = 1.5   # น้ำหนักความหลากหลายของหมวดใน fitness ของ Hybrid (0 = แบบ Project 1)
บรรทัด 1–10: docstring ระบุ endpoint หลัก (health, pois, packages, recompute) ส่วน endpoint อื่น ๆ ดูด้านล่างของไฟล์
บรรทัด 11: นำเข้าโมดูลมาตรฐาน (sys, os, time, random, secrets, threading, asyncio)
บรรทัด 12: นำเข้า type hint
บรรทัด 14: THIS_DIR โฟลเดอร์ของไฟล์นี้
บรรทัด 15: เพิ่มโฟลเดอร์ algorithm/ เข้า sys.path เพื่อให้ import utils import hybrid ทำงานได้
บรรทัด 17–21: นำเข้า FastAPI, ตัวจัดการ CORS, JSONResponse, StaticFiles (เสิร์ฟหน้าเว็บ) และ Pydantic (BaseModel, Field) สำหรับตรวจรูปแบบคำขอ
บรรทัด 23: นำเข้าจาก ➜ algorithm/utils.py ได้แก่ load_data evaluate_route set_travel_profile haversine_km MAX_ATTRS
บรรทัด 24–27: นำเข้าอัลกอริทึมทั้งหมด ➜ algorithm/greedy.py ➜ algorithm/genetic.py ➜ algorithm/hybrid.py ➜ algorithm/pareto.py
บรรทัด 29: นำเข้า json
บรรทัด 30: DATA_DIR โฟลเดอร์ data/
บรรทัด 31–32: โหลด provinces.json (ข้อมูลโปรไฟล์ของแต่ละจังหวัด เช่น ตัวคูณถนน ความเร็ว ชื่อ) เป็น PROVINCES
บรรทัด 33: DEFAULT_PROVINCE = 'phuket'
บรรทัด 34–38: โหลดสถานะจังหวัด provinces_status.json เก็บชุด SPARSE (จังหวัดข้อมูลน้อย) ใช้แสดงป้ายเตือนที่หน้าเว็บ ถ้าอ่านไม่ได้ใช้ชุดว่าง
บรรทัด 39: เพิ่ม DATA_DIR เข้า path
บรรทัด 40: นำเข้ารายชื่อ 77 จังหวัดจาก ➜ data/thai_provinces.py (ใช้แสดงจังหวัดที่ยังไม่พร้อม)
บรรทัด 41–46: โหลดนโยบาย RL ที่ฝึกแล้วจาก algorithm/rl_policy.json เป็น RL_THETA (ใช้เมื่อเลือก hybrid_rl ในโหมด Developer ดู ➜ algorithm/rl.py) ถ้าโหลดไม่ได้เป็น None
บรรทัด 47: DIVERSITY_WEIGHT = 1.5 น้ำหนักความหลากหลายของหมวดใน fitness ของ Hybrid (0 = แบบ Project 1)
บรรทัด 49–59  โหลดข้อมูลทุกจังหวัดเข้าหน่วยความจำ
49  # slug -> {'pois','hotels','poi_by_id','hotel_by_id'} (เฉพาะจังหวัดที่มีไฟล์ข้อมูลแล้ว)
50  DATA = {}
51  for _slug in list(PROVINCES):
52      _path = os.path.join(DATA_DIR, 'provinces', f'{_slug}.json')
53      if not os.path.exists(_path):
54          del PROVINCES[_slug]
55          continue
56      _pois, _hotels = load_data(_path)
57      DATA[_slug] = {'pois': _pois, 'hotels': _hotels,
58                     'poi_by_id': {p['id']: p for p in _pois},
59                     'hotel_by_id': {h['id']: h for h in _hotels}}
บรรทัด 49–50: DATA dict จาก slug เป็น {จุด โรงแรม ดัชนีตาม id}
บรรทัด 51–55: วนทุกจังหวัดใน PROVINCES ถ้าไม่มีไฟล์ data/provinces/<slug>.json ลบจังหวัดนั้นออกจากรายการ
บรรทัด 56: โหลดจุดและโรงแรมด้วย ➜ load_data() ใน algorithm/utils.py
บรรทัด 57–59: เก็บจุด โรงแรม และดัชนี poi_by_id hotel_by_id เพื่อค้นหาด้วย id ได้เร็ว
บรรทัด 62–67  เลือกจังหวัด
62  def get_province(slug):
63      if slug not in DATA:
64          raise HTTPException(status_code=404, detail=f'Province {slug} not found')
65      pv = PROVINCES[slug]   # ตั้งโปรไฟล์ระยะ/เวลาเดินทางของจังหวัดให้ request นี้
66      set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
67      return DATA[slug]
บรรทัด 62–67: get_province คืนข้อมูลของ slug ที่ขอ ไม่พบตอบ 404 และ **ตั้งโปรไฟล์เวลาเดินทางของจังหวัดนั้นให้ request ปัจจุบัน** ด้วย ➜ set_travel_profile() ใน algorithm/utils.py
บรรทัด 74–144  โมเดลข้อมูลคำขอ/คำตอบ (Pydantic)
74  class Preferences(BaseModel):
75      """ความชอบของผู้ใช้ — กรอง/ถ่วงน้ำหนัก POI ก่อนส่งให้อัลกอริทึม"""
76      liked: List[str] = []      # หมวดที่ชอบ (beach, temple, ...) ได้คะแนนถ่วงเพิ่มตอนเลือก
77      avoided: List[str] = []    # หมวดที่ไม่ต้องการ (ตัดออกจากตัวเลือก; ไม่รวม restaurant)
78      diet: str = 'none'         # 'none' | 'vegetarian' | 'halal' (กรองร้านอาหารตามแท็กใน OSM)
79
80
81  class PackageRequest(BaseModel):
82      province: str = Field(DEFAULT_PROVINCE, description="slug ของจังหวัด (ดู /api/provinces)")
83      preferences: Optional[Preferences] = None
84      budget: float = Field(..., ge=1000, le=100000)
85      days: int = Field(..., ge=1, le=7)
86      travelers: int = Field(1, ge=1, le=10)
87      seed: Optional[int] = Field(None, description="Random seed; None = random every call")
88      algorithm: Optional[str] = Field('hybrid', description="'greedy' | 'ga' | 'hybrid' | 'hybrid_rl'")
89      include_hotel: Optional[bool] = Field(True, description="รวมค่าโรงแรมในงบหรือไม่")
90
91
92  class RecomputeRequest(BaseModel):
93      province: str = DEFAULT_PROVINCE
94      hotel_id: str
95      days: int
96      budget: float
97      routes: List[List[str]]
98      travelers: int = 1
99
100
101  class ReoptimizeRequest(BaseModel):
102      province: str = DEFAULT_PROVINCE
103      tier: str = 'Custom'
104      hotel_id: str
105      days: int = Field(..., ge=1, le=7)
106      budget: float = Field(..., ge=1000, le=100000)   # งบรวมของผู้ใช้ (บาท)
107      travelers: int = Field(1, ge=1, le=10)
108      include_hotel: bool = True
109      routes: List[List[str]]
110      locked: List[str] = []      # POI ที่ผู้ใช้เลือกเอง ต้องคงไว้
111      excluded: List[str] = []    # POI ที่ผู้ใช้ลบ ห้ามกลับมา
112      preferences: Optional[Preferences] = None
113      seed: Optional[int] = None
114
115
116  class DayDetail(BaseModel):
117      day: int
118      pois: List[dict]
119      distance_km: float
120      time_min: float
121      cost: float
122      score: float
123      arrivals: List[list] = []   # [[poi_id, นาทีที่ถึง (นับจาก 00:00)], ...] ใช้สร้างตารางเวลา/ไฟล์ปฏิทิน
124
125
126  class Package(BaseModel):
127      tier: str
128      hotel: dict
129      days: List[DayDetail]
130      total_score: float
131      total_activity_cost: float
132      total_hotel_cost: float
133      total_cost: float
134      runtime_ms: float
135      valid: bool
136      violations: List[str]
137      notes: List[str] = []   # ข้อความแจ้งผู้ใช้ เช่น จุดที่เลือกแต่ใส่ในแผนไม่ได้
138      objectives: dict = {}   # Pareto: score / diversity / distance_km / cost ของแผนนี้
139
140
141  class PackageResponse(BaseModel):
142      request: dict
143      packages: List[Package]
144
บรรทัด 74–78: Preferences ความชอบ: หมวดที่ชอบ (liked) หมวดที่ไม่เอา (avoided) และอาหาร (diet: none, vegetarian, halal) ใช้ที่ apply_preferences
บรรทัด 81–89: PackageRequest คำขอสร้างแพ็กเกจ: จังหวัด ความชอบ งบ (1,000–100,000) จำนวนวัน (1–7) จำนวนคน (1–10) seed อัลกอริทึม และธงรวมโรงแรมหรือไม่
บรรทัด 92–98: RecomputeRequest คำขอคำนวณใหม่หลังผู้ใช้แก้ลำดับ: จังหวัด โรงแรม วัน งบ แผนเป็นรายการ id จำนวนคน
บรรทัด 101–113: ReoptimizeRequest คำขอปรับแผนใหม่ด้วย Hybrid: เพิ่ม locked (จุดที่ผู้ใช้เลือก ต้องคงไว้) และ excluded (จุดที่ลบ ห้ามกลับ) ใช้กับ ➜ reoptimize_solve() ใน algorithm/hybrid.py
บรรทัด 116–123: DayDetail รายละเอียดวัน (จุด ระยะ เวลา ค่าใช้จ่าย คะแนน เวลาถึงแต่ละจุดสำหรับตารางเวลา/ปฏิทิน)
บรรทัด 126–138: Package แพ็กเกจหนึ่งระดับ: โรงแรม รายวัน คะแนน ค่าใช้จ่ายกิจกรรม/โรงแรม/รวม เวลารัน ธง valid ข้อความผิดข้อจำกัด หมายเหตุถึงผู้ใช้ และวัตถุประสงค์แบบ Pareto
บรรทัด 141–143: PackageResponse ห่อคำขอกับแพ็กเกจที่ได้
บรรทัด 150–170  แปลงแผนเป็นรายละเอียดรายวัน
150  def make_day_details(routes_per_day, hotel, travelers=1):
151      """แปลง routes เป็น List[DayDetail] พร้อม metadata (ระยะทาง, เวลา, ค่าใช้จ่าย, score)"""
152      eval_result = evaluate_route(routes_per_day, hotel, budget=float('inf'))
153      days = []
154      for i, day_pois in enumerate(routes_per_day):
155          det = eval_result['days_detail'][i]
156          days.append(DayDetail(
157              day=i + 1,
158              pois=[{
159                  'id': p['id'], 'name_th': p['name_th'], 'name_en': p['name_en'],
160                  'category': p['category'], 'lat': p['lat'], 'lng': p['lng'],
161                  'score': p['score'], 'cost': p['cost'] * travelers,
162                  'duration_min': p['duration_min'],
163              } for p in day_pois],
164              distance_km=det['distance_km'],
165              time_min=det['time_min'],
166              cost=det['cost'] * travelers,
167              score=det['score'],
168              arrivals=[list(a) for a in det.get('arrivals', [])]
169          ))
170      return days, eval_result
บรรทัด 150–151: ประกาศ make_day_details แปลงแผน (รายการ POI รายวัน) เป็น DayDetail
บรรทัด 152: ประเมินด้วย ➜ evaluate_route() ใน algorithm/utils.py (งบเป็นอนันต์เพราะต้องการแค่ตัวเลข)
บรรทัด 153–169: วนทีละวัน ใส่ข้อมูลจุด (id ชื่อไทย/อังกฤษ หมวด พิกัด คะแนน ค่าใช้จ่ายคูณจำนวนคน ระยะเวลา) ระยะทาง เวลา ค่าใช้จ่ายคูณจำนวนคน คะแนน และเวลาถึง
บรรทัด 170: คืนรายละเอียดรายวันและผลประเมินดิบ
บรรทัด 173–251  `_prioritize_sights` จัดลำดับความสำคัญเมื่องบไม่พอ
173  def _prioritize_sights(routes, hotel, sight_pool, rest_pool, budget_pp):
174      """จัดลำดับความสำคัญเมื่องบไม่พอ: สถานที่ท่องเที่ยวต้องครบ (MAX_ATTRS ต่อวัน) ทุกวัน ส่วนมื้ออาหารเป็นรอง
175         1) ถ้าเกินงบ ตัดร้านอาหารของวันท้ายสุดก่อน (แล้วค่อยตัดสถานที่ที่มีค่าเข้าชม)
176         2) เติมสถานที่ท่องเที่ยวที่ยังไม่ได้ใช้ (ฟรี/ถูกก่อน) จนครบทุกวันเท่าที่เวลาและเวลาเปิด-ปิดอนุญาต
177         3) ถ้างบเหลือ เติมร้านอาหารคืนให้วันแรกก่อน (ร้านที่เพิ่มระยะทางน้อยที่สุด)"""
178      from utils import evaluate_route as _ev
179      routes = [list(d) for d in routes]
180      cost = lambda: sum(p['cost'] for d in routes for p in d)
181      ok = lambda day: _ev([day], hotel, float('inf'))['valid']
182      dist = lambda day: _ev([day], hotel, float('inf'))['days_detail'][0]['distance_km'] if day else 0.0
183
184      if cost() > budget_pp:
185          # งบตึง: ถอดร้านอาหารทั้งหมดออกก่อน (ร้านเดิมมักไกลกันและกินงบ) แล้วเติมสถานที่ท่องเที่ยวให้ครบ จากนั้นค่อยเติมร้านที่ใกล้ที่สุดเท่าที่งบเหลือ
186          routes = [[p for p in day if p['category'] != 'restaurant'] for day in routes]
187          while cost() > budget_pp:
188              paid = [(p['cost'], d, i) for d, day in enumerate(routes) for i, p in enumerate(day) if p['cost'] > 0]
189              if not paid:
190                  break
191              _, d, i = max(paid); routes[d].pop(i)
192
193      def add_best(d, pool, want_cat):
194          used = {p['id'] for day in routes for p in day}
195          left = budget_pp - cost()
196          base = dist(routes[d]); best = None
197          for c in pool:
198              if c['id'] in used or c['cost'] > left or (c['category'] == 'restaurant') != want_cat:
199                  continue
200              for pos in range(len(routes[d]) + 1):
201                  trial = routes[d][:pos] + [c] + routes[d][pos:]
202                  if not ok(trial):
203                      continue
204                  key = ((dist(trial) - base) + 0.1 * c['cost'], c['cost']) if want_cat else ((dist(trial) - base) - 0.1 * c['score'], c['cost'])
205                  if best is None or key < best[0]:
206                      best = (key, trial)
207          if best:
208              routes[d] = best[1]
209          return best is not None
210
211      def nearer_meals(d):
212          # ร้านที่ไกลจนวันเต็มเวลาแล้วใส่ที่เที่ยวไม่ได้ (เช่น สตูลวันละ 300 กม.): สลับเป็นร้านที่ทำให้ระยะขับของวันนั้นสั้นลงมากที่สุด ถ้าราคาไม่เกินงบ
213          for _ in range(4):
214              base = dist(routes[d]); best = None
215              used = {p['id'] for day in routes for p in day}
216              for i, p in enumerate(routes[d]):
217                  if p['category'] != 'restaurant':
218                      continue
219                  for c in rest_pool:
220                      if c['id'] in used or cost() - p['cost'] + c['cost'] > budget_pp:
221                          continue
222                      trial = routes[d][:i] + [c] + routes[d][i + 1:]
223                      if ok(trial) and (best is None or dist(trial) < best[0]):
224                          best = (dist(trial), trial)
225              if best and best[0] < base - 1.0:
226                  routes[d] = best[1]
227              else:
228                  break
229
230      for d in range(len(routes)):
231          if sum(1 for p in routes[d] if p['category'] != 'restaurant') < MAX_ATTRS:
232              nearer_meals(d)
233          if sum(1 for p in routes[d] if p['category'] != 'restaurant') < MAX_ATTRS and dist(routes[d]) > 120:
234              routes[d] = []   # วันที่เต็มเวลาเพราะขับไกลมาก (ร้านและที่เที่ยวอยู่ห่างโรงแรมเป็นร้อยกิโลเมตร): ล้างแล้วสร้างวันใหม่จากสถานที่ใกล้โรงแรม
235      for d in range(len(routes)):
236          while sum(1 for p in routes[d] if p['category'] != 'restaurant') < MAX_ATTRS and add_best(d, sight_pool, False):
237              pass
238      # วันที่ยังขาดสถานที่เพราะงบหมด: ถอดร้านอาหารของวันท้ายสุด (ราคาแพงสุดก่อน) เพื่อเอางบมาเติมสถานที่ท่องเที่ยว (สถานที่ครบสำคัญกว่ามื้ออาหาร)
239      for d in range(len(routes)):
240          for _ in range(8):
241              if sum(1 for p in routes[d] if p['category'] != 'restaurant') >= MAX_ATTRS or add_best(d, sight_pool, False):
242                  continue
243              cands = [(dd, i, p['cost']) for dd in range(len(routes) - 1, d - 1, -1) for i, p in enumerate(routes[dd]) if p['category'] == 'restaurant' and p['cost'] > 0]
244              if not cands:
245                  break
246              dd, i, _c = max(cands, key=lambda c: (c[0], c[2]))
247              routes[dd].pop(i)
248      for d in range(len(routes)):
249          while sum(1 for p in routes[d] if p['category'] == 'restaurant') < 2 and add_best(d, rest_pool, True):
250              pass
251      return routes
บรรทัด 173–177: ประกาศและ docstring: ที่เที่ยวต้องครบ 4 จุดต่อวันก่อน มื้ออาหารเป็นรอง: (1) ถ้าเกินงบตัดร้านอาหารก่อน (2) เติมที่เที่ยวที่ยังไม่ใช้จนครบ (3) ถ้างบเหลือเติมร้านคืนให้วันแรกก่อน ใช้กับแพ็กเกจที่สร้างผ่านหน้าเว็บเท่านั้น (ไม่ได้ใช้ในการทดลองบทที่ 4)
บรรทัด 178–182: ตั้งฟังก์ชันย่อย: cost ค่าใช้จ่ายรวม ok ตรวจวันนั้น valid ด้วย ➜ evaluate_route() ใน algorithm/utils.py และ dist ระยะของวัน
บรรทัด 184–191: ถ้าเกินงบ ถอดร้านอาหารทั้งหมด แล้วถอดจุดที่มีค่าเข้าแพงสุดจนอยู่ในงบ
บรรทัด 193–209: ฟังก์ชัน add_best เพิ่มจุดที่ดีที่สุดให้วันที่ d: ลองแทรกจุดที่ยังไม่ใช้ทุกตำแหน่ง ที่ผ่านข้อจำกัดและอยู่ในงบ เลือกตามระยะที่เพิ่มน้อยที่สุด (ที่เที่ยวมีโบนัสตามคะแนน ร้านมีโทษตามราคา)
บรรทัด 211–228: ฟังก์ชัน nearer_meals สลับร้านที่ไกลมากเป็นร้านที่ทำให้ระยะขับของวันสั้นลงมากที่สุดถ้างบพอ (เช่น สตูลวันละ 300 กม.) วนไม่เกิน 4 รอบ
บรรทัด 230–234: สำหรับแต่ละวัน ถ้าที่เที่ยวไม่ครบให้ลอง nearer_meals และถ้ายังไม่ครบและขับเกิน 120 กม. ให้ล้างวันนั้นแล้วสร้างใหม่จากสถานที่ใกล้โรงแรม
บรรทัด 235–237: เติมที่เที่ยวให้ครบทุกวัน
บรรทัด 238–247: วันที่ยังขาดเพราะงบหมด ถอดร้านอาหารของวันท้ายสุด (แพงสุดก่อน) เอางบมาเติมที่เที่ยว
บรรทัด 248–250: เติมร้านอาหารให้วันแรก ๆ ให้ครบ 2 ร้านเท่าที่งบเหลือ
บรรทัด 251: คืนแผน
บรรทัด 254–319  `_trim_to_budget` ตัดให้อยู่ในงบ (เฟส 1-3)
254  def _trim_to_budget(routes, hotel, max_activity_budget, travelers, pois):
255      """4-phase budget + time-window enforcement:
256         1) Swap expensive restaurants → cheaper unused
257         2) Remove paid attractions (highest cost first)
258         3) Remove any POI (incl. restaurants) if still over budget
259         4) Remove POIs causing time-window violations
260      """
261      import re as _re
262      from utils import evaluate_route as _eval
263
264      def _check(rts):
265          r = _eval(rts, hotel, budget=float('inf'))
266          # Budget ครอบคลุมเฉพาะ ค่าเข้า + ค่าอาหาร (per-person × travelers)
267          # ค่าเดินทาง (transportation) ถือเป็น overhead ไม่นับในงบกิจกรรม
268          poi_cost = sum(p['cost'] for day in rts for p in day) * travelers
269          return poi_cost, r
270
271      used_ids = {p['id'] for day in routes for p in day}
272      unused_rest = sorted(
273          [p for p in pois if p['category'] == 'restaurant' and p['id'] not in used_ids],
274          key=lambda x: (not x.get('_diet'), x['cost']))   # ร้านที่ตรงความต้องการด้านอาหารเป็นตัวสลับก่อน
275
276      # Phase 1: สลับร้านอาหารแพงด้วยร้านที่ถูกกว่า
277      for cheap_rest in unused_rest:
278          total_act, _ = _check(routes)
279          if total_act <= max_activity_budget:
280              break
281          worst_d, worst_i, worst_cost = None, None, cheap_rest['cost']
282          for di, day in enumerate(routes):
283              for pi, p in enumerate(day):
284                  if p['category'] == 'restaurant' and p['cost'] > worst_cost:
285                      worst_cost = p['cost']; worst_d, worst_i = di, pi
286          if worst_d is None:
287              break
288          old_id = routes[worst_d][worst_i]['id']
289          routes[worst_d][worst_i] = cheap_rest
290          used_ids.discard(old_id)
291          used_ids.add(cheap_rest['id'])
292
293      # Phase 2: ลบ attraction ที่มีค่าเข้าชม (เริ่มจากแพงสุด)
294      while True:
295          total_act, _ = _check(routes)
296          if total_act <= max_activity_budget:
297              break
298          worst_d, worst_i, worst_cost = None, None, 0
299          for di, day in enumerate(routes):
300              for pi, p in enumerate(day):
301                  if p['category'] != 'restaurant' and p['cost'] > worst_cost:
302                      worst_cost = p['cost']; worst_d, worst_i = di, pi
303          if worst_d is None:
304              break
305          routes[worst_d].pop(worst_i)
306
307      # Phase 3: ลบ POI ใดก็ได้รวมถึงร้านอาหาร ถ้ายังเกินงบ
308      while True:
309          total_act, _ = _check(routes)
310          if total_act <= max_activity_budget:
311              break
312          worst_d, worst_i, worst_cost = None, None, -1
313          for di, day in enumerate(routes):
314              for pi, p in enumerate(day):
315                  if p['cost'] > worst_cost:
316                      worst_cost = p['cost']; worst_d, worst_i = di, pi
317          if worst_d is None:
318              break
319          routes[worst_d].pop(worst_i)
บรรทัด 254–260: ประกาศและ docstring: 4 เฟส (1) สลับร้านแพงเป็นร้านถูก (2) ลบที่เที่ยวมีค่าเข้า (3) ลบจุดใดก็ได้ (4) ลบจุดที่ผิดเวลา
บรรทัด 261–262: นำเข้า re และ evaluate_route
บรรทัด 264–269: ฟังก์ชัน _check คืนค่าใช้จ่าย (ค่าเข้า+ค่าอาหาร) × จำนวนคน และผลประเมิน (ค่าเดินทางไม่นับในงบ)
บรรทัด 271–274: เตรียมร้านอาหารที่ยังไม่ใช้ เรียงให้ร้านที่ตรงความต้องการด้านอาหาร (_diet) ก่อน แล้วตามราคา
บรรทัด 276–291: เฟส 1 สลับร้านที่แพงกว่าด้วยร้านถูกที่ยังไม่ใช้ จนอยู่ในงบ
บรรทัด 293–305: เฟส 2 ลบที่เที่ยวที่มีค่าเข้าชม เริ่มจากแพงสุดจนอยู่ในงบ
บรรทัด 307–319: เฟส 3 ถ้ายังเกินงบ ลบจุดใดก็ได้ (รวมร้านอาหาร) เริ่มจากแพงสุด
บรรทัด 321–344  `_trim_to_budget` เฟส 4 และคืนผล
321      # Phase 4: ลบ POI ที่ไปถึงหลังเวลาปิด
322      for _ in range(30):
323          _, result = _check(routes)
324          tw = [v for v in result['violations'] if 'หลังเวลาปิด' in v]
325          if not tw:
326              break
327          removed = False
328          for viol in tw:
329              m = _re.search(r'ไปถึง (\S+) หลังเวลาปิด', viol)
330              if not m:
331                  continue
332              bad_id = m.group(1)
333              for di, day in enumerate(routes):
334                  for pi, p in enumerate(day):
335                      if p['id'] == bad_id:
336                          routes[di].pop(pi)
337                          removed = True
338                          break
339                  if removed:
340                      break
341          if not removed:
342              break
343
344      return routes
บรรทัด 321–342: เฟส 4 วนไม่เกิน 30 รอบ: ดึง id ของจุดที่ไปถึงหลังเวลาปิดจากข้อความผิดข้อจำกัดด้วย regex แล้วลบจุดนั้นออกจากแผน ถ้าไม่มีอะไรให้ลบหยุด
บรรทัด 344: คืนแผนที่ตัดให้อยู่ในงบและเวลาแล้ว
บรรทัด 347–380  ตัวเลือกตามความชอบ
347  LIKE_BOOST = 1.0   # คะแนนถ่วงเพิ่มให้ POI ในหมวดที่ผู้ใช้ชอบ (ใช้เลือกเท่านั้น ไม่นับในคะแนนที่รายงาน)
348  DIET_BOOST = 4.0   # ถ่วงร้านที่ตรงความต้องการด้านอาหารเมื่อร้านที่ตรงมีไม่พอทั้งทริป
349
350
351  def apply_preferences(pois, prefs, days):
352      """สร้างกลุ่ม POI สำหรับอัลกอริทึมตามความชอบ คืน (pool, notes)
353         - avoided: ตัด POI หมวดนั้นออก (ไม่แตะร้านอาหาร)
354         - diet: ใช้เฉพาะร้านที่มีแท็ก ถ้าน้อยกว่าจำนวนมื้อที่ต้องใช้ จะเสริมร้านทั่วไปและแจ้งผู้ใช้
355         - liked: คัดลอก POI พร้อมบวกคะแนน LIKE_BOOST เพื่อให้ถูกเลือกบ่อยขึ้น
356         pool คือสำเนา — ต้อง restore_scores() กลับเป็นออบเจ็กต์ต้นฉบับก่อนสร้างแพ็กเกจ"""
357      notes = []
358      if prefs is None:
359          return pois, notes
360      cats = {p['category'] for p in pois}
361      avoided = {c for c in prefs.avoided if c in cats and c != 'restaurant'}
362      liked = {c for c in prefs.liked if c in cats and c != 'restaurant'} - avoided
363      pool = [p for p in pois if p['category'] not in avoided]
364      if liked:
365          # _base = คะแนนจริง ใช้กำหนดช่วงคะแนนของแต่ละ tier ไม่ให้ที่ชอบหลุดจาก tier ประหยัด
366          pool = [dict(p, score=round(p['score'] + LIKE_BOOST, 2), _base=p['score']) if p['category'] in liked else p for p in pool]
367      if prefs.diet in ('vegetarian', 'halal'):
368          need = 2 * days + 2
369          match = [p for p in pool if p['category'] == 'restaurant' and prefs.diet in p.get('tags', [])]
370          label = 'มังสวิรัติ' if prefs.diet == 'vegetarian' else 'ฮาลาล'
371          if len(match) >= need:
372              pool = [p for p in pool if p['category'] != 'restaurant' or p in match]
373          elif match:
374              # ไม่พอทั้งทริป: ถ่วงคะแนนร้านที่ตรงให้ถูกเลือกก่อน ที่เหลือเสริมด้วยร้านทั่วไป
375              ids = {p['id'] for p in match}
376              pool = [dict(p, score=round(p['score'] + DIET_BOOST, 2), _base=p.get('_base', p['score']), _diet=True) if p['id'] in ids else p for p in pool]
377              notes.append(f'ร้านอาหาร{label}ในฐานข้อมูลมีเพียง {len(match)} ร้าน ไม่พอสำหรับทั้งทริป จึงใช้ร้านเหล่านี้ก่อนแล้วเสริมด้วยร้านทั่วไป (ไม่รับประกันว่ารองรับอาหาร{label})')
378          else:
379              notes.append(f'ไม่พบข้อมูลร้านอาหาร{label}ของจังหวัดนี้ในฐานข้อมูล จึงใช้ร้านทั่วไป (ไม่รับประกันว่ารองรับอาหาร{label})')
380      return pool, notes
บรรทัด 347: LIKE_BOOST = 1.0 คะแนนที่บวกให้หมวดที่ผู้ใช้ชอบ (ใช้เลือกเท่านั้น ไม่นับในคะแนนที่รายงาน)
บรรทัด 348: DIET_BOOST = 4.0 คะแนนถ่วงร้านที่ตรงความต้องการด้านอาหารเมื่อร้านที่ตรงมีไม่พอ
บรรทัด 351–356: ประกาศ apply_preferences และ docstring: คืน (กลุ่มจุด ข้อความแจ้งผู้ใช้) ตัดหมวดที่ไม่เอา เสริมร้านตามอาหารที่เลือก และบวกคะแนนหมวดที่ชอบ ผลเป็นสำเนา ต้องคืนวัตถุต้นฉบับก่อนสร้างแพ็กเกจ
บรรทัด 357–359: ถ้าไม่มีความชอบ คืนจุดเดิมทั้งหมด
บรรทัด 360–363: คำนวณชุดหมวดที่มีอยู่ หมวดที่ไม่เอา (ไม่รวมร้านอาหาร) หมวดที่ชอบ (ตัดหมวดที่ขัดกัน) และตัดจุดหมวดที่ไม่เอาออก
บรรทัด 364–366: ถ้ามีหมวดที่ชอบ ทำสำเนาจุดในหมวดนั้นพร้อมบวกคะแนน LIKE_BOOST และเก็บคะแนนจริงใน _base (ใช้กำหนดช่วงคะแนนของแต่ละ tier)
บรรทัด 367–370: ถ้าเลือกมังสวิรัติหรือฮาลาล คำนวณจำนวนมื้อที่ต้องใช้ (2 มื้อ/วัน + 2) และหาร้านที่มีแท็กตรง
บรรทัด 371–372: ถ้าร้านที่ตรงมีพอ ใช้เฉพาะร้านที่ตรง
บรรทัด 373–377: ถ้ามีไม่พอ บวกคะแนนร้านที่ตรง (_diet) ให้ถูกเลือกก่อน เสริมร้านทั่วไป และเพิ่มข้อความแจ้งผู้ใช้
บรรทัด 378–379: ถ้าไม่มีร้านที่ตรงเลย ใช้ร้านทั่วไปและแจ้งผู้ใช้
บรรทัด 380: คืนกลุ่มจุดและข้อความ
บรรทัด 383–411  คืนวัตถุต้นฉบับและสร้างแพ็กเกจ
383  def restore_originals(routes, originals):
384      """แทนที่ POI ที่ถูกถ่วงคะแนนด้วยออบเจ็กต์ต้นฉบับ (คะแนนที่รายงานต้องเป็นคะแนนจริง)"""
385      return [[originals.get(p['id'], p) for p in day] for day in routes]
386
387
388  def build_package(tier, hotel, routes, days, budget, runtime_ms, travelers, pois,
389                    max_total_budget=None, hotel_cost_override=None):
390      """สร้าง Package object จาก routes และตัดงบประมาณให้อยู่ใน max_total_budget ที่กำหนด"""
391      nights = max(0, days - 1)
392      hotel_cost = hotel_cost_override if hotel_cost_override is not None else hotel['cost'] * nights
393      # ถ้ากำหนด max_total_budget ให้ตัดงบตาม
394      if max_total_budget is not None:
395          max_activity = max(0, max_total_budget - hotel_cost)
396          routes = _trim_to_budget(routes, hotel, max_activity, travelers, pois)
397      day_details, eval_result = make_day_details(routes, hotel, travelers)
398      activity_cost = sum(d.cost for d in day_details)
399      total = activity_cost + hotel_cost
400      violations = list(eval_result['violations'])
401      valid = eval_result['valid']
402      return Package(
403          tier=tier, hotel=hotel, days=day_details,
404          total_score=eval_result['total_score'] if valid else 0,
405          total_activity_cost=activity_cost,
406          total_hotel_cost=hotel_cost,
407          total_cost=total,
408          runtime_ms=runtime_ms,
409          valid=valid,
410          violations=violations
411      )
บรรทัด 383–385: restore_originals แทนจุดที่ถูกบวกคะแนนด้วยออบเจ็กต์ต้นฉบับ เพื่อให้คะแนนที่รายงานเป็นคะแนนจริง
บรรทัด 388–390: ประกาศ build_package และ docstring
บรรทัด 391–392: จำนวนคืน = วัน − 1 และค่าโรงแรม (คูณจำนวนคืน หรือใช้ค่าที่กำหนดทับ)
บรรทัด 394–396: ถ้ามีงบรวมสูงสุด คำนวณงบกิจกรรมที่เหลือจากค่าโรงแรม และตัดแผนด้วย _trim_to_budget
บรรทัด 397–399: แปลงแผนเป็นรายละเอียดรายวันด้วย make_day_details และรวมค่ากิจกรรมกับค่าโรงแรม
บรรทัด 400–401: ดึงข้อความผิดข้อจำกัดและธง valid
บรรทัด 402–411: คืนวัตถุ Package (คะแนนเป็น 0 ถ้าแผนไม่ valid)
บรรทัด 418–457  สร้างแอปและ middleware
418  app = FastAPI(title='WeEasyTrip API', version='1.0.0')
419  # ---------- จำกัดคำขอหนัก (Hybrid/GA ใช้ CPU 2–4 วินาที): 20 ครั้ง/นาที/IP และรันพร้อมกันได้ 2 งาน ----------
420  _HEAVY = ('/api/packages', '/api/pareto', '/api/reoptimize')   # /api/recompute คำนวณเบา ใช้ตอนลากวางบ่อย จึงไม่จำกัด
421  _HITS = {}                                  # ip -> [เวลาของคำขอล่าสุด]
422  _SLOTS = asyncio.Semaphore(2)
423  RATE_PER_MIN = int(os.environ.get('WET_RATE_PER_MIN', '20'))
424
425
426  @app.middleware('http')
427  async def revalidate_static(request: Request, call_next):
428      """ไฟล์หน้าเว็บ (html/css/js) ให้เบราว์เซอร์ตรวจเวอร์ชันใหม่ทุกครั้ง (ใช้ ETag/Last-Modified ไม่โหลดซ้ำถ้าไม่เปลี่ยน)
429      ไม่งั้นแก้ CSS/JS แล้วผู้ใช้ยังเห็นของเก่าจากแคช"""
430      resp = await call_next(request)
431      if not request.url.path.startswith('/api'):
432          resp.headers['Cache-Control'] = 'no-cache'
433      return resp
434
435
436  @app.middleware('http')
437  async def limit_heavy(request: Request, call_next):
438      if request.method == 'POST' and request.url.path in _HEAVY:
439          ip = request.client.host if request.client else '?'
440          now = time.time()
441          hits = [t for t in _HITS.get(ip, []) if now - t < 60]
442          if len(hits) >= RATE_PER_MIN:
443              return JSONResponse({'detail': 'ส่งคำขอถี่เกินไป รอสักครู่แล้วลองใหม่'}, status_code=429)
444          _HITS[ip] = hits + [now]
445          try:
446              await asyncio.wait_for(_SLOTS.acquire(), timeout=20)
447          except asyncio.TimeoutError:
448              return JSONResponse({'detail': 'เซิร์ฟเวอร์กำลังประมวลผลหลายงาน ลองใหม่อีกครั้ง'}, status_code=503)
449          try:
450              return await call_next(request)
451          finally:
452              _SLOTS.release()
453      return await call_next(request)
454
455
456  app.add_middleware(CORSMiddleware, allow_origins=['*'],
457                     allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
บรรทัด 418: สร้างแอป FastAPI ชื่อ WeEasyTrip API
บรรทัด 419–423: ตั้งตัวจำกัดคำขอหนัก: _HEAVY รายการ endpoint ที่ใช้ CPU มาก _HITS ประวัติคำขอต่อ IP _SLOTS สัญญาณจำกัดการรันพร้อมกัน 2 งาน และ RATE_PER_MIN 20 ครั้ง/นาที (ปรับได้ด้วยตัวแปรแวดล้อม)
บรรทัด 426–433: middleware revalidate_static ตั้ง Cache-Control: no-cache ให้ไฟล์หน้าเว็บ (ไม่ใช่ /api) เพื่อให้เบราว์เซอร์ตรวจเวอร์ชันใหม่ทุกครั้ง แก้ CSS/JS แล้วไม่ติดแคชเก่า
บรรทัด 436–453: middleware limit_heavy สำหรับ POST ที่หนัก: นับคำขอต่อ IP ใน 60 วินาที ถ้าเกินตอบ 429 รอสัญญาณคิวได้ไม่เกิน 20 วินาที ไม่ทันตอบ 503 และคืนสัญญาณหลังเสร็จ
บรรทัด 456–457: เปิด CORS ให้ทุกที่มา (ใช้ตอนเปิดหน้าเว็บจากพอร์ตอื่น)
บรรทัด 464–502  endpoint พื้นฐาน
464  BUILD = '2026-11-09-travelcost0-distw0.3-retry-mealfloor-autonohotel-sightsfirst-nocache-nearmeals-rebuilddays-dropmeals-hotelreuse'
465
466
467  @app.get('/api/health')
468  def health():
469      """ตรวจสอบสถานะ API — คืนจำนวน POI และโรงแรมที่โหลดไว้ (ทุกจังหวัดรวมกัน)"""
470      return {'status': 'ok', 'build': BUILD,   # เปลี่ยน BUILD ทุกครั้งที่แก้อัลกอริทึม เพื่อเช็กว่าเซิร์ฟเวอร์รันโค้ดล่าสุด
471              'pois': sum(len(d['pois']) for d in DATA.values()),
472              'hotels': sum(len(d['hotels']) for d in DATA.values()),
473              'provinces': len(DATA)}
474
475
476  def _max_days(slug):
477      """จำนวนวันสูงสุดที่ข้อมูลรองรับ: สถานที่ ≥ 3 จุด/วัน และร้านอาหาร ≥ 2 ร้าน/วัน (มื้อกลางวัน+เย็น ไม่ซ้ำร้าน) (ไม่งั้นมีวันว่าง)"""
478      pois = DATA[slug]['pois']
479      rest = sum(1 for p in pois if p['category'] == 'restaurant')
480      return max(1, min(7, (len(pois) - rest) // 3, rest // 2))
481
482
483  @app.get('/api/provinces')
484  def get_provinces():
485      """รายการจังหวัดที่มีข้อมูล พร้อมศูนย์กลางแผนที่และจำนวน POI/โรงแรม"""
486      region = {p[0]: p[3] for p in PROVINCES_77}
487      region.update({k: v[2] for k, v in EXTRA_AREAS.items()})
488      return {'default': DEFAULT_PROVINCE,
489              'provinces': [{'slug': s, **PROVINCES[s], 'region': region.get(s, PROVINCES[s].get('region', '')),
490                             'pois': len(DATA[s]['pois']), 'hotels': len(DATA[s]['hotels']), 'sparse': s in SPARSE,
491                             'max_days': _max_days(s)}
492                            for s in DATA],
493              'planned': [{'slug': p[0], 'name_th': p[1], 'name_en': p[2], 'region': p[3]}
494                          for p in PROVINCES_77 if p[0] not in DATA]}
495
496
497
498  @app.get('/api/pois')
499  def get_pois(province: str = DEFAULT_PROVINCE):
500      """ดึงรายการ POI และโรงแรมทั้งหมดของจังหวัด"""
501      d = get_province(province)
502      return {'pois': d['pois'], 'hotels': d['hotels']}
บรรทัด 464: BUILD สตริงรุ่นของโค้ด เปลี่ยนทุกครั้งที่แก้อัลกอริทึม เพื่อเช็กว่าเซิร์ฟเวอร์รันโค้ดล่าสุด
บรรทัด 467–473: GET /api/health คืนสถานะ รุ่น จำนวน POI โรงแรม และจังหวัด
บรรทัด 476–480: _max_days จำนวนวันสูงสุดที่ข้อมูลรองรับ: ที่เที่ยวไม่น้อยกว่า 3 จุดต่อวัน และร้านอาหารไม่น้อยกว่า 2 ร้านต่อวัน
บรรทัด 483–494: GET /api/provinces รายการจังหวัดที่มีข้อมูล พร้อมศูนย์กลางแผนที่ จำนวนจุด/โรงแรม ธง sparse จำนวนวันสูงสุด และรายชื่อจังหวัดที่ยังไม่พร้อม
บรรทัด 498–502: GET /api/pois คืนจุดและโรงแรมของจังหวัด ผ่าน get_province
บรรทัด 505–536  โหมด Developer
505  # ---------- โหมด Developer: รหัสผ่านตรวจที่ backend (ตั้งค่าได้ด้วยตัวแปรแวดล้อม WET_DEV_PASSWORD) ----------
506  DEV_PASSWORD = os.environ.get('WET_DEV_PASSWORD', '007')
507  DEV_TOKENS = set()          # shortcut: เก็บในหน่วยความจำ — รีสตาร์ทเซิร์ฟเวอร์แล้วต้องใส่รหัสใหม่
508  _UNLOCK_FAILS = {}          # ip -> [เวลาที่ใส่ผิด] จำกัด 5 ครั้ง/นาที กันเดารหัส
509
510
511  class UnlockRequest(BaseModel):
512      password: str
513
514
515  @app.post('/api/dev/unlock')
516  def dev_unlock(body: UnlockRequest, request: Request):
517      ip = request.client.host if request.client else '?'
518      now = time.time()
519      fails = [t for t in _UNLOCK_FAILS.get(ip, []) if now - t < 60]
520      if len(fails) >= 5:
521          raise HTTPException(status_code=429, detail='ลองรหัสผิดหลายครั้ง รอ 1 นาทีแล้วลองใหม่')
522      if not secrets.compare_digest(body.password, DEV_PASSWORD):
523          _UNLOCK_FAILS[ip] = fails + [now]
524          raise HTTPException(status_code=403, detail='รหัสผ่านไม่ถูกต้อง')
525      token = secrets.token_hex(16)
526      DEV_TOKENS.add(token)
527      return {'token': token}
528
529
530  def is_dev(token: Optional[str]) -> bool:
531      return bool(token) and token in DEV_TOKENS
532
533
534  @app.get('/api/dev/check')
535  def dev_check(x_dev_token: Optional[str] = Header(None)):
536      return {'ok': is_dev(x_dev_token)}
บรรทัด 505–508: รหัสผ่านโหมด Developer จากตัวแปรแวดล้อม WET_DEV_PASSWORD เก็บโทเค็นในหน่วยความจำ และบันทึกการใส่รหัสผิดต่อ IP
บรรทัด 511–512: UnlockRequest รับรหัสผ่าน
บรรทัด 515–527: POST /api/dev/unlock จำกัดใส่ผิด 5 ครั้ง/นาที เทียบรหัสด้วย secrets.compare_digest (กัน timing attack) ถ้าถูกสร้างโทเค็นสุ่มเก็บไว้
บรรทัด 530–531: is_dev ตรวจโทเค็น
บรรทัด 534–536: GET /api/dev/check ตรวจว่าโทเค็นยังใช้ได้
บรรทัด 539–616  `POST /api/packages`: เตรียมและตัวช่วยของ tier
539  @app.post('/api/packages', response_model=PackageResponse)
540  def create_packages(req: PackageRequest, x_dev_token: Optional[str] = Header(None)):
541      """สร้าง 3 แพ็กเกจ (Budget / Standard / Premium) ด้วย algorithm ที่เลือก"""
542      # ใช้ seed ที่กำหนดเพื่อ reproduce ผล; None → สุ่มใหม่ทุกครั้ง
543      if (req.algorithm or 'hybrid').lower() != 'hybrid' and not is_dev(x_dev_token):   # เลือกอัลกอริทึมอื่นได้เฉพาะโหมด Developer
544          raise HTTPException(status_code=403, detail='ต้องเข้าโหมด Developer เพื่อเลือกอัลกอริทึมอื่นนอกจาก Hybrid')
545      random.seed(req.seed)
546      data = get_province(req.province)
547      HOTELS = data['hotels']
548      originals = data['poi_by_id']
549      POIS, pref_notes = apply_preferences(data['pois'], req.preferences, req.days)
550
551      # tier: (ชื่อ, สัดส่วนงบโรงแรม, สัดส่วนงบรวม, scoring_mode, score_pct, max_rest_cost)
552      # score_pct: percentile สูงสุดของ score ที่อนุญาตสำหรับ tier นั้น
553      # max_rest_cost: ราคาร้านอาหารสูงสุด (None = ไม่จำกัด)
554      tier_specs = [
555          ('Budget',   0.20, 0.40, 'ratio',   0.50,  150),  # ร้านถูก + attr ระดับกลาง
556          ('Standard', 0.45, 0.75, 'quality', 0.80,  400),  # ร้านกลาง + attr ระดับดี
557          ('Premium',  0.55, 1.00, 'quality', None,  None), # ทุกอย่าง เน้น score สูงสุด
558      ]
559      all_pois = POIS
560      sorted_hotels = sorted(HOTELS, key=lambda h: h['cost'])
561
562      # คำนวณ score threshold จาก non-restaurant POIs
563      _attr_scores = sorted(p.get('_base', p['score']) for p in all_pois if p['category'] != 'restaurant')
564      def _percentile(lst, pct):
565          idx = max(0, int(len(lst) * pct) - 1)
566          return lst[idx]
567
568      def make_tier_pois(score_pct, max_rest_cost=None, hotel=None):
569          """กรอง POI ตาม tier:
570             - attr: กรองตาม score percentile
571             - restaurant: กรองตาม max_rest_cost เพื่อให้ tier ต่างกันชัดเจน
572          """
573          result = []
574          attr_max = _percentile(_attr_scores, score_pct) if score_pct is not None else float('inf')
575          for p in all_pois:
576              if p['category'] == 'restaurant':
577                  if max_rest_cost is None or p['cost'] <= max_rest_cost:
578                      result.append(p)
579              else:
580                  if p.get('_base', p['score']) <= attr_max:
581                      result.append(p)
582          # ร้านที่ผ่านเพดานราคาของ tier น้อยเกินไป (เช่น กรองตามอาหารมังสวิรัติแล้วเหลือแต่ร้านแพง): เติมร้านที่ถูกที่สุดจนครบมื้อ
583          need = 2 * req.days + 2
584          chosen = [p for p in result if p['category'] == 'restaurant']
585          if len(chosen) < need:
586              rest_ids = {p['id'] for p in chosen}
587              extra = sorted((p for p in all_pois if p['category'] == 'restaurant' and p['id'] not in rest_ids),
588                             key=lambda p: (not p.get('_diet'), p['cost']))[:need - len(chosen)]
589              result += extra
590          # เพดานราคาตัดร้านใกล้โรงแรมทิ้งได้ จนต้องวิ่งไปร้านไกลซึ่งค่าเดินทางแพงกว่าส่วนต่างราคาอาหาร: คงร้านที่ใกล้โรงแรมที่สุดไว้เสมอ
591          if hotel is not None:
592              have = {p['id'] for p in result}
593              near = sorted((p for p in all_pois if p['category'] == 'restaurant' and p['id'] not in have),
594                            key=lambda p: haversine_km(hotel['lat'], hotel['lng'], p['lat'], p['lng']))[:need]
595              result += near
596          return result
597
598      _dist_cache = {}
599
600      def _median_dist(h):
601          if h['id'] not in _dist_cache:
602              ds = sorted(haversine_km(h['lat'], h['lng'], p['lat'], p['lng']) for p in all_pois if p['category'] != 'restaurant')
603              rs = sorted(haversine_km(h['lat'], h['lng'], p['lat'], p['lng']) for p in all_pois if p['category'] == 'restaurant')[:8]
604              # ระยะกลางถึงแหล่งเที่ยว + ระยะเฉลี่ยถึงร้านอาหาร 8 ร้านที่ใกล้สุด (ทุกวันต้องกิน 2 มื้อ ร้านอยู่ไกลโรงแรมทำให้ค่าเดินทางกินงบ)
605              _dist_cache[h['id']] = (ds[len(ds) // 2] if ds else 0.0) + (sum(rs) / len(rs) if rs else 0.0)
606          return _dist_cache[h['id']]
607
608      def find_best_hotel(max_per_night, exclude):
609          cands = [h for h in sorted_hotels
610                   if h['cost'] <= max_per_night and h['id'] not in exclude]
611          if not cands:
612              free = [h for h in sorted_hotels if h['id'] not in exclude]
613              return free[0] if free else sorted_hotels[0]   # โรงแรมไม่พอสำหรับ 3 ระดับ (จังหวัดข้อมูลน้อย) → ใช้ซ้ำได้
614          # คะแนนโรงแรมหักตามระยะเฉลี่ยถึงสถานที่ท่องเที่ยว: โรงแรมที่ไกลแหล่งเที่ยวทำให้ค่าเดินทางและเวลาเสียทุกวัน
615          return max(cands, key=lambda h: h['score'] - 0.08 * _median_dist(h))
616
บรรทัด 539–544: ประกาศ endpoint สร้างแพ็กเกจ 3 ระดับ ถ้าเลือกอัลกอริทึมอื่นนอกจาก hybrid ต้องเป็นโหมด Developer
บรรทัด 545–549: ตั้ง seed ดึงข้อมูลจังหวัด (ตั้งโปรไฟล์เวลาเดินทางด้วย get_province) และปรับจุดตามความชอบ
บรรทัด 551–558: tier_specs กำหนดแต่ละระดับ: สัดส่วนงบโรงแรม สัดส่วนงบรวม โหมดคะแนน เพดาน percentile คะแนนที่เที่ยว และเพดานราคาร้านอาหาร (Budget, Standard, Premium)
บรรทัด 559–566: เรียงโรงแรมตามราคา และคำนวณคะแนนที่เที่ยวไว้หา percentile
บรรทัด 568–596: make_tier_pois กรองจุดตามระดับ: ที่เที่ยวตาม percentile ร้านอาหารตามเพดานราคา ถ้าร้านน้อยกว่าจำนวนมื้อที่ต้องใช้ เติมร้านที่ถูกสุด และคงร้านที่ใกล้โรงแรมที่สุดไว้เสมอ
บรรทัด 598–606: _median_dist ระยะกลางจากโรงแรมถึงที่เที่ยว + ระยะเฉลี่ยถึงร้านอาหาร 8 ร้านที่ใกล้สุด (แคชไว้)
บรรทัด 608–615: find_best_hotel เลือกโรงแรมที่ราคาไม่เกินงบต่อคืนและยังไม่ถูกเลือก คะแนนโรงแรมหักตามระยะ (0.08 × ระยะ) ถ้าไม่มีที่เหมาะใช้ซ้ำได้
บรรทัด 617–638  โรงแรมอัตโนมัติ (ไม่รวมโรงแรม)
617      packages = []
618      picked = set()
619      algo = (req.algorithm or 'hybrid').lower()
620
621      nights = max(0, req.days - 1)
622      include_hotel = req.include_hotel if req.include_hotel is not None else True
623      auto_no_hotel = False
624      _min_meals = sum(sorted(p['cost'] for p in all_pois if p['category'] == 'restaurant')[:2 * req.days]) * req.travelers
625      if include_hotel and nights > 0:
626          # ที่พักถูกสุด + ค่าอาหารขั้นต่ำเกินงบ: สร้างแผนแบบไม่รวมโรงแรมให้แทน (ไม่งั้นแผนไม่มีร้านอาหารและเกินงบ)
627          if sorted_hotels[0]['cost'] * nights + _min_meals > req.budget:
628              include_hotel = False
629              auto_no_hotel = True
630
631      for tier, hotel_r, total_r, mode, score_pct, max_rest_cost in tier_specs:
632          if include_hotel:
633              max_per_night = req.budget * hotel_r / max(nights, 1) if nights > 0 else 0
634              hotel = find_best_hotel(max_per_night, picked) if nights > 0 else sorted_hotels[0]
635              if nights > 0 and hotel['cost'] * nights + _min_meals > req.budget >= sorted_hotels[0]['cost'] * nights + _min_meals:
636                  hotel = sorted_hotels[0]   # โรงแรมที่ไม่ซ้ำกันแพงเกินงบ แต่โรงแรมถูกสุดยังพอ: ใช้ซ้ำได้ (ไม่งั้นระดับสูงเกินงบ)
637          else:
638              # ไม่รวมโรงแรม: ใช้โรงแรมที่อยู่ใกล้แหล่งเที่ยวที่สุดเป็นจุดเริ่ม/จบของ routing เท่านั้น (ไม่คิดค่าห้อง)
บรรทัด 617–620: ตัวแปรเริ่มต้น: รายการแพ็กเกจ โรงแรมที่เลือกแล้ว และอัลกอริทึม
บรรทัด 621–624: จำนวนคืน ธงรวมโรงแรม ธงสลับเป็นไม่รวมโรงแรมอัตโนมัติ และค่าอาหารขั้นต่ำของทริป
บรรทัด 625–629: ถ้าที่พักถูกสุดรวมค่าอาหารขั้นต่ำเกินงบ สร้างแผนแบบไม่รวมโรงแรมให้แทน (ไม่งั้นแผนไม่มีร้านอาหารและเกินงบ)
บรรทัด 631–636: วนทีละระดับ ถ้ารวมโรงแรม เลือกโรงแรมตามงบต่อคืน และใช้โรงแรมถูกสุดซ้ำได้ถ้าโรงแรมที่ไม่ซ้ำแพงเกินแต่ถูกสุดยังพอ
บรรทัด 637–638: ถ้าไม่รวมโรงแรม ใช้โรงแรมที่ใกล้แหล่งเที่ยวที่สุดเป็นจุดเริ่ม/จบการจัดเส้นทางเท่านั้น (ไม่คิดค่าห้อง)
บรรทัด 639–693  เลือกโรงแรมและคำนวณงบกิจกรรมของแต่ละระดับ
639              # เดิมเลือกโรงแรมถูกสุด ซึ่งอาจอยู่ไกลจนค่าเดินทางกินงบ แผนเหลือแต่ร้านอาหาร
640              avail = [h for h in sorted_hotels if h['id'] not in picked]
641              hotel = min(avail or sorted_hotels, key=_median_dist)
642
643          if hotel is None:
644              packages.append(Package(
645                  tier=tier, hotel=sorted_hotels[0],
646                  days=[DayDetail(day=i+1, pois=[], distance_km=0, time_min=0,
647                                  cost=0, score=0) for i in range(req.days)],
648                  total_score=0, total_activity_cost=0, total_hotel_cost=0,
649                  total_cost=0, runtime_ms=0, valid=False,
650                  violations=[f'No hotel for {tier}']
651              ))
652              continue
653          picked.add(hotel['id'])
654
655          # คำนวณค่าโรงแรม (0 ถ้าไม่รวมโรงแรม หรือทริปวันเดียว)
656          hotel_total = hotel['cost'] * nights if include_hotel else 0
657
658          # งบสำหรับกิจกรรม
659          # ไม่รวมโรงแรม: งบทั้งหมดเป็นของกิจกรรม จึงไม่ลดงบ Budget เหลือ 40% (เดิมงบน้อยจนเหลือแต่ร้านอาหาร)
660          if not include_hotel:
661              total_r = {'Budget': 0.60, 'Standard': 0.85}.get(tier, 1.0)
662          target_total = req.budget * total_r
663          if include_hotel and nights > 0 and hotel_total > req.budget * hotel_r:
664              # โรงแรมถูกสุดของจังหวัดแพงกว่าสัดส่วนที่ระดับนี้จัดไว้ งบกิจกรรมจึงเหลือน้อยจนแผนมีแต่ร้านอาหาร:
665              # รับประกันงบกิจกรรมอย่างน้อย 40% ของเงินที่เหลือหลังหักค่าโรงแรม
666              target_total = hotel_total + max(target_total - hotel_total, 0.4 * max(0.0, req.budget - hotel_total))
667          budget_for_act = max(0, target_total - hotel_total) / req.travelers
668          # งบต่อคนต้องพอค่าอาหารขั้นต่ำของทริป (ร้านถูกที่สุด 2 มื้อ/วัน x 1.25) ไม่งั้นระดับ Budget ของทริปหลายคนงบไม่พอแม้แต่มื้ออาหาร
669          # อัลกอริทึมจึงทิ้งสถานที่ฟรีเกือบทั้งหมด (ผู้ใช้เห็นแผนมีแต่ร้านอาหาร) — จำกัดไม่เกินเงินที่ผู้ใช้มีจริง
670          _meal_min = sum(sorted(p['cost'] for p in all_pois if p['category'] == 'restaurant')[:2 * req.days])
671          _avail = max(0.0, req.budget - hotel_total) / req.travelers
672          budget_for_act = min(max(budget_for_act, 1.25 * _meal_min), _avail)
673          target_total = max(target_total, hotel_total + budget_for_act * req.travelers)
674
675          # Dynamic restaurant cap สำหรับ quality mode:
676          # ป้องกันร้านอาหารแพงกินงบหมดในทริปงบต่ำ
677          # Budget tier ใช้ ratio scoring ซึ่ง penalize ร้านแพงอยู่แล้ว → ไม่ต้องแตะ
678          if mode == 'quality':
679              # จัดสรรสูงสุด 1/5 ของงบต่อวันต่อมื้อ
680              # floor=150 ensures >= 21 restaurants in pool (7 days x 2 meals = 14 slots needed)
681              dyn_rest_cap = max(150.0, budget_for_act / (max(req.days, 1) * 5.0))
682              if max_rest_cost is not None:
683                  effective_rest_cap = min(max_rest_cost, dyn_rest_cap)
684              else:
685                  # Premium: ใช้ dynamic cap เฉพาะเมื่องบต่ำ; งบสูง (dyn≥500) ไม่จำกัด
686                  effective_rest_cap = dyn_rest_cap if dyn_rest_cap < 500 else None
687          else:
688              # Budget (ratio mode): ใช้ tier cap เดิม
689              effective_rest_cap = max_rest_cost
690
691          # กรอง POI pool ตาม tier (ทำให้แต่ละ tier ต่างกัน)
692          tier_pois = make_tier_pois(score_pct, effective_rest_cap, hotel)
693
บรรทัด 639–641: กรณีไม่รวมโรงแรม เลือกโรงแรมที่ใกล้แหล่งเที่ยวที่สุดจากที่ยังไม่ถูกเลือก (เดิมเลือกโรงแรมถูกสุด ซึ่งอาจไกลจนค่าเดินทางกินงบ แผนเหลือแต่ร้านอาหาร)
บรรทัด 643–652: ถ้าไม่มีโรงแรมเลย สร้างแพ็กเกจว่างที่ไม่ valid แล้วข้ามระดับนี้
บรรทัด 653: จดว่าโรงแรมนี้ถูกเลือกแล้ว
บรรทัด 656: ค่าโรงแรมรวม (0 ถ้าไม่รวมโรงแรม)
บรรทัด 660–662: ถ้าไม่รวมโรงแรม ใช้สัดส่วนงบกิจกรรม 60% (Budget) 85% (Standard) แล้วคำนวณงบเป้าหมาย target_total
บรรทัด 663–666: ถ้าโรงแรมแพงเกินสัดส่วนที่ระดับนั้นจัดไว้ รับประกันงบกิจกรรมอย่างน้อย 40% ของเงินที่เหลือ
บรรทัด 667: งบกิจกรรมต่อคน
บรรทัด 668–673: ปรับงบต่อคนให้พอค่าอาหารขั้นต่ำ (ร้านถูกสุด 2 มื้อต่อวัน × 1.25) แต่ไม่เกินเงินที่ผู้ใช้มีจริง กันแผนที่เหลือแต่ร้านอาหารเมื่อทริปหลายคนงบน้อย
บรรทัด 675–689: เพดานราคาร้านอาหารแบบพลวัตสำหรับโหมด quality (ไม่เกิน 1/5 ของงบต่อวัน ขั้นต่ำ 150) ระดับ Budget ใช้เพดานเดิมเพราะโหมด ratio หักราคาแพงอยู่แล้ว
บรรทัด 692: กรองจุดตามระดับด้วย make_tier_pois
บรรทัด 694–714  เรียกอัลกอริทึมและจัดลำดับความสำคัญ
694          t0 = time.time()
695          if algo == 'greedy':
696              routes = greedy_solve(tier_pois, hotel, req.days, budget_for_act,
697                                    scoring_mode=mode, random_factor=0.15)
698          elif algo == 'ga':
699              routes, _hist = genetic_solve(tier_pois, hotel, req.days, budget_for_act,
700                                            pop_size=30, generations=40,
701                                            mutation_rate=0.3, verbose=False)
702          else:  # hybrid
703              routes, _hist = hybrid_solve(tier_pois, hotel, req.days, budget_for_act,
704                                           scoring_mode=mode, pop_size=20,
705                                           generations=40, mutation_rate=0.3,
706                                           verbose=False, diversity_weight=DIVERSITY_WEIGHT,
707                                           rl_theta=RL_THETA if algo == 'hybrid_rl' else None,
708                                           ils=True)  # ILS: ดีขึ้นอย่างมีนัยสำคัญ 24/24 (experiments/results/ils_stats.txt)
709          runtime_ms = (time.time() - t0) * 1000.0
710          if algo != 'hybrid_rl':
711              routes = _prioritize_sights(routes, hotel, sorted((p for p in tier_pois if p['category'] != 'restaurant'), key=lambda p: -p['score'])
712                                          + sorted((p for p in all_pois if p['category'] != 'restaurant' and p not in tier_pois), key=lambda p: -p['score']),
713                                          sorted((p for p in all_pois if p['category'] == 'restaurant'), key=lambda p: p['cost']), budget_for_act)
714          routes = restore_originals(routes, originals)   # คะแนนที่รายงานต้องเป็นคะแนนจริง ไม่รวมตัวถ่วงความชอบ
บรรทัด 694–709: จับเวลาแล้วเรียกอัลกอริทึมตามที่เลือก: greedy เรียก ➜ greedy_solve() ใน algorithm/greedy.py; ga เรียก ➜ genetic_solve() ใน algorithm/genetic.py; ที่เหลือ (hybrid) เรียก ➜ hybrid_solve() ใน algorithm/hybrid.py ด้วยประชากร 20 รุ่น 40 น้ำหนักความหลากหลาย ILS เปิด และ RL seed เมื่อเลือก hybrid_rl
บรรทัด 710–713: ถ้าไม่ใช่ hybrid_rl ใช้ _prioritize_sights จัดลำดับความสำคัญเมื่องบไม่พอ (ที่เที่ยวครบก่อนมื้อ)
บรรทัด 714: คืนวัตถุต้นฉบับเพื่อให้คะแนนที่รายงานเป็นคะแนนจริง
บรรทัด 715–754  สร้างแพ็กเกจและลองใหม่เมื่อผิดข้อจำกัด
715          # ใช้ target_total เป็น cap แต่ละ tier เพื่อให้งบแตกต่างกันชัดเจน
716          pkg = build_package(tier, hotel, routes, req.days,
717                              req.budget, runtime_ms, req.travelers, POIS,
718                              max_total_budget=target_total,
719                              hotel_cost_override=hotel_total)
720          cap_total = max(0.0, req.budget - hotel_total)
721          if algo == 'hybrid':
722              # ไม่ยอมแสดงแผนที่ผิดข้อจำกัด (เช่น ถึงร้านสายเกินช่วงมื้อ) หรือเกินงบ: ลองสร้างใหม่ด้วยตัวเลือกทั้งหมด (ร้านทุกราคา) และสุ่มใหม่ สูงสุด 3 ครั้ง
723              # เลือกแผนที่ผ่านข้อจำกัดและคะแนนสูงสุด ถ้ายังไม่ผ่านใช้แผนที่ผิดน้อยที่สุด
724              def _bad(pk):
725                  return (0 if pk.valid else 1, 1 if pk.total_activity_cost > cap_total * 1.05 + 1 else 0)
726              for attempt in range(3):
727                  if _bad(pkg) == (0, 0):
728                      break
729                  t0 = time.time()
730                  random.seed(None if req.seed is None else req.seed + attempt + 1)
731                  r2, _h = hybrid_solve(make_tier_pois(None, None, hotel), hotel, req.days, cap_total / req.travelers,
732                                        scoring_mode='quality', pop_size=20, generations=40, mutation_rate=0.3,
733                                        verbose=False, diversity_weight=DIVERSITY_WEIGHT, ils=True)
734                  r2 = _prioritize_sights(r2, hotel, sorted((p for p in all_pois if p['category'] != 'restaurant'), key=lambda p: -p['score']),
735                                          sorted((p for p in all_pois if p['category'] == 'restaurant'), key=lambda p: p['cost']), cap_total / req.travelers)
736                  r2 = restore_originals(r2, originals)
737                  pkg2 = build_package(tier, hotel, r2, req.days, req.budget, runtime_ms + (time.time() - t0) * 1000.0,
738                                       req.travelers, POIS, max_total_budget=req.budget, hotel_cost_override=hotel_total)
739                  if (_bad(pkg2), -pkg2.total_score) < (_bad(pkg), -pkg.total_score):
740                      pkg = pkg2
741          pkg.notes = list(pref_notes)
742          if auto_no_hotel:
743              pkg.notes.append(f'งบ {req.budget:,.0f} บาท ไม่พอทั้งค่าที่พักและค่าอาหาร ระบบจึงสร้างแผนแบบไม่รวมค่าโรงแรมให้ (ที่พักถูกสุดของจังหวัดนี้ {sorted_hotels[0]["cost"]:,.0f} บาทต่อคืน) หากต้องการรวมที่พัก ลองเพิ่มงบหรือลดจำนวนวัน')
744          if _avail < 1.1 * _meal_min and hotel_total <= req.budget:
745              pkg.notes.append(f'งบต่อคน {_avail:,.0f} บาท แทบไม่พอค่าอาหารขั้นต่ำของ {req.days} วัน (ราว {_meal_min:,.0f} บาท) แผนจึงมีสถานที่ท่องเที่ยวน้อย ลองเพิ่มงบหรือลดจำนวนวัน')
746          if hotel_total > req.budget:   # ที่พักถูกสุดของจังหวัดแพงกว่างบทั้งหมด: ไม่มีเงินเหลือค่าอาหาร/ค่าเข้าชม
747              pkg.notes.append(f'งบ {req.budget:,.0f} บาท ไม่พอแม้แต่ค่าที่พัก {hotel_total:,.0f} บาท ({nights} คืน) แผนจึงไม่มีร้านอาหารและเกินงบ ลองเพิ่มงบ ลดจำนวนวัน หรือเลือก "ไม่รวมค่าโรงแรม"')
748          elif pkg.total_cost > req.budget * 1.05 + 1:
749              pkg.notes.append(f'งบ {req.budget:,.0f} บาท ไม่พอสำหรับ {req.days} วันในจังหวัดนี้ แผน{tier}มีค่าใช้จ่ายประมาณ {pkg.total_cost:,.0f} บาท ลองเพิ่มงบหรือลดจำนวนวัน')
750          empty = sum(1 for d in pkg.days if not d.pois)
751          if empty:   # จังหวัดข้อมูลน้อย: สถานที่ไม่พอเติมทุกวัน
752              pkg.notes.append(f'จังหวัดนี้มีข้อมูลสถานที่น้อย แผน{tier}มี {empty} วันที่ไม่มีกิจกรรม ลองลดจำนวนวันหรือเลือกจังหวัดอื่น')
753          packages.append(pkg)
754      return PackageResponse(request=req.dict(), packages=packages)
บรรทัด 715–719: สร้างแพ็กเกจด้วย build_package โดยใช้ target_total เป็นเพดานของระดับ
บรรทัด 720: งบกิจกรรมสูงสุดที่ผู้ใช้มีจริง cap_total
บรรทัด 721–725: ถ้าเป็น hybrid ฟังก์ชัน _bad ให้คะแนนความไม่ดี: (ไม่ valid, เกินงบเกิน 5%)
บรรทัด 726–740: ลองสร้างใหม่ไม่เกิน 3 ครั้งด้วยตัวเลือกทั้งหมดและ seed ใหม่ ถ้าแผนใหม่ดีกว่า (ผ่านข้อจำกัดและคะแนนสูงกว่า) จึงใช้แทน
บรรทัด 741–752: เพิ่มหมายเหตุถึงผู้ใช้: ข้อความจากความชอบ งบไม่พอทั้งที่พักและอาหาร (สร้างแผนไม่รวมโรงแรมให้) งบต่อคนแทบไม่พอค่าอาหาร ที่พักแพงกว่างบ แผนเกินงบ และวันที่ไม่มีกิจกรรมเพราะข้อมูลน้อย
บรรทัด 753–754: เพิ่มแพ็กเกจและคืน PackageResponse (ทั้ง 3 ระดับ)
บรรทัด 757–785  เซสชันร่วมกัน (Collaborative planning)
757  # ============================================================
758  # Collaborative planning: เซสชันที่แชร์ลิงก์ให้เพื่อนร่วมดู/แก้แผนเดียวกัน
759  # เก็บในหน่วยความจำและบันทึกลงไฟล์ data/sessions.json (กลับมาหลัง restart) — ใช้ version ทำ optimistic concurrency, ฝั่ง client โพลลิ่งทุก 2 วินาที
760  # ============================================================
761  SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sessions.json')
762
763
764  def _session_load():
765      try:
766          with open(SESSION_FILE, encoding='utf-8') as f:
767              return json.load(f)
768      except (OSError, ValueError):
769          return {}
770
771
772  def _session_save():   # เรียกขณะถือ SESSION_LOCK; เขียนไฟล์ชั่วคราวแล้ว replace กันไฟล์พังกลางคัน
773      try:
774          tmp = SESSION_FILE + '.tmp'
775          with open(tmp, 'w', encoding='utf-8') as f:
776              json.dump(SESSIONS, f, ensure_ascii=False)
777          os.replace(tmp, SESSION_FILE)
778      except OSError:
779          pass   # shortcut: บันทึกไม่ได้ก็ยังทำงานในหน่วยความจำต่อ
780
781
782  SESSIONS = _session_load()
783  SESSION_LOCK = threading.Lock()
784  SESSION_TTL_S = 24 * 3600
785  SESSION_MAX = 300
บรรทัด 757–760: คอมเมนต์: เซสชันที่แชร์ลิงก์ให้เพื่อนร่วมดู/แก้แผนเดียวกัน เก็บในหน่วยความจำและบันทึกลง data/sessions.json ใช้ version ทำ optimistic concurrency ฝั่ง client โพลลิ่งทุก 2 วินาที (ดู ➜ frontend/extras.js)
บรรทัด 761: SESSION_FILE พาธไฟล์เซสชัน
บรรทัด 764–769: _session_load โหลดเซสชันจากไฟล์ ถ้าอ่านไม่ได้เริ่มจากว่าง
บรรทัด 772–779: _session_save เขียนไฟล์ชั่วคราวแล้ว os.replace กันไฟล์พังกลางคัน ถ้าบันทึกไม่ได้ยังทำงานในหน่วยความจำต่อ
บรรทัด 782–785: ตัวแปรเซสชัน: SESSIONS ตัวล็อกเธรด อายุ 24 ชั่วโมง และจำนวนสูงสุด 300
บรรทัด 788–847  โมเดลและ endpoint ของเซสชัน
788  class SessionCreate(BaseModel):
789      province: str = DEFAULT_PROVINCE
790      package: dict
791      settings: dict = {}          # budget, travelers, include_hotel, start_date, preferences, locked, excluded
792
793
794  class SessionUpdate(BaseModel):
795      base_version: int
796      package: dict
797      settings: dict = {}
798
799
800  def _session_gc():
801      now = time.time()
802      for k in [k for k, v in SESSIONS.items() if now - v['updated'] > SESSION_TTL_S]:
803          del SESSIONS[k]
804
805
806  def _session_view(sid):
807      v = SESSIONS[sid]
808      return {'id': sid, 'version': v['version'], 'province': v['province'], 'package': v['package'], 'settings': v['settings']}
809
810
811  @app.post('/api/sessions')
812  def create_session(req: SessionCreate):
813      get_province(req.province)
814      if not isinstance(req.package.get('days'), list) or len(req.package['days']) > 7:
815          raise HTTPException(status_code=422, detail='invalid package')
816      with SESSION_LOCK:
817          _session_gc()
818          if len(SESSIONS) >= SESSION_MAX:
819              raise HTTPException(status_code=503, detail='too many sessions')
820          sid = secrets.token_urlsafe(6)
821          SESSIONS[sid] = {'version': 1, 'province': req.province, 'package': req.package,
822                           'settings': req.settings, 'updated': time.time()}
823          _session_save()
824          return _session_view(sid)
825
826
827  @app.get('/api/sessions/{sid}')
828  def get_session(sid: str, since: int = 0):
829      with SESSION_LOCK:
830          if sid not in SESSIONS:
831              raise HTTPException(status_code=404, detail='session not found or expired')
832          if since and SESSIONS[sid]['version'] == since:
833              return {'id': sid, 'version': since, 'changed': False}
834          return {**_session_view(sid), 'changed': True}
835
836
837  @app.put('/api/sessions/{sid}')
838  def update_session(sid: str, req: SessionUpdate):
839      with SESSION_LOCK:
840          if sid not in SESSIONS:
841              raise HTTPException(status_code=404, detail='session not found or expired')
842          cur = SESSIONS[sid]
843          if req.base_version != cur['version']:      # มีคนอื่นแก้ไปก่อน → ส่งสถานะล่าสุดกลับให้ client รวมเข้ากับของตัวเอง
844              raise HTTPException(status_code=409, detail=_session_view(sid))
845          cur.update(version=cur['version'] + 1, package=req.package, settings=req.settings or cur['settings'], updated=time.time())
846          _session_save()
847          return _session_view(sid)
บรรทัด 788–791: SessionCreate จังหวัด แพ็กเกจ และตั้งค่า (งบ จำนวนคน ไม่รวมโรงแรม วันเริ่ม ความชอบ จุดล็อก/ลบ)
บรรทัด 794–797: SessionUpdate เวอร์ชันฐาน แพ็กเกจใหม่ และตั้งค่า
บรรทัด 800–803: _session_gc ลบเซสชันที่เกินอายุ
บรรทัด 806–808: _session_view สร้างข้อมูลที่ส่งกลับ
บรรทัด 811–824: POST /api/sessions ตรวจแพ็กเกจ (รายการวัน ไม่เกิน 7) ล้างเซสชันเก่า จำกัดจำนวน สร้างรหัสสั้นแบบสุ่ม เวอร์ชัน 1 และบันทึกไฟล์
บรรทัด 827–834: GET /api/sessions/{sid} คืนเซสชัน ถ้าเวอร์ชันเท่ากับที่ client ถือ (since) คืน changed: False ลดข้อมูลที่ส่ง
บรรทัด 837–847: PUT /api/sessions/{sid} ถ้าเวอร์ชันฐานไม่ตรง (มีคนแก้ก่อน) ตอบ 409 พร้อมสถานะล่าสุดให้ client รวมเข้ากับของตัวเอง ถ้าตรง เพิ่มเวอร์ชันและบันทึก
บรรทัด 850–892  `POST /api/pareto` ทางเลือกหลายเป้าหมาย
850  @app.post('/api/pareto', response_model=PackageResponse)
851  def pareto(req: PackageRequest):
852      """หา Pareto front (NSGA-II) ระหว่าง คะแนน / ความหลากหลายของหมวด / ระยะทางรวม คืนแผนตัวแทนไม่เกิน 8 แผน
853      ใช้การตั้งค่าระดับ Standard (โรงแรม <=45% ใช้รวม <=75% ของงบ) ให้ผู้ใช้เลือก trade-off เอง"""
854      random.seed(req.seed)
855      data = get_province(req.province)
856      pool, pref_notes = apply_preferences(data['pois'], req.preferences, req.days)
857      nights = max(0, req.days - 1)
858      include_hotel = req.include_hotel if req.include_hotel is not None else True
859      hotels = sorted(data['hotels'], key=lambda h: h['cost'])
860      max_per_night = req.budget * 0.45 / max(nights, 1) if nights > 0 else 0
861      cands = [h for h in hotels if h['cost'] <= max_per_night] or hotels[:1]
862      hotel = max(cands, key=lambda h: h['score']) if include_hotel and nights > 0 else hotels[0]
863      hotel_total = hotel['cost'] * nights if include_hotel else 0
864      target_total = req.budget * 0.75
865      budget_for_act = max(0, target_total - hotel_total) / req.travelers
866      # เพดานราคาร้านอาหารเหมือนระดับ Standard (ไม่ให้ร้านแพงกินงบทั้งทริป) และเติมร้านถูกสุดถ้าไม่พอมื้อ
867      cap = min(400.0, max(150.0, budget_for_act / (max(req.days, 1) * 5.0)))
868      rests = [p for p in pool if p['category'] == 'restaurant']
869      ok_rests = [p for p in rests if p['cost'] <= cap]
870      need = 2 * req.days + 2
871      if len(ok_rests) < need:
872          ids = {p['id'] for p in ok_rests}
873          ok_rests += sorted((p for p in rests if p['id'] not in ids), key=lambda p: (not p.get('_diet'), p['cost']))[:need - len(ok_rests)]
874      keep_ids = {p['id'] for p in ok_rests}
875      pool = [p for p in pool if p['category'] != 'restaurant' or p['id'] in keep_ids]
876      t0 = time.time()
877      front = nsga2_solve(pool, hotel, req.days, budget_for_act, scoring_mode='quality', pop_size=40, generations=40)
878      runtime_ms = (time.time() - t0) * 1000.0
879      if len(front) > 8:   # เลือกตัวแทน 8 แผนกระจายตามระยะทาง (รวมสองปลาย)
880          by_dist = sorted(front, key=lambda s: s['distance_km'])
881          idx = sorted({round(i * (len(by_dist) - 1) / 7) for i in range(8)})
882          front = [by_dist[i] for i in idx]
883      packages = []
884      for i, sol in enumerate(sorted(front, key=lambda s: s['distance_km']), 1):
885          routes = restore_originals(sol['routes'], data['poi_by_id'])
886          pkg = build_package(f'Pareto {i}', hotel, routes, req.days, req.budget, runtime_ms / max(len(front), 1),
887                              req.travelers, pool, max_total_budget=target_total, hotel_cost_override=hotel_total)
888          pkg.objectives = {'score': round(sol['score'], 1), 'diversity': round(sol['diversity'], 2),
889                            'distance_km': round(sol['distance_km'], 1), 'cost': round(sol['cost'])}
890          pkg.notes = list(pref_notes)
891          packages.append(pkg)
892      return PackageResponse(request=req.dict(), packages=packages)
บรรทัด 850–853: ประกาศ endpoint คืนแผนตัวแทนไม่เกิน 8 แผนจาก Pareto front ด้วยการตั้งค่าระดับ Standard
บรรทัด 854–856: ตั้ง seed ดึงข้อมูลจังหวัด และปรับจุดตามความชอบ
บรรทัด 857–865: คำนวณจำนวนคืน เลือกโรงแรม (คะแนนสูงสุดภายใต้งบต่อคืน 45%) ค่าโรงแรม งบเป้าหมาย 75% และงบกิจกรรมต่อคน
บรรทัด 866–875: จำกัดราคาร้านอาหารเหมือนระดับ Standard และเติมร้านถูกสุดถ้าไม่พอมื้อ
บรรทัด 876–878: เรียก ➜ nsga2_solve() ใน algorithm/pareto.py (ประชากร 40 รุ่น 40)
บรรทัด 879–882: ถ้ามีเกิน 8 แผน เลือกตัวแทน 8 แผนกระจายตามระยะทาง (รวมสองปลาย)
บรรทัด 883–892: สร้างแพ็กเกจของแต่ละแผนเรียงตามระยะทาง ใส่วัตถุประสงค์ (คะแนน ความหลากหลาย ระยะ ค่าใช้จ่าย) และคืนผล
บรรทัด 895–911  `POST /api/recompute`
895  @app.post('/api/recompute', response_model=Package)
896  def recompute(req: RecomputeRequest):
897      data = get_province(req.province)
898      HOTEL_BY_ID, POI_BY_ID = data['hotel_by_id'], data['poi_by_id']
899      if req.hotel_id not in HOTEL_BY_ID:
900          raise HTTPException(status_code=404, detail=f'Hotel {req.hotel_id} not found')
901      hotel = HOTEL_BY_ID[req.hotel_id]
902      routes_per_day = []
903      for day in req.routes:
904          day_pois = []
905          for pid in day:
906              if pid not in POI_BY_ID:
907                  raise HTTPException(status_code=404, detail=f'POI {pid} not found')
908              day_pois.append(POI_BY_ID[pid])
909          routes_per_day.append(day_pois)
910      return build_package('Custom', hotel, routes_per_day, req.days,
911                           req.budget, 0, req.travelers, data['pois'])
บรรทัด 895–901: คำนวณแพ็กเกจใหม่หลังผู้ใช้ลากเรียง/สลับ ดึงข้อมูลจังหวัด ตรวจโรงแรมมีจริง (ไม่พบตอบ 404)
บรรทัด 902–909: แปลงรายการ id รายวันเป็นวัตถุจุด ถ้าไม่พบ id ตอบ 404
บรรทัด 910–911: สร้างแพ็กเกจ Custom จากแผนที่ผู้ใช้จัด (ไม่เรียกอัลกอริทึม เป็นการคำนวณเบา จึงไม่ถูกจำกัดอัตราคำขอ)
บรรทัด 915–946  `POST /api/reoptimize`
915  @app.post('/api/reoptimize', response_model=Package)
916  def reoptimize(req: ReoptimizeRequest):
917      """ปรับแผนใหม่ด้วย Hybrid หลังผู้ใช้ swap/เพิ่ม/ลบ POI โดยคงจุดที่ผู้ใช้เลือก (locked) และไม่ใส่จุดที่ลบ (excluded)"""
918      random.seed(req.seed)
919      data = get_province(req.province)
920      if req.hotel_id not in data['hotel_by_id']:
921          raise HTTPException(status_code=404, detail=f'Hotel {req.hotel_id} not found')
922      hotel = data['hotel_by_id'][req.hotel_id]
923      poi_by_id = data['poi_by_id']
924      for pid in [i for day in req.routes for i in day] + req.locked + req.excluded:
925          if pid not in poi_by_id:
926              raise HTTPException(status_code=404, detail=f'POI {pid} not found')
927      routes = [[poi_by_id[i] for i in day if i not in req.excluded] for day in req.routes]
928      nights = max(0, req.days - 1)
929      hotel_total = hotel['cost'] * nights if req.include_hotel else 0
930      budget_for_act = max(0, req.budget - hotel_total) / req.travelers
931      # POI ที่ผู้ใช้เลือกแต่ใส่ในแผนใดไม่ได้ (เช่น เปิดดึกเกินเวลาต่อวัน/เกินงบ) → นำออกและแจ้งผู้ใช้
932      bad = set(infeasible_locks(data['pois'], hotel, req.locked, budget_for_act))
933      routes = [[p for p in day if p['id'] not in bad] for day in routes]
934      pool, _ = apply_preferences(data['pois'], req.preferences, req.days)
935      t0 = time.time()
936      new_routes = reoptimize_solve(pool, hotel, routes, budget_for_act,
937                                    locked_ids=[i for i in req.locked if i not in bad], excluded_ids=req.excluded,
938                                    diversity_weight=DIVERSITY_WEIGHT)
939      new_routes = restore_originals(new_routes, poi_by_id)
940      runtime_ms = (time.time() - t0) * 1000.0
941      pkg = build_package(req.tier, hotel, new_routes, req.days, req.budget, runtime_ms,
942                           req.travelers, data['pois'], max_total_budget=req.budget,
943                           hotel_cost_override=hotel_total)
944      in_plan = {p['id'] for day in new_routes for p in day}
945      pkg.notes = [f"ใส่ {poi_by_id[i]['name_th']} ในแผนไม่ได้ (เวลาเปิด-ปิด งบ หรือเวลาต่อวันไม่พอ)" for i in req.locked if i not in in_plan]
946      return pkg
บรรทัด 915–917: ประกาศ endpoint ปรับแผนใหม่ด้วย Hybrid หลังผู้ใช้สลับ/เพิ่ม/ลบ โดยคงจุดล็อกและไม่ใส่จุดที่ลบ
บรรทัด 918–926: ตั้ง seed ดึงข้อมูลจังหวัด ตรวจโรงแรมและ id ทุกตัว
บรรทัด 927: แปลง id เป็นจุดและตัดจุดที่ลบ
บรรทัด 928–930: ค่าโรงแรมและงบกิจกรรมต่อคน
บรรทัด 931–933: หาจุดล็อกที่ใส่ไม่ได้ด้วย ➜ infeasible_locks() ใน algorithm/hybrid.py แล้วถอดออกจากแผน (แจ้งผู้ใช้ภายหลัง)
บรรทัด 934: ปรับจุดตามความชอบ
บรรทัด 935–940: เรียก ➜ reoptimize_solve() ใน algorithm/hybrid.py แล้วคืนวัตถุต้นฉบับและจับเวลา
บรรทัด 941–943: สร้างแพ็กเกจ
บรรทัด 944–946: เพิ่มหมายเหตุสำหรับจุดล็อกที่ใส่ในแผนไม่ได้
บรรทัด 949–960  เสิร์ฟหน้าเว็บและรันเซิร์ฟเวอร์
949  # เสิร์ฟหน้าเว็บจากบริการเดียวกัน (ตอน deploy) — ต้อง mount หลังประกาศ API ทั้งหมด
950  _FRONT = os.path.join(os.path.dirname(THIS_DIR), 'frontend')
951  if os.path.isdir(_FRONT):
952      app.mount('/', StaticFiles(directory=_FRONT, html=True), name='frontend')
953
954
955  if __name__ == '__main__':
956      import uvicorn
957      print('Starting WeEasyTrip API...')
958      for _s, _d in DATA.items():
959          print(f"Loaded {_s}: {len(_d['pois'])} POIs, {len(_d['hotels'])} hotels")
960      uvicorn.run(app, host='0.0.0.0', port=8000)
บรรทัด 949–952: ถ้ามีโฟลเดอร์ frontend ให้ mount เป็นเว็บไฟล์ static ที่ราก / (ต้อง mount หลังประกาศ API ทั้งหมด ไม่งั้นจะบังเส้นทาง API) ดูหน้าเว็บที่ ➜ frontend/index.html
บรรทัด 955–960: เมื่อรันไฟล์ตรง ๆ พิมพ์จำนวนจุด/โรงแรมที่โหลดของแต่ละจังหวัด และเปิด uvicorn ที่พอร์ต 8000

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
algorithm/pareto.py
algorithm/rl.py
algorithm/utils.py
data/thai_provinces.py
frontend/app.js
frontend/extras.js
frontend/index.html