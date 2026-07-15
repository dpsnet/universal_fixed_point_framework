/-
谱去递归化函子 D : Rec → Spec 的有限维原型形式化。

在论文中，D 将递归系统 (X, U_R) 映射到其谱对象，其中谱算子 A_R = -log U_R。
在有限维原型中，若 U_R 可逆，可定义 A_R = -log U_R；为简化等级 A 证明，
这里先取 D 为恒等/遗忘构造，即把演化算子 T 直接视为谱算子 A。

这一定义满足函子的两条公理：
1. D(id_X) = id_{D(X)}
2. D(g ∘ f) = D(g) ∘ D(f)
-/

import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.LinearAlgebra.FiniteDimensional
import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory

universe u v

variable {𝕜 : Type u} [Field 𝕜]

namespace DecursionFunctor

/-- D 函子在对象上的作用：RecObject → SpecObject（等级 A 原型为恒等）。 -/
def mapObj (X : RecObject 𝕜) : SpecObject 𝕜 := X.toSpecObject

/-- D 函子在态射上的作用：Rec 态射 → Spec 态射。
    由于等级 A 原型中两种态射结构相同，直接转换。 -/
def mapHom {X Y : RecObject 𝕜} (f : RecObject.Hom X Y) : SpecObject.Hom (mapObj X) (mapObj Y) where
  toLin := f.toLin
  comm := f.comm

@[simp]
lemma mapHom_toLin {X Y : RecObject 𝕜} (f : RecObject.Hom X Y) :
    (mapHom f).toLin = f.toLin := rfl

/-- D 保持恒等态射。 -/
lemma map_id (X : RecObject 𝕜) : mapHom (RecObject.id X) = SpecObject.id (mapObj X) := by
  ext v
  simp [mapHom, RecObject.id, SpecObject.id]

/-- D 保持态射复合。 -/
lemma map_comp {X Y Z : RecObject 𝕜} (g : RecObject.Hom Y Z) (f : RecObject.Hom X Y) :
    mapHom (RecObject.comp g f) = SpecObject.comp (mapHom g) (mapHom f) := by
  ext v
  simp [mapHom, RecObject.comp, SpecObject.comp]

end DecursionFunctor

/-- 谱去递归化函子 D : RecCategory 𝕜 → SpecCategory 𝕜（等级 A 原型）。 -/
def DFunctor : RecCategory 𝕜 ⥤ SpecCategory 𝕜 where
  obj := DecursionFunctor.mapObj
  map := @DecursionFunctor.mapHom 𝕜 _
  map_id := DecursionFunctor.map_id
  map_comp := DecursionFunctor.map_comp
