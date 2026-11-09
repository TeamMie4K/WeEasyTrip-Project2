// สลับภาษาไทย/อังกฤษ: แปลข้อความบนหน้าด้วยพจนานุกรม + รูปแบบ (regex) ที่ DOM แล้วเฝ้าดูการเปลี่ยนแปลง
// shortcut: ครอบคลุมเมนูหลัก ปุ่ม ข้อความแจ้งเตือน และป้ายในแผน — ข้อความที่ไม่อยู่ในพจนานุกรมจะแสดงเป็นภาษาไทยเหมือนเดิม
(function () {
  let lang = 'th';
  try { lang = localStorage.getItem('wet_lang') || 'th'; } catch (e) { /* ใช้ค่าเริ่มต้น */ }
  window.WET_LANG = lang;
  const D = {
    // หน้าแรก / ฟอร์ม
    'วางแผนเที่ยวไทยได้ง่ายๆ': 'Plan your Thailand trip with ease',
    'ระบบ AI หาเส้นทางที่ดีที่สุดภายใต้งบประมาณ เวลา และช่วงเวลาเปิด-ปิดของแต่ละสถานที่': 'AI finds the best route within your budget, time and each place’s opening hours',
    'วางแผนทริป': 'Plan your trip', 'ความชอบ': 'Preferences', 'จังหวัด': 'Province', 'งบประมาณ': 'Budget', 'บาท': 'THB',
    'โหมด Developer: เลือกอัลกอริทึมเองได้ (Greedy / GA / Hybrid)': 'Developer mode: choose the algorithm yourself (Greedy / GA / Hybrid)', 'เลือกช่วงวันเดินทาง...': 'Select travel dates...', 'เร็วสุด': 'Fastest', 'แนะนำ': 'Recommended',
    'Hybrid + RL seed (ทดลอง)': 'Hybrid + RL seed (experimental)', 'บันทึกแผนนี้ไว้ในเบราว์เซอร์': 'Save this plan in the browser', 'เทียบ Greedy / GA / Hybrid บนโจทย์เดียวกัน': 'Compare Greedy / GA / Hybrid on the same problem',
    'พยากรณ์จริงจาก Open-Meteo': 'Live forecast from Open-Meteo', 'ลากเพื่อเรียงลำดับหรือย้ายไปวันอื่น': 'Drag to reorder or move to another day', 'เปลี่ยน': 'Change', 'รีเซ็ตตำแหน่ง': 'Reset position',
    'Hybrid (แนะนำ): Greedy seed → GA refine → 2-opt local search': 'Hybrid (recommended): Greedy seed → GA refine → 2-opt local search',
    'ช่วงวันเดินทาง': 'Travel dates', 'จำนวนคน': 'Guests', 'ที่พัก': 'Accommodation', 'ค้นหา': 'Search', 'กำลังคำนวณ...': 'Calculating...',
    'รวมค่าโรงแรมในงบประมาณ': 'Include hotel in budget', 'ไม่รวมค่าโรงแรม': 'Hotel not included',
    'หักค่าโรงแรมออกจากงบก่อนวางแผนกิจกรรม': 'Hotel cost is deducted from the budget first',
    'ระบบจะหักค่าโรงแรมออกจากงบก่อนวางแผนกิจกรรม': 'Hotel cost is deducted from the budget first',
    'เลือกวันเช็คอินและเช็คเอาต์': 'Select check-in and check-out dates', 'กรุณาเลือกช่วงวันเดินทาง': 'Please select your travel dates',
    'อาหาร': 'Diet', 'ไม่จำกัด': 'No restriction', 'มังสวิรัติ': 'Vegetarian', 'ฮาลาล': 'Halal',
    'ใช้เท่าที่มีข้อมูลในฐานข้อมูล (OSM) ถ้าร้านไม่พอจะเสริมร้านทั่วไปและแจ้งเตือน': 'Uses what is in the OpenStreetMap data; if there are too few matching places, regular restaurants are added with a notice',
    'เที่ยวต่อจังหวัดข้างเคียง:': 'Add nearby provinces:', 'อัลกอริทึม': 'Algorithm',
    'พร้อมใช้งาน': 'Ready', 'ข้อมูลน้อย': 'Limited data', 'เร็วๆ นี้': 'Soon', 'ค้นหาจังหวัด...': 'Search province...', 'ค้นหาสถานที่...': 'Search places...',
    'ภาคเหนือ': 'North', 'ภาคกลาง': 'Central', 'ภาคตะวันออก': 'East', 'ภาคตะวันตก': 'West', 'ภาคตะวันออกเฉียงเหนือ': 'Northeast', 'ภาคอีสาน': 'Northeast', 'ภาคใต้': 'South', 'อื่น ๆ': 'Other',
    'หาด': 'Beach', 'วัด': 'Temple', 'จุดชมวิว': 'Viewpoint', 'วัฒนธรรม': 'Culture', 'ตลาด': 'Market', 'กิจกรรม': 'Activity', 'ร้านอาหาร': 'Restaurant', 'ทั้งหมด': 'All',
    'ชอบ': 'Like', 'ไม่ชอบ': 'Dislike', 'ยกเลิก "ชอบ"': 'Remove "like"', 'ยกเลิก "ไม่ชอบ"': 'Remove "dislike"',
    // แพ็กเกจ / รายละเอียด
    'เลือกแพ็กเกจที่คุณชอบ': 'Choose your package', 'ปรับแต่งทริปของคุณ': 'Customize your trip', 'แพ็กเกจ': 'Package',
    'กำลังวางแผนทริป...': 'Planning your trip...', 'กำลังวางแผนทริป 3 แบบ...': 'Planning 3 trip options...',
    'ไม่รวมที่พัก': 'No hotel', 'ค่าโรงแรม': 'Hotel', 'ค่ากิจกรรม': 'Activities', 'รวมทั้งหมด': 'Total', 'ค่าใช้จ่าย': 'Cost', 'รวมคะแนน': 'Total score',
    'งบไม่พอสำหรับแพ็กเกจนี้': 'Budget is too low for this package', 'ผ่านข้อจำกัด': 'Valid',
    'เพิ่มสถานที่': 'Add place', 'เพิ่มจุดใหม่': 'Add new place', 'เปลี่ยนสถานที่': 'Change place', 'ลบ': 'Remove', 'รีเซ็ต': 'Reset',
    'แสดงทุกวัน': 'Show all days', 'ซ่อนทุกวัน': 'Hide all days', 'แชร์': 'Share', 'ปฏิทิน': 'Calendar', 'ทางเลือก': 'Alternatives', 'เปิด': 'Opens', 'ทั้งวัน': 'All day', 'เปิดทั้งวัน': 'Open all day', 'ไม่ระบุ': 'N/A', 'ฟรี': 'Free', 'ไม่เสียค่าเข้า': 'Free entry',
    'เวลาเปิด-ปิด': 'Opening hours', 'เวลาถึงตามแผน': 'Planned arrival', 'ดูรายละเอียดและรีวิว': 'Details and reviews', 'ข้อมูลจำลอง': 'Sample data',
    'สุ่มสถานที่ใหม่ด้วย algorithm เดิม': 'Reshuffle places with the same algorithm', 'พิมพ์หรือบันทึกเป็น PDF': 'Print or save as PDF',
    'ดาวน์โหลดไฟล์ปฏิทิน (.ics) เปิดใน Google Calendar / Apple / Outlook': 'Download a calendar file (.ics) for Google Calendar / Apple / Outlook',
    'สร้างลิงก์ให้เพื่อนเปิดดูและแก้แผนเดียวกัน': 'Create a link so friends can view and edit the same plan',
    'ดูทางเลือกที่แลกเปลี่ยนกันระหว่างคะแนน ความหลากหลาย และระยะทาง (NSGA-II)': 'See trade-offs between score, variety and distance (NSGA-II)',
    'ทางเลือกที่แลกเปลี่ยนกัน (Pareto)': 'Trade-off alternatives (Pareto)', 'แต่ละแผนไม่มีแผนอื่นที่ดีกว่าในทุกด้านพร้อมกัน — เลือกตามที่คุณให้ความสำคัญ': 'No plan beats another on every measure — pick what matters to you',
    'ปิด': 'Close', 'แผน': 'Plan', 'คะแนน': 'Score', 'หมวด/วัน': 'Categories/day', 'ระยะทาง (km)': 'Distance (km)', 'ค่าใช้จ่าย (฿)': 'Cost (฿)', 'ใช้แผนนี้': 'Use this plan',
    '★ บันทึก': '★ Save', '⇄ เทียบอัลกอริทึม': '⇄ Compare algorithms', 'แผนของฉัน': 'My plans', 'แผนที่บันทึกไว้': 'Saved plans', 'แผนที่บันทึกไว้ในเบราว์เซอร์นี้': 'Plans saved in this browser',
    'เปิดแผนที่บันทึกไว้แล้ว': 'Saved plan opened', 'ผลทดลอง': 'Results', 'ผลการทดลอง': 'Experiment results', 'เทียบอัลกอริทึม': 'Compare algorithms',
    'เปรียบเทียบอัลกอริทึม': 'Algorithm comparison', 'Greedy · Genetic Algorithm · Hybrid บนโจทย์เดียวกัน': 'Greedy · Genetic Algorithm · Hybrid on the same problem',
    'อัลกอริทึม': 'Algorithm', 'คะแนนรวม': 'Total score', 'เวลาคำนวณ': 'Run time', 'ยังไม่มีแผนที่บันทึกไว้ — กดปุ่ม "บันทึก" ในหน้าปรับแต่งทริป': 'No saved plans yet — press "Save" on the trip page',
    'โหมด Developer': 'Developer mode', 'กรอกรหัสผ่านเพื่อเข้าใช้งาน': 'Enter the password to continue', 'เข้าสู่โหมด Developer': 'Enter Developer mode', 'รหัสผ่านไม่ถูกต้อง': 'Incorrect password',
    'เชื่อมต่อ backend ไม่ได้': 'Cannot reach the backend', 'รหัสผ่าน': 'Password',
    // ข้อความแจ้งเตือน
    'โหมด Developer: เลือกอัลกอริทึมได้': 'Developer mode: algorithm selection enabled', 'โหมดปกติ: ใช้ Hybrid': 'Normal mode: using Hybrid',
    'โหลดรายการจังหวัดไม่สำเร็จ': 'Could not load the province list', 'กำลังคำนวณเส้นทางใหม่...': 'Recalculating route...', 'กำลังปรับเส้นทางด้วย Hybrid...': 'Re-optimizing with Hybrid...',
    'กำลังสุ่มสถานที่ใหม่...': 'Reshuffling places...', 'ดาวน์โหลดไฟล์ปฏิทินแล้ว': 'Calendar file downloaded', 'เซสชันหมดอายุแล้ว': 'Session expired',
    'เพื่อนแก้ไขแผน — อัปเดตให้แล้ว': 'A friend edited the plan — updated', 'ลิงก์หมดอายุหรือไม่ถูกต้อง': 'Link expired or invalid',
    'กำลังหาทางเลือกที่ดีที่สุดในแต่ละด้าน...': 'Finding the best alternatives for each measure...', 'ไม่พบทางเลือกที่ผ่านข้อจำกัด ลองเพิ่มงบหรือลดความชอบ': 'No valid alternatives found — try a higher budget or fewer preferences',
    'บันทึกแผนแล้ว (เก็บในเบราว์เซอร์นี้ ได้สูงสุด 20 แผน)': 'Plan saved (kept in this browser, up to 20 plans)',
    'ไม่พบสถานที่ในร่มใกล้เคียงที่ยังไม่อยู่ในแผน': 'No nearby indoor places that are not already in the plan',
    'มีคนแก้ไขพร้อมกัน — ใช้ฉบับล่าสุดของเพื่อน': 'Edited at the same time — using your friend’s latest version',
    'คัดลอกลิงก์แล้ว — ส่งให้เพื่อนเพื่อวางแผนด้วยกัน': 'Link copied — send it to a friend to plan together',
    // สภาพอากาศ
    '☀️ ท้องฟ้าแจ่มใส': '☀️ Clear sky', '🌤️ มีเมฆบางส่วน': '🌤️ Partly cloudy', '☁️ เมฆมาก': '☁️ Overcast', '🌫️ หมอก': '🌫️ Fog', '🌦️ ฝนปรอย': '🌦️ Drizzle',
    '🌧️ ฝนตก': '🌧️ Rain', '🌧️ ฝนตกเป็นช่วง': '🌧️ Showers', '⛈️ พายุฝนฟ้าคะนอง': '⛈️ Thunderstorm',
  };
  Object.assign(D, {
    'ทางเลือกอื่นของทริปนี้': 'Other options for this trip', 'ทางเลือกอื่น': 'More options', 'ย้อนกลับ (Ctrl+Z)': 'Undo (Ctrl+Z)', 'เดินหน้า (Ctrl+Y)': 'Redo (Ctrl+Y)', 'ย้อนกลับแล้ว': 'Undone', 'ทำซ้ำแล้ว': 'Redone', '↺ คืนค่าเดิม': '↺ Restore original', 'คืนแผนกลับเป็นที่ระบบคำนวณให้ตอนแรก': 'Restore the plan the system first calculated', 'คืนแผนเดิมแล้ว': 'Original plan restored', 'ใช้เวลา': 'Duration', 'ตั้งแต่': 'From', 'เวลาที่ใช้ ณ สถานที่': 'Time spent at the place', 'ให้ระบบจัดลำดับและเวลาใหม่ให้ลงตัว (อาจถอดบางสถานที่ออกถ้าเวลาไม่พอ)': 'Let the system rearrange order and timing (may drop some places if time is short)', 'สถานที่': 'Places', 'ค่าใช้จ่าย': 'Cost', 'คะแนน': 'Score', 'สถานที่กลางแจ้ง อาจมีฝนตกได้': 'Outdoor place, it may rain',
    'เลือกแผนที่เน้นสิ่งที่คุณสนใจ เช่น ขับน้อย หลากหลาย หรือประหยัด — เทียบกับแผนที่คุณเปิดอยู่': 'Pick the plan that fits what you care about — less driving, more variety, or lower cost — compared with the plan you have open',
    'ดูแผนทางเลือก: ขับน้อย หลากหลาย หรือประหยัด': 'See alternatives: less driving, more variety, or cheaper',
    'แนะนำ': 'Recommended', 'ขับน้อยที่สุด': 'Least driving', 'หลากหลายที่สุด': 'Most variety', 'ประหยัดที่สุด': 'Cheapest', 'ทางเลือก': 'Alternative',
    'ได้สถานที่น่าสนใจโดยรวมสูงสุด': 'Best overall mix of attractions', 'เดินทางสั้น เหนื่อยน้อย ประหยัดค่าเดินทาง': 'Short trips, less tiring, lower travel cost',
    'ได้เที่ยวหลายประเภทในแต่ละวัน': 'Several kinds of places each day', 'ค่าใช้จ่ายรวมต่ำสุด': 'Lowest total cost',
    'อีกทางเลือกที่สมดุลระหว่างระยะทาง ความหลากหลายและค่าใช้จ่าย': 'A balanced option between distance, variety and cost',
    'ขับเฉลี่ย/วัน': 'Avg driving/day', 'ความหลากหลาย': 'Variety', 'ค่าใช้จ่าย/คน': 'Cost per person', 'เท่าแผนปัจจุบัน': 'Same as current', 'ใช้แผนนี้': 'Use this plan',
    'วิธีใช้': 'How to use', 'ผลทดลอง': 'Results', 'ผลการทดลอง': 'Experiment results'
  });
  const P = [
    [/^วันที่ (\d+)$/, 'Day $1'], [/^วัน (\d+) \((\d+)\)$/, 'Day $1 ($2)'], [/^วันที่ (\d+) · ลำดับ (\d+)$/, 'Day $1 · Stop $2'],
    [/^(\d+) วัน (\d+) คืน$/, '$1 days $2 nights'], [/(\d+) วัน (\d+) คืน/, '$1 days $2 nights'],
    [/^งบ ([\d,]+) ฿ · (\d+) วัน · (\d+) คน/, 'Budget $1 ฿ · $2 days · $3 guests'],
    [/^(\d+) นาที$/, '$1 min'], [/^(\d+) รีวิว$/, '$1 reviews'], [/^เปิด (.+)$/, 'Opens $1'], [/ค่าใช้จ่าย ([\d,]+) บาท/, 'Cost $1 THB'],
    [/^สร้าง (\d+) แพ็กเกจสำเร็จ$/, '$1 packages created'], [/^ผิดพลาด: (.+)$/, 'Error: $1'],
    [/^ปรับแผนใหม่แล้ว! Score (.+)$/, 'Plan re-optimized! Score $1'], [/^สุ่มใหม่แล้ว! Score (.+)$/, 'Reshuffled! Score $1'], [/^อัปเดต! Score (.+)$/, 'Updated! Score $1'],
    [/^(?:ปรับ|อัปเดต)แล้ว · (\d+) คำเตือน$/, 'Updated · $1 warnings'], [/^ใช้แผนทางเลือกที่ (\d+)$/, 'Using alternative plan $1'],
    [/^ชอบ (\d+)$/, 'Like $1'], [/^ไม่ชอบ (\d+)$/, 'Dislike $1'], [/^เพิ่มในวันที่ (\d+)$/, 'Add to day $1'],
    [/^ข้อมูลรองรับสูงสุด (\d+) วันสำหรับ (.+)$/, 'Data supports up to $1 days for $2'],
    [/^ข้อมูลของ (.+) รองรับสูงสุด (\d+) วัน .*$/, 'Data for $1 supports up to $2 days (not enough places or restaurants for more). Reduce the days or add a nearby province'],
    [/^(\d+) สถานที่ (\d+) โรงแรม — ตัวเลือกอาจน้อย$/, '$1 places, $2 hotels — fewer options'],
    [/^จังหวัดนี้มีข้อมูลสถานที่น้อย แผน(\w+)มี (\d+) วันที่ไม่มีกิจกรรม.*$/, 'Limited data for this province: the $1 plan has $2 day(s) without activities. Try fewer days or another province'],
    [/^เลือกได้ไม่เกิน 7 วัน.*$/, 'Up to 7 days — only 7 days will be used'],
    [/^สลับ (\d+) จุดเป็นสถานที่ในร่มแล้ว.*$/, 'Swapped $1 outdoor stop(s) for indoor places, re-routing...'],
    [/^☔ วันนี้โอกาสฝน (\d+)% แต่มีสถานที่กลางแจ้ง (\d+) จุด$/, '☔ $1% chance of rain today but $2 outdoor stop(s)'],
    [/^สลับเป็นสถานที่ในร่ม$/, 'Swap for indoor places'], [/^ฝน (\d+)%$/, 'Rain $1%'],
    [/^เข้าร่วมแผนที่เพื่อนแชร์มา.*$/, 'Joined a friend’s shared plan — edits are shared live'],
    [/^เข้าร่วมไม่ได้: (.+)$/, 'Could not join: $1'], [/^แชร์ไม่สำเร็จ: (.+)$/, 'Share failed: $1'],
  ];
  const nameMap = () => { const m = {}; Object.values((typeof STATE !== 'undefined' && STATE.provinces) || {}).forEach(p => { if (p.name_th && p.name_en) m[p.name_th] = p.name_en; }); return m; };
  function tr(s) {
    const t = s.trim(); if (!t) return s;
    const lead = s.slice(0, s.indexOf(t)), tail = s.slice(s.indexOf(t) + t.length);
    let out = D[t];
    if (out === undefined) { const nm = nameMap(); if (nm[t]) out = nm[t]; else if (t.includes(' + ') && t.split(' + ').every(x => nm[x])) out = t.split(' + ').map(x => nm[x]).join(' + '); }
    if (out === undefined) for (const [re, rep] of P) if (re.test(t)) { out = t.replace(re, rep); break; }
    out = inline(out === undefined ? t : out);
    return out === t ? s : lead + out + tail;
  }
  // แปลงส่วนย่อยในประโยค: คำทั่วไป + ชื่อจังหวัด/สถานที่/โรงแรมเป็นชื่ออังกฤษ
  const INL = [[/(\d+) สถานที่ · (\d+) โรงแรม/, '$1 places · $2 hotels'], [/รวมคะแนน · (\d+) จุด/, 'Total score · $1 places'], [/ฝน (\d+)%/g, 'Rain $1%'], [/เปิด (?=\d)/g, 'Open '], [/(\d) บาท/g, '$1 THB'], [/ บาท$/, ' THB'], [/(\d+) นาที/g, '$1 min'], [/(\d+) จุด/g, '$1 stops']];
  let nmCache = null, nmKey = '';
  function inline(t) {
    if (!/[฀-๿]/.test(t)) return t;
    for (const [re, rep] of INL) t = t.replace(re, rep);
    if (/[฀-๿]/.test(t) && typeof STATE !== 'undefined') {
      const key = STATE.pois.length + ':' + STATE.hotels.length + ':' + Object.keys(STATE.provinces).length;
      if (key !== nmKey) {
        nmKey = key; const m = nameMap();
        [...STATE.pois, ...STATE.hotels].forEach(p => { if (p.name_th && p.name_en) m[p.name_th] = p.name_en; });
        nmCache = Object.entries(m).sort((a, b) => b[0].length - a[0].length);
      }
      for (const [th, en] of nmCache) if (t.includes(th)) t = t.split(th).join(en);
    }
    return t;
  }
  const orig = new WeakMap(), shown = new WeakMap();
  function apply(node) {
    if (node.nodeType === 3) {
      if (!/[฀-๿]/.test(node.nodeValue) && !orig.has(node)) return;
      if (shown.get(node) !== node.nodeValue) orig.set(node, node.nodeValue);   // ข้อความใหม่จากแอป
      const base = orig.get(node), v = lang === 'en' ? tr(base) : base;
      if (node.nodeValue !== v) node.nodeValue = v;
      shown.set(node, v);
    } else if (node.nodeType === 1 && !['SCRIPT', 'STYLE'].includes(node.tagName)) {
      for (const a of ['title', 'placeholder']) {
        const k = 'data-th-' + a, cur = node.getAttribute(a);
        if (cur === null) continue;
        if (!node.hasAttribute(k) || node.getAttribute('data-en-' + a) !== cur) node.setAttribute(k, cur);   // ค่าใหม่ที่แอปตั้ง → จำเป็นต้นฉบับ
        const v = lang === 'en' ? tr(node.getAttribute(k)) : node.getAttribute(k);
        if (cur !== v) node.setAttribute(a, v);
        node.setAttribute('data-en-' + a, v);
      }
      node.childNodes.forEach(apply);
    }
  }
  let busy = false;
  const obs = new MutationObserver(muts => {
    if (busy) return; busy = true;
    muts.forEach(m => { if (m.type === 'characterData') apply(m.target); else if (m.type === 'attributes') apply(m.target); else m.addedNodes.forEach(apply); });
    busy = false;
  });
  function run() { busy = true; apply(document.body); busy = false; }
  window.setLang = function (l) {
    lang = l; window.WET_LANG = l; try { localStorage.setItem('wet_lang', l); } catch (e) { /* ไม่เก็บค่า */ }
    document.documentElement.lang = l; run();
    const b = document.getElementById('langBtn'); if (b) b.textContent = l === 'en' ? 'TH' : 'EN';
    window.dispatchEvent(new Event('wet-lang'));
  };
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.topbar-actions')?.insertAdjacentHTML('afterbegin', `<button class="icon-btn" id="langBtn" title="Language / ภาษา" style="font-size:.78rem;font-weight:700">${lang === 'en' ? 'TH' : 'EN'}</button>`);
    document.getElementById('langBtn').onclick = () => setLang(lang === 'en' ? 'th' : 'en');
    obs.observe(document.body, {childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['title', 'placeholder']});
    setTimeout(run, 400); setTimeout(run, 2500);
    document.documentElement.lang = lang;
  });
})();
