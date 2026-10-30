# -*- coding: utf-8 -*-
"""
P7-5e-230：Newton 细化系统差机制逐点验证
====================================================================
对 m=513（主点，175 与 N=1200 差 −1.25e-6 处）+ m=33/129（辅点）：
  a) Bstar_true(m, N=600, newton_steps=0) —— 谱方法 N=600 无 Newton（164 P2 预测 ≈N=1200）
  b) Bstar_true(m, N=600, newton_steps=3, h_rel=1e-5) —— 175 原版（应复现 175 json）
  c) h_rel 扫描 1e-4/1e-5/1e-6/1e-7（newton_steps=3）+ 单步对比 —— 偏移对 h 依赖
先验：P1 无 Newton N=600≈N=1200（δ 差 <1e-10）；P2 Newton 3 步 h=1e-5 复现 Δδ~−1.2e-6@513；
  P3 偏移随 h 变化（h 越小偏移越小 → 有限差分噪声主导）。
"""
import json, os
import numpy as np
from scipy.linalg import eig

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

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

def delta_of(B, m):
    return closed_1B(m) - 1.0/B

if __name__ == "__main__":
    # N=1200 参考（229/227）
    j229 = json.load(open(os.path.join(BASE, "_phase102_p7_5e229_lowm_N1200.json"), encoding="utf-8"))
    j227 = json.load(open(os.path.join(BASE, "_phase102_p7_5e227_dinf_final_shoot_ext.json"), encoding="utf-8"))
    ref = {}
    for k, v in j229["out"].items():
        ref[int(k)] = v["delta"]
    for mm in j227["ms"]:
        ref.setdefault(abs(mm), j227["spectral"][str(-mm)]["delta"])
    j175 = json.load(open(os.path.join(BASE, "_phase102_p7_5e175_delta63.json"), encoding="utf-8"))
    d175 = dict(zip([int(x) for x in j175["m"]], j175["delta"]))

    print("== P7-5e-230：Newton 细化系统差机制验证 ==", flush=True)
    print("  m  | 配置                          | δ                  | Δδ vs N1200", flush=True)
    for m in [513, 33, 129]:
        rN = ref.get(m)
        if rN is None:
            continue
        r175 = d175.get(m)
        # a) 无 Newton
        Ba = Bstar_true(-m, newton_steps=0)
        da = delta_of(Ba, m)
        # b) 175 原版（3 步 h=1e-5）
        Bb = Bstar_true(-m, newton_steps=3, h_rel=1e-5)
        db = delta_of(Bb, m)
        print("  %3d | N600 无Newton                  | %.10f | %+.2e" % (m, da, da-rN), flush=True)
        print("  %3d | N600 Newton3 h=1e-5（175 原版）| %.10f | %+.2e (175 json %+.2e)" %
              (m, db, db-rN, (r175-rN) if r175 is not None else float('nan')), flush=True)
        # c) h 扫描（3 步）
        for hh in [1e-4, 1e-6, 1e-7]:
            Bh = Bstar_true(-m, newton_steps=3, h_rel=hh)
            dh = delta_of(Bh, m)
            print("  %3d | N600 Newton3 h=%-3.0e          | %.10f | %+.2e" % (m, hh, dh, dh-rN), flush=True)
        # 单步 h=1e-5
        B1 = Bstar_true(-m, newton_steps=1, h_rel=1e-5)
        d1 = delta_of(B1, m)
        print("  %3d | N600 Newton1 h=1e-5            | %.10f | %+.2e" % (m, d1, d1-rN), flush=True)
        print("", flush=True)

    json.dump({"base": "Bstar_true N=600 config scan; ref N=1200 (229/227)",
               "note": "Newton refinement mechanism verification"},
              open(os.path.join(BASE, "_phase102_p7_5e230_newton_mechanism.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
