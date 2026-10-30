# -*- coding: utf-8 -*-
"""M83c 步骤2：分块检索 Koester2 网格 -> 完整 fid<->(Teff,logg) 表"""
import urllib.request, urllib.parse, re, json, time

def post(url, data, timeout=40):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'User-Agent': 'Mozilla/5.0',
                                                          'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

def get(url, timeout=40):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

# 分块检索：Teff 每 10000K 一块（避免 nres 截断）
chunks = [(5000, 15000), (15000, 25000), (25000, 35000), (35000, 45000), (45000, 55000), (55000, 70000)]
fid_table = {}  # (teff, logg) -> fid
for lo, hi in chunks:
    data = {'models': 'koester2', 'reqmodels[]': 'koester2',
            'params[koester2][teff][min]': str(lo), 'params[koester2][teff][max]': str(hi),
            'params[koester2][logg][min]': '7.0', 'params[koester2][logg][max]': '10.0',
            'nres': '500', 'sbut': 'Search'}
    try:
        st, body = post('http://svo2.cab.inta-csic.es/theory/newov2/index.php', data)
        # 解析行：fid + teff + logg
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', body, re.S)
        n = 0
        for row in rows:
            fidm = re.search(r'fid=(\d+)', row)
            if not fidm:
                continue
            txt = re.sub(r'<[^>]+>', '|', row)
            cells = [c.strip() for c in txt.split('|') if c.strip()]
            # cells: [..., Koester WD models, TEFF, LOGG, VOtable, ASCII]
            if len(cells) >= 4:
                try:
                    teff = int(float(cells[-4] if cells[-4].replace('.','').isdigit() else cells[-5]))
                except Exception:
                    continue
                try:
                    logg = float(cells[-3] if cells[-3].replace('.','').isdigit() else cells[-4])
                except Exception:
                    continue
                if 5000 <= teff <= 70000 and 7.0 <= logg <= 10.0:
                    fid_table[(teff, logg)] = int(fidm.group(1))
                    n += 1
        print(f'chunk {lo}-{hi}: {n} 光谱条目')
    except Exception as e:
        print(f'chunk {lo}-{hi} FAIL: {e}')
    time.sleep(0.5)

print(f'\n总网格点: {len(fid_table)}')
teffs = sorted(set(t for t, g in fid_table))
print(f'Teff 网格: {teffs[:6]} ... {teffs[-4:]}（{len(teffs)} 个值）')
loggs = sorted(set(g for t, g in fid_table))
print(f'logg 网格: {loggs}')

with open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_wd_m83c_fid_table.json', 'w', encoding='utf-8') as f:
    json.dump({f'{t}_{g}': fid for (t, g), fid in fid_table.items()}, f, ensure_ascii=False, indent=1)
print('DONE -> paperX_wd_m83c_fid_table.json')
