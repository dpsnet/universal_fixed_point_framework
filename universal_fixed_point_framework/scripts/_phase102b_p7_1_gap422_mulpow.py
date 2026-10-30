# -*- coding: utf-8 -*-
"""
Phase 102b P7-1 续-8：Λ/M_Pl 缺口 4.220 乘除/幂次组合搜索（未覆盖域）
==============================================================================
P7-1 续-7 已搜：加法组合 a·X ± b·Y（226 命中，口径依赖不立）
本脚本补搜：乘除组合（a·X·Y、a·X/Y）+ 幂次组合（X^p、X^a·Y^b）
目标：4.220（3 圈口径全框架缺口）
"""
import math, json, itertools

D_H = 2.7095
SIGMA = 1/15.0
K_MAX = 8.0
N_GEN = 3.0
KAPPA = 6/math.pi
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
DL3 = math.sqrt(2)*DL_MIN
TARGET = 4.220

def dev(f, e): return (f/e-1)*100

print("Phase 102b P7-1 续-8：缺口 4.220 乘除/幂次组合搜索")
print("="*74)

pool = {"d_H": D_H, "ln15": math.log(15), "ln16": math.log(16), "ln7": math.log(7),
        "κ": KAPPA, "π": math.pi, "e": math.e, "Δλ_min": DL_MIN, "Δλ₃": DL3, "σ": SIGMA,
        "√2": math.sqrt(2), "√3": math.sqrt(3), "√6": math.sqrt(6),
        "ln2": math.log(2), "ln3": math.log(3), "ln5": math.log(5),
        "2": 2.0, "3": 3.0, "5": 5.0, "7": 7.0, "8": 8.0, "16": 16.0,
        "N_c": 3.0, "ξ=√N_c": math.sqrt(3.0), "κ²": KAPPA**2, "C_QCD=9/4": 2.25,
        "2+√3": 2+math.sqrt(3), "2π/3": 2*math.pi/3, "σ⁻¹=15": 15.0}

# [A] 乘除组合：a·X·Y 与 a·X/Y
hits_mul = []
for (nx, X), (ny, Y) in itertools.combinations(pool.items(), 2):
    for a in [1, 2, 3, 4, 0.5, 1/3, 0.25]:
        for v, expr in [(a*X*Y, "%g·%s·%s" % (a, nx, ny)), (a*X/Y, "%g·%s/%s" % (a, nx, ny)), (a*Y/X, "%g·%s/%s" % (a, ny, nx))]:
            d = dev(v, TARGET)
            if abs(d) < 0.3:
                hits_mul.append((abs(d), d, expr))
hits_mul.sort()
print("\n[A] 乘除组合 <0.3%% 命中：%d" % len(hits_mul))
for ad, d, s in hits_mul[:12]:
    print("    [%+.4f%%] %s = %.5f" % (d, s, TARGET*(1+d/100)))

# [B] 幂次组合：X^p 与 X^a·Y^b（a,b ∈ 简单有理数）
fracs = [1, 2, 3, 4, 0.5, 1/3, 0.25, 2/3, 3/2, -1, -0.5, -2]
hits_pow = []
for (nx, X), (ny, Y) in itertools.combinations(pool.items(), 2):
    for a in fracs:
        for b in fracs:
            if abs(a)+abs(b) == 0: continue
            v = X**a * Y**b
            d = dev(v, TARGET)
            if abs(d) < 0.3:
                hits_pow.append((abs(d), d, "%s^%g · %s^%g" % (nx, a, ny, b)))
# 单量幂
for nx, X in pool.items():
    for a in fracs:
        v = X**a
        d = dev(v, TARGET)
        if abs(d) < 0.3:
            hits_pow.append((abs(d), d, "%s^%g" % (nx, a)))
hits_pow.sort()
print("\n[B] 幂次组合 <0.3%% 命中：%d" % len(hits_pow))
for ad, d, s in hits_pow[:15]:
    print("    [%+.4f%%] %s = %.5f" % (d, s, TARGET*(1+d/100)))

print("\n[机制预检候选]")
cands = {
    "ξ²√2 = 3√2": 3*math.sqrt(2),
    "2π·2/3": 4*math.pi/3,
    "2+√3": 2+math.sqrt(3),
    "C_QCD×(2+√3)/2.08": 2.25*(2+math.sqrt(3))/2.08,
    "κ·(2+√3)/1.333": KAPPA*(2+math.sqrt(3))/1.333,
    "4·(1+3σ/4)": 4*(1+3*SIGMA/4),
}
for name, v in cands.items():
    print("  %-24s = %.5f（偏差 %+.3f%%）" % (name, v, dev(v, TARGET)))

result = {"gap": TARGET, "mul_hits": len(hits_mul), "pow_hits": len(hits_pow),
          "best_mul": hits_mul[0] if hits_mul else None,
          "best_pow": hits_pow[0] if hits_pow else None}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102b_p7_1_gap422_mulpow.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
