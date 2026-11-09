# Graph Report - Thesis Project  (2026-11-06)

## Corpus Check
- 124 files · ~308,393 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: .ics 2, .css 1)

## Summary
- 661 nodes · 1334 edges · 41 communities (38 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- evaluate_route
- CS403_Report_68-2_33_pps-r1 Project 2_ffdbec9c.md
- Frontend App Logic
- Frontend Backup Copy
- main.py
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
- Team Orienteering Problem with Time Windows (TOPTW)
- CLAUDE.md
- Special Project 2 future work
- Algorithm Engine
- Greedy Algorithm (slot-based baseline)
- Genetic Algorithm (GA)
- pareto.py
- hybrid_solve
- การดำเนินงาน
- ils.py
- rl.py
- Results: Hybrid highest score in all scenarios
- project2_plan.md
- run_all_realistic.sh
- Tourist Trip Design Problem (TTDP)
- create_packages
- reoptimize
- pareto
- get_province
- get_provinces
- วิธีการวิจัย
- extras.js
- งานวิจัยที่เกี่ยวข้อง
- แนวคิดทฤษฎีที่เกี่ยวข้อง

## God Nodes (most connected - your core abstractions)
1. `evaluate_route()` - 37 edges
2. `การดำเนินงาน` - 25 edges
3. `hybrid_solve()` - 22 edges
4. `create_packages()` - 20 edges
5. `greedy_solve()` - 19 edges
6. `reoptimize_solve()` - 17 edges
7. `genetic_solve()` - 15 edges
8. `showToast()` - 15 edges
9. `meal_fill()` - 14 edges
10. `nsga2_solve()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `อัปเดต 6 พ.ย. 2569 — ข้อมูลครบ 77 จังหวัด` --references--> `collect()`  [INFERRED]
  docs/project2_plan.md → data/fetch_pois_osm.py
- `สถานะ (อัปเดต 24 ต.ค. 2569)` --references--> `reoptimize_solve()`  [INFERRED]
  docs/project2_plan.md → algorithm/hybrid.py
- `Vansteenwegen et al. (2011) The Orienteering Problem: A Survey` --cites--> `Orienteering Problem (OP)`  [EXTRACTED]
  graphify-out/converted/CS403_Report_68-2_33_pps-r1_280c1df9.md → CS403_Report_68-2_33_pps-r1.pdf
- `Reinforcement Learning Agent` --conceptually_related_to--> `Greedy Seeding`  [INFERRED]
  graphify-out/converted/CS403_Report_68-2_33_pps-r1_280c1df9.md → CS403_Report_68-2_33_pps-r1.pdf
- `Runtime comparison (Greedy 8-18ms, Hybrid 120-270ms, GA 430-880ms)` --references--> `Hybrid Algorithm (Greedy seed + GA + 2-opt)`  [EXTRACTED]
  CS403_Report_68-2_33_pps-r1.pdf → docs/problem_formulation.md

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

## Communities (41 total, 3 thin omitted)

### Community 0 - "evaluate_route"
Cohesion: 0.20
Nodes (9): _find_best_for_slot(), greedy_solve(), _repaired(), meal_fill(), episode_reward(), evaluate_route(), haversine_km(), travel_cost() (+1 more)

### Community 1 - "CS403_Report_68-2_33_pps-r1 Project 2_ffdbec9c.md"
Cohesion: 0.18
Nodes (10): ข้อจำกัดของโครงงาน, ขอบเขตของโครงงาน, ความก้าวหน้าของโครงงานพิเศษ 2, ความเป็นมาและความสำคัญของโครงงาน, ประโยชน์ของโครงงาน, ผลการดำเนินงาน, ผลการทดลองหลายจังหวัดและการปรับแผนใหม่, ระบบต้นแบบและผลลัพธ์เบื้องต้น (+2 more)

### Community 2 - "Frontend App Logic"
Cohesion: 0.06
Nodes (74): RFC-5545, addPoiToDay(), ALGO_HINTS, ALGO_NAMES, applySharedState(), arriveOf(), buildIcs(), CAT_ICON (+66 more)

### Community 3 - "Frontend Backup Copy"
Cohesion: 0.08
Nodes (38): addPoiToDay(), ALGO_HINTS, CAT_EMOJI, CAT_LABELS, closeSwapModal(), confirmSwap(), DAY_COLORS, drawOnMap() (+30 more)

### Community 4 - "main.py"
Cohesion: 0.15
Nodes (8): create_session(), get_session(), _session_gc(), _session_load(), _session_view(), SessionCreate, SessionUpdate, update_session()

### Community 5 - "Experiments & Dataset (Report)"
Cohesion: 0.15
Nodes (13): Chromosome Representation and Fitness, Genetic Algorithm (GA), Greedy Algorithm (Baseline), Hybrid Algorithm (Greedy seed + GA + 2-opt), 2-opt Local Search, Hybrid highest mean score in all scenarios, Convergence graphs of GA and Hybrid, Metaheuristics (GA, SA, ACO) (+5 more)

### Community 6 - "fetch_pois_osm.py"
Cohesion: 0.07
Nodes (18): clean_name(), collect(), coords(), diet_merge(), diet_tags(), extra(), main(), make_hotel() (+10 more)

### Community 7 - "Problem Formulation"
Cohesion: 0.13
Nodes (16): B-TOPTW with Meal Constraints, Constraints C1-C7 (budget, time, windows, hotel, flow, once, meals), OpenStreetMap / Overpass API data source, References (Vansteenwegen, Gunawan, Souffriau, Gavalas, Holland, OSM), User-System Interaction (packages, swap, evaluate_route), Kruskal-Wallis test (all p<0.001), Scenario S1_Short_Budget, Scenario S2_Medium_Standard (+8 more)

### Community 8 - "time"
Cohesion: 0.06
Nodes (34): set_travel_profile(), _session_save(), build(), geocode(), load(), main(), reeval(), verdict() (+26 more)

### Community 9 - "Frontend UI Structure"
Cohesion: 0.17
Nodes (15): flatpickr date picker library, Algorithm selector (Greedy, GA, Hybrid), closeProvDropdown, Detail section with day list and map (Step 3), filterProvince, index.html (WeEasyTrip landing page), Packages section (Step 2), Planner panel (Step 1 trip form) (+7 more)

### Community 10 - "System Architecture"
Cohesion: 0.23
Nodes (12): Backend API (FastAPI), Frontend WeEasyTrip (Leaflet.js), Algorithm Selector in Frontend, Swap Modal and Re-optimize (/api/recompute), Tech stack (Python, FastAPI, Uvicorn, NumPy, Pydantic, Leaflet.js, Chart.js), Backend API (FastAPI), Day Filter UX, API endpoints /api/health /api/packages /api/recompute (+4 more)

### Community 11 - "Convergence Plot Results"
Cohesion: 0.38
Nodes (7): Convergence plot: WeEasyTrip GA vs Hybrid vs Greedy (fitness per generation across S1/S2/S3), GA (genetic algorithm) fitness curve, Greedy baseline (S1 148.1, S2 244.6, S3 346.7), Hybrid method fitness curve (high start, flat), S1 Short Budget scenario, S2 Medium Standard scenario, S3 Long Premium scenario

### Community 12 - "Packages & Swap Feature"
Cohesion: 0.50
Nodes (4): Custom package swap and re-optimize, Scoring Modes (ratio vs quality), Three packages (Budget/Standard/Premium), Tier-based Budget Allocation

### Community 15 - "genetic.py"
Cohesion: 0.16
Nodes (8): crossover(), fitness(), genetic_solve(), initial_population(), mutate(), repair(), tournament_select(), _time_repair()

### Community 16 - "Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study"
Cohesion: 0.17
Nodes (16): Ant Colony Optimization, Gunawan et al. 2016 OP Survey of Variants, Lin and Yu 2012 SA for TOPTW, Souffriau et al. 2008 GRASP for TOP, Vansteenwegen et al. 2009 ILS for TOPTW, Vansteenwegen et al. 2011 OP Survey, GRASP, Iterated Local Search (+8 more)

### Community 17 - "Team Orienteering Problem with Time Windows (TOPTW)"
Cohesion: 0.33
Nodes (6): Team Orienteering Problem with Time Windows (TOPTW), GRASP, Greedy Algorithm (baseline, slot-based), Lin and Yu (2012) Simulated Annealing for TOPTW, Souffriau et al. (2008) GRASP for Team Orienteering, Vansteenwegen et al. (2009) Iterated Local Search for TOPTW

### Community 19 - "Special Project 2 future work"
Cohesion: 0.24
Nodes (10): Dynamic Pricing (Agoda/Booking.com), Greedy Seeding, Multi-objective Optimization (Pareto), Expansion to 77 Thai provinces, Google Places API opening hours / TripAdvisor ratings, Special Project 2 future work, Reinforcement Learning Agent for seeding, Expansion to 77 provinces (+2 more)

### Community 20 - "Algorithm Engine"
Cohesion: 0.25
Nodes (8): Budget-Constrained Team Orienteering Problem with Time Windows (B-TOPTW), Phuket POI Dataset (164 POIs, 20 hotels), OpenStreetMap / Overpass API, POI Data Schema (phuket_pois.json), Phuket POI dataset (164 POIs, 20 hotels), POI data structure (phuket_pois.json), Vansteenwegen et al. (2011) The Orienteering Problem: A Survey, Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study

### Community 21 - "Greedy Algorithm (slot-based baseline)"
Cohesion: 0.43
Nodes (6): Per-day Budget Cap (1.8x average), Diversity Bonus, Free-Attraction Fallback Mechanism (4-tier), Greedy Algorithm (slot-based baseline), Forced Meal-Time Wait, Day Pattern (attr-attr-lunch-attr-attr-dinner)

### Community 22 - "Genetic Algorithm (GA)"
Cohesion: 0.17
Nodes (12): Goldberg 1989 Genetic Algorithms, Holland 1992 Adaptation in Natural and Artificial Systems, Chromosome Representation (list of lists of POI indices), Day Pattern (attr-attr-lunch-attr-attr-dinner), Algorithm Engine, Genetic Algorithm (GA), GA Refinement (slot_repair, adaptive mutation, early stopping), Hybrid Algorithm (Greedy seed + GA + 2-opt) (+4 more)

### Community 23 - "pareto.py"
Cohesion: 0.13
Nodes (11): _crossover(), diversity_stats(), _mutate(), _slot_repair(), _crowding(), _dominates(), evaluate_objectives(), hypervolume() (+3 more)

### Community 24 - "hybrid_solve"
Cohesion: 0.12
Nodes (12): main(), _budget_repair(), _final_validity(), _fitness(), hybrid_solve(), infeasible_locks(), main(), reoptimize_solve() (+4 more)

### Community 25 - "การดำเนินงาน"
Cohesion: 0.08
Nodes (25): Algorithm Selector ใน Frontend, Forced Meal-Time Wait, Free-Attraction Fallback Mechanism (สำคัญสำหรับงบจำกัด), Hybrid Algorithm, Insertion Local Search (ILS), Reinforcement Learning (REINFORCE), กติกาความสมจริงของแผนรายวัน (Project 2), การขยายข้อมูลหลายจังหวัด (+17 more)

### Community 26 - "ils.py"
Cohesion: 0.17
Nodes (6): day_objective(), _has_room(), insertion_local_search(), kind(), local_search(), split_attrs()

### Community 27 - "rl.py"
Cohesion: 0.32
Nodes (4): features(), rl_solve(), chooser(), train()

### Community 28 - "Results: Hybrid highest score in all scenarios"
Cohesion: 0.33
Nodes (7): Convergence plot of GA vs Hybrid, Experiment: 15 trials x 3 scenarios x 3 algorithms (135 trials), Kruskal-Wallis test (p<0.001), Results: Hybrid highest score in all scenarios, Runtime comparison (Greedy 8-18ms, Hybrid 120-270ms, GA 430-880ms), Scenarios S1, S2, S3, Experiment: 135 trials, 15 per scenario

### Community 29 - "project2_plan.md"
Cohesion: 0.17
Nodes (11): ILS (Insertion Local Search) — เปิดใช้ใน Hybrid แล้ว, ILS (Insertion Local Search) — เปิดใช้ใน Hybrid แล้ว, ความเสี่ยง, สถานะปัจจุบันของโค้ด (ที่มีผลต่อแผน), สถานะล่าสุด (27 ต.ค. 2569), อัปเดต 28 ต.ค. 2569, อัปเดต 6 พ.ย. 2569 — ข้อมูลครบ 77 จังหวัด, เฟส 2 — ปรับ Hybrid และ re-optimization (+3 more)

### Community 30 - "run_all_realistic.sh"
Cohesion: 0.50
Nodes (3): PYTHONIOENCODING, PYTHONUNBUFFERED, run_all_realistic.sh script

### Community 31 - "Tourist Trip Design Problem (TTDP)"
Cohesion: 0.67
Nodes (4): Gavalas et al. 2014 TTDP Survey, Tabu Search, Tourist Trip Design Problem (TTDP), Gavalas et al. (2014) Survey on TTDP

### Community 32 - "create_packages"
Cohesion: 0.16
Nodes (11): build_package(), create_packages(), find_best_hotel(), make_tier_pois(), _median_dist(), _percentile(), DayDetail, make_day_details() (+3 more)

### Community 33 - "reoptimize"
Cohesion: 0.22
Nodes (6): apply_preferences(), Preferences, reoptimize(), ReoptimizeRequest, restore_originals(), สถานะ (อัปเดต 24 ต.ค. 2569)

### Community 34 - "pareto"
Cohesion: 0.31
Nodes (6): PackageRequest, PackageResponse, pareto(), recompute(), RecomputeRequest, เฟส 1 — ขยายจังหวัด (เริ่มตรงนี้)

### Community 35 - "get_province"
Cohesion: 0.29
Nodes (4): _combo(), get_pois(), get_province(), health()

### Community 36 - "get_provinces"
Cohesion: 0.29
Nodes (3): get_provinces(), _max_days(), _neighbors()

### Community 37 - "วิธีการวิจัย"
Cohesion: 0.29
Nodes (7): Workflow การใช้งาน, การจัดสรรงบประมาณตาม Tier, การวิเคราะห์ขอบเขตและความต้องการของระบบ, ผลลัพธ์ที่คาดหวัง, ภาพรวมของโครงงาน, วิธีการวิจัย, สถาปัตยกรรมของระบบ

### Community 38 - "extras.js"
Cohesion: 0.22
Nodes (12): applyProvince(), buildTips(), initTips(), loadWeather(), makeModal(), refreshTips(), registerCombo(), renderNeighbors() (+4 more)

### Community 39 - "งานวิจัยที่เกี่ยวข้อง"
Cohesion: 0.33
Nodes (6): ความแตกต่างของโครงงานนี้กับงานวิจัยข้างต้น, งานวิจัยของ Gavalas และคณะ (2014), งานวิจัยของ Souffriau และคณะ (2008), งานวิจัยของ Vansteenwegen และคณะ (2009), งานวิจัยที่เกี่ยวข้อง, วรรณกรรมและงานวิจัยที่เกี่ยวข้อง

### Community 40 - "แนวคิดทฤษฎีที่เกี่ยวข้อง"
Cohesion: 0.40
Nodes (5): Genetic Algorithm (GA), Greedy Algorithm, Orienteering Problem (OP), Team Orienteering Problem with Time Windows (TOPTW), แนวคิดทฤษฎีที่เกี่ยวข้อง

## Knowledge Gaps
- **53 isolated node(s):** `PYTHONIOENCODING`, `PYTHONUNBUFFERED`, `RFC-5545`, `API endpoints /api/health /api/packages /api/recompute`, `Day Filter UX` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 271 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_packages()` connect `create_packages` to `evaluate_route`, `reoptimize`, `pareto`, `get_province`, `main.py`, `Frontend App Logic`, `time`, `genetic.py`, `hybrid_solve`?**
  _High betweenness centrality (0.237) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `evaluate_route()` (e.g. with `make_day_details()` and `run_one()`) actually correct?**
  _`evaluate_route()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `PYTHONIOENCODING`, `PYTHONUNBUFFERED`, `RFC-5545` to the rest of the system?**
  _53 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Frontend App Logic` be split into smaller, more focused modules?**
  _Cohesion score 0.05789009697325889 - nodes in this community are weakly interconnected._
- **Why does `Hybrid Algorithm (Greedy seed + GA + 2-opt)` connect `Experiments & Dataset (Report)` to `Team Orienteering Problem with Time Windows (TOPTW)`, `Special Project 2 future work`, `Algorithm Engine`, `hybrid_solve`, `Results: Hybrid highest score in all scenarios`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `hybrid_solve()` (e.g. with `create_packages()` and `run_one()`) actually correct?**
  _`hybrid_solve()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `Frontend Backup Copy` be split into smaller, more focused modules?**
  _Cohesion score 0.08282828282828283 - nodes in this community are weakly interconnected._