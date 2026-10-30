# -*- coding: utf-8 -*-
"""
P7-5e-164：δ∞ 独立高精度锁定——N=1200 重算四点（C_m 去污染通道）
================================================================
背景（160）：全链 33..512 N=600 三参 δ∞ = 1/56 + 0.0073%（离散化残差 vs 真实偏差未分）。
本步先验登记：
  P1 N=1200 四点三参 δ∞：|dev vs 1/56| 显著小于 N=600 的 0.0073% → 离散化残差（1/56 真实极限）
  P2 N=1200 vs N=600 的 δ∞ 差 < 0.005% → 收敛（离散化已饱和）
  P3 C_m(128/256/384/512) 与 160 N=600 对比：差 < 0.5% → C_m 不随 N 漂（污染来自 δ∞ 偏差被 m 放大）
  P4 δ∞ 独立锁定后 → C_m 去污染：C_m'(m) = (闭式+δ∞_new − 1/B*)·m 与 C 候选对比
参数：N=1200、区间 [0.23|m|,3.1|m|]、窗口 ±2.65%（与 160 同口径）
"""
import time, json, os
import numpy as np
from scipy.linalg import eig
from functools import lru_cache
from multiprocessing import Pool

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
N_SP = 1200
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
    print("== P7-5e-164：δ∞ 独立高精度锁定（N=%d，四点 128/256/384/512）==" % N_SP, flush=True)

    ms = [-128, -256, -384, -512]
    with Pool(8) as p:
        results = p.map(worker, ms)
    out = {r["m"]: r for r in results}
    dt = time.time()-t0
    print("  计算完成：%d 点，耗时 %.0f s" % (len(out), dt), flush=True)

    # 160 N=600 对比数据
    ref160 = json.load(open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), encoding="utf-8"))
    print("", flush=True)
    print("== P2 收敛对比：N=1200 vs N=600（160）==", flush=True)
    devs = []
    for m in ms:
        B_old = ref160["out"][str(m)]["Bstar"]
        d = abs(out[m]["Bstar"] - B_old)/B_old
        devs.append(d)
        print("  m=%d: B*(N1200)=%.10f  B*(N600)=%.10f  差=%.3e (%.4f pct)" %
              (m, out[m]["Bstar"], B_old, d, d*100), flush=True)
    max_dev = max(devs)
    p2_txt = "通过——离散化已饱和" if max_dev*100 < 0.005 else "★ 未饱和"
    print("  P2 判据（<0.005%%）：%s" % p2_txt, flush=True)

    # P1 三参拟合（四点）δ∞
    print("", flush=True)
    print("== P1 四点三参拟合（δ∞ 独立锁定）==", flush=True)
    ms_f = np.array([abs(m) for m in ms], dtype=float)
    ds = np.array([out[m]["delta"] for m in ms])
    X3 = np.vstack([np.ones(len(ms_f)), 1.0/ms_f, 1.0/ms_f**2]).T
    c3, _, _, _ = np.linalg.lstsq(X3, ds, rcond=None)
    r3 = float(np.sqrt(np.mean((X3@c3-ds)**2)))
    inv56 = 1.0/56.0
    dev3 = (c3[0]-inv56)/inv56*100
    print("  三参：δ∞=%.10f  C=%.6f  D=%.6f  RMS=%.2e  → vs 1/56=%+.5f pct" %
          (c3[0], c3[1], c3[2], r3, dev3), flush=True)
    # 160 全链三参
    f160 = ref160["fit_3p_full"]
    print("  160 全链三参：δ∞=%.10f（dev %+.4f pct）" % (f160["d_inf"], f160["dev_vs_1o56_pct"]), flush=True)
    d_dinf = abs(c3[0]-f160["d_inf"])/f160["d_inf"]*100
    print("  N1200 vs N600 δ∞ 差：%+.5f pct（P2 判据 <0.005）" % d_dinf, flush=True)
    # 判别：|dev3| 是否显著小于 0.0073%
    if abs(dev3) < 0.003:
        p1_verdict = "★★★ δ∞ 收敛向 1/56（dev {0:+.5f} pct < 160 的 0.0073%）——1/56 为真实极限，160 偏差为离散化残差".format(dev3)
    elif abs(dev3) < 0.0073:
        p1_verdict = "★ δ∞ 改善但未收敛（dev {0:+.5f} pct，介于 0.003-0.0073）——需更高 N 判别".format(dev3)
    else:
        p1_verdict = "★ δ∞ 未收敛（dev {0:+.5f} pct ≥ 160 的 0.0073%）——+0.0073% 为真实偏差，1/56 需修正".format(dev3)
    print("  P1 判别：%s" % p1_verdict, flush=True)

    # P3/P4 C_m 去污染
    print("", flush=True)
    print("== P3/P4 C_m 去污染 ==", flush=True)
    c13_128 = 13.0/128.0
    c1016 = 0.1016
    def Cm(m, d_inf):
        invB = 1.0/out[m]["Bstar"]
        clp = abs(m)/2.0 + 1.0/7.0 + d_inf + 1.0/(7.0*2.0**abs(m))
        return (clp - invB) * abs(m)
    print("  C_m(m)（用 1/56 作为 δ∞）：", flush=True)
    for m in ms:
        v = Cm(m, inv56)
        print("    m=%d: C_m=%.8f  (vs 13/128=%.8f 差 %+.4f pct；vs 0.1016 差 %+.4f pct)" %
              (abs(m), v, c13_128, (v-c13_128)/c13_128*100, (v-c1016)/c1016*100), flush=True)
    # Richardson (256,512)
    Cm512 = Cm(-512, inv56); Cm256 = Cm(-256, inv56)
    C_rich = 2.0*Cm512 - Cm256
    print("  Richardson (256,512) 用 1/56：C = %.8f" % C_rich, flush=True)
    print("    vs 13/128 差 %+.5f pct；vs 0.1016 差 %+.5f pct" %
          ((C_rich-c13_128)/c13_128*100, (C_rich-c1016)/c1016*100), flush=True)
    # 用 N1200 拟合 δ∞ 再算
    Cm512n = Cm(-512, c3[0]); Cm256n = Cm(-256, c3[0])
    C_rich_n = 2.0*Cm512n - Cm256n
    print("  Richardson 用 N1200 拟合 δ∞=%.10f：C = %.8f" % (c3[0], C_rich_n), flush=True)
    print("    vs 13/128 差 %+.5f pct；vs 0.1016 差 %+.5f pct" %
          ((C_rich_n-c13_128)/c13_128*100, (C_rich_n-c1016)/c1016*100), flush=True)
    # 160 C_m 对比（P3）
    print("  160 C_m（N600）：", flush=True)
    for m in [128, 256, 512]:
        v160 = ref160["Cm_seq"][str(m)]
        vnew = Cm(-m, inv56)
        print("    m=%d: N600=%.8f  N1200=%.8f  差 %+.4f pct" %
              (m, v160, vnew, (vnew-v160)/v160*100), flush=True)

    # 判别
    print("", flush=True)
    unc = abs(Cm512 - C_rich)
    if abs(C_rich - c13_128) < 2.0e-5:
        c_verdict = "★★★ C = 13/128 锁定（%+.2e）" % (C_rich-c13_128)
    elif abs(C_rich - c1016) < 2.0e-5:
        c_verdict = "★★★ C = 0.1016 维持（%+.2e）" % (C_rich-c1016)
    else:
        c_verdict = "★ C 仍开放（Richardson=%.8f，13/128 差 %+.4f pct，0.1016 差 %+.4f pct，unc=%.2e）" % (
            C_rich, (C_rich-c13_128)/c13_128*100, (C_rich-c1016)/c1016*100, unc)
    print("  C 判别：%s" % c_verdict, flush=True)

    json.dump({"N": N_SP, "points": [abs(m) for m in ms], "runtime_s": dt,
               "P1_dinf_3p_N1200": {"d_inf": float(c3[0]), "C": float(c3[1]), "D": float(c3[2]), "rms": r3,
                                     "dev_vs_1o56_pct": float(dev3), "verdict": p1_verdict},
               "P2_max_dev_N1200_vs_N600": float(max_dev),
               "C_m_with_1o56": {str(abs(m)): float(Cm(m, inv56)) for m in ms},
               "C_richardson_1o56": float(C_rich), "C_richardson_N1200_dinf": float(C_rich_n),
               "C_verdict": c_verdict, "unc": float(unc),
               "out": {str(k): v for k, v in out.items()}},
              open(os.path.join(BASE, "_phase102_p7_5e164_dinf_N1200.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
