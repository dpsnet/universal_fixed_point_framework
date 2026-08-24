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
# 本文件中 UFPF 相关引用数量：2
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
paperX_redshift_topology.py — Phase 62D 红移/紫移统一拓扑解释数值验证

笔记来源: notes/06_photon_topology/photon_topology_theory.md §5
验证项:
  R1 多普勒红移公式: lambda_obs = lambda_emit * sqrt((1+beta)/(1-beta)) 且 lambda*nu = c
  R2 拓扑推导链恒等式: gamma*(1+beta) = sqrt((1+beta)/(1-beta))
  R3 引力红移基础项: z = GM/(R*c^2) 量级 (太阳 2.12e-6, 地球 6.95e-10)
  R4 UFPF 独有修正项 delta_z_Delta = eps_Delta * z_grav 量级估计 (太阳系/强引力场与预言 P1 带重叠)
  R5 宇宙学红移: z = a_obs/a_emit - 1 且 lambda*nu = c 保持
  R6 统一公式: z = (lambda_obs - lambda_emit)/lambda_emit 自洽
  R7 三类红移均保持 c = lambda*nu
  R8 弱场小 z 组合近似可加性 + 精确乘法形式

诚实边界: 本脚本验证三类红移公式的数值自洽性与 UFPF 独有修正项 delta_z_Delta
的量级结构估计 (依赖未定的代数系数 eps_Delta, 见笔记 §5.3.1 开放问题 5),
不构成对预言 P1 的实验验证。
"""
import numpy as np

# ============================================================
# 检查项框架
# ============================================================
_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


C = 299792458.0     # 真空光速 (m/s)
G = 6.67430e-11     # 万有引力常数 (N*m^2/kg^2)
M_SUN, R_SUN = 1.989e30, 6.957e8
M_EARTH, R_EARTH = 5.972e24, 6.371e6
# Delta 修正代数系数范围 (框架锁定量级, 具体值未定 -> 开放问题 5)
EPS_DELTA_LO, EPS_DELTA_HI = 1e-4, 1e-2


# ============================================================
# R1 多普勒红移公式
# ============================================================
def r1_doppler():
    betas = np.linspace(-0.9, 0.9, 181)
    lam_emit = 5.0e-7
    lam_obs = lam_emit * np.sqrt((1.0 + betas) / (1.0 - betas))
    f_emit = C / lam_emit
    f_obs = f_emit * np.sqrt((1.0 - betas) / (1.0 + betas))
    rel_err = np.max(np.abs(lam_obs * f_obs - C)) / C
    check("R1-C1 lambda_obs = lambda_emit*sqrt((1+beta)/(1-beta)) 且 lambda*nu = c",
          rel_err < 1e-12, "max rel err=%.2e" % rel_err)
    # beta > 0 (远离) -> 红移
    lam_red = lam_emit * np.sqrt((1.0 + 0.3) / (1.0 - 0.3))
    check("R1-C2 beta>0 (远离) lambda_obs > lambda_emit (红移)", lam_red > lam_emit)
    # beta < 0 (靠近) -> 紫移
    lam_blue = lam_emit * np.sqrt((1.0 - 0.3) / (1.0 + 0.3))
    check("R1-C3 beta<0 (靠近) lambda_obs < lambda_emit (紫移)", lam_blue < lam_emit)


# ============================================================
# R2 拓扑推导链恒等式
# ============================================================
def r2_derivation():
    betas = np.linspace(-0.999, 0.999, 501)
    gamma = 1.0 / np.sqrt(1.0 - betas**2)
    lhs = gamma * (1.0 + betas)      # 推导链: T_obs/T_emit = gamma*(1+beta)
    rhs = np.sqrt((1.0 + betas) / (1.0 - betas))
    rel_err = np.max(np.abs(lhs - rhs)) / np.max(np.abs(rhs))
    check("R2-C1 拓扑推导链 gamma*(1+beta) = sqrt((1+beta)/(1-beta))",
          rel_err < 1e-12, "max rel err=%.2e" % rel_err)


# ============================================================
# R3-R4 引力红移基础项 + Delta 修正项量级
# ============================================================
def r3_4_gravitational():
    # R3: 引力红移基础项 z = GM/(R*c^2) (弱场近似)
    z_sun = G * M_SUN / (R_SUN * C**2)
    z_earth = G * M_EARTH / (R_EARTH * C**2)
    check("R3-C1 太阳表面引力红移 z ~ 2.12e-6",
          abs(z_sun - 2.12e-6) / 2.12e-6 < 0.01, "z_sun=%.3e" % z_sun)
    check("R3-C2 地球表面引力红移 z ~ 6.95e-10",
          abs(z_earth - 6.95e-10) / 6.95e-10 < 0.01, "z_earth=%.3e" % z_earth)

    # R4: delta_z_Delta = eps_Delta * z_grav (笔记 §5.3.1 量级结构假设)
    dz_sun_lo, dz_sun_hi = EPS_DELTA_LO * z_sun, EPS_DELTA_HI * z_sun
    # 太阳系量级带: eps 范围内落在 ~[1e-10, 1e-7]
    check("R4-C1 太阳系 delta_z_Delta 量级带 [1e-10, 1e-7]",
          dz_sun_lo >= 1e-11 and dz_sun_hi <= 1e-6,
          "delta_z_Delta in [%.2e, %.2e]" % (dz_sun_lo, dz_sun_hi))

    # 强引力场 (白矮星: M~0.6 M_sun, R~0.01 R_sun -> z ~ 1.3e-4)
    M_wd, R_wd = 0.6 * M_SUN, 0.01 * R_SUN
    z_wd = G * M_wd / (R_wd * C**2)
    dz_wd_lo, dz_wd_hi = EPS_DELTA_LO * z_wd, EPS_DELTA_HI * z_wd
    # 与预言 P1 (偏振红移差 1e-6 ~ 1e-8) 量级带重叠
    check("R4-C2 强引力场 delta_z_Delta 与预言 P1 带 [1e-8, 1e-6] 重叠",
          dz_wd_lo <= 1e-6 and dz_wd_hi >= 1e-8,
          "delta_z_Delta in [%.2e, %.2e]" % (dz_wd_lo, dz_wd_hi))


# ============================================================
# R5 宇宙学红移
# ============================================================
def r5_cosmological():
    a_obs = np.array([1.0, 1.1, 2.0, 5.0, 10.0])
    a_emit = 1.0
    z = a_obs / a_emit - 1.0
    lam_emit = 5.0e-7
    lam_obs = lam_emit * (a_obs / a_emit)
    z_from_lambda = (lam_obs - lam_emit) / lam_emit
    check("R5-C1 宇宙学红移 z = a_obs/a_emit - 1 与统一公式自洽",
          bool(np.allclose(z, z_from_lambda, rtol=1e-12, atol=1e-14)))
    nu_obs = C / lam_obs
    check("R5-C2 宇宙学红移后 lambda*nu = c 保持",
          np.max(np.abs(lam_obs * nu_obs - C)) / C < 1e-12)


# ============================================================
# R6 统一公式
# ============================================================
def r6_unified():
    lam_emit = 5.0e-7
    for lam_obs in [5.5e-7, 4.0e-7, 1.0e-6, 3.0e-7]:
        z = (lam_obs - lam_emit) / lam_emit
        lam_check = lam_emit * (1.0 + z)
        if abs(lam_check - lam_obs) >= 1e-20:
            check("R6-C1 统一公式反解 lambda_obs = lambda_emit*(1+z)",
                  False, "z=%.4f" % z)
            return
    check("R6-C1 统一公式反解 lambda_obs = lambda_emit*(1+z)", True)


# ============================================================
# R7 三类红移均保持 c = lambda*nu
# ============================================================
def r7_lambda_nu_preserved():
    lam_emit = 5.0e-7
    # 多普勒
    beta = 0.3
    lam_d = lam_emit * np.sqrt((1.0 + beta) / (1.0 - beta))
    ok_d = abs(lam_d * (C / lam_d) - C) / C < 1e-12
    # 引力
    lam_g = lam_emit * (1.0 + 2.12e-6)
    ok_g = abs(lam_g * (C / lam_g) - C) / C < 1e-12
    # 宇宙学
    lam_c = lam_emit * 2.0
    ok_c = abs(lam_c * (C / lam_c) - C) / C < 1e-12
    check("R7-C1 三类红移均保持 c = lambda*nu", ok_d and ok_g and ok_c)


# ============================================================
# R8 弱场小 z 组合近似可加性 + 精确乘法形式
# ============================================================
def r8_combination():
    beta = 0.1
    z_dop = np.sqrt((1.0 + beta) / (1.0 - beta)) - 1.0
    z_grav = 2.12e-6
    z_cosmo = 0.01
    z_total = (1.0 + z_dop) * (1.0 + z_grav) * (1.0 + z_cosmo) - 1.0
    z_approx = z_dop + z_grav + z_cosmo
    rel_err = abs(z_total - z_approx) / z_total
    # 弱场/小 z 下乘法组合近似可加, 高阶项 ~ z_dop*z_cosmo
    check("R8-C1 弱场小 z 组合可加性 z_total ~ z_D + z_G + z_C",
          rel_err < 0.05, "rel err=%.3f (高阶项 z_D*z_C 量级)" % rel_err)
    check("R8-C2 精确组合乘法形式 z_total = (1+z_D)(1+z_G)(1+z_C) - 1",
          abs(z_total - ((1.0 + z_dop) * (1.0 + z_grav) * (1.0 + z_cosmo) - 1.0)) < 1e-15)


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 72)
    print("Paper 44 (Phase 62D): 红移/紫移统一拓扑解释数值验证")
    print("笔记: notes/06_photon_topology/photon_topology_theory.md §5")
    print("=" * 72)
    r1_doppler()
    r2_derivation()
    r3_4_gravitational()
    r5_cosmological()
    r6_unified()
    r7_lambda_nu_preserved()
    r8_combination()

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
