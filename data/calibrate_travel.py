# -*- coding: utf-8 -*-
"""
calibrate_travel.py — ปรับเทียบระยะ/เวลาเดินทางรายจังหวัดด้วย OSRM (ถนนจริง)
สุ่มคู่ POI/โรงแรมในจังหวัด 40 คู่ (seed คงที่) เรียก OSRM แล้วคำนวณ
  road_factor = Σ ระยะถนน / Σ ระยะเส้นตรง (haversine)
  speed_kmh   = Σ ระยะถนน / Σ เวลาขับ (free-flow ตาม speed limit — ไม่รวมการจราจร)
บันทึกกลับใน provinces.json (ใช้โดย algorithm/utils.py)
รัน:  python calibrate_travel.py [slug ...]
"""
import json, math, os, random, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OSRM = "https://router.project-osrm.org/route/v1/driving/{},{};{},{}?overview=false"
PAIRS = 40


def hav(a, b):
    R = 6371.0
    p1, p2 = math.radians(a['lat']), math.radians(b['lat'])
    dl = math.radians(b['lng'] - a['lng'])
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def route(a, b):
    url = OSRM.format(a['lng'], a['lat'], b['lng'], b['lat'])
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ThesisProject/1.0 (travel-calibration)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read())
            if d.get('code') == 'Ok':
                leg = d['routes'][0]
                return leg['distance'] / 1000.0, leg['duration'] / 3600.0
            return None
        except Exception:
            time.sleep(2 ** attempt)
    return None


def main(slugs):
    path = os.path.join(HERE, 'provinces.json')
    cfg = json.load(open(path, encoding='utf-8'))
    for slug in slugs:
        d = json.load(open(os.path.join(HERE, 'provinces', f'{slug}.json'), encoding='utf-8'))
        pts = d['pois'] + d['hotels']
        rng = random.Random(42)
        road = hv_sum = hours = 0.0
        n = 0
        while n < PAIRS:
            a, b = rng.sample(pts, 2)
            h = hav(a, b)
            if h < 1.0:
                continue
            r = route(a, b)
            time.sleep(0.4)
            if r is None:
                continue
            road += r[0]; hours += r[1]; hv_sum += h; n += 1
        cfg[slug]['road_factor'] = round(road / hv_sum, 2)
        cfg[slug]['speed_kmh'] = round(road / hours, 1)
        cfg[slug]['calibration'] = {'source': 'OSRM public demo (car, free-flow)', 'pairs': n}
        print(slug, 'road_factor', cfg[slug]['road_factor'], 'speed_kmh', cfg[slug]['speed_kmh'], flush=True)
    json.dump(cfg, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main(sys.argv[1:] or ['phuket', 'chiangmai', 'krabi', 'samui'])
