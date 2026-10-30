# -*- coding: utf-8 -*-
"""Phase 86 R4b：RWA 全渠道吸收系数计算（直接编码论文公式）
Eq.44 df/dE, Eq.43 sigma, Eq.56 磁场重标度, Eq.60 束缚能, Eq.64 阈值位移, Eq.68 占据数
计算中场(B=10-100 MG) vs 零场 的 Balmer 连续谱吸收比 at 观测带
对账：RWA 理论上限 vs 观测增强 +0.058 dex
"""
import json, io, os, math
import numpy as np

# ---- 常数 ----
alpha = 7.2973525693e-3
a0 = 5.29177210903e-9  # cm
B0 = 4.70103e9  # G
RYD = 13.605693  # eV
PI = math.pi

def sigma_nk(n, k):
    """Eq.43+44: 零场总光致电离截面（cm^2），epsilon 单位 Ry"""
    # df/dE (Eq.44)
    n3 = n ** 3
    k8 = k ** 8
    denom = (n ** 2 + k ** 2) ** (2 * n + 2)
    expo = math.exp(-4 * k * math.atan(n / k))
    dfde = (128 / 3) * n3 * k8 / denom * expo / (1 - math.exp(-2 * PI * k))
    return 4 * PI ** 2 * alpha * a0 ** 2 * dfde  # cm^2

# ---- n=2 Balmer 连续谱：零场 ----
def sigma2_zero(eps):
    """零场 n=2 连续谱截面（总，含所有子态简并）"""
    k = (eps - 0.25) ** (-0.5)
    if k <= 0 or not np.isfinite(k):
        return 0.0
    return sigma_nk(2, k)

# ---- 磁场子态（n=2: 2s m=0; 2p m=-1,0,+1；m_s=+1/2,-1/2）----
# 束缚能 Eq.60：E = -1/n^2 + 4(m/2+m_s)beta + n^2[5n^2+1-3l(l+1)](l^2+l-1+m^2)/((2l-1)(2l+3)) beta^2
def binding_energy(n, l, m, ms, beta):
    e0 = -1.0 / n ** 2
    lin = 4 * (m / 2 + ms) * beta
    quad = n ** 2 * (5 * n ** 2 + 1 - 3 * l * (l + 1)) * (l ** 2 + l - 1 + m ** 2)
    if (2 * l - 1) * (2 * l + 3) != 0:
        quad = quad / ((2 * l - 1) * (2 * l + 3)) * beta ** 2
    else:
        quad = 0
    return e0 + lin + quad

# 阈值 Eq.64（q=0 情形为主；给出 q=+1/-1 修正）
def threshold_emax(n, l, m, ms, beta, q):
    """E_{xi,*}（最小光致电离能量，Ry）。E_{-|m|}=|binding(n,l,|m|)| 近似"""
    emm = -binding_energy(n, l, abs(m), ms, beta)  # -E_{-|m|} = |E_{-|m|}| (束缚能绝对值)
    if q == +1 and m >= 0:
        eth = emm + 4 * beta
    elif q == -1 and m >= 1:
        eth = emm - 4 * beta
    else:
        eth = emm
    return max(0.0, eth)

# 截面重标度 Eq.56: sigma_xi(E) = E/(E-D) sigma0(E-D)，D = E_{xi,*} - E_{xi,0}，E_{xi,0}=1/n^2
def sigma_xi(n, l, m, ms, beta, q, eps):
    exi0 = 1.0 / n ** 2
    exis = threshold_emax(n, l, m, ms, beta, q)
    delta = exis - exi0
    eps_shift = eps - delta
    if eps_shift <= exi0 + 1e-6:
        return 0.0  # 低于零场阈值无吸收
    s0 = sigma_nk(n, (eps_shift) ** (-0.5)) if eps_shift > 0 else 0.0
    return eps / max(eps_shift, 1e-6) * s0

# 占据数 Eq.68 Boltzmann 因子（比值计算：零场归一）
def weight(n, l, m, ms, beta, T_k):
    eb = binding_energy(n, l, m, ms, beta)  # 负值（束缚）
    return math.exp(eb / kT_ry(T_k))

def kT_ry(T_k):
    return 8.617333262e-5 * T_k / RYD  # Ry

# ---- 吸收系数比（Balmer 连续谱，q 平均）----
def chi_ratio(B_mg, T_k, eps_grid, q_weights=(1 / 3, 1 / 3, 1 / 3)):
    beta = B_mg * 1e6 / B0
    kt = kT_ry(T_k)
    # 子态表
    states = []
    for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
        for m in range(-l, l + 1):
            for ms in mslist:
                states.append((2, l, m, ms))
    # 零场吸收（同能量网格，占据数零场=1/n^2 每子态）
    chi0 = np.zeros(len(eps_grid))
    chiB = np.zeros(len(eps_grid))
    for n, l, m, ms in states:
        # 零场：所有子态同截面（无磁场简并），权重均匀
        s0 = np.array([sigma2_zero(e) for e in eps_grid])
        chi0 += s0
        # 磁场：三极化平均
        sB = 0.0
        for q, wq in zip([-1, 0, 1], q_weights):
            sB += wq * np.array([sigma_xi(n, l, m, ms, beta, q, e) for e in eps_grid])
        # 占据权重（相对零场均匀）
        wB = weight(n, l, m, ms, beta, T_k) / (1.0 / n ** 2)
        chiB += wB * sB
    return chi0, chiB

# ---- 观测带 ----
BANDS = {"blue(3600-3640)": (3600, 3640), "red(3700-3750)": (3700, 3750),
         "slopeA(4000-4060)": (4000, 4060), "slopeB(5000-5800)": (5000, 5800)}

def band_avg(chi, eps, wl, bd):
    m = (wl >= bd[0]) & (wl <= bd[1])
    return np.mean(chi[m]) if np.sum(m) > 0 else None

wl = np.linspace(3400, 6200, 561)
eps = 13.605693 / (1240.0 / wl) / RYD  # eV / Ry
# 只取 Balmer 阈值以上
mask = eps > 0.25 + 1e-4
eps = eps[mask]; wl = wl[mask]

results = []
for B in [10, 30, 50, 100]:
    for T in [12000, 15000, 20000]:
        chi0, chiB = chi_ratio(B, T, eps)
        row = {"B_MG": B, "T_K": T}
        for nm, bd in BANDS.items():
            c0 = band_avg(chi0, eps, wl, bd)
            cb = band_avg(chiB, eps, wl, bd)
            if c0 and cb and cb > 0:
                row[nm] = float(np.log10(cb / c0))
            else:
                row[nm] = None
        results.append(row)
        print("B=%3d MG T=%5dK | blue %s | red %s | slopeA %s | slopeB %s (dex, +增强/-减弱)" % (
            B, T, "n/a" if row.get("blue(3600-3640)") is None else "%+.4f" % row["blue(3600-3640)"],
            "n/a" if row.get("red(3700-3750)") is None else "%+.4f" % row["red(3700-3750)"],
            "n/a" if row.get("slopeA(4000-4060)") is None else "%+.4f" % row["slopeA(4000-4060)"],
            "n/a" if row.get("slopeB(5000-5800)") is None else "%+.4f" % row["slopeB(5000-5800)"]))

out = {"method": "RWA 全渠道（Eq.44/56/58/60/64/68）Balmer 连续谱吸收比；q 平均；占据数 Boltzmann 权重",
       "bands": BANDS, "results": results}
with io.open(os.path.join(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs",
                          "paperX_wd_rwa_chi.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("\nwritten: paperX_wd_rwa_chi.json")
