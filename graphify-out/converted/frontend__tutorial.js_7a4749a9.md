<!-- converted from frontend__tutorial.js.docx -->

คู่มือโค้ด: frontend/tutorial.js
วิธีใช้แบบนำชม (Tutorial) สำหรับผู้ใช้ครั้งแรก
ไฟล์ต้นฉบับ: frontend/tutorial.js (82 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: แสดงกล่องนำชมทีละขั้นพร้อมไฮไลต์องค์ประกอบ ครั้งแรกที่เข้าเว็บหรือเมื่อห่างหายเกิน 30 วัน มีสองชุด: ชุดฟอร์มค้นหา (FORM) และชุดหน้ารายละเอียดแผน (DETAIL) ซึ่งแสดงหลังเปิดแผนครั้งแรก โดยห่อฟังก์ชัน renderDetail ของ ➜ renderDetail() ใน frontend/app.js ปุ่ม "?" ถูกแทรกข้างปุ่มธีมที่อยู่ใน ➜ frontend/index.html ภาษาอ่านจากตัวแปร WET_LANG ที่ ➜ frontend/i18n.js กำหนด และสไตล์ของกล่อง (คลาส tut) อยู่ใน ➜ frontend/style.css

บรรทัด 1–11  หัวไฟล์ และสถานะการเข้าใช้
1  // Tutorial สำหรับผู้ใช้ครั้งแรก และผู้ที่กลับมาใช้หลังไม่ได้เข้า 30 วัน — ปุ่ม "?" บนแถบบนเปิดดูซ้ำได้
2  // ใช้ localStorage (ถ้าใช้ไม่ได้ เช่น โหมดส่วนตัว จะแสดงทุกครั้งที่เปิดหน้า ไม่ทำให้หน้าพัง)
3  (function () {
4    const DAY = 86400000, RETURN_AFTER = 30 * DAY;
5    const get = k => { try { return +localStorage.getItem(k) || 0; } catch (e) { return 0; } };
6    const set = (k, v) => { try { localStorage.setItem(k, String(v)); } catch (e) { /* ไม่เก็บค่า */ } };
7    const en = () => window.WET_LANG === 'en';
8    const now = Date.now(), lastVisit = get('wet_last_visit'), doneAt = get('wet_tut_done');
9    set('wet_last_visit', now);
10    const due = !doneAt || (lastVisit && now - lastVisit > RETURN_AFTER);   // ครั้งแรก หรือห่างหายเกิน 30 วัน
11    let detailDue = due, el = null, idx = 0, steps = [], onEnd = null;
บรรทัด 1–2: คอมเมนต์อธิบายเงื่อนไขการแสดง และการใช้ localStorage แบบไม่ทำให้หน้าพังเมื่อใช้ไม่ได้
บรรทัด 3: เปิด IIFE
บรรทัด 4: ค่าคงที่ DAY และ RETURN_AFTER (30 วัน)
บรรทัด 5: get อ่านตัวเลขจาก localStorage ถ้าผิดพลาดคืน 0
บรรทัด 6: set เขียนค่าลง localStorage ถ้าผิดพลาดก็ข้าม
บรรทัด 7: en ตรวจว่าภาษาปัจจุบันเป็นอังกฤษ
บรรทัด 8: อ่านเวลาปัจจุบัน เวลาเข้าใช้ครั้งก่อน และเวลาที่ดู tutorial จบ
บรรทัด 9: บันทึกเวลาเข้าใช้ครั้งนี้
บรรทัด 10: due = ยังไม่เคยดูจบ หรือห่างหายเกิน 30 วัน
บรรทัด 11: ตัวแปรสถานะ: detailDue ว่าจะแสดงชุดรายละเอียดหรือไม่ el กล่องนำชม idx ขั้นปัจจุบัน steps รายการขั้น onEnd ฟังก์ชันเมื่อจบ
บรรทัด 13–27  ข้อความของแต่ละขั้น
13    const FORM = [
14      {th: ['ยินดีต้อนรับสู่ WeEasyTrip', 'ระบบช่วยวางแผนเที่ยวไทยตามงบประมาณและเวลาของคุณ ใช้เวลาเพียงไม่กี่ขั้นตอน ลองดูวิธีใช้สั้นๆ กัน'], en: ['Welcome to WeEasyTrip', 'Plan a Thailand trip around your budget and time in a few steps. Here is a quick tour.']},
15      {sel: '#provSelect', th: ['1. เลือกจังหวัด', 'มีให้เลือกครบ 77 จังหวัด ภาพด้านบนจะเปลี่ยนตามจังหวัดที่เลือก'], en: ['1. Pick a province', 'All 77 provinces are available. The banner changes with your choice.']},
16      {sel: '#dateRange', th: ['2. เลือกวันเดินทาง', 'เลือกวันเริ่มและวันสิ้นสุด ระบบจะแสดงพยากรณ์อากาศจริงให้ถ้าอยู่ในช่วง 16 วันข้างหน้า'], en: ['2. Choose your dates', 'Pick start and end dates. A real weather forecast appears if within the next 16 days.']},
17      {sel: '#budget', th: ['3. ใส่งบประมาณ', 'งบรวมของทริป ระบบจะจัดแผนให้ไม่เกินงบนี้ และเสนอ 3 ระดับ: ประหยัด มาตรฐาน พรีเมียม'], en: ['3. Set your budget', 'Total trip budget. Plans stay within it, in 3 tiers: Budget, Standard, Premium.']},
18      {sel: '#prefToggle', th: ['4. บอกความชอบ (ไม่บังคับ)', 'เลือกประเภทสถานที่ที่ชอบหรือไม่ต้องการ และอาหารมังสวิรัติ/ฮาลาล'], en: ['4. Tell us your tastes (optional)', 'Choose place types you like or want to avoid, and vegetarian/halal food.']},
19      {sel: '#searchBtn', th: ['5. กดค้นหา', 'ระบบจะสร้างแผน 3 แบบให้เลือก เมื่อได้แล้วจะมีวิธีใช้ส่วนถัดไปให้ดูอีกครั้ง'], en: ['5. Search', 'You get 3 plans to choose from. A second short tour appears once you open a plan.']},
20    ];
21    const DETAIL = [
22      {sel: '#dayPanels .poi-item', th: ['ลากการ์ดเพื่อเรียงลำดับ', 'กดค้างที่การ์ดสถานที่แล้วลากไปวางที่ใหม่หรือย้ายไปวันอื่น ช่องว่างสีแดงจางๆ คือจุดที่จะวาง ถ้าเวลาไม่พอหรือร้านปิด การ์ดจะเป็นสีแดงพร้อมคำอธิบาย'], en: ['Drag cards to reorder', 'Press and drag a card to a new spot or another day. The faint red gap shows where it will land. If a stop does not fit (e.g. closed), the card turns red with an explanation.']},
23      {sel: '#dayPanels .btn-swap', th: ['เปลี่ยนหรือลบสถานที่', 'กดปุ่มสลับเพื่อเลือกสถานที่อื่นแทน หรือถังขยะเพื่อลบ ระบบคำนวณเวลาและค่าใช้จ่ายใหม่ให้ทันที'], en: ['Swap or remove a stop', 'Use swap to pick another place, or the bin to remove it. Times and costs update instantly.']},
24      {sel: '#dayToggles', th: ['ดูเส้นทางบนแผนที่', 'หมายเลขบนแผนที่คือลำดับสถานที่ของแต่ละวัน แต่ละวันมีสีต่างกัน และเส้นประคือเส้นทางที่เดินทางระหว่างจุด กดปุ่มวันเพื่อดูเฉพาะวันนั้น แสดงทุกวัน หรือซ่อนทุกวัน'], en: ['Read the map route', 'Numbers on the map show the order of stops each day, with one colour per day and dashed lines for the route between them. Tap a day chip to see only that day, or show/hide all days.']},
25      {sel: '.map-wrap', th: ['คลิกหมุดเพื่อดูรายละเอียด', 'กดหมุดบนแผนที่เพื่อดูชื่อสถานที่ เวลาเปิด-ปิด และรีวิว หมุดสีส้มที่มีรูปเตียงคือโรงแรมที่พัก'], en: ['Tap a pin for details', 'Tap a pin to see the place name, opening hours and reviews. The orange bed pin is your hotel.']},
26      {sel: '.detail-actions', th: ['บันทึก แชร์ และส่งออก', 'บันทึกแผนไว้ในเบราว์เซอร์ ดูทางเลือกอื่นของทริป แชร์ลิงก์ให้เพื่อนแก้ร่วมกัน หรือส่งออกเป็นปฏิทินและ PDF'], en: ['Save, share and export', 'Save the plan, see alternatives, share a link for friends to edit together, or export to calendar and PDF.']},
27    ];
บรรทัด 13–20: FORM ชุดนำชมฟอร์ม: แต่ละขั้นมีตัวเลือก sel (CSS selector ขององค์ประกอบที่ไฮไลต์ ขั้นต้อนรับไม่มี) และข้อความไทยกับอังกฤษ [หัวเรื่อง, เนื้อความ]
บรรทัด 21–27: DETAIL ชุดนำชมหน้ารายละเอียด: ลากการ์ด เปลี่ยนหรือลบสถานที่ ดูเส้นทางบนแผนที่ คลิกหมุด และปุ่มบันทึก/แชร์/ส่งออก
บรรทัด 29–30  รีเซ็ตและปิด
29    function resetLanding() { document.querySelectorAll('.landing-screen').forEach(e => { e.scrollTop = 0; e.scrollLeft = 0; }); }
30    function close(finished) { resetLanding(); el?.remove(); el = null; window.removeEventListener('resize', placeSoon); window.removeEventListener('scroll', placeSoon, true); if (finished) onEnd?.(); }
บรรทัด 29: resetLanding เลื่อนหน้า landing กลับขึ้นบนสุด
บรรทัด 30: close ปิดกล่อง ถอดตัวฟังเหตุการณ์ และถ้าจบจริงเรียก onEnd
บรรทัด 31–39  สร้างกล่องนำชม
31    function build() {
32      el = document.createElement('div'); el.className = 'tut';
33      el.innerHTML = '<div class="tut-spot"></div><div class="tut-card"><div class="tut-title"></div><div class="tut-text"></div><div class="tut-foot"><span class="tut-dots"></span><span class="tut-btns"><button class="tut-skip"></button><button class="tut-prev"></button><button class="tut-next"></button></span></div></div>';
34      document.body.appendChild(el);
35      el.querySelector('.tut-skip').onclick = () => close(true);
36      el.querySelector('.tut-prev').onclick = () => go(idx - 1);
37      el.querySelector('.tut-next').onclick = () => (idx + 1 >= steps.length ? close(true) : go(idx + 1));
38      window.addEventListener('resize', placeSoon); window.addEventListener('scroll', placeSoon, true);
39    }
บรรทัด 31–34: build สร้างโครงสร้าง HTML (ไฮไลต์ การ์ด หัวเรื่อง เนื้อความ จุดบอกขั้น ปุ่มข้าม/ก่อนหน้า/ถัดไป) แล้วต่อเข้า body
บรรทัด 35–37: ผูกปุ่ม: ข้ามคือปิด ก่อนหน้าไปขั้นก่อน ถัดไปไปขั้นถัดไปหรือจบเมื่อถึงขั้นสุดท้าย
บรรทัด 38: ฟังการปรับขนาดและเลื่อนหน้าเพื่อจัดตำแหน่งใหม่
บรรทัด 40–50  ไปยังขั้นที่กำหนด
40    function go(i) {
41      idx = Math.max(0, Math.min(steps.length - 1, i)); const s = steps[idx], t = s[en() ? 'en' : 'th'];
42      const target = s.sel && document.querySelector(s.sel);
43      if (target && target.offsetParent !== null) { const r = target.getBoundingClientRect(); if (r.top < 80 || r.bottom > window.innerHeight - 80) window.scrollBy({top: r.top - window.innerHeight / 3, behavior: 'smooth'}); }   // ไม่ใช้ scrollIntoView: .landing-screen เป็น overflow:hidden จะถูกเลื่อนภายในจนเลื่อนกลับไม่ได้
44      el.querySelector('.tut-title').textContent = t[0]; el.querySelector('.tut-text').textContent = t[1];
45      el.querySelector('.tut-dots').innerHTML = steps.map((_, k) => `<i class="${k === idx ? 'on' : ''}"></i>`).join('');
46      el.querySelector('.tut-skip').textContent = en() ? 'Skip' : 'ข้าม'; el.querySelector('.tut-prev').textContent = en() ? 'Back' : 'ก่อนหน้า';
47      el.querySelector('.tut-prev').style.visibility = idx ? 'visible' : 'hidden';
48      el.querySelector('.tut-next').textContent = idx + 1 >= steps.length ? (en() ? 'Got it' : 'เริ่มใช้งาน') : (en() ? 'Next' : 'ถัดไป');
49      place(); el.classList.add('ready');   // วางตำแหน่งทันที (เลื่อนหน้าจอ: placeSoon จัดตำแหน่งซ้ำระหว่างเลื่อน)
50    }
บรรทัด 40–41: go หนีบเลขขั้นให้อยู่ในช่วง เลือกข้อความตามภาษา
บรรทัด 42–43: ถ้าองค์ประกอบเป้าหมายมองเห็นแต่ใกล้ขอบจอ เลื่อนหน้าให้เข้ามา (ไม่ใช้ scrollIntoView เพราะ .landing-screen ซ่อนส่วนที่ล้น จะเลื่อนภายในแล้วกลับไม่ได้)
บรรทัด 44: ใส่หัวเรื่องและเนื้อความ
บรรทัด 45: วาดจุดบอกขั้น ขั้นปัจจุบันเป็นสีเข้ม
บรรทัด 46–48: ตั้งข้อความปุ่มตามภาษา ซ่อนปุ่มก่อนหน้าในขั้นแรก ขั้นสุดท้ายเปลี่ยนปุ่มถัดไปเป็น "เริ่มใช้งาน"
บรรทัด 49: จัดตำแหน่งและเติมคลาส ready ให้แสดง
บรรทัด 51–63  จัดตำแหน่งไฮไลต์และการ์ด
51    let raf = 0;
52    function placeSoon() { if (!raf) raf = requestAnimationFrame(() => { raf = 0; place(); }); }
53    function place() {
54      if (!el) return; const s = steps[idx], target = s.sel && document.querySelector(s.sel), spot = el.querySelector('.tut-spot'), card = el.querySelector('.tut-card');
55      if (!target || target.offsetParent === null) { spot.style.cssText = 'display:none'; card.style.cssText = ''; card.classList.add('center'); el.classList.add('dim'); return; }
56      el.classList.remove('dim');
57      card.classList.remove('center');
58      const r = target.getBoundingClientRect(), pad = 8;
59      spot.style.cssText = `display:block;top:${r.top - pad}px;left:${r.left - pad}px;width:${r.width + pad * 2}px;height:${r.height + pad * 2}px`;
60      const cw = Math.min(340, window.innerWidth - 24), below = r.bottom + 16 + 190 < window.innerHeight;
61      card.style.top = below ? `${r.bottom + 16}px` : `${Math.max(12, r.top - 16 - card.offsetHeight)}px`;
62      card.style.left = `${Math.max(12, Math.min(window.innerWidth - cw - 12, r.left + r.width / 2 - cw / 2))}px`; card.style.width = cw + 'px';
63    }
บรรทัด 51–52: placeSoon รวมการจัดตำแหน่งหลายครั้งให้เหลือหนึ่งครั้งต่อเฟรมด้วย requestAnimationFrame
บรรทัด 53–54: place ออกถ้าไม่มีกล่อง แล้วอ่านขั้นปัจจุบัน เป้าหมาย ไฮไลต์ และการ์ด
บรรทัด 55: ถ้าไม่มีเป้าหมายหรือมองไม่เห็น ซ่อนไฮไลต์ วางการ์ดกลางจอ และทำพื้นหลังมืด
บรรทัด 56–57: มีเป้าหมาย: เอาพื้นหลังมืดและการ์ดกลางจอออก
บรรทัด 58–59: คำนวณกรอบเป้าหมายและวางไฮไลต์ขยายออกรอบละ 8 พิกเซล
บรรทัด 60: ความกว้างการ์ดไม่เกิน 340 และเช็กว่าใต้เป้าหมายมีที่พอ
บรรทัด 61–62: วางการ์ดไว้ใต้เป้าหมายถ้าพอ ไม่พอวางไว้เหนือ และจัดกลางโดยไม่ล้นจอ
บรรทัด 64–65  เริ่มชุดนำชม
64    function start(list, end) { resetLanding(); if (el) close(false); steps = list; idx = 0; onEnd = end; build(); go(0); }
65    window.startTutorial = () => start(FORM, () => set('wet_tut_done', Date.now()));
บรรทัด 64: start รีเซ็ต ปิดของเดิม ตั้งชุดขั้นและฟังก์ชันจบ แล้วสร้างและไปขั้นแรก
บรรทัด 65: window.startTutorial เปิดชุดฟอร์มและบันทึกเวลาว่าดูจบเมื่อจบ (ให้ปุ่มอื่นเรียกได้)
บรรทัด 67–71  เมื่อหน้าเว็บโหลดเสร็จ
67    document.addEventListener('DOMContentLoaded', () => {
68      document.getElementById('themeBtn')?.insertAdjacentHTML('beforebegin', '<button class="icon-btn" id="helpBtn" title="วิธีใช้" style="font-weight:700">?</button>');
69      document.getElementById('helpBtn').onclick = () => { detailDue = true; window.startTutorial(); };
70      if (due) setTimeout(window.startTutorial, 1200);
71    });
บรรทัด 67: รอ DOMContentLoaded
บรรทัด 68: แทรกปุ่ม "?" ก่อนปุ่มธีม
บรรทัด 69: คลิกปุ่มแล้วเปิดชุดฟอร์มใหม่ และอนุญาตให้ชุดรายละเอียดแสดงด้วย
บรรทัด 70: ถ้าถึงเวลาแสดง เปิดอัตโนมัติหลัง 1.2 วินาที
บรรทัด 72–82  ผูกกับการเปิดแผน
72    // เปิดแผนครั้งแรกในรอบนี้ → แสดงวิธีใช้ส่วนรายละเอียดแผน
73    const wrap = () => {
74      if (typeof renderDetail !== 'function') return setTimeout(wrap, 300);
75      const orig = renderDetail;
76      renderDetail = function (pkg) {
77        orig(pkg);
78        if (detailDue && !el) { detailDue = false; setTimeout(() => start(DETAIL, null), 900); }
79      };
80    };
81    wrap();
82  })();
บรรทัด 72: คอมเมนต์อธิบาย
บรรทัด 73–75: wrap รอจนฟังก์ชัน ➜ renderDetail() ใน frontend/app.js ถูกประกาศ (ลองซ้ำทุก 300 มิลลิวินาที) แล้วเก็บฟังก์ชันเดิม
บรรทัด 76–79: แทนที่ renderDetail ด้วยตัวห่อ: เรียกของเดิมก่อน แล้วถ้าถึงเวลาและไม่มีกล่องค้าง แสดงชุดรายละเอียดหลัง 0.9 วินาที (แสดงครั้งเดียวต่อรอบ)
บรรทัด 81–82: เรียก wrap และปิด IIFE

ไฟล์ที่เชื่อมกับไฟล์นี้
frontend/app.js
frontend/i18n.js
frontend/index.html
frontend/style.css