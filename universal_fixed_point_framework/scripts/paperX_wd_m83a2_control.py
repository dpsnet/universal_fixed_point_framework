# -*- coding: utf-8 -*-
"""M83a-2：Teff/log g 控制后 B 效应检验（多变量回归 + 分档控制）
- 星级口径（total_EW>0）
- 线性回归 resid ~ logB + Teff + logg——看 B 系数是否独立显著
- Teff 分档内看 B 梯度是否存活（大气效应排除）
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
print(f'星级有效样本: n={len(eff)}')

B = np.array([r['B_tesla'] for r in eff])
R = np.array([r['resid'] for r in eff])
Teff = np.array([r['Teff'] for r in eff])
logg = np.array([r.get('log_g', 8.0) for r in eff])

# 1) 单变量
rho, p = stats.spearmanr(B, R)
print(f'Spearman(B,resid): rho={rho:.3f} p={p:.2e}')

# 2) 多变量回归 resid ~ log10(B) + Teff + logg
X = np.column_stack([np.log10(B), Teff, logg])
Xc = X - X.mean(axis=0)
yc = R - R.mean()
# OLS
XtX = Xc.T @ Xc
XtXi = np.linalg.inv(XtX + np.eye(3) * 1e-9)
beta = XtXi @ Xc.T @ yc
yhat = Xc @ beta
resid = yc - yhat
s2 = resid @ resid / (len(yc) - 4)
se = np.sqrt(np.diag(XtXi * s2))
tvals = beta / se
print(f'\n回归 resid ~ log10(B)+Teff+logg:')
print(f'  beta(log10B) = {beta[0]:.4f} ± {se[0]:.4f}——t={tvals[0]:.2f} p={2*stats.t.sf(abs(tvals[0]), len(yc)-4):.2e}')
print(f'  beta(Teff)   = {beta[1]:.6f} ± {se[1]:.6f}——t={tvals[1]:.2f} p={2*stats.t.sf(abs(tvals[1]), len(yc)-4):.2e}')
print(f'  beta(logg)   = {beta[2]:.4f} ± {se[2]:.4f}——t={tvals[2]:.2f} p={2*stats.t.sf(abs(tvals[2]), len(yc)-4):.2e}')

# 3) Teff 分档内 B 梯度（大气效应排除）
print(f'\nTeff 分档内 B 梯度（Spearman）：')
for lo, hi, name in [(0, 12000, '<12kK'), (12000, 20000, '12-20kK'), (20000, 1e9, '>20kK')]:
    m = (Teff >= lo) & (Teff < hi)
    if m.sum() >= 8:
        rho2, p2 = stats.spearmanr(B[m], R[m])
        print(f'  {name}: n={m.sum()} rho={rho2:.3f} p={p2:.2e}')

# 4) 质量分档（log g 代理）
print(f'\nlog g 分档内 B 梯度：')
for lo, hi, name in [(0, 8.0, '<8.0'), (8.0, 8.8, '8.0-8.8'), (8.8, 1e9, '>8.8')]:
    m = (logg >= lo) & (logg < hi)
    if m.sum() >= 8:
        rho2, p2 = stats.spearmanr(B[m], R[m])
        print(f'  {name}: n={m.sum()} rho={rho2:.3f} p={p2:.2e}')

# 5) 弱场内部 B 梯度（<1kT 连续）
m = B < 1e3
if m.sum() >= 30:
    rho3, p3 = stats.spearmanr(B[m], R[m])
    print(f'\n弱场内部（<1kT, n={m.sum()}）B 梯度: rho={rho3:.3f} p={p3:.2e}')
