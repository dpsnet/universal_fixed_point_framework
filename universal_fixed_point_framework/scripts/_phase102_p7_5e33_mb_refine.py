# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-33：m_b 454.11 系数精化搜索
================================================================
目标：m_b = 4180 MeV——C²×454.11 = 4182.3（+0.0602%）——需要系数 453.8336
系统搜索：框架量两参数组合能否干净命中（容差 3e-4）
m_τ 精化模式（3/40 代数修正）是否在 m_b 复现？
"""
import math, json

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
dlam_P20 = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
C  = 2*math.sqrt(math.log(10))
C2 = C*C
kappa = 6/math.pi
Lam  = 16*math.log(10)*(dH+3)
kL   = kappa*Lam
sigma = 1/15
alpha_v = 1+sigma+math.sqrt(4/3/2)
alpha_t = math.log(7)
kmax, Ngen = 8, 3

m_b_pdg = 4180.0
target = m_b_pdg/C2
print("="*104)
print("P7-5e-33：m_b 454.11 系数精化搜索（目标系数 = %.6f）" % target)
print("="*104)
print("  C²×(2¹²/3²−1) = %.4f（%+.4f%%）——原系数 454.111 = 4096/9−1" % (C2*(4096/9-1), (C2*(4096/9-1)/m_b_pdg-1)*100))
print()

base = {
    "1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "5": 5.0, "6": 6.0, "7": 7.0, "8": 8.0, "9": 9.0,
    "kmax": kmax, "Ngen": Ngen, "kmax-1": kmax-1, "kmax-2": kmax-2,
    "Ngen!": math.factorial(Ngen), "2^12/3^2": 2**12/9,
    "dH": dH, "ln10": math.log(10), "ln2": math.log(2), "ln3": math.log(3),
    "ln15": dH, "pi": math.pi, "e": math.e,
    "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3), "sqrt5": math.sqrt(5), "sqrt10": math.sqrt(10),
    "C": C, "C2": C2, "kappa": kappa, "Lam": Lam, "kL": kL,
    "sigma": sigma, "sigma^2": sigma*sigma, "sigma^3": sigma**3,
    "alpha_v": alpha_v, "alpha_t": alpha_t,
    "dlam_EM": dlam_EM, "dlam_P20": dlam_P20,
    "dlam_EM/16": dlam_EM/16, "dlam_P20/16": dlam_P20/16,
    "3/40": 3/40,
}
multipliers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 32, 48, 64, 96, 128, 192, 193, 256, 454,
               1/2, 1/3, 1/4, 1/6, 1/8, 1/12, 1/16, 1/24, 1/32, 1/48, 1/64, 1/96, 1/128, 1/192, 1/256]
keys = list(base.keys())
hits = []
tol = 3e-4

def check(val, expr):
    if abs(val-target)/target < tol:
        hits.append((expr, val, (val/target-1)*100))

# 形式 1：a·x + b·y
for kx in keys:
    for ky in keys:
        if kx == ky: continue
        x, y = base[kx], base[ky]
        for a in [1,2,3,4,5,6,7,8,9,10,12,16,24,32,48,64,96,128,192,256,454]:
            for b in [1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8,9,-9,10,-10,12,-12,16,-16,24,-24,32,-32,48,-48,64,-64,96,-96,128,-128]:
                check(a*x+b*y, "%d·%s%+d·%s" % (a,kx,b,ky))

# 形式 2：a·x·y
for kx in keys:
    for ky in keys:
        if kx == ky: continue
        x, y = base[kx], base[ky]
        for a in multipliers:
            check(a*x*y, "%s·%s·%s" % (a,kx,ky))

# 形式 3：a·x/y
for kx in keys:
    for ky in keys:
        if kx == ky or abs(base[ky]) < 1e-9: continue
        x, y = base[kx], base[ky]
        for a in multipliers:
            check(a*x/y, "%s·%s/%s" % (a,kx,ky))

# 形式 4：a·x·(1 ± b·y)
for kx in keys:
    for ky in keys:
        if kx == ky: continue
        x, y = base[kx], base[ky]
        for a in multipliers:
            for b in [1/2,1/3,1/4,1/6,1/8,1/12,1/16,1/24,1/32,1/48,1/64,1/96,1/128,1/192,1/256,1/454]:
                check(a*x*(1+b*y), "%s·%s·(1+%s·%s)" % (a,kx,b,ky))
                check(a*x*(1-b*y), "%s·%s·(1-%s·%s)" % (a,kx,b,ky))

seen = set()
uniq = []
for expr, val, dev in hits:
    if expr not in seen:
        seen.add(expr); uniq.append((expr, val, dev))
uniq.sort(key=lambda t: abs(t[2]))

print("命中 %d 个（容差 %.0e）：" % (len(uniq), tol))
for expr, val, dev in uniq[:50]:
    print("  %-38s = %.6f（%+.4f%%）" % (expr, val, dev))
print()

json.dump([{"expr": e, "val": v, "dev_pct": d} for e,v,d in uniq],
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e33_mb_refine.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("JSON 落盘 ✓（%d 命中）" % len(uniq))
print("exit 0")
