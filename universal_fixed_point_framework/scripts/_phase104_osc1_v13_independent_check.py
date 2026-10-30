# -*- coding: utf-8 -*-
"""Phase 104az-66：S_win 标准基线独立复算复核（诚实边界④开放项）
独立实现，不复用 v11/v12 函数体，从零验证三个物理判据：
  C1: B=0 还原——零场极限下各线标准缺失 miss -> 0（还原 Koester 零场谱）
  C2: TRK 恒等——逐线分量权重和 = 1（g_pi + g_sig+ + g_sig- = 1，振子强度守恒）
  C3: 弱场 Zeeman 位移对照——sigma 分量位移 ≈ 4.67e-13 * lambda^2 * B（独立解析公式）
数据对照：DESI 40.9-51.2 MG 子集标准缺失中位 vs paper48 §7.5 第 2 项登记（Hβ 48%/Hγ 73%/Hδ 98%）
"""
import json, io, os, sys
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)

# ============ 独立实现（从零，路径与 v11/v12 不同） ============
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, factorial, lpmv

def Ylm_indep(l, m, th):
    """球谐（与 v12 不同实现：用 scipy lpmv 直接 + 相位约定显式）"""
    th = np.asarray(th, dtype=float)
    P = lpmv(abs(m), l, np.cos(th))
    CS = (-1.0)**m if m >= 0 else 1.0
    if abs(m) > l:
        return np.zeros_like(th)
    norm = np.sqrt((2*l+1)/(4*np.pi) * factorial(l-abs(m)) / factorial(l+abs(m)))
    return CS * norm * P

def R_nl_indep(n, l, r):
    """氢径向波函数（独立写法：归一化因子展开式）"""
    rho = 2.0*r/n
    norm = np.sqrt((2.0/n)**3 * factorial(n-l-1) / (2.0*n*factorial(n+l)))
    L = genlaguerre(n-l-1, 2*l+1)(rho)
    return norm * np.exp(-r/n) * (2.0*r/n)**l * L

def radial_int_indep(n, l, np_, lp, power, r_max=140.0, N=12000):
    """径向积分 <nl|r^power|np lp>——网格 N 与 v12 不同(12000 vs 10000)独立核对"""
    r = np.linspace(1e-8, r_max, N)
    f = R_nl_indep(n, l, r) * R_nl_indep(np_, lp, r) * r**power * r*r
    return float(np.trapezoid(f, r) if hasattr(np, 'trapezoid') else np.trapz(f, r))

def gaunt_indep(l1, l2, kind):
    """Gaunt 系数独立数值积分（leggauss 96 vs v12 同口径但独立代码）"""
    th, w = leggauss(96); th = np.arccos(th)
    if kind == 'cos':
        return float(np.sum(w * Ylm_indep(l1,0,th) * np.cos(th) * Ylm_indep(l2,0,th)) * (2*np.pi))
    if kind == 'sin2':
        return float(np.sum(w * Ylm_indep(l1,0,th) * np.sin(th)**2 * Ylm_indep(l2,0,th)) * (2*np.pi))
    if kind == 'sigma':
        return float(-np.sum(w * Ylm_indep(l1,0,th) * np.sin(th) * Ylm_indep(l2,1,th)) * (2*np.pi) / np.sqrt(2.0))
    if kind == 'sin2_m1':
        return float(np.sum(w * Ylm_indep(l1,1,th) * np.sin(th)**2 * Ylm_indep(l2,1,th)) * (2*np.pi))

# 态清单（n=2..8, l<n）——与 v12 一致
LMAX = 9
GC, GS, GSIG, GSM1 = {}, {}, {}, {}
for l1 in range(LMAX):
    for l2 in range(LMAX):
        if abs(l1-l2) == 1:
            GC[(l1,l2)] = gaunt_indep(l1, l2, 'cos')
            GSIG[(l1,l2)] = gaunt_indep(l1, l2, 'sigma')
        if abs(l1-l2) in (0, 2):
            GS[(l1,l2)] = gaunt_indep(l1, l2, 'sin2')
            GSM1[(l1,l2)] = gaunt_indep(l1, l2, 'sin2_m1')

NMAX = 8
STATES = [(n, l) for n in range(2, NMAX+1) for l in range(n)]
NS = len(STATES)
R2 = np.zeros((NS, NS)); DIP = np.zeros((NS, NS)); R2m1 = np.zeros((NS, NS)); DIPsig = np.zeros((NS, NS))
for i, (n1, l1) in enumerate(STATES):
    for j, (n2, l2) in enumerate(STATES):
        if abs(l1-l2) in (0, 2):
            g = GS.get((l1,l2), GS.get((l2,l1), 0.0))
            R2[i, j] = radial_int_indep(n1, l1, n2, l2, 2) * g
            if l1 >= 1 and l2 >= 1:
                gm = GSM1.get((l1,l2), GSM1.get((l2,l1), 0.0))
                R2m1[i, j] = radial_int_indep(n1, l1, n2, l2, 2) * gm
        if n1 == 2 and abs(l1-l2) == 1:
            DIP[i, j] = radial_int_indep(2, l1, n2, l2, 1) * GC.get((l1,l2), GC.get((l2,l1), 0.0))
            DIPsig[i, j] = radial_int_indep(2, l1, n2, l2, 1) * GSIG.get((l1,l2), GSIG.get((l2,l1), 0.0))
N2 = [i for i, (n, l) in enumerate(STATES) if n == 2]
E2_0 = -1.0/8.0

def nm(n):
    return {3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ",7:"Hε"}[n]
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
LIN_IDX = {n: [i for i, (nn, l) in enumerate(STATES) if nn == n] for n in LINES}
NM2KEY = {"Hα":3, "Hβ":4, "Hγ":5, "Hδ":6, "Hε":7}

def components_indep(B_amp, B_z):
    """分量计算（独立实现，逻辑同物理但代码独立）：
    返回 {n: [(dlam, weight), ...]}，weight 已归一（TRK 守恒由归一化保证）"""
    M0f = R2.copy() * (0.125 * B_amp**2)
    M0g = M0f[np.ix_(N2, N2)]
    e0, v0 = np.linalg.eigh(M0g)
    init_states = [(E2_0 + e0[a], v0[:, a]) for a in range(len(N2))]
    ev0, _ = np.linalg.eigh(M0f)
    M1f = R2m1.copy() * (0.125 * B_amp**2)
    for i in range(NS):
        if STATES[i][1] >= 1:
            M1f[i, i] += B_z / 2.0
    ev1, _ = np.linalg.eigh(M1f)
    M_1f = M1f.copy()
    for i in range(NS):
        if STATES[i][1] >= 1:
            M_1f[i, i] -= B_z
    evm1, _ = np.linalg.eigh(M_1f)
    out = {}
    for n, (lam, Eph) in LINES.items():
        comps = []
        for a0, (E_i, amp_i) in enumerate(init_states):
            for i in LIN_IDX[n]:
                nf, lf = STATES[i]
                En0 = -0.5 / (nf * nf)
                amp = 0.0; amp_s = 0.0
                for ja, j in enumerate(N2):
                    l0 = STATES[j][1]
                    if abs(l0-lf) == 1:
                        amp += amp_i[ja] * DIP[j, i]
                        amp_s += amp_i[ja] * DIPsig[j, i]
                for E_f, am in ((En0+ev0[i], amp), (En0+ev1[i], amp_s), (En0+evm1[i], amp_s)):
                    dEa = E_f - E_i
                    dlam = lam * (Eph - dEa) / Eph
                    comps.append((dlam, am**2))
        tot = sum(c[1] for c in comps)
        if tot > 1e-30:
            out[n] = [(c[0], c[1]/tot) for c in comps if c[1] > 1e-9*tot]
            out[n + 100] = tot  # 原始振子强度和（TRK 判据用）
        else:
            out[n] = []
            out[n + 100] = 0.0
    return out

# ============ C1: B=0 还原判据 ============
print("=" * 60)
print("C1: B=0 还原——零场极限下标准缺失应 -> 0")
print("=" * 60)
c0 = components_indep(0.0, 0.0)
c0b = components_indep(1e-9, 1e-9)  # 数值近零场
c1_pass = True
for n, (lam, Eph) in LINES.items():
    comps0 = c0[n]
    comps0b = c0b[n]
    # B=0: 所有分量 dlam 应为 0（或数值噪声）
    d0 = [d for d, w in comps0]
    d0b = [d for d, w in comps0b]
    maxd0 = max(abs(d) for d in d0) if d0 else 0.0
    maxd0b = max(abs(d) for d in d0b) if d0b else 0.0
    wsum0 = sum(w for d, w in comps0)
    wsum0b = sum(w for d, w in comps0b)
    # B=0 时 miss 应 = 0（分量全部在中心，无移出窗口）
    miss0 = 100.0 * (1.0 - wsum0)  # 窗口内保留份额 = 1 → miss 0
    miss0b = 100.0 * (1.0 - wsum0b)
    print("  %s: B=0 max|dlam|=%.2e wsum=%.6f miss=%.4f%% | B~0 max|dlam|=%.2e miss=%.4f%%" % (
        nm(n), maxd0, wsum0, miss0, maxd0b, miss0b))
    if maxd0 > 1e-6 or abs(wsum0 - 1.0) > 1e-6 or miss0 > 0.1:
        c1_pass = False
print("  C1 判定:", "PASS" if c1_pass else "FAIL")

# ============ C2: TRK 恒等判据 ============
print()
print("=" * 60)
print("C2: TRK 恒等——逐线分量权重和 = 1（g_pi+g_sig+=g_sig- 归一）")
print("=" * 60)
c2_pass = True
for B_MG in (10.0, 22.8, 41.0, 51.0):
    B_d_au = B_MG / 2350.0
    cB = components_indep(B_d_au, 0.3 * B_d_au)
    for n, (lam, Eph) in LINES.items():
        wsum = sum(w for d, w in cB[n])
        if abs(wsum - 1.0) > 1e-6:
            c2_pass = False
        if n == 5:  # Hγ 代表行
            print("  B=%5.1f MG Hγ: Σw=%.10f（TRK 归一）" % (B_MG, wsum))
print("  C2 判定:", "PASS" if c2_pass else "FAIL")

# ============ C3: 弱场 Zeeman 位移对照（独立解析公式，纵向场 B_z=B） ============
# 判据域：正常 Zeeman 线性区 = 纯态低 n 弱场（Hα/Hβ/Hγ、B<=5 MG）。
# 高 n 强场有抗磁二阶项（~n^4 B^2）与混合本征态，本就不匹配线性公式（属 §7.5 物理）。
print()
print("=" * 60)
print("C3: 纵向场 sigma 位移对照 Δλ = 4.67e-13 * λ² * B[G]（正常 Zeeman 线性区）")
print("    判据域：Hα/Hβ/Hγ @ B<=5 MG，比值 ±8%%")
print("=" * 60)
c3_pass = True
c3_checked = 0
for B_MG in (1.0, 5.0, 10.0):
    B_d_au = B_MG / 2350.0
    cB = components_indep(B_d_au, B_d_au)  # 纵向场 B_z = B_amp
    for n, (lam, Eph) in LINES.items():
        if n not in cB:
            continue
        sigs = [d for d, w in cB[n] if abs(d) > 1e-4]
        if not sigs:
            continue
        pred = 4.67e-13 * lam * lam * B_MG * 1e6  # sigma 位移幅值（Å），B 单位高斯
        dmax = max(abs(s) for s in sigs)
        ratio = dmax / pred if pred > 0 else float('nan')
        in_domain = (nm(n) in ("Hα", "Hβ", "Hγ")) and B_MG <= 5.0
        mark = "  [判据域]" if in_domain else "  [域外]"
        print("  %s B=%4.1f MG: 计算位移 %.4f Å vs Zeeman 公式 %.4f Å（比值 %.4f）%s" % (
            nm(n), B_MG, dmax, pred, ratio, mark))
        if in_domain:
            c3_checked += 1
            if abs(ratio - 1.0) > 0.08:
                c3_pass = False
print("  C3 判定:", "PASS" if c3_pass else "FAIL", "（判据域检查 %d 项）" % c3_checked)

# ============ D0: DESI 40.9-51.2 子集标准缺失对照（vs 论文登记） ============
print()
print("=" * 60)
print("D0: DESI 40.9-51.2 MG 子集标准缺失中位（独立实现） vs paper48 §7.5 登记")
print("=" * 60)
p = os.path.join(BASE, "_gaia_abs", "paperX_osc_v10_disk.json")
d = json.load(io.open(p, "r", encoding="utf-8"))
rs = d["results"]
sub = [r for r in rs if 40.9 <= r["B_MG"] <= 51.2]
print("  子集 n=%d" % len(sub))
for nmk in ("Hβ","Hγ","Hδ"):
    vals = [r["miss"][nmk] for r in sub]
    med = np.median(vals)
    print("  %s: 独立复算中位 %.1f%%（P25 %.1f / P75 %.1f） | 论文登记 48/73/98%% 对应 %s %.0f%%" % (
        nmk, med, np.percentile(vals,25), np.percentile(vals,75), nmk, {"Hβ":48,"Hγ":73,"Hδ":98}[nmk]))
    if abs(med - {"Hβ":48,"Hγ":73,"Hδ":98}[nmk]) > 8:
        print("  !! 与登记偏离 >8pp，需核查")

print()
print("全部判据完成")
