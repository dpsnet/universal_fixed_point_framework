#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图 9：芦草沟组（恒定-S1 型 c 型储层）vs 怀俄明三组（低 S1 源岩端锚点）
      —— OSI 窗形与 c 项差异的直观对照（Paper XLIII §4.3/§5.1，2026-08-09）

目的：直观验证理论边界——
  (1) c 项差异：芦草沟 c 信号在【绝对 S1 底板】（S1=0.126·TOC+2.790，R²=0.010，
      恒定-S1 型，OSI 代理失效第一例）vs 怀俄明三组无底板（S1→0，正斜率低截距）；
  (2) OSI 窗形差异：芦草沟高背景平台（OSI 中位 65.9）vs 怀俄明三组低值
      （OSI 19.3/16.7/7.1，源岩生烃态）；
  (3) 源-储分离梯度闭合：美方源岩端 4 锚点（EF 5.7/Lewis 7.1/Mowry 16.7/Niobrara 19.3）
      ≪ 中方储层端（长7段 53.6/沙海 62.9/芦草沟 65.9）。
"""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(BASE), 'figs')
os.makedirs(FIG, exist_ok=True)

SPECS = {
    "芦草沟组": ("data/rockeval_jimsar_lucaogou/lucaogou_rockeval.csv",
                 "#c62828", "o"),           # 恒定-S1 型 c 型储层（中国湖相）
    "Niobrara": ("data/rockeval_usgs_niobrara/niobrara_rockeval.csv",
                 "#1565c0", "s"),           # Bighorn 盆地
    "Mowry":    ("data/rockeval_usgs_mowry/mowry_rockeval.csv",
                 "#2e7d32", "^"),           # Wind River 盆地
    "Lewis":    ("data/rockeval_usgs_lewis/lewis_rockeval.csv",
                 "#f9a825", "D"),           # Wind River 盆地
}


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load(name):
    """返回 (toc, s1, tmax, osi) 数组。
    口径与论文一致：怀俄明三组按 wyoming_three.py（Tmax 有效 + OSI<300）；
    芦草沟组按 china_lacustrine.py（仅 TOC/S1 有效，无 Tmax/OSI 过滤，n=119）。"""
    fn, _, _ = SPECS[name]
    need_tmax = name != "芦草沟组"
    osi_cap = None if name == "芦草沟组" else 300.0
    toc_l, s1_l, tm_l, osi_l = [], [], [], []
    with open(os.path.join(BASE, fn), encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            toc, s1, tm = _tof(r["TOC_wt"]), _tof(r["S1_mgg"]), _tof(r["Tmax_C"])
            if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0:
                if need_tmax and not (np.isfinite(tm) and 350 < tm < 600):
                    continue
                osi = s1 / toc * 100.0
                if osi_cap is not None and osi >= osi_cap:
                    continue            # 排除污染/可动油饱和异常（仅美方体系）
                toc_l.append(toc); s1_l.append(s1)
                tm_l.append(tm); osi_l.append(osi)
    return (np.array(toc_l), np.array(s1_l), np.array(tm_l), np.array(osi_l))


def fit(toc, s1):
    a, b = np.polyfit(toc, s1, 1)
    yp = a * toc + b
    r2 = 1.0 - np.sum((s1 - yp) ** 2) / np.sum((s1 - s1.mean()) ** 2)
    return a, b, r2


def panel_c_term(ax):
    """面板 A：c 项差异——S1-TOC 标度（绝对 S1 底板 vs 无底板）"""
    for nm in ("芦草沟组", "Niobrara", "Mowry", "Lewis"):
        toc, s1, _, _ = load(nm)
        col, mk = SPECS[nm][1], SPECS[nm][2]
        ax.scatter(toc, s1, s=26, alpha=0.75, color=col, marker=mk,
                   label="%s (n=%d)" % (nm, len(toc)), edgecolors="none")
        a, b, r2 = fit(toc, s1)
        xx = np.linspace(0, toc.max() * 1.02, 50)
        ax.plot(xx, a * xx + b, color=col, lw=1.6,
                label="%s: S1=%+.3f·TOC%+.3f (R²=%.3f)" % (nm, a, b, r2))
    ax.axhspan(1.6, 4.0, color="#c62828", alpha=0.07)
    ax.annotate("芦草沟绝对 S1 底板 ~2 mg/g\n（恒定-S1 型：OSI 代理失效第一例）",
                xy=(4.0, 3.0), xytext=(0.5, 4.6), fontsize=9, color="#c62828",
                arrowprops=dict(arrowstyle="->", color="#c62828", lw=1))
    ax.annotate("怀俄明三组无底板：S1→0\n（源岩生烃态）",
                xy=(1.6, 0.35), xytext=(3.2, 1.15), fontsize=9, color="#1565c0",
                arrowprops=dict(arrowstyle="->", color="#1565c0", lw=1))
    ax.set_xlabel("TOC (wt%)")
    ax.set_ylabel("S1 (mg HC/g rock)")
    ax.set_xlim(0, 7.5)
    ax.set_ylim(-0.15, 5.5)
    ax.set_title("(a) c 项差异：绝对 S1 底板 vs 无底板", fontsize=11)
    ax.grid(alpha=.3)
    ax.legend(fontsize=7.5, loc="upper left")


def panel_osi_window(ax):
    """面板 B：OSI-Tmax 窗形——高背景平台 vs 低值源岩态"""
    for nm in ("芦草沟组", "Niobrara", "Mowry", "Lewis"):
        _, _, tm, osi = load(nm)
        col, mk = SPECS[nm][1], SPECS[nm][2]
        ax.scatter(tm, osi, s=22, alpha=0.6, color=col, marker=mk,
                   label="%s (OSI 中位 %.1f)" % (nm, np.median(osi)),
                   edgecolors="none")
        # 10℃ 箱窗形中位线（≥5 样品箱）
        xs, ys = [], []
        for lo in np.arange(405, 460, 10):
            m = (tm >= lo) & (tm < lo + 10)
            if m.sum() >= 5:
                xs.append(lo + 5); ys.append(np.median(osi[m]))
        if len(xs) >= 2:
            ax.plot(xs, ys, "-", color=col, lw=1.5)
    ax.axhline(45, color="gray", ls="--", lw=1)
    ax.annotate("储层端参照：Green River OSI 45.1", xy=(455, 46),
                xytext=(408, 52), fontsize=8, color="gray")
    ax.set_xlabel("Tmax (°C)")
    ax.set_ylabel("OSI = S1/TOC×100")
    ax.set_xlim(400, 465)
    ax.set_ylim(0, 180)
    ax.set_title("(b) OSI–Tmax 窗形：高背景平台 vs 低值源岩态", fontsize=11)
    ax.grid(alpha=.3)
    ax.legend(fontsize=8, loc="upper right")


def panel_osi_bar(ax):
    """面板 C：OSI 中位对照——源-储分离梯度闭合"""
    groups = [
        ("美方海相源岩端 4 锚点", "#9e9e9e",
         [("Eagle Ford\nGC-2", 5.7), ("Lewis", 7.1), ("Mowry", 16.7), ("Niobrara", 19.3)]),
        ("中方储层端 3 体系", "#c62828",
         [("长7段", 53.6), ("沙海组", 62.9), ("芦草沟组", 65.9)]),
    ]
    labels, vals, colors = [], [], []
    for gname, gcol, items in groups:
        for nm, v in items:
            labels.append(nm); vals.append(v)
            colors.append(gcol)
    # 组间分隔（在源岩端与储层端之间插入空隙标记）
    x = np.arange(len(labels))
    ax.bar(x, vals, color=colors, alpha=0.85, edgecolor="white")
    ax.axvline(3.5, color="black", ls=":", lw=1.2)
    ax.text(1.75, 73, "源岩端\n(OSI<20)", ha="center", fontsize=8.5, color="#555")
    ax.text(5.25, 73, "储层端\n(OSI>45)", ha="center", fontsize=8.5, color="#c62828")
    for xi, v in zip(x, vals):
        ax.text(xi, v + 1.2, "%.1f" % v, ha="center", fontsize=8.5)
    ax.axhspan(45, 105, color="gray", alpha=0.10)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("OSI 中位数")
    ax.set_ylim(0, 80)
    ax.set_title("(c) 源-储分离梯度闭合（OSI 中位）", fontsize=11)
    ax.grid(alpha=.3, axis="y")
    ax.annotate("芦草沟 OSI 65.9：c 信号在绝对 S1 底板\n而非 OSI 抬升（恒定-S1 型）",
                xy=(6, 65.9), xytext=(2.2, 55), fontsize=8.5, color="#c62828",
                arrowprops=dict(arrowstyle="->", color="#c62828", lw=1))


def main():
    fig, axs = plt.subplots(1, 3, figsize=(18.5, 5.6))
    panel_c_term(axs[0])
    panel_osi_window(axs[1])
    panel_osi_bar(axs[2])
    fig.suptitle("芦草沟组（恒定-S1 型 c 型储层）vs 怀俄明三组（低 S1 源岩端锚点）："
                 "OSI 窗形与 c 项差异的直观对照", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = os.path.join(FIG, "shale_fig9_lucaogou_wyoming.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print("图已保存：%s" % out)
    # 控制台复核关键数值
    for nm in ("芦草沟组", "Niobrara", "Mowry", "Lewis"):
        toc, s1, tm, osi = load(nm)
        a, b, r2 = fit(toc, s1)
        print("%-6s n=%-4d TOC[%.2f,%.2f] S1中位=%.3f  Tmax中位=%.0f  OSI中位=%.1f  "
              "S1=%+.3f·TOC%+.3f R²=%.3f"
              % (nm, len(toc), toc.min(), toc.max(), np.median(s1),
                 np.median(tm), np.median(osi), a, b, r2))


if __name__ == "__main__":
    main()
