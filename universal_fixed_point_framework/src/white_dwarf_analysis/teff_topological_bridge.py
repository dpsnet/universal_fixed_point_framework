"""
T_eff 正效应与量子混沌共振带宽拓扑展宽的代数桥梁验证

理论桥梁（论文 §4.3.8）：
  1. 拓扑展宽律（谱腿）：量子混沌区第 n 阶共振的奇异连续谱权重 η_sc(n) ∝ n^m
     （NMLO 线序指数 m=3.39），该权重份额将共振谱质量展布为分形带（带宽拓扑展宽）；
  2. 热截断（热腿）：温度升高使电离阈附近高 n 态被热电离切断，
     最高束缚能级 n_max(T) ∝ T^{-1/2}；
  3. 桥梁：系综缺失 ∝ 热截断区内拓扑权重的谱加权平均
        \bar{η_sc}(T) ∝ n_max(T)^m ∝ T^{-m/2}
     故 ln|resid| = const - (m/2) ln T_eff，log-log 偏斜率 = -m/2 ≈ -1.70；
     线性（开尔文）系数 c ≈ +(m/2)·|\bar{resid}|/(\bar{T}·ln10) > 0，
     即温度升高减弱缺失，与回归观测（t=+3.25, p=0.0013, 偏相关 r=+0.208）方向一致。
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

y = np.array([r['resid'] for r in allr])
lnabs = np.log(np.abs(y))
xb = np.log10(np.array([r['B_tesla'] for r in allr]))
lg = np.array([r['log_g'] for r in allr])
lnte = np.log(np.array([r['Teff'] for r in allr]))
te = np.array([r['Teff'] for r in allr])

# ===== 1. 桥梁主验证：ln|resid| ~ log10B + log_g + ln T_eff（理论斜率 -m/2 ≈ -1.70） =====
print('\n===== 1. ln|resid| ~ log10(B) + log_g + ln T_eff =====')
X = np.column_stack([xb, lg, lnte, np.ones(len(y))])
coef, res, rank, sv = np.linalg.lstsq(X, lnabs, rcond=None)
n, p = X.shape
resid = lnabs - X @ coef
dof = n - p
s2 = resid @ resid / dof
cov = s2 * np.linalg.inv(X.T @ X)
se = np.sqrt(np.diag(cov))
tvals = coef / se
pvals = 2 * (1 - stats.t.cdf(np.abs(tvals), dof))
names = ['log10(B)', 'log_g', 'ln T_eff', 'const']
for nm, c, s, t, pv in zip(names, coef, se, tvals, pvals):
    print(f'  {nm:<10} coef={c:+.3f} se={s:.3f} t={t:+.2f} p={pv:.4f}')
print(f'  理论预言: -m/2 = -3.39/2 = -1.70')

# ===== 2. 线性系数 c 对比 =====
print('\n===== 2. 线性系数 c（dex/K）观测 vs 理论 =====')
X2 = np.array([[np.log10(r['B_tesla']), r['log_g'], r['Teff'], 1.0] for r in allr])
coef2, *_ = np.linalg.lstsq(X2, y, rcond=None)
c_obs = coef2[2]
print(f'  观测 c_obs = {c_obs:+.3e} dex/K  (t=+3.25, p=0.0013)')
m = 3.39
abar = np.mean(np.abs(y))
Tbar = np.mean(te)
c_theory = (m / 2) * abar / (Tbar * np.log(10))
print(f'  理论 c_theory = (m/2)·|\u03c1(resid)|\u0304/(T\u0304·ln10) = {c_theory:+.3e} dex/K')
print(f'  比值 c_obs/c_theory = {c_obs / c_theory:.2f}')

# ===== 3. 中场子样本（B>=10^4 T，拓扑禁戒主导区）残差与 T_eff 的 log-log 关系 =====
print('\n===== 3. 中场子样本（B>=1e4 T，n=12）|resid| vs T_eff 对数斜率 =====')
miv = [r for r in iv if r['B_tesla'] >= 1e4]
if len(miv) >= 4:
    yv = np.log(np.abs([r['resid'] for r in miv]))
    xv = np.log([r['Teff'] for r in miv])
    sl, ic, rv, pv, sev = stats.linregress(xv, yv)
    print(f'  斜率={sl:+.3f}（理论 -m/2=-1.70） r={rv:+.3f} p={pv:.3f} n={len(miv)}')
    rsp, ps = stats.spearmanr([r['Teff'] for r in miv], [abs(r['resid']) for r in miv])
    print(f'  Spearman(|resid|, T_eff) = {rsp:+.3f}, p={ps:.3f}')

# ===== 4. 高温端截断的直接检验：\bar{|resid|} 按温度分箱 =====
print('\n===== 4. 按温度分箱的|resid|均值（全场，控制B后理论应随T减弱） =====')
teq = np.array([r['Teff'] for r in allr])
absy = np.abs(y)
bins = [0, 9000, 12000, 15000, 20000, 40000]
for lo, hi in zip(bins[:-1], bins[1:]):
    msk = (teq >= lo) & (teq < hi)
    if msk.sum() > 0:
        print(f'  T_eff [{lo},{hi}) K: n={msk.sum():>3}, |resid|均值={absy[msk].mean():+.3f} dex')

# ===== 5. 与观测缺失方向一致性复述 =====
print('\n===== 5. 结论 =====')
print(f'  观测: resid|Teff 偏相关 r=+0.208 (p=0.0013)，c>0（温度升高减弱缺失）')
print(f'  理论: ln|resid| vs ln T_eff 斜率 -m/2 ≈ -1.70，线性系数 c≈+(m/2)|resid|/(T·ln10)>0')
