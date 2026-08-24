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
He et al. (2026, ACS Omega 11(6), 10280-10293) 青山口组残烃分子特征复现检验（Paper XLIII，2026-08-09）
对应笔记：notes/05_condensed_matter/shale_data_inventory.md（c 项分子证据通道第一例）

数据：scripts/data/he2026_qingshankou/he2026_tables.csv（浏览器提取，忠实转录）
  Table 1：JY-1 井 Q1 段 12 页岩样品抽提产量（正己烷/二氯甲烷冷抽提 + 索氏）
  Table 2：35 样品残烃对比参数——C19-21TT/C23-25TT、C24TeT/C26TT、
           C15-sesquiterpane/8β(H)-drimane、C30-DiaH/C30H、C27-Diasteranes/C27-sterane
           （K2qn2 上段 18 油性灰黑泥岩 + K2qn1 下段 10 灰黑泥岩 + 7 砂岩/粉砂岩）

论文结论（摘要）：下段页岩残烃与相邻砂岩原油生物标志物一致（油源一致），
游离烃含量与芳香迁移参数（4-/1-MDBT、4,6-/1,4-DMDBT，仅图件）指示页岩-砂岩短距离运移；
上段与下段油源关系分异。

复现检验（c 项分子证据——"运移烃背景"第一步）：
  H0 游离烃占主体（Table 1）：冷抽提（正己烷+DCM）占抽提总量中位 > 0.5——可动油量化前提（c 项栖身游离组分）
  H1 上下段油源分异：上段页岩 vs 下段页岩各比值 MWU 显著差异（成熟度敏感参数 C30-DiaH/C30H、
     C27-重排甾烷/甾烷 应显著下段更高——下段更成熟）
  H2 下段页岩-砂岩源一致性：MWU 无显著差异（油源一致 → 短距离运移的分子证据）
  H3 上段页岩-砂岩分异：MWU 显著差异（砂岩油非上段来源）
  H4 垂向成熟度结构：深度 vs C30-DiaH/C30H、C27-重排甾烷/甾烷 Spearman 正相关（成熟度随深度增）
  H5（诚实登记）：经典成熟度比值（C29 20S/(20S+20R)、C32 22S/(22S+22R)、Ts/(Ts+Tm)、MPI）与
     4-/1-MDBT、4,6-/1,4-DMDBT 在本论文仅存在于图件（深度剖面）——表格数据无法数值复现
     "成熟度失配"本身；本检验复现的是其油源/迁移结构结论
"""
import csv
import os
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "data", "he2026_qingshankou", "he2026_tables.csv")

RATIOS = ["C19-21TT/C23-25TT", "C24TeT/C26TT", "C15-sesquiterpane/8β(H)-drimane",
          "C30-DiaH/C30H", "C27-Diasteranes/C27-sterane"]


def load_tables():
    t1, t2 = [], []
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            row = next(csv.reader([line]))
            if row[0] == "Table 1":
                t1.append(row[1:])
            elif row[0] == "Table 2":
                t2.append(row[1:])
    return t1, t2


def to_f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def group_medians(data, key):
    g = {}
    for r in data:
        k = key(r)
        if k is None:
            continue
        g.setdefault(k, []).append(r)
    return {k: np.median([to_f(r[col]) for r in rows]) for k, rows in g.items()}


def mwu(a, b, alt="two-sided"):
    return mannwhitneyu(a, b, alternative=alt)


def main():
    t1, t2 = load_tables()
    hdr = t2[0]
    rows2 = t2[1:]
    rows2 = [dict(zip(hdr, r)) for r in rows2]

    # 分组
    upper = [r for r in rows2 if r["layer"] == "K2qn2"]
    lower = [r for r in rows2 if r["layer"] == "K2qn1" and "mudstone" in r["lithology"]]
    sand = [r for r in rows2 if r["layer"] == "K2qn1" and
            ("sand" in r["lithology"] or "siltstone" in r["lithology"])]
    print("== He et al. (2026) 青山口残烃复现检验 ==")
    print("分组：上段 K2qn2 泥岩 n=%d / 下段 K2qn1 泥岩 n=%d / 砂岩粉砂岩 n=%d（含油砂 3 + 钙质砂 1 + 粉砂 3）"
          % (len(upper), len(lower), len(sand)))

    checks = []
    # H0 游离烃占主体（Table 1；含合并单元格双表头，列名在第 2 行）
    t1hdr = t1[1]
    rows1 = [dict(zip(t1hdr, r)) for r in t1[2:]]
    frac = [to_f(r["extracted hydrocarbons by n-hexane and dichloromethane/all extracted hydrocarbons"])
            for r in rows1]
    frac = [f for f in frac if f is not None]
    med_frac = float(np.median(frac))
    checks.append(("H0 游离烃占主体（Table 1 n=%d）：冷抽提占比中位 %.2f（>0.5）——可动油量化前提，c 项栖身游离组分"
                   % (len(frac), med_frac), med_frac > 0.5))

    # H1/H2/H3 成组比值 MWU
    def vals(rows, col):
        return [to_f(r[col]) for r in rows if to_f(r[col]) is not None]

    print("\n[成组中位（Table 2）]")
    print("%-32s %8s %8s %8s" % ("比值", "上段", "下段泥岩", "砂岩"))
    for c in RATIOS:
        m_up, m_lo, m_sa = np.median(vals(upper, c)), np.median(vals(lower, c)), np.median(vals(sand, c))
        print("%-32s %8.2f %8.2f %8.2f" % (c, m_up, m_lo, m_sa))

    n_h1 = 0
    for c in RATIOS:
        u, p = mwu(vals(upper, c), vals(lower, c))
        if p < 0.05:
            n_h1 += 1
    checks.append(("H1 上下段油源分异：%d/5 比值上段 vs 下段 MWU p<0.05（成熟度敏感参数 C30-DiaH/C30H、重排甾烷应显著）"
                   % n_h1, n_h1 >= 2))

    n_h2 = 0
    for c in RATIOS:
        u, p = mwu(vals(lower, c), vals(sand, c))
        if p >= 0.05:
            n_h2 += 1
    checks.append(("H2 下段页岩-砂岩源一致性：%d/5 比值无显著差异（油源一致 → 短距离运移分子证据）" % n_h2, n_h2 >= 4))

    n_h3 = 0
    for c in RATIOS:
        u, p = mwu(vals(upper, c), vals(sand, c))
        if p < 0.05:
            n_h3 += 1
    checks.append(("H3 上段页岩-砂岩分异：%d/5 比值 MWU p<0.05（砂岩油非上段来源）" % n_h3, n_h3 >= 2))

    # H4 垂向成熟度结构
    dep = [to_f(r["depth/m"]) for r in rows2]
    for c, name in [("C30-DiaH/C30H", "C30-DiaH/C30H"), ("C27-Diasteranes/C27-sterane", "重排甾烷/甾烷")]:
        x, y = [], []
        for r in rows2:
            d, v = to_f(r["depth/m"]), to_f(r[c])
            if d is not None and v is not None:
                x.append(d)
                y.append(v)
        rho, p = spearmanr(x, y)
        checks.append(("H4.%s 垂向梯度（n=%d）：深度-比值 Spearman ρ=%.3f（p=%.3g）——成熟度随深度增结构"
                       % (name, len(x), rho, p), rho > 0.3 and p < 0.05))

    # H5 诚实登记
    checks.append(("H5（登记）经典成熟度比值（20S/22S/Ts-Tm/MPI）与 4-/1-MDBT、4,6-/1,4-DMDBT 仅存在于图件（图 9/10 深度剖面），"
                   "表格数据无法数值复现'成熟度失配'本身；本检验复现油源/迁移结构结论", True))

    # H6 MDBT 迁移结构锚点（Discussion 文本数值，忠实转录）
    #   上组：4-/1-MDBT = 10.80–12.58、4,6-/1,4-DMDBT = 2.9–3.3
    #   下组：4-/1-MDBT = 9.87–15.23、4,6-/1,4-DMDBT = 3.20–4.33
    #   低值位于 2481–2484 m 与 2502–2509 m；Ro = 0.8–1.0%（成熟度不敏感区）
    mdb1_up = (10.80, 12.58); mdb1_lo = (9.87, 15.23)
    mdb2_up = (2.9, 3.3); mdb2_lo = (3.20, 4.33)
    overlap1 = max(mdb1_up[0], mdb1_lo[0]) <= min(mdb1_up[1], mdb1_lo[1])
    overlap2 = max(mdb2_up[0], mdb2_lo[0]) <= min(mdb2_up[1], mdb2_lo[1])
    checks.append(("H6（登记）MDBT 迁移结构锚点（文本）：上组 4-/1-MDBT %.2f-%.2f、4,6-/1,4-DMDBT %.1f-%.1f；"
                   "下组 %.2f-%.2f、%.2f-%.2f——上下组范围重叠=%s（非'成熟度失配'型分离，为短距离运移结构）"
                   % (mdb1_up[0], mdb1_up[1], mdb2_up[0], mdb2_up[1], mdb1_lo[0], mdb1_lo[1], mdb2_lo[0], mdb2_lo[1],
                      "是" if (overlap1 and overlap2) else "否"), overlap1 and overlap2))

    # H7 MDBT 低值深度 vs Table 2 砂岩层段重合（短距离运移进入砂岩薄层）
    #   论文：低值位于 2481–2484 / 2502–2509 m（整数米表述）；砂岩样品 2481.62–2510.32 m，
    #   其中 2509.97 m 油砂恰在"2502–2509"窗口边界（四舍五入 2510，同属砂岩层段底部）
    sand_depths = [to_f(r["depth/m"]) for r in sand]
    lo_win = [(2481.0, 2484.0), (2502.0, 2509.0)]
    hit = [d for d in sand_depths
           if any(a <= d <= b for a, b in lo_win)]
    hit_border = [d for d in sand_depths if abs(d - 2509.0) <= 1.0 and d not in hit]
    checks.append(("H7 MDBT 低值深度（2481–2484 / 2502–2509 m）与砂岩层段重合：%d/%d 砂岩样品落入低值窗口"
                   "（边界样品 %s 恰在 2509 m 四舍五入线）——MDBT 低值与砂岩薄层多数共位（运移进入砂岩的证据）"
                   % (len(hit), len(sand_depths), ", ".join("%.2f" % d for d in hit_border) if hit_border else "无"),
                   len(hit) >= max(3, int(len(sand_depths) * 0.7))))

    # H8 诚实登记：图号矛盾 + 成熟度不敏感区
    checks.append(("H8（登记）出版版图号矛盾（正文引 MDBT 剖面为图 9/图 10，实际图 9=抽提产量剖面、图 10=C15 倍半萜色谱，"
                   "无一张图与 MDBT 剖面相符）；Ro=0.8–1.0% 为成熟度不敏感区，经典成熟度比值近平衡——"
                   "严格'成熟度失配'无法用本文复现（机制实为短距离运移，非成熟度失配）", True))

    print("\n[检验]")
    n_pass = 0
    for name, ok in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
        n_pass += int(ok)
    print("结果：%d/%d 通过（H5/H6/H8 为登记项）" % (n_pass, len(checks)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
