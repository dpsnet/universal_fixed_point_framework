/-
# N5SingleLemmas.lean

Phase 72 剩余③：14 单因子模式 Lean 化的共享机制引理库。

设计：8 分割贡献的"死亡/存活机制"与模式无关，逐模式只负责
  ① 8sg 符号值假设（s12…s1234）
  ② ratio 值的推导（rw 恒等式 E-a/E-b/E-c + 推论 5.3 C0/C1 + norm_num）
本库提供机制引理（参数化），模式文件 import 本库后写模式引理与主定理。

机制一览（对应通用解析判定器 abg_predict 的 8 分割贡献公式）：
  M1  c123_4=0：Ā₍₂₃₄₎ r₀=+1 → θ⁺(r₀)=0（r₁ 自由，无需 hx）
  M2  c123_4=0：Ā₍₂₃₄₎ r₁=+1 → θ⁺(r₁)=0（r₀ 自由）
  M3  c1_234=0：Ā₍₃₄₅₎ r₁=+1 → θ⁺(r₁)=0（E6 自由）
  M4  c1_234 活：PT̂=1（E-a 定号）+ r₀=r₁=-1 → -s₃₄·s₄₅
  M5  c1_2_3_4=0：混合（rw 后 apply PThat_sym_mixed_zero）——模式引理内联
  M6  c1_2_3_4 全正（L3 r=+1）→ ∏sg·(-1)
  M7  c1_2_3_4 全负（L3 r=-1）→ ∏sg·1
零 sorry 目标。先证伪：通用解析判定器 400000 样本 48 组合 0 违反。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import MUFPFormalization.N5HardModeA

namespace N5SingleLemmas

open N5Criterion N5BranchSym N5SingleTermIdentities N5HardModeA SingleMinusAmplitude

-- ==================== M1/M2：c123_4 = 0 ====================

/-- c123_4=0：Ā₍₂₃₄₎ r₀=+1 → θ⁺(r₀)=0（r₁ 自由） -/
lemma c123_4_zero_of_r0_pos (w z : Fin 5 → ℝ)
    (h_r0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = 1) :
    c123_4 w z = 0 := by
  unfold c123_4 Ambar3
  rw [h_r0]
  simp [thetaP, thetaM, Ambar1]

/-- c123_4=0：Ā₍₂₃₄₎ r₁=+1 → θ⁺(r₁)=0（r₀ 自由） -/
lemma c123_4_zero_of_r1_pos (w z : Fin 5 → ℝ)
    (h_r1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1) :
    c123_4 w z = 0 := by
  unfold c123_4 Ambar3
  rw [h_r1]
  simp [thetaP, Ambar1]

-- ==================== M3：c1_234 = 0 ====================

/-- c1_234=0：Ā₍₃₄₅₎ r₁=+1 → θ⁺(r₁)=0（r₀=E6 项自由，E6 不出现在证明） -/
lemma c1_234_zero_of_r1_pos (w z : Fin 5 → ℝ)
    (h_r1 : ratio_sym (bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = 1) :
    c1_234 w z = 0 := by
  unfold c1_234 Ambar3
  rw [h_r1]
  simp [thetaP, Ambar1]

/-- c1_234=0：Ā₍₃₄₅₎ r₀=+1 → θ⁺(r₀)=0（r₁ 自由） -/
lemma c1_234_zero_of_r0_pos (w z : Fin 5 → ℝ)
    (h_r0 : ratio_sym (bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1) :
    c1_234 w z = 0 := by
  unfold c1_234 Ambar3
  rw [h_r0]
  simp [thetaP, Ambar1]

-- ==================== M4：c1_234 活 ====================

/-- c1_234 活：PT̂=p（E-a 定号）、Ā₍₃₄₅₎ r₀=r₁=-1 → 贡献 = p·(-s₃₄·s₄₅) -/
lemma c1_234_general (w z : Fin 5 → ℝ) (p : ℤ)
    (h_pt : PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))]
      [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
        (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))] = p)
    (h_r0 : ratio_sym (bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1)
    (h_r1 : ratio_sym (bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1) :
    c1_234 w z = p * -(sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) *
      sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))) := by
  unfold c1_234 Ambar3
  rw [h_pt, h_r0, h_r1]
  simp [thetaP, thetaM, Ambar1]

-- ==================== M5：c1_2_3_4 混合（L1）= 0 ====================

/-- c1_2_3_4=0：r=(1,-1,-1) 异号（L1） -/
lemma c1_2_3_4_mixed_1_neg_neg (w z : Fin 5 → ℝ)
    (hr0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = 1)
    (hr1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1)
    (hr2 : ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1) :
    c1_2_3_4 w z = 0 := by
  unfold c1_2_3_4
  rw [hr0, hr1, hr2]
  apply PThat_sym_mixed_zero
  · simp
  · simp

/-- c1_2_3_4=0：r=(1,1,-1) 异号（L1） -/
lemma c1_2_3_4_mixed_1_1_neg (w z : Fin 5 → ℝ)
    (hr0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = 1)
    (hr1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (hr2 : ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1) :
    c1_2_3_4 w z = 0 := by
  unfold c1_2_3_4
  rw [hr0, hr1, hr2]
  apply PThat_sym_mixed_zero
  · simp
  · simp

/-- c1_2_3_4=0：r=(-1,1,1) 异号（L1） -/
lemma c1_2_3_4_mixed_neg_1_1 (w z : Fin 5 → ℝ)
    (hr0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (hr1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (hr2 : ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = 1) :
    c1_2_3_4 w z = 0 := by
  unfold c1_2_3_4
  rw [hr0, hr1, hr2]
  apply PThat_sym_mixed_zero
  · simp
  · simp

-- ==================== M6/M7：c1_2_3_4 全同号（L3） ====================

/-- c1_2_3_4 全正（L3 r=+1）：PT̂=∏sg·(-1)，贡献 = -(s₂₃·s₃₄·s₄₅) -/
lemma c1_2_3_4_uniform_pos_pt (w z : Fin 5 → ℝ)
    (hr0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = 1)
    (hr1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (hr2 : ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = 1) :
    c1_2_3_4 w z = -(sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) *
      sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) *
      sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))) := by
  unfold c1_2_3_4
  rw [hr0, hr1, hr2]
  have hL : PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
      sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
      sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))] [1, 1, 1]
      = List.prod [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
          sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
          sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))] * -1 := by
    apply PThat_sym_uniform
    · simp
    · simp
    · simp
  rw [hL]
  simp [List.prod_cons, List.prod_nil]
  ring

/-- c1_2_3_4 全负（L3 r=-1）：PT̂=∏sg·1，贡献 = s₂₃·s₃₄·s₄₅ -/
lemma c1_2_3_4_uniform_neg_pt (w z : Fin 5 → ℝ)
    (hr0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (hr1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1)
    (hr2 : ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1) :
    c1_2_3_4 w z = sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) *
      sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) *
      sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) := by
  unfold c1_2_3_4
  rw [hr0, hr1, hr2]
  have hL : PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
      sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
      sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))] [-1, -1, -1]
      = List.prod [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
          sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
          sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))] * -(-1) := by
    apply PThat_sym_uniform
    · simp
    · simp
    · simp
  rw [hL]
  simp [List.prod_cons, List.prod_nil]
  ring

end N5SingleLemmas
