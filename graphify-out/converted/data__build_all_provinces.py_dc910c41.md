<!-- converted from data__build_all_provinces.py.docx -->

คู่มือโค้ด: data/build_all_provinces.py
ท่อสร้างข้อมูลทุกจังหวัดอัตโนมัติ (77 จังหวัด)
ไฟล์ต้นฉบับ: data/build_all_provinces.py (142 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์ควบคุมท่อสร้างข้อมูลจังหวัดที่เหลือทีละจังหวัด สำหรับแต่ละจังหวัด: หาจุดศูนย์กลางด้วย Nominatim ดึงสถานที่และโรงแรมจาก OpenStreetMap ด้วย ➜ data/fetch_pois_osm.py เติมชื่ออังกฤษด้วย ➜ data/apply_names.py ปรับเทียบเวลาเดินทางด้วย ➜ data/calibrate_travel.py แล้วลงทะเบียนใน data/provinces.json ซึ่ง ➜ backend/main.py อ่านเป็นรายการจังหวัด และบันทึกสถานะลง provinces_status.json (ready, sparse, insufficient, failed) ใช้รายชื่อจาก ➜ data/thai_provinces.py

บรรทัด 1–25  หัวไฟล์ นำเข้า และเกณฑ์
1  # -*- coding: utf-8 -*-
2  """
3  build_all_provinces.py — สร้างข้อมูลจังหวัดที่เหลือจาก 77 จังหวัดทีละจังหวัด (ต่อจากจุดที่ค้างได้)
4
5  ขั้นตอนต่อจังหวัด (ข้ามจังหวัดที่มีไฟล์ provinces/<slug>.json แล้ว):
6    1) หาจุดศูนย์กลางตัวเมืองด้วย Nominatim (อำเภอเมือง...; สำรองด้วยชื่ออังกฤษ) แล้วกำหนด bbox รอบจุดนั้น ±0.2 องศา (~44 กม.)
7    2) ดึง POI + โรงแรมจาก OpenStreetMap (fetch_pois_osm.main) + ร้านมังสวิรัติ/ฮาลาล (--diet) + เติมชื่ออังกฤษ (apply_names)
8    3) ปรับเทียบเวลาเดินทางด้วย OSRM (calibrate_travel)
9    4) ลงทะเบียนใน provinces.json (backend/หน้าเว็บอ่านไฟล์นี้) — จังหวัดที่ข้อมูลไม่พอ (POI<60 หรือโรงแรม<10) จะไม่ลงทะเบียน
10  การดึงข้อมูลแต่ละจังหวัดใช้ราว 1 ชั่วโมงเพราะ Overpass ฟรีคิวยาว → รันทิ้งไว้ได้ (`python build_all_provinces.py [จำนวนจังหวัด]`)
11  สถานะอยู่ที่ provinces_status.json
12  """
13  import json, os, sys, time, urllib.parse, urllib.request
14  HERE = os.path.dirname(os.path.abspath(__file__))
15  sys.path.insert(0, HERE)
16  import fetch_pois_osm as F
17  import calibrate_travel as C
18  from thai_provinces import PROVINCES_77, PRIORITY
19
20  STATUS = os.path.join(HERE, 'provinces_status.json')
21  REG = os.path.join(HERE, 'provinces.json')
22  STRICT, RELAXED = (60, 10), (20, 2)   # (POI, โรงแรม) ขั้นต่ำ: เกณฑ์ปกติ / เกณฑ์ผ่อนผันสำหรับจังหวัดเล็ก-ชนบท
23  HUBS = {'bangkok', 'chonburi', 'chiangmai', 'phuket', 'krabi', 'ayutthaya', 'kanchanaburi', 'phangnga',
24          'prachuapkhirikhan', 'chiangrai', 'suratthani', 'nakhonratchasima', 'khonkaen', 'songkhla', 'phetchaburi'}   # เมืองท่องเที่ยวหลักต้องผ่านเกณฑ์ปกติ ถ้าไม่ผ่านแปลว่าดึงข้อมูลพลาด ต้องดึงใหม่
25  HALF = 0.2   # องศา (~22 กม.) ครึ่งหนึ่งของด้านกล่อง
บรรทัด 1–12: docstring อธิบายสี่ขั้นตอนต่อจังหวัด ว่าข้ามจังหวัดที่มีไฟล์แล้ว ใช้เวลาราว 1 ชั่วโมงต่อจังหวัดเพราะ Overpass ฟรีมีคิวยาว และสถานะอยู่ที่ provinces_status.json
บรรทัด 13–15: นำเข้าโมดูลมาตรฐานและเพิ่มโฟลเดอร์นี้เข้า path
บรรทัด 16–18: นำเข้า ➜ data/fetch_pois_osm.py (ชื่อ F) ➜ data/calibrate_travel.py (ชื่อ C) และ PROVINCES_77 PRIORITY จาก ➜ data/thai_provinces.py
บรรทัด 20–21: พาธไฟล์สถานะและทะเบียนจังหวัด
บรรทัด 22: STRICT, RELAXED เกณฑ์ขั้นต่ำ (สถานที่, โรงแรม): เกณฑ์ปกติ 60/10 และเกณฑ์ผ่อนผัน 20/2 สำหรับจังหวัดเล็กหรือชนบท
บรรทัด 23–24: HUBS เมืองท่องเที่ยวหลักที่ต้องผ่านเกณฑ์ปกติเท่านั้น
บรรทัด 25: HALF = 0.2 ครึ่งหนึ่งของด้านกล่องค้นหา (ราว 22 กม.)
บรรทัด 28–29  อ่านไฟล์ JSON
28  def load(p, default):
29      return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default
บรรทัด 28–29: load อ่าน JSON ถ้ามีไฟล์ ไม่มีคืนค่าตั้งต้น
บรรทัด 32–45  หาจุดศูนย์กลางจังหวัด
32  def geocode(th, en):
33      """จุดศูนย์กลางตัวเมือง: ลอง 'อำเภอเมือง<จังหวัด>' ก่อน แล้ว '<English> city' (Nominatim: 1 request/วินาที)"""
34      for q in (f'อำเภอเมือง{th}, {th}, ประเทศไทย', f'{en}, Thailand'):
35          url = 'https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + urllib.parse.quote(q)
36          try:
37              req = urllib.request.Request(url, headers={'User-Agent': 'ThesisProject/1.0 (thai-tourism-research)'})
38              with urllib.request.urlopen(req, timeout=30) as r:
39                  d = json.loads(r.read())
40              time.sleep(1.2)
41              if d:
42                  return float(d[0]['lat']), float(d[0]['lon'])
43          except Exception as e:
44              print('  geocode error', e, flush=True)
45      return None
บรรทัด 32–33: ประกาศ geocode และ docstring (ลอง "อำเภอเมือง…" ก่อน แล้ว "<ชื่ออังกฤษ>, Thailand" Nominatim จำกัด 1 คำขอต่อวินาที)
บรรทัด 34: วนสองคำค้น
บรรทัด 35–37: ประกอบ URL และคำขอพร้อมชื่อ User-Agent ที่ระบุตัวสคริปต์
บรรทัด 38–39: ส่งคำขอและอ่านผล
บรรทัด 40: รอ 1.2 วินาทีตามกติกาบริการ
บรรทัด 41–42: ถ้ามีผล คืน (ละติจูด ลองจิจูด)
บรรทัด 43–44: ถ้าผิดพลาด พิมพ์ข้อความแล้วลองคำค้นถัดไป
บรรทัด 45: ไม่พบ คืน None
บรรทัด 48–54  ตัดสินว่าข้อมูลพอหรือไม่
48  def verdict(slug, n_p, n_h):
49      """ready = ผ่านเกณฑ์ปกติ; sparse = จังหวัดเล็ก/ชนบทที่ผ่านเกณฑ์ผ่อนผัน (ใช้ข้อมูลเท่าที่หาได้ทั้งหมด); insufficient = ไม่ผ่าน"""
50      if n_p >= STRICT[0] and n_h >= STRICT[1]:
51          return 'ready'
52      if slug not in HUBS and n_p >= RELAXED[0] and n_h >= RELAXED[1]:
53          return 'sparse'
54      return 'insufficient'
บรรทัด 48–49: ประกาศ verdict และ docstring (ready / sparse / insufficient)
บรรทัด 50–51: ถ้าผ่านเกณฑ์ปกติ คืน ready
บรรทัด 52–53: ถ้าไม่ใช่เมืองหลักและผ่านเกณฑ์ผ่อนผัน คืน sparse (ใช้ข้อมูลเท่าที่หาได้ หน้าเว็บแสดงป้าย "ข้อมูลน้อย")
บรรทัด 54: นอกนั้น insufficient
บรรทัด 57–94  สร้างข้อมูลหนึ่งจังหวัด
57  def build(slug, th, en, region, status):
58      reg = load(REG, {})
59      t0 = time.time()
60      c = geocode(th, en)
61      if not c:
62          status[slug] = {'state': 'failed', 'reason': 'geocode'}
63          return
64      lat, lng = c
65      reg[slug] = {'name_th': th, 'name_en': en, 'bbox': [round(lat - HALF, 4), round(lng - HALF, 4), round(lat + HALF, 4), round(lng + HALF, 4)],
66                   'center': [round(lat, 4), round(lng, 4)], 'zoom': 11, 'region': region, 'auto': True, 'area': th}
67      # ใช้ทะเบียนชั่วคราวระหว่างดึง แต่ยังไม่ให้ backend เห็นจนกว่าจะผ่านเกณฑ์ (เก็บแยกในตัวแปรนี้)
68      tmp = dict(load(REG, {}))
69      tmp[slug] = reg[slug]
70      json.dump(tmp, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
71      try:
72          F.main(slug)
73          F.diet_merge(slug)
74          import apply_names
75      except Exception as e:
76          status[slug] = {'state': 'failed', 'reason': str(e)[:200]}
77          tmp.pop(slug, None)
78          json.dump(tmp, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
79          return
80      data = json.load(open(os.path.join(HERE, 'provinces', f'{slug}.json'), encoding='utf-8'))
81      n_p, n_h = len(data['pois']), len(data['hotels'])
82      v = verdict(slug, n_p, n_h)
83      if v == 'insufficient':
84          status[slug] = {'state': 'insufficient', 'pois': n_p, 'hotels': n_h}
85          tmp.pop(slug, None)
86          json.dump(tmp, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
87          return
88      try:
89          C.main([slug])    # เติม road_factor/speed_kmh ลง provinces.json
90      except Exception as e:
91          print('  calibrate failed:', e, flush=True)
92      status[slug] = {'state': 'ready', 'pois': n_p, 'hotels': n_h, 'minutes': round((time.time() - t0) / 60, 1)}
93      if v == 'sparse':
94          status[slug]['sparse'] = True
บรรทัด 57–63: ประกาศ build โหลดทะเบียน หาจุดศูนย์กลาง ถ้าหาไม่ได้บันทึกสถานะ failed (เหตุ geocode)
บรรทัด 64–66: สร้างรายการทะเบียนของจังหวัด: ชื่อ กล่องค้นหา (bbox) จุดศูนย์กลาง ระดับซูม ภาค และธงสร้างอัตโนมัติ
บรรทัด 67–70: เขียนทะเบียนชั่วคราวเพื่อให้ตัวดึงข้อมูลอ่านได้ (ยังไม่ให้ backend เห็นจนกว่าจะผ่านเกณฑ์)
บรรทัด 71–73: ดึงข้อมูลด้วย F.main เพิ่มร้านมังสวิรัติ/ฮาลาลด้วย F.diet_merge และเติมชื่ออังกฤษโดยนำเข้า ➜ data/apply_names.py (สคริปต์ทำงานตอนนำเข้า)
บรรทัด 75–79: ถ้าล้มเหลว บันทึกสถานะ failed พร้อมเหตุ และถอนจังหวัดออกจากทะเบียน
บรรทัด 80–82: โหลดไฟล์ที่ได้ นับสถานที่และโรงแรม และตัดสินด้วย verdict
บรรทัด 83–87: ถ้าข้อมูลไม่พอ บันทึก insufficient และถอนออกจากทะเบียน
บรรทัด 88–91: ปรับเทียบเวลาเดินทางด้วย ➜ data/calibrate_travel.py (เติม road_factor และ speed_kmh) ถ้าล้มเหลวพิมพ์เตือน
บรรทัด 92–94: บันทึกสถานะ ready พร้อมจำนวน เวลาที่ใช้ และธง sparse ถ้าเป็นเกณฑ์ผ่อนผัน
บรรทัด 97–122  ตรวจจังหวัดที่เคยไม่พอด้วยเกณฑ์ปัจจุบัน
97  def reeval(status, info):
98      """ตรวจจังหวัด insufficient เดิมด้วยเกณฑ์ปัจจุบันจากไฟล์ที่มีอยู่ (ไม่ดึงข้อมูลใหม่) แล้วลงทะเบียนตัวที่ผ่าน"""
99      for slug, st in list(status.items()):
100          f = os.path.join(HERE, 'provinces', f'{slug}.json')
101          if st.get('state') != 'insufficient' or slug not in info or not os.path.exists(f):
102              continue
103          data = json.load(open(f, encoding='utf-8'))
104          n_p, n_h = len(data['pois']), len(data['hotels'])
105          if verdict(slug, n_p, n_h) == 'insufficient':
106              continue
107          _, th, en, region = info[slug]
108          c = geocode(th, en)
109          if not c:
110              continue
111          lat, lng = c
112          reg = load(REG, {})
113          reg[slug] = {'name_th': th, 'name_en': en, 'bbox': [round(lat - HALF, 4), round(lng - HALF, 4), round(lat + HALF, 4), round(lng + HALF, 4)],
114                       'center': [round(lat, 4), round(lng, 4)], 'zoom': 11, 'region': region, 'auto': True, 'area': th}
115          json.dump(reg, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
116          try:
117              C.main([slug])
118          except Exception as e:
119              print('  calibrate failed:', e, flush=True)
120          status[slug] = {'state': 'ready', 'pois': n_p, 'hotels': n_h, 'sparse': True}
121          json.dump(status, open(STATUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
122          print('  re-evaluated ->', slug, status[slug], flush=True)
บรรทัด 97–98: ประกาศ reeval ตรวจจังหวัดที่เคยเป็น insufficient ใหม่ด้วยเกณฑ์ปัจจุบันจากไฟล์เดิม (ไม่ดึงข้อมูลใหม่)
บรรทัด 99–102: วนสถานะ ข้ามที่ไม่ใช่ insufficient ไม่มีข้อมูล หรือไม่มีไฟล์
บรรทัด 103–106: อ่านไฟล์ นับ ถ้ายังไม่พอ ข้าม
บรรทัด 107–111: หาจุดศูนย์กลางใหม่ ถ้าไม่ได้ ข้าม
บรรทัด 112–115: ลงทะเบียนใน provinces.json
บรรทัด 116–119: ปรับเทียบเวลาเดินทาง
บรรทัด 120–122: บันทึกสถานะ ready แบบ sparse และพิมพ์ผล
บรรทัด 125–138  ฟังก์ชันหลัก
125  def main():
126      limit = int(sys.argv[1]) if len(sys.argv) > 1 else 3
127      status = load(STATUS, {})
128      info = {p[0]: p for p in PROVINCES_77}
129      reeval(status, info)
130      order = [s for s in PRIORITY if s in info] + [p[0] for p in PROVINCES_77 if p[0] not in PRIORITY]
131      todo = [s for s in order if not os.path.exists(os.path.join(HERE, 'provinces', f'{s}.json'))
132              and status.get(s, {}).get('state') not in ('ready', 'insufficient')]
133      for slug in todo[:limit]:
134          _, th, en, region = info[slug]
135          print(f'== {slug} ({th}) ==', flush=True)
136          build(slug, th, en, region, status)
137          json.dump(status, open(STATUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
138          print('  ->', status[slug], flush=True)
บรรทัด 125–129: ประกาศ main อ่านจำนวนจังหวัดที่จะทำต่อรอบ (ตั้งต้น 3) โหลดสถานะ และตรวจจังหวัดเก่าด้วย reeval
บรรทัด 130: เรียงลำดับ: จังหวัดในรายการ PRIORITY ก่อน แล้วที่เหลือ
บรรทัด 131–132: เลือกเฉพาะจังหวัดที่ยังไม่มีไฟล์และสถานะยังไม่ใช่ ready หรือ insufficient
บรรทัด 133–138: ทำทีละจังหวัดตามจำนวนที่กำหนด พิมพ์ชื่อ เรียก build บันทึกสถานะลงไฟล์ทุกครั้ง
บรรทัด 141–142  จุดเริ่มต้น
141  if __name__ == '__main__':
142      main()
บรรทัด 141–142: เรียก main() เมื่อรันไฟล์ตรง ๆ

ไฟล์ที่เชื่อมกับไฟล์นี้
backend/main.py
data/apply_names.py
data/calibrate_travel.py
data/fetch_pois_osm.py
data/thai_provinces.py