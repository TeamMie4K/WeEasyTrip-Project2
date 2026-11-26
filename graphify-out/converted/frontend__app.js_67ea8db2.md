<!-- converted from frontend__app.js.docx -->

คู่มือโค้ด: frontend/app.js
ตรรกะหลักของหน้าเว็บ (app.js)
ไฟล์ต้นฉบับ: frontend/app.js (1759 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ไฟล์ JavaScript หลักของเว็บ ทำหน้าที่ตั้งค่าเริ่มต้น เลือกวันเดินทางและอัลกอริทึม ส่งคำขอไป ➜ backend/main.py (เส้นทาง /api/provinces /api/pois /api/packages /api/recompute /api/reoptimize /api/pareto และเซสชันแชร์) แล้ววาดแพ็กเกจ รายละเอียดแผน การ์ดสถานที่ และแผนที่ Leaflet ตัวแปรกลาง STATE เก็บสถานะทั้งเว็บ ฟังก์ชันที่ผูกกับปุ่มใน ➜ frontend/index.html (onclick) อยู่ในไฟล์นี้ทั้งหมด ไฟล์ ➜ frontend/extras.js โหลดตามหลังและห่อฟังก์ชันหลายตัวของไฟล์นี้เพื่อเพิ่มฟีเจอร์ ส่วน ➜ frontend/i18n.js แปลข้อความที่ไฟล์นี้สร้างเป็นภาษาอังกฤษ ➜ frontend/tutorial.js ห่อ renderDetail และ ➜ frontend/style.css กำหนดสไตล์ของคลาสที่ไฟล์นี้สร้าง (ไฟล์ app.backup.js เป็นสำเนารุ่นเก่า ไม่ได้ใช้)

บรรทัด 1–5  หัวไฟล์ และที่อยู่ของ backend
1  // app.js - WeEasyTrip Frontend
2  // ระบบวางแผนท่องเที่ยวหลายจังหวัด — ส่วนแสดงผลหลัก
3
4  // เปิดจากเซิร์ฟเวอร์หน้าเว็บแยก (พอร์ต 5500) หรือไฟล์ในเครื่อง → ชี้ backend ที่ localhost:8000; ถูกเสิร์ฟจาก backend เอง (deploy) → เรียกที่เดียวกัน
5  const API_BASE = (location.protocol === 'file:' || location.port === '5500') ? 'http://localhost:8000' : '';
บรรทัด 1–2: คอมเมนต์ชื่อไฟล์และหน้าที่
บรรทัด 4–5: API_BASE ที่อยู่ backend: ถ้าเปิดเป็นไฟล์ในเครื่อง หรือจากเซิร์ฟเวอร์หน้าเว็บแยกที่พอร์ต 5500 ชี้ไป http://localhost:8000 ไม่เช่นนั้นใช้เส้นทางสัมพัทธ์ (เว็บและ API อยู่โดเมนเดียวกัน)
บรรทัด 7–25  สถานะกลางของเว็บ
7  const STATE = {
8    pois: [],
9    hotels: [],
10    poisById: {},
11    packages: [],
12    selectedPkg: null,
13    selectedIdx: null,
14    swapContext: null,
15    map: null,
16    mapMarkers: [],
17    mapPolylines: [],
18    // Track markers/polylines per day for filtering
19    mapDayLayers: {},   // {dayIdx: {markers: [], polyline: line, visible: true}}
20    hotelMarker: null,
21    provinces: {},   // slug -> {center, zoom, ...} จาก /api/provinces
22    session: null,         // {id, version, timer} เมื่อแชร์/เข้าร่วมแผนร่วมกัน
23    locked: new Set(),     // POI ที่ผู้ใช้เลือกเอง (swap/เพิ่ม) — re-optimize ต้องคงไว้
24    excluded: new Set(),   // POI ที่ผู้ใช้ลบ — re-optimize ห้ามใส่กลับ
25  };
บรรทัด 7–25: STATE เก็บ: รายการสถานที่ โรงแรม ตารางค้นหาตาม id แพ็กเกจที่ได้ แพ็กเกจที่เลือก บริบทของการสลับสถานที่ แผนที่และหมุด/เส้นต่อวัน (mapDayLayers) หมุดโรงแรม ตารางจังหวัดจาก /api/provinces เซสชันแชร์ และสองชุดสำคัญ: locked สถานที่ที่ผู้ใช้เลือกเอง (ปรับแผนใหม่ต้องคงไว้) กับ excluded สถานที่ที่ผู้ใช้ลบ (ห้ามใส่กลับ)
บรรทัด 27–30  ตัวช่วยอ่านค่า และโทเค็นโหมด Developer
27  const getProvince = () => document.getElementById('province').value;
28  // โทเค็นโหมด Developer (ได้จาก /api/dev/unlock หลังใส่รหัสถูก) — backend ใช้ตัดสินว่าอนุญาตให้เลือกอัลกอริทึมอื่นนอกจาก Hybrid หรือไม่
29  const devToken = () => { try { return localStorage.getItem('wet_dev_token') || ''; } catch (e) { return ''; } };
30  const devHeaders = () => ({'Content-Type': 'application/json', ...(devToken() ? {'X-Dev-Token': devToken()} : {})});
บรรทัด 27: getProvince อ่าน slug จังหวัดจากช่องซ่อน #province ใน ➜ frontend/index.html
บรรทัด 28–29: devToken อ่านโทเค็นโหมด Developer จาก localStorage (ได้มาจาก ➜ dev_unlock() ใน backend/main.py ผ่าน ➜ frontend/extras.js) ถ้าอ่านไม่ได้คืนสตริงว่าง
บรรทัด 30: devHeaders ส่วนหัวคำขอ JSON และถ้ามีโทเค็นเพิ่ม X-Dev-Token ที่ backend ใช้ตัดสินว่าอนุญาตอัลกอริทึมนอกเหนือ Hybrid
บรรทัด 32–64  ค่าคงที่การแสดงผล
32  const DAY_COLORS = ['#06b6d4', '#a78bfa', '#f97316', '#10b981', '#f43f5e', '#fbbf24', '#3b82f6'];
33
34  const CAT_LABELS = {
35    all: 'ทั้งหมด',
36    beach: 'หาด', temple: 'วัด', viewpoint: 'จุดชมวิว',
37    culture: 'วัฒนธรรม', market: 'ตลาด',
38    activity: 'กิจกรรม', restaurant: 'ร้านอาหาร'
39  };
40
41  // ไอคอนเส้นบาง (sprite ใน index.html) แทน emoji ให้โทนเดียวกับธีม
42  function ic(name, cls = '') {
43    return `<svg class="ic ${cls}" aria-hidden="true"><use href="#i-${name}"/></svg>`;
44  }
45  const CAT_ICON = {
46    beach: ic('beach'), temple: ic('temple'), viewpoint: ic('viewpoint'),
47    culture: ic('culture'), market: ic('market'),
48    activity: ic('activity'), restaurant: ic('restaurant'), hotel: ic('hotel')
49  };
50
51  // ไอคอน SVG แบบ inline (Lucide style)
52  const ICON = {
53    clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
54    coin:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-4a2 2 0 0 0 0 4h2a2 2 0 0 1 0 4H8"/><path d="M12 6v2m0 8v2"/></svg>',
55    route: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/><path d="M9 19h6a4 4 0 0 0 0-8h-6a4 4 0 0 1 0-8h6"/></svg>',
56    star:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
57    swap:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>',
58    pin:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
59    trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-2 14a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/></svg>',
60    plus:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
61    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
62    alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
63    spin:  '<svg class="spinner" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="50" stroke-dashoffset="30" stroke-linecap="round"/></svg>',
64  };
บรรทัด 32: DAY_COLORS สีประจำวันของเส้นและหมุดบนแผนที่ (7 วัน)
บรรทัด 34–39: CAT_LABELS ชื่อหมวดภาษาไทย
บรรทัด 41–44: ic สร้าง HTML ของไอคอนจากชุด sprite ใน ➜ frontend/index.html
บรรทัด 45–49: CAT_ICON ไอคอนของแต่ละหมวด
บรรทัด 51–64: ICON ไอคอน SVG แบบ inline (นาฬิกา เหรียญ เส้นทาง ดาว สลับ หมุด ถังขยะ บวก ถูก เตือน และตัวหมุน)
บรรทัด 69–79  เริ่มระบบเมื่อโหลดหน้า
69  window.addEventListener('DOMContentLoaded', async () => {
70    initTheme();
71    initDateRange();
72    initMap();
73    initBudgetValidation();
74    initAlgoControl();
75    initPrefs();
76    await loadProvinces();
77    const joinId = new URLSearchParams(location.search).get('s');
78    if (joinId) { await joinSession(joinId); } else { await loadPois(); }
79  });
บรรทัด 69: ฟังเหตุการณ์ DOMContentLoaded
บรรทัด 70–75: เรียกตัวเริ่มต้นตามลำดับ: ธีม ตัวเลือกวันที่ แผนที่ ตัวตรวจงบ ปุ่มอัลกอริทึม และความชอบ
บรรทัด 76: โหลดรายการจังหวัดจาก backend (➜ loadProvinces() ใน frontend/app.js) (ถูก ➜ frontend/extras.js ห่อไว้)
บรรทัด 77–78: ถ้า URL มีพารามิเตอร์ s (ลิงก์แชร์) เข้าร่วมเซสชันด้วย ➜ joinSession() ใน frontend/app.js ไม่เช่นนั้นโหลดสถานที่ของจังหวัดด้วย ➜ loadPois() ใน frontend/app.js
บรรทัด 81–88  ข้อความอัลกอริทึม
81  const ALGO_HINTS = {
82    greedy: 'Greedy: เร็วที่สุด (~10 ms) — เลือกจุดดีที่สุดทีละขั้น แต่อาจไม่ optimal ในภาพรวม',
83    ga:     'Genetic Algorithm: optimization ทั้งทริปพร้อมกัน (~3-8 sec) — global optimal กว่า greedy',
84    hybrid: 'Hybrid (แนะนำ): Greedy seed → GA refine → 2-opt local search (~0.3-0.7 sec) — รวมข้อดีของทั้งสอง',
85    hybrid_rl: 'Hybrid + RL seed: เพิ่มแผนเริ่มต้นจาก RL policy (ฝึกในสภาพแวดล้อมจำลอง) — ผลทดลองไม่ดีกว่า Hybrid อย่างสม่ำเสมอ ใช้เวลาเพิ่มเล็กน้อย (ทดลอง)',
86  };
87  const ALGO_NAMES = { greedy: 'Greedy', ga: 'Genetic Algorithm', hybrid: 'Hybrid', hybrid_rl: 'Hybrid + RL' };
88  let SELECTED_ALGO = 'hybrid';
บรรทัด 81–86: ALGO_HINTS ข้อความอธิบายแต่ละอัลกอริทึม (Greedy ➜ algorithm/greedy.py GA ➜ algorithm/genetic.py Hybrid ➜ algorithm/hybrid.py และ +RL ➜ algorithm/rl.py)
บรรทัด 87: ALGO_NAMES ชื่อแสดงของอัลกอริทึม (➜ frontend/extras.js ใช้ตอนเทียบ)
บรรทัด 88: SELECTED_ALGO ตัวเลือกปัจจุบัน ตั้งต้น Hybrid
บรรทัด 93–123  เลือกอัลกอริทึมและโหมด Developer
93  function initAlgoControl() {
94    document.querySelectorAll('#algoControl button').forEach(b => {
95      b.onclick = () => {
96        document.querySelectorAll('#algoControl button').forEach(x => x.classList.remove('active'));
97        b.classList.add('active');
98        SELECTED_ALGO = b.dataset.val;
99        document.getElementById('algoHint').textContent = ALGO_HINTS[SELECTED_ALGO];
100      };
101    });
102    // โหมด Developer: เปิดจากปุ่ม </> บนแถบบน หรือ ?dev=1 (จำค่าไว้ใน localStorage) — โหมดปกติรัน Hybrid เท่านั้น
103    let on = false;
104    try { on = localStorage.getItem('wet_dev') === '1'; } catch (e) { /* ใช้ค่าเริ่มต้น */ }
105    setDevMode(on);
106  }
107
108  function setDevMode(on) {
109    STATE.dev = !!on;
110    document.body.classList.toggle('dev-mode', STATE.dev);
111    document.getElementById('devBtn')?.setAttribute('aria-pressed', String(STATE.dev));
112    if (!STATE.dev) {   // ออกจากโหมด Developer → กลับไปใช้ Hybrid เสมอ
113      SELECTED_ALGO = 'hybrid';
114      document.querySelectorAll('#algoControl button').forEach(x => x.classList.toggle('active', x.dataset.val === 'hybrid'));
115      document.getElementById('algoHint').textContent = ALGO_HINTS.hybrid;
116    }
117    try { localStorage.setItem('wet_dev', STATE.dev ? '1' : '0'); } catch (e) { /* ไม่เก็บค่า */ }
118  }
119
120  function toggleDevMode() {
121    setDevMode(!STATE.dev);
122    showToast(STATE.dev ? 'โหมด Developer: เลือกอัลกอริทึมได้' : 'โหมดปกติ: ใช้ Hybrid', 'ok', 2500);
123  }
บรรทัด 93–101: initAlgoControl ผูกปุ่มอัลกอริทึมใน ➜ frontend/index.html: คลิกแล้วเปลี่ยนปุ่มที่เลือก ค่า SELECTED_ALGO และข้อความ hint
บรรทัด 102–105: อ่านโหมด Developer ที่จำไว้ใน localStorage แล้วเรียก setDevMode
บรรทัด 108–118: setDevMode ตั้ง STATE.dev เปิดปิดคลาส dev-mode ของ body (ซึ่ง ➜ frontend/style.css ใช้ซ่อน/แสดงองค์ประกอบ dev-only) ถ้าปิดโหมด บังคับกลับเป็น Hybrid และจำค่าลง localStorage
บรรทัด 120–123: toggleDevMode สลับโหมดแล้วแจ้งผ่าน showToast (ถูก ➜ frontend/extras.js ห่อให้ถามรหัสผ่านก่อนเปิด)
บรรทัด 128–149  ตรวจงบประมาณ
128  function initBudgetValidation() {
129    const budgetInput = document.getElementById('budget');
130    if (!budgetInput) return;
131    const hint = budgetInput.closest('.pf-col')?.querySelector('.pf-hint');
132    if (!hint) return;
133    budgetInput.addEventListener('input', () => {
134      const v = +budgetInput.value;
135      if (v < VALIDATION.budget.min) {
136        hint.textContent = `ต้องอย่างน้อย ${fmt(VALIDATION.budget.min)} บาท (ตอนนี้ ${fmt(v || 0)})`;
137        hint.style.color = 'var(--accent-danger)';
138        highlightField('budget', true);
139      } else if (v > VALIDATION.budget.max) {
140        hint.textContent = `สูงสุด ${fmt(VALIDATION.budget.max)} บาท`;
141        hint.style.color = 'var(--accent-danger)';
142        highlightField('budget', true);
143      } else {
144        hint.textContent = `${fmt(VALIDATION.budget.min)} - ${fmt(VALIDATION.budget.max)} บาท`;
145        hint.style.color = '';
146        highlightField('budget', false);
147      }
148    });
149  }
บรรทัด 128–132: initBudgetValidation อ่านช่องงบและข้อความ hint ใต้ช่อง ถ้าไม่มีก็ออก
บรรทัด 133–147: ทุกครั้งที่พิมพ์ ถ้าน้อยกว่าขั้นต่ำหรือมากกว่าขั้นสูง (VALIDATION.budget) แสดงข้อความสีแดงและไฮไลต์ช่อง ไม่เช่นนั้นคืนข้อความช่วงปกติ (ใช้ fmt และ highlightField)
บรรทัด 154–166  ธีม
154  function initTheme() {
155    const saved = localStorage.getItem('theme') || 'dark';
156    document.documentElement.dataset.theme = saved;
157  }
158
159  function toggleTheme() {
160    const cur = document.documentElement.dataset.theme || 'dark';
161    const next = cur === 'dark' ? 'light' : 'dark';
162    document.documentElement.dataset.theme = next;
163    localStorage.setItem('theme', next);
164    // re-tile map (since dark mode applies CSS filter)
165    if (STATE.map) STATE.map.invalidateSize();
166  }
บรรทัด 154–157: initTheme อ่านธีมที่จำไว้ (ตั้งต้นมืด) ใส่ที่ data-theme ของ html
บรรทัด 159–166: toggleTheme (ผูกกับปุ่มธีมใน ➜ frontend/index.html) สลับมืด/สว่าง จำลง localStorage และคำนวณขนาดแผนที่ใหม่เพราะโหมดมืดใช้ฟิลเตอร์ CSS
บรรทัด 171–178  ภาษาของตัวเลือกวันที่
171  let DATE_PICKER = null;
172  let SELECTED_DAYS = 3;
173
174  function fpLocale() {
175    let en = window.WET_LANG === 'en'; try { en = en || localStorage.getItem('wet_lang') === 'en'; } catch (e) { /* ใช้ค่าเริ่มต้น */ }
176    return (!en && window.flatpickr && flatpickr.l10ns && flatpickr.l10ns.th) ? 'th' : 'default';
177  }
178  window.addEventListener('wet-lang', () => { if (DATE_PICKER) { DATE_PICKER.set('locale', fpLocale()); updateDateSummary(DATE_PICKER.selectedDates); } });
บรรทัด 171–172: DATE_PICKER ตัวเลือกวันที่ และ SELECTED_DAYS จำนวนวันที่เลือก (ตั้งต้น 3)
บรรทัด 174–177: fpLocale เลือกภาษาไทยของ flatpickr ถ้าไม่ใช่โหมดอังกฤษ (➜ frontend/i18n.js ตั้ง WET_LANG)
บรรทัด 178: เมื่อสลับภาษา (เหตุการณ์ wet-lang) เปลี่ยนภาษาของปฏิทินและวาดสรุปวันใหม่
บรรทัด 180–261  ตัวเลือกช่วงวันที่
180  function initDateRange() {
181    const today = new Date();
182    const tomorrow = new Date(today.getTime() + 24*60*60*1000);
183    const day4    = new Date(today.getTime() + 4*24*60*60*1000);
184
185    DATE_PICKER = flatpickr('#dateRange', {
186      mode: 'range',
187      minDate: 'today',
188      maxDate: new Date().fp_incr(730),
189      locale: fpLocale(),
190      defaultDate: [tomorrow, day4],
191      dateFormat: 'Y-m-d',
192      altInput: true,
193      altFormat: 'j M Y',
194      onChange: (selectedDates) => {
195        // ถ้าเลือกแค่วันเดียว (กำลังรอวันสิ้นสุด) ให้ onDayCreate เพิ่มคำใบ้
196        updateDateSummary(selectedDates);
197      },
198      onDayCreate: (dObj, dStr, fp, dayElem) => {
199        // ถ้าเลือก start date แล้ว และ hover/click วันเดิม → แสดง tooltip "1 วัน"
200        if (fp.selectedDates.length === 1) {
201          const startTs = fp.selectedDates[0].getTime();
202          const cellTs  = dayElem.dateObj?.getTime();
203          if (cellTs === startTs) {
204            dayElem.title = 'คลิกเพื่อ One Day Trip';
205          }
206        }
207      },
208      onReady: (selectedDates, dateStr, instance) => {
209        const numWrapper = instance.currentYearElement?.closest('.numInputWrapper');
210        if (!numWrapper) return;
211        const prev = document.createElement('span');
212        prev.className = 'fp-year-prev';
213        prev.textContent = '‹';
214        prev.addEventListener('mousedown', (e) => {
215          e.preventDefault();
216          instance.changeMonth(-12, true);
217        });
218        const next = document.createElement('span');
219        next.className = 'fp-year-next';
220        next.textContent = '›';
221        next.addEventListener('mousedown', (e) => {
222          e.preventDefault();
223          instance.changeMonth(12, true);
224        });
225        numWrapper.parentNode.insertBefore(prev, numWrapper);
226        numWrapper.parentNode.insertBefore(next, numWrapper.nextSibling);
227      },
228      onOpen: (selectedDates, dateStr, instance) => {
229        setTimeout(() => {
230          const wrapper = document.querySelector('.date-range-input');
231          const cal = instance.calendarContainer;
232          if (!wrapper || !cal) return;
233          // center horizontally
234          const wRect = wrapper.getBoundingClientRect();
235          const calW  = cal.offsetWidth;
236          const newLeft = wRect.left + wRect.width / 2 - calW / 2 + window.scrollX;
237          cal.style.left = Math.max(8, newLeft) + 'px';
238          // shift up so calendar doesn't cover the input
239          const calH = cal.offsetHeight;
240          cal.style.top  = (wRect.top + window.scrollY - calH - 12) + 'px';
241        }, 0);
242      },
243      onClose: (selectedDates) => {
244        // ถ้าปิดโดยมีแค่ 1 วัน → ถือว่าเป็น One Day Trip
245        if (selectedDates.length === 1) {
246          const d = selectedDates[0];
247          DATE_PICKER.setDate([d, d], false);
248          updateDateSummary([d, d]);
249        }
250      },
251    });
252    updateDateSummary([tomorrow, day4]);
253
254    // ให้กดที่ไหนก็ได้บนกล่องวันที่ (รวมขอบและไอคอน) แล้วเปิด calendar
255    const wrapper = document.querySelector('.date-range-input');
256    if (wrapper) {
257      wrapper.addEventListener('click', function() {
258        if (DATE_PICKER && !DATE_PICKER.isOpen) DATE_PICKER.open();
259      });
260    }
261  }
บรรทัด 180–183: initDateRange คำนวณพรุ่งนี้และอีก 4 วัน เป็นค่าตั้งต้น
บรรทัด 185–193: สร้าง flatpickr แบบช่วงวัน เริ่มจากวันนี้ ไกลสุด 730 วัน ภาษาตาม fpLocale ค่าเริ่มต้นพรุ่งนี้ถึงอีก 4 วัน
บรรทัด 194–197: เมื่อเปลี่ยนการเลือกวัน เรียก updateDateSummary
บรรทัด 198–207: เมื่อสร้างช่องวัน ถ้าเลือกวันเริ่มแล้ว ให้วันเดิมมี tooltip "คลิกเพื่อ One Day Trip"
บรรทัด 208–227: เมื่อพร้อม เพิ่มปุ่ม ‹ › ข้างช่องปี เพื่อเลื่อนทีละ 12 เดือน
บรรทัด 228–242: เมื่อเปิดปฏิทิน จัดตำแหน่งให้อยู่กึ่งกลางเหนือช่องกรอกและไม่บังช่อง
บรรทัด 243–250: เมื่อปิดโดยเลือกแค่วันเดียว ถือเป็นทริปวันเดียว (ตั้งวันเริ่มกับวันสิ้นสุดเป็นวันเดียวกัน)
บรรทัด 252: วาดสรุปวันตั้งต้น
บรรทัด 254–260: ให้คลิกที่ไหนก็ได้บนกล่องวันที่ (รวมขอบและไอคอน) แล้วเปิดปฏิทิน
บรรทัด 266–313  สรุปวันที่และจำนวนวัน
266  function getSelectedDays() {
267    return SELECTED_DAYS;
268  }
269
270  function updateDateSummary(dates) {
271    const sumEl = document.getElementById('dateSummary');
272    const fmtDate = d => d.toLocaleDateString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH'), {day:'numeric', month:'short', year:'numeric'});
273
274    // กำลังเลือกวันแรก (ยังไม่ได้เลือกวันสิ้นสุด)
275    if (!dates || dates.length < 1) {
276      sumEl.textContent = 'กรุณาเลือกช่วงวันเดินทาง';
277      sumEl.className = 'date-summary invalid';
278      SELECTED_DAYS = 3;
279      setOneDayTripMode(false);
280      return;
281    }
282
283    // เลือกวันเดียว (คลิก 1 ครั้ง หรือเลือกวันเดิม 2 ครั้ง)
284    if (dates.length === 1) {
285      sumEl.innerHTML = `${ic('sunrise')} <b>One Day Trip</b> · ${fmtDate(dates[0])} — เลือกวันสิ้นสุดหรือคลิกวันเดิมอีกครั้ง`;
286      sumEl.className = 'date-summary oneday';
287      SELECTED_DAYS = 1;
288      setOneDayTripMode(true);
289      return;
290    }
291
292    const [ci, co] = dates;
293    const nights = Math.round((co - ci) / (24*60*60*1000));
294    const days = nights + 1;
295
296    if (nights === 0) {
297      // เลือกวันเดิมเป็น start และ end → One Day Trip
298      sumEl.innerHTML = `${ic('sunrise')} <b>One Day Trip</b> · ${fmtDate(ci)}`;
299      sumEl.className = 'date-summary oneday';
300      SELECTED_DAYS = 1;
301      setOneDayTripMode(true);
302    } else if (days > 7) {
303      sumEl.innerHTML = `เลือกได้ไม่เกิน 7 วัน (ขณะนี้ <b>${days} วัน ${nights} คืน</b>) — ระบบจะใช้แค่ 7 วัน`;
304      sumEl.className = 'date-summary invalid';
305      SELECTED_DAYS = 7;
306      setOneDayTripMode(false);
307    } else {
308      sumEl.innerHTML = `<b>${fmtDate(ci)}</b> → <b>${fmtDate(co)}</b> · ${days} วัน ${nights} คืน`;
309      sumEl.className = 'date-summary';
310      SELECTED_DAYS = days;
311      setOneDayTripMode(false);
312    }
313  }
บรรทัด 266–268: getSelectedDays คืนจำนวนวันที่เลือก
บรรทัด 270–272: updateDateSummary อ่านกล่องสรุป #dateSummary และเตรียมฟังก์ชันจัดรูปวันที่ตามภาษา (ถูกห่อโดย ➜ updateHint() ใน frontend/extras.js ให้อัปเดตข้อความอากาศ)
บรรทัด 275–281: ถ้ายังไม่ได้เลือกวัน แสดงข้อความขอให้เลือก ตั้ง 3 วัน และปิดโหมดทริปวันเดียว
บรรทัด 284–290: เลือกวันเดียว: แสดง "One Day Trip" และตั้งเป็น 1 วัน
บรรทัด 292–294: คำนวณจำนวนคืนและจำนวนวันจากวันเริ่ม/สิ้นสุด
บรรทัด 296–301: ถ้าวันเริ่มกับวันสิ้นสุดตรงกัน ถือเป็นทริปวันเดียว
บรรทัด 302–306: ถ้าเกิน 7 วัน แสดงคำเตือนและใช้ 7 วัน
บรรทัด 307–312: กรณีปกติ แสดงช่วงวันที่ จำนวนวัน และคืน
บรรทัด 313: ปิดฟังก์ชัน
บรรทัด 315–345  โหมดทริปวันเดียว
315  function setOneDayTripMode(isOneDay) {
316    const checkbox = document.getElementById('includeHotel');
317    const label    = document.getElementById('hotelToggleLabel');
318    const hint     = document.getElementById('hotelHint');
319    const card     = document.getElementById('hotelOptionCard');
320    const icon     = document.getElementById('hotelCardIcon');
321    if (!checkbox) return;
322
323    if (isOneDay) {
324      checkbox.checked  = false;
325      checkbox.disabled = true;
326      card?.classList.add('hotel-card-locked');
327      if (icon) icon.innerHTML = ic('lock');
328      // Badge inline กับ title row
329      const titleRow = card?.querySelector('.hotel-card-title-row');
330      if (titleRow && !titleRow.querySelector('.hotel-lock-badge')) {
331        const badge = document.createElement('span');
332        badge.className = 'hotel-lock-badge';
333        badge.innerHTML = ic('sunrise') + ' One Day Trip';
334        titleRow.appendChild(badge);
335      }
336      label.textContent = 'ไม่รวมค่าโรงแรม';
337      hint.textContent  = 'ทริปวันเดียวไม่มีค่าที่พัก — ใช้งบทั้งหมดสำหรับกิจกรรม';
338    } else {
339      checkbox.disabled = false;
340      card?.classList.remove('hotel-card-locked');
341      if (icon) icon.innerHTML = checkbox.checked ? ic('hotel') : ic('hotel-off');
342      card?.querySelector('.hotel-lock-badge')?.remove();
343      onHotelToggle();
344    }
345  }
บรรทัด 315–321: setOneDayTripMode อ่านองค์ประกอบของตัวเลือกโรงแรม (ช่องติ๊ก ป้าย ข้อความ การ์ด ไอคอน) ถ้าไม่มีช่องติ๊กก็ออก
บรรทัด 323–327: ถ้าเป็นทริปวันเดียว เอาติ๊กออก ปิดการใช้ช่อง ใส่คลาสล็อกที่การ์ด และเปลี่ยนไอคอนเป็นกุญแจ
บรรทัด 328–335: เพิ่มป้าย "One Day Trip" ในแถวหัวการ์ด (ถ้ายังไม่มี)
บรรทัด 336–337: เปลี่ยนข้อความเป็น "ไม่รวมค่าโรงแรม" และอธิบายว่าใช้งบทั้งหมดกับกิจกรรม
บรรทัด 338–344: ไม่ใช่ทริปวันเดียว: เปิดช่องใช้ได้ คืนไอคอน เอาป้ายออก แล้วเรียก onHotelToggle ให้ข้อความตรงสถานะ
บรรทัด 347–377  จำนวนคนและตัวเลือกโรงแรม
347  function changeTravelers(delta) {
348    const inp = document.getElementById('travelers');
349    const v = Math.min(10, Math.max(1, +inp.value + delta));
350    inp.value = v;
351  }
352
353  function toggleHotelOption() {
354    // คลิกที่ card ทั้งใบ → toggle checkbox (ยกเว้นเมื่อล็อค)
355    const checkbox = document.getElementById('includeHotel');
356    if (!checkbox || checkbox.disabled) return;
357    checkbox.checked = !checkbox.checked;
358    onHotelToggle();
359  }
360
361  function onHotelToggle() {
362    const checkbox = document.getElementById('includeHotel');
363    if (checkbox?.disabled) return;  // ล็อคโดย One Day Trip
364    const checked = checkbox?.checked;
365    const label = document.getElementById('hotelToggleLabel');
366    const hint  = document.getElementById('hotelHint');
367    const icon  = document.getElementById('hotelCardIcon');
368    if (checked) {
369      label.textContent = 'รวมค่าโรงแรมในงบประมาณ';
370      hint.textContent  = 'ระบบจะหักค่าโรงแรมออกจากงบก่อนวางแผนกิจกรรม';
371      if (icon) icon.innerHTML = ic('hotel');
372    } else {
373      label.textContent = 'ไม่รวมค่าโรงแรม';
374      hint.textContent  = 'เหมาะสำหรับทริปวันเดียว หรือมีที่พักของตัวเองแล้ว';
375      if (icon) icon.innerHTML = ic('hotel-off');
376    }
377  }
บรรทัด 347–351: changeTravelers เปลี่ยนจำนวนคนทีละ 1 หนีบให้อยู่ในช่วง 1–10 (ปุ่มใน ➜ frontend/index.html)
บรรทัด 353–359: toggleHotelOption เมื่อคลิกการ์ดโรงแรม สลับช่องติ๊ก (ยกเว้นถูกล็อก) แล้วเรียก onHotelToggle
บรรทัด 361–377: onHotelToggle ถ้าถูกล็อกออก ไม่เช่นนั้นเปลี่ยนข้อความและไอคอนตามสถานะติ๊ก (รวมโรงแรมในงบหรือไม่)
บรรทัด 382–390  สร้างแผนที่
382  function initMap() {
383    STATE.map = L.map('map', {zoomControl: true, attributionControl: false}).setView([7.88, 98.36], 11);
384    // tile.openstreetmap.org ตอบ 403 (Access blocked) เมื่อรันจาก localhost และ CARTO ต้องใช้ API key
385    // จึงใช้ Esri World Street Map ซึ่งไม่ต้องมี key (ต้องแสดง attribution)
386    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
387      maxZoom: 19,
388    }).addTo(STATE.map);
389    L.control.attribution({prefix: false}).addAttribution('Tiles © Esri — Esri, HERE, Garmin, © OpenStreetMap contributors').addTo(STATE.map);
390  }
บรรทัด 382–383: initMap สร้างแผนที่ Leaflet ใน #map ตั้งต้นที่ภูเก็ต (7.88, 98.36) ซูม 11
บรรทัด 384–389: ใช้ภาพพื้นหลังแผนที่ Esri (ไม่ต้องมีคีย์ เพราะ tile ของ OpenStreetMap ตอบ 403 เมื่อรันจาก localhost และ CARTO ต้องใช้คีย์) พร้อมแสดงที่มาตามที่กำหนด
บรรทัด 395–399  สถานะ API
395  function setApiStatus(state, text) {
396    const el = document.getElementById('apiStatus');
397    el.className = 'api-status ' + state;
398    el.querySelector('.status-text').textContent = text;
399  }
บรรทัด 395–399: setApiStatus เปลี่ยนคลาสและข้อความของป้ายสถานะการเชื่อมต่อ backend ใน ➜ frontend/index.html
บรรทัด 404–447  ความชอบของผู้ใช้
404  const PREF = {};   // category -> 'like' | 'avoid' (ไม่มีคีย์ = ปกติ)
405
406  function initPrefs() {
407    const box = document.getElementById('prefChips');
408    if (!box) return;
409    Object.entries(CAT_LABELS).filter(([k]) => k !== 'all' && k !== 'restaurant').forEach(([k, label]) => {
410      // ชื่อหมวด + ปุ่มไอคอน 👍 (ชอบ) / 👎 (ไม่ชอบ) ด้านหลัง กดซ้ำเพื่อยกเลิก — พื้นหลังเขียว=ชอบ แดง=ไม่ชอบ
411      const w = document.createElement('div');
412      w.className = 'pref-cat';
413      w.dataset.cat = k;
414      w.innerHTML = `<span class="pc-name">${label}</span><button type="button" class="pc-like" title="ชอบ">${ic('thumb')}</button><button type="button" class="pc-dislike" title="ไม่ชอบ">${ic('thumb')}</button>`;
415      const paint = () => {
416        w.dataset.state = PREF[k] || '';
417        w.querySelector('.pc-like').title = PREF[k] === 'like' ? 'ยกเลิก "ชอบ"' : 'ชอบ';
418        w.querySelector('.pc-dislike').title = PREF[k] === 'avoid' ? 'ยกเลิก "ไม่ชอบ"' : 'ไม่ชอบ';
419      };
420      const set = st => { if (PREF[k] === st) delete PREF[k]; else PREF[k] = st; paint(); updatePrefSummary(); };
421      w.querySelector('.pc-like').onclick = () => set('like');
422      w.querySelector('.pc-dislike').onclick = () => set('avoid');
423      paint();
424      box.appendChild(w);
425    });
426  }
427
428  function togglePrefs() {
429    const p = document.getElementById('prefPanel');
430    p.hidden = !p.hidden;
431    document.getElementById('prefToggle')?.setAttribute('aria-expanded', String(!p.hidden));
432  }
433
434  function getPreferences() {
435    const liked = Object.keys(PREF).filter(k => PREF[k] === 'like');
436    const avoided = Object.keys(PREF).filter(k => PREF[k] === 'avoid');
437    const diet = document.getElementById('prefDiet')?.value || 'none';
438    return (liked.length || avoided.length || diet !== 'none') ? {liked, avoided, diet} : null;
439  }
440
441  function updatePrefSummary() {
442    const p = getPreferences();
443    const dietLabel = {vegetarian: 'มังสวิรัติ', halal: 'ฮาลาล'};
444    document.getElementById('prefSummary').textContent = p
445      ? '· ' + [p.liked.length && `ชอบ ${p.liked.length}`, p.avoided.length && `ไม่ชอบ ${p.avoided.length}`, dietLabel[p.diet]].filter(Boolean).join(' · ')
446      : '';
447  }
บรรทัด 404: PREF ตารางหมวด → "like" หรือ "avoid" (ไม่มีคีย์คือปกติ) ที่ส่งไป ➜ backend/main.py เพื่อกรองและถ่วงน้ำหนักก่อนวางแผน
บรรทัด 406–408: initPrefs หาที่ว่างของชิป ถ้าไม่มีออก
บรรทัด 409–414: สร้างชิปของแต่ละหมวด (ไม่รวม "ทั้งหมด" และร้านอาหาร) ที่มีชื่อ และปุ่มชอบ/ไม่ชอบ
บรรทัด 415–419: paint ตั้งสถานะและ title ของปุ่ม (กดซ้ำคือยกเลิก)
บรรทัด 420–424: set สลับค่า ลบคีย์ถ้ากดซ้ำ แล้ววาดและอัปเดตสรุป ผูกปุ่มและต่อชิปเข้าแผง
บรรทัด 428–432: togglePrefs เปิดปิดแผงความชอบและ aria-expanded (ผูกกับปุ่มใน ➜ frontend/index.html)
บรรทัด 434–439: getPreferences รวมหมวดที่ชอบ ไม่ชอบ และอาหาร คืน null ถ้าไม่ได้ตั้งอะไร (ส่งเป็น preferences ใน ➜ searchPackages() ใน frontend/app.js)
บรรทัด 441–447: updatePrefSummary เขียนสรุปข้างปุ่มความชอบ เช่น "ชอบ 2 · ไม่ชอบ 1 · มังสวิรัติ"
บรรทัด 452–468  ตัวช่วยไฟล์ปฏิทิน
452  function icsEscape(s) {
453    return String(s).replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;');
454  }
455
456  // พับบรรทัดตาม RFC 5545 (≤75 octets ต่อบรรทัด) โดยไม่ตัดกลางตัวอักษร UTF-8
457  function icsFold(line) {
458    const enc = new TextEncoder();
459    const out = [];
460    let cur = '', bytes = 0;
461    for (const ch of line) {
462      const n = enc.encode(ch).length;
463      if (bytes + n > (out.length ? 74 : 75)) { out.push(cur); cur = ''; bytes = 0; }
464      cur += ch; bytes += n;
465    }
466    out.push(cur);
467    return out.join('\r\n ');
468  }
บรรทัด 452–454: icsEscape หลีกอักขระพิเศษของรูปแบบ iCalendar (\ ขึ้นบรรทัดใหม่ , ;)
บรรทัด 457–468: icsFold พับบรรทัดไม่ให้เกิน 75 ไบต์ตาม RFC 5545 โดยไม่ตัดกลางตัวอักษร UTF-8 (นับไบต์ด้วย TextEncoder และใช้บรรทัดต่อด้วยช่องว่างนำ)
บรรทัด 470–498  สร้างไฟล์ .ics
470  function buildIcs(pkg, startDate) {
471    const pad = n => String(n).padStart(2, '0');
472    const stamp = d => `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}`;
473    const local = (d, min) => `${stamp(d)}T${pad(Math.floor(min / 60) % 24)}${pad(min % 60)}00`;
474    const now = new Date().toISOString().replace(/[-:]/g, '').slice(0, 15) + 'Z';
475    const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//WeEasyTrip//TH', 'CALSCALE:GREGORIAN',
476                   'X-WR-CALNAME:' + icsEscape(`WeEasyTrip ${pkg.tier}`), 'X-WR-TIMEZONE:Asia/Bangkok'];
477    pkg.days.forEach((day, dIdx) => {
478      const date = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate() + dIdx);
479      const arrive = Object.fromEntries((day.arrivals || []).map(([id, m]) => [id, m]));
480      day.pois.forEach(poi => {
481        const start = arrive[poi.id];
482        if (start === undefined) return;
483        const desc = `${CAT_LABELS[poi.category] || poi.category} · ค่าใช้จ่าย ${fmt(poi.cost)} บาท`;
484        lines.push('BEGIN:VEVENT',
485          `UID:${poi.id}-${stamp(date)}-${dIdx}@weeasytrip`,
486          `DTSTAMP:${now}`,
487          `DTSTART:${local(date, start)}`,
488          `DTEND:${local(date, start + poi.duration_min)}`,
489          'SUMMARY:' + icsEscape(poi.name_th || poi.name_en),
490          'DESCRIPTION:' + icsEscape(desc),
491          `GEO:${poi.lat};${poi.lng}`,
492          'LOCATION:' + icsEscape(poi.name_en || poi.name_th),
493          'END:VEVENT');
494      });
495    });
496    lines.push('END:VCALENDAR');
497    return lines.map(icsFold).join('\r\n') + '\r\n';
498  }
บรรทัด 470–474: buildIcs ตัวช่วยจัดรูปวันที่/เวลาแบบ local (floating) และเวลาประทับ
บรรทัด 475–476: ส่วนหัวของปฏิทิน ชื่อ และเขตเวลา Asia/Bangkok
บรรทัด 477–479: แต่ละวัน คำนวณวันที่จริงจากวันเริ่ม และตารางเวลาถึงของแต่ละจุดจาก day.arrivals (ที่ ➜ backend/main.py คำนวณ)
บรรทัด 480–483: แต่ละสถานที่ที่มีเวลาถึง สร้างคำอธิบายด้วยหมวดและค่าใช้จ่าย
บรรทัด 484–493: เพิ่มเหตุการณ์ VEVENT: รหัส เวลาเริ่ม/จบ (จาก duration_min) ชื่อ คำอธิบาย พิกัด และสถานที่
บรรทัด 496–497: ปิดปฏิทิน พับบรรทัดและเชื่อมด้วย CRLF
บรรทัด 500–513  ดาวน์โหลดไฟล์ปฏิทิน
500  function exportIcs() {
501    const pkg = STATE.selectedPkg;
502    if (!pkg) return;
503    const start = (DATE_PICKER && DATE_PICKER.selectedDates[0]) || new Date();
504    const blob = new Blob([buildIcs(pkg, start)], {type: 'text/calendar;charset=utf-8'});
505    const a = document.createElement('a');
506    a.href = URL.createObjectURL(blob);
507    a.download = `weeasytrip-${getProvince()}-${pkg.tier.toLowerCase()}.ics`;
508    document.body.appendChild(a);
509    a.click();
510    a.remove();
511    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
512    showToast('ดาวน์โหลดไฟล์ปฏิทินแล้ว', 'ok');
513  }
บรรทัด 500–503: exportIcs (ผูกกับปุ่มใน ➜ frontend/index.html) ถ้าไม่มีแผนออก หาวันเริ่มจากตัวเลือกวัน (ไม่มีใช้วันนี้)
บรรทัด 504–511: สร้าง Blob และลิงก์ดาวน์โหลดชั่วคราว คลิก ลบ และเรียกคืน URL หลัง 1 วินาที
บรรทัด 512: แจ้งผู้ใช้
บรรทัด 518–533  ตั้งค่าที่ส่งขึ้นเซสชัน
518  function sessionSettings() {
519    const d = DATE_PICKER && DATE_PICKER.selectedDates[0];
520    return {
521      budget: +document.getElementById('budget').value,
522      travelers: +document.getElementById('travelers').value,
523      include_hotel: STATE.includeHotel !== false,
524      start_date: d ? `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}` : null,
525      preferences: getPreferences(),
526      locked: [...STATE.locked], excluded: [...STATE.excluded],
527      base_warn: STATE.selectedPkg && STATE.selectedPkg._base instanceof Set ? [...STATE.selectedPkg._base] : null,   // คำเตือนตั้งต้นของแผน ใช้ร่วมกันทุกเครื่อง ไม่งั้นแต่ละเครื่องตั้งต้นต่างกันแล้วเห็นคำเตือนไม่เหมือนกัน
528    };
529  }
530  function applyBaseWarn(pkg, st) { if (pkg && st && Array.isArray(st.base_warn)) setHidden(pkg, '_base', new Set(st.base_warn)); return pkg; }
531
532  // แผนจาก session อาจมี _base ที่ถูก serialize เป็น {} (จากรุ่นเก่า): ลบทิ้งเพื่อให้คำนวณคำเตือนตั้งต้นใหม่
533  function cleanShared(p) { if (p && !(p._base instanceof Set)) delete p._base; return p; }
บรรทัด 518–528: sessionSettings รวมงบ จำนวนคน ตัวเลือกโรงแรม วันเริ่ม ความชอบ ชุด locked/excluded และ base_warn (คำเตือนตั้งต้นของแผน เพื่อให้ทุกเครื่องเห็นคำเตือนชุดเดียวกัน) เป็นอ็อบเจ็กต์ที่ส่งไปให้เพื่อน
บรรทัด 530: applyBaseWarn นำ base_warn จากค่าตั้งมาตั้งเป็นคำเตือนตั้งต้นของแผน (เก็บเป็น Set ที่ซ่อนจาก JSON ด้วย setHidden)
บรรทัด 532–533: cleanShared ลบ _base ที่ถูก serialize เป็น {} (จากเซสชันรุ่นเก่า) เพื่อให้คำนวณคำเตือนตั้งต้นใหม่ ไม่เช่นนั้นเรียก .has ไม่ได้
บรรทัด 535–545  นำสถานะที่ได้มาใช้
535  function applySharedState(data, announce) {
536    STATE.selectedPkg = cleanShared(data.package);
537    const st = data.settings || {};
538    applyBaseWarn(STATE.selectedPkg, st);
539    STATE.locked = new Set(st.locked || []);
540    STATE.excluded = new Set(st.excluded || []);
541    STATE.session.version = data.version;
542    drawOnMap(STATE.selectedPkg);
543    renderDetail(STATE.selectedPkg);
544    if (announce) showToast(announce, 'ok', 3000);
545  }
บรรทัด 535–538: applySharedState ตั้งแผน (ผ่าน cleanShared) และคืนคำเตือนตั้งต้นด้วย applyBaseWarn
บรรทัด 539–541: ตั้งจุดที่ล็อกและลบ และเลขรุ่น (version) จากข้อมูลของเซสชัน
บรรทัด 542–544: วาดแผนที่ (➜ drawOnMap() ใน frontend/app.js) และรายละเอียด (➜ renderDetail() ใน frontend/app.js) ใหม่ และแจ้งข้อความถ้ามี
บรรทัด 547–568  สร้างลิงก์แชร์
547  async function shareSession() {
548    const pkg = STATE.selectedPkg;
549    if (!pkg) return;
550    try {
551      if (!STATE.session) {
552        const res = await fetch(`${API_BASE}/api/sessions`, {
553          method: 'POST', headers: {'Content-Type': 'application/json'},
554          body: JSON.stringify({province: getProvince(), package: pkg, settings: sessionSettings()}),
555        });
556        if (!res.ok) throw new Error(`HTTP ${res.status}`);
557        const data = await res.json();
558        STATE.session = {id: data.id, version: data.version, timer: null, busy: false};
559        history.replaceState(null, '', `?s=${data.id}`);
560        startSessionPolling();
561      }
562      const url = location.href;
563      try { await navigator.clipboard.writeText(url); showToast('คัดลอกลิงก์แล้ว — ส่งให้เพื่อนเพื่อวางแผนร่วมกัน', 'ok', 4500); }
564      catch (e) { window.prompt('คัดลอกลิงก์นี้ส่งให้เพื่อน', url); }
565    } catch (e) {
566      showToast(`แชร์ไม่สำเร็จ: ${e.message}`, 'error');
567    }
568  }
บรรทัด 547–549: shareSession ถ้าไม่มีแผนออก
บรรทัด 551–558: ถ้ายังไม่มีเซสชัน ส่ง POST ไป /api/sessions (➜ create_session() ใน backend/main.py) พร้อมจังหวัด แผน และค่าตั้ง แล้วจดรหัสเซสชันและเลขรุ่น
บรรทัด 559–560: ใส่ ?s=<รหัส> ใน URL และเริ่มโพลล์ดูการเปลี่ยนแปลง
บรรทัด 562–564: คัดลอกลิงก์ลงคลิปบอร์ด ถ้าทำไม่ได้แสดงช่องให้คัดลอกเอง
บรรทัด 565–567: ถ้าผิดพลาดแจ้งข้อความ
บรรทัด 570–589  โพลล์ดูการแก้ไขของเพื่อน
570  function startSessionPolling() {
571    clearInterval(STATE.session.timer);
572    STATE.session.timer = setInterval(async () => {
573      const ss = STATE.session;
574      if (!ss || ss.busy || document.hidden) return;
575      try {
576        const res = await fetch(`${API_BASE}/api/sessions/${ss.id}?since=${ss.version}`);
577        if (res.status === 404) { clearInterval(ss.timer); showToast('เซสชันหมดอายุแล้ว', 'error'); STATE.session = null; return; }
578        if (!res.ok) return;
579        const data = await res.json();
580        if (data.changed) {
581          try { applySharedState(data, 'เพื่อนแก้ไขแผน — อัปเดตให้แล้ว'); }
582          catch (e) {   // แสดงผลแผนจากเพื่อนไม่สำเร็จ: ต้องไม่เงียบ ไม่งั้นดูเหมือน "ไม่มีการอัปเดต"
583            console.error('applySharedState', e);
584            if (!ss.errShown) { ss.errShown = true; showToast(`รับแผนจากเพื่อนไม่สำเร็จ: ${e.message} (ลองรีเฟรชหน้า Ctrl+F5)`, 'error', 8000); }
585          }
586        }
587      } catch (e) { /* เครือข่ายสะดุด: ลองใหม่รอบหน้า */ }
588    }, 2000);
589  }
บรรทัด 570–572: startSessionPolling ล้างตัวจับเวลาเก่า แล้วตั้งทุก 2 วินาที
บรรทัด 573–574: ข้ามถ้าไม่มีเซสชัน กำลังส่งอยู่ (busy) หรือแท็บถูกซ่อน
บรรทัด 576–578: ถามเซสชันตามเลขรุ่น ถ้า 404 แจ้งว่าหมดอายุและหยุด
บรรทัด 580–586: ถ้ามีการเปลี่ยน นำสถานะใหม่มาใช้ และแจ้ง "เพื่อนแก้ไขแผน — อัปเดตให้แล้ว" ถ้าแสดงผลไม่สำเร็จ บันทึกข้อผิดพลาดใน console และแจ้งผู้ใช้ครั้งเดียว (errShown) ให้รีเฟรชหน้า (เดิมล้มเงียบ ดูเหมือนไม่มีการอัปเดต)
บรรทัด 587: เครือข่ายสะดุดข้ามไปลองรอบหน้า
บรรทัด 592–609  ส่งการแก้ไขของเราขึ้นเซสชัน
592  async function pushSession() {
593    const ss = STATE.session;
594    if (!ss) return;
595    ss.busy = true;
596    try {
597      const res = await fetch(`${API_BASE}/api/sessions/${ss.id}`, {
598        method: 'PUT', headers: {'Content-Type': 'application/json'},
599        body: JSON.stringify({base_version: ss.version, package: STATE.selectedPkg, settings: sessionSettings()}),
600      });
601      if (res.status === 409) {
602        const err = await res.json();
603        applySharedState(err.detail, 'มีคนแก้ไขพร้อมกัน — ใช้ฉบับล่าสุดของเพื่อน');
604      } else if (res.ok) {
605        ss.version = (await res.json()).version;
606      }
607    } catch (e) { console.warn('pushSession', e); /* ออฟไลน์: เก็บไว้ในเครื่อง */ }
608    finally { ss.busy = false; }
609  }
บรรทัด 592–595: pushSession ออกถ้าไม่มีเซสชัน ตั้ง busy ให้โพลล์ไม่ซ้อน
บรรทัด 597–600: ส่ง PUT พร้อมเลขรุ่นฐาน แผน และค่าตั้ง ไป ➜ update_session() ใน backend/main.py
บรรทัด 601–603: ถ้า 409 (มีคนแก้ก่อน) ใช้ฉบับล่าสุดของเพื่อนแทน และแจ้งผู้ใช้
บรรทัด 604–606: ถ้าสำเร็จ จดเลขรุ่นใหม่
บรรทัด 607–608: ถ้าออฟไลน์เก็บในเครื่องและบันทึกคำเตือนใน console และปลดสถานะ busy เสมอ
บรรทัด 611–650  เข้าร่วมเซสชันจากลิงก์
611  async function joinSession(id) {
612    try {
613      const res = await fetch(`${API_BASE}/api/sessions/${id}`);
614      if (!res.ok) throw new Error(res.status === 404 ? 'ลิงก์หมดอายุหรือไม่ถูกต้อง' : `HTTP ${res.status}`);
615      const data = await res.json();
616      const st = data.settings || {};
617      const item = [...document.querySelectorAll('#provList .prov-item')].find(i => i.dataset.value === data.province);
618      if (item) {                                   // ตั้งจังหวัดโดยไม่ล้างผลซ้ำ แล้วโหลดข้อมูลจังหวัดนั้น
619        document.querySelectorAll('.prov-item').forEach(i => i.classList.remove('prov-active'));
620        item.classList.add('prov-active');
621        document.getElementById('province').value = data.province;
622        document.getElementById('provName').textContent = item.dataset.label;
623      }
624      await loadPois();
625      if (st.budget) document.getElementById('budget').value = st.budget;
626      if (st.travelers) document.getElementById('travelers').value = st.travelers;
627      if (st.start_date && DATE_PICKER) {
628        const d0 = new Date(st.start_date + 'T00:00:00');
629        const d1 = new Date(d0.getTime() + (data.package.days.length - 1) * 86400000);
630        DATE_PICKER.setDate([d0, d1], true);
631      }
632      STATE.includeHotel = st.include_hotel !== false;
633      STATE.session = {id: data.id, version: data.version, timer: null, busy: false};
634      document.getElementById('detailPanel').style.display = 'block';
635      STATE.selectedPkg = applyBaseWarn(cleanShared(data.package), st);
636      STATE.locked = new Set(st.locked || []); STATE.excluded = new Set(st.excluded || []);
637      renderDetail(STATE.selectedPkg);
638      setTimeout(() => {
639        STATE.map.invalidateSize();
640        drawOnMap(STATE.selectedPkg);
641        document.getElementById('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
642        setTimeout(syncMapHeight, 150);
643      }, 150);
644      startSessionPolling();
645      showToast('เข้าร่วมแผนที่เพื่อนแชร์มา — แก้ไขแล้วทุกคนเห็นพร้อมกัน', 'ok', 4500);
646    } catch (e) {
647      showToast(`เข้าร่วมไม่ได้: ${e.message}`, 'error', 6000);
648      await loadPois();
649    }
650  }
บรรทัด 611–615: joinSession ขอข้อมูลเซสชัน ถ้า 404 แจ้งว่าลิงก์หมดอายุหรือไม่ถูกต้อง
บรรทัด 616–623: ตั้งจังหวัดในเมนูและช่องซ่อนโดยไม่ล้างผลซ้ำ
บรรทัด 624: โหลดสถานที่ของจังหวัดนั้น (➜ loadPois() ใน frontend/app.js)
บรรทัด 625–631: คืนค่างบ จำนวนคน และช่วงวันที่จากค่าตั้งที่แชร์
บรรทัด 632–637: ตั้งสถานะโรงแรม เซสชัน แผน (ผ่าน cleanShared และ applyBaseWarn) จุดที่ล็อกและลบ แล้วแสดงรายละเอียด
บรรทัด 638–643: หน่วง 150 มิลลิวินาที แล้ววาดแผนที่ เลื่อนหน้า และปรับความสูงแผนที่
บรรทัด 644–645: เริ่มโพลล์ และแจ้งว่าเข้าร่วมแล้ว
บรรทัด 646–649: ถ้าผิดพลาดแจ้งข้อความและโหลดสถานที่ตามปกติ
บรรทัด 655–693  ตัวช่วยเวลา และประวัติย้อนกลับ/เดินหน้า (undo/redo)
655  function fmtClock(min) {
656    return `${String(Math.floor(min / 60) % 24).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`;
657  }
658
659  // เก็บแผนตั้งต้นไว้เป็นคุณสมบัติที่ไม่ถูก serialize (ไม่ปนใน session/ไฟล์บันทึก)
660  function setHidden(obj, key, value) { Object.defineProperty(obj, key, {value, enumerable: false, writable: true, configurable: true}); }
661  const routeIds = p => JSON.stringify((p?.days || []).map(d => d.pois.map(x => x.id)));
662  // ย้อนกลับ / เดินหน้า (undo / redo) ทีละการแก้ไขเหมือนโปรแกรมแต่งภาพ: เก็บสำเนาแผนหลังการแก้แต่ละครั้ง (ลาก ลบ สลับ เพิ่ม สลับเป็นในร่ม) ผูกกับแผนตั้งต้น (_orig) ถ้าสร้างแผนใหม่ประวัติจะเริ่มใหม่
663  const HIST = {orig: null, base: null, stack: [], idx: -1, applying: false};
664  const histSnap = pkg => ({sig: routeIds(pkg) + JSON.stringify([...STATE.locked].sort()) + JSON.stringify([...STATE.excluded].sort()), pkg: JSON.parse(JSON.stringify(pkg)), locked: [...STATE.locked], excluded: [...STATE.excluded]});
665  function recordHistory(pkg) {
666    if (HIST.applying || !pkg._orig) return;
667    const s = histSnap(pkg);
668    if (HIST.orig !== pkg._orig) { HIST.orig = pkg._orig; HIST.stack = [s]; HIST.idx = 0; }
669    else if (s.sig !== HIST.stack[HIST.idx].sig) { HIST.stack = HIST.stack.slice(0, HIST.idx + 1); HIST.stack.push(s); HIST.idx++; if (HIST.stack.length > 50) { HIST.stack.shift(); HIST.idx--; } }
670    HIST.base = pkg._base;
671    updateHistBtns();
672  }
673  function updateHistBtns() {
674    const u = document.getElementById('undoBtn'), r = document.getElementById('redoBtn');
675    if (u) u.classList.toggle('disabled', HIST.idx <= 0);
676    if (r) r.classList.toggle('disabled', HIST.idx >= HIST.stack.length - 1);
677  }
678  function stepHistory(dir) {
679    const n = HIST.idx + dir; if (n < 0 || n >= HIST.stack.length || !STATE.selectedPkg) return;
680    HIST.idx = n; const e = HIST.stack[n], c = JSON.parse(JSON.stringify(e.pkg));
681    setHidden(c, '_orig', HIST.orig); if (HIST.base instanceof Set) setHidden(c, '_base', HIST.base);
682    STATE.selectedPkg = c; STATE.locked = new Set(e.locked); STATE.excluded = new Set(e.excluded);
683    HIST.applying = true;
684    try { drawOnMap(c); renderDetail(c); } finally { HIST.applying = false; }
685    updateHistBtns(); pushSession();
686    showToast(dir < 0 ? 'ย้อนกลับแล้ว' : 'ทำซ้ำแล้ว', 'ok', 1800);
687  }
688  const undoEdit = () => stepHistory(-1), redoEdit = () => stepHistory(1);
689  document.addEventListener('keydown', e => {
690    if (!(e.ctrlKey || e.metaKey) || e.target.closest?.('input, textarea, select, [contenteditable]') || document.querySelector('.modal.open')) return;
691    const k = e.key.toLowerCase();
692    if (k === 'z' && !e.shiftKey) { e.preventDefault(); undoEdit(); } else if (k === 'y' || (k === 'z' && e.shiftKey)) { e.preventDefault(); redoEdit(); }
693  });
บรรทัด 655–657: fmtClock แปลงนาทีจากเที่ยงคืนเป็นข้อความ HH:MM
บรรทัด 659–660: setHidden ตั้งคุณสมบัติที่ไม่ถูกนับตอนแปลงเป็น JSON (enumerable เป็นเท็จ) ใช้เก็บแผนตั้งต้นโดยไม่ปนไปกับเซสชันหรือไฟล์บันทึก
บรรทัด 661: routeIds ลายเซ็นลำดับ id ของสถานที่ทุกวัน
บรรทัด 662–664: HIST ตัวแปรสถานะประวัติ (แผนตั้งต้น ฐานคำเตือน กองประวัติ ตำแหน่ง และธง applying) และ histSnap สร้างสำเนาแผนพร้อมลายเซ็นของแผน ชุดล็อกและชุดลบ
บรรทัด 665–672: recordHistory ถ้ากำลังเรียกจาก undo/redo หรือไม่มีแผนตั้งต้นก็ข้าม ถ้าเป็นแผนใหม่เริ่มกองประวัติใหม่ ถ้าลายเซ็นเปลี่ยนตัดส่วนที่เดินหน้าทิ้ง เพิ่มรายการ (เก็บสูงสุด 50) แล้วอัปเดตปุ่ม (ถูกเรียกจากตัวห่อ renderDetail ใน ➜ recordHistory() ใน frontend/app.js )
บรรทัด 673–677: updateHistBtns ปิดปุ่มย้อนกลับเมื่ออยู่ต้นกอง และปุ่มเดินหน้าเมื่ออยู่ท้ายกอง
บรรทัด 678–687: stepHistory ขยับตำแหน่งในกอง คืนแผน (ตั้งคำเตือนตั้งต้น _base กลับเฉพาะเมื่อเป็น Set) ชุดล็อก/ลบ จากสำเนา วาดใหม่ในขณะตั้งธง applying แล้วส่งขึ้นเซสชัน (➜ pushSession() ใน frontend/app.js) และแจ้งผู้ใช้
บรรทัด 688: undoEdit และ redoEdit (ปุ่มที่ ➜ frontend/extras.js แทรกเรียกฟังก์ชันนี้)
บรรทัด 689–693: ปุ่มลัด Ctrl/Cmd+Z ย้อนกลับ และ Ctrl+Y หรือ Ctrl+Shift+Z เดินหน้า (ไม่ทำงานเมื่อกำลังพิมพ์หรือมีหน้าต่างเปิดอยู่)
บรรทัด 697–714  คำเตือนเวลาเปิด-ปิด
697  function uiWarnings(pkg, raw = false) {
698    const out = [], speed = (STATE.provinces[getProvince()] || {}).speed_kmh || 40;
699    (pkg.days || []).forEach((day, d) => {
700      let endT = 480, lat = pkg.hotel.lat, lng = pkg.hotel.lng;
701      day.pois.forEach(p => {
702        const full = {...(STATE.pois.find(q => q.id === p.id) || {}), ...p}, at = arriveOf(day, p);
703        const km = haversineKm(lat, lng, p.lat, p.lng), early = endT + km / speed * 60 * 1.25 + (km >= 0.3 ? 10 : 0);   // เวลาถึงก่อนรอร้านเปิด (ตัวคูณจราจร 1.25 + เผื่อจอด/เดิน 10 นาที ตรงกับ algorithm/utils.py)
704        if (full.close_min !== undefined && at >= 0 && at > full.close_min) out.push({d, id: p.id, type: 'late', poi: full});
705        else if (full.open_min > 0 && early < full.open_min - 10) out.push({d, id: p.id, type: 'early', poi: full});
706        endT = (at >= 0 ? at : early) + (p.duration_min || 0); lat = p.lat; lng = p.lng;
707      });
708    });
709    const key = w => `${w.id}:${w.type}`;
710    if (raw) return out;
711    // แผนที่ระบบสร้างเองมีการรอร้านเปิดตามปกติ จึงไม่เตือน: จำคำเตือนตั้งต้นของแผนไว้ (_base) แล้วแสดงเฉพาะที่เกิดใหม่หลังผู้ใช้แก้แผน
712    if (!(pkg._base instanceof Set)) { setHidden(pkg, '_base', new Set(out.map(key))); return []; }   // _base ต้องเป็น Set ที่ไม่ถูก serialize (ถ้าไปอยู่ใน JSON ของ session จะกลายเป็น {} แล้วเครื่องอื่นพัง)
713    return out.filter(w => !pkg._base.has(key(w)));
714  }
บรรทัด 697–698: uiWarnings เตรียมรายการ และความเร็วเดินทางของจังหวัด (ตั้งต้น 40 กม./ชม.)
บรรทัด 699–700: แต่ละวัน เริ่มที่ 8:00 (480 นาที) จากพิกัดโรงแรม
บรรทัด 701–703: แต่ละสถานที่ รวมข้อมูลเวลาเปิด-ปิดจาก STATE.pois หาเวลาถึงที่คำนวณไว้ (➜ arriveOf() ใน frontend/app.js) และประมาณเวลาถึงก่อนรอร้านเปิดด้วยระยะทาง haversineKm ตัวคูณจราจร 1.25 และเวลาเตรียม 10 นาที
บรรทัด 704–705: ถ้าเวลาถึงเกินเวลาปิด เป็นคำเตือน late ถ้าถึงก่อนร้านเปิดเกิน 10 นาที เป็น early
บรรทัด 706–708: อัปเดตเวลาสิ้นสุดและตำแหน่งปัจจุบัน
บรรทัด 709–710: key กุญแจคำเตือน และคืนทั้งหมดถ้า raw
บรรทัด 712: แผนที่ระบบสร้างมีการรอร้านเปิดตามปกติ จึงจำคำเตือนตั้งต้นเป็นฐาน (เก็บใน _base ที่เป็น Set ซ่อนจาก JSON ด้วย setHidden) และไม่เตือนครั้งแรก
บรรทัด 713–714: ครั้งต่อไปแสดงเฉพาะคำเตือนที่ผู้ใช้ทำเกิดใหม่ (ตัวแสดงผลคือ decorateWarnings ใน ➜ decorateWarnings() ใน frontend/extras.js)
บรรทัด 717–738  ตัวช่วยจัดรูปและเวลาถึง
717  function fmtDur(min) {
718    const m = Math.round(min), h = Math.floor(m / 60), r = m % 60;
719    return h ? (r ? `${h}H ${r}m` : `${h}H`) : `${r}m`;
720  }
721
722  function arriveOf(day, poi) {   // เวลาถึงที่อัลกอริทึมคำนวณ (นาทีจากเที่ยงคืน) หรือ -1 ถ้าไม่มี
723    const a = (day.arrivals || []).find(x => x[0] === poi.id);
724    return a ? a[1] : -1;
725  }
726
727  function hoursText(poi) {
728    if (poi.open_min === undefined) poi = STATE.pois.find(p => p.id === poi.id) || poi;   // POI ในแผนจาก API ไม่มีเวลาเปิด-ปิด
729    if (poi.open_min === undefined) return 'ไม่ระบุ';
730    if (poi.open_min <= 0 && poi.close_min >= 1439) return 'ทั้งวัน';
731    return `${fmtClock(poi.open_min)}–${fmtClock(poi.close_min)}`;
732  }
733
734  function strHash(str) {
735    let h = 2166136261;
736    for (const ch of str) { h ^= ch.codePointAt(0); h = Math.imul(h, 16777619); }
737    return h >>> 0;
738  }
บรรทัด 717–720: fmtDur แสดงระยะเวลาเป็น 45m หรือ 1H 30m
บรรทัด 722–725: arriveOf หาเวลาถึงของสถานที่จาก day.arrivals (ที่ backend คำนวณ) คืน -1 ถ้าไม่มี
บรรทัด 727–732: hoursText ข้อความเวลาเปิด-ปิด ดึงจาก STATE.pois ถ้า POI ในแผนไม่มี คืน "ไม่ระบุ" หรือ "ทั้งวัน"
บรรทัด 734–738: strHash แฮช FNV-1a ของข้อความ ใช้สร้างรีวิวจำลองที่ได้ผลเดิมทุกครั้ง
บรรทัด 740–760  รีวิวจำลอง
740  const MOCK_REVIEWS = {
741    beach: ['ทรายสะอาด น้ำใส เหมาะมาช่วงเช้าที่คนยังน้อย', 'วิวสวย มีร้านอาหารริมหาด แต่ช่วงบ่ายแดดแรง', 'เดินเล่นสบาย จอดรถง่าย บรรยากาศผ่อนคลาย'],
742    temple: ['สถาปัตยกรรมสวยงาม ควรแต่งกายสุภาพ', 'บรรยากาศสงบ เหมาะกับการมาช่วงเช้า', 'มีประวัติน่าสนใจ ใช้เวลาเดินชมไม่นาน'],
743    viewpoint: ['วิวกว้างมาก ถ่ายรูปสวยโดยเฉพาะช่วงเย็น', 'ทางขึ้นค่อนข้างชัน ควรใส่รองเท้าเดินสบาย', 'คุ้มกับการมา อากาศเย็นสบาย'],
744    culture: ['ให้ความรู้ดี เจ้าหน้าที่แนะนำเป็นกันเอง', 'จัดแสดงน่าสนใจ เหมาะกับครอบครัว', 'ค่าเข้าไม่แพง ใช้เวลาชมประมาณชั่วโมงกว่า'],
745    market: ['ของกินหลากหลาย ราคาไม่แพง', 'คนเยอะช่วงเย็น ควรมาก่อนหัวค่ำ', 'ของฝากน่าซื้อ บรรยากาศคึกคัก'],
746    activity: ['กิจกรรมสนุก เจ้าหน้าที่ดูแลดี', 'ควรจองล่วงหน้าช่วงวันหยุด', 'เหมาะกับกลุ่มเพื่อนและครอบครัว'],
747    hotel: ['ห้องพักสะอาด พนักงานบริการดี', 'ทำเลสะดวก เดินทางไปที่เที่ยวง่าย', 'อาหารเช้าหลากหลาย เตียงนอนสบาย', 'ราคาคุ้มค่า เหมาะกับการพักผ่อน', 'ห้องค่อนข้างเล็กแต่ครบครัน เช็คอินรวดเร็ว'],
748    restaurant: ['รสชาติดี ราคาเหมาะสม บริการรวดเร็ว', 'ร้านบรรยากาศดี ช่วงเที่ยงคนค่อนข้างเยอะ', 'เมนูแนะนำอร่อย ที่นั่งสบาย'],
749  };
750
751  function mockReviewsFor(poi) {   // สร้างจาก id ของสถานที่ ได้ผลเดิมทุกครั้ง; คะแนนอิงคะแนนของระบบ
752    const h = strHash(poi.id + poi.name_en);
753    const rating = Math.max(3.0, Math.min(5.0, poi.score / 2 + ((h % 7) - 3) * 0.05));
754    const pool = MOCK_REVIEWS[poi.category] || MOCK_REVIEWS.culture;
755    const picks = [0, 1, 2].map(i => ({
756      text: pool[(h + i) % pool.length],
757      stars: Math.max(3, Math.min(5, Math.round(rating + (((h >> (i + 3)) % 3) - 1) * 0.6))),
758    }));
759    return {rating, count: 40 + (h % 860), reviews: picks};
760  }
บรรทัด 740–749: MOCK_REVIEWS ประโยครีวิวตัวอย่างต่อหมวด (รวมโรงแรม hotel)
บรรทัด 751–760: mockReviewsFor สร้างคะแนน จำนวนรีวิว และรีวิวสามอัน จากแฮชของ id และชื่อสถานที่ (คะแนนอิงคะแนนของระบบ) ข้อมูลเหล่านี้เป็นตัวอย่างสำหรับสาธิต และหน้าเว็บมีป้าย "ข้อมูลจำลอง" กำกับ
บรรทัด 762–831  หน้าต่างรายละเอียดสถานที่และโรงแรม
762  function ensurePoiModal() {
763    let m = document.getElementById('poiModal');
764    if (!m) {
765      m = document.createElement('div');
766      m.className = 'modal';
767      m.id = 'poiModal';
768      m.innerHTML = `<div class="modal-backdrop" onclick="closePoiDetail()"></div>
769        <div class="modal-card"><div class="modal-head"><div><div class="modal-title" id="poiTitle"></div>
770        <div class="modal-sub" id="poiSub"></div></div>
771        <div class="modal-head-actions"><a class="icon-btn" id="poiMap" target="_blank" rel="noopener" title="ดูใน Google Maps">${ICON.pin}</a>
772        <button class="icon-btn" onclick="closePoiDetail()" title="ปิด"><svg class="ic "><use href="#i-close"/></svg></button></div></div>
773        <div class="modal-body" id="poiBody"></div></div>`;
774      document.body.appendChild(m);
775    }
776    return m;
777  }
778
779  function reviewBlock(r) {
780    const stars = n => '★'.repeat(n) + '☆'.repeat(5 - n);
781    return `<div class="rev-head"><span class="rev-score">${ic('star')} ${r.rating.toFixed(1)}</span>
782        <span class="rev-count">${r.count} รีวิว</span><span class="mock-chip">ข้อมูลจำลอง</span></div>
783      ${r.reviews.map(v => `<div class="rev-item"><div class="rev-stars">${stars(v.stars)}</div><div>${v.text}</div></div>`).join('')}
784      <p class="poi-note">รีวิวและจำนวนรีวิวเป็นข้อมูลตัวอย่างที่สร้างขึ้นเพื่อสาธิตฟีเจอร์ ไม่ใช่ความเห็นของนักท่องเที่ยวจริง (รีวิวจริงเป็นแนวทางต่อยอดผ่านบริการข้อมูลสถานที่)</p>`;
785  }
786
787  function showPoiDetail(poiId, arriveMin) {
788    const poi = STATE.pois.find(p => p.id === poiId);
789    if (!poi) return;
790    const m = ensurePoiModal();
791    document.getElementById('poiMap').href = gmapsUrl(poi);
792    document.getElementById('poiTitle').textContent = poi.name_th;
793    document.getElementById('poiSub').textContent = `${poi.name_en} · ${CAT_LABELS[poi.category] || poi.category}`;
794    document.getElementById('poiBody').innerHTML = `
795      <div class="poi-facts">
796        <div><span>เวลาเปิด-ปิด</span><b>${hoursText(poi)}</b></div>
797        ${arriveMin >= 0 ? `<div><span>เวลาถึงตามแผน</span><b>${fmtClock(arriveMin)}</b></div>` : ''}
798        <div><span>เวลาที่ใช้ ณ สถานที่</span><b>${poi.duration_min} นาที</b></div>
799        <div><span>ค่าใช้จ่าย</span><b>${poi.cost ? fmt(poi.cost) + ' ฿' : 'ฟรี'}</b></div>
800      </div>
801      <p class="poi-note">เวลาเปิด-ปิดมาจากข้อมูล OpenStreetMap หรือเป็นค่าประมาณตามประเภทสถานที่ ควรตรวจสอบกับสถานที่อีกครั้งก่อนเดินทาง</p>
802      ${reviewBlock(mockReviewsFor(poi))}`;
803    m.classList.add('open');
804    document.body.style.overflow = 'hidden';
805  }
806
807  // โรงแรม: ดาว/ราคาจากข้อมูลจริง ส่วนรีวิวเป็นข้อมูลจำลองเหมือนสถานที่ท่องเที่ยว (ติดป้ายกำกับ)
808  function showHotelDetail(hotelId) {
809    const h = (STATE.hotels || []).find(x => x.id === hotelId) || (STATE.selectedPkg && STATE.selectedPkg.hotel);
810    if (!h) return;
811    const m = ensurePoiModal();
812    const stars = Math.max(1, Math.min(5, Math.round(h.stars || 3)));
813    const r = mockReviewsFor({id: h.id, name_en: h.name_en, category: 'hotel', score: (h.score || 7)});
814    document.getElementById('poiMap').href = gmapsUrl({...h, name_th: h.name_en});
815    document.getElementById('poiTitle').textContent = h.name_th || h.name_en;
816    document.getElementById('poiSub').textContent = `${h.name_en} · โรงแรม`;
817    document.getElementById('poiBody').innerHTML = `
818      <div class="poi-facts">
819        <div><span>ระดับดาว</span><b>${'★'.repeat(stars)}${'☆'.repeat(5 - stars)}</b></div>
820        <div><span>ราคาต่อคืน</span><b>${fmt(h.cost)} ฿</b></div>
821      </div>
822      <p class="poi-note">ราคาต่อคืนเป็นค่าประมาณจากระดับดาวของโรงแรมใน OpenStreetMap ไม่ใช่ราคาจริง ควรตรวจสอบราคาและห้องว่างกับโรงแรมหรือเว็บจองห้องพักก่อนเดินทาง</p>
823      ${reviewBlock(r)}`;
824    m.classList.add('open');
825    document.body.style.overflow = 'hidden';
826  }
827
828  function closePoiDetail() {
829    document.getElementById('poiModal').classList.remove('open');
830    document.body.style.overflow = '';
831  }
บรรทัด 762–777: ensurePoiModal สร้างโครงโมดัลต่อท้าย body ครั้งแรก (หัวชื่อ ชื่อรอง กลุ่มปุ่มมุมขวาบนคือลิงก์หมุด Google Maps #poiMap และปุ่มปิด) แล้วคืนโมดัล ใช้ร่วมกันระหว่างหน้ารายละเอียดสถานที่และโรงแรม
บรรทัด 779–785: reviewBlock สร้าง HTML ส่วนคะแนนและรีวิวจำลอง พร้อมตัวช่วยดาว ป้าย "ข้อมูลจำลอง" และหมายเหตุว่าเป็นข้อมูลตัวอย่าง
บรรทัด 787–790: showPoiDetail หาสถานที่จากรหัส ถ้าไม่พบออก แล้วเตรียมโมดัลด้วย ensurePoiModal
บรรทัด 791–793: ตั้งลิงก์หมุดด้วย gmapsUrl และตั้งชื่อ ชื่ออังกฤษ และหมวด
บรรทัด 794–802: เติมเนื้อหา: ตารางข้อมูล (เวลาเปิด-ปิด เวลาถึง เวลาที่ใช้ ค่าใช้จ่าย) หมายเหตุว่ามาจาก OpenStreetMap และส่วนรีวิวจาก reviewBlock
บรรทัด 803–805: เปิดโมดัลและล็อกการเลื่อนหน้า
บรรทัด 807–826: showHotelDetail หาโรงแรมจากรหัส (หรือโรงแรมของแผนที่เลือก) แล้วแสดงชื่อ ระดับดาว ราคาต่อคืน (ค่าประมาณจากระดับดาว มีหมายเหตุกำกับ) และรีวิวจำลองที่สร้างจากแฮชของรหัสและชื่อโรงแรม พร้อมลิงก์หมุด Google Maps เปิดได้จากหมุดโรงแรมบนแผนที่และปุ่มหมุดข้างชื่อโรงแรมในการ์ดแพ็กเกจ
บรรทัด 828–831: closePoiDetail ปิดโมดัลและคืนการเลื่อน
บรรทัด 836–864  เปิดแผนทางเลือก (Pareto)
836  async function openPareto() {
837    const pkg = STATE.selectedPkg;
838    if (!pkg) return;
839    const t = showToast('กำลังหาทางเลือกที่ดีที่สุดในแต่ละด้าน...', 'loading', 20000);
840    try {
841      const res = await fetch(`${API_BASE}/api/pareto`, {
842        method: 'POST',
843        headers: {'Content-Type': 'application/json'},
844        body: JSON.stringify({
845          province: getProvince(), preferences: getPreferences(),
846          budget: +document.getElementById('budget').value, days: pkg.days.length,
847          travelers: +document.getElementById('travelers').value,
848          include_hotel: STATE.includeHotel !== false, seed: Math.floor(Math.random() * 1000000),
849        }),
850      });
851      if (!res.ok) throw new Error(`HTTP ${res.status}`);
852      const data = await res.json();
853      STATE.paretoPlans = data.packages;
854      renderParetoCards(data.packages);
855      t.remove();
856      (data.packages[0]?.notes || []).forEach(n => showToast(n, 'error', 6000));
857      if (!data.packages.length) { showToast('ไม่พบทางเลือกที่ผ่านข้อจำกัด ลองเพิ่มงบหรือลดความชอบ', 'error', 5000); return; }
858      document.getElementById('paretoModal').classList.add('open');
859      document.body.style.overflow = 'hidden';
860    } catch (e) {
861      t.remove();
862      showToast(`ผิดพลาด: ${e.message}`, 'error');
863    }
864  }
บรรทัด 836–838: openPareto (ผูกกับปุ่มใน ➜ frontend/index.html) ถ้าไม่มีแผนออก
บรรทัด 839: แจ้งว่ากำลังหาทางเลือก
บรรทัด 841–850: ส่ง POST ไป /api/pareto (➜ pareto() ใน backend/main.py) ด้วยจังหวัด ความชอบ งบ จำนวนวัน จำนวนคน ตัวเลือกโรงแรม และ seed สุ่ม ฝั่ง backend ใช้ ➜ algorithm/pareto.py หาแผนที่แลกกันระหว่างคะแนน ความหลากหลาย และระยะทาง
บรรทัด 851–855: ตรวจสถานะ เก็บแผนใน STATE.paretoPlans วาดการ์ด (➜ renderParetoCards() ใน frontend/app.js) และลบข้อความรอ
บรรทัด 856: แจ้งหมายเหตุของ backend ทุกข้อ
บรรทัด 857: ถ้าไม่มีแผนผ่านข้อจำกัด แจ้งให้เพิ่มงบหรือลดความชอบ แล้วออก
บรรทัด 858–859: เปิดโมดัลและล็อกการเลื่อน
บรรทัด 860–863: ถ้าผิดพลาดลบข้อความรอและแจ้ง
บรรทัด 867–916  วาดการ์ดแผนทางเลือก
867  function renderParetoCards(plans) {
868    const cur = STATE.selectedPkg, days = Math.max(cur.days.length, 1);
869    const km = p => p.objectives.distance_km, div = p => p.objectives.diversity, cost = p => p.objectives.cost, sc = p => p.objectives.score;
870    const best = (fn, dir) => plans.reduce((m, p, i) => (dir * fn(p) > dir * fn(plans[m]) ? i : m), 0);
871    const labels = {};   // index → [ป้าย, คำอธิบาย]
872    const put = (i, tag, why) => { (labels[i] ||= []).push([tag, why]); };
873    put(best(sc, 1), 'แนะนำ', 'ได้สถานที่น่าสนใจโดยรวมสูงสุด');
874    put(best(km, -1), 'ขับน้อยที่สุด', 'เดินทางสั้น เหนื่อยน้อย ประหยัดค่าเดินทาง');
875    put(best(div, 1), 'หลากหลายที่สุด', 'ได้เที่ยวหลายประเภทในแต่ละวัน');
876    put(best(cost, -1), 'ประหยัดที่สุด', 'ค่าใช้จ่ายรวมต่ำสุด');
877    const picks = Object.keys(labels).map(Number);
878    const rest = plans.map((_, i) => i).filter(i => !picks.includes(i));
879    const dots = d => { const n = Math.max(1, Math.min(5, Math.round(d))); return [1, 2, 3, 4, 5].map(k => `<i class="${k <= n ? 'on' : ''}"></i>`).join(''); };
880    const kmDay = p => km(p) / days;
881    const diff = (v, base, unit, lessGood) => { const d = v - base; if (Math.abs(d) < 0.5) return '<span class="pc-same">เท่าแผนปัจจุบัน</span>'; const good = lessGood ? d < 0 : d > 0; return `<span class="${good ? 'pc-good' : 'pc-bad'}">${d < 0 ? '−' : '+'}${Math.abs(d).toFixed(0)} ${unit}</span>`; };
882    const baseKm = cur.days.reduce((a, d) => a + d.distance_km, 0) / days;
883    const card = (i, extra) => {
884      const p = plans[i], tags = (labels[i] || []).map(x => x[0]), why = (labels[i] || [])[0]?.[1] || 'อีกทางเลือกที่สมดุลระหว่างระยะทาง ความหลากหลายและค่าใช้จ่าย';
885      const hi = p.days.flatMap(d => d.pois).filter(x => x.category !== 'restaurant').sort((a, b) => b.score - a.score).slice(0, 3).map(x => x.name_th);
886      return `<div class="pc ${tags.includes('แนะนำ') ? 'pc-main' : ''}">
887        <div class="pc-top"><div>${(tags.length ? tags : ['ทางเลือก']).map(t => `<span class="pc-tag">${t}</span>`).join('')}<span class="score-chip" style="margin-left:6px">★ ${sc(p)}</span></div></div>
888        <div class="pc-why">${why}</div>
889        <div class="pc-metrics">
890          <div><small>ขับเฉลี่ย/วัน</small><b>${kmDay(p).toFixed(0)} กม.</b>${diff(kmDay(p), baseKm, 'กม./วัน', true)}</div>
891          <div><small>ความหลากหลาย</small><b class="pc-dots">${dots(div(p))}</b></div>
892          <div><small>ค่าใช้จ่าย/คน</small><b>${fmt(cost(p))} ฿</b></div>
893        </div>
894        <div class="pc-hi">${hi.map(n => `<span>${n}</span>`).join('')}</div>
895        <button class="pareto-use" onclick="usePareto(${i})">ใช้แผนนี้</button></div>`;
896    };
897    const box = document.getElementById('paretoTable');
898    box.className = 'pc-wrap';
899    box.innerHTML = picks.sort((a, b) => a - b).map(i => card(i)).join('') +
900      (rest.length ? `<button class="pc-more" onclick="this.nextElementSibling.hidden=false;this.hidden=true">ดูแผนอื่นอีก ${rest.length} แบบ</button><div class="pc-wrap-in" hidden>${rest.map(i => card(i)).join('')}</div>` : '');
901  }
902
903  function closePareto() {
904    document.getElementById('paretoModal').classList.remove('open');
905    document.body.style.overflow = '';
906  }
907
908  function usePareto(i) {
909    STATE.selectedPkg = JSON.parse(JSON.stringify(STATE.paretoPlans[i]));
910    STATE.locked.clear(); STATE.excluded.clear();
911    closePareto();
912    drawOnMap(STATE.selectedPkg);
913    renderDetail(STATE.selectedPkg);
914    pushSession();
915    showToast(`ใช้แผนทางเลือกที่ ${i + 1}`, 'ok');
916  }
บรรทัด 867–870: renderParetoCards อ่านแผนปัจจุบันและจำนวนวัน ตัวดึงเป้าหมายแต่ละด้าน (ระยะทาง ความหลากหลาย ค่าใช้จ่าย คะแนน) และ best หาแผนที่ดีที่สุดในด้านหนึ่ง
บรรทัด 871–872: labels เก็บป้ายและเหตุผลของแต่ละแผน และ put เพิ่มป้าย
บรรทัด 873–876: ติดป้าย: แนะนำ (คะแนนสูงสุด) ขับน้อยที่สุด หลากหลายที่สุด และประหยัดที่สุด พร้อมคำอธิบาย
บรรทัด 877–878: แผนที่ได้ป้ายแสดงก่อน ที่เหลือพับไว้ใน "ดูแผนอื่น"
บรรทัด 879: dots สร้างจุดห้าดวงบอกระดับความหลากหลาย
บรรทัด 880–882: ระยะขับเฉลี่ยต่อวัน และ diff ตัวแสดงส่วนต่างจากแผนปัจจุบัน (เขียวเมื่อดีขึ้น) พร้อมระยะเฉลี่ยของแผนปัจจุบัน
บรรทัด 883–885: card สร้างการ์ดหนึ่งใบ: ป้าย คำอธิบาย และสถานที่เด่น 3 อันดับ (ไม่รวมร้านอาหาร)
บรรทัด 886–895: HTML ของการ์ด: ป้าย คะแนน ตัวชี้วัด (ขับเฉลี่ย ความหลากหลาย ค่าใช้จ่ายต่อคน) สถานที่เด่น และปุ่ม "ใช้แผนนี้" เรียก usePareto
บรรทัด 897–900: ใส่การ์ดที่ได้ป้ายก่อน แล้วปุ่ม "ดูแผนอื่นอีก N แบบ" ที่คลิกแล้วแสดงส่วนที่พับ
บรรทัด 903–906: closePareto ปิดโมดัลและคืนการเลื่อน (ผูกกับ ➜ frontend/index.html)
บรรทัด 908–916: usePareto ใช้แผนที่เลือก (สำเนาลึก) ล้างชุดล็อกและลบ วาดแผนที่และรายละเอียดใหม่ ส่งขึ้นเซสชัน และแจ้ง
บรรทัด 919–953  โหลดรายการจังหวัด
919  const REGION_ORDER = ['ภาคเหนือ', 'ภาคตะวันออกเฉียงเหนือ', 'ภาคกลาง', 'ภาคตะวันออก', 'ภาคตะวันตก', 'ภาคใต้'];
920
921  async function loadProvinces() {
922    try {
923      const res = await fetch(`${API_BASE}/api/provinces`);
924      if (!res.ok) throw new Error(`HTTP ${res.status}`);
925      const data = await res.json();
926      const list = document.getElementById('provList');
927      const active = getProvince();
928      list.innerHTML = '';
929      const regions = {};
930      data.provinces.forEach(pv => {
931        STATE.provinces[pv.slug] = pv;
932        (regions[pv.region || 'อื่น ๆ'] ||= []).push({...pv, ready: true});
933      });
934      data.planned.forEach(pv => (regions[pv.region] ||= []).push({...pv, ready: false}));
935      const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
936      [...REGION_ORDER, ...Object.keys(regions).filter(r => !REGION_ORDER.includes(r))].forEach(r => {
937        const items = (regions[r] || []).sort((a, b) => (b.ready - a.ready) || a.name_th.localeCompare(b.name_th, 'th'));
938        if (!items.length) return;
939        list.insertAdjacentHTML('beforeend', `<div class="prov-group-label">${esc(r)}</div>`);
940        items.forEach(pv => {
941          const el = document.createElement('div');
942          el.className = 'prov-item' + (pv.ready ? '' : ' prov-disabled') + (pv.ready && pv.slug === active ? ' prov-active' : '');
943          el.dataset.label = pv.name_th;
944          if (pv.ready) { el.dataset.value = pv.slug; el.onclick = () => selectProvince(el); }
945          el.innerHTML = `<span class="prov-item-name">${esc(pv.name_th)}</span>` +
946            (pv.ready ? (pv.sparse ? `<span class="prov-item-sparse" title="${pv.pois} สถานที่ ${pv.hotels} โรงแรม — ตัวเลือกอาจน้อย">ข้อมูลน้อย</span>` : '') + '<span class="prov-item-badge">พร้อมใช้งาน</span>' : '<span class="prov-item-soon">เร็วๆ นี้</span>');
947          list.appendChild(el);
948        });
949      });
950    } catch (e) {
951      showToast('โหลดรายการจังหวัดไม่สำเร็จ', 'error', 4000);
952    }
953  }
บรรทัด 919: REGION_ORDER ลำดับภาคที่แสดงในเมนู
บรรทัด 921–925: loadProvinces ขอ /api/provinces (➜ get_provinces() ใน backend/main.py) และอ่านผล
บรรทัด 926–928: ล้างรายการในเมนู (➜ frontend/index.html #provList) และจำจังหวัดที่เลือกอยู่
บรรทัด 929–934: จัดกลุ่มตามภาค: จังหวัดที่พร้อม (provinces) ลง STATE.provinces ส่วนจังหวัดที่ยังไม่มีข้อมูล (planned) แสดงแบบกดไม่ได้
บรรทัด 935: esc หลีกอักขระพิเศษ HTML
บรรทัด 936–939: ไล่ตามลำดับภาค เรียงจังหวัดที่พร้อมก่อน แล้วตามชื่อไทย และใส่ป้ายภาค
บรรทัด 940–948: สร้างรายการจังหวัด: คลาสตามสถานะ (พร้อม กดไม่ได้ กำลังเลือก) ผูกการคลิกกับ selectProvince ใน ➜ frontend/index.html และแสดงป้าย "ข้อมูลน้อย" ถ้าเป็นจังหวัด sparse (สถานะที่ ➜ data/build_all_provinces.py ตัดสินไว้)
บรรทัด 950–952: ถ้าผิดพลาดแจ้งผู้ใช้
บรรทัด 956–984  เปลี่ยนจังหวัดและโหลดสถานที่
956  async function onProvinceChange(slug) {
957    STATE.poisById = {};
958    STATE.packages = [];
959    STATE.selectedPkg = null;
960    STATE.selectedIdx = null;
961    ['packagesSection', 'detailPanel'].forEach(id => { document.getElementById(id).style.display = 'none'; });
962    const pv = STATE.provinces[slug];
963    if (pv && STATE.map) STATE.map.setView(pv.center, pv.zoom);
964    await loadPois();
965  }
966
967  async function loadPois() {
968    try {
969      setApiStatus('loading', 'connecting...');
970      const ctrl = new AbortController();
971      const timer = setTimeout(() => ctrl.abort(), 5000);
972      const res = await fetch(`${API_BASE}/api/pois?province=${encodeURIComponent(getProvince())}`, { signal: ctrl.signal });
973      clearTimeout(timer);
974      if (!res.ok) throw new Error(`HTTP ${res.status}`);
975      const data = await res.json();
976      STATE.pois = data.pois;
977      STATE.hotels = data.hotels;
978      [...data.pois, ...data.hotels].forEach(p => STATE.poisById[p.id] = p);
979      setApiStatus('ok', `${data.pois.length} สถานที่ · ${data.hotels.length} โรงแรม`);
980    } catch (e) {
981      setApiStatus('error', 'backend offline');
982      showToast(`โหลดข้อมูลไม่สำเร็จ — ตรวจสอบว่า backend รันที่ ${API_BASE}`, 'error', 6000);
983    }
984  }
บรรทัด 956–965: onProvinceChange ล้างตารางสถานที่ แพ็กเกจ และแผนที่เลือก (เพราะ id ของ POI ซ้ำกันข้ามจังหวัด) ซ่อนส่วนแพ็กเกจและรายละเอียด ย้ายแผนที่ไปจังหวัดใหม่ แล้วโหลดสถานที่ (ถูก ➜ frontend/extras.js ห่อเพื่อเปลี่ยนแบนเนอร์และปุ่มจังหวัดข้างเคียง)
บรรทัด 967–972: loadPois ตั้งสถานะ connecting ขอ /api/pois (➜ get_pois() ใน backend/main.py) พร้อมตัวตัดเวลา 5 วินาที
บรรทัด 973–979: ถ้าสำเร็จ เก็บสถานที่ โรงแรม และตารางค้นหาตาม id แล้วแสดงจำนวนในป้ายสถานะ
บรรทัด 980–983: ถ้าล้มเหลว ตั้งสถานะ offline และแจ้งให้ตรวจสอบว่า backend รันอยู่
บรรทัด 989–1003  แจ้งเตือน (toast)
989  function showToast(msg, kind = 'ok', duration = 3500) {
990    const container = document.getElementById('toastContainer');
991    const el = document.createElement('div');
992    el.className = `toast ${kind}`;
993    const iconMap = {ok: ICON.check, error: ICON.alert, loading: ICON.spin};
994    el.innerHTML = `<span class="toast-icon">${iconMap[kind] || ICON.check}</span><span>${msg}</span>`;
995    container.appendChild(el);
996    setTimeout(() => {
997      el.style.opacity = '0';
998      el.style.transform = 'translateX(20px)';
999      el.style.transition = 'all 200ms';
1000      setTimeout(() => el.remove(), 220);
1001    }, duration);
1002    return el;
1003  }
บรรทัด 989–994: showToast สร้างกล่องแจ้งเตือนตามชนิด (ok error loading) ใส่ไอคอนและข้อความ แล้วต่อเข้าถาด #toastContainer ใน ➜ frontend/index.html (ถูก ➜ frontend/extras.js ห่อเพื่อบันทึกประวัติ)
บรรทัด 996–1001: หลังครบเวลา ค่อยเฟดและเลื่อนออกแล้วลบ
บรรทัด 1002: คืนองค์ประกอบ ให้ผู้เรียกลบเองได้ (ข้อความ loading)
บรรทัด 1009–1037  ตรวจข้อมูลที่กรอก
1009  const VALIDATION = {
1010    budget: { min: 1000,  max: 100000, label: 'งบประมาณ' },
1011    days:   { min: 1,     max: 7,      label: 'จำนวนวัน' },
1012    travelers: { min: 1,  max: 10,     label: 'จำนวนคน' },
1013  };
1014
1015  function validateInputs(budget, days, travelers) {
1016    const errors = [];
1017    if (!Number.isFinite(budget) || budget < VALIDATION.budget.min) {
1018      errors.push(`${VALIDATION.budget.label}ต้องอย่างน้อย ${fmt(VALIDATION.budget.min)} บาท (ใส่ไว้ ${fmt(budget || 0)} บาท)`);
1019    }
1020    if (budget > VALIDATION.budget.max) {
1021      errors.push(`${VALIDATION.budget.label}สูงสุด ${fmt(VALIDATION.budget.max)} บาท`);
1022    }
1023    if (days < VALIDATION.days.min || days > VALIDATION.days.max) {
1024      errors.push(`${VALIDATION.days.label}ต้องอยู่ระหว่าง ${VALIDATION.days.min}-${VALIDATION.days.max} วัน (ตอนนี้ ${days})`);
1025    }
1026    if (travelers < VALIDATION.travelers.min || travelers > VALIDATION.travelers.max) {
1027      errors.push(`${VALIDATION.travelers.label}ต้อง ${VALIDATION.travelers.min}-${VALIDATION.travelers.max} คน`);
1028    }
1029    return errors;
1030  }
1031
1032  function highlightField(id, hasError) {
1033    const wrapper = document.getElementById(id)?.closest('.input-with-unit, .date-range-input, .counter-control, .select-input');
1034    if (wrapper) wrapper.classList.toggle('has-error', hasError);
1035    const input = document.getElementById(id);
1036    if (input) input.classList.toggle('has-error', hasError);
1037  }
บรรทัด 1009–1013: VALIDATION กฎตรวจฝั่งหน้าเว็บ (งบ 1,000–100,000 จำนวนวัน 1–7 จำนวนคน 1–10) ซึ่งต้องตรงกับ schema Pydantic ของ ➜ create_packages() ใน backend/main.py
บรรทัด 1015–1030: validateInputs ตรวจงบ จำนวนวัน และจำนวนคน คืนรายการข้อความผิดพลาด (ถูก ➜ frontend/extras.js ห่อเพิ่มกฎจำนวนวันสูงสุดของจังหวัด)
บรรทัด 1032–1037: highlightField ใส่หรือเอาคลาส has-error ที่ช่องกรอกและกรอบของมัน
บรรทัด 1039–1053  เริ่มค้นหา
1039  async function searchPackages() {
1040    const budget = +document.getElementById('budget').value;
1041    const days = getSelectedDays();
1042    const travelers = +document.getElementById('travelers').value;
1043    // One Day Trip → บังคับไม่รวมโรงแรม
1044    const includeHotel = days === 1 ? false : (document.getElementById('includeHotel')?.checked !== false);
1045
1046    // === Client-side validation FIRST ===
1047    const errors = validateInputs(budget, days, travelers);
1048    highlightField('budget', errors.some(e => e.includes('งบประมาณ')));
1049    highlightField('dateRange', errors.some(e => e.includes('จำนวนวัน')));
1050    if (errors.length > 0) {
1051      showToast(errors[0], 'error', 5000);
1052      return;
1053    }
บรรทัด 1039–1042: searchPackages (ผูกกับปุ่มค้นหาใน ➜ frontend/index.html) อ่านงบ จำนวนวัน และจำนวนคน
บรรทัด 1043–1044: ทริปวันเดียวบังคับไม่รวมโรงแรม ไม่เช่นนั้นอ่านจากช่องติ๊ก
บรรทัด 1046–1049: ตรวจข้อมูลก่อน และไฮไลต์ช่องที่ผิด
บรรทัด 1050–1053: ถ้ามีข้อผิดพลาด แจ้งข้อแรกและหยุด
บรรทัด 1055–1085  เตรียมหน้าจอรอผล
1055    // === Clear previous results ===
1056    if (STATE.map) {
1057      STATE.mapMarkers.forEach(m => STATE.map.removeLayer(m));
1058      STATE.mapPolylines.forEach(p => STATE.map.removeLayer(p));
1059      if (STATE.hotelMarker) STATE.map.removeLayer(STATE.hotelMarker);
1060      STATE.mapMarkers = [];
1061      STATE.mapPolylines = [];
1062      STATE.mapDayLayers = {};
1063      STATE.hotelMarker = null;
1064    }
1065    STATE.packages = [];
1066    STATE.selectedPkg = null;
1067    STATE.selectedIdx = null;
1068    document.getElementById('detailPanel').style.display = 'none';
1069    document.getElementById('dayToggles').innerHTML = '';
1070    document.getElementById('dayPanels').innerHTML = '';
1071
1072    const btn = document.getElementById('searchBtn');
1073    btn.classList.add('loading');
1074    btn.disabled = true;
1075
1076    const sec = document.getElementById('packagesSection');
1077    sec.style.display = 'block';
1078    document.getElementById('metaSummary').textContent = STATE.dev ? `กำลังคำนวณด้วย ${ALGO_NAMES[SELECTED_ALGO]}...` : 'กำลังวางแผนทริป...';
1079    const grid = document.getElementById('packagesRow');
1080    grid.innerHTML = '';
1081    const skTpl = document.getElementById('skeletonTemplate');
1082    for (let i = 0; i < 3; i++) grid.appendChild(skTpl.content.cloneNode(true));
1083    sec.scrollIntoView({behavior: 'smooth', block: 'start'});
1084
1085    const loadingToast = showToast(STATE.dev ? `กำลังเรียก ${ALGO_NAMES[SELECTED_ALGO]} 3 รอบ...` : 'กำลังวางแผนทริป 3 แบบ...', 'loading', 30000);
บรรทัด 1055–1064: ล้างหมุดและเส้นบนแผนที่และตารางต่อวัน (ผลก่อนหน้า)
บรรทัด 1065–1070: ล้างแพ็กเกจ แผนที่เลือก ซ่อนรายละเอียด และล้างตัวสลับวัน/รายการวัน
บรรทัด 1072–1074: ทำให้ปุ่มค้นหาเป็นสถานะกำลังโหลดและกดไม่ได้
บรรทัด 1076–1083: แสดงส่วนแพ็กเกจ ตั้งข้อความสถานะ (โหมด Developer บอกชื่ออัลกอริทึม) ใส่โครงรอโหลด 3 ใบจาก <template> และเลื่อนหน้าลงไป
บรรทัด 1085: แสดงข้อความ loading
บรรทัด 1087–1108  ส่งคำขอสร้างแพ็กเกจ
1087    try {
1088      const res = await fetch(`${API_BASE}/api/packages`, {
1089        method: 'POST',
1090        headers: devHeaders(),
1091        body: JSON.stringify({province: getProvince(), preferences: getPreferences(), budget, days, travelers, seed: Math.floor(Math.random() * 100000), algorithm: STATE.dev ? SELECTED_ALGO : 'hybrid', include_hotel: includeHotel}),
1092      });
1093      if (!res.ok) {
1094        // Parse FastAPI/Pydantic 422 detail
1095        let detail = `HTTP ${res.status}`;
1096        try {
1097          const errData = await res.json();
1098          if (errData.detail && Array.isArray(errData.detail)) {
1099            detail = errData.detail.map(d => {
1100              const field = d.loc ? d.loc[d.loc.length - 1] : '?';
1101              return `${field}: ${d.msg}`;
1102            }).join(' · ');
1103          } else if (errData.detail) {
1104            detail = errData.detail;
1105          }
1106        } catch {}
1107        throw new Error(detail);
1108      }
บรรทัด 1087–1092: ส่ง POST ไป /api/packages (➜ create_packages() ใน backend/main.py) พร้อมจังหวัด ความชอบ งบ วัน คน seed สุ่ม อัลกอริทึม (โหมดปกติบังคับ Hybrid) และตัวเลือกโรงแรม ส่วนหัวมีโทเค็นนักพัฒนา (➜ devHeaders() ใน frontend/app.js) backend จะเรียก ➜ algorithm/hybrid.py (หรืออัลกอริทึมที่เลือกในโหมด Developer)
บรรทัด 1093–1108: ถ้าตอบผิดพลาด อ่านรายละเอียดตามรูปแบบ 422 ของ FastAPI (รายการ field: ข้อความ) หรือข้อความเดี่ยว แล้วโยนข้อผิดพลาด
บรรทัด 1109–1128  ใช้ผลที่ได้
1109      const data = await res.json();
1110      STATE.packages = data.packages;
1111      STATE.includeHotel = includeHotel && !data.packages.every(p => !p.total_hotel_cost);   // งบไม่พอที่พัก: เซิร์ฟเวอร์สร้างแบบไม่รวมโรงแรมให้
1112      (data.packages[0]?.notes || []).forEach(n => showToast(n, 'error', 7000));   // เช่น ร้านอาหารตามความชอบมีไม่พอ
1113      renderPackages();
1114      const totalRuntime = data.packages.reduce((s, p) => s + p.runtime_ms, 0);
1115      document.getElementById('metaSummary').textContent =
1116        `งบ ${fmt(budget)} ฿ · ${days} วัน · ${travelers} คน` + (STATE.dev ? ` · ${ALGO_NAMES[SELECTED_ALGO]} · ${(totalRuntime/1000).toFixed(1)} วินาที` : '');
1117      loadingToast.remove();
1118      showToast(`สร้าง ${data.packages.length} แพ็กเกจสำเร็จ`, 'ok');
1119    } catch (e) {
1120      loadingToast.remove();
1121      showToast(`ผิดพลาด: ${e.message}`, 'error', 6000);
1122      grid.innerHTML = '';
1123      document.getElementById('metaSummary').textContent = '';
1124    } finally {
1125      btn.classList.remove('loading');
1126      btn.disabled = false;
1127    }
1128  }
บรรทัด 1109–1110: เก็บแพ็กเกจที่ได้
บรรทัด 1111: ตั้งธงรวมโรงแรม: ถ้าทุกแพ็กเกจไม่มีค่าโรงแรม แปลว่างบไม่พอและเซิร์ฟเวอร์สร้างแบบไม่รวมโรงแรม
บรรทัด 1112: แสดงหมายเหตุของ backend (เช่น ร้านอาหารตามความชอบไม่พอ)
บรรทัด 1113–1118: วาดการ์ด (➜ renderPackages() ใน frontend/app.js) สรุปเงื่อนไข (และเวลาในโหมด Developer) ลบข้อความ loading และแจ้งสำเร็จ
บรรทัด 1119–1123: ถ้าผิดพลาดแจ้งข้อความ ล้างการ์ด
บรรทัด 1124–1127: คืนปุ่มค้นหาให้กดได้เสมอ
บรรทัด 1133–1167  แสดงการ์ดแพ็กเกจ
1133  function renderPackages() {
1134    const grid = document.getElementById('packagesRow');
1135    grid.innerHTML = '';
1136
1137    const showHotel = STATE.includeHotel !== false;
1138
1139    STATE.packages.forEach((pkg, idx) => {
1140      const card = document.createElement('div');
1141      card.className = `package-card ${pkg.valid ? '' : 'invalid'}`;
1142      card.onclick = () => pkg.valid && selectPackage(idx);
1143      const totalPois = pkg.days.reduce((s, d) => s + d.pois.length, 0);
1144      card.innerHTML = `
1145        <div class="tier-row">
1146          <span class="tier-badge tier-${pkg.tier}">${pkg.tier}</span>
1147          <span class="runtime">${pkg.runtime_ms.toFixed(0)} ms</span>
1148        </div>
1149        ${showHotel
1150          ? `<div class="hotel-name">${CAT_ICON.hotel} ${pkg.hotel.name_en}
1151              <button type="button" class="hotel-info-btn" title="ดูรายละเอียดและรีวิว" onclick="event.stopPropagation(); showHotelDetail('${pkg.hotel.id}')">${ICON.pin}</button></div>`
1152          : `<div class="hotel-name no-hotel">${ic('hotel-off')} ไม่รวมที่พัก</div>`}
1153        ${pkg.valid ? `
1154          <div class="score-display">
1155            <span class="score-num">${pkg.total_score}</span>
1156            <span class="score-label"><span class="dev-txt">รวมคะแนน · </span>${totalPois} จุดท่องเที่ยว</span>
1157          </div>
1158          ${showHotel ? `<div class="stat-row"><span class="label">ค่าโรงแรม</span><span class="val">${fmt(pkg.total_hotel_cost)} ฿</span></div>` : ''}
1159          <div class="stat-row"><span class="label">ค่ากิจกรรม</span><span class="val">${fmt(pkg.total_activity_cost)} ฿</span></div>
1160          <div class="stat-row total"><span class="label">รวมทั้งหมด</span><span class="val">${fmt(pkg.total_cost)} ฿</span></div>
1161        ` : `
1162          <div class="invalid-msg">${pkg.violations[0] || 'งบไม่พอสำหรับแพ็กเกจนี้'}</div>
1163        `}
1164      `;
1165      grid.appendChild(card);
1166    });
1167  }
บรรทัด 1133–1137: renderPackages ล้างตาราง และอ่านว่าจะแสดงข้อมูลโรงแรมหรือไม่
บรรทัด 1139–1143: แต่ละแพ็กเกจสร้างการ์ด (ถ้าไม่ผ่านข้อจำกัดเป็นสีเทา) คลิกแล้วเรียก selectPackage เมื่อแพ็กเกจผ่านข้อจำกัด และนับจำนวนสถานที่
บรรทัด 1144–1152: หัวการ์ด: ระดับ (ประหยัด มาตรฐาน พรีเมียม) เวลาคำนวณ และชื่อโรงแรมพร้อมปุ่มหมุดเล็ก (.hotel-info-btn) ที่เปิด showHotelDetail โดยไม่เลือกแพ็กเกจ (stopPropagation) หรือ "ไม่รวมที่พัก"
บรรทัด 1153–1160: ถ้าผ่านข้อจำกัด แสดงคะแนน จำนวนจุดท่องเที่ยว ค่าโรงแรม ค่ากิจกรรม และรวมทั้งหมด
บรรทัด 1161–1163: ถ้าไม่ผ่าน แสดงข้อความละเมิดข้อแรก หรือ "งบไม่พอสำหรับแพ็กเกจนี้"
บรรทัด 1165–1166: ต่อการ์ดเข้าตาราง
บรรทัด 1172–1189  เลือกแพ็กเกจ
1172  function selectPackage(idx) {
1173    STATE.selectedPkg = JSON.parse(JSON.stringify(STATE.packages[idx]));
1174    STATE.locked.clear(); STATE.excluded.clear();
1175    STATE.selectedIdx = idx;
1176    document.querySelectorAll('.package-card').forEach((c, i) =>
1177      c.classList.toggle('selected', i === idx)
1178    );
1179    document.getElementById('detailPanel').style.display = 'block';
1180    renderDetail(STATE.selectedPkg);
1181    // CRITICAL: must invalidate size after detail panel becomes visible,
1182    // otherwise map container has 0px and fitBounds fails
1183    setTimeout(() => {
1184      STATE.map.invalidateSize();
1185      drawOnMap(STATE.selectedPkg);
1186      document.getElementById('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
1187      setTimeout(syncMapHeight, 150);
1188    }, 120);
1189  }
บรรทัด 1172–1175: selectPackage ทำสำเนาลึกของแพ็กเกจที่เลือก ล้างชุดล็อกและลบ และจดตำแหน่ง
บรรทัด 1176–1178: ไฮไลต์การ์ดที่เลือก
บรรทัด 1179–1180: แสดงส่วนรายละเอียดและวาดด้วย ➜ renderDetail() ใน frontend/app.js
บรรทัด 1181–1188: ต้องคำนวณขนาดแผนที่ใหม่หลังที่แสดงส่วนรายละเอียด (ไม่เช่นนั้นแผนที่สูง 0 พิกเซลและ fitBounds ล้มเหลว) แล้ววาดเส้นทาง เลื่อนหน้า และปรับความสูงแผนที่
บรรทัด 1194–1284  วาดแผนที่
1194  function drawOnMap(pkg) {
1195    // Clear all old layers
1196    STATE.mapMarkers.forEach(m => STATE.map.removeLayer(m));
1197    STATE.mapPolylines.forEach(p => STATE.map.removeLayer(p));
1198    if (STATE.hotelMarker) STATE.map.removeLayer(STATE.hotelMarker);
1199    STATE.mapMarkers = [];
1200    STATE.mapPolylines = [];
1201    STATE.mapDayLayers = {};
1202
1203    const showHotel = STATE.includeHotel !== false;
1204
1205    // Hotel marker — แสดงเฉพาะเมื่อรวมโรงแรม
1206    if (showHotel) {
1207      const hotelIcon = L.divIcon({
1208        html: `<div class="map-hotel-marker">${ic('hotel')}</div>`,
1209        className: '',
1210        iconSize: [40, 40], iconAnchor: [20, 20],
1211      });
1212      STATE.hotelMarker = L.marker([pkg.hotel.lat, pkg.hotel.lng], {icon: hotelIcon})
1213        .bindPopup(`<b>${pkg.hotel.name_en}</b><br><small>${pkg.hotel.cost} ฿/คืน</small><br>
1214           <a href="#" onclick="showHotelDetail('${pkg.hotel.id}'); return false;">ดูรายละเอียดและรีวิว</a>`)
1215        .addTo(STATE.map);
1216    } else {
1217      STATE.hotelMarker = null;
1218    }
1219
1220    // allLatLngs: รวม hotel ไว้ใน bounds เฉพาะเมื่อรวมโรงแรม
1221    const allLatLngs = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];
1222
1223    pkg.days.forEach((day, dIdx) => {
1224      const color = DAY_COLORS[dIdx % DAY_COLORS.length];
1225      // path: เริ่ม/จบที่โรงแรมเฉพาะเมื่อรวมโรงแรม
1226      const path = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];
1227      const dayMarkers = [];
1228
1229      day.pois.forEach((poi, pIdx) => {
1230        const icon = L.divIcon({
1231          html: `<div class="map-poi-marker" style="--c:${color};">
1232                   <span class="d">${dIdx + 1}</span>
1233                   <span class="p">${pIdx + 1}</span>
1234                 </div>`,
1235          className: '',
1236          iconSize: [36, 36], iconAnchor: [18, 18],
1237        });
1238        const m = L.marker([poi.lat, poi.lng], {icon}).bindPopup(
1239          `<b>${poi.name_th}</b><br>
1240           <small>${poi.name_en}</small><br>
1241           <span style="opacity:0.7;">วันที่ ${dIdx + 1} · ลำดับ ${pIdx + 1}</span><br>
1242           ${STATE.dev ? poi.score + ' คะแนน · ' : ''}${poi.cost} ฿ · ${poi.duration_min} นาที<br>
1243           <a href="#" onclick="showPoiDetail('${poi.id}', ${arriveOf(day, poi)}); return false;">ดูรายละเอียดและรีวิว</a>`
1244        ).addTo(STATE.map);
1245        dayMarkers.push(m);
1246        STATE.mapMarkers.push(m);
1247        path.push([poi.lat, poi.lng]);
1248        allLatLngs.push([poi.lat, poi.lng]);
1249      });
1250
1251      if (showHotel) path.push([pkg.hotel.lat, pkg.hotel.lng]);
1252      const line = L.polyline(path, {
1253        color, weight: 3, opacity: 0.8, dashArray: '6, 8',
1254      }).bindTooltip(`Day ${dIdx + 1}`).addTo(STATE.map);
1255      STATE.mapPolylines.push(line);
1256
1257      // Save layers for this day
1258      STATE.mapDayLayers[dIdx] = {
1259        markers: dayMarkers,
1260        polyline: line,
1261        visible: true,
1262        color,
1263      };
1264    });
1265
1266    // Default: show only day 1, hide the rest
1267    pkg.days.forEach((_, dIdx) => {
1268      if (dIdx === 0) return;
1269      const layer = STATE.mapDayLayers[dIdx];
1270      if (!layer) return;
1271      layer.markers.forEach(m => STATE.map.removeLayer(m));
1272      STATE.map.removeLayer(layer.polyline);
1273      layer.visible = false;
1274    });
1275
1276    renderDayToggles(pkg);
1277
1278    // fitBounds to day 1 only
1279    const day0Latlngs = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];
1280    pkg.days[0].pois.forEach(p => day0Latlngs.push([p.lat, p.lng]));
1281    if (day0Latlngs.length > 1) {
1282      STATE.map.fitBounds(L.latLngBounds(day0Latlngs).pad(0.15));
1283    }
1284  }
บรรทัด 1194–1201: drawOnMap ล้างหมุด เส้น และหมุดโรงแรมเดิม และตารางชั้นต่อวัน (ถูก ➜ frontend/extras.js ห่อให้คงสถานะวันที่เปิดอยู่)
บรรทัด 1203–1218: ถ้ารวมโรงแรม สร้างหมุดโรงแรมรูปเตียงพร้อมป๊อปอัปชื่อ ราคาต่อคืน และลิงก์ "ดูรายละเอียดและรีวิว" (เรียก showHotelDetail) ไม่เช่นนั้นไม่มีหมุด
บรรทัด 1221: เตรียมรายการพิกัดสำหรับจัดมุมมอง (รวมโรงแรมเฉพาะเมื่อรวมโรงแรม)
บรรทัด 1223–1227: แต่ละวัน เลือกสีประจำวัน และเริ่มเส้นทางที่โรงแรม (ถ้ารวมโรงแรม)
บรรทัด 1229–1237: แต่ละสถานที่ สร้างหมุดวงกลมสีของวัน แสดงเลขวันและลำดับ
บรรทัด 1238–1244: ผูกป๊อปอัปแสดงชื่อ ชื่ออังกฤษ วันและลำดับ (โหมด Developer แสดงคะแนนด้วย) ค่าใช้จ่ายและเวลา และลิงก์ไป ➜ showPoiDetail() ใน frontend/app.js
บรรทัด 1245–1248: จดหมุด จุดบนเส้นทาง และพิกัดทั้งหมด
บรรทัด 1251–1255: ปิดเส้นทางกลับโรงแรม แล้ววาดเส้นประสีของวัน
บรรทัด 1257–1263: เก็บชั้นของวันนั้นไว้ใน STATE.mapDayLayers (หมุด เส้น สถานะมองเห็น สี)
บรรทัด 1266–1274: ค่าตั้งต้นแสดงเฉพาะวันที่ 1 ซ่อนวันอื่นโดยถอดจากแผนที่
บรรทัด 1276: วาดปุ่มสลับวัน
บรรทัด 1278–1283: จัดมุมมองให้พอดีกับจุดของวันที่ 1 เว้นขอบ 15%
บรรทัด 1289–1342  ปุ่มสลับแต่ละวัน
1289  function renderDayToggles(pkg) {
1290    const root = document.getElementById('dayToggles');
1291    if (!root) return;
1292
1293    let html = `<button class="day-toggle show-all" onclick="toggleAllDays(true)" title="แสดงทุกวัน">
1294                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
1295                  <span>แสดงทุกวัน</span>
1296                </button>`;
1297    html += `<button class="day-toggle hide-all" onclick="toggleAllDays(false)" title="ซ่อนทุกวัน">
1298               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
1299               <span>ซ่อนทุกวัน</span>
1300             </button>`;
1301    html += `<button class="day-toggle reset-view" onclick="resetMapView()" title="รีเซ็ตตำแหน่ง">
1302               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
1303               <span>รีเซ็ต</span>
1304             </button>`;
1305    html += pkg.days.map((day, dIdx) => {
1306      const color = DAY_COLORS[dIdx % DAY_COLORS.length];
1307      const visible = STATE.mapDayLayers[dIdx] ? STATE.mapDayLayers[dIdx].visible : true;
1308      return `<button class="day-toggle ${visible ? 'active' : ''}"
1309                      style="--c:${color};"
1310                      onclick="toggleDay(${dIdx})">
1311                <span class="day-dot"></span>
1312                <span>วัน ${dIdx + 1} (${day.pois.length})</span>
1313              </button>`;
1314    }).join('');
1315    root.innerHTML = html;
1316  }
1317
1318  function toggleDay(dIdx) {
1319    const layer = STATE.mapDayLayers[dIdx];
1320    if (!layer) return;
1321    layer.visible = !layer.visible;
1322    if (layer.visible) {
1323      layer.markers.forEach(m => m.addTo(STATE.map));
1324      layer.polyline.addTo(STATE.map);
1325    } else {
1326      layer.markers.forEach(m => STATE.map.removeLayer(m));
1327      STATE.map.removeLayer(layer.polyline);
1328    }
1329    renderDayToggles(STATE.selectedPkg);
1330  }
1331
1332  function resetMapView() {
1333    const latlngs = [];
1334    Object.values(STATE.mapDayLayers).forEach(layer => {
1335      if (!layer.visible) return;
1336      layer.markers.forEach(m => latlngs.push(m.getLatLng()));
1337    });
1338    if (STATE.hotelMarker) latlngs.push(STATE.hotelMarker.getLatLng());
1339    if (latlngs.length > 1) {
1340      STATE.map.fitBounds(L.latLngBounds(latlngs).pad(0.15));
1341    }
1342  }
บรรทัด 1289–1291: renderDayToggles หาที่วางปุ่ม #dayToggles ใน ➜ frontend/index.html
บรรทัด 1293–1304: สร้างปุ่ม "แสดงทุกวัน" "ซ่อนทุกวัน" และ "รีเซ็ต"
บรรทัด 1305–1315: สร้างปุ่มของแต่ละวัน (สีและจำนวนจุด) ตามสถานะมองเห็น แล้วใส่ใน DOM
บรรทัด 1318–1330: toggleDay สลับการมองเห็นของวันหนึ่ง (เพิ่มหรือถอดหมุดและเส้นจากแผนที่) แล้ววาดปุ่มใหม่
บรรทัด 1332–1342: resetMapView รวมพิกัดหมุดของวันที่มองเห็นและโรงแรม แล้วปรับมุมมองให้พอดี
บรรทัด 1344–1358  แสดงหรือซ่อนทุกวัน
1344  function toggleAllDays(showAll) {
1345    Object.keys(STATE.mapDayLayers).forEach(k => {
1346      const layer = STATE.mapDayLayers[k];
1347      if (showAll && !layer.visible) {
1348        layer.markers.forEach(m => m.addTo(STATE.map));
1349        layer.polyline.addTo(STATE.map);
1350        layer.visible = true;
1351      } else if (!showAll && layer.visible) {
1352        layer.markers.forEach(m => STATE.map.removeLayer(m));
1353        STATE.map.removeLayer(layer.polyline);
1354        layer.visible = false;
1355      }
1356    });
1357    renderDayToggles(STATE.selectedPkg);
1358  }
บรรทัด 1344–1358: toggleAllDays แสดงหรือซ่อนทุกวันพร้อมกัน เฉพาะวันที่สถานะต่างจากเป้าหมาย แล้ววาดปุ่มใหม่
บรรทัด 1364–1395  จัดขนาดส่วนรายละเอียดให้พอดีจอ
1364  function fitDetail() {
1365    const sec = document.querySelector('.detail-section'), dayList = document.querySelector('.day-list'), grid = document.querySelector('.detail-grid');
1366    if (!sec || !dayList || !grid || sec.offsetParent === null) return;
1367    if (window.innerWidth <= 1000) { sec.style.minHeight = ''; dayList.style.maxHeight = ''; return; }
1368    const GAP = 36;   // ที่ว่างใต้กรอบ ไม่ให้ติดขอบล่างของเบราว์เซอร์
1369    const top = grid.getBoundingClientRect().top - sec.getBoundingClientRect().top;
1370    sec.style.minHeight = window.innerHeight + 'px';
1371    dayList.style.maxHeight = Math.max(360, window.innerHeight - top - GAP) + 'px';
1372    // ย่อการ์ดเท่าที่จำเป็น (ไม่ขยายเกินขนาดปกติ) ให้เห็นครบทุกจุดของวันที่ยาวที่สุดรวมปุ่มเพิ่มสถานที่โดยไม่ต้องเลื่อน
1373    // ลำดับ: บีบระยะห่าง --sp (1→0) ก่อน ถ้ายังไม่พอจึงลดตัวอักษร --fs (1→0.8)
1374    dayList.classList.add('fit');
1375    const need = () => Math.max(...[...dayList.querySelectorAll('.day-panel')].map(p => p.offsetHeight), 0);
1376    const room = dayList.clientHeight, setD = (sp, fs) => { dayList.style.setProperty('--sp', sp); dayList.style.setProperty('--fs', fs); };
1377    const MAXSP = 1.25;   // ที่ว่างที่เหลือ (เช่น จากกล่องฝนที่เล็กลง) ให้การ์ดขยายได้ถึง 1.25 เท่า ตัวอักษรโตสูงสุด 3%
1378    const tryD = (sp, fs = sp > 1 ? 1 + 0.03 * (sp - 1) / (MAXSP - 1) : 1) => { setD(sp.toFixed(3), fs.toFixed(3)); return need() <= room; };
1379    if (!tryD(MAXSP)) {
1380      if (tryD(0)) { let lo = 0, hi = MAXSP; for (let i = 0; i < 8; i++) { const m = (lo + hi) / 2; if (tryD(m)) lo = m; else hi = m; } tryD(lo); }
1381      else { let fs = 1; while (fs > 0.8 && need() > room) { fs -= 0.03; setD(0, fs.toFixed(3)); } }
1382    }
1383  }
1384  window.addEventListener('resize', () => { fitDetail(); syncMapHeight(); });
1385
1386  function syncMapHeight() {
1387    fitDetail();
1388    const dayList = document.querySelector('.day-list');
1389    const mapEl   = document.getElementById('map');
1390    if (!dayList || !mapEl) return;
1391    const listBottom = dayList.getBoundingClientRect().bottom;
1392    const mapTop     = mapEl.getBoundingClientRect().top;
1393    const mapH       = Math.max(listBottom - mapTop, 200);
1394    mapEl.style.height = mapH + 'px';
1395  }
บรรทัด 1364–1366: fitDetail หาองค์ประกอบ ถ้าไม่มีหรือซ่อนอยู่ออก
บรรทัด 1367: บนจอแคบ (ไม่เกิน 1000 พิกเซล) ล้างค่าบังคับความสูงแล้วออก
บรรทัด 1368–1371: คำนวณที่ว่างใต้กรอบ ตั้งความสูงขั้นต่ำเท่าจอ และจำกัดความสูงรายการวัน (ไม่ต่ำกว่า 360)
บรรทัด 1372–1382: ย่อการ์ดเท่าที่จำเป็นให้เห็นครบทุกจุดของวันที่ยาวที่สุด: ตัวแปร CSS --sp (ระยะห่าง 1.25 → 0) ก่อน ถ้ายังไม่พอจึงลด --fs (ขนาดอักษร 1 → 0.8) โดยค้นหาแบบแบ่งครึ่ง 8 รอบ
บรรทัด 1384: เมื่อปรับขนาดหน้าต่าง จัดขนาดและความสูงแผนที่ใหม่
บรรทัด 1386–1395: syncMapHeight จัดรายการวันก่อน แล้วตั้งความสูงแผนที่ให้เท่ารายการวัน (ไม่ต่ำกว่า 200 พิกเซล)
บรรทัด 1398–1492  วาดรายละเอียดแผน
1398  function renderDetail(pkg) {
1399    const showHotel = STATE.includeHotel !== false;
1400    document.getElementById('detailTitle').textContent = showHotel
1401      ? `${pkg.tier} — ${pkg.hotel.name_en}`
1402      : `${pkg.tier} — ไม่รวมที่พัก`;
1403
1404    // KPIs
1405    const totalPois = pkg.days.reduce((s, d) => s + d.pois.length, 0);
1406    document.querySelector('#kpiScore .kpi-val').textContent = pkg.total_score;
1407    document.querySelector('#kpiCost .kpi-val').textContent = `${fmt(pkg.total_activity_cost)} ฿`;
1408    document.querySelector('#kpiPois .kpi-val').textContent = totalPois;
1409
1410    const root = document.getElementById('dayPanels');
1411    root.innerHTML = '';
1412
1413    pkg.days.forEach((day, dIdx) => {
1414      const color = DAY_COLORS[dIdx % DAY_COLORS.length];
1415      const panel = document.createElement('div');
1416      panel.className = 'day-panel';
1417      panel.innerHTML = `
1418        <div class="day-head">
1419          <div class="day-title">
1420            <div class="day-color" style="background:${color};box-shadow:0 0 8px ${color};"></div>
1421            <h3>วันที่ ${dIdx + 1}</h3>
1422          </div>
1423          <div class="day-stats">
1424            <span class="day-score">${ICON.star} ${day.score}</span>
1425            <span>${ICON.coin} ${fmt(day.cost)}</span>
1426            <span>${ICON.clock} ${fmtDur(day.time_min)}</span>
1427            <span>${ICON.route} ${day.distance_km.toFixed(1)}km</span>
1428          </div>
1429        </div>
1430        <ul class="poi-list" id="day-${dIdx}-list"></ul>
1431        <button class="day-add" onclick="addPoiToDay(${dIdx})">
1432          <div class="add-num">${ICON.plus}</div>
1433          <span>เพิ่มสถานที่</span>
1434        </button>
1435      `;
1436      root.appendChild(panel);
1437
1438      const list = panel.querySelector('.poi-list');
1439      if (!day.pois.length) {
1440        list.innerHTML = '<li style="text-align:center;color:var(--text-muted);padding:1rem 0;font-size:0.85rem;">ยังไม่มีจุดในวันนี้</li>';
1441      }
1442      day.pois.forEach((poi, pIdx) => {
1443        // Distance connector before this POI
1444        if (pIdx === 0 && showHotel) {
1445          const distKm = haversineKm(pkg.hotel.lat, pkg.hotel.lng, poi.lat, poi.lng);
1446          const distEl = document.createElement('li');
1447          distEl.className = 'dist-connector';
1448          distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('hotel')} ${ic('arrow-right')} ${distKm.toFixed(1)} km</span><span class="dist-line"></span>`;
1449          list.appendChild(distEl);
1450        } else if (pIdx > 0) {
1451          const prev = day.pois[pIdx - 1];
1452          const distKm = haversineKm(prev.lat, prev.lng, poi.lat, poi.lng);
1453          const distEl = document.createElement('li');
1454          distEl.className = 'dist-connector';
1455          distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('arrow-down')} ${distKm.toFixed(1)} km</span><span class="dist-line"></span>`;
1456          list.appendChild(distEl);
1457        }
1458
1459        const li = document.createElement('li');
1460        li.className = 'poi-item';
1461        li.dataset.id = poi.id;
1462        li.innerHTML = `
1463          <div class="poi-num">${pIdx + 1}</div>
1464          <div class="poi-info">
1465            <div class="poi-name poi-link" onclick="showPoiDetail('${poi.id}', ${arriveOf(day, poi)})" title="ดูรายละเอียดและรีวิว">${CAT_ICON[poi.category] || ''} ${poi.name_th}</div>
1466            <div class="poi-meta">
1467              <span class="pill">${CAT_LABELS[poi.category] || poi.category}</span>
1468              ${arriveOf(day, poi) >= 0 ? `<span class="time-chip"><span class="tc-lbl">ตั้งแต่</span> ${fmtClock(arriveOf(day, poi))}–${fmtClock(arriveOf(day, poi) + (poi.duration_min || 0))} · เปิด ${hoursText(poi)}</span>` : ''}
1469              <span class="score-chip">${ic('star')} ${poi.score}</span>
1470              <span>${poi.cost} ฿</span>
1471              <span class="dur"><span class="dur-lbl">ใช้เวลา</span> ${fmtDur(poi.duration_min)}</span>
1472            </div>
1473          </div>
1474          <div class="poi-actions">
1475            <a class="btn-loc" href="${gmapsUrl(poi)}" target="_blank" rel="noopener" title="ดูใน Google Maps">${ICON.pin}</a>
1476            <button class="btn-swap" onclick="openSwapModal(${dIdx}, ${pIdx})" title="เปลี่ยน">${ICON.swap}</button>
1477            <button class="btn-remove" onclick="removePoi(${dIdx}, ${pIdx})" title="ลบ">${ICON.trash}</button>
1478          </div>
1479        `;
1480        list.appendChild(li);
1481
1482        // Return connector after last POI
1483        if (pIdx === day.pois.length - 1 && showHotel) {
1484          const distKm = haversineKm(poi.lat, poi.lng, pkg.hotel.lat, pkg.hotel.lng);
1485          const distEl = document.createElement('li');
1486          distEl.className = 'dist-connector';
1487          distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('arrow-down')} ${distKm.toFixed(1)} km ${ic('arrow-right')} ${ic('hotel')}</span><span class="dist-line"></span>`;
1488          list.appendChild(distEl);
1489        }
1490      });
1491    });
1492  }
บรรทัด 1398–1402: renderDetail ตั้งหัวเรื่องเป็น "ระดับ — ชื่อโรงแรม" หรือ "ไม่รวมที่พัก" (ถูกห่อโดย ➜ frontend/extras.js และ ➜ frontend/tutorial.js เพื่อเพิ่มพยากรณ์ คำเตือน การลากวาง ประวัติ และวิธีใช้)
บรรทัด 1404–1408: ใส่ตัวเลขสรุป (คะแนน ค่ากิจกรรม จำนวนจุด)
บรรทัด 1410–1411: ล้างรายการวันเดิม
บรรทัด 1413–1416: แต่ละวัน สร้างแผงวัน
บรรทัด 1417–1435: โครงแผง: ชื่อวันที่ สถิติของวัน (คะแนน ค่าใช้จ่าย เวลา ระยะทาง) รายการสถานที่ และปุ่ม "เพิ่มสถานที่" ที่เรียก addPoiToDay
บรรทัด 1436–1441: ต่อแผงเข้าหน้า ถ้าวันนั้นไม่มีจุด แสดงข้อความว่าง
บรรทัด 1442–1449: ก่อนจุดแรก (ถ้ารวมโรงแรม) แทรกป้ายระยะทางจากโรงแรม (haversineKm)
บรรทัด 1450–1457: ก่อนจุดถัด ๆ ไป แทรกป้ายระยะทางจากจุดก่อนหน้า
บรรทัด 1459–1472: สร้างการ์ดสถานที่: เลขลำดับ ชื่อ (คลิกดูรายละเอียด) หมวด เวลา (ตั้งแต่-ถึง และเวลาเปิด-ปิด) คะแนน ราคา และเวลาที่ใช้
บรรทัด 1474–1479: ปุ่มของการ์ด: ลิงก์ Google Maps ปุ่มเปลี่ยน (➜ openSwapModal() ใน frontend/app.js) และปุ่มลบ (➜ removePoi() ใน frontend/app.js) ต่อการ์ดเข้ารายการ
บรรทัด 1482–1489: หลังจุดสุดท้าย (ถ้ารวมโรงแรม) แทรกป้ายระยะทางกลับโรงแรม
บรรทัด 1490–1492: ปิดการวนและฟังก์ชัน
บรรทัด 1497–1522  เปิดหน้าต่างเปลี่ยนหรือเพิ่มสถานที่
1497  function openSwapModal(dayIdx, poiIdx) {
1498    const currentPoi = STATE.selectedPkg.days[dayIdx].pois[poiIdx];
1499    STATE.swapContext = {dayIdx, poiIdx, currentPoi, mode: 'swap', categoryFilter: 'all'};
1500    document.getElementById('swapTitle').textContent = 'เปลี่ยนสถานที่';
1501    document.getElementById('swapCurrentInfo').innerHTML =
1502      `ปัจจุบัน: ${CAT_ICON[currentPoi.category] || ''} ${currentPoi.name_th}`;
1503    document.getElementById('swapFilter').value = '';
1504    renderSwapList();
1505    document.getElementById('swapModal').classList.add('open');
1506    document.body.style.overflow = 'hidden';
1507  }
1508
1509  function addPoiToDay(dayIdx) {
1510    STATE.swapContext = {dayIdx, poiIdx: null, currentPoi: null, mode: 'add', categoryFilter: 'all'};
1511    document.getElementById('swapTitle').textContent = 'เพิ่มจุดใหม่';
1512    document.getElementById('swapCurrentInfo').textContent = `เพิ่มในวันที่ ${dayIdx + 1}`;
1513    document.getElementById('swapFilter').value = '';
1514    renderSwapList();
1515    document.getElementById('swapModal').classList.add('open');
1516    document.body.style.overflow = 'hidden';
1517  }
1518
1519  function setCategoryFilter(cat) {
1520    STATE.swapContext.categoryFilter = cat;
1521    renderSwapList();
1522  }
บรรทัด 1497–1507: openSwapModal (ผูกกับปุ่มเปลี่ยนของการ์ด) จดบริบท: วัน ตำแหน่ง สถานที่ปัจจุบัน โหมด "swap" และตัวกรองหมวด ตั้งหัวเรื่องและบรรทัดข้อมูลปัจจุบัน ล้างช่องค้นหา วาดรายการ (➜ renderSwapList() ใน frontend/app.js) แล้วเปิดโมดัลของ ➜ frontend/index.html
บรรทัด 1509–1517: addPoiToDay ทำเช่นเดียวกันแต่โหมด "add" เพื่อเพิ่มจุดท้ายวัน
บรรทัด 1519–1522: setCategoryFilter เปลี่ยนตัวกรองหมวดและวาดรายการใหม่
บรรทัด 1525–1538  ตัวช่วยรายการสถานที่
1525  function swapRainIcon(p) {
1526    const ctx = STATE.swapContext;
1527    if (!ctx || !window.dayRainPop || window.dayRainPop(ctx.dayIdx) < 60 || !(window.OUTDOOR_CATS || []).includes(p.category)) return '';
1528    const tip = window.WET_LANG === 'en' ? 'Outdoor place, it may rain' : 'สถานที่กลางแจ้ง อาจมีฝนตกได้';
1529    return `<span class="rain-ic" title="${tip}"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 14a4 4 0 0 0 0-8 5.5 5.5 0 0 0-10.6 1.5A3.5 3.5 0 0 0 7 14"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/></svg></span>`;
1530  }
1531
1532  // ลิงก์ Google Maps ค้นหาด้วยชื่อสถานที่ + ชื่อจังหวัด เพื่อให้ปักหมุดที่สถานที่จริงของ Google (ไม่ใช่พิกัดจากข้อมูล OSM ที่อาจเลื่อน)
1533  // ถ้าไม่มีชื่อไทยใช้ชื่ออังกฤษ
1534  function gmapsUrl(p) {
1535    const prov = STATE.provinces[getProvince()];
1536    const q = [p.name_th || p.name_en, prov?.name_th].filter(Boolean).join(' ');
1537    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`;
1538  }
บรรทัด 1525–1530: swapRainIcon ถ้าวันนั้นโอกาสฝน ≥ 60% (dayRainPop จาก ➜ frontend/extras.js) และสถานที่เป็นกลางแจ้ง คืนไอคอนฝนพร้อม tooltip สองภาษา ไม่เช่นนั้นคืนข้อความว่าง
บรรทัด 1532–1538: gmapsUrl สร้างลิงก์ค้นหาใน Google Maps ด้วยชื่อสถานที่ (หรือชื่ออังกฤษถ้าไม่มีชื่อไทย) ผนวกชื่อจังหวัดที่เลือก เพื่อปักหมุดที่สถานที่จริง
บรรทัด 1540–1587  วาดรายการสถานที่ให้เลือก
1540  function renderSwapList() {
1541    const ctx = STATE.swapContext;
1542    const usedIds = new Set();
1543    STATE.selectedPkg.days.forEach(d => d.pois.forEach(p => usedIds.add(p.id)));
1544    const all = STATE.pois.filter(p => !usedIds.has(p.id));
1545
1546    const counts = {all: all.length};
1547    all.forEach(p => { counts[p.category] = (counts[p.category] || 0) + 1; });
1548
1549    const filterCat = ctx.categoryFilter || 'all';
1550    const candidates = (filterCat === 'all' ? all : all.filter(p => p.category === filterCat))
1551      .sort((a, b) => b.score - a.score);
1552
1553    const cats = ['all', 'beach', 'temple', 'viewpoint', 'culture', 'market', 'activity', 'restaurant'];
1554    const filterButtons = cats
1555      .filter(c => counts[c])
1556          .map(c => `<button class="cat-btn ${c === filterCat ? 'active' : ''}" onclick="setCategoryFilter('${c}')">
1557                   ${c === 'all' ? '' : CAT_ICON[c] + ' '}${CAT_LABELS[c]} <span style="opacity:0.7">${counts[c]}</span>
1558                 </button>`).join('');
1559
1560    const list = document.getElementById('swapList');
1561    list.innerHTML = `
1562      <div class="cat-filter">${filterButtons}</div>
1563      ${candidates.length === 0
1564        ? '<div class="empty-msg">ไม่มีจุดที่ตรงเงื่อนไข</div>'
1565        : candidates.map(p => `
1566          <div class="swap-option" onclick="confirmSwap('${p.id}')">
1567            <div class="opt-info">
1568              <b>${CAT_ICON[p.category] || ''} ${p.name_th}${swapRainIcon(p)}</b>
1569              <span class="meta">${CAT_LABELS[p.category]} · ${p.cost} ฿ · ${p.duration_min} นาที</span>
1570              <span class="meta">เปิด-ปิด ${hoursText(p)}</span>
1571            </div>
1572            <div class="opt-actions">
1573              <button type="button" class="opt-btn" title="ดูรีวิว" onclick="event.stopPropagation(); showPoiDetail('${p.id}', -1)"><svg class="ic" viewBox="0 0 24 24"><use href="#i-star"/></svg></button>
1574              <a class="opt-btn" title="ดูใน Google Maps" target="_blank" rel="noopener" href="${gmapsUrl(p)}" onclick="event.stopPropagation()"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></a>
1575            </div>
1576          </div>
1577        `).join('')
1578      }
1579    `;
1580  }
1581
1582  function filterSwapList() {
1583    const q = document.getElementById('swapFilter').value.toLowerCase();
1584    document.querySelectorAll('.swap-option').forEach(el => {
1585      el.style.display = el.textContent.toLowerCase().includes(q) ? 'flex' : 'none';
1586    });
1587  }
บรรทัด 1540–1544: renderSwapList หาสถานที่ที่ยังไม่อยู่ในแผน
บรรทัด 1546–1547: นับจำนวนต่อหมวด
บรรทัด 1549–1551: กรองตามหมวดที่เลือก แล้วเรียงตามคะแนนมากไปน้อย
บรรทัด 1553–1558: สร้างปุ่มกรองหมวด (เฉพาะหมวดที่มีสถานที่) พร้อมจำนวน
บรรทัด 1560–1579: ใส่ตัวกรองและรายการ ถ้าไม่มีแสดงข้อความ ไม่เช่นนั้นแต่ละตัวเลือกแสดงชื่อ (พร้อมไอคอนฝน) หมวด ราคา เวลาที่ใช้ เวลาเปิด-ปิด ปุ่มดูรีวิว และลิงก์ Google Maps คลิกที่ตัวเลือกเรียก confirmSwap
บรรทัด 1582–1587: filterSwapList (ผูกกับช่องค้นหาใน ➜ frontend/index.html) ซ่อนตัวเลือกที่ข้อความไม่ตรงคำค้น
บรรทัด 1591–1621  ยืนยันสลับ เพิ่ม ลบ
1591  function snapshotEdit() { return {days: STATE.selectedPkg.days.map(d => d.pois.slice()), locked: new Set(STATE.locked), excluded: new Set(STATE.excluded)}; }
1592  function restoreEdit(sn) { STATE.selectedPkg.days.forEach((d, i) => { d.pois = sn.days[i].slice(); }); STATE.locked = sn.locked; STATE.excluded = sn.excluded; }
1593
1594  async function confirmSwap(newPoiId) {
1595    const ctx = STATE.swapContext;
1596    const newPoi = STATE.poisById[newPoiId];
1597    const sn = snapshotEdit();
1598    if (ctx.mode === 'swap') {
1599      STATE.selectedPkg.days[ctx.dayIdx].pois[ctx.poiIdx] = newPoi;
1600    } else {
1601      STATE.selectedPkg.days[ctx.dayIdx].pois.push(newPoi);
1602    }
1603    STATE.locked.add(newPoiId);
1604    STATE.excluded.delete(newPoiId);
1605    closeSwapModal();
1606    await recomputeAndRefresh(() => restoreEdit(sn));
1607  }
1608
1609  function removePoi(dayIdx, poiIdx) {
1610    const sn = snapshotEdit();
1611    const [removed] = STATE.selectedPkg.days[dayIdx].pois.splice(poiIdx, 1);
1612    STATE.locked.delete(removed.id);
1613    STATE.excluded.add(removed.id);
1614    recomputeAndRefresh(() => restoreEdit(sn));
1615  }
1616
1617  function closeSwapModal() {
1618    document.getElementById('swapModal').classList.remove('open');
1619    document.body.style.overflow = '';
1620    STATE.swapContext = null;
1621  }
บรรทัด 1589–1590: คอมเมนต์: การเพิ่ม สลับ ลบ ทำตามที่ผู้ใช้สั่งตรง ๆ แล้วให้ backend คำนวณเวลาและค่าใช้จ่ายใหม่ (เดิมเรียก Hybrid ทุกครั้ง ซึ่งทำให้สถานที่อื่นหายเมื่อเพิ่มกิจกรรมยาว)
บรรทัด 1591–1592: snapshotEdit และ restoreEdit จำและคืนลำดับสถานที่ ชุดล็อก และชุดลบ เพื่อย้อนกลับเมื่อ backend ล้มเหลว
บรรทัด 1594–1607: confirmSwap หาสถานที่ใหม่ จำสถานะ แทนที่หรือต่อท้ายวัน ใส่ในชุดล็อก เอาออกจากชุดลบ ปิดโมดัล แล้วเรียก recomputeAndRefresh
บรรทัด 1609–1615: removePoi จำสถานะ ตัดจุดออก เอาออกจากชุดล็อกใส่ในชุดลบ (ห้าม reoptimize ใส่กลับ) แล้วคำนวณใหม่
บรรทัด 1617–1621: closeSwapModal ปิดโมดัล คืนการเลื่อน และล้างบริบท
บรรทัด 1626–1705  สุ่มแพ็กเกจใหม่
1626  async function reshufflePackage() {
1627    if (!STATE.selectedPkg) return;
1628    const targetTier = STATE.selectedPkg.tier;
1629
1630    const budget    = +document.getElementById('budget').value;
1631    const days      = getSelectedDays();
1632    const travelers = +document.getElementById('travelers').value;
1633    const includeHotel = days === 1 ? false : (document.getElementById('includeHotel')?.checked !== false);
1634
1635    const detailEl = document.getElementById('detailPanel');
1636    // Inject animated overlay
1637    const overlay = document.createElement('div');
1638    overlay.id = 'reshuffleOverlay';
1639    overlay.innerHTML = `<div class="reshuffle-overlay-inner">
1640      <svg class="reshuffle-ring" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
1641        <circle cx="25" cy="25" r="20" stroke="rgba(34,211,238,0.25)" stroke-width="3"/>
1642        <circle cx="25" cy="25" r="20" stroke="#22d3ee" stroke-width="3" stroke-dasharray="40 90" stroke-linecap="round"/>
1643      </svg>
1644      <span>กำลังสุ่มสถานที่ใหม่...</span>
1645    </div>`;
1646    detailEl.appendChild(overlay);
1647    detailEl.classList.add('reshuffling');
1648    const t = showToast('กำลังสุ่มสถานที่ใหม่...', 'loading', 30000);
1649
1650    try {
1651      const ctrl = new AbortController();
1652      const timer = setTimeout(() => ctrl.abort(), 25000);
1653      const res = await fetch(`${API_BASE}/api/packages`, {
1654        method: 'POST',
1655        headers: devHeaders(),
1656        body: JSON.stringify({
1657          province: getProvince(),
1658          preferences: getPreferences(),
1659          budget, days, travelers,
1660          seed: Math.floor(Math.random() * 1000000),
1661          algorithm: STATE.dev ? SELECTED_ALGO : 'hybrid',
1662          include_hotel: includeHotel,
1663        }),
1664        signal: ctrl.signal,
1665      });
1666      clearTimeout(timer);
1667      if (!res.ok) throw new Error(`HTTP ${res.status}`);
1668      const data = await res.json();
1669
1670      // Update global package list
1671      STATE.packages = data.packages;
1672      STATE.includeHotel = includeHotel && !data.packages.every(p => !p.total_hotel_cost);   // งบไม่พอที่พัก: เซิร์ฟเวอร์สร้างแบบไม่รวมโรงแรมให้
1673
1674      // Find the matching tier (or fall back to same index)
1675      const tierIdx = data.packages.findIndex(p => p.tier === targetTier);
1676      const newIdx  = tierIdx >= 0 ? tierIdx : STATE.selectedIdx;
1677      STATE.selectedIdx = newIdx;
1678      STATE.selectedPkg = JSON.parse(JSON.stringify(data.packages[newIdx]));
1679      STATE.locked.clear(); STATE.excluded.clear();
1680      setTimeout(pushSession, 600);
1681
1682      // Refresh package cards without clearing detail section
1683      renderPackages();
1684      document.querySelectorAll('.package-card').forEach((c, i) =>
1685        c.classList.toggle('selected', i === newIdx)
1686      );
1687
1688      // Update detail in-place
1689      renderDetail(STATE.selectedPkg);
1690      setTimeout(() => {
1691        STATE.map.invalidateSize();
1692        drawOnMap(STATE.selectedPkg);
1693        setTimeout(syncMapHeight, 100);
1694      }, 80);
1695
1696      t.remove();
1697      showToast(STATE.dev ? `สุ่มใหม่แล้ว! Score ${STATE.selectedPkg.total_score}` : 'สุ่มใหม่แล้ว!', 'ok');
1698    } catch (e) {
1699      t.remove();
1700      showToast(`ผิดพลาด: ${e.message}`, 'error');
1701    } finally {
1702      detailEl.classList.remove('reshuffling');
1703      document.getElementById('reshuffleOverlay')?.remove();
1704    }
1705  }
บรรทัด 1626–1628: reshufflePackage (ผูกกับปุ่ม Re-shuffle) จำระดับของแพ็กเกจที่เลือก
บรรทัด 1630–1633: อ่านงบ วัน คน และตัวเลือกโรงแรมจากฟอร์ม
บรรทัด 1635–1648: ใส่ overlay หมุนทับส่วนรายละเอียด และแสดงข้อความ loading
บรรทัด 1650–1665: ตั้งตัวตัดเวลา 25 วินาที แล้วส่ง POST ไป /api/packages (➜ create_packages() ใน backend/main.py) ด้วย seed ใหม่ และอัลกอริทึมเดิม
บรรทัด 1666–1668: ตรวจผลและอ่านข้อมูล
บรรทัด 1671–1672: ตั้งรายการแพ็กเกจใหม่และธงรวมโรงแรม
บรรทัด 1674–1680: หาแพ็กเกจระดับเดียวกัน (ไม่มีใช้ตำแหน่งเดิม) ทำสำเนา ล้างชุดล็อกและลบ และส่งขึ้นเซสชันหลัง 0.6 วินาที (➜ pushSession() ใน frontend/app.js)
บรรทัด 1682–1689: วาดการ์ดแพ็กเกจใหม่โดยไม่ล้างส่วนรายละเอียด ไฮไลต์ใบที่เลือก และวาดรายละเอียด
บรรทัด 1690–1694: หลังหน่วงเล็กน้อย คำนวณขนาดและวาดแผนที่ใหม่
บรรทัด 1696–1697: ลบข้อความ loading และแจ้งผล
บรรทัด 1698–1704: ถ้าผิดพลาดแจ้งข้อความ และไม่ว่าอย่างไรเอา overlay ออก
บรรทัด 1707–1742  คำนวณใหม่หลังแก้
1707  async function recomputeAndRefresh(rollback) {
1708    const t = showToast('กำลังคำนวณเส้นทางใหม่...', 'loading', 10000);
1709    try {
1710      const routes = STATE.selectedPkg.days.map(d => d.pois.map(p => p.id));
1711      const res = await fetch(`${API_BASE}/api/recompute`, {
1712        method: 'POST',
1713        headers: {'Content-Type': 'application/json'},
1714        body: JSON.stringify({
1715          province: getProvince(),
1716          hotel_id: STATE.selectedPkg.hotel.id,
1717          days: STATE.selectedPkg.days.length,
1718          budget: 100000,
1719          routes,
1720          travelers: +document.getElementById('travelers').value,
1721        }),
1722      });
1723      if (!res.ok) throw new Error(`HTTP ${res.status}`);
1724      const data = await res.json();
1725      if (STATE.selectedPkg._base instanceof Set) setHidden(data, '_base', STATE.selectedPkg._base);   // คำเตือนตั้งต้นของแผนเดิม (ไม่ให้ถูก serialize)
1726      if (STATE.selectedPkg._orig) setHidden(data, '_orig', STATE.selectedPkg._orig);   // แผนตั้งต้นสำหรับปุ่มคืนค่าเดิม
1727      STATE.selectedPkg = data;
1728      drawOnMap(data);
1729      renderDetail(data);
1730      pushSession();   // ส่งแผนที่ผู้ใช้แก้ (ลาก/สลับ/ลบ/เพิ่ม) ขึ้นเซสชัน ให้เครื่องอื่นเห็น (ถ้าไม่ได้แชร์จะไม่ทำอะไร)
1731      t.remove();
1732      if (uiWarnings(data).length) {
1733        showToast(`อัปเดตแล้ว · ${uiWarnings(data).length} คำเตือน (ดูการ์ดสีแดง)`, 'error', 5000);
1734      } else {
1735        showToast((STATE.dev ? `อัปเดต! Score ${data.total_score}` : 'อัปเดตแผนแล้ว'), 'ok');
1736      }
1737    } catch (e) {
1738      t.remove();
1739      if (rollback) { rollback(); drawOnMap(STATE.selectedPkg); renderDetail(STATE.selectedPkg); }   // คืนแผนเดิม ไม่ให้หมุด/การ์ดค้างผิดที่
1740      showToast(`ผิดพลาด: ${e.message}${rollback ? ' (คืนแผนเดิมแล้ว)' : ''}`, 'error');
1741    }
1742  }
บรรทัด 1707–1710: recomputeAndRefresh (ฟังก์ชันที่ ➜ moveStop() ใน frontend/extras.js และการลาก/สลับเรียกใช้) รับฟังก์ชัน rollback สำหรับคืนค่า แล้วรวบรวมเส้นทางของแต่ละวัน
บรรทัด 1711–1722: ส่ง POST ไป /api/recompute (➜ recompute() ใน backend/main.py) พร้อมจังหวัด โรงแรม วัน งบ (ตั้ง 100,000 เพื่อไม่ให้งบตัดจุดที่ผู้ใช้เลือก) เส้นทาง และจำนวนคน ฝั่ง backend คำนวณเวลาถึง ค่าใช้จ่าย และระยะทางตามลำดับที่ผู้ใช้กำหนด
บรรทัด 1723–1727: ตรวจผล ส่งต่อคำเตือนตั้งต้น (เฉพาะเมื่อเป็น Set) และแผนตั้งต้น (ซ่อนจาก JSON) แล้วตั้งเป็นแผนที่เลือก
บรรทัด 1728–1736: วาดแผนที่และรายละเอียด ส่งแผนที่ผู้ใช้แก้ขึ้นเซสชันด้วย pushSession (ให้เครื่องอื่นเห็น) ลบข้อความ loading และแจ้งผล (ถ้ามีคำเตือนเป็นสีแดงให้ดูการ์ดสีแดง)
บรรทัด 1737–1741: ถ้าผิดพลาด เรียก rollback คืนแผนเดิมแล้ววาดใหม่ และแจ้งข้อผิดพลาด
บรรทัด 1747–1759  ฟังก์ชันเบ็ดเตล็ด
1747  function fmt(n) { return Math.round(n).toLocaleString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH')); }
1748
1749  function haversineKm(lat1, lng1, lat2, lng2) {
1750    const R = 6371, dLat = (lat2-lat1)*Math.PI/180, dLng = (lng2-lng1)*Math.PI/180;
1751    const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLng/2)**2;
1752    // × road_factor ของจังหวัด (จาก /api/provinces) ให้ตรงกับระยะที่ backend ใช้คำนวณเวลาและค่าเดินทาง
1753    return R * 2 * Math.asin(Math.sqrt(a)) * (STATE.provinces[getProvince()]?.road_factor || 1);
1754  }
1755
1756
1757  document.addEventListener('keydown', e => {
1758    if (e.key === 'Escape') closeSwapModal();
1759  });
บรรทัด 1747: fmt จัดรูปตัวเลขตามภาษา (ไทยหรืออังกฤษ ตาม WET_LANG ของ ➜ frontend/i18n.js)
บรรทัด 1749–1754: haversineKm คำนวณระยะทางบนผิวโลกด้วยสูตร haversine (รัศมี 6371 กม.) คูณ road_factor ของจังหวัดที่ ➜ data/calibrate_travel.py ปรับเทียบไว้ ให้ตรงกับระยะที่ backend ใช้คำนวณเวลาเดินทางและค่าเดินทาง
บรรทัด 1757–1759: กด Esc เพื่อปิดหน้าต่างเปลี่ยนสถานที่

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
algorithm/pareto.py
algorithm/rl.py
backend/main.py
data/build_all_provinces.py
data/calibrate_travel.py
frontend/app.js
frontend/extras.js
frontend/i18n.js
frontend/index.html
frontend/style.css
frontend/tutorial.js