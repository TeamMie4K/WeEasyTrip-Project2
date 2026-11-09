#!/bin/bash
# รันชุดทดลองทั้งหมดซ้ำภายใต้กติกาความสมจริงใหม่ (มื้อตามเวลาจริง, 2-5 จุด/วัน, เพดานเวลาเที่ยว 8 ชม.)
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8 PYTHONUNBUFFERED=1
for s in run_province_experiments.py run_preference_experiments.py run_pareto_experiments.py run_rl_experiments.py run_ils_experiments.py; do
  echo "=== $s $(date +%T)"; python $s || echo "FAILED $s"
done
echo ALLDONE
