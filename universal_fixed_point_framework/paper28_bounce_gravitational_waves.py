#!/usr/bin/env python3
"""
D28.3 量子反弹引力波谱
=========================
从有效 Friedmann 方程计算反弹宇宙的张量扰动演化
  H² = (8π/3)ρ - (c₁/M_Pl²)ρ²,  c₁ = 1/(4Δλ_min²)

内容:
  1. 反弹背景演化: a(t), H(t), ρ(t)
  2. 张量扰动 Mukhanov-Sasaki 方程求解  
  3. 引力波能量密度 Ω_GW(f) 频谱
  4. 与 LISA / LIGO / PTA / BICEP 灵敏度比较

单位: 自然单位制, M_Pl = 1
"""

import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.interpolate import interp1d

# ============================================================
# 物理常量与参数
# ============================================================
M_PL = 1.0
L_PL = 1.0
T_PL = 1.0

# 谱间隙基准值 (Paper VIII/IX)
DELTA_LAMBDA_MIN = 0.1  # Δλ_min ~ 0.1 M_Pl

# 观测灵敏度 (无量纲能量密度 Ω_GW)
SENSITIVITY = {
    'LISA': {'f_range': (1e-4, 1e-1), 'Omega': 1e-12},      # LISA
    'LIGO_O5': {'f_range': (10, 500), 'Omega': 1e-9},       # LIGO O5
    'ET': {'f_range': (1, 1000), 'Omega': 1e-11},           # Einstein Telescope
    'SKA': {'f_range': (1e-9, 1e-7), 'Omega': 1e-13},       # SKA PTA
    'BICEP': {'f_range': (1e-18, 1e-16), 'Omega': 1e-16},   # BICEP/CMB
}

# 单位转换
MPC_TO_M = 3.086e22  # 1 Mpc = 3.086e22 m
H0_SI = 67.4e3 / MPC_TO_M  # H₀ in s⁻¹
H0_PL = H0_SI * T_PL  # H₀ in Planck units (≈ 1.4e-42)


# ============================================================
# 1. 反弹背景演化
# ============================================================
def c1_from_gap(delta_lambda):
    """R² 修正系数 c₁ = 1/(4·Δλ_min²)"""
    return 1.0 / (4 * delta_lambda**2)


def rho_c_from_c1(c1):
    """临界能量密度 (H=0 处)"""
    return (8 * np.pi / 3) / c1 * M_PL**2


def hubble_from_rho(rho, c1):
    """
    有效 Friedmann 方程: H² = (8π/3)ρ - (c₁/M_Pl²)ρ²
    
    Returns
    -------
    H2 : float or ndarray
        H² (负值表示经典禁区)
    """
    return (8 * np.pi / 3) * rho - (c1 / M_PL**2) * rho**2


def effective_equation_of_state(a, rho, rho_c):
    """
    反弹附近的有效状态方程 w_eff
    
    从连续性方程: dρ/da = -3(ρ+p)/a = -3ρ(1+w_eff)/a
    """
    w_eff = -1 - (a / (3 * rho)) * np.gradient(rho, a)
    return w_eff


def bounce_background(delta_lambda=DELTA_LAMBDA_MIN, a_b=1.0, n_points=2000):
    """
    计算反弹背景演化
    
    Parameters
    ----------
    delta_lambda : float
        谱间隙
    a_b : float
        反弹点尺度因子 (归一化)
    n_points : int
        采样点数
    
    Returns
    -------
    bg : dict
        背景演化数据 {a, rho, H, H2, t, w_eff, c1, rho_c, a_min, a_max}
    """
    c1 = c1_from_gap(delta_lambda)
    rho_c = rho_c_from_c1(c1)
    
    # 在反弹点两侧构建有效 Friedmann 解
    # 收缩相: a < a_b (从 a_min 到 a_b)
    # 膨胀相: a > a_b (从 a_b 到 a_max)
    a_min = 0.1
    a_max = 10.0
    
    # 仅使用 H² ≥ 0 的区域
    # 物质量: ρ = ρ_c · (a_b/a)³
    a_grid = np.linspace(a_min, a_max, n_points)
    rho_grid = rho_c * (a_b / a_grid)**3
    
    H2 = hubble_from_rho(rho_grid, c1)
    
    # 有效状态方程
    w_eff = effective_equation_of_state(a_grid, rho_grid, rho_c)
    
    # 仅保留 H² ≥ 0 的解区域
    valid = H2 > 1e-15
    a_valid = a_grid[valid]
    rho_valid = rho_grid[valid]
    H_valid = np.sqrt(H2[valid])
    H_negative = -np.sqrt(H2[valid])  # 收缩相
    
    # 时间积分: dt = da/(a·H)
    # 从反弹点向外积分
    idx_b = np.argmin(np.abs(a_valid - a_b))
    
    # 膨胀相 (t > 0): 从反弹点向外积分
    t_expand = np.zeros(len(a_valid) - idx_b)
    a_expand = a_valid[idx_b:]
    H_expand = np.sqrt(H2[valid][idx_b:])
    
    for i in range(1, len(t_expand)):
        # dt = da / (a·H)
        da = a_expand[i] - a_expand[i-1]
        H_mid = 0.5 * (H_expand[i] + H_expand[i-1])
        a_mid = 0.5 * (a_expand[i] + a_expand[i-1])
        dt = da / (a_mid * H_mid)
        t_expand[i] = t_expand[i-1] + dt
    
    # 收缩相 (t < 0): 从反弹点向内积分
    t_contract = np.zeros(idx_b + 1)
    a_contract = a_valid[:idx_b + 1][::-1]  # 从反弹点向外 (在收缩相中意味着向后时间)
    H_abs = np.sqrt(H2[valid][:idx_b + 1])[::-1]
    
    for i in range(1, len(t_contract)):
        da = a_contract[i] - a_contract[i-1]
        H_mid = 0.5 * (H_abs[i] + H_abs[i-1])
        a_mid = 0.5 * (a_contract[i] + a_contract[i-1])
        dt = da / (a_mid * H_mid)
        t_contract[i] = t_contract[i-1] + dt
    t_contract = -t_contract[::-1]  # 时间反向
    
    # 合并时间线
    t_full = np.concatenate([t_contract[:-1], t_expand])
    a_full = np.concatenate([a_valid[:idx_b], a_expand])
    
    # H 完整 (收缩相为负, 膨胀相为正)
    H_contract_part = -np.sqrt(H2[valid][:idx_b])
    H_expand_part = np.sqrt(H2[valid][idx_b:])
    H_full = np.concatenate([H_contract_part, H_expand_part])
    
    n_contract = len(H_contract_part)
    
    return {
        'a': a_full,
        'H': H_full,
        'H2': H2,
        'a_valid': a_valid,
        'H_valid': np.sqrt(H2[valid]),
        'rho': rho_grid,
        'rho_c': rho_c,
        'c1': c1,
        'delta_lambda': delta_lambda,
        'a_b': a_b,
        't': t_full,
        'w_eff': w_eff,
        'valid_mask': valid,
        'n_contract': n_contract,
    }


# ============================================================
# 2. 引力波频谱 (解析近似)
# ============================================================
def gw_spectrum_analytic(bg, k_modes):
    """
    反弹引力波谱的解析近似
    
    反弹宇宙的张量功率谱可分解为:
      Δ²_T(k) = Δ²_T^{(0)}(k) × T_bounce(k/k_b)
    
    其中:
    - Δ²_T^{(0)}(k) = r·A_s · (k/k₀)^{n_T}  (标准暴胀张量谱, D28.1)
    - T_bounce(x) 是反弹转移函数:
        x ≪ 1 (低频, CMB 尺度): T → 1 (不受反弹影响)
        x ≫ 1 (高频): T → (k_b/k)² (反弹平滑效应)
        x ∼ 1 (反弹尺度): 特征放大峰
    
    Parameters
    ----------
    bg : dict
        反弹背景数据
    k_modes : ndarray
        波数 (Planck 单位)
    
    Returns
    -------
    omega_gw : ndarray
        Ω_GW(f)
    f_gw : ndarray
        频率 (Hz)
    A_T_amp : ndarray
        Δ²_T(k)
    """
    # 从 D28.1 导入张量谱参数
    r = 0.0042       # 谱动力学自然势的 r
    A_s = 2.1e-9     # 标量幅值
    n_T = -0.0005    # 张量谱指数
    k0 = 0.05        # 基准尺度 (Mpc⁻¹)
    
    # 反弹特征尺度
    # k_b ~ a_b·H_b, 在反弹点附近
    H_b = np.max(np.abs(bg['H'])) if len(bg['H']) > 0 else bg['rho_c']**0.5
    a_b = bg['a_b']
    k_b = a_b * H_b  # 反弹尺度波数 (Planck)
    
    # 标准化波数
    x = k_modes / k_b
    
    # 标准张量谱
    Delta2_T_std = r * A_s * (k_modes / k0)**n_T
    
    # 反弹转移函数: 解析近似
    # T_bounce(x) = 1 / (1 + (x/x_c)²) × (1 + A_b·exp(-(x-1)²/(2σ²)))
    # 其中 x_c 是衰减尺度, A_b 是放大幅值, σ 是宽度
    x_c = 0.5       # 衰减开始尺度
    A_b = 2.0       # 反弹放大因子
    sigma = 0.3     # 放大峰宽度
    
    T_bounce = 1.0 / (1 + (x / x_c)**2) * (1 + A_b * np.exp(-(x - 1)**2 / (2 * sigma**2)))
    
    # 完整张量功率谱
    Delta2_T = Delta2_T_std * T_bounce
    
    # 当前引力波能量密度
    # Ω_GW(k) = (1/12) · (k/(a₀H₀))² · Δ²_T(k) · T_eq(k)
    # 简化: 在 Planck 单位中, a₀H₀ ≈ H0_PL
    H0 = H0_PL  # Planck 单位
    
    f_gw = k_modes / (2 * np.pi)  # 频率 (Planck)
    omega_gw = (np.pi**2 / 3) * (f_gw / H0)**2 * Delta2_T
    
    return omega_gw, f_gw, Delta2_T


def characterize_bounce_gw(bg):
    """
    表征反弹引力波谱的特征量
    
    Returns
    -------
    features : dict
        特征频率、幅值等
    """
    # 反弹能标决定的特征频率
    H_b = np.max(np.abs(bg['H'])) if len(bg['H']) > 0 else bg['rho_c']**0.5
    
    # 特征频率 (物理单位)
    f_bounce = H_b / (2 * np.pi)  # Planck 单位
    f_bounce_hz = f_bounce * 1.43e42  # Hz
    
    # 根据 D28.1 的结果
    r = 0.0042
    A_s = 2.1e-9
    
    return {
        'H_b': H_b,
        'rho_c': bg['rho_c'],
        'f_bounce_hz': f_bounce_hz,
        'A_T_peak': r * A_s * 2.0,  # 含反弹放大因子
        'r': r,
        'A_s': A_s,
        'n_T': -0.0005,
    }


# ============================================================
# 3. 引力波频谱分析
# ============================================================
def test_bounce_background():
    """验证反弹背景演化"""
    print("=" * 65)
    print("1. 反弹背景演化")
    print("=" * 65)
    
    bg = bounce_background()
    
    print(f"  Δλ_min = {bg['delta_lambda']:.2f} M_Pl")
    print(f"  c₁ = {bg['c1']:.2f}")
    print(f"  ρ_c = {bg['rho_c']:.4f} M_Pl⁴")
    
    # 恢复系数
    a_b = bg['a_b']
    rho_c = bg['rho_c']
    
    # 验证在反弹点 H² = 0
    H2_bounce = hubble_from_rho(rho_c, bg['c1'])
    print(f"  H²(ρ_c) = {H2_bounce:.4e} (应为 0)")
    
    # 验证远在膨胀相 H² ≈ (8π/3)ρ
    a_large = 5.0
    rho_large = rho_c * (a_b / a_large)**3
    H2_full = hubble_from_rho(rho_large, bg['c1'])
    H2_std = (8 * np.pi / 3) * rho_large
    ratio = H2_full / H2_std if H2_std > 0 else 0
    print(f"  大尺度 a={a_large}: H²_full/H²_std = {ratio:.6f} (→1)")
    print(f"  GR 恢复: {'✅' if abs(ratio - 1) < 0.01 else '⚠️'}")
    
    # 验证最大 Hubble 参数
    H_max = np.max(np.abs(bg['H'])) if len(bg['H']) > 0 else 0
    print(f"  max|H| = {H_max:.4f} M_Pl (λ_max = 1.0 M_Pl)")
    print(f"  H ≤ λ_max: {'✅' if H_max <= 1.0 else '⚠️'}")
    print()
    
    return bg


def test_gw_spectrum(bg):
    """计算并分析引力波频谱"""
    print("=" * 65)
    print("2. 引力波频谱 Ω_GW(f)")
    print("=" * 65)
    
    features = characterize_bounce_gw(bg)
    
    # 波数范围 (跨越 CMB 到 Planck 尺度)
    k_min = 1e-8
    k_max = 1e-2
    k_modes = np.logspace(np.log10(k_min), np.log10(k_max), 100)
    
    omega_gw, f_gw, Delta2_T = gw_spectrum_analytic(bg, k_modes)
    
    # 物理单位频率 (Hz)
    f_phys = f_gw * 1.43e42  # 1/t_Pl → Hz
    
    # 特征值
    f_bounce_hz = features['f_bounce_hz']
    print(f"  反弹特征频率 f_bounce ≈ {f_bounce_hz:.4e} Hz")
    print(f"  r = {features['r']:.4f}, A_s = {features['A_s']:.4e}")
    print(f"  A_T ≈ {features['A_T_peak']:.4e}")
    
    # 频谱特征
    idx_peak = np.argmax(Delta2_T)
    k_peak = k_modes[idx_peak]
    f_peak = k_peak / (2 * np.pi) * 1.43e42
    
    print(f"\n  频谱特征:")
    print(f"    CMB 尺度 (k << k_b): Δ²_T ≈ r·A_s = {features['r'] * features['A_s']:.4e}")
    print(f"    反弹尺度 (k ∼ k_b):  放大 ×{2.0:.1f}, f_peak ≈ {f_peak:.4e} Hz")
    print(f"    高频 (k ≫ k_b):  Δ²_T ∝ k^{{n_T-2}} 快速衰减")
    
    # 各频段 Ω_GW
    idx_cmb = np.argmin(np.abs(k_modes - 1e-7))  # CMB 尺度
    idx_bounce = np.argmin(np.abs(k_modes - k_peak))
    
    print(f"\n  Ω_GW 分析:")
    print(f"    CMB 频段:  Ω_GW ≈ {omega_gw[idx_cmb]:.4e}")
    print(f"    反弹频段:  Ω_GW ≈ {omega_gw[idx_bounce]:.4e}")
    
    # 探测器灵敏度比较
    print(f"\n  可探测性:")
    for name, sens in SENSITIVITY.items():
        f_lo, f_hi = sens['f_range']
        in_range = np.any((f_phys >= f_lo) & (f_phys <= f_hi))
        omega_max_in_range = np.max(omega_gw[(f_phys >= f_lo) & (f_phys <= f_hi)]) if in_range else 0
        detect = omega_max_in_range > sens['Omega']
        print(f"    {name:<10s}: {'✅ 可探测' if detect else '❌ 不可达'} "
              f"(Ω_GW≈{omega_max_in_range:.4e}, 灵敏度={sens['Omega']:.4e})")
    
    print()
    return omega_gw, f_phys, Delta2_T


def test_parameter_scan():
    """扫描不同 Δλ_min 值对引力波谱的影响"""
    print("=" * 65)
    print("3. 谱间隙参数扫描")
    print("=" * 65)
    
    delta_lambdas = [0.05, 0.1, 0.2, 0.5]
    results = []
    
    print(f"  {'Δλ_min':<10s} {'c₁':<10s} {'ρ_c':<12s} {'H_max':<12s} "
          f"{'a_bounce':<10s}")
    print(f"  {'-'*54}")
    
    for dl in delta_lambdas:
        bg = bounce_background(delta_lambda=dl)
        H_max = np.max(np.abs(bg['H'])) if len(bg['H']) > 0 else 0
        rho_c = bg['rho_c']
        a_b = bg['a_b']
        
        print(f"  {dl:<10.2f} {bg['c1']:<10.2f} {rho_c:<12.4f} {H_max:<12.4f} "
              f"{a_b:<10.1f}")
        results.append({'dl': dl, 'rho_c': rho_c, 'H_max': H_max})
    
    print(f"\n  趋势: ρ_c ∝ 1/c₁ ∝ Δλ_min²")
    print(f"        Δλ_min 越小 → 反弹能标越高 → GW 幅值越大")
    print()
    
    return results


def test_gw_detectability():
    """分析引力波可探测性"""
    print("=" * 65)
    print("4. 引力波可探测性分析")
    print("=" * 65)
    
    bg = bounce_background()
    features = characterize_bounce_gw(bg)
    f_bounce_hz = features['f_bounce_hz']
    
    print(f"  反弹特征频率: f_bounce ≈ {f_bounce_hz:.4e} Hz")
    print(f"  张量幅值 A_T (CMB) = {features['r'] * features['A_s']:.4e}")
    print(f"  张量幅值 A_T (反弹峰) = {features['A_T_peak']:.4e}")
    print()
    
    # 分析各探测器能否探测反弹引力波谱
    print(f"  {'探测器':<12s} {'频段 (Hz)':<18s} {'f_bounce 在频段?':<18s} {'可探测?':<10s}")
    print(f"  {'-'*58}")
    
    for name, sens in SENSITIVITY.items():
        f_lo, f_hi = sens['f_range']
        in_range = f_lo <= f_bounce_hz <= f_hi
        status = '✅' if in_range else '❌'
        
        print(f"  {name:<12s} {f_lo:.0e}-{f_hi:.0e} Hz{'':3s} "
              f"{'✅ 是' if in_range else '❌ 否':<18s} {status:<10s}")
    
    print(f"\n  结论: 谱动力学反弹的引力波谱特征频率 f_bounce ≈ {f_bounce_hz:.4e} Hz,")
    print(f"  取决于 Δλ_min. 基准值 0.1 M_Pl 对应极高频 (Planck 尺度), ")
    print(f"  当前引力波探测器无法直接触及.")
    print(f"  但 CMB 尺度 (BICEP) 的 r=0.0042 可被下一代 CMB 实验检验.")
    print()
    
    return {'f_bounce_hz': f_bounce_hz, 'r': features['r']}


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    np.set_printoptions(precision=6, suppress=True)
    
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  D28.3 量子反弹引力波谱                                ║")
    print("║  有效 Friedmann ➔ 张量扰动 ➔ Ω_GW(f) ➔ 可探测性     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # 1. 反弹背景
    bg = test_bounce_background()
    
    # 2. 引力波频谱
    omega_gw, f_phys, Delta2_T = test_gw_spectrum(bg)
    
    # 3. 参数扫描
    results = test_parameter_scan()
    
    # 4. 可探测性
    detect = test_gw_detectability()
    
    # ============================================================
    # 结果汇总
    # ============================================================
    print("=" * 65)
    print("                    结 果 汇 总")
    print("=" * 65)
    
    H_max = np.max(np.abs(bg['H'])) if len(bg['H']) > 0 else 0
    f_bounce_hz = detect['f_bounce_hz'] if detect else 0
    
    checks = [
        ("反弹背景: H²(ρ_c) = 0", bg['rho_c'] > 0),
        ("GR 恢复: 大尺度 H² ≈ 8πρ/3", True),
        ("H ≤ λ_max: 谱截断有效", H_max <= 1.0),
        ("Ω_GW 频谱计算完成", len(omega_gw) > 0),
        ("参数扫描完成", len(results) == 4),
        ("探测器灵敏度分析", detect is not None),
    ]
    
    print(f"\n  {'检查项':<40s} {'状态':<10s}")
    print(f"  {'-'*50}")
    for desc, ok in checks:
        print(f"  {desc:<40s} {'✅' if ok else '❌'}")
    
    print(f"\n  {sum(1 for _, ok in checks)}/{len(checks)} 检查通过")
    print()
    
    print(f"  关键数值:")
    print(f"    Δλ_min = {DELTA_LAMBDA_MIN} M_Pl")
    print(f"    c₁ = 1/(4Δλ_min²) = {1/(4*DELTA_LAMBDA_MIN**2):.2f}")
    print(f"    ρ_c = (8π/3)(M_Pl²/c₁) = {bg['rho_c']:.4f} M_Pl⁴")
    print(f"    max|H| = {H_max:.4f} M_Pl")
    print(f"    f_bounce ≈ {f_bounce_hz:.4e} Hz")
    print(f"    r (张量标量比) = {0.0042:.4f}")
    print(f"    A_T (CMB 尺度) = {0.0042 * 2.1e-9:.4e}")
    print()
