# -*- coding: utf-8 -*-
"""M83c 步骤4：Koester EW 残差分析——重算 beta(log10B) + 与 M83a-2 对比"""
import json, os, sys
import numpy as np

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'

with open(base + '/scripts/paperX_wd_m83c_koester_ew.json', encoding='utf-8') as f:
    data = json.load(f)
samples = data['samples']
print(f'样本 {data["n_samples"]}——含 Koester EW {data["n_with_koester"]}')

# 有效样本（有 koester_EW）
S = [s for s in samples if s.get('koester_EW')]
print(f'有效 {len(S)}')

if not S:
    print('无有效样本——退出')
    sys.exit(0)

# 残差口径：log10(obs/koester)——B-残差
for s in S:
    obs = s['obs_EW']
    ko = s['koester_EW']
    s['resid_ko'] = np.log10(obs / ko) if (ko and obs > 0) else None
    s['log10B'] = np.log10(s['B_tesla'])

S2 = [s for s in S if s.get('resid_ko') is not None]
print(f'残差有效 {len(S2)}')

log10B = np.array([s['log10B'] for s in S2])
resid = np.array([s['resid_ko'] for s in S2])
Teff = np.array([s['Teff'] for s in S2])
logg = np.array([s['logg'] for s in S2])

# 1) Spearman
from scipy import stats
rho, p = stats.spearmanr(log10B, resid)
print(f'\n=== Koester EW 残差 vs log10B ===')
print(f'Spearman rho = {rho:.3f}, p = {p:.2e}')

# 2) 多变量回归（同 M83a-2 口径）
X = np.column_stack([np.ones(len(S2)), log10B, Teff, logg])
beta, res, rank, sv = np.linalg.lstsq(X, resid, rcond=None)
n = len(S2)
k = X.shape[1]
dof = n - k
sse = float(np.sum((resid - X @ beta) ** 2))
se = np.sqrt(sse / dof)
XtX_inv = np.linalg.inv(X.T @ X)
se_beta = np.sqrt(np.diag(XtX_inv)) * se
t_vals = beta / se_beta
from scipy import stats as st
p_vals = 2 * (1 - st.t.cdf(np.abs(t_vals), dof))
print(f'多变量回归（log10B、Teff、logg）:')
for nm, b, sb, t, pv in zip(['const', 'log10B', 'Teff', 'logg'], beta, se_beta, t_vals, p_vals):
    print(f'  {nm}: beta={b:.4f}±{sb:.4f}, t={t:.2f}, p={pv:.2e}')

# 3) Teff 分档（同 M83a-2 口径：<1万 / 1-2万 / >2万）
bins = [0, 10000, 20000, 1e9]
labels = ['<10k', '10-20k', '>20k']
for lb, lo, hi in zip(labels, bins[:-1], bins[1:]):
    m = (Teff >= lo) & (Teff < hi)
    if np.sum(m) >= 10:
        r2, p2 = stats.spearmanr(log10B[m], resid[m])
        print(f'  Teff {lb} (n={np.sum(m)}): rho={r2:.3f}, p={p2:.2e}')
    else:
        print(f'  Teff {lb} (n={np.sum(m)}): 样本不足')

# 4) 分档残差（B 分档——同 M83a-3 口径）
bl = np.array([s['B_tesla'] for s in S2])
edges = [0, 1000, 3000, 10000, 1e9]
for lo, hi in zip(edges[:-1], edges[1:]):
    m = (bl >= lo) & (bl < hi)
    if np.sum(m) >= 5:
        print(f'  B {lo}-{hi} (n={np.sum(m)}): 残差均值 {np.mean(resid[m]):.3f}±{np.std(resid[m]):.3f}')

# 5) 保存
out = {'n': len(S2), 'rho': float(rho), 'p': float(p),
       'beta': {nm: float(b) for nm, b in zip(['const', 'log10B', 'Teff', 'logg'], beta)},
       'pvals': {nm: float(pv) for nm, pv in zip(['const', 'log10B', 'Teff', 'logg'], p_vals)},
       'bins': {}}
for lb, lo, hi in zip(labels, bins[:-1], bins[1:]):
    m = (Teff >= lo) & (Teff < hi)
    if np.sum(m) >= 10:
        r2, p2 = stats.spearmanr(log10B[m], resid[m])
        out['bins'][lb] = {'n': int(np.sum(m)), 'rho': float(r2), 'p': float(p2)}
with open(base + '/scripts/paperX_wd_m83c_regression.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('\nDONE -> paperX_wd_m83c_regression.json')
