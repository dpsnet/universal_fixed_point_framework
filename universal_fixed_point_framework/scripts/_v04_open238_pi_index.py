# -*- coding: utf-8 -*-
# _v04_open238_pi_index.py — 104az-238: π 分量二次位移精确指数核算 (从 235 精确对角化函数)
# 目的: 验证 236 预注册判据① "π 指数 ∈ [1.9,2.1]" 在 100-200 MG 窗口的成立性
# 方法: 复用 235 的 hamiltonian/zee_freqs, 提取 Δm=0 (π, 一阶=0) 分量, 多 B 点拟合指数
import sys
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from _v04_open235_zeeman_benchmark import zee_freqs, unique_sorted
import numpy as np

print("=== 104az-238: π 二次位移精确指数核算 ===")
print("(基于 235 精确对角化: H0 + (γ/2)(Lz+2Sz) + γ²/8·ρ², n=1..4)")
print()
print(f"{'B(MG)':>7} {'γ':>10} {'π 完整位移(cm⁻¹)':>20} {'波长位移(Å)':>12}")
pts = []
for B in (20, 50, 100, 150, 200, 250, 300):
    f1 = unique_sorted(zee_freqs(B, with_diamag=False))
    f2 = unique_sorted(zee_freqs(B, with_diamag=True))
    gamma = B * 1e6 / 2.3505e9
    # π 分量 = 一阶为 0 的位移 (完整位移本身即二次效应)
    # 找出 f1 中 ~0 的 (一阶=0), 对应 f2 同位置
    pi_disp = None
    for x in f1:
        if abs(x) < 1.0:   # 一阶≈0 的分量 (π)
            # 找 f2 中最近
            j = min(range(len(f2)), key=lambda j_: abs(f2[j_] - x))
            pi_disp = f2[j]
            break
    if pi_disp is None:
        print(f"{B:>7} {gamma:>10.5f}  (无 π 分量检出)")
        continue
    dlam = pi_disp / 15233.0 * 6562.79
    pts.append((B, pi_disp, dlam))
    print(f"{B:>7} {gamma:>10.5f} {pi_disp:>20.3f} {dlam:>12.2f}")

print()
print("--- 指数拟合 (ln Δν vs ln B, 各窗口) ---")
def exponent(i, j):
    B1, d1, _ = pts[i]; B2, d2, _ = pts[j]
    return np.log(d2 / d1) / np.log(B2 / B1)
windows = [("100→200 MG", 2, 4), ("50→200 MG", 1, 4), ("20→200 MG", 0, 4), ("100→300 MG", 2, 6)]
for name, i, j in windows:
    if j < len(pts):
        print(f"  {name}: 指数 = {exponent(i, j):.3f}")

print()
print("--- 判据① 核验: [1.9, 2.1] ---")
e_100_200 = exponent(2, 4)
print(f"  100→200 MG 窗口指数 {e_100_200:.3f} -> {'✓ 达标' if 1.9 <= e_100_200 <= 2.1 else '✗ 不达标'}")
print()
print("--- R 需求重构 (测 π 二次位移, 定位精度 1/10) ---")
for B, d, dlam in pts:
    if B in (100, 150, 200, 220.78):
        print(f"  {B} MG: π 位移 {dlam:.1f} Å -> 定位 δ={dlam/10:.1f} Å -> R ≥ {6562.79/(dlam/10):.0f}")
