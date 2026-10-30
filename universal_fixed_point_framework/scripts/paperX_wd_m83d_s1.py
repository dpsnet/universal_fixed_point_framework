# -*- coding: utf-8 -*-
"""Kepler 2013 全表下载 + 筛选（扩样本 M83d）"""
import urllib.request, json

url = 'http://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/MNRAS/429/2934&-out.max=600&-out.all'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=60) as r:
    t = r.read().decode('utf-8', errors='replace')

open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/_kepler2013_full.tsv', 'w', encoding='utf-8').write(t)

# 解析 TSV（跳过 # 注释，表头 = 列行）
lines = [l for l in t.splitlines() if l and not l.startswith('#')]
# 表头行定位：含 SDSS 与 Plate
hdr_i = None
for i, l in enumerate(lines):
    if 'SDSS' in l and 'Plate' in l and 'Teff' in l:
        hdr_i = i
        break
if hdr_i is None:
    print('FAIL: 找不到表头')
    raise SystemExit
headers = [h.strip() for h in lines[hdr_i].split('\t')]
print('列:', headers)
rows = []
for l in lines[hdr_i+1:]:
    cells = l.split('\t')
    if len(cells) >= len(headers) and cells[0].strip().isdigit():
        rows.append(dict(zip(headers, cells)))
print(f'总行数: {len(rows)}')

# 统计
def fnum(r, k):
    try:
        return float(str(r.get(k, '')).strip())
    except (TypeError, ValueError):
        return None

n_B = sum(1 for r in rows if fnum(r, 'BHa') is not None)
n_Teff = sum(1 for r in rows if fnum(r, 'Teff') is not None)
print(f'有 BHa: {n_B}，有 Teff: {n_Teff}')
Bs = [fnum(r, 'BHa') for r in rows if fnum(r, 'BHa') is not None]
print(f'BHa 范围: {min(Bs):.1f} - {max(Bs):.1f} MG')

# 保存全表（JSON）
with open('E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_wd_m83d_kepler2013.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False)
print('DONE -> paperX_wd_m83d_kepler2013.json')
