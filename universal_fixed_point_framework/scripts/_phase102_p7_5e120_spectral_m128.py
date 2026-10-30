# -*- coding: utf-8 -*-
"""
P7-5e-120：Chebyshev 谱方法全链重算 m=−33..−128（独立验证通道）
================================================================
目标：闭合 δ∞ vs 1/56 的 +0.048%（118 tridiag 强候选）→ 锁定判据 <0.01%。
先验登记（计算前）：
  主判据：最佳模型 δ∞ vs 1/56=0.017857142857——|dev| < 0.01% → ★★★ 锁定
  稳健性检验（先验 P1）：1/m³ 项不显著（四参 δ∞ vs 三参 δ∞ 差 <0.005%）→ 三参为最佳模型
  稳定性检验（先验 P2）：分段 33..96 与 97..128 的 δ∞ 差 <0.02%
  外推检验（先验 P3）：前半（33..96）三参拟合预测后半（97..128）δ，偏差 <1%
参数：N=600（收敛测试 600/900/1200 逐位一致差 <1e-12，效能最优）
      区间 [0.23|m|, 3.1|m|]（119 同构缩放：m=13 时 = [3,40] 验证形态）
      窗口 ±2.65% 7 点 + 三次多项式过零（与 118/119 同口径）
v2 修正（v1 符号 bug）：δ = abs(1/B* − cl)——118 口径（118 Bstar_3dr 返回 abs）；
      新增四参/分段/外推先验检验。
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
    print("== P7-5e-120：谱方法全链 m=−33..−128（N=%d，区间 [0.23|m|,3.1|m|]）==" % N_SP, flush=True)
    print("先验：δ∞ vs 1/56——<0.01 pct 锁定 / 0.01~0.05 pct 强候选维持 / ≥0.05 pct 降级", flush=True)

    ms = list(range(-33, -129, -1))
    with Pool(8) as p:
        results = p.map(worker, ms)
    out = {r["m"]: r for r in results}
    dt = time.time()-t0

    # 读 118 tridiag 对照
    ref118 = json.load(open(os.path.join(BASE, "_phase102_p7_5e118_m128_scan.json"), encoding="utf-8"))["out"]
    for m in out:
        t = ref118.get(str(m))
        out[m]["tridiag_delta"] = t["delta"] if t else None
        out[m]["dev_vs_tridiag_pct"] = ((out[m]["delta"]-t["delta"])/t["delta"]*100) if t else None

    print("", flush=True)
    print("逐点（谱方法 vs 118 tridiag）：", flush=True)
    for m in sorted(out, reverse=True):
        r = out[m]
        t = ref118.get(str(m))
        tag = ("  tridiag δ=%.7f  差 %+.2f pct" % (r["tridiag_delta"], r["dev_vs_tridiag_pct"])) if t else ""
        print("  m=%4d  B*=%.8f  1/B*=%.8f  δ=%.7f%s" % (m, r["Bstar"], 1.0/r["Bstar"], r["delta"], tag), flush=True)

    # 双曲精化 33..128（两参/三参/四参）
    ms_f = np.arange(33, 129, dtype=float)
    ds = np.array([out[m]["delta"] for m in range(-33, -129, -1)])
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
    c2f, rms2, c3f, rms3, c4f, rms4 = fit(ds, ms_f)

    inv56 = 1.0/56.0
    dev2 = (c2f[0]-inv56)/inv56*100
    dev3 = (c3f[0]-inv56)/inv56*100
    dev4 = (c4f[0]-inv56)/inv56*100
    print("", flush=True)
    print("== 谱方法双曲精化（33..128，96 点，总耗时 %.0f s）==" % dt, flush=True)
    print("  两参数：δ∞=%.8f  C=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c2f[0], c2f[1], rms2, dev2), flush=True)
    print("  三参数：δ∞=%.8f  C=%.6f  D=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c3f[0], c3f[1], c3f[2], rms3, dev3), flush=True)
    print("  四参数：δ∞=%.8f  C=%.6f  D=%.6f  E=%.6f  RMS=%.2e  → vs 1/56=%+.4f pct" % (c4f[0], c4f[1], c4f[2], c4f[3], rms4, dev4), flush=True)
    # 118 对照
    j118 = json.load(open(os.path.join(BASE, "_phase102_p7_5e118_m128_scan.json"), encoding="utf-8"))
    f2 = j118["fit_2p"]; f3 = j118["fit_3p"]
    print("  118 tridiag 对照：两参 δ∞=%.8f（%+.3f pct） 三参 δ∞=%.8f（%+.3f pct）" % (
        f2["d_inf"], (f2["d_inf"]-inv56)/inv56*100, f3["d_inf"], (f3["d_inf"]-inv56)/inv56*100), flush=True)
    print("  双通道 δ∞ 差（两参）：%+.4f pct（三参）：%+.4f pct" % (
        (c2f[0]-f2["d_inf"])/f2["d_inf"]*100, (c3f[0]-f3["d_inf"])/f3["d_inf"]*100), flush=True)

    # 先验 P1：1/m³ 项显著性（四参 vs 三参 δ∞）
    d34 = abs(c4f[0]-c3f[0])/c3f[0]*100
    print("  先验 P1（1/m³ 不显著，判据 |Δδ∞(4→3)|<0.005 pct）：%+.4f pct → %s" % (
        d34, "通过" if d34 < 0.005 else "★ 未通过（需 1/m³ 项）"), flush=True)
    # 先验 P2：分段稳定性 33..96 vs 97..128
    half = np.arange(33, 97, dtype=float)
    tail = np.arange(97, 129, dtype=float)
    dh = np.array([out[m]["delta"] for m in range(-33, -97, -1)])
    dtail = np.array([out[m]["delta"] for m in range(-97, -129, -1)])
    _, _, c3h, r3h, _, _ = fit(dh, half)
    _, _, c3t, r3t, _, _ = fit(dtail, tail)
    dseg = abs(c3h[0]-c3t[0])/c3t[0]*100
    print("  先验 P2（分段稳定，判据 |Δδ∞(33..96 vs 97..128)|<0.02 pct）：%+.4f pct → %s" % (
        dseg, "通过" if dseg < 0.02 else "★ 未通过（δ∞ 漂移）"), flush=True)
    print("     分段：33..96 三参 δ∞=%.8f RMS=%.2e；97..128 三参 δ∞=%.8f RMS=%.2e" % (c3h[0], r3h, c3t[0], r3t), flush=True)
    # 先验 P3：前半外推后半
    pred_tail = c3h[0] + c3h[1]/tail + c3h[2]/tail**2
    devs_tail = (dtail - pred_tail)/pred_tail*100
    n_ok_t = int(np.sum(np.abs(devs_tail) < 1.0))
    print("  先验 P3（33..96 参数外推 97..128，判据 <1 pct 点数）：%d/32——%s（最大偏差 %+.2f pct）" % (
        n_ok_t, "通过" if n_ok_t >= 28 else "★ 未通过", float(devs_tail[np.argmax(np.abs(devs_tail))])), flush=True)

    # 最佳模型判定
    if d34 < 0.005:
        best, best_dev, best_name = c3f[0], dev3, "三参"
    else:
        best, best_dev, best_name = c4f[0], dev4, "四参"
    if abs(best_dev) < 0.01:
        verdict = "★★★ δ∞ 锁定 1/56（%s，%+.4f pct < 0.01 pct）" % (best_name, best_dev)
    elif abs(best_dev) < 0.05:
        verdict = "★★ δ∞ 强候选维持（%s，%+.4f pct）——未到锁定" % (best_name, best_dev)
    else:
        verdict = "★ δ∞ 强候选降级（%s，%+.4f pct——需分析）" % (best_name, best_dev)
    cross = abs(c3f[0]-f3["d_inf"])/f3["d_inf"]*100
    cross_tag = "双通道互证成立（<0.1 pct）" if cross < 0.1 else "双通道分歧（需诊断）"
    print("", flush=True)
    print("判别：%s" % verdict, flush=True)
    print("双通道（三参 δ∞）差 %.4f pct → %s" % (cross, cross_tag), flush=True)

    json.dump({"N": N_SP,
               "fit_2p": {"d_inf": float(c2f[0]), "C": float(c2f[1]), "rms": rms2, "dev_vs_1o56_pct": float(dev2)},
               "fit_3p": {"d_inf": float(c3f[0]), "C": float(c3f[1]), "D": float(c3f[2]), "rms": rms3, "dev_vs_1o56_pct": float(dev3)},
               "fit_4p": {"d_inf": float(c4f[0]), "C": float(c4f[1]), "D": float(c4f[2]), "E": float(c4f[3]), "rms": rms4, "dev_vs_1o56_pct": float(dev4)},
               "check_P1_d34_pct": float(d34), "check_P2_seg_pct": float(dseg),
               "check_P3_ok": n_ok_t, "ref118_fit_2p": {"d_inf": f2["d_inf"], "C": f2["C"]},
               "ref118_fit_3p": {"d_inf": f3["d_inf"], "C": f3["C"], "D": f3["D"]},
               "cross_channel_dev_3p_pct": float(cross), "verdict": verdict,
               "runtime_s": dt, "out": {str(k): v for k, v in out.items()}},
              open(os.path.join(BASE, "_phase102_p7_5e120_spectral_m128.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("", flush=True)
    print("JSON 落盘 OK exit 0", flush=True)
