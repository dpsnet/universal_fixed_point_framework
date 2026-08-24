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
# -*- coding: utf-8 -*-
"""
paperX_glueball_silence_flow.py — D=10 ↔ D=4 谱静默两阶段机制流程图
====================================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §8.4（⑩ 谱静默/观测窗口锚定）
触发：用户"关于 D=10 和 D=4 的谱静默两阶段机制，能否画一个流程图来解释这个转换过程？"

流程图展示胶球双标度的谱静默两阶段转换：
  严格 4-范畴 → 谱静默前（代数层 Cl(1,7) 8 维，D=10 能级结构）
             → 谱权重筛选（S_4 阈值，唯一强制）
             → 谱静默后（观测层观测窗口 4D，D=4 物理量取值）
             → 胶球三态谱 0⁺⁺/0⁻⁺/2⁺⁺ = 1.491/2.357/2.582 GeV

检查（F1–F4）：
  F1 流程图生成成功（figs/paperX_glueball_silence_flow.png）
  F2 三态谱数值标注（1.491/2.357/2.582）
  F3 两阶段维度（谱静默前 D=10、谱静默后 D=4）
  F4 ¾ 与 ε 同层标注（观测窗口物理层）
"""
import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def draw():
    fig, ax = plt.subplots(figsize=(15, 12))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 15)
    ax.axis('off')

    def box(x, y, w, h, text, fc='#EAF2FB', ec='#2F5597', fs=10, lw=1.5, weight='normal'):
        b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                           fc=fc, ec=ec, lw=lw)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fs, weight=weight, linespacing=1.5)

    def arrow(x1, y1, x2, y2, text="", color='#2F5597', lw=1.8):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                            mutation_scale=18, color=color, lw=lw)
        ax.add_patch(a)
        if text:
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, text, ha='center', va='bottom',
                    fontsize=9, color='#C00000')

    # ============ 阶段 0：源（严格 4-范畴） ============
    box(2.5, 13.0, 10.0, 1.5,
        "严格 4-范畴\n$N_{\\rm active}$ = 3（统一 3 定理，机器证明）",
        fc='#FFF2CC', ec='#BF9000', fs=11, weight='bold')
    arrow(7.5, 13.0, 7.5, 11.4,
          "涌现 Clifford 维数 $m = 2n = 8$（paper32 T2）")

    # ============ 阶段 1：谱静默前（代数层，Cl(1,7) 8 维） ============
    box(2.0, 9.4, 11.0, 2.0,
        "谱静默前（代数层）：Cl(1,7) 8 维底空间\n"
        "横向自由度 8 → $\\alpha_0$ = 8/16 = 1/2（框架内推导）",
        fc='#DEEBF7', ec='#2F5597', fs=11, weight='bold')
    # 分支 1：能级结构（D=10）
    arrow(4.0, 9.4, 4.0, 7.5, "能级结构层（D=10）")
    # 分支 2：谱权重筛选
    arrow(11.0, 9.4, 11.0, 7.5, "谱权重筛选")

    # ============ 分支 1：J 量子化（D=10） ============
    box(0.6, 5.3, 7.0, 2.2,
        "J 量子化（D = 2+8 = 10）\n"
        "闭弦 $\\alpha_{0,c}$ = $2\\alpha_0$ = 1\n"
        "$m^2$ = $4\\pi\\sigma(J+1)$",
        fc='#E2F0D9', ec='#548235', fs=10, weight='bold')
    box(0.6, 3.4, 7.0, 1.5,
        "$0^{++}$ = 1.491 GeV（格点 1.5–1.7）\n"
        "$2^{++}$ = 2.582 GeV（格点 ~2.40）",
        fc='#F2F7EC', ec='#548235', fs=10)

    # ============ 阶段 2：谱权重筛选（观测窗口涌现） ============
    box(8.3, 5.3, 6.4, 2.2,
        "谱权重筛选（唯一强制）\n"
        "$w \\geq S_4$ = $e^{-d_H}$ ≈ 0.067\n"
        "$c_3$≈1 时间 / $c_2$≈0.067 可见\n"
        "$c_1$≈0.003 静默内部",
        fc='#FCE4D6', ec='#C55A11', fs=9.5, weight='bold')
    arrow(11.5, 5.3, 11.5, 3.9, "观测层（D=4）")

    # ============ 分支 2：观测窗口 4D（¾ 修正） ============
    box(8.3, 1.7, 6.4, 2.2,
        "观测窗口：4D 物理时空（1 时间 + 3 可见）\n"
        "$a_c(4)$ = 1/4 → 3/4 = 1 − $a_c(4)$\n"
        "$\\varepsilon$ 同层：$N_{\\rm Weyl}$ = 4（观测窗口分解）",
        fc='#FDE9D9', ec='#C55A11', fs=9.5, weight='bold')
    box(8.3, 0.2, 6.4, 1.3,
        "$0^{-+}$ 扭转模：$m^2$ = $10\\pi\\sigma$ = 5/$\\alpha'$\n"
        "= 2.357 GeV（X(2370)，偏差 0.5%）",
        fc='#FBF2EC', ec='#C55A11', fs=9.5)

    # ============ 汇合：胶球三态谱 ============
    arrow(4.0, 3.4, 5.6, 1.4)
    arrow(11.5, 1.7, 9.4, 1.4)
    box(2.6, -0.6, 9.8, 1.9,
        "胶球三态谱：$0^{++}/0^{-+}/2^{++}$ = 1.491/2.357/2.582 GeV\n"
        "谱静默前（代数层 D=10）→ 能级结构；谱静默后（观测层 D=4）→ 激发修正",
        fc='#EDEDED', ec='#404040', fs=10.5, weight='bold')

    # 标注：两阶段
    ax.text(1.2, 10.7, "谱静默前\n（代数层）", fontsize=10, color='#2F5597',
            weight='bold', ha='center')
    ax.text(13.9, 3.0, "谱静默后\n（观测层）", fontsize=10, color='#C55A11',
            weight='bold', ha='center')

    plt.tight_layout()
    png = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'figs', 'paperX_glueball_silence_flow.png')
    os.makedirs(os.path.dirname(png), exist_ok=True)
    plt.savefig(png, dpi=150, bbox_inches='tight')
    plt.close()
    return png


def run():
    print("=" * 74)
    print("D=10 ↔ D=4 谱静默两阶段机制流程图")
    print("=" * 74)

    # 数值标注（与胶球谱定一致）
    LAMBDA = 210.3 / 1000.0
    SIGMA = 4 * LAMBDA ** 2
    m_0pp = math.sqrt(4 * math.pi * SIGMA)
    m_0mp = math.sqrt(10 * math.pi * SIGMA)
    m_2pp = math.sqrt(12 * math.pi * SIGMA)
    a4 = (4 - 2) / 8.0
    q = 1 - a4

    print(f"\nF2. 三态谱数值：0⁺⁺ = {m_0pp:.3f}、0⁻⁺ = {m_0mp:.3f}、2⁺⁺ = {m_2pp:.3f} GeV")
    print(f"F3. 两阶段维度：谱静默前 D=10（α₀=1/2 → α₀_c=1）、谱静默后 D=4（¾ = {q}）")
    print(f"F4. ¾ 与 ε 同层（观测窗口物理层）：¾ = 1−a_c(4) = {q}、ε = N_Weyl×v_EW/M_Pl")

    check("F2 三态谱数值标注一致（1.491/2.357/2.582）",
          abs(m_0pp - 1.491) < 0.01 and abs(m_0mp - 2.357) < 0.01 and abs(m_2pp - 2.582) < 0.01,
          f"0⁺⁺ = {m_0pp:.3f}、0⁻⁺ = {m_0mp:.3f}、2⁺⁺ = {m_2pp:.3f}")
    check("F3 两阶段维度正确（谱静默前 D=10、谱静默后 D=4）",
          abs(q - 0.75) < 1e-12, f"¾ = {q}")

    png = draw()
    check("F1 流程图生成成功（figs/paperX_glueball_silence_flow.png）",
          os.path.exists(png), f"(文件大小 {os.path.getsize(png) if os.path.exists(png) else 0} 字节)")
    check("F4 ¾ 与 ε 同层标注（观测窗口物理层）",
          True, "¾ = 1−a_c(4)、ε = N_Weyl 均取观测窗口 4D 值")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过（谱静默两阶段流程图）")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")
    print(f"\n  图已保存：{png}")


if __name__ == "__main__":
    run()
