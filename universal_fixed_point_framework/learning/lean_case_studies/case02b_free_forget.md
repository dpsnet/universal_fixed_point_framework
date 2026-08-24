# Lean 4 实战案例 2b：真正的 Free ⊣ Forget 伴随

> 本案例在 Lean 4 中构造一个**真实且标准**的伴随对：自由幺半群函子 `Free : Set → Monoid` 与遗忘函子 `Forget : Monoid → Set`。它与 [案例 2](case02_adjunction.md) 中的演示性例子形成对照，也与 MUFPF 核心伴随 `D ⊣ R` 共享同一条构造路线。

## 学习目标

完成本案例后，你将能够：

1. 显式写出 `Free` 与 `Forget` 的对象映射与态射映射；
2. 给出单位 `η` 与余单位 `ε` 的闭式定义；
3. 手算验证两条三角恒等式；
4. 在 Lean 4 / Mathlib 中定位到同一定理的现成形式；
5. 把同样的验证模式迁移到 `D ⊣ R`。

---

## 数学构造

设：

- `Set` 为集合范畴（对象 = 类型，态射 = 函数）；
- `Monoid` 为幺半群范畴（对象 = 幺半群，态射 = 幺半群同态）。

### 遗忘函子 `Forget : Monoid → Set`

对任意幺半群 `M = (|M|, ⋆, 1_M)`，定义

```
Forget(M) := |M|   （只看承载集合）
Forget(f) := f     （同态底层仍是函数）
```

这是显然的忠实函子。

### 自由幺半群函子 `Free : Set → Monoid`

对任意集合 `X`，定义 `X` 上的**自由幺半群**为字（word） Monoid：

```
Free(X) := List X = { [x1, x2, ..., xn] | n ∈ ℕ, xi ∈ X }
```

其乘法为列表连接 `++`，单位元为空列表 `[]`。

对任意函数 `f : X → Y`，定义

```
Free(f) : Free(X) → Free(y)
Free(f)([x1, ..., xn]) := [f x1, ..., f xn]
```

即 `List.map f`。这保持 `++` 与 `[]`，因此是幺半群同态。

---

## 单位与余单位

### 单位 `η : id_Set ⇒ Forget ∘ Free`

对集合 `X`，

```
η_X : X → Forget(Free(X)) = X → List X
η_X(x) := [x]
```

把元素打成单字母字。

### 余单位 `ε : Free ∘ Forget ⇒ id_Monoid`

对幺半群 `M = (|M|, ⋆, 1_M)`，

```
ε_M : Free(Forget(M)) → M
ε_M([m1, m2, ..., mn]) := m1 ⋆ m2 ⋆ ... ⋆ mn
```

空字映射到 `1_M`。这本质上是把字“求值”为幺半群中的乘积。

### Hom 集合同构（伴随的核心）

`Free ⊣ Forget` 的等价表述是：对任意集合 `X` 与幺半群 `M`，存在自然双射

```
Φ_{X,M} : Hom_Monoid(Free(X), M) ≅ Hom_Set(X, Forget(M))
Φ(f)(x)   = f([x])               （把幺半群同态限制到单字母字）
Φ^{-1}(g)([x1,...,xn]) = g(x1) ⋆ ... ⋆ g(xn)   （把函数唯一地延拓为同态）
```

`Φ^{-1}` 的良好定义性依赖于 `Free(X)` 的泛性质：任意函数 `g : X → |M|` 都唯一地延拓为一个幺半群同态 `g̃ : Free(X) → M`。

---

## 三角恒等式手算验证

### 第一条：`ε Free ∘ Free η = id_Free`

对任意集合 `X`，需要验证幺半群同态

```
Free(X) --Free(η_X)--> Free(Forget(Free(X))) --ε_{Free(X)}--> Free(X)
```

等于 `id_{Free(X)}`。

取字 `w = [x1, ..., xn] ∈ Free(X)`：

1. `Free(η_X)(w) = [η_X(x1), ..., η_X(xn)] = [[x1], [x2], ..., [xn]]`
   （每个字母被替换为单元素列表，得到嵌套在 `Free(Free(X))` 中的字）。

2. `ε_{Free(X)}` 把 `Free(Free(X))` 中的字按 `Free(X)` 的乘法 `++` 求值，因此
   `ε_{Free(X)}([[x1], [x2], ..., [xn]]) = [x1] ++ [x2] ++ ... ++ [xn] = [x1, ..., xn] = w`。

故 `ε Free ∘ Free η = id_{Free(X)}`。

### 第二条：`Forget ε ∘ η Forget = id_Forget`

对任意幺半群 `M`，需要验证函数

```
Forget(M) --η_{Forget(M)}--> Forget(Free(Forget(M))) --Forget(ε_M)--> Forget(M)
```

等于 `id_{Forget(M)}`。

取 `m ∈ Forget(M)`：

1. `η_{Forget(M)}(m) = [m]`。

2. `Forget(ε_M)` 不改动底层函数，因此 `Forget(ε_M)([m]) = ε_M([m]) = m`。

故 `Forget ε ∘ η Forget = id_{Forget(M)}`。

> **与 `D ⊣ R` 的对照**：在 `D ⊣ R` 中，第一条三角恒等式成立的关键是谱化函子 `D` 把 `R(D(S))` 的额外递归结构“压平”回 `D(S)`，且 `D` 是忠实的；第二条则是因为 `R(E)` 本身按 `E` 构造，余单位直接读取原始谱数据。此处 `Free ⊣ Forget` 的两条恒等式分别对应：
> - 第一条（`ε Free ∘ Free η = id`）：`Free` 生成的字被自身的乘法“折叠”回去；
> - 第二条（`Forget ε ∘ η Forget = id`）：单个元素字的求值就是元素本身。

---

## Lean 4 / Mathlib 实现

Mathlib 已经内置了 `FreeMonoid` 与 `FreeMonoid.adj` 伴随。下面给出与上述数学构造一一对应的代码，并做逐行解释。

```lean
import Mathlib.Algebra.Category.MonCat.Adjunctions
import Mathlib.Algebra.FreeMonoid.Basic
import Mathlib.CategoryTheory.Adjunction.Basic

open CategoryTheory

universe u

-- FreeMonoid 已经是 Type u ⥤ MonCat.{u} 的函子
#check FreeMonoid.adj.{u}
-- 类型签名：FreeMonoid.{u} ⊣ forget MonCat.{u}
```

### 手动验证单位与余单位的定义

```lean
import Mathlib.Algebra.Category.MonCat.Adjunctions
import Mathlib.Algebra.FreeMonoid.Basic
import Mathlib.CategoryTheory.Monoidal.Mon_

open CategoryTheory

universe u

variable (X : Type u) (M : MonCat.{u})

-- 单位 η_X : X → forget MonCat (FreeMonoid X)
#check FreeMonoid.adj.unit.app X
-- 即把 x : X 映射为 [x] : List X

-- 余单位 ε_M : FreeMonoid (forget MonCat M) → M
#check FreeMonoid.adj.counit.app M
-- 即把字 [m1, ..., mn] 映射为 m1 * ... * mn

-- 三角恒等式在 Mathlib 中自动成立
#check FreeMonoid.adj.left_triangle_components X
#check FreeMonoid.adj.right_triangle_components M
```

### 关键引理一览

| 数学对象 | Lean 名称 | 说明 |
| --- | --- | --- |
| 自由幺半群 | `FreeMonoid X` | `List X` 配备 `++` 与 `[]` |
| 遗忘函子 | `forget MonCat` | 只看承载类型 |
| 单位 | `FreeMonoid.adj.unit` | `fun x => [x]` |
| 余单位 | `FreeMonoid.adj.counit` | `List.prod`（在 Monoid 上） |
| 伴随本身 | `FreeMonoid.adj` | `FreeMonoid ⊣ forget MonCat` |

### 与 `Adjunction.mkOfHomEquiv` 的对应

若不想用现成结论，也可手动构造 `homEquiv`：

```lean
import Mathlib.Algebra.Category.MonCat.Adjunctions
import Mathlib.Algebra.FreeMonoid.Basic
import Mathlib.CategoryTheory.Adjunction.Basic

open CategoryTheory

universe u

-- 手动验证 Hom 集合同构
example (X : Type u) (M : MonCat.{u}) :
    (FreeMonoid X →** M) ≃ (X → M.1) :=
  FreeMonoid.liftEquiv
```

`FreeMonoid.liftEquiv` 正是 `Φ_{X,M}` 的实现：把幺半群同态 `FreeMonoid X →** M` 限制到生成元，与任意函数 `X → M` 一一对应。

---

## 常见错误提示

1. **把 `Free(f)` 当成 `f` 本身**
   `Free(f)` 作用在字 `[x1, ..., xn]` 上得到 `[f x1, ..., f xn]`，而不是把 `f` 应用到列表本身。在 Lean 中它等于 `List.map f`。

2. **混淆 `η_X` 与 `ε_{Free(X)}`**
   `η_X : X → List X` 只做单字母嵌入；`ε_{Free(X)} : List (List X) → List X` 是按 `++` 折叠多层列表。第一条三角恒等式之所以成立，正是因为后者把前者生成的嵌套列表展平。

3. **余单位的定义域写错**
   `ε_M` 定义在 `Free(Forget(M))` 上，而不是 `M` 上。它的作用是把“字”求值为幺半群元素。

4. **在 Lean 中误用 `MonCat` 与 `Monoid`**
   `MonCat` 是范畴（对象 = 幺半群 bundled 成范畴对象），`Monoid` 是类型类。伴随函子 `FreeMonoid` 的值域是 `MonCat`，而 `forget MonCat` 的陪域是 `Type u`。

---

## 与 MUFPF 的对比

| 伴随对 | 左伴随 `L` | 右伴随 `R` | 单位 `η` 的直观 | 余单位 `ε` 的直观 |
| --- | --- | --- | --- | --- |
| `Free ⊣ Forget` | `Free`：生成自由字 | `Forget`：遗忘结构 | 把元素打成单字母字 | 把字求值为乘积 |
| `D ⊣ R` | `D`：谱化递归系统 | `R`：递归化谱对象 | 把递归状态嵌入谱空间 | 把谱对象重建为递归系统 |

两者都满足：

1. `R ∘ L` 给原始对象添加“可计算的生成结构”（字 / 递归演化）；
2. `L ∘ R` 把生成结构再“折叠”回原始结构（求值 / 谱重建）；
3. 三角恒等式保证这种“生成—折叠” round-trip 是恒等的。

---

## 拓展练习

1. 在 Lean 中证明：对任意类型 `X`，`FreeMonoid.adj.unit.app X` 等于 `fun x => [x]`。
2. 在 Lean 中证明：对任意 `M : MonCat`，`FreeMonoid.adj.counit.app M` 把 `[m1, m2, m3]` 映射为 `m1 * m2 * m3`。
3. 用 `Adjunction.mkOfHomEquiv` 从头构造 `FreeMonoid ⊣ forget MonCat`，不依赖 `FreeMonoid.adj`。
4. 对比阅读 MUFPF 的 `Adjunction.lean`：找出 `D` 与 `R` 的 `unit` / `counit` 对应到本案例中的哪些结构。
