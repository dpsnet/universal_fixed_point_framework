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

# -*- coding: utf-8 -*-
"""质量 = 偏转时间轴的难度：图像 + 三角函数 三联动图（笔记插图，非数值验证）
输出: figs/mass_deflection_figs.png
Panel 1: 时间轴偏转的三角分解（sinθ=v/c, cosθ=1/γ, tanθ=γv/c）
Panel 2: 惯性侧 vs 引力侧——同一倾斜的两种读法
Panel 3: 同心圆坐标系（径向=T/Δ引力, 切向=空间, 垂直=时间）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

fig = plt.figure(figsize=(16, 5.5))

# ---------------- Panel 1: 时间轴偏转三角分解 ----------------
ax1 = fig.add_subplot(1, 3, 1)
theta = np.deg2rad(30)          # 时间轴偏转角 θ = arcsin(v/c)
v = np.sin(theta)               # v/c
gamma_inv = np.cos(theta)       # 1/γ = cosθ
tan_v = np.tan(theta)           # γv/c

# 坐标轴
ax1.arrow(0, 0, 0, 1.15, head_width=0.03, head_length=0.04, fc="k", ec="k")
ax1.arrow(0, 0, 1.15, 0, head_width=0.03, head_length=0.04, fc="k", ec="k")
ax1.text(0.02, 1.18, "t（时间轴）", fontsize=11)
ax1.text(1.16, 0.02, "x（空间）", fontsize=11)

# 世界线（倾斜 θ）
wl = np.array([0, 1.0])
ax1.plot(wl * np.cos(theta), wl * np.sin(theta), "b-", lw=2.5,
         label="世界线（有质量粒子）")

# 三角投影
ax1.plot([0, v], [0, 0], "r--", lw=1.5)            # sinθ = v/c
ax1.plot([v, v], [0, gamma_inv], "g--", lw=1.5)    # cosθ = 1/γ
ax1.plot([0, 0], [0, gamma_inv], "g-", lw=1.5)     # 垂直参考
ax1.plot([0, 0], [0, v], "r-", lw=1.5)

# 偏转角弧
arc = np.linspace(0, theta, 40)
ax1.plot(0.22 * np.cos(arc), 0.22 * np.sin(arc), "k-", lw=1.2)
ax1.text(0.26, 0.09, r"$\theta$", fontsize=14)

ax1.text(v / 2, -0.08, r"$\sin\theta=v/c$", color="r", fontsize=10)
ax1.text(v + 0.05, gamma_inv / 2, r"$\cos\theta=1/\gamma$", color="g", fontsize=10)
ax1.text(-0.02, gamma_inv + 0.03, r"$d\tau/dt=\cos\theta$", fontsize=10)

ax1.set_xlim(-0.15, 1.25)
ax1.set_ylim(-0.18, 1.28)
ax1.set_aspect("equal")
ax1.set_title("图1  时间轴偏转的三角分解\n（速度角 θ）", fontsize=11)
ax1.legend(loc="lower right", fontsize=8, frameon=False)
ax1.axis("off")

# ---------------- Panel 2: 惯性 vs 引力（同一倾斜两种读法） ----------------
ax2 = fig.add_subplot(1, 3, 2)

# 左：惯性侧（一个点，世界线倾斜）
ax2.arrow(0.18, 0.1, 0, 0.62, head_width=0.02, head_length=0.03, fc="gray", ec="gray")
ax2.plot([0.18, 0.18 + 0.45 * np.cos(theta)], [0.1, 0.1 + 0.45 * np.sin(theta)],
         "b-", lw=2.5)
ax2.plot([0.18, 0.18 + 0.45], [0.1, 0.1], "k:", lw=1)
ax2.text(0.18 + 0.12, 0.30, r"$\theta$", fontsize=13)
ax2.text(0.05, 0.76, "惯性侧（自身）", fontsize=10)
ax2.text(0.02, 0.0, "自己付代价\n$E=(\\sec\\theta-1)m$\nm = 难度系数", fontsize=9,
         va="top")

# 右：引力侧（中心源 + 周围点的时间方向倾斜）
cx, cy = 1.35, 0.42
ax2.plot(cx, cy, "ro", ms=8, zorder=5)
ax2.text(cx - 0.02, cy + 0.06, "源 m", fontsize=9, ha="center")
for ang in [80, 60, 40, 20, -20, -40, -60, -80]:
    a = np.deg2rad(ang)
    x0 = cx + 0.3 * np.cos(a)
    y0 = cy + 0.3 * np.sin(a)
    # 每点的时间方向（垂直偏转 φ）
    dx, dy = 0.0, 0.22
    ax2.plot([x0, x0 + dx], [y0, y0 + dy], "g-", lw=1.8)
    ax2.plot([x0, x0 - 0.12 * np.cos(a)], [y0, y0 - 0.12 * np.sin(a)], "g-", lw=1.8)
ax2.plot([cx - 0.42, cx + 0.42], [cy, cy], "k:", lw=0.8)
ax2.text(cx, cy + 0.42, "引力侧（他人）", fontsize=10, ha="center")
ax2.text(cx - 0.42, 0.02, "中心源 m 让每点时间方向倾斜\n$\\varphi_{grav}(r)$：m = 源强度",
         fontsize=9, va="top")

ax2.text(0.62, 0.55, "同一个倾斜", fontsize=12, color="purple",
         bbox=dict(boxstyle="round", fc="lavender", ec="purple", alpha=0.8))

ax2.set_xlim(0, 1.85)
ax2.set_ylim(-0.1, 0.95)
ax2.set_aspect("equal")
ax2.set_title("图2  惯性 vs 引力\n同一几何量（时间方向倾斜）", fontsize=11)
ax2.axis("off")

# ---------------- Panel 3: 同心圆坐标系 ----------------
ax3 = fig.add_subplot(1, 3, 3)
ax3.set_aspect("equal")

for r, lab, c in [(0.35, "范畴", "crimson"), (0.62, "谱流", "steelblue"),
                  (0.90, "三维空间", "darkgreen")]:
    t = np.linspace(0, 2 * np.pi, 300)
    ax3.plot(r * np.cos(t), r * np.sin(t), color=c, lw=1.8)
    ax3.text(0, r, lab, ha="center", va="bottom", color=c, fontsize=10)

# 径向（T/Δ 引力方向）：指向中心
ax3.annotate("", xy=(0.52, 0), xytext=(1.05, 0),
             arrowprops=dict(arrowstyle="-|>", color="purple", lw=2))
ax3.text(0.80, 0.06, "径向 = T/Δ（引力）", color="purple", fontsize=9)

# 切向（空间）
ax3.annotate("", xy=(0, 0.62), xytext=(0, 1.02),
             arrowprops=dict(arrowstyle="-|>", color="darkgreen", lw=2))
ax3.text(-0.30, 0.86, "切向 = 空间", color="darkgreen", fontsize=9)

# 垂直（时间堆叠）—— 用向上的粗箭头表示
ax3.annotate("", xy=(1.05, 1.30), xytext=(1.05, 0.90),
             arrowprops=dict(arrowstyle="-|>", color="darkorange", lw=2.5))
ax3.text(1.06, 1.12, "垂直 = 时间\n（分形递归堆叠）", color="darkorange", fontsize=9,
         va="center")

ax3.text(0.55, -1.02, "径向 ⊥ 切向 ⊥ 垂直\n= Δ ⊥ 空间 ⊥ 时间", fontsize=10,
         ha="center", bbox=dict(boxstyle="round", fc="#f0f8ff", ec="gray"))

ax3.set_xlim(-1.25, 1.45)
ax3.set_ylim(-1.15, 1.45)
ax3.set_title("图3  同心圆坐标系\n（弥漫包覆的理想化）", fontsize=11)
ax3.axis("off")

fig.suptitle("质量 = 偏转时间轴的难度：同一几何量的双重读法（等效原理的图像版）",
             fontsize=14, y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.95])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs", "mass_deflection_figs.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print("saved:", out)
