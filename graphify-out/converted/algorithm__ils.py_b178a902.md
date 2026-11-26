<!-- converted from algorithm__ils.py.docx -->

คู่มือโค้ด: algorithm/ils.py
Insertion Local Search (ILS) ปรับปรุงแผนที่ Hybrid สร้างแล้ว
ไฟล์ต้นฉบับ: algorithm/ils.py (137 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ขั้นตอนสุดท้ายของ ➜ hybrid_solve() ใน algorithm/hybrid.py (ขั้นที่ 7) ทำงานรายวัน: แทนที่จุดด้วยจุดที่ยังไม่ใช้ที่คุ้มกว่า เติมช่องที่เที่ยวที่ว่าง และ "เขย่า" (shake) เพื่อหนีค่าเหมาะสมเฉพาะที่ ใช้ตัวตรวจแผนจาก ➜ evaluate_route() ใน algorithm/utils.py และใช้ค่าถ่วงเดียวกับ fitness ของ Hybrid

บรรทัด 1–18  หัวไฟล์ นำเข้า และค่าคงที่
1  ﻿# -*- coding: utf-8 -*-
2  """
3  ils.py - Insertion local search (Iterated Local Search) สำหรับปรับปรุงแผนที่ Hybrid สร้างแล้ว
4
5  (1) แทนที่สถานที่ในแต่ละช่องด้วยสถานที่ที่ยังไม่ได้ใช้ (หมวดเดียวกัน: attraction หรือร้านอาหาร)
6      ถ้า objective ดีขึ้นโดยผ่านข้อจำกัด (เวลาต่อวัน เวลาปิด) และไม่เกินงบ
7  (2) เติมช่อง attraction ที่ว่าง (วันที่มี < 4 จุด) ที่ตำแหน่งดีที่สุด
8  (3) shake: แทนที่ 2 จุดแบบสุ่ม แล้ว local search ซ้ำ เก็บแผนที่ดีที่สุด
9  โครงสร้างวัน: <= 4 attraction, 2 มื้อ (6 จุด/วัน) — วิธีมาตรฐานของ TOPTW ที่ GA ที่สุ่มสลับไม่ได้ทำอย่างเป็นระบบ
10  """
11  import random
12  from typing import Dict, List
13
14  import utils
15  from utils import evaluate_route, MAX_ATTRS
16
17  DIST_WEIGHT = 0.3    # ต้องตรงกับ hybrid.DIST_WEIGHT
18  IDLE_WEIGHT = 0.02   # ต้องตรงกับค่า idle ใน hybrid._fitness
บรรทัด 1–10: docstring อธิบายสามขั้นตอนของ ILS: (1) แทนที่จุดในแต่ละช่องด้วยจุดที่ยังไม่ใช้ในหมวดเดียวกันเมื่อ objective ดีขึ้นและยังผ่านข้อจำกัด (2) เติมช่องที่เที่ยวที่ว่างในวันที่มีไม่ถึง 4 จุด (3) shake แทน 2 จุดแบบสุ่มแล้วค้นหาซ้ำ เก็บแผนที่ดีที่สุด
บรรทัด 11: นำเข้า random สำหรับการสุ่มลำดับวันและการ shake
บรรทัด 12: นำเข้า type hint
บรรทัด 14: นำเข้า utils ทั้งโมดูล (ใช้ utils.TIME_WEIGHT ที่บรรทัด 34)
บรรทัด 15: นำเข้า ➜ evaluate_route() ใน algorithm/utils.py และ MAX_ATTRS (ที่เที่ยวสูงสุด 4 ต่อวัน)
บรรทัด 17: DIST_WEIGHT = 0.3 ค่าถ่วงระยะขับ ต้องตรงกับ ➜ algorithm/hybrid.py (ซ้ำค่าเพราะ ils.py นำเข้า hybrid ไม่ได้ ไม่งั้นวนกัน)
บรรทัด 18: IDLE_WEIGHT = 0.02 ค่าถ่วงเวลารอก่อนมื้อ ต้องตรงกับ _fitness ใน ➜ _fitness() ใน algorithm/hybrid.py
บรรทัด 21–34  วัตถุประสงค์ของ 1 วัน
21  def day_objective(day: List[Dict], hotel: Dict, diversity_weight: float):
22      """(objective, cost) ของแผน 1 วัน หรือ None ถ้าไม่ผ่านข้อจำกัด"""
23      ev = evaluate_route([day], hotel, float('inf'))
24      if not ev['valid']:
25          return None
26      det = ev['days_detail'][0]
27      # หมายเหตุ: ไม่บังคับช่วงเวลามื้อ เพราะแผนที่ Hybrid/GA สร้างไม่ได้บังคับ (ตรงกับนิยามความถูกต้องของ evaluate_route)
28      obj = det['score']
29      if diversity_weight:
30          cats = [p['category'] for p in day if p['category'] != 'restaurant']
31          if cats:
32              counts = {c: cats.count(c) for c in set(cats)}
33              obj += diversity_weight * ((len(counts) - 1) - sum(max(0, n - 2) for n in counts.values()))
34      return obj - DIST_WEIGHT * det['distance_km'] - IDLE_WEIGHT * det['idle_min'] - utils.TIME_WEIGHT * det['time_min'], det['cost']
บรรทัด 21: ประกาศ day_objective รับวัน โรงแรม และน้ำหนักความหลากหลาย
บรรทัด 22: docstring: คืน (objective, ค่าใช้จ่าย) หรือ None ถ้าวันนั้นไม่ผ่านข้อจำกัด
บรรทัด 23: ประเมินวันเดียวด้วย evaluate_route
บรรทัด 24–25: ถ้าไม่ valid คืน None (ILS จะไม่ยอมรับแผนที่ผิดข้อจำกัด)
บรรทัด 26: ดึงรายละเอียดของวันนั้น
บรรทัด 27: คอมเมนต์: ไม่บังคับช่วงเวลามื้อเพิ่ม เพราะแผนของ Hybrid/GA ก็ไม่ได้บังคับ จึงตรงกับนิยาม valid ของ evaluate_route
บรรทัด 28: เริ่มจากคะแนนรวมของวัน
บรรทัด 29–33: ถ้ามีน้ำหนักความหลากหลาย บวกด้วย w × (จำนวนหมวดต่างกัน − 1) และหักการซ้ำหมวดเกิน 2 จุด
บรรทัด 34: คืน objective = คะแนน − ถ่วงระยะขับ − ถ่วงเวลารอ − ถ่วงเวลาทั้งวัน พร้อมค่าใช้จ่ายของวัน
บรรทัด 37–39  ตรวจว่ายังมีที่ว่างสำหรับที่เที่ยว
37  def _has_room(day, hotel):
38      """เพิ่มจุดได้ถ้ายังไม่ถึง MAX_ATTRS (เที่ยว 4 จุด/วัน) — ไม่ยืดเกินเพดาน ใช้การสลับจุดให้คุ้มขึ้นแทน"""
39      return sum(1 for p in day if p['category'] != 'restaurant') < MAX_ATTRS
บรรทัด 37–38: ประกาศ _has_room และ docstring: เพิ่มจุดได้ถ้ายังไม่ถึง 4 ที่เที่ยวต่อวัน ไม่ยืดเกินเพดาน
บรรทัด 39: คืนจริงถ้าจำนวนที่ไม่ใช่ร้านอาหารน้อยกว่า MAX_ATTRS
บรรทัด 42–58  ฟังก์ชันหลัก: เตรียมสถานะ
42  def insertion_local_search(routes: List[List[Dict]], pois: List[Dict], hotel: Dict, budget: float,
43                             diversity_weight: float = 0.0, locked=(), shakes: int = 8, top_k: int = 40) -> List[List[Dict]]:
44      locked = set(locked)
45      cur = [list(d) for d in routes]
46      base = [day_objective(d, hotel, diversity_weight) if d else (0.0, 0.0) for d in cur]
47      if any(b is None for b in base):
48          return routes                        # แผนเริ่มต้นไม่ผ่านเงื่อนไขของ ILS — ไม่แตะ
49      objs = [b[0] for b in base]
50      costs = [b[1] for b in base]
51      used = {p['id'] for d in cur for p in d}
52      by_score = sorted(pois, key=lambda p: -p['score'])
53      unused = {'attr': [p for p in by_score if p['category'] != 'restaurant' and p['id'] not in used],
54                'rest': [p for p in by_score if p['category'] == 'restaurant' and p['id'] not in used]}
55
56      def kind(p):
57          return 'rest' if p['category'] == 'restaurant' else 'attr'
58
บรรทัด 42–43: ประกาศ insertion_local_search รับแผน จุดทั้งหมด โรงแรม งบ น้ำหนักความหลากหลาย จุดล็อก จำนวนรอบ shake (8) และจำนวนตัวเลือกที่พิจารณา top_k (40)
บรรทัด 44: ทำเป็นเซ็ตของ id จุดล็อก (ห้ามแตะ)
บรรทัด 45: คัดลอกแผน
บรรทัด 46: คำนวณ objective ของทุกวัน (วันว่างให้ (0,0))
บรรทัด 47–48: ถ้าวันใดไม่ผ่านเงื่อนไขของ ILS คืนแผนเดิมโดยไม่แตะ
บรรทัด 49–50: แยก objective และค่าใช้จ่ายรายวัน
บรรทัด 51: ชุด id จุดที่ใช้อยู่
บรรทัด 52: เรียงจุดทั้งหมดตามคะแนนมากไปน้อย
บรรทัด 53–54: unused เก็บจุดที่ยังไม่ใช้แยกเป็นที่เที่ยว (attr) และร้านอาหาร (rest) เรียงตามคะแนน
บรรทัด 56–57: ฟังก์ชัน kind บอกชนิดของจุด (ร้านอาหาร หรือที่เที่ยว)
บรรทัด 59–88  local_search ส่วนแทนที่จุด
59      def local_search():
60          improved = True
61          while improved:
62              improved = False
63              order = list(range(len(cur)))
64              random.shuffle(order)
65              for d in order:
66                  day = cur[d]
67                  for i in range(len(day)):
68                      a = day[i]
69                      if a['id'] in locked:
70                          continue
71                      best = None
72                      for u in unused[kind(a)][:top_k]:
73                          trial = day[:i] + [u] + day[i + 1:]
74                          r = day_objective(trial, hotel, diversity_weight)
75                          if r is None or sum(costs) - costs[d] + r[1] > budget:
76                              continue
77                          gain = r[0] - objs[d]
78                          if gain > 1e-9 and (best is None or gain > best[0]):
79                              best = (gain, u, trial, r)
80                      if best:
81                          _g, u, trial, r = best
82                          unused[kind(a)].remove(u)
83                          unused[kind(a)].append(a)
84                          unused[kind(a)].sort(key=lambda p: -p['score'])
85                          cur[d] = trial
86                          day = trial
87                          objs[d], costs[d] = r
88                          improved = True
บรรทัด 59: ประกาศ local_search ลูปปรับปรุงจนไม่มีอะไรดีขึ้น
บรรทัด 60–62: ตั้งธง improved และวนต่อตราบที่ยังปรับปรุงได้
บรรทัด 63–64: สลับลำดับการวนวันแบบสุ่ม
บรรทัด 65–67: วนทีละวัน ทีละตำแหน่งในวัน
บรรทัด 68–70: ข้ามจุดที่ผู้ใช้ล็อก
บรรทัด 71–72: เตรียมหาตัวแทนที่ดีที่สุดจาก top_k จุดแรกของหมวดเดียวกัน
บรรทัด 73: ลองแทนที่ตำแหน่ง i ด้วยจุดที่ยังไม่ใช้
บรรทัด 74: คำนวณ objective ของวันที่แทนแล้ว
บรรทัด 75–76: ข้ามถ้าไม่ผ่านข้อจำกัด หรือค่าใช้จ่ายรวมทั้งทริปเกินงบ
บรรทัด 77–79: คำนวณผลต่าง (gain) เก็บตัวที่ gain มากสุด
บรรทัด 80–85: ถ้าพบ ให้นำจุดเดิมกลับเข้า unused เอาตัวแทนออก เรียงใหม่ และใช้แผนใหม่ของวัน
บรรทัด 86–88: อัปเดต objective ค่าใช้จ่ายของวัน และตั้งธง improved
บรรทัด 89–105  local_search ส่วนเติมช่องที่เที่ยวที่ว่าง
89                  if day and _has_room(day, hotel):
90                      best = None
91                      for u in unused['attr'][:top_k]:
92                          for j in range(len(day) + 1):
93                              trial = day[:j] + [u] + day[j:]
94                              r = day_objective(trial, hotel, diversity_weight)
95                              if r is None or sum(costs) - costs[d] + r[1] > budget:
96                                  continue
97                              gain = r[0] - objs[d]
98                              if gain > 1e-9 and (best is None or gain > best[0]):
99                                  best = (gain, u, trial, r)
100                      if best:
101                          _g, u, trial, r = best
102                          unused['attr'].remove(u)
103                          cur[d] = trial
104                          objs[d], costs[d] = r
105                          improved = True
บรรทัด 89: ถ้าวันนั้นยังมีที่ให้เพิ่มที่เที่ยว
บรรทัด 90: เตรียมตัวแทนที่ดีที่สุด
บรรทัด 91–93: ลองแทรกที่เที่ยวที่ยังไม่ใช้ทุกตำแหน่งของวัน
บรรทัด 94–96: คำนวณ objective ข้ามถ้าไม่ผ่านหรือเกินงบ
บรรทัด 97–99: เก็บทางเลือกที่ gain มากสุด
บรรทัด 100–105: ถ้าพบ ใช้แผนที่แทรกแล้ว เอาจุดออกจาก unused และอัปเดตสถานะ
บรรทัด 107–111  สำเนาสถานะและรอบแรก
107      def snapshot():
108          return ([list(d) for d in cur], list(objs), list(costs), {k: list(v) for k, v in unused.items()})
109
110      local_search()
111      best_state = snapshot()
บรรทัด 107–108: ฟังก์ชัน snapshot ถ่ายสำเนาแผน objective ค่าใช้จ่าย และ unused เพื่อกลับมาใช้ภายหลัง
บรรทัด 110: รัน local_search รอบแรก
บรรทัด 111: เก็บแผนที่ดีที่สุดตอนนี้
บรรทัด 112–137  shake: เขย่าแล้วค้นหาซ้ำ
112      for _ in range(shakes):
113          for _k in range(2):
114              cand = [(d, i) for d, day in enumerate(cur) for i, p in enumerate(day)
115                      if p['category'] != 'restaurant' and p['id'] not in locked]
116              if not cand or not unused['attr']:
117                  break
118              d, i = random.choice(cand)
119              u = random.choice(unused['attr'][:top_k * 2])
120              trial = cur[d][:i] + [u] + cur[d][i + 1:]
121              r = day_objective(trial, hotel, diversity_weight)
122              if r is None or sum(costs) - costs[d] + r[1] > budget:
123                  continue
124              a = cur[d][i]
125              unused['attr'].remove(u)
126              unused['attr'].append(a)
127              unused['attr'].sort(key=lambda p: -p['score'])
128              cur[d] = trial
129              objs[d], costs[d] = r
130          local_search()
131          if sum(objs) > sum(best_state[1]) + 1e-9:
132              best_state = snapshot()
133          else:                                # ไม่ดีขึ้น: กลับไปแผนที่ดีที่สุด
134              cur = [list(d) for d in best_state[0]]
135              objs, costs = list(best_state[1]), list(best_state[2])
136              unused = {k: list(v) for k, v in best_state[3].items()}
137      return best_state[0]
บรรทัด 112: วนตามจำนวนรอบ shake (8)
บรรทัด 113: ในแต่ละรอบแทนจุดแบบสุ่ม 2 ครั้ง
บรรทัด 114–115: รวบรวมที่เที่ยวที่ไม่ล็อกในแผนเป็นตัวเลือก
บรรทัด 116–117: ถ้าไม่มีตัวเลือก หรือไม่เหลือที่เที่ยวที่ยังไม่ใช้ ออกจากลูป
บรรทัด 118–119: สุ่มตำแหน่งและสุ่มตัวแทนจาก top_k × 2 ตัวแรก
บรรทัด 120–123: สร้างแผนที่แทนแล้วตรวจ ถ้าไม่ผ่านหรือเกินงบ ข้าม
บรรทัด 124–129: ถ้าผ่าน แทนจริงและอัปเดตสถานะ
บรรทัด 130: ค้นหาซ้ำด้วย local_search
บรรทัด 131–132: ถ้าผลรวม objective ดีกว่าที่ดีที่สุดเดิม จดสถานะนี้ไว้
บรรทัด 133–136: ถ้าไม่ดีขึ้น ย้อนกลับไปสถานะที่ดีที่สุด
บรรทัด 137: คืนแผนที่ดีที่สุด (ที่ผ่านการตรวจซ้ำใน ➜ hybrid_solve() ใน algorithm/hybrid.py ก่อนรับไปใช้)

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/hybrid.py
algorithm/utils.py