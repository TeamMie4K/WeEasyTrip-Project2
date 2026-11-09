# -*- coding: utf-8 -*-
"""
build_all_provinces.py — สร้างข้อมูลจังหวัดที่เหลือจาก 77 จังหวัดทีละจังหวัด (ต่อจากจุดที่ค้างได้)

ขั้นตอนต่อจังหวัด (ข้ามจังหวัดที่มีไฟล์ provinces/<slug>.json แล้ว):
  1) หาจุดศูนย์กลางตัวเมืองด้วย Nominatim (อำเภอเมือง...; สำรองด้วยชื่ออังกฤษ) แล้วกำหนด bbox รอบจุดนั้น ±0.2 องศา (~44 กม.)
  2) ดึง POI + โรงแรมจาก OpenStreetMap (fetch_pois_osm.main) + ร้านมังสวิรัติ/ฮาลาล (--diet) + เติมชื่ออังกฤษ (apply_names)
  3) ปรับเทียบเวลาเดินทางด้วย OSRM (calibrate_travel)
  4) ลงทะเบียนใน provinces.json (backend/หน้าเว็บอ่านไฟล์นี้) — จังหวัดที่ข้อมูลไม่พอ (POI<60 หรือโรงแรม<10) จะไม่ลงทะเบียน
การดึงข้อมูลแต่ละจังหวัดใช้ราว 1 ชั่วโมงเพราะ Overpass ฟรีคิวยาว → รันทิ้งไว้ได้ (`python build_all_provinces.py [จำนวนจังหวัด]`)
สถานะอยู่ที่ provinces_status.json
"""
import json, os, sys, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_pois_osm as F
import calibrate_travel as C
from thai_provinces import PROVINCES_77, PRIORITY

STATUS = os.path.join(HERE, 'provinces_status.json')
REG = os.path.join(HERE, 'provinces.json')
STRICT, RELAXED = (60, 10), (20, 2)   # (POI, โรงแรม) ขั้นต่ำ: เกณฑ์ปกติ / เกณฑ์ผ่อนผันสำหรับจังหวัดเล็ก-ชนบท
HUBS = {'bangkok', 'chonburi', 'chiangmai', 'phuket', 'krabi', 'ayutthaya', 'kanchanaburi', 'phangnga',
        'prachuapkhirikhan', 'chiangrai', 'suratthani', 'nakhonratchasima', 'khonkaen', 'songkhla', 'phetchaburi'}   # เมืองท่องเที่ยวหลักต้องผ่านเกณฑ์ปกติ ถ้าไม่ผ่านแปลว่าดึงข้อมูลพลาด ต้องดึงใหม่
HALF = 0.2   # องศา (~22 กม.) ครึ่งหนึ่งของด้านกล่อง


def load(p, default):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default


def geocode(th, en):
    """จุดศูนย์กลางตัวเมือง: ลอง 'อำเภอเมือง<จังหวัด>' ก่อน แล้ว '<English> city' (Nominatim: 1 request/วินาที)"""
    for q in (f'อำเภอเมือง{th}, {th}, ประเทศไทย', f'{en}, Thailand'):
        url = 'https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + urllib.parse.quote(q)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ThesisProject/1.0 (thai-tourism-research)'})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read())
            time.sleep(1.2)
            if d:
                return float(d[0]['lat']), float(d[0]['lon'])
        except Exception as e:
            print('  geocode error', e, flush=True)
    return None


def verdict(slug, n_p, n_h):
    """ready = ผ่านเกณฑ์ปกติ; sparse = จังหวัดเล็ก/ชนบทที่ผ่านเกณฑ์ผ่อนผัน (ใช้ข้อมูลเท่าที่หาได้ทั้งหมด); insufficient = ไม่ผ่าน"""
    if n_p >= STRICT[0] and n_h >= STRICT[1]:
        return 'ready'
    if slug not in HUBS and n_p >= RELAXED[0] and n_h >= RELAXED[1]:
        return 'sparse'
    return 'insufficient'


def build(slug, th, en, region, status):
    reg = load(REG, {})
    t0 = time.time()
    c = geocode(th, en)
    if not c:
        status[slug] = {'state': 'failed', 'reason': 'geocode'}
        return
    lat, lng = c
    reg[slug] = {'name_th': th, 'name_en': en, 'bbox': [round(lat - HALF, 4), round(lng - HALF, 4), round(lat + HALF, 4), round(lng + HALF, 4)],
                 'center': [round(lat, 4), round(lng, 4)], 'zoom': 11, 'region': region, 'auto': True, 'area': th}
    # ใช้ทะเบียนชั่วคราวระหว่างดึง แต่ยังไม่ให้ backend เห็นจนกว่าจะผ่านเกณฑ์ (เก็บแยกในตัวแปรนี้)
    tmp = dict(load(REG, {}))
    tmp[slug] = reg[slug]
    json.dump(tmp, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    try:
        F.main(slug)
        F.diet_merge(slug)
        import apply_names
    except Exception as e:
        status[slug] = {'state': 'failed', 'reason': str(e)[:200]}
        tmp.pop(slug, None)
        json.dump(tmp, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        return
    data = json.load(open(os.path.join(HERE, 'provinces', f'{slug}.json'), encoding='utf-8'))
    n_p, n_h = len(data['pois']), len(data['hotels'])
    v = verdict(slug, n_p, n_h)
    if v == 'insufficient':
        status[slug] = {'state': 'insufficient', 'pois': n_p, 'hotels': n_h}
        tmp.pop(slug, None)
        json.dump(tmp, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        return
    try:
        C.main([slug])    # เติม road_factor/speed_kmh ลง provinces.json
    except Exception as e:
        print('  calibrate failed:', e, flush=True)
    status[slug] = {'state': 'ready', 'pois': n_p, 'hotels': n_h, 'minutes': round((time.time() - t0) / 60, 1)}
    if v == 'sparse':
        status[slug]['sparse'] = True


def reeval(status, info):
    """ตรวจจังหวัด insufficient เดิมด้วยเกณฑ์ปัจจุบันจากไฟล์ที่มีอยู่ (ไม่ดึงข้อมูลใหม่) แล้วลงทะเบียนตัวที่ผ่าน"""
    for slug, st in list(status.items()):
        f = os.path.join(HERE, 'provinces', f'{slug}.json')
        if st.get('state') != 'insufficient' or slug not in info or not os.path.exists(f):
            continue
        data = json.load(open(f, encoding='utf-8'))
        n_p, n_h = len(data['pois']), len(data['hotels'])
        if verdict(slug, n_p, n_h) == 'insufficient':
            continue
        _, th, en, region = info[slug]
        c = geocode(th, en)
        if not c:
            continue
        lat, lng = c
        reg = load(REG, {})
        reg[slug] = {'name_th': th, 'name_en': en, 'bbox': [round(lat - HALF, 4), round(lng - HALF, 4), round(lat + HALF, 4), round(lng + HALF, 4)],
                     'center': [round(lat, 4), round(lng, 4)], 'zoom': 11, 'region': region, 'auto': True, 'area': th}
        json.dump(reg, open(REG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        try:
            C.main([slug])
        except Exception as e:
            print('  calibrate failed:', e, flush=True)
        status[slug] = {'state': 'ready', 'pois': n_p, 'hotels': n_h, 'sparse': True}
        json.dump(status, open(STATUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print('  re-evaluated ->', slug, status[slug], flush=True)


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    status = load(STATUS, {})
    info = {p[0]: p for p in PROVINCES_77}
    reeval(status, info)
    order = [s for s in PRIORITY if s in info] + [p[0] for p in PROVINCES_77 if p[0] not in PRIORITY]
    todo = [s for s in order if not os.path.exists(os.path.join(HERE, 'provinces', f'{s}.json'))
            and status.get(s, {}).get('state') not in ('ready', 'insufficient')]
    for slug in todo[:limit]:
        _, th, en, region = info[slug]
        print(f'== {slug} ({th}) ==', flush=True)
        build(slug, th, en, region, status)
        json.dump(status, open(STATUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print('  ->', status[slug], flush=True)


if __name__ == '__main__':
    main()
