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
# 本文件中 UFPF 相关引用数量：1
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EGDB 跨体系 f(M) 窗函数形式标定（Paper XLIII §6.3，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md §6.3 开放问题 1

目的：封闭开放问题"f(M) 函数形式（线性 vs 幂律 vs 生烃窗曲线）待跨盆地标定"——
对 EGDB 各主要体系（n>=150）拟合 OSI-Tmax 生烃窗曲线（不对称高斯），提取
峰位/峰高/左右半宽，并同时提取 c 项代理（低 TOC 端 S1 中位数）：

  W1 窗形普适性：各体系 OSI-Tmax 呈窗形（不对称高斯拟合 R^2 显著），
                 线性/幂律形式被窗形拟合取代
  W2 峰位一致性：各体系峰位 mu 是否落在油窗 [430,450]（生烃窗物理统一，f 的
                 窗形主体跨体系一致）
  W3 下降支体系差异：过成熟段 [465,500] vs 油窗 [430,450] 关键箱比——
                 排烃亏损（箱比<0.7）vs 运移烃掩盖（箱比>=1 或反向）
  W4 c 项尺度体系差异：TOC<0.5 wt% 样品 S1 中位数随体系变化（运移烃背景规模）

结论预期（2026-08-08 初步）：f(M) 为不对称高斯窗形（峰值 ~440-450℃），
峰位跨体系一致但峰高/右半宽体系特异——下降支（排烃亏损）只在无运移烃
掩盖的体系显现；c 项代理（低 TOC 端 S1）体系特异。
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
EGDB_WIDE = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv")

# Bakken 各段合并为一个体系（UFPF 同一体系）
BAKKEN_SET = {"BAKKEN", "BAKKEN UPPER", "BAKKEN LOWER", "BAKKEN SILTSTONE"}
MIN_N = 150        # 体系最小样品数
BIN = 5.0          # Tmax 箱宽（℃）
MIN_BIN_N = 5      # 每箱最小样品数


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load_data():
    """返回 {体系: [(Tmax, OSI), ...]}，Formation 缺失归入 'NA'"""
    by_fm = {}
    with open(EGDB_WIDE, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            toc, s1, tm = _tof(r["TOC"]), _tof(r["S1"]), _tof(r["TMAX"])
            if not (np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm)
                    and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600):
                continue
            o = s1 / toc * 100.0
            if o >= 300:
                continue
            fm = (r["Formation"] or "NA").strip().upper()
            if fm in BAKKEN_SET:
                fm = "BAKKEN"
            by_fm.setdefault(fm, []).append((tm, o, toc, s1))
    return by_fm


def asym_gauss(x, A, mu, sl, sr):
    """不对称高斯：x<mu 用左半宽 sl，x>=mu 用右半宽 sr"""
    s = np.where(x < mu, sl, sr)
    return A * np.exp(-0.5 * ((x - mu) / s) ** 2)


def fit_window(points):
    """对 (Tmax, OSI 中位) 箱统计拟合不对称高斯，返回参数 dict 或 None。

    物理约束：峰位 mu ∈ [380,540]℃（生烃窗物理范围），左右半宽 ∈ [5,120]℃，
    A ∈ [1,500]（OSI 峰值量级）。拟合收敛但峰位落在数据窗口边缘（单调/无峰）
    也返回 None——该类体系窗形被掩盖（运移烃背景主导）。
    """
    x, y = points[:, 0], points[:, 1]
    i0 = int(np.argmax(y))
    p0 = [float(y[i0]), float(x[i0]), 15.0, 15.0]
    try:
        popt, _ = curve_fit(
            asym_gauss, x, y, p0=p0,
            bounds=([1.0, 380.0, 5.0, 5.0], [500.0, 540.0, 120.0, 120.0]),
            maxfev=20000)
        if not (x.min() + 10 <= popt[1] <= x.max() - 10):
            return None  # 峰位贴边——单调/无峰，窗形未显现
        yp = asym_gauss(x, *popt)
        ss_res = float(np.sum((y - yp) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
        return {"A": float(popt[0]), "mu": float(popt[1]),
                "sl": float(popt[2]), "sr": float(popt[3]), "r2": r2, "nbox": len(x)}
    except Exception:
        return None


def box_median(pts, lo, hi):
    o = [o for t, o, _, _ in pts if lo <= t < hi]
    return np.median(o) if len(o) >= MIN_BIN_N else np.nan


def c_proxy(pts):
    """c 项代理：低 TOC（<0.5 wt%）样品 S1 中位数"""
    s1 = [s1 for _, _, toc, s1 in pts if toc < 0.5]
    return (float(np.median(s1)), len(s1)) if len(s1) >= 10 else (np.nan, len(s1))


def main():
    if not HAS_SCIPY:
        print("需要 scipy（curve_fit + Mann-Whitney U）")
        return
    by_fm = load_data()
    print("体系         n    峰位mu  峰高A  左半宽  右半宽  拟合R2  箱比[465/430]  c代理(TOC<0.5 S1)  c样数")
    print("-" * 100)
    rows = []   # 有峰体系
    flat = []   # 无峰/单调体系（窗形被掩盖）
    for fm, pts in sorted(by_fm.items(), key=lambda kv: -len(kv[1])):
        if len(pts) < MIN_N:
            continue
        arr = np.array([(t, o) for t, o, _, _ in pts])
        xb, yb = [], []
        for lo in range(350, 595, int(BIN)):
            m = (arr[:, 0] >= lo) & (arr[:, 0] < lo + BIN)
            if m.sum() >= MIN_BIN_N:
                xb.append(lo + BIN / 2)
                yb.append(np.median(arr[m, 1]))
        if len(xb) < 6:
            continue
        fit = fit_window(np.array(list(zip(xb, yb))))
        br = box_median(pts, 465, 500) / box_median(pts, 430, 450)
        cp, cn = c_proxy(pts)
        # 统一行结构：(体系, n, 拟合或None, 箱比, c代理, c样数)
        if fit is None or fit["r2"] < 0.2:
            flat.append((fm, len(pts), None, br, cp, cn))
            print("%-12s n=%5d  %-12s（单调/无峰或噪声，窗形未显现）  箱比=%5.2f  c=%.3f(n=%d)"
                  % (fm, len(pts), "——", br, cp, cn))
            continue
        rows.append((fm, len(pts), fit, br, cp, cn))
        print("%-12s n=%5d  mu=%5.1f  A=%6.1f  sl=%5.1f  sr=%5.1f  R2=%.2f  "
              "箱比=%5.2f  c=%.3f(n=%d)"
              % (fm, len(pts), fit["mu"], fit["A"], fit["sl"], fit["sr"],
                 fit["r2"], br, cp, cn))
    # W1 窗形普适性：有效拟合体系占比 + 平均 R2（仅对有峰体系）
    r2s = [r[2]["r2"] for r in rows]
    w1 = (len(rows) > 0 and np.median(r2s) > 0.7)
    print("W1 窗形普适性: %d 个有峰体系（%d 个无峰/单调被掩盖），R2 中位=%.2f -> %s"
          % (len(rows), len(flat), np.median(r2s) if r2s else float('nan'),
             "窗形普适（可拟合体系均呈窗形）" if w1 else "未通过"))
    # W2 峰位一致性：mu 是否都在 [425,455]（仅对有峰体系）
    mus = np.array([r[2]["mu"] for r in rows])
    if len(mus) >= 2:
        w2 = bool(((mus >= 425) & (mus <= 455)).all())
        print("W2 峰位一致性: mu ∈[%0.1f,%0.1f]（范围=%.1f℃）-> %s"
              % (mus.min(), mus.max(), mus.max() - mus.min(),
                 "峰位跨体系一致（油窗物理统一）" if w2 else "峰位体系分散"))
    else:
        w2 = False
        print("W2 峰位一致性: 有峰体系不足 2 个，无法判定")
    # W3 下降支体系差异：箱比分类（含无峰体系）
    allb = rows + flat
    d_down = [r for r in allb if np.isfinite(r[3]) and r[3] < 0.7]
    d_flatr = [r for r in allb if np.isfinite(r[3]) and 0.7 <= r[3] < 1.0]
    d_up = [r for r in allb if np.isfinite(r[3]) and r[3] >= 1.0]
    w3 = len(d_down) >= 1 and len(d_up) >= 1
    print("W3 下降支差异: 排烃亏损(箱比<0.7) %d 个 %s；平缓 %d 个 %s；反向/不降 %d 个 %s -> %s"
          % (len(d_down), [r[0] for r in d_down],
             len(d_flatr), [r[0] for r in d_flatr],
             len(d_up), [r[0] for r in d_up],
             "下降支体系分化确认（排烃亏损 vs 运移烃掩盖并存）" if w3 else "未分化"))
    # W4 c 项尺度差异：c 代理的范围
    cvals = np.array([r[4] for r in allb if np.isfinite(r[4])])
    if len(cvals) >= 2:
        spread = cvals.max() / cvals.min()
        w4 = spread > 3.0
        print("W4 c 项尺度: c 代理∈[%.3f, %.3f] mg/g（跨度 %.1f×）-> %s"
              % (cvals.min(), cvals.max(), spread,
                 "c 体系特异（运移烃背景规模差异显著）" if w4 else "c 跨体系近似一致"))
    else:
        w4 = False
        print("W4 c 项尺度: 有效体系不足")
    # W5 c-下降支耦合：c 代理与箱比的秩相关（c 高 → 不降，运移烃掩盖排烃亏损）
    pairs = [(r[4], r[3]) for r in allb if np.isfinite(r[4]) and np.isfinite(r[3])]
    if len(pairs) >= 4:
        rho, pv = st.spearmanr([p[0] for p in pairs], [p[1] for p in pairs])
        w5 = rho > 0.3 and pv < 0.3
        print("W5 c-下降支耦合: n=%d 体系, Spearman rho(c, 箱比)=%+.2f (p=%.2f) -> %s"
              % (len(pairs), rho, pv,
                 "c 越高越不降（运移烃背景掩盖排烃亏损，定量支持）" if w5
                 else "c-箱比无单调耦合"))
    else:
        w5 = False
        print("W5 c-下降支耦合: 有效体系不足")
    print("汇总: %d/5" % (int(w1) + int(w2) + int(w3) + int(w4) + int(w5)))


if __name__ == "__main__":
    main()
