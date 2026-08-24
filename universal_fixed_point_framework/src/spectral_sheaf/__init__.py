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

"""谱丛理论跨领域推广模块 (Phase 58-58E)

本模块将 Kerr 三对角谱丛理论推广到三个新领域：
  · 58A: 流变学 — 广义 Maxwell 模型的谱丛参数反演
  · 58B: NRG — Wilson 链谱丛剪枝加速
  · 58C: 记忆函数 — 连分数极点探测
  · 58E: 求解器算法定理补全 --- 自适应截断维度

依赖: leaver_unified_solver (两弦法框架)
"""

from ._rheo_to_tridiag import (
    compute_G_star, build_gmm_tridiag, compute_spectral_leaves,
    synthesize_rheo_data
)
from ._rheo_sheaf_inversion import (
    RheoSpectralInversion, sheaf_inversion, tikhonov_inversion
)
from ._nrg_tridiag import (
    compute_wilson_coefficients, compute_impurity_green_function,
    compute_spectral_function, build_nrg_tridiag,
    compute_nrg_spectral_leaves, green_from_tridiag,
    compute_condition_number, compute_pruning_threshold,
    get_pruned_indices, synthesize_kondo_data,
)
from ._nrg_sheaf_solver import (
    NRGStaticPruner, NRGDynamicPruner,
    analyze_spectral_leaves_coverage, benchmark_pruning,
    nrg_sheaf_solve,
)
from ._memory_tridiag import (
    compute_memory_function, compute_conductivity,
    compute_optical_conductivity, build_memory_tridiag,
    compute_memory_spectral_leaves, memory_from_tridiag,
    compute_det_AM, find_branch_points, synthesize_memory_data,
)
from ._memory_branch_detection import (
    compute_condition_number_A, scan_condition_number,
    compute_leaf_variation, scan_leaf_variation,
    locate_branch_points_joint, analyze_memory_branching,
    classify_branch_points,
)
from ._adaptive_N import (
    estimate_min_N, estimate_error, AdaptiveTruncation,
)

__all__ = [
    # 58A: 流变学
    "compute_G_star", "build_gmm_tridiag", "compute_spectral_leaves",
    "synthesize_rheo_data",
    "RheoSpectralInversion", "sheaf_inversion", "tikhonov_inversion",
    # 58B: NRG
    "compute_wilson_coefficients", "compute_impurity_green_function",
    "compute_spectral_function", "build_nrg_tridiag",
    "compute_nrg_spectral_leaves", "green_from_tridiag",
    "compute_condition_number", "compute_pruning_threshold",
    "get_pruned_indices", "synthesize_kondo_data",
    "NRGStaticPruner", "NRGDynamicPruner",
    "analyze_spectral_leaves_coverage", "benchmark_pruning",
    "nrg_sheaf_solve",
    # 58C: 记忆函数
    "compute_memory_function", "compute_conductivity",
    "compute_optical_conductivity", "build_memory_tridiag",
    "compute_memory_spectral_leaves", "memory_from_tridiag",
    "compute_det_AM", "find_branch_points", "synthesize_memory_data",
    "compute_condition_number_A", "scan_condition_number",
    "compute_leaf_variation", "scan_leaf_variation",
    "locate_branch_points_joint", "analyze_memory_branching",
    "classify_branch_points",
    # 58E: 自适应截断
    "estimate_min_N", "estimate_error", "AdaptiveTruncation",
]
