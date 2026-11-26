<!-- converted from data__calibrate_travel.py.docx -->

คู่มือโค้ด: data/calibrate_travel.py
ปรับเทียบระยะ/เวลาเดินทางรายจังหวัดด้วย OSRM
ไฟล์ต้นฉบับ: data/calibrate_travel.py (68 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์ออฟไลน์ที่ทำให้เวลาเดินทางในแผนสมจริงขึ้น สุ่มคู่สถานที่ในแต่ละจังหวัด ถามเส้นทางขับรถจริงจากบริการ OSRM แล้วคำนวณ "ตัวคูณระยะถนน" และ "ความเร็วเฉลี่ย" บันทึกกลับใน data/provinces.json ค่าเหล่านี้ถูกอ่านโดย ➜ get_province() ใน backend/main.py แล้วส่งให้ ➜ set_travel_profile() ใน algorithm/utils.py ใช้คำนวณระยะและเวลาเดินทางทุกอัลกอริทึม

บรรทัด 1–14  หัวไฟล์ ค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  calibrate_travel.py — ปรับเทียบระยะ/เวลาเดินทางรายจังหวัดด้วย OSRM (ถนนจริง)
4  สุ่มคู่ POI/โรงแรมในจังหวัด 40 คู่ (seed คงที่) เรียก OSRM แล้วคำนวณ
5    road_factor = Σ ระยะถนน / Σ ระยะเส้นตรง (haversine)
6    speed_kmh   = Σ ระยะถนน / Σ เวลาขับ (free-flow ตาม speed limit — ไม่รวมการจราจร)
7  บันทึกกลับใน provinces.json (ใช้โดย algorithm/utils.py)
8  รัน:  python calibrate_travel.py [slug ...]
9  """
10  import json, math, os, random, sys, time, urllib.request
11
12  HERE = os.path.dirname(os.path.abspath(__file__))
13  OSRM = "https://router.project-osrm.org/route/v1/driving/{},{};{},{}?overview=false"
14  PAIRS = 40
บรรทัด 1–9: docstring: สุ่มคู่ POI/โรงแรม 40 คู่ (seed คงที่) เรียก OSRM คำนวณ road_factor = Σ ระยะถนน ÷ Σ ระยะเส้นตรง และ speed_kmh = Σ ระยะถนน ÷ Σ เวลาขับ (แบบรถไม่ติด) วิธีรัน python calibrate_travel.py [slug ...]
บรรทัด 10: นำเข้าโมดูลมาตรฐานสำหรับ JSON คณิตศาสตร์ ไฟล์ สุ่ม และเรียก HTTP
บรรทัด 12: HERE โฟลเดอร์ของสคริปต์ (คือ data/)
บรรทัด 13: OSRM แม่แบบ URL ของบริการเส้นทางสาธารณะ (ขับรถ ไม่ขอรูปเส้นทาง)
บรรทัด 14: PAIRS = 40 จำนวนคู่ที่สุ่มต่อจังหวัด
บรรทัด 17–22  ระยะเส้นตรง
17  def hav(a, b):
18      R = 6371.0
19      p1, p2 = math.radians(a['lat']), math.radians(b['lat'])
20      dl = math.radians(b['lng'] - a['lng'])
21      h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
22      return 2 * R * math.asin(math.sqrt(h))
บรรทัด 17–22: hav สูตร Haversine เหมือน ➜ haversine_km() ใน algorithm/utils.py แต่ไม่คูณตัวคูณถนน (ใช้เป็นตัวหารของ road_factor)
บรรทัด 25–38  เรียก OSRM
25  def route(a, b):
26      url = OSRM.format(a['lng'], a['lat'], b['lng'], b['lat'])
27      for attempt in range(4):
28          try:
29              req = urllib.request.Request(url, headers={"User-Agent": "ThesisProject/1.0 (travel-calibration)"})
30              with urllib.request.urlopen(req, timeout=30) as r:
31                  d = json.loads(r.read())
32              if d.get('code') == 'Ok':
33                  leg = d['routes'][0]
34                  return leg['distance'] / 1000.0, leg['duration'] / 3600.0
35              return None
36          except Exception:
37              time.sleep(2 ** attempt)
38      return None
บรรทัด 25–26: ประกาศ route และประกอบ URL จากพิกัดสองจุด (OSRM รับ ลองจิจูด,ละติจูด)
บรรทัด 27: ลองได้ 4 ครั้ง
บรรทัด 28–31: ส่งคำขอพร้อมชื่อ User-Agent ที่ระบุตัวสคริปต์ และอ่านผล JSON (timeout 30 วินาที)
บรรทัด 32–34: ถ้าตอบ Ok คืน (ระยะกิโลเมตร, เวลาชั่วโมง)
บรรทัด 35: ถ้าหาเส้นทางไม่ได้ คืน None
บรรทัด 36–37: ถ้าเกิดข้อผิดพลาด (เครือข่าย) รอแบบเพิ่มเป็นทวีคูณแล้วลองใหม่
บรรทัด 38: ครบ 4 ครั้งยังไม่สำเร็จ คืน None
บรรทัด 41–64  ฟังก์ชันหลัก
41  def main(slugs):
42      path = os.path.join(HERE, 'provinces.json')
43      cfg = json.load(open(path, encoding='utf-8'))
44      for slug in slugs:
45          d = json.load(open(os.path.join(HERE, 'provinces', f'{slug}.json'), encoding='utf-8'))
46          pts = d['pois'] + d['hotels']
47          rng = random.Random(42)
48          road = hv_sum = hours = 0.0
49          n = 0
50          while n < PAIRS:
51              a, b = rng.sample(pts, 2)
52              h = hav(a, b)
53              if h < 1.0:
54                  continue
55              r = route(a, b)
56              time.sleep(0.4)
57              if r is None:
58                  continue
59              road += r[0]; hours += r[1]; hv_sum += h; n += 1
60          cfg[slug]['road_factor'] = round(road / hv_sum, 2)
61          cfg[slug]['speed_kmh'] = round(road / hours, 1)
62          cfg[slug]['calibration'] = {'source': 'OSRM public demo (car, free-flow)', 'pairs': n}
63          print(slug, 'road_factor', cfg[slug]['road_factor'], 'speed_kmh', cfg[slug]['speed_kmh'], flush=True)
64      json.dump(cfg, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
บรรทัด 41–43: ประกาศ main โหลด provinces.json เป็น cfg
บรรทัด 44–46: วนทีละจังหวัด โหลดไฟล์ข้อมูลจังหวัด รวมจุดและโรงแรมเป็นจุดสุ่ม
บรรทัด 47–49: ตัวสุ่มที่ตั้ง seed 42 (ผลซ้ำได้) และตัวสะสมระยะถนน ระยะเส้นตรง และชั่วโมง
บรรทัด 50–52: วนจนได้ครบ 40 คู่: สุ่มสองจุดและคำนวณระยะเส้นตรง
บรรทัด 53–54: ข้ามคู่ที่ใกล้กันกว่า 1 กม.
บรรทัด 55–58: เรียก OSRM รอ 0.4 วินาทีกันถูกจำกัดอัตรา ถ้าไม่ได้ผลลองคู่ใหม่
บรรทัด 59: สะสมผล
บรรทัด 60–61: คำนวณ road_factor และ speed_kmh ปัดเศษและเขียนลงค่าของจังหวัดนั้น
บรรทัด 62: บันทึกที่มาของค่า (OSRM สาธารณะ แบบ free-flow) และจำนวนคู่
บรรทัด 63: พิมพ์ผล
บรรทัด 64: เขียน provinces.json กลับ
บรรทัด 67–68  จุดเริ่มต้น
67  if __name__ == '__main__':
68      main(sys.argv[1:] or ['phuket', 'chiangmai', 'krabi', 'samui'])
บรรทัด 67–68: เมื่อรันตรง ๆ ใช้ slug จากอาร์กิวเมนต์ ถ้าไม่ระบุทำ 4 จังหวัดหลัก (ภูเก็ต เชียงใหม่ กระบี่ เกาะสมุย)

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/utils.py
backend/main.py