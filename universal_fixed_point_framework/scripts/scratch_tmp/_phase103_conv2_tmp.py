# -*- coding: utf-8 -*-
"""Phase 103e: 查 P3b 压缩/机制 json 的现成曲线"""
import json
BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'
for fn in ['_phase100_p3b_compression.json', '_phase100_p3b2_open_items.json', '_phase100_p3c_pi_retention.json']:
    try:
        with open(BASE + '\\' + fn, encoding='utf-8') as f:
            d = json.load(f)
        print('==== ' + fn + ' ====')
        s = json.dumps(d, ensure_ascii=False)
        print('keys:', list(d.keys())[:15] if isinstance(d, dict) else type(d).__name__)
        print(s[:1200])
        print()
    except Exception as e:
        print(fn, 'ERR', e)
