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

## 附录：全库 Lean 文件登记表（2026-08-13 逐项补查，96 文件全覆盖）

角色标记：**推导结论**（自底向上，结构证明导出）/ **推导前提**（推导输入/基础设施，常被复用）/ **常数**（纯数学常数）/ **唯象**（拟合/实验值）/ **工具**（编码/骨架构造）/ **测试**。

### 组 A：Paper I 基础范畴/函子（Rec/Sp/D 函子/∞-范畴/算子论）
| 文件 | 出处 | 核心符号 | 角色 |
|:-----|:-----|:--------|:----:|
| RecCategory | Paper I §2.1 | RecObj/RecHom/recCategory | 推导前提 |
| SpCategory | Paper I §2.2 | SpObj/SpHom/spCategory | 推导前提 |
| DecursionFunctor | Paper I §2.3（注 2.3.2a） | transferMatrix/DFunctor | 工具 |
| Adjunction | Paper I §2.4 | adjUnit/adjCounit/RFunctor | 工具（伴随基础） |
| Braided | Paper I §2.5（定义 2.11a） | recTensorProduct/辫子交叉数 k | 推导前提 |
| DynSys | Paper I §2.7（推测，无显式声明） | DynSys/koopmanLinfty | 工具 |
| OperatorTheory | Paper I §2.7/§4 | koopmanOperator/koopmanContraction/isMAccretive | 推导前提 |
| OrbitFunctor | Paper I §3.5（定义 3.8/3.10） | orbitRel/orbitWeight/orbitStabilizer | 工具 |
| AInfinityAlgebra | Paper I §2.11 + 附录 A.15.4 | ad/mN/stasheff_* | 推导前提 |
| InfinityCategory | Paper I §2.11 + 附录 A.15.4 | KillingField/ForceGenerators/unifiedSpectralFlow | 推导结论+唯象 |
| SpecInfinity | Paper I §2.11 + 附录 A.15.4 | SpecInfMorphism/SpecInfinity | 工具 |
| RecInfinity | Paper I §2.11 + 附录 A.15.4 | RecInfinity/RecInfMorphism | 工具 |
| DInfinityFunctor | Paper I §2.11 + 附录 A.15.4 | DInfinity_obj/one/inf | 推导结论 |
| DomainExtension | Paper I §2.3/§2.8（推测，Phase 15 residual） | ExpansiveIFS/contractiveDual/D_ext_* | 工具 |
| HigherDecursionFunctor | 笔记 deepening §A.2（定理 A.1）= Paper V §8.1 定理 8.1 | D2/D2_map_* | 工具 |
| HigherRecCategory | 笔记 rec2_exchange_deviation §4.3（定义 8 路径 B）+ Paper XXXV §2 | RecTwoMorphism/recExchangeLaw_* | 工具+唯象（Δ=引力） |

### 组 B：Paper I 静默/谱/遍历/分形
| 文件 | 出处 | 核心符号 | 角色 |
|:-----|:-----|:--------|:----:|
| Silence | Paper I §5.2（S1-S4）/§3.6（LACI）/§5.7.9（S_D） | silenceS1-S4/laciIndex/spectralSilence/deltaSilence | 推导前提 |
| SilenceHierarchy | Paper I §5.7（定理 5.15 层次；头部"定理 5.18/四层"为旧口径，见口径偏差①） | objectSilence/morphismSilence/spectralSilenceSimple/braidedSilence | 推导结论 |
| MultiSilenceMethodology | paper17 §2.2/§6.2 + 笔记 | S₁-S₄_factor/productDecomposition | 工具+唯象 |
| PhysicalSilenceAnalysis | paper17 §3.1/§5.1/§9 + 笔记 | higgsVEV_silence_prediction/kerr_QNM_frequency/dm_relic_density | 唯象 |
| SpectralCorrespondence | Paper I §3.4（定理 3.7a/3.7b，公式逐字对应） | spectralMap(μ↦e⁻μ)/spectralInv | 工具 |
| SpectralFlowHomotopy | Paper I §5.7.6a（paper1 点名） | spectralFlowMap/h_silence/spectralFlowInfEndo | 推导结论 |
| SpectralGap | paper20 §4.3/§5.4/§6 | agEigenvalue/spectralGap/Δλ_min | 推导结论 |
| ErgodicTheory | Paper I §7.10（Ledrappier-Young + 拓扑熵-谱间隙） | lyapunovExponent/OseledetsSplitting/HD-D/TE-G-M | 推导前提 |
| IFSFractal | Paper I 附录 Phase 16C-II + paper17 §3.1/§3.2 | IFS/hutchinsonOperator/HausdorffDimension/c1_physical | 工具 |
| WeierstrassGap | 笔记 spectral_phase3_fractal_expansion §2.3（S5） | weierstrassGraphMap/weierstrassGraphDimension | 工具+唯象 |
| HutchinsonAttractor | paper34 §1（Step 1）+ paper30 | hutchinsonK/hutchinson_attractor_exists_unique | 工具 |
| ContinuumLimit | paper34 §2/§3.5（paper34 点名） | S₄/c1_physical/c1_lt_S₄/AttractorAxioms | 推导前提 |
| CoherenceToBranching | paper30 §2.4/§2.5 + paper33 §4.1 + paper17（定理 R1） | LayerProduct/B(=15)/BranchCountingCorollary | 推导前提 |

### 组 C：d_H=ln15 推导链（登记册 ②④ 相关，章节细化）
| 文件 | 出处 | 核心符号 | 角色 |
|:-----|:-----|:--------|:----:|
| DHStructuralAnalysis | paper30 §2-§6 + paper17（定理 R1）+ paper37 | ln15/d_H_fit/delta_fit/sixtyfive_over_24/moran_solution_iff | 推导前提+常数 |
| BranchCounting | paper30 §2/§2.4/§2.5 + paper17（定理 R1） | LayerIndex/N_total/N_active/B(=15) | 推导结论（计数） |
| Unified3Theorem | paper33 §3/§5 | ActiveMorphismLayer/numActiveLayers/GenSpace/k_max | 推导结论 |
| BottTower | paper33 §4.1 + paper20 §5.3/§5.4/§5.8 | spinorDim/k_max/bott_truncation_index | 推导前提 |

### 组 D：Paper V/XVI/XIX/XX/XXI 谱动力学与纤维丛
| 文件 | 出处 | 核心符号 | 角色 |
|:-----|:-----|:--------|:----:|
| SpectralDynamics | Paper V §2（谱流方程母定义，全库复用） | spectralFlow/A_F/A_t=exp(tA_F)A₀exp(−tA_F) | 推导前提 |
| CategoryGeometry | Paper V §5 | directionalDerivative/A_GR=G(δR)/G_GR=ad(G)(A) | 工具 |
| Quantization | Paper V §6 | hbar/weylQuantize/quantumCommutator/β(g) | 工具 |
| NormalOrdering | Paper V §6.2 | wickContraction/normalOrderedProduct | 工具 |
| ForceUnification | Paper V §2/§3（§3.4 统一公式） | runningCoupling/unifiedGenerator/α_U≈1/24 | 推导结论 |
| SpacetimeStack | paper16 §10.3（主定理 21） | 谱曲率层 F_ε/谱 Einstein G_ε/CurvatureMatterFunctor | 推导结论 |
| GelfandDuality | paper19 §3.3（开放问题 #2） | D^id/gelfandMap/SpectralDualityData | 工具 |
| InfinityReflection | paper19 §4.2（开放问题 #1） | ℒ_∞/ι_∞/adjUnit_infty | 推导结论 |
| StaticTopologyFormalization | paper19 §3/§5（Rec_id≅CompHaus） | IdExtObj/IdExtHom/Rec_id | 推导结论 |
| NoiseCategory | paper19 §7/§8（Σ-Rec 嵌入） | SigmaRecObj/Sel/Ext/Diss/η_c | 工具 |
| IsolationConstraints | Paper I §3.7（定义 C3.1/定理 C3.2） | isolationConstraint/spectralScaleCompatible 等 | 推导前提 |
| IFSRecCoding | 笔记 category_scope_stratification 阶段 3（推测 paper19 Σ-Rec 系） | symbolicRecObj/symbolicSigmaRecObj | 工具 |
| TempRGFiber | paper21 §3.1-3.2（§9.1 模块总览） | TempObj/RGObj/𝒯̂_Riem | 工具 |
| NoiseFiber | paper21 §4.1 + paper19 §11-13 + paper10 §12.4 | NoiseObj(η)/η_c/𝒩̂ | 工具 |
| SignatureFiber | paper21 §4.2 + paper20 §5.5-5.7 | SigObj(p,q)/sigBottIndex/π_Sig | 工具 |
| KerrFiber | paper21 §5.1（+ paper12 §9） | KerrObj(M,a)/KerrHom | 推导前提 |
| FlavorFiber | paper17 §7 + paper21 §5.2（"Paper XV"为笔误→paper17 §3） | FlavorSector/J_f/d_H/θ₁₂/δ_CP | 推导结论 |
| TotalParameterFiber | paper21 §7/§9.1（Phase 55A-55G 收口） | TotalParamObj/complete_chain | 工具 |
| EFTCodomainFiber | paper21 §9.1（cod 余域纤维化） | EnergyScale(Λ)/ScaleHom/cod | 工具 |
| WeaveProductFiber | paper21 §6.1/§8.2 | TempRGObj/WeaveSection/∂Rec_D | 工具 |
| WeaveBCS | 笔记 spectral_BCS_weave（+ paper21 §8.2/paper14 §2） | a_BCS=1/1.764/d_BCS | 推导结论+常数 |
| CuprateDistribution | 笔记 spectral_cuprate_distribution（+ paper14 §5.1） | CuprateParams/YBCO_params | 唯象 |
| YukawaIFSWeights | 笔记 spectral_yukawa_IFS_weights（+ paper17 §5.4/§3） | FermionSector/IFSContractionFactors/YukawaWeights | 唯象 |
| CategoryRepBridge | paper20 §3.5/§4（SU(2) 范畴涌现） | SU2Generators/pauliSU2/C₂ | 推导结论 |

### 组 E：黑洞/物理应用
| 文件 | 出处 | 核心符号 | 角色 |
|:-----|:-----|:--------|:----:|
| BlackHoleInformation | paper42 §4-§6 + paper8 §5.3 | S_ent(t)/bhPageTime/bekensteinHawkingEntropy | 推导结论 |
| HawkingSpectrum | paper42 §2 + paper8 §4 | greybodyFactor/T_H=C/M/βMω | 推导结论 |
| LeaverComplexity | paper1 定理 7.27b（paper1_rkhs_and_applications） | TridiagonalData/Leaver 三对角矩阵/O(N) | 推导结论 |
| ColorDynamics | paper40 §2.2/§3.2 | color_jacobi_identity/SU(3) f^abc/Q^a | 推导前提 |
| RenormalizationChain | paper41 §4.2/§7 | ad_G^n(A)/β^(n)↔ad_G^n | 推导前提 |
| InflationDynamics | paper39 §5（定理 D3.1） | D(t)=exp(tG)·D₀·exp(−tG) | 推导结论 |
| ThermoFormalism | paper3 §4.4 + paper2（d_H 凹性） | topologicalPressure/Legendre/定理 DC 凹性 | 推导前提 |

### 组 F：RAP 勘误专项（对应《RAP_勘误与立场声明.md》）
| 文件 | 出处 | 核心符号 | 角色 |
|:-----|:-----|:--------|:----:|
| RAP1_weight_uniqueness | RAP 勘误（定理 R1） | w:ℕ→ℝ/s=w(1)/CauchyExponential/w_k=s^k | 推导结论 |
| RAP2_moran_nonrigidity | RAP 勘误（命题 R2） | r_i(d)={S₃S₄,S₄,1}/k(d)/∂d/∂c₃ | 推导结论 |
| RAP3_generation_obstruction | RAP 勘误（定理 R3） | irreducible_real_spinor_dim=16/Cl(1,7)≅M₁₆(ℝ) | 推导结论 |
| RAP4_silence_strictification | RAP 勘误（R4-R9/R10） | V_Λ/P_V/v(f)=‖P_VD(f)‖/‖D(f)‖/SilenceLevel | 推导结论 |
| RAP5a_explicit_adjunction | RAP 勘误（定理 R11） | transferMatrix/SpImD/R_im/D_im/adjUnit | 工具 |

### 组 G：测试件（无单一论文出处，验证所 import 模块）
| 文件 | 出处 | 核心符号 | 角色 |
|:-----|:-----|:--------|:----:|
| TestCategoryTheory | 测试（RecCategory/SpCategory/Adjunction 等） | RecObj/SpObj/DFunctor | 测试 |
| TestOperatorTheory | 测试（OperatorTheory/Silence/Leaver 等） | koopmanLinfty/silenceS1/laciIndex | 测试 |
| TestApplications | 测试（OrbitFunctor/Clifford/Ergodic 等） | orbitWeight/lyapunovExponent | 测试 |
| TestSpectralEquivalence | 测试（SpectralEquivalence/ICVerification 等） | spectralEquivalence/thm41/thm43 | 测试 |

### 组 H：头部注释直接对应（初筛已明确）
Paper VIII→BlackHoleEvolution；Paper IX→BlackHoleBounce；Paper III→ICDecidable, SpectralEquivalence；Paper I→ICVerification；paper44→PhotonTopology, PhotonTopology2Lifting, PhotonTopology2Category, PhotonTopologyFunctor, PhotonTopologyFunctorLaws（+Paper I）, PhotonTopologySpectral, PhotonTopologyCurvature, PhotonTopologyExterior（笔记）, KatoRellichSkeleton, CategoryGeometryDictionary（+paper31 J3 §4.1）；笔记→PhotonTopologyExterior。

## 补查发现的口径偏差（2026-08-13 已全部修正）

1. **SilenceHierarchy 头部"四层静默/定理 5.18"为旧口径** → ✅ 已修正：paper1 §5.7 现为**五层**（S0 表示层 + S1-S4），严格层次为**定理 5.15**。修正：SilenceHierarchy.lean 头部（Four-Layer→"五层体系 S1-S4 动力学/观测子集"）L13/L25/L68/L118（定理 5.18→5.15）；paper19_category_extension.md L720/L987（引用 paper1 旧编号 5.18→5.15）。
2. **SpectralGap.lean 与 BottTower.lean 注释中 Cl(1,7)≅M₈(ℝ)/旋量 8 为勘误前旧记** → ✅ 已修正：权威口径 M₁₆(ℝ)/旋量 16（paper20 v0.6 勘误）。修正：SpectralGap.lean L16、BottTower.lean L11 表格（标准旋量 16 | 翻倍工作基准 8）、**同类旧记顺带修正**：NoiseFiber.lean L591、SignatureFiber.lean L80。全库残留 M₈(ℝ) 均为有意保留的勘误说明文字（Clifford/BottTower/SpectralGap/SignatureFiber/RAP3 勘误注 + SignatureFiber 块嵌入数学事实）。
   **延伸修正（2026-08-13，Cl(9,1) 系列）**：SignatureFiber.lean L81 原注"Cl(9,1) ≅ M₁₆(ℝ)"为误 → M₃₂(ℝ)（权威 paper20 L518/paper33 L122）；BottTower.lean 表格 Level 1-3 理顺（真实旋量 32/64/128 与工作基准 spinorDim 8×2^k 分离标注）；paper21 L735 笔误"Cl(17,1) ≅ M₅₁₂(ℝ)"→ M₆₄(ℝ)（权威 paper20/33）。
3. **FlavorFiber.lean 注释"d_H from Paper XV"为笔误** → ✅ 已修正：d_H=ln15+δ 出自 paper17 §3。修正：FlavorFiber.lean L69（from Paper XVII §3 + 勘误标注）。

**修正验证**：`lake build` 2454 jobs 零警告零 sorry（注释层修正不影响编译）。提交见 git log。
