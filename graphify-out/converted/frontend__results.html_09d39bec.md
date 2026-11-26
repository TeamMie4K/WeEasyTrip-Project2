<!-- converted from frontend__results.html.docx -->

คู่มือโค้ด: frontend/results.html
หน้าแสดงผลการทดลอง (results.html)
ไฟล์ต้นฉบับ: frontend/results.html (124 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: หน้าเว็บอิสระที่แสดงผลการทดลองของ Project 2 เป็นกราฟแท่งและตาราง ดึงข้อมูลจากไฟล์ results.json ซึ่งสร้างโดย ➜ experiments/make_results_json.py จากผลของสคริปต์ทดลองต่าง ๆ (➜ experiments/run_experiments.py ➜ experiments/run_ils_experiments.py ➜ experiments/run_rl_experiments.py ➜ experiments/run_pareto_experiments.py ➜ experiments/run_sparse_experiments.py) หน้านี้เปิดจากปุ่ม "ผลทดลอง" ใน ➜ frontend/index.html (ปุ่มนั้นผูกในโค้ดของ ➜ frontend/app.js) ไฟล์นี้มี CSS และ JavaScript ฝังในตัวเอง ไม่ต้องพึ่ง ➜ frontend/style.css

บรรทัด 1–8  หัวเอกสาร
1  <!doctype html>
2  <html lang="th">
3  <head>
4  <meta charset="utf-8">
5  <meta name="viewport" content="width=device-width, initial-scale=1">
6  <title>ผลการทดลอง · WeEasyTrip</title>
7  <link rel="preconnect" href="https://fonts.googleapis.com">
8  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sarabun:wght@400;500;600;700&display=swap" rel="stylesheet">
บรรทัด 1–5: ประกาศ HTML5 ภาษาไทย ชุดอักขระ และ viewport ให้แสดงบนมือถือพอดี
บรรทัด 6: ชื่อหน้า
บรรทัด 7–8: โหลดฟอนต์ Inter และ Sarabun จาก Google Fonts
บรรทัด 9–46  สไตล์ที่ฝังในหน้า
9  <style>
10    :root { --bg:#fafaf9; --card:#fff; --text:#1c1917; --muted:#78716c; --line:#e7e5e4; --acc:#ff6d35; --y:#d6d3d1; --b:#94a3b8; --ok:#16a34a; --bad:#dc2626; }
11    :root[data-theme="dark"] { --bg:#0d0b09; --card:#17130f; --text:#faf5f0; --muted:#a8a29e; --line:#2a241e; --y:#57534e; --b:#78716c; }
12    * { box-sizing:border-box; }
13    body { margin:0; background:var(--bg); color:var(--text); font-family:'Sarabun','Inter',system-ui,sans-serif; line-height:1.6; }
14    main { max-width:980px; margin:0 auto; padding:28px 20px 80px; }
15    a.back { color:var(--muted); text-decoration:none; font-size:.9rem; } a.back:hover { color:var(--acc); }
16    h1 { font-size:2rem; font-weight:800; letter-spacing:-.02em; margin:14px 0 2px; }
17    h2 { font-size:1.15rem; font-weight:700; margin:0 0 2px; }
18    .sub, .muted { color:var(--muted); font-size:.88rem; }
19    section { margin-top:44px; }
20    .sec-head { margin-bottom:16px; }
21    .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; margin-top:22px; }
22    .stat { background:var(--card); border:1px solid var(--line); border-radius:18px; padding:18px 20px; }
23    .stat b { display:block; font-size:2.1rem; font-weight:800; color:var(--acc); line-height:1.1; letter-spacing:-.02em; }
24    .stat span { color:var(--muted); font-size:.85rem; }
25    .card { background:var(--card); border:1px solid var(--line); border-radius:18px; padding:18px 20px; }
26    .grid2 { display:grid; grid-template-columns:repeat(auto-fit,minmax(380px,1fr)); gap:14px; }
27    .legend { display:flex; gap:16px; font-size:.82rem; color:var(--muted); margin:0 0 12px; flex-wrap:wrap; }
28    .legend i { display:inline-block; width:10px; height:10px; border-radius:3px; margin-right:6px; vertical-align:-1px; }
29    .prov { font-weight:700; margin-bottom:10px; }
30    .sc { display:grid; grid-template-columns:34px 1fr; gap:10px; align-items:center; margin:12px 0; }
31    .sc > span { font-size:.78rem; color:var(--muted); font-weight:600; }
32    .bars { display:grid; gap:4px; }
33    .bar { height:11px; border-radius:6px; position:relative; min-width:3px; transition:width .5s; }
34    .bar i { position:absolute; left:calc(100% + 8px); top:-3px; font-style:normal; font-size:.72rem; color:var(--muted); white-space:nowrap; }
35    .bars { padding-right:54px; }
36    table { width:100%; border-collapse:collapse; font-size:.86rem; }
37    th, td { padding:9px 10px; text-align:right; border-bottom:1px solid var(--line); } th:first-child, td:first-child { text-align:left; }
38    th { color:var(--muted); font-weight:600; font-size:.78rem; text-transform:uppercase; letter-spacing:.04em; }
39    tr:last-child td { border-bottom:0; }
40    .win { color:var(--ok); font-weight:700; } .lose { color:var(--bad); font-weight:700; }
41    .pair { display:grid; grid-template-columns:96px 1fr 70px; gap:10px; align-items:center; margin:9px 0; font-size:.85rem; }
42    .track { height:10px; background:var(--line); border-radius:6px; overflow:hidden; } .track > div { height:100%; border-radius:6px; }
43    .note { margin-top:44px; padding:16px 20px; border-radius:14px; background:var(--card); border:1px dashed var(--line); color:var(--muted); font-size:.84rem; }
44    @media (max-width:640px){ .grid2 { grid-template-columns:1fr; } h1 { font-size:1.6rem; } }
45  </style>
46  </head>
บรรทัด 9: เปิดแท็ก style
บรรทัด 10–11: ตัวแปรสีของธีมสว่างและมืด (พื้น การ์ด ตัวอักษร เส้น สีเน้น สีแท่ง Greedy/GA ที่เป็นสีกลาง และสีชนะ/แพ้)
บรรทัด 12–14: รีเซ็ต box-sizing พื้นหลัง ฟอนต์ และจำกัดความกว้างเนื้อหา 980 พิกเซล
บรรทัด 15–20: ลิงก์กลับ หัวเรื่อง ข้อความรอง และระยะห่างของแต่ละหัวข้อ
บรรทัด 21–26: การ์ดตัวเลขสรุป (stats) การ์ดทั่วไป และกริดสองคอลัมน์
บรรทัด 27–28: คำอธิบายสี (legend)
บรรทัด 29–35: ส่วนกราฟแท่งของคะแนน: ชื่อจังหวัด แถว สถานการณ์ และแท่ง (ตัวเลขท้ายแท่งวางด้วย position)
บรรทัด 36–40: ตาราง: ส่วนหัว ตัวอักษรชิดขวา คอลัมน์แรกชิดซ้าย และสีเขียว/แดงสำหรับชนะ/แพ้
บรรทัด 41–42: แถวเปรียบเทียบสองแท่ง (pair) และรางแท่ง (track)
บรรทัด 43: กล่องหมายเหตุท้ายหน้า
บรรทัด 44: จอแคบ (ไม่เกิน 640 พิกเซล): เปลี่ยนกริดเป็นคอลัมน์เดียว
บรรทัด 45–46: ปิดแท็ก style และ head
บรรทัด 47–84  โครงหน้า
47  <body>
48  <main>
49    <a class="back" href="index.html">← กลับหน้าวางแผนทริป</a>
50    <h1>ผลการทดลอง</h1>
51    <div class="sub" id="sub">กำลังโหลด…</div>
52    <div class="stats" id="stats"></div>
53
54    <section>
55      <div class="sec-head"><h2>คะแนนของแผน: Hybrid เทียบกับเส้นฐาน</h2><div class="muted">คะแนนเฉลี่ยของแผน ยิ่งสูงยิ่งดี · S1 = 3 วัน, S2 = 5 วัน, S3 = 7 วัน</div></div>
56      <div class="legend"><span><i style="background:var(--y)"></i>Greedy</span><span><i style="background:var(--b)"></i>Genetic Algorithm</span><span><i style="background:var(--acc)"></i>Hybrid</span></div>
57      <div class="grid2" id="scores"></div>
58    </section>
59
60    <section>
61      <div class="sec-head"><h2>ปรับแผนใหม่หลังผู้ใช้แก้</h2><div class="muted">สัดส่วนแผนที่ยังผ่านข้อจำกัด หลังลบ 2 จุดและสลับเข้า 1 จุด (รวม <span id="reN"></span> กรณี)</div></div>
62      <div class="card" id="reopt"></div>
63    </section>
64
65    <section>
66      <div class="sec-head"><h2>ส่วนประกอบของ Hybrid</h2><div class="muted">Insertion Local Search เพิ่มคะแนนเท่าไร และ Reinforcement Learning ช่วยหรือไม่</div></div>
67      <div class="grid2">
68        <div class="card"><h2 style="font-size:1rem">Insertion Local Search</h2><div class="muted" id="ilsSub" style="margin-bottom:8px"></div><div id="ils"></div></div>
69        <div class="card"><h2 style="font-size:1rem">Reinforcement Learning เป็น seed</h2><div class="muted" id="rlSub" style="margin-bottom:8px"></div><div id="rl"></div></div>
70      </div>
71    </section>
72
73    <section>
74      <div class="sec-head"><h2>ทางเลือกหลายเป้าหมาย (NSGA-II)</h2><div class="muted">ให้แผนทางเลือกจำนวนมากกว่าในเวลาที่น้อยกว่า</div></div>
75      <div class="card" style="overflow-x:auto"><table id="par"></table></div>
76    </section>
77
78    <section>
79      <div class="sec-head"><h2>จังหวัดข้อมูลน้อย</h2><div class="muted">คะแนน Hybrid เทียบ GA ในแต่ละพื้นที่</div></div>
80      <div class="card" style="overflow-x:auto"><table id="sp"></table></div>
81    </section>
82
83    <div class="note">แผนที่ผิดข้อจำกัดนับเป็นคะแนน 0 · ทุกตัวเลขรันภายใต้กติกา 6 จุดต่อวัน (เที่ยว 4 + อาหาร 2) · Greedy เป็นวิธีกำหนดแน่นอนจึงรันครั้งเดียวต่อชุด · รายละเอียดเต็ม วิธีทดลอง และข้อจำกัด อยู่ในรายงานบทที่ 4</div>
84  </main>
บรรทัด 47–48: เปิด body และ main
บรรทัด 49: ลิงก์กลับหน้าวางแผนทริป ➜ frontend/index.html
บรรทัด 50–52: หัวข้อ บรรทัดรองที่เติมข้อความตอนโหลดเสร็จ และที่ว่างของการ์ดตัวเลขสรุป
บรรทัด 54–58: หัวข้อคะแนน Hybrid เทียบกับเส้นฐาน (Greedy และ GA) พร้อมคำอธิบายสี และที่ว่างของกราฟแต่ละจังหวัด
บรรทัด 60–63: หัวข้อปรับแผนใหม่หลังผู้ใช้แก้ (เทียบการคำนวณค่าใช้จ่ายใหม่กับการปรับแผนด้วย Hybrid ตามที่ ➜ reoptimize() ใน backend/main.py ทำ)
บรรทัด 65–71: หัวข้อส่วนประกอบของ Hybrid: การ์ดสองใบสำหรับ Insertion Local Search (➜ algorithm/ils.py) และ RL เป็น seed (➜ algorithm/rl.py)
บรรทัด 73–76: หัวข้อทางเลือกหลายเป้าหมาย NSGA-II (➜ algorithm/pareto.py) พร้อมตารางที่เติมด้วย JavaScript
บรรทัด 78–81: หัวข้อจังหวัดข้อมูลน้อย พร้อมตาราง
บรรทัด 83: หมายเหตุว่าแผนที่ผิดข้อจำกัดนับเป็นคะแนน 0 และทุกตัวเลขรันภายใต้กติกา 6 จุดต่อวัน
บรรทัด 84: ปิด main
บรรทัด 85–90  สคริปต์: ธีมและฟังก์ชันช่วย
85  <script>
86  try { document.documentElement.dataset.theme = localStorage.getItem('theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); } catch (e) {}
87  const TH = {phuket:'ภูเก็ต', chiangmai:'เชียงใหม่', krabi:'กระบี่', samui:'เกาะสมุย', nongbualamphu:'หนองบัวลำภู', phichit:'พิจิตร', lamphun:'ลำพูน', nakhonnayok:'นครนายก', singburi:'สิงห์บุรี', kalasin:'กาฬสินธุ์', chaiyaphum:'ชัยภูมิ', loei:'เลย'};
88  const $ = id => document.getElementById(id), name = s => TH[s] || s;
89  const fmtP = p => p < 0.0001 ? '<0.0001' : p.toFixed(4), avg = a => a.reduce((s, x) => s + x, 0) / a.length;
90  const pair = (label, a, b, n, colA, colB) => `<div class="pair"><span>${label}</span><div><div class="track"><div style="width:${100 * a / n}%;background:${colA}"></div></div><div class="track" style="margin-top:3px"><div style="width:${100 * b / n}%;background:${colB}"></div></div></div><b style="font-size:.8rem;text-align:right">${a}→${b}</b></div>`;
บรรทัด 85: เปิดแท็ก script
บรรทัด 86: ตั้งธีมจากค่าที่เก็บใน localStorage ไม่มีก็ตามการตั้งค่าของระบบ (มืดหรือสว่าง) ถ้าผิดพลาดก็ข้าม ค่า theme ตัวเดียวกับที่ ➜ frontend/app.js เก็บ
บรรทัด 87: TH ตารางชื่อจังหวัดและพื้นที่ จาก slug เป็นชื่อไทย
บรรทัด 88: $ ย่อ getElementById และ name แปลง slug เป็นชื่อไทย (ถ้าไม่มีใช้ slug เดิม)
บรรทัด 89: fmtP จัดรูปค่า p (ถ้าน้อยกว่า 0.0001 แสดง "<0.0001") และ avg ค่าเฉลี่ย
บรรทัด 90: pair สร้าง HTML ของแถวเทียบสองแท่ง (แท่งบนค่า a แท่งล่างค่า b จากจำนวนรวม n)
บรรทัด 91–97  โหลดผลและตัวเลขสรุป
91  fetch('results.json', {cache: 'no-cache'}).then(r => r.json()).then(D => {
92    const rows = D.rows, ok = x => x > 0;
93    const winGA = rows.filter(r => r.Hybrid.score > r.GA.score && r.p_vs_ga < 0.01).length, winGr = rows.filter(r => r.Hybrid.score > r.Greedy.score).length;
94    const speed = avg(rows.map(r => r.GA.ms / r.Hybrid.ms)), valid = rows.reduce((s, r) => s + r.Hybrid.valid, 0), tot = rows.reduce((s, r) => s + r.Hybrid.n, 0);
95    $('sub').textContent = `4 จังหวัดหลัก × 3 สถานการณ์ = ${rows.length} ชุด · GA และ Hybrid รันชุดละ ${D.trials} รอบ`;
96    $('stats').innerHTML = [[`${winGA}/${rows.length}`, 'ชุดที่ Hybrid ชนะ GA อย่างมีนัยสำคัญ'], [`${winGr}/${rows.length}`, 'ชุดที่ Hybrid สูงกว่า Greedy'], [`${speed.toFixed(1)}×`, 'Hybrid เร็วกว่า GA โดยเฉลี่ย'], [`${valid}/${tot}`, 'แผน Hybrid ที่ผ่านข้อจำกัดครบ']]
97      .map(([b, t]) => `<div class="stat"><b>${b}</b><span>${t}</span></div>`).join('');
บรรทัด 91: ดึง results.json แบบไม่ใช้แคช แล้วเริ่มวาดทั้งหน้าเมื่อได้ข้อมูล D
บรรทัด 92: rows แถวผลของแต่ละชุด
บรรทัด 93: นับชุดที่ Hybrid ชนะ GA อย่างมีนัยสำคัญ (p < 0.01) และชุดที่สูงกว่า Greedy
บรรทัด 94: คำนวณอัตราเร็ว (เวลา GA ÷ เวลา Hybrid) จำนวนแผนที่ผ่านข้อจำกัด และจำนวนแผนทั้งหมด
บรรทัด 95: เขียนบรรทัดรอง: จำนวนชุดและจำนวนรอบทดลอง
บรรทัด 96–97: วาดการ์ดตัวเลขสรุปทั้งหมด
บรรทัด 99–101  กราฟคะแนนต่อจังหวัด
99    const max = Math.max(...rows.flatMap(r => [r.Greedy.score, r.GA.score, r.Hybrid.score])), col = {Greedy: 'var(--y)', GA: 'var(--b)', Hybrid: 'var(--acc)'};
100    $('scores').innerHTML = ['phuket', 'chiangmai', 'krabi', 'samui'].map(p => `<div class="card"><div class="prov">${name(p)}</div>` + rows.filter(r => r.province === p).map(r =>
101      `<div class="sc"><span>${r.scenario.slice(0, 2)}</span><div class="bars">${['Greedy', 'GA', 'Hybrid'].map(a => `<div class="bar" style="width:${100 * r[a].score / max}%;background:${col[a]}"><i>${r[a].score.toFixed(0)}</i></div>`).join('')}</div></div>`).join('') + '</div>').join('');
บรรทัด 99: หาคะแนนสูงสุดเพื่อใช้ปรับสเกลแท่ง และกำหนดสีของแต่ละอัลกอริทึม
บรรทัด 100–101: สำหรับ 4 จังหวัดหลัก วาดการ์ด: แต่ละสถานการณ์มีสามแท่ง (Greedy GA Hybrid) ความกว้างตามสัดส่วนของคะแนนสูงสุด พร้อมตัวเลข
บรรทัด 103–106  ปรับแผนใหม่หลังแก้
103    const re = D.reopt, N = re.reduce((s, r) => s + r.n, 0); $('reN').textContent = N;
104    const sum = k => re.reduce((s, r) => s + r[k], 0);
105    $('reopt').innerHTML = pair('ผ่านข้อจำกัด', sum('recompute_valid'), sum('reoptimize_valid'), N, 'var(--y)', 'var(--acc)') + pair('มีมื้อครบทุกวัน', sum('recompute_meals'), sum('reoptimize_meals'), N, 'var(--y)', 'var(--acc)') +
106      '<div class="muted" style="margin-top:6px">แถบบน = คำนวณค่าใช้จ่ายใหม่แบบเดิม · แถบล่าง = ปรับแผนด้วย Hybrid</div>';
บรรทัด 103: อ่านผลการปรับแผนใหม่ รวมจำนวนแผนทั้งหมดและแสดงในหัวข้อ
บรรทัด 104: sum รวมค่าตามคีย์ที่ระบุ
บรรทัด 105–106: วาดสองแถวเทียบ (ผ่านข้อจำกัด และมีมื้อครบทุกวัน) แถบบนคือคำนวณค่าใช้จ่ายใหม่แบบเดิม แถบล่างคือปรับด้วย Hybrid
บรรทัด 108–113  ส่วนประกอบของ Hybrid
108    const gains = D.ils.map(x => x.gain);
109    $('ilsSub').textContent = `เพิ่มคะแนน ${Math.min(...gains).toFixed(1)}–${Math.max(...gains).toFixed(1)}% (มีนัยสำคัญ ${D.ils.filter(x => x.p < 0.05).length}/${D.ils.length} ชุด) แลกกับเวลาเพิ่ม ${(D.ils.reduce((s, x) => s + x.ms_ils, 0) / D.ils.reduce((s, x) => s + x.ms_base, 0)).toFixed(1)} เท่า`;
110    $('ils').innerHTML = ['phuket', 'chiangmai', 'krabi', 'samui'].map(p => { const g = avg(D.ils.filter(x => x.province === p).map(x => x.gain)); return `<div class="pair" style="grid-template-columns:90px 1fr 60px"><span>${name(p)}</span><div class="track"><div style="width:${Math.min(100, g * 14)}%;background:var(--acc)"></div></div><b style="text-align:right;font-size:.8rem">+${g.toFixed(1)}%</b></div>`; }).join('');
111    const sig = D.rl.filter(x => x.p < 0.05).length, better = D.rl.filter(x => x.hybrid_rl > x.hybrid).length;
112    $('rlSub').textContent = `ดีกว่า Hybrid อย่างมีนัยสำคัญเพียง ${sig}/${D.rl.length} ชุด (สูงกว่าเล็กน้อย ${better} ชุด) จึงไม่นำมาใช้เป็นค่าเริ่มต้น`;
113    $('rl').innerHTML = ['phuket', 'chiangmai', 'krabi', 'samui'].map(p => { const r = D.rl.filter(x => x.province === p), d = avg(r.map(x => x.hybrid_rl - x.hybrid)); return `<div class="pair" style="grid-template-columns:90px 1fr 70px"><span>${name(p)}</span><div class="track"><div style="width:${Math.min(100, Math.abs(d) * 60 + 2)}%;background:var(--b)"></div></div><b style="text-align:right;font-size:.8rem">${d >= 0 ? '+' : ''}${d.toFixed(2)}</b></div>`; }).join('') + '<div class="muted">ผลต่างคะแนนเฉลี่ย Hybrid+RL − Hybrid</div>';
บรรทัด 108–110: ILS: หาช่วงเปอร์เซ็นต์ที่เพิ่ม และนับชุดที่มีนัยสำคัญ แล้ววาดค่าเฉลี่ยของแต่ละจังหวัด
บรรทัด 111–113: RL: นับชุดที่ดีกว่าอย่างมีนัยสำคัญและชุดที่สูงกว่าเล็กน้อย แล้ววาดผลต่างเฉลี่ยของแต่ละจังหวัด
บรรทัด 115–116  ตาราง NSGA-II
115    $('par').innerHTML = '<tr><th>จังหวัด</th><th>แผนทางเลือก NSGA-II</th><th>แผนทางเลือก Hybrid</th><th>เวลา NSGA-II</th><th>เวลา Hybrid</th><th>คุณภาพรวม (hypervolume)</th></tr>' +
116      D.pareto.map(r => `<tr><td>${name(r.province)}</td><td><b>${r.plans_nsga.toFixed(0)}</b></td><td>${r.plans_ws.toFixed(0)}</td><td>${(r.ms_nsga / 1000).toFixed(1)} วินาที</td><td>${(r.ms_ws / 1000).toFixed(1)} วินาที</td><td class="${r.ratio > 1 && r.p < 0.05 ? 'win' : r.ratio < 1 ? 'lose' : ''}">${r.ratio.toFixed(2)}× ${r.ratio > 1 && r.p < 0.05 ? '(ดีกว่า)' : r.ratio < 1 ? '(ต่ำกว่า)' : '(ใกล้เคียง)'}</td></tr>`).join('');
บรรทัด 115–116: ส่วนหัวตาราง (จำนวนแผน เวลา และคุณภาพของทั้งสองวิธี) และแถวของแต่ละจังหวัดจากผล Pareto
บรรทัด 118–120  ตารางจังหวัดข้อมูลน้อย
118    $('sp').innerHTML = '<tr><th>พื้นที่</th><th>ร้านอาหาร</th>' + ['S1', 'S2', 'S3'].map(s => `<th>${s} Hybrid / GA</th>`).join('') + '</tr>' +
119      D.sparse.S1.map((r, i) => `<tr><td>${name(r.area)}</td><td>${r.rest}</td>` + ['S1', 'S2', 'S3'].map(s => { const x = D.sparse[s][i], w = x.Hybrid > x.GA && x.p < 0.05; return `<td class="${w ? 'win' : 'lose'}">${x.Hybrid.toFixed(0)} / ${x.GA.toFixed(0)}</td>`; }).join('') + '</tr>').join('') +
120      '<tr><td colspan="5" class="muted" style="text-align:left">สีเขียว = Hybrid สูงกว่า GA อย่างมีนัยสำคัญ · สีแดง = ไม่ใช่ (พิจิตรมีร้านอาหาร 8 ร้านจึงไม่พอสำหรับทริป 5–7 วัน)</td></tr>';
บรรทัด 118–120: ตารางพื้นที่ จำนวนร้านอาหาร และคะแนน Hybrid/GA ของสถานการณ์ S1 S2 S3 โดยเซลล์เป็นสีเขียวถ้า Hybrid ชนะอย่างมีนัยสำคัญ ไม่ก็สีแดง และท้ายตารางมีคำอธิบายสี
บรรทัด 121–124  จัดการข้อผิดพลาด
121  }).catch(e => { $('sub').textContent = 'โหลดข้อมูลผลทดลองไม่สำเร็จ: ' + e.message + ' (ต้องเปิดผ่านเซิร์ฟเวอร์ ไม่ใช่เปิดไฟล์ตรงๆ)'; });
122  </script>
123  </body>
124  </html>
บรรทัด 121: ถ้าโหลดไม่สำเร็จ แสดงข้อความผิดพลาด (ต้องเปิดผ่านเซิร์ฟเวอร์ ไม่ใช่เปิดไฟล์ตรง ๆ)
บรรทัด 122–124: ปิด script body และ html

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/ils.py
algorithm/pareto.py
algorithm/rl.py
backend/main.py
experiments/make_results_json.py
experiments/run_experiments.py
experiments/run_ils_experiments.py
experiments/run_pareto_experiments.py
experiments/run_rl_experiments.py
experiments/run_sparse_experiments.py
frontend/app.js
frontend/index.html
frontend/style.css