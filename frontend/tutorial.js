// Tutorial สำหรับผู้ใช้ครั้งแรก และผู้ที่กลับมาใช้หลังไม่ได้เข้า 30 วัน — ปุ่ม "?" บนแถบบนเปิดดูซ้ำได้
// ใช้ localStorage (ถ้าใช้ไม่ได้ เช่น โหมดส่วนตัว จะแสดงทุกครั้งที่เปิดหน้า ไม่ทำให้หน้าพัง)
(function () {
  const DAY = 86400000, RETURN_AFTER = 30 * DAY;
  const get = k => { try { return +localStorage.getItem(k) || 0; } catch (e) { return 0; } };
  const set = (k, v) => { try { localStorage.setItem(k, String(v)); } catch (e) { /* ไม่เก็บค่า */ } };
  const en = () => window.WET_LANG === 'en';
  const now = Date.now(), lastVisit = get('wet_last_visit'), doneAt = get('wet_tut_done');
  set('wet_last_visit', now);
  const due = !doneAt || (lastVisit && now - lastVisit > RETURN_AFTER);   // ครั้งแรก หรือห่างหายเกิน 30 วัน
  let detailDue = due, el = null, idx = 0, steps = [], onEnd = null;

  const FORM = [
    {th: ['ยินดีต้อนรับสู่ WeEasyTrip', 'ระบบช่วยวางแผนเที่ยวไทยตามงบประมาณและเวลาของคุณ ใช้เวลาเพียงไม่กี่ขั้นตอน ลองดูวิธีใช้สั้นๆ กัน'], en: ['Welcome to WeEasyTrip', 'Plan a Thailand trip around your budget and time in a few steps. Here is a quick tour.']},
    {sel: '#provSelect', th: ['1. เลือกจังหวัด', 'มีให้เลือกครบ 77 จังหวัด ภาพด้านบนจะเปลี่ยนตามจังหวัดที่เลือก'], en: ['1. Pick a province', 'All 77 provinces are available. The banner changes with your choice.']},
    {sel: '#dateRange', th: ['2. เลือกวันเดินทาง', 'เลือกวันเริ่มและวันสิ้นสุด ระบบจะแสดงพยากรณ์อากาศจริงให้ถ้าอยู่ในช่วง 16 วันข้างหน้า'], en: ['2. Choose your dates', 'Pick start and end dates. A real weather forecast appears if within the next 16 days.']},
    {sel: '#budget', th: ['3. ใส่งบประมาณ', 'งบรวมของทริป ระบบจะจัดแผนให้ไม่เกินงบนี้ และเสนอ 3 ระดับ: ประหยัด มาตรฐาน พรีเมียม'], en: ['3. Set your budget', 'Total trip budget. Plans stay within it, in 3 tiers: Budget, Standard, Premium.']},
    {sel: '#prefToggle', th: ['4. บอกความชอบ (ไม่บังคับ)', 'เลือกประเภทสถานที่ที่ชอบหรือไม่ต้องการ และอาหารมังสวิรัติ/ฮาลาล'], en: ['4. Tell us your tastes (optional)', 'Choose place types you like or want to avoid, and vegetarian/halal food.']},
    {sel: '#searchBtn', th: ['5. กดค้นหา', 'ระบบจะสร้างแผน 3 แบบให้เลือก เมื่อได้แล้วจะมีวิธีใช้ส่วนถัดไปให้ดูอีกครั้ง'], en: ['5. Search', 'You get 3 plans to choose from. A second short tour appears once you open a plan.']},
  ];
  const DETAIL = [
    {sel: '#dayPanels .poi-item', th: ['ลากการ์ดเพื่อเรียงลำดับ', 'กดค้างที่การ์ดสถานที่แล้วลากไปวางที่ใหม่หรือย้ายไปวันอื่น ช่องว่างสีแดงจางๆ คือจุดที่จะวาง ถ้าเวลาไม่พอหรือร้านปิด การ์ดจะเป็นสีแดงพร้อมคำอธิบาย'], en: ['Drag cards to reorder', 'Press and drag a card to a new spot or another day. The faint red gap shows where it will land. If a stop does not fit (e.g. closed), the card turns red with an explanation.']},
    {sel: '#dayPanels .btn-swap', th: ['เปลี่ยนหรือลบสถานที่', 'กดปุ่มสลับเพื่อเลือกสถานที่อื่นแทน หรือถังขยะเพื่อลบ ระบบคำนวณเวลาและค่าใช้จ่ายใหม่ให้ทันที'], en: ['Swap or remove a stop', 'Use swap to pick another place, or the bin to remove it. Times and costs update instantly.']},
    {sel: '#dayToggles', th: ['ดูเส้นทางบนแผนที่', 'หมายเลขบนแผนที่คือลำดับสถานที่ของแต่ละวัน แต่ละวันมีสีต่างกัน และเส้นประคือเส้นทางที่เดินทางระหว่างจุด กดปุ่มวันเพื่อดูเฉพาะวันนั้น แสดงทุกวัน หรือซ่อนทุกวัน'], en: ['Read the map route', 'Numbers on the map show the order of stops each day, with one colour per day and dashed lines for the route between them. Tap a day chip to see only that day, or show/hide all days.']},
    {sel: '.map-wrap', th: ['คลิกหมุดเพื่อดูรายละเอียด', 'กดหมุดบนแผนที่เพื่อดูชื่อสถานที่ เวลาเปิด-ปิด และรีวิว หมุดสีส้มที่มีรูปเตียงคือโรงแรมที่พัก'], en: ['Tap a pin for details', 'Tap a pin to see the place name, opening hours and reviews. The orange bed pin is your hotel.']},
    {sel: '.detail-actions', th: ['บันทึก แชร์ และส่งออก', 'บันทึกแผนไว้ในเบราว์เซอร์ ดูทางเลือกอื่นของทริป แชร์ลิงก์ให้เพื่อนแก้ร่วมกัน หรือส่งออกเป็นปฏิทินและ PDF'], en: ['Save, share and export', 'Save the plan, see alternatives, share a link for friends to edit together, or export to calendar and PDF.']},
  ];

  function resetLanding() { document.querySelectorAll('.landing-screen').forEach(e => { e.scrollTop = 0; e.scrollLeft = 0; }); }
  function close(finished) { resetLanding(); el?.remove(); el = null; window.removeEventListener('resize', placeSoon); window.removeEventListener('scroll', placeSoon, true); if (finished) onEnd?.(); }
  function build() {
    el = document.createElement('div'); el.className = 'tut';
    el.innerHTML = '<div class="tut-spot"></div><div class="tut-card"><div class="tut-title"></div><div class="tut-text"></div><div class="tut-foot"><span class="tut-dots"></span><span class="tut-btns"><button class="tut-skip"></button><button class="tut-prev"></button><button class="tut-next"></button></span></div></div>';
    document.body.appendChild(el);
    el.querySelector('.tut-skip').onclick = () => close(true);
    el.querySelector('.tut-prev').onclick = () => go(idx - 1);
    el.querySelector('.tut-next').onclick = () => (idx + 1 >= steps.length ? close(true) : go(idx + 1));
    window.addEventListener('resize', placeSoon); window.addEventListener('scroll', placeSoon, true);
  }
  function go(i) {
    idx = Math.max(0, Math.min(steps.length - 1, i)); const s = steps[idx], t = s[en() ? 'en' : 'th'];
    const target = s.sel && document.querySelector(s.sel);
    if (target && target.offsetParent !== null) { const r = target.getBoundingClientRect(); if (r.top < 80 || r.bottom > window.innerHeight - 80) window.scrollBy({top: r.top - window.innerHeight / 3, behavior: 'smooth'}); }   // ไม่ใช้ scrollIntoView: .landing-screen เป็น overflow:hidden จะถูกเลื่อนภายในจนเลื่อนกลับไม่ได้
    el.querySelector('.tut-title').textContent = t[0]; el.querySelector('.tut-text').textContent = t[1];
    el.querySelector('.tut-dots').innerHTML = steps.map((_, k) => `<i class="${k === idx ? 'on' : ''}"></i>`).join('');
    el.querySelector('.tut-skip').textContent = en() ? 'Skip' : 'ข้าม'; el.querySelector('.tut-prev').textContent = en() ? 'Back' : 'ก่อนหน้า';
    el.querySelector('.tut-prev').style.visibility = idx ? 'visible' : 'hidden';
    el.querySelector('.tut-next').textContent = idx + 1 >= steps.length ? (en() ? 'Got it' : 'เริ่มใช้งาน') : (en() ? 'Next' : 'ถัดไป');
    place(); el.classList.add('ready');   // วางตำแหน่งทันที (เลื่อนหน้าจอ: placeSoon จัดตำแหน่งซ้ำระหว่างเลื่อน)
  }
  let raf = 0;
  function placeSoon() { if (!raf) raf = requestAnimationFrame(() => { raf = 0; place(); }); }
  function place() {
    if (!el) return; const s = steps[idx], target = s.sel && document.querySelector(s.sel), spot = el.querySelector('.tut-spot'), card = el.querySelector('.tut-card');
    if (!target || target.offsetParent === null) { spot.style.cssText = 'display:none'; card.style.cssText = ''; card.classList.add('center'); el.classList.add('dim'); return; }
    el.classList.remove('dim');
    card.classList.remove('center');
    const r = target.getBoundingClientRect(), pad = 8;
    spot.style.cssText = `display:block;top:${r.top - pad}px;left:${r.left - pad}px;width:${r.width + pad * 2}px;height:${r.height + pad * 2}px`;
    const cw = Math.min(340, window.innerWidth - 24), below = r.bottom + 16 + 190 < window.innerHeight;
    card.style.top = below ? `${r.bottom + 16}px` : `${Math.max(12, r.top - 16 - card.offsetHeight)}px`;
    card.style.left = `${Math.max(12, Math.min(window.innerWidth - cw - 12, r.left + r.width / 2 - cw / 2))}px`; card.style.width = cw + 'px';
  }
  function start(list, end) { resetLanding(); if (el) close(false); steps = list; idx = 0; onEnd = end; build(); go(0); }
  window.startTutorial = () => start(FORM, () => set('wet_tut_done', Date.now()));

  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('themeBtn')?.insertAdjacentHTML('beforebegin', '<button class="icon-btn" id="helpBtn" title="วิธีใช้" style="font-weight:700">?</button>');
    document.getElementById('helpBtn').onclick = () => { detailDue = true; window.startTutorial(); };
    if (due) setTimeout(window.startTutorial, 1200);
  });
  // เปิดแผนครั้งแรกในรอบนี้ → แสดงวิธีใช้ส่วนรายละเอียดแผน
  const wrap = () => {
    if (typeof renderDetail !== 'function') return setTimeout(wrap, 300);
    const orig = renderDetail;
    renderDetail = function (pkg) {
      orig(pkg);
      if (detailDue && !el) { detailDue = false; setTimeout(() => start(DETAIL, null), 900); }
    };
  };
  wrap();
})();
