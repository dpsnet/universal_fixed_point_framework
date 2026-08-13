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
| Paper I (paper1_fractal_spectral_derecursion) | Rec/Sp 范畴、D 函子、谱静默、Clifford 纤维丛；五层静默 S0-S4（§5.7） | RecCategory, SpCategory, DecursionFunctor, Adjunction, Silence, SilenceHierarchy, Braided, Clifford, 等 |
| Paper XXXI (paper31_mass_delta_directionality) | J1-J3 质量-Δ 方向性；§4.1 层结构表（层 0-4，层 1-3 正交于 Δ、层 4 coherence=Δ） | HigherSpCategory, DeviationBound（§1.6/§1.7/§1.8）, CoherenceToBranching |
| Paper XXXIII (paper33_origin_of_3) / Paper XVII (paper17_zero_parameter_predictions) | 统一 3 定理（N_gen=N_active=3 机器证明）；定理 R1（S_k=s^k 单参数族、s=e⁻¹ 物理选定特例）；d_H=ln15+δ（分支计数+Moran/Bowen 机器证明） | Unified3Theorem, DHStructuralAnalysis, BranchCounting, BottTower |
| Paper XX/XXI (paper20/21) | k_max=8 由统一 3 定理（2^N_active）机器证明 + 对偶网络（B=2k_max−1）确定 | BottTower（Bott 塔翻倍工作基准）、Unified3Theorem |
| Paper XXX (paper30_dH_structural_analysis) | 定理 1：给定 B=15 解唯一；"为何 B=15"由 Sp 严格 4-范畴结构回答（统一 3 定理） | DHStructuralAnalysis, BranchCounting |
| Paper 33/XXVII（味/代） | GenSpace=ℂ³ 代空间 | FlavorFiber, Unified3Theorem（§3 主动生成层→GenSpace） |

## 去重候选重审（2026-08-13 恢复后，依据登记判定）

| # | 候选 | 论文来源核查 | 判定 | 依据 |
|:--|:-----|:------------|:----:|:-----|
| ① | `LayerIndex`：BranchCounting（5 层 obj+1-4）vs CategoryGeometryDictionary（4 层 1-4） | paper31 §4.1 层结构表 = **5 层**（层 0 对象 + 层 1-4，层 1-3 正交于 Δ、层 4 coherence=Δ）——BranchCounting 与之完全一致；CategoryGeometryDictionary 为 4 层子集（去层 0，paper44 语境） | ✅ 已完成（用户确认合并） | 同一论文出处（paper31 J3 §4.1）；CategoryGeometryDictionary 删本地定义，import BranchCounting + open，`isCoherenceLayer` 改 `.four`；directionMap 对 obj 层一致成立 |
| ② | e/ln15/N_total/r/d_H_fit/delta_fit：BranchCounting vs DHStructuralAnalysis | **r=e⁻¹ 来源 = 定理 R1**（RAP 勘误 L74：推导值，几何级数+生成元匹配+双重最优性；paper17：味物理选定特例）；**ln15 来源 = 分支计数+Moran/Bowen 机器证明**（paper17）；BranchCounting 侧 = 自底向上推导结论（N_total 关联 total_layers_count 机器证明）；DHStructuralAnalysis 侧 = 自顶向下推导前提 | ❌ 不合并（已恢复） | 来源角色不同（推导结论 vs 推导前提/常数） |
| ③ | `GenSpace`：FlavorFiber vs Unified3Theorem | Unified3Theorem 注释"为解除对损坏依赖链的耦合，此处本地定义（同一类型）" | ❌ 不合并（有意副本） | 有意设计，保留 |
| ④ | `k_max`/`k_max_value`：Unified3Theorem vs BottTower | **k_max=8 权威来源 = 统一 3 定理（2^N_active=2³）机器证明 + 对偶网络**（paper20 L439/paper21 L734）；**BottTower.k_max = spinorDim 0** = Bott 塔翻倍"工作基准"（paper2 L219 诠释 + 2026-08-07 勘误定位，不依赖 Cl(1,7) Bott 分类）；Unified3Theorem.k_max=8 = 数值（统一 3 定理） | ❌ 不合并（已恢复） | 论文来源不同（统一 3 定理 vs Bott 塔翻倍工作基准），数值同为 8 但角色不同 |
| ⑤ | `frobeniusNorm`：RAP4（ℝ 桥接）vs Silence（ℂ 自建） | RAP4 = mathlib `‖A‖` 桥接（ℝ）；Silence = 自建 `Real.sqrt ∑normSq`（ℂ，早期实现）——均实现同一数学对象（Frobenius 范数） | ❌ 不合并（注释已加） | 标量域不同（ℝ vs ℂ）、语义同族；Silence 侧注释"新增使用优先 mathlib ‖A‖" |
| ⑥ | `adjUnit`/`adjCounit`：Adjunction vs RAP5a | Adjunction = 抽象伴随（DFunctor/RFunctor）；RAP5a = 线性语义 SpImD 实例（DIm/RIm 本文件定义）——同一伴随概念两个实现层级 | ❌ 不合并（注释已加） | 不同函子实例；RAP5a 侧注释"新增优先复用 Adjunction 抽象定义" |
| ⑦ | 静默度：S_D / silenceDegree / deltaSilence | paper1 §5.7.9 S_D（D-静默度，投影到 Im(D)，表示层）；RAP4 silenceDegree（1−‖P·Df‖/‖Df‖，投影剩余）；Silence deltaSilence（对易子范数）——同族公式、三种语义 | ❌ 不合并（注释已加） | Silence deltaSilence 注释统一同族结构（对易子/投影/表示层） |
| ⑧ | SilenceLevel / SilenceLayer / LayerIndex 近名 | RAP4 SilenceLevel（strict/asymptotic/epsilon 分级）；MultiSilenceMethodology SilenceLayer（S1-S4 数据表）；BranchCounting LayerIndex（层索引）——近名不同义 | ❌ 不合并（注释已加） | 双向交叉注释明确不同义 |
| ⑨ | `spectralSilence` vs `spectralSilenceSimple` | Silence spectralSilence（S1-S4 完整，参数 τ w）；SilenceHierarchy spectralSilenceSimple（S1∧S2 单矩阵子集）——功能子集有意简化 | ❌ 不合并（注释已加） | 注释标注"勿扩展为第三个版本" |

## 防复发清单（新建/修改 Lean 文件前必查）

1. **查登记册**：本文件登记表确认符号/概念是否已有论文登记；
2. **grep 符号名**：`Grep pattern="^def|^theorem|^structure|^inductive|^abbrev|^class" path=UFPFormalization` 确认不重复；
3. **核查论文来源**：数值/字面相同 ≠ 重复——须确认论文出处与推导角色（结论/前提/常数/唯象），禁止凭代码表面特征判定；
4. **import 而非重定义**：确认为纯复制时 `import UFPFormalization.<母文件>` + 限定名引用；
5. **合并后验证**：`lake build` 必须保持 2454 jobs 零警告零 sorry；
6. **跨上下文同步**：论文/笔记/路线图/RAP 引用被删符号处同步更新。

## 附录：Lean→论文初筛索引（2026-08-13 扫描，NONE 待补）

扫描法：Lean 文件头 45 行注释中的 `paperX.md`/`Paper X` 引用。NONE = 头部无明确论文注释（可能对应正文引用/笔记，待逐文件补查）。

| 论文 | Lean 文件（头部注释直引） |
|:-----|:-------------------------|
| Paper I | ICVerification, PhotonTopologyFunctorLaws, Silence |
| Paper III | ICDecidable, SpectralEquivalence |
| Paper V | CategoryGeometry, InflationDynamics, NormalOrdering, Quantization, RenormalizationChain, SpectralDynamics |
| Paper VIII | BlackHoleEvolution |
| Paper IX | BlackHoleBounce |
| Paper XVI | SpacetimeStack |
| Paper XIX | GelfandDuality, InfinityReflection |
| Paper XXXV | HigherRecCategory |
| Paper XXXIX | InflationDynamics |
| paper40 | ColorDynamics |
| paper41 | RenormalizationChain |
| paper44 | CategoryGeometryDictionary, KatoRellichSkeleton, PhotonTopology, PhotonTopology2Category, PhotonTopology2Lifting, PhotonTopologyCurvature, PhotonTopologyFunctor, PhotonTopologyFunctorLaws, PhotonTopologySpectral |

**已知出处补充（正文/笔记关联，非头部直引）**：BranchCounting/DHStructuralAnalysis/Unified3Theorem/BottTower → paper17/20/21/30/33（d_H=ln15、统一 3 定理、k_max=8、Bott 塔）；HigherSpCategory/CoherenceToBranching/DeviationBound → paper31/paper1；SilenceHierarchy/Braided → paper1 §5.7/§2.5；RecCategory/SpCategory/DecursionFunctor/Adjunction → paper1 §2-§4。
