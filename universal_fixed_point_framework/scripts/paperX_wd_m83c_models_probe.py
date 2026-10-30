# -*- coding: utf-8 -*-
"""SVO2 模型列表探测——找 Tremblay/3D/其他白矮星网格"""
import urllib.request, re

def get(url, timeout=40):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

st, body = get('http://svo2.cab.inta-csic.es/theory/newov2/index.php')
# select 选项（模型下拉）
opts = re.findall(r'<option[^>]*value=[\'"]([^\'"]+)[\'"][^>]*>([^<]*)</option>', body)
print(f'=== select 选项 {len(opts)} ===')
for v, t in opts[:80]:
    print(f'  {v!r} -> {t.strip()[:60]}')

# 模型名（radio/checkbox）
mods = re.findall(r'name=[\'"]models?[\'"][^>]*value=[\'"]([^\'"]+)[\'"]', body)
print(f'\n=== models 值 ===')
print(sorted(set(mods))[:80])
