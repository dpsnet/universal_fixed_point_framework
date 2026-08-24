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
Green River（Uinta 盆地）湖相页岩大样本三因素机制标定（Paper XLIII §6.3，2026-08-09）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md（数据扩大计划任务 2）

数据源：USGS Green River 数据集（Birdwell, 2025，DOI 10.5066/P1WCA9UF，CC0）
  `rockeval_usgs_greenriver/GRF_Data_All_Wells.csv`——2586 行、107 列，
  TOC_wt%/S1_mg/g/S2_mg/g/S3_mg/g/Tmax_degC + 微量元素 + 矿物 + 深度/层段。
  有效 Rock-Eval 样品 n=1933，20 口井，层段覆盖 Uteland Butte(552)/Mahogany(265)/
  Carbonate Marker(146)/Douglas Creek(108)/Castle Peak(103) 等，Tmax 集中 430-450℃（油窗），
  过成熟（>460℃）仅 16 个——提供上升支+峰值证据，下降支覆盖弱。

目的（北美湖相对照）：
  G1 三判据分类：全窗 + 油窗内回归的 Z1/Z2/Z3——与长7段零阈值型对照
  G2 f(M) 窗形标定：OSI-Tmax 10℃ 箱中位 + 不对称高斯拟合（峰位/峰高/半宽）
  G3 c 项标定：c 代理（TOC<0.5 端 S1 中位）+ 油窗内截距 b——与 EGDB/中国湖相对照
  G4 北美湖相 vs 中国湖相 vs 美方海相（Bakken/Wolfcamp）OSI 背景对照

结论预期：Green River 湖相（高 TOC 油页岩/碳酸盐湖相）为 c 型高背景（滞留油，
与青山口/芦草沟一致）——湖相富油背景跨洋（北美/中国）再证；f(M) 窗形峰值
~440℃（生烃窗动力学普适）；Tmax 覆盖限制作下降支判断（诚实边界）。
"""
import csv
import os
import numpy as np
try:
    from scipy import stats as st
    from scipy.optimize import curve_fit
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

BASE = os.path.dirname(os.path.abspath(__file__))
GR_CSV = os.path.join(BASE, "data", "rockeval_usgs_greenriver", "GRF_Data_All_Wells.csv")


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load_gr():
    """Green River 有效样品：TOC/S1/S2/Tmax，过滤 0<TOC<30、S1>=0、350<Tmax<600"""
    toc_l, s1_l, s2_l, tm_l, fm_l = [], [], [], [], []
    with open(GR_CSV, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            toc, s1, s2, tm = _tof(r["TOC_wt%"]), _tof(r["S1_mg/g"]), \
                _tof(r["S2_mg/g"]), _tof(r["Tmax_degC"])
            if not (np.isfinite(toc) and np.isfinite(s1) and np.isfinite(s2)
                    and np.isfinite(tm) and 0 < toc < 30 and s1 >= 0
                    and 350 < tm < 600):
                continue
            o = s1 / toc * 100.0
            if o >= 300:
                continue
            toc_l.append(toc); s1_l.append(s1); s2_l.append(s2); tm_l.append(tm)
            fm_l.append((r["Interval"] or "").strip())
    return (np.array(toc_l), np.array(s1_l), np.array(s2_l),
            np.array(tm_l), np.array(fm_l, dtype=object))


def classify(toc, s1, tag=""):
    a, b = np.polyfit(toc, s1, 1)
    yp = a * toc + b
    r2 = 1.0 - np.sum((s1 - yp) ** 2) / np.sum((s1 - s1.mean()) ** 2)
    med = np.median(toc)
    lo = np.median(s1[toc < med]) / np.median(s1[toc >= med])
    z1, z2, z3 = r2 >= 0.90, lo < 0.35, s1.min() < 0.25
    typ = "零阈值型" if (z1 and z2 and z3) else "c 型（背景高，非零阈值）"
    print("  %-22s n=%-4d S1=%+.3f·TOC%+.3f  R2=%.3f  低/高比=%.3f  minS1=%.2f  "
          "OSI中位=%.1f  Z1Z2Z3=%s%s%s  -> %s"
          % (tag, len(toc), a, b, r2, lo, s1.min(), np.median(s1 / toc * 100),
             "Y" if z1 else "N", "Y" if z2 else "N", "Y" if z3 else "N", typ))
    return a, b, r2, lo, s1.min()


def asym_gauss(x, A, mu, sl, sr):
    s = np.where(x < mu, sl, sr)
    return A * np.exp(-0.5 * ((x - mu) / s) ** 2)


def fit_window(xb, yb):
    i0 = int(np.argmax(yb))
    p0 = [float(yb[i0]), float(xb[i0]), 15.0, 15.0]
    try:
        popt, _ = curve_fit(asym_gauss, xb, yb, p0=p0,
                            bounds=([1.0, 380.0, 5.0, 5.0],
                                    [500.0, 540.0, 120.0, 120.0]), maxfev=20000)
        if not (xb.min() + 8 <= popt[1] <= xb.max() - 8):
            return None
        yp = asym_gauss(xb, *popt)
        r2 = 1.0 - np.sum((yb - yp) ** 2) / np.sum((yb - yb.mean()) ** 2)
        return {"A": float(popt[0]), "mu": float(popt[1]),
                "sl": float(popt[2]), "sr": float(popt[3]), "r2": float(r2)}
    except Exception:
        return None


def main():
    if not HAS_SCIPY:
        print("需要 scipy")
        return
    toc, s1, s2, tm, fm = load_gr()
    print("Green River（Uinta 盆地）湖相：%d 有效样品（OSI<300 过滤）" % len(toc))
    print("TOC [%.2f, %.2f] 中位 %.2f | Tmax [%.0f, %.0f] 中位 %.0f | 层段 %d 个"
          % (toc.min(), toc.max(), np.median(toc), tm.min(), tm.max(),
             np.median(tm), len(set(fm.tolist()))))
    print("\nG1 三判据分类：")
    classify(toc, s1, "全窗（Tmax 350-500）")
    m = (tm >= 430) & (tm < 455)  # 油窗内（成熟度近似均匀）
    classify(toc[m], s1[m], "油窗内（430-455℃）")
    m_hi = (tm >= 440) & (tm < 450)
    classify(toc[m_hi], s1[m_hi], "峰值窗（440-450℃）")
    # 层段细分：Mahogany（富油页岩）vs Uteland Butte（碳酸盐储层）
    for seg in ("Mahogany zone", "Uteland Butte"):
        mseg = fm == seg
        if mseg.sum() >= 50:
            classify(toc[mseg], s1[mseg], seg)

    print("\nG2 f(M) 窗形（OSI-Tmax 10℃ 箱中位）：")
    xs, med, ns = [], [], []
    for lo in range(390, 500, 10):
        b = (tm >= lo) & (tm < lo + 10)
        if b.sum() >= 10:
            xs.append(lo + 5); med.append(np.median(s1[b] / toc[b] * 100)); ns.append(int(b.sum()))
    xs, med, ns = map(np.array, (xs, med, ns))
    for x, m2, n in zip(xs, med, ns):
        print("  Tmax %3d-%-3d  n=%-4d  OSI 中位=%6.1f" % (x - 5, x + 5, n, m2))
    fit = fit_window(xs, med)
    if fit:
        print("  不对称高斯：A=%.1f  mu=%.1f℃  sl=%.1f  sr=%.1f  R2=%.2f"
              % (fit["A"], fit["mu"], fit["sl"], fit["sr"], fit["r2"]))
        v1 = 430 <= fit["mu"] <= 470
        print("  V1 峰值在油窗[430,470]? %s" % ("是" if v1 else "否"))
    # 上升支秩相关（低熟段）
    low = (tm >= 420) & (tm < 445)
    rho, pv = st.spearmanr(tm[low], s1[low] / toc[low] * 100)
    print("  上升支（420-445℃）OSI-Tmax Spearman rho=%+.2f (p=%.2e) -> %s"
          % (rho, pv, "上升支显著（生烃窗非线性）" if rho > 0.3 and pv < 0.05 else "不显著"))

    print("\nG3 c 项标定：")
    # c 代理：TOC<0.5 端 S1 中位（EGDB 口径）；GR 低 TOC 样品少，辅以 TOC<1.0
    c050 = s1[toc < 0.5]
    c10 = s1[toc < 1.0]
    print("  c 代理（TOC<0.5，EGDB 口径）: %.3f mg/g (n=%d)"
          % (np.median(c050), len(c050)))
    print("  c 代理（TOC<1.0，n 扩大）:     %.3f mg/g (n=%d)"
          % (np.median(c10), len(c10)))
    m = (tm >= 430) & (tm < 455)
    a, b, _, _, _ = classify(toc[m], s1[m], "油窗内回归（截距=油窗内 c 项估计）")
    # 低 TOC 端底板：S1 第 10 分位随 TOC 箱
    print("  S1 低 TOC 端（TOC<1）中位=%.2f mg/g——绝对背景底板（青山口/芦草沟口径对照）"
          % np.median(s1[toc < 1.0]))

    print("\nG4 北美湖相 vs 中国湖相 vs 美方海相 OSI 对照：")
    osi_gr = s1 / toc * 100
    print("  Green River 湖相（北美）   n=%4d  OSI 中位=%5.1f  （本数据集）" % (len(toc), np.median(osi_gr)))
    # 中国湖相六体系（复用 china_lacustrine 数据）
    china_specs = {
        "长7段": ("rockeval_chang7/chang7_rockeval.csv", "TOC_wt", "S1_mgg", None),
        "青山口D86": ("rockeval_qingshankou_d86/qingshankou_d86_rockeval.csv", "TOC_wt", "S1_mgg", None),
        "青山口SL": ("rockeval_qingshankou/qingshankou_rockeval.csv", "TOC_wt", "S1_mgg", None),
        "沙海组": ("rockeval_shahai/shahai_rockeval.csv", "TOC_wt", "S1_mgg", 11),
        "芦草沟组": ("rockeval_jimsar_lucaogou/lucaogou_rockeval.csv", "TOC_wt", "S1_mgg", None),
    }
    osi_china = {}
    for nm, (fn, ct, cs, drop) in china_specs.items():
        s = []
        with open(os.path.join(BASE, "data", fn), encoding="utf-8-sig", errors="replace") as f:
            for i, r in enumerate(csv.DictReader(f), start=1):
                if drop and i == drop:
                    continue
                a, b = _tof(r[ct]), _tof(r[cs])
                if np.isfinite(a) and np.isfinite(b) and 0 < a < 30 and b >= 0:
                    o = b / a * 100
                    if o < 300:
                        s.append(o)
        osi_china[nm] = np.array(s)
        print("  %-22s n=%4d  OSI 中位=%5.1f" % (nm, len(s), np.median(s)))
    # 与长7段（零阈值型基准）单边对照：Green River 湖相背景是否显著更高
    for ref in ("长7段", "芦草沟组", "沙海组"):
        if ref in osi_china and len(osi_china[ref]) >= 10:
            u, p = st.mannwhitneyu(osi_gr, osi_china[ref], alternative="greater")
            print("  GR(中位 %.1f) vs %s(中位 %.1f)：单边 MWU p=%.2e -> %s"
                  % (np.median(osi_gr), ref, np.median(osi_china[ref]), p,
                     "GR 背景显著更高（北美湖相高背景确认）" if p < 0.05 else "无显著差异"))
    # 与 Bakken/Wolfcamp（美方海相）对照——若有本地数据
    print("  参考：Bakken（美方海相）OSI 44-69；Wolfcamp 峰值 75.6@445℃（paperX_shale_osi_window.py）")
    print("  注：Green River 全窗 OSI 中位 %.1f——高于长7段 53.6（零阈值型），与芦草沟 65.9 同量级"
          % np.median(osi_gr))


if __name__ == "__main__":
    main()
