# -*- coding: utf-8 -*-
"""
P7-5e-223：δ∞ 打靶法独立通道闭合（回主线第 1 项）——v4 标量加速版
====================================================================
v1 失败：solve_ivp 单向前积分 overflow（势垒区指数增长）。
v2 失败：DP45 numpy 数组版 overflow 检测 + 性能过慢（纯 numpy 标量循环 ~20 min 未完）。
v3 修复：符号翻转定位基态（非本征 E 的积分波函数井内振荡，nn≥1；第一个符号翻转=基态）。
v4（本版）：全部标量运算（无 numpy 数组分配）+ RTOL 1e-9 + 每步线性缩放（恒正因子，保符号/零点）。
方程：ψ'' = 2(V_eff − E)ψ；同口径区间 [0.23|m|, 3.1|m|]；B 窗口 ±2.65%；7 点三次拟合求根。
先验登记（计算前）：
  P1 打靶 δ∞ vs 1/56：|dev| < 0.003 pct → ★★★ δ∞=1/56 打靶闭合（164/166 偏差为谱方法系统误差）
     |dev| ∈ [0.003, 0.008) → ★ 改善未闭合
     |dev| ≥ 0.008 pct → 1/56 为近似值，δ∞ 有真实微修正
  P2 打靶 B* vs 164 谱方法 B*：四点相对差 < 0.02 pct → 独立通道交叉一致
  P3 打靶 δ(m) 序列单调复现
"""
import time, json, os
from scipy.optimize import brentq
from multiprocessing import Pool

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
W = 0.0265
RTOL = 1e-9
ATOL = 1e-12

def V_eff(r, B, m):
    t = m + 0.5*B*r*r
    return t*t/(2.0*r*r) - 1.0/r

def closed_1B(m):
    return abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))

def shoot_wall(E, r_lo, r_hi, B, m):
    """标量 DP45 积分 ψ''=2(V−E)ψ，每步线性缩放。
    k_s = (stage ψ', 2(V−E)·stage ψ)；y5/y4 的 ψ 分量用 k_s[0]、ψ' 分量用 k_s[1]。"""
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
        Vr = V_eff(r, B, m)
        # k1
        k1p = y1
        k1f = 2.0*(Vr - E)*y0
        # k2 (c2=1/5, a21=1/5)
        r2 = r + h*0.2
        s2p = y0 + h*0.2*k1p
        s2v = y1 + h*0.2*k1f
        k2p = s2v
        k2f = 2.0*(V_eff(r2, B, m) - E)*s2p
        # k3 (c3=3/10, a31=3/40 a32=9/40)
        r3 = r + h*0.3
        s3p = y0 + h*(0.075*k1p + 0.225*k2p)
        s3v = y1 + h*(0.075*k1f + 0.225*k2f)
        k3p = s3v
        k3f = 2.0*(V_eff(r3, B, m) - E)*s3p
        # k4 (c4=4/5, a41=44/45 a42=-56/15 a43=32/9)
        r4 = r + h*0.8
        s4p = y0 + h*(44.0/45.0*k1p - 56.0/15.0*k2p + 32.0/9.0*k3p)
        s4v = y1 + h*(44.0/45.0*k1f - 56.0/15.0*k2f + 32.0/9.0*k3f)
        k4p = s4v
        k4f = 2.0*(V_eff(r4, B, m) - E)*s4p
        # k5 (c5=8/9, a51=19372/6561 a52=-25360/2187 a53=64448/6561 a54=-212/729)
        r5 = r + h*(8.0/9.0)
        s5p = y0 + h*(19372.0/6561.0*k1p - 25360.0/2187.0*k2p + 64448.0/6561.0*k3p - 212.0/729.0*k4p)
        s5v = y1 + h*(19372.0/6561.0*k1f - 25360.0/2187.0*k2f + 64448.0/6561.0*k3f - 212.0/729.0*k4f)
        k5p = s5v
        k5f = 2.0*(V_eff(r5, B, m) - E)*s5p
        # k6 (c6=1, a61=9017/3168 a62=-355/33 a63=46732/5247 a64=49/176 a65=-5103/18656)
        r6 = r + h
        s6p = y0 + h*(9017.0/3168.0*k1p - 355.0/33.0*k2p + 46732.0/5247.0*k3p + 49.0/176.0*k4p - 5103.0/18656.0*k5p)
        s6v = y1 + h*(9017.0/3168.0*k1f - 355.0/33.0*k2f + 46732.0/5247.0*k3f + 49.0/176.0*k4f - 5103.0/18656.0*k5f)
        k6p = s6v
        k6f = 2.0*(V_eff(r6, B, m) - E)*s6p
        # k7 (c7=1, a71=35/384 a73=500/1113 a74=125/192 a75=-2187/6784 a76=11/84)
        s7p = y0 + h*(35.0/384.0*k1p + 500.0/1113.0*k3p + 125.0/192.0*k4p - 2187.0/6784.0*k5p + 11.0/84.0*k6p)
        s7v = y1 + h*(35.0/384.0*k1f + 500.0/1113.0*k3f + 125.0/192.0*k4f - 2187.0/6784.0*k5f + 11.0/84.0*k6f)
        k7p = s7v
        k7f = 2.0*(V_eff(r6, B, m) - E)*s7p
        # y5（5 阶）：b5=[35/384,0,500/1113,125/192,-2187/6784,11/84,0]
        y5_0 = y0 + h*(35.0/384.0*k1p + 500.0/1113.0*k3p + 125.0/192.0*k4p - 2187.0/6784.0*k5p + 11.0/84.0*k6p)
        y5_1 = y1 + h*(35.0/384.0*k1f + 500.0/1113.0*k3f + 125.0/192.0*k4f - 2187.0/6784.0*k5f + 11.0/84.0*k6f)
        # y4（4 阶）：bs=[5179/57600,0,7571/16695,393/640,-92097/339200,187/2100,1/40]
        y4_0 = y0 + h*(5179.0/57600.0*k1p + 7571.0/16695.0*k3p + 393.0/640.0*k4p - 92097.0/339200.0*k5p + 187.0/2100.0*k6p + 1.0/40.0*k7p)
        y4_1 = y1 + h*(5179.0/57600.0*k1f + 7571.0/16695.0*k3f + 393.0/640.0*k4f - 92097.0/339200.0*k5f + 187.0/2100.0*k6f + 1.0/40.0*k7f)
        err = max(abs(y5_0 - y4_0)/(ATOL + RTOL*max(abs(y5_0), abs(y4_0))),
                  abs(y5_1 - y4_1)/(ATOL + RTOL*max(abs(y5_1), abs(y4_1))))
        if err > 1.0 and h > hmin:
            h *= max(0.2, 0.9*(1.0/err)**0.2)
            continue
        # 接受步
        if prev != 0.0 and y5_0 != 0.0 and prev*y5_0 < 0.0:
            nnode += 1
        prev = y5_0
        y0, y1 = y5_0, y5_1
        r = r + h
        # 每步线性缩放（恒正因子）
        scl = abs(y0)
        if abs(y1) > scl:
            scl = abs(y1)
        if scl > 0.0:
            y0 /= scl
            y1 /= scl
        if err < 0.5:
            h = min(h*1.5, span/50.0)
    return y0, nnode

def E0_shooting(B, m, r_lo, r_hi):
    """打靶求基态能量：B 窗口 ±2.65% 内 |E0|<0.01（诊断确认 ~1e-4 量级）。
    细扫找第一个 ψ(r_hi;E) 符号翻转（=基态，翻转区间极窄 ~2e-4），brentq 后验证零节点。"""
    for (E_low, E_hi, step) in [(-0.01, 0.011, 0.0001), (-0.1, 0.101, 0.001)]:
        nE = int((E_hi - E_low)/step) + 1
        prev_psi = None
        prev_E = None
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
    # 三次多项式最小二乘（普通方程，3×3 可解析）
    # A = [1, x, x^2, x^3]；正规方程 4×4 求解
    n = 7
    G = [[sum(x**p for x in X) for p in range(7)] for _ in range(7)]
    # 简化：用 numpy lstsq（一次性，快）
    import numpy as np
    Xn = np.array(X); En = np.array(Es)
    A = np.vstack([np.ones_like(Xn), Xn, Xn**2, Xn**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, En, rcond=None)
    c0, c1, c2, c3 = coef
    xx = -c0/c1
    for _ in range(6):
        xx = xx - (c0+c1*xx+c2*xx**2+c3*xx**3)/(c1+2*c2*xx+3*c3*xx**2)
    return B0 + xx, Bs, Es

def worker(m):
    Bs, Bgrid, Es = Bstar_shooting(m)
    cl = closed_1B(m)
    return {"m": m, "Bstar": float(Bs), "delta": float(abs(1.0/Bs - cl)),
            "E0_win": [float(e) for e in Es]}

if __name__ == "__main__":
    t0 = time.time()
    print("== P7-5e-223：δ∞ 打靶法独立通道闭合 v4 标量版（m=128/256/384/512）==", flush=True)
    ms = [-128, -256, -384, -512]
    with Pool(4) as p:
        results = p.map(worker, ms)
    out = {r["m"]: r for r in results}
    print("  打靶计算完成：%d 点，耗时 %.0f s" % (len(out), time.time()-t0), flush=True)

    import numpy as np
    ref164 = json.load(open(os.path.join(BASE, "_phase102_p7_5e164_dinf_N1200.json"), encoding="utf-8"))
    print("", flush=True)
    print("== P2 独立通道交叉验证：打靶 B* vs 谱方法 B*（164）==", flush=True)
    max_dev_b = 0.0
    for m in ms:
        B_spec = ref164["out"][str(m)]["Bstar"]
        B_shoot = out[m]["Bstar"]
        d = abs(B_shoot - B_spec)/B_spec
        max_dev_b = max(max_dev_b, d)
        print("  m=%d: 打靶 B*=%.10f  谱方法 B*=%.10f  差=%.3e (%.4f pct)" %
              (abs(m), B_shoot, B_spec, d, d*100), flush=True)
    p2_txt = "通过——独立通道交叉一致（<0.02 pct）" if max_dev_b*100 < 0.02 else "★ 偏差超 0.02 pct"
    print("  P2 判据（<0.02%%）：%s" % p2_txt, flush=True)

    print("", flush=True)
    print("== P1 打靶四点三参拟合 δ∞ ==", flush=True)
    ms_f = np.array([abs(m) for m in ms], dtype=float)
    ds = np.array([out[m]["delta"] for m in ms])
    X3 = np.vstack([np.ones(len(ms_f)), 1.0/ms_f, 1.0/ms_f**2]).T
    c3, _, _, _ = np.linalg.lstsq(X3, ds, rcond=None)
    r3 = float(np.sqrt(np.mean((X3@c3-ds)**2)))
    inv56 = 1.0/56.0
    dev3 = (c3[0]-inv56)/inv56*100
    print("  打靶三点：δ∞=%.10f  C=%.6f  D=%.6f  RMS=%.2e  → vs 1/56=%+.5f pct" %
          (c3[0], c3[1], c3[2], r3, dev3), flush=True)
    ref_dinf = ref164["P1_dinf_3p_N1200"]["d_inf"]
    ref_dev = ref164["P1_dinf_3p_N1200"]["dev_vs_1o56_pct"]
    print("  参考：164 谱方法 δ∞=%.10f（%+.5f pct）；166 高阶 δ∞=%.10f（%+.5f pct）" %
          (ref_dinf, ref_dev, 0.01786159799, (0.01786159799-inv56)/inv56*100), flush=True)
    if abs(dev3) < 0.003:
        p1_verdict = ("★★★ δ∞=1/56 打靶闭合（dev %+.5f pct）——164/166 偏差为谱方法系统误差"
                      % dev3)
    elif abs(dev3) < 0.008:
        p1_verdict = "★ δ∞ 改善但未闭合（dev %+.5f pct）——需更高阶或解析" % dev3
    else:
        p1_verdict = ("★ δ∞ 未闭合（dev %+.5f pct）——1/56 为近似值，真实微修正=%+.5f pct"
                      % (dev3, dev3))
    print("  P1 判别：%s" % p1_verdict, flush=True)

    print("", flush=True)
    print("== P3 δ(m) 单调性 ==", flush=True)
    seq = [out[m]["delta"] for m in ms]
    mono = all(seq[i] < seq[i+1] for i in range(len(seq)-1))
    print("  δ 序列：%s" % ["%.6f" % d for d in seq], flush=True)
    print("  P3 判据（单调升）：%s" % ("通过" if mono else "★ 破坏"), flush=True)

    d2 = (seq[-1]*ms_f[-1] - seq[-2]*ms_f[-2])/(ms_f[-1] - ms_f[-2])
    print("", flush=True)
    print("  两高 m 线性外推 δ∞(2p) = %.10f（dev vs 1/56 %+.5f pct）" %
          (d2, (d2-inv56)/inv56*100), flush=True)

    json.dump({"method": "shooting-DP45-scalar-scaled-rtol1e-9", "m": [abs(m) for m in ms],
               "runtime_s": time.time()-t0,
               "P1_dinf_3p_shooting": {"d_inf": float(c3[0]), "C": float(c3[1]), "D": float(c3[2]),
                                       "rms": r3, "dev_vs_1o56_pct": float(dev3),
                                       "dinf_2p_linear": float(d2), "verdict": p1_verdict},
               "P2_max_dev_Bstar_vs_spectral_pct": float(max_dev_b*100),
               "P3_monotone": mono,
               "ref_164_dinf": ref_dinf, "ref_166_dinf_high": 0.01786159799,
               "out": {str(k): v for k, v in out.items()}},
              open(os.path.join(BASE, "_phase102_p7_5e223_shooting_dinf_closure.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
