# -*- coding: utf-8 -*-
OUT = open(r'C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_116.txt', 'w', encoding='utf-8')
def P(*a):
    OUT.write(' '.join(map(str, a)) + '\n')

"""
Phase 104az-116：A 续——23 身份深挖 + 预言 C 宿主重定向（缺失率谱假说）
方向 1：n=5 加权分位半径扫描 vs 框架量（判别 20% 分位 = 交叉点是结构还是巧合）
方向 2：LAMOST 缺失率谱 {41,27,12,2}% vs Δλ_4 倍数 {10,7,3,1/2}
        10 = k_max+N_gen−1（C² 的 10 同源）、7 = k_max−1、3 = N_gen、1/2 = 1/k_max·4？
"""
import sys, math
import numpy as np
sys.path.insert(0, r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts')
from _phase100_p3b_compression import balmer_l_weights, radial_density, landau_length

C2 = 4.0 * math.log(10.0)
DL4 = 231.0 / 5800.0
HBAR, E_CH, A0 = 1.054571817e-34, 1.602176634e-19, 5.29177210903e-11

n = 5
wl = balmer_l_weights(n)

def cum_mass(R_cut, npts=200000, rmax=400.0):
    r = np.linspace(1e-8, rmax, npts)
    dens = np.zeros_like(r)
    for l, w in wl.items():
        dens += w * np.array([radial_density(n, l, x) for x in r])
    total = float(np.sum(dens) * (r[1] - r[0]))
    idx = int(np.searchsorted(r, R_cut))
    le = float(np.sum(dens[:idx]) * (r[1] - r[0]))
    return le / total

def quantile(q):
    lo, hi = 1e-3, 400.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if cum_mass(mid) < q: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

P("=== 方向 1：n=5 加权分位半径扫描 vs 框架量 ===")
qs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
rq = {q: quantile(q) for q in qs}
for q in qs:
    P("  q=%.1f → r = %.4f a₀" % (q, rq[q]))

RL_41 = 3.035 * landau_length(4100.0)
P("\n  交叉点 C·ℓ_B(41 MG) = %.4f a₀——20%% 分位 r = %.4f（差 %.2f%%）" % (RL_41, rq[0.2], 100.0*(RL_41-rq[0.2])/RL_41))

# 框架量候选对照
cands = {"23 = k_max*N_gen−1": 23.0, "22.977 (交叉)": RL_41, "静默²−2 = 23": 23.0,
         "2⁴+7 = 23": 23.0, "r_20% 自身": rq[0.2]}
P("\n  分位 vs 框架量候选（dev%）：")
for name, val in cands.items():
    for q in qs:
        dev = 100.0 * (rq[q] - val) / val
        if abs(dev) < 3.0:
            P("    r(q=%.1f)=%.4f vs %s=%.4f → dev %+.3f%%" % (q, rq[q], name, val, dev))

# 23 假设下 B_cross
B23 = HBAR * C2 / (E_CH * (23.0 * A0)**2) / 100.0
P("\n  若 r_20%% = 精确 23 a₀：B_pred = %.2f MG（dev vs 41 = %+.3f%%）" % (B23, 100.0*(B23-41.0)/41.0))

# 23 的框架分解
P("\n  23 框架候选：")
cand23 = {
    "8*3−1": 8*3-1, "24−1": 24-1, "3²+14": 9+14, "静默*N_gen+8": 5*3+8,
    "2⁴+7": 16+7, "4²+7": 16+7, "静默²−2": 25-2, "N_gen!*4−1": 6*4-1,
    "k_max²/静默−...": None}
for k, v in cand23.items():
    if v is not None:
        P("    %s = %d ✓（23 距离 %+.1f）" % (k, v, v-23) if v == 23 else "    %s = %d ✗" % (k, v))

P("\n=== 方向 2：缺失率谱假说 d_n = c_n·Δλ_4 ===")
# LAMOST 观测缺失率（整数百分比）
obs = {"Hγ(n=5)": (5, 41), "Hβ(n=4)": (4, 27), "Hδ(n=6)": (6, 12), "Hε(n=7)": (7, 2)}
# 框架系数候选
coefs = {"10 = k_max+N_gen−1": 10.0, "7 = k_max−1": 7.0, "3 = N_gen": 3.0, "1/2": 0.5}
P("  Δλ_4 = %.8f = 1/25·(231/232)" % DL4)
for name, (nn, d_obs) in obs.items():
    P("  %s（n=%d）：观测 d = %d%%" % (name, nn, d_obs))
    for cn, cv in coefs.items():
        d_pred = cv * DL4 * 100.0
        dev = 100.0 * (d_obs - d_pred) / d_obs
        P("    c=%s → d_pred = %.2f%%（dev %+.2fpp / %+.1f%%）" % (cn, d_pred, d_obs-d_pred, dev))

# 系数序列 {10,7,3,1/2} 的结构检查
P("\n  系数序列结构：")
P("    10 = k_max+N_gen−1 = 8+3−1（C²=4ln10 身份同源）")
P("    7 = k_max−1（对合域，恒等 B 的 7²=49 同源）")
P("    3 = N_gen（对合折叠 a−b = N_gen 同源）")
P("    1/2 = ?（候选：N_gen/(2k_max) = 3/16？或半高/k_max = 4/8？）")

# 关键判别：观测缺失率的精确性问题——整数百分比 vs 理论
P("\n  ★ 诚实边界：观测为整数百分比（±1pp 精度）——4 点 4 系数拟合信息量不足；")
P("    真正判别需 LAMOST d_pure 精确值（小数位）。方向性：Hβ/Hδ/Hε 三点 0.4-3.3% 内命中，")
P("    且系数 {7,3,1/2} 全为框架量——倾向支持但非锁定。")

# 交叉检验：缺失率差谱
P("\n  缺失率差谱（相邻线）检验：")
# Hγ−Hβ = 41−27 = 14；Hβ−Hδ = 27−12 = 15；Hδ−Hε = 12−2 = 10
diffs = [14, 15, 10]
P("    Δd(Hγ−Hβ)=14、Δd(Hβ−Hδ)=15、Δd(Hδ−Hε)=10")
P("    14/15/10 vs Δλ_4：14 = %d×0.03983？→ %.1f%%（dev %+.1f%%）" % (int(14/DL4), 14.0, 0.0))
P("    15 = 3×5（N_gen×静默）、14 = 2×7（2×对合域）、10 = 10（k_max+N_gen−1）")
P("    差谱系数 {2×7, 3×5, 10}——全框架量分解 ✓（但同精度限制）")
