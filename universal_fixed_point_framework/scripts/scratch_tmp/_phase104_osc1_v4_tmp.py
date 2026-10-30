# -*- coding: utf-8 -*-
"""Phase 104az-59 v4 ★★★ 决定性计算（半解析版）：固定 n 流形抗磁对角化 → S_win(n,B)
中场 10-50 MG 对氢 γ=ħω_c/2Ryd = B/2350MG ~ 0.004-0.02（弱场）——标准物理 = Zeeman 线性 + 抗磁 l 混合
π 通道（m=0，Δm=0）：Zeeman 线性不位移 π——只有抗磁 B²ρ²/8 的 l 混合 + 位移
- 每 n 流形（m=0 子空间，l = n-1, n-3, ..., ≥0）构造抗磁矩阵 <nl|B²ρ²/8|nl'> 对角化
- 混合态 |α> = Σ c_l |n,l>——能量 E_α（抗磁位移）
- π 振子强度（相干）：f_α = |Σ_l c_l <2s/2pz|z|n,l>|²（只取 z 偶极允许的 l）
- S_win(n,B) = Σ_{α: |E_α-E2-E_ph|<ΔE(±80Å)} f_α / Σ_α f_α
- TRK 自检：Σ_α f_α 守恒
径向矩阵元：解析 R_nl 数值积分；角向：球谐数值积分（Gaunt）
"""
import json, io, os
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, factorial, sph_harm_y

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# ---------- 氢原子径向波函数 R_nl(r)（au） ----------
def R_nl(n, l, r):
    """R_nl = sqrt((2/n)^3 (n-l-1)!/(2n(n+l)!)) * e^{-r/n} (2r/n)^l L_{n-l-1}^{2l+1}(2r/n)"""
    r = np.asarray(r, dtype=float)
    rho = 2.0*r/n
    norm = np.sqrt((2.0/n)**3 * factorial(n-l-1) / (2.0*n*factorial(n+l)))
    L = genlaguerre(n-l-1, 2*l+1)(rho)
    return norm * np.exp(-r/n) * (2.0*r/n)**l * L

def radial_int(n, l, np_, lp, power, r_max=120.0, N=4000):
    """<nl|r^power|n'l'> 数值积分（辛普森）"""
    r = np.linspace(1e-8, r_max, N)
    dr = r[1]-r[0]
    f = R_nl(n, l, r) * R_nl(np_, lp, r) * r**power * r*r  # 体积元 r²dr
    return np.trapezoid(f, r) if hasattr(np, 'trapezoid') else np.trapz(f, r)

# ---------- 角向 Gaunt（数值，m=m'=0 情形即球谐 Y_l0） ----------
def gaunt_cos(l1, l2):
    """<Y_l1,0|cosθ|Y_l2,0>——z 偶极（π）角向因子（取实部）"""
    th, w = leggauss(96)
    th = np.arccos(th)  # θ 从 0..π
    c = np.cos(th)
    y1 = sph_harm_y(l1, 0, th, 0.0)
    y2 = sph_harm_y(l2, 0, th, 0.0)
    integrand = np.conj(y1) * c * y2 * np.sin(th)
    return float(np.real(np.sum(w * integrand)))

def gaunt_sin2(l1, l2):
    """<Y_l1,0|sin²θ|Y_l2,0>——ρ² 角向因子（m=0，取实部）"""
    th, w = leggauss(96)
    th = np.arccos(th)
    s2 = np.sin(th)**2
    y1 = sph_harm_y(l1, 0, th, 0.0)
    y2 = sph_harm_y(l2, 0, th, 0.0)
    integrand = np.conj(y1) * s2 * y2 * np.sin(th)
    return float(np.real(np.sum(w * integrand)))

# 预计算角向因子（l ≤ 7）
LMAX = 8
GC = {}  # (l1,l2) -> cos Gaunt
GS = {}  # (l1,l2) -> sin² Gaunt
for l1 in range(LMAX):
    for l2 in range(LMAX):
        if abs(l1-l2) == 1:      # cosθ 选择定则
            GC[(l1,l2)] = gaunt_cos(l1, l2)
        if abs(l1-l2) in (0, 2): # sin²θ = 1-cos²θ：Δl=0,±2
            GS[(l1,l2)] = gaunt_sin2(l1, l2)

# ---------- Balmer 线参数（跃迁能 = 1/8 - 1/2n²，正值） ----------
E2 = -1.0/8.0
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
W_ANG = 80.0

def pi_strength(n, l, n2_states):
    """π 振子强度 <n=2 流形|z|n,l>（相干）——n2_states = [(l2, coeff)]——返回复振幅"""
    tot = 0.0 + 0.0j
    for l2, coeff in n2_states:
        if abs(l2-l) == 1:
            g = GC.get((l2, l), GC.get((l, l2), 0.0))
            if abs(g) > 1e-12:
                ri = radial_int(2, l2, n, l, 1)
                tot += coeff * ri * g
    return tot

def run(B_au):
    B2 = B_au*B_au
    out = {"B_au": B_au, "B_MG": B_au*2350.0, "lines": {}}
    for n, (lam, Eph) in LINES.items():
        dE = Eph * 2.0*W_ANG / lam
        # n 流形 m=0 子空间：所有 l = 0..n-1（每 l 有 m=0 分量）
        ls = list(range(n))
        # 抗磁矩阵（对角化前先算）
        M = np.zeros((len(ls), len(ls)))
        for a, l in enumerate(ls):
            for b, lp in enumerate(ls):
                if abs(l-lp) in (0, 2):
                    g = GS.get((l, lp), GS.get((lp, l), 0.0))
                    if abs(g) > 1e-12:
                        M[a, b] = radial_int(n, l, n, lp, 2) * g
        M *= 0.125 * B2  # B²ρ²/8
        evals, evecs = np.linalg.eigh(M)
        # n=2 流形（m=0：2s(l=0) 与 2p_z(l=1)——π 耦合源）
        # 2s 对奇 l（p 型）；2p_z 对偶 l（s/d 型）
        n2_states = [(0, 1.0), (1, 1.0)]  # 2s + 2p_z（简并组合系数 1）
        # 各混合态 π 强度（相干）
        f_alpha = []
        for a in range(len(ls)):
            # 混合态 |α> = Σ_l evecs[l,a] |n,l>
            amp = 0.0
            for b, l in enumerate(ls):
                amp += evecs[b, a] * pi_strength(n, l, n2_states)
            E_alpha = Eph + evals[a]  # 跃迁能（正）+ 抗磁位移
            f_alpha.append((E_alpha, abs(amp)**2))
        total = sum(f for _, f in f_alpha)
        s_win = sum(f for Ea, f in f_alpha if abs(Ea - Eph) < dE)
        out["lines"][str(n)] = {"s_win": float(s_win), "total": float(total),
                                "frac": float(s_win/total) if total > 1e-30 else 0.0,
                                "n_alpha": len(f_alpha),
                                "shifts": [float(Ea-Eph) for Ea, _ in f_alpha],
                                "dE": float(dE),
                                "ls": ls,
                                "fs": [float(f) for _, f in f_alpha]}
    return out

print("=== v4 半解析：固定 n 流形抗磁对角化 → π 通道 S_win(n,B) ±80 Å ===", flush=True)
B_list = (0.0001, 0.005, 0.01, 0.02, 0.05)
results = []
for B in B_list:
    print("B=%.4f a.u. (%.1f MG)..." % (B, B*2350), flush=True)
    out = run(B)
    results.append(out)
    ln = out["lines"]
    print("  Hα %6.2f%% Hβ %6.2f%% Hγ %6.2f%% Hδ %6.2f%% Hε %6.2f%%  (窗内份额)" % (
        100*ln["3"]["frac"], 100*ln["4"]["frac"], 100*ln["5"]["frac"],
        100*ln["6"]["frac"], 100*ln["7"]["frac"]), flush=True)
    if B < 0.001:
        for n in (3, 4):
            print("  DEBUG n=%d: dE=%.2e ls=%s shifts=%s fs=%s" % (
                n, ln[str(n)]["dE"], ln[str(n)]["ls"],
                ["%.1e" % s for s in ln[str(n)]["shifts"]],
                ["%.2e" % f for f in ln[str(n)]["fs"]]), flush=True)
    print("  total: Hα %.4e Hβ %.4e Hγ %.4e Hδ %.4e Hε %.4e" % (
        ln["3"]["total"], ln["4"]["total"], ln["5"]["total"],
        ln["6"]["total"], ln["7"]["total"]), flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_v4.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_osc_pi_v4.json")
