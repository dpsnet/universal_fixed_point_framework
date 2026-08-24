# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
笔记分类映射脚本
================
1. 读取所有 .md 和 .py 文件
2. 按主题分类到子目录
3. 复制文件（保留原文件）
4. 生成 mapping_table.md（旧路径 ↔ 新路径对照表）
"""

import os, shutil, glob

NOTES_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# 分类规则: (glob_pattern, subdirectory)
# RULE_ORDER 决定匹配优先级（先匹配的优先）
# ============================================================================

RULE_ORDER = [
    # -- 07_validation (开放数据验证) --
    ("open_data_validation_report*", "07_validation"),
    ("open_data_analysis_*", "07_validation"),

    # -- 08_first_principles (第一性原理推导) --
    ("spectral_dynamics_first_principles_derivation*", "08_first_principles"),
    ("spectral_dynamics_force_unification*", "08_first_principles"),
    ("spectral_dynamics_high_school_physics*", "08_first_principles"),
    ("spectral_Zi_scheme_conversion*", "08_first_principles"),
    ("spectral_su2_emergence*", "08_first_principles"),
    ("spectral_vs_GR_geometry*", "08_first_principles"),

    # -- 00_foundations (范畴基础) --
    ("rec_spec_definitions*", "00_foundations"),
    ("spectral_correspondence_equivalence*", "00_foundations"),
    ("spectral_comprehensive_review*", "00_foundations"),
    ("spectral_QFT_axioms*", "00_foundations"),
    ("spectral_formalization*", "00_foundations"),
    ("spectral_higher_infinity_category_formalization*", "00_foundations"),
    ("spectral_static_topology_category*", "00_foundations"),
    ("spectral_static_topology*", "00_foundations"),
    ("spectral_noise_category*", "00_foundations"),
    ("spectral_lagrangian*", "00_foundations"),
    ("spectral_feynman_rules*", "00_foundations"),
    ("spectral_path_integral*", "00_foundations"),
    ("spectral_resource_theory*", "00_foundations"),
    ("spectral_unitarity_proof*", "00_foundations"),
    ("spectral_measurement*", "00_foundations"),
    ("spectral_entanglement*", "00_foundations"),
    ("spectral_contextuality_experiment*", "00_foundations"),
    ("spectral_quantum_eraser*", "00_foundations"),
    ("spectral_collapse_experiment*", "00_foundations"),
    ("spectral_non_markov_te_gm*", "00_foundations"),
    ("spectral_interpretation_comparison*", "00_foundations"),
    ("spectral_formal_proof_findings*", "00_foundations"),

    # -- 01_qcd_higgs (QCD、Higgs、手征对称性) --
    ("spectral_low_energy_QCD*", "01_qcd_higgs"),
    ("spectral_root_cause_analysis*", "01_qcd_higgs"),
    ("spectral_Higgs_silence_analysis*", "01_qcd_higgs"),
    ("spectral_Higgs_zero_parameter*", "01_qcd_higgs"),
    ("spectral_chiral_theory*", "01_qcd_higgs"),
    ("spectral_chiral_open_problems*", "01_qcd_higgs"),
    ("spectral_strong_CP*", "01_qcd_higgs"),
    ("spectral_alpha_exponent*", "01_qcd_higgs"),
    ("spectral_alpha_silence*", "01_qcd_higgs"),
    ("spectral_vacuum_stability*", "01_qcd_higgs"),
    ("spectral_delta_lambda_analytic*", "01_qcd_higgs"),
    ("spectral_epsilon_derivation*", "01_qcd_higgs"),

    # -- 02_ckm_pmns_flavor (CKM/PMNS/Yukawa/味道) --
    ("spectral_ckm_angles*", "02_ckm_pmns_flavor"),
    ("spectral_CKM*", "02_ckm_pmns_flavor"),
    ("spectral_full_19_parameters*", "02_ckm_pmns_flavor"),
    ("spectral_zero_parameter_derivation*", "02_ckm_pmns_flavor"),
    ("spectral_remaining_SM_params*", "02_ckm_pmns_flavor"),
    ("spectral_CP_phases*", "02_ckm_pmns_flavor"),
    ("spectral_Yukawa*", "02_ckm_pmns_flavor"),
    ("spectral_yukawa_IFS_weights*", "02_ckm_pmns_flavor"),
    ("spectral_J_gen_rotation*", "02_ckm_pmns_flavor"),
    ("spectral_first_order_CKM*", "02_ckm_pmns_flavor"),
    ("spectral_PMNS_theta13*", "02_ckm_pmns_flavor"),
    ("spectral_SM*", "02_ckm_pmns_flavor"),
    ("spectral_hypercharge_derivation*", "02_ckm_pmns_flavor"),

    # -- 03_neutrino (中微子) --
    ("spectral_neutrino_absolute*", "03_neutrino"),
    ("spectral_neutrino_hierarchy_silence*", "03_neutrino"),
    ("spectral_neutrino_seeSaw*", "03_neutrino"),
    ("spectral_see_saw_operator*", "03_neutrino"),
    ("spectral_see_saw_rotation*", "03_neutrino"),

    # -- 04_lorentz_gravity (Lorentz 谱流、引力、Kerr) --
    ("spectral_lorentz_dynamics*", "04_lorentz_gravity"),
    ("spectral_lorentz_kinematics*", "04_lorentz_gravity"),
    ("spectral_lorentz_causality