# -*- coding: utf-8 -*-
"""Phase 104az-61 v8：多流形联合对角化（跨 n 抗磁耦合——修正固定 n 流形近似）
- 全流形：n=2..8 全部 l 态——m=0 与 m=±1 子空间大矩阵
- 矩阵：抗磁 B²ρ²/8（跨 n 非对角）+ Zeeman ±B/2 对角（m 守恒）
- 初态：n=2 流形（2s/2p）在 B 场下的联合本征态
- 偶极矩阵元：<ψ_2|r|ψ_f>（全部末态）——π(m=0→0) + σ±(0→±1)
- S_win(n,B)：线心 ±80 Å 窗内份额——对比 v6/v7 固定 n 结果
- 输出：全线 S_win + 每线能量分布直方（准 Landau 分量结构——跨 n 混合的检验）
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

def radial_int(n, l, np_, lp, power, r_max=140.0, N=10000):
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

LMAX = 9
GC, GS, GSIG, GSM1 = {}, {}, {}, {}
for l1 in range(LMAX):
    for l2 in range(LMAX):
        if abs(l1-l2) == 1:
            GC[(l1,l2)] = gaunt_cos(l1, l2)
            GSIG[(l1,l2)] = gaunt_sigma(l1, l2)
        if abs(l1-l2) in (0, 2):
            GS[(l1,l2)] = gaunt_sin2(l1, l2)
            GSM1[(l1,l2)] = gaunt_sin2_m1(l1, l2)

print("=== v8 自检 ===", flush=True)
th, w = leggauss(96); th = np.arccos(th)
y00 = Ylm(0, 0, th)
print("∫|Y00|²(×2π):", np.sum(w*y00*y00)*2*np.pi, flush=True)
print("GC(0,1):", GC[(0,1)], " GSIG(0,1):", GSIG[(0,1)], flush=True)
print("<2s|r²|3d> 跨 n 径向:", radial_int(2,0,3,2,2), flush=True)

# 流形构建：n=2..NMAX 全部 l
NMAX = 8
STATES = []  # (n, l)
for n in range(2, NMAX+1):
    for l in range(n):
        STATES.append((n, l))
NS = len(STATES)
print("总态数:", NS, flush=True)
E0 = np.array([-0.5/n**2 for n, _ in STATES])

# 抗磁矩阵（m=0：l 任意；m=±1：l>=1）
def build(B_au, m):
    idx = [i for i, (n, l) in enumerate(STATES) if l >= abs(m)]
    M = np.zeros((len(idx), len(idx)))
    for a, i in enumerate(idx):
        n1, l1 = STATES[i]
        for b, j in enumerate(idx):
            n2, l2 = STATES[j]
            if abs(l1-l2) in (0, 2):
                g = GS.get((l1,l2), GS.get((l2,l1), 0.0)) if m == 0 else GSM1.get((l1,l2), GSM1.get((l2,l1), 0.0))
                if abs(g) > 1e-12:
                    M[a, b] = radial_int(n1, l1, n2, l2, 2) * g
    M *= 0.125 * B_au**2
    # Zeeman 对角（m 守恒）
    for a, i in enumerate(idx):
        M[a, a] += m * B_au / 2.0
    ev, evec = np.linalg.eigh(M)
    full_ev = np.zeros(NS); full_ev[:] = np.nan
    full_ev[idx] = ev
    full_vec = np.zeros((NS, len(idx)))
    full_vec[idx, :] = evec
    return idx, ev, evec, full_ev

# 初态：n=2 流形（m=0: 2s,2p；m=±1: 2p）场下本征态——偶极矩阵元
def dipole(B_au):
    # 末态 m 空间
    idx0, ev0, evc0, full_ev0 = build(B_au, 0)
    idx1, ev1, evc1, full_ev1 = build(B_au, 1)
    idxm1, evm1, evcm1, full_evm1 = build(B_au, -1)
    # 初态 n=2 流形态（m=0: 2s(l=0), 2p(l=1)）
    n2_idx0 = [i for i, (n, l) in enumerate(STATES) if n == 2 and l >= 0]
    # 初态在 B 场下的演化：只关心 n=2 流形内矩阵元（2s/2p 之间的抗磁耦合）
    M0 = np.zeros((len(n2_idx0), len(n2_idx0)))
    for a, i in enumerate(n2_idx0):
        n1, l1 = STATES[i]
        for b, j in enumerate(n2_idx0):
            n2, l2 = STATES[j]
            if abs(l1-l2) in (0, 2):
                g = GS.get((l1,l2), GS.get((l2,l1), 0.0))
                if abs(g) > 1e-12:
                    M0[a, b] = radial_int(n1, l1, n2, l2, 2) * g
    M0 *= 0.125 * B_au**2
    e0, v0 = np.linalg.eigh(M0)
    return idx0, ev0, evc0, full_ev0, idx1, ev1, evc1, full_ev1, idxm1, evm1, evcm1, full_evm1, n2_idx0, e0, v0

E2_0 = -1.0/8.0  # n=2 零场能量
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
W_ANG = 80.0

def run(B_au):
    (idx0, ev0, evc0, full_ev0, idx1, ev1, evc1, full_ev1,
     idxm1, evm1, evcm1, full_evm1, n2_idx0, e0, v0) = dipole(B_au)
    out = {"B_au": B_au, "B_MG": B_au*2350.0, "lines": {}}
    for n, (lam, Eph) in LINES.items():
        dE = Eph * 2.0*W_ANG / lam
        # 初态 n=2 本征态（2 个：2s/2p 混合）
        init_states = []
        for a in range(len(n2_idx0)):
            amp_i = np.zeros(NS)
            for b, i in enumerate(n2_idx0):
                amp_i[i] = v0[b, a]
            init_states.append((E2_0 + e0[a], amp_i))
        # π 通道：初态 m=0 → 末态 m=0
        f_pi = []
        for a0, (E_i, amp_i) in enumerate(init_states):
            for a in range(len(idx0)):
                i = idx0[a]
                nf, lf = STATES[i]
                if nf != n:
                    continue
                amp = 0.0
                for j, l in enumerate([0, 1]):  # 初态 2s/2p 分量（m=0）
                    # 初态 l 到末态 lf 的偶极
                    if abs(l-lf) == 1:
                        g = GC.get((l, lf), GC.get((lf, l), 0.0))
                        if abs(g) > 1e-12:
                            amp += amp_i[STATES.index((2, l))] * radial_int(2, l, nf, lf, 1) * g
                E_f = E2_0 + ev0[a]
                f_pi.append((E_f - E_i, amp**2))
        # σ+ 通道：末态 m=+1
        f_sigp = []
        for a0, (E_i, amp_i) in enumerate(init_states):
            for a in range(len(idx1)):
                i = idx1[a]
                nf, lf = STATES[i]
                if nf != n:
                    continue
                amp = 0.0
                for j, l in enumerate([1]):  # 初态 2p（m=0 → σ+ 需初态 m=0）
                    if abs(l-lf) == 1:
                        g = GSIG.get((l, lf), GSIG.get((lf, l), 0.0))
                        if abs(g) > 1e-12:
                            amp += amp_i[STATES.index((2, l))] * radial_int(2, l, nf, lf, 1) * g
                E_f = E2_0 + ev1[a]
                f_sigp.append((E_f - E_i, amp**2))
        # σ- 通道：末态 m=-1
        f_sigm = []
        for a0, (E_i, amp_i) in enumerate(init_states):
            for a in range(len(idxm1)):
                i = idxm1[a]
                nf, lf = STATES[i]
                if nf != n:
                    continue
                amp = 0.0
                for j, l in enumerate([1]):
                    if abs(l-lf) == 1:
                        g = GSIG.get((l, lf), GSIG.get((lf, l), 0.0))
                        if abs(g) > 1e-12:
                            amp += amp_i[STATES.index((2, l))] * radial_int(2, l, nf, lf, 1) * g
                E_f = E2_0 + evm1[a]
                f_sigm.append((E_f - E_i, amp**2))
        all_f = f_pi + f_sigp + f_sigm
        total = sum(f for _, f in all_f)
        s_win = sum(f for dEa, f in all_f if abs(dEa) < dE)
        dists = sorted([abs(dEa) for dEa, _ in all_f])
        # 近线心份额（±2dE）与能量分布特征
        frac_2 = sum(f for dEa, f in all_f if abs(dEa) < 2*dE)/total if total > 1e-30 else 0.0
        # 分量数（强度 > 1% total）
        ncomp = sum(1 for _, f in all_f if f > 0.01*total) if total > 1e-30 else 0
        out["lines"][str(n)] = {"s_win": float(s_win), "total": float(total),
                                "frac": float(s_win/total) if total > 1e-30 else 0.0,
                                "frac_in_2dE": float(frac_2), "n_comp": int(ncomp),
                                "min_dist": float(dists[0]) if dists else None,
                                "n_pi": len(f_pi), "n_sig": len(f_sigp)+len(f_sigm)}
    return out

print("=== v8 多流形联合对角化：S_win(n,B) ±80 Å ===", flush=True)
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
    print("  n_comp:   Hα %d Hβ %d Hγ %d Hδ %d Hε %d" % (
        ln["3"]["n_comp"], ln["4"]["n_comp"], ln["5"]["n_comp"],
        ln["6"]["n_comp"], ln["7"]["n_comp"]), flush=True)
    print("  min_dist: Hα %.5f Hβ %.5f Hγ %.5f Hδ %.5f Hε %.5f" % (
        ln["3"]["min_dist"], ln["4"]["min_dist"], ln["5"]["min_dist"],
        ln["6"]["min_dist"], ln["7"]["min_dist"]), flush=True)

ref = results[0]
print("\n=== TRK 守恒（total/0.2MG）===", flush=True)
for res in results:
    line = "B=%6.1f MG |" % res["B_MG"]
    for n in (3,4,5,6,7):
        line += " %s %.4f" % ({3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ",7:"Hε"}[n],
                              res["lines"][str(n)]["total"]/ref["lines"][str(n)]["total"])
    print(line, flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_sigma_v8.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_osc_pi_sigma_v8.json")
