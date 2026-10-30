# -*- coding: utf-8 -*-
"""探查 EW 数据文件结构（A/B 判别用）"""
import json

BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'
for fn in ['paperX_wd_m83c_koester_ew.json', '_m83e_desi_ew.json']:
    try:
        with open(BASE + '\\' + fn, encoding='utf-8') as f:
            d = json.load(f)
        print('==== ' + fn + ' ====')
        if isinstance(d, dict):
            print('keys:', list(d.keys())[:20])
            for k in list(d.keys())[:2]:
                print(' ', k, '->', json.dumps(d[k], ensure_ascii=False)[:400])
        elif isinstance(d, list):
            print('len:', len(d))
            print('sample:', json.dumps(d[0], ensure_ascii=False)[:400] if d else None)
        print()
    except Exception as e:
        print(fn, 'ERR', e)
