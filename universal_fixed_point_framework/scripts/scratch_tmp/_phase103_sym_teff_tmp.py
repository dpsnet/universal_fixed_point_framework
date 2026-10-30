# -*- coding: utf-8 -*-
"""查 Teff 字段值域 + 增量对称性（Teff 10-20kK 主档）"""
import json, statistics

with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs\paperX_wd_absflux_cal.json', encoding='utf-8') as f:
    data = json.load(f)
rows = data if isinstance(data, list) else data.get('rows', data.get('data', []))
print('total:', len(rows))
teffs = []
for r in rows:
    t = r.get('Teff')
    if t is not None:
        teffs.append(t)
print('Teff 样例:', teffs[:15])
print('Teff min/max:', min(teffs) if teffs else None, max(teffs) if teffs else None)
