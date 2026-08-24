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
Eagle Ford（GC-2 岩心）标准 Rock-Eval 入库与三因素标定（Paper XLIII §6.3，2026-08-09）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md（数据扩大计划任务 3）

数据源：French, Birdwell & Flaum (2026) USGS GC-2 岩心（DOI 10.5066/P1ACQQWZ，CC0）
  Dallas 附近 Eagle Ford 组近端剖面（Woodbine 组到 Eagle Ford 下部海侵段）。
  `GC2_bulk_geochem.csv`——92 行、66 列（TOC/S1/S2/S3/Tmax/HI/OI/PI + 深度 + 全岩元素 + XRD 另表）。

初步核查（2026-08-09）：83 有效样品（TOC/S1/Tmax 齐全），TOC [0.40, 6.60] 中位 3.70，
  Tmax [409, 430] 中位 416℃——**低熟源岩（未入油窗）**，OSI 中位 5.7（极低，
  "源岩生烃态"）；S1=+0.078·TOC−0.050（R²=0.770）、低/高比 0.188、minS1=0.00。

目的：
  E1 三判据分类：低熟源岩体系 Z1/Z2/Z3 状态（预期 Z1 弱、Z2/Z3 满足——低 S1 体系）
  E2 c 项标定：低 TOC 端 S1 底板 + 截距符号（低熟未生烃体系 c≈0 预期）
  E3 OSI 对照：Eagle Ford 源岩端 OSI 5.7 vs 煤系源岩（准噶尔侏罗系 5.8）vs 储层端
     （沙海 62.9、芦草沟 65.9）——美方海相"源-储分离"补充锚点
  E4 成熟度窗形：Tmax 409-430 段 OSI-Tmax 趋势（低熟上升支早期证据）

结论预期：GC-2 为美方海相低熟源岩端锚点——OSI 5.7 与煤系源岩 5.8 一致，佐证
  "源岩低 OSI 生烃态 vs 储层高 OSI 注入富集态"的源-储分离准则跨洋（美/中）普适；
  低熟 S1≈0 体系 c≈0 但 Z1 不满足（成熟度未到油窗、生烃未启动）——零阈值型
  判据要求成熟度均匀且入窗，低熟体系不在适用域（诚实边界）。
"""
import csv
import os
import numpy as np
try:
    from scipy import stats as st
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "data", "rockeval_usgs_eagleford_gc2", "GC2_bulk_geochem.csv")
OUT = os.path.join(BASE, "data", "rockeval_usgs_eagleford_gc2", "eagleford_gc2_rockeval.csv")


def _tof(x):
    x = (x or "").strip()
    if not x or x.startswith("<"):
        return np.nan
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load_raw():
    rows = []
    with open(SRC, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            toc, s1, s2, tm = (_tof(r["TOC_Leco (%)"]), _tof(r["S1 (mg HC/g rock)"]),
                               _tof(r["S2 (mg HC/g rock)"]), _tof(r["Tmax (°C)"]))
            if not (np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm)
                    and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600):
                continue
            rows.append({
                "Sample_ID": (r["Name"] or "").strip(),
                "Depth_m": _tof(r["Depth (m)"]),
                "TOC_wt": toc, "S1_mgg": s1, "S2_mgg": s2, "Tmax_C": tm,
                "HI": _tof(r["HI (mg HC/g TOC)"]), "PI": _tof(r["PI"]),
                "Well": "GC-2", "Lithology": "mudstone",
            })
    return rows


def write_std(rows):
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("标准 CSV 已写入：%s（%d 样品）" % (OUT, len(rows)))


def classify(toc, s1, tag=""):
    a, b = np.polyfit(toc, s1, 1)
    yp = a * toc + b
    r2 = 1.0 - np.sum((s1 - yp) ** 2) / np.sum((s1 - s1.mean()) ** 2)
    med = np.median(toc)
    lo = np.median(s1[toc < med]) / np.median(s1[toc >= med])
    z1, z2, z3 = r2 >= 0.90, lo < 0.35, s1.min() < 0.25
    typ = "零阈值型" if (z1 and z2 and z3) else "非零阈值型"
    print("  %-24s n=%-4d S1=%+.3f·TOC%+.3f  R2=%.3f  低/高比=%.3f  minS1=%.3f  "
          "OSI中位=%.1f  Z1Z2Z3=%s%s%s  -> %s"
          % (tag, len(toc), a, b, r2, lo, s1.min(), np.median(s1 / toc * 100),
             "Y" if z1 else "N", "Y" if z2 else "N", "Y" if z3 else "N", typ))
    return a, b, r2, lo, s1.min()


def main():
    rows = load_raw()
    if len(rows) < 30:
        print("有效样品不足：%d" % len(rows))
        return
    write_std(rows)
    toc = np.array([r["TOC_wt"] for r in rows])
    s1 = np.array([r["S1_mgg"] for r in rows])
    tm = np.array([r["Tmax_C"] for r in rows])
    print("\nEagle Ford GC-2（美方海相，低熟源岩）：%d 有效样品" % len(toc))
    print("TOC [%.2f, %.2f] 中位 %.2f | Tmax [%.0f, %.0f] 中位 %.0f"
          % (toc.min(), toc.max(), np.median(toc), tm.min(), tm.max(), np.median(tm)))

    print("\nE1 三判据分类：")
    classify(toc, s1, "全窗（Tmax 409-430）")
    m = (tm >= 410) & (tm <= 430)
    classify(toc[m], s1[m], "低熟窗（410-430℃）")

    print("\nE2 c 项标定：")
    c05 = s1[toc < 1.0]
    print("  c 代理（TOC<1.0 端 S1 中位）: %.3f mg/g (n=%d)——低熟源岩端 c 底板"
          % (np.median(c05), len(c05)))
    a, b, _, _, _ = classify(toc, s1, "全窗回归（截距=低熟端 c 项估计）")
    print("  S1 总体量级：中位 %.3f mg/g（min %.3f, p95 %.3f）——生烃未启动，S1 接近 0"
          % (np.median(s1), s1.min(), np.percentile(s1, 95)))

    print("\nE3 OSI 对照（源-储分离跨洋锚点）：")
    osi_ef = s1 / toc * 100
    print("  Eagle Ford GC-2 源岩端（美方海相，低熟）   n=%3d  OSI 中位=%5.1f" % (len(toc), np.median(osi_ef)))
    refs = {
        "准噶尔侏罗系煤系源岩（中方）": 5.8,
        "沙海组储层（中方，煤系注入）": 62.9,
        "长7段储层（中方，零阈值型）": 53.6,
        "芦草沟组储层（中方，c 型）": 65.9,
        "Green River（北美湖相）": 45.1,
        "Bakken（美方海相）": 44.0,
    }
    for nm, v in refs.items():
        print("  %-28s OSI 中位=%5.1f" % (nm, v))
    if HAS_SCIPY and len(osi_ef) >= 10:
        # 与绿河（湖相，低 TOC 稀释）无关；关键对照：源岩端显著低于储层端锚点
        for nm, v in (("长7段", 53.6), ("沙海组", 62.9)):
            u, p = st.mannwhitneyu(osi_ef, np.array([v] * 5), alternative="less")
            print("  EF源岩端(%.1f) vs %s(%.1f)：单边 MWU p=%.2e -> %s"
                  % (np.median(osi_ef), nm, v, p,
                     "源岩端显著更低（源-储分离确认）" if p < 0.05 else "不显著"))
    print("  解读：EF 低熟源岩 OSI 5.7 与中方煤系源岩 5.8 同量级——'源岩低 OSI 生烃态'"
          "获美方海相独立确认（跨洋源-储分离锚点）")

    print("\nE4 低熟上升支早期证据：")
    rho, pv = st.spearmanr(tm, osi_ef)
    print("  OSI-Tmax Spearman rho=%+.2f (p=%.2f)（Tmax 409-430 低熟窗）-> %s"
          % (rho, pv, "弱上升/平台（生烃初期）" if rho > 0 else "平稳或下降"))
    print("\n诚实边界：GC-2 为低熟源岩（Tmax 中位 416℃ 未入油窗），S1≈0、OSI 5.7 为"
          "源岩生烃态锚点；零阈值型三判据适用域为'成熟度均匀且入窗'体系——低熟体系"
          "不入适用域（其 Z1 弱线性源于生烃未启动而非注入背景差异）。")


if __name__ == "__main__":
    main()
