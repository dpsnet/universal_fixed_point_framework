# -*- coding: utf-8 -*-
"""探查 m83c 样本字段 + gaia_abs 标识字段"""
import json

BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'
with open(BASE + '\\paperX_wd_m83c_koester_ew.json', encoding='utf-8') as f:
    d = json.load(f)
s0 = d['samples'][0]
print('m83c samples[0] keys:', list(s0.keys()))
print('sample0:', json.dumps(s0, ensure_ascii=False)[:600])
print()
# 找有 koester 的样本
for s in d['samples']:
    if s.get('koester_ew') is not None or s.get('obs_ew') is not None:
        print('sample w/ koester:', json.dumps(s, ensure_ascii=False)[:600])
        break

with open(BASE + r'\_gaia_abs\paperX_wd_absflux_cal.json', encoding='utf-8') as f:
    g = json.load(f)
rows = g if isinstance(g, list) else g.get('rows', g.get('data', []))
print()
print('gaia_abs rows:', len(rows))
print('gaia_abs row0 keys:', list(rows[0].keys()))
print('row0:', json.dumps(rows[0], ensure_ascii=False)[:600])
