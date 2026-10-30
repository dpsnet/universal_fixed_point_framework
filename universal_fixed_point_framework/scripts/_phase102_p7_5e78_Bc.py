# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-78：束缚态消失临界场强 B_c(m)——势阱分析
================================================================
V_eff(r) = m²/(2r²) + m·B/2 + B²r²/8 − 1/r（母脚本哈密顿量对角项连续版）
对每个 m：扫描 B 找 V_eff 全局极小 V_min(B)——V_min < 0（束缚）/ > 0（自由）
B_c(m) = V_min = 0 的临界场强（经典判据；量子隧穿微移忽略）
判别：
  (a) B_c(-8) ≈ B_c(+1) → 同步收缩是势结构必然（9 缺口机制 = 势阱消失同步）
  (b) B_c(m) 序列是否框架量分数（/40 au 候选——0.225=9/40、0.25=10/40）
"""
import json, os
import numpy as np
from scipy.optimize import minimize_scalar, brentq
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def V_eff(r, m, B):
    return m**2 / (2.0 * r**2) + m * B / 2.0 + B**2 * r**2 / 8.0 - 1.0 / r

def V_min(m, B, r_lo=0.01, r_hi=80.0):
    # 数值找全局极小（log 空间更稳）
    rs = np.geomspace(r_lo, r_hi, 2000)
    vs = np.array([V_eff(r, m, B) for r in rs])
    i = int(np.argmin(vs))
    res = minimize_scalar(lambda r: V_eff(r, m, B), bounds=(rs[max(0,i-1)], rs[min(len(rs)-1,i+1)]),
                          method='bounded', options={'xatol': 1e-10})
    return res.fun

def B_c(m, B_lo=0.02, B_hi=0.6):
    # V_min 随 B 单调增（抗磁项正定）→ brentq 找 V_min=0
    def f(B):
        return V_min(m, B)
    # 先确认 V_min(B_lo) < 0（m 在低场有束缚）且 V_min(B_hi) > 0
    try:
        v_lo = f(B_lo)
        v_hi = f(B_hi)
        if v_lo < 0 < v_hi:
            return brentq(f, B_lo, B_hi, xtol=1e-9)
        elif v_lo < 0:
            return None  # B_hi 内未消失
        else:
            return B_lo  # 低场已无束缚（m 太大或正 m 升能）
    except Exception as e:
        return None

print("="*104)
print("P7-5e-78：束缚态消失临界场强 B_c(m)——势阱分析（V_min=0）")
print("="*104)

ms = list(range(-8, 3))
Bcs = {}
for m in ms:
    bc = B_c(m)
    Bcs[m] = bc
    status = "B_c=%.4f au（%.1f MG）" % (bc, bc*2350) if bc else ("未消失" if bc is None else "低场已自由")
    print("  m=%+d → %s" % (m, status), flush=True)

print()
print("【判别】")
print("-"*104)
bc_m8, bc_p1 = Bcs.get(-8), Bcs.get(1)
if bc_m8 and bc_p1:
    diff = abs(bc_m8 - bc_p1)
    print("  B_c(-8)=%.4f、B_c(+1)=%.4f、差=%.4f au（%.1f MG）" % (bc_m8, bc_p1, diff, diff*2350))
    print("  ★★ %s同步收缩的势结构解释" % ("支持" if diff < 0.02 else "不支持"))
print()
print("  B_c 序列（/40 au 候选——0.225=9/40、0.25=10/40 已命中）：")
for m in ms:
    bc = Bcs.get(m)
    if bc:
        x40 = bc * 40
        print("    m=%+d: B_c=%.4f = %.2f/40（框架量候选: 20=5·4, 9=N_gen², 10=配置基数, 12=N_gen·k_max/2, 14=2(k_max−1), 18=2N_gen²...）"
              % (m, bc, x40))

json.dump({str(m): (bc if bc is not None else None) for m, bc in Bcs.items()},
          open(os.path.join(BASE, "_phase102_p7_5e78_Bc.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
