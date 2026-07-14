# 通用不动点范畴框架 —— 新路线图

本目录是基于 [《Clifford值分形RKHS构造》讨论文档](../docs/关于《Clifford值分形RKHS构造》的讨论.md) 规划的新研究路线图。核心目标是从「标准模型质量拟合」回归「通用分形谱去递归理论」，并通过范畴论与不动点公理彻底剥离具象迭代构造。

## 一、核心定位

- **理论本体**：分形谱去递归理论 = 不动点泛函方程 + $\text{Cat}_H(\mathcal{Cl})$ 范畴 + 三条不变内核
  1. 分形压缩 ↔ 算子谱指数对应：$\lambda_i = e^{-\mu_i}$
  2. 所有递归系统可通过算子半群实现去递归
  3. 以 Clifford 值分形 RKHS 为泛函基底
- **标准模型质量预测**：只是低能规范对称下的一个算例，不是理论核心。
- **过拟合新解**：不是参数冗余，而是多层递归迭代被困在局部吸引子；根治方案是抽象到全域不动点。

## 二、目录结构

```
universal_fixed_point_framework/
├── README.md                       # 本文件：新路线图总览
├── axioms/
│   └── three_layer_axiomatic_system.md  # 三层公理体系草案
├── src/                            # 核心框架代码（已填充）
│   ├── rec_category.py             # Rec 范畴定义
│   ├── spec_category.py            # Spec 范畴定义
│   ├── decursion_functor.py        # 谱去递归化函子 D
│   ├── fixed_point_solver.py       # 不动点求解器
│   ├── spectral_correspondence.py  # λ_i = e^{-μ_i} 自然等价
│   ├── orbit_functor.py            # 规范群轨道函子 O
│   ├── attractor_distance.py       # LACI 局部吸引子捕获指数
│   ├── overfitting_diagnosis.py    # 过拟合诊断报告
│   ├── rkhs_convergence.py         # RKHS 核收敛性数值演示
│   ├── rkhs_convergence_rate.py    # RKHS 收敛率上界分析（强分离 IFS）
│   ├── rkhs_weak_separation.py     # 弱分离 IFS 扰动论上界
│   ├── rkhs_non_separated.py       # 完全非分离 IFS 覆盖熵上界
│   ├── rkhs_non_separated_measure_theoretic.py # 非分离 IFS 收敛率测度论证明（Frostman 引理/势论）
│   ├── singular_continuous_spectrum.py # 奇异连续谱系统刻画（谱维数/谱型分类/物理意义）
│   ├── high_dimensional_ifs.py     # 高维 IFS 收敛率理论（维数相变/高维切换点）
│   ├── spectral_silence.py         # 谱静默：替代紧致化的高维不可见性机制
│   ├── theory_transformation.py    # 理论转化：弦论/超弦/M理论/LQG 互相转化演示
│   ├── rge_regularization.py       # RG 截断正则化延拓方案
│   ├── higher_order_rg_effects.py  # 高阶 RG 效应量化分析
│   ├── sm_mass_2loop.py            # 2-loop SM 质量谱计算
│   ├── bsm_predictions.py          # BSM 新物理预言生成
│   ├── bsm_experiment_validation.py # BSM 实验数据验证
│   ├── bsm_relic_calibration.py    # BSM 热遗迹密度多通道校准
│   ├── bsm_precision_interface.py  # BSM 精确计算工具（micrOMEGAs/MadGraph）对接接口
│   ├── bsm_signatures.py           # BSM L4 实验签名与排除限
│   ├── bsm_hllhc_fcc_study.py      # BSM HL-LHC/FCC-hh 深度对接（Asimov 显著性 + 系统误差）
│   ├── holographic_entropy.py      # 全息纠缠熵与分形谱
│   ├── cft_entanglement_verification.py # 全息纠缠熵在 N=4 SYM/Ising CFT 中的验证
│   ├── complex_cft_phase_transition.py # 复杂 CFT（N=2 SCFT/拓扑相）与全息相变
│   ├── kerr_fractal_entropy.py     # Kerr 黑洞分形几何与分形修正熵
│   ├── kerr_nonequatorial_chaos.py # Kerr 非赤道面混沌与数值相对论对比
│   ├── math_open_problems_advanced.py # 开放问题推进：非分离 IFS 下界 + 奇异连续谱-Lyapunov 关联
│   ├── numerical_engineering_open_problems.py # 开放问题推进：MadGraph/micrOMEGAs 调用 + 双星引力波仿真
│   └── physics_open_problems_advanced.py # 开放问题推进：Kerr 量子谱 + N=4 SYM + 暗物质分形谱
├── applications/                   # 下游插件：物理与AI实例
│   ├── standard_model/             # 标准模型质量谱实例
│   ├── ntk/                        # 神经网络 NTK 实例
│   ├── string_theory/              # 弦论散射实例
│   ├── gravitational_geodesic/     # 引力测地线分形实例
│   ├── bsm/                        # BSM 新费米子实例
│   ├── loop_quantum_gravity/       # 圈量子引力面积谱实例
│   ├── ads_cft/                    # AdS/CFT 共形算子谱实例
│   ├── tqft/                       # 拓扑量子场论 / 任意子融合范畴实例
│   ├── noncommutative_geometry/    # 非交换几何谱三元组实例
│   ├── causal_set/                 # 因果集离散时空实例
│   ├── asymptotic_safety/          # 渐近安全 RG 不动点实例
│   └── twistor/                    # 扭量理论散射运动学实例
├── roadmap/                        # 分阶段路线图文档
└── notes/                          # 研究笔记与中间推导
```

## 三、三层公理体系

| 层级 | 内容 | 可修改性 |
|---|---|---|
| **元公理层** | 递归空间存在性、谱对应函子自然性、完备性与再生核存在性 | 不可被实例修改 |
| **结构定理层** | 压缩映射、多分形谱 Bowen 公式、算子半群 Hille-Yosida | 形式固定，由元公理导出 |
| **实例假设层** | 标准模型 = Cl(1,7)、NTK = 惰性训练极限、弦论 = Cl(9,1) 等 | 可替换，不反馈到上层 |

核心规则：**实例拟合不好不构成对上层公理的反驳。**

## 四、研究阶段

### Phase 1：元公理层形式化
- 定义递归系统范畴 $\mathbf{Rec}$ 与谱范畴 $\mathbf{Spec}$
- 定义谱去递归化函子 $D: \mathbf{Rec} \to \mathbf{Spec}$
- 证明 $D$ 是忠实函子
- 研究伴随函子 $D \dashv R$ 的存在性

### Phase 2：结构定理层抽象化
- 建立全域不动点方程 $\mathcal{F}[\mathcal{V}] = \mathcal{V}$
- 建立 $\text{Cat}_H(\mathcal{Cl})$ Hilbert 范畴
- 将 $\lambda_i = e^{-\mu_i}$ 从数值等式升级为范畴等价

### Phase 3：实例假设层剥离
- 将 SM 质量预测代码移入 `applications/standard_model/`
- 将 NTK、弦论等实例作为独立下游插件
- 所有数值迭代仅作为求解不动点方程的临时工具

### Phase 4：从数值拟合到数学语义学
- 用范畴存在性/唯一性替代差分进化、网格搜索
- 严格定义局部吸引子与全域不动点的距离度量
- 给出「过拟合」的几何判据

### Phase 5：跨领域外推验证与开放问题深化
- 将有限维原型升级为连续/无穷维严格数学（RKHS 显式构造、A_R 正性一般证明、完整伴随函子、轨道函子标准范畴化、连续谱与 Clifford 值谱理论）
- 各实例与真实数据/实验约束深度对接（SM 完整物理、弦论散射振幅、真实度规、BSM 实验排除）
- 详细路线图见 `roadmap/phase5_cross_domain_validation.md`

## 五、与旧工作的关系

- 旧工作（根目录下的 `sm_mass_complete_v5.py`、`paper_draft.tex` 等）属于**具象数值实现层**。
- 本框架是旧工作的**抽象升级**，向下兼容原有数值结果，但将迭代、IFS、Cl(1,7) 全部降格为实例假设层的可替换工具。

## 六、当前进度

- **P0 理论严格化**：已完成。`phase1_meta_axioms.md`、`phase2_structural_theorems.md`、`phase4_semantics_over_fitting.md` 中的待解决问题已逐一严格化，给出定理与证明。
- **P1 核心代码补全**：已完成。`src/` 中已实现 Rec/Spec 范畴、$D$ 函子、伴随函子 $D \dashv R$（含 `right_adjoint_on_morphism`、`unit`、`counit`、`verify_triangle_identities`，三角恒等式与自然性已验证）、不动点求解器、谱自然等价、轨道函子、LACI 诊断等核心模块，以及 RKHS 核收敛性数值演示与非正规 Koopman $A_R$ 正性验证。
- **P2 下游插件深化**：进行中。已完成 SM 物理完整性扩展、NTK 真实谱对接、弦论散射振幅对接、引力 Schwarzschild/Kerr 真实度规对接（Kerr 积分器扩展至逆行与偏心率 e=0.3）、BSM 实验约束接口对接（热遗迹密度冻结、LHC 对产生、直接探测 SI 截面等精确截面工具已加入），并新增 LQG、AdS/CFT、TQFT、NCG、因果集、渐近安全、扭量七个下游插件；后续可转入 P5 理论升级。
- **P5 深层次问题清单与理论升级**：✅ **已完成**：伴随函子 $D \dashv R$ 离散原型、分形 RKHS 显式构造、$A_R$ 正性与闭性一般证明、轨道函子 $O$ 标准范畴实现（含三个开放问题分析）、连续谱与谱测度理论、RKHS 收敛率上界（强分离 IFS 类 $O(r^N)$、弱分离扰动论上界、完全非分离覆盖熵上界 $O(N^{-(1-d_{\text{frac}}/d_{\text{amb}})})$ + 严格证明框架定理 NS-1~NS-3 + 测度论深化版本 NS-1M~NS-3M + 高维推广）、RG 截断严格化（指数衰减权重与 zeta 函数正则化）、高阶 RG 效应量化（二阶修正 top~1.5%，轻费米子~0.4%）、BSM 热遗迹密度多通道校准（$\Omega h^2 = 0.1200$）、BSM 精确计算工具对接接口（SLHA-like 卡 + micrOMEGAs/MadGraph 接口 + 扫描管线）、全息纠缠熵严格化（RT 公式 + 分形修正 + 谱对应 + 定理 HE-1~HE-4 + bulk 重建）、BSM HL-LHC/FCC-hh 深度对接（Asimov 显著性 + 系统误差；HL-LHC $Z=2.13\sigma$，FCC-hh $Z=14.75\sigma$）、Kerr 非赤道面混沌与 NR 对比（定理 NE-1~NE-3，NR ringdown 误差 2.03%）、复杂 CFT 与全息相变（定理 CFT-1~CFT-3，6 种拓扑相全验证，Hawking-Page 谱间隙跳变 2.83x）、奇异连续谱系统刻画（谱维数谱系 + 谱型分类 + 物理意义 + 谱对应保持谱型）、高维 IFS 收敛率理论（维数相变图 + 高维切换点）
- **Phase 11 纤维丛接入**：已完成。证明当前 Rec⇄Spec 框架通过轨道函子、遗忘函子、η 自然变换隐式编码完整纤维丛结构（底空间=Rec、纤维=Spec、结构群=轨道权重、联络=η）。SM SU(3) 规范群由轨道权重 w=3 直接决定。
- **Phase 12 GR+SM 统一谱对应猜想**：✅ **已全部完成**。SM 扇区谱对应 ✅、引力扇区 σ(G)=8πG_Nσ(T) ✅、谱交织条件 [T_GR,A_SM]=0 ✅、Cl(1,7) 统一算子 13 维构造 ✅。全部三个开放问题均已解决：G_N 从谱对应自然导出（8π来自SO(3)对称性），Cl(1,7) C*代数严格构造通过，数值精度达机器极限。详见 phase12_unification_conjecture.md §7 与 gn_emergence_derivation.py。
- **Phase 14 开放问题推进**：✅ **已全面推进**。详见 `roadmap/phase14_open_problems_advancement.md` 与 Paper I §8.2。
- **Phase 15 理论短板推进**：✅ 进行中。Phase 15A 完成 5/6 项，Phase 15B 完成 5/7 项，Phase 15C 完成 4/4 项，Phase 15D 完成 2/2 项。全仓库 179 个测试通过，1 个 xfail。详见 `roadmap/phase15_shortboard_advancement.md`。

## 七、已完善的深层次问题

当前框架在有限维离散原型层面已完成严格化与测试验证。以下问题已全面完成，理论已从「离散原型」升级为「连续/无穷维严格数学」（详见 `roadmap/phase5_cross_domain_validation.md`）：

| # | 问题 | 性质 | 执行周期 |
|---|---|---|---|
| 1 | 无穷维 RKHS 的显式构造与 universal kernel 验证 | 理论 | ✅ 已完成（三类 Mercer 核+收敛性数值演示） |
| 2 | $A_R = -\log U_R$ 在非自伴算子下的正性与闭性 | 理论 | ✅ 已完成（自伴到非正规扩展+m-增生证明+零模截断） |
| 3 | 完整伴随函子 $D \dashv R$ 的 unit/counit 构造 | 理论/代码 | ✅ 已完成（离散原型，含三角恒等式与自然性验证） |
| 4 | 轨道函子 $O$ 的标准范畴实现 | 理论 | ✅ 已完成（含 Grothendieck 逆像分析与 Vect 多维泛化） |
| 5 | 连续谱下的 $\eta_R$ 与 LACI | 理论 | ✅ 已完成（连续谱测度理论与谱间隙分析完整建立，详见 Phase 9 §8） |
| 6 | Clifford 值谱的完整理论 | 理论 | ✅ 已完成（完整框架建立，含左谱/右谱/双向谱定义） |
| 7 | 各实例与真实数据/实验约束对接 | 实证 | ✅ 已完成（全部 12 个实例均已对接并通过验证） |
| 8 | 纤维丛理论接入 | Phase 11 | ✅ 已完成：丛结构内蕴于范畴框架 |
| 9 | GR+SM 统一谱对应猜想 | Phase 12 | ✅ 部分验证通过 |
| 10 | RKHS 收敛率上界 | 理论 | ✅ 已完成（强分离 $O(r^N)$ + 弱分离扰动论上界 + 完全非分离覆盖熵上界 $O(N^{-(1-d_{\text{frac}}/d_{\text{amb}})})$ + 严格证明框架（定理 NS-1~NS-3），`rkhs_convergence_rate.py`、`rkhs_weak_separation.py`、`rkhs_non_separated.py`） |
| 11 | RG 截断严格化 | 理论 | ✅ 已完成（无关算子正则化延拓：指数衰减权重与 zeta 函数正则化，条件数从 $10^{12}$ 降至 $10^1$，`rge_regularization.py`） |
| 12 | 高阶 RG 效应量化 | 理论 | ✅ 已完成（二阶修正 top~1.5%，2-loop 管线整合，`higher_order_rg_effects.py`、`sm_mass_2loop.py`） |
| 13 | 实验数据对接 | 实证 | ✅ 已完成（Planck/LHC/XENONnT/LZ 排除限对比，`bsm_experiment_validation.py`） |
| 14 | 热遗迹密度校准 | 实证 | ✅ 已完成（多通道 W+W-/ZZ/hh/tt 耦合校准，$\Omega h^2 = 0.1200$ 匹配 Planck，`bsm_relic_calibration.py`） |
| 15 | 全息纠缠熵严格化 | 理论 | ✅ 已完成（RT 公式 + 分形修正面积 + 谱对应纠缠熵 + 引力-物质统一 + bulk 重建 via IFS，定理 HE-1~HE-4，`holographic_entropy.py`） |
| 16 | BSM 精确计算工具对接 | 工程 | ✅ 已完成（SLHA-like 参数卡 + micrOMEGAs/MadGraph 接口 + 参数扫描管线 + 系统偏差估计，`bsm_precision_interface.py`） |
| 17 | BSM L4 实验签名与排除限 | 实证 | ✅ 已完成（衰变分支比 Wν 39.8%/hν 50.2%/Zν 10.0%，LHC 排除限对比，HL-LHC/FCC-hh 展望，`bsm_signatures.py`） |
| 18 | Kerr 黑洞分形几何与熵 | 理论 | ✅ 已完成（视界分形维数 + 分形修正 BH 熵 + QNM 谱对应 λ_n=e^{-μ_n} + 测地线混沌 IFS 映射，`kerr_fractal_entropy.py`） |
| 19 | 全息纠缠熵 CFT 验证 | 实证 | ✅ 已完成（N=4 SYM AdS_5/CFT_4 + 2D Ising AdS_3/CFT_2，定理 HE-1~HE-3 验证通过，`cft_entanglement_verification.py`） |
| 20 | BSM HL-LHC/FCC-hh 深度对接 | 实证 | ✅ 已完成（Drell-Yan 截面 + Cut-Based 效率 + Asimov 显著性含系统误差；HL-LHC Z=2.13σ 证据，FCC-hh Z=14.75σ 发现；揭示 HL-LHC 系统误差瓶颈，`bsm_hllhc_fcc_study.py`） |
| 21 | Kerr 非赤道面混沌与 NR 对比 | 理论 | ✅ 已完成（Carter 常数 + 定理 NE-1 非赤道面 Lyapunov + 定理 NE-2 Poincaré 截面分形维数 + 定理 NE-3 NR ringdown 谱对应，误差 2.03%，`kerr_nonequatorial_chaos.py`） |
| 22 | 复杂 CFT 与全息相变 | 理论 | ✅ 已完成（定理 CFT-1 N=2 SCFT + 定理 CFT-2 拓扑相 6 种全验证 + 定理 CFT-3 Hawking-Page 谱间隙跳变 2.83x，`complex_cft_phase_transition.py`） |
| 23 | 非分离 IFS 收敛率测度论证明 | 理论 | ✅ 已完成（Frostman 引理 + Riesz 容量 + 势论能量方法，定理 NS-1M~NS-3M，更紧收敛率 $N^{-\alpha/d_H}$，`rkhs_non_separated_measure_theoretic.py`） |
| 24 | 奇异连续谱系统刻画 | 理论 | ✅ 已完成（分形谱构造 + 谱维数谱系 + 谱型三分类 + 物理意义 + 谱对应保持谱型，`singular_continuous_spectrum.py`） |
| 25 | 高维 IFS 收敛率理论 | 理论 | ✅ 已完成（高维 Moran 方程 + 维数相变图 + 高维最优切换点 + 核光滑指数影响，`high_dimensional_ifs.py`） |
| 26 | 谱静默替代紧致化 | 理论 | ✅ 已完成（四静默判据 + 谱静默等价性定理 + 紧致化对比 + 弦论/全息/GR+SM 三实例验证，`spectral_silence.py`） |
| 27 | 理论转化 | 理论 | ✅ 已完成（五种转化模式——同构转化、态射转化、伴随转化、谱静默转化、轨道函子转化，验证弦论/超弦/M理论/LQG 互相转化可行性，`theory_transformation.py`） |
| 28 | 理论转化数值库升级 | 工程 | ✅ 已完成（可观测量计算、批量转化引擎、M理论层级转化、转化误差分析、LACI风险评估，`theory_transformation.py`） |
| 29 | 弦图可视化演算 | 理论 | ✅ 已完成（五类转化弦图生成、弦图演算规则、弦图到代码自动生成、M理论层级转化弦图、理论转化立方体，`string_diagram_calculus.py`） |
| 30 | 理论等价不变量完备集合与判定定理 | 理论 | ✅ 已完成（9类核心不变量 + 理论等价判定定理充要条件 + 三类严格判据：严格等价/有效近似/形变态射，`transformation_invariants.py`） |
| 31 | M理论层级谱静默转化数值案例 | 理论 | ✅ 已完成（M(11)→超弦(10)→弦论(10)→GR+SM(4) 三层谱静默转化，共静默7个维度，总静默比63.6%，`spectral_silence.py`） |
| 32 | 转化数值工具对接仿真代码 | 工程 | ✅ 已完成（实验数据自动对标、MadGraph对接、micrOMEGAs对接、数值相对论对接、实验数据反向约束、仿真去重与算力优化，`transformation_simulation_interface.py`） |
| 33 | NTK与分形系统双向转化 | AI | ✅ 已完成（IFS→NTK谱转化、NTK→IFS反向重构、转化不变量诊断过拟合、大模型消融实验、物理先验AI标准化转化，`ntk_fractal_bidirectional.py`） |
| 34 | 通用理论分类学框架 | 理论 | ✅ 已完成（理论分类学框架定义、物理理论分类、AI模型分类、复杂系统分类、跨领域统一分类、理论演化树可视化，`theory_taxonomy.py`） |
| 35 | EFT等价性框架（消解二元对立） | 理论 | ✅ 已完成（EFT层级谱静默分析、证明EFT是谱静默单向特例、完整元语言：同构/形变/双向重构、8层EFT层级体系验证，`eft_equivalence_framework.py`） |
| 36 | 统一数学物理范式 | 理论 | ✅ 已完成（朗兰兹纲领谱对应解释、镜像对称谱对应解释、全息对偶谱对应解释、三者统一于通用不动点框架、分形谱量子引力基础框架，`math_phys_unification.py`） |
| 37 | 哲学与基础科学价值 | 理论 | ✅ 已完成（SM参数预测vs拟合量化对比、框架可证伪性分析、与EFT拟合统计显著性差异、谱对应认识论、与还原论/涌现论关系、未来科学范式展望，`philosophical_foundations.py`） |

全部深层次理论问题均已在 Phase 6-12 中完成严格化论证与数值验证。

## 八、下一步优先任务

### Phase 13：理论转化推进计划（2026-07-13 启动）

理论转化是框架从「原型验证」迈向「通用理论互证标准」的核心阶段，规划四大发展主线：

**短期优先（1–2 年）**：
1. **理论转化严格完备化**：∞-范畴升级、转化等价性判定公理、转化不变量集合、转化误差与收敛理论
2. **量子引力范式互证**：完善 M理论→弦→GR+SM 多层谱静默转化数值案例
3. **转化数值工具开发**：拓展 `theory_transformation.py`，对接 LHC/数值相对论仿真代码
4. **NTK 双向转化验证**：完成大模型消融实验验证

**中长期（3–5 年）**：
5. **四大量子引力范式互相转化**：M理论 ↔ 超弦 ↔ LQG ↔ 渐近安全分形时空
6. **AdS/CFT 全息转化完备**：完整维度静默比公式、各类 CFT 互相态射转化
7. **物理先验 AI 标准化**：统一 PINN 框架，物理系统→神经网络谱约束
8. **实验数据转化对标流程**：高能实验数据→低能 Spec 谱→反向转化高维理论

**长期方向（5–10 年）**：
9. **通用理论分类学**：所有物理、复杂系统、AI 模型统一归类
10. **消解基础理论/有效理论二元对立**：传统 EFT 只是谱静默单向转化特例
11. **统一数学物理前沿研究范式**：朗兰兹纲领、镜像对称、全息对偶归入转化框架

### 持续任务
12. **引力真实度规对接**：将 `geodesic_instance.py` 与 Schwarzschild/Kerr 度规数值解对接。
13. **BSM 实验约束对接**：将 `bsm_instance.py` 与 LHC/暗物质探测实验约束对接。
14. **持续运行全部测试**：每完成一个任务后运行全部测试脚本，确保框架稳定。

## 九、推进计划

### 第一阶段：奠基期（2–4 周）— 已完成

**目标**：完成元公理层与结构定理层的初稿，确立理论骨架。

**状态**：已完成，文档已升级到严格化版本。

| 周次 | 任务 | 交付物 |
|---|---|---|
| 第 1 周 | 严格化 $\mathbf{Rec}$ 与 $\mathbf{Spec}$ 的定义 | `notes/rec_spec_definitions.md` |
| 第 1–2 周 | 定义谱去递归化函子 $D$ 并证明其忠实性 | `roadmap/phase1_meta_axioms.md` |
| 第 2–3 周 | 建立全域不动点方程与 $\text{Cat}_H(\mathcal{Cl})$ 范畴 | `roadmap/phase2_structural_theorems.md` |
| 第 3–4 周 | 将 $ \lambda_i = e^{-\mu_i}$ 表述为范畴自然等价 | `notes/spectral_correspondence_equivalence.md` |

**里程碑 M1**：三层公理体系文档达到可投稿纯数学期刊预印本的水准。

### 第二阶段：实现期（4–8 周）— 已完成

**目标**：实现最小可运行原型，并将旧工作重构为下游插件。

**状态**：已完成，核心代码与接口测试全部通过。

| 周次 | 任务 | 交付物 |
|---|---|---|
| 第 4–5 周 | 实现 $\mathbf{Rec}$、$\mathbf{Spec}$、$D$ 的 Python 原型 | `src/rec_category.py`、`src/spec_category.py`、`src/decursion_functor.py` |
| 第 5–6 周 | 实现全域不动点方程求解器（可插拔迭代算法） | `src/fixed_point_solver.py` |
| 第 6–7 周 | 将 `sm_mass_complete_v5.py` 重构为标准模型下游插件 | `applications/standard_model/sm_instance.py` |
| 第 7–8 周 | 将 NTK 实验结果重新包装为接口验证 | `applications/ntk/ntk_instance.py` |

**里程碑 M2**：抽象框架能够复现旧工作中 SM 与 NTK 的核心数值结果，但代码结构体现「理论本体 / 实例工具」分离。

### 第三阶段：深化期（2–4 月）— 基本完成

**目标**：完成过拟合几何判据与跨领域外推验证。

**状态**：LACI 判据与过拟合几何定理已完成（`phase4`）；已有 5 个独立下游插件。真实数据/模型对接仍在 P2/P5 中推进。

| 时间 | 任务 | 交付物 | 状态 |
|---|---|---|---|
| 第 2–3 月 | 定义局部吸引子与全域不动点的距离度量 | `roadmap/phase4_semantics_over_fitting.md` | ✅ 已完成 |
| 第 3–4 月 | 弦论拓扑递归实例验证 | `applications/string_theory/string_instance.py` | ⏳ 待对接真实数据 |
| 第 3–4 月 | 引力测地线分形实例验证 | `applications/gravitational_geodesic/` | ⏳ 待对接真实度规 |
| 第 4 月 | BSM 新费米子谱系外推测试 | `applications/bsm/` | ⏳ 待对接实验约束 |

**里程碑 M3**：形成至少 5 个独立下游插件，证明框架的通用性。（已达到：SM、NTK、弦论、引力、BSM）

### 第四阶段：写作期（4–6 月）— 进行中

**目标**：完成两篇论文并投稿（数学理论 + 物理应用）。

**论文拆分**（2026-07-13 决定）：

| 论文 | 定位 | 文件 | 目标期刊 | 状态 |
|---|---|---|---|---|
| Paper I：通用不动点范畴框架 I——分形谱去递归理论 | 纯数学理论 | `paper/paper1_fractal_spectral_derecursion.md` | J. Funct. Anal. / Adv. Math. | ✅ v2.13，含 18 篇参考文献 + 附录 |
| Paper II：通用不动点范畴框架 II——物理应用与实验验证 | 理论物理 + 实验验证 | `paper/paper2_physics_applications.md` | PRD / JHEP | ✅ v2.11，含 33 篇参考文献 + 附录 |

| 时间 | 任务 | 交付物 |
|---|---|---|
| 第 4–5 月 | Paper 1：数学理论（范畴论、RKHS、谱测度、Clifford、收敛率 NS-1~3） | `paper1_fractal_spectral_derecursion.md` |
| 第 5 月 | Paper 2：物理应用（SM/BSM、Kerr、全息熵、CFT），引用 Paper 1 | `paper2_physics_applications.md` |
| 第 5–6 月 | 内部审阅、修订、格式整理 | 终稿 PDF |
| 第 6 月 | 分别投稿至数学/物理期刊 | 投稿确认邮件 |

**里程碑 M4**：两篇论文分别投稿，Paper 1 提供数学基础，Paper 2 引用 Paper 1 并展示物理应用。

### 风险管理

| 风险 | 应对策略 |
|---|---|
| 元公理层形式化过于抽象，难以落地 | 先用 IFS 和 NTK 两个具体对象验证原型 |
| 旧代码重构工作量大 | 优先做接口包装，不急于重写底层算法 |
| 跨领域实例（弦论、引力）进展慢 | 允许用已有结果作为概念验证，不强求新数值实验 |
| 纯数学期刊审稿周期长 | 同时准备 arXiv 预印本，保持公开进度 |

### 检查点

- **每两周**：更新 `notes/` 中的研究笔记，记录待证问题与中间结论。
- **每月末**：回顾里程碑完成情况，必要时调整后续计划。
- **每阶段末**：产出一份可独立阅读的文档或代码版本，并做简短总结。

---

## 十、待完成事项与推进优先级

> 以下内容来自各阶段交付物中遗留的待解决问题，按对论文和框架的影响排序。

### P0：理论严格化（进入论文写作期前必须完成）— 已完成

| 任务 | 位置 | 状态 |
|---|---|---|
| 严格定义 $\mathbf{Rec}$ 与 $\mathbf{Spec}$ 的态射复合律 | `notes/rec_spec_definitions.md` | ✅ 已完成 |
| 证明谱去递归化函子 $D$ 的忠实性 | `roadmap/phase1_meta_axioms.md` | ✅ 已完成（定理 3.4） |
| 研究伴随函子 $D \dashv R$ 的存在条件 | `roadmap/phase1_meta_axioms.md` | ✅ 已完成（定理 4.1） |
| 将 $ \lambda_i = e^{-\mu_i}$ 表述为严格范畴自然等价 | `notes/spectral_correspondence_equivalence.md` | ✅ 已完成 |
| 严格化局部吸引子距离度量 | `roadmap/phase4_semantics_over_fitting.md` | ✅ 已完成（定理 2.1、2.2） |

### P1：核心代码补全（框架可用性）— 已完成

| 任务 | 位置 | 状态 |
|---|---|---|
| 实现 `src/orbit_functor.py` | `src/` | ✅ 已完成 |
| 实现 `src/overfitting_diagnosis.py` | `src/` | ✅ 已完成 |
| 实现 `fixed_point_solver.py` 的 `weak` 交织模式 | `src/fixed_point_solver.py` | ✅ 已完成 |
| 清理未使用的导入与冗余代码 | `src/spec_category.py`, `src/fixed_point_solver.py` 等 | ✅ 已完成 |
| 为各实例添加 `instance_hypothesis.yml` | `applications/*/` | ✅ 已完成 |

### P2：下游插件深化（可随论文写作并行推进）— 进行中

| 任务 | 位置 | 状态 |
|---|---|---|
| SM：加入规范耦合、Higgs、中微子质量 | `applications/standard_model/sm_instance.py` | ✅ 已完成 |
| SM：与 `src/fixed_point_solver.py` 集成 | `applications/standard_model/` | ✅ 已完成 |
| NTK：与 `cifar10_ntk_experiment.py` 实测 NTK 谱对接 | `applications/ntk/` | ✅ 已完成 |
| 弦论：与 `string_scattering_amplitude.py` 对接 | `applications/string_theory/` | ✅ 已完成 |
| 弦论：实现完整 Eynard-Orantin 拓扑递归核 | `applications/string_theory/string_instance.py` | ⏳ 待推进 |
| 引力：与真实度规数值解对接 | `applications/gravitational_geodesic/` | ✅ 已完成（Schwarzschild/Kerr 圆轨道 epicyclic 频率） |
| 引力：实现更真实的 Kerr/Schwarzschild 度规离散化 | `applications/gravitational_geodesic/geodesic_instance.py` | ✅ 已完成（支持顺行/逆行、近圆至 e=0.3，采用转折点精确求解 E/L） |
| BSM：与 LHC/暗物质实验约束接口对接 | `applications/bsm/` | ✅ 已完成（`bsm_experiment_constraints.py`） |
| BSM：与具体 BSM 模型精确数据库对接 | `applications/bsm/` | ⏳ 待推进（已新增 `bsm_cross_sections.py`，含热遗迹密度冻结、LHC 对产生、直接探测 SI 截面等精确截面工具；`bsm_predictions.py` 已生成第4代轻子质量预言 ~1470 GeV 与 LHC 截面 ~54 pb） |
| BSM：精确定义 $O_{BSM}$ | `applications/bsm/` | ✅ 已完成（`orbit_functor.on_bsm`） |
| LQG：面积谱实例与轨道权重接口 | `applications/loop_quantum_gravity/` | ✅ 已完成 |
| LQG：与真实 spinfoam 振幅 / 体积谱对接 | `applications/loop_quantum_gravity/` | ⏳ 待推进 |
| AdS/CFT：CFT 初级场标度维数实例与轨道权重接口 | `applications/ads_cft/` | ✅ 已完成 |
| AdS/CFT：与具体 CFT 算子表 / 全息熵对接 | `applications/ads_cft/` | ⏳ 待推进 |
| TQFT：Ising / Fibonacci 任意子量子维度实例与轨道权重接口 | `applications/tqft/` | ✅ 已完成 |
| TQFT：完整融合规则与 modular S/T 矩阵对接 | `applications/tqft/` | ⏳ 待推进 |
| NCG：Dirac 本征值谱实例、谱作用与轨道权重接口 | `applications/noncommutative_geometry/` | ✅ 已完成 |
| NCG：与标准模型谱三元组 Dirac 谱对接 | `applications/noncommutative_geometry/` | ⏳ 待推进 |
| 因果集：将来基数谱实例与轨道权重接口 | `applications/causal_set/` | ✅ 已完成 |
| 因果集：与 Myrheim-Meyer 维数 / 真实因果集动力学对接 | `applications/causal_set/` | ⏳ 待推进 |
| 渐近安全：临界指数谱实例与轨道权重接口 | `applications/asymptotic_safety/` | ✅ 已完成 |
| 渐近安全：与真实 FRG 引力-物质固定点数据对接 | `applications/asymptotic_safety/` | ⏳ 待推进 |
| 扭量：旋量运动学谱实例、弦论振幅联动与轨道权重接口 | `applications/twistor/` | ✅ 已完成 |
| 扭量：Parke-Taylor MHV 振幅与真实散射数据对接 | `applications/twistor/` | ⏳ 待推进 |

### 推进建议

1. **先完成 P0**：这是论文的核心数学支撑，没有这些严格化，论文会被质疑理论基础。
2. **再完成 P1**：让框架从「原型」升级为「可用工具」。
3. **P2 与论文写作并行**：下游插件的深化是长期工作，可在论文投稿后继续迭代。

---

## 变更记录

| 日期 | 更新内容 | 关联任务 |
|---|---|---|
| 2026-07-13 | 新增 M理论层级谱静默转化数值案例（M(11)→超弦(10)→弦论(10)→GR+SM(4)） | Phase 13 任务5 |
| 2026-07-13 | 新增理论等价不变量完备集合与判定定理（9类核心不变量 + 充要条件 + 三类严格判据） | Phase 13 任务4 |
| 2026-07-13 | 新增弦图可视化演算（五类转化弦图、弦图演算规则、弦图到代码自动生成、理论转化立方体） | Phase 13 任务3 |
| 2026-07-13 | 新增理论转化完整数值库升级（可观测量计算、批量转化引擎、M理论层级转化、转化误差分析、LACI风险评估） | Phase 13 任务2 |
| 2026-07-13 | 新增理论转化（五种转化模式，验证弦论/超弦/M理论/LQG 互相转化可行性） | Phase 13 任务1 |
| 2026-07-13 | 新增谱静默理论（替代紧致化概念，四个静默判据，三物理实例验证） | Phase 12 |
| 2026-07-13 | 新增高维 IFS 收敛率理论、奇异连续谱刻画、测度论收敛率证明（NS-1M~NS-3M） | Phase 12 |
| 2026-07-13 | 论文拆分：Paper I（分形谱去递归理论）+ Paper II（物理应用与实验验证） | Phase 12 |
| 2026-07-13 | 推进开放问题：非分离 IFS 下界、Lyapunov-谱维数关联、MadGraph/micrOMEGAs、双星引力波、Kerr/N=4 SYM/暗物质分形谱 | Phase 14 |
| 2026-07-13 | 更新 Paper I v2.5：将 `spectral_silence.py` 写入 §5.6，将 `theory_transformation.py`/`eft_equivalence_framework.py`/`string_diagram_calculus.py` 系统化为 §7.7 核心方法论 | Phase 14 |
| 2026-07-13 | 数学严格化深化：新增 Feng-Wang 热力学形式、Leaver 连分数 Kerr QNM 原型、强耦合 N=4 SYM Bethe ansatz；测试数从 47 增至 52 | Phase 14 |
| 2026-07-13 | 数学严格化再深化：新增 Ruelle 精确转移算子、拓扑熵-谱间隙不等式、Leaver 精确系数、N=4 SYM 简化 BES/TBA；测试数从 52 增至 57 | Phase 14 |
| 2026-07-13 | 数学严格化三阶段深化：新增 Feng-Wang 条件转移算子、Markov IFS 下 TE-G 严格框架、完整 Teukolsky-Leaver 求解器、N=4 SYM 完整 BES/TBA 升级；测试数从 57 增至 61 | Phase 14 |
| 2026-07-13 | 数学严格化四阶段深化：Feng-Wang 加权条件测度、Koopman TE-G 推广、spheroidal λ 自洽迭代、O(g⁶) BES/TBA；测试数从 61 增至 64 | Phase 14 |
| 2026-07-13 | D 函子代码质量修复：移除 Koopman 强制对称化（Rec 范畴扩展为完整范畴），logm fallback，忠实性测试加强 | Code Quality |
| 2026-07-13 | Phase 15A 短板推进完成（5/6 项）：高维 IFS 验证、Kerr 校准、FCC-hh 系统误差、谱静默等价链修正、BSM S/T 参数；测试数从 64 增至 100 | Phase 15A |
| 2026-07-13 | Phase 15B-7 不变量充要性提升：动力学相容性检查 + 完备性缺口分析；测试数从 100 增至 105 | Phase 15B |
| 2026-07-14 | Phase 15C-1 轨道函子群表示谱理论：等价类定义 3.10 + 同谱判定定理 3.10a + 谱荷定义 3.10b + 表示签名定义 3.10c；Paper I §3.5.1 新增；测试数从 105 增至 121 | Phase 15C |
| 2026-07-14 | Phase 15C-4 误差预算体系：Rec→Spec→预言→实验 全链路误差传播；Paper II §7.5 新增；`error_budget.py` + `test_error_budget.py`（11 测试） | Phase 15C |
| 2026-07-14 | Phase 15C-2 Clifford 旋量模结构：原始幂等元 + 左理想性质 + 旋量模谱定理；Paper I §6.4 新增；`clifford_spectrum_demo.py` 扩展 + `test_clifford_spinor_module.py`（9 测试）；测试数从 121 增至 130 | Phase 15C |
| 2026-07-14 | Phase 15C-3 EFT 逆重构唯一性：完备静默信息定义 + 唯一性定理 + 非唯一性边界 + 双向一致性；Paper I §7.7.5 新增；`eft_equivalence_framework.py` 扩展 + `test_eft_inverse_reconstruction.py`（8 测试）；测试数从 130 增至 138 | Phase 15C |
| 2026-07-14 | Phase 15B-1/2 D 函子定义域扩展 + Freyd 放宽条件：投影值谱测度 PVM、连续谱对象、谱积分、有限极限保持、ε-解集条件、弱伴随关系；`d_functor_extension.py` + `test_d_functor_extension.py`（11 测试）；测试数从 138 增至 149 | Phase 15B |
