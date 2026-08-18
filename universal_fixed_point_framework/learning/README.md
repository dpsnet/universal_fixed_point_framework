# UFPF 范畴论学习路线图：从入门到精通

> 本学习资料面向通用不动点范畴框架（Universal Fixed Point Framework, UFPF）研究者，将标准范畴论概念与 UFPF 论文体系中的具体应用一一对应。

## 认知状态声明

> **本资料仅涉及 UFPF 框架的数学与范畴论结构。**
>
> UFPF 本质上是一个以递归-谱翻译为核心的**数学/范畴论框架**。物理领域中的应用（如 QCD、引力、粒子谱、黑洞 QNM 等）只是该框架在特定领域的**理论实例**，其物理正确性仍需实验检验，且尚未获得学术界的广泛认可。
>
> 形式化机证（Lean 4 / Mathlib）与范畴论推导保证的是**数学自洽性**——即在给定公理与定义的前提下，定理在形式系统内部无矛盾。数学自洽性**不自动蕴含**物理真理性、实验符合性或学术共同体认可。
>
> 学习时应区分三个独立层级：
> 1. **数学自洽性**（形式证明可验证）
> 2. **物理实例的正确性**（需实验/观测验证）
> 3. **学术界认可**（需同行评审与独立复现）

## 术语标准化说明

> 本学习资料采用**标准范畴论术语**。例如，Grothendieck 纤维化中的 lifting 使用 **"Cartesian 提升"**（对应英文 Cartesian lifting）。
>
> UFPF 原论文中曾使用 **"Cartan 提升"** 表述同一概念，属非标准用法。学习资料和 UFPF 论文已同步修正为标准术语，但读者可能在旧版本或外部引用中遇到 "Cartan 提升"，可视为 "Cartesian 提升" 的同义旧称。

## 已覆盖范畴概念速查

| 概念 | 说明 | 所在文件 |
|------|------|---------|
| 范畴、对象、态射、同构 | 基础定义与 UFPF 中的 $\mathbf{Rec}$、$\mathbf{Sp}$ | [part00_warmup.md](part00_warmup.md)、[part01_basics.md](part01_basics.md) |
| 子范畴、宽子范畴、全子范畴 | 限制对象或态射的方式 | [part01_basics.md](part01_basics.md) |
| 函子、自然变换、自然同构 | 范畴之间的结构保持映射及其比较 | [part02_functors_natural_transformations_adjoints.md](part02_functors_natural_transformations_adjoints.md) |
| 伴随对、单位、余单位 | UFPF 核心：$D \dashv R$、$\mathcal{L} \dashv \iota$、$\mathcal{S}el \dashv \mathcal{D}iss$ | [part02_functors_natural_transformations_adjoints.md](part02_functors_natural_transformations_adjoints.md) |
| 极限、余极限 | 积、余积、拉回、推出等泛构造 | [part03_limits_colimits_monads.md](part03_limits_colimits_monads.md) |
| 单子、Kleisli 范畴、Eilenberg-Moore 范畴 | $T = R \circ D$、平凡单子 $T = \mathcal{L} \circ \iota$ | [part03_limits_colimits_monads.md](part03_limits_colimits_monads.md) |
| 预层、层、茎、层化 | 时空谱层、奇点的层论定义 | [part04_sheaves_fibrations_stacks.md](part04_sheaves_fibrations_stacks.md) |
| Grothendieck 纤维化、Cartesian 提升、截面 | Temp/RG/Noise/Kerr/Flt 谱丛 | [part04_sheaves_fibrations_stacks.md](part04_sheaves_fibrations_stacks.md) |
| 谱栈 | 谱丛在开集范畴上的层论推广 | [part04_sheaves_fibrations_stacks.md](part04_sheaves_fibrations_stacks.md) |
| 2-范畴、2-函子 | $D_2: \mathbf{Rec}_2 \to \mathbf{Sp}_2$ | [part05_higher_category_theory.md](part05_higher_category_theory.md) |
| ∞-范畴、A∞/L∞ 代数 | 高阶括号与同伦结构 | [part05_higher_category_theory.md](part05_higher_category_theory.md) |
| 幺半范畴、辫子幺半范畴 | $\mathbf{Rec}$ 上的张量积与辫子结构 | [part08_advanced_formalization.md](part08_advanced_formalization.md) |
| 范畴等价、Gelfand 对偶 | 谱等价、$D^{\text{id}}$ 与 Gelfand 对偶的对比 | [part08_advanced_formalization.md](part08_advanced_formalization.md) |
| 表示范畴、几何范畴 | Koopman 表示桥接、几何-谱对应 | [part08_advanced_formalization.md](part08_advanced_formalization.md) |
| 同伦、谱流 | 谱流方程的同伦不变性、辫子交叉数 | [part08_advanced_formalization.md](part08_advanced_formalization.md) |

## 目录

| 文件 | 主题 | 难度 | 目标 |
|------|------|------|------|
| [part00_warmup.md](part00_warmup.md) | 范畴论直觉热身 | 零基础 | 用 3 个熟悉例子建立"对象 + 保持结构的映射"直觉 |
| [part01_basics.md](part01_basics.md) | 范畴、对象、态射、同构 | 入门 | 能读懂 UFPF 中 $\mathbf{Rec}$ 与 $\mathbf{Sp}$ 的定义 |
| [part02_functors_natural_transformations_adjoints.md](part02_functors_natural_transformations_adjoints.md) | 函子、自然变换、伴随 | 入门→进阶 | 理解谱化函子 $D \dashv R$ 的核心结构 |
| [part03_limits_colimits_monads.md](part03_limits_colimits_monads.md) | 极限/余极限、单子、Kleisli 范畴 | 进阶 | 理解 $\Sigma$-$\mathbf{Rec}$ 余完备化与 $T = \mathcal{L} \circ \iota$ 单子 |
| [part04_sheaves_fibrations_stacks.md](part04_sheaves_fibrations_stacks.md) | 层、预层、Grothendieck 纤维化、栈 | 进阶→精通 | 掌握 Temp/RG/Noise 等谱丛构造 |
| [part05_higher_category_theory.md](part05_higher_category_theory.md) | 2-范畴、∞-范畴、A∞/L∞ 代数 | 精通 | 理解 $D_2: \mathbf{Rec}_2 \to \mathbf{Sp}_2$ 与层论的 2-函子形式 |
| [part06_ufpf_applications.md](part06_ufpf_applications.md) | UFPF 论文映射与定理索引 | 应用 | 将范畴工具直接对应到 Paper I~XLIV |
| [part07_exercises_lean.md](part07_exercises_lean.md) | 习题与 Lean 4 形式化路径 | 实践 | 能独立形式化简单伴随对与纤维化 |
| [part08_advanced_formalization.md](part08_advanced_formalization.md) | 形式化仓库中的高级范畴结构 | 精通→前沿 | 掌握幺半范畴、对偶、表示桥接、同伦方法 |
| [part07_solutions.md](part07_solutions.md) | Part 7 习题解答与提示 | 参考 | 对照检查分级习题 |
| [lean_case_studies/](lean_case_studies/) | Lean 4 实战案例 | 实践 | 从 Set 范畴、伴随对到谱等价 |
| [paper_reading_guides/](paper_reading_guides/) | 核心论文精读导引 | 应用 | Paper I / XIX / XXI 的范畴论路线 |
| [bibliography.md](bibliography.md) | 经典教材、论文与在线资源 | 参考 | 构建后续深入学习资源库 |

## 学习阶段建议

### 阶段零：热身（0.5~1 周）
- 如果你完全没接触过范畴论，先读 [part00_warmup.md](part00_warmup.md)
- 完成其中的学前自测，确认理解"对象 + 保持结构的映射"这一核心直觉
- 可选同步阅读 Awodey《Category Theory》第 1 章

### 阶段一：入门（1~2 周）
- 阅读 [part01_basics.md](part01_basics.md) 与 [part02_functors_natural_transformations_adjoints.md](part02_functors_natural_transformations_adjoints.md)
- 同步对照 UFPF Paper I §2 中 $\mathbf{Rec}$、$\mathbf{Sp}$、$D \dashv R$ 的定义
- 完成 [part07_exercises_lean.md](part07_exercises_lean.md) 中 Level 1 习题

### 阶段二：进阶（2~3 周）
- 阅读 [part03_limits_colimits_monads.md](part03_limits_colimits_monads.md) 与 [part04_sheaves_fibrations_stacks.md](part04_sheaves_fibrations_stacks.md)
- 对照 Paper XIX（静态/随机扩展）、Paper XXI（纤维化综合）、Paper XVI（层论）
- 完成 Level 2 习题，尝试用 Lean 4 证明一个小伴随对

### 阶段三：精通（持续）
- 阅读 [part05_higher_category_theory.md](part05_higher_category_theory.md)、[part06_ufpf_applications.md](part06_ufpf_applications.md) 与 [part08_advanced_formalization.md](part08_advanced_formalization.md)
- 跟踪 UFPF 形式化仓库中的 `UFPFormalization` 模块
- 尝试为 Paper XIX、Paper XXI 或形式化仓库中的高级构造补充 Lean 形式化

### 阶段四：前沿探索（按需）
本教材未系统覆盖、但可能对 UFPF 深化有价值的高级范畴工具：

| 工具 | 可能的应用场景 | 当前教材位置 |
|------|--------------|-------------|
| **Kan 延拓** | 统一不同参数空间上的谱丛构造 | [part06_ufpf_applications.md](part06_ufpf_applications.md) §6.4 |
| **充实范畴（Enriched Category）** | 内蕴处理谱间隙、LACI、度量结构 | [part06_ufpf_applications.md](part06_ufpf_applications.md) §6.4 |
| **逗号范畴（Comma Category）** | 构造谱对象之间的关系范畴 | [part06_ufpf_applications.md](part06_ufpf_applications.md) §6.4 |
| **Topos 理论** | 为时空谱层提供内蕴逻辑与几何态射 | [part04_sheaves_fibrations_stacks.md](part04_sheaves_fibrations_stacks.md) §4.5 |
| **导出范畴 / 模型范畴** | 谱复形、同伦代数、耗散系统的弱等价 | [part05_higher_category_theory.md](part05_higher_category_theory.md) §5.6 |
| **Profunctor / Distributor** | 研究 $\mathbf{Rec}$ 与 $\mathbf{Sp}$ 之间的分布对应 | [part06_ufpf_applications.md](part06_ufpf_applications.md) §6.4 |
| **Operad** | 系统组织 A∞/L∞ 代数中的高阶运算 | [part05_higher_category_theory.md](part05_higher_category_theory.md) §5.4 |
| **∞-Topos** | 高阶谱栈、同伦下降、辫子静默严格化 | [part05_higher_category_theory.md](part05_higher_category_theory.md) §5.3 |

**说明**：这些工具属于博士阶段或研究前沿范畴，当前教材仅作方向性登记。建议在遇到具体数学瓶颈时再深入学习，避免过早抽象。

## 与 UFPF 核心理念的衔接

UFPF 的范畴论不是抽象游戏，而是为以下物理直觉提供严格语言：

1. **谱化 = 函子**：$D: \mathbf{Rec}_D \to \mathbf{Sp}$ 将递归动力学翻译为谱数据
2. **还原↔涌现 = 伴随**：$D \dashv R$ 的左右伴随分别对应 UV 归约与 IR 提升
3. **参数化物理 = 纤维化**：Grothendieck 纤维化将温度、能标、噪声等参数空间统一为谱族
4. **局域与整体 = 层论**：谱预层/层在弯曲时空中编码广义协变性
5. **同伦与退化 = 高阶范畴**：2-态射与 ∞-结构处理辫子静默、耗散混沌中的连续变形

## 版本

- v0.1（2026-08-18）：初始版本，覆盖 UFPF Paper I~XLIV 中范畴论工具全景
