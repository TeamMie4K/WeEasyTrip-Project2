# วิธีนำ WeEasyTrip ขึ้นเว็บให้คนอื่นใช้ (Render ฟรี)

ระบบเตรียมไว้ให้เป็น **บริการเดียว**: backend (FastAPI) เสิร์ฟหน้าเว็บ (`frontend/`) เอง จึงไม่ต้องตั้ง CORS หรือ API_BASE
(หน้าเว็บเลือก `API_BASE` อัตโนมัติ: เปิดจากพอร์ต 5500/ไฟล์ในเครื่อง → `http://localhost:8000`, ไม่งั้นเรียกที่เดียวกัน)

## ขั้นตอน (ผู้ใช้ทำเอง — ต้องมีบัญชี GitHub และ Render)
1. push โปรเจกต์ขึ้น GitHub (ไฟล์ที่ต้องมี: `Dockerfile`, `requirements.txt`, `render.yaml`, `algorithm/`, `backend/`, `frontend/`, `data/provinces*`)
2. Render → **New → Blueprint** → เลือก repo → Render อ่าน `render.yaml` แล้วสร้างเว็บให้
3. ตั้งตัวแปร `WET_DEV_PASSWORD` (รหัสโหมด Developer) ในหน้า Environment — **อย่าใช้ค่าเริ่มต้น 007 บนเว็บจริง**
4. เปิด URL ที่ Render ให้ ทดสอบ `/api/health` และหน้าแรก

## ข้อจำกัดของแผนฟรี
- เซิร์ฟเวอร์หลับเมื่อไม่มีคนใช้ ~15 นาที ตื่นช้า ~30–60 วินาที — เปิดหน้าไว้ก่อนวันนำเสนอ
- CPU น้อย: Hybrid ใช้ ~2–4 วินาที/คำขอ (บนเครื่องนี้) อาจช้ากว่านี้บน Render
- มีตัวจำกัดคำขอหนัก: 20 ครั้ง/นาที/IP (`WET_RATE_PER_MIN`) และรันพร้อมกันได้ 2 งาน (เกินจะรอ/ตอบ 503)
- เซสชันแชร์แผน (ร่วมกันวางแผน) และโทเค็น Developer เก็บในหน่วยความจำ — หายเมื่อเซิร์ฟเวอร์รีสตาร์ท
- ไฟล์ .ics/PDF สร้างที่หน้าเว็บ ไม่ผ่านเซิร์ฟเวอร์

## รันในเครื่องแบบบริการเดียว
```bash
pip install -r requirements.txt
python -m uvicorn main:app --app-dir backend --port 8000   # แล้วเปิด http://localhost:8000
```
