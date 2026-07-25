"""
spectral_hh2_first_principles.py  v1.0
======================================
P1: H+H₂ 谱键刚性第一性原理推导
    替代 3-中心 Hückel 模型，消除经验参数 β₀ 和 α₀

核心定理:
  定理 P1-A (H-H 谱键刚性): R_bond(H₂) = b_HH · ħ²/(m_e·ℓ_corr²) · exp(-R_HH/ℓ_corr)
  所有参数均由谱框架结构定理确定，无经验拟合。

对比方法:
  1. Hückel 模型 (β₀=-6.3 eV, α₀=-13.6 eV) — 旧方法（存档参考）
  2. 谱键刚性 (V_eq = R_bond/2 = 3.465 eV) — 本工作

依赖:
  - Paper V §5: 谱键刚性定理
  - Paper VI §4: ℓ_corr 丛不变量
  - design_hh2_spectral_bond.md: P1 设计笔记
"""

import numpy as np
from scipy import linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json

# ── 输出目录 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS_DIR = os.path.join(SCRIPT_DIR, '..', 'figs')
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
os.makedirs(FIGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# 谱框架基本常数
# ============================================================
H_BAR = 1.054571817e-34          # J·s
M_E = 9.10938356e-31             # kg
EV_TO_J = 1.602176634e-19        # J/eV

L_CORR = 0.5e-10                 # 0.5 Å → m
L_CORR_A = 0.5                   # Å 单位

# ħ²/(m_e·ℓ_corr²) 计算
E_SCALE_J = (H_BAR ** 2) / (M_E * L_CORR ** 2)
E_SCALE_EV = E_SCALE_J / EV_TO_J  # ≈ 30.48 eV

# ============================================================
# 定理 P1-A: H-H 谱键刚性
# ============================================================

def spectral_bond_rigidity(R_HH_A, b_HH=1.0, l_corr_A=L_CORR_A):
    """
    谱键刚性定理: R_bond = b · ħ²/(m_e·ℓ_corr²) · exp(-R_HH/ℓ_corr)
    
    参数:
      R_HH_A: H-H 键长 [Å]
      b_HH: 键序 (H-H 单键 = 1)
      l_corr_A: ℓ_corr [Å]
    
    返回:
      R_bond [eV]
    """
    prefactor = b_HH * E_SCALE_EV
    exponent = np.exp(-R_HH_A / l_corr_A)
    return prefactor * exponent


def hopping_spectral(R_A, V_eq, R_eq_A, l_corr_A=L_CORR_A):
    """
    谱耦合: V(R) = V_eq · exp(-(R - R_eq)/ℓ_corr)
    
    参数:
      R_A: 当前键长 [Å]
      V_eq: 平衡键长处的耦合 [eV]
      R_eq_A: 平衡键长 [Å] (H₂: 0.741 Å)
      l_corr_A: ℓ_corr [Å]
    """
    return V_eq * np.exp(-(R_A - R_eq_A) / l_corr_A)


# ============================================================
# 分子参数
# ============================================================

# H₂ 谱键刚性参数
R_eq = 0.741                    # [Å] H₂ 平衡键长
B_HH = 1.0                      # H-H 单键键序

# 计算谱键刚性
R_bond_H2 = spectral_bond_rigidity(R_eq, B_HH, L_CORR_A)
# 谱耦合取负值 (成键耦合): V < 0 使 HOMO 为成键轨道, LUMO 为反键轨道
# Hückel 约定: β₀ < 0, 谱键刚性的 V_eq 遵循相同符号约定
V_eq_spectral = -R_bond_H2 / 2.0  # 谱耦合 = -谱间隙/2

print(f"\n{'='*70}")
print(f"谱键刚性计算")
print(f"{'='*70}")
print(f"  ħ²/(m_e·ℓ_corr²) = {E_SCALE_EV:.4f} eV")
print(f"  exp(-R_eq/ℓ_corr) = exp(-{R_eq}/{L_CORR_A}) = {np.exp(-R_eq/L_CORR_A):.6f}")
print(f"  R_bond(H₂) = {B_HH} × {E_SCALE_EV:.4f} × {np.exp(-R_eq/L_CORR_A):.6f} = {R_bond_H2:.4f} eV")
print(f"  V_eq = -R_bond/2 = {V_eq_spectral:.4f} eV (成键耦合, V < 0)")
print(f"  (对比 Hückel β₀ = -6.3 eV, 2|β₀| = 12.6 eV)")

# H₃ 过渡态参数
R_TS = 0.93                     # [Å] TS H-H 距离
R_limit = 6.0                   # [Å] 渐近极限
SIGMA = 0.3                     # IRC 宽度参数

# 物理常数
k_B_eV = 8.617333262e-5         # eV/K

# 文献基准值
E0_LSTH = 0.425                 # [eV] LSTH PES 经典势垒高度

# CVT/SCT 文献对比值
CVT_SCT_LIT = {
    'T_range_K': [200, 300, 400, 500, 600, 800, 1000, 1500, 2000],
    'kappa_SCT': [15.0, 4.5, 2.5, 1.8, 1.5, 1.2, 1.1, 1.05, 1.02],
    'Gamma_CVT': [0.85, 0.88, 0.90, 0.92, 0.93, 0.95, 0.96, 0.97, 0.98],
}


# ============================================================
# Hückel 模型 (参考方法)
# ============================================================

BETA_0 = -6.3                    # [eV] Hückel β₀ @ R_eq
ALPHA_0 = -13.6                  # [eV] Hückel α₀ (VSIE)

def hopping_huckel(R, l_corr=L_CORR_A):
    """β(R) = β₀ exp(-(R-R_eq)/ℓ_corr) (Hückel 旧方法)"""
    if R < 0.3:
        R = 0.3
    return BETA_0 * np.exp(-(R - R_eq) / l_corr)


def solve_h3_huckel(R_ab, R_bc, T_K=300.0):
    """
    [参考] Hückel 模型: 3-中心 Hamiltonian
    H = [[α₀, β_ab, β_ac],
         [β_ab, α₀, β_bc],
         [β_ac, β_bc, α₀]]
    """
    R_ac = R_ab + R_bc
    β_ab = hopping_huckel(R_ab)
    β_bc = hopping_huckel(R_bc)
    β_ac = hopping_huckel(R_ac) * 0.3   # 次近邻经验因子

    H = np.array([
        [ALPHA_0, β_ab, β_ac],
        [β_ab, ALPHA_0, β_bc],
        [β_ac, β_bc, ALPHA_0]
    ])
    eigvals = linalg.eigh(H)[0]
    ε1, ε2, ε3 = eigvals
    δ_spec = ε3 - ε2
    kT = k_B_eV * T_K
    F_spec = 1.0 + np.exp(-δ_spec / kT) if δ_spec > 0 else 2.0

    return {'δ_spec': δ_spec, 'F_spec': F_spec, 'E_GS': 2*ε1 + ε2,
            'ε1': ε1, 'ε2': ε2, 'ε3': ε3}


# ============================================================
# 谱键刚性方法 (本工作)
# ============================================================

def solve_h3_spectral(R_ab, R_bc, T_K=300.0):
    """
    [本工作] 谱键刚性: 3-中心 Hamiltonian
    H = [[0, V(R_ab), V(R_ac)],
         [V(R_ab), 0, V(R_bc)],
         [V(R_ac), V(R_bc), 0]]
    对角元为零 (全同原子能量零点归一化)
    """
    R_ac = R_ab + R_bc
    V_ab = hopping_spectral(R_ab, V_eq_spectral, R_eq, L_CORR_A)
    V_bc = hopping_spectral(R_bc, V_eq_spectral, R_eq, L_CORR_A)
    V_ac = hopping_spectral(R_ac, V_eq_spectral, R_eq, L_CORR_A)

    H = np.array([
        [0.0, V_ab, V_ac],
        [V_ab, 0.0, V_bc],
        [V_ac, V_bc, 0.0]
    ])
    eigvals = linalg.eigh(H)[0]
    ε1, ε2, ε3 = eigvals

    # 谱间隙: HOMO-LUMO gap
    δ_spec = ε3 - ε2

    # 光谱修正因子
    kT = k_B_eV * T_K
    F_spec = 1.0 + np.exp(-δ_spec / kT) if δ_spec > 0 else 2.0

    # 激发态占据数
    n_exc = np.exp(-δ_spec / kT) / F_spec if δ_spec > 0 else 0.5

    return {'ε1': ε1, 'ε2': ε2, 'ε3': ε3,
            'δ_spec': δ_spec, 'F_spec': F_spec, 'n_exc': n_exc,
            'V_ab': V_ab, 'V_bc': V_bc, 'V_ac': V_ac}


def irc_params(s):
    """共线 Ha--Hb--Hc 的 IRC 路径参数化"""
    c = np.arctanh(1 - 2 * (R_TS - R_eq) / (R_limit - R_eq))
    R_ab = R_eq + (R_limit - R_eq) * (1 - np.tanh(s / SIGMA + c)) / 2
    R_bc = R_eq + (R_limit - R_eq) * (1 - np.tanh(-s / SIGMA + c)) / 2
    return R_ab, R_bc, R_ab + R_bc


# ============================================================
# IRC 扫描: 两方法对比
# ============================================================

print(f"\n{'='*70}")
print(f"IRC 扫描: 谱键刚性 vs Hückel")
print(f"{'='*70}")

s_range = np.linspace(-4, 4, 80)
results_spec = []
results_huck = []

for s in s_range:
    R_ab, R_bc, R_ac = irc_params(s)
    sol_spec = solve_h3_spectral(R_ab, R_bc)
    sol_huck = solve_h3_huckel(R_ab, R_bc)
    sol_spec['s'] = s
    sol_huck['s'] = s
    results_spec.append(sol_spec)
    results_huck.append(sol_huck)

# 提取数据
s_arr = np.array([r['s'] for r in results_spec])
δ_spec_arr = np.array([r['δ_spec'] for r in results_spec])
δ_huck_arr = np.array([r['δ_spec'] for r in results_huck])

# 归一化 gap closure ratio
δ_spec_norm = δ_spec_arr / δ_spec_arr[0]
δ_huck_norm = δ_huck_arr / δ_huck_arr[0]

# TS 值
ts_idx = np.argmin(np.abs(s_arr))
ts_δ_spec = δ_spec_arr[ts_idx]
ts_δ_huck = δ_huck_arr[ts_idx]
ts_closure_spec = 1 - ts_δ_spec / δ_spec_arr[0]
ts_closure_huck = 1 - ts_δ_huck / δ_huck_arr[0]

print(f"\n  TS @ s ≈ {s_arr[ts_idx]:.2f}")
print(f"  ┌─────────────────────┬──────────┬──────────┐")
print(f"  │ 量                   │ Hückel   │ 谱键刚性 │")
print(f"  ├─────────────────────┼──────────┼──────────┤")
print(f"  │ δ(reactant) [eV]    │ {δ_huck_arr[0]:>8.3f} │ {δ_spec_arr[0]:>8.3f} │")
print(f"  │ δ(TS) [eV]          │ {ts_δ_huck:>8.3f} │ {ts_δ_spec:>8.3f} │")
print(f"  │ Gap closure [%]     │ {ts_closure_huck*100:>8.1f} │ {ts_closure_spec*100:>8.1f} │")
print(f"  └─────────────────────┴──────────┴──────────┘")

# ============================================================
# 温度扫描: F_spec 修正对比
# ============================================================

print(f"\n{'='*70}")
print(f"温度扫描: F_spec 修正对比")
print(f"{'='*70}")

T_range = np.logspace(np.log10(200), np.log10(5000), 50)
F_spec_ts = []
F_huck_ts = []
F_spec_reac = []
F_huck_reac = []

for T in T_range:
    sol_spec_ts = solve_h3_spectral(R_TS, R_TS, T_K=T)
    sol_huck_ts = solve_h3_huckel(R_TS, R_TS, T_K=T)
    F_spec_ts.append(sol_spec_ts['F_spec'])
    F_huck_ts.append(sol_huck_ts['F_spec'])

    sol_spec_reac = solve_h3_spectral(R_limit, R_eq, T_K=T)
    sol_huck_reac = solve_h3_huckel(R_limit, R_eq, T_K=T)
    F_spec_reac.append(sol_spec_reac['F_spec'])
    F_huck_reac.append(sol_huck_reac['F_spec'])

F_spec_ts = np.array(F_spec_ts)
F_huck_ts = np.array(F_huck_ts)
F_spec_reac = np.array(F_spec_reac)
F_huck_reac = np.array(F_huck_reac)

# 找到 >1% 偏差的温度阈值
spec_dev = (F_spec_ts - 1) * 100
huck_dev = (F_huck_ts - 1) * 100
T_threshold_spec = T_range[np.where(spec_dev >= 1.0)[0][0]] if np.any(spec_dev >= 1.0) else T_range[-1]
T_threshold_huck = T_range[np.where(huck_dev >= 1.0)[0][0]] if np.any(huck_dev >= 1.0) else T_range[-1]

print(f"\n  F_spec(TS) >1% 阈值温度:")
print(f"    Hückel:   T > {T_threshold_huck:.0f} K")
print(f"    谱键刚性: T > {T_threshold_spec:.0f} K")

print(f"\n  {'T(K)':>8} {'F_spec(Hückel)':>16} {'F_spec(谱键)':>16} {'F-1%差':>10}")
print(f"  {'-'*55}")
for T_target in [300, 500, 1000, 2000, 3000, 5000]:
    idx = np.argmin(np.abs(T_range - T_target))
    dev_spec = (F_spec_ts[idx] - 1) * 100
    dev_huck = (F_huck_ts[idx] - 1) * 100
    dev_diff = dev_spec - dev_huck
    print(f"  {T_range[idx]:>8.0f} {F_huck_ts[idx]:>16.8f} {F_spec_ts[idx]:>16.8f} {dev_diff:>+9.4f}%")

# ============================================================
# 与 CVT/SCT 文献对比
# ============================================================

print(f"\n{'='*70}")
print(f"与 CVT/SCT 文献对比")
print(f"{'='*70}")

T_lit = np.array(CVT_SCT_LIT['T_range_K'])
kappa_SCT = np.array(CVT_SCT_LIT['kappa_SCT'])
Gamma_CVT = np.array(CVT_SCT_LIT['Gamma_CVT'])

print(f"\n  {'T(K)':>8} {'κ_SCT':>8} {'Γ_CVT':>8} {'F_spec':>10} {'F-1(%)':>10} {'F_huck':>10} {'F_h-1(%)':>10}")
print(f"  {'-'*65}")

comparison = []
for T, kSCT, gCVT in zip(T_lit, kappa_SCT, Gamma_CVT):
    sol_T = solve_h3_spectral(R_TS, R_TS, T_K=T)
    sol_T_h = solve_h3_huckel(R_TS, R_TS, T_K=T)
    F_T = sol_T['F_spec']
    F_Th = sol_T_h['F_spec']
    entry = {
        'T_K': float(T), 'kappa_SCT_lit': float(kSCT), 'Gamma_CVT_lit': float(gCVT),
        'F_spec_spectral': float(F_T), 'F_spec_Huckel': float(F_Th),
    }
    comparison.append(entry)
    print(f"  {T:>8.0f} {kSCT:>8.2f} {gCVT:>8.3f} {F_T:>10.6f} {(F_T-1)*100:>9.4f}% {F_Th:>10.6f} {(F_Th-1)*100:>9.4f}%")

# ============================================================
# ℓ_corr 敏感性分析
# ============================================================

print(f"\n{'='*70}")
print(f"ℓ_corr 敏感性分析: 对 δ_spec(TS) 的影响")
print(f"{'='*70}")

l_corr_sweep = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5, 2.0])
δ_TS_lc = []

for lc in l_corr_sweep:
    # 重新计算该 ℓ_corr 下的谱键刚性
    E_scale_lc = (H_BAR ** 2) / (M_E * (lc * 1e-10) ** 2) / EV_TO_J
    R_bond_lc = B_HH * E_scale_lc * np.exp(-R_eq / lc)
    V_eq_lc = -R_bond_lc / 2.0    # 负号: 成键耦合
    
    # TS 处的谱间隙
    V_TS_lc = V_eq_lc * np.exp(-(R_TS - R_eq) / lc)
    V_ac_lc = V_eq_lc * np.exp(-(2 * R_TS - R_eq) / lc)
    H_lc = np.array([[0.0, V_TS_lc, V_ac_lc],
                     [V_TS_lc, 0.0, V_TS_lc],
                     [V_ac_lc, V_TS_lc, 0.0]])
    eigvals = linalg.eigh(H_lc)[0]
    δ_TS_lc.append(eigvals[2] - eigvals[1])
    
    # 反应物极限的谱间隙 ≈ R_bond/2 (H₂ 2-能级间隙)
    δ_reac_lc = R_bond_lc / 2.0
    closure_3v2 = 1 - (eigvals[2] - eigvals[1]) / δ_reac_lc
    print(f"  ℓ_corr = {lc:.1f} Å: δ(TS) = {eigvals[2]-eigvals[1]:.4f} eV, "
          f"δ(reac) = {δ_reac_lc:.4f} eV, gap closure = {closure_3v2*100:.1f}%")

δ_TS_lc = np.array(δ_TS_lc)
print(f"\n  注: ℓ_corr={L_CORR_A} Å 为谱框架预言值, 其他供敏感性参考")

# ============================================================
# 可视化
# ============================================================

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle(r'P1: H+H$_2$ Spectral Bond Rigidity -- Huckel Comparison',
             fontsize=14, fontweight='bold')

# (a) IRC 几何
R_ab_arr = np.array([r['s'] for r in results_spec])
# Recompute geometry
R_ab_geo = np.array([irc_params(s)[0] for s in s_arr])
R_bc_geo = np.array([irc_params(s)[1] for s in s_arr])
R_ac_geo = np.array([irc_params(s)[2] for s in s_arr])

ax = axes[0, 0]
ax.plot(s_arr, R_ab_geo, 'b-', lw=2, label=r'$R_{\rm ab}$')
ax.plot(s_arr, R_bc_geo, 'r-', lw=2, label=r'$R_{\rm bc}$')
ax.plot(s_arr, R_ac_geo, 'g--', lw=1.5, label=r'$R_{\rm ac}$')
ax.axvline(0, color='gray', ls=':', alpha=0.5)
ax.set_xlabel('Reaction coordinate s')
ax.set_ylabel(r'Distance ($\AA$)')
ax.set_title('IRC geometry (collinear)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# (b) δ_spec 沿 IRC — 两方法对比
ax = axes[0, 1]
ax.plot(s_arr, δ_spec_arr, 'o-', color='#2196F3', lw=2, markersize=3,
        label=rf'Spectral bond ($V_{{eq}}$={V_eq_spectral:.3f} eV)')
ax.plot(s_arr, δ_huck_arr, 's--', color='#FF5722', lw=2, markersize=3,
        label=r'Huckel ($\beta_0$=-6.3 eV)')
ax.axvline(0, color='gray', ls=':', alpha=0.5)
ax.set_xlabel('Reaction coordinate s')
ax.set_ylabel(r'$\delta_{\rm spec}$ (eV)')
ax.set_title(r'HOMO-LUMO gap $\delta_{\rm spec}$')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# (c) 归一化 Gap Closure — 核心对比
ax = axes[0, 2]
ax.plot(s_arr, δ_spec_norm, 'o-', color='#2196F3', lw=2, markersize=3, label='Spectral bond')
ax.plot(s_arr, δ_huck_norm, 's--', color='#FF5722', lw=2, markersize=3, label='Huckel')
ax.axvline(0, color='gray', ls=':', alpha=0.5)
ax.set_xlabel('Reaction coordinate s')
ax.set_ylabel(r'$\delta_{\rm spec}(s)/\delta_{\rm spec}(-4)$')
ax.set_title('Normalized gap closure')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# (d) F_spec vs T
ax = axes[1, 0]
ax.semilogx(T_range, (F_spec_ts - 1)*100, 'b-', lw=2, label='Spectral bond (TS)')
ax.semilogx(T_range, (F_huck_ts - 1)*100, 'r--', lw=2, label='Huckel (TS)')
ax.axhline(1.0, color='gray', ls=':', alpha=0.5, label='1% threshold')
ax.axvline(T_threshold_spec, color='blue', ls='--', alpha=0.3)
ax.axvline(T_threshold_huck, color='red', ls='--', alpha=0.3)
ax.set_xlabel('T (K)')
ax.set_ylabel(r'$(F_{\rm spec}-1)\times 100$ (%)')
ax.set_title(r'$F_{\rm spec}$ vs temperature')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# (e) 与 CVT/SCT 对比
ax = axes[1, 1]
F_lit_spec = np.array([c['F_spec_spectral'] for c in comparison])
F_lit_huck = np.array([c['F_spec_Huckel'] for c in comparison])
ax.plot(T_lit, kappa_SCT, 's-', color='#FF5722', lw=2, ms=6, label='SCT (lit)')
ax.plot(T_lit, Gamma_CVT, '^--', color='#4CAF50', lw=2, ms=6, label='CVT Gamma (lit)')
ax.plot(T_lit, F_lit_spec, 'o-', color='#2196F3', lw=2, ms=6, label=r'$F_{\rm spec}$ Spectral bond')
ax.plot(T_lit, F_lit_huck, 'x:', color='#9C27B0', lw=1.5, ms=5, label=r'$F_{\rm spec}$ Huckel')
ax.set_xlabel('T (K)')
ax.set_ylabel('Correction factor')
ax.set_title('Spectral vs CVT/SCT corrections')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xscale('log')

# (f) ℓ_corr 敏感性
ax = axes[1, 2]
ax.plot(l_corr_sweep, δ_TS_lc, 'o-', color='#9C27B0', lw=2, ms=6)
ax.axvline(L_CORR_A, color='green', ls=':', alpha=0.5,
           label=rf'SF: $\ell_{{\rm corr}}$={L_CORR_A} $\AA$')
ax.set_xlabel(r'$\ell_{\rm corr}$ ($\AA$)')
ax.set_ylabel(r'$\delta_{\rm spec}(TS)$ (eV)')
ax.set_title(r'$\ell_{\rm corr}$ sensitivity at TS')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig_path = os.path.join(FIGS_DIR, 'hh2_first_principles_comparison.png')
plt.savefig(fig_path, dpi=150)
print(f"\n  图保存至: {fig_path}")

# ============================================================
# 保存数值结果
# ============================================================

result_data = {
    'spectral_bond_rigidity': {
        'E_scale_eV': float(E_SCALE_EV),
        'R_bond_H2_eV': float(R_bond_H2),
        'V_eq_eV': float(V_eq_spectral),
    },
    'IRC_comparison': {
        'δ_spec_reactant_eV': float(δ_spec_arr[0]),
        'δ_huck_reactant_eV': float(δ_huck_arr[0]),
        'δ_spec_TS_eV': float(ts_δ_spec),
        'δ_huck_TS_eV': float(ts_δ_huck),
        'closure_spec_pct': float(ts_closure_spec * 100),
        'closure_huck_pct': float(ts_closure_huck * 100),
    },
    'temperature_scan': {
        'T_threshold_spec_K': float(T_threshold_spec),
        'T_threshold_huck_K': float(T_threshold_huck),
    },
    'CVT_SCT_comparison': comparison,
    'l_corr_sensitivity': {
        'l_corr_A': l_corr_sweep.tolist(),
        'δ_TS_eV': δ_TS_lc.tolist(),
    },
}

json_path = os.path.join(DATA_DIR, 'hh2_first_principles_results.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(result_data, f, indent=2, ensure_ascii=False)
print(f"  数据保存至: {json_path}")

# ============================================================
# 结论
# ============================================================
print(f"\n{'='*70}")
print(f"核心结论")
print(f"{'='*70}")
print()
print(f"  谱键刚性 R_bond(H₂) = {R_bond_H2:.4f} eV (完全由结构定理确定)")
print(f"  谱耦合 V_eq = R_bond/2 = {V_eq_spectral:.4f} eV")
print(f"  (对比 Hückel: β₀ = −6.3 eV, α₀ = −13.6 eV, 均为经验参数)")
print()
print(f"  Gap closure 对比:")
print(f"    谱键刚性: δ_TS/δ_reactant = {δ_spec_norm[ts_idx]:.3f} (closure {ts_closure_spec*100:.1f}%)")
print(f"    Hückel:   δ_TS/δ_reactant = {δ_huck_norm[ts_idx]:.3f} (closure {ts_closure_huck*100:.1f}%)")
print(f"    差异: {(ts_closure_spec - ts_closure_huck)*100:+.1f}%")
print()
print(f"  F_spec 修正阈值温度:")
print(f"    谱键刚性: T > {T_threshold_spec:.0f} K")
print(f"    Hückel:   T > {T_threshold_huck:.0f} K")
print()
print(f"  谱键刚性方法的优势:")
print(f"    1. 零自由参数: V_eq 来自谱框架结构定理")
print(f"    2. 无次近邻经验因子: V_ac 由 ℓ_corr 直接衰减")
print(f"    3. 对角元归一化: 全同原子无需经验 VSIE")
print(f"    4. 与 ℓ_corr = 0.5 Å 完全自洽")
print(f"{'='*70}")
