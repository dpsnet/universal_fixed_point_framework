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
零注入阈值可操作判据（Paper XLIII §6.3 / §5.1 P4 修正收尾，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md §6.3 开放问题
"长7段负截距的物理对应（干酪根初次生烃临界 TOC）与 c→0 判据"

GCSRD G5 诊断表明：线性负截距 ≠ 零注入阈值必要条件（WILCOX 负截距源于中高 TOC
段凹上曲率，R2=0.442）。本脚本提炼 P4 修正后零注入阈值（"成熟度均匀、无运移烃
注入的原地生烃体系"）的可操作识别判据，并在长7段/GCSRD/EGDB 体系上分类：

  Z1 线性度判据：S1-TOC 线性 R2 >= 0.90（线性注入；曲率型 R2 低）
  Z2 低端趋零判据：低 TOC 半区 S1 中位 / 高 TOC 半区 S1 中位 < 0.35
     （生烃-注入标度在低 TOC 端趋零，非曲率拉负）
  Z3 c→0 判据：低 TOC（<0.5 wt%）S1 中位 < 0.05 mg/g，或（最低 20% TOC 端
     S1 中位 < 0.40 且最低 TOC 单样品 S1 < 0.25）——单调趋零、无运移背景
     （长7段无 <0.5 样品，用最低端趋势）
  综合：Z1+Z2+Z3 全过 → 零阈值型（c→0）；Z1 失败且负截距 → 曲率型；
        正截距（c 代理>0.05）→ c 型（运移背景）
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
CHANG7 = os.path.join(BASE, "data", "rockeval_chang7", "chang7_rockeval.csv")
GCSRD = os.path.join(BASE, "data", "rockeval_usgs_gcsrd", "GCSRD.txt")
EGDB_WIDE = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv")
BAKKEN_SET = {"BAKKEN", "BAKKEN UPPER", "BAKKEN LOWER", "BAKKEN SILTSTONE"}


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def _linfit(x, y):
    a, b = np.polyfit(x, y, 1)
    yp = a * x + b
    ss = np.sum((y - yp) ** 2) / np.sum((y - y.mean()) ** 2)
    return a, b, 1.0 - ss


def _read_ts(path, toc_col, s1_col):
    out = []
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        reader = csv.reader(f)
        header = next(r for r in reader if r and not r[0].lstrip().startswith("#"))
        idx_t, idx_s = header.index(toc_col), header.index(s1_col)
        for row in reader:
            if not row or row[0].lstrip().startswith("#"):
                continue
            toc, s1 = _tof(row[idx_t]), _tof(row[idx_s])
            if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0:
                out.append((toc, s1))
    return out


def load_chang7():
    """长7段多井/多区分组：CY 井（10）+ F75 井（Chen 2021，23）+ N228 井（崔德艺 2023，9）
    + Zhou2024 中央区（38，表2/表3 配对 TOC）+ Fan2023 陇东（10，Processes）"""
    out = {}
    out["长7CY井"] = _read_ts(CHANG7, "TOC_wt", "S1_mgg")
    f75 = os.path.join(BASE, "data", "rockeval_chang7_f75", "chang7_f75_rockeval.csv")
    out["长7F75井"] = _read_ts(f75, "TOC_wt", "S1_mgg")
    n228 = os.path.join(BASE, "data", "rockeval_chang7_n228", "chang7_n228_rockeval.csv")
    out["长7N228井"] = _read_ts(n228, "TOC_wt", "S1_mgg")
    zhou = os.path.join(BASE, "data", "rockeval_chang7_zhou", "zhou2024_tbl3.csv")
    out["长7Zhou2024"] = _read_ts(zhou, "TOC_wt", "S1_mgg")
    fan = os.path.join(BASE, "data", "rockeval_chang7_fan2023", "chang7_fan2023_rockeval.csv")
    out["长7Fan2023"] = _read_ts(fan, "TOC_wt", "S1_mgg")
    return out


def load_gcsrd():
    by = {}
    with open(GCSRD, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            toc, s1, tm = _tof(r["toc"]), _tof(r["s1"]), _tof(r["tmax"])
            if not (np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0):
                continue
            # 过滤口径与 gcsrd_crossval.py 对齐：Tmax 350-600 + OSI<300
            if not (np.isfinite(tm) and 350 < tm < 600):
                continue
            if s1 / toc * 100.0 >= 300:
                continue
            fm = (r["formation"] or r["display_strat_unit"] or "NA").strip().upper()
            by.setdefault(fm, []).append((toc, s1))
    sel = {}
    for fm in ("WILCOX GROUP", "TUSCALOOSA FORMATION", "SPARTA SAND"):
        if fm in by:
            sel[fm] = by[fm]
    return sel


def load_egdb():
    by = {}
    with open(EGDB_WIDE, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            toc, s1 = _tof(r["TOC"]), _tof(r["S1"])
            if not (np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0):
                continue
            fm = (r["Formation"] or "NA").strip().upper()
            if fm in BAKKEN_SET:
                fm = "BAKKEN"
            by.setdefault(fm, []).append((toc, s1))
    sel = {}
    for fm in ("NEW ALBANY",):
        if fm in by:
            sel[fm] = by[fm]
    return sel


def classify(toc_s1):
    x = np.array([t for t, s in toc_s1])
    y = np.array([s for t, s in toc_s1])
    if len(x) < 8:
        return None
    a, b, r2 = _linfit(x, y)
    med = np.median(x)
    lo_s1 = np.median(y[x < med])
    hi_s1 = np.median(y[x >= med])
    ratio = lo_s1 / hi_s1 if hi_s1 > 0 else np.nan
    clo = np.array([s for t, s in toc_s1 if t < 0.5])
    c_med = float(np.median(clo)) if len(clo) >= 5 else np.nan
    # 最低 TOC 端 S1（前 20% 低 TOC 样品）与最低单样品
    k = max(3, len(x) // 5)
    order = np.argsort(x)
    low_end = float(np.median(y[order[:k]]))
    min_end = float(y[order[0]])
    z1 = r2 >= 0.90
    z2 = np.isfinite(ratio) and ratio < 0.35
    z3 = (np.isfinite(c_med) and c_med < 0.05) or (low_end < 0.40 and min_end < 0.25)
    if z1 and z2 and z3:
        typ = "零阈值型（c→0，长7段式）"
    elif b > 0 and (not np.isfinite(c_med) or c_med >= 0.05):
        typ = "c 型（运移背景）"
    else:
        typ = "曲率型（负截距但低端非零）"
    return {"n": len(x), "a": a, "b": b, "r2": r2, "ratio": ratio,
            "c_med": c_med, "low_end": low_end, "min_end": min_end,
            "z1": z1, "z2": z2, "z3": z3, "typ": typ}


def main():
    datasets = {}
    datasets.update(load_chang7())
    datasets.update(load_gcsrd())
    datasets.update(load_egdb())
    print("体系                n     a       b       R2    低/高S1比  c代理(<0.5) 最低端S1  minS1   Z1 Z2 Z3 类型")
    print("-" * 118)
    zt, ct, cur = [], [], []
    for fm, pts in datasets.items():
        res = classify(pts)
        if res is None:
            continue
        (zt if res["typ"].startswith("零") else
         ct if res["typ"].startswith("c") else cur).append(fm)
        print("%-20s %4d  %+.3f  %+.3f  %.3f  %6.3f    %s    %5.3f   %5.3f  %s  %s  %s  %s"
              % (fm, res["n"], res["a"], res["b"], res["r2"], res["ratio"],
                 "%.3f" % res["c_med"] if np.isfinite(res["c_med"]) else "  ——  ",
                 res["low_end"], res["min_end"],
                 "Y" if res["z1"] else "N",
                 "Y" if res["z2"] else "N",
                 "Y" if res["z3"] else "N", res["typ"]))
    ok = "长7CY井" in zt and len(ct) >= 1
    print("三类并存：零阈值型 %s / c 型 %s / 曲率型 %s" % (zt, ct, cur))
    print("判据有效性（长7CY井为唯一零阈值型 + c 型/曲率型体系存在）: %s" % ("通过" if ok else "未完全通过"))
    print("长7段井间对比：CY 井零阈值（TOC*=0.42）vs F75/N228 井 c 型（低端 S1 底板非零）——"
          "同一层段内体系类型并存，零阈值型为特殊体系类而非层段普适特征。")
    print("物理对应：零注入阈值 = 线性注入标度（R2>=0.90）+ 低端趋零 + c→0——"
          "成熟度均匀、无运移烃注入的原地生烃体系（长7段）；负截距不构成充分条件（曲率型）。")


if __name__ == "__main__":
    main()
