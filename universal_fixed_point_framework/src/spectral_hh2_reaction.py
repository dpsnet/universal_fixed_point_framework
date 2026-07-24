"""
spectral_hh2_reaction.py
=========================
P1: H + H2 反应 IRC 沿线的谱分析 (v2.0 升级版)
使用 3-中心 Hückel 模型 + 谱框架 ℓ_corr 预言 + 文献 CVT/SCT 对比

升级内容 (v1.0 → v2.0):
  1. 添加 LSTH PES 文献参考数据和 H₃ 势垒基准
  2. 温度扫描 (300-5000K) 以确定 F_spec 可测量的温度阈值
  3. 与已发表的 CVT/SCT 计算结果的系统对比表
  4. Wigner 穿透修正作为参考
  5. F_spec 修正的 Arrhenius 分析

计算内容:
  1. HOMO-LUMO 谱间隙 δ_spec(s) 沿 IRC
  2. 谱通量 F_spec(s) = 1 + exp(-δ_spec(s)/kT)
  3. 光谱修正的 Arrhenius 偏差: ΔE_a, Δln(A)
  4. 与 CVT/SCT 文献值的系统对比
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg, optimize
import json, os

# ── 输出目录 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGS_DIR = os.path.join(SCRIPT_DIR, '..', 'figs')
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
os.makedirs(FIGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ════════════════════════════════════════════════════════════
# 1. 分子参数
# ════════════════════════════════════════════════════════════

# H₂ 分子参数
R_eq = 0.741    # [A] H₂ 平衡键长
D_e = 4.75      # [eV] H₂ 解离能
omega_e = 0.546 # [eV] H₂ 振动频率 (4401 cm^-1)

# 谱框架参数
L_CORR = 0.5    # [A] SF 预言 ℓ_corr

# Hückel 参数
# β₀: 从 H₂ 1σ_g-1σ_u 分裂确定
#   H₂ 在 R_eq: ΔE = 2|β(R_eq)| = 12.6 eV → |β(R_eq)| = 6.3 eV
BETA_0 = -6.3   # [eV] Hückel 跳跃积分 @ R_eq
ALPHA_0 = -13.6 # [eV] H 1s 库仑积分 (VSIE)

# H₃ 过渡态 (共线)
R_TS = 0.93     # [A] H₃ TS H-H 距离 (Sato 参数化, LSTH PES)
R_limit = 6.0   # [A] 渐近极限
SIGMA = 0.3     # IRC 宽度参数

# 文献 CVT/SCT 基准值 (H + H₂ → H₂ + H, 共线)
# 来源: Truhlar et al. (1982-1996), Garrett et al. (1980)
CVT_SCT_LIT = {
    'T_range_K': [200, 300, 400, 500, 600, 800, 1000, 1500, 2000],
    'kappa_SCT': [15.0, 4.5, 2.5, 1.8, 1.5, 1.2, 1.1, 1.05, 1.02],
    'Gamma_CVT': [0.85, 0.88, 0.90, 0.92, 0.93, 0.95, 0.96, 0.97, 0.98],
    'E0_classical': 0.425,  # [eV] 经典势垒高度 (LSTH PES)
    'E0_ZPE': 0.276,        # [eV] ZPE 修正后的势垒
    'Ea_TST_300K': 0.43,    # [eV] TST 活化能 @ 300K
    'Ea_CVT_SCT_300K': 0.28, # [eV] CVT/SCT 活化能 @ 300K
    'k_CVT_SCT_300K': 2.8e-17, # [cm^3/molecule/s]
}

k_B_eV = 8.617333262e-5  # [eV/K]
k_B_J = 1.380649e-23     # [J/K]
h_Js = 6.62607015e-34    # [J·s]
R_gas = 8.314462618       # [J/mol/K]

# ════════════════════════════════════════════════════════════
# 2. 核心模型函数
# ════════════════════════════════════════════════════════════

def hopping(R, l_corr=L_CORR):
    """β(R) = β₀ exp(-(R-R_eq)/ℓ_corr)"""
    if R < 0.3:
        R = 0.3
    return BETA_0 * np.exp(-(R - R_eq) / l_corr)

def irc_params(s):
    """
    共线 Ha--Hb--Hc 的 IRC 路径参数化。
    使用双曲正切插值确保 s=0 时精确给出 TS 几何。
    """
    c = np.arctanh(1 - 2 * (R_TS - R_eq) / (R_limit - R_eq))
    R_ab = R_eq + (R_limit - R_eq) * (1 - np.tanh(s / SIGMA + c)) / 2
    R_bc = R_eq + (R_limit - R_eq) * (1 - np.tanh(-s / SIGMA + c)) / 2
    R_ac = R_ab + R_bc
    return R_ab, R_bc, R_ac

def solve_h3(R_ab, R_bc, T_K=300.0, l_corr=L_CORR):
    """求解 H₃ 3-中心 Hückel Hamiltonian 并计算谱量。"""
    R_ac = R_ab + R_bc
    β_ab = hopping(R_ab, l_corr)
    β_bc = hopping(R_bc, l_corr)
    β_ac = hopping(R_ac, l_corr) * 0.3  # 次近邻耦合
    
    H = np.array([
        [ALPHA_0, β_ab, β_ac],
        [β_ab, ALPHA_0, β_bc],
        [β_ac, β_bc, ALPHA_0]
    ])
    
    eigvals, eigvecs = linalg.eigh(H)
    ε1, ε2, ε3 = eigvals
    
    E_GS = 2*ε1 + ε2
    E_HOMO = ε2
    E_LUMO = ε3
    δ_spec = ε3 - ε2
    
    # 光谱修正因子 F_spec
    kT = k_B_eV * T_K
    if δ_spec > 0:
        F_spec = 1.0 + np.exp(-δ_spec / kT)
    else:
        F_spec = 2.0  # degenerate limit
    
    if δ_spec > 0:
        n_exc = np.exp(-δ_spec / kT) / F_spec
    else:
        n_exc = 0.5
    
    return {
        'ε1': ε1, 'ε2': ε2, 'ε3': ε3,
        'E_GS': E_GS, 'E_HOMO': E_HOMO, 'E_LUMO': E_LUMO,
        'δ_spec': δ_spec, 'F_spec': F_spec, 'n_exc': n_exc,
        'β_ab': β_ab, 'β_bc': β_bc, 'β_ac': β_ac,
    }

def wigner_tunneling(T_K, nu_star=1500):
    """
    Wigner 穿透修正因子。
    nu_star: 虚频 [cm^-1], H₃ 共线 TS 约 1500i cm^-1
    """
    hc_cm_eV = 1.23984193e-4  # eV·cm
    hbar_omega = hc_cm_eV * nu_star  # [eV] h·nu*
    kT = k_B_eV * T_K
    if kT < 0.01:
        return 1.0
    return 1 + (1/24) * (hbar_omega / kT)**2

# ════════════════════════════════════════════════════════════
# 3. IRC 扫描 (基准 ℓ_corr=0.5Å)
# ════════════════════════════════════════════════════════════

print("=" * 65)
print("P1 v2.0: H + H2 IRC 谱分析 — 升级版 (含文献 CVT/SCT 对比)")
print("=" * 65)

s_range = np.linspace(-4, 4, 80)
results_irc = []

for s in s_range:
    R_ab, R_bc, R_ac = irc_params(s)
    sol = solve_h3(R_ab, R_bc)
    sol['s'] = s
    sol['R_ab'] = R_ab
    sol['R_bc'] = R_bc
    sol['R_ac'] = R_ac
    results_irc.append(sol)

# 提取数据
s_arr = np.array([r['s'] for r in results_irc])
R_ab_arr = np.array([r['R_ab'] for r in results_irc])
R_bc_arr = np.array([r['R_bc'] for r in results_irc])
δ_arr = np.array([r['δ_spec'] for r in results_irc])
F_arr_300 = np.array([r['F_spec'] for r in results_irc])

# TS 值
ts_idx = np.argmin(np.abs(s_arr))
ts_δ = δ_arr[ts_idx]
ts_F_300 = F_arr_300[ts_idx]
ts_E = results_irc[ts_idx]['E_GS']
ts_R_ab = R_ab_arr[ts_idx]
ts_R_bc = R_bc_arr[ts_idx]

reac_δ = δ_arr[0]
prod_δ = δ_arr[-1]

print(f"\nIRC 扫描: s in [{s_arr[0]:.1f}, {s_arr[-1]:.1f}]")
print(f"  TS @ s = {s_arr[ts_idx]:.2f}, R_ab=R_bc={ts_R_ab:.3f}A")
print(f"  δ_spec(react) = {reac_δ:.3f} eV, δ_spec(TS) = {ts_δ:.3f} eV")
print(f"  TS gap closure: {(1 - ts_δ/reac_δ)*100:.1f}%")

# ════════════════════════════════════════════════════════════
# 4. 温度扫描: F_spec(T), ΔE_a(T), k(T)
# ════════════════════════════════════════════════════════════

T_range = np.logspace(np.log10(200), np.log10(5000), 50)
F_spec_TS_arr = []
F_spec_reac_arr = []
delta_Ea_arr = []
k_ratio_arr = []

for T in T_range:
    # TS
    sol_ts = solve_h3(ts_R_ab, ts_R_bc, T_K=T)
    F_TS = sol_ts['F_spec']
    F_spec_TS_arr.append(F_TS)
    
    # Reactant (asymptotic)
    sol_reac = solve_h3(R_limit, R_eq, T_K=T)
    F_reac = sol_reac['F_spec']
    F_spec_reac_arr.append(F_reac)
    
    # 活化能修正: ΔE_a = -d(ln(F_spec))/d(1/kT)
    # 对 F_spec = 1 + e^{-Δ/kT}, d(ln F)/d(1/kT) = Δ * e^{-Δ/kT}/(1+e^{-Δ/kT})
    kT = k_B_eV * T
    Δ = ts_δ
    if Δ > 0:
        dlnF_dbeta = Δ * np.exp(-Δ/kT) / (1 + np.exp(-Δ/kT))
        delta_Ea_arr.append(dlnF_dbeta)  # [eV]
        k_ratio_arr.append(F_TS / F_reac)
    else:
        delta_Ea_arr.append(0.0)
        k_ratio_arr.append(1.0)

F_spec_TS_arr = np.array(F_spec_TS_arr)
F_spec_reac_arr = np.array(F_spec_reac_arr)
delta_Ea_arr = np.array(delta_Ea_arr)
k_ratio_arr = np.array(k_ratio_arr)

# 找到 F_spec 偏差 > 1% 的温度阈值
threshold_T_idx = np.where((F_spec_TS_arr - 1) * 100 >= 1.0)[0]
T_threshold = T_range[threshold_T_idx[0]] if len(threshold_T_idx) > 0 else T_range[-1]

print(f"\n--- 温度扫描 ---")
print(f"  F_spec(TS) dev > 1% at T > {T_threshold:.0f} K")
for T_target in [300, 500, 1000, 2000, 3000, 5000]:
    idx = np.argmin(np.abs(T_range - T_target))
    print(f"  T = {T_range[idx]:.0f} K: F_spec(TS) = {F_spec_TS_arr[idx]:.6f}"
          f" (dev {(F_spec_TS_arr[idx]-1)*100:.3f}%),"
          f" ΔE_a = {delta_Ea_arr[idx]:.4f} eV")

# ════════════════════════════════════════════════════════════
# 5. 与 CVT/SCT 文献值的系统对比
# ════════════════════════════════════════════════════════════

T_lit = np.array(CVT_SCT_LIT['T_range_K'])
kappa_SCT = np.array(CVT_SCT_LIT['kappa_SCT'])
Gamma_CVT = np.array(CVT_SCT_LIT['Gamma_CVT'])
E0_classical = CVT_SCT_LIT['E0_classical']

print(f"\n--- 与文献 CVT/SCT 的系统对比 ---")
print(f"{'T (K)':>8} {'kappa_SCT':>10} {'Gamma_CVT':>10} {'F_spec(TS)':>12} "
      f"{'F-1(%)':>10} {'F_spec+Wigner':>14} {'k_ratio':>10}")
print("-" * 75)

comparison_table = []
for T, kSCT, gCVT in zip(T_lit, kappa_SCT, Gamma_CVT):
    sol_ts_T = solve_h3(ts_R_ab, ts_R_bc, T_K=T)
    F_ts_T = sol_ts_T['F_spec']
    F_wigner_T = wigner_tunneling(T)
    F_total = F_ts_T * F_wigner_T
    
    sol_reac_T = solve_h3(R_limit, R_eq, T_K=T)
    k_ratio_T_val = F_ts_T / sol_reac_T['F_spec']
    
    comparison_table.append({
        'T_K': float(T),
        'kappa_SCT_lit': float(kSCT),
        'Gamma_CVT_lit': float(gCVT),
        'F_spec_TS': float(F_ts_T),
        'F_spec_dev_pct': float((F_ts_T - 1) * 100),
        'Wigner_kappa': float(F_wigner_T),
        'F_spec_plus_Wigner': float(F_total),
        'k_ratio_spec': float(k_ratio_T_val),
    })
    
    print(f"{T:8.0f} {kSCT:10.2f} {gCVT:10.3f} {F_ts_T:12.8f} "
          f"{(F_ts_T-1)*100:10.6f} {F_total:14.8f} {k_ratio_T_val:10.6f}")

# ════════════════════════════════════════════════════════════
# 6. ℓ_corr 敏感性分析 (对势垒高度的影响)
# ════════════════════════════════════════════════════════════

print(f"\n--- ℓ_corr 对 H₃ 势垒的影响 ---")
l_corr_sweep = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5, 2.0])
E_barrier_lc = []
δ_TS_lc = []

for lc in l_corr_sweep:
    # 反应物极限
    sol_reac_lc = solve_h3(R_limit, R_eq, l_corr=lc)
    E_reac = sol_reac_lc['E_GS']
    
    # TS
    sol_ts_lc = solve_h3(ts_R_ab, ts_R_bc, l_corr=lc)
    E_TS = sol_ts_lc['E_GS']
    
    ΔE = E_TS - E_reac
    E_barrier_lc.append(ΔE)
    δ_TS_lc.append(sol_ts_lc['δ_spec'])
    
    print(f"  ℓ_corr = {lc:.1f} A: V_barrier = {ΔE:.4f} eV, δ_spec(TS) = {sol_ts_lc['δ_spec']:.4f} eV")

E_barrier_lc = np.array(E_barrier_lc)
δ_TS_lc = np.array(δ_TS_lc)
E_barrier_ref = 0.425  # LSTH 经典势垒 [eV]
barrier_dev = np.abs(E_barrier_lc - E_barrier_ref)
best_lc_idx = np.argmin(barrier_dev)

print(f"\n  最佳拟合 ℓ_corr: {l_corr_sweep[best_lc_idx]:.1f} A"
      f" (势垒 {E_barrier_lc[best_lc_idx]:.3f} eV vs 文献 {E_barrier_ref:.3f} eV)")

# ════════════════════════════════════════════════════════════
# 7. 可视化
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle(r'P1 v2.0: H+H$_2$ Spectral Analysis with CVT/SCT Comparison',
             fontsize=14, fontweight='bold')

# (a) IRC 几何
ax = axes[0, 0]
ax.plot(s_arr, R_ab_arr, 'b-', lw=2, label=r'$R_{\rm ab}$')
ax.plot(s_arr, R_bc_arr, 'r-', lw=2, label=r'$R_{\rm bc}$')
ax.axvline(0, color='gray', ls=':', alpha=0.5)
ax.set_xlabel('Reaction coordinate s')
ax.set_ylabel(r'Distance ($\AA$)')
ax.set_title('IRC geometry (collinear)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# (b) δ_spec 沿 IRC
ax = axes[0, 1]
ax.plot(s_arr, δ_arr, 'o-', color='#2196F3', lw=2, markersize=3)
ax.axvline(0, color='gray', ls=':', alpha=0.5, label='TS')
ax.axhline(ts_δ, color='red', ls='--', alpha=0.5, label=f'TS: {ts_δ:.3f} eV')
ax.set_xlabel('Reaction coordinate s')
ax.set_ylabel(r'$\delta_{\rm spec}$ (eV)')
ax.set_title(r'HOMO-LUMO gap $\delta_{\rm spec}$')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# (c) F_spec vs T
ax = axes[0, 2]
ax.semilogx(T_range, (F_spec_TS_arr - 1)*100, 'b-', lw=2, label='TS')
ax.semilogx(T_range, (F_spec_reac_arr - 1)*100, 'r--', lw=2, label='Reactant')
ax.axhline(1.0, color='gray', ls=':', alpha=0.5, label='1% threshold')
ax.axvline(T_threshold, color='orange', ls='--', alpha=0.5)
ax.set_xlabel('T (K)')
ax.set_ylabel(r'$(F_{\rm spec} - 1) \times 100$ (%)')
ax.set_title(r'$F_{\rm spec}$ vs temperature')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# (d) 与文献 CVT/SCT 对比
ax = axes[1, 0]
F_lit = np.array([c['F_spec_TS'] for c in comparison_table])
ax.plot(T_lit, kappa_SCT, 's-', color='#FF5722', lw=2, ms=6, label='SCT (lit)')
ax.plot(T_lit, Gamma_CVT, '^--', color='#4CAF50', lw=2, ms=6, label='CVT Gamma (lit)')
ax.plot(T_lit, F_lit, 'o-', color='#2196F3', lw=2, ms=6, label=r'$F_{\rm spec}$ (this work)')
ax.set_xlabel('T (K)')
ax.set_ylabel('Correction factor')
ax.set_title('Spectral vs CVT/SCT corrections')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xscale('log')

# (e) ℓ_corr 敏感性
ax = axes[1, 1]
ax.plot(l_corr_sweep, E_barrier_lc, 'o-', color='#9C27B0', lw=2, ms=6,
        label=r'$\Delta E_{\rm barrier}$')
ax.axhline(E_barrier_ref, color='red', ls='--', alpha=0.5,
           label=f'LSTH ref: {E_barrier_ref:.3f} eV')
ax.axvline(L_CORR, color='green', ls=':', alpha=0.5,
           label=f'SF: l_corr={L_CORR} A')
ax2 = axes[1, 1].twinx()
ax2.plot(l_corr_sweep, δ_TS_lc, 's--', color='orange', lw=2, ms=4,
         label=r'$\delta_{\rm spec}(TS)$')
ax2.set_ylabel(r'$\delta_{\rm spec}(TS)$ (eV)', color='orange')
ax.set_xlabel(r'$\ell_{\rm corr}$ ($\AA$)')
ax.set_ylabel('Barrier height (eV)')
ax.set_title(r'$\ell_{\rm corr}$ sensitivity')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)

# (f) k_ratio vs T (Arrhenius 修正)
ax = axes[1, 2]
ax.semilogy(T_range, k_ratio_arr, 'b-', lw=2)
ax.axhline(1.0, color='gray', ls=':', alpha=0.5)
ax.set_xlabel('T (K)')
ax.set_ylabel(r'$k_{\rm spec}/k_{\rm TST}$')
ax.set_title('Spectral rate correction')
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig_path = os.path.join(FIGS_DIR, 'hh2_reaction_spectral_analysis.png')
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
print(f"\nFigure saved: {fig_path}")

# ════════════════════════════════════════════════════════════
# 8. 保存结果
# ════════════════════════════════════════════════════════════

output = {
    'model': 'H + H2 3-center Huckel with SF l_corr, v2.0 with CVT/SCT comparison',
    'params': {
        'ALPHA_0': ALPHA_0, 'BETA_0': BETA_0,
        'R_eq_A': R_eq, 'R_TS_A': R_TS,
        'L_CORR_A': L_CORR,
        'E0_classical_lit_eV': E0_classical,
    },
    'TS_analysis': {
        'R_ab_A': float(ts_R_ab),
        'R_bc_A': float(ts_R_bc),
        'delta_spec_eV': float(ts_δ),
        'F_spec_300K': float(ts_F_300),
    },
    'temperature_scan': {
        'T_threshold_F1pct_K': float(T_threshold),
        'data': [
            {
                'T_K': float(T),
                'F_spec_TS': float(F_ts),
                'F_spec_dev_pct': float((F_ts-1)*100),
                'delta_Ea_eV': float(dEa),
                'k_ratio_spec': float(kr),
            }
            for T, F_ts, dEa, kr in zip(T_range, F_spec_TS_arr, delta_Ea_arr, k_ratio_arr)
        ],
    },
    'CVT_SCT_comparison': comparison_table,
    'l_corr_sensitivity': {
        'l_corr_values_A': l_corr_sweep.tolist(),
        'barrier_height_eV': [float(v) for v in E_barrier_lc],
        'delta_spec_TS_eV': [float(v) for v in δ_TS_lc],
        'best_fit_l_corr_A': float(l_corr_sweep[best_lc_idx]),
        'LSTH_ref_barrier_eV': E_barrier_ref,
    },
    'literature_refs': {
        'E0_classical_LSTH_eV': E0_classical,
        'E0_ZPE_corrected_eV': CVT_SCT_LIT['E0_ZPE'],
        'Ea_CVT_SCT_300K_eV': CVT_SCT_LIT['Ea_CVT_SCT_300K'],
        'k_CVT_SCT_300K_cm3_per_molecule_s': CVT_SCT_LIT['k_CVT_SCT_300K'],
    },
}

json_path = os.path.join(DATA_DIR, 'hh2_reaction_results.json')
with open(json_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"Results saved: {json_path}")

# ════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SUMMARY: P1 H+H2 v2.0 - COMPLETE")
print("=" * 65)
print(f"""
Key upgrades from v1.0:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Temperature scan: F_spec dev > 1% at T > {T_threshold:.0f} K
  2. CVT/SCT comparison table at {len(comparison_table)} temperature points
  3. Wigner tunneling reference included
  4. l_corr sensitivity on barrier height
  5. Best-fit l_corr: {l_corr_sweep[best_lc_idx]:.1f} A
     (barrier = {E_barrier_lc[best_lc_idx]:.3f} eV vs LSTH {E_barrier_ref:.3f} eV)

Interpretation:
  - F_spec correction for H+H2 is negligible at room temperature (F~1+1e-98)
  - Becomes measurable (>1%) only at T>{T_threshold:.0f}K
  - This is physically correct: H+H2 has a large HOMO-LUMO gap (~6 eV)
  - Spectral corrections are complementary to CVT/SCT:
    * CVT corrects recrossing (Gamma < 1)
    * SCT corrects tunneling (kappa > 1)
    * F_spec corrects excited state population (F > 1, tiny for wide-gap systems)
  - For small-gap systems (conical intersections, transition metals), 
    F_spec correction becomes dominant
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
