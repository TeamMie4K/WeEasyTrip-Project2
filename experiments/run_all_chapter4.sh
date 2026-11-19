#!/bin/bash
# รันการทดลองบทที่ 4 ซ้ำ หลังให้ GA/Greedy ใช้ค่าถ่วงระยะเท่า Hybrid
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8 PYTHONUNBUFFERED=1
for s in run_province_experiments.py run_preference_experiments.py run_pareto_experiments.py run_rl_experiments.py run_ils_experiments.py; do
  echo "=== $s $(date +%T)"; python $s || echo "FAILED $s"
done
for i in 0 1 2; do
  echo "=== sparse SC_IDX=$i $(date +%T)"; SC_IDX=$i python run_sparse_experiments.py || echo "FAILED sparse $i"
done
python make_results_json.py || echo "FAILED make_results_json"
echo ALLDONE $(date +%T)
