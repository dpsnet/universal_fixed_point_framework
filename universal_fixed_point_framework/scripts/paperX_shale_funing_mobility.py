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
苏北阜宁组多温度热解组分数据入库与可动性分析（Paper XLIII 模块 C/D，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md
数据：Frontiers in Earth Science 2025（Peng J-N et al.，DOI 10.3389/feart.2025.1650751）
      TABLE 2——27 样品多温度热解组分（游离轻油 S'1-1、游离中重油 S'1-2、吸附混溶油 S'2-1、
      总游离油、总滞留油、三类占比、干酪根裂解再生气油 S'2-2、凹陷），B 级（组分口径）。

验证（模块 C 可动性判据：高 c 背景滞留体系）：
  V1 页岩基质（Shale/Mud shale，n=10）吸附混溶油占比中位 > 60% —— 滞留主导、可动性低
  V2 夹层/邻层（interlayer/Adjacent layer，n=16）游离油占比中位 > 50% —— 游离主导
  V3 夹层/邻层总滞留油中位 > 2×页岩基质 —— 含油量分异（夹层富油）
  V4 页岩基质游离油占比上限 < 60% —— 页岩基质无可动油富集（模块 C：高 c 背景体系 OSI 基准须修正）
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "data", "rockeval_subei_funing", "funing_multitemp_components.csv")


def _f(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    shale = [r for r in rows if r["Sample_position"] in ("Shale", "Mud shale")]
    adj = [r for r in rows if r["Sample_position"] in ("interlayer", "Adjacent layer")]

    def free_pct(grp):
        return np.array([_f(r["Pct_S11_over_retained"]) + _f(r["Pct_S12_over_retained"])
                         for r in grp if np.isfinite(_f(r["Pct_S11_over_retained"]))])

    def ads_pct(grp):
        return np.array([_f(r["Pct_S21_over_retained"]) for r in grp if np.isfinite(_f(r["Pct_S21_over_retained"]))])

    def total_oil(grp):
        return np.array([_f(r["Total_retained_oil_mgg"]) for r in grp if np.isfinite(_f(r["Total_retained_oil_mgg"]))])

    f_sh, a_sh = free_pct(shale), ads_pct(shale)
    f_adj, a_adj = free_pct(adj), ads_pct(adj)
    t_sh, t_adj = total_oil(shale), total_oil(adj)

    v1 = np.median(a_sh) > 60
    v2 = np.median(f_adj) > 50
    v3 = np.median(t_adj) > 2 * np.median(t_sh)
    v4 = f_sh.max() < 60

    print("苏北阜宁组 27 样品（B 级组分口径，Frontiers 2025）")
    print("页岩基质 n=%d：吸附占比中位 %.1f%%、游离占比中位 %.1f%%（范围 [%.1f, %.1f]）、总滞留中位 %.2f mg/g"
          % (len(shale), np.median(a_sh), np.median(f_sh), f_sh.min(), f_sh.max(), np.median(t_sh)))
    print("夹层/邻层 n=%d：游离占比中位 %.1f%%（范围 [%.1f, %.1f]）、吸附占比中位 %.1f%%、总滞留中位 %.2f mg/g"
          % (len(adj), np.median(f_adj), f_adj.min(), f_adj.max(), np.median(a_adj), np.median(t_adj)))
    checks = [
        ("V1 页岩基质吸附占比中位 %.1f%% > 60（滞留主导、可动性低）" % np.median(a_sh), v1),
        ("V2 夹层/邻层游离占比中位 %.1f%% > 50（游离主导）" % np.median(f_adj), v2),
        ("V3 夹层/邻层总滞留中位 %.2f > 2×页岩基质 %.2f（含油量分异 %.1f×）"
         % (np.median(t_adj), np.median(t_sh), np.median(t_adj) / np.median(t_sh)), v3),
        ("V4 页岩基质游离占比上限 %.1f%% < 60（无可动油富集，模块 C 判据：高 c 背景体系 OSI 基准须修正）" % f_sh.max(), v4),
    ]
    n_pass = 0
    for name, ok in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
        n_pass += int(ok)
    print("结果：%d/%d 通过" % (n_pass, len(checks)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
