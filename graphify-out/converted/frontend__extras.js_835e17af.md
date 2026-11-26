<!-- converted from frontend__extras.js.docx -->

คู่มือโค้ด: frontend/extras.js
ส่วนเสริมของหน้าเว็บ: แบนเนอร์ อากาศ ลากวาง Tips แผนที่บันทึก
ไฟล์ต้นฉบับ: frontend/extras.js (639 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ไฟล์ที่โหลดต่อจาก ➜ frontend/app.js และ "ห่อ" (wrap) ฟังก์ชันของ app.js โดยเก็บฟังก์ชันเดิมไว้ในตัวแปร orig... แล้วกำหนดฟังก์ชันใหม่ทับ ที่เรียกของเดิมก่อนแล้วเพิ่มงานของตัวเอง (เช่น ➜ onProvinceChange() ใน frontend/app.js ➜ renderDetail() ใน frontend/app.js ➜ drawOnMap() ใน frontend/app.js ➜ validateInputs() ใน frontend/app.js) จึงต้องมีตัวแปรกลางของ app.js เช่น STATE DATE_PICKER SELECTED_DAYS ฟีเจอร์ในไฟล์: แบนเนอร์จังหวัด จำกัดจำนวนวัน หมายเหตุฤดูกาล พยากรณ์อากาศจริง ลากวางการ์ดแบบ pointer สลับสถานที่ในร่ม กล่อง Tips บันทึกและเปิดแผน เทียบอัลกอริทึม ล็อกโหมด Developer ด้วยรหัสผ่าน และประวัติการแจ้งเตือน ไฟล์ใช้องค์ประกอบจาก ➜ frontend/index.html (เช่น #dateSummary #provSelect .detail-actions) และสไตล์จาก ➜ frontend/style.css ข้อความภาษาอังกฤษของ Tips เป็นของไฟล์นี้เอง ส่วนข้อความอื่นแปลโดย ➜ frontend/i18n.js

บรรทัด 3–10  หัวไฟล์ และตัวช่วย
3  (function () {
4    const $ = id => document.getElementById(id);
5    const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
6    const store = {
7      get() { try { return JSON.parse(localStorage.getItem('wet_saved') || '[]'); } catch (e) { return []; } },
8      set(v) { try { localStorage.setItem('wet_saved', JSON.stringify(v)); return true; } catch (e) { return false; } },
9    };
10    let baseSlug = null;
บรรทัด 3: เปิด IIFE แรก (ไฟล์มี IIFE สองก้อน ก้อนที่สองเริ่มที่บรรทัด 602)
บรรทัด 4: $ ย่อ getElementById
บรรทัด 5: esc ป้องกัน XSS โดยแปลงอักขระพิเศษ HTML (& < > ") ก่อนนำข้อความไปใส่ innerHTML
บรรทัด 6–9: store อ่าน/เขียนรายการแผนที่บันทึกใน localStorage คีย์ wet_saved ถ้าผิดพลาด (เช่นโหมดส่วนตัว) คืนรายการว่างหรือ false
บรรทัด 10: baseSlug จังหวัดที่ผู้ใช้เลือก
บรรทัด 12–12  ตัวช่วยชื่อจังหวัด
12    const nameOf = s => STATE.provinces[s]?.name_th || s;
บรรทัด 12: nameOf ชื่อไทยของ slug (ไม่มีใช้ slug เอง)
บรรทัด 14–28  แบนเนอร์จังหวัด
14    // แบนเนอร์ประจำจังหวัด: ใช้ img/provinces/<slug>.jpg (ภาพถ่ายถ้ามี) ไม่งั้นใช้ .svg ที่สร้างอัตโนมัติ; สลับด้วย cross-fade
15    let bannerSlug = 'phuket';
16    function setBanner(slug) {
17      const base = slug.split('+')[0]; if (base === bannerSlug) return; bannerSlug = base;
18      const hero = document.querySelector('.hero-visual'), old = hero?.querySelector('.hero-bg'); if (!hero || !old) return;
19      const cands = base === 'phuket' ? ['BG2.jpg'] : [`img/provinces/${base}.jpg`, `img/provinces/${base}.svg`];
20      const apply = url => {
21        if (bannerSlug !== base) return;   // ผู้ใช้เปลี่ยนจังหวัดไปแล้ว
22        const nu = document.createElement('div'); nu.className = 'hero-bg'; nu.style.backgroundImage = `url('${url}')`; nu.style.opacity = '0';
23        old.after(nu); requestAnimationFrame(() => requestAnimationFrame(() => { nu.style.opacity = '1'; }));
24        setTimeout(() => hero.querySelectorAll('.hero-bg').forEach(e => { if (e !== nu) e.remove(); }), 700);
25      };
26      (function tryNext(i) { if (i >= cands.length) return; const im = new Image(); im.onload = () => apply(cands[i]); im.onerror = () => tryNext(i + 1); im.src = cands[i]; })(0);
27      const lbl = document.querySelector('.hero-label'); if (lbl) lbl.textContent = (STATE.provinces[base]?.name_en || 'Your Travel Services');
28    }
บรรทัด 14–15: คอมเมนต์และตัวแปรจังหวัดของแบนเนอร์ปัจจุบัน (ตั้งต้นภูเก็ต) ภาพมาจาก img/provinces ที่สร้างโดย ➜ data/make_banners.py
บรรทัด 16–17: setBanner ใช้ slug ของจังหวัดที่เลือก (ตัดส่วนหลังเครื่องหมาย + ออกเผื่อ slug เก่า) ถ้าเป็นจังหวัดเดิมไม่ทำอะไร
บรรทัด 18: หา hero และภาพเดิม ถ้าไม่มีก็ออก
บรรทัด 19: รายการภาพที่ลอง: ภูเก็ตใช้ BG2.jpg จังหวัดอื่นลอง .jpg ก่อน แล้ว .svg
บรรทัด 20–25: apply สร้างชั้นภาพใหม่โปร่งใส ต่อท้ายภาพเดิม ค่อยเฟดเข้า และลบภาพเก่าหลัง 0.7 วินาที (ข้ามถ้าผู้ใช้เปลี่ยนจังหวัดไปแล้ว)
บรรทัด 26: ลองโหลดภาพตามลำดับ ถ้าโหลดไม่ได้ลองภาพถัดไป
บรรทัด 27: เปลี่ยนป้ายเล็กบนภาพเป็นชื่ออังกฤษของจังหวัด
บรรทัด 30–43  ห่อฟังก์ชันโหลดจังหวัด
30    const origProvinceChange = onProvinceChange;
31    onProvinceChange = async function (slug) {
32      setBanner(slug);
33      baseSlug = slug;
34      await origProvinceChange(slug);
35      updateHint();
36    };
37
38    const origLoadProvinces = loadProvinces;
39    loadProvinces = async function () {
40      await origLoadProvinces();
41      baseSlug = getProvince();
42      updateHint();
43    };
บรรทัด 30–36: ห่อ ➜ onProvinceChange() ใน frontend/app.js: ตั้งแบนเนอร์ จดจังหวัดที่เลือก เรียกของเดิมรอให้เสร็จ แล้วปรับข้อความ hint
บรรทัด 38–43: ห่อ ➜ loadProvinces() ใน frontend/app.js: หลังโหลดรายการจังหวัดจาก ➜ get_provinces() ใน backend/main.py เสร็จ ตั้งจังหวัดที่เลือกและปรับข้อความ hint
บรรทัด 45–53  จำกัดจำนวนวัน
45    // ---------- จำกัดจำนวนวันตามข้อมูล + หมายเหตุฤดูกาล ----------
46    const maxDays = () => STATE.provinces[getProvince()]?.max_days || 7;
47
48    const origValidate = validateInputs;
49    validateInputs = function (budget, days, travelers) {
50      const errs = origValidate(budget, days, travelers);
51      if (days > maxDays()) errs.push(`ข้อมูลของ ${nameOf(getProvince())} รองรับสูงสุด ${maxDays()} วัน (สถานที่หรือร้านอาหารไม่พอสำหรับ ${days} วัน) ลองลดจำนวนวัน`);
52      return errs;
53    };
บรรทัด 46: maxDays จำนวนวันสูงสุดตามข้อมูลของจังหวัดที่เลือก (ไม่ทราบใช้ 7)
บรรทัด 48–53: ห่อ ➜ validateInputs() ใน frontend/app.js: เรียกของเดิมแล้วถ้าจำนวนวันเกิน เพิ่มข้อความข้อผิดพลาดบอกว่าข้อมูลของจังหวัดนั้นรองรับกี่วัน
บรรทัด 55–74  หมายเหตุฤดูกาล
55    const ANDAMAN = ['phuket', 'krabi', 'phangnga', 'ranong', 'trang', 'satun'];
56    const GULF_SOUTH = ['suratthani', 'samui', 'nakhonsithammarat', 'chumphon', 'songkhla', 'pattani', 'yala', 'narathiwat', 'phatthalung'];
57    // ข้อมูลภูมิอากาศทั่วไปตามเดือน (คงที่ ไม่ใช่พยากรณ์อากาศ)
58    function seasonNote(slug, month) {   // month 1-12
59      const s = slug.split('+')[0], region = STATE.provinces[s]?.region || '';
60      const notes = [];
61      if (ANDAMAN.includes(s)) {
62        if (month >= 5 && month <= 10) notes.push('ฝั่งอันดามันเป็นฤดูมรสุม คลื่นลมแรง ทริปเกาะและกิจกรรมทางทะเลอาจงดบางวัน');
63        else notes.push('ช่วงนี้ทะเลฝั่งอันดามันสงบ เหมาะกับหาดและเกาะ (ฤดูท่องเที่ยวหลัก)');
64      } else if (GULF_SOUTH.includes(s) && (month >= 10 || month <= 1)) {
65        notes.push('ฝั่งอ่าวไทยตอนล่างฝนชุกช่วง ต.ค.–ม.ค. ควรเผื่อแผนสำรองในร่ม');
66      } else if (region === 'ภาคเหนือ' && month >= 2 && month <= 4) {
67        notes.push('ภาคเหนือช่วง ก.พ.–เม.ย. มักมีหมอกควันและฝุ่น PM2.5 จุดชมวิวอาจไม่ชัด');
68      } else if (region === 'ภาคเหนือ' && (month >= 11 || month <= 1)) {
69        notes.push('ภาคเหนือช่วงนี้อากาศเย็นสบาย เหมาะกับจุดชมวิวและกิจกรรมกลางแจ้ง (ฤดูท่องเที่ยวหลัก)');
70      }
71      if (month >= 3 && month <= 5) notes.push('ช่วง มี.ค.–พ.ค. อากาศร้อนจัด ควรเที่ยวกลางแจ้งช่วงเช้าหรือเย็น');
72      else if (month >= 6 && month <= 10 && !ANDAMAN.includes(s)) notes.push('ช่วง มิ.ย.–ต.ค. เป็นฤดูฝน ควรพกร่มและเผื่อสถานที่ในร่ม');
73      return notes;
74    }
บรรทัด 55–56: รายชื่อ slug จังหวัดฝั่งอันดามัน และฝั่งอ่าวไทยตอนล่าง
บรรทัด 58–60: seasonNote รับ slug และเดือน (1-12) หาจังหวัดฐานและภาค เตรียมรายการข้อความ
บรรทัด 61–63: อันดามัน: พ.ค.–ต.ค. เป็นฤดูมรสุม ช่วงอื่นทะเลสงบ
บรรทัด 64–65: อ่าวไทยตอนล่าง: ฝนชุก ต.ค.–ม.ค.
บรรทัด 66–69: ภาคเหนือ: ก.พ.–เม.ย. หมอกควัน PM2.5 และ พ.ย.–ม.ค. อากาศเย็น
บรรทัด 71–72: ทั่วประเทศ: มี.ค.–พ.ค. ร้อนจัด และ มิ.ย.–ต.ค. ฤดูฝน (ยกเว้นอันดามันที่พูดไปแล้ว)
บรรทัด 73: คืนรายการข้อความ
บรรทัด 76–85  อัปเดตคำแนะนำ
76    function updateHint() {
77      let el = $('seasonNote');
78      if (!el) { $('dateSummary').insertAdjacentHTML('afterend', '<div id="seasonNote" class="season-note"></div>'); el = $('seasonNote'); }
79      const dates = (typeof DATE_PICKER !== 'undefined' && DATE_PICKER) ? DATE_PICKER.selectedDates : [];
80      const slug = getProvince();
81      el.innerHTML = STATE.provinces[slug] ? `<div>ข้อมูลรองรับสูงสุด ${maxDays()} วันสำหรับ ${esc(nameOf(slug))}</div>` : '';
82      seasonLines = dates.length ? seasonNote(slug, dates[0].getMonth() + 1) : [];
83      refreshTips(true);
84      loadWeather(slug, dates);
85    }
บรรทัด 76–78: updateHint หากล่อง #seasonNote ถ้ายังไม่มีสร้างต่อจาก #dateSummary
บรรทัด 79–81: อ่านวันที่เลือกจาก DATE_PICKER ของ app.js แล้วเขียนข้อความจำนวนวันสูงสุดของจังหวัด
บรรทัด 82: สร้างหมายเหตุฤดูกาลจากเดือนของวันเริ่ม
บรรทัด 83–84: รีเฟรช Tips และโหลดพยากรณ์อากาศ
บรรทัด 89–118  พยากรณ์อากาศจริง
89    const WMO = c => c === 0 ? '☀️ ท้องฟ้าแจ่มใส' : c <= 2 ? '🌤️ มีเมฆบางส่วน' : c === 3 ? '☁️ เมฆมาก' : c <= 48 ? '🌫️ หมอก' : c <= 57 ? '🌦️ ฝนปรอย' : c <= 67 ? '🌧️ ฝนตก' : c <= 82 ? '🌧️ ฝนตกเป็นช่วง' : '⛈️ พายุฝนฟ้าคะนอง';
90    const wxCache = {};
91    let weatherLines = [], wxToken = 0, wetDays = false, wxDaily = {};
92    async function loadWeather(slug, dates) {
93      const my = ++wxToken, pv = STATE.provinces[slug];
94      weatherLines = []; wetDays = false; wxDaily = {};
95      if (!pv || !dates.length) return;
96      const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
97      const start = iso(dates[0]), end = iso(dates[dates.length - 1]);
98      const key = `${pv.center.map(x => x.toFixed(2))}|${start}|${end}`;
99      try {
100        if (!wxCache[key]) {
101          const url = `https://api.open-meteo.com/v1/forecast?latitude=${pv.center[0].toFixed(3)}&longitude=${pv.center[1].toFixed(3)}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FBangkok&start_date=${start}&end_date=${end}`;
102          const r = await fetch(url);
103          if (!r.ok) throw new Error(r.status);   // เช่น วันที่เกิน 16 วันข้างหน้า → 400
104          wxCache[key] = await r.json();
105        }
106        const d = wxCache[key].daily;
107        const fmtD = s => new Date(s + 'T00:00:00').toLocaleDateString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH'), {day: 'numeric', month: 'short'});
108        const wet = [];
109        d.time.forEach((t, i) => { wxDaily[t] = {code: d.weathercode[i], lo: Math.round(d.temperature_2m_min[i]), hi: Math.round(d.temperature_2m_max[i]), pop: d.precipitation_probability_max[i] ?? 0}; });
110        weatherLines = d.time.map((t, i) => {
111          if ((d.precipitation_probability_max[i] ?? 0) >= 60) wet.push(fmtD(t));
112          return `${WMO(d.weathercode[i])} ${fmtD(t)} ${Math.round(d.temperature_2m_min[i])}–${Math.round(d.temperature_2m_max[i])}°C โอกาสฝน ${d.precipitation_probability_max[i] ?? '-'}% (พยากรณ์จริง)`;
113        });
114        wetDays = wet.length > 0;
115        if (wet.length) weatherLines.unshift(`☔ ${wet.slice(0, 3).join(', ')} มีโอกาสฝนสูง ควรพกร่มและเผื่อสถานที่ในร่ม`);
116      } catch (e) { weatherLines = []; }
117      if (my === wxToken) { refreshTips(true); if (STATE.selectedPkg && $('detailPanel').style.display !== 'none') decorateWeather(STATE.selectedPkg); }
118    }
บรรทัด 89: WMO แปลงรหัสอากาศมาตรฐาน WMO เป็นข้อความไทยพร้อมอีโมจิ
บรรทัด 90–91: แคชผลตามพิกัดและช่วงวันที่ และตัวแปรสถานะ (บรรทัดพยากรณ์ โทเค็นกันผลซ้อน มีวันฝนหรือไม่ ข้อมูลรายวัน)
บรรทัด 92–95: loadWeather เพิ่มโทเค็น ล้างผลเก่า ถ้าไม่มีจังหวัดหรือวันที่ ออก
บรรทัด 96–98: สร้างวันที่ในรูป ISO และกุญแจแคช
บรรทัด 99–105: ถ้าไม่มีในแคช เรียก API ของ Open-Meteo ด้วยพิกัดศูนย์กลางจังหวัดเท่านั้น (ไม่ส่งข้อมูลผู้ใช้) ถ้าตอบผิดพลาด (เช่นเกิน 16 วัน) โยนข้อผิดพลาด
บรรทัด 106–109: อ่านผลรายวัน จัดรูปวันที่ตามภาษา และเก็บอุณหภูมิ รหัสอากาศ และโอกาสฝนของแต่ละวันลง wxDaily
บรรทัด 110–113: สร้างข้อความพยากรณ์รายวัน และจดวันที่โอกาสฝนตั้งแต่ 60%
บรรทัด 114–115: ตั้งธง wetDays และเพิ่มคำเตือนฝนไว้หน้าสุดของรายการ
บรรทัด 116: ถ้าผิดพลาดล้างข้อความพยากรณ์ (หน้าเว็บใช้หมายเหตุฤดูกาลแทน)
บรรทัด 117: ถ้าไม่มีคำขอใหม่แทรก รีเฟรช Tips และตกแต่งหน้าแผนที่เปิดอยู่
บรรทัด 120–142  ตกแต่งหน้าแผนด้วยอากาศ
120    const OUTDOOR = ['beach', 'viewpoint', 'activity'];
121    const dayIso = i => { const d0 = DATE_PICKER?.selectedDates[0]; if (!d0) return null; const d = new Date(d0.getTime() + i * 86400000); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
122    window.dayRainPop = i => (wxDaily[dayIso(i)] || {}).pop || 0;   // โอกาสฝน (%) ของวันที่ i ใช้ในหน้าเปลี่ยนสถานที่
123    window.OUTDOOR_CATS = OUTDOOR;
124    function decorateWeather(pkg) {
125      document.querySelectorAll('#dayPanels .day-panel').forEach((panel, i) => {
126        panel.querySelectorAll('.wx-chip, .rain-banner').forEach(e => e.remove());
127        const w = wxDaily[dayIso(i)]; if (!w) return;
128        panel.querySelector('.day-stats')?.insertAdjacentHTML('afterbegin', `<span class="wx-chip" title="พยากรณ์จริงจาก Open-Meteo">${WMO(w.code).split(' ')[0]} ${w.lo}–${w.hi}°C · ฝน ${w.pop}%</span>`);
129        const outdoor = pkg.days[i]?.pois.filter(p => OUTDOOR.includes(p.category)).length || 0;
130        if (w.pop >= 60) panel.querySelectorAll('.poi-item').forEach(li => {   // ไอคอนฝนที่การ์ดสถานที่กลางแจ้งในวันที่ฝนตก
131          const p = pkg.days[i]?.pois.find(x => x.id === li.dataset.id);
132          if (p && OUTDOOR.includes(p.category) && !li.querySelector('.rain-ic')) li.querySelector('.poi-name')?.insertAdjacentHTML('beforeend', `<span class="rain-ic" title="${window.WET_LANG === 'en' ? 'Outdoor place, it may rain' : 'สถานที่กลางแจ้ง อาจมีฝนตกได้'}"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 14a4 4 0 0 0 0-8 5.5 5.5 0 0 0-10.6 1.5A3.5 3.5 0 0 0 7 14"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/></svg></span>`);
133        });
134        if (w.pop >= 60 && outdoor) panel.querySelector('.day-head').insertAdjacentHTML('afterend', `<div class="rain-banner">☔ วันนี้โอกาสฝน ${w.pop}% แต่มีสถานที่กลางแจ้ง ${outdoor} จุด <button type="button" onclick="indoorSwap(${i})">สลับเป็นสถานที่ในร่ม</button></div>`);
135      });
136    }
137    const origRenderDetail = renderDetail;
138    renderDetail = function (pkg) {
139      if (!pkg._orig) setHidden(pkg, '_orig', JSON.parse(JSON.stringify(pkg)));   // จำแผนตั้งต้นที่ระบบคำนวณไว้ (ใช้กับปุ่มคืนค่าเดิม)
140      origRenderDetail(pkg);
141      for (const fn of [decorateWeather, decorateWarnings, enableDrag, recordHistory]) { try { fn(pkg); } catch (e) { console.error(fn.name, e); } }   // ข้อผิดพลาดในตัวตกแต่งต้องไม่ทำให้การลากการ์ดใช้ไม่ได้
142    };
บรรทัด 120: ประเภทสถานที่กลางแจ้ง
บรรทัด 121: dayIso คำนวณวันที่ ISO ของวันที่ i ในแผนจากวันเริ่มที่เลือก
บรรทัด 122–123: เปิด dayRainPop (โอกาสฝนของวัน) และ OUTDOOR_CATS ให้ ➜ frontend/app.js ใช้ในหน้าเลือกสถานที่
บรรทัด 124–128: decorateWeather ล้างป้ายเก่า แล้วเติมป้ายอุณหภูมิและโอกาสฝนในแถบสถิติของแต่ละวัน
บรรทัด 129: นับสถานที่กลางแจ้งของวันนั้น
บรรทัด 130–133: ถ้าโอกาสฝน ≥ 60% ใส่ไอคอนฝนที่การ์ดสถานที่กลางแจ้ง
บรรทัด 134: ถ้ามีสถานที่กลางแจ้งและฝนตกหนัก แทรกแถบเตือนพร้อมปุ่มสลับเป็นสถานที่ในร่ม (เรียก indoorSwap ด้านล่าง)
บรรทัด 135–136: ปิดการวนและฟังก์ชัน
บรรทัด 137–142: ห่อ ➜ renderDetail() ใน frontend/app.js: จำสำเนาแผนตั้งต้น (ซ่อนจากการแปลงเป็น JSON ด้วย setHidden) เรียกของเดิม แล้วเรียกตัวตกแต่งสี่ตัว (อากาศ คำเตือน ลากวาง และบันทึกประวัติ ➜ recordHistory() ใน frontend/app.js) ทีละตัวใน try/catch ให้ตัวหนึ่งพังไม่ทำให้ทั้งหน้าพัง
บรรทัด 144–158  แสดงคำเตือนที่การ์ด
144    // แสดงคำเตือนที่การ์ด (สีแดง + กล่องข้อความใต้การ์ด) เฉพาะ "อาจไปไม่ทันเวลาปิด" / "อาจไปถึงก่อนร้านเปิด" ค้างจนกว่าจะแก้หรือลากสลับใหม่
145    function decorateWarnings(pkg) {
146      document.querySelectorAll('.plan-warn, .poi-err-box').forEach(e => e.remove());
147      document.querySelectorAll('.poi-item.poi-error').forEach(e => e.classList.remove('poi-error'));
148      const panels = document.querySelectorAll('#dayPanels .day-panel'), clock = m => fmtClock(Math.round(m)), en = window.WET_LANG === 'en';
149      uiWarnings(pkg).forEach(w => {
150        const li = panels[w.d]?.querySelector(`.poi-item[data-id="${w.id}"]`); if (!li) return;
151        li.classList.add('poi-error');
152        let box = li.nextElementSibling; if (!box || !box.classList.contains('poi-err-box')) { box = document.createElement('li'); box.className = 'poi-err-box'; li.after(box); }
153        const msg = w.type === 'late'
154          ? (en ? `You may not make it before it closes (closes ${clock(w.poi.close_min)}). Try moving it earlier or choose another place.` : `อาจไปไม่ทันก่อนปิด (ปิดเวลา ${clock(w.poi.close_min)}) ลองย้ายไปไว้ก่อนหน้านี้หรือเปลี่ยนสถานที่`)
155          : (en ? `You may arrive before it opens (opens ${clock(w.poi.open_min)}). Try moving it later.` : `อาจไปถึงก่อนร้านเปิด (เปิดเวลา ${clock(w.poi.open_min)}) ลองย้ายไปไว้หลังจากนี้`);
156        box.innerHTML += `<div>⚠ ${esc(msg)}</div>`;
157      });
158    }
บรรทัด 145–148: decorateWarnings ล้างคำเตือนเก่า และเตรียมตัวช่วยจัดรูปเวลา (fmtClock) กับธงภาษา
บรรทัด 149–151: ไล่คำเตือนจาก ➜ uiWarnings() ใน frontend/app.js หาการ์ดของจุดนั้น แล้วทำให้เป็นสีแดง
บรรทัด 152: หาหรือสร้างกล่องข้อความใต้การ์ด
บรรทัด 153–155: ข้อความตามชนิด: ไปไม่ทันก่อนปิด (late) หรือถึงก่อนเปิด พร้อมสองภาษา
บรรทัด 156: ใส่ข้อความในกล่อง (หลีกอักขระพิเศษด้วย esc)
บรรทัด 160–186  ย้ายสถานที่และวาดแผนที่ใหม่
160    // ---------- ลากวางสถานที่เพื่อเรียงลำดับ/ย้ายข้ามวัน (แล้วคำนวณเวลา-ค่าใช้จ่ายใหม่ตามลำดับที่ลาก) ----------
161    // ย้ายสถานที่ไป "ตำแหน่งของเป้าหมาย" (ลากไปหลัง = ไปอยู่หลังเป้าหมาย, ลากไปหน้า = ไปอยู่หน้าเป้าหมาย); ถ้าส่งคำขอไม่สำเร็จ คืนแผนเดิม
162    let keepVis = null;   // จำวันที่เปิดอยู่บนแผนที่ไว้ตอนวาดใหม่หลังแก้แผน
163    const editView = focus => { keepVis = {focus, vis: Object.values(STATE.mapDayLayers).map(l => l.visible)}; };
164    function snapshot() { return STATE.selectedPkg.days.map(d => d.pois.slice()); }
165    function restore(snap) { STATE.selectedPkg.days.forEach((d, i) => { d.pois = snap[i].slice(); }); keepVis = null; }
166    function moveStop(src, dst) {
167      const days = STATE.selectedPkg.days, [sd, si] = src, snap = snapshot();
168      const [poi] = days[sd].pois.splice(si, 1);
169      const di = dst.i === null ? days[dst.d].pois.length : dst.i;
170      days[dst.d].pois.splice(di, 0, poi);
171      editView(null);
172      recomputeAndRefresh(() => restore(snap));
173    }
174    // วาดแผนที่ใหม่หลังแก้แผน: คงวันที่เปิดอยู่ (หรือแสดงเฉพาะวันที่แก้) — ไม่ทำให้ลากหมุดได้ (ลากการ์ดทางซ้ายแทน)
175    const origDrawOnMap = drawOnMap;
176    drawOnMap = function (pkg) {
177      origDrawOnMap(pkg);
178      if (keepVis) {
179        const {focus, vis} = keepVis; keepVis = null;
180        Object.keys(STATE.mapDayLayers).forEach(k => {
181          const want = focus != null ? +k === focus : vis[k] !== false, L_ = STATE.mapDayLayers[k];
182          if (L_.visible !== want) toggleDay(+k);
183        });
184        resetMapView();
185      }
186    };
บรรทัด 162: keepVis จำสถานะการเปิดปิดวันบนแผนที่ระหว่างวาดใหม่
บรรทัด 163: editView จดวันที่จะแสดงเฉพาะ (หรือคงของเดิม)
บรรทัด 164–165: snapshot จำลำดับสถานที่ทุกวัน และ restore คืนค่าเมื่อคำนวณไม่สำเร็จ
บรรทัด 166–173: moveStop ตัดสถานที่จากตำแหน่งเดิม วางที่ตำแหน่งใหม่ (หรือท้ายวัน) แล้วเรียก ➜ recomputeAndRefresh() ใน frontend/app.js ให้คำนวณเวลาและค่าใช้จ่ายใหม่ผ่าน ➜ recompute() ใน backend/main.py ถ้าล้มเหลวเรียก restore
บรรทัด 175–186: ห่อ ➜ drawOnMap() ใน frontend/app.js: เรียกของเดิม แล้วถ้ามี keepVis เปิดเฉพาะวันที่ต้องการด้วย ➜ toggleDay() ใน frontend/app.js และรีเซ็ตมุมมองด้วย ➜ resetMapView() ใน frontend/app.js
บรรทัด 188–262  ลากการ์ดด้วย pointer events (เมาส์และจอสัมผัส)
188    function enableDrag() {
189      const root = document.getElementById('dayPanels'); if (!root) return;
190      let gap = null, srcKey = null, srcLi = null, hiddenConn = null, ghost = null, offX = 0, offY = 0, corrX = 0, corrY = 0, curUl = null;
191      const cards = ul => [...ul.querySelectorAll('.poi-item')].filter(e => e !== srcLi && e !== ghost);
192      const flip = (ul, mutate) => {   // บันทึกตำแหน่งเดิม → เปลี่ยน DOM → เลื่อนจากตำแหน่งเดิมมาตำแหน่งใหม่
193        const items = cards(ul), before = new Map(items.map(e => [e, e.getBoundingClientRect().top]));
194        mutate();
195        items.forEach(e => { const dy = before.get(e) - e.getBoundingClientRect().top; if (dy) { e.style.transition = 'none'; e.style.transform = `translateY(${dy}px)`; requestAnimationFrame(() => { e.style.transition = 'transform .18s ease'; e.style.transform = ''; }); } });
196      };
197      const cleanup = () => { hiddenConn?.classList.remove('drag-hide'); hiddenConn = null; gap?.remove(); gap = null; ghost?.remove(); ghost = null; srcLi?.classList.remove('dragging'); srcLi = null; curUl = null; root.classList.remove('is-dragging'); document.body.classList.remove('wet-dragging'); };
198      // ใช้ pointer events แทน HTML5 drag-and-drop: การ์ดตามเมาส์ทุกเฟรม ไม่หน่วงเหมือน dragover ที่ถูกจำกัดความถี่
199      root.querySelectorAll('.poi-list').forEach(ul => {
200        const d = +(ul.id.match(/day-(\d+)-list/) || [])[1];
201        ul.querySelectorAll('.poi-item').forEach((li, i) => {
202          li.draggable = false; li.title = li.title || (window.WET_LANG === 'en' ? 'Drag to reorder or move to another day' : 'ลากเพื่อเรียงลำดับหรือย้ายไปวันอื่น');
203          li.ondragstart = e => e.preventDefault();   // ปิด drag ของเบราว์เซอร์ (ข้อความ/รูปในการ์ด) ที่จะขัดกับการลากแบบ pointer
204          li.onpointerdown = e => {
205            if (e.button !== 0 || e.target.closest('button, a, input, select')) return;
206            const touch = e.pointerType === 'touch';   // จอสัมผัส: กดค้าง 0.35 วินาทีจึงเริ่มลาก (ลากเร็วกว่านั้นคือเลื่อนหน้า)
207            if (!touch) e.preventDefault();
208            const sx = e.clientX, sy = e.clientY, r0 = li.getBoundingClientRect(); let started = false, lp = 0;
209            const noScroll = ev => { if (started && ev.cancelable) ev.preventDefault(); };   // ระหว่างลากบนจอสัมผัสไม่ให้หน้าเลื่อน
210            if (touch) document.addEventListener('touchmove', noScroll, {passive: false});
211            const start = () => {
212              started = true; srcKey = [d, i]; srcLi = li; offX = sx - r0.left; offY = sy - r0.top;
213              gap = document.createElement('li'); gap.className = 'drop-gap'; gap.style.height = li.offsetHeight + 'px';
214              root.classList.add('is-dragging'); document.body.classList.add('wet-dragging'); document.getSelection()?.removeAllRanges();
215              ghost = li.cloneNode(true); ghost.classList.add('drag-ghost'); ghost.removeAttribute('title');
216              ghost.style.cssText = `width:${r0.width}px;left:${r0.left}px;top:${r0.top}px;transform-origin:${offX}px ${offY}px`;
217              ul.appendChild(ghost);
218              ghost.style.animation = 'none'; ghost.style.transform = 'none'; const g0 = ghost.getBoundingClientRect(); ghost.style.animation = ''; ghost.style.transform = '';
219              corrX = g0.left - r0.left; corrY = g0.top - r0.top;   // บาง ancestor มี transform ทำให้ fixed อิงกรอบนั้น: ชดเชยส่วนต่างให้ตรงเมาส์
220              li.classList.add('dragging'); li.after(gap); curUl = ul;
221              const pv = li.previousElementSibling; if (pv?.classList.contains('dist-connector')) { pv.classList.add('drag-hide'); hiddenConn = pv; }
222              if (touch) { try { li.releasePointerCapture(e.pointerId); } catch (_) {} navigator.vibrate?.(15); }
223            };
224            if (touch) lp = setTimeout(() => { last = {clientX: sx, clientY: sy}; start(); frame(); }, 350);
225            let raf = 0, last = null;
226            const frame = () => {
227              raf = 0; if (!ghost || !last) return;
228              ghost.style.left = (last.clientX - offX - corrX) + 'px'; ghost.style.top = (last.clientY - offY - corrY) + 'px';
229              const under = document.elementFromPoint(last.clientX, last.clientY), panel = under?.closest('.day-panel'), tul = panel?.querySelector('.poi-list');
230              if (!tul) return;
231              if (touch) { const ed = last.clientY < 80 ? -14 : last.clientY > innerHeight - 80 ? 14 : 0; if (ed) { scrollBy(0, ed); if (!raf) raf = requestAnimationFrame(frame); } }   // ลากชิดขอบจอ: เลื่อนหน้าอัตโนมัติ
232              const cs = cards(tul); let ref = null;
233              for (const c of cs) { const r = c.getBoundingClientRect(); if (last.clientY < r.top + r.height / 2) { ref = c; break; } }
234              const already = gap.parentNode === tul && (ref ? gap.nextElementSibling === ref : !cs.some(c => gap.compareDocumentPosition(c) & 4));
235              if (already) return;
236              flip(tul, () => { if (ref) tul.insertBefore(gap, ref); else tul.appendChild(gap); }); curUl = tul;
237            };
238            const move = ev => {
239              if (!started) {
240                if (touch) { if (Math.hypot(ev.clientX - sx, ev.clientY - sy) > 8) clearTimeout(lp); return; }   // ขยับก่อนกดค้างครบเวลา = ผู้ใช้เลื่อนหน้า
241                if (Math.hypot(ev.clientX - sx, ev.clientY - sy) < 6) return; start();
242              }
243              last = ev; if (!raf) raf = requestAnimationFrame(frame);
244            };
245            const up = ev => {
246              document.removeEventListener('pointermove', move); document.removeEventListener('pointerup', up); document.removeEventListener('pointercancel', up);
247              clearTimeout(lp); document.removeEventListener('touchmove', noScroll);
248              if (!started) return;
249              if (raf) cancelAnimationFrame(raf);
250              window.addEventListener('click', ck => { ck.stopPropagation(); ck.preventDefault(); }, {capture: true, once: true});   // ไม่ให้การปล่อยเมาส์ถูกนับเป็นคลิกการ์ด
251              const targetUl = gap?.parentNode, src = srcKey;
252              if (ev.type === 'pointercancel' || !targetUl || !targetUl.classList.contains('poi-list')) { cleanup(); return; }
253              const dd = +targetUl.id.match(/day-(\d+)-list/)[1];
254              const idx = [...targetUl.children].filter(c => (c.classList.contains('poi-item') && c !== srcLi && c !== ghost) || c === gap).indexOf(gap);
255              cleanup();
256              if (!(src[0] === dd && src[1] === idx)) moveStop(src, {d: dd, i: idx});
257            };
258            document.addEventListener('pointermove', move); document.addEventListener('pointerup', up); document.addEventListener('pointercancel', up);
259          };
260        });
261      });
262    }
บรรทัด 188–191: enableDrag หาตัวห่อ #dayPanels และประกาศตัวแปรสถานะการลาก (ช่องว่าง การ์ดต้นทาง ตัวผี ออฟเซ็ต) และ cards คืนการ์ดอื่นในรายการ
บรรทัด 192–196: flip เทคนิค FLIP: จำตำแหน่งเดิม เปลี่ยน DOM แล้วเลื่อนการ์ดจากตำแหน่งเดิมมาตำแหน่งใหม่แบบนุ่ม ๆ
บรรทัด 197: cleanup ล้างสถานะและองค์ประกอบชั่วคราวทั้งหมดของการลาก
บรรทัด 198–199: ใช้ pointer events แทน HTML5 drag-and-drop เพราะการ์ดตามเมาส์/นิ้วทุกเฟรม แล้ววนทุกรายการวัน
บรรทัด 200–203: หาเลขวันจาก id ปิด draggable และ dragstart ของเบราว์เซอร์ และตั้ง title ของการ์ด
บรรทัด 204–210: เมื่อกดที่การ์ด (ไม่ใช่ปุ่มข้างใน) แยกเมาส์กับจอสัมผัส: เมาส์ป้องกันค่าเริ่มต้นทันที ส่วนจอสัมผัสต้องกดค้างก่อน จดจุดเริ่มต้น และผูกตัวดัก touchmove แบบ non-passive ที่กันหน้าเลื่อนเฉพาะเมื่อกำลังลากอยู่
บรรทัด 211–223: start เริ่มลากจริง: สร้างช่องว่าง drop-gap และตัวผีของการ์ด ชดเชยตำแหน่งกรณีบรรพบุรุษมี transform ซ่อนเส้นเชื่อมระยะทาง และบนจอสัมผัสปล่อย pointer capture แล้วสั่นเครื่องเบา ๆ
บรรทัด 224: จอสัมผัส: ตั้งตัวจับเวลา 350 มิลลิวินาที เมื่อครบโดยนิ้วไม่ขยับจึงเรียก start (ถ้านิ้วขยับก่อน move จะยกเลิกเพราะผู้ใช้กำลังเลื่อนหน้า)
บรรทัด 225–237: frame ทำงานหนึ่งครั้งต่อเฟรม: ย้ายตัวผีตามเมาส์/นิ้ว หารายการวันใต้ตำแหน่ง บนจอสัมผัสถ้านิ้วอยู่ใกล้ขอบบนหรือล่างของจอ (80 พิกเซล) เลื่อนหน้าอัตโนมัติ แล้วหาการ์ดที่จะแทรกก่อนและย้ายช่องว่างถ้าตำแหน่งเปลี่ยน
บรรทัด 238–244: move เมาส์: เริ่มลากเมื่อเกิน 6 พิกเซล จอสัมผัส: ถ้าขยับเกิน 8 พิกเซลก่อนกดค้างครบเวลาให้ยกเลิกตัวจับเวลา แล้วบันทึกตำแหน่งล่าสุดและขอเฟรม
บรรทัด 245–257: up ถอดตัวฟังและตัวจับเวลา ยกเลิกกรณี pointercancel หรือไม่มีเป้าหมาย คำนวณวันและตำแหน่งปลายทาง ล้างสถานะ และเรียก moveStop ถ้าตำแหน่งเปลี่ยนจริง (กันคลิกที่ตามมาด้วยตัวดักครั้งเดียว)
บรรทัด 258–262: ผูกตัวฟัง move up cancel แล้วปิดฟังก์ชัน
บรรทัด 265–287  สลับเป็นสถานที่ในร่ม
265    window.indoorSwap = async function (dIdx) {
266      const pkg = STATE.selectedPkg, day = pkg.days[dIdx];
267      const inPlan = new Set(pkg.days.flatMap(d => d.pois.map(p => p.id)));
268      const base = day.pois.filter(p => p.category !== 'restaurant');
269      const cLat = base.reduce((s, p) => s + p.lat, 0) / base.length, cLng = base.reduce((s, p) => s + p.lng, 0) / base.length;
270      const cands = STATE.pois.filter(p => ['culture', 'market'].includes(p.category) && !inPlan.has(p.id) && !STATE.excluded.has(p.id) && haversineKm(cLat, cLng, p.lat, p.lng) <= 25)
271        .sort((a, b) => (b.category === 'culture') - (a.category === 'culture') || b.score - a.score);
272      const snap = snapshot(), savedLocked = new Set(STATE.locked), savedExcl = new Set(STATE.excluded);
273      let n = 0;
274      day.pois.slice().forEach((p, k) => {
275        if (!OUTDOOR.includes(p.category)) return;
276        const at = arriveOf(day, p);   // นาทีที่ไปถึงจุดเดิม — เลือกที่ในร่มที่เปิดอยู่ช่วงนั้น
277        const ci = cands.findIndex(c => at < 0 || (c.open_min <= at && at + c.duration_min <= c.close_min));
278        if (ci < 0) return;
279        const [c] = cands.splice(ci, 1);
280        day.pois[k] = c; STATE.locked.add(c.id); STATE.excluded.add(p.id); STATE.locked.delete(p.id); n++;
281      });
282      if (!n) { showToast('ไม่พบสถานที่ในร่มใกล้เคียงที่ยังเปิดอยู่ในช่วงเวลานั้นและยังไม่อยู่ในแผน', 'error', 4500); return; }
283      showToast(`สลับ ${n} จุดของวันที่ ${dIdx + 1} เป็นสถานที่ในร่มแล้ว`, 'ok', 3000);
284      editView(dIdx);   // แสดงเฉพาะวันที่กดบนแผนที่
285      // คำนวณใหม่เฉพาะแผนที่ผู้ใช้แก้ (ไม่ย้ายจุดของวันอื่น) ถ้าล้มเหลวคืนค่าเดิมทั้งหมด
286      await recomputeAndRefresh(() => { restore(snap); STATE.locked = savedLocked; STATE.excluded = savedExcl; });
287    };
บรรทัด 265–269: indoorSwap หาแผน วัน สถานที่ที่อยู่ในแผนทั้งหมด และจุดศูนย์กลางของวันที่ไม่นับร้านอาหาร
บรรทัด 270–271: หาตัวเลือก: วัฒนธรรมหรือตลาด ที่ยังไม่อยู่ในแผนและไม่ถูกลบ ห่างไม่เกิน 25 กม. (haversineKm) เรียงให้วัฒนธรรมก่อนแล้วตามคะแนน
บรรทัด 272–273: จำสถานะเดิมไว้ย้อนกลับ
บรรทัด 274–281: แต่ละจุดกลางแจ้ง หาเวลาถึง (arriveOf) และเลือกที่ในร่มที่เปิดในช่วงนั้น แทนที่และล็อกจุดใหม่ ลบจุดเดิมออก
บรรทัด 282–283: แจ้งเตือนถ้าหาไม่เจอ หรือจำนวนที่สลับ
บรรทัด 284–286: แสดงเฉพาะวันนั้นบนแผนที่ แล้วคำนวณใหม่ ถ้าล้มเหลวคืนค่าเดิม
บรรทัด 289–349  แม่แบบ Tips ต่อหมวด
289    // ---------- กล่อง Tips (หมุนทุก 20 วินาที) ----------
290    let seasonLines = [], tipIdx = 0, tipPool = [], tipsTimer = null, tipsFor = null;
291    // แม่แบบ Tips ต่อหมวด: ok = เงื่อนไขจากข้อมูลจริงของสถานที่ (กันแนะนำผิด เช่น บอกให้ไปตอนเย็นทั้งที่ปิดแล้ว)
292    const hhmm = m => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
293    const price = p => p.cost > 0 ? `ค่าเข้า/ใช้จ่ายราว ${fmt(p.cost)} บาท` : 'ไม่เสียค่าเข้า';
294    const hrs = p => p.open_min <= 0 && p.close_min >= 1439 ? 'เปิดทั้งวัน' : `เปิด ${hhmm(p.open_min)}–${hhmm(p.close_min)}`;
295    const morning = p => p.open_min <= 600, evening = p => p.close_min >= 1080, any = () => true;
296    const dur = p => p.duration_min >= 30 ? `ใช้เวลาราว ${p.duration_min >= 90 ? Math.round(p.duration_min / 60 * 10) / 10 + ' ชั่วโมง' : p.duration_min + ' นาที'}` : '';
297    // dry = ใช้เฉพาะวันที่ไม่ฝน, rain = ใช้เฉพาะเมื่อพยากรณ์ว่าฝนตก
298    const TIP_TPL = {
299      beach: [
300        {ok: morning, dry: 1, t: p => `🏖️ ${p.name_th} ไปช่วงเช้าแดดยังไม่แรง ทรายเย็น เหมาะกับการเดินเล่น`},
301        {ok: evening, dry: 1, t: p => `🌅 ${p.name_th} นั่งชมพระอาทิตย์ตกได้ ${hrs(p)}`},
302        {ok: any, dry: 1, t: p => `🏖️ ${p.name_th} ${price(p)} อย่าลืมครีมกันแดดและน้ำดื่ม`},
303        {ok: any, t: p => `📸 ${p.name_th} จุดถ่ายรูปยอดนิยมของหมวดหาด ${dur(p)}`.trim()},
304        {ok: any, dry: 1, t: p => `🩴 ${p.name_th} พกรองเท้าแตะกับผ้าเช็ดตัวเล็ก ๆ ไว้ ลงเล่นน้ำได้ทันที`},
305        {ok: any, t: p => `🌊 ${p.name_th} ดูธงเตือนคลื่นลมก่อนลงเล่นน้ำทุกครั้ง และเล่นในเขตที่กำหนด`},
306        {ok: any, rain: 1, t: p => `🌧️ ${p.name_th} ช่วงฝนคลื่นอาจแรง ชมวิวจากริมหาดแทนการลงน้ำจะปลอดภัยกว่า`},
307      ],
308      temple: [
309        {ok: morning, t: p => `🛕 ${p.name_th} แวะตอนเช้าอากาศเย็น คนน้อย ${hrs(p)}`},
310        {ok: any, t: p => `🛕 ${p.name_th} แต่งกายสุภาพ ถอดรองเท้าก่อนเข้าอาคาร ${price(p)}`},
311        {ok: any, t: p => `🙏 ${p.name_th} ${dur(p) || 'แวะชมได้ไม่นาน'} เหมาะแทรกระหว่างสถานที่อื่น`},
312        {ok: evening, t: p => `🪔 ${p.name_th} ยังเปิดถึง ${hhmm(p.close_min)} ไปช่วงเย็นบรรยากาศสงบ`},
313        {ok: any, t: p => `🤫 ${p.name_th} พูดเบา ๆ และขออนุญาตก่อนถ่ายรูปพระหรือผู้คน`},
314        {ok: any, rain: 1, t: p => `☔ ${p.name_th} มีศาลาหรืออาคารให้หลบฝนได้ เหมาะกับวันฝนตก`},
315        {ok: any, dry: 1, t: p => `🌳 ${p.name_th} พื้นที่โล่ง ควรพกหมวกหรือร่มกันแดดไว้`},
316      ],
317      viewpoint: [
318        {ok: evening, dry: 1, t: p => `🌄 ${p.name_th} ควรไปช่วงเย็น แสงสวยที่สุด (ปิด ${hhmm(p.close_min)})`},
319        {ok: morning, dry: 1, t: p => `⛅ ${p.name_th} ไปเช้าท้องฟ้าโปร่ง ถ่ายวิวได้ชัด`},
320        {ok: any, t: p => `🌄 ${p.name_th} ${price(p)} พกกล้องหรือโทรศัพท์แบตเต็มไปด้วย`},
321        {ok: any, t: p => `👟 ${p.name_th} ใส่รองเท้าเดินสบาย ${dur(p)}`.trim()},
322        {ok: any, rain: 1, t: p => `🌫️ ${p.name_th} วันฝนทัศนียภาพอาจถูกเมฆบัง ลองสลับไปไว้วันที่ฟ้าเปิด`},
323        {ok: any, t: p => `🧥 ${p.name_th} ที่สูงลมแรงกว่าที่คิด พกเสื้อบาง ๆ ไว้สักตัว`},
324      ],
325      culture: [
326        {ok: any, t: p => `🏛️ ${p.name_th} ${hrs(p)} ${price(p)}`},
327        {ok: any, t: p => `🎟️ ${p.name_th} ${dur(p) || 'เดินชมได้สบาย'} เหมาะเป็นกิจกรรมหลบแดดช่วงบ่าย`},
328        {ok: morning, t: p => `📚 ${p.name_th} แวะตอนเช้าได้ข้อมูลเต็มที่ ก่อนคนเยอะ`},
329        {ok: any, t: p => `🏛️ ${p.name_th} ได้เรียนรู้เรื่องราวท้องถิ่น เหมาะกับครอบครัว`},
330        {ok: any, rain: 1, t: p => `☔ ${p.name_th} กิจกรรมในร่มที่เหมาะกับวันฝนตก ${hrs(p)}`},
331        {ok: any, t: p => `🗺️ ${p.name_th} ถามเจ้าหน้าที่ถึงเรื่องเล่าท้องถิ่น มักได้ข้อมูลที่ไม่มีในป้าย`},
332      ],
333      market: [
334        {ok: evening, t: p => `🛍️ ${p.name_th} ช่วงเย็นคึกคักที่สุด เหมาะกับมื้อเย็นและของฝาก (ปิด ${hhmm(p.close_min)})`},
335        {ok: any, t: p => `🍢 ${p.name_th} ลองของกินพื้นเมือง พกเงินสดเล็กน้อยไว้ต่อรอง`},
336        {ok: morning, t: p => `🧺 ${p.name_th} ไปเช้าของสดและของฝากครบกว่า`},
337        {ok: any, t: p => `🛍️ ${p.name_th} ${hrs(p)} เดินเล่นได้ ${dur(p)}`.trim()},
338        {ok: any, t: p => `🥭 ${p.name_th} ถามหาผลไม้หรือขนมประจำฤดูกาล ซื้อกินสด ๆ อร่อยกว่า`},
339        {ok: any, rain: 1, t: p => `🌂 ${p.name_th} ตลาดมักมีหลังคาบางส่วน พกร่มพับไว้ก็เดินได้สบาย`},
340      ],
341      activity: [
342        {ok: any, t: p => `🎈 ${p.name_th} กิจกรรมสนุก ๆ ${price(p)} ควรเช็คคิวหรือจองล่วงหน้า`},
343        {ok: morning, dry: 1, t: p => `🤸 ${p.name_th} เริ่มตอนเช้าอากาศดี ไม่ร้อนจัด`},
344        {ok: any, t: p => `👨‍👩‍👧 ${p.name_th} เหมาะกับเพื่อนและครอบครัว ${dur(p)}`.trim()},
345        {ok: any, dry: 1, t: p => `🎒 ${p.name_th} เตรียมเสื้อผ้าเปลี่ยนและครีมกันแดด ${hrs(p)}`},
346        {ok: any, rain: 1, t: p => `📞 ${p.name_th} กิจกรรมกลางแจ้งอาจเลื่อนเมื่อฝนตก โทรเช็คกับผู้ให้บริการก่อนออกเดินทาง`},
347        {ok: any, t: p => `💧 ${p.name_th} จิบน้ำบ่อย ๆ และฟังคำแนะนำด้านความปลอดภัยของเจ้าหน้าที่`},
348      ],
349    };
บรรทัด 290: ตัวแปรสถานะของกล่อง Tips
บรรทัด 292–296: ตัวช่วยสร้างข้อความ: เวลา (hhmm) ราคา เวลาเปิด-ปิด เงื่อนไขเช้า/เย็น และระยะเวลาที่ใช้
บรรทัด 298–349: TIP_TPL แม่แบบประโยคของแต่ละหมวด (หาด วัด จุดชมวิว วัฒนธรรม ตลาด กิจกรรม) แต่ละแม่แบบมีเงื่อนไข ok ตรวจจากข้อมูลจริงของสถานที่ (กันแนะนำผิด เช่นให้ไปตอนเย็นทั้งที่ปิดก่อน) และธง dry (ใช้เฉพาะวันไม่ฝน) หรือ rain (เฉพาะวันฝน)
บรรทัด 350–370  เคล็ดลับทั่วไป
350    // เคล็ดลับทั่วไป (ไม่ผูกกับสถานที่) — บางข้อปรับตามจำนวนวัน/งบ/จำนวนคนที่กรอก
351    function generalTips() {
352      const days = SELECTED_DAYS, budget = +$('budget').value || 0, ppl = +$('travelers').value || 1;
353      const t = [
354        '💡 กด "ความชอบ" เพื่อเลือกหมวดที่ชอบหรือไม่ชอบ แผนจะปรับตามให้',
355        '💡 บันทึกแผนที่ถูกใจด้วยปุ่ม ★ แล้วกลับมาเปิดดูได้ภายหลัง',
356        '🔄 ไม่ถูกใจสถานที่ไหน กดสลับหรือลบจุดในแผน ระบบจะจัดเส้นทางที่เหลือให้ใหม่',
357        '📅 ส่งแผนเข้าปฏิทินได้ด้วยปุ่ม ปฏิทิน และบันทึกเป็น PDF ไว้เปิดตอนไม่มีสัญญาณ',
358        '👫 ชวนเพื่อนวางแผนด้วยกันผ่านปุ่ม แชร์ ทุกคนเห็นและแก้แผนเดียวกันได้',
359        '⇄ อยากรู้ว่าอัลกอริทึมไหนวางแผนได้ดีกว่า ลองกด "เทียบอัลกอริทึม" ในหน้าปรับแต่งทริป',
360        '🚗 เวลาเดินทางในแผนคิดแบบรถไม่ติด ช่วงชั่วโมงเร่งด่วนควรเผื่อเวลาเพิ่มราว 20–30%',
361        '🍜 มื้อกลางวันช่วง 11:00–14:30 ร้านดัง ๆ คนเยอะ ไปก่อน 11:30 มักไม่ต้องรอคิว',
362        '🔋 พกพาวเวอร์แบงก์และเก็บแผนที่ออฟไลน์ไว้ เผื่อสัญญาณอินเทอร์เน็ตไม่ดี',
363        '🧴 ครีมกันแดด หมวก และน้ำดื่ม เป็นของที่ควรพกติดตัวทุกทริป',
364      ];
365      if (days >= 4) t.push(`🛌 ทริป ${days} วันแนะนำให้เว้นช่วงพักครึ่งวันสักวัน จะไม่เหนื่อยสะสม`);
366      if (days === 1) t.push('⏰ ทริปวันเดียวควรเริ่มก่อน 9:00 และเลือกสถานที่ที่อยู่ใกล้กัน');
367      if (budget && days) t.push(`💰 งบ ${fmt(budget)} บาท ตก ${fmt(budget / days / ppl)} บาท/คน/วัน รวมที่พักแล้ว ปรับงบเพิ่มเพื่อได้แพ็กเกจ Premium`);
368      if (ppl >= 4) t.push('👨‍👩‍👧‍👦 เดินทางหลายคน แชร์ค่ารถหรือเช่ารถตู้จะคุ้มกว่าเรียกรถแยก');
369      return t;
370    }
บรรทัด 351–364: generalTips อ่านจำนวนวัน งบ และจำนวนคนจากฟอร์ม แล้วสร้างรายการเคล็ดลับที่ไม่ผูกกับสถานที่
บรรทัด 365–368: เติมเคล็ดลับตามเงื่อนไข: ทริปยาว ≥ 4 วัน ทริปวันเดียว งบต่อคนต่อวัน และเดินทางหลายคน
บรรทัด 369–370: คืนรายการ
บรรทัด 371–388  เคล็ดลับตามจังหวัด
371    // Tips เฉพาะจังหวัด: จุดเด่นจากข้อมูลจริงของจังหวัดนั้น + เคล็ดลับตามภูมิภาค/ลักษณะพื้นที่
372    const REGION_TIPS = {
373      'ภาคเหนือ': ['🧣 ภาคเหนือหน้าหนาว (พ.ย.–ก.พ.) ตอนเช้าอากาศเย็นจัด พกเสื้อกันหนาวบางๆ', '🏍️ ถนนบนเขามีโค้งมาก ขับช้าๆ และเผื่อเวลาเดินทางเพิ่ม', '🍲 ลองอาหารเหนือ เช่น ขันโตก ข้าวซอย น้ำพริกหนุ่ม', '🌫️ ช่วงปลายหนาวถึงต้นร้อนอาจมีหมอกควัน ตรวจค่าฝุ่นก่อนไปจุดชมวิว'],
374      'ภาคตะวันออกเฉียงเหนือ': ['🌞 ภาคอีสานแดดแรงและร้อนจัดช่วงเมษายน แนะนำเที่ยวเช้าและเย็น', '🥗 ลองส้มตำ ลาบ และไก่ย่างของท้องถิ่น', '🛕 อีสานมีปราสาทหินและวัดเก่าแก่ ควรพกหมวกและน้ำดื่ม', '🚗 ระยะทางระหว่างอำเภอค่อนข้างไกล ควรเช่ารถหรือจัดรถไว้ล่วงหน้า'],
375      'ภาคกลาง': ['🛶 ภาคกลางมีตลาดน้ำและวัดเก่า แต่งกายสุภาพเมื่อเข้าวัด', '☀️ ช่วงบ่ายร้อนจัด เหมาะกับพิพิธภัณฑ์และร้านในร่ม', '🚆 เดินทางรถไฟหรือรถตู้ไปหลายเมืองได้สะดวก', '🍜 อาหารภาคกลางมีหลากหลาย ลองก๋วยเตี๋ยวเรือและขนมไทยโบราณ'],
376      'ภาคตะวันออก': ['🏖️ ชายฝั่งตะวันออกเที่ยวทะเลสะดวก ใกล้กรุงเทพฯ เหมาะกับทริปสั้น', '🍤 อาหารทะเลสดที่ตลาดชายหาด ถามราคาก่อนสั่งทุกครั้ง', '🍈 ช่วงเมษายน–มิถุนายนมีผลไม้ฤดูกาลมาก เช่น ทุเรียน มังคุด เงาะ', '⛴️ ถ้าไปเกาะ เช็คตารางเรือและสภาพคลื่นก่อนเดินทาง'],
377      'ภาคตะวันตก': ['🌳 ภาคตะวันตกมีป่า น้ำตก และอุทยาน พกยากันยุงและรองเท้าเดินป่า', '🌊 น้ำตกหน้าฝนน้ำแรง ตรวจประกาศอุทยานก่อนลงเล่นน้ำ', '🚆 รถไฟสายประวัติศาสตร์เป็นกิจกรรมที่น่าลอง ควรจองตั๋วล่วงหน้า', '🍃 ที่พักใกล้ธรรมชาติมักไม่มีสัญญาณมือถือ เก็บแผนที่ออฟไลน์ไว้'],
378      'ภาคใต้': ['⛵ ภาคใต้ทะเลอันดามัน ช่วงพ.ค.–ต.ค. คลื่นลมแรง เรือบางเส้นทางงดเดินเรือ', '🏝️ ฝั่งอ่าวไทยฝนหนักช่วงต.ค.–ธ.ค. เช็คพยากรณ์ก่อนไปเกาะ', '🍛 ลองอาหารใต้ เช่น แกงส้ม ข้าวยำ และโรตีกับแกงกะหรี่', '🧴 แดดทะเลแรงมาก ทาครีมกันแดดซ้ำทุก 2 ชั่วโมง'],
379    };
380    function provinceTips() {
381      const base = (typeof baseSlug !== 'undefined' && baseSlug) || getProvince().split('+')[0], pv = STATE.provinces[base] || {}, nm = pv.name_th || base;
382      const out = [...(REGION_TIPS[pv.region] || [])];
383      const best = c => STATE.pois.filter(p => p.category === c && p.open_min !== undefined).sort((a, b) => b.score - a.score).slice(0, 3).map(p => p.name_th);
384      const hi = [['beach', 'หาดและทะเล'], ['temple', 'วัด'], ['viewpoint', 'จุดชมวิว'], ['culture', 'วัฒนธรรมและพิพิธภัณฑ์'], ['market', 'ตลาด'], ['activity', 'กิจกรรม']];
385      hi.forEach(([c, label]) => { const b = best(c); if (b.length >= 2) out.push(`📍 ${label}เด่นของ${nm}: ${b.join(' · ')}`); });
386      const dist = STATE.provinces[base]?.max_days; if (dist) out.push(`🗓️ ข้อมูลของ${nm}รองรับทริปได้สูงสุด ${dist} วัน`);
387      return out;
388    }
บรรทัด 372–379: REGION_TIPS เคล็ดลับตามภูมิภาค
บรรทัด 380–382: provinceTips หาจังหวัดฐาน และเริ่มด้วยเคล็ดลับตามภาค
บรรทัด 383–385: หาสถานที่คะแนนสูงสุด 3 อันดับของแต่ละหมวด ถ้ามีอย่างน้อย 2 ที่ เพิ่มประโยค "…เด่นของจังหวัด"
บรรทัด 386: เพิ่มข้อความจำนวนวันสูงสุดที่ข้อมูลรองรับ
บรรทัด 387–388: คืนรายการ
บรรทัด 389–412  ประกอบและแสดง Tips
389    function buildTips() {
390      const top = STATE.pois.filter(p => TIP_TPL[p.category] && p.open_min !== undefined).sort((a, b) => b.score - a.score).slice(0, 20);
391      const used = new Set(), places = [];
392      top.forEach(p => {
393        const opts = TIP_TPL[p.category].filter(x => x.ok(p) && !(x.dry && wetDays) && !(x.rain && !wetDays) && !used.has(x));
394        const x = opts[Math.floor(Math.random() * opts.length)];   // แม่แบบเดียวกันใช้ได้ครั้งเดียวต่อรอบ ไม่ให้ประโยคซ้ำกันกับหลายสถานที่
395        if (x) { used.add(x); places.push(x.t(p)); }
396      });
397      const shuf = a => a.sort(() => Math.random() - 0.5);
398      const pool = [...weatherLines, ...(weatherLines.length ? [] : seasonLines.map(l => '🌤️ ' + l))];
399      // สลับสถานที่กับเคล็ดลับทั่วไปสลับกัน ไม่ให้ข้อความประเภทเดียวติดกันยาว
400      const g = shuf(generalTips().filter(x => STATE.dev || !x.includes('เทียบอัลกอริทึม'))), pl = shuf(places), rg = shuf(provinceTips());
401      while (g.length || pl.length || rg.length) { if (rg.length) pool.push(rg.pop()); if (pl.length) pool.push(pl.pop()); if (pl.length) pool.push(pl.pop()); if (g.length && Math.random() < 0.6) pool.push(g.pop()); else if (!pl.length && !rg.length) pool.push(g.pop()); }
402      return pool;
403    }
404    function showTip(animate) {
405      const t = $('tipsText'); if (!t || !tipPool.length) return;
406      const set = () => { t.textContent = tipPool[tipIdx++ % tipPool.length]; t.classList.remove('fade'); };
407      if (animate) { t.classList.add('fade'); setTimeout(set, 400); } else set();
408    }
409    function refreshTips(rebuild) {
410      if (!$('tipsText')) return;
411      if (rebuild || tipsFor !== STATE.pois) { tipPool = buildTips(); tipIdx = 0; tipsFor = STATE.pois; showTip(false); }
412    }
บรรทัด 389–391: buildTips เลือก 20 สถานที่คะแนนสูงสุดที่มีเวลาเปิด-ปิด
บรรทัด 392–396: แต่ละสถานที่สุ่มแม่แบบที่เข้าเงื่อนไข (ฝน/ไม่ฝน) และใช้แม่แบบเดียวกันได้ครั้งเดียวต่อรอบ
บรรทัด 397–400: สลับลำดับรายการ ตั้งต้นด้วยข้อความพยากรณ์หรือหมายเหตุฤดูกาล และซ่อนเคล็ดลับ "เทียบอัลกอริทึม" ถ้าไม่ได้อยู่โหมด Developer
บรรทัด 401–402: วนสลับประเภทข้อความไม่ให้ประเภทเดียวติดกันยาว แล้วคืนรายการทั้งหมด
บรรทัด 403: ปิดฟังก์ชัน
บรรทัด 404–408: showTip แสดงข้อความถัดไปเป็นวงกลม ถ้า animate ให้เฟดออกก่อน 0.4 วินาที
บรรทัด 409–412: refreshTips สร้างรายการใหม่ถ้าถูกสั่ง หรือข้อมูลสถานที่เปลี่ยน
บรรทัด 413–444  Tips ภาษาอังกฤษ
413    // ---------- Tips ภาษาอังกฤษ (ใช้เมื่อสลับภาษา) ----------
414    const WMO_EN = c => c === 0 ? '☀️ Clear' : c <= 2 ? '🌤️ Partly cloudy' : c === 3 ? '☁️ Overcast' : c <= 48 ? '🌫️ Fog' : c <= 57 ? '🌦️ Drizzle' : c <= 67 ? '🌧️ Rain' : c <= 82 ? '🌧️ Showers' : '⛈️ Thunderstorm';
415    const TIP_EN = {
416      beach: [p => `🏖️ ${p.name_en}: go in the morning or late afternoon when the sun is milder`, p => `🌊 ${p.name_en}: check the wave flags before swimming`],
417      temple: [p => `🛕 ${p.name_en}: dress modestly and take your shoes off before entering`, p => `🙏 ${p.name_en}: a quiet stop between busier places`],
418      viewpoint: [p => `🌄 ${p.name_en}: best around sunset (closes ${hhmm(p.close_min)})`, p => `👟 ${p.name_en}: wear comfortable shoes`],
419      culture: [p => `🏛️ ${p.name_en}: ${hrs(p).replace('เปิด', 'open').replace('ทั้งวัน', 'all day')} — a good indoor stop in the afternoon`, p => `🎟️ ${p.name_en}: ask the staff for local stories`],
420      market: [p => `🛍️ ${p.name_en}: liveliest in the evening — good for dinner and souvenirs`, p => `🍢 ${p.name_en}: try local snacks, bring a little cash`],
421      activity: [p => `🎈 ${p.name_en}: book ahead in busy periods`, p => `💧 ${p.name_en}: drink plenty of water and follow the safety briefing`],
422    };
423    function buildTipsEN() {
424      const days = SELECTED_DAYS, budget = +$('budget').value || 0, ppl = +$('travelers').value || 1;
425      const pool = [];
426      const iso = Object.keys(wxDaily).sort();
427      iso.forEach(t => { const w = wxDaily[t]; pool.push(`${WMO_EN(w.code)} ${t.slice(5)} ${w.lo}–${w.hi}°C · rain ${w.pop}% (live forecast)`); });
428      if (iso.some(t => wxDaily[t].pop >= 60)) pool.unshift('☔ High chance of rain on some days — bring an umbrella and keep indoor options ready');
429      const top = STATE.pois.filter(p => TIP_EN[p.category]).sort((a, b) => b.score - a.score).slice(0, 14);
430      const places = top.map(p => { const o = TIP_EN[p.category]; return o[Math.floor(Math.random() * o.length)](p); }).sort(() => Math.random() - 0.5);
431      const g = [
432        '💡 Open "Preferences" to like or dislike categories — your plan adapts', '💡 Save plans you like with ★ and reopen them later', '💡 Add a nearby province with the buttons under the province field',
433        '🔄 Swap or remove a stop and the rest of the route is re-optimized', '📅 Export to your calendar or save as PDF to use offline', '👫 Plan together: the Share button gives a live link',
434        '🚗 Travel times assume no traffic — add 20–30% in rush hour', '🍜 Popular lunch spots fill up after 11:30 — arrive a little earlier', '🔋 Carry a power bank and save an offline map', '🧴 Sunscreen, a hat and water are always worth packing',
435      ];
436      if (days >= 4) g.push(`🛌 On a ${days}-day trip, keep one half-day free to rest`);
437      if (budget && days) g.push(`💰 ${fmt(budget)} THB is about ${fmt(budget / days / ppl)} THB per person per day including accommodation`);
438      g.sort(() => Math.random() - 0.5);
439      while (g.length || places.length) { if (places.length) pool.push(places.pop()); if (places.length) pool.push(places.pop()); if (g.length) pool.push(g.pop()); }
440      return pool;
441    }
442    const buildTipsTH = buildTips;
443    buildTips = function () { return window.WET_LANG === 'en' ? buildTipsEN() : buildTipsTH(); };
444    window.addEventListener('wet-lang', () => refreshTips(true));
บรรทัด 414: WMO_EN แปลรหัสอากาศเป็นอังกฤษ
บรรทัด 415–422: TIP_EN แม่แบบประโยคอังกฤษของแต่ละหมวด (ใช้ชื่ออังกฤษของสถานที่)
บรรทัด 423–425: buildTipsEN อ่านจำนวนวัน งบ และจำนวนคน
บรรทัด 426–428: ใส่พยากรณ์รายวันและคำเตือนฝนสูง
บรรทัด 429–430: เลือก 14 สถานที่คะแนนสูงสุดและสุ่มประโยค
บรรทัด 431–437: เคล็ดลับทั่วไปภาษาอังกฤษ พร้อมข้อความตามจำนวนวันและงบ
บรรทัด 438–441: สลับลำดับและวนผสมแล้วคืนรายการ
บรรทัด 442–443: เก็บ buildTips ภาษาไทยไว้ แล้วทับด้วยฟังก์ชันที่เลือกตามภาษา (WET_LANG จาก ➜ frontend/i18n.js)
บรรทัด 444: เมื่อสลับภาษา (เหตุการณ์ wet-lang จาก ➜ frontend/i18n.js) สร้าง Tips ใหม่
บรรทัด 446–455  ติดตั้ง Tips
446    window.wetTips = () => tipPool.slice();   // ใช้ตรวจชุดข้อความ Tips ปัจจุบัน
447    function initTips() {
448      document.querySelector('.pf-col-search')?.insertAdjacentHTML('beforebegin',
449        '<div class="pf-col pf-col-tips"><label class="pf-label">Tips</label><div class="tips-card"><span class="tips-badge">TIPS</span><span class="tips-text" id="tipsText"></span></div></div>');
450      tipsTimer = setInterval(() => { refreshTips(false); showTip(true); }, 10000);
451      setInterval(() => { if (tipsFor !== STATE.pois && STATE.pois.length) refreshTips(true); }, 1000);   // ข้อมูลจังหวัดโหลดเสร็จ/เปลี่ยนจังหวัด
452    }
453
454    const origDateSummary = updateDateSummary;
455    updateDateSummary = function (dates) { origDateSummary(dates); updateHint(); };
บรรทัด 446: wetTips คืนสำเนา Tips ปัจจุบัน (ไว้ตรวจสอบ)
บรรทัด 447–452: initTips แทรกกล่อง Tips ก่อนปุ่มค้นหา (ปุ่มอยู่ใน ➜ frontend/index.html) ตั้งตัวจับเวลาเปลี่ยนข้อความทุก 10 วินาที และตรวจทุกวินาทีว่าข้อมูลสถานที่เปลี่ยนไหม
บรรทัด 454–455: ห่อ ➜ updateDateSummary() ใน frontend/app.js ให้อัปเดต hint ทุกครั้งที่เปลี่ยนวัน
บรรทัด 457–465  หน้าต่างโมดัล
457    // ---------- บันทึก / เปิดแผน ----------
458    function makeModal(id, title, sub) {
459      document.body.insertAdjacentHTML('beforeend', `<div class="modal" id="${id}"><div class="modal-backdrop" data-close></div><div class="modal-card"><div class="modal-head"><div><div class="modal-title">${title}</div><div class="modal-sub">${sub}</div></div><button class="icon-btn" data-close title="ปิด">✕</button></div><div class="modal-body" id="${id}Body"></div></div></div>`);
460      $(id).querySelectorAll('[data-close]').forEach(b => b.onclick = () => toggleModal(id, false));
461    }
462    function toggleModal(id, on) {
463      $(id).classList.toggle('open', on);
464      document.body.style.overflow = on ? 'hidden' : '';
465    }
บรรทัด 458–461: makeModal สร้างโมดัลมาตรฐาน (ชื่อ คำอธิบาย ส่วนเนื้อหา) ต่อท้าย body และผูกปุ่มปิด
บรรทัด 462–465: toggleModal เปิดหรือปิดโมดัลและล็อกการเลื่อนของหน้า
บรรทัด 467–478  บันทึกแผน
467    window.savePlan = function () {
468      const pkg = STATE.selectedPkg;
469      if (!pkg) return;
470      const list = store.get();
471      const d0 = (typeof DATE_PICKER !== 'undefined' && DATE_PICKER?.selectedDates[0]) || null;
472      list.unshift({
473        id: Date.now(), province: getProvince(), label: `${nameOf(getProvince())} · ${pkg.tier} · ${pkg.days.length} วัน`,
474        budget: +$('budget').value, travelers: +$('travelers').value, includeHotel: STATE.includeHotel !== false,
475        start: d0 ? d0.toISOString().slice(0, 10) : null, pkg,
476      });
477      showToast(store.set(list.slice(0, 20)) ? 'บันทึกแผนแล้ว (เก็บในเบราว์เซอร์นี้ ได้สูงสุด 20 แผน)' : 'บันทึกไม่ได้ พื้นที่เบราว์เซอร์เต็มหรือถูกปิดไว้', list.length ? 'ok' : 'error');
478    };
บรรทัด 467–469: savePlan ถ้าไม่มีแผนที่เลือก ออก
บรรทัด 470–476: เพิ่มรายการใหม่ไว้หน้าสุด: id (เวลา) จังหวัด ป้ายชื่อ งบ จำนวนคน ตัวเลือกโรงแรม วันเริ่ม และตัวแผนทั้งก้อน
บรรทัด 477: เก็บสูงสุด 20 แผน แล้วแจ้งผ่าน ➜ showToast() ใน frontend/app.js ว่าสำเร็จหรือไม่
บรรทัด 480–489  รายการแผนที่บันทึก
480    window.openSaved = function () {
481      const list = store.get();
482      $('savedModalBody').innerHTML = list.length ? list.map(p =>
483        `<div class="saved-row"><div><b>${esc(p.label)}</b><div class="pf-hint">งบ ${fmt(p.budget)} ฿ · ${p.travelers} คน · ${new Date(p.id).toLocaleString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH'))}</div></div>
484         <div><button class="pareto-use" onclick="loadSaved(${p.id})">เปิด</button> <button class="pareto-use" onclick="deleteSaved(${p.id})">ลบ</button></div></div>`).join('')
485        : '<p class="pf-hint">ยังไม่มีแผนที่บันทึกไว้ — กดปุ่ม "บันทึก" ในหน้าปรับแต่งทริป</p>';
486      toggleModal('savedModal', true);
487    };
488
489    window.deleteSaved = id => { store.set(store.get().filter(p => p.id !== id)); openSaved(); };
บรรทัด 480–487: openSaved สร้างแถวของแต่ละแผน (ชื่อ งบ จำนวนคน เวลา ปุ่มเปิดและลบ) ถ้าไม่มีแสดงข้อความแนะนำ แล้วเปิดโมดัล
บรรทัด 489: deleteSaved ลบแผนตาม id แล้ววาดรายการใหม่
บรรทัด 491–517  เปิดแผนที่บันทึก
491    window.loadSaved = async function (id) {
492      const p = store.get().find(x => x.id === id);
493      if (!p) return;
494      toggleModal('savedModal', false);
495      baseSlug = p.province.split('+')[0];   // แผนที่บันทึกไว้จากเวอร์ชันที่เคยมีทริปข้ามจังหวัด: เปิดด้วยจังหวัดแรก
496      $('province').value = baseSlug;
497      $('provName').textContent = nameOf(baseSlug);
498      document.querySelectorAll('.prov-item').forEach(i => i.classList.toggle('prov-active', i.dataset.value === baseSlug));
499      await loadPois();
500      $('budget').value = p.budget; $('travelers').value = p.travelers;
501      if (p.start && DATE_PICKER) {
502        const d0 = new Date(p.start + 'T00:00:00');
503        DATE_PICKER.setDate([d0, new Date(d0.getTime() + (p.pkg.days.length - 1) * 86400000)], true);
504      }
505      STATE.includeHotel = p.includeHotel;
506      STATE.packages = [p.pkg]; STATE.selectedPkg = JSON.parse(JSON.stringify(p.pkg));
507      STATE.locked.clear(); STATE.excluded.clear();
508      $('detailPanel').style.display = 'block';
509      renderDetail(STATE.selectedPkg);
510      setTimeout(() => {
511        STATE.map.setView(STATE.provinces[p.province].center, STATE.provinces[p.province].zoom);
512        STATE.map.invalidateSize(); drawOnMap(STATE.selectedPkg);
513        $('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
514        setTimeout(syncMapHeight, 150);
515      }, 150);
516      showToast('เปิดแผนที่บันทึกไว้แล้ว', 'ok');
517    };
บรรทัด 491–494: loadSaved หาแผน ปิดโมดัล
บรรทัด 495–498: ตั้งจังหวัดที่เลือก (แผนที่บันทึกไว้จากเวอร์ชันที่เคยมีทริปข้ามจังหวัดจะเปิดด้วยจังหวัดแรก) ตั้งช่องและชื่อ และไฮไลต์จังหวัดในเมนู
บรรทัด 499: โหลดสถานที่ของจังหวัดด้วย ➜ loadPois() ใน frontend/app.js
บรรทัด 500–504: คืนค่าฟอร์ม: งบ จำนวนคน และช่วงวันที่
บรรทัด 505–509: ตั้งสถานะ: ตัวเลือกโรงแรม แพ็กเกจ แผนที่เลือก (ทำสำเนาลึก) ล้างจุดที่ล็อกและลบ แล้วแสดงหน้ารายละเอียดด้วย ➜ renderDetail() ใน frontend/app.js
บรรทัด 510–515: หน่วง 150 มิลลิวินาทีให้หน้าต่างแสดงก่อน แล้วตั้งมุมมองแผนที่ วาดแผน เลื่อนหน้า และปรับความสูงแผนที่ (➜ syncMapHeight() ใน frontend/app.js)
บรรทัด 516: แจ้งว่าเปิดแล้ว
บรรทัด 520–541  เทียบอัลกอริทึม
520    window.openCompare = async function () {
521      if (!STATE.selectedPkg) return;
522      const body = {province: getProvince(), preferences: getPreferences(), budget: +$('budget').value,
523        days: STATE.selectedPkg.days.length, travelers: +$('travelers').value, include_hotel: STATE.includeHotel !== false, seed: 12345};
524      const t = showToast('กำลังรัน Greedy, GA และ Hybrid บนโจทย์เดียวกัน (GA ใช้เวลาหลายวินาที)...', 'loading', 60000);
525      try {
526        const res = await Promise.all(['greedy', 'ga', 'hybrid'].map(async a => {
527          const r = await fetch(`${API_BASE}/api/packages`, {method: 'POST', headers: devHeaders(), body: JSON.stringify({...body, algorithm: a})});
528          if (!r.ok) throw new Error(`${a}: HTTP ${r.status}`);
529          return [a, (await r.json()).packages];
530        }));
531        const km = p => p.days.reduce((s, d) => s + d.distance_km, 0);
532        let rows = '';
533        res.forEach(([a, pk]) => pk.forEach(p => {
534          rows += `<tr class="${a === 'hybrid' ? 'cmp-main' : ''}"><td>${ALGO_NAMES[a]}</td><td>${p.tier}</td><td>${p.total_score.toFixed(1)}</td><td>${fmt(p.total_cost)}</td><td>${km(p).toFixed(0)}</td><td>${p.runtime_ms < 1000 ? Math.round(p.runtime_ms) + ' ms' : (p.runtime_ms / 1000).toFixed(1) + ' s'}</td><td>${p.valid ? '✓' : '✗'}</td></tr>`;
535        }));
536        $('compareModalBody').innerHTML = `<table class="pareto-table"><tr><th>อัลกอริทึม</th><th>แพ็กเกจ</th><th>คะแนนรวม</th><th>ค่าใช้จ่าย (฿)</th><th>ระยะทาง (km)</th><th>เวลาคำนวณ</th><th>ผ่านข้อจำกัด</th></tr>${rows}</table>
537          <p class="pf-hint">โจทย์เดียวกัน (${body.days} วัน งบ ${fmt(body.budget)} ฿ ${body.travelers} คน) seed เดียวกัน — Hybrid เป็นอัลกอริทึมหลัก ส่วน Greedy และ GA เป็นเส้นฐานเปรียบเทียบ</p>`;
538        t.remove();
539        toggleModal('compareModal', true);
540      } catch (e) { t.remove(); showToast(`ผิดพลาด: ${e.message}`, 'error'); }
541    };
บรรทัด 520–523: openCompare ถ้าไม่มีแผนออก เตรียมคำขอด้วยค่าในฟอร์ม และ seed 12345 เพื่อให้ทุกอัลกอริทึมเจอโจทย์เดียวกัน
บรรทัด 524: แจ้งสถานะกำลังรัน
บรรทัด 526–530: ส่งคำขอสามตัวพร้อมกันไปที่ ➜ create_packages() ใน backend/main.py ด้วยอัลกอริทึม Greedy (➜ algorithm/greedy.py) GA (➜ algorithm/genetic.py) และ Hybrid (➜ algorithm/hybrid.py) แล้วรอทุกคำตอบ (ถ้าตัวใดล้มเหลวโยนข้อผิดพลาด)
บรรทัด 531–535: คำนวณระยะทางรวมของแต่ละแผน แล้วสร้างแถวตาราง (แถว Hybrid ถูกเน้น)
บรรทัด 536–537: ใส่ตารางและหมายเหตุในโมดัล
บรรทัด 538–540: ลบข้อความกำลังรัน แล้วเปิดโมดัล ถ้าผิดพลาดแจ้งข้อผิดพลาด
บรรทัด 544–560  ตัวเลือกอาหาร
544    function initDietSelect() {
545      const sel = $('prefDiet'); if (!sel) return;
546      sel.style.display = 'none';
547      sel.insertAdjacentHTML('afterend', '<div class="diet-wrap"><button type="button" class="diet-btn" id="dietBtn"></button><div class="diet-list" id="dietList"></div></div>');
548      const btn = $('dietBtn'), list = $('dietList');
549      const paint = () => {
550        btn.innerHTML = `<span>${esc(sel.selectedOptions[0].textContent)}</span><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>`;
551        list.innerHTML = [...sel.options].map(o => `<div class="diet-item${o.value === sel.value ? ' on' : ''}" data-v="${o.value}">${esc(o.textContent)}</div>`).join('');
552      };
553      btn.onclick = e => { e.stopPropagation(); list.classList.toggle('open'); btn.classList.toggle('open'); };
554      list.onclick = e => {
555        const it = e.target.closest('.diet-item'); if (!it) return;
556        sel.value = it.dataset.v; updatePrefSummary(); paint(); list.classList.remove('open'); btn.classList.remove('open');
557      };
558      document.addEventListener('click', () => { list.classList.remove('open'); btn.classList.remove('open'); });
559      paint();
560    }
บรรทัด 544–547: initDietSelect ซ่อน select เดิม (➜ frontend/index.html ช่อง #prefDiet) และแทรกปุ่มกับรายการแทน
บรรทัด 548–552: paint วาดข้อความที่เลือกและรายการตัวเลือก
บรรทัด 553: คลิกปุ่มเพื่อเปิดปิดรายการ
บรรทัด 554–557: คลิกรายการเพื่อตั้งค่า select เรียก ➜ updatePrefSummary() ใน frontend/app.js วาดใหม่ และปิดรายการ
บรรทัด 558–559: คลิกที่อื่นเพื่อปิดรายการ แล้ววาดครั้งแรก
บรรทัด 563–582  โหมด Developer ต้องใส่รหัส
563    const origToggleDev = toggleDevMode;
564    toggleDevMode = function () {
565      if (STATE.dev) return origToggleDev();
566      $('devPw').value = ''; $('devErr').textContent = '';
567      toggleModal('devModal', true); setTimeout(() => $('devPw').focus(), 50);
568    };
569    window.submitDevPw = async function () {   // ตรวจรหัสที่ backend (ไม่ฝังรหัสไว้ในหน้าเว็บ)
570      try {
571        const r = await fetch(`${API_BASE}/api/dev/unlock`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({password: $('devPw').value})});
572        if (r.ok) {
573          try { localStorage.setItem('wet_dev_token', (await r.json()).token); } catch (e) { /* ไม่เก็บค่า */ }
574          toggleModal('devModal', false); origToggleDev();
575        } else {
576          $('devErr').textContent = (await r.json().catch(() => ({}))).detail || 'รหัสผ่านไม่ถูกต้อง';
577          $('devPw').select();
578        }
579      } catch (e) { $('devErr').textContent = 'เชื่อมต่อ backend ไม่ได้'; }
580    };
581    // เปิดหน้าใหม่ขณะจำโหมด Developer ไว้ แต่โทเค็นหมดอายุ (เซิร์ฟเวอร์รีสตาร์ท) → ปิดโหมดให้
582    setTimeout(() => { if (STATE.dev) fetch(`${API_BASE}/api/dev/check`, {headers: devHeaders()}).then(r => r.json()).then(j => { if (!j.ok) setDevMode(false); }).catch(() => {}); }, 1500);
บรรทัด 563–568: ห่อ ➜ toggleDevMode() ใน frontend/app.js: ถ้าเปิดอยู่แล้วเรียกของเดิมเพื่อปิด ไม่เช่นนั้นล้างช่องรหัสแล้วเปิดโมดัลถามรหัส
บรรทัด 569–580: submitDevPw ส่งรหัสไปตรวจที่ ➜ dev_unlock() ใน backend/main.py (ไม่ฝังรหัสไว้ในหน้าเว็บ) ถ้าถูก เก็บโทเค็นใน localStorage ปิดโมดัล และเปิดโหมดด้วยฟังก์ชันเดิม ถ้าผิดแสดงข้อความและเลือกช่องรหัส ถ้าเชื่อมต่อไม่ได้แจ้ง
บรรทัด 581–582: ถ้าเปิดหน้าด้วยโหมด Developer ที่จำไว้แต่โทเค็นหมดอายุ (เซิร์ฟเวอร์รีสตาร์ท) ตรวจกับ ➜ dev_check() ใน backend/main.py แล้วปิดโหมด (➜ setDevMode() ใน frontend/app.js)
บรรทัด 585–598  ติดตั้งปุ่มและหน้าต่าง
585    makeModal('savedModal', 'แผนของฉัน', 'แผนที่บันทึกไว้ในเบราว์เซอร์นี้');
586    makeModal('compareModal', 'เปรียบเทียบอัลกอริทึม', 'Greedy · Genetic Algorithm · Hybrid บนโจทย์เดียวกัน');
587    document.body.insertAdjacentHTML('beforeend', '<div class="modal" id="devModal"><div class="modal-backdrop" data-close></div><div class="modal-card dev-modal-card"><div class="modal-title">โหมด Developer</div><div class="modal-sub">กรอกรหัสผ่านเพื่อเข้าใช้งาน</div><input type="password" id="devPw" placeholder="รหัสผ่าน" autocomplete="off" onkeydown="if(event.keyCode===13)submitDevPw()"><div class="dev-err" id="devErr"></div><button class="pareto-use" onclick="submitDevPw()">เข้าสู่โหมด Developer</button></div></div>');
588    $('devModal').querySelectorAll('[data-close]').forEach(b => b.onclick = () => toggleModal('devModal', false));
589    initTips();
590    initDietSelect();
591    document.querySelector('.topbar-actions')?.insertAdjacentHTML('afterbegin', '<a class="icon-btn results-link dev-only" href="results.html" title="ผลการทดลอง" style="text-decoration:none;font-size:.8rem;width:auto;padding:0 .7rem">ผลทดลอง</a>');
592    document.querySelector('.topbar-actions')?.insertAdjacentHTML('afterbegin', '<button class="icon-btn saved-btn" onclick="openSaved()" title="แผนที่บันทึกไว้">★</button>');
593    document.querySelector('.detail-actions')?.insertAdjacentHTML('afterbegin',
594      '<button class="reshuffle-btn export-btn" onclick="savePlan()" title="บันทึกแผนนี้ไว้ในเบราว์เซอร์">★ บันทึก</button>' +
595      '<span class="hist-group"><button type="button" class="reshuffle-btn export-btn hist-btn disabled" id="undoBtn" onclick="undoEdit()" title="ย้อนกลับ (Ctrl+Z)"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14L4 9l5-5M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/></svg></button>' +
596      '<button type="button" class="reshuffle-btn export-btn hist-btn disabled" id="redoBtn" onclick="redoEdit()" title="เดินหน้า (Ctrl+Y)"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14l5-5-5-5M20 9H9.5a5.5 5.5 0 0 0 0 11H13"/></svg></button></span>' +
597      '<button class="reshuffle-btn export-btn dev-only" onclick="openCompare()" title="เทียบ Greedy / GA / Hybrid บนโจทย์เดียวกัน">⇄ เทียบอัลกอริทึม</button>');
598  })();
บรรทัด 585–586: สร้างโมดัลแผนของฉัน และโมดัลเทียบอัลกอริทึม
บรรทัด 587–588: สร้างโมดัลรหัสผ่านโหมด Developer และผูกปุ่มปิด
บรรทัด 589–590: เริ่ม Tips และตัวเลือกอาหาร
บรรทัด 591: เพิ่มลิงก์ "ผลทดลอง" ไป ➜ frontend/results.html (แสดงเฉพาะโหมด Developer) ที่แถบบน
บรรทัด 592: เพิ่มปุ่มดาวเปิดรายการแผนที่บันทึก
บรรทัด 593–597: เพิ่มปุ่มในกล่องปุ่มของแผน: บันทึก ย้อนกลับและเดินหน้า (➜ undoEdit() ใน frontend/app.js ➜ recordHistory() ใน frontend/app.js) และเทียบอัลกอริทึม (เฉพาะโหมด Developer)
บรรทัด 598: ปิด IIFE แรก
บรรทัด 601–639  ประวัติการแจ้งเตือน
601  // ---------- ปุ่มประวัติการแจ้งเตือน (ลอยมุมขวาล่าง เลื่อนตามผู้ใช้) ----------
602  (function () {
603    const KEY = 'wet_notif', MAX = 50;
604    let list = [], unread = 0;
605    try { list = JSON.parse(sessionStorage.getItem(KEY) || '[]'); } catch (e) { list = []; }
606    const save = () => { try { sessionStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* ไม่เก็บค่า */ } };
607    const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
608    const btn = document.createElement('button');
609    btn.type = 'button'; btn.id = 'notifBtn'; btn.className = 'notif-btn'; btn.title = 'ประวัติการแจ้งเตือน';
610    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 0 1-3.46 0"/></svg><span class="notif-badge" hidden></span>';
611    const panel = document.createElement('div');
612    panel.id = 'notifPanel'; panel.className = 'notif-panel'; panel.hidden = true;
613    panel.innerHTML = '<div class="notif-head"><b>ประวัติการแจ้งเตือน</b><button type="button" class="notif-clear">ล้างทั้งหมด</button></div><div class="notif-list"></div>';
614    document.body.append(btn, panel);
615    const badge = btn.querySelector('.notif-badge'), box = panel.querySelector('.notif-list');
616    function render() {
617      badge.hidden = !unread; badge.textContent = unread > 9 ? '9+' : unread;
618      box.innerHTML = list.length ? list.slice().reverse().map(n =>
619        `<div class="notif-item ${n.k}"><span class="notif-dot"></span><div><div class="notif-msg">${esc(n.m)}</div><div class="notif-time">${esc(n.t)}</div></div></div>`).join('')
620        : '<div class="notif-empty">ยังไม่มีการแจ้งเตือน</div>';
621    }
622    function add(msg, kind) {
623      const m = String(msg).replace(/<[^>]*>/g, '').trim();
624      if (!m || kind === 'loading') return;
625      const last = list[list.length - 1];
626      if (last && last.m === m && Date.now() - last.ts < 1500) return;   // ข้อความซ้ำติดกัน (ปุ่มถูกกดซ้ำ)
627      list.push({m, k: kind === 'error' ? 'error' : 'ok', t: new Date().toLocaleTimeString('th-TH', {hour12: false}), ts: Date.now()});
628      if (list.length > MAX) list.shift();
629      if (panel.hidden) unread++;
630      save(); render();
631    }
632    const orig = window.showToast;
633    window.showToast = function (msg, kind, duration) { try { add(msg, kind); } catch (e) { /* ประวัติพังต้องไม่ทำให้แจ้งเตือนหาย */ } return orig.apply(this, arguments); };
634    btn.addEventListener('click', e => { e.stopPropagation(); panel.hidden = !panel.hidden; if (!panel.hidden) { unread = 0; render(); } });
635    panel.querySelector('.notif-clear').addEventListener('click', () => { list = []; unread = 0; save(); render(); });
636    document.addEventListener('click', e => { if (!panel.hidden && !panel.contains(e.target) && e.target !== btn) panel.hidden = true; });
637    document.addEventListener('keydown', e => { if (e.key === 'Escape') panel.hidden = true; });
638    render();
639  })();
บรรทัด 603–606: IIFE ที่สอง: ค่าคงที่ จำนวนสูงสุด 50 รายการ อ่านรายการจาก sessionStorage และฟังก์ชัน save
บรรทัด 607: esc ป้องกัน XSS (สำเนาในขอบเขตนี้)
บรรทัด 608–610: สร้างปุ่มกระดิ่งลอยมุมขวาล่าง
บรรทัด 611–615: สร้างแผงรายการและต่อเข้า body
บรรทัด 616–621: render แสดงป้ายจำนวนที่ยังไม่อ่าน และรายการล่าสุดก่อน
บรรทัด 622–631: add ลบแท็ก HTML ข้ามข้อความว่าง/สถานะ loading และข้อความซ้ำภายใน 1.5 วินาที แล้วจดรายการ (สูงสุด 50) นับยังไม่อ่านถ้าแผงปิดอยู่ และบันทึก
บรรทัด 632–633: ห่อ ➜ showToast() ใน frontend/app.js: บันทึกประวัติก่อน (พังได้ ไม่ทำให้แจ้งเตือนหาย) แล้วเรียกของเดิม
บรรทัด 634–635: คลิกกระดิ่งเปิดปิดแผงและล้างยังไม่อ่าน คลิก "ล้างทั้งหมด" ล้างรายการ
บรรทัด 636–637: คลิกข้างนอกหรือกด Esc เพื่อปิดแผง
บรรทัด 638–639: วาดครั้งแรก แล้วปิด IIFE

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