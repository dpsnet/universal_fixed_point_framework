#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EGDB 跨体系 c 项属性驱动检验（Paper XLIII §6.3，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md §6.3 开放问题 2
"c 与盆地属性（规模/断裂系统/成熟度结构）的关系待建立"

目的：用 EGDB 体系中可观测属性（埋深 TopDepth_ft、成熟度结构 Tmax p95 /
过成熟占比 Tmax>465）检验 c 代理（TOC<0.5 wt% 端 S1 中位数）的驱动因素：

  C1 埋深驱动：c 随体系中位埋深增加（深部高压封闭/运移烃富集）
  C2 成熟度结构驱动：c 随体系 Tmax p95 或过成熟占比（Tmax>465℃）增加
     （体系经历更充分的生烃-排烃-运移循环 → 背景烃积累）
  C3 代理稳健性：两个 c 代理（低 TOC 端 S1 中位 vs 全体系 OSI 中位）秩一致

结论预期（不确定，诚实报告）：若 C1/C2 正相关成立，c 的体系差异可由埋深/
成熟度结构部分解释；若不成立，c 差异主要归因于未观测属性（断裂系统/砂条
规模/运移通道），登记负结果。
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
EGDB_WIDE = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv")

BAKKEN_SET = {"BAKKEN", "BAKKEN UPPER", "BAKKEN LOWER", "BAKKEN SILTSTONE"}
MIN_N = 150


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load_systems():
    """返回 {体系: dict(深度列表, Tmax列表, 低TOC的S1列表, 全OSI列表)}"""
    sysd = {}
    with open(EGDB_WIDE, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            toc, s1, tm = _tof(r["TOC"]), _tof(r["S1"]), _tof(r["TMAX"])
            if not (np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm)
                    and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600):
                continue
            o = s1 / toc * 100.0
            if o >= 300:
                continue
            dep = _tof(r["TopDepth_ft"])
            fm = (r["Formation"] or "NA").strip().upper()
            if fm in BAKKEN_SET:
                fm = "BAKKEN"
            d = sysd.setdefault(fm, {"dep": [], "tm": [], "s1lo": [], "osi": []})
            d["tm"].append(tm)
            d["osi"].append(o)
            if np.isfinite(dep):
                d["dep"].append(dep)
            if toc < 0.5:
                d["s1lo"].append(s1)
    return sysd


def main():
    if not HAS_SCIPY:
        print("需要 scipy")
        return
    sysd = load_systems()
    print("体系         n    深中位ft  深范围       Tmax中位  Tmax p95  过成熟占比  c代理(TOC<0.5 S1)  OSI中位")
    print("-" * 110)
    rows = []
    for fm, d in sorted(sysd.items(), key=lambda kv: -len(kv[1]["tm"])):
        if len(d["tm"]) < MIN_N:
            continue
        tm = np.array(d["tm"])
        dep = np.array(d["dep"]) if d["dep"] else np.array([])
        s1lo = np.array(d["s1lo"]) if d["s1lo"] else np.array([])
        osi = np.array(d["osi"])
        over_frac = float((tm > 465).mean())
        c1 = float(np.median(s1lo)) if len(s1lo) >= 10 else np.nan
        rows.append({
            "fm": fm, "n": len(tm),
            "dep_med": float(np.median(dep)) if len(dep) else np.nan,
            "dep_hi": float(np.max(dep)) if len(dep) else np.nan,
            "tm_med": float(np.median(tm)), "tm_p95": float(np.percentile(tm, 95)),
            "over_frac": over_frac, "c1": c1, "osi_med": float(np.median(osi)),
        })
        dep_s = ("%.0f-%.0f" % (dep.min(), dep.max())) if len(dep) else "——"
        print("%-12s n=%5d  %8.0f  %14s  %7.1f  %7.1f  %7.1f%%  c=%.3f(n=%d)  %6.1f"
              % (fm, len(tm),
                 rows[-1]["dep_med"] if np.isfinite(rows[-1]["dep_med"]) else 0,
                 dep_s, tm_med if (tm_med := np.median(tm)) else 0,
                 rows[-1]["tm_p95"], over_frac * 100,
                 c1 if np.isfinite(c1) else float('nan'),
                 len(s1lo), np.median(osi)))
    # C1 埋深驱动：c 代理 vs 体系中位深度
    pairs = [(r["dep_med"], r["c1"]) for r in rows
             if np.isfinite(r["dep_med"]) and np.isfinite(r["c1"])]
    if len(pairs) >= 4:
        rho, pv = st.spearmanr([p[0] for p in pairs], [p[1] for p in pairs])
        c1ok = rho > 0.3 and pv < 0.3
        print("C1 埋深驱动: n=%d 体系, rho(c, 深中位)=%+.2f (p=%.2f) -> %s"
              % (len(pairs), rho, pv,
                 "c 随埋深增加（深部封闭/运移烃富集）" if c1ok
                 else "c-埋深无显著关联"))
    else:
        c1ok = False
        print("C1 埋深驱动: 有效体系不足")
    # C2 成熟度结构驱动：c 代理 vs Tmax p95 / 过成熟占比
    pairs2 = [(r["tm_p95"], r["c1"]) for r in rows if np.isfinite(r["c1"])]
    if len(pairs2) >= 4:
        rho2, pv2 = st.spearmanr([p[0] for p in pairs2], [p[1] for p in pairs2])
        c2ok = rho2 > 0.3 and pv2 < 0.3
        print("C2 成熟度结构: n=%d 体系, rho(c, Tmax p95)=%+.2f (p=%.2f) -> %s"
              % (len(pairs2), rho2, pv2,
                 "c 随体系成熟度上限增加（排烃-运移循环充分）" if c2ok
                 else "c-成熟度上限无显著关联"))
    else:
        c2ok = False
        print("C2 成熟度结构: 有效体系不足")
    # C3 代理稳健性：c1（低 TOC S1）vs OSI 中位
    pairs3 = [(r["c1"], r["osi_med"]) for r in rows if np.isfinite(r["c1"])]
    if len(pairs3) >= 4:
        rho3, pv3 = st.spearmanr([p[0] for p in pairs3], [p[1] for p in pairs3])
        c3ok = rho3 > 0.3
        print("C3 代理稳健性: n=%d 体系, rho(c1, OSI中位)=%+.2f (p=%.2f) -> %s"
              % (len(pairs3), rho3, pv3,
                 "两代理一致（c 信号稳健）" if c3ok else "两代理不一致"))
    else:
        c3ok = False
        print("C3 代理稳健性: 有效体系不足")
    print("汇总: %d/3" % (int(c1ok) + int(c2ok) + int(c3ok)))


if __name__ == "__main__":
    main()
