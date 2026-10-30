/-
  DualScalingEquiv.lean — 缩放函子对偶等价（Phase 104az-115，C 项：对偶完整伴随对接第一步）
  =======================================================

  把 GapDualityFunctor 的缩放函子语义骨架提升为**逆缩放对偶等价**：
    - 逆缩放函子 F_{1/κ} : x ↦ x/κΛ——谱映射的逆（κΛ ≠ 0 良定义）
    - 对偶消去：F_{1/κ}∘F_κ = id 且 F_κ∘F_{1/κ} = id（函数层范畴等价）
    - 互锁比在对偶消去下保持：对偶不改变两口径的比值结构
    - 对偶投影：逆缩放把 scaleF dlP20 送回 dlP20、把 scaleF dlEM 送回 dlEM
      （Rec 层对数平方 ↔ Sp 层计数平方各自回到自身——对偶配对的函子实现）

  与既有伴随资产的对接语义：
    - RAP5a_explicit_adjunction.lean：Rec/Sp 的 D ⊣ R 伴随（线性语义 SpImD 实例）
    - 本文件：双谱隙缩放对偶的等价层（缩放函子 F_κ 与 F_{1/κ}）
    - 两者分层互补：D ⊣ R 是"范畴层"伴随，F_κ/F_{1/κ} 是"谱映射层"对偶等价
    - 完整伴随（Adjunction.lean 抽象）对接仍为长期开放项（语义层主张，非完整反变等价）

  诚实边界：本文件证明的是缩放函子的**等价/对偶消去**（严格可证），
    非完整伴随自然同构（后者需 ℝ 态射层结构，仍开放）。
-/

import Mathlib.Tactic
import MUFPFormalization.GapDualityFunctor

namespace MUFPF.GapEquiv

open MUFPF.GapFunctor
open MUFPF.DualGap
open MUFPF.LambdaGap

/-! =========================================================
    逆缩放函子（谱映射的逆）
   ========================================================= -/

/-- 逆缩放函子 F_{1/κ} : x ↦ x/κΛ——缩放对偶（κΛ ≠ 0 良定义）。 -/
noncomputable def scaleInv (x : ℝ) : ℝ := x / kappaLambda

/-- 对偶消去（方向一）：F_{1/κ}∘F_κ = id——先缩放后逆缩放回到原值。 -/
theorem scaleInv_comp_scale (x : ℝ) : scaleInv (scaleF x) = x := by
  unfold scaleInv scaleF
  field_simp [kappaLambda_ne_zero]

/-- 对偶消去（方向二）：F_κ∘F_{1/κ} = id——先逆缩放后缩放回到原值。 -/
theorem scale_comp_scaleInv (x : ℝ) : scaleF (scaleInv x) = x := by
  unfold scaleInv scaleF
  field_simp [kappaLambda_ne_zero]

/-! =========================================================
    缩放对偶等价
   ========================================================= -/

/-- 对偶等价（函数层）：缩放函子与逆缩放函子互为拟逆——双向消去。 -/
theorem scale_dual_equiv (x : ℝ) :
    scaleF (scaleInv x) = x ∧ scaleInv (scaleF x) = x := by
  constructor
  · exact scale_comp_scaleInv x
  · exact scaleInv_comp_scale x

/-- 缩放对偶等价（全称版）：任意 x，双向消去均成立——等价是全域结构。 -/
theorem scale_dual_equiv_universal :
    (∀ x : ℝ, scaleF (scaleInv x) = x) ∧ (∀ x : ℝ, scaleInv (scaleF x) = x) := by
  constructor
  · intro x
    exact scale_comp_scaleInv x
  · intro x
    exact scaleInv_comp_scale x

/-! =========================================================
    互锁比的对偶不变性
   ========================================================= -/

/-- 互锁比在对偶消去下保持：F_{1/κ}(F_κ(Δλ_P20)) / F_{1/κ}(F_κ(Δλ_EM)) = 7²/(4ln10)。
    对偶不改变两口径的比值结构——对偶配对的函子核心在对偶等价下稳定。 -/
theorem interlock_dual_invariant :
    scaleInv (scaleF dlP20) / scaleInv (scaleF dlEM) = (7 : ℝ) ^ 2 / (4 * Real.log 10) := by
  rw [scaleInv_comp_scale, scaleInv_comp_scale]
  exact interlock_ratio

/-! =========================================================
    对偶投影（函子语言）
   ========================================================= -/

/-- 对偶投影：逆缩放把缩放后的计数平方送回 P20 谱隙、把缩放后的对数平方送回 EM 谱隙。
    同一缩放函子的双投影在对偶消去下各自回到自身（Rec/Sp 双通道稳定）。 -/
theorem dual_projection_functorial :
    (scaleInv (scaleF dlP20) = dlP20) ∧ (scaleInv (scaleF dlEM) = dlEM) := by
  constructor
  · exact scaleInv_comp_scale dlP20
  · exact scaleInv_comp_scale dlEM

/-- 对偶自洽（函子语言）：缩放→逆缩放回到原点——谱隙在对偶往返下无漂移。 -/
theorem duality_roundtrip_stable (x : ℝ) :
    scaleF (scaleInv (scaleF x)) = scaleF x := by
  rw [scale_comp_scaleInv]

end MUFPF.GapEquiv
