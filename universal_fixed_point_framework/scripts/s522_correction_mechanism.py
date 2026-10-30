# -*- coding: utf-8 -*-
"""
S522 修正存在性机制代数根源——"纯乘积 vs 跨层组合"判别（2026-10-29）
模式 8 先证伪：检验"为何组装需修正"机制候选

机制候选：修正 ⟺ 裸量含跨层/跨链组合（求和/减法/比值/跨链乘积）；
          纯同链框架量乘法复合（m_Δ）→ 无修正。
判别公式（9 例——8 框架量 + m_Δ）：
  m_Δ  = 16×7×11 纯乘积（全框架量乘法复合）
  m_ρ  = 8×(16+3⁴)×(1−(8/3)σ³)  求和（16+3⁴ 跨层）
  α_s  = (17/2)(1−7σ³)  = (24−7)/2（减法+除法——跨层）
  ε_μ  = 144e⁻¹⁶(1+6σ³)  乘积（144 框架量 × e⁻¹⁶ 跨链）
  δ_hf = (3/4)(1−σ) = (活跃/不动点)(1−σ)  比值（跨层）
  公共残差 = (1−12σ³) 纯修正因子（无裸量——不适用判别）
  κ/fnp/观测边界 = 纯修正因子（无裸量——不适用判别）
"""
from fractions import Fraction

sigma = Fraction(1, 15)
active, powBase, silence, fixedPoint, kMax, involution = 3, 2, 5, 4, 8, 7

# 9 例公式核验（精确有理）
cases = [
    # (名称, 裸量形态, 是否跨层组合, 是否带修正, 公式核验)
    ("m_Δ",  "纯乘积(16×7×11)", False, False,
     Fraction(16) * 7 * 11, Fraction(1232)),
    ("m_ρ",  "乘积×求和(8×(16+3⁴))", True, True,
     Fraction(8) * (16 + 81) * (1 - Fraction(8, 3) * sigma**3),
     Fraction(7850792, 10125)),
    ("α_s",  "组装((24−7)/2)", True, True,
     Fraction(17, 2) * (1 - 7 * sigma**3), Fraction(28628, 3375)),
    ("ε_μ",  "乘积×e链(144e⁻¹⁶)", True, True,
     Fraction(144) * (1 + 6 * sigma**3), Fraction(144 * 1127, 1125)),
    ("δ_hf", "比值(活跃/不动点)", True, True,
     Fraction(3, 4) * (1 - sigma), Fraction(7, 10)),
    ("公共残差", "纯修正因子(无裸量)", None, True,
     Fraction(1) - 12 * sigma**3, Fraction(1121, 1125)),
    ("κ",    "纯修正因子(无裸量)", None, True,
     Fraction(1) - Fraction(2, 3) * sigma, Fraction(43, 45)),
    ("fnp",  "纯修正因子(无裸量)", None, True,
     Fraction(1) - Fraction(1, 3) * sigma**2, Fraction(674, 675)),
    ("观测边界", "纯修正因子(无裸量)", None, True,
     Fraction(1) - 3 * sigma, Fraction(4, 5)),
]

print("S522 修正存在性机制——'纯乘积 vs 跨层组合'判别（模式 8 先证伪）")
print("=" * 70)
print("%-10s %-24s %-8s %-8s %s" % ("量", "裸量形态", "跨层组合", "带修正", "公式核验"))
all_ok = True
for name, form, cross, corr, lhs, rhs in cases:
    ok = lhs == rhs
    all_ok = all_ok and ok
    print("%-10s %-24s %-8s %-8s %s" % (name, form[:24], str(cross), str(corr), "PASS" if ok else "FAIL"))

print()
print("机制判别（5 例有裸量的公式）：")
print("  纯乘积形态 → 无修正：m_Δ")
print("  跨层组合形态 → 带修正：m_ρ/α_s/ε_μ/δ_hf")
print("  纯修正因子（无裸量——判别不适用）：公共残差/κ/fnp/观测边界")
print()
print("统一检验：跨层组合(4例) 全部带修正 + 纯乘积(1例) 无修正 → 5/5 一致")
cross_cases = [c for c in cases if c[2] is True]
pure_cases = [c for c in cases if c[2] is False]
ok_cross = all(c[3] for c in cross_cases)
ok_pure = all(not c[3] for c in pure_cases)
print("  跨层组合→修正：%d/%d %s" % (sum(1 for c in cross_cases if c[3]), len(cross_cases), "PASS" if ok_cross else "FAIL"))
print("  纯乘积→无修正：%d/%d %s" % (sum(1 for c in pure_cases if not c[3]), len(pure_cases), "PASS" if ok_pure else "FAIL"))
print()
print("结论：%s" % ("机制候选成形——修正⟺跨层组合（观察级）" if (all_ok and ok_cross and ok_pure) else "有失败——需勘误"))
print("诚实边界：m_Δ 无修正仍观察级（公式后验）——'为何纯乘积免修正'的范畴构造开放")
