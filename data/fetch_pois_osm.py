# -*- coding: utf-8 -*-
"""
fetch_pois_osm.py — ดึง POI + โรงแรมของจังหวัดจาก OpenStreetMap (Overpass API) ฟรี ไม่ต้อง API key
รัน:  python fetch_pois_osm.py <slug>        เช่น  python fetch_pois_osm.py chiangmai
อ่านขอบเขต (bbox) จาก provinces.json และเขียน provinces/<slug>.json (schema เดียวกับ phuket.json)

ข้อจำกัดของข้อมูล OSM (ต้องระบุในรายงาน):
  - score ประเมินจาก heuristic (มี wikidata/website ฯลฯ) ไม่ใช่รีวิวจริง
  - ราคาโรงแรมประมาณจากจำนวนดาว (OSM ไม่มีราคา); ค่าเข้าสถานที่ใช้ค่าเริ่มต้นตามหมวด
"""
import json, os, re, sys, time, urllib.request, urllib.parse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

# (osm_filter, category, duration_min, cost)
QUERIES = [
    ('node["amenity"="place_of_worship"]["religion"="buddhist"]["name"]', 'temple', 60, 0),
    ('way["amenity"="place_of_worship"]["religion"="buddhist"]["name"]',  'temple', 60, 0),
    ('node["natural"="beach"]["name"]', 'beach', 90, 0),
    ('way["natural"="beach"]["name"]',  'beach', 90, 0),
    ('node["tourism"="viewpoint"]["name"]', 'viewpoint', 40, 0),
    ('node["tourism"="museum"]["name"]',    'culture', 60, 100),
    ('node["historic"="monument"]["name"]', 'culture', 40, 0),
    ('node["amenity"="marketplace"]["name"]', 'market', 60, 0),
    ('way["amenity"="marketplace"]["name"]',  'market', 60, 0),
    ('node["leisure"="water_park"]["name"]',  'activity', 180, 800),
    ('node["tourism"="theme_park"]["name"]',  'activity', 180, 500),
    ('node["tourism"="zoo"]["name"]',         'activity', 150, 400),
    ('node["tourism"="attraction"]["name"]',  'culture', 45, 0),
    ('node["amenity"="restaurant"]["name"]',  'restaurant', 60, 200),
]
# หมวดเสริม (กิจกรรม/ธรรมชาติ/สปา) และร้านอาหารหลายระดับราคา — ใช้กับ --extra
EXTRA_QUERIES = [
    ('node["natural"="waterfall"]["name"]', 'viewpoint', 60, 0),
    ('way["boundary"="national_park"]["name"]', 'activity', 180, 200),
    ('rel["boundary"="national_park"]["name"]', 'activity', 180, 200),
    ('node["leisure"="nature_reserve"]["name"]', 'activity', 120, 100),
    ('way["leisure"="nature_reserve"]["name"]', 'activity', 120, 100),
    ('node["shop"="massage"]["name"]', 'activity', 90, 300),
    ('node["leisure"="spa"]["name"]', 'activity', 90, 400),
    ('node["amenity"="dive_centre"]["name"]', 'activity', 240, 1500),
    ('node["amenity"="cooking_school"]["name"]', 'activity', 180, 900),
    ('node["sport"="climbing"]["name"]', 'activity', 120, 500),
    ('node["leisure"="garden"]["name"]', 'culture', 45, 50),
    ('node["tourism"="gallery"]["name"]', 'culture', 45, 100),
    ('node["amenity"="restaurant"]["name"]', 'restaurant', 60, 200),
    ('node["amenity"="fast_food"]["name"]', 'restaurant', 40, 80),
    ('node["amenity"="food_court"]["name"]', 'restaurant', 50, 100),
    # ชนบท: ร้านมักถูกแมปเป็นอาคาร (way) หรือเป็นร้านกาแฟ — เพิ่มเพื่อให้จังหวัดข้อมูลน้อยมีร้านพอ
    ('way["amenity"="restaurant"]["name"]', 'restaurant', 60, 200),
    ('node["amenity"="cafe"]["name"]', 'restaurant', 45, 100),
    ('way["amenity"="cafe"]["name"]', 'restaurant', 45, 100),
    ('way["amenity"="fast_food"]["name"]', 'restaurant', 40, 80),
]
HOTEL_QUERIES = [
    ('node["tourism"="hotel"]["name"]',       3),
    ('way["tourism"="hotel"]["name"]',        3),
    ('node["tourism"="resort"]["name"]',      4),
    ('node["tourism"="guest_house"]["name"]', 2),
    ('node["tourism"="hostel"]["name"]',      1),
]
MAX_PER_CATEGORY = {'restaurant': 50}   # หมวดอื่นเก็บสูงสุด 40
DEFAULT_MAX = 40
HOURS = {'restaurant': (660, 1320), 'market': (1020, 1380), 'beach': (360, 1320)}
HOTEL_COST = {1: 450, 2: 600, 3: 1100, 4: 2200, 5: 5000}
HOTEL_SCORE = {1: 7.0, 2: 7.4, 3: 7.8, 4: 8.4, 5: 9.1}
HOTELS_PER_STAR = 6


AREA = None   # ชื่อจังหวัด (ไทย) ที่ใช้ค้นตามเขต; None = ใช้ bbox
_BAD = {}   # url -> เวลาที่ล้มเหลวล่าสุด: ข้าม mirror ที่เพิ่งล้มเหลวเป็นเวลา 10 นาที ลดเวลารอเมื่อ mirror ไหนล่ม


def overpass(filter_str, bbox):
    """ส่ง query พร้อม fallback หลาย mirror (จำ mirror ที่ล่มชั่วคราว) และ retry แบบ exponential backoff"""
    if AREA:   # จำกัดตามเส้นเขตจังหวัดจริง (admin_level=4) แทนกรอบสี่เหลี่ยม ไม่ให้ปนกับจังหวัดข้างเคียง
        body = (f'area["boundary"="administrative"]["admin_level"="4"]["name"~"{AREA}"]->.a;'
                f'({filter_str}(area.a););')
    else:
        body = f"({filter_str}({','.join(map(str, bbox))}););"
    q = 'data=' + urllib.parse.quote(f"[out:json][timeout:180];{body}out center 400;")
    last = None
    for attempt in range(4):
        now = time.time()
        urls = [u for u in ENDPOINTS if now - _BAD.get(u, 0) > 600] or list(ENDPOINTS)
        for url in urls:
            try:
                req = urllib.request.Request(url, data=q.encode(), headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "ThesisProject/1.0 (thai-tourism-research)"})
                with urllib.request.urlopen(req, timeout=200) as r:
                    return json.loads(r.read())
            except Exception as e:
                last = e
                _BAD[url] = time.time()
        time.sleep(5 * 2 ** attempt)
    raise RuntimeError(f"Overpass failed: {last}")


def parse_hours(tags, category):
    """อ่านเวลาเปิด-ปิดรูปแบบง่าย 'HH:MM-HH:MM' ถ้าไม่มีใช้ค่าเริ่มต้นตามหมวด"""
    m = re.search(r'(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})', tags.get('opening_hours', ''))
    if m:
        o, c = int(m[1]) * 60 + int(m[2]), int(m[3]) * 60 + int(m[4])
        if c <= o:
            c += 1440 if c + 1440 <= 1560 else 0
        if 0 <= o < c <= 1560:
            return o, min(c, 1439)
    return HOURS.get(category, (480, 1080))


def quality(tags):
    """คะแนนความสมบูรณ์/ความโดดเด่นของข้อมูลใน OSM (ค่าต่อเนื่อง 0-2.6) — ใช้แทนรีวิวจริง
    รวมสัญญาณ: wikidata/wikipedia, เว็บไซต์, โทรศัพท์, เวลาเปิด-ปิด, รูปภาพ, มรดก/ประวัติศาสตร์,
    ชื่ออังกฤษ/ไทย และจำนวนแท็กทั้งหมด (ยิ่งมีคนบันทึกละเอียด ยิ่งเป็นที่รู้จัก)"""
    s = 0.0
    if tags.get('wikidata') or tags.get('wikipedia'):
        s += 0.8
    if tags.get('website') or tags.get('contact:website') or tags.get('url'):
        s += 0.3
    if tags.get('phone') or tags.get('contact:phone'):
        s += 0.15
    if tags.get('opening_hours'):
        s += 0.2
    if tags.get('image') or tags.get('wikimedia_commons') or tags.get('mapillary'):
        s += 0.2
    if tags.get('heritage') or tags.get('historic'):
        s += 0.2
    if tags.get('description') or tags.get('description:en'):
        s += 0.1
    if tags.get('name:en'):
        s += 0.1
    if tags.get('name:th'):
        s += 0.05
    s += 0.04 * min(len(tags), 25)
    return min(s, 2.6)


def coords(e):
    return (e.get('lat') or e.get('center', {}).get('lat'),
            e.get('lon') or e.get('center', {}).get('lon'))


def names(tags):
    en = (tags.get('name:en') or tags.get('name') or '').strip()
    th = (tags.get('name:th') or tags.get('name') or en).strip()
    return en, th


CHEAP = ('street_food', 'noodle', 'rice', 'fast_food', 'sandwich', 'kebab', 'regional', 'local')
MID = ('thai', 'chinese', 'vietnamese', 'asian', 'pizza', 'burger', 'chicken', 'seafood_market')
PRICEY = ('seafood', 'steak', 'steak_house', 'japanese', 'sushi', 'italian', 'french', 'indian', 'german', 'fine_dining', 'mediterranean')


def restaurant_cost(tags, default):
    """ประมาณราคาต่อคนจาก cuisine/amenity (OSM ไม่มีราคา) — ใช้แยกร้านถูก/กลาง/แพงให้ tier Budget มีร้านใช้"""
    if tags.get('amenity') in ('fast_food', 'food_court'):
        return default
    cu = tags.get('cuisine', '').lower().replace(' ', '').split(';')
    if any(c in PRICEY for c in cu) or tags.get('stars'):
        return 400
    if any(c in CHEAP for c in cu):
        return 80
    if any(c in MID for c in cu):
        return 120
    return default


GENERIC = {'viewpoint', 'view point', 'beach', 'market', 'temple', 'restaurant', 'wat', 'park', 'garden'}


def clean_name(en):
    """คืน True ถ้าชื่อใช้ได้: อักษรไทย/ละติน/ตัวเลขเท่านั้น และไม่ใช่คำทั่วไปคำเดียว"""
    if en.strip().lower() in GENERIC:
        return False
    return all(c.isascii() or '฀' <= c <= '๿' for c in en)


def diet_tags(tags):
    """แท็กอาหารจาก OSM: vegetarian / vegan / halal (จาก diet:* หรือ cuisine) + ประเภทอาหาร (cuisine) — ข้อมูลใน OSM บางมาก"""
    cuisine = [c.strip().lower() for c in tags.get('cuisine', '').replace(',', ';').split(';') if c.strip()]
    out = []
    def flag(key):
        return tags.get('diet:' + key, '') in ('yes', 'only')
    if flag('vegan') or 'vegan' in cuisine:
        out += ['vegan', 'vegetarian']
    elif flag('vegetarian') or 'vegetarian' in cuisine:
        out.append('vegetarian')
    if flag('halal') or 'halal' in cuisine or 'muslim' in cuisine:
        out.append('halal')
    return out + [c for c in cuisine if c not in ('vegan', 'vegetarian', 'halal', 'muslim')][:2]


def make_poi(e, category, duration, cost):
    tags = e.get('tags', {})
    lat, lng = coords(e)
    en, th = names(tags)
    if not lat or not lng or not en or not clean_name(en):
        return None
    if category == 'restaurant':
        cost = restaurant_cost(tags, cost)
    o, c = parse_hours(tags, category)
    return {"name_th": th, "name_en": en, "category": category,
            "lat": round(lat, 6), "lng": round(lng, 6),
            "score": round(6.8 + quality(tags), 1), "cost": cost,
            "duration_min": duration, "open_min": o, "close_min": c,
            "tags": [category] + (diet_tags(tags) if category == 'restaurant' else [])}


def make_hotel(e, default_stars):
    tags = e.get('tags', {})
    lat, lng = coords(e)
    en, th = names(tags)
    if not lat or not lng or not en:
        return None
    try:
        stars = int(float(tags.get('stars', default_stars)))
    except ValueError:
        stars = default_stars
    stars = min(max(stars, 1), 5)
    return {"name_th": th, "name_en": en, "lat": round(lat, 6), "lng": round(lng, 6),
            "score": round(min(HOTEL_SCORE[stars] + quality(tags) * 0.25, 9.9), 1),
            "cost": HOTEL_COST[stars], "stars": stars,
            "_q": quality(tags) + (0.5 if tags.get('stars') else 0)}


def collect(queries, build):
    """รัน query ทั้งหมด กรองชื่อซ้ำ แล้วคืนรายการ; query ที่ล้มเหลว (Overpass ล่ม/timeout) จะถูกลองใหม่อีกสูงสุด 3 รอบ
    ไม่งั้นหมวดนั้นหายเงียบ ๆ แล้วจังหวัดได้ข้อมูลน้อยกว่าความจริง"""
    out, seen = [], set()
    pending = list(queries)
    for rnd in range(4):
        failed = []
        for q in pending:
            flt = q[0]
            print(f"  {flt[:60]}" + (f" (retry {rnd})" if rnd else ""))
            try:
                elems = overpass(flt, BBOX).get('elements', [])
            except Exception as ex:
                print(f"    ERROR: {ex}")
                failed.append(q)
                continue
            n = 0
            for e in elems:
                item = build(e, *q[1:])
                if item is None or item['name_en'].lower() in seen:
                    continue
                seen.add(item['name_en'].lower())
                out.append(item)
                n += 1
            print(f"    +{n}")
            time.sleep(1)
        pending = failed
        if not pending:
            break
        time.sleep(120)   # ให้ Overpass คลายโหลดก่อนลองใหม่
    if pending:
        print(f"  WARNING: {len(pending)} query ล้มเหลวถาวร: {[q[0][:40] for q in pending]}")
    return out


def select(pois):
    """จำกัดจำนวนต่อหมวด; ร้านอาหารเก็บ 35 อันดับคะแนนสูงสุด + ร้านราคา<=150 อีกไม่เกิน 15 (ให้ tier Budget มีมื้อ)"""
    kept = []
    for cat in sorted({p['category'] for p in pois}):
        items = sorted((p for p in pois if p['category'] == cat), key=lambda p: (-p['score'], p['name_en']))
        cap = MAX_PER_CATEGORY.get(cat, DEFAULT_MAX)
        if cat == 'restaurant':
            # สำรองที่ให้ร้านที่มีแท็ก vegetarian / halal อย่างละไม่เกิน 12 ร้าน (รองรับความชอบด้านอาหาร)
            diet = []
            for flag in ('vegetarian', 'halal'):
                diet += [p for p in items if flag in p.get('tags', []) and p not in diet][:12]
            rest = [p for p in items if p not in diet]
            top = rest[:cap - 15 - len(diet)]
            cheap = [p for p in rest[len(top):] if p['cost'] <= 150]
            kept += diet + top + cheap[:cap - len(diet) - len(top)]
        else:
            kept += items[:cap]
    return kept


def extra(slug, restaurants_only=False):
    """เติมหมวดเสริม + สร้างร้านอาหารใหม่ในไฟล์จังหวัดที่มีอยู่ (ไม่ดึงโรงแรม/หมวดเดิมซ้ำ)
    restaurants_only=True: ดึงเฉพาะร้านอาหารใหม่ (พร้อมแท็ก cuisine/diet) แล้วคงหมวดอื่นไว้"""
    global BBOX, AREA
    _p = json.load(open(os.path.join(HERE, 'provinces.json'), encoding='utf-8'))[slug]
    BBOX, AREA = _p['bbox'], _p.get('area')
    path = os.path.join(HERE, 'provinces', f'{slug}.json')
    data = json.load(open(path, encoding='utf-8'))
    old = [p for p in data['pois'] if (p['category'] != 'restaurant' or restaurants_only) and clean_name(p['name_en'])]   # --restaurants: คงร้านเดิมไว้ ไม่ให้ลดลง
    new = collect([q for q in EXTRA_QUERIES if not restaurants_only or q[1] == 'restaurant'], make_poi)
    seen = {p['name_en'].lower() for p in old}
    merged = old + [p for p in new if p['name_en'].lower() not in seen]
    kept = select(merged)
    for i, p in enumerate(kept, 1):
        p['id'] = f"P{i:02d}"
    print(f"{slug}: {len(kept)} POIs", dict(sorted(Counter(p['category'] for p in kept).items())))
    rc = [p['cost'] for p in kept if p['category'] == 'restaurant']
    print("  restaurants cost<=150:", sum(1 for c in rc if c <= 150), "of", len(rc))
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({"pois": kept, "hotels": data['hotels']}, f, ensure_ascii=False, indent=2)
    print(f"Saved {path}")


def main(slug):
    global BBOX, AREA
    prov = json.load(open(os.path.join(HERE, 'provinces.json'), encoding='utf-8'))[slug]
    BBOX, AREA = prov['bbox'], prov.get('area')
    print(f"[{slug}] bbox={BBOX}")
    pois = collect([q for q in QUERIES if q[1] != 'restaurant'] + EXTRA_QUERIES, make_poi)
    hotels = collect(HOTEL_QUERIES, make_hotel)

    kept = select(pois)
    # โรงแรม: ให้กระจายทุกระดับดาว ระดับละไม่เกิน HOTELS_PER_STAR (เลือกตัวที่ข้อมูลครบก่อน)
    hsel = []
    for s in range(1, 6):
        items = sorted((h for h in hotels if h['stars'] == s), key=lambda h: (-h['_q'], h['name_en']))
        hsel += items[:HOTELS_PER_STAR]

    for i, p in enumerate(kept, 1):
        p['id'] = f"P{i:02d}"
    for i, h in enumerate(hsel, 1):
        h['id'] = f"H{i:02d}"
        h.pop('_q', None)

    print(f"\n{slug}: {len(kept)} POIs, {len(hsel)} hotels")
    for k, v in sorted(Counter(p['category'] for p in kept).items()):
        print(f"  {k}: {v}")
    print("  hotels by stars:", dict(sorted(Counter(h['stars'] for h in hsel).items())))
    if len(kept) < 100 or len(hsel) < 15:
        print("WARNING: ข้อมูลน้อยกว่าเกณฑ์ (POI>=100, hotels>=15) — ตรวจ/เสริมข้อมูลก่อนใช้")

    out = os.path.join(HERE, 'provinces', f'{slug}.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump({"pois": kept, "hotels": hsel}, f, ensure_ascii=False, indent=2)
    print(f"Saved {out}")


# ร้านที่ OSM ระบุว่ามังสวิรัติ/วีแกน/ฮาลาล (ใช้เสริมจังหวัดที่ร้านอาหารไม่มีแท็กอาหาร เช่น ภูเก็ตที่คัดเอง)
DIET_QUERIES = [
    ('node["amenity"~"restaurant|cafe|fast_food"]["diet:vegetarian"~"yes|only"]["name"]', 'restaurant', 60, 200),
    ('node["amenity"~"restaurant|cafe|fast_food"]["diet:vegan"~"yes|only"]["name"]', 'restaurant', 60, 200),
    ('node["amenity"~"restaurant|cafe|fast_food"]["cuisine"~"vegetarian|vegan"]["name"]', 'restaurant', 60, 200),
    ('node["amenity"~"restaurant|cafe|fast_food"]["diet:halal"~"yes|only"]["name"]', 'restaurant', 60, 200),
    ('node["amenity"~"restaurant|cafe|fast_food"]["cuisine"~"halal|muslim"]["name"]', 'restaurant', 60, 200),
]


def diet_merge(slug):
    """เพิ่มร้านที่มีแท็กอาหาร (vegetarian/halal) จาก OSM เข้าไฟล์จังหวัด โดยไม่แตะข้อมูลเดิม (ไม่ซ้ำชื่อ)"""
    global BBOX, AREA
    _p = json.load(open(os.path.join(HERE, 'provinces.json'), encoding='utf-8'))[slug]
    BBOX, AREA = _p['bbox'], _p.get('area')
    path = os.path.join(HERE, 'provinces', f'{slug}.json')
    data = json.load(open(path, encoding='utf-8'))
    new = [p for p in collect(DIET_QUERIES, make_poi) if any(t in p['tags'] for t in ('vegetarian', 'halal'))]
    seen = {p['name_en'].lower() for p in data['pois']}
    add = []
    for flag in ('vegetarian', 'halal'):
        add += [p for p in sorted(new, key=lambda p: (-p['score'], p['name_en'])) if flag in p['tags'] and p not in add][:12]
    add = [p for p in add if p['name_en'].lower() not in seen]
    # id ต่อจากเลขสูงสุดที่มีอยู่ (ไฟล์ภูเก็ตเดิมมี id ไม่ต่อเนื่อง — ห้ามใช้ len() เพราะจะชนกับ id เดิม)
    n0 = max(int(''.join(ch for ch in p['id'] if ch.isdigit())) for p in data['pois'])
    for i, p in enumerate(add, n0 + 1):
        p['id'] = f"P{i:02d}"
    data['pois'] += add
    print(f"{slug}: +{len(add)} diet restaurants (vegetarian {sum('vegetarian' in p['tags'] for p in add)}, halal {sum('halal' in p['tags'] for p in add)})")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {path}")


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3) or (len(sys.argv) == 3 and sys.argv[2] not in ('--extra', '--restaurants', '--diet')):
        sys.exit("usage: python fetch_pois_osm.py <slug> [--extra | --restaurants | --diet]")
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif sys.argv[2] == '--diet':
        diet_merge(sys.argv[1])
    else:
        extra(sys.argv[1], restaurants_only=(sys.argv[2] == '--restaurants'))
