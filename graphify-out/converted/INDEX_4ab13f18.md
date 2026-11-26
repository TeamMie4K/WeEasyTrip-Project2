<!-- converted from INDEX.docx -->

คู่มือโค้ด WeEasyTrip (Project 2)
คู่มือนี้อธิบายโค้ดทีละไฟล์ ทีละบรรทัด ในแต่ละหน้าจะแสดงโค้ดจริงเป็นช่วง ๆ แล้วตามด้วยคำอธิบายของแต่ละบรรทัด ถ้าโค้ดเรียกใช้ฟังก์ชันที่อยู่คนละไฟล์ จะมีลิงก์ ➜ กดไปที่ฟังก์ชันนั้นในคู่มือของอีกไฟล์ได้ทันที (เก็บไฟล์ .docx ทั้งหมดไว้ในโฟลเดอร์เดียวกันเพื่อให้ลิงก์ทำงาน)
อัลกอริทึม (algorithm/)
algorithm/genetic.py  — Genetic Algorithm (GA) สำหรับ B-TOPTW
algorithm/greedy.py  — Greedy แบบแบ่งช่อง (slot-based) สร้างแผนเริ่มต้น
algorithm/hybrid.py  — Hybrid Algorithm: Greedy seed + GA + 2-opt + ซ่อมแผน + ILS
algorithm/ils.py  — Insertion Local Search (ILS) ปรับปรุงแผนที่ Hybrid สร้างแล้ว
algorithm/pareto.py  — NSGA-II หลายวัตถุประสงค์ (Pareto front)
algorithm/rl.py  — Reinforcement Learning (REINFORCE) สร้างแผนเริ่มต้นแทน Greedy
algorithm/utils.py  — ฟังก์ชันพื้นฐาน: ระยะทาง เวลาเดินทาง และตัวตรวจสอบแผน
เซิร์ฟเวอร์ (backend/)
backend/main.py  — FastAPI Backend ของ WeEasyTrip (API สร้างแพ็กเกจ ปรับแผน เซสชันร่วมกัน และให้บริการหน้าเว็บ)
หน้าเว็บ (frontend/)
frontend/app.js  — ตรรกะหลักของหน้าเว็บ (app.js)
frontend/extras.js  — ส่วนเสริมของหน้าเว็บ: จังหวัดข้างเคียง อากาศ ลากวาง Tips แผนที่บันทึก
frontend/i18n.js  — สลับภาษาไทย/อังกฤษด้วยพจนานุกรมและ regex
frontend/index.html  — หน้าหลักของเว็บ (index.html)
frontend/results.html  — หน้าแสดงผลการทดลอง (results.html)
frontend/style.css  — สไตล์ของหน้าเว็บทั้งหมด (style.css)
frontend/tooltip.js  — กล่องคำอธิบาย (tooltip) แบบเรียบง่าย
frontend/tutorial.js  — วิธีใช้แบบนำชม (Tutorial) สำหรับผู้ใช้ครั้งแรก
การทดลอง (experiments/)
experiments/make_results_json.py  — สรุปผลทดลองเป็น JSON สำหรับหน้าผลทดลอง
experiments/run_experiments.py  — การทดลองของ Project 1: Greedy / GA / Hybrid บนภูเก็ต (30 รอบ × 3 สถานการณ์)
experiments/run_ils_experiments.py  — การทดลอง ILS: Hybrid เทียบ Hybrid+ILS
experiments/run_pareto_experiments.py  — การทดลอง Pareto: NSGA-II เทียบ Hybrid แบบถ่วงน้ำหนัก
experiments/run_preference_experiments.py  — การทดลองความชอบของผู้ใช้ (เฟส 3)
experiments/run_province_experiments.py  — การทดลองหลักบทที่ 4: เปรียบเทียบอัลกอริทึมใน 4 จังหวัด และจำลองผู้ใช้แก้แผน
experiments/run_rl_experiments.py  — การทดลอง RL: คุณภาพ seed และ Hybrid ที่ใช้ RL seed
experiments/run_sparse_experiments.py  — การทดลองจังหวัดข้อมูลน้อย (sparse) และทริปข้ามจังหวัด
experiments/train_rl.py  — ฝึกนโยบาย RL ในสภาพแวดล้อมจำลอง
ข้อมูลและท่อประมวลผล (data/)
data/apply_names.py  — เติมชื่ออังกฤษให้สถานที่ที่ OSM มีแต่ชื่อไทย
data/build_all_provinces.py  — ท่อสร้างข้อมูลทุกจังหวัดอัตโนมัติ (77 จังหวัด)
data/calibrate_travel.py  — ปรับเทียบระยะ/เวลาเดินทางรายจังหวัดด้วย OSRM
data/fetch_pois_osm.py  — ดึงสถานที่และโรงแรมของจังหวัดจาก OpenStreetMap (Overpass API)
data/make_banners.py  — สร้างภาพแบนเนอร์ SVG ประจำจังหวัด
data/merge_pois.py  — รวมข้อมูล OSM ใหม่กับข้อมูลเดิมของภูเก็ต (legacy)
data/thai_provinces.py  — ทะเบียนรายชื่อ 77 จังหวัด
หมายเหตุ: ไฟล์ frontend/app.backup.js เป็นสำเนาสำรองของ app.js รุ่นเก่า จึงไม่อธิบายซ้ำ