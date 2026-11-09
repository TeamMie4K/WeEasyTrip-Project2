# -*- coding: utf-8 -*-
"""
apply_names.py — เติมชื่ออังกฤษ (name_en) ให้ POI/โรงแรมที่ OSM มีแต่ชื่อไทย
อ่านตาราง name_translations.json {ชื่อไทย: ชื่ออังกฤษ} (แปลโดย AI ตรวจโดยคนไม่ได้ครบ — ระบุเป็นข้อจำกัดในรายงาน)
รัน:  python apply_names.py            # ทุกจังหวัด; พิมพ์รายการที่ยังไม่มีคำแปล
"""
import json, glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
TR = json.load(open(os.path.join(HERE, 'name_translations.json'), encoding='utf-8'))
is_thai = lambda s: re.search('[\u0e00-\u0e7f]', s) is not None
missing = {}
for path in sorted(glob.glob(os.path.join(HERE, 'provinces', '*.json'))):
    d = json.load(open(path, encoding='utf-8'))
    n = 0
    for p in d['pois'] + d['hotels']:
        if is_thai(p['name_en']):
            en = TR.get(p['name_th']) or TR.get(p['name_en'])
            if en:
                p['name_en'] = en
                n += 1
            else:
                missing.setdefault(os.path.basename(path), []).append(p['name_th'])
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(os.path.basename(path), 'translated', n, 'missing', len(missing.get(os.path.basename(path), [])))
json.dump(missing, open(os.path.join(HERE, '_missing_names.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
