#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
陈中红参数间解耦法试算——李宗亮 2025 表 4（Paper XLIII，2026-08-09）
对应笔记：notes/05_condensed_matter/shale_data_inventory.md（§9.4 同位素指纹通道候选 #6）

方法：陈中红、柴智 2022（岩性油气藏 34(5):38-49，DOI 10.12108/yxyqc.20220503）
——同一油样不同组分成熟度参数的系统性差异（轻烃/金刚烷计算成熟度 > 甾萜烷/芳烃
计算成熟度）= 原油混合/多期充注证据（参数间解耦 = c 项"运移烃背景"指纹式判别器）。

李宗亮 2025（地质科学 60(5):1329-1341）表 4 可及参数（原油 4 样 A0001-A0004）：
  G = αααC29 20S/(20S+20R) = 0.44/0.46/0.49/0.51（甾烷异构化，平衡 0.52-0.55）
  A = C29ββ/(ββ+αα)        = 0.56/0.58/0.59/0.61（甾烷异构化）
  F = C31 22S/(22R+22S)    = 0.59/0.60/0.59/0.60（萜烷异构化，平衡 ~0.57-0.62）
  正文 MPI = 0.723-0.785 → EqVRo 0.83-0.87%（Radke 成熟窗 Ro=0.6·MPI+0.4，作者原文）
  ★ 缺金刚烷（MDI/MAI）与轻烃（C7）逐样品列——陈中红式"高敏感组"维度缺失

检验：
  D1 甾烷内部一致性：原油 G vs A Spearman（同组分异构化同步性；n=4）
  D2 F 饱和诊断：C31 22S 近平衡不敏感（F 跨度 vs G 跨度）
  D3 MPI-甾烷区间对照：MPI-EqVRo [0.83,0.87] vs G→EqVRo（两种陆相锚定换算）重叠判定
  D4（登记）作者内禀声明：原文"MPI 计算 Ro 验证了甾萜类化合物计算成熟度的准确性"
  D5（登记）维度不足：MPI 仅正文区间（无逐样品表列）+ 无金刚烷/轻烃 → 解耦不可完全复现

结论（预期）：零假设（参数一致/单源）未被拒绝；陈中红式解耦判别须待含金刚烷/轻烃
逐样品数据的新载体（诚实负结果/维度不足登记）。
"""
import csv
import os
import numpy as np
from scipy.stats import spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "data", "lizongliang2025_zhengning", "lzl2025_table4.csv")

# 正文：4 个原油 MPI 区间 0.723-0.785 → EqVRo 0.83-0.87%（Radke 成熟窗 Ro = 0.6·MPI1 + 0.4）
MPI_RANGE = (0.723, 0.785)
MPI_RO = (0.6 * MPI_RANGE[0] + 0.4, 0.6 * MPI_RANGE[1] + 0.4)

# G（C29 20S）→ EqVRo 陆相经验换算（诚实标注：换算锚点本身具不确定性）
#   换算 A（常规锚点）：20S=0.25→Ro 0.50%、20S=0.52→Ro 1.00%
#   换算 B（陡峭锚点）：20S=0.25→Ro 0.45%、20S=0.55→Ro 1.10%
ANCHORS = {
    "A": ((0.25, 0.50), (0.52, 1.00)),
    "B": ((0.25, 0.45), (0.55, 1.10)),
}


def to_f(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def load_oil():
    rows = []
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["Lithology"] == "原油":
                rows.append(r)
    return rows


def lin_convert(x, p0, p1):
    """两点线性换算：p0=(x0,y0), p1=(x1,y1)"""
    x0, y0 = p0
    x1, y1 = p1
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def main():
    oil = load_oil()
    ids = [r["SampleID"] for r in oil]
    g = np.array([to_f(r["G"]) for r in oil])
    a = np.array([to_f(r["A"]) for r in oil])
    f = np.array([to_f(r["F"]) for r in oil])

    print("== 陈中红参数间解耦法试算——李宗亮 2025 表 4（原油 n=%d） ==" % len(oil))
    print("样品：%s" % ",".join(ids))
    print("  G（αααC29 20S）= %s（平衡 0.52-0.55）" % ",".join("%.2f" % v for v in g))
    print("  A（C29ββ）     = %s" % ",".join("%.2f" % v for v in a))
    print("  F（C31 22S）   = %s（平衡 ~0.57-0.62）" % ",".join("%.2f" % v for v in f))
    print("  MPI（正文区间）  = %.3f-%.3f → EqVRo %.2f-%.2f%%" % (MPI_RANGE[0], MPI_RANGE[1], MPI_RO[0], MPI_RO[1]))

    checks = []

    # D1 甾烷内部一致性：G vs A Spearman
    rho, p = spearmanr(g, a)
    print("\n[D1 甾烷内部一致性]")
    print("  G vs A：ρ=%.3f（p=%.3g，n=%d）——两甾烷异构化参数同步性" % (rho, p, len(g)))
    checks.append(("D1 原油 G vs A Spearman ρ=%.3f（n=%d）——甾烷异构化内部同步（ρ≥0.8 一致）"
                   % (rho, len(g)), rho >= 0.8))

    # D2 F 饱和诊断
    span_f = float(np.ptp(f))
    span_g = float(np.ptp(g))
    print("\n[D2 F 饱和诊断]")
    print("  F 跨度 %.2f vs G 跨度 %.2f（比值 %.2f）——C31 22S 近平衡对样品间差异不敏感" % (span_f, span_g, span_f / span_g))
    checks.append(("D2 C31 22S 饱和诊断：F 跨度 %.2f < 0.03 且 F/G 跨度比 %.2f < 0.5（22S 在成熟窗已达平衡）"
                   % (span_f, span_f / span_g), span_f < 0.03 and span_f / span_g < 0.5))

    # D3 MPI-甾烷区间对照
    g_lo, g_hi = float(g.min()), float(g.max())
    print("\n[D3 MPI-甾烷区间对照（参数间解耦核心）]")
    print("  MPI-EqVRo 区间 [%.3f, %.3f]%%" % (MPI_RO[0], MPI_RO[1]))
    overlaps = {}
    for name, (p0, p1) in ANCHORS.items():
        ro_lo = lin_convert(g_lo, p0, p1)
        ro_hi = lin_convert(g_hi, p0, p1)
        ov = not (ro_hi < MPI_RO[0] or ro_lo > MPI_RO[1])
        overlaps[name] = ov
        print("  换算 %s：G→EqVRo [%.3f, %.3f]%% vs MPI [%.3f, %.3f]%% → %s"
              % (name, ro_lo, ro_hi, MPI_RO[0], MPI_RO[1], "重叠（无解耦证据）" if ov else "不重叠（解耦方向性）"))
    checks.append(("D3 MPI-甾烷解耦：换算 A 下 G-EqVRo 与 MPI-EqVRo 区间%s——零假设（参数一致）未被拒绝；"
                   "换算 B 敏感性见输出（%s）"
                   % ("重叠" if overlaps["A"] else "不重叠", "B=%s" % ("重叠" if overlaps["B"] else "不重叠")),
                   overlaps["A"]))

    # D4 作者内禀声明（登记）
    print("\n[D4（登记）作者内禀声明]")
    print("  原文（正文）：'研究区4个原油样品的甲基菲指标在0.723~0.785之间，根据该数据计算原油成熟度")
    print("  相当于Ro在0.83%~0.87%，处于成熟演化阶段，这也验证了利用甾萜类化合物计算原油所处成熟阶段")
    print("  的准确性。'——作者立场 = MPI 与甾萜指示一致（零假设成立），无解耦证据")
    checks.append(("D4（登记）作者内禀声明：MPI-Ro 0.83-0.87% 验证甾萜类成熟度计算准确性——"
                   "原文自带参数间一致性声明，与 D3 结果一致", True))

    # D5 维度不足（登记）
    print("\n[D5（登记）维度不足]")
    print("  ① MPI 仅正文区间 0.723-0.785（无逐样品表列）→ 无法做逐样品秩级解耦；")
    print("  ② 缺金刚烷（MDI/MAI）与轻烃（C7/Mango）列 → 陈中红式'高敏感组（轻烃/金刚烷）vs 低敏感组（甾萜/芳烃）'")
    print("     解耦不可复现（李宗亮表 4 仅'低敏感组'内部两参数：甾烷 G 与芳烃 MPI）；")
    print("  ③ G→EqVRo 换算锚点不确定性（换算 A/B 区间差异 ~0.03-0.15%）→ 绝对成熟度对照不稳定")
    checks.append(("D5（登记）维度不足：缺金刚烷/轻烃列 + MPI 仅区间 + 换算不确定——"
                   "陈中红式参数间解耦在李宗亮表 4 不可判定（诚实负结果/维度不足）", True))

    print("\n[检验]")
    n_pass = 0
    for name, ok in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
        n_pass += int(ok)
    print("结果：%d/%d 通过（D4/D5 为登记项）" % (n_pass, len(checks)))

    print("\n[解读]")
    print("  陈中红 2022 式参数间解耦（轻烃/金刚烷 > 甾萜/芳烃 = 混源）在李宗亮 2025 表 4：")
    print("  ① D1/D2：甾烷参数内部同步（G↔A ρ=%.2f）、C31 22S 饱和不敏感——单源一致性结构；" % rho)
    print("  ② D3：MPI（芳烃）与甾烷 G 的 EqVRo 区间在常规换算下重叠——无参数间解耦证据；")
    print("  ③ D4：作者内禀声明两参数一致；")
    print("  → 结论：零假设（单源、参数一致）未被拒绝，与李宗亮'自供烃+短距运移'结论一致；")
    print("    但陈中红式解耦判别器的完整复现须待含金刚烷/轻烃逐样品数据的新载体（如刘梦醒 2021")
    print("    渤中 19-6 型 MAI/MDI + Mango 轻烃表），本试算确立方法模板与数据需求清单。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
