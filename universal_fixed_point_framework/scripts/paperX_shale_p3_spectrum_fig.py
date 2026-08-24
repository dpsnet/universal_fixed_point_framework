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
P3 分支参数谱全景对比图（图 10）
横轴：介质类别（合成单裂缝面 → 合成颗粒堆积/真实裂缝 → 合成球堆积 → 真实岩石裂缝网络）
纵轴：D_1d（1D 投影盒计数维数），对照 ln2/ln3 = 0.6309。
数据源：
  - DPMP DRP-374 合成 29 块/14 独立几何（paperX_shale_p3_dpmp_boxcount.py）
  - DRP-443 IFN.raw 真实岩石诱导裂缝网络（paperX_shale_p3_drp443_rawboxcount.py）
E[N] 为 Moran 反推（假设 r=1/3）：D = ln E[N]/ln(1/r)。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

db = np.log(2) / np.log(3)

categories = ["Synthetic\nsingle fracture\nplane",
              "Synthetic\nfractured grain\npack / real-like",
              "Synthetic\nfractured\nsphere pack",
              "Real rock\nIFN (DRP-443)\nprojection-filling"]

# 每类 (中值, 低, 高, 点列表[(值, 标签)], E[N] 文本)
data = [
    (0.455, 0.40, 0.51, [], "E[N]=1.6-1.8"),
    (0.80, 0.72, 0.89, [(0.813, "374_05_00 x"), (0.818, "374_05_00 y"),
                        (0.723, "374_08_00 x"), (0.888, "374_08_00 y")], "E[N]=2.2-2.7"),
    (0.67, 0.49, 0.85, [(0.625, "374_09_01 x"), (0.684, "374_09_01 y"),
                        (0.521, "374_09_03 y"), (0.523, "374_09_04 x")], "E[N]=1.9-2.1"),
    (0.970, 0.97, 0.993, [(0.970, "x"), (0.970, "y"), (0.993, "z")], "E[N]->inf\n(percolation)"),
]

fig, ax = plt.subplots(figsize=(9.5, 6.5))

for i, (med, lo, hi, pts, en) in enumerate(data):
    x = i + 1
    # 范围条
    ax.plot([x, x], [lo, hi], color="steelblue", lw=8, alpha=0.45, solid_capstyle="round")
    ax.plot([x], [med], marker="_", color="steelblue", ms=14, lw=2)
    # 数据点
    for (v, lab) in pts:
        ax.scatter([x], [v], s=42, c="crimson", zorder=5, edgecolors="white", linewidths=0.6)
        ax.annotate(lab, (x, v), textcoords="offset points",
                    xytext=(9, 6 - 3 * (0 if i % 2 else 0)), fontsize=8, color="crimson",
                    rotation=30, ha="left", va="bottom")
    ax.text(x, 1.045, en, ha="center", va="bottom", fontsize=9.5, color="darkgreen")

# 0.6309 参考线
ax.axhline(db, color="black", ls="--", lw=1.4)
ax.text(4.45, db + 0.012, r"$D_b=\ln 2/\ln 3\approx 0.6309$", fontsize=11,
        ha="right", va="bottom", style="italic")

# 类别标注
ax.set_xticks(range(1, 5))
ax.set_xticklabels(categories, fontsize=10)
ax.set_ylim(0.10, 1.16)
ax.set_ylabel(r"$D_{1d}$  (1D projection box-counting dimension)", fontsize=12)
ax.set_xlim(0.4, 4.9)
ax.grid(axis="y", ls=":", alpha=0.5)
ax.set_title("P3 branch-parameter spectrum: medium class determines $D_{1d}$",
             fontsize=12.5)

# 注释：口径说明
ax.text(0.5, 0.13,
        "Single-fracture / grain-pack / sphere-pack: centroid-line projection (R$^2\\geq$0.8)\n"
        "Real rock IFN: projection-occupancy (correct for volumetric networks, R$^2\\approx$1.0)\n"
        "374_09_01 dual projections {0.625, 0.684} match 0.6309 (E[N]$\\approx$2.0)",
        fontsize=8.5, ha="left", va="bottom", color="dimgray")

plt.tight_layout()
out = "e:/workspace/hyper-resolution/universal_fixed_point_framework/figs/shale_fig10_p3_spectrum.png"
plt.savefig(out, dpi=200)
print("saved:", out)
