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
paperX_photon_topology_figs.py — Paper 44 可视化图形生成（4 图, 2026-08-11）

输出（figs/ 目录）:
  photon_fig1_directionality_step.png        图 1: 方向性阶跃公理 A4（χ_Φ=Θ(t-t*), σ_S3=1-χ_Φ）
  photon_fig2_resonance_dual_gate.png        图 2: 可拦截性共振双门（定义 2.4：能量门 + 取向门）
  photon_fig3_closure_direction_transition.png 图 3: 闭合结构方向转变（命题 2.6，几何示意）
  photon_fig4_helicity_winding.png           图 4: 环绕方向/螺旋度 s=±1（拓扑表述 2.5.1，几何示意）

性质声明: 图 1/2 为数据图（数值自洽性可视化，已知物理的拓扑重述）；
          图 3/4 为几何示意（命题 2.6 / 拓扑表述 2.5.1 的直观表达）。
          均不构成新物理预言（与 paper44 §7.2 诚实边界一致）。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

H_PLANCK = 6.62607015e-34   # h (J*s)
C_LIGHT = 299792458.0       # c (m/s)

FIG_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs"))


def _save(fig, name):
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  [fig] %s" % os.path.relpath(path, os.path.join(FIG_DIR, "..")))
    return path


def fig1_directionality_step():
    """图 1: 方向性阶跃公理 A4（数据图）——χ_Φ(t) 与 σ_S3(t) 阶跃，单向不可逆"""
    t = np.linspace(0.0, 2.0, 2001)
    t_star = 1.0
    chi = np.where(t >= t_star, 1.0, 0.0)
    sigma = 1.0 - chi
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.plot(t, chi, lw=2.0, label=r"$\chi_\Phi(t)=\Theta(t-t_*)$  (topological class)")
    ax.plot(t, sigma, lw=2.0, ls="--",
            label=r"$\sigma_{S3}(t)=1-\chi_\Phi$  (spectral silence)")
    ax.axvline(t_star, color="k", ls=":", lw=1.0)
    ax.text(t_star + 0.03, 0.62, "emission: spontaneous $1\\to 0$", fontsize=9, color="C1")
    ax.text(0.03, 0.35, "absorption: driven $0\\to 1$ ($R$-folding)", fontsize=9, color="C0")
    ax.set_xlabel("$t$")
    ax.set_ylim(-0.06, 1.16)
    ax.set_title("Axiom A4: directional step (closed $\\to$ open, irreversible)")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    return _save(fig, "photon_fig1_directionality_step.png")


def fig2_resonance_dual_gate():
    """图 2: 可拦截性共振双门（定义 2.4，数据图）——能量门（洛伦兹）+ 取向门（选择定则）"""
    Delta_E = 3.2e-19
    nu0 = Delta_E / H_PLANCK
    Gamma = 1.0e9
    B12 = 1.0

    def g(nu):
        return (Gamma / (2.0 * np.pi)) / ((nu - nu0) ** 2 + (Gamma / 2.0) ** 2)

    def sigma_abs(nu):
        return (H_PLANCK * nu / C_LIGHT) * B12 * g(nu)

    nu = np.linspace(nu0 - 20.0 * Gamma, nu0 + 20.0 * Gamma, 4001)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.5))
    ax1.plot(nu, sigma_abs(nu), lw=2.0)
    ax1.axvline(nu0, color="r", ls="--", lw=1.0)
    ax1.text(nu0 - 19.0 * Gamma, sigma_abs(nu0) * 0.55,
             "off-resonance: $\\sigma_{abs}\\to 0$\n(20$\\Gamma$: ratio $<10^{-3}$)", fontsize=8)
    ax1.set_xlabel(r"$\nu$")
    ax1.set_ylabel(r"$\sigma_{abs}(\nu)\propto h\nu\,B_{12}\,g(\nu)/c$")
    ax1.set_title("Energy gate: Lorentzian resonance ($h\\nu=\\Delta E$)")
    ax2.axis("off")
    rows = [
        [r"$\sigma^+$", "+1", r"$\Delta m=+1$", "allowed"],
        [r"$\sigma^-$", "-1", r"$\Delta m=-1$", "allowed"],
        [r"$\pi$", "0", r"$\Delta m=0$", "allowed"],
        [r"$2s\to 1s$", "—", r"$\Delta l=0$", "forbidden ($B_{12}=0$)"],
    ]
    tbl = ax2.table(cellText=rows, colLabels=["polarization", "$J_z$", r"$\Delta m$", "$B_{12}$ gate"],
                    loc="center", cellLoc="center", colWidths=[0.13, 0.07, 0.13, 0.22])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    ax2.set_title("Orientation gate: selection rules\n$\\Delta m=J_z^{photon}\\in\\{0,\\pm1\\}$ (Prop. 2.3)")
    fig.tight_layout()
    return _save(fig, "photon_fig2_resonance_dual_gate.png")


def fig3_closure_direction_transition():
    """图 3: 闭合结构方向转变（命题 2.6，几何示意）——驻波边界闭合 → 行波环绕轴闭合"""
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig = plt.figure(figsize=(10.5, 4.0))
    # 左：驻波（边界空间闭合）
    ax1 = fig.add_subplot(1, 2, 1)
    x = np.linspace(0.0, 2.0 * np.pi, 500)
    ax1.plot(x, np.sin(x), lw=2.0)
    ax1.axvline(0.0, color="k", lw=2.0)
    ax1.axvline(2.0 * np.pi, color="k", lw=2.0)
    ax1.text(0.12, 0.9, "$\\partial M\\neq\\emptyset$ (Coulomb barrier)", fontsize=8.5)
    ax1.text(0.12, -0.95, "deformation closed at spatial boundary", fontsize=8)
    ax1.set_title("Standing wave: boundary-space closure", fontsize=10)
    ax1.set_xlabel("x")
    ax1.set_ylim(-1.3, 1.3)
    # 右：行波（环绕轴闭合）——螺旋线 + 轴向投影
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    z = np.linspace(0.0, 4.0 * np.pi, 800)
    xr, yr = np.cos(z), np.sin(z)
    ax2.plot(xr, yr, z, lw=2.0)
    ax2.plot(np.zeros_like(z), np.zeros_like(z), z, color="r", lw=2.0,
             label="straight motion = axial projection of encircling loop")
    ax2.set_title("Traveling wave: axis-encircling closure\n($\\partial M=\\emptyset$, helicity $s=\\pm1$)", fontsize=10)
    ax2.legend(fontsize=8, loc="upper left")
    ax2.set_xlabel("x"); ax2.set_ylabel("y"); ax2.set_zlabel("k")
    fig.suptitle("Proposition 2.6: closure-direction transition", fontsize=11)
    fig.tight_layout()
    return _save(fig, "photon_fig3_closure_direction_transition.png")


def fig4_helicity_winding():
    """图 4: 环绕方向/螺旋度 s=±1（拓扑表述 2.5.1，几何示意）——圆偏振场矢量绕 k 旋转"""
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8))
    z = np.linspace(0.0, 3.0 * np.pi, 13)
    for s, title, ax in [(+1, r"$s=+1$ ($\sigma^+$): $\mathrm{Im}(\varepsilon^*\times\varepsilon)\cdot\hat{k}=+1$", axes[0]),
                         (-1, r"$s=-1$ ($\sigma^-$): $\mathrm{Im}(\varepsilon^*\times\varepsilon)\cdot\hat{k}=-1$", axes[1])]:
        for zi in z:
            ex, ey = np.cos(s * zi), np.sin(s * zi)
            ax.arrow(0.0, 0.0, 0.55 * ex, 0.55 * ey, head_width=0.06, head_length=0.09,
                     fc="C0", ec="C0", alpha=0.85)
        ax.plot([-1.2, 1.2], [0, 0], color="k", lw=0.8, ls=":")
        ax.plot([0, 0], [-1.2, 1.2], color="k", lw=0.8, ls=":")
        ax.annotate("k (out of plane)", xy=(1.05, -1.05), fontsize=8)
        ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("$\\varepsilon_1$"); ax.set_ylabel("$\\varepsilon_2$")
    fig.suptitle(r"Topology statement 2.5.1: E-field winding around $\mathbf{k}$ in normal plane", fontsize=10)
    fig.tight_layout()
    return _save(fig, "photon_fig4_helicity_winding.png")


def main():
    print("=" * 72)
    print("Paper 44 (Phase 62B): 可视化图形生成（4 图）")
    print("输出目录: %s" % FIG_DIR)
    print("=" * 72)
    paths = [
        fig1_directionality_step(),
        fig2_resonance_dual_gate(),
        fig3_closure_direction_transition(),
        fig4_helicity_winding(),
    ]
    ok = all(os.path.exists(p) and os.path.getsize(p) > 0 for p in paths)
    print("汇总: %d/%d 图生成" % (sum(1 for p in paths if os.path.exists(p)), len(paths)))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
