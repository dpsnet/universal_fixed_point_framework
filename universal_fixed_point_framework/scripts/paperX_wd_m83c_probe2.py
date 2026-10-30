# -*- coding: utf-8 -*-
"""M83c：SVO2 Koester 网格对接——端点批量探测
1) VO Registry 查 SVO2 SSA 服务端点
2) SVO2 常见端点变体
"""
import urllib.request, re, json

def get(url, timeout=25):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

# 1) VO Registry 搜索 SVO2 服务
reg_urls = [
    'http://registry.ivoa.net/search?keywords=SVO2',
    'http://vao.stsci.edu/directory/search.aspx?keywords=SVO2',
]
for u in reg_urls:
    try:
        st, body = get(u)
        print(f'=== Registry {u} status={st} len={len(body)}')
        # 找 ssa / accessURL
        for kw in ['ssa', 'accessURL', 'SVO2']:
            ms = re.findall(r'[Hh][Tt][Tt][Pp][Ss]?://[^"\'<> ]*', body)
            hits = [m for m in ms if 'svo2' in m.lower() or 'ssa' in m.lower()]
            if hits:
                print(f'  {kw}: {hits[:5]}')
    except Exception as e:
        print(f'=== Registry {u} FAIL: {e}')

# 2) SVO2 端点变体探测
endpoints = [
    'http://svo2.cab.inta-csic.es/theory/newov2/ssa.php',
    'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php',
    'http://svo2.cab.inta-csic.es/theory/newov2/ssa_service.php',
    'http://svo2.cab.inta-csic.es/theory/newov2/api/spectra',
    'http://svo2.cab.inta-csic.es/theory/newov2/api/koester',
    'http://svo2.cab.inta-csic.es/theory/newov2/scripts/ssa.php',
    'http://svo2.cab.inta-csic.es/theory/newov2/koester-dw/index.html',
    'http://svo2.cab.inta-csic.es/theory/newov2/koester_dw.html',
    'http://svo2.cab.inta-csic.es/theory/newov2/?models=koester-dw',
    'http://svo2.cab.inta-csic.es/theory/newov2/ssa_help.php',
]
print('\n=== SVO2 端点探测 ===')
for u in endpoints:
    try:
        st, body = get(u)
        print(f'{st}  {u}  len={len(body)}')
        if st == 200 and len(body) > 500 and 'ssa' in body.lower():
            # 找 SSA 端点线索
            for m in re.findall(r'(?:ssa|ssap)[a-z_]*\.php[^"\']*', body.lower())[:3]:
                print(f'    -> {m}')
    except Exception as e:
        print(f'FAIL {u}  ({type(e).__name__}: {e})')
