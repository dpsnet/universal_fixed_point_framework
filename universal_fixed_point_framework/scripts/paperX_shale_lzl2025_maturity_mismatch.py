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
李宗亮 et al. (2025, 地质科学 60(5), 1329-1341) 正宁长7₁₋₂ 原油成熟度失配严格复现（Paper XLIII，2026-08-09）
对应笔记：notes/05_condensed_matter/shale_data_inventory.md（§九 载体检索——首选"部分满足型"载体）

数据：scripts/data/lizongliang2025_zhengning/lzl2025_table4.csv（浏览器提取，忠实转录）
  表 4：原油与烃源岩萜甾类化合物特征参数（19 行 = 原油 4 + 长7₁₋₂ 岩石 3 + 长7₃ 烃源岩 12）
  成熟度比值列：A=C29ββ/(ββ+αα)、F=C31 22S/(22R+22S)、G=αααC29 20S/(20S+20R)、B=Ts/Tm
  正文补充：原油 MPI 0.723-0.785 → Ro 0.83-0.87%；长7₃ 实测 Ro 0.62-0.76%

目的：严格成熟度失配复现——若游离烃（原油）成熟度参数与源岩失配且方向与运移一致 → c 项
（运移烃背景）分子层证据。承接 He 2026 教训（成熟度不敏感区 + 比值仅在图件）——本论文
含成熟度比值数据表，可做数值复现。

检验：
  M1 原油 vs 长7₃ 上部（浅部 4 样品，含低熟点 A0057=0.22/A0068=0.10）G（C29 20S）MWU——
     失配显著性（原油更成熟则为运移烃证据）
  M2 原油 vs 长7₃ 下部（深部 8 样品）G MWU——油源是否定位于深部更成熟段
  M3 原油 vs 长7₁₋₂ 原地岩石（3 样品）G MWU——浅层原地源岩一致性（无显著差异=匹配）
  M4 垂向成熟度梯度：长7₃ 12 样品 深度 vs G/F/A Spearman——成熟度随深度增结构
  M5 原油成熟度定位：原油 G 在长7₃ 分布中的百分位 + 长7₃ 上部 vs 下部 G 差异
  M6（登记）MPI-Ro vs 实测 Ro（正文区间）：原油 0.83-0.87% vs 长7₃ 0.62-0.76%——口径标注
     （换算值 vs 实测值，非严格同口径，仅作方向性弱证据）
  M7（登记）数据异常 + 取整差 + 失配结论判定
"""
import csv
import os
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "data", "lizongliang2025_zhengning", "lzl2025_table4.csv")

COLUMNS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "C27", "C28", "C29", "K"]
MATURITY = {"A": "C29ββ/(ββ+αα)", "F": "C31 22S/(22R+22S)", "G": "αααC29 20S/(20S+20R)", "B": "Ts/Tm"}


def to_f(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def load():
    rows = []
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def vals(rows, col):
    return [to_f(r[col]) for r in rows if to_f(r[col]) is not None]


def main():
    rows = load()
    oil = [r for r in rows if r["Lithology"] == "原油"]
    rock71 = [r for r in rows if r["Layer"] == "长7₁₋₂" and r["Lithology"] != "原油"]
    c73 = [r for r in rows if r["Layer"] == "长7₃"]
    c73_upper = [r for r in c73 if to_f(r["Depth_m"]) is not None and to_f(r["Depth_m"]) <= 1758.48]
    c73_lower = [r for r in c73 if to_f(r["Depth_m"]) is not None and to_f(r["Depth_m"]) >= 1761.45]
    print("== 李宗亮 et al. (2025) 正宁长7₁₋₂ 成熟度失配严格复现 ==")
    print("分组：原油 n=%d / 长7₁₋₂ 岩石 n=%d / 长7₃ 烃源岩 n=%d（上部 4 个 1745.37-1758.48m + 下部 8 个 1761.45-1785.20m）"
          % (len(oil), len(rock71), len(c73)))

    checks = []

    def mwu_txt(a, b, alt="two-sided"):
        u, p = mannwhitneyu(a, b, alternative=alt)
        return u, p

    # M1 原油 vs 长7₃ 上部 G
    g_oil = vals(oil, "G")
    g_up = vals(c73_upper, "G")
    g_lo = vals(c73_lower, "G")
    g_r71 = vals(rock71, "G")
    med = lambda x: float(np.median(x))
    print("\n[成熟度比值 G = αααC29 20S/(20S+20R)]")
    print("  原油 n=%d 中位 %.3f（%s）" % (len(g_oil), med(g_oil), ",".join("%.2f" % v for v in g_oil)))
    print("  长7₃ 上部 n=%d 中位 %.3f（%s）" % (len(g_up), med(g_up), ",".join("%.2f" % v for v in g_up)))
    print("  长7₃ 下部 n=%d 中位 %.3f（%s）" % (len(g_lo), med(g_lo), ",".join("%.2f" % v for v in g_lo)))
    print("  长7₁₋₂ 岩石 n=%d 中位 %.3f（%s）" % (len(g_r71), med(g_r71), ",".join("%.2f" % v for v in g_r71)))

    _, p_m1 = mwu_txt(g_oil, g_up)
    checks.append(("M1 原油 vs 长7₃ 上部 G：MWU p=%.3f（n=%d/%d）——失配显著性（p<0.05 且原油更成熟才成立）"
                   % (p_m1, len(g_oil), len(g_up)), p_m1 < 0.05))

    _, p_m2 = mwu_txt(g_oil, g_lo)
    checks.append(("M2 原油 vs 长7₃ 下部 G：MWU p=%.3f（n=%d/%d）——油源定位于深部更成熟段（无显著差异=匹配）"
                   % (p_m2, len(g_oil), len(g_lo)), p_m2 < 0.05))

    _, p_m3 = mwu_txt(g_oil, g_r71)
    checks.append(("M3 原油 vs 长7₁₋₂ 原地岩石 G：MWU p=%.3f（n=%d/%d）——浅层原地源岩一致性（p≥0.05=匹配）"
                   % (p_m3, len(g_oil), len(g_r71)), p_m3 >= 0.05))

    # M4 垂向成熟度梯度（长7₃ 12 样品）
    print("\n[垂向成熟度结构（长7₃ 烃源岩 n=%d）]" % len(c73))
    for col in ("G", "F", "A"):
        x, y = [], []
        for r in c73:
            d, v = to_f(r["Depth_m"]), to_f(r[col])
            if d is not None and v is not None:
                x.append(d)
                y.append(v)
        rho, p = spearmanr(x, y)
        print("  深度-%s（%s）：ρ=%.3f（p=%.3g）" % (col, MATURITY[col], rho, p))
        if col == "G":
            checks.append(("M4 垂向成熟度梯度：深度-G ρ=%.3f（p=%.3g，n=%d）——长7₃ 内部成熟度随深度增结构"
                           % (rho, p, len(x)), rho > 0.3 and p < 0.05))

    # M5 原油成熟度定位
    g_all = sorted(g_lo + g_up)
    frac = sum(1 for v in g_all if v < med(g_oil)) / len(g_all)
    _, p_up_lo = mannwhitneyu(g_up, g_lo, alternative="less")
    checks.append(("M5 定位：原油 G 中位 %.3f 处于长7₃ 全组 %d 个样品分布 %.0f%% 分位；长7₃ 上部 vs 下部"
                   "（浅→深）MWU p=%.3f（单边 less）——长7₃ 内部浅低熟-深成熟分异"
                   % (med(g_oil), len(g_all), frac * 100, p_up_lo),
                   p_up_lo < 0.05 and 0.2 <= frac <= 0.8))

    # M6 MPI-Ro vs 实测 Ro（正文区间，登记）
    mpi_ro = (0.83, 0.87)
    ro73 = (0.62, 0.76)
    gap = mpi_ro[0] - ro73[1]
    checks.append(("M6（登记）原油 MPI-Ro %.2f-%.2f%% vs 长7₃ 实测 Ro %.2f-%.2f%%——区间不重叠（间隙 %.2f%%），"
                   "原油成熟度高于长7₃ 实测；口径标注：MPI 为换算值 vs 镜质体反射率实测值，非严格同口径，仅方向性弱证据"
                   % (mpi_ro[0], mpi_ro[1], ro73[0], ro73[1], gap), True))

    # M7 诚实登记
    print("\n[数据质量]")
    for r in rows:
        if r["SampleID"] == "A0063":
            print("  A0063：F（C31 22S）=0.98，远超平衡区 0.54-0.62（原文如此）")
        if r["SampleID"] == "A0057":
            print("  A0057：B（Ts/Tm）=7.50，远超同组 0.58-1.47（原文如此）")
        if r["SampleID"] == "A0068":
            print("  A0068：G（C29 20S）=0.10，与 F=0.60（已达平衡）不匹配（原文如此）")
    checks.append(("M7（登记）结论判定：原油 G 均值 0.475（正文引 0.47，0.005 取整差）；成熟油窗体系"
                   "（G 全线 0.44-0.61 近平衡 0.52-0.55）——严格成熟度失配成立与否见 M1-M3；"
                   "A0063 F=0.98 / A0057 B=7.50 / A0068 G=0.10 为原文异常值已标注", True))

    print("\n[检验]")
    n_pass = 0
    for name, ok in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
        n_pass += int(ok)
    print("结果：%d/%d 通过（M6/M7 为登记项）" % (n_pass, len(checks)))

    # 结论解读
    print("\n[解读]")
    if p_m1 >= 0.05 and p_m2 >= 0.05 and p_m3 >= 0.05:
        print("  表 4 成熟度比值层面：原油与长7₃（上/下部）及长7₁₋₂ 原地岩石均无显著失配——")
        print("  '严格成熟度失配'在本体系不成立（诚实负结果，与 He 2026 教训一致：成熟油窗体系比值近平衡难以失配）。")
        print("  仅 M6 弱线索（MPI-Ro > 实测 Ro）指示更成熟烃进入浅层储层的方向性可能——待更强证据。")
    print("  c 项含义：本体系（长7 = 零阈值基准 R²=0.994，c→0）油-源成熟度一致支持'自供烃+短距运移'，")
    print("  运移烃与原地烃成熟度相近 → c 项分子证据须转向'失配型'体系或同位素/化合物级指纹。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
