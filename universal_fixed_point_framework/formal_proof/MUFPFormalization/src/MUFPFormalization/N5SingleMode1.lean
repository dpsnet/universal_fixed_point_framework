/-
# N5SingleMode1.lean

Phase 72 剩余③：14 单因子模式之三——全死型代表。

模式 tuple = (-1,-1,-1,-1,1,1,-1,1)（列 6 单因子 E6）：
  s12=s23=s34=s45=s234=s1234=-1；s51=s123=+1；hx=-1（=s234，但证明不需要 hx）
判据：E6=-1 ⇒ A_BG=0；E6=+1 ⇒ A_BG=+1。本文件：E6=-1 分支（A_BG=0）。

贡献结构（通用判定器先证伪）：全部 8 项 = 0——
  c123_4=0：Ā₍₂₃₄₎ r₀=s234·s23=+1 → θ⁺=0（M1，r₁ 自由）
  c1_234=0：Ā₍₃₄₅₎ r₁=E7·s45=+1 → θ⁺=0（M3，E6 判据熄灭处 r₀ 自由）
  c1_2_3_4=0：r=(s23·s12, s34·s123, s45·s51)=(1,-1,-1) 异号（L1）
依赖：N5SingleLemmas（M1/M3 机制）。零 sorry 目标。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import MUFPFormalization.N5SingleLemmas

namespace N5SingleMode1

open N5Criterion N5BranchSym N5SingleTermIdentities N5HardModeA N5SingleLemmas SingleMinusAmplitude

/-- c123_4=0：r₀=s234·s23=+1（M1） -/
lemma c123_4_zero (w z : Fin 5 → ℝ)
    (h_s23 : sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (h_s234 : sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5))) = -1) :
    c123_4 w z = 0 := by
  apply c123_4_zero_of_r0_pos
  unfold ratio_sym
  rw [h_s234, h_s23]
  norm_num

/-- c1_234=0：r₀=E6·s34=+1（M4-r0 熄灭；本模式 E7 固定=+1，判据 E6 分支） -/
lemma c1_234_zero (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1)
    (h_e6 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5))) = -1) :
    c1_234 w z = 0 := by
  apply c1_234_zero_of_r0_pos
  unfold ratio_sym
  rw [corollary53_c0_eq_e6 w z h_sum h_mom, h_e6, h_s34]
  norm_num

/-- c1_2_3_4=0：r=(1,-1,-1) 异号（L1） -/
lemma c1_2_3_4_zero (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (h_s12 : sgn (bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5))) = -1)
    (h_s23 : sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1)
    (h_s45 : sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1)
    (h_s51 : sgn (bk w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5))) = 1)
    (h_s123 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5))) = 1) :
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

/-- 模式 (-1,-1,-1,-1,1,1,-1,1) 列 6：E6=-1 ⇒ A_BG = 0 -/
theorem mode1_ABG_eq_zero (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (h_s12 : sgn (bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5))) = -1)
    (h_s23 : sgn (bk w z ({1} : Finset (Fin 5)) ({2} : Finset (Fin 5))) = -1)
    (h_s34 : sgn (bk w z ({2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1)
    (h_s45 : sgn (bk w z ({3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) = -1)
    (h_s51 : sgn (bk w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5))) = 1)
    (h_s123 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5))) = 1)
    (h_s234 : sgn (bk w z ({1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5))) = -1)
    (_h_s1234 : sgn (bk w z ({0} : Finset (Fin 5)) ({1, 2, 3} : Finset (Fin 5))) = 1)
    (h_e6 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5))) = -1)
    (_h_e7 : sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2, 3} : Finset (Fin 5))) = 1)
    (A1234 : ℤ) :
    -(c1234 A1234 + c123_4 w z + c12_34 w z + c12_3_4 w z + c1_234 w z +
      c1_23_4 w z + c1_2_34 w z + c1_2_3_4 w z) = 0 := by
  rw [c1234_zero A1234, c123_4_zero w z h_s23 h_s234,
      c12_34_zero, c12_3_4_zero,
      c1_234_zero w z h_sum h_mom h_s34 h_e6,
      c1_23_4_zero, c1_2_34_zero,
      c1_2_3_4_zero w z h_sum h_mom h_s12 h_s23 h_s34 h_s45 h_s51 h_s123]
  norm_num

end N5SingleMode1
