# -*- coding: utf-8 -*-
"""
P7-5e-181：E 的碗形 i(2) Richardson 通道——碗形第 3 层系数提取 + γ 链闭合
================================================================
背景：180 已证 δ4 通道分辨率不足（±1.69e-3 > 候选差 6.0e-4），E=+41/2000 vs ≈0.0199
判别需更高精度层。180 笔记推导：i(2) = h'(2)/2 + 9/512 − γ/4（碗形 1/m³ 层系数
与过零位移 1/m³ 层系数 γ 的映射，独立于 δ 拟合）。
本步执行：
  P1 四档（64/128/256/512）E_0(x/m)·|m| 曲线（x 聚焦 [1.6, 2.4]）
  P2 h_m(x) = m²·(y − f − g_∞/m)，h_m'(2) 独立提取 + Richardson → h'_∞(2)
  P3 i_m(2) = m³·(y(2) − g_∞(2)/m − h(2)/m²)（h(2)=7/64 已锁），Richardson → i_∞(2)
  P4 γ 链闭合验证：γ_obs = 9/128 + 2h'_∞(2) − 4i_∞(2) vs 179 实测 γ=0.0898422
     （若闭合 → 碗形链 f→g→h→i 四层自洽；γ 差 → 判别 γ 真值 → D 链延伸）
  P5 i(2) 身份候选搜索（框架量代数）
诚实边界：E 的 1/m⁴ 层关联需 h''(2)/i'(2)/j(2)，本步不强行（成本高误差累积）；
本步交付 i(2) 与 γ 链闭合结果作为碗形侧新资产 + E 的间接方向点。
"""
import json
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

N_SP = 800
OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e181_i2.json"

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

def E0_at(B, m, N=N_SP):
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

H2_LOCK = 7.0/64.0          # 169b 锁定
G2 = 0.125                  # g(2)=1/8 精确
GAMMA_179 = 0.0898422       # 179 实测（33..128）
GAMMA_PRED = 0.089875       # 41/2000 预测（179 推导）

def richardson(vals, ms, order):
    """vals[i] at ms[i], ms 倍增。order=1 一阶 1/m 残差，2 二阶..."""
    arr = np.array(vals, float)
    m_arr = np.array(ms, float)
    for _ in range(order):
        r = m_arr[1:] / m_arr[:-1]
        arr = (arr[1:] * r - arr[:-1]) / (r - 1.0)
        m_arr = m_arr[:-1]
    return float(arr[0])

print("=== P7-5e-181 i(2) 碗形通道 ===", flush=True)
ms = [-64, -128, -256, -512]
xs = np.linspace(1.6, 2.4, 17)   # 聚焦窗口，步长 0.05

h2_vals = {}   # m -> h_m(2)（用 h(2) 锁值 7/64 会吸收 i/m 残差，这里同时给原始 h_m(2)）
h2p_vals = {}  # m -> h_m'(2)
i2_vals = {}   # m -> i_m(2)（用 H2_LOCK）

for m in ms:
    nm = abs(m)
    Bs = xs / nm
    Es = np.array([E0_at(b, m) for b in Bs])
    y = Es * nm
    hm = (y - f_model(xs) - g_inf(xs)/nm) * nm**2
    # h_m'(2)：二次多项式拟合局部导数（x=1.6..2.4）
    A = np.vstack([np.ones_like(xs), xs, xs**2]).T
    c, *_ = np.linalg.lstsq(A, hm, rcond=None)
    h2p = c[1] + 2.0*c[2]*2.0
    h2 = float(np.interp(2.0, xs, hm))
    # i_m(2)：x=2 处，用锁定 h(2)=7/64
    y2 = float(np.interp(2.0, xs, y))
    i2 = nm**3 * (y2 - G2/nm - H2_LOCK/nm**2)
    h2_vals[nm] = h2
    h2p_vals[nm] = h2p
    i2_vals[nm] = i2
    print("m=%4d：h_m(2)=%.8f  h_m'(2)=%.8f  i_m(2)=%.8f" % (nm, h2, h2p, i2), flush=True)

print("--- P2 h'(2) Richardson ---", flush=True)
ms_l = [64, 128, 256, 512]
r1 = richardson([h2p_vals[m] for m in ms_l[:2]], ms_l[:2], 1)
r2 = richardson([h2p_vals[m] for m in ms_l[:3]], ms_l[:3], 2)
r3 = richardson([h2p_vals[m] for m in ms_l], ms_l, 3)
print("  h'(2) Richardson：2档 %.8f / 3档 %.8f / 4档 %.8f" % (r1, r2, r3), flush=True)

print("--- P3 i(2) Richardson ---", flush=True)
s1 = richardson([i2_vals[m] for m in ms_l[:2]], ms_l[:2], 1)
s2 = richardson([i2_vals[m] for m in ms_l[:3]], ms_l[:3], 2)
s3 = richardson([i2_vals[m] for m in ms_l], ms_l, 3)
print("  i(2) Richardson：2档 %.8f / 3档 %.8f / 4档 %.8f" % (s1, s2, s3), flush=True)

print("--- P4 γ 链闭合验证 ---", flush=True)
i2_best = s3 if s3 is not None else s2
h2p_best = r3 if r3 is not None else r2
gamma_obs = 9.0/128.0 + 2.0*h2p_best - 4.0*i2_best
print("  γ_obs = 9/128 + 2·h'(2) − 4·i(2) = %.8f" % gamma_obs, flush=True)
print("  vs 179 实测 γ = %.8f：差 %.4f%%" % (GAMMA_179, (gamma_obs/GAMMA_179 - 1.0)*100.0), flush=True)
print("  vs 41/2000 预测 γ = %.8f：差 %.4f%%" % (GAMMA_PRED, (gamma_obs/GAMMA_PRED - 1.0)*100.0), flush=True)
print("  反向：由 γ_179 与 h'(2) 反推 i(2) = 9/512 + h'(2)/2 − γ/4 = %.8f（vs 直接提取 %.8f）" % (
    9.0/512.0 + h2p_best/2.0 - GAMMA_179/4.0, i2_best), flush=True)

print("--- P5 i(2) 身份候选搜索 ---", flush=True)
i2v = i2_best
cands = {
    "1/24": 1.0/24.0, "1/48": 1.0/48.0, "1/64": 1.0/64.0, "3/128": 3.0/128.0,
    "5/256": 5.0/256.0, "7/256": 7.0/256.0, "9/512": 9.0/512.0, "11/512": 11.0/512.0,
    "13/512": 13.0/512.0, "15/1024": 15.0/1024.0, "17/1024": 17.0/1024.0,
    "1/56": 1.0/56.0, "1/32": 1.0/32.0, "41/2000": 41.0/2000.0, "13/128": 13.0/128.0,
    "7/64": 7.0/64.0, "3/64": 3.0/64.0, "1/16": 1.0/16.0, "1/128": 1.0/128.0,
    "1/512": 1.0/512.0, "1/1024": 1.0/1024.0, "3/1024": 3.0/1024.0,
    "103/5000": 103.0/5000.0, "1/200": 1.0/200.0, "1/100": 1.0/100.0,
    "9/1024": 9.0/1024.0, "11/1024": 11.0/1024.0, "5/1024": 5.0/1024.0,
    "13/1024": 13.0/1024.0, "15/1024": 15.0/1024.0, "1/40": 1.0/40.0,
}
hits = []
for name, v in cands.items():
    dev = (i2v/v - 1.0) * 100.0
    if abs(dev) < 2.0:
        hits.append((name, v, dev))
hits.sort(key=lambda t: abs(t[2]))
for name, v, dev in hits:
    print("  候选 %s = %.8f：偏差 %+.4f%%" % (name, v, dev), flush=True)
if not hits:
    print("  2% 内零命中", flush=True)

print("--- 附加：i(2) 与 E 关联检查（1/m⁴ 层映射符号）---", flush=True)
# 过零 1/m⁴ 方程（含 j(2)、i'(2)、h''(2)）：不强行数值，仅登记结构
print("  δ4 = −γ/4 − 25/2048 + 9h'(2)/8 − h''(2)/2 + 2i'(2) − 4j(2)（1/m⁴ 过零方程，符号已验）", flush=True)

res = {
    "P2_h2p": h2p_vals, "P3_i2": i2_vals,
    "h2p_richardson": {"r1": r1, "r2": r2, "r3": r3},
    "i2_richardson": {"r1": s1, "r2": s2, "r3": s3},
    "i2_best": i2_best, "h2p_best": h2p_best,
    "gamma_obs": gamma_obs, "gamma_179": GAMMA_179, "gamma_pred": GAMMA_PRED,
    "gamma_dev_pct_179": (gamma_obs/GAMMA_179 - 1.0)*100.0,
    "i2_from_gamma179": 9.0/512.0 + h2p_best/2.0 - GAMMA_179/4.0,
    "identity_hits": hits,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("json 已写：%s" % OUT, flush=True)
print("exit 0", flush=True)
