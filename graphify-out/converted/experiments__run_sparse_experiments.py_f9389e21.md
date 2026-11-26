<!-- converted from experiments__run_sparse_experiments.py.docx -->

คู่มือโค้ด: experiments/run_sparse_experiments.py
การทดลองจังหวัดข้อมูลน้อย (sparse) และทริปข้ามจังหวัด
ไฟล์ต้นฉบับ: experiments/run_sparse_experiments.py (62 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ทดสอบ Greedy GA และ Hybrid บนจังหวัดที่ข้อมูลน้อย 8 จังหวัดและทริปข้ามจังหวัด 4 คู่ ด้วยกติกาและพารามิเตอร์เดียวกับ ➜ experiments/run_province_experiments.py เลือกสถานการณ์ด้วยตัวแปรแวดล้อม SC_IDX (0=S1 1=S2 2=S3) ผลใช้เขียนส่วนจังหวัดข้อมูลน้อยในบทที่ 4 และ 5 ของรายงาน

บรรทัด 1–20  หัวไฟล์ ค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  run_sparse_experiments.py — WeEasyTrip Project 2
4  ทดลอง Greedy / GA / Hybrid (1) บนจังหวัดข้อมูลน้อย (sparse) และ (2) บนทริปข้ามจังหวัดข้างเคียง (รวมข้อมูลหลายจังหวัด)
5  ใช้ฟังก์ชันจาก run_province_experiments.py (กติกาและพารามิเตอร์เดียวกัน) — สถานการณ์ S1 (3 วัน 10,000 บาท)
6  ผลลัพธ์: results/sparse_results.json, results/sparse_stats.txt
7  รัน:  python run_sparse_experiments.py [trials]
8  """
9  import sys, os, json, statistics
10  sys.argv = [sys.argv[0]] + sys.argv[1:2]      # ให้ run_province_experiments อ่าน trials จาก argv[1] เท่านั้น
11  import run_province_experiments as R
12  from utils import load_data, set_travel_profile
13  from scipy import stats as st
14
15  TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 10
16  SPARSE = ['nongbualamphu', 'phichit', 'lamphun', 'nakhonnayok', 'singburi', 'kalasin', 'chaiyaphum', 'loei']
17  COMBOS = [('chiangmai', 'lamphun'), ('bangkok', 'nonthaburi'), ('phuket', 'phangnga'), ('phuket', 'krabi')]
18  SC = R.SCENARIOS[int(os.environ.get('SC_IDX', 0))]
19  SUF = '' if SC is R.SCENARIOS[0] else '_' + SC['label'].split('_')[0]
20  R.TRIALS = TRIALS
บรรทัด 1–8: docstring อธิบายการทดลองและที่เก็บผล (sparse_results*.json และ sparse_stats*.txt)
บรรทัด 9: นำเข้าโมดูลมาตรฐาน
บรรทัด 10: ตัด sys.argv ให้โมดูลทดลองหลักอ่านจำนวนรอบจากอาร์กิวเมนต์แรกเท่านั้น
บรรทัด 11–13: นำเข้า ➜ experiments/run_province_experiments.py (ในชื่อ R) ➜ load_data() ใน algorithm/utils.py และ ➜ set_travel_profile() ใน algorithm/utils.py และ scipy.stats
บรรทัด 15: TRIALS จำนวนรอบ (ตั้งต้น 10)
บรรทัด 16: SPARSE รายชื่อจังหวัดข้อมูลน้อย 8 จังหวัด
บรรทัด 17: COMBOS คู่จังหวัดข้างเคียงสำหรับทริปข้ามจังหวัด
บรรทัด 18: เลือกสถานการณ์จาก SC_IDX
บรรทัด 19: ต่อท้ายชื่อไฟล์ผลลัพธ์ (ว่างสำหรับ S1 หรือ _S2 _S3)
บรรทัด 20: ตั้งจำนวนรอบให้โมดูลหลัก
บรรทัด 23–32  โหลดข้อมูลจังหวัดหรือคู่จังหวัด
23  def load(slug):
24      parts = slug.split('+')
25      pois, hotels = [], []
26      for s in parts:
27          p, h = load_data(os.path.join(R.ROOT, 'data', 'provinces', f'{s}.json'))
28          pre = (lambda x: {**x, 'id': f'{s}.{x["id"]}'}) if len(parts) > 1 else (lambda x: x)
29          pois += [pre(x) for x in p]; hotels += [pre(x) for x in h]
30      cfg = R.PROV_CFG[parts[0]]
31      set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
32      return pois, hotels
บรรทัด 23–27: load รับ slug เดี่ยวหรือ a+b โหลดข้อมูลของแต่ละจังหวัด
บรรทัด 28–29: ถ้าเป็นหลายจังหวัด ใส่คำนำหน้า id ของแต่ละจังหวัดเพื่อไม่ให้ id ซ้ำ (เหมือน _combo ใน ➜ get_province() ใน backend/main.py)
บรรทัด 30–31: ตั้งโปรไฟล์เดินทางจากจังหวัดแรกของคู่
บรรทัด 32: คืนจุดและโรงแรม
บรรทัด 35–48  รันหนึ่งพื้นที่
35  def run(slug):
36      pois, hotels = load(slug)
37      hs = sorted(hotels, key=lambda h: h['cost'])
38      hotel = hs[int(len(hs) * SC['hotel_frac'])]
39      act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
40      out, groups = {'pois': len(pois), 'hotels': len(hotels), 'restaurants': sum(p['category'] == 'restaurant' for p in pois)}, {}
41      for algo in ('Greedy', 'GA', 'Hybrid'):
42          n = 1 if algo == 'Greedy' else TRIALS
43          tr = [R.run_algo(algo, pois, hotel, SC['days'], act, SC['mode'], seed=t)[1] for t in range(n)]
44          groups[algo] = [t['score'] for t in tr]
45          out[algo] = {'n': n, 'score': R.summarize(groups[algo]), 'time_ms': R.summarize([t['time_ms'] for t in tr])['mean'],
46                       'valid': sum(t['valid'] for t in tr), 'meals_ok': sum(t['meals_ok'] for t in tr), 'km_day': round(statistics.mean(t['km_day'] for t in tr), 1)}
47      out['hybrid_vs_ga_p'] = float(st.mannwhitneyu(groups['Hybrid'], groups['GA'], alternative='greater').pvalue)
48      return out
บรรทัด 35–39: ประกาศ run โหลดข้อมูล เลือกโรงแรมตามตำแหน่งของสถานการณ์ และคำนวณงบกิจกรรม
บรรทัด 40: เตรียมผลลัพธ์พร้อมจำนวนจุด โรงแรม และร้านอาหาร
บรรทัด 41–46: รันทั้งสามอัลกอริทึมด้วย R.run_algo (Greedy ครั้งเดียว) สรุปคะแนน เวลา จำนวนที่ผ่าน มื้อครบ และระยะขับ
บรรทัด 47: ทดสอบ Mann-Whitney ทางเดียว (Hybrid มากกว่า GA)
บรรทัด 48: คืนผล
บรรทัด 51–62  จุดเริ่มต้นและบันทึกผล
51  if __name__ == '__main__':
52      res = {}
53      for slug in SPARSE + ['+'.join(c) for c in COMBOS]:
54          res[slug] = run(slug)
55          r = res[slug]
56          print(f"{slug:24s} POI={r['pois']:4d} H={r['hotels']:3d} rest={r['restaurants']:3d}  Greedy={r['Greedy']['score']['mean']:6.1f}  GA={r['GA']['score']['mean']:6.1f}  Hybrid={r['Hybrid']['score']['mean']:6.1f}  valid {r['Hybrid']['valid']}/{r['Hybrid']['n']}  p={r['hybrid_vs_ga_p']:.4f}", flush=True)
57      json.dump({'trials': TRIALS, 'scenario': SC['label'], 'results': res}, open(os.path.join(R.OUT_DIR, f'sparse_results{SUF}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
58      with open(os.path.join(R.OUT_DIR, f'sparse_stats{SUF}.txt'), 'w', encoding='utf-8') as f:
59          f.write(f"SPARSE / CROSS-PROVINCE EXPERIMENTS — trials={TRIALS}, scenario={SC['label']}\n")
60          for slug, r in res.items():
61              f.write(f"{slug}\tPOI={r['pois']}\tH={r['hotels']}\trest={r['restaurants']}\tGreedy={r['Greedy']['score']['mean']}\tGA={r['GA']['score']['mean']}\tHybrid={r['Hybrid']['score']['mean']}\tvalid={r['Hybrid']['valid']}/{r['Hybrid']['n']}\tp={r['hybrid_vs_ga_p']:.4f}\n")
62      print('saved')
บรรทัด 51–56: วนทุกจังหวัดข้อมูลน้อยและทุกคู่ รันและพิมพ์สรุปบรรทัดเดียว
บรรทัด 57: เขียน sparse_results*.json
บรรทัด 58–61: เขียน sparse_stats*.txt แบบแยกคอลัมน์ด้วยแท็บ
บรรทัด 62: พิมพ์ saved

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/utils.py
backend/main.py
experiments/run_province_experiments.py