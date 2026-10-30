# -*- coding: utf-8 -*-
"""M83c：Koester2 网格检索 POST 测试"""
import urllib.request, urllib.parse, re

def post(url, data, timeout=40):
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'User-Agent': 'Mozilla/5.0',
                                                          'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

# 1) Koester2 宽范围检索
data = {
    'reqmodels[]': 'koester2',
    'params[koester2][teff][min]': '10000',
    'params[koester2][teff][max]': '20000',
    'params[koester2][logg][min]': '7.0',
    'params[koester2][logg][max]': '9.0',
    'nres': '50',
}
st, body = post('http://svo2.cab.inta-csic.es/theory/newov2/index.php', data)
print(f'POST 检索: status={st} len={len(body)}')

# 找光谱条目/下载链接
found = []
for pat in [r'(?:http[^"\']*(?:fits|ascii|dat|spectra)[^"\']*)', r'(?:download|get|retrieve)[^"\']*',
            r'ssa:Access[^<]*', r'Access\.Reference[^<]*', r'(?:teff|logg)[^<]{0,60}']:
    ms = re.findall(pat, body, re.I)
    print(f'--- {pat}: {len(ms)}')
    for m in ms[:6]:
        print('   ', m[:150])
    found.extend(ms[:6])

# 保存页面供分析
with open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/_m83c_ko2_search.html', 'w', encoding='utf-8') as f:
    f.write(body)
print('\n页面已保存 _m83c_ko2_search.html')
