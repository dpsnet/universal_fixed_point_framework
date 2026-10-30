# -*- coding: utf-8 -*-
import json, os
from collections import Counter

scripts = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts'

# n=9 判定表
with open(os.path.join(scripts, 'paperX_n9_base27_table.json'), encoding='utf-8') as f:
    t9 = json.load(f)
print("n9 top-level keys:", len(t9))

vals = set()
zero_keys = []
sym_pos_with_zero = Counter()
for k, v in t9.items():
    syms = k.split(',')
    for i, x in enumerate(syms):
        vals.add(x)
        if x == '0':
            sym_pos_with_zero[i] += 1
    if '0' in syms:
        zero_keys.append((k, v))
print("symbol values set:", vals)
print("keys containing 0:", len(zero_keys), "/", len(t9))
print("0 positions dist:", dict(sym_pos_with_zero))
# 示例含 0 键
for k, v in zero_keys[:5]:
    print("  key:", k, "->", v)
# bg 值分布（每键取 bg）
bgc = Counter()
for k, v in t9.items():
    bg = v['bg'] if isinstance(v, dict) else v
    bgc[int(bg)] += 1
print("bg dist:", dict(bgc))

# 基座顺序来源：n=9 minbasis 结果
mb = os.path.join(scripts, 'paperX_n9_minbasis_results.json')
if os.path.exists(mb):
    with open(mb, encoding='utf-8') as f:
        m = json.load(f)
    def dig(o, depth=0):
        if isinstance(o, dict):
            for key in ('basis', 'factors', 'chosen', 'base', 'tail'):
                if key in o:
                    print("n9 minbasis key:", key, "->", o[key] if not isinstance(o[key], (dict, list)) or len(str(o[key])) < 300 else str(o[key])[:300])
        return None
    dig(m)
    print("minbasis top keys:", list(m.keys()) if isinstance(m, dict) else type(m).__name__)
    for kk, vv in (list(m.items())[:8] if isinstance(m, dict) else []):
        print(" ", kk, ":", str(vv)[:200])
else:
    print("no minbasis results file")
