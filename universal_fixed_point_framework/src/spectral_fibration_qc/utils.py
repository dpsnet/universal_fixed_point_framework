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
utils.py — 谱纤维拆分包工具函数
==================================
提供数值类型转换、谱间隙计算等通用工具。
"""

import numpy as np

# ── 物理常数 ──
k_B_eV = 8.617333262e-5   # Boltzmann 常数 [eV/K]
k_B_J = 1.380649e-23       # Boltzmann 常数 [J/K]
h_Js = 6.62607015e-34      # Planck 常数 [J·s]
hbar_eV_s = 6.582119569e-16  # 约化 Planck 常数 [eV·s]
eV_to_cm1 = 8065.54        # eV → cm⁻¹ 换算因子
R_gas = 8.314462618         # 气体常数 [J/mol/K]
L_CORR_DEFAULT = 0.5        # 默认 ℓ_corr [Å]


def convert_numpy(obj):
    """将 numpy 类型递归转换为 Python 原生类型（JSON 序列化兼容）。

    Parameters
    ----------
    obj : any
        输入对象，可为 numpy 标量、数组、嵌套 dict/list。

    Returns
    -------
    any
        Python 原生类型的等效对象。
    """
    if isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy(v) for v in obj]
    return obj


def spectral_gap_from_eigenvalues(eigvals):
    """从本征值列表计算 HOMO-LUMO 谱间隙。

    对一组排序后的本征值：
      - 若为偶数个：δ_spec = E_{N/2+1} - E_{N/2}
      - 若为奇数个：δ_spec = E_{(N+1)/2} - E_{(N-1)/2}

    Parameters
    ----------
    eigvals : ndarray
        已排序的本征值数组（升序）。

    Returns
    -------
    delta_spec : float
        HOMO-LUMO 间隙 [eV]。
    """
    eigvals = np.sort(np.asarray(eigvals, dtype=float))
    n = len(eigvals)
    if n < 2:
        return 0.0
    homo_idx = n // 2 - 1 if n % 2 == 0 else (n - 1) // 2
    lumo_idx = n // 2 if n % 2 == 0 else (n + 1) // 2
    return float(eigvals[lumo_idx] - eigvals[homo_idx])


def hopping_beta(R, beta0, R0=1.5, l_corr=L_CORR_DEFAULT):
    """随距离指数衰减的跳跃积分。

    β(R) = β₀ · exp(-(R - R₀) / ℓ_corr)

    Parameters
    ----------
    R : float
        当前距离 [Å]。
    beta0 : float
        参考距离处的耦合强度 [eV]。
    R0 : float
        参考距离 [Å]，默认 1.5。
    l_corr : float
        关联长度 [Å]，默认 0.5。

    Returns
    -------
    beta : float
        跳跃积分 [eV]。
    """
    if R < 0.3:
        R = 0.3
    return beta0 * np.exp(-(R - R0) / l_corr)


def gaussian_broaden(energies, weights, x_grid, sigma=0.05):
    """对离散谱进行高斯展宽。

    Parameters
    ----------
    energies : ndarray
        离散能级 [eV]。
    weights : ndarray
        各能级的权重（如振子强度）。
    x_grid : ndarray
        输出能量网格 [eV]。
    sigma : float
        高斯展宽宽度 [eV]，默认 0.05。

    Returns
    -------
    spectrum : ndarray
        展宽后的谱密度。
    """
    spectrum = np.zeros_like(x_grid)
    for E, w in zip(energies, weights):
        spectrum += w * np.exp(-0.5 * ((x_grid - E) / sigma) ** 2)
    spectrum /= np.sqrt(2 * np.pi) * sigma
    return spectrum
