# -*- coding: utf-8 -*-
"""สร้างภาพแบนเนอร์ SVG ประจำจังหวัด (ครบทุกจังหวัดใน provinces.json) -> frontend/img/provinces/<slug>.svg
ภาพเป็นภาพวาดเชิงนามธรรมตามลักษณะพื้นที่ (ทะเล/ภูเขา/ทุ่งนา/วัด/เมือง) สร้างจาก slug ให้ได้ผลเดิมทุกครั้ง ไม่ใช่ภาพถ่ายจริง
ถ้าต้องการภาพถ่ายจริง วางไฟล์ <slug>.jpg ไว้ในโฟลเดอร์เดียวกัน หน้าเว็บจะใช้ .jpg ก่อน .svg
รัน: python data/make_banners.py
"""
import json, os, random, math

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'frontend', 'img', 'provinces')
W, H = 1600, 640
COAST = set('''phuket krabi samui suratthani phangnga ranong satun trang songkhla pattani narathiwat nakhonsithammarat chumphon
prachuapkhirikhan phetchaburi samutsongkhram samutsakhon samutprakan chonburi rayong chanthaburi trat chachoengsao bangkok'''.split())
CITY = set('bangkok nonthaburi pathumthani samutprakan'.split())
TEMPLE = set('ayutthaya sukhothai lopburi angthong singburi chainat suphanburi nakhonpathom saraburi kamphaengphet phitsanulok phichit uthaithani nakhonsawan'.split())
PAL = {   # (บนฟ้า, ล่างฟ้า, สีเงาไกล, สีเงาใกล้)
    'ภาคเหนือ': ('#1f6f78', '#f6c98b', '#3b8a7e', '#164e4a'),
    'ภาคตะวันออกเฉียงเหนือ': ('#c2410c', '#fcd88a', '#b4571f', '#7c2d12'),
    'ภาคกลาง': ('#6d4aa6', '#f9b98a', '#8a5a9c', '#3f2a63'),
    'ภาคตะวันออก': ('#0e7490', '#fbd38d', '#2b8ca1', '#134e63'),
    'ภาคตะวันตก': ('#2f6b4f', '#f3d69a', '#4a8467', '#1d4535'),
    'ภาคใต้': ('#0369a1', '#ffd9a0', '#2f86b8', '#0b4a70'),
}


def ridge(rng, y, amp, steps, jag=1.0):
    pts = [(0, y)]
    for i in range(1, steps):
        pts.append((W * i / steps, y - rng.random() * amp * jag))
    pts.append((W, y))
    d = f'M0,{H} L0,{y} '
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        d += f'Q{x1:.0f},{y1:.0f} {(x1 + x2) / 2:.0f},{(y1 + y2) / 2:.0f} '
    return d + f'L{W},{H} Z'


def chedi(x, base, h, fill):
    w = h * 0.42
    return (f'<path d="M{x - w / 2:.0f},{base} L{x - w / 2:.0f},{base - h * .18:.0f} L{x - w * .35:.0f},{base - h * .32:.0f} L{x - w * .22:.0f},{base - h * .5:.0f} '
            f'L{x - w * .1:.0f},{base - h * .78:.0f} L{x:.0f},{base - h:.0f} L{x + w * .1:.0f},{base - h * .78:.0f} L{x + w * .22:.0f},{base - h * .5:.0f} '
            f'L{x + w * .35:.0f},{base - h * .32:.0f} L{x + w / 2:.0f},{base - h * .18:.0f} L{x + w / 2:.0f},{base} Z" fill="{fill}"/>')


def make(slug, region):
    rng = random.Random(slug)
    top, bot, far, near = PAL.get(region, PAL['ภาคกลาง'])
    shift = rng.randint(-10, 10)
    sun_x, sun_y = rng.randint(300, 1300), rng.randint(190, 300)
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">',
         f'<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset=".72" stop-color="{bot}"/></linearGradient>'
         f'<radialGradient id="g"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#s)" style="filter:hue-rotate({shift}deg)"/>',
         f'<circle cx="{sun_x}" cy="{sun_y}" r="230" fill="url(#g)" opacity=".55"/><circle cx="{sun_x}" cy="{sun_y}" r="62" fill="#fff6d8" opacity=".95"/>']
    for _ in range(5):   # เมฆ
        cx, cy = rng.randint(0, W), rng.randint(60, 240)
        g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rng.randint(90, 190)}" ry="{rng.randint(12, 24)}" fill="#fff" opacity=".22"/>')
    coast = slug in COAST
    if region == 'ภาคเหนือ' or slug in ('kanchanaburi', 'tak', 'phetchabun', 'loei', 'nakhonnayok'):
        g.append(f'<path d="{ridge(rng, 420, 190, 7)}" fill="{far}" opacity=".7"/>')
        g.append(f'<path d="{ridge(rng, 500, 200, 6)}" fill="{far}"/>')
        g.append(f'<path d="{ridge(rng, 585, 150, 8)}" fill="{near}"/>')
        g.append(f'<rect y="440" width="{W}" height="90" fill="#fff" opacity=".12"/>')
    elif slug in CITY:
        g.append(f'<path d="{ridge(rng, 520, 40, 10)}" fill="{far}" opacity=".6"/>')
        x = 0
        while x < W:
            w, h = rng.randint(50, 120), rng.randint(110, 330)
            g.append(f'<rect x="{x}" y="{H - 90 - h}" width="{w}" height="{h + 90}" fill="{near}" opacity="{rng.choice([.85, .95, 1])}"/>')
            for wy in range(H - 70 - h, H - 100, 34):
                if rng.random() < .55: g.append(f'<rect x="{x + 10}" y="{wy}" width="{max(w - 20, 8)}" height="6" fill="#ffd66b" opacity=".6"/>')
            x += w + rng.randint(0, 14)
    elif slug in TEMPLE:
        g.append(f'<path d="{ridge(rng, 500, 60, 8)}" fill="{far}" opacity=".7"/>')
        for _ in range(rng.randint(3, 5)):
            g.append(chedi(rng.randint(120, W - 120), 560, rng.randint(200, 360), near))
        g.append(f'<path d="{ridge(rng, 585, 30, 12)}" fill="{near}"/>')
    elif coast:
        g.append(f'<path d="{ridge(rng, 400, 150, 6)}" fill="{far}" opacity=".75"/>')   # เกาะไกลๆ
        g.append(f'<rect y="430" width="{W}" height="{H - 430}" fill="{far}" opacity=".9"/>')
        for i in range(9):
            y = 450 + i * 20
            g.append(f'<path d="M0,{y} q100,-14 200,0 t200,0 t200,0 t200,0 t200,0 t200,0 t200,0 t200,0" stroke="#fff" stroke-width="3" fill="none" opacity="{.35 - i * .03:.2f}"/>')
        g.append(f'<path d="{ridge(rng, 600, 120, 5)}" fill="{near}"/>')
        bx = rng.randint(500, 1100)
        g.append(f'<path d="M{bx},470 h90 l-18,22 h-54z M{bx + 44},470 v-78 l44,70z" fill="#fff" opacity=".9"/>')
    else:   # ที่ราบ ทุ่งนา
        g.append(f'<path d="{ridge(rng, 470, 90, 7)}" fill="{far}" opacity=".7"/>')
        for i in range(6):
            y = 500 + i * 24
            g.append(f'<path d="M0,{y} Q{W / 2:.0f},{y - 30 + i * 4} {W},{y}" stroke="{near}" stroke-width="{10 + i * 3}" fill="none" opacity="{.45 + i * .08:.2f}"/>')
        g.append(f'<path d="{ridge(rng, 600, 25, 14)}" fill="{near}"/>')
        for _ in range(rng.randint(2, 4)):   # ต้นตาล
            x = rng.randint(80, W - 80); h = rng.randint(150, 240)
            g.append(f'<rect x="{x}" y="{600 - h}" width="9" height="{h}" fill="{near}"/><ellipse cx="{x + 4}" cy="{600 - h}" rx="58" ry="16" fill="{near}"/>')
    g.append(f'<rect width="{W}" height="{H}" fill="#000" opacity=".08"/></svg>')
    return ''.join(g)


def main():
    os.makedirs(OUT, exist_ok=True)
    import sys
    sys.path.insert(0, os.path.join(ROOT, 'data'))
    from thai_provinces import PROVINCES_77, EXTRA_AREAS
    region = {p[0]: p[3] for p in PROVINCES_77}
    region.update({k: v[2] for k, v in EXTRA_AREAS.items()})
    provs = json.load(open(os.path.join(ROOT, 'data', 'provinces.json'), encoding='utf-8'))
    slugs = sorted(set(region) | {s for s in provs if not s.startswith('_')})
    for s in slugs:
        open(os.path.join(OUT, s + '.svg'), 'w', encoding='utf-8').write(make(s, region.get(s, 'ภาคใต้' if s in COAST else 'ภาคกลาง')))
    print(len(slugs), 'banners ->', OUT)


if __name__ == '__main__':
    main()
