<!-- converted from frontend__i18n.js.docx -->

คู่มือโค้ด: frontend/i18n.js
สลับภาษาไทย/อังกฤษด้วยพจนานุกรมและ regex
ไฟล์ต้นฉบับ: frontend/i18n.js (160 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: แปลข้อความบนหน้าเว็บโดยไม่ต้องเขียนข้อความสองภาษาไว้ในโค้ดแต่ละที่: เก็บข้อความไทยเป็นต้นฉบับ แล้วแปลทับ DOM ด้วยพจนานุกรม (D) รูปแบบ regex (P) และตารางชื่อจังหวัด สถานที่ โรงแรมที่อ่านจากตัวแปร STATE ใน ➜ frontend/app.js จากนั้นใช้ MutationObserver เฝ้าดูข้อความใหม่ที่แอปสร้างตอนทำงาน ปุ่ม EN/TH ถูกแทรกเข้าแถบบนของ ➜ frontend/index.html ภาษาที่เลือกเก็บใน localStorage และเปิดเป็นตัวแปร WET_LANG ให้ ➜ frontend/tutorial.js ➜ frontend/extras.js และ ➜ frontend/app.js อ่านได้ ทั้งนี้ข้อความที่ไม่อยู่ในพจนานุกรมจะแสดงเป็นภาษาไทยตามเดิม

บรรทัด 1–6  หัวไฟล์ และภาษาเริ่มต้น
1  // สลับภาษาไทย/อังกฤษ: แปลข้อความบนหน้าด้วยพจนานุกรม + รูปแบบ (regex) ที่ DOM แล้วเฝ้าดูการเปลี่ยนแปลง
2  // shortcut: ครอบคลุมเมนูหลัก ปุ่ม ข้อความแจ้งเตือน และป้ายในแผน — ข้อความที่ไม่อยู่ในพจนานุกรมจะแสดงเป็นภาษาไทยเหมือนเดิม
3  (function () {
4    let lang = 'th';
5    try { lang = localStorage.getItem('wet_lang') || 'th'; } catch (e) { /* ใช้ค่าเริ่มต้น */ }
6    window.WET_LANG = lang;
บรรทัด 1–2: คอมเมนต์อธิบายหน้าที่ และ shortcut ที่รู้ว่าข้อความนอกพจนานุกรมไม่ถูกแปล
บรรทัด 3: เปิด IIFE
บรรทัด 4–5: ตั้งภาษาเริ่มต้นเป็นไทย แล้วอ่านภาษาที่เคยเลือกจาก localStorage (ถ้าใช้ไม่ได้ใช้ค่าเดิม)
บรรทัด 6: เปิดภาษาปัจจุบันเป็น window.WET_LANG
บรรทัด 7–61  พจนานุกรมหลัก
7    const D = {
8      // หน้าแรก / ฟอร์ม
9      'วางแผนเที่ยวไทยได้ง่ายๆ': 'Plan your Thailand trip with ease',
10      'ระบบ AI หาเส้นทางที่ดีที่สุดภายใต้งบประมาณ เวลา และช่วงเวลาเปิด-ปิดของแต่ละสถานที่': 'AI finds the best route within your budget, time and each place’s opening hours',
11      'วางแผนทริป': 'Plan your trip', 'ความชอบ': 'Preferences', 'จังหวัด': 'Province', 'งบประมาณ': 'Budget', 'บาท': 'THB',
12      'โหมด Developer: เลือกอัลกอริทึมเองได้ (Greedy / GA / Hybrid)': 'Developer mode: choose the algorithm yourself (Greedy / GA / Hybrid)', 'เลือกช่วงวันเดินทาง...': 'Select travel dates...', 'เร็วสุด': 'Fastest', 'แนะนำ': 'Recommended',
13      'Hybrid + RL seed (ทดลอง)': 'Hybrid + RL seed (experimental)', 'บันทึกแผนนี้ไว้ในเบราว์เซอร์': 'Save this plan in the browser', 'เทียบ Greedy / GA / Hybrid บนโจทย์เดียวกัน': 'Compare Greedy / GA / Hybrid on the same problem',
14      'พยากรณ์จริงจาก Open-Meteo': 'Live forecast from Open-Meteo', 'ลากเพื่อเรียงลำดับหรือย้ายไปวันอื่น': 'Drag to reorder or move to another day', 'เปลี่ยน': 'Change', 'รีเซ็ตตำแหน่ง': 'Reset position',
15      'Hybrid (แนะนำ): Greedy seed → GA refine → 2-opt local search': 'Hybrid (recommended): Greedy seed → GA refine → 2-opt local search',
16      'ช่วงวันเดินทาง': 'Travel dates', 'จำนวนคน': 'Guests', 'ที่พัก': 'Accommodation', 'ค้นหา': 'Search', 'กำลังคำนวณ...': 'Calculating...',
17      'รวมค่าโรงแรมในงบประมาณ': 'Include hotel in budget', 'ไม่รวมค่าโรงแรม': 'Hotel not included',
18      'หักค่าโรงแรมออกจากงบก่อนวางแผนกิจกรรม': 'Hotel cost is deducted from the budget first',
19      'ระบบจะหักค่าโรงแรมออกจากงบก่อนวางแผนกิจกรรม': 'Hotel cost is deducted from the budget first',
20      'เลือกวันเช็คอินและเช็คเอาต์': 'Select check-in and check-out dates', 'กรุณาเลือกช่วงวันเดินทาง': 'Please select your travel dates',
21      'อาหาร': 'Diet', 'ไม่จำกัด': 'No restriction', 'มังสวิรัติ': 'Vegetarian', 'ฮาลาล': 'Halal',
22      'ใช้เท่าที่มีข้อมูลในฐานข้อมูล (OSM) ถ้าร้านไม่พอจะเสริมร้านทั่วไปและแจ้งเตือน': 'Uses what is in the OpenStreetMap data; if there are too few matching places, regular restaurants are added with a notice',
23      'อัลกอริทึม': 'Algorithm',
24      'พร้อมใช้งาน': 'Ready', 'ข้อมูลน้อย': 'Limited data', 'เร็วๆ นี้': 'Soon', 'ค้นหาจังหวัด...': 'Search province...', 'ค้นหาสถานที่...': 'Search places...',
25      'ภาคเหนือ': 'North', 'ภาคกลาง': 'Central', 'ภาคตะวันออก': 'East', 'ภาคตะวันตก': 'West', 'ภาคตะวันออกเฉียงเหนือ': 'Northeast', 'ภาคอีสาน': 'Northeast', 'ภาคใต้': 'South', 'อื่น ๆ': 'Other',
26      'หาด': 'Beach', 'วัด': 'Temple', 'จุดชมวิว': 'Viewpoint', 'วัฒนธรรม': 'Culture', 'ตลาด': 'Market', 'กิจกรรม': 'Activity', 'ร้านอาหาร': 'Restaurant', 'ทั้งหมด': 'All',
27      'ชอบ': 'Like', 'ไม่ชอบ': 'Dislike', 'ยกเลิก "ชอบ"': 'Remove "like"', 'ยกเลิก "ไม่ชอบ"': 'Remove "dislike"',
28      // แพ็กเกจ / รายละเอียด
29      'เลือกแพ็กเกจที่คุณชอบ': 'Choose your package', 'ปรับแต่งทริปของคุณ': 'Customize your trip', 'แพ็กเกจ': 'Package',
30      'กำลังวางแผนทริป...': 'Planning your trip...', 'กำลังวางแผนทริป 3 แบบ...': 'Planning 3 trip options...',
31      'ไม่รวมที่พัก': 'No hotel', 'ค่าโรงแรม': 'Hotel', 'ค่ากิจกรรม': 'Activities', 'รวมทั้งหมด': 'Total', 'ค่าใช้จ่าย': 'Cost', 'รวมคะแนน': 'Total score',
32      'งบไม่พอสำหรับแพ็กเกจนี้': 'Budget is too low for this package', 'ผ่านข้อจำกัด': 'Valid',
33      'เพิ่มสถานที่': 'Add place', 'เพิ่มจุดใหม่': 'Add new place', 'เปลี่ยนสถานที่': 'Change place', 'ลบ': 'Remove', 'รีเซ็ต': 'Reset',
34      'แสดงทุกวัน': 'Show all days', 'ซ่อนทุกวัน': 'Hide all days', 'แชร์': 'Share', 'ปฏิทิน': 'Calendar', 'ทางเลือก': 'Alternatives', 'เปิด': 'Opens', 'ทั้งวัน': 'All day', 'เปิดทั้งวัน': 'Open all day', 'ไม่ระบุ': 'N/A', 'ฟรี': 'Free', 'ไม่เสียค่าเข้า': 'Free entry',
35      'เวลาเปิด-ปิด': 'Opening hours', 'เวลาถึงตามแผน': 'Planned arrival', 'ดูรายละเอียดและรีวิว': 'Details and reviews', 'ข้อมูลจำลอง': 'Sample data', 'ระดับดาว': 'Star rating', 'ราคาต่อคืน': 'Price per night',
36      'สุ่มสถานที่ใหม่ด้วย algorithm เดิม': 'Reshuffle places with the same algorithm', 'พิมพ์หรือบันทึกเป็น PDF': 'Print or save as PDF',
37      'ดาวน์โหลดไฟล์ปฏิทิน (.ics) เปิดใน Google Calendar / Apple / Outlook': 'Download a calendar file (.ics) for Google Calendar / Apple / Outlook',
38      'สร้างลิงก์ให้เพื่อนเปิดดูและแก้แผนเดียวกัน': 'Create a link so friends can view and edit the same plan',
39      'ดูทางเลือกที่แลกเปลี่ยนกันระหว่างคะแนน ความหลากหลาย และระยะทาง (NSGA-II)': 'See trade-offs between score, variety and distance (NSGA-II)',
40      'ทางเลือกที่แลกเปลี่ยนกัน (Pareto)': 'Trade-off alternatives (Pareto)', 'แต่ละแผนไม่มีแผนอื่นที่ดีกว่าในทุกด้านพร้อมกัน — เลือกตามที่คุณให้ความสำคัญ': 'No plan beats another on every measure — pick what matters to you',
41      'ปิด': 'Close', 'แผน': 'Plan', 'คะแนน': 'Score', 'หมวด/วัน': 'Categories/day', 'ระยะทาง (km)': 'Distance (km)', 'ค่าใช้จ่าย (฿)': 'Cost (฿)', 'ใช้แผนนี้': 'Use this plan',
42      '★ บันทึก': '★ Save', '⇄ เทียบอัลกอริทึม': '⇄ Compare algorithms', 'แผนของฉัน': 'My plans', 'แผนที่บันทึกไว้': 'Saved plans', 'แผนที่บันทึกไว้ในเบราว์เซอร์นี้': 'Plans saved in this browser',
43      'เปิดแผนที่บันทึกไว้แล้ว': 'Saved plan opened', 'ผลทดลอง': 'Results', 'ผลการทดลอง': 'Experiment results', 'เทียบอัลกอริทึม': 'Compare algorithms',
44      'เปรียบเทียบอัลกอริทึม': 'Algorithm comparison', 'Greedy · Genetic Algorithm · Hybrid บนโจทย์เดียวกัน': 'Greedy · Genetic Algorithm · Hybrid on the same problem',
45      'อัลกอริทึม': 'Algorithm', 'คะแนนรวม': 'Total score', 'เวลาคำนวณ': 'Run time', 'ยังไม่มีแผนที่บันทึกไว้ — กดปุ่ม "บันทึก" ในหน้าปรับแต่งทริป': 'No saved plans yet — press "Save" on the trip page',
46      'โหมด Developer': 'Developer mode', 'กรอกรหัสผ่านเพื่อเข้าใช้งาน': 'Enter the password to continue', 'เข้าสู่โหมด Developer': 'Enter Developer mode', 'รหัสผ่านไม่ถูกต้อง': 'Incorrect password',
47      'เชื่อมต่อ backend ไม่ได้': 'Cannot reach the backend', 'รหัสผ่าน': 'Password',
48      // ข้อความแจ้งเตือน
49      'โหมด Developer: เลือกอัลกอริทึมได้': 'Developer mode: algorithm selection enabled', 'โหมดปกติ: ใช้ Hybrid': 'Normal mode: using Hybrid',
50      'โหลดรายการจังหวัดไม่สำเร็จ': 'Could not load the province list', 'กำลังคำนวณเส้นทางใหม่...': 'Recalculating route...', 'กำลังปรับเส้นทางด้วย Hybrid...': 'Re-optimizing with Hybrid...',
51      'กำลังสุ่มสถานที่ใหม่...': 'Reshuffling places...', 'ดาวน์โหลดไฟล์ปฏิทินแล้ว': 'Calendar file downloaded', 'เซสชันหมดอายุแล้ว': 'Session expired',
52      'เพื่อนแก้ไขแผน — อัปเดตให้แล้ว': 'A friend edited the plan — updated', 'ลิงก์หมดอายุหรือไม่ถูกต้อง': 'Link expired or invalid',
53      'กำลังหาทางเลือกที่ดีที่สุดในแต่ละด้าน...': 'Finding the best alternatives for each measure...', 'ไม่พบทางเลือกที่ผ่านข้อจำกัด ลองเพิ่มงบหรือลดความชอบ': 'No valid alternatives found — try a higher budget or fewer preferences',
54      'บันทึกแผนแล้ว (เก็บในเบราว์เซอร์นี้ ได้สูงสุด 20 แผน)': 'Plan saved (kept in this browser, up to 20 plans)',
55      'ไม่พบสถานที่ในร่มใกล้เคียงที่ยังไม่อยู่ในแผน': 'No nearby indoor places that are not already in the plan',
56      'มีคนแก้ไขพร้อมกัน — ใช้ฉบับล่าสุดของเพื่อน': 'Edited at the same time — using your friend’s latest version',
57      'คัดลอกลิงก์แล้ว — ส่งให้เพื่อนเพื่อวางแผนด้วยกัน': 'Link copied — send it to a friend to plan together',
58      // สภาพอากาศ
59      '☀️ ท้องฟ้าแจ่มใส': '☀️ Clear sky', '🌤️ มีเมฆบางส่วน': '🌤️ Partly cloudy', '☁️ เมฆมาก': '☁️ Overcast', '🌫️ หมอก': '🌫️ Fog', '🌦️ ฝนปรอย': '🌦️ Drizzle',
60      '🌧️ ฝนตก': '🌧️ Rain', '🌧️ ฝนตกเป็นช่วง': '🌧️ Showers', '⛈️ พายุฝนฟ้าคะนอง': '⛈️ Thunderstorm',
61    };
บรรทัด 7: ประกาศอ็อบเจ็กต์ D คีย์เป็นข้อความไทยตรงตัว ค่าเป็นข้อความอังกฤษ
บรรทัด 8–27: หมวดหน้าแรกและฟอร์ม: หัวเรื่อง ป้ายช่องกรอก งบประมาณ โหมด Developer อัลกอริทึม วันเดินทาง อาหาร จังหวัด ภาค และประเภทสถานที่
บรรทัด 28–47: หมวดแพ็กเกจและหน้ารายละเอียด: ค่าใช้จ่าย ปุ่มเพิ่ม/เปลี่ยน/ลบ/แชร์/ปฏิทิน ข้อความเวลาเปิด-ปิด Pareto ผลทดลอง และแผนที่บันทึก
บรรทัด 48–57: หมวดข้อความแจ้งเตือน (toast) เช่น กำลังคำนวณ บันทึกแล้ว ลิงก์หมดอายุ
บรรทัด 58–60: หมวดสภาพอากาศพร้อมอีโมจิ
บรรทัด 61: ปิดอ็อบเจ็กต์
บรรทัด 62–72  พจนานุกรมส่วนเพิ่ม
62    Object.assign(D, {
63      'ประวัติการแจ้งเตือน': 'Notification history', 'ล้างทั้งหมด': 'Clear all', 'ยังไม่มีการแจ้งเตือน': 'No notifications yet', 'ทางเลือกอื่นของทริปนี้': 'Other options for this trip', 'ทางเลือกอื่น': 'More options', 'ย้อนกลับ (Ctrl+Z)': 'Undo (Ctrl+Z)', 'เดินหน้า (Ctrl+Y)': 'Redo (Ctrl+Y)', 'ย้อนกลับแล้ว': 'Undone', 'ทำซ้ำแล้ว': 'Redone', '↺ คืนค่าเดิม': '↺ Restore original', 'คืนแผนกลับเป็นที่ระบบคำนวณให้ตอนแรก': 'Restore the plan the system first calculated', 'คืนแผนเดิมแล้ว': 'Original plan restored', 'ใช้เวลา': 'Duration', 'ตั้งแต่': 'From', 'เวลาที่ใช้ ณ สถานที่': 'Time spent at the place', 'ให้ระบบจัดลำดับและเวลาใหม่ให้ลงตัว (อาจถอดบางสถานที่ออกถ้าเวลาไม่พอ)': 'Let the system rearrange order and timing (may drop some places if time is short)', 'สถานที่': 'Places', 'ค่าใช้จ่าย': 'Cost', 'คะแนน': 'Score', 'สถานที่กลางแจ้ง อาจมีฝนตกได้': 'Outdoor place, it may rain',
64      'เลือกแผนที่เน้นสิ่งที่คุณสนใจ เช่น ขับน้อย หลากหลาย หรือประหยัด — เทียบกับแผนที่คุณเปิดอยู่': 'Pick the plan that fits what you care about — less driving, more variety, or lower cost — compared with the plan you have open',
65      'ดูแผนทางเลือก: ขับน้อย หลากหลาย หรือประหยัด': 'See alternatives: less driving, more variety, or cheaper',
66      'แนะนำ': 'Recommended', 'ขับน้อยที่สุด': 'Least driving', 'หลากหลายที่สุด': 'Most variety', 'ประหยัดที่สุด': 'Cheapest', 'ทางเลือก': 'Alternative',
67      'ได้สถานที่น่าสนใจโดยรวมสูงสุด': 'Best overall mix of attractions', 'เดินทางสั้น เหนื่อยน้อย ประหยัดค่าเดินทาง': 'Short trips, less tiring, lower travel cost',
68      'ได้เที่ยวหลายประเภทในแต่ละวัน': 'Several kinds of places each day', 'ค่าใช้จ่ายรวมต่ำสุด': 'Lowest total cost',
69      'อีกทางเลือกที่สมดุลระหว่างระยะทาง ความหลากหลายและค่าใช้จ่าย': 'A balanced option between distance, variety and cost',
70      'ขับเฉลี่ย/วัน': 'Avg driving/day', 'ความหลากหลาย': 'Variety', 'ค่าใช้จ่าย/คน': 'Cost per person', 'เท่าแผนปัจจุบัน': 'Same as current', 'ใช้แผนนี้': 'Use this plan',
71      'วิธีใช้': 'How to use', 'ผลทดลอง': 'Results', 'ผลการทดลอง': 'Experiment results'
72    });
บรรทัด 62–72: Object.assign เติมคำของฟีเจอร์ที่เพิ่มภายหลัง: ประวัติการแจ้งเตือน แผนทางเลือก (ขับน้อย หลากหลาย ประหยัด) และคำเทียบเปอร์เซ็นต์
บรรทัด 73–92  รูปแบบ regex
73    const P = [
74      [/^วันที่ (\d+)$/, 'Day $1'], [/^วัน (\d+) \((\d+)\)$/, 'Day $1 ($2)'], [/^วันที่ (\d+) · ลำดับ (\d+)$/, 'Day $1 · Stop $2'],
75      [/^(\d+) วัน (\d+) คืน$/, '$1 days $2 nights'], [/(\d+) วัน (\d+) คืน/, '$1 days $2 nights'],
76      [/^งบ ([\d,]+) ฿ · (\d+) วัน · (\d+) คน/, 'Budget $1 ฿ · $2 days · $3 guests'],
77      [/^(\d+) นาที$/, '$1 min'], [/^(\d+) รีวิว$/, '$1 reviews'], [/^เปิด (.+)$/, 'Opens $1'], [/ค่าใช้จ่าย ([\d,]+) บาท/, 'Cost $1 THB'],
78      [/^สร้าง (\d+) แพ็กเกจสำเร็จ$/, '$1 packages created'], [/^ผิดพลาด: (.+)$/, 'Error: $1'],
79      [/^ปรับแผนใหม่แล้ว! Score (.+)$/, 'Plan re-optimized! Score $1'], [/^สุ่มใหม่แล้ว! Score (.+)$/, 'Reshuffled! Score $1'], [/^อัปเดต! Score (.+)$/, 'Updated! Score $1'],
80      [/^(?:ปรับ|อัปเดต)แล้ว · (\d+) คำเตือน$/, 'Updated · $1 warnings'], [/^ใช้แผนทางเลือกที่ (\d+)$/, 'Using alternative plan $1'],
81      [/^ชอบ (\d+)$/, 'Like $1'], [/^ไม่ชอบ (\d+)$/, 'Dislike $1'], [/^เพิ่มในวันที่ (\d+)$/, 'Add to day $1'],
82      [/^ข้อมูลรองรับสูงสุด (\d+) วันสำหรับ (.+)$/, 'Data supports up to $1 days for $2'],
83      [/^ข้อมูลของ (.+) รองรับสูงสุด (\d+) วัน .*$/, 'Data for $1 supports up to $2 days (not enough places or restaurants for more). Reduce the days or add a nearby province'],
84      [/^(\d+) สถานที่ (\d+) โรงแรม — ตัวเลือกอาจน้อย$/, '$1 places, $2 hotels — fewer options'],
85      [/^จังหวัดนี้มีข้อมูลสถานที่น้อย แผน(\w+)มี (\d+) วันที่ไม่มีกิจกรรม.*$/, 'Limited data for this province: the $1 plan has $2 day(s) without activities. Try fewer days or another province'],
86      [/^เลือกได้ไม่เกิน 7 วัน.*$/, 'Up to 7 days — only 7 days will be used'],
87      [/^สลับ (\d+) จุดเป็นสถานที่ในร่มแล้ว.*$/, 'Swapped $1 outdoor stop(s) for indoor places, re-routing...'],
88      [/^☔ วันนี้โอกาสฝน (\d+)% แต่มีสถานที่กลางแจ้ง (\d+) จุด$/, '☔ $1% chance of rain today but $2 outdoor stop(s)'],
89      [/^สลับเป็นสถานที่ในร่ม$/, 'Swap for indoor places'], [/^ฝน (\d+)%$/, 'Rain $1%'],
90      [/^เข้าร่วมแผนที่เพื่อนแชร์มา.*$/, 'Joined a friend’s shared plan — edits are shared live'],
91      [/^เข้าร่วมไม่ได้: (.+)$/, 'Could not join: $1'], [/^แชร์ไม่สำเร็จ: (.+)$/, 'Share failed: $1'],
92    ];
บรรทัด 73–92: P รายการคู่ [regex, ข้อความแทน] สำหรับข้อความที่มีตัวเลขหรือชื่อแทรก เช่น "วันที่ 2" → "Day 2" "งบ … ฿ · … วัน" ข้อความเตือนฝน ข้อจำกัดของข้อมูลจังหวัด และข้อความแชร์แผน ใช้ $1 $2 อ้างกลุ่มที่จับได้
บรรทัด 93–93  ตารางชื่อจังหวัด
93    const nameMap = () => { const m = {}; Object.values((typeof STATE !== 'undefined' && STATE.provinces) || {}).forEach(p => { if (p.name_th && p.name_en) m[p.name_th] = p.name_en; }); return m; };
บรรทัด 93: nameMap สร้างตาราง {ชื่อไทย: ชื่ออังกฤษ} ของทุกจังหวัดจาก STATE.provinces (ตัวแปรของ ➜ frontend/app.js) ถ้ายังไม่โหลดจะได้ตารางว่าง
บรรทัด 94–102  แปลข้อความหนึ่งก้อน
94    function tr(s) {
95      const t = s.trim(); if (!t) return s;
96      const lead = s.slice(0, s.indexOf(t)), tail = s.slice(s.indexOf(t) + t.length);
97      let out = D[t];
98      if (out === undefined) { const nm = nameMap(); if (nm[t]) out = nm[t]; }
99      if (out === undefined) for (const [re, rep] of P) if (re.test(t)) { out = t.replace(re, rep); break; }
100      out = inline(out === undefined ? t : out);
101      return out === t ? s : lead + out + tail;
102    }
บรรทัด 94–96: tr ตัดช่องว่างหน้าท้ายออกไว้ก่อนแล้วประกอบกลับตอนท้าย ข้อความว่างคืนตามเดิม
บรรทัด 97: ลองหาในพจนานุกรม D ตรงตัวก่อน
บรรทัด 98: ถ้าไม่เจอ ลองหาชื่อจังหวัดในตารางชื่อ (nameMap)
บรรทัด 99: ถ้ายังไม่เจอ ลองไล่ regex ใน P จนตรงตัวแรก
บรรทัด 100: ส่งผลผ่าน inline เพื่อแปลส่วนย่อยที่เหลือ
บรรทัด 101: ถ้าผลไม่เปลี่ยนจากต้นฉบับ คืนข้อความเดิม ไม่ก็ใส่ช่องว่างหน้าท้ายกลับ
บรรทัด 103–119  แปลส่วนย่อยในประโยค
103    // แปลงส่วนย่อยในประโยค: คำทั่วไป + ชื่อจังหวัด/สถานที่/โรงแรมเป็นชื่ออังกฤษ
104    const INL = [[/(\d+) สถานที่ · (\d+) โรงแรม/, '$1 places · $2 hotels'], [/รวมคะแนน · (\d+) จุด/, 'Total score · $1 places'], [/ฝน (\d+)%/g, 'Rain $1%'], [/เปิด (?=\d)/g, 'Open '], [/(\d) บาท/g, '$1 THB'], [/ บาท$/, ' THB'], [/(\d+) นาที/g, '$1 min'], [/(\d+) จุด/g, '$1 stops']];
105    let nmCache = null, nmKey = '';
106    function inline(t) {
107      if (!/[฀-๿]/.test(t)) return t;
108      for (const [re, rep] of INL) t = t.replace(re, rep);
109      if (/[฀-๿]/.test(t) && typeof STATE !== 'undefined') {
110        const key = STATE.pois.length + ':' + STATE.hotels.length + ':' + Object.keys(STATE.provinces).length;
111        if (key !== nmKey) {
112          nmKey = key; const m = nameMap();
113          [...STATE.pois, ...STATE.hotels].forEach(p => { if (p.name_th && p.name_en) m[p.name_th] = p.name_en; });
114          nmCache = Object.entries(m).sort((a, b) => b[0].length - a[0].length);
115        }
116        for (const [th, en] of nmCache) if (t.includes(th)) t = t.split(th).join(en);
117      }
118      return t;
119    }
บรรทัด 103: คอมเมนต์อธิบาย
บรรทัด 104: INL รายการ regex แปลวลีสั้นที่ฝังในประโยคยาว (เช่น "N สถานที่ · M โรงแรม")
บรรทัด 105: ตัวแปรแคช nmCache และกุญแจ nmKey ของตารางชื่อ
บรรทัด 106–107: inline ถ้าไม่มีอักษรไทยเหลือ คืนทันที (ช่วงยูนิโค้ด 0E00–0E7F)
บรรทัด 108: ใช้ regex ในลิสต์ INL ทีละตัว
บรรทัด 109–110: ถ้ายังมีอักษรไทยและมี STATE สร้างกุญแจจากจำนวนสถานที่ โรงแรม จังหวัด เพื่อตรวจว่าข้อมูลเปลี่ยนหรือไม่
บรรทัด 111–115: ถ้ากุญแจเปลี่ยน สร้างตารางชื่อใหม่รวมจังหวัด สถานที่ โรงแรม แล้วเรียงชื่อยาวก่อน (กันชื่อสั้นไปทับชื่อยาว)
บรรทัด 116: แทนที่ชื่อไทยที่พบด้วยชื่ออังกฤษ
บรรทัด 118: คืนข้อความ
บรรทัด 120–139  แปลโหนดใน DOM
120    const orig = new WeakMap(), shown = new WeakMap();
121    function apply(node) {
122      if (node.nodeType === 3) {
123        if (!/[฀-๿]/.test(node.nodeValue) && !orig.has(node)) return;
124        if (shown.get(node) !== node.nodeValue) orig.set(node, node.nodeValue);   // ข้อความใหม่จากแอป
125        const base = orig.get(node), v = lang === 'en' ? tr(base) : base;
126        if (node.nodeValue !== v) node.nodeValue = v;
127        shown.set(node, v);
128      } else if (node.nodeType === 1 && !['SCRIPT', 'STYLE'].includes(node.tagName)) {
129        for (const a of ['title', 'placeholder']) {
130          const k = 'data-th-' + a, cur = node.getAttribute(a);
131          if (cur === null) continue;
132          if (!node.hasAttribute(k) || node.getAttribute('data-en-' + a) !== cur) node.setAttribute(k, cur);   // ค่าใหม่ที่แอปตั้ง → จำเป็นต้นฉบับ
133          const v = lang === 'en' ? tr(node.getAttribute(k)) : node.getAttribute(k);
134          if (cur !== v) node.setAttribute(a, v);
135          node.setAttribute('data-en-' + a, v);
136        }
137        node.childNodes.forEach(apply);
138      }
139    }
บรรทัด 120: orig เก็บข้อความไทยต้นฉบับของแต่ละโหนด shown เก็บข้อความที่แสดงล่าสุด (WeakMap ไม่กันหน่วยความจำ)
บรรทัด 121–122: apply ถ้าเป็นโหนดข้อความ
บรรทัด 123: ข้ามโหนดที่ไม่มีอักษรไทยและไม่เคยแปล
บรรทัด 124: ถ้าข้อความตอนนี้ไม่ใช่ที่เราเพิ่งแสดง แปลว่าแอปเขียนข้อความใหม่ ให้จำเป็นต้นฉบับ
บรรทัด 125–127: ถ้าเป็นภาษาอังกฤษแปลจากต้นฉบับ ไม่ก็ใช้ต้นฉบับ แล้วเขียนกลับเมื่อต่างจากเดิม และจดว่าแสดงอะไร
บรรทัด 128: ถ้าเป็นองค์ประกอบ (ไม่ใช่ script หรือ style)
บรรทัด 129–136: แปลแอตทริบิวต์ title และ placeholder แบบเดียวกัน โดยเก็บต้นฉบับไว้ใน data-th-* และค่าที่แสดงใน data-en-*
บรรทัด 137: ไล่ลูกทุกตัวซ้ำ
บรรทัด 138–139: ปิดเงื่อนไขและฟังก์ชัน
บรรทัด 140–146  เฝ้าดู DOM
140    let busy = false;
141    const obs = new MutationObserver(muts => {
142      if (busy) return; busy = true;
143      muts.forEach(m => { if (m.type === 'characterData') apply(m.target); else if (m.type === 'attributes') apply(m.target); else m.addedNodes.forEach(apply); });
144      busy = false;
145    });
146    function run() { busy = true; apply(document.body); busy = false; }
บรรทัด 140–145: obs MutationObserver: ถ้ากำลังแปลอยู่ (busy) ข้ามเพื่อไม่ให้วนไม่รู้จบ ไม่เช่นนั้นแปลโหนดที่ข้อความ แอตทริบิวต์ หรือโหนดที่เพิ่มเข้ามาเปลี่ยน
บรรทัด 146: run แปลทั้ง body
บรรทัด 147–152  สลับภาษา
147    window.setLang = function (l) {
148      lang = l; window.WET_LANG = l; try { localStorage.setItem('wet_lang', l); } catch (e) { /* ไม่เก็บค่า */ }
149      document.documentElement.lang = l; run();
150      const b = document.getElementById('langBtn'); if (b) b.textContent = l === 'en' ? 'TH' : 'EN';
151      window.dispatchEvent(new Event('wet-lang'));
152    };
บรรทัด 147–149: window.setLang ตั้งภาษา เก็บลง localStorage ตั้ง lang ของ html แล้วแปลทั้งหน้า
บรรทัด 150: เปลี่ยนข้อความปุ่มภาษาเป็นภาษาตรงข้าม
บรรทัด 151: ส่งเหตุการณ์ wet-lang ให้สคริปต์อื่นที่ต้องวาดใหม่ตามภาษา เช่นใน ➜ frontend/app.js และ ➜ frontend/extras.js
บรรทัด 153–160  เริ่มต้นเมื่อโหลดหน้า
153    document.addEventListener('DOMContentLoaded', () => {
154      document.querySelector('.topbar-actions')?.insertAdjacentHTML('afterbegin', `<button class="icon-btn" id="langBtn" title="Language / ภาษา" style="font-size:.78rem;font-weight:700">${lang === 'en' ? 'TH' : 'EN'}</button>`);
155      document.getElementById('langBtn').onclick = () => setLang(lang === 'en' ? 'th' : 'en');
156      obs.observe(document.body, {childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['title', 'placeholder']});
157      setTimeout(run, 400); setTimeout(run, 2500);
158      document.documentElement.lang = lang;
159    });
160  })();
บรรทัด 153: รอ DOMContentLoaded
บรรทัด 154: แทรกปุ่มภาษาไว้หน้าสุดของ .topbar-actions ใน ➜ frontend/index.html
บรรทัด 155: ผูกคลิกให้สลับภาษา
บรรทัด 156: เริ่ม observer ดูข้อความ แอตทริบิวต์ title/placeholder และโหนดใหม่
บรรทัด 157: แปลซ้ำหลัง 0.4 และ 2.5 วินาที เพื่อให้ครอบคลุมข้อมูลที่โหลดตามมา
บรรทัด 158: ตั้งภาษาของ html
บรรทัด 159–160: ปิด callback และ IIFE

ไฟล์ที่เชื่อมกับไฟล์นี้
frontend/app.js
frontend/extras.js
frontend/index.html
frontend/tutorial.js