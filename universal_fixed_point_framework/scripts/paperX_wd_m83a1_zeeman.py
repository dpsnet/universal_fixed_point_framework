# -*- coding: utf-8 -*-
"""M83a-1：Zeeman 线系诊断（C 路径）
- 逐线（Hα/Hβ/Hγ）独立测 EW——按 B 分档比较各线残差梯度
- Zeeman 分裂对 Hα（最大波长/最大展宽）影响最强——若梯度仅 Hα 显著 → Zeeman 伪影；全线一致 → 非 Zeeman
- 现有数据零新依赖
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

print('=== 线系诊断：单线 EW 相对强度（EW_line / theo_EW_total）按 B 分档 ===')
for line in LINES:
    row = []
    for lo, hi, name in BANDS:
        vals = []
        for r in stars:
            if not (r.get('B_tesla') and lo <= r['B_tesla'] < hi):
                continue
            br = r.get('balmer_results', {})
            ew = br.get(line, {}).get('EW')
            det = br.get(line, {}).get('detected')
            theo = r.get('theo_EW')
            if ew is None or theo is None or not det or theo <= 0:
                continue
            vals.append(ew / theo)
        if vals:
            row.append('{name}: n={n} 均值 {m:.3f}'.format(name=name, n=len(vals), m=np.mean(vals)))
        else:
            row.append('{name}: n=0'.format(name=name))
    print(line + ': ' + ' | '.join(row))

print()
print('=== 线级 B 相关（Spearman）===')
for line in LINES:
    Bs, Is = [], []
    for r in stars:
        br = r.get('balmer_results', {})
        ew = br.get(line, {}).get('EW')
        det = br.get(line, {}).get('detected')
        theo = r.get('theo_EW')
        if ew is None or theo is None or not det or theo <= 0:
            continue
        Bs.append(r['B_tesla'])
        Is.append(ew / theo)
    if len(Bs) >= 10:
        rho, p = spearmanr(Bs, Is)
        print('{line}: n={n} rho={rho:.3f} p={p:.2e}'.format(line=line, n=len(Bs), rho=rho, p=p))

Bs, Is = [], []
for r in stars:
    if r.get('total_EW', 0) > 0 and r.get('theo_EW'):
        Bs.append(r['B_tesla'])
        Is.append(r['total_EW'] / r['theo_EW'])
rho, p = spearmanr(Bs, Is)
print()
print('总EW: n={n} rho={rho:.3f} p={p:.2e}'.format(n=len(Bs), rho=rho, p=p))
