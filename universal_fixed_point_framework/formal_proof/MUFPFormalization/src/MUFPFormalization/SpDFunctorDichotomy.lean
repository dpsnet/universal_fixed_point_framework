-- ============================================================
-- `DFunctor` 值域的二分：自伴像与非自伴像并存
-- ============================================================
-- D39（`SpDFunctorStrong.lean`）已否证「每个像都非自伴」——`step = id` 时像为
-- `A = 1`，自伴。但非自伴那一半当时还没落成 `DFunctor` 像：D35 的
-- `cyclic3SpObj` 是直接构造 `⟨3, stepMatrix cyclicStep3⟩`，不是 `obj` 调用。
--
-- 本模块补上这一半，并把两侧焊成二分定理。
--
-- 证非自伴不走矩阵代数（`Pᴴ C P` 的共轭链太长），而走**元素级判定**：
-- `DFunctor.obj X` 的 `A` 在指标 `(e 0, e 1)` 与 `(e 1, e 0)` 上分别取 1 与 0，
-- 其中 `e := Fintype.equivFin X.T`。自伴要求这两元互为共轭，1 ≠ star 0。
-- 数值侧已穷举确认：n = 3 的全部 6 个置换下 `Pᴴ = P⁻¹`、`PᴴP = 1`，且
-- `Pᴴ C P` 一律非自伴 ⇒ 该结论与 `equivFin` 的具体实现无关。
-- ============================================================

import MUFPFormalization.SpDFunctorStrong
import MUFPFormalization.SpDFunctorRange

namespace MUFPF

open CategoryTheory Matrix

/-- 3-循环 `cyclicStep3` 作为 `RecObj` 的演化规则。
    用 `abbrev` 而非 `def`：否则 `cyclicRec.T` 不可归约到 `Fin 3`，
    指标处的 `OfNat cyclicRec.T 0` 无法 synth。 -/
abbrev cyclicRec : RecObj where
  T := Fin 3
  fin := inferInstance
  dec := inferInstance
  step := cyclicStep3

/-- **非自伴像**：`DFunctor` 在 `cyclicRec` 上的像的算子非自伴。

    证明只看两个元素：`A (e 0) (e 1) = 1`、`A (e 1) (e 0) = 0`，
    故自伴所要求的 `A (e 0) (e 1) = star (A (e 1) (e 0))` 退化为 `1 = 0`。 -/
theorem DFunctor_obj_cyclic_nonhermitian : ¬ IsHermitian (DFunctor.obj cyclicRec) := by
  intro h
  have h01 := (isHermitian_iff_entries.mp h)
    (Fintype.equivFin cyclicRec.T 0) (Fintype.equivFin cyclicRec.T 1)
  have hA01 : (DFunctor.obj cyclicRec).A
      (Fintype.equivFin cyclicRec.T 0) (Fintype.equivFin cyclicRec.T 1) = 1 := by
    change stepMatrix (Fintype.equivFin cyclicRec.T ∘ cyclicRec.step
        ∘ (Fintype.equivFin cyclicRec.T).symm)
        (Fintype.equivFin cyclicRec.T 0) (Fintype.equivFin cyclicRec.T 1) = 1
    simp [stepMatrix, transferMatrix, cyclicRec, cyclicStep3]
  have hne : (Fintype.equivFin cyclicRec.T) 2 ≠ (Fintype.equivFin cyclicRec.T) 0 := by
    intro hc
    have h20 : (2 : Fin 3) = 0 := (Fintype.equivFin cyclicRec.T).injective hc
    exact absurd h20 (by decide)
  have hA10 : (DFunctor.obj cyclicRec).A
      (Fintype.equivFin cyclicRec.T 1) (Fintype.equivFin cyclicRec.T 0) = 0 := by
    change stepMatrix (Fintype.equivFin cyclicRec.T ∘ cyclicRec.step
        ∘ (Fintype.equivFin cyclicRec.T).symm)
        (Fintype.equivFin cyclicRec.T 1) (Fintype.equivFin cyclicRec.T 0) = 0
    simp [stepMatrix, transferMatrix, cyclicRec, cyclicStep3, hne]
  rw [hA01, hA10] at h01
  simp at h01

/-- **二分定理**：`DFunctor` 的值域内**既有**自伴像，**也有**非自伴像。

    ⇒ 「每个像都非自伴」（D39 已否证）与「每个像都自伴」（D35 `not_all_spObj_hermitian`
    只管全空间，不管值域）两种一刀切表述都不成立。 -/
theorem DFunctor_range_dichotomy :
    (∃ X : RecObj.{0}, IsHermitian (DFunctor.obj X)) ∧
    (∃ Y : RecObj.{0}, ¬ IsHermitian (DFunctor.obj Y)) :=
  ⟨⟨idRec1, DFunctor_obj_idRec1_isHermitian⟩,
   ⟨cyclicRec, DFunctor_obj_cyclic_nonhermitian⟩⟩

end MUFPF
