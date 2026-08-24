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
"""D_plateau 解析公式与 L=16→256 全范围仿真数据对比图。

理论预测：
  D_red(L) = d_min - beta_eff + O(L^{-1/nu})
  d_min ≈ 1.374, beta_eff ≈ 0.52  →  D_red ≈ 0.854
  P3 预言: D_b = 0.631

仿真数据（N_CFG=3, D=2.4, c=0, Tarjan 算法 + 快速 BFS 骨架提取）
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 仿真数据（§12.9.1 第十步）
# ============================================================
L_vals = np.array([16, 32, 48, 64, 96, 128, 256])
Db_mean = np.array([0.869, 0.815, 0.971, 0.817, 0.790, 0.869, 0.764])
Db_std  = np.array([0.164, 0.151, 0.209, 0.083, 0.077, 0.028, 0.053])
n_red   = np.array([12, 21, 45, 38, 102, 124, 162])

# 理论预测
D_MIN = 1.374          # 渗流最短路径分形维数
BETA_EFF = 0.52        # 红键密度衰减指数
D_RED_THEORY = D_MIN - BETA_EFF  # ≈ 0.854
D_P3 = 0.631           # P3 预言
D_RED_INF = 1.0 / 0.876  # 1/ν ≈ 1.141（无限极限）

# ============================================================
# 绘图：双面板（D_b vs L  +  n_red vs L）
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), gridspec_kw={'height_ratios': [3, 2]})

# ---- 上图：D_b(red) vs L ----
ax1.errorbar(L_vals, Db_mean, yerr=Db_std, fmt='o', color='#1f77b4',
             ecolor='#1f77b4', elinewidth=1.5, capsize=5, markersize=8,
             label=r'$D_b(\mathrm{red})$ 仿真 (N$_\mathrm{CFG}$=3)', zorder=5)

# 理论线
ax1.axhline(y=D_RED_THEORY, color='#d62728', linestyle='-', linewidth=2,
            label=rf'$D_{{\mathrm{{red}}}} = d_{{\min}} - \beta_{{\mathrm{{eff}}}} \approx {D_RED_THEORY:.3f}$' +
                  rf' ($d_{{\min}}={D_MIN}$, $\beta_{{\mathrm{{eff}}}}={BETA_EFF}$)')
ax1.axhline(y=D_P3, color='#2ca02c', linestyle='--', linewidth=2,
            label=rf'P3 预言 $D_b = {D_P3:.3f}$')
ax1.axhline(y=D_RED_INF, color='#ff7f0e', linestyle=':', linewidth=1.5,
            label=rf'$1/\nu \approx {D_RED_INF:.3f}$ (L$\to\infty$ 极限)')

# 整体均值带
overall_mean = np.mean(Db_mean)
overall_std = np.std(Db_mean)
ax1.fill_between([8, 320], overall_mean - overall_std, overall_mean + overall_std,
                 alpha=0.1, color='#1f77b4', label=f'仿真均值 {overall_mean:.3f}±{overall_std:.3f}')

ax1.set_xlabel('系统尺寸 L', fontsize=13)
ax1.set_ylabel(r'$D_b(\mathrm{red})$', fontsize=13)
ax1.set_title(r'D$_{\mathrm{plateau}}$ 解析公式与仿真对比：红键维数的有限尺寸标度', fontsize=14)
ax1.set_xscale('log', base=2)
ax1.set_xlim(8, 320)
ax1.set_ylim(0.4, 1.3)
ax1.legend(loc='lower right', fontsize=10, framealpha=0.9)
ax1.grid(True, alpha=0.3)

# 标注 L=256
ax1.annotate(f'L=256: {Db_mean[-1]:.3f}±{Db_std[-1]:.3f}\n(最接近 P3)',
             xy=(256, Db_mean[-1]), xytext=(180, 0.55),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'),
             bbox=dict(boxstyle='round,pad=0.3', fc='lightyellow', ec='gray', alpha=0.8))

# ---- 下图：n_red vs L（对数-对数） ----
ax2.loglog(L_vals, n_red, 's-', color='#9467bd', markersize=8, linewidth=1.5,
           label=r'$n_{\mathrm{red}}$ 仿真', zorder=5)

# 幂律拟合
log_L = np.log(L_vals)
log_n = np.log(n_red)
slope, intercept = np.polyfit(log_L, log_n, 1)
L_fit = np.linspace(16, 256, 100)
ax2.loglog(L_fit, np.exp(intercept) * L_fit**slope, '--', color='#9467bd', alpha=0.5,
           label=rf'幂律拟合: $n_{{\mathrm{{red}}}} \sim L^{{{slope:.2f}}}$')

# 理论参考线 n ~ L^{D_b}
for exp, label in [(0.854, r'$L^{0.854}$ (理论 $D_{\mathrm{red}}$)'), (1.141, r'$L^{1/\nu}$')]:
    ax2.loglog(L_fit, 12 * (L_fit / 16)**exp, ':', alpha=0.4,
               label=label)

ax2.set_xlabel('系统尺寸 L', fontsize=13)
ax2.set_ylabel(r'$n_{\mathrm{red}}$（红键数）', fontsize=13)
ax2.set_title(r'红键数 $n_{\mathrm{red}}$ 的标度', fontsize=14)
ax2.legend(loc='upper left', fontsize=10, framealpha=0.9)
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()

# 保存
fig_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'notes', '05_condensed_matter', 'figures')
os.makedirs(fig_dir, exist_ok=True)
save_path = os.path.join(fig_dir, 'paper43_Dplateau_comparison.png')
fig.savefig(save_path, dpi=150, bbox_inches='tight')
print(f'图已保存: {save_path}')

# 输出关键数值
print(f'\n=== 关键数值 ===')
print(f'理论预测: D_red = d_min - beta_eff = {D_MIN} - {BETA_EFF} = {D_RED_THEORY:.3f}')
print(f'仿真均值: {overall_mean:.3f} ± {overall_std:.3f}')
print(f'P3 预言:  {D_P3:.3f}')
print(f'1/nu:     {D_RED_INF:.3f}')
print(f'n_red 标度指数: {slope:.3f}')
print(f'L=256: D_b={Db_mean[-1]:.3f}±{Db_std[-1]:.3f}, n_red={n_red[-1]}')
