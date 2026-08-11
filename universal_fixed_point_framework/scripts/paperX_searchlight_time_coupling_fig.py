#!/usr/bin/env python3
"""
paperX_searchlight_time_coupling_fig.py — 探照灯与"时间接收面"类比示意图（知乎文档 §4.3, 2026-08-11）

方向 6（photon_first_principle_origin.md §7.6）：把"时间耦合"类比为垂直光束下接收板的正对程度——
  静止（θ=0°）    正对光束，有效受光 = 满幅（cosθ=1）；
  加速（θ 增大）  倾斜，有效受光 = L·cosθ 衰减；
  光速（θ=90°）   侧身，有效受光 = 0（光子极限，时间"冻结"）。

输出（figs/ 目录）:
  photon_fig6_searchlight_time_coupling.png  图 6: 1x2 图集
     (a) 探照灯三姿态：水平(静止)/倾斜(加速)/竖直(光速)，有效受光 = L·cosθ
     (b) 时间耦合 cosθ vs 速度角 θ：三状态点标注

性质声明: 几何类比示意图（非数据图），数学上与 cosθ = 1/γ 等价，不构成新物理预言。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs"))

# 三状态配色（与 fig5 风格一致）
C_REST = "C2"     # 静止（绿）
C_ACC = "C0"      # 加速（蓝）
C_LIGHT = "C3"    # 光速（红）


def _save(fig, name):
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  [fig] %s" % os.path.relpath(path, os.path.join(FIG_DIR, "..")))
    return path


def _plate(ax, x0, y0, theta_deg, color, label):
    """画一块接收板：中心 (x0,y0)，倾斜角 theta，返回两端 x 坐标（用于投影标注）。"""
    L = 1.6
    th = np.deg2rad(theta_deg)
    # 板：绕中心旋转。水平(θ=0)时沿 x 方向。
    dx, dy = L / 2 * np.cos(th), L / 2 * np.sin(th)
    xa, ya = x0 - dx, y0 - dy
    xb, yb = x0 + dx, y0 + dy
    ax.plot([xa, xb], [ya, yb], color=color, lw=4, solid_capstyle="round", zorder=5)
    # 端点上方的垂直光束箭头（光从上往下）
    for x in (xa, xb):
        ax.annotate("", xy=(x, max(ya, yb)), xytext=(x, 3.5),
                    arrowprops=dict(arrowstyle="-|>", color="k", lw=1.2))
    # 标签
    ax.text(x0, y0 + 1.15, label, ha="center", fontsize=9, color=color)
    # 有效受光 = 水平投影宽度 = L·cosθ
    proj = L * np.cos(th)
    # 地面投影标尺（y=-0.35）：板两端的 x 区间
    yg = -0.35
    ax.plot([xa, xb], [yg, yg], color=color, lw=6, alpha=0.85, solid_capstyle="butt", zorder=4)
    ax.text((xa + xb) / 2, yg - 0.28, "received $= L\\cos\\theta=%.2fL$" % proj,
            ha="center", fontsize=8, color=color)
    return xa, xb


def fig_a_searchlight(ax):
    """(a) 探照灯：垂直光束下接收板三种姿态，有效受光 = L·cosθ"""
    ax.set_xlim(-0.3, 6.0)
    ax.set_ylim(-1.0, 4.2)
    # 探照灯（左上）与光束整体
    ax.annotate("", xy=(5.9, 3.9), xytext=(0.1, 3.9), arrowprops=dict(arrowstyle="-", color="y", lw=0))
    ax.plot([0.05, 5.95], [3.9, 3.9], color="k", lw=1)
    ax.text(0.05, 4.05, "time light (time axis, vertical)", fontsize=9, color="k")
    for x in np.arange(0.3, 6.0, 0.75):
        ax.annotate("", xy=(x, 3.55), xytext=(x, 3.9),
                    arrowprops=dict(arrowstyle="-|>", color="grey", lw=1.0))
    # 三块接收板（同一板长 L=1.6）
    _plate(ax, 1.0, 1.0, 0.0, C_REST, r"rest $\theta=0^\circ$")
    _plate(ax, 3.1, 1.0, 45.0, C_ACC, r"accelerate $\theta=45^\circ$")
    _plate(ax, 5.1, 1.0, 90.0, C_LIGHT, r"light speed $\theta=90^\circ$")
    # 地面参考线
    ax.plot([-0.1, 6.0], [-0.35, -0.35], color="k", lw=0.8, ls=":")
    ax.text(5.9, -0.72, "received time light (projection)", fontsize=8, color="k", ha="right")
    ax.text(3.0, -1.15, "effective receiving width $= L\\cos\\theta$:  full / reduced / zero",
            ha="center", fontsize=9)
    ax.set_title("(a) searchlight analogy: plate vs time light", fontsize=10)
    ax.axis("off")


def fig_b_coupling_curve(ax):
    """(b) 时间耦合 cosθ vs 速度角 θ：三状态点"""
    th = np.linspace(0, np.deg2rad(90.0), 400)
    cos = np.cos(th)
    ax.plot(th * 180 / np.pi, cos, color="k", lw=2, label=r"time coupling $\cos\theta$")
    # 三状态点
    pts = [(0.0, C_REST, r"rest $\theta=0^\circ$: coupling $=1$"),
           (45.0, C_ACC, r"accelerate $\theta=45^\circ$: coupling $\approx 0.71$"),
           (90.0, C_LIGHT, r"light speed $\theta=90^\circ$: coupling $=0$")]
    for deg, c, lab in pts:
        ax.plot(deg, np.cos(np.deg2rad(deg)), "o", color=c, ms=8, zorder=5)
        ax.annotate(lab, xy=(deg, np.cos(np.deg2rad(deg))),
                    xytext=(deg + 2, np.cos(np.deg2rad(deg)) - 0.22 if deg < 90 else 0.55),
                    fontsize=8.5, color=c,
                    arrowprops=dict(arrowstyle="->", color=c, lw=0.8))
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel(r"speed angle $\theta$ (deg, $\sin\theta=v/c$)")
    ax.set_ylabel("time coupling")
    ax.set_xlim(0, 90)
    ax.set_ylim(-0.1, 1.15)
    ax.set_title("(b) coupling decays with speed angle", fontsize=10)
    ax.legend(fontsize=9, loc="upper right")


def main():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig_a_searchlight(axes[0])
    fig_b_coupling_curve(axes[1])
    fig.suptitle("Time coupling $\\cos\\theta$: the searchlight & receiving-plate analogy"
                 " (clock slow $=$ reduced coupling)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "photon_fig6_searchlight_time_coupling.png")


if __name__ == "__main__":
    main()
