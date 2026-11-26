# Graph Report - Thesis Project  (2026-10-24)

## Corpus Check
- 23 files · ~32,577 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 374 nodes · 663 edges · 15 communities (13 shown, 2 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Genetic Algorithm Core
- Research Theory & Literature
- Frontend App Logic
- Frontend Backup Copy
- FastAPI Backend
- Experiments & Dataset (Report)
- OSM POI Fetching
- Problem Formulation
- Experiment Scripts
- Frontend UI Structure
- System Architecture
- Convergence Plot Results
- Packages & Swap Feature
- Background Image
- Project Limitations

## God Nodes (most connected - your core abstractions)
1. `evaluate_route()` - 17 edges
2. `create_packages()` - 17 edges
3. `genetic_solve()` - 14 edges
4. `hybrid_solve()` - 14 edges
5. `Genetic Algorithm (GA)` - 14 edges
6. `main()` - 13 edges
7. `Budget-Aware Travel Route Generation and Optimization Using AI: Phuket Case Study` - 13 edges
8. `greedy_solve()` - 12 edges
9. `Hybrid Algorithm (Greedy seed + GA + 2-opt)` - 12 edges
10. `meal_fill()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Reinforcement Learning Agent` --conceptually_related_to--> `Greedy Seeding`  [INFERRED]
  graphify-out/converted/CS403_Report_68-2_33_pps-r1_280c1df9.md → CS403_Report_68-2_33_pps-r1.pdf
- `Runtime comparison (Greedy 8-18ms, Hybrid 120-270ms, GA 430-880ms)` --references--> `Hybrid Algorithm (Greedy seed + GA + 2-opt)`  [EXTRACTED]
  CS403_Report_68-2_33_pps-r1.pdf → docs/problem_formulation.md
- `Hybrid Algorithm (Greedy seed + GA + 2-opt)` --references--> `Greedy Seeding`  [EXTRACTED]
  docs/problem_formulation.md → CS403_Report_68-2_33_pps-r1.pdf
- `Frontend (HTML/JS/Leaflet.js)` --references--> `Algorithm Selector in Frontend`  [EXTRACTED]
  graphify-out/converted/CS403_Report_68-2_33_pps-r1_280c1df9.md → CS403_Report_68-2_33_pps-r1.pdf
- `Free-Attraction Fallback Mechanism (4-tier)` --conceptually_related_to--> `Day Pattern (attr-attr-lunch-attr-attr-dinner)`  [INFERRED]
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

## Communities (15 total, 2 thin omitted)

### Community 0 - "Genetic Algorithm Core"
Cohesion: 0.08
Nodes (28): crossover(), fitness(), genetic_solve(), initial_population(), main(), mutate(), repair(), tournament_select() (+20 more)

### Community 1 - "Research Theory & Literature"
Cohesion: 0.05
Nodes (54): Ant Colony Optimization, Budget-Constrained Team Orienteering Problem with Time Windows (B-TOPTW), Per-day Budget Cap (1.8x average), Gavalas et al. 2014 TTDP Survey, Goldberg 1989 Genetic Algorithms, Gunawan et al. 2016 OP Survey of Variants, Holland 1992 Adaptation in Natural and Artificial Systems, Lin and Yu 2012 SA for TOPTW (+46 more)

### Community 2 - "Frontend App Logic"
Cohesion: 0.08
Nodes (40): addPoiToDay(), ALGO_HINTS, ALGO_NAMES, CAT_EMOJI, CAT_LABELS, closeSwapModal(), confirmSwap(), DAY_COLORS (+32 more)

### Community 3 - "Frontend Backup Copy"
Cohesion: 0.08
Nodes (38): addPoiToDay(), ALGO_HINTS, CAT_EMOJI, CAT_LABELS, closeSwapModal(), confirmSwap(), DAY_COLORS, drawOnMap() (+30 more)

### Community 4 - "FastAPI Backend"
Cohesion: 0.09
Nodes (14): build_package(), create_packages(), make_tier_pois(), _percentile(), DayDetail, get_pois(), health(), make_day_details() (+6 more)

### Community 5 - "Experiments & Dataset (Report)"
Cohesion: 0.08
Nodes (28): Convergence plot of GA vs Hybrid, Phuket POI Dataset (164 POIs, 20 hotels), Experiment: 15 trials x 3 scenarios x 3 algorithms (135 trials), Kruskal-Wallis test (p<0.001), OpenStreetMap / Overpass API, POI Data Schema (phuket_pois.json), Results: Hybrid highest score in all scenarios, Runtime comparison (Greedy 8-18ms, Hybrid 120-270ms, GA 430-880ms) (+20 more)

### Community 6 - "OSM POI Fetching"
Cohesion: 0.14
Nodes (6): main(), make_poi(), overpass_query(), add_pois(), load(), save()

### Community 7 - "Problem Formulation"
Cohesion: 0.13
Nodes (16): B-TOPTW with Meal Constraints, Constraints C1-C7 (budget, time, windows, hotel, flow, once, meals), OpenStreetMap / Overpass API data source, References (Vansteenwegen, Gunawan, Souffriau, Gavalas, Holland, OSM), User-System Interaction (packages, swap, evaluate_route), Kruskal-Wallis test (all p<0.001), Scenario S1_Short_Budget, Scenario S2_Medium_Standard (+8 more)

### Community 8 - "Experiment Scripts"
Cohesion: 0.15
Nodes (7): activity_budget(), _avg_history(), main(), plot_convergence(), print_summary(), stats_summary(), write_stats_report()

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

## Knowledge Gaps
- **50 isolated node(s):** `Chromosome Representation and Fitness`, `2-opt Local Search`, `S1 Short Budget scenario`, `S2 Medium Standard scenario`, `S3 Long Premium scenario` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 144 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_packages()` connect `FastAPI Backend` to `Genetic Algorithm Core`, `Frontend App Logic`?**
  _High betweenness centrality (0.248) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `evaluate_route()` (e.g. with `make_day_details()` and `run_one()`) actually correct?**
  _`evaluate_route()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Chromosome Representation and Fitness`, `2-opt Local Search`, `S1 Short Budget scenario` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Genetic Algorithm Core` be split into smaller, more focused modules?**
  _Cohesion score 0.07506584723441616 - nodes in this community are weakly interconnected._
- **Why does `Hybrid Algorithm (Greedy seed + GA + 2-opt)` connect `Experiments & Dataset (Report)` to `Genetic Algorithm Core`, `Research Theory & Literature`?**
  _High betweenness centrality (0.237) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `create_packages()` (e.g. with `genetic_solve()` and `greedy_solve()`) actually correct?**
  _`create_packages()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Research Theory & Literature` be split into smaller, more focused modules?**
  _Cohesion score 0.052597402597402594 - nodes in this community are weakly interconnected._