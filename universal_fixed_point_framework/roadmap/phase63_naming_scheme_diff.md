# Phase 63 命名方案修订对比表与数学边界条件

**文档编号**: UFPF-RM-P63-DIFF-001
**日期**: 2026-08-23
**框架**: Universal Fixed Point Framework (UFPF)
**关联文档**: Phase 63/63b 全部文档
**状态**: 研究记录（命名方案尚未充分验证，已从 paper 目录移除）

---

## 缩写回顾

| 缩写 | 全称 |
|------|------|
| UFPF | Universal Fixed Point Framework（全域不动点框架，总称） |
| 狭义 UFPF | Original UFPF（UFPF₀）：有界算子 + H1-H5 假设下的四体制基础框架 |
| 广义 UFPF | Generalized UFPF（G-UFPF）：包含平展统一猜想、体制间态、Gödel-Koopman 算子等全部扩展的猜想体系 |
| H1-H5 | 五条充分假设（Sufficient Hypotheses 1-5），狭义 UFPF 的工作前提 |
| Rec | Recursive Category（递归范畴） |
| Sp | Spectral Category（谱范畴） |
| D | Decursion Functor（去递归函子） |

---

## §1 修订对比表（Diff）：命名方案引入的全部变更

以下表格逐文件列出 2026-08-23 引入狭义 UFPF / 广义 UFPF 命名方案时的全部修改点。

### 1.1 主框架文档（3 个文件）

#### 文件 1：`paper/paper1_fractal_spectral_derecursion.md`（Paper I, v2.56）

| 变更位置 | 变更类型 | 旧内容（节选） | 新内容（节选） |
|---------|---------|--------------|--------------|
| 术语说明（第 11 行后） | **新增区块** | 无命名方案 | 新增"命名方案"引用块，定义狭义 UFPF（UFPF₀）与广义 UFPF（G-UFPF），给出包含关系 $\subset$、约化条件、猜想 3.5 独立性说明 |

**具体变更**：
- 新增内容：在术语说明段落后插入引用块 `> **命名方案**（v2.56 引入）`
- 关键定义：
  - 狭义 UFPF = 有界算子 + H1-H5 + 四体制元定理（A/B1/B2/C），Paper I-XVI 主体，非猜想
  - 广义 UFPF = N-平展统一猜想 + 体制间态 + 算子代数推广 + Gödel-Koopman 算子，猜想体系
  - 约化条件：算子有界 + H1-H5 全成立 + 存在尖锐 $C_{\mathrm{crit}}$ → G-UFPF 约化为 UFPF₀

#### 文件 2：`paper/UFPF体系总序.md`

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 版本对齐后（第 5 行后） | **新增引用块** | 仅版本对齐声明 | 在版本对齐声明后新增"命名方案"引用块，定义两个层次并给出行文规则：已证定理→狭义 UFPF；猜想扩展→广义 UFPF |

#### 文件 3：`README.md`

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 重要声明后（第 3 行后） | **新增引用块** | 仅⚠️重要声明 + 项目状态 | 在重要声明后新增"命名方案"引用块，给出完整定义和包含关系 |

### 1.2 Phase 63b 路线图文档（4 个文件）

#### 文件 4：`roadmap/phase63b_flattening_unification.md`（v0.3）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 缩写回顾表 | **新增 3 行** | `\| UFPF \| 全域不动点框架 \|`（1 行） | UFPF 行改注"总称"；新增狭义 UFPF 行、广义 UFPF 行 |
| 缩写回顾表后 | **新增命名说明** | 无 | 新增命名说明引用块：平展统一猜想、体制间态、Gödel-Koopman 算子均属广义 UFPF |
| §1.1 背景（第 35 行） | **正文标注** | "UFPF 框架识别出五类'盲区'" | "**狭义 UFPF**（UFPF₀，即有界算子 + H1-H5 假设下的四体制框架）识别出五类'盲区'" |
| §5 D4 推论 3.4（第 226 行） | **正文标注** | "则 $T$ 被 UFPF 覆盖" | "则 $T$ 被**广义 UFPF** 覆盖" |
| §5 D5 猜想 3.5（第 234 行后） | **新增归属说明** | 直接陈述猜想 | 新增归属说明引用块：猜想 3.5 属广义 UFPF 内部额外更强独立猜想 |
| §5 D5 猜想 3.5 论证 | **正文标注** | "$T^*$ 自洽 $\Rightarrow$ UFPF 覆盖" | "$T^*$ 自洽 $\Rightarrow$ **广义 UFPF** 覆盖" |
| 版本历史 | **新增条目** | v0.2（最后一行） | 新增 v0.3 条目 |

#### 文件 5：`roadmap/phase63b_experimental_verification_plan.md`（v0.2）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 缩写回顾表 | **新增 3 行** | UFPF（1 行） | UFPF 改注"总称"；新增狭义 UFPF、广义 UFPF 行 |
| 缩写回顾表后 | **新增命名说明** | 无 | 新增命名说明：模块 2-4 属广义 UFPF 验证；模块 1 四体制 Q 指标属狭义 UFPF 验证 |
| 版本历史 | **新增条目** | v0.1（最后一行） | 新增 v0.2 条目 |

#### 文件 6：`roadmap/phase63b_module2_model_parameters.md`（v0.2）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 缩写回顾表 | **新增 2 行** | UFPF（1 行） | UFPF 改注"总称"；新增狭义 UFPF、广义 UFPF 行 |
| 版本历史后 | **新增命名说明** | 无 | 新增命名说明：平展统一验证属广义 UFPF；四体制分类属狭义 UFPF |
| 版本历史 | **新增条目** | v0.1（最后一行） | 新增 v0.2 条目 |

#### 文件 7：`roadmap/phase63_meta_theorem_open_problems.md`（v0.2）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 修订历史 | **新增条目** | v0.1（最后一行） | 新增 v0.2 条目 |
| 修订历史后 | **新增命名说明** | 无 | 新增命名说明：四体制元定理 + 五盲区属狭义 UFPF；三层推广框架属广义 UFPF；行文规则说明 |

### 1.3 研究笔记文档（5 个文件）

#### 文件 8：`research_notes/flattening_unification_conjecture_2026-08-23.md`（v0.2）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 缩写回顾表 | **新增 2 行** | UFPF（1 行） | UFPF 改注"总称"；新增狭义 UFPF、广义 UFPF 行 |
| §1.1 问题起源（第 30 行） | **正文标注** | "在 UFPF 框架的元定理完备性讨论中" | "在 UFPF 框架（具体为**狭义 UFPF**，即有界算子 + H1-H5 假设下的四体制框架）的元定理完备性讨论中" |
| 文件末尾 | **新建版本历史 + 命名说明** | 仅脚注行 | 新建版本历史节（v0.1 + v0.2）+ 命名说明：平展统一猜想、推论 3.4、猜想 3.5 均属广义 UFPF；猜想 3.5 独立性说明 |

#### 文件 9：`research_notes/godel_operator_spectral_silence_2026-08-23.md`（v0.2）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 缩写回顾表 | **新增 2 行** | UFPF（1 行） | UFPF 改注"总称"；新增狭义 UFPF、广义 UFPF 行 |
| 文件末尾 | **新建版本历史 + 命名说明** | 仅脚注行 | 新建版本历史节（v0.1 + v0.2）+ 命名说明：Gödel-Koopman 算子属广义 UFPF；谱静默判据基础定义属狭义 UFPF |

#### 文件 10：`research_notes/blind_spot_physical_system_mapping_2026-08-23.md`（v0.2）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 修订历史 | **新增条目** | v0.1（最后一行） | 新增 v0.2 条目 |
| 修订历史后 | **新增命名说明** | 无 | 新增命名说明：四体制 + 五盲区属狭义 UFPF；盲区解决方案属广义 UFPF |

#### 文件 11：`research_notes/inter_regime_state_definition_2026-08-23.md`（v0.2）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 修订历史 | **新增条目** | v0.1（最后一行） | 新增 v0.2 条目 |
| 修订历史后 | **新增命名说明** | 无 | 新增命名说明：体制间态 $\mathcal{R}_{\mathrm{inter}}$ + Drinfeld 联结子形变属广义 UFPF；四体制 + H1-H5 属狭义 UFPF |

#### 文件 12：`research_notes/meta_theorem_completeness_discussion_2026-08-23.md`（v0.2）

| 变更位置 | 变更类型 | 旧内容 | 新内容 |
|---------|---------|-------|-------|
| 文件末尾 | **新建修订历史 + 命名说明** | 无版本历史/命名说明 | 新建修订历史节（v0.1 + v0.2）+ 命名说明：四体制 + H1-H5 + 五盲区属狭义 UFPF；一般形式推广属广义 UFPF |

### 1.4 变更统计汇总

| 变更类型 | 涉及文件数 | 变更次数 |
|---------|----------|---------|
| 缩写回顾表新增条目 | 6 | 14 行新增 |
| 命名说明新增 | 12 | 12 处 |
| 版本历史新增条目 | 10 | 10 条 |
| 正文术语标注（狭义/广义） | 2 | 4 处 |
| 归属说明新增（猜想 3.5） | 1 | 1 处 |
| 术语说明新增命名方案区块 | 1 | 1 处 |
| 引用块新增（主框架文档） | 2 | 2 处 |
| **合计** | **12 个文件** | **44 处变更** |

---

## §2 狭义 UFPF / 广义 UFPF 严格数学边界条件对比表

以下表格可直接插入 Phase 63 术语表章节。每行给出一个边界条件的严格数学表述。

### 2.1 算子代数层边界

| 边界条件 | 狭义 UFPF（UFPF₀） | 广义 UFPF（G-UFPF） | 数学形式化 | 状态 |
|---------|-------------------|-------------------|-----------|------|
| **算子类型** | 有界线性算子 $T: \mathcal{H} \to \mathcal{H}$，$\|T\| < \infty$ | 有界 + 无界算子；无界算子需指定稠密定义域 $\mathrm{Dom}(T) \subseteq \mathcal{H}$ | 狭义：$T \in \mathcal{B}(\mathcal{H})$；广义：$T: \mathrm{Dom}(T) \to \mathcal{H}$，$\mathrm{Dom}(T)$ 稠密 | 狭义已证；广义待证 |
| **谱分解假设（H2）** | 谱分解存在：$T = \int \lambda \, dE(\lambda)$（谱测度 $E$ 存在） | 允许谱分解失败（盲区 1/T1b）：$\mathrm{spectralDecomposable}(S) = \mathrm{False}$ | 狭义：$\exists E: \sigma(T) \to \mathrm{Proj}(\mathcal{H})$；广义：$E$ 可不存在 | 狭义有限维自动成立；广义 Lean 反例已证 |
| **自伴/耗散分解（H3）** | 算子可分解为 $A = A_{\mathrm{sa}} + A_{\mathrm{anti}}$，其中 $A_{\mathrm{sa}} = A_{\mathrm{sa}}^*$ | 推广至 von Neumann 代数层面：$A \in \mathcal{M}$（vN 代数），Tomita-Takesaki 分解 | 狭义：$A_{\mathrm{sa}} = \frac{A+A^*}{2}$, $A_{\mathrm{anti}} = \frac{A-A^*}{2}$；广义：$\mathcal{M}$ 上的 modular automorphism 群 | 狭义已证；广义概念框架建立 |
| **万有核条件（H4）** | $K_S$ 是万有核（点分离 RKHS）：$\forall x \neq y, \exists k: k(x) \neq k(y)$ | 保留 H4，但允许在弱三元组中退化 | 狭义：$\mathrm{universalKernel}(S) = \mathrm{True}$；广义：弱化至 $\mathrm{semi\text{-}universal}$ 或算子丛截面 | 狭义有限维自动成立；广义待形式化 |
| **谱对应（H5）** | $\lambda_i = e^{-\mu_i}$ 作为范畴自然同构 $M \cong_{\mathrm{br}} L$ 成立 | 保留 H5 作为局部条件；Gödel-Koopman 算子中谱对应退化为谱静默 | 狭义：$M_0 \cong L_0$（定理 3.7a）；广义：$M^{\mathrm{br}} \cong_{\mathrm{br}} L^{\mathrm{br}}$（定理 3.7b）或谱静默 | 狭义已证；广义辫子情形已证 |

### 2.2 耦合与临界层边界

| 边界条件 | 狭义 UFPF（UFPF₀） | 广义 UFPF（G-UFPF） | 数学形式化 | 状态 |
|---------|-------------------|-------------------|-----------|------|
| **耦合度 $C$** | $C = 1$（自伴体制 A）或 $C \in (1, C_{\mathrm{crit}})$（耗散体制 B1/B2） | $C$ 可任意大，包括 $C \geq C_{\mathrm{crit}}$（退化体制 C）和 $C_{\mathrm{crit}}$ 不存在的情形 | $C = \|A_{\mathrm{sa}}\| \cdot \|A_{\mathrm{anti}}\| / \|[A_{\mathrm{sa}}, A_{\mathrm{anti}}]\|$（伪谱扰动界） | 狭义已证；广义体制 C 概念定义 |
| **临界值 $C_{\mathrm{crit}}$** | 存在**尖锐** $C_{\mathrm{crit}} \in \mathbb{R}_{>0}$：$C < C_{\mathrm{crit}}$ 时辫子六边形公理成立 | 允许 $C_{\mathrm{crit}}$ 不存在（盲区 4）或为函数 $C_{\mathrm{crit}}(\theta)$（连续化） | 狭义：$\exists C_{\mathrm{crit}} \in \mathbb{R}: C \geq C_{\mathrm{crit}} \Rightarrow \text{辫子瓦解}$；广义：$C_{\mathrm{crit}}$ 可不存在或连续 | 狭义有限维验证；广义盲区 4 待验证 |
| **辫子交叉数 $k$** | $k \in \mathbb{Z}_{\geq 0}$（离散） | $k$ 可连续化：$k \in \mathbb{R}_{\geq 0}$ | 狭义：$k \in \mathbb{Z}$，辫子范畴 $\mathrm{BrCat}$；广义：$k \in \mathbb{R}$，弱辫子/Drinfeld 联结子 | 狭义 Lean 已形式化；广义 Drinfeld 联结子形变已推导 |

### 2.3 范畴与函子层边界

| 边界条件 | 狭义 UFPF（UFPF₀） | 广义 UFPF（G-UFPF） | 数学形式化 | 状态 |
|---------|-------------------|-------------------|-----------|------|
| **Rec 范畴对象** | $S = (\mathrm{carrier}, \mathrm{step}, T_S, K_S)$，满足 H1-H5 全部 | 扩展为 $\mathrm{GeneralRecObj}$：允许 $\mathrm{spectralDecomposable} = \mathrm{False}$ | 狭义：$\mathrm{RecObj}$（Lean 已定义）；广义：$\mathrm{GeneralRecObj}$（Lean 已定义） | 狭义已形式化；广义已定义 |
| **D 函子存在性** | $D: \mathrm{Rec}_D \to \mathrm{Sp}$ 存在且忠实（定理 2.3.4） | $D$ 可能不存在（盲区 1）；引入 D 存在性元公理 | 狭义：$D(S) = (\mathcal{H}_S, T_S)$；广义：$D_{\mathrm{partial}}: \mathrm{GeneralRecObj} \to \mathrm{Option}(\mathrm{SpObj})$ | 狭义已证；广义 Lean 反例已证 |
| **伴随关系 $D \dashv R$** | $D \dashv R$ 存在（定理 2.4.5） | 推广为弱伴随或算子丛层面伴随 | 狭义：$\mathrm{Hom}_{\mathrm{Sp}}(D(S), A) \cong \mathrm{Hom}_{\mathrm{Rec}}(S, R(A))$；广义：弱化态射集 | 狭义已证；广义待形式化 |
| **谱静默变换** | 谱静默判据（Definition 5.1, Paper I）：连续谱 + 零测度 + LACI→∞ + 零轨道权重 | 谱静默作为 N-平展的特例；Gödel-Koopman 算子实现不可判定性→谱静默对应 | 狭义：$D^{\mathrm{sil}}_{N}(S)$，$\rho_N = |\{i: |\lambda_i|^N < \varepsilon\}|/d$；广义：$\mathrm{Flat}_N(S) = (\mathcal{H}, T_S^N)$ | 狭义已定义；广义平展统一猜想待证 |

### 2.4 体制分类与覆盖性边界

| 边界条件 | 狭义 UFPF（UFPF₀） | 广义 UFPF（G-UFPF） | 数学形式化 | 状态 |
|---------|-------------------|-------------------|-----------|------|
| **体制分类** | 四体制离散树：A（自伴）⊂ B1（解耦耗散）⊂ B2（耦合耗散），B2 $\xrightarrow{C \geq C_{\mathrm{crit}}}$ C（退化） | 新增体制间态 $\mathcal{R}_{\mathrm{inter}}$（B2↔C 过渡带）+ 退化体制 $C^*$ | 狭义：$A \subset B_1 \subset B_2$，$B_2 \xrightarrow{C_{\mathrm{crit}}} C$；广义：$+ \mathcal{R}_{\mathrm{inter}}$, $+ C^*$ | 狭义 Lean 已形式化；广义体制间态已定义 |
| **覆盖完备性** | 存在五个盲区（H1-H5 不满足、无界算子、临界层、$C_{\mathrm{crit}}$ 缺失、时变/非线性） | 平展统一猜想（猜想 3.1）：$\forall S, \exists N^*: \mathrm{Flat}_{N^*}(S) \in \bigcup R \cup \mathrm{Silence}$ | 狭义：五盲区未覆盖；广义：$\forall S \in \mathrm{GeneralRecObj}, \exists N^* \in \mathbb{N} \cup \{\infty\}$ | 狭义盲区已识别；广义猜想数值验证 6/6 + 6/6 通过 |
| **Gödel 不可判定性** | 不处理逻辑自指 | Gödel-Koopman 算子 $T_F: \ell^2(\mathbb{N}) \to \ell^2(\mathbb{N})$，不可判定性 ⇔ 自指深度 $N_{\mathrm{self}}$ 处谱静默 | 广义：$T_F \delta_n = \delta_{f_F(n)}$，$\sigma(T_F)$ 含连续谱分量 | 狭义不适用；广义算子已构造，数值验证通过 |
| **最优理论 $T^*$** | 不涉及 | 猜想 3.5：$\exists T^*: \mathrm{Consistent} \wedge \mathrm{Complete} \wedge \mathrm{Covered} \wedge \mathrm{Rich} \wedge \mathrm{Correct}$ | 广义独立猜想；广义 UFPF 核心覆盖不依赖此猜想 | 狭义不适用；广义数值验证 $Q_{\mathrm{new}}(T^*) = 0.923$ 最高 |

### 2.5 约化关系

| 条件 | 数学表述 |
|------|---------|
| **G-UFPF → UFPF₀ 约化** | 当以下条件**全部**成立时，广义 UFPF 约化为狭义 UFPF： |
| (1) 算子有界 | $T \in \mathcal{B}(\mathcal{H})$，$\|T\| < \infty$ |
| (2) H1-H5 全成立 | $\mathrm{spectralDecomposable} \wedge \mathrm{universalKernel} \wedge \mathrm{spectralCorrespondence} \wedge \cdots = \mathrm{True}$ |
| (3) 尖锐 $C_{\mathrm{crit}}$ 存在 | $\exists C_{\mathrm{crit}} \in \mathbb{R}_{>0}: C \geq C_{\mathrm{crit}} \Rightarrow \text{辫子瓦解}$ |
| (4) $k$ 离散 | $k \in \mathbb{Z}_{\geq 0}$ |
| (5) 不含平展/体制间态/Gödel 算子 | 不使用 $\mathrm{Flat}_N$, $\mathcal{R}_{\mathrm{inter}}$, $T_F$ |
| **包含关系** | $\textbf{狭义 UFPF} \subset \textbf{广义 UFPF}$ |

---

## §3 术语对照表：狭义 vs 广义引用规则

| 语境 | 应使用术语 | 示例 |
|------|----------|------|
| 已证定理、四体制分类（A/B1/B2/C） | **狭义 UFPF**（UFPF₀） | "狭义 UFPF 的四体制元定理已在 Lean 中形式化" |
| H1-H5 假设、有界算子、谱分解 | **狭义 UFPF** | "狭义 UFPF 在有界算子与 H1-H5 假设下成立" |
| 五盲区识别（问题侧） | **狭义 UFPF** | "狭义 UFPF 识别出五类盲区" |
| N-平展、静默比 $\rho_N$、多深度谱系 | **广义 UFPF**（G-UFPF） | "广义 UFPF 的平展统一猜想给出深度-体制对应" |
| 体制间态 $\mathcal{R}_{\mathrm{inter}}$ | **广义 UFPF** | "体制间态属于广义 UFPF 猜想体系" |
| Gödel-Koopman 算子、不可判定↔谱静默 | **广义 UFPF** | "广义 UFPF 建立 Gödel-Koopman 算子对应" |
| 推论 3.4（全域覆盖） | **广义 UFPF** | "自洽理论被广义 UFPF 覆盖" |
| 猜想 3.5（最优理论 $T^*$） | **广义 UFPF 内独立猜想** | "猜想 3.5 是广义 UFPF 内部额外更强的独立猜想" |
| 算子代数推广（vN 代数、Tomita-Takesaki） | **广义 UFPF** | "广义 UFPF 通过算子代数推广处理盲区 2" |
| 标准句式 | — | "狭义 UFPF 在有界算子与 H1-H5 假设下成立；广义 UFPF 作为猜想体系，尝试解除这些前提假设，拓展框架适用边界。狭义 UFPF 是广义 UFPF 在强假设下的特例。" |

---

## §4 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1 | 2026-08-23 | 初版创建：Phase 63 命名方案修订对比表 + 数学边界条件对比表 |

---

*本文档为 UFPF 内部路线图文档。正式论文需自包含，仅引用已发表 UFPF 论文和标准学术文献。*
