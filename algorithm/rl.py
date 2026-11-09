# -*- coding: utf-8 -*-
"""
rl.py - Reinforcement Learning agent สำหรับสร้างแผนเริ่มต้น (แทน Greedy seed)

ปัญหาแบบ sequential decision: ในแต่ละ slot ของวัน (attr, attr, lunch, attr, attr, dinner)
agent เลือก 1 สถานที่จากรายการ candidate ที่ผ่านข้อจำกัด (เวลาเปิด-ปิด งบ เวลาต่อวัน) แล้วเดินต่อ
policy: softmax เชิงเส้น  pi(a|s) ∝ exp(theta · phi(s,a))
ฝึกด้วย REINFORCE (baseline = ค่าเฉลี่ยรางวัลของ scenario) ใน "สภาพแวดล้อมจำลอง" (ตัวอัลกอริทึมเอง)
รางวัล = คะแนนรวมของแผนที่ผ่านข้อจำกัด (ลบเมื่อเกินงบ/ผิดเวลา) — ไม่ใช้ประวัติผู้ใช้จริง เพราะระบบยังไม่มีข้อมูลนั้น
"""
import math
import random
from typing import Dict, List, Tuple

import numpy as np

from utils import haversine_km, travel_cost, DAY_TIME_BUDGET, DAY_START_MIN, evaluate_route
from utils import MAX_SIGHT_MIN
from greedy import (_find_best_for_slot, DAY_PATTERN, LUNCH_TRIGGER, DINNER_TRIGGER, DINNER_BUFFER_MIN)

N_FEATURES = 9


def features(cands: List[tuple], budget_left: float) -> np.ndarray:
    """เมทริกซ์ลักษณะเฉพาะ (n_candidates x N_FEATURES) ของ candidate ที่ _find_best_for_slot ส่งมา"""
    rows = []
    for (_s, poi, d_to, arrive, add_cost, slack, wait, cat_count) in cands:
        frac = min(add_cost / (budget_left + 1.0), 1.0)
        rows.append([
            poi['score'] / 10.0,
            frac,
            min(d_to / 20.0, 2.0),
            min(wait / 60.0, 1.0),
            1.0 if cat_count == 0 else 0.0,
            1.0 if poi['cost'] == 0 else 0.0,
            max(min(slack / DAY_TIME_BUDGET, 1.0), 0.0),
            (poi['score'] / 10.0) * (1.0 - frac),
            min((poi['score'] / (add_cost + 80.0)) * 100.0, 5.0) / 5.0,
        ])
    return np.array(rows, dtype=float)


def rl_solve(pois: List[Dict], hotel: Dict, days: int, budget: float, theta: np.ndarray,
             day_time: float = DAY_TIME_BUDGET, sample: bool = True, temperature: float = 1.0,
             record: list = None) -> List[List[Dict]]:
    """สร้างแผนด้วย policy (sample=False → เลือกค่าสูงสุดแบบ deterministic)
    record: ถ้าส่ง list มา จะเก็บ (phi, chosen_index) ของทุกการตัดสินใจไว้ใช้ฝึก"""
    used_ids = set()
    remaining = float(budget)
    routes = [[] for _ in range(days)]
    per_day_budget = (budget / max(days, 1)) * 1.1
    state = {'budget_left': remaining}

    def chooser(cands):
        phi = features(cands, state['budget_left'])
        logits = phi @ theta / max(temperature, 1e-6)
        logits -= logits.max()
        p = np.exp(logits)
        p /= p.sum()
        idx = int(np.random.choice(len(p), p=p)) if sample else int(np.argmax(p))
        if record is not None:
            record.append((phi, idx))
        return idx

    for day_idx in range(days):
        pos, t = hotel, float(DAY_START_MIN)
        cats = {}
        day_left = min(per_day_budget, remaining)
        past_lunch = dinner_done = False
        sight_left = MAX_SIGHT_MIN
        for slot in DAY_PATTERN:
            if slot == 'lunch' and t < LUNCH_TRIGGER:
                t = float(LUNCH_TRIGGER)
            elif slot == 'dinner' and t < DINNER_TRIGGER:
                t = float(DINNER_TRIGGER)
            db = DINNER_BUFFER_MIN if (slot == 'attr' and past_lunch and not dinner_done) else 0
            state['budget_left'] = day_left
            res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, day_left, cats, slot,
                                      dinner_buffer=db, chooser=chooser, sight_left=sight_left)
            if res is None and slot in ('lunch', 'dinner'):          # fallback เหมือน Greedy: มื้อเป็น hard requirement
                state['budget_left'] = max(300.0, remaining * 0.5)
                res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, state['budget_left'], cats, slot, chooser=chooser, sight_left=sight_left)
            if res is None and slot in ('lunch', 'dinner'):
                state['budget_left'] = 1e9
                res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, 1e9, cats, slot, chooser=chooser, sight_left=sight_left)
            if res is None and slot in ('lunch', 'dinner'):
                res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, 1e9, cats, slot, chooser=chooser, relax_meal=True, sight_left=sight_left)
            if res is None:
                state['budget_left'] = 1e9
                res = _find_best_for_slot(pois, used_ids, pos, t, hotel, day_time, 1e9, cats, slot,
                                          free_only=True, dinner_buffer=db, chooser=chooser, sight_left=sight_left)
            if slot == 'lunch':
                past_lunch = True
            if slot == 'dinner':
                dinner_done = True
            if res is None:
                continue
            poi, d_to, arrive = res
            used_ids.add(poi['id'])
            routes[day_idx].append(poi)
            if poi['category'] != 'restaurant': sight_left -= poi['duration_min']
            t = arrive + poi['duration_min']
            pos = poi
            spent = travel_cost(d_to) + poi['cost']
            remaining -= spent
            day_left = max(0.0, day_left - spent)
            cats[poi['category']] = cats.get(poi['category'], 0) + 1
        if routes[day_idx]:
            remaining -= travel_cost(haversine_km(pos['lat'], pos['lng'], hotel['lat'], hotel['lng']))
    return routes


def episode_reward(routes, hotel, budget, days) -> float:
    """รางวัล = คะแนนรวมต่อวัน (ปรับสเกล) ลบโทษเมื่อผิดข้อจำกัด"""
    ev = evaluate_route(routes, hotel, budget)
    r = ev['total_score'] / max(days, 1) / 10.0
    if not ev['valid']:
        r -= 0.5 * len(ev['violations'])
    return r


def train(envs: List[tuple], episodes: int = 1500, lr: float = 0.08, seed: int = 0,
          theta0: np.ndarray = None, log_every: int = 250) -> Tuple[np.ndarray, List[float]]:
    """ฝึก policy ด้วย REINFORCE
    envs: รายการ (pois, hotel, days, budget) — สุ่มหนึ่ง env ต่อ episode; baseline แยกตาม env
    คืน (theta, ประวัติรางวัลเฉลี่ยทุก log_every episodes)"""
    rng = random.Random(seed)
    np.random.seed(seed)
    theta = np.zeros(N_FEATURES) if theta0 is None else theta0.copy()
    baseline = [None] * len(envs)
    hist, window = [], []
    for ep in range(episodes):
        i = rng.randrange(len(envs))
        pois, hotel, days, budget = envs[i]
        rec = []
        routes = rl_solve(pois, hotel, days, budget, theta, sample=True, record=rec)
        R = episode_reward(routes, hotel, budget, days)
        baseline[i] = R if baseline[i] is None else 0.95 * baseline[i] + 0.05 * R
        adv = R - baseline[i]
        grad = np.zeros(N_FEATURES)
        for phi, idx in rec:
            logits = phi @ theta
            logits -= logits.max()
            p = np.exp(logits)
            p /= p.sum()
            grad += phi[idx] - p @ phi
        if rec:
            theta += lr * adv * grad / len(rec) * 10.0
        window.append(R)
        if (ep + 1) % log_every == 0:
            hist.append(float(np.mean(window)))
            window = []
    return theta, hist
