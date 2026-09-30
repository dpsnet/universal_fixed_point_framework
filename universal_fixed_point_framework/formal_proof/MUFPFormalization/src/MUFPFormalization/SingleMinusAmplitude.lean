/-
# SingleMinusAmplitude.lean

Phase 71 核心引理形式化（arXiv:2602.12176v2 单负剥离振幅）

目标：证明 n=4 时通式(39) 与显式公式(30) 在 R1 区（半共线+动量守恒）下的代数等价。

结构（分两层）：
- 引理 1 (formula_39_30_algebra)：纯代数核心——对任意整数 a,b,c,d，
  (a-b)(c-d)=0 → (a+b)(c+d) = 2(bd+ac)。[ring]
- 引理 2 (r1_momentum_sign_identity)：R1 区特有恒等式——ω₁<0, ω₂₃₄>0,
  动量守恒 Σω=0, Σωz̄=0 下 (sg_12-sg_23)(sg_34-sg_41)=0。
- 定理 n4_formula_39_eq_30_r1：组合二者得到 (39)=(30)。

记号：sg_ab = sgn(ω_a·ω_b·(z̄_a - z̄_b))。
R1 下符号简化：sg_12 = sgn(z̄_2-z̄_1)（因 ω₁<0, ω₂>0），
sg_23 = sgn(z̄_2-z̄_3)，sg_34 = sgn(z̄_3-z̄_4)，sg_41 = sgn(z̄_1-z̄_4)。

状态：全闭（零 sorry，2026-09-30 lake build 通过）。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic

namespace SingleMinusAmplitude

/-- 符号函数：x<0 → -1，x=0 → 0，x>0 → 1 -/
noncomputable def sgn (x : ℝ) : ℤ :=
  if x < 0 then -1 else if x = 0 then 0 else 1

lemma sgn_of_lt_zero {x : ℝ} (h : x < 0) : sgn x = -1 := by
  simp [sgn, h]

lemma sgn_of_eq_zero {x : ℝ} (h : x = 0) : sgn x = 0 := by
  simp [sgn, h]

lemma sgn_of_gt_zero {x : ℝ} (h : 0 < x) : sgn x = 1 := by
  have h1 : ¬ x < 0 := by linarith
  have h2 : ¬ x = 0 := by linarith
  simp [sgn, h1, h2]

lemma sgn_neg (x : ℝ) : sgn (-x) = -sgn x := by
  by_cases h0 : x = 0
  · have hx : -x = 0 := by linarith
    simp [sgn, h0, hx]
  · by_cases hx : x < 0
    · have hnot1 : ¬ -x < 0 := by linarith
      have hnot2 : ¬ -x = 0 := by linarith
      simp [sgn, hx, hnot1, hnot2]
    · have hposx : 0 < x := lt_of_le_of_ne (le_of_not_gt hx) (Ne.symm h0)
      have hneg : -x < 0 := by linarith
      simp [sgn, hx, hneg, h0]

lemma sgn_nonzero_iff_ne_zero (x : ℝ) : sgn x ≠ 0 ↔ x ≠ 0 := by
  constructor
  · intro h hx
    have : sgn x = 0 := by simp [sgn, hx]
    exact h this
  · intro hx h
    by_cases hlt : x < 0
    · have : sgn x = -1 := sgn_of_lt_zero hlt
      omega
    · have hgt : 0 < x := lt_of_le_of_ne (le_of_not_gt hlt) (Ne.symm hx)
      have : sgn x = 1 := sgn_of_gt_zero hgt
      omega

/-- 引理 1（纯代数核心）：(a-b)(c-d)=0 → (a+b)(c+d) = 2(bd+ac)。
   对应 (39)|n=4 与 (30) 的整数等价（两边同乘 4）。-/
lemma formula_39_30_algebra (a b c d : ℤ)
    (hcond : (a - b) * (c - d) = 0) :
    (a + b) * (c + d) = 2 * (b * d + a * c) := by
  have hcalc : (a + b) * (c + d) - 2 * (b * d + a * c) = -((a - b) * (c - d)) := by
    ring
  rw [hcond] at hcalc
  exact sub_eq_zero.mp hcalc

/-- 组合定理（n=4）：在恒等式前提 h_cond 下，通式(39) 与显式公式(30) 等价。
   h_cond 即 (sg_12 - sg_23)(sg_34 - sg_41) = 0。 -/
theorem n4_formula_equivalence (s12 s23 s34 s41 : ℤ)
    (h_cond : (s12 - s23) * (s34 - s41) = 0) :
    (s12 + s23) * (s34 + s41) = 2 * (s23 * s41 + s12 * s34) := by
  exact formula_39_30_algebra s12 s23 s34 s41 h_cond

/- ==================== 轮 2：R1 动量守恒恒等式 ==================== -/

/-- sgn 保持性：a>0 时 sgn(a*x) = sgn x -/
lemma sgn_mul_pos {a x : ℝ} (h : 0 < a) : sgn (a * x) = sgn x := by
  by_cases hx : x = 0
  · have hax : a * x = 0 := by rw [hx, mul_zero]
    rw [sgn_of_eq_zero hax, sgn_of_eq_zero hx]
  · by_cases hlt : x < 0
    · have hax : a * x < 0 := by nlinarith
      rw [sgn_of_lt_zero hax, sgn_of_lt_zero hlt]
    · have hgt : 0 < x := lt_of_le_of_ne (le_of_not_gt hlt) (Ne.symm hx)
      have hax : 0 < a * x := by nlinarith
      rw [sgn_of_gt_zero hax, sgn_of_gt_zero hgt]

/-- sgn 反号性：a<0 时 sgn(a*x) = -sgn x -/
lemma sgn_mul_neg {a x : ℝ} (h : a < 0) : sgn (a * x) = -sgn x := by
  by_cases hx : x = 0
  · have hax : a * x = 0 := by rw [hx, mul_zero]
    rw [sgn_of_eq_zero hax]
    rw [sgn_of_eq_zero hx, neg_zero]
  · by_cases hlt : x < 0
    · have hax : 0 < a * x := by nlinarith
      have hsx : sgn x = -1 := sgn_of_lt_zero hlt
      rw [sgn_of_gt_zero hax, hsx, neg_neg]
    · have hgt : 0 < x := lt_of_le_of_ne (le_of_not_gt hlt) (Ne.symm hx)
      have hax : a * x < 0 := by nlinarith
      have hsx : sgn x = 1 := sgn_of_gt_zero hgt
      rw [sgn_of_lt_zero hax, hsx]

/-- F1 非零 ⇒ (x,y) 同号且 |y| ≥ |x|（允许 x=0）。-/
lemma sgn_neq_of_f1 (x y : ℝ) (h : sgn x ≠ sgn (x - y)) :
    (0 < x ∧ x ≤ y) ∨ (x < 0 ∧ y ≤ x) ∨ (x = 0 ∧ y ≠ 0) := by
  by_cases hx0 : x = 0
  · right; right
    constructor
    · exact hx0
    · intro hy0
      have hs1 : sgn x = 0 := sgn_of_eq_zero hx0
      have hxy0 : x - y = 0 := by rw [hx0, hy0, sub_zero]
      have hs2 : sgn (x - y) = 0 := sgn_of_eq_zero hxy0
      exact h (by rw [hs1, hs2])
  · by_cases hxlt : x < 0
    · right; left
      constructor
      · exact hxlt
      · by_contra hxy
        have hx_lt_y : x < y := lt_of_not_ge hxy
        have hxy_neg : x - y < 0 := by linarith
        have hs1 : sgn x = -1 := sgn_of_lt_zero hxlt
        have hs2 : sgn (x - y) = -1 := sgn_of_lt_zero hxy_neg
        rw [hs1, hs2] at h
        norm_num at h
    · left
      constructor
      · exact lt_of_le_of_ne (le_of_not_gt hxlt) (Ne.symm hx0)
      · by_contra hxy
        have hy_lt_x : y < x := lt_of_not_ge hxy
        have hxy_pos : 0 < x - y := by linarith
        have hs1 : sgn x = 1 := sgn_of_gt_zero (lt_of_le_of_ne (le_of_not_gt hxlt) (Ne.symm hx0))
        have hs2 : sgn (x - y) = 1 := sgn_of_gt_zero hxy_pos
        rw [hs1, hs2] at h
        norm_num at h

/-- F2 非零 ⇒ (w,y) 同号且 |y| ≥ |w|（允许 w=0）。-/
lemma sgn_neq_of_f2 (y w : ℝ) (h : sgn (y - w) ≠ sgn (-w)) :
    (0 < w ∧ w ≤ y) ∨ (w < 0 ∧ y ≤ w) ∨ (w = 0 ∧ y ≠ 0) := by
  by_cases hw0 : w = 0
  · right; right
    constructor
    · exact hw0
    · intro hy0
      have hwneg : -w = 0 := by linarith
      have hs1 : sgn (-w) = 0 := sgn_of_eq_zero hwneg
      have hyw0 : y - w = 0 := by rw [hw0, hy0, sub_zero]
      have hs2 : sgn (y - w) = 0 := sgn_of_eq_zero hyw0
      exact h (by rw [hs1, hs2])
  · by_cases hwlt : w < 0
    · right; left
      constructor
      · exact hwlt
      · by_contra hyw
        have hw_lt_y : w < y := lt_of_not_ge hyw
        have hyw_pos : 0 < y - w := by linarith
        have hs1 : sgn (y - w) = 1 := sgn_of_gt_zero hyw_pos
        have hnegw : 0 < -w := by linarith
        have hs2 : sgn (-w) = 1 := sgn_of_gt_zero hnegw
        rw [hs1, hs2] at h
        norm_num at h
    · left
      constructor
      · exact lt_of_le_of_ne (le_of_not_gt hwlt) (Ne.symm hw0)
      · by_contra hyw
        have hy_lt_w : y < w := lt_of_not_ge hyw
        have hyw_neg : y - w < 0 := by linarith
        have hs1 : sgn (y - w) = -1 := sgn_of_lt_zero hyw_neg
        have hw_pos : 0 < w := lt_of_le_of_ne (le_of_not_gt hwlt) (Ne.symm hw0)
        have hnegw : -w < 0 := by linarith
        have hs2 : sgn (-w) = -1 := sgn_of_lt_zero hnegw
        rw [hs1, hs2] at h
        norm_num at h

/-- R1 动量守恒恒等式：ω₁<0、ω₂,ω₃,ω₄>0、Σω=0、Σωz̄=0
    ⇒ (sg_12 - sg_23)(sg_34 - sg_41) = 0。
   物理来源：动量守恒迫使 z̄₂ 与 z̄₃ 或 z̄₄ 与 z̄₃ 同侧，
   即 (31)(39) 的 R1 特有符号结构（数值验证见 T5v2/T6）。 -/
lemma r1_momentum_sign_identity
    (w1 w2 w3 w4 z1 z2 z3 z4 : ℝ)
    (h_sum : w1 + w2 + w3 + w4 = 0)
    (h_w1 : w1 < 0) (h_w2 : 0 < w2) (h_w3 : 0 < w3) (h_w4 : 0 < w4)
    (h_mom : w1 * z1 + w2 * z2 + w3 * z3 + w4 * z4 = 0) :
    (sgn (w1 * w2 * (z1 - z2)) - sgn (w2 * w3 * (z2 - z3))) *
      (sgn (w3 * w4 * (z3 - z4)) - sgn (w4 * w1 * (z4 - z1))) = 0 := by
  let x : ℝ := z2 - z1
  let y : ℝ := z3 - z1
  let w : ℝ := z4 - z1
  have h_w1w2 : w1 * w2 < 0 := by nlinarith
  have h_w2w3 : 0 < w2 * w3 := by nlinarith
  have h_w3w4 : 0 < w3 * w4 := by nlinarith
  have h_w4w1 : w4 * w1 < 0 := by nlinarith
  have hs12 : sgn (w1 * w2 * (z1 - z2)) = sgn (z2 - z1) := by
    rw [sgn_mul_neg h_w1w2]
    have hz : z2 - z1 = -(z1 - z2) := by ring
    rw [hz, sgn_neg]
  have hs23 : sgn (w2 * w3 * (z2 - z3)) = sgn (z2 - z3) := by
    rw [sgn_mul_pos h_w2w3]
  have hs34 : sgn (w3 * w4 * (z3 - z4)) = sgn (z3 - z4) := by
    rw [sgn_mul_pos h_w3w4]
  have hs41 : sgn (w4 * w1 * (z4 - z1)) = sgn (z1 - z4) := by
    rw [sgn_mul_neg h_w4w1]
    have hz : z1 - z4 = -(z4 - z1) := by ring
    rw [hz, sgn_neg]
  by_contra hprod
  have hf1_ne : sgn (w1 * w2 * (z1 - z2)) - sgn (w2 * w3 * (z2 - z3)) ≠ 0 := by
    intro hz
    apply hprod
    rw [hz, zero_mul]
  have hf2_ne : sgn (w3 * w4 * (z3 - z4)) - sgn (w4 * w1 * (z4 - z1)) ≠ 0 := by
    intro hz
    apply hprod
    rw [hz, mul_zero]
  have hf1' : sgn x ≠ sgn (x - y) := by
    have h1 : sgn (z2 - z1) ≠ sgn (z2 - z3) := by
      intro hz
      apply hf1_ne
      rw [hs12, hs23]
      rw [hz, sub_self]
    have hz23 : z2 - z3 = x - y := by dsimp [x, y]; ring
    rw [hz23] at h1
    simpa [x, y] using h1
  have hf2' : sgn (y - w) ≠ sgn (-w) := by
    have h2 : sgn (z3 - z4) ≠ sgn (z1 - z4) := by
      intro hz
      apply hf2_ne
      rw [hs34, hs41]
      rw [hz, sub_self]
    have hz34 : z3 - z4 = y - w := by dsimp [y, w]; ring
    have hz1w4 : z1 - z4 = -w := by dsimp [w]; ring
    rw [hz34, hz1w4] at h2
    simpa [y, w] using h2
  have h_mom' : w2 * x + w3 * y + w4 * w = 0 := by
    dsimp [x, y, w]
    have hw1 : w1 = -(w2 + w3 + w4) := by linarith
    calc
      w2 * (z2 - z1) + w3 * (z3 - z1) + w4 * (z4 - z1)
          = w1 * z1 + w2 * z2 + w3 * z3 + w4 * z4 := by
            rw [hw1]
            ring
      _ = 0 := h_mom
  rcases sgn_neq_of_f1 x y hf1' with hf1pos | hf1neg | hf1zero
  · rcases sgn_neq_of_f2 y w hf2' with hf2pos | hf2neg | hf2zero
    · have hx0 : 0 < x := hf1pos.1
      have hxy : x ≤ y := hf1pos.2
      have hy0 : 0 < y := lt_of_lt_of_le hx0 hxy
      have hw0 : 0 < w := hf2pos.1
      have hsum_pos : 0 < w2 * x + w3 * y + w4 * w := by nlinarith
      linarith
    · have hx0 : 0 < x := hf1pos.1
      have hxy : x ≤ y := hf1pos.2
      have hy_pos : 0 < y := lt_of_lt_of_le hx0 hxy
      have hw_neg : w < 0 := hf2neg.1
      have hyw : y ≤ w := hf2neg.2
      have hy_neg : y < 0 := lt_of_le_of_lt hyw hw_neg
      linarith
    · have hx0 : 0 < x := hf1pos.1
      have hxy : x ≤ y := hf1pos.2
      have hy_pos : 0 < y := lt_of_lt_of_le hx0 hxy
      have hw0 : w = 0 := hf2zero.1
      have hsum_pos : 0 < w2 * x + w3 * y + w4 * w := by
        rw [hw0]
        nlinarith
      linarith
  · rcases sgn_neq_of_f2 y w hf2' with hf2pos | hf2neg | hf2zero
    · have hx_neg : x < 0 := hf1neg.1
      have hxy : y ≤ x := hf1neg.2
      have hy_neg : y < 0 := lt_of_le_of_lt hxy hx_neg
      have hw0 : 0 < w := hf2pos.1
      have hwy : w ≤ y := hf2pos.2
      have hy_pos : 0 < y := lt_of_lt_of_le hw0 hwy
      linarith
    · have hx_neg : x < 0 := hf1neg.1
      have hxy : y ≤ x := hf1neg.2
      have hy_neg : y < 0 := lt_of_le_of_lt hxy hx_neg
      have hw_neg : w < 0 := hf2neg.1
      have hsum_neg : w2 * x + w3 * y + w4 * w < 0 := by nlinarith
      linarith
    · have hx_neg : x < 0 := hf1neg.1
      have hxy : y ≤ x := hf1neg.2
      have hy_neg : y < 0 := lt_of_le_of_lt hxy hx_neg
      have hw0 : w = 0 := hf2zero.1
      have hsum_neg : w2 * x + w3 * y + w4 * w < 0 := by
        rw [hw0]
        nlinarith
      linarith
  · rcases sgn_neq_of_f2 y w hf2' with hf2pos | hf2neg | hf2zero
    · have hx0 : x = 0 := hf1zero.1
      have hw0 : 0 < w := hf2pos.1
      have hwy : w ≤ y := hf2pos.2
      have hy_pos : 0 < y := lt_of_lt_of_le hw0 hwy
      have hsum_pos : 0 < w2 * x + w3 * y + w4 * w := by
        rw [hx0]
        nlinarith
      linarith
    · have hx0 : x = 0 := hf1zero.1
      have hw_neg : w < 0 := hf2neg.1
      have hyw : y ≤ w := hf2neg.2
      have hy_neg : y < 0 := lt_of_le_of_lt hyw hw_neg
      have hsum_neg : w2 * x + w3 * y + w4 * w < 0 := by
        rw [hx0]
        nlinarith
      linarith
    · have hx0 : x = 0 := hf1zero.1
      have hy_ne0 : y ≠ 0 := hf1zero.2
      have hw0 : w = 0 := hf2zero.1
      have hsum_ne : w2 * x + w3 * y + w4 * w ≠ 0 := by
        rw [hx0, hw0]
        simpa using (mul_ne_zero (ne_of_gt h_w3) hy_ne0)
      exact hsum_ne h_mom'

/-- 最终定理：R1 区（半共线+动量守恒）下，通式(39) 与显式公式(30) 等价。 -/
theorem n4_formula_39_eq_30_r1
    (w1 w2 w3 w4 z1 z2 z3 z4 : ℝ)
    (h_sum : w1 + w2 + w3 + w4 = 0)
    (h_w1 : w1 < 0) (h_w2 : 0 < w2) (h_w3 : 0 < w3) (h_w4 : 0 < w4)
    (h_mom : w1 * z1 + w2 * z2 + w3 * z3 + w4 * z4 = 0) :
    (sgn (w1 * w2 * (z1 - z2)) + sgn (w2 * w3 * (z2 - z3))) *
      (sgn (w3 * w4 * (z3 - z4)) + sgn (w4 * w1 * (z4 - z1)))
    = 2 * (sgn (w2 * w3 * (z2 - z3)) * sgn (w4 * w1 * (z4 - z1))
        + sgn (w1 * w2 * (z1 - z2)) * sgn (w3 * w4 * (z3 - z4))) := by
  have hcond : (sgn (w1 * w2 * (z1 - z2)) - sgn (w2 * w3 * (z2 - z3))) *
      (sgn (w3 * w4 * (z3 - z4)) - sgn (w4 * w1 * (z4 - z1))) = 0 :=
    r1_momentum_sign_identity w1 w2 w3 w4 z1 z2 z3 z4 h_sum h_w1 h_w2 h_w3 h_w4 h_mom
  exact n4_formula_equivalence
    (sgn (w1 * w2 * (z1 - z2))) (sgn (w2 * w3 * (z2 - z3)))
    (sgn (w3 * w4 * (z3 - z4))) (sgn (w4 * w1 * (z4 - z1))) hcond

end SingleMinusAmplitude
