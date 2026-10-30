# -*- coding: utf-8 -*-
"""I_e/I_μ = 26/9 候选验证（2026-10-25）：间隔比 = 幂基×(k_max+静默)/N_gen²

候选：I_e/I_μ ≈ 26/9——26 = 2×13 = 幂基×(k_max+静默)、9 = N_gen²
实测差 0.0057%（达标 <0.01%）——本脚本做锁定级检查（<0.001%）+ 邻域判别。
"""
import math

N_gen, k_max = 3, 8
e = math.e
ln2, ln15, ln16 = math.log(2), math.log(15), math.log(16)
sigma = 1/15
s3 = sigma**3
alpha_v = 16/15 + math.sqrt(2/N_gen)
I_mu = ln16 + e**(-3)
I_e  = 3*e - s3*(1+alpha_v)
ratio = I_e / I_mu

print("=== 26/9 候选判别 ===")
cand = 26/9
rel = (cand - ratio)/ratio
print(f"I_e/I_μ = {ratio:.10f}")
print(f"26/9    = {cand:.10f}")
print(f"差 = {rel*100:+.4f}%（达标 <0.01%：{abs(rel)<1e-4}；锁定 <0.001%：{abs(rel)<1e-5}）")
print()

print("=== 26 的框架分解 ===")
print(f"26 = 2×13 = 幂基×(k_max+静默) = {2*13}")
print(f"26 = 7²−7−16 = 对合域²−对合域−全态 = {49-7-16}")
print(f"26 = 16+10 = 全态+幂基×静默 = {16+10}")
print(f"26 = 2×(6+7) = 幂基×(N_gen!+对合域) = {2*(6+7)}")
print(f"26 = 3²+17？——17 无框架身份")
print()

print("=== 邻域判别（26/9 是否为最优框架组合） ===")
best = []
for a in range(1, 41):
    for b in range(1, 41):
        v = a/b
        r = (v - ratio)/ratio
        if abs(r) < 5e-4:
            best.append((abs(r), f"{a}/{b}", v))
best.sort()
print("≤0.05% 有理命中：")
for r, name, v in best[:8]:
    print(f"   {name} = {v:.10f}  差 {r*100:+.4f}%")
print()

print("=== 交叉验证：26/9×I_μ vs I_e ===")
print(f"26/9×I_μ = {cand*I_mu:.10f}")
print(f"I_e      = {I_e:.10f}")
print(f"差 = {(cand*I_mu-I_e)/I_e*100:+.4f}%")
print()

print("=== 统一形式候选：I_e ≈ 26/9×I_μ（间隔比生成链） ===")
print("若 I_e = (26/9)·I_μ 成立，则 m_e/m_μ = e^{−(I_e−I_μ)} = e^{−I_μ·17/9}")
print(f"I_μ×17/9 = {I_mu*17/9:.10f}（= I_e−I_μ 候选身份 5.3316？）")
print(f"I_e−I_μ 实际 = {I_e-I_mu:.10f}，差 {(I_mu*17/9-(I_e-I_mu))/(I_e-I_mu)*100:+.4f}%")
print(f"  ——17/9 = (k_max+静默+对合域?)/N_gen²——17 无框架身份——弱")
print()
print("=== 16/3 候选复核 ===")
print(f"16/3 vs I_e−I_μ：差 {(16/3-(I_e-I_mu))/(I_e-I_mu)*100:+.4f}%（0.032% 候选）")
print(f"——16/3 = 2⁴/N_gen = 全态/N_gen")
