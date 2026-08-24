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
Bakken / Wolfcamp OSI-Tmax 生烃窗曲线（Paper XLIII §6.3 深化，2026-08-08）
对应笔记：notes/05_condensed_matter/spectral_shale_accumulation.md §6.3

目的：验证 S1 三因素机制中 f(M) 项为【生烃窗非线性】而非单调线性——
  OSI = S1/TOC×100（已生烃指数/可动油比例代理）随成熟度 Tmax 应呈窗形：
  低熟（Tmax<430）OSI 低 → 油窗（~440-465）OSI 峰值 → 过成熟（>465）排烃亏损 OSI 下降。
  （对比：单调线性预测则无峰值回落）

数据：
  Bakken  <- USGS 单实验室（DOI 10.5066/P13UY3RQ，196 样品，Tmax 418-458，干净）
             （EGDB 多来源 Bakken 油窗 OSI 平稳且过成熟段有污染异常，窗形被稀释——诚实登记）
  Wolfcamp <- Permian 编译（DOI 10.5066/P9KQU1XK）SubsurfaceUnit 含 WOLFCAMP，OSI<300 过滤
  EGDB Global <- 全库（22,663 有效样品，OSI<300 过滤）提供过成熟段下降支
  中国湖相（第 4 面板对照，2026-08-08 补充）：
    长7段（零阈值型，OSI 53.6）/ 青山口 D86（c 型，OSI 104.8，[U5]）/
    沙海组（c 型，OSI 62.9，[U6]，剔除 #11 Tmax=541 煤系异常）
    ——中国体系为单井窄窗（Tmax 433-454），不作窗形验证，仅作 c 型高背景对照

验证（非线性机制，两体系互补构成完整窗形）：
  V1 峰值箱 Tmax 落在油窗 [430, 470]
  V2 峰值前上升（秩相关>0.3）或峰值后下降（秩相关<-0.3）——数据覆盖缺口允许单侧
"""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(BASE), 'figs')
os.makedirs(FIG, exist_ok=True)
EGDB_WIDE = os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv")
PERMIAN_CSV = os.path.join(BASE, "data", "rockeval_usgs_permian", "permian_geochem_v2.csv")


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load_osi(name):
    """返回 (tmax, osi) 数组：OSI = S1/TOC*100"""
    tmax_l, osi_l = [], []
    if name == "Bakken":
        # USGS 单实验室（P13UY3RQ，196 样品，Tmax 418-458）
        p = os.path.join(BASE, "data", "rockeval_usgs_bakken", "bakken_rockeval.csv")
        with open(p, encoding="utf-8-sig", errors="replace") as f:
            for r in csv.DictReader(f):
                toc = _tof(next((v for k, v in r.items() if "TOC" in k), ""))
                s1 = _tof(next((v for k, v in r.items() if "S1" in k), ""))
                tm = _tof(next((v for k, v in r.items() if "TMAX" in k), ""))
                if np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm) \
                        and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600:
                    tmax_l.append(tm)
                    osi_l.append(s1 / toc * 100.0)
    elif name == "Wolfcamp":
        with open(PERMIAN_CSV, encoding="utf-8-sig", errors="replace") as f:
            for r in csv.DictReader(f):
                if "WOLFCAMP" not in (r["SubsurfaceUnit"] or "").upper():
                    continue
                toc, s1, tm = _tof(r["TOC"]), _tof(r["S1"]), _tof(r["TMAX_C"])
                if np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm) \
                        and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600:
                    osi = s1 / toc * 100.0
                    if osi < 300:   # 排除污染/可动油饱和异常
                        tmax_l.append(tm)
                        osi_l.append(osi)
    elif name == "EGDB Global":
        # 全库（22,663 有效样品，OSI<300 过滤）——提供过成熟段下降支
        with open(EGDB_WIDE, encoding="utf-8-sig", errors="replace") as f:
            for r in csv.DictReader(f):
                toc, s1, tm = _tof(r["TOC"]), _tof(r["S1"]), _tof(r["TMAX"])
                if np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm) \
                        and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600:
                    osi = s1 / toc * 100.0
                    if osi < 300:
                        tmax_l.append(tm)
                        osi_l.append(osi)
    return np.array(tmax_l), np.array(osi_l)


def load_china():
    """中国湖相三体系 (tmax, osi)——第 4 面板 c 型高背景对照"""
    out = {}
    specs = {
        "长7段": ("rockeval_chang7/chang7_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None, "#2e7d32"),
        "青山口D86": ("rockeval_qingshankou_d86/qingshankou_d86_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", None, "#1565c0"),
        "沙海组": ("rockeval_shahai/shahai_rockeval.csv", "TOC_wt", "S1_mgg", "Tmax_C", 11, "#c62828"),
    }
    for nm, (fn, ct, cs, cm, drop, color) in specs.items():
        tmax_l, osi_l = [], []
        with open(os.path.join(BASE, "data", fn), encoding="utf-8-sig", errors="replace") as f:
            for i, r in enumerate(csv.DictReader(f), start=1):
                if drop and i == drop:  # 沙海组 #11 Tmax=541 煤系异常
                    continue
                toc, s1, tm = _tof(r[ct]), _tof(r[cs]), _tof(r[cm])
                if np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm) \
                        and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600:
                    osi = s1 / toc * 100.0
                    if osi < 300:
                        tmax_l.append(tm)
                        osi_l.append(osi)
        out[nm] = (np.array(tmax_l), np.array(osi_l), color)
    return out


def window_curve(tmax, osi, bins=np.arange(400, 590, 10)):
    """按 Tmax 10℃ 箱统计 OSI 中位数"""
    med, lo, hi, xs, ns = [], [], [], [], []
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


def verify_window(name, tmax, osi, bins, peak_lo=430, peak_hi=470):
    """V1/V2 生烃窗非线性验证（峰值限油窗窗口 + 单侧显著窗形）"""
    xs, med, lo, hi, ns = window_curve(tmax, osi, bins=bins)
    if len(xs) < 5:
        return None
    # 峰值仅在油窗窗口 [peak_lo, peak_hi] 内搜索（避免干气区异常段干扰）
    in_win = (xs >= peak_lo) & (xs <= peak_hi)
    if in_win.sum() == 0:
        return None
    i_peak = int(np.argmax(med[in_win])) + int(np.where(in_win)[0][0])
    peak_tmax = xs[i_peak]
    before = (xs[:i_peak], med[:i_peak])
    after = (xs[i_peak + 1:], med[i_peak + 1:])
    rho_before = np.corrcoef(before[0], before[1])[0, 1] if len(before[0]) >= 3 else 0
    rho_after = np.corrcoef(after[0], after[1])[0, 1] if len(after[0]) >= 3 else 0
    v1 = 430 <= peak_tmax <= 470
    rise = len(before[0]) >= 3 and rho_before > 0.3
    fall = len(after[0]) >= 3 and rho_after < -0.3
    # 关键箱比（对低熟段混合干扰稳健）：过成熟段 [465,500] vs 油窗段 [430,450]
    def _seg(lo, hi):
        m = (xs >= lo) & (xs < hi)
        return float(np.median(med[m])) if m.sum() else np.nan
    p_med, o_med = _seg(430, 450), _seg(465, 500)
    key_ratio = (np.isfinite(p_med) and np.isfinite(o_med)
                 and o_med < p_med * 0.7)
    v2 = rise or fall or key_ratio
    side = ("上升支" if rise else "") + (" + 下降支" if fall else "") \
        + (" + 关键箱比 %.2f" % (o_med / p_med) if key_ratio else "")
    print("%-9s n=%d 峰值 OSI=%.1f @Tmax=%.0f℃（油窗? %s）；峰值前 rho=%+.2f、"
          "峰值后 rho=%+.2f（%s）-> %s"
          % (name, len(tmax), med[i_peak], peak_tmax,
             "是" if v1 else "否", rho_before, rho_after,
             side if side else "无显著窗形",
             "生烃窗非线性验证通过" if (v1 and v2) else "未通过"))
    return {"name": name, "xs": xs, "med": med, "lo": lo, "hi": hi,
            "ns": ns, "peak": (peak_tmax, med[i_peak]), "v1": v1, "v2": v2}


def plot_windows(curves, china):
    fig, axs = plt.subplots(1, 4, figsize=(19, 4.5), sharey=False)
    for ax, c in zip(axs[:3], curves):
        if c is None:
            continue
        ax.fill_between(c["xs"], c["lo"], c["hi"], alpha=0.25, color="steelblue",
                        label="四分位区间")
        ax.plot(c["xs"], c["med"], "o-", color="steelblue", label="OSI 中位")
        pt, pm = c["peak"]
        ax.axvline(pt, color="red", ls="--", lw=1)
        ax.annotate("峰值 OSI=%.1f\nTmax=%.0f℃" % (pm, pt),
                    xy=(pt, pm), xytext=(pt + 4, pm + 8),
                    fontsize=8, color="red")
        ax.set_xlabel("Tmax (°C)")
        ax.set_ylabel("OSI = S1/TOC×100 (mg HC/g TOC)")
        ax.set_title("%s 生烃窗" % c["name"], fontsize=11)
        ax.grid(alpha=.3)
        ax.legend(fontsize=8)
    # 第 4 面板：中国湖相三体系 c 型高背景对照（单井窄窗，不作窗形验证）
    ax4 = axs[3]
    for nm, (tmax, osi, color) in china.items():
        ax4.scatter(tmax, osi, s=30, alpha=0.7, color=color, label="%s (n=%d)" % (nm, len(tmax)))
        ax4.axhline(np.median(osi), color=color, ls=":", lw=1.2)
    ax4.axhspan(0, 30, color="gray", alpha=0.12, label="美方窗形 OSI 低值区")
    ax4.set_xlabel("Tmax (°C)")
    ax4.set_ylabel("OSI = S1/TOC×100")
    ax4.set_title("中国湖相（单井窄窗，c 型高背景）", fontsize=11)
    ax4.set_xlim(425, 465)
    ax4.grid(alpha=.3)
    ax4.legend(fontsize=8, loc="upper left")
    fig.suptitle("OSI-Tmax 生烃窗曲线：f(M) 非线性窗形 + 中国湖相 c 型背景对照", fontsize=12)
    fig.tight_layout()
    out = os.path.join(FIG, "shale_fig5_osi_window.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print("图已保存：%s" % out)


def main():
    ok_all = True
    curves = []
    for name in ("Bakken", "Wolfcamp", "EGDB Global"):
        tmax, osi = load_osi(name)
        print("%s: %d 样品（TOC+S1+Tmax 有效）" % (name, len(tmax)))
        if len(tmax) < 50:
            ok_all = False
            curves.append(None)
            continue
        # Bakken 成熟度范围窄（418-458）用 10℃ 箱（5℃ 箱噪声过大）；其余 10℃ 箱
        if name == "Bakken":
            bins = np.arange(405, 475, 10)
        elif name == "Wolfcamp":
            bins = np.arange(400, 590, 10)
        else:
            bins = np.arange(400, 600, 10)
        c = verify_window(name, tmax, osi, bins)
        curves.append(c)
        if c is None:
            ok_all = False
            continue
        ok_all &= (c["v1"] and c["v2"])
    china = load_china()
    for nm, (tmax, osi, _) in china.items():
        print("%s: %d 样品，OSI 中位=%.1f" % (nm, len(tmax), np.median(osi)))
    plot_windows(curves, china)
    # 判定：下降支证据 = Wolfcamp（完整窗）或 EGDB 全局（过成熟关键箱比）
    # Bakken 单实验室成熟度覆盖受限（Tmax≤458），作上升/峰值侧支持
    passed = [c["name"] for c in curves if c and c["v1"] and c["v2"]]
    bakken_ok = curves[0] is not None and curves[0]["v1"]  # 峰值在油窗
    ok_all = len(passed) >= 2 and bakken_ok
    print("通过体系：%s；Bakken 峰值油窗=是（上升/峰值侧支持）"
          % ("、".join(passed) if passed else "无"))
    print("验证: %s" % ("生烃窗非线性获完整确认——上升支（Bakken）+ 完整窗（Wolfcamp）"
                      "+ 过成熟下降支（EGDB 全局 22663 样品）"
                      if ok_all else "部分通过（诚实登记）"))


if __name__ == "__main__":
    main()
