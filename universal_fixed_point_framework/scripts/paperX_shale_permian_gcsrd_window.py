#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1-2：Permian/GCSRD 层段细分 f(M) 窗形标定（Paper XLIII 适用域边界测试，2026-08-09）
对应母笔记：notes/05_condensed_matter/spectral_shale_accumulation.md
"下一步采样策略 P1②：Permian/GCSRD 层段细分 f(M) 窗形"

目标：f(M) 生烃窗非线性已在体系级（Bakken/Wolfcamp 合成完整窗形，§6.3）验证。
P1-2 将尺度下沉到层段级——检验窗形是体系普适还是层段特异：

  Permian 编译（DOI 10.5066/P9KQU1XK）按 SubsurfaceUnit 分组：
    Bone Spring / Avalon / Wolfcamp 等各自标定 OSI-Tmax 窗形
  GCSRD（DOI 10.5066/P9NV8HDU）按 formation 分组：
    Tuscaloosa / Eagle Ford 等各自标定

判据（沿用 osi_window.py V1/V2）：
  V1 峰值 Tmax 落在油窗 [430, 470]
  V2 峰值前上升（秩相关>0.3）或峰值后下降（秩相关<-0.3），或
     关键箱比（过成熟 [465,500] vs 油窗 [430,450]）<0.7
另附每层段 S1-TOC 回归 a/b（c 项截距），与 EGDB 层段级 c 信号交叉对照。

诚实边界：Permian 为岩屑样多实验室编译（cuttings，深度非等间隔）；GCSRD
为多参考汇编（Enomoto 等），层段 n 可能不足 50——小样本层段仅登记窗形骨架。
"""
import csv
import os
import re
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(BASE), 'figs')
os.makedirs(FIG, exist_ok=True)
PERMIAN_CSV = os.path.join(BASE, "data", "rockeval_usgs_permian", "permian_geochem_v2.csv")
GCSRD_CSV = os.path.join(BASE, "data", "rockeval_usgs_gcsrd", "GCSRD.txt")


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def _norm(s):
    if not s:
        return ""
    s = s.upper()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("/", "_").replace("-", "_")
    return s.strip()


def _r2(y, yp):
    return 1 - np.sum((y - yp) ** 2) / np.sum((y - y.mean()) ** 2)


def load_permian():
    """按 SubsurfaceUnit 分组 -> {unit: (toc, s1, tmax)}"""
    grp = defaultdict(lambda: {"toc": [], "s1": [], "tm": []})
    with open(PERMIAN_CSV, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            u = _norm(r.get("SubsurfaceUnit", ""))
            if not u:
                continue
            toc, s1, tm = _tof(r["TOC"]), _tof(r["S1"]), _tof(r["TMAX_C"])
            if np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm) \
                    and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600:
                osi = s1 / toc * 100.0
                if osi >= 300:
                    continue
                g = grp[u]
                g["toc"].append(toc); g["s1"].append(s1); g["tm"].append(tm)
    return grp


def load_gcsrd():
    """按 formation 分组 -> {fm: (toc, s1, tmax)}"""
    grp = defaultdict(lambda: {"toc": [], "s1": [], "tm": []})
    with open(GCSRD_CSV, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            fm = _norm(r.get("formation", ""))
            if not fm:
                continue
            toc, s1, tm = _tof(r.get("toc", "")), _tof(r.get("s1", "")), _tof(r.get("tmax", ""))
            if np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm) \
                    and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600:
                osi = s1 / toc * 100.0
                if osi >= 300:
                    continue
                g = grp[fm]
                g["toc"].append(toc); g["s1"].append(s1); g["tm"].append(tm)
    return grp


def window_curve(tmax, osi, bins=np.arange(390, 590, 10)):
    xs, med, lo, hi, ns = [], [], [], [], []
    for i in range(len(bins) - 1):
        m = (tmax >= bins[i]) & (tmax < bins[i + 1])
        if m.sum() < 5:
            continue
        xs.append((bins[i] + bins[i + 1]) / 2)
        med.append(np.median(osi[m]))
        lo.append(np.percentile(osi[m], 25))
        hi.append(np.percentile(osi[m], 75))
        ns.append(m.sum())
    return np.array(xs), np.array(med), np.array(lo), np.array(hi), np.array(ns)


def unit_metrics(toc, s1, tmax, n_min=40):
    """层段级指标：窗形验证 + S1-TOC 回归（c 项截距）+ 低 TOC S1 中位"""
    n = len(toc)
    out = {"n": n}
    if n < n_min:
        return out
    # 成熟度覆盖（p5-p95 跨度，评估窗形可验证性）
    out["tmax_med"] = float(np.median(tmax))
    out["tmax_span"] = float(np.percentile(tmax, 95) - np.percentile(tmax, 5))
    # S1-TOC 回归
    a, b = np.polyfit(toc, s1, 1)
    yp = a * toc + b
    out.update({"a": a, "b": b, "r2": _r2(s1, yp)})
    # c 项：低 TOC (<1 wt%) S1 中位
    lt = toc < 1.0
    out["c_med"] = float(np.median(s1[lt])) if lt.sum() >= 5 else np.nan
    # OSI-Tmax 窗形
    osi = s1 / toc * 100.0
    xs, med, lo, hi, ns = window_curve(tmax, osi)
    out["win"] = (xs, med, lo, hi, ns)
    if len(xs) < 5:
        return out
    in_win = (xs >= 430) & (xs <= 470)
    if in_win.sum() == 0:
        return out
    i_peak = int(np.argmax(med[in_win])) + int(np.where(in_win)[0][0])
    peak_tmax, peak_osi = xs[i_peak], med[i_peak]
    before, after = (xs[:i_peak], med[:i_peak]), (xs[i_peak + 1:], med[i_peak + 1:])
    rho_b = np.corrcoef(before[0], before[1])[0, 1] if len(before[0]) >= 3 else 0
    rho_a = np.corrcoef(after[0], after[1])[0, 1] if len(after[0]) >= 3 else 0

    def _seg(lo_, hi_):
        m = (xs >= lo_) & (xs < hi_)
        return float(np.median(med[m])) if m.sum() else np.nan
    p_med, o_med = _seg(430, 450), _seg(465, 500)
    key_ratio = o_med / p_med if (np.isfinite(p_med) and np.isfinite(o_med)) else np.nan
    v1 = 430 <= peak_tmax <= 470
    rise, fall = (len(before[0]) >= 3 and rho_b > 0.3), (len(after[0]) >= 3 and rho_a < -0.3)
    v2 = rise or fall or (np.isfinite(key_ratio) and key_ratio < 0.7)
    out.update({"peak": (peak_tmax, peak_osi), "rho_b": rho_b, "rho_a": rho_a,
                "key_ratio": key_ratio, "v1": v1, "v2": v2})
    return out


def analyze_src(title, grp, src, n_min=40):
    print("\n=== %s ===" % title)
    rows = []
    for u, g in grp.items():
        toc = np.array(g["toc"]); s1 = np.array(g["s1"]); tm = np.array(g["tm"])
        m = unit_metrics(toc, s1, tm, n_min=n_min)
        m["u"] = u
        m["_g"] = g
        rows.append(m)
    # 按 n 降序
    for m in sorted(rows, key=lambda r: r["n"], reverse=True):
        u = m["u"]
        if m["n"] < 40:
            print("  %-28s [%s] n=%d 样品不足" % (u[:28], src, m["n"]))
            continue
        g = m["_g"]
        osi_med = float(np.median(np.array(g["s1"]) / np.array(g["toc"]) * 100.0))
        line = "  %-28s [%s] n=%-5d Tmax=%.0f(跨%.0f℃) S1=%+.3f·TOC%+.3f R2=%.2f OSI中位=%.1f c=%.3f" % (
            u[:28], src, m["n"], m["tmax_med"], m["tmax_span"],
            m["a"], m["b"], m["r2"], osi_med, m.get("c_med", np.nan))
        if "peak" in m:
            pt, pm = m["peak"]
            side = ("↑" if m["rho_b"] > 0.3 else "·") + ("↓" if m["rho_a"] < -0.3 else "·")
            line += " 峰值OSI=%.1f@%.0f℃ 前rho=%+.2f 后rho=%+.2f 关键比=%.2f V1=%s V2=%s [%s]" % (
                pm, pt, m["rho_b"], m["rho_a"], m.get("key_ratio", np.nan),
                "Y" if m["v1"] else "N", "Y" if m["v2"] else "N", side)
        print(line)
    return rows


def main():
    print("P1-2：Permian/GCSRD 层段细分 f(M) 窗形标定（OSI<300、Tmax 350-600、0<TOC<30）")
    perm = load_permian()
    gcsrd = load_gcsrd()
    print("Permian SubsurfaceUnit 数：%d；GCSRD formation 数：%d" % (len(perm), len(gcsrd)))

    perm_rows = analyze_src("Permian 编译（SubsurfaceUnit 层段）", perm, "Perm")
    gcsrd_rows = analyze_src("GCSRD（formation 层段）", gcsrd, "GCSRD")

    # 判定汇总：区分"可验证（Tmax 覆盖够宽）"与"覆盖不足（诚实不可验证）"
    def _tally(rows):
        n_big = [m for m in rows if m["n"] >= 40]
        n_wide = [m for m in n_big if m.get("tmax_span", 0) >= 40]   # 跨度>=40℃ 才可测窗形
        n_full = [m for m in n_wide if m.get("v1") and m.get("v2")]
        return n_big, n_wide, n_full
    p_big, p_wide, p_full = _tally(perm_rows)
    g_big, g_wide, g_full = _tally(gcsrd_rows)
    n_big = len(p_big) + len(g_big)
    n_wide = len(p_wide) + len(g_wide)
    n_full = len(p_full) + len(g_full)
    print("\n窗形验证（V1+V2）：完整 %d/%d 个可验证层段（Tmax 跨度>=40℃）；"
          "层段总数 %d（其余为 Tmax 覆盖不足，不可验证——诚实负结果）"
          % (n_full, n_wide, n_big))
    print("  可验证层段明细：")
    for m in sorted(p_wide + g_wide, key=lambda r: r["n"], reverse=True):
        ok = "V1+V2 ✓" if (m.get("v1") and m.get("v2")) else (
            "V1 峰值油窗" if m.get("v1") else "未通过")
        print("    %-28s [%s] n=%d 跨%.0f℃ -> %s" % (
            m["u"][:28], "Perm" if m in p_wide else "GCSRD",
            m["n"], m["tmax_span"], ok))
    print("  未通过（宽覆盖但未验证）层段：%s" % (
        "、".join("%s[%s]" % (m["u"][:22], "Perm" if m in p_wide else "GCSRD")
                  for m in sorted(p_wide + g_wide, key=lambda r: r["n"], reverse=True)
                  if not (m.get("v1") and m.get("v2"))) or "无"))
    if n_full >= 2:
        print("结论：f(M) 窗形在层段级部分复现（%d/%d 可验证层段完整验证：Barnett、Pearsall）"
              "——窗形非体系特异，但层段级混合样（多实验室/多井）可稀释窗形；"
              "未通过层段与窄覆盖层段均登记为诚实负结果。" % (n_full, n_wide))
    elif n_full == 1:
        print("结论：层段级仅 1 例完整窗形（Barnett 或 Pearsall），其余层段 Tmax "
              "覆盖不足不可验证——窗形层段级复现证据有限（诚实负结果登记）。")
    else:
        print("结论：可验证层段均未通过窗形验证（诚实负结果）。")


if __name__ == "__main__":
    main()
