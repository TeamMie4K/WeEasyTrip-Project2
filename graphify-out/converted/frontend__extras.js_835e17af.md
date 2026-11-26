<!-- converted from frontend__extras.js.docx -->

คู่มือโค้ด: frontend/extras.js
ส่วนเสริมของหน้าเว็บ: จังหวัดข้างเคียง อากาศ ลากวาง Tips แผนที่บันทึก
ไฟล์ต้นฉบับ: frontend/extras.js (679 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ไฟล์ที่โหลดต่อจาก ➜ frontend/app.js และ "ห่อ" (wrap) ฟังก์ชันของ app.js โดยเก็บฟังก์ชันเดิมไว้ในตัวแปร orig... แล้วกำหนดฟังก์ชันใหม่ทับ ที่เรียกของเดิมก่อนแล้วเพิ่มงานของตัวเอง (เช่น ➜ onProvinceChange() ใน frontend/app.js ➜ renderDetail() ใน frontend/app.js ➜ drawOnMap() ใน frontend/app.js ➜ validateInputs() ใน frontend/app.js) จึงต้องมีตัวแปรกลางของ app.js เช่น STATE DATE_PICKER SELECTED_DAYS ฟีเจอร์ในไฟล์: ทริปข้ามจังหวัด แบนเนอร์จังหวัด จำกัดจำนวนวัน หมายเหตุฤดูกาล พยากรณ์อากาศจริง ลากวางการ์ดแบบ pointer สลับสถานที่ในร่ม กล่อง Tips บันทึกและเปิดแผน เทียบอัลกอริทึม ล็อกโหมด Developer ด้วยรหัสผ่าน และประวัติการแจ้งเตือน ไฟล์ใช้องค์ประกอบจาก ➜ frontend/index.html (เช่น #dateSummary #provSelect .detail-actions) และสไตล์จาก ➜ frontend/style.css ข้อความภาษาอังกฤษของ Tips เป็นของไฟล์นี้เอง ส่วนข้อความอื่นแปลโดย ➜ frontend/i18n.js

บรรทัด 3–10  หัวไฟล์ และตัวช่วย
3  (function () {
4    const $ = id => document.getElementById(id);
5    const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
6    const store = {
7      get() { try { return JSON.parse(localStorage.getItem('wet_saved') || '[]'); } catch (e) { return []; } },
8      set(v) { try { localStorage.setItem('wet_saved', JSON.stringify(v)); return true; } catch (e) { return false; } },
9    };
10    let baseSlug = null;
บรรทัด 3: เปิด IIFE แรก (ไฟล์มี IIFE สองก้อน ก้อนที่สองเริ่มที่บรรทัด 632)
บรรทัด 4: $ ย่อ getElementById
บรรทัด 5: esc ป้องกัน XSS โดยแปลงอักขระพิเศษ HTML (& < > ") ก่อนนำข้อความไปใส่ innerHTML
บรรทัด 6–9: store อ่าน/เขียนรายการแผนที่บันทึกใน localStorage คีย์ wet_saved ถ้าผิดพลาด (เช่นโหมดส่วนตัว) คืนรายการว่างหรือ false
บรรทัด 10: baseSlug จังหวัดหลักที่ผู้ใช้เลือก (ไม่รวมจังหวัดข้างเคียงที่ต่อท้าย)
บรรทัด 12–22  สร้างจังหวัดแบบรวม
12    // ---------- จังหวัดข้างเคียง (ทริปข้ามจังหวัด) ----------
13    const nameOf = s => STATE.provinces[s]?.name_th || s;
14    function registerCombo(slug) {
15      if (!slug.includes('+') || STATE.provinces[slug]) return;
16      const ps = slug.split('+').map(s => STATE.provinces[s]);
17      STATE.provinces[slug] = {
18        ...ps[0], name_th: slug.split('+').map(nameOf).join(' + '),
19        center: [0, 1].map(i => ps.reduce((a, p) => a + p.center[i], 0) / ps.length),
20        zoom: Math.max(8, ps[0].zoom - 2), max_days: Math.min(7, ps.reduce((a, p) => a + p.max_days, 0)),
21      };
22    }
บรรทัด 13: nameOf ชื่อไทยของ slug (ไม่มีใช้ slug เอง)
บรรทัด 14–16: registerCombo สำหรับ slug แบบรวมที่มี "+" เช่น phuket+krabi และยังไม่เคยลงทะเบียน ดึงข้อมูลจังหวัดย่อยแต่ละตัว
บรรทัด 17–21: สร้างรายการจังหวัดรวมใน STATE.provinces: ใช้ข้อมูลของจังหวัดแรกเป็นฐาน ชื่อต่อด้วย " + " จุดกลางแผนที่เป็นค่าเฉลี่ยพิกัด ซูมถอยออก 2 ระดับ (ไม่ต่ำกว่า 8) และจำนวนวันสูงสุดเป็นผลรวม (ไม่เกิน 7)
บรรทัด 24–38  ปุ่มจังหวัดข้างเคียง
24    function renderNeighbors() {
25      let row = $('neighborRow');
26      if (!row) { $('provSelect').insertAdjacentHTML('afterend', '<div id="neighborRow" class="neighbor-row"></div>'); row = $('neighborRow'); }
27      const pv = STATE.provinces[baseSlug];
28      if (!pv || !pv.neighbors?.length) { row.innerHTML = ''; return; }
29      const cur = getProvince().split('+');
30      row.innerHTML = '<span class="neighbor-label">เที่ยวต่อจังหวัดข้างเคียง:</span>' + pv.neighbors.map(n =>
31        `<button type="button" class="neighbor-chip${cur.includes(n) ? ' on' : ''}" data-slug="${n}" aria-pressed="${cur.includes(n)}">${esc(nameOf(n))}</button>`).join('');
32      row.querySelectorAll('button').forEach(b => b.onclick = () => {
33        const on = b.classList.toggle('on');
34        b.setAttribute('aria-pressed', String(on));
35        const picked = [...row.querySelectorAll('button.on')].map(x => x.dataset.slug).slice(0, 2);   // รวมกันไม่เกิน 3 จังหวัด
36        applyProvince([baseSlug, ...picked].join('+'));
37      });
38    }
บรรทัด 24–26: renderNeighbors หาแถว #neighborRow ถ้ายังไม่มีสร้างต่อจาก #provSelect ใน ➜ frontend/index.html
บรรทัด 27–28: ถ้าจังหวัดฐานไม่มีรายการจังหวัดข้างเคียง ล้างแถวแล้วออก
บรรทัด 29–31: อ่านจังหวัดที่เลือกอยู่ (getProvince ของ app.js) แล้วสร้างปุ่มชิปของแต่ละจังหวัดข้างเคียง ปุ่มที่เลือกอยู่จะเป็น on
บรรทัด 32–34: เมื่อคลิก สลับสถานะ on และ aria-pressed
บรรทัด 35: รวบรวมปุ่มที่เลือก จำกัดไม่เกิน 2 จังหวัดเพิ่ม (รวมกันไม่เกิน 3 จังหวัด)
บรรทัด 36: เรียก applyProvince ด้วย slug ที่ต่อด้วย "+"
บรรทัด 40–45  ใช้จังหวัดที่เลือก
40    function applyProvince(slug) {
41      registerCombo(slug);
42      $('province').value = slug;
43      $('provName').textContent = slug.split('+').map(nameOf).join(' + ');
44      onProvinceChange(slug);
45    }
บรรทัด 40–45: applyProvince ลงทะเบียนจังหวัดรวม ตั้งค่าช่องซ่อน #province และชื่อที่แสดง แล้วเรียก ➜ onProvinceChange() ใน frontend/app.js ให้โหลดข้อมูลใหม่
บรรทัด 47–61  แบนเนอร์จังหวัด
47    // แบนเนอร์ประจำจังหวัด: ใช้ img/provinces/<slug>.jpg (ภาพถ่ายถ้ามี) ไม่งั้นใช้ .svg ที่สร้างอัตโนมัติ; สลับด้วย cross-fade
48    let bannerSlug = 'phuket';
49    function setBanner(slug) {
50      const base = slug.split('+')[0]; if (base === bannerSlug) return; bannerSlug = base;
51      const hero = document.querySelector('.hero-visual'), old = hero?.querySelector('.hero-bg'); if (!hero || !old) return;
52      const cands = base === 'phuket' ? ['BG2.jpg'] : [`img/provinces/${base}.jpg`, `img/provinces/${base}.svg`];
53      const apply = url => {
54        if (bannerSlug !== base) return;   // ผู้ใช้เปลี่ยนจังหวัดไปแล้ว
55        const nu = document.createElement('div'); nu.className = 'hero-bg'; nu.style.backgroundImage = `url('${url}')`; nu.style.opacity = '0';
56        old.after(nu); requestAnimationFrame(() => requestAnimationFrame(() => { nu.style.opacity = '1'; }));
57        setTimeout(() => hero.querySelectorAll('.hero-bg').forEach(e => { if (e !== nu) e.remove(); }), 700);
58      };
59      (function tryNext(i) { if (i >= cands.length) return; const im = new Image(); im.onload = () => apply(cands[i]); im.onerror = () => tryNext(i + 1); im.src = cands[i]; })(0);
60      const lbl = document.querySelector('.hero-label'); if (lbl) lbl.textContent = (STATE.provinces[base]?.name_en || 'Your Travel Services');
61    }
บรรทัด 47–48: คอมเมนต์และตัวแปรจังหวัดของแบนเนอร์ปัจจุบัน (ตั้งต้นภูเก็ต) ภาพมาจาก img/provinces ที่สร้างโดย ➜ data/make_banners.py
บรรทัด 49–50: setBanner ใช้จังหวัดแรกของ slug รวม ถ้าเป็นจังหวัดเดิมไม่ทำอะไร
บรรทัด 51: หา hero และภาพเดิม ถ้าไม่มีก็ออก
บรรทัด 52: รายการภาพที่ลอง: ภูเก็ตใช้ BG2.jpg จังหวัดอื่นลอง .jpg ก่อน แล้ว .svg
บรรทัด 53–58: apply สร้างชั้นภาพใหม่โปร่งใส ต่อท้ายภาพเดิม ค่อยเฟดเข้า และลบภาพเก่าหลัง 0.7 วินาที (ข้ามถ้าผู้ใช้เปลี่ยนจังหวัดไปแล้ว)
บรรทัด 59: ลองโหลดภาพตามลำดับ ถ้าโหลดไม่ได้ลองภาพถัดไป
บรรทัด 60: เปลี่ยนป้ายเล็กบนภาพเป็นชื่ออังกฤษของจังหวัด
บรรทัด 63–80  ห่อฟังก์ชันโหลดจังหวัด
63    const origProvinceChange = onProvinceChange;
64    onProvinceChange = async function (slug) {
65      setBanner(slug);
66      if (!slug.includes('+')) baseSlug = slug;
67      else baseSlug = slug.split('+')[0];
68      registerCombo(slug);
69      await origProvinceChange(slug);
70      renderNeighbors();
71      updateHint();
72    };
73
74    const origLoadProvinces = loadProvinces;
75    loadProvinces = async function () {
76      await origLoadProvinces();
77      baseSlug = getProvince().split('+')[0];
78      renderNeighbors();
79      updateHint();
80    };
บรรทัด 63–72: ห่อ ➜ onProvinceChange() ใน frontend/app.js: ตั้งแบนเนอร์ จดจังหวัดฐาน ลงทะเบียนจังหวัดรวม เรียกของเดิมรอให้เสร็จ แล้ววาดปุ่มจังหวัดข้างเคียงและข้อความ hint
บรรทัด 74–80: ห่อ ➜ loadProvinces() ใน frontend/app.js: หลังโหลดรายการจังหวัดจาก ➜ get_provinces() ใน backend/main.py เสร็จ ตั้งจังหวัดฐานและวาดปุ่มและ hint
บรรทัด 82–90  จำกัดจำนวนวัน
82    // ---------- จำกัดจำนวนวันตามข้อมูล + หมายเหตุฤดูกาล ----------
83    const maxDays = () => STATE.provinces[getProvince()]?.max_days || 7;
84
85    const origValidate = validateInputs;
86    validateInputs = function (budget, days, travelers) {
87      const errs = origValidate(budget, days, travelers);
88      if (days > maxDays()) errs.push(`ข้อมูลของ ${nameOf(getProvince())} รองรับสูงสุด ${maxDays()} วัน (สถานที่หรือร้านอาหารไม่พอสำหรับ ${days} วัน) ลองลดจำนวนวันหรือเพิ่มจังหวัดข้างเคียง`);
89      return errs;
90    };
บรรทัด 83: maxDays จำนวนวันสูงสุดตามข้อมูลของจังหวัดที่เลือก (ไม่ทราบใช้ 7)
บรรทัด 85–90: ห่อ ➜ validateInputs() ใน frontend/app.js: เรียกของเดิมแล้วถ้าจำนวนวันเกิน เพิ่มข้อความข้อผิดพลาดบอกว่าข้อมูลของจังหวัดนั้นรองรับกี่วัน
บรรทัด 92–111  หมายเหตุฤดูกาล
92    const ANDAMAN = ['phuket', 'krabi', 'phangnga', 'ranong', 'trang', 'satun'];
93    const GULF_SOUTH = ['suratthani', 'samui', 'nakhonsithammarat', 'chumphon', 'songkhla', 'pattani', 'yala', 'narathiwat', 'phatthalung'];
94    // ข้อมูลภูมิอากาศทั่วไปตามเดือน (คงที่ ไม่ใช่พยากรณ์อากาศ)
95    function seasonNote(slug, month) {   // month 1-12
96      const s = slug.split('+')[0], region = STATE.provinces[s]?.region || '';
97      const notes = [];
98      if (ANDAMAN.includes(s)) {
99        if (month >= 5 && month <= 10) notes.push('ฝั่งอันดามันเป็นฤดูมรสุม คลื่นลมแรง ทริปเกาะและกิจกรรมทางทะเลอาจงดบางวัน');
100        else notes.push('ช่วงนี้ทะเลฝั่งอันดามันสงบ เหมาะกับหาดและเกาะ (ฤดูท่องเที่ยวหลัก)');
101      } else if (GULF_SOUTH.includes(s) && (month >= 10 || month <= 1)) {
102        notes.push('ฝั่งอ่าวไทยตอนล่างฝนชุกช่วง ต.ค.–ม.ค. ควรเผื่อแผนสำรองในร่ม');
103      } else if (region === 'ภาคเหนือ' && month >= 2 && month <= 4) {
104        notes.push('ภาคเหนือช่วง ก.พ.–เม.ย. มักมีหมอกควันและฝุ่น PM2.5 จุดชมวิวอาจไม่ชัด');
105      } else if (region === 'ภาคเหนือ' && (month >= 11 || month <= 1)) {
106        notes.push('ภาคเหนือช่วงนี้อากาศเย็นสบาย เหมาะกับจุดชมวิวและกิจกรรมกลางแจ้ง (ฤดูท่องเที่ยวหลัก)');
107      }
108      if (month >= 3 && month <= 5) notes.push('ช่วง มี.ค.–พ.ค. อากาศร้อนจัด ควรเที่ยวกลางแจ้งช่วงเช้าหรือเย็น');
109      else if (month >= 6 && month <= 10 && !ANDAMAN.includes(s)) notes.push('ช่วง มิ.ย.–ต.ค. เป็นฤดูฝน ควรพกร่มและเผื่อสถานที่ในร่ม');
110      return notes;
111    }
บรรทัด 92–93: รายชื่อ slug จังหวัดฝั่งอันดามัน และฝั่งอ่าวไทยตอนล่าง
บรรทัด 95–97: seasonNote รับ slug และเดือน (1-12) หาจังหวัดฐานและภาค เตรียมรายการข้อความ
บรรทัด 98–100: อันดามัน: พ.ค.–ต.ค. เป็นฤดูมรสุม ช่วงอื่นทะเลสงบ
บรรทัด 101–102: อ่าวไทยตอนล่าง: ฝนชุก ต.ค.–ม.ค.
บรรทัด 103–106: ภาคเหนือ: ก.พ.–เม.ย. หมอกควัน PM2.5 และ พ.ย.–ม.ค. อากาศเย็น
บรรทัด 108–109: ทั่วประเทศ: มี.ค.–พ.ค. ร้อนจัด และ มิ.ย.–ต.ค. ฤดูฝน (ยกเว้นอันดามันที่พูดไปแล้ว)
บรรทัด 110: คืนรายการข้อความ
บรรทัด 113–122  อัปเดตคำแนะนำ
113    function updateHint() {
114      let el = $('seasonNote');
115      if (!el) { $('dateSummary').insertAdjacentHTML('afterend', '<div id="seasonNote" class="season-note"></div>'); el = $('seasonNote'); }
116      const dates = (typeof DATE_PICKER !== 'undefined' && DATE_PICKER) ? DATE_PICKER.selectedDates : [];
117      const slug = getProvince();
118      el.innerHTML = STATE.provinces[slug] ? `<div>ข้อมูลรองรับสูงสุด ${maxDays()} วันสำหรับ ${esc(nameOf(slug))}</div>` : '';
119      seasonLines = dates.length ? seasonNote(slug, dates[0].getMonth() + 1) : [];
120      refreshTips(true);
121      loadWeather(slug, dates);
122    }
บรรทัด 113–115: updateHint หากล่อง #seasonNote ถ้ายังไม่มีสร้างต่อจาก #dateSummary
บรรทัด 116–118: อ่านวันที่เลือกจาก DATE_PICKER ของ app.js แล้วเขียนข้อความจำนวนวันสูงสุดของจังหวัด
บรรทัด 119: สร้างหมายเหตุฤดูกาลจากเดือนของวันเริ่ม
บรรทัด 120–121: รีเฟรช Tips และโหลดพยากรณ์อากาศ
บรรทัด 126–155  พยากรณ์อากาศจริง
126    const WMO = c => c === 0 ? '☀️ ท้องฟ้าแจ่มใส' : c <= 2 ? '🌤️ มีเมฆบางส่วน' : c === 3 ? '☁️ เมฆมาก' : c <= 48 ? '🌫️ หมอก' : c <= 57 ? '🌦️ ฝนปรอย' : c <= 67 ? '🌧️ ฝนตก' : c <= 82 ? '🌧️ ฝนตกเป็นช่วง' : '⛈️ พายุฝนฟ้าคะนอง';
127    const wxCache = {};
128    let weatherLines = [], wxToken = 0, wetDays = false, wxDaily = {};
129    async function loadWeather(slug, dates) {
130      const my = ++wxToken, pv = STATE.provinces[slug];
131      weatherLines = []; wetDays = false; wxDaily = {};
132      if (!pv || !dates.length) return;
133      const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
134      const start = iso(dates[0]), end = iso(dates[dates.length - 1]);
135      const key = `${pv.center.map(x => x.toFixed(2))}|${start}|${end}`;
136      try {
137        if (!wxCache[key]) {
138          const url = `https://api.open-meteo.com/v1/forecast?latitude=${pv.center[0].toFixed(3)}&longitude=${pv.center[1].toFixed(3)}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FBangkok&start_date=${start}&end_date=${end}`;
139          const r = await fetch(url);
140          if (!r.ok) throw new Error(r.status);   // เช่น วันที่เกิน 16 วันข้างหน้า → 400
141          wxCache[key] = await r.json();
142        }
143        const d = wxCache[key].daily;
144        const fmtD = s => new Date(s + 'T00:00:00').toLocaleDateString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH'), {day: 'numeric', month: 'short'});
145        const wet = [];
146        d.time.forEach((t, i) => { wxDaily[t] = {code: d.weathercode[i], lo: Math.round(d.temperature_2m_min[i]), hi: Math.round(d.temperature_2m_max[i]), pop: d.precipitation_probability_max[i] ?? 0}; });
147        weatherLines = d.time.map((t, i) => {
148          if ((d.precipitation_probability_max[i] ?? 0) >= 60) wet.push(fmtD(t));
149          return `${WMO(d.weathercode[i])} ${fmtD(t)} ${Math.round(d.temperature_2m_min[i])}–${Math.round(d.temperature_2m_max[i])}°C โอกาสฝน ${d.precipitation_probability_max[i] ?? '-'}% (พยากรณ์จริง)`;
150        });
151        wetDays = wet.length > 0;
152        if (wet.length) weatherLines.unshift(`☔ ${wet.slice(0, 3).join(', ')} มีโอกาสฝนสูง ควรพกร่มและเผื่อสถานที่ในร่ม`);
153      } catch (e) { weatherLines = []; }
154      if (my === wxToken) { refreshTips(true); if (STATE.selectedPkg && $('detailPanel').style.display !== 'none') decorateWeather(STATE.selectedPkg); }
155    }
บรรทัด 126: WMO แปลงรหัสอากาศมาตรฐาน WMO เป็นข้อความไทยพร้อมอีโมจิ
บรรทัด 127–128: แคชผลตามพิกัดและช่วงวันที่ และตัวแปรสถานะ (บรรทัดพยากรณ์ โทเค็นกันผลซ้อน มีวันฝนหรือไม่ ข้อมูลรายวัน)
บรรทัด 129–132: loadWeather เพิ่มโทเค็น ล้างผลเก่า ถ้าไม่มีจังหวัดหรือวันที่ ออก
บรรทัด 133–135: สร้างวันที่ในรูป ISO และกุญแจแคช
บรรทัด 136–142: ถ้าไม่มีในแคช เรียก API ของ Open-Meteo ด้วยพิกัดศูนย์กลางจังหวัดเท่านั้น (ไม่ส่งข้อมูลผู้ใช้) ถ้าตอบผิดพลาด (เช่นเกิน 16 วัน) โยนข้อผิดพลาด
บรรทัด 143–146: อ่านผลรายวัน จัดรูปวันที่ตามภาษา และเก็บอุณหภูมิ รหัสอากาศ และโอกาสฝนของแต่ละวันลง wxDaily
บรรทัด 147–150: สร้างข้อความพยากรณ์รายวัน และจดวันที่โอกาสฝนตั้งแต่ 60%
บรรทัด 151–152: ตั้งธง wetDays และเพิ่มคำเตือนฝนไว้หน้าสุดของรายการ
บรรทัด 153: ถ้าผิดพลาดล้างข้อความพยากรณ์ (หน้าเว็บใช้หมายเหตุฤดูกาลแทน)
บรรทัด 154: ถ้าไม่มีคำขอใหม่แทรก รีเฟรช Tips และตกแต่งหน้าแผนที่เปิดอยู่
บรรทัด 157–179  ตกแต่งหน้าแผนด้วยอากาศ
157    const OUTDOOR = ['beach', 'viewpoint', 'activity'];
158    const dayIso = i => { const d0 = DATE_PICKER?.selectedDates[0]; if (!d0) return null; const d = new Date(d0.getTime() + i * 86400000); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
159    window.dayRainPop = i => (wxDaily[dayIso(i)] || {}).pop || 0;   // โอกาสฝน (%) ของวันที่ i ใช้ในหน้าเปลี่ยนสถานที่
160    window.OUTDOOR_CATS = OUTDOOR;
161    function decorateWeather(pkg) {
162      document.querySelectorAll('#dayPanels .day-panel').forEach((panel, i) => {
163        panel.querySelectorAll('.wx-chip, .rain-banner').forEach(e => e.remove());
164        const w = wxDaily[dayIso(i)]; if (!w) return;
165        panel.querySelector('.day-stats')?.insertAdjacentHTML('afterbegin', `<span class="wx-chip" title="พยากรณ์จริงจาก Open-Meteo">${WMO(w.code).split(' ')[0]} ${w.lo}–${w.hi}°C · ฝน ${w.pop}%</span>`);
166        const outdoor = pkg.days[i]?.pois.filter(p => OUTDOOR.includes(p.category)).length || 0;
167        if (w.pop >= 60) panel.querySelectorAll('.poi-item').forEach(li => {   // ไอคอนฝนที่การ์ดสถานที่กลางแจ้งในวันที่ฝนตก
168          const p = pkg.days[i]?.pois.find(x => x.id === li.dataset.id);
169          if (p && OUTDOOR.includes(p.category) && !li.querySelector('.rain-ic')) li.querySelector('.poi-name')?.insertAdjacentHTML('beforeend', `<span class="rain-ic" title="${window.WET_LANG === 'en' ? 'Outdoor place, it may rain' : 'สถานที่กลางแจ้ง อาจมีฝนตกได้'}"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 14a4 4 0 0 0 0-8 5.5 5.5 0 0 0-10.6 1.5A3.5 3.5 0 0 0 7 14"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/></svg></span>`);
170        });
171        if (w.pop >= 60 && outdoor) panel.querySelector('.day-head').insertAdjacentHTML('afterend', `<div class="rain-banner">☔ วันนี้โอกาสฝน ${w.pop}% แต่มีสถานที่กลางแจ้ง ${outdoor} จุด <button type="button" onclick="indoorSwap(${i})">สลับเป็นสถานที่ในร่ม</button></div>`);
172      });
173    }
174    const origRenderDetail = renderDetail;
175    renderDetail = function (pkg) {
176      if (!pkg._orig) setHidden(pkg, '_orig', JSON.parse(JSON.stringify(pkg)));   // จำแผนตั้งต้นที่ระบบคำนวณไว้ (ใช้กับปุ่มคืนค่าเดิม)
177      origRenderDetail(pkg);
178      for (const fn of [decorateWeather, decorateWarnings, enableDrag, recordHistory]) { try { fn(pkg); } catch (e) { console.error(fn.name, e); } }   // ข้อผิดพลาดในตัวตกแต่งต้องไม่ทำให้การลากการ์ดใช้ไม่ได้
179    };
บรรทัด 157: ประเภทสถานที่กลางแจ้ง
บรรทัด 158: dayIso คำนวณวันที่ ISO ของวันที่ i ในแผนจากวันเริ่มที่เลือก
บรรทัด 159–160: เปิด dayRainPop (โอกาสฝนของวัน) และ OUTDOOR_CATS ให้ ➜ frontend/app.js ใช้ในหน้าเลือกสถานที่
บรรทัด 161–165: decorateWeather ล้างป้ายเก่า แล้วเติมป้ายอุณหภูมิและโอกาสฝนในแถบสถิติของแต่ละวัน
บรรทัด 166: นับสถานที่กลางแจ้งของวันนั้น
บรรทัด 167–170: ถ้าโอกาสฝน ≥ 60% ใส่ไอคอนฝนที่การ์ดสถานที่กลางแจ้ง
บรรทัด 171: ถ้ามีสถานที่กลางแจ้งและฝนตกหนัก แทรกแถบเตือนพร้อมปุ่มสลับเป็นสถานที่ในร่ม (เรียก indoorSwap ด้านล่าง)
บรรทัด 172–173: ปิดการวนและฟังก์ชัน
บรรทัด 174–179: ห่อ ➜ renderDetail() ใน frontend/app.js: จำสำเนาแผนตั้งต้น (ซ่อนจากการแปลงเป็น JSON ด้วย setHidden) เรียกของเดิม แล้วเรียกตัวตกแต่งสี่ตัว (อากาศ คำเตือน ลากวาง และบันทึกประวัติ ➜ recordHistory() ใน frontend/app.js) ทีละตัวใน try/catch ให้ตัวหนึ่งพังไม่ทำให้ทั้งหน้าพัง
บรรทัด 181–195  แสดงคำเตือนที่การ์ด
181    // แสดงคำเตือนที่การ์ด (สีแดง + กล่องข้อความใต้การ์ด) เฉพาะ "อาจไปไม่ทันเวลาปิด" / "อาจไปถึงก่อนร้านเปิด" ค้างจนกว่าจะแก้หรือลากสลับใหม่
182    function decorateWarnings(pkg) {
183      document.querySelectorAll('.plan-warn, .poi-err-box').forEach(e => e.remove());
184      document.querySelectorAll('.poi-item.poi-error').forEach(e => e.classList.remove('poi-error'));
185      const panels = document.querySelectorAll('#dayPanels .day-panel'), clock = m => fmtClock(Math.round(m)), en = window.WET_LANG === 'en';
186      uiWarnings(pkg).forEach(w => {
187        const li = panels[w.d]?.querySelector(`.poi-item[data-id="${w.id}"]`); if (!li) return;
188        li.classList.add('poi-error');
189        let box = li.nextElementSibling; if (!box || !box.classList.contains('poi-err-box')) { box = document.createElement('li'); box.className = 'poi-err-box'; li.after(box); }
190        const msg = w.type === 'late'
191          ? (en ? `You may not make it before it closes (closes ${clock(w.poi.close_min)}). Try moving it earlier or choose another place.` : `อาจไปไม่ทันก่อนปิด (ปิดเวลา ${clock(w.poi.close_min)}) ลองย้ายไปไว้ก่อนหน้านี้หรือเปลี่ยนสถานที่`)
192          : (en ? `You may arrive before it opens (opens ${clock(w.poi.open_min)}). Try moving it later.` : `อาจไปถึงก่อนร้านเปิด (เปิดเวลา ${clock(w.poi.open_min)}) ลองย้ายไปไว้หลังจากนี้`);
193        box.innerHTML += `<div>⚠ ${esc(msg)}</div>`;
194      });
195    }
บรรทัด 182–185: decorateWarnings ล้างคำเตือนเก่า และเตรียมตัวช่วยจัดรูปเวลา (fmtClock) กับธงภาษา
บรรทัด 186–188: ไล่คำเตือนจาก ➜ uiWarnings() ใน frontend/app.js หาการ์ดของจุดนั้น แล้วทำให้เป็นสีแดง
บรรทัด 189: หาหรือสร้างกล่องข้อความใต้การ์ด
บรรทัด 190–192: ข้อความตามชนิด: ไปไม่ทันก่อนปิด (late) หรือถึงก่อนเปิด พร้อมสองภาษา
บรรทัด 193: ใส่ข้อความในกล่อง (หลีกอักขระพิเศษด้วย esc)
บรรทัด 197–223  ย้ายสถานที่และวาดแผนที่ใหม่
197    // ---------- ลากวางสถานที่เพื่อเรียงลำดับ/ย้ายข้ามวัน (แล้วคำนวณเวลา-ค่าใช้จ่ายใหม่ตามลำดับที่ลาก) ----------
198    // ย้ายสถานที่ไป "ตำแหน่งของเป้าหมาย" (ลากไปหลัง = ไปอยู่หลังเป้าหมาย, ลากไปหน้า = ไปอยู่หน้าเป้าหมาย); ถ้าส่งคำขอไม่สำเร็จ คืนแผนเดิม
199    let keepVis = null;   // จำวันที่เปิดอยู่บนแผนที่ไว้ตอนวาดใหม่หลังแก้แผน
200    const editView = focus => { keepVis = {focus, vis: Object.values(STATE.mapDayLayers).map(l => l.visible)}; };
201    function snapshot() { return STATE.selectedPkg.days.map(d => d.pois.slice()); }
202    function restore(snap) { STATE.selectedPkg.days.forEach((d, i) => { d.pois = snap[i].slice(); }); keepVis = null; }
203    function moveStop(src, dst) {
204      const days = STATE.selectedPkg.days, [sd, si] = src, snap = snapshot();
205      const [poi] = days[sd].pois.splice(si, 1);
206      const di = dst.i === null ? days[dst.d].pois.length : dst.i;
207      days[dst.d].pois.splice(di, 0, poi);
208      editView(null);
209      recomputeAndRefresh(() => restore(snap));
210    }
211    // วาดแผนที่ใหม่หลังแก้แผน: คงวันที่เปิดอยู่ (หรือแสดงเฉพาะวันที่แก้) — ไม่ทำให้ลากหมุดได้ (ลากการ์ดทางซ้ายแทน)
212    const origDrawOnMap = drawOnMap;
213    drawOnMap = function (pkg) {
214      origDrawOnMap(pkg);
215      if (keepVis) {
216        const {focus, vis} = keepVis; keepVis = null;
217        Object.keys(STATE.mapDayLayers).forEach(k => {
218          const want = focus != null ? +k === focus : vis[k] !== false, L_ = STATE.mapDayLayers[k];
219          if (L_.visible !== want) toggleDay(+k);
220        });
221        resetMapView();
222      }
223    };
บรรทัด 199: keepVis จำสถานะการเปิดปิดวันบนแผนที่ระหว่างวาดใหม่
บรรทัด 200: editView จดวันที่จะแสดงเฉพาะ (หรือคงของเดิม)
บรรทัด 201–202: snapshot จำลำดับสถานที่ทุกวัน และ restore คืนค่าเมื่อคำนวณไม่สำเร็จ
บรรทัด 203–210: moveStop ตัดสถานที่จากตำแหน่งเดิม วางที่ตำแหน่งใหม่ (หรือท้ายวัน) แล้วเรียก ➜ recomputeAndRefresh() ใน frontend/app.js ให้คำนวณเวลาและค่าใช้จ่ายใหม่ผ่าน ➜ recompute() ใน backend/main.py ถ้าล้มเหลวเรียก restore
บรรทัด 212–223: ห่อ ➜ drawOnMap() ใน frontend/app.js: เรียกของเดิม แล้วถ้ามี keepVis เปิดเฉพาะวันที่ต้องการด้วย ➜ toggleDay() ใน frontend/app.js และรีเซ็ตมุมมองด้วย ➜ resetMapView() ใน frontend/app.js
บรรทัด 225–299  ลากการ์ดด้วย pointer events (เมาส์และจอสัมผัส)
225    function enableDrag() {
226      const root = document.getElementById('dayPanels'); if (!root) return;
227      let gap = null, srcKey = null, srcLi = null, hiddenConn = null, ghost = null, offX = 0, offY = 0, corrX = 0, corrY = 0, curUl = null;
228      const cards = ul => [...ul.querySelectorAll('.poi-item')].filter(e => e !== srcLi && e !== ghost);
229      const flip = (ul, mutate) => {   // บันทึกตำแหน่งเดิม → เปลี่ยน DOM → เลื่อนจากตำแหน่งเดิมมาตำแหน่งใหม่
230        const items = cards(ul), before = new Map(items.map(e => [e, e.getBoundingClientRect().top]));
231        mutate();
232        items.forEach(e => { const dy = before.get(e) - e.getBoundingClientRect().top; if (dy) { e.style.transition = 'none'; e.style.transform = `translateY(${dy}px)`; requestAnimationFrame(() => { e.style.transition = 'transform .18s ease'; e.style.transform = ''; }); } });
233      };
234      const cleanup = () => { hiddenConn?.classList.remove('drag-hide'); hiddenConn = null; gap?.remove(); gap = null; ghost?.remove(); ghost = null; srcLi?.classList.remove('dragging'); srcLi = null; curUl = null; root.classList.remove('is-dragging'); document.body.classList.remove('wet-dragging'); };
235      // ใช้ pointer events แทน HTML5 drag-and-drop: การ์ดตามเมาส์ทุกเฟรม ไม่หน่วงเหมือน dragover ที่ถูกจำกัดความถี่
236      root.querySelectorAll('.poi-list').forEach(ul => {
237        const d = +(ul.id.match(/day-(\d+)-list/) || [])[1];
238        ul.querySelectorAll('.poi-item').forEach((li, i) => {
239          li.draggable = false; li.title = li.title || (window.WET_LANG === 'en' ? 'Drag to reorder or move to another day' : 'ลากเพื่อเรียงลำดับหรือย้ายไปวันอื่น');
240          li.ondragstart = e => e.preventDefault();   // ปิด drag ของเบราว์เซอร์ (ข้อความ/รูปในการ์ด) ที่จะขัดกับการลากแบบ pointer
241          li.onpointerdown = e => {
242            if (e.button !== 0 || e.target.closest('button, a, input, select')) return;
243            const touch = e.pointerType === 'touch';   // จอสัมผัส: กดค้าง 0.35 วินาทีจึงเริ่มลาก (ลากเร็วกว่านั้นคือเลื่อนหน้า)
244            if (!touch) e.preventDefault();
245            const sx = e.clientX, sy = e.clientY, r0 = li.getBoundingClientRect(); let started = false, lp = 0;
246            const noScroll = ev => { if (started && ev.cancelable) ev.preventDefault(); };   // ระหว่างลากบนจอสัมผัสไม่ให้หน้าเลื่อน
247            if (touch) document.addEventListener('touchmove', noScroll, {passive: false});
248            const start = () => {
249              started = true; srcKey = [d, i]; srcLi = li; offX = sx - r0.left; offY = sy - r0.top;
250              gap = document.createElement('li'); gap.className = 'drop-gap'; gap.style.height = li.offsetHeight + 'px';
251              root.classList.add('is-dragging'); document.body.classList.add('wet-dragging'); document.getSelection()?.removeAllRanges();
252              ghost = li.cloneNode(true); ghost.classList.add('drag-ghost'); ghost.removeAttribute('title');
253              ghost.style.cssText = `width:${r0.width}px;left:${r0.left}px;top:${r0.top}px;transform-origin:${offX}px ${offY}px`;
254              ul.appendChild(ghost);
255              ghost.style.animation = 'none'; ghost.style.transform = 'none'; const g0 = ghost.getBoundingClientRect(); ghost.style.animation = ''; ghost.style.transform = '';
256              corrX = g0.left - r0.left; corrY = g0.top - r0.top;   // บาง ancestor มี transform ทำให้ fixed อิงกรอบนั้น: ชดเชยส่วนต่างให้ตรงเมาส์
257              li.classList.add('dragging'); li.after(gap); curUl = ul;
258              const pv = li.previousElementSibling; if (pv?.classList.contains('dist-connector')) { pv.classList.add('drag-hide'); hiddenConn = pv; }
259              if (touch) { try { li.releasePointerCapture(e.pointerId); } catch (_) {} navigator.vibrate?.(15); }
260            };
261            if (touch) lp = setTimeout(() => { last = {clientX: sx, clientY: sy}; start(); frame(); }, 350);
262            let raf = 0, last = null;
263            const frame = () => {
264              raf = 0; if (!ghost || !last) return;
265              ghost.style.left = (last.clientX - offX - corrX) + 'px'; ghost.style.top = (last.clientY - offY - corrY) + 'px';
266              const under = document.elementFromPoint(last.clientX, last.clientY), panel = under?.closest('.day-panel'), tul = panel?.querySelector('.poi-list');
267              if (!tul) return;
268              if (touch) { const ed = last.clientY < 80 ? -14 : last.clientY > innerHeight - 80 ? 14 : 0; if (ed) { scrollBy(0, ed); if (!raf) raf = requestAnimationFrame(frame); } }   // ลากชิดขอบจอ: เลื่อนหน้าอัตโนมัติ
269              const cs = cards(tul); let ref = null;
270              for (const c of cs) { const r = c.getBoundingClientRect(); if (last.clientY < r.top + r.height / 2) { ref = c; break; } }
271              const already = gap.parentNode === tul && (ref ? gap.nextElementSibling === ref : !cs.some(c => gap.compareDocumentPosition(c) & 4));
272              if (already) return;
273              flip(tul, () => { if (ref) tul.insertBefore(gap, ref); else tul.appendChild(gap); }); curUl = tul;
274            };
275            const move = ev => {
276              if (!started) {
277                if (touch) { if (Math.hypot(ev.clientX - sx, ev.clientY - sy) > 8) clearTimeout(lp); return; }   // ขยับก่อนกดค้างครบเวลา = ผู้ใช้เลื่อนหน้า
278                if (Math.hypot(ev.clientX - sx, ev.clientY - sy) < 6) return; start();
279              }
280              last = ev; if (!raf) raf = requestAnimationFrame(frame);
281            };
282            const up = ev => {
283              document.removeEventListener('pointermove', move); document.removeEventListener('pointerup', up); document.removeEventListener('pointercancel', up);
284              clearTimeout(lp); document.removeEventListener('touchmove', noScroll);
285              if (!started) return;
286              if (raf) cancelAnimationFrame(raf);
287              window.addEventListener('click', ck => { ck.stopPropagation(); ck.preventDefault(); }, {capture: true, once: true});   // ไม่ให้การปล่อยเมาส์ถูกนับเป็นคลิกการ์ด
288              const targetUl = gap?.parentNode, src = srcKey;
289              if (ev.type === 'pointercancel' || !targetUl || !targetUl.classList.contains('poi-list')) { cleanup(); return; }
290              const dd = +targetUl.id.match(/day-(\d+)-list/)[1];
291              const idx = [...targetUl.children].filter(c => (c.classList.contains('poi-item') && c !== srcLi && c !== ghost) || c === gap).indexOf(gap);
292              cleanup();
293              if (!(src[0] === dd && src[1] === idx)) moveStop(src, {d: dd, i: idx});
294            };
295            document.addEventListener('pointermove', move); document.addEventListener('pointerup', up); document.addEventListener('pointercancel', up);
296          };
297        });
298      });
299    }
บรรทัด 225–228: enableDrag หาตัวห่อ #dayPanels และประกาศตัวแปรสถานะการลาก (ช่องว่าง การ์ดต้นทาง ตัวผี ออฟเซ็ต) และ cards คืนการ์ดอื่นในรายการ
บรรทัด 229–233: flip เทคนิค FLIP: จำตำแหน่งเดิม เปลี่ยน DOM แล้วเลื่อนการ์ดจากตำแหน่งเดิมมาตำแหน่งใหม่แบบนุ่ม ๆ
บรรทัด 234: cleanup ล้างสถานะและองค์ประกอบชั่วคราวทั้งหมดของการลาก
บรรทัด 235–236: ใช้ pointer events แทน HTML5 drag-and-drop เพราะการ์ดตามเมาส์/นิ้วทุกเฟรม แล้ววนทุกรายการวัน
บรรทัด 237–240: หาเลขวันจาก id ปิด draggable และ dragstart ของเบราว์เซอร์ และตั้ง title ของการ์ด
บรรทัด 241–247: เมื่อกดที่การ์ด (ไม่ใช่ปุ่มข้างใน) แยกเมาส์กับจอสัมผัส: เมาส์ป้องกันค่าเริ่มต้นทันที ส่วนจอสัมผัสต้องกดค้างก่อน จดจุดเริ่มต้น และผูกตัวดัก touchmove แบบ non-passive ที่กันหน้าเลื่อนเฉพาะเมื่อกำลังลากอยู่
บรรทัด 248–260: start เริ่มลากจริง: สร้างช่องว่าง drop-gap และตัวผีของการ์ด ชดเชยตำแหน่งกรณีบรรพบุรุษมี transform ซ่อนเส้นเชื่อมระยะทาง และบนจอสัมผัสปล่อย pointer capture แล้วสั่นเครื่องเบา ๆ
บรรทัด 261: จอสัมผัส: ตั้งตัวจับเวลา 350 มิลลิวินาที เมื่อครบโดยนิ้วไม่ขยับจึงเรียก start (ถ้านิ้วขยับก่อน move จะยกเลิกเพราะผู้ใช้กำลังเลื่อนหน้า)
บรรทัด 262–274: frame ทำงานหนึ่งครั้งต่อเฟรม: ย้ายตัวผีตามเมาส์/นิ้ว หารายการวันใต้ตำแหน่ง บนจอสัมผัสถ้านิ้วอยู่ใกล้ขอบบนหรือล่างของจอ (80 พิกเซล) เลื่อนหน้าอัตโนมัติ แล้วหาการ์ดที่จะแทรกก่อนและย้ายช่องว่างถ้าตำแหน่งเปลี่ยน
บรรทัด 275–281: move เมาส์: เริ่มลากเมื่อเกิน 6 พิกเซล จอสัมผัส: ถ้าขยับเกิน 8 พิกเซลก่อนกดค้างครบเวลาให้ยกเลิกตัวจับเวลา แล้วบันทึกตำแหน่งล่าสุดและขอเฟรม
บรรทัด 282–294: up ถอดตัวฟังและตัวจับเวลา ยกเลิกกรณี pointercancel หรือไม่มีเป้าหมาย คำนวณวันและตำแหน่งปลายทาง ล้างสถานะ และเรียก moveStop ถ้าตำแหน่งเปลี่ยนจริง (กันคลิกที่ตามมาด้วยตัวดักครั้งเดียว)
บรรทัด 295–299: ผูกตัวฟัง move up cancel แล้วปิดฟังก์ชัน
บรรทัด 302–324  สลับเป็นสถานที่ในร่ม
302    window.indoorSwap = async function (dIdx) {
303      const pkg = STATE.selectedPkg, day = pkg.days[dIdx];
304      const inPlan = new Set(pkg.days.flatMap(d => d.pois.map(p => p.id)));
305      const base = day.pois.filter(p => p.category !== 'restaurant');
306      const cLat = base.reduce((s, p) => s + p.lat, 0) / base.length, cLng = base.reduce((s, p) => s + p.lng, 0) / base.length;
307      const cands = STATE.pois.filter(p => ['culture', 'market'].includes(p.category) && !inPlan.has(p.id) && !STATE.excluded.has(p.id) && haversineKm(cLat, cLng, p.lat, p.lng) <= 25)
308        .sort((a, b) => (b.category === 'culture') - (a.category === 'culture') || b.score - a.score);
309      const snap = snapshot(), savedLocked = new Set(STATE.locked), savedExcl = new Set(STATE.excluded);
310      let n = 0;
311      day.pois.slice().forEach((p, k) => {
312        if (!OUTDOOR.includes(p.category)) return;
313        const at = arriveOf(day, p);   // นาทีที่ไปถึงจุดเดิม — เลือกที่ในร่มที่เปิดอยู่ช่วงนั้น
314        const ci = cands.findIndex(c => at < 0 || (c.open_min <= at && at + c.duration_min <= c.close_min));
315        if (ci < 0) return;
316        const [c] = cands.splice(ci, 1);
317        day.pois[k] = c; STATE.locked.add(c.id); STATE.excluded.add(p.id); STATE.locked.delete(p.id); n++;
318      });
319      if (!n) { showToast('ไม่พบสถานที่ในร่มใกล้เคียงที่ยังเปิดอยู่ในช่วงเวลานั้นและยังไม่อยู่ในแผน', 'error', 4500); return; }
320      showToast(`สลับ ${n} จุดของวันที่ ${dIdx + 1} เป็นสถานที่ในร่มแล้ว`, 'ok', 3000);
321      editView(dIdx);   // แสดงเฉพาะวันที่กดบนแผนที่
322      // คำนวณใหม่เฉพาะแผนที่ผู้ใช้แก้ (ไม่ย้ายจุดของวันอื่น) ถ้าล้มเหลวคืนค่าเดิมทั้งหมด
323      await recomputeAndRefresh(() => { restore(snap); STATE.locked = savedLocked; STATE.excluded = savedExcl; });
324    };
บรรทัด 302–306: indoorSwap หาแผน วัน สถานที่ที่อยู่ในแผนทั้งหมด และจุดศูนย์กลางของวันที่ไม่นับร้านอาหาร
บรรทัด 307–308: หาตัวเลือก: วัฒนธรรมหรือตลาด ที่ยังไม่อยู่ในแผนและไม่ถูกลบ ห่างไม่เกิน 25 กม. (haversineKm) เรียงให้วัฒนธรรมก่อนแล้วตามคะแนน
บรรทัด 309–310: จำสถานะเดิมไว้ย้อนกลับ
บรรทัด 311–318: แต่ละจุดกลางแจ้ง หาเวลาถึง (arriveOf) และเลือกที่ในร่มที่เปิดในช่วงนั้น แทนที่และล็อกจุดใหม่ ลบจุดเดิมออก
บรรทัด 319–320: แจ้งเตือนถ้าหาไม่เจอ หรือจำนวนที่สลับ
บรรทัด 321–323: แสดงเฉพาะวันนั้นบนแผนที่ แล้วคำนวณใหม่ ถ้าล้มเหลวคืนค่าเดิม
บรรทัด 326–386  แม่แบบ Tips ต่อหมวด
326    // ---------- กล่อง Tips (หมุนทุก 20 วินาที) ----------
327    let seasonLines = [], tipIdx = 0, tipPool = [], tipsTimer = null, tipsFor = null;
328    // แม่แบบ Tips ต่อหมวด: ok = เงื่อนไขจากข้อมูลจริงของสถานที่ (กันแนะนำผิด เช่น บอกให้ไปตอนเย็นทั้งที่ปิดแล้ว)
329    const hhmm = m => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
330    const price = p => p.cost > 0 ? `ค่าเข้า/ใช้จ่ายราว ${fmt(p.cost)} บาท` : 'ไม่เสียค่าเข้า';
331    const hrs = p => p.open_min <= 0 && p.close_min >= 1439 ? 'เปิดทั้งวัน' : `เปิด ${hhmm(p.open_min)}–${hhmm(p.close_min)}`;
332    const morning = p => p.open_min <= 600, evening = p => p.close_min >= 1080, any = () => true;
333    const dur = p => p.duration_min >= 30 ? `ใช้เวลาราว ${p.duration_min >= 90 ? Math.round(p.duration_min / 60 * 10) / 10 + ' ชั่วโมง' : p.duration_min + ' นาที'}` : '';
334    // dry = ใช้เฉพาะวันที่ไม่ฝน, rain = ใช้เฉพาะเมื่อพยากรณ์ว่าฝนตก
335    const TIP_TPL = {
336      beach: [
337        {ok: morning, dry: 1, t: p => `🏖️ ${p.name_th} ไปช่วงเช้าแดดยังไม่แรง ทรายเย็น เหมาะกับการเดินเล่น`},
338        {ok: evening, dry: 1, t: p => `🌅 ${p.name_th} นั่งชมพระอาทิตย์ตกได้ ${hrs(p)}`},
339        {ok: any, dry: 1, t: p => `🏖️ ${p.name_th} ${price(p)} อย่าลืมครีมกันแดดและน้ำดื่ม`},
340        {ok: any, t: p => `📸 ${p.name_th} จุดถ่ายรูปยอดนิยมของหมวดหาด ${dur(p)}`.trim()},
341        {ok: any, dry: 1, t: p => `🩴 ${p.name_th} พกรองเท้าแตะกับผ้าเช็ดตัวเล็ก ๆ ไว้ ลงเล่นน้ำได้ทันที`},
342        {ok: any, t: p => `🌊 ${p.name_th} ดูธงเตือนคลื่นลมก่อนลงเล่นน้ำทุกครั้ง และเล่นในเขตที่กำหนด`},
343        {ok: any, rain: 1, t: p => `🌧️ ${p.name_th} ช่วงฝนคลื่นอาจแรง ชมวิวจากริมหาดแทนการลงน้ำจะปลอดภัยกว่า`},
344      ],
345      temple: [
346        {ok: morning, t: p => `🛕 ${p.name_th} แวะตอนเช้าอากาศเย็น คนน้อย ${hrs(p)}`},
347        {ok: any, t: p => `🛕 ${p.name_th} แต่งกายสุภาพ ถอดรองเท้าก่อนเข้าอาคาร ${price(p)}`},
348        {ok: any, t: p => `🙏 ${p.name_th} ${dur(p) || 'แวะชมได้ไม่นาน'} เหมาะแทรกระหว่างสถานที่อื่น`},
349        {ok: evening, t: p => `🪔 ${p.name_th} ยังเปิดถึง ${hhmm(p.close_min)} ไปช่วงเย็นบรรยากาศสงบ`},
350        {ok: any, t: p => `🤫 ${p.name_th} พูดเบา ๆ และขออนุญาตก่อนถ่ายรูปพระหรือผู้คน`},
351        {ok: any, rain: 1, t: p => `☔ ${p.name_th} มีศาลาหรืออาคารให้หลบฝนได้ เหมาะกับวันฝนตก`},
352        {ok: any, dry: 1, t: p => `🌳 ${p.name_th} พื้นที่โล่ง ควรพกหมวกหรือร่มกันแดดไว้`},
353      ],
354      viewpoint: [
355        {ok: evening, dry: 1, t: p => `🌄 ${p.name_th} ควรไปช่วงเย็น แสงสวยที่สุด (ปิด ${hhmm(p.close_min)})`},
356        {ok: morning, dry: 1, t: p => `⛅ ${p.name_th} ไปเช้าท้องฟ้าโปร่ง ถ่ายวิวได้ชัด`},
357        {ok: any, t: p => `🌄 ${p.name_th} ${price(p)} พกกล้องหรือโทรศัพท์แบตเต็มไปด้วย`},
358        {ok: any, t: p => `👟 ${p.name_th} ใส่รองเท้าเดินสบาย ${dur(p)}`.trim()},
359        {ok: any, rain: 1, t: p => `🌫️ ${p.name_th} วันฝนทัศนียภาพอาจถูกเมฆบัง ลองสลับไปไว้วันที่ฟ้าเปิด`},
360        {ok: any, t: p => `🧥 ${p.name_th} ที่สูงลมแรงกว่าที่คิด พกเสื้อบาง ๆ ไว้สักตัว`},
361      ],
362      culture: [
363        {ok: any, t: p => `🏛️ ${p.name_th} ${hrs(p)} ${price(p)}`},
364        {ok: any, t: p => `🎟️ ${p.name_th} ${dur(p) || 'เดินชมได้สบาย'} เหมาะเป็นกิจกรรมหลบแดดช่วงบ่าย`},
365        {ok: morning, t: p => `📚 ${p.name_th} แวะตอนเช้าได้ข้อมูลเต็มที่ ก่อนคนเยอะ`},
366        {ok: any, t: p => `🏛️ ${p.name_th} ได้เรียนรู้เรื่องราวท้องถิ่น เหมาะกับครอบครัว`},
367        {ok: any, rain: 1, t: p => `☔ ${p.name_th} กิจกรรมในร่มที่เหมาะกับวันฝนตก ${hrs(p)}`},
368        {ok: any, t: p => `🗺️ ${p.name_th} ถามเจ้าหน้าที่ถึงเรื่องเล่าท้องถิ่น มักได้ข้อมูลที่ไม่มีในป้าย`},
369      ],
370      market: [
371        {ok: evening, t: p => `🛍️ ${p.name_th} ช่วงเย็นคึกคักที่สุด เหมาะกับมื้อเย็นและของฝาก (ปิด ${hhmm(p.close_min)})`},
372        {ok: any, t: p => `🍢 ${p.name_th} ลองของกินพื้นเมือง พกเงินสดเล็กน้อยไว้ต่อรอง`},
373        {ok: morning, t: p => `🧺 ${p.name_th} ไปเช้าของสดและของฝากครบกว่า`},
374        {ok: any, t: p => `🛍️ ${p.name_th} ${hrs(p)} เดินเล่นได้ ${dur(p)}`.trim()},
375        {ok: any, t: p => `🥭 ${p.name_th} ถามหาผลไม้หรือขนมประจำฤดูกาล ซื้อกินสด ๆ อร่อยกว่า`},
376        {ok: any, rain: 1, t: p => `🌂 ${p.name_th} ตลาดมักมีหลังคาบางส่วน พกร่มพับไว้ก็เดินได้สบาย`},
377      ],
378      activity: [
379        {ok: any, t: p => `🎈 ${p.name_th} กิจกรรมสนุก ๆ ${price(p)} ควรเช็คคิวหรือจองล่วงหน้า`},
380        {ok: morning, dry: 1, t: p => `🤸 ${p.name_th} เริ่มตอนเช้าอากาศดี ไม่ร้อนจัด`},
381        {ok: any, t: p => `👨‍👩‍👧 ${p.name_th} เหมาะกับเพื่อนและครอบครัว ${dur(p)}`.trim()},
382        {ok: any, dry: 1, t: p => `🎒 ${p.name_th} เตรียมเสื้อผ้าเปลี่ยนและครีมกันแดด ${hrs(p)}`},
383        {ok: any, rain: 1, t: p => `📞 ${p.name_th} กิจกรรมกลางแจ้งอาจเลื่อนเมื่อฝนตก โทรเช็คกับผู้ให้บริการก่อนออกเดินทาง`},
384        {ok: any, t: p => `💧 ${p.name_th} จิบน้ำบ่อย ๆ และฟังคำแนะนำด้านความปลอดภัยของเจ้าหน้าที่`},
385      ],
386    };
บรรทัด 327: ตัวแปรสถานะของกล่อง Tips
บรรทัด 329–333: ตัวช่วยสร้างข้อความ: เวลา (hhmm) ราคา เวลาเปิด-ปิด เงื่อนไขเช้า/เย็น และระยะเวลาที่ใช้
บรรทัด 335–386: TIP_TPL แม่แบบประโยคของแต่ละหมวด (หาด วัด จุดชมวิว วัฒนธรรม ตลาด กิจกรรม) แต่ละแม่แบบมีเงื่อนไข ok ตรวจจากข้อมูลจริงของสถานที่ (กันแนะนำผิด เช่นให้ไปตอนเย็นทั้งที่ปิดก่อน) และธง dry (ใช้เฉพาะวันไม่ฝน) หรือ rain (เฉพาะวันฝน)
บรรทัด 387–408  เคล็ดลับทั่วไป
387    // เคล็ดลับทั่วไป (ไม่ผูกกับสถานที่) — บางข้อปรับตามจำนวนวัน/งบ/จำนวนคนที่กรอก
388    function generalTips() {
389      const days = SELECTED_DAYS, budget = +$('budget').value || 0, ppl = +$('travelers').value || 1;
390      const t = [
391        '💡 กด "ความชอบ" เพื่อเลือกหมวดที่ชอบหรือไม่ชอบ แผนจะปรับตามให้',
392        '💡 บันทึกแผนที่ถูกใจด้วยปุ่ม ★ แล้วกลับมาเปิดดูได้ภายหลัง',
393        '💡 เที่ยวต่อจังหวัดข้างเคียงได้ กดชื่อจังหวัดใต้ช่องเลือกจังหวัด',
394        '🔄 ไม่ถูกใจสถานที่ไหน กดสลับหรือลบจุดในแผน ระบบจะจัดเส้นทางที่เหลือให้ใหม่',
395        '📅 ส่งแผนเข้าปฏิทินได้ด้วยปุ่ม ปฏิทิน และบันทึกเป็น PDF ไว้เปิดตอนไม่มีสัญญาณ',
396        '👫 ชวนเพื่อนวางแผนด้วยกันผ่านปุ่ม แชร์ ทุกคนเห็นและแก้แผนเดียวกันได้',
397        '⇄ อยากรู้ว่าอัลกอริทึมไหนวางแผนได้ดีกว่า ลองกด "เทียบอัลกอริทึม" ในหน้าปรับแต่งทริป',
398        '🚗 เวลาเดินทางในแผนคิดแบบรถไม่ติด ช่วงชั่วโมงเร่งด่วนควรเผื่อเวลาเพิ่มราว 20–30%',
399        '🍜 มื้อกลางวันช่วง 11:00–14:30 ร้านดัง ๆ คนเยอะ ไปก่อน 11:30 มักไม่ต้องรอคิว',
400        '🔋 พกพาวเวอร์แบงก์และเก็บแผนที่ออฟไลน์ไว้ เผื่อสัญญาณอินเทอร์เน็ตไม่ดี',
401        '🧴 ครีมกันแดด หมวก และน้ำดื่ม เป็นของที่ควรพกติดตัวทุกทริป',
402      ];
403      if (days >= 4) t.push(`🛌 ทริป ${days} วันแนะนำให้เว้นช่วงพักครึ่งวันสักวัน จะไม่เหนื่อยสะสม`);
404      if (days === 1) t.push('⏰ ทริปวันเดียวควรเริ่มก่อน 9:00 และเลือกสถานที่ที่อยู่ใกล้กัน');
405      if (budget && days) t.push(`💰 งบ ${fmt(budget)} บาท ตก ${fmt(budget / days / ppl)} บาท/คน/วัน รวมที่พักแล้ว ปรับงบเพิ่มเพื่อได้แพ็กเกจ Premium`);
406      if (ppl >= 4) t.push('👨‍👩‍👧‍👦 เดินทางหลายคน แชร์ค่ารถหรือเช่ารถตู้จะคุ้มกว่าเรียกรถแยก');
407      return t;
408    }
บรรทัด 388–402: generalTips อ่านจำนวนวัน งบ และจำนวนคนจากฟอร์ม แล้วสร้างรายการเคล็ดลับที่ไม่ผูกกับสถานที่
บรรทัด 403–406: เติมเคล็ดลับตามเงื่อนไข: ทริปยาว ≥ 4 วัน ทริปวันเดียว งบต่อคนต่อวัน และเดินทางหลายคน
บรรทัด 407–408: คืนรายการ
บรรทัด 409–426  เคล็ดลับตามจังหวัด
409    // Tips เฉพาะจังหวัด: จุดเด่นจากข้อมูลจริงของจังหวัดนั้น + เคล็ดลับตามภูมิภาค/ลักษณะพื้นที่
410    const REGION_TIPS = {
411      'ภาคเหนือ': ['🧣 ภาคเหนือหน้าหนาว (พ.ย.–ก.พ.) ตอนเช้าอากาศเย็นจัด พกเสื้อกันหนาวบางๆ', '🏍️ ถนนบนเขามีโค้งมาก ขับช้าๆ และเผื่อเวลาเดินทางเพิ่ม', '🍲 ลองอาหารเหนือ เช่น ขันโตก ข้าวซอย น้ำพริกหนุ่ม', '🌫️ ช่วงปลายหนาวถึงต้นร้อนอาจมีหมอกควัน ตรวจค่าฝุ่นก่อนไปจุดชมวิว'],
412      'ภาคตะวันออกเฉียงเหนือ': ['🌞 ภาคอีสานแดดแรงและร้อนจัดช่วงเมษายน แนะนำเที่ยวเช้าและเย็น', '🥗 ลองส้มตำ ลาบ และไก่ย่างของท้องถิ่น', '🛕 อีสานมีปราสาทหินและวัดเก่าแก่ ควรพกหมวกและน้ำดื่ม', '🚗 ระยะทางระหว่างอำเภอค่อนข้างไกล ควรเช่ารถหรือจัดรถไว้ล่วงหน้า'],
413      'ภาคกลาง': ['🛶 ภาคกลางมีตลาดน้ำและวัดเก่า แต่งกายสุภาพเมื่อเข้าวัด', '☀️ ช่วงบ่ายร้อนจัด เหมาะกับพิพิธภัณฑ์และร้านในร่ม', '🚆 เดินทางรถไฟหรือรถตู้ไปหลายเมืองได้สะดวก', '🍜 อาหารภาคกลางมีหลากหลาย ลองก๋วยเตี๋ยวเรือและขนมไทยโบราณ'],
414      'ภาคตะวันออก': ['🏖️ ชายฝั่งตะวันออกเที่ยวทะเลสะดวก ใกล้กรุงเทพฯ เหมาะกับทริปสั้น', '🍤 อาหารทะเลสดที่ตลาดชายหาด ถามราคาก่อนสั่งทุกครั้ง', '🍈 ช่วงเมษายน–มิถุนายนมีผลไม้ฤดูกาลมาก เช่น ทุเรียน มังคุด เงาะ', '⛴️ ถ้าไปเกาะ เช็คตารางเรือและสภาพคลื่นก่อนเดินทาง'],
415      'ภาคตะวันตก': ['🌳 ภาคตะวันตกมีป่า น้ำตก และอุทยาน พกยากันยุงและรองเท้าเดินป่า', '🌊 น้ำตกหน้าฝนน้ำแรง ตรวจประกาศอุทยานก่อนลงเล่นน้ำ', '🚆 รถไฟสายประวัติศาสตร์เป็นกิจกรรมที่น่าลอง ควรจองตั๋วล่วงหน้า', '🍃 ที่พักใกล้ธรรมชาติมักไม่มีสัญญาณมือถือ เก็บแผนที่ออฟไลน์ไว้'],
416      'ภาคใต้': ['⛵ ภาคใต้ทะเลอันดามัน ช่วงพ.ค.–ต.ค. คลื่นลมแรง เรือบางเส้นทางงดเดินเรือ', '🏝️ ฝั่งอ่าวไทยฝนหนักช่วงต.ค.–ธ.ค. เช็คพยากรณ์ก่อนไปเกาะ', '🍛 ลองอาหารใต้ เช่น แกงส้ม ข้าวยำ และโรตีกับแกงกะหรี่', '🧴 แดดทะเลแรงมาก ทาครีมกันแดดซ้ำทุก 2 ชั่วโมง'],
417    };
418    function provinceTips() {
419      const base = (typeof baseSlug !== 'undefined' && baseSlug) || getProvince().split('+')[0], pv = STATE.provinces[base] || {}, nm = pv.name_th || base;
420      const out = [...(REGION_TIPS[pv.region] || [])];
421      const best = c => STATE.pois.filter(p => p.category === c && p.open_min !== undefined).sort((a, b) => b.score - a.score).slice(0, 3).map(p => p.name_th);
422      const hi = [['beach', 'หาดและทะเล'], ['temple', 'วัด'], ['viewpoint', 'จุดชมวิว'], ['culture', 'วัฒนธรรมและพิพิธภัณฑ์'], ['market', 'ตลาด'], ['activity', 'กิจกรรม']];
423      hi.forEach(([c, label]) => { const b = best(c); if (b.length >= 2) out.push(`📍 ${label}เด่นของ${nm}: ${b.join(' · ')}`); });
424      const dist = STATE.provinces[base]?.max_days; if (dist) out.push(`🗓️ ข้อมูลของ${nm}รองรับทริปได้สูงสุด ${dist} วัน`);
425      return out;
426    }
บรรทัด 410–417: REGION_TIPS เคล็ดลับตามภูมิภาค
บรรทัด 418–420: provinceTips หาจังหวัดฐาน และเริ่มด้วยเคล็ดลับตามภาค
บรรทัด 421–423: หาสถานที่คะแนนสูงสุด 3 อันดับของแต่ละหมวด ถ้ามีอย่างน้อย 2 ที่ เพิ่มประโยค "…เด่นของจังหวัด"
บรรทัด 424: เพิ่มข้อความจำนวนวันสูงสุดที่ข้อมูลรองรับ
บรรทัด 425–426: คืนรายการ
บรรทัด 427–450  ประกอบและแสดง Tips
427    function buildTips() {
428      const top = STATE.pois.filter(p => TIP_TPL[p.category] && p.open_min !== undefined).sort((a, b) => b.score - a.score).slice(0, 20);
429      const used = new Set(), places = [];
430      top.forEach(p => {
431        const opts = TIP_TPL[p.category].filter(x => x.ok(p) && !(x.dry && wetDays) && !(x.rain && !wetDays) && !used.has(x));
432        const x = opts[Math.floor(Math.random() * opts.length)];   // แม่แบบเดียวกันใช้ได้ครั้งเดียวต่อรอบ ไม่ให้ประโยคซ้ำกันกับหลายสถานที่
433        if (x) { used.add(x); places.push(x.t(p)); }
434      });
435      const shuf = a => a.sort(() => Math.random() - 0.5);
436      const pool = [...weatherLines, ...(weatherLines.length ? [] : seasonLines.map(l => '🌤️ ' + l))];
437      // สลับสถานที่กับเคล็ดลับทั่วไปสลับกัน ไม่ให้ข้อความประเภทเดียวติดกันยาว
438      const g = shuf(generalTips().filter(x => STATE.dev || !x.includes('เทียบอัลกอริทึม'))), pl = shuf(places), rg = shuf(provinceTips());
439      while (g.length || pl.length || rg.length) { if (rg.length) pool.push(rg.pop()); if (pl.length) pool.push(pl.pop()); if (pl.length) pool.push(pl.pop()); if (g.length && Math.random() < 0.6) pool.push(g.pop()); else if (!pl.length && !rg.length) pool.push(g.pop()); }
440      return pool;
441    }
442    function showTip(animate) {
443      const t = $('tipsText'); if (!t || !tipPool.length) return;
444      const set = () => { t.textContent = tipPool[tipIdx++ % tipPool.length]; t.classList.remove('fade'); };
445      if (animate) { t.classList.add('fade'); setTimeout(set, 400); } else set();
446    }
447    function refreshTips(rebuild) {
448      if (!$('tipsText')) return;
449      if (rebuild || tipsFor !== STATE.pois) { tipPool = buildTips(); tipIdx = 0; tipsFor = STATE.pois; showTip(false); }
450    }
บรรทัด 427–429: buildTips เลือก 20 สถานที่คะแนนสูงสุดที่มีเวลาเปิด-ปิด
บรรทัด 430–434: แต่ละสถานที่สุ่มแม่แบบที่เข้าเงื่อนไข (ฝน/ไม่ฝน) และใช้แม่แบบเดียวกันได้ครั้งเดียวต่อรอบ
บรรทัด 435–438: สลับลำดับรายการ ตั้งต้นด้วยข้อความพยากรณ์หรือหมายเหตุฤดูกาล และซ่อนเคล็ดลับ "เทียบอัลกอริทึม" ถ้าไม่ได้อยู่โหมด Developer
บรรทัด 439–440: วนสลับประเภทข้อความไม่ให้ประเภทเดียวติดกันยาว แล้วคืนรายการทั้งหมด
บรรทัด 441: ปิดฟังก์ชัน
บรรทัด 442–446: showTip แสดงข้อความถัดไปเป็นวงกลม ถ้า animate ให้เฟดออกก่อน 0.4 วินาที
บรรทัด 447–450: refreshTips สร้างรายการใหม่ถ้าถูกสั่ง หรือข้อมูลสถานที่เปลี่ยน
บรรทัด 451–482  Tips ภาษาอังกฤษ
451    // ---------- Tips ภาษาอังกฤษ (ใช้เมื่อสลับภาษา) ----------
452    const WMO_EN = c => c === 0 ? '☀️ Clear' : c <= 2 ? '🌤️ Partly cloudy' : c === 3 ? '☁️ Overcast' : c <= 48 ? '🌫️ Fog' : c <= 57 ? '🌦️ Drizzle' : c <= 67 ? '🌧️ Rain' : c <= 82 ? '🌧️ Showers' : '⛈️ Thunderstorm';
453    const TIP_EN = {
454      beach: [p => `🏖️ ${p.name_en}: go in the morning or late afternoon when the sun is milder`, p => `🌊 ${p.name_en}: check the wave flags before swimming`],
455      temple: [p => `🛕 ${p.name_en}: dress modestly and take your shoes off before entering`, p => `🙏 ${p.name_en}: a quiet stop between busier places`],
456      viewpoint: [p => `🌄 ${p.name_en}: best around sunset (closes ${hhmm(p.close_min)})`, p => `👟 ${p.name_en}: wear comfortable shoes`],
457      culture: [p => `🏛️ ${p.name_en}: ${hrs(p).replace('เปิด', 'open').replace('ทั้งวัน', 'all day')} — a good indoor stop in the afternoon`, p => `🎟️ ${p.name_en}: ask the staff for local stories`],
458      market: [p => `🛍️ ${p.name_en}: liveliest in the evening — good for dinner and souvenirs`, p => `🍢 ${p.name_en}: try local snacks, bring a little cash`],
459      activity: [p => `🎈 ${p.name_en}: book ahead in busy periods`, p => `💧 ${p.name_en}: drink plenty of water and follow the safety briefing`],
460    };
461    function buildTipsEN() {
462      const days = SELECTED_DAYS, budget = +$('budget').value || 0, ppl = +$('travelers').value || 1;
463      const pool = [];
464      const iso = Object.keys(wxDaily).sort();
465      iso.forEach(t => { const w = wxDaily[t]; pool.push(`${WMO_EN(w.code)} ${t.slice(5)} ${w.lo}–${w.hi}°C · rain ${w.pop}% (live forecast)`); });
466      if (iso.some(t => wxDaily[t].pop >= 60)) pool.unshift('☔ High chance of rain on some days — bring an umbrella and keep indoor options ready');
467      const top = STATE.pois.filter(p => TIP_EN[p.category]).sort((a, b) => b.score - a.score).slice(0, 14);
468      const places = top.map(p => { const o = TIP_EN[p.category]; return o[Math.floor(Math.random() * o.length)](p); }).sort(() => Math.random() - 0.5);
469      const g = [
470        '💡 Open "Preferences" to like or dislike categories — your plan adapts', '💡 Save plans you like with ★ and reopen them later', '💡 Add a nearby province with the buttons under the province field',
471        '🔄 Swap or remove a stop and the rest of the route is re-optimized', '📅 Export to your calendar or save as PDF to use offline', '👫 Plan together: the Share button gives a live link',
472        '🚗 Travel times assume no traffic — add 20–30% in rush hour', '🍜 Popular lunch spots fill up after 11:30 — arrive a little earlier', '🔋 Carry a power bank and save an offline map', '🧴 Sunscreen, a hat and water are always worth packing',
473      ];
474      if (days >= 4) g.push(`🛌 On a ${days}-day trip, keep one half-day free to rest`);
475      if (budget && days) g.push(`💰 ${fmt(budget)} THB is about ${fmt(budget / days / ppl)} THB per person per day including accommodation`);
476      g.sort(() => Math.random() - 0.5);
477      while (g.length || places.length) { if (places.length) pool.push(places.pop()); if (places.length) pool.push(places.pop()); if (g.length) pool.push(g.pop()); }
478      return pool;
479    }
480    const buildTipsTH = buildTips;
481    buildTips = function () { return window.WET_LANG === 'en' ? buildTipsEN() : buildTipsTH(); };
482    window.addEventListener('wet-lang', () => refreshTips(true));
บรรทัด 452: WMO_EN แปลรหัสอากาศเป็นอังกฤษ
บรรทัด 453–460: TIP_EN แม่แบบประโยคอังกฤษของแต่ละหมวด (ใช้ชื่ออังกฤษของสถานที่)
บรรทัด 461–463: buildTipsEN อ่านจำนวนวัน งบ และจำนวนคน
บรรทัด 464–466: ใส่พยากรณ์รายวันและคำเตือนฝนสูง
บรรทัด 467–468: เลือก 14 สถานที่คะแนนสูงสุดและสุ่มประโยค
บรรทัด 469–475: เคล็ดลับทั่วไปภาษาอังกฤษ พร้อมข้อความตามจำนวนวันและงบ
บรรทัด 476–479: สลับลำดับและวนผสมแล้วคืนรายการ
บรรทัด 480–481: เก็บ buildTips ภาษาไทยไว้ แล้วทับด้วยฟังก์ชันที่เลือกตามภาษา (WET_LANG จาก ➜ frontend/i18n.js)
บรรทัด 482: เมื่อสลับภาษา (เหตุการณ์ wet-lang จาก ➜ frontend/i18n.js) สร้าง Tips ใหม่
บรรทัด 484–493  ติดตั้ง Tips
484    window.wetTips = () => tipPool.slice();   // ใช้ตรวจชุดข้อความ Tips ปัจจุบัน
485    function initTips() {
486      document.querySelector('.pf-col-search')?.insertAdjacentHTML('beforebegin',
487        '<div class="pf-col pf-col-tips"><label class="pf-label">Tips</label><div class="tips-card"><span class="tips-badge">TIPS</span><span class="tips-text" id="tipsText"></span></div></div>');
488      tipsTimer = setInterval(() => { refreshTips(false); showTip(true); }, 10000);
489      setInterval(() => { if (tipsFor !== STATE.pois && STATE.pois.length) refreshTips(true); }, 1000);   // ข้อมูลจังหวัดโหลดเสร็จ/เปลี่ยนจังหวัด
490    }
491
492    const origDateSummary = updateDateSummary;
493    updateDateSummary = function (dates) { origDateSummary(dates); updateHint(); };
บรรทัด 484: wetTips คืนสำเนา Tips ปัจจุบัน (ไว้ตรวจสอบ)
บรรทัด 485–490: initTips แทรกกล่อง Tips ก่อนปุ่มค้นหา (ปุ่มอยู่ใน ➜ frontend/index.html) ตั้งตัวจับเวลาเปลี่ยนข้อความทุก 10 วินาที และตรวจทุกวินาทีว่าข้อมูลสถานที่เปลี่ยนไหม
บรรทัด 492–493: ห่อ ➜ updateDateSummary() ใน frontend/app.js ให้อัปเดต hint ทุกครั้งที่เปลี่ยนวัน
บรรทัด 495–503  หน้าต่างโมดัล
495    // ---------- บันทึก / เปิดแผน ----------
496    function makeModal(id, title, sub) {
497      document.body.insertAdjacentHTML('beforeend', `<div class="modal" id="${id}"><div class="modal-backdrop" data-close></div><div class="modal-card"><div class="modal-head"><div><div class="modal-title">${title}</div><div class="modal-sub">${sub}</div></div><button class="icon-btn" data-close title="ปิด">✕</button></div><div class="modal-body" id="${id}Body"></div></div></div>`);
498      $(id).querySelectorAll('[data-close]').forEach(b => b.onclick = () => toggleModal(id, false));
499    }
500    function toggleModal(id, on) {
501      $(id).classList.toggle('open', on);
502      document.body.style.overflow = on ? 'hidden' : '';
503    }
บรรทัด 496–499: makeModal สร้างโมดัลมาตรฐาน (ชื่อ คำอธิบาย ส่วนเนื้อหา) ต่อท้าย body และผูกปุ่มปิด
บรรทัด 500–503: toggleModal เปิดหรือปิดโมดัลและล็อกการเลื่อนของหน้า
บรรทัด 505–516  บันทึกแผน
505    window.savePlan = function () {
506      const pkg = STATE.selectedPkg;
507      if (!pkg) return;
508      const list = store.get();
509      const d0 = (typeof DATE_PICKER !== 'undefined' && DATE_PICKER?.selectedDates[0]) || null;
510      list.unshift({
511        id: Date.now(), province: getProvince(), label: `${nameOf(getProvince())} · ${pkg.tier} · ${pkg.days.length} วัน`,
512        budget: +$('budget').value, travelers: +$('travelers').value, includeHotel: STATE.includeHotel !== false,
513        start: d0 ? d0.toISOString().slice(0, 10) : null, pkg,
514      });
515      showToast(store.set(list.slice(0, 20)) ? 'บันทึกแผนแล้ว (เก็บในเบราว์เซอร์นี้ ได้สูงสุด 20 แผน)' : 'บันทึกไม่ได้ พื้นที่เบราว์เซอร์เต็มหรือถูกปิดไว้', list.length ? 'ok' : 'error');
516    };
บรรทัด 505–507: savePlan ถ้าไม่มีแผนที่เลือก ออก
บรรทัด 508–514: เพิ่มรายการใหม่ไว้หน้าสุด: id (เวลา) จังหวัด ป้ายชื่อ งบ จำนวนคน ตัวเลือกโรงแรม วันเริ่ม และตัวแผนทั้งก้อน
บรรทัด 515: เก็บสูงสุด 20 แผน แล้วแจ้งผ่าน ➜ showToast() ใน frontend/app.js ว่าสำเร็จหรือไม่
บรรทัด 518–527  รายการแผนที่บันทึก
518    window.openSaved = function () {
519      const list = store.get();
520      $('savedModalBody').innerHTML = list.length ? list.map(p =>
521        `<div class="saved-row"><div><b>${esc(p.label)}</b><div class="pf-hint">งบ ${fmt(p.budget)} ฿ · ${p.travelers} คน · ${new Date(p.id).toLocaleString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH'))}</div></div>
522         <div><button class="pareto-use" onclick="loadSaved(${p.id})">เปิด</button> <button class="pareto-use" onclick="deleteSaved(${p.id})">ลบ</button></div></div>`).join('')
523        : '<p class="pf-hint">ยังไม่มีแผนที่บันทึกไว้ — กดปุ่ม "บันทึก" ในหน้าปรับแต่งทริป</p>';
524      toggleModal('savedModal', true);
525    };
526
527    window.deleteSaved = id => { store.set(store.get().filter(p => p.id !== id)); openSaved(); };
บรรทัด 518–525: openSaved สร้างแถวของแต่ละแผน (ชื่อ งบ จำนวนคน เวลา ปุ่มเปิดและลบ) ถ้าไม่มีแสดงข้อความแนะนำ แล้วเปิดโมดัล
บรรทัด 527: deleteSaved ลบแผนตาม id แล้ววาดรายการใหม่
บรรทัด 529–557  เปิดแผนที่บันทึก
529    window.loadSaved = async function (id) {
530      const p = store.get().find(x => x.id === id);
531      if (!p) return;
532      toggleModal('savedModal', false);
533      baseSlug = p.province.split('+')[0];
534      registerCombo(p.province);
535      $('province').value = p.province;
536      $('provName').textContent = p.province.split('+').map(nameOf).join(' + ');
537      document.querySelectorAll('.prov-item').forEach(i => i.classList.toggle('prov-active', i.dataset.value === baseSlug));
538      await loadPois();
539      renderNeighbors();
540      $('budget').value = p.budget; $('travelers').value = p.travelers;
541      if (p.start && DATE_PICKER) {
542        const d0 = new Date(p.start + 'T00:00:00');
543        DATE_PICKER.setDate([d0, new Date(d0.getTime() + (p.pkg.days.length - 1) * 86400000)], true);
544      }
545      STATE.includeHotel = p.includeHotel;
546      STATE.packages = [p.pkg]; STATE.selectedPkg = JSON.parse(JSON.stringify(p.pkg));
547      STATE.locked.clear(); STATE.excluded.clear();
548      $('detailPanel').style.display = 'block';
549      renderDetail(STATE.selectedPkg);
550      setTimeout(() => {
551        STATE.map.setView(STATE.provinces[p.province].center, STATE.provinces[p.province].zoom);
552        STATE.map.invalidateSize(); drawOnMap(STATE.selectedPkg);
553        $('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
554        setTimeout(syncMapHeight, 150);
555      }, 150);
556      showToast('เปิดแผนที่บันทึกไว้แล้ว', 'ok');
557    };
บรรทัด 529–532: loadSaved หาแผน ปิดโมดัล
บรรทัด 533–537: ตั้งจังหวัดฐาน ลงทะเบียนจังหวัดรวม ตั้งช่องและชื่อ และไฮไลต์จังหวัดในเมนู
บรรทัด 538–539: โหลดสถานที่ของจังหวัดด้วย ➜ loadPois() ใน frontend/app.js และวาดปุ่มจังหวัดข้างเคียง
บรรทัด 540–544: คืนค่าฟอร์ม: งบ จำนวนคน และช่วงวันที่
บรรทัด 545–549: ตั้งสถานะ: ตัวเลือกโรงแรม แพ็กเกจ แผนที่เลือก (ทำสำเนาลึก) ล้างจุดที่ล็อกและลบ แล้วแสดงหน้ารายละเอียดด้วย ➜ renderDetail() ใน frontend/app.js
บรรทัด 550–555: หน่วง 150 มิลลิวินาทีให้หน้าต่างแสดงก่อน แล้วตั้งมุมมองแผนที่ วาดแผน เลื่อนหน้า และปรับความสูงแผนที่ (➜ syncMapHeight() ใน frontend/app.js)
บรรทัด 556: แจ้งว่าเปิดแล้ว
บรรทัด 560–581  เทียบอัลกอริทึม
560    window.openCompare = async function () {
561      if (!STATE.selectedPkg) return;
562      const body = {province: getProvince(), preferences: getPreferences(), budget: +$('budget').value,
563        days: STATE.selectedPkg.days.length, travelers: +$('travelers').value, include_hotel: STATE.includeHotel !== false, seed: 12345};
564      const t = showToast('กำลังรัน Greedy, GA และ Hybrid บนโจทย์เดียวกัน (GA ใช้เวลาหลายวินาที)...', 'loading', 60000);
565      try {
566        const res = await Promise.all(['greedy', 'ga', 'hybrid'].map(async a => {
567          const r = await fetch(`${API_BASE}/api/packages`, {method: 'POST', headers: devHeaders(), body: JSON.stringify({...body, algorithm: a})});
568          if (!r.ok) throw new Error(`${a}: HTTP ${r.status}`);
569          return [a, (await r.json()).packages];
570        }));
571        const km = p => p.days.reduce((s, d) => s + d.distance_km, 0);
572        let rows = '';
573        res.forEach(([a, pk]) => pk.forEach(p => {
574          rows += `<tr class="${a === 'hybrid' ? 'cmp-main' : ''}"><td>${ALGO_NAMES[a]}</td><td>${p.tier}</td><td>${p.total_score.toFixed(1)}</td><td>${fmt(p.total_cost)}</td><td>${km(p).toFixed(0)}</td><td>${p.runtime_ms < 1000 ? Math.round(p.runtime_ms) + ' ms' : (p.runtime_ms / 1000).toFixed(1) + ' s'}</td><td>${p.valid ? '✓' : '✗'}</td></tr>`;
575        }));
576        $('compareModalBody').innerHTML = `<table class="pareto-table"><tr><th>อัลกอริทึม</th><th>แพ็กเกจ</th><th>คะแนนรวม</th><th>ค่าใช้จ่าย (฿)</th><th>ระยะทาง (km)</th><th>เวลาคำนวณ</th><th>ผ่านข้อจำกัด</th></tr>${rows}</table>
577          <p class="pf-hint">โจทย์เดียวกัน (${body.days} วัน งบ ${fmt(body.budget)} ฿ ${body.travelers} คน) seed เดียวกัน — Hybrid เป็นอัลกอริทึมหลัก ส่วน Greedy และ GA เป็นเส้นฐานเปรียบเทียบ</p>`;
578        t.remove();
579        toggleModal('compareModal', true);
580      } catch (e) { t.remove(); showToast(`ผิดพลาด: ${e.message}`, 'error'); }
581    };
บรรทัด 560–563: openCompare ถ้าไม่มีแผนออก เตรียมคำขอด้วยค่าในฟอร์ม และ seed 12345 เพื่อให้ทุกอัลกอริทึมเจอโจทย์เดียวกัน
บรรทัด 564: แจ้งสถานะกำลังรัน
บรรทัด 566–570: ส่งคำขอสามตัวพร้อมกันไปที่ ➜ create_packages() ใน backend/main.py ด้วยอัลกอริทึม Greedy (➜ algorithm/greedy.py) GA (➜ algorithm/genetic.py) และ Hybrid (➜ algorithm/hybrid.py) แล้วรอทุกคำตอบ (ถ้าตัวใดล้มเหลวโยนข้อผิดพลาด)
บรรทัด 571–575: คำนวณระยะทางรวมของแต่ละแผน แล้วสร้างแถวตาราง (แถว Hybrid ถูกเน้น)
บรรทัด 576–577: ใส่ตารางและหมายเหตุในโมดัล
บรรทัด 578–580: ลบข้อความกำลังรัน แล้วเปิดโมดัล ถ้าผิดพลาดแจ้งข้อผิดพลาด
บรรทัด 584–600  ตัวเลือกอาหาร
584    function initDietSelect() {
585      const sel = $('prefDiet'); if (!sel) return;
586      sel.style.display = 'none';
587      sel.insertAdjacentHTML('afterend', '<div class="diet-wrap"><button type="button" class="diet-btn" id="dietBtn"></button><div class="diet-list" id="dietList"></div></div>');
588      const btn = $('dietBtn'), list = $('dietList');
589      const paint = () => {
590        btn.innerHTML = `<span>${esc(sel.selectedOptions[0].textContent)}</span><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>`;
591        list.innerHTML = [...sel.options].map(o => `<div class="diet-item${o.value === sel.value ? ' on' : ''}" data-v="${o.value}">${esc(o.textContent)}</div>`).join('');
592      };
593      btn.onclick = e => { e.stopPropagation(); list.classList.toggle('open'); btn.classList.toggle('open'); };
594      list.onclick = e => {
595        const it = e.target.closest('.diet-item'); if (!it) return;
596        sel.value = it.dataset.v; updatePrefSummary(); paint(); list.classList.remove('open'); btn.classList.remove('open');
597      };
598      document.addEventListener('click', () => { list.classList.remove('open'); btn.classList.remove('open'); });
599      paint();
600    }
บรรทัด 584–587: initDietSelect ซ่อน select เดิม (➜ frontend/index.html ช่อง #prefDiet) และแทรกปุ่มกับรายการแทน
บรรทัด 588–592: paint วาดข้อความที่เลือกและรายการตัวเลือก
บรรทัด 593: คลิกปุ่มเพื่อเปิดปิดรายการ
บรรทัด 594–597: คลิกรายการเพื่อตั้งค่า select เรียก ➜ updatePrefSummary() ใน frontend/app.js วาดใหม่ และปิดรายการ
บรรทัด 598–599: คลิกที่อื่นเพื่อปิดรายการ แล้ววาดครั้งแรก
บรรทัด 603–622  โหมด Developer ต้องใส่รหัส
603    const origToggleDev = toggleDevMode;
604    toggleDevMode = function () {
605      if (STATE.dev) return origToggleDev();
606      $('devPw').value = ''; $('devErr').textContent = '';
607      toggleModal('devModal', true); setTimeout(() => $('devPw').focus(), 50);
608    };
609    window.submitDevPw = async function () {   // ตรวจรหัสที่ backend (ไม่ฝังรหัสไว้ในหน้าเว็บ)
610      try {
611        const r = await fetch(`${API_BASE}/api/dev/unlock`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({password: $('devPw').value})});
612        if (r.ok) {
613          try { localStorage.setItem('wet_dev_token', (await r.json()).token); } catch (e) { /* ไม่เก็บค่า */ }
614          toggleModal('devModal', false); origToggleDev();
615        } else {
616          $('devErr').textContent = (await r.json().catch(() => ({}))).detail || 'รหัสผ่านไม่ถูกต้อง';
617          $('devPw').select();
618        }
619      } catch (e) { $('devErr').textContent = 'เชื่อมต่อ backend ไม่ได้'; }
620    };
621    // เปิดหน้าใหม่ขณะจำโหมด Developer ไว้ แต่โทเค็นหมดอายุ (เซิร์ฟเวอร์รีสตาร์ท) → ปิดโหมดให้
622    setTimeout(() => { if (STATE.dev) fetch(`${API_BASE}/api/dev/check`, {headers: devHeaders()}).then(r => r.json()).then(j => { if (!j.ok) setDevMode(false); }).catch(() => {}); }, 1500);
บรรทัด 603–608: ห่อ ➜ toggleDevMode() ใน frontend/app.js: ถ้าเปิดอยู่แล้วเรียกของเดิมเพื่อปิด ไม่เช่นนั้นล้างช่องรหัสแล้วเปิดโมดัลถามรหัส
บรรทัด 609–620: submitDevPw ส่งรหัสไปตรวจที่ ➜ dev_unlock() ใน backend/main.py (ไม่ฝังรหัสไว้ในหน้าเว็บ) ถ้าถูก เก็บโทเค็นใน localStorage ปิดโมดัล และเปิดโหมดด้วยฟังก์ชันเดิม ถ้าผิดแสดงข้อความและเลือกช่องรหัส ถ้าเชื่อมต่อไม่ได้แจ้ง
บรรทัด 621–622: ถ้าเปิดหน้าด้วยโหมด Developer ที่จำไว้แต่โทเค็นหมดอายุ (เซิร์ฟเวอร์รีสตาร์ท) ตรวจกับ ➜ dev_check() ใน backend/main.py แล้วปิดโหมด (➜ setDevMode() ใน frontend/app.js)
บรรทัด 625–638  ติดตั้งปุ่มและหน้าต่าง
625    makeModal('savedModal', 'แผนของฉัน', 'แผนที่บันทึกไว้ในเบราว์เซอร์นี้');
626    makeModal('compareModal', 'เปรียบเทียบอัลกอริทึม', 'Greedy · Genetic Algorithm · Hybrid บนโจทย์เดียวกัน');
627    document.body.insertAdjacentHTML('beforeend', '<div class="modal" id="devModal"><div class="modal-backdrop" data-close></div><div class="modal-card dev-modal-card"><div class="modal-title">โหมด Developer</div><div class="modal-sub">กรอกรหัสผ่านเพื่อเข้าใช้งาน</div><input type="password" id="devPw" placeholder="รหัสผ่าน" autocomplete="off" onkeydown="if(event.keyCode===13)submitDevPw()"><div class="dev-err" id="devErr"></div><button class="pareto-use" onclick="submitDevPw()">เข้าสู่โหมด Developer</button></div></div>');
628    $('devModal').querySelectorAll('[data-close]').forEach(b => b.onclick = () => toggleModal('devModal', false));
629    initTips();
630    initDietSelect();
631    document.querySelector('.topbar-actions')?.insertAdjacentHTML('afterbegin', '<a class="icon-btn results-link dev-only" href="results.html" title="ผลการทดลอง" style="text-decoration:none;font-size:.8rem;width:auto;padding:0 .7rem">ผลทดลอง</a>');
632    document.querySelector('.topbar-actions')?.insertAdjacentHTML('afterbegin', '<button class="icon-btn saved-btn" onclick="openSaved()" title="แผนที่บันทึกไว้">★</button>');
633    document.querySelector('.detail-actions')?.insertAdjacentHTML('afterbegin',
634      '<button class="reshuffle-btn export-btn" onclick="savePlan()" title="บันทึกแผนนี้ไว้ในเบราว์เซอร์">★ บันทึก</button>' +
635      '<span class="hist-group"><button type="button" class="reshuffle-btn export-btn hist-btn disabled" id="undoBtn" onclick="undoEdit()" title="ย้อนกลับ (Ctrl+Z)"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14L4 9l5-5M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/></svg></button>' +
636      '<button type="button" class="reshuffle-btn export-btn hist-btn disabled" id="redoBtn" onclick="redoEdit()" title="เดินหน้า (Ctrl+Y)"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14l5-5-5-5M20 9H9.5a5.5 5.5 0 0 0 0 11H13"/></svg></button></span>' +
637      '<button class="reshuffle-btn export-btn dev-only" onclick="openCompare()" title="เทียบ Greedy / GA / Hybrid บนโจทย์เดียวกัน">⇄ เทียบอัลกอริทึม</button>');
638  })();
บรรทัด 625–626: สร้างโมดัลแผนของฉัน และโมดัลเทียบอัลกอริทึม
บรรทัด 627–628: สร้างโมดัลรหัสผ่านโหมด Developer และผูกปุ่มปิด
บรรทัด 629–630: เริ่ม Tips และตัวเลือกอาหาร
บรรทัด 631: เพิ่มลิงก์ "ผลทดลอง" ไป ➜ frontend/results.html (แสดงเฉพาะโหมด Developer) ที่แถบบน
บรรทัด 632: เพิ่มปุ่มดาวเปิดรายการแผนที่บันทึก
บรรทัด 633–637: เพิ่มปุ่มในกล่องปุ่มของแผน: บันทึก ย้อนกลับและเดินหน้า (➜ undoEdit() ใน frontend/app.js ➜ recordHistory() ใน frontend/app.js) และเทียบอัลกอริทึม (เฉพาะโหมด Developer)
บรรทัด 638: ปิด IIFE แรก
บรรทัด 641–679  ประวัติการแจ้งเตือน
641  // ---------- ปุ่มประวัติการแจ้งเตือน (ลอยมุมขวาล่าง เลื่อนตามผู้ใช้) ----------
642  (function () {
643    const KEY = 'wet_notif', MAX = 50;
644    let list = [], unread = 0;
645    try { list = JSON.parse(sessionStorage.getItem(KEY) || '[]'); } catch (e) { list = []; }
646    const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* ไม่เก็บค่า */ } };
647    const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
648    const btn = document.createElement('button');
649    btn.type = 'button'; btn.id = 'notifBtn'; btn.className = 'notif-btn'; btn.title = 'ประวัติการแจ้งเตือน';
650    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 0 1-3.46 0"/></svg><span class="notif-badge" hidden></span>';
651    const panel = document.createElement('div');
652    panel.id = 'notifPanel'; panel.className = 'notif-panel'; panel.hidden = true;
653    panel.innerHTML = '<div class="notif-head"><b>ประวัติการแจ้งเตือน</b><button type="button" class="notif-clear">ล้างทั้งหมด</button></div><div class="notif-list"></div>';
654    document.body.append(btn, panel);
655    const badge = btn.querySelector('.notif-badge'), box = panel.querySelector('.notif-list');
656    function render() {
657      badge.hidden = !unread; badge.textContent = unread > 9 ? '9+' : unread;
658      box.innerHTML = list.length ? list.slice().reverse().map(n =>
659        `<div class="notif-item ${n.k}"><span class="notif-dot"></span><div><div class="notif-msg">${esc(n.m)}</div><div class="notif-time">${esc(n.t)}</div></div></div>`).join('')
660        : '<div class="notif-empty">ยังไม่มีการแจ้งเตือน</div>';
661    }
662    function add(msg, kind) {
663      const m = String(msg).replace(/<[^>]*>/g, '').trim();
664      if (!m || kind === 'loading') return;
665      const last = list[list.length - 1];
666      if (last && last.m === m && Date.now() - last.ts < 1500) return;   // ข้อความซ้ำติดกัน (ปุ่มถูกกดซ้ำ)
667      list.push({m, k: kind === 'error' ? 'error' : 'ok', t: new Date().toLocaleTimeString('th-TH', {hour12: false}), ts: Date.now()});
668      if (list.length > MAX) list.shift();
669      if (panel.hidden) unread++;
670      save(); render();
671    }
672    const orig = window.showToast;
673    window.showToast = function (msg, kind, duration) { try { add(msg, kind); } catch (e) { /* ประวัติพังต้องไม่ทำให้แจ้งเตือนหาย */ } return orig.apply(this, arguments); };
674    btn.addEventListener('click', e => { e.stopPropagation(); panel.hidden = !panel.hidden; if (!panel.hidden) { unread = 0; render(); } });
675    panel.querySelector('.notif-clear').addEventListener('click', () => { list = []; unread = 0; save(); render(); });
676    document.addEventListener('click', e => { if (!panel.hidden && !panel.contains(e.target) && e.target !== btn) panel.hidden = true; });
677    document.addEventListener('keydown', e => { if (e.key === 'Escape') panel.hidden = true; });
678    render();
679  })();
บรรทัด 643–646: IIFE ที่สอง: ค่าคงที่ จำนวนสูงสุด 50 รายการ อ่านรายการจาก sessionStorage และฟังก์ชัน save
บรรทัด 647: esc ป้องกัน XSS (สำเนาในขอบเขตนี้)
บรรทัด 648–650: สร้างปุ่มกระดิ่งลอยมุมขวาล่าง
บรรทัด 651–655: สร้างแผงรายการและต่อเข้า body
บรรทัด 656–661: render แสดงป้ายจำนวนที่ยังไม่อ่าน และรายการล่าสุดก่อน
บรรทัด 662–671: add ลบแท็ก HTML ข้ามข้อความว่าง/สถานะ loading และข้อความซ้ำภายใน 1.5 วินาที แล้วจดรายการ (สูงสุด 50) นับยังไม่อ่านถ้าแผงปิดอยู่ และบันทึก
บรรทัด 672–673: ห่อ ➜ showToast() ใน frontend/app.js: บันทึกประวัติก่อน (พังได้ ไม่ทำให้แจ้งเตือนหาย) แล้วเรียกของเดิม
บรรทัด 674–675: คลิกกระดิ่งเปิดปิดแผงและล้างยังไม่อ่าน คลิก "ล้างทั้งหมด" ล้างรายการ
บรรทัด 676–677: คลิกข้างนอกหรือกด Esc เพื่อปิดแผง
บรรทัด 678–679: วาดครั้งแรก แล้วปิด IIFE

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
backend/main.py
data/make_banners.py
frontend/app.js
frontend/i18n.js
frontend/index.html
frontend/results.html
frontend/style.css