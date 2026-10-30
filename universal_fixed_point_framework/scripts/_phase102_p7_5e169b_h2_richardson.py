# -*- coding: utf-8 -*-
"""
P7-5e-169b：h(2) Richardson 三点外推终判——7/64 vs 0.109395
================================================================
169 A 证明 h_m(x) 差纯 i(x)/m 残差（比值 3.0 精确匹配 1/m 理论值）——
h_m(2) = h(2) + i(2)/m → 三点 Richardson 外推 m→∞ 可消残差。
四档 {64,128,256,512} × 16 点（x∈[1.4,2.4] 聚焦 x=2）：
  P1 h_m(2) 四档序列
  P2 Richardson 三点外推 h(2)_∞（三组：64/128/256、128/256/512、64/128/256/512 四点）
  P3 判别：h(2)_∞ vs 7/64 = 0.109375 vs 0.109395
  P4 C 闭环：C = h(2)_∞ − 1/128 vs 13/128
"""
import numpy as np
from scipy.linalg import eig
import json, os

N_SP = 800

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

def richardson_3(vals, steps):
    """三点 Richardson：v(m) = h + i/m（1/m 残差）→ h = (v1 s1 - ... )"""
    # v_j = h + i/m_j → h = (v1/m2 - v2/m1)/(1/m2 - 1/m1) 逐对后取均值不行——
    # 标准：h = v3 + (v3-v2)*(1/m3)/(1/m2-1/m3)... 用最小二乘 h + i/m
    A = np.vstack([np.ones(3), 1.0/np.array(steps)]).T
    c, _, _, _ = np.linalg.lstsq(A, vals, rcond=None)
    return c[0], c[1]

print("=== P7-5e-169b h(2) Richardson 外推终判 ===", flush=True)
ms = [64, 128, 256, 512]
xs = np.linspace(1.4, 2.4, 16)
h2_m = {}
for m in ms:
    Bs = xs / m
    Es = np.array([E0_at(b, -m) for b in Bs])   # 负 m 才是有束缚态的物理通道
    y = Es*m
    h = (y - f_model(xs) - g_inf(xs)/m) * m**2
    h2 = float(np.interp(2.0, xs, h))
    h2_m[m] = h2
    print("  m=%3d：h(2) = %.8f" % (m, h2), flush=True)

print("\n--- P2 Richardson 外推 ---", flush=True)
res = {}
for trio, name in [((64,128,256), "64/128/256"), ((128,256,512), "128/256/512")]:
    v = np.array([h2_m[m] for m in trio])
    h2inf, i2 = richardson_3(v, list(trio))
    res[name] = h2inf
    print("  %s：h(2)_∞ = %.8f（i(2) = %.6f）" % (name, h2inf, i2), flush=True)
# 四点外推 h + i/m + j/m²
v4 = np.array([h2_m[m] for m in ms])
A4 = np.vstack([np.ones(4), 1.0/np.array(ms), 1.0/np.array(ms)**2]).T
c4, _, _, _ = np.linalg.lstsq(A4, v4, rcond=None)
res["quad"] = c4[0]
print("  四点（h+i/m+j/m²）：h(2)_∞ = %.8f（i=%.4f j=%.2f）" % (c4[0], c4[1], c4[2]), flush=True)

print("\n--- P3 判别 ---", flush=True)
vals = list(res.values())
h2_best = float(np.mean(vals))
spread = float(np.max(vals) - np.min(vals))
print("  三通道均值 h(2)_∞ = %.8f（散布 %.1e）" % (h2_best, spread), flush=True)
for name, h2inf in res.items():
    print("  %s：vs 7/64 %+.5f pct｜vs 0.109395 %+.5f pct" %
          (name, (h2inf-7.0/64.0)/(7.0/64.0)*100, (h2inf-0.109395)/0.109395*100), flush=True)
C_ext = h2_best - 1.0/128.0
print("  C 闭环：C = h(2)_∞ − 1/128 = %.8f（13/128 = %.8f，差 %+.5f pct）" %
      (C_ext, 13.0/128.0, (C_ext-13.0/128.0)/(13.0/128.0)*100), flush=True)
if spread < 2e-5:
    dev7 = abs(h2_best - 7.0/64.0)
    if dev7 < 2e-5:
        verdict = "★★ h(2) = 7/64 锁定（外推 %+.2e）→ C = 13/128 解析链闭合" % dev7
    else:
        verdict = "★ h(2) ≠ 7/64（差 %+.3f pct）——0.109395 数值维持，13/128 解析闭合未达成" % (dev7/(7.0/64.0)*100)
else:
    verdict = "判别未决（三通道散布 %.1e）" % spread
print("  终判：%s" % verdict, flush=True)
print("  诚实边界：外推依赖 1/m 残差纯度（169 A 已证比值 3.0 精确）；m≤512 数据", flush=True)

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with open(os.path.join(BASE, "_phase102_p7_5e169b_h2_richardson.json"), "w", encoding="utf-8") as fo:
    json.dump({"h2_m": {str(m): v for m, v in h2_m.items()},
               "richardson": {k: v for k, v in res.items()},
               "h2_best": float(h2_best), "spread": float(spread),
               "C_ext": float(C_ext), "verdict": verdict}, fo, indent=1, ensure_ascii=False)
print("JSON 落盘 OK exit 0", flush=True)
