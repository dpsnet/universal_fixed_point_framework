#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SCMP D2Q9 G=−4.5 窗口测试——共存密度 + 稳定性（半盒液/汽平衡）。
目的：修正 P2-6d 登记的汽相驱替压力方向倒置问题。
判据：能稳定维持液/汽两相并存（不发散、不全部坍缩一相），
并给出经验共存密度 (rho_v, rho_l) 供驱替边界设置。"""
import numpy as np

EX = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1], dtype=np.int64)
EY = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1], dtype=np.int64)
W  = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])

def psi(rho):
    return 1.0 - np.exp(-rho)

def step(f, solid, tau, G):
    rho = f.sum(0)
    ux = (f*EX[:, None, None]).sum(0) / np.maximum(rho, 1e-12)
    uy = (f*EY[:, None, None]).sum(0) / np.maximum(rho, 1e-12)
    usq = ux*ux + uy*uy
    fx = np.zeros_like(rho); fy = np.zeros_like(rho)
    p = psi(rho)
    for i in range(9):
        pe = np.roll(p, (-EY[i], -EX[i]), axis=(0, 1))
        fx -= G * W[i] * p * pe * EX[i]
        fy -= G * W[i] * p * pe * EY[i]
    ueqx = ux + tau*fx/np.maximum(rho, 1e-12)
    ueqy = uy + tau*fy/np.maximum(rho, 1e-12)
    ueqsq = ueqx*ueqx + ueqy*ueqy
    out = np.zeros_like(f)
    for i in range(9):
        eu = EX[i]*ueqx + EY[i]*ueqy
        feq = rho * W[i] * (1.0 + 3.0*eu + 4.5*eu*eu - 1.5*ueqsq)
        ef = EX[i]*fx + EY[i]*fy
        g = W[i]*(1.0 - 0.5/tau) * (3.0*ef + 9.0*eu*ef - 3.0*(ueqx*fx+ueqy*fy))
        c = f[i] - (f[i] - feq)/tau + g
        out[i] = np.roll(c, (EY[i], EX[i]), axis=(0, 1))
    out[:, solid] = 0.0
    return out

def plateaus(rho):
    """从液/汽并存场提取两相峰值密度（直方图双峰中心）。"""
    h, edges = np.histogram(rho, bins=40, range=(0, 3))
    # 粗略：分成低/高两半各找峰
    bins = edges[:-1] + 0.5*(edges[1]-edges[0])
    m = bins < 0.8
    lo = bins[m][np.argmax(h[m])] if m.sum() else np.nan
    hi = bins[~m][np.argmax(h[~m])] if (~m).sum() else np.nan
    return lo, hi

def test(G, ny, nx, rho_v, rho_l, nstep=15000, seed=0):
    """左半汽（rho_v）、右半液（rho_l）+ 界面扰动，看能否维持并存。"""
    rng = np.random.default_rng(seed)
    rho = np.full((ny, nx), rho_v)
    rho[:, nx//2:] = rho_l
    # 界面加少量噪声促进平衡
    rho += 0.02*rng.random((ny, nx))
    f = np.stack([W[i]*rho for i in range(9)])
    solid = np.zeros((ny, nx), dtype=bool)
    for st in range(nstep):
        f = step(f, solid, 1.0, G)
        if not np.isfinite(f).all():
            print(f"  G={G:5.2f}: 发散（step {st}）")
            return None, None, None
    r = f.sum(0)
    rv, rl = plateaus(r)
    std = r.std()
    # 每相平均压力（SC 热力学压 P=ρ/3+Gψ²/6，离散形式）——远离界面测
    mid_v = r[:, :nx//2-6]
    mid_l = r[:, nx//2+6:]
    Pv = (mid_v/3 + G*psi(mid_v)**2/6).mean()
    Pl = (mid_l/3 + G*psi(mid_l)**2/6).mean()
    v_frac = (r < 0.8).mean()
    l_frac = (r > 1.0).mean()
    ok = v_frac > 0.1 and l_frac > 0.1
    print(f"  G={G:5.2f}: std={std:.3f}  ρ_v≈{rv:.2f} ρ_l≈{rl:.2f}  "
          f"P_v={Pv:.4f} P_l={Pl:.4f}  汽{v_frac*100:.0f}% 液{l_frac*100:.0f}%  "
          f"{'并存✓' if ok else '异常'}")
    return rv, rl, ok

if __name__ == "__main__":
    for G in (-4.0, -4.5):
        test(G, 64, 128, 0.1, 2.0)
