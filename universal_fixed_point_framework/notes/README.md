# 研究笔记 / Research Notes

本目录存放抽象化改造过程中的中间推导、问题记录与待证命题。

## 已完成问题（已严格化并进入论文/代码）

| 问题 | 状态 | 位置 |
|---|---|---|
| $\mathbf{Rec}$ 的严格定义（复合律、单位律、结合律） | ✅ 已完成 | `roadmap/phase1_meta_axioms.md`、`src/rec_category.py` |
| $D$ 的忠实性证明 | ✅ 已完成 | `roadmap/phase1_meta_axioms.md` 定理 3.4 |
| 伴随函子 $D \dashv R$ 离散原型 | ✅ 已完成 | `src/decursion_functor.py`、`src/test_decursion_functor.py` |
| 谱对应 $ \lambda_i = e^{-\mu_i}$ 的范畴自然等价 | ✅ 已完成 | `notes/spectral_correspondence_equivalence.md`、`src/spectral_correspondence.py` |
| 局部吸引子距离度量（LACI） | ✅ 已完成 | `roadmap/phase4_semantics_over_fitting.md`、`src/attractor_distance.py` |
| **零参数质量预测（Spec 4-范畴静默层级→全部SM参数）** | ✅ **已完成，24项已验证** | `notes/spectral_root_cause_analysis.md`、`paper/paper17_zero_parameter_predictions.md` |
| **CKM 五参数第一性推导** | ✅ 已完成 | `notes/spectral_ckm_angles.md` |
| **PMNS 四参数第一性推导（含 δ_CP）** | ✅ 已完成 | `notes/spectral_ckm_angles.md` |
| **强 CP 谱解** | ✅ 已完成 | `notes/spectral_strong_CP.md` |
| **全 24 参数验证 + ε_K 交叉检验** | ✅ **24/24 已验证** | `paperX_all_predictions.py` |
| **p-value 统计分析** | ✅ **Fisher p≈0** | `paperX_pvalue_analysis.py` |
| **根因分析** | ✅ 已完成 | `notes/spectral_root_cause_analysis.md` |
| **框架完整推导综述** | ✅ 已完成 | `notes/spectral_comprehensive_review.md` |
| **独有实验预言汇总** | ✅ 已完成 | `notes/spectral_unique_predictions.md` |
| **跨领域谱对应——复杂系统** | ✅ → **Paper XIII** | `paper/paper13_spectral_complex_systems.md` |
| **凝聚态物理谱翻译** | ✅ → **Paper XIV** | `paper/paper14_spectral_condensed_matter.md` |
| **量子化学谱翻译** | ✅ → **Paper XV** | `paper/paper15_spectral_quantum_chemistry.md` |
| **S₁→S₂ 方案转换因子 Z_i** | 🟡 框架建立 | `notes/spectral_Zi_scheme_conversion.md` |
| **超荷 Y 的 Cl(1,7) 代数推导** | ✅ 已完成 | `notes/spectral_hypercharge_derivation.md` |
| **See-saw 谱算子推导** | ✅ 已完成 | `notes/spectral_see_saw_operator.md` |
| **多重静默通用方法论** | ✅ 已完成 | `notes/spectral_multi_silence_methodology.md` |
| **Kerr QNM 多重静默分析** | ✅ 已完成 | `notes/spectral_Kerr_silence_analysis.md` |
| **Higgs VEV 多重静默分析** | ✅ 已完成 | `notes/spectral_Higgs_silence_analysis.md` |
| **中微子质量层级多重静默分析** | ✅ 已完成 | `notes/spectral_neutrino_hierarchy_silence.md` |
| **暗物质遗迹密度多重静默分析** | ✅ 已完成 | `notes/spectral_dark_matter_silence.md` |

See `spectral_comprehensive_review.md` for a self-contained derivation chain from first principles to all 29 SM parameters.

**笔记→论文覆盖率：57/57（100%），详见 `notes_to_papers_audit.md`。**
**多重静默理论笔记：8 篇，详见 `spectral_root_cause_analysis.md`。**

## 当前重点问题（开放问题推进中）

1. **规范引力混合修正（Paper XII §9.3 β₃^(spec)）**：三圈 β 函数中的规范-引力混合项可使 M_Pl 处耦合偏移 ~5-15%；见 `src/spectral_rge_running.py`、`notes/spectral_root_cause_analysis.md` §4a。
2. **GUT 能标门限修正**：在 M_GUT ∼ 2×10¹⁶ GeV 处若存在新物理（seesaw 中微子质量），引入额外态射通道改变 β 系数。
3. **Kerr m≠0 Leaver 求解器收敛**：角向求解已收敛，径向 Leaver 系数约定需调试；见 `src/kerr_s2_guided_solver.py`、`notes/spectral_Kerr_silence_analysis.md`。
4. **谱方案 → MS-bar 方案转换因子 Z_i**：S₂ 层 DS 减除对易子框架已建立，Z_i 的显式解析公式待推导；见 `notes/spectral_Zi_scheme_conversion.md`。
5. **暗物质 α_DM 的第一原理推导**：谱静默粒子在 A_GR 谱结构中的精确范畴维数；见 `notes/spectral_dark_matter_silence.md`。

## 文件命名约定

- `YYYYMMDD_topic.md`：按日期记录的研究笔记。

## 相关索引

- 路线图：`roadmap/phase14_open_problems_advancement.md`
- 论文 I 开放问题：`paper/paper1_fractal_spectral_derecursion.md` §8.2
- 论文 II 开放问题：`paper/paper2_physics_applications.md` §8.2
- 代码实现：`src/math_open_problems_advanced.py`、`src/numerical_engineering_open_problems.py`、`src/physics_open_problems_advanced.py`
