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
页岩油气成藏谱流论文图件生成 II（Paper XLIII 正式版配套，2026-08-08 扩展多井）
图7 shale_fig7_zero_threshold.png   零注入阈值判据（长7段 CY 井 S1-TOC 低端趋零 + TOC* 外推 + 三判据；F75/N228 井 c 型对照）
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


def load_chang7_wells():
    """多井/多区分组：{'CY': (n,2), 'F75': ..., 'N228': ..., 'Zhou': ..., 'Fan': ...}"""
    wells = {}
    for key, rel in (("CY", os.path.join("data", "rockeval_chang7", "chang7_rockeval.csv")),
                     ("F75", os.path.join("data", "rockeval_chang7_f75", "chang7_f75_rockeval.csv")),
                     ("N228", os.path.join("data", "rockeval_chang7_n228", "chang7_n228_rockeval.csv")),
                     ("Zhou", os.path.join("data", "rockeval_chang7_zhou", "zhou2024_tbl3.csv")),
                     ("Fan", os.path.join("data", "rockeval_chang7_fan2023", "chang7_fan2023_rockeval.csv"))):
        pts = []
        with open(os.path.join(BASE, rel), encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f)
            header = next(r for r in reader if r and not r[0].lstrip().startswith("#"))
            idx_t, idx_s = header.index("TOC_wt"), header.index("S1_mgg")
            for r in reader:
                if not r or r[0].lstrip().startswith("#"):
                    continue
                toc, s1 = _tof(r[idx_t]), _tof(r[idx_s])
                if np.isfinite(toc) and np.isfinite(s1) and 0 < toc < 30 and s1 >= 0:
                    pts.append((toc, s1))
        wells[key] = np.array(pts)
    return wells


def fig7():
    """零注入阈值判据（P4）：长7段多井/多区——CY 井零阈值（线性注入+TOC*+低端趋零）
    vs F75/N228 井 c 型（低端 S1 底板）vs Zhou2024 中央区（低端趋零但线性度受限）"""
    wells = load_chang7_wells()
    d = wells["CY"]
    toc, s1 = d[:, 0], d[:, 1]
    a, b = np.polyfit(toc, s1, 1)
    r2 = 1.0 - np.sum((s1 - (a * toc + b)) ** 2) / np.sum((s1 - s1.mean()) ** 2)
    toc_star = -b / a                       # 负截距外推零点
    # Z2 低/高 TOC 半区 S1 中位比
    med = np.median(toc)
    lo, hi = s1[toc <= med], s1[toc > med]
    z2 = float(np.median(lo) / np.median(hi))
    z3 = float(s1.min())
    fig, ax = plt.subplots(2, 2, figsize=(11, 8.6))
    xs = np.linspace(0, 24, 100)
    ax = ax.ravel()
    # (a) CY 井线性注入与负截距外推
    ax[0].scatter(toc, s1, s=45, c='steelblue', zorder=3, label='CY井（n=10）')
    ax[0].plot(xs, np.clip(a * xs + b, -9, 9), 'r--', lw=1.2)
    ax[0].axvline(toc_star, color='red', ls=':', lw=1.4)
    ax[0].text(toc_star + 0.12, 0.55, 'TOC*≈%.2f wt%%' % toc_star,
               color='red', fontsize=10)
    ax[0].axhline(0, color='gray', lw=.6)
    ax[0].set_xlabel('TOC (wt%)')
    ax[0].set_ylabel('S1 (mg/g)')
    ax[0].set_title('(a) CY井线性注入与负截距外推（Z1：R²=%.3f）' % r2, fontsize=10)
    ax[0].legend(fontsize=8)
    ax[0].grid(alpha=.3)
    # (b) CY 井低端放大
    m = toc < 4.0
    ax[1].scatter(toc[m], s1[m], s=55, c='#d9534f', zorder=3)
    ax[1].plot(xs[xs < 4], np.clip(a * xs[xs < 4] + b, 0, 9), 'k-', lw=1.5)
    ax[1].axvline(toc_star, color='red', ls=':', lw=1.4)
    ax[1].annotate('TOC*（干酪根初次生烃临界）', xy=(toc_star, 0.02),
                   xytext=(1.1, 0.62), fontsize=9, color='red',
                   arrowprops=dict(arrowstyle='->', color='red', lw=1))
    ax[1].set_xlabel('TOC (wt%)')
    ax[1].set_ylabel('S1 (mg/g)')
    ax[1].set_title('(b) CY井低端趋零：Z2 低/高比=%.3f，Z3 minS1=%.3f' % (z2, z3), fontsize=10)
    ax[1].grid(alpha=.3)
    # (c) 多井/多区 S1-TOC 叠加
    colors = {'CY': 'steelblue', 'F75': '#d9534f', 'N228': 'seagreen', 'Zhou': '#8e44ad', 'Fan': '#e67e22'}
    marks = {'CY': 'o', 'F75': 's', 'N228': '^', 'Zhou': 'D', 'Fan': 'v'}
    labels = {'CY': 'CY井（n=10，零阈值型）', 'F75': 'F75井（n=23，Chen 2021）',
              'N228': 'N228井（n=9，崔德艺2023）', 'Zhou': 'Zhou2024中央区（n=38）',
              'Fan': 'Fan2023陇东（n=10）'}
    fits = {}
    for k in ("CY", "F75", "N228", "Zhou", "Fan"):
        w = wells[k]
        xk, yk = w[:, 0], w[:, 1]
        ak, bk = np.polyfit(xk, yk, 1)
        r2k = 1.0 - np.sum((yk - (ak * xk + bk)) ** 2) / np.sum((yk - yk.mean()) ** 2)
        fits[k] = (ak, bk, r2k)
        ax[2].scatter(xk, yk, s=40, c=colors[k], marker=marks[k],
                      zorder=3, label='%s（S1=%.2f·TOC%+.2f，R²=%.2f）' % (labels[k], ak, bk, r2k))
        xr = np.linspace(xk.min(), xk.max(), 60)
        ax[2].plot(xr, ak * xr + bk, ls='--', lw=1.0, c=colors[k], alpha=.7)
    ax[2].set_xlabel('TOC (wt%)')
    ax[2].set_ylabel('S1 (mg/g)')
    ax[2].set_title('(c) 长7段多井/多区 S1-TOC：零阈值型 vs c 型并存', fontsize=10)
    ax[2].legend(fontsize=7.5, loc='upper left')
    ax[2].grid(alpha=.3)
    # (d) 低 TOC 窗口：c 型低端 S1 底板 vs CY 零阈值
    for k in ("CY", "F75", "N228", "Zhou", "Fan"):
        w = wells[k]
        wk = w[(w[:, 0] < 6.0)] if k not in ("N228", "Fan") else w
        ax[3].scatter(wk[:, 0], wk[:, 1], s=40, c=colors[k], marker=marks[k],
                      zorder=3, label=labels[k])
        if len(wk) > 0:
            ax[3].axhline(np.median(wk[:, 1]), color=colors[k], ls=':', lw=1.0)
    ax[3].set_xlabel('TOC (wt%)')
    ax[3].set_ylabel('S1 (mg/g)')
    ax[3].set_title('(d) 低端 TOC 窗口：c 型 S1 底板非零 vs CY 井趋零', fontsize=10)
    ax[3].legend(fontsize=8, loc='upper left')
    ax[3].grid(alpha=.3)
    fig.suptitle('长7段零注入阈值判据（CY 井三判据齐备 vs F75/N228/Fan 井 c 型背景 vs Zhou2024 中央区弱背景）', fontsize=11)
    fig.tight_layout()
    out = os.path.join(FIG, 'shale_fig7_zero_threshold.png')
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print('图7 已生成：%s（CY TOC*=%.3f wt%%，R²=%.3f，Z2=%.3f，Z3=%.3f）'
          % (out, toc_star, r2, z2, z3))
    for k in ("CY", "F75", "N228", "Zhou", "Fan"):
        ak, bk, r2k = fits[k]
        print('   %s：S1=%.3f·TOC%+.3f（R²=%.3f，n=%d）' % (k, ak, bk, r2k, len(wells[k])))


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
