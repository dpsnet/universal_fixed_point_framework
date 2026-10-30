# -*- coding: utf-8 -*-
"""M83c：下载测试 + fid 参数表提取"""
import urllib.request, urllib.parse, re

def get(url, timeout=40):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

def post(url, data, timeout=40):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'User-Agent': 'Mozilla/5.0',
                                                          'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

# 1) 下载 fid=263 ascii 光谱
print('=== 下载测试 fid=263 ===')
st, body = get('http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=koester2&fid=263&format=ascii')
print(f'status={st} len={len(body)}')
print('head:', body[:400].replace('\n', ' | '))
print('tail:', body[-200:].replace('\n', ' | '))

# 2) 从结果页提取 fid + 参数（Teff/logg）
print('\n=== fid 参数表 ===')
data = {'models': 'koester2', 'reqmodels[]': 'koester2',
        'params[koester2][teff][min]': '10000', 'params[koester2][teff][max]': '20000',
        'params[koester2][logg][min]': '7.0', 'params[koester2][logg][max]': '9.0',
        'nres': '50', 'sbut': 'Search'}
st, body = post('http://svo2.cab.inta-csic.es/theory/newov2/index.php', data)
# 找每条光谱行：fid + teff + logg
# 常见结构：<tr>...ssap.php?model=koester2&fid=263...Teff...Logg...</tr>
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', body, re.S)
cnt = 0
for row in rows:
    fid = re.search(r'fid=(\d+)', row)
    if fid:
        txt = re.sub(r'<[^>]+>', '|', row)
        txt = re.sub(r'\|+', '|', txt)
        print(f'fid={fid.group(1)}: {txt[:150]}')
        cnt += 1
        if cnt >= 12:
            break
