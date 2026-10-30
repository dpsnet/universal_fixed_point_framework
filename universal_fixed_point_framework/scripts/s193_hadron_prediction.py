# -*- coding: utf-8 -*-
"""S193 新强子预测检验 + Δ 分裂族统一性
框架预测能力检验：对未纳入升格的强子（η/K/ω/φ/N/Λ/Σ/Ω）做框架量
候选测试（统一公式：质量 = 态数×生成根层展开）——全部 σ_score 判别
另：Δ−N 分裂（42×7=294）vs Δ−Σ 分裂（42−3=39）——统一性检查
"""
import math

# 质量（MeV——PDG 2024）
m_pi = 134.9768
m_eta = 547.862
m_K = 493.677
m_rho = 775.387
m_omega = 782.65
m_phi = 1019.461
m_N = 938.272
m_Delta = 1232.0
m_Lambda = 1115.683
m_Sigma = 1193.15
m_Omega = 1672.45

# σ_rel
sr_pi = 4e-7
sr_eta = 0.07/547.862   # ≈1.28e-4
sr_K = 0.016/493.677
sr_rho = 2.97e-4
sr_omega = 0.05/782.65  # ≈6.4e-5
sr_phi = 0.019/1019.461 # ≈1.86e-5
sr_N = 9.6e-8
sr_Delta = 2.0/1232.0
sr_Lambda = 0.006/1115.683
sr_Sigma = 0.05/1193.15
sr_Omega = 0.29/1672.45

def ss(name, r, cand, cand_name, sr1, sr2):
    rel = abs(r-cand)/r
    sig = math.sqrt(sr1**2+sr2**2)
    score = rel/sig
    status = "达标" if score <= 1 else ("提示" if score <= 3 else "不达标")
    print(f"  {name} = {r:.6f} vs {cand_name} = {cand:.6f}——σ_score {score:.2f}σ {status}")
    return score, status

print("=== S193: 新强子预测检验 ===\n")

print("=== ① 介子（ρ 家族——统一公式 8×(全态+活跃⁴)×修正） ===")
print("m_η 候选（7/10×m_ρ？——0.7 两口径）")
ss("m_η/m_ρ", m_eta/m_rho, 0.7, "7/10", sr_eta, sr_rho)
print("m_φ 候选（21/16？——谱标度）")
ss("m_φ/m_ρ", m_phi/m_rho, 21/16, "21/16", sr_phi, sr_rho)
print("m_ω 候选（1+2.1σ²？——2.1 不干净）")
print(f"  m_ω/m_ρ = {m_omega/m_rho:.6f}——1+2.1σ² = {1+2.1/225:.6f}——2.1 非框架量——弃")
print("m_ω−m_ρ = 7.263——≈对合7？")
print(f"  {m_omega-m_rho:.3f} vs 7——差 0.263——0.0376 相对——3.6% 观察级——不升格")

print("\n=== ② 重子（Δ 家族——m_Δ = 全态×对合×显态 = 1232） ===")
print("m_N 候选（Δ−42×7 = 294？——S187/S188 已登记）")
ss("m_N/m_Δ", m_N/m_Delta, 1-294/1232, "1−42×7/1232", sr_N, sr_Delta)
print(f"  m_Δ−m_N = {m_Delta-m_N:.3f}——42×7 = 294——差 {abs(294-(m_Delta-m_N)):.3f}")
print("m_Σ 候选（Δ−(42−3) = 39？——新）")
ss("m_Σ/m_Δ", m_Sigma/m_Delta, 1-39/1232, "1−(42−3)/1232", sr_Sigma, sr_Delta)
print(f"  m_Δ−m_Σ = {m_Delta-m_Sigma:.3f}——39 = 约束域−活跃——差 {abs(39-(m_Delta-m_Sigma)):.3f}")
print(f"  → 脚本实际 σ_score = 0.08σ 达标（σ_rel(Δ)=1.62e-3 主导）——但后验组装+分裂不统一——观察级")
print("m_Λ 候选？")
print(f"  m_Λ/m_Δ = {m_Lambda/m_Delta:.6f}——无干净候选")
print("m_Ω 候选？")
print(f"  m_Ω/m_Δ = {m_Omega/m_Delta:.6f}——无干净候选")

print("\n=== ③ Δ 分裂族统一性检查 ===")
print(f"m_Δ−m_N = 293.728——候选 42×7 = 294（乘法——约束域×对合）")
print(f"m_Δ−m_Σ = 38.85——候选 42−3 = 39（减法——约束域−活跃）")
print(f"→ 两分裂用不同组装（乘法 vs 减法）——不统一——提示巧合风险")
print(f"→ m_Σ 候选观察级登记——1.5σ 提示——不升格")

print("\n=== ④ 诚实判别 ===")
print("新强子预测检验：")
print("  m_η：7/10——28.7σ 证伪（不达标）")
print("  m_φ：21/16——5.8σ 证伪（不达标）")
print("  m_ω：2.1σ² 弃（2.1 非框架量）、Δω−ρ = 7.263 观察级（3.6%——不升格）")
print("  m_N：Δ−42×7 = 938——0.18σ 达标（后验——S187/S188 已登记）")
print("  m_Σ：Δ−39 = 1193——0.08σ 达标（新候选——后验组装+分裂不统一——观察级不升格）")
print("  m_Λ/m_Ω：无干净候选")
print("→ 框架当前预测边界：已升格 ρ/Δ + 后验 N——新强子无先验命中")
print("→ 诚实登记：框架对未纳入强子的先验预测能力尚未建立")
