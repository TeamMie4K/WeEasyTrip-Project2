<!-- converted from data__fetch_pois_osm.py.docx -->

คู่มือโค้ด: data/fetch_pois_osm.py
ดึงสถานที่และโรงแรมของจังหวัดจาก OpenStreetMap (Overpass API)
ไฟล์ต้นฉบับ: data/fetch_pois_osm.py (387 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: หัวใจของท่อสร้างข้อมูลจังหวัด: ส่งคำค้นไปที่ Overpass API (ฟรี ไม่ต้องใช้คีย์) ตามขอบเขตของจังหวัดใน data/provinces.json แปลงข้อมูลดิบของ OSM เป็นสถานที่ (POI) และโรงแรมตามโครงสร้างเดียวกับ phuket.json เขียนเป็น data/provinces/<slug>.json ถูกเรียกจาก ➜ data/build_all_provinces.py ข้อจำกัดสำคัญคือคะแนนสถานที่ประเมินจากความสมบูรณ์ของข้อมูลใน OSM (ไม่ใช่รีวิวจริง) ราคาโรงแรมประมาณจากดาว และราคาร้านอาหารประมาณจากประเภทอาหาร ข้อมูลที่ได้ถูกโหลดโดย ➜ load_data() ใน algorithm/utils.py และ ➜ backend/main.py

บรรทัด 1–19  หัวไฟล์ นำเข้า และ endpoint
1  # -*- coding: utf-8 -*-
2  """
3  fetch_pois_osm.py — ดึง POI + โรงแรมของจังหวัดจาก OpenStreetMap (Overpass API) ฟรี ไม่ต้อง API key
4  รัน:  python fetch_pois_osm.py <slug>        เช่น  python fetch_pois_osm.py chiangmai
5  อ่านขอบเขต (bbox) จาก provinces.json และเขียน provinces/<slug>.json (schema เดียวกับ phuket.json)
6
7  ข้อจำกัดของข้อมูล OSM (ต้องระบุในรายงาน):
8    - score ประเมินจาก heuristic (มี wikidata/website ฯลฯ) ไม่ใช่รีวิวจริง
9    - ราคาโรงแรมประมาณจากจำนวนดาว (OSM ไม่มีราคา); ค่าเข้าสถานที่ใช้ค่าเริ่มต้นตามหมวด
10  """
11  import json, os, re, sys, time, urllib.request, urllib.parse
12  from collections import Counter
13
14  HERE = os.path.dirname(os.path.abspath(__file__))
15  ENDPOINTS = [
16      "https://overpass-api.de/api/interpreter",
17      "https://overpass.kumi.systems/api/interpreter",
18      "https://overpass.private.coffee/api/interpreter",
19  ]
บรรทัด 1–10: docstring อธิบายหน้าที่ วิธีรัน และข้อจำกัดของข้อมูล OSM ที่ต้องระบุในรายงาน (คะแนนเป็นค่าประเมิน ราคาโรงแรมจากดาว ค่าเข้าสถานที่เป็นค่าเริ่มต้น)
บรรทัด 11–12: นำเข้าโมดูลมาตรฐานและ Counter
บรรทัด 14: HERE โฟลเดอร์ data/
บรรทัด 15–19: ENDPOINTS เซิร์ฟเวอร์ Overpass สามแห่งไว้สลับเมื่อแห่งใดล่ม
บรรทัด 21–73  ตารางคำค้นและค่าตั้งต้น
21  # (osm_filter, category, duration_min, cost)
22  QUERIES = [
23      ('node["amenity"="place_of_worship"]["religion"="buddhist"]["name"]', 'temple', 60, 0),
24      ('way["amenity"="place_of_worship"]["religion"="buddhist"]["name"]',  'temple', 60, 0),
25      ('node["natural"="beach"]["name"]', 'beach', 90, 0),
26      ('way["natural"="beach"]["name"]',  'beach', 90, 0),
27      ('node["tourism"="viewpoint"]["name"]', 'viewpoint', 40, 0),
28      ('node["tourism"="museum"]["name"]',    'culture', 60, 100),
29      ('node["historic"="monument"]["name"]', 'culture', 40, 0),
30      ('node["amenity"="marketplace"]["name"]', 'market', 60, 0),
31      ('way["amenity"="marketplace"]["name"]',  'market', 60, 0),
32      ('node["leisure"="water_park"]["name"]',  'activity', 180, 800),
33      ('node["tourism"="theme_park"]["name"]',  'activity', 180, 500),
34      ('node["tourism"="zoo"]["name"]',         'activity', 150, 400),
35      ('node["tourism"="attraction"]["name"]',  'culture', 45, 0),
36      ('node["amenity"="restaurant"]["name"]',  'restaurant', 60, 200),
37  ]
38  # หมวดเสริม (กิจกรรม/ธรรมชาติ/สปา) และร้านอาหารหลายระดับราคา — ใช้กับ --extra
39  EXTRA_QUERIES = [
40      ('node["natural"="waterfall"]["name"]', 'viewpoint', 60, 0),
41      ('way["boundary"="national_park"]["name"]', 'activity', 180, 200),
42      ('rel["boundary"="national_park"]["name"]', 'activity', 180, 200),
43      ('node["leisure"="nature_reserve"]["name"]', 'activity', 120, 100),
44      ('way["leisure"="nature_reserve"]["name"]', 'activity', 120, 100),
45      ('node["shop"="massage"]["name"]', 'activity', 90, 300),
46      ('node["leisure"="spa"]["name"]', 'activity', 90, 400),
47      ('node["amenity"="dive_centre"]["name"]', 'activity', 240, 1500),
48      ('node["amenity"="cooking_school"]["name"]', 'activity', 180, 900),
49      ('node["sport"="climbing"]["name"]', 'activity', 120, 500),
50      ('node["leisure"="garden"]["name"]', 'culture', 45, 50),
51      ('node["tourism"="gallery"]["name"]', 'culture', 45, 100),
52      ('node["amenity"="restaurant"]["name"]', 'restaurant', 60, 200),
53      ('node["amenity"="fast_food"]["name"]', 'restaurant', 40, 80),
54      ('node["amenity"="food_court"]["name"]', 'restaurant', 50, 100),
55      # ชนบท: ร้านมักถูกแมปเป็นอาคาร (way) หรือเป็นร้านกาแฟ — เพิ่มเพื่อให้จังหวัดข้อมูลน้อยมีร้านพอ
56      ('way["amenity"="restaurant"]["name"]', 'restaurant', 60, 200),
57      ('node["amenity"="cafe"]["name"]', 'restaurant', 45, 100),
58      ('way["amenity"="cafe"]["name"]', 'restaurant', 45, 100),
59      ('way["amenity"="fast_food"]["name"]', 'restaurant', 40, 80),
60  ]
61  HOTEL_QUERIES = [
62      ('node["tourism"="hotel"]["name"]',       3),
63      ('way["tourism"="hotel"]["name"]',        3),
64      ('node["tourism"="resort"]["name"]',      4),
65      ('node["tourism"="guest_house"]["name"]', 2),
66      ('node["tourism"="hostel"]["name"]',      1),
67  ]
68  MAX_PER_CATEGORY = {'restaurant': 50}   # หมวดอื่นเก็บสูงสุด 40
69  DEFAULT_MAX = 40
70  HOURS = {'restaurant': (660, 1320), 'market': (1020, 1380), 'beach': (360, 1320)}
71  HOTEL_COST = {1: 450, 2: 600, 3: 1100, 4: 2200, 5: 5000}
72  HOTEL_SCORE = {1: 7.0, 2: 7.4, 3: 7.8, 4: 8.4, 5: 9.1}
73  HOTELS_PER_STAR = 6
บรรทัด 21–37: QUERIES คำค้นหลักแต่ละรายการเป็น (ตัวกรอง OSM, หมวด, เวลาที่ใช้เป็นนาที, ค่าเข้า): วัด หาด จุดชมวิว พิพิธภัณฑ์ อนุสาวรีย์ ตลาด สวนน้ำ สวนสนุก สวนสัตว์ จุดท่องเที่ยว และร้านอาหาร
บรรทัด 38–60: EXTRA_QUERIES หมวดเสริม (น้ำตก อุทยาน เขตสงวน นวด สปา ดำน้ำ โรงเรียนทำอาหาร ปีนผา สวน แกลเลอรี) และร้านอาหารหลายระดับราคา รวมร้านที่ถูกแมปเป็นอาคาร ร้านกาแฟ และฟาสต์ฟู้ด เพื่อให้จังหวัดชนบทมีร้านพอ
บรรทัด 61–67: HOTEL_QUERIES ชนิดที่พักพร้อมจำนวนดาวตั้งต้น (โรงแรม รีสอร์ต เกสต์เฮาส์ โฮสเทล)
บรรทัด 68–69: จำนวนสูงสุดต่อหมวด (ร้านอาหาร 50 หมวดอื่น 40)
บรรทัด 70: HOURS เวลาเปิด-ปิดตั้งต้นตามหมวด
บรรทัด 71–72: ค่าห้องและคะแนนตั้งต้นของโรงแรมตามจำนวนดาว
บรรทัด 73: HOTELS_PER_STAR = 6 จำนวนโรงแรมสูงสุดต่อระดับดาว
บรรทัด 76–103  เรียก Overpass
76  AREA = None   # ชื่อจังหวัด (ไทย) ที่ใช้ค้นตามเขต; None = ใช้ bbox
77  _BAD = {}   # url -> เวลาที่ล้มเหลวล่าสุด: ข้าม mirror ที่เพิ่งล้มเหลวเป็นเวลา 10 นาที ลดเวลารอเมื่อ mirror ไหนล่ม
78
79
80  def overpass(filter_str, bbox):
81      """ส่ง query พร้อม fallback หลาย mirror (จำ mirror ที่ล่มชั่วคราว) และ retry แบบ exponential backoff"""
82      if AREA:   # จำกัดตามเส้นเขตจังหวัดจริง (admin_level=4) แทนกรอบสี่เหลี่ยม ไม่ให้ปนกับจังหวัดข้างเคียง
83          body = (f'area["boundary"="administrative"]["admin_level"="4"]["name"~"{AREA}"]->.a;'
84                  f'({filter_str}(area.a););')
85      else:
86          body = f"({filter_str}({','.join(map(str, bbox))}););"
87      q = 'data=' + urllib.parse.quote(f"[out:json][timeout:180];{body}out center 400;")
88      last = None
89      for attempt in range(4):
90          now = time.time()
91          urls = [u for u in ENDPOINTS if now - _BAD.get(u, 0) > 600] or list(ENDPOINTS)
92          for url in urls:
93              try:
94                  req = urllib.request.Request(url, data=q.encode(), headers={
95                      "Content-Type": "application/x-www-form-urlencoded",
96                      "User-Agent": "ThesisProject/1.0 (thai-tourism-research)"})
97                  with urllib.request.urlopen(req, timeout=200) as r:
98                      return json.loads(r.read())
99              except Exception as e:
100                  last = e
101                  _BAD[url] = time.time()
102          time.sleep(5 * 2 ** attempt)
103      raise RuntimeError(f"Overpass failed: {last}")
บรรทัด 76: AREA ชื่อจังหวัดไทยที่ใช้ค้นตามเขตการปกครอง (ถ้าไม่ตั้งใช้ bbox)
บรรทัด 77: _BAD จำ mirror ที่ล้มเหลวล่าสุด ข้ามไป 10 นาที
บรรทัด 80–81: ประกาศ overpass และ docstring (สลับ mirror ได้ และ retry แบบถอยหลังเพิ่มเป็นทวีคูณ)
บรรทัด 82–84: ถ้ามี AREA ค้นตามเส้นเขตจังหวัดจริง (admin_level=4) ไม่ให้ปนกับจังหวัดข้างเคียง
บรรทัด 85–86: ไม่เช่นนั้นค้นในกรอบสี่เหลี่ยม bbox
บรรทัด 87: ประกอบคำขอ Overpass (JSON timeout 180 วินาที ผลสูงสุด 400)
บรรทัด 88–102: วนลอง 4 รอบ: เลือก mirror ที่ยังไม่ล้มเหลวล่าสุด ส่งคำขอ ถ้าสำเร็จคืน JSON ถ้าล้มเหลวจดเวลาของ mirror แล้วรอ 5, 10, 20, 40 วินาที
บรรทัด 103: ถ้าครบทุกรอบ ยก RuntimeError
บรรทัด 106–115  เวลาเปิด-ปิด
106  def parse_hours(tags, category):
107      """อ่านเวลาเปิด-ปิดรูปแบบง่าย 'HH:MM-HH:MM' ถ้าไม่มีใช้ค่าเริ่มต้นตามหมวด"""
108      m = re.search(r'(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})', tags.get('opening_hours', ''))
109      if m:
110          o, c = int(m[1]) * 60 + int(m[2]), int(m[3]) * 60 + int(m[4])
111          if c <= o:
112              c += 1440 if c + 1440 <= 1560 else 0
113          if 0 <= o < c <= 1560:
114              return o, min(c, 1439)
115      return HOURS.get(category, (480, 1080))
บรรทัด 106–107: ประกาศ parse_hours และ docstring
บรรทัด 108: ค้นรูปแบบ HH:MM-HH:MM ใน opening_hours
บรรทัด 109–114: แปลงเป็นนาทีจากเที่ยงคืน ถ้าเวลาปิดน้อยกว่าเวลาเปิด (ปิดหลังเที่ยงคืน) ปรับ และคืนเฉพาะค่าที่สมเหตุสมผล
บรรทัด 115: ถ้าไม่มี ใช้ค่าตั้งต้นของหมวด (หรือ 08:00–18:00)
บรรทัด 118–142  คะแนนจากความสมบูรณ์ของข้อมูล
118  def quality(tags):
119      """คะแนนความสมบูรณ์/ความโดดเด่นของข้อมูลใน OSM (ค่าต่อเนื่อง 0-2.6) — ใช้แทนรีวิวจริง
120      รวมสัญญาณ: wikidata/wikipedia, เว็บไซต์, โทรศัพท์, เวลาเปิด-ปิด, รูปภาพ, มรดก/ประวัติศาสตร์,
121      ชื่ออังกฤษ/ไทย และจำนวนแท็กทั้งหมด (ยิ่งมีคนบันทึกละเอียด ยิ่งเป็นที่รู้จัก)"""
122      s = 0.0
123      if tags.get('wikidata') or tags.get('wikipedia'):
124          s += 0.8
125      if tags.get('website') or tags.get('contact:website') or tags.get('url'):
126          s += 0.3
127      if tags.get('phone') or tags.get('contact:phone'):
128          s += 0.15
129      if tags.get('opening_hours'):
130          s += 0.2
131      if tags.get('image') or tags.get('wikimedia_commons') or tags.get('mapillary'):
132          s += 0.2
133      if tags.get('heritage') or tags.get('historic'):
134          s += 0.2
135      if tags.get('description') or tags.get('description:en'):
136          s += 0.1
137      if tags.get('name:en'):
138          s += 0.1
139      if tags.get('name:th'):
140          s += 0.05
141      s += 0.04 * min(len(tags), 25)
142      return min(s, 2.6)
บรรทัด 118–121: ประกาศ quality และ docstring: ใช้ความสมบูรณ์ของข้อมูลใน OSM แทนรีวิว (ค่าต่อเนื่อง 0–2.6)
บรรทัด 122–140: บวกคะแนนจากสัญญาณ: wikidata/wikipedia (0.8) เว็บไซต์ (0.3) โทรศัพท์ (0.15) เวลาเปิด-ปิด (0.2) รูปภาพ (0.2) มรดก/ประวัติศาสตร์ (0.2) คำอธิบาย (0.1) ชื่ออังกฤษ (0.1) ชื่อไทย (0.05)
บรรทัด 141: บวก 0.04 ต่อจำนวนแท็กทั้งหมด (สูงสุด 25 แท็ก)
บรรทัด 142: จำกัดค่าสูงสุดที่ 2.6
บรรทัด 145–153  พิกัดและชื่อ
145  def coords(e):
146      return (e.get('lat') or e.get('center', {}).get('lat'),
147              e.get('lon') or e.get('center', {}).get('lon'))
148
149
150  def names(tags):
151      en = (tags.get('name:en') or tags.get('name') or '').strip()
152      th = (tags.get('name:th') or tags.get('name') or en).strip()
153      return en, th
บรรทัด 145–147: coords ดึง lat/lng จากองค์ประกอบ (จุดตรง ๆ หรือจุดศูนย์กลางของพื้นที่)
บรรทัด 150–153: names คืน (ชื่ออังกฤษ ชื่อไทย) โดยใช้ name:en name:th หรือ name ที่ถอยกลับ
บรรทัด 156–172  ประมาณราคาร้านอาหาร
156  CHEAP = ('street_food', 'noodle', 'rice', 'fast_food', 'sandwich', 'kebab', 'regional', 'local')
157  MID = ('thai', 'chinese', 'vietnamese', 'asian', 'pizza', 'burger', 'chicken', 'seafood_market')
158  PRICEY = ('seafood', 'steak', 'steak_house', 'japanese', 'sushi', 'italian', 'french', 'indian', 'german', 'fine_dining', 'mediterranean')
159
160
161  def restaurant_cost(tags, default):
162      """ประมาณราคาต่อคนจาก cuisine/amenity (OSM ไม่มีราคา) — ใช้แยกร้านถูก/กลาง/แพงให้ tier Budget มีร้านใช้"""
163      if tags.get('amenity') in ('fast_food', 'food_court'):
164          return default
165      cu = tags.get('cuisine', '').lower().replace(' ', '').split(';')
166      if any(c in PRICEY for c in cu) or tags.get('stars'):
167          return 400
168      if any(c in CHEAP for c in cu):
169          return 80
170      if any(c in MID for c in cu):
171          return 120
172      return default
บรรทัด 156–158: ชุดประเภทอาหารตามระดับราคา: ถูก กลาง แพง
บรรทัด 161–162: ประกาศ restaurant_cost และ docstring (OSM ไม่มีราคา จึงประมาณจากประเภทอาหารให้ระดับ Budget มีร้านถูก)
บรรทัด 163–164: ฟาสต์ฟู้ดและฟู้ดคอร์ตใช้ค่าตั้งต้น
บรรทัด 165–167: ประเภทแพงหรือมีดาว: 400 บาท
บรรทัด 168–169: ประเภทถูก: 80 บาท
บรรทัด 170–171: ประเภทกลาง: 120 บาท
บรรทัด 172: อื่น ๆ ใช้ค่าตั้งต้น
บรรทัด 175–197  กรองชื่อและแท็กอาหาร
175  GENERIC = {'viewpoint', 'view point', 'beach', 'market', 'temple', 'restaurant', 'wat', 'park', 'garden'}
176
177
178  def clean_name(en):
179      """คืน True ถ้าชื่อใช้ได้: อักษรไทย/ละติน/ตัวเลขเท่านั้น และไม่ใช่คำทั่วไปคำเดียว"""
180      if en.strip().lower() in GENERIC:
181          return False
182      return all(c.isascii() or '฀' <= c <= '๿' for c in en)
183
184
185  def diet_tags(tags):
186      """แท็กอาหารจาก OSM: vegetarian / vegan / halal (จาก diet:* หรือ cuisine) + ประเภทอาหาร (cuisine) — ข้อมูลใน OSM บางมาก"""
187      cuisine = [c.strip().lower() for c in tags.get('cuisine', '').replace(',', ';').split(';') if c.strip()]
188      out = []
189      def flag(key):
190          return tags.get('diet:' + key, '') in ('yes', 'only')
191      if flag('vegan') or 'vegan' in cuisine:
192          out += ['vegan', 'vegetarian']
193      elif flag('vegetarian') or 'vegetarian' in cuisine:
194          out.append('vegetarian')
195      if flag('halal') or 'halal' in cuisine or 'muslim' in cuisine:
196          out.append('halal')
197      return out + [c for c in cuisine if c not in ('vegan', 'vegetarian', 'halal', 'muslim')][:2]
บรรทัด 175: GENERIC ชื่อทั่วไปที่ไม่ใช้ (เช่น viewpoint, beach, temple)
บรรทัด 178–182: clean_name ปฏิเสธชื่อทั่วไป และชื่อที่มีอักษรนอกเหนือไทย/ละติน/ตัวเลข
บรรทัด 185–197: diet_tags สร้างแท็กอาหารจาก diet:* และ cuisine (vegan, vegetarian, halal) บวกประเภทอาหารสูงสุด 2 อย่าง ใช้กับตัวเลือกอาหารในหน้าเว็บ (ดู apply_preferences ใน ➜ apply_preferences() ใน backend/main.py)
บรรทัด 200–230  แปลงองค์ประกอบ OSM เป็นสถานที่และโรงแรม
200  def make_poi(e, category, duration, cost):
201      tags = e.get('tags', {})
202      lat, lng = coords(e)
203      en, th = names(tags)
204      if not lat or not lng or not en or not clean_name(en):
205          return None
206      if category == 'restaurant':
207          cost = restaurant_cost(tags, cost)
208      o, c = parse_hours(tags, category)
209      return {"name_th": th, "name_en": en, "category": category,
210              "lat": round(lat, 6), "lng": round(lng, 6),
211              "score": round(6.8 + quality(tags), 1), "cost": cost,
212              "duration_min": duration, "open_min": o, "close_min": c,
213              "tags": [category] + (diet_tags(tags) if category == 'restaurant' else [])}
214
215
216  def make_hotel(e, default_stars):
217      tags = e.get('tags', {})
218      lat, lng = coords(e)
219      en, th = names(tags)
220      if not lat or not lng or not en:
221          return None
222      try:
223          stars = int(float(tags.get('stars', default_stars)))
224      except ValueError:
225          stars = default_stars
226      stars = min(max(stars, 1), 5)
227      return {"name_th": th, "name_en": en, "lat": round(lat, 6), "lng": round(lng, 6),
228              "score": round(min(HOTEL_SCORE[stars] + quality(tags) * 0.25, 9.9), 1),
229              "cost": HOTEL_COST[stars], "stars": stars,
230              "_q": quality(tags) + (0.5 if tags.get('stars') else 0)}
บรรทัด 200–205: make_poi ดึงแท็ก พิกัด และชื่อ ถ้าขาดหรือชื่อไม่ผ่านการกรอง คืน None
บรรทัด 206–207: ถ้าเป็นร้านอาหาร ประมาณราคาจากประเภทอาหาร
บรรทัด 208: อ่านเวลาเปิด-ปิด
บรรทัด 209–213: คืนสถานที่: ชื่อ หมวด พิกัด คะแนน (6.8 + คะแนนความสมบูรณ์) ค่าใช้จ่าย เวลาที่ใช้ เวลาเปิดปิด และแท็ก
บรรทัด 216–221: make_hotel ดึงพิกัดและชื่อ
บรรทัด 222–226: อ่านจำนวนดาว (ถ้าอ่านไม่ได้ใช้ค่าตั้งต้น) และจำกัด 1–5
บรรทัด 227–230: คืนโรงแรม: คะแนน (ตามดาว + ส่วนเสริมจากความสมบูรณ์) ราคาต่อคืนตามดาว และ _q คะแนนไว้เลือกตัวที่ข้อมูลครบ
บรรทัด 233–265  รันคำค้นทั้งหมด
233  def collect(queries, build):
234      """รัน query ทั้งหมด กรองชื่อซ้ำ แล้วคืนรายการ; query ที่ล้มเหลว (Overpass ล่ม/timeout) จะถูกลองใหม่อีกสูงสุด 3 รอบ
235      ไม่งั้นหมวดนั้นหายเงียบ ๆ แล้วจังหวัดได้ข้อมูลน้อยกว่าความจริง"""
236      out, seen = [], set()
237      pending = list(queries)
238      for rnd in range(4):
239          failed = []
240          for q in pending:
241              flt = q[0]
242              print(f"  {flt[:60]}" + (f" (retry {rnd})" if rnd else ""))
243              try:
244                  elems = overpass(flt, BBOX).get('elements', [])
245              except Exception as ex:
246                  print(f"    ERROR: {ex}")
247                  failed.append(q)
248                  continue
249              n = 0
250              for e in elems:
251                  item = build(e, *q[1:])
252                  if item is None or item['name_en'].lower() in seen:
253                      continue
254                  seen.add(item['name_en'].lower())
255                  out.append(item)
256                  n += 1
257              print(f"    +{n}")
258              time.sleep(1)
259          pending = failed
260          if not pending:
261              break
262          time.sleep(120)   # ให้ Overpass คลายโหลดก่อนลองใหม่
263      if pending:
264          print(f"  WARNING: {len(pending)} query ล้มเหลวถาวร: {[q[0][:40] for q in pending]}")
265      return out
บรรทัด 233–235: ประกาศ collect และ docstring: รันทุกคำค้น กรองชื่อซ้ำ และลองใหม่คำค้นที่ล้มเหลว ไม่งั้นหมวดนั้นหายเงียบ ๆ และจังหวัดได้ข้อมูลน้อยกว่าจริง
บรรทัด 236–237: เตรียมผลและรายการที่รอรัน
บรรทัด 238–239: วนไม่เกิน 4 รอบ
บรรทัด 240–248: วนทีละคำค้น เรียก overpass ถ้าล้มเหลวจดไว้ลองรอบหน้า
บรรทัด 249–257: แปลงทุกองค์ประกอบเป็นรายการ ข้ามที่เป็น None หรือชื่อซ้ำ และพิมพ์จำนวนที่เพิ่ม
บรรทัด 258: รอ 1 วินาทีระหว่างคำค้น
บรรทัด 259–262: ถ้ายังเหลือคำค้นที่ล้มเหลว รอ 2 นาทีให้ Overpass คลายโหลดแล้วรอบถัดไป
บรรทัด 263–264: ถ้ายังล้มเหลวถาวร พิมพ์คำเตือน
บรรทัด 265: คืนรายการ
บรรทัด 268–285  คัดจำนวนต่อหมวด
268  def select(pois):
269      """จำกัดจำนวนต่อหมวด; ร้านอาหารเก็บ 35 อันดับคะแนนสูงสุด + ร้านราคา<=150 อีกไม่เกิน 15 (ให้ tier Budget มีมื้อ)"""
270      kept = []
271      for cat in sorted({p['category'] for p in pois}):
272          items = sorted((p for p in pois if p['category'] == cat), key=lambda p: (-p['score'], p['name_en']))
273          cap = MAX_PER_CATEGORY.get(cat, DEFAULT_MAX)
274          if cat == 'restaurant':
275              # สำรองที่ให้ร้านที่มีแท็ก vegetarian / halal อย่างละไม่เกิน 12 ร้าน (รองรับความชอบด้านอาหาร)
276              diet = []
277              for flag in ('vegetarian', 'halal'):
278                  diet += [p for p in items if flag in p.get('tags', []) and p not in diet][:12]
279              rest = [p for p in items if p not in diet]
280              top = rest[:cap - 15 - len(diet)]
281              cheap = [p for p in rest[len(top):] if p['cost'] <= 150]
282              kept += diet + top + cheap[:cap - len(diet) - len(top)]
283          else:
284              kept += items[:cap]
285      return kept
บรรทัด 268–269: ประกาศ select และ docstring
บรรทัด 270–272: วนทีละหมวด เรียงตามคะแนนสูงสุดก่อน
บรรทัด 273: เพดานจำนวนของหมวด
บรรทัด 274–282: ร้านอาหาร: สำรองร้านมังสวิรัติ/ฮาลาลอย่างละไม่เกิน 12 ร้าน เก็บร้านคะแนนสูงสุด และเติมร้านราคาไม่เกิน 150 บาทให้ระดับ Budget มีตัวเลือก
บรรทัด 283–284: หมวดอื่นเก็บตามเพดาน
บรรทัด 285: คืนรายการที่คัดแล้ว
บรรทัด 288–308  โหมด `--extra` / `--restaurants`
288  def extra(slug, restaurants_only=False):
289      """เติมหมวดเสริม + สร้างร้านอาหารใหม่ในไฟล์จังหวัดที่มีอยู่ (ไม่ดึงโรงแรม/หมวดเดิมซ้ำ)
290      restaurants_only=True: ดึงเฉพาะร้านอาหารใหม่ (พร้อมแท็ก cuisine/diet) แล้วคงหมวดอื่นไว้"""
291      global BBOX, AREA
292      _p = json.load(open(os.path.join(HERE, 'provinces.json'), encoding='utf-8'))[slug]
293      BBOX, AREA = _p['bbox'], _p.get('area')
294      path = os.path.join(HERE, 'provinces', f'{slug}.json')
295      data = json.load(open(path, encoding='utf-8'))
296      old = [p for p in data['pois'] if (p['category'] != 'restaurant' or restaurants_only) and clean_name(p['name_en'])]   # --restaurants: คงร้านเดิมไว้ ไม่ให้ลดลง
297      new = collect([q for q in EXTRA_QUERIES if not restaurants_only or q[1] == 'restaurant'], make_poi)
298      seen = {p['name_en'].lower() for p in old}
299      merged = old + [p for p in new if p['name_en'].lower() not in seen]
300      kept = select(merged)
301      for i, p in enumerate(kept, 1):
302          p['id'] = f"P{i:02d}"
303      print(f"{slug}: {len(kept)} POIs", dict(sorted(Counter(p['category'] for p in kept).items())))
304      rc = [p['cost'] for p in kept if p['category'] == 'restaurant']
305      print("  restaurants cost<=150:", sum(1 for c in rc if c <= 150), "of", len(rc))
306      with open(path, 'w', encoding='utf-8') as f:
307          json.dump({"pois": kept, "hotels": data['hotels']}, f, ensure_ascii=False, indent=2)
308      print(f"Saved {path}")
บรรทัด 288–290: ประกาศ extra และ docstring: เติมหมวดเสริมหรือสร้างร้านอาหารใหม่ในไฟล์จังหวัดที่มีอยู่ (ไม่ดึงโรงแรมใหม่)
บรรทัด 291–295: อ่าน bbox/area ของจังหวัด และโหลดไฟล์เดิม
บรรทัด 296: เก็บสถานที่เดิมที่ผ่านการกรองชื่อ (โหมดร้านอาหารเก็บร้านเดิมไว้ไม่ให้ลดลง)
บรรทัด 297: ดึงคำค้นเสริม
บรรทัด 298–300: รวมโดยตัดชื่อซ้ำ แล้วคัดจำนวนต่อหมวด
บรรทัด 301–303: ใส่ id ใหม่ P01, P02, ... และพิมพ์สรุป
บรรทัด 304–305: พิมพ์จำนวนร้านที่ราคาไม่เกิน 150 บาท
บรรทัด 306–308: เขียนไฟล์จังหวัดกลับ (โรงแรมเดิมไม่เปลี่ยน)
บรรทัด 311–342  ฟังก์ชันหลัก `main`
311  def main(slug):
312      global BBOX, AREA
313      prov = json.load(open(os.path.join(HERE, 'provinces.json'), encoding='utf-8'))[slug]
314      BBOX, AREA = prov['bbox'], prov.get('area')
315      print(f"[{slug}] bbox={BBOX}")
316      pois = collect([q for q in QUERIES if q[1] != 'restaurant'] + EXTRA_QUERIES, make_poi)
317      hotels = collect(HOTEL_QUERIES, make_hotel)
318
319      kept = select(pois)
320      # โรงแรม: ให้กระจายทุกระดับดาว ระดับละไม่เกิน HOTELS_PER_STAR (เลือกตัวที่ข้อมูลครบก่อน)
321      hsel = []
322      for s in range(1, 6):
323          items = sorted((h for h in hotels if h['stars'] == s), key=lambda h: (-h['_q'], h['name_en']))
324          hsel += items[:HOTELS_PER_STAR]
325
326      for i, p in enumerate(kept, 1):
327          p['id'] = f"P{i:02d}"
328      for i, h in enumerate(hsel, 1):
329          h['id'] = f"H{i:02d}"
330          h.pop('_q', None)
331
332      print(f"\n{slug}: {len(kept)} POIs, {len(hsel)} hotels")
333      for k, v in sorted(Counter(p['category'] for p in kept).items()):
334          print(f"  {k}: {v}")
335      print("  hotels by stars:", dict(sorted(Counter(h['stars'] for h in hsel).items())))
336      if len(kept) < 100 or len(hsel) < 15:
337          print("WARNING: ข้อมูลน้อยกว่าเกณฑ์ (POI>=100, hotels>=15) — ตรวจ/เสริมข้อมูลก่อนใช้")
338
339      out = os.path.join(HERE, 'provinces', f'{slug}.json')
340      with open(out, 'w', encoding='utf-8') as f:
341          json.dump({"pois": kept, "hotels": hsel}, f, ensure_ascii=False, indent=2)
342      print(f"Saved {out}")
บรรทัด 311–315: ประกาศ main อ่าน bbox/area ของจังหวัดจาก provinces.json และพิมพ์
บรรทัด 316–317: ดึงสถานที่ (หมวดหลักที่ไม่ใช่ร้านอาหาร และหมวดเสริมรวมร้านอาหาร) และโรงแรม
บรรทัด 319: คัดจำนวนต่อหมวด
บรรทัด 320–324: คัดโรงแรมกระจายทุกระดับดาว ระดับละไม่เกิน 6 โดยเลือกตัวที่ข้อมูลครบ
บรรทัด 326–330: ใส่ id สถานที่ P.. และโรงแรม H.. แล้วลบฟิลด์ _q
บรรทัด 332–335: พิมพ์สรุปจำนวนต่อหมวดและโรงแรมต่อดาว
บรรทัด 336–337: เตือนถ้าข้อมูลน้อยกว่าเกณฑ์ (สถานที่ 100 โรงแรม 15)
บรรทัด 339–342: เขียน data/provinces/<slug>.json
บรรทัด 345–376  เสริมร้านมังสวิรัติ/ฮาลาล (`--diet`)
345  # ร้านที่ OSM ระบุว่ามังสวิรัติ/วีแกน/ฮาลาล (ใช้เสริมจังหวัดที่ร้านอาหารไม่มีแท็กอาหาร เช่น ภูเก็ตที่คัดเอง)
346  DIET_QUERIES = [
347      ('node["amenity"~"restaurant|cafe|fast_food"]["diet:vegetarian"~"yes|only"]["name"]', 'restaurant', 60, 200),
348      ('node["amenity"~"restaurant|cafe|fast_food"]["diet:vegan"~"yes|only"]["name"]', 'restaurant', 60, 200),
349      ('node["amenity"~"restaurant|cafe|fast_food"]["cuisine"~"vegetarian|vegan"]["name"]', 'restaurant', 60, 200),
350      ('node["amenity"~"restaurant|cafe|fast_food"]["diet:halal"~"yes|only"]["name"]', 'restaurant', 60, 200),
351      ('node["amenity"~"restaurant|cafe|fast_food"]["cuisine"~"halal|muslim"]["name"]', 'restaurant', 60, 200),
352  ]
353
354
355  def diet_merge(slug):
356      """เพิ่มร้านที่มีแท็กอาหาร (vegetarian/halal) จาก OSM เข้าไฟล์จังหวัด โดยไม่แตะข้อมูลเดิม (ไม่ซ้ำชื่อ)"""
357      global BBOX, AREA
358      _p = json.load(open(os.path.join(HERE, 'provinces.json'), encoding='utf-8'))[slug]
359      BBOX, AREA = _p['bbox'], _p.get('area')
360      path = os.path.join(HERE, 'provinces', f'{slug}.json')
361      data = json.load(open(path, encoding='utf-8'))
362      new = [p for p in collect(DIET_QUERIES, make_poi) if any(t in p['tags'] for t in ('vegetarian', 'halal'))]
363      seen = {p['name_en'].lower() for p in data['pois']}
364      add = []
365      for flag in ('vegetarian', 'halal'):
366          add += [p for p in sorted(new, key=lambda p: (-p['score'], p['name_en'])) if flag in p['tags'] and p not in add][:12]
367      add = [p for p in add if p['name_en'].lower() not in seen]
368      # id ต่อจากเลขสูงสุดที่มีอยู่ (ไฟล์ภูเก็ตเดิมมี id ไม่ต่อเนื่อง — ห้ามใช้ len() เพราะจะชนกับ id เดิม)
369      n0 = max(int(''.join(ch for ch in p['id'] if ch.isdigit())) for p in data['pois'])
370      for i, p in enumerate(add, n0 + 1):
371          p['id'] = f"P{i:02d}"
372      data['pois'] += add
373      print(f"{slug}: +{len(add)} diet restaurants (vegetarian {sum('vegetarian' in p['tags'] for p in add)}, halal {sum('halal' in p['tags'] for p in add)})")
374      with open(path, 'w', encoding='utf-8') as f:
375          json.dump(data, f, ensure_ascii=False, indent=2)
376      print(f"Saved {path}")
บรรทัด 345–352: DIET_QUERIES คำค้นร้านที่ OSM ระบุว่ามังสวิรัติ วีแกน หรือฮาลาล
บรรทัด 355–356: ประกาศ diet_merge และ docstring (เพิ่มร้านที่มีแท็กอาหารเข้าไฟล์จังหวัดโดยไม่แตะข้อมูลเดิม)
บรรทัด 357–361: อ่าน bbox/area และไฟล์จังหวัด
บรรทัด 362: ดึงร้านที่มีแท็กอาหารจริง
บรรทัด 363–367: เลือกอย่างละไม่เกิน 12 ร้านตามคะแนน และตัดชื่อที่มีอยู่แล้ว
บรรทัด 368–371: ใส่ id ต่อจากเลขสูงสุดที่มี (ไม่ใช้ len() เพราะไฟล์ภูเก็ตเดิมมี id ไม่ต่อเนื่อง)
บรรทัด 372–376: เพิ่มเข้าไฟล์ พิมพ์สรุปและบันทึก
บรรทัด 379–387  จุดเริ่มต้นจากบรรทัดคำสั่ง
379  if __name__ == '__main__':
380      if len(sys.argv) not in (2, 3) or (len(sys.argv) == 3 and sys.argv[2] not in ('--extra', '--restaurants', '--diet')):
381          sys.exit("usage: python fetch_pois_osm.py <slug> [--extra | --restaurants | --diet]")
382      if len(sys.argv) == 2:
383          main(sys.argv[1])
384      elif sys.argv[2] == '--diet':
385          diet_merge(sys.argv[1])
386      else:
387          extra(sys.argv[1], restaurants_only=(sys.argv[2] == '--restaurants'))
บรรทัด 379–381: ตรวจอาร์กิวเมนต์ ถ้าผิดรูปแบบแสดงวิธีใช้
บรรทัด 382–383: ถ้ามีเฉพาะ slug เรียก main
บรรทัด 384–385: ถ้าเป็น --diet เรียก diet_merge
บรรทัด 386–387: ถ้าเป็น --extra หรือ --restaurants เรียก extra

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/utils.py
backend/main.py
data/build_all_provinces.py