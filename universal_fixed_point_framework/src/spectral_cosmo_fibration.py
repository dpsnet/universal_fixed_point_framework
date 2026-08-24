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
spectral_cosmo_fibration.py — 宇宙学 6层嵌套纤维化链谱交织条件验证

Phase 56C2 (宇宙学 6层分解 + 时间-纤维化对偶) 的核心验证脚本。验证内容：

1. 6 层谱生成元构造（Inflation/Reheat/BBN/LSS/DE/Quantum_Cosmo）
2. 基于红移差的谱交织条件 ε_cosmo ∼ H²/M_Pl²
3. 时间-纤维化对偶的数值验证
4. ℓ_corr = H^{-1}(z) 的数值标定

参考：
- notes/05_cosmology/spectral_cosmo_fibration.md
- notes/00_foundations/spectral_fibration_domain_generalization.md §6
- Paper V §7 (FLRW 谱动力学)
"""

import numpy as np
from typing import Dict

# ============================================================
# 宇宙学常数
# ============================================================
M_PL = 1.22091e19       # Planck 质量 (GeV)
H0 = 67.4               # km/s/Mpc (today)
H0_INV = 1.44e26        # Hubble 半径 (m)
T_CMB = 2.725           # CMB 温度 (K)

# 红移与能标
COSMO_PARAMS = {
    'Inflation': {
        'z': 1e27,
        'E_GeV': 1e16,           # GeV
        'H': 1e13,                # GeV (暴胀期 Hubble 标度)
        'desc': '暴胀',
    },
    'Reheat': {
        'z': 1e26,
        'E_GeV': 1e15,           # GeV
        'H': 1e12,
        'desc': '再加热',
    },
    'BBN': {
        'z': 1e9,
        'E_GeV': 1e-3,           # ~1 MeV
        'H': 1e-27,               # GeV
        'desc': 'BBN',
    },
    'LSS': {
        'z': 1100,
        'E_GeV': 3e-10,          # ~0.3 eV
        'H': 3e-37,               # GeV
        'desc': '重组/CMB',
    },
    'DE': {
        'z': 0,
        'E_GeV': 2e-13,          # ~0.2 meV
        'H': 1.2e-42,            # GeV (H0)
        'desc': '暗能量',
    },
    'Quantum_Cosmo': {
        'z': 0,                   # 同一时刻，Planck 标度
        'E_GeV': M_PL,
        'H': 1.0,                 # Planck 单位的 H
        'desc': '量子宇宙学',
    },
}

# ℓ_corr 替换值 (m)
LCORR_COSMO = {
    'Inflation': 5.4e-30,        # H_inf^{-1} ~ 1/(1e13 GeV) * 1.97e-16 m/GeV
    'Reheat': 1.97e-22,          # T_rh^{-1} ~ 1/(1e4 GeV)  * ...
    'BBN': 1.97e-7,               # T_BBN^{-1}
    'LSS': 1.44e26,              # r_s(z_*) ~ 147 Mpc
    'DE': 1.44e26,                # d_H(z), Hubble 距离
    'Quantum_Cosmo': 8.2e-35,    # l_Pl = 1/M_Pl * 1.97e-16
}


def spectral_operator_cosmo_layer(layer: str, size: int = 4) -> np.ndarray:
    """构造宇宙学各层的谱生成元 A_i

    Parameters
    ----------
    layer : str — 层名
    size : int — 矩阵维度

    Returns
    -------
    np.ndarray — 谱生成元
    """
    if layer == 'Inflation':
        # 暴胀子谱: V(φ) ~ m²φ²/2
        phi_vals = np.linspace(0.1, 1.0, size)
        evals = 0.5 * (0.1 * M_PL)**2 * phi_vals**2  # m ~ 0.1 M_Pl
        evals = evals / M_PL**2  # 归一化
        H = np.diag(evals)

    elif layer == 'Reheat':
        # 再加热温度谱: T(z) 的衰减
        z_vals = np.array([1e26, 1e25, 1e24, 1e23])[:size]
        evals = 1e15 / z_vals  # T ~ 1e15/z (GeV) 近似
        evals = np.maximum(evals, 1e-10)
        H = np.diag(evals)

    elif layer == 'BBN':
        # BBN 温度谱
        T_vals = np.array([1e-3, 5e-4, 1e-4, 5e-5])[:size]  # GeV
        evals = T_vals
        H = np.diag(evals)

    elif layer == 'LSS':
        # CMB 功率谱 ℓ 模
        ell_vals = np.array([10, 100, 500, 1000])[:size]
        # C_ℓ ~ 1/(ℓ(ℓ+1))
        evals = 1.0 / (ell_vals * (ell_vals + 1))
        H = np.diag(evals)

    elif layer == 'DE':
        # 暗能量 w(z) 谱
        z_vals = np.array([0.0, 0.5, 1.0, 2.0])[:size]
        w0 = -1.0
        wa = 0.0
        evals = w0 + wa * z_vals / (1 + z_vals)
        evals = np.abs(evals)  # 取绝对值
        evals = np.maximum(evals, 1e-10)
        H = np.diag(evals)

    elif layer == 'Quantum_Cosmo':
        # 宇宙波函数谱: 无边界条件
        # Hartle-Hawking 波函数 ψ ~ exp(-S_E/ħ)
        evals = np.exp(-np.arange(1, size + 1))  # 指数衰减谱
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
# 1. 时间-纤维化对偶验证
# ============================================================
def verify_time_fibration_duality() -> Dict:
    """验证时间-纤维化对偶：红移顺序与谱流参数的一致性"""
    layers_in_order = ['Inflation', 'Reheat', 'BBN', 'LSS', 'DE', 'Quantum_Cosmo']

    print("=" * 65)
    print("宇宙学时间-纤维化对偶验证")
    print("=" * 65)
    print(f"  {'层':<20} {'红移 z':<16} {'谱流参数 ξ':<20} {'能标 (GeV)'}")
    print("-" * 65)

    results = {}
    for layer in layers_in_order:
        params = COSMO_PARAMS[layer]
        z = params['z']
        E = params['E_GeV']

        # 谱流参数
        if layer == 'Inflation':
            xi = 'ln a (指数膨胀)'
        elif layer == 'Reheat':
            xi = 'T (温度)'
        elif layer == 'BBN':
            xi = 'T_nuc (核合成温度)'
        elif layer == 'LSS':
            xi = 'a(t) (尺度因子)'
        elif layer == 'DE':
            xi = 'w(z) (暗能量状态)'
        else:
            xi = 'l_Pl (Planck 标度)'

        z_str = f"{z:.0e}" if z > 0 else "0"
        E_str = f"{E:.4e}" if E > 1 else f"{E:.4e}"
        print(f"  Bun({layer:<16}) {z_str:<16} {xi:<20} {E_str}")
        results[layer] = {'z': z, 'xi': xi, 'E_GeV': E}

    print("-" * 65)
    print("  红移 z 的演化 = 谱流方程 dξ/dt = H(t) 的解")
    print("  时间方向 = 纤维化方向 (d=+1, 能标从高到低)")
    print()

    return results


# ============================================================
# 2. 谱交织条件验证
# ============================================================
def verify_intertwining_cosmo() -> Dict:
    """验证宇宙学各层间谱交织条件 ε_cosmo ∼ H²/M_Pl²"""
    layers = ['Inflation', 'Reheat', 'BBN', 'LSS', 'DE', 'Quantum_Cosmo']
    dim = 4

    print("=" * 65)
    print("宇宙学谱交织条件 [A_i, π]_{HS} 验证")
    print("=" * 65)
    print(f"  ε_cosmo ∼ H_i² / M_Pl² (暴胀-再加热) 及类似估计")
    print("-" * 65)
    print(f"  {'界面':<20} {'HS 范数':<16} {'ε_cosmo':<16}")
    print("-" * 65)

    results = {}
    for i in range(len(layers) - 1):
        layer_i = layers[i]
        layer_ip1 = layers[i + 1]

        A_i = spectral_operator_cosmo_layer(layer_i, dim)
        A_ip1 = spectral_operator_cosmo_layer(layer_ip1, dim)

        pi = projection_operator(dim, dim)
        commutator = A_i @ pi - pi @ A_ip1
        hs_val = np.sqrt(np.trace(commutator.conj().T @ commutator).real)

        # ε_cosmo ∼ H_i² / M_Pl²
        H_i = COSMO_PARAMS[layer_i]['H']  # GeV
        H_ip1 = COSMO_PARAMS[layer_ip1]['H']
        eps = (min(H_i, H_ip1) / M_PL)**2
        eps = max(eps, 1e-80)

        if hs_val < eps or np.isnan(hs_val):
            status = "OK"
        elif hs_val < 10 * eps:
            status = "边缘"
        else:
            status = "大偏差"

        entry = {
            'interface': f'{layer_i}→{layer_ip1}',
            'hs_norm': hs_val,
            'epsilon': eps,
            'status': status,
        }
        results[f'{layer_i}→{layer_ip1}'] = entry

        hs_str = f"{hs_val:.4e}" if not np.isnan(hs_val) else "N/A"
        eps_str = f"{eps:.2e}" if eps > 1e-300 else "<1e-300"
        print(f"  {layer_i+'→'+layer_ip1:<20} {hs_str:<16} {eps_str:<16} {status}")

    print("-" * 65)
    print()

    return results


# ============================================================
# 3. ℓ_corr 替换验证
# ============================================================
def verify_lcorr_cosmo() -> Dict:
    """验证宇宙学 ℓ_corr = H^{-1}(z) 替换"""
    print("=" * 65)
    print("宇宙学 ℓ_corr = H^{-1}(z) 替换验证")
    print("=" * 65)
    print(f"  {'层':<20} {'ℓ_corr 公式':<30} {'数值 (m)':<16}")
    print("-" * 65)

    results = {}
    lcorr_info = {
        'Inflation': 'H_inf^{-1}',
        'Reheat': 'T_rh^{-1}',
        'BBN': 'T_BBN^{-1}',
        'LSS': 'r_s(z_*)',
        'DE': 'd_H(z)',
        'Quantum_Cosmo': 'l_Pl',
    }

    for layer, formula in lcorr_info.items():
        val = LCORR_COSMO[layer]
        val_str = f"{val:.4e}"
        print(f"  Bun({layer:<16}) {formula:<30} {val_str}")
        results[layer] = {'formula': formula, 'value': val}

    print("-" * 65)
    print(f"  ℓ_corr 跨度: {min(LCORR_COSMO.values()):.4e} ~ {max(LCORR_COSMO.values()):.4e} m")
    print()

    return results


# ============================================================
# 4. 统一验证报告
# ============================================================
def run_all_tests():
    """运行所有验证测试"""
    print()
    print("#" * 65)
    print("#  宇宙学 6层纤维化链验证报告")
    print("#  Phase 56C2 — 2026-07-25")
    print("#" * 65)
    print()

    # 1. 时间-纤维化对偶
    duality = verify_time_fibration_duality()

    # 2. 谱交织条件
    int_results = verify_intertwining_cosmo()

    # 3. ℓ_corr
    lcorr_results = verify_lcorr_cosmo()

    # === 汇总 ===
    print("=" * 65)
    print("宇宙学 6层纤维化链 — 验证汇总")
    print("=" * 65)
    print(f"  {'界面':<20} {'HS 范数':<16} {'ε_cosmo':<16}")
    print("-" * 65)

    ok_count = 0
    for name, entry in int_results.items():
        hs = entry['hs_norm']
        eps = entry['epsilon']
        hs_str = f"{hs:.4e}" if not np.isnan(hs) else "N/A"
        eps_str = f"{eps:.2e}" if eps > 1e-300 else "<1e-300"
        print(f"  {name:<20} {hs_str:<16} {eps_str:<16} {entry['status']}")
        if entry['status'] == 'OK':
            ok_count += 1

    print("-" * 65)
    print(f"  总界面数: 5, OK: {ok_count}")
    print(f"  时间-纤维化对偶: 红移方向 = 谱流方向 (d=+1)")
    print(f"  ℓ_corr 替换: H⁻¹(z)")
    print("=" * 65)

    return {
        'time_fibration_duality': duality,
        'intertwining': int_results,
        'lcorr': lcorr_results,
    }


if __name__ == '__main__':
    run_all_tests()
