/-
谱范畴 Spec 的有限维原型形式化。

在论文中，Spec 的对象是谱对象，由 Koopman 算子的谱信息（特征值/特征向量）构成。
等级 A 原型采用有限维交换代数/可对角化线性算子的视角：
- 对象：有限维向量空间 V 上的线性自同态 A : V → V（代表“谱算子”）
- 态射：与谱算子交换的线性映射

注：这里 Spec 的对象在等级 A 原型下与 RecObject 结构相同，但范畴的“意图”不同：
Rec 强调动力学演化，Spec 强调谱分解与谱对应。后续伴随函子 D : Rec → Spec
在原型中可视为恒等/遗忘类构造。
-/

import Mathlib.CategoryTheory.Category.Basic
import Mathlib.LinearAlgebra.FiniteDimensional
import UFPFormalization.RecCategory

universe u v

/-- 谱对象：有限维向量空间上的线性自同态（等级 A 原型）。 -/
structure SpecObject (𝕜 : Type u) [Field 𝕜] where
  V : Type v
  [instFinDim : FiniteDimensional 𝕜 V]
  A : V →ₗ[𝕜] V

attribute [instance] SpecObject.instFinDim

namespace SpecObject

variable {𝕜 : Type u} [Field 𝕜]

/-- 谱态射：与谱算子交换的线性映射。 -/
structure Hom (X Y : SpecObject 𝕜) where
  toLin : X.V →ₗ[𝕜] Y.V
  comm : ∀ v, toLin (X.A v) = Y.A (toLin v)

@[ext]
lemma Hom.ext {X Y : SpecObject 𝕜} (f g : Hom X Y) (h : ∀ v, f.toLin v = g.toLin v) : f = g := by
  cases f; cases g
  simp_all
  apply LinearMap.ext
  exact h

def id (X : SpecObject 𝕜) : Hom X X where
  toLin := LinearMap.id
  comm := by simp

def comp {X Y Z : SpecObject 𝕜} (g : Hom Y Z) (f : Hom X Y) : Hom X Z where
  toLin := g.toLin.comp f.toLin
  comm := by
    intro v
    simp [g.comm, f.comm]

@[simp]
lemma comp_toLin {X Y Z : SpecObject 𝕜} (g : Hom Y Z) (f : Hom X Y) :
    (comp g f).toLin = g.toLin.comp f.toLin := rfl

lemma comp_assoc {W X Y Z : SpecObject 𝕜}
    (h : Hom Y Z) (g : Hom X Y) (f : Hom W X) :
    comp (comp h g) f = comp h (comp g f) := by
  ext w
  simp

lemma id_comp {X Y : SpecObject 𝕜} (f : Hom X Y) : comp (id Y) f = f := by
  ext v
  simp [comp, id]

lemma comp_id {X Y : SpecObject 𝕜} (f : Hom X Y) : comp f (id X) = f := by
  ext v
  simp [comp, id]

end SpecObject

/-- Spec 范畴的有限维原型。 -/
def SpecCategory (𝕜 : Type u) [Field 𝕜] : Category (SpecObject 𝕜) where
  Hom := SpecObject.Hom
  id := SpecObject.id
  comp := @SpecObject.comp 𝕜 _
  id_comp := SpecObject.id_comp
  comp_id := SpecObject.comp_id
  assoc := SpecObject.comp_assoc

/-- Rec 到 Spec 的遗忘/恒等转换：在等级 A 原型中，动力学对象与谱对象结构相同。 -/
def RecObject.toSpecObject {𝕜 : Type u} [Field 𝕜] (X : RecObject 𝕜) : SpecObject 𝕜 where
  V := X.V
  A := X.T

/-- Spec 到 Rec 的遗忘/恒等转换。 -/
def SpecObject.toRecObject {𝕜 : Type u} [Field 𝕜] (X : SpecObject 𝕜) : RecObject 𝕜 where
  V := X.V
  T := X.A
