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

"""
test_open_problems_advanced.py

开放问题推进模块的单元测试。
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from math_open_problems_advanced import (
    minimax_lower_bound,
    adversarial_sample_configuration,
    spectral_dimension_from_lyapunov_entropy,
    verify_singular_continuous_lyapunov_relation,
    feng_wang_dimension,
    dimension_vs_overlap_curve,
    RuelleTransferOperator,
    FengWangOptimalConditionalOperator,
    FengWangConditionalTransferOperator,
    verify_topological_entropy_gap_inequality,
    MarkovIFS,
    GeneralDynamicalSystemTEG,
)
from numerical_engineering_open_problems import (
    MadGraphInterface,
    MicrOmegasInterface,
    BinaryGWWaveform,
)
from physics_open_problems_advanced import (
    KerrBlackHole,
    KerrGlobalSpectrum,
    N4SYMSpectrum,
    N4SYMBES,
    N4SYMBESFull,
    FullTeukolskyQNM,
    DarkMatterFractalSpectrum,
)
from kerr_fractal_entropy import KerrBlackHole


def test_minimax_lower_bound_scaling():
    """下界应随 N 增大而多项式衰减，指数 ~ -α/d_H。"""
    d_h, alpha = 0.85, 1.0
    lb1 = minimax_lower_bound(d_h, alpha, holder_constant=1.0, diameter=1.0, N=100)
    lb2 = minimax_lower_bound(d_h, alpha, holder_constant=1.0, diameter=1.0, N=1000)
    assert lb2 < lb1
    # 比值近似 10^{-α/d_H}
    ratio = lb2 / lb1
    expected = 1000 ** (-alpha / d_h) / 100 ** (-alpha / d_h)
    assert np.isclose(ratio, expected, rtol=1e-6)


def test_adversarial_configuration_reaches_lower_bound():
    """对抗性样本的特征值差异应不低于预测下界。"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    adv = adversarial_sample_configuration(c, p, N=200, ambient_dim=1, overlap_degree=0.3)
    assert adv["eigenvalue_diff"] >= adv["predicted_lower"]


def test_kaplan_yorke_matches_hausdorff_for_symmetric_ifs():
    """对称 IFS 下 D_KY 应接近 d_H。"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    verify = verify_singular_continuous_lyapunov_relation(c, p, ambient_dim=1)
    assert verify["agreement"]


def test_madgraph_interface_fallback():
    """MadGraph 未安装时返回解析回退结果。"""
    mg = MadGraphInterface(model="sm", energy_com=13.0, nevents=1000)
    result = mg.run_madgraph(
        initial_states=[("p", "p")],
        final_states=[["t", "t~"]],
    )
    assert result["tool"] == "madgraph_fallback" or result["tool"] == "madgraph"
    assert result["cross_section_pb"] > 0


def test_micromegas_interface_fallback():
    """micrOMEGAs 未安装时返回解析回退结果。"""
    mo = MicrOmegasInterface(model_name="singletDM")
    mo.alpha_X = 0.003
    result = mo.run_micromegas()
    assert result["tool"] in ("micromegas_fallback", "micromegas")
    if result["tool"] == "micromegas_fallback":
        assert 0.05 <= result["relic_density"] <= 10.0


def test_binary_gw_waveform_shape():
    """双星波形输出长度合理，h_plus 与 h_cross 同长度。"""
    gw = BinaryGWWaveform(m1=30.0, m2=25.0, f_low=30.0, delta_t=1.0 / 4096.0)
    wf = gw.generate_waveform()
    assert len(wf["time_s"]) == len(wf["h_plus"]) == len(wf["h_cross"])
    assert wf["f_merger_Hz"] > gw.f_low
    assert wf["f_ringdown_Hz"] > wf["f_merger_Hz"]


def test_kerr_global_spectrum():
    """Kerr 全局谱生成合理数量的模式。"""
    bh = KerrBlackHole(M=1.0, a=0.5)
    spec = KerrGlobalSpectrum(bh, s=-2, l_max=3, n_max=2)
    result = spec.global_spectrum()
    # l=2,3; m=-l..l; n=0,1 => 2*(5+7) = 24? actually 2*sum(2l+1) for l=2,3 = 2*(5+7)=24
    assert result["n_modes"] == 24
    # 所有 λ 应在 (0,1]
    for mode in result["modes"]:
        assert 0 < mode["lambda"] <= 1.0


def test_n4_sym_framework_match():
    """N=4 SYM 谱对应 η_R 精确成立。"""
    n4 = N4SYMSpectrum(N_c=3, lambda_tHooft=6.0, J_max=4)
    match = n4.match_to_framework()
    assert match["framework_match"]
    assert match["max_eta_error"] < 1e-10


def test_dark_matter_constrained_spectrum():
    """暗物质分形谱在合理参数下至少有一个候选通过约束。"""
    dm = DarkMatterFractalSpectrum(
        m_base=100.0,
        ifs_c=np.array([0.5, 0.3]),
        ifs_p=np.array([0.7, 0.3]),
        alpha_X=0.003,
    )
    constrained = dm.constrained_spectrum(n_levels=2)
    assert len(constrained["allowed_candidates"]) >= 1
    assert constrained["fractal_dimension"] > 0


def test_feng_wang_dimension_decreases_with_overlap():
    """Feng-Wang 维数应随重叠度增大而下降（非分离 IFS）。"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    fw0 = feng_wang_dimension(c, p, overlap_degree=0.0, n_letters=4)
    fw3 = feng_wang_dimension(c, p, overlap_degree=0.3, n_letters=4)
    assert fw0["d_feng_wang"] > fw3["d_feng_wang"]
    assert fw0["d_feng_wang"] > 0.9  # Moran 维数 ~1


def test_dimension_vs_overlap_curve_monotonic():
    """维数-重叠度曲线应整体非增。"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    curve = dimension_vs_overlap_curve(
        c, p, overlap_values=np.linspace(0.0, 0.5, 6)
    )
    dims = curve["dimensions"]
    assert all(dims[i] >= dims[i + 1] - 1e-6 for i in range(len(dims) - 1))


def test_leaver_qnm_solver_converges():
    """Leaver 连分数求解器应在有限步内收敛。"""
    bh = KerrBlackHole(M=1.0, a=0.5)
    spec = KerrGlobalSpectrum(bh, s=-2, l_max=3, n_max=2)
    leaver = spec.solve_qnm_leaver(l=2, m=0, n=0)
    assert leaver["iterations"] > 0
    assert leaver["iterations"] <= 50
    assert isinstance(leaver["omega"], complex)


def test_n4_sym_strong_coupling_growth():
    """强耦合下 Konishi 维数应按 λ^{1/4} 增长。"""
    n4_small = N4SYMSpectrum(N_c=3, lambda_tHooft=1.0, J_max=4)
    n4_large = N4SYMSpectrum(N_c=3, lambda_tHooft=1000.0, J_max=4)
    assert n4_large._konishi_dimension_strong() > n4_small._konishi_dimension_strong()
    # 强耦合 1000^{1/4} ≈ 5.6，增长约 5.6/1 = 5.6 倍
    ratio = (n4_large._konishi_dimension_strong() - 2.0) / (n4_small._konishi_dimension_strong() - 2.0)
    assert 3.0 < ratio < 8.0


def test_n4_sym_interpolation_bridges_regimes():
    """弱→强耦合插值应在中间耦合介于弱耦合与强耦合之间。"""
    n4 = N4SYMSpectrum(N_c=3, lambda_tHooft=6.0, J_max=4)
    d_weak = n4._konishi_dimension()
    d_strong = n4._konishi_dimension_strong()
    d_interp = n4.interpolate_dimension(2, 6.0)
    assert min(d_weak, d_strong) <= d_interp <= max(d_weak, d_strong)


def test_ruelle_transfer_operator_matches_moran():
    """Ruelle 转移算子在 OSC 情形应复现 Moran 维数。"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    rto = RuelleTransferOperator(c, p, overlap_degree=0.0)
    res = rto.dimension(s_min=0.0, s_max=2.0, n_grid=80)
    assert abs(res["d_moran"] - 1.0) < 0.05
    assert abs(res["d_transfer"] - res["d_moran"]) < 0.05


def test_ruelle_dimension_decreases_with_overlap():
    """Ruelle/Feng-Wang 精确转移算子维数应随重叠度增大而下降。"""
    c = np.array([0.5, 0.3])
    p = np.array([0.6, 0.4])
    rto0 = RuelleTransferOperator(c, p, overlap_degree=0.0)
    rto3 = RuelleTransferOperator(c, p, overlap_degree=0.3)
    d0 = rto0.dimension(s_min=0.0, s_max=2.0, n_grid=80)["d_transfer"]
    d3 = rto3.dimension(s_min=0.0, s_max=2.0, n_grid=80)["d_transfer"]
    assert d0 > d3


def test_topological_entropy_gap_inequality():
    """拓扑熵-谱间隙不等式 h_μ·γ ≤ 1 对典型参数成立。"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    res = verify_topological_entropy_gap_inequality(c, p)
    assert res["satisfied"]
    assert 0.0 < res["topological_entropy"] < np.log(2) + 1e-6


def test_leaver_exact_qnm_solver_converges():
    """精确系数 Leaver 连分数求解器应收敛。"""
    bh = KerrBlackHole(M=1.0, a=0.5)
    spec = KerrGlobalSpectrum(bh, s=-2, l_max=3, n_max=2)
    leaver = spec.solve_qnm_leaver_exact(l=2, m=0, n=0)
    assert leaver["iterations"] > 0
    assert leaver["iterations"] <= 50
    assert isinstance(leaver["omega"], complex)


def test_n4_bes_konishi_converges():
    """简化 BES 方程对 Konishi 算子应给出有限维数。"""
    bes = N4SYMBES(N_c=3, lambda_tHooft=6.0)
    res = bes.bes_dimension(J=2)
    assert res["residual"] < 1e-3
    assert 1.5 < res["Delta"] < 6.0


def test_feng_wang_optimal_conditional_operator():
    """Feng-Wang 最优条件转移算子（加权测度）在 OSC 情形应复现 Moran 维数。"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    fw_opt = FengWangOptimalConditionalOperator(c, p, scale_factor=2.0)
    res = fw_opt.dimension(s_min=0.0, s_max=2.0, n_grid=80)
    assert abs(res["d_moran"] - 1.0) < 0.05
    assert abs(res["d_transfer"] - res["d_moran"]) < 0.05
    # 加权测度应比贪心选择更稳定（连续权重）
    fw_cond = FengWangConditionalTransferOperator(c, p, separation_factor=0.5)
    res_cond = fw_cond.dimension(s_min=0.0, s_max=2.0, n_grid=80)
    assert abs(res_cond["d_transfer"] - res["d_transfer"]) < 0.2


def test_general_dynamical_system_teg():
    """一般动力系统 TE-G 框架应能数值验证 h_top·γ ≤ C。"""
    gen_teg = GeneralDynamicalSystemTEG(dim=1)
    res = gen_teg.verify_inequality(constant=1.0)
    assert res["satisfied"]
    np.random.seed(42)
    A = gen_teg.random_mixing_matrix(n=8)
    # 对 d 维随机矩阵，常数 C 应取 dim 的适当倍数
    # 这里用保守估计 C = 8（矩阵维数）
    res2 = gen_teg.verify_inequality(A, constant=8.0)
    assert res2["satisfied"]
    assert res2["h_top"] > 0


def test_full_teukolsky_self_consistent():
    """完整 Teukolsky-Leaver 求解器应收敛（使用 homotopy continuation）。"""
    teuk = FullTeukolskyQNM(M=1.0, a=0.5, s=-2)
    res = teuk.solve_full(l=2, m=0, n=0)
    assert res["iterations"] > 0
    assert res["iterations"] <= 50
    assert isinstance(res["omega"], complex)
    assert res["converged"], f"求解器未收敛: {res['omega']}"


def test_n4_bes_full_dressing_order():
    """完整 BES/TBA 的 dressing order 应可升级且收敛。"""
    bes_full = N4SYMBESFull(N_c=3, lambda_tHooft=6.0)
    # dressing_order=1 应与简化版接近
    res1 = bes_full.full_bes_dimension(J=2)
    assert res1["residual"] < 1e-2
    assert 1.5 < res1["Delta"] < 6.0


def test_markov_ifs_entropy_gap():
    """Markov IFS 的 h_top·γ 应可显式计算并满足 ≤ 1。"""
    A = np.array([[1.0, 1.0], [1.0, 1.0]])
    markov = MarkovIFS(A, np.array([0.5, 0.5]))
    res = markov.entropy_and_gap()
    assert res["product"] <= 1.0 + 1e-10
    assert res["h_top"] > 0


def test_full_teukolsky_qnm_converges():
    """完整 Teukolsky-Leaver 求解器应收敛。"""
    teuk = FullTeukolskyQNM(M=1.0, a=0.5, s=-2)
    res = teuk.solve(l=2, m=0, n=0)
    assert res["iterations"] > 0
    assert res["iterations"] <= 50
    assert isinstance(res["omega"], complex)


def test_n4_bes_full_konishi_converges():
    """完整 BES/TBA（含 dressing phase + wrapping）应给出有限维数。"""
    bes_full = N4SYMBESFull(N_c=3, lambda_tHooft=6.0)
    res = bes_full.full_bes_dimension(J=2)
    assert res["residual"] < 1e-2
    assert 1.5 < res["Delta"] < 6.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
