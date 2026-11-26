# -*- coding: utf-8 -*-
"""
run_preference_cause.py — หาสาเหตุที่ความชอบ (ชอบกิจกรรม/จุดชมวิว) ไม่เพิ่มสัดส่วนอย่างมีนัยสำคัญใน 8 จังหวัดที่มีสถานที่หมวดนั้น 6-10 จุด
ตรวจ 2 สมมติฐาน: (H1) น้ำหนักถ่วง LIKE_BOOST = 1.0 น้อยเกินไปเมื่อเทียบกับช่วงคะแนนสถานที่  (H2) สถานที่ในหมวดที่ชอบมีคะแนนต่ำหรืออยู่ไกลโรงแรม
วิธี: S2, Hybrid+Div, 15 รอบ, LIKE_BOOST = 1.0 (ค่าปัจจุบัน) เทียบ 3.0 และ 5.0; วัดสัดส่วนจุดหมวดที่ชอบ (Wilcoxon ทางเดียวเทียบเงื่อนไขปกติ)
      พร้อมสถิติของสถานที่ในหมวดที่ชอบ: คะแนนเฉลี่ยเทียบสถานที่ท่องเที่ยวทั้งหมด และระยะเฉลี่ยถึงโรงแรมที่ใช้
ผลลัพธ์: results/preference_cause.json
"""
import sys, os, json, random, statistics
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
sys.path.insert(0, os.path.join(HERE, '..', 'backend'))
from scipy import stats as st
import main as api
from utils import evaluate_route, set_travel_profile, haversine_km
from hybrid import hybrid_solve

OUT = os.path.join(HERE, 'results')
PROVS = ['buengkan', 'phangnga', 'phayao', 'phrae', 'prachuapkhirikhan', 'ranong', 'saraburi', 'suratthani']
LIKE = ['activity', 'viewpoint']
SC = {'days': 5, 'budget': 15_000, 'hotel_frac': 0.35, 'mode': 'ratio'}
HY = dict(pop_size=30, generations=60, mutation_rate=0.3)
TRIALS = 15
PREF = api.Preferences(liked=LIKE)


def share(routes):
    a = [p for day in routes for p in day if p['category'] != 'restaurant']
    return (sum(p['category'] in LIKE for p in a) / len(a)) if a else 0.0


def run(prov, boost):
    d = api.DATA[prov]; pv = api.PROVINCES[prov]
    set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
    hs = sorted(d['hotels'], key=lambda h: h['cost']); hotel = hs[int(len(hs) * SC['hotel_frac'])]
    act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
    api.LIKE_BOOST = boost
    base, like = [], []
    for t in range(TRIALS):
        for pref, store in ((None, base), (PREF, like)):
            pool, _ = api.apply_preferences(d['pois'], pref, SC['days'])
            random.seed(t)
            r, _ = hybrid_solve(pool, hotel, SC['days'], act, scoring_mode=SC['mode'], diversity_weight=api.DIVERSITY_WEIGHT, **HY)
            r = api.restore_originals(r, d['poi_by_id'])
            store.append(share(r))
    try:
        p = st.wilcoxon(like, base, alternative='greater').pvalue
    except ValueError:
        p = float('nan')
    return statistics.mean(base), statistics.mean(like), p


res = {}
for prov in PROVS:
    d = api.DATA[prov]
    att = [p for p in d['pois'] if p['category'] != 'restaurant']
    liked = [p for p in att if p['category'] in LIKE]
    hs = sorted(d['hotels'], key=lambda h: h['cost']); hotel = hs[int(len(hs) * SC['hotel_frac'])]
    km = lambda ps: statistics.mean(haversine_km(p['lat'], p['lng'], hotel['lat'], hotel['lng']) for p in ps)
    res[prov] = {'attractions': len(att), 'liked': len(liked),
                 'score_liked': round(statistics.mean(p['score'] for p in liked), 2), 'score_all': round(statistics.mean(p['score'] for p in att), 2),
                 'km_liked': round(km(liked), 1), 'km_all': round(km(att), 1), 'boost': {}}
    for b in (1.0, 3.0, 5.0):
        base, like, p = run(prov, b)
        res[prov]['boost'][str(b)] = {'base': round(base, 3), 'like': round(like, 3), 'p': None if p != p else round(p, 4)}
    print(prov, json.dumps(res[prov], ensure_ascii=False), flush=True)
json.dump(res, open(os.path.join(OUT, 'preference_cause.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
