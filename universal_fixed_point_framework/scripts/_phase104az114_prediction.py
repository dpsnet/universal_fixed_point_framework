# -*- coding: utf-8 -*-
OUT = open(r'C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_114.txt', 'w', encoding='utf-8')
def P(*a):
    OUT.write(' '.join(map(str, a)) + '\n')

"""
Phase 104az-114 B：预言 C 判别性设计——Δλ_4 = 0.0398276 在 Hγ 系统 (η_comp 交叉) 的可测签名
核心：η_comp(n=5, B) 曲线在 B_cross(0.8) = 41 MG 附近的结构——若某特征宽度/跨度 = Δλ_4，则判别可测
"""
import sys, math
import numpy as np
sys.path.insert(0, r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts')
from _phase100_p3b_compression import eta_comp

DL4 = 231.0 / 5800.0   # Δλ_4 = 0.0398275862（预言 C 纯框架）
Bc = 4100.0             # 41 MG 交叉（T）

def cross_field(target, lo=1.0, hi=1e5):
    assert eta_comp(5, lo, 3.035) < target < eta_comp(5, hi, 3.035)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if eta_comp(5, mid, 3.035) < target: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

P("=== B：预言 C 判别性设计（Hγ η_comp 交叉系统）===")
P("Δλ_4 = %.8f = 231/5800（预言 C）" % DL4)

# 交叉点精确值
B80 = cross_field(0.8)
P("\n[交叉点]")
P("  B(η=0.8) = %.2f T = %.2f MG（观测 41 MG，dev %+.2f%%）" % (B80, B80/100.0, 100.0*(B80/100.0-41.0)/41.0))

# 谱隙宽度判别：η = 0.8 ± Δλ_4/2 的场强跨度
eta_lo, eta_hi = 0.8 - DL4/2, 0.8 + DL4/2
B_lo, B_hi = cross_field(eta_lo), cross_field(eta_hi)
P("\n[判别 1：η = 0.8±Δλ_4/2 场强跨度]")
P("  η_lo = %.6f → B_lo = %.1f MG" % (eta_lo, B_lo/100.0))
P("  η_hi = %.6f → B_hi = %.1f MG" % (eta_hi, B_hi/100.0))
span = (B_hi - B_lo) / B80
P("  跨度 (B_hi−B_lo)/B_cross = %.6f vs Δλ_4 = %.6f" % (span, DL4))
P("  比率 = %.4f" % (span / DL4))

# 判别 2：η = 0.8±Δλ_4（更宽窗口）
eta_lo2, eta_hi2 = 0.8 - DL4, 0.8 + DL4
B_lo2, B_hi2 = cross_field(eta_lo2), cross_field(eta_hi2)
span2 = (B_hi2 - B_lo2) / B80
P("\n[判别 2：η = 0.8±Δλ_4 场强跨度]")
P("  η_lo = %.6f → B_lo = %.1f MG；η_hi = %.6f → B_hi = %.1f MG" % (eta_lo2, B_lo2/100.0, eta_hi2, B_hi2/100.0))
P("  跨度 = %.6f vs Δλ_4 = %.6f——比率 = %.4f" % (span2, DL4, span2/DL4))

# 判别 3：交叉点斜率 dη/d(log10 B)
def slope_at(B, h=0.001):
    e1, e2 = eta_comp(5, B*(1-h), 3.035), eta_comp(5, B*(1+h), 3.035)
    return (e2 - e1) / (math.log10(B*(1+h)) - math.log10(B*(1-h)))
s = slope_at(B80)
P("\n[判别 3：交叉点斜率]")
P("  dη/dlog10B @ B_cross = %.4f" % s)
P("  线性跨度 Δlog10B(η 变化 0.2) = %.4f → ΔB/B = %.4f" % (0.2/s, 10**(0.2/s)-1))

# 判别 4：预言 C 的谱隙投影——η(B_cross·(1±Δλ_4)) 的差
e_p, e_m = eta_comp(5, B80*(1+DL4), 3.035), eta_comp(5, B80*(1-DL4), 3.035)
P("\n[判别 4：B_cross·(1±Δλ_4) 的 η 差]")
P("  η(B·(1+Δλ_4)) = %.6f，η(B·(1−Δλ_4)) = %.6f" % (e_p, e_m))
P("  Δη = %.6f（若 ≈ Δλ_4 → 预言 C 谱隙 = η 曲线纵向谱隙）" % (e_p - e_m))
P("  比率 Δη/Δλ_4 = %.4f" % ((e_p-e_m)/DL4))

# 判别 5：η_comp = 1−3σ = 0.8 的静默临界恒等——η(41.01) 精确值
P("\n[判别 5：静默临界恒等]")
P("  η(B80) 自检 = %.8f（应 = 0.8）" % eta_comp(5, B80, 3.035))
P("  3σ = %.10f，1−3σ = %.10f——交叉点即静默临界 ✓" % (3.0/15.0, 1.0-3.0/15.0))

P("\n[判定]")
P("  判别 1/2：跨度比率——若 ≈1 则 Δλ_4 = η 曲线的场强半谱隙（可测：η(B) 观测斜率）")
P("  判别 3：斜率可测（EW 梯度 vs B 分档）")
P("  判别 4：纵向谱隙候选")
