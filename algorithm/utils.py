# -*- coding: utf-8 -*-
"""
utils.py - Helper functions for distance, time, cost, and route evaluation

Provides:
  - load_data:     โหลด POI + hotel จาก JSON
  - haversine_km:  คำนวณระยะทาง
  - evaluate_route: ตรวจสอบ constraint ทั้งหมดของ routes
  - print_result:  แสดงผลสรุป
"""
import json
import math
from contextvars import ContextVar
from typing import Dict, List, Tuple

# ============================================================
# ค่าคงที่
# ============================================================
AVG_SPEED_KMH = 40
COST_PER_KM = 10
DAY_TIME_BUDGET = 840       # 14 hours (8:00 - 22:00)
DAY_START_MIN = 480         # 8:00

# โปรไฟล์การเดินทางรายจังหวัด: (road_factor, speed_kmh) — ปรับเทียบจาก OSRM ใน data/calibrate_travel.py
# ใช้ ContextVar เพื่อให้ API ที่ประมวลผลหลาย request พร้อมกันไม่ปนกัน; ค่าเริ่มต้นคือแบบเดิม (เส้นตรง, 40 km/h)
# กติกาความสมจริงของวัน: ช่วงเวลาเริ่มมื้อ (นาทีจากเที่ยงคืน), เวลาเที่ยวต่อวันไม่เกิน MAX_SIGHT_MIN
LUNCH_WIN = (660, 870)      # 11:00-14:30
DINNER_WIN = (1020, 1200)   # 17:00-20:00
MEAL_SPLIT = 930            # ร้านที่ถึงก่อน 15:30 นับเป็นมื้อกลางวัน ไม่งั้นมื้อเย็น
MAX_SIGHT_MIN = 480         # เวลาท่องเที่ยว (ไม่รวมมื้อ/เดินทาง) สูงสุดต่อวัน 8 ชม.
TIME_WEIGHT = 0.01         # คะแนนที่หักต่อนาทีของเวลาทั้งวัน (ให้แผน 6 จุดใช้เวลาคุ้มขึ้น) — ปรับด้วยการทดลอง
MAX_ATTRS = 4              # สถานที่เที่ยวสูงสุดต่อวัน (+ มื้ออาหาร 2 = 6 จุด/วัน ตรงกับ Project 1: attr-attr-lunch-attr-attr-dinner)
MORNING_SPAN = 190          # นาทีที่ใช้ได้ก่อนมื้อกลางวัน (08:00 -> ~11:10)


def split_attrs(attrs: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """แบ่ง attraction เป็นช่วงเช้า/บ่าย/ค่ำ: จุดที่เปิดหลัง 17:00 (โชว์, ตลาดกลางคืน) ไปหลังมื้อเย็น
    ที่เหลือแบ่งเช้า/บ่ายตามเวลาที่ใช้จริง (ประมาณ: duration + 25 นาทีเดินทางต่อจุด)"""
    evening = [p for p in attrs if p['open_min'] >= 1020]
    day = [p for p in attrs if p['open_min'] < 1020]
    t, k = 0, 0
    while k < len(day) and t < MORNING_SPAN:
        t += day[k]['duration_min'] + 25
        k += 1
    return day[:k], day[k:], evening


_PROFILE: ContextVar = ContextVar('travel_profile', default=(1.0, AVG_SPEED_KMH))


def set_travel_profile(road_factor: float = 1.0, speed_kmh: float = AVG_SPEED_KMH) -> None:
    """ตั้งค่าตัวคูณระยะทางถนน/เส้นตรง และความเร็วเฉลี่ย สำหรับ context ปัจจุบัน"""
    _PROFILE.set((float(road_factor), float(speed_kmh)))



# ============================================================
# โหลด / บันทึกข้อมูล
# ============================================================
def load_data(path: str) -> Tuple[List[Dict], List[Dict]]:
    """โหลด POI และโรงแรมจากไฟล์ JSON"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['pois'], data['hotels']



# ============================================================
# ระยะทาง / เวลาเดินทาง / ค่าใช้จ่าย
# ============================================================
def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """ระยะทางระหว่างสองพิกัด (km): Haversine (เส้นตรง) × road_factor ของจังหวัด = ประมาณระยะทางถนน"""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c * _PROFILE.get()[0]


# เวลาเดินทางสมจริงขึ้น: ความเร็วที่ปรับเทียบด้วย OSRM เป็นแบบรถไม่ติด (free-flow) ไม่รวมการจราจรและเวลาหาที่จอด/เดินเข้าจุด
# จึงคูณตัวคูณการจราจร (TRAFFIC_FACTOR) และบวกเวลาเผื่อต่อการย้ายจุดที่ไกลกว่า 0.3 กม. (TRANSFER_BUFFER_MIN) — สองค่านี้เป็นสมมติฐาน ไม่ได้วัดจริง
TRAFFIC_FACTOR = 1.25
TRANSFER_BUFFER_MIN = 10.0
BUFFER_MIN_KM = 0.3


def travel_time_min(dist_km: float) -> float:
    """เวลาเดินทางเป็นนาที = ระยะทาง/ความเร็วเฉลี่ยตามโปรไฟล์จังหวัด × ตัวคูณการจราจร + เวลาเผื่อจอด/เดิน (ถ้าย้ายไกลกว่า 0.3 กม.)"""
    t = (dist_km / _PROFILE.get()[1]) * 60.0 * TRAFFIC_FACTOR
    return t + (TRANSFER_BUFFER_MIN if dist_km >= BUFFER_MIN_KM else 0.0)


def travel_cost(dist_km: float) -> float:
    """ค่าเดินทางเป็นบาท จากระยะทาง km (อัตรา 10 บาท/km)"""
    return dist_km * COST_PER_KM



# ============================================================
# ประเมิน route
# ============================================================
def evaluate_route(routes_per_day: List[List[Dict]], hotel: Dict,
                   budget: float, day_time: float = DAY_TIME_BUDGET) -> Dict:
    """ประเมินคุณภาพ routes พร้อมตรวจสอบ constraint ทั้งหมด (งบ / เวลา / เวลาปิด)"""
    total_score = 0.0
    total_cost = 0.0
    days_detail = []
    violations = []

    for day_idx, day_pois in enumerate(routes_per_day):
        day_dist = 0.0
        day_cost_local = 0.0
        day_score_local = 0.0
        current_time = float(DAY_START_MIN)
        arrivals = []
        sight = 0
        meals_seen = 0
        idle = 0.0

        if not day_pois:
            days_detail.append({
                'pois': [], 'distance_km': 0.0, 'time_min': 0.0,
                'cost': 0.0, 'score': 0.0, 'arrivals': []
            })
            continue

        path = [hotel] + day_pois + [hotel]

        for i in range(len(path) - 1):
            d = haversine_km(path[i]['lat'], path[i]['lng'],
                             path[i + 1]['lat'], path[i + 1]['lng'])
            t = travel_time_min(d)
            c = travel_cost(d)
            day_dist += d
            day_cost_local += c
            current_time += t

            if i + 1 < len(path) - 1:
                poi = path[i + 1]
                if current_time < poi['open_min']:
                    current_time = float(poi['open_min'])
                if poi['category'] == 'restaurant':
                    lo, hi = LUNCH_WIN if (meals_seen == 0 and current_time < MEAL_SPLIT) else DINNER_WIN
                    meals_seen += 1
                    if current_time < lo:
                        idle += lo - current_time
                        current_time = float(lo)          # รอ/พักจนถึงเวลามื้อ (เวลาที่รอนับรวมในเวลาต่อวัน)
                    elif current_time > hi:
                        violations.append(f"Day {day_idx + 1}: ถึง {poi['id']} สายเกินช่วงมื้อ")
                else:
                    sight += poi['duration_min']
                if current_time > poi['close_min']:      # ตรวจหลังรอช่วงมื้อ: ร้านที่ปิดก่อน 17:00 ใช้เป็นมื้อเย็นไม่ได้
                    violations.append(
                        f"Day {day_idx + 1}: ไปถึง {poi['id']} หลังเวลาปิด"
                    )
                arrivals.append((poi['id'], int(current_time)))
                day_score_local += poi['score']
                day_cost_local += poi['cost']
                current_time += poi['duration_min']

        if sight > MAX_SIGHT_MIN:
            violations.append(f"Day {day_idx + 1}: เวลาท่องเที่ยวเกิน ({sight} > {MAX_SIGHT_MIN} นาที)")
        day_time_total = current_time - DAY_START_MIN
        if day_time_total > day_time:
            violations.append(
                f"Day {day_idx + 1}: ใช้เวลาเกิน ({day_time_total:.0f} > {day_time} นาที)"
            )

        days_detail.append({
            'pois': [p['id'] for p in day_pois],
            'distance_km': round(day_dist, 2),
            'time_min': round(day_time_total, 1),
            'cost': round(day_cost_local, 0),
            'score': round(day_score_local, 1),
            'idle_min': round(idle),
            'arrivals': arrivals
        })
        total_score += day_score_local
        total_cost += day_cost_local

    if total_cost > budget:
        violations.append(f"งบประมาณเกิน: {total_cost:.0f} > {budget}")

    return {
        'total_score': round(total_score, 1),
        'total_cost': round(total_cost, 0),
        'days_detail': days_detail,
        'valid': len(violations) == 0,
        'violations': violations
    }



# ============================================================
# แสดงผล
# ============================================================
def print_result(result: Dict, label: str = '', elapsed_ms: float = None):
    """แสดงผลสรุป: score, cost, valid, violations และรายละเอียดแต่ละวัน"""
    print('=' * 60)
    if label:
        print(f"  {label}")
        print('=' * 60)
    print(f"  Total score : {result['total_score']}")
    print(f"  Total cost  : {result['total_cost']:.0f}")
    print(f"  Valid       : {result['valid']}")
    if elapsed_ms is not None:
        print(f"  Runtime     : {elapsed_ms:.1f} ms")
    if result['violations']:
        print(f"  Violations  : {len(result['violations'])}")
        for v in result['violations'][:3]:
            print(f"    - {v}")
    print('  Days:')
    for i, d in enumerate(result['days_detail']):
        print(f"    Day {i + 1}: {len(d['pois'])} จุด - "
              f"score={d['score']}, time={d['time_min']:.0f}m, "
              f"cost={d['cost']:.0f}, dist={d['distance_km']}km")
        print(f"      {d['pois']}")
