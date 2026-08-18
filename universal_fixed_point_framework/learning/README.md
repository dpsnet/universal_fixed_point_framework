# UFPF 范畴论学习路线图：从入门到精通

> 本学习资料面向通用不动点范畴框架（Universal Fixed Point Framework, UFPF）研究者，将标准范畴论概念与 UFPF 论文体系中的具体应用一一对应。

## 认知状态声明

> **本资料仅涉及 UFPF 框架的数学与范畴论结构。**
>
> UFPF 作为物理理论目前仍处于**预研阶段**：其物理预言（如耦合常数、禁闭尺度、anyon 编织相位、引力修正等）需经实验检验，且尚未获得学术界的广泛认可。
>
> 形式化机证（Lean 4 / Mathlib）与范畴论推导保证的是**数学自洽性**——即在给定公理与定义的前提下，定理在形式系统内部无矛盾。数学自洽性**不自动蕴含**物理真理性、实验符合性或学术共同体认可。
>
> 学习时应区分三个独立层级：
> 1. **数学自洽性**（形式证明可验证）
> 2. **物理对应性**（需实验/观测验证）
> 3. **学术界认可**（需同行评审与独立复现）

## 目录

| 文件 | 主题 | 难度 | 目标 |
|------|------|------|------|
| [part01_basics.md](part01_basics.md) | 范畴、对象、态射、同构 | 入门 | 能读懂 UFPF 中 $\mathbf{Rec}$ 与 $\mathbf{Sp}$ 的定义 |
| [part02_functors_natural_transformations_adjoints.md](part02_functors_natural_transformations_adjoints.md) | 函子、自然变换、伴随 | 入门→进阶 | 理解谱化函子 $D \dashv R$ 的核心结构 |
| [part03_limits_colimits_monads.md](part03_limits_colimits_monads.md) | 极限/余极限、单子、Kleisli 范畴 | 进阶 | 理解 $\Sigma$-$\mathbf{Rec}$ 余完备化与 $T = \mathcal{L} \circ \iota$ 单子 |
| [part04_sheaves_fibrations_stacks.md](part04_sheaves_fibrations_stacks.md) | 层、预层、Grothendieck 纤维化、栈 | 进阶→精通 | 掌握 Temp/RG/Noise 等谱丛构造 |
| [part05_higher_category_theory.md](part05_higher_category_theory.md) | 2-范畴、∞-范畴、A∞/L∞ 代数 | 精通 | 理解 $D_2: \mathbf{Rec}_2 \to \mathbf{Sp}_2$ 与层论的 2-函子形式 |
| [part06_ufpf_applications.md](part06_ufpf_applications.md) | UFPF 论文映射与定理索引 | 应用 | 将范畴工具直接对应到 Paper I~XLIV |
| [part07_exercises_lean.md](part07_exercises_lean.md) | 习题与 Lean 4 形式化路径 | 实践 | 能独立形式化简单伴随对与纤维化 |
| [part08_advanced_formalization.md](part08_advanced_formalization.md) | 形式化仓库中的高级范畴结构 | 精通→前沿 | 掌握幺半范畴、对偶、表示桥接、同伦方法 |
| [bibliography.md](bibliography.md) | 经典教材、论文与在线资源 | 参考 | 构建后续深入学习资源库 |

## 学习阶段建议

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

## 与 UFPF 核心理念的衔接

UFPF 的范畴论不是抽象游戏，而是为以下物理直觉提供严格语言：

1. **谱化 = 函子**：$D: \mathbf{Rec}_D \to \mathbf{Sp}$ 将递归动力学翻译为谱数据
2. **还原↔涌现 = 伴随**：$D \dashv R$ 的左右伴随分别对应 UV 归约与 IR 提升
3. **参数化物理 = 纤维化**：Grothendieck 纤维化将温度、能标、噪声等参数空间统一为谱族
4. **局域与整体 = 层论**：谱预层/层在弯曲时空中编码广义协变性
5. **同伦与退化 = 高阶范畴**：2-态射与 ∞-结构处理辫子静默、耗散混沌中的连续变形

## 版本

- v0.1（2026-08-18）：初始版本，覆盖 UFPF Paper I~XLIV 中范畴论工具全景
