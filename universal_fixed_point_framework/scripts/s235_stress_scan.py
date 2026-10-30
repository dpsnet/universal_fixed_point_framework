# -*- coding: utf-8 -*-
"""S235 轻子组装链应力攻坚：Δ = ln(m_mu/m_e) - (I_e - I_mu)
扫描框架修正候选（σ 幂 x 系数、e 幂、混合）——先证伪纪律
"""
import math
print("=== S235: 轻子组装链 1.35σ 应力攻坚 ===\n")

I_e = 8.1539907847
I_mu = 2.8223920536
m_mu = 105.6583755
m_e = 0.51099895000
u_mu = 2.3e-6
u_e = 1.5e-10

print("=== 1. 应力 Δ 精确计算 ===")
ln_r = math.log(m_mu/m_e)
delta = ln_r - (I_e - I_mu)
u_ln = math.sqrt((u_mu/m_mu)**2 + (u_e/m_e)**2)
print(f"ln(m_mu/m_e) = {ln_r:.10f}±{u_ln:.2e}")
print(f"I_e - I_mu = {I_e-I_mu:.10f}")
print(f"Δ = {delta:+.10e}（相对 ln = {abs(delta)/ln_r*100:.4f}%）")

print("\n=== 2. 框架修正候选扫描 ===")
sig = 1/15
print(f"σ = 1/15——σ^5 = {sig**5:.3e}、σ^6 = {sig**6:.3e}")
print(f"42σ^5 = {42*sig**5:.3e}")
print(f"Δ/42σ^5 = {delta/(42*sig**5):.3f}")
print(f"Δ/σ^5 = {delta/(sig**5):.3f}")
print(f"Δ/σ^6 = {delta/(sig**6):.3f}")
print(f"Δ/e^(-6) = {delta/math.exp(-6):.4f}")
print(f"Δ/2σ^5 = {delta/(2*sig**5):.3f}")

print("\n=== 3. 候选命中判定 ===")
print(f"42σ^5 = {42*sig**5:.6e} vs Δ = {delta:.6e}——相对差 {abs(delta-42*sig**5)/abs(delta)*100:.2f}%")
print(f"26σ^5 = {26*sig**5:.6e} vs Δ——相对差 {abs(delta-26*sig**5)/abs(delta)*100:.2f}%")
print(f"42σ^6 = {42*sig**6:.6e} vs Δ——相对差 {abs(delta-42*sig**6)/abs(delta)*100:.2f}%")

print("\n=== 4. σ_score 口径（Δ 的不确定度） ===")
print(f"Δ 的不确定度 ≈ u_ln = {u_ln:.2e}（m_μ/m_e 传播——腿 3 精度）")
print(f"若候选与 Δ 差 < u_ln——σ_score < 1——可消除应力")

print("\n=== 5. 诚实评估 ===")
print("应力 Δ 数量级 ~1e-5——框架最小量 σ^5 ~1.3e-6——")
print("候选 42σ^5 ~5.5e-5 与 Δ 同量级——但需精确命中")
print("若命中——轻子组装链应力可由 42σ^5 消除——新结构")
print("若未命中——应力登记开放——不强行拟合")
