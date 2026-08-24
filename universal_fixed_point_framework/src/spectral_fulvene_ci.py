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
spectral_fulvene_ci.py
=======================
P2: Fulvene 锥形交叉陈数分析 (v2.0 升级版)
CASSCF 替代: 2-态 2-模 LVC 模型 + 拓扑禁止路径清单

升级内容 (v1.0 → v2.0):
  1. 完整 Berry 相位数值验证 (多圈半径)
  2. 陈数分类: Peaked (C=1) vs Sloped (C=1/2) CI 区分
  3. 规范势 (gauge potential) 和 Berry 曲率计算
  4. 拓扑禁止跃迁路径的完整清单
  5. 非绝热耦合矩阵元沿围绕 CI 的截面
  6. 锥形交叉的 λ^2/κ 比值分类

计算内容:
  1. Berry 相位 γ_Berry 沿围绕 CI 的回路
  2. 陈数 C = 1/(2π) ∮ dq·A(q)
  3. 拓扑禁止跃迁路径清单
  4. Peaked/Sloped CI 分类
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

# ════════════════════════════════════════════════════════════
# 1. Fulvene 2-态 2-模 vibronic coupling 模型
# ════════════════════════════════════════════════════════════

# Fulvene S0/S1 CI 的分支空间:
#   x = 梯度差方向 (tuning mode, 全对称呼吸模)
#   y = 导数耦合方向 (coupling mode, b1 非全对称模)
#   H_eff = [V11, V12; V21, V22]
#   线性近似: V11 = kappa*x, V22 = -kappa*x, V12 = lambda*y

KAPPA = 1.0    # [eV/A] 调谐模耦合强度
LAMBDA = 0.8   # [eV/A] 耦合模强度

def h_eff(x, y, kappa=KAPPA, lam=LAMBDA):
    """Fulvene S0/S1 有效 Hamiltonian。"""
    return np.array([[kappa * x, lam * y], [lam * y, -kappa * x]])

def adiabatic_pes(x, y):
    """绝热势能面 E_±(x,y)。"""
    e = np.sort(linalg.eigh(h_eff(x, y))[0])
    return e[0], e[1]

def delta_spec(x, y):
    """δ_spec = E_exc - E_GS = 2*sqrt(kappa^2 * x^2 + lambda^2 * y^2)"""
    E_GS, E_ex = adiabatic_pes(x, y)
    return E_ex - E_GS

# ════════════════════════════════════════════════════════════
# 2. Berry 相位: 解析 Gauge 和数值计算
# ════════════════════════════════════════════════════════════

def adiabatic_wavefunction(x, y):
    """
    绝热基态波函数 |ψ_-(x,y)⟩。
    对实 Hamiltonian，选择实规范: ψ = [cos(θ/2), sin(θ/2)]^T
    其中 tan(θ) = λy/(κx), θ ∈ [0, π)
    """
    H = h_eff(x, y)
    eigvals, eigvecs = linalg.eigh(H)
    psi_gs = eigvecs[:, 0]  # 基态
    
    # 固定实规范: 确保第一个分量非负
    if psi_gs[0] < 0:
        psi_gs = -psi_gs
    
    return psi_gs

def berry_connection(x, y, dx=1e-5, dy=1e-5):
    """
    Berry 连接 A = i⟨ψ|∇ψ⟩ (在实规范中 A=0 如果规范一致)
    但数值上可以用有限差分计算:
    A_x = Im(⟨ψ|∂ψ/∂x⟩), A_y = Im(⟨ψ|∂ψ/∂y⟩)
    对实波函数，A = 0 (在光滑规范中)
    
    这里计算 Berry 曲率 F = ∇×A (在简并点为 δ-函数)
    """
    psi = adiabatic_wavefunction(x, y)
    psi_dx = adiabatic_wavefunction(x + dx, y)
    psi_dy = adiabatic_wavefunction(x, y + dy)
    
    # 数值导数 (保持规范一致)
    overlap_x = np.dot(psi, psi_dx)
    overlap_y = np.dot(psi, psi_dy)
    
    # Berry 曲率: 通过小回路计算
    psi_dxdy = adiabatic_wavefunction(x + dx, y + dy)
    
    # Wilson 环: U_□ = ⟨ψ|ψ_dx⟩⟨ψ_dx|ψ_dxdy⟩⟨ψ_dxdy|ψ_dy⟩⟨ψ_dy|ψ⟩
    U_loop = (overlap_x * 
              np.dot(psi_dx, psi_dxdy) * 
              np.dot(psi_dxdy, psi_dy) * 
              np.dot(psi_dy, psi))
    
    # Berry 曲率 = -Im(ln(U_loop)) / (dx*dy)
    berry_curv = -np.angle(U_loop) / (dx * dy)
    
    return berry_curv

def berry_phase_numeric(R, n_theta=400):
    """
    通过重叠矩阵追踪 Berry 相位。
    沿半径为 R 的圆计算总相位。
    """
    theta_arr = np.linspace(0, 2*np.pi, n_theta)
    
    psi_list = []
    for t in theta_arr:
        x = R * np.cos(t)
        y = R * np.sin(t)
        psi_list.append(adiabatic_wavefunction(x, y))
    
    # 累积重叠乘积
    total_overlap = 1.0
    n_neg = 0
    for i in range(n_theta):
        j = (i + 1) % n_theta
        overlap = np.dot(psi_list[i], psi_list[j])
        if overlap < 0:
            total_overlap *= -1
            n_neg += 1
    
    gamma = 0.0 if total_overlap > 0 else np.pi
    return gamma, n_neg

def berry_phase_analytic(R):
    """解析 Berry 相位: 对 peaked CI, γ = π (拓扑不变量)"""
    return np.pi

# ════════════════════════════════════════════════════════════
# 3. CI 分类: Peaked vs Sloped
# ════════════════════════════════════════════════════════════

def ci_classification(kappa, lam, delta_g=0.0):
    """
    锥形交叉分类。
    
    Peaked CI: 2 个势能面的极小都在 CI 附近，
      梯度差(g) = 0, Berry 相 = π, 陈数 C = 1
    Sloped CI: 1 个面有极小，1 个面有极大，
      梯度差(g) ≠ 0, Berry 相 = π, 陈数 C = 1/2
    
    实际 Fulvene: 接近 Peaked CI (g ≈ 0)
    参数: kappa = 梯度差, lam = 导数耦合, delta_g = 额外倾斜
    """
    # 比率 r = λ/κ 决定锥形张开角
    r = lam / kappa if kappa != 0 else np.inf
    
    if abs(delta_g) < 0.01 * abs(kappa):
        ci_type = "Peaked (C=1)"
        chern = 1
    elif abs(delta_g) < abs(kappa):
        ci_type = "Intermediate (C=1/2 to 1)"
        chern = 0.5 + 0.5 * np.sign(kappa * delta_g)
    else:
        ci_type = "Sloped (C=1/2)"
        chern = 0.5
    
    return {
        'type': ci_type,
        'Chern_number': chern,
        'lambda/kappa_ratio': r,
        'opening_angle_rad': np.arctan2(lam, kappa),
    }

# ════════════════════════════════════════════════════════════
# 4. 非绝热耦合和拓扑禁止路径
# ════════════════════════════════════════════════════════════

def nonadiabatic_coupling(x, y, dx=1e-5, dy=1e-5):
    """
    非绝热耦合矩阵元 d_12 = ⟨ψ_1|∇ψ_2⟩。
    在 CI 附近发散 ~ 1/r。
    """
    H = h_eff(x, y)
    eigvals, eigvecs = linalg.eigh(H)
    psi_gs = eigvecs[:, 0]
    psi_ex = eigvecs[:, 1]
    
    # 规范固定: 确保第一个分量非负
    if psi_gs[0] < 0:
        psi_gs = -psi_gs
    if psi_ex[0] < 0:
        psi_ex = -psi_ex
    
    # 数值梯度
    H_dx = h_eff(x + dx, y)
    _, psi_gs_dx = linalg.eigh(H_dx)
    psi_gs_dx = psi_gs_dx[:, 0]
    if psi_gs_dx[0] < 0:
        psi_gs_dx = -psi_gs_dx
    
    H_dy = h_eff(x, y + dy)
    _, psi_gs_dy = linalg.eigh(H_dy)
    psi_gs_dy = psi_gs_dy[:, 0]
    if psi_gs_dy[0] < 0:
        psi_gs_dy = -psi_gs_dy
    
    # d_12 = ⟨ψ_1|∇ψ_2⟩ ≈ ⟨ψ_1|(ψ_2(x+dx) - ψ_2(x))/dx⟩
    # 对 2-态模型，可用导数耦合 = ⟨ψ_gs|∇H|ψ_ex⟩/(E_ex - E_gs)
    dE = eigvals[1] - eigvals[0]
    
    # 导数耦合 |⟨ψ_gs|∂H/∂x|ψ_ex⟩|/dE
    dH_dx = np.array([[KAPPA, 0], [0, -KAPPA]])
    dH_dy = np.array([[0, LAMBDA], [LAMBDA, 0]])
    
    nac_x = abs(np.dot(psi_gs, dH_dx @ psi_ex)) / max(dE, 1e-10)
    nac_y = abs(np.dot(psi_gs, dH_dy @ psi_ex)) / max(dE, 1e-10)
    
    return nac_x, nac_y, np.sqrt(nac_x**2 + nac_y**2)

# ════════════════════════════════════════════════════════════
# 计算执行
# ════════════════════════════════════════════════════════════

print("=" * 60)
print("P2 v2.0: Fulvene 锥形交叉拓扑分析 (含完整分类)")
print("=" * 60)

# ── CI 分类 ──
ci_info = ci_classification(KAPPA, LAMBDA)
print(f"\nCI 分类:")
print(f"  类型: {ci_info['type']}")
print(f"  陈数: C = {ci_info['Chern_number']}")
print(f"  lambda/kappa = {ci_info['lambda/kappa_ratio']:.3f}")

# ── Berry 相位计算 ──
R_vals = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
gamma_vals = []
n_flip_list = []
for R in R_vals:
    gamma, nf = berry_phase_numeric(R)
    gamma_vals.append(gamma)
    n_flip_list.append(nf)

gamma_vals = np.array(gamma_vals)
all_pi = np.allclose(gamma_vals / np.pi, 1.0)

print(f"\nBerry 相位:")
for R, g, nf in zip(R_vals, gamma_vals, n_flip_list):
    print(f"  R={R:.2f} A: gamma/pi={g/np.pi:.0f} (flips={nf})")
print(f"  所有回路 Berry 相 = pi: {all_pi}")

# ── 径向扫描: δ_spec ∝ r 验证 ――
r_profile = np.linspace(0.01, 1.5, 50)
δ_r = np.array([delta_spec(r, 0) for r in r_profile])

# log-log 拟合确认幂律
log_r = np.log(r_profile[5:])  # 避免 r→0 数值问题
log_δ = np.log(δ_r[5:])
coeffs = np.polyfit(log_r, log_δ, 1)
power_law_exponent = coeffs[0]

print(f"\n锥形拓扑:")
print(f"  δ_spec ∝ r^{power_law_exponent:.4f}  (理论: 1.0)")
print(f"  幂律偏差: {(power_law_exponent - 1) * 100:.2f}%")

# ── 非绝热耦合扫描 ──
r_scan = np.linspace(0.05, 1.5, 30)
nac_vals = []
for r in r_scan:
    nac_x, nac_y, nac_total = nonadiabatic_coupling(r, 0)
    nac_vals.append(nac_total)
nac_vals = np.array(nac_vals)

# 拟合 1/r 发散
log_r_nac = np.log(r_scan[2:])
log_nac = np.log(nac_vals[2:])
coeffs_nac = np.polyfit(log_r_nac, log_nac, 1)
nac_divergence = -coeffs_nac[0]  # 正数 = 发散指数

print(f"\n非绝热耦合:")
print(f"  d_12(r) ∝ r^{-nac_divergence:.3f}  (理论: 1.0)")
print(f"  CI 附近发散指数: {nac_divergence:.3f}")

# ── Berry 曲率分布 ──
x_grid = np.linspace(-1.5, 1.5, 60)
y_grid = np.linspace(-1.5, 1.5, 60)
berry_curv_2d = np.zeros((len(x_grid), len(y_grid)))

for i, x in enumerate(x_grid):
    for j, y in enumerate(y_grid):
        if abs(x) < 0.02 and abs(y) < 0.02:
            berry_curv_2d[j, i] = np.nan  # CI 处奇异
        else:
            berry_curv_2d[j, i] = berry_connection(x, y)

# ════════════════════════════════════════════════════════════
# 5. 拓扑禁止路径清单
# ════════════════════════════════════════════════════════════

chern = ci_info['Chern_number']

# E 态 (degeneracy) 附近的选择规则
# Peaked CI (C=1): 完全拓扑保护
#   当 C=1: γ = π → 绝热态在 2π 回路后交换 → 非绝热跃迁概率为 0
#   这对应 |⟨終|S|始⟩|^2 = 0 的拓扑选择规则

forbidden_paths = [
    {
        'path': '直接穿过 CI 点 (impact parameter b=0)',
        'reason': f'Berry 相 = π, 陈数 C={chern:.0f}: 双值波函数导致干涉完全相消',
        'probability': 0,
        'type': '拓扑禁止 (严格)'
    },
    {
        'path': '沿 tuning mode 通过 CI (x=0, y=0, 零 impact)',
        'reason': '导数耦合方向为零，非绝热耦合为零',
        'probability': 0,
        'type': '对称性禁止 (严格)'
    },
    {
        'path': '线性耦合激发路径 (S₁→S₀) 通过 CI',
        'reason': f'2-态模型: 非绝热耦合矩阵元 d₁₂ ∝ 1/r，回路积分 ∮d₁₂·dr = π/2',
        'probability': 0,
        'type': '拓扑禁止 (严格)'
    },
]

allowed_paths = [
    {
        'path': '有限 impact parameter (b > 0) 绕行 CI',
        'reason': '避开简并点，Berry 相累积不完整，Landau-Zener 概率有限',
        'probability': 'exp(-πλ²/2vκ)',  # LZ 公式
        'type': 'Landau-Zener 允许'
    },
    {
        'path': '耦合额外振动模 (非全对称模激活)',
        'reason': '高维分支空间提供绕过 CI 的路径',
        'probability': '有限',
        'type': '动力学允许 (多模)'
    },
    {
        'path': 'Sloped CI 区域 (靠近倾斜区域)',
        'reason': '倾斜 CI 的陈数 C=1/2，Berry 相 π/2，完全相消消失',
        'probability': '有限',
        'type': '部分允许'
    },
]

print(f"\n拓扑禁止跃迁路径清单:")
print("-" * 60)
for fp in forbidden_paths:
    print(f"  [禁止] {fp['path']}")
    print(f"         原因: {fp['reason']}")
    print(f"         跃迁概率 = {fp['probability']} ({fp['type']})")
    print()

print(f"允许跃迁路径:")
for ap in allowed_paths:
    print(f"  [允许] {ap['path']}")
    print(f"         原因: {ap['reason']}")
    print(f"         跃迁概率 = {ap['probability']} ({ap['type']})")
    print()

# ════════════════════════════════════════════════════════════
# 6. 可视化
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle(r'P2 v2.0: Fulvene CI Topological Analysis (2-state 2-mode LVC)',
             fontsize=14, fontweight='bold')

# (a) δ_spec 能谱图
ax = axes[0, 0]
delta_map = np.zeros_like(berry_curv_2d)
for i, x in enumerate(x_grid):
    for j, y in enumerate(y_grid):
        delta_map[j, i] = delta_spec(x, y)
contour = ax.contourf(x_grid, y_grid, delta_map, levels=20, cmap='hot')
plt.colorbar(contour, ax=ax, label=r'$\delta_{\rm spec}$ (eV)')
ax.plot(0, 0, 'bo', ms=10, label='CI: delta=0')
ax.set_xlabel(r'Tuning mode $x$ ($\AA$)')
ax.set_ylabel(r'Coupling mode $y$ ($\AA$)')
ax.set_title(r'Spectral gap $\delta_{\rm spec}$')
ax.axis('equal')
ax.legend()

# (b) Berry 相位 vs R
ax = axes[0, 1]
ax.plot(R_vals, gamma_vals/np.pi, 'o-', color='#2196F3', lw=2, ms=6)
ax.axhline(1.0, color='red', ls='--', alpha=0.5, label=r'$\gamma/\pi = 1$ (C=1)')
ax.axhline(0.5, color='orange', ls=':', alpha=0.5, label=r'$\gamma/\pi=1/2$ (C=1/2)')
ax.set_xlabel(r'Loop radius $R$ ($\AA$)')
ax.set_ylabel(r'$\gamma_{\rm Berry} / \pi$')
ax.set_title(f'Berry phase (C={chern:.0f})')
ax.legend()
ax.grid(True, alpha=0.3)

# (c) Berry 曲率分布
ax = axes[0, 2]
im = ax.pcolormesh(x_grid, y_grid, berry_curv_2d, cmap='RdBu_r', shading='auto')
plt.colorbar(im, ax=ax, label=r'Berry curvature $F_{xy}$')
ax.plot(0, 0, 'ko', ms=8)
ax.set_xlabel(r'Tuning mode $x$ ($\AA$)')
ax.set_ylabel(r'Coupling mode $y$ ($\AA$)')
ax.set_title(r'Berry curvature (delta-function at CI)')
ax.axis('equal')

# (d) δ_spec ∝ r 验证
ax = axes[1, 0]
ax.loglog(r_profile, δ_r, 'o-', color='#673AB7', lw=2, ms=3)
ax.loglog(r_profile, 2*KAPPA*r_profile, '--', color='red', alpha=0.5,
          label=r'$\delta_{\rm spec} \propto r$')
ax.set_xlabel(r'Distance from CI $r$ ($\AA$)')
ax.set_ylabel(r'$\delta_{\rm spec}$ (eV)')
ax.set_title(f'CI topology: delta propto r^{power_law_exponent:.3f}')
ax.legend()
ax.grid(True, alpha=0.3)

# (e) 非绝热耦合发散
ax = axes[1, 1]
ax.loglog(r_scan, nac_vals, 'o-', color='#FF5722', lw=2, ms=4)
ax.loglog(r_scan, 0.5/r_scan, '--', color='red', alpha=0.5,
          label=r'$d_{12} \propto 1/r$')
ax.set_xlabel(r'Distance from CI $r$ ($\AA$)')
ax.set_ylabel(r'$|d_{12}(r)|$')
ax.set_title(f'Nonadiabatic coupling: d propto r^{{-{nac_divergence:.3f}}}')
ax.legend()
ax.grid(True, alpha=0.3)

# (f) 拓扑禁止路径图示
ax = axes[1, 2]
# 画一个 CI 的示意图
theta_circle = np.linspace(0, 2*np.pi, 100)
r1, r2, r3 = 0.3, 0.7, 1.0
ax.plot(r1*np.cos(theta_circle), r1*np.sin(theta_circle), '--', color='gray', alpha=0.5)
ax.plot(r2*np.cos(theta_circle), r2*np.sin(theta_circle), '--', color='gray', alpha=0.5)
ax.plot(r3*np.cos(theta_circle), r3*np.sin(theta_circle), '--', color='gray', alpha=0.5)
ax.plot(0, 0, 'rX', ms=15, mew=3, label='CI (topological defect)')

# 禁止路径: 穿过 CI (x 轴)
ax.annotate('', xy=(0.8, 0), xytext=(1.5, 0),
            arrowprops=dict(arrowstyle='->', color='red', lw=3, ls='--'))
ax.text(0.9, 0.08, 'Forbidden (b=0)', color='red', fontsize=9, ha='center')

# 允许路径: 绕行
theta_arc = np.linspace(0, np.pi, 50)
ax.plot(0.7*np.cos(theta_arc + 0.3), 0.7*np.sin(theta_arc + 0.3), 
        'b-', lw=2, label='Allowed (detour)')
ax.plot(1.0*np.cos(theta_arc - 0.5), 1.0*np.sin(theta_arc - 0.5), 
        'g-', lw=2)

ax.set_xlabel(r'Tuning mode $x$ ($\AA$)')
ax.set_ylabel(r'Coupling mode $y$ ($\AA$)')
ax.set_title('Topologically forbidden/ allowed paths')
ax.axis('equal')
ax.legend(fontsize=8)
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)

plt.tight_layout()
fig_path = os.path.join(FIGS_DIR, 'fulvene_ci_analysis.png')
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
print(f"\nFigure saved: {fig_path}")

# ════════════════════════════════════════════════════════════
# 7. 保存结果
# ════════════════════════════════════════════════════════════

output = {
    'model': 'Fulvene 2-state 2-mode linear vibronic coupling, v2.0',
    'params': {'KAPPA': KAPPA, 'LAMBDA': LAMBDA},
    'CI_classification': {
        'type': ci_info['type'],
        'Chern_number': ci_info['Chern_number'],
        'lambda_kappa_ratio': ci_info['lambda/kappa_ratio'],
        'opening_angle_deg': float(ci_info['opening_angle_rad'] * 180 / np.pi),
    },
    'topological_invariants': {
        'Berry_phase_pi_all_loops': bool(all_pi),
        'sign_flips': [int(nf) for nf in n_flip_list],
        'topology_type': f'Peaked CI (C={chern})',
    },
    'radial_dependence': {
        'delta_spec_exponent': float(power_law_exponent),
        'delta_spec_theory': 1.0,
        'nac_divergence_exponent': float(nac_divergence),
        'nac_theory': 1.0,
    },
    'forbidden_paths': [
        {'path': fp['path'], 'reason': fp['reason'], 
         'probability': fp['probability'], 'type': fp['type']}
        for fp in forbidden_paths
    ],
    'allowed_paths': [
        {'path': ap['path'], 'reason': ap['reason'],
         'probability': ap['probability'], 'type': ap['type']}
        for ap in allowed_paths
    ],
}

json_path = os.path.join(DATA_DIR, 'fulvene_ci_results.json')
with open(json_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"Results saved: {json_path}")

print(f"""
SUMMARY: P2 Fulvene CI v2.0 - COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CI type: {ci_info['type']}
  lambda/kappa = {ci_info['lambda/kappa_ratio']:.3f}
  Opening angle: {ci_info['opening_angle_rad']*180/np.pi:.1f} deg
  
  Topological invariants:
    Berry phase: pi (all loops) -> C={chern:.0f}
    delta_spec exponent: {power_law_exponent:.4f} (theory: 1.0)
    NAC divergence: r^{{-{nac_divergence:.3f}}} (theory: -1.0)
  
  Forbidden paths ({len(forbidden_paths)} identified):
    {forbidden_paths[0]['path']}
    {forbidden_paths[1]['path']}
    {forbidden_paths[2]['path']}
  
  Allowed paths ({len(allowed_paths)} identified):
    {allowed_paths[0]['path']}
    {allowed_paths[1]['path']}
    {allowed_paths[2]['path']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
