# -*- coding: utf-8 -*-
import json
for n, p in [("n8", r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n8_base23_table.json'),
             ("n9", r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n9_base27_table.json')]:
    with open(p, encoding='utf-8') as f:
        t = json.load(f)
    print("=====", n, "=====")
    print('top keys:', list(t.keys()) if isinstance(t, dict) else type(t).__name__)
    if isinstance(t, dict) and 'basis' in t:
        print('basis len:', len(t['basis']))
        print('basis:', t['basis'][:5], '...')
    tbl = t['table'] if isinstance(t, dict) and 'table' in t else t
    items = list(tbl.items())[:3]
    for k, v in items:
        print('key:', repr(k)[:200])
        print('val:', repr(v)[:100])
    print('total entries:', len(tbl))
    from collections import Counter
    c = Counter()
    for v in tbl.values():
        try:
            c[int(v)] += 1
        except Exception:
            c[repr(v)] += 1
    print('value dist:', dict(c))
