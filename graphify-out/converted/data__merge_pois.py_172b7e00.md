<!-- converted from data__merge_pois.py.docx -->

คู่มือโค้ด: data/merge_pois.py
รวมข้อมูล OSM ใหม่กับข้อมูลเดิมของภูเก็ต (legacy)
ไฟล์ต้นฉบับ: data/merge_pois.py (93 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์รุ่น Project 1 ใช้เฉพาะภูเก็ต: รวมสถานที่ที่ดึงจาก OSM ใหม่กับร้านอาหาร กิจกรรม และคาเฟ่จากข้อมูลเดิม (เพราะรอบนั้น OSM ดึงร้านอาหารไม่ได้เนื่องจาก rate limit) ผลเป็น phuket_pois_merged.json ที่ต้องตรวจก่อนคัดลอกไปเป็น provinces/phuket.json จังหวัดอื่นไม่ต้องใช้ไฟล์นี้เพราะ ➜ data/fetch_pois_osm.py สร้างไฟล์จังหวัดตรง ๆ

บรรทัด 1–23  หัวไฟล์ และฟังก์ชันอ่าน/เขียนไฟล์
1  # -*- coding: utf-8 -*-
2  """
3  merge_pois.py — (legacy, เฉพาะภูเก็ต) รวม OSM data ใหม่ + ข้อมูลเดิม (restaurants + hotels)
4  จังหวัดใหม่ใช้ fetch_pois_osm.py <slug> ซึ่งสร้าง provinces/<slug>.json โดยตรง ไม่ต้อง merge
5  รัน: python merge_pois.py
6  ผลลัพธ์: phuket_pois_merged.json
7  """
8  import json
9  from collections import Counter
10
11
12  # ============================================================
13  # ฟังก์ชัน I/O
14  # ============================================================
15  def load(path):
16      """โหลดไฟล์ JSON และคืนผลเป็น dict"""
17      with open(path, 'r', encoding='utf-8') as f:
18          return json.load(f)
19
20  def save(path, data):
21      """บันทึก dict ลงไฟล์ JSON (รองรับภาษาไทย, indent=2)"""
22      with open(path, 'w', encoding='utf-8') as f:
23          json.dump(data, f, ensure_ascii=False, indent=2)
บรรทัด 1–6: docstring ระบุว่าเป็นของเก่า (legacy) สำหรับภูเก็ต และวิธีรัน
บรรทัด 8–9: นำเข้า json และ Counter
บรรทัด 15–18: load โหลดไฟล์ JSON คืน dict
บรรทัด 20–23: save เขียน dict เป็น JSON (รองรับภาษาไทย มีย่อหน้า 2 ช่อง)
บรรทัด 29–47  โหลดและแยกข้อมูล
29  # โหลดข้อมูลทั้งสอง
30  old = load('provinces/phuket.json')
31  osm = load('phuket_pois_osm.json')
32
33  old_pois   = old['pois']
34  old_hotels = old.get('hotels', [])
35  osm_pois   = osm['pois']
36
37  # เก็บร้านอาหารจากข้อมูลเดิม (OSM ดึงไม่ได้เพราะ rate limit)
38  old_restaurants = [p for p in old_pois if p['category'] == 'restaurant']
39  old_activities  = [p for p in old_pois if p['category'] == 'activity']
40  old_cafes       = [p for p in old_pois if p['category'] == 'cafe']
41
42  # OSM pois (non-restaurant)
43  osm_non_rest = [p for p in osm_pois if p['category'] != 'restaurant']
44
45  # Re-index ทุก POI ด้วย ID ที่สม่ำเสมอ
46  merged_pois = []
47  seen_names = set()
บรรทัด 29–31: โหลดข้อมูลเดิม (provinces/phuket.json) และข้อมูล OSM ใหม่
บรรทัด 33–35: แยกสถานที่เดิม โรงแรมเดิม และสถานที่จาก OSM
บรรทัด 37–40: เก็บร้านอาหาร กิจกรรม และคาเฟ่จากข้อมูลเดิม
บรรทัด 43: เลือกสถานที่จาก OSM ที่ไม่ใช่ร้านอาหาร
บรรทัด 46–47: เตรียมรายการผลรวมและชุดชื่อที่เห็นแล้ว (กันซ้ำ)
บรรทัด 53–76  รวมข้อมูลและกำหนด id ใหม่
53  def add_pois(pois_list, id_prefix):
54      """เพิ่ม POI เข้า merged_pois โดยกรองซ้ำด้วย name_en"""
55      for p in pois_list:
56          key = p['name_en'].lower().strip()
57          if key in seen_names or not key:
58              continue
59          seen_names.add(key)
60          merged_pois.append(p)
61
62  # ลำดับความสำคัญ: OSM non-restaurant ก่อน (ข้อมูลใหม่กว่า ครบกว่า)
63  add_pois(osm_non_rest, 'OSM')
64
65  # เติม activity จากเดิมที่ OSM ไม่ค่อยมี
66  add_pois(old_activities, 'ACT')
67
68  # เติม cafe จากเดิม
69  add_pois(old_cafes, 'CAFE')
70
71  # เติมร้านอาหารจากเดิม (OSM timeout)
72  add_pois(old_restaurants, 'REST')
73
74  # กำหนด ID ใหม่ให้เรียงลำดับ
75  for i, p in enumerate(merged_pois):
76      p['id'] = f"P{i+1:02d}"
บรรทัด 53–60: add_pois เพิ่มจุดเข้าผลรวมโดยกรองซ้ำด้วยชื่ออังกฤษตัวพิมพ์เล็ก (ข้ามชื่อว่าง)
บรรทัด 62–63: ลำดับความสำคัญแรก: จุดจาก OSM ที่ไม่ใช่ร้านอาหาร (ใหม่และครบกว่า)
บรรทัด 65–72: เติมกิจกรรม คาเฟ่ และร้านอาหารจากข้อมูลเดิมตามลำดับ
บรรทัด 74–76: กำหนด id ใหม่ให้เรียงลำดับ รูปแบบ P01, P02, ...
บรรทัด 82–93  สรุปและบันทึก
82  # สรุป
83  cats = Counter(p['category'] for p in merged_pois)
84  print(f"Merged POIs: {len(merged_pois)} total")
85  for cat, n in sorted(cats.items()):
86      print(f"  {cat}: {n}")
87  print(f"Hotels: {len(old_hotels)}")
88
89  # บันทึก
90  result = {"pois": merged_pois, "hotels": old_hotels}
91  save('phuket_pois_merged.json', result)
92  print(f"\nSaved to phuket_pois_merged.json")
93  print("ตรวจสอบแล้วถ้าโอเค: copy phuket_pois_merged.json → provinces/phuket.json")
บรรทัด 82–87: นับจำนวนสถานที่ตามหมวดและพิมพ์พร้อมจำนวนโรงแรม
บรรทัด 90–92: เขียน phuket_pois_merged.json
บรรทัด 93: เตือนให้ตรวจแล้วคัดลอกเป็น provinces/phuket.json

ไฟล์ที่เชื่อมกับไฟล์นี้
data/fetch_pois_osm.py