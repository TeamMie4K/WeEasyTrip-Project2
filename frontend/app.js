// app.js - WeEasyTrip Frontend
// ระบบวางแผนท่องเที่ยวหลายจังหวัด — ส่วนแสดงผลหลัก

// เปิดจากเซิร์ฟเวอร์หน้าเว็บแยก (พอร์ต 5500) หรือไฟล์ในเครื่อง → ชี้ backend ที่ localhost:8000; ถูกเสิร์ฟจาก backend เอง (deploy) → เรียกที่เดียวกัน
const API_BASE = (location.protocol === 'file:' || location.port === '5500') ? 'http://localhost:8000' : '';

const STATE = {
  pois: [],
  hotels: [],
  poisById: {},
  packages: [],
  selectedPkg: null,
  selectedIdx: null,
  swapContext: null,
  map: null,
  mapMarkers: [],
  mapPolylines: [],
  // Track markers/polylines per day for filtering
  mapDayLayers: {},   // {dayIdx: {markers: [], polyline: line, visible: true}}
  hotelMarker: null,
  provinces: {},   // slug -> {center, zoom, ...} จาก /api/provinces
  session: null,         // {id, version, timer} เมื่อแชร์/เข้าร่วมแผนร่วมกัน
  locked: new Set(),     // POI ที่ผู้ใช้เลือกเอง (swap/เพิ่ม) — re-optimize ต้องคงไว้
  excluded: new Set(),   // POI ที่ผู้ใช้ลบ — re-optimize ห้ามใส่กลับ
};

const getProvince = () => document.getElementById('province').value;
// โทเค็นโหมด Developer (ได้จาก /api/dev/unlock หลังใส่รหัสถูก) — backend ใช้ตัดสินว่าอนุญาตให้เลือกอัลกอริทึมอื่นนอกจาก Hybrid หรือไม่
const devToken = () => { try { return localStorage.getItem('wet_dev_token') || ''; } catch (e) { return ''; } };
const devHeaders = () => ({'Content-Type': 'application/json', ...(devToken() ? {'X-Dev-Token': devToken()} : {})});

const DAY_COLORS = ['#06b6d4', '#a78bfa', '#f97316', '#10b981', '#f43f5e', '#fbbf24', '#3b82f6'];

const CAT_LABELS = {
  all: 'ทั้งหมด',
  beach: 'หาด', temple: 'วัด', viewpoint: 'จุดชมวิว',
  culture: 'วัฒนธรรม', market: 'ตลาด',
  activity: 'กิจกรรม', restaurant: 'ร้านอาหาร'
};

// ไอคอนเส้นบาง (sprite ใน index.html) แทน emoji ให้โทนเดียวกับธีม
function ic(name, cls = '') {
  return `<svg class="ic ${cls}" aria-hidden="true"><use href="#i-${name}"/></svg>`;
}
const CAT_ICON = {
  beach: ic('beach'), temple: ic('temple'), viewpoint: ic('viewpoint'),
  culture: ic('culture'), market: ic('market'),
  activity: ic('activity'), restaurant: ic('restaurant'), hotel: ic('hotel')
};

// ไอคอน SVG แบบ inline (Lucide style)
const ICON = {
  clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
  coin:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-4a2 2 0 0 0 0 4h2a2 2 0 0 1 0 4H8"/><path d="M12 6v2m0 8v2"/></svg>',
  route: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/><path d="M9 19h6a4 4 0 0 0 0-8h-6a4 4 0 0 1 0-8h6"/></svg>',
  star:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
  swap:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>',
  pin:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
  trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-2 14a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/></svg>',
  plus:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
  alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
  spin:  '<svg class="spinner" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="50" stroke-dashoffset="30" stroke-linecap="round"/></svg>',
};

// ============================================================
// เริ่มต้นระบบ
// ============================================================
window.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  initDateRange();
  initMap();
  initBudgetValidation();
  initAlgoControl();
  initPrefs();
  await loadProvinces();
  const joinId = new URLSearchParams(location.search).get('s');
  if (joinId) { await joinSession(joinId); } else { await loadPois(); }
});

const ALGO_HINTS = {
  greedy: 'Greedy: เร็วที่สุด (~10 ms) — เลือกจุดดีที่สุดทีละขั้น แต่อาจไม่ optimal ในภาพรวม',
  ga:     'Genetic Algorithm: optimization ทั้งทริปพร้อมกัน (~3-8 sec) — global optimal กว่า greedy',
  hybrid: 'Hybrid (แนะนำ): Greedy seed → GA refine → 2-opt local search (~0.3-0.7 sec) — รวมข้อดีของทั้งสอง',
  hybrid_rl: 'Hybrid + RL seed: เพิ่มแผนเริ่มต้นจาก RL policy (ฝึกในสภาพแวดล้อมจำลอง) — ดีขึ้นเล็กน้อย (~0.3%) ช้าลง ~10-20%',
};
const ALGO_NAMES = { greedy: 'Greedy', ga: 'Genetic Algorithm', hybrid: 'Hybrid', hybrid_rl: 'Hybrid + RL' };
let SELECTED_ALGO = 'hybrid';

// ============================================================
// เลือก Algorithm
// ============================================================
function initAlgoControl() {
  document.querySelectorAll('#algoControl button').forEach(b => {
    b.onclick = () => {
      document.querySelectorAll('#algoControl button').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      SELECTED_ALGO = b.dataset.val;
      document.getElementById('algoHint').textContent = ALGO_HINTS[SELECTED_ALGO];
    };
  });
  // โหมด Developer: เปิดจากปุ่ม </> บนแถบบน หรือ ?dev=1 (จำค่าไว้ใน localStorage) — โหมดปกติรัน Hybrid เท่านั้น
  let on = false;
  try { on = localStorage.getItem('wet_dev') === '1'; } catch (e) { /* ใช้ค่าเริ่มต้น */ }
  setDevMode(on);
}

function setDevMode(on) {
  STATE.dev = !!on;
  document.body.classList.toggle('dev-mode', STATE.dev);
  document.getElementById('devBtn')?.setAttribute('aria-pressed', String(STATE.dev));
  if (!STATE.dev) {   // ออกจากโหมด Developer → กลับไปใช้ Hybrid เสมอ
    SELECTED_ALGO = 'hybrid';
    document.querySelectorAll('#algoControl button').forEach(x => x.classList.toggle('active', x.dataset.val === 'hybrid'));
    document.getElementById('algoHint').textContent = ALGO_HINTS.hybrid;
  }
  try { localStorage.setItem('wet_dev', STATE.dev ? '1' : '0'); } catch (e) { /* ไม่เก็บค่า */ }
}

function toggleDevMode() {
  setDevMode(!STATE.dev);
  showToast(STATE.dev ? 'โหมด Developer: เลือกอัลกอริทึมได้' : 'โหมดปกติ: ใช้ Hybrid', 'ok', 2500);
}

// ============================================================
// ควบคุมงบ / จำนวนคน / โรงแรม
// ============================================================
function initBudgetValidation() {
  const budgetInput = document.getElementById('budget');
  if (!budgetInput) return;
  const hint = budgetInput.closest('.pf-col')?.querySelector('.pf-hint');
  if (!hint) return;
  budgetInput.addEventListener('input', () => {
    const v = +budgetInput.value;
    if (v < VALIDATION.budget.min) {
      hint.textContent = `ต้องอย่างน้อย ${fmt(VALIDATION.budget.min)} บาท (ตอนนี้ ${fmt(v || 0)})`;
      hint.style.color = 'var(--accent-danger)';
      highlightField('budget', true);
    } else if (v > VALIDATION.budget.max) {
      hint.textContent = `สูงสุด ${fmt(VALIDATION.budget.max)} บาท`;
      hint.style.color = 'var(--accent-danger)';
      highlightField('budget', true);
    } else {
      hint.textContent = `${fmt(VALIDATION.budget.min)} - ${fmt(VALIDATION.budget.max)} บาท`;
      hint.style.color = '';
      highlightField('budget', false);
    }
  });
}

// ============================================================
// ธีม (Dark / Light)
// ============================================================
function initTheme() {
  const saved = localStorage.getItem('theme') || 'dark';
  document.documentElement.dataset.theme = saved;
}

function toggleTheme() {
  const cur = document.documentElement.dataset.theme || 'dark';
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('theme', next);
  // re-tile map (since dark mode applies CSS filter)
  if (STATE.map) STATE.map.invalidateSize();
}

// ============================================================
// ตัวเลือกช่วงวันที่ (Flatpickr)
// ============================================================
let DATE_PICKER = null;
let SELECTED_DAYS = 3;

function fpLocale() {
  let en = window.WET_LANG === 'en'; try { en = en || localStorage.getItem('wet_lang') === 'en'; } catch (e) { /* ใช้ค่าเริ่มต้น */ }
  return (!en && window.flatpickr && flatpickr.l10ns && flatpickr.l10ns.th) ? 'th' : 'default';
}
window.addEventListener('wet-lang', () => { if (DATE_PICKER) { DATE_PICKER.set('locale', fpLocale()); updateDateSummary(DATE_PICKER.selectedDates); } });

function initDateRange() {
  const today = new Date();
  const tomorrow = new Date(today.getTime() + 24*60*60*1000);
  const day4    = new Date(today.getTime() + 4*24*60*60*1000);

  DATE_PICKER = flatpickr('#dateRange', {
    mode: 'range',
    minDate: 'today',
    maxDate: new Date().fp_incr(730),
    locale: fpLocale(),
    defaultDate: [tomorrow, day4],
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'j M Y',
    onChange: (selectedDates) => {
      // ถ้าเลือกแค่วันเดียว (กำลังรอวันสิ้นสุด) ให้ onDayCreate เพิ่มคำใบ้
      updateDateSummary(selectedDates);
    },
    onDayCreate: (dObj, dStr, fp, dayElem) => {
      // ถ้าเลือก start date แล้ว และ hover/click วันเดิม → แสดง tooltip "1 วัน"
      if (fp.selectedDates.length === 1) {
        const startTs = fp.selectedDates[0].getTime();
        const cellTs  = dayElem.dateObj?.getTime();
        if (cellTs === startTs) {
          dayElem.title = 'คลิกเพื่อ One Day Trip';
        }
      }
    },
    onReady: (selectedDates, dateStr, instance) => {
      const numWrapper = instance.currentYearElement?.closest('.numInputWrapper');
      if (!numWrapper) return;
      const prev = document.createElement('span');
      prev.className = 'fp-year-prev';
      prev.textContent = '‹';
      prev.addEventListener('mousedown', (e) => {
        e.preventDefault();
        instance.changeMonth(-12, true);
      });
      const next = document.createElement('span');
      next.className = 'fp-year-next';
      next.textContent = '›';
      next.addEventListener('mousedown', (e) => {
        e.preventDefault();
        instance.changeMonth(12, true);
      });
      numWrapper.parentNode.insertBefore(prev, numWrapper);
      numWrapper.parentNode.insertBefore(next, numWrapper.nextSibling);
    },
    onOpen: (selectedDates, dateStr, instance) => {
      setTimeout(() => {
        const wrapper = document.querySelector('.date-range-input');
        const cal = instance.calendarContainer;
        if (!wrapper || !cal) return;
        // center horizontally
        const wRect = wrapper.getBoundingClientRect();
        const calW  = cal.offsetWidth;
        const newLeft = wRect.left + wRect.width / 2 - calW / 2 + window.scrollX;
        cal.style.left = Math.max(8, newLeft) + 'px';
        // shift up so calendar doesn't cover the input
        const calH = cal.offsetHeight;
        cal.style.top  = (wRect.top + window.scrollY - calH - 12) + 'px';
      }, 0);
    },
    onClose: (selectedDates) => {
      // ถ้าปิดโดยมีแค่ 1 วัน → ถือว่าเป็น One Day Trip
      if (selectedDates.length === 1) {
        const d = selectedDates[0];
        DATE_PICKER.setDate([d, d], false);
        updateDateSummary([d, d]);
      }
    },
  });
  updateDateSummary([tomorrow, day4]);

  // ให้กดที่ไหนก็ได้บนกล่องวันที่ (รวมขอบและไอคอน) แล้วเปิด calendar
  const wrapper = document.querySelector('.date-range-input');
  if (wrapper) {
    wrapper.addEventListener('click', function() {
      if (DATE_PICKER && !DATE_PICKER.isOpen) DATE_PICKER.open();
    });
  }
}

// ============================================================
// ตัวช่วยวันที่
// ============================================================
function getSelectedDays() {
  return SELECTED_DAYS;
}

function updateDateSummary(dates) {
  const sumEl = document.getElementById('dateSummary');
  const fmtDate = d => d.toLocaleDateString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH'), {day:'numeric', month:'short', year:'numeric'});

  // กำลังเลือกวันแรก (ยังไม่ได้เลือกวันสิ้นสุด)
  if (!dates || dates.length < 1) {
    sumEl.textContent = 'กรุณาเลือกช่วงวันเดินทาง';
    sumEl.className = 'date-summary invalid';
    SELECTED_DAYS = 3;
    setOneDayTripMode(false);
    return;
  }

  // เลือกวันเดียว (คลิก 1 ครั้ง หรือเลือกวันเดิม 2 ครั้ง)
  if (dates.length === 1) {
    sumEl.innerHTML = `${ic('sunrise')} <b>One Day Trip</b> · ${fmtDate(dates[0])} — เลือกวันสิ้นสุดหรือคลิกวันเดิมอีกครั้ง`;
    sumEl.className = 'date-summary oneday';
    SELECTED_DAYS = 1;
    setOneDayTripMode(true);
    return;
  }

  const [ci, co] = dates;
  const nights = Math.round((co - ci) / (24*60*60*1000));
  const days = nights + 1;

  if (nights === 0) {
    // เลือกวันเดิมเป็น start และ end → One Day Trip
    sumEl.innerHTML = `${ic('sunrise')} <b>One Day Trip</b> · ${fmtDate(ci)}`;
    sumEl.className = 'date-summary oneday';
    SELECTED_DAYS = 1;
    setOneDayTripMode(true);
  } else if (days > 7) {
    sumEl.innerHTML = `เลือกได้ไม่เกิน 7 วัน (ขณะนี้ <b>${days} วัน ${nights} คืน</b>) — ระบบจะใช้แค่ 7 วัน`;
    sumEl.className = 'date-summary invalid';
    SELECTED_DAYS = 7;
    setOneDayTripMode(false);
  } else {
    sumEl.innerHTML = `<b>${fmtDate(ci)}</b> → <b>${fmtDate(co)}</b> · ${days} วัน ${nights} คืน`;
    sumEl.className = 'date-summary';
    SELECTED_DAYS = days;
    setOneDayTripMode(false);
  }
}

function setOneDayTripMode(isOneDay) {
  const checkbox = document.getElementById('includeHotel');
  const label    = document.getElementById('hotelToggleLabel');
  const hint     = document.getElementById('hotelHint');
  const card     = document.getElementById('hotelOptionCard');
  const icon     = document.getElementById('hotelCardIcon');
  if (!checkbox) return;

  if (isOneDay) {
    checkbox.checked  = false;
    checkbox.disabled = true;
    card?.classList.add('hotel-card-locked');
    if (icon) icon.innerHTML = ic('lock');
    // Badge inline กับ title row
    const titleRow = card?.querySelector('.hotel-card-title-row');
    if (titleRow && !titleRow.querySelector('.hotel-lock-badge')) {
      const badge = document.createElement('span');
      badge.className = 'hotel-lock-badge';
      badge.innerHTML = ic('sunrise') + ' One Day Trip';
      titleRow.appendChild(badge);
    }
    label.textContent = 'ไม่รวมค่าโรงแรม';
    hint.textContent  = 'ทริปวันเดียวไม่มีค่าที่พัก — ใช้งบทั้งหมดสำหรับกิจกรรม';
  } else {
    checkbox.disabled = false;
    card?.classList.remove('hotel-card-locked');
    if (icon) icon.innerHTML = checkbox.checked ? ic('hotel') : ic('hotel-off');
    card?.querySelector('.hotel-lock-badge')?.remove();
    onHotelToggle();
  }
}

function changeTravelers(delta) {
  const inp = document.getElementById('travelers');
  const v = Math.min(10, Math.max(1, +inp.value + delta));
  inp.value = v;
}

function toggleHotelOption() {
  // คลิกที่ card ทั้งใบ → toggle checkbox (ยกเว้นเมื่อล็อค)
  const checkbox = document.getElementById('includeHotel');
  if (!checkbox || checkbox.disabled) return;
  checkbox.checked = !checkbox.checked;
  onHotelToggle();
}

function onHotelToggle() {
  const checkbox = document.getElementById('includeHotel');
  if (checkbox?.disabled) return;  // ล็อคโดย One Day Trip
  const checked = checkbox?.checked;
  const label = document.getElementById('hotelToggleLabel');
  const hint  = document.getElementById('hotelHint');
  const icon  = document.getElementById('hotelCardIcon');
  if (checked) {
    label.textContent = 'รวมค่าโรงแรมในงบประมาณ';
    hint.textContent  = 'ระบบจะหักค่าโรงแรมออกจากงบก่อนวางแผนกิจกรรม';
    if (icon) icon.innerHTML = ic('hotel');
  } else {
    label.textContent = 'ไม่รวมค่าโรงแรม';
    hint.textContent  = 'เหมาะสำหรับทริปวันเดียว หรือมีที่พักของตัวเองแล้ว';
    if (icon) icon.innerHTML = ic('hotel-off');
  }
}

// ============================================================
// เริ่มต้นแผนที่
// ============================================================
function initMap() {
  STATE.map = L.map('map', {zoomControl: true, attributionControl: false}).setView([7.88, 98.36], 11);
  // tile.openstreetmap.org ตอบ 403 (Access blocked) เมื่อรันจาก localhost และ CARTO ต้องใช้ API key
  // จึงใช้ Esri World Street Map ซึ่งไม่ต้องมี key (ต้องแสดง attribution)
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
  }).addTo(STATE.map);
  L.control.attribution({prefix: false}).addAttribution('Tiles © Esri — Esri, HERE, Garmin, © OpenStreetMap contributors').addTo(STATE.map);
}

// ============================================================
// แสดงสถานะ API
// ============================================================
function setApiStatus(state, text) {
  const el = document.getElementById('apiStatus');
  el.className = 'api-status ' + state;
  el.querySelector('.status-text').textContent = text;
}

// ============================================================
// ความชอบของผู้ใช้ (หมวดที่ชอบ/ไม่เอา + อาหาร) — ส่งให้ backend กรอง/ถ่วงน้ำหนักก่อนปรับแผน
// ============================================================
const PREF = {};   // category -> 'like' | 'avoid' (ไม่มีคีย์ = ปกติ)

function initPrefs() {
  const box = document.getElementById('prefChips');
  if (!box) return;
  Object.entries(CAT_LABELS).filter(([k]) => k !== 'all' && k !== 'restaurant').forEach(([k, label]) => {
    // ชื่อหมวด + ปุ่มไอคอน 👍 (ชอบ) / 👎 (ไม่ชอบ) ด้านหลัง กดซ้ำเพื่อยกเลิก — พื้นหลังเขียว=ชอบ แดง=ไม่ชอบ
    const w = document.createElement('div');
    w.className = 'pref-cat';
    w.dataset.cat = k;
    w.innerHTML = `<span class="pc-name">${label}</span><button type="button" class="pc-like" title="ชอบ">${ic('thumb')}</button><button type="button" class="pc-dislike" title="ไม่ชอบ">${ic('thumb')}</button>`;
    const paint = () => {
      w.dataset.state = PREF[k] || '';
      w.querySelector('.pc-like').title = PREF[k] === 'like' ? 'ยกเลิก "ชอบ"' : 'ชอบ';
      w.querySelector('.pc-dislike').title = PREF[k] === 'avoid' ? 'ยกเลิก "ไม่ชอบ"' : 'ไม่ชอบ';
    };
    const set = st => { if (PREF[k] === st) delete PREF[k]; else PREF[k] = st; paint(); updatePrefSummary(); };
    w.querySelector('.pc-like').onclick = () => set('like');
    w.querySelector('.pc-dislike').onclick = () => set('avoid');
    paint();
    box.appendChild(w);
  });
}

function togglePrefs() {
  const p = document.getElementById('prefPanel');
  p.hidden = !p.hidden;
  document.getElementById('prefToggle')?.setAttribute('aria-expanded', String(!p.hidden));
}

function getPreferences() {
  const liked = Object.keys(PREF).filter(k => PREF[k] === 'like');
  const avoided = Object.keys(PREF).filter(k => PREF[k] === 'avoid');
  const diet = document.getElementById('prefDiet')?.value || 'none';
  return (liked.length || avoided.length || diet !== 'none') ? {liked, avoided, diet} : null;
}

function updatePrefSummary() {
  const p = getPreferences();
  const dietLabel = {vegetarian: 'มังสวิรัติ', halal: 'ฮาลาล'};
  document.getElementById('prefSummary').textContent = p
    ? '· ' + [p.liked.length && `ชอบ ${p.liked.length}`, p.avoided.length && `ไม่ชอบ ${p.avoided.length}`, dietLabel[p.diet]].filter(Boolean).join(' · ')
    : '';
}

// ============================================================
// ส่งออกแผนเป็นไฟล์ปฏิทิน (.ics) — เวลาแบบ local (floating) ตามตารางที่อัลกอริทึมคำนวณ
// ============================================================
function icsEscape(s) {
  return String(s).replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;');
}

// พับบรรทัดตาม RFC 5545 (≤75 octets ต่อบรรทัด) โดยไม่ตัดกลางตัวอักษร UTF-8
function icsFold(line) {
  const enc = new TextEncoder();
  const out = [];
  let cur = '', bytes = 0;
  for (const ch of line) {
    const n = enc.encode(ch).length;
    if (bytes + n > (out.length ? 74 : 75)) { out.push(cur); cur = ''; bytes = 0; }
    cur += ch; bytes += n;
  }
  out.push(cur);
  return out.join('\r\n ');
}

function buildIcs(pkg, startDate) {
  const pad = n => String(n).padStart(2, '0');
  const stamp = d => `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}`;
  const local = (d, min) => `${stamp(d)}T${pad(Math.floor(min / 60) % 24)}${pad(min % 60)}00`;
  const now = new Date().toISOString().replace(/[-:]/g, '').slice(0, 15) + 'Z';
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//WeEasyTrip//TH', 'CALSCALE:GREGORIAN',
                 'X-WR-CALNAME:' + icsEscape(`WeEasyTrip ${pkg.tier}`), 'X-WR-TIMEZONE:Asia/Bangkok'];
  pkg.days.forEach((day, dIdx) => {
    const date = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate() + dIdx);
    const arrive = Object.fromEntries((day.arrivals || []).map(([id, m]) => [id, m]));
    day.pois.forEach(poi => {
      const start = arrive[poi.id];
      if (start === undefined) return;
      const desc = `${CAT_LABELS[poi.category] || poi.category} · ค่าใช้จ่าย ${fmt(poi.cost)} บาท`;
      lines.push('BEGIN:VEVENT',
        `UID:${poi.id}-${stamp(date)}-${dIdx}@weeasytrip`,
        `DTSTAMP:${now}`,
        `DTSTART:${local(date, start)}`,
        `DTEND:${local(date, start + poi.duration_min)}`,
        'SUMMARY:' + icsEscape(poi.name_th || poi.name_en),
        'DESCRIPTION:' + icsEscape(desc),
        `GEO:${poi.lat};${poi.lng}`,
        'LOCATION:' + icsEscape(poi.name_en || poi.name_th),
        'END:VEVENT');
    });
  });
  lines.push('END:VCALENDAR');
  return lines.map(icsFold).join('\r\n') + '\r\n';
}

function exportIcs() {
  const pkg = STATE.selectedPkg;
  if (!pkg) return;
  const start = (DATE_PICKER && DATE_PICKER.selectedDates[0]) || new Date();
  const blob = new Blob([buildIcs(pkg, start)], {type: 'text/calendar;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `weeasytrip-${getProvince()}-${pkg.tier.toLowerCase()}.ics`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  showToast('ดาวน์โหลดไฟล์ปฏิทินแล้ว', 'ok');
}

// ============================================================
// Collaborative planning: แชร์ลิงก์ให้เพื่อนดู/แก้แผนเดียวกัน (โพลลิ่งทุก 2 วินาที, version กันชนกัน)
// ============================================================
function sessionSettings() {
  const d = DATE_PICKER && DATE_PICKER.selectedDates[0];
  return {
    budget: +document.getElementById('budget').value,
    travelers: +document.getElementById('travelers').value,
    include_hotel: STATE.includeHotel !== false,
    start_date: d ? `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}` : null,
    preferences: getPreferences(),
    locked: [...STATE.locked], excluded: [...STATE.excluded],
  };
}

function applySharedState(data, announce) {
  STATE.selectedPkg = data.package;
  const st = data.settings || {};
  STATE.locked = new Set(st.locked || []);
  STATE.excluded = new Set(st.excluded || []);
  STATE.session.version = data.version;
  drawOnMap(STATE.selectedPkg);
  renderDetail(STATE.selectedPkg);
  if (announce) showToast(announce, 'ok', 3000);
}

async function shareSession() {
  const pkg = STATE.selectedPkg;
  if (!pkg) return;
  try {
    if (!STATE.session) {
      const res = await fetch(`${API_BASE}/api/sessions`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({province: getProvince(), package: pkg, settings: sessionSettings()}),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      STATE.session = {id: data.id, version: data.version, timer: null, busy: false};
      history.replaceState(null, '', `?s=${data.id}`);
      startSessionPolling();
    }
    const url = location.href;
    try { await navigator.clipboard.writeText(url); showToast('คัดลอกลิงก์แล้ว — ส่งให้เพื่อนเพื่อวางแผนร่วมกัน', 'ok', 4500); }
    catch (e) { window.prompt('คัดลอกลิงก์นี้ส่งให้เพื่อน', url); }
  } catch (e) {
    showToast(`แชร์ไม่สำเร็จ: ${e.message}`, 'error');
  }
}

function startSessionPolling() {
  clearInterval(STATE.session.timer);
  STATE.session.timer = setInterval(async () => {
    const ss = STATE.session;
    if (!ss || ss.busy || document.hidden) return;
    try {
      const res = await fetch(`${API_BASE}/api/sessions/${ss.id}?since=${ss.version}`);
      if (res.status === 404) { clearInterval(ss.timer); showToast('เซสชันหมดอายุแล้ว', 'error'); STATE.session = null; return; }
      if (!res.ok) return;
      const data = await res.json();
      if (data.changed) applySharedState(data, 'เพื่อนแก้ไขแผน — อัปเดตให้แล้ว');
    } catch (e) { /* เครือข่ายสะดุด: ลองใหม่รอบหน้า */ }
  }, 2000);
}

// ส่งแผนที่แก้ไขในเครื่องขึ้นเซสชัน ถ้ามีคนแก้ก่อน (409) ให้ใช้ฉบับล่าสุดของเซิร์ฟเวอร์
async function pushSession() {
  const ss = STATE.session;
  if (!ss) return;
  ss.busy = true;
  try {
    const res = await fetch(`${API_BASE}/api/sessions/${ss.id}`, {
      method: 'PUT', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({base_version: ss.version, package: STATE.selectedPkg, settings: sessionSettings()}),
    });
    if (res.status === 409) {
      const err = await res.json();
      applySharedState(err.detail, 'มีคนแก้ไขพร้อมกัน — ใช้ฉบับล่าสุดของเพื่อน');
    } else if (res.ok) {
      ss.version = (await res.json()).version;
    }
  } catch (e) { /* ออฟไลน์: เก็บไว้ในเครื่อง */ }
  finally { ss.busy = false; }
}

async function joinSession(id) {
  try {
    const res = await fetch(`${API_BASE}/api/sessions/${id}`);
    if (!res.ok) throw new Error(res.status === 404 ? 'ลิงก์หมดอายุหรือไม่ถูกต้อง' : `HTTP ${res.status}`);
    const data = await res.json();
    const st = data.settings || {};
    const item = [...document.querySelectorAll('#provList .prov-item')].find(i => i.dataset.value === data.province);
    if (item) {                                   // ตั้งจังหวัดโดยไม่ล้างผลซ้ำ แล้วโหลดข้อมูลจังหวัดนั้น
      document.querySelectorAll('.prov-item').forEach(i => i.classList.remove('prov-active'));
      item.classList.add('prov-active');
      document.getElementById('province').value = data.province;
      document.getElementById('provName').textContent = item.dataset.label;
    }
    await loadPois();
    if (st.budget) document.getElementById('budget').value = st.budget;
    if (st.travelers) document.getElementById('travelers').value = st.travelers;
    if (st.start_date && DATE_PICKER) {
      const d0 = new Date(st.start_date + 'T00:00:00');
      const d1 = new Date(d0.getTime() + (data.package.days.length - 1) * 86400000);
      DATE_PICKER.setDate([d0, d1], true);
    }
    STATE.includeHotel = st.include_hotel !== false;
    STATE.session = {id: data.id, version: data.version, timer: null, busy: false};
    document.getElementById('detailPanel').style.display = 'block';
    STATE.selectedPkg = data.package;
    STATE.locked = new Set(st.locked || []); STATE.excluded = new Set(st.excluded || []);
    renderDetail(STATE.selectedPkg);
    setTimeout(() => {
      STATE.map.invalidateSize();
      drawOnMap(STATE.selectedPkg);
      document.getElementById('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
      setTimeout(syncMapHeight, 150);
    }, 150);
    startSessionPolling();
    showToast('เข้าร่วมแผนที่เพื่อนแชร์มา — แก้ไขแล้วทุกคนเห็นพร้อมกัน', 'ok', 4500);
  } catch (e) {
    showToast(`เข้าร่วมไม่ได้: ${e.message}`, 'error', 6000);
    await loadPois();
  }
}

// ============================================================
// รายละเอียดสถานที่: เวลาเปิด-ปิด + รีวิว (รีวิวเป็นข้อมูลจำลองเพื่อสาธิตฟีเจอร์ ไม่ใช่ข้อมูลจริง)
// ============================================================
function fmtClock(min) {
  return `${String(Math.floor(min / 60) % 24).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`;
}

// เก็บแผนตั้งต้นไว้เป็นคุณสมบัติที่ไม่ถูก serialize (ไม่ปนใน session/ไฟล์บันทึก)
function setHidden(obj, key, value) { Object.defineProperty(obj, key, {value, enumerable: false, writable: true, configurable: true}); }
const routeIds = p => JSON.stringify((p?.days || []).map(d => d.pois.map(x => x.id)));
// ย้อนกลับ / เดินหน้า (undo / redo) ทีละการแก้ไขเหมือนโปรแกรมแต่งภาพ: เก็บสำเนาแผนหลังการแก้แต่ละครั้ง (ลาก ลบ สลับ เพิ่ม สลับเป็นในร่ม) ผูกกับแผนตั้งต้น (_orig) ถ้าสร้างแผนใหม่ประวัติจะเริ่มใหม่
const HIST = {orig: null, base: null, stack: [], idx: -1, applying: false};
const histSnap = pkg => ({sig: routeIds(pkg) + JSON.stringify([...STATE.locked].sort()) + JSON.stringify([...STATE.excluded].sort()), pkg: JSON.parse(JSON.stringify(pkg)), locked: [...STATE.locked], excluded: [...STATE.excluded]});
function recordHistory(pkg) {
  if (HIST.applying || !pkg._orig) return;
  const s = histSnap(pkg);
  if (HIST.orig !== pkg._orig) { HIST.orig = pkg._orig; HIST.stack = [s]; HIST.idx = 0; }
  else if (s.sig !== HIST.stack[HIST.idx].sig) { HIST.stack = HIST.stack.slice(0, HIST.idx + 1); HIST.stack.push(s); HIST.idx++; if (HIST.stack.length > 50) { HIST.stack.shift(); HIST.idx--; } }
  HIST.base = pkg._base;
  updateHistBtns();
}
function updateHistBtns() {
  const u = document.getElementById('undoBtn'), r = document.getElementById('redoBtn');
  if (u) u.classList.toggle('disabled', HIST.idx <= 0);
  if (r) r.classList.toggle('disabled', HIST.idx >= HIST.stack.length - 1);
}
function stepHistory(dir) {
  const n = HIST.idx + dir; if (n < 0 || n >= HIST.stack.length || !STATE.selectedPkg) return;
  HIST.idx = n; const e = HIST.stack[n], c = JSON.parse(JSON.stringify(e.pkg));
  setHidden(c, '_orig', HIST.orig); c._base = HIST.base;
  STATE.selectedPkg = c; STATE.locked = new Set(e.locked); STATE.excluded = new Set(e.excluded);
  HIST.applying = true;
  try { drawOnMap(c); renderDetail(c); } finally { HIST.applying = false; }
  updateHistBtns(); pushSession();
  showToast(dir < 0 ? 'ย้อนกลับแล้ว' : 'ทำซ้ำแล้ว', 'ok', 1800);
}
const undoEdit = () => stepHistory(-1), redoEdit = () => stepHistory(1);
document.addEventListener('keydown', e => {
  if (!(e.ctrlKey || e.metaKey) || e.target.closest?.('input, textarea, select, [contenteditable]') || document.querySelector('.modal.open')) return;
  const k = e.key.toLowerCase();
  if (k === 'z' && !e.shiftKey) { e.preventDefault(); undoEdit(); } else if (k === 'y' || (k === 'z' && e.shiftKey)) { e.preventDefault(); redoEdit(); }
});

// คำเตือนที่แสดงแก่ผู้ใช้: เฉพาะ "อาจไปไม่ทันเวลาปิด" และ "อาจไปถึงก่อนร้านเปิด" (ไม่เตือนเรื่องช่วงเวลามื้อ เวลารวมต่อวัน — ผู้ใช้จัดเองได้)
// ไม่บอกเวลาถึงที่แน่นอน เพราะไม่รู้ว่าผู้ใช้จะออกเดินทางจริงกี่โมง; เวลาถึงตามแผนเป็นการประมาณจากเวลาเริ่มวัน 08:00 + เวลาเที่ยว + เวลาเดินทาง
function uiWarnings(pkg, raw = false) {
  const out = [], speed = (STATE.provinces[getProvince().split('+')[0]] || {}).speed_kmh || 40;
  (pkg.days || []).forEach((day, d) => {
    let endT = 480, lat = pkg.hotel.lat, lng = pkg.hotel.lng;
    day.pois.forEach(p => {
      const full = {...(STATE.pois.find(q => q.id === p.id) || {}), ...p}, at = arriveOf(day, p);
      const km = haversineKm(lat, lng, p.lat, p.lng), early = endT + km / speed * 60 * 1.25 + (km >= 0.3 ? 10 : 0);   // เวลาถึงก่อนรอร้านเปิด (ตัวคูณจราจร 1.25 + เผื่อจอด/เดิน 10 นาที ตรงกับ algorithm/utils.py)
      if (full.close_min !== undefined && at >= 0 && at > full.close_min) out.push({d, id: p.id, type: 'late', poi: full});
      else if (full.open_min > 0 && early < full.open_min - 10) out.push({d, id: p.id, type: 'early', poi: full});
      endT = (at >= 0 ? at : early) + (p.duration_min || 0); lat = p.lat; lng = p.lng;
    });
  });
  const key = w => `${w.id}:${w.type}`;
  if (raw) return out;
  // แผนที่ระบบสร้างเองมีการรอร้านเปิดตามปกติ จึงไม่เตือน: จำคำเตือนตั้งต้นของแผนไว้ (_base) แล้วแสดงเฉพาะที่เกิดใหม่หลังผู้ใช้แก้แผน
  if (!pkg._base) { pkg._base = new Set(out.map(key)); return []; }
  return out.filter(w => !pkg._base.has(key(w)));
}

// รูปแบบระยะเวลา: น้อยกว่า 60 นาที = 45m, ตั้งแต่ 60 นาที = 1H / 1H 30m
function fmtDur(min) {
  const m = Math.round(min), h = Math.floor(m / 60), r = m % 60;
  return h ? (r ? `${h}H ${r}m` : `${h}H`) : `${r}m`;
}

function arriveOf(day, poi) {   // เวลาถึงที่อัลกอริทึมคำนวณ (นาทีจากเที่ยงคืน) หรือ -1 ถ้าไม่มี
  const a = (day.arrivals || []).find(x => x[0] === poi.id);
  return a ? a[1] : -1;
}

function hoursText(poi) {
  if (poi.open_min === undefined) poi = STATE.pois.find(p => p.id === poi.id) || poi;   // POI ในแผนจาก API ไม่มีเวลาเปิด-ปิด
  if (poi.open_min === undefined) return 'ไม่ระบุ';
  if (poi.open_min <= 0 && poi.close_min >= 1439) return 'ทั้งวัน';
  return `${fmtClock(poi.open_min)}–${fmtClock(poi.close_min)}`;
}

function strHash(str) {
  let h = 2166136261;
  for (const ch of str) { h ^= ch.codePointAt(0); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

const MOCK_REVIEWS = {
  beach: ['ทรายสะอาด น้ำใส เหมาะมาช่วงเช้าที่คนยังน้อย', 'วิวสวย มีร้านอาหารริมหาด แต่ช่วงบ่ายแดดแรง', 'เดินเล่นสบาย จอดรถง่าย บรรยากาศผ่อนคลาย'],
  temple: ['สถาปัตยกรรมสวยงาม ควรแต่งกายสุภาพ', 'บรรยากาศสงบ เหมาะกับการมาช่วงเช้า', 'มีประวัติน่าสนใจ ใช้เวลาเดินชมไม่นาน'],
  viewpoint: ['วิวกว้างมาก ถ่ายรูปสวยโดยเฉพาะช่วงเย็น', 'ทางขึ้นค่อนข้างชัน ควรใส่รองเท้าเดินสบาย', 'คุ้มกับการมา อากาศเย็นสบาย'],
  culture: ['ให้ความรู้ดี เจ้าหน้าที่แนะนำเป็นกันเอง', 'จัดแสดงน่าสนใจ เหมาะกับครอบครัว', 'ค่าเข้าไม่แพง ใช้เวลาชมประมาณชั่วโมงกว่า'],
  market: ['ของกินหลากหลาย ราคาไม่แพง', 'คนเยอะช่วงเย็น ควรมาก่อนหัวค่ำ', 'ของฝากน่าซื้อ บรรยากาศคึกคัก'],
  activity: ['กิจกรรมสนุก เจ้าหน้าที่ดูแลดี', 'ควรจองล่วงหน้าช่วงวันหยุด', 'เหมาะกับกลุ่มเพื่อนและครอบครัว'],
  restaurant: ['รสชาติดี ราคาเหมาะสม บริการรวดเร็ว', 'ร้านบรรยากาศดี ช่วงเที่ยงคนค่อนข้างเยอะ', 'เมนูแนะนำอร่อย ที่นั่งสบาย'],
};

function mockReviewsFor(poi) {   // สร้างจาก id ของสถานที่ ได้ผลเดิมทุกครั้ง; คะแนนอิงคะแนนของระบบ
  const h = strHash(poi.id + poi.name_en);
  const rating = Math.max(3.0, Math.min(5.0, poi.score / 2 + ((h % 7) - 3) * 0.05));
  const pool = MOCK_REVIEWS[poi.category] || MOCK_REVIEWS.culture;
  const picks = [0, 1, 2].map(i => ({
    text: pool[(h + i) % pool.length],
    stars: Math.max(3, Math.min(5, Math.round(rating + (((h >> (i + 3)) % 3) - 1) * 0.6))),
  }));
  return {rating, count: 40 + (h % 860), reviews: picks};
}

function showPoiDetail(poiId, arriveMin) {
  const poi = STATE.pois.find(p => p.id === poiId);
  if (!poi) return;
  let m = document.getElementById('poiModal');
  if (!m) {
    m = document.createElement('div');
    m.className = 'modal';
    m.id = 'poiModal';
    m.innerHTML = `<div class="modal-backdrop" onclick="closePoiDetail()"></div>
      <div class="modal-card"><div class="modal-head"><div><div class="modal-title" id="poiTitle"></div>
      <div class="modal-sub" id="poiSub"></div></div>
      <button class="icon-btn" onclick="closePoiDetail()" title="ปิด"><svg class="ic "><use href="#i-close"/></svg></button></div>
      <div class="modal-body" id="poiBody"></div></div>`;
    document.body.appendChild(m);
  }
  const r = mockReviewsFor(poi);
  const stars = n => '★'.repeat(n) + '☆'.repeat(5 - n);
  document.getElementById('poiTitle').textContent = poi.name_th;
  document.getElementById('poiSub').textContent = `${poi.name_en} · ${CAT_LABELS[poi.category] || poi.category}`;
  document.getElementById('poiBody').innerHTML = `
    <div class="poi-facts">
      <div><span>เวลาเปิด-ปิด</span><b>${hoursText(poi)}</b></div>
      ${arriveMin >= 0 ? `<div><span>เวลาถึงตามแผน</span><b>${fmtClock(arriveMin)}</b></div>` : ''}
      <div><span>เวลาที่ใช้ ณ สถานที่</span><b>${poi.duration_min} นาที</b></div>
      <div><span>ค่าใช้จ่าย</span><b>${poi.cost ? fmt(poi.cost) + ' ฿' : 'ฟรี'}</b></div>
    </div>
    <p class="poi-note">เวลาเปิด-ปิดมาจากข้อมูล OpenStreetMap หรือเป็นค่าประมาณตามประเภทสถานที่ ควรตรวจสอบกับสถานที่อีกครั้งก่อนเดินทาง</p>
    <div class="rev-head"><span class="rev-score">${ic('star')} ${r.rating.toFixed(1)}</span>
      <span class="rev-count">${r.count} รีวิว</span><span class="mock-chip">ข้อมูลจำลอง</span></div>
    ${r.reviews.map(v => `<div class="rev-item"><div class="rev-stars">${stars(v.stars)}</div><div>${v.text}</div></div>`).join('')}
    <p class="poi-note">รีวิวและจำนวนรีวิวเป็นข้อมูลตัวอย่างที่สร้างขึ้นเพื่อสาธิตฟีเจอร์ ไม่ใช่ความเห็นของนักท่องเที่ยวจริง (รีวิวจริงเป็นแนวทางต่อยอดผ่านบริการข้อมูลสถานที่)</p>`;
  m.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closePoiDetail() {
  document.getElementById('poiModal').classList.remove('open');
  document.body.style.overflow = '';
}

// ============================================================
// Pareto: ทางเลือกที่แลกเปลี่ยนกัน (NSGA-II) — ผู้ใช้เลือกแผนตามที่ให้ความสำคัญ
// ============================================================
async function openPareto() {
  const pkg = STATE.selectedPkg;
  if (!pkg) return;
  const t = showToast('กำลังหาทางเลือกที่ดีที่สุดในแต่ละด้าน...', 'loading', 20000);
  try {
    const res = await fetch(`${API_BASE}/api/pareto`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        province: getProvince(), preferences: getPreferences(),
        budget: +document.getElementById('budget').value, days: pkg.days.length,
        travelers: +document.getElementById('travelers').value,
        include_hotel: STATE.includeHotel !== false, seed: Math.floor(Math.random() * 1000000),
      }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    STATE.paretoPlans = data.packages;
    renderParetoCards(data.packages);
    t.remove();
    (data.packages[0]?.notes || []).forEach(n => showToast(n, 'error', 6000));
    if (!data.packages.length) { showToast('ไม่พบทางเลือกที่ผ่านข้อจำกัด ลองเพิ่มงบหรือลดความชอบ', 'error', 5000); return; }
    document.getElementById('paretoModal').classList.add('open');
    document.body.style.overflow = 'hidden';
  } catch (e) {
    t.remove();
    showToast(`ผิดพลาด: ${e.message}`, 'error');
  }
}

// แปลงแผนทางเลือกให้เข้าใจง่าย: ตั้งป้ายตามจุดเด่น (ขับน้อยสุด/หลากหลายสุด/ประหยัดสุด/แนะนำ) แล้วแสดงเป็นการ์ดเทียบกับแผนปัจจุบัน
function renderParetoCards(plans) {
  const cur = STATE.selectedPkg, days = Math.max(cur.days.length, 1);
  const km = p => p.objectives.distance_km, div = p => p.objectives.diversity, cost = p => p.objectives.cost, sc = p => p.objectives.score;
  const best = (fn, dir) => plans.reduce((m, p, i) => (dir * fn(p) > dir * fn(plans[m]) ? i : m), 0);
  const labels = {};   // index → [ป้าย, คำอธิบาย]
  const put = (i, tag, why) => { (labels[i] ||= []).push([tag, why]); };
  put(best(sc, 1), 'แนะนำ', 'ได้สถานที่น่าสนใจโดยรวมสูงสุด');
  put(best(km, -1), 'ขับน้อยที่สุด', 'เดินทางสั้น เหนื่อยน้อย ประหยัดค่าเดินทาง');
  put(best(div, 1), 'หลากหลายที่สุด', 'ได้เที่ยวหลายประเภทในแต่ละวัน');
  put(best(cost, -1), 'ประหยัดที่สุด', 'ค่าใช้จ่ายรวมต่ำสุด');
  const picks = Object.keys(labels).map(Number);
  const rest = plans.map((_, i) => i).filter(i => !picks.includes(i));
  const dots = d => { const n = Math.max(1, Math.min(5, Math.round(d))); return [1, 2, 3, 4, 5].map(k => `<i class="${k <= n ? 'on' : ''}"></i>`).join(''); };
  const kmDay = p => km(p) / days;
  const diff = (v, base, unit, lessGood) => { const d = v - base; if (Math.abs(d) < 0.5) return '<span class="pc-same">เท่าแผนปัจจุบัน</span>'; const good = lessGood ? d < 0 : d > 0; return `<span class="${good ? 'pc-good' : 'pc-bad'}">${d < 0 ? '−' : '+'}${Math.abs(d).toFixed(0)} ${unit}</span>`; };
  const baseKm = cur.days.reduce((a, d) => a + d.distance_km, 0) / days;
  const card = (i, extra) => {
    const p = plans[i], tags = (labels[i] || []).map(x => x[0]), why = (labels[i] || [])[0]?.[1] || 'อีกทางเลือกที่สมดุลระหว่างระยะทาง ความหลากหลายและค่าใช้จ่าย';
    const hi = p.days.flatMap(d => d.pois).filter(x => x.category !== 'restaurant').sort((a, b) => b.score - a.score).slice(0, 3).map(x => x.name_th);
    return `<div class="pc ${tags.includes('แนะนำ') ? 'pc-main' : ''}">
      <div class="pc-top"><div>${(tags.length ? tags : ['ทางเลือก']).map(t => `<span class="pc-tag">${t}</span>`).join('')}<span class="score-chip" style="margin-left:6px">★ ${sc(p)}</span></div></div>
      <div class="pc-why">${why}</div>
      <div class="pc-metrics">
        <div><small>ขับเฉลี่ย/วัน</small><b>${kmDay(p).toFixed(0)} กม.</b>${diff(kmDay(p), baseKm, 'กม./วัน', true)}</div>
        <div><small>ความหลากหลาย</small><b class="pc-dots">${dots(div(p))}</b></div>
        <div><small>ค่าใช้จ่าย/คน</small><b>${fmt(cost(p))} ฿</b></div>
      </div>
      <div class="pc-hi">${hi.map(n => `<span>${n}</span>`).join('')}</div>
      <button class="pareto-use" onclick="usePareto(${i})">ใช้แผนนี้</button></div>`;
  };
  const box = document.getElementById('paretoTable');
  box.className = 'pc-wrap';
  box.innerHTML = picks.sort((a, b) => a - b).map(i => card(i)).join('') +
    (rest.length ? `<button class="pc-more" onclick="this.nextElementSibling.hidden=false;this.hidden=true">ดูแผนอื่นอีก ${rest.length} แบบ</button><div class="pc-wrap-in" hidden>${rest.map(i => card(i)).join('')}</div>` : '');
}

function closePareto() {
  document.getElementById('paretoModal').classList.remove('open');
  document.body.style.overflow = '';
}

function usePareto(i) {
  STATE.selectedPkg = JSON.parse(JSON.stringify(STATE.paretoPlans[i]));
  STATE.locked.clear(); STATE.excluded.clear();
  closePareto();
  drawOnMap(STATE.selectedPkg);
  renderDetail(STATE.selectedPkg);
  pushSession();
  showToast(`ใช้แผนทางเลือกที่ ${i + 1}`, 'ok');
}

// สร้างรายการจังหวัดใน dropdown จาก /api/provinces: ครบ 77 จังหวัดจัดตามภาค — จังหวัดที่มีข้อมูลเลือกได้ ที่เหลือแสดง "เร็วๆ นี้"
const REGION_ORDER = ['ภาคเหนือ', 'ภาคตะวันออกเฉียงเหนือ', 'ภาคกลาง', 'ภาคตะวันออก', 'ภาคตะวันตก', 'ภาคใต้'];

async function loadProvinces() {
  try {
    const res = await fetch(`${API_BASE}/api/provinces`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const list = document.getElementById('provList');
    const active = getProvince();
    list.innerHTML = '';
    const regions = {};
    data.provinces.forEach(pv => {
      STATE.provinces[pv.slug] = pv;
      (regions[pv.region || 'อื่น ๆ'] ||= []).push({...pv, ready: true});
    });
    data.planned.forEach(pv => (regions[pv.region] ||= []).push({...pv, ready: false}));
    const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
    [...REGION_ORDER, ...Object.keys(regions).filter(r => !REGION_ORDER.includes(r))].forEach(r => {
      const items = (regions[r] || []).sort((a, b) => (b.ready - a.ready) || a.name_th.localeCompare(b.name_th, 'th'));
      if (!items.length) return;
      list.insertAdjacentHTML('beforeend', `<div class="prov-group-label">${esc(r)}</div>`);
      items.forEach(pv => {
        const el = document.createElement('div');
        el.className = 'prov-item' + (pv.ready ? '' : ' prov-disabled') + (pv.ready && pv.slug === active ? ' prov-active' : '');
        el.dataset.label = pv.name_th;
        if (pv.ready) { el.dataset.value = pv.slug; el.onclick = () => selectProvince(el); }
        el.innerHTML = `<span class="prov-item-name">${esc(pv.name_th)}</span>` +
          (pv.ready ? (pv.sparse ? `<span class="prov-item-sparse" title="${pv.pois} สถานที่ ${pv.hotels} โรงแรม — ตัวเลือกอาจน้อย">ข้อมูลน้อย</span>` : '') + '<span class="prov-item-badge">พร้อมใช้งาน</span>' : '<span class="prov-item-soon">เร็วๆ นี้</span>');
        list.appendChild(el);
      });
    });
  } catch (e) {
    showToast('โหลดรายการจังหวัดไม่สำเร็จ', 'error', 4000);
  }
}

// เปลี่ยนจังหวัด: ล้างผลเดิม (id ของ POI ซ้ำกันข้ามจังหวัด) แล้วโหลดข้อมูลใหม่ + ย้ายแผนที่
async function onProvinceChange(slug) {
  STATE.poisById = {};
  STATE.packages = [];
  STATE.selectedPkg = null;
  STATE.selectedIdx = null;
  ['packagesSection', 'detailPanel'].forEach(id => { document.getElementById(id).style.display = 'none'; });
  const pv = STATE.provinces[slug];
  if (pv && STATE.map) STATE.map.setView(pv.center, pv.zoom);
  await loadPois();
}

async function loadPois() {
  try {
    setApiStatus('loading', 'connecting...');
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 5000);
    const res = await fetch(`${API_BASE}/api/pois?province=${encodeURIComponent(getProvince())}`, { signal: ctrl.signal });
    clearTimeout(timer);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    STATE.pois = data.pois;
    STATE.hotels = data.hotels;
    [...data.pois, ...data.hotels].forEach(p => STATE.poisById[p.id] = p);
    setApiStatus('ok', `${data.pois.length} สถานที่ · ${data.hotels.length} โรงแรม`);
  } catch (e) {
    setApiStatus('error', 'backend offline');
    showToast(`โหลดข้อมูลไม่สำเร็จ — ตรวจสอบว่า backend รันที่ ${API_BASE}`, 'error', 6000);
  }
}

// ============================================================
// แจ้งเตือน Toast
// ============================================================
function showToast(msg, kind = 'ok', duration = 3500) {
  const container = document.getElementById('toastContainer');
  const el = document.createElement('div');
  el.className = `toast ${kind}`;
  const iconMap = {ok: ICON.check, error: ICON.alert, loading: ICON.spin};
  el.innerHTML = `<span class="toast-icon">${iconMap[kind] || ICON.check}</span><span>${msg}</span>`;
  container.appendChild(el);
  setTimeout(() => {
    el.style.opacity = '0';
    el.style.transform = 'translateX(20px)';
    el.style.transition = 'all 200ms';
    setTimeout(() => el.remove(), 220);
  }, duration);
  return el;
}

// ============================================================
// ค้นหาแพ็กเกจ
// ============================================================
// กฎ validation ฝั่ง client (ต้องตรงกับ Pydantic schema ของ backend)
const VALIDATION = {
  budget: { min: 1000,  max: 100000, label: 'งบประมาณ' },
  days:   { min: 1,     max: 7,      label: 'จำนวนวัน' },
  travelers: { min: 1,  max: 10,     label: 'จำนวนคน' },
};

function validateInputs(budget, days, travelers) {
  const errors = [];
  if (!Number.isFinite(budget) || budget < VALIDATION.budget.min) {
    errors.push(`${VALIDATION.budget.label}ต้องอย่างน้อย ${fmt(VALIDATION.budget.min)} บาท (ใส่ไว้ ${fmt(budget || 0)} บาท)`);
  }
  if (budget > VALIDATION.budget.max) {
    errors.push(`${VALIDATION.budget.label}สูงสุด ${fmt(VALIDATION.budget.max)} บาท`);
  }
  if (days < VALIDATION.days.min || days > VALIDATION.days.max) {
    errors.push(`${VALIDATION.days.label}ต้องอยู่ระหว่าง ${VALIDATION.days.min}-${VALIDATION.days.max} วัน (ตอนนี้ ${days})`);
  }
  if (travelers < VALIDATION.travelers.min || travelers > VALIDATION.travelers.max) {
    errors.push(`${VALIDATION.travelers.label}ต้อง ${VALIDATION.travelers.min}-${VALIDATION.travelers.max} คน`);
  }
  return errors;
}

function highlightField(id, hasError) {
  const wrapper = document.getElementById(id)?.closest('.input-with-unit, .date-range-input, .counter-control, .select-input');
  if (wrapper) wrapper.classList.toggle('has-error', hasError);
  const input = document.getElementById(id);
  if (input) input.classList.toggle('has-error', hasError);
}

async function searchPackages() {
  const budget = +document.getElementById('budget').value;
  const days = getSelectedDays();
  const travelers = +document.getElementById('travelers').value;
  // One Day Trip → บังคับไม่รวมโรงแรม
  const includeHotel = days === 1 ? false : (document.getElementById('includeHotel')?.checked !== false);

  // === Client-side validation FIRST ===
  const errors = validateInputs(budget, days, travelers);
  highlightField('budget', errors.some(e => e.includes('งบประมาณ')));
  highlightField('dateRange', errors.some(e => e.includes('จำนวนวัน')));
  if (errors.length > 0) {
    showToast(errors[0], 'error', 5000);
    return;
  }

  // === Clear previous results ===
  if (STATE.map) {
    STATE.mapMarkers.forEach(m => STATE.map.removeLayer(m));
    STATE.mapPolylines.forEach(p => STATE.map.removeLayer(p));
    if (STATE.hotelMarker) STATE.map.removeLayer(STATE.hotelMarker);
    STATE.mapMarkers = [];
    STATE.mapPolylines = [];
    STATE.mapDayLayers = {};
    STATE.hotelMarker = null;
  }
  STATE.packages = [];
  STATE.selectedPkg = null;
  STATE.selectedIdx = null;
  document.getElementById('detailPanel').style.display = 'none';
  document.getElementById('dayToggles').innerHTML = '';
  document.getElementById('dayPanels').innerHTML = '';

  const btn = document.getElementById('searchBtn');
  btn.classList.add('loading');
  btn.disabled = true;

  const sec = document.getElementById('packagesSection');
  sec.style.display = 'block';
  document.getElementById('metaSummary').textContent = STATE.dev ? `กำลังคำนวณด้วย ${ALGO_NAMES[SELECTED_ALGO]}...` : 'กำลังวางแผนทริป...';
  const grid = document.getElementById('packagesRow');
  grid.innerHTML = '';
  const skTpl = document.getElementById('skeletonTemplate');
  for (let i = 0; i < 3; i++) grid.appendChild(skTpl.content.cloneNode(true));
  sec.scrollIntoView({behavior: 'smooth', block: 'start'});

  const loadingToast = showToast(STATE.dev ? `กำลังเรียก ${ALGO_NAMES[SELECTED_ALGO]} 3 รอบ...` : 'กำลังวางแผนทริป 3 แบบ...', 'loading', 30000);

  try {
    const res = await fetch(`${API_BASE}/api/packages`, {
      method: 'POST',
      headers: devHeaders(),
      body: JSON.stringify({province: getProvince(), preferences: getPreferences(), budget, days, travelers, seed: Math.floor(Math.random() * 100000), algorithm: STATE.dev ? SELECTED_ALGO : 'hybrid', include_hotel: includeHotel}),
    });
    if (!res.ok) {
      // Parse FastAPI/Pydantic 422 detail
      let detail = `HTTP ${res.status}`;
      try {
        const errData = await res.json();
        if (errData.detail && Array.isArray(errData.detail)) {
          detail = errData.detail.map(d => {
            const field = d.loc ? d.loc[d.loc.length - 1] : '?';
            return `${field}: ${d.msg}`;
          }).join(' · ');
        } else if (errData.detail) {
          detail = errData.detail;
        }
      } catch {}
      throw new Error(detail);
    }
    const data = await res.json();
    STATE.packages = data.packages;
    STATE.includeHotel = includeHotel;
    (data.packages[0]?.notes || []).forEach(n => showToast(n, 'error', 7000));   // เช่น ร้านอาหารตามความชอบมีไม่พอ
    renderPackages();
    const totalRuntime = data.packages.reduce((s, p) => s + p.runtime_ms, 0);
    document.getElementById('metaSummary').textContent =
      `งบ ${fmt(budget)} ฿ · ${days} วัน · ${travelers} คน` + (STATE.dev ? ` · ${ALGO_NAMES[SELECTED_ALGO]} · ${(totalRuntime/1000).toFixed(1)} วินาที` : '');
    loadingToast.remove();
    showToast(`สร้าง ${data.packages.length} แพ็กเกจสำเร็จ`, 'ok');
  } catch (e) {
    loadingToast.remove();
    showToast(`ผิดพลาด: ${e.message}`, 'error', 6000);
    grid.innerHTML = '';
    document.getElementById('metaSummary').textContent = '';
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
  }
}

// ============================================================
// แสดงการ์ดแพ็กเกจ
// ============================================================
function renderPackages() {
  const grid = document.getElementById('packagesRow');
  grid.innerHTML = '';

  const showHotel = STATE.includeHotel !== false;

  STATE.packages.forEach((pkg, idx) => {
    const card = document.createElement('div');
    card.className = `package-card ${pkg.valid ? '' : 'invalid'}`;
    card.onclick = () => pkg.valid && selectPackage(idx);
    const totalPois = pkg.days.reduce((s, d) => s + d.pois.length, 0);
    card.innerHTML = `
      <div class="tier-row">
        <span class="tier-badge tier-${pkg.tier}">${pkg.tier}</span>
        <span class="runtime">${pkg.runtime_ms.toFixed(0)} ms</span>
      </div>
      ${showHotel
        ? `<div class="hotel-name">${CAT_ICON.hotel} ${pkg.hotel.name_en}</div>`
        : `<div class="hotel-name no-hotel">${ic('hotel-off')} ไม่รวมที่พัก</div>`}
      ${pkg.valid ? `
        <div class="score-display">
          <span class="score-num">${pkg.total_score}</span>
          <span class="score-label"><span class="dev-txt">รวมคะแนน · </span>${totalPois} จุดท่องเที่ยว</span>
        </div>
        ${showHotel ? `<div class="stat-row"><span class="label">ค่าโรงแรม</span><span class="val">${fmt(pkg.total_hotel_cost)} ฿</span></div>` : ''}
        <div class="stat-row"><span class="label">ค่ากิจกรรม</span><span class="val">${fmt(pkg.total_activity_cost)} ฿</span></div>
        <div class="stat-row total"><span class="label">รวมทั้งหมด</span><span class="val">${fmt(pkg.total_cost)} ฿</span></div>
      ` : `
        <div class="invalid-msg">${pkg.violations[0] || 'งบไม่พอสำหรับแพ็กเกจนี้'}</div>
      `}
    `;
    grid.appendChild(card);
  });
}

// ============================================================
// เลือกแพ็กเกจ
// ============================================================
function selectPackage(idx) {
  STATE.selectedPkg = JSON.parse(JSON.stringify(STATE.packages[idx]));
  STATE.locked.clear(); STATE.excluded.clear();
  STATE.selectedIdx = idx;
  document.querySelectorAll('.package-card').forEach((c, i) =>
    c.classList.toggle('selected', i === idx)
  );
  document.getElementById('detailPanel').style.display = 'block';
  renderDetail(STATE.selectedPkg);
  // CRITICAL: must invalidate size after detail panel becomes visible,
  // otherwise map container has 0px and fitBounds fails
  setTimeout(() => {
    STATE.map.invalidateSize();
    drawOnMap(STATE.selectedPkg);
    document.getElementById('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
    setTimeout(syncMapHeight, 150);
  }, 120);
}

// ============================================================
// วาดแผนที่
// ============================================================
function drawOnMap(pkg) {
  // Clear all old layers
  STATE.mapMarkers.forEach(m => STATE.map.removeLayer(m));
  STATE.mapPolylines.forEach(p => STATE.map.removeLayer(p));
  if (STATE.hotelMarker) STATE.map.removeLayer(STATE.hotelMarker);
  STATE.mapMarkers = [];
  STATE.mapPolylines = [];
  STATE.mapDayLayers = {};

  const showHotel = STATE.includeHotel !== false;

  // Hotel marker — แสดงเฉพาะเมื่อรวมโรงแรม
  if (showHotel) {
    const hotelIcon = L.divIcon({
      html: `<div class="map-hotel-marker">${ic('hotel')}</div>`,
      className: '',
      iconSize: [40, 40], iconAnchor: [20, 20],
    });
    STATE.hotelMarker = L.marker([pkg.hotel.lat, pkg.hotel.lng], {icon: hotelIcon})
      .bindPopup(`<b>${pkg.hotel.name_en}</b><br><small>${pkg.hotel.cost} ฿/คืน</small>`)
      .addTo(STATE.map);
  } else {
    STATE.hotelMarker = null;
  }

  // allLatLngs: รวม hotel ไว้ใน bounds เฉพาะเมื่อรวมโรงแรม
  const allLatLngs = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];

  pkg.days.forEach((day, dIdx) => {
    const color = DAY_COLORS[dIdx % DAY_COLORS.length];
    // path: เริ่ม/จบที่โรงแรมเฉพาะเมื่อรวมโรงแรม
    const path = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];
    const dayMarkers = [];

    day.pois.forEach((poi, pIdx) => {
      const icon = L.divIcon({
        html: `<div class="map-poi-marker" style="--c:${color};">
                 <span class="d">${dIdx + 1}</span>
                 <span class="p">${pIdx + 1}</span>
               </div>`,
        className: '',
        iconSize: [36, 36], iconAnchor: [18, 18],
      });
      const m = L.marker([poi.lat, poi.lng], {icon}).bindPopup(
        `<b>${poi.name_th}</b><br>
         <small>${poi.name_en}</small><br>
         <span style="opacity:0.7;">วันที่ ${dIdx + 1} · ลำดับ ${pIdx + 1}</span><br>
         ${STATE.dev ? poi.score + ' คะแนน · ' : ''}${poi.cost} ฿ · ${poi.duration_min} นาที<br>
         <a href="#" onclick="showPoiDetail('${poi.id}', ${arriveOf(day, poi)}); return false;">ดูรายละเอียดและรีวิว</a>`
      ).addTo(STATE.map);
      dayMarkers.push(m);
      STATE.mapMarkers.push(m);
      path.push([poi.lat, poi.lng]);
      allLatLngs.push([poi.lat, poi.lng]);
    });

    if (showHotel) path.push([pkg.hotel.lat, pkg.hotel.lng]);
    const line = L.polyline(path, {
      color, weight: 3, opacity: 0.8, dashArray: '6, 8',
    }).bindTooltip(`Day ${dIdx + 1}`).addTo(STATE.map);
    STATE.mapPolylines.push(line);

    // Save layers for this day
    STATE.mapDayLayers[dIdx] = {
      markers: dayMarkers,
      polyline: line,
      visible: true,
      color,
    };
  });

  // Default: show only day 1, hide the rest
  pkg.days.forEach((_, dIdx) => {
    if (dIdx === 0) return;
    const layer = STATE.mapDayLayers[dIdx];
    if (!layer) return;
    layer.markers.forEach(m => STATE.map.removeLayer(m));
    STATE.map.removeLayer(layer.polyline);
    layer.visible = false;
  });

  renderDayToggles(pkg);

  // fitBounds to day 1 only
  const day0Latlngs = showHotel ? [[pkg.hotel.lat, pkg.hotel.lng]] : [];
  pkg.days[0].pois.forEach(p => day0Latlngs.push([p.lat, p.lng]));
  if (day0Latlngs.length > 1) {
    STATE.map.fitBounds(L.latLngBounds(day0Latlngs).pad(0.15));
  }
}

// ============================================================
// สลับแสดง/ซ่อนแต่ละวัน
// ============================================================
function renderDayToggles(pkg) {
  const root = document.getElementById('dayToggles');
  if (!root) return;

  let html = `<button class="day-toggle show-all" onclick="toggleAllDays(true)" title="แสดงทุกวัน">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <span>แสดงทุกวัน</span>
              </button>`;
  html += `<button class="day-toggle hide-all" onclick="toggleAllDays(false)" title="ซ่อนทุกวัน">
             <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
             <span>ซ่อนทุกวัน</span>
           </button>`;
  html += `<button class="day-toggle reset-view" onclick="resetMapView()" title="รีเซ็ตตำแหน่ง">
             <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
             <span>รีเซ็ต</span>
           </button>`;
  html += pkg.days.map((day, dIdx) => {
    const color = DAY_COLORS[dIdx % DAY_COLORS.length];
    const visible = STATE.mapDayLayers[dIdx] ? STATE.mapDayLayers[dIdx].visible : true;
    return `<button class="day-toggle ${visible ? 'active' : ''}"
                    style="--c:${color};"
                    onclick="toggleDay(${dIdx})">
              <span class="day-dot"></span>
              <span>วัน ${dIdx + 1} (${day.pois.length})</span>
            </button>`;
  }).join('');
  root.innerHTML = html;
}

function toggleDay(dIdx) {
  const layer = STATE.mapDayLayers[dIdx];
  if (!layer) return;
  layer.visible = !layer.visible;
  if (layer.visible) {
    layer.markers.forEach(m => m.addTo(STATE.map));
    layer.polyline.addTo(STATE.map);
  } else {
    layer.markers.forEach(m => STATE.map.removeLayer(m));
    STATE.map.removeLayer(layer.polyline);
  }
  renderDayToggles(STATE.selectedPkg);
}

function resetMapView() {
  const latlngs = [];
  Object.values(STATE.mapDayLayers).forEach(layer => {
    if (!layer.visible) return;
    layer.markers.forEach(m => latlngs.push(m.getLatLng()));
  });
  if (STATE.hotelMarker) latlngs.push(STATE.hotelMarker.getLatLng());
  if (latlngs.length > 1) {
    STATE.map.fitBounds(L.latLngBounds(latlngs).pad(0.15));
  }
}

function toggleAllDays(showAll) {
  Object.keys(STATE.mapDayLayers).forEach(k => {
    const layer = STATE.mapDayLayers[k];
    if (showAll && !layer.visible) {
      layer.markers.forEach(m => m.addTo(STATE.map));
      layer.polyline.addTo(STATE.map);
      layer.visible = true;
    } else if (!showAll && layer.visible) {
      layer.markers.forEach(m => STATE.map.removeLayer(m));
      STATE.map.removeLayer(layer.polyline);
      layer.visible = false;
    }
  });
  renderDayToggles(STATE.selectedPkg);
}

// ============================================================
// หน้าต่างรายละเอียดแพ็กเกจ
// ============================================================
// ให้ส่วนรายละเอียดแผนสูงเท่าหน้าจอพอดี: เลื่อนสุดล่างแล้วเห็นหัวข้อ STEP 3 ชิดบน และมีที่ว่างเล็กน้อยด้านล่าง (จอกว้างเท่านั้น)
function fitDetail() {
  const sec = document.querySelector('.detail-section'), dayList = document.querySelector('.day-list'), grid = document.querySelector('.detail-grid');
  if (!sec || !dayList || !grid || sec.offsetParent === null) return;
  if (window.innerWidth <= 1000) { sec.style.minHeight = ''; dayList.style.maxHeight = ''; return; }
  const GAP = 36;   // ที่ว่างใต้กรอบ ไม่ให้ติดขอบล่างของเบราว์เซอร์
  const top = grid.getBoundingClientRect().top - sec.getBoundingClientRect().top;
  sec.style.minHeight = window.innerHeight + 'px';
  dayList.style.maxHeight = Math.max(360, window.innerHeight - top - GAP) + 'px';
  // ย่อการ์ดเท่าที่จำเป็น (ไม่ขยายเกินขนาดปกติ) ให้เห็นครบทุกจุดของวันที่ยาวที่สุดรวมปุ่มเพิ่มสถานที่โดยไม่ต้องเลื่อน
  // ลำดับ: บีบระยะห่าง --sp (1→0) ก่อน ถ้ายังไม่พอจึงลดตัวอักษร --fs (1→0.8)
  dayList.classList.add('fit');
  const need = () => Math.max(...[...dayList.querySelectorAll('.day-panel')].map(p => p.offsetHeight), 0);
  const room = dayList.clientHeight, setD = (sp, fs) => { dayList.style.setProperty('--sp', sp); dayList.style.setProperty('--fs', fs); };
  const MAXSP = 1.25;   // ที่ว่างที่เหลือ (เช่น จากกล่องฝนที่เล็กลง) ให้การ์ดขยายได้ถึง 1.25 เท่า ตัวอักษรโตสูงสุด 3%
  const tryD = (sp, fs = sp > 1 ? 1 + 0.03 * (sp - 1) / (MAXSP - 1) : 1) => { setD(sp.toFixed(3), fs.toFixed(3)); return need() <= room; };
  if (!tryD(MAXSP)) {
    if (tryD(0)) { let lo = 0, hi = MAXSP; for (let i = 0; i < 8; i++) { const m = (lo + hi) / 2; if (tryD(m)) lo = m; else hi = m; } tryD(lo); }
    else { let fs = 1; while (fs > 0.8 && need() > room) { fs -= 0.03; setD(0, fs.toFixed(3)); } }
  }
}
window.addEventListener('resize', () => { fitDetail(); syncMapHeight(); });

function syncMapHeight() {
  fitDetail();
  const dayList = document.querySelector('.day-list');
  const mapEl   = document.getElementById('map');
  if (!dayList || !mapEl) return;
  const listBottom = dayList.getBoundingClientRect().bottom;
  const mapTop     = mapEl.getBoundingClientRect().top;
  const mapH       = Math.max(listBottom - mapTop, 200);
  mapEl.style.height = mapH + 'px';
}

// ============================================================
function renderDetail(pkg) {
  const showHotel = STATE.includeHotel !== false;
  document.getElementById('detailTitle').textContent = showHotel
    ? `${pkg.tier} — ${pkg.hotel.name_en}`
    : `${pkg.tier} — ไม่รวมที่พัก`;

  // KPIs
  const totalPois = pkg.days.reduce((s, d) => s + d.pois.length, 0);
  document.querySelector('#kpiScore .kpi-val').textContent = pkg.total_score;
  document.querySelector('#kpiCost .kpi-val').textContent = `${fmt(pkg.total_activity_cost)} ฿`;
  document.querySelector('#kpiPois .kpi-val').textContent = totalPois;

  const root = document.getElementById('dayPanels');
  root.innerHTML = '';

  pkg.days.forEach((day, dIdx) => {
    const color = DAY_COLORS[dIdx % DAY_COLORS.length];
    const panel = document.createElement('div');
    panel.className = 'day-panel';
    panel.innerHTML = `
      <div class="day-head">
        <div class="day-title">
          <div class="day-color" style="background:${color};box-shadow:0 0 8px ${color};"></div>
          <h3>วันที่ ${dIdx + 1}</h3>
        </div>
        <div class="day-stats">
          <span class="day-score">${ICON.star} ${day.score}</span>
          <span>${ICON.coin} ${fmt(day.cost)}</span>
          <span>${ICON.clock} ${fmtDur(day.time_min)}</span>
          <span>${ICON.route} ${day.distance_km.toFixed(1)}km</span>
        </div>
      </div>
      <ul class="poi-list" id="day-${dIdx}-list"></ul>
      <button class="day-add" onclick="addPoiToDay(${dIdx})">
        <div class="add-num">${ICON.plus}</div>
        <span>เพิ่มสถานที่</span>
      </button>
    `;
    root.appendChild(panel);

    const list = panel.querySelector('.poi-list');
    if (!day.pois.length) {
      list.innerHTML = '<li style="text-align:center;color:var(--text-muted);padding:1rem 0;font-size:0.85rem;">ยังไม่มีจุดในวันนี้</li>';
    }
    day.pois.forEach((poi, pIdx) => {
      // Distance connector before this POI
      if (pIdx === 0 && showHotel) {
        const distKm = haversineKm(pkg.hotel.lat, pkg.hotel.lng, poi.lat, poi.lng);
        const distEl = document.createElement('li');
        distEl.className = 'dist-connector';
        distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('hotel')} ${ic('arrow-right')} ${distKm.toFixed(1)} km</span><span class="dist-line"></span>`;
        list.appendChild(distEl);
      } else if (pIdx > 0) {
        const prev = day.pois[pIdx - 1];
        const distKm = haversineKm(prev.lat, prev.lng, poi.lat, poi.lng);
        const distEl = document.createElement('li');
        distEl.className = 'dist-connector';
        distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('arrow-down')} ${distKm.toFixed(1)} km</span><span class="dist-line"></span>`;
        list.appendChild(distEl);
      }

      const li = document.createElement('li');
      li.className = 'poi-item';
      li.dataset.id = poi.id;
      li.innerHTML = `
        <div class="poi-num">${pIdx + 1}</div>
        <div class="poi-info">
          <div class="poi-name poi-link" onclick="showPoiDetail('${poi.id}', ${arriveOf(day, poi)})" title="ดูรายละเอียดและรีวิว">${CAT_ICON[poi.category] || ''} ${poi.name_th}</div>
          <div class="poi-meta">
            <span class="pill">${CAT_LABELS[poi.category] || poi.category}</span>
            ${arriveOf(day, poi) >= 0 ? `<span class="time-chip"><span class="tc-lbl">ตั้งแต่</span> ${fmtClock(arriveOf(day, poi))}–${fmtClock(arriveOf(day, poi) + (poi.duration_min || 0))} · เปิด ${hoursText(poi)}</span>` : ''}
            <span class="score-chip">${ic('star')} ${poi.score}</span>
            <span>${poi.cost} ฿</span>
            <span class="dur"><span class="dur-lbl">ใช้เวลา</span> ${fmtDur(poi.duration_min)}</span>
          </div>
        </div>
        <div class="poi-actions">
          <a class="btn-loc" href="${gmapsUrl(poi)}" target="_blank" rel="noopener" title="ดูใน Google Maps">${ICON.pin}</a>
          <button class="btn-swap" onclick="openSwapModal(${dIdx}, ${pIdx})" title="เปลี่ยน">${ICON.swap}</button>
          <button class="btn-remove" onclick="removePoi(${dIdx}, ${pIdx})" title="ลบ">${ICON.trash}</button>
        </div>
      `;
      list.appendChild(li);

      // Return connector after last POI
      if (pIdx === day.pois.length - 1 && showHotel) {
        const distKm = haversineKm(poi.lat, poi.lng, pkg.hotel.lat, pkg.hotel.lng);
        const distEl = document.createElement('li');
        distEl.className = 'dist-connector';
        distEl.innerHTML = `<span class="dist-line"></span><span class="dist-badge">${ic('arrow-down')} ${distKm.toFixed(1)} km ${ic('arrow-right')} ${ic('hotel')}</span><span class="dist-line"></span>`;
        list.appendChild(distEl);
      }
    });
  });
}

// ============================================================
// Modal เปลี่ยน / เพิ่ม POI
// ============================================================
function openSwapModal(dayIdx, poiIdx) {
  const currentPoi = STATE.selectedPkg.days[dayIdx].pois[poiIdx];
  STATE.swapContext = {dayIdx, poiIdx, currentPoi, mode: 'swap', categoryFilter: 'all'};
  document.getElementById('swapTitle').textContent = 'เปลี่ยนสถานที่';
  document.getElementById('swapCurrentInfo').innerHTML =
    `ปัจจุบัน: ${CAT_ICON[currentPoi.category] || ''} ${currentPoi.name_th}`;
  document.getElementById('swapFilter').value = '';
  renderSwapList();
  document.getElementById('swapModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function addPoiToDay(dayIdx) {
  STATE.swapContext = {dayIdx, poiIdx: null, currentPoi: null, mode: 'add', categoryFilter: 'all'};
  document.getElementById('swapTitle').textContent = 'เพิ่มจุดใหม่';
  document.getElementById('swapCurrentInfo').textContent = `เพิ่มในวันที่ ${dayIdx + 1}`;
  document.getElementById('swapFilter').value = '';
  renderSwapList();
  document.getElementById('swapModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function setCategoryFilter(cat) {
  STATE.swapContext.categoryFilter = cat;
  renderSwapList();
}

// วันที่ฝนมีโอกาสตก (>=60%): ติดไอคอนฝนท้ายชื่อสถานที่กลางแจ้ง (ไม่ติด = สถานที่ในร่ม)
function swapRainIcon(p) {
  const ctx = STATE.swapContext;
  if (!ctx || !window.dayRainPop || window.dayRainPop(ctx.dayIdx) < 60 || !(window.OUTDOOR_CATS || []).includes(p.category)) return '';
  const tip = window.WET_LANG === 'en' ? 'Outdoor place, it may rain' : 'สถานที่กลางแจ้ง อาจมีฝนตกได้';
  return `<span class="rain-ic" title="${tip}"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 14a4 4 0 0 0 0-8 5.5 5.5 0 0 0-10.6 1.5A3.5 3.5 0 0 0 7 14"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/></svg></span>`;
}

// ลิงก์ Google Maps ค้นหาด้วยชื่อสถานที่ + ชื่อจังหวัด เพื่อให้ปักหมุดที่สถานที่จริงของ Google (ไม่ใช่พิกัดจากข้อมูล OSM ที่อาจเลื่อน)
// ทริปข้ามจังหวัดใช้จังหวัดที่ใกล้จุดนั้นที่สุด; ถ้าไม่มีชื่อไทยใช้ชื่ออังกฤษ
function gmapsUrl(p) {
  const provs = getProvince().split('+').map(s => STATE.provinces[s]).filter(Boolean);
  const near = provs.slice().sort((a, b) => haversineKm(p.lat, p.lng, ...(a.center || [p.lat, p.lng])) - haversineKm(p.lat, p.lng, ...(b.center || [p.lat, p.lng])))[0];
  const q = [p.name_th || p.name_en, near?.name_th].filter(Boolean).join(' ');
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`;
}

function renderSwapList() {
  const ctx = STATE.swapContext;
  const usedIds = new Set();
  STATE.selectedPkg.days.forEach(d => d.pois.forEach(p => usedIds.add(p.id)));
  const all = STATE.pois.filter(p => !usedIds.has(p.id));

  const counts = {all: all.length};
  all.forEach(p => { counts[p.category] = (counts[p.category] || 0) + 1; });

  const filterCat = ctx.categoryFilter || 'all';
  const candidates = (filterCat === 'all' ? all : all.filter(p => p.category === filterCat))
    .sort((a, b) => b.score - a.score);

  const cats = ['all', 'beach', 'temple', 'viewpoint', 'culture', 'market', 'activity', 'restaurant'];
  const filterButtons = cats
    .filter(c => counts[c])
        .map(c => `<button class="cat-btn ${c === filterCat ? 'active' : ''}" onclick="setCategoryFilter('${c}')">
                 ${c === 'all' ? '' : CAT_ICON[c] + ' '}${CAT_LABELS[c]} <span style="opacity:0.7">${counts[c]}</span>
               </button>`).join('');

  const list = document.getElementById('swapList');
  list.innerHTML = `
    <div class="cat-filter">${filterButtons}</div>
    ${candidates.length === 0
      ? '<div class="empty-msg">ไม่มีจุดที่ตรงเงื่อนไข</div>'
      : candidates.map(p => `
        <div class="swap-option" onclick="confirmSwap('${p.id}')">
          <div class="opt-info">
            <b>${CAT_ICON[p.category] || ''} ${p.name_th}${swapRainIcon(p)}</b>
            <span class="meta">${CAT_LABELS[p.category]} · ${p.cost} ฿ · ${p.duration_min} นาที</span>
            <span class="meta">เปิด-ปิด ${hoursText(p)}</span>
          </div>
          <div class="opt-actions">
            <button type="button" class="opt-btn" title="ดูรีวิว" onclick="event.stopPropagation(); showPoiDetail('${p.id}', -1)"><svg class="ic" viewBox="0 0 24 24"><use href="#i-star"/></svg></button>
            <a class="opt-btn" title="ดูใน Google Maps" target="_blank" rel="noopener" href="${gmapsUrl(p)}" onclick="event.stopPropagation()"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></a>
          </div>
        </div>
      `).join('')
    }
  `;
}

function filterSwapList() {
  const q = document.getElementById('swapFilter').value.toLowerCase();
  document.querySelectorAll('.swap-option').forEach(el => {
    el.style.display = el.textContent.toLowerCase().includes(q) ? 'flex' : 'none';
  });
}

// การเพิ่ม/สลับ/ลบสถานที่ของผู้ใช้ทำตามที่ผู้ใช้สั่งตรงๆ แล้วคำนวณเวลาและค่าใช้จ่ายใหม่ (recompute) ไม่ให้ Hybrid ถอดสถานที่อื่นออกเอง
// (เดิมเรียก Hybrid ทุกครั้ง: เพิ่มกิจกรรม 8 ชั่วโมงแล้วสถานที่อื่นหายหมดเพราะเต็มเพดานเวลาท่องเที่ยว) — ถ้าอยากให้ระบบช่วยจัดลงตัว กดปุ่ม "ช่วยจัดให้ลงตัว"
function snapshotEdit() { return {days: STATE.selectedPkg.days.map(d => d.pois.slice()), locked: new Set(STATE.locked), excluded: new Set(STATE.excluded)}; }
function restoreEdit(sn) { STATE.selectedPkg.days.forEach((d, i) => { d.pois = sn.days[i].slice(); }); STATE.locked = sn.locked; STATE.excluded = sn.excluded; }

async function confirmSwap(newPoiId) {
  const ctx = STATE.swapContext;
  const newPoi = STATE.poisById[newPoiId];
  const sn = snapshotEdit();
  if (ctx.mode === 'swap') {
    STATE.selectedPkg.days[ctx.dayIdx].pois[ctx.poiIdx] = newPoi;
  } else {
    STATE.selectedPkg.days[ctx.dayIdx].pois.push(newPoi);
  }
  STATE.locked.add(newPoiId);
  STATE.excluded.delete(newPoiId);
  closeSwapModal();
  await recomputeAndRefresh(() => restoreEdit(sn));
}

function removePoi(dayIdx, poiIdx) {
  const sn = snapshotEdit();
  const [removed] = STATE.selectedPkg.days[dayIdx].pois.splice(poiIdx, 1);
  STATE.locked.delete(removed.id);
  STATE.excluded.add(removed.id);
  recomputeAndRefresh(() => restoreEdit(sn));
}

function closeSwapModal() {
  document.getElementById('swapModal').classList.remove('open');
  document.body.style.overflow = '';
  STATE.swapContext = null;
}

// ============================================================
// สุ่มแพ็กเกจใหม่ (Shuffle)
// ============================================================
async function reshufflePackage() {
  if (!STATE.selectedPkg) return;
  const targetTier = STATE.selectedPkg.tier;

  const budget    = +document.getElementById('budget').value;
  const days      = getSelectedDays();
  const travelers = +document.getElementById('travelers').value;
  const includeHotel = days === 1 ? false : (document.getElementById('includeHotel')?.checked !== false);

  const detailEl = document.getElementById('detailPanel');
  // Inject animated overlay
  const overlay = document.createElement('div');
  overlay.id = 'reshuffleOverlay';
  overlay.innerHTML = `<div class="reshuffle-overlay-inner">
    <svg class="reshuffle-ring" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="25" cy="25" r="20" stroke="rgba(34,211,238,0.25)" stroke-width="3"/>
      <circle cx="25" cy="25" r="20" stroke="#22d3ee" stroke-width="3" stroke-dasharray="40 90" stroke-linecap="round"/>
    </svg>
    <span>กำลังสุ่มสถานที่ใหม่...</span>
  </div>`;
  detailEl.appendChild(overlay);
  detailEl.classList.add('reshuffling');
  const t = showToast('กำลังสุ่มสถานที่ใหม่...', 'loading', 30000);

  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 25000);
    const res = await fetch(`${API_BASE}/api/packages`, {
      method: 'POST',
      headers: devHeaders(),
      body: JSON.stringify({
        province: getProvince(),
        preferences: getPreferences(),
        budget, days, travelers,
        seed: Math.floor(Math.random() * 1000000),
        algorithm: STATE.dev ? SELECTED_ALGO : 'hybrid',
        include_hotel: includeHotel,
      }),
      signal: ctrl.signal,
    });
    clearTimeout(timer);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    // Update global package list
    STATE.packages = data.packages;
    STATE.includeHotel = includeHotel;

    // Find the matching tier (or fall back to same index)
    const tierIdx = data.packages.findIndex(p => p.tier === targetTier);
    const newIdx  = tierIdx >= 0 ? tierIdx : STATE.selectedIdx;
    STATE.selectedIdx = newIdx;
    STATE.selectedPkg = JSON.parse(JSON.stringify(data.packages[newIdx]));
    STATE.locked.clear(); STATE.excluded.clear();
    setTimeout(pushSession, 600);

    // Refresh package cards without clearing detail section
    renderPackages();
    document.querySelectorAll('.package-card').forEach((c, i) =>
      c.classList.toggle('selected', i === newIdx)
    );

    // Update detail in-place
    renderDetail(STATE.selectedPkg);
    setTimeout(() => {
      STATE.map.invalidateSize();
      drawOnMap(STATE.selectedPkg);
      setTimeout(syncMapHeight, 100);
    }, 80);

    t.remove();
    showToast(STATE.dev ? `สุ่มใหม่แล้ว! Score ${STATE.selectedPkg.total_score}` : 'สุ่มใหม่แล้ว!', 'ok');
  } catch (e) {
    t.remove();
    showToast(`ผิดพลาด: ${e.message}`, 'error');
  } finally {
    detailEl.classList.remove('reshuffling');
    document.getElementById('reshuffleOverlay')?.remove();
  }
}

// หลังผู้ใช้แก้แผน: ให้ backend รัน Hybrid ปรับทั้งแพ็กเกจใหม่ (คงจุดที่เลือก/ไม่ใส่จุดที่ลบ)
// ถ้า endpoint ใช้ไม่ได้ ถอยไปใช้ recompute เดิม (คำนวณค่าใช้จ่ายอย่างเดียว)
async function reoptimizeAndRefresh() {
  const t = showToast('กำลังปรับเส้นทางด้วย Hybrid...', 'loading', 15000);
  try {
    const pkg = STATE.selectedPkg;
    const res = await fetch(`${API_BASE}/api/reoptimize`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        province: getProvince(),
        preferences: getPreferences(),
        tier: pkg.tier,
        hotel_id: pkg.hotel.id,
        days: pkg.days.length,
        budget: +document.getElementById('budget').value,
        travelers: +document.getElementById('travelers').value,
        include_hotel: STATE.includeHotel !== false,
        routes: pkg.days.map(d => d.pois.map(p => p.id)),
        locked: [...STATE.locked],
        excluded: [...STATE.excluded],
        seed: Math.floor(Math.random() * 1000000),
      }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    STATE.selectedPkg = data;
    drawOnMap(data);
    renderDetail(data);
    t.remove();
    pushSession();
    (data.notes || []).forEach(n => showToast(n, 'error', 6000));
    showToast(uiWarnings(data).length ? `ปรับแล้ว · ${uiWarnings(data).length} คำเตือน` : (STATE.dev ? `ปรับแผนใหม่แล้ว! Score ${data.total_score}` : 'ปรับแผนใหม่แล้ว!'),
              uiWarnings(data).length ? 'error' : 'ok', 4000);
  } catch (e) {
    t.remove();
    await recomputeAndRefresh();
  }
}

async function recomputeAndRefresh(rollback) {
  const t = showToast('กำลังคำนวณเส้นทางใหม่...', 'loading', 10000);
  try {
    const routes = STATE.selectedPkg.days.map(d => d.pois.map(p => p.id));
    const res = await fetch(`${API_BASE}/api/recompute`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        province: getProvince(),
        hotel_id: STATE.selectedPkg.hotel.id,
        days: STATE.selectedPkg.days.length,
        budget: 100000,
        routes,
        travelers: +document.getElementById('travelers').value,
      }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    data._base = STATE.selectedPkg._base;   // คำเตือนตั้งต้นของแผนเดิม
    if (STATE.selectedPkg._orig) setHidden(data, '_orig', STATE.selectedPkg._orig);   // แผนตั้งต้นสำหรับปุ่มคืนค่าเดิม
    STATE.selectedPkg = data;
    drawOnMap(data);
    renderDetail(data);
    t.remove();
    if (uiWarnings(data).length) {
      showToast(`อัปเดตแล้ว · ${uiWarnings(data).length} คำเตือน (ดูการ์ดสีแดง)`, 'error', 5000);
    } else {
      showToast((STATE.dev ? `อัปเดต! Score ${data.total_score}` : 'อัปเดตแผนแล้ว'), 'ok');
    }
  } catch (e) {
    t.remove();
    if (rollback) { rollback(); drawOnMap(STATE.selectedPkg); renderDetail(STATE.selectedPkg); }   // คืนแผนเดิม ไม่ให้หมุด/การ์ดค้างผิดที่
    showToast(`ผิดพลาด: ${e.message}${rollback ? ' (คืนแผนเดิมแล้ว)' : ''}`, 'error');
  }
}

// ============================================================
// ฟังก์ชันเบ็ดเตล็ด
// ============================================================
function fmt(n) { return Math.round(n).toLocaleString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH')); }

function haversineKm(lat1, lng1, lat2, lng2) {
  const R = 6371, dLat = (lat2-lat1)*Math.PI/180, dLng = (lng2-lng1)*Math.PI/180;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLng/2)**2;
  // × road_factor ของจังหวัด (จาก /api/provinces) ให้ตรงกับระยะที่ backend ใช้คำนวณเวลาและค่าเดินทาง
  return R * 2 * Math.asin(Math.sqrt(a)) * (STATE.provinces[getProvince()]?.road_factor || 1);
}


document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeSwapModal();
});
