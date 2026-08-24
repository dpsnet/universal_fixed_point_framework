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
"""多组分 SC D2Q9 不混相驱替 2D 验证（t4b-3）。

基于 mc_scan 修正结论（力含负号 + 组分独立 ueq + 力除组分密度）：
  G11=-1.0（各自凝聚）+ G12=1.5（互斥）→ 不混相双相，共存密度 (0.014, 1.535)。

驱替设置：
  域 64×128，随机固体 φ=0.28（与 scmp_drive2d 同介质，便于对比），
  初始孔隙全为组分 1（油，ρ=1.4 近平衡液密度）；
  入口 x∈[0,dx) 缓冲：纯组分 2 ρ_in=1.5（过饱和高压，化学势优势）；
  出口缓冲：纯组分 2 ρ_out=0.05（低压），组分 1 可排出。
检验：组分 2 前沿推进 + 油（组分 1）占比下降 + 残余油形成。

迁移用周期 np.roll + 缓冲列覆盖（出口回卷的组分 2 在入口无害、组分 1 被冲掉）。
"""
import numpy as np

EX = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1], dtype=np.int64)
EY = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1], dtype=np.int64)
W  = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])
OPP = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6])

def psi(rho):
    return 1.0 - np.exp(-rho)

def step2(f1, f2, solid, tau, G11, G12, rho_in, rho_out, dx_in, dx_out, F_ext=0.0):
    ny, nx = f1.shape[1], f1.shape[2]
    rho1 = f1.sum(0); rho2 = f2.sum(0)
    rho = rho1 + rho2
    ux = ((f1*EX[:, None, None]).sum(0) + (f2*EX[:, None, None]).sum(0)) / np.maximum(rho, 1e-12)
    uy = ((f1*EY[:, None, None]).sum(0) + (f2*EY[:, None, None]).sum(0)) / np.maximum(rho, 1e-12)
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
    # 组分 2 外力（宏观压差驱动，仅孔隙格点）
    fx2 += F_ext * (~solid)
    ueq1x = ux + tau*fx1/np.maximum(rho1, 1e-12)
    ueq1y = uy + tau*fy1/np.maximum(rho1, 1e-12)
    ueq2x = ux + tau*fx2/np.maximum(rho2, 1e-12)
    ueq2y = uy + tau*fy2/np.maximum(rho2, 1e-12)
    out1 = np.zeros_like(f1); out2 = np.zeros_like(f2)
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
    # bounce-back at solid（BFL 标准方案，质量守恒）：
    # 固体格点收到邻格迁移来的分布后，原路反射回来源格点；固体格点本身清零。
    for k, (f, out) in enumerate(((f1, out1), (f2, out2))):
        for i in range(9):
            back = out[i] * solid
            out[OPP[i]] += np.roll(back, (EY[OPP[i]], EX[OPP[i]]), axis=(0, 1))
            out[i] *= ~solid
        out[:, solid] = 0.0
    # 缓冲列：入口纯组分2=rho_in（高压），出口纯组分2=rho_out（低压）
    for x in range(dx_in):
        out1[:, :, x] = 0.0
        for i in range(9):
            out2[i, :, x] = W[i] * rho_in
    for x in range(nx - dx_out, nx):
        out1[:, :, x] = 0.0
        for i in range(9):
            out2[i, :, x] = W[i] * rho_out
    return out1, out2

if __name__ == "__main__":
    ny, nx = 64, 128
    rng = np.random.default_rng(3)
    solid = np.zeros((ny, nx), dtype=bool)
    solid[1:-1, 1:-1] = rng.random((ny-2, nx-2)) < 0.28
    solid[:, :4] = False
    solid[:, -4:] = False
    # 初始：半域预分离（x<64 组分2，x≥64 组分1），界面 6 列斜坡，周期域无缓冲
    # 阶段 A：混合初始（两组分重叠 0.7±0.03）→ 自旋节分离，形成平衡界面（mc_scan 同款稳定设置）
    rng = np.random.default_rng(7)
    rho1 = np.where(solid, 0.0, 0.7 + 0.1*rng.random((ny, nx)))
    rho2 = np.where(solid, 0.0, 0.7 + 0.1*rng.random((ny, nx)))
    f1 = np.stack([W[i]*rho1 for i in range(9)])
    f2 = np.stack([W[i]*rho2 for i in range(9)])
    G11, G12, tau = -1.0, 0.6, 1.0
    rho_in = rho_out = None
    dx_in = dx_out = 0
    nstep = 1500
    pore = (~solid).sum()
    for st in range(nstep):
        f1, f2 = step2(f1, f2, solid, tau, G11, G12, rho_in, rho_out, dx_in, dx_out)
        if st % 500 == 0:
            r1 = f1.sum(0); r2 = f2.sum(0)
            if not np.isfinite(r1).all():
                print(f"  [阶段A] step {st} 发散")
                break
            print(f"  [阶段A] step {st:5d}: ρ1max={r1.max():.2f} ρ2max={r2.max():.2f} "
                  f"ρ1_hi={(r1>1.0).sum()}格 ρ2_hi={(r2>1.0).sum()}格")
    print("  阶段 A 完成（自分离）")
    # 阶段 B：封闭体系充注——x 两端反弹墙，组分2 恒定外力 F_ext 侵入组分1 空间。
    # F_ext 扫描：每次从阶段 A 终态独立演化，测平衡 S2(F_ext) 即 S(ΔP)。
    solid[:, 0] = True
    solid[:, -1] = True
    for F_ext in (2e-3, 5e-3, 1e-2, 2e-2):
        g1 = f1.copy(); g2 = f2.copy()
        for st in range(1500):
            g1, g2 = step2(g1, g2, solid, tau, G11, G12, 0.0, 0.0, 0, 0, F_ext)
            if st % 300 == 0:
                r1 = g1.sum(0); r2 = g2.sum(0)
                if not np.isfinite(r1).all():
                    print(f"  F_ext={F_ext:.1e}: step {st} 发散")
                    break
        r1 = g1.sum(0); r2 = g2.sum(0)
        S1 = (r1 > 0.8).sum() / pore
        S2 = (r2 > 0.8).sum() / pore
        print(f"  F_ext={F_ext:.1e}: 油={S1*100:5.1f}% 驱相={S2*100:5.1f}% "
              f"ρ1max={r1.max():.2f} ρ2max={r2.max():.2f}")
