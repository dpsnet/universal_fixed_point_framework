# -*- coding: utf-8 -*-
"""Phase 104az-62 v9：盘面平均（偶极场 B_d + 倾角 i + 视向投影）——A 路线第一步完整版
- 每表面点：抗磁 ∝ |B(θ_p)|²（偶极场幅值）、Zeeman ∝ B_z（视向投影）
- 权重：可见面投影面积 cosγ（γ = 表面法线与视线夹角）
- S_win_disk(n, B_d, i) = Σ w·S_win_local(n, B(θ_p), B_z(θ_p,φ_p,i)) / Σw
- 输出：全线盘面平均保留份额 vs 单点对比——同口径（±80 Å）
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

print("=== v9 自检 ===", flush=True)
th, w = leggauss(96); th = np.arccos(th)
y00 = Ylm(0, 0, th)
print("∫|Y00|²(×2π):", np.sum(w*y00*y00)*2*np.pi, flush=True)
print("GC(0,1):", GC[(0,1)], " GSIG(0,1):", GSIG[(0,1)], flush=True)

NMAX = 8
STATES = [(n, l) for n in range(2, NMAX+1) for l in range(n)]
NS = len(STATES)
print("总态数:", NS, flush=True)

def build(B_amp, B_z, m):
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
    M *= 0.125 * B_amp**2
    for a, i in enumerate(idx):
        M[a, a] += m * B_z / 2.0
    ev, evec = np.linalg.eigh(M)
    full_ev = np.full(NS, np.nan)
    full_ev[idx] = ev
    return idx, ev, evec, full_ev

E2_0 = -1.0/8.0
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
W_ANG = 80.0

def s_win_local(B_amp, B_z):
    idx0, ev0, evc0, _ = build(B_amp, B_z, 0)
    idx1, ev1, evc1, _ = build(B_amp, B_z, 1)
    idxm1, evm1, evcm1, _ = build(B_amp, B_z, -1)
    # 初态 n=2 流形（m=0: 2s/2p）
    n2_idx0 = [i for i, (n, l) in enumerate(STATES) if n == 2]
    M0 = np.zeros((len(n2_idx0), len(n2_idx0)))
    for a, i in enumerate(n2_idx0):
        n1, l1 = STATES[i]
        for b, j in enumerate(n2_idx0):
            n2, l2 = STATES[j]
            if abs(l1-l2) in (0, 2):
                g = GS.get((l1,l2), GS.get((l2,l1), 0.0))
                if abs(g) > 1e-12:
                    M0[a, b] = radial_int(n1, l1, n2, l2, 2) * g
    M0 *= 0.125 * B_amp**2
    for a, i in enumerate(n2_idx0):
        M0[a, a] += 0.0  # 初态 m=0 无 Zeeman
    e0, v0 = np.linalg.eigh(M0)
    init_states = [(E2_0 + e0[a], v0[:, a]) for a in range(len(n2_idx0))]
    out = {}
    for n, (lam, Eph) in LINES.items():
        dE = Eph * 2.0*W_ANG / lam
        all_f = []
        for a0, (E_i, amp_i) in enumerate(init_states):
            for a in range(len(idx0)):
                i = idx0[a]
                nf, lf = STATES[i]
                if nf != n: continue
                amp = 0.0
                for j, l in enumerate([0, 1]):
                    if abs(l-lf) == 1:
                        g = GC.get((l, lf), GC.get((lf, l), 0.0))
                        if abs(g) > 1e-12:
                            amp += amp_i[STATES.index((2, l))] * radial_int(2, l, nf, lf, 1) * g
                all_f.append((E2_0 + ev0[a] - E_i, amp**2))
        for a0, (E_i, amp_i) in enumerate(init_states):
            for a in range(len(idx1)):
                i = idx1[a]
                nf, lf = STATES[i]
                if nf != n: continue
                amp = 0.0
                for j, l in enumerate([1]):
                    if abs(l-lf) == 1:
                        g = GSIG.get((l, lf), GSIG.get((lf, l), 0.0))
                        if abs(g) > 1e-12:
                            amp += amp_i[STATES.index((2, l))] * radial_int(2, l, nf, lf, 1) * g
                all_f.append((E2_0 + ev1[a] - E_i, amp**2))
        for a0, (E_i, amp_i) in enumerate(init_states):
            for a in range(len(idxm1)):
                i = idxm1[a]
                nf, lf = STATES[i]
                if nf != n: continue
                amp = 0.0
                for j, l in enumerate([1]):
                    if abs(l-lf) == 1:
                        g = GSIG.get((l, lf), GSIG.get((lf, l), 0.0))
                        if abs(g) > 1e-12:
                            amp += amp_i[STATES.index((2, l))] * radial_int(2, l, nf, lf, 1) * g
                all_f.append((E2_0 + evm1[a] - E_i, amp**2))
        total = sum(f for _, f in all_f)
        s_win = sum(f for dEa, f in all_f if abs(dEa) < dE)
        out[n] = s_win/total if total > 1e-30 else 0.0
    return out

def disk_average(B_d_au, i_deg):
    i = np.radians(i_deg)
    nz = np.cos(i); nx = np.sin(i)
    Nt, Np = 20, 40
    num, den = {}, {}
    for n in LINES:
        num[n] = 0.0; den[n] = 0.0
    Wsum = 0.0
    for at in range(Nt):
        thp = np.pi*(at+0.5)/Nt
        cost = np.cos(thp); sint = np.sin(thp)
        B_amp = B_d_au * np.sqrt(1.0 + 3.0*cost**2) / 2.0
        # B̂·n̂ = (3cosθ_p cosγ − cos i)/√(1+3cos²θ_p)
        for ap in range(Np):
            php = 2*np.pi*(ap+0.5)/Np
            cosp = np.cos(php); sinp = np.sin(php)
            # 表面法线 r̂·n̂ = cosγ
            cosg = sint*cosp*nx + cost*nz
            if cosg <= 0: continue
            # B̂·n̂
            bdn = (3.0*cost*cosg - nz) / np.sqrt(1.0 + 3.0*cost**2)
            B_z = B_amp * bdn
            w = cosg
            Wsum += w
            sw = s_win_local(B_amp, B_z)
            for n in LINES:
                num[n] += w * sw[n]
                den[n] += w
    return {n: num[n]/den[n] if den[n] > 0 else 0.0 for n in LINES}, Wsum

print("=== v9 盘面平均：S_win_disk(n, B_d, i) ±80 Å ===", flush=True)
# 预计算单点对照（i=0 无投影、B_z=B 的情形≈v8）
for B_d_au in (0.005, 0.01, 0.02):
    B_MG = B_d_au*2350
    print("\n--- B_d = %.1f MG ---" % B_MG, flush=True)
    # 单点（B_z = B_d 全投影——纵向场极限）
    sp = s_win_local(B_d_au, B_d_au)
    print("单点(B_z=B_d): Hα %5.1f Hβ %5.1f Hγ %5.1f Hδ %5.1f Hε %5.1f %%" % (
        100*sp[3], 100*sp[4], 100*sp[5], 100*sp[6], 100*sp[7]), flush=True)
    for i_deg in (0, 30, 60, 90):
        avg, Wsum = disk_average(B_d_au, i_deg)
        print("盘面 i=%2d°: Hα %5.1f Hβ %5.1f Hγ %5.1f Hδ %5.1f Hε %5.1f %% (Σw=%.1f)" % (
            i_deg, 100*avg[3], 100*avg[4], 100*avg[5], 100*avg[6], 100*avg[7], Wsum), flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_sigma_v9_disk.json"), "w", encoding="utf-8") as f:
    json.dump({"note": "S_win_disk(B_d, i) 盘面平均——见 .out"}, f)
print("\ndone")
