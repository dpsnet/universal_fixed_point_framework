# Lean-论文登记册与去重判定（Lean–Paper Registry & Dedup Ruling）

**用途**：以论文为权威来源，登记 UFPFormalization 每个 Lean 文件/核心符号的**论文出处、参数语义、推导角色**（结论 vs 前提 vs 常数 vs 唯象拟合）。据此判定哪些可合并、哪些必须保留。
**原则（2026-08-13 用户裁定）**：数值/字面相同的符号**不等于重复**——须以论文来源与推导角色为准；先登记造册，再依据登记判定合并。

## 登记表（按论文组织，分阶段补齐）

### 判定准则
| 情形 | 判定 |
|:-----|:-----|
| 同一论文、同一符号、同一推导角色、纯复制 | ✅ 可合并（保留母定义，子处 import 引用） |
| 数值相同但论文来源/推导角色不同（结论 vs 前提/常数） | ❌ 不可合并（保留各自定义 + 交叉注释） |
| 注释明确"有意副本"（如解除依赖耦合） | ❌ 不可合并（保留 + 交叉注释） |
| 不同标量域/不同函子实例（概念同族） | ❌ 不可合并（保留 + 注释标注同族） |

### 论文索引（已确认部分，待扩展）
| 论文 | 主题 | 对应 Lean 文件（初列） |
|:-----|:-----|:----------------------|
| Paper I (paper1_fractal_spectral_derecursion) | Rec/Sp 范畴、D 函子、谱静默、Clifford 纤维丛 | RecCategory, SpCategory, DecursionFunctor, Adjunction, Silence, SilenceHierarchy, Braided, Clifford, 等 |
| Paper XXXI (paper31_mass_delta_directionality) | J1-J3 质量-Δ 方向性、层 1-3 正交于 Δ、层 4 coherence | HigherSpCategory, DeviationBound（§1.6/§1.7/§1.8）, CoherenceToBranching |
| Paper XXXIII / d_H=ln15 推导 | 分支组合原理、统一 3 定理 | DHStructuralAnalysis, BranchCounting, BottTower, Unified3Theorem |
| Paper 33/XXVII（味/代） | GenSpace=ℂ³ 代空间 | FlavorFiber, Unified3Theorem（§3 主动生成层→GenSpace） |

## 去重候选重审（2026-08-13 恢复后，依据登记判定）

| # | 候选 | 论文来源核查 | 判定 | 依据 |
|:--|:-----|:------------|:----:|:-----|
| ① | `LayerIndex`：BranchCounting（5 层 obj+1-4）vs CategoryGeometryDictionary（4 层 1-4） | ⏳ 待 paper1 §3.5/paper31 J3 §4.1 重读确认两处层结构的论文出处与角色 | ⏳ 待判定 | 两处均描述 Sp 4-范畴层结构；需确认论文中是否为同一登记（合并）还是不同角色（保留） |
| ② | e/ln15/N_total/r/d_H_fit/delta_fit：BranchCounting vs DHStructuralAnalysis | ✅ 已确认：BranchCounting 侧 = 自底向上推导结论（N_total 关联 `total_layers_count`（LayerIndex 计数机器证明）、r = 定理 R1 谱静默因子）；DHStructuralAnalysis 侧 = 自顶向下推导前提（N_active/N_total/r 为 d_H=ln15 推导输入、ln15/e 为纯常数） | ❌ 不合并（已恢复） | 来源角色不同（结论 vs 前提） |
| ③ | `GenSpace`：FlavorFiber vs Unified3Theorem | ✅ 已确认：Unified3Theorem 注释"为解除对损坏依赖链的耦合，此处本地定义（同一类型）" | ❌ 不合并（有意副本） | 有意设计，保留 |
| ④ | `k_max`/`k_max_value`：Unified3Theorem vs BottTower | ⏳ 待重读：Unified3Theorem.k_max=8（数值）；BottTower.k_max=spinorDim 0（Bott 塔结构定义）——需确认论文中 k_max=8 的来源登记（模型选择 vs 统一 3 定理，参见勘误"k_max=8 不再声称来自 Cl(1,7) Bott 分类"） | ⏳ 待判定 | 定义路径不同（数值 vs spinorDim 结构）；且涉及 k_max=8 勘误语义，须以论文为准 |
| ⑤ | `frobeniusNorm`：RAP4（ℝ 桥接）vs Silence（ℂ 自建） | ⏳ 待登记 | ⏳ 待判定 | 标量域不同；语义同族 |
| ⑥ | `adjUnit`/`adjCounit`：Adjunction vs RAP5a | ⏳ 待登记 | ⏳ 待判定 | 不同函子（DFunctor vs DIm） |
| ⑦ | 静默度：S_D / silenceDegree / deltaSilence | ⏳ 待 paper1 §5.7.9 + 各文件注释登记 | ⏳ 待判定 | 同族公式、不同语义 |
| ⑧ | SilenceLevel / SilenceLayer / LayerIndex 近名 | ⏳ 待登记 | ⏳ 待判定 | 近名不同义，登记对照 |
| ⑨ | spectralSilence vs spectralSilenceSimple | ⏳ 待登记 | ⏳ 待判定 | 功能子集简化变体 |

## 防复发清单（新建/修改 Lean 文件前必查）

1. **查登记册**：本文件登记表确认符号/概念是否已有论文登记；
2. **grep 符号名**：`Grep pattern="^def|^theorem|^structure|^inductive|^abbrev|^class" path=UFPFormalization` 确认不重复；
3. **核查论文来源**：数值/字面相同 ≠ 重复——须确认论文出处与推导角色（结论/前提/常数/唯象），禁止凭代码表面特征判定；
4. **import 而非重定义**：确认为纯复制时 `import UFPFormalization.<母文件>` + 限定名引用；
5. **合并后验证**：`lake build` 必须保持 2454 jobs 零警告零 sorry；
6. **跨上下文同步**：论文/笔记/路线图/RAP 引用被删符号处同步更新。
