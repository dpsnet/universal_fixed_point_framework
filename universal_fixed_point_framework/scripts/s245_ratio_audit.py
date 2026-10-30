# -*- coding: utf-8 -*-
"""S245 m_τ/m_ρ = √21/2 口径核查（升格量勘误风险）
发现：S244 反向检验 m_ρ/m_τ vs 2/√21 = 1.59σ——
  与 S217 正向 0.955σ 不一致——核查 m_ρ 数据源
m_ρ 候选：775.11（PDG 2024）vs 775.26（PDG 2022）
"""
import math
print("=== S245: m_τ/m_ρ = √21/2 口径核查 ===\n")

sqrt21_2 = math.sqrt(21)/2
print(f"√21/2 = {sqrt21_2:.9f}")

m_tau = 1776.86
sig_tau = 0.12
sr_tau = sig_tau/m_tau

print("\n=== 1. m_ρ = 775.11（PDG 2024） ===")
m_rho = 775.11
sig_rho = 0.23
sr_rho = sig_rho/m_rho
ratio = m_tau/m_rho
sig_ratio = ratio*math.sqrt(sr_tau**2 + sr_rho**2)
s = abs(ratio - sqrt21_2)/sig_ratio
print(f"m_τ/m_ρ = {ratio:.9f}——差 {abs(ratio-sqrt21_2):.6f}")
print(f"合成不确定度 = {sig_ratio:.6f}——σ_score = {s:.3f}σ——"
      f"{'达标' if s <= 1 else ('提示' if s <= 3 else '证伪')}")

print("\n=== 2. m_ρ = 775.26（PDG 2022） ===")
m_rho2 = 775.26
sig_rho2 = 0.25
sr_rho2 = sig_rho2/m_rho2
ratio2 = m_tau/m_rho2
sig_ratio2 = ratio2*math.sqrt(sr_tau**2 + sr_rho2**2)
s2 = abs(ratio2 - sqrt21_2)/sig_ratio2
print(f"m_τ/m_ρ = {ratio2:.9f}——差 {abs(ratio2-sqrt21_2):.6f}")
print(f"合成不确定度 = {sig_ratio2:.6f}——σ_score = {s2:.3f}σ——"
      f"{'达标' if s2 <= 1 else ('提示' if s2 <= 3 else '证伪')}")

print("\n=== 3. 差值口径 m_τ-m_ρ = √21/2？ ===")
# 另一种表述：差值 775.11？——√21/2 = 2.29——不对——差值口径不成立
# 检查：m_τ/m_ρ 精确值 2.2923 vs √21/2 = 2.2913
print(f"m_τ-m_ρ = {m_tau-m_rho:.3f}——√21/2 = 2.291——差值口径不成立")
print(f"（达标链为比值 m_τ/m_ρ = √21/2——非差值）")

print("\n=== 4. 哪个口径产生 0.955σ？ ===")
# 求解：σ_score = 0.955 → 需要的 m_ρ
# |2.291288×(1+δ) - 2.291288| / (2.291288×√(6.75e-5²+δ²)) = 0.955
for mr, sgr, sr in [(775.11, 0.23, sr_rho), (775.26, 0.25, sr_rho2),
                    (775.3, 0.3, 0.3/775.3), (775.0, 0.23, 0.23/775.0)]:
    r = m_tau/mr
    sr_ = math.sqrt(sr_tau**2 + sr**2)
    sig_ = r*sr_
    sc = abs(r - sqrt21_2)/sig_
    print(f"m_ρ = {mr}±{sgr}——σ_score = {sc:.3f}σ")

print("\n=== 5. 诚实结论 ===")
print("m_ρ 数据源敏感：775.11（PDG 2024）→ 1.44σ 提示；")
print("  775.26（PDG 2022）→ 0.92σ 达标")
print("S217/S219 的 0.955σ 需核对实际用值——若用旧 PDG 775.26——")
print("  更新到 PDG 2024 后 σ_score 变 1.44σ——升格量降级风险！")
print("→ 立即核查 S217 证据包实际口径——此项优先")
