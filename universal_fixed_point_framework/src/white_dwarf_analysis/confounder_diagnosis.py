"""
混淆分解诊断：残差 ~ log10(B) + log_g + Teff 多元回归 + 匹配对照(仅弱场<1e3)
"""
import json
import numpy as np
from scipy import stats

V10 = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v10_results.json'
GAP = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\results\white_dwarf_analysis_v11_gap_results.json'

with open(V10, 'r', encoding='utf-8') as f:
    d10 = json.load(f)
with open(GAP, 'r', encoding='utf-8') as f:
    dgap = json.load(f)

iv = [r for r in d10['int'] if r.get('resid') is not None and r['total_EW'] > 0]       # mid
wv1 = [r for r in d10['weak'] if r.get('resid') is not None and r['total_EW'] > 0]     # weak <1e3
gap = [r for r in dgap['results'] if r.get('resid') is not None and r['total_EW'] > 0] # gap
allr = iv + wv1 + gap

print(f'n: mid={len(iv)}, weak<1e3={len(wv1)}, gap={len(gap)}, total={len(allr)}')

# ===== 1. 多元回归 resid ~ log10B + log_g + Teff =====
print('\n===== 1. 多元线性回归: resid = a*log10(B) + b*log_g + c*Teff + d =====')
X = np.array([[np.log10(r['B_tesla']), r['log_g'], r['Teff'], 1.0] for r in allr])
y = np.array([r['resid'] for r in allr])
coef, res, rank, sv = np.linalg.lstsq(X, y, rcond=None)
yhat = X @ coef
resid = y - yhat
n, p = X.shape
dof = n - p
s2 = resid @ resid / dof
cov = s2 * np.linalg.inv(X.T @ X)
se = np.sqrt(np.diag(cov))
tvals = coef / se
# p-values
pvals = 2 * (1 - stats.t.cdf(np.abs(tvals), dof))
names = ['log10(B)', 'log_g', 'Teff', 'const']
for nm, c, s, t, pv in zip(names, coef, se, tvals, pvals):
    print(f'  {nm:<10} coef={c:+.4f} se={s:.4f} t={t:+.2f} p={pv:.4f}')
# partial corr of resid with log10B after removing log_g,Teff
def partial_corr(x, y, zs):
    # residuals of x on zs and y on zs, then corr
    Z = np.column_stack(zs + [np.ones(len(x))])
    def linres(v):
        b, *_ = np.linalg.lstsq(Z, v, rcond=None)
        return v - Z @ b
    rx = linres(x); ry = linres(y)
    return stats.pearsonr(rx, ry)
xb = np.log10(np.array([r['B_tesla'] for r in allr]))
lg = np.array([r['log_g'] for r in allr])
te = np.array([r['Teff'] for r in allr])
pr, pp = partial_corr(xb, y, [lg, te])
print(f'  偏相关 resid|log10B (控制log_g,Teff): r={pr:+.3f}, p={pp:.4f}')
pr2, pp2 = partial_corr(lg, y, [xb, te])
print(f'  偏相关 resid|log_g (控制log10B,Teff): r={pr2:+.3f}, p={pp2:.4f}')
pr3, pp3 = partial_corr(te, y, [xb, lg])
print(f'  偏相关 resid|Teff (控制log10B,log_g): r={pr3:+.3f}, p={pp3:.4f}')

# ===== 2. <1e4 T 内 log_g 与 log B 的混淆程度 =====
print('\n===== 2. <10^4 T 内 log_g vs log10(B) 相关（象限效应是否B驱动） =====')
sub = wv1 + gap
sb = np.log10(np.array([r['B_tesla'] for r in sub]))
slg = np.array([r['log_g'] for r in sub])
rho_lg_b, p_lg_b = stats.spearmanr(slg, sb)
print(f'  Spearman(log_g, log10B): rho={rho_lg_b:+.3f}, p={p_lg_b:.2e}')
rho_te_b, p_te_b = stats.spearmanr(np.array([r['Teff'] for r in sub]), sb)
print(f'  Spearman(Teff, log10B): rho={rho_te_b:+.3f}, p={p_te_b:.2e}')

# ===== 3. 匹配对照（匹配池仅限弱场 <10^3 T） =====
print('\n===== 3. 匹配对照（匹配池仅限弱场<10^3 T，避免B驱动污染） =====')
md = []
for r in iv:
    ww = min(wv1, key=lambda w: ((np.log10(w['Teff'])-np.log10(r['Teff']))/0.1)**2
             + ((w['log_g']-r['log_g'])/0.5)**2)
    md.append(r['resid'] - ww['resid'])
md = np.array(md)
t_m, p_m = stats.ttest_1samp(md, 0)
print(f'  匹配后残差差异: 均值={np.mean(md):+.3f} dex (EW比值 {10**np.mean(md):.3f}), 负比例={np.mean(md<0)*100:.0f}% ({np.sum(md<0)}/{len(md)})')
print(f'  单样本t: t={t_m:.2f}, p={p_m:.4f}')

# 对称对照: 缺口星(3e3-1e4)同样匹配弱场<1e3
print('\n  对称对照: 缺口星(3x10^3-10^4 T) vs 弱场<10^3 T 匹配')
g3 = [r for r in gap if r['B_tesla'] >= 3e3]
mdg = []
for r in g3:
    ww = min(wv1, key=lambda w: ((np.log10(w['Teff'])-np.log10(r['Teff']))/0.1)**2
             + ((w['log_g']-r['log_g'])/0.5)**2)
    mdg.append(r['resid'] - ww['resid'])
mdg = np.array(mdg)
t_g, p_g = stats.ttest_1samp(mdg, 0)
print(f'  缺口(3e3-1e4)匹配后差异: 均值={np.mean(mdg):+.3f} dex, t={t_g:.2f}, p={p_g:.4f}, 负比例={np.mean(mdg<0)*100:.0f}%')

# ===== 4. 四象限（仅弱场<1e3）复核 =====
print('\n===== 4. 仅弱场<10^3 T 四象限复核 =====')
lgm = np.median([r['log_g'] for r in wv1]); tem = np.median([r['Teff'] for r in wv1])
for lg_hi in [False, True]:
    for te_hi in [False, True]:
        vals = [r['resid'] for r in wv1 if (r['log_g']>=lgm)==lg_hi and (r['Teff']>=tem)==te_hi]
        if vals:
            v = np.array(vals)
            print(f'  log_g{"高" if lg_hi else "低"} x Teff{"高" if te_hi else "低"}: n={len(v):>3}, 均值={np.mean(v):+.3f} dex')

# ===== 5. 高log_g低Teff象限的B构成 =====
print('\n===== 5. 高log_g x 低Teff象限的B分布（是否B驱动） =====')
ql = [r for r in sub if r['log_g']>=lgm and r['Teff']<tem]
if ql:
    print(f'  n={len(ql)}, log10B 中值={np.median(np.log10([r["B_tesla"] for r in ql])):.2f}, 均值残差={np.mean([r["resid"] for r in ql]):+.3f}')
    print(f'  与全<1e4样本比: log10B中值={np.median(sb):.2f}')
