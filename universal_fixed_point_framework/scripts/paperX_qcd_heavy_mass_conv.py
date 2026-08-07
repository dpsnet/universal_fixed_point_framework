#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_qcd_heavy_mass_conv.py — 重味 pole 质量修正的收敛性可视化（61B）
============================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §8.2 重味 dressing 标度依赖分析
（推论 5.11 配套图：m_c/m_b 有效质量随 α_s 的 pole-MS 修正曲线，展示圈阶收敛性）。

物理：重味有效质量 m_Q,eff = m_Q,MS·(1 + δ_Q(α_s))，其中 pole-MS 圈阶修正
  δ_Q(α_s) = (4/3)(α_s/π)                                   （单圈）
  δ_Q(α_s) = (4/3)(α_s/π) + C₂(α_s/π)²                     （两圈，C₂ = 13.44）
收敛性判据：两圈修正 ≈ 单圈修正 → 不收敛（取单圈）；两圈 << 单圈 → 收敛（取两圈）。
谱定点：α_s(m_c) = 0.413（charm，不收敛 → 单圈）、α_s(m_b) = 0.224（bottom，收敛 → 两圈）。

输出：paperX_qcd_heavy_mass_conv.png（双面板：m_c_eff(α_s) 与 m_b_eff(α_s) 单圈/两圈曲线 +
谱定点与经验水平线标注）。
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Windows 中文字体（SimHei / Microsoft YaHei），避免 CJK glyph 缺失
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

M_C_MS, M_B_MS = 1.27, 4.18            # GeV，MS-bar 裸质量
C2 = 13.44                             # 两圈 pole-MS 系数
A_MC = 0.413                           # 谱定 α_s(m_c)（两圈跨味，推论 5.10）
A_MB = 0.224                           # 谱定 α_s(m_b)
M_C_EMP, M_B_EMP = 1.5, 4.8            # Cornell 经验有效质量
PNG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'figs', 'paperX_qcd_heavy_mass_conv.png')

def m_c_1loop(a):
    return M_C_MS * (1.0 + (4.0 / 3.0) * (a / math.pi))

def m_c_2loop(a):
    return M_C_MS * (1.0 + (4.0 / 3.0) * (a / math.pi) + C2 * (a / math.pi)**2)

def m_b_1loop(a):
    return M_B_MS * (1.0 + (4.0 / 3.0) * (a / math.pi))

def m_b_2loop(a):
    return M_B_MS * (1.0 + (4.0 / 3.0) * (a / math.pi) + C2 * (a / math.pi)**2)

checks = []

def check(name, cond, detail=""):
    checks.append((name, cond, detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

print("=" * 72)
print("61B 重味 pole 质量修正收敛性可视化：m_c/m_b 随 α_s 变化曲线")
print("=" * 72)

# === 数值检查 ===
m_c_sp = m_c_1loop(A_MC)      # 谱定 charm（单圈）
m_b_sp = m_b_2loop(A_MB)      # 谱定 bottom（两圈）
corr_c1 = (4.0 / 3.0) * (A_MC / math.pi)
corr_c2 = C2 * (A_MC / math.pi)**2
corr_b1 = (4.0 / 3.0) * (A_MB / math.pi)
corr_b2 = C2 * (A_MB / math.pi)**2

print(f"\nN1/N2. 谱定点复核：m_c_eff(0.413) = {m_c_sp:.3f} GeV、m_b_eff(0.224) = {m_b_sp:.3f} GeV")
check("N1 charm 谱定点 m_c_eff = 1.492 GeV（单圈 pole）",
      abs(m_c_sp - 1.492) < 0.005, f"(m_c_eff = {m_c_sp:.3f})")
check("N2 bottom 谱定点 m_b_eff = 4.861 GeV（两圈 pole）",
      abs(m_b_sp - 4.861) < 0.005, f"(m_b_eff = {m_b_sp:.3f})")

print(f"\nN3/N4. 圈阶收敛性（两圈/单圈修正比）：")
print(f"  charm：两圈 {corr_c2:.3f} vs 单圈 {corr_c1:.3f}（比值 {corr_c2/corr_c1:.2f} → 不收敛 → 单圈）")
print(f"  bottom：两圈 {corr_b2:.3f} vs 单圈 {corr_b1:.3f}（比值 {corr_b2/corr_b1:.2f} → 收敛 → 两圈）")
check("N3 charm 两圈修正 ≈ 单圈（比值 > 0.8，不收敛 → 单圈截断）",
      corr_c2 / corr_c1 > 0.8, f"(比值 {corr_c2/corr_c1:.2f})")
check("N4 bottom 两圈修正 << 单圈（比值 < 0.8，收敛 → 两圈）",
      corr_b2 / corr_b1 < 0.8, f"(比值 {corr_b2/corr_b1:.2f})")

d_c = (m_c_sp - M_C_MS) * 1000.0
d_b = (m_b_sp - M_B_MS) * 1000.0
print(f"\nN5. 重味 dressing 标度依赖：charm Δ_c = {d_c:.0f} MeV、bottom Δ_b = {d_b:.0f} MeV")
print(f"    bottom/charm dressing 比 = {d_b/d_c:.2f}（m_MS 比 = {M_B_MS/M_C_MS:.2f}，近线性标度依赖）")
check("N5 重味 dressing 随质量标度增大（Δ_b > Δ_c，近线性）",
      d_b > d_c and abs((d_b/d_c) / (M_B_MS/M_C_MS) - 1.0) < 0.3,
      f"(Δ_b/Δ_c = {d_b/d_c:.2f}, m_MS 比 = {M_B_MS/M_C_MS:.2f})")

# === 可视化 ===
alpha_c = np.linspace(0.15, 0.55, 300)
alpha_b = np.linspace(0.10, 0.40, 300)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 面板 1：charm
ax1.plot(alpha_c, [m_c_1loop(a) for a in alpha_c], 'b-', lw=2, label=r'$m_{c,\mathrm{eff}}$ 单圈')
ax1.plot(alpha_c, [m_c_2loop(a) for a in alpha_c], 'r--', lw=2, label=r'$m_{c,\mathrm{eff}}$ 两圈')
ax1.fill_between(alpha_c, [m_c_1loop(a) for a in alpha_c], [m_c_2loop(a) for a in alpha_c],
                 color='r', alpha=0.15, label='圈阶差距（不收敛区）')
ax1.axvline(A_MC, color='k', ls=':', lw=1.5, label=r'$\alpha_s(m_c) = 0.413$')
ax1.axhline(M_C_EMP, color='g', ls='--', lw=1.5, label=r'经验 $m_c = 1.5$ GeV')
ax1.plot(A_MC, m_c_sp, 'ko', ms=8, zorder=5)
ax1.annotate(r'谱定点 (0.413, 1.492)' , xy=(A_MC, m_c_sp), xytext=(0.30, 1.62),
             arrowprops=dict(arrowstyle='->', color='k'), fontsize=10)
ax1.set_xlabel(r'$\alpha_s$')
ax1.set_ylabel(r'$m_{c,\mathrm{eff}}$ (GeV)')
ax1.set_title(r'charm：两圈修正 $\approx$ 单圈（不收敛 $\to$ 单圈）', fontsize=10)
ax1.legend(fontsize=8, loc='upper left')
ax1.grid(alpha=0.3)

# 面板 2：bottom
ax2.plot(alpha_b, [m_b_1loop(a) for a in alpha_b], 'b-', lw=2, label=r'$m_{b,\mathrm{eff}}$ 单圈')
ax2.plot(alpha_b, [m_b_2loop(a) for a in alpha_b], 'r--', lw=2, label=r'$m_{b,\mathrm{eff}}$ 两圈')
ax2.fill_between(alpha_b, [m_b_1loop(a) for a in alpha_b], [m_b_2loop(a) for a in alpha_b],
                 color='r', alpha=0.15, label='圈阶差距（收敛区）')
ax2.axvline(A_MB, color='k', ls=':', lw=1.5, label=r'$\alpha_s(m_b) = 0.224$')
ax2.axhline(M_B_EMP, color='g', ls='--', lw=1.5, label=r'经验 $m_b = 4.8$ GeV')
ax2.plot(A_MB, m_b_sp, 'ko', ms=8, zorder=5)
ax2.annotate(r'谱定点 (0.224, 4.861)', xy=(A_MB, m_b_sp), xytext=(0.20, 5.05),
             arrowprops=dict(arrowstyle='->', color='k'), fontsize=10)
ax2.set_xlabel(r'$\alpha_s$')
ax2.set_ylabel(r'$m_{b,\mathrm{eff}}$ (GeV)')
ax2.set_title(r'bottom：两圈修正 $\ll$ 单圈（收敛 $\to$ 两圈）', fontsize=10)
ax2.legend(fontsize=8, loc='upper left')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(PNG, dpi=150, bbox_inches='tight')
plt.close()
print(f"\nN6. 图已保存：{PNG}")
check("N6 收敛性图生成成功（paperX_qcd_heavy_mass_conv.png）",
      os.path.exists(PNG), f"(文件大小 {os.path.getsize(PNG) if os.path.exists(PNG) else 0} 字节)")

# === 汇总 ===
print("\n" + "=" * 72)
n_pass = sum(1 for _, c, _ in checks if c)
print(f"汇总: {n_pass}/{len(checks)} 检查通过")
if n_pass != len(checks):
    raise SystemExit(f"FAIL: {len(checks)-n_pass} 项未通过")

print("\n关键数值（笔记引用）：")
print(f"  谱定点：m_c_eff = {m_c_sp:.3f} GeV（单圈）、m_b_eff = {m_b_sp:.3f} GeV（两圈）")
print(f"  收敛性：charm 两圈/单圈 = {corr_c2/corr_c1:.2f}（不收敛）、bottom = {corr_b2/corr_b1:.2f}（收敛）")
print(f"  dressing：Δ_c = {d_c:.0f} MeV、Δ_b = {d_b:.0f} MeV（Δ_b/Δ_c = {d_b/d_c:.2f} ≈ m_MS 比 {M_B_MS/M_C_MS:.2f}）")
