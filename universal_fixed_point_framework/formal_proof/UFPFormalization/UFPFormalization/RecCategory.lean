/-
递归系统范畴 Rec 的有限维原型形式化。

在论文中，Rec 的对象是递归系统 (X, U_R)，其中 U_R 是 Koopman 压缩半群。
为适配等级 A（极易形式化）模块，这里先做有限维线性原型：
- 对象：有限维向量空间 V 上的线性自同态 T : V → V（代表离散时间一步演化）
- 态射：线性映射 f : V → W，满足与演化算子的交换条件 f ∘ T_V = T_W ∘ f

未来等级 B/C 再将其提升到无穷维 Banach/Hilbert 空间及压缩半群情形。
-/

import Mathlib.CategoryTheory.Category.Basic
import Mathlib.LinearAlgebra.FiniteDimensional
import Mathlib.LinearAlgebra.Matrix

universe u v

/-- 递归系统对象：有限维向量空间上的线性自同态。 -/
structure RecObject (𝕜 : Type u) [Field 𝕜] where
  V : Type v
  [instFinDim : FiniteDimensional 𝕜 V]
  T : V →ₗ[𝕜] V

attribute [instance] RecObject.instFinDim

namespace RecObject

variable {𝕜 : Type u} [Field 𝕜]

/-- 两个递归系统之间的态射：与演化算子交换的线性映射。 -/
structure Hom (X Y : RecObject 𝕜) where
  toLin : X.V →ₗ[𝕜] Y.V
  comm : ∀ v, toLin (X.T v) = Y.T (toLin v)

@[ext]
lemma Hom.ext {X Y : RecObject 𝕜} (f g : Hom X Y) (h : ∀ v, f.toLin v = g.toLin v) : f = g := by
  cases f; cases g
  simp_all
  apply LinearMap.ext
  exact h

/-- 恒等态射。 -/
def id (X : RecObject 𝕜) : Hom X X where
  toLin := LinearMap.id
  comm := by simp

/-- 态射复合。 -/
def comp {X Y Z : RecObject 𝕜} (g : Hom Y Z) (f : Hom X Y) : Hom X Z where
  toLin := g.toLin.comp f.toLin
  comm := by
    intro v
    simp [g.comm, f.comm]

@[simp]
lemma comp_toLin {X Y Z : RecObject 𝕜} (g : Hom Y Z) (f : Hom X Y) :
    (comp g f).toLin = g.toLin.comp f.toLin := rfl

/-- 复合满足结合律。 -/
lemma comp_assoc {W X Y Z : RecObject 𝕜}
    (h : Hom Y Z) (g : Hom X Y) (f : Hom W X) :
    comp (comp h g) f = comp h (comp g f) := by
  ext w
  simp

/-- 恒等复合。 -/
lemma id_comp {X Y : RecObject 𝕜} (f : Hom X Y) : comp (id Y) f = f := by
  ext v
  simp [comp, id]

lemma comp_id {X Y : RecObject 𝕜} (f : Hom X Y) : comp f (id X) = f := by
  ext v
  simp [comp, id]

end RecObject

/-- Rec 范畴的有限维原型：对象是有限维向量空间上的线性自同态，
    态射是与演化算子交换的线性映射。 -/
def RecCategory (𝕜 : Type u) [Field 𝕜] : Category (RecObject 𝕜) where
  Hom := RecObject.Hom
  id := RecObject.id
  comp := @RecObject.comp 𝕜 _
  id_comp := RecObject.id_comp
  comp_id := RecObject.comp_id
  assoc := RecObject.comp_assoc
