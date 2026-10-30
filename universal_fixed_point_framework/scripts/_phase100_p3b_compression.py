# -*- coding: utf-8 -*-
"""Phase 100 P3b：高 n 横向压缩 η_comp(n,B) 量化——闭合 P3 线序缺口
物理：Balmer 上态 n=3..7 各 l 分波径向分布（按偶极权重加权）
      横向支撑半径 R_L = C·ℓ_B（Landau 可支撑区）
      η_comp = 无场态在 r > R_L 的加权分数（横向环绕循环被 Landau 紧致切断）
物理锚点：圆态（l=n-1）经典轨道半径 r_orbit = n²a₀——与 ℓ_B 竞争
对照观测：DESI 中场 40.9-51.0 MG 线序 Hβ −45%/Hγ −84%/Hδ −98%
三机制合并：η_line = 1-(1-η_comp)(1-η_σ)(1-η_3g)
诚实边界：球坐标径向 tail 代理横向分布（圆态准确、低 l 分波保守）；C 自由参数（C=2,3,4 扫描）
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
    """|R_nl(r)|²·r²（球壳概率密度）"""
    R = R_nl(n, l, r)
    return R * R * r * r

# 偶极权重：n=2 → n_up 各 l 分波的跃迁权重（径向×角向，同 P1/P3）
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

def balmer_l_weights(n_up):
    """n=2 → n_up 各 l 分波偶极权重 w_l（径向×角向合并）"""
    lower = [(2, 0, 0)] + [(2, 1, m) for m in (-1, 0, 1)]
    wl = {}
    for (n1, l1, m1) in lower:
        for l2 in range(0, n_up):
            if abs(l2 - l1) != 1: continue
            rad2 = radial_matrix_au(n1, l1, n_up, l2) ** 2
            for m2 in range(-l2, l2 + 1):
                dm = m2 - m1
                if dm not in (0, 1, -1): continue
                ang2 = angular_matrix(l1, m1, l2, m2, dm) ** 2
                wl[l2] = wl.get(l2, 0.0) + rad2 * ang2
    return wl

def radial_matrix_au(n1, l1, n2, l2, rmax=160.0, npts=30000):
    r = np.linspace(1e-6, rmax, npts)
    R1 = np.array([R_nl(n1, l1, x) for x in r])
    R2 = np.array([R_nl(n2, l2, x) for x in r])
    return float(np.trapezoid(R1 * R2 * r ** 3, r))

def tail_fraction(n_up, R_cut, npts=20000):
    """加权 tail 分数：r > R_cut 的权重占比"""
    wl = balmer_l_weights(n_up)
    W = sum(wl.values())
    r = np.linspace(1e-6, 200.0, npts)
    dr = r[1] - r[0]
    dens = np.zeros_like(r)
    for l, w in wl.items():
        dens += w * np.array([radial_density(n_up, l, x) for x in r])
    total = float(np.sum(dens) * dr)
    tail = float(np.sum(dens[r > R_cut]) * dr)
    return tail / total, tail / W, total / W  # (tail分数, 归一化确认, 总归一)

def landau_length(B_T):
    return 1.0 / math.sqrt(B_T / 2.35e5)

def eta_comp(n, B_T, C):
    R_L = C * landau_length(B_T)
    tf, _, _ = tail_fraction(n, R_L)
    return tf

def main():
    names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}
    obs = {"Hβ": 0.45, "Hγ": 0.84, "Hδ": 0.98}
    results = {"model": "P3b 高n横向压缩 η_comp = r>C·ℓ_B 加权tail分数", "C_scan": {}, "merged": {}, "verdict": {}}
    print("=" * 96)
    print("Phase 100 P3b：高 n 横向压缩 η_comp(n,B) 量化")
    for C in (2.0, 3.0, 4.0):
        print(f"\n[C = {C}（Landau 可支撑半径 R_L = {C}·ℓ_B）]")
        row = {}
        for n in (3, 4, 5, 6, 7):
            eta = eta_comp(n, 4500.0, C)
            row[names[n]] = eta
        results["C_scan"][f"C={C}"] = row
        print("  45 MG: " + ", ".join(f"{k}:{v:.3f}" for k, v in row.items()))
    # 三机制合并（B=45 MG，C=3 代表）：η_line = 1-(1-η_comp)(1-η_σ)(1-η_3g)
    C_rep = 3.0
    B = 4500.0
    kB = 8.617333262e-5
    fill = math.exp(-(1.16e-4 * B / 2.0) / (kB * 12000.0))   # σ 填充率
    print("\n三机制合并（45 MG，C=3，σ填充 + 压缩 + 第三门）：")
    for n in (3, 4, 5, 6, 7):
        W0 = balmer_l_weights(n)
        sfrac = sum(W0.values())  # 占位（σ 份额在合并中不直接用 l 权重）
    # 逐线 σ 份额（P1 口径）与第三门（P2 口径）
    from math import exp as mexp
    def landau_fill(B_T): return mexp(-(1.16e-4*B_T/2.0)/(kB*12000.0))
    def third_gate(n, B_T):
        RYD = 13.6057
        E_bind = RYD / n**2
        E_cycle = RYD * (1.0/4.0 - 1.0/n**2)
        E_z = (B_T/2.35e5)*RYD - E_bind
        if E_z <= 0: return 0.0
        phi = 4.0*math.pi*E_z/E_cycle
        eps = min(1.0, 2.0*abs(math.sin(phi/2.0)))
        return 1.0 - mexp(-eps)
    # σ 份额：用通道权重（角向选择定则）——P3 已证 σ 份额逐线相同 0.6667
    sfrac = 0.6667
    eta_s = sfrac * (1.0 - landau_fill(B))
    print(f"\n{'线':<6}{'η_comp':<10}{'η_σ':<10}{'η_3g':<10}{'合并η':<10}{'观测':<10}{'缺口'}")
    for n in (3, 4, 5, 6, 7):
        ec = eta_comp(n, B, C_rep)
        es = eta_s
        e3 = third_gate(n, B)
        em = 1.0 - (1.0-ec)*(1.0-es)*(1.0-e3)
        ob = obs.get(names[n], "-")
        gap = (ob - em) if ob != "-" else None
        results["merged"][names[n]] = {"eta_comp": ec, "eta_sigma": es, "eta_3g": e3, "eta_line": em, "obs": ob, "gap": gap}
        print(f"{names[n]:<6}{ec:<10.3f}{es:<10.3f}{e3:<10.3f}{em:<10.3f}{ob:<10}{gap if gap is None else f'{gap:.3f}'}")
    # 判定
    rep = results["merged"]
    verdict = {
        "line_order_reproduced": bool(rep["Hβ"]["eta_line"] < rep["Hγ"]["eta_line"] < rep["Hδ"]["eta_line"]),
        "Hdelta_reached_0.9": bool(rep["Hδ"]["eta_line"] >= 0.9),
        "Hbeta_gap": rep["Hβ"]["gap"], "Hgamma_gap": rep["Hγ"]["gap"], "Hdelta_gap": rep["Hδ"]["gap"],
        "conclusion": None}
    if verdict["line_order_reproduced"] and verdict["Hdelta_reached_0.9"]:
        verdict["conclusion"] = "三机制协同回归观测线序与量级——P3 缺口闭合（候选）"
    else:
        verdict["conclusion"] = "线序复现=" + str(verdict["line_order_reproduced"]) + "，Hδ量级达标=" + str(verdict["Hdelta_reached_0.9"]) + "——仍需调整（C 扫描/归因）"
    results["verdict"] = verdict
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase100_p3b_compression.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=float)
    print(f"\n判定：线序复现={verdict['line_order_reproduced']}  Hδ≥0.9={verdict['Hdelta_reached_0.9']}  Hβ缺口={verdict['Hbeta_gap']:.3f}  Hγ缺口={verdict['Hgamma_gap']:.3f}  Hδ缺口={verdict['Hdelta_gap']:.3f}")
    print(verdict["conclusion"])
    print("已写入 _phase100_p3b_compression.json")

if __name__ == "__main__":
    main()
