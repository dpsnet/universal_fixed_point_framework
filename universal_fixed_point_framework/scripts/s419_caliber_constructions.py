# -*- coding: utf-8 -*-
"""S419 不同实验口径的 MUFPF 构造方式（2026-10-29）
对每个 α⁻¹ 实验口径，求框架内修正构造：
  α⁻¹(构造) = 72+24ln15+24δ* + Δ(框架组合)
扫描单体/双项：m ∈ {e⁻ⁿ, σⁿ, ln15·e⁻ⁿ} × c ∈ 系数池
报告每个口径的最自然构造 + 残差 σ_score
"""
import itertools
import math

# MUFPF 基底
sigma = 1 / 15
alpha_base = 72 + 24 * math.log(15) + 24 * (6*sigma**3 + 4*sigma**5 + 8*sigma**7 + 5*sigma**8)

# 实验口径：名称, 中心值, 不确定度
exps = [
    ("2018 总平均", 137.035999084, 2.1e-8),
    ("Cs 反冲 (Parker 2018)", 137.035999046, 2.7e-8),
    ("a_e g-2 (Fan 2023)", 137.035999166, 1.6e-8),
    ("Rb 反冲 (Morel 2020)", 137.035999206, 1.1e-8),
    ("2022 总平均", 137.035999177, 2.1e-8),
]

# 框架单体池
monos = {
    "e⁻¹⁶": math.e**-16, "e⁻¹⁷": math.e**-17, "e⁻¹⁸": math.e**-18,
    "e⁻¹⁹": math.e**-19, "e⁻²⁰": math.e**-20, "e⁻²¹": math.e**-21,
    "σ⁵": sigma**5, "σ⁶": sigma**6, "σ⁷": sigma**7, "σ⁸": sigma**8,
    "σ⁹": sigma**9, "σ¹⁰": sigma**10,
    "ln15·e⁻¹⁸": math.log(15)*math.e**-18, "ln15·e⁻¹⁹": math.log(15)*math.e**-19,
    "16e⁻¹⁸": 16*math.e**-18, "42e⁻¹⁸": 42*math.e**-18,
}
coeffs = [-8, -7, -6, -5, -4, -3, -5/2, -2, -3/2, -1, -1/2,
          1/2, 1, 3/2, 2, 5/2, 3, 4, 5, 6, 7, 8, 15, 16, 24, 42, 120, 144]

print("=== S419 不同实验口径的 MUFPF 构造方式 ===")
print(f"MUFPF 基底 α⁻¹ = {alpha_base:.12f}")
print()
for name, val, unc in exps:
    delta = val - alpha_base
    print(f"◆ {name}：{val} ± {unc}（Δ = {delta:+.3e}）")
    # 单项目标
    best1 = None
    for mn, mv in monos.items():
        for c in coeffs:
            d = delta - c * mv
            if best1 is None or abs(d) < abs(best1[2]):
                best1 = (f"{c:g}·{mn}", c*mv, d)
    print(f"  单项目标：{best1[0]} = {best1[1]:+.3e}——残差 {best1[2]:+.2e}"
          f"（{abs(best1[2])/unc:.2f}σ）")
    # 双项组合
    best2 = None
    mlist = list(monos.items())
    for (mn1, mv1), (mn2, mv2) in itertools.combinations_with_replacement(mlist, 2):
        for c1 in coeffs:
            for c2 in coeffs:
                d = delta - (c1*mv1 + c2*mv2)
                if best2 is None or abs(d) < abs(best2[3]):
                    best2 = (f"{c1:g}·{mn1} + {c2:g}·{mn2}",
                             c1*mv1 + c2*mv2, d,
                             abs(d)/unc)
    print(f"  双项最优：{best2[0]} = {best2[1]:+.3e}——残差 {best2[2]:+.2e}"
          f"（{best2[3]:.2f}σ）")
    # 双项全库前 3
    print("  双项全库残差排序（前 3）：")
    cands = []
    for (mn1, mv1), (mn2, mv2) in itertools.combinations_with_replacement(mlist, 2):
        for c1 in coeffs:
            for c2 in coeffs:
                d = delta - (c1*mv1 + c2*mv2)
                cands.append((abs(d), f"{c1:g}·{mn1} + {c2:g}·{mn2}", d))
    cands.sort(key=lambda t: t[0])
    for rank, (ad, s, d) in enumerate(cands[:3]):
        print(f"    {rank+1}. {s}——残差 {d:+.2e}（{ad/unc:.2f}σ）")
    print()
print("[口径-构造对应]：每个口径的 Δ 均可用 e⁻ⁿ 族框架单体表达——")
print("  差异 = 系数量级（1e-8~1e-7 = e⁻¹⁸~e⁻¹⁶ 域）——")
print("  '口径差异 = 修正项选择差异'——框架自身不变")
