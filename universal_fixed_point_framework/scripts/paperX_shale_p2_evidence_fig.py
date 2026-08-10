#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 超压临界幂律数值四路裁决证据图（附录 A 图 A2）。

(a) 东营朗缪尔支：Xu et al. 2021 图 7 转录 R_m(ΔP) 三井逐点
    （转录数据同 paperX_shale_p2_xu2021_fit.py，P2-6b）
    + 朗缪尔拟合式 Rm = 20.83·ΔP/(ΔP+1.09)（论文式 6）；
    内嵌双倒数 1/R_m vs 1/ΔP 线性化（三井 R²=0.93–0.99）。
(b) 动态 IP（DIP）ν(c) 动态指纹：64³ ncfg=8 均值表
    （数值来源：paperX_shale_p2_dyn_ip.py 论文级运行，朗缪尔阈值 a=1.09）——
    均匀阻力（φ=0.31/0.40）毛细支 1.275/1.346 → 粘性支 0.009/0.007；
    阻力∝阈值 → 粘性支 0.287/0.329；c=1 两段幂律分支
    （ν_lo≈0.11–0.19 突破暂态 / ν_hi≈0.48–0.62 饱和趋近）。
    平均场 ν=1/2 参考线：四路均无支持。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ---------------- 面板 (a) 数据：东营 Xu et al. 2021 转录 ----------------
# (ΔP, R_m)  绿 well-1 6 点 / 蓝 well-2 6 点 / 红 well-3 5 点（缺 3.01 点）
dongying = {
    "well-1": np.array([[0.08, 1.5], [0.33, 4.2], [0.75, 9.3], [1.34, 12.3], [2.09, 13.9], [2.78, 19.7]]),
    "well-2": np.array([[0.08, 4.3], [0.33, 7.0], [0.75, 12.8], [1.34, 11.0], [2.09, 15.0], [2.78, 16.2]]),
    "well-3": np.array([[0.08, 5.0], [0.33, 8.0], [0.75, 12.3], [1.34, 15.1], [2.09, 18.8]]),
}
WELL_COLOR = {"well-1": "#2ca02c", "well-2": "#1f77b4", "well-3": "#d62728"}
RF_PAPER, DPL_PAPER = 20.83, 1.09

def langmuir(dp):
    return RF_PAPER * dp / (dp + DPL_PAPER)

def double_reciprocal_fit(dp, rm):
    """1/rm = 1/Rf + (dPL/Rf)·(1/dp) 线性拟合 → R²。"""
    X, Y = 1.0 / dp, 1.0 / rm
    k, b = np.linalg.lstsq(np.vstack([X, np.ones_like(X)]).T, Y, rcond=None)[0]
    pred = k * X + b
    r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
    return k, b, r2

# ---------------- 面板 (b) 数据：DIP ν(c)（64³ ncfg=8 均值） ----------------
C_VALS = np.array([0.0, 0.3, 1.0, 3.0, 10.0])
NU_CURVES = {
    "uniform phi=0.31":  (np.array([1.275, 0.574, 0.337, 0.110, 0.009]), "steelblue", "-"),
    "uniform phi=0.40":  (np.array([1.346, 0.572, 0.334, 0.107, 0.007]), "steelblue", "--"),
    "res~thr phi=0.31":  (np.array([1.275, 0.597, 0.422, 0.329, 0.287]), "crimson", "-"),
    "res~thr phi=0.40":  (np.array([1.346, 0.636, 0.467, 0.373, 0.329]), "crimson", "--"),
}
# c=1 两段幂律分支（64³ ncfg=16，四组合并区间：ν_lo≈0.11–0.19 / ν_hi≈0.48–0.62）

# ---------------- 绘图 ----------------
fig = plt.figure(figsize=(12.5, 5.6))
gs = GridSpec(1, 2, width_ratios=[1.05, 1.0], wspace=0.30)

# ===== 面板 (a)：东营朗缪尔支 =====
ax = fig.add_subplot(gs[0])
dp_grid = np.linspace(0.02, 3.1, 400)
ax.plot(dp_grid, langmuir(dp_grid), color="black", lw=1.8,
        label=r"Langmuir: $R_m=20.83\cdot\Delta P/(\Delta P+1.09)$")
for wname, pts in dongying.items():
    ax.scatter(pts[:, 0], pts[:, 1], s=42, c=WELL_COLOR[wname],
               edgecolors="white", linewidths=0.6, zorder=5, label=wname)
ax.set_xlabel(r"$\Delta P$ (MPa)", fontsize=11)
ax.set_ylabel(r"$R_m$ (oil recovery, %)", fontsize=11)
ax.set_xlim(0, 3.2)
ax.set_ylim(0, 22)
ax.set_title("(a) Dongying capillary limit: Langmuir branch $\\nu=1$\n"
             r"$R_m(\Delta P)$ from NMR centrifugation (Xu et al. 2021)", fontsize=10.5)
ax.legend(fontsize=8, loc="upper left", framealpha=0.9)

# 内嵌：双倒数线性化
axin = ax.inset_axes([0.30, 0.42, 0.62, 0.52])
axin.set_facecolor("white")
axin.patch.set_alpha(0.92)
r2txt = []
for wname, pts in dongying.items():
    dp, rm = pts[:, 0], pts[:, 1]
    k, b, r2 = double_reciprocal_fit(dp, rm)
    r2txt.append((wname, r2))
    X = 1.0 / dp
    axin.scatter(X, 1.0 / rm, s=22, c=WELL_COLOR[wname], edgecolors="none", zorder=5)
    xs = np.linspace(min(X), max(X), 50)
    axin.plot(xs, k * xs + b, color=WELL_COLOR[wname], lw=1.0, alpha=0.85)
axin.set_xlabel(r"$1/\Delta P$", fontsize=8)
axin.set_ylabel(r"$1/R_m$", fontsize=8)
axin.tick_params(labelsize=7)
axin.set_title("double reciprocal", fontsize=8.5)
r2str = ", ".join(f"{w}: R$^2$={r:.3f}" for w, r in r2txt)
axin.text(0.02, 0.97, r2str, transform=axin.transAxes, fontsize=7.5,
          ha="left", va="top", color="dimgray")
ax.text(0.03, 0.06, r"$\nu=1$ Langmuir branch = capillary limit ($c_{\rm eff}\lesssim 0.05$)",
        transform=ax.transAxes, fontsize=9, color="dimgray")

# ===== 面板 (b)：动态 IP ν(c) 指纹 =====
ax2 = fig.add_subplot(gs[1])
x_plot = np.where(C_VALS == 0.0, 0.02, C_VALS)   # c=0 → 毛细极限端显示
for name, (nu, color, ls) in NU_CURVES.items():
    ax2.plot(x_plot, nu, color=color, ls=ls, lw=1.6, marker="o", ms=4, label=name)
ax2.axhline(0.5, color="black", ls=":", lw=1.2)
ax2.text(0.013, 0.53, "mean-field $\\nu=1/2$", fontsize=9, ha="left", va="bottom")
# 东营 ν=1 朗缪尔支锚点（毛细极限端）
ax2.plot([0.02], [1.0], marker="*", ms=14, c="darkgreen", zorder=6)
ax2.annotate("Dongying $\\nu=1$\n(Langmuir capillary limit)",
             xy=(0.02, 1.0), xytext=(0.25, 1.42), fontsize=8.5,
             color="darkgreen", ha="center",
             arrowprops=dict(arrowstyle="->", lw=0.8, color="darkgreen"))
# c=1 两段幂律分支区间
ax2.axvspan(0.7, 1.4, color="gold", alpha=0.18)
ax2.text(1.0, 0.95, "c=1 intermediate:\n$\\nu_{\\rm lo}$=0.11-0.19 (breakthrough transient)\n"
                    "$\\nu_{\\rm hi}$=0.48-0.62 (saturation approach)",
         fontsize=7.5, ha="center", va="center", color="#8a6d00",
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#8a6d00", alpha=0.85))
ax2.set_xscale("log")
ax2.set_xlim(0.012, 14)
ax2.set_ylim(-0.05, 1.55)
ax2.set_xlabel(r"$c$ (Ca-number proxy: viscous / capillary)", fontsize=11)
ax2.set_ylabel(r"P2-type exponent $\nu$", fontsize=11)
ax2.set_title("(b) Dynamic IP (DIP, $64^3$, ncfg=8): $\\nu(c)$ dynamic fingerprint\n"
              "viscous competition rewrites $\\nu$, mean-field $1/2$ unsupported", fontsize=10.5)
ax2.legend(fontsize=8, loc="center right", framealpha=0.9)
ax2.grid(which="both", ls=":", alpha=0.35)
ax2.set_xticks([0.02, 0.1, 0.3, 1.0, 3.0, 10.0])
ax2.set_xticklabels(["c$\\to$0", "0.1", "0.3", "1.0", "3.0", "10.0"], fontsize=8.5)

fig.subplots_adjust(left=0.07, right=0.97, bottom=0.12, top=0.88, wspace=0.28)
out = "e:/workspace/hyper-resolution/universal_fixed_point_framework/figs/shale_fig13_p2_evidence.png"
plt.savefig(out, dpi=200)
print("saved:", out)
