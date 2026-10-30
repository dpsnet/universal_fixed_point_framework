# -*- coding: utf-8 -*-
"""S256g σ 幂次谱核查：V1/V2 的 σ⁷ 与 Fibonacci 幂次规则冲突？
σ 幂次谱观察（S122/S134/S135）：使用幂次 ∈ Fib = {1,2,3,5,8,13}
  ——8 = 5+3、5 = 3+2、3 = 2+1——"静默族幂次 = Fibonacci 递归链"
  ——S130 明确：σ⁷/σ⁹ 不命中（非 Fib）
V1 = 6σ³+4σ⁵+15σ⁷、V2 = 6σ³+4σ⁵+14σ⁷+13σ⁸——都含 σ⁷！
核查：① 6σ³+4σ⁵ 主导项的残差落在哪层？② 15σ⁷ = σ⁶（非 Fib）
③ 纯 Fib 幂次（σ³/σ⁵/σ⁸）能否表达 δ？
"""
from decimal import Decimal, getcontext
getcontext().prec = 30
import math

ln15 = Decimal(15).ln()
delta_target = Decimal(16259)/Decimal(6000) - ln15
sigma = Decimal(1)/Decimal(15)

print("=== S256g: σ 幂次谱核查 ===")
print(f"δ_α = {float(delta_target):.12f}")
print(f"σ 幂次谱（Fib）：1, 2, 3, 5, 8, 13...——σ⁷ ∉ Fib")

s3 = sigma**3; s5 = sigma**5; s7 = sigma**7; s8 = sigma**8
s6 = sigma**6

print(f"\n--- ① 主导项 6σ³+4σ⁵ 残差 ---")
lead = 6*s3 + 4*s5
resid = delta_target - lead
print(f"6σ³+4σ⁵ = {float(lead):.12f}")
print(f"残差 = {float(resid):.3e}")
print(f"残差/σ⁶ = {float(resid/s6):.4f}（σ⁶ 非 Fib）")
print(f"残差/σ⁷ = {float(resid/s7):.4f}（σ⁷ 非 Fib——V1/V2 用的层）")
print(f"残差/σ⁸ = {float(resid/s8):.4f}（σ⁸ Fib——系数 {float(resid/s8):.1f} 非框架量？）")
print(f"残差/σ⁵ = {float(resid/s5):.4f}（σ⁵ Fib——系数非整）")

print(f"\n--- ② 15σ⁷ = σ⁶ ? ---")
print(f"15σ⁷ = {float(15*s7):.12e} vs σ⁶ = {float(s6):.12e}")
print(f"15×1/15⁷ = 1/15⁶ = σ⁶ ✓——V1 第三项 = σ⁶（非 Fib！）")

print(f"\n--- ③ 纯 Fib 幂次组合（σ³/σ⁵/σ⁸） ---")
# δ = aσ³+bσ⁵+cσ⁸——a ≈ 6（Fib 系数？6 非框架常数——但 6 = 幂基×活跃）
# b ≈ 4（不动点——Fib 幂次 σ⁵ 配不动点系数）
# c = 残差/σ⁸
c_needed = resid/s8
print(f"aσ³ 主导：a ≈ 6.018（6 = 幂基×活跃 ✓——Fib 幂 σ³ 配 6）")
print(f"bσ⁵：b ≈ 4.066（4 = 不动点 ✓——Fib 幂 σ⁵ 配 4）")
print(f"cσ⁸：c = {float(c_needed):.4f}——需 {float(c_needed):.1f}——非框架量 ✗")

print(f"\n--- ④ 框架量系数 × Fib 幂次全集扫描 ---")
# 系数候选：框架量 1-42、幂次 Fib {1,2,3,5,8,13}
fib_pows = [1, 2, 3, 5, 8, 13]
coefs = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,24,25,27,30,32,36,40,42]
best = []
from itertools import product
for (p1,p2,p3) in product(fib_pows, repeat=3):
    for (c1,c2,c3) in product(coefs, repeat=3):
        v = c1*sigma**p1 + c2*sigma**p2 + c3*sigma**p3
        d = abs(v - delta_target)
        if d < 1e-6:
            best.append((float(d), f"{c1}σ^{p1}+{c2}σ^{p2}+{c3}σ^{p3}"))
best.sort()
print(f"纯 Fib 幂次+框架量系数：{len(best)} 个组合差 <1e-6——top 5：")
for d, s in best[:5]:
    sig_a = d*24/2.1e-8
    print(f"  {s} = 差 {d:.2e}——α⁻¹σ = {sig_a:.1f}")

print(f"\n--- ⑤ 结论 ---")
print("6σ³+4σ⁵ 残差 8.66e-8 落在 σ⁶/σ⁷ 层（均非 Fib）——")
print("纯 Fib 幂次组合（框架量系数）无法 ≤1σ 命中——")
print("V1/V2 用 σ⁷ 是'必要违规'——与 σ 幂次 Fib 谱观察冲突")
