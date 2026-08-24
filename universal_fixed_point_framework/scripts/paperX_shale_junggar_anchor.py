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
准噶尔侏罗系煤系源岩锚点分析（Paper XLIII 模块 B 补充，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md
数据审计结论：
  ① [C1] 地质力学学报 2026（八道湾组 78 件）表 2 为【汇总统计】（两凹陷范围+均值），
     逐样品 TOC/S1/S2 未发表——"逐样品表为 PDF 图片待转录"为错误假设，C 级定位由
     发表形式限制决定；升级路径 = 联系作者（通讯作者李宝庆 libq@cug.edu.cn）。
  ② 替代 OA 来源审计：
     - Petroleum Science 2024（Ge et al.，DOI 10.1016/j.petsci.2024.03.011）：
       19 样品逐样品（泥岩 10 + 碳质泥岩 6 + 煤 3，含 J1b 八道湾组 6 个），
       **口径为 S1+S2（生烃潜量），无单独 S1**——无法算 OSI，不能做模块 B 判据分类；
     - ACS Omega 2024（Gong et al.，DOI 10.1021/acsomega.3c05448）：
       142 样品 Rock-Eval 调查仅公布 6 个代表样品（含 J1b 煤/碳质泥岩/暗色泥岩），
       **有单独 S1**——可算 OSI，但样本量小（锚点级）。

验证（煤系源岩 OSI 锚点 vs 沙海组储层对比）：
  V1 ACS 6 样品（低成熟 vRo 0.43-0.62）OSI 中位 < 20 —— 煤系源岩端 S1 丰度低
  V2 沙海组页岩（[U6]）OSI 中位 > 60 而 ACS 锚点 OSI 中位 < 20 —— 源-储分离对比
  V3 J1b（八道湾组）样品在 19 件全表中可辨识（n≥3）—— 油-煤共存体系定位
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, "data", "rockeval_junggar_jurassic")


def _load(fn):
    with open(os.path.join(D, fn), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _f(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def _shahai():
    rows = list(csv.DictReader(
        open(os.path.join(BASE, "data", "rockeval_shahai", "shahai_rockeval.csv"), encoding="utf-8-sig")))
    out = []
    for i, r in enumerate(rows, start=1):
        if i == 11:  # 沙海组 #11 Tmax=541 煤系异常（既有口径）
            continue
        osi = _f(r["S1_mgg"]) / _f(r["TOC_wt"]) * 100
        if np.isfinite(osi):
            out.append(osi)
    return out


def main():
    acs = _load("junggar_jurassic_acs_anchor.csv")
    ps = _load("junggar_jurassic_rockeval.csv")

    # V1/V2：ACS 锚点 OSI
    osi = np.array([_f(r["S1_mgg"]) / _f(r["TOC_wt"]) * 100 for r in acs])
    osi = osi[np.isfinite(osi)]
    sh_osi = np.array(_shahai())
    checks = [
        ("V1 ACS 煤系源岩 OSI 中位 < 20（实测 %.1f）" % np.median(osi), np.median(osi) < 20),
        ("V2 沙海组页岩 OSI 中位 %.1f > ACS 源岩 %.1f（源-储分离）" % (np.median(sh_osi), np.median(osi)),
         np.median(sh_osi) > 60 and np.median(osi) < 20),
        ("V3 J1b（八道湾组）全表可辨识 n>=3（实测 %d）" % sum(1 for r in ps if r["Formation"] == "J1b"),
         sum(1 for r in ps if r["Formation"] == "J1b") >= 3),
    ]
    print("ACS 锚点 n=%d  OSI 中位=%.1f 范围=[%.1f, %.1f]" % (len(osi), np.median(osi), osi.min(), osi.max()))
    print("沙海组（储层页岩）OSI 中位=%.1f（n=%d）" % (np.median(sh_osi), len(sh_osi)))
    n_pass = 0
    for name, ok in checks:
        print("[%s] %s" % ("PASS" if ok else "FAIL", name))
        n_pass += int(ok)
    print("结果：%d/%d 通过" % (n_pass, len(checks)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
