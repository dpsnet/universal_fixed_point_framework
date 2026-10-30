# -*- coding: utf-8 -*-
"""Phase 104az-53：C=3.03 第一性定标检验——p=0.99 框架身份 + 41 精确化（独立脚本，无 import 副作用）"""
import math
import numpy as np
from _phase100_p3b_compression import eta_comp

names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}

def cross_field(n, target, C, lo=1.0, hi=1e5):
    assert eta_comp(n, lo, C) < target < eta_comp(n, hi, C), (n, eta_comp(n, lo, C), eta_comp(n, hi, C))
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if eta_comp(n, mid, C) < target:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo+hi)

# --- 1. p=0.99 的框架身份 ---
print("=== C 的第一性定标：p 的框架身份 ===")
Nc, Ngen, kmax = 3.0, 3.0, 8.0
sigma = 1.0/15.0
print("  1-p 候选：(Nc*sigma/2)^2 = %.6f (=1/100)  <- C_QCD*sigma^2 身份" % ((Nc*sigma/2.0)**2))
print("  1-p 候选：C_QCD*sigma^2 = (Nc/2)^2/225 = %.6f" % ((Nc/2.0)**2/225.0))
print("  dual_10 = Ngen+kmax-1 = %.0f -> ln10 = %.6f" % (Ngen+kmax-1, math.log(Ngen+kmax-1)))
C_1st = 2.0*math.sqrt(math.log(Ngen+kmax-1))
print("  C_1st = 2*sqrt(ln10) = %.5f" % C_1st)
print("  C(p=0.99 精确) = sqrt(2*ln100) = %.5f  <- 两者一致" % math.sqrt(2*math.log(100)))
print("  论文 C=3.03 vs C_1st=%.5f rel %.3f%%" % (C_1st, 100*abs(3.03-C_1st)/C_1st))

# --- 2. C_1st 的 45MG 四线 η_comp vs 论文 (0.530/0.806/0.905/0.945) ---
print("\n=== C_1st = 2√ln10 = %.5f：45 MG 四线 η_comp vs 论文 ===" % C_1st)
paper = {4: 0.530, 5: 0.806, 6: 0.905, 7: 0.945}
for n in (3, 4, 5, 6, 7):
    ec = eta_comp(n, 4500.0, C_1st)
    pv = paper.get(n)
    tag = "  vs 论文 %.3f (rel %.2f%%)" % (pv, 100*abs(ec-pv)/pv) if pv else ""
    print("  %s: η_comp = %.4f%s" % (names[n], ec, tag))

# --- 3. C_1st 的 0.8 交叉场强 ---
print("\n=== C_1st 的 η_comp=0.8 交叉场强 ===")
for n in (4, 5, 6, 7):
    B_MG = cross_field(n, 0.8, C_1st)/100.0
    print("  %s: B_0.8 = %.2f MG" % (names[n], B_MG))

# --- 4. 41 MG 处四线 η_comp（C_1st）---
print("\n=== 41 MG 处四线 η_comp（C_1st）===")
for n in (3, 4, 5, 6, 7):
    print("  %s: η_comp(41MG) = %.4f" % (names[n], eta_comp(n, 4100.0, C_1st)))

# --- 5. 41.4 的框架分解候选 ---
print("\n=== 41.4 vs 41 的框架分解候选 ===")
print("  41.4 = 40 + 7/5（k_max*N_total + (k_max-1)/N_total）")
print("  41.4 = 41×(1+1/100)（静默单元 × (Nc·σ/2)^2 修正）")
print("  41.43(C=3.03) vs 40+7/5=41.40: rel %.3f%%" % (100*abs(41.43-41.4)/41.4))
print("  41.43(C=3.03) vs 41×(1+1/100)=41.41: rel %.3f%%" % (100*abs(41.43-41.41)/41.41))

# --- 6. 反解 C*：η_comp(Hγ,41MG)=0.8 ---
print("\n=== 反解 C*：η_comp(Hγ, 41 MG)=0.8 ===")
lo, hi = 2.9, 3.2
for _ in range(60):
    mid = 0.5*(lo+hi)
    if eta_comp(5, 4100.0, mid) < 0.8:
        lo = mid
    else:
        hi = mid
Cstar = 0.5*(lo+hi)
pstar = 1.0 - math.exp(-Cstar*Cstar/2.0)
print("  C* = %.5f（η_comp(Hγ,41MG)=0.8 精确）" % Cstar)
print("  p* = 1-exp(-C*²/2) = %.5f" % pstar)
print("  1-p* = %.6f" % (1-pstar))
print("  C* vs 3.00: rel %.3f%% | vs 3.03: rel %.3f%% | vs C_1st=%.5f: rel %.3f%%" % (
    100*abs(Cstar-3.0)/3.0, 100*abs(Cstar-3.03)/3.03, C_1st, 100*abs(Cstar-C_1st)/C_1st))
print("  p* vs 0.99: rel %.3f%%" % (100*abs(pstar-0.99)/0.99))
