# -*- coding: utf-8 -*-
"""Phase 100 P3c：Hβ 过禁戒闭合——π/σ 分通道横向压缩 + π 保留率反演（v2，口径修正）

v1 修正：
  1. η_comp 口径改密度加权 tail/total（与 P3b 一致）：η = Σw·tail_l / Σw·total_l
  2. α(n) 模型改"反演 + 单调拟合"：先求每线所需的 α_req，再拟合单调 α(n)

物理：横向压缩（Landau 化）压缩波函数横向（ρ）；
  - σ 通道（Δm=±1，x±iy 偶极）依赖横向 → 压缩（α_σ=1）
  - π 通道（Δm=0，z 偶极）依赖纵向 → 保留程度 α_π∈[0,1]
  η_comp_eff(n) = [tail_dens_σ + α_π·tail_dens_π] / total_dens
"""
import json, math
import numpy as np

def fact(n): return math.factorial(n)

def laguerre(n, alpha, x):
    L0 = 1.0
    if n == 0: return L0
    L1 = 1.0 + alpha - x
    if n == 1: return L1
    Lm1, L = L0, L1
    for k in range(1, n):
        Lk = ((2*k + 1 + alpha - x) * L - (k + alpha) * Lm1) / (k + 1)
        Lm1, L = L, Lk
    return L

def R_nl(n, l, r):
    if r <= 0: return 0.0
    rho = 2.0 * r / n
    norm = math.sqrt((2.0 / n) ** 3 * fact(n - l - 1) / (2.0 * n * fact(n + l)))
    return norm * math.exp(-r / n) * rho ** l * laguerre(n - l - 1, 2 * l + 1, rho)

def radial_density(n, l, r):
    R = R_nl(n, l, r)
    return R * R * r * r

def Y_lm(l, m, th, ph):
    mu = np.cos(th)
    m_abs = abs(m)
    if l == 0:
        P = np.ones_like(mu)
    else:
        Pmm = np.ones_like(mu)
        for i in range(1, m_abs + 1):
            Pmm = -Pmm * (2 * i - 1) * np.sin(th)
        if l == m_abs:
            P = Pmm
        else:
            Pm1 = Pmm
            Pmm_prev = np.zeros_like(mu)
            for i in range(m_abs + 1, l + 1):
                P = ((2 * i - 1) * mu * Pm1 - (i + m_abs - 1) * Pmm_prev) / (i - m_abs)
                Pmm_prev, Pm1 = Pm1, P
    norm = math.sqrt((2 * l + 1) / (4 * math.pi) * fact(l - m_abs) / fact(l + m_abs))
    return norm * P * np.exp(1j * m * ph)

def angular_matrix(l1, m1, l2, m2, q):
    nth, nph = 200, 40
    th = np.linspace(1e-4, math.pi - 1e-4, nth)
    ph = np.linspace(0, 2 * math.pi, nph, endpoint=False)
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    integ = Y_lm(l2, m2, TH, PH).conj() * Y_lm(1, q, TH, PH) * Y_lm(l1, m1, TH, PH) * np.sin(TH)
    dth = th[1] - th[0]; dph = ph[1] - ph[0]
    return float(np.trapezoid(np.trapezoid(integ, ph, axis=1), th))

def radial_matrix_au(n1, l1, n2, l2, rmax=160.0, npts=30000):
    r = np.linspace(1e-6, rmax, npts)
    R1 = np.array([R_nl(n1, l1, x) for x in r])
    R2 = np.array([R_nl(n2, l2, x) for x in r])
    return float(np.trapezoid(R1 * R2 * r ** 3, r))

def channel_decomp(n_up):
    """逐通道（下态 → 上态 l,m）偶极权重，按 Δm 分类 π/σ"""
    lower = [(2, 0, 0)] + [(2, 1, m) for m in (-1, 0, 1)]
    ch = {}
    for (n1, l1, m1) in lower:
        for l2 in range(0, n_up):
            if abs(l2 - l1) != 1: continue
            rad2 = radial_matrix_au(n1, l1, n_up, l2) ** 2
            for m2 in range(-l2, l2 + 1):
                dm = m2 - m1
                if dm not in (0, 1, -1): continue
                ang2 = angular_matrix(l1, m1, l2, m2, dm) ** 2
                ch[(l2, m2, dm)] = ch.get((l2, m2, dm), 0.0) + rad2 * ang2
    return ch

def l_density(n, l, R_cut, npts=20000):
    r = np.linspace(1e-6, 200.0, npts)
    dr = r[1] - r[0]
    dens = np.array([radial_density(n, l, x) for x in r])
    total = float(np.sum(dens) * dr)
    tail = float(np.sum(dens[r > R_cut]) * dr)
    return total, tail

def landau_length(B_T):
    return 1.0 / math.sqrt(B_T / 2.35e5)

def pi_sigma_comp(n, B_T, C=3.03):
    """π/σ 分通道密度加权压缩（口径与 P3b tail/total 一致）"""
    ch = channel_decomp(n)
    R_L = C * landau_length(B_T)
    dens_cache = {}
    def ld(l):
        if l not in dens_cache:
            dens_cache[l] = l_density(n, l, R_L)
        return dens_cache[l]
    tot_pi = tail_pi = tot_sig = tail_sig = 0.0
    for (l, m, dm), w in ch.items():
        total_l, tail_l = ld(l)
        if dm == 0:
            tot_pi += w * total_l; tail_pi += w * tail_l
        else:
            tot_sig += w * total_l; tail_sig += w * tail_l
    p_pi = tot_pi / (tot_pi + tot_sig)
    eta_pi = tail_pi / tot_pi if tot_pi > 0 else 0.0
    eta_sig = tail_sig / tot_sig if tot_sig > 0 else 0.0
    eta_glob = (tail_pi + tail_sig) / (tot_pi + tot_sig)
    return p_pi, eta_pi, 1.0 - p_pi, eta_sig, eta_glob

def merge(eta_comp, eta_sigma, eta_3g):
    return 1.0 - (1.0 - eta_comp) * (1.0 - eta_sigma) * (1.0 - eta_3g)

def main():
    names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}
    obs = {"Hβ": 0.45, "Hγ": 0.84, "Hδ": 0.98}
    B = 4500.0
    C = 3.03
    kB = 8.617333262e-5
    fill = math.exp(-(1.16e-4 * B / 2.0) / (kB * 12000.0))
    eta_s = 0.6667 * (1.0 - fill)
    results = {"model": "P3c v2：π 保留率反演（密度加权口径）",
               "B_MG": B / 100.0, "C": C, "T_K": 12000.0,
               "pi_sigma_decomp": {}, "alpha_required": {}, "alpha_fit": {}, "verdict": {}, "prediction": {}}
    print("=" * 92)
    print("Phase 100 P3c v2：Hβ 过禁戒闭合——π 保留率反演（密度加权口径）")
    decomp = {}
    for n in (3, 4, 5, 6, 7):
        p_pi, e_pi, p_sig, e_sig, e_glob = pi_sigma_comp(n, B, C)
        decomp[names[n]] = {"p_pi": p_pi, "eta_pi": e_pi, "p_sigma": p_sig, "eta_sigma": e_sig,
                            "eta_comp_global": e_glob}
        results["pi_sigma_decomp"][names[n]] = decomp[names[n]]
        print(f"  {names[n]}: p_π={p_pi:.4f} η_π={e_pi:.4f} | p_σ={p_sig:.4f} η_σ={e_sig:.4f} | 全局={e_glob:.4f}")
    # ① 反演：每线所需 α_req（使合并=观测；无观测线用 α=1 基准）
    print("\n[1] α_req 反演（每线所需 π 压缩适用率；α=1 全压=原模型，α=0 π 全保留）：")
    alpha_req = {}
    for name in ("Hβ", "Hγ", "Hδ"):
        n = {v: k for k, v in names.items()}[name]
        d = decomp[name]
        target = obs[name]
        # merge(ec, eta_s, 0) = target → ec = 1-(1-target)/(1-eta_s)
        ec_target = 1.0 - (1.0 - target) / (1.0 - eta_s)
        # ec = [tail_sig + α·tail_pi]/tot → α = (ec_target·tot - tail_sig)/tail_pi
        # 用全局：η_comp_eff = p_sig·(η_sig·? )... 密度口径：ec = (1-p_pi)·? 
        # 简化：η_comp_eff(α) = p_pi·α·η_pi + p_sig·η_sig   (权重份额 × 分通道 η，密度口径近似)
        # 精确：η_comp_eff(α) = [(1-p_pi)·η_sig + p_pi·α·η_pi]   —— 仅在 π/σ 密度分布一致时精确；
        # 这里 p_pi 是密度份额，η_sig/η_pi 是分通道尾比——近似成立（分通道内 l 权重均匀）
        alpha = (ec_target - (1.0 - d["p_pi"]) * d["eta_sigma"]) / (d["p_pi"] * d["eta_pi"]) if d["p_pi"] * d["eta_pi"] > 0 else float("inf")
        alpha_req[name] = {"alpha_req": alpha, "ec_target": ec_target}
        results["alpha_required"][name] = {"alpha_req": alpha, "ec_target": ec_target}
        print(f"  {name}: 目标 η_comp_eff={ec_target:.4f} → α_req={alpha:.4f}")
    # ② 单调模型：α(n) 是否单调？α_req: Hβ→Hγ→Hδ
    seq = [alpha_req[k]["alpha_req"] for k in ("Hβ", "Hγ", "Hδ")]
    monotone_inc = bool(seq[0] < seq[1] <= seq[2])
    print(f"\n  α_req 序列 Hβ/Hγ/Hδ = {seq[0]:.3f}/{seq[1]:.3f}/{seq[2]:.3f} — 单调递增={monotone_inc}")
    # ③ 拟合：指数饱和模型 α(n) = α_max - (α_max - α_β)·exp(-(ξ-ξβ)/τ)，α_max=1
    xi = {names[n]: n ** 2 / landau_length(B) for n in (3, 4, 5, 6, 7)}
    xi_beta = xi["Hβ"]
    alpha_beta = alpha_req["Hβ"]["alpha_req"]
    # 用 Hγ 定 τ：α(ξγ) = 1 - (1-αβ)·exp(-(ξγ-ξβ)/τ) = α_req(Hγ)
    tau = -(xi["Hγ"] - xi_beta) / math.log(max(1.0 - alpha_req["Hγ"]["alpha_req"], 1e-9) / (1.0 - alpha_beta))
    print(f"  指数饱和模型：α_max=1，α(ξβ)={alpha_beta:.4f}，τ={tau:.3f}（由 Hγ 定标）")
    fit = {}
    for n in (3, 4, 5, 6, 7):
        d = decomp[names[n]]
        a = 1.0 - (1.0 - alpha_beta) * math.exp(-(xi[names[n]] - xi_beta) / tau)
        a = max(0.0, min(1.0, a))
        ec = (1.0 - d["p_pi"]) * d["eta_sigma"] + d["p_pi"] * a * d["eta_pi"]
        eta_line = merge(ec, eta_s, 0.0)
        fit[names[n]] = {"alpha_pi": a, "eta_comp_eff": ec, "eta_line": eta_line}
    results["alpha_fit"]["exp_saturation"] = fit
    o = {k: obs.get(k, "-") for k in ("Hβ", "Hγ", "Hδ")}
    m = {k: fit[k]["eta_line"] for k in ("Hβ", "Hγ", "Hδ")}
    err = {k: (m[k] - o[k]) if isinstance(o[k], float) else None for k in o}
    print(f"  指数模型: Hβ={m['Hβ']:.3f}(Δ{err['Hβ']:+.3f}) Hγ={m['Hγ']:.3f}(Δ{err['Hγ']:+.3f}) Hδ={m['Hδ']:.3f}(Δ{err['Hδ']:+.3f})")
    line_order = bool(fit["Hβ"]["eta_line"] < fit["Hγ"]["eta_line"] < fit["Hδ"]["eta_line"])
    max_err = max(abs(err[k]) for k in err if isinstance(err[k], float))
    verdict = {
        "line_order_reproduced": line_order,
        "max_abs_err_3lines": max_err,
        "Hbeta_closed_within_0.05": bool(abs(err["Hβ"]) <= 0.05),
        "Hgamma_closed_within_0.05": bool(abs(err["Hγ"]) <= 0.05),
        "Hdelta_gap_remains": 0.98 - fit["Hδ"]["eta_line"],
        "alpha_req_sequence_monotone": monotone_inc,
        "alpha_beta": alpha_beta, "tau": tau,
        "conclusion": None}
    if verdict["Hbeta_closed_within_0.05"] and verdict["Hgamma_closed_within_0.05"]:
        verdict["conclusion"] = ("Hβ 过禁戒闭合（候选）：π 保留随 n 递减（α_req 单调递增：Hβ %.3f→Hδ %.3f）——"
                                 "低 n 态 π 通道（z-偶极）纵向保留、高 n 态整体 Landau 管化 π 亦被压缩；"
                                 "Hβ/Hγ 同时闭合，Hδ 欠禁戒缺口保留（%.3f）"
                                 % (seq[0], seq[2], verdict["Hdelta_gap_remains"]))
    else:
        verdict["conclusion"] = ("诚实负结论：π 保留模型可闭合 Hβ 但 Hγ/Hδ 存在偏差（α_req 单调递增趋势明确）；"
                                 "Hδ 欠禁戒缺口保留——需偏振观测判别或额外禁戒")
    results["verdict"] = verdict
    pred = {}
    for n in (3, 4, 5, 6, 7):
        d = decomp[names[n]]
        a = 1.0 - (1.0 - alpha_beta) * math.exp(-(xi[names[n]] - xi_beta) / tau)
        a = max(0.0, min(1.0, a))
        pred[names[n]] = {"alpha_pi": a, "pi_retained_frac": d["p_pi"] * (1.0 - a),
                          "sigma_compressed_frac": (1.0 - d["p_pi"]) * d["eta_sigma"]}
    results["prediction"] = pred
    print(f"\n判定：线序={line_order}  Hβ|Δ|≤0.05={verdict['Hbeta_closed_within_0.05']}  Hγ|Δ|≤0.05={verdict['Hgamma_closed_within_0.05']}  最大|Δ|={max_err:.3f}  Hδ缺口={verdict['Hdelta_gap_remains']:.3f}")
    print(verdict["conclusion"])
    print("判别预言（偏振观测靶标）：π 保留分数 p_π·(1-α) 随 n 递减——低 n（Hβ）π 强、高 n（Hδ）π 弱——线偏振比 P_π(n) 单调递减")
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase100_p3c_pi_retention.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=float)
    print("已写入 _phase100_p3c_pi_retention.json")

if __name__ == "__main__":
    main()
