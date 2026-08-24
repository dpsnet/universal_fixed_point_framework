# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SCMP D2Q9 相分离参数扫描——找两相分离的 G 阈值。"""
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
    # 伪势力
    fx = np.zeros_like(rho); fy = np.zeros_like(rho)
    p = psi(rho)
    for i in range(9):
        pe = np.roll(p, (-EY[i], -EX[i]), axis=(0, 1))
        fx -= G * W[i] * p * pe * EX[i]
        fy -= G * W[i] * p * pe * EY[i]
    # 速度修正（Shan-Chen）
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
    for i in range(9):
        j = 9 if i == 0 else None
    for i in range(9):
        # 反弹
        pass
    out[:, solid] = 0.0
    return out

def test(G, nstep=4000, seed=0):
    ny = nx = 64
    rng = np.random.default_rng(seed)
    rho0 = 1.2
    rho = rho0 + 0.05*rng.random((ny, nx))
    f = np.stack([W[i]*rho for i in range(9)])
    solid = np.zeros((ny, nx), dtype=bool)
    for st in range(nstep):
        f = step(f, solid, 1.0, G)
    r = f.sum(0)
    h, _ = np.histogram(r, bins=12, range=(0, 3))
    std = r.std()
    # 相位分离判据：直方图两端都有显著质量
    low = h[:3].sum(); high = h[-3:].sum()
    sep = low > 20 and high > 20
    print(f"G={G:5.2f}: std={std:.3f}  直方图={h.tolist()}  {'** 相分离 **' if sep else ''}")

if __name__ == "__main__":
    for G in (-1.0, -2.0, -3.0, -4.0, -5.0, -6.0):
        test(G)
