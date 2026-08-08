#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
页岩油气成藏谱流论文图件生成 II（Paper XLIII 正式版配套，2026-08-08）
图7 shale_fig7_zero_threshold.png   零注入阈值判据（长7段 S1-TOC 低端趋零 + TOC* 外推 + 三判据）
图8 shale_fig8_c_attr_drive.png     c 项成熟度结构驱动（EGDB 体系 c 代理 vs Tmax p95）
"""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
try:
    from scipy import stats as st
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(BASE), 'figs')
os.makedirs(FIG, exist_ok=True)


def _tof(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def load_chang7():
    out = []
    with open(os.path.join(BASE, "data", "rockeval_chang7", "chang7_rockeval.csv"),
              encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            toc, s1 = _tof(r["TOC_wt"]), _tof(r["S1_mgg"])
            if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0:
                out.append((toc, s1))
    return np.array(out)


def fig7():
    """零注入阈值判据（P4）：长7段 S1-TOC 线性注入 + 负截距外推 TOC* + 低端趋零放大"""
    d = load_chang7()
    toc, s1 = d[:, 0], d[:, 1]
    a, b = np.polyfit(toc, s1, 1)
    r2 = 1.0 - np.sum((s1 - (a * toc + b)) ** 2) / np.sum((s1 - s1.mean()) ** 2)
    toc_star = -b / a                       # 负截距外推零点
    # Z2 低/高 TOC 半区 S1 中位比
    med = np.median(toc)
    lo, hi = s1[toc <= med], s1[toc > med]
    z2 = float(np.median(lo) / np.median(hi))
    z3 = float(s1.min())
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    xs = np.linspace(0, 8, 100)
    ax[0].scatter(toc, s1, s=45, c='steelblue', zorder=3, label='长7段样品')
    ax[0].plot(xs, a * xs + b, 'k-', lw=1.5,
               label='S1=%.2f·TOC%+.2f（R²=%.3f）' % (a, b, r2))
    ax[0].plot(xs, a * xs + b, 'k-', lw=0)
    # 负截距外推至零点：TOC*
    ax[0].plot(xs, np.clip(a * xs + b, -9, 9), 'r--', lw=1.2)
    ax[0].axvline(toc_star, color='red', ls=':', lw=1.4)
    ax[0].text(toc_star + 0.12, 0.55, 'TOC*≈%.2f wt%%' % toc_star,
               color='red', fontsize=10)
    ax[0].axhline(0, color='gray', lw=.6)
    ax[0].set_xlabel('TOC (wt%)')
    ax[0].set_ylabel('S1 (mg/g)')
    ax[0].set_title('线性注入与负截距外推（Z1：R²=%.3f）' % r2, fontsize=10)
    ax[0].legend(fontsize=8)
    ax[0].grid(alpha=.3)
    # 低端放大：TOC < 4 wt%
    m = toc < 4.0
    ax[1].scatter(toc[m], s1[m], s=55, c='#d9534f', zorder=3)
    ax[1].plot(xs[xs < 4], np.clip(a * xs[xs < 4] + b, 0, 9), 'k-', lw=1.5)
    ax[1].axvline(toc_star, color='red', ls=':', lw=1.4)
    ax[1].annotate('TOC*（干酪根初次生烃临界）', xy=(toc_star, 0.02),
                   xytext=(1.1, 0.62), fontsize=9, color='red',
                   arrowprops=dict(arrowstyle='->', color='red', lw=1))
    ax[1].set_xlabel('TOC (wt%)')
    ax[1].set_ylabel('S1 (mg/g)')
    ax[1].set_title('低端趋零放大：Z2 低/高比=%.3f，Z3 minS1=%.3f' % (z2, z3), fontsize=10)
    ax[1].grid(alpha=.3)
    fig.suptitle('长7段零注入阈值判据（三判据齐备：Z1 线性度≥0.90 + Z2 低端趋零<0.35 + Z3 c→0）',
                 fontsize=11)
    fig.tight_layout()
    out = os.path.join(FIG, 'shale_fig7_zero_threshold.png')
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print('图7 已生成：%s（TOC*=%.3f wt%%，R²=%.3f，Z2=%.3f，Z3=%.3f）'
          % (out, toc_star, r2, z2, z3))


def load_egdb_systems():
    """返回 {体系: Tmax列表, TOC<0.5 的 S1 列表}（n>=150 体系）"""
    sysd = {}
    with open(os.path.join(BASE, "data", "rockeval_usgs_egdb", "egdb_re_wide.csv"),
              encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            toc, s1, tm = _tof(r["TOC"]), _tof(r["S1"]), _tof(r["TMAX"])
            if not (np.isfinite(toc) and np.isfinite(s1) and np.isfinite(tm)
                    and 0 < toc < 30 and s1 >= 0 and 350 < tm < 600):
                continue
            if s1 / toc * 100.0 >= 300:
                continue
            fm = (r["Formation"] or "NA").strip().upper()
            if fm in {"BAKKEN", "BAKKEN UPPER", "BAKKEN LOWER", "BAKKEN SILTSTONE"}:
                fm = "BAKKEN"
            d = sysd.setdefault(fm, {"tm": [], "s1lo": []})
            d["tm"].append(tm)
            if toc < 0.5:
                d["s1lo"].append(s1)
    return sysd


def fig8():
    """c 项成熟度结构驱动（C2）：c 代理（TOC<0.5 S1 中位）vs 体系 Tmax p95"""
    if not HAS_SCIPY:
        print("需要 scipy")
        return
    sysd = load_egdb_systems()
    rows = []
    for fm, d in sysd.items():
        tm = np.array(d["tm"])
        s1lo = np.array(d["s1lo"])
        if len(tm) < 150 or len(s1lo) < 10:
            continue
        rows.append((fm, float(np.percentile(tm, 95)),
                     float(np.median(s1lo)), len(tm)))
    rows.sort(key=lambda t: -t[2])
    fm_l, tm95, c, n = zip(*rows)
    rho, pv = st.spearmanr(tm95, c)
    rp, pp = st.pearsonr(tm95, c)
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.scatter(tm95, c, s=90, c='steelblue', zorder=3)
    for x, y, nm in zip(tm95, c, fm_l):
        ax.annotate(nm, (x, y), xytext=(5, 5), textcoords='offset points',
                    fontsize=8)
    xs = np.linspace(min(tm95), max(tm95), 50)
    a, b = np.polyfit(tm95, c, 1)
    ax.plot(xs, a * xs + b, 'r--', lw=1.3,
            label='线性：c=%.4f·Tmax_p95%+.2f' % (a, b))
    ax.set_xlabel('体系成熟度结构 Tmax p95 (℃)')
    ax.set_ylabel('c 代理（TOC<0.5 wt% 端 S1 中位，mg/g）')
    ax.set_title('运移烃背景项 c 由体系成熟度结构驱动（n=%d 体系）' % len(rows), fontsize=11)
    ax.text(0.04, 0.93, 'Spearman ρ=%+.2f（p=%.2f）\nPearson r=%+.2f（p=%.2f）'
            % (rho, pv, rp, pp), transform=ax.transAxes, fontsize=10,
            bbox=dict(fc='white', ec='gray', alpha=.9))
    ax.legend(fontsize=8)
    ax.grid(alpha=.3)
    fig.tight_layout()
    out = os.path.join(FIG, 'shale_fig8_c_attr_drive.png')
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print('图8 已生成：%s（n=%d 体系，Spearman ρ=%+.2f p=%.2f；Pearson r=%+.2f p=%.2f）'
          % (out, len(rows), rho, pv, rp, pp))


def main():
    fig7()
    fig8()
    print('图 7/8 已生成到 figs/')


if __name__ == '__main__':
    main()
