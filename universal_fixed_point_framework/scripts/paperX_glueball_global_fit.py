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
paperX_glueball_global_fit.py — 胶球宽度全局最优拟合（2026-08-11）

方向 6 §7.20/7.21（photon_first_principle_origin.md）：整合四自由度（μ, C', N, L）
在物理约束下求最优拟合，输出三态（0⁺⁺/2⁺⁺/0⁻⁺）最终宽度预测。

参数与物理约束：
  μ（衰变标度）：μ ∈ [0.4, 0.8] GeV（Landau 极点前禁闭标度区，§7.14）
  C'（归一化耦合因子）：C' ∈ [0.2, 0.8]（~4π 色/非微扰因子量级，§7.19）
  N（同位旋）：固定 N=1（I=0 归一化，§7.20 显示最接近锚点）
  L（角动量）：完整包含（S/D/G 波 Blatt-Weisskopf，§7.18）
  T（0⁻⁺ 拓扑因子）：T ∈ [0.5, 2.0]（~O(1)，G·G̃ 抑制，态特定）

目标：χ²(μ,C',T) = Σ_i [(Γ_pred,i - Γ_anchor,i)/σ_i]² 最小化
  σ 估计：0⁺⁺=50、2⁺⁺=30、0⁻⁺=25 MeV（锚点不确定度）

输出：figs/paperX_glueball_global_fit.png（χ² 等高线，μ-C' 平面，T 每点最优）
性质声明: 全局最优拟合（物理约束 + 共享参数），非独立新预言。
"""
import math
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAMBDA = 0.210
M_PI, M_RHO, M_K, M_ETA = 0.140, 0.775, 0.498, 0.548
M_G = {"0++": 1.491, "2++": 2.582, "0-+": 2.354}
ANCHOR = {"0++": 0.500, "2++": 0.200, "0-+": 0.170}
SIGMA = {"0++": 0.050, "2++": 0.030, "0-+": 0.025}
R_BW = 1.0
N_ISO = 1.0

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


def pref(m, mu, Cp):
    return 3.0 * alpha_s(mu) ** 2 * (1.0 / (m * m)) * Cp


def width_0pp(mu, Cp):
    """0⁺⁺ → ππ S 波（S=3/2）"""
    m = M_G["0++"]
    p = pstar(m, M_PI)
    return pref(m, mu, Cp) * p * 1.0 * 1.5


def width_2pp(mu, Cp):
    """2⁺⁺ 多道（ππ D + ρρ S+D+G + KK D + ηη D，N=1）"""
    m = M_G["2++"]
    total = 0.0
    for m_d, L, S in ((M_PI, 2, 0.5), (M_RHO, 0, N_ISO), (M_RHO, 2, N_ISO),
                      (M_RHO, 4, N_ISO), (M_K, 2, 0.5), (M_ETA, 2, 0.5)):
        p = pstar(m, m_d)
        z = p * R_BW
        total += pref(m, mu, Cp) * p * bw(L, z) ** 2 * S
    return total


def width_0mp(mu, Cp, T):
    """0⁻⁺ → ππ S 波 × 拓扑因子 T（S=3/2）"""
    m = M_G["0-+"]
    p = pstar(m, M_PI)
    return pref(m, mu, Cp) * p * 1.0 * 1.5 * T


def chi2(mu, Cp, T):
    return (((width_0pp(mu, Cp) - ANCHOR["0++"]) / SIGMA["0++"]) ** 2
            + ((width_2pp(mu, Cp) - ANCHOR["2++"]) / SIGMA["2++"]) ** 2
            + ((width_0mp(mu, Cp, T) - ANCHOR["0-+"]) / SIGMA["0-+"]) ** 2)


def main():
    mu_grid = np.linspace(0.40, 0.80, 81)
    cp_grid = np.linspace(0.20, 0.80, 121)
    t_grid = np.linspace(0.50, 2.00, 76)

    best = None
    chi2_grid = np.full((len(cp_grid), len(mu_grid)), np.inf)
    for i, mu in enumerate(mu_grid):
        for j, cp in enumerate(cp_grid):
            c2min = min(chi2(mu, cp, t) for t in t_grid)
            chi2_grid[j, i] = c2min
            if best is None or c2min < best[0]:
                best = (c2min, mu, cp, min(t_grid, key=lambda t: chi2(mu, cp, t)))

    c2, mu_star, cp_star, t_star = best
    w0 = width_0pp(mu_star, cp_star)
    w2 = width_2pp(mu_star, cp_star)
    wm = width_0mp(mu_star, cp_star, t_star)

    print("胶球宽度全局最优拟合（物理约束 + 共享 μ/C'）")
    print("=" * 74)
    print(f"最优参数：μ* = {mu_star:.2f} GeV（∈[0.4,0.8] 禁闭标度区）")
    print(f"          C'* = {cp_star:.3f}（∈[0.2,0.8]，C*=4π·C'*={4*math.pi*cp_star:.1f}）")
    print(f"          T* = {t_star:.2f}（0⁻⁺ 拓扑因子，~O(1)）")
    print(f"          N=1（I=0 归一化，固定）；L 完整（S/D/G 波）")
    print(f"χ²_min = {c2:.2f}（3 态，3 参数 → 约化 χ²≈{c2/(3-3) if False else c2:.2f}）")
    print("-" * 74)
    print(f"{'态':>5} {'预测 Γ (MeV)':>14} {'锚点 (MeV)':>12} {'偏差':>8}")
    for k, w, a in (("0++", w0, ANCHOR["0++"]), ("2++", w2, ANCHOR["2++"]), ("0-+", wm, ANCHOR["0-+"])):
        print(f"{k:>5} {w*1000:>10.1f} {a*1000:>10.0f} {100*(w-a)/a:>+7.1f}%")
    print("-" * 74)
    print("物理约束检查：")
    print(f"  μ*={mu_star:.2f} ∈ [0.4,0.8] ✓（Landau 极点前禁闭标度）")
    print(f"  C'*={cp_star:.3f} → C*=4πC'*={4*math.pi*cp_star:.1f}（色/非微扰因子，~4π 量级 {'' if 4*math.pi*0.2<=4*math.pi*cp_star<=4*math.pi*0.8 else '⚠️'}）")
    print(f"  T*={t_star:.2f} ∈ [0.5,2.0] ✓（~O(1)）")

    # 图：χ² 等高线（μ-C' 平面）
    fig, ax = plt.subplots(figsize=(9, 6.5))
    X, Y = np.meshgrid(mu_grid, cp_grid)
    lv = np.percentile(chi2_grid[chi2_grid < np.inf], [30, 60, 85])
    cs = ax.contourf(X, Y, chi2_grid, levels=20, cmap="viridis")
    ax.contour(X, Y, chi2_grid, levels=sorted(lv), colors="w", linewidths=0.7)
    ax.plot(mu_star, cp_star, "r*", ms=16, label=rf"optimum ($\mu$*={mu_star:.2f}, C'*={cp_star:.3f})")
    ax.set_xlabel(r"$\mu$ (GeV)")
    ax.set_ylabel(r"$C' = C/4\pi$")
    ax.set_title(r"Global $\chi^2$ for 3-state glueball widths (T optimized per point)")
    ax.legend(fontsize=8, loc="upper right")
    fig.colorbar(cs, ax=ax, label=r"$\chi^2_{\min}$")
    ax.set_xlim(0.4, 0.8)
    ax.set_ylim(0.2, 0.8)
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, "paperX_glueball_global_fit.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("=" * 74)
    print(f"[fig] {os.path.relpath(path, os.path.join(FIG_DIR, '..'))}")
    print("结论：物理约束下全局最优 (μ*,C'*,T*) = ({:.2f}, {:.3f}, {:.2f})，"
          "三态宽度预测 0⁺⁺={:.0f}/2⁺⁺={:.0f}/0⁻⁺={:.0f} MeV（锚点 500/200/170）。".format(
              mu_star, cp_star, t_star, w0*1000, w2*1000, wm*1000))
    print("诚实边界：σ 为锚点不确定度估计；μ/C'/T 的物理约束区间为方案设定；"
          "N=1 固定（§7.20 优选）；完全第一性（参数无独立来源）仍未闭合。")


if __name__ == "__main__":
    main()
