// tooltip แบบ minimal แทนกล่องสีดำของเบราว์เซอร์: ตอน hover ย้าย title ไปเป็นกล่องของเราชั่วคราว และคืน title ตอนเมาส์ออก (ให้ระบบแปลภาษายังใช้ title ได้)
(function () {
  let tip = null, cur = null, saved = '', held = [];   // held = [element, title] ของ title ที่ถอดไว้ชั่วคราว (รวมของ element แม่ ไม่ให้กล่องของเบราว์เซอร์ซ้อนขึ้นมา)
  const hide = () => { tip?.classList.remove('show'); held.forEach(([e, t]) => e.setAttribute('title', t)); held = []; cur = null; saved = ''; };
  document.addEventListener('mouseover', e => {
    const el = e.target.closest?.('[title]');
    if (!el || el === cur) return;
    hide(); const t = el.getAttribute('title'); if (!t) return;
    cur = el; saved = t;
    for (let e = el; e && e !== document.body; e = e.parentElement) { const tt = e.getAttribute('title'); if (tt) { held.push([e, tt]); e.removeAttribute('title'); } }
    if (!tip) { tip = document.createElement('div'); tip.className = 'wet-tip'; document.body.appendChild(tip); }
    tip.textContent = t; tip.style.left = '0px'; tip.style.top = '0px';
    const r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
    const above = r.top - h - 8 >= 6;
    tip.style.top = `${above ? r.top - h - 8 : r.bottom + 8}px`;
    tip.style.left = `${Math.max(6, Math.min(window.innerWidth - w - 6, r.left + r.width / 2 - w / 2))}px`;
    tip.classList.add('show');
  });
  document.addEventListener('mouseout', e => { if (cur && !cur.contains(e.relatedTarget)) hide(); });
  document.addEventListener('scroll', hide, true); document.addEventListener('mousedown', hide);
})();
