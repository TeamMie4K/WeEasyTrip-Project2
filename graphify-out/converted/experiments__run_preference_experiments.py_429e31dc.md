<!-- converted from experiments__run_preference_experiments.py.docx -->

คู่มือโค้ด: experiments/run_preference_experiments.py
การทดลองความชอบของผู้ใช้ (เฟส 3)
ไฟล์ต้นฉบับ: experiments/run_preference_experiments.py (88 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: วัดว่าการเลือก "ชอบ" และ "ไม่เอา" หมวดสถานที่ส่งผลต่อแผนที่ Hybrid+Div สร้างอย่างไร ในสถานการณ์ S2 (5 วัน 15,000 บาท) ใช้ตัวช่วย apply_preferences และ restore_originals ตัวเดียวกับเซิร์ฟเวอร์ใน ➜ apply_preferences() ใน backend/main.py ผลคือตาราง 4.5 ในรายงาน ไฟล์นี้วนทุกจังหวัดที่เซิร์ฟเวอร์โหลด (รวม 78 ชุดข้อมูล) ตารางในรายงานแสดงเฉพาะ 16 จังหวัดแรก

บรรทัด 1–28  หัวไฟล์ นำเข้า และเงื่อนไขทดลอง
1  # -*- coding: utf-8 -*-
2  """
3  run_preference_experiments.py — WeEasyTrip Project 2 เฟส 3 (User Preference)
4  วัดผลของความชอบต่อแผนที่ Hybrid+Div สร้าง: 4 จังหวัด × scenario S2 × 15 รอบ (seed เดียวกันทุกเงื่อนไข)
5  เงื่อนไข: baseline | avoid{temple,market} | like{activity,viewpoint} | like+avoid
6  ตัวชี้วัด: จำนวนจุดหมวดที่ไม่เอา (ต้อง 0), สัดส่วนจุดหมวดที่ชอบ, คะแนนจริง (ไม่รวมตัวถ่วง), ผ่านข้อจำกัด, มื้อครบ
7  ผลลัพธ์: results/preference_results.json, results/preference_stats.txt
8  """
9  import sys, os, json, random, statistics
10  HERE = os.path.dirname(__file__)
11  sys.path.insert(0, os.path.join(HERE, '..', 'algorithm'))
12  sys.path.insert(0, os.path.join(HERE, '..', 'backend'))
13  from scipy import stats as st
14  import main as api                      # ใช้ apply_preferences / restore_originals ตัวเดียวกับ backend
15  from utils import evaluate_route, set_travel_profile
16  from hybrid import hybrid_solve
17
18  OUT = os.path.join(HERE, 'results')
19  TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 15
20  SC = {'days': 5, 'budget': 15_000, 'hotel_frac': 0.35, 'mode': 'ratio'}
21  LIKE, AVOID = ['activity', 'viewpoint'], ['temple', 'market']
22  CONDS = {
23      'baseline':   None,
24      'avoid':      api.Preferences(avoided=AVOID),
25      'like':       api.Preferences(liked=LIKE),
26      'like+avoid': api.Preferences(liked=LIKE, avoided=AVOID),
27  }
28  HYBRID = dict(pop_size=30, generations=60, mutation_rate=0.3)
บรรทัด 1–7: docstring: เงื่อนไข 4 แบบ (baseline, avoid, like, like+avoid) และตัวชี้วัด (จำนวนจุดหมวดที่ไม่เอา ซึ่งต้องเป็น 0 สัดส่วนจุดหมวดที่ชอบ และคะแนนจริง)
บรรทัด 9: นำเข้าโมดูลมาตรฐาน
บรรทัด 10–12: เพิ่มโฟลเดอร์ algorithm/ และ backend/ เข้า path
บรรทัด 13: นำเข้า scipy.stats
บรรทัด 14: นำเข้า ➜ backend/main.py ในชื่อ api (โหลดข้อมูลทุกจังหวัดและให้ apply_preferences restore_originals Preferences)
บรรทัด 15–16: นำเข้า ➜ evaluate_route() ใน algorithm/utils.py ➜ set_travel_profile() ใน algorithm/utils.py และ ➜ hybrid_solve() ใน algorithm/hybrid.py
บรรทัด 18–19: โฟลเดอร์ผลลัพธ์ และจำนวนรอบ (ตั้งต้น 15)
บรรทัด 20: SC สถานการณ์ S2
บรรทัด 21: LIKE (กิจกรรม จุดชมวิว) และ AVOID (วัด ตลาด)
บรรทัด 22–27: CONDS ความชอบของแต่ละเงื่อนไขเป็นวัตถุ Preferences
บรรทัด 28: พารามิเตอร์ Hybrid
บรรทัด 31–53  รันหนึ่งจังหวัด
31  def run(prov):
32      d = api.DATA[prov]
33      pv = api.PROVINCES[prov]
34      set_travel_profile(pv.get('road_factor', 1.0), pv.get('speed_kmh', 40))
35      hs = sorted(d['hotels'], key=lambda h: h['cost'])
36      hotel = hs[int(len(hs) * SC['hotel_frac'])]
37      act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
38      rows = {c: [] for c in CONDS}
39      for t in range(TRIALS):
40          for name, pref in CONDS.items():
41              pool, _ = api.apply_preferences(d['pois'], pref, SC['days'])
42              random.seed(t)
43              routes, _ = hybrid_solve(pool, hotel, SC['days'], act, scoring_mode=SC['mode'],
44                                       diversity_weight=api.DIVERSITY_WEIGHT, **HYBRID)
45              routes = api.restore_originals(routes, d['poi_by_id'])
46              ev = evaluate_route(routes, hotel, act)
47              pois = [p for day in routes for p in day if p['category'] != 'restaurant']
48              rows[name].append({
49                  'avoided': sum(p['category'] in AVOID for p in pois),
50                  'liked_share': (sum(p['category'] in LIKE for p in pois) / len(pois)) if pois else 0.0,
51                  'score': ev['total_score'], 'valid': ev['valid'],
52                  'meals': all(sum(1 for p in day if p['category'] == 'restaurant') >= 2 for day in routes if day)})
53      return rows
บรรทัด 31–34: ประกาศ run ดึงข้อมูลจังหวัดจาก api.DATA และตั้งโปรไฟล์เดินทาง
บรรทัด 35–37: เลือกโรงแรมตามตำแหน่งในรายการเรียงราคา และคำนวณงบกิจกรรม
บรรทัด 38: ตัวเก็บผลแยกตามเงื่อนไข
บรรทัด 39–41: วนทุกรอบ ทุกเงื่อนไข ปรับกลุ่มจุดตามความชอบด้วย ➜ apply_preferences() ใน backend/main.py
บรรทัด 42–44: ตั้ง seed เดียวกันทุกเงื่อนไข และรัน Hybrid พร้อมน้ำหนักความหลากหลายของเซิร์ฟเวอร์
บรรทัด 45: คืนวัตถุต้นฉบับเพื่อให้คะแนนเป็นคะแนนจริง
บรรทัด 46–47: ประเมินแผนและเก็บเฉพาะที่เที่ยว
บรรทัด 48–52: บันทึกจำนวนจุดหมวดที่ไม่เอา สัดส่วนจุดหมวดที่ชอบ คะแนน ความถูกต้อง และมื้อครบหรือไม่
บรรทัด 53: คืนผล
บรรทัด 56–88  ลูปจังหวัดและบันทึกผล
56  def main_():
57      res, lines = {}, ['=' * 96, f'PREFERENCE EXPERIMENTS — Hybrid+Div, S2 (5 days, 15,000 THB), trials={TRIALS}', '=' * 96,
58                        f"{'Province':<11}{'Condition':<12}{'avoided#':>9}{'liked%':>8}{'score':>8}{'Δscore%':>9}{'valid':>7}{'meals':>7}{'p(score)':>10}{'p(liked)':>10}"]
59      for prov in api.DATA:
60          rows = run(prov)
61          base = [r['score'] for r in rows['baseline']]
62          bl = [r['liked_share'] for r in rows['baseline']]
63          res[prov] = {}
64          for name, rs in rows.items():
65              sc = [r['score'] for r in rs]
66              try:
67                  p_sc = st.wilcoxon(sc, base).pvalue if name != 'baseline' else float('nan')
68                  p_lk = st.wilcoxon([r['liked_share'] for r in rs], bl, alternative='greater').pvalue if 'like' in name else float('nan')
69              except ValueError:
70                  p_sc = p_lk = float('nan')
71              m = {'avoided_mean': statistics.mean(r['avoided'] for r in rs),
72                   'liked_share': statistics.mean(r['liked_share'] for r in rs),
73                   'score': statistics.mean(sc), 'delta_pct': 100 * (statistics.mean(sc) - statistics.mean(base)) / statistics.mean(base),
74                   'valid': sum(r['valid'] for r in rs), 'meals': sum(r['meals'] for r in rs), 'n': len(rs),
75                   'p_score': p_sc, 'p_liked': p_lk}
76              res[prov][name] = m
77              lines.append(f"{prov:<11}{name:<12}{m['avoided_mean']:>9.2f}{100*m['liked_share']:>8.1f}{m['score']:>8.1f}{m['delta_pct']:>9.1f}"
78                           f"{str(m['valid'])+'/'+str(m['n']):>7}{str(m['meals'])+'/'+str(m['n']):>7}{p_sc:>10.4f}{p_lk:>10.4f}")
79          print(prov, 'done', flush=True)
80      json.dump({'trials': TRIALS, 'like': LIKE, 'avoid': AVOID, 'results': res},
81                open(os.path.join(OUT, 'preference_results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
82      txt = '\n'.join(lines)
83      open(os.path.join(OUT, 'preference_stats.txt'), 'w', encoding='utf-8').write(txt)
84      print(txt)
85
86
87  if __name__ == '__main__':
88      main_()
บรรทัด 56–58: ประกาศ main_ และหัวตาราง
บรรทัด 59–63: วนทุกจังหวัด รันและเตรียมค่าฐาน (baseline)
บรรทัด 64–70: ทุกเงื่อนไข ทดสอบ Wilcoxon ของคะแนนเทียบ baseline และของสัดส่วนหมวดที่ชอบ (ทางเดียว) ถ้าทดสอบไม่ได้ให้ nan
บรรทัด 71–76: สรุปค่าเฉลี่ย ร้อยละที่เปลี่ยนของคะแนน จำนวนผ่าน และค่า p
บรรทัด 77–78: เพิ่มบรรทัดผลลงตาราง
บรรทัด 79: พิมพ์ว่าจังหวัดนั้นเสร็จ
บรรทัด 80–81: เขียน results/preference_results.json
บรรทัด 82–84: เขียน preference_stats.txt และพิมพ์ ซึ่งใช้เติมตาราง 4.5
บรรทัด 87–88: เรียก main_() เมื่อรันไฟล์ตรง ๆ

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/hybrid.py
algorithm/utils.py
backend/main.py