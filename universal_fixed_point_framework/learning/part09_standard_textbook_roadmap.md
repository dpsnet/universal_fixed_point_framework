# 本教程与标准范畴论教材：Gap 填补路线图

## 本路线要解决的问题

本教程的定位是**范畴论入门与落地指南**，不是标准教材的替代物。标准教材（Awodey、Leinster、Riehl、Mac Lane 等）在定义、定理与证明上是完整的，但常见问题是：读者学完后仍不知道如何在具体理论中把范畴工具真正“用”起来。本教程则用 MUFPF（不动点与谱理论）作为可触摸的着陆场，把抽象概念映射到 `Rec`、`Sp`、`D ⊣ R`、`T = R ∘ D`、谱丛等具体构造。

因此，学习者的最佳策略是**并行阅读、互相补缺**。本路线要解决的核心问题是：

1. **教材的抽象 vs 本教程的具体**：标准教材给出完整定义和证明，但缺少能在 Lean 中直接验证的“活例子”；本教程提供 `Rec`/`Sp` 等具体范畴和代码直觉，但压缩了部分证明细节。
2. **两套话语体系的对齐**：读者不知道本教程的哪一部分对应 Awodey、Leinster、Riehl 或 Mac Lane 的哪一章，难以在需要时切换回标准教材补足严密性。
3. **从“看懂记号”到“能写证明”**：本教程提到 Lean 4 / Mathlib，但需要与教材章节同步的验证任务，才能避免“读完仍然不会形式化”。

本路线通过**并行阅读 + 三遍学习法**，把本教程、经典范畴论教材和 Lean 4 形式化任务按主题一一对应，让两套资源互为补充。

## 目标读者

- 已经读完或正在读 MUFPF `learning/` 教程，希望用标准教材补严密性的学习者。
- 有一定数学基础（至少熟悉线性代数与基本拓扑/分析），想从范畴论角度理解 MUFPF 论文的读者。
- 希望最终能在 Lean 4 / Mathlib 中形式化简单范畴构造的研究者或工程师。

## 预期收益

完成本路线后，你应该能够：

- 独立阅读标准范畴论教材中的定义、定理与证明，并用 MUFPF 中的例子验证理解。
- 把 MUFPF 论文中出现的构造（`Rec`、`Sp`、`D ⊣ R`、`T = R ∘ D`、谱丛、Grothendieck 纤维化、Cartesian 提升等）准确地映射到范畴论语汇。
- 在 Lean 4 中形式化简单范畴构造（如 `Set` 范畴、伴随对、极限、单子实例），并理解 Mathlib 范畴论模块的组织方式。
- 具备进一步阅读 MUFPF 高阶论文（层、栈、∞-范畴、谱流形）所需的范畴论基础。

> 本路线把本教程（`learning/` 下的 Part 00~08）与经典范畴论教材按主题一一对应，便于读者在“快速建立直觉”和“补足数学严密性”之间切换。
>
> 基本策略：**本教程负责动机、例子与代码直觉，标准教材负责定义、定理与证明，Lean 4 代码负责验证理解。**

## 两套资源之间的 Gap

| Gap 编号 | 标准教材提供什么 | 本教程提供什么 |
|----------|------------------|----------------|
| **Gap 1：从抽象到具体** | 完整定义、定理、证明、反例；覆盖所有标准构造。 | `Rec`、`Sp`、`D ⊣ R`、谱丛、Grothendieck 纤维化等可在 Lean 中直接形式化的具体例子。 |
| **Gap 2：从例子到证明** | 以 `Set`、`Grp`、`Top` 为例说明定义，但例子和代码实现脱节。 | 每个概念都给出“代码直觉”和 `Mathlib` 对应，但许多证明细节被压缩为“可验证的直觉”。 |
| **Gap 3：从纸笔到 Lean** | 通常是纯数学表述，不会告诉你 `Category`、`Functor`、`Adjunction` 等类型类如何组织。 | 直接指向 `Mathlib.CategoryTheory.*` 中的定义，鼓励用 Lean 复现小构造。 |
| **Gap 4：从入门到落地** | 教会范畴论的“语言”，但很少教人如何把它嵌入一个原创理论。 | 以 MUFPF 为案例，展示如何把伴随、极限、层、∞-范畴等工具用于不动点与谱理论的原创研究。 |

阅读建议：**标准教材负责回答“是什么 / 为什么”，本教程负责回答“怎么用 / 在代码里长什么样”。** 当本教程说“这是伴随对”时，如果想知道伴随对的完整等价定义，就去 Awodey 第 9 章或 Riehl 第 4 章；当教材读完“极限”却不知道怎么验证时，回到本教程的 `Σ-Rec` 余完备化例子或 Lean 的 `Limits.lean`。

## 总体策略：三遍学习法

1. **第一遍——直觉先行**：读完本教程对应章节，看懂它要解决什么问题，再翻标准教材查核心定义。
2. **第二遍——严密补缺**：反过来读标准教材的对应章节，把本教程中的例子当作习题验证。
3. **第三遍——形式化落地**：在 Lean 4 中复现简单构造，确认自己不只是“读懂了记号”。

---

## 阶段对照表

| 阶段 | 学习目标 | 本教程（落地与代码直觉） | 标准教材（定义与证明） | 内部论文 / Lean 代码 | 时间建议 |
|------|---------|--------------------------|------------------------|---------------------|---------|
| **0. 热身** | 建立“对象 + 保持结构的映射”直觉 | `part00_warmup.md`<br>`case01_set_category.md` | Awodey 第 1 章<br>Leinster 第 1 章 | Paper I §2<br>`Mathlib.CategoryTheory.Category.Basic` | 0.5 ~ 1 周 |
| **1. 范畴基础** | 熟练掌握范畴、态射、同构、积/余积、对偶 | `part01_basics.md` | Awodey 1–5 章<br>Leinster 1–3 章<br>Mac Lane I–III | Paper I §2、附录<br>`SetCategory.lean` | 1 ~ 2 周 |
| **2. 函子与自然变换** | 理解函子、自然变换、等价、Yoneda、表示 | `part02_functors_natural_transformations_adjoints.md`（前半） | Awodey 6–8 章<br>Leinster 第 4 章<br>Riehl 1–4 章 | Paper I 附录 A.3<br>`Functor.lean`<br>`Yoneda.lean` | 1 ~ 2 周 |
| **3. 伴随对** | 掌握伴随对的四种定义、单位/余单位、例子 | `part02_functors_natural_transformations_adjoints.md`（后半） | Awodey 9–10 章<br>Leinster 5–6 章<br>Riehl 第 5 章<br>Mac Lane IV、VII | Paper I `D ⊣ R`<br>`paper1_philosophy.md`<br>`Adjunction.lean`<br>`case02_adjunction.md` | 2 ~ 3 周 |
| **4. 极限与余极限** | 能用泛性质理解积、余积、等化子、余等化子、拉回、推出 | `part03_limits_colimits_monads.md`（前半） | Riehl 第 6 章<br>Mac Lane V–VI<br>Leinster 第 5 章 | `Limits.lean`<br>切片范畴实例 | 2 周 |
| **5. 单子与 Kleisli** | 理解单子作为“自函子上的代数结构”、Kleisli 范畴、Eilenberg-Mooe 范畴 | `part03_limits_colimits_monads.md`（后半） | Mac Lane XII<br>Awodey 第 10 章后半<br>Riehl 第 5 章相关习题 | Paper I 中 `T = R ∘ D`<br>`T = 𝓛 ∘ ι`<br>`Monad.lean` | 1 ~ 2 周 |
| **6. 层与 Grothendieck 纤维化** | 掌握预层、层公理、Cartesian 提升、下降条件、谱栈 | `part04_sheaves_fibrations_stacks.md`<br>`paper_reading_guides/paper21_guide.md` | Riehl 第 7 章<br>Mac Lane 第 IX 章<br>Borceux 卷 2 第 8 章<br>Stacks Project 第 6 章 | Paper XVI、XIX、XXI、XXVII–XXIX<br>`FiberedCategory.lean`<br>`Sites.Sheaf.lean`<br>`case03_spectral_equivalence.md` | 3 ~ 4 周 |
| **7. 高阶与无穷范畴** | 了解 2-范畴、∞-范畴、A∞/L∞ 代数、模型范畴 | `part05_higher_category_theory.md`<br>`part08_advanced_formalization.md` | Riehl *Elements of ∞-Category Theory* 1–3 章<br>Kerodon 第 1 章<br>Riehl *Categorical Homotopy Theory* | Paper V、IX、XXI<br>`Braided.lean`<br>`SpectralFlowHomotopy.lean` | 3 ~ 5 周 |
| **8. MUFPF 应用** | 把范畴工具映射到 MUFPF 论文具体问题 | `part06_mufpf_applications.md` | Connes *Noncommutative Geometry* 1–2 章<br>Kassel *Quantum Groups*<br>Etingof et al. *Tensor Categories*<br>Atiyah–Patodi–Singer *Spectral Asymmetry* | Paper X–XV、XVII、XX、XXV | 按需 |
| **9. Lean 4 形式化** | 能在 Lean 中形式化简单范畴构造 | `part07_exercises_lean.md`<br>`part07_solutions.md`<br>`lean_case_studies/` | *Theorem Proving in Lean 4*<br>Mathlib4 范畴论文档 | `MUFPFormalization/`<br>`PresurveyFormalization/` | 贯穿全程 |

---

## 详细周计划

### 第 0~1 周：热身与范畴基础

**本教程**

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

**本教程**

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

### 第 4~6 周：伴随对（MUFPF 核心）

**本教程**

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
2. 对 MUFPF 中的 `D ⊣ R`，写出单位 `η : 1 → R ∘ D` 和余单位 `ε : D ∘ R → 1` 的物理含义（UV 归约 / IR 提升）。
3. 在 Lean 中证明一个自己构造的小伴随对。

**掌握标准**：看到 `F ⊣ G` 能立即画出三角等式，并能在 MUFPF 论文中识别哪个函子是左伴随、哪个是右伴随。

---

### 第 7~8 周：极限与余极限

**本教程**

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

**掌握标准**：能把 MUFPF 中“把一族谱对象粘合成整体”的描述翻译成余极限语言。

---

### 第 9~10 周：单子与 Kleisli

**本教程**

- 读 `part03_limits_colimits_monads.md` 第 5–8 节。
- 对照 Paper I 中 `T = R ∘ D` 与平凡单子 `T = 𝓛 ∘ ι`。

**标准教材**

- Mac Lane 第 XII 章。
- Awodey 第 10 章后半。
- Riehl 第 5 章中的单子习题。

**练习**

1. 验证 `Maybe : Set → Set`（`X ↦ X + {*}`）构成单子。
2. 对 MUFPF 的 `T = R ∘ D`，写出 `μ : T² → T` 与 `η : 1 → T`。
3. 比较 Kleisli 范畴与 Eilenberg-Moore 范畴在该单子下的区别。

**掌握标准**：能把 MUFPF 中的“谱化后再还原”操作识别为单子的乘法。

---

### 第 11~14 周：层、纤维化与栈

**本教程**

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

**本教程**

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

**本教程**

- 读 `part06_mufpf_applications.md`。
- 选择自己关心的应用领域论文（Paper X–XV、XVII、XX、XXV）。

**标准教材**

- 非交换几何：Connes 第 1–2 章。
- 辫子/张量范畴：Kassel、Etingof et al.。
- 谱几何：Atiyah–Patodi–Singer。

**练习**

1. 选一个 MUFPF 应用论文，用范畴论语汇重写它的核心结论。
2. 为该论文中的一个引理或定理补充 Lean 形式化（哪怕是非常小的引理）。

**掌握标准**：能向他人用 3 句话说明某篇 MUFPF 论文“用了什么范畴工具、为什么需要它、结论是什么”。

---

## 常见误区与纠正

| 误区 | 纠正 |
|------|------|
| “读完本教程就等于学会了范畴论。” | 本教程是**入门与落地指南**，不是完整教材。定理证明、深层例子和反例仍需标准教材补全。 |
| “只看标准教材就够了。” | 没有具体例子（如 `Rec`、`Sp`、谱丛）和 Lean 代码，抽象的极限/伴随容易变成纯符号游戏。 |
| “Lean 代码看懂就行。” | 形式化能暴露直觉中的漏洞。建议至少独立复现一个小引理。 |
| “先学完所有范畴论再读 MUFPF 论文。” | MUFPF 论文本身就是很好的学习材料。可以在读论文时缺什么补什么。 |

---

## 与 README 中“学习阶段建议”的关系

- `README.md` 给出的是**按学习阶段划分**的本教程内部阅读顺序。
- 本文件给出的是**本教程 ↔ 标准教材**的并行阅读方案，明确每部分由谁负责。
- 两者结合使用：先用 README 规划每周看哪几份资料，再用本文件找到对应的标准教材章节和 Lean 代码任务。

---

## 版本

- v0.2（2026-08-19）：重构为 Gap 填补路线图，强调标准教材负责定义与证明、本教程负责落地与代码直觉。
- v0.1（2026-08-19）：初始版本，覆盖 Part 00~08 与 Awodey / Leinster / Riehl / Mac Lane 等经典教材的对照。
