# -*- coding: utf-8 -*-
"""สร้างคู่มือโค้ด (.docx) จากไฟล์ spec ใน spec/*.txt

วิธีใช้:  python build_manual.py            # สร้างทุกไฟล์ที่มี spec + สารบัญ
          python build_manual.py algorithm/hybrid.py   # สร้างเฉพาะไฟล์นั้น

รูปแบบ spec (ไฟล์ spec/<path ที่ / เปลี่ยนเป็น __>.txt เช่น algorithm__hybrid.py.txt):
  @title   ชื่อหัวเรื่องสั้น ๆ
  @role    บทบาทของไฟล์ 1-2 ประโยค (ขึ้นต้นเอกสาร)
  @@ 12-30 หัวข้อของบล็อก      <- บล็อกโค้ดบรรทัด 12-30 (โค้ดจริงถูกดึงจากไฟล์อัตโนมัติ)
  12: คำอธิบายบรรทัด 12
  14-18: คำอธิบายบรรทัด 14 ถึง 18
  ข้อความธรรมดา (ไม่ขึ้นต้นด้วยเลขบรรทัด) = ย่อหน้าอธิบายรวม
ลิงก์ข้ามไฟล์ใช้ได้ในทุกข้อความ:  [[algorithm/hybrid.py#meal_fill]]  หรือ  [[algorithm/hybrid.py#meal_fill|ข้อความลิงก์]]
                                    [[algorithm/hybrid.py]] (ลิงก์ไปหน้าแรกของไฟล์นั้น)
บุ๊กมาร์กของฟังก์ชัน/คลาสสร้างให้อัตโนมัติจาก def/class/function ที่อยู่ในบล็อก
"""
import os, re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(OUT, 'spec')
TH_FONT = 'TH Sarabun New'
CODE_FONT = 'Consolas'


def docname(path):
    return path.replace('/', '__') + '.docx'


def set_font(run, name, size=None, bold=None, color=None):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), name)
    if size: run.font.size = Pt(size)
    if bold is not None: run.font.bold = bold
    if color: run.font.color.rgb = RGBColor.from_string(color)


def shade(par, fill):
    ppr = par._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    ppr.append(shd)


def para_fmt(par, before=0, after=0, left=None, line=None):
    pf = par.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    if left is not None: pf.left_indent = Cm(left)
    if line: pf.line_spacing = line


_bm_id = [100]


def add_bookmark(par, name):
    _bm_id[0] += 1
    s = OxmlElement('w:bookmarkStart'); s.set(qn('w:id'), str(_bm_id[0])); s.set(qn('w:name'), name)
    e = OxmlElement('w:bookmarkEnd'); e.set(qn('w:id'), str(_bm_id[0]))
    par._p.append(s)
    par._p.append(e)


def add_link(par, target, text, size=14, color='0563C1'):
    part = par.part
    rid = part.relate_to(target, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rid)
    r = OxmlElement('w:r'); rpr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts')
    for a in ('w:ascii', 'w:hAnsi', 'w:cs'): rf.set(qn(a), TH_FONT)
    rpr.append(rf)
    c = OxmlElement('w:color'); c.set(qn('w:val'), color); rpr.append(c)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rpr.append(u)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(int(size * 2))); rpr.append(sz)
    szc = OxmlElement('w:szCs'); szc.set(qn('w:val'), str(int(size * 2))); rpr.append(szc)
    r.append(rpr)
    t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); r.append(t)
    h.append(r); par._p.append(h)


LINK_RE = re.compile(r'\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]')
TICK_RE = re.compile(r'`([^`]+)`')
used_links = set()


def rich(par, text, size=14):
    """ข้อความ + `โค้ดสั้น` + [[ลิงก์]]"""
    pos = 0
    pieces = []
    for m in LINK_RE.finditer(text):
        pieces.append(('t', text[pos:m.start()])); pieces.append(('l', m)); pos = m.end()
    pieces.append(('t', text[pos:]))
    for kind, val in pieces:
        if kind == 't':
            p2 = 0
            for tm in TICK_RE.finditer(val):
                if tm.start() > p2:
                    set_font(par.add_run(val[p2:tm.start()]), TH_FONT, size)
                set_font(par.add_run(tm.group(1)), CODE_FONT, size - 2, color='B03A2E')
                p2 = tm.end()
            if p2 < len(val):
                set_font(par.add_run(val[p2:]), TH_FONT, size)
        else:
            m = val
            f, sym, label = m.group(1).strip(), m.group(2), m.group(3)
            used_links.add(f)
            tgt = docname(f) + ('#fn_' + sym.strip() if sym else '')
            txt = label or ((sym.strip() + '()' if sym else '') + (' ใน ' if sym else '') + f)
            add_link(par, tgt, '➜ ' + txt, size)


DEF_PY = re.compile(r'^\s*(?:async\s+)?(?:def|class)\s+(\w+)')
DEF_JS = [re.compile(r'^\s*(?:async\s+)?function\s+(\w+)'), re.compile(r'^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(?:\(|function|\w+\s*=>)')]


def defs_in(src_lines, a, b, ext):
    names = []
    for i in range(a - 1, min(b, len(src_lines))):
        ln = src_lines[i]
        if ext == '.py':
            m = DEF_PY.match(ln)
            if m: names.append(m.group(1))
        elif ext == '.js':
            for rx in DEF_JS:
                m = rx.match(ln)
                if m: names.append(m.group(1)); break
    return names


def parse_spec(path):
    meta = {'title': '', 'role': ''}
    blocks = []
    cur = None
    for raw in open(path, encoding='utf-8').read().splitlines():
        if raw.startswith('@title'):
            meta['title'] = raw[6:].strip(); continue
        if raw.startswith('@role'):
            meta['role'] = raw[5:].strip(); continue
        m = re.match(r'^@@\s*(\d+)-(\d+)\s*(.*)$', raw)
        if m:
            cur = {'a': int(m.group(1)), 'b': int(m.group(2)), 'head': m.group(3).strip(), 'items': []}
            blocks.append(cur); continue
        if cur is None or not raw.strip():
            continue
        m = re.match(r'^(\d+)(?:-(\d+))?:\s*(.*)$', raw)
        if m:
            cur['items'].append(('line', int(m.group(1)), int(m.group(2) or m.group(1)), m.group(3)))
        else:
            cur['items'].append(('note', raw.strip()))
    return meta, blocks


def build(relpath):
    spec_path = os.path.join(SPEC, relpath.replace('/', '__') + '.txt')
    meta, blocks = parse_spec(spec_path)
    src_path = os.path.join(ROOT, relpath)
    src = open(src_path, encoding='utf-8').read().splitlines()
    ext = os.path.splitext(relpath)[1]
    used_links.clear()
    d = Document()
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Cm(1.8); sec.top_margin = sec.bottom_margin = Cm(1.8)
    st = d.styles['Normal']; st.font.name = TH_FONT; st.font.size = Pt(14)
    # title
    p = d.add_paragraph(); para_fmt(p, 0, 2)
    add_bookmark(p, 'top')
    set_font(p.add_run('คู่มือโค้ด: ' + relpath), TH_FONT, 22, True, '1F3864')
    if meta['title']:
        p = d.add_paragraph(); para_fmt(p, 0, 4)
        set_font(p.add_run(meta['title']), TH_FONT, 16, False, '595959')
    p = d.add_paragraph(); para_fmt(p, 0, 6)
    set_font(p.add_run(f'ไฟล์ต้นฉบับ: {relpath} ({len(src)} บรรทัด)   '), TH_FONT, 12, False, '7F7F7F')
    add_link(p, docname('INDEX'), '➜ กลับสารบัญคู่มือ', 12)
    if meta['role']:
        p = d.add_paragraph(); para_fmt(p, 4, 8); shade(p, 'EAF1FB')
        rich(p, 'บทบาทของไฟล์: ' + meta['role'], 14)
    d.add_paragraph()
    covered = set()
    for blk in blocks:
        a, b = blk['a'], min(blk['b'], len(src))
        names = defs_in(src, a, b, ext)
        p = d.add_paragraph(); para_fmt(p, 10, 3)
        p.paragraph_format.keep_with_next = True
        for n in names:
            add_bookmark(p, 'fn_' + n)
        set_font(p.add_run(f'บรรทัด {a}–{b}  {blk["head"]}'), TH_FONT, 16, True, 'C55A11')
        # code
        width = len(str(b))
        for i in range(a - 1, b):
            cp = d.add_paragraph(); para_fmt(cp, 0, 0, line=1.0); shade(cp, 'F2F2F2')
            code = src[i].replace('\t', '    ')
            set_font(cp.add_run(f'{i + 1:>{width}}  '), CODE_FONT, 8.5, color='7F7F7F')
            set_font(cp.add_run(code if code else ' '), CODE_FONT, 8.5)
        covered.update(range(a, b + 1))
        # explanation
        for it in blk['items']:
            ep = d.add_paragraph(); para_fmt(ep, 2, 2, left=0.5)
            if it[0] == 'line':
                _, x, y, text = it
                lab = f'บรรทัด {x}' if x == y else f'บรรทัด {x}–{y}'
                set_font(ep.add_run(lab + ': '), TH_FONT, 14, True, '1F3864')
                rich(ep, text)
            else:
                rich(ep, it[1])
    # unexplained code check
    missing = [i for i in range(1, len(src) + 1) if i not in covered and src[i - 1].strip() and not src[i - 1].strip().startswith(('#', '//', '/*', '*', '<!--'))]
    if used_links:
        d.add_paragraph()
        p = d.add_paragraph(); set_font(p.add_run('ไฟล์ที่เชื่อมกับไฟล์นี้'), TH_FONT, 16, True, 'C55A11')
        for f in sorted(used_links):
            lp = d.add_paragraph(); para_fmt(lp, 0, 0, left=0.5)
            add_link(lp, docname(f), f)
    out = os.path.join(OUT, docname(relpath))
    d.save(out)
    return out, missing, sorted(used_links)


def build_index():
    files = sorted(f[:-4].replace('__', '/') for f in os.listdir(SPEC) if f.endswith('.txt'))
    d = Document()
    sec = d.sections[0]; sec.left_margin = sec.right_margin = Cm(2);
    st = d.styles['Normal']; st.font.name = TH_FONT; st.font.size = Pt(14)
    p = d.add_paragraph(); set_font(p.add_run('คู่มือโค้ด WeEasyTrip (Project 2)'), TH_FONT, 26, True, '1F3864')
    p = d.add_paragraph()
    rich(p, 'คู่มือนี้อธิบายโค้ดทีละไฟล์ ทีละบรรทัด ในแต่ละหน้าจะแสดงโค้ดจริงเป็นช่วง ๆ แล้วตามด้วยคำอธิบายของแต่ละบรรทัด ถ้าโค้ดเรียกใช้ฟังก์ชันที่อยู่คนละไฟล์ จะมีลิงก์ ➜ กดไปที่ฟังก์ชันนั้นในคู่มือของอีกไฟล์ได้ทันที (เก็บไฟล์ .docx ทั้งหมดไว้ในโฟลเดอร์เดียวกันเพื่อให้ลิงก์ทำงาน)')
    groups = {}
    for f in files:
        groups.setdefault(f.split('/')[0], []).append(f)
    names = {'algorithm': 'อัลกอริทึม (algorithm/)', 'backend': 'เซิร์ฟเวอร์ (backend/)', 'frontend': 'หน้าเว็บ (frontend/)', 'experiments': 'การทดลอง (experiments/)', 'data': 'ข้อมูลและท่อประมวลผล (data/)'}
    for g in ('algorithm', 'backend', 'frontend', 'experiments', 'data'):
        if g not in groups: continue
        p = d.add_paragraph(); para_fmt(p, 12, 4); set_font(p.add_run(names[g]), TH_FONT, 18, True, 'C55A11')
        for f in groups[g]:
            meta, _ = parse_spec(os.path.join(SPEC, f.replace('/', '__') + '.txt'))
            lp = d.add_paragraph(); para_fmt(lp, 0, 1, left=0.5)
            add_link(lp, docname(f), f)
            if meta['title']:
                set_font(lp.add_run('  — ' + meta['title']), TH_FONT, 13, False, '595959')
    p = d.add_paragraph(); para_fmt(p, 14, 0)
    set_font(p.add_run('หมายเหตุ: ไฟล์ frontend/app.backup.js เป็นสำเนาสำรองของ app.js รุ่นเก่า จึงไม่อธิบายซ้ำ'), TH_FONT, 12, False, '7F7F7F')
    out = os.path.join(OUT, docname('INDEX'))
    d.save(out)
    return out


if __name__ == '__main__':
    targets = sys.argv[1:] or sorted(f[:-4].replace('__', '/') for f in os.listdir(SPEC) if f.endswith('.txt'))
    for t in targets:
        out, missing, links = build(t)
        print('OK', os.path.basename(out), '| code lines not covered:', len(missing), ('first ' + str(missing[:8])) if missing else '', '| links:', links)
    print('INDEX', os.path.basename(build_index()))
