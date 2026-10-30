# -*- coding: utf-8 -*-
"""
P7-5e-124：谱方法全链重算 m=−33..−256（m 推进到 256，用户授权）
================================================================
目标：检验双曲渐近 δ(m)=1/56−C/m−D/m² 在 m>128 的持续性与系数稳定性。
  ★ 判别点（P7-5e-123 遗留）：
    - D 判别：分段 129..256 三参 D 若收敛 ~0.0188 → 候选升级；若漂移 → 模型依赖维持
    - E 重新判别：高 m 段（129..256）1/m³ 灵敏度提升 60 倍——E 真实应稳定、伪项应消失
先验登记（计算前）：
  P1 全链 33..256 三参 δ∞ vs 1/56：|dev| < 0.01% → 锁定维持
  P2 δ∞ 分段（33..128 vs 129..256）差 <0.02% → 双曲持续
  P3 D 判别：分段 129..256 三参 D vs 0.0188——偏差 <10% → D 候选获独立支持
  P4 E 重新判别：129..256 段四参 |E|：<0.005 → 伪项确认；~0.0157 → 真实（推翻 123）
  P5 运行级验证：33..128 逐点 vs 120 权威 JSON——一致（差 <1e-6 级）
参数：N=600（124a 收敛测试 m=−256 逐位一致 6.4e-14）、区间 [0.23|m|,3.1|m|]、窗口 ±2.65%
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
    print("== P7-5e-124：谱方法全链 m=−33..−256（224 点，N=%d）==" % N_SP, flush=True)

    ms = list(range(-33, -257, -1))
    with Pool(8) as p:
        results = p.map(worker, ms)
    out = {r["m"]: r for r in results}
    dt = time.time()-t0
    print("  计算完成：%d 点，耗时 %.0f s" % (len(out), dt), flush=True)

    # 运行级验证：33..128 逐点 vs 120 权威
    ref120 = json.load(open(os.path.join(BASE, "_phase102_p7_5e120_spectral_m128.json"), encoding="utf-8"))["out"]
    devs_120 = []
    for m in range(-33, -129, -1):
        d = abs(out[m]["Bstar"] - ref120[str(m)]["Bstar"])/ref120[str(m)]["Bstar"]
        devs_120.append(d)
    max_dev_120 = float(max(devs_120))
    print("  P5 运行级验证（33..128 vs 120 权威）：最大 B* 偏差 %.2e → %s" % (
        max_dev_120, "一致" if max_dev_120 < 1e-6 else "★ 不一致——需诊断"), flush=True)

    # 双曲拟合
    ms_f = np.arange(33, 257, dtype=float)
    ds = np.array([out[m]["delta"] for m in range(-33, -257, -1)])
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
    # 全链
    c2f, rms2, c3f, rms3, c4f, rms4 = fit(ds, ms_f)
    dev3 = (c3f[0]-inv56)/inv56*100
    print("", flush=True)
    print("== 全链 33..256（224 点）==", flush=True)
    print("  两参：δ∞=%.8f  C=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c2f[0], c2f[1], rms2, (c2f[0]-inv56)/inv56*100), flush=True)
    print("  三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c3f[0], c3f[1], c3f[2], rms3, dev3), flush=True)
    print("  四参：δ∞=%.8f  C=%.6f  D=%.6f  E=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c4f[0], c4f[1], c4f[2], c4f[3], rms4, (c4f[0]-inv56)/inv56*100), flush=True)

    # 分段判别
    seg1 = np.arange(33, 129, dtype=float)   # 33..128（120 衔接）
    seg2 = np.arange(129, 257, dtype=float)  # 129..256（新增）
    d1 = np.array([out[m]["delta"] for m in range(-33, -129, -1)])
    d2 = np.array([out[m]["delta"] for m in range(-129, -257, -1)])
    _, _, c3h, r3h, c4h, r4h = fit(d1, seg1)
    _, _, c3t, r3t, c4t, r4t = fit(d2, seg2)
    print("", flush=True)
    print("== 分段判别 ==", flush=True)
    print("  33..128 三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (c3h[0], c3h[1], c3h[2], r3h), flush=True)
    print("  33..128 四参：δ∞=%.8f  C=%.6f  D=%.6f  E=%.6f  RMS=%.2e" % (c4h[0], c4h[1], c4h[2], c4h[3], r4h), flush=True)
    print("  129..256 三参：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e" % (c3t[0], c3t[1], c3t[2], r3t), flush=True)
    print("  129..256 四参：δ∞=%.8f  C=%.6f  D=%.6f  E=%.6f  RMS=%.2e" % (c4t[0], c4t[1], c4t[2], c4t[3], r4t), flush=True)
    dseg_dinf = abs(c3h[0]-c3t[0])/c3t[0]*100
    print("  P2 δ∞ 分段差：%+.4f pct（判据 <0.02）→ %s" % (dseg_dinf, "通过——双曲持续" if dseg_dinf < 0.02 else "★ 未通过"), flush=True)
    dseg_C = abs(c3h[1]-c3t[1])/c3t[1]*100
    print("  C 分段差：%+.4f pct" % dseg_C, flush=True)
    dseg_D = abs(c3h[2]-c3t[2])/c3t[2]*100
    print("  D 分段差：%+.4f pct" % dseg_D, flush=True)
    # P3 D 判别：129..256 段 D vs 0.0188
    dev_D_tail = (c3t[2]-0.0188)/0.0188*100
    print("  P3 D 判别（129..256 三参 D vs 0.0188）：%+.4f pct → %s" % (
        dev_D_tail, "候选获独立支持" if abs(dev_D_tail) < 10 else "模型依赖维持"), flush=True)
    # P4 E 重新判别：129..256 段四参 E（正号口径 = −c4[3]）
    E_tail = -c4t[3]
    print("  P4 E 重新判别（129..256 四参 E，正号）：%.6f → %s" % (
        E_tail, "伪项确认（高 m 消失）" if abs(E_tail) < 0.005 else ("E 真实（推翻 123）" if abs(E_tail-0.015707) < 0.003 else "★ 需分析")), flush=True)
    E_head = -c4h[3]
    print("     33..128 段四参 E（正号）：%.6f（123 全链 0.0157 对照）" % E_head, flush=True)

    # 三参 vs 四参 δ∞ 稳定性（全链）
    d34 = abs(c4f[0]-c3f[0])/c3f[0]*100
    print("  P1 三/四参 δ∞ 差：%+.4f pct（<0.005 → 三参最佳）" % d34, flush=True)
    verdict = "★★★ δ∞ 锁定 1/56 维持（三参 %+.4f pct）" % dev3 if abs(dev3) < 0.01 else "★ 需分析（%+.4f pct）" % dev3
    print("  判别：%s" % verdict, flush=True)

    # 落盘
    json.dump({"N": N_SP, "range": "-33..-256", "n_points": len(out), "runtime_s": dt,
               "fit_3p_full": {"d_inf": float(c3f[0]), "C": float(c3f[1]), "D": float(c3f[2]), "rms": rms3, "dev_vs_1o56_pct": float(dev3)},
               "fit_4p_full": {"d_inf": float(c4f[0]), "C": float(c4f[1]), "D": float(c4f[2]), "E": float(c4f[3]), "rms": rms4},
               "seg_33_128_3p": {"d_inf": float(c3h[0]), "C": float(c3h[1]), "D": float(c3h[2]), "rms": r3h},
               "seg_129_256_3p": {"d_inf": float(c3t[0]), "C": float(c3t[1]), "D": float(c3t[2]), "rms": r3t},
               "seg_33_128_4p_E": float(E_head), "seg_129_256_4p_E": float(E_tail),
               "check_P2_seg_dinf_pct": float(dseg_dinf), "check_C_seg_pct": float(dseg_C),
               "check_D_seg_pct": float(dseg_D), "check_P3_D_tail_dev_pct": float(dev_D_tail),
               "check_P4_E_tail": float(E_tail), "check_P5_max_dev_vs_120": float(max_dev_120),
               "verdict": verdict,
               "out": {str(k): v for k, v in out.items()}},
              open(os.path.join(BASE, "_phase102_p7_5e124_spectral_m256.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("", flush=True)
    print("JSON 落盘 OK exit 0", flush=True)
