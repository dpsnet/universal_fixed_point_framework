# -*- coding: utf-8 -*-
"""
P7-5e-169：互补恒等来源判别——h(x) 精确形态 + f 的 m 依赖线性项检验
================================================================
167 锁定 f + 8g = x − 1（机器精度），但"为何 k_max 归一化绑定"开放。
剩余候选：(a) f 有 m 依赖线性项 κ·x（被 g 提取吸收进 h 层）
          (b) h(x) 含隐藏封闭形态（→ h(2) 精确值 → C 解析锁定）
本步：复现 147 三档 h(x) 提取，判别
  A) h 三档差的 m 缩放（纯 i(x)/m 残差 vs 常数 κ·x 指纹）
  B) h(x) 形态多模型判别（找精确形态候选）
  C) h(2) 精确候选对照（7/64 vs 0.109395）
"""
import numpy as np
from scipy.linalg import eig

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

print("=== P7-5e-169 互补恒等来源判别 ===", flush=True)
ms = [-64, -128, -256]
xs = np.linspace(0.6, 2.5, 24)
hs = {}
for m in ms:
    Bs = xs / abs(m)
    Es = np.array([E0_at(b, m) for b in Bs])
    y = Es*abs(m)
    h = (y - f_model(xs) - g_inf(xs)/abs(m)) * abs(m)**2
    hs[m] = h
    print("m=%4d：24 点完成" % abs(m), flush=True)

print("\n--- A) h 三档差 m 缩放判别（f 的 m 依赖线性项指纹）---", flush=True)
d1 = hs[-64] - hs[-256]
d2 = hs[-128] - hs[-256]
rms1, rms2 = float(np.sqrt(np.mean(d1**2))), float(np.sqrt(np.mean(d2**2)))
print("  |h_64 − h_256| RMS = %.3e；|h_128 − h_256| RMS = %.3e" % (rms1, rms2), flush=True)
print("  比值 = %.2f（纯 i(x)/m 残差应 ≈ 2.0；常数 κ·x 指纹应 → 1.0）" % (rms1/rms2), flush=True)
# 逐点比值
ratio_pt = d1/d2
print("  逐点比值 中位 %.2f  极差 [%.2f, %.2f]" %
      (float(np.median(ratio_pt)), float(np.min(ratio_pt)), float(np.max(ratio_pt))), flush=True)
# 常数项检验：d1/m 缩放后是否有常数分量
# 若 h_m = h + κ·x（κ 常数）→ d1(m1,m2) = κ·x 与 m 无关
A_c = np.vstack([np.ones_like(xs), xs]).T
c1_, _, _, _ = np.linalg.lstsq(A_c, d1, rcond=None)
c2_, _, _, _ = np.linalg.lstsq(A_c, d2, rcond=None)
print("  差拟合 a+bx：d1 a=%.2e b=%.2e；d2 a=%.2e b=%.2e" % (c1_[0], c1_[1], c2_[0], c2_[1]), flush=True)
print("  b 比值 = %.2f（≈2 → 差∝1/m 无常数 κ·x；≈1 → 常数指纹存在）" % (c1_[1]/c2_[1]), flush=True)

print("\n--- B) h(x) 形态多模型判别（m=256 档）---", flush=True)
h = hs[-256]
models = {
    "a+b√x+cx":       lambda x: np.vstack([np.ones_like(x), np.sqrt(x), x]).T,
    "a+b√x+cx+d/x":   lambda x: np.vstack([np.ones_like(x), np.sqrt(x), x, 1.0/x]).T,
    "a+b√x+cx+dx²":   lambda x: np.vstack([np.ones_like(x), np.sqrt(x), x, x*x]).T,
    "a+b√x+cx+d√x·x": lambda x: np.vstack([np.ones_like(x), np.sqrt(x), x, np.sqrt(x)*x]).T,
    "a+b√x+cx+d/x²":  lambda x: np.vstack([np.ones_like(x), np.sqrt(x), x, 1.0/x**2]).T,
}
best = None
for name, fn in models.items():
    A = fn(xs)
    c, _, _, _ = np.linalg.lstsq(A, h, rcond=None)
    r = float(np.sqrt(np.mean((A@c - h)**2)))
    print("  %-18s 系数 %s  RMS = %.2e" % (name, np.array2string(c, precision=6), r), flush=True)
    if best is None or r < best[1]:
        best = (name, r, c)

print("\n--- C) h(2) 精确候选对照 ---", flush=True)
h2_num = float(np.interp(2.0, xs, h))
print("  h(2) 插值（m=256）= %.6f" % h2_num, flush=True)
print("  候选 7/64 = %.6f（差 %+.4f pct）｜数值 0.109395（差 %+.4f pct）" %
      (7.0/64.0, (h2_num-7.0/64.0)/(7.0/64.0)*100, (h2_num-0.109395)/0.109395*100), flush=True)
print("  C 闭环：h(2)−1/128 = %.6f（13/128=%.6f）" % (h2_num-1.0/128.0, 13.0/128.0), flush=True)

print("\n--- 判别 ---", flush=True)
if best[1] < 1e-8:
    print("  ★ h(x) 精确形态候选：%s（RMS %.1e）——h(2) 解析身份可锁定" % (best[0], best[1]), flush=True)
else:
    print("  h(x) 无简单封闭形态（最优 %s RMS %.1e）——形态含更高阶结构" % (best[0], best[1]), flush=True)
print("exit 0", flush=True)
