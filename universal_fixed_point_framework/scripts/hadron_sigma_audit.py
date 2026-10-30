# -*- coding: utf-8 -*-
"""强子端 σ 批量审计（2026-10-26）

P7-2/P7-6 链（组分模型）σ_score 口径：
  m_N  = 938.450（P7-6d 判别最优：Δ_hf = Λ·14/15 + 缺口 = Λ·b₀/25）
  m_ρ  = 2M_ud_eff（+0.11%）
  缺口 = κΛ(1−2σ_score/3)/5 = 76.649（+0.025%）vs κ²Λ/10 = 76.599（−0.041%）
实验精度：m_N 3e-10、m_ρ 4e-7（PDG）——σ_score 口径判定。
"""
import math

m_N_exp = 938.27208816
m_rho_exp = 775.26
m_N_rel = 3e-10          # PDG 938.27208816(29)
m_rho_rel = 0.03/775.26  # PDG 775.26 ± 0.03? 取 4e-5 保守

def grade(s):
    return "✓ 达标" if s <= 1 else ("～ 提示" if s <= 3 else "✗ 不达标")

print("="*70)
print("强子端 σ 批量审计（实验精度 PDG：m_N 3e-10、m_ρ ~4e-5 保守）")
print("="*70)

# ① m_N 链（P7-6d 判别最优）
m_N_pred = 938.450
sN = abs(m_N_pred-m_N_exp)/(m_N_exp*m_N_rel)
print(f"\n① m_N 链（P7-6d）：pred = {m_N_pred} vs 实验 {m_N_exp}")
print(f"   +{ (m_N_pred-m_N_exp)/m_N_exp*100:.4f}%（+{m_N_pred-m_N_exp:.3f} MeV）")
print(f"   σ_score = {sN:.0f} {grade(sN)}——实验精度 3e-10 使任何 >10⁻⁶ 级偏差天文不达标")

# ② m_ρ 链（2M_ud_eff）
m_rho_pred = 2*387.94   # M_ud_eff ≈ 387.94（P7-6 判别口径，m_ρ = 775.88 +0.08%?）
sR = abs(m_rho_pred-m_rho_exp)/(m_rho_exp*m_rho_rel)
print(f"\n② m_ρ 链（2M_ud_eff）：pred ≈ {m_rho_pred} vs 实验 {m_rho_exp}")
print(f"   +{ (m_rho_pred-m_rho_exp)/m_rho_exp*100:.3f}%")
print(f"   σ ≈ {sR:.0f} {grade(sR)}")

# ③ m_N 缺口链（无独立实验锚——来自框架公式残差，登记百分比级）
gap_exp = 1014.9-938.27208816   # SU(6) 组分 m_N − 实验（P7-2 口径）
# 判别候选：κΛ(1−2σ_score/3)/5
sigma = 1/15
L = 210  # Λ_QCD 框架值（禁闭域×静默）
kappa = 6/math.pi
d1 = kappa*L*(1-2*sigma/3)/5
d2 = (kappa**2)*L/10
print(f"\n③ m_N 缺口链（组分 m_N 1014.9 − 实验 938.272）：")
print(f"   缺口实验值 ≈ 76.63 MeV（无独立精度锚——框架残差口径）")
print(f"   候选1 κΛ(1−2σ_score/3)/5 = {d1:.3f}（+{(d1-76.63)/76.63*100:+.3f}%）")
print(f"   候选2 κ²Λ/10 = {d2:.3f}（{ (d2-76.63)/76.63*100:+.3f}%）")
print(f"   ★ σ_score 口径不适用（缺口非独立可测物理量——是框架公式残差）——维持百分比级登记")

# ④ SU(6) 缺陷（+8.1%）
print(f"\n④ SU(6) 缺陷：m_N 组分 1014.9 vs 实验 938.272 → +{(1014.9-m_N_exp)/m_N_exp*100:.1f}%")
print(f"   σ_score = {(1014.9-m_N_exp)/(m_N_exp*3e-10):.0f} ✗——已知开放缺口（P7-2 登记）")

# ⑤ Λ_QCD 框架值（禁闭域×静默 = 210）
print(f"\n⑤ Λ_QCD = 210（禁闭域×静默 = 42×5，104az-155）——框架量定义（非对实验的预测）")
print(f"   实验 Λ_MS(4味) 方案依赖（~296 MeV 等）——不同方案值不可直接 σ——维持框架量登记")

print()
print("="*70)
print("判别总结：强子质量链（组分模型）σ_score 口径全不达标")
print("——实验精度 10⁻⁸ vs 框架组分模型精度 10⁻⁴-10⁻²——精度鸿沟")
print("——'不是新失败'而是'精度等级诚实定位'：强子端 = 框架粗精度区")
print("（组分模型级 0.01-8%）、轻子端 = 精精度区（0.001% 级 σ_score 达标）")
print("——与笔记 P7-5d 体系判定一致（链的精度由最弱环节决定）")
print("——σ_score 口径统一后理论状态更清晰：轻子达标、强子粗精度、缺口谱开放")
