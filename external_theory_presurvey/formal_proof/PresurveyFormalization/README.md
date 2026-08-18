# PresurveyFormalization — 外部理论预研形式化

**定位**：`external_theory_presurvey/`（外部理论预研）阶段的形式化根目录。当前内容为预研笔记
`external_theory_lineage_presurvey.md` §7.15（"恰 1 个零权重分支"公理化证明）的 Lean 4 机器形式化
及其候选前提 A3/A5 的严格化。基于 **Lean 4.31.0 + mathlib4**。

## 项目结构

```
PresurveyFormalization/
├── lakefile.lean                 # Lake 配置：绝对路径复用主框架共享 mathlib
├── lean-toolchain                # leanprover/lean4:v4.31.0
├── PresurveyFormalization.lean   # 库入口
├── Main.lean                     # 可执行入口
└── PresurveyFormalization/
    ├── SpinorSilenceBranch.lean  # §7.15 全部形式化（§①–§⑥）
    └── TimeBranch.lean           # §7.34 时间分支双指标刻画（w=0 ∧ c₃=1 ∧ t）
```

## 环境复用（不改动主框架）

本项目的 `.elan`（工具链）与 `.lake`（mathlib 及 8 个传递依赖）**复用**主框架
`universal_fixed_point_framework/formal_proof/UFPFormalization/` 的既有环境：

- `.elan`：使用用户级 elan（`C:\Users\qinxi\.elan`，Lean 4.31.0 + Lake 5.0.0）——本地
  `.elan` 的 toolchain junction 不可用，故直接用用户级工具链；
- `.lake`：[lakefile.lean](lakefile.lean) 以**绝对路径**引用共享
  `.lake/packages/{mathlib,batteries,aesop,Qq,proofwidgets,plausible,Cli,importGraph,LeanSearchClient}`，
  零拷贝、离线可用、**不改动主框架任何源码**。

## 构建

在 PowerShell 中（首次 `lake build` 会因 manifest 初始化触发 mathlib post-update cache 钩子，
离线时 `cache get` 失败属正常；mathlib 已预编译，**重新运行一次 `lake build` 即跳过钩子并正常构建**）：

```powershell
$env:PATH = "C:\Users\qinxi\.elan\bin;$env:PATH"
cd d:\trae-work\hyper-resolution\external_theory_presurvey\formal_proof\PresurveyFormalization
lake build
```

当前状态：**3834 jobs 全量通过，零 `sorry` 零 `axiom` 零警告**。

## 定理清单（SpinorSilenceBranch.lean）

对应预研笔记 §7.15 证明步骤与严格化：

| 节 | 定理 | 内容 |
|----|------|------|
| 结构 | `S4` / `Branch := Fin 16` / `Silent` / `Observable` | A4 阈值 S₄ = 1/15、16 分支、A1/A4 谓词 |
| §① | `observableWindow_forces_k_le_15` | 均匀权重 1/k ≥ S₄ ⟹ k ≤ 15 ⟹ 静默数 m ≥ 1 |
| §① | `silent_count_ge_one` | m = 16 − k ≥ 1 |
| §② | `uniformShannonEntropy_eq_log` | 均匀分布熵 H = ln k |
| §② | `uniformEntropy_le_log_15` / `uniformEntropy_lt_log_15` | H ≤ ln15、严格递增 |
| §③ | `maxEntropy_forces_k_eq_15` | 熵达上界 ln15 ⟹ k = 15 |
| 主定理 | `exactly_one_silent_branch` | **m = 1 ∧ k = 15（恰 1 零权重分支）** |
| 主定理 | `normalization_uniform_consistent` | A2：k·(1/k) = 1 |
| §④ | `corollary_observable_count` | B = 15 观测窗口计数 |
| §④ | `corollary_weight_at_threshold` | w = 1/15 = S₄ 恰在阈值 |
| §④ | `corollary_entropy_eq_dH` | ln15 = −ln S₄ = d_H |
| §⑤ A5 严格化 | `entropy_le_log_card` | KL 上界：H(p) ≤ ln k |
| §⑤ A5 严格化 | `entropy_eq_log_card_iff_uniform` | 等号 ⟺ 均匀 pᵢ = 1/k（唯一性） |
| §⑤ A5 严格化 | `max_entropy_forces_uniform` | "最大熵 ⟹ 均匀"成为定理 |
| §⑥ A3 严格化 | `branch_eigenvector` | A_E e_i = λ_i e_i（特征方程） |
| §⑥ A3 严格化 | `branch_eigenspace_eq_span` | 分支 = 1 维特征子空间 span{e_i} |
| §⑥ A3 严格化 | `stdBasis_decomposition` | 基展开完备 v = Σ v_i e_i |
| §⑥ A3 严格化 | `branch_operator_symmetric` | A_E 自伴 |
| §⑥ A3 严格化 | `silence_weights_are_probability` | 1 零权重 + 15×1/15 合法概率分布 |
| §⑥ A3 严格化 | `A3_spinor_branch_decomposition` | 打包 A3 谱分解四性质 |

## 定理清单（TimeBranch.lean）

对应预研笔记 §7.34（时间分支双指标刻画：w = 0（谱静默）∧ c₃ = 1（演化非静默）∧ t（演化参数））：

| 节 | 定理 | 内容 |
|----|------|------|
| 指标①② | `TimeSilent` | 时间分支谱权重为零（= Silent，谱静默） |
| 指标② | `silenceWeight` / `TimeNeverSilent` | 静默权重 c_t = 1（paper33 c₃ 全保留，永不静默） |
| 双指标 | `dual_indicators_consistent` | **双指标一致配置存在**：w 合法概率分布 ∧ w_t=0 ∧ c_t=1（§7.32"静默双义"机器表述） |
| 唯一性 | `time_branch_uniqueness` | 时间分支 = §7.15 恰 1 个零权重分支（A3/A4/A5 下 m=1 ∧ k=15） |
| 指标③ | `TimeEvolution` | 演化参数 t 的单向演化骨架（A4 代数核心，独立重构） |
| 指标③ | `TimeEvolution.directional` | **方向性**：t₁<t*<t₂ ⟹ 静默单向 1→0（bifurcation_directional 同构） |
| 综合 | `time_branch_carries_evolution` | 时间分支（谱权重 0）同时承载单向演化（三指标叠加） |

## 候选前提状态与诚实边界

- **A5（最大熵 ⟹ 均匀）**：从候选前提**升级为已证定理**（v0.27，§⑤）——KL/熵上界引理机器证明（证实，非否定）；
- **A3（旋量 16 分支谱分解）**：谱分解结构从候选前提**升级为已证定理**（v0.28，§⑥）——有限维谱定理（对角实现）；
  **剩余显式前提** = `DistinctBranchSpectrum`（分支谱互异性，即 A3 原义"存在具 16 分支谱的 A_E"的
  精确定义）；旋量 16 维（Cl(1,7) ≅ M₁₆(ℝ)）锚点引用主框架 `BottTower`/`Unified3Theorem`（不重证）；
- 谱测度 μ_E 仅通过分支权重 w_i 进入（A1/A2），未引入完整测度论 / 谱测度 Lebesgue 分解。

## 与主框架关系

零改动主框架 `formal_proof`；仅环境复用 + 锚点引用；符合预研"先内后外"保护原则。

## 版本记录

- **v0.26**（2026-08-17）：§7.15 形式化（环境复用搭建 + 证明步骤 ①–④ + 主定理）；
- **v0.27**（2026-08-17）：A5 严格化（§⑤ KL/熵上界引理）；
- **v0.28**（2026-08-17）：A3 严格化（§⑥ 有限维谱定理，对角实现）；
- **v0.29**（2026-08-17）：TimeBranch 形式化（§7.34 时间分支双指标刻画：`dual_indicators_consistent` / `TimeEvolution.directional` 等，3828 jobs 零错误）；
- **v0.30**（2026-08-17）：LuInvariant 部分形式化（§7.35 LU 引理 1 矩阵代数核心：`partialTrace`/`kron`/`ortho_inner`/δ 吸收三引理，3830 jobs；主定理求和重排开放）；
- **v0.31**（2026-08-17）：LayerEntropy 形式化（§7.53 熵分解恒等式：`layerProb`/`layerProb_sum_eq_one`/`entropy_decomposition_eq_log_15`——总熵 ln 15 = 层分布熵 + 层内熵加权，3832 jobs 零错误零警告）；
- **v0.32**（2026-08-17）：RUniqueness 形式化（§7.56 R 重构唯一性代数核心：`diagonal_injective`（Matrix.diagonal 单射——谱像 ⟹ 对角算子唯一）、`spectrum_determines_operator`（同一算子两对角实现 ⟹ 相同特征值向量，R 重构唯一性）、`spectral_operator_unique`（谱像 ⟹ 算子存在唯一），3834 jobs 零错误零警告）。
- **v0.33**（2026-08-17）：**LuInvariant 完整机证（§7.62 机证闭合）**——`partialTrace_conj_kron`（部分迹变换律 Tr_B[(U⊗V)ρ(U⊗V)ᵀ] = U(Tr_B ρ)Uᵀ）**完整机器证明成功**：新增 `sum_reorder_b_inner`（三重求和 b 移入最内层，显式 `conv_lhs` 限定 `Finset.sum_comm`）+ 主定理约 90 行证明脚本（kron 展开 ⟹ 求和重排 ⟹ V 正交吸收 ⟹ δ 吸收 ⟹ partialTrace 识别 ⟹ RHS 展开匹配）；§7.61 开放项闭合，3834 jobs 零错误零警告；组件 b（谱熵幺正不变）仍开放（诚实标注）。
- **v0.34**（2026-08-17）：**RUniqueness 谱投影层完整形式化（§7.64 机证闭合）**——`branchProjection`（分支 i 谱投影 E_ii）+ `spectral_projection_unique`（像条件 ∧ 零化条件 ⟹ P = E_ii——**特征子空间直和 ⟹ 谱投影唯一**）+ `spectral_projection_exists_unique`（存在且唯一）；§7.56"特征子空间直和 ⟹ 投影唯一"开放项闭合，R 唯一性三层机证齐备（算子/投影/分支结构），3834 jobs 零错误零警告。
- **v0.35**（2026-08-17）：**TimeSpectrum 形式化（§7.69 t*_i 分布代数核心机器化）**——新文件 `TimeSpectrum.lean`，lake build **3836 jobs 零错误零警告**：`layerWeight`/`S4`/`dH`/`tstar` 核心定义 + `tstar_eq_log`（**t*_k = ln(S_k/S₄) 权重比形式机证**：`Real.log_mul` + `Real.log_exp` + `ring`）+ `tstar_window_endpoint`（**t*_1 = ln(15/e)** 观测窗口终点：`Real.log_div` + `Real.log_exp`）+ `tstar_ordering`（**t*_1 > t*_2 > t*_3** 层序严格降序：`linarith`）；§7.68"非对角分量未分析"闭合（非对角-对角完全解耦，权重比仅依赖对角初始值与静态谱值——t*_i 对非对角扰动鲁棒）。
