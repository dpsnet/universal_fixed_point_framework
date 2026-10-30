# -*- coding: utf-8 -*-
"""
P7-5e-170b：h(2) m=1024 档提取——5 点 Richardson 判别（C=13/128 维持 or 修正）
================================================================
170 全链揭示 C_m 直接口径系统性漂移（0.10148→0.09902，偏离 13/128 −2.5%）。
判别：h(2) 局部通道（169b）是否仍收敛 7/64——
  A) h(2)(1024) 延续每倍程减半 → 5 点 Richardson 仍锁 7/64 → C=13/128 维持
  B) h(2)(1024) 偏离减半路径 → 169b 锁定需重新评估（C 有 m 依赖修正）
方法：同 169b（N=800、xs∈[1.4,2.4] 16 点、E_0·|m| 提取 h(2)）。
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

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
# 169b 已算四档（读 JSON）
old = json.load(open(BASE + r"\_phase102_p7_5e169b_h2_richardson.json", encoding="utf-8"))
h2_m = {int(k): v for k, v in old["h2_m"].items()}
print("== P7-5e-170b：h(2) m=1024 档提取 ==", flush=True)
print("  已有四档：%s" % {k: "%.8f" % v for k, v in h2_m.items()}, flush=True)

# m=1024 档
m = 1024
xs = np.linspace(1.4, 2.4, 16)
Bs = xs / m
Es = np.array([E0_at(b, -m) for b in Bs])
y = Es*m
h = (y - f_model(xs) - g_inf(xs)/m) * m**2
h2 = float(np.interp(2.0, xs, h))
h2_m[m] = h2
print("  m=1024：h(2) = %.8f" % h2, flush=True)

# 5 点序列（含 1024）
ms_all = sorted(h2_m.keys())
print("\n  序列：", flush=True)
for mm in ms_all:
    print("    m=%5d：h(2) = %.8f（7/64 差 %+.3e）" % (mm, h2_m[mm], h2_m[mm]-7.0/64.0), flush=True)

# 倍程减半检验（最后一档是否延续）
if len(ms_all) >= 5:
    d_last = h2_m[ms_all[-2]] - 7.0/64.0
    d_new = h2_m[ms_all[-1]] - 7.0/64.0
    ratio = d_new / d_last
    print("  减半检验：残差比 d(1024)/d(512) = %.3f（1/m 减半预期 ~0.5）" % ratio, flush=True)

# 5 点 Richardson 组
def richardson_3(vals, steps):
    A = np.vstack([np.ones(3), 1.0/np.array(steps)]).T
    c, _, _, _ = np.linalg.lstsq(A, vals, rcond=None)
    return c[0], c[1]

print("\n--- Richardson 外推（含 m=1024 档）---", flush=True)
res = {}
for trio, name in [((128,256,512), "128/256/512"), ((256,512,1024), "256/512/1024"), ((128,256,512,1024), "128/256/512/1024 四点")]:
    v = np.array([h2_m[m] for m in trio])
    if len(trio) == 3:
        h2inf, i2 = richardson_3(v, list(trio))
        res[name] = h2inf
        print("  %s：h(2)_∞ = %.8f（i(2) = %.6f）" % (name, h2inf, i2), flush=True)
    else:
        A4 = np.vstack([np.ones(4), 1.0/np.array(trio), 1.0/np.array(trio)**2]).T
        c4, _, _, _ = np.linalg.lstsq(A4, v, rcond=None)
        res[name] = c4[0]
        print("  %s：h(2)_∞ = %.8f（i=%.4f j=%.2f）" % (name, c4[0], c4[1], c4[2]), flush=True)

vals = list(res.values())
h2_best = float(np.mean(vals))
spread = float(np.max(vals) - np.min(vals))
print("  四通道均值 h(2)_∞ = %.8f（散布 %.1e）" % (h2_best, spread), flush=True)
for name, h2inf in res.items():
    print("  %s：vs 7/64 %+.5f pct" % (name, (h2inf-7.0/64.0)/(7.0/64.0)*100), flush=True)
C_ext = h2_best - 1.0/128.0
print("  C 闭环：C = h(2)_∞ − 1/128 = %.8f（13/128 = %.8f，差 %+.5f pct）" %
      (C_ext, 13.0/128.0, (C_ext-13.0/128.0)/(13.0/128.0)*100), flush=True)
if spread < 2e-5:
    dev7 = abs(h2_best - 7.0/64.0)
    if dev7 < 2e-5:
        verdict = "★★ h(2) = 7/64 维持（5 点外推 %+.2e）→ C = 13/128 解析锁定维持（C_m 直接漂移为高阶污染）" % dev7
    else:
        verdict = "★ h(2) ≠ 7/64（差 %+.3f pct）——C 有 m 依赖修正——169b 锁定需重评" % (dev7/(7.0/64.0)*100)
else:
    verdict = "判别未决（四通道散布 %.1e）" % spread
print("  终判：%s" % verdict, flush=True)

with open(os.path.join(BASE, "_phase102_p7_5e170b_h2_m1024.json"), "w", encoding="utf-8") as fo:
    json.dump({"h2_m": {str(k): v for k, v in h2_m.items()},
               "halving_ratio_last": float(ratio) if len(ms_all) >= 5 else None,
               "richardson": {k: v for k, v in res.items()},
               "h2_best": float(h2_best), "spread": float(spread),
               "C_ext": float(C_ext), "verdict": verdict}, fo, indent=1, ensure_ascii=False)
print("JSON 落盘 OK exit 0", flush=True)
