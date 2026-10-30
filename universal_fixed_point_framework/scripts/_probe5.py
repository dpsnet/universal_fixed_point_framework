# -*- coding: utf-8 -*-
import json, io
s = json.load(io.open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_wd_m83e_desi137.json', encoding='utf-8'))
print('keys:', list(s.keys()))
v = s['samples']
print('samples type:', type(v).__name__, 'len:', len(v) if hasattr(v, '__len__') else 'n/a')
if isinstance(v, dict):
    k0 = list(v.keys())[0]
    print('first key:', k0)
    print('val:', repr(v[k0])[:400])
elif isinstance(v, list):
    print('first item:', repr(v[0])[:400])
