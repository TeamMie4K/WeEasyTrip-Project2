# -*- coding: utf-8 -*-
"""
pareto.py - Multi-objective optimization (NSGA-II) สำหรับ B-TOPTW

วัตถุประสงค์ 3 ข้อ (ผู้ใช้เลือก trade-off เองจาก Pareto front):
  1) total score            (มากที่สุด)
  2) ความหลากหลาย            (จำนวนหมวด attraction ที่ต่างกันเฉลี่ยต่อวัน — มากที่สุด)
  3) ระยะทางรวม (km)         (น้อยที่สุด)
ข้อจำกัด (งบ, เวลา, เวลาปิด, มื้ออาหาร 2 มื้อต่อวัน) จัดการด้วย constraint-domination ของ Deb:
  คำตอบที่ผ่านข้อจำกัดชนะคำตอบที่ไม่ผ่านเสมอ; ถ้าไม่ผ่านทั้งคู่ เทียบค่าความละเมิดรวม
ผลลัพธ์สุดท้ายผ่าน meal_fill / 2-opt / ซ่อมเวลาและงบ แล้วกรองให้เหลือเฉพาะ front ที่ผ่านข้อจำกัด
"""
import copy
import random
from typing import Dict, List

from utils import evaluate_route, DAY_TIME_BUDGET
from greedy import greedy_solve
from hybrid import (_crossover, _mutate, _slot_repair, two_opt_day, meal_fill,
                    _time_repair, _budget_repair, diversity_stats)


def evaluate_objectives(routes: List[List[Dict]], hotel: Dict, budget: float) -> Dict:
    """คืน objectives (ยิ่งน้อยยิ่งดีทุกตัว) + ค่าความละเมิดข้อจำกัด (0 = ผ่าน) + ค่าดิบสำหรับแสดงผล"""
    ev = evaluate_route(routes, hotel, float('inf'))
    div, _ = diversity_stats(routes)
    dist = sum(d['distance_km'] for d in ev['days_detail'])
    # งบประมาณนับเฉพาะค่าเข้า+ค่าอาหาร (ต่อคน) ตรงกับ _trim_to_budget — ค่าเดินทางถือเป็น overhead ไม่นับในงบกิจกรรม
    poi_cost = sum(p['cost'] for day in routes for p in day)
    viol = float(len(ev['violations']))
    if poi_cost > budget:
        viol += (poi_cost - budget) / max(budget, 1.0) * 10.0
    for d in ev['days_detail']:
        if d['time_min'] > DAY_TIME_BUDGET:
            viol += (d['time_min'] - DAY_TIME_BUDGET) / 60.0
    for day in routes:
        if day and sum(1 for p in day if p['category'] == 'restaurant') < 2:
            viol += 1.0
    return {'obj': (-ev['total_score'], -div, dist), 'viol': viol, 'score': ev['total_score'],
            'diversity': div, 'distance_km': dist, 'cost': poi_cost, 'valid': viol == 0}


def _dominates(a: Dict, b: Dict) -> bool:
    """a constraint-dominates b"""
    if a['viol'] == 0 and b['viol'] > 0:
        return True
    if a['viol'] > 0:
        return b['viol'] > 0 and a['viol'] < b['viol']
    better = False
    for x, y in zip(a['obj'], b['obj']):
        if x > y:
            return False
        if x < y:
            better = True
    return better


def _nondominated_sort(evals: List[Dict]) -> List[List[int]]:
    n = len(evals)
    dominated_by = [[] for _ in range(n)]
    count = [0] * n
    fronts = [[]]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if _dominates(evals[i], evals[j]):
                dominated_by[i].append(j)
            elif _dominates(evals[j], evals[i]):
                count[i] += 1
        if count[i] == 0:
            fronts[0].append(i)
    k = 0
    while fronts[k]:
        nxt = []
        for i in fronts[k]:
            for j in dominated_by[i]:
                count[j] -= 1
                if count[j] == 0:
                    nxt.append(j)
        k += 1
        fronts.append(nxt)
    return fronts[:-1]


def _crowding(front: List[int], evals: List[Dict]) -> Dict[int, float]:
    dist = {i: 0.0 for i in front}
    if len(front) <= 2:
        return {i: float('inf') for i in front}
    for m in range(3):
        order = sorted(front, key=lambda i: evals[i]['obj'][m])
        lo, hi = evals[order[0]]['obj'][m], evals[order[-1]]['obj'][m]
        dist[order[0]] = dist[order[-1]] = float('inf')
        if hi - lo < 1e-12:
            continue
        for a in range(1, len(order) - 1):
            dist[order[a]] += (evals[order[a + 1]]['obj'][m] - evals[order[a - 1]]['obj'][m]) / (hi - lo)
    return dist


def _repair_final(routes, pois, hotel, budget, scoring_mode):
    """ขั้นสุดท้ายของแต่ละคำตอบใน front: 2-opt, เติมมื้อ, ซ่อมเวลา/งบ (ลำดับเดียวกับ Hybrid)"""
    r = [two_opt_day(day, hotel) for day in routes]
    r = meal_fill(r, pois, hotel, budget, scoring_mode)
    r = _time_repair(r, hotel)
    for _ in range(60):   # ซ่อมงบ (เฉพาะค่าเข้า+ค่าอาหาร): ลบ attraction ที่แพงที่สุดจนอยู่ในงบ
        if sum(p['cost'] for day in r for p in day) <= budget:
            break
        cands = [(d, i, p) for d, day in enumerate(r) for i, p in enumerate(day) if p['category'] != 'restaurant']
        if not cands:
            break
        d, i, _p = max(cands, key=lambda c: (c[2]['cost'], -c[2]['score']))
        r[d] = [p for j, p in enumerate(r[d]) if j != i]
    return meal_fill(r, pois, hotel, budget, scoring_mode)


def nsga2_solve(pois: List[Dict], hotel: Dict, days: int, budget: float, scoring_mode: str = 'quality',
                pop_size: int = 40, generations: int = 40, mutation_rate: float = 0.5,
                seeds: List[List[List[Dict]]] = None) -> List[Dict]:
    """คืนรายการคำตอบบน Pareto front (ผ่านข้อจำกัด) เรียงตามคะแนนมากไปน้อย
    แต่ละรายการ: {'routes', 'score', 'diversity', 'distance_km', 'cost'}"""
    pop = [copy.deepcopy(s) for s in (seeds or [])]
    while len(pop) < pop_size:   # ประชากรเริ่มต้น: greedy หลายแบบ (สุ่มสลับลำดับ + noise ต่างกันเพื่อกระจายคำตอบ)
        shuffled = list(pois)
        random.shuffle(shuffled)
        pop.append(greedy_solve(shuffled, hotel, days, budget, scoring_mode=random.choice(['ratio', 'quality']),
                                random_factor=random.choice([0.05, 0.15, 0.4])))
    evals = [evaluate_objectives(c, hotel, budget) for c in pop]

    for _ in range(generations):
        fronts = _nondominated_sort(evals)
        rank, crowd = {}, {}
        for r, f in enumerate(fronts):
            c = _crowding(f, evals)
            for i in f:
                rank[i], crowd[i] = r, c[i]

        def pick():
            a, b = random.sample(range(len(pop)), 2)
            return a if (rank[a], -crowd[a]) < (rank[b], -crowd[b]) else b

        children = []
        while len(children) < pop_size:
            child = _crossover(pop[pick()], pop[pick()])
            child = _mutate(child, pois, mutation_rate)
            children.append(child)
        cevals = [evaluate_objectives(c, hotel, budget) for c in children]
        allpop, allev = pop + children, evals + cevals
        fronts = _nondominated_sort(allev)
        nxt = []
        for f in fronts:
            if len(nxt) + len(f) <= pop_size:
                nxt += f
            else:
                c = _crowding(f, allev)
                nxt += sorted(f, key=lambda i: -c[i])[:pop_size - len(nxt)]
                break
        pop = [allpop[i] for i in nxt]
        evals = [allev[i] for i in nxt]

    front0 = _nondominated_sort(evals)[0]
    out = []
    for i in front0:
        routes = _repair_final(pop[i], pois, hotel, budget, scoring_mode)
        e = evaluate_objectives(routes, hotel, budget)
        if e['valid']:
            out.append({'routes': routes, 'score': e['score'], 'diversity': e['diversity'],
                        'distance_km': e['distance_km'], 'cost': e['cost'], 'obj': e['obj'], 'viol': 0.0})
    # กรองซ้ำและเหลือเฉพาะ non-dominated หลังซ่อม
    keep = []
    for a in out:
        if not any(_dominates(b, a) for b in out if b is not a):
            if not any(abs(a['score'] - k['score']) < 1e-9 and abs(a['distance_km'] - k['distance_km']) < 1e-6 and abs(a['diversity'] - k['diversity']) < 1e-9 for k in keep):
                keep.append(a)
    return sorted(keep, key=lambda s: -s['score'])


def hypervolume(points: List[tuple], ref: tuple, samples: int = 60000, rng: random.Random = None) -> float:
    """ประมาณ hypervolume (minimization) ด้วย Monte Carlo ภายในกล่อง [min(points), ref]"""
    if not points:
        return 0.0
    rng = rng or random.Random(0)
    lo = [min(p[m] for p in points) for m in range(3)]
    box = 1.0
    for m in range(3):
        box *= max(ref[m] - lo[m], 1e-12)
    hit = 0
    for _ in range(samples):
        q = [rng.uniform(lo[m], ref[m]) for m in range(3)]
        if any(all(p[m] <= q[m] for m in range(3)) for p in points):
            hit += 1
    return box * hit / samples
