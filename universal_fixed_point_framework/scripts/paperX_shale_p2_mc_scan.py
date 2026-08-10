#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多组分 SC D2Q9 相分离扫描：G11=G22 自身吸引 + G12 相互排斥。"""
import numpy as np

EX = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1], dtype=np.int64)
EY = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1], dtype=np.int64)
W  = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])

def psi(rho):
    return 1.0 - np.exp(-rho)

def step2(f1, f2, solid, tau, G11, G12):
    rho1 = f1.sum(0); rho2 = f2.sum(0)
    rho = rho1 + rho2
    ux = ((f1*EX[:, None, None]).sum(0) + (f2*EX[:, None, None]).sum(0)) / np.maximum(rho, 1e-12)
    uy = ((f1*EY[:, None, None]).sum(0) + (f2*EY[:, None, None]).sum(0)) / np.maximum(rho, 1e-12)
    usq = ux*ux + uy*uy
    p1 = psi(rho1); p2 = psi(rho2)
    fx1 = np.zeros_like(rho1); fy1 = np.zeros_like(rho1)
    fx2 = np.zeros_like(rho1); fy2 = np.zeros_like(rho1)
    for i in range(9):
        p1e = np.roll(p1, (-EY[i], -EX[i]), axis=(0, 1))
        p2e = np.roll(p2, (-EY[i], -EX[i]), axis=(0, 1))
        w = W[i]
        # 标准 Shan-Chen 力（含负号）：
        #   G11<0 → 同组分吸引（−G11>0）；G12>0 → 异组分排斥（−G12<0）
        fx1 -= (G11*w*p1*p1e + G12*w*p1*p2e) * EX[i]
        fy1 -= (G11*w*p1*p1e + G12*w*p1*p2e) * EY[i]
        fx2 -= (G11*w*p2*p2e + G12*w*p2*p1e) * EX[i]
        fy2 -= (G11*w*p2*p2e + G12*w*p2*p1e) * EY[i]
    out1 = np.zeros_like(f1); out2 = np.zeros_like(f2)
    # 每组分独立速度修正（力除以组分密度，非总密度）
    ueq1x = ux + tau*fx1/np.maximum(rho1, 1e-12)
    ueq1y = uy + tau*fy1/np.maximum(rho1, 1e-12)
    ueq2x = ux + tau*fx2/np.maximum(rho2, 1e-12)
    ueq2y = uy + tau*fy2/np.maximum(rho2, 1e-12)
    for i in range(9):
        eu1 = EX[i]*ueq1x + EY[i]*ueq1y
        u1sq = ueq1x*ueq1x + ueq1y*ueq1y
        feq1 = rho1 * W[i] * (1.0 + 3.0*eu1 + 4.5*eu1*eu1 - 1.5*u1sq)
        ef1 = EX[i]*fx1 + EY[i]*fy1
        g1 = W[i]*(1.0 - 0.5/tau) * (3.0*ef1 + 9.0*eu1*ef1 - 3.0*(ueq1x*fx1 + ueq1y*fy1))
        c1 = f1[i] - (f1[i] - feq1)/tau + g1
        out1[i] = np.roll(c1, (EY[i], EX[i]), axis=(0, 1))
        eu2 = EX[i]*ueq2x + EY[i]*ueq2y
        u2sq = ueq2x*ueq2x + ueq2y*ueq2y
        feq2 = rho2 * W[i] * (1.0 + 3.0*eu2 + 4.5*eu2*eu2 - 1.5*u2sq)
        ef2 = EX[i]*fx2 + EY[i]*fy2
        g2 = W[i]*(1.0 - 0.5/tau) * (3.0*ef2 + 9.0*eu2*ef2 - 3.0*(ueq2x*fx2 + ueq2y*fy2))
        c2 = f2[i] - (f2[i] - feq2)/tau + g2
        out2[i] = np.roll(c2, (EY[i], EX[i]), axis=(0, 1))
    # 反弹
    for k, (f, out) in enumerate(((f1, out1), (f2, out2))):
        for i in range(9):
            j = [0, 3, 4, 1, 2, 7, 8, 5, 6][i]
            out[i] = np.where(solid, f[j], out[i])
        out[:, solid] = 0.0
    return out1, out2

def test(G11, G12, rho_init=0.7, nstep=6000, seed=0):
    ny = nx = 64
    rng = np.random.default_rng(seed)
    rho1 = rho_init + 0.1*rng.random((ny, nx))
    rho2 = rho_init + 0.1*rng.random((ny, nx))
    f1 = np.stack([W[i]*rho1 for i in range(9)])
    f2 = np.stack([W[i]*rho2 for i in range(9)])
    solid = np.zeros((ny, nx), dtype=bool)
    ok = True
    for st in range(nstep):
        f1, f2 = step2(f1, f2, solid, 1.0, G11, G12)
        if st % 1000 == 0:
            r1 = f1.sum(0)
            if not np.isfinite(r1).all():
                print(f"G11={G11:.2f} G12={G12:.2f}: step {st} 发散")
                return
    r1 = f1.sum(0); r2 = f2.sum(0)
    print(f"G11={G11:5.2f} G12={G12:5.2f}: ρ1 std={r1.std():.2f} "
          f"ρ1[中位,min,max]=[{np.median(r1):.3f},{r1.min():.3f},{r1.max():.3f}] "
          f"ρ2[中位,min,max]=[{np.median(r2):.3f},{r2.min():.3f},{r2.max():.3f}]")
    h1, _ = np.histogram(r1, bins=12, range=(0, 3))
    h2, _ = np.histogram(r2, bins=12, range=(0, 3))
    sep1 = h1[:2].sum() > 20 and h1[-2:].sum() > 20
    sep2 = h2[:2].sum() > 20 and h2[-2:].sum() > 20
    tag = "** 分离 **" if (sep1 and sep2) else ""
    print(f"       直方图 ρ1={h1.tolist()}  {tag}")

if __name__ == "__main__":
    # G12 临界扫描：正=排斥（本脚本符号口径）
    for G11 in (0.0, -0.5, -1.0):
        for G12 in (0.5, 1.0, 1.5, 2.0):
            test(G11, G12, nstep=4000)
