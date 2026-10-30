# -*- coding: utf-8 -*-
"""
Phase 104az-38 (26.16j-86): 切换点精确定位 -- eta_comp(n,B)=0.8 交叉场强 vs B_th 序列
复用 _phase100_p3b_compression.py 的 tail_fraction/eta_comp 实现
问题: 加法静默 (1-3sigma=0.8) 的切换点 = eta_comp 达 0.8 的场强?
对照 B_th 序列 (n=7..3): 48.01/65.35/94.11/147.05/261.41 MG (B_th*n^2 = 2352.7 恒定)
"""
import json, os, math
import numpy as np

# ---- 复用 p3b 实现 ----
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
    R = R_nl(n, l, r)
    return R * R * r * r

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

def radial_matrix_au(n1, l1, n2, l2, rmax=160.0, npts=30000):
    r = np.linspace(1e-6, rmax, npts)
    R1 = np.array([R_nl(n1, l1, x) for x in r])
    R2 = np.array([R_nl(n2, l2, x) for x in r])
    return float(np.trapezoid(R1 * R2 * r ** 3, r))

def balmer_l_weights(n_up):
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

def tail_fraction(n_up, R_cut, npts=20000):
    wl = balmer_l_weights(n_up)
    r = np.linspace(1e-6, 200.0, npts)
    dr = r[1] - r[0]
    dens = np.zeros_like(r)
    for l, w in wl.items():
        dens += w * np.array([radial_density(n_up, l, x) for x in r])
    total = float(np.sum(dens) * dr)
    tail = float(np.sum(dens[r > R_cut]) * dr)
    return tail / total

def landau_length(B_T):
    return 1.0 / math.sqrt(B_T / 2.35e5)

def eta_comp(n, B_T, C):
    return tail_fraction(n, C * landau_length(B_T))

# ---- 切换点扫描 ----
names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}
B_th = {7: 48.01, 6: 65.35, 5: 94.11, 4: 147.05, 3: 261.41}  # MG
B_MG = np.linspace(5.0, 300.0, 296)

res = {"model": "eta_comp(n,B)=0.8 交叉场强", "C": 3.0, "cross": {}, "B_th": B_th,
       "relation": {}, "verdict": ""}

print("=" * 100)
print("切换点定位: eta_comp(n,B) = 0.8 交叉场强 (C=3.0)")
print(f"{'线':<6}{'B_th(MG)':<12}{'B_0.8(MG)':<12}{'B_0.8/B_th':<12}")

for n in (3, 4, 5, 6, 7):
    cross = None
    for B in B_MG:
        B_T = B * 100.0  # 1 MG = 100 Tesla
        eta = eta_comp(n, B_T, 3.0)
        if eta >= 0.8:
            cross = float(B)
            break
    bth = B_th[n]
    ratio = cross / bth if cross else None
    res["cross"][names[n]] = cross
    res["relation"][names[n]] = {"B_th": bth, "B_0.8": cross,
                                  "ratio_B08_Bth": round(ratio, 4) if ratio else None}
    cross_s = f"{cross:.2f}" if cross else "-"
    ratio_s = f"{ratio:.4f}" if ratio else "-"
    print(f"{names[n]:<6}{bth:<12.2f}{cross_s:<12}{ratio_s:<12}")

# 关系分析: B_0.8 vs B_th -- 是否 B_0.8 ~ B_th/2? B_0.8*n^2 恒定?
print("\n关系候选:")
n2_const = {}
for n in (3, 4, 5, 6, 7):
    c = res["cross"][names[n]]
    if c:
        n2_const[names[n]] = round(c * n**2, 2)
print(f"  B_0.8 * n^2 恒定候选: {n2_const}")
res["B08_n2"] = n2_const

# 45 MG 分档交叉确认
print("\n45 MG 分档交叉确认:")
for n in (3, 4, 5, 6, 7):
    eta45 = eta_comp(n, 4500.0, 3.0)  # 45 MG = 4500 T
    print(f"  {names[n]}: eta_comp(45MG)={eta45:.3f} {'>=0.8' if eta45>=0.8 else '<0.8'}")
    res.setdefault("eta45", {})[names[n]] = round(eta45, 4)

verdict = (
    "切换点定位: B_0.8(n) (eta_comp 达 0.8 的场强) vs B_th(n) -- 关系候选: "
    + ("B_0.8*n^2 恒定=" + str(n2_const) if len(set(n2_const.values())) <= 2 else "非恒定")
    + "; 加法静默切换点=B_0.8(n) (线依赖) -- B_th 为阈值序列(禁戒开始), B_0.8 为压缩饱和(0.8) -- 两序列关系待判"
)
res["verdict"] = verdict

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_p1_switch_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2, default=float)
print(f"\n{verdict}")
print(f"已存盘: {out}")
