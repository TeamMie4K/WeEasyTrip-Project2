# -*- coding: utf-8 -*-
"""ฝึก RL agent ในสภาพแวดล้อมจำลอง (4 จังหวัด × 3 scenarios, seed ฝึก 1000+) แล้วบันทึก theta ที่ algorithm/rl_policy.json"""
import sys, os, json, random, time
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
sys.argv = [sys.argv[0], '15']
import numpy as np
import run_province_experiments as E
import rl

EPISODES = int(os.environ.get('RL_EPISODES', 2400))
envs = []
for prov in E.PROVINCES:
    for sc in E.SCENARIOS:
        pois, hotel, act = E.setup(prov, sc)   # ตั้งโปรไฟล์เดินทางของจังหวัดด้วย
        envs.append((prov, sc, pois, hotel, sc['days'], act))
# หมายเหตุ: โปรไฟล์เดินทางเป็น ContextVar ตั้งตอน setup() ล่าสุดเท่านั้น จึงฝึกทีละ env โดยตั้งโปรไฟล์ใหม่ก่อนทุก episode
from utils import set_travel_profile
cfg = E.PROV_CFG
theta = np.zeros(rl.N_FEATURES)
rng = random.Random(0)
np.random.seed(0)
t0 = time.time()
hist = []
window = []
base = {}
for ep in range(EPISODES):
    prov, sc, pois, hotel, days, act = envs[rng.randrange(len(envs))]
    set_travel_profile(cfg[prov].get('road_factor', 1.0), cfg[prov].get('speed_kmh', 40))
    rec = []
    routes = rl.rl_solve(pois, hotel, days, act, theta, sample=True, record=rec)
    R = rl.episode_reward(routes, hotel, act, days)
    key = (prov, sc['label'])
    base[key] = R if key not in base else 0.95 * base[key] + 0.05 * R
    adv = R - base[key]
    grad = np.zeros(rl.N_FEATURES)
    for phi, idx in rec:
        lg = phi @ theta; lg -= lg.max(); p = np.exp(lg); p /= p.sum()
        grad += phi[idx] - p @ phi
    if rec:
        theta += 0.8 * adv * grad / len(rec)
    window.append(R)
    if (ep + 1) % 300 == 0:
        hist.append(float(np.mean(window))); window = []
        print(ep + 1, 'mean reward', round(hist[-1], 4), 'theta', np.round(theta, 2).tolist(), round(time.time() - t0), 's', flush=True)
json.dump({'theta': theta.tolist(), 'episodes': EPISODES, 'reward_history': hist,
           'features': ['score', 'cost_frac', 'dist', 'wait', 'new_category', 'free', 'time_slack', 'score*(1-cost)', 'score/cost']},
          open(os.path.join(HERE, '..', 'algorithm', 'rl_policy.json'), 'w', encoding='utf-8'), indent=1)
print('saved')
