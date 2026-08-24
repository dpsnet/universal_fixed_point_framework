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
"""D2Q9 多组分伪势 LBM（P2 ν 裁决 t4 前置验证）。

验证：两相自发分离 + 均质介质水驱油前沿 + 残余油测量。
迁移用 pull 形式：fn_i[x] = f_i[x−e_i]（np.roll 实现）。
"""
import numpy as np

# ---- D2Q9 ----
EX = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1], dtype=np.int64)
EY = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1], dtype=np.int64)
W  = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])
OPP = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6])

def psi(rho):
    return 1.0 - np.exp(-rho)

def mac(f1, f2):
    rho1 = f1.sum(0); rho2 = f2.sum(0)
    rho = rho1 + rho2
    ux = ((f1*EX[:, None, None]).sum(0) + (f2*EX[:, None, None]).sum(0)) / np.maximum(rho, 1e-12)
    uy = ((f1*EY[:, None, None]).sum(0) + (f2*EY[:, None, None]).sum(0)) / np.maximum(rho, 1e-12)
    return rho1, rho2, ux, uy

def collide_stream(f1, f2, solid, tau, G12):
    """碰撞(Guo力) + pull 迁移 + 反弹。"""
    rho1, rho2, ux, uy = mac(f1, f2)
    usq = ux*ux + uy*uy
    # 伪势力场（组分间排斥）
    fx1 = np.zeros_like(rho1); fy1 = np.zeros_like(rho1)
    fx2 = np.zeros_like(rho1); fy2 = np.zeros_like(rho1)
    p1 = psi(rho1); p2 = psi(rho2)
    for i in range(9):
        # psi(x+e_i)
        p1e = np.roll(p1, (-EY[i], -EX[i]), axis=(0, 1))
        p2e = np.roll(p2, (-EY[i], -EX[i]), axis=(0, 1))
        w = W[i]
        fx1 -= G12 * w * p1 * p2e * EX[i]
        fy1 -= G12 * w * p1 * p2e * EY[i]
        fx2 -= G12 * w * p2 * p1e * EX[i]
        fy2 -= G12 * w * p2 * p1e * EY[i]
    out1 = np.zeros_like(f1); out2 = np.zeros_like(f2)
    for i in range(9):
        eu = EX[i]*ux + EY[i]*uy
        feq1 = rho1 * W[i] * (1.0 + 3.0*eu + 4.5*eu*eu - 1.5*usq)
        feq2 = rho2 * W[i] * (1.0 + 3.0*eu + 4.5*eu*eu - 1.5*usq)
        # Guo 力项（每组分自己的力）
        ef1 = EX[i]*fx1 + EY[i]*fy1
        ef2 = EX[i]*fx2 + EY[i]*fy2
        g1 = W[i]*(1.0 - 0.5/tau) * (3.0*ef1 + 9.0*eu*ef1 - 3.0*(ux*fx1+uy*fy1))
        g2 = W[i]*(1.0 - 0.5/tau) * (3.0*ef2 + 9.0*eu*ef2 - 3.0*(ux*fx2+uy*fy2))
        c1 = f1[i] - (f1[i] - feq1)/tau + g1
        c2 = f2[i] - (f2[i] - feq2)/tau + g2
        # pull 迁移：out_i[x] = c_i[x−e_i]
        out1[i] = np.roll(c1, (EY[i], EX[i]), axis=(0, 1))
        out2[i] = np.roll(c2, (EY[i], EX[i]), axis=(0, 1))
    # 固体反弹（细粒：反弹到对面方向）
    for i in range(9):
        j = OPP[i]
        b = solid
        out1[i] = np.where(b, f1[j], out1[i])
        out2[i] = np.where(b, f2[j], out2[i])
    # 固体内部清零
    out1[:, solid] = 0.0
    out2[:, solid] = 0.0
    return out1, out2

def run_phase_sep(ny, nx, nstep, tau=1.0, G12=1.2, seed=1):
    """验证1：均质扰动 → 两相分离。"""
    rng = np.random.default_rng(seed)
    rho1 = 1.0 + 0.2*rng.random((ny, nx))
    rho2 = 1.0 + 0.2*rng.random((ny, nx))
    f1 = np.stack([W[i]*rho1 for i in range(9)])
    f2 = np.stack([W[i]*rho2 for i in range(9)])
    solid = np.zeros((ny, nx), dtype=bool)
    for step in range(nstep):
        f1, f2 = collide_stream(f1, f2, solid, tau, G12)
        if step % 500 == 0:
            r1, r2, _, _ = mac(f1, f2)
            print(f"  step {step}: rho1 范围 [{r1.min():.3f},{r1.max():.3f}] std={r1.std():.4f}")
    r1, r2, _, _ = mac(f1, f2)
    h, _ = np.histogram(r1, bins=15, range=(0, 3))
    print("  组分1 密度直方图（双峰→相分离）:", h.tolist())
    return r1

def run_waterflood(ny, nx, nstep, tau=1.0, G12=1.2, rho_in=2.0, log_every=200):
    """验证2：均质孔隙（多孔障碍）+ 水驱油。入口 x=0 注水。"""
    solid = np.zeros((ny, nx), dtype=bool)
    # 简单障碍：随机小方柱（孔隙率 ~70%）
    rng = np.random.default_rng(2)
    solid[1:-1, 1:-1] = rng.random((ny-2, nx-2)) < 0.3
    # 入口列和出口列留空
    solid[:, 0] = False; solid[:, -1] = False
    rho1 = np.where(solid, 0.0, 2.0)   # 油
    rho2 = np.where(solid, 0.0, 0.01)  # 水（微量）
    f1 = np.stack([W[i]*rho1 for i in range(9)])
    f2 = np.stack([W[i]*rho2 for i in range(9)])
    for step in range(nstep):
        # 入口：x=0 固定水密度（压力源）
        if step % 2 == 0:
            # 设置入口柱的分布为平衡
            r1, r2, ux, uy = mac(f1, f2)
            r2[0, :] = rho_in
            r1[0, :] = 0.01
            usq = ux*ux + uy*uy
            for i in range(9):
                eu = EX[i]*ux[0, :] + EY[i]*uy[0, :]
                f2[i, 0, :] = r2[0, :] * W[i] * (1.0 + 3.0*eu + 4.5*eu*eu - 1.5*usq[0, :])
                f1[i, 0, :] = r1[0, :] * W[i] * (1.0 + 3.0*eu + 4.5*eu*eu - 1.5*usq[0, :])
        f1, f2 = collide_stream(f1, f2, solid, tau, G12)
        if step % log_every == 0:
            r1, r2, _, _ = mac(f1, f2)
            oil_tot = r1[1-solids if False else 1:, :].sum() if False else (r1*(1-solid)).sum()
            water_front = (r2 > 1.0).sum()
            print(f"  step {step}: 油总量={oil_tot:.0f} 水区体积={water_front}  "
                  f"前沿最远 x={(r2>1.0).any(0).nonzero()[0].max() if (r2>1.0).any() else 0}")
    return f1, f2, solid

if __name__ == "__main__":
    print("=" * 60)
    print("验证1：两相自发分离（G12=1.2 排斥）")
    print("=" * 60)
    r1 = run_phase_sep(64, 64, 3000)

    print()
    print("=" * 60)
    print("验证2：水驱油前沿推进（多孔障碍 ~70% 孔隙率）")
    print("=" * 60)
    f1, f2, solid = run_waterflood(64, 128, 3000)
