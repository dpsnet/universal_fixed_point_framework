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
paperX_time_coupling_fig5ab_zhihu.py — 图 5 的 (a)(b) 面板裁剪（知乎文档专用, 2026-08-11）

复用 paperX_time_coupling_lorentz_figs.py 的 (a) 速度角分解 与 (b) 耦合/膨胀因子 两个面板，
生成单行双面板图，供知乎文档《飞船时钟变慢的作用机理》§3.3 使用。

输出（figs/ 目录）:
  photon_fig5ab_time_coupling_zhihu.png  图 5(a)(b) 裁剪：速度角分解 + cosθ/secθ 曲线

性质声明: 与 paper44 图 5 内容一致（几何示意/数据图），数学上与 SR 标准快度图像等价
          （η = arctanh(sinθ)，coshη = γ = secθ），不构成新物理预言。
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
    ax.annotate("", xy=(1.15, 0), xytext=(-0.15, 0),
                arrowprops=dict(arrowstyle="->", color="k"))
    ax.annotate("", xy=(0, 1.15), xytext=(0, -0.15),
                arrowprops=dict(arrowstyle="->", color="k"))
    ax.text(1.13, -0.08, "time axis", fontsize=9)
    ax.text(-0.03, 1.13, "photon normal (90$^\\circ$, speed $c$)", fontsize=9, color="C3")
    th = np.deg2rad(45.0)
    ax.annotate("", xy=(np.cos(th), np.sin(th)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="C0", lw=2))
    ax.plot([0, np.cos(th)], [0, 0], color="C1", lw=1.5, ls="--")
    ax.plot([np.cos(th), np.cos(th)], [0, np.sin(th)], color="C2", lw=1.5, ls="--")
    ax.text(0.30, 0.05, "time coupling $= \\cos\\theta$", fontsize=8.5, color="C1")
    ax.text(0.52, 0.45, "$\\sin\\theta=v/c$", fontsize=8.5, color="C2")
    ax.text(0.18, 0.20, "$\\theta$", fontsize=11, color="C0")
    ax.plot([np.cos(th)], [np.sin(th)], "o", color="C0", ms=4)
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
    ax2.plot(th * 180 / np.pi, sec, color="C0", lw=2, ls="--",
             label=r"dilation factor $\sec\theta=1/\cos\theta$")
    ax2.set_ylabel("dilation factor $\\sec\\theta$", color="C0")
    ax2.set_yscale("log")
    ax2.set_ylim(1, 1e3)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(90, color="C3", lw=1.2, ls=":")
    ax.text(90.5, 0.9, "$90^\\circ$ (light speed)", fontsize=8, color="C3", rotation=90, va="top")
    ax.set_title("(b) coupling $\\cos\\theta$ vs factor $\\sec\\theta$", fontsize=10)
    ax.legend(fontsize=8, loc="center right")
    ax2.legend(fontsize=8, loc="lower center")


def main():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig_a_speed_angle(axes[0])
    fig_b_coupling_factor(axes[1])
    fig.suptitle("Time coupling $\\cos\\theta$: speed-angle decomposition & decay"
                 " (clock slow $=$ weaker coupling)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "photon_fig5ab_time_coupling_zhihu.png")


if __name__ == "__main__":
    main()
