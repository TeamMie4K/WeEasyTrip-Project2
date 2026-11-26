# -*- coding: utf-8 -*-
"""make_figures.py — สร้างแผนภาพประกอบรายงาน (สถาปัตยกรรม, sequence, flowchart ของ Hybrid, โมเดลข้อมูล)
รัน: python docs/figures/make_figures.py  -> docs/figures/fig_*.png"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

plt.rcParams['font.family'] = 'TH Sarabun New'
plt.rcParams['font.size'] = 16
OUT = os.path.dirname(__file__)
INK, FILL, LINE = '#222222', '#F4F4F4', '#555555'
ACC = '#E2711D'


def box(ax, x, y, w, h, text, fc=FILL, ec=LINE, fs=15, bold=False, lw=1.3, style='round,pad=0.02,rounding_size=0.08'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs, color=INK,
            fontweight='bold' if bold else 'normal', linespacing=1.15)


def arrow(ax, p, q, text=None, dashed=False, fs=13, off=(0, 0.12), both=False):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='<|-|>' if both else '-|>', mutation_scale=14, lw=1.3, color=LINE,
                                 linestyle='--' if dashed else '-', shrinkA=0, shrinkB=0))
    if text:
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], text, ha='center', va='bottom', fontsize=fs, color=INK)


def canvas(w, h, name):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis('off')
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_architecture():
    fig, ax = canvas(10, 6.4, 'arch')
    # layers
    for y, h, t in ((4.55, 1.65, 'ส่วนติดต่อผู้ใช้ (Frontend: HTML / JavaScript / Leaflet.js)'),
                    (2.25, 2.0, 'เซิร์ฟเวอร์ (Backend: Python FastAPI)'),
                    (0.1, 1.85, 'ส่วนอัลกอริทึมและข้อมูล')):
        ax.add_patch(FancyBboxPatch((0.1, y), 9.8, h, boxstyle='round,pad=0.02,rounding_size=0.1', fc='white', ec=LINE, lw=1.1, ls='--'))
        ax.text(0.3, y + h - 0.12, t, va='top', fontsize=14, color=ACC, fontweight='bold')
    fx = [('ฟอร์มกรอกงบ/วัน/จังหวัด\nและความชอบ', 0.3), ('แผนที่และรายการวัน\n(ลากวาง สลับ ลบ)', 2.75), ('ย้อนกลับ/เดินหน้า\nปฏิทิน .ics / PDF', 5.2), ('หน้าสรุปผลทดลอง\nโหมด Developer', 7.65)]
    for t, x in fx:
        box(ax, x, 4.65, 2.1, 0.95, t, fs=14)
    be = [('/api/packages\n/api/pareto', 0.3), ('/api/recompute\n/api/reoptimize', 2.75), ('/api/sessions\n(วางแผนร่วมกัน)', 5.2), ('ตรวจสิทธิ์ Dev\nจำกัดอัตราคำขอ', 7.65)]
    for t, x in be:
        box(ax, x, 2.4, 2.1, 0.95, t, fs=14)
    box(ax, 0.3, 0.2, 2.1, 0.95, 'Greedy / GA\nHybrid + ILS', fs=14, fc='#FCEBDD')
    box(ax, 2.75, 0.2, 2.1, 0.95, 'NSGA-II (Pareto)\nRL (REINFORCE)', fs=14)
    box(ax, 5.2, 0.2, 2.1, 0.95, 'ตัวตรวจแผนกลาง\n(evaluate_route)', fs=14)
    box(ax, 7.65, 0.2, 2.1, 0.95, 'ข้อมูล 77 จังหวัด\n(JSON จาก OSM)', fs=14)
    arrow(ax, (5.0, 4.6), (5.0, 3.45), None, both=True)
    ax.text(5.15, 4.15, 'REST / JSON', fontsize=13, va='center', bbox=dict(fc='white', ec='none', pad=1))
    arrow(ax, (5.0, 2.35), (5.0, 1.25), None, both=True)
    ax.text(5.15, 2.05, 'เรียกใช้', fontsize=13, va='center', bbox=dict(fc='white', ec='none', pad=1))
    save(fig, 'fig_architecture.png')


def fig_sequence():
    fig, ax = canvas(10, 6.6, 'seq')
    cols = [('ผู้ใช้', 1.0), ('Frontend', 3.4), ('Backend API', 5.9), ('Algorithm Engine', 8.4)]
    for t, x in cols:
        box(ax, x - 0.85, 6.0, 1.7, 0.5, t, fs=15, bold=True)
        ax.plot([x, x], [0.25, 6.0], color=LINE, lw=1, ls=':')
    X = dict((t, x) for t, x in cols)
    steps = [
        ('ผู้ใช้', 'Frontend', 5.6, 'กรอกงบ วัน จังหวัด ความชอบ', False),
        ('Frontend', 'Backend API', 5.15, 'POST /api/packages', False),
        ('Backend API', 'Algorithm Engine', 4.7, 'รัน Hybrid 3 ระดับ', False),
        ('Algorithm Engine', 'Backend API', 4.25, 'เส้นทางรายวัน + ผลตรวจข้อจำกัด', True),
        ('Backend API', 'Frontend', 3.8, '3 แพ็กเกจ (JSON)', True),
        ('Frontend', 'ผู้ใช้', 3.35, 'แสดงแผนที่และตารางค่าใช้จ่าย', True),
        ('ผู้ใช้', 'Frontend', 2.7, 'สลับ / เพิ่ม / ลบ / ลากสถานที่', False),
        ('Frontend', 'Backend API', 2.25, 'POST /api/recompute', False),
        ('Backend API', 'Frontend', 1.8, 'เวลา ค่าใช้จ่าย คำเตือนใหม่', True),
        ('ผู้ใช้', 'Frontend', 1.15, 'ส่งออกปฏิทิน (.ics) / PDF', False),
        ('Frontend', 'ผู้ใช้', 0.7, 'ไฟล์ปฏิทิน / หน้าพิมพ์ (สร้างฝั่งเบราว์เซอร์)', True),
    ]
    for a, b, y, t, back in steps:
        arrow(ax, (X[a], y), (X[b], y), t, dashed=back, fs=13, off=(0, 0.05))
    save(fig, 'fig_sequence.png')


def fig_hybrid_flow():
    fig, ax = canvas(7.6, 9.4, 'flow')
    cx, w, h = 3.8, 4.6, 0.8
    items = [('ข้อมูล POI + โรงแรม + งบ + จำนวนวัน', FILL),
             ('1) Greedy seed แบบ slot-based\n(หลายจุดเริ่มต้น + seed แบบ ratio)', FILL),
             ('2) Genetic Algorithm refinement\n(crossover รายวัน, mutation, slot repair)', FILL),
             ('3) 2-opt จัดลำดับจุดภายในวัน', FILL),
             ('4) Insertion Local Search (ILS)\nแทนที่ / เติม / shake', '#FCEBDD'),
             ('5) meal_fill และซ่อมเวลา-เวลาปิด', FILL),
             ('6) ซ่อมงบ (_budget_repair)', FILL),
             ('ตรวจแผนด้วย evaluate_route', FILL)]
    n = len(items)
    top = 9.0
    gap = 1.12
    ys = []
    for i, (t, fc) in enumerate(items):
        y = top - i * gap - h
        ys.append(y)
        box(ax, cx - w / 2, y, w, h, t, fc=fc, fs=14)
        if i:
            arrow(ax, (cx, ys[i - 1]), (cx, y + h))
    # decision diamond
    dy = ys[-1] - 1.1
    ax.add_patch(Polygon([[cx, dy + 0.9], [cx + 1.3, dy + 0.45], [cx, dy], [cx - 1.3, dy + 0.45]], fc='white', ec=LINE, lw=1.3))
    ax.text(cx, dy + 0.45, 'ผ่านข้อจำกัด?', ha='center', va='center', fontsize=14)
    arrow(ax, (cx, ys[-1]), (cx, dy + 0.9))
    box(ax, cx - 1.1, dy - 1.0, 2.2, 0.6, 'ส่งแผนให้ผู้ใช้', fs=14, fc='#E9F5E9')
    arrow(ax, (cx, dy), (cx, dy - 0.4), 'ใช่', off=(0.3, -0.02))
    # no-loop
    ax.plot([cx + 1.3, cx + 3.0, cx + 3.0], [dy + 0.45, dy + 0.45, ys[1] + h / 2], color=LINE, lw=1.3)
    arrow(ax, (cx + 3.0, ys[1] + h / 2), (cx + w / 2, ys[1] + h / 2))
    ax.text(cx + 2.15, dy + 0.5, 'ไม่: สร้างใหม่ (สูงสุด 3 ครั้ง)', fontsize=12, ha='center', va='bottom')
    ax.set_xlim(0, 7.6); ax.set_ylim(dy - 1.2, 9.2)
    save(fig, 'fig_hybrid_flow.png')


def fig_er():
    fig, ax = canvas(7.2, 6.6, 'er')
    def ent(x, y, title, rows, w=2.9):
        h = 0.5 + 0.32 * len(rows)
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.06', fc='white', ec=LINE, lw=1.3))
        ax.add_patch(FancyBboxPatch((x, y + h - 0.45), w, 0.45, boxstyle='round,pad=0.02,rounding_size=0.06', fc='#FCEBDD', ec=LINE, lw=1.3))
        ax.text(x + w / 2, y + h - 0.22, title, ha='center', va='center', fontsize=15, fontweight='bold')
        for i, r in enumerate(rows):
            ax.text(x + 0.12, y + h - 0.45 - 0.32 * (i + 0.65), r, fontsize=13, va='center')
    ent(0.2, 3.0, 'Province', ['slug (PK)', 'name_th / name_en', 'center (lat, lng)', 'road_factor, speed_kmh', 'sparse (เบาบางหรือไม่)'], w=2.7)
    ent(0.2, 0.15, 'Session (วางแผนร่วมกัน)', ['id (PK)', 'province (FK)', 'version', 'package (JSON)', 'updated'], w=2.7)
    ent(3.9, 0.15, 'POI', ['id (PK)', 'province (FK)', 'name_th / name_en', 'category', 'lat, lng', 'cost, duration_min', 'open_min, close_min', 'score', 'tags (diet, cuisine ฯลฯ)'], w=3.0)
    ent(3.9, 4.0, 'Hotel', ['id (PK)', 'province (FK)', 'name_th / name_en', 'stars, score', 'lat, lng', 'cost (ต่อคืน)'], w=3.0)
    arrow(ax, (2.9, 3.4), (3.9, 2.2), None)
    arrow(ax, (2.9, 4.6), (3.9, 5.1), None)
    arrow(ax, (1.55, 3.0), (1.55, 2.5), None)
    ax.text(3.15, 3.15, '1 : N', fontsize=12, ha='center'); ax.text(3.15, 4.95, '1 : N', fontsize=12, ha='center')
    ax.text(1.75, 2.72, '1 : N', fontsize=12, ha='left')
    ax.set_xlim(0, 7.2); ax.set_ylim(0, 6.6)
    save(fig, 'fig_er.png')




if __name__ == '__main__':
    fig_architecture(); fig_sequence(); fig_hybrid_flow(); fig_er()
    print('ok')
