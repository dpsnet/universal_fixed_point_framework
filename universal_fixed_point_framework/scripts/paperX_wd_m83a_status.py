# -*- coding: utf-8 -*-
"""P83 M83a 前置：v10/v11 白矮星残差现状统计"""
import json, numpy as np

BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results'

def load(fn):
    d = json.load(open(f'{BASE}\\{fn}', encoding='utf-8'))
    return d.get('results', d) if isinstance(d, dict) else d

# v11 gap（1e3-1e4 T）
rs = load('white_dwarf_analysis_v11_gap_results.json')
eff = [r for r in rs if r.get('resid') is not None and r['total_EW'] > 0]
print(f'v11 gap: 成功 {len(rs)} 有效(EW>0) {len(eff)}')
for lo, hi, name in [(1e3, 3e3, '1-3kT'), (3e3, 5e3, '3-5kT'), (5e3, 7e3, '5-7kT'), (7e3, 1e4, '7-10kT')]:
    band = [r['resid'] for r in eff if lo <= r['B_tesla'] < hi]
    if band:
        print(f'  {name}: n={len(band)} 残差均值 {np.mean(band):+.3f} dex')

# v10（弱场 + 中场）
v10d = json.load(open(f'{BASE}\\white_dwarf_analysis_v10_results.json', encoding='utf-8'))
rs10 = v10d.get('weak', []) + v10d.get('int', [])
weff = [r for r in rs10 if r.get('resid') is not None and r['total_EW'] > 0 and r['B_tesla'] < 1e3]
inter = [r for r in rs10 if r.get('resid') is not None and r['total_EW'] > 0 and 1e4 <= r['B_tesla'] < 1e5]
if weff:
    wr = np.array([r['resid'] for r in weff])
    print(f'\nv10 弱场(<1kT): n={len(weff)} 残差 {np.mean(wr):+.3f} ± {np.std(wr):.3f} dex')
if inter:
    ir = np.array([r['resid'] for r in inter])
    print(f'v10 中场(10-100kT): n={len(inter)} 残差 {np.mean(ir):+.3f} ± {np.std(ir):.3f} dex')
    if weff:
        diff = np.mean(ir) - np.mean(wr)
        se = np.sqrt(np.var(ir)/len(ir) + np.var(wr)/len(wr))
        print(f'差异 {diff:+.3f} dex——t 值 {diff/se:.2f}——辐射缺失 {(1-10**diff)*100:.1f}%')

# 全 B 梯度（合并 v10 + v11 中场带）
all_eff = weff + eff + inter
Bs = np.array([r['B_tesla'] for r in all_eff])
Rs = np.array([r['resid'] for r in all_eff])
print(f'\n全样本: n={len(all_eff)}')
for lo, hi, name in [(0, 1e3, '<1kT'), (1e3, 3e3, '1-3kT'), (3e3, 1e4, '3-10kT'), (1e4, 1e5, '10-100kT')]:
    m = (Bs >= lo) & (Bs < hi)
    if m.sum():
        print(f'  {name}: n={m.sum()} 残差 {np.mean(Rs[m]):+.3f} ± {np.std(Rs[m]):.3f}')

# Spearman 相关（B vs 残差）
from scipy.stats import spearmanr
try:
    rho, p = spearmanr(Bs, Rs)
    print(f'\nSpearman(B, resid): rho={rho:.3f} p={p:.2e}')
except Exception as e:
    print('spearman fail:', e)
