# -*- coding: utf-8 -*-
"""
greedy.py - Slot-based Greedy Algorithm สำหรับปัญหา B-TOPTW

Workflow ต่อหนึ่งวัน: [attr, attr, lunch, attr, attr, dinner]
  - เลือก POI ที่มี score/cost ratio สูงสุดในแต่ละ slot
  - มี fallback 3 ระดับเพื่อรับประกัน lunch + dinner ทุกวัน
  - random_factor เพิ่ม diversity เพื่อใช้เป็น seed ใน GA/Hybrid
"""
import random
from typing import List, Dict
from utils import (haversine_km, travel_time_min, travel_cost,
                   DAY_TIME_BUDGET, DAY_START_MIN, evaluate_route, LUNCH_WIN, DINNER_WIN, MAX_SIGHT_MIN)

DAY_PATTERN    = ['attr', 'attr', 'lunch', 'attr', 'attr', 'dinner']   # 6 จุด/วัน (เที่ยว 4 + อาหาร 2) เหมือน Project 1
LUNCH_TRIGGER  = 690
DINNER_TRIGGER = 1020
LUNCH_ARRIVE   = LUNCH_WIN
DINNER_ARRIVE  = DINNER_WIN
LUNCH_RELAXED  = LUNCH_WIN      # ไม่ผ่อนช่วงเวลามื้อแล้ว (ต้องตรงเวลาจริง)
DINNER_RELAXED = DINNER_WIN
MAX_MEAL_WAIT  = 90
DINNER_BUFFER_MIN = 150



# ============================================================
# ฟังก์ชันเลือก POI ต่อ slot
# ============================================================
def _find_best_for_slot(pois, used_ids, current_pos, current_time, hotel,
                        day_time, budget_left, day_categories,
                        slot_type, scoring_mode='ratio',
                        free_only=False, dinner_buffer=0, random_factor=0.0, relax_meal=False, chooser=None, sight_left=1e9):
    """เลือก POI ที่เหมาะสมที่สุดสำหรับ slot ประเภท attr / lunch / dinner
    คืน (poi, distance_km, arrive_time) หรือ None ถ้าหาไม่ได้
    chooser: ฟังก์ชันเลือก candidate แทนการเรียงคะแนน (ใช้กับ RL) รับ list ของ
             (score, poi, d_to, arrive, add_cost, time_slack, wait, cat_count) คืน index ที่เลือก
    """
    candidates = []
    for poi in pois:
        if poi['id'] in used_ids: continue
        if slot_type == 'attr' and poi['category'] == 'restaurant': continue
        if slot_type in ('lunch', 'dinner') and poi['category'] != 'restaurant': continue
        if free_only and poi['cost'] > 0: continue
        if slot_type == 'attr' and (poi['duration_min'] > 240 or poi['duration_min'] > sight_left): continue
        d_to   = haversine_km(current_pos['lat'], current_pos['lng'], poi['lat'], poi['lng'])
        d_back = haversine_km(poi['lat'], poi['lng'], hotel['lat'], hotel['lng'])
        travel_t = travel_time_min(d_to)
        back_t   = travel_time_min(d_back)
        arrive_raw = current_time + travel_t
        if arrive_raw < poi['open_min']:
            wait = poi['open_min'] - arrive_raw
            max_wait = MAX_MEAL_WAIT if slot_type in ('lunch', 'dinner') else 60
            if wait > max_wait: continue
            arrive = float(poi['open_min'])
        else:
            arrive = arrive_raw
        if arrive > poi['close_min']: continue
        lw = LUNCH_RELAXED if relax_meal else LUNCH_ARRIVE
        dw = DINNER_RELAXED if relax_meal else DINNER_ARRIVE
        if slot_type == 'lunch' and not (lw[0] <= arrive <= lw[1]): continue
        if slot_type == 'dinner' and not (dw[0] <= arrive <= dw[1]): continue
        finish = arrive + poi['duration_min']
        if (finish + back_t + dinner_buffer) - DAY_START_MIN > day_time: continue
        add_cost = travel_cost(d_to) + poi['cost']
        if poi['cost'] > 0 and add_cost > budget_left: continue
        cat_count = day_categories.get(poi['category'], 0)
        diversity_bonus = 1.0 if cat_count == 0 else (1.0 / (1 + cat_count * 0.5))
        if scoring_mode == 'quality':
            base_score = poi['score'] * diversity_bonus
        else:
            # ratio mode: ใช้ floor 80 เพื่อป้องกัน POI ฟรีใกล้ๆ ชนะจากระยะทางเสมอ
            # → POI ฟรีทุกอันแข่งกันด้วย score เป็นหลัก + noise กระจาย diversity
            effective_cost = max(add_cost, 80.0)
            base_score = (poi['score'] * diversity_bonus) / (effective_cost + 1.0)
        noise = 1.0 + random.uniform(-random_factor, random_factor) if random_factor > 0 else 1.0
        score = base_score * noise
        candidates.append((score, poi, d_to, arrive, add_cost,
                           (DAY_START_MIN + day_time) - (finish + back_t), arrive - arrive_raw, cat_count))
    if not candidates: return None
    if chooser is not None:
        c = candidates[chooser(candidates)]
        return (c[1], c[2], c[3])
    candidates.sort(key=lambda x: x[0], reverse=True)
    best, best_d_to, best_arrive = candidates[0][1], candidates[0][2], candidates[0][3]
    return (best, best_d_to, best_arrive)



# ============================================================
# Greedy solve หลัก
# ============================================================
def greedy_solve(pois, hotel, days, budget, day_time=DAY_TIME_BUDGET,
                 scoring_mode='ratio', random_factor=0.15, _alt=True):
    """สร้าง routes ด้วย slot-based greedy (วนทุกวัน × ทุก slot ตาม DAY_PATTERN)
    คืน routes: List[List[Dict]]  — routes[วัน][ลำดับ POI]
    """
    used_ids = set()
    remaining_budget = float(budget)
    routes = [[] for _ in range(days)]
    per_day_budget = (budget / max(days, 1)) * 1.1

    pois_shuffled = list(pois)
    random.shuffle(pois_shuffled)

    for day_idx in range(days):
        current_pos = hotel
        current_time = float(DAY_START_MIN)
        day_categories = {}
        day_budget_left = min(per_day_budget, remaining_budget)
        past_lunch = False
        sight_left = MAX_SIGHT_MIN
        dinner_done = False

        for slot_type in DAY_PATTERN:
            if slot_type == 'lunch' and current_time < LUNCH_TRIGGER:
                current_time = float(LUNCH_TRIGGER)
            elif slot_type == 'dinner' and current_time < DINNER_TRIGGER:
                current_time = float(DINNER_TRIGGER)

            db = DINNER_BUFFER_MIN if (slot_type == 'attr' and past_lunch and not dinner_done) else 0

            result = _find_best_for_slot(
                pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
                day_budget_left, day_categories, slot_type, scoring_mode,
                dinner_buffer=db, random_factor=random_factor, sight_left=sight_left)

            if result is None and slot_type in ('lunch', 'dinner'):
                # Fallback 1: ขยายงบสำหรับมื้ออาหาร
                meal_cap = max(300, remaining_budget * 0.5)
                result = _find_best_for_slot(
                    pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
                    meal_cap, day_categories, slot_type, scoring_mode,
                    dinner_buffer=0, random_factor=random_factor, sight_left=sight_left)

            if result is None and slot_type in ('lunch', 'dinner'):
                # Fallback 2: ร้านอาหารใดก็ได้โดยไม่สนงบ (ต้องมีมื้ออาหาร)
                result = _find_best_for_slot(
                    pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
                    1e9, day_categories, slot_type, scoring_mode,
                    dinner_buffer=0, random_factor=random_factor, sight_left=sight_left)

            if result is None and slot_type in ('lunch', 'dinner'):
                # Fallback 3: ขยายช่วงเวลาเข้าร้าน (มื้ออาหารเป็น hard requirement)
                result = _find_best_for_slot(
                    pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
                    1e9, day_categories, slot_type, scoring_mode,
                    dinner_buffer=0, random_factor=random_factor, sight_left=sight_left, relax_meal=True)

            if result is None:
                # Fallback: เลือกเฉพาะ POI ฟรี
                result = _find_best_for_slot(
                    pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
                    1e9, day_categories, slot_type, scoring_mode,
                    free_only=True, dinner_buffer=db, random_factor=random_factor, sight_left=sight_left)

            if result is None and slot_type == 'attr' and not past_lunch:
                result = _find_best_for_slot(
                    pois_shuffled, used_ids, current_pos, current_time, hotel, day_time,
                    day_budget_left, day_categories, 'attr', scoring_mode,
                    dinner_buffer=0, random_factor=random_factor, sight_left=sight_left)

            if slot_type == 'lunch': past_lunch = True
            if slot_type == 'dinner': dinner_done = True
            if result is None: continue

            poi, d_to, arrive = result
            used_ids.add(poi['id'])
            routes[day_idx].append(poi)
            if poi['category'] != 'restaurant': sight_left -= poi['duration_min']
            current_time = arrive + poi['duration_min']
            current_pos = poi
            spent = travel_cost(d_to) + poi['cost']
            remaining_budget -= spent
            day_budget_left = max(0, day_budget_left - spent)
            day_categories[poi['category']] = day_categories.get(poi['category'], 0) + 1

        if routes[day_idx]:
            d_back = haversine_km(current_pos['lat'], current_pos['lng'],
                                  hotel['lat'], hotel['lng'])
            remaining_budget -= travel_cost(d_back)
    if _alt and scoring_mode == 'quality' and evaluate_route(routes, hotel, float('inf'))['total_cost'] > budget:
        # quality ไม่คิดค่าเดินทางตอนเลือก (โรงแรมไกลทำให้เกินงบแล้วต้องตัดจนแผนสั้น) — ลองแบบ ratio แล้วเก็บแผนที่คะแนนสูงกว่า
        alt = greedy_solve(pois, hotel, days, budget, day_time, 'ratio', random_factor, _alt=False)
        base = routes
        s_alt = evaluate_route(alt, hotel, budget)
        s_base = evaluate_route(_repaired(base, hotel, budget), hotel, budget)
        return alt if (s_alt['valid'] and s_alt['total_score'] > s_base['total_score']) else _repaired(base, hotel, budget)
    return _repaired(routes, hotel, budget)


def _repaired(routes, hotel, budget):
    routes = [list(d) for d in routes]
    # ซ่อมงบ: ถ้ารวมแล้วเกินงบ (ค่ามื้อ/เดินทางกลับ) ถอด attraction ที่แพงสุดจนอยู่ในงบ — ใช้ได้กับทุกโหมด
    # ซ่อมงบ: ถ้ารวมแล้วเกินงบ (ค่ามื้อ/ค่าเดินทาง) ถอด attraction ที่ถอดแล้วประหยัดได้มากที่สุดต่อคะแนนที่เสีย
    total = lambda rs: evaluate_route(rs, hotel, float('inf'))['total_cost']
    cur = total(routes)
    for _ in range(60):
        if cur <= budget:
            break
        best = None
        for d, day in enumerate(routes):
            for i, p in enumerate(day):
                if p['category'] == 'restaurant':
                    continue
                c = total(routes[:d] + [day[:i] + day[i + 1:]] + routes[d + 1:])
                save = cur - c
                if save > 0 and (best is None or save / p['score'] > best[0]):
                    best = (save / p['score'], d, i, c)
        if best is None:
            break
        _r, d, i, cur = best
        routes[d].pop(i)
    return routes
