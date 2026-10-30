/-
# N5HardModeA.lean

Phase 72：困难模式 A 的单非零项具体定理（推论 5.2 第 1 步的机器证明）

定理：困难模式 A（8sg 符号值）+ 非零条件 E6=E7=-1 + 1 条投影序事实
      sg([λ₂₃,λ₄])=+1（h_extra）⇒ A_BG（8 分割符号和）= +1。

A_BG = -Σ₈ c_p，8 个分割贡献（粒子 2..5 的有序分割，0-based 块）：
  c1234   单块：PT̂_sym [] [] = 0（V=Ṽ=1）
  c123_4  粒子 234|5：Ā₍₂₃₄₎=0（三分割 ratio₁=+1 → θ⁺=0）
  c12_34  粒子 23|45：Ā(23)=Ā(45)=0（2 元素块定义）
  c12_3_4 粒子 23|4|5：Ā(23)=0
  c1_234  粒子 2|345（活）：PT̂=-s12（E-a）、Ā₍₃₄₅₎=-s34·s45（L4）→ 贡献 -1
  c1_23_4 粒子 2|34|5：Ā(34)=0
  c1_2_34 粒子 2|3|45：Ā(45)=0
  c1_2_3_4 粒子 2|3|4|5：PT̂=0（L1，ratios=(1,1,-1)）

依赖：N5BranchSym（符号引擎 L1/L2）、N5SingleTermIdentities（E-a/E-b/E-c）、
      N5Criterion（bk、推论 5.3 C0/C1）。先证伪已过（n5_branch_symbol_falsify.py 55 样本）。
零 sorry 目标。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import MUFPFormalization.N5BranchSym
import MUFPFormalization.N5SingleTermIdentities

namespace N5HardModeA

open N5Criterion N5BranchSym N5SingleTermIdentities SingleMinusAmplitude

-- ==================== 定义 ====================

/-- ratio 的符号（= sgn(num)·sgn(d)，d≠0 时等价于 sgn(num/d)） -/
noncomputable def ratio_sym (num d : ℝ) : ℤ := sgn num * sgn d

/-- Ā：|S|=1 → 1 -/
def Ambar1 : ℤ := 1

/-- Ā：|S|=2 → 0 -/
def Ambar2 : ℤ := 0

/-- Ā：|S|=3 → -V_sym⁺（唯一三分割）= -(∏sg)·(∏θ⁺) -/
def Ambar3 (sgds ratios : List ℤ) : ℤ := -(List.prod sgds * List.prod (ratios.map thetaP))

-- 8 个分割贡献（粒子 2..5 的有序分割，0-based 块 = 相对索引 1..4）

/-- c1234：单块（V=Ṽ=1 → PT̂=0，Ā₍₂₃₄₅₎ 任意） -/
noncomputable def c1234 (A1234 : ℤ) : ℤ :=
  PThat_sym [] [] * A1234

/-- c123_4：粒子 234|5 -/
noncomputable def c123_4 (w z : Fin 5 → ℝ) : ℤ :=
  PThat_sym [sgn (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
            [ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
                       (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
    * Ambar3 [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
              sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5)))]
             [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)))
                        (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
              ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5)))
                        (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5)))]
    * Ambar1

/-- c12_34：粒子 23|45 -/
noncomputable def c12_34 (w z : Fin 5 → ℝ) : ℤ :=
  PThat_sym [sgn (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))]
            [ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
                       (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))]
    * Ambar2 * Ambar2

/-- c12_3_4：粒子 23|4|5 -/
noncomputable def c12_3_4 (w z : Fin 5 → ℝ) : ℤ :=
  PThat_sym [sgn (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
             sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
            [ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
                       (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
             ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
                       (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
    * Ambar2 * Ambar1 * Ambar1

/-- c1_234：粒子 2|345（活分割） -/
noncomputable def c1_234 (w z : Fin 5 → ℝ) : ℤ :=
  PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))]
            [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
                       (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))]
    * Ambar1
    * Ambar3 [sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
              sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
             [ratio_sym (bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
                        (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
              ratio_sym (bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
                        (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]

/-- c1_23_4：粒子 2|34|5 -/
noncomputable def c1_23_4 (w z : Fin 5 → ℝ) : ℤ :=
  PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
             sgn (bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
            [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
                       (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
             ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
                       (bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
    * Ambar1 * Ambar2 * Ambar1

/-- c1_2_34：粒子 2|3|45 -/
noncomputable def c1_2_34 (w z : Fin 5 → ℝ) : ℤ :=
  PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
             sgn (bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))]
            [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
                       (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
             ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
                       (bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))]
    * Ambar1 * Ambar1 * Ambar2

/-- c1_2_3_4：粒子 2|3|4|5 -/
noncomputable def c1_2_3_4 (w z : Fin 5 → ℝ) : ℤ :=
  PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
             sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
             sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
            [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
                       (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
             ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
                       (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
             ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
                       (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]

-- ==================== 每分割贡献 ====================

/-- c1234 = 0：单块 PT̂=0（V=Ṽ=1 → 空积差 0） -/
lemma c1234_zero (A1234 : ℤ) : c1234 A1234 = 0 := by
  simp [c1234, PThat_sym]

/-- c123_4 = 0：Ā₍₂₃₄₎=0（三分割 ratio₁=sg([λ₂₃,λ₄])/s₃₄ = +1 → θ⁺=0） -/
lemma c123_4_zero (w z : Fin 5 → ℝ)
    (h_s23 : sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (h_s234 : sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5))) = 1)
    (h_extra : sgn (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1) :
    c123_4 w z = 0 := by
  unfold c123_4
  have hr0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1 := by
    unfold ratio_sym
    rw [h_s234, h_s23]
    norm_num
  have hr1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1 := by
    unfold ratio_sym
    rw [h_extra, h_s34]
    norm_num
  have hamb : Ambar3 [sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
      sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5)))]
      [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)))
        (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))),
       ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5)))
        (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5)))] = 0 := by
    unfold Ambar3
    rw [hr0, hr1]
    simp [thetaP, h_s23, h_s34]
  rw [hamb]
  simp [Ambar1]

/-- c12_34 = 0：Ā(23)=Ā(45)=0（2 元素块定义） -/
lemma c12_34_zero : c12_34 w z = 0 := by
  simp [c12_34, Ambar2]

/-- c12_3_4 = 0：Ā(23)=0 -/
lemma c12_3_4_zero : c12_3_4 w z = 0 := by
  simp [c12_3_4, Ambar2]

/-- c1_234 = -1：活分割（PT̂=-s12、Ā₍₃₄₅₎=-s34·s45） -/
lemma c1_234_contrib (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (h_s12 : sgn (bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5))) = -1)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (h_s45 : sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = 1)
    (h_e6 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5))) = -1)
    (h_e7 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2, 3} : Finset (Fin 5))) = -1) :
    c1_234 w z = -1 := by
  unfold c1_234
  -- PT̂ = -sgn([λ₂,λ₃₄₅]) = -s12（E-a）
  have hpt : PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))]
      [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
        (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))] = 1 := by
    have hd : sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5))) = -1 := by
      rw [bk_2_345_eq_12 w z h_sum h_mom]
      exact h_s12
    unfold PThat_sym ratio_sym
    rw [hd]
    simp [thetaP, thetaM]
  -- Ā₍₃₄₅₎ = -s34·s45（L4，r₁=r₂=-1 ⟺ E6/E7）
  have hr0 : ratio_sym (bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1 := by
    unfold ratio_sym
    rw [corollary53_c0_eq_e6 w z h_sum h_mom, h_e6, h_s34]
    norm_num
  have hr1 : ratio_sym (bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1 := by
    unfold ratio_sym
    rw [corollary53_c1_eq_e7 w z h_sum h_mom, h_e7, h_s45]
    norm_num
  have hamb : Ambar3 [sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
      sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))]
      [ratio_sym (bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
        (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))),
       ratio_sym (bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
        (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))] = -1 := by
    unfold Ambar3
    rw [hr0, hr1]
    simp [thetaP, h_s34, h_s45]
  rw [hpt, hamb]
  simp [Ambar1]

/-- c1_23_4 = 0：Ā(34)=0 -/
lemma c1_23_4_zero : c1_23_4 w z = 0 := by
  simp [c1_23_4, Ambar2]

/-- c1_2_34 = 0：Ā(45)=0 -/
lemma c1_2_34_zero : c1_2_34 w z = 0 := by
  simp [c1_2_34, Ambar2]

/-- c1_2_3_4 = 0：PT̂=0（L1，ratios=(1,1,-1) 异号） -/
lemma c1_2_3_4_zero (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (h_s12 : sgn (bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5))) = -1)
    (h_s23 : sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (h_s45 : sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = 1)
    (h_s51 : sgn (bk w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5))) = -1)
    (h_s123 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5))) = 1) :
    c1_2_3_4 w z = 0 := by
  unfold c1_2_3_4
  -- ratio₀ = s12/s23 = +1（E-a）
  have hr0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = 1 := by
    unfold ratio_sym
    rw [bk_2_345_eq_12 w z h_sum h_mom, h_s12, h_s23]
    norm_num
  -- ratio₁ = s123/s34 = +1（E-b）
  have hr1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1 := by
    unfold ratio_sym
    rw [bk_23_45_eq_1_23 w z h_sum h_mom, h_s123, h_s34]
    norm_num
  -- ratio₂ = s51/s45 = -1（E-c）
  have hr2 : ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1 := by
    unfold ratio_sym
    rw [bk_234_5_eq_51 w z h_sum h_mom, h_s51, h_s45]
    norm_num
  rw [hr0, hr1, hr2]
  apply PThat_sym_mixed_zero
  · simp
  · simp

-- ==================== 主定理：困难模式 A ⇒ A_BG = +1 ====================

/-- 困难模式 A（8sg 符号值 + E6=E7=-1 + 投影序事实 h_extra）⇒ A_BG = +1。
   注：s1234 不参与单非零项推导（只用于模式等价类识别），列作 _h_s1234。 -/
theorem hard_mode_A_ABG_eq_one (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (h_s12 : sgn (bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5))) = -1)
    (h_s23 : sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (h_s45 : sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = 1)
    (h_s51 : sgn (bk w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5))) = -1)
    (h_s123 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5))) = 1)
    (h_s234 : sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5))) = 1)
    (_h_s1234 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2, 3} : Finset (Fin 5))) = -1)
    (h_e6 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5))) = -1)
    (h_e7 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2, 3} : Finset (Fin 5))) = -1)
    (h_extra : sgn (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (A1234 : ℤ) :
    -(c1234 A1234 + c123_4 w z + c12_34 w z + c12_3_4 w z + c1_234 w z +
      c1_23_4 w z + c1_2_34 w z + c1_2_3_4 w z) = 1 := by
  rw [c1234_zero A1234, c123_4_zero w z h_s23 h_s34 h_s234 h_extra,      c12_34_zero, c12_3_4_zero,
      c1_234_contrib w z h_sum h_mom h_s12 h_s34 h_s45 h_e6 h_e7,
      c1_23_4_zero, c1_2_34_zero,
      c1_2_3_4_zero w z h_sum h_mom h_s12 h_s23 h_s34 h_s45 h_s51 h_s123]
  norm_num

end N5HardModeA
