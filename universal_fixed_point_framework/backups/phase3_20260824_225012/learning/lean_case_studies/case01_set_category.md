# Lean 4 实战案例 1：证明 Set 是范畴

> 本案例复现 [part07_exercises_lean.md](../part07_exercises_lean.md) 中的项目 A，帮助读者理解如何在 Lean 4 中定义一个范畴。

## 学习目标

完成本案例后，你将能够：
1. 使用 `Mathlib.CategoryTheory.Category.Basic` 定义范畴实例
2. 验证范畴公理（结合律、单位律）
3. 理解 `rfl` 在证明中的作用

## 完整代码

```lean
import Mathlib.CategoryTheory.Category.Basic

universe u

/-- SetCat 是 Type u 层面的集合范畴。
    对象是 Type u 中的类型，态射是它们之间的函数。 -/
def SetCat : Type (u + 1) := Type u

instance : Category.{u, u + 1} SetCat where
  Hom X Y := X → Y
  id X := fun x => x
  comp f g := fun x => g (f x)
  id_comp := by
    -- 对任意 f : X → Y，证明 f ∘ id_X = f
    intros
    rfl
  comp_id := by
    -- 对任意 f : X → Y，证明 id_Y ∘ f = f
    intros
    rfl
  assoc := by
    -- 对任意 f : X → Y, g : Y → Z, h : Z → W，证明 (h ∘ g) ∘ f = h ∘ (g ∘ f)
    intros
    rfl
```

## 代码解析

### `def SetCat : Type (u + 1) := Type u`

我们把 `Type u` 重新包装为 `SetCat`。在范畴论语境中，`SetCat` 的对象是 `Type u` 中的元素，即类型。

### `instance : Category.{u, u + 1} SetCat`

`Category.{v, u}` 是 Mathlib 中范畴的类型类。这里 `u` 是对象宇宙的层级，`v` 是态射宇宙的层级。

### 字段说明

| 字段 | 含义 | 本例中的实现 |
|------|------|------------|
| `Hom X Y` | 对象 X 到 Y 的态射集合 | `X → Y`，即函数 |
| `id X` | 对象 X 的恒等态射 | 恒等函数 `fun x => x` |
| `comp f g` | 态射 f 与 g 的复合 | 函数复合 `g ∘ f` |
| `id_comp` | 左单位律 | `f ∘ id = f` |
| `comp_id` | 右单位律 | `id ∘ f = f` |
| `assoc` | 结合律 | `h ∘ (g ∘ f) = (h ∘ g) ∘ f` |

### 为什么 `rfl` 足够？

在 Lean 中，函数复合的定义是：

```lean
(g ∘ f) x = g (f x)
```

因此：
- `(f ∘ id) x = f (id x) = f x`，即 `f ∘ id = f`，由定义可得 `rfl`
- `((h ∘ g) ∘ f) x = (h ∘ g) (f x) = h (g (f x))`，与 `(h ∘ (g ∘ f)) x` 相同

## 验证构建

将上述代码保存为 `SetCategory.lean`，放在某个 Lake 项目的 `MyProject/` 目录下，运行：

```bash
lake build
```

如果编译通过，说明 Set 范畴的定义在 Lean 4 中是自洽的。

## 拓展练习

1. 定义有限集合范畴 `FinSetCat`，对象为 `Finset (Fin n)` 类型族。
2. 证明 `SetCat` 中的同构就是双射函数。
3. 尝试定义 `SetCat` 中的积与余积（提示：使用 `Prod` 和 `Sum` 类型）。

## 与 UFPF 的联系

UFPF 中的 `RecCategory.lean` 和 `SpCategory.lean` 都遵循同样的模式：定义对象类型、定义态射、验证范畴公理。理解 Set 范畴是理解 UFPF 中更复杂范畴的第一步。
