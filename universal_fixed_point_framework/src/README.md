# 核心框架代码

本目录存放「通用不动点范畴框架」的核心实现，不依赖任何具体物理实例。

## 设计目标

- 用 Python 实现递归系统范畴 $\mathbf{Rec}$、谱范畴 $\mathbf{Sp}$、谱化函子 $D$ 的完整原型。
- 所有数值迭代仅作为求解不动点方程的工具方法，不侵入理论本体。

## 模块清单

### 范畴论基础

| 模块 | 功能 | 状态 |
|---|---|---|
| `rec_category.py` | 递归系统范畴 $\mathbf{Rec}$ 的对象、态射、复合律 | ✅ 已完成 |
| `spec_category.py` | 谱范畴 $\mathbf{Sp}$ 的对象、态射、谱映射 | ✅ 已完成 |
| `decursion_functor.py` | 谱化函子 $D: \mathbf{Rec} \to \mathbf{Sp}$，含伴随函子 $D \dashv R$ | ✅ 已完成 |
| `fixed_point_solver.py` | 全域不动点方程 $\mathcal{F}[\mathcal{V}] = \mathcal{V}$ 的数值求解器 | ✅ 已完成 |
| `spectral_correspondence.py` | 谱对应自然同构 $M \cong L$ 的数值验证 | ✅ 已完成 |
| `orbit_functor.py` | 规范群轨道函子 $O$ 的构造与性质验证 + 群表示谱理论（等价类/同谱判定/谱权范数/表示签名） | ✅ 已完成 |

### 连续谱与谱测度

| 模块 | 功能 | 状态 |
|---|---|---|
| `continuous_spectrum_demo.py` | 连续谱测度的数值演示，Lebesgue 分解、$\eta_R$ 同构 | ✅ 已完成 |
| `singular_continuous_spectrum.py` | 奇异连续谱系统刻画（分形谱/谱维数/谱型分类/物理意义） | ✅ 已完成 |
| `spectral_silence.py` | 谱静默：替代紧致化的高维不可见性机制（四判据/维度映射/三物理实例） | ✅ 已完成 |
| `theory_transformation.py` | 理论转化：五种转化模式（同构/态射/伴随/谱静默/轨道函子）+ 完整数值库（可观测量计算、批量转化引擎、M理论层级转化、转化误差分析、LACI风险评估），验证弦论/超弦/M理论/LQG 互相转化可行性 | ✅ 已完成 |
| `string_diagram_calculus.py` | 弦图可视化演算：五类转化弦图生成、弦图演算规则（复合/简化/伴随三角形验证）、弦图到代码自动生成、M理论层级转化弦图、理论转化立方体可视化 | ✅ 已完成 |
| `transformation_invariants.py` | 理论等价不变量：9类核心不变量（谱维数谱系/LACI指数/轨道权重/纠缠熵/熵标度/Lyapunov指数/谱间隙/分形维数/度量维数）+ 理论等价判定定理（充要条件）+ 三类严格判据（严格等价/有效近似/形变态射） | ✅ 已完成 |
| `transformation_simulation_interface.py` | 转化仿真接口：实验数据自动对标、MadGraph对接（LHC截面）、micrOMEGAs对接（暗物质）、数值相对论对接（Kerr ringdown）、实验数据反向约束高维理论、仿真去重与算力优化 | ✅ 已完成 |
| `ntk_fractal_bidirectional.py` | NTK-分形双向转化：IFS→NTK谱转化（最优初始化）、NTK→IFS反向重构（AI可解释）、转化不变量诊断过拟合、大模型消融实验、物理先验AI标准化转化（PINN谱约束） | ✅ 已完成 |
| `theory_taxonomy.py` | 通用理论分类学：理论分类学框架定义、物理理论分类（8个理论）、AI模型分类（3个理论）、复杂系统分类（3个理论）、跨领域统一分类分析、理论演化树可视化、转化路径查找（BFS） | ✅ 已完成 |
| `eft_equivalence_framework.py` | EFT等价性框架：消解基础理论/有效理论二元对立、证明EFT是谱静默单向特例、完整元语言（同构/形变/双向重构）、8层EFT层级体系（弦论UV→量子引力→GUT→电弱→SM→QCD→核物理→经典力学）、谱静默四判据验证 + EFT逆重构唯一性（完备静默信息条件、唯一性定理、非唯一性边界、双向一致性） | ✅ 已完成 |
| `math_phys_unification.py` | 统一数学物理范式：朗兰兹纲领谱对应解释（数论↔几何范畴等价）、镜像对称谱对应解释（Calabi-Yau镜像对Hodge谱转置等价）、全息对偶谱对应解释（bulk↔boundary谱静默转化）、三者统一于通用不动点框架、分形谱量子引力基础框架（分形维数扫描、量子引力谱作用量） | ✅ 已完成 |
| `sc_l_te_g_strict_proof.py` | SC-L/TE-G 严格证明推广：SC-L 严格证明（Ledrappier-Young + 谱对应共形不变性）+ TE-G 严格证明（变分原理 + 迹估计）+ Markov IFS/一般动力系统推广 | ✅ 已完成 |
| `d_functor_extension.py` | D 函子定义域扩展 + Freyd 放宽条件：投影值谱测度 PVM、连续谱对象、谱积分、有限极限保持、ε-解集条件、弱伴随关系 | ✅ 已完成 |
| `d_functor_dissipative_extension.py` | D 函子耗散扩展：非自伴算子伪谱理论、耗散半群框架（Hille-Yosida）、广义伴随关系、Henon 映射耗散版本 | ✅ 已完成 |
| `ns_lb_strict_proof.py` | NS-LB 显式最优常数严格证明：Frostman 引理严格证明、对偶问题求解、显式常数推导、变分原理验证 | ✅ 已完成 |
| `nonzero_curvature_connection.py` | 纤维丛非零曲率联络：Levi-Civita 联络、规范场、曲率张量、平行移动、环绕、Clifford 联络、Dirac 算子 | ✅ 已完成 |
| `spectral_silence_axiomatization.py` | 谱静默测度论公理化定义：A1-A4 公理体系、S1-S4 判据独立性与完备性证明、综合静默度计算 | ✅ 已完成 |
| `d_functor_expansion_if.py` | D 函子扩张 IFS 扩展：扩张 IFS 逆系统构造、不稳定流形理论、双曲谱对象、D 函子映射 | ✅ 已完成 |
| `ns_lb_constant_optimization.py` | NS-LB 常数变分优化：Frostman 常数变分原理、对偶问题求解、稳定性验证 | ✅ 已完成 |
| `feng_wang_concavity.py` | IFS 凹性证明：理论证明框架（变分原理 + 熵凹性）、数值验证 | ✅ 已完成 |
| `attractor_distance.py` | LACI 诊断与吸引子距离计算 | ✅ 已完成 |
| `overfitting_diagnosis.py` | 过拟合诊断报告 | ✅ 已完成 |

### Clifford 值谱理论

| 模块 | 功能 | 状态 |
|---|---|---|
| `clifford_spectrum_demo.py` | $\mathrm{Cl}(p,q)$ 值 Hilbert 空间范畴与纤维丛内蕴结构 + 旋量模结构（原始幂等元、最小左理想、旋量谱定理） | ✅ 已完成 |
| `fiber_bundle_demo.py` | 纤维丛结构数值演示 | ✅ 已完成 |

### RKHS 收敛率理论

| 模块 | 功能 | 状态 |
|---|---|---|
| `rkhs_convergence.py` | RKHS 核收敛性数值演示 | ✅ 已完成 |
| `rkhs_convergence_rate.py` | 强分离 IFS 收敛率上界（定理 NS-1 组合版） | ✅ 已完成 |
| `rkhs_weak_separation.py` | 弱分离 IFS 收敛率上界（定理 NS-2 组合版） | ✅ 已完成 |
| `rkhs_non_separated.py` | 完全非分离 IFS 覆盖熵上界（定理 NS-3 组合版） | ✅ 已完成 |
| `rkhs_non_separated_measure_theoretic.py` | 非分离 IFS 收敛率测度论证明（Frostman/势论，NS-1M~NS-3M） | ✅ 已完成 |
| `high_dimensional_ifs.py` | 高维 IFS 收敛率理论（维数相变/高维切换点） | ✅ 已完成 |

### 正则化与高阶修正

| 模块 | 功能 | 状态 |
|---|---|---|
| `rge_regularization.py` | RG 截断正则化延拓（指数衰减/zeta 函数） | ✅ 已完成 |
| `higher_order_rg_effects.py` | 高阶 RG 效应量化分析 | ✅ 已完成 |
| `ar_positivity_test.py` | $A_R = -\log U_R$ 正性与闭性测试 | ✅ 已完成 |

### 物理应用（Paper II 支撑代码）

| 模块 | 功能 | 状态 |
|---|---|---|
| `sm_mass_2loop.py` | 2-loop SM 质量谱计算 | ✅ 已完成 |
| `bsm_predictions.py` | BSM 新物理预言生成 | ✅ 已完成 |
| `bsm_experiment_validation.py` | BSM 实验数据验证（Planck/LHC/XENONnT/LZ） | ✅ 已完成 |
| `bsm_relic_calibration.py` | BSM 热遗迹密度多通道校准 | ✅ 已完成 |
| `bsm_precision_interface.py` | BSM 精确计算工具对接接口 | ✅ 已完成 |
| `bsm_signatures.py` | BSM L4 实验签名与排除限 | ✅ 已完成 |
| `bsm_hllhc_fcc_study.py` | BSM HL-LHC/FCC-hh 深度对接 | ✅ 已完成 |
| `holographic_entropy.py` | 全息纠缠熵与分形谱（定理 HE-1~HE-4） | ✅ 已完成 |
| `cft_entanglement_verification.py` | 全息纠缠熵 CFT 验证（N=4 SYM/Ising） | ✅ 已完成 |
| `complex_cft_phase_transition.py` | 复杂 CFT 与全息相变（N=2 SCFT/拓扑相/Hawking-Page） | ✅ 已完成 |
| `kerr_fractal_entropy.py` | Kerr 黑洞分形几何与分形修正熵 | ✅ 已完成 |
| `kerr_nonequatorial_chaos.py` | Kerr 非赤道面混沌与数值相对论对比 | ✅ 已完成 |
| `unification_conjecture_demo.py` | GR+SM 统一谱对应猜想演示 | ✅ 已完成 |
| `gn_emergence_derivation.py` | $G_N$ 从谱对应自然导出 | ✅ 已完成 |

### 开放问题分析

| 模块 | 功能 | 状态 |
|---|---|---|
| `continuous_open_problems.py` | 连续谱开放问题数值分析 | ✅ 已完成 |
| `orbit_open_problems.py` | 轨道函子开放问题分析 | ✅ 已完成 |
| `unification_open_problems.py` | 统一猜想开放问题分析 | ✅ 已完成 |
| `math_open_problems_advanced.py` | 非分离 IFS 收敛率下界 + 奇异连续谱-Lyapunov 关联 + IFS/Ruelle/最优条件转移算子 + 拓扑熵-谱间隙不等式 + Markov IFS 严格框架 + Koopman TE-G 推广 | ✅ 已完成 |
| `numerical_engineering_open_problems.py` | MadGraph/micrOMEGAs 调用接口 + 双星引力波仿真 | ✅ 已完成 |
| `physics_open_problems_advanced.py` | Kerr 全局量子谱（含 Leaver 简化/精确/自洽 Teukolsky） + N=4 SYM（含强耦合/BES/O(g⁶) BES/TBA） + 暗物质分形谱 | ✅ 已完成 |
| `dynamic_spectrum/leaver_unified_solver.py` | **最终版 Leaver QNM 统一求解器**：基于分形谱化理论，集成 DerecursionAnalyzer（Koopman 谱分析）+ LeaverResidual（修正系数）+ LACIEvaluator（物理根选择）+ LeaverUnifiedSolver（双重 Homotopy）。**替代已归档的早期实现**：`leaver_corrected_solver.py`（正确的二次多项式系数 + 角向谱方法 + 同伦延拓）、`leaver_spectral_derecursion.py`（连分数→三对角矩阵 + 双初始向量逆迭代法逆迭代）、`leaver_derecursion.py`（乘积形式系数早期版本）——以上已移入 `_archive/leaver_deprecated/` | ✅ 已完成 |
| `error_budget.py` | 误差预算体系：Rec→Spec→预言→实验 全链路误差传播（ErrorSource/ErrorBudget + Rec/Spec/预言/RKHS/G_N 误差估计 + 误差链传播） | ✅ 已完成 |

### 实验数据分析（2026-08-28 从 research_notes 整理）

| 目录/模块 | 功能 | 状态 |
|---|---|---|
| `white_dwarf_analysis/` | 白矮星光谱分析（v3–v11 迭代：v11 补全 $10^3$–$10^4$ T 缺口 + 选择效应四类显性证伪检验；$T_{\text{eff}}$ 正效应与量子混沌拓扑展宽代数桥梁验证（$c_{\text{theory}}/c_{\text{obs}}=0.79$）；SDSS/LAMOST 数据对接） | ✅ 已完成 |
| `nmlo_emission/` | 非马尔可夫线型算子（NMLO，Paper XLVIII §5.5）：Cantor 奇异连续谱测度 → 幂律记忆核 → 混合谱线型 → 发射 EW 线序标度拟合（$m=3.39$，$R^2=0.80$）；非局域相关时间（NLCT）精确标度方程验证（尾区斜率 $\beta=2+D$、$\tau_{\text{NL}}=D/(1+D)\cdot T$） | ✅ 已完成 |
| `harper_analysis/` | Harper 谱分析（光谱数据解析） | ✅ 已完成 |
| `hydrogen_analysis/` | 氢原子磁/辐射分析（Stark 效应、B 场测量） | ✅ 已完成 |
| `sdss_lamost_query/` | SDSS/LAMOST 公开数据查询与下载工具 | ✅ 已完成 |
| `rydberg_stark_analysis/` | Rydberg 态 Stark 效应分析 | ✅ 已完成 |
| `blue_end_analysis/` | 蓝端白矮星光谱 SDSS 分析 | ✅ 已完成 |

**数据路径约定**：
- 结果数据（JSON）→ `../results/`
- 公开数据（FITS/DAT）→ `../data/`
- 分析代码中的路径已统一为绝对路径或相对于项目根目录的路径

## 测试

| 测试文件 | 覆盖内容 | 状态 |
|---|---|---|
| `test_decursion_functor.py` | $D$ 函子、伴随函子、三角恒等式 | ✅ 通过 |
| `test_orbit_functor.py` | 轨道函子 + 群表示谱理论（等价类/同谱判定/谱权范数/表示签名） | ✅ 通过 |
| `test_spectral_correspondence.py` | 谱对应自然同构 | ✅ 通过 |
| `test_overfitting_diagnosis.py` | 过拟合诊断 / LACI | ✅ 通过 |
| `test_weak_intertwining.py` | 弱交织模式 | ✅ 通过 |
| `test_open_problems_advanced.py` | 开放问题推进模块（数学/数值/物理，含 IFS/Ruelle/最优条件、TE-G/Markov/Koopman、Leaver 简化/精确/自洽、N=4 强耦合/BES/O(g⁶) BES） | ✅ 通过 |
| `test_error_budget.py` | 误差预算体系（ErrorSource/ErrorBudget + Rec/Spec/预言/RKHS/G_N 误差估计 + 误差链传播） | ✅ 通过 |

## 与论文的对应关系

| 论文章节 | 对应代码模块 |
|---|---|
| **Paper I §2-3**：范畴论基础、谱化函子、全域不动点 | `rec_category.py`、`spec_category.py`、`decursion_functor.py`、`fixed_point_solver.py`、`spectral_correspondence.py` |
| **Paper I §4**：连续谱与谱测度 | `continuous_spectrum_demo.py`、`singular_continuous_spectrum.py` |
| **Paper I §5**：Clifford 值谱与纤维丛 | `clifford_spectrum_demo.py`、`fiber_bundle_demo.py`、`test_clifford_spinor_module.py` |
| **Paper I §6**：RKHS 收敛率 | `rkhs_convergence_rate.py`、`rkhs_weak_separation.py`、`rkhs_non_separated.py`、`rkhs_non_separated_measure_theoretic.py`、`high_dimensional_ifs.py` |
| **Paper I §7.4/§8.2**：开放问题推进（非分离 IFS 下界、Lyapunov-谱维数关联） | `math_open_problems_advanced.py` |
| **Paper I §5**：谱静默理论 | `spectral_silence.py` |
| **Paper I §7.7**：理论转化与 EFT 等价性框架 | `theory_transformation.py`、`eft_equivalence_framework.py` |
| **Paper I §7.7.3**：弦图演算 | `string_diagram_calculus.py` |
| **Paper I §7.7.4**：理论等价不变量与判定定理 | `transformation_invariants.py` |
| **Paper II §2-3**：标准模型、GR+SM 统一 | `sm_mass_2loop.py`、`unification_conjecture_demo.py`、`gn_emergence_derivation.py` |
| **Paper II §4**：BSM 物理与实验 | `bsm_predictions.py`、`bsm_signatures.py`、`bsm_hllhc_fcc_study.py`、`bsm_relic_calibration.py`、`bsm_experiment_validation.py`、`bsm_precision_interface.py` |
| **Paper II §5**：Kerr 黑洞与引力波 | `kerr_fractal_entropy.py`、`kerr_nonequatorial_chaos.py` |
| **Paper I §7.8**：谱化理论在 Kerr Leaver 连分数中的应用 | `dynamic_spectrum/leaver_unified_solver.py`（**最终版**；早期探索实现 `leaver_corrected_solver.py`、`leaver_spectral_derecursion.py`、`leaver_derecursion.py` 已归档至 `_archive/leaver_deprecated/`） |
| **Paper II §8.2/A.12**：开放问题推进（Kerr 量子谱、N=4 SYM、暗物质分形谱、MadGraph/micrOMEGAs、双星引力波） | `physics_open_problems_advanced.py`、`numerical_engineering_open_problems.py` |
| **Paper II §6-7**：全息纠缠熵、CFT、理论转化应用 | `holographic_entropy.py`、`cft_entanglement_verification.py`、`complex_cft_phase_transition.py`、`transformation_simulation_interface.py`、`ntk_fractal_bidirectional.py`、`theory_taxonomy.py`、`eft_equivalence_framework.py`、`math_phys_unification.py`、`philosophical_foundations.py` |
| **Paper II §7.5**：误差预算体系 | `error_budget.py` |

---

## 变更记录

| 日期 | 更新内容 | 新增模块 |
|---|---|---|
| 2026-07-15 | 谱化深化："双初始向量逆迭代法"逆迭代优化（Thomas算法 + Rayleigh商，O(N³)→O(N)），多吸引子谱优势定理（平衡点K≈3）（该模块现已归档至 `_archive/leaver_deprecated/`，最终版见 `dynamic_spectrum/leaver_unified_solver.py`） | `leaver_spectral_derecursion.py` 增强（已归档） |
| 2026-07-15 | 谱化理论实质验证：新增 `leaver_corrected_solver.py`（正确二次多项式系数）和 `leaver_spectral_derecursion.py`（谱分解方法），三路径对照验证（迭代 vs 谱分解 vs qnm 包）给出一致 QNM 频率（均已归档至 `_archive/leaver_deprecated/`，最终版见 `dynamic_spectrum/leaver_unified_solver.py`） | `leaver_corrected_solver.py`、`leaver_spectral_derecursion.py`（均已归档） |
| 2026-07-13 | 同步 Paper I v2.5：§5.6 谱静默定理深化、§7.7 理论转化/EFT/弦图演算方法论系统化 | 论文对应关系更新 |
| 2026-07-13 | 数学严格化深化：`math_open_problems_advanced.py` 新增 IFS 热力学形式；`physics_open_problems_advanced.py` 新增 Leaver 连分数 Kerr QNM、强耦合 N=4 SYM；测试数从 47 增至 52 | 开放问题推进 |
| 2026-07-13 | 数学严格化再深化：`math_open_problems_advanced.py` 新增 Ruelle 精确转移算子、拓扑熵-谱间隙不等式；`physics_open_problems_advanced.py` 新增 Leaver 精确系数、N=4 SYM 简化 BES/TBA；测试数从 52 增至 57 | 开放问题推进 |
| 2026-07-13 | 数学严格化三阶段深化：`math_open_problems_advanced.py` 新增 IFS 条件转移算子、Markov IFS 下 TE-G 严格框架；`physics_open_problems_advanced.py` 新增完整 Teukolsky-Leaver 求解器、N=4 SYM 完整 BES/TBA 升级；测试数从 57 增至 61 | 开放问题推进 |
| 2026-07-13 | 数学严格化四阶段深化：`math_open_problems_advanced.py` 新增 IFS 最优条件转移算子、Koopman TE-G 推广；`physics_open_problems_advanced.py` 新增 spheroidal λ 自洽迭代、O(g⁶) BES/TBA；测试数从 61 增至 64 | 开放问题推进 |
| 2026-07-13 | 代码质量修复：移除 D 函子 Koopman 矩阵强制对称化；`from_koopman` 增加 logm fallback 处理不可对角化矩阵；忠实性测试扩展为多组随机态射验证；`map_morphism` 增加交织验证选项；Callable 演化增加误差估计 | `decursion_functor.py` `spec_category.py` `rec_category.py` `test_decursion_functor.py` |
| 2026-07-13 | Phase 15A-1 高维 IFS 数值验证：新增 `test_high_dimensional_ifs.py`（13 项：解析层 8 + 数值层 2 + 相变层 2 + 跨维数 1），覆盖合成核矩阵幂律衰减验证 | `test_high_dimensional_ifs.py` |
| 2026-07-13 | Phase 15A-2 Kerr 校准：新增 `test_qnm_calibration.py`（4 项 + 1 xfail），homotopy continuation 修复 m=0；改进 `qnm_frequency_approximation` | `test_qnm_calibration.py` `physics_open_problems_advanced.py` |
| 2026-07-13 | Phase 15A-3 FCC 系统误差：新增 `test_bsm_systematic_errors.py`（4 项），修复 sigma_sys=0 退化 | `test_bsm_systematic_errors.py` |
| 2026-07-13 | Phase 15A-5 谱静默等价链：新增 `test_spectral_silence_equivalence.py`（7 项），修正定理 5.4 等价性为以 S2 为基准 | `test_spectral_silence_equivalence.py` |
| 2026-07-13 | Phase 15A-6 BSM S/T 参数：新增 `bsm_oblique_parameters.py` 与 `test_bsm_oblique.py`（6 项），Peskin-Takeuchi 公式 | `bsm_oblique_parameters.py` |
| 2026-07-13 | Phase 15B-7 不变量充要性提升：新增 `test_transformation_invariants.py`（4 项），`transformation_invariants.py` 新增动力学相容性检查与完备性缺口分析 | `transformation_invariants.py` |
| 2026-07-14 | Phase 15C-1 轨道函子群表示谱理论：`orbit_functor.py` 新增 `weight_equivalence_class`/`same_spectrum_criterion`/`spectrum_charge`/`representation_signature`/`compute_ratios`；`test_orbit_functor.py` 新增 5 项测试；测试数从 105 增至 121 | `orbit_functor.py` |
| 2026-07-14 | Phase 15C-4 误差预算体系：新增 `error_budget.py`（ErrorSource/ErrorBudget + Rec/Spec/预言/RKHS/G_N 误差估计 + 误差链传播）与 `test_error_budget.py`（11 项测试） | `error_budget.py` |
| 2026-07-14 | Phase 15C-2 Clifford 旋量模结构：`clifford_spectrum_demo.py` 新增 `clifford_idempotent`/`spinor_module_basis`/`spinor_dim`；新增 `test_clifford_spinor_module.py`（9 项测试）；测试数从 121 增至 130 | `clifford_spectrum_demo.py` |
| 2026-07-13 | 新增 M理论层级谱静默转化数值案例 | `spectral_silence.py`（新增函数） |
| 2026-07-13 | 新增理论等价不变量完备集合与判定定理 | `transformation_invariants.py` |
| 2026-07-13 | 新增弦图可视化演算 | `string_diagram_calculus.py` |
| 2026-07-13 | 新增理论转化完整数值库升级 | `theory_transformation.py`（扩展） |
| 2026-07-13 | 新增理论转化五种转化模式 | `theory_transformation.py` |
| 2026-07-13 | 新增谱静默理论 | `spectral_silence.py` |
| 2026-07-13 | 新增高维 IFS 收敛率理论 | `high_dimensional_ifs.py` |
| 2026-07-13 | 新增奇异连续谱刻画 | `singular_continuous_spectrum.py` |
| 2026-07-13 | 新增测度论收敛率证明 | `rkhs_non_separated_measure_theoretic.py` |
| 2026-07-13 | 推进开放问题：非分离 IFS 下界、奇异连续谱-Lyapunov 关联 | `math_open_problems_advanced.py` |
| 2026-07-13 | 推进开放问题：MadGraph/micrOMEGAs 接口、双星引力波仿真 | `numerical_engineering_open_problems.py` |
| 2026-07-13 | 推进开放问题：Kerr 量子谱、N=4 SYM、暗物质分形谱 | `physics_open_problems_advanced.py` |
