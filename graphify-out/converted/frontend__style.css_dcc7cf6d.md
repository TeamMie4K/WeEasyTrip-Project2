<!-- converted from frontend__style.css.docx -->

คู่มือโค้ด: frontend/style.css
สไตล์ของหน้าเว็บทั้งหมด (style.css)
ไฟล์ต้นฉบับ: frontend/style.css (1973 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ไฟล์ CSS เดียวที่กำหนดหน้าตาของ ➜ frontend/index.html และองค์ประกอบที่สร้างด้วย JavaScript ใน ➜ frontend/app.js ➜ frontend/extras.js ➜ frontend/tutorial.js ➜ frontend/tooltip.js (คลาสอย่าง .package-card .poi-item .day-toggle .toast .modal .tut .wet-tip) ไฟล์นี้เขียนต่อเติมเป็นรุ่น ๆ จึงมีกฎของส่วนเดียวกันกระจายในหลายช่วงและกฎช่วงหลังทับช่วงก่อน (ลำดับการวางสำคัญ) ธีมมืดเป็นค่าตั้งต้นและธีมสว่างทับด้วย [data-theme="light"] ที่ตัวแปรสี คู่มือนี้อธิบายระดับกลุ่มของกฎ (ไม่อธิบายทีละคุณสมบัติ เพราะซ้ำรูปแบบกันมาก) โดยแต่ละช่วงบอกว่ากฎเหล่านั้นจัดรูปองค์ประกอบอะไร ไฟล์ ➜ frontend/results.html ใช้ CSS ฝังในตัวเองจึงไม่เกี่ยวกับไฟล์นี้

บรรทัด 1–65  ตัวแปรสี ขนาด และธีม
1  /* ===========================================================================
2     Phuket Smart Trip Planner - Modern Design System
3     ====================================================================== */
4
5  /* --- Tokens --- */
6  :root {
7    /* base palette */
8    --bg-base:      #0d0b09;
9    --bg-surface:   rgba(28, 20, 12, 0.70);
10    --bg-elevated:  rgba(36, 26, 14, 0.92);
11    --bg-overlay:   rgba(13, 11, 9,  0.82);
12
13    --border-subtle: rgba(255,160, 80, 0.10);
14    --border-default: rgba(255,160, 80, 0.18);
15    --border-strong:  rgba(255,160, 80, 0.32);
16
17    --text-primary:   #faf5f0;
18    --text-secondary: #e0d0c0;
19    --text-tertiary:  #a08070;
20    --text-muted:     #6a5848;
21
22    --accent-primary: #ff6d35;
23    --accent-glow:    #ff8c5a;
24    --accent-warm:    #f97316;
25    --accent-success: #10b981;
26    --accent-danger:  #ef4444;
27    --accent-warning: #f59e0b;
28
29    --grad-cta:     linear-gradient(135deg, #ff6d35 0%, #e0501a 100%);
30    --grad-text:    linear-gradient(135deg, #ff8c5a, #ffb347);
31
32    --radius-sm: 8px;
33    --radius-md: 12px;
34    --radius-lg: 18px;
35    --radius-xl: 24px;
36
37    --shadow-sm:    0 1px 2px rgba(0,0,0,0.2);
38    --shadow-md:    0 4px 12px rgba(0,0,0,0.25);
39    --shadow-lg:    0 12px 30px rgba(0,0,0,0.4);
40
41    --font-sans: 'Inter', 'Sarabun', system-ui, sans-serif;
42    --transition: 200ms cubic-bezier(0.4, 0, 0.2, 1);
43  }
44
45  [data-theme="light"] {
46    --bg-base:      #ffffff;
47    --bg-surface:   rgba(255, 255, 255, 0.7);
48    --bg-elevated:  rgba(255, 255, 255, 0.9);
49    --bg-overlay:   rgba(255, 255, 255, 0.85);
50
51    --border-subtle: rgba(15, 23, 42, 0.08);
52    --border-default: rgba(15, 23, 42, 0.15);
53    --border-strong:  rgba(15, 23, 42, 0.25);
54
55    --text-primary:   #0f172a;
56    --text-secondary: #334155;
57    --text-tertiary:  #64748b;
58    --text-muted:     #94a3b8;
59
60    --shadow-sm:    0 1px 2px rgba(15,23,42,0.06);
61    --shadow-md:    0 4px 12px rgba(15,23,42,0.08);
62    --shadow-lg:    0 12px 30px rgba(15,23,42,0.12);
63  }
64
65  /* --- Base --- */
บรรทัด 1–5: คอมเมนต์ชื่อระบบ
บรรทัด 6–44: :root ตัวแปรของธีมมืด (ค่าตั้งต้น): สีพื้นผิว สีเส้นขอบสามระดับ สีตัวอักษรสี่ระดับ สีเน้นส้ม (--accent-primary) สถานะสำเร็จ/อันตราย/เตือน ไล่สี รัศมีมุม เงา ฟอนต์ และการเปลี่ยนสถานะ
บรรทัด 45–65: [data-theme="light"] ทับตัวแปรสีด้วยชุดสว่าง (สลับโดย ➜ toggleTheme() ใน frontend/app.js)
บรรทัด 66–91  พื้นฐานของหน้า
66  * { box-sizing: border-box; }
67  html, body {
68    margin: 0; padding: 0;
69    font-family: var(--font-sans);
70    background: var(--bg-base);
71    color: var(--text-primary);
72    font-size: 15px;
73    line-height: 1.55;
74    font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
75    -webkit-font-smoothing: antialiased;
76  }
77  /* เดิม html และ body ตั้ง overflow-x: hidden ทั้งคู่ ทำให้ body กลายเป็นตัวเลื่อนอีกชั้น (แถบเลื่อนซ้อน 2 อัน) — ให้ html เป็นตัวเลื่อนเดียว ส่วน body ใช้ clip ที่ไม่สร้างตัวเลื่อน */
78  html { overflow-x: hidden; }
79  body { overflow-x: clip; }
80
81  button { font-family: inherit; cursor: pointer; border: none; background: none; color: inherit; }
82  input { font-family: inherit; color: inherit; }
83
84  h1, h2, h3, h4 { margin: 0; font-weight: 700; letter-spacing: -0.02em; }
85  h2 { font-size: 1.85rem; }
86  h3 { font-size: 1.15rem; }
87  p  { margin: 0; color: var(--text-secondary); }
88
89
90
91  /* --- Topbar --- */
บรรทัด 66–77: รีเซ็ต box-sizing และตั้งฟอนต์ พื้นหลัง สี ขนาด 15 พิกเซล ให้ html และ body
บรรทัด 78–80: ป้องกันการเลื่อนแนวนอน (ใช้ clip ที่ body เพื่อไม่ให้ body กลายเป็นตัวเลื่อน)
บรรทัด 81–91: ปุ่ม ช่องกรอก และหัวข้อ h1–h4 รับฟอนต์และขนาดมาตรฐาน
บรรทัด 92–212  แถบบน ป้ายขั้น ช่องกรอก และปุ่มค้นหา
92  .topbar {
93    display: flex; justify-content: space-between; align-items: center;
94    padding: 1.25rem 2rem;
95    position: relative; z-index: 20;
96    background: var(--bg-overlay);
97    backdrop-filter: blur(20px);
98    -webkit-backdrop-filter: blur(20px);
99    border-bottom: 1px solid var(--border-subtle);
100    z-index: 100;
101  }
102  .brand { display: flex; align-items: center; gap: 0.75rem; }
103
104  .topbar-actions { display: flex; align-items: center; gap: 0.75rem; }
105  .api-status {
106    display: flex; align-items: center; gap: 0.5rem;
107    padding: 0.4rem 0.8rem;
108    background: var(--bg-surface);
109    border: 1px solid var(--border-subtle);
110    border-radius: 999px;
111    font-size: 0.78rem;
112    color: var(--text-tertiary);
113  }
114  .api-status .dot {
115    width: 7px; height: 7px; border-radius: 50%;
116    background: var(--text-muted);
117  }
118  .api-status.ok .dot { background: var(--accent-success); box-shadow: 0 0 8px var(--accent-success); }
119  .api-status.error .dot { background: var(--accent-danger); }
120  .api-status.loading .dot { background: var(--accent-warning); }
121
122  .icon-btn {
123    width: 38px; height: 38px;
124    display: flex; align-items: center; justify-content: center;
125    border-radius: 10px;
126    border: 1px solid var(--border-subtle);
127    background: var(--bg-surface);
128    color: var(--text-secondary);
129    transition: var(--transition);
130  }
131  .icon-btn:hover { color: var(--text-primary); border-color: var(--border-default); transform: translateY(-1px); }
132  .icon-btn svg { width: 18px; height: 18px; }
133  .icon-sun, .icon-moon { display: none; }
134  [data-theme="dark"] .icon-sun { display: block; }
135  [data-theme="light"] .icon-moon { display: block; }
136
137
138  .step-badge {
139    display: inline-block;
140    padding: 0.25rem 0.7rem;
141    background: var(--bg-elevated);
142    border: 1px solid var(--border-subtle);
143    border-radius: 999px;
144    font-size: 0.7rem; font-weight: 600;
145    color: var(--accent-glow);
146    text-transform: uppercase; letter-spacing: 0.08em;
147  }
148  .input-with-unit {
149    display: flex; align-items: center;
150    background: var(--bg-elevated);
151    border: 1px solid var(--border-subtle);
152    border-radius: var(--radius-md);
153    padding: 0.25rem 1rem;
154    transition: var(--transition);
155  }
156  .input-with-unit:focus-within { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(255,109,53,0.15); }
157  .input-with-unit input {
158    flex: 1; padding: 0.65rem 0; border: none; outline: none;
159    background: transparent; font-size: 1.1rem; font-weight: 600;
160  }
161  .input-with-unit .unit { color: var(--text-tertiary); font-size: 0.9rem; font-weight: 500; }
162
163
164  .counter-control {
165    display: grid; grid-template-columns: 44px 1fr 44px;
166    background: var(--bg-elevated);
167    border: 1px solid var(--border-subtle);
168    border-radius: var(--radius-md);
169    align-items: center;
170    overflow: hidden;
171  }
172  .counter-control button {
173    height: 44px; font-size: 1.2rem; font-weight: 700;
174    color: var(--text-secondary);
175    transition: var(--transition);
176  }
177  .counter-control button:hover { background: rgba(255,255,255,0.05); color: var(--accent-primary); }
178  .counter-control input {
179    text-align: center; border: none; outline: none;
180    background: transparent;
181    font-size: 1.05rem; font-weight: 600;
182    width: 100%;
183  }
184
185  /* CTA button */
186  .cta-btn {
187    width: 100%;
188    position: relative;
189    background: var(--grad-cta);
190    color: white;
191    padding: 0.95rem;
192    border-radius: var(--radius-md);
193    font-size: 1rem; font-weight: 600;
194    transition: var(--transition);
195    box-shadow: 0 8px 20px rgba(255,109,53,0.40);
196    overflow: hidden;
197  }
198  .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(255,109,53,0.50); }
199  .cta-btn:disabled { transform: none; box-shadow: none; opacity: 0.7; cursor: wait; }
200  .btn-content, .btn-loader { display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
201  .btn-content svg { width: 18px; height: 18px; }
202  .btn-loader { display: none; }
203  .cta-btn.loading .btn-content { display: none; }
204  .cta-btn.loading .btn-loader { display: flex; }
205  .spinner {
206    width: 18px; height: 18px;
207    animation: spin 1s linear infinite;
208  }
209  .spinner circle { stroke: currentColor; stroke-dasharray: 50; stroke-dashoffset: 30; stroke-linecap: round; }
210  @keyframes spin { to { transform: rotate(360deg); } }
211
212  /* --- Section heads --- */
บรรทัด 92–101: .topbar แถบบนโปร่งแสงเบลอฉากหลัง
บรรทัด 102–104: .brand และกลุ่มปุ่ม .topbar-actions
บรรทัด 105–121: .api-status ป้ายสถานะ backend และจุดสี ok/error/loading (ตั้งโดย ➜ setApiStatus() ใน frontend/app.js)
บรรทัด 122–137: .icon-btn ปุ่มไอคอนกลม และการสลับไอคอนพระอาทิตย์/พระจันทร์ตามธีม
บรรทัด 138–185: .step-badge และช่องกรอกที่มีหน่วย (.input-with-unit) กับตัวนับจำนวนคน (.counter-control)
บรรทัด 186–212: .cta-btn ปุ่มค้นหาสีไล่เฉด สถานะ loading ที่ซ่อนข้อความและแสดงตัวหมุน (@keyframes spin)
บรรทัด 213–324  หัวส่วน แพ็กเกจ และโครงรอโหลด
213  .section-head {
214    display: flex; justify-content: space-between; align-items: flex-end;
215    margin-bottom: 1.5rem; padding-top: 1rem;
216  }
217  .section-head h2 { margin-top: 0.5rem; font-size: 1.85rem; }
218  .meta-summary {
219    font-size: 0.85rem;
220    color: var(--text-tertiary);
221    text-align: right;
222  }
223
224  /* --- Packages --- */
225  .packages-section {
226    max-width: 1280px;
227    margin: 0 auto;
228    padding: 1rem 2rem 3rem;
229  }
230  .packages-grid {
231    display: grid;
232    grid-template-columns: repeat(3, 1fr);
233    gap: 1.25rem;
234  }
235  .package-card {
236    position: relative;
237    padding: 1.5rem;
238    background: var(--bg-surface);
239    backdrop-filter: blur(20px);
240    -webkit-backdrop-filter: blur(20px);
241    border: 1px solid var(--border-subtle);
242    border-radius: var(--radius-lg);
243    cursor: pointer;
244    transition: var(--transition);
245    animation: cardIn 600ms ease both;
246  }
247  .package-card:nth-child(1) { animation-delay: 0ms; }
248  .package-card:nth-child(2) { animation-delay: 80ms; }
249  .package-card:nth-child(3) { animation-delay: 160ms; }
250  @keyframes cardIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
251  .package-card:hover { transform: translateY(-4px); border-color: var(--border-default); box-shadow: var(--shadow-lg); }
252  .package-card.selected {
253    border-color: var(--accent-primary);
254    box-shadow: 0 0 0 1px var(--accent-primary), 0 0 30px rgba(255,109,53,0.25);
255  }
256  .package-card.invalid { opacity: 0.5; cursor: not-allowed; }
257  .package-card.invalid:hover { transform: none; box-shadow: none; }
258
259  .tier-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
260  .tier-badge {
261    display: inline-flex; align-items: center; gap: 0.4rem;
262    padding: 0.3rem 0.7rem;
263    border-radius: 999px;
264    font-size: 0.72rem; font-weight: 700;
265    text-transform: uppercase; letter-spacing: 0.06em;
266  }
267  .tier-Budget   { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
268  .tier-Standard { background: rgba(255,109,53,0.15);  color: #22d3ee; border: 1px solid rgba(255,109,53,0.3); }
269  .tier-Premium  { background: rgba(249,115,22,0.15); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }
270  .tier-row .runtime {
271    font-size: 0.7rem; color: var(--text-muted);
272    font-feature-settings: 'tnum';
273  }
274
275  .hotel-name {
276    font-size: 1.05rem; font-weight: 600;
277    color: var(--text-primary);
278    margin: 0.5rem 0 1rem;
279  }
280  .hotel-name.no-hotel {
281    color: var(--text-muted); font-weight: 500; font-size: 0.9rem;
282  }
283  .score-display {
284    display: flex; align-items: baseline; gap: 0.4rem;
285    margin-bottom: 1rem;
286  }
287  .score-num {
288    font-size: 2rem; font-weight: 800;
289    background: var(--grad-text);
290    -webkit-background-clip: text; background-clip: text;
291    -webkit-text-fill-color: transparent;
292    line-height: 1;
293    font-feature-settings: 'tnum';
294  }
295  .score-label { color: var(--text-tertiary); font-size: 0.85rem; }
296
297  .stat-row {
298    display: flex; justify-content: space-between; align-items: center;
299    padding: 0.5rem 0;
300    font-size: 0.88rem;
301    border-bottom: 1px solid var(--border-subtle);
302  }
303  .stat-row:last-of-type { border-bottom: none; }
304  .stat-row .label { color: var(--text-tertiary); }
305  .stat-row .val { font-weight: 600; font-feature-settings: 'tnum'; }
306  .stat-row.total { padding-top: 0.75rem; border-top: 1px solid var(--border-default); border-bottom: none; }
307  .stat-row.total .val { color: var(--accent-glow); font-size: 1.15rem; }
308
309  .invalid-msg {
310    background: rgba(239,68,68,0.1);
311    color: #fca5a5; border: 1px solid rgba(239,68,68,0.3);
312    padding: 0.65rem 0.85rem;
313    border-radius: var(--radius-sm);
314    font-size: 0.85rem; margin-top: 0.75rem;
315  }
316
317  /* skeleton */
318  .skeleton .sk { background: var(--bg-elevated); border-radius: 6px; margin: 0.5rem 0; animation: shimmer 1.4s infinite; }
319  .sk-tier { width: 70px; height: 22px; }
320  .sk-title { width: 80%; height: 26px; }
321  .sk-row { width: 100%; height: 14px; }
322  @keyframes shimmer { 0%, 100% { opacity: 0.5; } 50% { opacity: 0.85; } }
323
324  /* --- Detail section --- */
บรรทัด 213–224: .section-head หัวของส่วนแพ็กเกจและรายละเอียด
บรรทัด 225–317: .packages-grid และ .package-card (เข้าฉากด้วย @keyframes cardIn ลอยเมื่อชี้ แบบไม่ผ่านเป็นสีเทา) ป้ายระดับ .tier-* เวลาคำนวณ ตัวเลขคะแนน แถวสถิติ และข้อความไม่ผ่านข้อจำกัด ซึ่งตรงกับ HTML ที่ ➜ renderPackages() ใน frontend/app.js สร้าง
บรรทัด 318–324: โครงรอโหลด .sk ที่กระพริบด้วย @keyframes shimmer (ใช้กับ <template id="skeletonTemplate"> ใน ➜ frontend/index.html)
บรรทัด 325–462  ส่วนรายละเอียดแผนและแผนที่
325  .detail-section {
326    max-width: 1250px;   /* ความกว้างสูงสุดของส่วน STEP 3 (ผู้ใช้กำหนด) */
327    margin: 0 auto;
328    padding: 1rem 2rem 4rem;
329    position: relative;
330  }
331  .detail-actions { display: flex; gap: 0.75rem; }
332  .kpi {
333    display: flex; flex-direction: column;
334    padding: 0.5rem 1rem;
335    background: var(--bg-surface);
336    border: 1px solid var(--border-subtle);
337    border-radius: var(--radius-md);
338    min-width: 80px;
339  }
340  .kpi-label {
341    font-size: 0.7rem; color: var(--text-tertiary);
342    text-transform: uppercase; letter-spacing: 0.06em;
343    font-weight: 600;
344  }
345  .kpi-val {
346    font-size: 1.05rem; font-weight: 700;
347    color: var(--text-primary);
348    font-feature-settings: 'tnum';
349  }
350
351  .detail-grid {
352    display: grid;
353    grid-template-columns: 1.1fr 1fr;
354    gap: 1.5rem;
355    align-items: start;
356  }
357  .day-list { max-height: 720px; overflow-y: auto; padding-right: 0.5rem; }
358  .day-list::-webkit-scrollbar { width: 6px; }
359  .day-list::-webkit-scrollbar-track { background: transparent; }
360  .day-list::-webkit-scrollbar-thumb { background: var(--border-default); border-radius: 3px; }
361
362  .day-panel {
363    background: var(--bg-surface);
364    backdrop-filter: blur(20px);
365    -webkit-backdrop-filter: blur(20px);
366    border: 1px solid var(--border-subtle);
367    border-radius: var(--radius-lg);
368    padding: 1.25rem;
369    margin-bottom: 1rem;
370  }
371  .day-head {
372    display: flex; justify-content: space-between; align-items: center;
373    margin-bottom: 0.75rem;
374    padding-bottom: 0.75rem;
375    border-bottom: 1px solid var(--border-subtle);
376  }
377  .day-title { display: flex; align-items: center; gap: 0.6rem; }
378  .day-color {
379    width: 10px; height: 10px; border-radius: 50%;
380  }
381  .day-title h3 { font-size: 1rem; font-weight: 700; }
382  .day-stats {
383    display: flex; gap: 0.75rem;
384    font-size: 0.78rem; color: var(--text-tertiary);
385    font-feature-settings: 'tnum';
386  }
387  .day-stats span { display: flex; align-items: center; gap: 0.25rem; }
388  .day-stats svg { width: 14px; height: 14px; opacity: 0.7; }
389
390  .poi-list { list-style: none; padding: 0; margin: 0; }
391
392  .poi-item {
393    display: flex; align-items: center; gap: 0.75rem;
394    padding: 0.65rem 0.5rem;
395    border-radius: var(--radius-sm);
396    transition: var(--transition);
397  }
398  .poi-item:hover { background: var(--bg-elevated); }
399  .poi-num {
400    width: 28px; height: 28px; flex-shrink: 0;
401    background: var(--bg-elevated);
402    border: 1px solid var(--border-default);
403    border-radius: 50%;
404    display: flex; align-items: center; justify-content: center;
405    font-size: 0.78rem; font-weight: 700;
406    color: var(--text-secondary);
407  }
408  .poi-info { flex: 1; min-width: 0; }
409  .poi-name { font-weight: 500; font-size: 0.95rem; }
410  .poi-meta {
411    display: flex; gap: 0.5rem; flex-wrap: wrap;
412    font-size: 0.75rem; color: var(--text-muted);
413    margin-top: 0.15rem;
414    font-feature-settings: 'tnum';
415  }
416  .poi-meta .pill {
417    padding: 1px 6px;
418    background: var(--bg-elevated);
419    border-radius: 4px;
420    font-weight: 500;
421    color: var(--text-tertiary);
422  }
423  .poi-actions { display: flex; gap: 0.3rem; flex-shrink: 0; }
424  .poi-actions button, .poi-actions a.btn-loc {
425    width: 32px; height: 32px;
426    display: flex; align-items: center; justify-content: center;
427    border-radius: 6px;
428    color: var(--text-tertiary);
429    transition: var(--transition);
430  }
431  .poi-actions button:hover { background: var(--bg-elevated); }
432  .poi-actions .btn-swap:hover { color: var(--accent-glow); }
433  .poi-actions a.btn-loc { text-decoration: none; }
434  .poi-actions a.btn-loc:hover { background: var(--bg-elevated); color: var(--accent-primary); }
435  .poi-actions .btn-remove:hover { color: var(--accent-danger); }
436  .poi-actions svg { width: 16px; height: 16px; }
437
438
439  /* Map */
440  .map-wrap { position: sticky; top: 90px; align-self: start; }
441  #map {
442    height: 500px; /* fallback — overridden by syncMapHeight() */
443    border-radius: var(--radius-lg);
444    border: 1px solid var(--border-subtle);
445    overflow: hidden;
446    box-shadow: var(--shadow-lg);
447    background: var(--bg-surface);
448  }
449  .leaflet-container {
450    background: var(--bg-base);
451    font-family: var(--font-sans);
452  }
453  .leaflet-popup-content-wrapper {
454    background: var(--bg-elevated) !important;
455    color: var(--text-primary) !important;
456    border: 1px solid var(--border-default);
457    border-radius: var(--radius-md) !important;
458  }
459  .leaflet-popup-tip { background: var(--bg-elevated) !important; }
460  [data-theme="dark"] .leaflet-tile-pane { filter: brightness(0.65) invert(1) contrast(0.85) hue-rotate(180deg) saturate(0.4) brightness(1.1); }
461
462  /* --- Modal --- */
บรรทัด 325–357: .detail-section .detail-grid และตัวเลข KPI
บรรทัด 358–439: .day-list (เลื่อนในตัวและแถบเลื่อนเล็ก) .day-panel .day-head .day-stats รายการสถานที่ .poi-list .poi-item เลขลำดับ ข้อมูลเมตา และปุ่มของการ์ด (➜ renderDetail() ใน frontend/app.js)
บรรทัด 440–462: ส่วนแผนที่: .leaflet-container และฟิลเตอร์ให้ภาพแผนที่มืดในธีมมืด
บรรทัด 463–636  หน้าต่าง โมดัล และการสุ่มใหม่
463  .modal {
464    position: fixed; inset: 0; z-index: 1000;
465    display: none;
466    align-items: center; justify-content: center;
467  }
468  .modal.open { display: flex; }
469  .modal-backdrop {
470    position: absolute; inset: 0;
471    background: rgba(2,6,23,0.7);
472    backdrop-filter: blur(8px);
473    animation: fadeIn 200ms ease both;
474  }
475  .modal-card {
476    position: relative;
477    width: 92%; max-width: 620px;
478    max-height: 80vh;
479    display: flex; flex-direction: column;
480    padding: 1.5rem;
481    box-shadow: var(--shadow-lg);
482    border-radius: 20px;
483    animation: scaleIn 280ms cubic-bezier(0.34, 1.56, 0.64, 1) both;
484    overflow: hidden;
485    background: #0d0b09;
486  }
487  [data-theme="light"] .modal-card {
488    background: #ffffff;
489  }
490  .modal-body {
491    flex: 1;
492    overflow-y: auto;
493    overflow-x: hidden;
494    overscroll-behavior: contain;
495  }
496  .modal-body::-webkit-scrollbar { width: 6px; }
497  .modal-body::-webkit-scrollbar-track { background: transparent; }
498  .modal-body::-webkit-scrollbar-thumb { background: var(--border-default); border-radius: 3px; }
499  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
500  @keyframes scaleIn { from { opacity: 0; transform: scale(0.92); } to { opacity: 1; transform: scale(1); } }
501  .modal-head {
502    display: flex; justify-content: space-between; align-items: flex-start;
503    margin-bottom: 0.75rem;
504  }
505  .modal-head-actions { display: flex; gap: 0.5rem; flex-shrink: 0; margin-left: 0.75rem; }
506  .modal-head-actions a.icon-btn { text-decoration: none; }
507  .modal-head-actions a.icon-btn:hover { color: var(--accent-primary); }
508  .modal-sub { font-size: 0.85rem; color: var(--text-tertiary); margin-top: 0.25rem; }
509  /* swap modal search bar */
510  .modal-search { margin-bottom: 0.75rem; }
511  .modal-search input {
512    width: 100%; box-sizing: border-box;
513    padding: 0.6rem 1rem;
514    background: var(--bg-elevated);
515    border: 1px solid var(--border-subtle);
516    border-radius: var(--radius-md);
517    color: var(--text-primary);
518    font-size: 0.93rem;
519    outline: none;
520    transition: var(--transition);
521  }
522  .modal-search input:focus { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(255,109,53,0.15); }
523
524  /* Re-shuffle button */
525  .reshuffle-btn {
526    display: inline-flex; align-items: center; gap: 0.45rem;
527    padding: 0.5rem 1.1rem;
528    background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(6,182,212,0.18));
529    border: 1px solid rgba(99,102,241,0.4);
530    border-radius: var(--radius-md);
531    color: var(--text-primary);
532    font-size: 0.85rem; font-weight: 600;
533    cursor: pointer;
534    transition: var(--transition);
535  }
536  .reshuffle-btn:hover { background: linear-gradient(135deg, rgba(99,102,241,0.32), rgba(6,182,212,0.28)); border-color: var(--accent-primary); }
537  .reshuffle-btn svg { width: 15px; height: 15px; stroke: var(--accent-primary); }
538  /* Blur overlay while reshuffling */
539  .detail-section { transition: var(--transition); }
540  .detail-section.reshuffling {
541    pointer-events: none;
542  }
543  /* Blur everything EXCEPT the spinner overlay */
544  .detail-section.reshuffling > *:not(#reshuffleOverlay) {
545    filter: blur(6px) saturate(0.3) brightness(0.7);
546    opacity: 0.45;
547    transition: filter 0.35s ease, opacity 0.35s ease;
548  }
549
550  /* Reshuffle animated overlay (injected by JS) */
551  #reshuffleOverlay {
552    position: absolute;
553    inset: 0;
554    display: flex;
555    align-items: center;
556    justify-content: center;
557    z-index: 50;
558    pointer-events: none;
559    animation: fadeIn 250ms ease;
560    border-radius: var(--radius-lg);
561  }
562  .reshuffle-overlay-inner {
563    display: flex;
564    flex-direction: column;
565    align-items: center;
566    gap: 0.8rem;
567    padding: 1.5rem 2.8rem;
568    background: rgba(10, 14, 26, 0.6);
569    backdrop-filter: blur(8px);
570    -webkit-backdrop-filter: blur(8px);
571    border-radius: var(--radius-xl);
572    border: 1px solid rgba(34, 211, 238, 0.35);
573    box-shadow: 0 0 50px rgba(34, 211, 238, 0.15), inset 0 1px 0 rgba(255,255,255,0.06);
574  }
575  .reshuffle-ring {
576    width: 54px; height: 54px;
577    animation: spin 0.85s linear infinite;
578    filter: drop-shadow(0 0 10px rgba(34, 211, 238, 0.7));
579  }
580  .reshuffle-overlay-inner span {
581    font-size: 0.95rem;
582    font-weight: 600;
583    color: var(--accent-glow);
584    letter-spacing: 0.03em;
585  }
586
587  .cat-filter {
588    display: flex; flex-wrap: wrap; gap: 0.4rem;
589    padding-bottom: 0.85rem;
590    margin-bottom: 0.75rem;
591    border-bottom: 1px solid var(--border-subtle);
592  }
593  .cat-btn {
594    padding: 0.35rem 0.75rem;
595    background: var(--bg-elevated);
596    border: 1px solid var(--border-subtle);
597    border-radius: 999px;
598    font-size: 0.78rem;
599    color: var(--text-secondary);
600    transition: var(--transition);
601  }
602  .cat-btn:hover { color: var(--text-primary); border-color: var(--border-default); }
603  .cat-btn.active {
604    background: var(--grad-cta); color: white; border-color: transparent;
605    box-shadow: var(--shadow-sm);
606  }
607
608  .swap-list {
609    overflow-y: auto;
610    flex: 1;
611    list-style: none;
612    margin: 0;
613    padding: 0;
614    width: 100%;
615  }
616  .swap-list::-webkit-scrollbar { width: 6px; }
617  .swap-list::-webkit-scrollbar-thumb { background: var(--border-default); border-radius: 3px; }
618  .swap-option {
619    display: flex; justify-content: space-between; align-items: center;
620    padding: 0.7rem 0.85rem;
621    margin: 0.3rem 1.75rem;
622    background: var(--bg-elevated);
623    border: 1px solid var(--border-subtle);
624    border-radius: var(--radius-md);
625    cursor: pointer;
626    transition: var(--transition);
627  }
628  .swap-option:hover { border-color: var(--accent-primary); transform: scale(1.025); box-shadow: 0 4px 16px rgba(255,109,53,0.2); background: var(--bg-surface); }
629  .swap-option .opt-info b { font-size: 0.92rem; }
630  .swap-option .opt-info .meta { font-size: 0.75rem; color: var(--text-tertiary); margin-top: 0.15rem; display: block; }
631  .empty-msg {
632    text-align: center; color: var(--text-muted);
633    padding: 2rem 0; font-size: 0.9rem;
634  }
635
636  /* --- Toasts --- */
บรรทัด 463–507: .modal .modal-backdrop .modal-card .modal-head .modal-body และอนิเมชัน fadeIn scaleIn (ใช้กับโมดัลสลับสถานที่ แผนทางเลือก และรายละเอียดสถานที่/โรงแรม) รวมถึงกลุ่มปุ่มมุมขวาบน .modal-head-actions (ปุ่มหมุด Google Maps และปุ่มปิด)
บรรทัด 508–521: ช่องค้นหาในโมดัลสลับสถานที่ (➜ filterSwapList() ใน frontend/app.js)
บรรทัด 522–547: ปุ่ม Re-shuffle และการเบลอส่วนรายละเอียดระหว่างสุ่ม (.detail-section.reshuffling)
บรรทัด 548–584: ตัวครอบและวงแหวนหมุนของ #reshuffleOverlay ที่ ➜ reshufflePackage() ใน frontend/app.js แทรกเข้ามา
บรรทัด 585–636: ตัวกรองหมวด .cat-filter .cat-btn และรายการตัวเลือก .swap-option ของ ➜ renderSwapList() ใน frontend/app.js
บรรทัด 637–711  แจ้งเตือน หน้าจอแคบ และหมุดแผนที่
637  .toast-container {
638    position: fixed; top: 90px; right: 1.5rem; z-index: 1100;
639    display: flex; flex-direction: column; gap: 0.5rem;
640    pointer-events: none;
641  }
642  .toast {
643    padding: 0.85rem 1.1rem;
644    background: var(--bg-elevated);
645    border: 1px solid var(--border-default);
646    border-radius: var(--radius-md);
647    box-shadow: var(--shadow-lg);
648    font-size: 0.9rem;
649    color: var(--text-primary);
650    display: flex; align-items: center; gap: 0.6rem;
651    animation: toastIn 300ms ease both;
652    pointer-events: auto;
653    min-width: 240px;
654  }
655  .toast.ok { border-color: rgba(16,185,129,0.4); }
656  .toast.error { border-color: rgba(239,68,68,0.4); }
657  .toast.loading { border-color: rgba(245,158,11,0.4); }
658  .toast .toast-icon { flex-shrink: 0; width: 18px; height: 18px; }
659  .toast.ok .toast-icon { color: var(--accent-success); }
660  .toast.error .toast-icon { color: var(--accent-danger); }
661  .toast.loading .toast-icon { color: var(--accent-warning); animation: spin 1s linear infinite; }
662  @keyframes toastIn { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
663  @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
664
665  /* --- Responsive --- */
666  @media (max-width: 980px) {
667
668    .packages-grid { grid-template-columns: 1fr; }
669    .detail-grid { grid-template-columns: 1fr; }
670    .map-wrap { position: static; }
671    #map { height: 400px; }
672    .topbar { padding: 1rem; }
673    .section-head { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
674    .detail-actions { flex-wrap: wrap; }
675  }
676
677  /* --- Map custom markers --- */
678  .map-hotel-marker {
679    width: 40px; height: 40px;
680    background: var(--grad-cta);
681    border: 3px solid white;
682    border-radius: 50%;
683    display: flex; align-items: center; justify-content: center;
684    font-size: 18px;
685    box-shadow: 0 4px 12px rgba(0,0,0,0.4), 0 0 0 4px rgba(6,182,212,0.25);
686  }
687  .map-poi-marker {
688    width: 36px; height: 36px;
689    background: var(--c, #06b6d4);
690    border: 2px solid white;
691    border-radius: 50%;
692    display: flex; align-items: center; justify-content: center;
693    font-weight: 700;
694    color: white;
695    box-shadow: 0 4px 10px rgba(0,0,0,0.35);
696    font-feature-settings: 'tnum';
697    position: relative;
698  }
699  .map-poi-marker .d {
700    font-size: 11px;
701    line-height: 1;
702    margin-bottom: -2px;
703    opacity: 0.85;
704  }
705  .map-poi-marker .p {
706    font-size: 14px;
707    line-height: 1;
708    font-weight: 800;
709  }
710
711  /* === User-requested fixes === */
บรรทัด 637–665: .toast-container .toast (ok error loading) และอนิเมชัน toastIn slideUp ของ ➜ showToast() ใน frontend/app.js
บรรทัด 666–677: @media (max-width: 980px) ปรับโครงเป็นคอลัมน์เดียว
บรรทัด 678–711: หมุดแผนที่ .map-poi-marker (วงกลมสีของวันพร้อมเลขวันและลำดับ) และ .map-hotel-marker ที่ ➜ drawOnMap() ใน frontend/app.js สร้าง
บรรทัด 712–783  ชุดแก้ไขตามคำขอ
712
713  /* 1) Remove number spinner arrows (Chrome/Safari/Firefox) */
714  input[type=number]::-webkit-inner-spin-button,
715  input[type=number]::-webkit-outer-spin-button {
716    -webkit-appearance: none;
717    margin: 0;
718  }
719  input[type=number] { -moz-appearance: textfield; appearance: textfield; }
720
721
722  .date-summary {
723    font-size: 0.78rem;
724    color: var(--text-tertiary);
725    margin-top: 0.5rem;
726    padding: 0.4rem 0.6rem;
727    background: var(--bg-elevated);
728    border-radius: 6px;
729    border-left: 3px solid var(--accent-primary);
730  }
731  .date-summary.invalid { border-left-color: var(--accent-danger); color: var(--accent-danger); }
732  .date-summary.oneday {
733    border-left-color: #10b981; color: #10b981;
734    background: rgba(16,185,129,0.08);
735  }
736
737  /* One-day-trip lock badge (inline beside title) */
738  .hotel-lock-badge {
739    display: inline-flex; align-items: center;
740    font-size: 0.7rem; font-weight: 600;
741    background: rgba(16,185,129,0.15); color: #10b981;
742    border: 1px solid rgba(16,185,129,0.3);
743    border-radius: 20px; padding: 2px 9px; white-space: nowrap; flex-shrink: 0;
744  }
745
746  /* 4) Smaller "เพิ่มสถานที่" button - looks like POI item with + icon */
747  .day-add {
748    display: flex; align-items: center; gap: 0.6rem;
749    width: 100%;
750    margin-top: 0.5rem;
751    padding: 0.55rem 0.75rem;
752    background: transparent;
753    border: 1px dashed var(--border-default);
754    border-radius: var(--radius-sm);
755    color: var(--text-tertiary);
756    font-size: 0.88rem;
757    text-align: left;
758    transition: var(--transition);
759  }
760  .day-add:hover {
761    border-color: var(--accent-primary);
762    border-style: solid;
763    color: var(--accent-primary);
764    background: var(--bg-elevated);
765  }
766  .day-add svg { width: 16px; height: 16px; flex-shrink: 0; }
767  .day-add .add-num {
768    width: 28px; height: 28px; flex-shrink: 0;
769    border: 1px dashed currentColor;
770    border-radius: 50%;
771    display: flex; align-items: center; justify-content: center;
772    opacity: 0.7;
773  }
774
775  /* 5) FIX: gentler dark mode tile filter (was breaking map appearance) */
776  [data-theme="dark"] .leaflet-tile-pane {
777    filter: brightness(0.85) saturate(0.7) hue-rotate(180deg) invert(0.92);
778  }
779  .leaflet-control-zoom a {
780    background: var(--bg-elevated) !important;
781    color: var(--text-primary) !important;
782    border-color: var(--border-default) !important;
783  }
บรรทัด 712–737: การปรับช่องตัวเลข สรุปวันที่ (.date-summary สถานะ oneday/invalid) และรายละเอียดเล็กน้อยที่ปรับตามคำขอ
บรรทัด 738–766: ป้ายล็อกของทริปวันเดียวและการ์ดโรงแรมแบบล็อก (➜ setOneDayTripMode() ใน frontend/app.js)
บรรทัด 767–783: ปุ่ม .day-add (เพิ่มสถานที่) และการปรับภาพแผนที่ในธีมมืด
บรรทัด 784–843  พื้นหลังออโรรา
784  .leaflet-control-attribution {
785    background: var(--bg-elevated) !important;
786    color: var(--text-tertiary) !important;
787    border-radius: 4px;
788    font-size: 10px;
789  }
790
791  /* === V3 Updates: Aurora background, Flatpickr, scrollable select === */
792
793
794  /* New background layers */
795  .bg-layers {
796    position: fixed; inset: 0; z-index: -1;
797    overflow: hidden;
798    pointer-events: none;
799  }
800
801  /* Subtle grid */
802  .bg-grid {
803    position: absolute; inset: 0;
804    background-image:
805      linear-gradient(rgba(148,163,184,0.04) 1px, transparent 1px),
806      linear-gradient(90deg, rgba(148,163,184,0.04) 1px, transparent 1px);
807    background-size: 60px 60px;
808    mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
809    -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
810  }
811  [data-theme="light"] .bg-grid {
812    background-image:
813      linear-gradient(rgba(15,23,42,0.04) 1px, transparent 1px),
814      linear-gradient(90deg, rgba(15,23,42,0.04) 1px, transparent 1px);
815  }
816
817  /* Aurora orbs - animated */
818  .bg-aurora { position: absolute; inset: 0; }
819  .bg-aurora .orb {
820    position: absolute;
821    border-radius: 50%;
822    filter: blur(140px);
823    opacity: 0.55;
824    will-change: transform;
825  }
826  .bg-aurora .orb-1 { width: 520px; height: 520px; background: #ff6d35; top: -80px; left: -120px; animation: drift1 22s ease-in-out infinite alternate; }
827  .bg-aurora .orb-2 { width: 600px; height: 600px; background: #b84000; top: 25%; right: -200px; animation: drift2 28s ease-in-out infinite alternate; }
828  .bg-aurora .orb-3 { width: 460px; height: 460px; background: #f97316; bottom: -120px; left: 25%; opacity: 0.35; animation: drift3 30s ease-in-out infinite alternate; }
829  .bg-aurora .orb-4 { width: 380px; height: 380px; background: #cc3300; top: 55%; left: 8%; opacity: 0.10; animation: drift4 26s ease-in-out infinite alternate; }
830  .bg-aurora .orb-5 { width: 420px; height: 420px; background: #ff7722; top: 5%; left: 45%; opacity: 0.08; animation: drift5 32s ease-in-out infinite alternate; }
831
832  [data-theme="light"] .bg-aurora .orb { opacity: 0.22; }
833  [data-theme="light"] .bg-aurora .orb-3,
834  [data-theme="light"] .bg-aurora .orb-4,
835  [data-theme="light"] .bg-aurora .orb-5 { opacity: 0.15; }
836
837  @keyframes drift1 { from { transform: translate(0, 0) scale(1); } to { transform: translate(120px, 80px) scale(1.15); } }
838  @keyframes drift2 { from { transform: translate(0, 0) scale(1); } to { transform: translate(-150px, 100px) scale(1.1); } }
839  @keyframes drift3 { from { transform: translate(0, 0) scale(1); } to { transform: translate(80px, -120px) scale(0.9); } }
840  @keyframes drift4 { from { transform: translate(0, 0) scale(1); } to { transform: translate(180px, -80px) scale(1.2); } }
841  @keyframes drift5 { from { transform: translate(0, 0) scale(1); } to { transform: translate(-100px, 120px) scale(1.1); } }
842
843  /* Subtle film grain (SVG noise) */
บรรทัด 784–843: .bg-layers ตาราง .bg-grid ลูกแสงห้าก้อนที่เคลื่อนช้า ๆ (@keyframes drift1–drift5) และเกรนฟิล์ม SVG (ลักษณะตามองค์ประกอบใน ➜ frontend/index.html)
บรรทัด 844–1024  ช่องวันที่และธีมของ flatpickr
844  .bg-grain {
845    position: absolute; inset: 0;
846    background-image: url("data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PScwIDAgMjAwIDIwMCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJz48ZmlsdGVyIGlkPSdub2lzZUZpbHRlcic+PGZlVHVyYnVsZW5jZSB0eXBlPSdmcmFjdGFsTm9pc2UnIGJhc2VGcmVxdWVuY3k9JzAuOScgbnVtT2N0YXZlcz0nMScgc3RpdGNoVGlsZXM9J3N0aXRjaCcvPjwvZmlsdGVyPjxyZWN0IHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEwMCUnIGZpbHRlcj0ndXJsKCNub2lzZUZpbHRlciknLz48L3N2Zz4=");
847    opacity: 0.04;
848    mix-blend-mode: overlay;
849  }
850  [data-theme="light"] .bg-grain { opacity: 0.06; mix-blend-mode: multiply; }
851
852
853  /* === New date range input (single field for Flatpickr) === */
854  .date-range-input {
855    display: flex; align-items: center; gap: 0.6rem;
856    background: var(--bg-elevated);
857    border: 1px solid var(--border-subtle);
858    border-radius: var(--radius-md);
859    padding: 0.65rem 1rem;
860    cursor: pointer;
861    transition: var(--transition);
862  }
863  .date-range-input:hover { border-color: var(--border-default); }
864  .date-range-input:focus-within { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(255,109,53,0.15); }
865  .date-range-input .date-icon { width: 18px; height: 18px; color: var(--text-tertiary); flex-shrink: 0; pointer-events: none; }
866  .date-range-input input {
867    flex: 1; padding: 0; border: none; outline: none;
868    background: transparent;
869    font-size: 0.95rem; font-weight: 600;
870    color: var(--text-primary);
871    cursor: pointer;
872  }
873  .date-range-input input::placeholder { color: var(--text-tertiary); font-weight: 500; }
874
875  /* === Flatpickr theming === */
876  .flatpickr-calendar {
877    background: #1a1208 !important;
878    border: 1px solid var(--border-default) !important;
879    border-radius: var(--radius-lg) !important;
880    box-shadow: 0 20px 60px rgba(0,0,0,0.6) !important;
881    font-family: var(--font-sans) !important;
882    width: 320px !important;
883    padding: 0.5rem !important;
884    z-index: 99999 !important;
885  }
886  [data-theme="light"] .flatpickr-calendar { background: #ffffff !important; }
887
888  /* Year input — ซ่อน default arrows, ใช้ปุ่ม custom แทน */
889  .flatpickr-current-month .numInputWrapper { pointer-events: auto !important; }
890  .flatpickr-current-month input.cur-year {
891    pointer-events: auto !important;
892    cursor: default !important;
893    background: transparent !important;
894    border: none !important;
895    padding: 0 2px !important;
896    color: var(--text-primary) !important;
897    font-weight: 700 !important;
898  }
899  .numInputWrapper span.arrowUp,
900  .numInputWrapper span.arrowDown { display: none !important; }
901
902  /* Custom year nav buttons */
903  .fp-year-prev, .fp-year-next {
904    display: inline-flex; align-items: center; justify-content: center;
905    width: 22px; height: 22px; border-radius: 50%;
906    cursor: pointer; font-size: 1rem; font-weight: 700;
907    color: var(--text-secondary);
908    background: transparent;
909    border: none;
910    transition: background 0.15s, color 0.15s;
911    user-select: none;
912    vertical-align: middle;
913  }
914  .fp-year-prev:hover, .fp-year-next:hover {
915    background: rgba(255,109,53,0.15);
916    color: var(--accent-primary);
917  }
918  .flatpickr-calendar.arrowTop:before,
919  .flatpickr-calendar.arrowTop:after { border-bottom-color: var(--border-default) !important; }
920  .flatpickr-calendar.arrowBottom:before,
921  .flatpickr-calendar.arrowBottom:after { border-top-color: var(--border-default) !important; }
922
923  .flatpickr-months {
924    padding: 0.5rem 0 0.75rem !important;
925    border-bottom: 1px solid var(--border-subtle);
926  }
927  .flatpickr-month {
928    background: transparent !important;
929    color: var(--text-primary) !important;
930    height: 36px !important;
931    display: flex !important;
932    align-items: center !important;
933    justify-content: center !important;
934  }
935  .flatpickr-current-month {
936    color: var(--text-primary) !important;
937    font-size: 0.95rem !important;
938    font-weight: 700 !important;
939    padding: 0 !important;
940    display: flex !important;
941    align-items: center !important;
942    justify-content: center !important;
943    gap: 4px !important;
944    width: 100% !important;
945    position: static !important;
946  }
947  .flatpickr-current-month .numInputWrapper { color: var(--text-primary) !important; }
948  .flatpickr-current-month input.cur-year {
949    color: var(--text-primary) !important;
950    font-weight: 700 !important;
951  }
952  .flatpickr-monthDropdown-months {
953    background: #1a1208 !important;
954    color: var(--text-primary) !important;
955    font-weight: 600 !important;
956    border-radius: 6px;
957  }
958  [data-theme="light"] .flatpickr-monthDropdown-months { background: #ffffff !important; }
959  .flatpickr-monthDropdown-month { background: #1a1208 !important; }
960  [data-theme="light"] .flatpickr-monthDropdown-month { background: #ffffff !important; }
961
962  .flatpickr-prev-month, .flatpickr-next-month {
963    color: var(--text-secondary) !important;
964    fill: var(--text-secondary) !important;
965    padding: 8px !important;
966    border-radius: 8px;
967    transition: var(--transition);
968  }
969  .flatpickr-prev-month:hover, .flatpickr-next-month:hover {
970    color: var(--accent-glow) !important;
971    fill: var(--accent-glow) !important;
972    background: var(--bg-base) !important;
973  }
974
975  .flatpickr-weekdays { background: transparent !important; padding: 0.5rem 0; }
976  .flatpickr-weekday {
977    color: var(--text-tertiary) !important;
978    font-weight: 600 !important;
979    font-size: 0.75rem !important;
980    text-transform: uppercase;
981    letter-spacing: 0.04em;
982  }
983
984  .flatpickr-day {
985    color: var(--text-secondary) !important;
986    border-radius: 8px !important;
987    font-weight: 500 !important;
988    transition: var(--transition);
989    border: 1px solid transparent !important;
990    height: 38px !important;
991    line-height: 38px !important;
992    margin: 1px 0;
993  }
994  .flatpickr-day:hover {
995    background: var(--bg-base) !important;
996    color: var(--text-primary) !important;
997  }
998  .flatpickr-day.today {
999    border-color: var(--accent-primary) !important;
1000    color: var(--accent-glow) !important;
1001  }
1002  .flatpickr-day.today:hover { background: var(--accent-primary) !important; color: white !important; }
1003  .flatpickr-day.selected,
1004  .flatpickr-day.startRange,
1005  .flatpickr-day.endRange,
1006  .flatpickr-day.selected.inRange,
1007  .flatpickr-day.startRange.inRange,
1008  .flatpickr-day.endRange.inRange {
1009    background: var(--accent-primary) !important;
1010    border-color: var(--accent-primary) !important;
1011    color: white !important;
1012    box-shadow: 0 4px 12px rgba(255,109,53,0.3);
1013  }
1014  .flatpickr-day.inRange {
1015    background: rgba(255,109,53,0.15) !important;
1016    border-color: transparent !important;
1017    color: var(--text-primary) !important;
1018    box-shadow: none !important;
1019  }
1020  .flatpickr-day.startRange { border-radius: 8px 0 0 8px !important; }
1021  .flatpickr-day.endRange { border-radius: 0 8px 8px 0 !important; }
1022  .flatpickr-day.startRange.endRange { border-radius: 8px !important; }
1023  .flatpickr-day.flatpickr-disabled,
1024  .flatpickr-day.prevMonthDay,
บรรทัด 844–865: .date-range-input ช่องวันที่ช่องเดียว (โฟกัส และ placeholder)
บรรทัด 866–1024: ตกแต่งปฏิทิน flatpickr ให้เข้ากับธีม: เดือน ปี ปุ่ม ‹ › ที่เพิ่มด้วย ➜ initDateRange() ใน frontend/app.js ชื่อวัน วันที่ที่ชี้ ช่วงที่เลือก และวันของเดือนอื่น
บรรทัด 1025–1118  รุ่น V4–V6
1025  .flatpickr-day.nextMonthDay {
1026    color: var(--text-muted) !important;
1027    opacity: 0.4;
1028  }
1029
1030  .numInput, .numInputWrapper span {
1031    color: var(--text-primary) !important;
1032  }
1033  .flatpickr-time { background: var(--bg-elevated) !important; border-top: 1px solid var(--border-subtle); }
1034
1035  /* === V4 Updates === */
1036
1037
1038  /* 2) Custom scrollbars (whole page) */
1039  * { scrollbar-width: thin; scrollbar-color: var(--border-default) transparent; }
1040  *::-webkit-scrollbar { width: 10px; height: 10px; }
1041  *::-webkit-scrollbar-track { background: transparent; }
1042  *::-webkit-scrollbar-thumb {
1043    background: linear-gradient(180deg, var(--border-default), var(--border-strong));
1044    border-radius: 5px;
1045    border: 2px solid transparent;
1046    background-clip: padding-box;
1047  }
1048  *::-webkit-scrollbar-thumb:hover {
1049    background: linear-gradient(180deg, var(--accent-primary), var(--accent-glow));
1050    background-clip: padding-box;
1051    border: 2px solid transparent;
1052  }
1053  *::-webkit-scrollbar-corner { background: transparent; }
1054
1055  /* 3) Day toggles (filter routes on map by day) */
1056  .day-toggles {
1057    display: flex; flex-wrap: wrap; gap: 0.5rem;
1058    padding: 0.75rem;
1059    background: var(--bg-surface);
1060    backdrop-filter: blur(20px);
1061    -webkit-backdrop-filter: blur(20px);
1062    border: 1px solid var(--border-subtle);
1063    border-radius: var(--radius-md);
1064    margin-bottom: 0.75rem;
1065  }
1066  .day-toggle {
1067    display: inline-flex; align-items: center; gap: 0.5rem;
1068    padding: 0.4rem 0.85rem;
1069    background: var(--bg-elevated);
1070    border: 1px solid var(--border-subtle);
1071    border-radius: 999px;
1072    font-size: 0.82rem; font-weight: 600;
1073    color: var(--text-tertiary);
1074    transition: var(--transition);
1075    cursor: pointer;
1076  }
1077  .day-toggle .day-dot {
1078    width: 8px; height: 8px; border-radius: 50%;
1079    background: var(--c, var(--accent-primary));
1080    opacity: 0.4;
1081    transition: var(--transition);
1082  }
1083  .day-toggle.active {
1084    background: var(--bg-base);
1085    color: var(--text-primary);
1086    border-color: var(--c, var(--accent-primary));
1087    box-shadow: 0 0 0 1px var(--c, var(--accent-primary));
1088  }
1089  .day-toggle.active .day-dot {
1090    opacity: 1;
1091    box-shadow: 0 0 8px var(--c, var(--accent-primary));
1092  }
1093  .day-toggle:hover { color: var(--text-primary); }
1094  .day-toggle.show-all {
1095    background: var(--grad-cta);
1096    color: white;
1097    border-color: transparent;
1098  }
1099  .day-toggle.show-all:hover { opacity: 0.9; }
1100
1101  /* === V5: Validation error state === */
1102  .input-with-unit.has-error,
1103  .date-range-input.has-error,
1104  .select-input.has-error {
1105    border-color: var(--accent-danger) !important;
1106    box-shadow: 0 0 0 3px rgba(239,68,68,0.18) !important;
1107  }
1108  .input-with-unit.has-error .unit { color: var(--accent-danger); }
1109
1110  @keyframes shake {
1111    0%, 100% { transform: translateX(0); }
1112    20%, 60% { transform: translateX(-4px); }
1113    40%, 80% { transform: translateX(4px); }
1114  }
1115  .has-error { animation: shake 320ms ease; }
1116
1117  /* === V6: Subtle gradient body background === */
1118  [data-theme="dark"] body {
บรรทัด 1025–1088: แถบเลื่อนทั้งหน้า ปุ่มสลับวัน .day-toggle และสถานะ active ของ ➜ renderDayToggles() ใน frontend/app.js
บรรทัด 1089–1104: สถานะผิดพลาดของช่องกรอก .has-error พร้อมอนิเมชันสั่น shake (➜ highlightField() ใน frontend/app.js)
บรรทัด 1105–1118: พื้นหลังไล่สีอ่อนของ body
บรรทัด 1119–1249  รุ่น V7–V8
1119    background:
1120      radial-gradient(ellipse at top left,    rgba(6,182,212,0.08), transparent 50%),
1121      radial-gradient(ellipse at bottom right, rgba(167,139,250,0.08), transparent 50%),
1122      linear-gradient(180deg, #0a0e1a 0%, #0d1424 50%, #0a0e1a 100%);
1123  }
1124  [data-theme="light"] body {
1125    background:
1126      radial-gradient(ellipse at top left,    rgba(6,182,212,0.06), transparent 50%),
1127      radial-gradient(ellipse at bottom right, rgba(167,139,250,0.06), transparent 50%),
1128      linear-gradient(180deg, #f6f7fb 0%, #eef2f9 50%, #f6f7fb 100%);
1129  }
1130
1131  /* === V7: Hide-all button & realistic schedule == */
1132  .day-toggle.hide-all {
1133    background: rgba(239, 68, 68, 0.15);
1134    color: #fca5a5;
1135    border-color: rgba(239, 68, 68, 0.4);
1136  }
1137  .day-toggle.hide-all:hover {
1138    background: rgba(239, 68, 68, 0.25);
1139    color: #fecaca;
1140  }
1141  .day-toggle svg { flex-shrink: 0; }
1142
1143  /* === V8: Algorithm selector === */
1144  .algo-segment {
1145    display: grid;
1146    grid-template-columns: repeat(3, 1fr);
1147    gap: 4px;
1148    background: var(--bg-elevated);
1149    padding: 4px;
1150    border-radius: var(--radius-md);
1151    border: 1px solid var(--border-subtle);
1152  }
1153  .algo-segment button {
1154    padding: 0.65rem 0.5rem;
1155    border-radius: 8px;
1156    font-weight: 600;
1157    font-size: 0.86rem;
1158    color: var(--text-tertiary);
1159    transition: var(--transition);
1160  }
1161  .algo-segment button:hover { color: var(--text-primary); background: rgba(255,255,255,0.04); }
1162  .algo-segment button.active {
1163    background: var(--grad-cta);
1164    color: white;
1165    box-shadow: 0 4px 10px rgba(255,109,53,0.3);
1166  }
1167
1168
1169  /* ── Hotel option card ── */
1170  .hotel-card {
1171    display: flex; align-items: center; gap: 14px;
1172    padding: 14px 16px; border-radius: var(--radius-md);
1173    background: var(--bg-surface);
1174    border: 1px solid var(--border-default);
1175    cursor: pointer; transition: var(--transition);
1176    user-select: none;
1177  }
1178  .hotel-card:hover { border-color: var(--accent-cyan); }
1179  .hotel-card.hotel-card-locked {
1180    border-color: #10b981;
1181    background: rgba(16,185,129,0.06);
1182    cursor: default;
1183  }
1184  .hotel-card-icon {
1185    font-size: 1.5rem; flex-shrink: 0;
1186    width: 42px; height: 42px;
1187    display: flex; align-items: center; justify-content: center;
1188    background: var(--bg-elevated);
1189    border-radius: var(--radius-sm);
1190  }
1191  .hotel-card-body { flex: 1; min-width: 0; }
1192  .hotel-card-title-row {
1193    display: flex; align-items: center; gap: 8px;
1194    margin-bottom: 2px;
1195  }
1196  .hotel-card-title {
1197    font-weight: 600; font-size: 0.9rem;
1198    color: var(--text-primary);
1199  }
1200  .hotel-card-switch {
1201    flex-shrink: 0; display: flex; align-items: center;
1202  }
1203  .hotel-card-switch input[type="checkbox"] { display: none; }
1204  .toggle-track {
1205    width: 44px; height: 24px;
1206    background: var(--bg-elevated);
1207    border: 1.5px solid var(--border-default);
1208    border-radius: 12px;
1209    position: relative; cursor: pointer;
1210    transition: background 0.2s ease, border-color 0.2s ease;
1211    display: block;
1212  }
1213  input[type="checkbox"]:checked + .toggle-track,
1214  input[type="checkbox"]:checked + label.toggle-track {
1215    background: var(--accent-primary);
1216    border-color: var(--accent-primary);
1217  }
1218  .toggle-thumb {
1219    position: absolute; top: 2px; left: 2px;
1220    width: 18px; height: 18px;
1221    background: white; border-radius: 50%;
1222    transition: transform 0.2s ease;
1223    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
1224  }
1225  input[type="checkbox"]:checked + .toggle-track .toggle-thumb {
1226    transform: translateX(18px);
1227  }
1228  .hotel-lock-badge {
1229    font-size: 0.68rem; font-weight: 700;
1230    background: #10b981; color: white;
1231    padding: 1px 7px; border-radius: 99px;
1232    letter-spacing: 0.02em;
1233  }
1234  .date-summary.oneday { border-left-color: #10b981; color: #10b981; }
1235
1236  /* ── Distance connectors between POIs ── */
1237  .dist-connector {
1238    display: flex; align-items: center; gap: 0.4rem;
1239    padding: 0.05rem 0.5rem;
1240    list-style: none;
1241  }
1242  .dist-line {
1243    flex: 1; height: 1px;
1244    background: linear-gradient(90deg, transparent, var(--border-default), transparent);
1245  }
1246  .dist-badge {
1247    font-size: 0.68rem; color: var(--text-muted);
1248    white-space: nowrap;
1249    padding: 1px 7px;
บรรทัด 1119–1131: ปุ่มซ่อนทุกวันและตารางเวลาแบบสมจริง
บรรทัด 1132–1166: ตัวเลือกอัลกอริทึม .algo-segment (ใน ➜ initAlgoControl() ใน frontend/app.js)
บรรทัด 1167–1237: การ์ดโรงแรม .hotel-card สวิตช์ .toggle-track ป้ายล็อก และป้ายระยะทาง .dist-badge ในรายการ
บรรทัด 1238–1249: รายละเอียดป้ายระยะทาง
บรรทัด 1250–1587  โครงหน้าแบบใหม่ (หน้า landing และเมนูจังหวัด)
1250    background: var(--bg-elevated);
1251    border: 1px solid var(--border-subtle);
1252    border-radius: 8px;
1253    font-feature-settings: 'tnum';
1254    letter-spacing: 0.01em;
1255  }
1256
1257
1258  /* ================================================================
1259     NEW TRIPVENTURE LAYOUT
1260     ================================================================ */
1261
1262  .brand-trip { color: var(--accent-primary); }
1263  .topbar { padding: 0.65rem 2.5rem; }
1264
1265  /* Body background */
1266  html, body { background: #0d0b09 !important; }
1267  html[data-theme="light"], html[data-theme="light"] body { background: #ffffff !important; }
1268
1269  /* ── Landing screen ── */
1270  .landing-screen {
1271    min-height: 100vh;
1272    min-height: 100dvh;
1273    position: relative;
1274    background: #ffffff;
1275    overflow: visible;   /* ไม่ตัดเมนูเลือกจังหวัดที่ยื่นลงมาเกินหน้าจอแรก (เดิม hidden ทำให้ STEP 2 ทับเมนู) */
1276    display: flex; flex-direction: column;
1277  }
1278  [data-theme="dark"] .landing-screen {
1279    background: #0d0b09;
1280  }
1281
1282  /* ── Hero ── */
1283  .hero-visual {
1284    position: absolute;
1285    top: 0; left: 0; right: 0;
1286    width: 100%;
1287    height: 75vh;
1288    overflow: hidden;
1289    display: flex;
1290    align-items: center;
1291    justify-content: center;
1292    padding: 0;
1293  }
1294  .hero-bg {
1295    position: absolute; inset: 0;
1296    background-size: cover;
1297    background-position: center bottom;
1298    transform: scale(1.03);
1299    transition: transform 8s ease;
1300  }
1301  .hero-visual:hover .hero-bg { transform: scale(1.0); }
1302  .hero-overlay {
1303    position: absolute; inset: 0;
1304    background: linear-gradient(to bottom, rgba(8,5,2,0.42) 0%, rgba(8,5,2,0.28) 45%, rgba(8,5,2,0.68) 100%);
1305  }
1306  .hero-content {
1307    position: absolute; z-index: 2;
1308    top: 30%; left: 0; right: 0;
1309    transform: translateY(-50%);
1310    text-align: center;
1311    width: 100%;
1312    padding: 0 2rem;
1313    animation: slideUp 700ms ease both;
1314  }
1315  .hero-label {
1316    display: inline-block;
1317    font-size: 1rem; font-weight: 700;
1318    color: var(--accent-warm);
1319    text-transform: uppercase; letter-spacing: 0.14em;
1320    margin-bottom: 1.9rem;
1321    padding: 0.25rem 0.9rem; border-radius: 999px;
1322    background: rgba(255,255,255,0.88);
1323  }
1324  .hero-h1 {
1325    font-size: clamp(2.6rem, 5.5vw, 4.4rem);
1326    font-weight: 900; color: #fff;
1327    letter-spacing: -0.03em; line-height: 1.1;
1328    margin: 0 0 1rem; white-space: nowrap;
1329    text-shadow: 0 2px 24px rgba(0,0,0,0.5);
1330  }
1331  .hero-desc {
1332    font-size: 1rem; color: rgba(255,255,255,0.78);
1333    line-height: 1.7; margin: 0 auto; max-width: none; white-space: nowrap;
1334    text-shadow: 0 2px 16px rgba(0,0,0,0.6);
1335  }
1336
1337  /* ── Planner wrapper ── */
1338  .planner-wrapper {
1339    max-width: 1280px; width: 100%;
1340    position: relative;
1341    margin: auto auto 0; /* pins the panel to the bottom of the first screen */
1342    padding: 330px 2rem 1rem; /* top padding = min clearance for hero text on short screens */
1343    z-index: 10;
1344    pointer-events: none;
1345  }
1346  .planner-wrapper > * { pointer-events: auto; }
1347  .planner-panel {
1348    zoom: 0.9; /* scales the whole box and its contents uniformly */
1349    background: var(--bg-elevated);
1350    border: 1px solid var(--border-subtle);
1351    border-radius: var(--radius-xl);
1352    padding: 1.5rem 1.75rem 1.25rem;
1353    box-shadow: 0 16px 48px rgba(0,0,0,0.45);
1354    backdrop-filter: blur(24px);
1355    -webkit-backdrop-filter: blur(24px);
1356  }
1357  [data-theme="light"] .planner-panel {
1358    background: rgba(255,255,255,0.97);
1359    box-shadow: 0 16px 48px rgba(100,50,20,0.12);
1360  }
1361
1362  /* Header row */
1363  .planner-top-row {
1364    display: flex; align-items: center; gap: 0.75rem;
1365    margin-bottom: 1.1rem;
1366    padding-bottom: 0.9rem;
1367    border-bottom: 1px solid var(--border-subtle);
1368  }
1369  .planner-title { font-size: 1rem; font-weight: 700; flex: 1; }
1370  .ml-auto { margin-left: auto; }
1371
1372  /* Divider */
1373  .pf-divider {
1374    height: 1px; background: var(--border-subtle);
1375    margin: 1rem 0;
1376  }
1377
1378  /* Grid rows */
1379  .pf-grid {
1380    display: grid;
1381    grid-template-columns: 1fr 1fr 1.5fr 0.9fr;
1382    gap: 1rem;
1383    align-items: start;
1384  }
1385  .pf-grid-b {
1386    grid-template-columns: auto 1fr auto;  /* ที่พัก (กว้างเท่าเนื้อหา) + กล่อง Tips (ยืดเต็มที่เหลือ) + ปุ่มค้นหา */
1387    align-items: start;   /* ป้ายและปุ่มของทุกคอลัมน์อยู่ระนาบเดียวกัน */
1388  }
1389  .pf-col-search .pf-label { visibility: hidden; }
1390  .pf-algo-row { display: none; margin-top: 0.9rem; }
1391  .dev-mode .pf-algo-row { display: block; }
1392  .dev-btn { font-family: ui-monospace, Consolas, monospace; font-size: 0.8rem; font-weight: 700; }
1393  .dev-mode .dev-btn { color: #fff; background: var(--accent-primary, #ff6d35); border-color: transparent; }
1394  .pf-col { position: relative; }
1395  .pf-col-wide  { /* dates — wider */ }
1396  .pf-col-hotel { /* hotel toggle */ }
1397  .pf-col-algo  { /* algo segment */ }
1398  .pf-col-search { min-width: 148px; }
1399
1400  /* Labels */
1401  .pf-label {
1402    display: block;
1403    font-size: 0.73rem; font-weight: 600;
1404    color: var(--text-tertiary);
1405    text-transform: uppercase; letter-spacing: 0.07em;
1406    margin-bottom: 0.45rem;
1407    min-height: 1rem;
1408  }
1409
1410  /* Hint text below each control — reserves space */
1411  .pf-hint {
1412    font-size: 0.72rem; color: var(--text-muted);
1413    margin-top: 0.35rem; min-height: 1rem;
1414    line-height: 1.3;
1415  }
1416
1417  /* All controls same height */
1418  .planner-panel .select-input,
1419  .planner-panel .input-with-unit,
1420  .planner-panel .date-range-input,
1421  .planner-panel .counter-control,
1422  .planner-panel .hotel-card,
1423  .planner-panel .algo-segment { height: 48px; min-height: 48px; }
1424
1425  /* hotel card compact */
1426  .planner-panel .hotel-card {
1427    display: flex; align-items: center;
1428    padding: 0 0.85rem; gap: 0.6rem;
1429  }
1430
1431  /* algo segment height */
1432  .planner-panel .algo-segment {
1433    display: flex; align-items: center; padding: 4px;
1434  }
1435  .planner-panel .algo-segment button {
1436    flex: 1; height: 100%;
1437    display: flex; align-items: center; justify-content: center;
1438    gap: 5px;
1439    text-align: center;
1440    letter-spacing: 0;
1441  }
1442  .planner-panel .algo-segment button .btn-icon {
1443    display: inline-flex;
1444    align-items: center;
1445    width: 1em;
1446    justify-content: center;
1447    flex-shrink: 0;
1448  }
1449
1450  /* search button */
1451  .pf-col-search .cta-btn {
1452    height: 48px; width: 100%;
1453    padding: 0 1.25rem; font-size: 0.92rem;
1454  }
1455
1456
1457  /* Section backgrounds */
1458  .packages-section, .detail-section { background: #0d0b09; }
1459  html[data-theme="light"] .packages-section,
1460  html[data-theme="light"] .detail-section { background: #ffffff; }
1461
1462
1463  /* ── Province custom dropdown ── */
1464  .prov-select {
1465    position: relative;
1466    display: flex; align-items: center; gap: 0.55rem;
1467    height: 48px; min-height: 48px;
1468    padding: 0 0.9rem;
1469    background: var(--bg-elevated);
1470    border: 1.5px solid var(--border-subtle);
1471    border-radius: var(--radius-md);
1472    cursor: pointer;
1473    user-select: none;
1474    transition: border-color 0.18s, box-shadow 0.18s;
1475  }
1476  .prov-select:hover { border-color: var(--accent-primary); }
1477  .prov-select.open {
1478    border-color: var(--accent-primary);
1479    box-shadow: 0 0 0 3px rgba(255,109,53,0.18);
1480  }
1481  .prov-name { flex: 1; font-size: 0.9rem; font-weight: 600; color: var(--text-primary); }
1482  .prov-arrow {
1483    width: 16px; height: 16px; flex-shrink: 0;
1484    color: var(--text-tertiary);
1485    transition: transform 0.2s;
1486  }
1487  .prov-select.open .prov-arrow { transform: rotate(180deg); }
1488
1489  /* Dropdown panel */
1490  .prov-dropdown {
1491    position: absolute;
1492    top: calc(100% + 6px);
1493    left: 0; transform: translateY(-8px) scale(0.98);
1494    width: 280px; z-index: 999;
1495    background: var(--bg-elevated);
1496    border: 1.5px solid var(--border-subtle);
1497    border-radius: var(--radius-lg);
1498    box-shadow: 0 16px 48px rgba(0,0,0,0.45), 0 4px 16px rgba(0,0,0,0.3);
1499    backdrop-filter: blur(20px);
1500    overflow: hidden;
1501    opacity: 0;
1502    pointer-events: none;
1503    display: none;   /* ปิดอยู่ต้องไม่กินพื้นที่ (ไม่งั้นดันความสูงหน้าให้เลื่อนเกินจำเป็น) */
1504  }
1505  .prov-dropdown.open {
1506    display: block;
1507    opacity: 1; transform: translateY(0) scale(1);
1508    pointer-events: all;
1509    animation: provPop 0.18s ease both;
1510  }
1511  @keyframes provPop { from { opacity: 0; transform: translateY(-8px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
1512  @keyframes provPopUp { from { opacity: 0; transform: translateY(8px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
1513  /* เปิดขึ้นด้านบนเมื่อพื้นที่ด้านล่างไม่พอ */
1514  .prov-dropdown.drop-up {
1515    top: auto;
1516    bottom: calc(100% + 6px);
1517    transform: translateY(8px) scale(0.98);
1518  }
1519  .prov-dropdown.drop-up.open {
1520    transform: translateY(0) scale(1);
1521    animation-name: provPopUp;
1522  }
1523  [data-theme="light"] .prov-dropdown {
1524    background: #fff;
1525    box-shadow: 0 16px 48px rgba(100,50,20,0.16), 0 4px 16px rgba(0,0,0,0.08);
1526  }
1527
1528  /* Search box */
1529  .prov-search-wrap {
1530    display: flex; align-items: center; gap: 0.5rem;
1531    padding: 0.7rem 0.9rem;
1532    border-bottom: 1px solid var(--border-subtle);
1533  }
1534  .prov-search-wrap svg {
1535    width: 15px; height: 15px; flex-shrink: 0;
1536    color: var(--text-tertiary);
1537  }
1538  .prov-search-wrap input {
1539    flex: 1; border: none; background: transparent;
1540    font-size: 0.85rem; color: var(--text-primary);
1541    outline: none;
1542  }
1543  .prov-search-wrap input::placeholder { color: var(--text-muted); }
1544
1545  /* Scrollable list */
1546  .prov-list {
1547    max-height: 260px; overflow-y: auto;
1548    padding: 0.4rem 0;
1549    scrollbar-width: thin;
1550    scrollbar-color: rgba(255,109,53,0.3) transparent;
1551  }
1552  .prov-list::-webkit-scrollbar { width: 4px; }
1553  .prov-list::-webkit-scrollbar-thumb { background: rgba(255,109,53,0.35); border-radius: 4px; }
1554
1555  /* Group label */
1556  .prov-group-label {
1557    padding: 0.45rem 0.9rem 0.25rem;
1558    font-size: 0.68rem; font-weight: 700;
1559    color: var(--text-tertiary);
1560    text-transform: uppercase; letter-spacing: 0.08em;
1561  }
1562
1563  /* Province item */
1564  .prov-item {
1565    display: flex; align-items: center; gap: 0.6rem;
1566    padding: 0.5rem 0.9rem;
1567    cursor: pointer;
1568    transition: background 0.12s;
1569    border-radius: 0;
1570  }
1571  .prov-item:hover:not(.prov-disabled) { background: rgba(255,109,53,0.12); }
1572  .prov-item.prov-active {
1573    background: rgba(255,109,53,0.15);
1574  }
1575  .prov-item.prov-active .prov-item-name {
1576    color: var(--accent-primary); font-weight: 700;
1577  }
1578  .prov-item.prov-disabled {
1579    cursor: default; opacity: 0.55;
1580  }
1581  .prov-item-name { flex: 1; font-size: 0.875rem; color: var(--text-primary); }
1582  .prov-item-sparse {
1583    font-size: 0.65rem; font-weight: 700; margin-right: 6px;
1584    color: var(--text-secondary, #aaa); padding: 2px 7px; border-radius: 20px;
1585    border: 1px dashed currentColor;
1586  }
1587  .prov-item-badge {
บรรทัด 1250–1256: ส่วนหัวของโครงใหม่ ชื่อแบรนด์ และการปรับ topbar
บรรทัด 1257–1353: พื้นหลังของธีม ภาพหัวเรื่อง .hero-bg .hero-overlay .hero-content ป้าย .hero-label (ภาพถูกเปลี่ยนโดย ➜ setBanner() ใน frontend/extras.js) และตัวห่อแผงวางแผน
บรรทัด 1354–1450: แผงวางแผน .planner-panel แถวบน เส้นคั่น กริดช่อง .pf-grid ป้าย ข้อความ hint และความสูงของตัวควบคุมให้เท่ากัน รวมถึงการ์ดโรงแรมและปุ่มค้นหา
บรรทัด 1451–1481: พื้นหลังของส่วนแพ็กเกจและรายละเอียด
บรรทัด 1482–1587: เมนูจังหวัดแบบเลื่อน: กล่อง .prov-select .prov-dropdown (เปิดขึ้นหรือลงด้วยคลาส drop-up และอนิเมชัน provPop) ช่องค้นหา รายการ .prov-list ป้ายภาค และรายการจังหวัด .prov-item (ทำงานร่วมกับสคริปต์ท้าย ➜ frontend/index.html)
บรรทัด 1588–1650  พิมพ์ แผนทางเลือก และความชอบ
1588    font-size: 0.65rem; font-weight: 700;
1589    background: rgba(255,109,53,0.18);
1590    color: var(--accent-primary);
1591    padding: 2px 7px; border-radius: 20px;
1592    border: 1px solid rgba(255,109,53,0.35);
1593  }
1594  /* ── Print / บันทึกเป็น PDF: แสดงเฉพาะรายละเอียดทริป (พื้นขาว ตัวดำ) ── */
1595  @media print {
1596    .bg-layers, .topbar, .landing-screen, .packages-section, .toast-container,
1597    .detail-actions button, .map-wrap, .day-toggles, .modal,
1598    .poi-actions, .day-add, .day-list .poi-item button { display: none !important; }
1599    html, body { background: #fff !important; color: #000 !important; }
1600    .detail-section { display: block !important; padding: 0 !important; background: #fff !important; }
1601    .detail-grid { display: block !important; }
1602    .day-list { max-height: none !important; overflow: visible !important; }
1603    .day-panel { break-inside: avoid; border: 1px solid #999 !important; background: #fff !important; box-shadow: none !important; margin-bottom: 0.8rem; }
1604    .detail-section * { color: #000 !important; text-shadow: none !important; background: transparent !important; box-shadow: none !important; }
1605    .detail-section .kpi, .detail-section .dist-badge { border: 1px solid #999 !important; }
1606    .detail-section .day-color { background: #666 !important; }
1607  }
1608
1609  /* ── Pareto modal ── */
1610  .pareto-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
1611  .pareto-table th, .pareto-table td { padding: 0.45rem 0.6rem; text-align: right; border-bottom: 1px solid var(--border-subtle); }
1612  .pareto-table th:first-child, .pareto-table td:first-child { text-align: center; }
1613  .pareto-table th { color: var(--text-muted); font-weight: 600; font-size: 0.75rem; }
1614  .pareto-use { background: var(--grad-cta, #ff6d35); color: #fff; border: 0; border-radius: 8px; padding: 0.25rem 0.7rem; cursor: pointer; font-size: 0.8rem; white-space: nowrap; }
1615  @media (max-width: 720px) { .pareto-table th, .pareto-table td { padding: 0.4rem 0.3rem; } .pareto-use { padding: 0.25rem 0.5rem; font-size: 0.75rem; } }
1616
1617  /* ── Preferences (ความชอบ) ── */
1618  .pref-toggle {
1619    background: var(--grad-cta, linear-gradient(135deg, #ff7a3d, #e8561f)); border: 0;
1620    color: #fff; border-radius: 999px; padding: 0.4rem 1.1rem;
1621    font-size: 0.85rem; font-weight: 700; cursor: pointer;
1622    box-shadow: 0 4px 14px rgba(255,109,53,0.35); transition: transform .15s, box-shadow .15s;
1623  }
1624  .pref-toggle:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(255,109,53,0.5); }
1625  .pref-toggle[aria-expanded="true"] { box-shadow: 0 0 0 3px rgba(255,109,53,0.3); }
1626  .pref-summary { color: #fff; font-weight: 700; opacity: .9; }
1627  .pref-panel { margin: -0.4rem 0 0.9rem; padding: 0.6rem 0.8rem; display: grid; gap: 0.5rem; border: 1px solid var(--border-subtle); border-radius: 12px; background: var(--bg-surface); }
1628  .pref-panel[hidden] { display: none; }
1629  .pref-row { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
1630  .pref-label { font-size: 0.8rem; color: var(--text-secondary); min-width: 5.5rem; }
1631  .pref-label small, .pref-note { color: var(--text-muted); font-size: 0.7rem; }
1632  .pref-chips { display: flex; gap: 0.4rem; flex-wrap: wrap; }
1633  .pref-chip {
1634    border: 1px solid var(--border-subtle); background: var(--bg-surface); color: var(--text-secondary);
1635    border-radius: 999px; padding: 0.2rem 0.7rem; font-size: 0.8rem; cursor: pointer;
1636  }
1637  .pref-chip[data-state="like"]  { background: rgba(16,185,129,0.18); border-color: rgba(16,185,129,0.6); color: var(--text-primary); }
1638
1639  .pref-chip[data-state="avoid"] { background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.55); color: var(--text-primary); text-decoration: line-through; }
1640
1641  #prefDiet {
1642    appearance: none; -webkit-appearance: none; outline: none; cursor: pointer;
1643    background: var(--bg-surface) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E") no-repeat right 0.7rem center;
1644    color: var(--text-primary); border: 1px solid var(--border-subtle); border-radius: 999px;
1645    padding: 0.3rem 2rem 0.3rem 0.9rem; font-size: 0.82rem; transition: border-color .15s;
1646  }
1647  #prefDiet:hover, #prefDiet:focus { border-color: var(--accent-primary); }
1648  #prefDiet option { background: #2a211b; color: #fff; }
1649  .prov-item-soon {
1650    font-size: 0.65rem; font-weight: 600;
บรรทัด 1588–1607: @media print ซ่อนองค์ประกอบที่ไม่ต้องพิมพ์ (ปุ่ม แผนที่ โมดัล พื้นหลัง) และทำหน้ากระดาษพื้นขาว ใช้กับปุ่ม PDF ที่เรียก window.print()
บรรทัด 1608–1617: ตาราง .pareto-table และปุ่ม .pareto-use
บรรทัด 1618–1650: ปุ่มและแผงความชอบ .pref-toggle .pref-panel ชิป .pref-chips และช่องเลือกอาหาร #prefDiet
บรรทัด 1651–1815  ไอคอน มือถือ และฟีเจอร์เสริม
1651    color: var(--text-muted);
1652    padding: 2px 7px; border-radius: 20px;
1653    border: 1px solid var(--border-subtle);
1654  }
1655
1656
1657  /* ---- ไอคอนเส้นบางแทน emoji ---- */
1658  .ic { width: 1.1em; height: 1.1em; flex-shrink: 0; fill: none; stroke: currentColor; stroke-width: 1.7;
1659        stroke-linecap: round; stroke-linejoin: round; vertical-align: -0.2em; }
1660  .hotel-card-icon .ic { width: 22px; height: 22px; color: var(--accent-primary); }
1661  .map-hotel-marker .ic { width: 20px; height: 20px; color: #fff; }
1662  .dist-badge .ic { width: 0.95em; height: 0.95em; vertical-align: -0.12em; }
1663  .poi-name .ic { color: var(--accent-primary); margin-right: 2px; }
1664  .score-chip .ic { width: 0.95em; height: 0.95em; color: var(--accent-primary); fill: currentColor; stroke-width: 1.2; }
1665  .btn-icon .ic { width: 1em; height: 1em; }
1666  .export-btn .ic, .pref-toggle .ic { width: 1.05em; height: 1.05em; }
1667
1668  /* ---- ปุ่มการทำงานของแผน: โทนเดียวกับธีม (เส้นบาง ไม่มีสีน้ำเงิน/ฟ้า) ---- */
1669  .detail-actions { gap: 0.5rem; align-items: center; flex-wrap: wrap; }
1670  .reshuffle-btn {
1671    background: var(--bg-surface); border: 1px solid var(--border-default);
1672    border-radius: 999px; padding: 0.45rem 0.95rem; font-weight: 500; white-space: nowrap; color: var(--text-secondary);
1673  }
1674  .reshuffle-btn:hover { background: rgba(255,109,53,0.10); border-color: var(--accent-primary); color: var(--text-primary); }
1675  .reshuffle-btn .ic, .reshuffle-btn svg { width: 15px; height: 15px; stroke: var(--accent-primary); }
1676  .day-title h3 { white-space: nowrap; }
1677
1678  /* ---- มือถือ: ฟอร์มเรียงคอลัมน์เดียว ไม่ล้นจอ ---- */
1679  @media (max-width: 720px) {
1680    .planner-panel { zoom: 1; padding: 1.1rem 1rem 1rem; }
1681    .planner-top-row { flex-wrap: wrap; }
1682    .planner-title { flex-basis: 60%; }
1683    .pf-grid, .pf-grid-b, .dev-mode .pf-grid-b { grid-template-columns: 1fr; gap: 0.8rem; }
1684    .pf-col-search { min-width: 0; }
1685    .pf-col-search .cta-btn { width: 100%; justify-content: center; }
1686    .planner-panel .hotel-card { height: auto; min-height: 48px; }
1687    .hero-content h1 { font-size: clamp(1.7rem, 8vw, 2.4rem); line-height: 1.25; overflow-wrap: anywhere; }
1688  }
1689  @media (max-width: 720px) {
1690    .hero-h1 { white-space: normal; font-size: clamp(1.8rem, 9vw, 2.6rem); }
1691    .hero-desc { white-space: normal; font-size: 0.9rem; }
1692    .hero-content { padding: 0 1.2rem; }
1693    .hero-label { font-size: 0.8rem; margin-bottom: 1rem; }
1694    .planner-wrapper { padding: 330px 0.9rem 1rem; }
1695  }
1696
1697  /* ── รายละเอียดสถานที่ / รีวิวจำลอง ── */
1698  .poi-link { cursor: pointer; }
1699  .poi-link:hover { text-decoration: underline; text-underline-offset: 3px; }
1700  .poi-facts { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.6rem; margin-bottom: 0.8rem; }
1701  .poi-facts > div { border: 1px solid var(--border-subtle); border-radius: 12px; padding: 0.55rem 0.75rem; display: flex; flex-direction: column; gap: 0.15rem; }
1702  .poi-facts span { font-size: 0.75rem; color: var(--text-tertiary); }
1703  .poi-note { font-size: 0.78rem; color: var(--text-tertiary); margin: 0.6rem 0; line-height: 1.5; }
1704  .rev-head { display: flex; align-items: center; gap: 0.6rem; margin: 0.8rem 0 0.4rem; }
1705  .rev-score { display: inline-flex; align-items: center; gap: 0.25rem; font-weight: 700; font-size: 1.1rem; }
1706  .rev-count { font-size: 0.82rem; color: var(--text-tertiary); }
1707  .mock-chip { margin-left: auto; font-size: 0.7rem; padding: 0.15rem 0.55rem; border-radius: 999px; border: 1px dashed var(--border-default); color: var(--text-tertiary); }
1708  .rev-item { border-top: 1px solid var(--border-subtle); padding: 0.55rem 0; font-size: 0.88rem; line-height: 1.5; }
1709  .rev-stars { color: #f59e0b; letter-spacing: 1px; font-size: 0.85rem; }
1710
1711  /* ── ส่วนเสริม: ฤดูกาล / แผนที่บันทึก / เปรียบเทียบ ── */
1712  .tips-card { height: 43px; box-sizing: border-box; display: flex; align-items: center; gap: 8px; padding: 0 12px; border-radius: 16px; background: rgba(255,109,53,0.08); border: 1px dashed rgba(255,109,53,0.45); overflow: hidden; }
1713  .tips-badge { flex-shrink: 0; font-size: 0.62rem; font-weight: 800; letter-spacing: .04em; color: #fff; background: var(--accent-primary); border-radius: 999px; padding: 2px 8px; }
1714  .tips-text { font-size: 0.8rem; line-height: 1.35; color: var(--text-primary); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; transition: opacity .4s; }
1715  .tips-text.fade { opacity: 0; }
1716  .dev-modal-card { max-width: 340px; }
1717  .dev-modal-card input { width: 100%; box-sizing: border-box; margin: 10px 0 6px; padding: 9px 14px; border-radius: 999px; border: 1px solid var(--border-subtle); background: var(--bg-surface); color: var(--text-primary); font-size: 1rem; text-align: center; }
1718  .dev-modal-card .dev-err { color: #f87171; font-size: 0.78rem; min-height: 1.1em; }
1719  .season-note { font-size: 0.75rem; color: var(--text-secondary); margin-top: 6px; line-height: 1.5; }
1720  .saved-row { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 10px 0; border-bottom: 1px solid rgba(128,128,128,0.2); }
1721  .saved-btn { font-size: 1.1rem; }
1722  .pareto-table tr.cmp-main td { font-weight: 700; color: var(--accent-primary); }
1723  @media (max-width: 640px) { .modal-body { overflow-x: auto; } }
1724
1725  /* ── ความชอบ: ชื่อหมวด + ปุ่มไอคอน 👍/👎 ด้านหลัง ── */
1726  .pref-cat { display: inline-flex; align-items: center; gap: 2px; padding: 3px 4px 3px 14px; border-radius: 999px; border: 1.5px solid var(--border-subtle); background: var(--bg-surface); transition: border-color .15s, background .15s, box-shadow .15s; }
1727  .pref-cat .pc-name { font-size: 0.85rem; color: var(--text-secondary); margin-right: 6px; transition: color .15s; }
1728  .pref-cat button { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border: 0; border-radius: 50%; background: none; color: var(--text-muted); cursor: pointer; transition: background .15s, color .15s, transform .15s; }
1729  .pref-cat button .ic { width: 1.05em; height: 1.05em; }
1730  .pref-cat .pc-dislike .ic { transform: scaleY(-1); }
1731  .pref-cat .pc-like:hover { background: rgba(34,197,94,0.2); color: #22c55e; transform: scale(1.12); }
1732  .pref-cat .pc-dislike:hover { background: rgba(239,68,68,0.2); color: #f87171; transform: scale(1.12); }
1733  .pref-cat[data-state="like"] { border-color: transparent; background: linear-gradient(135deg, #22c55e, #15803d); box-shadow: 0 3px 14px rgba(34,197,94,0.45); }
1734  .pref-cat[data-state="avoid"] { border-color: transparent; background: linear-gradient(135deg, #ef4444, #b91c1c); box-shadow: 0 3px 14px rgba(239,68,68,0.45); }
1735  .pref-cat[data-state="like"] .pc-name, .pref-cat[data-state="avoid"] .pc-name { color: #fff; font-weight: 700; }
1736  .pref-cat[data-state="like"] .pc-like, .pref-cat[data-state="avoid"] .pc-dislike { background: rgba(255,255,255,0.28); color: #fff; }
1737  .pref-cat[data-state="like"] .pc-dislike, .pref-cat[data-state="avoid"] .pc-like { color: rgba(255,255,255,0.55); }
1738
1739  /* ── dropdown อาหาร ── */
1740  .diet-wrap { position: relative; display: inline-block; }
1741  .diet-btn { font: inherit; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.6rem; min-width: 9rem; justify-content: space-between; padding: 0.38rem 0.95rem; color: var(--text-primary); background: var(--bg-surface); border: 1.5px solid var(--border-subtle); border-radius: 999px; cursor: pointer; transition: border-color .15s, box-shadow .15s; }
1742  .diet-btn:hover, .diet-btn.open { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(255,109,53,0.15); }
1743  .diet-btn svg { color: var(--accent-primary); transition: transform .18s; }
1744  .diet-btn.open svg { transform: rotate(180deg); }
1745  .diet-list { position: absolute; top: calc(100% + 6px); left: 0; min-width: 100%; z-index: 999; padding: 6px; background: var(--bg-elevated); border: 1.5px solid var(--border-subtle); border-radius: 18px; box-shadow: 0 16px 40px rgba(0,0,0,0.45); opacity: 0; transform: translateY(-6px); pointer-events: none; transition: opacity .16s, transform .16s; }
1746  .diet-list.open { opacity: 1; transform: none; pointer-events: auto; }
1747  .diet-item { padding: 0.4rem 0.9rem; border-radius: 12px; font-size: 0.85rem; cursor: pointer; color: var(--text-primary); white-space: nowrap; }
1748  .diet-item:hover { background: rgba(255,109,53,0.14); }
1749  .diet-item.on { background: rgba(255,109,53,0.2); color: var(--accent-primary); font-weight: 700; }
1750  [data-theme="light"] .diet-list { background: #fff; box-shadow: 0 16px 40px rgba(100,50,20,0.16); }
1751
1752  .dev-only { display: none !important; }
1753  .dev-mode .dev-only { display: inline-flex !important; }
1754
1755  .wx-chip { color: #7dd3fc; font-weight: 600; }
1756  .rain-banner { margin: 0 0 8px; padding: 8px 12px; border-radius: 12px; font-size: 0.8rem; background: rgba(56,189,248,0.12); border: 1px solid rgba(56,189,248,0.4); display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
1757  .rain-banner button { font: inherit; font-size: 0.78rem; padding: 3px 12px; border-radius: 999px; border: 0; background: #0ea5e9; color: #fff; cursor: pointer; }
1758
1759  .poi-item[draggable="true"] { cursor: grab; }
1760  .poi-item.dragging { opacity: .45; }
1761
1762  /* มือถือ: ปุ่มบนแถบบนเยอะขึ้น (ผลทดลอง/ภาษา/★/Dev/ธีม) — ย่อและตัดบรรทัดไม่ให้ล้นจอ */
1763  @media (max-width: 560px) {
1764    .topbar-actions { flex-wrap: wrap; justify-content: flex-end; gap: 4px; max-width: calc(100vw - 110px); flex-wrap: nowrap; }
1765    .topbar-actions .icon-btn { min-width: 30px; width: auto; height: 30px; padding: 0 .35rem; font-size: .72rem; }
1766    .topbar-actions .results-link { padding: 0 .45rem !important; display: inline-flex; align-items: center; }
1767  }
1768  @media (max-width: 560px) {
1769    .topbar .brand h1 { font-size: 1.1rem; }
1770    .topbar-actions .results-link { font-size: 0 !important; width: 30px !important; justify-content: center; padding: 0 !important; }
1771    .topbar-actions .results-link::before { content: "📊"; font-size: .85rem; }
1772  }
1773  [data-theme="light"] .pref-cat .pc-like, [data-theme="light"] .pref-cat .pc-dislike { color: #64748b; }
1774  [data-theme="light"] .pref-cat[data-state="like"] button, [data-theme="light"] .pref-cat[data-state="avoid"] button { color: rgba(255,255,255,.7); }
1775  [data-theme="light"] .pref-cat[data-state="like"] .pc-like, [data-theme="light"] .pref-cat[data-state="avoid"] .pc-dislike { color: #fff; }
1776
1777  .plan-warn{margin:10px 0;padding:10px 14px;border-radius:12px;border:1px solid rgba(234,179,8,.5);background:rgba(234,179,8,.12);font-size:.85rem}
1778  .plan-warn ul{margin:6px 0 0;padding-left:18px}
1779
1780  /* ซ่อนคะแนน/ตัวเลขภายในจากผู้ใช้ทั่วไป — แสดงเฉพาะโหมด Developer */
1781  body:not(.dev-mode) :is(.score-num, .dev-txt, .score-chip, #kpiScore, .runtime, .day-score) { display: none !important; }
1782
1783  /* ลากการ์ดแบบ real-time */
1784  .is-dragging .dist-connector { opacity: .45; }
1785  .dist-connector.drag-hide { display: none; }
1786  .poi-item.dragging { display: none; }
1787  .drop-gap { list-style: none; border: 2px dashed rgba(239,68,68,.55); background: rgba(239,68,68,.09); border-radius: 14px; margin: 4px 0; position: relative; }
1788  .drop-gap::before { content: ''; position: absolute; left: 10px; right: 10px; top: -5px; height: 3px; border-radius: 3px; background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,.7); }
1789  /* การ์ดที่ผิดข้อจำกัด: สีแดง + กล่องข้อความใต้การ์ด */
1790  .poi-item.poi-error { border-color: #ef4444 !important; background: rgba(239,68,68,.10) !important; box-shadow: 0 0 0 1px rgba(239,68,68,.4); }
1791  .poi-item.poi-error .poi-num { background: #ef4444 !important; color: #fff !important; }
1792  .poi-err-box { list-style: none; margin: -2px 0 6px; padding: 8px 12px; font-size: .8rem; line-height: 1.4; color: #b91c1c; background: rgba(239,68,68,.12); border: 1px solid rgba(239,68,68,.5); border-top: 0; border-radius: 0 0 12px 12px; }
1793  [data-theme="dark"] .poi-err-box { color: #fca5a5; }
1794  .plan-warn { margin: 6px 0 10px; padding: 8px 12px; font-size: .82rem; color: #92400e; background: rgba(245,158,11,.14); border: 1px solid rgba(245,158,11,.5); border-radius: 10px; }
1795  [data-theme="dark"] .plan-warn { color: #fcd34d; }
1796
1797  .hero-visual .hero-bg { transition: opacity .6s ease, transform 8s ease; }
1798
1799  /* ทางเลือกอื่นของทริป (การ์ด) */
1800  .pc-wrap, .pc-wrap-in { display: grid; gap: 12px; }
1801  .pc { border: 1px solid var(--border-subtle); border-radius: 16px; padding: 14px 16px; background: var(--bg-surface); }
1802  .pc-main { border-color: var(--accent-primary); box-shadow: 0 0 0 1px var(--accent-primary) inset; }
1803  .pc-tag { display: inline-block; font-size: .75rem; font-weight: 700; padding: 3px 10px; margin-right: 6px; border-radius: 999px; background: rgba(255,109,53,.14); color: var(--accent-primary); }
1804  .pc-why { margin: 6px 0 10px; font-size: .88rem; color: var(--text-secondary, var(--text-muted)); }
1805  .pc-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
1806  .pc-metrics > div { display: flex; flex-direction: column; gap: 1px; }
1807  .pc-metrics small { color: var(--text-muted); font-size: .72rem; }
1808  .pc-metrics b { font-size: 1rem; }
1809  .pc-dots { letter-spacing: 2px; color: var(--accent-primary); font-size: .85rem !important; }
1810  .pc-good { color: #16a34a; font-size: .74rem; font-weight: 600; } .pc-bad { color: #dc2626; font-size: .74rem; font-weight: 600; } .pc-same { color: var(--text-muted); font-size: .74rem; }
1811  .pc-hi { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0; }
1812  .pc-hi span { font-size: .75rem; padding: 3px 9px; border-radius: 999px; background: var(--bg-elevated, rgba(127,127,127,.12)); color: var(--text-secondary, inherit); }
1813  .pc .pareto-use { width: 100%; padding: .5rem; font-size: .9rem; border-radius: 10px; }
1814  .pc-more { margin: 4px auto 0; background: none; border: 1px dashed var(--border-subtle); color: var(--text-muted); border-radius: 999px; padding: .4rem 1rem; cursor: pointer; }
1815  @media (max-width: 560px) { .pc-metrics { grid-template-columns: 1fr 1fr; } }
บรรทัด 1651–1673: ไอคอนเส้นบาง .ic และปุ่มปฏิบัติการของแผน
บรรทัด 1674–1694: @media (max-width: 720px) ฟอร์มเรียงคอลัมน์เดียว
บรรทัด 1695–1708: ลิงก์ชื่อสถานที่และหน้าต่างรายละเอียดสถานที่ (.poi-facts, รีวิว) ของ ➜ showPoiDetail() ใน frontend/app.js
บรรทัด 1709–1719: กล่อง Tips .tips-text และหมายเหตุฤดูกาล .season-note ที่ ➜ frontend/extras.js สร้าง
บรรทัด 1720–1748: ปรับโมดัลบนจอแคบ ชิปความชอบ .pref-cat (สถานะ like/avoid) และตัวเลือกอาหารที่แทน select (.diet-btn .diet-item)
บรรทัด 1749–1774: .dev-only ซ่อนองค์ประกอบสำหรับโหมด Developer (เปิดด้วยคลาส dev-mode ที่ ➜ setDevMode() ใน frontend/app.js) แถบเตือนฝน .rain-banner และเป้าหมายการลาก .drop-over
บรรทัด 1775–1800: กล่องคำเตือนของแผน .plan-warn การ์ดที่ผิดเวลา .poi-error และซ่อนเส้นเชื่อมระหว่างลาก
บรรทัด 1801–1815: การ์ดแผนทางเลือก .pc .pc-metrics .pc-dots ที่ ➜ renderParetoCards() ใน frontend/app.js สร้าง
บรรทัด 1816–1868  วิธีใช้ ลากการ์ด และ tooltip
1816
1817  /* Tutorial */
1818  .tut { position: fixed; inset: 0; z-index: 3000; }
1819  .tut-spot { position: fixed; border-radius: 14px; box-shadow: 0 0 0 9999px rgba(0,0,0,.62); transition: all .25s ease; pointer-events: none; outline: 2px solid var(--accent-primary); }
1820  .tut-card { position: fixed; background: var(--bg-surface, #fff); color: var(--text-primary); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 16px 18px; box-shadow: 0 18px 50px rgba(0,0,0,.35); max-width: 340px; }
1821  .tut-card.center { top: 50%; left: 50%; transform: translate(-50%, -50%); width: min(360px, calc(100vw - 24px)); }
1822  .tut-title { font-weight: 800; font-size: 1.05rem; margin-bottom: 6px; }
1823  .tut-text { font-size: .9rem; line-height: 1.55; color: var(--text-secondary, var(--text-muted)); }
1824  .tut-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 14px; gap: 10px; }
1825  .tut-dots i { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: var(--border-subtle); margin-right: 5px; }
1826  .tut-dots i.on { background: var(--accent-primary); }
1827  .tut-btns { display: flex; gap: 6px; }
1828  .tut-btns button { border: 0; border-radius: 999px; padding: .4rem .9rem; cursor: pointer; font: inherit; font-size: .82rem; background: var(--bg-elevated, rgba(127,127,127,.15)); color: var(--text-primary); }
1829  .tut-btns .tut-next { background: var(--accent-primary); color: #fff; font-weight: 700; }
1830  .tut-btns .tut-skip { background: none; color: var(--text-muted); }
1831  .tut.dim { background: rgba(0,0,0,.6); }
1832
1833  .pc-dots { display: flex; gap: 5px; align-items: center; height: 1.4rem; }
1834  .pc-dots i { width: 11px; height: 11px; border-radius: 50%; border: 2px solid var(--accent-primary); box-sizing: border-box; }
1835  .pc-dots i.on { background: var(--accent-primary); }
1836  .drop-gap::after { content: ''; position: absolute; left: 10px; right: 10px; bottom: -5px; height: 3px; border-radius: 3px; background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,.7); }
1837  .is-dragging .poi-err-box { display: none; }
1838
1839  /* marker ตอนลากการ์ด: บางลง ปลายซ้าย-ขวาจาง กลางเข้ม */
1840  .drop-gap::before, .drop-gap::after { left: 0 !important; right: 0 !important; height: 2px !important; border-radius: 2px;
1841    background: linear-gradient(90deg, rgba(239,68,68,0) 0%, #ef4444 28%, #ef4444 72%, rgba(239,68,68,0) 100%) !important; box-shadow: 0 0 4px rgba(239,68,68,.45) !important; }
1842  .drop-gap::before { top: -4px !important; } .drop-gap::after { bottom: -4px !important; }
1843  .rain-ic { display: inline-flex; vertical-align: -3px; margin-left: 6px; color: #0ea5e9; cursor: help; }
1844
1845  .planner-panel .hotel-card { width: max-content; max-width: 100%; }
1846  .planner-panel .hotel-card-body { flex: none; }
1847  .planner-panel .hotel-card-switch { margin-left: 0.5rem; }
1848  @media (max-width: 720px) { .planner-panel .hotel-card { width: 100%; } .planner-panel .hotel-card-body { flex: 1; } }
1849
1850  /* tutorial: ซ่อนการ์ดจนกว่าจะวางตำแหน่ง, ไม่ทำ transition บนเงาขนาดใหญ่ (ลด lag) */
1851  .tut:not(.ready) .tut-card { visibility: hidden; }
1852  .tut-spot { transition: none !important; will-change: top, left, width, height; }
1853  /* tooltip แบบ minimal แทนกล่องดำของเบราว์เซอร์ */
1854  .wet-tip { position: fixed; z-index: 4000; max-width: 260px; padding: 6px 11px; border-radius: 10px; font-size: .78rem; line-height: 1.4; pointer-events: none;
1855    background: var(--bg-surface, #fff); color: var(--text-primary, #111); border: 1px solid var(--border-default, rgba(127,127,127,.3)); box-shadow: 0 6px 22px rgba(0,0,0,.18); opacity: 0; transform: translateY(3px); transition: opacity .12s, transform .12s; }
1856  .wet-tip.show { opacity: 1; transform: none; }
1857  /* คืนอนิเมชันของ tutorial (เลื่อนไลต์ไปยังเป้าหมายอย่างนุ่มนวล) โดยทำ transition เฉพาะตำแหน่ง/ขนาด */
1858  .tut-spot { transition: top .25s ease, left .25s ease, width .25s ease, height .25s ease !important; }
1859  /* ที่พักยาวขึ้น Tips สั้นลง */
1860  .pf-grid-b { grid-template-columns: 1fr 1fr auto; }
1861  .planner-panel .hotel-card { width: 100%; justify-content: flex-start; }
1862  /* ที่พักกว้าง ~42% ของแถว สวิตช์ชิดขวา, Tips ยาวขึ้น */
1863  .pf-grid-b { grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr) auto; }
1864  .planner-panel .hotel-card { justify-content: space-between; }
1865  .planner-panel .hotel-card-body { flex: 1; }
1866  .planner-panel .hotel-card-switch { margin-left: auto; }
1867  .drop-gap { margin: 6px 0; }
1868
บรรทัด 1816–1837: สไตล์ของ tutorial: .tut .tut-spot .tut-card ปุ่มและจุดบอกขั้น ที่ ➜ frontend/tutorial.js สร้าง
บรรทัด 1838–1848: ตัวบอกตำแหน่งตอนลากการ์ด .drop-gap (ช่องว่างสีแดงจาง) และการปรับการ์ดโรงแรมบนจอแคบ
บรรทัด 1849–1851: ซ่อนการ์ด tutorial จนกว่าจะจัดตำแหน่งเสร็จ
บรรทัด 1852–1868: กล่อง .wet-tip ที่ ➜ frontend/tooltip.js ใช้แทนกล่องข้อความของเบราว์เซอร์
บรรทัด 1869–1943  จัดขนาดพอดีจอ ประวัติ และการแจ้งเตือน
1869  @media (min-width: 1001px) { .detail-section { box-sizing: border-box; padding-bottom: 2.25rem; } }
1870
1871  /* ย่อการ์ดให้เห็นครบ 6 จุด + ปุ่มเพิ่มสถานที่ (ค่า --sp ระยะห่าง, --fs ตัวอักษร ตั้งจาก fitDetail) */
1872  .day-list.fit { --sp: 1; --fs: 1; }
1873  .day-list.fit .day-panel { padding: calc(0.6rem + 0.65rem * var(--sp)) 1.1rem; margin-bottom: calc(0.5rem + 0.5rem * var(--sp)); }
1874  .day-list.fit .day-head { margin-bottom: calc(0.3rem + 0.45rem * var(--sp)); padding-bottom: calc(0.3rem + 0.45rem * var(--sp)); }
1875  .day-list.fit .poi-item { padding: calc(0.3rem + 0.32rem * var(--sp)) 0.5rem; }
1876  .day-list.fit .poi-num { width: calc(24px + 4px * var(--sp)); height: calc(24px + 4px * var(--sp)); }
1877  .day-list.fit .poi-name { font-size: calc(0.95rem * var(--fs)); }
1878  .day-list.fit .poi-meta { font-size: calc(0.75rem * var(--fs)); margin-top: calc(0.15rem * var(--sp)); }
1879  .day-list.fit .poi-actions button, .day-list.fit .poi-actions a.btn-loc { width: calc(28px + 4px * var(--sp)); height: calc(28px + 4px * var(--sp)); }
1880  .day-list.fit .rain-banner, .day-list.fit .plan-warn { padding: 5px 12px; margin-bottom: calc(3px + 5px * var(--sp)); }
1881  .day-list.fit .dist-connector { height: 0; padding: 0 0.5rem; margin: 0; position: relative; overflow: visible; z-index: 2; }
1882  .day-list.fit .dist-badge { background: var(--bg-surface); }
1883  .day-list.fit .day-add { margin-top: calc(0.2rem + 0.3rem * var(--sp)); padding: calc(0.3rem + 0.25rem * var(--sp)) 0.75rem; }
1884  /* ฟอนต์การ์ดเล็กลงอีก + ช่องไฟระหว่างข้อความการ์ดกับป้ายระยะทางมากขึ้น */
1885  .day-list.fit .poi-name { font-size: calc(0.86rem * var(--fs)); }
1886  .day-list.fit .poi-meta { font-size: calc(0.68rem * var(--fs)); }
1887  .day-list.fit .poi-item { padding: calc(0.42rem + 0.3rem * var(--sp)) 0.5rem; }
1888  .day-list.fit .dist-badge { font-size: calc(0.64rem * var(--fs)); }
1889
1890  /* กล่องเตือนฝนเล็กลง เพื่อให้พื้นที่กับการ์ด */
1891  .day-list.fit .rain-banner { padding: 3px 10px; font-size: 0.72rem; gap: 6px; margin-bottom: calc(2px + 3px * var(--sp)); border-radius: 10px; }
1892  .day-list.fit .rain-banner button { font-size: 0.68rem; padding: 1px 10px; }
1893  /* กล่องฝน: เว้นระยะใต้กล่องให้เท่ากับด้านบน ไม่ชิดป้ายระยะทางแรก */
1894  .day-list.fit .rain-banner { margin-bottom: 4px; }
1895  .day-list.fit .poi-list { padding-top: 18px; }
1896  /* ไอคอนโรงแรมในป้ายระยะทาง: ใหญ่ขึ้นและใช้สีส้มของธีม */
1897  .dist-badge .ic:has(use[href="#i-hotel"]) { width: 1.7em; height: 1.7em; vertical-align: -0.4em; color: var(--accent-primary); stroke-width: 2.2; }
1898  .dist-badge .ic:has(use[href="#i-arrow-right"]) { width: 1.1em; height: 1.1em; }
1899  /* ชื่อสถานที่: พื้นที่คลิก/hover เท่าความยาวชื่อเท่านั้น ส่วนที่เหลือของการ์ดใช้สำหรับลาก */
1900  .poi-item .poi-name { width: fit-content; max-width: 100%; }
1901
1902  /* หน้าเปลี่ยนสถานที่: ปุ่มรีวิว / Google Maps ด้านขวา */
1903  .swap-option .opt-actions { display: flex; gap: 8px; margin-left: 12px; flex-shrink: 0; }
1904  .opt-btn { display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; padding: 0; border-radius: 9px; background: #fff; color: #475569;
1905    border: 1px solid rgba(127,127,127,.3); cursor: pointer; text-decoration: none; transition: box-shadow .15s, transform .15s, color .15s, border-color .15s; }
1906  .opt-btn .ic { width: 15px; height: 15px; }
1907  .opt-btn:hover { color: var(--accent-primary); border-color: var(--accent-primary); box-shadow: 0 5px 16px rgba(0,0,0,.2); transform: translateY(-2px); }
1908
1909  /* ภาพการ์ดที่กำลังลาก: คมชัด ย่อลงเล็กน้อย ไม่มีแอนิเมชัน */
1910  .poi-item.drag-ghost { position: fixed !important; z-index: 3500; margin: 0 !important; pointer-events: none; opacity: 1 !important; filter: none !important; background: var(--bg-surface, #fff);
1911    box-shadow: 0 14px 34px rgba(0,0,0,.28), 0 0 0 2px rgba(255,109,53,.55); border-radius: 14px; transform: scale(.9);
1912    animation: none; transition: none !important; }
1913
1914  body.wet-dragging, body.wet-dragging * { user-select: none !important; cursor: grabbing !important; }
1915  .poi-item { cursor: grab; }
1916  .poi-item.drag-ghost { will-change: left, top; contain: layout; }
1917
1918  /* ปุ่มย้อนกลับ / เดินหน้า */
1919  .hist-group { display: inline-flex; gap: 6px; }
1920  .hist-btn { padding-left: .7rem; padding-right: .7rem; }
1921  .hist-btn .ic { width: 16px; height: 16px; }
1922  .hist-btn.disabled { opacity: .4; pointer-events: none; }
1923
1924  /* ── ปุ่มประวัติการแจ้งเตือน (ลอยมุมขวาล่าง) ── */
1925  .notif-btn { position: fixed; right: 24px; bottom: 24px; z-index: 900; width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;
1926    background: var(--bg-elevated, #fff); color: var(--text-primary); border: 1px solid var(--border-subtle); box-shadow: 0 6px 20px rgba(0,0,0,.25); transition: transform .15s ease, box-shadow .15s ease; }
1927  .notif-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 26px rgba(0,0,0,.3); border-color: var(--accent-primary); }
1928  .notif-btn svg { width: 22px; height: 22px; }
1929  .notif-badge { position: absolute; top: -3px; right: -3px; min-width: 18px; height: 18px; padding: 0 4px; border-radius: 9px; background: var(--accent-primary, #ff6d35); color: #fff; font-size: .68rem; font-weight: 700; line-height: 18px; text-align: center; }
1930  .notif-panel { position: fixed; right: 24px; bottom: 82px; z-index: 900; width: min(340px, calc(100vw - 32px)); max-height: 60vh; display: flex; flex-direction: column; overflow: hidden;
1931    background: var(--bg-elevated, #fff); backdrop-filter: blur(16px); color: var(--text-primary); border: 1px solid var(--border-subtle); border-radius: 16px; box-shadow: 0 18px 50px rgba(0,0,0,.35); }
1932  .notif-panel[hidden] { display: none; }
1933  .notif-head { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border-bottom: 1px solid var(--border-subtle); font-size: .9rem; }
1934  .notif-clear { background: none; border: 0; color: var(--text-muted); font-size: .78rem; cursor: pointer; }
1935  .notif-clear:hover { color: var(--accent-primary); }
1936  .notif-list { overflow-y: auto; padding: 6px 0; }
1937  .notif-item { display: flex; gap: 10px; padding: 9px 14px; font-size: .82rem; line-height: 1.4; }
1938  .notif-item + .notif-item { border-top: 1px solid var(--border-subtle); }
1939  .notif-dot { flex: none; width: 8px; height: 8px; margin-top: 6px; border-radius: 50%; background: #22c55e; }
1940  .notif-item.error .notif-dot { background: #ef4444; }
1941  .notif-time { margin-top: 2px; font-size: .7rem; color: var(--text-muted); }
1942  .notif-empty { padding: 22px 14px; text-align: center; font-size: .82rem; color: var(--text-muted); }
1943  @media print { .notif-btn, .notif-panel { display: none !important; } }
บรรทัด 1869–1896: ปรับความสูงและขนาดของส่วนรายละเอียดให้ตรงกับ ➜ fitDetail() ใน frontend/app.js ผ่านตัวแปร --sp (ระยะห่าง) และ --fs (ขนาดอักษร) ของ .day-list.fit
บรรทัด 1897–1914: รายละเอียดของไอคอนและปุ่มในรายการตัวเลือก
บรรทัด 1915–1931: ตัวผีขณะลาก .drag-ghost (ที่ ➜ enableDrag() ใน frontend/extras.js สร้าง) และปุ่มย้อนกลับ/เดินหน้า .hist-btn (➜ undoEdit() ใน frontend/app.js)
บรรทัด 1932–1943: ปุ่มกระดิ่งและแผงประวัติการแจ้งเตือน .notif-* ของ ➜ frontend/extras.js และซ่อนปุ่มเหล่านี้ตอนพิมพ์
บรรทัด 1944–1968  รองรับมือถือและจอสัมผัส
1944
1945  /* ── รองรับมือถือ / จอสัมผัส ── */
1946  @media (max-width: 1000px) {
1947    #map { height: min(62vh, 440px) !important; }
1948    .day-list { max-height: none !important; overflow: visible !important; }   /* จอแคบ: ไม่ใช้กรอบเลื่อนซ้อนในหน้า */
1949  }
1950  @media (max-width: 640px) {
1951    .icon-btn { width: 36px; height: 36px; }
1952    input, select, textarea { font-size: 16px !important; }   /* กัน iOS ซูมเองเมื่อแตะช่องกรอก */
1953    .day-head { flex-wrap: wrap; gap: 0.4rem; }
1954    .day-stats { flex-wrap: wrap; gap: 0.3rem 0.75rem; }
1955    .wx-chip { white-space: nowrap; }
1956    .poi-item { flex-wrap: wrap; row-gap: 0.2rem; }
1957    .poi-info { flex: 1 1 calc(100% - 44px); }
1958    .poi-actions { flex: 1 1 100%; justify-content: flex-end; gap: 0.5rem; }
1959    .poi-actions button, .poi-actions a.btn-loc { width: 44px; height: 40px; }
1960  }
1961  @media (pointer: coarse) {
1962    .poi-item { -webkit-touch-callout: none; -webkit-user-select: none; user-select: none; touch-action: pan-y; }
1963    .poi-actions button, .poi-actions a.btn-loc { min-width: 40px; min-height: 36px; }
1964  }
1965  @media (max-width: 640px) { .swap-option { margin-left: 0; } }
1966  @media (max-width: 720px) {   /* กฎ pf-grid-b ด้านบนมาทีหลังกฎจอแคบ จึงต้องทับซ้ำ */
1967    .pf-grid, .pf-grid-b, .dev-mode .pf-grid-b { grid-template-columns: 1fr !important; }
1968  }
บรรทัด 1944–1949: คอมเมนต์หัวส่วน และกฎสำหรับจอกว้างไม่เกิน 1000 พิกเซล: แผนที่สูง 62% ของความสูงจอแต่ไม่เกิน 440 พิกเซล (ใช้ !important เพราะ syncMapHeight ใน ➜ frontend/app.js ตั้งความสูงเป็นสไตล์ในบรรทัด) และ .day-list ไม่ใช้กรอบเลื่อนซ้อนในหน้า
บรรทัด 1950–1960: จอกว้างไม่เกิน 640 พิกเซล: ปุ่มไอคอนบนแถบบนใหญ่ขึ้น ช่องกรอกใช้อักษร 16 พิกเซลกัน iOS ซูมเอง ปุ่มความชอบสูงพอแตะ หัวของวันและตัวเลขสถิติขึ้นบรรทัดใหม่ได้ ชิปสภาพอากาศไม่ตัดบรรทัด และการ์ดสถานที่แยกปุ่มเป็นแถวใต้ชื่อพร้อมปุ่มขนาด 44x40 พิกเซล
บรรทัด 1961–1964: อุปกรณ์สัมผัส (pointer: coarse): ปิดเมนูแตะค้างและการเลือกข้อความบนการ์ดเพื่อให้กดค้างแล้วลากได้ (➜ enableDrag() ใน frontend/extras.js) และตั้ง touch-action: pan-y ให้ปัดขึ้นลงเลื่อนหน้าได้ปกติ
บรรทัด 1965: จอแคบ: ตัวเลือกในหน้าต่างเปลี่ยนสถานที่ไม่เยื้องซ้าย
บรรทัด 1966–1968: จอกว้างไม่เกิน 720 พิกเซล: ทับกฎ .pf-grid-b (แถวที่พัก Tips ปุ่มค้นหา) ให้เป็นคอลัมน์เดียว เพราะกฎสามคอลัมน์ที่เขียนไว้ด้านบนอยู่หลังกฎจอแคบเดิมจึงทับกฎนั้น ทำให้ช่องที่พักแคบเกินไปบนมือถือ
บรรทัด 1970–1973  ปุ่มรายละเอียดโรงแรม
1970  .hotel-info-btn { display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; margin-left: .35rem; vertical-align: middle;
1971    border: 1px solid var(--border-subtle, rgba(255,255,255,.15)); border-radius: 8px; background: transparent; color: var(--text-muted); cursor: pointer; }
1972  .hotel-info-btn svg { width: 15px; height: 15px; }
1973  .hotel-info-btn:hover { color: var(--accent-primary); }
บรรทัด 1970–1973: .hotel-info-btn ปุ่มหมุดเล็กข้างชื่อโรงแรมในการ์ดแพ็กเกจ (กดเปิดหน้ารายละเอียดและรีวิวของโรงแรมด้วย showHotelDetail ใน ➜ frontend/app.js) ขนาด 26 พิกเซล ขอบบาง และเปลี่ยนเป็นสีส้มของธีมเมื่อชี้

ไฟล์ที่เชื่อมกับไฟล์นี้
frontend/app.js
frontend/extras.js
frontend/index.html
frontend/results.html
frontend/tooltip.js
frontend/tutorial.js