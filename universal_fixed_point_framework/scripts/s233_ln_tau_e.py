# -*- coding: utf-8 -*-
"""S233 重大候选：ln(m_tau/m_e) vs I_e（框架量 8.1539907847）
检验：轻子质量比的对数 = 框架量 I_e？——e 直接参与轻子谱
先证伪纪律：精确计算——σ_score 判定
"""
import math
print("=== S233: ln(m_tau/m_e) vs I_e 检验 ===\n")

print("=== 1. 输入 ===")
m_tau = 1776.86       # MeV——PDG ±0.12
m_e = 0.51099895000   # MeV——PDG ±1.5e-10
u_tau = 0.12
u_e = 1.5e-10
print(f"m_tau = {m_tau}±{u_tau} MeV")
print(f"m_e = {m_e}±{u_e} MeV")

print("\n=== 2. ln(m_tau/m_e) 计算 ===")
r = m_tau/m_e
ln_r = math.log(r)
# 误差传播：u_ln = sqrt((u_tau/m_tau)^2 + (u_e/m_e)^2)
u_ln = math.sqrt((u_tau/m_tau)**2 + (u_e/m_e)**2)
print(f"m_tau/m_e = {r:.4f}")
print(f"ln(m_tau/m_e) = {ln_r:.8f}±{u_ln:.2e}")

print("\n=== 3. 框架量对照 ===")
I_e = 8.1539907847
print(f"I_e = 8.1539907847（活跃×e^(-σ^3)(1+α_v')——S172 升格量）")
diff = ln_r - I_e
s = abs(diff)/u_ln
print(f"差 = {diff:+.2e}")
print(f"σ_score = {s:.2f}σ——{'达标' if s<=1 else '提示' if s<=3 else '不达标'}")

print("\n=== 4. 展开 e^I_e vs m_tau/m_e ===")
eI = math.exp(I_e)
print(f"e^I_e = {eI:.4f}")
print(f"m_tau/m_e = {r:.4f}")
print(f"相对差 = {abs(eI-r)/r*100:.3f}%")

print("\n=== 5. 诚实评估 ===")
print("若 σ_score ≤1σ——I_e 直接给出 ln(m_tau/m_e)——重大")
print("  （框架量直接锚定轻子质量比——e 参与轻子谱！）")
print("若提示/不达标——普通接近——观察级或证伪")
