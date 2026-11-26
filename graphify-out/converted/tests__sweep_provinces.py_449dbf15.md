<!-- converted from tests__sweep_provinces.py.docx -->

คู่มือโค้ด: tests/sweep_provinces.py
กวาดทดสอบ API ทุกจังหวัด
ไฟล์ต้นฉบับ: tests/sweep_provinces.py (57 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ยิงคำขอ /api/packages ของ ➜ backend/main.py ผ่าน FastAPI TestClient กับทุกชุดข้อมูลจังหวัด (78 ชุด) 9 เงื่อนไข (งบ จำนวนวัน จำนวนคน รวมโรงแรมหรือไม่) และ 3 ระดับแพ็กเกจ รวม 2,106 แผน แล้วตรวจว่าทุกแผนผ่านข้อจำกัด ไม่เกินงบ ทุกวันมีสถานที่ท่องเที่ยว ครบ 4 แห่งต่อวัน และมีมื้ออาหาร 2 มื้อต่อวัน ผลคือ experiments/results/sweep_provinces.json ที่ใช้ในตารางที่ 4.12 ของรายงาน

บรรทัด 1–16  หัวไฟล์ เงื่อนไขทดสอบ
1  # -*- coding: utf-8 -*-
2  """
3  sweep_provinces.py — กวาดทดสอบ API /api/packages กับทุกชุดข้อมูลจังหวัด หลายเงื่อนไขงบ/จำนวนวัน/รวมโรงแรม
4  ตรวจทุกแพ็กเกจ: ผ่านข้อจำกัด (valid), ไม่เกินงบ, ทุกวันมีสถานที่ท่องเที่ยว, ครบ 4 แห่งต่อวัน, มีมื้อ 2 มื้อต่อวัน
5  จำนวนวันถูกจำกัดตาม max_days ของจังหวัดเหมือนหน้าเว็บ
6  รัน:  python tests/sweep_provinces.py [จำนวน process]      ผลลัพธ์: experiments/results/sweep_provinces.json
7  """
8  import os, sys, json, time
9  from multiprocessing import Pool
10  os.environ['WET_RATE_PER_MIN'] = '1000000'      # ปิดตัวจำกัดอัตราคำขอเฉพาะการทดสอบ
11  ROOT = os.path.join(os.path.dirname(__file__), '..')
12  sys.path.insert(0, os.path.join(ROOT, 'algorithm')); sys.path.insert(0, os.path.join(ROOT, 'backend'))
13
14  # (งบรวม, วัน, จำนวนคน, รวมโรงแรมในงบ)
15  CASES = [(1000, 1, 1, False), (1000, 2, 1, False), (1000, 3, 1, False), (2000, 3, 1, False), (5000, 3, 2, False),
16           (3000, 2, 1, False), (10000, 4, 2, True), (2000, 4, 2, False), (1000, 2, 1, True)]
บรรทัด 1–7: docstring อธิบายสิ่งที่ตรวจ และวิธีรัน (python tests/sweep_provinces.py [จำนวน process])
บรรทัด 8–12: นำเข้าโมดูล ปิดตัวจำกัดอัตราคำขอเฉพาะตอนทดสอบ (WET_RATE_PER_MIN) และเพิ่มโฟลเดอร์ algorithm กับ backend เข้า path
บรรทัด 14–16: CASES เงื่อนไข 9 แบบ (งบรวม จำนวนวัน จำนวนคน รวมโรงแรมในงบ)
บรรทัด 19–39  ทดสอบกลุ่มจังหวัดหนึ่งชุด
19  def work(slugs):
20      from fastapi.testclient import TestClient
21      import main as api
22      api.SESSION_FILE = os.path.join(os.environ.get('TEMP', '.'), f'sweep_sessions_{os.getpid()}.json')
23      c = TestClient(api.app)
24      out = []
25      for slug in slugs:
26          mx = api._max_days(slug)
27          for ci, (budget, days, trav, hotel) in enumerate(CASES):
28              d = min(days, mx)
29              r = c.post('/api/packages', json={'province': slug, 'budget': budget, 'days': d, 'travelers': trav, 'seed': 1, 'include_hotel': hotel})
30              if r.status_code != 200:
31                  out.append({'slug': slug, 'case': ci, 'status': r.status_code, 'detail': str(r.text)[:120]}); continue
32              for pkg in r.json()['packages']:
33                  sights = [sum(1 for p in day['pois'] if p['category'] != 'restaurant') for day in pkg['days']]
34                  meals = [sum(1 for p in day['pois'] if p['category'] == 'restaurant') for day in pkg['days']]
35                  out.append({'slug': slug, 'case': ci, 'tier': pkg['tier'], 'status': 200, 'days': d, 'clamped': d != days, 'valid': pkg['valid'],
36                              'over_budget': pkg['total_cost'] > budget + 1e-6, 'cost': pkg['total_cost'], 'budget': budget,
37                              'no_sights': sum(sights) == 0, 'empty_days': sum(1 for s in sights if s == 0), 'short_days': sum(1 for s in sights if s < 4),
38                              'short_meals_days': sum(1 for m in meals if m < 2), 'notes': len(pkg.get('notes', [])), 'violations': pkg.get('violations', [])})
39      return out
บรรทัด 19–24: work สร้าง TestClient ตั้งไฟล์เซสชันชั่วคราวแยกต่อ process (ไม่เขียนทับไฟล์จริง)
บรรทัด 25–31: ต่อจังหวัด จำกัดจำนวนวันตาม max_days ของจังหวัดเหมือนหน้าเว็บ แล้วส่งคำขอ ถ้าไม่ใช่ 200 บันทึกข้อผิดพลาด
บรรทัด 32–38: ต่อแพ็กเกจ นับสถานที่ท่องเที่ยวและมื้อต่อวัน แล้วบันทึกธง valid เกินงบ วันว่าง วันที่ที่เที่ยวน้อยกว่า 4 วันที่มื้อไม่ครบ จำนวนหมายเหตุ และข้อความผิดข้อจำกัด
บรรทัด 39: คืนผลของกลุ่ม
บรรทัด 42–57  จุดเริ่มต้น และสรุปผล
42  if __name__ == '__main__':
43      import main as api
44      nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 4
45      slugs = sorted(api.DATA)
46      chunks = [slugs[i::nproc] for i in range(nproc)]
47      t0 = time.time()
48      with Pool(nproc) as pool:
49          res = [x for part in pool.map(work, chunks) for x in part]
50      ok = [r for r in res if r['status'] == 200]
51      summary = {'datasets': len(slugs), 'cases': len(CASES), 'plans': len(ok), 'http_errors': [r for r in res if r['status'] != 200],
52                 'invalid': sum(not r['valid'] for r in ok), 'over_budget': sum(r['over_budget'] for r in ok), 'no_sights': sum(r['no_sights'] for r in ok),
53                 'plans_with_empty_day': sum(r['empty_days'] > 0 for r in ok), 'plans_with_short_sight_days': sum(r['short_days'] > 0 for r in ok),
54                 'plans_with_short_meals': sum(r['short_meals_days'] > 0 for r in ok), 'plans_with_notes': sum(r['notes'] > 0 for r in ok),
55                 'clamped_requests': sum(1 for r in ok if r['clamped']) // 3, 'seconds': round(time.time() - t0)}
56      json.dump({'summary': summary, 'plans': ok}, open(os.path.join(ROOT, 'experiments', 'results', 'sweep_provinces.json'), 'w', encoding='utf-8'), ensure_ascii=False)
57      print(json.dumps({k: v for k, v in summary.items() if k != 'http_errors'}, ensure_ascii=False, indent=1), 'http_errors', len(summary['http_errors']))
บรรทัด 42–49: แบ่งจังหวัดเป็นกลุ่มตามจำนวน process แล้วรันพร้อมกันด้วย multiprocessing.Pool
บรรทัด 50–55: สรุปจำนวนแผน ข้อผิดพลาด HTTP แผนผิดข้อจำกัด เกินงบ ไม่มีสถานที่ มีวันว่าง วันที่สถานที่น้อย มื้อขาด มีหมายเหตุ และคำขอที่ถูกจำกัดจำนวนวัน
บรรทัด 56–57: เขียน sweep_provinces.json และพิมพ์สรุป

ไฟล์ที่เชื่อมกับไฟล์นี้
backend/main.py