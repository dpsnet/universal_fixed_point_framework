# -*- coding: utf-8 -*-
"""M83c-TMAP：tmap2 分块检索 fid 表（热端复核）"""
import urllib.request, urllib.parse, re, json, time

def post(url, data, timeout=40):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'User-Agent': 'Mozilla/5.0',
                                                          'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

chunks = [(20000, 30000), (30000, 40000), (40000, 50000), (50000, 70000)]
fid_table = {}
for lo, hi in chunks:
    data = {'models': 'tmap2', 'reqmodels[]': 'tmap2',
            'params[tmap2][teff][min]': str(lo), 'params[tmap2][teff][max]': str(hi),
            'params[tmap2][logg][min]': '7.0', 'params[tmap2][logg][max]': '9.5',
            'nres': '500', 'sbut': 'Search'}
    try:
        st, body = post('http://svo2.cab.inta-csic.es/theory/newov2/index.php', data)
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', body, re.S)
        n = 0
        for row in rows:
            fidm = re.search(r'fid=(\d+)', row)
            if not fidm:
                continue
            txt = re.sub(r'<[^>]+>', '|', row)
            cells = [c.strip() for c in txt.split('|') if c.strip()]
            # cells 结构探测：找 teff/logg
            teff = logg = None
            for j, c in enumerate(cells):
                if c.isdigit() and 10000 <= int(c) <= 200000:
                    teff = int(c)
                    # logg 在 teff 后 1-3 格
                    for k in range(j+1, min(j+4, len(cells))):
                        try:
                            g = float(cells[k])
                            if 6.0 <= g <= 10.0:
                                logg = g
                                break
                        except ValueError:
                            continue
                    break
            if teff and logg:
                fid_table[(teff, logg)] = int(fidm.group(1))
                n += 1
        print(f'chunk {lo}-{hi}: {n} 条目')
    except Exception as e:
        print(f'chunk {lo}-{hi} FAIL: {e}')
    time.sleep(0.5)

print(f'\n总网格点: {len(fid_table)}')
teffs = sorted(set(t for t, g in fid_table))
print(f'Teff: {teffs[:5]}...{teffs[-5:]}（{len(teffs)} 值）')
loggs = sorted(set(g for t, g in fid_table))
print(f'logg: {loggs}')
with open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_wd_m83c_tmap_fid.json', 'w', encoding='utf-8') as f:
    json.dump({f'{t}_{g}': fid for (t, g), fid in fid_table.items()}, f, ensure_ascii=False, indent=1)
print('DONE')
