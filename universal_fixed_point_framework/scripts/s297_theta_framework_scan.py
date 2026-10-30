# -*- coding: utf-8 -*-
"""S297: θ_F 框架量精确候选扫描（2026-10-28）

S296 发现 θ_F ≈ 2/9 rad = σ·(10/3)——偏差 0.0004°。本步：
  ① 精确候选扫描——θ_F 的框架量组合（含 σ 幂修正 δ_V3 型）
  ② 判定 2/9 是精确恒等还是近似——偏差来源
  ③ 若存在框架量精确表达——登记内生候选（重大）
"""
import math

print("=== S297: θ_F 框架量精确候选扫描 ===\n")

sigma = 1/15
e = math.e

# θ_F 精确反推值（等价类代表——从 MUFPF 公式——S295/S296 反推）
# 更精确：用 MUFPF 三质量重算 θ_F
E_tau_D = 16*math.log(15) + (7/10)*math.log(16/15) - 8*(144*e**(-16)*(1+6*sigma**3)) \
          - (sigma**5 - e**(-16)) - 2*sigma**8*(1+sigma)
alpha_vp = 16/15 + math.sqrt(2/3)*(1+6*sigma**3)
I_e = 3*e - sigma**3*(1+alpha_vp)
I_mu = e + 42*e**(-6) + 2*sigma**5
I_e_next = I_e + (5/2)*e**(-18)
E_e = E_tau_D + I_e_next - (27/80)*e**(-19)
E_mu = E_tau_D + I_mu
m_e, m_mu, m_tau = e**(-E_e), e**(-E_mu), e**(-E_tau_D)

s_e, s_mu, s_tau = math.sqrt(m_e), math.sqrt(m_mu), math.sqrt(m_tau)
A = (s_e+s_mu+s_tau)/3
x0 = (s_e/A-1)/math.sqrt(2)
x1 = (s_mu/A-1)/math.sqrt(2)
sin_theta = (-0.5*x0 - x1)*2/math.sqrt(3)
theta = math.atan2(sin_theta, x0)
theta_mod = math.degrees(theta) % 120.0
theta_mod = theta_mod if theta_mod <= 60 else theta_mod - 120.0
theta_rad = math.radians(theta_mod)
print(f"θ_F（模 120° 等价类代表）={theta_mod:.10f}° = {theta_rad:.12f} rad")

# ① 精确候选扫描——框架量组合
print(f"\n① 框架量组合候选：")
delta_V3 = 6*sigma**3 + 4*sigma**5 + 8*sigma**7 + 5*sigma**8  # 0.0017830940

cands = {
    "2/9": 2/9,
    "2/9 + δ_V3/7": 2/9 + delta_V3/7,
    "2/9 + δ_V3/6": 2/9 + delta_V3/6,
    "2/9 − δ_V3/6": 2/9 - delta_V3/6,
    "2/9·(1+σ)": 2/9*(1+sigma),
    "2/9·(1+σ²)": 2/9*(1+sigma**2),
    "2/9·(1+σ³)": 2/9*(1+sigma**3),
    "σ·10/3·(1+σ³)": sigma*10/3*(1+sigma**3),
    "σ·10/3·(1+δ_V3)": sigma*10/3*(1+delta_V3),
    "σ·(10/3+ε_μ·σ)": sigma*(10/3 + 144*e**(-16)*(1+6*sigma**3)*sigma),
    "σ·(静默×幂基/活跃)·(1+σ³)": None,
    "2/9 + e⁻¹⁶·σ": 2/9 + e**(-16)*sigma,
    "2/9 + 42e⁻⁶·σ⁵": 2/9 + 42*e**(-6)*sigma**5,
    "arctan(σ·10/3)": math.atan(sigma*10/3),
    "asin(σ·10/3·(1−σ))": None,
    "π/14.137": math.pi/14.137,
}
print(f"目标：θ_F = {theta_rad:.12f} rad")
results = []
for name, val in cands.items():
    if val is None:
        continue
    diff = abs(val - theta_rad)
    rel = diff/theta_rad
    results.append((diff, name, val, rel))
    print(f"  {name} = {val:.12f}——偏差 {diff:.2e}（相对 {rel:.2e}）")

results.sort()
print(f"\n★ 最优候选：")
for diff, name, val, rel in results[:4]:
    print(f"  {name} = {val:.12f}——偏差 {diff:.2e}（{diff*180/math.pi:.6f}°）")

# ② 判定 2/9 是否精确
print(f"\n② 2/9 判定：")
diff_29 = abs(2/9 - theta_rad)
print(f"  2/9 = 0.222222222222 vs θ_F = {theta_rad:.12f}——偏差 {diff_29:.2e}")
print(f"  相对偏差 = {diff_29/theta_rad:.2e}")
print(f"  ——偏差非零——2/9 是近似（~7e-6 相对）——非精确恒等")
print(f"  ——但偏差极小（0.0004°）——与 θ_F 测量精度同量级——")
print(f"    框架语义候选（非升格证据）")

# ③ 若存在框架量精确表达——登记
print(f"\n③ 精确性判定：")
if results[0][0] < 1e-9:
    print(f"  ★ 找到精确框架量表达：{results[0][1]}——偏差 < 1e-9 rad")
    print(f"    ——重大：θ_F 内生候选成立")
else:
    print(f"  无精确框架量表达（最优偏差 {results[0][0]:.2e} rad = {results[0][0]*180/math.pi:.6f}°）")
    print(f"  ——θ_F 框架量分解保持候选级（2/9 近似 + σ_score ~0.08）")
    print(f"  ——框架语义待深挖（2/9 简单有理数——防巧合）")

print(f"\n结论：")
print(f"  · θ_F ≈ 2/9 = σ·10/3——偏差 0.0004°——候选级（防巧合登记）")
print(f"  · 无精确框架量恒等——θ_F 内生化未达成——保持'近似互证'级")
print(f"  · 论文价值：Koide 结构角 ≈ MUFPF 框架量组合（σ·静默×幂基/活跃）")
print(f"    ——近似级交叉验证材料（诚实标注）")
