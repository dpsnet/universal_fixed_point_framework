# -*- coding: utf-8 -*-
"""M83c：ssap.php 参数探测 + 主页 JS API 提取"""
import urllib.request, re

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

# 1) ssap.php 参数探测
tests = [
    'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?REQUEST=queryData&FORMAT=metadata',
    'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?REQUEST=queryData&COLLECTION=koester-dw',
    'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?REQUEST=capabilities',
    'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?REQUEST=queryData&TARGETCLASS=STAR&COLLECTION=koester-dw',
]
print('=== ssap.php 参数探测 ===')
for u in tests:
    try:
        st, body = get(u)
        print(f'{st}  len={len(body)}  {u}')
        if len(body) > 50:
            print(f'    head: {body[:200].replace(chr(10), " ")}')
    except Exception as e:
        print(f'FAIL {u}  ({e})')

# 2) 主页 JS API 提取
print('\n=== 主页 JS/API 提取 ===')
st, body = get('http://svo2.cab.inta-csic.es/theory/newov2/?models=koester-dw')
# 找 js 文件
for m in re.findall(r'[Ss][Rr][Cc]\s*=\s*[\'"]([^\'"]+\.js[^\'"]*)[\'"]', body)[:10]:
    print('  JS:', m)
# 找 fetch/ajax/api 关键词
for kw in ['fetch(', 'api', 'ajax', 'ssap', 'ssa.php', 'service']:
    for m in re.finditer(kw, body, re.I):
        i = m.start()
        ctx = body[max(0, i-80):i+120].replace('\n', ' ')
        print(f'  [{kw}] ...{ctx}...')
        break
# 找表单/输入
for m in re.findall(r'<form[^>]*>', body)[:5]:
    print('  FORM:', m)
