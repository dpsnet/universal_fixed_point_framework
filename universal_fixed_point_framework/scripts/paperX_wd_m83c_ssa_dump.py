# -*- coding: utf-8 -*-
"""SVO2 主页链接全量 dump"""
import urllib.request, re

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', errors='replace')

txt = get('http://svo2.cab.inta-csic.es/theory/newov2/')
print('len:', len(txt))
# 所有 href
ms = re.findall(r'href=[\'"]([^\'"]+)[\'"]', txt)
print('total hrefs:', len(ms))
for m in ms[:40]:
    print(' ', m)
# 搜 ssa/ssap/script 关键词上下文
for kw in ['ssa', 'SSA', 'script', 'protocol', 'Virtual Observatory']:
    idx = txt.find(kw)
    if idx >= 0:
        print(f'--- {kw} @ {idx}: ...{txt[max(0,idx-120):idx+180]}...')
