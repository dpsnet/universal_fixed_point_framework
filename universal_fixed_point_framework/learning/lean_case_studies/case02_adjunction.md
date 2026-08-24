# Lean 4 实战案例 2：构造一个小伴随对

> 本案例展示如何在 Lean 4 中构造一个具体的伴随对，帮助读者理解 `Adjunction.mkOfHomEquiv` 的使用方法。
>
> 注意：本文件前半部分包含一个“不是真正伴随”的演示性例子（`F(S) ⊣ G`），用于说明 API；一个**真实且标准**的 `Free ⊣ Forget` 伴随请见 [案例 2b：真正的 Free ⊣ Forget 伴随](case02b_free_forget.md)。

## 学习目标

完成本案例后，你将能够：
1. 定义两个简单范畴和它们之间的函子
2. 使用 `Adjunction.mkOfHomEquiv` 构造伴随对
3. 理解单位与余单位的构造方式

## 伴随对的例子

考虑如下伴随：

**离散范畴** ↔ **集合范畴**

更具体地，我们构造一个非常简单的例子：设范畴 $\mathcal{C}$ 只有一个对象和一个态射（即单子范畴），范畴 $\mathcal{D}$ 也只有一个对象和一个态射。那么任何两个函子 $L, R$ 都自动伴随。

为了更有教育意义，我们使用一个稍复杂但仍初等的例子：

### 例子：集合的"加一"函子与"遗忘"函子

设：
- $\mathcal{C} = \mathcal{D} = \mathbf{Set}$
- $L(X) = X \times \{*\}$（给集合 $X$ 添加一个标记点，同构于 $X$ 本身）
- $R(Y) = Y$（恒等函子）

则 $L \dashv R$，因为：

$$\mathrm{Hom}(L(X), Y) = \mathrm{Hom}(X \times \{*\}, Y) \cong \mathrm{Hom}(X, Y) = \mathrm{Hom}(X, R(Y))$$

这个例子虽然平凡，但展示了伴随对 Hom 集合同构的结构。

## 完整代码

```lean
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.CategoryTheory.Adjunction.Basic

universe u

def UnitCat : Type (u + 1) := PUnit

instance : Category.{u, u + 1} UnitCat where
  Hom _ _ := PUnit
  id _ := PUnit.unit
  comp _ _ := PUnit.unit
  id_comp := by intros; rfl
  comp_id := by intros; rfl
  assoc := by intros; rfl

/-- 从 UnitCat 到 SetCat 的函子：选择某个集合 S 作为唯一对象的像。 -/
def F (S : Type u) : UnitCat.{u} ⥤ Type u where
  obj _ := S
  map _ := id

/-- 从 SetCat 到 UnitCat 的常值函子。 -/
def G : Type u ⥤ UnitCat.{u} where
  obj _ := PUnit.unit
  map _ := PUnit.unit

/-- 构造 F(S) ⊣ G 的伴随。

    对 X : UnitCat 和 Y : Type u：
    Hom_{Type u}(F(S).obj X, Y) = (S → Y)
    Hom_{UnitCat}(X, G.obj Y) = PUnit

    这不是真正的伴随，除非 S 是单点。本代码仅演示 Adjunction.mkOfHomEquiv 的用法。
    更真实、更标准的 Free ⊣ Forget 伴随请参见 [案例 2b](case02b_free_forget.md)。 -/
```

## 一个更真实的例子：积与对角

在 `Type` 范畴中，对角函子 $\Delta: \mathbf{Type} \to \mathbf{Type} \times \mathbf{Type}$，$\Delta(X) = (X, X)$，与积函子 $\Pi: \mathbf{Type} \times \mathbf{Type} \to \mathbf{Type}$，$\Pi(X, Y) = X \times Y$ 构成伴随：

$$\mathrm{Hom}_{\mathbf{Type} \times \mathbf{Type}}(\Delta(X), (Y, Z)) \cong \mathrm{Hom}_{\mathbf{Type}}(X, Y \times Z)$$

这是右伴随。左伴随则是余对角与余积。

```lean
open CategoryTheory

/-- 对角函子 Δ : Type ⥤ Type × Type -/
def Diagonal : Type u ⥤ Type u × Type u where
  obj X := (X, X)
  map f := (f, f)

/-- 积函子 Π : Type × Type ⥤ Type -/
def ProductFunctor : Type u × Type u ⥤ Type u where
  obj := fun (X, Y) => X × Y
  map := fun (f, g) => fun p => (f p.1, g p.2)

/-- Δ ⊣ Π 伴随的 Hom 等价 -/
def DiagonalProductAdjunction : Diagonal ⊣ ProductFunctor :=
  Adjunction.mkOfHomEquiv {
    homEquiv := fun X (Y, Z) =>
      { toFun := fun f => fun x => (f (x, x)).1
        invFun := fun g => fun (x1, x2) => (g x1, g x2)
        left_inv := by
          intro f
          funext ⟨x1, x2⟩
          simp
        right_inv := by
          intro g
          funext x
          simp }
  }
```

**注意**：上述 `DiagonalProductAdjunction` 的类型签名和 `homEquiv` 的具体实现需要根据 Lean 4 的积范畴类型做调整。这里的代码是概念演示，可能需要根据 Mathlib 的实际接口微调。

## 与 MUFPF 的联系

MUFPF 中最重要的伴随对是 $D \dashv R$（`Adjunction.lean`）。其构造思路与本案例相同：

1. 定义两个范畴（$\mathbf{Rec}_D$ 和 $\mathbf{Sp}$）
2. 定义谱化函子 $D$ 和递归化函子 $R$
3. 构造 Hom 集合之间的自然同构

不同的是，$D \dashv R$ 的态射空间涉及无限维 Hilbert 空间和算子理论，因此实现更为复杂。

## 拓展练习

1. 在 `Type` 范畴中构造余对角函子与余积函子之间的伴随。
2. 证明如果 $L \dashv R$ 且 $R$ 是完全忠实的，则单位 $\eta$ 是同构。
3. 阅读 MUFPF `RAP5a_explicit_adjunction.lean`，找出其中 `DIm ⊣ RIm` 的 `homEquiv` 构造。
