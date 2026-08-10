#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t5-3 朗缪尔双倒数几何抑制量化（→ P2-6k）。

目标：量化 P2-6f 中"朗缪尔双倒数拟合成功率 0/8、4/8、7/8（φ=0.20/0.31/0.40）"
的机制——渗流几何在突破暂态对双倒数线性的抑制窗口。

分解：S(P) = G(P)·F(P)，F=P/(P+a) 精确朗缪尔（无几何直接累积），
G=S/F = 几何因子（≤1，突破后趋 1=几何透明）。
双倒数 1/S 对 1/P 线性 ⟺ 1/G 在窗内对 1/P 仿射。

机制锚点：若 G(P) = (P+a)/(P+a')（"可重正化族"），则 S=P/(P+a') 仍精确朗缪尔
（双倒数拟合必然成功，仅参数平移 a→a'）；**拟合失败 ⟺ G 偏离该族**
（突破暂态渗流包络形状非可重正化族）。

诊断（窗 P∈(P_c,3.01]）：
  G(P_c)    突破处抑制深度
  P_95      几何透明阈值（G≥0.95 最小 P）
  W=(P_95−P_c)/P_c   抑制窗宽（以 P_c 为单位）
  msupp=1−mean(G)   窗内平均抑制
  slp       1/G 对 1/P 标准化斜率（G≡const→0；越大曲率越强→越失败）
  r2f       G 对 (P+a)/(P+a') 族拟合 R²（=1 则失败机制不激活）
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_ip_langmuir import run_ip_langmuir, langmuir_fit

A = 1.09          # 东营 ΔP_L (MPa)
PCAP = 3.01       # 东营窗口上限

def fit_family(P, G, a=A):
    """G 对可重正化族 (P+a)/(P+a') 的拟合：返回 a', R²。"""
    from scipy.optimize import minimize_scalar
    def resid(ap):
        return np.sum((G - (P + a)/(P + ap))**2)
    res = minimize_scalar(resid, bounds=(1e-6, 500.0), method="bounded")
    ap = res.x
    Ghat = (P + a)/(P + ap)
    ss_res = np.sum((G - Ghat)**2)
    ss_tot = np.sum((G - G.mean())**2)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else np.nan
    return ap, r2

def geo_diag(P, S, Pc):
    """单配置几何抑制诊断。"""
    F = P/(P + A)
    G = S/F
    m = (P > Pc) & (P <= PCAP) & (F > 1e-3) & (S > 1e-3) & (S < 0.999)
    if m.sum() < 5:
        return None
    Pm, Gm = P[m], G[m]
    Gpc = Gm[np.argmin(Pm)]
    idx = np.flatnonzero(Gm >= 0.95)
    P95 = Pm[idx[0]] if idx.size else np.nan
    W = (P95 - Pc)/Pc if np.isfinite(P95) else (PCAP - Pc)/Pc
    # 抑制窗占拟合窗比例（最锐利预测指标）
    f_supp = (P95 - Pc)/(PCAP - Pc) if np.isfinite(P95) else 1.0
    msupp = 1.0 - Gm.mean()
    X = 1.0/Pm; Y = 1.0/Gm
    A_ = np.vstack([X, np.ones_like(X)]).T
    k, b = np.linalg.lstsq(A_, Y, rcond=None)[0]
    slp = k * (X.std()/Y.std()) if Y.std() > 0 else np.nan
    ap, r2f = fit_family(Pm, Gm)
    return dict(Pc=Pc, Gpc=Gpc, P95=P95, W=W, msupp=msupp, slp=slp, ap=ap, r2f=r2f,
                f_supp=f_supp)

if __name__ == "__main__":
    n, ncfg = 96, 8
    print(f"t5-3 朗缪尔双倒数几何抑制量化（{n}³ ncfg={ncfg}，a={A}，窗 P∈(P_c,{PCAP}]）")
    print("=" * 100)
    print(f"{'φ':>6} {'成功':>5} {'P_c':>7} {'G(P_c)':>7} {'P_95':>7} {'W(×P_c)':>8} "
          f"{'msupp':>6} {'slp':>6} {'r2f族':>6} {'f_supp':>7} | {'成功vs msupp':>12} {'成功vs slp':>11}")
    for phi in (0.20, 0.31, 0.40):
        succ, r2s = [], []
        diags = []
        for cfg in range(ncfg):
            rng = np.random.default_rng(cfg)
            binary = rng.random((n, n, n)) < phi
            P, S, Pc, Sc = run_ip_langmuir(binary, seed=cfg)
            if Pc < 0:
                continue
            lf = langmuir_fit(P, S, Pc)
            ok = lf is not None
            succ.append(ok)
            if lf:
                r2s.append(lf[2])
            d = geo_diag(P, S, Pc)
            if d:
                d["ok"] = ok
                diags.append(d)
        ns = len(succ)
        if ns == 0:
            print(f"{phi:6.2f} 无突破配置")
            continue
        n_ok = sum(succ)
        d = np.array([(x["Pc"], x["Gpc"], x["W"], x["msupp"], x["slp"], x["r2f"], x["f_supp"], x["ok"])
                      for x in diags])
        Pc_ = d[:, 0].mean(); Gpc_ = d[:, 1].mean()
        W_ = d[:, 2].mean(); msupp_ = d[:, 3].mean()
        slp_ = d[:, 4].mean(); r2f_ = d[:, 5].mean()
        f_supp_ = d[:, 6].mean()
        # 成功 vs msupp / slp 的相关（点双列）
        def point_biserial(metric, ok):
            m0 = metric[ok == 0]; m1 = metric[ok == 1]
            if m0.size == 0 or m1.size == 0:
                return np.nan
            return (m1.mean() - m0.mean()) / metric.std()
        r_ms = point_biserial(d[:, 3], d[:, 7].astype(bool))
        r_sl = point_biserial(d[:, 4], d[:, 7].astype(bool))
        P95_ = np.nanmean([x["P95"] for x in diags])
        r2mean = np.mean(r2s) if r2s else np.nan
        print(f"{phi:6.2f} {n_ok:3d}/{ns:<2} {Pc_:7.3f} {Gpc_:7.3f} {P95_:7.2f} {W_:8.2f} "
              f"{msupp_:6.3f} {slp_:6.3f} {r2f_:6.3f} {f_supp_:7.2f} | {r_ms:12.3f} {r_sl:11.3f}"
              f"   (成功者 R²均={r2mean:.3f})")

    print("\n[机制表] 各 φ 典型配置：G(P) 剖面（P/P_c 网格）")
    for phi in (0.20, 0.31, 0.40):
        cfg = 0
        rng = np.random.default_rng(cfg)
        binary = rng.random((n, n, n)) < phi
        P, S, Pc, Sc = run_ip_langmuir(binary, seed=cfg)
        if Pc < 0:
            continue
        F = P/(P + A)
        G = S/F
        m = (P > Pc) & (P <= PCAP) & (F > 1e-3) & (S > 1e-3) & (S < 0.999)
        Pm, Gm = P[m], G[m]
        # 在 P/P_c 网格上插值 G
        grid = np.array([1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0]) * Pc
        grid = grid[grid <= PCAP]
        Gg = np.interp(grid, Pm, Gm)
        lf = langmuir_fit(P, S, Pc)
        tag = "成功" if lf else "失败"
        print(f"  φ={phi:.2f} P_c={Pc:.3f} ({tag}): " +
              " ".join(f"P/Pc={g/Pc:g}:G={Gg[i]:.3f}" for i, g in enumerate(grid)))
