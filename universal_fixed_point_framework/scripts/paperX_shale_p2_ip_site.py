#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D 随机站点渗流介质 + 侵入渗流——P2 ν 对照（临界介质，替代 DRP-374）。

φ≈0.2–0.35 跨越 3D 站点渗流阈值 f_c≈0.3116。
提取 IP 的 S(P)、突破点 (P_c, S_c)，拟合 P2 形式 ΔP ∝ (S_c−S)^{−ν}。
对照：P2 ν=1/2（平均场）、Langmuir ν=1、IP 普适类（β=0.41 / ν_p=0.88）。
"""
import numpy as np
from scipy import ndimage

def site_media(n, phi, seed=0):
    """随机站点渗流介质：n³，开孔比例 phi，26 连通。"""
    rng = np.random.default_rng(seed)
    return rng.random((n, n, n)) < phi

def random_ip(binary, seed=0, axis=2, P_steps=400):
    """随机阈值 IP。阈值 U~U(0,1) 仅在孔隙上。"""
    rng = np.random.default_rng(seed + 1000)
    nz, ny, nx = binary.shape
    U = np.where(binary, rng.random((nz, ny, nx)), 1.0)
    pore = binary.sum()
    Ps = np.linspace(0.01, 1.0, P_steps)
    S = np.zeros(P_steps)
    sl = [slice(None)] * 3; sl[axis] = 0
    sl2 = [slice(None)] * 3; sl2[axis] = nz - 1
    P_c = None; S_c = None
    for i, P in enumerate(Ps):
        mask = (U <= P) & binary
        lab, _ = ndimage.label(mask, structure=np.ones((3, 3, 3)))
        # 只取与入口层连通的簇（入口层孔隙的标签）
        entry = np.unique(lab[tuple(sl)][mask[tuple(sl)]])
        entry = entry[entry > 0]
        connected = np.isin(lab, entry)
        S[i] = connected.sum() / pore
        if P_c is None and connected[tuple(sl2)].any():
            P_c = P; S_c = S[i]
    return Ps, S, P_c, S_c

def fit_forms(P, S, P_c, S_c, phi, tag):
    """多种指数形式拟合。"""
    print(f"  [{tag} φ={phi:.2f}] 突破 P_c={P_c:.3f} S_c={S_c*100:.1f}%  S末={S[-1]*100:.0f}%")
    # 形式1: P2 型 ΔP∝(S_c−S)^{−ν}，S_c=S[-1]（渐近可动）
    for Sc_name, Sc in [("S_c=S末", S[-1])]:
        resid = Sc - S
        m = (resid > 0.01) & (S > 0.02) & (P < P_c if P_c else True)
        if np.any(m) and m.sum() >= 6:
            X = np.log(resid[m]); Y = np.log(P[m])
            A = np.vstack([X, np.ones_like(X)]).T
            k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
            pred = k * X + b
            r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
            print(f"    突破前段 P2型(ν): 斜率={k:.3f} → ν={-k:.3f}  R²={r2:.4f}  (n={m.sum()})")
    # 形式2: 突破点标度 S−S_c ∝ (P−P_c)^β（IP 占领概率）
    if P_c:
        m2 = (P > P_c) & (S > S_c)
        if m2.sum() >= 6:
            X = np.log(P[m2] - P_c)
            Y = np.log(S[m2] - S_c)
            A = np.vstack([X, np.ones_like(X)]).T
            k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
            pred = k * X + b
            r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
            print(f"    突破后 S−S_c∝(P−P_c)^β: β={k:.3f}  R²={r2:.4f}")
    # 形式3: Langmuir 双倒数 1/S vs 1/(P−P_c)
    if P_c:
        m3 = (P > P_c + 1e-3) & (S > 0.01)
        if m3.sum() >= 6:
            X = 1.0 / (P[m3] - P_c)
            Y = 1.0 / S[m3]
            A = np.vstack([X, np.ones_like(X)]).T
            k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
            pred = k * X + b
            r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
            print(f"    Langmuir双倒数(1/S vs 1/(P−P_c)): R²={r2:.4f}")

if __name__ == "__main__":
    import sys
    n = 192 if "--big" in sys.argv else 96
    ncfg = 10 if "--big" in sys.argv else 1
    for phi in (0.20, 0.31, 0.45):
        betas = []; nus = []
        for cfg in range(ncfg):
            media = site_media(n, phi, seed=cfg)
            Ps, S, P_c, S_c = random_ip(media, seed=cfg, P_steps=250)
            if P_c is None:
                continue
            # 突破后窄窗拟合 β
            m2 = (Ps > P_c) & (Ps < P_c * 2.5) & (S > S_c)
            if m2.sum() >= 6:
                X = np.log(Ps[m2] - P_c); Y = np.log(S[m2] - S_c)
                A = np.vstack([X, np.ones_like(X)]).T
                k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
                pred = k * X + b
                r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
                betas.append((k, r2))
        if ncfg == 1:
            fit_forms(Ps, S, P_c, S_c, phi, f"站点渗流 {n}³")
        else:
            if betas:
                bs = np.array([b[0] for b in betas])
                r2s = np.array([b[1] for b in betas])
                print(f"  [站点渗流 {n}³ φ={phi:.2f}] ncfg={ncfg}: "
                      f"β={bs.mean():.3f}±{bs.std():.3f}  (R²中位 {np.median(r2s):.3f})")
            else:
                print(f"  [站点渗流 {n}³ φ={phi:.2f}] 无有效配置")
