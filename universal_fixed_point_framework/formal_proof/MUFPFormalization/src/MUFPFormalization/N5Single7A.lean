/-
# N5Single7A.lean

Phase 72 剩余③：14 单因子模式之一的具体定理（hx=s234 类代表）。

模式 tuple = (-1,-1,1,1,-1,-1,1,-1)（列 7 单因子 E7）：
  s12=s23=s51=s1234=-1；s34=s45=s123=s234=+1；hx=sg([λ₂₃,λ₄])=+1（=s234）
判据（Paper 58 附录 B）：E7=-1 ⇒ A_BG=+1；E7=+1 ⇒ A_BG=0。
本文件：E7=-1 分支定理（8 分割符号和 = +1）。

贡献结构（通用判定器 n5_single14_analytic.py 先证伪 48 组合 0 违反）：
  c123_4 = 0：Ā₍₂₃₄₎ ratio₁=hx·s34=+1 → θ⁺=0（r₀=s234·s23=-1、r₁=+1 异号）
  c1_234 = -1：PT̂=-s12=+1（E-a）；Ā₍₃₄₅₎ r₀=E6·s34=-1、r₁=E7·s45=-1 → -s34·s45=-1
  c1_2_3_4 = 0：r=(s23·s12, s34·s123, s45·s51)=(1,-1,-1) 异号（L1）
  其余 5 项 = 0（单块 PT̂=0 / 2 元素块 Ā=0）
依赖：N5HardModeA（c_defs 参数化定义）+ N5ProjectionOrder（hx 兑现，可选）。
零 sorry 目标。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import MUFPFormalization.N5HardModeA

namespace N5Single7A

open N5Criterion N5BranchSym N5SingleTermIdentities N5HardModeA SingleMinusAmplitude

/-- c123_4 = 0：Ā₍₂₃₄₎ 的 ratio₁ = hx·s34 = +1 → θ⁺=0 -/
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
  have hpt : PThat_sym [sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))]
      [ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
        (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))] = 1 := by
    have hd : sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5))) = -1 := by
      rw [bk_2_345_eq_12 w z h_sum h_mom]
      exact h_s12
    unfold PThat_sym ratio_sym
    rw [hd]
    simp [thetaP, thetaM]
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

/-- c1_2_3_4 = 0：PT̂=0（L1，r=(1,-1,-1) 异号） -/
lemma c1_2_3_4_zero (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (h_s12 : sgn (bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5))) = -1)
    (h_s23 : sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (h_s45 : sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = 1)
    (h_s51 : sgn (bk w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5))) = -1)
    (h_s123 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5))) = -1) :
    c1_2_3_4 w z = 0 := by
  unfold c1_2_3_4
  have hr0 : ratio_sym (bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)))
      (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = 1 := by
    unfold ratio_sym
    rw [bk_2_345_eq_12 w z h_sum h_mom, h_s12, h_s23]
    norm_num
  have hr1 : ratio_sym (bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)))
      (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1 := by
    unfold ratio_sym
    rw [bk_23_45_eq_1_23 w z h_sum h_mom, h_s123, h_s34]
    norm_num
  have hr2 : ratio_sym (bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)))
      (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1 := by
    unfold ratio_sym
    rw [bk_234_5_eq_51 w z h_sum h_mom, h_s51, h_s45]
    norm_num
  rw [hr0, hr1, hr2]
  apply PThat_sym_mixed_zero
  · simp
  · simp

/-- 模式 (-1,-1,1,1,-1,-1,1,-1) 列 7：E7=-1 ⇒ A_BG = +1 -/
theorem single7_mode_ABG_eq_one (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (h_s12 : sgn (bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5))) = -1)
    (h_s23 : sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (h_s45 : sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = 1)
    (h_s51 : sgn (bk w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5))) = -1)
    (h_s123 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5))) = -1)
    (h_s234 : sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5))) = 1)
    (_h_s1234 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2, 3} : Finset (Fin 5))) = -1)
    (h_e6 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5))) = -1)
    (h_e7 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2, 3} : Finset (Fin 5))) = -1)
    (h_extra : sgn (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1)
    (A1234 : ℤ) :
    -(c1234 A1234 + c123_4 w z + c12_34 w z + c12_3_4 w z + c1_234 w z +
      c1_23_4 w z + c1_2_34 w z + c1_2_3_4 w z) = 1 := by
  rw [c1234_zero A1234, c123_4_zero w z h_s23 h_s34 h_s234 h_extra,
      c12_34_zero, c12_3_4_zero,
      c1_234_contrib w z h_sum h_mom h_s12 h_s34 h_s45 h_e6 h_e7,
      c1_23_4_zero, c1_2_34_zero,
      c1_2_3_4_zero w z h_sum h_mom h_s12 h_s23 h_s34 h_s45 h_s51 h_s123]
  norm_num

end N5Single7A
