# UFPF 教程与标准教材对照学习路线

> 本路线把 UFPF 学习资料（`learning/` 下的 Part 00~08）与经典范畴论教材按主题一一对应，便于读者在“快速建立直觉”和“补足数学严密性”之间切换。
>
> 基本策略：**UFPF 教程负责动机与例子，标准教材负责定义、定理与证明，Lean 4 代码负责验证理解。**

## 总体策略：三遍学习法

1. **第一遍——直觉先行**：读完 UFPF 教程对应章节，看懂它要解决什么问题，再翻标准教材查核心定义。
2. **第二遍——严密补缺**：反过来读标准教材的对应章节，把 UFPF 中的例子当作习题验证。
3. **第三遍——形式化落地**：在 Lean 4 中复现简单构造，确认自己不只是“读懂了记号”。

---

## 阶段对照表

| 阶段 | 学习目标 | UFPF 教程 | 标准教材 | 内部论文 / Lean 代码 | 时间建议 |
|------|---------|-----------|---------|---------------------|---------|
| **0. 热身** | 建立“对象 + 保持结构的映射”直觉 | `part00_warmup.md`<br>`case01_set_category.md` | Awodey 第 1 章<br>Leinster 第 1 章 | Paper I §2<br>`Mathlib.CategoryTheory.Category.Basic` | 0.5 ~ 1 周 |
| **1. 范畴基础** | 熟练掌握范畴、态射、同构、积/余积、对偶 | `part01_basics.md` | Awodey 1–5 章<br>Leinster 1–3 章<br>Mac Lane I–III | Paper I §2、附录<br>`SetCategory.lean` | 1 ~ 2 周 |
| **2. 函子与自然变换** | 理解函子、自然变换、等价、Yoneda、表示 | `part02_functors_natural_transformations_adjoints.md`（前半） | Awodey 6–8 章<br>Leinster 第 4 章<br>Riehl 1–4 章 | Paper I 附录 A.3<br>`Functor.lean`<br>`Yoneda.lean` | 1 ~ 2 周 |
| **3. 伴随对** | 掌握伴随对的四种定义、单位/余单位、例子 | `part02_functors_natural_transformations_adjoints.md`（后半） | Awodey 9–10 章<br>Leinster 5–6 章<br>Riehl 第 5 章<br>Mac Lane IV、VII | Paper I `D ⊣ R`<br>`paper1_philosophy.md`<br>`Adjunction.lean`<br>`case02_adjunction.md` | 2 ~ 3 周 |
| **4. 极限与余极限** | 能用泛性质理解积、余积、等化子、余等化子、拉回、推出 | `part03_limits_colimits_monads.md`（前半） | Riehl 第 6 章<br>Mac Lane V–VI<br>Leinster 第 5 章 | `Limits.lean`<br>切片范畴实例 | 2 周 |
| **5. 单子与 Kleisli** | 理解单子作为“自函子上的代数结构”、Kleisli 范畴、Eilenberg-Mooe 范畴 | `part03_limits_colimits_monads.md`（后半） | Mac Lane XII<br>Awodey 第 10 章后半<br>Riehl 第 5 章相关习题 | Paper I 中 `T = R ∘ D`<br>`T = 𝓛 ∘ ι`<br>`Monad.lean` | 1 ~ 2 周 |
| **6. 层与 Grothendieck 纤维化** | 掌握预层、层公理、Cartesian 提升、下降条件、谱栈 | `part04_sheaves_fibrations_stacks.md`<br>`paper_reading_guides/paper21_guide.md` | Riehl 第 7 章<br>Mac Lane 第 IX 章<br>Borceux 卷 2 第 8 章<br>Stacks Project 第 6 章 | Paper XVI、XIX、XXI、XXVII–XXIX<br>`FiberedCategory.lean`<br>`Sites.Sheaf.lean`<br>`case03_spectral_equivalence.md` | 3 ~ 4 周 |
| **7. 高阶与无穷范畴** | 了解 2-范畴、∞-范畴、A∞/L∞ 代数、模型范畴 | `part05_higher_category_theory.md`<br>`part08_advanced_formalization.md` | Riehl *Elements of ∞-Category Theory* 1–3 章<br>Kerodon 第 1 章<br>Riehl *Categorical Homotopy Theory* | Paper V、IX、XXI<br>`Braided.lean`<br>`SpectralFlowHomotopy.lean` | 3 ~ 5 周 |
| **8. UFPF 应用** | 把范畴工具映射到 UFPF 论文具体问题 | `part06_ufpf_applications.md` | Connes *Noncommutative Geometry* 1–2 章<br>Kassel *Quantum Groups*<br>Etingof et al. *Tensor Categories*<br>Atiyah–Patodi–Singer *Spectral Asymmetry* | Paper X–XV、XVII、XX、XXV | 按需 |
| **9. Lean 4 形式化** | 能在 Lean 中形式化简单范畴构造 | `part07_exercises_lean.md`<br>`part07_solutions.md`<br>`lean_case_studies/` | *Theorem Proving in Lean 4*<br>Mathlib4 范畴论文档 | `UFPFormalization/`<br>`PresurveyFormalization/` | 贯穿全程 |

---

## 详细周计划

### 第 0~1 周：热身与范畴基础

**UFPF**

- 读 `part00_warmup.md`，完成学前自测。
- 读 `part01_basics.md` 第 1–3 节。
- 浏览 `case01_set_category.md`，确认 `Set` 范畴满足范畴三公理。

**标准教材**

- Awodey 第 1–3 章 或 Leinster 第 1–2 章。
- 重点：范畴、函子（预告）、单/满态射、同构、积/余积。

**练习**

1. 验证 `Set`、`Vec_k`、`Poset`、`Grp` 都满足范畴三公理。
2. 在 `Set` 中构造两个集合的积与余积，并验证泛性质。
3. 在 Lean 中打开 `Mathlib.CategoryTheory.Category.Basic`，查看 `Category` 类型类定义。

**掌握标准**：看到 `D : Rec → Sp` 这样的记号，能立刻认出它是一个**函子**而非普通映射。

---

### 第 2~3 周：函子、自然变换、Yoneda

**UFPF**

- 读 `part02_functors_natural_transformations_adjoints.md` 第 1–4 节。
- 精读 `paper1_appendix.md` 中 Yoneda 与 Freyd 定理相关段落。

**标准教材**

- Awodey 第 6–8 章。
- Leinster 第 4 章。
- Riehl 第 2 章（自然变换与等价）。

**练习**

1. 对 `Set` 上的恒等函子与幂集函子 `P : Set → Set`，写出一个自然变换 `η_X : X → P(X)`（提示：`x ↦ {x}`）。
2. 用 Yoneda 引理证明 `Nat(h_c, F) ≅ F(c)`。
3. 在 Lean 中完成 `case02_adjunction.md` 中的 `const ⊣ lim` 小练习。

**掌握标准**：能独立判断一个“映射族”是否自然，并能用 Yoneda 把“对象决定 functor 的表示”这一说法翻译成可验证的等式。

---

### 第 4~6 周：伴随对（UFPF 核心）

**UFPF**

- 读 `part02_functors_natural_transformations_adjoints.md` 第 5–8 节。
- 读 `paper1_philosophy.md` 中关于 `D ⊣ R` 的物理诠释。
- 对照 Paper I 中 `D : Rec_D → Sp` 与 `R : Sp → Rec_D` 的定义。

**标准教材**

- Awodey 第 9–10 章。
- Leinster 第 5–6 章。
- Riehl 第 4 章（伴随）。
- Mac Lane 第 IV 章（范畴等价）和第 VII 章（伴随）。

**练习**

1. 用四种等价定义证明 `Free ⊣ Forget : Grp ⇆ Set`。
2. 对 UFPF 中的 `D ⊣ R`，写出单位 `η : 1 → R ∘ D` 和余单位 `ε : D ∘ R → 1` 的物理含义（UV 归约 / IR 提升）。
3. 在 Lean 中证明一个自己构造的小伴随对。

**掌握标准**：看到 `F ⊣ G` 能立即画出三角等式，并能在 UFPF 论文中识别哪个函子是左伴随、哪个是右伴随。

---

### 第 7~8 周：极限与余极限

**UFPF**

- 读 `part03_limits_colimits_monads.md` 第 1–4 节。
- 重点理解 `Σ-Rec` 余完备化中的余极限构造。

**标准教材**

- Riehl 第 6 章。
- Mac Lane 第 V–VI 章。
- Leinster 第 5 章。

**练习**

1. 证明 `Set` 中任意小图的极限等于锥上的相容选择集合。
2. 构造一个拉回，并验证它满足泛性质。
3. 用 Lean 的 `CategoryTheory.Limits` 定义一个简单图的极限（如 `2 → Set`）。

**掌握标准**：能把 UFPF 中“把一族谱对象粘合成整体”的描述翻译成余极限语言。

---

### 第 9~10 周：单子与 Kleisli

**UFPF**

- 读 `part03_limits_colimits_monads.md` 第 5–8 节。
- 对照 Paper I 中 `T = R ∘ D` 与平凡单子 `T = 𝓛 ∘ ι`。

**标准教材**

- Mac Lane 第 XII 章。
- Awodey 第 10 章后半。
- Riehl 第 5 章中的单子习题。

**练习**

1. 验证 `Maybe : Set → Set`（`X ↦ X + {*}`）构成单子。
2. 对 UFPF 的 `T = R ∘ D`，写出 `μ : T² → T` 与 `η : 1 → T`。
3. 比较 Kleisli 范畴与 Eilenberg-Moore 范畴在该单子下的区别。

**掌握标准**：能把 UFPF 中的“谱化后再还原”操作识别为单子的乘法。

---

### 第 11~14 周：层、纤维化与栈

**UFPF**

- 读 `part04_sheaves_fibrations_stacks.md` 全部。
- 读 `paper_reading_guides/paper21_guide.md`。
- 精读 `notes/00_foundations/spectral_Grothendieck_fibration.md`。

**标准教材**

- Riehl 第 7 章（层与纤维范畴）。
- Mac Lane 第 IX 章（层）。
- Borceux 卷 2 第 8 章（纤维范畴）。
- Stacks Project 第 6 章（层论严格处理）。

**练习**

1. 用开集范畴 `Op(X)` 上的预层定义，验证层公理对常值预层何时成立。
2. 给定基范畴 `B` 与 `Set` 上的离散纤维化，构造一个 Cartesian 提升。
3. 在 Lean 中查看 `Mathlib.CategoryTheory.FiberedCategory` 中的 `IsCartesian` 定义。
4. 把 Temp/RG/Noise 谱丛的物理参数翻译成基范畴对象与纤维。

**掌握标准**：能独立判断一个谱丛中的态射是否为 Cartesian，理解“下降条件”与层公理的异同。

---

### 第 15~19 周：高阶范畴与无穷范畴

**UFPF**

- 读 `part05_higher_category_theory.md`。
- 读 `part08_advanced_formalization.md` 第 1–4 节。
- 对照 Paper V（`D_2 : Rec_2 → Sp_2`）与 Paper IX。

**标准教材**

- Riehl *Elements of ∞-Category Theory* 第 1–3 章。
- Kerodon 第 1 章。
- Riehl *Categorical Homotopy Theory*（模型范畴部分）。

**练习**

1. 给出一个 2-范畴的小例子（如 `Cat` 自身）。
2. 比较严格 2-范畴与双范畴的区别。
3. 用 A∞ 代数的结构方程解释“高阶括号的结合性直到同伦”。
4. 在 Lean 中阅读 `Braided.lean`，找出辫子结构满足的单位公理。

**掌握标准**：能解释为什么谱流、辫子静默等物理现象需要 2-态射或 ∞-结构来形式化。

---

### 第 20 周起：应用与形式化（按需）

**UFPF**

- 读 `part06_ufpf_applications.md`。
- 选择自己关心的应用领域论文（Paper X–XV、XVII、XX、XXV）。

**标准教材**

- 非交换几何：Connes 第 1–2 章。
- 辫子/张量范畴：Kassel、Etingof et al.。
- 谱几何：Atiyah–Patodi–Singer。

**练习**

1. 选一个 UFPF 应用论文，用范畴论语汇重写它的核心结论。
2. 为该论文中的一个引理或定理补充 Lean 形式化（哪怕是非常小的引理）。

**掌握标准**：能向他人用 3 句话说明某篇 UFPF 论文“用了什么范畴工具、为什么需要它、结论是什么”。

---

## 常见误区与纠正

| 误区 | 纠正 |
|------|------|
| “读完 UFPF 教程就等于学会了范畴论。” | UFPF 教程是**应用导向的速写**。定理证明、深层例子和反例仍需标准教材补全。 |
| “只看标准教材就够了。” | 没有具体例子（如 `Rec`、`Sp`、谱丛），抽象的极限/伴随容易变成纯符号游戏。 |
| “Lean 代码看懂就行。” | 形式化能暴露直觉中的漏洞。建议至少独立复现一个小引理。 |
| “先学完所有范畴论再读 UFPF 论文。” | UFPF 论文本身就是很好的学习材料。可以在读论文时缺什么补什么。 |

---

## 与 README 中“学习阶段建议”的关系

- `README.md` 给出的是**按 UFPF 内部结构划分**的阶段。
- 本文件给出的是**UFPF 教程 ↔ 标准教材**的并行阅读方案。
- 两者结合使用：先用 README 规划每周看哪几份 UFPF 资料，再用本文件找到对应的标准教材章节。

---

## 版本

- v0.1（2026-08-19）：初始版本，覆盖 Part 00~08 与 Awodey / Leinster / Riehl / Mac Lane 等经典教材的对照。
