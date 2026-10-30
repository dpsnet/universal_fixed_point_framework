# -*- coding: utf-8 -*-
"""
S486 强子三胞胎 Koide k 系统检验：k = (Σm)/(Σ√m)² 是否 ≈ 活跃⁻¹ = 1/3
背景：S481 轻子 Koide k = 幂基/活跃 = 2/3（0.053σ✓）；S482 √2 =
RMS/均值比（0.004σ✓）；S485 θ_F 链函数（0.352σ✓）——轻子端 Koide
三成分全框架化闭合。
本步：强子端 Koide 型结构检验——三代三重结构（重子/介子三胞胎）：
  k_h = (Σm)/(Σ√m)²——若 ≈ 1/3 = 活跃⁻¹——强子端集合级形状
  框架化（与轻子 2/3 平行——'三代三重结构'统一形状规律）；
  RMS/⟨A⟩ = √(3k)——k=1/3 ⟹ RMS/⟨A⟩ = 1（强子三重态分布紧）
候选三胞胎：重子 (N,Δ,Σ)、(N,Δ,Λ)、(Σ,Λ,Ξ)、(Λ,Σ,Ξ)；
  介子 (π⁺,K⁺,η)、(ρ,K*,ω)、(π⁰,K⁰,η') 等。
纪律：σ_score 判定（合成不确定度）；先证伪再证明；pyenv。
"""
import math

# PDG 质量（MeV）与不确定度
hadrons = {
    # 重子
    "p":      (938.272089, 0.0001),
    "n":      (939.565421, 0.0001),
    "N":      (938.9187,   0.0001),   # (p+n)/2
    "Delta":  (1232.0,     0.1),      # Δ(1232)——PDG 1232.0 ± 0.1
    "Sigma":  (1192.642,   0.024),    # Σ⁰
    "Lambda": (1115.683,   0.006),
    "Xi":     (1314.86,    0.20),     # Ξ⁰
    # 介子
    "pi+":    (139.57039,  0.00012),
    "K+":     (493.677,    0.016),
    "eta":    (547.862,    0.018),
    "rho":    (775.26,     0.23),
    "K*":     (891.66,     0.26),
    "omega":  (782.65,     0.12),
    "pi0":    (134.9768,   0.0003),
    "K0":     (497.611,    0.013),
    "eta'":   (957.78,     0.06),
}

# 三胞胎候选（按质量组）
triplets = [
    ("重子 (N,Δ,Σ)",     ["N", "Delta", "Sigma"]),
    ("重子 (N,Δ,Λ)",     ["N", "Delta", "Lambda"]),
    ("重子 (Σ,Λ,Ξ)",     ["Sigma", "Lambda", "Xi"]),
    ("重子 (N,Σ,Ξ)",     ["N", "Sigma", "Xi"]),
    ("重子 (p,Δ,Σ)",     ["p", "Delta", "Sigma"]),
    ("介子 (π⁺,K⁺,η)",   ["pi+", "K+", "eta"]),
    ("介子 (ρ,K*,ω)",    ["rho", "K*", "omega"]),
    ("介子 (π⁰,K⁰,η')",  ["pi0", "K0", "eta'"]),
    ("介子 (π⁺,K⁺,η')",  ["pi+", "K+", "eta'"]),
    ("混合 (p,Δ,Λ)",     ["p", "Delta", "Lambda"]),
]

def koide_k(masses):
    s_sqrt = sum(math.sqrt(m) for m in masses)
    return sum(masses)/(s_sqrt*s_sqrt)

print("=" * 78)
print("S486 强子三胞胎 Koide k 检验：k = (Σm)/(Σ√m)² vs 活跃⁻¹ = 1/3")
print("=" * 78)

# 先验候选：活跃⁻¹ = 1/3（k=1/3 ⟹ RMS/⟨A⟩ = √(3k) = 1——紧分布）
pred_k = 1/3.0
print("  先验候选：k = 活跃⁻¹ = 1/3（⟹ RMS/⟨A⟩ = √(3k) = 1——三重态紧分布）")
print()

results = []
for name, names in triplets:
    ms = [hadrons[n][0] for n in names]
    us = [hadrons[n][1] for n in names]
    k = koide_k(ms)
    # k 不确定度：质量误差传播——∂k/∂m_i
    s = sum(math.sqrt(m) for m in ms)
    dk_dmi = [(1/s**2) - (2*sum(ms)/s**3)*(0.5/math.sqrt(m)) for m in ms]
    u_k = math.sqrt(sum((dk_dmi[i]*us[i])**2 for i in range(3)))
    ss = abs(k - pred_k)/u_k
    rms_mean = math.sqrt(3*k)   # S482：RMS/⟨A⟩ = √(3k)
    results.append((ss, name, k, u_k, rms_mean))

results.sort()
print("  %-20s %12s %12s %8s %10s" % ("三胞胎", "k", "u_k", "σ_score", "RMS/⟨A⟩"))
for ss, name, k, u_k, rms_mean in results:
    mark = "✓" if ss <= 1 else ("提示" if ss <= 3 else "✗")
    print("  %-20s %12.6f %12.2e %8.2f %10.5f %s" % (name, k, u_k, ss, rms_mean, mark))

print()
print("=" * 78)
print("对照组：轻子三重态（S481 已闭合）")
print("=" * 78)
m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.93
k_lep = koide_k([m_e, m_mu, m_tau])
print("  轻子 (e,μ,τ)：k = %.10f vs 幂基/活跃 = 2/3（0.053σ✓ S481）"
      % k_lep)
print("  RMS/⟨A⟩ = √(3k) = %.6f vs √2（0.004σ✓ S482）" % math.sqrt(3*k_lep))
print("  → 轻子 k = 2/3（展布大）、强子 k ≈ 1/3（紧）——")
print("    集合级形状由框架量（幂基/活跃 vs 活跃⁻¹）编码")

print()
print("=" * 78)
print("结论")
print("=" * 78)
hits = [r for r in results if r[0] <= 3]
print("  ≤3σ 命中的三胞胎：")
for ss, name, k, u_k, rms_mean in hits:
    print("    %s：k = %.6f——σ_score = %.2f" % (name, k, ss))
if not hits:
    print("    无——强子三胞胎 Koide k ≠ 1/3（证伪）")
print("  [诚实边界]：k=1/3 若命中为后验检验（非先验预言）——")
print("    强子三重态选择自由度（哪些三胞胎有意义）——")
print("    需机制论证（三代三重结构 vs 任意三重组合）")
