# -*- coding: utf-8 -*-
"""M83a-3：稳健性分析
- 极端 5% 删除后 Spearman
- 中位数分位（分位回归思想——中位数斜率）
- 置换检验（B 洗牌——rho 零分布）
- 每档极端删除
"""
import json, numpy as np
from scipy import stats

BASE = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results'

def load(fn):
    with open(f'{BASE}\\{fn}', encoding='utf-8') as f:
        return json.load(f)

v10 = load('white_dwarf_analysis_v10_results.json')
v11 = load('white_dwarf_analysis_v11_gap_results.json')
stars = v10.get('weak', []) + v10.get('int', []) + v11.get('results', [])

eff = [r for r in stars if r.get('resid') is not None and r['total_EW'] > 0]
B = np.array([r['B_tesla'] for r in eff])
R = np.array([r['resid'] for r in eff])
n = len(eff)

# 1) 原始
rho0, p0 = stats.spearmanr(B, R)
print(f'原始: n={n} rho={rho0:.3f} p={p0:.2e}')

# 2) 极端 5% 删除（B 端和 R 端）
for frac, name in [(0.05, '5%'), (0.10, '10%')]:
    q_lo, q_hi = np.quantile(B, [frac, 1 - frac])
    qr_lo, qr_hi = np.quantile(R, [frac, 1 - frac])
    m = (B >= q_lo) & (B <= q_hi) & (R >= qr_lo) & (R <= qr_hi)
    rho, p = stats.spearmanr(B[m], R[m])
    print(f'删极端 {name}（B 和 R）: n={m.sum()} rho={rho:.3f} p={p:.2e}')

# 3) 置换检验（10000 次——B 洗牌）
rng = np.random.default_rng(42)
count = 0
NPERM = 10000
for _ in range(NPERM):
    Bp = rng.permutation(B)
    rp = stats.spearmanr(Bp, R).statistic
    if abs(rp) >= abs(rho0):
        count += 1
print(f'置换检验（10000 次）: p={count/NPERM:.5f}')

# 4) 每档删除极端后分档均值
print('\n分档（删 10% 极端残差）:')
for lo, hi, name in [(0, 1e3, '<1kT'), (1e3, 3e3, '1-3kT'), (3e3, 1e4, '3-10kT'), (1e4, 1e5, '10-100kT')]:
    m = (B >= lo) & (B < hi)
    if m.sum() >= 5:
        vals = R[m]
        ql, qh = np.quantile(vals, [0.1, 0.9])
        v2 = vals[(vals >= ql) & (vals <= qh)]
        print(f'  {name}: n={m.sum()} 原始均值 {np.mean(vals):+.3f} -> 删后 n={len(v2)} 均值 {np.mean(v2):+.3f}')

# 5) 加权 Spearman（log 档加权——n 不平衡校正）
from scipy.stats import rankdata
rb = rankdata(B)
rr = rankdata(R)
# 简单加权：每档 1/sqrt(n)
band_w = {}
for lo, hi in [(0, 1e3), (1e3, 3e3), (3e3, 1e4), (1e4, 1e5)]:
    cnt = sum(1 for b in B if lo <= b < hi)
    band_w[(lo, hi)] = 1.0 / np.sqrt(cnt) if cnt > 0 else 0
w = np.array([band_w[tuple(next((b2 for lo2, hi2 in [(0,1e3),(1e3,3e3),(3e3,1e4),(1e4,1e5)] if lo2 <= b < hi2), (0,1e3)))] for b in B])
# 加权 Spearman（近似——rank 相关系数加权）
rbc = rb - rb.mean()
rrc = rr - rr.mean()
rho_w = np.sum(w * rbc * rrc) / np.sqrt(np.sum(w * rbc**2) * np.sum(w * rrc**2))
print(f'\n加权 Spearman（档间 1/sqrt(n)）: rho={rho_w:.3f}')
