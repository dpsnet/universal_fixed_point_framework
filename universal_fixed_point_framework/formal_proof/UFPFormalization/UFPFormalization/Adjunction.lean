/-
D ⊣ R 伴随关系的有限维原型形式化。

在论文中，D : Rec → Spec 有右伴随 R : Spec → Rec。
等级 A 原型中，D 与 R 均取为恒等/遗忘构造，因此它们自然形成伴随：

Hom_{Spec}(D(X), Y) ≅ Hom_{Rec}(X, R(Y))

同构由恒等映射给出（因为两种 Hom 集在原型中相等）。

注：在提升到无穷维/半群情形后，D 将对 U_R 取对数得到谱算子 A_R，
R 将对谱对象取指数得到演化半群；伴随性需要更精细的泛函分析论证（等级 B）。
-/

import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.CategoryTheory.Adjunction.Basic
import Mathlib.LinearAlgebra.FiniteDimensional
import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory
import UFPFormalization.DecursionFunctor

universe u v

variable {𝕜 : Type u} [Field 𝕜]

namespace AdjunctionPrototype

/-- R 函子在对象上的作用：SpecObject → RecObject（等级 A 原型为恒等）。 -/
def R_mapObj (Y : SpecObject 𝕜) : RecObject 𝕜 := Y.toRecObject

/-- R 函子在态射上的作用。 -/
def R_mapHom {X Y : SpecObject 𝕜} (f : SpecObject.Hom X Y) : RecObject.Hom (R_mapObj X) (R_mapObj Y) where
  toLin := f.toLin
  comm := f.comm

@[simp]
lemma R_mapHom_toLin {X Y : SpecObject 𝕜} (f : SpecObject.Hom X Y) :
    (R_mapHom f).toLin = f.toLin := rfl

/-- R 函子 R : SpecCategory 𝕜 → RecCategory 𝕜（等级 A 原型）。 -/
def RFunctor : SpecCategory 𝕜 ⥤ RecCategory 𝕜 where
  obj := R_mapObj
  map := @R_mapHom 𝕜 _
  map_id := by
    intro X
    ext v
    simp [R_mapHom, RecObject.id, SpecObject.id]
  map_comp := by
    intro X Y Z g f
    ext v
    simp [R_mapHom, RecObject.comp, SpecObject.comp]

/-- D 与 R 的 Hom 集之间的自然同构（等级 A 原型中为恒等）。 -/
def homEquiv (X : RecObject 𝕜) (Y : SpecObject 𝕜) :
    (DFunctor.obj X ⟶ Y) ≃ (X ⟶ RFunctor.obj Y) where
  toFun f := RecObject.Hom.mk f.toLin f.comm
  invFun g := SpecObject.Hom.mk g.toLin g.comm
  left_inv _ := by ext v; rfl
  right_inv _ := by ext v; rfl

/-- 验证 homEquiv 的自然性（左）。 -/
lemma homEquiv_naturality_left {X' X : RecObject 𝕜} {Y : SpecObject 𝕜}
    (f : X' ⟶ X) (g : DFunctor.obj X ⟶ Y) :
    homEquiv X' Y (g ≫ DFunctor.map f) = homEquiv X Y g ≫ RFunctor.map f := by
  ext v
  simp [homEquiv, DFunctor, RFunctor, DecursionFunctor.mapHom, R_mapHom]

/-- 验证 homEquiv 的自然性（右）。 -/
lemma homEquiv_naturality_right {X : RecObject 𝕜} {Y Y' : SpecObject 𝕜}
    (f : DFunctor.obj X ⟶ Y) (g : Y ⟶ Y') :
    homEquiv X Y' (DFunctor.map (𝟙 X) ≫ g) = homEquiv X Y f ≫ g := by
  simp [homEquiv]

end AdjunctionPrototype

/-- D ⊣ R 伴随关系（等级 A 原型）。 -/
def DAdjR : DFunctor ⊣ AdjunctionPrototype.RFunctor :=
  Adjunction.mkOfHomEquiv
  { homEquiv := AdjunctionPrototype.homEquiv
    homEquiv_naturality_left := @AdjunctionPrototype.homEquiv_naturality_left 𝕜 _
    homEquiv_naturality_right := @AdjunctionPrototype.homEquiv_naturality_right 𝕜 _ }
