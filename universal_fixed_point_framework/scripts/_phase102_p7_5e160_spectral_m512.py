# -*- coding: utf-8 -*-
"""
P7-5e-160：谱方法全链重算 m=−33..−512（m 推进到 512，用户授权 C 终判）
================================================================
目标：C 终判（13/128 vs 0.1016 vs 0.10158 的 5-6 位判别）+ 双曲渐近在 m>256 的持续性。
先验登记（计算前）：
  P1 全链 33..512 三参 δ∞ vs 1/56：|dev| < 0.01% → 锁定维持
  P2 δ∞ 分段（33..256 vs 257..512）差 <0.02% → 双曲持续
  P6 C 终判（核心）：
     - C_m(m) = (1/B* − (m/2+1/8))·m 在 m=256/512 端（b 口径，排除 2^m 尾巴污染）
     - Richardson (256,512) 对：C = 2·C_m(512) − C_m(256)（消 D/m 一阶）
     - 判据：收敛 0.1015625±2e-5 → 13/128 锁定；0.101600±2e-5 → 127·8/10⁴ 维持；
             其他 → 需分析
  P7 运行级验证：33..256 逐点 vs 124 权威 JSON——一致（差 <1e-6 级）
参数：N=600（124 口径统一）、区间 [0.23|m|,3.1|m|]、窗口 ±2.65%
"""
import time, json, os
import numpy as np
from scipy.linalg import eig
from functools import lru_cache
from multiprocessing import Pool

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
N_SP = 600
W = 0.0265

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
    return abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))

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
    print("== P7-5e-160：谱方法全链 m=−33..−512（480 点，N=%d）==" % N_SP, flush=True)

    ms = list(range(-33, -513, -1))
    with Pool(8) as p:
        results = p.map(worker, ms)
    out = {r["m"]: r for r in results}
    dt = time.time()-t0
    print("  计算完成：%d 点，耗时 %.0f s" % (len(out), dt), flush=True)

    # P7 运行级验证：33..256 vs 124 权威
    ref124 = json.load(open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), encoding="utf-8"))["out"]
    devs_124 = []
    for m in range(-33, -257, -1):
        d = abs(out[m]["Bstar"] - ref124[str(m)]["Bstar"])/ref124[str(m)]["Bstar"]
        devs_124.append(d)
    max_dev_124 = float(max(devs_124))
    print("  P7 运行级验证（33..256 vs 124 权威）：最大 B* 偏差 %.2e → %s" % (
        max_dev_124, "一致" if max_dev_124 < 1e-6 else "★ 不一致——需诊断"), flush=True)

    # 双曲拟合
    ms_f = np.arange(33, 513, dtype=float)
    ds = np.array([out[m]["delta"] for m in range(-33, -513, -1)])
    def fit(ds_, ms_):
        X2 = np.vstack([np.ones(len(ms_)), 1.0/ms_]).T
        c2, _, _, _ = np.linalg.lstsq(X2, ds_, rcond=None)
        r2 = float(np.sqrt(np.mean((X2@c2-ds_)**2)))
        X3 = np.vstack([np.ones(len(ms_)), 1.0/ms_, 1.0/ms_**2]).T
        c3, _, _, _ = np.linalg.lstsq(X3, ds_, rcond=None)
        r3 = float(np.sqrt(np.mean((X3@c3-ds_)**2)))
        X4 = np.vstack([np.ones(len(ms_)), 1.0/ms_, 1.0/ms_**2, 1.0/ms_**3]).T
        c4, _, _, _ = np.linalg.lstsq(X4, ds_, rcond=None)
        r4 = float(np.sqrt(np.mean((X4@c4-ds_)**2)))
        return c2, r2, c3, r3, c4, r4

    inv56 = 1.0/56.0
    c2f, rms2, c3f, rms3, c4f, rms4 = fit(ds, ms_f)
    dev3 = (c3f[0]-inv56)/inv56*100
    print("", flush=True)
    print("== 全链 33..512（480 点）==", flush=True)
    print("  两参：δ∞=%.8f  C=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c2f[0], c2f[1], rms2, (c2f[0]-inv56)/inv56*100), flush=True)
    print("  三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c3f[0], c3f[1], c3f[2], rms3, dev3), flush=True)
    print("  四参：δ∞=%.8f  C=%.6f  D=%.6f  E=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c4f[0], c4f[1], c4f[2], c4f[3], rms4, (c4f[0]-inv56)/inv56*100), flush=True)

    # 分段判别（33..256 vs 257..512）
    seg1 = np.arange(33, 257, dtype=float)
    seg2 = np.arange(257, 513, dtype=float)
    d1 = np.array([out[m]["delta"] for m in range(-33, -257, -1)])
    d2 = np.array([out[m]["delta"] for m in range(-257, -513, -1)])
    _, _, c3h, r3h, c4h, r4h = fit(d1, seg1)
    _, _, c3t, r3t, c4t, r4t = fit(d2, seg2)
    print("", flush=True)
    print("== 分段判别 ==", flush=True)
    print("  33..256 三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (c3h[0], c3h[1], c3h[2], r3h), flush=True)
    print("  257..512 三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (c3t[0], c3t[1], c3t[2], r3t), flush=True)
    dseg_dinf = abs(c3h[0]-c3t[0])/c3t[0]*100
    print("  P2 δ∞ 分段差：%+.4f pct（判据 <0.02）→ %s" % (dseg_dinf, "通过——双曲持续" if dseg_dinf < 0.02 else "★ 未通过"), flush=True)
    dseg_C = abs(c3h[1]-c3t[1])/c3t[1]*100
    print("  C 分段差：%+.4f pct" % dseg_C, flush=True)

    # P6 C 终判（核心）：C_m(m) = (闭式 + 1/56 − 1/B*)·m —— 扣除 δ∞ 主项后的收敛序列
    #   1/B* ≈ 闭式 + 1/56 − C/m − D/m² → C_m = C + D/m + ... → 收敛到 C（正号）
    #   闭式 + 1/56 = m/2 + 1/7 + 1/56 + 1/(7·2^m) = m/2 + 9/56 + 1/(7·2^m)
    inv56 = 1.0/56.0
    c13_128 = 13.0/128.0
    c1016 = 0.1016
    c10158 = 0.10158   # 147: h(2)−1/128
    def Cm(m):
        invB = 1.0/out[m]["Bstar"]
        clp = abs(m)/2.0 + 9.0/56.0 + 1.0/(7.0*2.0**abs(m))
        return (clp - invB) * abs(m)
    print("", flush=True)
    print("== P6 C 终判（C_m = (闭式+1/56 − 1/B*)·m，收敛到 C）==", flush=True)
    seq = [64, 128, 256, 384, 512]
    vals = {}
    for m in seq:
        vals[m] = Cm(-m)
        print("  C_m(m=%d) = %.10f" % (m, vals[m]), flush=True)
    # Richardson (256,512) 对（消 D/m）
    C_rich = 2.0*vals[512] - vals[256]
    print("  Richardson (256,512)：C = 2·C(512) − C(256) = %.10f" % C_rich, flush=True)
    # (384,512) 对（更近端）
    C_rich2 = 512.0/(512.0-384.0)*vals[512] - 384.0/(512.0-384.0)*vals[384]
    print("  Richardson (384,512)：C = %.10f" % C_rich2, flush=True)
    # 偏差
    print("  vs 13/128 = %.10f：差 %+.6f pct" % (c13_128, (C_rich-c13_128)/c13_128*100), flush=True)
    print("  vs 0.1016 = %.10f：差 %+.6f pct" % (c1016, (C_rich-c1016)/c1016*100), flush=True)
    print("  vs 0.10158 = %.10f：差 %+.6f pct" % (c10158, (C_rich-c10158)/c10158*100), flush=True)
    # 收敛判定（Richardson 精度 ~ D²/(m²) 量级；用 C(512) 与 C_rich 差估不确定度）
    unc = abs(vals[512] - C_rich)
    print("  不确定度估计（|C(512)−C_rich|）：%.3e" % unc, flush=True)
    if abs(C_rich - c13_128) < 2.0e-5:
        c_verdict = "★★★ C = 13/128 锁定（Richardson 收敛 %+.2e）" % (C_rich-c13_128)
    elif abs(C_rich - c1016) < 2.0e-5:
        c_verdict = "★★★ C = 0.1016 = 127·8/10⁴ 维持（%+.2e）" % (C_rich-c1016)
    else:
        c_verdict = "★ C 需分析（Richardson = %.8f，13/128 差 %+.4f pct，0.1016 差 %+.4f pct）" % (
            C_rich, (C_rich-c13_128)/c13_128*100, (C_rich-c1016)/c1016*100)
    print("  判别：%s" % c_verdict, flush=True)

    # 三参 vs 四参 δ∞ 稳定性（全链）
    d34 = abs(c4f[0]-c3f[0])/c3f[0]*100
    print("  P1 三/四参 δ∞ 差：%+.4f pct（<0.005 → 三参最佳）" % d34, flush=True)
    verdict = "★★★ δ∞ 锁定 1/56 维持（三参 %+.4f pct）" % dev3 if abs(dev3) < 0.01 else "★ 需分析（%+.4f pct）" % dev3
    print("  判别：%s" % verdict, flush=True)

    # 落盘
    json.dump({"N": N_SP, "range": "-33..-512", "n_points": len(out), "runtime_s": dt,
               "fit_3p_full": {"d_inf": float(c3f[0]), "C": float(c3f[1]), "D": float(c3f[2]), "rms": rms3, "dev_vs_1o56_pct": float(dev3)},
               "fit_4p_full": {"d_inf": float(c4f[0]), "C": float(c4f[1]), "D": float(c4f[2]), "E": float(c4f[3]), "rms": rms4},
               "seg_33_256_3p": {"d_inf": float(c3h[0]), "C": float(c3h[1]), "D": float(c3h[2]), "rms": r3h},
               "seg_257_512_3p": {"d_inf": float(c3t[0]), "C": float(c3t[1]), "D": float(c3t[2]), "rms": r3t},
               "Cm_seq": {str(k): float(v) for k, v in vals.items()},
               "C_richardson_256_512": float(C_rich), "C_richardson_384_512": float(C_rich2),
               "C_unc_est": float(unc), "C_verdict": c_verdict,
               "check_P2_seg_dinf_pct": float(dseg_dinf), "check_C_seg_pct": float(dseg_C),
               "check_P7_max_dev_vs_124": float(max_dev_124),
               "verdict_dinf": verdict,
               "out": {str(k): v for k, v in out.items()}},
              open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("", flush=True)
    print("JSON 落盘 OK exit 0", flush=True)
