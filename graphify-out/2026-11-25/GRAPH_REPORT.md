# Graph Report - Thesis Project  (2026-11-25)

## Corpus Check
- 186 files · ~548,707 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .css 1)

## Summary
- 928 nodes · 1751 edges · 98 communities (66 shown, 32 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 120 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6157083b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- greedy.py
- Results: Hybrid highest score in all scenarios
- app.js
- os
- main.py
- Experiments & Dataset (Report)
- fetch_pois_osm.py
- Problem Formulation
- run_experiments.py
- Frontend UI Structure
- System Architecture
- Convergence Plot Results
- Packages & Swap Feature
- Background Image
- Project Limitations
- genetic.py
- Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study
- TestAPI
- _prioritize_sights
- Special Project 2 future work
- statistics
- Greedy Algorithm (slot-based baseline)
- Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study
- pareto.py
- hybrid.py
- การดำเนินงาน
- utils.py
- create_packages
- การดำเนินงาน
- project2_plan.md
- make_figures.py
- ผลการทดลองหลายจังหวัดและการปรับแผนใหม่
- get_province
- reoptimize
- services
- pareto
- ผลการทดลองหลายจังหวัดและการปรับแผนใหม่
- extras.js
- json
- วิธีนำ WeEasyTrip ขึ้นเว็บให้คนอื่นใช้ (Render ฟรี)
- i18n.js
- sys
- tutorial.js
- showToast
- reshufflePackage
- Algorithm Engine
- rl_solve
- renderDetail
- ic
- limit_heavy
- buildIcs
- confirmSwap
- build_manual.py
- utils.py
- run_province_experiments.py
- get_provinces
- CS403_Report_68-2_33_pps-r1 Project 2_ffdbec9c.md
- CS403_Report_68-2_33_pps-r1 Project 2_แก้รายการ_52ebbc5c.md
- แนวคิดทฤษฎีที่เกี่ยวข้อง
- แนวคิดทฤษฎีที่เกี่ยวข้อง
- Hybrid Algorithm (Greedy seed + GA + 2-opt)
- ภาพรวมของโครงงาน
- งานวิจัยที่เกี่ยวข้อง
- ภาพรวมของโครงงาน
- งานวิจัยที่เกี่ยวข้อง
- สรุป
- สรุป
- run_all_realistic.sh
- run_ils_experiments.py

## God Nodes (most connected - your core abstractions)
1. `evaluate_route()` - 43 edges
2. `hybrid_solve()` - 26 edges
3. `create_packages()` - 23 edges
4. `greedy_solve()` - 21 edges
5. `การดำเนินงาน` - 20 edges
6. `การดำเนินงาน` - 20 edges
7. `reoptimize_solve()` - 19 edges
8. `genetic_solve()` - 16 edges
9. `renderDetail()` - 16 edges
10. `TestAPI` - 16 edges

## Surprising Connections (you probably didn't know these)
- `อัปเดต 6 พ.ย. 2569 — ข้อมูลครบ 77 จังหวัด` --references--> `collect()`  [INFERRED]
  docs/project2_plan.md → data/fetch_pois_osm.py
- `สถานะ (อัปเดต 24 ต.ค. 2569)` --references--> `reoptimize_solve()`  [INFERRED]
  docs/project2_plan.md → algorithm/hybrid.py
- `Runtime comparison (Greedy 8-18ms, Hybrid 120-270ms, GA 430-880ms)` --references--> `Hybrid Algorithm (Greedy seed + GA + 2-opt)`  [EXTRACTED]
  CS403_Report_68-2_33_pps-r1.pdf → docs/problem_formulation.md
- `Reinforcement Learning Agent` --conceptually_related_to--> `Greedy Seeding`  [INFERRED]
  graphify-out/converted/CS403_Report_68-2_33_pps-r1_280c1df9.md → CS403_Report_68-2_33_pps-r1.pdf
- `run()` --calls--> `evaluate_route()`  [INFERRED]
  experiments/run_phichit_cause.py → algorithm/utils.py

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

## Communities (98 total, 32 thin omitted)

### Community 0 - "greedy.py"
Cohesion: 0.12
Nodes (10): _find_best_for_slot(), greedy_solve(), _repaired(), episode_reward(), evaluate_route(), haversine_km(), travel_cost(), travel_time_min() (+2 more)

### Community 1 - "Results: Hybrid highest score in all scenarios"
Cohesion: 0.33
Nodes (7): Convergence plot of GA vs Hybrid, Experiment: 15 trials x 3 scenarios x 3 algorithms (135 trials), Kruskal-Wallis test (p<0.001), Results: Hybrid highest score in all scenarios, Runtime comparison (Greedy 8-18ms, Hybrid 120-270ms, GA 430-880ms), Scenarios S1, S2, S3, Experiment: 135 trials, 15 per scenario

### Community 2 - "app.js"
Cohesion: 0.06
Nodes (32): RFC-5545, addPoiToDay(), ALGO_HINTS, ALGO_NAMES, CAT_ICON, CAT_LABELS, DAY_COLORS, fpLocale() (+24 more)

### Community 3 - "os"
Cohesion: 0.39
Nodes (5): _session_save(), chedi(), main(), make(), ridge()

### Community 4 - "main.py"
Cohesion: 0.13
Nodes (8): create_session(), get_session(), _session_gc(), _session_load(), _session_view(), SessionCreate, SessionUpdate, update_session()

### Community 5 - "Experiments & Dataset (Report)"
Cohesion: 0.13
Nodes (16): Chromosome Representation and Fitness, Genetic Algorithm (GA), Greedy Algorithm (Baseline), Hybrid Algorithm (Greedy seed + GA + 2-opt), 2-opt Local Search, Hybrid highest mean score in all scenarios, Convergence graphs of GA and Hybrid, GRASP (+8 more)

### Community 6 - "fetch_pois_osm.py"
Cohesion: 0.09
Nodes (18): clean_name(), collect(), coords(), diet_merge(), diet_tags(), extra(), main(), make_hotel() (+10 more)

### Community 7 - "Problem Formulation"
Cohesion: 0.13
Nodes (16): B-TOPTW with Meal Constraints, Constraints C1-C7 (budget, time, windows, hotel, flow, once, meals), OpenStreetMap / Overpass API data source, References (Vansteenwegen, Gunawan, Souffriau, Gavalas, Holland, OSM), User-System Interaction (packages, swap, evaluate_route), Kruskal-Wallis test (all p<0.001), Scenario S1_Short_Budget, Scenario S2_Medium_Standard (+8 more)

### Community 8 - "run_experiments.py"
Cohesion: 0.16
Nodes (8): activity_budget(), _avg_history(), kruskal_wallis(), main(), plot_convergence(), print_summary(), stats_summary(), write_stats_report()

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
Cohesion: 0.16
Nodes (8): crossover(), fitness(), genetic_solve(), initial_population(), main(), mutate(), repair(), tournament_select()

### Community 16 - "Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study"
Cohesion: 0.15
Nodes (15): Budget-Constrained Team Orienteering Problem with Time Windows (B-TOPTW), Gunawan et al. 2016 OP Survey of Variants, Souffriau et al. 2008 GRASP for TOP, GRASP, NP-hard complexity, Orienteering Problem (OP), Team Orienteering Problem with Time Windows (TOPTW), Traveling Salesman Problem (TSP) (+7 more)

### Community 17 - "TestAPI"
Cohesion: 0.08
Nodes (3): act_budget(), TestAlgorithms, TestAPI

### Community 18 - "_prioritize_sights"
Cohesion: 0.28
Nodes (5): dist(), _prioritize_sights(), add_best(), nearer_meals(), _trim_to_budget()

### Community 19 - "Special Project 2 future work"
Cohesion: 0.24
Nodes (10): Dynamic Pricing (Agoda/Booking.com), Greedy Seeding, Multi-objective Optimization (Pareto), Expansion to 77 Thai provinces, Google Places API opening hours / TripAdvisor ratings, Special Project 2 future work, Reinforcement Learning Agent for seeding, Expansion to 77 provinces (+2 more)

### Community 20 - "statistics"
Cohesion: 0.23
Nodes (7): run(), share(), main_(), run(), apply(), main(), one()

### Community 21 - "Greedy Algorithm (slot-based baseline)"
Cohesion: 0.43
Nodes (6): Per-day Budget Cap (1.8x average), Diversity Bonus, Free-Attraction Fallback Mechanism (4-tier), Greedy Algorithm (slot-based baseline), Forced Meal-Time Wait, Day Pattern (attr-attr-lunch-attr-attr-dinner)

### Community 22 - "Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study"
Cohesion: 0.17
Nodes (14): Ant Colony Optimization, Gavalas et al. 2014 TTDP Survey, Goldberg 1989 Genetic Algorithms, Holland 1992 Adaptation in Natural and Artificial Systems, Lin and Yu 2012 SA for TOPTW, Vansteenwegen et al. 2011 OP Survey, Chromosome Representation (list of lists of POI indices), Genetic Algorithm (GA) (+6 more)

### Community 23 - "pareto.py"
Cohesion: 0.11
Nodes (13): _crossover(), diversity_stats(), _mutate(), _slot_repair(), _crowding(), _dominates(), evaluate_objectives(), hypervolume() (+5 more)

### Community 24 - "hybrid.py"
Cohesion: 0.12
Nodes (14): _budget_repair(), _final_validity(), _fitness(), hybrid_solve(), infeasible_locks(), main(), meal_fill(), reoptimize_solve() (+6 more)

### Community 25 - "การดำเนินงาน"
Cohesion: 0.10
Nodes (20): Free-Attraction Fallback Mechanism (สำคัญสำหรับงบจำกัด), Hybrid Algorithm, Insertion Local Search (ILS), กติกาความสมจริงของแผนรายวันและตัวตรวจแผนกลาง, การขยายข้อมูลหลายจังหวัด, การจัดการ Constraint Violation, การจัดเตรียมฮาร์ดแวร์และซอฟต์แวร์, การดำเนินงาน (+12 more)

### Community 26 - "utils.py"
Cohesion: 0.29
Nodes (5): day_objective(), _has_room(), insertion_local_search(), kind(), local_search()

### Community 27 - "create_packages"
Cohesion: 0.32
Nodes (6): create_packages(), find_best_hotel(), make_tier_pois(), _median_dist(), _percentile(), งานตรวจรอบสุดท้าย (25 ต.ค. 2569)

### Community 28 - "การดำเนินงาน"
Cohesion: 0.10
Nodes (20): Free-Attraction Fallback Mechanism (สำคัญสำหรับงบจำกัด), Hybrid Algorithm, Insertion Local Search (ILS), กติกาความสมจริงของแผนรายวันและตัวตรวจแผนกลาง, การขยายข้อมูลหลายจังหวัด, การจัดการ Constraint Violation, การจัดเตรียมฮาร์ดแวร์และซอฟต์แวร์, การดำเนินงาน (+12 more)

### Community 29 - "project2_plan.md"
Cohesion: 0.11
Nodes (17): 9 พ.ย. 2569 (ต่อ 2), 9 พ.ย. 2569 (ต่อ 3), 9 พ.ย. 2569 (ต่อ) — UI และงานปิดท้าย, 9 พ.ย. 2569 — รันการทดลองทั้งหมดใหม่หลังปรับเวลาเดินทางให้สมจริง (เสร็จ), ILS (Insertion Local Search) — เปิดใช้ใน Hybrid แล้ว, ILS (Insertion Local Search) — เปิดใช้ใน Hybrid แล้ว, ความเสี่ยง, สถานะปัจจุบันของโค้ด (ที่มีผลต่อแผน) (+9 more)

### Community 30 - "make_figures.py"
Cohesion: 0.18
Nodes (15): diag(), save(), scores(), tradeoff(), fig_chromosome(), fig_reopt(), fig_usecase(), arrow() (+7 more)

### Community 31 - "ผลการทดลองหลายจังหวัดและการปรับแผนใหม่"
Cohesion: 0.17
Nodes (12): Insertion Local Search, Reinforcement Learning, การปรับแผนใหม่หลังผู้ใช้แก้ไข, การออกแบบการทดลอง, คุณภาพของข้อมูลที่สร้างอัตโนมัติ, ความชอบของผู้ใช้, ความไวต่อพารามิเตอร์, จังหวัดข้อมูลน้อยและทริปข้ามจังหวัด (+4 more)

### Community 32 - "get_province"
Cohesion: 0.22
Nodes (6): _combo(), dev_check(), get_pois(), get_province(), health(), is_dev()

### Community 33 - "reoptimize"
Cohesion: 0.22
Nodes (6): apply_preferences(), Preferences, reoptimize(), ReoptimizeRequest, restore_originals(), สถานะ (อัปเดต 24 ต.ค. 2569)

### Community 34 - "services"
Cohesion: 0.22
Nodes (8): key, sync, services, envVars, name, plan, runtime, type

### Community 36 - "pareto"
Cohesion: 0.20
Nodes (10): build_package(), DayDetail, make_day_details(), Package, PackageRequest, PackageResponse, pareto(), recompute() (+2 more)

### Community 37 - "ผลการทดลองหลายจังหวัดและการปรับแผนใหม่"
Cohesion: 0.17
Nodes (12): Insertion Local Search, Reinforcement Learning, การปรับแผนใหม่หลังผู้ใช้แก้ไข, การออกแบบการทดลอง, คุณภาพของข้อมูลที่สร้างอัตโนมัติ, ความชอบของผู้ใช้, ความไวต่อพารามิเตอร์, จังหวัดข้อมูลน้อยและทริปข้ามจังหวัด (+4 more)

### Community 38 - "extras.js"
Cohesion: 0.12
Nodes (21): add(), applyProvince(), buildTips(), decorateWeather(), enableDrag(), generalTips(), initTips(), loadWeather() (+13 more)

### Community 40 - "json"
Cohesion: 0.22
Nodes (9): build(), geocode(), load(), main(), reeval(), verdict(), hav(), main() (+1 more)

### Community 41 - "วิธีนำ WeEasyTrip ขึ้นเว็บให้คนอื่นใช้ (Render ฟรี)"
Cohesion: 0.40
Nodes (4): ขั้นตอน (ผู้ใช้ทำเอง — ต้องมีบัญชี GitHub และ Render), ข้อจำกัดของแผนฟรี, รันในเครื่องแบบบริการเดียว, วิธีนำ WeEasyTrip ขึ้นเว็บให้คนอื่นใช้ (Render ฟรี)

### Community 42 - "i18n.js"
Cohesion: 0.70
Nodes (4): apply(), inline(), run(), tr()

### Community 43 - "sys"
Cohesion: 0.14
Nodes (3): run(), main(), score()

### Community 44 - "tutorial.js"
Cohesion: 0.64
Nodes (7): build(), close(), go(), place(), placeSoon(), resetLanding(), start()

### Community 45 - "showToast"
Cohesion: 0.21
Nodes (16): applySharedState(), closePareto(), drawOnMap(), joinSession(), loadPois(), onProvinceChange(), pushSession(), redoEdit() (+8 more)

### Community 46 - "reshufflePackage"
Cohesion: 0.19
Nodes (16): devHeaders(), devToken(), fitDetail(), fmt(), getPreferences(), getSelectedDays(), highlightField(), initBudgetValidation() (+8 more)

### Community 47 - "Algorithm Engine"
Cohesion: 0.20
Nodes (12): Backend API (FastAPI), Phuket POI Dataset (164 POIs, 20 hotels), Algorithm Engine, Frontend WeEasyTrip (Leaflet.js), OpenStreetMap / Overpass API, Three Trip Packages, POI Data Schema (phuket_pois.json), Swap Modal and Re-optimize (/api/recompute) (+4 more)

### Community 48 - "rl_solve"
Cohesion: 0.33
Nodes (3): features(), rl_solve(), chooser()

### Community 49 - "renderDetail"
Cohesion: 0.26
Nodes (13): arriveOf(), fmtClock(), fmtDur(), getProvince(), gmapsUrl(), haversineKm(), hoursText(), loadProvinces() (+5 more)

### Community 50 - "ic"
Cohesion: 0.38
Nodes (7): ic(), initPrefs(), onHotelToggle(), setOneDayTripMode(), toggleHotelOption(), updateDateSummary(), updatePrefSummary()

### Community 51 - "limit_heavy"
Cohesion: 0.25
Nodes (4): dev_unlock(), limit_heavy(), revalidate_static(), UnlockRequest

### Community 52 - "buildIcs"
Cohesion: 0.50
Nodes (4): buildIcs(), exportIcs(), icsEscape(), icsFold()

### Community 53 - "confirmSwap"
Cohesion: 0.50
Nodes (5): closeSwapModal(), confirmSwap(), removePoi(), restoreEdit(), snapshotEdit()

### Community 55 - "build_manual.py"
Cohesion: 0.12
Nodes (14): add_bookmark(), add_link(), build(), build_index(), defs_in(), docname(), para_fmt(), parse_spec() (+6 more)

### Community 81 - "utils.py"
Cohesion: 0.18
Nodes (8): load_data(), set_travel_profile(), load(), part1(), part2(), load(), load(), run()

### Community 83 - "run_province_experiments.py"
Cohesion: 0.36
Nodes (5): min_meals(), part_a(), part_b(), setup(), summarize()

### Community 84 - "get_provinces"
Cohesion: 0.33
Nodes (3): get_provinces(), _max_days(), _neighbors()

### Community 85 - "CS403_Report_68-2_33_pps-r1 Project 2_ffdbec9c.md"
Cohesion: 0.20
Nodes (9): การทดสอบซอฟต์แวร์, ข้อจำกัดของโครงงาน, ขอบเขตของโครงงาน, ความก้าวหน้าของโครงงานพิเศษ 2, ความเป็นมาและความสำคัญของโครงงาน, ประโยชน์ของโครงงาน, ผลการดำเนินงาน, ระบบต้นแบบและผลลัพธ์เบื้องต้น (+1 more)

### Community 86 - "CS403_Report_68-2_33_pps-r1 Project 2_แก้รายการ_52ebbc5c.md"
Cohesion: 0.20
Nodes (9): การทดสอบซอฟต์แวร์, ข้อจำกัดของโครงงาน, ขอบเขตของโครงงาน, ความก้าวหน้าของโครงงานพิเศษ 2, ความเป็นมาและความสำคัญของโครงงาน, ประโยชน์ของโครงงาน, ผลการดำเนินงาน, ระบบต้นแบบและผลลัพธ์เบื้องต้น (+1 more)

### Community 87 - "แนวคิดทฤษฎีที่เกี่ยวข้อง"
Cohesion: 0.25
Nodes (8): Genetic Algorithm (GA), Greedy Algorithm, Iterated Local Search (ILS), Multi-objective Optimization และ NSGA-II, Orienteering Problem (OP), Reinforcement Learning และ REINFORCE, Team Orienteering Problem with Time Windows (TOPTW), แนวคิดทฤษฎีที่เกี่ยวข้อง

### Community 88 - "แนวคิดทฤษฎีที่เกี่ยวข้อง"
Cohesion: 0.25
Nodes (8): Genetic Algorithm (GA), Greedy Algorithm, Iterated Local Search (ILS), Multi-objective Optimization และ NSGA-II, Orienteering Problem (OP), Reinforcement Learning และ REINFORCE, Team Orienteering Problem with Time Windows (TOPTW), แนวคิดทฤษฎีที่เกี่ยวข้อง

### Community 89 - "Hybrid Algorithm (Greedy seed + GA + 2-opt)"
Cohesion: 0.33
Nodes (6): Vansteenwegen et al. 2009 ILS for TOPTW, Day Pattern (attr-attr-lunch-attr-attr-dinner), GA Refinement (slot_repair, adaptive mutation, early stopping), Hybrid Algorithm (Greedy seed + GA + 2-opt), Iterated Local Search, 2-opt Local Search

### Community 90 - "ภาพรวมของโครงงาน"
Cohesion: 0.33
Nodes (6): Workflow การใช้งาน, การจัดสรรงบประมาณตาม Tier, การวิเคราะห์ขอบเขตและความต้องการของระบบ, ภาพรวมของโครงงาน, วิธีการวิจัย, สถาปัตยกรรมของระบบ

### Community 91 - "งานวิจัยที่เกี่ยวข้อง"
Cohesion: 0.33
Nodes (6): ความแตกต่างของโครงงานนี้กับงานวิจัยข้างต้น, งานวิจัยของ Gavalas และคณะ (2014), งานวิจัยของ Souffriau และคณะ (2008), งานวิจัยของ Vansteenwegen และคณะ (2011), งานวิจัยที่เกี่ยวข้อง, วรรณกรรมและงานวิจัยที่เกี่ยวข้อง

### Community 92 - "ภาพรวมของโครงงาน"
Cohesion: 0.33
Nodes (6): Workflow การใช้งาน, การจัดสรรงบประมาณตาม Tier, การวิเคราะห์ขอบเขตและความต้องการของระบบ, ภาพรวมของโครงงาน, วิธีการวิจัย, สถาปัตยกรรมของระบบ

### Community 93 - "งานวิจัยที่เกี่ยวข้อง"
Cohesion: 0.33
Nodes (6): ความแตกต่างของโครงงานนี้กับงานวิจัยข้างต้น, งานวิจัยของ Gavalas และคณะ (2014), งานวิจัยของ Souffriau และคณะ (2008), งานวิจัยของ Vansteenwegen และคณะ (2011), งานวิจัยที่เกี่ยวข้อง, วรรณกรรมและงานวิจัยที่เกี่ยวข้อง

### Community 94 - "สรุป"
Cohesion: 0.40
Nodes (5): ข้อจำกัดของผลงาน, ข้อเสนอแนะและแนวทางต่อยอด, สรุป, สรุปผลการดำเนินงาน, อภิปรายผล

### Community 95 - "สรุป"
Cohesion: 0.40
Nodes (5): ข้อจำกัดของผลงาน, ข้อเสนอแนะและแนวทางต่อยอด, สรุป, สรุปผลการดำเนินงาน, อภิปรายผล

### Community 96 - "run_all_realistic.sh"
Cohesion: 0.50
Nodes (3): PYTHONIOENCODING, PYTHONUNBUFFERED, run_all_realistic.sh script

## Knowledge Gaps
- **55 isolated node(s):** `PYTHONIOENCODING`, `PYTHONUNBUFFERED`, `PYTHONIOENCODING`, `PYTHONUNBUFFERED`, `RFC-5545` (+50 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 423 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_packages()` connect `create_packages` to `greedy.py`, `reoptimize`, `get_province`, `app.js`, `main.py`, `pareto`, `json`, `genetic.py`, `_prioritize_sights`, `limit_heavy`, `hybrid.py`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `evaluate_route()` (e.g. with `make_day_details()` and `part1()`) actually correct?**
  _`evaluate_route()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `PYTHONIOENCODING`, `PYTHONUNBUFFERED`, `PYTHONIOENCODING` to the rest of the system?**
  _55 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `greedy.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1206896551724138 - nodes in this community are weakly interconnected._
- **Why does `Hybrid Algorithm (Greedy seed + GA + 2-opt)` connect `Experiments & Dataset (Report)` to `hybrid.py`, `Results: Hybrid highest score in all scenarios`, `Special Project 2 future work`, `Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `hybrid_solve()` (e.g. with `create_packages()` and `run_one()`) actually correct?**
  _`hybrid_solve()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Should `app.js` be split into smaller, more focused modules?**
  _Cohesion score 0.06463414634146342 - nodes in this community are weakly interconnected._