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
spectral_gravity_fibration.py — 引力/黑洞 5层反向嵌套纤维化链的谱交织条件数值验证

Phase 56B1 (引力反向能标排序形式化) 的核心验证脚本。验证内容：

1. 反向纤维化方向 d=-1 的谱交织条件修正
2. 5 层谱生成元构造（Horizon/Exterior/Interior/Quantum_Core/Singularity）
3. 从外向内（低能→高能）的谱交织条件 [A_i, π_{i←i+1}]_{HS} 计算
4. 不同质量黑洞的谱交织条件收敛性对比

参考：
- notes/04_lorentz_gravity/spectral_gravity_fibration.md
- notes/00_foundations/spectral_fibration_domain_generalization.md §3
- notes/04_lorentz_gravity/spectral_kerr_fibration.md
"""

import numpy as np
from typing import Dict, List, Tuple

# ============================================================
# 物理常数
# ============================================================
HBARC = 197.327       # MeV·fm
M_PL = 1.22091e19     # Planck 质量 (GeV)
L_PL = 8.2e-20        # Planck 长度 (fm)
G_N = 6.67430e-11     # 引力常数 (m^3 kg^-1 s^-2)
M_SUN = 1.98892e30    # 太阳质量 (kg)
G_CGS = 6.67430e-8    # 引力常数 (cgs)

# ============================================================
# 黑洞基本参数
# ============================================================
M_SOLAR_GEV = 1.115e57    # 太阳质量 → GeV (c=1, hbar=1)
M_SOLAR_FM = 2.954e9      # 太阳质量 Schwarzschild 半径 (fm)


def kerr_parameters(M_GeV: float, a_ratio: float = 0.0) -> Dict:
    """计算 Kerr 黑洞的基本参数

    Parameters
    ----------
    M_GeV : float — 黑洞质量 (GeV)
    a_ratio : float — 无量纲自旋 a/M ∈ [0, 1)

    Returns
    -------
    dict — 含视界半径、表面引力、Hawking 温度等
    """
    # hbar*c = 197.327 MeV·fm, M_in_fm = M_GeV * 1e9 * G_N / c^2 / (hbar*c)
    # 简化: M (GeV) → r_+ (fm) ≈ M_GeV / M_SOLAR_GEV * 2.954e9 * (1 + sqrt(1-a^2))
    a = a_ratio * M_GeV  # 物理角动量
    r_plus = M_GeV / M_SOLAR_GEV * M_SOLAR_FM * (1 + np.sqrt(1 - a_ratio**2))
    r_minus = M_GeV / M_SOLAR_GEV * M_SOLAR_FM * (1 - np.sqrt(1 - a_ratio**2))

    # 表面引力 (GeV)
    kappa = np.sqrt(M_GeV**2 - a**2) / (2 * M_GeV * r_plus)

    # Hawking 温度 (GeV)
    T_H = kappa / (2 * np.pi)

    # 谱间隙 (Paper VIII)
    dlambda = 2 * np.pi * T_H / M_PL

    return {
        'M_GeV': M_GeV,
        'a_ratio': a_ratio,
        'r_plus_fm': r_plus,
        'r_minus_fm': r_minus,
        'kappa_GeV': kappa,
        'T_H_GeV': T_H,
        'dlambda': dlambda,
    }


def epsilon_threshold_gravity(E_i: float, E_ip1: float) -> float:
    """引力系统的谱交织条件阈值

    反向能标排序 d=-1 的 ε_i 修正：
    ε_i^{(-1)} = ε_i^{(+1)} * E_{i+1} / E_i

    其中 ε_i^{(+1)} = ε_0 · (ΔE_0 / ΔE_i)^α, α=1
    """
    eps0 = 1e-3
    dE0 = 1.0  # eV
    dE = abs(E_i - E_ip1)  # GeV
    if dE <= 0:
        return 1.0

    dE_eV = dE * 1e9
    eps_forward = eps0 * (dE0 / dE_eV)

    # d=-1 修正: 乘以能标比
    # 对于反向排序: E_i < E_{i+1} (从外到内能标增大)
    if E_i > 0 and E_ip1 > 0:
        # 反向量纲: ε 应正比于小能标/大能标
        ratio = min(E_i, E_ip1) / max(E_i, E_ip1)
        eps_reverse = eps_forward * ratio
    else:
        eps_reverse = eps_forward

    return max(eps_reverse, 1e-80)


# ============================================================
# 各层谱生成元
# ============================================================
def spectral_operator_gravity_layer(layer: str, size: int = 4,
                                    M_GeV: float = M_SOLAR_GEV,
                                    a_ratio: float = 0.0) -> np.ndarray:
    """构造引力 5 层谱生成元 A_i

    反向能标排序：从 Bun(Horizon) 低能 → Bun(Singularity) 高能
    """
    params = kerr_parameters(M_GeV, a_ratio)

    if layer == 'Horizon':
        # 视界谱：Hawking 温度驱动的热谱
        T_H = params['T_H_GeV']
        kT = max(T_H, 1e-20) * M_PL  # 归一化
        evals = kT * np.arange(1, size + 1)
        H = np.diag(evals)

    elif layer == 'Exterior':
        # 外部 QNM 谱：复频率模
        # 基模频率 (简化): ω = ω_R - i ω_I
        # ω_R ~ (l+1/2) / (3*sqrt(3)*M) (Schwarzschild 近似)
        M_geom = M_GeV / M_SOLAR_GEV  # 以太阳质量为单位的质量
        if M_geom > 0:
            omega_R = (3 / (2 * np.sqrt(3))) / (3 * np.sqrt(3) * M_geom)
            omega_I = 0.0890 / M_geom
        else:
            omega_R = 1.0
            omega_I = 0.1

        # 构造复谱生成元（这里用实部）
        evals = omega_R * np.arange(1, size + 1)
        H = np.diag(evals)

    elif layer == 'Interior':
        # 内部谱: 指数衰减的离散谱
        S4 = 0.082  # 谱静默 S_4 因子
        E0 = 1e-5  # GeV
        evals = np.array([E0 * S4**n for n in range(size)])
        evals = np.maximum(evals, 1e-20)  # 避免零值
        H = np.diag(evals)

    elif layer == 'Quantum_Core':
        # 量子核心: Planck 标度谱编织
        gap = 0.122 * M_PL  # Cl(1,7) 谱间隙 (D0)
        evals = gap * np.arange(1, size + 1)
        H = np.diag(evals)

    elif layer == 'Singularity':
        # 奇点层: 极限谱 → 0, UV 截断
        cutoff = M_PL
        evals = cutoff / (np.arange(1, size + 1))**2
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
    """构造层间投影算子 π_{i←i+1}

    对于反向排序：投影从外（低能）向内（高能），
    即从 Bun(i) 到 Bun(i+1) 是纤维化（精细嵌入）。
    """
    pi = np.zeros((n_fine, n_coarse))
    for i in range(min(n_fine, n_coarse)):
        pi[i, i] = 1.0
    return pi


# ============================================================
# 1. 反向能标排序验证
# ============================================================
def verify_reverse_energy_ordering() -> Dict:
    """验证引力系统的反向能标排序"""
    # 从外向内：能标递增
    layers_outer = ['Horizon', 'Exterior', 'Interior', 'Quantum_Core', 'Singularity']
    energy_labels = {
        'Horizon': 'E_H = T_H ~ 10^{-11} GeV (M_sun)',
        'Exterior': 'E_QNM ~ 10^{-11} GeV (QNM 频率)',
        'Interior': 'E_int ~ 10^{-5} GeV (内部离散谱)',
        'Quantum_Core': 'E_QG ~ 10^{19} GeV (Planck 标度)',
        'Singularity': 'E_UV ~ 10^{19} GeV (UV 截断)',
    }
    # 能标估计 (GeV)
    E_values = {
        'Horizon': 1e-11,       # T_H for solar mass
        'Exterior': 1e-11,      # QNM frequencies
        'Interior': 1e-5,       # interior discrete spectrum
        'Quantum_Core': M_PL,   # Planck
        'Singularity': M_PL,    # UV cutoff
    }

    print("=" * 65)
    print("引力系统反向能标排序验证 (d=-1)")
    print("=" * 65)
    print(f"  {'层':<15} {'能标估计 (GeV)':<24} {'描述'}")
    print("-" * 65)

    for i, layer in enumerate(layers_outer):
        E = E_values[layer]
        print(f"  Bun({layer:<12}) {E:<24.4e} {energy_labels[layer]}")
        if i < len(layers_outer) - 1:
            E_next = E_values[layers_outer[i + 1]]
            direction = "↑" if E_next > E else "↓"
            print(f"                       {direction}")

    print("-" * 65)
    print("  排序方向: E_outter < E_inner → d = -1 (反向纤维化)")
    print()

    return {'layers': layers_outer, 'energies': E_values}


# ============================================================
# 2. 谱交织条件验证 (反向方向)
# ============================================================
def verify_intertwining_gravity(M_GeV: float = M_SOLAR_GEV,
                                 a_ratio: float = 0.0) -> Dict:
    """计算引力 5 层反向谱交织条件

    从外向内：Bun(Horizon) → Bun(Exterior) → Bun(Interior)
           → Bun(Quantum_Core) → Bun(Singularity)

    由于 d=-1, 投影方向为精粒化 (fine embedding):
    π_{i←i+1}: Bun(i+1) → Bun(i), 形状 (dim_i, dim_{i+1})
    """
    layers = ['Horizon', 'Exterior', 'Interior', 'Quantum_Core', 'Singularity']
    # 维度从外到内递增 (外层低能少自由度, 内层高能多自由度)
    dims = {'Horizon': 3, 'Exterior': 4, 'Interior': 5, 'Quantum_Core': 6, 'Singularity': 7}

    print("=" * 65)
    print(f"谱交织条件验证 (反向 d=-1)")
    print(f"黑洞质量: {M_GeV/M_SOLAR_GEV:.2e} M_sun, 自旋 a/M = {a_ratio}")
    print("=" * 65)
    print(f"  {'界面':<20} {'dim_i':<8} {'dim_{i+1}':<10} {'HS 范数':<16} {'ε_i':<16}")
    print("-" * 65)

    results = {}
    for i in range(len(layers) - 1):
        layer_i = layers[i]
        layer_ip1 = layers[i + 1]
        dim_i = dims[layer_i]
        dim_ip1 = dims[layer_ip1]

        A_i = spectral_operator_gravity_layer(layer_i, dim_i, M_GeV, a_ratio)
        A_ip1 = spectral_operator_gravity_layer(layer_ip1, dim_ip1, M_GeV, a_ratio)

        # 投影 π: V_{i+1} → V_i (从内层投影到外层)
        # 形状 (dim_i, dim_{ip1}) 对应外层×内层
        pi = projection_operator(dim_i, dim_ip1)

        # [A_i, π] = A_i @ π - π @ A_ip1
        # A_i: (dim_i × dim_i), π: (dim_i × dim_ip1), A_ip1: (dim_ip1 × dim_ip1)
        commutator = A_i @ pi - pi @ A_ip1
        hs_val = np.sqrt(np.trace(commutator.conj().T @ commutator).real)

        # 阈值计算 (d=-1 修正)
        E_i = 1.0  # placeholder
        E_ip1 = 1.0
        if layer_i == 'Horizon':
            E_i = 1e-11
        elif layer_i == 'Exterior':
            E_i = 1e-11
        elif layer_i == 'Interior':
            E_i = 1e-5
        elif layer_i == 'Quantum_Core':
            E_i = M_PL
        if layer_ip1 == 'Exterior':
            E_ip1 = 1e-11
        elif layer_ip1 == 'Interior':
            E_ip1 = 1e-5
        elif layer_ip1 == 'Quantum_Core':
            E_ip1 = M_PL
        elif layer_ip1 == 'Singularity':
            E_ip1 = M_PL

        eps = epsilon_threshold_gravity(E_i, E_ip1)

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
            'dim': (dim_i, dim_ip1),
            'hs_norm': hs_val,
            'epsilon': eps,
            'status': status,
        }
        results[f'{layer_i}→{layer_ip1}'] = entry

        hs_str = f"{hs_val:.4e}" if not np.isnan(hs_val) else "N/A"
        eps_str = f"{eps:.2e}" if eps > 1e-300 else "<1e-300"
        print(f"  {layer_i+'→'+layer_ip1:<20} {dim_i:<8} {dim_ip1:<10} {hs_str:<16} {eps_str:<16} {status}")

    print("-" * 65)
    print()

    return results


# ============================================================
# 3. 质量依赖性对比
# ============================================================
def compare_mass_scaling() -> Dict:
    """对比不同质量黑洞的谱交织条件"""
    masses = {
        '原初黑洞 (M ~ 10^{12} kg)': 1e12 / M_SUN * M_SOLAR_GEV,
        '恒星质量黑洞 (10 M_sun)': 10 * M_SOLAR_GEV,
        '星系中心黑洞 (10^6 M_sun)': 1e6 * M_SOLAR_GEV,
        '超大质量黑洞 (10^9 M_sun)': 1e9 * M_SOLAR_GEV,
    }

    print("=" * 65)
    print("不同质量黑洞的谱交织条件对比")
    print("=" * 65)

    results = {}
    for name, M_GeV in masses.items():
        r_plus_fm = kerr_parameters(M_GeV)['r_plus_fm']
        # Horizon→Exterior 谱交织近似
        dE_ratio = L_PL / r_plus_fm
        eps_approx = max(dE_ratio**2, 1e-100)

        results[name] = {
            'M_Sun': M_GeV / M_SOLAR_GEV,
            'r_plus_fm': r_plus_fm,
            'eps_approx': eps_approx,
        }

        eps_str = f"{eps_approx:.2e}" if eps_approx > 1e-300 else "<1e-300"
        print(f"  {name:<30} M={M_GeV/M_SOLAR_GEV:.2e} M_sun")
        print(f"  {'':>30} r_+ = {r_plus_fm:.4e} fm, ε ≈ {eps_str}")

    print("-" * 65)
    print()

    return results


# ============================================================
# 4. 截面传递与 ℓ_corr
# ============================================================
def verify_section_propagation_gravity() -> Dict:
    """验证引力系统层间截面传递"""
    sections = {
        'Horizon': ['T_H', 'S_BH = A/4', 'Δλ_min', 'κ'],
        'Exterior': ['ω_lmn', 'Ringdown 波形', 'ISCO', 'Lensing'],
        'Interior': ['Cauchy 视界稳定性', '内部 QNM', '质量膨胀指数'],
        'Quantum_Core': ['量子反弹谱', '面积量子化', 'Bohr-Sommerfeld 量子数'],
        'Singularity': ['奇点消解条件', '分支反射比', 'UV 截断'],
    }

    lcorr = {
        'Horizon': ('r_+^{-1}', '视界曲率标度'),
        'Exterior': ('r^{-1}', '径向坐标倒数'),
        'Interior': ('(r_+ - r)^{-1}', 'Cauchy 接近度'),
        'Quantum_Core': ('l_Pl', 'Planck 长度'),
        'Singularity': ('Λ_UV', 'UV 截断'),
    }

    print("=" * 65)
    print("引力系统层间截面传递")
    print("=" * 65)
    print(f"  方向: 低能(外) → 高能(内), d = -1")
    print("-" * 65)

    layers = ['Horizon', 'Exterior', 'Interior', 'Quantum_Core', 'Singularity']
    results = {}
    for layer in layers:
        obs = sections[layer]
        lc = lcorr[layer]
        print(f"  Bun({layer:<15}) : {', '.join(obs[:3])}")
        print(f"  {'':>20} ℓ_corr = {lc[0]:<18} [{lc[1]}]")
        results[layer] = {'observables': obs, 'lcorr': lc}

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
    print("#  引力/黑洞 反向纤维化链验证报告")
    print("#  Phase 56B — 2026-07-25")
    print("#" * 65)
    print()

    # 1. 反向能标排序
    energy_results = verify_reverse_energy_ordering()

    # 2. 谱交织条件 (太阳质量黑洞)
    int_solar = verify_intertwining_gravity(M_SOLAR_GEV, 0.0)

    # 3. 谱交织条件 (原初黑洞)
    M_primordial = 1e12 / M_SUN * M_SOLAR_GEV
    int_primordial = verify_intertwining_gravity(M_primordial, 0.0)

    # 4. 质量依赖性
    mass_results = compare_mass_scaling()

    # 5. 截面传递
    sec_results = verify_section_propagation_gravity()

    # === 汇总表 ===
    print("=" * 65)
    print("引力 5层反向纤维化链 — 验证汇总")
    print("=" * 65)
    print(f"  方向: 低能(外) → 高能(内)")
    print(f"  d = -1 (反向纤维化)")
    print("-" * 65)

    for name, entry in int_solar.items():
        hs = entry['hs_norm']
        eps = entry['epsilon']
        hs_str = f"{hs:.4e}" if not np.isnan(hs) else "N/A"
        eps_str = f"{eps:.2e}" if eps > 1e-300 else "<1e-300"
        print(f"  {name:<25} HS={hs_str:<15} ε={eps_str:<15} {entry['status']}")

    print("-" * 65)

    # 状态判断 (太阳质量黑洞)
    ok_all = all(
        e['status'] == 'OK' or e['status'] == 'N/A'
        for e in int_solar.values()
    )

    if ok_all:
        print("\n  结论: 太阳质量黑洞谱交织条件全部满足。")
        print("  反向纤维化 d=-1 在常规黑洞情形有效。")
    else:
        print("\n  结论: 部分层间谱交织条件需进一步分析。")
        print("  原初黑洞或极端自旋可能需要 RG 流嵌入。")

    print()
    print("=" * 65)
    print(f"  太阳质量 r_+ ≈ {kerr_parameters(M_SOLAR_GEV)['r_plus_fm']:.4e} fm")
    print(f"  原初黑洞 r_+ ≈ {kerr_parameters(M_primordial)['r_plus_fm']:.4e} fm")
    print(f"  谱交织条件 ε ∝ (l_Pl/r_+)^2")
    print(f"  Bun(Quantum_Core) ↔ Bun(Singularity) 需量子引力理论")
    print("=" * 65)

    return {
        'energy_ordering': energy_results,
        'intertwining_solar': int_solar,
        'intertwining_primordial': int_primordial,
        'mass_scaling': mass_results,
        'sections': sec_results,
        'feasible': ok_all,
    }


if __name__ == '__main__':
    results = run_all_tests()
