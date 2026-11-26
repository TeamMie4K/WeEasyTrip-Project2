# -*- coding: utf-8 -*-
"""make_figures3.py — use case, chromosome/crossover, flowchart ของ re-optimization
ใช้ฟังก์ชันวาดร่วมกับ make_figures.py  รัน: python docs/figures/make_figures3.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_figures import *
from matplotlib.patches import Ellipse


def fig_usecase():
    fig, ax = canvas(9, 6.2, 'uc')
    ax.add_patch(FancyBboxPatch((2.6, 0.2), 6.2, 5.8, boxstyle='round,pad=0.02,rounding_size=0.1', fc='white', ec=LINE, lw=1.3))
    ax.text(5.7, 5.72, 'ระบบ WeEasyTrip', ha='center', fontsize=16, fontweight='bold')
    uc = [('กรอกงบ จำนวนวัน จังหวัด\nและความชอบ', 5.0), ('ดู 3 แพ็กเกจบนแผนที่', 4.2), ('สลับ/เพิ่ม/ลบ/ลากสถานที่\n(ย้อนกลับ-เดินหน้า)', 3.4),
          ('ส่งออกปฏิทิน (.ics) / PDF', 2.6), ('แชร์แผนให้เพื่อนแก้ร่วมกัน', 1.8), ('เลือกอัลกอริทึม เทียบผล\nและดูผลทดลอง', 0.9)]
    for t, y in uc:
        ax.add_patch(Ellipse((5.7, y), 3.9, 0.66, fc=FILL if y > 1.0 else '#FCEBDD', ec=LINE, lw=1.2))
        ax.text(5.7, y, t, ha='center', va='center', fontsize=13, linespacing=1.05)
    for name, x, y in (('ผู้ใช้ทั่วไป', 1.2, 3.4), ('ผู้ใช้โหมด\nDeveloper', 1.2, 0.9)):
        ax.plot([x], [y + 0.55], 'o', color=INK, ms=9)
        ax.plot([x, x], [y + 0.45, y - 0.15], color=INK, lw=1.5)
        ax.plot([x - 0.3, x + 0.3], [y + 0.3, y + 0.3], color=INK, lw=1.5)
        ax.plot([x, x - 0.25], [y - 0.15, y - 0.6], color=INK, lw=1.5)
        ax.plot([x, x + 0.25], [y - 0.15, y - 0.6], color=INK, lw=1.5)
        ax.text(x, y - 0.95, name, ha='center', va='top', fontsize=13, linespacing=1.05)
    for _, y in uc[:5]:
        ax.plot([1.5, 3.75], [3.5, y], color=LINE, lw=1)
    ax.plot([1.5, 3.75], [1.0, 0.9], color=LINE, lw=1)
    ax.plot([1.5, 3.75], [1.0, 3.4], color=LINE, lw=1, ls=':')
    ax.text(2.7, -0.25, 'เส้นประ: ผู้ใช้โหมด Developer ใช้ฟังก์ชันของผู้ใช้ทั่วไปได้ด้วย', fontsize=12)
    ax.set_xlim(0, 9); ax.set_ylim(-0.6, 6.2)
    save(fig, 'fig_usecase.png')


def fig_chromosome():
    fig, ax = canvas(9.8, 5.0, 'chrom')
    cw, ch = 0.46, 0.5
    ca, cb = '#DCE8F5', '#FCEBDD'
    A = [['P3', 'P7', 'R2', 'P9', 'P1', 'R5'], ['P4', 'P8', 'R1', 'P2', 'P6', 'R3'], ['P5', 'P1', 'R4', 'P7', 'P3', 'R2']]
    B = [['P2', 'P6', 'R3', 'P4', 'P8', 'R1'], ['P9', 'P3', 'R5', 'P1', 'P5', 'R2'], ['P7', 'P2', 'R1', 'P6', 'P4', 'R3']]
    pick = [0, 1, 0]
    xs = (0.8, 4.0, 7.2)
    for x, t in zip(xs, ('พ่อแม่ A', 'พ่อแม่ B', 'ลูก (ฟ้า = จาก A, ส้ม = จาก B)')):
        ax.text(x, 4.75, t, fontsize=15, fontweight='bold')
    for d in range(3):
        y = 3.95 - d * 0.85
        ax.text(0.55, y + 0.25, f'วัน {d+1}', fontsize=12, ha='right', va='center')
        for i in range(6):
            box(ax, xs[0] + i * cw, y, cw - 0.04, ch, A[d][i], fc=ca, fs=11, style='square,pad=0')
            box(ax, xs[1] + i * cw, y, cw - 0.04, ch, B[d][i], fc=cb, fs=11, style='square,pad=0')
            src = (A, B)[pick[d]][d]
            box(ax, xs[2] + i * cw, y, cw - 0.04, ch, src[i], fc=(ca, cb)[pick[d]], fs=11, style='square,pad=0')
    ax.text(0.2, 1.15, 'P = สถานที่ท่องเที่ยว  R = ร้านอาหาร (ตำแหน่งที่ 3 = มื้อกลางวัน ตำแหน่งที่ 6 = มื้อเย็น)', fontsize=12)
    ax.text(0.2, 0.7, '1) เลือกทั้งวันจากพ่อแม่ A หรือ B   2) slot_repair ลบสถานที่ซ้ำข้ามวันและคืนรูปแบบ 4+2 จุด', fontsize=12)
    ax.text(0.2, 0.25, '3) mutation แทนที่สถานที่ในหมวดเดียวกัน หรือสลับ/เลื่อนจุดภายในวัน', fontsize=12)
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.0)
    save(fig, 'fig_chromosome.png')


def fig_reopt():
    fig, ax = canvas(7.8, 9.8, 'reopt')
    cx, w, h = 3.7, 5.2, 0.85
    items = [('แผนปัจจุบันที่ผู้ใช้แก้ + จุดล็อก (สลับเข้า/เพิ่ม)\nและจุดที่ลบ (ห้ามกลับเข้ามา)', FILL),
             ('ตรวจจุดล็อกที่ใส่ไม่ได้ (เวลา งบ) และแจ้งผู้ใช้', FILL),
             ('(mu+lambda) evolutionary search\nใช้ mutation เท่านั้น เริ่มจากแผนปัจจุบัน', '#FCEBDD'),
             ('ทิ้งผลที่ละเมิดจุดล็อกหรือจุดที่ลบ', FILL),
             ('2-opt จัดลำดับจุดในแต่ละวัน', FILL),
             ('รอบซ่อม: ซ่อมเวลา/เวลาปิด, ซ่อมงบ,\nเติมมื้อที่ขาด, ตรวจแต่ละวัน', FILL)]
    top, gap = 9.5, 1.2
    ys = []
    for i, (t, fc) in enumerate(items):
        y = top - i * gap - h
        ys.append(y)
        box(ax, cx - w / 2, y, w, h, t, fc=fc, fs=14)
        if i:
            arrow(ax, (cx, ys[i - 1]), (cx, y + h))
    dy = ys[-1] - 1.2
    ax.add_patch(Polygon([[cx, dy + 0.95], [cx + 1.5, dy + 0.48], [cx, dy], [cx - 1.5, dy + 0.48]], fc='white', ec=LINE, lw=1.3))
    ax.text(cx, dy + 0.48, 'ผ่านข้อจำกัด\nและมีมื้อครบ?', ha='center', va='center', fontsize=13, linespacing=1.05)
    arrow(ax, (cx, ys[-1]), (cx, dy + 0.95))
    box(ax, cx - 1.9, dy - 1.05, 3.8, 0.75, 'ส่งแผนใหม่ (ถอดจุดล็อกที่ชนมื้อเย็น\nและแจ้งผู้ใช้ถ้าจำเป็น)', fs=12, fc='#E9F5E9')
    arrow(ax, (cx, dy), (cx, dy - 0.3), None)
    ax.text(cx + 0.15, dy - 0.15, 'ใช่', fontsize=12)
    ax.plot([cx + 1.5, cx + 3.3, cx + 3.3], [dy + 0.48, dy + 0.48, ys[-1] + h / 2], color=LINE, lw=1.3)
    arrow(ax, (cx + 3.3, ys[-1] + h / 2), (cx + w / 2, ys[-1] + h / 2))
    ax.text(cx + 2.4, dy + 0.55, 'ไม่: วนซ้ำ', fontsize=12, ha='center', va='bottom')
    ax.set_xlim(0, 7.8); ax.set_ylim(dy - 1.3, 9.6)
    save(fig, 'fig_reopt.png')


if __name__ == '__main__':
    fig_usecase(); fig_chromosome(); fig_reopt(); print('ok')
