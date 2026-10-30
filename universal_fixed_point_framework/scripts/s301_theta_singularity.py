# -*- coding: utf-8 -*-
"""S301: θ_F 灵敏度奇异域深挖——静默保护 m_e 非零（2026-10-28）

S300 发现：θ_F 反推对质量极度敏感（sens=51.2）——e 侧
1+√2cos(θ_e)=0.04 接近参数化奇异（cos → −1/√2 ⟹ m_e → 0）。
本步深挖：
  ① 奇异极限：m_e=0 ⟺ θ_F=15°（=SigmaInv 度数值）——验证
  ② 奇异距离 δ = 15°−θ_F——δ ≈ 静默⁻² = 1/25 rad？——精确扫描
  ③ m_e 侧因子 = 1+√2cos(θ_e) ≈ δ——静默机制保护 m_e 非零
  ④ θ_F 奇异极限 = 15° 的框架语义（SigmaInv 度数值）
"""
import math

print("=== S301: θ_F 灵敏度奇异域深挖 ===\n")

sigma = 1/15
e = math.e

# θ_F 反推精确值（MUFPF——S295）
theta_F = 12.7328197583   # 度（模 120° 代表）
theta_rad = math.radians(theta_F)

# ① 奇异极限验证
print("① 奇异极限（m_e=0）：")
print(f"   m_e ∝ (1+√2·cos(θ_e))²——m_e=0 ⟺ cos(θ_e) = −1/√2")
print(f"   θ_e = θ_F+2kπ/3——cos(θ_e)=−1/√2 ⟹ θ_e = 135° 或 225°")
print(f"   135°：θ_F+120°=135° ⟹ θ_F = 15°；225°：θ_F+240°=225° ⟹ θ_F = −15° ≡ 15°（模 120°）")
print(f"   ★ 奇异极限 θ_F = 15°——恰为 SigmaInv=15 的度数值！")
print()

# ② 奇异距离 δ
delta = 15.0 - theta_F
delta_rad = math.radians(delta)
print("② 奇异距离 δ = 15°−θ_F：")
print(f"   δ = {delta:.9f}° = {delta_rad:.9f} rad")
cands = {
    "静默⁻² = 1/25": 1/25,
    "静默⁻²·(1+σ)": 0.04*(1+sigma),
    "静默⁻²·(1−σ)": 0.04*(1-sigma),
    "σ·(3/5)": sigma*3/5,
    "σ²·9 = (3σ)²": (3*sigma)**2,
    "σ·2/7": sigma*2/7,
    "e⁻³": e**(-3),
    "σ·3·(1/2)": sigma*3/2,
    "1/(2·12.6)": 1/(2*12.6),
    "2σ/3·(5/3)": 2*sigma/3*5/3,
}
for name, val in cands.items():
    diff = abs(val - delta_rad)
    print(f"   {name} = {val:.9f}——偏差 {diff:.2e}（相对 {diff/delta_rad:.2e}）")
print(f"   ——静默⁻² = 0.04——偏差 {abs(1/25-delta_rad):.2e}（相对 {abs(1/25-delta_rad)/delta_rad:.2e}）")
print()

# ③ m_e 侧因子 ≈ δ 验证
theta_e = theta_rad + 2*math.pi/3   # k=1（e 侧——θ_F+120°）
factor_e = 1 + math.sqrt(2)*math.cos(theta_e)
print("③ m_e 侧因子 = 1+√2cos(θ_e)：")
print(f"   θ_e = {math.degrees(theta_e):.6f}°——cos = {math.cos(theta_e):.9f}")
print(f"   因子 = {factor_e:.9f} vs δ = {delta_rad:.9f}——比值 {factor_e/delta_rad:.4f}")
print(f"   一阶近似：因子 ≈ δ——差 {abs(factor_e-delta_rad):.2e}（{abs(factor_e-delta_rad)/delta_rad:.2%}）")
print(f"   ——高阶修正（δ² 项）——cos(135°−δ) 展开——二阶 −δ²/2·√2")
corr2 = delta_rad**2/math.sqrt(2)/2
print(f"   二阶修正估计：δ²/2√2 = {corr2:.2e}——(因子−δ)/二阶 = {abs(factor_e-delta_rad)/corr2:.2f}")
print()

# ④ θ_F 奇异极限 = 15° 框架语义
print("④ θ_F 奇异极限 = 15° 的框架语义：")
print(f"   SigmaInv = 15（σ=1/15 的框架常数）——度数值恰为奇异极限")
print(f"   ★ m_e=0 ⟺ θ_F = 15° = SigmaInv°——Koide 质量谱的奇异")
print(f"     边界由框架常数 SigmaInv 定义（度数值）")
print(f"   ★ 实际 θ_F = 12.7328°——偏离 δ ≈ 静默⁻²——")
print(f"     m_e 非零（近零）由静默机制抬升保护——'静默保护'")
print(f"     ——静默 = 冻结/闭合——m_e 接近冻结但被静默⁻² 抬升")
print()

# ⑤ m_e/m_μ 与 δ 的关系——S269b 修正候选检验
print("⑤ m_e 近零性与轻子端闭合的衔接：")
m_e_v = 4.185463e-23
m_mu_v = 8.654209e-21
ratio = m_e_v/m_mu_v
# Koide 侧：m_e/m_μ = [1+√2cos(θ_e)]²/[1+√2cos(θ_μ)]²（θ_μ = θ_F+4π/3——k=2）
theta_mu = theta_rad + 4*math.pi/3
f_mu = 1 + math.sqrt(2)*math.cos(theta_mu)
f_e = 1 + math.sqrt(2)*math.cos(theta_e)
print(f"   Koide 侧 m_e/m_μ = (f_e/f_μ)² = ({f_e:.6f}/{f_mu:.6f})² = {(f_e/f_mu)**2:.6f}")
print(f"   MUFPF m_e/m_μ = {ratio:.6f}")
print(f"   偏差 = {abs((f_e/f_mu)**2-ratio)/ratio:.2e}")
print(f"   ——e 侧因子 f_e ≈ 静默⁻²（0.04）——m_e 近零性 = 静默抬升")
print(f"   ——m_e 的 0.007σ 修正候选（S269b +(5/2)e⁻¹⁸）——θ_F 或 δ 级")

print(f"\n判定：")
print(f"  ★ θ_F 奇异极限 = 15° = SigmaInv°——框架常数定义 Koide 谱边界")
print(f"  ★ δ = 15°−θ_F ≈ 静默⁻² = 1/25（偏差 1.08%——近似级）")
print(f"  ★ m_e 非零由静默机制保护（静默⁻² 抬升）——'静默保护'语义")
print(f"  ★ m_e 近零性 = Koide 谱中静默机制的显现——e 侧敏感性的根源")
print(f"  诚实标注：δ ≈ 静默⁻² 偏差 1.08%——近似候选——精确分解待深挖；")
print(f"    奇异极限 15° = SigmaInv 为数值巧合或框架语义——待机制论证")
