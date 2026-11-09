# -*- coding: utf-8 -*-
"""V9 段第二次修正：v1.2 陈述（σ⁻¹∈[1,64] 唯一）为假，且"根互异"也不足以救
（σ⁻¹=7 → {1,7}、12 → {2,6} 亦满足判别式平方）。唯一性只能在
σ⁻¹ = 2^{N+1}−1 的参数族内陈述。故 Lean 侧只保留可机的真断言：
D(N) 12 项具体值、N=3 见证、族外反例登记；全枚举唯一性登记为待补。
"""
import io, sys, os

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\ActiveSilentVieta.lean"

START = "/-- ★★ V9（v1.3 修正，评审 #1 处置 + 本轮自检）：韦达判别式的族内唯一性。"
END = "/-- V9 推论：方案 B"

NEW = '''/-- ★★ V9（v1.3 修正，评审 #1 处置 + 本轮自检）：真实判别式族
    D(N) = 4^N − 2^{N+3} + 4（对应 k_max = 2^N、σ⁻¹ = 2^{N+1} − 1）。

    修正历史（两级）：
    (1) v1.2 原陈述"σ⁻¹ ∈ [1,64] 唯一使判别式 k_max² − 4σ⁻¹ 为完全平方"为**假**：
        σ⁻¹ = 7（根 {1,7}，D = 36 = 6²）、σ⁻¹ = 12（根 {2,6}，D = 16 = 4²）、
        σ⁻¹ = 16（根 {4,4}，D = 0 = 0²）都给整数根且判别式为完全平方。
    (2) 因此唯一性只能在 σ⁻¹ = 2^{N+1}−1 的参数族**内**陈述（族内唯一解 = N = 3）。
        该族内全枚举（N = 1..12 逐一排除非平方）尚未机检，登记为待补（§12.4 项 3）。

    本文件机检的是可判定的三部分：D(N) 的 12 项具体值、N = 3 见证、族外反例。 -/

/-- V9-a：D(N) = 4^N − 2^{N+3} + 4 在 N = 1..12 的具体值（算术恒等，机检）。 -/
theorem vieta_discriminant_family_values :
    (4 : ℤ)^1 - (2 : ℤ)^4 + 4 = -8 ∧
    (4 : ℤ)^2 - (2 : ℤ)^5 + 4 = -12 ∧
    (4 : ℤ)^3 - (2 : ℤ)^6 + 4 = 4 ∧
    (4 : ℤ)^4 - (2 : ℤ)^7 + 4 = 132 ∧
    (4 : ℤ)^5 - (2 : ℤ)^8 + 4 = 772 ∧
    (4 : ℤ)^6 - (2 : ℤ)^9 + 4 = 3588 ∧
    (4 : ℤ)^7 - (2 : ℤ)^10 + 4 = 15364 ∧
    (4 : ℤ)^8 - (2 : ℤ)^11 + 4 = 63492 ∧
    (4 : ℤ)^9 - (2 : ℤ)^12 + 4 = 258052 ∧
    (4 : ℤ)^10 - (2 : ℤ)^13 + 4 = 1040388 ∧
    (4 : ℤ)^11 - (2 : ℤ)^14 + 4 = 4177924 ∧
    (4 : ℤ)^12 - (2 : ℤ)^15 + 4 = 16744452 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num,
          by norm_num, by norm_num, by norm_num, by norm_num, by norm_num,
          by norm_num, by norm_num⟩

/-- V9-b：N = 3 见证——D(3) = 4 = 2²，韦达根 {3,5} 互异。 -/
theorem vieta_discriminant_mersenne_witness :
    (∃ d : ℤ, (4 : ℤ)^3 - (2 : ℤ)^6 + 4 = d ^ 2) ∧
    (∃ a b : ℕ, a + b = 8 ∧ a * b = 15 ∧ a ≠ b) := by
  refine ⟨⟨2, by norm_num⟩, ⟨3, 5, by norm_num, by norm_num, by norm_num⟩⟩

/-- V9-c 族外反例登记：σ⁻¹ = 7（{1,7}，D = 36 = 6²）、12（{2,6}，D = 16 = 4²）、
    16（{4,4} 重根，D = 0 = 0²）都满足整数根 + 判别式完全平方，
    故"σ⁻¹ ∈ [1,64] 唯一"不成立；唯一性只在 Mersenne 参数族内成立。 -/
theorem vieta_discriminant_out_of_family_counterexamples :
    (∃ a b : ℕ, a + b = 8 ∧ a * b = 7 ∧ a ≠ b) ∧
    (∃ d : ℤ, (8 : ℤ) ^ 2 - 4 * 7 = d ^ 2) ∧
    (∃ a b : ℕ, a + b = 8 ∧ a * b = 12 ∧ a ≠ b) ∧
    (∃ d : ℤ, (8 : ℤ) ^ 2 - 4 * 12 = d ^ 2) ∧
    (∃ a b : ℕ, a + b = 8 ∧ a * b = 16 ∧ a = b) ∧
    (∃ d : ℤ, (8 : ℤ) ^ 2 - 4 * 16 = d ^ 2) := by
  refine ⟨⟨1, 7, by norm_num, by norm_num, by norm_num⟩, ⟨6, by norm_num⟩,
          ⟨2, 6, by norm_num, by norm_num, by norm_num⟩, ⟨4, by norm_num⟩,
          ⟨4, 4, by norm_num, by norm_num, rfl⟩, ⟨0, by norm_num⟩⟩

'''

def main():
    with io.open(P, "r", encoding="utf-8") as f:
        s = f.read()
    i = s.find(START); j = s.find(END)
    if i < 0 or j < 0 or j < i:
        print("ANCHOR-FAIL", i, j); sys.exit(2)
    print("old-block lines:", s[i:j].count("\n"))
    s2 = s[:i] + NEW + s[j:]
    with io.open(P, "w", encoding="utf-8", newline="\n") as f:
        f.write(s2)
    print("bytes:", len(s2), "OK")

main()
