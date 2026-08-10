#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IP + 朗缪尔孔喉阈值分布——检验东营 ν=1 是否系孔径分布属性。

动机（P2-6e 结论的收尾检验）：随机介质（U~U(0,1)）IP 给出 P2 型 ν≈0.2–0.4，
东营 R_m(ΔP) 双倒数线性 R² 0.93–0.99（朗缪尔 ν=1）。若朗缪尔累积 ↔
体积加权孔喉分布 f(r)∝(C+ΔP_L·r)^(−2)，则把该分布采样进 IP 阈值，
渗流几何下 S(ΔP) 若仍保持朗缪尔型（双倒数线性 + ν≈1）→ 几何不扭曲材料属性，
东营 ν=1 系孔径分布陈述；若被扭曲（R² 降、ν 偏移）→ 临界几何改写了响应。

阈值采样：朗缪尔累积 F(P)=P/(P+a)，逆变换 U = a·T/(1−T)，T~U(0,1)，a=ΔP_L=1.09。
对照：无几何直接累积 F(P)=P/(P+a)。
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_ip_uf import ip_union_entry

A = 1.09  # 东营 ΔP_L (MPa)

def langmuir_thresholds(binary, seed=0, a=A):
    """每孔隙朗缪尔隐含阈值 U=a·T/(1−T)。固体处 2.0（占位）。"""
    nz, ny, nx = binary.shape
    rng = np.random.default_rng(seed + 1000)
    T = rng.random((nz, ny, nx))
    U = a * T / (1.0 - T)
    return np.where(binary, U, 2.0)

def run_ip_langmuir(binary, seed=0):
    nz, ny, nx = binary.shape
    U3d = langmuir_thresholds(binary, seed=seed)
    pore_idx = np.flatnonzero(binary.ravel())
    Uf = U3d.ravel()
    order = pore_idx[np.argsort(Uf[pore_idx])]
    return ip_union_entry(binary, Uf, order)

def langmuir_fit(P, S, Pc, Pmax=3.01):
    """双倒数线性化 1/S = 1/R_f + (a/R_f)·(1/P)，限突破后物理窗口 P∈(P_c,Pmax]。
    返回 R_f, a, R²。"""
    m = (P > Pc) & (P <= Pmax) & (S > 1e-3) & (S < 0.999)
    if m.sum() < 5:
        return None
    X = 1.0 / P[m]; Y = 1.0 / S[m]
    A_ = np.vstack([X, np.ones_like(X)]).T
    k, b = np.linalg.lstsq(A_, Y, rcond=None)[0]
    pred = k * X + b
    r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
    if k <= 0 or b <= 0:
        return None
    Rf = 1.0 / b; a_ = k / b
    return Rf, a_, r2

def p2nu(P, S, Pc, Pmax=3.01):
    """P2 型 ν：log P vs log(1−S)，限突破后窗口 P∈(P_c, Pmax]。"""
    resid = 1.0 - S
    m2 = (resid > 0.01) & (P > Pc) & (P <= Pmax)
    if m2.sum() < 10:
        return None
    X = np.log(resid[m2]); Y = np.log(P[m2])
    A_ = np.vstack([X, np.ones_like(X)]).T
    k, b = np.linalg.lstsq(A_, Y, rcond=None)[0]
    pred = k * X + b
    r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
    return -k, r2

if __name__ == "__main__":
    n = 96
    ncfg = 8
    for phi in (0.20, 0.31, 0.40):
        rows = []
        for cfg in range(ncfg):
            rng = np.random.default_rng(cfg)
            binary = rng.random((n, n, n)) < phi
            P, S, Pc, Sc = run_ip_langmuir(binary, seed=cfg)
            if Pc < 0:
                print(f"  [dbg] φ={phi:.2f} cfg{cfg}: 无突破")
                continue
            lf = langmuir_fit(P, S, Pc)
            nu = p2nu(P, S, Pc)
            # 无几何对照：直接累积 F(P)=P/(P+a)，同突破后窗口
            F = P / (P + A)
            m = (P > Pc) & (P <= 3.01) & (F < 0.999) & (F > 1e-3)
            X = 1.0 / P[m]; Y = 1.0 / F[m]
            A_ = np.vstack([X, np.ones_like(X)]).T
            k, b = np.linalg.lstsq(A_, Y, rcond=None)[0]
            pred = k * X + b
            r2F = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
            if lf:
                Rf, a_, r2 = lf
            else:
                Rf = a_ = r2 = np.nan
            # 几何透明度：窗口顶 S(P→3.01)/F(3.01)
            mtop = (P <= 3.01) & (P > 0)
            Stop = S[mtop][-1] if mtop.sum() else np.nan
            Ftop = 3.01 / (3.01 + A)
            sf_top = Stop / Ftop
            rows.append((Pc, Sc, Rf, a_, r2, nu[0] if nu else np.nan,
                         nu[1] if nu else np.nan, r2F, sf_top))
        if not rows:
            print(f"[φ={phi:.2f}] 无突破配置")
            continue
        rows = np.array(rows)
        n_lf = np.isfinite(rows[:, 2]).sum()
        Pc, Sc = rows[:, 0].mean(), rows[:, 1].mean()
        Rf = np.nanmean(rows[:, 2]); a_ = np.nanmean(rows[:, 3])
        r2 = np.nanmean(rows[:, 4])
        nu = np.nanmean(rows[:, 5]); r2nu = np.nanmean(rows[:, 6])
        r2F = rows[:, 7].mean()
        sf_top = rows[:, 8].mean()
        print(f"[朗缪尔阈值 IP {n}³ φ={phi:.2f}] P_c={Pc:.3f} S_c={Sc*100:.1f}% | "
              f"朗缪尔拟合 {n_lf}/{ncfg} 成功 R_f={Rf:.3f} a_eff={a_:.3f} R²={r2:.3f} | "
              f"P2型ν={nu:.3f} (R² {r2nu:.3f}) | 无几何F对照R²={r2F:.3f} | S/F顶={sf_top:.3f}")
