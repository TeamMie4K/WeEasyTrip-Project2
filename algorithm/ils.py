# -*- coding: utf-8 -*-
"""
ils.py - Insertion local search (Iterated Local Search) สำหรับปรับปรุงแผนที่ Hybrid สร้างแล้ว

(1) แทนที่สถานที่ในแต่ละช่องด้วยสถานที่ที่ยังไม่ได้ใช้ (หมวดเดียวกัน: attraction หรือร้านอาหาร)
    ถ้า objective ดีขึ้นโดยผ่านข้อจำกัด (เวลาต่อวัน เวลาปิด) และไม่เกินงบ
(2) เติมช่อง attraction ที่ว่าง (วันที่มี < 4 จุด) ที่ตำแหน่งดีที่สุด
(3) shake: แทนที่ 2 จุดแบบสุ่ม แล้ว local search ซ้ำ เก็บแผนที่ดีที่สุด
โครงสร้างวัน: <= 4 attraction, 2 มื้อ (6 จุด/วัน) — วิธีมาตรฐานของ TOPTW ที่ GA ที่สุ่มสลับไม่ได้ทำอย่างเป็นระบบ
"""
import random
from typing import Dict, List

import utils
from utils import evaluate_route, MAX_ATTRS

DIST_WEIGHT = 0.03   # ต้องตรงกับ hybrid.DIST_WEIGHT
IDLE_WEIGHT = 0.02   # ต้องตรงกับค่า idle ใน hybrid._fitness


def day_objective(day: List[Dict], hotel: Dict, diversity_weight: float):
    """(objective, cost) ของแผน 1 วัน หรือ None ถ้าไม่ผ่านข้อจำกัด"""
    ev = evaluate_route([day], hotel, float('inf'))
    if not ev['valid']:
        return None
    det = ev['days_detail'][0]
    # หมายเหตุ: ไม่บังคับช่วงเวลามื้อ เพราะแผนที่ Hybrid/GA สร้างไม่ได้บังคับ (ตรงกับนิยามความถูกต้องของ evaluate_route)
    obj = det['score']
    if diversity_weight:
        cats = [p['category'] for p in day if p['category'] != 'restaurant']
        if cats:
            counts = {c: cats.count(c) for c in set(cats)}
            obj += diversity_weight * ((len(counts) - 1) - sum(max(0, n - 2) for n in counts.values()))
    return obj - DIST_WEIGHT * det['distance_km'] - IDLE_WEIGHT * det['idle_min'] - utils.TIME_WEIGHT * det['time_min'], det['cost']


def _has_room(day, hotel):
    """เพิ่มจุดได้ถ้ายังไม่ถึง MAX_ATTRS (เที่ยว 4 จุด/วัน) — ไม่ยืดเกินเพดาน ใช้การสลับจุดให้คุ้มขึ้นแทน"""
    return sum(1 for p in day if p['category'] != 'restaurant') < MAX_ATTRS


def insertion_local_search(routes: List[List[Dict]], pois: List[Dict], hotel: Dict, budget: float,
                           diversity_weight: float = 0.0, locked=(), shakes: int = 8, top_k: int = 40) -> List[List[Dict]]:
    locked = set(locked)
    cur = [list(d) for d in routes]
    base = [day_objective(d, hotel, diversity_weight) if d else (0.0, 0.0) for d in cur]
    if any(b is None for b in base):
        return routes                        # แผนเริ่มต้นไม่ผ่านเงื่อนไขของ ILS — ไม่แตะ
    objs = [b[0] for b in base]
    costs = [b[1] for b in base]
    used = {p['id'] for d in cur for p in d}
    by_score = sorted(pois, key=lambda p: -p['score'])
    unused = {'attr': [p for p in by_score if p['category'] != 'restaurant' and p['id'] not in used],
              'rest': [p for p in by_score if p['category'] == 'restaurant' and p['id'] not in used]}

    def kind(p):
        return 'rest' if p['category'] == 'restaurant' else 'attr'

    def local_search():
        improved = True
        while improved:
            improved = False
            order = list(range(len(cur)))
            random.shuffle(order)
            for d in order:
                day = cur[d]
                for i in range(len(day)):
                    a = day[i]
                    if a['id'] in locked:
                        continue
                    best = None
                    for u in unused[kind(a)][:top_k]:
                        trial = day[:i] + [u] + day[i + 1:]
                        r = day_objective(trial, hotel, diversity_weight)
                        if r is None or sum(costs) - costs[d] + r[1] > budget:
                            continue
                        gain = r[0] - objs[d]
                        if gain > 1e-9 and (best is None or gain > best[0]):
                            best = (gain, u, trial, r)
                    if best:
                        _g, u, trial, r = best
                        unused[kind(a)].remove(u)
                        unused[kind(a)].append(a)
                        unused[kind(a)].sort(key=lambda p: -p['score'])
                        cur[d] = trial
                        day = trial
                        objs[d], costs[d] = r
                        improved = True
                if day and _has_room(day, hotel):
                    best = None
                    for u in unused['attr'][:top_k]:
                        for j in range(len(day) + 1):
                            trial = day[:j] + [u] + day[j:]
                            r = day_objective(trial, hotel, diversity_weight)
                            if r is None or sum(costs) - costs[d] + r[1] > budget:
                                continue
                            gain = r[0] - objs[d]
                            if gain > 1e-9 and (best is None or gain > best[0]):
                                best = (gain, u, trial, r)
                    if best:
                        _g, u, trial, r = best
                        unused['attr'].remove(u)
                        cur[d] = trial
                        objs[d], costs[d] = r
                        improved = True

    def snapshot():
        return ([list(d) for d in cur], list(objs), list(costs), {k: list(v) for k, v in unused.items()})

    local_search()
    best_state = snapshot()
    for _ in range(shakes):
        for _k in range(2):
            cand = [(d, i) for d, day in enumerate(cur) for i, p in enumerate(day)
                    if p['category'] != 'restaurant' and p['id'] not in locked]
            if not cand or not unused['attr']:
                break
            d, i = random.choice(cand)
            u = random.choice(unused['attr'][:top_k * 2])
            trial = cur[d][:i] + [u] + cur[d][i + 1:]
            r = day_objective(trial, hotel, diversity_weight)
            if r is None or sum(costs) - costs[d] + r[1] > budget:
                continue
            a = cur[d][i]
            unused['attr'].remove(u)
            unused['attr'].append(a)
            unused['attr'].sort(key=lambda p: -p['score'])
            cur[d] = trial
            objs[d], costs[d] = r
        local_search()
        if sum(objs) > sum(best_state[1]) + 1e-9:
            best_state = snapshot()
        else:                                # ไม่ดีขึ้น: กลับไปแผนที่ดีที่สุด
            cur = [list(d) for d in best_state[0]]
            objs, costs = list(best_state[1]), list(best_state[2])
            unused = {k: list(v) for k, v in best_state[3].items()}
    return best_state[0]
