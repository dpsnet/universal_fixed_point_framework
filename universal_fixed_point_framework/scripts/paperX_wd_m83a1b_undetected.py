# -*- coding: utf-8 -*-
"""M83a-1b：Zeeman 诊断补充——含未检测线（选择偏差排除）
- 未检测 → EW=0 计入——避免"只有强线进入"偏差
- 逐线（detected 或 0）按 B 分档强度 + Spearman
"""
import json, numpy as np
from scipy.stats import spearmanr

BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results'

def load(fn):
    with open(f'{BASE}\\{fn}', encoding='utf-8') as f:
        return json.load(f)

v10 = load('white_dwarf_analysis_v10_results.json')
v11 = load('white_dwarf_analysis_v11_gap_results.json')
stars = v10.get('weak', []) + v10.get('int', []) + v11.get('results', [])

LINES = ['Hα', 'Hβ', 'Hγ', 'Hδ', 'Hε']
BANDS = [(0, 1e3, '<1kT'), (1e3, 3e3, '1-3kT'), (3e3, 1e4, '3-10kT'), (1e4, 1e5, '10-100kT')]

print('=== 含未检测（EW=0）：单线强度均值按 B 分档 ===')
for line in LINES:
    row = []
    for lo, hi, name in BANDS:
        vals = []
        for r in stars:
            if not (r.get('B_tesla') and lo <= r['B_tesla'] < hi):
                continue
            br = r.get('balmer_results', {})
            ew = br.get(line, {}).get('EW', 0.0)
            if ew is None:
                ew = 0.0
            theo = r.get('theo_EW')
            if theo is None or theo <= 0:
                continue
            vals.append(ew / theo)
        if vals:
            row.append('{name}: n={n} 均值 {m:.4f}'.format(name=name, n=len(vals), m=np.mean(vals)))
        else:
            row.append('{name}: n=0'.format(name=name))
    print(line + ': ' + ' | '.join(row))

print()
print('=== 含未检测：线级 B 相关（Spearman）===')
for line in LINES:
    Bs, Is = [], []
    for r in stars:
        br = r.get('balmer_results', {})
        ew = br.get(line, {}).get('EW', 0.0)
        if ew is None:
            ew = 0.0
        theo = r.get('theo_EW')
        if theo is None or theo <= 0:
            continue
        Bs.append(r['B_tesla'])
        Is.append(ew / theo)
    if len(Bs) >= 10:
        rho, p = spearmanr(Bs, Is)
        print('{line}: n={n} rho={rho:.3f} p={p:.2e}'.format(line=line, n=len(Bs), rho=rho, p=p))
