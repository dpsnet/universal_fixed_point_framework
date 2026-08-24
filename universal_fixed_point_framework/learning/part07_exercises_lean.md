# Part 7：习题与 Lean 4 形式化路径

> 目标：通过分级习题和 Lean 4 形式化项目，将范畴论知识转化为可验证的证明能力。

## 7.1 习题分级

### Level 1：入门（对应 Part 1-2）

**习题 1.1**：验证 $\mathbf{Set}$ 满足范畴公理：结合律、单位律。

**习题 1.2**：设 $\mathcal{C}$ 是范畴，$X, Y \in \mathrm{Ob}(\mathcal{C})$。证明若 $X$ 与 $Y$ 都初始，则 $X \cong Y$。

**习题 1.3**：在 MUFPF 的 $\mathbf{Rec}$ 中，恒等态射 $\mathrm{id}_R$ 是什么？验证它满足单位律。

**习题 2.1**：设 $F, G: \mathcal{C} \to \mathcal{D}$ 是函子，$\alpha: F \Rightarrow G$ 是自然变换。证明若每个 $\alpha_X$ 是同构，则 $\alpha^{-1}: G \Rightarrow F$ 也是自然变换。

**习题 2.2**：证明伴随对的两种定义等价：
- Hom 集合自然同构：$\mathrm{Hom}_{\mathcal{D}}(L(X), Y) \cong \mathrm{Hom}_{\mathcal{C}}(X, R(Y))$
- 单位 $\eta$ 与余单位 $\varepsilon$ 满足三角恒等式

**习题 2.3**：在 $D \dashv R$ 中，单位 $\eta: \mathrm{id}_{\mathbf{Rec}_D} \to R \circ D$ 的物理含义是什么？余单位 $\varepsilon: D \circ R \to \mathrm{id}_{\mathbf{Sp}}$ 呢？

### Level 2：进阶（对应 Part 3-4）

**习题 3.1**：在 $\mathbf{Set}$ 中构造两个集合的积与余积，并验证其泛性质。

**习题 3.2**：证明：若范畴 $\mathcal{C}$ 有等化子和有限积，则它有拉回。

**习题 3.3**：设 $(T, \eta, \mu)$ 是范畴 $\mathcal{C}$ 上的单子。验证 Eilenberg-Moore 范畴 $\mathcal{C}^T$ 满足范畴公理。

**习题 3.4**：解释 Paper XIX 中 $T = \mathcal{L} \circ \iota$ 为何是恒等函子，并写出其 Eilenberg-Moore 范畴与 $\mathbf{Rec}_{\text{id}}$ 同构的映射。

**习题 4.1**：设 $M$ 是拓扑空间，$\mathcal{F}$ 是 $M$ 上的常值层。验证层公理（局域性与粘合性）。

**习题 4.2**：构造一个预层但不是层的例子。（提示：在 $S^1$ 上考虑常值预层的某些变体。）

**习题 4.3**：验证 Grothendieck 纤维化的 Cartesian 提升满足万有性质。

**习题 4.4**：为 Paper XXI 中的 Temp 纤维化写出：一个基对象、一个纤维对象、一个截面、一个 Cartesian 提升。

### Level 3：精通（对应 Part 5-6）

**习题 5.1**：在严格 2-范畴中，验证水平复合与垂直复合的交换律（中间交换律）。

**习题 5.2**：将 Paper V 中 $D_2$ 的 4 条 2-函子公理写成具体等式。

**习题 5.3**：解释为什么 ∞-范畴中所有 $n \ge 2$ 的态射可逆这一条件，使其适合描述同伦论。

**习题 6.1**：为 Paper XXI 中的六个纤维化实例各构造一个具体的物理截面。

**习题 6.2**：画出 Paper XIX 三层伴随对嵌套的示意图，并标出每个函子的方向。

**习题 6.3**：选择 Part 6 中列出的一个"未来方向"（Kan 延拓、topos、导出范畴等），说明它可能如何应用于 MUFPF 的某个开放问题。

## 7.2 Lean 4 形式化路径

MUFPF 已有形式化仓库 `MUFPFormalization`（Lean 4）。以下是从零开始的形式化学习路径。

### 前置准备

1. 安装 Lean 4 工具链：`elan`, `lake`
2. 熟悉 Mathlib 基础：
   - `Mathlib.CategoryTheory.Category`
   - `Mathlib.CategoryTheory.Functor`
   - `Mathlib.CategoryTheory.NatTrans`
   - `Mathlib.CategoryTheory.Adjunction`
   - `Mathlib.CategoryTheory.Limits`
   - `Mathlib.CategoryTheory.Monad`
   - `Mathlib.CategoryTheory.Sites.Sheaf`

### 入门项目

**项目 A：证明 $\mathbf{Set}$ 是范畴**

```lean
import Mathlib.CategoryTheory.Category.Basic

def SetCat : Type (u+1) := Type u

instance : Category.{u, u+1} SetCat where
  Hom X Y := X → Y
  id X := fun x => x
  comp f g := fun x => g (f x)
  id_comp := by intros; rfl
  comp_id := by intros; rfl
  assoc := by intros; rfl
```

**项目 B：定义一个小型谱范畴并构造谱化函子**

```lean
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic

-- 简化的递归系统：仅包含类型和自映射
structure RecSys where
  S : Type
  Φ : S → S

structure SpecObj where
  H : Type
  A : H → H

-- 谱化函子：从递归系统到谱对象
-- 此处仅为类型签名示意，实际 MUFPF 中 A_R = -log U_R
```

### 进阶项目

**项目 C：形式化一个伴随对**

参考 Mathlib：

```lean
import Mathlib.CategoryTheory.Adjunction.Basic

-- 定义两个范畴和函子，并证明它们伴随
variable (C D : Type _) [Category C] [Category D]
variable (L : C ⥤ D) (R : D ⥤ C)

-- 构造伴随需要单位、余单位和三角恒等式
#check Adjunction.mkOfHomEquiv
```

**项目 D：形式化一个 Grothendieck 纤维化**

参考 Mathlib 中的纤维范畴相关模块：

```lean
import Mathlib.CategoryTheory.FiberedCategory.HomLift
-- 或相关纤维化定义
```

### 精通项目

**项目 E：为 Paper XIX 中的 $\mathcal{L} \dashv \iota$ 构造 Lean 证明**

这需要：
1. 定义 $\mathbf{Rec}_{\text{id}}$ 作为全子范畴
2. 定义静态化函子 $\mathcal{L}$
3. 构造单位与余单位
4. 验证三角恒等式

**项目 F：为 Paper XXI 中的 Temp 纤维化构造 Lean 骨架**

这需要：
1. 定义基范畴（温度参数范畴）
2. 定义纤维范畴（固定温度下的谱对象）
3. 定义总范畴
4. 构造投影函子
5. 证明 Cartesian 提升存在

## 7.3 MUFPF 现有形式化模块参考

| 模块 | 文件 | 对应内容 |
|------|------|---------|
| `SilenceHierarchy.lean` | MUFPFormalization | S1-S4 静默层次包含关系 |
| `StaticTopologyFormalization.lean` | MUFPFormalization | Paper XIX 静态拓扑嵌入 |
| `NoiseCategory.lean` | MUFPFormalization | Paper XIX 随机噪声嵌入 |
| `SilenceHierarchyDeepened.lean` | MUFPFormalization | Paper XIX §15 静默深化 |
| `ContextualitySheaf.lean` | MUFPFormalization | Kochen-Specker 定理的层翻译 |
| `eft_slice_category.py` | Paper I 附录 | Slice category 数值原型 |

## 7.4 练习

1. 完成项目 A：在 Lean 4 中证明 `SetCat` 是范畴。
2. 完成项目 B 的类型签名部分，思考 `A_R = -log U_R` 在 Lean 中需要哪些 Mathlib 导入。
3. 阅读 `Mathlib.CategoryTheory.Adjunction.Basic` 文档，用 `Adjunction.mkOfHomEquiv` 构造一个小伴随对。
4. 在 MUFPF 形式化仓库中找到一个已有定理，尝试理解其证明结构并写出 3 行总结。

## 7.5 关键要点

- 习题按难度分级，覆盖 Part 1-6 的核心概念。
- Lean 4 形式化从 $\mathbf{Set}$ 范畴开始，逐步过渡到伴随、纤维化、层论。
- MUFPF 已有丰富的形式化模块，可作为学习和扩展的模板。
- 形式化能力是验证 MUFPF 理论严格性的核心技能。
