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
"""D2Q9 SCMP 两相驱替（numba 版）——油(液)被汽相驱替验证。

修正（2026-08-09）：原 rho_in=0.05(共存汽)/rho_out=2.4(液) 压力方向倒置
（共存汽压 < 液相压，汽无法推油）。改用 G=−4.5（−4 临界与 −5 发散之间，
实测共存 ρ_v≈0.04/ρ_l≈1.84）：
  - 入口 = 过饱和汽 ρ_in=0.30（汽分支，高于共存汽密度 → P>P_co）
  - 出口 = 欠密度液 ρ_out=1.3（液分支，低于共存液密度 → P<P_co）
亚稳分支单调性保证 P_in > P_co > P_out，驱动方向正确。

验证点：汽相前沿自入口推进、油饱和度下降、残余油形成。
若通过 → D3Q19 升维在临界介质（φ≈0.2–0.35）上跑 S(ΔP) 曲线。
"""
import numpy as np
from numba import njit

EX = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1], dtype=np.int64)
EY = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1], dtype=np.int64)
W  = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])
OPP = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6])

@njit
def scmp_step(f, solid, tau, G, rho_in, rho_out, dx_in, dx_out):
    """单步 SCMP D2Q9。f: (9, ny, nx) 分布。
    dx_in: 入口缓冲列数（x=0..dx_in-1 固定 rho_in）
    dx_out: 出口缓冲列数（x=nx-dx_out..nx-1 固定 rho_out）
    返回新 f 和宏观量。"""
    ny, nx = f.shape[1], f.shape[2]
    fnew = f.copy()
    # 预计算密度场
    rho_field = f.sum(0)
    psi_field = 1.0 - np.exp(-rho_field)
    # 碰撞 + 迁移逐体素
    for y in range(ny):
        for x in range(nx):
            if solid[y, x]:
                continue
            rho = rho_field[y, x]
            ux = 0.0; uy = 0.0
            for q in range(9):
                ux += EX[q] * f[q, y, x]
                uy += EY[q] * f[q, y, x]
            if rho < 1e-10:
                rho = 1e-10
            ux /= rho; uy /= rho
            # 伪势力（梯度 ψ）
            p = psi_field[y, x]
            fx = 0.0; fy = 0.0
            for q in range(9):
                xn = x + EX[q]; yn = y + EY[q]
                # 越界回卷（周期近似）
                if xn < 0: xn += nx
                if xn >= nx: xn -= nx
                if yn < 0: yn += ny
                if yn >= ny: yn -= ny
                pn = psi_field[yn, xn] if not solid[yn, xn] else p
                fx -= G * W[q] * p * pn * EX[q]
                fy -= G * W[q] * p * pn * EY[q]
            # 速度修正 + 平衡
            ueqx = ux + tau * fx / rho
            ueqy = uy + tau * fy / rho
            ueqsq = ueqx*ueqx + ueqy*ueqy
            for q in range(9):
                eu = EX[q]*ueqx + EY[q]*ueqy
                feq = rho * W[q] * (1.0 + 3.0*eu + 4.5*eu*eu - 1.5*ueqsq)
                ef = EX[q]*fx + EY[q]*fy
                g = W[q]*(1.0 - 0.5/tau) * (3.0*ef + 9.0*eu*ef - 3.0*(ueqx*fx + ueqy*fy))
                fnew[q, y, x] = f[q, y, x] - (f[q, y, x] - feq)/tau + g
    # 迁移（pull）
    f2 = np.zeros_like(f)
    for y in range(ny):
        for x in range(nx):
            if solid[y, x]:
                continue
            for q in range(9):
                xp = x - EX[q]; yp = y - EY[q]
                if xp < 0 or xp >= nx or yp < 0 or yp >= ny:
                    # 反弹（边界）
                    qr = OPP[q]
                    f2[q, y, x] = fnew[qr, y, x]
                else:
                    f2[q, y, x] = fnew[q, yp, xp] if not solid[yp, xp] else fnew[OPP[q], y, x]
    # 入口/出口缓冲：固定密度（压力）
    for y in range(ny):
        for x in range(dx_in):
            rho = rho_in
            ux = 0.0; uy = 0.0
            for q in range(9):
                eu = 0.0
                feq = rho * W[q]
                f2[q, y, x] = feq
        for x in range(nx - dx_out, nx):
            rho = rho_out
            for q in range(9):
                f2[q, y, x] = rho * W[q]
    return f2

if __name__ == "__main__":
    ny, nx = 64, 128
    rng = np.random.default_rng(3)
    solid = np.zeros((ny, nx), dtype=np.bool_)
    solid[1:-1, 1:-1] = rng.random((ny-2, nx-2)) < 0.28
    # 留出入入口列
    solid[:, :2] = False
    solid[:, -2:] = False
    # 初始：孔隙全液相（油），取共存液密度附近
    rho0 = 1.8
    f = np.zeros((9, ny, nx))
    for q in range(9):
        f[q] = W[q] * np.where(solid, 0.0, rho0)
    # 驱替参数（G=−4.5 修正：入口过饱和汽 > 出口欠密度液）
    G = -4.5; tau = 1.0
    rho_in = 0.38    # 入口过饱和汽（近汽旋节点 0.405，最大汽分支压）
    rho_out = 1.15   # 出口欠密度液（近液旋节点 1.099，最小液分支压）
    dx_in, dx_out = 3, 3
    nstep = 8000
    pore = (~solid).sum()
    for st in range(nstep):
        f = scmp_step(f, solid, tau, G, rho_in, rho_out, dx_in, dx_out)
        if st % 500 == 0:
            rho = f.sum(0)
            ux = (f[1] - f[3] + f[5] - f[6] - f[7] + f[8]) / np.maximum(rho, 1e-12)
            umag = np.abs(ux[~solid]).mean()
            # 压力诊断（SC 热力学压形式，仅作趋势参照）
            P_field = rho/3 + G*(1.0 - np.exp(-rho))**2/6
            Pin = P_field[:, :dx_in].mean()
            Pout = P_field[:, -dx_out:].mean()
            Pbulk = P_field[:, dx_in:-dx_out][~solid[:, dx_in:-dx_out]].mean()
            oil_frac = (rho[~solid] > 1.0).sum() / pore
            gas_frac = (rho[~solid] < 0.8).sum() / pore
            gas_r = np.where(rho < 0.8, np.arange(nx), -1)
            front = gas_r.max()
            print(f"  step {st}: 油={oil_frac*100:5.1f}% 汽={gas_frac*100:5.1f}% "
                  f"前沿x={front} |u|={umag:.3e} P_in={Pin:.4f} P_bulk={Pbulk:.4f} P_out={Pout:.4f}")
    rho = f.sum(0)
    oil_frac = (rho[~solid] > 1.0).sum() / pore
    print(f"\n  最终 油占比={oil_frac*100:.1f}%")
