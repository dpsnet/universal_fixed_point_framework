# -*- coding: utf-8 -*-
"""S256j 正确目标下干净组合精扫
固定 6σ³ 主导（6 = 幂基×活跃——先验最优），三修正项：
- 单量系数 {1,2,3,4,5,7,8,15,16,24,42}
- 双量系数 {6,10,12,14,20,21,28,30,32,35,40,45,48,56,60,64,72,80}
- 幂次 {4,5,6,7,8,9,10}
找 σ ≤ 1 的最干净组合（先单量，再双量）
"""
from decimal import Decimal, getcontext
getcontext().prec = 50
import math

alpha_obs = Decimal("137.035999084")
unc = Decimal("2.1e-8")
ln15 = Decimal(15).ln()
sigma = Decimal(1)/Decimal(15)
delta_obs = alpha_obs/24 - 3 - ln15

s_pow = {p: sigma**p for p in range(1, 13)}

coefs_single = [1,2,3,4,5,7,8,15,16,24,42]
coefs_double = [6,10,12,14,20,21,28,30,32,35,40,45,48,56,60,64,72,80]

def alpha_sig(delta_pred):
    alpha_pred = 24*(ln15 + delta_pred + 3)
    return abs(alpha_pred - alpha_obs)/unc

results = []
# 固定 6σ³
base = 6*s_pow[3]
from itertools import product as iprod
for (p1, p2, p3) in iprod(range(4, 11), repeat=3):
    for cs in [coefs_single, coefs_double]:
        for (c1, c2, c3) in iprod(cs, repeat=3):
            v = base + c1*s_pow[p1] + c2*s_pow[p2] + c3*s_pow[p3]
            d = abs(v - delta_obs)
            sig = float(24*d/unc)
            if sig <= 2.0:
                results.append((sig, f"6σ³+{c1}σ^{p1}+{c2}σ^{p2}+{c3}σ^{p3}", p1, p2, p3, c1, c2, c3))
results.sort()
print("=== S256j: 6σ³ 主导 + 三修正项精扫（σ ≤ 2） ===")
print(f"目标 δ^(obs) = {float(delta_obs):.12f}")
print(f"共 {len(results)} 个组合 σ ≤ 2\n")

print("--- 单量系数组合（σ ≤ 1） ---")
for sig, expr, *_ in [r for r in results if all(c in coefs_single for c in [r[5], r[6], r[7]])][:8]:
    print(f"  {expr}——α⁻¹σ = {sig:.3f}")

print("\n--- 全部组合 top 8 ---")
for sig, expr, *_ in results[:8]:
    print(f"  {expr}——α⁻¹σ = {sig:.3f}")

print("\n--- 框架身份检查（单量 top） ---")
for sig, expr, p1, p2, p3, c1, c2, c3 in [r for r in results if all(c in coefs_single for c in [r[5], r[6], r[7]])][:3]:
    idents = {2:"幂基",3:"活跃",4:"不动点",5:"静默",7:"对合",8:"幂基³",15:"态域",16:"全态",24:"不动点!",42:"约束域"}
    pi = ", ".join(f"σ^{p}={idents.get(p,'?')}" for p in [3, p1, p2, p3])
    ci = ", ".join(str(c) for c in [6, c1, c2, c3])
    print(f"  {expr}：幂次 {pi}——系数 6、{ci}")
