# -*- coding: utf-8 -*-
# _v04_open239d_hbetagamma_pi_v4.py — 104az-239: Hβ π 分量二次位移精确核算 v4
# v4 修正: 零场能差用 a.u. 相减 (与 235/238 一致), 归属用主成分 argmax + 正能量剔除
# 门: Hα 交叉验证 (238: 236.572@100, 861.057@200 cm⁻¹)
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, lpmv, factorial

B0 = 2.3505e9
R_INF = 109737.315685
LAM_HA = 6562.79
LAM_HB = 4861.33

def basis(nmax):
    return [(n, l, m) for n in range(1, nmax + 1) for l in range(n) for m in range(-l, l + 1)]

def R_nl(n, l, r):
    rho = 2.0 * r / n
    norm = np.sqrt((2.0 / n) ** 3 * factorial(n - l - 1) / (2.0 * n * factorial(n + l)))
    return norm * np.exp(-r / n) * (2.0 * r / n) ** l * genlaguerre(n - l - 1, 2 * l + 1)(rho)

def r2_int(n, l, np_, r_max=140.0, N=400):
    x, w = leggauss(N)
    r = 0.5 * r_max * (x + 1.0)
    f = R_nl(n, l, r) * R_nl(np_, l, r) * r ** 4
    return float(0.5 * r_max * np.sum(w * f))

def ang_sin2(l1, m1, l2, m2, Nth=128):
    if m1 != m2:
        return 0.0
    x, w = leggauss(Nth)
    th = np.arccos(x)
    P1 = lpmv(abs(m1), l1, np.cos(th))
    P2 = lpmv(abs(m2), l2, np.cos(th))
    n1 = np.sqrt((2 * l1 + 1) / (4 * np.pi) * factorial(l1 - abs(m1)) / factorial(l1 + abs(m1)))
    n2 = np.sqrt((2 * l2 + 1) / (4 * np.pi) * factorial(l2 - abs(m2)) / factorial(l2 + abs(m2)))
    cs1 = (-1.0) ** m1 if m1 >= 0 else 1.0
    cs2 = (-1.0) ** m2 if m2 >= 0 else 1.0
    Y1 = cs1 * n1 * P1
    Y2 = cs2 * n2 * P2
    return float(np.sum(w * Y1 * Y2 * (1.0 - x ** 2)))

def diag(B_MG, nmax=4, with_diamag=True):
    gamma = B_MG * 1e6 / B0
    out = {}
    for ms in (0.5, -0.5):
        ST = basis(nmax)
        NS = len(ST)
        H = np.zeros((NS, NS))
        for i, (n, l, m) in enumerate(ST):
            H[i, i] = -0.5 / n ** 2 + 0.5 * gamma * (m + 2 * ms)
        if with_diamag:
            for i, (n1, l1, m1) in enumerate(ST):
                for j, (n2, l2, m2) in enumerate(ST):
                    if m1 != m2 or l1 != l2:
                        continue
                    a = ang_sin2(l1, m1, l2, m2)
                    if abs(a) < 1e-12:
                        continue
                    H[i, j] += (gamma ** 2 / 8.0) * r2_int(n1, l1, n2) * a
        E, V = np.linalg.eigh(H)
        info = []
        for k in range(NS):
            if E[k] > 0:
                continue
            Lz = sum(V[i, k] ** 2 * ST[i][2] for i in range(NS))
            comp = {}
            for i, (n, l, m) in enumerate(ST):
                comp[n] = comp.get(n, 0.0) + V[i, k] ** 2
            nstar = max(comp, key=comp.get)
            info.append((E[k], Lz, nstar, comp[nstar]))
        out[ms] = info
    return out

def line_pi(B_MG, nu, nd, lam0, nmax=4):
    di = diag(B_MG, nmax=nmax, with_diamag=True)
    dE0 = (-0.5 / nu ** 2) - (-0.5 / nd ** 2)   # a.u. 零场能差
    pis = []
    for ms in (0.5, -0.5):
        up = [k for k, (E, Lz, ns, f) in enumerate(di[ms]) if ns == nu]
        dn = [k for k, (E, Lz, ns, f) in enumerate(di[ms]) if ns == nd]
        for ku in up:
            for kd in dn:
                dlz = di[ms][ku][1] - di[ms][kd][1]
                if abs(dlz) > 0.5:
                    continue
                dE = (di[ms][ku][0] - di[ms][kd][0] - dE0) * 2 * R_INF   # cm⁻¹
                pis.append(dE)
    return sorted(pis)

print("=== 104az-239 v4: Hβ π 位移精确核算 (n=1..4, a.u. 零场差) ===")
print()
print("--- 门: Hα 交叉验证 (238: 236.572@100, 861.057@200 cm⁻¹) ---")
ok = True
for B, expect in ((100, 236.572), (200, 861.057)):
    pis = line_pi(B, 3, 2, LAM_HA)
    inner = min(pis, key=abs) if pis else None
    match = inner is not None and abs(inner - expect) < 5.0
    ok = ok and match
    print(f"  Hα @{B:>5} MG: 最内层 π = {inner if inner is None else round(inner,3)} cm⁻¹ (期望 {expect}) {'✓' if match else '✗'}")
if not ok:
    print("!! 交叉验证失败")
    raise SystemExit(1)
print("  交叉验证通过 ✓")
print()
print(f"{'B(MG)':>7} | Hβ π 内层 cm⁻¹ | Å | 位置Å | Hβ π 分量数 | 全列表(前 10)")
for B in (20, 50, 100, 120, 150, 180, 200, 220.78):
    pis = line_pi(B, 4, 2, LAM_HB)
    if not pis:
        print(f"{B:>7} | (无)") 
        continue
    inner = min(pis, key=abs)
    dlam = inner * LAM_HB ** 2 / 1e8
    pos = LAM_HB + dlam
    lst = " ".join(f"{x:+.0f}" for x in pis[:10])
    print(f"{B:>7} | {inner:>+11.1f} {dlam:>7.1f} {pos:>7.0f} | {len(pis):>8} | {lst}")
print()
print("--- 指数拟合 (Hβ 最内层 π) ---")
pts = {}
for B in (20, 50, 100, 150, 200):
    pis = line_pi(B, 4, 2, LAM_HB)
    if pis:
        pts[B] = min(pis, key=abs)
for (B1, B2) in ((100, 200), (50, 200), (20, 200)):
    if B1 in pts and B2 in pts:
        e = np.log(pts[B2] / pts[B1]) / np.log(B2 / B1)
        print(f"  {B1}→{B2} MG: 指数 = {e:.3f}  (238 判据①修订带 [1.85,2.0])")
print()
print("--- 蓝窗覆盖 (G227-35 ISIS R600B 3650-5300 Å) ---")
for B in (120, 150, 180):
    pis = line_pi(B, 4, 2, LAM_HB)
    if pis:
        inner = min(pis, key=abs)
        dlam = inner * LAM_HB ** 2 / 1e8
        pos = LAM_HB + dlam
        print(f"  Hβ π @{B} MG: 位置 {pos:.0f} Å -> {'✓ 窗内' if 3650 <= pos <= 5300 else '✗ 窗外'} (位移 {dlam:+.0f} Å)")
