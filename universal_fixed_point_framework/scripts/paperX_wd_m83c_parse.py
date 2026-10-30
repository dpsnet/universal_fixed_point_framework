# -*- coding: utf-8 -*-
"""M83c：解析 Koester2 检索结果——光谱条目 + 下载链接"""
import urllib.request, urllib.parse, re

def post(url, data, timeout=40):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'User-Agent': 'Mozilla/5.0',
                                                          'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

data = {'models': 'koester2', 'reqmodels[]': 'koester2',
        'params[koester2][teff][min]': '10000', 'params[koester2][teff][max]': '20000',
        'params[koester2][logg][min]': '7.0', 'params[koester2][logg][max]': '9.0',
        'nres': '50', 'sbut': 'Search'}
st, body = post('http://svo2.cab.inta-csic.es/theory/newov2/index.php', data)
open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/_m83c_result.html', 'w', encoding='utf-8').write(body)

# 找模型光谱条目（VOTable 行 / 下载 URL / Teff-logg 对）
print('=== VOTable 链接 / 下载 ===')
for pat in [r'[Hh][Rr][Ee][Ff]\s*=\s*[\'"]([^\'"]*(?:votable|fits|dat|ascii|spectrum|spectra)[^\'"]*)[\'"]',
            r'([A-Za-z0-9_./:-]+\.(?:fits|dat|ascii|txt)(?:\?[^\'">]*)?)',
            r'[Hh][Rr][Ee][Ff]\s*=\s*[\'"]([^\'"]+)[\'"]']:
    ms = re.findall(pat, body, re.I)
    print(f'--- {pat[:40]}: {len(ms)}')
    for m in ms[:15]:
        print('   ', str(m)[:140])

# Teff/logg 值对
print('\n=== 光谱参数行（Teff/logg）===')
pairs = re.findall(r'([Tt]eff[^<]*?<[^>]*>)?\s*([0-9]{4,6})\s*[Kk]?\s*[^<]{0,20}\s*(?:logg?|log g|gravity)[^<]*?<[^>]*>\s*([0-9]\.[0-9])', body)
for p in pairs[:10]:
    print('   ', p)
