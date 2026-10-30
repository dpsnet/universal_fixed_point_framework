# -*- coding: utf-8 -*-
"""S234 轻子间隔量结构三腿自洽闭合检验
S179 组装链：m_mu/m_tau = e^(-I_mu)、m_e/m_tau = e^(-I_e)
三腿检验：m_mu/m_e = e^(-(I_e-I_mu))——组装链第三腿
I_e = 8.1539907847、I_mu = 2.8223920536（S172 升格框架量）
"""
import math
print("=== S234: 轻子间隔量三腿自洽检验 ===\n")

I_e = 8.1539907847
I_mu = 2.8223920536

print("=== 1. 三腿预测 ===")
m_tau, m_mu, m_e = 1776.86, 105.6583755, 0.51099895000
u_tau, u_mu, u_e = 0.12, 2.3e-6, 1.5e-10

# 腿 1：m_mu/m_tau = e^(-I_mu)
p1 = math.exp(-I_mu)
r1 = m_mu/m_tau
u1 = r1 * math.sqrt((u_mu/m_mu)**2 + (u_tau/m_tau)**2)
s1 = abs(r1-p1)/u1
print(f"腿1：m_mu/m_tau 实验 {r1:.6f}±{u1:.2e} vs e^(-I_mu) = {p1:.6f}——σ_score = {s1:.2f}σ")

# 腿 2：m_e/m_tau = e^(-I_e)
p2 = math.exp(-I_e)
r2 = m_e/m_tau
u2 = r2 * math.sqrt((u_e/m_e)**2 + (u_tau/m_tau)**2)
s2 = abs(r2-p2)/u2
print(f"腿2：m_e/m_tau 实验 {r2:.8f}±{u2:.2e} vs e^(-I_e) = {p2:.8f}——σ_score = {s2:.2f}σ")

# 腿 3：m_mu/m_e = e^(I_e-I_mu)（商——正指数）
p3 = math.exp(I_e-I_mu)
r3 = m_mu/m_e
u3 = r3 * math.sqrt((u_mu/m_mu)**2 + (u_e/m_e)**2)
s3 = abs(r3-p3)/u3
print(f"腿3：m_mu/m_e 实验 {r3:.4f}±{u3:.2e} vs e^(-(I_e-I_mu)) = {p3:.4f}——σ_score = {s3:.2f}σ")

print("\n=== 2. 间隔量结构 ===")
print(f"I_mu = e + 42e^(-6) + 2σ^5 = {I_mu:.8f}——e 主项 + 修正")
print(f"I_e = 3e - σ^3(1+α_v') = {I_e:.8f}——3e 主项 - 修正")
print(f"I_e - I_mu = {I_e-I_mu:.6f}——vs 16/3 = 5.3333——差 {abs((I_e-I_mu)-16/3):.4f}")
print(f"  （S227 证伪 e^(16/3) 的精确来源——I_e-I_mu ≠ 16/3）")
print(f"I_e/I_mu = {I_e/I_mu:.4f}——vs 26/9 = 2.8889——差 {abs(I_e/I_mu-26/9)/ (26/9)*100:.3f}%（S199 观察）")

print("\n=== 3. 诚实评估 ===")
print("三腿全部 = 组装链（S179 已确立）——本检验为自洽再确认")
print("0.00σ 级一致 = 链内部一致性——非独立新检验")
print("新观察：轻子质量比对数 = 框架间隔量（I 值含 e 主项）")
print("  ——'e 线性参与轻子谱'（I_mu 的 e、I_e 的 3e）")
print("I_e/I_mu ≈ 26/9：0.004% 差——但理论-理论比——观察级")
print("→ 无新升格——轻子间隔量结构完整闭合确认")
