# -*- coding: utf-8 -*-
"""M83c-TMAP：探测 TMAP 模型标识 + 检索热端网格"""
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

# 1) 主页找 TMAP 模型标识
st, body = get('http://svo2.cab.inta-csic.es/theory/newov2/?models=koester2')
tmap_ids = re.findall(r'index\.php\?models=([a-z0-9_]+)', body)
print('主页模型标识:', sorted(set(tmap_ids)))

# 2) 试 TMAP 检索（猜标识）
for mid in ['tmap', 'tmap2', 'tmap1', 'tmap-grid2', 'tmap_g2']:
    data = {'models': mid, 'reqmodels[]': mid,
            'params[' + mid + '][teff][min]': '20000', 'params[' + mid + '][teff][max]': '40000',
            'nres': '20', 'sbut': 'Search'}
    try:
        st, b = post('http://svo2.cab.inta-csic.es/theory/newov2/index.php', data)
        n_rows = len(re.findall(r'fid=(\d+)', b))
        print(f'{mid}: status={st} len={len(b)} fid 数={n_rows}')
        if n_rows > 0:
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', b, re.S)
            for row in rows[:3]:
                if 'fid=' in row:
                    txt = re.sub(r'<[^>]+>', '|', row)
                    print('    ', txt[:120])
    except Exception as e:
        print(f'{mid} FAIL: {e}')
    time.sleep(0.5)
