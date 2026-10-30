# -*- coding: utf-8 -*-
"""静默族修正覆盖域扫描（2026-10-26）

问题：静默族修正能覆盖哪些链失配？（第三链先验预言的边界刻画）
方法：全部已知理论-实验失配清单 vs 静默族修正量级谱——谱内 = 可修正候选、
谱外 = 机制外（需其他机制）。
"""
import math

n_gen, silence, powers, involution, fixed = 3, 5, 2, 7, 4
kmax = powers**n_gen  # 8
sigma = 1/(n_gen*silence)  # 1/15

# 静默族修正量级谱（幂和谱 {−2, −4, −6}）
corrections = {
    "σ":                sigma,                                  # 6.67%
    "静默⁻²":          1/silence**2,                            # 4%
    "Δ_dress = 2σ/3":  2*sigma/3,                              # 4.44%
    "σ²":              sigma**2,                                # 0.44%
    "6σ³":             6*sigma**3,                              # 0.18%
    "σ³×k_max×N_gen⁻¹": sigma**3*kmax/n_gen,                   # 0.079%（m_ρ 已闭合）
    "σ³×幂基×N_gen⁻¹":  sigma**3*powers/n_gen,                 # 0.0197%
    "静默⁻²×N_gen⁻⁴":   1/(silence**2*n_gen**4),                 # 0.049%
    "σ³":              sigma**3,                                # 0.03%
    "σ⁴":              sigma**4,                                # 0.002%
}

# 已知失配清单（理论-实验，轻子已闭合后剩余 + 已闭合参照）
mismatches = [
    # (链, 失配率绝对值, 状态, 参考)
    ("m_e（已闭合）", 0.064*2.935e-8, "✓ ε_μ 家族", "B''' 0.064σ_score"),
    ("m_μ（已闭合）", 0.034*2.177e-8, "✓ ε_μ 家族", "B''' 0.034σ_score"),
    ("E_τ（已闭合）", 0.018*6.84e-5, "✓ ε_μ 家族", "B''' 0.018σ_score"),
    ("m_ρ", 0.0008, "✓ 已闭合", "σ³×k_max×N_gen⁻¹ = 0.079%"),
    ("m_N", 0.00019, "近候选", "σ³×幂基×N_gen⁻¹ = 0.0197%（差 4.1%）"),
    ("m_N SU(6)", 0.082, "开放", "粗精度区——谱外"),
    ("Λ_QCD", 4.2, "开放", "绝对标度——谱外"),
    ("EM_pn", 0.38, "开放", "粗精度区——谱外"),
]

print("=== 静默族修正量级谱（排序）===")
for name, val in sorted(corrections.items(), key=lambda kv: -kv[1]):
    print(f"  {name:<24} {val*100:8.4f}%")
print()

print("=== 失配清单 vs 谱 ===")
for chain, rate, status, ref in mismatches:
    # 找谱内最近候选
    best_name, best_gap = None, 1e9
    for name, val in corrections.items():
        gap = abs(math.log10(rate+1e-30) - math.log10(val+1e-30)) if rate > 0 else 1e9
        if gap < best_gap:
            best_gap, best_name = gap, name
    inside = (rate >= 1e-5 and rate <= 0.01)  # 谱区间 [1e-5, 1%]
    mark = "谱内" if inside else "谱外"
    print(f"  {chain:<18} 失配 {rate*100:9.4f}% [{mark}] 最近谱成员: {best_name} | {status}")
print()

print("=== 覆盖域结论 ===")
print("静默族修正覆盖精细失配区 [1e-5, 1%]：m_ρ 已闭合（0.079% 命中）、")
print("m_N 近候选（0.0197% vs 0.019%——差 4.1%——组分容差内不立）")
print("谱外（>1%）：SU(6) 8.2%、EM_pn 38%、Λ 4.2×——需其他机制（非静默族）")
print()
print("先验预言状态：静默族可修正的宿主 = 精细失配区——当前谱内宿主仅")
print("m_ρ（已闭合）+ m_N（近候选）——**严格第三链先验预言仍未满足**——")
print("预言目标有限是覆盖域的诚实刻画（非失败）")
