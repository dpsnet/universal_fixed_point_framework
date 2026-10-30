# -*- coding: utf-8 -*-
"""M83c：完整表单 POST 测试（含 sbut/models）"""
import urllib.request, urllib.parse, re

def post(url, data, timeout=40):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'User-Agent': 'Mozilla/5.0',
                                                          'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

variants = [
    {'models': 'koester2', 'reqmodels[]': 'koester2',
     'params[koester2][teff][min]': '10000', 'params[koester2][teff][max]': '20000',
     'params[koester2][logg][min]': '7.0', 'params[koester2][logg][max]': '9.0',
     'nres': '50', 'sbut': 'Search'},
    {'reqmodels[]': 'koester2', 'nres': '50', 'boton': 'Search'},
    {'models': 'koester2', 'nres': '50', 'sbut': '1'},
]
for vi, data in enumerate(variants):
    try:
        st, body = post('http://svo2.cab.inta-csic.es/theory/newov2/index.php', data)
        # 检索结果特征：找模型条目 / VOTable / fits / spectral 链接
        markers = [m for m in ['VOTable', '.fits', 'spectra', 'Download', 'RESULTS', 'result'] if m.lower() in body.lower()]
        print(f'var{vi}: status={st} len={len(body)} markers={markers}')
        # 表格行（模型参数）
        rows = re.findall(r'<tr[^>]*>.*?</tr>', body, re.S)
        if rows and len(body) > 30000:
            print(f'  行数={len(rows)} 首行: {rows[0][:200].replace(chr(10)," ")}')
    except Exception as e:
        print(f'var{vi} FAIL: {e}')
