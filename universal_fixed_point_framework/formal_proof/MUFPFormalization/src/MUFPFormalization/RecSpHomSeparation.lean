import MUFPFormalization.SpCategory
import MUFPFormalization.RecCategory
import Mathlib.Data.Fintype.Card
import Mathlib.Analysis.Complex.Basic
import Mathlib.Tactic.Ext

namespace MUFPF

open CategoryTheory

universe u

/-!
# Rec / Sp 的 Hom 集基数分离

把「Rec ≠ Sp」从定义观察升级为可机检的范畴不变量。

* `SpObj` 的 A 是任意矩阵；一维零算子上，任意标量都是自态射 ⇒ 该对象自态射集无限。
* `RecObj` 的 T 是 `Fintype`，态射是有限状态空间之间的映射 ⇒ 任意对象对之间 Hom 集有限。

范畴等价要求 Hom 集之间双射；有限与无限不能被双射消除，故两者不可能等价。
-/

/-! ## 一、Sp 侧：Hom 集无限 -/

/-- 一维零谱对象。 -/
def spZero1 : SpObj where
  n := 1
  A := (0 : Matrix (Fin 1) (Fin 1) ℂ)

/-- 标量 `c` 给出的自态射。 -/
def spHomOfScalar (c : ℂ) : spZero1 ⟶ spZero1 where
  P := Matrix.of (fun _ _ => c)
  intertwine := by
    show Matrix.of (fun _ _ => c) * (0 : Matrix (Fin spZero1.n) (Fin spZero1.n) ℂ)
        = (0 : Matrix (Fin spZero1.n) (Fin spZero1.n) ℂ) * Matrix.of (fun _ _ => c)
    rw [Matrix.mul_zero, Matrix.zero_mul]

/-- `c ↦ spHomOfScalar c` 是单射。 -/
theorem spHomOfScalar_injective : Function.Injective spHomOfScalar := by
  intro a b h
  have h' : (spHomOfScalar a).P ⟨0, by simp [spZero1]⟩ ⟨0, by simp [spZero1]⟩
      = (spHomOfScalar b).P ⟨0, by simp [spZero1]⟩ ⟨0, by simp [spZero1]⟩ :=
    congrArg (fun f : spZero1 ⟶ spZero1 =>
      f.P ⟨0, by simp [spZero1]⟩ ⟨0, by simp [spZero1]⟩) h
  simpa [spHomOfScalar, Matrix.of_apply] using h'

/-- `spZero1` 的自态射集无限。 -/
theorem spHom_infinite : Infinite (spZero1 ⟶ spZero1) :=
  Infinite.of_injective spHomOfScalar spHomOfScalar_injective

/-! ## 二、Rec 侧：Hom 集有限 -/

/-- 态射由底层映射唯一决定（交换条件为命题）。 -/
theorem recHom_toFun_injective {X Y : RecObj.{u}} :
    Function.Injective (fun r : RecHom X Y => r.toFun) := by
  intro a b h
  ext x
  exact congrFun h x

/-- `RecHom` 是有限类型：状态空间有限，态射只在有限多个映射中取。 -/
noncomputable instance recHomFintype (X Y : RecObj.{u}) : Fintype (RecHom X Y) :=
  Fintype.ofInjective (fun r : RecHom X Y => r.toFun) recHom_toFun_injective

/-- 单点递归系统。 -/
def recUnit : RecObj.{0} where
  T := PUnit
  fin := inferInstance
  dec := inferInstance
  step := fun _ => PUnit.unit

/-- 任意 Rec 对象对之间的 Hom 集有限。 -/
theorem recHom_finite (X Y : RecObj.{u}) : Finite (RecHom X Y) :=
  Finite.of_fintype (RecHom X Y)

/-- `recUnit` 的自态射集有限。 -/
theorem recHomUnit_finite : Finite (RecHom.{0, 0} recUnit recUnit) :=
  recHom_finite (X := recUnit) (Y := recUnit)

/-! ## 三、并置 -/

theorem hom_cardinality_separation :
    Infinite (spZero1 ⟶ spZero1) ∧ Finite (RecHom.{0, 0} recUnit recUnit) :=
  ⟨spHom_infinite, recHomUnit_finite⟩

end MUFPF
