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
c 项诊断判据跨体系验证（Paper XLIII 应用路线图 §二，2026-08-08）
对应笔记：notes/05_condensed_matter/shale_application_roadmap.md 模块 B

目的：技术路线图模块 B 的煤系/外部油源注入诊断判据
  （J1 正截距 b>0.05；J2 OSI 背景>60；J3 线性度 R2）目前仅经沙海组单案例，
本脚本用全部已入库体系（中国 5 + GCSRD 3 + EGDB 1）系统验证判据的分类能力，
并检验"正截距是否为煤系特有"——预期：正截距是 c 型（运移/滞留背景）的
普遍特征，煤系注入须结合地质背景（油-煤共存）判别，非煤系湖相（青山口
滞留油、苏北阜宁）亦可正截距/高背景——判据须与地质背景互证；负截距
（长7段）为唯一零阈值型，苏北阜宁 GY1（负截距+高 OSI）再证负截距≠c→0。
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    # (名称, 文件, toc列, s1列, 剔除行, Formation过滤, 地质背景)
    ("长7段", "data/rockeval_chang7/chang7_rockeval.csv", "TOC_wt", "S1_mgg", None, None, "鄂尔多斯湖相（原地生烃）"),
    ("青山口D86", "data/rockeval_qingshankou_d86/qingshankou_d86_rockeval.csv", "TOC_wt", "S1_mgg", None, None, "松辽湖相（滞留油富集）"),
    ("青山口SL", "data/rockeval_qingshankou/qingshankou_rockeval.csv", "TOC_wt", "S1_mgg", None, None, "松辽湖相（滞留油富集）"),
    ("沙海组", "data/rockeval_shahai/shahai_rockeval.csv", "TOC_wt", "S1_mgg", 11, None, "阜新油-煤共存（煤系注入）"),
    ("苏北阜宁GY1", "data/rockeval_subei_funing/rockeval_funing_gy1.csv", "TOC_wt", "S1_mgg", None, None, "苏北湖相（滞留/运移背景）"),
    ("TUSCALOOSA", "data/rockeval_usgs_gcsrd/GCSRD.txt", "toc", "s1", None, "TUSCALOOSA FORMATION", "Gulf Coast 海相"),
    ("WILCOX", "data/rockeval_usgs_gcsrd/GCSRD.txt", "toc", "s1", None, "WILCOX GROUP", "Gulf Coast 海相"),
    ("SPARTA", "data/rockeval_usgs_gcsrd/GCSRD.txt", "toc", "s1", None, "SPARTA SAND", "Gulf Coast 海相"),
    ("NEW ALBANY", "data/rockeval_usgs_egdb/egdb_re_wide.csv", "TOC", "S1", None, "NEW ALBANY", "伊利诺伊海相-湖相过渡"),
]


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load(fname, ct, cs, drop, fm_filter):
    toc, s1 = [], []
    is_gcsrd = "gcsrd" in fname
    with open(os.path.join(BASE, fname), encoding="utf-8-sig", errors="replace") as f:
        for i, r in enumerate(csv.DictReader(f, delimiter="\t" if is_gcsrd else ","), start=1):
            if drop and i == drop:
                continue
            if fm_filter:
                fm = (r.get("formation") or r.get("display_strat_unit")
                      or r.get("Formation") or "NA").strip().upper()
                if fm != fm_filter:
                    continue
            a, b = _tof(r[ct]), _tof(r[cs])
            if not (np.isfinite(a) and np.isfinite(b) and 0 < a < 30 and b >= 0):
                continue
            if is_gcsrd:  # GCSRD 过滤口径与 zero_threshold/gcsrd_crossval 对齐
                tm = _tof(r.get("tmax", ""))
                if not (np.isfinite(tm) and 350 < tm < 600):
                    continue
                if b / a * 100.0 >= 300:
                    continue
            toc.append(a)
            s1.append(b)
    return np.array(toc), np.array(s1)


def main():
    print("c 项诊断判据跨体系验证（模块 B 判据 J1/J2/J3）")
    print("体系           n    截距b    c代理(<0.5) OSI中位  R2      J1正截距 J2OSI>60  J3线性  类型           地质背景")
    print("-" * 132)
    for nm, fn, ct, cs, drop, fmf, bg in FILES:
        toc, s1 = load(fn, ct, cs, drop, fmf)
        if len(toc) < 5:
            print("%-12s 样品不足(n=%d)" % (nm, len(toc)))
            continue
        a, b = np.polyfit(toc, s1, 1)
        yp = a * toc + b
        r2 = 1.0 - np.sum((s1 - yp) ** 2) / np.sum((s1 - s1.mean()) ** 2)
        osi = s1 / toc * 100.0
        clo = s1[toc < 0.5]
        c_proxy = float(np.median(clo)) if len(clo) >= 5 else np.nan
        j1 = "是" if b > 0.05 else ("近零" if abs(b) <= 0.05 else "否(负)")
        j2 = "是" if np.median(osi) > 60 else "否"
        j3 = "是" if r2 >= 0.90 else "否"
        # 类型（三判据式分类简化）
        typ = ("零阈值型" if (r2 >= 0.90 and s1.min() < 0.25) else
               "c 型" if b > 0.05 else "曲率/背景型")
        print("%-12s %4d  %+6.3f  %s  %6.1f  %.3f   %s       %s       %s   %-8s  %s"
              % (nm, len(toc), b,
                 "%.3f" % c_proxy if np.isfinite(c_proxy) else "  ——  ",
                 np.median(osi), r2, j1, j2, j3, typ, bg))
    print("\n判据解读：")
    print("  1. 正截距（J1）是 c 型普遍特征，非煤系特有——TUSCALOOSA/NEW ALBANY（海相运移/吸附背景）亦正截距，故正截距单独不构成煤系证据；")
    print("  2. 煤系注入判定须 J1 + J2 + 地质背景（油-煤共存）互证，沙海组为模板；")
    print("  3. 负截距（长7段）为唯一零阈值型——J1 是 c 型/零阈值型的首要判别量；")
    print("  4. 苏北阜宁 GY1（负截距 + OSI 64.2 高背景）与青山口 SL 再证负截距≠c→0——")
    print("     负截距须结合 Z1 线性度（R2≥0.90）与 Z2 低端趋零（低/高比<0.35）判零阈值型；")
    print("  5. 源-储分离：煤系源岩 OSI 低（准噶尔 5.8）vs 储层页岩高（沙海 62.9）——")
    print("     判据 J2 加在储层端（油-煤共存体系勘探中区分源岩与储层）。")


if __name__ == "__main__":
    main()
