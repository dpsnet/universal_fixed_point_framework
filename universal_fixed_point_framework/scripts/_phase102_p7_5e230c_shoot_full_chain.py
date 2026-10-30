# -*- coding: utf-8 -*-
"""
P7-5e-230c：打靶全链干净数据（低 m 段 33..129 步 16 扩展 + 227 打靶 9 点合并，16 点）
====================================================================
背景（230 判定）：打靶（DP45+brentq 1e-12）是干净真值通道（@513 与 N=1200 差 1.2e-7、
  与 175 差 1.37e-6）；N=1200 高 m 段三次拟合残差（1e-7~4e-7）污染 227b/228 的 ε 判别。
  本脚本：打靶扩展低 m 段 7 点 + 227 打靶 9 点 → 16 点打靶全链 → C/D/E/ε 判别。
先验：P1 打靶全链 {δ∞,C,D} 三参 C vs 13/128 <0.5% → C 双通道确认；P2 ε 打靶全链
  窗口一致性（33..1024 vs 128..1024 差 <0.5e-6）→ ε 锁定尝试（若 N=1200 的漂移是
  三次拟合残差所致，打靶版应收敛）。
"""
import time, json, os
import numpy as np
from scipy.optimize import brentq
from multiprocessing import Pool

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
W = 0.0265
ATOL = 1e-13; RTOL = 1e-13
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0

def V_eff_sh(r, B, m):
    t = m + 0.5*B*r*r
    return t*t/(2.0*r*r) - 1.0/r

def closed_1B(m):
    am = abs(m)
    tiny = 1.0/(7.0*2.0**am) if am <= 1000 else 0.0
    return am/2.0 + 1.0/7.0 + tiny

def shoot_wall(E, r_lo, r_hi, B, m):
    y0, y1 = 0.0, 1.0
    r = float(r_lo)
    span = r_hi - r_lo
    h = span/200.0
    hmin = span/1e7
    nnode = 0
    prev = 0.0
    while r < r_hi:
        if r + h > r_hi:
            h = r_hi - r
        Vr = V_eff_sh(r, B, m)
        k1p = y1; k1f = 2.0*(Vr - E)*y0
        r2 = r + h*0.2
        s2p = y0 + h*0.2*k1p; s2v = y1 + h*0.2*k1f
        k2p = s2v; k2f = 2.0*(V_eff_sh(r2, B, m) - E)*s2p
        r3 = r + h*0.3
        s3p = y0 + h*(0.075*k1p + 0.225*k2p); s3v = y1 + h*(0.075*k1f + 0.225*k2f)
        k3p = s3v; k3f = 2.0*(V_eff_sh(r3, B, m) - E)*s3p
        r4 = r + h*0.8
        s4p = y0 + h*(44.0/45.0*k1p - 56.0/15.0*k2p + 32.0/9.0*k3p)
        s4v = y1 + h*(44.0/45.0*k1f - 56.0/15.0*k2f + 32.0/9.0*k3f)
        k4p = s4v; k4f = 2.0*(V_eff_sh(r4, B, m) - E)*s4p
        r5 = r + h*(8.0/9.0)
        s5p = y0 + h*(19372.0/6561.0*k1p - 25360.0/2187.0*k2p + 64448.0/6561.0*k3p - 212.0/729.0*k4p)
        s5v = y1 + h*(19372.0/6561.0*k1f - 25360.0/2187.0*k2f + 64448.0/6561.0*k3f - 212.0/729.0*k4f)
        k5p = s5v; k5f = 2.0*(V_eff_sh(r5, B, m) - E)*s5p
        r6 = r + h
        s6p = y0 + h*(9017.0/3168.0*k1p - 355.0/33.0*k2p + 46732.0/5247.0*k3p + 49.0/176.0*k4p - 5103.0/18656.0*k5p)
        s6v = y1 + h*(9017.0/3168.0*k1f - 355.0/33.0*k2f + 46732.0/5247.0*k3f + 49.0/176.0*k4f - 5103.0/18656.0*k5f)
        k6p = s6v; k6f = 2.0*(V_eff_sh(r6, B, m) - E)*s6p
        r7 = r + h
        s7p = y0 + h*(35.0/384.0*k1p + 500.0/1113.0*k3p + 125.0/192.0*k4p - 2187.0/6784.0*k5p + 11.0/84.0*k6p)
        s7v = y1 + h*(35.0/384.0*k1f + 500.0/1113.0*k3f + 125.0/192.0*k4f - 2187.0/6784.0*k5f + 11.0/84.0*k6f)
        k7p = s7v; k7f = 2.0*(V_eff_sh(r6, B, m) - E)*s7p
        y5_0 = y0 + h*(35.0/384.0*k1p + 500.0/1113.0*k3p + 125.0/192.0*k4p - 2187.0/6784.0*k5p + 11.0/84.0*k6p)
        y5_1 = y1 + h*(35.0/384.0*k1f + 500.0/1113.0*k3f + 125.0/192.0*k4f - 2187.0/6784.0*k5f + 11.0/84.0*k6f)
        y4_0 = y0 + h*(5179.0/57600.0*k1p + 7571.0/16695.0*k3p + 393.0/640.0*k4p - 92097.0/339200.0*k5p + 187.0/2100.0*k6p + 1.0/40.0*k7p)
        y4_1 = y1 + h*(5179.0/57600.0*k1f + 7571.0/16695.0*k3f + 393.0/640.0*k4f - 92097.0/339200.0*k5f + 187.0/2100.0*k6f + 1.0/40.0*k7f)
        err = max(abs(y5_0 - y4_0)/(ATOL + RTOL*max(abs(y5_0), abs(y4_0))),
                  abs(y5_1 - y4_1)/(ATOL + RTOL*max(abs(y5_1), abs(y4_1))))
        if err > 1.0 and h > hmin:
            h *= max(0.2, 0.9*(1.0/err)**0.2)
            continue
        if prev != 0.0 and y5_0 != 0.0 and prev*y5_0 < 0.0:
            nnode += 1
        prev = y5_0
        y0, y1 = y5_0, y5_1
        r = r + h
        scl = abs(y0)
        if abs(y1) > scl:
            scl = abs(y1)
        if scl > 0.0:
            y0 /= scl; y1 /= scl
        if err < 0.5:
            h = min(h*1.5, span/50.0)
    return y0, nnode

def E0_shooting(B, m, r_lo, r_hi):
    for (E_low, E_hi, step) in [(-0.01, 0.011, 0.0001), (-0.1, 0.101, 0.001)]:
        nE = int((E_hi - E_low)/step) + 1
        prev_psi = None; prev_E = None
        for i in range(nE):
            E = E_low + step*i
            psi, nn = shoot_wall(E, r_lo, r_hi, B, m)
            if prev_psi is not None and prev_psi*psi < 0.0:
                Eroot = brentq(lambda e: shoot_wall(e, r_lo, r_hi, B, m)[0],
                               prev_E, E, xtol=1e-12, rtol=1e-12)
                _, nn2 = shoot_wall(Eroot, r_lo, r_hi, B, m)
                if nn2 == 0:
                    return Eroot
            prev_psi, prev_E = psi, E
    raise RuntimeError("打靶未定位基态（m=%d B=%.6f）" % (m, B))

def Bstar_shooting(m):
    cl = closed_1B(m)
    Bc = 1.0/cl
    r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
    Bs = [Bc*(1-W) + 2.0*W*Bc*i/6.0 for i in range(7)]
    Es = [E0_shooting(B, m, r_lo, r_hi) for B in Bs]
    B0 = Bs[3]; X = [b - B0 for b in Bs]
    Xn = np.array(X); En = np.array(Es)
    A = np.vstack([np.ones_like(Xn), Xn, Xn**2, Xn**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, En, rcond=None)
    c0, c1, c2, c3 = coef
    xx = -c0/c1
    for _ in range(6):
        xx = xx - (c0+c1*xx+c2*xx**2+c3*xx**3)/(c1+2*c2*xx+3*c3*xx**2)
    return B0 + xx, Bs, Es

def worker_sh(m):
    Bs, Bgrid, Es = Bstar_shooting(m)
    cl = closed_1B(m)
    return {"m": m, "Bstar": float(Bs), "delta": float(abs(1.0/Bs - cl))}

if __name__ == "__main__":
    t0 = time.time()
    print("== P7-5e-230c：打靶全链干净数据（低 m 段扩展 + 227 合并）==", flush=True)
    ms_low = [-33, -49, -65, -81, -97, -113, -129]
    with Pool(4) as p:
        res = p.map(worker_sh, ms_low)
    print("  低 m 段打靶完成（7 点，%.0f s）" % (time.time()-t0), flush=True)
    out = {abs(r["m"]): r for r in res}
    for m in sorted(out):
        print("  m=%3d  δ=%.10f  B*=%.10f" % (m, out[m]["delta"], out[m]["Bstar"]), flush=True)

    j227 = json.load(open(os.path.join(BASE, "_phase102_p7_5e227_dinf_final_shoot_ext.json"), encoding="utf-8"))
    for mm in j227["ms"]:
        out.setdefault(abs(mm), {"delta": j227["shooting"][str(-mm)]["delta"],
                                 "Bstar": j227["shooting"][str(-mm)]["Bstar"]})
    ms_all = sorted(out.keys())
    print("  打靶全链干净数据：%d 点（33..1024）" % len(ms_all), flush=True)

    def fit(lo, hi, cols, y_shift=None):
        msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
        ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
        y = ds.copy()
        if y_shift is not None:
            y = y + y_shift(msf)
        X = np.vstack(cols(msf)).T
        c = np.linalg.lstsq(X, y, rcond=None)[0]
        rms = float(np.sqrt(np.mean((y - X@c)**2)))
        return msf, c, rms

    print("", flush=True)
    print("== C/D 三参（E 固定 39/2000）==", flush=True)
    for lo, hi, lab in [(33, 129, "33..129"), (33, 161, "33..161"), (33, 256, "33..256"), (33, 1024, "33..1024")]:
        msf, c, r = fit(lo, hi, lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2],
                        lambda m: -E39/m**3)
        print("  [%s] N=%d δ∞=%.10f(dev %+.5f pct) C=%.7f(vs13/128 %+.3f pct) D=%.6f(vs41/2000 %+.2f pct) RMS=%.2e" %
              (lab, len(msf), c[0], (c[0]-INV56)/INV56*100, c[1], (c[1]-C13)/C13*100, c[2], (c[2]-D41)/D41*100, r), flush=True)

    print("", flush=True)
    print("== ε {δ∞} 单参（C/D/E 锁定）窗口一致性 ==", flush=True)
    eps = {}
    for lo, hi, lab in [(33, 129, "33..129"), (33, 256, "33..256"), (33, 512, "33..512"), (33, 1024, "33..1024"),
                        (128, 1024, "128..1024"), (512, 1024, "512..1024")]:
        msf, c, r = fit(lo, hi, lambda m: [np.ones_like(m)],
                        lambda m: C13/m + D41/m**2 - E39/m**3)
        eps[lab] = (c[0]-INV56, r)
        print("  [%s] ε=δ∞−1/56=%+.3e (dev %+.5f pct) RMS=%.2e" % (lab, c[0]-INV56, (c[0]-INV56)/INV56*100, r), flush=True)

    print("", flush=True)
    print("== E 两参（C/D 锁定）低 m 段 ==", flush=True)
    for lo, hi, lab in [(33, 129, "33..129"), (33, 256, "33..256")]:
        msf, c, r = fit(lo, hi, lambda m: [np.ones_like(m), 1.0/m**3],
                        lambda m: C13/m + D41/m**2)
        print("  [%s] N=%d δ∞=%.10f(dev %+.5f pct) E=+%.6f(vs39 %+.2f pct) RMS=%.2e" %
              (lab, len(msf), c[0], (c[0]-INV56)/INV56*100, c[1], (c[1]-E39)/E39*100, r), flush=True)

    json.dump({"method": "shooting DP45 low-m extension + 227 shoot merge", "points": ms_all,
               "runtime_s": time.time()-t0, "out": {str(k): v for k, v in out.items()},
               "eps_windows": eps},
              open(os.path.join(BASE, "_phase102_p7_5e230c_shoot_full_chain.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
