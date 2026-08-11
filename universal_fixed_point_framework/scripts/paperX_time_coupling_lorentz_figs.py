#!/usr/bin/env python3
"""
paperX_time_coupling_lorentz_figs.py — 洛伦兹变换的时间耦合诠释（图 5, 2026-08-11）

方向 6（photon_first_principle_origin.md §7.6）：从"光子 ⊥ 时间"角度重新表述洛伦兹变换——
时间耦合 = cos(theta)（sin theta = v/c），boost 的时间耦合重标定（sec theta = 1/cos theta）。

输出（figs/ 目录）:
  photon_fig5_time_coupling_lorentz.png   图 5: 2x2 图集
     (a) 速度角分解：时间轴 vs 光子法向(90°)，时间耦合 = cos(theta)
     (b) 时间耦合 cos(theta) 与膨胀因子 sec(theta) vs 速度角
     (c) 钟慢：牛顿斜线(穿过光速) vs 相对论渐近曲线(贴近光速)
     (d) 时空图：boost 时间轴倾斜，光锥 45° 不变

性质声明: 几何示意/数据图，数学上与 SR 标准快度图像等价（eta = arctanh(sin theta)），
          诠释增量在"时间耦合"语言，不构成新物理预言。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs"))


def _save(fig, name):
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  [fig] %s" % os.path.relpath(path, os.path.join(FIG_DIR, "..")))
    return path


def fig_a_speed_angle(ax):
    """(a) 速度角分解：时间轴(水平) vs 光子法向(90°)，时间耦合 = cos(theta)"""
    ax.set_aspect("equal")
    # 轴
    ax.annotate("", xy=(1.15, 0), xytext=(-0.15, 0),
                arrowprops=dict(arrowstyle="->", color="k"))
    ax.annotate("", xy=(0, 1.15), xytext=(0, -0.15),
                arrowprops=dict(arrowstyle="->", color="k"))
    ax.text(1.13, -0.08, "time axis", fontsize=9)
    ax.text(-0.03, 1.13, "photon normal (90$^\\circ$, speed $c$)", fontsize=9, color="C3")
    # 速度矢量（theta = 45 度示例）
    th = np.deg2rad(45.0)
    ax.annotate("", xy=(np.cos(th), np.sin(th)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="C0", lw=2))
    ax.plot([0, np.cos(th)], [0, 0], color="C1", lw=1.5, ls="--")
    ax.plot([np.cos(th), np.cos(th)], [0, np.sin(th)], color="C2", lw=1.5, ls="--")
    ax.text(0.30, 0.05, "time coupling $= \\cos\\theta$", fontsize=8.5, color="C1")
    ax.text(0.52, 0.45, "$\\sin\\theta=v/c$", fontsize=8.5, color="C2")
    ax.text(0.18, 0.20, "$\\theta$", fontsize=11, color="C0")
    ax.plot([np.cos(th)], [np.sin(th)], "o", color="C0", ms=4)
    # 标注端点
    ax.text(0.03, -0.16, "$\\theta=0^\\circ$: coupling $=1$", fontsize=8, color="k")
    ax.text(0.68, 1.03, "$\\theta=90^\\circ$: coupling $=0$", fontsize=8, color="C3")
    ax.set_xlim(-0.35, 1.45)
    ax.set_ylim(-0.45, 1.45)
    ax.set_title("(a) speed angle $\\theta$: time coupling $=\\cos\\theta$", fontsize=10)
    ax.axis("off")


def fig_b_coupling_factor(ax):
    """(b) 时间耦合 cos(theta)（左轴）与膨胀因子 sec(theta)=1/cos(theta)（右轴）"""
    th = np.linspace(0, np.deg2rad(89.0), 400)
    cos = np.cos(th)
    sec = 1.0 / cos
    ax.plot(th * 180 / np.pi, cos, color="C1", lw=2, label=r"time coupling $\cos\theta$")
    ax.set_xlabel(r"speed angle $\theta$ (deg)")
    ax.set_ylabel("time coupling", color="C1")
    ax.set_ylim(0, 1.05)
    ax2 = ax.twinx()
    ax2.plot(th * 180 / np.pi, sec, color="C0", lw=2, ls="--", label=r"dilation factor $\sec\theta=1/\cos\theta$")
    ax2.set_ylabel("dilation factor $\\sec\\theta$", color="C0")
    ax2.set_yscale("log")
    ax2.set_ylim(1, 1e3)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(90, color="C3", lw=1.2, ls=":")
    ax.text(90.5, 0.9, "$90^\\circ$ (light speed)", fontsize=8, color="C3", rotation=90, va="top")
    ax.set_title("(b) coupling $\\cos\\theta$ vs factor $\\sec\\theta$", fontsize=10)
    ax.legend(fontsize=8, loc="center right")
    ax2.legend(fontsize=8, loc="lower center")


def fig_c_clock_slow(ax):
    """(c) 钟慢：牛顿斜线(穿过光速) vs 相对论渐近曲线(贴近光速)"""
    t = np.linspace(0.01, 4.0, 400)
    beta_newton = t / 3.0                       # v/c = at/c, 直线（将穿过 1.0）
    beta_rel = t / np.sqrt(9.0 + t * t)          # v/c = at/sqrt(c^2+a^2t^2)，渐近 1.0
    ax.plot(t, beta_newton, color="C2", lw=1.8, ls="--", label=r"Newton $v/c=at/c$ (crosses light speed)")
    ax.plot(t, beta_rel, color="C0", lw=2, label=r"relativistic $v/c=at/\sqrt{c^2+a^2t^2}$")
    ax.axhline(1.0, color="C3", lw=1.2, ls=":")
    ax.text(0.1, 1.02, "light speed $c$", fontsize=8, color="C3")
    ax.annotate("asymptotic to 90$^\\circ$ (time coupling $\\to 0$)",
                xy=(3.6, 0.77), fontsize=8, color="C0",
                xytext=(1.4, 0.35), arrowprops=dict(arrowstyle="->", color="C0"))
    ax.set_xlabel("time $at/c$ (normalized)")
    ax.set_ylabel(r"$v/c$")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1.25)
    ax.set_title("(c) clock slow: straight line vs asymptote curve", fontsize=10)
    ax.legend(fontsize=7.5, loc="upper left")


def fig_d_spacetime(ax):
    """(d) 时空图：boost 时间轴倾斜 arctan(beta)，光锥 45° 不变"""
    ax.set_aspect("equal")
    # 光锥
    ax.plot([-1, 1], [1, 1], color="C3", lw=1.4, ls=":")
    ax.plot([-1, 1], [-1, -1], color="C3", lw=1.4, ls=":")
    ax.text(0.72, 1.02, "light cone", fontsize=8, color="C3")
    # 静止系轴
    ax.annotate("", xy=(0, 1.15), xytext=(0, -0.15), arrowprops=dict(arrowstyle="->", color="k"))
    ax.annotate("", xy=(1.15, 0), xytext=(-0.15, 0), arrowprops=dict(arrowstyle="->", color="k"))
    ax.text(-0.16, 1.1, "$t$ (rest)", fontsize=9)
    ax.text(1.1, -0.1, "$x$", fontsize=9)
    # 运动系（beta = 0.6）t' 轴倾斜 arctan(beta) ~ 31°
    beta = 0.6
    alpha = np.arctan(beta)  # t' 轴在 (ct, x) 平面的倾斜角
    ax.annotate("", xy=(np.sin(alpha), np.cos(alpha)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="C0", lw=2))
    ax.text(np.sin(alpha) + 0.03, np.cos(alpha) - 0.06, "$t'$ (moving, $\\beta=0.6$)", fontsize=8.5, color="C0")
    # x' 轴（与 t' 对称倾斜）
    ax.annotate("", xy=(np.cos(alpha), np.sin(alpha)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="C1", lw=2))
    ax.text(np.cos(alpha) + 0.02, np.sin(alpha) + 0.02, "$x'$", fontsize=9, color="C1")
    ax.text(0.05, 0.10, "$\\alpha=\\arctan\\beta$", fontsize=8.5, color="C0")
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-0.45, 1.35)
    ax.set_title("(d) boost = time-axis tilt, cone fixed", fontsize=10)
    ax.axis("off")


def main():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig_a_speed_angle(axes[0, 0])
    fig_b_coupling_factor(axes[0, 1])
    fig_c_clock_slow(axes[1, 0])
    fig_d_spacetime(axes[1, 1])
    fig.suptitle("Lorentz transform via time-coupling angle $\\theta$ (time coupling $=\\cos\\theta$, $\\sin\\theta=v/c$)",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _save(fig, "photon_fig5_time_coupling_lorentz.png")


if __name__ == "__main__":
    main()
