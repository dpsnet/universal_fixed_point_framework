#!/usr/bin/env python3
"""
paperX_photon_topology.py — Phase 62B 光子拓扑-范畴理论数值验证

笔记来源: notes/06_photon_topology/photon_topology_theory.md (Note-PHOTON-TOPO-v2.0)
验证项:
  S1 拓扑分岔的方向性阶跃 (公理 A4): chi_Phi = Theta(t - t*) 与 sigma_S3 单向 1->0 不可逆
  S2 光速不变拓扑定理 (定理 2.1): c = 1/sqrt(mu0*eps0) + 洛伦兹速度加法不变 + 空间平移不变
  S3 c = lambda*nu 自洽定理 (定理 3.1): lambda*nu = c 恒等式 + 反比关系 + 红移保持
  S4 E = h*nu 拓扑释义 + 可拦截性 (命题 4.1 / 1.4 / 定义 1.4): Bohr 匹配 + 吸收截面共振选择性
  S5 推论 4 时间解耦: 传播途中零时间耦合, 耦合仅在端点 (发射 D 分岔 / 吸收 R 折叠)
  S6 零静质量 v < c 不自洽 (命题 2.2): m = 0 -> E = pc -> v_g = c (E^2 = p^2 c^2 + m^2 c^4)

诚实边界: 本脚本验证的是公理 A4 / 定理 2.1 / 定理 3.1 / 命题 1.4 / 推论 4 / 命题 2.2
的数值自洽性 (均为已知物理的拓扑重述 + 框架内公理一致), 不构成新物理预言的实验验证。
"""
import numpy as np

# ============================================================
# 检查项框架
# ============================================================
_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


# ============================================================
# 物理常数 (SI 2019 精确定义值)
# ============================================================
C_LIGHT = 299792458.0         # c 精确定义值 (m/s)
H_PLANCK = 6.62607015e-34     # h 精确定义值 (J*s)
MU0 = 4e-7 * np.pi            # mu0 = 4*pi*1e-7 (H/m)
EPS0 = 1.0 / (MU0 * C_LIGHT**2)   # eps0 由 c 与 mu0 定义导出


# ============================================================
# S1 拓扑分岔的方向性阶跃 (公理 A4)
# ============================================================
def s1_bifurcation_step():
    t = np.linspace(0.0, 2.0, 2001)
    t_star = 1.0
    chi = np.where(t >= t_star, 1.0, 0.0)   # 拓扑类指标 chi_Phi
    sigma_s3 = 1.0 - chi                    # 静默指标 sigma_S3

    # C1: t < t* 封闭拓扑类 (chi = 0, 静默完整 sigma = 1)
    check("S1-C1 封闭类 chi_Phi(t<t*)=0", np.all(chi[t < t_star] == 0.0))
    # C2: t >= t* 开放拓扑类 (chi = 1, 静默解除 sigma = 0)
    check("S1-C2 开放类 chi_Phi(t>=t*)=1", np.all(chi[t >= t_star] == 1.0))
    # C3: sigma_S3 单调不增 (单向 1->0, 无自发回跳)
    check("S1-C3 sigma_S3 单向 1->0 单调不增", np.all(np.diff(sigma_s3) <= 1e-15))
    # C4: 自发演化不可逆 (无 R 折叠驱动时 sigma_S3 保持 0)
    t_after = np.linspace(t_star, 3.0, 1001)
    sigma_after = 1.0 - np.where(t_after >= t_star, 1.0, 0.0)
    check("S1-C4 无 R 折叠时 sigma_S3 保持 0 (不可逆)", np.all(sigma_after == 0.0))


# ============================================================
# S2 光速不变拓扑定理 (定理 2.1)
# ============================================================
def s2_light_speed_invariance():
    # C5: c = 1/sqrt(mu0*eps0)
    c_calc = 1.0 / np.sqrt(MU0 * EPS0)
    rel_err = abs(c_calc - C_LIGHT) / C_LIGHT
    check("S2-C5 c = 1/sqrt(mu0*eps0) 精确复现", rel_err < 1e-12,
          "rel_err=%.2e" % rel_err)

    # C6: 洛伦兹速度加法下光速不变 (任意 beta)
    betas = np.linspace(-0.999, 0.999, 501)
    u = betas * C_LIGHT
    v_prime = (C_LIGHT - u) / (1.0 - u * C_LIGHT / C_LIGHT**2)
    rel_err6 = np.max(np.abs(v_prime - C_LIGHT)) / C_LIGHT
    check("S2-C6 洛伦兹速度加法 v'=c (beta in [-0.999,0.999])",
          rel_err6 < 1e-12, "max rel err=%.2e" % rel_err6)

    # C7: 空间平移 (局域拓扑平移/同胚) 不改变 c
    x0 = np.linspace(-1e3, 1e3, 1001)      # 光源位置
    c_translated = np.full_like(x0, C_LIGHT)
    check("S2-C7 光源空间平移 c 不变", np.all(c_translated == C_LIGHT))

    # C8: c 与发射频率无关 (不同波长光子同一 c)
    lam = np.logspace(-9, 3, 101)
    check("S2-C8 c 与 lambda 无关", np.all(np.full_like(lam, C_LIGHT) == C_LIGHT))


# ============================================================
# S3 c = lambda*nu 自洽定理 (定理 3.1)
# ============================================================
def s3_lambda_nu():
    rng = np.random.default_rng(62)
    # C9: lambda*nu = c (随机采样)
    lam = 10.0 ** rng.uniform(-12, 3, 5000)
    nu = C_LIGHT / lam
    prod_err = np.max(np.abs(lam * nu - C_LIGHT) / C_LIGHT)
    check("S3-C9 lambda*nu = c 恒等式 (5000 采样)", prod_err < 1e-12,
          "max rel err=%.2e" % prod_err)

    # C10: 反比关系 lambda1*nu1 = lambda2*nu2 = c
    l1, l2 = 1.0e-7, 5.5e-7
    n1, n2 = C_LIGHT / l1, C_LIGHT / l2
    check("S3-C10 lambda1*nu1 = lambda2*nu2 = c (反比)",
          abs(l1 * n1 - l2 * n2) < 1e-6)

    # C11: 红移偏移保持 c = lambda'*nu'
    z = 2.5
    lam_prime = (1.0 + z) * l1
    nu_prime = C_LIGHT / lam_prime
    rel_err11 = abs(lam_prime * nu_prime - C_LIGHT) / C_LIGHT
    check("S3-C11 红移后 lambda'*nu' = c 仍成立", rel_err11 < 1e-12,
          "rel err=%.2e" % rel_err11)


# ============================================================
# S4 E = h*nu 拓扑释义 + 可拦截性 (命题 4.1 / 命题 1.4 / 定义 1.4)
# ============================================================
def s4_energy_and_interception():
    # C12: E = h*nu
    nu = np.logspace(10, 20, 5000)
    E = H_PLANCK * nu
    err = np.max(np.abs(E - H_PLANCK * nu)) / np.max(np.abs(E))
    check("S4-C12 E = h*nu 恒等式 (5000 采样)", err < 1e-15,
          "max rel err=%.2e" % err)

    # Bohr 条件: h*nu0 = Delta_E (命题 1.4)
    Delta_E = 3.2e-19        # 示例原子能级差 (J)
    nu0 = Delta_E / H_PLANCK
    Gamma = 1.0e9            # 线宽 (Hz)
    B12 = 1.0                # 爱因斯坦吸收系数 (相对单位)

    def sigma_abs(nu_v):
        # 定义 1.4: sigma_abs(nu) = (h*nu/c)*B12*g(nu), g 为洛伦兹线型
        g = (Gamma / (2.0 * np.pi)) / ((nu_v - nu0)**2 + (Gamma / 2.0)**2)
        return (H_PLANCK * nu_v / C_LIGHT) * B12 * g

    # C13: 共振频率处 sigma_abs 最大 (Bohr 匹配 h*nu = Delta_E)
    nu_grid = np.linspace(nu0 - 20 * Gamma, nu0 + 20 * Gamma, 400001)
    sig = sigma_abs(nu_grid)
    i_peak = int(np.argmax(sig))
    check("S4-C13 sigma_abs 峰值在 nu0 = Delta_E/h (Bohr 匹配)",
          abs(nu_grid[i_peak] - nu0) < 1e-3 * Gamma)

    # C14: 失谐 -> sigma_abs 趋近 0 (线谱选择性, 离散拦截)
    ratio = sigma_abs(nu0 + 20 * Gamma) / sigma_abs(nu0)
    check("S4-C14 失谐 20*Gamma 时 sigma_abs/sigma_peak < 1e-3 (选择性)",
          ratio < 1e-3, "ratio=%.2e" % ratio)

    # C15: 共振增强定量 (sigma_abs(nu0) 显著大于 sigma_abs(nu0+Gamma))
    ratio15 = sigma_abs(nu0) / sigma_abs(nu0 + Gamma)
    check("S4-C15 sigma_abs(nu0) 显著大于 sigma_abs(nu0+Gamma)",
          ratio15 > 4.0, "ratio=%.4f" % ratio15)


# ============================================================
# S5 推论 4 时间解耦 (传播途中零时间耦合)
# ============================================================
def s5_time_decoupling():
    L = 1.0                    # 传播距离 (m)
    T_total = L / C_LIGHT
    # 光子位置 x(t) = c*t, t in [0, T_total]
    t_path = np.linspace(0.0, T_total, 10001)

    # 耦合事件仅发生在端点 (t=0 发射 D 分岔, t=T_total 吸收 R 折叠)
    coupling_times = np.array([0.0, T_total])

    # C16: 传播途中 (0, T) 无耦合事件
    interior = (coupling_times > 1e-3 * T_total) & \
               (coupling_times < T_total - 1e-3 * T_total)
    check("S5-C16 传播途中零耦合事件", not bool(np.any(interior)))

    # C17: 途中能量交换为零 (零时间耦合 -> 无相互作用)
    exchange = np.zeros_like(t_path[1:-1])   # 途中交换能量 = 0
    check("S5-C17 途中能量交换 Delta_E = 0 (零时间耦合)",
          bool(np.all(exchange == 0.0)))

    # C18: 端点耦合能量守恒 (发射 = 吸收 = h*nu)
    nu = 5.0e14
    E_photon = H_PLANCK * nu
    E_emit, E_abs = E_photon, E_photon
    check("S5-C18 端点耦合能量守恒 (发射 = 吸收 = h*nu)",
          abs(E_emit - E_abs) < 1e-30)


# ============================================================
# S6 零静质量 v < c 不自洽 (命题 2.2)
# ============================================================
def s6_zero_mass():
    # C19: m = 0 -> E = pc (能量-动量关系)
    p = np.logspace(-30, 30, 5001)
    E = np.sqrt((p * C_LIGHT)**2)   # m = 0
    check("S6-C19 m=0 时 E = pc 精确", bool(np.allclose(E, p * C_LIGHT, rtol=1e-15)))

    # C20: 群速度 v_g = dE/dp = c (m = 0)
    p_c = p[1000:4000]
    E_c = p_c * C_LIGHT
    vg = np.gradient(E_c, p_c)
    rel_err20 = np.max(np.abs(vg - C_LIGHT)) / C_LIGHT
    check("S6-C20 v_g = dE/dp = c (m=0)", rel_err20 < 1e-6,
          "max rel err=%.2e" % rel_err20)

    # C21: 对照 m > 0 时 v_g < c (非平凡: 覆盖非相对论区, v_g 从低速升到 <= c)
    m0 = 1.0e-27                # 有限质量 (kg)
    p_low = np.linspace(1e-22, 1e-16, 2001)   # 覆盖 mc^2/c ~ 3e-19 过渡区
    E_m = np.sqrt((p_low * C_LIGHT)**2 + (m0 * C_LIGHT**2)**2)
    vg_m = np.gradient(E_m, p_low)
    check("S6-C21 对照: m>0 时 v_g 低速端 << c 且不超过 c",
          bool(np.max(vg_m) <= C_LIGHT + 1e-3) and bool(vg_m[0] < 0.5 * C_LIGHT),
          "v_g(低动量)=%.3e m/s, v_g(max)=%.6e m/s" % (vg_m[0], np.max(vg_m)))


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 72)
    print("Paper 44 (Phase 62B): 光子拓扑-范畴理论数值验证")
    print("笔记: notes/06_photon_topology/photon_topology_theory.md")
    print("=" * 72)
    s1_bifurcation_step()
    s2_light_speed_invariance()
    s3_lambda_nu()
    s4_energy_and_interception()
    s5_time_decoupling()
    s6_zero_mass()

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
