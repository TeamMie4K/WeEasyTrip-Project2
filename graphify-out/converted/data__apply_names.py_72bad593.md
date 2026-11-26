<!-- converted from data__apply_names.py.docx -->

คู่มือโค้ด: data/apply_names.py
เติมชื่ออังกฤษให้สถานที่ที่ OSM มีแต่ชื่อไทย
ไฟล์ต้นฉบับ: data/apply_names.py (25 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์หลังท่อสร้างข้อมูล (➜ data/fetch_pois_osm.py และ ➜ data/build_all_provinces.py) ที่เติม name_en ให้ POI และโรงแรมซึ่ง OpenStreetMap มีแต่ชื่อไทย โดยค้นจากตารางแปล data/name_translations.json (แปลโดย AI และยังตรวจโดยคนไม่ครบ) รายการที่ยังไม่มีคำแปลจะบันทึกไว้ใน data/_missing_names.json

บรรทัด 1–25  ทั้งไฟล์
1  # -*- coding: utf-8 -*-
2  """
3  apply_names.py — เติมชื่ออังกฤษ (name_en) ให้ POI/โรงแรมที่ OSM มีแต่ชื่อไทย
4  อ่านตาราง name_translations.json {ชื่อไทย: ชื่ออังกฤษ} (แปลโดย AI ตรวจโดยคนไม่ได้ครบ — ระบุเป็นข้อจำกัดในรายงาน)
5  รัน:  python apply_names.py            # ทุกจังหวัด; พิมพ์รายการที่ยังไม่มีคำแปล
6  """
7  import json, glob, os, re
8  HERE = os.path.dirname(os.path.abspath(__file__))
9  TR = json.load(open(os.path.join(HERE, 'name_translations.json'), encoding='utf-8'))
10  is_thai = lambda s: re.search('[\u0e00-\u0e7f]', s) is not None
11  missing = {}
12  for path in sorted(glob.glob(os.path.join(HERE, 'provinces', '*.json'))):
13      d = json.load(open(path, encoding='utf-8'))
14      n = 0
15      for p in d['pois'] + d['hotels']:
16          if is_thai(p['name_en']):
17              en = TR.get(p['name_th']) or TR.get(p['name_en'])
18              if en:
19                  p['name_en'] = en
20                  n += 1
21              else:
22                  missing.setdefault(os.path.basename(path), []).append(p['name_th'])
23      json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
24      print(os.path.basename(path), 'translated', n, 'missing', len(missing.get(os.path.basename(path), [])))
25  json.dump(missing, open(os.path.join(HERE, '_missing_names.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
บรรทัด 1–6: docstring อธิบายหน้าที่และวิธีรัน (รันครั้งเดียวกับทุกจังหวัด และพิมพ์รายการที่ยังขาดคำแปล)
บรรทัด 7: นำเข้า json glob os re
บรรทัด 8: HERE โฟลเดอร์ data/
บรรทัด 9: โหลดตารางแปล {ชื่อไทย: ชื่ออังกฤษ}
บรรทัด 10: is_thai ตรวจว่าข้อความมีอักษรไทย (ช่วงยูนิโค้ด 0E00–0E7F)
บรรทัด 11: missing เก็บรายการที่ยังไม่มีคำแปลแยกตามไฟล์จังหวัด
บรรทัด 12: วนทุกไฟล์ data/provinces/*.json
บรรทัด 13–14: โหลดข้อมูลจังหวัดและตั้งตัวนับคำแปลที่ใส่ได้
บรรทัด 15: วนทั้งสถานที่และโรงแรม
บรรทัด 16: ถ้า name_en ยังเป็นภาษาไทย (OSM ไม่มีชื่ออังกฤษ)
บรรทัด 17: หาคำแปลจากชื่อไทยก่อน ถ้าไม่มีลองจากชื่อใน name_en
บรรทัด 18–20: ถ้ามีคำแปล ใส่แทนและนับ
บรรทัด 21–22: ถ้าไม่มี จดไว้ในรายการที่ขาด
บรรทัด 23: เขียนไฟล์จังหวัดกลับ (รองรับภาษาไทย)
บรรทัด 24: พิมพ์จำนวนที่แปลได้และที่ยังขาดของไฟล์นั้น
บรรทัด 25: เขียนรายการที่ยังขาดทั้งหมดลง data/_missing_names.json

ไฟล์ที่เชื่อมกับไฟล์นี้
data/build_all_provinces.py
data/fetch_pois_osm.py