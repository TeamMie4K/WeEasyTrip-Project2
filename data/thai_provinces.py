# -*- coding: utf-8 -*-
"""รายชื่อ 77 จังหวัด (ไทย, อังกฤษ, slug, ภาค 6 ภาคตามราชบัณฑิตยสภา) ใช้สร้างทะเบียนจังหวัดและ dropdown"""
PROVINCES_77 = [
    # (slug, ชื่อไทย, ชื่ออังกฤษ, ภาค)
    # --- เหนือ ---
    ('chiangmai', 'เชียงใหม่', 'Chiang Mai', 'ภาคเหนือ'), ('chiangrai', 'เชียงราย', 'Chiang Rai', 'ภาคเหนือ'),
    ('maehongson', 'แม่ฮ่องสอน', 'Mae Hong Son', 'ภาคเหนือ'), ('nan', 'น่าน', 'Nan', 'ภาคเหนือ'),
    ('phayao', 'พะเยา', 'Phayao', 'ภาคเหนือ'), ('phrae', 'แพร่', 'Phrae', 'ภาคเหนือ'),
    ('lampang', 'ลำปาง', 'Lampang', 'ภาคเหนือ'), ('lamphun', 'ลำพูน', 'Lamphun', 'ภาคเหนือ'),
    ('uttaradit', 'อุตรดิตถ์', 'Uttaradit', 'ภาคเหนือ'),
    # --- ตะวันออกเฉียงเหนือ ---
    ('kalasin', 'กาฬสินธุ์', 'Kalasin', 'ภาคตะวันออกเฉียงเหนือ'), ('khonkaen', 'ขอนแก่น', 'Khon Kaen', 'ภาคตะวันออกเฉียงเหนือ'),
    ('chaiyaphum', 'ชัยภูมิ', 'Chaiyaphum', 'ภาคตะวันออกเฉียงเหนือ'), ('nakhonphanom', 'นครพนม', 'Nakhon Phanom', 'ภาคตะวันออกเฉียงเหนือ'),
    ('nakhonratchasima', 'นครราชสีมา', 'Nakhon Ratchasima', 'ภาคตะวันออกเฉียงเหนือ'), ('buengkan', 'บึงกาฬ', 'Bueng Kan', 'ภาคตะวันออกเฉียงเหนือ'),
    ('buriram', 'บุรีรัมย์', 'Buri Ram', 'ภาคตะวันออกเฉียงเหนือ'), ('mahasarakham', 'มหาสารคาม', 'Maha Sarakham', 'ภาคตะวันออกเฉียงเหนือ'),
    ('mukdahan', 'มุกดาหาร', 'Mukdahan', 'ภาคตะวันออกเฉียงเหนือ'), ('yasothon', 'ยโสธร', 'Yasothon', 'ภาคตะวันออกเฉียงเหนือ'),
    ('roiet', 'ร้อยเอ็ด', 'Roi Et', 'ภาคตะวันออกเฉียงเหนือ'), ('loei', 'เลย', 'Loei', 'ภาคตะวันออกเฉียงเหนือ'),
    ('sisaket', 'ศรีสะเกษ', 'Si Sa Ket', 'ภาคตะวันออกเฉียงเหนือ'), ('sakonnakhon', 'สกลนคร', 'Sakon Nakhon', 'ภาคตะวันออกเฉียงเหนือ'),
    ('surin', 'สุรินทร์', 'Surin', 'ภาคตะวันออกเฉียงเหนือ'), ('nongkhai', 'หนองคาย', 'Nong Khai', 'ภาคตะวันออกเฉียงเหนือ'),
    ('nongbualamphu', 'หนองบัวลำภู', 'Nong Bua Lam Phu', 'ภาคตะวันออกเฉียงเหนือ'), ('udonthani', 'อุดรธานี', 'Udon Thani', 'ภาคตะวันออกเฉียงเหนือ'),
    ('ubonratchathani', 'อุบลราชธานี', 'Ubon Ratchathani', 'ภาคตะวันออกเฉียงเหนือ'), ('amnatcharoen', 'อำนาจเจริญ', 'Amnat Charoen', 'ภาคตะวันออกเฉียงเหนือ'),
    # --- กลาง ---
    ('bangkok', 'กรุงเทพมหานคร', 'Bangkok', 'ภาคกลาง'), ('kamphaengphet', 'กำแพงเพชร', 'Kamphaeng Phet', 'ภาคกลาง'),
    ('chainat', 'ชัยนาท', 'Chai Nat', 'ภาคกลาง'), ('nakhonnayok', 'นครนายก', 'Nakhon Nayok', 'ภาคกลาง'),
    ('nakhonpathom', 'นครปฐม', 'Nakhon Pathom', 'ภาคกลาง'), ('nakhonsawan', 'นครสวรรค์', 'Nakhon Sawan', 'ภาคกลาง'),
    ('nonthaburi', 'นนทบุรี', 'Nonthaburi', 'ภาคกลาง'), ('pathumthani', 'ปทุมธานี', 'Pathum Thani', 'ภาคกลาง'),
    ('ayutthaya', 'พระนครศรีอยุธยา', 'Phra Nakhon Si Ayutthaya', 'ภาคกลาง'), ('phichit', 'พิจิตร', 'Phichit', 'ภาคกลาง'),
    ('phitsanulok', 'พิษณุโลก', 'Phitsanulok', 'ภาคกลาง'), ('phetchabun', 'เพชรบูรณ์', 'Phetchabun', 'ภาคกลาง'),
    ('lopburi', 'ลพบุรี', 'Lop Buri', 'ภาคกลาง'), ('samutprakan', 'สมุทรปราการ', 'Samut Prakan', 'ภาคกลาง'),
    ('samutsongkhram', 'สมุทรสงคราม', 'Samut Songkhram', 'ภาคกลาง'), ('samutsakhon', 'สมุทรสาคร', 'Samut Sakhon', 'ภาคกลาง'),
    ('singburi', 'สิงห์บุรี', 'Sing Buri', 'ภาคกลาง'), ('sukhothai', 'สุโขทัย', 'Sukhothai', 'ภาคกลาง'),
    ('suphanburi', 'สุพรรณบุรี', 'Suphan Buri', 'ภาคกลาง'), ('saraburi', 'สระบุรี', 'Saraburi', 'ภาคกลาง'),
    ('angthong', 'อ่างทอง', 'Ang Thong', 'ภาคกลาง'), ('uthaithani', 'อุทัยธานี', 'Uthai Thani', 'ภาคกลาง'),
    # --- ตะวันออก ---
    ('chanthaburi', 'จันทบุรี', 'Chanthaburi', 'ภาคตะวันออก'), ('chachoengsao', 'ฉะเชิงเทรา', 'Chachoengsao', 'ภาคตะวันออก'),
    ('chonburi', 'ชลบุรี', 'Chon Buri', 'ภาคตะวันออก'), ('prachinburi', 'ปราจีนบุรี', 'Prachin Buri', 'ภาคตะวันออก'),
    ('rayong', 'ระยอง', 'Rayong', 'ภาคตะวันออก'), ('sakaeo', 'สระแก้ว', 'Sa Kaeo', 'ภาคตะวันออก'),
    ('trat', 'ตราด', 'Trat', 'ภาคตะวันออก'),
    # --- ตะวันตก ---
    ('kanchanaburi', 'กาญจนบุรี', 'Kanchanaburi', 'ภาคตะวันตก'), ('tak', 'ตาก', 'Tak', 'ภาคตะวันตก'),
    ('prachuapkhirikhan', 'ประจวบคีรีขันธ์', 'Prachuap Khiri Khan', 'ภาคตะวันตก'), ('phetchaburi', 'เพชรบุรี', 'Phetchaburi', 'ภาคตะวันตก'),
    ('ratchaburi', 'ราชบุรี', 'Ratchaburi', 'ภาคตะวันตก'),
    # --- ใต้ ---
    ('krabi', 'กระบี่', 'Krabi', 'ภาคใต้'), ('chumphon', 'ชุมพร', 'Chumphon', 'ภาคใต้'), ('trang', 'ตรัง', 'Trang', 'ภาคใต้'),
    ('nakhonsithammarat', 'นครศรีธรรมราช', 'Nakhon Si Thammarat', 'ภาคใต้'), ('narathiwat', 'นราธิวาส', 'Narathiwat', 'ภาคใต้'),
    ('pattani', 'ปัตตานี', 'Pattani', 'ภาคใต้'), ('phangnga', 'พังงา', 'Phang Nga', 'ภาคใต้'), ('phatthalung', 'พัทลุง', 'Phatthalung', 'ภาคใต้'),
    ('phuket', 'ภูเก็ต', 'Phuket', 'ภาคใต้'), ('ranong', 'ระนอง', 'Ranong', 'ภาคใต้'), ('satun', 'สตูล', 'Satun', 'ภาคใต้'),
    ('songkhla', 'สงขลา', 'Songkhla', 'ภาคใต้'), ('suratthani', 'สุราษฎร์ธานี', 'Surat Thani', 'ภาคใต้'), ('yala', 'ยะลา', 'Yala', 'ภาคใต้'),
]
# เกาะสมุยเป็นพื้นที่ท่องเที่ยวย่อยของสุราษฎร์ธานี — เก็บเป็นรายการแยก (ทำไว้แล้ว) ไม่นับเป็นจังหวัดเพิ่ม
EXTRA_AREAS = {'samui': ('เกาะสมุย', 'Koh Samui', 'ภาคใต้', 'suratthani')}

# ลำดับความสำคัญในการดึงข้อมูล (แหล่งท่องเที่ยวยอดนิยมก่อน)
PRIORITY = ['bangkok', 'chonburi', 'prachuapkhirikhan', 'ayutthaya', 'kanchanaburi', 'phangnga', 'chiangrai', 'trat',
            'suratthani', 'nakhonratchasima', 'khonkaen', 'udonthani', 'phetchaburi', 'rayong', 'sukhothai', 'phitsanulok',
            'nakhonsithammarat', 'songkhla', 'trang', 'ubonratchathani', 'nan', 'maehongson', 'loei', 'lampang', 'chanthaburi']

assert len(PROVINCES_77) == 77 and len({p[0] for p in PROVINCES_77}) == 77
