# -*- coding: utf-8 -*-
"""
test_system.py — ชุดทดสอบซอฟต์แวร์ของ WeEasyTrip (unittest + FastAPI TestClient)
ส่วน A: ทดสอบหน่วย (unit) ของ algorithm/  ส่วน B: ทดสอบ API (integration) ของ backend/
รัน:  python -m unittest tests.test_system -v     (จากโฟลเดอร์รากของโปรเจกต์)
"""
import os, sys, random, tempfile, unittest
ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.join(ROOT, 'algorithm'))
sys.path.insert(0, os.path.join(ROOT, 'backend'))

import utils
from utils import load_data, evaluate_route, haversine_km, travel_time_min, set_travel_profile
from greedy import greedy_solve
from genetic import genetic_solve
from hybrid import hybrid_solve, reoptimize_solve

PHUKET = os.path.join(ROOT, 'data', 'provinces', 'phuket.json')
POIS, HOTELS = load_data(PHUKET)
HOTEL = sorted(HOTELS, key=lambda h: h['cost'])[len(HOTELS) // 3]
BUDGET = 15_000
CATS_ATTR = lambda day: [p for p in day if p['category'] != 'restaurant']
CATS_REST = lambda day: [p for p in day if p['category'] == 'restaurant']


def act_budget(days):
    return max(0.0, BUDGET - HOTEL['cost'] * (days - 1))


class TestUtils(unittest.TestCase):
    def setUp(self):
        set_travel_profile(1.0, 40)

    def test_haversine_zero_and_symmetric(self):
        a, b = POIS[0], POIS[1]
        self.assertAlmostEqual(haversine_km(a['lat'], a['lng'], a['lat'], a['lng']), 0.0, places=6)
        self.assertAlmostEqual(haversine_km(a['lat'], a['lng'], b['lat'], b['lng']),
                               haversine_km(b['lat'], b['lng'], a['lat'], a['lng']), places=9)

    def test_travel_time_monotonic(self):
        self.assertLess(travel_time_min(1), travel_time_min(10))
        self.assertLess(travel_time_min(10), travel_time_min(50))

    def test_empty_plan_is_evaluated(self):
        ev = evaluate_route([[], []], HOTEL, 5000)
        self.assertEqual(ev['total_score'], 0.0)

    def test_budget_violation_detected(self):
        route = [[p for p in POIS if p['category'] != 'restaurant' and p['cost'] > 0][:3]]
        ev = evaluate_route(route, HOTEL, 1.0)
        self.assertFalse(ev['valid'])
        self.assertTrue(ev['violations'])

    def test_data_integrity(self):
        ids = [p['id'] for p in POIS]
        self.assertEqual(len(ids), len(set(ids)))
        for p in POIS:
            self.assertTrue(-90 <= p['lat'] <= 90 and -180 <= p['lng'] <= 180)
            self.assertGreaterEqual(p['cost'], 0)


class TestAlgorithms(unittest.TestCase):
    DAYS = 3

    @classmethod
    def setUpClass(cls):
        set_travel_profile(1.38, 45.8)
        random.seed(1)
        cls.hy, _ = hybrid_solve(POIS, HOTEL, cls.DAYS, act_budget(cls.DAYS), pop_size=20, generations=30)
        random.seed(1)
        cls.ga, _ = genetic_solve(POIS, HOTEL, cls.DAYS, act_budget(cls.DAYS), pop_size=20, generations=30)
        cls.gr = greedy_solve(POIS, HOTEL, cls.DAYS, act_budget(cls.DAYS))

    def _check_plan(self, routes):
        self.assertEqual(len(routes), self.DAYS)
        ev = evaluate_route(routes, HOTEL, act_budget(self.DAYS))
        self.assertTrue(ev['valid'], ev['violations'])
        ids = [p['id'] for day in routes for p in day]
        self.assertEqual(len(ids), len(set(ids)), 'สถานที่ซ้ำในแผน')
        self.assertLessEqual(ev['total_cost'], act_budget(self.DAYS) + 1e-6)

    def test_hybrid_valid(self):
        self._check_plan(self.hy)

    def test_ga_valid(self):
        self._check_plan(self.ga)

    def test_greedy_valid(self):
        self._check_plan(self.gr)

    def test_hybrid_day_pattern(self):
        for day in self.hy:
            self.assertLessEqual(len(CATS_ATTR(day)), 4)
            self.assertEqual(len(CATS_REST(day)), 2, 'ต้องมีมื้อกลางวันและเย็นวันละ 2 ร้าน')

    def test_hybrid_meal_windows(self):
        ev = evaluate_route(self.hy, HOTEL, act_budget(self.DAYS))
        by_id = {p['id']: p for p in POIS}
        for dd in ev['days_detail']:
            meals = [a for a in dd['arrivals'] if by_id[a[0]]['category'] == 'restaurant']
            self.assertEqual(len(meals), 2)
            self.assertTrue(11 * 60 <= meals[0][1] <= 14.5 * 60 + 1, f'มื้อกลางวันเริ่ม {meals[0][1]} นาที')
            self.assertTrue(17 * 60 <= meals[1][1] <= 20 * 60 + 1, f'มื้อเย็นเริ่ม {meals[1][1]} นาที')

    def test_hybrid_reproducible_with_seed(self):
        random.seed(7)
        a, _ = hybrid_solve(POIS, HOTEL, 2, act_budget(2), pop_size=10, generations=10)
        random.seed(7)
        b, _ = hybrid_solve(POIS, HOTEL, 2, act_budget(2), pop_size=10, generations=10)
        self.assertEqual([[p['id'] for p in d] for d in a], [[p['id'] for p in d] for d in b])

    def test_reoptimize_respects_locks_and_exclusions(self):
        removed = self.hy[0][0]['id']
        extra = next(p for p in POIS if p['category'] != 'restaurant' and p['id'] not in {q['id'] for d in self.hy for q in d})
        edited = [[p for p in d if p['id'] != removed] for d in self.hy]
        random.seed(3)
        out = reoptimize_solve(POIS, HOTEL, edited, act_budget(self.DAYS), locked_ids=[], excluded_ids=[removed])
        ids = {p['id'] for d in out for p in d}
        self.assertNotIn(removed, ids)
        random.seed(3)
        out2 = reoptimize_solve(POIS, HOTEL, edited, act_budget(self.DAYS), locked_ids=[extra['id']], excluded_ids=[removed])
        ids2 = {p['id'] for d in out2 for p in d}
        self.assertNotIn(removed, ids2)


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from fastapi.testclient import TestClient
        import main as api
        cls.api = api
        api.SESSION_FILE = os.path.join(tempfile.mkdtemp(), 'sessions.json')   # ไม่เขียนทับไฟล์จริง
        api.SESSIONS.clear()
        cls.c = TestClient(api.app)
        cls.body = {'province': 'phuket', 'budget': 20000, 'days': 3, 'travelers': 2, 'seed': 5}
        cls.pk = cls.c.post('/api/packages', json=cls.body).json()

    def test_health(self):
        r = self.c.get('/api/health').json()
        self.assertEqual(r['status'], 'ok')
        self.assertGreaterEqual(r['provinces'], 77)

    def test_provinces_listing(self):
        r = self.c.get('/api/provinces').json()
        slugs = {p['slug'] for p in r['provinces']}
        self.assertIn('phuket', slugs)
        self.assertGreaterEqual(len(slugs), 77)

    def test_pois_endpoint(self):
        r = self.c.get('/api/pois', params={'province': 'krabi'}).json()
        self.assertTrue(r['pois'] and r['hotels'])

    def test_unknown_province_404(self):
        self.assertEqual(self.c.get('/api/pois', params={'province': 'atlantis'}).status_code, 404)

    def test_packages_three_tiers(self):
        tiers = [p['tier'] for p in self.pk['packages']]
        self.assertEqual(tiers, ['Budget', 'Standard', 'Premium'])

    def test_packages_within_budget_and_valid(self):
        for p in self.pk['packages']:
            self.assertLessEqual(p['total_cost'], self.body['budget'] * 1.0001)
            self.assertEqual(len(p['days']), self.body['days'])
            self.assertTrue(p['valid'], p['violations'])

    def test_request_validation(self):
        self.assertEqual(self.c.post('/api/packages', json={**self.body, 'budget': 500}).status_code, 422)
        self.assertEqual(self.c.post('/api/packages', json={**self.body, 'days': 8}).status_code, 422)

    def test_other_algorithm_requires_developer_mode(self):
        r = self.c.post('/api/packages', json={**self.body, 'algorithm': 'ga'})
        self.assertEqual(r.status_code, 403)

    def test_wrong_dev_password_rejected(self):
        self.assertNotEqual(self.c.post('/api/dev/unlock', json={'password': 'wrong'}).status_code, 200)

    def test_avoided_category_never_appears(self):
        r = self.c.post('/api/packages', json={**self.body, 'preferences': {'avoided': ['temple', 'market']}}).json()
        for pkg in r['packages']:
            for d in pkg['days']:
                for p in d['pois']:
                    self.assertNotIn(p['category'], ('temple', 'market'))

    def test_recompute_roundtrip(self):
        pkg = self.pk['packages'][1]
        routes = [[p['id'] for p in d['pois']] for d in pkg['days']]
        r = self.c.post('/api/recompute', json={'province': 'phuket', 'hotel_id': pkg['hotel']['id'], 'days': 3,
                                                'budget': 20000, 'routes': routes, 'travelers': 2})
        self.assertEqual(r.status_code, 200)
        self.assertAlmostEqual(r.json()['total_score'], pkg['total_score'], delta=pkg['total_score'] * 0.05 + 1)

    def test_recompute_unknown_poi_404(self):
        pkg = self.pk['packages'][0]
        r = self.c.post('/api/recompute', json={'province': 'phuket', 'hotel_id': pkg['hotel']['id'], 'days': 1,
                                                'budget': 20000, 'routes': [['no-such-poi']]})
        self.assertEqual(r.status_code, 404)

    def test_session_create_get_and_conflict(self):
        pkg = self.pk['packages'][0]
        s = self.c.post('/api/sessions', json={'province': 'phuket', 'package': pkg}).json()
        self.assertEqual(s['version'], 1)
        got = self.c.get(f"/api/sessions/{s['id']}").json()
        self.assertEqual(got['package']['tier'], pkg['tier'])
        ok = self.c.put(f"/api/sessions/{s['id']}", json={'base_version': 1, 'package': pkg})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.json()['version'], 2)
        stale = self.c.put(f"/api/sessions/{s['id']}", json={'base_version': 1, 'package': pkg})
        self.assertEqual(stale.status_code, 409)

    def test_session_not_found(self):
        self.assertEqual(self.c.get('/api/sessions/zzzzzz').status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
