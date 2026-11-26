<!-- converted from data__thai_provinces.py.docx -->

คู่มือโค้ด: data/thai_provinces.py
ทะเบียนรายชื่อ 77 จังหวัด
ไฟล์ต้นฉบับ: data/thai_provinces.py (58 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: ไฟล์ข้อมูลล้วน ๆ เก็บรายชื่อจังหวัดไทย 77 จังหวัด (slug ชื่อไทย ชื่ออังกฤษ ภาค) ใช้โดย ➜ backend/main.py เพื่อแสดงรายการจังหวัดที่ยังไม่พร้อม และใช้โดยท่อสร้างข้อมูล ➜ data/build_all_provinces.py และ ➜ data/fetch_pois_osm.py เพื่อรู้ว่าต้องสร้างจังหวัดใดบ้าง

บรรทัด 1–3  หัวไฟล์และตัวแปรหลัก
1  # -*- coding: utf-8 -*-
2  """รายชื่อ 77 จังหวัด (ไทย, อังกฤษ, slug, ภาค 6 ภาคตามราชบัณฑิตยสภา) ใช้สร้างทะเบียนจังหวัดและ dropdown"""
3  PROVINCES_77 = [
บรรทัด 1–2: docstring อธิบายว่าเป็นรายชื่อ 77 จังหวัด (ไทย อังกฤษ slug และ 6 ภาคตามราชบัณฑิตยสภา)
บรรทัด 3: เริ่มประกาศ PROVINCES_77 เป็นลิสต์ของทูเพิล (slug, ชื่อไทย, ชื่ออังกฤษ, ภาค)
บรรทัด 4–49  รายการจังหวัดแยกตามภาค
4      # (slug, ชื่อไทย, ชื่ออังกฤษ, ภาค)
5      # --- เหนือ ---
6      ('chiangmai', 'เชียงใหม่', 'Chiang Mai', 'ภาคเหนือ'), ('chiangrai', 'เชียงราย', 'Chiang Rai', 'ภาคเหนือ'),
7      ('maehongson', 'แม่ฮ่องสอน', 'Mae Hong Son', 'ภาคเหนือ'), ('nan', 'น่าน', 'Nan', 'ภาคเหนือ'),
8      ('phayao', 'พะเยา', 'Phayao', 'ภาคเหนือ'), ('phrae', 'แพร่', 'Phrae', 'ภาคเหนือ'),
9      ('lampang', 'ลำปาง', 'Lampang', 'ภาคเหนือ'), ('lamphun', 'ลำพูน', 'Lamphun', 'ภาคเหนือ'),
10      ('uttaradit', 'อุตรดิตถ์', 'Uttaradit', 'ภาคเหนือ'),
11      # --- ตะวันออกเฉียงเหนือ ---
12      ('kalasin', 'กาฬสินธุ์', 'Kalasin', 'ภาคตะวันออกเฉียงเหนือ'), ('khonkaen', 'ขอนแก่น', 'Khon Kaen', 'ภาคตะวันออกเฉียงเหนือ'),
13      ('chaiyaphum', 'ชัยภูมิ', 'Chaiyaphum', 'ภาคตะวันออกเฉียงเหนือ'), ('nakhonphanom', 'นครพนม', 'Nakhon Phanom', 'ภาคตะวันออกเฉียงเหนือ'),
14      ('nakhonratchasima', 'นครราชสีมา', 'Nakhon Ratchasima', 'ภาคตะวันออกเฉียงเหนือ'), ('buengkan', 'บึงกาฬ', 'Bueng Kan', 'ภาคตะวันออกเฉียงเหนือ'),
15      ('buriram', 'บุรีรัมย์', 'Buri Ram', 'ภาคตะวันออกเฉียงเหนือ'), ('mahasarakham', 'มหาสารคาม', 'Maha Sarakham', 'ภาคตะวันออกเฉียงเหนือ'),
16      ('mukdahan', 'มุกดาหาร', 'Mukdahan', 'ภาคตะวันออกเฉียงเหนือ'), ('yasothon', 'ยโสธร', 'Yasothon', 'ภาคตะวันออกเฉียงเหนือ'),
17      ('roiet', 'ร้อยเอ็ด', 'Roi Et', 'ภาคตะวันออกเฉียงเหนือ'), ('loei', 'เลย', 'Loei', 'ภาคตะวันออกเฉียงเหนือ'),
18      ('sisaket', 'ศรีสะเกษ', 'Si Sa Ket', 'ภาคตะวันออกเฉียงเหนือ'), ('sakonnakhon', 'สกลนคร', 'Sakon Nakhon', 'ภาคตะวันออกเฉียงเหนือ'),
19      ('surin', 'สุรินทร์', 'Surin', 'ภาคตะวันออกเฉียงเหนือ'), ('nongkhai', 'หนองคาย', 'Nong Khai', 'ภาคตะวันออกเฉียงเหนือ'),
20      ('nongbualamphu', 'หนองบัวลำภู', 'Nong Bua Lam Phu', 'ภาคตะวันออกเฉียงเหนือ'), ('udonthani', 'อุดรธานี', 'Udon Thani', 'ภาคตะวันออกเฉียงเหนือ'),
21      ('ubonratchathani', 'อุบลราชธานี', 'Ubon Ratchathani', 'ภาคตะวันออกเฉียงเหนือ'), ('amnatcharoen', 'อำนาจเจริญ', 'Amnat Charoen', 'ภาคตะวันออกเฉียงเหนือ'),
22      # --- กลาง ---
23      ('bangkok', 'กรุงเทพมหานคร', 'Bangkok', 'ภาคกลาง'), ('kamphaengphet', 'กำแพงเพชร', 'Kamphaeng Phet', 'ภาคกลาง'),
24      ('chainat', 'ชัยนาท', 'Chai Nat', 'ภาคกลาง'), ('nakhonnayok', 'นครนายก', 'Nakhon Nayok', 'ภาคกลาง'),
25      ('nakhonpathom', 'นครปฐม', 'Nakhon Pathom', 'ภาคกลาง'), ('nakhonsawan', 'นครสวรรค์', 'Nakhon Sawan', 'ภาคกลาง'),
26      ('nonthaburi', 'นนทบุรี', 'Nonthaburi', 'ภาคกลาง'), ('pathumthani', 'ปทุมธานี', 'Pathum Thani', 'ภาคกลาง'),
27      ('ayutthaya', 'พระนครศรีอยุธยา', 'Phra Nakhon Si Ayutthaya', 'ภาคกลาง'), ('phichit', 'พิจิตร', 'Phichit', 'ภาคกลาง'),
28      ('phitsanulok', 'พิษณุโลก', 'Phitsanulok', 'ภาคกลาง'), ('phetchabun', 'เพชรบูรณ์', 'Phetchabun', 'ภาคกลาง'),
29      ('lopburi', 'ลพบุรี', 'Lop Buri', 'ภาคกลาง'), ('samutprakan', 'สมุทรปราการ', 'Samut Prakan', 'ภาคกลาง'),
30      ('samutsongkhram', 'สมุทรสงคราม', 'Samut Songkhram', 'ภาคกลาง'), ('samutsakhon', 'สมุทรสาคร', 'Samut Sakhon', 'ภาคกลาง'),
31      ('singburi', 'สิงห์บุรี', 'Sing Buri', 'ภาคกลาง'), ('sukhothai', 'สุโขทัย', 'Sukhothai', 'ภาคกลาง'),
32      ('suphanburi', 'สุพรรณบุรี', 'Suphan Buri', 'ภาคกลาง'), ('saraburi', 'สระบุรี', 'Saraburi', 'ภาคกลาง'),
33      ('angthong', 'อ่างทอง', 'Ang Thong', 'ภาคกลาง'), ('uthaithani', 'อุทัยธานี', 'Uthai Thani', 'ภาคกลาง'),
34      # --- ตะวันออก ---
35      ('chanthaburi', 'จันทบุรี', 'Chanthaburi', 'ภาคตะวันออก'), ('chachoengsao', 'ฉะเชิงเทรา', 'Chachoengsao', 'ภาคตะวันออก'),
36      ('chonburi', 'ชลบุรี', 'Chon Buri', 'ภาคตะวันออก'), ('prachinburi', 'ปราจีนบุรี', 'Prachin Buri', 'ภาคตะวันออก'),
37      ('rayong', 'ระยอง', 'Rayong', 'ภาคตะวันออก'), ('sakaeo', 'สระแก้ว', 'Sa Kaeo', 'ภาคตะวันออก'),
38      ('trat', 'ตราด', 'Trat', 'ภาคตะวันออก'),
39      # --- ตะวันตก ---
40      ('kanchanaburi', 'กาญจนบุรี', 'Kanchanaburi', 'ภาคตะวันตก'), ('tak', 'ตาก', 'Tak', 'ภาคตะวันตก'),
41      ('prachuapkhirikhan', 'ประจวบคีรีขันธ์', 'Prachuap Khiri Khan', 'ภาคตะวันตก'), ('phetchaburi', 'เพชรบุรี', 'Phetchaburi', 'ภาคตะวันตก'),
42      ('ratchaburi', 'ราชบุรี', 'Ratchaburi', 'ภาคตะวันตก'),
43      # --- ใต้ ---
44      ('krabi', 'กระบี่', 'Krabi', 'ภาคใต้'), ('chumphon', 'ชุมพร', 'Chumphon', 'ภาคใต้'), ('trang', 'ตรัง', 'Trang', 'ภาคใต้'),
45      ('nakhonsithammarat', 'นครศรีธรรมราช', 'Nakhon Si Thammarat', 'ภาคใต้'), ('narathiwat', 'นราธิวาส', 'Narathiwat', 'ภาคใต้'),
46      ('pattani', 'ปัตตานี', 'Pattani', 'ภาคใต้'), ('phangnga', 'พังงา', 'Phang Nga', 'ภาคใต้'), ('phatthalung', 'พัทลุง', 'Phatthalung', 'ภาคใต้'),
47      ('phuket', 'ภูเก็ต', 'Phuket', 'ภาคใต้'), ('ranong', 'ระนอง', 'Ranong', 'ภาคใต้'), ('satun', 'สตูล', 'Satun', 'ภาคใต้'),
48      ('songkhla', 'สงขลา', 'Songkhla', 'ภาคใต้'), ('suratthani', 'สุราษฎร์ธานี', 'Surat Thani', 'ภาคใต้'), ('yala', 'ยะลา', 'Yala', 'ภาคใต้'),
49  ]
บรรทัด 4: คอมเมนต์บอกรูปแบบของทูเพิล
บรรทัด 5–10: จังหวัดภาคเหนือ 9 จังหวัด เริ่มจากเชียงใหม่
บรรทัด 11–21: จังหวัดภาคตะวันออกเฉียงเหนือ (อีสาน)
บรรทัด 22–33: จังหวัดภาคกลาง รวมกรุงเทพมหานคร
บรรทัด 34–38: จังหวัดภาคตะวันออก
บรรทัด 39–42: จังหวัดภาคตะวันตก
บรรทัด 43–48: จังหวัดภาคใต้
บรรทัด 49: ปิดลิสต์
บรรทัด 50–58  พื้นที่เสริม ลำดับความสำคัญ และการตรวจจำนวน
50  # เกาะสมุยเป็นพื้นที่ท่องเที่ยวย่อยของสุราษฎร์ธานี — เก็บเป็นรายการแยก (ทำไว้แล้ว) ไม่นับเป็นจังหวัดเพิ่ม
51  EXTRA_AREAS = {'samui': ('เกาะสมุย', 'Koh Samui', 'ภาคใต้', 'suratthani')}
52
53  # ลำดับความสำคัญในการดึงข้อมูล (แหล่งท่องเที่ยวยอดนิยมก่อน)
54  PRIORITY = ['bangkok', 'chonburi', 'prachuapkhirikhan', 'ayutthaya', 'kanchanaburi', 'phangnga', 'chiangrai', 'trat',
55              'suratthani', 'nakhonratchasima', 'khonkaen', 'udonthani', 'phetchaburi', 'rayong', 'sukhothai', 'phitsanulok',
56              'nakhonsithammarat', 'songkhla', 'trang', 'ubonratchathani', 'nan', 'maehongson', 'loei', 'lampang', 'chanthaburi']
57
58  assert len(PROVINCES_77) == 77 and len({p[0] for p in PROVINCES_77}) == 77
บรรทัด 50–51: EXTRA_AREAS พื้นที่ท่องเที่ยวย่อยที่ไม่ใช่จังหวัด คือเกาะสมุย (ของสุราษฎร์ธานี) เก็บแยกเพื่อให้ท่อสร้างข้อมูลและหน้าเว็บจัดการเป็นพื้นที่หนึ่งได้
บรรทัด 53–56: PRIORITY ลำดับการดึงข้อมูล (แหล่งท่องเที่ยวยอดนิยมก่อน) ใช้ใน ➜ data/build_all_provinces.py
บรรทัด 58: assert ตรวจว่ามี 77 รายการพอดีและ slug ไม่ซ้ำ ถ้าแก้ไฟล์แล้วผิดจะล้มทันทีตอนนำเข้า

ไฟล์ที่เชื่อมกับไฟล์นี้
backend/main.py
data/build_all_provinces.py
data/fetch_pois_osm.py