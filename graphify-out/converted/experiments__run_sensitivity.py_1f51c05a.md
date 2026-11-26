<!-- converted from experiments__run_sensitivity.py.docx -->

คู่มือโค้ด: experiments/run_sensitivity.py
วิเคราะห์ความไวของพารามิเตอร์
ไฟล์ต้นฉบับ: experiments/run_sensitivity.py (82 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ตรวจว่าข้อสรุป "Hybrid ดีกว่า GA และ Greedy" ยังคงอยู่เมื่อเปลี่ยนพารามิเตอร์ที่ผู้พัฒนาเลือกเอง 4 ตัว คือ DIST_WEIGHT (หักคะแนนต่อกิโลเมตร) GREEDY_KM_PENALTY (ค่าปรับกิโลเมตรของ Greedy) TRAFFIC_FACTOR (ตัวคูณเวลาเดินทาง) และ TIME_WEIGHT (หักคะแนนต่อนาที) ปรับทีละตัว ตัวอื่นคงค่าเดิม รันสถานการณ์ S2 บน 4 จังหวัดหลักด้วยกติกาของ ➜ experiments/run_province_experiments.py ผลคือ results/sensitivity_*.json ที่ใช้ในตารางที่ 4.11 ของรายงาน

บรรทัด 1–23  หัวไฟล์ ตารางค่าที่ลอง
1  # -*- coding: utf-8 -*-
2  """
3  run_sensitivity.py — Project 2: วิเคราะห์ความไวของพารามิเตอร์ที่ผู้พัฒนาเลือกเอง
4  พารามิเตอร์: DIST_WEIGHT (หักคะแนนต่อ กม. ใน Hybrid/GA/ILS), GREEDY_KM_PENALTY (บาทต่อ กม. ของ Greedy),
5               TRAFFIC_FACTOR (ตัวคูณเวลาเดินทาง), TIME_WEIGHT (หักคะแนนต่อนาทีของเวลาทั้งวัน)
6  สถานการณ์ S2 (5 วัน 15,000 บาท) 4 จังหวัด; ปรับทีละพารามิเตอร์ ตัวอื่นคงค่าเดิม
7  ตัวชี้วัด: คะแนนเฉลี่ย (ไม่รวมตัวหัก), กม./วัน, ชม./วัน, ผ่านข้อจำกัด+มื้อครบ, Hybrid เทียบ GA (Mann-Whitney ทางเดียว)
8  รัน:  python run_sensitivity.py <dist|greedy|traffic|time> [trials]
9  ผลลัพธ์: results/sensitivity_<name>.json
10  """
11  import sys, os, json, statistics
12  NAME = sys.argv[1]
13  TRIALS = int(sys.argv[2]) if len(sys.argv) > 2 else 8
14  sys.argv = [sys.argv[0], str(TRIALS)]
15  import run_province_experiments as E
16  import hybrid, ils, genetic, greedy, utils
17  from utils import evaluate_route
18  from scipy import stats as st
19
20  SC = E.SCENARIOS[1]
21  GRID = {'dist': [0.0, 0.1, 0.3, 0.6, 1.0], 'greedy': [0.0, 10.0, 30.0, 100.0],
22          'traffic': [1.0, 1.25, 1.5], 'time': [0.0, 0.01, 0.03]}
23  BASE = {'dist': 0.3, 'greedy': 10.0, 'traffic': 1.25, 'time': 0.01}
บรรทัด 1–10: docstring อธิบายพารามิเตอร์ สถานการณ์ ตัวชี้วัด และวิธีรัน (python run_sensitivity.py <dist|greedy|traffic|time> [trials])
บรรทัด 11–14: อ่านชื่อพารามิเตอร์จากอาร์กิวเมนต์แรกและจำนวนรอบจากอาร์กิวเมนต์ที่สอง (ตั้งต้น 8) แล้วตั้ง sys.argv ให้โมดูลหลักอ่านได้
บรรทัด 15–18: นำเข้า ➜ experiments/run_province_experiments.py (ชื่อ E) โมดูลอัลกอริทึมที่จะปรับค่าตัวแปร และ scipy.stats
บรรทัด 20: ใช้สถานการณ์ S2 (5 วัน 15,000 บาท)
บรรทัด 21–22: GRID ค่าที่ลองของแต่ละพารามิเตอร์
บรรทัด 23: BASE ค่าตั้งต้นที่ระบบใช้จริง
บรรทัด 26–46  ตั้งค่าพารามิเตอร์และรันหนึ่งอัลกอริทึม
26  def apply(v):
27      if NAME == 'dist':
28          hybrid.DIST_WEIGHT = ils.DIST_WEIGHT = genetic.DIST_WEIGHT = v
29      elif NAME == 'greedy':
30          greedy.GREEDY_KM_PENALTY = v
31      elif NAME == 'traffic':
32          utils.TRAFFIC_FACTOR = v
33      else:
34          utils.TIME_WEIGHT = v
35
36
37  def one(prov, algo):
38      pois, hotel, act = E.setup(prov, SC)
39      n = 1 if algo == 'Greedy' else TRIALS
40      rows = []
41      for t in range(n):
42          routes, m = E.run_algo(algo, pois, hotel, SC['days'], act, SC['mode'], seed=t)
43          ev = evaluate_route(routes, hotel, act)
44          hrs = statistics.mean(d['time_min'] for d in ev['days_detail']) / 60
45          rows.append({**m, 'hours_day': hrs, 'ok': m['valid'] and m['meals_ok']})
46      return rows
บรรทัด 26–34: apply ตั้งค่าตัวแปรของโมดูลที่เกี่ยวข้อง dist ตั้งทั้ง hybrid ils genetic ส่วนอีกสามพารามิเตอร์ตั้งที่ greedy หรือ utils
บรรทัด 37–46: one รันอัลกอริทึมหนึ่งตัวบนหนึ่งจังหวัด (Greedy ครั้งเดียว ที่เหลือตามจำนวนรอบ) วัดคะแนน ชั่วโมงต่อวันจาก ➜ evaluate_route() ใน algorithm/utils.py และธงผ่านข้อจำกัดพร้อมมื้อครบ
บรรทัด 49–78  วนทุกค่าและบันทึกผล
49  def main():
50      res = {}
51      for v in GRID[NAME]:
52          apply(v)
53          cell = {}
54          for algo in ('Greedy', 'GA', 'Hybrid'):
55              if NAME == 'greedy' and algo != 'Greedy':
56                  continue
57              per, allrows = {}, []
58              for prov in E.PROVINCES:
59                  rows = one(prov, algo)
60                  per[prov] = [r['score'] for r in rows]
61                  allrows += rows
62              cell[algo] = {'score': statistics.mean(r['score'] for r in allrows),
63                            'km_day': statistics.mean(r['km_day'] for r in allrows),
64                            'hours_day': statistics.mean(r['hours_day'] for r in allrows),
65                            'ok': sum(r['ok'] for r in allrows), 'n': len(allrows),
66                            'per_prov': {p: statistics.mean(x) for p, x in per.items()}, 'raw': per}
67          if 'GA' in cell:
68              h = [s for p in E.PROVINCES for s in cell['Hybrid']['raw'][p]]
69              g = [s for p in E.PROVINCES for s in cell['GA']['raw'][p]]
70              cell['hybrid_vs_ga_p'] = float(st.mannwhitneyu(h, g, alternative='greater').pvalue)
71          for a in cell:
72              if isinstance(cell[a], dict):
73                  cell[a].pop('raw', None)
74          res[str(v)] = cell
75          print(NAME, v, json.dumps({a: (round(c['score'], 1), round(c['km_day'], 1), round(c['hours_day'], 1)) for a, c in cell.items() if isinstance(c, dict)}),
76                cell.get('hybrid_vs_ga_p'), flush=True)
77          json.dump({'param': NAME, 'base': BASE[NAME], 'trials': TRIALS, 'scenario': SC['label'], 'results': res},
78                    open(os.path.join(E.OUT_DIR, f'sensitivity_{NAME}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
บรรทัด 49–56: วนทุกค่าใน GRID ตั้งค่า แล้วรัน Greedy GA และ Hybrid (กรณี greedy รันเฉพาะ Greedy เพราะพารามิเตอร์ไม่กระทบอัลกอริทึมอื่น)
บรรทัด 57–66: รวมคะแนนจากทุกจังหวัด สรุปคะแนนเฉลี่ย กิโลเมตรต่อวัน ชั่วโมงต่อวัน จำนวนแผนที่ผ่าน และคะแนนรายจังหวัด
บรรทัด 67–70: ทดสอบ Mann-Whitney ทางเดียวว่า Hybrid สูงกว่า GA หรือไม่ (รวมทุกจังหวัด)
บรรทัด 71–76: ตัดข้อมูลดิบออกก่อนบันทึก แล้วพิมพ์สรุปบรรทัดเดียว
บรรทัด 77–78: เขียน sensitivity_<ชื่อ>.json ทุกครั้งที่จบหนึ่งค่า (ถ้าหยุดกลางคันยังเหลือผลบางส่วน)
บรรทัด 81–82  จุดเริ่มต้น
81  if __name__ == '__main__':
82      main()
บรรทัด 81–82: เรียก main

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/utils.py
experiments/run_province_experiments.py