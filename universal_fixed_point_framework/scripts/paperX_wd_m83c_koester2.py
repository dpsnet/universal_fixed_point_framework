# -*- coding: utf-8 -*-
"""M83c：koester2 页面提取——找检索表单/下载接口"""
import urllib.request, re

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

st, body = get('http://svo2.cab.inta-csic.es/theory/newov2/index.php?models=koester2')
print(f'koester2 页面 len={len(body)}')

# 找表单/选择器/下载按钮
for pat in [r'<form[^>]*>', r'action=[\'"][^\'"]*[\'"]', r'name=[\'"](?:Teff|logg|logg?|mass|parameter)[\'"]',
            r'<select[^>]*>', r'(?:Download|download|ascii|VOTable|votable)[^<]{0,40}']:
    ms = re.findall(pat, body)
    print(f'\n--- {pat}: {len(ms)} ---')
    for m in ms[:12]:
        print('  ', m[:120])

# 找光谱检索脚本（可能有 grid 参数选择 -> 提交 URL）
for kw in ['getspectrum', 'get_spectrum', 'spectrum.php', 'retrieve', 'download.php', 'spectra']:
    cnt = body.lower().count(kw)
    if cnt:
        i = body.lower().find(kw)
        print(f'\n[{kw}] x{cnt}: ...{body[max(0,i-80):i+120].replace(chr(10)," ")}...')
