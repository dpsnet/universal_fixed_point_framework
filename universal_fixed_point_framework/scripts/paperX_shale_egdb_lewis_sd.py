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
P1-1b：EGDB 零阈值型候选深化诊断——LEWIS（South Dakota）近零阈值 + SUZAK 反例
（Paper XLIII 适用域边界测试，2026-08-09）

背景（P1-1 初筛）：
  窄窗口径（Tmax 中位±10℃，成熟度均匀）下：
  - LEWIS_SD n=51：S1=+0.356·TOC−0.207（R²=0.970）、低/高=0.37（略超 0.35 线）、
    minS1=0.020、OSI=13.3——近零阈值候选（仅 Z2 边界），TOC\*=0.207/0.356≈0.58
  - SUZAK n=21：S1=+0.342·TOC−0.101（R²=0.995 完美线性），但低/高=0.50 低端不趋零
    ——线性度≠零阈值的独立反例

本步深化：
  D1 LEWIS_SD 分层来源（State/County）与成熟度结构——确认是否"成熟度均匀、无注入"
  D2 LEWIS_SD 三判据敏感性：Z2 判据线 0.35 附近的稳健性（半区分割方式、低端截断）
  D3 LEWIS_SD TOC\* 与长7段（0.42）对比——生烃启动临界物理一致性
  D4 SUZAK 低端不趋零的机制诊断（低 TOC 端 S1 底板？干酪根类型切换？）
"""
import csv
import os
import re
from collections import Counter, defaultdict
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
EGDB_WIDE = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv")


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def _norm(fm):
    if not fm:
        return ""
    fm = re.sub(r"\s+", " ", fm.upper().strip())
    fm = fm.replace("/", "_").replace("-", "_")
    return fm


def load(fm_target):
    fm_target = _norm(fm_target)
    rows = []
    with open(EGDB_WIDE, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            if _norm(r["Formation"]) != fm_target:
                continue
            toc = _tof(r["TOC"])
            if not np.isfinite(toc):
                toc = _tof(r["TOC_Leco"])
            s1, tm = _tof(r["S1"]), _tof(r["TMAX"])
            if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0:
                osi = s1 / toc * 100.0
                if osi < 300:
                    rows.append({"toc": toc, "s1": s1, "tm": tm,
                                 "state": (r["State"] or "").strip(),
                                 "county": (r["County"] or "").strip()})
    return rows


def d1_source(rows, tag):
    """D1 分层来源与成熟度结构"""
    st = Counter(r["state"] for r in rows)
    co = Counter((r["state"], r["county"]) for r in rows)
    tms = [r["tm"] for r in rows if np.isfinite(r["tm"])]
    print("  %s n=%d  State: %s" % (tag, len(rows), dict(st)))
    print("    County top5: %s" % dict(co.most_common(5)))
    if tms:
        print("    Tmax [%.0f, %.0f] 中位 %.0f（p10-p90: %.0f-%.0f）"
              % (min(tms), max(tms), np.median(tms),
                 np.percentile(tms, 10), np.percentile(tms, 90)))


def d2_z2_sensitivity(rows, tag):
    """D2 Z2 低/高比敏感性：中位分割 vs 低端截断（TOC<0.75 vs >1.5）"""
    toc = np.array([r["toc"] for r in rows])
    s1 = np.array([r["s1"] for r in rows])
    med = np.median(toc)
    r_med = np.median(s1[toc < med]) / np.median(s1[toc >= med])
    lo = s1[(toc > 0) & (toc < 0.75)]
    hi = s1[(toc > 1.5)]
    r_lo = np.median(lo) / np.median(hi) if len(lo) and len(hi) else np.nan
    print("  %s Z2 低/高比：中位分割=%.3f（判据线 0.35）；低端(TOC<0.75, n=%d) vs "
          "高端(TOC>1.5, n=%d) 中位比=%.3f" % (tag, r_med, len(lo), len(hi), r_lo))


def d3_tocstar(rows, tag):
    """D3 TOC* = -b/a"""
    toc = np.array([r["toc"] for r in rows])
    s1 = np.array([r["s1"] for r in rows])
    a, b = np.polyfit(toc, s1, 1)
    ts = -b / a
    print("  %s TOC* = -b/a = %.3f/%.3f ≈ %.2f wt%%（长7段 0.42 参照）"
          % (tag, -b, a, ts))


def d4_suzak_low_end(rows, tag):
    """D4 SUZAK 低端机制：低 TOC 端 S1 分布"""
    toc = np.array([r["toc"] for r in rows])
    s1 = np.array([r["s1"] for r in rows])
    for lo, hi, nm in ((0, 0.5, "TOC<0.5"), (0.5, 1.0, "0.5-1.0"),
                       (1.0, 2.0, "1.0-2.0"), (2.0, 30, "TOC>2.0")):
        m = (toc >= lo) & (toc < hi)
        if m.sum():
            print("    %-10s n=%-4d S1 中位=%.3f min=%.3f max=%.3f OSI 中位=%.1f"
                  % (nm, m.sum(), np.median(s1[m]), s1[m].min(), s1[m].max(),
                     np.median(s1[m] / toc[m] * 100)))


def main():
    for fm, tag in (("LEWIS /SD/", "LEWIS_SD"), ("SUZAK", "SUZAK")):
        rows = load(fm)
        if not rows:
            print("%s：无数据" % tag)
            continue
        print("\n=== %s ===" % tag)
        d1_source(rows, tag)
        d2_z2_sensitivity(rows, tag)
        d3_tocstar(rows, tag)
        if tag == "SUZAK":
            d4_suzak_low_end(rows, tag)


if __name__ == "__main__":
    main()
