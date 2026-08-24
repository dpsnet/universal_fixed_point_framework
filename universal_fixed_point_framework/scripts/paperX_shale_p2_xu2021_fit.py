# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""东营 Xu et al. 2021 图 7 转录数据 ν 拟合（P2 跨体系复核）。

检验：R_m(ΔP) 是否 Langmuir (ν=1) 还是幂律临界 (ν=1/2)。
数据来自 P2-6b 转录表（2026-08-09）。
式 6: R_m = 20.83·ΔP/(ΔP+1.09)，R_f=20.83, ΔP_L=1.09。
"""
import numpy as np
from scipy.optimize import curve_fit

# 转录数据（P2-6b）：(ΔP, R_m)  绿 well-1 6 点 / 蓝 well-2 6 点 / 红 well-3 5 点
data = {
    "well-1(绿)": np.array([[0.08, 1.5], [0.33, 4.2], [0.75, 9.3], [1.34, 12.3], [2.09, 13.9], [2.78, 19.7]]),
    "well-2(蓝)": np.array([[0.08, 4.3], [0.33, 7.0], [0.75, 12.8], [1.34, 11.0], [2.09, 15.0], [2.78, 16.2]]),
    "well-3(红)": np.array([[0.08, 5.0], [0.33, 8.0], [0.75, 12.3], [1.34, 15.1], [2.09, 18.8]]),
}

def langmuir(dp, Rf, dPL):
    return Rf * dp / (dp + dPL)

def gen_power(dp, Rf, dPL, n):
    return Rf * (dp / (dp + dPL)) ** n

Rf_paper = 20.83
dPL_paper = 1.09

print("=" * 78)
print("A. 双倒数线性化：Langmuir (ν=1) 判据 —— 1/R_m vs 1/ΔP 应线性")
print("   (若幂律 ν<1，双倒数图向上弯曲)")
print("=" * 78)
for name, d in data.items():
    dp, rm = d[:, 0], d[:, 1]
    if dp[-1] > 3.0:   # 排除 2.78 差异点做对照
        pass
    for label, mask in [("全点", slice(None)), ("去2.78", slice(None, -1))]:
        dp_, rm_ = dp[mask], rm[mask]
        # 线性拟合 1/rm vs 1/dp
        X = 1.0 / dp_
        Y = 1.0 / rm_
        A = np.vstack([X, np.ones_like(X)]).T
        k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
        pred = k * X + b
        r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
        Rf_inv, dPL_over = b, k   # 1/rm = 1/Rf + (dPL/Rf)/dp
        Rf_fit = 1 / b
        dPL_fit = k * Rf_fit
        print(f"{name:10s} {label:8s}: 1/Rm=({k:.4f})/dP+({b:.4f})  R²={r2:.4f}  "
              f"-> Rf={Rf_fit:6.2f}, dPL={dPL_fit:6.3f}   (论文: Rf=20.83, dPL=1.09)")

print()
print("=" * 78)
print("B. 幂律临界判定：log(ΔP) vs log(Rf−Rm)，斜率 = −ν")
print("   Rf 取论文 20.83；ν=1 (Langmuir) vs ν=1/2 (平均场)")
print("=" * 78)
for name, d in data.items():
    dp, rm = d[:, 0], d[:, 1]
    for label, mask in [("全点", slice(None)), ("去2.78", slice(None, -1))]:
        dp_, rm_ = dp[mask], rm[mask]
        resid = Rf_paper - rm_
        if np.any(resid <= 0):
            continue
        X = np.log(resid)
        Y = np.log(dp_)
        A = np.vstack([X, np.ones_like(X)]).T
        k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
        pred = k * X + b
        r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
        print(f"{name:10s} {label:8s}: log(dP)=({k:.3f})·log(20.83−Rm)+({b:.3f})  R²={r2:.4f}  -> ν={-k:.3f}")

print()
print("=" * 78)
print("C. 三参数广义拟合 Rm = Rf·(ΔP/(ΔP+dPL))^n（n=1 即 Langmuir）")
print("=" * 78)
for name, d in data.items():
    dp, rm = d[:, 0], d[:, 1]
    try:
        p0 = [20.83, 1.09, 1.0]
        popt, pcov = curve_fit(gen_power, dp, rm, p0=p0, maxfev=20000)
        perr = np.sqrt(np.diag(pcov))
        rm_pred = gen_power(dp, *popt)
        r2 = 1 - np.sum((rm - rm_pred) ** 2) / np.sum((rm - rm.mean()) ** 2)
        print(f"{name:10s}: Rf={popt[0]:6.2f}±{perr[0]:5.2f}, dPL={popt[1]:5.3f}±{perr[1]:.3f}, "
              f"n={popt[2]:5.3f}±{perr[2]:.3f}  R²={r2:.4f}")
    except Exception as e:
        print(f"{name:10s}: fit failed {e}")

print()
print("=" * 78)
print("E. ν 裁决：固定指数模型比较（同一 2 参数形式）")
print("   Rm = Rf·(ΔP/(ΔP+dPL))^n, n=1 (Langmuir/ν=1) vs n=1/2 (平均场) vs 自由 n")
print("=" * 78)
for name, d in data.items():
    dp, rm = d[:, 0], d[:, 1]
    row = [f"{name:10s}"]
    for n in (1.0, 0.5):
        def f(dp, Rf, dPL, n=n):
            return Rf * (dp / (dp + dPL)) ** n
        popt, _ = curve_fit(f, dp, rm, p0=[15.0, 0.5], maxfev=20000)
        pred = f(dp, *popt)
        r2 = 1 - np.sum((rm - pred) ** 2) / np.sum((rm - rm.mean()) ** 2)
        # AIC (n=2 参数)
        n_obs = len(rm)
        rss = np.sum((rm - pred) ** 2)
        aic = n_obs * np.log(rss / n_obs) + 2 * 2
        row.append(f"n={n}: Rf={popt[0]:5.1f} dPL={popt[1]:5.2f} R²={r2:.4f} AIC={aic:6.1f}")
    # 自由 n（3 参数）
    def f3(dp, Rf, dPL, n):
        return Rf * (dp / (dp + dPL)) ** n
    try:
        popt, _ = curve_fit(f3, dp, rm, p0=[15.0, 0.5, 1.0], maxfev=40000)
        pred = f3(dp, *popt)
        r2 = 1 - np.sum((rm - pred) ** 2) / np.sum((rm - rm.mean()) ** 2)
        n_obs = len(rm)
        rss = np.sum((rm - pred) ** 2)
        aic = n_obs * np.log(rss / n_obs) + 2 * 3
        row.append(f"自由n: Rf={popt[0]:5.1f} dPL={popt[1]:5.2f} n={popt[2]:.3f} R²={r2:.4f} AIC={aic:6.1f}")
    except Exception as e:
        row.append(f"自由n: fail {e}")
    print("  ".join(row))

print()
print("=" * 78)
print("G. 物理约束裁决：固定 Rf=20.83（论文值，三井共用自由油比例）")
print("   Rm = 20.83·(ΔP/(ΔP+dPL))^n —— 只允许 dPL, n 自由")
print("=" * 78)
for name, d in data.items():
    dp, rm = d[:, 0], d[:, 1]
    row = [f"{name:10s}"]
    best = None
    for n in (1.0, 0.5):
        def f(dp, dPL, n=n):
            return Rf_paper * (dp / (dp + dPL)) ** n
        try:
            popt, _ = curve_fit(f, dp, rm, p0=[1.0], maxfev=40000)
            pred = f(dp, *popt)
            rss = np.sum((rm - pred) ** 2)
            n_obs = len(rm)
            r2 = 1 - rss / np.sum((rm - rm.mean()) ** 2)
            aic = n_obs * np.log(rss / n_obs) + 2 * 1
            row.append(f"n={n}: dPL={popt[0]:5.2f} R²={r2:.4f} AIC={aic:6.1f}")
            if best is None or aic < best[0]:
                best = (aic, n)
        except Exception as e:
            row.append(f"n={n}: fail {e}")
    # 自由 n（2 参数: dPL, n）
    def f2(dp, dPL, n):
        return Rf_paper * (dp / (dp + dPL)) ** n
    try:
        popt, _ = curve_fit(f2, dp, rm, p0=[1.0, 1.0], maxfev=40000)
        pred = f2(dp, *popt)
        rss = np.sum((rm - pred) ** 2)
        n_obs = len(rm)
        r2 = 1 - rss / np.sum((rm - rm.mean()) ** 2)
        aic = n_obs * np.log(rss / n_obs) + 2 * 2
        row.append(f"自由n: dPL={popt[0]:5.2f} n={popt[1]:.3f} R²={r2:.4f} AIC={aic:6.1f}")
    except Exception as e:
        row.append(f"自由n: fail {e}")
    print("  ".join(row))
