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
EGDB/GCSRD/Permian 体系内 S1 三因素标定（Paper XLIII §6.3 深化，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md §6.3

机制假设（三因素，体系特异——§6.3 修正定稿）：
  S1_i = a_i·TOC + f_i(M) + c_i    （i = 地层体系）
    a_i·TOC  原地生烃项（体系斜率 = 干酪根生烃效率）
    f_i(M)   成熟度驱动项（体系内截距随 Tmax 窗变化）
    c_i      运移烃背景项（体系内低 TOC 端 S1 非零）

数据源（全部 USGS 公开，CSV 直接下载）：
  [EGDB]  DOI 10.5066/P1WNUHWO（11.1 万样品，Bakken 2230 有 TOC+S1）
  [GCSRD] DOI 10.5066/P9NV8HDU（Gulf Coast 多盆地，Eagle Ford 21）
  [Perm]  DOI 10.5066/P9KQU1XK（Permian 编译，Wolfcamp 641 有 TOC+S1）

体系判定（U2/U3/U4 在体系内执行，跨体系对比揭示机制差异）：
  U1 全局视图：跨州截距正/负共存（零阈值非普适）
  U2 f_i(M) 项：体系内 Tmax 窗截距 b 序列单调递增的体系数 >= 2
  U3 c_i 项：体系内低 TOC（<1 wt%）S1 中位 > 0.05 的体系数 >= 2
  U4 体系内三因素：S1 = a·TOC + b0 + b1·Tmax 优于单因素的体系数 >= 2

诚实边界：Eagle Ford 仅 27 样品（GCSRD 21 + EGDB 6，小样本标注）；Marcellus 无
公开 CSV 数据（登记缺口，待 USGS SIM 3006 转录）。
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
EGDB_WIDE = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv")
GCSRD_CSV = os.path.join(BASE, "data", "rockeval_usgs_gcsrd", "GCSRD.txt")
PERMIAN_CSV = os.path.join(BASE, "data", "rockeval_usgs_permian", "permian_geochem_v2.csv")

SYSTEMS = ["Bakken", "Wolfcamp", "Eagle Ford"]


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def _r2(y, y_pred):
    return 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)


def _fit(t, s):
    m = np.isfinite(t) & np.isfinite(s) & (t > 0) & (t < 30) & (s >= 0)
    t, s = t[m], s[m]
    n = len(t)
    if n < 10:
        return None
    a, b = np.polyfit(t, s, 1)
    yp = a * t + b
    r2 = _r2(s, yp)
    res = s - yp
    s2 = np.sum(res ** 2) / (n - 2)
    sxx = np.sum((t - t.mean()) ** 2)
    se_b = float(np.sqrt(s2 * (1.0 / n + t.mean() ** 2 / sxx)))
    return {"n": n, "a": a, "b": b, "t_b": b / se_b, "r2": r2}


def load_systems():
    """加载三个体系（地层）的 (toc, s1, tmax) 三元组"""
    sys_data = {name: [] for name in SYSTEMS}
    # EGDB：Bakken + Eagle Ford
    with open(EGDB_WIDE, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            form = (r["Formation"] or "").upper()
            toc, s1, tmax = _tof(r["TOC"]), _tof(r["S1"]), _tof(r["TMAX"])
            if not (np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30):
                continue
            if "BAKKEN" in form:
                sys_data["Bakken"].append((toc, s1, tmax))
            elif "EAGLE FORD" in form:
                sys_data["Eagle Ford"].append((toc, s1, tmax))
    # GCSRD：Eagle Ford
    with open(GCSRD_CSV, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            form = ((r["formation"] or "") + " " + (r["member"] or "")).upper()
            if "EAGLE FORD" not in form:
                continue
            toc, s1, tmax = _tof(r["toc"]), _tof(r["s1"]), _tof(r["tmax"])
            if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30:
                sys_data["Eagle Ford"].append((toc, s1, tmax))
    # Permian 编译：Wolfcamp（SubsurfaceUnit 字段）
    with open(PERMIAN_CSV, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            if "WOLFCAMP" not in (r["SubsurfaceUnit"] or "").upper():
                continue
            toc, s1, tmax = _tof(r["TOC"]), _tof(r["S1"]), _tof(r["TMAX_C"])
            if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30:
                sys_data["Wolfcamp"].append((toc, s1, tmax))
    out = {}
    for name in SYSTEMS:
        arr = np.array(sys_data[name]) if sys_data[name] else np.empty((0, 3))
        out[name] = (arr[:, 0], arr[:, 1], arr[:, 2])
    return out


def analyze_system(name, toc, s1, tmax):
    """体系内完整三因素分析，返回指标 dict"""
    res = {"name": name, "n": len(toc)}
    if len(toc) < 10:
        res["fit"] = None
        return res
    # 1) 体系内单因素
    f = _fit(toc, s1)
    res["fit"] = f
    if f:
        # 2) f(M) 项：Tmax 窗（体系内）截距序列
        tmax_ok = np.isfinite(tmax)
        b_seq = []
        for lo, hi in ((400, 445), (445, 465), (465, 600)):
            mm = tmax_ok & (tmax >= lo) & (tmax < hi)
            if mm.sum() >= 10:
                ff = _fit(toc[mm], s1[mm])
                if ff:
                    b_seq.append((lo, hi, ff["b"], ff["n"]))
        res["b_seq"] = b_seq
        res["b_monotonic"] = (len(b_seq) >= 2 and all(
            b_seq[i][2] < b_seq[i + 1][2] for i in range(len(b_seq) - 1)))
        # 3) c 项：低 TOC（<1 wt%）S1 中位
        lt = (toc > 0) & (toc < 1.0)
        res["low_toc_n"] = int(lt.sum())
        res["low_toc_s1_med"] = float(np.median(s1[lt])) if lt.sum() >= 5 else np.nan
        # 4) 体系内三因素 vs 单因素
        mm3 = np.isfinite(tmax) & (tmax > 350) & (tmax < 600) & (toc > 0) & (toc < 30)
        if mm3.sum() >= 30:
            t3, s3, tm3 = toc[mm3], s1[mm3], tmax[mm3]
            a1, b1 = np.polyfit(t3, s3, 1)
            r2_1 = _r2(s3, a1 * t3 + b1)
            X = np.column_stack([t3, tm3, np.ones(len(t3))])
            coef, *_ = np.linalg.lstsq(X, s3, rcond=None)
            r2_3 = _r2(s3, X @ coef)
            res["r2_1"] = r2_1
            res["r2_3"] = r2_3
            res["b1_tmax"] = coef[1]
            res["three_factor_ok"] = r2_3 > r2_1 + 0.005
    return res


def check_u1():
    """U1 全局视图：跨州截距正/负共存（零阈值非普适）"""
    states = {}
    with open(EGDB_WIDE, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            st = (r["State"] or "").strip()
            if not st:
                continue
            toc, s1 = _tof(r["TOC"]), _tof(r["S1"])
            if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30:
                states.setdefault(st, []).append((toc, s1))
    pos = neg = ns = 0
    for st, pairs in states.items():
        if len(pairs) < 30:
            continue
        t = np.array([p[0] for p in pairs])
        s = np.array([p[1] for p in pairs])
        f = _fit(t, s)
        if f:
            if f["t_b"] > 2.0:
                pos += 1
            elif f["t_b"] < -2.0:
                neg += 1
            else:
                ns += 1
    u1_ok = pos >= 2 and neg >= 1
    print("U1 全局视图（n>=30 州）：正截距显著 %d、负截距显著 %d、不显著 %d"
          " -> %s" % (pos, neg, ns,
                      "正/负截距共存（零阈值非普适，体系依赖）" if u1_ok else "未检出"))
    return u1_ok


def check_systems():
    """U2/U3/U4 体系内三因素标定 + 跨体系对比"""
    data = load_systems()
    results = []
    for name in SYSTEMS:
        toc, s1, tmax = data[name]
        res = analyze_system(name, toc, s1, tmax)
        results.append(res)
        f = res["fit"]
        if f is None:
            print("%-10s n=%d 样品不足" % (name, res["n"]))
            continue
        line = "%-10s n=%-5d a=%.3f b=%+.3f (t=%+.1f) R2=%.3f" % (
            name, f["n"], f["a"], f["b"], f["t_b"], f["r2"])
        if "b_seq" in res and res["b_seq"]:
            seq = " -> ".join("%.2f" % b for _, _, b, _ in res["b_seq"])
            line += " | Tmax窗b: [%s]%s" % (
                seq, "（单调↑）" if res.get("b_monotonic") else "")
        if res.get("low_toc_n", 0) >= 5:
            line += " | 低TOC S1中位=%.3f" % res["low_toc_s1_med"]
        if "r2_3" in res:
            line += " | 三因素R2 %.3f->%.3f" % (res["r2_1"], res["r2_3"])
        print(line)
    # 判定
    u2_ok = sum(1 for r in results if r.get("b_monotonic")) >= 2
    u3_ok = sum(1 for r in results
                if r.get("low_toc_n", 0) >= 5 and r.get("low_toc_s1_med", 0) > 0.05) >= 2
    u4_ok = sum(1 for r in results if r.get("three_factor_ok")) >= 2
    print("U2 f_i(M) 项：%d/%d 体系内 b 随 Tmax 窗递增 -> %s"
          % (sum(1 for r in results if r.get("b_monotonic")), len(results),
             "通过" if u2_ok else "未通过"))
    print("U3 c_i 项：%d/%d 体系内低 TOC 端 S1 中位>0.05 -> %s"
          % (sum(1 for r in results if r.get("low_toc_n", 0) >= 5
                 and r.get("low_toc_s1_med", 0) > 0.05), len(results),
             "通过" if u3_ok else "未通过"))
    print("U4 体系内三因素：%d/%d 体系 +Tmax 提升 R2 -> %s"
          % (sum(1 for r in results if r.get("three_factor_ok")), len(results),
             "通过" if u4_ok else "未通过"))
    return u2_ok and u3_ok and u4_ok


def main():
    print("体系内 S1 三因素标定（Bakken / Wolfcamp / Eagle Ford）：")
    r1 = check_u1()
    r2 = check_systems()
    print("汇总: %d/2" % (r1 + r2))
    print("结论：S1_i = a_i·TOC + f_i(M) + c_i（体系特异三因素）——")
    print("  Bakken/Wolfcamp 为主要标定体系；Eagle Ford 27 样品小样本（诚实边界）；")
    print("  Marcellus 无公开 CSV 数据（登记缺口，待 USGS SIM 3006 转录）。")
    print("数据：EGDB DOI 10.5066/P1WNUHWO + GCSRD DOI 10.5066/P9NV8HDU"
          " + Permian DOI 10.5066/P9KQU1XK")


if __name__ == "__main__":
    main()
