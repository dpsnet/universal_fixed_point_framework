# -*- coding: utf-8 -*-
import json, os
scripts = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'

with open(os.path.join(scripts, 'paperX_n9_minbasis_results.json'), encoding='utf-8') as f:
    m = json.load(f)
print("tail_set:", m['tail_set'])
print("tail_count:", m['tail_count'])
print("remove_set:", m['remove_set'])

# 补因子顺序：查 verify2 脚本或 final_summary
for fn in ['paperX_n9_verify2.py', 'paperX_n9_final_summary.json']:
    p = os.path.join(scripts, fn)
    if os.path.exists(p):
        print("=====", fn, "=====")
        if fn.endswith('.json'):
            with open(p, encoding='utf-8') as f:
                d = json.load(f)
            print(str(d)[:1500])
        else:
            with open(p, encoding='utf-8') as f:
                s = f.read()
            for kw in ['base', 'basis', 's1_2345', 's123_456789', 'factors', 'pad', '补']:
                idx = 0
                while True:
                    i = s.find(kw, idx)
                    if i < 0:
                        break
                    print("...", s[max(0, i-80):i+160].replace("\n", " "))
                    idx = i + 1
                    if idx > len(s):
                        break
