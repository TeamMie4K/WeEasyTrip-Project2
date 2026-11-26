<!-- converted from frontend__app.js.docx -->

คู่มือโค้ด: frontend/app.js
ตรรกะหลักของหน้าเว็บ (app.js)
ไฟล์ต้นฉบับ: frontend/app.js (1713 บรรทัด)   ➜ กลับสารบัญคู่มือ
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
บรรทัด 518–528  ตั้งค่าที่ส่งขึ้นเซสชัน
518  function sessionSettings() {
519    const d = DATE_PICKER && DATE_PICKER.selectedDates[0];
520    return {
521      budget: +document.getElementById('budget').value,
522      travelers: +document.getElementById('travelers').value,
523      include_hotel: STATE.includeHotel !== false,
524      start_date: d ? `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}` : null,
525      preferences: getPreferences(),
526      locked: [...STATE.locked], excluded: [...STATE.excluded],
527    };
528  }
บรรทัด 518–528: sessionSettings รวมงบ จำนวนคน ตัวเลือกโรงแรม วันเริ่ม ความชอบ และชุด locked/excluded เป็นอ็อบเจ็กต์ที่ส่งไปให้เพื่อน
บรรทัด 530–539  นำสถานะที่ได้มาใช้
530  function applySharedState(data, announce) {
531    STATE.selectedPkg = data.package;
532    const st = data.settings || {};
533    STATE.locked = new Set(st.locked || []);
534    STATE.excluded = new Set(st.excluded || []);
535    STATE.session.version = data.version;
536    drawOnMap(STATE.selectedPkg);
537    renderDetail(STATE.selectedPkg);
538    if (announce) showToast(announce, 'ok', 3000);
539  }
บรรทัด 530–535: applySharedState ตั้งแผน จุดที่ล็อกและลบ และเลขรุ่น (version) จากข้อมูลของเซสชัน
บรรทัด 536–538: วาดแผนที่ (➜ drawOnMap() ใน frontend/app.js) และรายละเอียด (➜ renderDetail() ใน frontend/app.js) ใหม่ และแจ้งข้อความถ้ามี
บรรทัด 541–562  สร้างลิงก์แชร์
541  async function shareSession() {
542    const pkg = STATE.selectedPkg;
543    if (!pkg) return;
544    try {
545      if (!STATE.session) {
546        const res = await fetch(`${API_BASE}/api/sessions`, {
547          method: 'POST', headers: {'Content-Type': 'application/json'},
548          body: JSON.stringify({province: getProvince(), package: pkg, settings: sessionSettings()}),
549        });
550        if (!res.ok) throw new Error(`HTTP ${res.status}`);
551        const data = await res.json();
552        STATE.session = {id: data.id, version: data.version, timer: null, busy: false};
553        history.replaceState(null, '', `?s=${data.id}`);
554        startSessionPolling();
555      }
556      const url = location.href;
557      try { await navigator.clipboard.writeText(url); showToast('คัดลอกลิงก์แล้ว — ส่งให้เพื่อนเพื่อวางแผนร่วมกัน', 'ok', 4500); }
558      catch (e) { window.prompt('คัดลอกลิงก์นี้ส่งให้เพื่อน', url); }
559    } catch (e) {
560      showToast(`แชร์ไม่สำเร็จ: ${e.message}`, 'error');
561    }
562  }
บรรทัด 541–543: shareSession ถ้าไม่มีแผนออก
บรรทัด 545–552: ถ้ายังไม่มีเซสชัน ส่ง POST ไป /api/sessions (➜ create_session() ใน backend/main.py) พร้อมจังหวัด แผน และค่าตั้ง แล้วจดรหัสเซสชันและเลขรุ่น
บรรทัด 553–554: ใส่ ?s=<รหัส> ใน URL และเริ่มโพลล์ดูการเปลี่ยนแปลง
บรรทัด 556–558: คัดลอกลิงก์ลงคลิปบอร์ด ถ้าทำไม่ได้แสดงช่องให้คัดลอกเอง
บรรทัด 559–561: ถ้าผิดพลาดแจ้งข้อความ
บรรทัด 564–577  โพลล์ดูการแก้ไขของเพื่อน
564  function startSessionPolling() {
565    clearInterval(STATE.session.timer);
566    STATE.session.timer = setInterval(async () => {
567      const ss = STATE.session;
568      if (!ss || ss.busy || document.hidden) return;
569      try {
570        const res = await fetch(`${API_BASE}/api/sessions/${ss.id}?since=${ss.version}`);
571        if (res.status === 404) { clearInterval(ss.timer); showToast('เซสชันหมดอายุแล้ว', 'error'); STATE.session = null; return; }
572        if (!res.ok) return;
573        const data = await res.json();
574        if (data.changed) applySharedState(data, 'เพื่อนแก้ไขแผน — อัปเดตให้แล้ว');
575      } catch (e) { /* เครือข่ายสะดุด: ลองใหม่รอบหน้า */ }
576    }, 2000);
577  }
บรรทัด 564–566: startSessionPolling ล้างตัวจับเวลาเก่า แล้วตั้งทุก 2 วินาที
บรรทัด 567–568: ข้ามถ้าไม่มีเซสชัน กำลังส่งอยู่ (busy) หรือแท็บถูกซ่อน
บรรทัด 570–572: ถามเซสชันตามเลขรุ่น ถ้า 404 แจ้งว่าหมดอายุและหยุด
บรรทัด 573–574: ถ้ามีการเปลี่ยน นำสถานะใหม่มาใช้ และแจ้ง "เพื่อนแก้ไขแผน — อัปเดตให้แล้ว"
บรรทัด 575: เครือข่ายสะดุดข้ามไปลองรอบหน้า
บรรทัด 580–597  ส่งการแก้ไขของเราขึ้นเซสชัน
580  async function pushSession() {
581    const ss = STATE.session;
582    if (!ss) return;
583    ss.busy = true;
584    try {
585      const res = await fetch(`${API_BASE}/api/sessions/${ss.id}`, {
586        method: 'PUT', headers: {'Content-Type': 'application/json'},
587        body: JSON.stringify({base_version: ss.version, package: STATE.selectedPkg, settings: sessionSettings()}),
588      });
589      if (res.status === 409) {
590        const err = await res.json();
591        applySharedState(err.detail, 'มีคนแก้ไขพร้อมกัน — ใช้ฉบับล่าสุดของเพื่อน');
592      } else if (res.ok) {
593        ss.version = (await res.json()).version;
594      }
595    } catch (e) { /* ออฟไลน์: เก็บไว้ในเครื่อง */ }
596    finally { ss.busy = false; }
597  }
บรรทัด 580–583: pushSession ออกถ้าไม่มีเซสชัน ตั้ง busy ให้โพลล์ไม่ซ้อน
บรรทัด 585–588: ส่ง PUT พร้อมเลขรุ่นฐาน แผน และค่าตั้ง ไป ➜ update_session() ใน backend/main.py
บรรทัด 589–591: ถ้า 409 (มีคนแก้ก่อน) ใช้ฉบับล่าสุดของเพื่อนแทน และแจ้งผู้ใช้
บรรทัด 592–594: ถ้าสำเร็จ จดเลขรุ่นใหม่
บรรทัด 595–596: ออฟไลน์เก็บในเครื่อง และปลดสถานะ busy เสมอ
บรรทัด 599–638  เข้าร่วมเซสชันจากลิงก์
599  async function joinSession(id) {
600    try {
601      const res = await fetch(`${API_BASE}/api/sessions/${id}`);
602      if (!res.ok) throw new Error(res.status === 404 ? 'ลิงก์หมดอายุหรือไม่ถูกต้อง' : `HTTP ${res.status}`);
603      const data = await res.json();
604      const st = data.settings || {};
605      const item = [...document.querySelectorAll('#provList .prov-item')].find(i => i.dataset.value === data.province);
606      if (item) {                                   // ตั้งจังหวัดโดยไม่ล้างผลซ้ำ แล้วโหลดข้อมูลจังหวัดนั้น
607        document.querySelectorAll('.prov-item').forEach(i => i.classList.remove('prov-active'));
608        item.classList.add('prov-active');
609        document.getElementById('province').value = data.province;
610        document.getElementById('provName').textContent = item.dataset.label;
611      }
612      await loadPois();
613      if (st.budget) document.getElementById('budget').value = st.budget;
614      if (st.travelers) document.getElementById('travelers').value = st.travelers;
615      if (st.start_date && DATE_PICKER) {
616        const d0 = new Date(st.start_date + 'T00:00:00');
617        const d1 = new Date(d0.getTime() + (data.package.days.length - 1) * 86400000);
618        DATE_PICKER.setDate([d0, d1], true);
619      }
620      STATE.includeHotel = st.include_hotel !== false;
621      STATE.session = {id: data.id, version: data.version, timer: null, busy: false};
622      document.getElementById('detailPanel').style.display = 'block';
623      STATE.selectedPkg = data.package;
624      STATE.locked = new Set(st.locked || []); STATE.excluded = new Set(st.excluded || []);
625      renderDetail(STATE.selectedPkg);
626      setTimeout(() => {
627        STATE.map.invalidateSize();
628        drawOnMap(STATE.selectedPkg);
629        document.getElementById('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
630        setTimeout(syncMapHeight, 150);
631      }, 150);
632      startSessionPolling();
633      showToast('เข้าร่วมแผนที่เพื่อนแชร์มา — แก้ไขแล้วทุกคนเห็นพร้อมกัน', 'ok', 4500);
634    } catch (e) {
635      showToast(`เข้าร่วมไม่ได้: ${e.message}`, 'error', 6000);
636      await loadPois();
637    }
638  }
บรรทัด 599–603: joinSession ขอข้อมูลเซสชัน ถ้า 404 แจ้งว่าลิงก์หมดอายุหรือไม่ถูกต้อง
บรรทัด 604–611: ตั้งจังหวัดในเมนูและช่องซ่อนโดยไม่ล้างผลซ้ำ
บรรทัด 612: โหลดสถานที่ของจังหวัดนั้น (➜ loadPois() ใน frontend/app.js)
บรรทัด 613–619: คืนค่างบ จำนวนคน และช่วงวันที่จากค่าตั้งที่แชร์
บรรทัด 620–625: ตั้งสถานะโรงแรม เซสชัน แผน จุดที่ล็อกและลบ แล้วแสดงรายละเอียด
บรรทัด 626–631: หน่วง 150 มิลลิวินาที แล้ววาดแผนที่ เลื่อนหน้า และปรับความสูงแผนที่
บรรทัด 632–633: เริ่มโพลล์ และแจ้งว่าเข้าร่วมแล้ว
บรรทัด 634–637: ถ้าผิดพลาดแจ้งข้อความและโหลดสถานที่ตามปกติ
บรรทัด 643–681  ตัวช่วยเวลา และประวัติย้อนกลับ/เดินหน้า (undo/redo)
643  function fmtClock(min) {
644    return `${String(Math.floor(min / 60) % 24).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`;
645  }
646
647  // เก็บแผนตั้งต้นไว้เป็นคุณสมบัติที่ไม่ถูก serialize (ไม่ปนใน session/ไฟล์บันทึก)
648  function setHidden(obj, key, value) { Object.defineProperty(obj, key, {value, enumerable: false, writable: true, configurable: true}); }
649  const routeIds = p => JSON.stringify((p?.days || []).map(d => d.pois.map(x => x.id)));
650  // ย้อนกลับ / เดินหน้า (undo / redo) ทีละการแก้ไขเหมือนโปรแกรมแต่งภาพ: เก็บสำเนาแผนหลังการแก้แต่ละครั้ง (ลาก ลบ สลับ เพิ่ม สลับเป็นในร่ม) ผูกกับแผนตั้งต้น (_orig) ถ้าสร้างแผนใหม่ประวัติจะเริ่มใหม่
651  const HIST = {orig: null, base: null, stack: [], idx: -1, applying: false};
652  const histSnap = pkg => ({sig: routeIds(pkg) + JSON.stringify([...STATE.locked].sort()) + JSON.stringify([...STATE.excluded].sort()), pkg: JSON.parse(JSON.stringify(pkg)), locked: [...STATE.locked], excluded: [...STATE.excluded]});
653  function recordHistory(pkg) {
654    if (HIST.applying || !pkg._orig) return;
655    const s = histSnap(pkg);
656    if (HIST.orig !== pkg._orig) { HIST.orig = pkg._orig; HIST.stack = [s]; HIST.idx = 0; }
657    else if (s.sig !== HIST.stack[HIST.idx].sig) { HIST.stack = HIST.stack.slice(0, HIST.idx + 1); HIST.stack.push(s); HIST.idx++; if (HIST.stack.length > 50) { HIST.stack.shift(); HIST.idx--; } }
658    HIST.base = pkg._base;
659    updateHistBtns();
660  }
661  function updateHistBtns() {
662    const u = document.getElementById('undoBtn'), r = document.getElementById('redoBtn');
663    if (u) u.classList.toggle('disabled', HIST.idx <= 0);
664    if (r) r.classList.toggle('disabled', HIST.idx >= HIST.stack.length - 1);
665  }
666  function stepHistory(dir) {
667    const n = HIST.idx + dir; if (n < 0 || n >= HIST.stack.length || !STATE.selectedPkg) return;
668    HIST.idx = n; const e = HIST.stack[n], c = JSON.parse(JSON.stringify(e.pkg));
669    setHidden(c, '_orig', HIST.orig); c._base = HIST.base;
670    STATE.selectedPkg = c; STATE.locked = new Set(e.locked); STATE.excluded = new Set(e.excluded);
671    HIST.applying = true;
672    try { drawOnMap(c); renderDetail(c); } finally { HIST.applying = false; }
673    updateHistBtns(); pushSession();
674    showToast(dir < 0 ? 'ย้อนกลับแล้ว' : 'ทำซ้ำแล้ว', 'ok', 1800);
675  }
676  const undoEdit = () => stepHistory(-1), redoEdit = () => stepHistory(1);
677  document.addEventListener('keydown', e => {
678    if (!(e.ctrlKey || e.metaKey) || e.target.closest?.('input, textarea, select, [contenteditable]') || document.querySelector('.modal.open')) return;
679    const k = e.key.toLowerCase();
680    if (k === 'z' && !e.shiftKey) { e.preventDefault(); undoEdit(); } else if (k === 'y' || (k === 'z' && e.shiftKey)) { e.preventDefault(); redoEdit(); }
681  });
บรรทัด 643–645: fmtClock แปลงนาทีจากเที่ยงคืนเป็นข้อความ HH:MM
บรรทัด 647–648: setHidden ตั้งคุณสมบัติที่ไม่ถูกนับตอนแปลงเป็น JSON (enumerable เป็นเท็จ) ใช้เก็บแผนตั้งต้นโดยไม่ปนไปกับเซสชันหรือไฟล์บันทึก
บรรทัด 649: routeIds ลายเซ็นลำดับ id ของสถานที่ทุกวัน
บรรทัด 650–652: HIST ตัวแปรสถานะประวัติ (แผนตั้งต้น ฐานคำเตือน กองประวัติ ตำแหน่ง และธง applying) และ histSnap สร้างสำเนาแผนพร้อมลายเซ็นของแผน ชุดล็อกและชุดลบ
บรรทัด 653–660: recordHistory ถ้ากำลังเรียกจาก undo/redo หรือไม่มีแผนตั้งต้นก็ข้าม ถ้าเป็นแผนใหม่เริ่มกองประวัติใหม่ ถ้าลายเซ็นเปลี่ยนตัดส่วนที่เดินหน้าทิ้ง เพิ่มรายการ (เก็บสูงสุด 50) แล้วอัปเดตปุ่ม (ถูกเรียกจากตัวห่อ renderDetail ใน ➜ recordHistory() ใน frontend/app.js )
บรรทัด 661–665: updateHistBtns ปิดปุ่มย้อนกลับเมื่ออยู่ต้นกอง และปุ่มเดินหน้าเมื่ออยู่ท้ายกอง
บรรทัด 666–675: stepHistory ขยับตำแหน่งในกอง คืนแผน ชุดล็อก/ลบ จากสำเนา วาดใหม่ในขณะตั้งธง applying แล้วส่งขึ้นเซสชัน (➜ pushSession() ใน frontend/app.js) และแจ้งผู้ใช้
บรรทัด 676: undoEdit และ redoEdit (ปุ่มที่ ➜ frontend/extras.js แทรกเรียกฟังก์ชันนี้)
บรรทัด 677–681: ปุ่มลัด Ctrl/Cmd+Z ย้อนกลับ และ Ctrl+Y หรือ Ctrl+Shift+Z เดินหน้า (ไม่ทำงานเมื่อกำลังพิมพ์หรือมีหน้าต่างเปิดอยู่)
บรรทัด 685–702  คำเตือนเวลาเปิด-ปิด
685  function uiWarnings(pkg, raw = false) {
686    const out = [], speed = (STATE.provinces[getProvince().split('+')[0]] || {}).speed_kmh || 40;
687    (pkg.days || []).forEach((day, d) => {
688      let endT = 480, lat = pkg.hotel.lat, lng = pkg.hotel.lng;
689      day.pois.forEach(p => {
690        const full = {...(STATE.pois.find(q => q.id === p.id) || {}), ...p}, at = arriveOf(day, p);
691        const km = haversineKm(lat, lng, p.lat, p.lng), early = endT + km / speed * 60 * 1.25 + (km >= 0.3 ? 10 : 0);   // เวลาถึงก่อนรอร้านเปิด (ตัวคูณจราจร 1.25 + เผื่อจอด/เดิน 10 นาที ตรงกับ algorithm/utils.py)
692        if (full.close_min !== undefined && at >= 0 && at > full.close_min) out.push({d, id: p.id, type: 'late', poi: full});
693        else if (full.open_min > 0 && early < full.open_min - 10) out.push({d, id: p.id, type: 'early', poi: full});
694        endT = (at >= 0 ? at : early) + (p.duration_min || 0); lat = p.lat; lng = p.lng;
695      });
696    });
697    const key = w => `${w.id}:${w.type}`;
698    if (raw) return out;
699    // แผนที่ระบบสร้างเองมีการรอร้านเปิดตามปกติ จึงไม่เตือน: จำคำเตือนตั้งต้นของแผนไว้ (_base) แล้วแสดงเฉพาะที่เกิดใหม่หลังผู้ใช้แก้แผน
700    if (!pkg._base) { pkg._base = new Set(out.map(key)); return []; }
701    return out.filter(w => !pkg._base.has(key(w)));
702  }
บรรทัด 685–686: uiWarnings เตรียมรายการ และความเร็วเดินทางของจังหวัด (ตั้งต้น 40 กม./ชม.)
บรรทัด 687–688: แต่ละวัน เริ่มที่ 8:00 (480 นาที) จากพิกัดโรงแรม
บรรทัด 689–691: แต่ละสถานที่ รวมข้อมูลเวลาเปิด-ปิดจาก STATE.pois หาเวลาถึงที่คำนวณไว้ (➜ arriveOf() ใน frontend/app.js) และประมาณเวลาถึงก่อนรอร้านเปิดด้วยระยะทาง haversineKm ตัวคูณจราจร 1.25 และเวลาเตรียม 10 นาที
บรรทัด 692–693: ถ้าเวลาถึงเกินเวลาปิด เป็นคำเตือน late ถ้าถึงก่อนร้านเปิดเกิน 10 นาที เป็น early
บรรทัด 694–696: อัปเดตเวลาสิ้นสุดและตำแหน่งปัจจุบัน
บรรทัด 697–698: key กุญแจคำเตือน และคืนทั้งหมดถ้า raw
บรรทัด 700: แผนที่ระบบสร้างมีการรอร้านเปิดตามปกติ จึงจำคำเตือนตั้งต้นเป็นฐานและไม่เตือนครั้งแรก
บรรทัด 701–702: ครั้งต่อไปแสดงเฉพาะคำเตือนที่ผู้ใช้ทำเกิดใหม่ (ตัวแสดงผลคือ decorateWarnings ใน ➜ decorateWarnings() ใน frontend/extras.js)
บรรทัด 705–726  ตัวช่วยจัดรูปและเวลาถึง
705  function fmtDur(min) {
706    const m = Math.round(min), h = Math.floor(m / 60), r = m % 60;
707    return h ? (r ? `${h}H ${r}m` : `${h}H`) : `${r}m`;
708  }
709
710  function arriveOf(day, poi) {   // เวลาถึงที่อัลกอริทึมคำนวณ (นาทีจากเที่ยงคืน) หรือ -1 ถ้าไม่มี
711    const a = (day.arrivals || []).find(x => x[0] === poi.id);
712    return a ? a[1] : -1;
713  }
714
715  function hoursText(poi) {
716    if (poi.open_min === undefined) poi = STATE.pois.find(p => p.id === poi.id) || poi;   // POI ในแผนจาก API ไม่มีเวลาเปิด-ปิด
717    if (poi.open_min === undefined) return 'ไม่ระบุ';
718    if (poi.open_min <= 0 && poi.close_min >= 1439) return 'ทั้งวัน';
719    return `${fmtClock(poi.open_min)}–${fmtClock(poi.close_min)}`;
720  }
721
722  function strHash(str) {
723    let h = 2166136261;
724    for (const ch of str) { h ^= ch.codePointAt(0); h = Math.imul(h, 16777619); }
725    return h >>> 0;
726  }
บรรทัด 705–708: fmtDur แสดงระยะเวลาเป็น 45m หรือ 1H 30m
บรรทัด 710–713: arriveOf หาเวลาถึงของสถานที่จาก day.arrivals (ที่ backend คำนวณ) คืน -1 ถ้าไม่มี
บรรทัด 715–720: hoursText ข้อความเวลาเปิด-ปิด ดึงจาก STATE.pois ถ้า POI ในแผนไม่มี คืน "ไม่ระบุ" หรือ "ทั้งวัน"
บรรทัด 722–726: strHash แฮช FNV-1a ของข้อความ ใช้สร้างรีวิวจำลองที่ได้ผลเดิมทุกครั้ง
บรรทัด 728–747  รีวิวจำลอง
728  const MOCK_REVIEWS = {
729    beach: ['ทรายสะอาด น้ำใส เหมาะมาช่วงเช้าที่คนยังน้อย', 'วิวสวย มีร้านอาหารริมหาด แต่ช่วงบ่ายแดดแรง', 'เดินเล่นสบาย จอดรถง่าย บรรยากาศผ่อนคลาย'],
730    temple: ['สถาปัตยกรรมสวยงาม ควรแต่งกายสุภาพ', 'บรรยากาศสงบ เหมาะกับการมาช่วงเช้า', 'มีประวัติน่าสนใจ ใช้เวลาเดินชมไม่นาน'],
731    viewpoint: ['วิวกว้างมาก ถ่ายรูปสวยโดยเฉพาะช่วงเย็น', 'ทางขึ้นค่อนข้างชัน ควรใส่รองเท้าเดินสบาย', 'คุ้มกับการมา อากาศเย็นสบาย'],
732    culture: ['ให้ความรู้ดี เจ้าหน้าที่แนะนำเป็นกันเอง', 'จัดแสดงน่าสนใจ เหมาะกับครอบครัว', 'ค่าเข้าไม่แพง ใช้เวลาชมประมาณชั่วโมงกว่า'],
733    market: ['ของกินหลากหลาย ราคาไม่แพง', 'คนเยอะช่วงเย็น ควรมาก่อนหัวค่ำ', 'ของฝากน่าซื้อ บรรยากาศคึกคัก'],
734    activity: ['กิจกรรมสนุก เจ้าหน้าที่ดูแลดี', 'ควรจองล่วงหน้าช่วงวันหยุด', 'เหมาะกับกลุ่มเพื่อนและครอบครัว'],
735    restaurant: ['รสชาติดี ราคาเหมาะสม บริการรวดเร็ว', 'ร้านบรรยากาศดี ช่วงเที่ยงคนค่อนข้างเยอะ', 'เมนูแนะนำอร่อย ที่นั่งสบาย'],
736  };
737
738  function mockReviewsFor(poi) {   // สร้างจาก id ของสถานที่ ได้ผลเดิมทุกครั้ง; คะแนนอิงคะแนนของระบบ
739    const h = strHash(poi.id + poi.name_en);
740    const rating = Math.max(3.0, Math.min(5.0, poi.score / 2 + ((h % 7) - 3) * 0.05));
741    const pool = MOCK_REVIEWS[poi.category] || MOCK_REVIEWS.culture;
742    const picks = [0, 1, 2].map(i => ({
743      text: pool[(h + i) % pool.length],
744      stars: Math.max(3, Math.min(5, Math.round(rating + (((h >> (i + 3)) % 3) - 1) * 0.6))),
745    }));
746    return {rating, count: 40 + (h % 860), reviews: picks};
747  }
บรรทัด 728–736: MOCK_REVIEWS ประโยครีวิวตัวอย่างต่อหมวด
บรรทัด 738–747: mockReviewsFor สร้างคะแนน จำนวนรีวิว และรีวิวสามอัน จากแฮชของ id และชื่อสถานที่ (คะแนนอิงคะแนนของระบบ) ข้อมูลเหล่านี้เป็นตัวอย่างสำหรับสาธิต และหน้าเว็บมีป้าย "ข้อมูลจำลอง" กำกับ
บรรทัด 749–787  หน้าต่างรายละเอียดสถานที่
749  function showPoiDetail(poiId, arriveMin) {
750    const poi = STATE.pois.find(p => p.id === poiId);
751    if (!poi) return;
752    let m = document.getElementById('poiModal');
753    if (!m) {
754      m = document.createElement('div');
755      m.className = 'modal';
756      m.id = 'poiModal';
757      m.innerHTML = `<div class="modal-backdrop" onclick="closePoiDetail()"></div>
758        <div class="modal-card"><div class="modal-head"><div><div class="modal-title" id="poiTitle"></div>
759        <div class="modal-sub" id="poiSub"></div></div>
760        <button class="icon-btn" onclick="closePoiDetail()" title="ปิด"><svg class="ic "><use href="#i-close"/></svg></button></div>
761        <div class="modal-body" id="poiBody"></div></div>`;
762      document.body.appendChild(m);
763    }
764    const r = mockReviewsFor(poi);
765    const stars = n => '★'.repeat(n) + '☆'.repeat(5 - n);
766    document.getElementById('poiTitle').textContent = poi.name_th;
767    document.getElementById('poiSub').textContent = `${poi.name_en} · ${CAT_LABELS[poi.category] || poi.category}`;
768    document.getElementById('poiBody').innerHTML = `
769      <div class="poi-facts">
770        <div><span>เวลาเปิด-ปิด</span><b>${hoursText(poi)}</b></div>
771        ${arriveMin >= 0 ? `<div><span>เวลาถึงตามแผน</span><b>${fmtClock(arriveMin)}</b></div>` : ''}
772        <div><span>เวลาที่ใช้ ณ สถานที่</span><b>${poi.duration_min} นาที</b></div>
773        <div><span>ค่าใช้จ่าย</span><b>${poi.cost ? fmt(poi.cost) + ' ฿' : 'ฟรี'}</b></div>
774      </div>
775      <p class="poi-note">เวลาเปิด-ปิดมาจากข้อมูล OpenStreetMap หรือเป็นค่าประมาณตามประเภทสถานที่ ควรตรวจสอบกับสถานที่อีกครั้งก่อนเดินทาง</p>
776      <div class="rev-head"><span class="rev-score">${ic('star')} ${r.rating.toFixed(1)}</span>
777        <span class="rev-count">${r.count} รีวิว</span><span class="mock-chip">ข้อมูลจำลอง</span></div>
778      ${r.reviews.map(v => `<div class="rev-item"><div class="rev-stars">${stars(v.stars)}</div><div>${v.text}</div></div>`).join('')}
779      <p class="poi-note">รีวิวและจำนวนรีวิวเป็นข้อมูลตัวอย่างที่สร้างขึ้นเพื่อสาธิตฟีเจอร์ ไม่ใช่ความเห็นของนักท่องเที่ยวจริง (รีวิวจริงเป็นแนวทางต่อยอดผ่านบริการข้อมูลสถานที่)</p>`;
780    m.classList.add('open');
781    document.body.style.overflow = 'hidden';
782  }
783
784  function closePoiDetail() {
785    document.getElementById('poiModal').classList.remove('open');
786    document.body.style.overflow = '';
787  }
บรรทัด 749–751: showPoiDetail หาสถานที่จากรหัส ถ้าไม่พบออก
บรรทัด 752–763: ถ้ายังไม่มีหน้าต่าง สร้างโครงโมดัลต่อท้าย body
บรรทัด 764–767: สร้างรีวิวจำลอง ตัวช่วยดาว และตั้งชื่อ ชื่ออังกฤษ และหมวด
บรรทัด 768–779: เติมเนื้อหา: ตารางข้อมูล (เวลาเปิด-ปิด เวลาถึง เวลาที่ใช้ ค่าใช้จ่าย) หมายเหตุว่ามาจาก OpenStreetMap คะแนน รีวิว และหมายเหตุว่าเป็นข้อมูลตัวอย่าง
บรรทัด 780–781: เปิดโมดัลและล็อกการเลื่อนหน้า
บรรทัด 784–787: closePoiDetail ปิดโมดัลและคืนการเลื่อน
บรรทัด 792–820  เปิดแผนทางเลือก (Pareto)
792  async function openPareto() {
793    const pkg = STATE.selectedPkg;
794    if (!pkg) return;
795    const t = showToast('กำลังหาทางเลือกที่ดีที่สุดในแต่ละด้าน...', 'loading', 20000);
796    try {
797      const res = await fetch(`${API_BASE}/api/pareto`, {
798        method: 'POST',
799        headers: {'Content-Type': 'application/json'},
800        body: JSON.stringify({
801          province: getProvince(), preferences: getPreferences(),
802          budget: +document.getElementById('budget').value, days: pkg.days.length,
803          travelers: +document.getElementById('travelers').value,
804          include_hotel: STATE.includeHotel !== false, seed: Math.floor(Math.random() * 1000000),
805        }),
806      });
807      if (!res.ok) throw new Error(`HTTP ${res.status}`);
808      const data = await res.json();
809      STATE.paretoPlans = data.packages;
810      renderParetoCards(data.packages);
811      t.remove();
812      (data.packages[0]?.notes || []).forEach(n => showToast(n, 'error', 6000));
813      if (!data.packages.length) { showToast('ไม่พบทางเลือกที่ผ่านข้อจำกัด ลองเพิ่มงบหรือลดความชอบ', 'error', 5000); return; }
814      document.getElementById('paretoModal').classList.add('open');
815      document.body.style.overflow = 'hidden';
816    } catch (e) {
817      t.remove();
818      showToast(`ผิดพลาด: ${e.message}`, 'error');
819    }
820  }
บรรทัด 792–794: openPareto (ผูกกับปุ่มใน ➜ frontend/index.html) ถ้าไม่มีแผนออก
บรรทัด 795: แจ้งว่ากำลังหาทางเลือก
บรรทัด 797–806: ส่ง POST ไป /api/pareto (➜ pareto() ใน backend/main.py) ด้วยจังหวัด ความชอบ งบ จำนวนวัน จำนวนคน ตัวเลือกโรงแรม และ seed สุ่ม ฝั่ง backend ใช้ ➜ algorithm/pareto.py หาแผนที่แลกกันระหว่างคะแนน ความหลากหลาย และระยะทาง
บรรทัด 807–811: ตรวจสถานะ เก็บแผนใน STATE.paretoPlans วาดการ์ด (➜ renderParetoCards() ใน frontend/app.js) และลบข้อความรอ
บรรทัด 812: แจ้งหมายเหตุของ backend ทุกข้อ
บรรทัด 813: ถ้าไม่มีแผนผ่านข้อจำกัด แจ้งให้เพิ่มงบหรือลดความชอบ แล้วออก
บรรทัด 814–815: เปิดโมดัลและล็อกการเลื่อน
บรรทัด 816–819: ถ้าผิดพลาดลบข้อความรอและแจ้ง
บรรทัด 823–872  วาดการ์ดแผนทางเลือก
823  function renderParetoCards(plans) {
824    const cur = STATE.selectedPkg, days = Math.max(cur.days.length, 1);
825    const km = p => p.objectives.distance_km, div = p => p.objectives.diversity, cost = p => p.objectives.cost, sc = p => p.objectives.score;
826    const best = (fn, dir) => plans.reduce((m, p, i) => (dir * fn(p) > dir * fn(plans[m]) ? i : m), 0);
827    const labels = {};   // index → [ป้าย, คำอธิบาย]
828    const put = (i, tag, why) => { (labels[i] ||= []).push([tag, why]); };
829    put(best(sc, 1), 'แนะนำ', 'ได้สถานที่น่าสนใจโดยรวมสูงสุด');
830    put(best(km, -1), 'ขับน้อยที่สุด', 'เดินทางสั้น เหนื่อยน้อย ประหยัดค่าเดินทาง');
831    put(best(div, 1), 'หลากหลายที่สุด', 'ได้เที่ยวหลายประเภทในแต่ละวัน');
832    put(best(cost, -1), 'ประหยัดที่สุด', 'ค่าใช้จ่ายรวมต่ำสุด');
833    const picks = Object.keys(labels).map(Number);
834    const rest = plans.map((_, i) => i).filter(i => !picks.includes(i));
835    const dots = d => { const n = Math.max(1, Math.min(5, Math.round(d))); return [1, 2, 3, 4, 5].map(k => `<i class="${k <= n ? 'on' : ''}"></i>`).join(''); };
836    const kmDay = p => km(p) / days;
837    const diff = (v, base, unit, lessGood) => { const d = v - base; if (Math.abs(d) < 0.5) return '<span class="pc-same">เท่าแผนปัจจุบัน</span>'; const good = lessGood ? d < 0 : d > 0; return `<span class="${good ? 'pc-good' : 'pc-bad'}">${d < 0 ? '−' : '+'}${Math.abs(d).toFixed(0)} ${unit}</span>`; };
838    const baseKm = cur.days.reduce((a, d) => a + d.distance_km, 0) / days;
839    const card = (i, extra) => {
840      const p = plans[i], tags = (labels[i] || []).map(x => x[0]), why = (labels[i] || [])[0]?.[1] || 'อีกทางเลือกที่สมดุลระหว่างระยะทาง ความหลากหลายและค่าใช้จ่าย';
841      const hi = p.days.flatMap(d => d.pois).filter(x => x.category !== 'restaurant').sort((a, b) => b.score - a.score).slice(0, 3).map(x => x.name_th);
842      return `<div class="pc ${tags.includes('แนะนำ') ? 'pc-main' : ''}">
843        <div class="pc-top"><div>${(tags.length ? tags : ['ทางเลือก']).map(t => `<span class="pc-tag">${t}</span>`).join('')}<span class="score-chip" style="margin-left:6px">★ ${sc(p)}</span></div></div>
844        <div class="pc-why">${why}</div>
845        <div class="pc-metrics">
846          <div><small>ขับเฉลี่ย/วัน</small><b>${kmDay(p).toFixed(0)} กม.</b>${diff(kmDay(p), baseKm, 'กม./วัน', true)}</div>
847          <div><small>ความหลากหลาย</small><b class="pc-dots">${dots(div(p))}</b></div>
848          <div><small>ค่าใช้จ่าย/คน</small><b>${fmt(cost(p))} ฿</b></div>
849        </div>
850        <div class="pc-hi">${hi.map(n => `<span>${n}</span>`).join('')}</div>
851        <button class="pareto-use" onclick="usePareto(${i})">ใช้แผนนี้</button></div>`;
852    };
853    const box = document.getElementById('paretoTable');
854    box.className = 'pc-wrap';
855    box.innerHTML = picks.sort((a, b) => a - b).map(i => card(i)).join('') +
856      (rest.length ? `<button class="pc-more" onclick="this.nextElementSibling.hidden=false;this.hidden=true">ดูแผนอื่นอีก ${rest.length} แบบ</button><div class="pc-wrap-in" hidden>${rest.map(i => card(i)).join('')}</div>` : '');
857  }
858
859  function closePareto() {
860    document.getElementById('paretoModal').classList.remove('open');
861    document.body.style.overflow = '';
862  }
863
864  function usePareto(i) {
865    STATE.selectedPkg = JSON.parse(JSON.stringify(STATE.paretoPlans[i]));
866    STATE.locked.clear(); STATE.excluded.clear();
867    closePareto();
868    drawOnMap(STATE.selectedPkg);
869    renderDetail(STATE.selectedPkg);
870    pushSession();
871    showToast(`ใช้แผนทางเลือกที่ ${i + 1}`, 'ok');
872  }
บรรทัด 823–826: renderParetoCards อ่านแผนปัจจุบันและจำนวนวัน ตัวดึงเป้าหมายแต่ละด้าน (ระยะทาง ความหลากหลาย ค่าใช้จ่าย คะแนน) และ best หาแผนที่ดีที่สุดในด้านหนึ่ง
บรรทัด 827–828: labels เก็บป้ายและเหตุผลของแต่ละแผน และ put เพิ่มป้าย
บรรทัด 829–832: ติดป้าย: แนะนำ (คะแนนสูงสุด) ขับน้อยที่สุด หลากหลายที่สุด และประหยัดที่สุด พร้อมคำอธิบาย
บรรทัด 833–834: แผนที่ได้ป้ายแสดงก่อน ที่เหลือพับไว้ใน "ดูแผนอื่น"
บรรทัด 835: dots สร้างจุดห้าดวงบอกระดับความหลากหลาย
บรรทัด 836–838: ระยะขับเฉลี่ยต่อวัน และ diff ตัวแสดงส่วนต่างจากแผนปัจจุบัน (เขียวเมื่อดีขึ้น) พร้อมระยะเฉลี่ยของแผนปัจจุบัน
บรรทัด 839–841: card สร้างการ์ดหนึ่งใบ: ป้าย คำอธิบาย และสถานที่เด่น 3 อันดับ (ไม่รวมร้านอาหาร)
บรรทัด 842–851: HTML ของการ์ด: ป้าย คะแนน ตัวชี้วัด (ขับเฉลี่ย ความหลากหลาย ค่าใช้จ่ายต่อคน) สถานที่เด่น และปุ่ม "ใช้แผนนี้" เรียก usePareto
บรรทัด 853–856: ใส่การ์ดที่ได้ป้ายก่อน แล้วปุ่ม "ดูแผนอื่นอีก N แบบ" ที่คลิกแล้วแสดงส่วนที่พับ
บรรทัด 859–862: closePareto ปิดโมดัลและคืนการเลื่อน (ผูกกับ ➜ frontend/index.html)
บรรทัด 864–872: usePareto ใช้แผนที่เลือก (สำเนาลึก) ล้างชุดล็อกและลบ วาดแผนที่และรายละเอียดใหม่ ส่งขึ้นเซสชัน และแจ้ง
บรรทัด 875–909  โหลดรายการจังหวัด
875  const REGION_ORDER = ['ภาคเหนือ', 'ภาคตะวันออกเฉียงเหนือ', 'ภาคกลาง', 'ภาคตะวันออก', 'ภาคตะวันตก', 'ภาคใต้'];
876
877  async function loadProvinces() {
878    try {
879      const res = await fetch(`${API_BASE}/api/provinces`);
880      if (!res.ok) throw new Error(`HTTP ${res.status}`);
881      const data = await res.json();
882      const list = document.getElementById('provList');
883      const active = getProvince();
884      list.innerHTML = '';
885      const regions = {};
886      data.provinces.forEach(pv => {
887        STATE.provinces[pv.slug] = pv;
888        (regions[pv.region || 'อื่น ๆ'] ||= []).push({...pv, ready: true});
889      });
890      data.planned.forEach(pv => (regions[pv.region] ||= []).push({...pv, ready: false}));
891      const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
892      [...REGION_ORDER, ...Object.keys(regions).filter(r => !REGION_ORDER.includes(r))].forEach(r => {
893        const items = (regions[r] || []).sort((a, b) => (b.ready - a.ready) || a.name_th.localeCompare(b.name_th, 'th'));
894        if (!items.length) return;
895        list.insertAdjacentHTML('beforeend', `<div class="prov-group-label">${esc(r)}</div>`);
896        items.forEach(pv => {
897          const el = document.createElement('div');
898          el.className = 'prov-item' + (pv.ready ? '' : ' prov-disabled') + (pv.ready && pv.slug === active ? ' prov-active' : '');
899          el.dataset.label = pv.name_th;
900          if (pv.ready) { el.dataset.value = pv.slug; el.onclick = () => selectProvince(el); }
901          el.innerHTML = `<span class="prov-item-name">${esc(pv.name_th)}</span>` +
902            (pv.ready ? (pv.sparse ? `<span class="prov-item-sparse" title="${pv.pois} สถานที่ ${pv.hotels} โรงแรม — ตัวเลือกอาจน้อย">ข้อมูลน้อย</span>` : '') + '<span class="prov-item-badge">พร้อมใช้งาน</span>' : '<span class="prov-item-soon">เร็วๆ นี้</span>');
903          list.appendChild(el);
904        });
905      });
906    } catch (e) {
907      showToast('โหลดรายการจังหวัดไม่สำเร็จ', 'error', 4000);
908    }
909  }
บรรทัด 875: REGION_ORDER ลำดับภาคที่แสดงในเมนู
บรรทัด 877–881: loadProvinces ขอ /api/provinces (➜ get_provinces() ใน backend/main.py) และอ่านผล
บรรทัด 882–884: ล้างรายการในเมนู (➜ frontend/index.html #provList) และจำจังหวัดที่เลือกอยู่
บรรทัด 885–890: จัดกลุ่มตามภาค: จังหวัดที่พร้อม (provinces) ลง STATE.provinces ส่วนจังหวัดที่ยังไม่มีข้อมูล (planned) แสดงแบบกดไม่ได้
บรรทัด 891: esc หลีกอักขระพิเศษ HTML
บรรทัด 892–895: ไล่ตามลำดับภาค เรียงจังหวัดที่พร้อมก่อน แล้วตามชื่อไทย และใส่ป้ายภาค
บรรทัด 896–904: สร้างรายการจังหวัด: คลาสตามสถานะ (พร้อม กดไม่ได้ กำลังเลือก) ผูกการคลิกกับ selectProvince ใน ➜ frontend/index.html และแสดงป้าย "ข้อมูลน้อย" ถ้าเป็นจังหวัด sparse (สถานะที่ ➜ data/build_all_provinces.py ตัดสินไว้)
บรรทัด 906–908: ถ้าผิดพลาดแจ้งผู้ใช้
บรรทัด 912–940  เปลี่ยนจังหวัดและโหลดสถานที่
912  async function onProvinceChange(slug) {
913    STATE.poisById = {};
914    STATE.packages = [];
915    STATE.selectedPkg = null;
916    STATE.selectedIdx = null;
917    ['packagesSection', 'detailPanel'].forEach(id => { document.getElementById(id).style.display = 'none'; });
918    const pv = STATE.provinces[slug];
919    if (pv && STATE.map) STATE.map.setView(pv.center, pv.zoom);
920    await loadPois();
921  }
922
923  async function loadPois() {
924    try {
925      setApiStatus('loading', 'connecting...');
926      const ctrl = new AbortController();
927      const timer = setTimeout(() => ctrl.abort(), 5000);
928      const res = await fetch(`${API_BASE}/api/pois?province=${encodeURIComponent(getProvince())}`, { signal: ctrl.signal });
929      clearTimeout(timer);
930      if (!res.ok) throw new Error(`HTTP ${res.status}`);
931      const data = await res.json();
932      STATE.pois = data.pois;
933      STATE.hotels = data.hotels;
934      [...data.pois, ...data.hotels].forEach(p => STATE.poisById[p.id] = p);
935      setApiStatus('ok', `${data.pois.length} สถานที่ · ${data.hotels.length} โรงแรม`);
936    } catch (e) {
937      setApiStatus('error', 'backend offline');
938      showToast(`โหลดข้อมูลไม่สำเร็จ — ตรวจสอบว่า backend รันที่ ${API_BASE}`, 'error', 6000);
939    }
940  }
บรรทัด 912–921: onProvinceChange ล้างตารางสถานที่ แพ็กเกจ และแผนที่เลือก (เพราะ id ของ POI ซ้ำกันข้ามจังหวัด) ซ่อนส่วนแพ็กเกจและรายละเอียด ย้ายแผนที่ไปจังหวัดใหม่ แล้วโหลดสถานที่ (ถูก ➜ frontend/extras.js ห่อเพื่อเปลี่ยนแบนเนอร์และปุ่มจังหวัดข้างเคียง)
บรรทัด 923–928: loadPois ตั้งสถานะ connecting ขอ /api/pois (➜ get_pois() ใน backend/main.py) พร้อมตัวตัดเวลา 5 วินาที
บรรทัด 929–935: ถ้าสำเร็จ เก็บสถานที่ โรงแรม และตารางค้นหาตาม id แล้วแสดงจำนวนในป้ายสถานะ
บรรทัด 936–939: ถ้าล้มเหลว ตั้งสถานะ offline และแจ้งให้ตรวจสอบว่า backend รันอยู่
บรรทัด 945–959  แจ้งเตือน (toast)
945  function showToast(msg, kind = 'ok', duration = 3500) {
946    const container = document.getElementById('toastContainer');
947    const el = document.createElement('div');
948    el.className = `toast ${kind}`;
949    const iconMap = {ok: ICON.check, error: ICON.alert, loading: ICON.spin};
950    el.innerHTML = `<span class="toast-icon">${iconMap[kind] || ICON.check}</span><span>${msg}</span>`;
951    container.appendChild(el);
952    setTimeout(() => {
953      el.style.opacity = '0';
954      el.style.transform = 'translateX(20px)';
955      el.style.transition = 'all 200ms';
956      setTimeout(() => el.remove(), 220);
957    }, duration);
958    return el;
959  }
บรรทัด 945–950: showToast สร้างกล่องแจ้งเตือนตามชนิด (ok error loading) ใส่ไอคอนและข้อความ แล้วต่อเข้าถาด #toastContainer ใน ➜ frontend/index.html (ถูก ➜ frontend/extras.js ห่อเพื่อบันทึกประวัติ)
บรรทัด 952–957: หลังครบเวลา ค่อยเฟดและเลื่อนออกแล้วลบ
บรรทัด 958: คืนองค์ประกอบ ให้ผู้เรียกลบเองได้ (ข้อความ loading)
บรรทัด 965–993  ตรวจข้อมูลที่กรอก
965  const VALIDATION = {
966    budget: { min: 1000,  max: 100000, label: 'งบประมาณ' },
967    days:   { min: 1,     max: 7,      label: 'จำนวนวัน' },
968    travelers: { min: 1,  max: 10,     label: 'จำนวนคน' },
969  };
970
971  function validateInputs(budget, days, travelers) {
972    const errors = [];
973    if (!Number.isFinite(budget) || budget < VALIDATION.budget.min) {
974      errors.push(`${VALIDATION.budget.label}ต้องอย่างน้อย ${fmt(VALIDATION.budget.min)} บาท (ใส่ไว้ ${fmt(budget || 0)} บาท)`);
975    }
976    if (budget > VALIDATION.budget.max) {
977      errors.push(`${VALIDATION.budget.label}สูงสุด ${fmt(VALIDATION.budget.max)} บาท`);
978    }
979    if (days < VALIDATION.days.min || days > VALIDATION.days.max) {
980      errors.push(`${VALIDATION.days.label}ต้องอยู่ระหว่าง ${VALIDATION.days.min}-${VALIDATION.days.max} วัน (ตอนนี้ ${days})`);
981    }
982    if (travelers < VALIDATION.travelers.min || travelers > VALIDATION.travelers.max) {
983      errors.push(`${VALIDATION.travelers.label}ต้อง ${VALIDATION.travelers.min}-${VALIDATION.travelers.max} คน`);
984    }
985    return errors;
986  }
987
988  function highlightField(id, hasError) {
989    const wrapper = document.getElementById(id)?.closest('.input-with-unit, .date-range-input, .counter-control, .select-input');
990    if (wrapper) wrapper.classList.toggle('has-error', hasError);
991    const input = document.getElementById(id);
992    if (input) input.classList.toggle('has-error', hasError);
993  }
บรรทัด 965–969: VALIDATION กฎตรวจฝั่งหน้าเว็บ (งบ 1,000–100,000 จำนวนวัน 1–7 จำนวนคน 1–10) ซึ่งต้องตรงกับ schema Pydantic ของ ➜ create_packages() ใน backend/main.py
บรรทัด 971–986: validateInputs ตรวจงบ จำนวนวัน และจำนวนคน คืนรายการข้อความผิดพลาด (ถูก ➜ frontend/extras.js ห่อเพิ่มกฎจำนวนวันสูงสุดของจังหวัด)
บรรทัด 988–993: highlightField ใส่หรือเอาคลาส has-error ที่ช่องกรอกและกรอบของมัน
บรรทัด 995–1009  เริ่มค้นหา
995  async function searchPackages() {
996    const budget = +document.getElementById('budget').value;
997    const days = getSelectedDays();
998    const travelers = +document.getElementById('travelers').value;
999    // One Day Trip → บังคับไม่รวมโรงแรม
1000    const includeHotel = days === 1 ? false : (document.getElementById('includeHotel')?.checked !== false);
1001
1002    // === Client-side validation FIRST ===
1003    const errors = validateInputs(budget, days, travelers);
1004    highlightField('budget', errors.some(e => e.includes('งบประมาณ')));
1005    highlightField('dateRange', errors.some(e => e.includes('จำนวนวัน')));
1006    if (errors.length > 0) {
1007      showToast(errors[0], 'error', 5000);
1008      return;
1009    }
บรรทัด 995–998: searchPackages (ผูกกับปุ่มค้นหาใน ➜ frontend/index.html) อ่านงบ จำนวนวัน และจำนวนคน
บรรทัด 999–1000: ทริปวันเดียวบังคับไม่รวมโรงแรม ไม่เช่นนั้นอ่านจากช่องติ๊ก
บรรทัด 1002–1005: ตรวจข้อมูลก่อน และไฮไลต์ช่องที่ผิด
บรรทัด 1006–1009: ถ้ามีข้อผิดพลาด แจ้งข้อแรกและหยุด
บรรทัด 1011–1041  เตรียมหน้าจอรอผล
1011    // === Clear previous results ===
1012    if (STATE.map) {
1013      STATE.mapMarkers.forEach(m => STATE.map.removeLayer(m));
1014      STATE.mapPolylines.forEach(p => STATE.map.removeLayer(p));
1015      if (STATE.hotelMarker) STATE.map.removeLayer(STATE.hotelMarker);
1016      STATE.mapMarkers = [];
1017      STATE.mapPolylines = [];
1018      STATE.mapDayLayers = {};
1019      STATE.hotelMarker = null;
1020    }
1021    STATE.packages = [];
1022    STATE.selectedPkg = null;
1023    STATE.selectedIdx = null;
1024    document.getElementById('detailPanel').style.display = 'none';
1025    document.getElementById('dayToggles').innerHTML = '';
1026    document.getElementById('dayPanels').innerHTML = '';
1027
1028    const btn = document.getElementById('searchBtn');
1029    btn.classList.add('loading');
1030    btn.disabled = true;
1031
1032    const sec = document.getElementById('packagesSection');
1033    sec.style.display = 'block';
1034    document.getElementById('metaSummary').textContent = STATE.dev ? `กำลังคำนวณด้วย ${ALGO_NAMES[SELECTED_ALGO]}...` : 'กำลังวางแผนทริป...';
1035    const grid = document.getElementById('packagesRow');
1036    grid.innerHTML = '';
1037    const skTpl = document.getElementById('skeletonTemplate');
1038    for (let i = 0; i < 3; i++) grid.appendChild(skTpl.content.cloneNode(true));
1039    sec.scrollIntoView({behavior: 'smooth', block: 'start'});
1040
1041    const loadingToast = showToast(STATE.dev ? `กำลังเรียก ${ALGO_NAMES[SELECTED_ALGO]} 3 รอบ...` : 'กำลังวางแผนทริป 3 แบบ...', 'loading', 30000);
บรรทัด 1011–1020: ล้างหมุดและเส้นบนแผนที่และตารางต่อวัน (ผลก่อนหน้า)
บรรทัด 1021–1026: ล้างแพ็กเกจ แผนที่เลือก ซ่อนรายละเอียด และล้างตัวสลับวัน/รายการวัน
บรรทัด 1028–1030: ทำให้ปุ่มค้นหาเป็นสถานะกำลังโหลดและกดไม่ได้
บรรทัด 1032–1039: แสดงส่วนแพ็กเกจ ตั้งข้อความสถานะ (โหมด Developer บอกชื่ออัลกอริทึม) ใส่โครงรอโหลด 3 ใบจาก <template> และเลื่อนหน้าลงไป
บรรทัด 1041: แสดงข้อความ loading
บรรทัด 1043–1064  ส่งคำขอสร้างแพ็กเกจ
1043    try {
1044      const res = await fetch(`${API_BASE}/api/packages`, {
1045        method: 'POST',
1046        headers: devHeaders(),
1047        body: JSON.stringify({province: getProvince(), preferences: getPreferences(), budget, days, travelers, seed: Math.floor(Math.random() * 100000), algorithm: STATE.dev ? SELECTED_ALGO : 'hybrid', include_hotel: includeHotel}),
1048      });
1049      if (!res.ok) {
1050        // Parse FastAPI/Pydantic 422 detail
1051        let detail = `HTTP ${res.status}`;
1052        try {
1053          const errData = await res.json();
1054          if (errData.detail && Array.isArray(errData.detail)) {
1055            detail = errData.detail.map(d => {
1056              const field = d.loc ? d.loc[d.loc.length - 1] : '?';
1057              return `${field}: ${d.msg}`;
1058            }).join(' · ');
1059          } else if (errData.detail) {
1060            detail = errData.detail;
1061          }
1062        } catch {}
1063        throw new Error(detail);
1064      }
บรรทัด 1043–1048: ส่ง POST ไป /api/packages (➜ create_packages() ใน backend/main.py) พร้อมจังหวัด ความชอบ งบ วัน คน seed สุ่ม อัลกอริทึม (โหมดปกติบังคับ Hybrid) และตัวเลือกโรงแรม ส่วนหัวมีโทเค็นนักพัฒนา (➜ devHeaders() ใน frontend/app.js) backend จะเรียก ➜ algorithm/hybrid.py (หรืออัลกอริทึมที่เลือกในโหมด Developer)
บรรทัด 1049–1064: ถ้าตอบผิดพลาด อ่านรายละเอียดตามรูปแบบ 422 ของ FastAPI (รายการ field: ข้อความ) หรือข้อความเดี่ยว แล้วโยนข้อผิดพลาด
บรรทัด 1065–1084  ใช้ผลที่ได้
1065      const data = await res.json();
1066      STATE.packages = data.packages;
1067      STATE.includeHotel = includeHotel && !data.packages.every(p => !p.total_hotel_cost);   // งบไม่พอที่พัก: เซิร์ฟเวอร์สร้างแบบไม่รวมโรงแรมให้
1068      (data.packages[0]?.notes || []).forEach(n => showToast(n, 'error', 7000));   // เช่น ร้านอาหารตามความชอบมีไม่พอ
1069      renderPackages();
1070      const totalRuntime = data.packages.reduce((s, p) => s + p.runtime_ms, 0);
1071      document.getElementById('metaSummary').textContent =
1072        `งบ ${fmt(budget)} ฿ · ${days} วัน · ${travelers} คน` + (STATE.dev ? ` · ${ALGO_NAMES[SELECTED_ALGO]} · ${(totalRuntime/1000).toFixed(1)} วินาที` : '');
1073      loadingToast.remove();
1074      showToast(`สร้าง ${data.packages.length} แพ็กเกจสำเร็จ`, 'ok');
1075    } catch (e) {
1076      loadingToast.remove();
1077      showToast(`ผิดพลาด: ${e.message}`, 'error', 6000);
1078      grid.innerHTML = '';
1079      document.getElementById('metaSummary').textContent = '';
1080    } finally {
1081      btn.classList.remove('loading');
1082      btn.disabled = false;
1083    }
1084  }
บรรทัด 1065–1066: เก็บแพ็กเกจที่ได้
บรรทัด 1067: ตั้งธงรวมโรงแรม: ถ้าทุกแพ็กเกจไม่มีค่าโรงแรม แปลว่างบไม่พอและเซิร์ฟเวอร์สร้างแบบไม่รวมโรงแรม
บรรทัด 1068: แสดงหมายเหตุของ backend (เช่น ร้านอาหารตามความชอบไม่พอ)
บรรทัด 1069–1074: วาดการ์ด (➜ renderPackages() ใน frontend/app.js) สรุปเงื่อนไข (และเวลาในโหมด Developer) ลบข้อความ loading และแจ้งสำเร็จ
บรรทัด 1075–1079: ถ้าผิดพลาดแจ้งข้อความ ล้างการ์ด
บรรทัด 1080–1083: คืนปุ่มค้นหาให้กดได้เสมอ
บรรทัด 1089–1122  แสดงการ์ดแพ็กเกจ
1089  function renderPackages() {
1090    const grid = document.getElementById('packagesRow');
1091    grid.innerHTML = '';
1092
1093    const showHotel = STATE.includeHotel !== false;
1094
1095    STATE.packages.forEach((pkg, idx) => {
1096      const card = document.createElement('div');
1097      card.className = `package-card ${pkg.valid ? '' : 'invalid'}`;
1098      card.onclick = () => pkg.valid && selectPackage(idx);
1099      const totalPois = pkg.days.reduce((s, d) => s + d.pois.length, 0);
1100      card.innerHTML = `
1101        <div class="tier-row">
1102          <span class="tier-badge tier-${pkg.tier}">${pkg.tier}</span>
1103          <span class="runtime">${pkg.runtime_ms.toFixed(0)} ms</span>
1104        </div>
1105        ${showHotel
1106          ? `<div class="hotel-name">${CAT_ICON.hotel} ${pkg.hotel.name_en}</div>`
1107          : `<div class="hotel-name no-hotel">${ic('hotel-off')} ไม่รวมที่พัก</div>`}
1108        ${pkg.valid ? `
1109          <div class="score-display">
1110            <span class="score-num">${pkg.total_score}</span>
1111            <span class="score-label"><span class="dev-txt">รวมคะแนน · </span>${totalPois} จุดท่องเที่ยว</span>
1112          </div>
1113          ${showHotel ? `<div class="stat-row"><span class="label">ค่าโรงแรม</span><span class="val">${fmt(pkg.total_hotel_cost)} ฿</span></div>` : ''}
1114          <div class="stat-row"><span class="label">ค่ากิจกรรม</span><span class="val">${fmt(pkg.total_activity_cost)} ฿</span></div>
1115          <div class="stat-row total"><span class="label">รวมทั้งหมด</span><span class="val">${fmt(pkg.total_cost)} ฿</span></div>
1116        ` : `
1117          <div class="invalid-msg">${pkg.violations[0] || 'งบไม่พอสำหรับแพ็กเกจนี้'}</div>
1118        `}
1119      `;
1120      grid.appendChild(card);
1121    });
1122  }
บรรทัด 1089–1093: renderPackages ล้างตาราง และอ่านว่าจะแสดงข้อมูลโรงแรมหรือไม่
บรรทัด 1095–1099: แต่ละแพ็กเกจสร้างการ์ด (ถ้าไม่ผ่านข้อจำกัดเป็นสีเทา) คลิกแล้วเรียก selectPackage เมื่อแพ็กเกจผ่านข้อจำกัด และนับจำนวนสถานที่
บรรทัด 1100–1107: หัวการ์ด: ระดับ (ประหยัด มาตรฐาน พรีเมียม) เวลาคำนวณ และชื่อโรงแรม (หรือ "ไม่รวมที่พัก")
บรรทัด 1108–1115: ถ้าผ่านข้อจำกัด แสดงคะแนน จำนวนจุดท่องเที่ยว ค่าโรงแรม ค่ากิจกรรม และรวมทั้งหมด
บรรทัด 1116–1118: ถ้าไม่ผ่าน แสดงข้อความละเมิดข้อแรก หรือ "งบไม่พอสำหรับแพ็กเกจนี้"
บรรทัด 1120–1121: ต่อการ์ดเข้าตาราง
บรรทัด 1127–1144  เลือกแพ็กเกจ
1127  function selectPackage(idx) {
1128    STATE.selectedPkg = JSON.parse(JSON.stringify(STATE.packages[idx]));
1129    STATE.locked.clear(); STATE.excluded.clear();
1130    STATE.selectedIdx = idx;
1131    document.querySelectorAll('.package-card').forEach((c, i) =>
1132      c.classList.toggle('selected', i === idx)
1133    );
1134    document.getElementById('detailPanel').style.display = 'block';
1135    renderDetail(STATE.selectedPkg);
1136    // CRITICAL: must invalidate size after detail panel becomes visible,
1137    // otherwise map container has 0px and fitBounds fails
1138    setTimeout(() => {
1139      STATE.map.invalidateSize();
1140      drawOnMap(STATE.selectedPkg);
1141      document.getElementById('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
1142      setTimeout(syncMapHeight, 150);
1143    }, 120);
1144  }
บรรทัด 1127–1130: selectPackage ทำสำเนาลึกของแพ็กเกจที่เลือก ล้างชุดล็อกและลบ และจดตำแหน่ง
บรรทัด 1131–1133: ไฮไลต์การ์ดที่เลือก
บรรทัด 1134–1135: แสดงส่วนรายละเอียดและวาดด้วย ➜ renderDetail() ใน frontend/app.js
บรรทัด 1136–1143: ต้องคำนวณขนาดแผนที่ใหม่หลังที่แสดงส่วนรายละเอียด (ไม่เช่นนั้นแผนที่สูง 0 พิกเซลและ fitBounds ล้มเหลว) แล้ววาดเส้นทาง เลื่อนหน้า และปรับความสูงแผนที่
บรรทัด 1149–1238  วาดแผนที่
1149  function drawOnMap(pkg) {
1150    // Clear all old layers
1151    STATE.mapMarkers.forEach(m => STATE.map.removeLayer(m));
1152    STATE.mapPolylines.forEach(p => STATE.map.removeLayer(p));
1153    if (STATE.hotelMarker) STATE.map.removeLayer(STATE.hotelMarker);
1154    STATE.mapMarkers = [];
1155    STATE.mapPolylines = [];
1156    STATE.mapDayLayers = {};
1157
1158    const showHotel = STATE.includeHotel !== false;
1159
1160    // Hotel marker — แสดงเฉพาะเมื่อรวมโรงแรม
1161    if (showHotel) {
1162      const hotelIcon = L.divIcon({
1163        html: `<div class="map-hotel-marker">${ic('hotel')}</div>`,
1164        className: '',
1165        iconSize: [40, 40], iconAnchor: [20, 20],
1166      });
1167      STATE.hotelMarker = L.marker([pkg.hotel.lat, pkg.hotel.lng], {icon: hotelIcon})
1168        .bindPopup(`<b>${pkg.hotel.name_en}</b><br><small>${pkg.hotel.cost} ฿/คืน</small>`)
1169        .addTo(STATE.map);
1170    } else {
1171      STATE.hotelMarker = null;
1172    }
1173
1174    // allLatLngs: รวม hotel ไว้ใน bounds เฉพาะเมื่อรวมโรงแรม
1175    const allLatLngs = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];
1176
1177    pkg.days.forEach((day, dIdx) => {
1178      const color = DAY_COLORS[dIdx % DAY_COLORS.length];
1179      // path: เริ่ม/จบที่โรงแรมเฉพาะเมื่อรวมโรงแรม
1180      const path = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];
1181      const dayMarkers = [];
1182
1183      day.pois.forEach((poi, pIdx) => {
1184        const icon = L.divIcon({
1185          html: `<div class="map-poi-marker" style="--c:${color};">
1186                   <span class="d">${dIdx + 1}</span>
1187                   <span class="p">${pIdx + 1}</span>
1188                 </div>`,
1189          className: '',
1190          iconSize: [36, 36], iconAnchor: [18, 18],
1191        });
1192        const m = L.marker([poi.lat, poi.lng], {icon}).bindPopup(
1193          `<b>${poi.name_th}</b><br>
1194           <small>${poi.name_en}</small><br>
1195           <span style="opacity:0.7;">วันที่ ${dIdx + 1} · ลำดับ ${pIdx + 1}</span><br>
1196           ${STATE.dev ? poi.score + ' คะแนน · ' : ''}${poi.cost} ฿ · ${poi.duration_min} นาที<br>
1197           <a href="#" onclick="showPoiDetail('${poi.id}', ${arriveOf(day, poi)}); return false;">ดูรายละเอียดและรีวิว</a>`
1198        ).addTo(STATE.map);
1199        dayMarkers.push(m);
1200        STATE.mapMarkers.push(m);
1201        path.push([poi.lat, poi.lng]);
1202        allLatLngs.push([poi.lat, poi.lng]);
1203      });
1204
1205      if (showHotel) path.push([pkg.hotel.lat, pkg.hotel.lng]);
1206      const line = L.polyline(path, {
1207        color, weight: 3, opacity: 0.8, dashArray: '6, 8',
1208      }).bindTooltip(`Day ${dIdx + 1}`).addTo(STATE.map);
1209      STATE.mapPolylines.push(line);
1210
1211      // Save layers for this day
1212      STATE.mapDayLayers[dIdx] = {
1213        markers: dayMarkers,
1214        polyline: line,
1215        visible: true,
1216        color,
1217      };
1218    });
1219
1220    // Default: show only day 1, hide the rest
1221    pkg.days.forEach((_, dIdx) => {
1222      if (dIdx === 0) return;
1223      const layer = STATE.mapDayLayers[dIdx];
1224      if (!layer) return;
1225      layer.markers.forEach(m => STATE.map.removeLayer(m));
1226      STATE.map.removeLayer(layer.polyline);
1227      layer.visible = false;
1228    });
1229
1230    renderDayToggles(pkg);
1231
1232    // fitBounds to day 1 only
1233    const day0Latlngs = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];
1234    pkg.days[0].pois.forEach(p => day0Latlngs.push([p.lat, p.lng]));
1235    if (day0Latlngs.length > 1) {
1236      STATE.map.fitBounds(L.latLngBounds(day0Latlngs).pad(0.15));
1237    }
1238  }
บรรทัด 1149–1156: drawOnMap ล้างหมุด เส้น และหมุดโรงแรมเดิม และตารางชั้นต่อวัน (ถูก ➜ frontend/extras.js ห่อให้คงสถานะวันที่เปิดอยู่)
บรรทัด 1158–1172: ถ้ารวมโรงแรม สร้างหมุดโรงแรมรูปเตียงพร้อมป๊อปอัปชื่อและราคาต่อคืน ไม่เช่นนั้นไม่มีหมุด
บรรทัด 1175: เตรียมรายการพิกัดสำหรับจัดมุมมอง (รวมโรงแรมเฉพาะเมื่อรวมโรงแรม)
บรรทัด 1177–1181: แต่ละวัน เลือกสีประจำวัน และเริ่มเส้นทางที่โรงแรม (ถ้ารวมโรงแรม)
บรรทัด 1183–1191: แต่ละสถานที่ สร้างหมุดวงกลมสีของวัน แสดงเลขวันและลำดับ
บรรทัด 1192–1198: ผูกป๊อปอัปแสดงชื่อ ชื่ออังกฤษ วันและลำดับ (โหมด Developer แสดงคะแนนด้วย) ค่าใช้จ่ายและเวลา และลิงก์ไป ➜ showPoiDetail() ใน frontend/app.js
บรรทัด 1199–1202: จดหมุด จุดบนเส้นทาง และพิกัดทั้งหมด
บรรทัด 1205–1209: ปิดเส้นทางกลับโรงแรม แล้ววาดเส้นประสีของวัน
บรรทัด 1211–1217: เก็บชั้นของวันนั้นไว้ใน STATE.mapDayLayers (หมุด เส้น สถานะมองเห็น สี)
บรรทัด 1220–1228: ค่าตั้งต้นแสดงเฉพาะวันที่ 1 ซ่อนวันอื่นโดยถอดจากแผนที่
บรรทัด 1230: วาดปุ่มสลับวัน
บรรทัด 1232–1237: จัดมุมมองให้พอดีกับจุดของวันที่ 1 เว้นขอบ 15%
บรรทัด 1243–1296  ปุ่มสลับแต่ละวัน
1243  function renderDayToggles(pkg) {
1244    const root = document.getElementById('dayToggles');
1245    if (!root) return;
1246
1247    let html = `<button class="day-toggle show-all" onclick="toggleAllDays(true)" title="แสดงทุกวัน">
1248                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
1249                  <span>แสดงทุกวัน</span>
1250                </button>`;
1251    html += `<button class="day-toggle hide-all" onclick="toggleAllDays(false)" title="ซ่อนทุกวัน">
1252               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
1253               <span>ซ่อนทุกวัน</span>
1254             </button>`;
1255    html += `<button class="day-toggle reset-view" onclick="resetMapView()" title="รีเซ็ตตำแหน่ง">
1256               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
1257               <span>รีเซ็ต</span>
1258             </button>`;
1259    html += pkg.days.map((day, dIdx) => {
1260      const color = DAY_COLORS[dIdx % DAY_COLORS.length];
1261      const visible = STATE.mapDayLayers[dIdx] ? STATE.mapDayLayers[dIdx].visible : true;
1262      return `<button class="day-toggle ${visible ? 'active' : ''}"
1263                      style="--c:${color};"
1264                      onclick="toggleDay(${dIdx})">
1265                <span class="day-dot"></span>
1266                <span>วัน ${dIdx + 1} (${day.pois.length})</span>
1267              </button>`;
1268    }).join('');
1269    root.innerHTML = html;
1270  }
1271
1272  function toggleDay(dIdx) {
1273    const layer = STATE.mapDayLayers[dIdx];
1274    if (!layer) return;
1275    layer.visible = !layer.visible;
1276    if (layer.visible) {
1277      layer.markers.forEach(m => m.addTo(STATE.map));
1278      layer.polyline.addTo(STATE.map);
1279    } else {
1280      layer.markers.forEach(m => STATE.map.removeLayer(m));
1281      STATE.map.removeLayer(layer.polyline);
1282    }
1283    renderDayToggles(STATE.selectedPkg);
1284  }
1285
1286  function resetMapView() {
1287    const latlngs = [];
1288    Object.values(STATE.mapDayLayers).forEach(layer => {
1289      if (!layer.visible) return;
1290      layer.markers.forEach(m => latlngs.push(m.getLatLng()));
1291    });
1292    if (STATE.hotelMarker) latlngs.push(STATE.hotelMarker.getLatLng());
1293    if (latlngs.length > 1) {
1294      STATE.map.fitBounds(L.latLngBounds(latlngs).pad(0.15));
1295    }
1296  }
บรรทัด 1243–1245: renderDayToggles หาที่วางปุ่ม #dayToggles ใน ➜ frontend/index.html
บรรทัด 1247–1258: สร้างปุ่ม "แสดงทุกวัน" "ซ่อนทุกวัน" และ "รีเซ็ต"
บรรทัด 1259–1269: สร้างปุ่มของแต่ละวัน (สีและจำนวนจุด) ตามสถานะมองเห็น แล้วใส่ใน DOM
บรรทัด 1272–1284: toggleDay สลับการมองเห็นของวันหนึ่ง (เพิ่มหรือถอดหมุดและเส้นจากแผนที่) แล้ววาดปุ่มใหม่
บรรทัด 1286–1296: resetMapView รวมพิกัดหมุดของวันที่มองเห็นและโรงแรม แล้วปรับมุมมองให้พอดี
บรรทัด 1298–1312  แสดงหรือซ่อนทุกวัน
1298  function toggleAllDays(showAll) {
1299    Object.keys(STATE.mapDayLayers).forEach(k => {
1300      const layer = STATE.mapDayLayers[k];
1301      if (showAll && !layer.visible) {
1302        layer.markers.forEach(m => m.addTo(STATE.map));
1303        layer.polyline.addTo(STATE.map);
1304        layer.visible = true;
1305      } else if (!showAll && layer.visible) {
1306        layer.markers.forEach(m => STATE.map.removeLayer(m));
1307        STATE.map.removeLayer(layer.polyline);
1308        layer.visible = false;
1309      }
1310    });
1311    renderDayToggles(STATE.selectedPkg);
1312  }
บรรทัด 1298–1312: toggleAllDays แสดงหรือซ่อนทุกวันพร้อมกัน เฉพาะวันที่สถานะต่างจากเป้าหมาย แล้ววาดปุ่มใหม่
บรรทัด 1318–1349  จัดขนาดส่วนรายละเอียดให้พอดีจอ
1318  function fitDetail() {
1319    const sec = document.querySelector('.detail-section'), dayList = document.querySelector('.day-list'), grid = document.querySelector('.detail-grid');
1320    if (!sec || !dayList || !grid || sec.offsetParent === null) return;
1321    if (window.innerWidth <= 1000) { sec.style.minHeight = ''; dayList.style.maxHeight = ''; return; }
1322    const GAP = 36;   // ที่ว่างใต้กรอบ ไม่ให้ติดขอบล่างของเบราว์เซอร์
1323    const top = grid.getBoundingClientRect().top - sec.getBoundingClientRect().top;
1324    sec.style.minHeight = window.innerHeight + 'px';
1325    dayList.style.maxHeight = Math.max(360, window.innerHeight - top - GAP) + 'px';
1326    // ย่อการ์ดเท่าที่จำเป็น (ไม่ขยายเกินขนาดปกติ) ให้เห็นครบทุกจุดของวันที่ยาวที่สุดรวมปุ่มเพิ่มสถานที่โดยไม่ต้องเลื่อน
1327    // ลำดับ: บีบระยะห่าง --sp (1→0) ก่อน ถ้ายังไม่พอจึงลดตัวอักษร --fs (1→0.8)
1328    dayList.classList.add('fit');
1329    const need = () => Math.max(...[...dayList.querySelectorAll('.day-panel')].map(p => p.offsetHeight), 0);
1330    const room = dayList.clientHeight, setD = (sp, fs) => { dayList.style.setProperty('--sp', sp); dayList.style.setProperty('--fs', fs); };
1331    const MAXSP = 1.25;   // ที่ว่างที่เหลือ (เช่น จากกล่องฝนที่เล็กลง) ให้การ์ดขยายได้ถึง 1.25 เท่า ตัวอักษรโตสูงสุด 3%
1332    const tryD = (sp, fs = sp > 1 ? 1 + 0.03 * (sp - 1) / (MAXSP - 1) : 1) => { setD(sp.toFixed(3), fs.toFixed(3)); return need() <= room; };
1333    if (!tryD(MAXSP)) {
1334      if (tryD(0)) { let lo = 0, hi = MAXSP; for (let i = 0; i < 8; i++) { const m = (lo + hi) / 2; if (tryD(m)) lo = m; else hi = m; } tryD(lo); }
1335      else { let fs = 1; while (fs > 0.8 && need() > room) { fs -= 0.03; setD(0, fs.toFixed(3)); } }
1336    }
1337  }
1338  window.addEventListener('resize', () => { fitDetail(); syncMapHeight(); });
1339
1340  function syncMapHeight() {
1341    fitDetail();
1342    const dayList = document.querySelector('.day-list');
1343    const mapEl   = document.getElementById('map');
1344    if (!dayList || !mapEl) return;
1345    const listBottom = dayList.getBoundingClientRect().bottom;
1346    const mapTop     = mapEl.getBoundingClientRect().top;
1347    const mapH       = Math.max(listBottom - mapTop, 200);
1348    mapEl.style.height = mapH + 'px';
1349  }
บรรทัด 1318–1320: fitDetail หาองค์ประกอบ ถ้าไม่มีหรือซ่อนอยู่ออก
บรรทัด 1321: บนจอแคบ (ไม่เกิน 1000 พิกเซล) ล้างค่าบังคับความสูงแล้วออก
บรรทัด 1322–1325: คำนวณที่ว่างใต้กรอบ ตั้งความสูงขั้นต่ำเท่าจอ และจำกัดความสูงรายการวัน (ไม่ต่ำกว่า 360)
บรรทัด 1326–1336: ย่อการ์ดเท่าที่จำเป็นให้เห็นครบทุกจุดของวันที่ยาวที่สุด: ตัวแปร CSS --sp (ระยะห่าง 1.25 → 0) ก่อน ถ้ายังไม่พอจึงลด --fs (ขนาดอักษร 1 → 0.8) โดยค้นหาแบบแบ่งครึ่ง 8 รอบ
บรรทัด 1338: เมื่อปรับขนาดหน้าต่าง จัดขนาดและความสูงแผนที่ใหม่
บรรทัด 1340–1349: syncMapHeight จัดรายการวันก่อน แล้วตั้งความสูงแผนที่ให้เท่ารายการวัน (ไม่ต่ำกว่า 200 พิกเซล)
บรรทัด 1352–1446  วาดรายละเอียดแผน
1352  function renderDetail(pkg) {
1353    const showHotel = STATE.includeHotel !== false;
1354    document.getElementById('detailTitle').textContent = showHotel
1355      ? `${pkg.tier} — ${pkg.hotel.name_en}`
1356      : `${pkg.tier} — ไม่รวมที่พัก`;
1357
1358    // KPIs
1359    const totalPois = pkg.days.reduce((s, d) => s + d.pois.length, 0);
1360    document.querySelector('#kpiScore .kpi-val').textContent = pkg.total_score;
1361    document.querySelector('#kpiCost .kpi-val').textContent = `${fmt(pkg.total_activity_cost)} ฿`;
1362    document.querySelector('#kpiPois .kpi-val').textContent = totalPois;
1363
1364    const root = document.getElementById('dayPanels');
1365    root.innerHTML = '';
1366
1367    pkg.days.forEach((day, dIdx) => {
1368      const color = DAY_COLORS[dIdx % DAY_COLORS.length];
1369      const panel = document.createElement('div');
1370      panel.className = 'day-panel';
1371      panel.innerHTML = `
1372        <div class="day-head">
1373          <div class="day-title">
1374            <div class="day-color" style="background:${color};box-shadow:0 0 8px ${color};"></div>
1375            <h3>วันที่ ${dIdx + 1}</h3>
1376          </div>
1377          <div class="day-stats">
1378            <span class="day-score">${ICON.star} ${day.score}</span>
1379            <span>${ICON.coin} ${fmt(day.cost)}</span>
1380            <span>${ICON.clock} ${fmtDur(day.time_min)}</span>
1381            <span>${ICON.route} ${day.distance_km.toFixed(1)}km</span>
1382          </div>
1383        </div>
1384        <ul class="poi-list" id="day-${dIdx}-list"></ul>
1385        <button class="day-add" onclick="addPoiToDay(${dIdx})">
1386          <div class="add-num">${ICON.plus}</div>
1387          <span>เพิ่มสถานที่</span>
1388        </button>
1389      `;
1390      root.appendChild(panel);
1391
1392      const list = panel.querySelector('.poi-list');
1393      if (!day.pois.length) {
1394        list.innerHTML = '<li style="text-align:center;color:var(--text-muted);padding:1rem 0;font-size:0.85rem;">ยังไม่มีจุดในวันนี้</li>';
1395      }
1396      day.pois.forEach((poi, pIdx) => {
1397        // Distance connector before this POI
1398        if (pIdx === 0 && showHotel) {
1399          const distKm = haversineKm(pkg.hotel.lat, pkg.hotel.lng, poi.lat, poi.lng);
1400          const distEl = document.createElement('li');
1401          distEl.className = 'dist-connector';
1402          distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('hotel')} ${ic('arrow-right')} ${distKm.toFixed(1)} km</span><span class="dist-line"></span>`;
1403          list.appendChild(distEl);
1404        } else if (pIdx > 0) {
1405          const prev = day.pois[pIdx - 1];
1406          const distKm = haversineKm(prev.lat, prev.lng, poi.lat, poi.lng);
1407          const distEl = document.createElement('li');
1408          distEl.className = 'dist-connector';
1409          distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('arrow-down')} ${distKm.toFixed(1)} km</span><span class="dist-line"></span>`;
1410          list.appendChild(distEl);
1411        }
1412
1413        const li = document.createElement('li');
1414        li.className = 'poi-item';
1415        li.dataset.id = poi.id;
1416        li.innerHTML = `
1417          <div class="poi-num">${pIdx + 1}</div>
1418          <div class="poi-info">
1419            <div class="poi-name poi-link" onclick="showPoiDetail('${poi.id}', ${arriveOf(day, poi)})" title="ดูรายละเอียดและรีวิว">${CAT_ICON[poi.category] || ''} ${poi.name_th}</div>
1420            <div class="poi-meta">
1421              <span class="pill">${CAT_LABELS[poi.category] || poi.category}</span>
1422              ${arriveOf(day, poi) >= 0 ? `<span class="time-chip"><span class="tc-lbl">ตั้งแต่</span> ${fmtClock(arriveOf(day, poi))}–${fmtClock(arriveOf(day, poi) + (poi.duration_min || 0))} · เปิด ${hoursText(poi)}</span>` : ''}
1423              <span class="score-chip">${ic('star')} ${poi.score}</span>
1424              <span>${poi.cost} ฿</span>
1425              <span class="dur"><span class="dur-lbl">ใช้เวลา</span> ${fmtDur(poi.duration_min)}</span>
1426            </div>
1427          </div>
1428          <div class="poi-actions">
1429            <a class="btn-loc" href="${gmapsUrl(poi)}" target="_blank" rel="noopener" title="ดูใน Google Maps">${ICON.pin}</a>
1430            <button class="btn-swap" onclick="openSwapModal(${dIdx}, ${pIdx})" title="เปลี่ยน">${ICON.swap}</button>
1431            <button class="btn-remove" onclick="removePoi(${dIdx}, ${pIdx})" title="ลบ">${ICON.trash}</button>
1432          </div>
1433        `;
1434        list.appendChild(li);
1435
1436        // Return connector after last POI
1437        if (pIdx === day.pois.length - 1 && showHotel) {
1438          const distKm = haversineKm(poi.lat, poi.lng, pkg.hotel.lat, pkg.hotel.lng);
1439          const distEl = document.createElement('li');
1440          distEl.className = 'dist-connector';
1441          distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('arrow-down')} ${distKm.toFixed(1)} km ${ic('arrow-right')} ${ic('hotel')}</span><span class="dist-line"></span>`;
1442          list.appendChild(distEl);
1443        }
1444      });
1445    });
1446  }
บรรทัด 1352–1356: renderDetail ตั้งหัวเรื่องเป็น "ระดับ — ชื่อโรงแรม" หรือ "ไม่รวมที่พัก" (ถูกห่อโดย ➜ frontend/extras.js และ ➜ frontend/tutorial.js เพื่อเพิ่มพยากรณ์ คำเตือน การลากวาง ประวัติ และวิธีใช้)
บรรทัด 1358–1362: ใส่ตัวเลขสรุป (คะแนน ค่ากิจกรรม จำนวนจุด)
บรรทัด 1364–1365: ล้างรายการวันเดิม
บรรทัด 1367–1370: แต่ละวัน สร้างแผงวัน
บรรทัด 1371–1389: โครงแผง: ชื่อวันที่ สถิติของวัน (คะแนน ค่าใช้จ่าย เวลา ระยะทาง) รายการสถานที่ และปุ่ม "เพิ่มสถานที่" ที่เรียก addPoiToDay
บรรทัด 1390–1395: ต่อแผงเข้าหน้า ถ้าวันนั้นไม่มีจุด แสดงข้อความว่าง
บรรทัด 1396–1403: ก่อนจุดแรก (ถ้ารวมโรงแรม) แทรกป้ายระยะทางจากโรงแรม (haversineKm)
บรรทัด 1404–1411: ก่อนจุดถัด ๆ ไป แทรกป้ายระยะทางจากจุดก่อนหน้า
บรรทัด 1413–1426: สร้างการ์ดสถานที่: เลขลำดับ ชื่อ (คลิกดูรายละเอียด) หมวด เวลา (ตั้งแต่-ถึง และเวลาเปิด-ปิด) คะแนน ราคา และเวลาที่ใช้
บรรทัด 1428–1433: ปุ่มของการ์ด: ลิงก์ Google Maps ปุ่มเปลี่ยน (➜ openSwapModal() ใน frontend/app.js) และปุ่มลบ (➜ removePoi() ใน frontend/app.js) ต่อการ์ดเข้ารายการ
บรรทัด 1436–1443: หลังจุดสุดท้าย (ถ้ารวมโรงแรม) แทรกป้ายระยะทางกลับโรงแรม
บรรทัด 1444–1446: ปิดการวนและฟังก์ชัน
บรรทัด 1451–1476  เปิดหน้าต่างเปลี่ยนหรือเพิ่มสถานที่
1451  function openSwapModal(dayIdx, poiIdx) {
1452    const currentPoi = STATE.selectedPkg.days[dayIdx].pois[poiIdx];
1453    STATE.swapContext = {dayIdx, poiIdx, currentPoi, mode: 'swap', categoryFilter: 'all'};
1454    document.getElementById('swapTitle').textContent = 'เปลี่ยนสถานที่';
1455    document.getElementById('swapCurrentInfo').innerHTML =
1456      `ปัจจุบัน: ${CAT_ICON[currentPoi.category] || ''} ${currentPoi.name_th}`;
1457    document.getElementById('swapFilter').value = '';
1458    renderSwapList();
1459    document.getElementById('swapModal').classList.add('open');
1460    document.body.style.overflow = 'hidden';
1461  }
1462
1463  function addPoiToDay(dayIdx) {
1464    STATE.swapContext = {dayIdx, poiIdx: null, currentPoi: null, mode: 'add', categoryFilter: 'all'};
1465    document.getElementById('swapTitle').textContent = 'เพิ่มจุดใหม่';
1466    document.getElementById('swapCurrentInfo').textContent = `เพิ่มในวันที่ ${dayIdx + 1}`;
1467    document.getElementById('swapFilter').value = '';
1468    renderSwapList();
1469    document.getElementById('swapModal').classList.add('open');
1470    document.body.style.overflow = 'hidden';
1471  }
1472
1473  function setCategoryFilter(cat) {
1474    STATE.swapContext.categoryFilter = cat;
1475    renderSwapList();
1476  }
บรรทัด 1451–1461: openSwapModal (ผูกกับปุ่มเปลี่ยนของการ์ด) จดบริบท: วัน ตำแหน่ง สถานที่ปัจจุบัน โหมด "swap" และตัวกรองหมวด ตั้งหัวเรื่องและบรรทัดข้อมูลปัจจุบัน ล้างช่องค้นหา วาดรายการ (➜ renderSwapList() ใน frontend/app.js) แล้วเปิดโมดัลของ ➜ frontend/index.html
บรรทัด 1463–1471: addPoiToDay ทำเช่นเดียวกันแต่โหมด "add" เพื่อเพิ่มจุดท้ายวัน
บรรทัด 1473–1476: setCategoryFilter เปลี่ยนตัวกรองหมวดและวาดรายการใหม่
บรรทัด 1479–1493  ตัวช่วยรายการสถานที่
1479  function swapRainIcon(p) {
1480    const ctx = STATE.swapContext;
1481    if (!ctx || !window.dayRainPop || window.dayRainPop(ctx.dayIdx) < 60 || !(window.OUTDOOR_CATS || []).includes(p.category)) return '';
1482    const tip = window.WET_LANG === 'en' ? 'Outdoor place, it may rain' : 'สถานที่กลางแจ้ง อาจมีฝนตกได้';
1483    return `<span class="rain-ic" title="${tip}"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 14a4 4 0 0 0 0-8 5.5 5.5 0 0 0-10.6 1.5A3.5 3.5 0 0 0 7 14"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/></svg></span>`;
1484  }
1485
1486  // ลิงก์ Google Maps ค้นหาด้วยชื่อสถานที่ + ชื่อจังหวัด เพื่อให้ปักหมุดที่สถานที่จริงของ Google (ไม่ใช่พิกัดจากข้อมูล OSM ที่อาจเลื่อน)
1487  // ทริปข้ามจังหวัดใช้จังหวัดที่ใกล้จุดนั้นที่สุด; ถ้าไม่มีชื่อไทยใช้ชื่ออังกฤษ
1488  function gmapsUrl(p) {
1489    const provs = getProvince().split('+').map(s => STATE.provinces[s]).filter(Boolean);
1490    const near = provs.slice().sort((a, b) => haversineKm(p.lat, p.lng, ...(a.center || [p.lat, p.lng])) - haversineKm(p.lat, p.lng, ...(b.center || [p.lat, p.lng])))[0];
1491    const q = [p.name_th || p.name_en, near?.name_th].filter(Boolean).join(' ');
1492    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`;
1493  }
บรรทัด 1479–1484: swapRainIcon ถ้าวันนั้นโอกาสฝน ≥ 60% (dayRainPop จาก ➜ frontend/extras.js) และสถานที่เป็นกลางแจ้ง คืนไอคอนฝนพร้อม tooltip สองภาษา ไม่เช่นนั้นคืนข้อความว่าง
บรรทัด 1486–1493: gmapsUrl สร้างลิงก์ค้นหาใน Google Maps ด้วยชื่อสถานที่ผนวกชื่อจังหวัดที่ใกล้ที่สุด (กรณีทริปข้ามจังหวัด) เพื่อปักหมุดที่สถานที่จริง
บรรทัด 1495–1542  วาดรายการสถานที่ให้เลือก
1495  function renderSwapList() {
1496    const ctx = STATE.swapContext;
1497    const usedIds = new Set();
1498    STATE.selectedPkg.days.forEach(d => d.pois.forEach(p => usedIds.add(p.id)));
1499    const all = STATE.pois.filter(p => !usedIds.has(p.id));
1500
1501    const counts = {all: all.length};
1502    all.forEach(p => { counts[p.category] = (counts[p.category] || 0) + 1; });
1503
1504    const filterCat = ctx.categoryFilter || 'all';
1505    const candidates = (filterCat === 'all' ? all : all.filter(p => p.category === filterCat))
1506      .sort((a, b) => b.score - a.score);
1507
1508    const cats = ['all', 'beach', 'temple', 'viewpoint', 'culture', 'market', 'activity', 'restaurant'];
1509    const filterButtons = cats
1510      .filter(c => counts[c])
1511          .map(c => `<button class="cat-btn ${c === filterCat ? 'active' : ''}" onclick="setCategoryFilter('${c}')">
1512                   ${c === 'all' ? '' : CAT_ICON[c] + ' '}${CAT_LABELS[c]} <span style="opacity:0.7">${counts[c]}</span>
1513                 </button>`).join('');
1514
1515    const list = document.getElementById('swapList');
1516    list.innerHTML = `
1517      <div class="cat-filter">${filterButtons}</div>
1518      ${candidates.length === 0
1519        ? '<div class="empty-msg">ไม่มีจุดที่ตรงเงื่อนไข</div>'
1520        : candidates.map(p => `
1521          <div class="swap-option" onclick="confirmSwap('${p.id}')">
1522            <div class="opt-info">
1523              <b>${CAT_ICON[p.category] || ''} ${p.name_th}${swapRainIcon(p)}</b>
1524              <span class="meta">${CAT_LABELS[p.category]} · ${p.cost} ฿ · ${p.duration_min} นาที</span>
1525              <span class="meta">เปิด-ปิด ${hoursText(p)}</span>
1526            </div>
1527            <div class="opt-actions">
1528              <button type="button" class="opt-btn" title="ดูรีวิว" onclick="event.stopPropagation(); showPoiDetail('${p.id}', -1)"><svg class="ic" viewBox="0 0 24 24"><use href="#i-star"/></svg></button>
1529              <a class="opt-btn" title="ดูใน Google Maps" target="_blank" rel="noopener" href="${gmapsUrl(p)}" onclick="event.stopPropagation()"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></a>
1530            </div>
1531          </div>
1532        `).join('')
1533      }
1534    `;
1535  }
1536
1537  function filterSwapList() {
1538    const q = document.getElementById('swapFilter').value.toLowerCase();
1539    document.querySelectorAll('.swap-option').forEach(el => {
1540      el.style.display = el.textContent.toLowerCase().includes(q) ? 'flex' : 'none';
1541    });
1542  }
บรรทัด 1495–1499: renderSwapList หาสถานที่ที่ยังไม่อยู่ในแผน
บรรทัด 1501–1502: นับจำนวนต่อหมวด
บรรทัด 1504–1506: กรองตามหมวดที่เลือก แล้วเรียงตามคะแนนมากไปน้อย
บรรทัด 1508–1513: สร้างปุ่มกรองหมวด (เฉพาะหมวดที่มีสถานที่) พร้อมจำนวน
บรรทัด 1515–1534: ใส่ตัวกรองและรายการ ถ้าไม่มีแสดงข้อความ ไม่เช่นนั้นแต่ละตัวเลือกแสดงชื่อ (พร้อมไอคอนฝน) หมวด ราคา เวลาที่ใช้ เวลาเปิด-ปิด ปุ่มดูรีวิว และลิงก์ Google Maps คลิกที่ตัวเลือกเรียก confirmSwap
บรรทัด 1537–1542: filterSwapList (ผูกกับช่องค้นหาใน ➜ frontend/index.html) ซ่อนตัวเลือกที่ข้อความไม่ตรงคำค้น
บรรทัด 1546–1576  ยืนยันสลับ เพิ่ม ลบ
1546  function snapshotEdit() { return {days: STATE.selectedPkg.days.map(d => d.pois.slice()), locked: new Set(STATE.locked), excluded: new Set(STATE.excluded)}; }
1547  function restoreEdit(sn) { STATE.selectedPkg.days.forEach((d, i) => { d.pois = sn.days[i].slice(); }); STATE.locked = sn.locked; STATE.excluded = sn.excluded; }
1548
1549  async function confirmSwap(newPoiId) {
1550    const ctx = STATE.swapContext;
1551    const newPoi = STATE.poisById[newPoiId];
1552    const sn = snapshotEdit();
1553    if (ctx.mode === 'swap') {
1554      STATE.selectedPkg.days[ctx.dayIdx].pois[ctx.poiIdx] = newPoi;
1555    } else {
1556      STATE.selectedPkg.days[ctx.dayIdx].pois.push(newPoi);
1557    }
1558    STATE.locked.add(newPoiId);
1559    STATE.excluded.delete(newPoiId);
1560    closeSwapModal();
1561    await recomputeAndRefresh(() => restoreEdit(sn));
1562  }
1563
1564  function removePoi(dayIdx, poiIdx) {
1565    const sn = snapshotEdit();
1566    const [removed] = STATE.selectedPkg.days[dayIdx].pois.splice(poiIdx, 1);
1567    STATE.locked.delete(removed.id);
1568    STATE.excluded.add(removed.id);
1569    recomputeAndRefresh(() => restoreEdit(sn));
1570  }
1571
1572  function closeSwapModal() {
1573    document.getElementById('swapModal').classList.remove('open');
1574    document.body.style.overflow = '';
1575    STATE.swapContext = null;
1576  }
บรรทัด 1544–1545: คอมเมนต์: การเพิ่ม สลับ ลบ ทำตามที่ผู้ใช้สั่งตรง ๆ แล้วให้ backend คำนวณเวลาและค่าใช้จ่ายใหม่ (เดิมเรียก Hybrid ทุกครั้ง ซึ่งทำให้สถานที่อื่นหายเมื่อเพิ่มกิจกรรมยาว)
บรรทัด 1546–1547: snapshotEdit และ restoreEdit จำและคืนลำดับสถานที่ ชุดล็อก และชุดลบ เพื่อย้อนกลับเมื่อ backend ล้มเหลว
บรรทัด 1549–1562: confirmSwap หาสถานที่ใหม่ จำสถานะ แทนที่หรือต่อท้ายวัน ใส่ในชุดล็อก เอาออกจากชุดลบ ปิดโมดัล แล้วเรียก recomputeAndRefresh
บรรทัด 1564–1570: removePoi จำสถานะ ตัดจุดออก เอาออกจากชุดล็อกใส่ในชุดลบ (ห้าม reoptimize ใส่กลับ) แล้วคำนวณใหม่
บรรทัด 1572–1576: closeSwapModal ปิดโมดัล คืนการเลื่อน และล้างบริบท
บรรทัด 1581–1660  สุ่มแพ็กเกจใหม่
1581  async function reshufflePackage() {
1582    if (!STATE.selectedPkg) return;
1583    const targetTier = STATE.selectedPkg.tier;
1584
1585    const budget    = +document.getElementById('budget').value;
1586    const days      = getSelectedDays();
1587    const travelers = +document.getElementById('travelers').value;
1588    const includeHotel = days === 1 ? false : (document.getElementById('includeHotel')?.checked !== false);
1589
1590    const detailEl = document.getElementById('detailPanel');
1591    // Inject animated overlay
1592    const overlay = document.createElement('div');
1593    overlay.id = 'reshuffleOverlay';
1594    overlay.innerHTML = `<div class="reshuffle-overlay-inner">
1595      <svg class="reshuffle-ring" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
1596        <circle cx="25" cy="25" r="20" stroke="rgba(34,211,238,0.25)" stroke-width="3"/>
1597        <circle cx="25" cy="25" r="20" stroke="#22d3ee" stroke-width="3" stroke-dasharray="40 90" stroke-linecap="round"/>
1598      </svg>
1599      <span>กำลังสุ่มสถานที่ใหม่...</span>
1600    </div>`;
1601    detailEl.appendChild(overlay);
1602    detailEl.classList.add('reshuffling');
1603    const t = showToast('กำลังสุ่มสถานที่ใหม่...', 'loading', 30000);
1604
1605    try {
1606      const ctrl = new AbortController();
1607      const timer = setTimeout(() => ctrl.abort(), 25000);
1608      const res = await fetch(`${API_BASE}/api/packages`, {
1609        method: 'POST',
1610        headers: devHeaders(),
1611        body: JSON.stringify({
1612          province: getProvince(),
1613          preferences: getPreferences(),
1614          budget, days, travelers,
1615          seed: Math.floor(Math.random() * 1000000),
1616          algorithm: STATE.dev ? SELECTED_ALGO : 'hybrid',
1617          include_hotel: includeHotel,
1618        }),
1619        signal: ctrl.signal,
1620      });
1621      clearTimeout(timer);
1622      if (!res.ok) throw new Error(`HTTP ${res.status}`);
1623      const data = await res.json();
1624
1625      // Update global package list
1626      STATE.packages = data.packages;
1627      STATE.includeHotel = includeHotel && !data.packages.every(p => !p.total_hotel_cost);   // งบไม่พอที่พัก: เซิร์ฟเวอร์สร้างแบบไม่รวมโรงแรมให้
1628
1629      // Find the matching tier (or fall back to same index)
1630      const tierIdx = data.packages.findIndex(p => p.tier === targetTier);
1631      const newIdx  = tierIdx >= 0 ? tierIdx : STATE.selectedIdx;
1632      STATE.selectedIdx = newIdx;
1633      STATE.selectedPkg = JSON.parse(JSON.stringify(data.packages[newIdx]));
1634      STATE.locked.clear(); STATE.excluded.clear();
1635      setTimeout(pushSession, 600);
1636
1637      // Refresh package cards without clearing detail section
1638      renderPackages();
1639      document.querySelectorAll('.package-card').forEach((c, i) =>
1640        c.classList.toggle('selected', i === newIdx)
1641      );
1642
1643      // Update detail in-place
1644      renderDetail(STATE.selectedPkg);
1645      setTimeout(() => {
1646        STATE.map.invalidateSize();
1647        drawOnMap(STATE.selectedPkg);
1648        setTimeout(syncMapHeight, 100);
1649      }, 80);
1650
1651      t.remove();
1652      showToast(STATE.dev ? `สุ่มใหม่แล้ว! Score ${STATE.selectedPkg.total_score}` : 'สุ่มใหม่แล้ว!', 'ok');
1653    } catch (e) {
1654      t.remove();
1655      showToast(`ผิดพลาด: ${e.message}`, 'error');
1656    } finally {
1657      detailEl.classList.remove('reshuffling');
1658      document.getElementById('reshuffleOverlay')?.remove();
1659    }
1660  }
บรรทัด 1581–1583: reshufflePackage (ผูกกับปุ่ม Re-shuffle) จำระดับของแพ็กเกจที่เลือก
บรรทัด 1585–1588: อ่านงบ วัน คน และตัวเลือกโรงแรมจากฟอร์ม
บรรทัด 1590–1603: ใส่ overlay หมุนทับส่วนรายละเอียด และแสดงข้อความ loading
บรรทัด 1605–1620: ตั้งตัวตัดเวลา 25 วินาที แล้วส่ง POST ไป /api/packages (➜ create_packages() ใน backend/main.py) ด้วย seed ใหม่ และอัลกอริทึมเดิม
บรรทัด 1621–1623: ตรวจผลและอ่านข้อมูล
บรรทัด 1626–1627: ตั้งรายการแพ็กเกจใหม่และธงรวมโรงแรม
บรรทัด 1629–1635: หาแพ็กเกจระดับเดียวกัน (ไม่มีใช้ตำแหน่งเดิม) ทำสำเนา ล้างชุดล็อกและลบ และส่งขึ้นเซสชันหลัง 0.6 วินาที (➜ pushSession() ใน frontend/app.js)
บรรทัด 1637–1644: วาดการ์ดแพ็กเกจใหม่โดยไม่ล้างส่วนรายละเอียด ไฮไลต์ใบที่เลือก และวาดรายละเอียด
บรรทัด 1645–1649: หลังหน่วงเล็กน้อย คำนวณขนาดและวาดแผนที่ใหม่
บรรทัด 1651–1652: ลบข้อความ loading และแจ้งผล
บรรทัด 1653–1659: ถ้าผิดพลาดแจ้งข้อความ และไม่ว่าอย่างไรเอา overlay ออก
บรรทัด 1662–1696  คำนวณใหม่หลังแก้
1662  async function recomputeAndRefresh(rollback) {
1663    const t = showToast('กำลังคำนวณเส้นทางใหม่...', 'loading', 10000);
1664    try {
1665      const routes = STATE.selectedPkg.days.map(d => d.pois.map(p => p.id));
1666      const res = await fetch(`${API_BASE}/api/recompute`, {
1667        method: 'POST',
1668        headers: {'Content-Type': 'application/json'},
1669        body: JSON.stringify({
1670          province: getProvince(),
1671          hotel_id: STATE.selectedPkg.hotel.id,
1672          days: STATE.selectedPkg.days.length,
1673          budget: 100000,
1674          routes,
1675          travelers: +document.getElementById('travelers').value,
1676        }),
1677      });
1678      if (!res.ok) throw new Error(`HTTP ${res.status}`);
1679      const data = await res.json();
1680      data._base = STATE.selectedPkg._base;   // คำเตือนตั้งต้นของแผนเดิม
1681      if (STATE.selectedPkg._orig) setHidden(data, '_orig', STATE.selectedPkg._orig);   // แผนตั้งต้นสำหรับปุ่มคืนค่าเดิม
1682      STATE.selectedPkg = data;
1683      drawOnMap(data);
1684      renderDetail(data);
1685      t.remove();
1686      if (uiWarnings(data).length) {
1687        showToast(`อัปเดตแล้ว · ${uiWarnings(data).length} คำเตือน (ดูการ์ดสีแดง)`, 'error', 5000);
1688      } else {
1689        showToast((STATE.dev ? `อัปเดต! Score ${data.total_score}` : 'อัปเดตแผนแล้ว'), 'ok');
1690      }
1691    } catch (e) {
1692      t.remove();
1693      if (rollback) { rollback(); drawOnMap(STATE.selectedPkg); renderDetail(STATE.selectedPkg); }   // คืนแผนเดิม ไม่ให้หมุด/การ์ดค้างผิดที่
1694      showToast(`ผิดพลาด: ${e.message}${rollback ? ' (คืนแผนเดิมแล้ว)' : ''}`, 'error');
1695    }
1696  }
บรรทัด 1662–1665: recomputeAndRefresh (ฟังก์ชันที่ ➜ moveStop() ใน frontend/extras.js และการลาก/สลับเรียกใช้) รับฟังก์ชัน rollback สำหรับคืนค่า แล้วรวบรวมเส้นทางของแต่ละวัน
บรรทัด 1666–1677: ส่ง POST ไป /api/recompute (➜ recompute() ใน backend/main.py) พร้อมจังหวัด โรงแรม วัน งบ (ตั้ง 100,000 เพื่อไม่ให้งบตัดจุดที่ผู้ใช้เลือก) เส้นทาง และจำนวนคน ฝั่ง backend คำนวณเวลาถึง ค่าใช้จ่าย และระยะทางตามลำดับที่ผู้ใช้กำหนด
บรรทัด 1678–1682: ตรวจผล ส่งต่อคำเตือนตั้งต้นและแผนตั้งต้น (ซ่อนจาก JSON) แล้วตั้งเป็นแผนที่เลือก
บรรทัด 1683–1690: วาดแผนที่และรายละเอียด ลบข้อความ loading และแจ้งผล (ถ้ามีคำเตือนเป็นสีแดงให้ดูการ์ดสีแดง)
บรรทัด 1691–1695: ถ้าผิดพลาด เรียก rollback คืนแผนเดิมแล้ววาดใหม่ และแจ้งข้อผิดพลาด
บรรทัด 1701–1713  ฟังก์ชันเบ็ดเตล็ด
1701  function fmt(n) { return Math.round(n).toLocaleString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH')); }
1702
1703  function haversineKm(lat1, lng1, lat2, lng2) {
1704    const R = 6371, dLat = (lat2-lat1)*Math.PI/180, dLng = (lng2-lng1)*Math.PI/180;
1705    const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLng/2)**2;
1706    // × road_factor ของจังหวัด (จาก /api/provinces) ให้ตรงกับระยะที่ backend ใช้คำนวณเวลาและค่าเดินทาง
1707    return R * 2 * Math.asin(Math.sqrt(a)) * (STATE.provinces[getProvince()]?.road_factor || 1);
1708  }
1709
1710
1711  document.addEventListener('keydown', e => {
1712    if (e.key === 'Escape') closeSwapModal();
1713  });
บรรทัด 1701: fmt จัดรูปตัวเลขตามภาษา (ไทยหรืออังกฤษ ตาม WET_LANG ของ ➜ frontend/i18n.js)
บรรทัด 1703–1708: haversineKm คำนวณระยะทางบนผิวโลกด้วยสูตร haversine (รัศมี 6371 กม.) คูณ road_factor ของจังหวัดที่ ➜ data/calibrate_travel.py ปรับเทียบไว้ ให้ตรงกับระยะที่ backend ใช้คำนวณเวลาเดินทางและค่าเดินทาง
บรรทัด 1711–1713: กด Esc เพื่อปิดหน้าต่างเปลี่ยนสถานที่

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