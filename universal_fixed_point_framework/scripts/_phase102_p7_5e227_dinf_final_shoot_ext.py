# -*- coding: utf-8 -*-
"""
P7-5e-227：1/56 精确终判 + 独立数据源（打靶扩展 9 点 + 谱方法 N=1200 同 m 对照）
====================================================================
背景（226 定案后）：
  175/176（N=600 谱方法 + Newton 细化）对完整模型（C=13/128、D=41/2000、E=39/2000，
  δ∞=1/56 固定）残差 ~8e-10（225 通道 D）；
  但 223 打靶四点 / 164（N=1200 谱方法）四点对同一模型残差 +3.1e-7→+1.3e-6 递增（224 已登记）。
  → 175/176 与 164/打靶存在 ~1e-6 级 δ 系统差（164 与打靶相互一致 6.5e-9~7.5e-8），
    需判定谁有系统误差（175 的 N=600 离散化 vs 164 的 N=1200 / 打靶 DP45）。
  这直接影响 225/226 的 E 判别（175/176 数据源偏差）与 1/56 精确终判。
先验登记（计算前）：
  P1 数据一致性：打靶 vs 谱方法(N=1200) 同 m 8 点 δ 绝对差 ≤ 1e-7 级（m≤512）→ 两独立求解器交叉一致；
    另：谱方法 N=1200 @m=513 vs 175 N=600 @m=513 直接对比——|差| ≤ 1e-7 → 175 无系统误差（164/打靶 1e-6 残差另有原因）；
    |差| ≥ 1e-6 → 175/176 的 N=600 离散化系统差实锤（225/226 的 E 判别需数据源修正重审）。
  P2 1/56 终判：完整模型（C/D/E 锁定）δ∞ 自由单参拟合：
     |dev vs 1/56| < 0.003% → ★★★ δ∞=1/56 精确终判（打靶 + 谱双通道闭合）
     |dev| ∈ [0.003, 0.008)% → 1/56 近似值待修
     |dev| ≥ 0.008% → 1/56 有真实微修正
  P3 E 独立数据源复核：打靶 8 点对完整模型（δ∞=1/56、C/D 锁定）E 自由：
     |E_opt − 39/2000| < 1% → E=39/2000 获独立数据源支撑（锁定判别强化）
     |E_opt − 39/2000| ≥ 5% → 39/2000 疑为 175/176 数据源伪影（225/226 重审）
"""
import time, json, os
import numpy as np
from scipy.optimize import brentq
from multiprocessing import Pool
from scipy.linalg import eig

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
W = 0.0265
RTOL = 1e-9
ATOL = 1e-12
N_SP = 1200

# ---------- 打靶（DP45 标量版，223 复用） ----------
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

# ---------- 谱方法（Chebyshev N=1200，164 复用） ----------
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
        H = T[1:-1, 1:-1] + np.diag(V_eff_sh(r_in, float(B), m))
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

def worker_sp(m):
    Bs = Bstar_spectral(m)
    cl = closed_1B(m)
    return {"m": m, "Bstar": float(Bs), "delta": float(abs(1.0/Bs - cl))}

# ---------- 模型 ----------
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0

def model_full(m, dinf, C, D, E):
    return dinf - C/m - D/m**2 + E/m**3

if __name__ == "__main__":
    t0 = time.time()
    print("== P7-5e-227：1/56 精确终判 + 独立数据源（打靶扩展 9 点 + 谱方法 N=1200 同 m 对照）==", flush=True)
    ms = [-128, -256, -384, -512, -513, -640, -768, -896, -1024]

    # 打靶（复用 223 v6，9 点）
    t1 = time.time()
    print("  [Part A] 打靶 DP45 标量版 9 点（m=128..1024 + 513）…", flush=True)
    with Pool(4) as p:
        res_sh = p.map(worker_sh, ms)
    out_sh = {r["m"]: r for r in res_sh}
    print("  打靶完成：%d 点，耗时 %.0f s" % (len(out_sh), time.time()-t1), flush=True)

    # 谱方法（164 N=1200 复用，9 点）
    t2 = time.time()
    print("  [Part B] 谱方法 Chebyshev N=1200 同 9 点…", flush=True)
    with Pool(4) as p:
        res_sp = p.map(worker_sp, ms)
    out_sp = {r["m"]: r for r in res_sp}
    print("  谱方法完成：%d 点，耗时 %.0f s" % (len(out_sp), time.time()-t2), flush=True)

    # ---------- P1 数据一致性 ----------
    print("", flush=True)
    print("== P1 数据一致性：打靶 vs 谱方法(N=1200) 同 m δ ==", flush=True)
    max_dev_d = 0.0
    for m in ms:
        d_sh = out_sh[m]["delta"]; d_sp = out_sp[m]["delta"]
        dd = abs(d_sh - d_sp)
        max_dev_d = max(max_dev_d, dd)
        print("  m=%4d: 打靶 δ=%.10f  谱δ=%.10f  差=%.3e" % (abs(m), d_sh, d_sp, dd), flush=True)
    p1a = "通过（≤1e-7 级）——双求解器交叉一致" if max_dev_d <= 1e-7 else ("★ 超 1e-7（%.1e）——需查求解器差" % max_dev_d)
    print("  P1a 判据（同 m 差≤1e-7）：%s" % p1a, flush=True)

    # 175（N=600）@513 直接对比
    d175_513 = None
    try:
        j175 = json.load(open(os.path.join(BASE, "_phase102_p7_5e175_delta63.json"), encoding="utf-8"))
        ms175 = j175["m"]; ds175 = j175["delta"]
        idx = ms175.index(513.0) if 513.0 in ms175 else None
        if idx is None:
            idx = [i for i, x in enumerate(ms175) if abs(x - 513.0) < 1e-9]
            idx = idx[0] if idx else None
        d175_513 = ds175[idx] if idx is not None else None
    except Exception as e:
        print("  175 json 读取失败：%s" % e, flush=True)
    if d175_513 is not None:
        d_sp513 = out_sp[-513]["delta"]
        dd = abs(d175_513 - d_sp513)
        print("  ★ 175(N=600)@513: δ=%.10f  vs  谱(N=1200)@513: δ=%.10f  差=%.3e" % (d175_513, d_sp513, dd), flush=True)
        if dd >= 1e-6:
            p1b = "★ 175/176 的 N=600 离散化系统差实锤（%.1e）——225/226 的 E 判别建立在有偏数据上，需重审" % dd
        elif dd <= 1e-7:
            p1b = "175 无系统误差（差 %.1e）——164/打靶的 1e-6 残差另有原因（模型层）" % dd
        else:
            p1b = "175 与 N=1200 差 %.1e——中等级，需更多对照点" % dd
        print("  P1b 判别（175 vs N=1200 @513）：%s" % p1b, flush=True)
    else:
        p1b = "175 json 无 m=513 点，跳过"

    # ---------- 固定 δ∞=1/56 残差 ----------
    print("", flush=True)
    print("== 固定 δ∞=1/56 完整模型残差（C/D/E 锁定）==", flush=True)
    for tag, out in [("打靶", out_sh), ("谱N1200", out_sp)]:
        for lo, hi, lab in [(128, 512, "128..512"), (512, 1024, "512..1024"), (128, 1024, "128..1024")]:
            r = []
            for m in ms:
                mm = abs(m)
                if lo <= mm <= hi:
                    r.append(out[m]["delta"] - model_full(mm, INV56, C13, D41, E39))
            if r:
                rms = float(np.sqrt(np.mean(np.array(r)**2)))
                print("  %s [%s]: N=%d RMS=%.3e  max|r|=%.3e" % (tag, lab, len(r), rms, max(abs(x) for x in r)), flush=True)

    # ---------- P2 δ∞ 自由单参（完整模型） ----------
    print("", flush=True)
    print("== P2 1/56 终判：δ∞ 自由单参拟合（C/D/E 锁定）==", flush=True)
    for tag, out in [("打靶", out_sh), ("谱N1200", out_sp)]:
        for lo, hi, lab in [(128, 1024, "128..1024"), (512, 1024, "512..1024")]:
            msf = np.array([abs(m) for m in ms if lo <= abs(m) <= hi], dtype=float)
            ds = np.array([out[m]["delta"] for m in ms if lo <= abs(m) <= hi])
            X = np.vstack([np.ones_like(msf)]).T
            # 单参：δ∞ 最优 = mean(ds + C/m + D/m² − E/m³)
            target = ds + C13/msf + D41/msf**2 - E39/msf**3
            dinf_fit = float(np.mean(target))
            rms = float(np.sqrt(np.mean((dinf_fit - target)**2)))
            dev = (dinf_fit - INV56)/INV56*100
            print("  %s [%s]: δ∞_fit=%.10f  dev=%+.5f pct  RMS=%.2e" % (tag, lab, dinf_fit, dev, rms), flush=True)

    # ---------- 三参 {δ∞,C,D} 对照（223/164 口径） ----------
    print("", flush=True)
    print("== 三参 {δ∞,C,D} 对照（E 固定 39/2000，223/164 口径）==", flush=True)
    for tag, out in [("打靶", out_sh), ("谱N1200", out_sp)]:
        msf = np.array([abs(m) for m in ms], dtype=float)
        ds = np.array([out[m]["delta"] for m in ms])
        X3 = np.vstack([np.ones_like(msf), 1.0/msf, 1.0/msf**2]).T
        # 用 E 项已知修正：拟合 (ds − E39/m³)
        y = ds - E39/msf**3
        c3, _, _, _ = np.linalg.lstsq(X3, y, rcond=None)
        r3 = float(np.sqrt(np.mean((X3@c3 - y)**2)))
        dev3 = (c3[0]-INV56)/INV56*100
        print("  %s 三参：δ∞=%.10f（dev %+.5f pct） C=%.6f D=%.6f RMS=%.2e" % (tag, c3[0], dev3, c3[1], c3[2], r3), flush=True)

    # ---------- P3 E 独立复核（打靶 + 谱，δ∞=1/56、C/D 锁定） ----------
    print("", flush=True)
    print("== P3 E 独立数据源复核：E 自由单参（δ∞=1/56、C/D 锁定）==", flush=True)
    for tag, out in [("打靶", out_sh), ("谱N1200", out_sp)]:
        for lo, hi, lab in [(128, 1024, "128..1024"), (512, 1024, "512..1024"), (128, 512, "128..512")]:
            msf = np.array([abs(m) for m in ms if lo <= abs(m) <= hi], dtype=float)
            ds = np.array([out[m]["delta"] for m in ms if lo <= abs(m) <= hi])
            # E 单参：E_opt = mean(m³·(ds − 1/56 + C/m + D/m²))
            target = msf**3 * (ds - INV56 + C13/msf + D41/msf**2)
            E_fit = float(np.mean(target))
            rms = float(np.sqrt(np.mean((E_fit - target)**2)))
            dev39 = (E_fit - E39)/E39*100
            print("  %s [%s]: N=%d E_opt=+%.6f  vs 39/2000 %+.2f pct  RMS=%.2e" % (tag, lab, len(msf), E_fit, dev39, rms), flush=True)

    # ---------- 判别汇总 ----------
    print("", flush=True)
    print("== 判别汇总 ==", flush=True)
    # P2 判别用打靶 512..1024
    msf_hi = np.array([abs(m) for m in ms if 512 <= abs(m) <= 1024], dtype=float)
    ds_hi = np.array([out_sh[m]["delta"] for m in ms if 512 <= abs(m) <= 1024])
    target_hi = ds_hi + C13/msf_hi + D41/msf_hi**2 - E39/msf_hi**3
    dinf_hi = float(np.mean(target_hi))
    dev_hi = (dinf_hi - INV56)/INV56*100
    if abs(dev_hi) < 0.003:
        p2 = "★★★ δ∞=1/56 精确终判成立（打靶高 m 段 dev %+.5f pct）——1/56 是精确极限" % dev_hi
    elif abs(dev_hi) < 0.008:
        p2 = "★ δ∞ 接近但未闭合（dev %+.5f pct）——1/56 近似值待修" % dev_hi
    else:
        p2 = "★ δ∞ 未闭合（dev %+.5f pct）——1/56 有真实微修正" % dev_hi
    print("  P2（打靶 512..1024）：%s" % p2, flush=True)

    # P3 判别用打靶 512..1024
    E_fit_hi = float(np.mean(msf_hi**3 * (ds_hi - INV56 + C13/msf_hi + D41/msf_hi**2)))
    devE_hi = (E_fit_hi - E39)/E39*100
    if abs(devE_hi) < 1.0:
        p3 = "★★★ E=39/2000 获独立数据源支撑（打靶 E_opt=+%.6f，dev %+.2f pct）——225/226 的 39/2000 非 175/176 数据伪影" % (E_fit_hi, devE_hi)
    elif abs(devE_hi) < 5.0:
        p3 = "★ E 独立复核偏差 %+.2f pct（39/2000 仍兼容，需更多点）" % devE_hi
    else:
        p3 = "★ E=39/2000 疑为 175/176 数据源伪影（dev %+.2f pct）——225/226 重审" % devE_hi
    print("  P3（打靶 512..1024）：%s" % p3, flush=True)

    json.dump({
        "method": "shooting-DP45-scalar + cheb-N1200 (9 points 128..1024+513)",
        "ms": [abs(m) for m in ms], "runtime_s": time.time()-t0,
        "P1a_max_delta_dev_shoot_vs_spectral": float(max_dev_d),
        "P1b_175_vs_N1200_513": (None if d175_513 is None else float(abs(d175_513 - out_sp[-513]["delta"]))),
        "P2_dinf_free_hi_shooting": {"dinf": dinf_hi, "dev_vs_1o56_pct": float(dev_hi), "verdict": p2},
        "P3_E_free_hi_shooting": {"E_opt": float(E_fit_hi), "dev_vs_39o2000_pct": float(devE_hi), "verdict": p3},
        "shooting": {str(k): v for k, v in out_sh.items()},
        "spectral": {str(k): v for k, v in out_sp.items()},
        "ref_175_513_delta": d175_513,
    }, open(os.path.join(BASE, "_phase102_p7_5e227_dinf_final_shoot_ext.json"), "w",
           encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
