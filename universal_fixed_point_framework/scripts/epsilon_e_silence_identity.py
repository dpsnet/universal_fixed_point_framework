# -*- coding: utf-8 -*-
"""ε_e 静默族身份验证（2026-10-26）

ε_e（I_e 侧次级失配 ≈ −4.3e-7，之前"无净身份"）候选：
  ε_e = −ε_μ · 幂基/(N_gen×静默²) = −144e^{−16}(1+6σ³) · 2/75
验证：精确 ε_e 反解值 vs 候选。
"""
import math

sigma = 1/15; s3 = sigma**3
m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86

# 主导项（体系 A 口径）
I_e0 = 3*math.e - s3*(1+16/15+math.sqrt(2/3))
I_mu0 = math.log(16) + math.e**(-3)
I_e_exp = math.log(m_tau_c/m_e_c)
I_mu_exp = math.log(m_tau_c/m_mu_c)

# ε_μ 新身份
eps_mu = 144*math.e**(-16)*(1+6*s3)

# ε_e 反解（主导项失配——假设 ε_e 加在 I_e 上）
eps_e_recon = I_e_exp - I_e0
eps_e_mu = I_mu_exp - I_mu0

print(f"ε_μ（144e^{{−16}}(1+6σ³)）= {eps_mu:.6e}")
print(f"I_e 失配 ε_e_recon = {eps_e_recon:.6e}")
print(f"I_μ 失配 ε_μ_recon = {eps_e_mu:.6e}")
print()

# 候选 1：−ε_μ × 2/75（幂基/(N_gen×静默²)）
cand1 = -eps_mu * 2/75
print(f"候选1：−ε_μ×2/75 = {cand1:.6e}")
print(f"  vs ε_e_recon = {eps_e_recon:.6e}——差 {(cand1-eps_e_recon)/abs(eps_e_recon)*100:+.4f}%")
print()

# 候选 2：−ε_μ × (16/15−1)²/？——2/75 的框架分解检查
print(f"2/75 框架身份：幂基/(N_gen×静默²) = 2/(3×25)")
print(f"  2/75 = {2/75:.8f}")
print(f"  16/15−1 = 1/15 = σ——σ²×2/3？{2/3*sigma**2:.8f}（= 2/75? {2/3*sigma**2 == 2/75}）")
print()

# 候选 3：−ε_μ × σ×幂基/静默？
cand3 = -eps_mu * sigma*2/5
print(f"候选3：−ε_μ×σ×2/5 = {cand3:.6e}——vs {eps_e_recon:.6e} 差 {(cand3-eps_e_recon)/abs(eps_e_recon)*100:+.4f}%")
print()

# 判别：哪个候选最接近
print("判别：若候选1（2/75）<0.5% 则 ε_e 归入静默族修正第三处（−ε_μ×幂基/(N_gen×静默²)）")
print(f"  精确 ε_e 需用实验反解：ε_e = I_e_exp − I_e0 = {eps_e_recon:.6e}")
