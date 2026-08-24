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
"""
paperX_glueball_width_c_scan.py — 2⁺⁺ 宽度对耦合因子 C 的扫描（2026-08-11）

方向 6 §7.18/7.19（photon_first_principle_origin.md）：§7.17 扫描 μ（非线性 α_s² 驱动），
本脚本扫描归一化耦合 C'=C/4π ∈ [0.3,0.7]（覆盖 §7.16 拟合值 C'=0.52），
观察 ΣΓ(2⁺⁺) 趋势——Γ ∝ C 严格线性，与 μ 的非线性敏感形成对比。

公式：Γ(2⁺⁺) = Σ_ch 3α_s(μ)²·(p*/m²)·C'·F_L(z)²·S·N（C'=C/4π，μ=0.5 GeV 固定，
      N=1 同位旋 I=0 归一化，与 §7.18 一致）。

输出：figs/paperX_glueball_width_c_scan.png（线性趋势 + 200 MeV 线 + ±25% 带）
性质声明: 参数敏感性分析（C 线性 vs μ 非线性对比），非独立新预言。
"""
import math
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAMBDA = 0.210
M_PI, M_RHO, M_K, M_ETA = 0.140, 0.775, 0.498, 0.548
M_G2 = 2.582
R_BW = 1.0
MU = 0.5
C_PRIME_FIT = 0.52      # §7.16 拟合：C=6.55 → C'=C/4π≈0.52
GAMMA_FIT_MEV = 209.0   # §7.16 基准 ΣΓ（C'=0.52, μ=0.5, N=1）

FIG_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs"))


def alpha_s(mu):
    return 2.0 * math.pi / (9.0 * math.log(mu / LAMBDA))


def pstar(m, m1):
    return 0.5 * math.sqrt(max(m * m - 4.0 * m1 * m1, 1e-12))


def bw(L, z):
    if L == 0:
        return 1.0
    if L == 2:
        z2, z4 = z * z, z ** 4
        return math.sqrt(z4 / (9.0 + 3.0 * z2 + z4))
    raise ValueError


def geom_2pp_total():
    """2⁺⁺ 多道几何和：Σ 3α_s²(p*/m²)·F_L²·S（不含 C'）"""
    m = M_G2
    a2 = alpha_s(MU) ** 2
    total = 0.0
    for m_d, L, S in ((M_PI, 2, 0.5), (M_RHO, 0, 1.0), (M_RHO, 2, 1.0),
                      (M_K, 2, 0.5), (M_ETA, 2, 0.5)):
        p = pstar(m, m_d)
        z = p * R_BW
        total += 3.0 * a2 * (p / (m * m)) * bw(L, z) ** 2 * S
    return total


def main():
    G = geom_2pp_total()
    c = np.linspace(0.30, 0.70, 161)
    width = G * c * 1000.0   # MeV（线性：Γ ∝ C'）

    # 校验拟合点
    w_fit = G * C_PRIME_FIT * 1000.0
    print("2⁺⁺ 宽度对耦合因子 C'=C/4π 的扫描（μ=0.5 GeV 固定，N=1）")
    print("=" * 72)
    print(f"几何和 G = {G:.4f}；拟合校验：C'={C_PRIME_FIT} → ΣΓ={w_fit:.0f} MeV（vs 209 基准）")
    print("-" * 72)
    print("Γ ∝ C' 严格线性（公式 Γ = 3α_s²(p*/m²)·C'·F_L²·S·N）：")
    for c0 in (0.30, 0.40, 0.52, 0.60, 0.70):
        print(f"   C'={c0:.2f} → ΣΓ = {G*c0*1000:.0f} MeV")
    print("-" * 72)

    # ±25% 带（150-250 MeV）覆盖的 C' 区间
    c_lo, c_hi = 150.0 / 1000.0 / G, 250.0 / 1000.0 / G
    print(f"200±25% (150-250 MeV) 覆盖 C'∈[{c_lo:.3f},{c_hi:.3f}]（宽 {c_hi-c_lo:.3f}）")
    in_band = (width >= 150) & (width <= 250)
    frac_band = in_band.mean()
    print(f"C'∈[0.3,0.7] 内落入 ±25% 带比例 = {frac_band*100:.0f}%")
    print("-" * 72)
    print("对比 §7.17 μ 扫描（非线性 α_s² 驱动：379→88 MeV，敏感）vs C 扫描（线性）：")
    print("  C' 扫描范围 0.3-0.7 内 ΣΓ={:.0f}→{:.0f} MeV（±40% 内线性变化）——"
          "C 线性敏感、μ 非线性敏感".format(G*0.30*1000, G*0.70*1000))

    # 图
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.axhspan(150, 250, color="gray", alpha=0.15, label="200 ± 25% band")
    ax.axhline(200, color="k", ls=":", lw=1, label="anchor 200 MeV")
    ax.plot(c, width, color="C1", lw=2, label=r"$\Sigma\Gamma(2^{++})$ (linear in $C'$)")
    ax.plot([C_PRIME_FIT], [w_fit], "o", color="C3", ms=6, label=r"§7.16 fit $C'=0.52$")
    ax.set_xlabel(r"$C' = C/4\pi$   [normalized coupling factor]")
    ax.set_ylabel(r"$\Sigma\Gamma(2^{++})$ (MeV)")
    ax.set_title(r"$2^{++}$ glueball width vs coupling $C'$: linear trend")
    ax.legend(fontsize=8)
    ax.set_xlim(0.3, 0.7)
    ax.grid(alpha=0.3)
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, "paperX_glueball_width_c_scan.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("=" * 72)
    print(f"[fig] {os.path.relpath(path, os.path.join(FIG_DIR, '..'))}")
    print("结论：Γ ∝ C' 严格线性（无拐点）；C'∈[0.3,0.7] 内 ΣΓ={:.0f}→{:.0f} MeV；"
          "±25% 带覆盖 C'∈[{:.3f},{:.3f}]——C 线性敏感（每 0.1 变化 ~40 MeV）。"
          .format(G*0.30*1000, G*0.70*1000, c_lo, c_hi))


if __name__ == "__main__":
    main()
