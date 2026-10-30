# -*- coding: utf-8 -*-
"""Phase 104az-63 v9b：盘面平均（优化版——径向积分预计算缓存）
- 径向积分 <nl|r²|n'l'>、<2l|r|n'l'> 与 B 无关——预计算一次
- 每表面点：只组装矩阵 + 对角化（快）
- 偶极场：|B(θ_p)| = B_d·√(1+3cos²θ_p)/2；B_z = B·(B̂·n̂)——抗磁 ∝|B|²、Zeeman ∝B_z
- 权重 cosγ（可见面）——S_win_disk(n, B_d, i)
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

print("=== v9b 自检 ===", flush=True)
th, w = leggauss(96); th = np.arccos(th)
y00 = Ylm(0, 0, th)
print("∫|Y00|²(×2π):", np.sum(w*y00*y00)*2*np.pi, flush=True)

NMAX = 8
STATES = [(n, l) for n in range(2, NMAX+1) for l in range(n)]
NS = len(STATES)

# ---- 预计算（与 B 无关）----
print("预计算径向积分...", flush=True)
R2 = np.zeros((NS, NS))   # <nl|r²|n'l'>
DIP = np.zeros((NS, NS))  # <2,l|r|n,l'>（初态 n=2 到任意末态）——按 (初态 idx, 末态 idx) 存
for i, (n1, l1) in enumerate(STATES):
    for j, (n2, l2) in enumerate(STATES):
        if abs(l1-l2) in (0, 2):
            g = GS.get((l1,l2), GS.get((l2,l1), 0.0)) if True else 0.0
            # r² 矩阵元：Gaunt sin²θ（m=0 用 GS）——含角向因子
            R2[i, j] = radial_int(n1, l1, n2, l2, 2) * g
        if n1 == 2 and abs(l1-l2) == 1:
            g = GC.get((l1, l2), GC.get((l2, l1), 0.0))
            DIP[i, j] = radial_int(2, l1, n2, l2, 1) * g
R2m1 = np.zeros((NS, NS))   # <nl|r²|n'l'> m=+1（sin²θ 用 GSM1）
DIPsig = np.zeros((NS, NS)) # <2,1|r|n,l'> σ（σ+ 初态 2p m=0 → 末态 m=+1）
for i, (n1, l1) in enumerate(STATES):
    for j, (n2, l2) in enumerate(STATES):
        if l1 >= 1 and l2 >= 1 and abs(l1-l2) in (0, 2):
            g = GSM1.get((l1,l2), GSM1.get((l2,l1), 0.0))
            R2m1[i, j] = radial_int(n1, l1, n2, l2, 2) * g
        if n1 == 2 and abs(l1-l2) == 1:
            g = GSIG.get((l1, l2), GSIG.get((l2, l1), 0.0))
            DIPsig[i, j] = radial_int(2, l1, n2, l2, 1) * g
print("预计算完成。", flush=True)

# 初态 n=2 抗磁（m=0，含 2s/2p）
N2 = [i for i, (n, l) in enumerate(STATES) if n == 2]
M0base = np.zeros((len(N2), len(N2)))
for a, i in enumerate(N2):
    for b, j in enumerate(N2):
        M0base[a, b] = R2[i, j]
print("初态 n=2 流形:", [(n, l) for n, l in STATES if n == 2], flush=True)

E2_0 = -1.0/8.0
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
W_ANG = 80.0
# 预计算各线末态索引（每 n 的态）
LIN_IDX = {}
for n in LINES:
    LIN_IDX[n] = [i for i, (nn, l) in enumerate(STATES) if nn == n]

def s_win_local_fast(B_amp, B_z):
    """B_amp: 抗磁（|B|）；B_z: Zeeman 纵向（视向投影）"""
    # m=0 子空间（π + 初态）
    idx0 = [i for i, (n, l) in enumerate(STATES) if l >= 0]
    M0f = np.zeros((NS, NS))
    for i in range(NS):
        for j in range(NS):
            M0f[i, j] = R2[i, j]
    M0f *= 0.125 * B_amp**2
    # 初态（n=2）
    M0g = np.zeros((len(N2), len(N2)))
    for a, i in enumerate(N2):
        for b, j in enumerate(N2):
            M0g[a, b] = M0f[i, j]
    e0, v0 = np.linalg.eigh(M0g)
    init_states = [(E2_0 + e0[a], v0[:, a]) for a in range(len(N2))]
    # 末态 m=0：全 NS 流形（含初态）
    ev0, evc0 = np.linalg.eigh(M0f)
    # m=+1 子空间
    idx1 = [i for i, (n, l) in enumerate(STATES) if l >= 1]
    M1f = np.zeros((NS, NS))
    for i in range(NS):
        for j in range(NS):
            M1f[i, j] = R2m1[i, j]
    M1f *= 0.125 * B_amp**2
    for i in idx1:
        M1f[i, i] += B_z / 2.0
    ev1, evc1 = np.linalg.eigh(M1f)
    # m=-1
    M_1f = M1f.copy()
    for i in idx1:
        M_1f[i, i] -= B_z
    M_1f += 0.0  # 已在上面加 B_z/2，这里减 B_z → 净 -B_z/2
    for i in idx1:
        M_1f[i, i] = M1f[i, i] - B_z
    evm1, evcm1 = np.linalg.eigh(M_1f)
    out = {}
    for n, (lam, Eph) in LINES.items():
        dE = Eph * 2.0*W_ANG / lam
        all_f = []
        for a0, (E_i, amp_i) in enumerate(init_states):
            for i in LIN_IDX[n]:
                nf, lf = STATES[i]
                # π：初态 l=0,1 → 末态 l±1
                amp = 0.0
                for ja, j in enumerate(N2):
                    l0 = STATES[j][1]
                    if abs(l0-lf) == 1 and abs(DIP[j, i]) > 1e-12:
                        amp += amp_i[ja] * DIP[j, i]
                all_f.append((E2_0 + ev0[i] - E_i, amp**2))
                # σ+：初态 n=2（2s/2p 混合，m=0）→ 末态 m=+1
                amp_s = 0.0
                for ja, j in enumerate(N2):
                    l0 = STATES[j][1]
                    if abs(l0-lf) == 1 and abs(DIPsig[j, i]) > 1e-12:
                        amp_s += amp_i[ja] * DIPsig[j, i]
                all_f.append((E2_0 + ev1[i] - E_i, amp_s**2))
                # σ-：同 σ+ 矩阵元、m=-1 能量
                all_f.append((E2_0 + evm1[i] - E_i, amp_s**2))
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
    for at in range(Nt):
        thp = np.pi*(at+0.5)/Nt
        cost = np.cos(thp); sint = np.sin(thp)
        B_amp = B_d_au * np.sqrt(1.0 + 3.0*cost**2) / 2.0
        for ap in range(Np):
            php = 2*np.pi*(ap+0.5)/Np
            cosp = np.cos(php)
            cosg = sint*cosp*nx + cost*nz
            if cosg <= 0: continue
            bdn = (3.0*cost*cosg - nz) / np.sqrt(1.0 + 3.0*cost**2)
            B_z = B_amp * bdn
            w = cosg
            sw = s_win_local_fast(B_amp, B_z)
            for n in LINES:
                num[n] += w * sw[n]
                den[n] += w
    return {n: num[n]/den[n] if den[n] > 0 else 0.0 for n in LINES}

print("=== v9b 盘面平均：S_win_disk(n, B_d, i) ±80 Å ===", flush=True)
for B_d_au in (0.005, 0.01, 0.02):
    B_MG = B_d_au*2350
    print("\n--- B_d = %.1f MG ---" % B_MG, flush=True)
    sp = s_win_local_fast(B_d_au, B_d_au)
    print("单点(B_z=B_d): Hα %5.1f Hβ %5.1f Hγ %5.1f Hδ %5.1f Hε %5.1f %%" % (
        100*sp[3], 100*sp[4], 100*sp[5], 100*sp[6], 100*sp[7]), flush=True)
    for i_deg in (0, 30, 60, 90):
        avg = disk_average(B_d_au, i_deg)
        print("盘面 i=%2d°: Hα %5.1f Hβ %5.1f Hγ %5.1f Hδ %5.1f Hε %5.1f %%" % (
            i_deg, 100*avg[3], 100*avg[4], 100*avg[5], 100*avg[6], 100*avg[7]), flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_sigma_v9_disk.json"), "w", encoding="utf-8") as f:
    json.dump({"note": "S_win_disk(B_d,i)——out 见 .out"}, f)
print("\ndone")
