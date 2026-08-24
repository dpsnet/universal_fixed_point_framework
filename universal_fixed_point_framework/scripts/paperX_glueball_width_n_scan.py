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
paperX_glueball_width_n_scan.py — 2⁺⁺ 宽度对同位旋因子 N 的扫描（2026-08-11）

方向 6 §7.18/7.20（photon_first_principle_origin.md）：§7.18 给出 N=1（210 MeV）与
N=3（552 MeV）两点——本脚本连续扫描 N∈[1,3] 展示宽度对 N 的依赖关系。

N 依赖结构：N 只乘在 ρρ 部分（I=0 胶球 → ρρ 3 电荷态的同位旋因子），
因此 Γ(N) = Γ_非ρρ + N·Γ_ρρ —— 严格线性（斜率 = Γ_ρρ，截距 = Γ_非ρρ）。

公式：Γ_ch = 3α_s(μ)²·(p*/m²)·C'·F_L(z)²·S·N（μ=0.5 GeV，C'=0.52，
      ρρ 含 L=0,2,4；ππ/KK/ηη 为 D 波且 N=1）
输出：figs/paperX_glueball_width_n_scan.png
性质声明: 同位旋 N 的线性依赖分析（N 为离散约定，连续扫描为插值展示），非独立新预言。
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
C_PRIME = 0.52          # §7.16 拟合

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
    if L == 4:
        z2, z4, z6, z8 = z * z, z ** 4, z ** 6, z ** 8
        return math.sqrt(z8 / (225.0 + 45.0 * z2 + 6.0 * z4 + z6))
    raise ValueError


def gamma_mev(m_d, L, S, N=1.0):
    m = M_G2
    a2 = alpha_s(MU) ** 2
    p = pstar(m, m_d)
    z = p * R_BW
    f2 = bw(L, z) ** 2
    return 3.0 * a2 * (p / (m * m)) * C_PRIME * f2 * S * N * 1000.0


def main():
    # ρρ 部分（N=1）：L=0,2,4
    g_rho = gamma_mev(M_RHO, 0, 1.0) + gamma_mev(M_RHO, 2, 1.0) + gamma_mev(M_RHO, 4, 1.0)
    # 非 ρρ 部分：ππ(D)+KK(D)+ηη(D)
    g_other = (gamma_mev(M_PI, 2, 0.5) + gamma_mev(M_K, 2, 0.5) + gamma_mev(M_ETA, 2, 0.5))

    n = np.linspace(1.0, 3.0, 201)
    width = g_other + n * g_rho   # 线性：Γ = 截距 + 斜率·N

    n_star = (200.0 - g_other) / g_rho   # 反解 Γ=200 的 N

    print("2⁺⁺ 宽度对同位旋因子 N 的扫描（μ=0.5 GeV，C'=0.52，ρρ 含 L=0,2,4）")
    print("=" * 70)
    print(f"Γ(N) = Γ_非ρρ + N·Γ_ρρ（严格线性）")
    print(f"  Γ_ρρ(N=1) = {g_rho:.1f} MeV（S+D+L4 求和）")
    print(f"  Γ_非ρρ     = {g_other:.1f} MeV（ππ D + KK D + ηη D）")
    print(f"  斜率 = {g_rho:.1f} MeV/单位 N；截距 = {g_other:.1f} MeV")
    print("-" * 70)
    for n0 in (1.0, 1.5, 2.0, 2.5, 3.0):
        print(f"   N={n0:.1f} → ΣΓ = {g_other + n0*g_rho:.0f} MeV")
    print("-" * 70)
    print(f"200 MeV 反解：N* = (200-{g_other:.0f})/{g_rho:.0f} = {n_star:.2f}（<1）")
    print(f"  → I=0 归一化（N=1）已给出 {g_other+g_rho:.0f} MeV（>200 的 {100*(g_other+g_rho)/200-100:.0f}%）；")
    print(f"    200 MeV 需 N≈{n_star:.2f}（N<1，超出物理约定区间）")
    print("-" * 70)
    print("结论：Γ 对 N 严格线性（N 仅乘 ρρ 部分）；N∈[1,3] 对应 ΣΓ∈[{:.0f},{:.0f}] MeV；".format(
        g_other + 1.0 * g_rho, g_other + 3.0 * g_rho))
    print("      N=1（I=0 归一化）最接近 200 MeV 锚点；N>1 的电荷态求和线性抬高宽度。")

    # 图
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.axhspan(150, 250, color="gray", alpha=0.15, label="200 ± 25% band")
    ax.axhline(200, color="k", ls=":", lw=1, label="anchor 200 MeV")
    ax.plot(n, width, color="C2", lw=2, label=r"$\Sigma\Gamma(N)$ = const + $N\cdot\Gamma_{\rho\rho}$")
    ax.plot([1.0, 3.0], [g_other + g_rho, g_other + 3 * g_rho], "o", color="C3", ms=6,
            label=r"§7.18 points (N=1,3)")
    ax.axvline(n_star, color="C1", ls="--", lw=1.2, label=rf"$N^*$={n_star:.2f} (Γ=200)")
    ax.set_xlabel(r"isospin factor $N$   [ρρ charge-state convention]")
    ax.set_ylabel(r"$\Sigma\Gamma(2^{++})$ (MeV)")
    ax.set_title(r"$2^{++}$ glueball width vs isospin factor $N$: linear dependence")
    ax.legend(fontsize=8)
    ax.set_xlim(1.0, 3.0)
    ax.grid(alpha=0.3)
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, "paperX_glueball_width_n_scan.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("=" * 70)
    print(f"[fig] {os.path.relpath(path, os.path.join(FIG_DIR, '..'))}")
    print("诚实边界：N 为离散约定（1 vs 3），连续扫描为插值展示；N=1 最接近锚点；"
          "完全第一性（N 无独立来源）未闭合。")


if __name__ == "__main__":
    main()
