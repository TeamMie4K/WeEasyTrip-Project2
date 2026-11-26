<!-- converted from data__make_banners.py.docx -->

คู่มือโค้ด: data/make_banners.py
สร้างภาพแบนเนอร์ SVG ประจำจังหวัด
ไฟล์ต้นฉบับ: data/make_banners.py (114 บรรทัด)   ➜ กลับสารบัญคู่มือ
บทบาทของไฟล์: สคริปต์สร้างภาพวาดเชิงนามธรรมขนาด 1600×640 ของทุกจังหวัดเป็น SVG ไว้ที่ frontend/img/provinces/<slug>.svg ตามลักษณะพื้นที่ (เมือง วัด ชายฝั่ง ภูเขา หรือทุ่งนา) และสีตามภาค หน้าเว็บ (➜ frontend/app.js) ใช้ภาพนี้เป็นหัวการ์ดจังหวัด ถ้าวางไฟล์ <slug>.jpg ไว้ในโฟลเดอร์เดียวกัน หน้าเว็บจะใช้ภาพถ่ายแทน ใช้รายชื่อภาคจาก ➜ data/thai_provinces.py

บรรทัด 1–23  หัวไฟล์ ค่าคงที่ และจานสี
1  # -*- coding: utf-8 -*-
2  """สร้างภาพแบนเนอร์ SVG ประจำจังหวัด (ครบทุกจังหวัดใน provinces.json) -> frontend/img/provinces/<slug>.svg
3  ภาพเป็นภาพวาดเชิงนามธรรมตามลักษณะพื้นที่ (ทะเล/ภูเขา/ทุ่งนา/วัด/เมือง) สร้างจาก slug ให้ได้ผลเดิมทุกครั้ง ไม่ใช่ภาพถ่ายจริง
4  ถ้าต้องการภาพถ่ายจริง วางไฟล์ <slug>.jpg ไว้ในโฟลเดอร์เดียวกัน หน้าเว็บจะใช้ .jpg ก่อน .svg
5  รัน: python data/make_banners.py
6  """
7  import json, os, random
8
9  ROOT = os.path.join(os.path.dirname(__file__), '..')
10  OUT = os.path.join(ROOT, 'frontend', 'img', 'provinces')
11  W, H = 1600, 640
12  COAST = set('''phuket krabi samui suratthani phangnga ranong satun trang songkhla pattani narathiwat nakhonsithammarat chumphon
13  prachuapkhirikhan phetchaburi samutsongkhram samutsakhon samutprakan chonburi rayong chanthaburi trat chachoengsao bangkok'''.split())
14  CITY = set('bangkok nonthaburi pathumthani samutprakan'.split())
15  TEMPLE = set('ayutthaya sukhothai lopburi angthong singburi chainat suphanburi nakhonpathom saraburi kamphaengphet phitsanulok phichit uthaithani nakhonsawan'.split())
16  PAL = {   # (บนฟ้า, ล่างฟ้า, สีเงาไกล, สีเงาใกล้)
17      'ภาคเหนือ': ('#1f6f78', '#f6c98b', '#3b8a7e', '#164e4a'),
18      'ภาคตะวันออกเฉียงเหนือ': ('#c2410c', '#fcd88a', '#b4571f', '#7c2d12'),
19      'ภาคกลาง': ('#6d4aa6', '#f9b98a', '#8a5a9c', '#3f2a63'),
20      'ภาคตะวันออก': ('#0e7490', '#fbd38d', '#2b8ca1', '#134e63'),
21      'ภาคตะวันตก': ('#2f6b4f', '#f3d69a', '#4a8467', '#1d4535'),
22      'ภาคใต้': ('#0369a1', '#ffd9a0', '#2f86b8', '#0b4a70'),
23  }
บรรทัด 1–5: docstring อธิบายหน้าที่ ที่เก็บผล และวิธีรัน
บรรทัด 7: นำเข้า json os random
บรรทัด 9–11: ROOT ราก repo OUT โฟลเดอร์ปลายทาง และขนาดภาพ W, H
บรรทัด 12–13: COAST ชุดจังหวัดชายฝั่ง
บรรทัด 14: CITY ชุดจังหวัดเมือง (กรุงเทพฯ และปริมณฑล)
บรรทัด 15: TEMPLE ชุดจังหวัดมรดกทางวัฒนธรรม (วัดและเจดีย์)
บรรทัด 16–23: PAL จานสีของแต่ละภาค: สีบนฟ้า สีล่างฟ้า สีเงาไกล สีเงาใกล้
บรรทัด 26–34  วาดเส้นสันเขา
26  def ridge(rng, y, amp, steps, jag=1.0):
27      pts = [(0, y)]
28      for i in range(1, steps):
29          pts.append((W * i / steps, y - rng.random() * amp * jag))
30      pts.append((W, y))
31      d = f'M0,{H} L0,{y} '
32      for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
33          d += f'Q{x1:.0f},{y1:.0f} {(x1 + x2) / 2:.0f},{(y1 + y2) / 2:.0f} '
34      return d + f'L{W},{H} Z'
บรรทัด 26–34: ridge สร้างพาธ SVG ของสันเขา/เนินด้วยจุดสุ่ม (ความสูง amp และความขรุขระ jag) เชื่อมด้วยเส้นโค้ง Q แล้วปิดลงพื้นภาพ
บรรทัด 37–41  วาดเจดีย์
37  def chedi(x, base, h, fill):
38      w = h * 0.42
39      return (f'<path d="M{x - w / 2:.0f},{base} L{x - w / 2:.0f},{base - h * .18:.0f} L{x - w * .35:.0f},{base - h * .32:.0f} L{x - w * .22:.0f},{base - h * .5:.0f} '
40              f'L{x - w * .1:.0f},{base - h * .78:.0f} L{x:.0f},{base - h:.0f} L{x + w * .1:.0f},{base - h * .78:.0f} L{x + w * .22:.0f},{base - h * .5:.0f} '
41              f'L{x + w * .35:.0f},{base - h * .32:.0f} L{x + w / 2:.0f},{base - h * .18:.0f} L{x + w / 2:.0f},{base} Z" fill="{fill}"/>')
บรรทัด 37–41: chedi สร้างพาธรูปเจดีย์ที่ตำแหน่ง x ฐาน base ความสูง h และสี fill
บรรทัด 44–96  สร้างภาพของหนึ่งจังหวัด
44  def make(slug, region):
45      rng = random.Random(slug)
46      top, bot, far, near = PAL.get(region, PAL['ภาคกลาง'])
47      shift = rng.randint(-10, 10)
48      sun_x, sun_y = rng.randint(300, 1300), rng.randint(190, 300)
49      g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">',
50           f'<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset=".72" stop-color="{bot}"/></linearGradient>'
51           f'<radialGradient id="g"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>',
52           f'<rect width="{W}" height="{H}" fill="url(#s)" style="filter:hue-rotate({shift}deg)"/>',
53           f'<circle cx="{sun_x}" cy="{sun_y}" r="230" fill="url(#g)" opacity=".55"/><circle cx="{sun_x}" cy="{sun_y}" r="62" fill="#fff6d8" opacity=".95"/>']
54      for _ in range(5):   # เมฆ
55          cx, cy = rng.randint(0, W), rng.randint(60, 240)
56          g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rng.randint(90, 190)}" ry="{rng.randint(12, 24)}" fill="#fff" opacity=".22"/>')
57      coast = slug in COAST
58      if region == 'ภาคเหนือ' or slug in ('kanchanaburi', 'tak', 'phetchabun', 'loei', 'nakhonnayok'):
59          g.append(f'<path d="{ridge(rng, 420, 190, 7)}" fill="{far}" opacity=".7"/>')
60          g.append(f'<path d="{ridge(rng, 500, 200, 6)}" fill="{far}"/>')
61          g.append(f'<path d="{ridge(rng, 585, 150, 8)}" fill="{near}"/>')
62          g.append(f'<rect y="440" width="{W}" height="90" fill="#fff" opacity=".12"/>')
63      elif slug in CITY:
64          g.append(f'<path d="{ridge(rng, 520, 40, 10)}" fill="{far}" opacity=".6"/>')
65          x = 0
66          while x < W:
67              w, h = rng.randint(50, 120), rng.randint(110, 330)
68              g.append(f'<rect x="{x}" y="{H - 90 - h}" width="{w}" height="{h + 90}" fill="{near}" opacity="{rng.choice([.85, .95, 1])}"/>')
69              for wy in range(H - 70 - h, H - 100, 34):
70                  if rng.random() < .55: g.append(f'<rect x="{x + 10}" y="{wy}" width="{max(w - 20, 8)}" height="6" fill="#ffd66b" opacity=".6"/>')
71              x += w + rng.randint(0, 14)
72      elif slug in TEMPLE:
73          g.append(f'<path d="{ridge(rng, 500, 60, 8)}" fill="{far}" opacity=".7"/>')
74          for _ in range(rng.randint(3, 5)):
75              g.append(chedi(rng.randint(120, W - 120), 560, rng.randint(200, 360), near))
76          g.append(f'<path d="{ridge(rng, 585, 30, 12)}" fill="{near}"/>')
77      elif coast:
78          g.append(f'<path d="{ridge(rng, 400, 150, 6)}" fill="{far}" opacity=".75"/>')   # เกาะไกลๆ
79          g.append(f'<rect y="430" width="{W}" height="{H - 430}" fill="{far}" opacity=".9"/>')
80          for i in range(9):
81              y = 450 + i * 20
82              g.append(f'<path d="M0,{y} q100,-14 200,0 t200,0 t200,0 t200,0 t200,0 t200,0 t200,0 t200,0" stroke="#fff" stroke-width="3" fill="none" opacity="{.35 - i * .03:.2f}"/>')
83          g.append(f'<path d="{ridge(rng, 600, 120, 5)}" fill="{near}"/>')
84          bx = rng.randint(500, 1100)
85          g.append(f'<path d="M{bx},470 h90 l-18,22 h-54z M{bx + 44},470 v-78 l44,70z" fill="#fff" opacity=".9"/>')
86      else:   # ที่ราบ ทุ่งนา
87          g.append(f'<path d="{ridge(rng, 470, 90, 7)}" fill="{far}" opacity=".7"/>')
88          for i in range(6):
89              y = 500 + i * 24
90              g.append(f'<path d="M0,{y} Q{W / 2:.0f},{y - 30 + i * 4} {W},{y}" stroke="{near}" stroke-width="{10 + i * 3}" fill="none" opacity="{.45 + i * .08:.2f}"/>')
91          g.append(f'<path d="{ridge(rng, 600, 25, 14)}" fill="{near}"/>')
92          for _ in range(rng.randint(2, 4)):   # ต้นตาล
93              x = rng.randint(80, W - 80); h = rng.randint(150, 240)
94              g.append(f'<rect x="{x}" y="{600 - h}" width="9" height="{h}" fill="{near}"/><ellipse cx="{x + 4}" cy="{600 - h}" rx="58" ry="16" fill="{near}"/>')
95      g.append(f'<rect width="{W}" height="{H}" fill="#000" opacity=".08"/></svg>')
96      return ''.join(g)
บรรทัด 44–48: ประกาศ make ตั้งตัวสุ่มจาก slug (ภาพของแต่ละจังหวัดคงเดิมทุกครั้ง) เลือกจานสีตามภาค สุ่มการหมุนสีและตำแหน่งดวงอาทิตย์
บรรทัด 49–53: เริ่ม SVG: ไล่สีท้องฟ้า แสงเรืองรอง ดวงอาทิตย์
บรรทัด 54–56: วาดเมฆ 5 ก้อน
บรรทัด 57: ตรวจว่าเป็นจังหวัดชายฝั่ง
บรรทัด 58–62: ภูเขาซ้อนกัน 3 ชั้นสำหรับภาคเหนือและจังหวัดภูเขาที่ระบุ พร้อมแถบหมอก
บรรทัด 63–71: ฉากเมือง: สุ่มตึกสูงต่ำและหน้าต่างสีเหลือง
บรรทัด 72–76: ฉากวัด: เจดีย์ 3–5 องค์
บรรทัด 77–85: ฉากทะเล: เกาะไกล พื้นน้ำ คลื่น ฝั่ง และเรือใบ
บรรทัด 86–94: ฉากทุ่งนา: เนินไกล คันนา ฝั่งใกล้ และต้นตาล 2–4 ต้น
บรรทัด 95–96: ซ้อนชั้นมืดบาง ๆ ปิดแท็ก SVG และคืนข้อความ
บรรทัด 99–114  ฟังก์ชันหลัก
99  def main():
100      os.makedirs(OUT, exist_ok=True)
101      import sys
102      sys.path.insert(0, os.path.join(ROOT, 'data'))
103      from thai_provinces import PROVINCES_77, EXTRA_AREAS
104      region = {p[0]: p[3] for p in PROVINCES_77}
105      region.update({k: v[2] for k, v in EXTRA_AREAS.items()})
106      provs = json.load(open(os.path.join(ROOT, 'data', 'provinces.json'), encoding='utf-8'))
107      slugs = sorted(set(region) | {s for s in provs if not s.startswith('_')})
108      for s in slugs:
109          open(os.path.join(OUT, s + '.svg'), 'w', encoding='utf-8').write(make(s, region.get(s, 'ภาคใต้' if s in COAST else 'ภาคกลาง')))
110      print(len(slugs), 'banners ->', OUT)
111
112
113  if __name__ == '__main__':
114      main()
บรรทัด 99–100: ประกาศ main สร้างโฟลเดอร์ปลายทาง
บรรทัด 101–103: นำเข้า PROVINCES_77 และ EXTRA_AREAS จาก ➜ data/thai_provinces.py
บรรทัด 104–105: สร้างตารางจังหวัด → ภาค (รวมเกาะสมุย)
บรรทัด 106–107: อ่านโปรไฟล์จังหวัดจาก data/provinces.json และรวมรายชื่อ slug ทั้งหมด
บรรทัด 108–109: เขียนไฟล์ SVG ของแต่ละจังหวัด (ถ้าไม่ทราบภาค ใช้ภาคใต้สำหรับชายฝั่งหรือภาคกลาง)
บรรทัด 110: พิมพ์จำนวนภาพที่สร้าง
บรรทัด 113–114: เรียก main() เมื่อรันไฟล์ตรง ๆ

ไฟล์ที่เชื่อมกับไฟล์นี้
data/thai_provinces.py
frontend/app.js