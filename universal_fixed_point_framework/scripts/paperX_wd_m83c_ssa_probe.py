# -*- coding: utf-8 -*-
"""M83c：SVO2 SSA 端点探测——Koester DA 网格检索"""
import urllib.request, json

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', errors='replace')

# 1) 服务描述（capabilities）
tests = [
    ('ssa.php capabilities', 'http://svo2.cab.inta-csic.es/theory/newov2/ssa.php?REQUEST=capabilities'),
    ('ssa queryData koester', 'http://svo2.cab.inta-csic.es/theory/newov2/ssa.php?REQUEST=queryData&COLLECTION=koester-dw&FORMAT=metadata'),
]
for name, url in tests:
    try:
        txt = get(url)
        print(f'=== {name} ===')
        print(txt[:1500])
        print()
    except Exception as e:
        print(f'=== {name} FAIL: {e} ===\n')
