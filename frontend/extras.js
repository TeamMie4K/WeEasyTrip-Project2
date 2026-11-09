// ส่วนเสริมหน้าเว็บ: จำกัดวันตามข้อมูลจังหวัด, ทริปข้ามจังหวัดข้างเคียง, หมายเหตุฤดูกาล,
// บันทึก/เปิดแผน (localStorage), เปรียบเทียบอัลกอริทึม — โหลดต่อจาก app.js
(function () {
  const $ = id => document.getElementById(id);
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const store = {
    get() { try { return JSON.parse(localStorage.getItem('wet_saved') || '[]'); } catch (e) { return []; } },
    set(v) { try { localStorage.setItem('wet_saved', JSON.stringify(v)); return true; } catch (e) { return false; } },
  };
  let baseSlug = null;

  // ---------- จังหวัดข้างเคียง (ทริปข้ามจังหวัด) ----------
  const nameOf = s => STATE.provinces[s]?.name_th || s;
  function registerCombo(slug) {
    if (!slug.includes('+') || STATE.provinces[slug]) return;
    const ps = slug.split('+').map(s => STATE.provinces[s]);
    STATE.provinces[slug] = {
      ...ps[0], name_th: slug.split('+').map(nameOf).join(' + '),
      center: [0, 1].map(i => ps.reduce((a, p) => a + p.center[i], 0) / ps.length),
      zoom: Math.max(8, ps[0].zoom - 2), max_days: Math.min(7, ps.reduce((a, p) => a + p.max_days, 0)),
    };
  }

  function renderNeighbors() {
    let row = $('neighborRow');
    if (!row) { $('provSelect').insertAdjacentHTML('afterend', '<div id="neighborRow" class="neighbor-row"></div>'); row = $('neighborRow'); }
    const pv = STATE.provinces[baseSlug];
    if (!pv || !pv.neighbors?.length) { row.innerHTML = ''; return; }
    const cur = getProvince().split('+');
    row.innerHTML = '<span class="neighbor-label">เที่ยวต่อจังหวัดข้างเคียง:</span>' + pv.neighbors.map(n =>
      `<button type="button" class="neighbor-chip${cur.includes(n) ? ' on' : ''}" data-slug="${n}" aria-pressed="${cur.includes(n)}">${esc(nameOf(n))}</button>`).join('');
    row.querySelectorAll('button').forEach(b => b.onclick = () => {
      const on = b.classList.toggle('on');
      b.setAttribute('aria-pressed', String(on));
      const picked = [...row.querySelectorAll('button.on')].map(x => x.dataset.slug).slice(0, 2);   // รวมกันไม่เกิน 3 จังหวัด
      applyProvince([baseSlug, ...picked].join('+'));
    });
  }

  function applyProvince(slug) {
    registerCombo(slug);
    $('province').value = slug;
    $('provName').textContent = slug.split('+').map(nameOf).join(' + ');
    onProvinceChange(slug);
  }

  // แบนเนอร์ประจำจังหวัด: ใช้ img/provinces/<slug>.jpg (ภาพถ่ายถ้ามี) ไม่งั้นใช้ .svg ที่สร้างอัตโนมัติ; สลับด้วย cross-fade
  let bannerSlug = 'phuket';
  function setBanner(slug) {
    const base = slug.split('+')[0]; if (base === bannerSlug) return; bannerSlug = base;
    const hero = document.querySelector('.hero-visual'), old = hero?.querySelector('.hero-bg'); if (!hero || !old) return;
    const cands = base === 'phuket' ? ['BG2.jpg'] : [`img/provinces/${base}.jpg`, `img/provinces/${base}.svg`];
    const apply = url => {
      if (bannerSlug !== base) return;   // ผู้ใช้เปลี่ยนจังหวัดไปแล้ว
      const nu = document.createElement('div'); nu.className = 'hero-bg'; nu.style.backgroundImage = `url('${url}')`; nu.style.opacity = '0';
      old.after(nu); requestAnimationFrame(() => requestAnimationFrame(() => { nu.style.opacity = '1'; }));
      setTimeout(() => hero.querySelectorAll('.hero-bg').forEach(e => { if (e !== nu) e.remove(); }), 700);
    };
    (function tryNext(i) { if (i >= cands.length) return; const im = new Image(); im.onload = () => apply(cands[i]); im.onerror = () => tryNext(i + 1); im.src = cands[i]; })(0);
    const lbl = document.querySelector('.hero-label'); if (lbl) lbl.textContent = (STATE.provinces[base]?.name_en || 'Your Travel Services');
  }

  const origProvinceChange = onProvinceChange;
  onProvinceChange = async function (slug) {
    setBanner(slug);
    if (!slug.includes('+')) baseSlug = slug;
    else baseSlug = slug.split('+')[0];
    registerCombo(slug);
    await origProvinceChange(slug);
    renderNeighbors();
    updateHint();
  };

  const origLoadProvinces = loadProvinces;
  loadProvinces = async function () {
    await origLoadProvinces();
    baseSlug = getProvince().split('+')[0];
    renderNeighbors();
    updateHint();
  };

  // ---------- จำกัดจำนวนวันตามข้อมูล + หมายเหตุฤดูกาล ----------
  const maxDays = () => STATE.provinces[getProvince()]?.max_days || 7;

  const origValidate = validateInputs;
  validateInputs = function (budget, days, travelers) {
    const errs = origValidate(budget, days, travelers);
    if (days > maxDays()) errs.push(`ข้อมูลของ ${nameOf(getProvince())} รองรับสูงสุด ${maxDays()} วัน (สถานที่หรือร้านอาหารไม่พอสำหรับ ${days} วัน) ลองลดจำนวนวันหรือเพิ่มจังหวัดข้างเคียง`);
    return errs;
  };

  const ANDAMAN = ['phuket', 'krabi', 'phangnga', 'ranong', 'trang', 'satun'];
  const GULF_SOUTH = ['suratthani', 'samui', 'nakhonsithammarat', 'chumphon', 'songkhla', 'pattani', 'yala', 'narathiwat', 'phatthalung'];
  // ข้อมูลภูมิอากาศทั่วไปตามเดือน (คงที่ ไม่ใช่พยากรณ์อากาศ)
  function seasonNote(slug, month) {   // month 1-12
    const s = slug.split('+')[0], region = STATE.provinces[s]?.region || '';
    const notes = [];
    if (ANDAMAN.includes(s)) {
      if (month >= 5 && month <= 10) notes.push('ฝั่งอันดามันเป็นฤดูมรสุม คลื่นลมแรง ทริปเกาะและกิจกรรมทางทะเลอาจงดบางวัน');
      else notes.push('ช่วงนี้ทะเลฝั่งอันดามันสงบ เหมาะกับหาดและเกาะ (ฤดูท่องเที่ยวหลัก)');
    } else if (GULF_SOUTH.includes(s) && (month >= 10 || month <= 1)) {
      notes.push('ฝั่งอ่าวไทยตอนล่างฝนชุกช่วง ต.ค.–ม.ค. ควรเผื่อแผนสำรองในร่ม');
    } else if (region === 'ภาคเหนือ' && month >= 2 && month <= 4) {
      notes.push('ภาคเหนือช่วง ก.พ.–เม.ย. มักมีหมอกควันและฝุ่น PM2.5 จุดชมวิวอาจไม่ชัด');
    } else if (region === 'ภาคเหนือ' && (month >= 11 || month <= 1)) {
      notes.push('ภาคเหนือช่วงนี้อากาศเย็นสบาย เหมาะกับจุดชมวิวและกิจกรรมกลางแจ้ง (ฤดูท่องเที่ยวหลัก)');
    }
    if (month >= 3 && month <= 5) notes.push('ช่วง มี.ค.–พ.ค. อากาศร้อนจัด ควรเที่ยวกลางแจ้งช่วงเช้าหรือเย็น');
    else if (month >= 6 && month <= 10 && !ANDAMAN.includes(s)) notes.push('ช่วง มิ.ย.–ต.ค. เป็นฤดูฝน ควรพกร่มและเผื่อสถานที่ในร่ม');
    return notes;
  }

  function updateHint() {
    let el = $('seasonNote');
    if (!el) { $('dateSummary').insertAdjacentHTML('afterend', '<div id="seasonNote" class="season-note"></div>'); el = $('seasonNote'); }
    const dates = (typeof DATE_PICKER !== 'undefined' && DATE_PICKER) ? DATE_PICKER.selectedDates : [];
    const slug = getProvince();
    el.innerHTML = STATE.provinces[slug] ? `<div>ข้อมูลรองรับสูงสุด ${maxDays()} วันสำหรับ ${esc(nameOf(slug))}</div>` : '';
    seasonLines = dates.length ? seasonNote(slug, dates[0].getMonth() + 1) : [];
    refreshTips(true);
    loadWeather(slug, dates);
  }

  // ---------- พยากรณ์อากาศจริง (Open-Meteo: ฟรี ไม่ต้องใช้คีย์; ส่งเฉพาะพิกัดศูนย์กลางจังหวัดและวันที่) ----------
  // shortcut: พยากรณ์ล่วงหน้าได้ ~16 วัน, เกินนั้นใช้หมายเหตุฤดูกาลแบบคงที่แทน
  const WMO = c => c === 0 ? '☀️ ท้องฟ้าแจ่มใส' : c <= 2 ? '🌤️ มีเมฆบางส่วน' : c === 3 ? '☁️ เมฆมาก' : c <= 48 ? '🌫️ หมอก' : c <= 57 ? '🌦️ ฝนปรอย' : c <= 67 ? '🌧️ ฝนตก' : c <= 82 ? '🌧️ ฝนตกเป็นช่วง' : '⛈️ พายุฝนฟ้าคะนอง';
  const wxCache = {};
  let weatherLines = [], wxToken = 0, wetDays = false, wxDaily = {};
  async function loadWeather(slug, dates) {
    const my = ++wxToken, pv = STATE.provinces[slug];
    weatherLines = []; wetDays = false; wxDaily = {};
    if (!pv || !dates.length) return;
    const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    const start = iso(dates[0]), end = iso(dates[dates.length - 1]);
    const key = `${pv.center.map(x => x.toFixed(2))}|${start}|${end}`;
    try {
      if (!wxCache[key]) {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${pv.center[0].toFixed(3)}&longitude=${pv.center[1].toFixed(3)}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FBangkok&start_date=${start}&end_date=${end}`;
        const r = await fetch(url);
        if (!r.ok) throw new Error(r.status);   // เช่น วันที่เกิน 16 วันข้างหน้า → 400
        wxCache[key] = await r.json();
      }
      const d = wxCache[key].daily;
      const fmtD = s => new Date(s + 'T00:00:00').toLocaleDateString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH'), {day: 'numeric', month: 'short'});
      const wet = [];
      d.time.forEach((t, i) => { wxDaily[t] = {code: d.weathercode[i], lo: Math.round(d.temperature_2m_min[i]), hi: Math.round(d.temperature_2m_max[i]), pop: d.precipitation_probability_max[i] ?? 0}; });
      weatherLines = d.time.map((t, i) => {
        if ((d.precipitation_probability_max[i] ?? 0) >= 60) wet.push(fmtD(t));
        return `${WMO(d.weathercode[i])} ${fmtD(t)} ${Math.round(d.temperature_2m_min[i])}–${Math.round(d.temperature_2m_max[i])}°C โอกาสฝน ${d.precipitation_probability_max[i] ?? '-'}% (พยากรณ์จริง)`;
      });
      wetDays = wet.length > 0;
      if (wet.length) weatherLines.unshift(`☔ ${wet.slice(0, 3).join(', ')} มีโอกาสฝนสูง ควรพกร่มและเผื่อสถานที่ในร่ม`);
    } catch (e) { weatherLines = []; }
    if (my === wxToken) { refreshTips(true); if (STATE.selectedPkg && $('detailPanel').style.display !== 'none') decorateWeather(STATE.selectedPkg); }
  }
  // ---------- พยากรณ์รายวันในหน้าแผน + ปุ่มสลับเป็นสถานที่ในร่มเมื่อฝนตกหนัก ----------
  const OUTDOOR = ['beach', 'viewpoint', 'activity'];
  const dayIso = i => { const d0 = DATE_PICKER?.selectedDates[0]; if (!d0) return null; const d = new Date(d0.getTime() + i * 86400000); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
  window.dayRainPop = i => (wxDaily[dayIso(i)] || {}).pop || 0;   // โอกาสฝน (%) ของวันที่ i ใช้ในหน้าเปลี่ยนสถานที่
  window.OUTDOOR_CATS = OUTDOOR;
  function decorateWeather(pkg) {
    document.querySelectorAll('#dayPanels .day-panel').forEach((panel, i) => {
      panel.querySelectorAll('.wx-chip, .rain-banner').forEach(e => e.remove());
      const w = wxDaily[dayIso(i)]; if (!w) return;
      panel.querySelector('.day-stats')?.insertAdjacentHTML('afterbegin', `<span class="wx-chip" title="พยากรณ์จริงจาก Open-Meteo">${WMO(w.code).split(' ')[0]} ${w.lo}–${w.hi}°C · ฝน ${w.pop}%</span>`);
      const outdoor = pkg.days[i]?.pois.filter(p => OUTDOOR.includes(p.category)).length || 0;
      if (w.pop >= 60) panel.querySelectorAll('.poi-item').forEach(li => {   // ไอคอนฝนที่การ์ดสถานที่กลางแจ้งในวันที่ฝนตก
        const p = pkg.days[i]?.pois.find(x => x.id === li.dataset.id);
        if (p && OUTDOOR.includes(p.category) && !li.querySelector('.rain-ic')) li.querySelector('.poi-name')?.insertAdjacentHTML('beforeend', `<span class="rain-ic" title="${window.WET_LANG === 'en' ? 'Outdoor place, it may rain' : 'สถานที่กลางแจ้ง อาจมีฝนตกได้'}"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 14a4 4 0 0 0 0-8 5.5 5.5 0 0 0-10.6 1.5A3.5 3.5 0 0 0 7 14"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/></svg></span>`);
      });
      if (w.pop >= 60 && outdoor) panel.querySelector('.day-head').insertAdjacentHTML('afterend', `<div class="rain-banner">☔ วันนี้โอกาสฝน ${w.pop}% แต่มีสถานที่กลางแจ้ง ${outdoor} จุด <button type="button" onclick="indoorSwap(${i})">สลับเป็นสถานที่ในร่ม</button></div>`);
    });
  }
  const origRenderDetail = renderDetail;
  renderDetail = function (pkg) {
    if (!pkg._orig) setHidden(pkg, '_orig', JSON.parse(JSON.stringify(pkg)));   // จำแผนตั้งต้นที่ระบบคำนวณไว้ (ใช้กับปุ่มคืนค่าเดิม)
    origRenderDetail(pkg);
    for (const fn of [decorateWeather, decorateWarnings, enableDrag, recordHistory]) { try { fn(pkg); } catch (e) { console.error(fn.name, e); } }   // ข้อผิดพลาดในตัวตกแต่งต้องไม่ทำให้การลากการ์ดใช้ไม่ได้
  };

  // แสดงคำเตือนที่การ์ด (สีแดง + กล่องข้อความใต้การ์ด) เฉพาะ "อาจไปไม่ทันเวลาปิด" / "อาจไปถึงก่อนร้านเปิด" ค้างจนกว่าจะแก้หรือลากสลับใหม่
  function decorateWarnings(pkg) {
    document.querySelectorAll('.plan-warn, .poi-err-box').forEach(e => e.remove());
    document.querySelectorAll('.poi-item.poi-error').forEach(e => e.classList.remove('poi-error'));
    const panels = document.querySelectorAll('#dayPanels .day-panel'), clock = m => fmtClock(Math.round(m)), en = window.WET_LANG === 'en';
    uiWarnings(pkg).forEach(w => {
      const li = panels[w.d]?.querySelector(`.poi-item[data-id="${w.id}"]`); if (!li) return;
      li.classList.add('poi-error');
      let box = li.nextElementSibling; if (!box || !box.classList.contains('poi-err-box')) { box = document.createElement('li'); box.className = 'poi-err-box'; li.after(box); }
      const msg = w.type === 'late'
        ? (en ? `You may not make it before it closes (closes ${clock(w.poi.close_min)}). Try moving it earlier or choose another place.` : `อาจไปไม่ทันก่อนปิด (ปิดเวลา ${clock(w.poi.close_min)}) ลองย้ายไปไว้ก่อนหน้านี้หรือเปลี่ยนสถานที่`)
        : (en ? `You may arrive before it opens (opens ${clock(w.poi.open_min)}). Try moving it later.` : `อาจไปถึงก่อนร้านเปิด (เปิดเวลา ${clock(w.poi.open_min)}) ลองย้ายไปไว้หลังจากนี้`);
      box.innerHTML += `<div>⚠ ${esc(msg)}</div>`;
    });
  }

  // ---------- ลากวางสถานที่เพื่อเรียงลำดับ/ย้ายข้ามวัน (แล้วคำนวณเวลา-ค่าใช้จ่ายใหม่ตามลำดับที่ลาก) ----------
  // ย้ายสถานที่ไป "ตำแหน่งของเป้าหมาย" (ลากไปหลัง = ไปอยู่หลังเป้าหมาย, ลากไปหน้า = ไปอยู่หน้าเป้าหมาย); ถ้าส่งคำขอไม่สำเร็จ คืนแผนเดิม
  let keepVis = null;   // จำวันที่เปิดอยู่บนแผนที่ไว้ตอนวาดใหม่หลังแก้แผน
  const editView = focus => { keepVis = {focus, vis: Object.values(STATE.mapDayLayers).map(l => l.visible)}; };
  function snapshot() { return STATE.selectedPkg.days.map(d => d.pois.slice()); }
  function restore(snap) { STATE.selectedPkg.days.forEach((d, i) => { d.pois = snap[i].slice(); }); keepVis = null; }
  function moveStop(src, dst) {
    const days = STATE.selectedPkg.days, [sd, si] = src, snap = snapshot();
    const [poi] = days[sd].pois.splice(si, 1);
    const di = dst.i === null ? days[dst.d].pois.length : dst.i;
    days[dst.d].pois.splice(di, 0, poi);
    editView(null);
    recomputeAndRefresh(() => restore(snap));
  }
  // วาดแผนที่ใหม่หลังแก้แผน: คงวันที่เปิดอยู่ (หรือแสดงเฉพาะวันที่แก้) — ไม่ทำให้ลากหมุดได้ (ลากการ์ดทางซ้ายแทน)
  const origDrawOnMap = drawOnMap;
  drawOnMap = function (pkg) {
    origDrawOnMap(pkg);
    if (keepVis) {
      const {focus, vis} = keepVis; keepVis = null;
      Object.keys(STATE.mapDayLayers).forEach(k => {
        const want = focus != null ? +k === focus : vis[k] !== false, L_ = STATE.mapDayLayers[k];
        if (L_.visible !== want) toggleDay(+k);
      });
      resetMapView();
    }
  };
  // ลากการ์ดแบบ real-time: ขณะลากมีช่องว่าง (ไฮไลต์แดงจาง) เลื่อนไปตามตำแหน่งเมาส์ การ์ดอื่นขยับหลบด้วยอนิเมชัน (FLIP) แล้ววางลงช่องนั้น
  function enableDrag() {
    const root = document.getElementById('dayPanels'); if (!root) return;
    let gap = null, srcKey = null, srcLi = null, hiddenConn = null, ghost = null, offX = 0, offY = 0, corrX = 0, corrY = 0, curUl = null;
    const cards = ul => [...ul.querySelectorAll('.poi-item')].filter(e => e !== srcLi && e !== ghost);
    const flip = (ul, mutate) => {   // บันทึกตำแหน่งเดิม → เปลี่ยน DOM → เลื่อนจากตำแหน่งเดิมมาตำแหน่งใหม่
      const items = cards(ul), before = new Map(items.map(e => [e, e.getBoundingClientRect().top]));
      mutate();
      items.forEach(e => { const dy = before.get(e) - e.getBoundingClientRect().top; if (dy) { e.style.transition = 'none'; e.style.transform = `translateY(${dy}px)`; requestAnimationFrame(() => { e.style.transition = 'transform .18s ease'; e.style.transform = ''; }); } });
    };
    const cleanup = () => { hiddenConn?.classList.remove('drag-hide'); hiddenConn = null; gap?.remove(); gap = null; ghost?.remove(); ghost = null; srcLi?.classList.remove('dragging'); srcLi = null; curUl = null; root.classList.remove('is-dragging'); document.body.classList.remove('wet-dragging'); };
    // ใช้ pointer events แทน HTML5 drag-and-drop: การ์ดตามเมาส์ทุกเฟรม ไม่หน่วงเหมือน dragover ที่ถูกจำกัดความถี่
    root.querySelectorAll('.poi-list').forEach(ul => {
      const d = +(ul.id.match(/day-(\d+)-list/) || [])[1];
      ul.querySelectorAll('.poi-item').forEach((li, i) => {
        li.draggable = false; li.title = li.title || (window.WET_LANG === 'en' ? 'Drag to reorder or move to another day' : 'ลากเพื่อเรียงลำดับหรือย้ายไปวันอื่น');
        li.ondragstart = e => e.preventDefault();   // ปิด drag ของเบราว์เซอร์ (ข้อความ/รูปในการ์ด) ที่จะขัดกับการลากแบบ pointer
        li.onpointerdown = e => {
          if (e.button !== 0 || e.pointerType === 'touch' || e.target.closest('button, a, input, select')) return;
          e.preventDefault();
          const sx = e.clientX, sy = e.clientY, r0 = li.getBoundingClientRect(); let started = false;
          const start = () => {
            started = true; srcKey = [d, i]; srcLi = li; offX = sx - r0.left; offY = sy - r0.top;
            gap = document.createElement('li'); gap.className = 'drop-gap'; gap.style.height = li.offsetHeight + 'px';
            root.classList.add('is-dragging'); document.body.classList.add('wet-dragging'); document.getSelection()?.removeAllRanges();
            ghost = li.cloneNode(true); ghost.classList.add('drag-ghost'); ghost.removeAttribute('title');
            ghost.style.cssText = `width:${r0.width}px;left:${r0.left}px;top:${r0.top}px;transform-origin:${offX}px ${offY}px`;
            ul.appendChild(ghost);
            ghost.style.animation = 'none'; ghost.style.transform = 'none'; const g0 = ghost.getBoundingClientRect(); ghost.style.animation = ''; ghost.style.transform = '';
            corrX = g0.left - r0.left; corrY = g0.top - r0.top;   // บาง ancestor มี transform ทำให้ fixed อิงกรอบนั้น: ชดเชยส่วนต่างให้ตรงเมาส์
            li.classList.add('dragging'); li.after(gap); curUl = ul;
            const pv = li.previousElementSibling; if (pv?.classList.contains('dist-connector')) { pv.classList.add('drag-hide'); hiddenConn = pv; }
          };
          let raf = 0, last = null;
          const frame = () => {
            raf = 0; if (!ghost || !last) return;
            ghost.style.left = (last.clientX - offX - corrX) + 'px'; ghost.style.top = (last.clientY - offY - corrY) + 'px';
            const under = document.elementFromPoint(last.clientX, last.clientY), panel = under?.closest('.day-panel'), tul = panel?.querySelector('.poi-list');
            if (!tul) return;
            const cs = cards(tul); let ref = null;
            for (const c of cs) { const r = c.getBoundingClientRect(); if (last.clientY < r.top + r.height / 2) { ref = c; break; } }
            const already = gap.parentNode === tul && (ref ? gap.nextElementSibling === ref : !cs.some(c => gap.compareDocumentPosition(c) & 4));
            if (already) return;
            flip(tul, () => { if (ref) tul.insertBefore(gap, ref); else tul.appendChild(gap); }); curUl = tul;
          };
          const move = ev => {
            if (!started) { if (Math.hypot(ev.clientX - sx, ev.clientY - sy) < 6) return; start(); }
            last = ev; if (!raf) raf = requestAnimationFrame(frame);
          };
          const up = ev => {
            document.removeEventListener('pointermove', move); document.removeEventListener('pointerup', up); document.removeEventListener('pointercancel', up);
            if (!started) return;
            if (raf) cancelAnimationFrame(raf);
            window.addEventListener('click', ck => { ck.stopPropagation(); ck.preventDefault(); }, {capture: true, once: true});   // ไม่ให้การปล่อยเมาส์ถูกนับเป็นคลิกการ์ด
            const targetUl = gap?.parentNode, src = srcKey;
            if (ev.type === 'pointercancel' || !targetUl || !targetUl.classList.contains('poi-list')) { cleanup(); return; }
            const dd = +targetUl.id.match(/day-(\d+)-list/)[1];
            const idx = [...targetUl.children].filter(c => (c.classList.contains('poi-item') && c !== srcLi && c !== ghost) || c === gap).indexOf(gap);
            cleanup();
            if (!(src[0] === dd && src[1] === idx)) moveStop(src, {d: dd, i: idx});
          };
          document.addEventListener('pointermove', move); document.addEventListener('pointerup', up); document.addEventListener('pointercancel', up);
        };
      });
    });
  }

  // สลับสถานที่กลางแจ้ง (หาด จุดชมวิว กิจกรรม) ของวันนั้นเป็นพิพิธภัณฑ์/ตลาดคะแนนสูงที่ใกล้ที่สุดและยังไม่อยู่ในแผน แล้วให้ Hybrid จัดเส้นทางใหม่
  window.indoorSwap = async function (dIdx) {
    const pkg = STATE.selectedPkg, day = pkg.days[dIdx];
    const inPlan = new Set(pkg.days.flatMap(d => d.pois.map(p => p.id)));
    const base = day.pois.filter(p => p.category !== 'restaurant');
    const cLat = base.reduce((s, p) => s + p.lat, 0) / base.length, cLng = base.reduce((s, p) => s + p.lng, 0) / base.length;
    const cands = STATE.pois.filter(p => ['culture', 'market'].includes(p.category) && !inPlan.has(p.id) && !STATE.excluded.has(p.id) && haversineKm(cLat, cLng, p.lat, p.lng) <= 25)
      .sort((a, b) => (b.category === 'culture') - (a.category === 'culture') || b.score - a.score);
    const snap = snapshot(), savedLocked = new Set(STATE.locked), savedExcl = new Set(STATE.excluded);
    let n = 0;
    day.pois.slice().forEach((p, k) => {
      if (!OUTDOOR.includes(p.category)) return;
      const at = arriveOf(day, p);   // นาทีที่ไปถึงจุดเดิม — เลือกที่ในร่มที่เปิดอยู่ช่วงนั้น
      const ci = cands.findIndex(c => at < 0 || (c.open_min <= at && at + c.duration_min <= c.close_min));
      if (ci < 0) return;
      const [c] = cands.splice(ci, 1);
      day.pois[k] = c; STATE.locked.add(c.id); STATE.excluded.add(p.id); STATE.locked.delete(p.id); n++;
    });
    if (!n) { showToast('ไม่พบสถานที่ในร่มใกล้เคียงที่ยังเปิดอยู่ในช่วงเวลานั้นและยังไม่อยู่ในแผน', 'error', 4500); return; }
    showToast(`สลับ ${n} จุดของวันที่ ${dIdx + 1} เป็นสถานที่ในร่มแล้ว`, 'ok', 3000);
    editView(dIdx);   // แสดงเฉพาะวันที่กดบนแผนที่
    // คำนวณใหม่เฉพาะแผนที่ผู้ใช้แก้ (ไม่ย้ายจุดของวันอื่น) ถ้าล้มเหลวคืนค่าเดิมทั้งหมด
    await recomputeAndRefresh(() => { restore(snap); STATE.locked = savedLocked; STATE.excluded = savedExcl; });
  };

  // ---------- กล่อง Tips (หมุนทุก 20 วินาที) ----------
  let seasonLines = [], tipIdx = 0, tipPool = [], tipsTimer = null, tipsFor = null;
  // แม่แบบ Tips ต่อหมวด: ok = เงื่อนไขจากข้อมูลจริงของสถานที่ (กันแนะนำผิด เช่น บอกให้ไปตอนเย็นทั้งที่ปิดแล้ว)
  const hhmm = m => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
  const price = p => p.cost > 0 ? `ค่าเข้า/ใช้จ่ายราว ${fmt(p.cost)} บาท` : 'ไม่เสียค่าเข้า';
  const hrs = p => p.open_min <= 0 && p.close_min >= 1439 ? 'เปิดทั้งวัน' : `เปิด ${hhmm(p.open_min)}–${hhmm(p.close_min)}`;
  const morning = p => p.open_min <= 600, evening = p => p.close_min >= 1080, any = () => true;
  const dur = p => p.duration_min >= 30 ? `ใช้เวลาราว ${p.duration_min >= 90 ? Math.round(p.duration_min / 60 * 10) / 10 + ' ชั่วโมง' : p.duration_min + ' นาที'}` : '';
  // dry = ใช้เฉพาะวันที่ไม่ฝน, rain = ใช้เฉพาะเมื่อพยากรณ์ว่าฝนตก
  const TIP_TPL = {
    beach: [
      {ok: morning, dry: 1, t: p => `🏖️ ${p.name_th} ไปช่วงเช้าแดดยังไม่แรง ทรายเย็น เหมาะกับการเดินเล่น`},
      {ok: evening, dry: 1, t: p => `🌅 ${p.name_th} นั่งชมพระอาทิตย์ตกได้ ${hrs(p)}`},
      {ok: any, dry: 1, t: p => `🏖️ ${p.name_th} ${price(p)} อย่าลืมครีมกันแดดและน้ำดื่ม`},
      {ok: any, t: p => `📸 ${p.name_th} จุดถ่ายรูปยอดนิยมของหมวดหาด ${dur(p)}`.trim()},
      {ok: any, dry: 1, t: p => `🩴 ${p.name_th} พกรองเท้าแตะกับผ้าเช็ดตัวเล็ก ๆ ไว้ ลงเล่นน้ำได้ทันที`},
      {ok: any, t: p => `🌊 ${p.name_th} ดูธงเตือนคลื่นลมก่อนลงเล่นน้ำทุกครั้ง และเล่นในเขตที่กำหนด`},
      {ok: any, rain: 1, t: p => `🌧️ ${p.name_th} ช่วงฝนคลื่นอาจแรง ชมวิวจากริมหาดแทนการลงน้ำจะปลอดภัยกว่า`},
    ],
    temple: [
      {ok: morning, t: p => `🛕 ${p.name_th} แวะตอนเช้าอากาศเย็น คนน้อย ${hrs(p)}`},
      {ok: any, t: p => `🛕 ${p.name_th} แต่งกายสุภาพ ถอดรองเท้าก่อนเข้าอาคาร ${price(p)}`},
      {ok: any, t: p => `🙏 ${p.name_th} ${dur(p) || 'แวะชมได้ไม่นาน'} เหมาะแทรกระหว่างสถานที่อื่น`},
      {ok: evening, t: p => `🪔 ${p.name_th} ยังเปิดถึง ${hhmm(p.close_min)} ไปช่วงเย็นบรรยากาศสงบ`},
      {ok: any, t: p => `🤫 ${p.name_th} พูดเบา ๆ และขออนุญาตก่อนถ่ายรูปพระหรือผู้คน`},
      {ok: any, rain: 1, t: p => `☔ ${p.name_th} มีศาลาหรืออาคารให้หลบฝนได้ เหมาะกับวันฝนตก`},
      {ok: any, dry: 1, t: p => `🌳 ${p.name_th} พื้นที่โล่ง ควรพกหมวกหรือร่มกันแดดไว้`},
    ],
    viewpoint: [
      {ok: evening, dry: 1, t: p => `🌄 ${p.name_th} ควรไปช่วงเย็น แสงสวยที่สุด (ปิด ${hhmm(p.close_min)})`},
      {ok: morning, dry: 1, t: p => `⛅ ${p.name_th} ไปเช้าท้องฟ้าโปร่ง ถ่ายวิวได้ชัด`},
      {ok: any, t: p => `🌄 ${p.name_th} ${price(p)} พกกล้องหรือโทรศัพท์แบตเต็มไปด้วย`},
      {ok: any, t: p => `👟 ${p.name_th} ใส่รองเท้าเดินสบาย ${dur(p)}`.trim()},
      {ok: any, rain: 1, t: p => `🌫️ ${p.name_th} วันฝนทัศนียภาพอาจถูกเมฆบัง ลองสลับไปไว้วันที่ฟ้าเปิด`},
      {ok: any, t: p => `🧥 ${p.name_th} ที่สูงลมแรงกว่าที่คิด พกเสื้อบาง ๆ ไว้สักตัว`},
    ],
    culture: [
      {ok: any, t: p => `🏛️ ${p.name_th} ${hrs(p)} ${price(p)}`},
      {ok: any, t: p => `🎟️ ${p.name_th} ${dur(p) || 'เดินชมได้สบาย'} เหมาะเป็นกิจกรรมหลบแดดช่วงบ่าย`},
      {ok: morning, t: p => `📚 ${p.name_th} แวะตอนเช้าได้ข้อมูลเต็มที่ ก่อนคนเยอะ`},
      {ok: any, t: p => `🏛️ ${p.name_th} ได้เรียนรู้เรื่องราวท้องถิ่น เหมาะกับครอบครัว`},
      {ok: any, rain: 1, t: p => `☔ ${p.name_th} กิจกรรมในร่มที่เหมาะกับวันฝนตก ${hrs(p)}`},
      {ok: any, t: p => `🗺️ ${p.name_th} ถามเจ้าหน้าที่ถึงเรื่องเล่าท้องถิ่น มักได้ข้อมูลที่ไม่มีในป้าย`},
    ],
    market: [
      {ok: evening, t: p => `🛍️ ${p.name_th} ช่วงเย็นคึกคักที่สุด เหมาะกับมื้อเย็นและของฝาก (ปิด ${hhmm(p.close_min)})`},
      {ok: any, t: p => `🍢 ${p.name_th} ลองของกินพื้นเมือง พกเงินสดเล็กน้อยไว้ต่อรอง`},
      {ok: morning, t: p => `🧺 ${p.name_th} ไปเช้าของสดและของฝากครบกว่า`},
      {ok: any, t: p => `🛍️ ${p.name_th} ${hrs(p)} เดินเล่นได้ ${dur(p)}`.trim()},
      {ok: any, t: p => `🥭 ${p.name_th} ถามหาผลไม้หรือขนมประจำฤดูกาล ซื้อกินสด ๆ อร่อยกว่า`},
      {ok: any, rain: 1, t: p => `🌂 ${p.name_th} ตลาดมักมีหลังคาบางส่วน พกร่มพับไว้ก็เดินได้สบาย`},
    ],
    activity: [
      {ok: any, t: p => `🎈 ${p.name_th} กิจกรรมสนุก ๆ ${price(p)} ควรเช็คคิวหรือจองล่วงหน้า`},
      {ok: morning, dry: 1, t: p => `🤸 ${p.name_th} เริ่มตอนเช้าอากาศดี ไม่ร้อนจัด`},
      {ok: any, t: p => `👨‍👩‍👧 ${p.name_th} เหมาะกับเพื่อนและครอบครัว ${dur(p)}`.trim()},
      {ok: any, dry: 1, t: p => `🎒 ${p.name_th} เตรียมเสื้อผ้าเปลี่ยนและครีมกันแดด ${hrs(p)}`},
      {ok: any, rain: 1, t: p => `📞 ${p.name_th} กิจกรรมกลางแจ้งอาจเลื่อนเมื่อฝนตก โทรเช็คกับผู้ให้บริการก่อนออกเดินทาง`},
      {ok: any, t: p => `💧 ${p.name_th} จิบน้ำบ่อย ๆ และฟังคำแนะนำด้านความปลอดภัยของเจ้าหน้าที่`},
    ],
  };
  // เคล็ดลับทั่วไป (ไม่ผูกกับสถานที่) — บางข้อปรับตามจำนวนวัน/งบ/จำนวนคนที่กรอก
  function generalTips() {
    const days = SELECTED_DAYS, budget = +$('budget').value || 0, ppl = +$('travelers').value || 1;
    const t = [
      '💡 กด "ความชอบ" เพื่อเลือกหมวดที่ชอบหรือไม่ชอบ แผนจะปรับตามให้',
      '💡 บันทึกแผนที่ถูกใจด้วยปุ่ม ★ แล้วกลับมาเปิดดูได้ภายหลัง',
      '💡 เที่ยวต่อจังหวัดข้างเคียงได้ กดชื่อจังหวัดใต้ช่องเลือกจังหวัด',
      '🔄 ไม่ถูกใจสถานที่ไหน กดสลับหรือลบจุดในแผน ระบบจะจัดเส้นทางที่เหลือให้ใหม่',
      '📅 ส่งแผนเข้าปฏิทินได้ด้วยปุ่ม ปฏิทิน และบันทึกเป็น PDF ไว้เปิดตอนไม่มีสัญญาณ',
      '👫 ชวนเพื่อนวางแผนด้วยกันผ่านปุ่ม แชร์ ทุกคนเห็นและแก้แผนเดียวกันได้',
      '⇄ อยากรู้ว่าอัลกอริทึมไหนวางแผนได้ดีกว่า ลองกด "เทียบอัลกอริทึม" ในหน้าปรับแต่งทริป',
      '🚗 เวลาเดินทางในแผนคิดแบบรถไม่ติด ช่วงชั่วโมงเร่งด่วนควรเผื่อเวลาเพิ่มราว 20–30%',
      '🍜 มื้อกลางวันช่วง 11:00–14:30 ร้านดัง ๆ คนเยอะ ไปก่อน 11:30 มักไม่ต้องรอคิว',
      '🔋 พกพาวเวอร์แบงก์และเก็บแผนที่ออฟไลน์ไว้ เผื่อสัญญาณอินเทอร์เน็ตไม่ดี',
      '🧴 ครีมกันแดด หมวก และน้ำดื่ม เป็นของที่ควรพกติดตัวทุกทริป',
    ];
    if (days >= 4) t.push(`🛌 ทริป ${days} วันแนะนำให้เว้นช่วงพักครึ่งวันสักวัน จะไม่เหนื่อยสะสม`);
    if (days === 1) t.push('⏰ ทริปวันเดียวควรเริ่มก่อน 9:00 และเลือกสถานที่ที่อยู่ใกล้กัน');
    if (budget && days) t.push(`💰 งบ ${fmt(budget)} บาท ตก ${fmt(budget / days / ppl)} บาท/คน/วัน รวมที่พักแล้ว ปรับงบเพิ่มเพื่อได้แพ็กเกจ Premium`);
    if (ppl >= 4) t.push('👨‍👩‍👧‍👦 เดินทางหลายคน แชร์ค่ารถหรือเช่ารถตู้จะคุ้มกว่าเรียกรถแยก');
    return t;
  }
  // Tips เฉพาะจังหวัด: จุดเด่นจากข้อมูลจริงของจังหวัดนั้น + เคล็ดลับตามภูมิภาค/ลักษณะพื้นที่
  const REGION_TIPS = {
    'ภาคเหนือ': ['🧣 ภาคเหนือหน้าหนาว (พ.ย.–ก.พ.) ตอนเช้าอากาศเย็นจัด พกเสื้อกันหนาวบางๆ', '🏍️ ถนนบนเขามีโค้งมาก ขับช้าๆ และเผื่อเวลาเดินทางเพิ่ม', '🍲 ลองอาหารเหนือ เช่น ขันโตก ข้าวซอย น้ำพริกหนุ่ม', '🌫️ ช่วงปลายหนาวถึงต้นร้อนอาจมีหมอกควัน ตรวจค่าฝุ่นก่อนไปจุดชมวิว'],
    'ภาคตะวันออกเฉียงเหนือ': ['🌞 ภาคอีสานแดดแรงและร้อนจัดช่วงเมษายน แนะนำเที่ยวเช้าและเย็น', '🥗 ลองส้มตำ ลาบ และไก่ย่างของท้องถิ่น', '🛕 อีสานมีปราสาทหินและวัดเก่าแก่ ควรพกหมวกและน้ำดื่ม', '🚗 ระยะทางระหว่างอำเภอค่อนข้างไกล ควรเช่ารถหรือจัดรถไว้ล่วงหน้า'],
    'ภาคกลาง': ['🛶 ภาคกลางมีตลาดน้ำและวัดเก่า แต่งกายสุภาพเมื่อเข้าวัด', '☀️ ช่วงบ่ายร้อนจัด เหมาะกับพิพิธภัณฑ์และร้านในร่ม', '🚆 เดินทางรถไฟหรือรถตู้ไปหลายเมืองได้สะดวก', '🍜 อาหารภาคกลางมีหลากหลาย ลองก๋วยเตี๋ยวเรือและขนมไทยโบราณ'],
    'ภาคตะวันออก': ['🏖️ ชายฝั่งตะวันออกเที่ยวทะเลสะดวก ใกล้กรุงเทพฯ เหมาะกับทริปสั้น', '🍤 อาหารทะเลสดที่ตลาดชายหาด ถามราคาก่อนสั่งทุกครั้ง', '🍈 ช่วงเมษายน–มิถุนายนมีผลไม้ฤดูกาลมาก เช่น ทุเรียน มังคุด เงาะ', '⛴️ ถ้าไปเกาะ เช็คตารางเรือและสภาพคลื่นก่อนเดินทาง'],
    'ภาคตะวันตก': ['🌳 ภาคตะวันตกมีป่า น้ำตก และอุทยาน พกยากันยุงและรองเท้าเดินป่า', '🌊 น้ำตกหน้าฝนน้ำแรง ตรวจประกาศอุทยานก่อนลงเล่นน้ำ', '🚆 รถไฟสายประวัติศาสตร์เป็นกิจกรรมที่น่าลอง ควรจองตั๋วล่วงหน้า', '🍃 ที่พักใกล้ธรรมชาติมักไม่มีสัญญาณมือถือ เก็บแผนที่ออฟไลน์ไว้'],
    'ภาคใต้': ['⛵ ภาคใต้ทะเลอันดามัน ช่วงพ.ค.–ต.ค. คลื่นลมแรง เรือบางเส้นทางงดเดินเรือ', '🏝️ ฝั่งอ่าวไทยฝนหนักช่วงต.ค.–ธ.ค. เช็คพยากรณ์ก่อนไปเกาะ', '🍛 ลองอาหารใต้ เช่น แกงส้ม ข้าวยำ และโรตีกับแกงกะหรี่', '🧴 แดดทะเลแรงมาก ทาครีมกันแดดซ้ำทุก 2 ชั่วโมง'],
  };
  function provinceTips() {
    const base = (typeof baseSlug !== 'undefined' && baseSlug) || getProvince().split('+')[0], pv = STATE.provinces[base] || {}, nm = pv.name_th || base;
    const out = [...(REGION_TIPS[pv.region] || [])];
    const best = c => STATE.pois.filter(p => p.category === c && p.open_min !== undefined).sort((a, b) => b.score - a.score).slice(0, 3).map(p => p.name_th);
    const hi = [['beach', 'หาดและทะเล'], ['temple', 'วัด'], ['viewpoint', 'จุดชมวิว'], ['culture', 'วัฒนธรรมและพิพิธภัณฑ์'], ['market', 'ตลาด'], ['activity', 'กิจกรรม']];
    hi.forEach(([c, label]) => { const b = best(c); if (b.length >= 2) out.push(`📍 ${label}เด่นของ${nm}: ${b.join(' · ')}`); });
    const dist = STATE.provinces[base]?.max_days; if (dist) out.push(`🗓️ ข้อมูลของ${nm}รองรับทริปได้สูงสุด ${dist} วัน`);
    return out;
  }
  function buildTips() {
    const top = STATE.pois.filter(p => TIP_TPL[p.category] && p.open_min !== undefined).sort((a, b) => b.score - a.score).slice(0, 20);
    const used = new Set(), places = [];
    top.forEach(p => {
      const opts = TIP_TPL[p.category].filter(x => x.ok(p) && !(x.dry && wetDays) && !(x.rain && !wetDays) && !used.has(x));
      const x = opts[Math.floor(Math.random() * opts.length)];   // แม่แบบเดียวกันใช้ได้ครั้งเดียวต่อรอบ ไม่ให้ประโยคซ้ำกันกับหลายสถานที่
      if (x) { used.add(x); places.push(x.t(p)); }
    });
    const shuf = a => a.sort(() => Math.random() - 0.5);
    const pool = [...weatherLines, ...(weatherLines.length ? [] : seasonLines.map(l => '🌤️ ' + l))];
    // สลับสถานที่กับเคล็ดลับทั่วไปสลับกัน ไม่ให้ข้อความประเภทเดียวติดกันยาว
    const g = shuf(generalTips().filter(x => STATE.dev || !x.includes('เทียบอัลกอริทึม'))), pl = shuf(places), rg = shuf(provinceTips());
    while (g.length || pl.length || rg.length) { if (rg.length) pool.push(rg.pop()); if (pl.length) pool.push(pl.pop()); if (pl.length) pool.push(pl.pop()); if (g.length && Math.random() < 0.6) pool.push(g.pop()); else if (!pl.length && !rg.length) pool.push(g.pop()); }
    return pool;
  }
  function showTip(animate) {
    const t = $('tipsText'); if (!t || !tipPool.length) return;
    const set = () => { t.textContent = tipPool[tipIdx++ % tipPool.length]; t.classList.remove('fade'); };
    if (animate) { t.classList.add('fade'); setTimeout(set, 400); } else set();
  }
  function refreshTips(rebuild) {
    if (!$('tipsText')) return;
    if (rebuild || tipsFor !== STATE.pois) { tipPool = buildTips(); tipIdx = 0; tipsFor = STATE.pois; showTip(false); }
  }
  // ---------- Tips ภาษาอังกฤษ (ใช้เมื่อสลับภาษา) ----------
  const WMO_EN = c => c === 0 ? '☀️ Clear' : c <= 2 ? '🌤️ Partly cloudy' : c === 3 ? '☁️ Overcast' : c <= 48 ? '🌫️ Fog' : c <= 57 ? '🌦️ Drizzle' : c <= 67 ? '🌧️ Rain' : c <= 82 ? '🌧️ Showers' : '⛈️ Thunderstorm';
  const TIP_EN = {
    beach: [p => `🏖️ ${p.name_en}: go in the morning or late afternoon when the sun is milder`, p => `🌊 ${p.name_en}: check the wave flags before swimming`],
    temple: [p => `🛕 ${p.name_en}: dress modestly and take your shoes off before entering`, p => `🙏 ${p.name_en}: a quiet stop between busier places`],
    viewpoint: [p => `🌄 ${p.name_en}: best around sunset (closes ${hhmm(p.close_min)})`, p => `👟 ${p.name_en}: wear comfortable shoes`],
    culture: [p => `🏛️ ${p.name_en}: ${hrs(p).replace('เปิด', 'open').replace('ทั้งวัน', 'all day')} — a good indoor stop in the afternoon`, p => `🎟️ ${p.name_en}: ask the staff for local stories`],
    market: [p => `🛍️ ${p.name_en}: liveliest in the evening — good for dinner and souvenirs`, p => `🍢 ${p.name_en}: try local snacks, bring a little cash`],
    activity: [p => `🎈 ${p.name_en}: book ahead in busy periods`, p => `💧 ${p.name_en}: drink plenty of water and follow the safety briefing`],
  };
  function buildTipsEN() {
    const days = SELECTED_DAYS, budget = +$('budget').value || 0, ppl = +$('travelers').value || 1;
    const pool = [];
    const iso = Object.keys(wxDaily).sort();
    iso.forEach(t => { const w = wxDaily[t]; pool.push(`${WMO_EN(w.code)} ${t.slice(5)} ${w.lo}–${w.hi}°C · rain ${w.pop}% (live forecast)`); });
    if (iso.some(t => wxDaily[t].pop >= 60)) pool.unshift('☔ High chance of rain on some days — bring an umbrella and keep indoor options ready');
    const top = STATE.pois.filter(p => TIP_EN[p.category]).sort((a, b) => b.score - a.score).slice(0, 14);
    const places = top.map(p => { const o = TIP_EN[p.category]; return o[Math.floor(Math.random() * o.length)](p); }).sort(() => Math.random() - 0.5);
    const g = [
      '💡 Open "Preferences" to like or dislike categories — your plan adapts', '💡 Save plans you like with ★ and reopen them later', '💡 Add a nearby province with the buttons under the province field',
      '🔄 Swap or remove a stop and the rest of the route is re-optimized', '📅 Export to your calendar or save as PDF to use offline', '👫 Plan together: the Share button gives a live link',
      '🚗 Travel times assume no traffic — add 20–30% in rush hour', '🍜 Popular lunch spots fill up after 11:30 — arrive a little earlier', '🔋 Carry a power bank and save an offline map', '🧴 Sunscreen, a hat and water are always worth packing',
    ];
    if (days >= 4) g.push(`🛌 On a ${days}-day trip, keep one half-day free to rest`);
    if (budget && days) g.push(`💰 ${fmt(budget)} THB is about ${fmt(budget / days / ppl)} THB per person per day including accommodation`);
    g.sort(() => Math.random() - 0.5);
    while (g.length || places.length) { if (places.length) pool.push(places.pop()); if (places.length) pool.push(places.pop()); if (g.length) pool.push(g.pop()); }
    return pool;
  }
  const buildTipsTH = buildTips;
  buildTips = function () { return window.WET_LANG === 'en' ? buildTipsEN() : buildTipsTH(); };
  window.addEventListener('wet-lang', () => refreshTips(true));

  window.wetTips = () => tipPool.slice();   // ใช้ตรวจชุดข้อความ Tips ปัจจุบัน
  function initTips() {
    document.querySelector('.pf-col-search')?.insertAdjacentHTML('beforebegin',
      '<div class="pf-col pf-col-tips"><label class="pf-label">Tips</label><div class="tips-card"><span class="tips-badge">TIPS</span><span class="tips-text" id="tipsText"></span></div></div>');
    tipsTimer = setInterval(() => { refreshTips(false); showTip(true); }, 10000);
    setInterval(() => { if (tipsFor !== STATE.pois && STATE.pois.length) refreshTips(true); }, 1000);   // ข้อมูลจังหวัดโหลดเสร็จ/เปลี่ยนจังหวัด
  }

  const origDateSummary = updateDateSummary;
  updateDateSummary = function (dates) { origDateSummary(dates); updateHint(); };

  // ---------- บันทึก / เปิดแผน ----------
  function makeModal(id, title, sub) {
    document.body.insertAdjacentHTML('beforeend', `<div class="modal" id="${id}"><div class="modal-backdrop" data-close></div><div class="modal-card"><div class="modal-head"><div><div class="modal-title">${title}</div><div class="modal-sub">${sub}</div></div><button class="icon-btn" data-close title="ปิด">✕</button></div><div class="modal-body" id="${id}Body"></div></div></div>`);
    $(id).querySelectorAll('[data-close]').forEach(b => b.onclick = () => toggleModal(id, false));
  }
  function toggleModal(id, on) {
    $(id).classList.toggle('open', on);
    document.body.style.overflow = on ? 'hidden' : '';
  }

  window.savePlan = function () {
    const pkg = STATE.selectedPkg;
    if (!pkg) return;
    const list = store.get();
    const d0 = (typeof DATE_PICKER !== 'undefined' && DATE_PICKER?.selectedDates[0]) || null;
    list.unshift({
      id: Date.now(), province: getProvince(), label: `${nameOf(getProvince())} · ${pkg.tier} · ${pkg.days.length} วัน`,
      budget: +$('budget').value, travelers: +$('travelers').value, includeHotel: STATE.includeHotel !== false,
      start: d0 ? d0.toISOString().slice(0, 10) : null, pkg,
    });
    showToast(store.set(list.slice(0, 20)) ? 'บันทึกแผนแล้ว (เก็บในเบราว์เซอร์นี้ ได้สูงสุด 20 แผน)' : 'บันทึกไม่ได้ พื้นที่เบราว์เซอร์เต็มหรือถูกปิดไว้', list.length ? 'ok' : 'error');
  };

  window.openSaved = function () {
    const list = store.get();
    $('savedModalBody').innerHTML = list.length ? list.map(p =>
      `<div class="saved-row"><div><b>${esc(p.label)}</b><div class="pf-hint">งบ ${fmt(p.budget)} ฿ · ${p.travelers} คน · ${new Date(p.id).toLocaleString((window.WET_LANG === 'en' ? 'en-GB' : 'th-TH'))}</div></div>
       <div><button class="pareto-use" onclick="loadSaved(${p.id})">เปิด</button> <button class="pareto-use" onclick="deleteSaved(${p.id})">ลบ</button></div></div>`).join('')
      : '<p class="pf-hint">ยังไม่มีแผนที่บันทึกไว้ — กดปุ่ม "บันทึก" ในหน้าปรับแต่งทริป</p>';
    toggleModal('savedModal', true);
  };

  window.deleteSaved = id => { store.set(store.get().filter(p => p.id !== id)); openSaved(); };

  window.loadSaved = async function (id) {
    const p = store.get().find(x => x.id === id);
    if (!p) return;
    toggleModal('savedModal', false);
    baseSlug = p.province.split('+')[0];
    registerCombo(p.province);
    $('province').value = p.province;
    $('provName').textContent = p.province.split('+').map(nameOf).join(' + ');
    document.querySelectorAll('.prov-item').forEach(i => i.classList.toggle('prov-active', i.dataset.value === baseSlug));
    await loadPois();
    renderNeighbors();
    $('budget').value = p.budget; $('travelers').value = p.travelers;
    if (p.start && DATE_PICKER) {
      const d0 = new Date(p.start + 'T00:00:00');
      DATE_PICKER.setDate([d0, new Date(d0.getTime() + (p.pkg.days.length - 1) * 86400000)], true);
    }
    STATE.includeHotel = p.includeHotel;
    STATE.packages = [p.pkg]; STATE.selectedPkg = JSON.parse(JSON.stringify(p.pkg));
    STATE.locked.clear(); STATE.excluded.clear();
    $('detailPanel').style.display = 'block';
    renderDetail(STATE.selectedPkg);
    setTimeout(() => {
      STATE.map.setView(STATE.provinces[p.province].center, STATE.provinces[p.province].zoom);
      STATE.map.invalidateSize(); drawOnMap(STATE.selectedPkg);
      $('detailPanel').scrollIntoView({behavior: 'smooth', block: 'start'});
      setTimeout(syncMapHeight, 150);
    }, 150);
    showToast('เปิดแผนที่บันทึกไว้แล้ว', 'ok');
  };

  // ---------- เปรียบเทียบอัลกอริทึม ----------
  window.openCompare = async function () {
    if (!STATE.selectedPkg) return;
    const body = {province: getProvince(), preferences: getPreferences(), budget: +$('budget').value,
      days: STATE.selectedPkg.days.length, travelers: +$('travelers').value, include_hotel: STATE.includeHotel !== false, seed: 12345};
    const t = showToast('กำลังรัน Greedy, GA และ Hybrid บนโจทย์เดียวกัน (GA ใช้เวลาหลายวินาที)...', 'loading', 60000);
    try {
      const res = await Promise.all(['greedy', 'ga', 'hybrid'].map(async a => {
        const r = await fetch(`${API_BASE}/api/packages`, {method: 'POST', headers: devHeaders(), body: JSON.stringify({...body, algorithm: a})});
        if (!r.ok) throw new Error(`${a}: HTTP ${r.status}`);
        return [a, (await r.json()).packages];
      }));
      const km = p => p.days.reduce((s, d) => s + d.distance_km, 0);
      let rows = '';
      res.forEach(([a, pk]) => pk.forEach(p => {
        rows += `<tr class="${a === 'hybrid' ? 'cmp-main' : ''}"><td>${ALGO_NAMES[a]}</td><td>${p.tier}</td><td>${p.total_score.toFixed(1)}</td><td>${fmt(p.total_cost)}</td><td>${km(p).toFixed(0)}</td><td>${p.runtime_ms < 1000 ? Math.round(p.runtime_ms) + ' ms' : (p.runtime_ms / 1000).toFixed(1) + ' s'}</td><td>${p.valid ? '✓' : '✗'}</td></tr>`;
      }));
      $('compareModalBody').innerHTML = `<table class="pareto-table"><tr><th>อัลกอริทึม</th><th>แพ็กเกจ</th><th>คะแนนรวม</th><th>ค่าใช้จ่าย (฿)</th><th>ระยะทาง (km)</th><th>เวลาคำนวณ</th><th>ผ่านข้อจำกัด</th></tr>${rows}</table>
        <p class="pf-hint">โจทย์เดียวกัน (${body.days} วัน งบ ${fmt(body.budget)} ฿ ${body.travelers} คน) seed เดียวกัน — Hybrid เป็นอัลกอริทึมหลัก ส่วน Greedy และ GA เป็นเส้นฐานเปรียบเทียบ</p>`;
      t.remove();
      toggleModal('compareModal', true);
    } catch (e) { t.remove(); showToast(`ผิดพลาด: ${e.message}`, 'error'); }
  };

  // ---------- dropdown อาหาร (แทน <select> ของเบราว์เซอร์ ให้เข้ากับสไตล์เว็บ) ----------
  function initDietSelect() {
    const sel = $('prefDiet'); if (!sel) return;
    sel.style.display = 'none';
    sel.insertAdjacentHTML('afterend', '<div class="diet-wrap"><button type="button" class="diet-btn" id="dietBtn"></button><div class="diet-list" id="dietList"></div></div>');
    const btn = $('dietBtn'), list = $('dietList');
    const paint = () => {
      btn.innerHTML = `<span>${esc(sel.selectedOptions[0].textContent)}</span><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>`;
      list.innerHTML = [...sel.options].map(o => `<div class="diet-item${o.value === sel.value ? ' on' : ''}" data-v="${o.value}">${esc(o.textContent)}</div>`).join('');
    };
    btn.onclick = e => { e.stopPropagation(); list.classList.toggle('open'); btn.classList.toggle('open'); };
    list.onclick = e => {
      const it = e.target.closest('.diet-item'); if (!it) return;
      sel.value = it.dataset.v; updatePrefSummary(); paint(); list.classList.remove('open'); btn.classList.remove('open');
    };
    document.addEventListener('click', () => { list.classList.remove('open'); btn.classList.remove('open'); });
    paint();
  }

  // ---------- โหมด Developer ต้องใส่รหัสผ่าน (ป้องกันแบบหน้าเว็บ ไม่ใช่ความปลอดภัยจริง) ----------
  const origToggleDev = toggleDevMode;
  toggleDevMode = function () {
    if (STATE.dev) return origToggleDev();
    $('devPw').value = ''; $('devErr').textContent = '';
    toggleModal('devModal', true); setTimeout(() => $('devPw').focus(), 50);
  };
  window.submitDevPw = async function () {   // ตรวจรหัสที่ backend (ไม่ฝังรหัสไว้ในหน้าเว็บ)
    try {
      const r = await fetch(`${API_BASE}/api/dev/unlock`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({password: $('devPw').value})});
      if (r.ok) {
        try { localStorage.setItem('wet_dev_token', (await r.json()).token); } catch (e) { /* ไม่เก็บค่า */ }
        toggleModal('devModal', false); origToggleDev();
      } else {
        $('devErr').textContent = (await r.json().catch(() => ({}))).detail || 'รหัสผ่านไม่ถูกต้อง';
        $('devPw').select();
      }
    } catch (e) { $('devErr').textContent = 'เชื่อมต่อ backend ไม่ได้'; }
  };
  // เปิดหน้าใหม่ขณะจำโหมด Developer ไว้ แต่โทเค็นหมดอายุ (เซิร์ฟเวอร์รีสตาร์ท) → ปิดโหมดให้
  setTimeout(() => { if (STATE.dev) fetch(`${API_BASE}/api/dev/check`, {headers: devHeaders()}).then(r => r.json()).then(j => { if (!j.ok) setDevMode(false); }).catch(() => {}); }, 1500);

  // ---------- ติดตั้งปุ่ม/หน้าต่าง ----------
  makeModal('savedModal', 'แผนของฉัน', 'แผนที่บันทึกไว้ในเบราว์เซอร์นี้');
  makeModal('compareModal', 'เปรียบเทียบอัลกอริทึม', 'Greedy · Genetic Algorithm · Hybrid บนโจทย์เดียวกัน');
  document.body.insertAdjacentHTML('beforeend', '<div class="modal" id="devModal"><div class="modal-backdrop" data-close></div><div class="modal-card dev-modal-card"><div class="modal-title">โหมด Developer</div><div class="modal-sub">กรอกรหัสผ่านเพื่อเข้าใช้งาน</div><input type="password" id="devPw" placeholder="รหัสผ่าน" autocomplete="off" onkeydown="if(event.keyCode===13)submitDevPw()"><div class="dev-err" id="devErr"></div><button class="pareto-use" onclick="submitDevPw()">เข้าสู่โหมด Developer</button></div></div>');
  $('devModal').querySelectorAll('[data-close]').forEach(b => b.onclick = () => toggleModal('devModal', false));
  initTips();
  initDietSelect();
  document.querySelector('.topbar-actions')?.insertAdjacentHTML('afterbegin', '<a class="icon-btn results-link dev-only" href="results.html" title="ผลการทดลอง" style="text-decoration:none;font-size:.8rem;width:auto;padding:0 .7rem">ผลทดลอง</a>');
  document.querySelector('.topbar-actions')?.insertAdjacentHTML('afterbegin', '<button class="icon-btn saved-btn" onclick="openSaved()" title="แผนที่บันทึกไว้">★</button>');
  document.querySelector('.detail-actions')?.insertAdjacentHTML('afterbegin',
    '<button class="reshuffle-btn export-btn" onclick="savePlan()" title="บันทึกแผนนี้ไว้ในเบราว์เซอร์">★ บันทึก</button>' +
    '<span class="hist-group"><button type="button" class="reshuffle-btn export-btn hist-btn disabled" id="undoBtn" onclick="undoEdit()" title="ย้อนกลับ (Ctrl+Z)"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14L4 9l5-5M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/></svg></button>' +
    '<button type="button" class="reshuffle-btn export-btn hist-btn disabled" id="redoBtn" onclick="redoEdit()" title="เดินหน้า (Ctrl+Y)"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14l5-5-5-5M20 9H9.5a5.5 5.5 0 0 0 0 11H13"/></svg></button></span>' +
    '<button class="reshuffle-btn export-btn dev-only" onclick="openCompare()" title="เทียบ Greedy / GA / Hybrid บนโจทย์เดียวกัน">⇄ เทียบอัลกอริทึม</button>');
})();
