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
บรรทัด 463–633  หน้าต่าง โมดัล และการสุ่มใหม่
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
505  .modal-sub { font-size: 0.85rem; color: var(--text-tertiary); margin-top: 0.25rem; }
506  /* swap modal search bar */
507  .modal-search { margin-bottom: 0.75rem; }
508  .modal-search input {
509    width: 100%; box-sizing: border-box;
510    padding: 0.6rem 1rem;
511    background: var(--bg-elevated);
512    border: 1px solid var(--border-subtle);
513    border-radius: var(--radius-md);
514    color: var(--text-primary);
515    font-size: 0.93rem;
516    outline: none;
517    transition: var(--transition);
518  }
519  .modal-search input:focus { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(255,109,53,0.15); }
520
521  /* Re-shuffle button */
522  .reshuffle-btn {
523    display: inline-flex; align-items: center; gap: 0.45rem;
524    padding: 0.5rem 1.1rem;
525    background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(6,182,212,0.18));
526    border: 1px solid rgba(99,102,241,0.4);
527    border-radius: var(--radius-md);
528    color: var(--text-primary);
529    font-size: 0.85rem; font-weight: 600;
530    cursor: pointer;
531    transition: var(--transition);
532  }
533  .reshuffle-btn:hover { background: linear-gradient(135deg, rgba(99,102,241,0.32), rgba(6,182,212,0.28)); border-color: var(--accent-primary); }
534  .reshuffle-btn svg { width: 15px; height: 15px; stroke: var(--accent-primary); }
535  /* Blur overlay while reshuffling */
536  .detail-section { transition: var(--transition); }
537  .detail-section.reshuffling {
538    pointer-events: none;
539  }
540  /* Blur everything EXCEPT the spinner overlay */
541  .detail-section.reshuffling > *:not(#reshuffleOverlay) {
542    filter: blur(6px) saturate(0.3) brightness(0.7);
543    opacity: 0.45;
544    transition: filter 0.35s ease, opacity 0.35s ease;
545  }
546
547  /* Reshuffle animated overlay (injected by JS) */
548  #reshuffleOverlay {
549    position: absolute;
550    inset: 0;
551    display: flex;
552    align-items: center;
553    justify-content: center;
554    z-index: 50;
555    pointer-events: none;
556    animation: fadeIn 250ms ease;
557    border-radius: var(--radius-lg);
558  }
559  .reshuffle-overlay-inner {
560    display: flex;
561    flex-direction: column;
562    align-items: center;
563    gap: 0.8rem;
564    padding: 1.5rem 2.8rem;
565    background: rgba(10, 14, 26, 0.6);
566    backdrop-filter: blur(8px);
567    -webkit-backdrop-filter: blur(8px);
568    border-radius: var(--radius-xl);
569    border: 1px solid rgba(34, 211, 238, 0.35);
570    box-shadow: 0 0 50px rgba(34, 211, 238, 0.15), inset 0 1px 0 rgba(255,255,255,0.06);
571  }
572  .reshuffle-ring {
573    width: 54px; height: 54px;
574    animation: spin 0.85s linear infinite;
575    filter: drop-shadow(0 0 10px rgba(34, 211, 238, 0.7));
576  }
577  .reshuffle-overlay-inner span {
578    font-size: 0.95rem;
579    font-weight: 600;
580    color: var(--accent-glow);
581    letter-spacing: 0.03em;
582  }
583
584  .cat-filter {
585    display: flex; flex-wrap: wrap; gap: 0.4rem;
586    padding-bottom: 0.85rem;
587    margin-bottom: 0.75rem;
588    border-bottom: 1px solid var(--border-subtle);
589  }
590  .cat-btn {
591    padding: 0.35rem 0.75rem;
592    background: var(--bg-elevated);
593    border: 1px solid var(--border-subtle);
594    border-radius: 999px;
595    font-size: 0.78rem;
596    color: var(--text-secondary);
597    transition: var(--transition);
598  }
599  .cat-btn:hover { color: var(--text-primary); border-color: var(--border-default); }
600  .cat-btn.active {
601    background: var(--grad-cta); color: white; border-color: transparent;
602    box-shadow: var(--shadow-sm);
603  }
604
605  .swap-list {
606    overflow-y: auto;
607    flex: 1;
608    list-style: none;
609    margin: 0;
610    padding: 0;
611    width: 100%;
612  }
613  .swap-list::-webkit-scrollbar { width: 6px; }
614  .swap-list::-webkit-scrollbar-thumb { background: var(--border-default); border-radius: 3px; }
615  .swap-option {
616    display: flex; justify-content: space-between; align-items: center;
617    padding: 0.7rem 0.85rem;
618    margin: 0.3rem 1.75rem;
619    background: var(--bg-elevated);
620    border: 1px solid var(--border-subtle);
621    border-radius: var(--radius-md);
622    cursor: pointer;
623    transition: var(--transition);
624  }
625  .swap-option:hover { border-color: var(--accent-primary); transform: scale(1.025); box-shadow: 0 4px 16px rgba(255,109,53,0.2); background: var(--bg-surface); }
626  .swap-option .opt-info b { font-size: 0.92rem; }
627  .swap-option .opt-info .meta { font-size: 0.75rem; color: var(--text-tertiary); margin-top: 0.15rem; display: block; }
628  .empty-msg {
629    text-align: center; color: var(--text-muted);
630    padding: 2rem 0; font-size: 0.9rem;
631  }
632
633  /* --- Toasts --- */
บรรทัด 463–504: .modal .modal-backdrop .modal-card .modal-head .modal-body และอนิเมชัน fadeIn scaleIn (ใช้กับโมดัลสลับสถานที่ แผนทางเลือก และรายละเอียดสถานที่)
บรรทัด 505–518: ช่องค้นหาในโมดัลสลับสถานที่ (➜ filterSwapList() ใน frontend/app.js)
บรรทัด 519–544: ปุ่ม Re-shuffle และการเบลอส่วนรายละเอียดระหว่างสุ่ม (.detail-section.reshuffling)
บรรทัด 545–581: ตัวครอบและวงแหวนหมุนของ #reshuffleOverlay ที่ ➜ reshufflePackage() ใน frontend/app.js แทรกเข้ามา
บรรทัด 582–633: ตัวกรองหมวด .cat-filter .cat-btn และรายการตัวเลือก .swap-option ของ ➜ renderSwapList() ใน frontend/app.js
บรรทัด 634–708  แจ้งเตือน หน้าจอแคบ และหมุดแผนที่
634  .toast-container {
635    position: fixed; top: 90px; right: 1.5rem; z-index: 1100;
636    display: flex; flex-direction: column; gap: 0.5rem;
637    pointer-events: none;
638  }
639  .toast {
640    padding: 0.85rem 1.1rem;
641    background: var(--bg-elevated);
642    border: 1px solid var(--border-default);
643    border-radius: var(--radius-md);
644    box-shadow: var(--shadow-lg);
645    font-size: 0.9rem;
646    color: var(--text-primary);
647    display: flex; align-items: center; gap: 0.6rem;
648    animation: toastIn 300ms ease both;
649    pointer-events: auto;
650    min-width: 240px;
651  }
652  .toast.ok { border-color: rgba(16,185,129,0.4); }
653  .toast.error { border-color: rgba(239,68,68,0.4); }
654  .toast.loading { border-color: rgba(245,158,11,0.4); }
655  .toast .toast-icon { flex-shrink: 0; width: 18px; height: 18px; }
656  .toast.ok .toast-icon { color: var(--accent-success); }
657  .toast.error .toast-icon { color: var(--accent-danger); }
658  .toast.loading .toast-icon { color: var(--accent-warning); animation: spin 1s linear infinite; }
659  @keyframes toastIn { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
660  @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
661
662  /* --- Responsive --- */
663  @media (max-width: 980px) {
664
665    .packages-grid { grid-template-columns: 1fr; }
666    .detail-grid { grid-template-columns: 1fr; }
667    .map-wrap { position: static; }
668    #map { height: 400px; }
669    .topbar { padding: 1rem; }
670    .section-head { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
671    .detail-actions { flex-wrap: wrap; }
672  }
673
674  /* --- Map custom markers --- */
675  .map-hotel-marker {
676    width: 40px; height: 40px;
677    background: var(--grad-cta);
678    border: 3px solid white;
679    border-radius: 50%;
680    display: flex; align-items: center; justify-content: center;
681    font-size: 18px;
682    box-shadow: 0 4px 12px rgba(0,0,0,0.4), 0 0 0 4px rgba(6,182,212,0.25);
683  }
684  .map-poi-marker {
685    width: 36px; height: 36px;
686    background: var(--c, #06b6d4);
687    border: 2px solid white;
688    border-radius: 50%;
689    display: flex; align-items: center; justify-content: center;
690    font-weight: 700;
691    color: white;
692    box-shadow: 0 4px 10px rgba(0,0,0,0.35);
693    font-feature-settings: 'tnum';
694    position: relative;
695  }
696  .map-poi-marker .d {
697    font-size: 11px;
698    line-height: 1;
699    margin-bottom: -2px;
700    opacity: 0.85;
701  }
702  .map-poi-marker .p {
703    font-size: 14px;
704    line-height: 1;
705    font-weight: 800;
706  }
707
708  /* === User-requested fixes === */
บรรทัด 634–662: .toast-container .toast (ok error loading) และอนิเมชัน toastIn slideUp ของ ➜ showToast() ใน frontend/app.js
บรรทัด 663–674: @media (max-width: 980px) ปรับโครงเป็นคอลัมน์เดียว
บรรทัด 675–708: หมุดแผนที่ .map-poi-marker (วงกลมสีของวันพร้อมเลขวันและลำดับ) และ .map-hotel-marker ที่ ➜ drawOnMap() ใน frontend/app.js สร้าง
บรรทัด 709–780  ชุดแก้ไขตามคำขอ
709
710  /* 1) Remove number spinner arrows (Chrome/Safari/Firefox) */
711  input[type=number]::-webkit-inner-spin-button,
712  input[type=number]::-webkit-outer-spin-button {
713    -webkit-appearance: none;
714    margin: 0;
715  }
716  input[type=number] { -moz-appearance: textfield; appearance: textfield; }
717
718
719  .date-summary {
720    font-size: 0.78rem;
721    color: var(--text-tertiary);
722    margin-top: 0.5rem;
723    padding: 0.4rem 0.6rem;
724    background: var(--bg-elevated);
725    border-radius: 6px;
726    border-left: 3px solid var(--accent-primary);
727  }
728  .date-summary.invalid { border-left-color: var(--accent-danger); color: var(--accent-danger); }
729  .date-summary.oneday {
730    border-left-color: #10b981; color: #10b981;
731    background: rgba(16,185,129,0.08);
732  }
733
734  /* One-day-trip lock badge (inline beside title) */
735  .hotel-lock-badge {
736    display: inline-flex; align-items: center;
737    font-size: 0.7rem; font-weight: 600;
738    background: rgba(16,185,129,0.15); color: #10b981;
739    border: 1px solid rgba(16,185,129,0.3);
740    border-radius: 20px; padding: 2px 9px; white-space: nowrap; flex-shrink: 0;
741  }
742
743  /* 4) Smaller "เพิ่มสถานที่" button - looks like POI item with + icon */
744  .day-add {
745    display: flex; align-items: center; gap: 0.6rem;
746    width: 100%;
747    margin-top: 0.5rem;
748    padding: 0.55rem 0.75rem;
749    background: transparent;
750    border: 1px dashed var(--border-default);
751    border-radius: var(--radius-sm);
752    color: var(--text-tertiary);
753    font-size: 0.88rem;
754    text-align: left;
755    transition: var(--transition);
756  }
757  .day-add:hover {
758    border-color: var(--accent-primary);
759    border-style: solid;
760    color: var(--accent-primary);
761    background: var(--bg-elevated);
762  }
763  .day-add svg { width: 16px; height: 16px; flex-shrink: 0; }
764  .day-add .add-num {
765    width: 28px; height: 28px; flex-shrink: 0;
766    border: 1px dashed currentColor;
767    border-radius: 50%;
768    display: flex; align-items: center; justify-content: center;
769    opacity: 0.7;
770  }
771
772  /* 5) FIX: gentler dark mode tile filter (was breaking map appearance) */
773  [data-theme="dark"] .leaflet-tile-pane {
774    filter: brightness(0.85) saturate(0.7) hue-rotate(180deg) invert(0.92);
775  }
776  .leaflet-control-zoom a {
777    background: var(--bg-elevated) !important;
778    color: var(--text-primary) !important;
779    border-color: var(--border-default) !important;
780  }
บรรทัด 709–734: การปรับช่องตัวเลข สรุปวันที่ (.date-summary สถานะ oneday/invalid) และรายละเอียดเล็กน้อยที่ปรับตามคำขอ
บรรทัด 735–763: ป้ายล็อกของทริปวันเดียวและการ์ดโรงแรมแบบล็อก (➜ setOneDayTripMode() ใน frontend/app.js)
บรรทัด 764–780: ปุ่ม .day-add (เพิ่มสถานที่) และการปรับภาพแผนที่ในธีมมืด
บรรทัด 781–840  พื้นหลังออโรรา
781  .leaflet-control-attribution {
782    background: var(--bg-elevated) !important;
783    color: var(--text-tertiary) !important;
784    border-radius: 4px;
785    font-size: 10px;
786  }
787
788  /* === V3 Updates: Aurora background, Flatpickr, scrollable select === */
789
790
791  /* New background layers */
792  .bg-layers {
793    position: fixed; inset: 0; z-index: -1;
794    overflow: hidden;
795    pointer-events: none;
796  }
797
798  /* Subtle grid */
799  .bg-grid {
800    position: absolute; inset: 0;
801    background-image:
802      linear-gradient(rgba(148,163,184,0.04) 1px, transparent 1px),
803      linear-gradient(90deg, rgba(148,163,184,0.04) 1px, transparent 1px);
804    background-size: 60px 60px;
805    mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
806    -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
807  }
808  [data-theme="light"] .bg-grid {
809    background-image:
810      linear-gradient(rgba(15,23,42,0.04) 1px, transparent 1px),
811      linear-gradient(90deg, rgba(15,23,42,0.04) 1px, transparent 1px);
812  }
813
814  /* Aurora orbs - animated */
815  .bg-aurora { position: absolute; inset: 0; }
816  .bg-aurora .orb {
817    position: absolute;
818    border-radius: 50%;
819    filter: blur(140px);
820    opacity: 0.55;
821    will-change: transform;
822  }
823  .bg-aurora .orb-1 { width: 520px; height: 520px; background: #ff6d35; top: -80px; left: -120px; animation: drift1 22s ease-in-out infinite alternate; }
824  .bg-aurora .orb-2 { width: 600px; height: 600px; background: #b84000; top: 25%; right: -200px; animation: drift2 28s ease-in-out infinite alternate; }
825  .bg-aurora .orb-3 { width: 460px; height: 460px; background: #f97316; bottom: -120px; left: 25%; opacity: 0.35; animation: drift3 30s ease-in-out infinite alternate; }
826  .bg-aurora .orb-4 { width: 380px; height: 380px; background: #cc3300; top: 55%; left: 8%; opacity: 0.10; animation: drift4 26s ease-in-out infinite alternate; }
827  .bg-aurora .orb-5 { width: 420px; height: 420px; background: #ff7722; top: 5%; left: 45%; opacity: 0.08; animation: drift5 32s ease-in-out infinite alternate; }
828
829  [data-theme="light"] .bg-aurora .orb { opacity: 0.22; }
830  [data-theme="light"] .bg-aurora .orb-3,
831  [data-theme="light"] .bg-aurora .orb-4,
832  [data-theme="light"] .bg-aurora .orb-5 { opacity: 0.15; }
833
834  @keyframes drift1 { from { transform: translate(0, 0) scale(1); } to { transform: translate(120px, 80px) scale(1.15); } }
835  @keyframes drift2 { from { transform: translate(0, 0) scale(1); } to { transform: translate(-150px, 100px) scale(1.1); } }
836  @keyframes drift3 { from { transform: translate(0, 0) scale(1); } to { transform: translate(80px, -120px) scale(0.9); } }
837  @keyframes drift4 { from { transform: translate(0, 0) scale(1); } to { transform: translate(180px, -80px) scale(1.2); } }
838  @keyframes drift5 { from { transform: translate(0, 0) scale(1); } to { transform: translate(-100px, 120px) scale(1.1); } }
839
840  /* Subtle film grain (SVG noise) */
บรรทัด 781–840: .bg-layers ตาราง .bg-grid ลูกแสงห้าก้อนที่เคลื่อนช้า ๆ (@keyframes drift1–drift5) และเกรนฟิล์ม SVG (ลักษณะตามองค์ประกอบใน ➜ frontend/index.html)
บรรทัด 841–1021  ช่องวันที่และธีมของ flatpickr
841  .bg-grain {
842    position: absolute; inset: 0;
843    background-image: url("data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PScwIDAgMjAwIDIwMCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJz48ZmlsdGVyIGlkPSdub2lzZUZpbHRlcic+PGZlVHVyYnVsZW5jZSB0eXBlPSdmcmFjdGFsTm9pc2UnIGJhc2VGcmVxdWVuY3k9JzAuOScgbnVtT2N0YXZlcz0nMScgc3RpdGNoVGlsZXM9J3N0aXRjaCcvPjwvZmlsdGVyPjxyZWN0IHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEwMCUnIGZpbHRlcj0ndXJsKCNub2lzZUZpbHRlciknLz48L3N2Zz4=");
844    opacity: 0.04;
845    mix-blend-mode: overlay;
846  }
847  [data-theme="light"] .bg-grain { opacity: 0.06; mix-blend-mode: multiply; }
848
849
850  /* === New date range input (single field for Flatpickr) === */
851  .date-range-input {
852    display: flex; align-items: center; gap: 0.6rem;
853    background: var(--bg-elevated);
854    border: 1px solid var(--border-subtle);
855    border-radius: var(--radius-md);
856    padding: 0.65rem 1rem;
857    cursor: pointer;
858    transition: var(--transition);
859  }
860  .date-range-input:hover { border-color: var(--border-default); }
861  .date-range-input:focus-within { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(255,109,53,0.15); }
862  .date-range-input .date-icon { width: 18px; height: 18px; color: var(--text-tertiary); flex-shrink: 0; pointer-events: none; }
863  .date-range-input input {
864    flex: 1; padding: 0; border: none; outline: none;
865    background: transparent;
866    font-size: 0.95rem; font-weight: 600;
867    color: var(--text-primary);
868    cursor: pointer;
869  }
870  .date-range-input input::placeholder { color: var(--text-tertiary); font-weight: 500; }
871
872  /* === Flatpickr theming === */
873  .flatpickr-calendar {
874    background: #1a1208 !important;
875    border: 1px solid var(--border-default) !important;
876    border-radius: var(--radius-lg) !important;
877    box-shadow: 0 20px 60px rgba(0,0,0,0.6) !important;
878    font-family: var(--font-sans) !important;
879    width: 320px !important;
880    padding: 0.5rem !important;
881    z-index: 99999 !important;
882  }
883  [data-theme="light"] .flatpickr-calendar { background: #ffffff !important; }
884
885  /* Year input — ซ่อน default arrows, ใช้ปุ่ม custom แทน */
886  .flatpickr-current-month .numInputWrapper { pointer-events: auto !important; }
887  .flatpickr-current-month input.cur-year {
888    pointer-events: auto !important;
889    cursor: default !important;
890    background: transparent !important;
891    border: none !important;
892    padding: 0 2px !important;
893    color: var(--text-primary) !important;
894    font-weight: 700 !important;
895  }
896  .numInputWrapper span.arrowUp,
897  .numInputWrapper span.arrowDown { display: none !important; }
898
899  /* Custom year nav buttons */
900  .fp-year-prev, .fp-year-next {
901    display: inline-flex; align-items: center; justify-content: center;
902    width: 22px; height: 22px; border-radius: 50%;
903    cursor: pointer; font-size: 1rem; font-weight: 700;
904    color: var(--text-secondary);
905    background: transparent;
906    border: none;
907    transition: background 0.15s, color 0.15s;
908    user-select: none;
909    vertical-align: middle;
910  }
911  .fp-year-prev:hover, .fp-year-next:hover {
912    background: rgba(255,109,53,0.15);
913    color: var(--accent-primary);
914  }
915  .flatpickr-calendar.arrowTop:before,
916  .flatpickr-calendar.arrowTop:after { border-bottom-color: var(--border-default) !important; }
917  .flatpickr-calendar.arrowBottom:before,
918  .flatpickr-calendar.arrowBottom:after { border-top-color: var(--border-default) !important; }
919
920  .flatpickr-months {
921    padding: 0.5rem 0 0.75rem !important;
922    border-bottom: 1px solid var(--border-subtle);
923  }
924  .flatpickr-month {
925    background: transparent !important;
926    color: var(--text-primary) !important;
927    height: 36px !important;
928    display: flex !important;
929    align-items: center !important;
930    justify-content: center !important;
931  }
932  .flatpickr-current-month {
933    color: var(--text-primary) !important;
934    font-size: 0.95rem !important;
935    font-weight: 700 !important;
936    padding: 0 !important;
937    display: flex !important;
938    align-items: center !important;
939    justify-content: center !important;
940    gap: 4px !important;
941    width: 100% !important;
942    position: static !important;
943  }
944  .flatpickr-current-month .numInputWrapper { color: var(--text-primary) !important; }
945  .flatpickr-current-month input.cur-year {
946    color: var(--text-primary) !important;
947    font-weight: 700 !important;
948  }
949  .flatpickr-monthDropdown-months {
950    background: #1a1208 !important;
951    color: var(--text-primary) !important;
952    font-weight: 600 !important;
953    border-radius: 6px;
954  }
955  [data-theme="light"] .flatpickr-monthDropdown-months { background: #ffffff !important; }
956  .flatpickr-monthDropdown-month { background: #1a1208 !important; }
957  [data-theme="light"] .flatpickr-monthDropdown-month { background: #ffffff !important; }
958
959  .flatpickr-prev-month, .flatpickr-next-month {
960    color: var(--text-secondary) !important;
961    fill: var(--text-secondary) !important;
962    padding: 8px !important;
963    border-radius: 8px;
964    transition: var(--transition);
965  }
966  .flatpickr-prev-month:hover, .flatpickr-next-month:hover {
967    color: var(--accent-glow) !important;
968    fill: var(--accent-glow) !important;
969    background: var(--bg-base) !important;
970  }
971
972  .flatpickr-weekdays { background: transparent !important; padding: 0.5rem 0; }
973  .flatpickr-weekday {
974    color: var(--text-tertiary) !important;
975    font-weight: 600 !important;
976    font-size: 0.75rem !important;
977    text-transform: uppercase;
978    letter-spacing: 0.04em;
979  }
980
981  .flatpickr-day {
982    color: var(--text-secondary) !important;
983    border-radius: 8px !important;
984    font-weight: 500 !important;
985    transition: var(--transition);
986    border: 1px solid transparent !important;
987    height: 38px !important;
988    line-height: 38px !important;
989    margin: 1px 0;
990  }
991  .flatpickr-day:hover {
992    background: var(--bg-base) !important;
993    color: var(--text-primary) !important;
994  }
995  .flatpickr-day.today {
996    border-color: var(--accent-primary) !important;
997    color: var(--accent-glow) !important;
998  }
999  .flatpickr-day.today:hover { background: var(--accent-primary) !important; color: white !important; }
1000  .flatpickr-day.selected,
1001  .flatpickr-day.startRange,
1002  .flatpickr-day.endRange,
1003  .flatpickr-day.selected.inRange,
1004  .flatpickr-day.startRange.inRange,
1005  .flatpickr-day.endRange.inRange {
1006    background: var(--accent-primary) !important;
1007    border-color: var(--accent-primary) !important;
1008    color: white !important;
1009    box-shadow: 0 4px 12px rgba(255,109,53,0.3);
1010  }
1011  .flatpickr-day.inRange {
1012    background: rgba(255,109,53,0.15) !important;
1013    border-color: transparent !important;
1014    color: var(--text-primary) !important;
1015    box-shadow: none !important;
1016  }
1017  .flatpickr-day.startRange { border-radius: 8px 0 0 8px !important; }
1018  .flatpickr-day.endRange { border-radius: 0 8px 8px 0 !important; }
1019  .flatpickr-day.startRange.endRange { border-radius: 8px !important; }
1020  .flatpickr-day.flatpickr-disabled,
1021  .flatpickr-day.prevMonthDay,
บรรทัด 841–862: .date-range-input ช่องวันที่ช่องเดียว (โฟกัส และ placeholder)
บรรทัด 863–1021: ตกแต่งปฏิทิน flatpickr ให้เข้ากับธีม: เดือน ปี ปุ่ม ‹ › ที่เพิ่มด้วย ➜ initDateRange() ใน frontend/app.js ชื่อวัน วันที่ที่ชี้ ช่วงที่เลือก และวันของเดือนอื่น
บรรทัด 1022–1115  รุ่น V4–V6
1022  .flatpickr-day.nextMonthDay {
1023    color: var(--text-muted) !important;
1024    opacity: 0.4;
1025  }
1026
1027  .numInput, .numInputWrapper span {
1028    color: var(--text-primary) !important;
1029  }
1030  .flatpickr-time { background: var(--bg-elevated) !important; border-top: 1px solid var(--border-subtle); }
1031
1032  /* === V4 Updates === */
1033
1034
1035  /* 2) Custom scrollbars (whole page) */
1036  * { scrollbar-width: thin; scrollbar-color: var(--border-default) transparent; }
1037  *::-webkit-scrollbar { width: 10px; height: 10px; }
1038  *::-webkit-scrollbar-track { background: transparent; }
1039  *::-webkit-scrollbar-thumb {
1040    background: linear-gradient(180deg, var(--border-default), var(--border-strong));
1041    border-radius: 5px;
1042    border: 2px solid transparent;
1043    background-clip: padding-box;
1044  }
1045  *::-webkit-scrollbar-thumb:hover {
1046    background: linear-gradient(180deg, var(--accent-primary), var(--accent-glow));
1047    background-clip: padding-box;
1048    border: 2px solid transparent;
1049  }
1050  *::-webkit-scrollbar-corner { background: transparent; }
1051
1052  /* 3) Day toggles (filter routes on map by day) */
1053  .day-toggles {
1054    display: flex; flex-wrap: wrap; gap: 0.5rem;
1055    padding: 0.75rem;
1056    background: var(--bg-surface);
1057    backdrop-filter: blur(20px);
1058    -webkit-backdrop-filter: blur(20px);
1059    border: 1px solid var(--border-subtle);
1060    border-radius: var(--radius-md);
1061    margin-bottom: 0.75rem;
1062  }
1063  .day-toggle {
1064    display: inline-flex; align-items: center; gap: 0.5rem;
1065    padding: 0.4rem 0.85rem;
1066    background: var(--bg-elevated);
1067    border: 1px solid var(--border-subtle);
1068    border-radius: 999px;
1069    font-size: 0.82rem; font-weight: 600;
1070    color: var(--text-tertiary);
1071    transition: var(--transition);
1072    cursor: pointer;
1073  }
1074  .day-toggle .day-dot {
1075    width: 8px; height: 8px; border-radius: 50%;
1076    background: var(--c, var(--accent-primary));
1077    opacity: 0.4;
1078    transition: var(--transition);
1079  }
1080  .day-toggle.active {
1081    background: var(--bg-base);
1082    color: var(--text-primary);
1083    border-color: var(--c, var(--accent-primary));
1084    box-shadow: 0 0 0 1px var(--c, var(--accent-primary));
1085  }
1086  .day-toggle.active .day-dot {
1087    opacity: 1;
1088    box-shadow: 0 0 8px var(--c, var(--accent-primary));
1089  }
1090  .day-toggle:hover { color: var(--text-primary); }
1091  .day-toggle.show-all {
1092    background: var(--grad-cta);
1093    color: white;
1094    border-color: transparent;
1095  }
1096  .day-toggle.show-all:hover { opacity: 0.9; }
1097
1098  /* === V5: Validation error state === */
1099  .input-with-unit.has-error,
1100  .date-range-input.has-error,
1101  .select-input.has-error {
1102    border-color: var(--accent-danger) !important;
1103    box-shadow: 0 0 0 3px rgba(239,68,68,0.18) !important;
1104  }
1105  .input-with-unit.has-error .unit { color: var(--accent-danger); }
1106
1107  @keyframes shake {
1108    0%, 100% { transform: translateX(0); }
1109    20%, 60% { transform: translateX(-4px); }
1110    40%, 80% { transform: translateX(4px); }
1111  }
1112  .has-error { animation: shake 320ms ease; }
1113
1114  /* === V6: Subtle gradient body background === */
1115  [data-theme="dark"] body {
บรรทัด 1022–1085: แถบเลื่อนทั้งหน้า ปุ่มสลับวัน .day-toggle และสถานะ active ของ ➜ renderDayToggles() ใน frontend/app.js
บรรทัด 1086–1101: สถานะผิดพลาดของช่องกรอก .has-error พร้อมอนิเมชันสั่น shake (➜ highlightField() ใน frontend/app.js)
บรรทัด 1102–1115: พื้นหลังไล่สีอ่อนของ body
บรรทัด 1116–1246  รุ่น V7–V8
1116    background:
1117      radial-gradient(ellipse at top left,    rgba(6,182,212,0.08), transparent 50%),
1118      radial-gradient(ellipse at bottom right, rgba(167,139,250,0.08), transparent 50%),
1119      linear-gradient(180deg, #0a0e1a 0%, #0d1424 50%, #0a0e1a 100%);
1120  }
1121  [data-theme="light"] body {
1122    background:
1123      radial-gradient(ellipse at top left,    rgba(6,182,212,0.06), transparent 50%),
1124      radial-gradient(ellipse at bottom right, rgba(167,139,250,0.06), transparent 50%),
1125      linear-gradient(180deg, #f6f7fb 0%, #eef2f9 50%, #f6f7fb 100%);
1126  }
1127
1128  /* === V7: Hide-all button & realistic schedule == */
1129  .day-toggle.hide-all {
1130    background: rgba(239, 68, 68, 0.15);
1131    color: #fca5a5;
1132    border-color: rgba(239, 68, 68, 0.4);
1133  }
1134  .day-toggle.hide-all:hover {
1135    background: rgba(239, 68, 68, 0.25);
1136    color: #fecaca;
1137  }
1138  .day-toggle svg { flex-shrink: 0; }
1139
1140  /* === V8: Algorithm selector === */
1141  .algo-segment {
1142    display: grid;
1143    grid-template-columns: repeat(3, 1fr);
1144    gap: 4px;
1145    background: var(--bg-elevated);
1146    padding: 4px;
1147    border-radius: var(--radius-md);
1148    border: 1px solid var(--border-subtle);
1149  }
1150  .algo-segment button {
1151    padding: 0.65rem 0.5rem;
1152    border-radius: 8px;
1153    font-weight: 600;
1154    font-size: 0.86rem;
1155    color: var(--text-tertiary);
1156    transition: var(--transition);
1157  }
1158  .algo-segment button:hover { color: var(--text-primary); background: rgba(255,255,255,0.04); }
1159  .algo-segment button.active {
1160    background: var(--grad-cta);
1161    color: white;
1162    box-shadow: 0 4px 10px rgba(255,109,53,0.3);
1163  }
1164
1165
1166  /* ── Hotel option card ── */
1167  .hotel-card {
1168    display: flex; align-items: center; gap: 14px;
1169    padding: 14px 16px; border-radius: var(--radius-md);
1170    background: var(--bg-surface);
1171    border: 1px solid var(--border-default);
1172    cursor: pointer; transition: var(--transition);
1173    user-select: none;
1174  }
1175  .hotel-card:hover { border-color: var(--accent-cyan); }
1176  .hotel-card.hotel-card-locked {
1177    border-color: #10b981;
1178    background: rgba(16,185,129,0.06);
1179    cursor: default;
1180  }
1181  .hotel-card-icon {
1182    font-size: 1.5rem; flex-shrink: 0;
1183    width: 42px; height: 42px;
1184    display: flex; align-items: center; justify-content: center;
1185    background: var(--bg-elevated);
1186    border-radius: var(--radius-sm);
1187  }
1188  .hotel-card-body { flex: 1; min-width: 0; }
1189  .hotel-card-title-row {
1190    display: flex; align-items: center; gap: 8px;
1191    margin-bottom: 2px;
1192  }
1193  .hotel-card-title {
1194    font-weight: 600; font-size: 0.9rem;
1195    color: var(--text-primary);
1196  }
1197  .hotel-card-switch {
1198    flex-shrink: 0; display: flex; align-items: center;
1199  }
1200  .hotel-card-switch input[type="checkbox"] { display: none; }
1201  .toggle-track {
1202    width: 44px; height: 24px;
1203    background: var(--bg-elevated);
1204    border: 1.5px solid var(--border-default);
1205    border-radius: 12px;
1206    position: relative; cursor: pointer;
1207    transition: background 0.2s ease, border-color 0.2s ease;
1208    display: block;
1209  }
1210  input[type="checkbox"]:checked + .toggle-track,
1211  input[type="checkbox"]:checked + label.toggle-track {
1212    background: var(--accent-primary);
1213    border-color: var(--accent-primary);
1214  }
1215  .toggle-thumb {
1216    position: absolute; top: 2px; left: 2px;
1217    width: 18px; height: 18px;
1218    background: white; border-radius: 50%;
1219    transition: transform 0.2s ease;
1220    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
1221  }
1222  input[type="checkbox"]:checked + .toggle-track .toggle-thumb {
1223    transform: translateX(18px);
1224  }
1225  .hotel-lock-badge {
1226    font-size: 0.68rem; font-weight: 700;
1227    background: #10b981; color: white;
1228    padding: 1px 7px; border-radius: 99px;
1229    letter-spacing: 0.02em;
1230  }
1231  .date-summary.oneday { border-left-color: #10b981; color: #10b981; }
1232
1233  /* ── Distance connectors between POIs ── */
1234  .dist-connector {
1235    display: flex; align-items: center; gap: 0.4rem;
1236    padding: 0.05rem 0.5rem;
1237    list-style: none;
1238  }
1239  .dist-line {
1240    flex: 1; height: 1px;
1241    background: linear-gradient(90deg, transparent, var(--border-default), transparent);
1242  }
1243  .dist-badge {
1244    font-size: 0.68rem; color: var(--text-muted);
1245    white-space: nowrap;
1246    padding: 1px 7px;
บรรทัด 1116–1128: ปุ่มซ่อนทุกวันและตารางเวลาแบบสมจริง
บรรทัด 1129–1163: ตัวเลือกอัลกอริทึม .algo-segment (ใน ➜ initAlgoControl() ใน frontend/app.js)
บรรทัด 1164–1234: การ์ดโรงแรม .hotel-card สวิตช์ .toggle-track ป้ายล็อก และป้ายระยะทาง .dist-badge ในรายการ
บรรทัด 1235–1246: รายละเอียดป้ายระยะทาง
บรรทัด 1247–1584  โครงหน้าแบบใหม่ (หน้า landing และเมนูจังหวัด)
1247    background: var(--bg-elevated);
1248    border: 1px solid var(--border-subtle);
1249    border-radius: 8px;
1250    font-feature-settings: 'tnum';
1251    letter-spacing: 0.01em;
1252  }
1253
1254
1255  /* ================================================================
1256     NEW TRIPVENTURE LAYOUT
1257     ================================================================ */
1258
1259  .brand-trip { color: var(--accent-primary); }
1260  .topbar { padding: 0.65rem 2.5rem; }
1261
1262  /* Body background */
1263  html, body { background: #0d0b09 !important; }
1264  html[data-theme="light"], html[data-theme="light"] body { background: #ffffff !important; }
1265
1266  /* ── Landing screen ── */
1267  .landing-screen {
1268    min-height: 100vh;
1269    min-height: 100dvh;
1270    position: relative;
1271    background: #ffffff;
1272    overflow: visible;   /* ไม่ตัดเมนูเลือกจังหวัดที่ยื่นลงมาเกินหน้าจอแรก (เดิม hidden ทำให้ STEP 2 ทับเมนู) */
1273    display: flex; flex-direction: column;
1274  }
1275  [data-theme="dark"] .landing-screen {
1276    background: #0d0b09;
1277  }
1278
1279  /* ── Hero ── */
1280  .hero-visual {
1281    position: absolute;
1282    top: 0; left: 0; right: 0;
1283    width: 100%;
1284    height: 75vh;
1285    overflow: hidden;
1286    display: flex;
1287    align-items: center;
1288    justify-content: center;
1289    padding: 0;
1290  }
1291  .hero-bg {
1292    position: absolute; inset: 0;
1293    background-size: cover;
1294    background-position: center bottom;
1295    transform: scale(1.03);
1296    transition: transform 8s ease;
1297  }
1298  .hero-visual:hover .hero-bg { transform: scale(1.0); }
1299  .hero-overlay {
1300    position: absolute; inset: 0;
1301    background: linear-gradient(to bottom, rgba(8,5,2,0.42) 0%, rgba(8,5,2,0.28) 45%, rgba(8,5,2,0.68) 100%);
1302  }
1303  .hero-content {
1304    position: absolute; z-index: 2;
1305    top: 30%; left: 0; right: 0;
1306    transform: translateY(-50%);
1307    text-align: center;
1308    width: 100%;
1309    padding: 0 2rem;
1310    animation: slideUp 700ms ease both;
1311  }
1312  .hero-label {
1313    display: inline-block;
1314    font-size: 1rem; font-weight: 700;
1315    color: var(--accent-warm);
1316    text-transform: uppercase; letter-spacing: 0.14em;
1317    margin-bottom: 1.9rem;
1318    padding: 0.25rem 0.9rem; border-radius: 999px;
1319    background: rgba(255,255,255,0.88);
1320  }
1321  .hero-h1 {
1322    font-size: clamp(2.6rem, 5.5vw, 4.4rem);
1323    font-weight: 900; color: #fff;
1324    letter-spacing: -0.03em; line-height: 1.1;
1325    margin: 0 0 1rem; white-space: nowrap;
1326    text-shadow: 0 2px 24px rgba(0,0,0,0.5);
1327  }
1328  .hero-desc {
1329    font-size: 1rem; color: rgba(255,255,255,0.78);
1330    line-height: 1.7; margin: 0 auto; max-width: none; white-space: nowrap;
1331    text-shadow: 0 2px 16px rgba(0,0,0,0.6);
1332  }
1333
1334  /* ── Planner wrapper ── */
1335  .planner-wrapper {
1336    max-width: 1280px; width: 100%;
1337    position: relative;
1338    margin: auto auto 0; /* pins the panel to the bottom of the first screen */
1339    padding: 330px 2rem 1rem; /* top padding = min clearance for hero text on short screens */
1340    z-index: 10;
1341    pointer-events: none;
1342  }
1343  .planner-wrapper > * { pointer-events: auto; }
1344  .planner-panel {
1345    zoom: 0.9; /* scales the whole box and its contents uniformly */
1346    background: var(--bg-elevated);
1347    border: 1px solid var(--border-subtle);
1348    border-radius: var(--radius-xl);
1349    padding: 1.5rem 1.75rem 1.25rem;
1350    box-shadow: 0 16px 48px rgba(0,0,0,0.45);
1351    backdrop-filter: blur(24px);
1352    -webkit-backdrop-filter: blur(24px);
1353  }
1354  [data-theme="light"] .planner-panel {
1355    background: rgba(255,255,255,0.97);
1356    box-shadow: 0 16px 48px rgba(100,50,20,0.12);
1357  }
1358
1359  /* Header row */
1360  .planner-top-row {
1361    display: flex; align-items: center; gap: 0.75rem;
1362    margin-bottom: 1.1rem;
1363    padding-bottom: 0.9rem;
1364    border-bottom: 1px solid var(--border-subtle);
1365  }
1366  .planner-title { font-size: 1rem; font-weight: 700; flex: 1; }
1367  .ml-auto { margin-left: auto; }
1368
1369  /* Divider */
1370  .pf-divider {
1371    height: 1px; background: var(--border-subtle);
1372    margin: 1rem 0;
1373  }
1374
1375  /* Grid rows */
1376  .pf-grid {
1377    display: grid;
1378    grid-template-columns: 1fr 1fr 1.5fr 0.9fr;
1379    gap: 1rem;
1380    align-items: start;
1381  }
1382  .pf-grid-b {
1383    grid-template-columns: auto 1fr auto;  /* ที่พัก (กว้างเท่าเนื้อหา) + กล่อง Tips (ยืดเต็มที่เหลือ) + ปุ่มค้นหา */
1384    align-items: start;   /* ป้ายและปุ่มของทุกคอลัมน์อยู่ระนาบเดียวกัน */
1385  }
1386  .pf-col-search .pf-label { visibility: hidden; }
1387  .pf-algo-row { display: none; margin-top: 0.9rem; }
1388  .dev-mode .pf-algo-row { display: block; }
1389  .dev-btn { font-family: ui-monospace, Consolas, monospace; font-size: 0.8rem; font-weight: 700; }
1390  .dev-mode .dev-btn { color: #fff; background: var(--accent-primary, #ff6d35); border-color: transparent; }
1391  .pf-col { position: relative; }
1392  .pf-col-wide  { /* dates — wider */ }
1393  .pf-col-hotel { /* hotel toggle */ }
1394  .pf-col-algo  { /* algo segment */ }
1395  .pf-col-search { min-width: 148px; }
1396
1397  /* Labels */
1398  .pf-label {
1399    display: block;
1400    font-size: 0.73rem; font-weight: 600;
1401    color: var(--text-tertiary);
1402    text-transform: uppercase; letter-spacing: 0.07em;
1403    margin-bottom: 0.45rem;
1404    min-height: 1rem;
1405  }
1406
1407  /* Hint text below each control — reserves space */
1408  .pf-hint {
1409    font-size: 0.72rem; color: var(--text-muted);
1410    margin-top: 0.35rem; min-height: 1rem;
1411    line-height: 1.3;
1412  }
1413
1414  /* All controls same height */
1415  .planner-panel .select-input,
1416  .planner-panel .input-with-unit,
1417  .planner-panel .date-range-input,
1418  .planner-panel .counter-control,
1419  .planner-panel .hotel-card,
1420  .planner-panel .algo-segment { height: 48px; min-height: 48px; }
1421
1422  /* hotel card compact */
1423  .planner-panel .hotel-card {
1424    display: flex; align-items: center;
1425    padding: 0 0.85rem; gap: 0.6rem;
1426  }
1427
1428  /* algo segment height */
1429  .planner-panel .algo-segment {
1430    display: flex; align-items: center; padding: 4px;
1431  }
1432  .planner-panel .algo-segment button {
1433    flex: 1; height: 100%;
1434    display: flex; align-items: center; justify-content: center;
1435    gap: 5px;
1436    text-align: center;
1437    letter-spacing: 0;
1438  }
1439  .planner-panel .algo-segment button .btn-icon {
1440    display: inline-flex;
1441    align-items: center;
1442    width: 1em;
1443    justify-content: center;
1444    flex-shrink: 0;
1445  }
1446
1447  /* search button */
1448  .pf-col-search .cta-btn {
1449    height: 48px; width: 100%;
1450    padding: 0 1.25rem; font-size: 0.92rem;
1451  }
1452
1453
1454  /* Section backgrounds */
1455  .packages-section, .detail-section { background: #0d0b09; }
1456  html[data-theme="light"] .packages-section,
1457  html[data-theme="light"] .detail-section { background: #ffffff; }
1458
1459
1460  /* ── Province custom dropdown ── */
1461  .prov-select {
1462    position: relative;
1463    display: flex; align-items: center; gap: 0.55rem;
1464    height: 48px; min-height: 48px;
1465    padding: 0 0.9rem;
1466    background: var(--bg-elevated);
1467    border: 1.5px solid var(--border-subtle);
1468    border-radius: var(--radius-md);
1469    cursor: pointer;
1470    user-select: none;
1471    transition: border-color 0.18s, box-shadow 0.18s;
1472  }
1473  .prov-select:hover { border-color: var(--accent-primary); }
1474  .prov-select.open {
1475    border-color: var(--accent-primary);
1476    box-shadow: 0 0 0 3px rgba(255,109,53,0.18);
1477  }
1478  .prov-name { flex: 1; font-size: 0.9rem; font-weight: 600; color: var(--text-primary); }
1479  .prov-arrow {
1480    width: 16px; height: 16px; flex-shrink: 0;
1481    color: var(--text-tertiary);
1482    transition: transform 0.2s;
1483  }
1484  .prov-select.open .prov-arrow { transform: rotate(180deg); }
1485
1486  /* Dropdown panel */
1487  .prov-dropdown {
1488    position: absolute;
1489    top: calc(100% + 6px);
1490    left: 0; transform: translateY(-8px) scale(0.98);
1491    width: 280px; z-index: 999;
1492    background: var(--bg-elevated);
1493    border: 1.5px solid var(--border-subtle);
1494    border-radius: var(--radius-lg);
1495    box-shadow: 0 16px 48px rgba(0,0,0,0.45), 0 4px 16px rgba(0,0,0,0.3);
1496    backdrop-filter: blur(20px);
1497    overflow: hidden;
1498    opacity: 0;
1499    pointer-events: none;
1500    display: none;   /* ปิดอยู่ต้องไม่กินพื้นที่ (ไม่งั้นดันความสูงหน้าให้เลื่อนเกินจำเป็น) */
1501  }
1502  .prov-dropdown.open {
1503    display: block;
1504    opacity: 1; transform: translateY(0) scale(1);
1505    pointer-events: all;
1506    animation: provPop 0.18s ease both;
1507  }
1508  @keyframes provPop { from { opacity: 0; transform: translateY(-8px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
1509  @keyframes provPopUp { from { opacity: 0; transform: translateY(8px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
1510  /* เปิดขึ้นด้านบนเมื่อพื้นที่ด้านล่างไม่พอ */
1511  .prov-dropdown.drop-up {
1512    top: auto;
1513    bottom: calc(100% + 6px);
1514    transform: translateY(8px) scale(0.98);
1515  }
1516  .prov-dropdown.drop-up.open {
1517    transform: translateY(0) scale(1);
1518    animation-name: provPopUp;
1519  }
1520  [data-theme="light"] .prov-dropdown {
1521    background: #fff;
1522    box-shadow: 0 16px 48px rgba(100,50,20,0.16), 0 4px 16px rgba(0,0,0,0.08);
1523  }
1524
1525  /* Search box */
1526  .prov-search-wrap {
1527    display: flex; align-items: center; gap: 0.5rem;
1528    padding: 0.7rem 0.9rem;
1529    border-bottom: 1px solid var(--border-subtle);
1530  }
1531  .prov-search-wrap svg {
1532    width: 15px; height: 15px; flex-shrink: 0;
1533    color: var(--text-tertiary);
1534  }
1535  .prov-search-wrap input {
1536    flex: 1; border: none; background: transparent;
1537    font-size: 0.85rem; color: var(--text-primary);
1538    outline: none;
1539  }
1540  .prov-search-wrap input::placeholder { color: var(--text-muted); }
1541
1542  /* Scrollable list */
1543  .prov-list {
1544    max-height: 260px; overflow-y: auto;
1545    padding: 0.4rem 0;
1546    scrollbar-width: thin;
1547    scrollbar-color: rgba(255,109,53,0.3) transparent;
1548  }
1549  .prov-list::-webkit-scrollbar { width: 4px; }
1550  .prov-list::-webkit-scrollbar-thumb { background: rgba(255,109,53,0.35); border-radius: 4px; }
1551
1552  /* Group label */
1553  .prov-group-label {
1554    padding: 0.45rem 0.9rem 0.25rem;
1555    font-size: 0.68rem; font-weight: 700;
1556    color: var(--text-tertiary);
1557    text-transform: uppercase; letter-spacing: 0.08em;
1558  }
1559
1560  /* Province item */
1561  .prov-item {
1562    display: flex; align-items: center; gap: 0.6rem;
1563    padding: 0.5rem 0.9rem;
1564    cursor: pointer;
1565    transition: background 0.12s;
1566    border-radius: 0;
1567  }
1568  .prov-item:hover:not(.prov-disabled) { background: rgba(255,109,53,0.12); }
1569  .prov-item.prov-active {
1570    background: rgba(255,109,53,0.15);
1571  }
1572  .prov-item.prov-active .prov-item-name {
1573    color: var(--accent-primary); font-weight: 700;
1574  }
1575  .prov-item.prov-disabled {
1576    cursor: default; opacity: 0.55;
1577  }
1578  .prov-item-name { flex: 1; font-size: 0.875rem; color: var(--text-primary); }
1579  .prov-item-sparse {
1580    font-size: 0.65rem; font-weight: 700; margin-right: 6px;
1581    color: var(--text-secondary, #aaa); padding: 2px 7px; border-radius: 20px;
1582    border: 1px dashed currentColor;
1583  }
1584  .prov-item-badge {
บรรทัด 1247–1253: ส่วนหัวของโครงใหม่ ชื่อแบรนด์ และการปรับ topbar
บรรทัด 1254–1350: พื้นหลังของธีม ภาพหัวเรื่อง .hero-bg .hero-overlay .hero-content ป้าย .hero-label (ภาพถูกเปลี่ยนโดย ➜ setBanner() ใน frontend/extras.js) และตัวห่อแผงวางแผน
บรรทัด 1351–1447: แผงวางแผน .planner-panel แถวบน เส้นคั่น กริดช่อง .pf-grid ป้าย ข้อความ hint และความสูงของตัวควบคุมให้เท่ากัน รวมถึงการ์ดโรงแรมและปุ่มค้นหา
บรรทัด 1448–1478: พื้นหลังของส่วนแพ็กเกจและรายละเอียด
บรรทัด 1479–1584: เมนูจังหวัดแบบเลื่อน: กล่อง .prov-select .prov-dropdown (เปิดขึ้นหรือลงด้วยคลาส drop-up และอนิเมชัน provPop) ช่องค้นหา รายการ .prov-list ป้ายภาค และรายการจังหวัด .prov-item (ทำงานร่วมกับสคริปต์ท้าย ➜ frontend/index.html)
บรรทัด 1585–1647  พิมพ์ แผนทางเลือก และความชอบ
1585    font-size: 0.65rem; font-weight: 700;
1586    background: rgba(255,109,53,0.18);
1587    color: var(--accent-primary);
1588    padding: 2px 7px; border-radius: 20px;
1589    border: 1px solid rgba(255,109,53,0.35);
1590  }
1591  /* ── Print / บันทึกเป็น PDF: แสดงเฉพาะรายละเอียดทริป (พื้นขาว ตัวดำ) ── */
1592  @media print {
1593    .bg-layers, .topbar, .landing-screen, .packages-section, .toast-container,
1594    .detail-actions button, .map-wrap, .day-toggles, .modal,
1595    .poi-actions, .day-add, .day-list .poi-item button { display: none !important; }
1596    html, body { background: #fff !important; color: #000 !important; }
1597    .detail-section { display: block !important; padding: 0 !important; background: #fff !important; }
1598    .detail-grid { display: block !important; }
1599    .day-list { max-height: none !important; overflow: visible !important; }
1600    .day-panel { break-inside: avoid; border: 1px solid #999 !important; background: #fff !important; box-shadow: none !important; margin-bottom: 0.8rem; }
1601    .detail-section * { color: #000 !important; text-shadow: none !important; background: transparent !important; box-shadow: none !important; }
1602    .detail-section .kpi, .detail-section .dist-badge { border: 1px solid #999 !important; }
1603    .detail-section .day-color { background: #666 !important; }
1604  }
1605
1606  /* ── Pareto modal ── */
1607  .pareto-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
1608  .pareto-table th, .pareto-table td { padding: 0.45rem 0.6rem; text-align: right; border-bottom: 1px solid var(--border-subtle); }
1609  .pareto-table th:first-child, .pareto-table td:first-child { text-align: center; }
1610  .pareto-table th { color: var(--text-muted); font-weight: 600; font-size: 0.75rem; }
1611  .pareto-use { background: var(--grad-cta, #ff6d35); color: #fff; border: 0; border-radius: 8px; padding: 0.25rem 0.7rem; cursor: pointer; font-size: 0.8rem; white-space: nowrap; }
1612  @media (max-width: 720px) { .pareto-table th, .pareto-table td { padding: 0.4rem 0.3rem; } .pareto-use { padding: 0.25rem 0.5rem; font-size: 0.75rem; } }
1613
1614  /* ── Preferences (ความชอบ) ── */
1615  .pref-toggle {
1616    background: var(--grad-cta, linear-gradient(135deg, #ff7a3d, #e8561f)); border: 0;
1617    color: #fff; border-radius: 999px; padding: 0.4rem 1.1rem;
1618    font-size: 0.85rem; font-weight: 700; cursor: pointer;
1619    box-shadow: 0 4px 14px rgba(255,109,53,0.35); transition: transform .15s, box-shadow .15s;
1620  }
1621  .pref-toggle:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(255,109,53,0.5); }
1622  .pref-toggle[aria-expanded="true"] { box-shadow: 0 0 0 3px rgba(255,109,53,0.3); }
1623  .pref-summary { color: #fff; font-weight: 700; opacity: .9; }
1624  .pref-panel { margin: -0.4rem 0 0.9rem; padding: 0.6rem 0.8rem; display: grid; gap: 0.5rem; border: 1px solid var(--border-subtle); border-radius: 12px; background: var(--bg-surface); }
1625  .pref-panel[hidden] { display: none; }
1626  .pref-row { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
1627  .pref-label { font-size: 0.8rem; color: var(--text-secondary); min-width: 5.5rem; }
1628  .pref-label small, .pref-note { color: var(--text-muted); font-size: 0.7rem; }
1629  .pref-chips { display: flex; gap: 0.4rem; flex-wrap: wrap; }
1630  .pref-chip {
1631    border: 1px solid var(--border-subtle); background: var(--bg-surface); color: var(--text-secondary);
1632    border-radius: 999px; padding: 0.2rem 0.7rem; font-size: 0.8rem; cursor: pointer;
1633  }
1634  .pref-chip[data-state="like"]  { background: rgba(16,185,129,0.18); border-color: rgba(16,185,129,0.6); color: var(--text-primary); }
1635
1636  .pref-chip[data-state="avoid"] { background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.55); color: var(--text-primary); text-decoration: line-through; }
1637
1638  #prefDiet {
1639    appearance: none; -webkit-appearance: none; outline: none; cursor: pointer;
1640    background: var(--bg-surface) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E") no-repeat right 0.7rem center;
1641    color: var(--text-primary); border: 1px solid var(--border-subtle); border-radius: 999px;
1642    padding: 0.3rem 2rem 0.3rem 0.9rem; font-size: 0.82rem; transition: border-color .15s;
1643  }
1644  #prefDiet:hover, #prefDiet:focus { border-color: var(--accent-primary); }
1645  #prefDiet option { background: #2a211b; color: #fff; }
1646  .prov-item-soon {
1647    font-size: 0.65rem; font-weight: 600;
บรรทัด 1585–1604: @media print ซ่อนองค์ประกอบที่ไม่ต้องพิมพ์ (ปุ่ม แผนที่ โมดัล พื้นหลัง) และทำหน้ากระดาษพื้นขาว ใช้กับปุ่ม PDF ที่เรียก window.print()
บรรทัด 1605–1614: ตาราง .pareto-table และปุ่ม .pareto-use
บรรทัด 1615–1647: ปุ่มและแผงความชอบ .pref-toggle .pref-panel ชิป .pref-chips และช่องเลือกอาหาร #prefDiet
บรรทัด 1648–1819  ไอคอน มือถือ และฟีเจอร์เสริม
1648    color: var(--text-muted);
1649    padding: 2px 7px; border-radius: 20px;
1650    border: 1px solid var(--border-subtle);
1651  }
1652
1653
1654  /* ---- ไอคอนเส้นบางแทน emoji ---- */
1655  .ic { width: 1.1em; height: 1.1em; flex-shrink: 0; fill: none; stroke: currentColor; stroke-width: 1.7;
1656        stroke-linecap: round; stroke-linejoin: round; vertical-align: -0.2em; }
1657  .hotel-card-icon .ic { width: 22px; height: 22px; color: var(--accent-primary); }
1658  .map-hotel-marker .ic { width: 20px; height: 20px; color: #fff; }
1659  .dist-badge .ic { width: 0.95em; height: 0.95em; vertical-align: -0.12em; }
1660  .poi-name .ic { color: var(--accent-primary); margin-right: 2px; }
1661  .score-chip .ic { width: 0.95em; height: 0.95em; color: var(--accent-primary); fill: currentColor; stroke-width: 1.2; }
1662  .btn-icon .ic { width: 1em; height: 1em; }
1663  .export-btn .ic, .pref-toggle .ic { width: 1.05em; height: 1.05em; }
1664
1665  /* ---- ปุ่มการทำงานของแผน: โทนเดียวกับธีม (เส้นบาง ไม่มีสีน้ำเงิน/ฟ้า) ---- */
1666  .detail-actions { gap: 0.5rem; align-items: center; flex-wrap: wrap; }
1667  .reshuffle-btn {
1668    background: var(--bg-surface); border: 1px solid var(--border-default);
1669    border-radius: 999px; padding: 0.45rem 0.95rem; font-weight: 500; white-space: nowrap; color: var(--text-secondary);
1670  }
1671  .reshuffle-btn:hover { background: rgba(255,109,53,0.10); border-color: var(--accent-primary); color: var(--text-primary); }
1672  .reshuffle-btn .ic, .reshuffle-btn svg { width: 15px; height: 15px; stroke: var(--accent-primary); }
1673  .day-title h3 { white-space: nowrap; }
1674
1675  /* ---- มือถือ: ฟอร์มเรียงคอลัมน์เดียว ไม่ล้นจอ ---- */
1676  @media (max-width: 720px) {
1677    .planner-panel { zoom: 1; padding: 1.1rem 1rem 1rem; }
1678    .planner-top-row { flex-wrap: wrap; }
1679    .planner-title { flex-basis: 60%; }
1680    .pf-grid, .pf-grid-b, .dev-mode .pf-grid-b { grid-template-columns: 1fr; gap: 0.8rem; }
1681    .pf-col-search { min-width: 0; }
1682    .pf-col-search .cta-btn { width: 100%; justify-content: center; }
1683    .planner-panel .hotel-card { height: auto; min-height: 48px; }
1684    .hero-content h1 { font-size: clamp(1.7rem, 8vw, 2.4rem); line-height: 1.25; overflow-wrap: anywhere; }
1685  }
1686  @media (max-width: 720px) {
1687    .hero-h1 { white-space: normal; font-size: clamp(1.8rem, 9vw, 2.6rem); }
1688    .hero-desc { white-space: normal; font-size: 0.9rem; }
1689    .hero-content { padding: 0 1.2rem; }
1690    .hero-label { font-size: 0.8rem; margin-bottom: 1rem; }
1691    .planner-wrapper { padding: 330px 0.9rem 1rem; }
1692  }
1693
1694  /* ── รายละเอียดสถานที่ / รีวิวจำลอง ── */
1695  .poi-link { cursor: pointer; }
1696  .poi-link:hover { text-decoration: underline; text-underline-offset: 3px; }
1697  .poi-facts { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.6rem; margin-bottom: 0.8rem; }
1698  .poi-facts > div { border: 1px solid var(--border-subtle); border-radius: 12px; padding: 0.55rem 0.75rem; display: flex; flex-direction: column; gap: 0.15rem; }
1699  .poi-facts span { font-size: 0.75rem; color: var(--text-tertiary); }
1700  .poi-note { font-size: 0.78rem; color: var(--text-tertiary); margin: 0.6rem 0; line-height: 1.5; }
1701  .rev-head { display: flex; align-items: center; gap: 0.6rem; margin: 0.8rem 0 0.4rem; }
1702  .rev-score { display: inline-flex; align-items: center; gap: 0.25rem; font-weight: 700; font-size: 1.1rem; }
1703  .rev-count { font-size: 0.82rem; color: var(--text-tertiary); }
1704  .mock-chip { margin-left: auto; font-size: 0.7rem; padding: 0.15rem 0.55rem; border-radius: 999px; border: 1px dashed var(--border-default); color: var(--text-tertiary); }
1705  .rev-item { border-top: 1px solid var(--border-subtle); padding: 0.55rem 0; font-size: 0.88rem; line-height: 1.5; }
1706  .rev-stars { color: #f59e0b; letter-spacing: 1px; font-size: 0.85rem; }
1707
1708  /* ── ส่วนเสริม: จังหวัดข้างเคียง / ฤดูกาล / แผนที่บันทึก / เปรียบเทียบ ── */
1709  .neighbor-row { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-top: 8px; }
1710  .neighbor-label { font-size: 0.75rem; color: var(--text-secondary); }
1711  .neighbor-chip { font: inherit; font-size: 0.78rem; padding: 4px 12px; background: transparent; border: 1px solid rgba(255,109,53,0.4); border-radius: 20px; cursor: pointer; color: var(--text-primary); transition: background .15s, color .15s; }
1712  .neighbor-chip:hover { background: rgba(255,109,53,0.12); }
1713  .neighbor-chip.on { background: var(--grad-cta, #ff6d35); border-color: transparent; color: #fff; font-weight: 700; box-shadow: 0 2px 10px rgba(255,109,53,0.35); }
1714  .tips-card { height: 43px; box-sizing: border-box; display: flex; align-items: center; gap: 8px; padding: 0 12px; border-radius: 16px; background: rgba(255,109,53,0.08); border: 1px dashed rgba(255,109,53,0.45); overflow: hidden; }
1715  .tips-badge { flex-shrink: 0; font-size: 0.62rem; font-weight: 800; letter-spacing: .04em; color: #fff; background: var(--accent-primary); border-radius: 999px; padding: 2px 8px; }
1716  .tips-text { font-size: 0.8rem; line-height: 1.35; color: var(--text-primary); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; transition: opacity .4s; }
1717  .tips-text.fade { opacity: 0; }
1718  .dev-modal-card { max-width: 340px; }
1719  .dev-modal-card input { width: 100%; box-sizing: border-box; margin: 10px 0 6px; padding: 9px 14px; border-radius: 999px; border: 1px solid var(--border-subtle); background: var(--bg-surface); color: var(--text-primary); font-size: 1rem; text-align: center; }
1720  .dev-modal-card .dev-err { color: #f87171; font-size: 0.78rem; min-height: 1.1em; }
1721  .season-note { font-size: 0.75rem; color: var(--text-secondary); margin-top: 6px; line-height: 1.5; }
1722  .saved-row { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 10px 0; border-bottom: 1px solid rgba(128,128,128,0.2); }
1723  .saved-btn { font-size: 1.1rem; }
1724  .pareto-table tr.cmp-main td { font-weight: 700; color: var(--accent-primary); }
1725  @media (max-width: 640px) { .modal-body { overflow-x: auto; } .neighbor-row { gap: 4px; } }
1726
1727  /* ── ความชอบ: ชื่อหมวด + ปุ่มไอคอน 👍/👎 ด้านหลัง ── */
1728  .pref-cat { display: inline-flex; align-items: center; gap: 2px; padding: 3px 4px 3px 14px; border-radius: 999px; border: 1.5px solid var(--border-subtle); background: var(--bg-surface); transition: border-color .15s, background .15s, box-shadow .15s; }
1729  .pref-cat .pc-name { font-size: 0.85rem; color: var(--text-secondary); margin-right: 6px; transition: color .15s; }
1730  .pref-cat button { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border: 0; border-radius: 50%; background: none; color: var(--text-muted); cursor: pointer; transition: background .15s, color .15s, transform .15s; }
1731  .pref-cat button .ic { width: 1.05em; height: 1.05em; }
1732  .pref-cat .pc-dislike .ic { transform: scaleY(-1); }
1733  .pref-cat .pc-like:hover { background: rgba(34,197,94,0.2); color: #22c55e; transform: scale(1.12); }
1734  .pref-cat .pc-dislike:hover { background: rgba(239,68,68,0.2); color: #f87171; transform: scale(1.12); }
1735  .pref-cat[data-state="like"] { border-color: transparent; background: linear-gradient(135deg, #22c55e, #15803d); box-shadow: 0 3px 14px rgba(34,197,94,0.45); }
1736  .pref-cat[data-state="avoid"] { border-color: transparent; background: linear-gradient(135deg, #ef4444, #b91c1c); box-shadow: 0 3px 14px rgba(239,68,68,0.45); }
1737  .pref-cat[data-state="like"] .pc-name, .pref-cat[data-state="avoid"] .pc-name { color: #fff; font-weight: 700; }
1738  .pref-cat[data-state="like"] .pc-like, .pref-cat[data-state="avoid"] .pc-dislike { background: rgba(255,255,255,0.28); color: #fff; }
1739  .pref-cat[data-state="like"] .pc-dislike, .pref-cat[data-state="avoid"] .pc-like { color: rgba(255,255,255,0.55); }
1740
1741  /* ── dropdown อาหาร ── */
1742  .diet-wrap { position: relative; display: inline-block; }
1743  .diet-btn { font: inherit; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.6rem; min-width: 9rem; justify-content: space-between; padding: 0.38rem 0.95rem; color: var(--text-primary); background: var(--bg-surface); border: 1.5px solid var(--border-subtle); border-radius: 999px; cursor: pointer; transition: border-color .15s, box-shadow .15s; }
1744  .diet-btn:hover, .diet-btn.open { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(255,109,53,0.15); }
1745  .diet-btn svg { color: var(--accent-primary); transition: transform .18s; }
1746  .diet-btn.open svg { transform: rotate(180deg); }
1747  .diet-list { position: absolute; top: calc(100% + 6px); left: 0; min-width: 100%; z-index: 999; padding: 6px; background: var(--bg-elevated); border: 1.5px solid var(--border-subtle); border-radius: 18px; box-shadow: 0 16px 40px rgba(0,0,0,0.45); opacity: 0; transform: translateY(-6px); pointer-events: none; transition: opacity .16s, transform .16s; }
1748  .diet-list.open { opacity: 1; transform: none; pointer-events: auto; }
1749  .diet-item { padding: 0.4rem 0.9rem; border-radius: 12px; font-size: 0.85rem; cursor: pointer; color: var(--text-primary); white-space: nowrap; }
1750  .diet-item:hover { background: rgba(255,109,53,0.14); }
1751  .diet-item.on { background: rgba(255,109,53,0.2); color: var(--accent-primary); font-weight: 700; }
1752  [data-theme="light"] .diet-list { background: #fff; box-shadow: 0 16px 40px rgba(100,50,20,0.16); }
1753
1754  .dev-only { display: none !important; }
1755  .dev-mode .dev-only { display: inline-flex !important; }
1756
1757  .wx-chip { color: #7dd3fc; font-weight: 600; }
1758  .rain-banner { margin: 0 0 8px; padding: 8px 12px; border-radius: 12px; font-size: 0.8rem; background: rgba(56,189,248,0.12); border: 1px solid rgba(56,189,248,0.4); display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
1759  .rain-banner button { font: inherit; font-size: 0.78rem; padding: 3px 12px; border-radius: 999px; border: 0; background: #0ea5e9; color: #fff; cursor: pointer; }
1760
1761  .poi-item[draggable="true"] { cursor: grab; }
1762  .poi-item.dragging { opacity: .45; }
1763
1764  /* มือถือ: ปุ่มบนแถบบนเยอะขึ้น (ผลทดลอง/ภาษา/★/Dev/ธีม) — ย่อและตัดบรรทัดไม่ให้ล้นจอ */
1765  @media (max-width: 560px) {
1766    .topbar-actions { flex-wrap: wrap; justify-content: flex-end; gap: 4px; max-width: calc(100vw - 110px); flex-wrap: nowrap; }
1767    .topbar-actions .icon-btn { min-width: 30px; width: auto; height: 30px; padding: 0 .35rem; font-size: .72rem; }
1768    .topbar-actions .results-link { padding: 0 .45rem !important; display: inline-flex; align-items: center; }
1769  }
1770  @media (max-width: 560px) {
1771    .topbar .brand h1 { font-size: 1.1rem; }
1772    .topbar-actions .results-link { font-size: 0 !important; width: 30px !important; justify-content: center; padding: 0 !important; }
1773    .topbar-actions .results-link::before { content: "📊"; font-size: .85rem; }
1774  }
1775  .neighbor-row .neighbor-chip { color: var(--text-primary); }
1776  .neighbor-row .neighbor-chip.on { color: #fff; }
1777  [data-theme="light"] .pref-cat .pc-like, [data-theme="light"] .pref-cat .pc-dislike { color: #64748b; }
1778  [data-theme="light"] .pref-cat[data-state="like"] button, [data-theme="light"] .pref-cat[data-state="avoid"] button { color: rgba(255,255,255,.7); }
1779  [data-theme="light"] .pref-cat[data-state="like"] .pc-like, [data-theme="light"] .pref-cat[data-state="avoid"] .pc-dislike { color: #fff; }
1780
1781  .plan-warn{margin:10px 0;padding:10px 14px;border-radius:12px;border:1px solid rgba(234,179,8,.5);background:rgba(234,179,8,.12);font-size:.85rem}
1782  .plan-warn ul{margin:6px 0 0;padding-left:18px}
1783
1784  /* ซ่อนคะแนน/ตัวเลขภายในจากผู้ใช้ทั่วไป — แสดงเฉพาะโหมด Developer */
1785  body:not(.dev-mode) :is(.score-num, .dev-txt, .score-chip, #kpiScore, .runtime, .day-score) { display: none !important; }
1786
1787  /* ลากการ์ดแบบ real-time */
1788  .is-dragging .dist-connector { opacity: .45; }
1789  .dist-connector.drag-hide { display: none; }
1790  .poi-item.dragging { display: none; }
1791  .drop-gap { list-style: none; border: 2px dashed rgba(239,68,68,.55); background: rgba(239,68,68,.09); border-radius: 14px; margin: 4px 0; position: relative; }
1792  .drop-gap::before { content: ''; position: absolute; left: 10px; right: 10px; top: -5px; height: 3px; border-radius: 3px; background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,.7); }
1793  /* การ์ดที่ผิดข้อจำกัด: สีแดง + กล่องข้อความใต้การ์ด */
1794  .poi-item.poi-error { border-color: #ef4444 !important; background: rgba(239,68,68,.10) !important; box-shadow: 0 0 0 1px rgba(239,68,68,.4); }
1795  .poi-item.poi-error .poi-num { background: #ef4444 !important; color: #fff !important; }
1796  .poi-err-box { list-style: none; margin: -2px 0 6px; padding: 8px 12px; font-size: .8rem; line-height: 1.4; color: #b91c1c; background: rgba(239,68,68,.12); border: 1px solid rgba(239,68,68,.5); border-top: 0; border-radius: 0 0 12px 12px; }
1797  [data-theme="dark"] .poi-err-box { color: #fca5a5; }
1798  .plan-warn { margin: 6px 0 10px; padding: 8px 12px; font-size: .82rem; color: #92400e; background: rgba(245,158,11,.14); border: 1px solid rgba(245,158,11,.5); border-radius: 10px; }
1799  [data-theme="dark"] .plan-warn { color: #fcd34d; }
1800
1801  .hero-visual .hero-bg { transition: opacity .6s ease, transform 8s ease; }
1802
1803  /* ทางเลือกอื่นของทริป (การ์ด) */
1804  .pc-wrap, .pc-wrap-in { display: grid; gap: 12px; }
1805  .pc { border: 1px solid var(--border-subtle); border-radius: 16px; padding: 14px 16px; background: var(--bg-surface); }
1806  .pc-main { border-color: var(--accent-primary); box-shadow: 0 0 0 1px var(--accent-primary) inset; }
1807  .pc-tag { display: inline-block; font-size: .75rem; font-weight: 700; padding: 3px 10px; margin-right: 6px; border-radius: 999px; background: rgba(255,109,53,.14); color: var(--accent-primary); }
1808  .pc-why { margin: 6px 0 10px; font-size: .88rem; color: var(--text-secondary, var(--text-muted)); }
1809  .pc-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
1810  .pc-metrics > div { display: flex; flex-direction: column; gap: 1px; }
1811  .pc-metrics small { color: var(--text-muted); font-size: .72rem; }
1812  .pc-metrics b { font-size: 1rem; }
1813  .pc-dots { letter-spacing: 2px; color: var(--accent-primary); font-size: .85rem !important; }
1814  .pc-good { color: #16a34a; font-size: .74rem; font-weight: 600; } .pc-bad { color: #dc2626; font-size: .74rem; font-weight: 600; } .pc-same { color: var(--text-muted); font-size: .74rem; }
1815  .pc-hi { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0; }
1816  .pc-hi span { font-size: .75rem; padding: 3px 9px; border-radius: 999px; background: var(--bg-elevated, rgba(127,127,127,.12)); color: var(--text-secondary, inherit); }
1817  .pc .pareto-use { width: 100%; padding: .5rem; font-size: .9rem; border-radius: 10px; }
1818  .pc-more { margin: 4px auto 0; background: none; border: 1px dashed var(--border-subtle); color: var(--text-muted); border-radius: 999px; padding: .4rem 1rem; cursor: pointer; }
1819  @media (max-width: 560px) { .pc-metrics { grid-template-columns: 1fr 1fr; } }
บรรทัด 1648–1670: ไอคอนเส้นบาง .ic และปุ่มปฏิบัติการของแผน
บรรทัด 1671–1691: @media (max-width: 720px) ฟอร์มเรียงคอลัมน์เดียว
บรรทัด 1692–1705: ลิงก์ชื่อสถานที่และหน้าต่างรายละเอียดสถานที่ (.poi-facts, รีวิว) ของ ➜ showPoiDetail() ใน frontend/app.js
บรรทัด 1706–1721: ชิปจังหวัดข้างเคียง .neighbor-chip กล่อง Tips .tips-text และหมายเหตุฤดูกาล .season-note ที่ ➜ frontend/extras.js สร้าง
บรรทัด 1722–1750: ปรับโมดัลบนจอแคบ ชิปความชอบ .pref-cat (สถานะ like/avoid) และตัวเลือกอาหารที่แทน select (.diet-btn .diet-item)
บรรทัด 1751–1778: .dev-only ซ่อนองค์ประกอบสำหรับโหมด Developer (เปิดด้วยคลาส dev-mode ที่ ➜ setDevMode() ใน frontend/app.js) แถบเตือนฝน .rain-banner และเป้าหมายการลาก .drop-over
บรรทัด 1779–1804: กล่องคำเตือนของแผน .plan-warn การ์ดที่ผิดเวลา .poi-error และซ่อนเส้นเชื่อมระหว่างลาก
บรรทัด 1805–1819: การ์ดแผนทางเลือก .pc .pc-metrics .pc-dots ที่ ➜ renderParetoCards() ใน frontend/app.js สร้าง
บรรทัด 1820–1872  วิธีใช้ ลากการ์ด และ tooltip
1820
1821  /* Tutorial */
1822  .tut { position: fixed; inset: 0; z-index: 3000; }
1823  .tut-spot { position: fixed; border-radius: 14px; box-shadow: 0 0 0 9999px rgba(0,0,0,.62); transition: all .25s ease; pointer-events: none; outline: 2px solid var(--accent-primary); }
1824  .tut-card { position: fixed; background: var(--bg-surface, #fff); color: var(--text-primary); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 16px 18px; box-shadow: 0 18px 50px rgba(0,0,0,.35); max-width: 340px; }
1825  .tut-card.center { top: 50%; left: 50%; transform: translate(-50%, -50%); width: min(360px, calc(100vw - 24px)); }
1826  .tut-title { font-weight: 800; font-size: 1.05rem; margin-bottom: 6px; }
1827  .tut-text { font-size: .9rem; line-height: 1.55; color: var(--text-secondary, var(--text-muted)); }
1828  .tut-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 14px; gap: 10px; }
1829  .tut-dots i { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: var(--border-subtle); margin-right: 5px; }
1830  .tut-dots i.on { background: var(--accent-primary); }
1831  .tut-btns { display: flex; gap: 6px; }
1832  .tut-btns button { border: 0; border-radius: 999px; padding: .4rem .9rem; cursor: pointer; font: inherit; font-size: .82rem; background: var(--bg-elevated, rgba(127,127,127,.15)); color: var(--text-primary); }
1833  .tut-btns .tut-next { background: var(--accent-primary); color: #fff; font-weight: 700; }
1834  .tut-btns .tut-skip { background: none; color: var(--text-muted); }
1835  .tut.dim { background: rgba(0,0,0,.6); }
1836
1837  .pc-dots { display: flex; gap: 5px; align-items: center; height: 1.4rem; }
1838  .pc-dots i { width: 11px; height: 11px; border-radius: 50%; border: 2px solid var(--accent-primary); box-sizing: border-box; }
1839  .pc-dots i.on { background: var(--accent-primary); }
1840  .drop-gap::after { content: ''; position: absolute; left: 10px; right: 10px; bottom: -5px; height: 3px; border-radius: 3px; background: #ef4444; box-shadow: 0 0 6px rgba(239,68,68,.7); }
1841  .is-dragging .poi-err-box { display: none; }
1842
1843  /* marker ตอนลากการ์ด: บางลง ปลายซ้าย-ขวาจาง กลางเข้ม */
1844  .drop-gap::before, .drop-gap::after { left: 0 !important; right: 0 !important; height: 2px !important; border-radius: 2px;
1845    background: linear-gradient(90deg, rgba(239,68,68,0) 0%, #ef4444 28%, #ef4444 72%, rgba(239,68,68,0) 100%) !important; box-shadow: 0 0 4px rgba(239,68,68,.45) !important; }
1846  .drop-gap::before { top: -4px !important; } .drop-gap::after { bottom: -4px !important; }
1847  .rain-ic { display: inline-flex; vertical-align: -3px; margin-left: 6px; color: #0ea5e9; cursor: help; }
1848
1849  .planner-panel .hotel-card { width: max-content; max-width: 100%; }
1850  .planner-panel .hotel-card-body { flex: none; }
1851  .planner-panel .hotel-card-switch { margin-left: 0.5rem; }
1852  @media (max-width: 720px) { .planner-panel .hotel-card { width: 100%; } .planner-panel .hotel-card-body { flex: 1; } }
1853
1854  /* tutorial: ซ่อนการ์ดจนกว่าจะวางตำแหน่ง, ไม่ทำ transition บนเงาขนาดใหญ่ (ลด lag) */
1855  .tut:not(.ready) .tut-card { visibility: hidden; }
1856  .tut-spot { transition: none !important; will-change: top, left, width, height; }
1857  /* tooltip แบบ minimal แทนกล่องดำของเบราว์เซอร์ */
1858  .wet-tip { position: fixed; z-index: 4000; max-width: 260px; padding: 6px 11px; border-radius: 10px; font-size: .78rem; line-height: 1.4; pointer-events: none;
1859    background: var(--bg-surface, #fff); color: var(--text-primary, #111); border: 1px solid var(--border-default, rgba(127,127,127,.3)); box-shadow: 0 6px 22px rgba(0,0,0,.18); opacity: 0; transform: translateY(3px); transition: opacity .12s, transform .12s; }
1860  .wet-tip.show { opacity: 1; transform: none; }
1861  /* คืนอนิเมชันของ tutorial (เลื่อนไลต์ไปยังเป้าหมายอย่างนุ่มนวล) โดยทำ transition เฉพาะตำแหน่ง/ขนาด */
1862  .tut-spot { transition: top .25s ease, left .25s ease, width .25s ease, height .25s ease !important; }
1863  /* ที่พักยาวขึ้น Tips สั้นลง */
1864  .pf-grid-b { grid-template-columns: 1fr 1fr auto; }
1865  .planner-panel .hotel-card { width: 100%; justify-content: flex-start; }
1866  /* ที่พักกว้าง ~42% ของแถว สวิตช์ชิดขวา, Tips ยาวขึ้น */
1867  .pf-grid-b { grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr) auto; }
1868  .planner-panel .hotel-card { justify-content: space-between; }
1869  .planner-panel .hotel-card-body { flex: 1; }
1870  .planner-panel .hotel-card-switch { margin-left: auto; }
1871  .drop-gap { margin: 6px 0; }
1872
บรรทัด 1820–1841: สไตล์ของ tutorial: .tut .tut-spot .tut-card ปุ่มและจุดบอกขั้น ที่ ➜ frontend/tutorial.js สร้าง
บรรทัด 1842–1852: ตัวบอกตำแหน่งตอนลากการ์ด .drop-gap (ช่องว่างสีแดงจาง) และการปรับการ์ดโรงแรมบนจอแคบ
บรรทัด 1853–1855: ซ่อนการ์ด tutorial จนกว่าจะจัดตำแหน่งเสร็จ
บรรทัด 1856–1872: กล่อง .wet-tip ที่ ➜ frontend/tooltip.js ใช้แทนกล่องข้อความของเบราว์เซอร์
บรรทัด 1873–1947  จัดขนาดพอดีจอ ประวัติ และการแจ้งเตือน
1873  @media (min-width: 1001px) { .detail-section { box-sizing: border-box; padding-bottom: 2.25rem; } }
1874
1875  /* ย่อการ์ดให้เห็นครบ 6 จุด + ปุ่มเพิ่มสถานที่ (ค่า --sp ระยะห่าง, --fs ตัวอักษร ตั้งจาก fitDetail) */
1876  .day-list.fit { --sp: 1; --fs: 1; }
1877  .day-list.fit .day-panel { padding: calc(0.6rem + 0.65rem * var(--sp)) 1.1rem; margin-bottom: calc(0.5rem + 0.5rem * var(--sp)); }
1878  .day-list.fit .day-head { margin-bottom: calc(0.3rem + 0.45rem * var(--sp)); padding-bottom: calc(0.3rem + 0.45rem * var(--sp)); }
1879  .day-list.fit .poi-item { padding: calc(0.3rem + 0.32rem * var(--sp)) 0.5rem; }
1880  .day-list.fit .poi-num { width: calc(24px + 4px * var(--sp)); height: calc(24px + 4px * var(--sp)); }
1881  .day-list.fit .poi-name { font-size: calc(0.95rem * var(--fs)); }
1882  .day-list.fit .poi-meta { font-size: calc(0.75rem * var(--fs)); margin-top: calc(0.15rem * var(--sp)); }
1883  .day-list.fit .poi-actions button, .day-list.fit .poi-actions a.btn-loc { width: calc(28px + 4px * var(--sp)); height: calc(28px + 4px * var(--sp)); }
1884  .day-list.fit .rain-banner, .day-list.fit .plan-warn { padding: 5px 12px; margin-bottom: calc(3px + 5px * var(--sp)); }
1885  .day-list.fit .dist-connector { height: 0; padding: 0 0.5rem; margin: 0; position: relative; overflow: visible; z-index: 2; }
1886  .day-list.fit .dist-badge { background: var(--bg-surface); }
1887  .day-list.fit .day-add { margin-top: calc(0.2rem + 0.3rem * var(--sp)); padding: calc(0.3rem + 0.25rem * var(--sp)) 0.75rem; }
1888  /* ฟอนต์การ์ดเล็กลงอีก + ช่องไฟระหว่างข้อความการ์ดกับป้ายระยะทางมากขึ้น */
1889  .day-list.fit .poi-name { font-size: calc(0.86rem * var(--fs)); }
1890  .day-list.fit .poi-meta { font-size: calc(0.68rem * var(--fs)); }
1891  .day-list.fit .poi-item { padding: calc(0.42rem + 0.3rem * var(--sp)) 0.5rem; }
1892  .day-list.fit .dist-badge { font-size: calc(0.64rem * var(--fs)); }
1893
1894  /* กล่องเตือนฝนเล็กลง เพื่อให้พื้นที่กับการ์ด */
1895  .day-list.fit .rain-banner { padding: 3px 10px; font-size: 0.72rem; gap: 6px; margin-bottom: calc(2px + 3px * var(--sp)); border-radius: 10px; }
1896  .day-list.fit .rain-banner button { font-size: 0.68rem; padding: 1px 10px; }
1897  /* กล่องฝน: เว้นระยะใต้กล่องให้เท่ากับด้านบน ไม่ชิดป้ายระยะทางแรก */
1898  .day-list.fit .rain-banner { margin-bottom: 4px; }
1899  .day-list.fit .poi-list { padding-top: 18px; }
1900  /* ไอคอนโรงแรมในป้ายระยะทาง: ใหญ่ขึ้นและใช้สีส้มของธีม */
1901  .dist-badge .ic:has(use[href="#i-hotel"]) { width: 1.7em; height: 1.7em; vertical-align: -0.4em; color: var(--accent-primary); stroke-width: 2.2; }
1902  .dist-badge .ic:has(use[href="#i-arrow-right"]) { width: 1.1em; height: 1.1em; }
1903  /* ชื่อสถานที่: พื้นที่คลิก/hover เท่าความยาวชื่อเท่านั้น ส่วนที่เหลือของการ์ดใช้สำหรับลาก */
1904  .poi-item .poi-name { width: fit-content; max-width: 100%; }
1905
1906  /* หน้าเปลี่ยนสถานที่: ปุ่มรีวิว / Google Maps ด้านขวา */
1907  .swap-option .opt-actions { display: flex; gap: 8px; margin-left: 12px; flex-shrink: 0; }
1908  .opt-btn { display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; padding: 0; border-radius: 9px; background: #fff; color: #475569;
1909    border: 1px solid rgba(127,127,127,.3); cursor: pointer; text-decoration: none; transition: box-shadow .15s, transform .15s, color .15s, border-color .15s; }
1910  .opt-btn .ic { width: 15px; height: 15px; }
1911  .opt-btn:hover { color: var(--accent-primary); border-color: var(--accent-primary); box-shadow: 0 5px 16px rgba(0,0,0,.2); transform: translateY(-2px); }
1912
1913  /* ภาพการ์ดที่กำลังลาก: คมชัด ย่อลงเล็กน้อย ไม่มีแอนิเมชัน */
1914  .poi-item.drag-ghost { position: fixed !important; z-index: 3500; margin: 0 !important; pointer-events: none; opacity: 1 !important; filter: none !important; background: var(--bg-surface, #fff);
1915    box-shadow: 0 14px 34px rgba(0,0,0,.28), 0 0 0 2px rgba(255,109,53,.55); border-radius: 14px; transform: scale(.9);
1916    animation: none; transition: none !important; }
1917
1918  body.wet-dragging, body.wet-dragging * { user-select: none !important; cursor: grabbing !important; }
1919  .poi-item { cursor: grab; }
1920  .poi-item.drag-ghost { will-change: left, top; contain: layout; }
1921
1922  /* ปุ่มย้อนกลับ / เดินหน้า */
1923  .hist-group { display: inline-flex; gap: 6px; }
1924  .hist-btn { padding-left: .7rem; padding-right: .7rem; }
1925  .hist-btn .ic { width: 16px; height: 16px; }
1926  .hist-btn.disabled { opacity: .4; pointer-events: none; }
1927
1928  /* ── ปุ่มประวัติการแจ้งเตือน (ลอยมุมขวาล่าง) ── */
1929  .notif-btn { position: fixed; right: 24px; bottom: 24px; z-index: 900; width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;
1930    background: var(--bg-elevated, #fff); color: var(--text-primary); border: 1px solid var(--border-subtle); box-shadow: 0 6px 20px rgba(0,0,0,.25); transition: transform .15s ease, box-shadow .15s ease; }
1931  .notif-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 26px rgba(0,0,0,.3); border-color: var(--accent-primary); }
1932  .notif-btn svg { width: 22px; height: 22px; }
1933  .notif-badge { position: absolute; top: -3px; right: -3px; min-width: 18px; height: 18px; padding: 0 4px; border-radius: 9px; background: var(--accent-primary, #ff6d35); color: #fff; font-size: .68rem; font-weight: 700; line-height: 18px; text-align: center; }
1934  .notif-panel { position: fixed; right: 24px; bottom: 82px; z-index: 900; width: min(340px, calc(100vw - 32px)); max-height: 60vh; display: flex; flex-direction: column; overflow: hidden;
1935    background: var(--bg-elevated, #fff); backdrop-filter: blur(16px); color: var(--text-primary); border: 1px solid var(--border-subtle); border-radius: 16px; box-shadow: 0 18px 50px rgba(0,0,0,.35); }
1936  .notif-panel[hidden] { display: none; }
1937  .notif-head { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border-bottom: 1px solid var(--border-subtle); font-size: .9rem; }
1938  .notif-clear { background: none; border: 0; color: var(--text-muted); font-size: .78rem; cursor: pointer; }
1939  .notif-clear:hover { color: var(--accent-primary); }
1940  .notif-list { overflow-y: auto; padding: 6px 0; }
1941  .notif-item { display: flex; gap: 10px; padding: 9px 14px; font-size: .82rem; line-height: 1.4; }
1942  .notif-item + .notif-item { border-top: 1px solid var(--border-subtle); }
1943  .notif-dot { flex: none; width: 8px; height: 8px; margin-top: 6px; border-radius: 50%; background: #22c55e; }
1944  .notif-item.error .notif-dot { background: #ef4444; }
1945  .notif-time { margin-top: 2px; font-size: .7rem; color: var(--text-muted); }
1946  .notif-empty { padding: 22px 14px; text-align: center; font-size: .82rem; color: var(--text-muted); }
1947  @media print { .notif-btn, .notif-panel { display: none !important; } }
บรรทัด 1873–1900: ปรับความสูงและขนาดของส่วนรายละเอียดให้ตรงกับ ➜ fitDetail() ใน frontend/app.js ผ่านตัวแปร --sp (ระยะห่าง) และ --fs (ขนาดอักษร) ของ .day-list.fit
บรรทัด 1901–1918: รายละเอียดของไอคอนและปุ่มในรายการตัวเลือก
บรรทัด 1919–1935: ตัวผีขณะลาก .drag-ghost (ที่ ➜ enableDrag() ใน frontend/extras.js สร้าง) และปุ่มย้อนกลับ/เดินหน้า .hist-btn (➜ undoEdit() ใน frontend/app.js)
บรรทัด 1936–1947: ปุ่มกระดิ่งและแผงประวัติการแจ้งเตือน .notif-* ของ ➜ frontend/extras.js และซ่อนปุ่มเหล่านี้ตอนพิมพ์
บรรทัด 1948–1973  รองรับมือถือและจอสัมผัส
1948
1949  /* ── รองรับมือถือ / จอสัมผัส ── */
1950  @media (max-width: 1000px) {
1951    #map { height: min(62vh, 440px) !important; }
1952    .day-list { max-height: none !important; overflow: visible !important; }   /* จอแคบ: ไม่ใช้กรอบเลื่อนซ้อนในหน้า */
1953  }
1954  @media (max-width: 640px) {
1955    .icon-btn { width: 36px; height: 36px; }
1956    input, select, textarea { font-size: 16px !important; }   /* กัน iOS ซูมเองเมื่อแตะช่องกรอก */
1957    .neighbor-chip, .pref-toggle { min-height: 36px; }
1958    .day-head { flex-wrap: wrap; gap: 0.4rem; }
1959    .day-stats { flex-wrap: wrap; gap: 0.3rem 0.75rem; }
1960    .wx-chip { white-space: nowrap; }
1961    .poi-item { flex-wrap: wrap; row-gap: 0.2rem; }
1962    .poi-info { flex: 1 1 calc(100% - 44px); }
1963    .poi-actions { flex: 1 1 100%; justify-content: flex-end; gap: 0.5rem; }
1964    .poi-actions button, .poi-actions a.btn-loc { width: 44px; height: 40px; }
1965  }
1966  @media (pointer: coarse) {
1967    .poi-item { -webkit-touch-callout: none; -webkit-user-select: none; user-select: none; touch-action: pan-y; }
1968    .poi-actions button, .poi-actions a.btn-loc { min-width: 40px; min-height: 36px; }
1969  }
1970  @media (max-width: 640px) { .swap-option { margin-left: 0; } }
1971  @media (max-width: 720px) {   /* กฎ pf-grid-b ด้านบนมาทีหลังกฎจอแคบ จึงต้องทับซ้ำ */
1972    .pf-grid, .pf-grid-b, .dev-mode .pf-grid-b { grid-template-columns: 1fr !important; }
1973  }
บรรทัด 1948–1953: คอมเมนต์หัวส่วน และกฎสำหรับจอกว้างไม่เกิน 1000 พิกเซล: แผนที่สูง 62% ของความสูงจอแต่ไม่เกิน 440 พิกเซล (ใช้ !important เพราะ syncMapHeight ใน ➜ frontend/app.js ตั้งความสูงเป็นสไตล์ในบรรทัด) และ .day-list ไม่ใช้กรอบเลื่อนซ้อนในหน้า
บรรทัด 1954–1965: จอกว้างไม่เกิน 640 พิกเซล: ปุ่มไอคอนบนแถบบนใหญ่ขึ้น ช่องกรอกใช้อักษร 16 พิกเซลกัน iOS ซูมเอง ปุ่มเลือกจังหวัดข้างเคียงและปุ่มความชอบสูงพอแตะ หัวของวันและตัวเลขสถิติขึ้นบรรทัดใหม่ได้ ชิปสภาพอากาศไม่ตัดบรรทัด และการ์ดสถานที่แยกปุ่มเป็นแถวใต้ชื่อพร้อมปุ่มขนาด 44x40 พิกเซล
บรรทัด 1966–1969: อุปกรณ์สัมผัส (pointer: coarse): ปิดเมนูแตะค้างและการเลือกข้อความบนการ์ดเพื่อให้กดค้างแล้วลากได้ (➜ enableDrag() ใน frontend/extras.js) และตั้ง touch-action: pan-y ให้ปัดขึ้นลงเลื่อนหน้าได้ปกติ
บรรทัด 1970: จอแคบ: ตัวเลือกในหน้าต่างเปลี่ยนสถานที่ไม่เยื้องซ้าย
บรรทัด 1971–1973: จอกว้างไม่เกิน 720 พิกเซล: ทับกฎ .pf-grid-b (แถวที่พัก Tips ปุ่มค้นหา) ให้เป็นคอลัมน์เดียว เพราะกฎสามคอลัมน์ที่เขียนไว้ด้านบนอยู่หลังกฎจอแคบเดิมจึงทับกฎนั้น ทำให้ช่องที่พักแคบเกินไปบนมือถือ

ไฟล์ที่เชื่อมกับไฟล์นี้
frontend/app.js
frontend/extras.js
frontend/index.html
frontend/results.html
frontend/tooltip.js
frontend/tutorial.js