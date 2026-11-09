# -*- coding: utf-8 -*-
"""
hybrid.py - Hybrid Algorithm: Greedy seed + GA refinement + 2-opt local search

Workflow:
  1) Greedy slot-based → ได้ initial solution ที่ใช้งานได้ทันที
  2) GA refinement → ลองสับเปลี่ยน POIs ระหว่างวันเพื่อหา global optima
  3) 2-opt local search → ปรับลำดับ attractions ในแต่ละวันให้ travel distance น้อยสุด

ออกแบบให้รักษา slot pattern (slot 3 = lunch, slot 6 = dinner) ตลอดกระบวนการ
"""
import random
import copy
import time
import utils
from typing import List, Dict, Tuple
from utils import (split_attrs, MAX_ATTRS, haversine_km, travel_time_min, travel_cost,
                   evaluate_route, DAY_TIME_BUDGET, DAY_START_MIN)
from greedy import (greedy_solve, _find_best_for_slot,
                    LUNCH_TRIGGER, DINNER_TRIGGER)


# ============================================================
# 2-opt Local Search
# ============================================================
def _route_distance(day_pois: List[Dict], hotel: Dict) -> float:
    """ระยะทางรวมของเส้นทางใน 1 วัน (โรงแรม → POIs → โรงแรม)"""
    if not day_pois:
        return 0.0
    path = [hotel] + day_pois + [hotel]
    total = 0.0
    for i in range(len(path) - 1):
        total += haversine_km(path[i]['lat'], path[i]['lng'],
                              path[i + 1]['lat'], path[i + 1]['lng'])
    return total


def two_opt_day(day_pois: List[Dict], hotel: Dict) -> List[Dict]:
    """2-opt swap optimization within a day.
    รักษาตำแหน่ง slot 3 (lunch) และ slot 6 (dinner) ไว้
    Only accepts swaps that don't create time-window violations.
    """
    n = len(day_pois)
    if n < 3:
        return day_pois

    # หา positions ที่เป็น restaurant - ห้ามขยับ
    fixed_positions = set()
    for idx, p in enumerate(day_pois):
        if p['category'] == 'restaurant':
            fixed_positions.add(idx)

    current = list(day_pois)
    current_dist = _route_distance(current, hotel)
    improved = True
    iters = 0
    while improved and iters < 50:
        improved = False
        iters += 1
        for i in range(n - 1):
            if i in fixed_positions:
                continue
            for j in range(i + 1, n):
                if j in fixed_positions:
                    continue
                # ลอง swap ตำแหน่ง i และ j
                trial = list(current)
                trial[i], trial[j] = trial[j], trial[i]
                trial_dist = _route_distance(trial, hotel)
                if trial_dist < current_dist - 0.01:
                    # ตรวจสอบ: ไม่มี time violation หลัง swap
                    ev = evaluate_route([trial], hotel, float('inf'))
                    if ev['valid']:
                        current = trial
                        current_dist = trial_dist
                        improved = True
                        break
            if improved:
                break
    return current


# ============================================================
# GA operators (รักษา slot pattern)
# ============================================================
def _slot_repair(chromosome: List[List[Dict]]) -> List[List[Dict]]:
    """แก้ chromosome ให้ตรงรูปแบบ slot:
       attractions ใน slots 1,2,4,5  +  restaurants ใน slots 3,6
       ถ้าไม่มี restaurant ในวัน → leave gap (skip slot)
    """
    repaired = []
    for day in chromosome:
        attrs = [p for p in day if p['category'] != 'restaurant']
        rests = [p for p in day if p['category'] == 'restaurant']

        # จำกัด attractions สูงสุด MAX_ATTRS / restaurants สูงสุด 2; แบ่งเช้า/บ่ายตามเวลาที่ใช้จริง
        attrs = attrs[:MAX_ATTRS]
        rests = rests[:2]
        morning, afternoon, evening = split_attrs(attrs)
        new_day = list(morning)
        if len(rests) >= 1:
            new_day.append(rests[0])          # มื้อกลางวัน
        new_day.extend(afternoon)
        if len(rests) >= 2:
            new_day.append(rests[1])          # มื้อเย็น
        new_day.extend(evening)               # จุดที่เปิดค่ำ (โชว์/ตลาดกลางคืน) หลังมื้อเย็น
        repaired.append(new_day)

    # ลบ POI ที่ซ้ำข้ามวัน
    seen = set()
    final = [[] for _ in repaired]
    for d, day in enumerate(repaired):
        for poi in day:
            if poi['id'] not in seen:
                seen.add(poi['id'])
                final[d].append(poi)
    return final


def _crossover(p1: List[List[Dict]], p2: List[List[Dict]]) -> List[List[Dict]]:
    """Day-level crossover: แต่ละวันสุ่มรับจาก p1 หรือ p2 แล้ว slot_repair"""
    days = len(p1)
    child = []
    for d in range(days):
        if random.random() < 0.5:
            child.append([dict(x) for x in p1[d]])
        else:
            child.append([dict(x) for x in p2[d]])
    return _slot_repair(child)


def _mutate(chromosome: List[List[Dict]], all_pois: List[Dict],
            mutation_rate: float = 0.3) -> List[List[Dict]]:
    """Mutation operators (slot-aware):
       - swap_attr: swap attraction with unused
       - swap_rest: swap restaurant with unused
       - move_across_days: move POI from one day to another
    """
    if random.random() > mutation_rate:
        return chromosome

    used_ids = {p['id'] for day in chromosome for p in day}
    unused_attrs = [p for p in all_pois if p['category'] != 'restaurant' and p['id'] not in used_ids]
    unused_rests = [p for p in all_pois if p['category'] == 'restaurant' and p['id'] not in used_ids]

    op = random.choice(['swap_attr', 'swap_rest', 'cross_day', 'remove'])

    if op == 'swap_attr' and unused_attrs:
        days_with_attr = [(d, [i for i, p in enumerate(chromosome[d])
                                if p['category'] != 'restaurant'])
                          for d in range(len(chromosome))]
        days_with_attr = [(d, idxs) for d, idxs in days_with_attr if idxs]
        if days_with_attr:
            d, idxs = random.choice(days_with_attr)
            i = random.choice(idxs)
            chromosome[d][i] = random.choice(unused_attrs)

    elif op == 'swap_rest' and unused_rests:
        days_with_rest = [(d, [i for i, p in enumerate(chromosome[d])
                                if p['category'] == 'restaurant'])
                          for d in range(len(chromosome))]
        days_with_rest = [(d, idxs) for d, idxs in days_with_rest if idxs]
        if days_with_rest:
            d, idxs = random.choice(days_with_rest)
            i = random.choice(idxs)
            chromosome[d][i] = random.choice(unused_rests)

    elif op == 'cross_day' and len(chromosome) >= 2:
        non_empty = [d for d in range(len(chromosome)) if chromosome[d]]
        if len(non_empty) >= 2:
            d1, d2 = random.sample(non_empty, 2)
            i = random.randrange(len(chromosome[d1]))
            j = random.randrange(len(chromosome[d2]))
            # สลับเฉพาะ POI ประเภทเดียวกัน
            if chromosome[d1][i]['category'] == chromosome[d2][j]['category']:
                chromosome[d1][i], chromosome[d2][j] = chromosome[d2][j], chromosome[d1][i]

    elif op == 'remove':
        non_empty = [d for d in range(len(chromosome)) if chromosome[d]]
        if non_empty:
            d = random.choice(non_empty)
            i = random.randrange(len(chromosome[d]))
            chromosome[d].pop(i)

    return _slot_repair(chromosome)


# ============================================================
# คำนวณ fitness (slot + budget aware)
# ============================================================
def diversity_stats(chromosome: List[List[Dict]]) -> Tuple[float, int]:
    """(จำนวนหมวด attraction ที่ต่างกันเฉลี่ยต่อวัน, จำนวนครั้งที่หมวดเดียวซ้ำเกิน 2 จุดต่อวัน)"""
    distinct, over = [], 0
    for day in chromosome:
        cats = [p['category'] for p in day if p['category'] != 'restaurant']
        if not cats:
            continue
        counts = {c: cats.count(c) for c in set(cats)}
        distinct.append(len(counts))
        over += sum(max(0, n - 2) for n in counts.values())
    return (sum(distinct) / len(distinct) if distinct else 0.0), over


DIST_WEIGHT = 0.03   # คะแนนที่หักต่อ km ที่ต้องขับ (แผนสมจริงขึ้น: ไม่ซิกแซกข้ามเกาะ/จังหวัด)


def _fitness(chromosome: List[List[Dict]], hotel: Dict, budget: float,
             scoring_mode: str = 'ratio', diversity_weight: float = 0.0) -> float:
    result = evaluate_route(chromosome, hotel, budget)
    score = result['total_score']
    penalty = 0.0

    if result['total_cost'] > budget:
        penalty += (result['total_cost'] - budget) * 0.03
    for v in result['violations']:
        if 'งบประมาณเกิน' in v: pass
        elif 'ใช้เวลาเกิน' in v: penalty += 50.0
        elif 'หลังเวลาปิด' in v or 'เกินช่วงมื้อ' in v: penalty += 25.0
        elif 'เวลาท่องเที่ยวเกิน' in v: penalty += 50.0
        else: penalty += 10.0

    # Slot pattern bonus: reward valid 6-slot days
    slot_bonus = 0.0
    for day in chromosome:
        n = len(day)
        if n == 0:
            continue
        # ให้ bonus วันที่มีครบ 6 จุด
        if n >= 6:
            slot_bonus += 3.0
        # ให้ bonus วันที่มีมื้ออาหาร
        rests = [p for p in day if p['category'] == 'restaurant']
        if len(rests) >= 1:
            slot_bonus += 1.0
        if len(rests) >= 2:
            slot_bonus += 1.0
        # penalize วันที่มีร้านอาหารมากเกิน
        if len(rests) > 2:
            penalty += (len(rests) - 2) * 5.0

    if diversity_weight:
        # หลายวัตถุประสงค์ (weighted-sum): score + ความหลากหลายของหมวดต่อวัน − การซ้ำหมวดเกิน 2 จุด/วัน
        for day in chromosome:
            cats = [p['category'] for p in day if p['category'] != 'restaurant']
            if not cats:
                continue
            counts = {c: cats.count(c) for c in set(cats)}
            score += diversity_weight * (len(counts) - 1)
            score -= diversity_weight * sum(max(0, n - 2) for n in counts.values())

    penalty += 0.02 * sum(d.get('idle_min', 0) for d in result['days_detail'])   # เวลานั่งรอก่อนมื้อ
    penalty += utils.TIME_WEIGHT * sum(d['time_min'] for d in result['days_detail'])   # เวลาทั้งวัน (เที่ยว+เดินทาง+มื้อ+รอ)
    penalty += DIST_WEIGHT * sum(d['distance_km'] for d in result['days_detail'])      # ระยะขับรวม: ให้แผนจัดกลุ่มตามพื้นที่
    return score + slot_bonus - penalty


# ============================================================
# เติมมื้ออาหาร — รับประกัน lunch + dinner ครบทุกวัน
# ============================================================
def meal_fill(routes: List[List[Dict]], pois: List[Dict], hotel: Dict,
              budget: float, scoring_mode: str = 'ratio') -> List[List[Dict]]:
    """Post-process GA/Hybrid result: use greedy slot logic to insert
    missing lunch and dinner into every day that lacks them.

    GA controls attraction selection (better global search);
    this ensures realistic meal slots are always present.
    """
    used_ids = {p['id'] for day in routes for p in day}
    ev = evaluate_route(routes, hotel, budget)
    remaining = max(0.0, budget - ev['total_cost'])

    new_routes = []
    for day_idx, day in enumerate(routes):
        attrs  = [p for p in day if p['category'] != 'restaurant']
        e_rest = [p for p in day if p['category'] == 'restaurant']

        # มี lunch + dinner ครบแล้ว — จัดลำดับ slot เท่านั้น
        if len(e_rest) >= 2:
            mo, af, ev_ = split_attrs(attrs[:MAX_ATTRS])
            new_day = mo + [e_rest[0]] + af + [e_rest[1]] + ev_
            new_routes.append(new_day)
            continue

        # แบ่ง attractions เป็นช่วงเช้า (slots 1-2) และช่วงบ่าย (slots 4-5)
        morning, afternoon, evening = split_attrs(attrs[:MAX_ATTRS])
        days_left = max(1, len(routes) - day_idx)
        day_bgt   = remaining / days_left
        day_cats  = {}

        # --- จำลองเวลาผ่าน attractions ช่วงเช้า ---
        cur_t   = float(DAY_START_MIN)
        cur_pos = hotel
        for poi in morning:
            d = haversine_km(cur_pos['lat'], cur_pos['lng'],
                             poi['lat'], poi['lng'])
            cur_t += travel_time_min(d)
            if cur_t < poi['open_min']:
                cur_t = float(poi['open_min'])
            cur_t += poi['duration_min']
            cur_pos = poi
            day_cats[poi['category']] = day_cats.get(poi['category'], 0) + 1
            day_bgt -= travel_cost(d) + poi['cost']

        # เลื่อนเวลาเข้าสู่ช่วง lunch
        if cur_t < LUNCH_TRIGGER:
            cur_t = float(LUNCH_TRIGGER)

        # --- หาร้านอาหาร lunch ---
        lunch = None
        if e_rest:
            # ใช้ restaurant ที่มีอยู่แล้วเป็น lunch
            lunch = e_rest[0]
            d = haversine_km(cur_pos['lat'], cur_pos['lng'],
                             lunch['lat'], lunch['lng'])
            cur_t = max(cur_t + travel_time_min(d), float(lunch['open_min']))
            cur_t += lunch['duration_min']
            cur_pos = lunch
        else:
            r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
                                    DAY_TIME_BUDGET, day_bgt, day_cats,
                                    'lunch', scoring_mode)
            if r is None:   # มื้อเป็น hard requirement: ขยายงบและช่วงเวลาเข้าร้าน
                r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
                                        DAY_TIME_BUDGET, 1e9, day_cats,
                                        'lunch', scoring_mode, relax_meal=True)
            if r:
                lunch, d_l, arr_l = r
                used_ids.add(lunch['id'])
                cost_l = travel_cost(d_l) + lunch['cost']
                day_bgt   -= cost_l
                remaining -= cost_l
                cur_t      = arr_l + lunch['duration_min']
                cur_pos    = lunch

        if lunch:
            day_cats['restaurant'] = day_cats.get('restaurant', 0) + 1

        # --- จำลองเวลาผ่าน attractions ช่วงบ่าย ---
        for poi in afternoon:
            d = haversine_km(cur_pos['lat'], cur_pos['lng'],
                             poi['lat'], poi['lng'])
            cur_t += travel_time_min(d)
            if cur_t < poi['open_min']:
                cur_t = float(poi['open_min'])
            cur_t += poi['duration_min']
            cur_pos = poi
            day_cats[poi['category']] = day_cats.get(poi['category'], 0) + 1
            day_bgt -= travel_cost(d) + poi['cost']

        # เลื่อนเวลาเข้าสู่ช่วง dinner
        if cur_t < DINNER_TRIGGER:
            cur_t = float(DINNER_TRIGGER)

        # --- หาร้านอาหาร dinner ---
        dinner = None
        r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
                                DAY_TIME_BUDGET, day_bgt, day_cats,
                                'dinner', scoring_mode)
        if r is None:
            # Fallback: ขยายงบ — dinner เป็น hard requirement
            meal_cap = max(500, budget * 0.08)
            r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
                                    DAY_TIME_BUDGET, meal_cap, day_cats,
                                    'dinner', scoring_mode)
        if r is None:
            # Last resort: ร้านอาหารฟรีเท่านั้น
            r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
                                    DAY_TIME_BUDGET, 1e9, day_cats,
                                    'dinner', scoring_mode, free_only=True)
        if r is None:
            r = _find_best_for_slot(pois, used_ids, cur_pos, cur_t, hotel,
                                    DAY_TIME_BUDGET, 1e9, day_cats,
                                    'dinner', scoring_mode, relax_meal=True)
        if r:
            dinner, d_d, arr_d = r
            used_ids.add(dinner['id'])
            remaining -= travel_cost(d_d) + dinner['cost']

        # --- ประกอบ route ของวันตามลำดับ slot ---
        new_day = list(morning)
        if lunch:    new_day.append(lunch)
        new_day.extend(afternoon)
        if dinner:   new_day.append(dinner)
        new_day.extend(evening)
        new_routes.append(new_day)

    return new_routes


# ============================================================
# ซ่อมเวลา — ลบ attr ออกจากวันที่เกิน time budget
# ============================================================
def _time_repair(routes: List[List[Dict]], hotel: Dict, protect=()) -> List[List[Dict]]:
    """Remove violating non-restaurant POIs from days that:
      (a) exceed DAY_TIME_BUDGET, or
      (b) contain POIs visited after their closing time.
    Preserves restaurant (meal) slots and POIs whose id is in `protect` (เลือกโดยผู้ใช้)."""
    import re as _re
    routes = [list(d) for d in routes]
    for d_idx in range(len(routes)):
        for _ in range(10):  # max 10 removals per day
            ev = evaluate_route([routes[d_idx]], hotel, float('inf'))
            day_viols = [v for v in ev['violations'] if f'Day 1:' in v]
            time_ok = ev['days_detail'][0]['time_min'] <= DAY_TIME_BUDGET
            if time_ok and not day_viols:
                break

            # รวบรวม ID ของ POI ที่ไปถึงหลังเวลาปิด
            late_ids = set()
            for v in day_viols:
                if 'หลังเวลาปิด' in v:
                    m = _re.search(r'ไปถึง (\S+) หลังเวลาปิด', v)
                    if m:
                        late_ids.add(m.group(1))

            # Priority: ลบ POI ที่ไปถึงสายก่อน ถ้าไม่มีให้ลบ attr score ต่ำสุด
            worst_i = None
            if late_ids:
                for i, p in enumerate(routes[d_idx]):
                    if p['id'] in late_ids and p['category'] != 'restaurant' and p['id'] not in protect:
                        worst_i = i
                        break
            if worst_i is None:
                worst_score = float('inf')
                for i, p in enumerate(routes[d_idx]):
                    if p['category'] != 'restaurant' and p['id'] not in protect and p['score'] < worst_score:
                        worst_score = p['score']; worst_i = i
            if worst_i is None:
                break
            routes[d_idx].pop(worst_i)
    return routes


# ============================================================
# Hybrid main
# ============================================================
def hybrid_solve(pois: List[Dict], hotel: Dict, days: int, budget: float,
                 scoring_mode: str = 'ratio',
                 pop_size: int = 30, generations: int = 60,
                 mutation_rate: float = 0.3,
                 verbose: bool = False,
                 diversity_weight: float = 0.0, rl_theta=None, ils: bool = True) -> Tuple[List[List[Dict]], List[float]]:
    """Hybrid Algorithm:
       Step 1: Greedy slot-based seed (multiple random starts)
       Step 2: GA refinement
       Step 3: 2-opt local search per day
       Returns: (best_chromosome, fitness_history)
    """
    # ขั้นที่ 1: สร้างประชากรเริ่มต้นจาก greedy seeds หลายชุด (POI order ต่างกัน)
    population = []
    seed_pois = list(pois)
    random.shuffle(seed_pois)
    population.append(greedy_solve(seed_pois, hotel, days, budget, scoring_mode=scoring_mode))
    population.append(greedy_solve(pois, hotel, days, budget, scoring_mode=scoring_mode))
    if rl_theta is not None:   # RL seed: policy ที่ฝึกแล้ว 1 แผน deterministic + ครึ่งหนึ่งของที่เหลือสุ่มตาม policy (temperature ต่ำ)
        from rl import rl_solve
        population.append(rl_solve(pois, hotel, days, budget, rl_theta, sample=False))
    while len(population) < pop_size:
        random.shuffle(seed_pois)
        if rl_theta is not None and len(population) % 2 == 0:
            import numpy as _np
            _np.random.seed(random.randrange(1 << 30))
            cand = rl_solve(seed_pois, hotel, days, budget, rl_theta, sample=True, temperature=0.4)
        else:
            # โหมด quality ไม่คิดค่าเดินทางตอนเลือก — ผสม seed แบบ ratio (คำนึงถึงต้นทุน) เพื่อให้มีแผนที่อยู่ในงบเมื่อโรงแรมอยู่ไกลแหล่งท่องเที่ยว
            cand = greedy_solve(seed_pois, hotel, days, budget,
                                scoring_mode='ratio' if (scoring_mode == 'quality' and len(population) % 3 == 0) else scoring_mode)
        population.append(cand)

    fitnesses = [_fitness(c, hotel, budget, scoring_mode, diversity_weight) for c in population]

    best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
    best = copy.deepcopy(population[best_idx])
    best_fit = fitnesses[best_idx]
    history = [best_fit]
    no_improve = 0
    EARLY_STOP = 15

    # ขั้นที่ 2: วิวัฒนาการด้วย Genetic Algorithm
    for gen in range(generations):
        new_pop = [copy.deepcopy(best)]  # elitism

        # ปรับ mutation rate ลดลงตาม generation
        cur_mut_rate = mutation_rate * (1.0 - gen / (2.0 * generations))

        while len(new_pop) < pop_size:
            # Tournament selection k=3 (เลือก best จาก 3 ตัวสุ่ม)
            c1 = random.sample(range(len(population)), 3)
            p1 = population[max(c1, key=lambda i: fitnesses[i])]
            c2 = random.sample(range(len(population)), 3)
            p2 = population[max(c2, key=lambda i: fitnesses[i])]
            child = _crossover(p1, p2)
            child = _mutate(child, pois, cur_mut_rate)
            new_pop.append(child)

        population = new_pop
        fitnesses = [_fitness(c, hotel, budget, scoring_mode, diversity_weight) for c in population]

        cur_best = max(range(len(population)), key=lambda i: fitnesses[i])
        if fitnesses[cur_best] > best_fit:
            best_fit = fitnesses[cur_best]
            best = copy.deepcopy(population[cur_best])
            no_improve = 0
        else:
            no_improve += 1

        history.append(best_fit)
        if verbose and gen % 10 == 0:
            print(f"  Gen {gen}: fitness={best_fit:.2f}")
        # หยุดเร็วถ้าไม่มี improvement
        if no_improve >= EARLY_STOP:
            if verbose:
                print(f"  Early stop at gen {gen} (no improvement for {EARLY_STOP} gens)")
            break

    # ขั้นที่ 3: 2-opt local search บน best solution
    refined = []
    for day in best:
        refined.append(two_opt_day(day, hotel))

    # ขั้นที่ 4: รับประกัน lunch + dinner ครบทุกวัน
    refined = meal_fill(refined, pois, hotel, budget, scoring_mode)

    # ขั้นที่ 5: ลบ attr ออกจากวันที่ยังเกิน time budget
    refined = _time_repair(refined, hotel)

    # ขั้นที่ 6: การเติมมื้อ/ซ่อมเวลาอาจดันงบเกิน (พบ 2 จาก 960 รอบทดสอบ) — ซ่อมงบแล้วตรวจมื้อและเวลาซ้ำ
    for _ in range(3):
        refined = _budget_repair(refined, hotel, budget, pool=pois)
        if all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in refined if day):
            break
        for d, day in enumerate(refined):   # วันที่แน่นจนไม่มีเวลาใส่มื้อ: ถอด attraction คะแนนต่ำสุดออกก่อนเติมมื้อ
            if day and sum(1 for p in day if p['category'] == 'restaurant') < 2:
                cands = [(i, p) for i, p in enumerate(day) if p['category'] != 'restaurant']
                if cands:
                    refined[d] = [p for i, p in enumerate(day) if i != min(cands, key=lambda c: c[1]['score'])[0]]
        refined = _time_repair(meal_fill(refined, pois, hotel, budget, scoring_mode), hotel)
    refined = _budget_repair(refined, hotel, budget, pool=pois)

    if ils:   # ขั้นที่ 7 (ทดลอง): insertion local search — รับผลเฉพาะเมื่อยังผ่านข้อจำกัดและ fitness ไม่แย่ลง
        from ils import insertion_local_search
        improved = insertion_local_search(refined, pois, hotel, budget, diversity_weight)
        improved = [two_opt_day(day, hotel) for day in improved]
        ev = evaluate_route(improved, hotel, budget)
        meals_ok = all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in improved if day)
        if ev['valid'] and meals_ok and (_fitness(improved, hotel, budget, scoring_mode, diversity_weight)
                                         >= _fitness(refined, hotel, budget, scoring_mode, diversity_weight)):
            refined = improved

    return refined, history


def _budget_repair(routes: List[List[Dict]], hotel: Dict, budget: float, protect=(), pool=None) -> List[List[Dict]]:
    """ถ้าแผนเกินงบ แทนที่ attraction (ไม่ได้ล็อก) ที่แพงสุดในวันที่มีสถานที่มากที่สุด ด้วยสถานที่ที่ถูกกว่าและคะแนนสูงสุดที่ยังไม่ได้ใช้ในวันเดียวกัน
       ถ้าไม่มีตัวแทนที่ใช้ได้จึงลบทิ้ง จนอยู่ในงบ (เดิมลบอย่างเดียว ทำให้บางวันเหลือจุดน้อยเมื่อกำหนดงบต่ำ)"""
    routes = [list(d) for d in routes]
    for _ in range(60):
        if evaluate_route(routes, hotel, float('inf'))['total_cost'] <= budget:
            break
        cands = [(d, i, p) for d, day in enumerate(routes) for i, p in enumerate(day)
                 if p['category'] != 'restaurant' and p['id'] not in protect]
        if not cands:
            break
        sights = [sum(1 for p in day if p['category'] != 'restaurant') for day in routes]
        d, i, old = max(cands, key=lambda c: (sights[c[0]], c[2]['cost'], -c[2]['score']))   # ตัดจากวันที่มีสถานที่มากที่สุดก่อน เพื่อให้แต่ละวันเหลือจำนวนใกล้เคียงกัน
        used = {p['id'] for day in routes for p in day}
        subs = sorted((p for p in (pool or []) if p['category'] != 'restaurant' and p['id'] not in used and p['id'] not in protect
                       and p['cost'] < old['cost']), key=lambda p: -p['score'])[:30]
        for u in subs:
            trial = routes[d][:i] + [u] + routes[d][i + 1:]
            if evaluate_route([trial], hotel, float('inf'))['valid']:
                routes[d] = trial
                break
        else:
            routes[d].pop(i)
    return routes


def _final_validity(routes: List[List[Dict]], hotel: Dict, locked, tried=None) -> List[List[Dict]]:
    """วันที่ยังผิดเวลา/เวลาปิดหลังซ่อมแล้ว (มักเกิดจากจุดที่ผู้ใช้ล็อกเปิดดึก ชนกับมื้อเย็น):
       1) ลองย้ายจุดล็อกที่เปิดหลัง 17:00 ไปท้ายวัน  2) ถ้ายังไม่ผ่าน ถอดจุดล็อกของวันนั้นออก (ผู้ใช้จะได้รับแจ้ง)"""
    routes = [list(d) for d in routes]
    for d, day in enumerate(routes):
        if not day or evaluate_route([day], hotel, float('inf'))['valid']:
            continue
        late = [p for p in day if p['id'] in locked and p['open_min'] >= 1020]
        trial = [p for p in day if p not in late] + late
        # ย้ายไปท้ายวันได้ครั้งเดียวต่อวัน (meal_fill อาจจัดลำดับกลับ) — ถ้ายังไม่ผ่านรอบถัดไปถอดจุดล็อกออก
        if late and (tried is None or d not in tried) and evaluate_route([trial], hotel, float('inf'))['valid']:
            routes[d] = trial
            if tried is not None:
                tried.add(d)
        else:
            routes[d] = [p for p in day if p['id'] not in locked]
    return routes


def infeasible_locks(pois: List[Dict], hotel: Dict, locked_ids, budget: float) -> List[str]:
    """POI ที่ผู้ใช้เลือกแต่ใส่ในแผนใดก็ไม่ได้ (เปิดดึกเกินวัน/เกินงบ/เกินเวลาต่อวัน) — คืน id เพื่อไม่ล็อกและแจ้งผู้ใช้"""
    by_id = {p['id']: p for p in pois}
    bad = []
    for pid in locked_ids:
        p = by_id.get(pid)
        if p is None:
            continue
        ev = evaluate_route([[p]], hotel, budget)
        if not ev['valid']:
            bad.append(pid)
    return bad


def reoptimize_solve(pois: List[Dict], hotel: Dict, routes: List[List[Dict]], budget: float,
                     locked_ids=(), excluded_ids=(), scoring_mode: str = 'quality',
                     pop_size: int = 20, generations: int = 30,
                     mutation_rate: float = 0.6, diversity_weight: float = 0.0) -> List[List[Dict]]:
    """Re-optimization หลังผู้ใช้แก้แผน: เริ่มจาก routes ปัจจุบัน (ไม่สร้างใหม่ทั้งหมด)
       - locked_ids:   POI ที่ผู้ใช้เลือกเอง (สลับเข้า/เพิ่ม) ต้องอยู่ในแผนเสมอ
       - excluded_ids: POI ที่ผู้ใช้ลบ ห้ามกลับเข้ามา
       ใช้ evolutionary search แบบ (mu+lambda) เฉพาะ mutation แล้วตามด้วย 2-opt, meal_fill, time_repair
       เพื่อปรับ POI ที่ไม่ล็อกให้ score สูงขึ้นภายใต้งบ/เวลาเดิม
    """
    locked, excluded = set(locked_ids), set(excluded_ids)
    locked -= set(infeasible_locks(pois, hotel, locked, budget))
    locked_all = set(locked)
    pool = [p for p in pois if p['id'] not in excluded]
    start = [[p for p in day if p['id'] not in excluded] for day in routes]

    def respects(ch):
        ids = {p['id'] for day in ch for p in day}
        return locked <= ids and not (ids & excluded)

    population = [start]
    fits = [_fitness(start, hotel, budget, scoring_mode, diversity_weight)]
    for _ in range(generations):
        children = []
        for _ in range(pop_size):
            parent = population[random.randrange(len(population))]
            child = _mutate(copy.deepcopy(parent), pool, mutation_rate)
            if respects(child):
                children.append(child)
        population += children
        fits += [_fitness(c, hotel, budget, scoring_mode, diversity_weight) for c in children]
        order = sorted(range(len(population)), key=lambda i: fits[i], reverse=True)[:pop_size]
        population = [population[i] for i in order]
        fits = [fits[i] for i in order]

    refined = [two_opt_day(day, hotel) for day in population[0]]
    before = refined
    refined = meal_fill(refined, pool, hotel, budget, scoring_mode)
    kept = {p['id'] for day in refined for p in day}
    for d, day in enumerate(before):          # meal_fill ตัด attr เกิน 4 ต่อวัน — คืนจุดที่ผู้ใช้ล็อกไว้
        for p in day:
            if p['id'] in locked and p['id'] not in kept:
                refined[d].insert(max(0, len(refined[d]) - 1), p)
    # รอบซ่อมวนซ้ำจนแผนผ่านทุกข้อจำกัดและมีมื้อครบ (การเติมมื้ออาจทำให้เวลา/งบเสียอีก จึงต้องตรวจหลังเติมเสมอ)
    def meals_ok(rs):
        return all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in rs)

    tried_days = set()
    for _ in range(5):
        refined = _time_repair(refined, hotel, protect=locked)
        refined = _budget_repair(refined, hotel, budget, protect=locked)
        refined = _final_validity(refined, hotel, locked, tried_days)
        locked = locked & {p['id'] for day in refined for p in day}      # จุดล็อกที่ยังอยู่ในแผน
        lacking = [d for d, day in enumerate(refined)
                   if sum(1 for p in day if p['category'] == 'restaurant') < 2]
        for d in lacking:           # วันที่แน่นจนไม่มีเวลาใส่มื้อ: ลบ attraction คะแนนต่ำสุดที่ไม่ได้ล็อกก่อนเติมมื้อ
            cands = [(i, p) for i, p in enumerate(refined[d])
                     if p['category'] != 'restaurant' and p['id'] not in locked]
            if cands:
                refined[d].pop(min(cands, key=lambda c: c[1]['score'])[0])
        refined = meal_fill(refined, pool, hotel, budget, scoring_mode)
        ev = evaluate_route(refined, hotel, budget)
        if ev['valid'] and meals_ok(refined):
            break
    if not meals_ok(refined):    # ทางสุดท้าย: วันที่ยังไม่มีมื้อครบ เก็บเฉพาะจุดที่ผู้ใช้ล็อก แล้วเติมมื้อใหม่ (ได้แผนสั้นแต่ใช้ได้จริง)
        for d, day in enumerate(refined):
            if sum(1 for p in day if p['category'] == 'restaurant') < 2:
                refined[d] = [p for p in day if p['id'] in locked and p['category'] != 'restaurant']
        refined = _time_repair(meal_fill(refined, pool, hotel, budget, scoring_mode), hotel, protect=locked)
        refined = _budget_repair(refined, hotel, budget, protect=locked)
    for _ in range(2):    # วันที่ยังผิดข้อจำกัดอยู่ (เช่น มื้อสายเกินช่วง): ล้างเหลือเฉพาะจุดที่ล็อก แล้วสร้างวันนั้นใหม่
        bad = {int(v.split()[1].rstrip(':')) - 1 for v in evaluate_route(refined, hotel, budget)['violations'] if v.startswith('Day ')}
        if not bad:
            break
        for d in bad:
            refined[d] = [p for p in refined[d] if p['id'] in locked and p['category'] != 'restaurant']
        refined = _time_repair(meal_fill(refined, pool, hotel, budget, scoring_mode), hotel, protect=locked)
        refined = _budget_repair(refined, hotel, budget, protect=locked)
    # จุดล็อกที่ใส่ได้จริงแต่ถูกถอดระหว่างซ่อม: ใส่กลับในตำแหน่งที่ทำให้แผนยังผ่านทุกข้อจำกัด (ระยะเพิ่มน้อยสุด)
    by_id = {p['id']: p for p in pois}
    for pid in locked_all - {p['id'] for day in refined for p in day}:
        best = None
        for d, day in enumerate(refined):
            for i in range(len(day) + 1):
                trial = refined[:d] + [day[:i] + [by_id[pid]] + day[i:]] + refined[d + 1:]
                ev = evaluate_route(trial, hotel, budget)
                if ev['valid']:
                    km = sum(x['distance_km'] for x in ev['days_detail'])
                    if best is None or km < best[0]:
                        best = (km, trial)
        if best:
            refined = best[1]
    return refined


def main():
    from utils import load_data, print_result
    pois, hotels = load_data('../data/provinces/phuket.json')
    h = next(h for h in hotels if h['id'] == 'H11')
    print(f"Hotel: {h['name_en']}")
    t0 = time.time()
    routes, history = hybrid_solve(pois, h, 6, 6800, verbose=True)
    elapsed = (time.time() - t0) * 1000
    print(f"\nElapsed: {elapsed:.0f} ms")
    print(f"History: gen0={history[0]:.1f} → final={history[-1]:.1f}")
    result = evaluate_route(routes, h, 6800)
    print_result(result, label='Hybrid')


if __name__ == '__main__':
    main()
