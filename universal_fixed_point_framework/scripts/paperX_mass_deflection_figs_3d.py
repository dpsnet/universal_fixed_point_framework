# -*- coding: utf-8 -*-
"""质量 = 偏转时间轴的难度：三维透视版（笔记插图，非数值验证）
输出: figs/mass_deflection_figs_3d.png
同心圆坐标系 3D 透视：
  - 水平面同心圆环（内圈范畴 → 中圈谱流 → 外圈三维空间），沿垂直方向逐层堆叠 = 时间
  - 径向箭头（指向中心）= T/Δ 引力方向（⊥ 空间）
  - 切向箭头 = 空间方向
  - 垂直箭头 = 时间（分形递归堆叠）
  - 三层正交：径向 ⊥ 切向 ⊥ 垂直 = Δ ⊥ 空间 ⊥ 时间
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection="3d")

# ---- 同心圆环：3 层（时间堆叠）x 3 环（范畴/谱流/空间） ----
zs = np.array([0.0, 0.9, 1.8])            # 时间堆叠层
rs = [0.45, 0.9, 1.35]                    # 半径：范畴/谱流/三维空间
colors = ["crimson", "steelblue", "darkgreen"]
labels = ["范畴", "谱流", "三维空间"]

t = np.linspace(0, 2 * np.pi, 240)
for zi in zs:
    for ri, c in zip(rs, colors):
        ax.plot(ri * np.cos(t), ri * np.sin(t), zi, color=c, lw=1.6, alpha=0.9)

# ---- 柱壁：连接相邻层的同半径环（层间 = 径向结构/T）----
for ri, c in zip(rs, colors):
    for phi in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        ax.plot([ri * np.cos(phi)] * 2, [ri * np.sin(phi)] * 2,
                [zs[0], zs[-1]], color=c, lw=0.6, alpha=0.35)

# ---- 顶层标注环名 ----
for ri, c, lab in zip(rs, colors, labels):
    ax.text(ri, 0.06, zs[-1] + 0.15, lab, color=c, fontsize=11)

# ---- 径向箭头（T/Δ 引力方向，指向中心）----
ax.quiver(1.55, 0, 0.45, -1.5, 0, 0, color="purple", lw=2.2,
          arrow_length_ratio=0.12)
ax.text(0.55, 0.15, 0.45, "径向 = T/Δ\n（引力，⊥ 空间）", color="purple",
        fontsize=10)

# ---- 切向箭头（空间方向）----
ax.quiver(1.35, 0, 0.45, 0, 0.85, 0, color="darkgreen", lw=2.2,
          arrow_length_ratio=0.12)
ax.text(1.42, 0.55, 0.45, "切向 = 空间", color="darkgreen", fontsize=10)

# ---- 垂直箭头（时间堆叠）----
ax.quiver(1.7, 1.5, -0.2, 0, 0, 2.3, color="darkorange", lw=3,
          arrow_length_ratio=0.1)
ax.text(1.72, 1.5, 0.95, "垂直 = 时间\n（分形递归堆叠）", color="darkorange",
        fontsize=11)

# ---- 质量的几何：同一时间轴倾斜的两种水平方向（切向=惯性，径向=引力）----
px, py, pz = 1.35, -0.85, 0.45                # 三维空间层代表点
th = np.deg2rad(30)
L = 0.62
ax.plot([px, px], [py, py], [pz, pz + L], "gray", lw=1.1, ls="--",
        alpha=0.8)                            # 公共垂直时间方向（未偏转）
# 惯性：切向（y）扬起 θ
ax.quiver(px, py, pz, 0, L * np.sin(th), L * np.cos(th),
          color="blue", lw=2.6, arrow_length_ratio=0.14)
arc = np.linspace(0, th, 30)
ax.plot([px] * 30, py + 0.18 * np.sin(arc), pz + 0.18 * np.cos(arc),
        "k-", lw=1.0)
ax.text(px + 0.1, py + 0.28, pz + 0.26, r"$\theta_i$", fontsize=14)
ax.text(px - 1.5, py - 0.28, pz + 0.05,
        "惯性：切向向上扬起 θ_i\n（运动方向 = 时间轴倾斜）", fontsize=9,
        color="blue")
# 引力：径向（x，指向中心）扬起 θ（= 切向水平旋转 90°）
ax.quiver(px, py, pz, -L * np.sin(th), 0, L * np.cos(th),
          color="purple", lw=2.6, arrow_length_ratio=0.14)
arc2 = np.linspace(0, th, 30)
ax.plot(px - 0.18 * np.sin(arc2), [py] * 30, pz + 0.18 * np.cos(arc2),
        "k-", lw=1.0)
ax.text(px - 0.30, py, pz + 0.26, r"$\theta_g$", fontsize=14)
ax.text(px - 2.6, py - 0.28, pz + 0.05,
        "引力：径向向上扬起 θ_g\n（= 切向水平旋转 90° → 径向）", fontsize=9,
        color="purple")
ax.text(px + 0.30, py + 0.12, pz + 0.42,
        "cosθ = dτ/dt，m = 偏转难度/源（同一几何量）", fontsize=9, color="k")

# ---- 三层正交说明 ----
ax.text(0, -1.75, -0.35,
        "径向 ⊥ 切向 ⊥ 垂直\n= Δ ⊥ 三维空间 ⊥ 时间",
        fontsize=11, ha="center",
        bbox=dict(boxstyle="round", fc="#f0f8ff", ec="gray", alpha=0.9))

ax.set_xlim(-1.9, 1.9)
ax.set_ylim(-1.9, 1.9)
ax.set_zlim(-0.4, 2.6)
ax.set_xlabel("x", fontsize=10)
ax.set_ylabel("y", fontsize=10)
ax.set_zlabel("t（时间堆叠）", fontsize=10)
ax.set_title("同心圆坐标系 3D 透视：一个点增值以不同径向距离、切向等距铺满所有法向自由度\n"
             "（结构 / 对称性 / 强制平均保证；T = 弥漫结构强制平均）",
             fontsize=13)
ax.view_init(elev=22, azim=-58)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs",
                   "mass_deflection_figs_3d.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print("saved:", out)
