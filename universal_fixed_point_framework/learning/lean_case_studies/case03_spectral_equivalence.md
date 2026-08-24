# Lean 4 实战案例 3：复现 SpectralEquivalence.lean 的核心定理

> 本案例带领读者阅读并复现 MUFPF 形式化仓库中 `SpectralEquivalence.lean` 的核心思想：由范畴同构诱导的等价关系。

## 学习目标

完成本案例后，你将能够：
1. 理解 `Nonempty (DFunctor.obj R₁ ≅ DFunctor.obj R₂)` 的含义
2. 验证由同构诱导的等价关系
3. 把这一思想迁移到其他范畴构造

## 核心定理回顾

在 `SpectralEquivalence.lean` 中，谱等价定义为：

```lean
import MUFPFormalization.RecCategory
import MUFPFormalization.SpCategory
import MUFPFormalization.DecursionFunctor
import MUFPFormalization.SpectralCorrespondence
import MUFPFormalization.IsolationConstraints
import Mathlib.CategoryTheory.EqToHom

namespace MUFPFormalization

open CategoryTheory

/-- Spectral equivalence relation on RecObj.
    R₁ ≃_spec R₂ iff D(R₁) ≅ D(R₂) as objects in the Spec category. -/
def spectralEquivalence (R₁ R₂ : RecObj) : Prop :=
  Nonempty (DFunctor.obj R₁ ≅ DFunctor.obj R₂)
```

## 为什么用 `Nonempty` 而不是直接取同构？

`Iso X Y` 是范畴论中的同构类型。`Nonempty (X ≅ Y)` 表示"存在一个同构"，但不需要具体给出哪一个。

使用 `Nonempty` 而不是直接取 `X ≅ Y` 的原因是：
- 我们只想表达"谱等价"这一**性质**（命题）
- 具体是哪一个同构对等价关系本身不重要
- 这避免了选择公理和具体构造的依赖

## 等价关系的三个性质

```lean
theorem spectralEquivalence_refl (R : RecObj) : spectralEquivalence R R :=
  ⟨Iso.refl _⟩

theorem spectralEquivalence_symm {R₁ R₂ : RecObj} (h : spectralEquivalence R₁ R₂) :
    spectralEquivalence R₂ R₁ :=
  ⟨h.some.symm⟩

theorem spectralEquivalence_trans {R₁ R₂ R₃ : RecObj}
    (h₁₂ : spectralEquivalence R₁ R₂) (h₂₃ : spectralEquivalence R₂ R₃) :
    spectralEquivalence R₁ R₃ :=
  ⟨h₁₂.some.trans h₂₃.some⟩
```

### 解析

| 定理 | 用到的同构性质 | 含义 |
|------|--------------|------|
| `spectralEquivalence_refl` | `Iso.refl _` | 恒等同构，任何对象与自身谱等价 |
| `spectralEquivalence_symm` | `h.some.symm` | 同构的逆仍是同构 |
| `spectralEquivalence_trans` | `h₁₂.some.trans h₂₃.some` | 同构的复合仍是同构 |

其中 `h.some` 是从 `Nonempty` 命题中提取一个具体同构的语法。

## 简化的独立例子

为了理解这个模式，我们可以在任意范畴中证明：由对象同构诱导的关系是等价关系。

```lean
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Iso

universe u v

open CategoryTheory

variable (C : Type u) [Category.{v} C]

/-- 由范畴 C 中的同构诱导的等价关系。 -/
def isoEquiv (X Y : C) : Prop :=
  Nonempty (X ≅ Y)

/-- 自反性。 -/
theorem isoEquiv_refl (X : C) : isoEquiv C X X :=
  ⟨Iso.refl X⟩

/-- 对称性。 -/
theorem isoEquiv_symm {X Y : C} (h : isoEquiv C X Y) : isoEquiv C Y X :=
  ⟨h.some.symm⟩

/-- 传递性。 -/
theorem isoEquiv_trans {X Y Z : C}
    (h₁ : isoEquiv C X Y) (h₂ : isoEquiv C Y Z) : isoEquiv C X Z :=
  ⟨h₁.some.trans h₂.some⟩
```

## 与 MUFPF 的联系

`SpectralEquivalence.lean` 的核心思想是：

> 两个递归系统是否"本质相同"，可以通过它们的谱化像是否同构来判断。

这正是 Paper III §3 中"谱等价"概念的形式化。它把动力系统中的"等价"问题转化为谱范畴中的"同构"问题。

## 拓展练习

1. 证明 `isoEquiv` 满足等价关系的完整定义（即构造 `Equivalence` 实例）。
2. 在 `Type` 范畴中，证明 `isoEquiv` 等价于存在双射。
3. 阅读 MUFPF `Braided.lean`，找出其中由辫子结构诱导的等价关系，并与 `spectralEquivalence` 比较。
4. 思考：如果 $D$ 不是完全忠实的，`spectralEquivalence` 是否仍然是"好"的等价概念？
