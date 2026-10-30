# -*- coding: utf-8 -*-
"""M83c：主页 JS/API 提取 v2"""
import urllib.request, re

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

st, body = get('http://svo2.cab.inta-csic.es/theory/newov2/?models=koester-dw')
print(f'主页 len={len(body)}')

# 所有 js/php 引用
for pat in [r'[Ss][Rr][Cc]\s*=\s*[\'"]([^\'"]+)[\'"]', r'[Hh][Rr][Ee][Ff]\s*=\s*[\'"]([^\'"]+\.(?:php|js|py)[^\'"]*)[\'"]']:
    for m in re.findall(pat, body)[:20]:
        print('  REF:', m)

# fetch/ajax/XMLHttpRequest 上下文
for kw in ['fetch', 'ajax', 'XMLHttpRequest', 'ssap', 'ssa', 'POST', 'action=', 'koester']:
    cnt = body.lower().count(kw.lower())
    print(f'  [{kw}] 出现 {cnt} 次')
    if cnt:
        i = body.lower().find(kw.lower())
        print(f'    首现上下文: ...{body[max(0,i-100):i+150].replace(chr(10)," ")}...')
