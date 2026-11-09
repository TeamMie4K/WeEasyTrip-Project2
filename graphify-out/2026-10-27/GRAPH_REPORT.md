# Graph Report - Thesis Project  (2026-10-25)

## Corpus Check
- 45 files · ~76,927 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: .ics 2, .css 1)

## Summary
- 603 nodes · 1219 edges · 25 communities (22 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 64 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Genetic Algorithm Core
- Backend API (FastAPI)
- Frontend App Logic
- Frontend Backup Copy
- FastAPI Backend
- Experiments & Dataset (Report)
- fetch_pois_osm.py
- Problem Formulation
- time
- Frontend UI Structure
- System Architecture
- Convergence Plot Results
- Packages & Swap Feature
- Background Image
- Project Limitations
- genetic.py
- Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study
- Orienteering Problem (OP)
- CLAUDE.md
- Special Project 2 future work
- Algorithm Engine
- Greedy Algorithm (slot-based baseline)
- Genetic Algorithm (GA)
- Hybrid Algorithm (Greedy seed + GA + 2-opt)
- การดำเนินงาน

## God Nodes (most connected - your core abstractions)
1. `evaluate_route()` - 33 edges
2. `hybrid_solve()` - 22 edges
3. `create_packages()` - 19 edges
4. `reoptimize_solve()` - 17 edges
5. `การดำเนินงาน` - 17 edges
6. `genetic_solve()` - 15 edges
7. `greedy_solve()` - 15 edges
8. `showToast()` - 15 edges
9. `nsga2_solve()` - 14 edges
10. `Genetic Algorithm (GA)` - 14 edges

## Surprising Connections (you probably didn't know these)
- `สถานะ (อัปเดต 24 ต.ค. 2569)` --references--> `reoptimize_solve()`  [INFERRED]
  docs/project2_plan.md → algorithm/hybrid.py
- `Reinforcement Learning Agent` --conceptually_related_to--> `Greedy Seeding`  [INFERRED]
  graphify-out/converted/CS403_Report_68-2_33_pps-r1_280c1df9.md → CS403_Report_68-2_33_pps-r1.pdf
- `สถานะ (อัปเดต 24 ต.ค. 2569)` --references--> `Preferences`  [INFERRED]
  docs/project2_plan.md → backend/main.py
- `เฟส 1 — ขยายจังหวัด (เริ่มตรงนี้)` --references--> `PackageRequest`  [INFERRED]
  docs/project2_plan.md → backend/main.py
- `เฟส 1 — ขยายจังหวัด (เริ่มตรงนี้)` --references--> `RecomputeRequest`  [INFERRED]
  docs/project2_plan.md → backend/main.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **GA vs Hybrid vs Greedy fitness comparison** — experiments_results_convergence_ga, experiments_results_convergence_hybrid, experiments_results_convergence_greedy [EXTRACTED 1.00]
- **S1/S2/S3 test scenarios** — experiments_results_convergence_s1_short_budget, experiments_results_convergence_s2_medium_standard, experiments_results_convergence_s3_long_premium [EXTRACTED 1.00]
- **Three-step trip planning flow** — frontend_index_plannerpanel, frontend_index_packagessection, frontend_index_detailsection [EXTRACTED 1.00]
- **Hybrid pipeline stages** — cs403_report_68_2_33_pps_r1_greedy_seeding, cs403_report_68_2_33_pps_r1_ga_refinement, cs403_report_68_2_33_pps_r1_two_opt [EXTRACTED 1.00]
- **Hybrid pipeline** — cs403_report_68_2_33_pps_r1_greedy_seeding, docs_problem_formulation_ga, docs_problem_formulation_two_opt [EXTRACTED 1.00]
- **Three-tier system architecture** — cs403_report_68_2_33_pps_r1_engine, cs403_report_68_2_33_pps_r1_backend, cs403_report_68_2_33_pps_r1_frontend [EXTRACTED 1.00]
- **Greedy vs GA vs Hybrid comparison** — graphify_out_converted_cs403_report_68_2_33_pps_r1_280c1df9_greedy, docs_problem_formulation_ga, docs_problem_formulation_hybrid, cs403_report_68_2_33_pps_r1_kw [EXTRACTED 1.00]
- **Three compared algorithms** — cs403_report_68_2_33_pps_r1_greedy, cs403_report_68_2_33_pps_r1_ga, cs403_report_68_2_33_pps_r1_hybrid [EXTRACTED 1.00]
- **Experiment scenarios S1-S3** — experiments_results_stats_s1, experiments_results_stats_s2, experiments_results_stats_s3 [EXTRACTED 1.00]
- **Greedy, GA and Hybrid solvers** — docs_problem_formulation_greedy, docs_problem_formulation_ga, docs_problem_formulation_hybrid [EXTRACTED 1.00]

## Communities (25 total, 3 thin omitted)

### Community 0 - "Genetic Algorithm Core"
Cohesion: 0.05
Nodes (39): _find_best_for_slot(), greedy_solve(), _budget_repair(), _crossover(), diversity_stats(), _final_validity(), _fitness(), hybrid_solve() (+31 more)

### Community 1 - "Backend API (FastAPI)"
Cohesion: 0.83
Nodes (4): Backend API (FastAPI), Frontend WeEasyTrip (Leaflet.js), Swap Modal and Re-optimize (/api/recompute), Tech stack (Python, FastAPI, Uvicorn, NumPy, Pydantic, Leaflet.js, Chart.js)

### Community 2 - "Frontend App Logic"
Cohesion: 0.06
Nodes (66): RFC-5545, addPoiToDay(), ALGO_HINTS, ALGO_NAMES, applySharedState(), buildIcs(), CAT_EMOJI, CAT_LABELS (+58 more)

### Community 3 - "Frontend Backup Copy"
Cohesion: 0.08
Nodes (38): addPoiToDay(), ALGO_HINTS, CAT_EMOJI, CAT_LABELS, closeSwapModal(), confirmSwap(), DAY_COLORS, drawOnMap() (+30 more)

### Community 4 - "FastAPI Backend"
Cohesion: 0.05
Nodes (39): apply_preferences(), build_package(), create_packages(), make_tier_pois(), _percentile(), create_session(), DayDetail, get_pois() (+31 more)

### Community 5 - "Experiments & Dataset (Report)"
Cohesion: 0.09
Nodes (23): Convergence plot of GA vs Hybrid, Experiment: 15 trials x 3 scenarios x 3 algorithms (135 trials), Kruskal-Wallis test (p<0.001), Results: Hybrid highest score in all scenarios, Runtime comparison (Greedy 8-18ms, Hybrid 120-270ms, GA 430-880ms), Scenarios S1, S2, S3, Chromosome Representation and Fitness, Genetic Algorithm (GA) (+15 more)

### Community 6 - "fetch_pois_osm.py"
Cohesion: 0.09
Nodes (18): clean_name(), collect(), coords(), diet_merge(), diet_tags(), extra(), main(), make_hotel() (+10 more)

### Community 7 - "Problem Formulation"
Cohesion: 0.13
Nodes (16): B-TOPTW with Meal Constraints, Constraints C1-C7 (budget, time, windows, hotel, flow, once, meals), OpenStreetMap / Overpass API data source, References (Vansteenwegen, Gunawan, Souffriau, Gavalas, Holland, OSM), User-System Interaction (packages, swap, evaluate_route), Kruskal-Wallis test (all p<0.001), Scenario S1_Short_Budget, Scenario S2_Medium_Standard (+8 more)

### Community 8 - "time"
Cohesion: 0.09
Nodes (23): hypervolume(), set_travel_profile(), build(), geocode(), load(), main(), hav(), main() (+15 more)

### Community 9 - "Frontend UI Structure"
Cohesion: 0.17
Nodes (15): flatpickr date picker library, Algorithm selector (Greedy, GA, Hybrid), closeProvDropdown, Detail section with day list and map (Step 3), filterProvince, index.html (WeEasyTrip landing page), Packages section (Step 2), Planner panel (Step 1 trip form) (+7 more)

### Community 10 - "System Architecture"
Cohesion: 0.32
Nodes (8): Algorithm Selector in Frontend, Backend API (FastAPI), Day Filter UX, API endpoints /api/health /api/packages /api/recompute, Algorithm Engine (Python), Frontend (HTML/JS/Leaflet.js), Leaflet.js, WeEasyTrip web system

### Community 11 - "Convergence Plot Results"
Cohesion: 0.38
Nodes (7): Convergence plot: WeEasyTrip GA vs Hybrid vs Greedy (fitness per generation across S1/S2/S3), GA (genetic algorithm) fitness curve, Greedy baseline (S1 148.1, S2 244.6, S3 346.7), Hybrid method fitness curve (high start, flat), S1 Short Budget scenario, S2 Medium Standard scenario, S3 Long Premium scenario

### Community 12 - "Packages & Swap Feature"
Cohesion: 0.50
Nodes (4): Custom package swap and re-optimize, Scoring Modes (ratio vs quality), Three packages (Budget/Standard/Premium), Tier-based Budget Allocation

### Community 15 - "genetic.py"
Cohesion: 0.08
Nodes (17): crossover(), fitness(), genetic_solve(), initial_population(), main(), mutate(), repair(), tournament_select() (+9 more)

### Community 16 - "Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study"
Cohesion: 0.27
Nodes (10): Ant Colony Optimization, Lin and Yu 2012 SA for TOPTW, Souffriau et al. 2008 GRASP for TOP, Vansteenwegen et al. 2009 ILS for TOPTW, Vansteenwegen et al. 2011 OP Survey, GRASP, Iterated Local Search, Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study (+2 more)

### Community 17 - "Orienteering Problem (OP)"
Cohesion: 0.18
Nodes (12): Budget-Constrained Team Orienteering Problem with Time Windows (B-TOPTW), Gunawan et al. 2016 OP Survey of Variants, NP-hard complexity, Orienteering Problem (OP), Traveling Salesman Problem (TSP), Team Orienteering Problem with Time Windows (TOPTW), NP-hard, Gunawan et al. (2016) Orienteering Problem survey (+4 more)

### Community 19 - "Special Project 2 future work"
Cohesion: 0.24
Nodes (10): Dynamic Pricing (Agoda/Booking.com), Greedy Seeding, Multi-objective Optimization (Pareto), Expansion to 77 Thai provinces, Google Places API opening hours / TripAdvisor ratings, Special Project 2 future work, Reinforcement Learning Agent for seeding, Expansion to 77 provinces (+2 more)

### Community 20 - "Algorithm Engine"
Cohesion: 0.25
Nodes (8): Phuket POI Dataset (164 POIs, 20 hotels), Algorithm Engine, OpenStreetMap / Overpass API, Three Trip Packages, POI Data Schema (phuket_pois.json), Tier-based Budget Allocation (Budget/Standard/Premium), Phuket POI dataset (164 POIs, 20 hotels), POI data structure (phuket_pois.json)

### Community 21 - "Greedy Algorithm (slot-based baseline)"
Cohesion: 0.43
Nodes (6): Per-day Budget Cap (1.8x average), Diversity Bonus, Free-Attraction Fallback Mechanism (4-tier), Greedy Algorithm (slot-based baseline), Forced Meal-Time Wait, Day Pattern (attr-attr-lunch-attr-attr-dinner)

### Community 22 - "Genetic Algorithm (GA)"
Cohesion: 0.22
Nodes (9): Gavalas et al. 2014 TTDP Survey, Goldberg 1989 Genetic Algorithms, Holland 1992 Adaptation in Natural and Artificial Systems, Chromosome Representation (list of lists of POI indices), Genetic Algorithm (GA), Penalty Function for Constraint Violation, Tabu Search, Tourist Trip Design Problem (TTDP) (+1 more)

### Community 23 - "Hybrid Algorithm (Greedy seed + GA + 2-opt)"
Cohesion: 0.50
Nodes (4): Day Pattern (attr-attr-lunch-attr-attr-dinner), GA Refinement (slot_repair, adaptive mutation, early stopping), Hybrid Algorithm (Greedy seed + GA + 2-opt), 2-opt Local Search

### Community 25 - "การดำเนินงาน"
Cohesion: 0.04
Nodes (45): Algorithm Selector ใน Frontend, Forced Meal-Time Wait, Free-Attraction Fallback Mechanism (สำคัญสำหรับงบจำกัด), Genetic Algorithm (GA), Greedy Algorithm, Hybrid Algorithm, Orienteering Problem (OP), Team Orienteering Problem with Time Windows (TOPTW) (+37 more)

## Knowledge Gaps
- **51 isolated node(s):** `RFC-5545`, `API endpoints /api/health /api/packages /api/recompute`, `Day Filter UX`, `Leaflet.js`, `S1 Short Budget scenario` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 247 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_packages()` connect `FastAPI Backend` to `Genetic Algorithm Core`, `time`, `Frontend App Logic`, `genetic.py`?**
  _High betweenness centrality (0.215) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `evaluate_route()` (e.g. with `make_day_details()` and `run_one()`) actually correct?**
  _`evaluate_route()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-5545`, `API endpoints /api/health /api/packages /api/recompute`, `Day Filter UX` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Genetic Algorithm Core` be split into smaller, more focused modules?**
  _Cohesion score 0.05054945054945055 - nodes in this community are weakly interconnected._
- **Why does `Hybrid Algorithm (Greedy seed + GA + 2-opt)` connect `Experiments & Dataset (Report)` to `Genetic Algorithm Core`, `Orienteering Problem (OP)`, `Special Project 2 future work`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `hybrid_solve()` (e.g. with `create_packages()` and `run_one()`) actually correct?**
  _`hybrid_solve()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `Frontend App Logic` be split into smaller, more focused modules?**
  _Cohesion score 0.0625694187338023 - nodes in this community are weakly interconnected._