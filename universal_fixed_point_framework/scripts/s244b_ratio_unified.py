# -*- coding: utf-8 -*-
"""S244b 比值族扩展扫描——统一口径修正版
m_ρ 统一用 PDG 2024 Breit-Wigner 官方口径：775.26 ± 0.23
（S245 核查：T-matrix pole 775.11±0.34 → 1.09σ 临界——登记敏感性）
m_Δ = 1232.0±0.3、m_μ = 105.6583755±0.0000023、m_τ = 1776.86±0.12
"""
import math
print("=== S244b: 比值族扩展扫描——统一口径（775.26） ===\n")

m_t = 1776.86; st = 0.12
m_r = 775.26; sr = 0.23
m_d = 1232.0; sd = 0.3
m_u = 105.6583755; sm = 0.0000023

def ratio_sig(n, dn, d, dd):
    r = n/d
    return r*math.sqrt((dn/n)**2 + (dd/d)**2)

# m_τ/m_ρ = √21/2（正向——S217 已升格）
r0 = m_t/m_r; s0 = ratio_sig(m_t, st, m_r, sr)
c0 = math.sqrt(21)/2
print(f"m_τ/m_ρ = {r0:.6f} vs √21/2 = {c0:.6f}——σ = {abs(r0-c0)/s0:.3f}σ——达标（S217 确认）")

# m_Δ/m_μ = 35/3
r1 = m_d/m_u; s1 = ratio_sig(m_d, sd, m_u, sm)
c1 = 35.0/3.0
print(f"m_Δ/m_μ = {r1:.6f} vs 35/3 = {c1:.6f}——σ = {abs(r1-c1)/s1:.2f}σ——提示")

# m_Δ/m_ρ = 27/17（活跃^3/F2）
r2 = m_d/m_r; s2 = ratio_sig(m_d, sd, m_r, sr)
c2 = 27.0/17.0
print(f"m_Δ/m_ρ = {r2:.6f} vs 27/17 = {c2:.6f}——σ = {abs(r2-c2)/s2:.2f}σ——提示")

# m_ρ/m_μ = 22/3（幂基×显态/活跃）
r3 = m_r/m_u; s3 = ratio_sig(m_r, sr, m_u, sm)
c3 = 22.0/3.0
print(f"m_ρ/m_μ = {r3:.6f} vs 22/3 = {c3:.6f}——σ = {abs(r3-c3)/s3:.2f}σ——提示")

# m_ρ/m_τ 反向
r4 = m_r/m_t; s4 = ratio_sig(m_r, sr, m_t, st)
c4 = 2.0/math.sqrt(21)
print(f"m_ρ/m_τ = {r4:.6f} vs 2/√21 = {c4:.6f}——σ = {abs(r4-c4)/s4:.3f}σ——达标（与正向一致）")

print("\n=== 结论 ===")
print("统一口径 775.26 后：m_ρ/m_τ 反向 = 0.955σ 与正向一致 ✓")
print("m_Δ/m_μ 35/3 = 2.27σ 提示、m_Δ/m_ρ 27/17 提示、m_ρ/m_μ 22/3 提示")
print("Δ 端比值 1.2-2.3σ 提示区家族模式——登记不升格")
print("★ S245 核查结论：S217 升格量口径正确（PDG 2024 Breit-Wigner")
print("  775.26±0.23→0.955σ 达标）——但共振质量定义敏感（T-matrix")
print("  pole 775.11±0.34→1.09σ 临界）——登记敏感性——升格保留")
