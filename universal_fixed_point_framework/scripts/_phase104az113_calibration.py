# -*- coding: utf-8 -*-
OUT = open(r'C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_113.txt', 'w', encoding='utf-8')
def P(*a):
    OUT.write(' '.join(map(str, a)) + '\n')

"""
Phase 104az-113 A：框架量→MG 标定链机制推导
核心检验：B_cross(η_comp=0.8, n=5) = ħ·C²/(e·r_20%²)
  - r_20% = Hγ 上态（n=5）Balmer 加权径向分布的 20% 分位半径
  - C² = 4ln10（框架内，26.16j-102 已锁定）
  - 若 B_pred ≈ 41 MG → 静默临界交叉场强全框架推导，标定链闭合
闭式：B_cross/B₀ = C²/f²（f = r_20%/a₀）——推导在脚本内
"""
import sys, math
import numpy as np
sys.path.insert(0, r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts')
from _phase100_p3b_compression import balmer_l_weights, radial_density, landau_length

# 物理常数（SI）
HBAR = 1.054571817e-34
E_CH = 1.602176634e-19
A0 = 5.29177210903e-11
C2 = 4.0 * math.log(10.0)   # 框架 C² = 4ln10
B0_T = 2.3527e5             # 2352.7 MG = 2.3527e5 T（n=1 Zeeman=束缚能场强）
OBS_41_MG = 41.0
OBS_RATIO = 41.0 / 2352.7

# 加权径向密度（n=5）
n = 5
wl = balmer_l_weights(n)
W = sum(wl.values())
P("Balmer 加权 n=%d 各 l 权重:" % n)
for l, w in sorted(wl.items()):
    P("  l=%d: w=%.6f (%.2f%%)" % (l, w, 100.0 * w / W))

# 高精度累积分布：二分求 r_20%（累积质量 = 0.2）
def cum_mass(R_cut, npts=200000, rmax=400.0):
    r = np.linspace(1e-8, rmax, npts)
    dens = np.zeros_like(r)
    for l, w in wl.items():
        dens += w * np.array([radial_density(n, l, x) for x in r])
    total = float(np.sum(dens) * (r[1] - r[0]))
    idx = int(np.searchsorted(r, R_cut))
    le = float(np.sum(dens[:idx]) * (r[1] - r[0]))
    return le / total

lo, hi = 1e-3, 400.0
for _ in range(80):
    mid = 0.5 * (lo + hi)
    if cum_mass(mid) < 0.2: lo = mid
    else: hi = mid
r20 = 0.5 * (lo + hi)
P("\n[r_20% 二分求解]")
P("  r_20%%(n=5 加权) = %.6f a₀" % r20)
P("  cum_mass 自检 @r20: %.10f" % cum_mass(r20))

# 交叉点自洽：tail_fraction(5, R_L) 在 41 MG 处
RL_41 = 3.035 * landau_length(4100.0)  # C=3.035≈2√ln10 @ 41 MG
P("\n[41 MG 交叉自洽]")
P("  C·ℓ_B(41 MG) = %.4f a₀（C=3.035）" % RL_41)
P("  r_20%% = %.4f a₀——两者差 = %.4f a₀（%.2f%%）" % (r20, RL_41 - r20, 100.0*(RL_41-r20)/r20))

# B_pred = ħC²/(e·r_20%²)（SI）
r_si = r20 * A0
B_pred_T = HBAR * C2 / (E_CH * r_si * r_si)
B_pred_MG = B_pred_T / 100.0
P("\n[机制闭式 B_cross = ħC²/(e·r_20%²)]")
P("  B_pred = %.2f T = %.2f MG" % (B_pred_T, B_pred_MG))
P("  观测 41 MG——dev = %+.4f%%" % (100.0 * (B_pred_MG - OBS_41_MG) / OBS_41_MG))

# 无量纲闭式 B_cross/B₀ = C²/f²
f2 = r20 * r20
ratio_pred = C2 / f2
P("\n[无量纲闭式 B_cross/B₀ = C²/f²]")
P("  f = r_20%%/a₀ = %.6f，f² = %.4f" % (r20, f2))
P("  B_cross/B₀ (pred) = %.8f" % ratio_pred)
P("  B_cross/B₀ (obs)  = %.8f (41/2352.7)" % OBS_RATIO)
P("  dev = %+.4f%%" % (100.0 * (ratio_pred - OBS_RATIO) / OBS_RATIO))
P("  π/180 = %.8f——对照参考（此前的 0.06%% 近似）" % (math.pi/180.0))
P("  dev vs π/180 = %+.4f%%" % (100.0*(ratio_pred - math.pi/180.0)/(math.pi/180.0)))

# 框架化 B₀ 检验：B₀ = m²c²α²/(eħ)（标准 Zeeman=束缚能）
ME = 9.1093837015e-31
C_L = 299792458.0
ALPHA = 7.2973525693e-3
B0_fw = ME*ME*C_L*C_L*ALPHA*ALPHA/(E_CH*HBAR)/1e4  # T→MG?  T = 1e4 G, MG = 1e6 G → T/100
P("\n[B₀ 框架化核验]")
P("  B₀(公式) = %.1f MG vs 2352.7 MG（dev %+.3f%%）" % (B0_fw/100.0, 100.0*(B0_fw/100.0-2352.7)/2352.7))

# 误差归因：r_20% 数值精度 vs 观测偏差
P("\n[误差归因]")
P("  总 dev +%.3f%%（B_pred vs 41）——来源候选：① tail_fraction 网格精度（20000 点）② 加权分布定义 ③ 观测 2352.7 拟合" % (100.0*(B_pred_MG-41.0)/41.0))
P("  若 r_20%% 精确 = RL_41 = %.6f（交叉点），B_pred = %.2f MG（dev %+.3f%%）" % (RL_41, HBAR*C2/(E_CH*(RL_41*A0)**2)/100.0, 100.0*(HBAR*C2/(E_CH*(RL_41*A0)**2)/100.0-41.0)/41.0))
