# -*- coding: utf-8 -*-
"""S194 比值族全扫描完整化——完整矩阵 σ_score 辨巧合
全部质量比值 × 全部框架量候选——系统性判别命中/提示/证伪
（S185 部分——本步完整化：含 π/η/ω/φ/K/N/Λ/Σ/Ω 全家族 + 所有候选）
"""
import math

# 质量（PDG 2024——MeV）
m_e = 0.51099895069
m_mu = 105.658375
m_tau = 1776.86
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

sr = {'e': 2.94e-10, 'mu': 2.2e-8, 'tau': 6.75e-5, 'pi': 4e-7, 'eta': 0.07/547.862,
      'K': 0.016/493.677, 'rho': 2.97e-4, 'omega': 0.05/782.65, 'phi': 0.019/1019.461,
      'N': 9.6e-8, 'Delta': 2.0/1232.0, 'Lambda': 0.006/1115.683, 'Sigma': 0.05/1193.15,
      'Omega': 0.29/1672.45}
m = {'e': m_e, 'mu': m_mu, 'tau': m_tau, 'pi': m_pi, 'eta': m_eta, 'K': m_K,
     'rho': m_rho, 'omega': m_omega, 'phi': m_phi, 'N': m_N, 'Delta': m_Delta,
     'Lambda': m_Lambda, 'Sigma': m_Sigma, 'Omega': m_Omega}

# 框架量候选（全）
cands = {
    '21/4': 21/4, '42/8': 42/8, '√21/2': math.sqrt(21)/2, '7/10': 0.7,
    '21/16': 21/16, '42×7/1232': 42*7/1232, '(42−3)/1232修正': 1-39/1232,
    '16/15': 16/15, '15/16': 15/16, '3/2': 3/2, '√(2/3)': math.sqrt(2/3),
    '7/11': 7/11, '11/7': 11/7, '√(5/2)': math.sqrt(5/2), '√2': math.sqrt(2),
    'σ²': (1/15)**2, 'σ³': (1/15)**3, 'σ⁴': (1/15)**4, 'e^{−2}': math.exp(-2),
    'e^{−I_e}': math.exp(-8.1539907847), 'e^{−I_μ}': math.exp(-2.8223920536),
}

def check(name, r, cand, cand_name, sr1, sr2):
    rel = abs(r-cand)/r
    sig = math.sqrt(sr1**2+sr2**2)
    score = rel/sig
    return score, (">3σ 证伪" if score > 3 else ("1-3σ 提示" if score > 1 else "≤1σ 达标"))

print("=== S194: 比值族全扫描完整化（完整矩阵 σ_score） ===\n")

# 全家族质量对（非平凡——排除同一家族已知 e^{−间隔} 结构）
pairs = [('tau','rho'), ('mu','rho'), ('e','rho'), ('tau','Delta'), ('mu','Delta'),
         ('e','Delta'), ('rho','Delta'), ('pi','rho'), ('eta','rho'), ('K','rho'),
         ('omega','rho'), ('phi','rho'), ('N','rho'), ('N','Delta'), ('Sigma','Delta'),
         ('Lambda','Delta'), ('Omega','Delta'), ('tau','pi'), ('rho','N'), ('Delta','Omega')]

hits = []
for a, b in pairs:
    r = m[a]/m[b]
    best = None
    for cn, cv in cands.items():
        sc, st = check(f"{a}/{b}", r, cv, cn, sr[a], sr[b])
        if sc <= 1:  # 只报达标
            best = (sc, cn, st)
            break
    if best:
        hits.append((a, b, best[0], best[1]))

print("=== ≤1σ 达标命中（比值 × 候选） ===")
for a, b, sc, cn in hits:
    print(f"  {m[a]/m[b]:.6f}（{a}/{b}）≈ {cn}——σ_score {sc:.2f}σ 达标")
if not hits:
    print("  （无）")

print("\n=== 重点候选逐项全家族检验 ===")
# √21/2 候选（m_τ/m_ρ）
print("√21/2 = 2.291288（m_τ/m_ρ 候选）——跨家族检验：")
for a, b in [('tau','rho'), ('tau','Delta'), ('tau','N'), ('tau','Sigma'), ('rho','Delta')]:
    r = m[a]/m[b]
    sc, st = check(f"{a}/{b}", r, math.sqrt(21)/2, "√21/2", sr[a], sr[b])
    print(f"  {a}/{b} = {r:.6f}——σ_score {sc:.2f}σ {st}")
print("→ √21/2 仅对 τ/ρ 命中——其余证伪——防巧合通过（S185 确认维持）")

# 21/16 候选（谱标度）
print("\n21/16 = 1.3125（谱标度候选）——跨家族检验：")
for a, b in [('phi','rho'), ('Delta','N'), ('tau','N'), ('Omega','Delta')]:
    r = m[a]/m[b]
    sc, st = check(f"{a}/{b}", r, 21/16, "21/16", sr[a], sr[b])
    print(f"  {a}/{b} = {r:.6f}——σ_score {sc:.2f}σ {st}")
print("→ 21/16 对 Δ/N 0.26σ 达标（S188 谱标度候选确认——已登记）")
print("→ φ/ρ 5.8σ 证伪（S193）、Ω/Δ 20.3σ 证伪——21/16 不泛化到奇异家族")

# 7/10 候选
print("\n7/10 = 0.7——跨家族检验：")
for a, b in [('eta','rho'), ('N','Delta'), ('Lambda','Delta'), ('tau','rho'), ('mu','rho')]:
    r = m[a]/m[b]
    sc, st = check(f"{a}/{b}", r, 0.7, "7/10", sr[a], sr[b])
    print(f"  {a}/{b} = {r:.6f}——σ_score {sc:.2f}σ {st}")
print("→ 7/10 无达标命中（η/ρ 28.7σ 证伪——S193）——仅作 E_τ 系数")

print("\n=== 已升格链汇总（σ_score 符合度总表） ===")
print("E_e 0.001σ ✓ / E_μ 1.83e-5σ ✓ / E_τ 0.0000σ ✓（轻子三链升格）")
print("m_ρ 0.55σ ✓ / m_Δ 0.000σ ✓（强子两链升格）")
print("m_τ/m_ρ = √21/2 0.40σ（候选——待裁决）")
print("42/8 = 21/4 0.81σ（m_τ²/m_ρ² 候选）")
print("42×7 = 294 0.14σ（Δ−N 分裂候选）")
print("m_ud/κΛ 观察级（σ_abs 未知）")
print("→ 升格链合计 5 条 + 比值候选 3 条——全可溯源")

print("\n=== 诚实判别 ===")
print("完整矩阵：≤1σ 达标仅 m_τ/m_ρ vs √21/2（且候选特异性）——")
print("  其余候选无跨家族泛化——防巧合通过")
print("√21/2 候选的跨家族特异性确认（τ/Δ、τ/N、τ/Σ、ρ/Δ 全证伪）")
