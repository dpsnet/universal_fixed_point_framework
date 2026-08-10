#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""综合交叉标度图：D_b(red) 和 D_b(backbone) 随 L 变化。

数据：
  红键: L∈{16, 64} (已有仿真)
  骨架: L∈{16, 32, 48, 64, 96, 128} (paper43_cross_scaling_bb.py)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# 渗流常数
NU = 0.876
D_RED_INF = 1.0 / NU
D_F = 1.87
D_PLATEAU = 0.756

# 已有红键数据
red_data = {
    16: {2.2: 0.756, 2.4: 0.756, 2.6: 0.756, 2.8: 0.756, 3.0: 0.756, 3.2: 0.756},
    64: {2.2: 0.865, 2.4: 0.740, 2.6: 0.903, 2.8: 0.856, 3.0: 0.701, 3.2: 0.872},
}

# 已有骨架数据 (paper43_cross_scaling_bb.py)
bb_data = {
    16: {2.4: 1.767, 3.0: 1.767},
    32: {2.4: 2.366, 3.0: 2.366},
    48: {2.4: 2.137, 3.0: 2.137},
    64: {2.4: 1.994, 3.0: 1.994},
    96: {2.4: 1.830, 3.0: 1.830},
    128: {2.4: 1.978, 3.0: 1.978},
}

def cross_function(x, nu=NU):
    y = x ** (2.0 / nu)
    return y / (1.0 + y)

# ============ 综合图：3 行 × 2 列 ============
fig, axes = plt.subplots(3, 2, figsize=(12, 14))

# --- 行1: 红键 D_b(red) vs L (6个D值) ---
D_values_red = [2.2, 2.4, 2.6, 2.8, 3.0, 3.2]
colors = plt.cm.viridis(np.linspace(0, 1, len(D_values_red)))

ax_red = axes[0, 0]
for i, D in enumerate(D_values_red):
    L_data = []
    Db_data = []
    for L in sorted(red_data.keys()):
        if D in red_data[L]:
            L_data.append(L)
            Db_data.append(red_data[L][D])
    ax_red.plot(L_data, Db_data, 'o-', color=colors[i], markersize=6, 
                label=f'D={D:.1f}', linewidth=1.5)

# 交叉标度拟合：D=3.0
D_frac_fit = 0.631
if 64 in red_data and 3.0 in red_data[64]:
    Db_64 = red_data[64][3.0]
    ratio_64 = (Db_64 - D_PLATEAU) / (D_frac_fit - D_PLATEAU)
    ratio_64 = np.clip(ratio_64, 0.001, 0.999)
    y_64 = ratio_64 / (1 - ratio_64)
    x_64 = y_64 ** (NU / 2.0)
    xi_c_fit = 64 / x_64 if x_64 > 0 else 100
    
    L_fit = np.logspace(np.log10(10), np.log10(300), 100)
    Db_fit = [D_PLATEAU + (D_frac_fit - D_PLATEAU) * cross_function(L_f / xi_c_fit) 
              for L_f in L_fit]
    ax_red.plot(L_fit, Db_fit, 'k--', alpha=0.5, linewidth=2, 
                label=f'Cross-fit ($\\xi_c$={xi_c_fit:.0f})')

ax_red.axhline(y=0.631, color='green', linestyle=':', alpha=0.5, label='P3: ln2/ln3')
ax_red.axhline(y=D_PLATEAU, color='gray', linestyle=':', alpha=0.5, label=f'$D_{{plateau}}$={D_PLATEAU}')
ax_red.set_xscale('log')
ax_red.set_xlabel('L (grid size)')
ax_red.set_ylabel(r'$D_b$(red)')
ax_red.set_title(r'$D_b$(red) vs $L$ — Cross-Scaling')
ax_red.legend(fontsize=7, ncol=2)
ax_red.grid(True, alpha=0.3)

# --- 行2: 骨架 D_b(backbone) vs L ---
ax_bb = axes[1, 0]
for D in [2.4, 3.0]:
    L_data = []
    Db_data = []
    for L in sorted(bb_data.keys()):
        if D in bb_data[L]:
            L_data.append(L)
            Db_data.append(bb_data[L][D])
    ax_bb.plot(L_data, Db_data, 's-', markersize=8, linewidth=2, 
               label=f'D={D:.1f}', color='steelblue')

ax_bb.axhline(y=D_F, color='red', linestyle='--', alpha=0.7, label=r'$D_f \approx 1.87$')
ax_bb.set_xscale('log')
ax_bb.set_xlabel('L (grid size)')
ax_bb.set_ylabel(r'$D_b$(backbone)')
ax_bb.set_title(r'$D_b$(backbone) vs $L$ — Topological Invariant')
ax_bb.legend()
ax_bb.grid(True, alpha=0.3)

# --- 行3: bb_fraction vs L ---
ax_frac = axes[2, 0]
L_list = sorted(bb_data.keys())
frac_list = [0.73] * len(L_list)  # 所有 L 的 bb_fraction 均为 0.73
ax_frac.plot(L_list, frac_list, 'D-', color='darkorange', markersize=8, linewidth=2)
ax_frac.set_xscale('log')
ax_frac.set_ylim(0.6, 0.9)
ax_frac.set_xlabel('L (grid size)')
ax_frac.set_ylabel('Backbone fraction')
ax_frac.set_title('Backbone Fraction = Const (0.73) — Topological Invariant')
ax_frac.grid(True, alpha=0.3)

# --- 右列：理论示意图 ---
# 行1: 交叉标度公式示意
ax_schematic = axes[0, 1]
L_schematic = np.logspace(np.log10(5), np.log10(300), 200)
for D_val, D_frac_val, color in [(3.0, 0.631, 'red'), (2.4, 0.700, 'blue'), (2.8, 0.680, 'green')]:
    xi_c = 100
    Db_sch = [D_PLATEAU + (D_frac_val - D_PLATEAU) * cross_function(L / xi_c) 
              for L in L_schematic]
    ax_schematic.plot(L_schematic, Db_sch, '-', color=color, linewidth=2, 
                      label=f'D={D_val} ($D_{{fractal}}$={D_frac_val:.3f})')
ax_schematic.axhline(y=D_PLATEAU, color='gray', linestyle=':', alpha=0.5)
ax_schematic.axhline(y=0.631, color='green', linestyle=':', alpha=0.5)
ax_schematic.axvline(x=100, color='purple', linestyle=':', alpha=0.5, label=r'$\xi_c=100$')
ax_schematic.set_xscale('log')
ax_schematic.set_xlabel('L (grid size)')
ax_schematic.set_ylabel(r'$D_b$')
ax_schematic.set_title('Cross-Scaling Model: ' + r'$D_b = D_{plateau} + [D_{fractal} - D_{plateau}] \cdot \Phi(L/\xi_c)$')
ax_schematic.legend(fontsize=7)
ax_schematic.grid(True, alpha=0.3)

# 行2: 红键 vs 骨架对比
ax_compare = axes[1, 1]
# 红键数据 (D=3.0)
if 16 in red_data and 3.0 in red_data[16]:
    ax_compare.plot(16, red_data[16][3.0], 'ro', markersize=10, label=r'$D_b$(red) L=16')
if 64 in red_data and 3.0 in red_data[64]:
    ax_compare.plot(64, red_data[64][3.0], 'ro', markersize=10)
# 骨架数据 (D=3.0)
for L in sorted(bb_data.keys()):
    if 3.0 in bb_data[L]:
        ax_compare.plot(L, bb_data[L][3.0], 'bs', markersize=8, label=r'$D_b$(backbone)' if L == 16 else '')
ax_compare.axhline(y=D_PLATEAU, color='red', linestyle=':', alpha=0.5, label=r'$D_{plateau}$')
ax_compare.axhline(y=D_F, color='blue', linestyle=':', alpha=0.5, label=r'$D_f$')
ax_compare.set_xscale('log')
ax_compare.set_xlabel('L (grid size)')
ax_compare.set_ylabel(r'$D_b$')
ax_compare.set_title(r'$D_b$(red) vs $D_b$(backbone) — D=3.0')
ax_compare.legend(fontsize=7)
ax_compare.grid(True, alpha=0.3)

# 行3: D_fractal(D) 理论曲线
ax_fracD = axes[2, 1]
D_range = np.linspace(2.2, 3.2, 50)
R_MAX = 100.0
DELTA_RC = 10.0
Pc_approx = {2.2: 0.041, 2.4: 0.035, 2.6: 0.031, 2.8: 0.028, 3.0: 0.025, 3.2: 0.023}

eta_vals = []
D_frac_vals = []
for D in D_range:
    # 插值 P_c
    D_lo = max([k for k in Pc_approx.keys() if k <= D])
    D_hi = min([k for k in Pc_approx.keys() if k >= D])
    if D_lo == D_hi:
        Pc = Pc_approx[D]
    else:
        t = (D - D_lo) / (D_hi - D_lo)
        Pc = Pc_approx[D_lo] * (1-t) + Pc_approx[D_hi] * t
    rc = 1.0 / Pc
    eta = (D - 2) * (rc / R_MAX) ** (D - 3) * DELTA_RC / R_MAX
    eta_vals.append(eta)
    D_frac = D_RED_INF * eta ** (D_F - 1)
    D_frac_vals.append(D_frac)

ax_fracD.plot(D_range, D_frac_vals, 'b-', linewidth=2, label=r'$D_{fractal}(D) = D_{red}^{\infty} \cdot \eta(D)^{D_f-1}$')
ax_fracD.axhline(y=0.631, color='green', linestyle=':', alpha=0.5, label='P3: ln2/ln3')
ax_fracD.set_xlabel('D (fractal dimension)')
ax_fracD.set_ylabel(r'$D_{fractal}$')
ax_fracD.set_title(r'$D_{fractal}(D)$ — Theory vs P3 Prediction')
ax_fracD.legend()
ax_fracD.grid(True, alpha=0.3)

fig.suptitle('Cross-Scaling Analysis: $D_b$(red) vs $D_b$(backbone)\n'
             'Red bonds: finite-size cross-over from plateau (0.756) to fractal limit\n'
             'Backbone: topological invariant, independent of D',
             fontsize=13, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.92])

save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', '05_condensed_matter', 'figures')
fig.savefig(os.path.join(save_dir, 'paper43_cross_scaling_comprehensive.png'), dpi=150)
plt.close(fig)
print(f"综合图已保存: {save_dir}/paper43_cross_scaling_comprehensive.png")
