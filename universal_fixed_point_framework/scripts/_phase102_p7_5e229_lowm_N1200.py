# -*- coding: utf-8 -*-
"""
P7-5e-229：低 m 段干净数据（N=1200 谱方法，33..129 步 16）+ 175/176 系统差全貌
====================================================================
背景（228 后）：干净数据只有 m≥128（227 的 9 点）——C/D/ε 的低 m 段干净值缺失。
  低 m 段（33..65）C/D 信号强（1/m 项 ~1e-3）、E 信号 ~5e-7（m=33）可提取。
  同时 175/176 与 N=1200 在 m=33/49/65/81/97/113 重合——同 m 直接对比得系统差全貌。
先验登记（计算前）：
  P1 C 干净值（低 m 段 {δ∞,C,D} 三参）vs 13/128 差 <0.5% → C 锁定维持（干净数据验证）
  P2 D 干净值 vs 41/2000 差 <5% → D 锁定维持（干净数据验证）
  P3 ε 低 m 段（33..97）vs 227 高 m 段（128..512）+1.40e-6：差 <±0.5e-6 → ε 收敛
     （228 的窗口漂移 = E/F 吸收伪漂移）；差 >1e-6 → 模型残留结构确认
  P4 175/176 vs N=1200 同 m 系统差全貌：低 m 段差 ~1e-6 级 → Newton 细化系统差全链实锤
"""
import time, json, os
import numpy as np
from multiprocessing import Pool
from scipy.linalg import eig

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
W = 0.0265
N_SP = 1200
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0

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
    am = abs(m)
    tiny = 1.0/(7.0*2.0**am) if am <= 1000 else 0.0
    return am/2.0 + 1.0/7.0 + tiny

def Bstar_spectral(m, N=N_SP, w=W):
    cl = closed_1B(m)
    Bc = 1.0/cl
    r_lo = 0.23*abs(m); r_hi = 3.1*abs(m)
    x, D1, D2 = cheb_d1d2(N)
    a, b = r_lo, r_hi
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
    return B0 + xx

def worker(m):
    Bs = Bstar_spectral(m)
    cl = closed_1B(m)
    return {"m": m, "Bstar": float(Bs), "delta": float(abs(1.0/Bs - cl))}

if __name__ == "__main__":
    t0 = time.time()
    print("== P7-5e-229：低 m 段干净数据（N=1200，33..129 步 16）==", flush=True)
    ms_new = [-33, -49, -65, -81, -97, -113, -129]
    with Pool(4) as p:
        res = p.map(worker, ms_new)
    out = {abs(r["m"]): r for r in res}
    print("  计算完成：%d 点，耗时 %.0f s" % (len(out), time.time()-t0), flush=True)
    for m in sorted(out):
        print("  m=%3d  δ=%.10f  B*=%.10f" % (m, out[m]["delta"], out[m]["Bstar"]), flush=True)

    # 合并 227 的 9 点（m≥128）
    j227 = json.load(open(os.path.join(BASE, "_phase102_p7_5e227_dinf_final_shoot_ext.json"), encoding="utf-8"))
    for mm in j227["ms"]:
        if abs(mm) >= 128:
            out.setdefault(abs(mm), {"delta": j227["spectral"][str(-mm)]["delta"],
                                     "Bstar": j227["spectral"][str(-mm)]["Bstar"]})

    ms_all = sorted(out.keys())
    print("  合并谱方法干净数据：%d 点（33..1024）" % len(ms_all), flush=True)

    # ---------- 判别 1：C/D 干净值（低 m 段三参） ----------
    print("", flush=True)
    print("== P1/P2：低 m 段 {δ∞,C,D} 三参（E 固定 39/2000）==", flush=True)
    for lo, hi, lab in [(33, 129, "33..129"), (33, 97, "33..97"), (33, 161, "33..161")]:
        msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
        ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
        y = ds - E39/msf**3
        X3 = np.vstack([np.ones_like(msf), 1.0/msf, 1.0/msf**2]).T
        c3 = np.linalg.lstsq(X3, y, rcond=None)[0]
        r3 = float(np.sqrt(np.mean((X3@c3 - y)**2)))
        devC = (abs(c3[1]) - C13)/C13*100
        devD = (abs(c3[2]) - D41)/D41*100
        print("  [%s] N=%d δ∞=%.10f(dev %+.5f pct) C=%.7f(vs13/128 %+.2f pct) D=%.6f(vs41/2000 %+.2f pct) RMS=%.2e" %
              (lab, len(msf), c3[0], (c3[0]-INV56)/INV56*100, c3[1], devC, c3[2], devD, r3), flush=True)

    # ---------- 判别 2：ε 低 m 段单参 ----------
    print("", flush=True)
    print("== P3：ε 低 m 段 {δ∞} 单参（C/D/E 锁定）==", flush=True)
    for lo, hi, lab in [(33, 97, "33..97"), (33, 129, "33..129"), (33, 161, "33..161")]:
        msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
        ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
        tgt = ds + C13/msf + D41/msf**2 - E39/msf**3
        d1 = float(np.mean(tgt))
        r1 = float(np.sqrt(np.mean((tgt-d1)**2)))
        print("  [%s] N=%d ε=δ∞−1/56=%+.3e (dev %+.5f pct) RMS=%.2e" % (lab, len(msf), d1-INV56, (d1-INV56)/INV56*100, r1), flush=True)

    # ---------- 判别 3：E 低 m 段 {δ∞,E} 两参 ----------
    print("", flush=True)
    print("== E 低 m 段可提取性：{δ∞,E} 两参（C/D 锁定）==", flush=True)
    for lo, hi, lab in [(33, 97, "33..97"), (33, 129, "33..129")]:
        msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
        ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
        X2 = np.vstack([np.ones_like(msf), 1.0/msf**3]).T
        c2 = np.linalg.lstsq(X2, ds + C13/msf + D41/msf**2, rcond=None)[0]
        r2 = float(np.sqrt(np.mean((X2@c2 - (ds + C13/msf + D41/msf**2))**2)))
        print("  [%s] N=%d δ∞=%.10f(dev %+.5f pct) E=+%.6f(vs39 %+.2f pct) RMS=%.2e" %
              (lab, len(msf), c2[0], (c2[0]-INV56)/INV56*100, c2[1], (c2[1]-E39)/E39*100, r2), flush=True)

    # ---------- 判别 4：175/176 vs N=1200 同 m 系统差全貌 ----------
    print("", flush=True)
    print("== P4：175/176 vs N=1200 同 m 系统差全貌 ==", flush=True)
    j175 = json.load(open(os.path.join(BASE, "_phase102_p7_5e175_delta63.json"), encoding="utf-8"))
    j176 = json.load(open(os.path.join(BASE, "_phase102_p7_5e176_delta_lowm.json"), encoding="utf-8"))
    d175 = dict(zip([int(x) for x in j175["m"]], j175["delta"]))
    d176 = dict(zip([int(x) for x in j176["m"]], j176["delta"]))
    print("   m   | 175(N600) δ | 176(N600) δ | N1200 δ | Δ175 | Δ176")
    for m in sorted(ms_all):
        dd = out[m]["delta"]
        row = "  %4d |" % m
        if m in d175:
            row += " %.10f |" % d175[m]
            a175 = d175[m] - dd
        else:
            row += "      —      |"
            a175 = None
        if m in d176:
            row += " %.10f |" % d176[m]
            a176 = d176[m] - dd
        else:
            row += "      —      |"
            a176 = None
        row += " %.10f |" % dd
        row += (" %+.2e" % a175) if a175 is not None else "    —"
        row += (" | %+.2e" % a176) if a176 is not None else " |  —"
        print(row, flush=True)

    json.dump({"method": "cheb-N1200 low-m extension", "points": sorted(ms_all),
               "runtime_s": time.time()-t0, "out": {str(k): v for k, v in out.items()}},
              open(os.path.join(BASE, "_phase102_p7_5e229_lowm_N1200.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
