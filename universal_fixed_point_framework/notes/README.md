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
| **全 29 参数验证 + ε_K 交叉检验** | ✅ **29/29 已验证** | `paperX_all_predictions.py` |
| **d_H 结构分析与机器验证** | ✅ **Paper 30 v1.1** （11 项 Lean 证明 + 2 项数值验证） | `notes/08_first_principles/spectral_hierarchy_evolution_analysis.md`、`paper/paper30_dH_structural_analysis.md` |
| **p-value 统计分析** | ✅ **Fisher p≈0** | `paperX_pvalue_analysis.py` |
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

See `notes/00_foundations/spectral_comprehensive_review.md` for a self-contained derivation chain from first principles to all 29 SM parameters.

**笔记→论文覆盖率：57/57（100%），详见 `notes/07_validation/notes_to_papers_audit.md`。**
**多重静默理论笔记：8 篇，详见 `notes/01_qcd_higgs/spectral_root_cause_analysis.md`。**

## 当前重点问题（开放问题推进中）

1. **规范引力混合修正（Paper XII §9.3 β₃^(spec)）**：三圈 β 函数中的规范-引力混合项可使 M_Pl 处耦合偏移 ~5-15%；见 `src/spectral_rge_running.py`、`notes/01_qcd_higgs/spectral_root_cause_analysis.md` §4a。
2. **GUT 能标门限修正**：在 M_GUT ∼ 2×10¹⁶ GeV 处若存在新物理（seesaw 中微子质量），引入额外态射通道改变 β 系数。
3. **Kerr m≠0 Leaver 求解器收敛**：角向求解已收敛，径向 Leaver 系数约定需调试；见 `src/kerr_s2_guided_solver.py`、`notes/04_lorentz_gravity/spectral_Kerr_silence_analysis.md`。
4. **谱方案 → MS-bar 方案转换因子 Z_i**：S₂ 层 DS 减除对易子框架已建立，Z_i 的显式解析公式待推导；见 `notes/10_gauge_RG/spectral_Zi_scheme_conversion.md`。
5. **暗物质 α_DM 的第一原理推导**：谱静默粒子在 A_GR 谱结构中的精确范畴维数；见 `notes/04_lorentz_gravity/spectral_dark_matter_silence.md`。

## 文件命名约定

- `YYYYMMDD_topic.md`：按日期记录的研究笔记。

## 结构化目录（2026-07-22 整理）

所有旧文件已归档至 `99_archive/old_flat/`。以下子目录为正式存放位置，交叉引用已同步修复。

| 目录 | 文件数 | 说明 |
|:----|:-----:|:-----|
| `00_foundations/` | 19 | 范畴基础、谱对应、形式化、路径积分、Feynman 规则 |
| `01_qcd_higgs/` | 9 | QCD、Higgs、手征对称性、强 CP |
| `02_ckm_pmns_flavor/` | 14 | CKM、PMNS、Yukawa、味道物理 |
| `03_neutrino/` | 4 | 中微子质量、Seesaw、层级 |
| `04_lorentz_gravity/` | 20 | Lorentz 谱流、引力、Kerr、暴涨 |
| `05_condensed_matter/` | 10 | 凝聚态、超导、临界现象、流变学 |
| `06_quantum_chem_pv/` | 2 | 量子化学、光伏 |
| `07_validation/` | 4 | 开放数据验证报告 |
| `08_first_principles/` | 3 | 第一性原理推导、力统一 |
| `09_experimental/` | 4 | 实验提案、独有预言 |
| `10_gauge_RG/` | 13 | 规范理论、重整化群、方案转换 |
| `11_transition_bridges/` | 5 | 范畴-表示桥接（Phase 53） |
| `12_phase_results/` | 3 | 阶段结果汇总 |
| `99_archive/` | 10 | 已完成/合并到论文的旧笔记 |

完整映射关系见：[STRUCTURE_MAPPING.md](STRUCTURE_MAPPING.md)

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
