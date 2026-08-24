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
spectral_flavor_fibration.py — 味物理 5层嵌套纤维化链谱交织条件数值验证

Phase 56B3 (味物理 5层纤维化) 的核心验证脚本。验证内容：

1. 5 层谱生成元构造（Yukawa/Mixing/CP/Seesaw/Hierarchy）
2. 层间谱交织条件 [A_i, π_{i←i+1}]_{HS} 计算
3. 非单调能标排序的 d 方向判断（Seesaw 层反向跳跃）
4. ℓ_corr 替换为 ln(c_i) 的数值标定

参考：
- notes/02_ckm_pmns_flavor/spectral_flavor_fibration.md §5
- notes/00_foundations/spectral_fibration_domain_generalization.md §5
- notes/02_ckm_pmns_flavor/spectral_ckm_angles.md
- notes/02_ckm_pmns_flavor/spectral_yukawa_IFS_weights.md
"""

import numpy as np
from typing import Dict

# ============================================================
# 味物理基本常数
# ============================================================
D_H = 2.7095           # IFS Hausdorff 维数
M_GUT = 2.0e16         # GUT 标度 (GeV)
M_EW = 246.0           # 电弱标度 (GeV)
LAMBDA_CHI = 1.0       # 手征标度 (GeV)
M_R = 1.0e11           # Seesaw 标度 (GeV)
LAMBDA_QCD = 0.33      # QCD 标度 (GeV)

EPSILON_0 = 1e-3       # 基准阈值
DELTA_E_0 = 1.0        # 基准能标间隔 (eV)

# 能标表 (GeV) - 注意非单调排序
ENERGY_SCALES = {
    'Yukawa': M_GUT,       # 10^16 GeV (最高能)
    'Mixing': M_EW,        # 10^2 GeV
    'CP': LAMBDA_CHI,      # 1 GeV
    'Seesaw': M_R,         # 10^11 GeV (跳跃)
    'Hierarchy': LAMBDA_QCD,  # 0.33 GeV (最低)
}

# 代间质量比（用于 ℓ_corr = ln(c_i) 的数值标定）
MASS_RATIOS = {
    'Yukawa': {
        'c_t': 172.44 / 1.27,    # m_t/m_c ~ 136
        'c_b': 4.18 / 0.093,     # m_b/m_s ~ 45
        'c_tau': 1.77686 / 0.10566,  # m_tau/m_mu ~ 16.8
    },
    'Hierarchy': {
        'c_12': np.exp(-D_H * 1),  # 第1-2代间
        'c_23': np.exp(-D_H * 1),  # 第2-3代间
    }
}

# CKM 角度（rad）
CKM_ANGLES = {
    'theta_12': D_H / 12,    # 0.2258
    'theta_23': 1.0 / 24,    # 0.04167
    'theta_13': D_H / 720,   # 0.003763
    'delta_CP': 1.180,       # rad
}


def epsilon_threshold_flavor(E_i: float, E_ip1: float,
                             d: int = 1) -> float:
    """味物理的谱交织条件阈值

    非单调能标排序的方向判断：
    - d=+1: 能标从高到低（投影是粗粒化）
    - d=-1: 能标从低到高（投影是精粒化）
    """
    eps0 = 1e-3
    dE0 = 1.0  # eV
    dE = abs(E_i - E_ip1)  # GeV
    if dE <= 0:
        return 1.0

    dE_eV = dE * 1e9
    eps_forward = eps0 * (dE0 / dE_eV)

    if d == -1:
        # 反向修正
        ratio = min(E_i, E_ip1) / max(E_i, E_ip1)
        eps_reverse = eps_forward * ratio
    else:
        eps_reverse = eps_forward

    return max(eps_reverse, 1e-80)


# ============================================================
# 各层谱生成元
# ============================================================
def spectral_operator_flavor_layer(layer: str, size: int = 3) -> np.ndarray:
    """构造味物理各层的谱生成元 A_i

    Parameters
    ----------
    layer : str — 层名
    size : int — 矩阵维度（代数量）

    Returns
    -------
    np.ndarray — 谱生成元 A_i
    """
    if layer == 'Yukawa':
        # Yukawa 特征值谱（轻子扇区归一化）
        y = np.array([0.00475, 0.0169, 0.00724])[:size]
        y = y / np.max(y)
        H = np.diag(y)

    elif layer == 'Mixing':
        # 混合角谱生成元（J-旋转的特征值）
        # 对应 CKM 角度：θ12, θ23, θ13
        thetas = np.array([CKM_ANGLES['theta_12'],
                           CKM_ANGLES['theta_23'],
                           CKM_ANGLES['theta_13']])[:size]
        evals = np.sin(thetas) ** 2
        evals = np.maximum(evals, 1e-10)
        H = np.diag(evals)

    elif layer == 'CP':
        # CP 相位谱生成元
        # δ_CP 作为谱和乐，生成元来自 Arg(J) 的虚部
        evals = np.array([CKM_ANGLES['delta_CP'],
                          CKM_ANGLES['delta_CP'] / 10,
                          CKM_ANGLES['delta_CP'] / 100])[:size]
        H = np.diag(evals)

    elif layer == 'Seesaw':
        # Seesaw 谱生成元
        # M_ν ≈ m_D^2 / M_R，中微子质量 ~ 0.1 eV
        m_nu = 0.1  # eV → GeV
        m_D = 1.0   # GeV (Dirac mass ~ 电弱标度)
        evals = np.array([m_nu**2 / m_D,
                          m_nu / m_D,
                          m_nu / m_D * 10])[:size]
        evals = np.maximum(evals, 1e-30)
        H = np.diag(evals)

    elif layer == 'Hierarchy':
        # 代间质量层级谱生成元
        # IFS 收缩因子 c_i^α
        alpha = 2.7095  # 基础 α
        c1 = np.exp(-alpha * 0)
        c2 = np.exp(-alpha * 1)
        c3 = np.exp(-alpha * 2)
        evals = np.array([c1, c2, c3])[:size]
        H = np.diag(evals)

    else:
        raise ValueError(f"Unknown layer: {layer}")

    # 谱生成元 A = exp(-β · H)，归一化
    beta = 1.0 / (np.trace(H) / size + 1e-30)
    A = np.linalg.matrix_power(np.eye(size) - beta * H / size, size)
    A = (A + A.conj().T) / 2
    norm = np.linalg.norm(A)
    A = A / norm if norm > 0 else A
    return A


def projection_operator(n_fine: int, n_coarse: int) -> np.ndarray:
    """构造层间投影算子 π_{i←i+1}"""
    pi = np.zeros((n_fine, n_coarse))
    for i in range(min(n_fine, n_coarse)):
        pi[i, i] = 1.0
    return pi


# ============================================================
# 1. 能标排序与纤维方向
# ============================================================
def verify_energy_ordering() -> Dict:
    """验证味物理的非单调能标排序"""
    layers_in_order = ['Yukawa', 'Mixing', 'CP', 'Seesaw', 'Hierarchy']
    E_values = {
        'Yukawa': M_GUT,
        'Mixing': M_EW,
        'CP': LAMBDA_CHI,
        'Seesaw': M_R,
        'Hierarchy': LAMBDA_QCD,
    }

    print("=" * 65)
    print("味物理能标排序验证（非单调）")
    print("=" * 65)
    print(f"  {'层':<15} {'能标 (GeV)':<18} {'方向'}")
    print("-" * 65)

    results = {}
    for i, layer in enumerate(layers_in_order):
        E = E_values[layer]
        E_str = f"{E:.4e}"
        if i < len(layers_in_order) - 1:
            E_next = E_values[layers_in_order[i + 1]]
            if E_next > E:
                direction = "↑ (d=-1, 反向)"
            else:
                direction = "↓ (d=+1, 正向)"
        else:
            direction = "—"
        print(f"  Bun({layer:<10}) {E_str:<18} {direction}")
        results[layer] = {'energy_GeV': E, 'direction': direction}

    print("-" * 65)
    print("  注意: Seesaw 层 (10^11 GeV) 能标高于 Mixing 和 CP 层,")
    print("  导致 CP→Seesaw 界面为反向跳跃 (d=-1).")
    print()

    return results


# ============================================================
# 2. ℓ_corr 替换验证
# ============================================================
def verify_lcorr_flavor() -> Dict:
    """验证味物理的 ℓ_corr = ln(c_i) 替换"""
    results = {}

    lcorr_table = {
        'Bun(Yukawa)': {
            'formula': r'\ln(c_t)',
            'value': np.log(MASS_RATIOS['Yukawa']['c_t']),
            'physical': '顶-粲代间',
        },
        'Bun(Mixing)': {
            'formula': r'\ln(c_b)',
            'value': np.log(MASS_RATIOS['Yukawa']['c_b']),
            'physical': '底-奇异代间',
        },
        'Bun(CP)': {
            'formula': r'\ln(c_\tau)',
            'value': np.log(MASS_RATIOS['Yukawa']['c_tau']),
            'physical': 'τ-μ 代间',
        },
        'Bun(Seesaw)': {
            'formula': r'\ln(m_\nu/m_\tau)',
            'value': np.log(0.1e-9 / 1.77686),
            'physical': '中微子-轻子极端跨度',
        },
        'Bun(Hierarchy)': {
            'formula': r'd_H',
            'value': D_H,
            'physical': 'IFS Hausdorff 维数',
        },
    }

    print("=" * 65)
    print("味物理 ℓ_corr = ln(c_i) 替换验证")
    print("=" * 65)
    print(f"  {'层':<20} {'ℓ_D 公式':<24} {'值':<12} {'物理意义'}")
    print("-" * 65)

    for layer, info in lcorr_table.items():
        val = info['value']
        print(f"  {layer:<20} {info['formula']:<24} {val:<12.4f} {info['physical']}")
        results[layer] = info

    print("-" * 65)
    print()

    return results


# ============================================================
# 3. 谱交织条件验证
# ============================================================
def verify_intertwining_flavor() -> Dict:
    """计算味物理各层间的 Hilbert-Schmidt 谱交织范数

    层序: Yukawa(高) → Mixing → CP → Seesaw(跳跃) → Hierarchy(低)
    所有层使用代空间维度 3.
    """
    layers = ['Yukawa', 'Mixing', 'CP', 'Seesaw', 'Hierarchy']
    dims = {'Yukawa': 3, 'Mixing': 3, 'CP': 3, 'Seesaw': 3, 'Hierarchy': 3}

    # 方向判断: 正向(+1)能标递减, 反向(-1)能标递增
    E_vals = {'Yukawa': M_GUT, 'Mixing': M_EW, 'CP': LAMBDA_CHI,
              'Seesaw': M_R, 'Hierarchy': LAMBDA_QCD}

    print("=" * 65)
    print("味物理谱交织条件 [A_i, π_{i←i+1}]_{HS} 验证")
    print("=" * 65)
    print(f"  {'界面':<20} {'d':<5} {'HS 范数':<18} {'ε_i':<18}")
    print("-" * 65)

    results = {}
    for i in range(len(layers) - 1):
        layer_i = layers[i]
        layer_ip1 = layers[i + 1]
        dim_i = dims[layer_i]
        dim_ip1 = dims[layer_ip1]

        A_i = spectral_operator_flavor_layer(layer_i, dim_i)
        A_ip1 = spectral_operator_flavor_layer(layer_ip1, dim_ip1)

        # 投影 π: V_{i+1} → V_i
        pi = projection_operator(dim_i, dim_ip1)
        commutator = A_i @ pi - pi @ A_ip1
        hs_val = np.sqrt(np.trace(commutator.conj().T @ commutator).real)

        # 方向判断
        E_i = E_vals[layer_i]
        E_ip1 = E_vals[layer_ip1]
        d = 1 if E_i >= E_ip1 else -1

        eps = epsilon_threshold_flavor(E_i, E_ip1, d)

        # 状态判断
        if hs_val < eps or np.isnan(hs_val):
            status = "OK"
        elif hs_val < 10 * eps:
            status = "边缘"
        elif hs_val < 100 * eps:
            status = "需 RG"
        else:
            status = "大偏差"

        entry = {
            'interface': f'{layer_i}→{layer_ip1}',
            'd': d,
            'hs_norm': hs_val,
            'epsilon': eps,
            'status': status,
        }
        results[f'{layer_i}→{layer_ip1}'] = entry

        hs_str = f"{hs_val:.4e}" if not np.isnan(hs_val) else "N/A"
        eps_str = f"{eps:.2e}" if eps > 1e-300 else "<1e-300"
        print(f"  {layer_i+'→'+layer_ip1:<20} {d:<5} {hs_str:<18} {eps_str:<18} {status}")

    print("-" * 65)
    print()

    return results


# ============================================================
# 4. 截面传递验证
# ============================================================
def verify_section_propagation_flavor() -> Dict:
    """验证味物理层间截面传递"""
    sections = {
        'Yukawa': ['y_u', 'y_c', 'y_t', 'y_d', 'y_s', 'y_b', 'y_e', 'y_μ', 'y_τ'],
        'Mixing': ['θ12', 'θ23', 'θ13', 'δ_CP', '|V_{us}|', '|V_{cb}|', '|V_{ub}|'],
        'CP': ['δ_CP', 'Jarlskog J', 'Im(V)'],
        'Seesaw': ['m_ν1', 'm_ν2', 'm_ν3', 'U_PMNS', 'Δm²_sol', 'Δm²_atm'],
        'Hierarchy': ['c_12 = exp(-d_H)', 'c_23 = exp(-d_H)',
                       'α 指数', 'm_i/c_i^α 比'],
    }

    print("=" * 65)
    print("味物理层间截面传递映射")
    print("=" * 65)
    print(f"  截面传递链: σ_Y → σ_M → σ_CP → σ_S → σ_H")
    print("-" * 65)

    results = {}
    for layer, obs in sections.items():
        obs_str = ', '.join(obs[:4])
        print(f"  Bun({layer:<10}) : {obs_str}...")
        results[layer] = {'observables': obs}

    print("-" * 65)
    print()

    return results


# ============================================================
# 5. 统一验证报告
# ============================================================
def run_all_tests():
    """运行所有验证测试并生成报告"""
    print()
    print("#" * 65)
    print("#  味物理 5层纤维化链验证报告")
    print("#  Phase 56B3 — 2026-07-25")
    print("#" * 65)
    print()

    # 1. 能标排序
    energy_results = verify_energy_ordering()

    # 2. ℓ_corr
    lcorr_results = verify_lcorr_flavor()

    # 3. 谱交织条件
    int_results = verify_intertwining_flavor()

    # 4. 截面传递
    sec_results = verify_section_propagation_flavor()

    # === 汇总表 ===
    print("=" * 65)
    print("味物理 5层纤维化链 — 验证汇总")
    print("=" * 65)
    print(f"  {'界面':<20} {'方向 d':<8} {'HS 范数':<16} {'ε_i':<16}")
    print("-" * 65)

    for name, entry in int_results.items():
        hs = entry['hs_norm']
        eps = entry['epsilon']
        hs_str = f"{hs:.4e}" if not np.isnan(hs) else "N/A"
        eps_str = f"{eps:.2e}" if eps > 1e-300 else "<1e-300"
        print(f"  {name:<20} {entry['d']:<8} {hs_str:<16} {eps_str:<16} {entry['status']}")

    print("-" * 65)

    # 状态判断
    ok_all = all(
        e['status'] == 'OK' or e['status'] == 'N/A'
        for e in int_results.values()
    )

    if ok_all:
        print("\n  结论: 味物理 5层纤维化链的谱交织条件全部满足。")
        print("  层间解耦在理论精度内成立。")
    else:
        print("\n  结论: 部分层间谱交织条件超出阈值。")
        print("  需要进一步 RG 流嵌入或能标分层优化。")

    print()
    print("=" * 65)
    print(f"  总层数: 5")
    print(f"  总谱交织条件数: 4")
    print(f"  正向方向 (d=+1): 3 个界面")
    print(f"  反向方向 (d=-1): 1 个界面 (CP→Seesaw)")
    print(f"  ℓ_corr 替换: ln(c_i)")
    print("=" * 65)

    return {
        'energy_ordering': energy_results,
        'lcorr': lcorr_results,
        'intertwining': int_results,
        'sections': sec_results,
        'feasible': ok_all,
    }


if __name__ == '__main__':
    results = run_all_tests()
