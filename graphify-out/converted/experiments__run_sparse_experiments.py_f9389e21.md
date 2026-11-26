<!-- converted from experiments__run_sparse_experiments.py.docx -->

คู่มือโค้ด: experiments/run_sparse_experiments.py
การทดลองจังหวัดข้อมูลน้อย (sparse)
ไฟล์ต้นฉบับ: experiments/run_sparse_experiments.py (57 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ทดสอบ Greedy GA และ Hybrid บนจังหวัดที่ข้อมูลน้อย 8 จังหวัด ด้วยกติกาและพารามิเตอร์เดียวกับการทดลองหลักของ ➜ experiments/run_province_experiments.py (เดิมมีชุดทริปข้ามจังหวัดข้างเคียงด้วย แต่ถอดฟังก์ชันนั้นออกจากระบบแล้ว) ผลคือ sparse_results*.json และ sparse_stats*.txt ที่ใช้ในตารางที่ 4.9 ของรายงาน

บรรทัด 1–20  หัวไฟล์ ค่าคงที่
1  # -*- coding: utf-8 -*-
2  """
3  run_sparse_experiments.py — WeEasyTrip Project 2
4  ทดลอง Greedy / GA / Hybrid บนจังหวัดข้อมูลน้อย (sparse)
5  (เดิมมีชุดทริปข้ามจังหวัดข้างเคียงด้วย แต่ถอดฟังก์ชันนั้นออกจากระบบแล้ว)
6  ใช้ฟังก์ชันจาก run_province_experiments.py (กติกาและพารามิเตอร์เดียวกัน) — สถานการณ์ S1 (3 วัน 10,000 บาท)
7  ผลลัพธ์: results/sparse_results.json, results/sparse_stats.txt
8  รัน:  python run_sparse_experiments.py [trials]
9  """
10  import sys, os, json, statistics
11  sys.argv = [sys.argv[0]] + sys.argv[1:2]      # ให้ run_province_experiments อ่าน trials จาก argv[1] เท่านั้น
12  import run_province_experiments as R
13  from utils import load_data, set_travel_profile
14  from scipy import stats as st
15
16  TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 10
17  SPARSE = ['nongbualamphu', 'phichit', 'lamphun', 'nakhonnayok', 'singburi', 'kalasin', 'chaiyaphum', 'loei']
18  SC = R.SCENARIOS[int(os.environ.get('SC_IDX', 0))]
19  SUF = '' if SC is R.SCENARIOS[0] else '_' + SC['label'].split('_')[0]
20  R.TRIALS = TRIALS
บรรทัด 1–9: docstring อธิบายการทดลองและที่เก็บผล (sparse_results*.json และ sparse_stats*.txt)
บรรทัด 10: นำเข้าโมดูลมาตรฐาน
บรรทัด 11: ตัด sys.argv ให้โมดูลทดลองหลักอ่านจำนวนรอบจากอาร์กิวเมนต์แรกเท่านั้น
บรรทัด 12–14: นำเข้า ➜ experiments/run_province_experiments.py (ในชื่อ R) ➜ load_data() ใน algorithm/utils.py และ ➜ set_travel_profile() ใน algorithm/utils.py และ scipy.stats
บรรทัด 16: TRIALS จำนวนรอบ (ตั้งต้น 10)
บรรทัด 17: SPARSE รายชื่อจังหวัดข้อมูลน้อย 8 จังหวัด
บรรทัด 18: เลือกสถานการณ์จาก SC_IDX
บรรทัด 19: ต่อท้ายชื่อไฟล์ผลลัพธ์ (ว่างสำหรับ S1 หรือ _S2 _S3)
บรรทัด 20: ตั้งจำนวนรอบให้โมดูลหลัก
บรรทัด 23–27  โหลดข้อมูลจังหวัด
23  def load(slug):
24      pois, hotels = load_data(os.path.join(R.ROOT, 'data', 'provinces', f'{slug}.json'))
25      cfg = R.PROV_CFG[slug]
26      set_travel_profile(cfg.get('road_factor', 1.0), cfg.get('speed_kmh', 40))
27      return pois, hotels
บรรทัด 23–24: load โหลดสถานที่และโรงแรมของจังหวัดจากไฟล์ใน data/provinces
บรรทัด 25–26: ตั้งโปรไฟล์เดินทางของจังหวัด (road factor และความเร็ว)
บรรทัด 27: คืนจุดและโรงแรม
บรรทัด 30–43  รันหนึ่งจังหวัด
30  def run(slug):
31      pois, hotels = load(slug)
32      hs = sorted(hotels, key=lambda h: h['cost'])
33      hotel = hs[int(len(hs) * SC['hotel_frac'])]
34      act = max(0.0, SC['budget'] - hotel['cost'] * (SC['days'] - 1))
35      out, groups = {'pois': len(pois), 'hotels': len(hotels), 'restaurants': sum(p['category'] == 'restaurant' for p in pois)}, {}
36      for algo in ('Greedy', 'GA', 'Hybrid'):
37          n = 1 if algo == 'Greedy' else TRIALS
38          tr = [R.run_algo(algo, pois, hotel, SC['days'], act, SC['mode'], seed=t)[1] for t in range(n)]
39          groups[algo] = [t['score'] for t in tr]
40          out[algo] = {'n': n, 'score': R.summarize(groups[algo]), 'time_ms': R.summarize([t['time_ms'] for t in tr])['mean'],
41                       'valid': sum(t['valid'] for t in tr), 'meals_ok': sum(t['meals_ok'] for t in tr), 'km_day': round(statistics.mean(t['km_day'] for t in tr), 1)}
42      out['hybrid_vs_ga_p'] = float(st.mannwhitneyu(groups['Hybrid'], groups['GA'], alternative='greater').pvalue)
43      return out
บรรทัด 30–34: ประกาศ run โหลดข้อมูล เลือกโรงแรมตามตำแหน่งของสถานการณ์ และคำนวณงบกิจกรรม
บรรทัด 35: เตรียมผลลัพธ์พร้อมจำนวนจุด โรงแรม และร้านอาหาร
บรรทัด 36–41: รันทั้งสามอัลกอริทึมด้วย R.run_algo (Greedy ครั้งเดียว) สรุปคะแนน เวลา จำนวนที่ผ่าน มื้อครบ และกิโลเมตรต่อวัน
บรรทัด 42: ทดสอบ Mann-Whitney ทางเดียว (Hybrid มากกว่า GA)
บรรทัด 43: คืนผล
บรรทัด 46–57  จุดเริ่มต้นและบันทึกผล
46  if __name__ == '__main__':
47      res = {}
48      for slug in SPARSE:
49          res[slug] = run(slug)
50          r = res[slug]
51          print(f"{slug:24s} POI={r['pois']:4d} H={r['hotels']:3d} rest={r['restaurants']:3d}  Greedy={r['Greedy']['score']['mean']:6.1f}  GA={r['GA']['score']['mean']:6.1f}  Hybrid={r['Hybrid']['score']['mean']:6.1f}  valid {r['Hybrid']['valid']}/{r['Hybrid']['n']}  p={r['hybrid_vs_ga_p']:.4f}", flush=True)
52      json.dump({'trials': TRIALS, 'scenario': SC['label'], 'results': res}, open(os.path.join(R.OUT_DIR, f'sparse_results{SUF}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
53      with open(os.path.join(R.OUT_DIR, f'sparse_stats{SUF}.txt'), 'w', encoding='utf-8') as f:
54          f.write(f"SPARSE EXPERIMENTS — trials={TRIALS}, scenario={SC['label']}\n")
55          for slug, r in res.items():
56              f.write(f"{slug}\tPOI={r['pois']}\tH={r['hotels']}\trest={r['restaurants']}\tGreedy={r['Greedy']['score']['mean']}\tGA={r['GA']['score']['mean']}\tHybrid={r['Hybrid']['score']['mean']}\tvalid={r['Hybrid']['valid']}/{r['Hybrid']['n']}\tp={r['hybrid_vs_ga_p']:.4f}\n")
57      print('saved')
บรรทัด 46–51: วนทุกจังหวัดข้อมูลน้อย รันและพิมพ์สรุปบรรทัดเดียว
บรรทัด 52: เขียน sparse_results*.json
บรรทัด 53–56: เขียน sparse_stats*.txt แบบแยกคอลัมน์ด้วยแท็บ
บรรทัด 57: พิมพ์ saved

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/utils.py
experiments/run_province_experiments.py