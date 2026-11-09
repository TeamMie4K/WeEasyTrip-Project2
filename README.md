# WeEasyTrip — ระบบแนะนำการท่องเที่ยวหลายจังหวัดภายใต้งบประมาณ

ระบบแนะนำการท่องเที่ยวแบบหลายวัน ภายใต้งบประมาณจำกัด (รองรับภูเก็ต เชียงใหม่ กระบี่ เกาะสมุย)
โดยใช้ Optimization Algorithm (Greedy / GA / Hybrid) สำหรับการจัดเส้นทาง

ความสามารถหลัก: สร้าง 3 แพ็กเกจตามงบ · ปรับแผนใหม่ด้วย Hybrid หลังสลับ/เพิ่ม/ลบสถานที่ · ความชอบ (หมวดที่ชอบ/ไม่เอา, อาหารมังสวิรัติ/ฮาลาล) · ส่งออกเป็นไฟล์ปฏิทิน (.ics) และ PDF

> **รายวิชา CS403 | ปีการศึกษา 2568 ภาคเรียนที่ 2 | กลุ่มที่ 33**

---

## โครงสร้างโฟลเดอร์

```
Thesis Project/
├── README.md                            # ไฟล์นี้
├── CS403_Report_68-2_33_pps-r1 Project 2.docx  # รายงาน Project 2 (Word, ใช้เทมเพลต 2568-2)
├── CS403_Report_68-2_33_pps-r1.docx    # รายงาน Project 1 (Word)
├── CS403_Report_68-2_33_pps-r1.pdf     # รายงานฉบับเต็ม (PDF)
├── docs/
│   └── problem_formulation.md          # นิยามปัญหา B-TOPTW + สมการคณิตศาสตร์
├── data/
│   ├── provinces.json                  # รายชื่อจังหวัด + bbox/center/zoom
│   ├── provinces/<slug>.json           # ข้อมูลรายจังหวัด (phuket, chiangmai, krabi, samui)
│   ├── phuket_pois_backup.json         # สำรองข้อมูลภูเก็ตเดิม
│   ├── fetch_pois_osm.py               # ดึงข้อมูลจังหวัดจาก OpenStreetMap: <slug> | --extra | --restaurants | --diet
│   ├── calibrate_travel.py             # ปรับเทียบระยะ/เวลาเดินทางรายจังหวัดด้วย OSRM
│   ├── apply_names.py + name_translations.json  # เติมชื่ออังกฤษให้รายการที่มีแต่ชื่อไทย
│   └── merge_pois.py                   # (legacy) รวม OSM + ข้อมูลเดิมของภูเก็ต
├── algorithm/
│   ├── utils.py                        # ฟังก์ชันช่วย: ระยะทาง, เวลา, ตรวจ constraint
│   ├── greedy.py                       # Greedy slot-based algorithm (Baseline)
│   ├── genetic.py                      # Genetic Algorithm
│   └── hybrid.py                       # Hybrid: Greedy seed + GA + 2-opt
├── backend/
│   └── main.py                         # FastAPI server
├── frontend/
│   ├── index.html                      # หน้า UI หลัก
│   ├── style.css                       # Aurora background + glass-morphism + dark/light
│   ├── app.js                          # Algorithm selector, day filter, map, swap modal
│   └── BG2.jpg                         # ภาพพื้นหลัง
└── experiments/
    ├── run_experiments.py              # Project 1: 3 algos × 3 scenarios (ภูเก็ต)
    ├── run_province_experiments.py     # Project 2: 4 จังหวัด × Greedy/GA/Hybrid/Hybrid+Div + ปรับแผนหลังแก้ไข
    ├── run_preference_experiments.py   # Project 2: ผลของความชอบ
    └── results/
        ├── results.json                # ผลการทดลองทั้งหมด
        ├── stats.txt                   # สรุปสถิติ
        ├── convergence.png             # กราฟ convergence (Project 1)
        ├── province_stats.txt          # ผลทดลอง Project 2 (4 จังหวัด + ปรับแผน)
        └── preference_stats.txt        # ผลทดลองความชอบ
```

---

## ชุดโปรแกรมที่จำเป็นต้องติดตั้ง

### ซอฟต์แวร์หลัก

| โปรแกรม | เวอร์ชันที่แนะนำ | ดาวน์โหลด |
|--------|----------------|-----------|
| Python | 3.10 ขึ้นไป | https://www.python.org/downloads/ |
| Web Browser | Chrome / Firefox / Edge (เวอร์ชันล่าสุด) | — |

### Python Packages

| Package | การใช้งาน |
|---------|----------|
| `fastapi` | Backend API framework |
| `uvicorn` | ASGI server สำหรับรัน FastAPI |
| `pydantic` | Data validation สำหรับ API |
| `matplotlib` | วาดกราฟ convergence (ใช้ในการทดลอง) |

> **หมายเหตุ:** `frontend/index.html` ใช้ Leaflet.js และ Flatpickr ผ่าน CDN ไม่ต้องติดตั้งเพิ่ม

---

## วิธีการติดตั้งและตั้งค่า

### 1. ตรวจสอบ Python

```bash
python --version
# ต้องเป็น Python 3.10 ขึ้นไป
```

### 2. ติดตั้ง Dependencies

```bash
pip install fastapi uvicorn pydantic matplotlib
```


## วิธีการติดตั้งโปรแกรม

ไม่จำเป็นต้อง build หรือ compile — โปรแกรมพร้อมใช้งานทันทีหลังติดตั้ง dependencies

```bash
# 1. เปิด Terminal แล้วไปที่โฟลเดอร์ backend
cd "Thesis Project/backend"

# 2. รัน Backend server
uvicorn main:app --reload --port 8000
```

เมื่อเห็นข้อความ `Application startup complete.` แสดงว่า Backend พร้อมใช้งาน

---

## วิธีการใช้งานโปรแกรม

### การใช้งานระบบ WeEasyTrip (UI)

**ขั้นที่ 1 — เปิด Backend**

```bash
cd "Thesis Project/backend"
uvicorn main:app --reload --port 8000
```

**ขั้นที่ 2 — เปิด Frontend**

เปิดไฟล์ `frontend/index.html` ด้วย Web Browser โดยตรง
(ไม่จำเป็นต้องมี web server)

**ขั้นที่ 3 — กรอกข้อมูล**

| ช่อง | รายละเอียด |
|------|-----------|
| งบประมาณ (บาท) | 1,000 – 100,000 บาท |
| วันเดินทาง | เลือกช่วงวันที่จาก date picker (1–7 วัน) |
| จำนวนคน | 1–10 คน |
| Algorithm | Greedy / GA / Hybrid (แนะนำ: Hybrid) |
| รวมค่าโรงแรม | เลือกว่าจะรวมค่าโรงแรมในงบหรือไม่ |

**ขั้นที่ 4 — ดูผลลัพธ์**

- ระบบสร้าง **3 แพ็กเกจ** (Budget / Standard / Premium) อัตโนมัติ
- กดการ์ดแพ็กเกจเพื่อดูรายละเอียดเส้นทางและแผนที่
- กด **Swap** เพื่อเปลี่ยนสถานที่ท่องเที่ยวในแต่ละวัน
- กด **Shuffle** เพื่อสุ่มแพ็กเกจใหม่ในระดับเดิม

### การรันการทดลอง (Experiments)

```bash
cd "Thesis Project/experiments"
python run_experiments.py
```

ผลลัพธ์จะถูกบันทึกใน `experiments/results/`:
- `results.json` — ผล trial ทั้งหมด (score, cost, valid, time)
- `stats.txt` — ตารางสรุปสถิติ (mean ± std, Kruskal-Wallis test)
- `convergence.png` — กราฟ convergence ของ GA vs Hybrid vs Greedy

### API Endpoints (สำหรับนักพัฒนา)

| Method | Endpoint | คำอธิบาย |
|--------|----------|----------|
| GET | `/api/health` | ตรวจสอบสถานะ server |
| GET | `/api/pois` | ดึงข้อมูล POI และโรงแรมทั้งหมด |
| POST | `/api/packages` | สร้าง 3 แพ็กเกจจากข้อมูลที่กรอก |
| POST | `/api/recompute` | คำนวณใหม่หลังผู้ใช้แก้ไข route |

ดู API docs แบบ interactive ได้ที่: `http://localhost:8000/docs`

---
## Project 2 — สิ่งที่เพิ่ม
- หลายจังหวัด (4 จังหวัดหลัก + จังหวัดที่สร้างอัตโนมัติด้วย `data/build_all_provinces.py`), เวลาเดินทางรายจังหวัดปรับเทียบด้วย OSRM
- Hybrid + **Insertion Local Search** (`algorithm/ils.py`, เปิดเป็นค่าเริ่มต้น), กติกาความสมจริงของแผนรายวัน (มื้อตามเวลาจริง, 6 จุด/วัน (เที่ยว 4 + อาหาร 2 ตรงกับ Project 1), เพดานเวลาเที่ยว 8 ชม.), หักคะแนนระยะขับ
- ปรับแผนใหม่หลังผู้ใช้แก้ (`/api/reoptimize`), ความชอบ/อาหาร, Pareto (NSGA-II, `/api/pareto`), วางแผนร่วมกัน (`/api/sessions`), ส่งออก .ics/PDF
- โหมด Developer (ปุ่ม `</>` หรือ `?dev=1`) เลือก Greedy / GA / Hybrid / Hybrid+RL ได้; โหมดปกติใช้ Hybrid อย่างเดียว
- ทดลองซ้ำได้ที่ `experiments/` (`run_all_realistic.sh`); ผลอยู่ใน `experiments/results/`. Hybrid+RL ไม่ได้ดีกว่า Hybrid (พักไว้)
- (28 ต.ค.) หน้าต่างรายละเอียดสถานที่: เวลาเปิด-ปิดและเวลาถึงตามแผน; **รีวิวเป็นข้อมูลจำลองเพื่อสาธิต** (ติดป้ายในหน้าจอ) ไม่ใช่รีวิวจริง; เซสชันร่วมกันบันทึกที่ `data/sessions.json`
