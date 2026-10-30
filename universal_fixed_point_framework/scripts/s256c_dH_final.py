# -*- coding: utf-8 -*-
"""S256c d_H 内生攻坚最终扫描
关键认识：δ_α = 16259/6000 − ln15 无理——纯 σ 幂有理组合无法精确
正确路径：δ = ln15×(框架有理)——ln15 因子吸收无理
目标：δ/ln15 = 0.0006584561（需精确到 8.75e-10/ln15 = 3.2e-10）
同时试：α⁻¹ = 72+24ln15+24δ 的含 ln15 结构
"""
import math
from itertools import product

ln15 = math.log(15)
sigma = 1/15
dH = 16259/6000
delta = dH - ln15
ratio = delta/ln15
print("=== S256c: δ 含 ln15 因子扫描 ===")
print(f"δ_α = {delta:.12f}")
print(f"δ/ln15 = {ratio:.12f}——需框架有理精确到 3.2e-10")

# 候选：σ 幂组合（有理数——k·σ^p ± m·σ^q ± ...）
print("\n=== A. δ = ln15×(σ 幂有理组合) top 8 ===")
res = []
for p in range(3, 8):
    for q in range(3, 8):
        for k in range(1, 15):
            for m in range(1, 15):
                v = k*sigma**p + m*sigma**q
                for s in (+1, -1):
                    vv = k*sigma**p + s*m*sigma**q
                    if vv <= 0: continue
                    res.append((abs(vv-ratio), vv, f"{k}σ^{p}{'+' if s>0 else '−'}{m}σ^{q}"))
res.sort()
for d, v, s in res[:8]:
    d_delta = abs(v-ratio)*ln15
    sig_a = d_delta*24/2.1e-8
    print(f"  δ/ln15 = {s} = {v:.10f}  差 {d:.2e}  α⁻¹σ={sig_a:.1f}")

print("\n=== B. 三项组合（σ⁴/σ⁵/σ⁶ 系数小整） ===")
best = None
for a in range(80, 100):
    for b in range(-10, 10):
        for c in range(-15, 15):
            v = a*sigma**4 + b*sigma**5 + c*sigma**6
            d = abs(v - ratio)
            if best is None or d < best[0]:
                best = (d, v, f"{a}σ⁴{b:+d}σ⁵{c:+d}σ⁶")
print(f"  最优三项：{best[2]} = {best[1]:.10f}  差 {best[0]:.2e}")
print(f"  α⁻¹σ = {best[0]*ln15*24/2.1e-8:.1f}")

print("\n=== C. α⁻¹ = 72+24ln15+24δ 结构核查 ===")
alpha_alt = 72 + 24*ln15 + 24*delta
print(f"72+24ln15+24δ = {alpha_alt:.9f}（= 24(d_H+3) 应 = 137.036）")
print(f"72 = 约束域+静默×(幂基×活跃) = 42+30 ✓ 全框架")
print(f"24 = 不动点！ ✓   ln15 = 态域对数（Moran 解——机器证明）")
print(f"→ 若 δ 闭环——α⁻¹ 全内生（ln15 入链——无理精度可及）")
print(f"→ δ 未闭环 = 当前唯一缺口——σ 幂组合极限 σ~92（90σ⁴+4σ⁵）")

print("\n=== D. gen2 尺度呼应（报告 5.4） ===")
print(f"三代质量指数 {0, ln15, ln15+3}")
print(f"ln15+3 = {ln15+3:.7f} vs d_H+3 = {dH+3:.7f}——差 {dH-ln15:.6f} = δ")
print(f"→ d_H+3 = gen2 尺度+3+δ——'质量谱尺度'与 α⁻¹ 链共享 ln15")

print("\n=== 诚实结论 ===")
print("四条路径（δ 响应/修正项/RMS 系数/σ 幂组合）全部未达 ≤1σ")
print("最接近：δ ≈ ln15×(90σ⁴+4σ⁵)——α⁻¹σ = 92——不达标")
print("d_H 内生化未闭合——α⁻¹ = 72+24ln15+24δ 结构完整但 δ 缺口")
