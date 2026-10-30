# -*- coding: utf-8 -*-
"""
P7-5e-170：谱方法全链重算 m=−33..−1024（992 点，用户授权）
================================================================
前置：收敛测试已过（m=1024 单点 N=600 vs N=1200 差 3.45e-15——N=600 饱和）。
目标：
  P1 δ∞ 偏差身份判别（166 遗留）：m=1024 时 1/m 级残差减半——
     - 偏差收敛向 <1e-6 → (a) 截断伪影，1/56 精确
     - 偏差保持 ~1.3e-6（166 的 m≥256 五点 4.46e-6）→ (b) 真实修正
  P2 δ∞ 多窗口（m≥256/512/768/1024）漂移判别
  P3 C_m 延伸（768/1024）→ 13/128 数值再确认（169b 已解析锁定）
  P4 运行级验证：33..512 vs 160 权威（差 <1e-6）
先验登记（计算前）：
  - δ∞ = 1/56（121 锁定；偏差 ~1.3e-6 待判别）
  - C = 13/128（169b 解析锁定，数值再确认）
参数：N=600（160 口径统一）、区间 [0.23|m|,3.1|m|]、窗口 ±2.65%
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
    a = abs(m)
    tail = 1.0/(7.0*2.0**a) if a <= 120 else 0.0
    return a/2.0 + 1.0/7.0 + tail

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
    print("== P7-5e-170：谱方法全链 m=−33..−1024（992 点，N=%d）==" % N_SP, flush=True)
    ms = list(range(-33, -1025, -1))
    with Pool(8) as p:
        results = p.map(worker, ms)
    out = {r["m"]: r for r in results}
    dt = time.time()-t0
    print("  计算完成：%d 点，耗时 %.0f s" % (len(out), dt), flush=True)

    # P4 运行级验证：33..512 vs 160 权威
    ref160 = json.load(open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), encoding="utf-8"))["out"]
    devs = []
    for m in range(-33, -513, -1):
        d = abs(out[m]["Bstar"] - ref160[str(m)]["Bstar"])/ref160[str(m)]["Bstar"]
        devs.append(d)
    max_dev = float(max(devs))
    print("  P4 运行级验证（33..512 vs 160 权威）：最大 B* 偏差 %.2e → %s" % (
        max_dev, "一致" if max_dev < 1e-6 else "★ 不一致——需诊断"), flush=True)

    # P1/P2 δ∞ 偏差身份判别：多窗口 × 多阶模型
    inv56 = 1.0/56.0
    def fit_window(ms_, kmax=5):
        ds_ = np.array([out[m]["delta"] for m in range(-int(ms_[0]), -int(ms_[-1])-1, -1)])
        best = None
        for k in range(2, kmax+1):
            A = np.vstack([1.0/ms_**j for j in range(k)]).T
            c, _, _, _ = np.linalg.lstsq(A, ds_, rcond=None)
            r = float(np.sqrt(np.mean((A@c - ds_)**2)))
            if best is None or r < best[1]:
                best = (c, r, k)
        return best
    print("\n== P1/P2 δ∞ 多窗口 × 多阶模型（偏差身份判别）==", flush=True)
    rows = {}
    for lo in [128, 256, 384, 512, 768]:
        ms_ = np.arange(lo, 1025, dtype=float)
        c, r, k = fit_window(ms_)
        dev = (c[0]-inv56)/inv56*100
        rows[lo] = {"dinf": float(c[0]), "dev_pct": float(dev), "k": k, "rms": r, "abs_dev": float(abs(c[0]-inv56))}
        print("  m≥%4d（%d 点，%d 参）：δ∞=%.10f  vs 1/56 差 %+.4f pct（abs %.2e）RMS=%.1e" %
              (lo, len(ms_), k, c[0], dev, abs(c[0]-inv56), r), flush=True)
    # 判别：偏差随窗口增大是否收敛到 0
    devs_abs = [rows[lo]["abs_dev"] for lo in [512, 768]]
    if devs_abs[-1] < 1e-6:
        verdict_d = "★★ δ∞ 偏差收敛 <1e-6——(a) 截断伪影——1/56 精确锁定" 
    elif devs_abs[-1] < rows[512]["abs_dev"]*0.8:
        verdict_d = "★ δ∞ 偏差随窗口收敛中（%.2e → %.2e）——倾向截断伪影，未完全归零" % (rows[512]["abs_dev"], devs_abs[-1])
    else:
        verdict_d = "★ δ∞ 偏差未随窗口收敛（%.2e → %.2e）——(b) 真实修正候选维持" % (rows[512]["abs_dev"], devs_abs[-1])
    print("  判别：%s" % verdict_d, flush=True)

    # P3 C_m 延伸 + C 再确认
    print("\n== P3 C_m 延伸（C = (闭式+1/56 − 1/B*)·m）==", flush=True)
    def Cm(m):
        invB = 1.0/out[m]["Bstar"]
        clp = abs(m)/2.0 + 9.0/56.0 + (1.0/(7.0*2.0**abs(m)) if abs(m) <= 120 else 0.0)
        return (clp - invB) * abs(m)
    seq = [256, 384, 512, 768, 1024]
    vals = {}
    for m in seq:
        vals[m] = Cm(-m)
        print("  C_m(m=%4d) = %.10f" % (m, vals[m]), flush=True)
    c13 = 13.0/128.0
    C_rich_512_1024 = 2.0*vals[1024] - vals[512]
    C_rich_768_1024 = 1024.0/(1024.0-768.0)*vals[1024] - 768.0/(1024.0-768.0)*vals[768]
    print("  Richardson (512,1024)：C = %.10f（13/128 差 %+.6f pct）" % (C_rich_512_1024, (C_rich_512_1024-c13)/c13*100), flush=True)
    print("  Richardson (768,1024)：C = %.10f（13/128 差 %+.6f pct）" % (C_rich_768_1024, (C_rich_768_1024-c13)/c13*100), flush=True)

    # 落盘
    json.dump({"N": N_SP, "range": "-33..-1024", "n_points": len(out), "runtime_s": dt,
               "check_P4_max_dev_vs_160": float(max_dev),
               "dinf_windows": {str(k): v for k, v in rows.items()},
               "verdict_dinf_identity": verdict_d,
               "Cm_seq": {str(k): float(v) for k, v in vals.items()},
               "C_richardson_512_1024": float(C_rich_512_1024),
               "C_richardson_768_1024": float(C_rich_768_1024),
               "out": {str(k): v for k, v in out.items()}},
              open(os.path.join(BASE, "_phase102_p7_5e170_spectral_m1024.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("\nJSON 落盘 OK exit 0", flush=True)
