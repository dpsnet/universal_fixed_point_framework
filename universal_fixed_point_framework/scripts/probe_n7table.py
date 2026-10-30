# -*- coding: utf-8 -*-
import json
p = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n7_base16_table.json'
with open(p, encoding='utf-8') as f:
    t = json.load(f)
print('type:', type(t).__name__)
if isinstance(t, dict):
    items = list(t.items())[:3]
    for k, v in items:
        print('key:', repr(k)[:150])
        print('val:', repr(v)[:250])
    print('total entries:', len(t))
    # 值分布
    from collections import Counter
    c = Counter()
    for v in t.values():
        if isinstance(v, dict):
            c[v.get('bg', v)] += 1
        else:
            c[v] += 1
    print('value dist:', dict(c))
elif isinstance(t, list):
    print('first 3:', t[:3])
    print('len:', len(t))
