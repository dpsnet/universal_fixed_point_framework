# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-96：65 框架身份系统搜索
================================================================
目标：1/65 修正（m=-1 边界态）的第二实例与精确框架身份
框架量集合：σ、k_max、N_gen、N_Weyl、α₀、d_H、s=e^-1、κ=6/π、
C_F=4/3、α_v、α_t=ln7、Λ、κΛ、Δλ_min^(EM)、Δλ_min(P20)、C²、e
搜索：两参数四则组合命中 65（±0.01%）与 1/65（±0.01%）
另检查：65 = 5×13（(k_max−N_gen)·(2k_max−N_gen)）、24·d_H ≈ 65
"""
import json, os
import math
from itertools import product

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

q = {
    "sigma": 1.0/15.0, "k_max": 8.0, "N_gen": 3.0, "N_Weyl": 4.0,
    "alpha0": 0.5, "dH": math.log(15.0), "s": math.e**-1, "kappa": 6.0/math.pi,
    "CF": 4.0/3.0, "alpha_v": 1.88317, "alpha_t": math.log(7.0),
    "Lambda": 210.292, "kL": 401.629,
    "dlam_EM": math.pi/(24.0*math.log(15.0)+72.0),
    "dlam_P20": (math.sqrt(6.0)-math.sqrt(2.0))/math.sqrt(72.0),
    "C2": 4.0*math.log(10.0), "e": math.e,
}
names = list(q.keys())
vals = list(q.values())

print("="*104)
print("P7-5e-96：65 框架身份系统搜索（两参数组合）")
print("="*104)

hits_65, hits_inv65 = [], []
for (n1, v1), (n2, v2) in product(zip(names, vals), repeat=2):
    if n1 == n2:
        continue
    combos = {
        "a+b": v1+v2, "a-b": v1-v2, "b-a": v2-v1,
        "a*b": v1*v2, "a/b": v1/v2, "b/a": v2/v1,
        "a^2+b": v1**2+v2, "a^2-b": v1**2-v2,
        "a+b^2": v1+v2**2, "a*b^2": v1*v2**2, "a^2*b": v1**2*v2,
        "a/b^2": v1/v2**2, "b/a^2": v2/v1**2, "a^2/b": v1**2/v2,
    }
    for label, val in combos.items():
        if abs(val - 65.0)/65.0 < 2e-4:
            hits_65.append((n1, n2, label, val, (val-65.0)/65.0*100))
        if abs(val - 1.0/65.0)/(1.0/65.0) < 2e-4:
            hits_inv65.append((n1, n2, label, val, (val-1.0/65.0)/(1.0/65.0)*100))

print("\n★ 命中 65（±0.02%）：")
for h in sorted(hits_65, key=lambda x: abs(x[4]))[:15]:
    print("   %-6s %-10s %-8s = %.8f（差 %+.5f%%）" % (h[0], h[1], h[2], h[3], h[4]))
print("\n★ 命中 1/65（±0.02%）：")
for h in sorted(hits_inv65, key=lambda x: abs(x[4]))[:15]:
    print("   %-6s %-10s %-8s = %.8f（差 %+.5f%%）" % (h[0], h[1], h[2], h[3], h[4]))

print("\n★ 特殊候选检验：")
cand = [
    ("24·dH（k_max·N_gen·dH）", 24.0*q["dH"]),
    ("(k_max−N_gen)·(2k_max−N_gen) = 5×13", (8-3)*(16-3)),
    ("k_max² + k_max·α₀³", 64.0+8.0*0.5**3),
    ("k_max·N_gen·dH+1", 24.0*q["dH"]+1),
    ("2^6+1", 65.0),
    ("C²·7.056", q["C2"]*7.056),
    ("κΛ/6.18", q["kL"]/6.18),
    ("1/α_EM/2.108", 137.028/2.108),
]
for label, val in cand:
    print("   %-40s = %.8f（vs 65 差 %+.4f%%）" % (label, val, (val-65.0)/65.0*100))

json.dump({"hits_65": hits_65[:15], "hits_inv65": hits_inv65[:15],
           "d24": 24.0*q["dH"], "d24_dev": (24.0*q["dH"]-65)/65*100,
           "prod513": 65.0},
          open(os.path.join(BASE, "_phase102_p7_5e96_65_identity.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
