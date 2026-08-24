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
# 本文件中 UFPF 相关引用数量：2
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

# -*- coding: utf-8 -*-
"""谱交织旋转检验：可行性分析（笔记 §7.2/§7.5 的数值化，非新预言）
差异信号：Δτ(φ)/τ ∝ (θ_g² − θ_i²)·sin²φ
  - 等效原理（谱交织存在）下 θ_i = θ_g → 无差异
  - 若 m_i ≠ m_g（η ≠ 0）：Δτ(φ)/τ ≈ η·θ²·sin²φ
用 Eötvös 参数 η 参数化，对比光钟精度，给出可探测性下限。
诚实边界：框架无 UFPF 独有预测值；本脚本为等效原理检验的精度需求分析。
"""
import os
import numpy as np

c = 299792458.0          # m/s
G = 6.674e-11            # m^3 kg^-1 s^-2
M_earth = 5.972e24
R_earth = 6.371e6
M_sun = 1.989e30
R_sun = 6.957e8

G_clock = 1e-18          # 光钟相对精度

def v_esc(M, r):
    return np.sqrt(2.0 * G * M / r)

def theta_esc_deg(M, r):
    v = v_esc(M, r)
    return np.degrees(np.arcsin(v / c)), v / c

print("=" * 70)
print("谱交织旋转检验可行性分析（等效原理检验的精度需求）")
print("=" * 70)

# 1) 各引力场的逃逸速度角 θ_esc
sites = [
    ("地球表面", M_earth, R_earth),
    ("GPS 轨道(~2e7 m)", M_earth, 2.02e7),
    ("太阳表面", M_sun, R_sun),
]
print("\n[1] 特征偏转角（引力侧 θ_g ≈ θ_esc）")
rows = []
for name, M, r in sites:
    th_deg, beta = theta_esc_deg(M, r)
    th_rad = np.radians(th_deg)
    rows.append((name, beta, th_deg, th_rad))
    print(f"  {name:20s} v_esc/c={beta:.3e}  θ_esc={th_deg:.5f}° = {th_rad:.3e} rad")

# 2) 可探测 η 下限（光钟精度 1e-18，φ=90° 最大信号）
print("\n[2] 光钟精度 1e-18 下可探测的 Eötvös 参数下限 η_min ≈ 1e-18/θ²")
for name, beta, th_deg, th_rad in rows:
    eta_min = G_clock / (th_rad ** 2)
    print(f"  {name:20s} η_min = {eta_min:.2e}")

# 3) 信号幅度（固定 η = 1e-13 示例，地球表面）
eta_ex = 1e-13
_, _, _, th_earth = rows[0]
sig = eta_ex * th_earth ** 2
print(f"\n[3] 示例信号（η = 1e-13，地球表面，φ=90°）：Δτ/τ ≈ {sig:.2e}")
print(f"      vs 光钟精度 1e-18：{'可探测' if sig > G_clock else '低于精度'}")

# 4) sin²φ 曲线形状（φ 扫描）
print("\n[4] 信号形状 Δτ/τ ∝ sin²φ（旋转角依赖签名）")
phis = np.array([0, 30, 45, 60, 90])
for p in phis:
    print(f"  φ={p:3d}°  sin²φ={np.sin(np.radians(p))**2:.3f}")

print("\n结论（诚实）：")
print("  - 框架无 UFPF 独有预测值：等效原理下 θ_i=θ_g，信号恒为零（谱交织存在 = 标准预言）")
print("  - 若等效原理被违反（η≠0），信号形式 sin²φ 由正交叠加几何导出（建模假设）")
print("  - 光钟(1e-18)可把 Eötvös η 探测推至 ~1e-10(地球)~1e-13(太阳)，补充/优于 MICROSCOPE(1e-15)")
print("  - 该检验为公共判据：测到差异=同时违反等效原理与谱交织；测不到=两者相容（不区分）")
