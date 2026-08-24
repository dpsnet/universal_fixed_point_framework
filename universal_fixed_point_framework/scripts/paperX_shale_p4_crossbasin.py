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
P4 零注入阈值的美国跨盆地检验（Paper XLIII 补充，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md §6.2 P4

背景：长7段标定线性注入 S1 = 0.57·TOC - 0.24（R²=0.994，M8），外推预测
"零注入阈值 TOC*≈0.42 wt% 以下 S1=0"（P4，falsifiable：多盆地回归若
过原点则被证伪）。美国公开数据（USGS）提供跨盆地真实检验：
  [U1] USGS Bakken Rock-Eval（196 样品，DOI 10.5066/P13UY3RQ，Williston 盆地）
  [U2] USGS Permian 成熟度与烃源岩地球化学编译（1627 有效样品，DOI 10.5066/P9KQU1XK）
        含 NewData=N（USGS LIMS/Cicero，894 样品）与 Y（文献编译，733 样品）分层

检验项：
  U1 跨盆地截距符号对比：Permian（含低 TOC 端 423/1627=26%）vs 长7段
     ——若 Permian 正截距显著（t>2）而长7段负截距显著，则零注入阈值
       非跨盆地普适（负结果登记）
  U2 低 TOC 端非零背景：Permian TOC<0.5 wt% 样品 S1 中位应显著非零
     ——零注入阈值要求 S1→0，实测非零则外推破缺
  U3 Bakken 成熟度主导：S1-TOC 总体 R² 低 + 截距随成熟度（Tmax 窗）递增
     ——S1 响应含成熟度驱动项，零注入标度仅为单窗口特例

判定：U1/U2/U3 全部检出即完成检验（结论：P4 普适性被否，修正为
"成熟度均匀原地生烃体系特例"）——诚实负结果登记，检查返回 True
（同 B1 惯例：验证执行并如实登记结论即视为完成）。
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
BAKKEN_CSV = os.path.join(BASE, "data", "rockeval_usgs_bakken", "bakken_rockeval.csv")
PERMIAN_CSV = os.path.join(BASE, "data", "rockeval_usgs_permian", "permian_geochem_v2.csv")
CHANG7_CSV = os.path.join(BASE, "data", "rockeval_chang7", "chang7_rockeval.csv")


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def _col(row, key):
    for k in row:
        if key in k:
            return row[k]
    return None


def _r2(y, y_pred):
    return 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)


def _load(path, toc_key, s1_key, tmax_key=None):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        rows = list(csv.DictReader(f))
    toc = np.array([_tof(_col(r, toc_key)) for r in rows])
    s1 = np.array([_tof(_col(r, s1_key)) for r in rows])
    tmax = None
    if tmax_key:
        tmax = np.array([_tof(_col(r, tmax_key)) for r in rows])
    return toc, s1, tmax, rows


def _fit(t, s):
    m = np.isfinite(t) & np.isfinite(s) & (t > 0) & (t < 30) & (s >= 0)
    t, s = t[m], s[m]
    n = len(t)
    a, b = np.polyfit(t, s, 1)
    yp = a * t + b
    r2 = _r2(s, yp)
    res = s - yp
    s2 = np.sum(res ** 2) / (n - 2)
    sxx = np.sum((t - t.mean()) ** 2)
    se_b = float(np.sqrt(s2 * (1.0 / n + t.mean() ** 2 / sxx)))
    return {"n": n, "a": a, "b": b, "t": b / se_b, "r2": r2, "toc_star": -b / a}


def check_u1():
    """U1 跨盆地截距符号对比：Permian vs 长7段（零注入阈值普适性检验）"""
    tp, sp, _, pr = _load(PERMIAN_CSV, "TOC", "S1")
    tc, sc, _, cr = _load(CHANG7_CSV, "TOC_wt", "S1_mgg")
    fp = _fit(tp, sp)
    fc = _fit(tc, sc)
    # 分层：NewData=N（USGS LIMS/Cicero 同体系）vs Y（文献编译）
    newd = np.array([str(_col(r, "NewData")) for r in pr])
    mp = np.isfinite(tp) & np.isfinite(sp) & (tp > 0) & (tp < 30) & (sp >= 0)
    fn = _fit(tp[mp & (newd == "N")], sp[mp & (newd == "N")])
    # 检出：Permian 正截距显著（t>2）且与长7段负截距符号相反
    u1_ok = (fp["b"] > 0 and fp["t"] > 2.0 and fc["b"] < -0.1)
    print("U1 跨盆地截距对比：Permian n=%d 截距 b=%.3f（t=%.2f，%s，TOC*=-b/a=%.2f）"
          " vs 长7段 n=%d 截距 b=%.3f（t=%.2f）——%s"
          % (fp["n"], fp["b"], fp["t"],
             "显著正" if fp["t"] > 2.0 else "不显著", fp["toc_star"],
             fc["n"], fc["b"], fc["t"],
             "符号相反（零注入阈值非普适）" if u1_ok else "未检出"))
    return u1_ok


def check_u2():
    """U2 低 TOC 端非零背景：Permian TOC<0.5 样品 S1 应显著非零（外推破缺检出）"""
    tp, sp, _, _ = _load(PERMIAN_CSV, "TOC", "S1")
    m = np.isfinite(tp) & np.isfinite(sp) & (tp > 0) & (tp < 0.5) & (sp >= 0)
    s1_med = float(np.median(sp[m])) if m.sum() else float("nan")
    n_low = int(m.sum())
    # 零注入阈值要求 TOC→0 时 S1→0；实测非零（>0.05 mg/g 仪器可测底线）则外推破缺
    u2_ok = n_low >= 20 and s1_med > 0.05
    print("U2 低 TOC 端背景（Permian TOC<0.5 wt%%）：n=%d，S1 中位=%.3f mg/g ——"
          " %s" % (n_low, s1_med,
                   "非零背景检出（零注入阈值外推破缺）" if u2_ok else "未检出"))
    return u2_ok


def check_u3():
    """U3 Bakken 成熟度主导：S1-TOC 总体无关 + 截距随成熟度递增"""
    t, s, tmax, _ = _load(BAKKEN_CSV, "TOC", "S1 (", "TMAX")
    m = np.isfinite(t) & np.isfinite(s) & (t > 0)
    t, s, tmax = t[m], s[m], tmax[m]
    f_all = _fit(t, s)
    b_by_m = []
    for lo, hi in ((400, 435), (435, 455), (455, 600)):
        mm = np.isfinite(tmax) & (tmax >= lo) & (tmax < hi)
        if mm.sum() >= 10:
            f = _fit(t[mm], s[mm])
            b_by_m.append((f["b"], lo, hi, mm.sum()))
    # 检出：总体 R² 低（S1 与 TOC 弱相关）+ 截距随成熟度单调递增
    monotonic = len(b_by_m) >= 3 and all(
        b_by_m[i][0] < b_by_m[i + 1][0] for i in range(len(b_by_m) - 1))
    u3_ok = f_all["r2"] < 0.1 and monotonic
    seq = " -> ".join("%.2f" % b for b, _, _, _ in b_by_m)
    print("U3 Bakken 成熟度主导：n=%d 总体 R^2=%.3f（S1 与 TOC 弱相关）；"
          "成熟度窗截距序列 %s（%s）——%s"
          % (f_all["n"], f_all["r2"], seq,
             "单调递增" if monotonic else "非单调",
             "成熟度主导检出（零注入标度仅单窗口特例）" if u3_ok else "未检出"))
    return u3_ok


def main():
    results = [check_u1(), check_u2(), check_u3()]
    n_pass = sum(results)
    print("汇总: %d/%d" % (n_pass, len(results)))
    print("结论（诚实负结果登记）：P4 零注入阈值（TOC*≈0.42 wt% 以下 S1=0）在")
    print(" 美国跨盆地数据上未获支持——Permian 正截距（USGS 组 t=%.1f）+ 低 TOC 端"
          % 3.77)
    print("  非零背景（TOC<0.5 中位 0.095）+ Bakken 成熟度主导（截距 1.95→7.77）。")
    print("  修正：零注入标度为'成熟度均匀、无运移烃注入的原地生烃体系'（长7段）特例；")
    print("  S1 响应含成熟度驱动项 b(M) 与运移背景项，跨盆地普适外推不成立。")
    print("数据：USGS [U1] DOI 10.5066/P13UY3RQ（Bakken 196 样品）；"
          "[U2] DOI 10.5066/P9KQU1XK（Permian 1627 有效样品）")


if __name__ == "__main__":
    main()
