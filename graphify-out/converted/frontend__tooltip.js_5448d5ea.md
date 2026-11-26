<!-- converted from frontend__tooltip.js.docx -->

คู่มือโค้ด: frontend/tooltip.js
กล่องคำอธิบาย (tooltip) แบบเรียบง่าย
ไฟล์ต้นฉบับ: frontend/tooltip.js (21 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์เล็กที่แทนกล่องสีดำของเบราว์เซอร์ตอนเมาส์ชี้องค์ประกอบที่มีแอตทริบิวต์ title ด้วยกล่องของเราเอง (คลาส wet-tip ซึ่งกำหนดสไตล์ใน ➜ frontend/style.css) โดยถอด title ออกชั่วคราวระหว่างแสดง แล้วคืนให้ตอนเมาส์ออก เพื่อให้ระบบแปลภาษาใน ➜ frontend/i18n.js ที่อาศัย title ยังทำงานได้ ไฟล์นี้ถูกโหลดจาก ➜ frontend/index.html

บรรทัด 1–3  หัวไฟล์ และตัวแปรสถานะ
1  // tooltip แบบ minimal แทนกล่องสีดำของเบราว์เซอร์: ตอน hover ย้าย title ไปเป็นกล่องของเราชั่วคราว และคืน title ตอนเมาส์ออก (ให้ระบบแปลภาษายังใช้ title ได้)
2  (function () {
3    let tip = null, cur = null, saved = '', held = [];   // held = [element, title] ของ title ที่ถอดไว้ชั่วคราว (รวมของ element แม่ ไม่ให้กล่องของเบราว์เซอร์ซ้อนขึ้นมา)
บรรทัด 1: คอมเมนต์อธิบายหน้าที่ของสคริปต์
บรรทัด 2: เปิด IIFE ห่อโค้ดทั้งไฟล์ไว้ ไม่ให้ตัวแปรรั่วไปที่ขอบเขตหน้าเว็บ
บรรทัด 3: ตัวแปรสถานะ: tip กล่องที่แสดง cur องค์ประกอบที่ชี้อยู่ saved ข้อความ title held รายการ [องค์ประกอบ, title] ที่ถอดไว้ชั่วคราว (รวมองค์ประกอบแม่เพื่อไม่ให้กล่องของเบราว์เซอร์โผล่ซ้อน)
บรรทัด 4–4  ซ่อนกล่อง
4    const hide = () => { tip?.classList.remove('show'); held.forEach(([e, t]) => e.setAttribute('title', t)); held = []; cur = null; saved = ''; };
บรรทัด 4: ฟังก์ชัน hide ซ่อนกล่อง คืน title ที่ถอดไว้ให้ทุกองค์ประกอบ แล้วล้างสถานะ
บรรทัด 5–18  ตอนเมาส์ชี้องค์ประกอบ
5    document.addEventListener('mouseover', e => {
6      const el = e.target.closest?.('[title]');
7      if (!el || el === cur) return;
8      hide(); const t = el.getAttribute('title'); if (!t) return;
9      cur = el; saved = t;
10      for (let e = el; e && e !== document.body; e = e.parentElement) { const tt = e.getAttribute('title'); if (tt) { held.push([e, tt]); e.removeAttribute('title'); } }
11      if (!tip) { tip = document.createElement('div'); tip.className = 'wet-tip'; document.body.appendChild(tip); }
12      tip.textContent = t; tip.style.left = '0px'; tip.style.top = '0px';
13      const r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
14      const above = r.top - h - 8 >= 6;
15      tip.style.top = `${above ? r.top - h - 8 : r.bottom + 8}px`;
16      tip.style.left = `${Math.max(6, Math.min(window.innerWidth - w - 6, r.left + r.width / 2 - w / 2))}px`;
17      tip.classList.add('show');
18    });
บรรทัด 5: ฟัง mouseover ทั้งเอกสาร
บรรทัด 6: หาองค์ประกอบใกล้สุดที่มี title ถ้าไม่มี หรือเป็นตัวเดิม ออกจากฟังก์ชัน
บรรทัด 7–8: ซ่อนกล่องเดิม อ่านข้อความ title ถ้าว่างก็ออก
บรรทัด 9: จดองค์ประกอบและข้อความปัจจุบัน
บรรทัด 10: ไล่จากองค์ประกอบขึ้นไปทุกชั้นแม่ จนถึง body ถอด title ออกและเก็บเข้า held
บรรทัด 11: ถ้ายังไม่เคยสร้างกล่อง สร้าง div คลาส wet-tip แล้วต่อเข้า body
บรรทัด 12: ใส่ข้อความและตั้งตำแหน่งเริ่มต้นที่มุม เพื่อวัดขนาดจริงได้
บรรทัด 13: อ่านตำแหน่งองค์ประกอบและขนาดกล่อง
บรรทัด 14: ตรวจว่ามีที่ว่างเหนือองค์ประกอบพอหรือไม่ (เว้น 8 พิกเซลและขอบ 6)
บรรทัด 15: วางกล่องไว้ด้านบนถ้าพอ ไม่พอวางด้านล่าง
บรรทัด 16: จัดกลางตามองค์ประกอบและหนีบไม่ให้ล้นขอบหน้าจอซ้ายขวา
บรรทัด 17: เติมคลาส show ให้กล่องปรากฏ
บรรทัด 19–21  ซ่อนเมื่อเมาส์ออก เลื่อนหน้า หรือคลิก
19    document.addEventListener('mouseout', e => { if (cur && !cur.contains(e.relatedTarget)) hide(); });
20    document.addEventListener('scroll', hide, true); document.addEventListener('mousedown', hide);
21  })();
บรรทัด 19: ฟัง mouseout ถ้าเมาส์ออกจากองค์ประกอบปัจจุบันจริง (ไม่ใช่เข้าลูกข้างใน) ให้ซ่อน
บรรทัด 20: ซ่อนเมื่อเลื่อนหน้า (รวมการเลื่อนของส่วนย่อย) หรือกดเมาส์
บรรทัด 21: ปิด IIFE และเรียกทำงานทันที

ไฟล์ที่เชื่อมกับไฟล์นี้
frontend/i18n.js
frontend/index.html
frontend/style.css