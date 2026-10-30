# -*- coding: utf-8 -*-
"""Phase 100 P3：机制分解线加权合并——σ 填充 × 第三门 能否回归观测线序缺失
观测输入（Paper 48 §4.9 DESI 8-25kK 扩容，中场 40.9-51.0 MG，n=16）：
  - 分线序纯线深降幅：Hβ −45% / Hγ −84% / Hδ −98%
  - 总纯线深 −63.1%；总 EW 缺失 46.9%（Amorim 12 中场 vs 188 弱场）
模型：
  1. 逐线 σ 份额（P1 通道分解扩展 n=3..7）
  2. η_σ(n,B) = σ_frac(n) × (1 − Landau 填充率)   [P1]
  3. η_3g(n,B) = 第三门（纵向电离→闭合性破坏）     [P2]
  4. 合并 η_line = 1 − (1−η_σ)(1−η_3g)（独立机制乘法）
  5. 线加权总缺失（无场理论 EW 权重近似 Hα:Hβ:Hγ:Hδ:Hε = 1:0.5:0.35:0.25:0.15）
判定：能否回归观测线序（Hβ<Hγ<Hδ）与量级（−45/−84/−98%）？若不能→诚实负结论登记缺口
"""
import json, math
import numpy as np

# ---------- 复用 P1 通道分解 ----------
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

def radial_matrix(n1, l1, n2, l2, rmax=120.0, npts=30000):
    r = np.linspace(1e-6, rmax, npts)
    R1 = np.array([R_nl(n1, l1, x) for x in r])
    R2 = np.array([R_nl(n2, l2, x) for x in r])
    return float(np.trapezoid(R1 * R2 * r ** 3, r))

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

def balmer_channel_weights(n_up):
    lower = [(2, 0, 0)] + [(2, 1, m) for m in (-1, 0, 1)]
    W = {q: 0.0 for q in (0, 1, -1)}
    for (n1, l1, m1) in lower:
        for l2 in range(0, n_up):
            if abs(l2 - l1) != 1: continue
            for m2 in range(-l2, l2 + 1):
                dm = m2 - m1
                if dm not in (0, 1, -1): continue
                d = radial_matrix(n1, l1, n_up, l2) * angular_matrix(l1, m1, l2, m2, dm)
                W[dm] += abs(d) ** 2
    return W

# ---------- P1: σ 填充 ----------
def landau_fill(B_T, T_K=12000.0):
    """末态 m'=±1 层玻尔兹曼填充率"""
    kB = 8.617333262e-5
    dE = 1.16e-4 * B_T / 2.0          # |m|=1 Landau 间隔（eV）
    return math.exp(-dE / (kB * T_K))

# ---------- P2: 第三门 ----------
def third_gate_eta(n, B_T):
    """纵向电离→闭合性破坏→第三门禁戒因子（P2 模型）"""
    RYD = 13.6057
    E_bind = RYD / n ** 2
    E_cycle = RYD * (1.0 / 4.0 - 1.0 / n ** 2)
    hbar_wc_half = (B_T / 2.35e5) * 13.6057   # ħω_c/2 (eV)
    E_z = hbar_wc_half - E_bind
    if E_z <= 0:
        return 0.0
    phi = 4.0 * math.pi * E_z / E_cycle
    eps = min(1.0, 2.0 * abs(math.sin(phi / 2.0)))
    return 1.0 - math.exp(-eps)

def main():
    names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}
    ew_weights = {3: 1.0, 4: 0.5, 5: 0.35, 6: 0.25, 7: 0.15}  # 无场理论 EW 近似权重
    obs_lines = {"Hβ": 0.45, "Hγ": 0.84, "Hδ": 0.98}   # DESI 中场 40.9-51.0 MG 纯线深降幅
    B_desi = [4090.0, 4500.0, 5100.0]                   # T（40.9-51.0 MG）
    results = {"model": "P3 机制分解：σ填充×第三门 线加权合并", "T_K": 12000.0,
               "per_line": {}, "merged": {}, "verdict": {}}
    print("=" * 84)
    print("Phase 100 P3：机制分解线加权合并（DESI 中场 40.9-51.0 MG）")
    print(f"\n{'线':<6}{'σ份额':<8}{'η_σ(45MG)':<12}{'η_3g(45MG)':<12}{'合并η':<10}{'观测':<10}")
    for n in (3, 4, 5, 6, 7):
        W0 = balmer_channel_weights(n)
        sfrac = (W0[1] + W0[-1]) / sum(W0.values())
        fill45 = landau_fill(4500.0)
        eta_s = sfrac * (1.0 - fill45)
        eta_3g = third_gate_eta(n, 4500.0)
        eta_line = 1.0 - (1.0 - eta_s) * (1.0 - eta_3g)
        obs = obs_lines.get(names[n], "-")
        results["per_line"][names[n]] = {"n": n, "sigma_fraction": sfrac,
                                         "eta_sigma_45MG": eta_s, "eta_3g_45MG": eta_3g,
                                         "eta_line_45MG": eta_line}
        print(f"{names[n]:<6}{sfrac:<8.4f}{eta_s:<12.4f}{eta_3g:<12.4f}{eta_line:<10.4f}{obs}")
    # 线加权总缺失（B 扫描）
    for B in B_desi:
        tot_num = 0.0; tot_den = 0.0
        per = {}
        for n in (3, 4, 5, 6, 7):
            W0 = balmer_channel_weights(n)
            sfrac = (W0[1] + W0[-1]) / sum(W0.values())
            eta_s = sfrac * (1.0 - landau_fill(B))
            eta_3g = third_gate_eta(n, B)
            eta_line = 1.0 - (1.0 - eta_s) * (1.0 - eta_3g)
            per[names[n]] = eta_line
            tot_num += ew_weights[n] * eta_line
            tot_den += ew_weights[n]
        results["merged"][f"{B/100:.1f}MG"] = {"total_eta": tot_num / tot_den, "per_line": per}
    # 判定（45 MG 代表）
    rep = results["merged"]["45.0MG"]["per_line"]
    verdict = {
        "obs_Hbeta_Hgamma_Hdelta": ["Hβ −45%", "Hγ −84%", "Hδ −98%"],
        "model_45MG_Hbeta": rep["Hβ"], "model_45MG_Hgamma": rep["Hγ"], "model_45MG_Hdelta": rep["Hδ"],
        "model_total_45MG": results["merged"]["45.0MG"]["total_eta"],
        "obs_total_EW": 0.469, "obs_pure_depth": 0.631,
        "reproduces_line_order": bool(rep["Hβ"] < rep["Hγ"] < rep["Hδ"]),
        "reaches_obs_magnitude": bool(rep["Hδ"] >= 0.9),
        "gap_Hdelta": 0.98 - rep["Hδ"],
        "conclusion": None}
    if verdict["reproduces_line_order"] and verdict["reaches_obs_magnitude"]:
        verdict["conclusion"] = "两机制协同回归观测线序与量级"
    else:
        verdict["conclusion"] = ("诚实负结论：σ填充(≈15%)+第三门(≈0%@<65MG)在 DESI 中场（40.9-51.0 MG）"
                                 "合计 ≈15-20%，无法回归观测 Hδ −98% 与总缺失 63%——中场线序缺失需新机制或归因重审")
    results["verdict"] = verdict
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase100_p3_mechanism_decomposition.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=float)
    print("\n线加权总缺失（B 扫描）：")
    for k, v in results["merged"].items():
        print(f"  {k}: 总 η = {v['total_eta']:.4f}  逐线 = " + ", ".join(f"{kk}:{vv:.3f}" for kk, vv in v["per_line"].items()))
    print(f"\n判定（45 MG）: 线序复现={verdict['reproduces_line_order']}  量级达标(Hδ≥0.9)={verdict['reaches_obs_magnitude']}  Hδ缺口={verdict['gap_Hdelta']:.3f}")
    print(verdict["conclusion"])
    print("已写入 _phase100_p3_mechanism_decomposition.json")

if __name__ == "__main__":
    main()
