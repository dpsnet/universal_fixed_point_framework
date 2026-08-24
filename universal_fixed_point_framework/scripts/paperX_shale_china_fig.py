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
中国湖相五体系 S1-TOC 三因素对比图（Paper XLIII §6.3，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md §6.3
输出：figs/shale_fig6_china_threefactor.png

展示：长7段（零阈值型）/ 青山口 D86 / 青山口 SL / 沙海组 / 苏北阜宁 GY1（c 型）的
S1-TOC 散点与线性回归，标注截距与分类；沙海组 #11 异常点（Tmax=541 煤系
干扰）单独标出（不含于回归）。苏北阜宁 GY1 于 2026-08-08 入库（Wiley JGE 2025）。
"""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(BASE), "figs")
os.makedirs(FIG, exist_ok=True)

FILES = {
    "长7段（零阈值型）": ("data/rockeval_chang7/chang7_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None, "#2e7d32"),
    "青山口 D86（c 型）": ("data/rockeval_qingshankou_d86/qingshankou_d86_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None, "#1565c0"),
    "青山口 SL（c 型）": ("data/rockeval_qingshankou/qingshankou_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None, "#6a1b9a"),
    "沙海组（c 型，煤系注入）": ("data/rockeval_shahai/shahai_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", 11, "#c62828"),
    "苏北阜宁 GY1（c 型，高背景）": ("data/rockeval_subei_funing/rockeval_funing_gy1.csv", "TOC_wt", "S1_mgg", "Tmax_C", None, "#e65100"),
}


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load(fname, ct, cs, cm, drop_idx):
    toc, s1, tm, drop_pt = [], [], [], []
    with open(os.path.join(BASE, fname), encoding="utf-8-sig", errors="replace") as f:
        for i, r in enumerate(csv.DictReader(f), start=1):
            a, b, c = _tof(r[ct]), _tof(r[cs]), _tof(r[cm])
            if not (np.isfinite(a) and np.isfinite(b) and 0 < a < 30 and b >= 0):
                continue
            if drop_idx and i == drop_idx:
                drop_pt.append((a, b))
                continue
            toc.append(a)
            s1.append(b)
            tm.append(c)
    return np.array(toc), np.array(s1), np.array(tm), drop_pt


def main():
    fig, ax = plt.subplots(figsize=(9, 6.2))
    markers = ["o", "s", "^", "D", "*"]
    for (nm, (fn, ct, cs, cm, drop, color)), mk in zip(FILES.items(), markers):
        toc, s1, tm, drop_pt = load(fn, ct, cs, cm, drop)
        a, b = np.polyfit(toc, s1, 1)
        yp = a * toc + b
        r2 = 1.0 - np.sum((s1 - yp) ** 2) / np.sum((s1 - s1.mean()) ** 2)
        xs = np.linspace(toc.min() - 0.3, toc.max() + 0.3, 50)
        ax.scatter(toc, s1, marker=mk, s=42, alpha=0.8, label="%s" % nm, color=color)
        ax.plot(xs, a * xs + b, "--", color=color, lw=1.3,
                label="  S1=%.2f·TOC%+.2f（R²=%.2f，截距%+.2f）"
                      % (a, b, r2, b))
        # 异常点单独标注（沙海组 #11）
        for (tx, ty) in drop_pt:
            ax.scatter([tx], [ty], marker="x", s=110, color="#c62828", zorder=5,
                       label="沙海组 #11 异常（Tmax=541℃）" if not ax.get_legend_handles_labels()[1].count("异常") else "")
            ax.annotate("#11\nTmax=541", (tx, ty), textcoords="offset points",
                        xytext=(8, 8), fontsize=8, color="#c62828")
    ax.set_xlabel("TOC (wt%)", fontsize=11)
    ax.set_ylabel("S1 (mg HC/g rock)", fontsize=11)
    ax.set_title("中国湖相五体系 S1-TOC：零阈值型 vs c 型（沙海组正截距=煤系注入；苏北阜宁负截距但高 OSI 64.2）", fontsize=11.5)
    ax.legend(fontsize=7.5, loc="upper left", framealpha=0.9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = os.path.join(FIG, "shale_fig6_china_threefactor.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print("saved:", out)


if __name__ == "__main__":
    main()
