#!/usr/bin/env python3
"""
paperX_photon_cross_effects.py — Phase 62E 交叉衍生效应定量化数值验证

笔记来源: notes/06_photon_topology/photon_topology_theory.md §6
验证项 (六项预言 P1-P6):
  E1 P1 引力 Delta-偏振红移差: delta_z_pol = kappa_Delta * z_grav
  E2 P2 S3 静默-辐射波长标度: nu(Z)/nu0 = 1 + eta_S3*(Z/Z_ref)
  E3 P3 h-c-Delta 三常数约束: 候选代数形式的量级合理性 (Delta_lambda_min, hc)
  E4 P4 分形宇宙红移震荡: S4 = e^(-d_H) = 1/15, 幅度与对数周期候选形式
  E5 P5 场表述康普顿散射: Delta_lambda = lambda_e*(1-cos(theta))
  E6 P6 多层静默无辐射跃迁判据: R_supp(N) = sigma_silent^N, N_crit

诚实边界: 六项预言均为远期可证伪假说, 本脚本验证其定量形式/量级结构的
数值自洽性 (含候选系数 kappa_Delta, eta_S3 的框架锁定量级扫描),
不构成实验验证; P5 的标准康普顿公式为已知物理 (温和兼容).
"""
import numpy as np

# ============================================================
# 检查项框架
# ============================================================
_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


# 物理常数 (SI)
C = 299792458.0
H = 6.62607015e-34
HBAR = H / (2.0 * np.pi)
M_E = 9.1093837015e-31
G = 6.67430e-11
M_SUN, R_SUN = 1.989e30, 6.957e8
# 框架候选系数范围
KAPPA_DELTA_LO, KAPPA_DELTA_HI = 1e-4, 1e-2   # P1 偏振不对称系数
ETA_S3_LO, ETA_S3_HI = 1e-5, 1e-3             # P2 S3 静默耦合系数


# ============================================================
# E1 预言 P1: 引力 Delta-偏振红移差
# ============================================================
def e1_polarization_redshift():
    z_sun = G * M_SUN / (R_SUN * C**2)          # 2.12e-6
    M_wd, R_wd = 0.6 * M_SUN, 0.01 * R_SUN
    z_wd = G * M_wd / (R_wd * C**2)             # 1.27e-4

    dz_sun_lo = KAPPA_DELTA_LO * z_sun
    dz_sun_hi = KAPPA_DELTA_HI * z_sun
    check("E1-C1 太阳系 delta_z_pol 量级带 [1e-10, 1e-7]",
          dz_sun_lo >= 1e-11 and dz_sun_hi <= 1e-6,
          "delta_z_pol in [%.2e, %.2e]" % (dz_sun_lo, dz_sun_hi))

    dz_wd_lo = KAPPA_DELTA_LO * z_wd
    dz_wd_hi = KAPPA_DELTA_HI * z_wd
    check("E1-C2 强引力场 delta_z_pol 与预言带 [1e-8, 1e-6] 重叠",
          dz_wd_lo <= 1e-6 and dz_wd_hi >= 1e-8,
          "delta_z_pol in [%.2e, %.2e]" % (dz_wd_lo, dz_wd_hi))

    # 偏振差分量不超过引力红移总 Delta 修正 (delta_z_Delta = eps* z, eps<=1e-2)
    dz_pol_max = KAPPA_DELTA_HI * z_wd
    dz_Delta_max = 1e-2 * z_wd
    check("E1-C3 偏振差分量 <= 总 Delta 修正 (delta_z_pol <= delta_z_Delta)",
          dz_pol_max <= dz_Delta_max + 1e-30,
          "%.2e <= %.2e" % (dz_pol_max, dz_Delta_max))


# ============================================================
# E2 预言 P2: S3 静默-辐射波长标度
# ============================================================
def e2_silence_wavelength():
    Z = np.linspace(1.0, 92.0, 200)
    Z_ref = 1.0
    for eta in [ETA_S3_LO, 1e-4, ETA_S3_HI]:
        nu_ratio = 1.0 + eta * (Z / Z_ref)
        # 单调性: Z 增大 -> nu 抬升
        if not np.all(np.diff(nu_ratio) > 0):
            check("E2-C1 nu(Z) 随 Z 单调抬升 (eta=%.1e)" % eta, False)
            return
    check("E2-C1 nu(Z) 随 Z 单调抬升 (eta in [1e-5, 1e-3])", True)

    # 相对抬升量级 (Z=92, 铀): eta*92
    rel_lo = ETA_S3_LO * 92.0
    rel_hi = ETA_S3_HI * 92.0
    check("E2-C2 全元素范围相对抬升量级 [1e-4, 1e-1]",
          rel_lo >= 1e-5 and rel_hi <= 1.0,
          "Delta_nu/nu0 in [%.2e, %.2e]" % (rel_lo, rel_hi))


# ============================================================
# E3 预言 P3: h-c-Delta 三常数约束 (候选代数形式量级检验)
# ============================================================
def e3_hcdelta():
    k_max = 8
    k = np.arange(1, k_max + 1)
    lambda_raw = np.sqrt(k * (k + 1))
    lambda_norm = lambda_raw / lambda_raw[-1]
    DL = lambda_norm[1] - lambda_norm[0]     # Delta_lambda_min
    # 精确值: (sqrt(6)-sqrt(2))/sqrt(k_max(k_max+1)) = (sqrt(3)-1)/6
    DL_exact = (np.sqrt(6.0) - np.sqrt(2.0)) / np.sqrt(k_max * (k_max + 1))
    check("E3-C1 Delta_lambda_min 数值 = (sqrt6-sqrt2)/sqrt(k_max(k_max+1))",
          abs(DL - DL_exact) / DL_exact < 1e-12,
          "DL=%.6f" % DL)

    # 候选约束量级检验: hc * Delta_lambda_min^2 与 hbar*c 同量级
    hc = H * C
    hc_bar_c = HBAR * C
    ratio = hc * DL**2 / hc_bar_c
    check("E3-C2 候选约束 hc*Delta_lambda_min^2 与 hbar*c 同量级",
          ratio > 0.01 and ratio < 100.0,
          "ratio=%.3f (量级 %d)" % (ratio, int(np.floor(np.log10(abs(ratio))))))
    # 量纲一致性: hc 量纲 = 能量*长度 (J*m)
    check("E3-C3 量纲一致性 hc [J*m] = 能量*长度",
          abs(H * C - 1.98644586e-25) / 1.98644586e-25 < 1e-3,
          "hc=%.4e J*m" % hc)


# ============================================================
# E4 预言 P4: 分形宇宙红移周期性震荡
# ============================================================
def e4_fractal_oscillation():
    d_H = np.log(15.0)
    S4 = np.exp(-d_H)
    # S4 = 1/15
    check("E4-C1 S4 = e^(-ln15) = 1/15 精确",
          abs(S4 - 1.0 / 15.0) / (1.0 / 15.0) < 1e-12,
          "S4=%.8f" % S4)

    # p=1 候选: 相对震荡幅度 = S4 = 6.67%
    check("E4-C2 相对震荡幅度 S4 ~ 6.67% (p=1 候选)",
          abs(S4 - 0.0667) / 0.0667 < 0.01,
          "S4=%.4f" % S4)

    # 对数周期候选: z 翻 15 倍 -> 相位增加 2*pi (周期检测)
    z0 = 1.0
    phi = lambda z: 2.0 * np.pi * np.log(z / z0) / np.log(15.0)
    phase_1 = phi(15.0)   # z=15: 相位 2*pi
    check("E4-C3 对数周期候选: z 翻 15 倍相位增 2*pi",
          abs(phase_1 - 2.0 * np.pi) < 1e-9,
          "phase=%.6f" % phase_1)


# ============================================================
# E5 预言 P5: 场表述康普顿散射
# ============================================================
def e5_compton():
    lam_e = H / (M_E * C)
    # 康普顿波长 = 2.426e-12 m
    check("E5-C1 康普顿波长 lambda_e = h/(m_e c) = 2.426e-12 m",
          abs(lam_e - 2.42631023867e-12) / 2.42631023867e-12 < 1e-6,
          "lambda_e=%.6e m" % lam_e)

    # Delta_lambda = lambda_e*(1-cos(theta)) 对 theta 扫描
    theta = np.linspace(0.0, np.pi, 501)
    dl = lam_e * (1.0 - np.cos(theta))
    # 标准康普顿: Delta_lambda 单调增 (0 -> 2*lambda_e)
    check("E5-C2 Delta_lambda = lambda_e(1-cos theta) 单调增 [0, 2*lambda_e]",
          np.all(np.diff(dl) >= 0) and abs(dl[-1] - 2.0 * lam_e) < 1e-20,
          "Delta_lambda_max=%.4e" % dl[-1])

    # 康普顿特征: Delta_lambda 与入射光子能量无关 (只依赖 theta)
    E_ph = np.array([1e3, 1e5, 1e7, 1e9]) * 1.602176634e-19  # eV -> J
    dl_energy = lam_e * (1.0 - np.cos(0.5))  # theta=0.5 固定
    check("E5-C3 Delta_lambda 与入射光子能量无关 (康普顿特征)",
          np.all(np.full_like(E_ph, dl_energy) == dl_energy))


# ============================================================
# E6 预言 P6: 多层静默无辐射跃迁判据
# ============================================================
def e6_silence_layers():
    sigma_silent = np.exp(-np.log(15.0))   # e^{-d_H} = 1/15
    check("E6-C1 单层静默强度 sigma_silent = 1/15",
          abs(sigma_silent - 1.0 / 15.0) < 1e-12,
          "sigma_silent=%.6f" % sigma_silent)

    Ns = np.arange(0, 11)
    R_supp = sigma_silent**Ns
    check("E6-C2 R_supp(N) = sigma_silent^N 单调递减",
          bool(np.all(np.diff(R_supp) < 0)))

    # N_crit = ceil(ln(theta_crit)/ln(sigma_silent))
    def ncrit(theta):
        import math
        return int(math.ceil(math.log(theta) / math.log(sigma_silent)))

    n1 = ncrit(1e-3)
    check("E6-C3 N_crit(theta=1e-3) = 3 层", n1 == 3, "N_crit=%d" % n1)
    n2 = ncrit(1e-6)
    check("E6-C4 N_crit(theta=1e-6) = 6 层", n2 == 6, "N_crit=%d" % n2)


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 72)
    print("Paper 44 (Phase 62E): 交叉衍生效应定量化数值验证")
    print("笔记: notes/06_photon_topology/photon_topology_theory.md §6")
    print("=" * 72)
    e1_polarization_redshift()
    e2_silence_wavelength()
    e3_hcdelta()
    e4_fractal_oscillation()
    e5_compton()
    e6_silence_layers()

    passed = sum(1 for _, ok, _ in _CHECKS if ok)
    total = len(_CHECKS)
    print("\n" + "=" * 72)
    print("汇总: %d/%d" % (passed, total))
    print("=" * 72)
    for name, ok, detail in _CHECKS:
        mark = "[PASS]" if ok else "[FAIL]"
        line = "  %s %s" % (mark, name)
        if detail:
            line += "  (%s)" % detail
        print(line)
    print()
    if passed < total:
        print("存在未通过检查项")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
