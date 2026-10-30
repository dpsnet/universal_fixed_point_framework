# -*- coding: utf-8 -*-
"""
P7-5e-176: 低 m 段加密判别——41/2000 vs 103/5000 优势源定位
================================================================
175 系列发现：41/2000 零自由 RMS 优 103/5000 达 2.5 倍，但优势集中于 m<129 段
（175 数据 m=33..1009 step16，m<129 仅 6 点）。
本步：真实 Newton 加密 m=17..127（step 2，56 点）+ 复用 175 json 62 点，判别：
  1. 加密段（m=17..129）逐点残差：41/2000 vs 103/5000 归属定位
  2. 分段稳定性细化：17..32 / 33..64 / 65..128 / 129..256 / 257+
  3. 零自由 RMS 全链对照
  4. 自由四参拟合（低 m 段 vs 全链）——E 项在低 m 段贡献大，E 精度提升判别
     （注意：m=15..32 是 129 标注的过渡尾迹带，低 m 四参可能被过渡偏移污染——分段评估）
  5. 1/m^4 残差 F 判别（加密段）
输出 56 点数据到 _phase102_p7_5e176_delta_lowm.json 供复用。
"""
import numpy as np, json, os
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

def Bstar_true(m, N=600, w=0.0265, newton_steps=3, h_rel=1e-5):
    cl = closed_1B(m)
    Bc = 1.0/cl
    x, D1, D2 = cheb_d1d2(N)
    a, b = 0.23*abs(m), 3.1*abs(m)
    r = (b-a)/2.0 * x + (a+b)/2.0
    scale = (b-a)/2.0
    T = (-0.5 * D2 / (scale*scale))[1:-1, 1:-1]
    r_in = r[1:-1]
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    Es = np.empty(7)
    for i, B in enumerate(Bs):
        H = T + np.diag(V_eff(r_in, float(B), m))
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
    for _ in range(newton_steps):
        h = h_rel * abs(B)
        e_p = np.real(eig(T + np.diag(V_eff(r_in, float(B+h), m)), check_finite=False)[0])
        e_m = np.real(eig(T + np.diag(V_eff(r_in, float(B-h), m)), check_finite=False)[0])
        e_0 = np.real(eig(T + np.diag(V_eff(r_in, float(B), m)), check_finite=False)[0])
        cp = e_p[(e_p > -1.0) & (e_p < 1.0)]; cm = e_m[(e_m > -1.0) & (e_m < 1.0)]
        c0v = e_0[(e_0 > -1.0) & (e_0 < 1.0)]
        if len(cp) == 0 or len(cm) == 0 or len(c0v) == 0:
            break
        de = (cp.min() - cm.min()) / (2.0*h)
        if not np.isfinite(de) or de == 0.0:
            break
        dB = -c0v.min() / de
        B = B + dB
        if abs(dB) < 1e-15*abs(B):
            break
    return B

C13 = -13.0/128.0
inv56 = 1.0/56.0

def rms_of(dv, basev):
    return float(np.sqrt(np.mean((dv - basev)**2)))

def fit(dv, ms_, cols):
    A = np.vstack(cols(ms_)).T
    c, _, _, _ = np.linalg.lstsq(A, dv, rcond=None)
    resid = dv - A@c
    return c, float(np.sqrt(np.mean(resid**2)))

mA = lambda m: (1.0/m**2 - 1.0/m**3)
c41 = 41.0/2000.0
c103 = 103.0/5000.0

base = os.path.dirname(os.path.abspath(__file__))

# 读 175 json（m=33..1009 step16, 62 点）
with open(os.path.join(base, "_phase102_p7_5e175_delta63.json")) as f:
    d175 = json.load(f)
ms175 = np.array(d175["m"]); d175v = np.array(d175["delta"])

print("== P7-5e-176 低 m 加密（m=17..127 step2，56 点真实 Newton）==", flush=True)
msL = np.arange(17, 128, 2, dtype=float)   # 17..127
dL = np.empty(len(msL))
for i, m in enumerate(msL):
    cl = closed_1B(int(m))
    B = Bstar_true(-int(m))
    dL[i] = cl - 1.0/B
    if i % 8 == 0:
        print("  m=%5d  delta=%.9e" % (int(m), dL[i]), flush=True)

out = {"m": msL.tolist(), "delta": dL.tolist()}
with open(os.path.join(base, "_phase102_p7_5e176_delta_lowm.json"), "w") as f:
    json.dump(out, f)
print("  saved _phase102_p7_5e176_delta_lowm.json", flush=True)

# 合并全链
ms_all = np.concatenate([msL, ms175])
d_all = np.concatenate([dL, d175v])
print("  合并全链 %d 点（m=%d..%d）" % (len(ms_all), int(ms_all.min()), int(ms_all.max())))

# ---- 1. 加密段逐点残差（m=17..129）----
print("\n-- 1. 加密段逐点残差 r_c = delta - [1/56 - 13/128/m - c(1/m^2-1/m^3)] --")
print("   m     r41        r103      |r41|-|r103|   （负=41 优, 正=103 优）")
sel = ms_all <= 129.0
for m, dv in zip(ms_all[sel], d_all[sel]):
    r41 = dv - (inv56 + C13/m + (-c41)*mA(m))
    r103 = dv - (inv56 + C13/m + (-c103)*mA(m))
    mark = "41★" if abs(r41) < abs(r103) else "103★"
    print("  %5d  %+.3e  %+.3e  %+.3e  %s" % (int(m), r41, r103, abs(r41)-abs(r103), mark))

# ---- 2. 分段稳定性（零自由）----
print("\n-- 2. 分段稳定性（零自由 RMS 比 41/103；<1 表示 41 优）--")
for lo, hi in [(17, 32), (33, 64), (65, 128), (129, 256), (257, 10**6)]:
    sel = (ms_all >= lo) & (ms_all < hi)
    if sel.sum() == 0:
        continue
    r41 = rms_of(d_all[sel], inv56 + C13/ms_all[sel] + (-c41)*mA(ms_all[sel]))
    r103 = rms_of(d_all[sel], inv56 + C13/ms_all[sel] + (-c103)*mA(ms_all[sel]))
    print("   m=%4d..%-4d（%3d 点）41/2000 RMS=%.3e | 103/5000 RMS=%.3e | 比=%.2f" %
          (lo, hi, int(sel.sum()), r41, r103, r41/r103))

# ---- 3. 全链零自由 RMS 对照 ----
print("\n-- 3. 全链零自由 RMS（%d 点）--" % len(ms_all))
print("   41/2000 : RMS=%.3e" % rms_of(d_all, inv56 + C13/ms_all + (-c41)*mA(ms_all)))
print("   103/5000: RMS=%.3e" % rms_of(d_all, inv56 + C13/ms_all + (-c103)*mA(ms_all)))

# ---- 4. 自由四参拟合（低 m 段 vs 全链）----
print("\n-- 4. 自由四参拟合（D/E 精度判别；注意 m<33 过渡尾迹污染风险）--")
for lo, hi, tag in [(17, 10**6, "全链"), (33, 10**6, "m>=33（174c 口径）"),
                    (33, 129, "m=33..128（低 m 段）"), (17, 32, "m=17..32（过渡带）")]:
    sel = (ms_all >= lo) & (ms_all < hi)
    if sel.sum() < 4:
        continue
    c, rms = fit(d_all[sel], ms_all[sel],
                 lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3])
    print("   %-14s（%3d 点）C=%+.9f  D=%+.7f（41 距 %+.2f pct, 103 距 %+.2f pct）  E=%+.7f  RMS=%.3e" % (
        tag, int(sel.sum()), c[1], c[2],
        (c[2]+c41)/c41*100, (c[2]+c103)/c103*100, c[3], rms))

# ---- 5. 1/m^4 残差判别（加密段固定候选后）----
print("\n-- 5. 1/m^4 残差判别（m=17..128 段，固定候选后 F/m^4 拟合）--")
sel = (ms_all >= 17) & (ms_all < 129)
for dn, dv in [("41/2000", c41), ("103/5000", c103)]:
    resid = d_all[sel] - (inv56 + C13/ms_all[sel] + (-dv)*mA(ms_all[sel]))
    cf, rms = fit(resid, ms_all[sel], lambda m: [1.0/m**4])
    print("   c=%-9s F=%+.7f（1/32=%+.7f, 差 %+.2f pct）  RMS=%.3e" % (
        dn, cf[0], -1.0/32.0, (cf[0]+1.0/32.0)/(1.0/32.0)*100, rms))

# ---- 6. 全链 +F/m^4 四参（41 固定基）----
print("\n-- 6. 全链固定 41/2000 基 + F/m^4 自由 --")
sel = ms_all >= 17
c, rms = fit(d_all[sel], ms_all[sel],
             lambda m: [np.ones_like(m), 1.0/m, c41*(1.0/m**2 - 1.0/m**3), 1.0/m**4])
print("   固定 D=41/2000: C=%+.9f  F=%+.7f  RMS=%.3e" % (c[1], c[3], rms))
print("exit 0", flush=True)
