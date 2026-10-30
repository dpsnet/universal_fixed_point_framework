# -*- coding: utf-8 -*-
"""S256i 正确目标重定位（高效贪心分层版）
δ^(obs) = α⁻¹(obs)/24 − 3 − ln15——真实无理目标
分层贪心：每层取最优 (系数,幂次) 逼近当前残差
"""
from decimal import Decimal, getcontext
getcontext().prec = 50
import math

alpha_obs = Decimal("137.035999084")
unc = Decimal("2.1e-8")
ln15 = Decimal(15).ln()
sigma = Decimal(1)/Decimal(15)

dH_obs = alpha_obs/24 - 3
delta_obs = dH_obs - ln15
need = unc/24  # δ 层面达标线

print("=== S256i: 正确目标 δ^(obs) ===")
print(f"δ^(obs) = {delta_obs}")
print(f"δ^(obs) 数值 = {float(delta_obs):.12f}")
print(f"达标线 δ 层面 ≤ {float(need):.2e}\n")

# 系数候选（框架量）
coefs = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,24,25,27,30,32,36,40,42,45,48,54,60,64]
powers = list(range(1, 16))

def greed(resid, nterms):
    """贪心：每层选 |c·σ^p − resid| 最小"""
    terms = []
    r = resid
    for _ in range(nterms):
        best = None
        for p in powers:
            for c in coefs:
                d = abs(c*sigma**p - r)
                if best is None or d < best[0]:
                    best = (d, c, p, c*sigma**p)
        if best is None:
            break
        d, c, p, contrib = best
        terms.append((c, p, float(contrib)))
        r = r - contrib
        if abs(r) < Decimal("1e-13"):
            break
    return terms, r

print("--- ① 3 项贪心 ---")
terms, r = greed(delta_obs, 3)
alpha_pred = 24*(ln15 + (delta_obs - r) + 3)
sig = abs(alpha_pred - alpha_obs)/unc
expr = "+".join(f"{c}σ^{p}" for c, p, _ in terms)
print(f"{expr} = {float(delta_obs-r):.12f}")
print(f"  残差 = {float(r):.3e}——α⁻¹σ = {float(sig):.2f}")

print("\n--- ② 4 项贪心 ---")
terms4, r4 = greed(delta_obs, 4)
alpha_pred4 = 24*(ln15 + (delta_obs - r4) + 3)
sig4 = abs(alpha_pred4 - alpha_obs)/unc
expr4 = "+".join(f"{c}σ^{p}" for c, p, _ in terms4)
print(f"{expr4} = {float(delta_obs-r4):.12f}")
print(f"  残差 = {float(r4):.3e}——α⁻¹σ = {float(sig4):.2f}")

print("\n--- ③ 5 项贪心 ---")
terms5, r5 = greed(delta_obs, 5)
alpha_pred5 = 24*(ln15 + (delta_obs - r5) + 3)
sig5 = abs(alpha_pred5 - alpha_obs)/unc
expr5 = "+".join(f"{c}σ^{p}" for c, p, _ in terms5)
print(f"{expr5} = {float(delta_obs-r5):.12f}")
print(f"  残差 = {float(r5):.3e}——α⁻¹σ = {float(sig5):.2f}")

print("\n--- ④ 6 项贪心（看极限） ---")
terms6, r6 = greed(delta_obs, 6)
alpha_pred6 = 24*(ln15 + (delta_obs - r6) + 3)
sig6 = abs(alpha_pred6 - alpha_obs)/unc
expr6 = "+".join(f"{c}σ^{p}" for c, p, _ in terms6)
print(f"{expr6}")
print(f"  残差 = {float(r6):.3e}——α⁻¹σ = {float(sig6):.2f}")

print("\n--- ⑤ 含 ln15 因子的结构（δ/ln15 有理化） ---")
ratio = delta_obs/ln15
print(f"δ^(obs)/ln15 = {float(ratio):.12f}")
# 找 1/1500 附近的邻居——0.00065845 ≈ ?
for denom in [1519, 1520, 1518, 1518.5, 1519.5, 1518.75]:
    base = ln15/Decimal(denom)
    r = delta_obs - base
    sig_r = abs(24*r)/unc
    print(f"  ln15/{denom} = {float(base):.10f}——残余 {float(r):.2e}——α⁻¹σ = {float(sig_r):.1f}")

print("\n--- ⑥ 关键结论 ---")
print(f"达标线（δ 层面）= {float(need):.2e}")
print("若贪心 5-6 项达 ≤1σ——σ 幂组合可行（注意幂次/系数框架身份）")
print("若 6 项仍 >3σ——纯 σ 幂路径极限不足——必须含 ln15 因子")
