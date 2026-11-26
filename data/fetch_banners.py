# -*- coding: utf-8 -*-
"""
fetch_banners.py — ดาวน์โหลดภาพแบนเนอร์ประจำจังหวัดจาก Wikimedia Commons (เฉพาะไฟล์ที่ใบอนุญาตเสรี: CC0, PD, CC BY, CC BY-SA)
ผลลัพธ์: frontend/img/provinces/<slug>.jpg (กว้าง 1600 px) และ frontend/img/provinces/CREDITS.json (ผู้ถ่าย ใบอนุญาต ลิงก์ต้นฉบับ)

ขั้นตอน
  python data/fetch_banners.py search            # ค้นผู้สมัครต่อจังหวัด -> data/banner_candidates.json
  python data/fetch_banners.py download          # ดาวน์โหลดภาพที่เลือก (ผู้สมัครอันดับแรก หรือไฟล์ใน data/banner_choices.json)
  python data/fetch_banners.py rank slug ...     # ค้นใหม่แนวภาพมุมกว้าง/มุมสูง แล้วจัดอันดับตามความสวย (ผู้สมัครอันดับแรกคือภาพที่คะแนนสูงสุด)
  python data/fetch_banners.py download slug ... # ดาวน์โหลดเฉพาะจังหวัดที่ระบุ
data/banner_choices.json = {slug: "File:ชื่อไฟล์.jpg"} ใช้เลือกภาพเองแทนผู้สมัครอันดับแรก
หน้าเว็บ (frontend/extras.js setBanner) ลองใช้ img/provinces/<slug>.jpg ก่อน ถ้าไม่มีใช้ .svg ที่สร้างอัตโนมัติ
"""
import os, sys, json, re, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'frontend', 'img', 'provinces')
API = 'https://commons.wikimedia.org/w/api.php'
UA = 'WeEasyTripBanners/1.0 (student project; image fetch script)'
WIDTH = 1920
MINW = int(os.environ.get('FETCH_MINW', WIDTH))      # ผ่อนเกณฑ์ขนาดสำหรับจังหวัดที่ Commons มีภาพน้อย (ภาพจะถูกขยายไม่เกินขนาดจริง)
MINAR = float(os.environ.get('FETCH_MINAR', 1.3))
OK_LICENSE = re.compile(r'^(CC0|Public domain|PD|CC[ -]BY(-SA)?[ -]\d)', re.I)
BAD_TITLE = re.compile(r'map|logo|flag|coat of arms|seal|diagram|chart|sign|poster|stamp|banknote|plan|locator|panorama of the city hall', re.I)

# สถานที่สำคัญของแต่ละจังหวัด (เลือกให้หลากหลาย: วัด โบราณสถาน ธรรมชาติ ตลาด สะพาน ทะเลสาบ ฯลฯ) พร้อมคำค้นสำรอง
LANDMARKS = {
    'chiangmai': ['Doi Inthanon', 'Doi Suthep Wat Phra That'],
    'krabi': ['Railay Beach Krabi', 'Phra Nang Beach Krabi'],
    'samui': ['Big Buddha Koh Samui', 'Wat Phra Yai Samui'],
    'bangkok': ['Wat Arun Bangkok', 'Grand Palace Bangkok'],
    'chonburi': ['Sanctuary of Truth Pattaya', 'Pattaya Thailand viewpoint'],
    'prachuapkhirikhan': ['Phraya Nakhon Cave', 'Khao Sam Roi Yot'],
    'ayutthaya': ['Wat Chaiwatthanaram sunset', 'Wat Phra Si Sanphet', 'Ayutthaya Historical Park aerial'],
    'kanchanaburi': ['Bridge over the River Kwai Kanchanaburi', 'Erawan Waterfall'],
    'phangnga': ['Phang Nga Bay Khao Phing Kan', 'James Bond Island Thailand'],
    'chiangrai': ['Wat Rong Khun White Temple', 'White Temple Chiang Rai'],
    'suratthani': ['Cheow Lan Lake Khao Sok', 'Khao Sok National Park'],
    'nakhonratchasima': ['Phimai Historical Park', 'Khao Yai National Park', 'Nakhon Ratchasima Thailand'],
    'khonkaen': ['Wat Nong Waeng Phra Mahathat Kaen Nakhon', 'Khon Kaen nine-storey pagoda'],
    'udonthani': ['Udon Thani', 'Ban Chiang Udon Thani', 'Phu Phra Bat Historical Park'],
    'phetchaburi': ['Phra Nakhon Khiri Phetchaburi', 'Khao Wang Phetchaburi palace'],
    'rayong': ['Ko Samet beach', 'Koh Samet Ao Phrao'],
    'sukhothai': ['Sukhothai Historical Park Wat Mahathat', 'Wat Si Chum Sukhothai'],
    'phitsanulok': ['Wat Phra Si Rattana Mahathat Phitsanulok', 'Phitsanulok Wat Yai'],
    'songkhla': ['Golden Mermaid Samila Beach Songkhla', 'Samila Beach Songkhla'],
    'ubonratchathani': ['Khong Chiam Mekong Mun river', 'Sam Phan Bok', 'Pha Taem cliff Ubon', 'Wat Nong Pah Pong'],
    'nan': ['Wat Phumin Nan', 'Nan Thailand temple Wat Phumin'],
    'lampang': ['Wat Chaloem Phra Kiat Phra Bat Pong Daeng', 'Lampang Wat Sri Chum', 'Lampang Kuang river horse carriage'],
    'chanthaburi': ['Chanthaburi Cathedral Immaculate Conception', 'Cathedral Chanthaburi'],
    'phayao': ['Kwan Phayao lake', 'Phayao lake sunset'],
    'mukdahan': ['Phu Pha Thoep National Park Mukdahan', 'Wat Phu Manorom Mukdahan'],
    'roiet': ['Phra Maha Chedi Chai Mongkol Roi Et', 'Roi Et Bueng Phlan Chai'],
    'nongkhai': ['Sala Keoku Nong Khai', 'Nong Khai Friendship Bridge Mekong'],
    'lamphun': ['Wat Phra That Hariphunchai', 'Hariphunchai Lamphun'],
    'nonthaburi': ['Wat Chalermprakiat Nonthaburi', 'Nonthaburi Chao Phraya river sunset', 'Nonthaburi Wat Prasat Bunyawat'],
    'phetchabun': ['Phu Thap Boek', 'Khao Kho Phetchabun'],
    'lopburi': ['Phra Prang Sam Yot Lopburi', 'Lopburi monkey temple'],
    'samutprakan': ['Erawan Museum Samut Prakan', 'Ancient City Samut Prakan'],
    'samutsongkhram': ['Maeklong Railway Market', 'Mae Klong Railway Market umbrellas'],
    'saraburi': ['Wat Phra Phutthabat Saraburi', 'Phra Phutthabat Saraburi'],
    'trat': ['Ko Chang White Sand Beach', 'Koh Chang Trat beach'],
    'nakhonsithammarat': ['Wat Phra Mahathat Woramahawihan Nakhon Si Thammarat', 'Nakhon Si Thammarat Wat Phra Mahathat'],
    'trang': ['Trang Thailand', 'Hat Yao Trang', 'Koh Kradan Trang'],
    'maehongson': ['Wat Phra That Doi Kong Mu Mae Hong Son', 'Mae Hong Son Wat Chong Kham Chong Klang'],
    'loei': ['Phu Ruea Loei sea of mist', 'Chiang Khan Loei Mekong', 'Phu Pa Po Loei'],
    'phrae': ['Wat Phra That Cho Hae Phrae', 'Phrae old town teak house', 'Phrae Wat Luang'],
    'uttaradit': ['Sirikit Dam Uttaradit', 'Uttaradit Thailand'],
    'kalasin': ['Lam Pao Dam reservoir','Phu Phan mountains Kalasin','Phu Kum Khao Sirindhorn dinosaur museum','Kalasin Thailand sunset','Wat Phu Pa Phan Kalasin'],
    'buriram': ['Prasat Phanom Rung', 'Phanom Rung Historical Park'],
    'yasothon': ['Yasothon Thailand', 'Phaya Thaen Yasothon', 'Wat Mahathat Yasothon'],
    'sisaket': ['Khao Phra Wihan Preah Vihear Sisaket', 'Prasat Sa Kamphaeng Yai', 'Wat Lan Khuat Sisaket bottle temple'],
    'sakonnakhon': ['Phra That Choeng Chum Sakon Nakhon', 'Wat Phra That Choeng Chum'],
    'surin': ['Prasat Sikhoraphum', 'Prasat Mueang Tam Surin', 'Surin Thailand landscape'],
    'nongbualamphu': ['Tham Erawan Nong Bua Lamphu', 'Erawan Cave Nong Bua Lamphu'],
    'kamphaengphet': ['Kamphaeng Phet Historical Park', 'Wat Phra Kaeo Kamphaeng Phet'],
    'chainat': ['Wat Phra Borommathat Woramahawihan Chai Nat', 'Chainat Chao Phraya dam', 'Chai Nat Wat Thammamun'],
    'nakhonnayok': ['Sarika Waterfall Nakhon Nayok', 'Nang Rong Waterfall'],
    'nakhonpathom': ['Phra Pathommachedi Nakhon Pathom', 'Phra Pathom Chedi'],
    'nakhonsawan': ['Bueng Boraphet', 'Nakhon Sawan Paknam Pho'],
    'pathumthani': ['Wat Phra Dhammakaya Pathum Thani', 'Dhammakaya Cetiya'],
    'phichit': ['Wat Tha Luang Phichit', 'Bueng Si Fai Phichit lake', 'Phichit Wat Hat Sieo'],
    'samutsakhon': ['Samut Sakhon salt farm', 'Mahachai Samut Sakhon fishing'],
    'singburi': ['Bang Rachan Monument Sing Buri', 'Bang Rachan Singburi'],
    'suphanburi': ['Wat Pa Lelai Suphanburi', 'Don Chedi Monument Suphanburi', 'Suphan Buri Wat Phra Si Rattana Mahathat'],
    'uthaithani': ['Wat Tha Sung Uthai Thani', 'Sakaekrang River Uthai Thani'],
    'chachoengsao': ['Wat Sothonwararam Chachoengsao', 'Wat Sothon Chachoengsao'],
    'prachinburi': ['Kaeng Hin Phoeng Prachinburi', 'Thap Lan National Park', 'Dong Phayayen Prachinburi'],
    'sakaeo': ['Pang Sida National Park', 'Sa Kaeo Thailand Pang Sida waterfall'],
    'tak': ['Thi Lo Su Waterfall', 'Bhumibol Dam Tak'],
    'ratchaburi': ['Damnoen Saduak floating market', 'Ratchaburi Wat Khao Ngu cave'],
    'chumphon': ['Thung Wua Laen Beach Chumphon', 'Chumphon Thailand beach'],
    'narathiwat': ['Taksin Ratchaniwet Palace Narathiwat', 'Wat Chonthara Singhe Narathiwat', 'Narathiwat mosque Wadi Al-Hussein'],
    'phatthalung': ['Thale Noi Phatthalung', 'Thale Noi waterbird park lotus'],
    'ranong': ['Ranong Raksa Warin hot spring', 'Koh Phayam Ranong beach sunset', 'Ranong Thailand Kraburi river Myanmar border'],
    'satun': ['Tham Le Stegodon Satun', 'Ko Lipe Satun beach'],
    'yala': ['Bang Lang Dam Yala', 'Yala City Pillar Shrine', 'Aiyoeweng Yala', 'Yala', 'Yala province', 'Betong'],
    'chaiyaphum': ['Pa Hin Ngam National Park', 'Tat Ton Waterfall Chaiyaphum'],
    'nakhonphanom': ['Wat Phra That Phanom', 'Phra That Phanom Nakhon Phanom'],
    'buengkan': ['Wat Phu Tok Bueng Kan', 'Phu Tok Bueng Kan'],
    'mahasarakham': ['Maha Sarakham', 'Phra That Na Dun', 'Maha Sarakham Thailand temple'],
    'amnatcharoen': ['Phu Sa Dok Bua National Park', 'Amnat Charoen Wat Phu Phra Angkhan', 'Amnat Charoen reservoir sunset'],
    'angthong': ['Great Buddha of Thailand Wat Muang Ang Thong', 'Ang Thong Wat Khun Inthapramun reclining Buddha', 'Ang Thong Thailand temple'],
    'pattani': ['Lim Ko Niao Shrine Pattani', 'Pattani Bay Yaring beach', 'Pattani Central Mosque'],
}


def api(params, tries=6):
    url = API + '?' + urllib.parse.urlencode(params)
    for k in range(tries):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            wait = int(e.headers.get('Retry-After') or 0) or 10 * (k + 1)   # ถูกจำกัดอัตราคำขอ: รอแล้วลองใหม่
            print('  429 รอ', wait, 'วินาที', flush=True)
            time.sleep(wait)


def thumb_url(title):
    """ขอ URL ภาพย่อกว้าง WIDTH px ของไฟล์เดียว (ขอตอนดาวน์โหลดเท่านั้น เพื่อไม่ให้ Commons สร้างภาพย่อให้ทุกผู้สมัคร)"""
    data = api({'action': 'query', 'format': 'json', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url', 'iiurlwidth': WIDTH})
    pg = next(iter(data['query']['pages'].values()))
    return pg['imageinfo'][0]['thumburl']


def clean(html):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html or '')).strip()


def search(query, limit=20):
    data = api({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': query + ' filetype:bitmap',
                'gsrnamespace': 6, 'gsrlimit': limit, 'prop': 'imageinfo', 'iiprop': 'url|size|mime|extmetadata'})
    out = []
    for pg in sorted((data.get('query', {}).get('pages', {})).values(), key=lambda p: p.get('index', 0)):
        ii = (pg.get('imageinfo') or [{}])[0]
        md = ii.get('extmetadata', {})
        lic = (md.get('LicenseShortName') or {}).get('value', '')
        w, h = ii.get('width', 0), ii.get('height', 1)
        title = pg['title']
        if ii.get('mime') != 'image/jpeg' or w < MINW or w / h < MINAR or w / h > 2.6:
            continue
        if not OK_LICENSE.match(lic.strip()) or BAD_TITLE.search(title):
            continue
        out.append({'title': title, 'width': w, 'height': h, 'license': lic, 'page': ii.get('descriptionurl'),
                    'author': clean((md.get('Artist') or {}).get('value')), 'query': query,
                    'cats': (md.get('Categories') or {}).get('value', '')})
    return out


def cmd_search():
    path = os.path.join(HERE, 'banner_candidates.json')
    cands = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
    for slug, queries in LANDMARKS.items():
        if cands.get(slug):
            continue                      # ค้นแล้ว (รันต่อจากเดิมได้)
        seen, found = set(), []
        for q in queries:
            try:
                for c in search(q):
                    if c['title'] not in seen:
                        seen.add(c['title']); found.append(c)
            except Exception as e:
                print('ERR', slug, q, e)
            time.sleep(1.5)
        cands[slug] = found[:8]
        print(slug, len(found), cands[slug][0]['title'] if cands[slug] else '-- ไม่พบ --', flush=True)
        json.dump(cands, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


GOOD = [(r'aerial|drone', 3.0), (r'sunrise|sunset|dusk|twilight|golden|evening|night', 2.0), (r'panorama|view|overview|skyline|landscape|lake|reflection|mist|fog|clouds', 1.5)]
BAD = r'interior|inside|detail|close|portrait|mural|painting|food|menu|truck|bus|airport|station|panoramio|crowd|people|monk|bird|frog|snake|butterfly|moth|flower|market|dish|selfie|night market'


def score(c, pos):
    t = c['title'].lower(); cats = c.get('cats', '')
    sc = 0.5 if pos < 3 else 0
    sc += 2 if c['width'] >= 4000 else 1.5 if c['width'] >= 2800 else 1 if c['width'] >= 2000 else 0
    ar = c['width'] / c['height']
    sc += 1.5 if 1.5 <= ar <= 2.4 else 0.5 if ar >= 1.3 else 0
    for pat, w in GOOD:
        if re.search(pat, t) or re.search(pat, cats.lower()):
            sc += w
    for pat, w in (('Featured pictures', 4), ('Quality images', 2.5), ('Valued images', 1.5), ('Aerial photographs', 2)):
        if pat.lower() in cats.lower():
            sc += w
    if re.search(BAD, t):
        sc -= 3
    return round(sc, 2)


def cmd_rank(slugs):
    """ค้นใหม่ด้วยคำค้นแนวมุมกว้าง/มุมสูง/พระอาทิตย์ขึ้น-ตก แล้วจัดอันดับภาพที่สวยและไกล (ซีเนมาติก) ขึ้นก่อน"""
    path = os.path.join(HERE, 'banner_candidates.json')
    cands = json.load(open(path, encoding='utf-8'))
    for slug in slugs:
        base = LANDMARKS[slug]
        qs = [base[0], base[0] + ' aerial drone', base[0] + ' sunrise sunset', (base[1] if len(base) > 1 else base[0]) + ' view panorama', base[0] + ' landscape']
        seen, found = set(), []
        for q in qs:
            try:
                for i, c in enumerate(search(q, 30)):
                    if c['title'] not in seen:
                        seen.add(c['title']); c['score'] = score(c, i); found.append(c)
            except Exception as e:
                print('ERR', slug, q, e)
            time.sleep(1.5)
        found.sort(key=lambda c: -c['score'])
        cands[slug] = found[:8]
        print(slug, len(found), [(c['score'], c['title'][5:40]) for c in found[:2]], flush=True)
        json.dump(cands, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def cmd_download(only):
    cands = json.load(open(os.path.join(HERE, 'banner_candidates.json'), encoding='utf-8'))
    cp = os.path.join(HERE, 'banner_choices.json')
    choices = json.load(open(cp, encoding='utf-8')) if os.path.exists(cp) else {}
    os.makedirs(OUT, exist_ok=True)
    credits_path = os.path.join(OUT, 'CREDITS.json')
    credits = json.load(open(credits_path, encoding='utf-8')) if os.path.exists(credits_path) else {}
    for slug in (only or LANDMARKS):
        lst = cands.get(slug, [])
        pick = next((c for c in lst if c['title'] == choices.get(slug)), None) if slug in choices else (lst[0] if lst else None)
        if pick is None:
            print('SKIP', slug, '(ไม่มีผู้สมัคร/ไฟล์ที่เลือกไม่อยู่ในรายการ)'); continue
        req = urllib.request.Request(thumb_url(pick['title']), headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        with open(os.path.join(OUT, slug + '.jpg'), 'wb') as f:
            f.write(data)
        credits[slug] = {k: pick[k] for k in ('title', 'author', 'license', 'page')}
        print('OK', slug, round(len(data) / 1024), 'KB', pick['title'], flush=True)
        time.sleep(1.5)
    json.dump(credits, open(credits_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'search':
        cmd_search()
    elif len(sys.argv) > 1 and sys.argv[1] == 'rank':
        cmd_rank(sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == 'download':
        cmd_download(sys.argv[2:])
    else:
        print(__doc__)
