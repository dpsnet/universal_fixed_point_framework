# -*- coding: utf-8 -*-
"""Phase 85 R3：守恒定量检验（中场 vs 弱场，控制 Teff）
输入 paperX_wd_continuum.json -> 输出 paperX_wd_continuum_reg.json
1) 离群剔除（res_b1 |diff|>0.5）
2) Teff 分档控制对比
3) 连续谱量 vs log10B 回归（Spearman + OLS，与 EW 残差同口径）
4) 与 Paper 48 EW 缺失量守恒对比
"""
import os, json, io
import numpy as np
from scipy import stats

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "paperX_wd_continuum.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

rows = [r for r in data["rows"] if r.get("res_b1_diff") is None or abs(r["res_b1_diff"]) < 0.5]
print("原始 %d -> 剔除离群后 %d" % (len(data["rows"]), len(rows)))

def grp(rows, cond, key):
    vs = [r[key] for r in rows if cond(r) and r.get(key) is not None]
    return vs

# ---- 1) Teff 分档对比（弱场 vs 中场）----
print("\n=== Teff 分档：slope_res / D_B_res（弱场 vs 中场）===")
for tmin, tmax, tnm in [(None, 10000, "<10kK"), (10000, 20000, "10-20kK"), (20000, None, ">20kK")]:
    for key in ["slope_res", "D_B_res"]:
        w = grp(rows, lambda r, a=tmin, b=tmax: r["B_MG"] < 10 and (a is None or r["Teff"] >= a) and (b is None or r["Teff"] < b), key)
        m = grp(rows, lambda r, a=tmin, b=tmax: 10 <= r["B_MG"] < 100 and (a is None or r["Teff"] >= a) and (b is None or r["Teff"] < b), key)
        if len(w) >= 3 and len(m) >= 3:
            t, p = stats.ttest_ind(m, w, equal_var=False)
            print("%-9s %-10s 弱场 n=%2d mean=%+.4f | 中场 n=%2d mean=%+.4f | t=%.2f p=%.4f" % (
                tnm, key, len(w), np.mean(w), len(m), np.mean(m), t, p))
        else:
            print("%-9s %-10s 弱场 n=%d 中场 n=%d (样本不足)" % (tnm, key, len(w), len(m)))

# ---- 2) 连续谱量 vs log10B 回归（全样本）----
print("\n=== 连续谱量 vs log10B（Spearman + OLS）===")
for key in ["slope_res", "D_B_res", "res_b3_diff"]:
    xs, ys = [], []
    for r in rows:
        if r.get(key) is not None:
            xs.append(np.log10(r["B_MG"])); ys.append(r[key])
    if len(xs) < 10:
        print(key, "样本不足", len(xs)); continue
    xs, ys = np.array(xs), np.array(ys)
    rho, p = stats.spearmanr(xs, ys)
    # OLS
    X = np.column_stack([np.ones_like(xs), xs])
    beta, res, _, _ = np.linalg.lstsq(X, ys, rcond=None)
    n = len(xs)
    dof = n - 2
    yhat = X @ beta
    s2 = np.sum((ys - yhat) ** 2) / dof
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    tval = beta[1] / se[1]
    pval = 2 * (1 - stats.t.cdf(abs(tval), dof))
    print("%-12s n=%3d rho=%+.3f p=%.3g | beta(log10B)=%+.4f (t=%.2f, p=%.3g)" % (key, n, rho, p, beta[1], tval, pval))

# ---- 3) 守恒对比：线缺失 vs 连续谱形状偏移 ----
print("\n=== 守恒对比（Paper 48 中场 EW 残差 vs 连续谱形状残差）===")
# Paper 48: 中场 EW 残差均值 -0.520 dex（总EW比值 0.384 对应的 log10）；中场残差 -0.275 dex（vs 弱场）
# 这里比较：中场 vs 弱场的连续谱形状残差偏移
for key in ["slope_res", "D_B_res", "res_b3_diff"]:
    w = grp(rows, lambda r: r["B_MG"] < 10, key)
    m = grp(rows, lambda r: 10 <= r["B_MG"] < 100, key)
    if len(w) >= 5 and len(m) >= 5:
        d = np.mean(m) - np.mean(w)
        print("%-12s 中场-弱场偏移 = %+.4f dex（EW 线缺失量级：-0.275 dex 中场均值差 / 总EW残差 -0.520）" % (key, d))
