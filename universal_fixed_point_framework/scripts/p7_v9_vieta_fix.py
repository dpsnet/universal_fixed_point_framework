# -*- coding: utf-8 -*-
"""修正 ActiveSilentVieta.lean 的 V9 段：
v1.2 陈述 "sigma_inv in [1,64] 唯一使判别式为完全平方" 为假（sigma_inv=16 重根反例 D=0）。
改为：根互异条件下唯一解 = 15，并显式登记 16 为重根反例、15 为正向见证。
原 `interval_cases sigma_inv with hsigma` 不是合法语法（上界分支也不足 64 case）。
"""
import io, sys, shutil, os

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\ActiveSilentVieta.lean"

START = "/-- ★★ V9：当 k_max = 2^3 = 8 时"
END = "/-- V9 推论：方案 B"

NEW = '''/-- ★★ V9（v1.3 修正，评审 #1 处置 + 本轮自检）：韦达判别式的族内唯一性。

    修正要点：v1.2 陈述 "σ⁻¹ ∈ [1,64] 唯一使判别式 k_max² − 4σ⁻¹ 为完全平方"
    含反例 σ⁻¹ = 16：a = b = 4 给出 a+b = 8、a·b = 16、D = 64 − 64 = 0 = 0²，
    但 16 ≠ 15。故正确命题必须附加"根互异"（a ≠ b）——重根分支被排除后，
    σ⁻¹ ∈ [1,64] 的唯一解是 σ⁻¹ = 15（根 {3,5}，D = 4 = 2²）。
    原证明行 `interval_cases σ_inv with hσ` 亦非合法语法（interval_cases 无 with 形式）。 -/
theorem vieta_discriminant_unique_distinct :
    ∀ σ : ℕ, 1 ≤ σ → σ ≤ 64 →
    (∃ a b : ℕ, a + b = 8 ∧ a * b = σ ∧ a ≠ b) →
    (∃ d : ℤ, (8 : ℤ) ^ 2 - 4 * (σ : ℤ) = d ^ 2) → σ = 15 := by
  intro σ h1 h64 hab _
  interval_cases σ <;>
    (rcases hab with ⟨a, b, ha, hb, hne⟩
     have h8 : a ≤ 8 := by omega
     interval_cases a <;> omega)

/-- ★★ V9 反例登记：σ⁻¹ = 16 满足 a+b = 8、a·b = 16（重根 a = b = 4）且 D = 0 = 0²，
    但 16 ≠ 15。这是 v1.2 定理陈述的反例，v1.3 以"根互异"条件显式排除之。 -/
theorem vieta_discriminant_sixteen_counterexample :
    (∃ a b : ℕ, a + b = 8 ∧ a * b = 16 ∧ a = b) ∧
    (∃ d : ℤ, (8 : ℤ) ^ 2 - 4 * (16 : ℤ) = d ^ 2) ∧ (16 : ℕ) ≠ 15 := by
  refine ⟨⟨4, 4, by norm_num, by norm_num, rfl⟩, ⟨0, by norm_num⟩, by norm_num⟩

/-- ★★ V9 正向见证：σ⁻¹ = 15 时 a+b = 8、a·b = 15 有互异整数根 {3,5}，D = 4 = 2²。 -/
theorem vieta_discriminant_fifteen_witness :
    (∃ a b : ℕ, a + b = 8 ∧ a * b = 15 ∧ a ≠ b) ∧
    (∃ d : ℤ, (8 : ℤ) ^ 2 - 4 * (15 : ℤ) = d ^ 2) := by
  refine ⟨⟨3, 5, by norm_num, by norm_num, by norm_num⟩, ⟨2, by norm_num⟩⟩

'''

def main():
    with io.open(P, "r", encoding="utf-8") as f:
        s = f.read()
    i = s.find(START)
    j = s.find(END)
    if i < 0 or j < 0 or j < i:
        print("ANCHOR-FAIL", i, j); sys.exit(2)
    old = s[i:j]
    print("old-block chars:", len(old), "lines:", old.count("\n"))
    s2 = s[:i] + NEW + s[j:]
    shutil.copy2(P, os.environ.get("TEMP", ".") + r"\ActiveSilentVieta_v12_backup.lean")
    with io.open(P, "w", encoding="utf-8", newline="\n") as f:
        f.write(s2)
    print("new file bytes:", len(s2))
    print("OK")

main()
