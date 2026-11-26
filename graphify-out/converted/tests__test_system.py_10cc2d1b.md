<!-- converted from tests__test_system.py.docx -->

คู่มือโค้ด: tests/test_system.py
ชุดทดสอบซอฟต์แวร์ (unittest)
ไฟล์ต้นฉบับ: tests/test_system.py (215 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ชุดทดสอบ 26 กรณีของระบบ: ส่วน A ทดสอบหน่วยของโมดูลใน algorithm/ (➜ algorithm/utils.py ➜ algorithm/greedy.py ➜ algorithm/genetic.py ➜ algorithm/hybrid.py) และส่วน B ทดสอบ API ของ ➜ backend/main.py ด้วย FastAPI TestClient รันด้วย python -m unittest tests.test_system -v จากโฟลเดอร์รากของโปรเจกต์ ผลคือตารางที่ 4.12 ของรายงาน

บรรทัด 1–28  หัวไฟล์ ข้อมูลทดสอบ
1  # -*- coding: utf-8 -*-
2  """
3  test_system.py — ชุดทดสอบซอฟต์แวร์ของ WeEasyTrip (unittest + FastAPI TestClient)
4  ส่วน A: ทดสอบหน่วย (unit) ของ algorithm/  ส่วน B: ทดสอบ API (integration) ของ backend/
5  รัน:  python -m unittest tests.test_system -v     (จากโฟลเดอร์รากของโปรเจกต์)
6  """
7  import os, sys, random, tempfile, unittest
8  ROOT = os.path.join(os.path.dirname(__file__), '..')
9  sys.path.insert(0, os.path.join(ROOT, 'algorithm'))
10  sys.path.insert(0, os.path.join(ROOT, 'backend'))
11
12  import utils
13  from utils import load_data, evaluate_route, haversine_km, travel_time_min, set_travel_profile
14  from greedy import greedy_solve
15  from genetic import genetic_solve
16  from hybrid import hybrid_solve, reoptimize_solve
17
18  PHUKET = os.path.join(ROOT, 'data', 'provinces', 'phuket.json')
19  POIS, HOTELS = load_data(PHUKET)
20  HOTEL = sorted(HOTELS, key=lambda h: h['cost'])[len(HOTELS) // 3]
21  BUDGET = 15_000
22  CATS_ATTR = lambda day: [p for p in day if p['category'] != 'restaurant']
23  CATS_REST = lambda day: [p for p in day if p['category'] == 'restaurant']
24
25
26  def act_budget(days):
27      return max(0.0, BUDGET - HOTEL['cost'] * (days - 1))
28
บรรทัด 1–6: docstring อธิบายสองส่วนและวิธีรัน
บรรทัด 7–16: นำเข้าโมดูลมาตรฐานและเพิ่ม algorithm กับ backend เข้า path แล้วนำเข้าฟังก์ชันที่ทดสอบ
บรรทัด 18–23: โหลดข้อมูลภูเก็ต เลือกโรงแรมระดับกลาง งบ 15,000 บาท และตัวช่วยแยกสถานที่ท่องเที่ยวกับร้านอาหาร
บรรทัด 26–27: act_budget งบกิจกรรมหลังหักค่าโรงแรมตามจำนวนคืน
บรรทัด 30–59  ส่วน A1: ทดสอบ utils
30  class TestUtils(unittest.TestCase):
31      def setUp(self):
32          set_travel_profile(1.0, 40)
33
34      def test_haversine_zero_and_symmetric(self):
35          a, b = POIS[0], POIS[1]
36          self.assertAlmostEqual(haversine_km(a['lat'], a['lng'], a['lat'], a['lng']), 0.0, places=6)
37          self.assertAlmostEqual(haversine_km(a['lat'], a['lng'], b['lat'], b['lng']),
38                                 haversine_km(b['lat'], b['lng'], a['lat'], a['lng']), places=9)
39
40      def test_travel_time_monotonic(self):
41          self.assertLess(travel_time_min(1), travel_time_min(10))
42          self.assertLess(travel_time_min(10), travel_time_min(50))
43
44      def test_empty_plan_is_evaluated(self):
45          ev = evaluate_route([[], []], HOTEL, 5000)
46          self.assertEqual(ev['total_score'], 0.0)
47
48      def test_budget_violation_detected(self):
49          route = [[p for p in POIS if p['category'] != 'restaurant' and p['cost'] > 0][:3]]
50          ev = evaluate_route(route, HOTEL, 1.0)
51          self.assertFalse(ev['valid'])
52          self.assertTrue(ev['violations'])
53
54      def test_data_integrity(self):
55          ids = [p['id'] for p in POIS]
56          self.assertEqual(len(ids), len(set(ids)))
57          for p in POIS:
58              self.assertTrue(-90 <= p['lat'] <= 90 and -180 <= p['lng'] <= 180)
59              self.assertGreaterEqual(p['cost'], 0)
บรรทัด 30–32: ตั้งโปรไฟล์เดินทางกลางก่อนทุกกรณี
บรรทัด 34–38: ระยะ haversine ของจุดเดียวกันเป็น 0 และสมมาตร
บรรทัด 40–42: เวลาเดินทางเพิ่มตามระยะ
บรรทัด 44–46: แผนว่างประเมินได้ คะแนน 0
บรรทัด 48–52: แผนที่เกินงบถูกตรวจพบว่าผิดข้อจำกัด
บรรทัด 54–59: ข้อมูลภูเก็ตไม่มี id ซ้ำ พิกัดอยู่ในช่วงถูกต้อง และค่าใช้จ่ายไม่ติดลบ
บรรทัด 62–123  ส่วน A2: ทดสอบอัลกอริทึม
62  class TestAlgorithms(unittest.TestCase):
63      DAYS = 3
64
65      @classmethod
66      def setUpClass(cls):
67          set_travel_profile(1.38, 45.8)
68          random.seed(1)
69          cls.hy, _ = hybrid_solve(POIS, HOTEL, cls.DAYS, act_budget(cls.DAYS), pop_size=20, generations=30)
70          random.seed(1)
71          cls.ga, _ = genetic_solve(POIS, HOTEL, cls.DAYS, act_budget(cls.DAYS), pop_size=20, generations=30)
72          cls.gr = greedy_solve(POIS, HOTEL, cls.DAYS, act_budget(cls.DAYS))
73
74      def _check_plan(self, routes):
75          self.assertEqual(len(routes), self.DAYS)
76          ev = evaluate_route(routes, HOTEL, act_budget(self.DAYS))
77          self.assertTrue(ev['valid'], ev['violations'])
78          ids = [p['id'] for day in routes for p in day]
79          self.assertEqual(len(ids), len(set(ids)), 'สถานที่ซ้ำในแผน')
80          self.assertLessEqual(ev['total_cost'], act_budget(self.DAYS) + 1e-6)
81
82      def test_hybrid_valid(self):
83          self._check_plan(self.hy)
84
85      def test_ga_valid(self):
86          self._check_plan(self.ga)
87
88      def test_greedy_valid(self):
89          self._check_plan(self.gr)
90
91      def test_hybrid_day_pattern(self):
92          for day in self.hy:
93              self.assertLessEqual(len(CATS_ATTR(day)), 4)
94              self.assertEqual(len(CATS_REST(day)), 2, 'ต้องมีมื้อกลางวันและเย็นวันละ 2 ร้าน')
95
96      def test_hybrid_meal_windows(self):
97          ev = evaluate_route(self.hy, HOTEL, act_budget(self.DAYS))
98          by_id = {p['id']: p for p in POIS}
99          for dd in ev['days_detail']:
100              meals = [a for a in dd['arrivals'] if by_id[a[0]]['category'] == 'restaurant']
101              self.assertEqual(len(meals), 2)
102              self.assertTrue(11 * 60 <= meals[0][1] <= 14.5 * 60 + 1, f'มื้อกลางวันเริ่ม {meals[0][1]} นาที')
103              self.assertTrue(17 * 60 <= meals[1][1] <= 20 * 60 + 1, f'มื้อเย็นเริ่ม {meals[1][1]} นาที')
104
105      def test_hybrid_reproducible_with_seed(self):
106          random.seed(7)
107          a, _ = hybrid_solve(POIS, HOTEL, 2, act_budget(2), pop_size=10, generations=10)
108          random.seed(7)
109          b, _ = hybrid_solve(POIS, HOTEL, 2, act_budget(2), pop_size=10, generations=10)
110          self.assertEqual([[p['id'] for p in d] for d in a], [[p['id'] for p in d] for d in b])
111
112      def test_reoptimize_respects_locks_and_exclusions(self):
113          removed = self.hy[0][0]['id']
114          extra = next(p for p in POIS if p['category'] != 'restaurant' and p['id'] not in {q['id'] for d in self.hy for q in d})
115          edited = [[p for p in d if p['id'] != removed] for d in self.hy]
116          random.seed(3)
117          out = reoptimize_solve(POIS, HOTEL, edited, act_budget(self.DAYS), locked_ids=[], excluded_ids=[removed])
118          ids = {p['id'] for d in out for p in d}
119          self.assertNotIn(removed, ids)
120          random.seed(3)
121          out2 = reoptimize_solve(POIS, HOTEL, edited, act_budget(self.DAYS), locked_ids=[extra['id']], excluded_ids=[removed])
122          ids2 = {p['id'] for d in out2 for p in d}
123          self.assertNotIn(removed, ids2)
บรรทัด 62–72: ตั้งโปรไฟล์ภูเก็ต แล้วสร้างแผน 3 วันด้วย Hybrid GA และ Greedy หนึ่งครั้งเพื่อใช้ร่วมกัน
บรรทัด 74–80: _check_plan ตรวจจำนวนวัน แผนผ่านข้อจำกัด ไม่มีสถานที่ซ้ำ และค่าใช้จ่ายไม่เกินงบ
บรรทัด 82–89: แผนของทั้งสามอัลกอริทึมผ่านการตรวจ
บรรทัด 91–94: แผนของ Hybrid มีที่เที่ยวไม่เกิน 4 และมื้อ 2 ร้านทุกวัน
บรรทัด 96–103: เวลาเริ่มมื้อกลางวันอยู่ใน 11:00-14:30 และมื้อเย็นใน 17:00-20:00
บรรทัด 105–110: เมื่อตั้ง seed เดียวกัน Hybrid ได้แผนเดิมทุกครั้ง
บรรทัด 112–123: ➜ reoptimize_solve() ใน algorithm/hybrid.py ไม่ใส่จุดที่ผู้ใช้ลบกลับมา และเมื่อให้ล็อกจุดอื่นก็ยังไม่ใส่จุดที่ลบ
บรรทัด 126–211  ส่วน B: ทดสอบ API
126  class TestAPI(unittest.TestCase):
127      @classmethod
128      def setUpClass(cls):
129          from fastapi.testclient import TestClient
130          import main as api
131          cls.api = api
132          api.SESSION_FILE = os.path.join(tempfile.mkdtemp(), 'sessions.json')   # ไม่เขียนทับไฟล์จริง
133          api.SESSIONS.clear()
134          cls.c = TestClient(api.app)
135          cls.body = {'province': 'phuket', 'budget': 20000, 'days': 3, 'travelers': 2, 'seed': 5}
136          cls.pk = cls.c.post('/api/packages', json=cls.body).json()
137
138      def test_health(self):
139          r = self.c.get('/api/health').json()
140          self.assertEqual(r['status'], 'ok')
141          self.assertGreaterEqual(r['provinces'], 77)
142
143      def test_provinces_listing(self):
144          r = self.c.get('/api/provinces').json()
145          slugs = {p['slug'] for p in r['provinces']}
146          self.assertIn('phuket', slugs)
147          self.assertGreaterEqual(len(slugs), 77)
148
149      def test_pois_endpoint(self):
150          r = self.c.get('/api/pois', params={'province': 'krabi'}).json()
151          self.assertTrue(r['pois'] and r['hotels'])
152
153      def test_unknown_province_404(self):
154          self.assertEqual(self.c.get('/api/pois', params={'province': 'atlantis'}).status_code, 404)
155
156      def test_packages_three_tiers(self):
157          tiers = [p['tier'] for p in self.pk['packages']]
158          self.assertEqual(tiers, ['Budget', 'Standard', 'Premium'])
159
160      def test_packages_within_budget_and_valid(self):
161          for p in self.pk['packages']:
162              self.assertLessEqual(p['total_cost'], self.body['budget'] * 1.0001)
163              self.assertEqual(len(p['days']), self.body['days'])
164              self.assertTrue(p['valid'], p['violations'])
165
166      def test_request_validation(self):
167          self.assertEqual(self.c.post('/api/packages', json={**self.body, 'budget': 500}).status_code, 422)
168          self.assertEqual(self.c.post('/api/packages', json={**self.body, 'days': 8}).status_code, 422)
169
170      def test_other_algorithm_requires_developer_mode(self):
171          r = self.c.post('/api/packages', json={**self.body, 'algorithm': 'ga'})
172          self.assertEqual(r.status_code, 403)
173
174      def test_wrong_dev_password_rejected(self):
175          self.assertNotEqual(self.c.post('/api/dev/unlock', json={'password': 'wrong'}).status_code, 200)
176
177      def test_avoided_category_never_appears(self):
178          r = self.c.post('/api/packages', json={**self.body, 'preferences': {'avoided': ['temple', 'market']}}).json()
179          for pkg in r['packages']:
180              for d in pkg['days']:
181                  for p in d['pois']:
182                      self.assertNotIn(p['category'], ('temple', 'market'))
183
184      def test_recompute_roundtrip(self):
185          pkg = self.pk['packages'][1]
186          routes = [[p['id'] for p in d['pois']] for d in pkg['days']]
187          r = self.c.post('/api/recompute', json={'province': 'phuket', 'hotel_id': pkg['hotel']['id'], 'days': 3,
188                                                  'budget': 20000, 'routes': routes, 'travelers': 2})
189          self.assertEqual(r.status_code, 200)
190          self.assertAlmostEqual(r.json()['total_score'], pkg['total_score'], delta=pkg['total_score'] * 0.05 + 1)
191
192      def test_recompute_unknown_poi_404(self):
193          pkg = self.pk['packages'][0]
194          r = self.c.post('/api/recompute', json={'province': 'phuket', 'hotel_id': pkg['hotel']['id'], 'days': 1,
195                                                  'budget': 20000, 'routes': [['no-such-poi']]})
196          self.assertEqual(r.status_code, 404)
197
198      def test_session_create_get_and_conflict(self):
199          pkg = self.pk['packages'][0]
200          s = self.c.post('/api/sessions', json={'province': 'phuket', 'package': pkg}).json()
201          self.assertEqual(s['version'], 1)
202          got = self.c.get(f"/api/sessions/{s['id']}").json()
203          self.assertEqual(got['package']['tier'], pkg['tier'])
204          ok = self.c.put(f"/api/sessions/{s['id']}", json={'base_version': 1, 'package': pkg})
205          self.assertEqual(ok.status_code, 200)
206          self.assertEqual(ok.json()['version'], 2)
207          stale = self.c.put(f"/api/sessions/{s['id']}", json={'base_version': 1, 'package': pkg})
208          self.assertEqual(stale.status_code, 409)
209
210      def test_session_not_found(self):
211          self.assertEqual(self.c.get('/api/sessions/zzzzzz').status_code, 404)
บรรทัด 126–136: เตรียม TestClient ตั้งไฟล์เซสชันชั่วคราว และสร้างแพ็กเกจตัวอย่างหนึ่งชุดใช้ร่วมกัน
บรรทัด 138–141: /api/health ตอบ ok และมีจังหวัดอย่างน้อย 77
บรรทัด 143–147: /api/provinces มีภูเก็ตและอย่างน้อย 77 รายการ
บรรทัด 149–151: /api/pois ของกระบี่มีสถานที่และโรงแรม
บรรทัด 153–154: จังหวัดที่ไม่มีตอบ 404
บรรทัด 156–158: แพ็กเกจมี 3 ระดับ Budget Standard Premium
บรรทัด 160–164: ทุกแพ็กเกจผ่านข้อจำกัดและไม่เกินงบ และจำนวนวันตรงกับคำขอ
บรรทัด 166–168: งบหรือจำนวนวันนอกช่วงถูกปฏิเสธด้วย 422
บรรทัด 170–172: อัลกอริทึมอื่นนอกจาก Hybrid ต้องใช้โหมด Developer (ตอบ 403)
บรรทัด 174–175: รหัสโหมด Developer ผิดถูกปฏิเสธ
บรรทัด 177–182: หมวดที่ผู้ใช้ไม่เอาไม่ปรากฏในแผน
บรรทัด 184–190: คำนวณแผนใหม่ด้วย /api/recompute ได้คะแนนใกล้เคียงเดิม
บรรทัด 192–196: คำนวณใหม่ด้วยสถานที่ที่ไม่มีตอบ 404
บรรทัด 198–208: สร้างเซสชันแชร์ อ่าน แก้ไขเลขรุ่นต่อเนื่อง และแก้ด้วยเลขรุ่นเก่าได้ 409
บรรทัด 210–211: เซสชันที่ไม่มีตอบ 404
บรรทัด 214–215  จุดเริ่มต้น
214  if __name__ == '__main__':
215      unittest.main(verbosity=2)
บรรทัด 214–215: รัน unittest

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
algorithm/utils.py
backend/main.py