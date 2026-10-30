# -*- coding: utf-8 -*-
"""
P7-5e-118c：m=128 五档收敛性诊断——判定 Richardson 数值极限 vs 物理变换
=====================================================================
118 主脚本（0.02/0.01/0.005 二阶）δ(128)=0.01631 vs 高精度复核（0.005/0.0025 二阶）
δ(128)=0.01939——两口径差 19%，且 m=80/123 复核偏离双曲 +5~18%——
怀疑大 N_r（≥102400）dstemr 数值精度退化使 Richardson 失效。
本脚本：m=128/80 五档 B*(dr)（0.04/0.02/0.01/0.005/0.0025）收敛序列诊断
+ Richardson 二阶/三阶对比 + 双曲预测对照。
"""
import time, json, os
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
w = 0.0265
D_INF, C_HYP = 0.017895, 0.103317

def closed_1B(m):
    return abs(m)/2.0 + 1.0/7.0 + 1.0/(7.0*2.0**abs(m))

def solve(N_r, r_max, B, m):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    return float(eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))[0])

def Bstar_1dr(m, r_max, dr):
    cl = closed_1B(m); Bc = 1.0/cl
    Bs = np.linspace(Bc*(1-w), Bc*(1+w), 7)
    N_r = int(round(r_max / dr))
    Es = np.array([solve(N_r, r_max, float(B), m) for B in Bs])
    B0 = float(Bs[3]); X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    x = -c0/c1
    for _ in range(6):
        x = x - (c0+c1*x+c2*x**2+c3*x**3)/(c1+2*c2*x+3*c3*x**2)
    return B0 + x

drs = [0.04, 0.02, 0.01, 0.005, 0.0025]
for m in [-80, -128]:
    r_max = max(120.0, 4.0*abs(m))
    cl = closed_1B(m); Bc = 1.0/cl
    print("== m=%d  r_max=%.0f  闭式 B*_closed=%.8f（1/B*=%.6f）==" % (m, r_max, Bc, cl), flush=True)
    t0 = time.time()
    Bs_dr = {}
    for dr in drs:
        Bs_dr[dr] = Bstar_1dr(m, r_max, dr)
        print("  dr=%.4f → B*=%.8f（N_r=%d，%.1f s）" % (dr, Bs_dr[dr],
              int(round(r_max/dr)), time.time()-t0), flush=True)
    seq = [Bs_dr[d] for d in drs]
    diffs = [seq[i+1]-seq[i] for i in range(4)]
    print("  相邻差：%s" % ["%+.2e" % x for x in diffs], flush=True)
    # Richardson 二阶各对
    R2_005_0025 = (4*Bs_dr[0.0025]-Bs_dr[0.005])/3.0
    R2_01_005 = (4*Bs_dr[0.005]-Bs_dr[0.01])/3.0
    R2_02_01 = (4*Bs_dr[0.01]-Bs_dr[0.02])/3.0
    # Richardson 三阶（等比 dr/2：用 0.01/0.005/0.0025——通用三阶公式 B0=(64B1−20B2+B3)/45 for ratio 1:2:4）
    # 对 dr 序列 d, d/2, d/4：B(dr)=B0+a·dr²+b·dr⁴；三档消 a,b：
    R3 = (45*Bs_dr[0.0025] - 30*Bs_dr[0.005] + 3*Bs_dr[0.01])/18.0  # 需要验证系数
    # 标准：B1=B(d), B2=B(d/2), B3=B(d/4)：B0 = (B1 − 4·2²·? ...) 用公式 B0=(64B3−20B2+B1)/45
    R3s = (64*Bs_dr[0.0025] - 20*Bs_dr[0.005] + Bs_dr[0.01])/45.0
    print("", flush=True)
    for tag, R in [("R2(0.005/0.0025)", R2_005_0025), ("R2(0.01/0.005)", R2_01_005),
                   ("R2(0.02/0.01)", R2_02_01), ("R3(0.01/0.005/0.0025)", R3s)]:
        delta = abs(1.0/R - cl)
        pred = D_INF - C_HYP/abs(m)
        print("  %s → B*=%.8f  δ=%.6f  双曲=%.6f  偏差=%+.2f pct"
              % (tag, R, delta, pred, (delta-pred)/pred*100), flush=True)
    print("", flush=True)
print("exit 0", flush=True)
