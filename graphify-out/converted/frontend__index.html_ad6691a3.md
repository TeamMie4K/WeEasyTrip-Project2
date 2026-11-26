<!-- converted from frontend__index.html.docx -->

คู่มือโค้ด: frontend/index.html
หน้าหลักของเว็บ (index.html)
ไฟล์ต้นฉบับ: frontend/index.html (429 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: โครง HTML ของหน้าเว็บหลักทั้งหน้า: ฟอร์มวางแผน ส่วนแพ็กเกจ 3 แบบ ส่วนรายละเอียดแผนพร้อมแผนที่ หน้าต่างเปลี่ยนสถานที่ และหน้าต่างแผนทางเลือก ไฟล์นี้ไม่มีตรรกะเอง ปุ่มและช่องกรอกอ้างฟังก์ชันใน ➜ frontend/app.js ผ่านแอตทริบิวต์ onclick/onchange ส่วนสไตล์ทั้งหมดอยู่ใน ➜ frontend/style.css ท้ายไฟล์โหลดสคริปต์ ➜ frontend/app.js ➜ frontend/extras.js ➜ frontend/tutorial.js ➜ frontend/tooltip.js ➜ frontend/i18n.js ตามลำดับ และมีสคริปต์ย่อยจัดการเมนูเลือกจังหวัด ข้อมูลที่แสดงมาจาก ➜ backend/main.py ผ่านโค้ดใน app.js (ไฟล์นี้เองไม่เรียก API)

บรรทัด 1–14  หัวเอกสาร
1  <!DOCTYPE html>
2  <html lang="th" data-theme="light">
3  <head>
4    <meta charset="UTF-8" />
5    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
6    <title>WeEasyTrip</title>
7    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23ff6d35'/%3E%3Cpath d='M8 21l5-10 4 7 3-5 4 8z' fill='white'/%3E%3C/svg%3E" />
8    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
9    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
10    <link rel="preconnect" href="https://fonts.googleapis.com">
11    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
12    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sarabun:wght@400;500;600;700&display=swap" rel="stylesheet">
13    <link rel="stylesheet" href="style.css" />
14  </head>
บรรทัด 1–2: ประกาศ HTML5 ภาษาไทย และตั้งธีมเริ่มต้นเป็นสว่างด้วย data-theme (ปุ่มธีมเปลี่ยนค่านี้)
บรรทัด 3–6: ชุดอักขระ viewport และชื่อหน้า
บรรทัด 7: ไอคอนแท็บเบราว์เซอร์แบบ SVG ฝังในตัว (สี่เหลี่ยมสีส้มพร้อมรูปภูเขา)
บรรทัด 8–9: สไตล์ของไลบรารีแผนที่ Leaflet และตัวเลือกวันที่ flatpickr
บรรทัด 10–12: โหลดฟอนต์ Inter และ Sarabun
บรรทัด 13: ➜ frontend/style.css สไตล์ของเว็บเอง
บรรทัด 14: ปิด head
บรรทัด 15–44  ชุดไอคอน SVG
15  <body>
16  <svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
17  <symbol id="i-beach" viewBox="0 0 24 24"><path d="M3 18c1.5 0 1.5 1 3 1s1.5-1 3-1 1.5 1 3 1 1.5-1 3-1 1.5 1 3 1 1.5-1 3-1"/><path d="M4 13a8 8 0 0 1 16 0z"/><path d="M12 13v5"/></symbol>
18  <symbol id="i-temple" viewBox="0 0 24 24"><path d="M12 3l2 3h-4zM7 11l5-5 5 5zM5 15l7-4 7 4zM6 15v5M18 15v5M10 20v-3h4v3M4 20h16"/></symbol>
19  <symbol id="i-viewpoint" viewBox="0 0 24 24"><path d="M3 19l6-10 4 6 2-3 6 7z"/><circle cx="17" cy="6" r="1.6"/></symbol>
20  <symbol id="i-culture" viewBox="0 0 24 24"><path d="M3 9l9-5 9 5zM5 9v9M9.5 9v9M14.5 9v9M19 9v9M3 20h18"/></symbol>
21  <symbol id="i-market" viewBox="0 0 24 24"><path d="M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2"/></symbol>
22  <symbol id="i-activity" viewBox="0 0 24 24"><path d="M12 3l2.2 5.3 5.8.5-4.4 3.8 1.4 5.6L12 15l-5 3.2 1.4-5.6L4 8.8l5.8-.5z"/></symbol>
23  <symbol id="i-restaurant" viewBox="0 0 24 24"><path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 21V3c-2.5 1.5-3.5 4-3.5 7 0 1.5 1 2.5 3.5 3"/></symbol>
24  <symbol id="i-hotel" viewBox="0 0 24 24"><path d="M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16M15 10h4a1 1 0 0 1 1 1v10M2.5 21h19M8 8h3M8 12h3M8 16h3M17.5 14h.01M17.5 18h.01"/></symbol>
25  <symbol id="i-sunrise" viewBox="0 0 24 24"><path d="M3 18h18M6 18a6 6 0 0 1 12 0M12 5v3M5 9l2 2M19 9l-2 2"/></symbol>
26  <symbol id="i-lock" viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></symbol>
27  <symbol id="i-hotel-off" viewBox="0 0 24 24"><path d="M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16M15 10h4a1 1 0 0 1 1 1v10M2.5 21h19M8 8h3M8 12h3M8 16h3M17.5 14h.01M17.5 18h.01"/><path d="M3.5 3.5l17 17"/></symbol>
28  <symbol id="i-tent" viewBox="0 0 24 24"><path d="M3 19L12 5l9 14zM12 19l-3-5h6z"/></symbol>
29  <symbol id="i-star" viewBox="0 0 24 24"><path d="M12 3.5l2.5 5.2 5.7.8-4.1 4 1 5.7-5.1-2.7-5.1 2.7 1-5.7-4.1-4 5.7-.8z"/></symbol>
30  <symbol id="i-bolt" viewBox="0 0 24 24"><path d="M13 3L5 13h6l-1 8 8-10h-6z"/></symbol>
31  <symbol id="i-rocket" viewBox="0 0 24 24"><path d="M5 19c0-3 1-4 3-4l-1-3c3-6 8-8 13-8 0 5-2 10-8 13l-3-1c0 2-1 3-4 3zM15 9h.01"/></symbol>
32  <symbol id="i-bot" viewBox="0 0 24 24"><rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M3 13v2M21 13v2"/></symbol>
33  <symbol id="i-link" viewBox="0 0 24 24"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></symbol>
34  <symbol id="i-scale" viewBox="0 0 24 24"><path d="M12 4v16M7 20h10M5 8h14M5 8l-3 7a3.5 3.5 0 0 0 6 0zM19 8l-3 7a3.5 3.5 0 0 0 6 0z"/></symbol>
35  <symbol id="i-calendar" viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="3"/><path d="M4 10h16M9 3v4M15 3v4"/></symbol>
36  <symbol id="i-file" viewBox="0 0 24 24"><path d="M7 3h7l5 5v12a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zM14 3v5h5M9 13h6M9 17h6"/></symbol>
37  <symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
38  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></symbol>
39  <symbol id="i-arrow-down" viewBox="0 0 24 24"><path d="M12 5v14M6 13l6 6 6-6"/></symbol>
40  <symbol id="i-arrow-right" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
41  <symbol id="i-thumb" viewBox="0 0 24 24"><path d="M8 11v9H4v-9zM8 11l4-8c2 0 3 1.5 2.5 3.5L14 9h5a2 2 0 0 1 2 2.3l-1 6A2 2 0 0 1 18 19H8"/></symbol>
42  <symbol id="i-ban" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M6 6l12 12"/></symbol>
43  <symbol id="i-sliders" viewBox="0 0 24 24"><path d="M4 7h10M18 7h2M4 17h2M10 17h10M14 4v6M8 14v6"/></symbol>
44  </defs></svg>
บรรทัด 15–16: เปิด body และ SVG ซ่อน (กว้างยาวศูนย์) ที่เก็บ symbol ของไอคอนให้เรียกซ้ำด้วย <use href="#i-...">
บรรทัด 17–24: ไอคอนประเภทสถานที่: หาด วัด จุดชมวิว วัฒนธรรม ตลาด กิจกรรม ร้านอาหาร โรงแรม
บรรทัด 25–34: ไอคอนอื่น ๆ: พระอาทิตย์ขึ้น กุญแจ (จุดที่ล็อก) โรงแรมถูกขีดฆ่า เต็นท์ ดาว สายฟ้า จรวด หุ่นยนต์ ลิงก์ ตาชั่ง
บรรทัด 35–43: ไอคอนปฏิทิน ไฟล์ ปิด ค้นหา ลูกศร ถูกใจ ห้าม และแถบเลื่อน
บรรทัด 44: ปิดชุดไอคอน
บรรทัด 46–57  พื้นหลังตกแต่ง
46    <!-- Background: aurora orbs + grid + grain -->
47    <div class="bg-layers" aria-hidden="true">
48      <div class="bg-grid"></div>
49      <div class="bg-aurora">
50        <div class="orb orb-1"></div>
51        <div class="orb orb-2"></div>
52        <div class="orb orb-3"></div>
53        <div class="orb orb-4"></div>
54        <div class="orb orb-5"></div>
55      </div>
56      <div class="bg-grain"></div>
57    </div>
บรรทัด 46–57: เลเยอร์พื้นหลัง (ตาราง แสงออโรราห้าก้อน และลายเกรน) ใช้ aria-hidden เพราะเป็นของประดับ
บรรทัด 59–76  ส่วนบนสุดของหน้า
59    <!-- Landing screen (fits exactly 100vh) -->
60    <div class="landing-screen">
61
62    <!-- Top navigation -->
63    <nav class="topbar">
64      <div class="brand">
65        <div class="brand-text">
66          <h1>WeEasy<span class="brand-trip">Trip</span></h1>
67        </div>
68      </div>
69      <div class="topbar-actions">
70        <button class="icon-btn" id="themeBtn" onclick="toggleTheme()" title="Toggle theme">
71          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"></path></svg>
72          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
73        </button>
74        <button class="icon-btn dev-btn" id="devBtn" onclick="toggleDevMode()" title="Developer Mode" aria-pressed="false">&lt;/&gt;</button>
75      </div>
76    </nav>
บรรทัด 59–60: เปิดหน้า landing ที่สูงเต็มจอพอดี (.landing-screen)
บรรทัด 62–68: แถบบน: ชื่อแบรนด์ "WeEasyTrip"
บรรทัด 69–73: กลุ่มปุ่มบนแถบ (.topbar-actions) ปุ่มธีมเรียก ➜ toggleTheme() ใน frontend/app.js สลับไอคอนพระอาทิตย์/พระจันทร์ (ปุ่มภาษาจาก ➜ frontend/i18n.js และปุ่ม "?" จาก ➜ frontend/tutorial.js ถูกแทรกเข้าที่นี่ตอนโหลด)
บรรทัด 74: ปุ่มโหมด Developer เรียก ➜ toggleDevMode() ใน frontend/app.js
บรรทัด 75–76: ปิดกลุ่มปุ่มและแถบบน
บรรทัด 78–87  ภาพหัวเรื่อง
78    <!-- Hero visual -->
79    <section class="hero-visual">
80      <div class="hero-bg" style="background-image:url('BG2.jpg')"></div>
81      <div class="hero-overlay"></div>
82      <div class="hero-content">
83        <span class="hero-label">Your Travel Services</span>
84        <h1 class="hero-h1">วางแผนเที่ยวไทยได้ง่ายๆ</h1>
85        <p class="hero-desc">ระบบ AI หาเส้นทางที่ดีที่สุดภายใต้งบประมาณ เวลา และช่วงเวลาเปิด-ปิดของแต่ละสถานที่</p>
86      </div>
87    </section>
บรรทัด 78–87: ส่วน hero: ภาพพื้นหลัง BG2.jpg (ถูกเปลี่ยนตามจังหวัดโดยโค้ดใน ➜ frontend/app.js) ชั้นทึบ และข้อความหัวเรื่อง "วางแผนเที่ยวไทยได้ง่ายๆ"
บรรทัด 89–116  แผงวางแผนและความชอบ
89    <!-- Planner panel -->
90    <div class="planner-wrapper">
91      <div class="planner-panel">
92        <div class="planner-top-row">
93          <span class="step-badge">Step 1</span>
94          <h3 class="planner-title">วางแผนทริป</h3>
95          <button type="button" class="pref-toggle ml-auto" id="prefToggle" onclick="togglePrefs()"><svg class="ic "><use href="#i-sliders"/></svg> ความชอบ <span id="prefSummary" class="pref-summary"></span></button>
96          <span id="apiStatus" class="api-status">
97            <span class="dot"></span><span class="status-text">connecting...</span>
98          </span>
99        </div>
100
101        <!-- ความชอบ (พับเก็บได้ — เปิดจากปุ่มด้านบน) -->
102        <div class="pref-panel" id="prefPanel" hidden>
103          <div class="pref-row">
104            <span class="pref-label">ความชอบ</span>
105            <div class="pref-chips" id="prefChips"></div>
106          </div>
107          <div class="pref-row">
108            <span class="pref-label">อาหาร</span>
109            <select id="prefDiet" onchange="updatePrefSummary()">
110              <option value="none">ไม่จำกัด</option>
111              <option value="vegetarian">มังสวิรัติ</option>
112              <option value="halal">ฮาลาล</option>
113            </select>
114            <small class="pref-note">ใช้เท่าที่มีข้อมูลในฐานข้อมูล (OSM) ถ้าร้านไม่พอจะเสริมร้านทั่วไปและแจ้งเตือน</small>
115          </div>
116        </div>
บรรทัด 89–91: ตัวห่อและแผงฟอร์มวางแผน
บรรทัด 92–99: แถวบนของแผง: ป้าย Step 1 ชื่อฟอร์ม ปุ่ม "ความชอบ" เรียก ➜ togglePrefs() ใน frontend/app.js และป้ายสถานะการเชื่อมต่อ backend (#apiStatus)
บรรทัด 101–106: แผงความชอบที่พับเก็บได้ (เริ่มซ่อน) ชิปประเภทสถานที่ที่ชอบหรือไม่ชอบถูกสร้างใน #prefChips ด้วย ➜ frontend/app.js
บรรทัด 107–115: ตัวเลือกอาหาร (ไม่จำกัด มังสวิรัติ ฮาลาล) เมื่อเปลี่ยนเรียก ➜ updatePrefSummary() ใน frontend/app.js พร้อมหมายเหตุเรื่องข้อมูลร้านจาก OSM
บรรทัด 116: ปิดแผงความชอบ
บรรทัด 118–164  ช่องเลือกจังหวัด
118        <div class="pf-grid">
119          <!-- จังหวัด -->
120          <div class="pf-col">
121            <label class="pf-label">จังหวัด</label>
122            <input type="hidden" id="province" value="phuket"/>
123            <div class="prov-select" id="provSelect" onclick="toggleProvDropdown(event)">
124              <span class="prov-name" id="provName">ภูเก็ต</span>
125              <svg class="prov-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
126            </div>
127            <div class="pf-hint"></div>
128            <div class="prov-dropdown" id="provDropdown">
129              <div class="prov-search-wrap">
130                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
131                <input type="text" id="provSearch" placeholder="ค้นหาจังหวัด..." oninput="filterProvince(this.value)" autocomplete="off"/>
132              </div>
133              <div class="prov-list" id="provList">
134                <div class="prov-item prov-active" data-value="phuket" data-label="ภูเก็ต" onclick="selectProvince(this)">
135                  <span class="prov-item-name">ภูเก็ต</span>
136                  <span class="prov-item-badge">พร้อมใช้งาน</span>
137                </div>
138                <div class="prov-group-label">ภาคเหนือ</div>
139                <div class="prov-item prov-disabled" data-label="เชียงใหม่"><span class="prov-item-name">เชียงใหม่</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
140                <div class="prov-item prov-disabled" data-label="เชียงราย"><span class="prov-item-name">เชียงราย</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
141                <div class="prov-item prov-disabled" data-label="แม่ฮ่องสอน"><span class="prov-item-name">แม่ฮ่องสอน</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
142                <div class="prov-item prov-disabled" data-label="น่าน"><span class="prov-item-name">น่าน</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
143                <div class="prov-item prov-disabled" data-label="เลย"><span class="prov-item-name">เลย</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
144                <div class="prov-group-label">ภาคกลาง</div>
145                <div class="prov-item prov-disabled" data-label="กรุงเทพมหานคร"><span class="prov-item-name">กรุงเทพมหานคร</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
146                <div class="prov-item prov-disabled" data-label="นครปฐม"><span class="prov-item-name">นครปฐม</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
147                <div class="prov-item prov-disabled" data-label="พระนครศรีอยุธยา"><span class="prov-item-name">พระนครศรีอยุธยา</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
148                <div class="prov-group-label">ภาคตะวันออก</div>
149                <div class="prov-item prov-disabled" data-label="ชลบุรี"><span class="prov-item-name">ชลบุรี</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
150                <div class="prov-item prov-disabled" data-label="ระยอง"><span class="prov-item-name">ระยอง</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
151                <div class="prov-item prov-disabled" data-label="จันทบุรี"><span class="prov-item-name">จันทบุรี</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
152                <div class="prov-group-label">ภาคใต้</div>
153                <div class="prov-item prov-disabled" data-label="กระบี่"><span class="prov-item-name">กระบี่</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
154                <div class="prov-item prov-disabled" data-label="สุราษฎร์ธานี"><span class="prov-item-name">สุราษฎร์ธานี</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
155                <div class="prov-item prov-disabled" data-label="นครศรีธรรมราช"><span class="prov-item-name">นครศรีธรรมราช</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
156                <div class="prov-item prov-disabled" data-label="พังงา"><span class="prov-item-name">พังงา</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
157                <div class="prov-item prov-disabled" data-label="ตรัง"><span class="prov-item-name">ตรัง</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
158                <div class="prov-group-label">ภาคอีสาน</div>
159                <div class="prov-item prov-disabled" data-label="ขอนแก่น"><span class="prov-item-name">ขอนแก่น</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
160                <div class="prov-item prov-disabled" data-label="นครราชสีมา"><span class="prov-item-name">นครราชสีมา</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
161                <div class="prov-item prov-disabled" data-label="อุบลราชธานี"><span class="prov-item-name">อุบลราชธานี</span><span class="prov-item-soon">เร็วๆ นี้</span></div>
162              </div>
163            </div>
164          </div>
บรรทัด 118–122: เริ่มกริดฟอร์ม ช่องจังหวัดมีช่องซ่อน #province เก็บ slug (ตั้งต้น phuket) ที่โค้ดอ่านตอนค้นหา
บรรทัด 123–127: กล่องที่คลิกเพื่อเปิดเมนูจังหวัด เรียก toggleProvDropdown (ประกาศท้ายไฟล์นี้) แสดงชื่อจังหวัดและลูกศร
บรรทัด 128–132: เมนูจังหวัด (ซ่อนจนกว่าจะเปิด) พร้อมช่องค้นหา ที่เรียก filterProvince ทุกครั้งที่พิมพ์
บรรทัด 133–137: รายการจังหวัดแรก (ภูเก็ต) สถานะ "พร้อมใช้งาน" คลิกแล้วเรียก selectProvince
บรรทัด 138–161: จังหวัดอื่นจัดกลุ่มตามภาค (เหนือ กลาง ตะวันออก ใต้ อีสาน) ตั้งต้นเป็นสถานะ "เร็วๆ นี้" แบบกดไม่ได้ ภายหลัง ➜ frontend/app.js เปลี่ยนสถานะตามข้อมูลจริงที่ ➜ get_provinces() ใน backend/main.py ส่งกลับมา
บรรทัด 162–164: ปิดรายการ เมนู และช่องจังหวัด
บรรทัด 165–186  งบประมาณและวันเดินทาง
165          <!-- งบประมาณ -->
166          <div class="pf-col">
167            <label class="pf-label">งบประมาณ</label>
168            <div class="input-with-unit">
169              <input type="number" id="budget" value="20000" min="1000" step="500"/>
170              <span class="unit">บาท</span>
171            </div>
172            <div class="pf-hint">1,000 – 100,000 บาท</div>
173          </div>
174          <!-- วันเดินทาง -->
175          <div class="pf-col pf-col-wide">
176            <label class="pf-label">ช่วงวันเดินทาง</label>
177            <div class="date-range-input">
178              <svg class="date-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
179                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
180                <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>
181                <line x1="3" y1="10" x2="21" y2="10"/>
182              </svg>
183              <input type="text" id="dateRange" placeholder="เลือกช่วงวันเดินทาง..." readonly/>
184            </div>
185            <div class="date-summary pf-hint" id="dateSummary">เลือกวันเช็คอินและเช็คเอาต์</div>
186          </div>
บรรทัด 165–173: ช่องงบประมาณ (ตั้งต้น 20,000 ขั้น 500 ขั้นต่ำ 1,000) หน่วยบาท
บรรทัด 174–186: ช่องช่วงวันเดินทาง ใช้ flatpickr (อ่านอย่างเดียว) และบรรทัดสรุปวันเช็คอิน/เช็คเอาต์ที่ ➜ frontend/app.js เติมให้
บรรทัด 187–198  จำนวนคน
187          <!-- จำนวนคน -->
188          <div class="pf-col">
189            <label class="pf-label">จำนวนคน</label>
190            <div class="counter-control">
191              <button onclick="changeTravelers(-1)">−</button>
192              <input type="number" id="travelers" value="2" min="1" max="10" readonly/>
193              <button onclick="changeTravelers(1)">+</button>
194            </div>
195          </div>
196        </div>
197
198        <div class="pf-divider"></div>
บรรทัด 187–195: ตัวนับจำนวนคน (ตั้งต้น 2 ช่วง 1-10) ปุ่ม − และ + เรียก ➜ changeTravelers() ใน frontend/app.js
บรรทัด 196–198: ปิดกริดแรกและเส้นคั่น
บรรทัด 200–231  ที่พักและปุ่มค้นหา
200        <div class="pf-grid pf-grid-b">
201          <!-- ที่พัก -->
202          <div class="pf-col pf-col-hotel">
203            <label class="pf-label">ที่พัก</label>
204            <div class="hotel-card" id="hotelOptionCard" onclick="toggleHotelOption()">
205              <div class="hotel-card-icon" id="hotelCardIcon"><svg class="ic "><use href="#i-hotel"/></svg></div>
206              <div class="hotel-card-body">
207                <span class="hotel-card-title" id="hotelToggleLabel">รวมค่าโรงแรมในงบประมาณ</span>
208              </div>
209              <div class="hotel-card-switch" onclick="event.stopPropagation()">
210                <input type="checkbox" id="includeHotel" checked onchange="onHotelToggle()"/>
211                <label for="includeHotel" class="toggle-track"><span class="toggle-thumb"></span></label>
212              </div>
213            </div>
214            <div class="pf-hint" id="hotelHint">หักค่าโรงแรมออกจากงบก่อนวางแผนกิจกรรม</div>
215          </div>
216          <!-- ปุ่มค้นหา -->
217          <div class="pf-col pf-col-search">
218            <label class="pf-label">&nbsp;</label>
219            <button id="searchBtn" class="cta-btn" onclick="searchPackages()">
220              <span class="btn-content">
221                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg>
222                <span>ค้นหา</span>
223              </span>
224              <span class="btn-loader">
225                <svg class="spinner" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="3" fill="none"></circle></svg>
226                <span>กำลังคำนวณ...</span>
227              </span>
228            </button>
229            <div class="pf-hint"></div>
230          </div>
231        </div>
บรรทัด 200–215: การ์ดตัวเลือกที่พัก: คลิกที่การ์ดเรียก ➜ toggleHotelOption() ใน frontend/app.js สวิตช์ includeHotel เรียก ➜ onHotelToggle() ใน frontend/app.js (stopPropagation กันคลิกซ้อน) และข้อความอธิบายที่เปลี่ยนตามสถานะ
บรรทัด 216–230: ปุ่มค้นหา #searchBtn เรียก ➜ searchPackages() ใน frontend/app.js ซึ่งส่งคำขอไป ➜ create_packages() ใน backend/main.py ปุ่มมีสองสถานะ (ข้อความปกติ และสปินเนอร์พร้อม "กำลังคำนวณ...")
บรรทัด 231: ปิดกริดที่สอง
บรรทัด 233–251  เลือกอัลกอริทึม (เฉพาะโหมด Developer)
233        <!-- อัลกอริทึม (เฉพาะโหมด Developer — ล่างสุดของฟอร์ม) -->
234        <div class="pf-algo-row">
235          <!-- อัลกอริทึม -->
236          <div class="pf-col pf-col-algo">
237            <label class="pf-label">อัลกอริทึม</label>
238            <div class="algo-segment" id="algoControl">
239              <button data-val="greedy" title="เร็วสุด"><span class="btn-icon"><svg class="ic "><use href="#i-bolt"/></svg></span> Greedy</button>
240              <button data-val="ga" title="Global optimization"><span class="btn-icon"><svg class="ic "><use href="#i-rocket"/></svg></span> GA</button>
241              <button data-val="hybrid" class="active" title="แนะนำ"><span class="btn-icon"><svg class="ic "><use href="#i-star"/></svg></span> Hybrid</button>
242              <button data-val="hybrid_rl" title="Hybrid + RL seed (ทดลอง)"><span class="btn-icon"><svg class="ic "><use href="#i-bot"/></svg></span> +RL</button>
243            </div>
244            <div class="pf-hint" id="algoHint">Hybrid: รวมข้อดีของ Greedy + GA + 2-opt</div>
245          </div>
246        </div>
247
248      </div>
249    </div>
250
251    </div><!-- /landing-screen -->
บรรทัด 233–246: แถวเลือกอัลกอริทึม แสดงเฉพาะโหมด Developer ปุ่มสี่ปุ่ม: Greedy (➜ algorithm/greedy.py) GA (➜ algorithm/genetic.py) Hybrid (➜ algorithm/hybrid.py) และ +RL (➜ algorithm/rl.py) พร้อมข้อความอธิบายที่ ➜ frontend/app.js เปลี่ยนตามตัวเลือก
บรรทัด 247–251: ปิดแผง ตัวห่อ และหน้า landing
บรรทัด 253–263  ส่วนแพ็กเกจ (ขั้นที่ 2)
253      <!-- Packages section -->
254    <section class="packages-section" id="packagesSection" style="display:none;">
255      <div class="section-head">
256        <div>
257          <span class="step-badge">Step 2</span>
258          <h2>เลือกแพ็กเกจที่คุณชอบ</h2>
259        </div>
260        <div class="meta-summary" id="metaSummary"></div>
261      </div>
262      <div class="packages-grid" id="packagesRow"></div>
263    </section>
บรรทัด 253–263: ส่วนเลือกแพ็กเกจ (ซ่อนจนกว่าจะมีผล) หัวเรื่อง ป้าย Step 2 สรุปเงื่อนไขการค้นหา (#metaSummary) และที่ว่างวางการ์ด 3 แพ็กเกจ (#packagesRow) ที่ ➜ renderPackages() ใน frontend/app.js เติม
บรรทัด 265–293  ส่วนรายละเอียดแผน (ขั้นที่ 3)
265    <!-- Detail section: side panel + map -->
266    <section class="detail-section" id="detailPanel" style="display:none;">
267      <div class="section-head">
268        <div>
269          <span class="step-badge">Step 3</span>
270          <h2 id="detailTitle">ปรับแต่งทริปของคุณ</h2>
271        </div>
272        <div class="detail-actions">
273          <span class="kpi" id="kpiScore"><span class="kpi-label">คะแนน</span><span class="kpi-val">—</span></span>
274          <span class="kpi" id="kpiCost"><span class="kpi-label">ค่าใช้จ่าย</span><span class="kpi-val">—</span></span>
275          <span class="kpi" id="kpiPois"><span class="kpi-label">สถานที่</span><span class="kpi-val">—</span></span>
276          <button class="reshuffle-btn export-btn" onclick="shareSession()" title="สร้างลิงก์ให้เพื่อนเปิดดูและแก้แผนเดียวกัน"><svg class="ic "><use href="#i-link"/></svg> แชร์</button>
277          <button class="reshuffle-btn export-btn" onclick="openPareto()" title="ดูแผนทางเลือก: ขับน้อย หลากหลาย หรือประหยัด"><svg class="ic "><use href="#i-scale"/></svg> ทางเลือกอื่น</button>
278          <button class="reshuffle-btn export-btn" onclick="exportIcs()" title="ดาวน์โหลดไฟล์ปฏิทิน (.ics) เปิดใน Google Calendar / Apple / Outlook"><svg class="ic "><use href="#i-calendar"/></svg> ปฏิทิน</button>
279          <button class="reshuffle-btn export-btn" onclick="window.print()" title="พิมพ์หรือบันทึกเป็น PDF"><svg class="ic "><use href="#i-file"/></svg> PDF</button>
280          <button class="reshuffle-btn" onclick="reshufflePackage()" title="สุ่มสถานที่ใหม่ด้วย algorithm เดิม">
281            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>
282            Re-shuffle
283          </button>
284        </div>
285      </div>
286      <div class="detail-grid">
287        <div class="day-list" id="dayPanels"></div>
288        <div class="map-wrap">
289          <div class="day-toggles" id="dayToggles"></div>
290          <div id="map"></div>
291        </div>
292      </div>
293    </section>
บรรทัด 265–271: ส่วนรายละเอียด (ซ่อนจนกว่าจะเลือกแผน) หัวเรื่องและป้าย Step 3
บรรทัด 272–275: กล่องปุ่มของแผนและตัวเลขสรุป (KPI) คะแนน ค่าใช้จ่าย จำนวนสถานที่ ซึ่ง ➜ renderDetail() ใน frontend/app.js เติมค่า
บรรทัด 276: ปุ่มแชร์ เรียก ➜ shareSession() ใน frontend/app.js
บรรทัด 277: ปุ่มแผนทางเลือก เรียก ➜ openPareto() ใน frontend/app.js ซึ่งเรียก ➜ pareto() ใน backend/main.py
บรรทัด 278: ปุ่มส่งออกปฏิทิน .ics เรียก ➜ exportIcs() ใน frontend/app.js
บรรทัด 279: ปุ่ม PDF ใช้ window.print() ของเบราว์เซอร์
บรรทัด 280–283: ปุ่มสุ่มสถานที่ใหม่ เรียก ➜ reshufflePackage() ใน frontend/app.js
บรรทัด 284–285: ปิดกล่องปุ่มและหัวส่วน
บรรทัด 286–292: กริดรายละเอียด: รายการวัน (#dayPanels) ฝั่งซ้าย และแผนที่ฝั่งขวาพร้อมปุ่มเปิดปิดแต่ละวัน (#dayToggles) และพื้นที่แผนที่ (#map)
บรรทัด 293: ปิดส่วนรายละเอียด
บรรทัด 295–304  แม่แบบโครงรอโหลด
295    <!-- Loading skeleton template -->
296    <template id="skeletonTemplate">
297      <div class="package-card skeleton">
298        <div class="sk sk-tier"></div>
299        <div class="sk sk-title"></div>
300        <div class="sk sk-row"></div>
301        <div class="sk sk-row"></div>
302        <div class="sk sk-row"></div>
303      </div>
304    </template>
บรรทัด 295–304: <template> ของการ์ดแพ็กเกจโครงรอโหลด (skeleton) ที่ ➜ frontend/app.js คัดลอกไปแสดงระหว่างรอผลจาก backend
บรรทัด 306–324  หน้าต่างเปลี่ยนสถานที่
306    <!-- Swap modal -->
307    <div class="modal" id="swapModal">
308      <div class="modal-backdrop" onclick="closeSwapModal()"></div>
309      <div class="modal-card">
310        <div class="modal-head">
311          <div>
312            <div class="modal-title" id="swapTitle">เปลี่ยนสถานที่</div>
313            <div class="modal-sub" id="swapCurrentInfo"></div>
314          </div>
315          <button class="icon-btn" onclick="closeSwapModal()" title="ปิด"><svg class="ic "><use href="#i-close"/></svg></button>
316        </div>
317        <div class="modal-search">
318          <input type="text" id="swapFilter" placeholder="ค้นหาสถานที่..." oninput="filterSwapList()" />
319        </div>
320        <div class="modal-body">
321          <ul id="swapList" class="swap-list"></ul>
322        </div>
323      </div>
324    </div>
บรรทัด 306–308: ตัวหน้าต่าง ฉากหลังที่คลิกแล้วปิดด้วย ➜ closeSwapModal() ใน frontend/app.js
บรรทัด 309–316: หัวหน้าต่าง: ชื่อ ข้อมูลจุดปัจจุบัน และปุ่มปิด
บรรทัด 317–319: ช่องค้นหาสถานที่ เรียก ➜ filterSwapList() ใน frontend/app.js ทุกครั้งที่พิมพ์
บรรทัด 320–324: รายการสถานที่ให้เลือกสลับ (#swapList) และปิดหน้าต่าง
บรรทัด 326–341  หน้าต่างแผนทางเลือก (Pareto)
326    <!-- Pareto: ทางเลือกที่ต่างกัน (คะแนน / ความหลากหลาย / ระยะทาง) -->
327    <div class="modal" id="paretoModal">
328      <div class="modal-backdrop" onclick="closePareto()"></div>
329      <div class="modal-card">
330        <div class="modal-head">
331          <div>
332            <div class="modal-title">ทางเลือกอื่นของทริปนี้</div>
333            <div class="modal-sub">เลือกแผนที่เน้นสิ่งที่คุณสนใจ เช่น ขับน้อย หลากหลาย หรือประหยัด — เทียบกับแผนที่คุณเปิดอยู่</div>
334          </div>
335          <button class="icon-btn" onclick="closePareto()" title="ปิด"><svg class="ic "><use href="#i-close"/></svg></button>
336        </div>
337        <div class="modal-body">
338          <div id="paretoTable"></div>
339        </div>
340      </div>
341    </div>
บรรทัด 326–329: ตัวหน้าต่าง และฉากหลังที่ปิดด้วย ➜ closePareto() ใน frontend/app.js
บรรทัด 330–336: หัวหน้าต่าง คำอธิบายทางเลือก (ขับน้อย หลากหลาย ประหยัด) และปุ่มปิด
บรรทัด 337–341: ที่ว่างของตารางแผนทางเลือก (#paretoTable) ที่ ➜ openPareto() ใน frontend/app.js เติมจากผลของ ➜ algorithm/pareto.py
บรรทัด 343–353  ถาดแจ้งเตือนและสคริปต์
343    <!-- Toast container -->
344    <div id="toastContainer" class="toast-container"></div>
345
346    <!-- Scripts -->
347    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
348    <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
349    <script src="app.js"></script>
350    <script src="extras.js"></script>
351    <script src="tutorial.js"></script>
352    <script src="tooltip.js"></script>
353    <script src="i18n.js"></script>
บรรทัด 343–344: ถาดแจ้งเตือน (toast)
บรรทัด 346–348: โหลด Leaflet และ flatpickr จาก CDN
บรรทัด 349–353: โหลดสคริปต์ของเว็บ: ➜ frontend/app.js (ตรรกะหลัก) ➜ frontend/extras.js (ฟีเจอร์เสริม) ➜ frontend/tutorial.js ➜ frontend/tooltip.js และ ➜ frontend/i18n.js (ต้องมาท้ายสุดเพื่อแปลหลังสร้างหน้าเสร็จ)
บรรทัด 355–383  เปิดเมนูจังหวัด
355    <script>
356    // Province dropdown
357    function toggleProvDropdown(e) {
358      e.stopPropagation();
359      const dd = document.getElementById('provDropdown');
360      const sel = document.getElementById('provSelect');
361      const isOpen = dd.classList.contains('open');
362      closeProvDropdown();
363      if (!isOpen) {
364        // รีเซต drop-up ก่อน แล้วค่อยตรวจพื้นที่ใหม่
365        dd.classList.remove('drop-up');
366        const selRect = sel.getBoundingClientRect();
367        const dropW = 280;
368        const dropH = 340;
369        // จัด center ตาม trigger แล้ว clamp ให้ไม่เกินขอบจอ
370        const idealLeft = selRect.left + selRect.width / 2 - dropW / 2;
371        const clampedLeft = Math.max(8, Math.min(idealLeft, window.innerWidth - dropW - 8));
372        // แปลงเป็น offset จาก parent (.pf-col ที่มี position: relative)
373        const colRect = sel.closest('.pf-col').getBoundingClientRect();
374        dd.style.left = (clampedLeft - colRect.left) + 'px';
375        const spaceBelow = window.innerHeight - selRect.bottom;
376        if (spaceBelow < dropH) {
377          dd.classList.add('drop-up');
378        }
379        dd.classList.add('open');
380        sel.classList.add('open');
381        setTimeout(() => document.getElementById('provSearch').focus(), 50);
382      }
383    }
บรรทัด 355–356: เปิดสคริปต์ย่อย
บรรทัด 357–361: toggleProvDropdown หยุดไม่ให้คลิกลอยขึ้นไป ปิดเมนูเดิม แล้วถ้าเมนูไม่ได้เปิดอยู่ก็เตรียมเปิด
บรรทัด 362–365: รีเซตสถานะเปิดขึ้นบน (drop-up) ก่อน
บรรทัด 366–371: คำนวณตำแหน่งแนวนอน จัดกึ่งกลางตามกล่องเลือกและหนีบไม่ให้ล้นขอบจอ (กว้าง 280 สูง 340)
บรรทัด 372–374: แปลงเป็นระยะห่างจากคอลัมน์แม่ที่ใช้ position: relative
บรรทัด 375–378: ถ้าที่ว่างใต้กล่องน้อยกว่าความสูงเมนู เปิดเมนูขึ้นด้านบนแทน
บรรทัด 379–382: เติมคลาส open ให้เมนูและกล่อง แล้วโฟกัสช่องค้นหา (หน่วง 50 มิลลิวินาทีเพื่อให้เมนูปรากฏก่อน)
บรรทัด 383: ปิดฟังก์ชัน
บรรทัด 384–398  ปิดและเลือกจังหวัด
384    function closeProvDropdown() {
385      document.getElementById('provDropdown').classList.remove('open');
386      document.getElementById('provSelect').classList.remove('open');
387      document.getElementById('provSearch').value = '';
388      filterProvince('');
389    }
390    function selectProvince(el) {
391      if (el.classList.contains('prov-disabled')) return;
392      document.querySelectorAll('.prov-item').forEach(i => i.classList.remove('prov-active'));
393      el.classList.add('prov-active');
394      document.getElementById('province').value = el.dataset.value;
395      document.getElementById('provName').textContent = el.dataset.label;
396      closeProvDropdown();
397      onProvinceChange(el.dataset.value);
398    }
บรรทัด 384–389: closeProvDropdown เอาคลาส open ออก ล้างช่องค้นหา และเรียก filterProvince('') คืนรายการเต็ม
บรรทัด 390–398: selectProvince ไม่ทำอะไรถ้าจังหวัดนั้นกดไม่ได้ ไม่เช่นนั้นไฮไลต์รายการที่เลือก เก็บ slug ลงช่องซ่อน เปลี่ยนชื่อที่แสดง ปิดเมนู และเรียก ➜ onProvinceChange() ใน frontend/app.js เพื่อโหลดข้อมูลจังหวัดใหม่
บรรทัด 399–422  กรองรายชื่อจังหวัด
399    function filterProvince(q) {
400      const term = q.trim().toLowerCase();
401      const items = document.querySelectorAll('#provList .prov-item');
402      const groups = document.querySelectorAll('#provList .prov-group-label');
403      let visibleInGroup = {};
404      let gi = -1;
405      groups.forEach((g, i) => { visibleInGroup[i] = 0; });
406      items.forEach(item => {
407        const name = item.dataset.label ? item.dataset.label.toLowerCase() : '';
408        const match = !term || name.includes(term);
409        item.style.display = match ? '' : 'none';
410        // find group index
411        let prev = item.previousElementSibling;
412        while (prev) {
413          if (prev.classList.contains('prov-group-label')) {
414            const idx = Array.from(groups).indexOf(prev);
415            if (match && idx >= 0) visibleInGroup[idx] = (visibleInGroup[idx]||0) + 1;
416            break;
417          }
418          prev = prev.previousElementSibling;
419        }
420      });
421      groups.forEach((g, i) => { g.style.display = visibleInGroup[i] > 0 ? '' : 'none'; });
422    }
บรรทัด 399–405: filterProvince ตัดช่องว่างและทำเป็นตัวพิมพ์เล็ก เก็บรายการและป้ายภาค เตรียมตัวนับจำนวนรายการที่เห็นในแต่ละภาค
บรรทัด 406–409: แต่ละรายการ: ตรงกับคำค้นไหม (ค้นว่างคือตรงทั้งหมด) แล้วซ่อนหรือแสดง
บรรทัด 410–420: หาป้ายภาคที่อยู่เหนือรายการนั้น แล้วนับรายการที่ตรงเข้ากลุ่มนั้น
บรรทัด 421–422: ซ่อนป้ายภาคที่ไม่มีรายการเหลือเลย
บรรทัด 423–428  ปิดเมนูเมื่อคลิกข้างนอก
423    document.addEventListener('click', function(e) {
424      if (!e.target.closest('#provSelect') && !e.target.closest('#provDropdown')) closeProvDropdown();
425    });
426    </script>
427  </body>
428  </html>
บรรทัด 423–425: ฟังคลิกทั้งเอกสาร ถ้าคลิกอยู่นอกกล่องและเมนูจังหวัดให้ปิดเมนู
บรรทัด 426–428: ปิดสคริปต์ body และ html

ไฟล์ที่เชื่อมกับไฟล์นี้
algorithm/genetic.py
algorithm/greedy.py
algorithm/hybrid.py
algorithm/pareto.py
algorithm/rl.py
backend/main.py
frontend/app.js
frontend/extras.js
frontend/i18n.js
frontend/style.css
frontend/tooltip.js
frontend/tutorial.js