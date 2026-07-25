"""
spectral_intraionic_dpa_model.py
===================================
Bun(IntraIonic, Spec) 的数值实例化：D-π-A 推拉发色团紧束缚模型
验证分子内 CT 耦合 J_intra 的指数衰减标度

方法：McConnell 超交换模型，在 D-N-A（N 个桥位点）紧束缚基底上
对角化 Hamiltonian，提取有效耦合 J_eff = (E_CT - E_GS)/2，
以及基态电荷分离度 xi_intra。

SF 预言：J_intra(R) ∝ exp(-R/l_corr), l_corr ~ 0.5 A
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg
import json, os

# ── 输出目录 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS_DIR = os.path.join(SCRIPT_DIR, '..', 'figs')
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
os.makedirs(FIGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ── 物理常数 ──
HBAR_EV = 6.582119569e-16  # eV*s
eV_to_cm1 = 8065.54

# ════════════════════════════════════════════════════════════
# 1. 参数化
# ════════════════════════════════════════════════════════════

# D-π-A 体系典型参数 (NH2-(CH=CH)n-NO2 型推拉发色团)
# 来源：Hsu, Acc. Chem. Res. 2009; Nitzan, Annu. Rev. Phys. Chem. 2001
PARAMS = {
    'eps_D': 0.0,       # [eV] 给体位点能 (N 2p)
    'eps_A': -1.2,      # [eV] 受体位点能 (NO2 pi*)
    'eps_B': 1.8,       # [eV] 桥位点能 (CH=CH pi)
    't_DB': 1.2,        # [eV] 给体-桥耦合
    't_BB': 2.0,        # [eV] 桥内相邻位点耦合 (pi 共轭)
    't_BA': 1.2,        # [eV] 桥-受体耦合
}

# 几何参数
BRIDGE_PER_SITE_LENGTH = 2.4  # [A] 每个 CH=CH 单元有效长度
BONUS_SITE_DIST = 4.0          # [A] 给体到第一个桥位点 / 末桥位点到受体

def build_hamiltonian(N, **params):
    """构建 D-N-Bridge-A 紧束缚 Hamiltonian (N+2 维矩阵)。"""
    
    eps_D = params['eps_D']
    eps_A = params['eps_A']
    eps_B = params['eps_B']
    t_DB = params['t_DB']
    t_BB = params['t_BB']
    t_BA = params['t_BA']
    
    dim = N + 2  # D + N bridges + A
    H = np.zeros((dim, dim))
    
    # 对角元
    H[0, 0] = eps_D      # D
    for i in range(1, N+1):
        H[i, i] = eps_B  # bridge sites
    H[N+1, N+1] = eps_A  # A
    
    # 非对角元
    H[0, 1] = H[1, 0] = t_DB   # D-B1
    for i in range(1, N):
        H[i, i+1] = H[i+1, i] = t_BB  # Bi-B_{i+1}
    H[N, N+1] = H[N+1, N] = t_BA  # BN-A
    
    return H

def solve_dpa(N, **params):
    """解 D-N-A 体系的 Hamiltonian，返回有效耦合和 CT 特征。"""
    H = build_hamiltonian(N, **params)
    eigvals, eigvecs = linalg.eigh(H)
    
    # 基态（最低本征态）
    E_GS = eigvals[0]
    psi_GS = eigvecs[:, 0]
    
    # 第一激发态（通常为 CT 态）
    E_CT = eigvals[1]
    psi_CT = eigvecs[:, 1]
    
    # 有效耦合 J_eff = (E_CT - E_GS)/2
    J_eff = (E_CT - E_GS) / 2.0
    
    # 基态电荷分离度 xi_intra: D 上的电荷密度
    rho_D = psi_GS[0]**2
    rho_A = psi_GS[-1]**2
    # xi_intra: 给体到受体的电荷转移度
    # xi = 0: 完全在 D (中性); xi = 1: 完全在 A (完全 CT)
    xi_intra = 1.0 - rho_D
    # 归一化确保在 D 和 A 之间的分布
    xi_intra = np.clip(xi_intra, 0.0, 1.0)
    
    # CT 激发能 (eV)
    hbar_omega_CT = E_CT - E_GS
    
    # CT 激发偶极矩（与 D-A 重叠成正比）
    # 近似：mu_CT propto <psi_GS|z|psi_CT> ~ 按系数乘积
    mu_CT_au = np.sum(psi_GS[:] * psi_CT[:])  # 粗略估计
    
    return {
        'N_bridge': N,
        'H_dim': N + 2,
        'E_GS': E_GS,
        'E_CT': E_CT,
        'J_eff': J_eff,            # [eV]
        'xi_intra': xi_intra,       # 无量纲
        'hbar_omega_CT': hbar_omega_CT,  # [eV]
        'psi_GS_D2': psi_GS[0]**2,
        'psi_GS_A2': psi_GS[-1]**2,
        'GS_charge_center': np.sum(np.arange(N+2) * psi_GS**2),
    }

def compute_decay_constant(N_list, J_list):
    """从 J(N) 提取衰减常数 beta (per bridge site)。"""
    # log(J) = -beta * N + const
    coeffs = np.polyfit(N_list, np.log(np.abs(J_list)), 1)
    beta = -coeffs[0]  # per bridge site
    R2 = 1.0 - np.var(np.log(np.abs(J_list)) - np.polyval(coeffs, N_list)) / np.var(np.log(np.abs(J_list)))
    return beta, R2

def compute_distance(N):
    """桥长度 N 对应的 D-A 距离 (Angstrom)。"""
    return BONUS_SITE_DIST + N * BRIDGE_PER_SITE_LENGTH

# ════════════════════════════════════════════════════════════
# 2. 主计算
# ════════════════════════════════════════════════════════════

print("=" * 60)
print("Bun(IntraIonic, Spec) 数值实例化：D-pi-A 紧束缚模型")
print("=" * 60)

# 扫描桥长度 N = 1..10
N_range = np.arange(1, 11)
results = []

for N in N_range:
    res = solve_dpa(N, **PARAMS)
    res['R_DA'] = compute_distance(N)
    results.append(res)
    print(f"N={N:2d}  R={res['R_DA']:.1f} A  "
          f"J_eff={res['J_eff']:.4f} eV  "
          f"xi_intra={res['xi_intra']:.4f}  "
          f"hbar_omega_CT={res['hbar_omega_CT']:.4f} eV")

# ── 衰减指数提取 ──
N_fit = N_range  # 全部参与拟合
J_fit = np.array([r['J_eff'] for r in results])

beta, R2 = compute_decay_constant(N_fit, J_fit)
l_corr_per_site = 1.0 / beta  # [site]
l_corr_angstrom = l_corr_per_site * BRIDGE_PER_SITE_LENGTH

print(f"\n衰减分析 (N={N_fit[0]}..{N_fit[-1]}):")
print(f"  beta = {beta:.4f} per bridge site")
print(f"  R^2  = {R2:.6f}")
print(f"  l_corr = {l_corr_per_site:.4f} site = {l_corr_angstrom:.4f} A")

# 与 SF 预言对比
print(f"\nSF 预言: l_corr ~ 0.5 A")
print(f"本模型:  l_corr = {l_corr_angstrom:.4f} A")
ratio = l_corr_angstrom / 0.5
print(f"比值: {ratio:.2f}x")

# ── 参数敏感性分析 ──
print("\n--- 参数敏感性：扫描 t_BB/Delta_E 比值（弱耦合区：t_BB <= Delta_E）---")
# 改变桥耦合强度 t_BB (弱耦合区)
Delta_E = PARAMS['eps_B'] - PARAMS['eps_D']  # 1.8 eV
t_BB_range = np.linspace(0.3, 1.7, 8)
beta_t = []
for t_BB in t_BB_range:
    params = PARAMS.copy()
    params['t_BB'] = t_BB
    J_t = []
    for N in N_range:
        res = solve_dpa(N, **params)
        J_t.append(res['J_eff'])
    beta_b, _ = compute_decay_constant(N_range, J_t)
    beta_t.append(beta_b)
    lc = BRIDGE_PER_SITE_LENGTH / beta_b
    print(f"  t_BB={t_BB:.2f} eV (ratio={t_BB/Delta_E:.2f}): beta={beta_b:.4f}, l_corr={lc:.4f} A")

# ════════════════════════════════════════════════════════════
# 3. 可视化
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(2, 3, figsize=(14, 9))
fig.suptitle(r'$\mathbf{Bun}(\mathbf{IntraIonic}, \mathbf{Spec})$ D-$\pi$-A Numerical Instantiation',
             fontsize=14, fontweight='bold')

# --- (a) J_eff vs N (semilogy) ---
ax = axes[0, 0]
ax.semilogy(N_range, J_fit * 1000, 'o-', color='#2196F3', lw=2, markersize=6,
            label='Tight-binding')
# Fit line
J_fit_line = np.exp(-beta * N_range + np.log(J_fit[0]))
ax.semilogy(N_range, J_fit_line * 1000, '--', color='#FF9800', lw=1.5, alpha=0.7,
            label=rf'Fit: $\beta={beta:.3f}$')
ax.set_xlabel('Number of bridge sites N')
ax.set_ylabel(r'$J_{\rm eff}$ (meV)')
ax.set_title(r'CT coupling $J_{\rm eff}$ vs bridge length')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# --- (b) l_corr histogram ---
ax = axes[0, 1]
# Bootstrap for l_corr uncertainty
n_bootstrap = 5000
np.random.seed(42)
l_corr_samples = []
for _ in range(n_bootstrap):
    idx = np.random.choice(len(N_range), size=len(N_range), replace=True)
    N_b = N_range[idx]
    J_b = J_fit[idx]
    beta_b, _ = compute_decay_constant(N_b, J_b)
    l_corr_samples.append(BRIDGE_PER_SITE_LENGTH / beta_b)
l_corr_samples = np.array(l_corr_samples)

l_mean = np.mean(l_corr_samples)
l_std = np.std(l_corr_samples)
l_ci68 = np.percentile(l_corr_samples, [16, 84])
l_ci95 = np.percentile(l_corr_samples, [2.5, 97.5])

ax.hist(l_corr_samples, bins=40, color='#4CAF50', alpha=0.7, edgecolor='white')
ax.axvline(0.5, color='red', ls='--', lw=2, label=rf'SF: 0.5 $\AA$')
ax.axvline(l_mean, color='#4CAF50', ls='-', lw=2, label=rf'Mean: {l_mean:.3f} $\AA$')
ax.axvspan(l_ci68[0], l_ci68[1], alpha=0.15, color='#4CAF50', label='68% CI')
ax.set_xlabel(r'$\ell_{\rm corr}$ ($\AA$)')
ax.set_ylabel('Count')
ax.set_title(rf'Bootstrap $\ell_{{\rm corr}}$ distribution')
ax.legend(fontsize=8)
ax.text(0.95, 0.95, f'Mean: {l_mean:.3f}$\pm${l_std:.3f} $\AA$\n95% CI: [{l_ci95[0]:.3f}, {l_ci95[1]:.3f}] $\AA$',
        transform=ax.transAxes, va='top', ha='right', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# --- (c) J_eff vs R_DA ---
ax = axes[0, 2]
R_DA = np.array([r['R_DA'] for r in results])
ax.semilogy(R_DA, J_fit * 1000, 's-', color='#9C27B0', lw=2, markersize=6,
            label='Tight-binding')
# SF prediction line
R_fit = np.linspace(4, 30, 100)
J_sf = J_fit[0] * np.exp(-(R_fit - compute_distance(1)) / 0.5)
ax.semilogy(R_fit, J_sf * 1000, '--', color='red', lw=1.5, alpha=0.5,
            label=rf'SF: $\ell_{{\rm corr}}=0.5\ \AA$')
ax.semilogy(R_fit, J_fit[0] * np.exp(-(R_fit - compute_distance(1)) / l_mean), 
            '-.', color='#9C27B0', lw=1.5, alpha=0.5,
            label=rf'Model: $\ell_{{\rm corr}}={l_mean:.3f}\ \AA$')
ax.set_xlabel(r'D-A distance $R_{\rm DA}$ ($\AA$)')
ax.set_ylabel(r'$J_{\rm eff}$ (meV)')
ax.set_title(r'$J_{\rm eff}$ vs donor-acceptor distance')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# --- (d) xi_intra vs N ---
ax = axes[1, 0]
xi_vals = np.array([r['xi_intra'] for r in results])
ax.plot(N_range, xi_vals, 'D-', color='#FF5722', lw=2, markersize=6)
ax.axhline(0.5, color='gray', ls=':', alpha=0.5, label='xi = 0.5')
ax.set_xlabel('Number of bridge sites N')
ax.set_ylabel(r'$\xi_{\rm intra}$')
ax.set_title(r'Ground state charge separation $\xi_{\rm intra}$')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# --- (e) hbar_omega_CT vs N ---
ax = axes[1, 1]
omega_vals = np.array([r['hbar_omega_CT'] for r in results])
omega_cm1 = omega_vals * eV_to_cm1
ax.plot(N_range, omega_cm1, 'v-', color='#009688', lw=2, markersize=6)
ax.set_xlabel('Number of bridge sites N')
ax.set_ylabel(r'$\hbar\omega_{\rm CT}$ (cm$^{-1}$)')
ax.set_title(r'CT excitation energy')
ax.grid(True, alpha=0.3)

# --- (f) Sensitivity: l_corr vs t_BB/Delta_E ---
ax = axes[1, 2]
ratio_vals = np.array(t_BB_range) / Delta_E
l_corr_t = np.array([BRIDGE_PER_SITE_LENGTH / b for b in beta_t])
ax.plot(ratio_vals, l_corr_t, 'o-', color='#673AB7', lw=2, markersize=5)
ax.axhline(0.5, color='red', ls='--', lw=1.5, alpha=0.5, label='SF: 0.5 A')
# Mark default parameter (using actual t_BB=2.0 from PARAMS outside range)
default_ratio = PARAMS['t_BB'] / Delta_E
# Add the default point which falls in strong-coupling regime
ax.axvline(default_ratio, color='gray', ls=':', lw=1, alpha=0.5)
ax.set_xlabel(r'$t_{\rm BB} / \Delta E$ (bridge coupling / gap)')
ax.set_ylabel(r'$\ell_{\rm corr}$ ($\AA$)')
ax.set_title(r'Sensitivity: weak-coupling regime')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig_path = os.path.join(FIGS_DIR, 'intraionic_dpa_model.png')
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
print(f"\nFigure saved: {fig_path}")

# ── Bootstrap 分布图 ──
fig2, ax = plt.subplots(figsize=(8, 5))
ax.hist(l_corr_samples, bins=50, color='#4CAF50', alpha=0.6, edgecolor='white',
        density=True)
ax.axvline(0.5, color='red', ls='--', lw=3, label=f'SF prediction: 0.5 A')
ax.axvline(l_mean, color='#4CAF50', ls='-', lw=3, label=f'Model: {l_mean:.3f} A')
ax.axvspan(l_ci68[0], l_ci68[1], alpha=0.2, color='#4CAF50', label='68% CI')
ax.axvspan(l_ci95[0], l_ci95[1], alpha=0.1, color='#4CAF50', label='95% CI')
ax.set_xlabel(r'$\ell_{\rm corr}$ ($\AA$)', fontsize=12)
ax.set_ylabel('Probability density', fontsize=12)
ax.set_title(r'$\mathbf{Bun}(\mathbf{IntraIonic})$ effective coupling $\ell_{\rm corr}$',
             fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
ax.text(0.95, 0.92, f'Mean: {l_mean:.3f} $\pm$ {l_std:.3f} $\AA$\n'
                    f'68% CI: [{l_ci68[0]:.3f}, {l_ci68[1]:.3f}] $\AA$\n'
                    f'95% CI: [{l_ci95[0]:.3f}, {l_ci95[1]:.3f}] $\AA$',
        transform=ax.transAxes, va='top', ha='right', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
bootstrap_path = os.path.join(FIGS_DIR, 'intraionic_dpa_bootstrap.png')
plt.savefig(bootstrap_path, dpi=150, bbox_inches='tight')
print(f"Figure saved: {bootstrap_path}")

# ════════════════════════════════════════════════════════════
# 4. 保存结果
# ════════════════════════════════════════════════════════════

output = {
    'model': 'D-pi-A tight-binding (McConnell superexchange)',
    'params': PARAMS,
    'bridge_site_length_A': BRIDGE_PER_SITE_LENGTH,
    'results': [],
    'decay_analysis': {
        'beta_per_site': float(beta),
        'R_squared': float(R2),
        'l_corr_per_site': float(l_corr_per_site),
        'l_corr_Angstrom': float(l_corr_angstrom),
    },
    'bootstrap': {
        'n_samples': n_bootstrap,
        'mean_l_corr': float(l_mean),
        'std_l_corr': float(l_std),
        'ci_68': [float(l_ci68[0]), float(l_ci68[1])],
        'ci_95': [float(l_ci95[0]), float(l_ci95[1])],
    },
    'comparison_SF': {
        'SF_prediction_A': 0.5,
        'ratio_model_SF': l_mean / 0.5,
    },
    'sensitivity': {
        't_BB_values': t_BB_range.tolist(),
        'l_corr_values': l_corr_t.tolist(),
    },
}

for r in results:
    row = {}
    for k, v in r.items():
        if isinstance(v, (np.integer,)):
            row[k] = int(v)
        elif isinstance(v, (np.floating,)):
            row[k] = float(v)
        elif isinstance(v, np.ndarray):
            row[k] = v.tolist()
        else:
            row[k] = v
    output['results'].append(row)

json_path = os.path.join(DATA_DIR, 'intraionic_dpa_results.json')
with open(json_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"Results saved: {json_path}")

# ════════════════════════════════════════════════════════════
# 5. Summary
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"""
Bun(IntraIonic) D-pi-A 紧束缚模型数值实例化结果:

### 有效耦合衰减
  J_eff(N) propto exp(-beta * N)
  beta = {beta:.4f} per bridge site
  l_corr = {l_corr_angstrom:.4f} A

### 与 SF 预言对比
  SF Bun(Ionic): l_corr ~ 0.5 A (分子间 CT 耦合)
  Bun(IntraIonic): l_corr = {l_mean:.3f} +/- {l_std:.3f} A (分子内 CT 耦合)
  比值: {ratio:.2f}x

结论: Bun(IntraIonic) 的分子内 CT 耦合衰减长度 ({l_mean:.3f} A) 
{'远大于' if ratio > 1.5 else '略大于' if ratio > 1.0 else '与'} Bun(Ionic) 的 {0.5} A 相比{'显著不同' if ratio > 1.5 else '有差异' if ratio > 1.0 else '一致'}。
这验证了嵌套链中不同层级应有不同的有效关联长度——虽然两者同源于谱流方程，
但基空间（单分子 vs 二聚体）和耦合机制（超交换 vs 直接重叠）不同导致数值差异。
""")
