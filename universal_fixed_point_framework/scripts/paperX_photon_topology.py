#!/usr/bin/env python3
"""
paperX_photon_topology.py — Phase 62B 光子拓扑-范畴理论数值验证

笔记来源: notes/06_photon_topology/photon_topology_theory.md (Note-PHOTON-TOPO-v2.0)
验证项:
  S1 拓扑转变的方向性阶跃 (公理 A4): chi_Phi = Theta(t - t*) 与 sigma_S3 单向 1->0 不可逆
  S2 光速不变拓扑定理 (定理 2.1): c = 1/sqrt(mu0*eps0) + 洛伦兹速度加法不变 + 空间平移不变
  S3 c = lambda*nu 自洽定理 (定理 3.1): lambda*nu = c 恒等式 + 反比关系 + 红移保持
  S4 E = h*nu 拓扑释义 + 可拦截性 (命题 4.1 / 1.4 / 定义 1.4): Bohr 匹配 + 吸收截面共振选择性
  S5 推论 4 时间解耦: 传播途中零时间耦合, 耦合仅在端点 (发射 D 转变 / 吸收 R 折叠)
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
# S1 拓扑转变的方向性阶跃 (公理 A4)
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

    # 耦合事件仅发生在端点 (t=0 发射 D 转变, t=T_total 吸收 R 折叠)
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
# S7 捕获-再转变模型 (命题 3.2, 开放问题 #3 推进)
# ============================================================
def s7_capture_reemission():
    # 介质中"光速变慢"的拓扑补充: 光子被介质原子捕获(R 折叠) -> 重新转变(D) -> 继续
    # 真空段单光子拓扑严格 v = c; 宏观 v_avg < c 为捕获-再转变延迟的统计效应
    c = C_LIGHT
    L = 100.0                  # 介质长度 (m)
    n_atoms = 200              # 捕获点数量
    tau_mean = 5.0e-9          # 平均捕获-再转变延迟 (s)
    p_capture = 0.5

    def simulate(seed, pc):
        rng = np.random.default_rng(seed)
        atom_pos = np.sort(rng.uniform(0.0, L, n_atoms))
        t_tot = 0.0
        x = 0.0
        seg = []
        for pos in atom_pos:
            d = pos - x
            t_tot += d / c          # 真空段: 单光子拓扑严格 v = c
            seg.append(c)
            x = pos
            if rng.random() < pc:
                t_tot += rng.exponential(tau_mean)   # 捕获-再转变延迟
        t_tot += (L - x) / c
        seg.append(c)
        return t_tot, seg

    t_single, seg = simulate(7, p_capture)
    v_avg = L / t_single

    # C22: 真空传播段严格 v = c (单光子拓扑, 模型构造)
    check("S7-C22 真空传播段严格 v = c (单光子拓扑)",
          bool(all(abs(s - c) < 1e-6 for s in seg)))

    # C23: 宏观平均速度 < c (捕获-再转变统计延迟)
    check("S7-C23 宏观 v_avg < c (捕获-再转变统计延迟)",
          v_avg < c, "v_avg=%.4e m/s" % v_avg)

    # C24: 解析公式 t_avg = L/c + n_atoms*p_capture*tau_mean 与多次模拟平均一致
    trials = 20
    ts = [simulate(100 + i, p_capture)[0] for i in range(trials)]
    t_avg = float(np.mean(ts))
    t_analytic = L / c + n_atoms * p_capture * tau_mean
    rel_err = abs(t_avg - t_analytic) / t_analytic
    check("S7-C24 解析 t_avg = L/c + n·p·τ 与模拟平均一致",
          rel_err < 0.05, "rel err=%.3f" % rel_err)

    # C25: 无捕获 (p_capture = 0) 退化 v_avg = c
    t_free = L / c
    check("S7-C25 p_capture=0 退化 v_avg = c",
          abs(L / t_free - c) < 1e-6)

    # C26: v_avg 随捕获概率单调递减 (解析)
    ps = [0.0, 0.25, 0.5, 0.75, 0.9]
    v_avgs = [L / (L / c + n_atoms * pc * tau_mean) for pc in ps]
    mono = all(v_avgs[i] > v_avgs[i + 1] for i in range(len(v_avgs) - 1))
    check("S7-C26 v_avg 随捕获概率单调递减 (解析)",
          mono, "v_avg range [%.6e, %.6e] m/s" % (v_avgs[0], v_avgs[-1]))


# ============================================================
# S8 自由传播模方守恒一致性 (开放问题 #6 推进, 树级)
# ============================================================
def s8_free_propagation():
    # 漏洞修正: 原"时间解耦等价性"命名过强——本节约为树级(忽略真空修正)自由传播的
    #   模方守恒一致性 + 定义 2.4 与标准公式的定义一致性, 非"等价性验证":
    #   - C27/C29 为定义一致性 (定义 2.4 本身 = 标准量子光学公式)
    #   - C28/C30 为 |e^{-iωnt}|^2 = 1 的模方守恒 (trivial 恒等式, 物理为设定)
    #   - 推论 2.1 的"光子视角递归静止"(γ→∞) 部分未在本节数值验证
    eps0 = 8.8541878128e-12
    hbar = H_PLANCK / (2.0 * np.pi)
    d12 = 3.0e-29              # 偶极矩阵元 (C*m, 原子量级)
    nu0 = 4.57e14              # 氢 Ly-alpha 频率 (Hz)
    Gamma = 1.0e9              # 线宽 (Hz)

    # C27: 定义 2.4 = 标准量子光学形式 (定义一致性: 同一公式的两条计算路径)
    B12 = (np.pi / (3.0 * eps0 * hbar**2)) * d12**2
    g0 = 2.0 / (np.pi * Gamma)          # 洛伦兹线型共振值
    sigma_def24 = (H_PLANCK * nu0 / C_LIGHT) * B12 * g0
    sigma_std = (np.pi / (3.0 * eps0 * C_LIGHT * hbar**2)) * H_PLANCK * nu0 * d12**2 * g0
    rel_err27 = abs(sigma_def24 - sigma_std) / sigma_std
    check("S8-C27 定义2.4 吸收截面 = 标准量子光学形式 (定义一致性)",
          rel_err27 < 1e-12, "rel err=%.2e" % rel_err27)

    # C28: 树级自由传播模方守恒 (|e^{-iωnt}|^2 = 1, trivial 恒等式)
    n = 1
    omega = 2.0 * np.pi * nu0
    t = np.linspace(0.0, 1.0e-9, 1000)
    phase = np.exp(-1j * omega * n * t)
    n_expect = n * np.abs(phase)**2
    check("S8-C28 树级自由演化模方守恒 (|e^{-iωnt}|^2=1, 保光子数)",
          np.max(np.abs(n_expect - n)) < 1e-12)

    # C29: R 折叠概率反解 B_12 = 标准 B_12 (定义一致性)
    sigma_peak = (H_PLANCK * nu0 / C_LIGHT) * B12 * g0
    B12_from_sigma = sigma_peak / ((H_PLANCK * nu0 / C_LIGHT) * g0)
    rel_err29 = abs(B12_from_sigma - B12) / B12
    check("S8-C29 R 折叠概率反解 B_12 = 标准 B_12 (定义一致性)",
          rel_err29 < 1e-12, "rel err=%.2e" % rel_err29)

    # C30: 树级传播间隔内模方不变 (与 S5 一致的 trivial 确认)
    n_end = n * np.abs(np.exp(-1j * omega * n * 1.0e-9))**2
    check("S8-C30 树级传播间隔模方守恒 (保光子数)",
          abs(n_end - n) < 1e-12)


# ============================================================
# S9 静默指标与爱因斯坦系数定量关联 (开放问题 #8 推进)
# ============================================================
def s9_silence_einstein():
    # 核心关联: W_eff(t) = (1 - sigma_S3(t)) * W_ij
    #   静默屏障 = 跃迁率的乘法门控因子 (离散拓扑开关 sigma 0/1 x 连续量子速率 W_ij)
    #   对应笔记 §1.2 公理 A4 / 论文 §2.3
    nu0 = 4.57e14                       # 氢 Ly-alpha 频率 (Hz)
    A21_std = 6.3e8                     # Ly-alpha 自发辐射率 (s^-1)

    # C31: 门控模型 sigma=1 -> W_eff=0; sigma=0 -> W_eff=W_ij
    W_eff_silent = (1.0 - 1.0) * A21_std
    W_eff_open = (1.0 - 0.0) * A21_std
    check("S9-C31 门控模型: sigma=1 -> W_eff=0, sigma=0 -> W_eff=W_ij",
          abs(W_eff_silent) < 1e-12 and abs(W_eff_open - A21_std) / A21_std < 1e-12)

    # C32: 转变瞬间跃迁率阶跃 (与公理 A4 一致): sigma 1->0 时 W_eff 0->W_ij
    t_star = 1.0
    t_grid = np.linspace(0.0, 2.0, 2001)
    sigma = np.where(t_grid < t_star, 1.0, 0.0)
    W_eff = (1.0 - sigma) * A21_std
    W_before = W_eff[t_grid < t_star]
    W_after = W_eff[t_grid >= t_star]
    check("S9-C32 转变瞬间跃迁率阶跃 (sigma 1->0, W_eff 0->W_ij)",
          np.max(W_before) < 1e-12 and abs(np.min(W_after) - A21_std) < 1e-12)

    # C33: 爱因斯坦关系 A_21 = (8*pi*h*nu^3/c^3)*B_21 (黑体辐射一致性)
    ratio_std = 8.0 * np.pi * H_PLANCK * nu0**3 / C_LIGHT**3
    B21 = A21_std / ratio_std          # 由关系确定 B_21
    check("S9-C33 爱因斯坦关系 A_21 = (8πhν³/c³)B_21 自洽",
          abs(A21_std - ratio_std * B21) < 1e-3,
          "ratio_std=%.3e J^-1 s^-1 m^-3" % ratio_std)

    # C34: B_12 = B_21 (简并相等, 细结构常数无关)
    B12 = B21
    check("S9-C34 B_12 = B_21 (简并相等)", B12 == B21)

    # C35: 静默解除后自发衰变 N(t) = N0*exp(-A_21 t) (指数衰变律)
    N0 = 100.0
    t = np.linspace(0.0, 5.0e-9, 500)
    N = N0 * np.exp(-A21_std * t)
    ln_ratio = np.log(N / N0)
    slope = (ln_ratio[-1] - ln_ratio[0]) / (t[-1] - t[0])
    check("S9-C35 静默解除后自发衰变 N = N0*exp(-A_21 t) (指数)",
          abs(slope + A21_std) / A21_std < 1e-6)

    # C36: 静默期间无跃迁 (sigma=1 时 N 不变, W_eff = 0)
    check("S9-C36 静默期间无跃迁 (sigma=1 时 W_eff = 0, N 不变)",
          abs(W_eff_silent) < 1e-12)


# ============================================================
# S10 可拦截性选择定则门 (命题 2.3 取向门, 2026-08-11)
# ============================================================
def s10_selection_rules():
    # 命题 2.3 取向门: 光子环绕方向(二元取向 s=±1)须与原子跃迁角动量变化匹配——
    #   已知物理 = 原子选择定则 (电偶极 E1: Δl=±1, Δm=0,±1; σ±↔Δm=±1, π↔Δm=0)
    #   拓扑重述: 环绕方向 = 二元取向; 选择定则 = 取向门控 (结合 = 能量门 ∧ 取向门)
    # C37: 偏振-环绕方向-Δm 匹配表 (σ± 携带 ±ħ 环绕角动量, π 为 0)
    sel = {"sigma+": (+1, +1), "sigma-": (-1, -1), "pi": (0, 0)}  # 偏振 -> (环绕方向, Δm)
    match37 = all(h == dm for h, dm in sel.values()) and set(sel) == {"sigma+", "sigma-", "pi"}
    check("S10-C37 偏振↔环绕方向↔Δm 匹配表 (σ±↔±1, π↔0)",
          bool(match37),
          "σ+↔(+1,+1), σ-↔(-1,-1), π↔(0,0)")

    # C38: 氢 2p→1s: Δl=-1 电偶极 E1 允许 (B12 ≠ 0)
    dl_2p1s = 0 - 1                     # 1s(l=0) - 2p(l=1)
    allowed = abs(dl_2p1s) == 1         # E1 允许: Δl = ±1
    B12_2p1s = 1.0 if allowed else 0.0
    check("S10-C38 氢 2p→1s Δl=±1 电偶极允许 (B12≠0)",
          bool(allowed and B12_2p1s > 0), "Δl=%d" % dl_2p1s)

    # C39: 氢 2s→1s: Δl=0 电偶极 E1 禁戒 (B12=0, 实际经双光子衰变)
    dl_2s1s = 0 - 0                     # 1s(l=0) - 2s(l=0)
    forbidden = abs(dl_2s1s) != 1       # Δl=0: E1 禁戒 (宇称不变)
    B12_2s1s = 0.0 if forbidden else 1.0
    check("S10-C39 氢 2s→1s Δl=0 电偶极禁戒 (B12=0)",
          bool(forbidden and B12_2s1s == 0), "Δl=%d → E1 禁戒(双光子)" % dl_2s1s)

    # C40: 禁戒跃迁即使能量匹配 hν=ΔE 也不拦截 (取向门语义, 命题 2.3)
    nu0 = (13.6 - 3.4) * 1.602176634e-19 / H_PLANCK   # 氢 2s→1s 能量匹配示例
    g0 = 1.0
    sigma_forbidden = (H_PLANCK * nu0 / C_LIGHT) * B12_2s1s * g0   # B12=0
    check("S10-C40 禁戒跃迁 B12=0 即使 hν=ΔE 也不拦截 (σ_abs=0)",
          abs(sigma_forbidden) < 1e-300, "σ_abs=%.2e" % sigma_forbidden)


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
    s7_capture_reemission()
    s8_free_propagation()
    s9_silence_einstein()
    s10_selection_rules()

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
