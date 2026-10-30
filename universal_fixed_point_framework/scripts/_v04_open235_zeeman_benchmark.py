# -*- coding: utf-8 -*-
"""104az-235: #481 理论基准线 —— 强场氢原子 Zeeman 分量频率表（标准量子力学）
n=1..4 全 (l,m,s) 基组，对角化 H0 + gamma*(Lz+2Sz) + gamma^2/8*rho^2
输出：Halpha (3->2) 分量频率位移 @ 100/200/300/500/700/1000 MG
对照：一阶 Zeeman 预言（4.67e-13*lambda^2*B 锚点）→ 二次修正残差结构
注：纯标准 QM，无框架内容——为将来观测对照的 A 级基准线。
忽略精细结构/自旋轨道（~1e-5 eV 量级 << 分量间隔）。
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, lpmv, factorial

# 物理常数（原子单位）
B0 = 2.3505e9          # G，一原子单位磁场
R_INF = 109737.315685  # cm^-1
LAM_HA = 6562.79       # Halpha 零场波长 A

# ---------- 基组：n=1..4，全 (l,m)，ms=+1/2 与 -1/2 分离块 ----------
def basis(nmax=4):
    st = []
    for n in range(1, nmax + 1):
        for l in range(n):
            for m in range(-l, l + 1):
                st.append((n, l, m))
    return st

ST = basis(4)
NS = len(ST)
IDX = {s: i for i, s in enumerate(ST)}

# ---------- 径向 <n'l'|r^2|nl>：高斯-勒让德数值积分（l'=l 才非零，跨 n 全算） ----------
def R_nl(n, l, r):
    """氢径向波函数 R_nl(r)（a.u.，实）"""
    rho = 2.0 * r / n
    norm = np.sqrt((2.0 / n) ** 3 * factorial(n - l - 1) / (2.0 * n * factorial(n + l)))
    return norm * np.exp(-r / n) * (2.0 * r / n) ** l * genlaguerre(n - l - 1, 2 * l + 1)(rho)

def r2_int(n, l, np_, r_max=140.0, N=400):
    x, w = leggauss(N)
    r = 0.5 * r_max * (x + 1.0)          # [0, r_max]
    f = R_nl(n, l, r) * R_nl(np_, l, r) * r ** 4
    return float(0.5 * r_max * np.sum(w * f))

# ---------- 角向 <l'm'|sin^2 theta|lm>：leggauss 数值（theta） ----------
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

# ---------- 哈密顿量矩阵（对每个 ms 块；含一阶 Zeeman (γ/2)(Lz+2Sz) + 抗磁 γ²/8·ρ²） ----------
def hamiltonian(gamma, ms, with_diamag=True):
    H = np.zeros((NS, NS))
    for i, (n, l, m) in enumerate(ST):
        E0 = -0.5 / n ** 2
        Hz = 0.5 * gamma * (m + 2 * ms)      # (γ/2)(L_z + 2S_z)
        H[i, i] = E0 + Hz
    if with_diamag:
        for i, (n1, l1, m1) in enumerate(ST):
            for j, (n2, l2, m2) in enumerate(ST):
                if m1 != m2 or l1 != l2:
                    continue
                a = ang_sin2(l1, m1, l2, m2)
                if abs(a) < 1e-12:
                    continue
                H[i, j] += (gamma ** 2 / 8.0) * r2_int(n1, l1, n2) * a
    return H

# ---------- 主流程 ----------
E3_0 = -0.5 / 9.0          # n=3 库仑零场能（a.u.）
E2_0 = -0.5 / 4.0          # n=2
DE0 = (E3_0 - E2_0) * 2 * R_INF   # 零场 Halpha 跃迁 cm^-1

def zee_freqs(B_MG, with_diamag=True):
    """分量相对零场 Halpha 的频率位移（cm^-1，减库仑零场跃迁；偶极允许筛选）"""
    gamma = B_MG * 1e6 / B0
    freqs = []
    for ms in (0.5, -0.5):
        H = hamiltonian(gamma, ms, with_diamag)
        E, V = np.linalg.eigh(H)          # E: a.u.
        def band_weight(nb):
            w = np.zeros(NS)
            for i, (n, l, m) in enumerate(ST):
                if n == nb:
                    w += V[i] ** 2
            return w
        up_w = band_weight(3)
        dn_w = band_weight(2)
        up = [k for k in range(NS) if up_w[k] > 0.5]
        dn = [k for k in range(NS) if dn_w[k] > 0.5]
        # 每本征态 ⟨L_z⟩（ms 块内固定 → 自旋不翻转天然满足 Δm_s=0）
        def Lz(k):
            return float(sum(V[i, k] ** 2 * ST[i][2] for i in range(NS)))
        for ku in up:
            for kd in dn:
                if abs(Lz(ku) - Lz(kd)) > 1.15:      # 偶极选择定则 |Δm_l| ≤ 1（混合容差）
                    continue
                dE = (E[ku] - E[kd] - (E3_0 - E2_0)) * 2 * R_INF   # cm^-1 相对零场
                freqs.append(dE)
    return sorted(freqs)

def unique_sorted(f, tol=0.5):
    keep = []
    for x in f:
        if not keep or abs(x - keep[-1]) > tol:
            keep.append(x)
    return keep

print("=== Halpha 强场 Zeeman 分量频率（标准 QM 精确对角化，n=1..4 基组，(γ/2)(Lz+2Sz) + γ²/8·ρ²）===")
print(f"{'B(MG)':>6} {'γ':>8} {'一阶分量数':>8} {'完整分量数':>8}  二次效应残差（完整−一阶，cm⁻¹）")
print("  （残差 = 抗磁 γ²/8·ρ² + 高阶耦合贡献 —— #481 B 级要检验的结构）")
for B in (50, 100, 200, 300, 500, 700, 1000):
    f1 = unique_sorted(zee_freqs(B, with_diamag=False))
    f2 = unique_sorted(zee_freqs(B, with_diamag=True))
    gamma = B * 1e6 / B0
    # 配对最近分量求残差
    resid = []
    for x in f2:
        j = min(range(len(f1)), key=lambda j_: abs(f1[j_] - x))
        resid.append(x - f1[j])
    resid.sort()
    s = "  ".join(f"{r:+9.3f}" for r in resid[:10])
    print(f"{B:>6} {gamma:>8.5f} {len(f1):>8} {len(f2):>8}  {s}")
    if len(resid) > 10:
        print(f"{'':>30} ...共 {len(resid)} 个残差，中位 {resid[len(resid)//2]:+.3f}")

print()
print("=== 弱场极限锚点：4.67e-13·λ²·B 公式（v13 C3 判据域，<5 MG 适用）===")
for B in (0.1, 1.0, 5.0):
    dlam = 4.67e-13 * LAM_HA ** 2 * (B * 1e6)
    dnu = dlam / (LAM_HA * (LAM_HA + dlam)) * 1e8
    print(f"B={B:>5.1f} MG: dlam={dlam:>9.3f} A, dnu={dnu:>10.4f} cm^-1（单位分量，g·m 组合系数另乘）")
    f = unique_sorted(zee_freqs(B, with_diamag=True))
    print(f"  -> 精确对角化最内层分量位移 ~ {abs(f[0]):.3f} / {abs(f[-1]):.3f} cm^-1（符号两端）")
