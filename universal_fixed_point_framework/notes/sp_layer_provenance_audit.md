# Sp 层结构溯源台账（2026-07-17 → 2026-09-05）

本文件是对「三层态射 / 主动生成层 / Sp 层结构」起源的逐提交核验记录。所有结论均以本仓库 git 对象为唯一依据，命令附于 §10，可逐条复算。凡与既有叙述不一致处，以本台账为准。

## 1. 核验方法

- 提交存在性与元数据：`git rev-parse --verify <rev>^{commit}`、`git show -s --format='%H|%ai|%s'`。
- 文件级变化：`git diff --stat <rev1> <rev2> -- <path>`、`git show --stat <rev>`。
- 内容判定：`git show <rev>:<path>` 取原文后逐行计数（层类型名、关键词、sorry），不依赖工作树文件或任何本地副本。
- 关键词计数为出现次数，行数为 `git show` 输出行数。

## 2. 十提交台账

| 短哈希 | 日期（+0800） | 消息 | 核验结果 |
|---|---|---|---|
| `8012c4f` | 2026-07-17 16:09:06 | chore: 完成 Phase29 全部开发与形式化整合 | 存在；创建 HigherSpecCategory.lean |
| `f0a3455` | 2026-07-21 01:09:31 | feat(phase31): 完成高阶∞-范畴Lean形式化骨架与配套文档更新 | 存在；该文件仍无 3-态射 |
| `80f2d92` | 2026-07-26 17:25:50 | docs: 统一将"谱翻译"替换为"谱表述"并修正范畴命名 | 存在；纯术语 |
| `27cdf8d` | 2026-07-27 19:04:50 | feat(formal_proof): 新增完整形式化体系，闭合统一3定理缺口 | 存在；首次写入 3-态射 |
| `463df34` | 2026-07-28 02:32:58 | feat: 新增d_H偏差结构分析相关代码与文档 | 存在；该文件 10+/21−（净 −11） |
| `fb0f259` | 2026-07-28 12:09:02 | refactor(lean formalization): 统一将Spec→Sp术语修正 | 存在；−174 / +299 两文件 |
| `5d4bdc2` | 2026-07-28 18:10:02 | docs: update spectral hierarchy analysis doc and formalize layer independence + IFS mapping | 存在 |
| `a3df3c5` | 2026-07-29 05:39:48 | feat: 新增四维时空涌现严格定理组与数值验证 | 存在 |
| `9cbffe1` | 2026-08-07 23:00:07 | docs: RAP-Errata/Registry v0.21——d_H 与 k_max 表述全库修正 + k_max=8 对偶映射推导与形式化 | 存在 |
| `2135296` | 2026-09-05 10:09:49 | chore(lean): 完成 UFPF 更名 MUFPF 第一阶段迁移 | 存在 |

十项全部命中，日期与消息一致。`fb0f259` 之前的路径为双层目录：

```
universal_fixed_point_framework/formal_proof/UFPFormalization/UFPFormalization/HigherSpecCategory.lean
```

`fb0f259` 起更名为 `HigherSpCategory.lean`（同目录）。

## 3. 逐条实证

### 3.1 `8012c4f`（Phase29，首建）

`HigherSpecCategory.lean`：106 行。关键字计数：SpecTwoMorphism 15、SpecThreeMorphism 0、SpecFourMorphism 0、链复形 0、coherence 0、sorry 0。

结论：确为 2-范畴（层 0 对象 + 层 1 SpHom + 层 2 SpecTwoMorphism），无 3-态射、无链复形字样。

### 3.2 `f0a3455`（Phase31，∞-范畴骨架）

该文件 108 行，SpecThreeMorphism 仍为 0，sorry 1 次。文件级变化 73 插入 / 71 删除（144 行被改写，净 +2）。整提交 20 文件、1038 插入 / 146 删除。

结论：确为「引入 ∞-范畴骨架但未加三层态射」。清单「+144/-? 行」应改为「73+/71−（144 行改写）」——+144 不是插入数。

### 3.3 `80f2d92`（术语）

108 行，层类型计数不变（Two 15 / Three 0 / Four 0）。纯术语替换。

### 3.4 `27cdf8d`（关键决策点）

提交级：7 文件，2109 插入 / 4 删除。五个新文件行数：Unified3Theorem 233、BottTower 196、BranchCounting 203、CoherenceToBranching 253、DHStructuralAnalysis 485。

文件级：`HigherSpecCategory.lean` 81 插入 / 4 删除（85 行改动），108 → 185 行。关键字计数：SpecTwoMorphism 22、SpecThreeMorphism 9、SpecFourMorphism 0、链复形 1、coherence 2、sorry 1。

要点：SpecFourMorphism 为 0 —— 该提交内不存在四层态射的任何 Lean 结构。

### 3.5 `463df34`（d_H 偏差结构）

该文件 174 行，10 插入 / 21 删除（净 −11），SpecFourMorphism 仍为 0。清单「+31 行」实为 31 行被改动（10+/21−），插入数 10。

### 3.6 `fb0f259`（Spec→Sp）

`HigherSpecCategory.lean` 174 行全部删除；`HigherSpCategory.lean` 299 行全部新增。与清单一致。

### 3.7 后四个提交

`5d4bdc2`、`a3df3c5`、`9cbffe1`、`2135296` 均存在，作用与清单描述同向；本台账未逐行核对其新增定理内容（见 §11）。

## 4. `27cdf8d` 原文摘录

### 4.1 三层态射注释（`HigherSpecCategory.lean` L129–137，逐字）

```lean
/-! =========================================================
    3-态射（SpecThreeMorphism）
   =========================================================

   模式：𝐒𝐩 高阶范畴具有链复形结构，每层的"缺陷"由同一个交换子 [A, ·] 给出：
     层 1（1-态射）：SpHom P  满足   P·A_Y = A_X·P
     层 2（2-态射）：α: P⇒Q  满足   Q.P - P.P = A_X·α.homotopy - α.homotopy·A_Y
     层 3（3-态射）：Σ: α⇛β  满足   β.homotopy - α.homotopy = A_X·Σ.二阶同伦 - Σ.二阶同伦·A_Y
-/
```

（`Σ.二阶同伦` 为当时字段的显示名；现行文件已更名为 `thirdHomotopy`。）

### 4.2 同一提交的交换律 docstring（L96–127）

```
/-- Exchange law for Spec₂ 2-morphisms.

    This is NOT provable as a strict equality in the current spectral
    framework because SpecTwoMorphism.homotopy does NOT satisfy the
    intertwining condition (homotopy·Y.A = X.A·homotopy). ...
    This is an intrinsic property of the spectral model: the Sp 2-category
    is weak (bicategory), not strict.  In the strict 4-category limit
    (where homotopies degenerate), the exchange law would hold strictly,
    but in the full spectral model it requires a 3-morphism coherence that
    itself depends on additional spectral conditions.

    **Impact on branching count**: the exchange law's strictness is not
    required for the layer-counting argument B = N_active × N_total = 15.
    Layer counting depends only on the number of distinct morphism layers,
    not on the exchange law.
-/
theorem specExchangeLaw ... := sorry
```

### 4.3 同提交内「不可能有第 4 个主动生成层」的表述

`Unified3Theorem.lean` L151–158：

```
§5 𝐒𝐩 态射层链复形结构（统一 3 定理的核心论据）

𝐒𝐩 高阶范畴的链复形结构：每层的"缺陷"由同一个交换子 [A, ·] 给出。
这意味着所有 3 个主动生成层共享相同的代数结构，
且不可能有第 4 个主动生成层（coherence 层不是主动生成元）。
```

`BottTower.lean` L149–152：

```
此证明将 Bott 截断指数从"数值巧合"升级为"范畴结构推论"。
翻倍次数由主动生成层数决定——若有第 4 个主动生成层，
则应有 k_max ≥ 2⁴ = 16，但 4-态射是 coherence 层，
不产生翻倍。
```

## 5. 引文与原文的差异

| 清单引文 | `27cdf8d` 原文 | 性质 |
|---|---|---|
| `Σ.secondHomotopy` | `Σ.二阶同伦` | 字段显示名不同（后期英文化） |
| `Q·P - P·P` | `Q.P - P.P` | 投影语法写作点乘 |
| N_active = 3（主动生成层数，即非平凡态射层数） | L43「层 4：4-态射（coherence）—— 不生成物理自由度」+ L45「主动生成层 = 层 1, 2, 3（排除对象层和 coherence 层）」+ L48 docstring | 语义对应，无该逐字句 |
| log₂ k_max = N_active = 3 | BottTower L25「因此 log₂(k_max) = N_active = 3」 | 括号形式不同 |
| B = 3 × 5 = 15（层计数：N_active × N_total） | BranchCounting L9「有效分支数 B = N_active × N_total = 15」+ L88「= 3 × 5 = 15」 | 语义对应，分置两处 |

结论：引文在语义上逐条有据，但不是逐字节原文；引用时应标为「据原意转写」。

## 6. 层 4 的实际来历

- `27cdf8d`：层 4 只以文字出现（Unified3Theorem L43/L45/L157、BottTower L151、BranchCounting L38，以及 paper17_zero_parameter_predictions.md L59「4-态射为 Coherence 同构」、notes/08_first_principles/... L470「5 为 Sp 的总层数」）。此时 `SpecFourMorphism` 在 Lean 中不存在（全树 grep 的 `.lean` 结构命中为 0）。
- `ffc2b56`（2026-08-13，17 天后）：`SpFourMorphism` 与 `thirdHomotopy` 首次出现在 Lean 代码中。
- 现行 `HigherSpCategory.lean`：`SpFourMorphism` 带自由参数 `thirdHomotopy` 与同形交换子条件；`SpFiveMorphism` 全库无。

因此「层 4 = coherence 层」在 2026-07-27 是一句为排除第 4 个翻倍步、保住 k_max=8 而给出的断言（BottTower L150–152 的论证结构正是「若加一层则 k_max ≥ 16，但它是 coherence，故不加」），不是从链复形导出的结论；到 2026-08-13 它才成为可操作但同形的 Lean 层。

## 7. `N_active = 3` 的定义性来源

`27cdf8d` 的 `Unified3Theorem.lean` L49–66：

```lean
inductive ActiveMorphismLayer : Type
  | first    : ActiveMorphismLayer   -- 层 1
  | second   : ActiveMorphismLayer   -- 层 2
  | third    : ActiveMorphismLayer   -- 层 3

def numActiveLayers : ℕ := 3

theorem card_active_layers : Fintype.card ActiveMorphismLayer = 3 := by simp
```

该类型恰有 3 个构造子，card = 3 由 simp 直接闭合，numActiveLayers := 3 为字面量。所以 3 是类型定义的结果，不是任何代数结构的推论；k_max := spinorDim 0（BottTower L117，值 8）与 N_total := 5（BranchCounting L54，字面量）同理。

## 8. 与机检结果的对接

- `d_A(H) = A_X·H − H·A_Y` 在 `27cdf8d` 的 `Unified3Theorem` L160–163 被写作「统一"微分" d_A」，引号本身即表明当时未主张其为数学微分。
- 该式的链复形前提 d_A ∘ d_A = 0 已被机检否证：`SpChainComplexAudit.lean` 的 `dJ_dJ_E21_ne_zero` 给出 d_A²(E₂₁) = −2J ≠ 0；数值侧 d² = 0 仅在 A_X = A_Y = c·1 时成立，而该情形 d_A ≡ 0、无非平凡 2-态射。
- 层塔在第 3 阶后塌缩的候选（H³ = 0）亦已被 `SpLayerNonCollapse.lean` 否证。

两条路线均不成立，故层数只能来自「定义停止」。

## 9. 对六条核心发现的判定

| 清单结论 | 判定 | 依据 |
|---|---|---|
| 三层态射是从链复形结构推出的 | 不成立 | 仅有以「模式：」自陈的一段注释；文件内无链复形算子、无 d∘d=0、无层 4 截断证明；且 d²≠0 已机检否证 |
| 不是从数值反推的 | 不成立 | 同一提交的 docstring 把 B = N_active × N_total = 15 直接称为 the layer-counting argument，并自陈层计数只依赖「写下了几层」；同提交 L45 用「层 4 是 coherence」排除第 4 层以保住 k_max = 8 |
| SpecThreeMorphism 定义先于 N_active=3 术语 | 无证据 | 同一 commit 内的先后不构成时序证据；N_active 由 3 构造子的 inductive 直接给出，card = 3 为 simp |
| coherence 层 = 层 4 的来源 | 部分成立、归因需改写 | 文字断言确实始于 27cdf8d；但它不是链复形的推论，且 Lean 结构直到 ffc2b56（2026-08-13）才出现 |
| 2026-07-17 版本只有 2-范畴 | 成立 | 106 行，SpecThreeMorphism 0 |
| 2026-07-21 版本仍只有 2-范畴 | 成立 | 108 行，SpecThreeMorphism 0 |

汇总：清单的事实层（提交、日期、行数、文件、层类型首现时点）基本可靠；归因层（「链复形必然性」「结构先行、数值后继」）不成立。

## 10. 复现命令

```powershell
$r="E:\workspace\hyper-resolution"; $g="D:\apps\Git\cmd\git.exe"
$p="universal_fixed_point_framework/formal_proof/UFPFormalization/UFPFormalization/HigherSpecCategory.lean"

& $g -C $r show -s --format='%h|%ai|%s' 27cdf8d
& $g -C $r diff --stat 80f2d92 27cdf8d -- $p
& $g -C $r show "27cdf8d:$p"
& $g -C $r grep -n -e 'FourMorphism' -e '4-态射' 27cdf8d
& $g -C $r log --all --format='%h|%ai|%s' -S'SpFourMorphism' -- '*.lean'
```

## 11. 未核项与边界

- `5d4bdc2`、`a3df3c5`、`9cbffe1`、`2135296` 只核对了存在性与提交消息，未逐行核对其新增定理的实质内容。
- 本台账不判断「链复形」作为一种读法是否仍有价值，只判断它能否承担层数结论——结论是不能。
- `N_total` 存在两套并行口径：`27cdf8d` 的 `BranchCounting` 用 `N_total := 5`（B = 3×5），论文 §4.2 用 `N_total = 4`（2⁴−1 = 15）。两者都得 15，权威性未裁决，此处如实并列。
