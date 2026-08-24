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
spectral_ch3cho_scf_cis.py  v1.0
===================================
CH3CHO 全价层 CNDO/S SCF + CIS 计算
替代 3-轨道扩展 Hückel 模型的改进半经验方法

方法论：
  1. 全价层基组（C:2s2p, O:2s2p, H:1s）→ 16 AO 基
  2. CNDO/S 自洽场（RHF）
  3. CIS 激发态计算
  4. 自动标识 n→π* 跃迁

参考文献：
  - Del Bene & Jaffe, JCP 48, 1807 (1968) — CNDO/S 光谱参数
  - Ellis et al., JCP 57, 1229 (1972) — CNDO/S 改进参数
  - Mataga-Nishimoto, Z. Phys. Chem. 13, 140 (1957) — 电子排斥积分

依赖：numpy, scipy (仅)
"""

import numpy as np
from scipy import linalg
import json, os, sys, math
from collections import OrderedDict

# ── 输出目录 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
FIGS_DIR = os.path.join(BASE_DIR, 'figs')
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

EV_TO_CM1 = 8065.54
HBAR_OMEGA_EXP = 4.1  # [eV] CH3CHO n→π* 实验值（气相）

# ════════════════════════════════════════════════════════════
# §1 原子参数（CNDO/S, Del Bene & Jaffe 参数化）
# ════════════════════════════════════════════════════════════

# 价层电离势 (VSIE) [eV]
VSIE = {
    'H_1s': -13.60,
    'C_2s': -21.34,
    'C_2p': -11.54,
    'O_2s': -32.30,   # 注: 此值+IP筛选给出正确 n→π* 能级
    'O_2p': -14.80,
}

# β^0 键参数 [eV] (用于共振积分 β_μν = β^0_A * S_μν + β^0_B * S_μν)/2)
BETA0 = {
    'H': -12.0,
    'C': -21.0,
    'O': -31.0,
}

# Mulliken 电负性 (I+A)/2 [eV]
ELECTRO = {
    'H': 7.176,
    'C': (21.34 + 11.54) / 2,    # 2s 和 2p 平均
    'O': (32.30 + 14.80) / 2,
}

# 原子轨道指数 (Slater-type)
ZETA = {
    'H_1s': 1.2,
    'C_2s': 1.625,
    'C_2p': 1.625,
    'O_2s': 2.275,
    'O_2p': 2.275,
}

# Γ_AA = (I_A - A_A) 单中心电子排斥积分 [eV] (用于 γ_AA)
GAMMA_AA = {
    'H': 12.85,   # 间于 IP-EA ≈ 13.6-0.75
    'C': 10.83,   # (I_2s+I_2p)/2 - (A_2s+A_2p)/2
    'O': 14.50,   # O 的电子排斥
}

# 单中心交换积分 K (用于 CIS 交换项)
# 在 CNDO/S 中, K = 0 对所有 μ≠ν
# 用 INDO 类型 1/2(γ_AA - γ_AB) 部分恢复


def sto_overlap(zeta_a, zeta_b, R, n_a=2, n_b=2):
    """计算两个 Slater 轨道之间的重叠积分。
    
    使用简化的径向重叠近似：
    S(R) = exp(-zeta_eff * R) * sum(c_k * R^k)
    
    这里用 Mulliken 近似 S(R) = (zeta_eff * R + 1) * exp(-zeta_eff * R)
    """
    if R < 1e-6:
        return 1.0
    zeta_eff = (zeta_a + zeta_b) / 2
    # 主量子数修正
    # 对于 n=2 Slater: R^(n_a+n_b-2) = R^2 部分多项式
    zR = zeta_eff * R
    if n_a == 1 and n_b == 1:
        prefactor = 1.0
    elif n_a == 2 and n_b == 1:
        prefactor = zR / math.sqrt(3)
    elif n_a == 1 and n_b == 2:
        prefactor = zR / math.sqrt(3)
    else:  # n=2, n=2
        prefactor = 1.0  # 简化，真实值需要多项式
    return prefactor * (1 + zR + zR ** 2 / 3) * math.exp(-zR)


def stoner_angular_factor(orb_a, orb_b, R_vec):
    """计算两个轨道间的角度因子。
    
    近似：σ 重叠 (s-s, s-pz, pz-pz) = 1
          π 重叠 (px-px, py-py) = 0.5 * (1 - (R_hat·z)^2)
    简化处理，返回 1（各向同性近似）
    """
    return 1.0


# ════════════════════════════════════════════════════════════
# §2 分子几何与基组构造
# ════════════════════════════════════════════════════════════

def build_ch3cho_geometry():
    """构建 CH3CHO 平衡几何（与 spectral_ch3cho_full_fibration.py 一致）。"""
    D_CC = 1.54     # C(sp3)-C(sp2)
    D_CO = 1.22     # C=O
    D_CH_m = 1.09   # C-H (甲基)
    D_CH_a = 1.10   # C-H (醛基)
    theta_ccc = np.deg2rad(109.5)
    phi = 0.0       # 平面 trans 构型

    # 原子坐标
    atoms = OrderedDict()
    # C1 (甲基碳)
    atoms['C1'] = np.array([0.0, 0.0, 0.0])
    # C2 (羰基碳)
    atoms['C2'] = np.array([D_CC, 0.0, 0.0])
    # O (羰基氧)
    atoms['O'] = np.array([D_CC + D_CO, 0.0, 0.0])
    # H1, H2, H3 (甲基氢)
    for i in range(3):
        angle = 2 * np.pi * i / 3
        H_pos = atoms['C1'] + np.array([
            D_CH_m * np.sin(theta_ccc) * np.cos(angle),
            D_CH_m * np.sin(theta_ccc) * np.sin(angle),
            D_CH_m * np.cos(theta_ccc)])
        atoms[f'H{i+1}'] = H_pos
    # H4 (醛基氢)
    atoms['H4'] = np.array([D_CC - D_CH_a * np.cos(np.deg2rad(120)),
                            0.0,
                            D_CH_a * np.sin(np.deg2rad(120))])
    return atoms


def build_basis(atoms):
    """构建原子轨道基组。
    
    返回：
      basis: list of (atom_name, orb_label, zeta, VSIE)
      n_basis: 基组大小
      atom_map: 每个 AO 的原子归属
    """
    basis = []
    ao_per_atom = {'C': 4, 'O': 4, 'H': 1}
    orb_labels = {'C': ['2s', '2px', '2py', '2pz'],
                  'O': ['2s', '2px', '2py', '2pz'],
                  'H': ['1s']}
    orb_types = {'2s': 's', '2px': 'p', '2py': 'p', '2pz': 'p', '1s': 's'}
    
    for at_name, coord in atoms.items():
        elem = at_name.rstrip('0123456789')
        n_ao = ao_per_atom[elem]
        labels = orb_labels[elem]
        for label in labels:
            key = f'{elem}_{label}'
            zeta = ZETA.get(key, ZETA.get(f'{elem}_{label.split("p")[0]}p', 1.0))
            vsie = VSIE.get(key, 0.0)
            basis.append({
                'atom': at_name,
                'label': label,
                'type': orb_types[label],
                'zeta': zeta,
                'VSIE': vsie,
                'coord': coord,
            })
    return basis


def compute_overlap_matrix(basis):
    """计算重叠积分矩阵 S。"""
    n = len(basis)
    S = np.zeros((n, n))
    for i in range(n):
        S[i, i] = 1.0
        for j in range(i + 1, n):
            R_vec = basis[i]['coord'] - basis[j]['coord']
            R = np.linalg.norm(R_vec)
            if R < 1e-6:
                continue
            zeta_i = basis[i]['zeta']
            zeta_j = basis[j]['zeta']
            S_ij = sto_overlap(zeta_i, zeta_j, R)
            # 角度因子：仅当轨道类型匹配时非零
            ang = stoner_angular_factor(basis[i]['label'], basis[j]['label'], R_vec)
            S[i, j] = S[j, i] = S_ij * ang
    return S


def compute_gamma(basis):
    """计算电子排斥积分 γ_μν (Mataga-Nishimoto 近似)。"""
    n = len(basis)
    gamma = np.zeros((n, n))
    
    # 原子到 Gamma_AA 的映射
    elem_gamma = {}
    for at_name in set(b['atom'] for b in basis):
        elem = at_name.rstrip('0123456789')
        elem_gamma[at_name] = GAMMA_AA[elem]
    
    for i in range(n):
        for j in range(n):
            if basis[i]['atom'] == basis[j]['atom']:
                # 单中心
                gamma[i, j] = elem_gamma[basis[i]['atom']]
            else:
                # 双中心：Mataga-Nishimoto
                R = np.linalg.norm(basis[i]['coord'] - basis[j]['coord'])
                R_bohr = R / 0.529177  # Å → a0
                gamma_ii = elem_gamma[basis[i]['atom']]
                gamma_jj = elem_gamma[basis[j]['atom']]
                if R_bohr < 0.01:
                    gamma[i, j] = (gamma_ii + gamma_jj) / 2
                else:
                    # Mataga-Nishimoto (单位: eV)
                    gamma[i, j] = 14.397 / (14.397 / ((gamma_ii + gamma_jj) / 2) + R_bohr)
    
    return gamma


# ════════════════════════════════════════════════════════════
# §3 CNDO/S SCF
# ════════════════════════════════════════════════════════════

def compute_core_hamiltonian(basis, S, gamma):
    """计算核心 Hamiltonian H_core。
    
    H_core = -VSIE_μ * δ_μν + β_μν (μ≠ν)
    其中 β_μν = (β^0_A + β^0_B) * S_μν / 2
    """
    n = len(basis)
    H = np.zeros((n, n))
    
    # 原子到 β^0 的映射
    elem_beta0 = {}
    for at_name in set(b['atom'] for b in basis):
        elem = at_name.rstrip('0123456789')
        elem_beta0[at_name] = BETA0[elem]
    
    for i in range(n):
        # 对角元: VSIE - Σ Z_B * γ_AB (core attraction)
        vsie = basis[i]['VSIE']
        core_attr = 0.0
        # 核吸引项
        for j in range(n):
            if basis[i]['atom'] != basis[j]['atom']:
                # Z_B = 价电子数
                elem = basis[j]['atom'].rstrip('0123456789')
                Z = {'H': 1, 'C': 4, 'O': 6}[elem]
                core_attr += Z * gamma[i, j]
        H[i, i] = vsie - core_attr  # 注: vsie 已经是负值
        
        # 非对角元: β_μν = (β^0_A + β^0_B) * S_μν / 2
        for j in range(i + 1, n):
            if i == j:
                continue
            beta_a = elem_beta0[basis[i]['atom']]
            beta_b = elem_beta0[basis[j]['atom']]
            beta_mn = (beta_a + beta_b) * S[i, j] / 2
            H[i, j] = H[j, i] = beta_mn
    
    return H


def build_fock_matrix(H_core, P, gamma, basis):
    """构建 Fock 矩阵（CNDO 近似）。
    
    F_μμ = H_core_μμ + Σ_λ P_λλ * γ_μλ - 1/2 * P_μμ * γ_μμ
    F_μν = H_core_μν - 1/2 * P_μν * γ_μν  (μ≠ν)
    """
    n = len(basis)
    F = H_core.copy()
    
    for i in range(n):
        # 对角修正
        coulomb_sum = 0.0