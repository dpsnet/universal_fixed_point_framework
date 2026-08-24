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
P1-1：EGDB 层段级三判据筛选——零阈值型第二例（Paper XLIII 适用域边界测试，2026-08-09）

目标：零阈值型（Z1Z2Z3 齐备：线性度 R²≥0.90 + 低端趋零 + c→0）当前仅长7段 1 例。
在 EGDB 46,599 样品全库中按地层体系 + 成熟度窄窗筛选，检验零阈值型是否可复现、
TOC\*≈0.42 是否体系普适。

方法（两级口径，对齐零阈值型适用域"成熟度均匀、无运移注入"）：
  A 全体系口径：Formation 体系（n>=40）直接三判据分类
  B 窄窗口径：体系内 Tmax 中位 ±10℃ 均匀窗（n>=20）——模拟长7段单井窄窗条件
  Z1 R²≥0.90（S1-TOC 线性度）；Z2 低/高 TOC 半区 S1 比<0.35；Z3 minS1<0.25

诚实边界：EGDB 为多实验室混合数据（跨实验室系统偏差已知）；Formation 字段为
USGS 原始地层名，含同组异名/合并层段；零阈值型判据对成熟度均匀与无注入
的适用域显式限定——宽窗体系即使满足判据亦须标注成熟度结构。
"""
import csv
import os
import re
from collections import defaultdict
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
EGDB_WIDE = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv")


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def _norm(fm):
    """Formation 规范化：大写 + 折叠空白 + 统一分隔符"""
    if not fm:
        return ""
    fm = fm.upper()
    fm = re.sub(r"\s+", " ", fm)
    fm = fm.replace("/", "_").replace("-", "_")
    return fm.strip()


def _r2(y, yp):
    return 1 - np.sum((y - yp) ** 2) / np.sum((y - y.mean()) ** 2)


def classify(toc, s1, tag=""):
    if len(toc) < 15:
        return None
    a, b = np.polyfit(toc, s1, 1)
    yp = a * toc + b
    r2 = _r2(s1, yp)
    med = np.median(toc)
    lo_ratio = np.median(s1[toc < med]) / np.median(s1[toc >= med])
    z1, z2, z3 = r2 >= 0.90, lo_ratio < 0.35, s1.min() < 0.25
    return {"n": len(toc), "a": a, "b": b, "r2": r2, "lo": lo_ratio,
            "min_s1": s1.min(), "osi": float(np.median(s1 / toc * 100)),
            "z1": z1, "z2": z2, "z3": z3,
            "type": "零阈值型" if (z1 and z2 and z3) else (
                "近零阈值(Z1Z2)" if (z1 and z2) else (
                "仅Z1" if z1 else ("仅Z2" if z2 else "非零阈值")))}


def main():
    # 1) 加载：Formation 分组（TOC/S1/TMAX 有效，0<toc<30, s1>=0, OSI<300）
    grp = defaultdict(lambda: {"toc": [], "s1": [], "tm": []})
    with open(EGDB_WIDE, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            fm = _norm(r["Formation"])
            if not fm:
                continue
            toc = _tof(r["TOC"])
            if not np.isfinite(toc):
                toc = _tof(r["TOC_Leco"])
            s1, tm = _tof(r["S1"]), _tof(r["TMAX"])
            if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0:
                osi = s1 / toc * 100.0
                if osi >= 300:
                    continue
                g = grp[fm]
                g["toc"].append(toc); g["s1"].append(s1); g["tm"].append(tm)
    print("EGDB Formation 体系数：%d（TOC+S1 有效，OSI<300）" % len(grp))

    # 2) 体系级三判据（两口径）
    rows_all, rows_win = [], []
    for fm, g in grp.items():
        toc = np.array(g["toc"]); s1 = np.array(g["s1"]); tm = np.array(g["tm"])
        if len(toc) < 40:
            continue
        c = classify(toc, s1)
        if c:
            tm_valid = tm[np.isfinite(tm)]
            tm_span = (tm_valid.max() - tm_valid.min()) if len(tm_valid) else np.nan
            tm_med = np.median(tm_valid) if len(tm_valid) else np.nan
            rows_all.append({"fm": fm, "tmax_med": tm_med, "tmax_span": tm_span, **c})
        # 窄窗口径：Tmax 中位 ±10℃（成熟度均匀子集）
        m = np.isfinite(tm) & (tm >= np.median(tm) - 10) & (tm <= np.median(tm) + 10)
        if m.sum() >= 20:
            cw = classify(toc[m], s1[m])
            if cw:
                tm_valid = tm[m]
                rows_win.append({"fm": fm, "tmax_med": float(np.median(tm_valid)),
                                 "tmax_span": float(tm_valid.max() - tm_valid.min()), **cw})

    # 3) 输出：全体系口径 top 零阈值型候选
    print("\n[A] 全体系口径（n>=40，%d 体系）——按零阈值完整度排序：" % len(rows_all))
    score = lambda r: (r["z1"], r["z2"], r["z3"], r["r2"])
    for r in sorted(rows_all, key=score, reverse=True)[:18]:
        print("  %-26s n=%-5d Tmax中位=%.0f(跨%.0f) S1=%+.3f·TOC%+.3f R2=%.3f "
              "低/高=%.2f minS1=%.3f OSI=%.1f  %s"
              % (r["fm"][:26], r["n"], r["tmax_med"], r["tmax_span"], r["a"], r["b"],
                 r["r2"], r["lo"], r["min_s1"], r["osi"],
                 "Z1Z2Z3=YYY ★零阈值" if r["type"] == "零阈值型" else r["type"]))

    # 4) 窄窗口径输出
    print("\n[B] 窄窗口径（Tmax 中位±10℃，n>=20，%d 体系）——零阈值型第二例候选：" % len(rows_win))
    hit = [r for r in rows_win if r["type"] == "零阈值型"]
    near = [r for r in rows_win if r["type"] == "近零阈值(Z1Z2)"]
    for r in sorted(rows_win, key=score, reverse=True)[:25]:
        mark = " ★★★零阈值第二例" if r["type"] == "零阈值型" else (
            " ★近零" if r["type"] == "近零阈值(Z1Z2)" else "")
        print("  %-26s n=%-4d Tmax中位=%.0f(跨%.0f) S1=%+.3f·TOC%+.3f R2=%.3f "
              "低/高=%.2f minS1=%.3f OSI=%.1f  %s%s"
              % (r["fm"][:26], r["n"], r["tmax_med"], r["tmax_span"], r["a"], r["b"],
                 r["r2"], r["lo"], r["min_s1"], r["osi"], r["type"], mark))

    print("\n结论：零阈值型第二例候选 %d 个；近零阈值(Z1Z2) %d 个（%d 体系窄窗）"
          % (len(hit), len(near), len(rows_win)))
    if hit:
        print("  → 候选：%s" % "、".join("%s(OSI %.1f, TOC* %.2f)" % (
            r["fm"], r["osi"], -r["b"] / r["a"]) for r in hit))
    else:
        print("  → 未发现零阈值型第二例（零阈值型仍仅长7段 1 例——诚实负结果："
              "零阈值型为特殊体系类，非普适）")


if __name__ == "__main__":
    main()
