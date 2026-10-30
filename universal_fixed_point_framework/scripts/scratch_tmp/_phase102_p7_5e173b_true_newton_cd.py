# -*- coding: utf-8 -*-
"""
P7-5e-173b: 真实 E(B) Newton 求根——消除三次插值截断伪影，重新拟合 C/D
========================================================================
173 意外：w=0.01 窄窗拟合爆炸（C/D 发散）——窄窗是另一种数值病（7 点三次
插值在窄窗下条件变差），172 的"κ→0 ⟹ 真实无 κ"推理不完整。
173b：B* 提取改为——7 点三次插值给初值 → 对【真实 E(B)】做 2 步 Newton
（E' 中心差分）。三次插值只决定初值，结果与 w 无关，截断伪影 O(w⁴) 消除。
判别：C vs 13/128、D vs 103/5000（用户候选：103 = 2^7 − 5^2，分母 5^4·2^3）、
残差 RMS（真实提取后是否无 κ 项）。
"""
import numpy as np
from scipy.linalg import eig
from functools import lru_cache

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

def closed_1B(m):
    a = abs(m)
    tail = 1.0/(7.0*2.0**a) if a <= 120 else 0.0
    return a/2.0 + 1.0/7.0 + tail

class Spec:
    """缓存 N=600 谱微分矩阵；单点 E(B) 求值"""
    def __init__(self, m, N=600):
        self.m = int(abs(m))
        r_lo = 0.23*self.m; r_hi = 3.1*self.m
        x, D1, D2 = cheb_d1d2(N)
        a, b = r_lo, r_hi
        r = (b-a)/2.0 * x + (a+b)/2.0
        scale = (b-a)/2.0
        self.T = (-0.5 * D2 / (scale*scale))[1:-1, 1:-1]
        self.r_in = r[1:-1]
    def E0(self, B):
        H = self.T + np.diag(V_eff(self.r_in, float(B), self.m))
        ev = np.real(eig(H, check_finite=False)[0])
        cand = ev[(ev > -1.0) & (ev < 1.0)]
        return cand.min() if len(cand) else np.nan

def Bstar_true(m, N=600, w=0.0265, newton_steps=3, h_rel=1e-5):
    """三次插值初值 + 真实 E(B) Newton"""
    cl = closed_1B(m)
    Bc = 1.0/cl
    x, D1, D2 = cheb_d1d2(N)
    a, b = 0.23*abs(m), 3.1*abs(m)
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = -0.5 * D2 / (scale*scale)
    r_in = r[1:-1]
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    Es = np.empty(7)
    for i, B in enumerate(Bs):
        H = T[1:-1, 1:-1] + np.diag(V_eff(r_in, float(B), m))
        ev = np.real(eig(H, check_finite=False)[0])
        cand = ev[(ev > -1.0) & (ev < 1.0)]
        Es[i] = cand.min() if len(cand) else np.nan
    B0 = float(Bs[3]); X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    xx = -c0/c1
    for _ in range(6):
        xx = xx - (c0+c1*xx+c2*xx**2+c3*xx**3)/(c1+2*c2*xx+3*c3*xx**2)
    B = B0 + xx
    # 真实 Newton（初值已近根；E' 中心差分）
    sp = Spec(m, N)
    for _ in range(newton_steps):
        h = h_rel * abs(B)
        e_plus = sp.E0(B + h); e_minus = sp.E0(B - h)
        e0 = sp.E0(B)
        de = (e_plus - e_minus) / (2.0*h)
        if not np.isfinite(de) or de == 0.0:
            break
        dB = -e0 / de
        B = B + dB
        if abs(dB) < 1e-15*abs(B):
            break
    return B

print("== P7-5e-173b 真实 E(B) Newton 提取（消除插值伪影）==", flush=True)
ms = np.arange(512, 1025, 32, dtype=float)
inv56 = 1.0/56.0
C13 = -13.0/128.0
Dcan = -103.0/5000.0
delta = np.empty(len(ms))
for i, m in enumerate(ms):
    cl = closed_1B(int(m))
    B = Bstar_true(-int(m))
    delta[i] = cl - 1.0/B
    print("  m=%5d  delta=%.9e" % (int(m), delta[i]), flush=True)

for name, jmax in [("3 参（1/56+C/m+D/m²）", 3), ("4 参（+E/m³）", 4)]:
    A = np.vstack([1.0/ms**j for j in range(jmax)]).T
    c, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
    resid = delta - A@c
    rms = float(np.sqrt(np.mean(resid**2)))
    Cfit = c[1]; Dfit = c[2] if jmax >= 3 else float('nan')
    print("\n%s（m≥512，17 点，真实 Newton）：RMS=%.2e" % (name, rms))
    print("  C = %+.12f   13/128 = %+.12f   差 %+.6f pct" % (Cfit, C13, (Cfit-C13)/abs(C13)*100))
    print("  D = %+.12f   103/5000 = %+.12f   差 %+.4f pct" % (Dfit, Dcan, (Dfit-Dcan)/abs(Dcan)*100))
    if jmax >= 4:
        print("  E = %+.6f" % c[3])

print("\n== 分段稳定性（真实 Newton，4 参）==")
for lo in [512, 640, 768, 896]:
    sel = ms >= lo
    A = np.vstack([1.0/ms[sel]**j for j in range(4)]).T
    c, _, _, _ = np.linalg.lstsq(A, delta[sel], rcond=None)
    resid = delta[sel] - A@c
    rms = float(np.sqrt(np.mean(resid**2)))
    print("  m>=%4d（%2d 点）C=%+.10f  D=%+.10f  RMS=%.2e   |D−103/5000|=%+.4f pct" % (
        lo, sel.sum(), c[1], c[2], rms, (c[2]-Dcan)/abs(Dcan)*100))
print("\n== 173b 补充：含 κ 模型判别（真实 Newton 17 点）==", flush=True)
ms17 = ms; d17 = delta.copy()
models = {
    "1/56+C/m+D/m²（无κ）":      (lambda m: [1.0/m, 1.0/m**2], 2),
    "1/56+C/m+D/m²+κ·m":         (lambda m: [1.0/m, 1.0/m**2, m], 3),
    "1/56+C/m+D/m²+E/m³+κ·m":    (lambda m: [1.0/m, 1.0/m**2, 1.0/m**3, m], 4),
    "1/56+C/m+D/m²+κ·m+F/m⁴":    (lambda m: [1.0/m, 1.0/m**2, m, 1.0/m**4], 4),
    "1/56+C/m+D/m²+E/m³（无κ）":  (lambda m: [1.0/m, 1.0/m**2, 1.0/m**3], 3),
}
for name, (bf, nk) in models.items():
    A = np.vstack(bf(ms17)).T
    c, _, _, _ = np.linalg.lstsq(A, d17, rcond=None)
    resid = d17 - A@c
    rms = float(np.sqrt(np.mean(resid**2)))
    tag = "  C=%+.10f（13/128 差 %+.6f pct）" % (c[0], (c[0]-C13)/abs(C13)*100)
    if nk >= 2:
        tag += "  D=%+.6f（103/5000=%+.6f，差 %+.2f pct）" % (c[1], Dcan, (c[1]-Dcan)/abs(Dcan)*100)
    if nk >= 3:
        tag += "  κ=%+.3e" % c[2]
    if nk >= 4:
        tag += "  次=%+.4f" % c[3]
    print("  %-28s RMS=%.2e %s" % (name, rms, tag))
print("exit 0", flush=True)
