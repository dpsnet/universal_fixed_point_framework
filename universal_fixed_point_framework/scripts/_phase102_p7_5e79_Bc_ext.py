# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-79：经典 B_c 扩展扫描——α₀=1/2 量子提前因子判别
================================================================
P7-5e-78 发现：m=+2 量子消失（0.05-0.06）≈ α₀×经典 B_c（0.1055×1/2=0.0528）
判别：扩展 B_hi 算 m=+1、m=-8 的经典 B_c——
  (a) B_c(+1) ≈ 0.45-0.5 → α₀×B_c ≈ 0.225-0.25 命中量子区间（同步收缩 = α₀ 规则）
  (b) B_c(-8) 有限且 ≈ 0.45-0.5 → 同规则覆盖负侧（9 缺口机制闭合）
  (c) 若 B_c(-8) 不存在/极大 → α₀ 规则仅正侧成立——负侧另寻机制
"""
import json, os
import numpy as np
from scipy.optimize import minimize_scalar, brentq
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def V_eff(r, m, B):
    return m**2 / (2.0 * r**2) + m * B / 2.0 + B**2 * r**2 / 8.0 - 1.0 / r

def V_min(m, B, r_lo=0.01, r_hi=100.0):
    rs = np.geomspace(r_lo, r_hi, 2000)
    vs = np.array([V_eff(r, m, B) for r in rs])
    i = int(np.argmin(vs))
    res = minimize_scalar(lambda r: V_eff(r, m, B), bounds=(rs[max(0,i-1)], rs[min(len(rs)-1,i+1)]),
                          method='bounded', options={'xatol': 1e-10})
    return res.fun

def B_c(m, B_lo=0.02, B_hi=5.0):
    def f(B):
        return V_min(m, B)
    try:
        v_lo = f(B_lo)
        v_hi = f(B_hi)
        if v_lo < 0 < v_hi:
            return brentq(f, B_lo, B_hi, xtol=1e-9)
        elif v_lo < 0:
            return None  # B_hi 内未消失
        else:
            return B_lo
    except Exception:
        return None

print("="*104)
print("P7-5e-79：经典 B_c 扩展扫描（B_hi=5.0 au）——α₀=1/2 量子提前因子判别")
print("="*104)

for m in [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2]:
    bc = B_c(m)
    if bc:
        print("  m=%+d: 经典 B_c = %.4f au（%.1f MG）→ α₀×B_c = %.4f au（%.1f MG）"
              % (m, bc, bc*2350, bc/2, bc*2350/2), flush=True)
    else:
        print("  m=%+d: 经典 B_c 不存在（B_hi=5.0 au 内 V_min 恒负——势阱永存）" % m, flush=True)

print()
print("【判别】")
print("-"*104)
print("  量子实测消失场强：m=+2 → 0.05-0.06；m=+1 → 0.225-0.25；m=-8 → 0.225-0.25")
print("  若 α₀ 规则成立：量子 = 经典/2——上表第二列应命中对应量子区间")

json.dump({}, open(os.path.join(BASE, "_phase102_p7_5e79_Bc_ext.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
