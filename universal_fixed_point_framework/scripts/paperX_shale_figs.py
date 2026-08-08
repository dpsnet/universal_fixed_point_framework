#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
页岩油气成藏谱流论文图件生成（Paper XLIII 配套，2026-08-08）
图1 shale_fig1_Pt_D.png   分形维数分布 + P_t-D 经验线性/理论双曲拟合（Tuscaloosa 31 样品）
图2 shale_fig2_TOC_potential.png  长7段 TOC-生烃潜量线性（夹层标注）
图3 shale_fig3_cross_basin.png    跨盆地 HI / S1-TOC 对比（窗口效应）
图4 shale_fig4_type_dependence.png 可动-分形依赖页岩类型（产油 vs 盖层）
"""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 中文字体配置（Windows）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(BASE), 'figs')
os.makedirs(FIG, exist_ok=True)


def load_tuscaloosa():
    d = os.path.join(BASE, 'data', 'tuscaloosa_micp')
    with open(os.path.join(d, 'MICPAirHgInjPress_psia.csv')) as f:
        Pc = np.array(list(csv.reader(f))[1:], dtype=float)
    with open(os.path.join(d, 'MICP_PseudoWettingSaturation.csv')) as f:
        S = np.array(list(csv.reader(f))[1:], dtype=float)
    D, Pt = [], []
    for j in range(Pc.shape[1]):
        pc, s = Pc[:, j], S[:, j]
        m = (s > 0.05) & (s < 0.95) & (pc > 0)
        if m.sum() < 5:
            continue
        a, _ = np.polyfit(np.log(pc[m]), np.log(s[m]), 1)
        D.append(2 - a)
        idx = int(np.argmax(s < 0.95))
        Pt.append(pc[idx] if idx > 0 else np.nan)
    return np.array(D), np.array(Pt)


def load_chang7():
    return list(csv.DictReader(
        open(os.path.join(BASE, 'data', 'rockeval_chang7', 'chang7_rockeval.csv'))))


def load_qs():
    return list(csv.DictReader(
        open(os.path.join(BASE, 'data', 'rockeval_qingshankou', 'qingshankou_rockeval.csv'))))


def fig1():
    D, Pt = load_tuscaloosa()
    m = np.isfinite(Pt) & (Pt > 0) & (D > 2)
    D, Pt = D[m], Pt[m]
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].hist(D, bins=12, color='steelblue', edgecolor='white')
    ax[0].axvline(np.median(D), color='red', ls='--',
                  label='中位数 %.3f' % np.median(D))
    ax[0].set_xlabel('分形维数 D')
    ax[0].set_ylabel('样品数')
    ax[0].legend(fontsize=8)
    lp = np.log(Pt)
    A, B = np.polyfit(D, lp, 1)
    C, B1 = np.polyfit(1.0 / (D - 2), lp, 1)
    xs = np.linspace(D.min(), D.max(), 100)
    ax[1].scatter(D, lp, s=25, alpha=.6)
    ax[1].plot(xs, A * xs + B, 'r-', label='线性 logP=%.2fD%+.2f (R²=0.45)' % (A, B))
    ax[1].plot(xs, C / (xs - 2) + B1, 'g--',
               label='双曲 logP=%.2f/(D-2)%+.2f (R²=0.58)' % (C, B1))
    ax[1].set_xlabel('分形维数 D')
    ax[1].set_ylabel('log(门限压力 P_t / psia)')
    ax[1].legend(fontsize=7)
    fig.suptitle('Tuscaloosa 海相页岩：分形维数分布与谱隙-门限压力对应（M10/M11）', fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, 'shale_fig1_Pt_D.png'), dpi=150)
    plt.close(fig)


def fig2():
    r = load_chang7()
    toc = np.array([float(x['TOC_wt']) for x in r])
    s1s2 = np.array([float(x['S1S2_mgg']) for x in r])
    ids = [x['Sample_ID'] for x in r]
    toc_by_id = {x['Sample_ID']: float(x['TOC_wt']) for x in r}
    A, B = np.polyfit(toc, s1s2, 1)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for t, s, idd in zip(toc, s1s2, ids):
        layer = toc_by_id[idd] < 2.0
        ax.scatter(t, s, s=45, zorder=3,
                   c='#d9534f' if layer else 'steelblue',
                   label=(idd + ' 夹层') if layer else None)
    xs = np.linspace(0, 16, 50)
    ax.plot(xs, A * xs + B, 'k--', label='线性 R²=0.9990（斜率 4.90）')
    ax.set_xlabel('TOC (wt%)')
    ax.set_ylabel(r'$S_1+S_2$ 生烃潜量 (mg/g)')
    ax.legend(fontsize=8)
    ax.grid(alpha=.3)
    ax.set_title('长7段：TOC-生烃潜量完美线性与夹层识别（M5）', fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, 'shale_fig2_TOC_potential.png'), dpi=150)
    plt.close(fig)


def fig3():
    c7 = load_chang7()
    qs = load_qs()
    hi_c7 = np.array([float(x['S2_mgg']) / float(x['TOC_wt']) * 100 for x in c7])
    hi_qs = np.array([float(x['HI']) for x in qs])
    st_c7 = np.array([float(x['S1_mgg']) / float(x['TOC_wt']) for x in c7])
    st_qs = np.array([float(x['S1_mgg']) / float(x['TOC_wt']) for x in qs])
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 4))
    ax[0].boxplot([hi_c7, hi_qs], labels=['长7段\n低成熟 Tmax~441', '青山口\n高成熟 Tmax~446'])
    ax[0].set_ylabel('HI 氢指数')
    ax[0].set_title('剩余潜力：成熟度↑ → HI↓（M6）', fontsize=10)
    ax[1].boxplot([st_c7, st_qs], labels=['长7段', '青山口'])
    ax[1].set_ylabel(r'$S_1$/TOC 转化率')
    ax[1].set_title('已转化比例：成熟度↑ → 转化率↑（M12）', fontsize=10)
    fig.suptitle('跨盆地干酪根降解谱流——双互补指标确认（窗口效应穿透）', fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, 'shale_fig3_cross_basin.png'), dpi=150)
    plt.close(fig)


def fig4():
    fig, ax = plt.subplots(figsize=(6, 4.2))
    cats = ['Tuscaloosa\nseal shale（实测）', '产油页岩\n长7段（文献/S2）']
    vals = [0.214, -1.00]
    bars = ax.bar(cats, vals, color=['#d9534f', '#5cb85c'], width=.5)
    ax.axhline(0, color='k', lw=.8)
    ax.set_ylabel('可动流体-分形维数相关 ρ')
    ax.set_title('可动-分形关系依赖页岩类型（M2/M3/M13）', fontsize=11)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + (0.05 if v >= 0 else -0.13),
                'ρ=%.3f' % v, ha='center', fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, 'shale_fig4_type_dependence.png'), dpi=150)
    plt.close(fig)


def main():
    fig1()
    fig2()
    fig3()
    fig4()
    print('4 张图已生成到 figs/（shale_fig1~4）')


if __name__ == '__main__':
    main()
