# -*- coding: utf-8 -*-
"""S256 d_H 内生攻坚：δ 精化扫描
目标：δ_α = 16259/6000 − ln15 = 0.00178313197
一阶响应：δ = ln15·(ε₁+14ε₂)/29（Paper XXX 定理 3——机器证明的导数结构）
任务：找 ε₁、ε₂ 的框架量组合使 δ 精确命中 δ_α
线索：_phase102 有 ε₁ = −1/150（框架量——静默²×幂基×活跃 = 150）
     比例 ε₁/ε₂ ≈ 10/9 = (幂基×静默)/活跃²
"""
import math
from itertools import product

ln15 = math.log(15)
dH_target = 16259/6000
delta_target = dH_target - ln15
print("=== S256: δ 精化扫描 ===")
print(f"ln15 = {ln15:.10f}")
print(f"d_H 目标 = 16259/6000 = {dH_target:.10f}")
print(f"δ_α 目标 = {delta_target:.10f}")
print(f"δ/ln15 = {delta_target/ln15:.10f}（需 (ε₁+14ε₂)/29 = 此值）")

# 框架量候选池（ε 是小量——σ 幂/框架常数倒数）
sigma = 1/15
pool = []
pool.append(("σ", sigma))
pool.append(("σ²", sigma**2))
pool.append(("σ³", sigma**3))
pool.append(("σ⁴", sigma**4))
pool.append(("σ⁵", sigma**5))
pool.append(("2σ³", 2*sigma**3))
pool.append(("4σ³", 4*sigma**3))
pool.append(("6σ³", 6*sigma**3))
pool.append(("σ²/3", sigma**2/3))
pool.append(("σ³/3", sigma**3/3))
pool.append(("σ³×3", 3*sigma**3))
pool.append(("1/150", 1/150))
pool.append(("-1/150", -1/150))
pool.append(("1/225", 1/225))
pool.append(("1/300", 1/300))
pool.append(("1/450", 1/450))
pool.append(("1/600", 1/600))
pool.append(("1/675", 1/675))
pool.append(("1/10125", 1/10125))
pool.append(("1/50625", 1/50625))
pool.append(("1/(150×9)", 1/1350))
pool.append(("1/(225×2)", 1/450))
pool.append(("e^-6", math.exp(-6)))
pool.append(("e^-6/2", math.exp(-6)/2))
pool.append(("e^-6×3", 3*math.exp(-6)))
pool.append(("e^-7", math.exp(-7)))
pool.append(("ln(16/15)", math.log(16/15)))
pool.append(("ln(16/15)/36", math.log(16/15)/36))
pool.append(("σ·ln2/30", sigma*math.log(2)/30))
pool.append(("0", 0))

target = delta_target/ln15  # 需 (ε₁+14ε₂)/29
need = target*29  # ε₁+14ε₂ 必须 = need

print(f"\n目标 ε₁+14ε₂ = {need:.10f}")
print("\n=== 双元扫描（ε₁、ε₂ 各取候选——最优 10） ===")
res = []
for (n1, e1), (n2, e2) in product(pool, repeat=2):
    v = e1 + 14*e2
    res.append((abs(v - need), v, f"ε₁={n1}, ε₂={n2}"))
res.sort()
for d, v, s in res[:10]:
    d_delta = abs(v/29 - target)*ln15  # δ 层面偏差
    sigma_alpha = abs(v/29 - target)*ln15*24/2.1e-8  # α⁻¹ 层面 σ
    print(f"  {s} → ε₁+14ε₂ = {v:.10f}  δ偏差 {d_delta:.2e}  α⁻¹σ={sigma_alpha:.1f}")

print("\n=== 单参数精化（ε₂ 自由——纯二级） ===")
e2_needed = need/14
print(f"纯二级 ε₂ = {e2_needed:.10f}")
print(f"  框架量候选：1/750 = {1/750:.10f}（差 {(e2_needed-1/750)*14*29/ln15*ln15:.2e}）")
print(f"  1/560 = {1/560:.10f}（差 {(e2_needed-1/560):.2e}）")
print(f"  1/600 = {1/600:.10f}（差 {(e2_needed-1/600):.2e}）")
print(f"  1/540 = {1/540:.10f}（差 {(e2_needed-1/540):.2e}）")

print("\n=== 结论 ===")
print("看是否存在框架量组合精确命中 δ_α——若 α⁻¹σ ≤ 1 则达标")
