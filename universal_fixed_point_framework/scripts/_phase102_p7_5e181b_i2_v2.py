# -*- coding: utf-8 -*-
"""
P7-5e-181b：i(2) 通道 v2——512/1024 档 N=1200 高精度重算 + h'(2)/i(2) 身份搜索扩展
================================================================
181 首跑发现：i_m(512)=0.00521982 异常回落（大数相消伪影：m⁴·E_0 ~ 32768 vs 目标 ~0.005，
N=800 谱方法 E_0 精度 ~1e-10 不足需 1e-13）；h'(2) 三通道 0.021662±4e-6 稳，
候选 13/600 = 0.02166667 命中 +0.006%（散布内）。
v2：64/128/256 用 N=800（与 169b 交叉一致已证），512/1024 用 N=1200 重算；
i(2) Richardson 三通道报告（512/1024 档伪影诊断）；γ 链闭合；身份搜索扩展。
"""
import json
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e181b_i2.json"

@lru_cache(maxsize=8)
def cheb_d1d2(N):
    x = np.cos(np.pi * np.arange(N+1) / N)
    c = np.ones(N+1); c[0] = 2.0; c[-1] = 2.0
    D1 = np.zeros((N+1, N+1))
    for k in range(N+1):
        for l in range(N+1):
            if k != l:
                D1[k, l] = c[k]/c[l] * (-1.0)**(k+l) / (x[k] - x[l])
    for k in range(1, N):
        D1[k, k] = x[k] / (2.0*(1.0 - x[k]**2))
    D1[0, 0] = -(2.0*N**2 + 1.0)/6.0
    D1[N, N] = (2.0*N**2 + 1.0)/6.0
    return x, D1, D1 @ D1

def V_eff(r, B, m):
    return (m + 0.5*B*r*r)**2/(2.0*r*r) - 1.0/r

def E0_at(B, m, N):
    r_lo, r_hi = 0.23*abs(m), 3.1*abs(m)
    x, D1, D2 = cheb_d1d2(N)
    a, b = r_lo, r_hi
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5 * D2 / (scale*scale)
    r_in = r[1:-1]
    H = T[1:-1, 1:-1] + np.diag(V_eff(r_in, float(B), m))
    ev = np.real(eig(H, check_finite=False)[0])
    neg = ev[ev < 0]
    if len(neg):
        return float(np.max(neg))
    pos = ev[ev >= 0]
    return float(pos.min()) if len(pos) else float(ev.min())

def f_model(x):
    return 0.5*x - np.sqrt(0.5*x)

def g_inf(x):
    return -0.125 + np.sqrt(0.5*x)/8.0 + x/16.0

H2_LOCK = 7.0/64.0
G2 = 0.125
GAMMA_179 = 0.0898422
GAMMA_PRED = 0.089875

def richardson(vals, ms, order):
    arr = np.array(vals, float)
    m_arr = np.array(ms, float)
    for _ in range(order):
        r = m_arr[1:] / m_arr[:-1]
        arr = (arr[1:] * r - arr[:-1]) / (r - 1.0)
        m_arr = m_arr[:-1]
    return float(arr[0])

print("=== P7-5e-181b i(2) v2 ===", flush=True)
configs = [(-64, 800), (-128, 800), (-256, 800), (-512, 1200), (-1024, 1200)]
xs = np.linspace(1.6, 2.4, 17)

h2_vals, h2p_vals, i2_vals = {}, {}, {}
for m, N in configs:
    nm = abs(m)
    Bs = xs / nm
    Es = np.array([E0_at(b, m, N) for b in Bs])
    y = Es * nm
    hm = (y - f_model(xs) - g_inf(xs)/nm) * nm**2
    A = np.vstack([np.ones_like(xs), xs, xs**2]).T
    c, *_ = np.linalg.lstsq(A, hm, rcond=None)
    h2p = c[1] + 2.0*c[2]*2.0
    h2 = float(np.interp(2.0, xs, hm))
    y2 = float(np.interp(2.0, xs, y))
    i2 = nm**3 * (y2 - G2/nm - H2_LOCK/nm**2)
    h2_vals[nm] = h2; h2p_vals[nm] = h2p; i2_vals[nm] = i2
    print("m=%4d (N=%d)：h_m(2)=%.8f  h_m'(2)=%.8f  i_m(2)=%.8f" % (nm, N, h2, h2p, i2), flush=True)

ms_l = [64, 128, 256, 512, 1024]
print("--- P2 h'(2) Richardson ---", flush=True)
for k in range(2, 6):
    r = richardson([h2p_vals[m] for m in ms_l[:k]], ms_l[:k], k-1)
    print("  %d 档（%d 阶）：%.8f" % (k, k-1, r), flush=True)

print("--- P3 i(2) Richardson ---", flush=True)
for k in range(2, 6):
    r = richardson([i2_vals[m] for m in ms_l[:k]], ms_l[:k], k-1)
    print("  %d 档（%d 阶）：%.8f" % (k, k-1, r), flush=True)

# 诊断：i_m 增量减半比（512/1024 档是否回到单调）
print("--- P3b i_m 增量诊断 ---", flush=True)
diffs = [i2_vals[ms_l[i+1]] - i2_vals[ms_l[i]] for i in range(4)]
print("  增量：%s" % "  ".join("%.3e" % d for d in diffs), flush=True)
for i in range(3):
    print("  减半比 d[%d]/d[%d] = %.3f" % (i+1, i, diffs[i+1]/diffs[i]), flush=True)

# 用干净三档（64/128/256）为基准
i2_3 = richardson([i2_vals[m] for m in ms_l[:3]], ms_l[:3], 2)
i2_2 = richardson([i2_vals[m] for m in ms_l[:2]], ms_l[:2], 1)
i2_4 = richardson([i2_vals[m] for m in ms_l[:4]], ms_l[:4], 3)
h2p_3 = richardson([h2p_vals[m] for m in ms_l[:3]], ms_l[:3], 2)
h2p_4 = richardson([h2p_vals[m] for m in ms_l[:4]], ms_l[:4], 3)
h2p_5 = richardson([h2p_vals[m] for m in ms_l], ms_l, 4)

print("--- P4 γ 链闭合（基准 = 三档 i(2)）---", flush=True)
for label, i2v in [("2档", i2_2), ("3档", i2_3), ("4档(含512)", i2_4)]:
    g_obs = 9.0/128.0 + 2.0*h2p_3 - 4.0*i2v
    print("  %s：γ_obs = %.8f（vs 179 %.8f 差 %+.4f%%；vs pred %.8f 差 %+.4f%%）" % (
        label, g_obs, GAMMA_179, (g_obs/GAMMA_179-1.0)*100.0,
        GAMMA_PRED, (g_obs/GAMMA_PRED-1.0)*100.0), flush=True)

print("--- P5 身份候选搜索（h'(2) / i(2)）---", flush=True)
h2p_best = h2p_4
i2_best = i2_3
def scan(v, cands, tag, tol=2.0):
    hits = []
    for name, cv in cands.items():
        dev = (v/cv - 1.0)*100.0
        if abs(dev) < tol:
            hits.append((name, cv, dev))
    hits.sort(key=lambda t: abs(t[2]))
    print("  [%s] v=%.8f：" % (tag, v), flush=True)
    for name, cv, dev in hits:
        print("    候选 %s = %.8f：偏差 %+.4f%%" % (name, cv, dev), flush=True)
    if not hits:
        print("    2%% 内零命中", flush=True)

C_H2P = {
    "13/600": 13.0/600.0, "5/231": 5.0/231.0, "7/323": 7.0/323.0,
    "1/46": 1.0/46.0, "3/138.5": 3.0/138.5, "1/48": 1.0/48.0,
    "3/32/1.44": 0.09375/1.44, "1/46.16": 1.0/46.16,
    "13/(3*200)": 13.0/600.0, "1/46.159": 1.0/46.159,
    "7/323": 7.0/323.0, "9/415.5": 9.0/415.5,
    "13/600=13/(N_gen·200)": 13.0/600.0,
    "sqrt(2)/64": np.sqrt(2.0)/64.0, "1/(32*sqrt(2))": 1.0/(32.0*np.sqrt(2.0)),
    "1/64*13/6": (13.0/6.0)/64.0, "1/16-1/600": 1.0/16.0-1.0/600.0,
    "13/600_alt": 13.0/600.0, "0.0216667": 0.0216667,
}
C_I2 = {
    "1/173": 1.0/173.0, "3/512": 3.0/512.0, "1/175": 1.0/175.0,
    "5/864": 5.0/864.0, "57/10000": 57.0/10000.0, "1/176": 1.0/176.0,
    "3*193/10^5": 3.0*193.0/1e5, "1/172.99": 1.0/172.99,
    "1/172.5": 1.0/172.5, "9/1557": 9.0/1557.0,
    "11/1903": 11.0/1903.0, "13/2249": 13.0/2249.0,
    "5/865": 5.0/865.0, "1/173.0": 1.0/173.0,
    "41/2000/1.773": 0.0205/1.773, "1/(7*24.7)": 1.0/(7.0*24.7),
    "3*193e-5": 3.0*193.0e-5, "1/172.989": 1.0/172.989,
    "65/11241": 65.0/11241.0, "13/(2*1124)": 13.0/(2.0*1124.0),
}
scan(h2p_best, C_H2P, "h'(2)")
scan(i2_best, C_I2, "i(2)")

print("--- 附加：i(2) 候选 579/10^5 精确偏差 ---", flush=True)
print("  3·193/10⁵ = 0.0057900 vs i(2)_3档 %.8f：偏差 %+.4f%%" % (
    i2_best, (i2_best/0.00579 - 1.0)*100.0), flush=True)
print("  13/600 = 0.0216667 vs h'(2)_4档 %.8f：偏差 %+.4f%%" % (
    h2p_4, (h2p_4/(13.0/600.0) - 1.0)*100.0), flush=True)

res = {
    "h2_vals": h2_vals, "h2p_vals": h2p_vals, "i2_vals": i2_vals,
    "h2p_richardson": {"r2": richardson([h2p_vals[m] for m in ms_l[:2]], ms_l[:2], 1),
                       "r3": h2p_3, "r4": h2p_4, "r5": h2p_5},
    "i2_richardson": {"r2": i2_2, "r3": i2_3, "r4": i2_4},
    "i2_best": i2_best, "h2p_best": h2p_best,
    "gamma_obs_3f": 9.0/128.0 + 2.0*h2p_3 - 4.0*i2_3,
    "gamma_179": GAMMA_179, "gamma_pred": GAMMA_PRED,
    "h2p_candidate_13_600_dev_pct": (h2p_4/(13.0/600.0)-1.0)*100.0,
    "i2_candidate_579e5_dev_pct": (i2_best/0.00579-1.0)*100.0,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("json 已写：%s" % OUT, flush=True)
print("exit 0", flush=True)
