# 研究笔记 / Research Notes

本目录存放抽象化改造过程中的中间推导、问题记录与待证命题。

## 已完成问题（已严格化并进入论文/代码）

| 问题 | 状态 | 位置 |
|---|---|---|
| $\mathbf{Rec}$ 的严格定义（复合律、单位律、结合律） | ✅ 已完成 | `roadmap/phase1_meta_axioms.md`、`src/rec_category.py` |
| $D$ 的忠实性证明 | ✅ 已完成 | `roadmap/phase1_meta_axioms.md` 定理 3.4 |
| 伴随函子 $D \dashv R$ 离散原型 | ✅ 已完成 | `src/decursion_functor.py`、`src/test_decursion_functor.py` |
| 谱对应 $ \lambda_i = e^{-\mu_i}$ 的范畴自然同构 | ✅ 已完成 | `notes/00_foundations/spectral_correspondence_equivalence.md`、`src/spectral_correspondence.py` |
| 局部吸引子距离度量（LACI） | ✅ 已完成 | `roadmap/phase4_semantics_over_fitting.md`、`src/attractor_distance.py` |
| **零参数质量预测（Spec 4-范畴静默层级→全部SM参数）** | ✅ **已完成，29项已验证** | `notes/01_qcd_higgs/spectral_root_cause_analysis.md`、`paper/paper17_zero_parameter_predictions.md` |
| **CKM 五参数第一性推导** | ✅ 已完成 | `notes/02_ckm_pmns_flavor/spectral_ckm_angles.md` |
| **PMNS 四参数第一性推导（含 δ_CP）** | ✅ 已完成 | `notes/02_ckm_pmns_flavor/spectral_ckm_angles.md` |
| **强 CP 谱解** | ✅ 已完成 | `notes/01_qcd_higgs/spectral_strong_CP.md` |
| **全 29 参数验证 + ε_K 交叉检验** | ✅ **29/29 已验证** | `scripts/paperX_all_predictions.py` |
| **d_H 结构分析与机器验证** | ✅ **Paper 30 v1.1** （11 项 Lean 证明 + 2 项数值验证） | `notes/08_first_principles/spectral_hierarchy_evolution_analysis.md`、`paper/paper30_dH_structural_analysis.md` |
| **B2 连续极限（分形→光滑时空）** | ✅ **理论闭合（Paper XXXIV v1.2）** — 6/6 子步骤 | `notes/08_first_principles/b2_continuum_limit_analysis.md`、`paper/paper34_continuum_limit.md` |
| **ContinuumLimit.lean 形式化** | ✅ $c_1 < S_4$ 机器证明，`depthLayering` 完整证明链；**hDiamLeOne 闭合（2026-08-04，O9）**——吸引子 ⊆ [0,1] 与 diam ≤ 1 机器证明 | `formal_proof/UFPFormalization/UFPFormalization/ContinuumLimit.lean` |
| **假设-演绎论证方法论** | ✅ **已确立（2026-08-04）** — 三层级论证强度（①预测检验 ②框架自洽 ③先验导出）+ A_GR 谱假设定位 + 非循环性判据；提炼于 Paper XXXVII §4.4 与勘误 §一·补充 | `notes/00_foundations/spectral_hypothesis_deductive_methodology.md`、`paper/paper37_open_problems.md` |
| **引力范畴论起源** | ✅ **Paper XXXV v0.2** — 交换律偏差 = 引力 | `notes/08_first_principles/04_gravity_analysis.md`、`paper/paper35_gravity_origin.md` |
| **开放问题系统综述** | ✅ **Paper XXXVII v0.1** — A/B/C 三组分类 + 层次距离 + Bott-Moran 桥 | `notes/08_first_principles/05_hierarchy_distance.md`、`notes/08_first_principles/spectral_hierarchy_evolution_analysis.md`、`paper/paper37_open_problems.md` |
| **p-value 统计分析** | ✅ **Fisher p≈0** | `scripts/paperX_pvalue_analysis.py` |
| **根因分析** | ✅ 已完成 | `notes/01_qcd_higgs/spectral_root_cause_analysis.md` |
| **框架完整推导综述** | ✅ 已完成 | `notes/00_foundations/spectral_comprehensive_review.md` |
| **独有实验预言汇总** | ✅ 已完成 | `notes/09_experimental/spectral_unique_predictions.md` |
| **跨领域谱对应——复杂系统** | ✅ → **Paper XIII** | `paper/paper13_spectral_complex_systems.md` |
| **凝聚态物理谱表述** | ✅ → **Paper XIV** | `paper/paper14_spectral_condensed_matter.md` |
| **量子化学谱表述** | ✅ → **Paper XV** | `paper/paper15_spectral_quantum_chemistry.md` |
| **光伏效率谱增强** | 🟢 研究笔记 v0.2 | `notes/06_quantum_chem_pv/spectral_photovoltaics.md` |
| **开放数据验证报告** | ✅ 已完成 | `notes/07_validation/open_data_validation_report.md` |
| **OPV2D 大规模验证** | ✅ 5/5 通过（38,849 D-A 对） | `src/opv_validation_extended.py` |
| **QCD 谱框架验证** | ✅ 偏差 < 3% | `src/qcd_spectral_validation.py` |
| **MgB₂ 超导隙比验证** | ✅ 6 组独立实验 | `src/mgb2_gap_ratio_validation.py` |
| **BSM 实验验证** | ✅ Planck/LHC/XENONnT/LZ | `src/bsm_experiment_validation.py` |
| **S₁→S₂ 方案转换因子 Z_i** | 🟡 框架建立 | `notes/10_gauge_RG/spectral_Zi_scheme_conversion.md` |
| **超荷 Y 的 Cl(1,7) 代数推导** | ✅ 已完成 | `notes/00_foundations/spectral_hypercharge_derivation.md` |
| **See-saw 谱算子推导** | ✅ 已完成 | `notes/03_neutrino/spectral_see_saw_operator.md` |
| **多重静默通用方法论** | ✅ 已完成 | `notes/11_transition_bridges/spectral_multi_silence_methodology.md` |
| **Kerr QNM 多重静默分析** | ✅ 已完成 | `notes/04_lorentz_gravity/spectral_Kerr_silence_analysis.md` |
| **Higgs VEV 多重静默分析** | ✅ 已完成 | `notes/01_qcd_higgs/spectral_Higgs_silence_analysis.md` |
| **中微子质量层级多重静默分析** | ✅ 已完成 | `notes/03_neutrino/spectral_neutrino_hierarchy_silence.md` |
| **暗物质遗迹密度多重静默分析** | ✅ 已完成 | `notes/04_lorentz_gravity/spectral_dark_matter_silence.md` |
| **表示静默（D-静默）S0 层** | ✅ 研究笔记 v0.1（交叉校验发现：SpImD 态射层基数反例 → 静默度同构推广） | `notes/00_foundations/spectral_representation_silence.md` |
| **页岩油气成藏谱流（应用推演）** | 🟢 研究笔记 v0.1（跨领域探索：多孔介质多相流 + 微型圈闭集合的谱流/谱隙/静默重构，预测分级 A/B/C，待数据标定） | `notes/05_condensed_matter/spectral_shale_accumulation.md` |

See `notes/00_foundations/spectral_comprehensive_review.md` for a self-contained derivation chain from first principles to all 29 SM parameters.

**笔记→论文覆盖率：57/57（100%），详见 `notes/07_validation/notes_to_papers_audit.md`。**
**多重静默理论笔记：8 篇，详见 `notes/01_qcd_higgs/spectral_root_cause_analysis.md`。**
**Phase 61 物理方向笔记（2026-08-03/04）**：`notes/05_cosmology/spectral_inflation_dynamics.md`（61A 暴涨）、`notes/01_qcd_higgs/spectral_color_dynamics.md`（61B 色规范）、`notes/00_foundations/spectral_renormalization_chain.md`（61C 重整化链）、`notes/04_lorentz_gravity/spectral_black_hole_evolution_formalization.md`（61D 黑洞演化）——均对应论文 `paper39-42`，全部达到完成判据（Lean/Agda 双语言 + 数值验证）。

## 当前重点问题（开放问题推进中）

1. **B2 3b/3d/3e/3f Lean 形式化**：B2 连续极限理论已闭合，形式化受限于 mathlib 基础设施（拟共形几何库、拓扑学库尚未完善）
2. **B3 暗能量 $\Lambda$**：$\Delta_{\text{global}}$ 的形式化——数值拟合通道已关闭，真瓶颈为机制缺失
3. **O3 $d_H$ 出路 A/B**：构造已完成，待循环闭合
4. **规范引力混合修正（Paper XII §9.3 β₃^(spec)）**：三圈 β 函数中的规范-引力混合项可使 M_Pl 处耦合偏移 ~5-15%
5. **GUT 能标门限修正**：在 M_GUT ∼ 2×10¹⁶ GeV 处若存在新物理（seesaw 中微子质量），引入额外态射通道改变 β 系数
6. **Kerr m≠0 Leaver 求解器收敛**：角向求解已收敛，径向 Leaver 系数约定需调试
7. **谱方案 → MS-bar 方案转换因子 Z_i**：S₂ 层 DS 减除对易子框架已建立，Z_i 的显式解析公式待推导
8. **暗物质 α_DM 的第一原理推导**：谱静默粒子在 A_GR 谱结构中的精确范畴维数
9. **Phase 63 元定理完备性**：四体制分类（A/B1/B2/C）的五盲区分析与体制间态理论推进（详见下方）

## Phase 63：元定理完备性与体制间态（2026-08-23）

**状态**：第一阶段（Lean 形式化闭合）已完成，第二阶段（体制间态理论深化）进行中

**核心成果**：
- 四体制元定理（A/B1/B2/C）的五盲区系统性分析
- 体制间态（Inter-Regime State）形式化定义（Drinfeld 联结子形变）
- Gödel-Koopman 算子构造（不可判定命题的算子实现）
- 平展统一猜想（Flattening Unification Conjecture）
- 谱静默不覆盖盲区 1 的 Lean 反例验证
- **Lean 形式化全面闭合**（2026-08-24 审计：101 个 .lean 文件零 sorry）

**关键文档**：
| 文档 | 位置 | 内容 |
|:----|:----|:----|
| 元定理完备性讨论 | `00_foundations/meta_theorem_completeness_discussion_2026-08-23.md` | 五盲区分析、四体制一般形式 |
| 五盲区物理对应表 | `00_foundations/blind_spot_physical_system_mapping_2026-08-23.md` | 盲区 1-5 的物理系统对应 |
| 体制间态定义 | `00_foundations/inter_regime_state_definition_2026-08-23.md` | Drinfeld 联结子形变推导 |
| Gödel 算子 | `00_foundations/godel_operator_spectral_silence_2026-08-23.md` | Gödel-Koopman 算子与谱静默截面 |
| 平展统一猜想 | `00_foundations/flattening_unification_conjecture_2026-08-23.md` | N-平展、静默比、覆盖完备性 |
| θ-C 独立性分析 | `00_foundations/spectral_theta_C_independence_analysis_2026-08-24.md` | 理论独立性与数值矛盾分析 |
| 进展报告 | `12_phase_results/phase63_meta_theorem_progress_2026-08-24.md` | Lean 审计结果、推进重点 |
| 推进路线图 | `roadmap/phase63_meta_theorem_open_problems.md` | 四阶段推进计划、开放问题清单 |

**开放问题（Phase 63 路线图）**：
- C1: ε_hex 在无穷维中的计算方法（有限维截断逼近）
- D1: θ-C 独立性理论解释（数值 r=-0.53 矛盾）
- C2-C4: 体制间态拓扑分类、谱静默关系、临界体制边界
- B2-B5: 盲区 2-5 形式化推进（长期）

## 重要公告：框架更名计划（2026-08-24）

**UFPF → MUFPF 更名计划**

由于当前框架名称 **UFPF**（Universal Fixed Point Framework）与 IEEE 生物图像识别框架（Universal Feature Perception Framework, UFPF）在国际英文检索上存在严重冲突，导致学术流量被彻底分流，现启动更名计划。

**新名称**：**MUFPF**（Meta-Universal Fixed-Point Functorial Framework）
- 中文名称：元通用不动点函子范畴框架
- 读音：Mee-U-F-P-F

**更名原因**：
1. 解决命名冲突，确保学术检索唯一性
2. 理论内涵升级：Meta（元数学）、Functorial（函子范畴论）
3. 匹配 Lean 4 形式化验证的学术高度

**更名范围**：约 265 个文件，845+ 处引用
**预计时间**：8 周（分四阶段实施）

**详细计划**：`roadmap/mu_renaming_plan.md`

---

## 文件命名约定

- `YYYYMMDD_topic.md`：按日期记录的研究笔记。

## 结构化目录（2026-07-22 整理）

所有旧文件已归档至 `99_archive/old_flat/`。以下子目录为正式存放位置，交叉引用已同步修复。

| 目录 | 文件数 | 说明 |
|:----|:-----:|:-----|
| `00_foundations/` | 49 | 范畴基础、谱对应、形式化、路径积分、Feynman 规则、∞-范畴预研、术语治理 |
| `01_qcd_higgs/` | 21 | QCD、Higgs、手征对称性、强 CP |
| `02_ckm_pmns_flavor/` | 14 | CKM、PMNS、Yukawa、味道物理 |
| `02_superconductivity/` | 5 | 超导、BCS 编织、迈斯纳、量子 Hall 拓扑 |
| `03_condensed_fluid/` | 1 | 凝聚流体谱纤维化 |
| `03_neutrino/` | 4 | 中微子质量、Seesaw、层级 |
| `04_lorentz_gravity/` | 63 | Lorentz 谱流、引力、Kerr、暴涨、力/质量/静默方向/总账、Leaver 连分数、LACI、谱丛、双星动力学 |
| `05_condensed_matter/` | 15 | 凝聚态、超导、临界现象、流变学、页岩成藏谱流 |
| `05_cosmology/` | 2 | 暴涨动力学、宇宙学谱纤维化 |
| `06_photon_topology/` | 3 | 光子拓扑、第一性原理起源、未知粒子 X |
| `06_quantum_chem_pv/` | 13 | 量子化学、光伏、纤维化方法 |
| `07_validation/` | 5 | 开放数据验证报告 |
| `08_first_principles/` | 15 | 第一性原理推导、力统一、B2 连续极限 |
| `09_experimental/` | 4 | 实验提案、独有预言 |
| `10_gauge_RG/` | 13 | 规范理论、重整化群、方案转换 |
| `11_transition_bridges/` | 6 | 范畴-表示桥接（Phase 53）+ 融合路径 |
| `12_phase_results/` | 3 | 阶段结果汇总 |
| `99_archive/` | 7 | 已完成/合并到论文的旧笔记 |

完整映射关系见：[STRUCTURE_MAPPING.md](STRUCTURE_MAPPING.md)

## 直觉/诠释与治理笔记备案（2026-08-16 增补）

| 笔记 | 状态 | 位置 |
|:--|:--|:--|
| 力 = 偏转时间轴的驱动（力笔记，v0.25） | 🟡 直觉/诠释 + §4 [推导] 混合 | `04_lorentz_gravity/force_essence_deflection.md` |
| 质量 = 偏转时间轴的难度（质量笔记，v0.26，含 T 纲领 CONJECTURE 与 §7.0a 讨论共识） | 🟡 直觉/诠释 | `04_lorentz_gravity/mass_time_deflection_intuition.md` |
| 未闭合项总账（治理登记，含 §3 静默方向条目研究历程） | 🟡 治理登记 | `04_lorentz_gravity/force_open_items_ledger.md` |
| 静默方向到法向/耦合自由度分配机制（v0.18，含 §8 研究历程日志） | 🟢 推导推进 + 机器证明骨架 | `04_lorentz_gravity/silence_direction_allocation.md` |
| 自然单位制 ħ=1 规范固定（v0.24 配套） | 🟢 推导 | `04_lorentz_gravity/natural_unit_gauge_fixing.md` |
| LACI 公理化（定理 T1–T3，v0.2，2026-08-16 语义反转修正） | 🟢 定理系 | `04_lorentz_gravity/laci_axiomatization.md` |
| LACI 跨域推广（流变学等） | 🟢 推广 | `04_lorentz_gravity/laci_cross_domain_generalization.md` |
| LACI 高泛音验证 | 🟢 验证 | `04_lorentz_gravity/laci_high_overtone_validation.md` |
| LACI 谱丛解释（谱叶追踪） | 🟢 谱丛几何 | `04_lorentz_gravity/spectral_sheaf_leaver.md` |
| 融合路径 4（Wigner 谱桥接） | 🟢 桥接 | `11_transition_bridges/fusion_path4_wigner_spectral_bridge.md` |

**谱丛/Leaver/LACI 笔记群**（2026-08-16 自根目录归入 `04_lorentz_gravity/`）：`leaver_*`/`laci_*`/`spectral_sheaf_*`/`dynamic_*`/`dual_homotopy_convergence` 共 34 篇——Kerr 谱丛、Leaver 连分数、动态双星波形、LACI 系列研究线，与 paper27/26 配套；∞-范畴预研/谱纤维化/术语治理 3 篇归入 `00_foundations/`。根目录现仅存索引文件（README、STRUCTURE_MAPPING）。

## 教学辅助文档

| 文档 | 说明 |
|:----|:----|
| `08_first_principles/spectral_dynamics_high_school_physics.md` | 谱动力学视角下的初高中物理知识 |

## 第一性推导

| 文档 | 说明 |
|:----|:----|
| `08_first_principles/spectral_dynamics_first_principles_derivation.md` | 从谱动力学第一原理推导牛顿力学 |

## 相关索引

- 路线图：`roadmap/phase14_open_problems_advancement.md`
- 论文 I 开放问题：`paper/paper1_fractal_spectral_derecursion.md` §8.2
- 论文 II 开放问题：`paper/paper2_physics_applications.md` §8.2
- 代码实现：`src/math_open_problems_advanced.py`、`src/numerical_engineering_open_problems.py`、`src/physics_open_problems_advanced.py`
