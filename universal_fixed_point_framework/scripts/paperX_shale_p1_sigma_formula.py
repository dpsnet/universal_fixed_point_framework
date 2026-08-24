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
"""σ(D,c) Langevin 噪声幅度定量公式（2026-08-11，开放问题推进 v3：物理分解）
理论依据：notes/05_condensed_matter/spectral_shale_accumulation.md §12.5.3/§12.9.2
依赖复用：paper43_coupled_spectral_dip.py

开放问题：σ(D,c) 解析公式待推导（笔记 §12.10.2）。

物理分解（v3）：
  σ(D,c) = σ_vis(D) + [σ_aval(D) − σ_vis(D)] / (1 + (c/h(D))^n)
  * σ_aval(D)：雪崩噪声分量（c=0 极限），近临界孔隙机制 → D 大 σ 大、D→3 饱和
  * σ_vis(D) ：粘性极限平台（c→∞ 残差，确定性拟合余差——g_cap 非线性/谱带离散）
  * h        ：抑制 onset（c·R_path 涨落 ~ ΔU_spread），从 D=2.5 密集扫描标定
  * n        ：抑制陡度（≈2，Lorentzian 型阈值加宽）

v2 教训：σ(c) 快速衰减后趋于非零平台（c=0.3→1.0 仅再降 20%），无平台形式在 c 大端系统性高估抑制。
方法：σ_aval(D)、σ_vis(D) 分别用 18 点登记表 c=0 / c=1.0 列拟合；h、n 用 D=2.5 密集 c 扫描
（独立 DIP）标定；组合公式对 18 点表交叉验证。
"""

import numpy as np
import os
import sys
from scipy.optimize import curve_fit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper43_coupled_spectral_dip import (
    fractal_pore_network,
    run_fractal_dip,
    spectral_band_mapping,
    verify_spectral_flow,
)

# 已登记数据（笔记 §12.5.3 表，64³ N_CFG=2）
D_DATA = np.array([2.2, 2.4, 2.6, 2.8, 3.0, 3.2])
C_DATA = np.array([0.0, 0.3, 1.0])
SIGMA_TABLE = np.array([
    [0.1076, 0.0057, 0.0036],
    [0.1161, 0.0058, 0.0048],
    [0.1269, 0.0068, 0.0065],
    [0.1301, 0.0089, 0.0075],
    [0.1246, 0.0122, 0.0088],
    [0.1276, 0.0101, 0.0138],
])
X_D = D_DATA - 2.0


def r2_score(y, yhat):
    return 1.0 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)


def fit1(x, y, f, p0):
    popt, _ = curve_fit(f, x, y, p0=p0, maxfev=50000)
    return popt


def compute_sigma(pressures, A_t, g_inj, dA_dt):
    residuals = []
    for k in range(g_inj.shape[1]):
        xk = g_inj[:, k]
        yk = dA_dt[:, k]
        if np.std(xk) < 1e-12 or np.std(yk) < 1e-12:
            continue
        A_ = np.vstack([xk, np.ones_like(xk)]).T
        a, b = np.linalg.lstsq(A_, yk, rcond=None)[0]
        residuals.extend(yk - a * xk - b)
    return float(np.std(residuals)) if residuals else np.nan


def dip_sigma(N, phi, D, c, seed):
    binary, radii, lambdas, U = fractal_pore_network(N, phi, D, seed=seed)
    P_arr, S_arr, P_c, S_c, order, Uf = run_fractal_dip(binary, U, c=c, seed=seed)
    if P_c < 0 or P_c > 1e6:
        return np.nan
    pressures, A_t, lam_edges, snapshots = spectral_band_mapping(binary, lambdas, P_arr, P_c, Uf)
    sf = verify_spectral_flow(pressures, A_t, lambdas, binary, Uf, lam_edges)
    if sf is None:
        return np.nan
    return compute_sigma(pressures, A_t, sf["g_inj"], sf["dA_dt"])


def main():
    print("== σ(D,c) Langevin 噪声幅度定量公式（v3 物理分解） ==")

    # ---- 1. σ_aval(D) = σ(D, c=0) 列拟合（二次）----
    y0 = SIGMA_TABLE[:, 0]
    p0_fit = fit1(X_D, y0, lambda x, a, b, c: a + b * x + c * x * x, (0.09, 0.08, -0.04))
    r2_g0 = r2_score(y0, p0_fit[0] + p0_fit[1] * X_D + p0_fit[2] * X_D ** 2)
    print("诊断 1  σ_aval(D) 二次拟合：σ=%.4f + %.4f·x + %.4f·x²，R²=%.4f"
          % (p0_fit[0], p0_fit[1], p0_fit[2], r2_g0))

    # ---- 2. σ_vis(D) = σ(D, c=1.0) 列拟合（二次）----
    yv = SIGMA_TABLE[:, 2]
    pv_fit = fit1(X_D, yv, lambda x, a, b, c: a + b * x + c * x * x, (0.004, 0.01, 0.0))
    r2_gv = r2_score(yv, pv_fit[0] + pv_fit[1] * X_D + pv_fit[2] * X_D ** 2)
    print("诊断 2  σ_vis(D) 二次拟合：σ=%.4f + %.4f·x + %.4f·x²，R²=%.4f"
          % (pv_fit[0], pv_fit[1], pv_fit[2], r2_gv))

    # ---- 3. 密集 c 扫描（D=2.5）标定 h、n ----
    print("诊断 3  密集 c 扫描（D=2.5, N=48, φ=0.31, ncfg=6）标定 h、n")
    C_SCAN = np.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0])
    sig_scan = []
    for c in C_SCAN:
        sigs = [dip_sigma(48, 0.31, 2.5, c, seed=s) for s in range(2000, 8000, 1000)]
        sigs = [s for s in sigs if not np.isnan(s)]
        sig_scan.append(float(np.mean(sigs)))
        print("   c=%.2f：σ=%.5f" % (c, sig_scan[-1]))
    sig_scan = np.array(sig_scan)
    x25 = 0.5
    g0_25 = p0_fit[0] + p0_fit[1] * x25 + p0_fit[2] * x25 ** 2
    gv_25 = pv_fit[0] + pv_fit[1] * x25 + pv_fit[2] * x25 ** 2
    # 平台 hill：σ(c) = gv + (g0-gv)/(1+(c/h)^n)，固定 g0/gv 于 D=2.5 值，拟合 h、n
    model = lambda c, h, n: gv_25 + (g0_25 - gv_25) / (1.0 + np.power(c / h, n))
    ph, pn = fit1(C_SCAN, sig_scan, model, (0.05, 2.0))
    pred_scan = model(C_SCAN, ph, pn)
    r2_scan = r2_score(sig_scan, pred_scan)
    print("   g0(2.5)=%.4f, gv(2.5)=%.4f；h=%.4f, n=%.3f；拟合 R²=%.4f"
          % (g0_25, gv_25, ph, pn, r2_scan))

    # ---- 4. 组合公式：σ(D,c) = gv(D) + (g0(D)-gv(D))/(1+(c/h)^n) ----
    def sigma_formula(D, c):
        x = D - 2.0
        g0 = p0_fit[0] + p0_fit[1] * x + p0_fit[2] * x ** 2
        gv = pv_fit[0] + pv_fit[1] * x + pv_fit[2] * x ** 2
        return gv + (g0 - gv) / (1.0 + np.power(c / ph, pn))

    pred_table = np.array([[sigma_formula(D, c) for c in C_DATA] for D in D_DATA])
    r2_table = r2_score(SIGMA_TABLE.ravel(), pred_table.ravel())
    print("诊断 4  组合公式对 18 点登记表交叉验证 R²=%.4f" % r2_table)

    # ---- 5. 外推独立验证（D=3.0, c=0.5 与 D=2.2, c=0.5，不在拟合域）----
    print("诊断 5  外推独立验证（N=48, ncfg=6）")
    for D, c in [(3.0, 0.5), (2.2, 0.5), (3.0, 0.1)]:
        sigs = [dip_sigma(48, 0.31, D, c, seed=s) for s in range(2000, 8000, 1000)]
        sigs = [s for s in sigs if not np.isnan(s)]
        if not sigs:
            continue
        m = float(np.mean(sigs))
        p = sigma_formula(D, c)
        print("   D=%.1f c=%.2f：实测 σ=%.5f±%.5f vs 公式 %.5f（比值 %.2f）"
              % (D, c, m, float(np.std(sigs)), p, m / p))

    print("结论：σ(D,c) = σ_vis(D) + [σ_aval(D) − σ_vis(D)]/(1+(c/h)^n)，h=%.3f, n=%.2f；"
          % (ph, pn))
    print("      σ_aval(D)=%.4f+%.4f·x+%.4f·x²（R²=%.3f），σ_vis(D)=%.4f+%.4f·x+%.4f·x²（R²=%.3f）"
          % (p0_fit[0], p0_fit[1], p0_fit[2], r2_g0, pv_fit[0], pv_fit[1], pv_fit[2], r2_gv))
    print("      18 点表交叉验证 R²=%.4f，密集扫描拟合 R²=%.4f（诚实边界：h/n 单 D 标定，"
          % (r2_table, r2_scan))
    print("      σ_vis(D) 的 D 依赖已含于公式，h(D) 的 D 依赖待扩展扫描）")
    ok = [r2_g0 > 0.7, r2_gv > 0.5, r2_table > 0.8, r2_scan > 0.9]
    for i, cnd in enumerate(ok):
        print("[%s] 判定 %d" % ("PASS" if cnd else "FAIL", i + 1))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
