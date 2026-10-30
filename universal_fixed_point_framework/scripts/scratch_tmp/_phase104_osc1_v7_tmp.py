# -*- coding: utf-8 -*-
"""Phase 104az-60 v7：Zeeman+抗磁联合对角化（修正 v6 刚性 Zeeman 近似）
- σ± 通道：±B/2 作为对角项（m 守恒，全部 l 同值）与抗磁矩阵联合对角化
- π 通道：m=0 无 Zeeman 线性项——抗磁对角化（同 v6）
- 矩阵元与能量均取自联合本征态——对比 v6 刚性近似的偏差量级
- 输出：S_win(n,B) + 每线能量分布（准 Landau 区间分量结构）
"""
import json, io, os
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, factorial, lpmv

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def Ylm(l, m, th):
    th = np.asarray(th, dtype=float)
    P = lpmv(abs(m), l, np.cos(th))
    CS = (-1.0)**m if m >= 0 else 1.0
    if abs(m) > l:
        return np.zeros_like(th)
    norm = np.sqrt((2*l+1)/(4*np.pi) * factorial(l-abs(m)) / factorial(l+abs(m)))
    return CS * norm * P

def R_nl(n, l, r):
    rho = 2.0*r/n
    norm = np.sqrt((2.0/n)**3 * factorial(n-l-1) / (2.0*n*factorial(n+l)))
    L = genlaguerre(n-l-1, 2*l+1)(rho)
    return norm * np.exp(-r/n) * (2.0*r/n)**l * L

def radial_int(n, l, np_, lp, power, r_max=120.0, N=8000):
    r = np.linspace(1e-8, r_max, N)
    f = R_nl(n, l, r) * R_nl(np_, lp, r) * r**power * r*r
    return float(np.trapezoid(f, r) if hasattr(np, 'trapezoid') else np.trapz(f, r))

def gaunt_cos(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    y1 = Ylm(l1, 0, th); y2 = Ylm(l2, 0, th)
    return float(np.sum(w * y1 * np.cos(th) * y2) * (2*np.pi))

def gaunt_sin2(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    y1 = Ylm(l1, 0, th); y2 = Ylm(l2, 0, th)
    return float(np.sum(w * y1 * np.sin(th)**2 * y2) * (2*np.pi))

def gaunt_sigma(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    y1 = Ylm(l1, 0, th); y2 = Ylm(l2, 1, th)
    return float(-np.sum(w * y1 * np.sin(th) * y2) * (2*np.pi) / np.sqrt(2.0))

def gaunt_sin2_m1(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    y1 = Ylm(l1, 1, th); y2 = Ylm(l2, 1, th)
    return float(np.sum(w * y1 * np.sin(th)**2 * y2) * (2*np.pi))

LMAX = 8
GC, GS, GSIG, GSM1 = {}, {}, {}, {}
for l1 in range(LMAX):
    for l2 in range(LMAX):
        if abs(l1-l2) == 1:
            GC[(l1,l2)] = gaunt_cos(l1, l2)
            GSIG[(l1,l2)] = gaunt_sigma(l1, l2)
        if abs(l1-l2) in (0, 2):
            GS[(l1,l2)] = gaunt_sin2(l1, l2)
            GSM1[(l1,l2)] = gaunt_sin2_m1(l1, l2)

# 自检
print("=== v7 归一化自检 ===", flush=True)
th, w = leggauss(96); th = np.arccos(th)
y00 = Ylm(0, 0, th)
print("∫|Y00|²(×2π 应=1):", np.sum(w*y00*y00)*2*np.pi, flush=True)
print("GC(0,1) 应=0.5774:", GC[(0,1)], flush=True)
print("GSIG(0,1) 应=-0.5774:", GSIG[(0,1)], flush=True)

E2 = -1.0/8.0
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
W_ANG = 80.0

def run(B_au):
    B2 = B_au*B_au
    out = {"B_au": B_au, "B_MG": B_au*2350.0, "lines": {}}
    for n, (lam, Eph) in LINES.items():
        dE = Eph * 2.0*W_ANG / lam
        ls = list(range(n))
        # π 通道（m=0：无 Zeeman 线性项——抗磁对角化）
        M = np.zeros((len(ls), len(ls)))
        for a, l in enumerate(ls):
            for b, lp in enumerate(ls):
                if abs(l-lp) in (0, 2):
                    g = GS.get((l, lp), GS.get((lp, l), 0.0))
                    if abs(g) > 1e-12:
                        M[a, b] = radial_int(n, l, n, lp, 2) * g
        M *= 0.125 * B2
        evals, evecs = np.linalg.eigh(M)
        n2_states = [(0, 1.0), (1, 1.0)]
        f_pi = []
        for a in range(len(ls)):
            amp = 0.0
            for b, l in enumerate(ls):
                tot = 0.0
                for l2, coeff in n2_states:
                    if abs(l2-l) == 1:
                        g = GC.get((l2, l), GC.get((l, l2), 0.0))
                        if abs(g) > 1e-12:
                            tot += coeff * radial_int(2, l2, n, l, 1) * g
                amp += evecs[b, a] * tot
            f_pi.append((Eph + evals[a], amp**2))
        # σ± 通道（m=±1：Zeeman 项 ±B/2 对角 + 抗磁——联合对角化）
        f_sig = []
        for sgn in (+1, -1):
            M2 = np.zeros((len(ls), len(ls)))
            for a, l in enumerate(ls):
                for b, lp in enumerate(ls):
                    if abs(l-lp) in (0, 2):
                        g = GSM1.get((l, lp), GSM1.get((lp, l), 0.0))
                        if abs(g) > 1e-12:
                            M2[a, b] = radial_int(n, l, n, lp, 2) * g
            M2 *= 0.125 * B2
            # Zeeman 对角项（m 守恒，全部 l 同值）
            for a in range(len(ls)):
                M2[a, a] += sgn * B_au / 2.0
            ev2, evc2 = np.linalg.eigh(M2)
            for a in range(len(ls)):
                amp = 0.0
                for b, l in enumerate(ls):
                    tot = 0.0
                    for l2, coeff in n2_states:
                        if abs(l2-l) == 1:
                            g = GSIG.get((l2, l), GSIG.get((l, l2), 0.0))
                            if abs(g) > 1e-12:
                                tot += coeff * radial_int(2, l2, n, l, 1) * g
                    amp += evc2[b, a] * tot
                f_sig.append((Eph + ev2[a], amp**2))
        all_f = f_pi + f_sig
        total = sum(f for _, f in all_f)
        s_win = sum(f for Ea, f in all_f if abs(Ea - Eph) < dE)
        # 能量分布结构：距线心最近分量
        dists = sorted([abs(Ea - Eph) for Ea, _ in all_f])
        out["lines"][str(n)] = {"s_win": float(s_win), "total": float(total),
                                "frac": float(s_win/total) if total > 1e-30 else 0.0,
                                "min_dist": float(dists[0]) if dists else None,
                                "frac_in_2dE": float(sum(f for Ea,f in all_f if abs(Ea-Eph)<2*dE)/total) if total>1e-30 else 0.0}
    return out

print("=== v7 联合对角化：π+σ S_win(n,B) ±80 Å ===", flush=True)
B_list = (0.0001, 0.005, 0.01, 0.02, 0.05)
results = []
for B in B_list:
    print("B=%.4f a.u. (%.1f MG)..." % (B, B*2350), flush=True)
    out = run(B)
    results.append(out)
    ln = out["lines"]
    print("  Hα %6.1f%% Hβ %6.1f%% Hγ %6.1f%% Hδ %6.1f%% Hε %6.1f%%" % (
        100*ln["3"]["frac"], 100*ln["4"]["frac"], 100*ln["5"]["frac"],
        100*ln["6"]["frac"], 100*ln["7"]["frac"]), flush=True)
    print("  min_dist(au): Hα %.5f Hβ %.5f Hγ %.5f Hδ %.5f Hε %.5f" % (
        ln["3"]["min_dist"], ln["4"]["min_dist"], ln["5"]["min_dist"],
        ln["6"]["min_dist"], ln["7"]["min_dist"]), flush=True)
    print("  frac_in_2dE:  Hα %.3f Hβ %.3f Hγ %.3f Hδ %.3f Hε %.3f" % (
        ln["3"]["frac_in_2dE"], ln["4"]["frac_in_2dE"], ln["5"]["frac_in_2dE"],
        ln["6"]["frac_in_2dE"], ln["7"]["frac_in_2dE"]), flush=True)

ref = results[0]
print("\n=== TRK 守恒（total/0.2MG）===", flush=True)
for res in results:
    line = "B=%6.1f MG |" % res["B_MG"]
    for n in (3,4,5,6,7):
        line += " %s %.4f" % ({3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ",7:"Hε"}[n],
                              res["lines"][str(n)]["total"]/ref["lines"][str(n)]["total"])
    print(line, flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_sigma_v7.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_osc_pi_sigma_v7.json")
