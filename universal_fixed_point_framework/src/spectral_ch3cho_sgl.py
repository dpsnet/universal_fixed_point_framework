"""
spectral_ch3cho_sgl.py
=======================
P3: CH3CHO SGL（Spectral Gap Landscape）隐式通道扫描
寻找 δ_spec（HOMO-LUMO 谱间隙）极小 vs PES 鞍点偏差

方法：扩展 Hückel 模型扫描 CH3CHO 的：
  - φ: C-C 扭转角 (0-180°)
  - θ: CHO 面外弯曲 (0-60°)
  
预言：δ_spec 极小位置可能与 PES 鞍点有偏差 → 隐式反应通道
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS_DIR = os.path.join(SCRIPT_DIR, '..', 'figs')
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
os.makedirs(FIGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ── CH3CHO 简化的扩展 Hückel 模型 ──
# 有效轨道: 
#   C1(sp³) C2(sp²) =O(pπ) H1s × 3(甲基) + H1s(醛基)
# 简化为每个重原子贡献 1 个有效价轨道

# 轨道能 (VSIE)
ALPHA_C = -11.4   # [eV] C 2p
ALPHA_O = -12.2   # [eV] O 2p
ALPHA_H = -13.6   # [eV] H 1s

# 跳跃积分参数
BETA_CC = -2.5    # [eV] C-C σ
BETA_CO = -3.0    # [eV] C=O π
BETA_CH = -4.0    # [eV] C-H σ
BETA_CD = -1.0    # [eV] 非键角依赖耦合因子

# ℓ_corr 参数（谱框架）
L_CORR = 0.5      # [Å]

def hopping_beta(R, beta0, R0=1.5):
    """随距离指数衰减的跳跃积分。"""
    if R < 0.5: R = 0.5
    return beta0 * np.exp(-(R - R0) / L_CORR)

def ch3cho_geometry(phi, theta):
    """
    构建 CH3CHO 原子坐标。
    phi:  C-C 扭转角 (rad), 0=cis, π=trans  
    theta: CHO 面外弯曲角 (rad)
    
    简化的 3-重原子模型: CH3—C(rot)—O
    """
    # 键长参数 [Å]
    d_CC = 1.54   # C(sp³)-C(sp²)
    d_CO = 1.22   # C=O
    d_CH_methyl = 1.09
    d_CH_aldehyde = 1.10
    
    # 原子位置（简化 2D+θ 模型）
    # C1 (甲基碳) 在原点
    C1 = np.array([0.0, 0.0, 0.0])
    
    # C2 (羰基碳) 在 x 方向
    C2 = np.array([d_CC, 0.0, 0.0])
    
    # O 醛基氧，在 xy 平面旋转 phi
    O = np.array([d_CC + d_CO * np.cos(phi), 
                  d_CO * np.sin(phi),
                  0.0])
    
    # 3 个甲基 H (在 C1 周围)
    H_methyl = []
    for i in range(3):
        angle = 2*np.pi * i / 3 + phi * 0.3
        H = C1 + np.array([d_CH_methyl * np.cos(angle),
                           d_CH_methyl * np.sin(angle),
                           d_CH_methyl * 0.2 * (-1)**i])
        H_methyl.append(H)
    
    # 醛基 H (在 C2 旁，面外弯曲 θ)
    H_aldehyde = C2 + np.array([-d_CH_aldehyde * np.cos(theta),
                                0.0,
                                d_CH_aldehyde * np.sin(theta)])
    
    # 所有原子 (只保留有效价轨道: 重原子每个贡献 1 个轨道)
    atoms = {
        'C1': C1,
        'C2': C2,
        'O': O,
    }
    
    return atoms, [O, C2, C1] + H_methyl + [H_aldehyde]

def build_hamiltonian_ch3cho(phi, theta):
    """构建 CH3CHO 有效 Hamiltonian。"""
    atoms, all_atoms = ch3cho_geometry(phi, theta)
    n = len(atoms)  # 重原子数 = 3
    H = np.zeros((n, n))
    
    # 轨道能
    alpha = {'C1': ALPHA_C, 'C2': ALPHA_C, 'O': ALPHA_O}
    
    for i, (name_i, atom_i) in enumerate(atoms.items()):
        H[i, i] = alpha[name_i]
        for j, (name_j, atom_j) in enumerate(atoms.items()):
            if i >= j:
                continue
            R_ij = np.linalg.norm(atom_i - atom_j)
            
            # 距离依赖耦合
            if name_i[0] == 'C' and name_j[0] == 'C':
                beta_ij = hopping_beta(R_ij, BETA_CC)
            elif name_i[0] == 'C' and name_j[0] == 'O':
                beta_ij = hopping_beta(R_ij, BETA_CO)
            elif name_i[0] == 'O' and name_j[0] == 'C':
                beta_ij = hopping_beta(R_ij, BETA_CO)
            else:
                beta_ij = hopping_beta(R_ij, BETA_CD)
            
            # 角度依赖 (扭转调制)
            if name_i == 'C1' and name_j == 'C2':
                beta_ij *= np.cos(theta) * 0.8
            elif name_i == 'C2' and name_j == 'O':
                beta_ij *= (0.5 + 0.5 * np.cos(phi))
            
            H[i, j] = H[j, i] = beta_ij
    
    return H

def analyze_ch3cho(phi, theta):
    """对给定 (phi, theta) 计算谱量和能量。"""
    H = build_hamiltonian_ch3cho(phi, theta)
    eigvals = np.sort(linalg.eigh(H)[0])
    
    n_occ = H.shape[0]  # 占据数 = 重原子数
    # 对简化的 3 轨道模型，HOMO 和 LUMO 大致在中间位置
    n_elec = n_occ  # 每个重原子提供 1-2 电子
    homo_idx = n_occ // 2
    
    # 对于 3 轨道: 电子填充
    # 3 个轨道, 6 个电子 (C sp² 贡献 1, O pπ 贡献 2, etc.)
    # 简化: 取轨道 2 为 HOMO (n=3, homo_idx=1, lumo_idx=2)
    # 对不同的 n 适用不同规则
    if n_occ == 3:
        E_HOMO = eigvals[n_occ - 2]  # 轨道 2
        E_LUMO = eigvals[n_occ - 1]  # 轨道 3
    else:
        E_HOMO = eigvals[n_elec // 2]
        E_LUMO = eigvals[n_elec // 2 + 1]
    
    δ_spec = E_LUMO - E_HOMO
    E_total = np.sum(eigvals[:n_occ])  # PES 近似
    
    return {
        'phi': phi, 'theta': theta,
        'E_total': E_total,
        'E_HOMO': E_HOMO, 'E_LUMO': E_LUMO,
        'δ_spec': δ_spec,
        'eigenvalues': eigvals.tolist(),
    }

# ════════════════════════════════════════════════════════════
print("=" * 60)
print("P3: CH3CHO SGL (Spectral Gap Landscape) Scan")
print("=" * 60)

# 扫描参数空间
phi_range = np.linspace(0, np.pi, 40)
theta_range = np.linspace(0, np.pi/3, 30)
PHI, THETA = np.meshgrid(phi_range, theta_range)

E_total_2d = np.zeros_like(PHI)
δ_2d = np.zeros_like(PHI)

for i in range(len(phi_range)):
    for j in range(len(theta_range)):
        res = analyze_ch3cho(PHI[j, i], THETA[j, i])
        E_total_2d[j, i] = res['E_total']
        δ_2d[j, i] = res['δ_spec']

# ── 极值位置查找 ──

# PES 鞍点 (E_total 最大)
i_pes_min = np.unravel_index(np.argmin(E_total_2d), E_total_2d.shape)
i_pes_max = np.unravel_index(np.argmax(E_total_2d), E_total_2d.shape)
phi_pes_max = PHI[i_pes_max]
theta_pes_max = THETA[i_pes_max]

# δ_spec 极小
i_δ_min = np.unravel_index(np.argmin(δ_2d), δ_2d.shape)
phi_δ_min = PHI[i_δ_min]
theta_δ_min = THETA[i_δ_min]

# δ_spec 极大
i_δ_max = np.unravel_index(np.argmax(δ_2d), δ_2d.shape)
phi_δ_max = PHI[i_δ_max]
theta_δ_max = THETA[i_δ_max]

# 偏差
d_phi = (phi_δ_min - phi_pes_max) * 180 / np.pi
d_theta = (theta_δ_min - theta_pes_max) * 180 / np.pi

print(f"\nPES 鞍点 (E_max):  phi={phi_pes_max:.3f} rad ({phi_pes_max*180/np.pi:.1f}°), "
      f"theta={theta_pes_max:.3f} rad ({theta_pes_max*180/np.pi:.1f}°)")
print(f"δ_spec 极小:       phi={phi_δ_min:.3f} rad ({phi_δ_min*180/np.pi:.1f}°), "
      f"theta={theta_δ_min:.3f} rad ({theta_δ_min*180/np.pi:.1f}°)")
print(f"\n偏差: Δphi = {d_phi:.1f}°, Δtheta = {d_theta:.1f}°")

has_deviation = abs(d_phi) > 5 or abs(d_theta) > 5
if has_deviation:
    print(f"\n⚠ δ_spec 极小与 PES 鞍点存在实质性偏差 → 隐式反应通道!")
else:
    print(f"\nδ_spec 极小与 PES 鞍点重合 → 无隐式通道 (或需更高维度扫描)")

# ── 可视化 ──
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(r'P3: CH$_3$CHO Spectral Gap Landscape (SGL)',
             fontsize=14, fontweight='bold')

# (a) δ_spec 能谱图
ax = axes[0, 0]
contour1 = ax.contourf(PHI*180/np.pi, THETA*180/np.pi, δ_2d, levels=20, cmap='hot')
plt.colorbar(contour1, ax=ax, label=r'$\delta_{\rm spec}$ (eV)')
ax.plot(phi_δ_min*180/np.pi, theta_δ_min*180/np.pi, 'b*', ms=15, 
        label=rf'$\delta_{{\rm min}}$ ({phi_δ_min*180/np.pi:.0f}$^\circ$, {theta_δ_min*180/np.pi:.0f}$^\circ$)')
ax.set_xlabel(r'Torsion $\phi$ ($^\circ$)')
ax.set_ylabel(r'CHO bend $\theta$ ($^\circ$)')
ax.set_title(r'Spectral gap $\delta_{\rm spec}$ landscape')
ax.legend()

# (b) PES
ax = axes[0, 1]
contour2 = ax.contourf(PHI*180/np.pi, THETA*180/np.pi, E_total_2d, levels=20, cmap='viridis')
plt.colorbar(contour2, ax=ax, label='E_total (eV)')
ax.plot(phi_pes_max*180/np.pi, theta_pes_max*180/np.pi, 'r*', ms=15,
        label=rf'PES saddle ({phi_pes_max*180/np.pi:.0f}$^\circ$, {theta_pes_max*180/np.pi:.0f}$^\circ$)')
ax.plot(phi_δ_min*180/np.pi, theta_δ_min*180/np.pi, 'bs', ms=8, 
        label=rf'$\delta_{{\rm min}}$', alpha=0.7)
if has_deviation:
    ax.annotate('', xy=(phi_pes_max*180/np.pi, theta_pes_max*180/np.pi),
                xytext=(phi_δ_min*180/np.pi, theta_δ_min*180/np.pi),
                arrowprops=dict(arrowstyle='->', color='yellow', lw=2))
ax.set_xlabel(r'Torsion $\phi$ ($^\circ$)')
ax.set_ylabel(r'CHO bend $\theta$ ($^\circ$)')
ax.set_title(r'PES (E_total) landscape')
ax.legend()

# (c) δ_spec vs φ (固定 θ)
ax = axes[1, 0]
theta_fixed_idx = len(theta_range) // 2
δ_fixed_theta = δ_2d[theta_fixed_idx, :]
ax.plot(phi_range*180/np.pi, δ_fixed_theta, 'b-', lw=2, label=rf'$\theta={theta_range[theta_fixed_idx]*180/np.pi:.0f}^\circ$')
ax.set_xlabel(r'Torsion $\phi$ ($^\circ$)')
ax.set_ylabel(r'$\delta_{\rm spec}$ (eV)')
ax.set_title(r'$\delta_{\rm spec}$ at fixed $\theta$')
ax.grid(True, alpha=0.3)

# (d) δ_spec vs θ (固定 φ)
ax = axes[1, 1]
phi_fixed_idx = len(phi_range) // 2
δ_fixed_phi = δ_2d[:, phi_fixed_idx]
ax.plot(theta_range*180/np.pi, δ_fixed_phi, 'r-', lw=2, label=rf'$\phi={phi_range[phi_fixed_idx]*180/np.pi:.0f}^\circ$')
ax.set_xlabel(r'CHO bend $\theta$ ($^\circ$)')
ax.set_ylabel(r'$\delta_{\rm spec}$ (eV)')
ax.set_title(r'$\delta_{\rm spec}$ at fixed $\phi$')
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig_path = os.path.join(FIGS_DIR, 'ch3cho_sgl_scan.png')
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
print(f"\nFigure saved: {fig_path}")

# ════════════════════════════════════════════════════════════
# 保存
# ════════════════════════════════════════════════════════════
output = {
    'model': 'CH3CHO SGL scan (extended Huckel model)',
    'scan_parameters': {
        'phi_range_rad': [float(phi_range[0]), float(phi_range[-1])],
        'theta_range_rad': [float(theta_range[0]), float(theta_range[-1])],
    },
    'extrema': {
        'PES_saddle': {
            'phi_rad': float(phi_pes_max),
            'phi_deg': float(phi_pes_max*180/np.pi),
            'theta_rad': float(theta_pes_max),
            'theta_deg': float(theta_pes_max*180/np.pi),
            'E_total_eV': float(E_total_2d[i_pes_max]),
        },
        'δ_spec_min': {
            'phi_rad': float(phi_δ_min),
            'phi_deg': float(phi_δ_min*180/np.pi),
            'theta_rad': float(theta_δ_min),
            'theta_deg': float(theta_δ_min*180/np.pi),
            'δ_spec_eV': float(δ_2d[i_δ_min]),
        },
        'deviation': {
            'd_phi_deg': float(d_phi),
            'd_theta_deg': float(d_theta),
            'has_implicit_channel': has_deviation,
        },
    },
}

json_path = os.path.join(DATA_DIR, 'ch3cho_sgl_results.json')
with open(json_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"Results saved: {json_path}")

print(f"""
SUMMARY: P3 CH3CHO SGL Scan - COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PES saddle:  φ={phi_pes_max*180/np.pi:.1f}°, θ={theta_pes_max*180/np.pi:.1f}°
  δ_spec min:  φ={phi_δ_min*180/np.pi:.1f}°, θ={theta_δ_min*180/np.pi:.1f}°
  Deviation:   Δφ={d_phi:.1f}°, Δθ={d_theta:.1f}°
  
  Implicit channel: {'YES' if has_deviation else 'NO'}
  (threshold: >5° in either coordinate)

  Interpretation:
    {'δ_spec minimum and PES saddle coincide → no evidence of hidden channel '
     'in this 2D scan. Higher-dimensional scan (e.g., including C-H bond stretch) '
     'may be needed.' if not has_deviation else
     'δ_spec minimum offset from PES saddle → supports existence of implicit '
     'spectral reaction channel. The reaction pathway predicted by spectral '
     'framework differs from conventional TST.'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
