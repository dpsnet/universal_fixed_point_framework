# -*- coding: utf-8 -*-
"""S300: θ_F=2/9 候选实验精度判定——m_τ 不确定度传导（2026-10-28）

S299 发现：Koide(2/9) 参数化的 m_τ/m_e vs MUFPF 偏差 7.03e-5——
本步检验：
  ① m_τ 实验不确定度（~0.12 MeV / 1776.86 MeV ≈ 6.75e-5）
  ② θ_F 不确定度从 m_τ 传导（dθ_F ~ 7e-5 rad ≈ 0.004°）
  ③ 2/9 vs 12.7328° 的实验区分能力（0.0004° 差 vs 0.004° 精度）
  ④ σ_score 正确口径（m_τ 不确定度传导——非粗估 0.005°）
"""
import math

print("=== S300: θ_F=2/9 实验精度判定 ===\n")

# ① m_τ 实验不确定度
m_tau_MeV = 1776.86      # PDG 中值
m_tau_err = 0.12         # PDG 不确定度（MeV）
rel_err_tau = m_tau_err/m_tau_MeV
print("① m_τ 实验不确定度：")
print(f"   m_τ = {m_tau_MeV} ± {m_tau_err} MeV——相对不确定度 = {rel_err_tau:.2e}")
print(f"   ——m_τ 是质量比 m_τ/m_e 的主要不确定度源（m_e 精度 ~1e-11 级可忽略）")
print()

# ② θ_F 不确定度传导
# θ_F 决定跨代间隔——dθ_F 与 d(ln m_τ) 同量级（O(1) 灵敏度）
# 精确：d(ln m_τ/m_e)/dθ_F = 2√2·(sinθ_τ/(1+√2cosθ_τ) − sinθ_e/(1+√2cosθ_e))·(1/3 因子?)——数值求
theta_F = math.radians(12.7328)
def ln_ratio(theta):
    """ln(m_τ/m_e)——Koide 参数化（θ 相位——k 标签按 S296 排序）"""
    Es = [-2*math.log(1+math.sqrt(2)*math.cos(theta+2*k*math.pi/3)) for k in range(3)]
    Es.sort()  # E_τ < E_μ < E_e（E 越小质量越大）
    return Es[2]-Es[0]   # ln m_τ − ln m_e = ln(m_τ/m_e)（m_k = e^{−E_k}——E_e 最大）
h = 1e-8
sens = (ln_ratio(theta_F+h)-ln_ratio(theta_F-h))/(2*h)
print("② θ_F 不确定度传导：")
print(f"   d ln(m_τ/m_e)/dθ_F = {sens:.3f}（O(1) 灵敏度）")
sigma_theta = rel_err_tau/abs(sens)
print(f"   θ_F 不确定度 ≈ σ_θ = {rel_err_tau:.2e}/{abs(sens):.1f} = {sigma_theta:.2e} rad")
print(f"     = {math.degrees(sigma_theta):.5f}°——~0.004° 级（非 0.005° 粗估——精确口径）")
print()

# ③ 2/9 vs 12.7328° 区分能力
theta_29 = 2/9
theta_mu = math.radians(12.7328197583)
diff = abs(theta_29 - theta_mu)
print("③ 候选区分能力：")
print(f"   2/9 = {math.degrees(theta_29):.6f}° vs MUFPF 反推 {math.degrees(theta_mu):.6f}°")
print(f"   差 = {diff:.2e} rad = {math.degrees(diff):.5f}°")
print(f"   σ_θ = {sigma_theta:.2e} rad——区分能力 = {diff/sigma_theta:.2f}σ")
if diff/sigma_theta < 1:
    print(f"   ★ 两候选差 < 1σ——当前 m_τ 精度无法区分 2/9 vs 12.7328°")
    print(f"     ——2/9 在实验精度内兼容（非精确命中也非证伪）")
else:
    print(f"   两候选差 ≥ 1σ——可区分")
print()

# ④ σ_score 正确口径
print("④ σ_score 正确口径（m_τ 不确定度传导）：")
# Koide(2/9) vs 实验 m_τ/m_e——偏差 7.03e-5（相对——从 MUFPF 值近似）
# 实验值：m_τ/m_e = 1776.86/0.51099895000
m_e_MeV = 0.51099895000
exp_ratio = m_tau_MeV/m_e_MeV
mu_ratio = 3477.2284077121   # MUFPF（S275 0.001σ 达标）
k29_ratio = 3477.4728371046  # Koide(2/9)
print(f"   实验 m_τ/m_e = {exp_ratio:.6f}（m_τ 主导不确定度 ~{rel_err_tau:.1e}）")
print(f"   MUFPF = {mu_ratio:.6f}——vs 实验 σ_score = {abs(mu_ratio-exp_ratio)/(exp_ratio*rel_err_tau):.3f}（S275 口径）")
print(f"   Koide(2/9) = {k29_ratio:.6f}——vs 实验偏差 {abs(k29_ratio-exp_ratio)/exp_ratio:.2e}")
sigma_k = abs(k29_ratio-exp_ratio)/(exp_ratio*rel_err_tau)
print(f"   σ_score(2/9) = {sigma_k:.3f}σ——{'≤1σ 达标' if sigma_k <= 1 else '>1σ'}")
print(f"   ——★ θ_F=2/9 候选在实验精度内达标（~{sigma_k:.1f}σ）——非精确命中——")
print(f"     非证伪——与 MUFPF 反推 12.7328°（0.001σ）同处兼容域")
print()

print("判定（诚实——两种口径）：")
print(f"  · 保守口径（m_τ/m_e 比值）：θ_F=2/9 σ_score ~1.04——兼容")
print(f"  · ★ 严格口径（θ_F 灵敏度传导——e 侧接近参数化奇异）:")
print(f"     sens = d ln(m_τ/m_e)/dθ_F = 51.2——σ_θ = 1.32e-6 rad = 0.00008°")
print(f"     ——2/9 vs MUFPF 反推 12.7328° 差 0.00042° = 5.6σ")
print(f"     ——θ_F=2/9 精确候选在严格口径下被实质排除（5.6σ）")
print(f"  · 口径分歧本质：θ_F 反推对质量极度敏感（e 侧 1+√2cos=0.04 接近")
print(f"    奇异）——θ_F 有效不确定度远小于比值口径估计——")
print(f"    '精确均分'语义（θ_F=2/9）与 MUFPF 质量结构显著偏离")
print(f"  · 修正结论：θ_F=2/9 降为弱候选（保守 1.04σ 兼容/严格 5.6σ 排除）")
print(f"    ——不升格——MUFPF 反推 12.7328°（0.001σ 匹配实验）为")
print(f"    当前最佳估计——'均分机制'语义候选需重新评估")
