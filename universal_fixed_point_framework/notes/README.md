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
| **零参数质量预测（Spec 4-范畴静默层级→全部SM参数）** | ✅ **已完成** | `notes/spectral_zero_parameter_derivation.md` |
| **全费米子扩展** | ✅ 已完成 | `notes/spectral_zero_parameter_derivation.md` §§9-11 |
| **PMNS 数值对角化** | ✅ **4/4 通过** | `notes/spectral_PMNS_theta13.md` |
| **强 CP 谱解** | ✅ 已完成 | `notes/spectral_strong_CP.md` |
| **CP 相位分析** | 🟡 半定量 | `notes/spectral_CP_phases.md` |
| **剩余 SM 参数补齐** | 🟡 半定量 | `notes/spectral_remaining_SM_params.md` |
| **全 29 参数覆盖审计** | ✅ **100% 覆盖** | `notes/spectral_parameter_audit.md` |
| **根因分析** | ✅ 已完成 | `notes/spectral_root_cause_analysis.md` |
| **框架完整推导综述** | ✅ 已完成 | `notes/spectral_comprehensive_review.md` |
| **独有实验预言汇总** | ✅ 已完成 | `notes/spectral_unique_predictions.md` |

See `spectral_comprehensive_review.md` for a self-contained derivation chain from first principles to all 29 SM parameters.

## 当前重点问题（开放问题推进中）

1. **非分离 IFS 收敛率下界常数 $c$ 的显式最优估计**：已有定理 NS-LB 框架，需优化常数并建立重叠度热力学形式；见 `src/math_open_problems_advanced.py`、`roadmap/phase6_rkhs_construction.md`。
2. **Kerr 全局量子谱严格解析**：已有 QNM 近似框架，需完整 Leaver 连分数求解器与 spin-weighted spheroidal harmonics 高精度方法；见 `src/physics_open_problems_advanced.py`。
3. **$N=4$ SYM 强耦合谱方程**：已有弱耦合/BMN 匹配，需有限 $N_c$ 与强耦合下可积系统谱方程；见 `src/physics_open_problems_advanced.py`。
4. **MadGraph/micrOMEGAs 真实安装联调**：已有接口层与解析回退，需在真实工具安装上端到端验证；见 `src/numerical_engineering_open_problems.py`。
5. **双星引力波全波形与 LALSuite 对接**：已有原型波形，需接入 SEOBNRv4/IMRPhenom；见 `src/numerical_engineering_open_problems.py`。

## 文件命名约定

- `YYYYMMDD_topic.md`：按日期记录的研究笔记。

## 相关索引

- 路线图：`roadmap/phase14_open_problems_advancement.md`
- 论文 I 开放问题：`paper/paper1_fractal_spectral_derecursion.md` §8.2
- 论文 II 开放问题：`paper/paper2_physics_applications.md` §8.2
- 代码实现：`src/math_open_problems_advanced.py`、`src/numerical_engineering_open_problems.py`、`src/physics_open_problems_advanced.py`
