# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-37：m_e 系数精化搜索
================================================================
目标：m_e = 0.51099895 MeV——C²×(1−Δλ_EM/16)/18 = 0.510949（−0.0092%）——需要系数 0.0554813
系统搜索：框架量组合能否干净命中（容差 3e-4）
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

m_e_pdg = 0.51099895
target = m_e_pdg/C2
print("="*104)
print("P7-5e-37：m_e 系数精化搜索（目标系数 = %.8f）" % target)
print("="*104)
print("  原式：C²×(1−Δλ_EM/16)/18 = %.6f（%+.4f%%）——(1−Δλ/16)/18 = %.8f" % (C2*(1-dlam_EM/16)/18, (C2*(1-dlam_EM/16)/18/m_e_pdg-1)*100, (1-dlam_EM/16)/18))
print("  需要的谱隙修正 δ = 1−18×%.8f = %.8f vs Δλ_EM/16 = %.8f（差 %+.2f%%）" % (target, 1-18*target, dlam_EM/16, (1-18*target)/(dlam_EM/16)*100-100))
print()

base = {
    "1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "5": 5.0, "6": 6.0, "7": 7.0, "8": 8.0, "9": 9.0,
    "kmax": kmax, "Ngen": Ngen, "kmax-1": kmax-1, "kmax-2": kmax-2, "Ngen!": math.factorial(Ngen),
    "dH": dH, "ln10": math.log(10), "ln2": math.log(2), "ln3": math.log(3), "ln7": alpha_t,
    "pi": math.pi, "e": math.e, "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3),
    "sqrt5": math.sqrt(5), "sqrt10": math.sqrt(10), "C": C, "C2": C2,
    "kappa": kappa, "Lam": Lam, "kL": kL, "sigma": sigma, "sigma^2": sigma*sigma, "sigma^3": sigma**3,
    "alpha_v": alpha_v, "alpha_t": alpha_t, "dlam_EM": dlam_EM, "dlam_P20": dlam_P20,
    "dlam_EM/16": dlam_EM/16, "dlam_P20/16": dlam_P20/16, "3/40": 3/40,
    "1/18": 1/18, "3/8": 3/8, "81/8": 81/8,
}
keys = list(base.keys())
hits = []
tol = 3e-4

def check(val, expr):
    if abs(val-target)/target < tol:
        hits.append((expr, val, (val/target-1)*100))

# 形式 1：a·x（含修正因子）
for kx in keys:
    x = base[kx]
    for a in [1,2,3,4,5,6,7,8,9,10,12,16,18,24,32,48,64,96,128,192,256, 1/2,1/3,1/4,1/6,1/8,1/9,1/12,1/16,1/18,1/24,1/32,1/48,1/64,1/96,1/128,1/192,1/256]:
        check(a*x, "%s·%s" % (a,kx))

# 形式 2：a·x/y
for kx in keys:
    for ky in keys:
        if kx == ky or abs(base[ky]) < 1e-9: continue
        x, y = base[kx], base[ky]
        for a in [1,2,3,4,5,6,7,8,9,10,12,16,18,24,32,48,64,96,128,192,256, 1/2,1/3,1/4,1/6,1/8,1/9,1/12,1/16,1/18,1/24,1/32,1/48,1/64,1/96,1/128,1/192,1/256]:
            check(a*x/y, "%s·%s/%s" % (a,kx,ky))

# 形式 3：a·x·(1 ± b·y)
for kx in keys:
    for ky in keys:
        if kx == ky: continue
        x, y = base[kx], base[ky]
        for a in [1,2,3,4,5,6,7,8,9,10,12,16,18,24,32,48,64,96,128,192,256, 1/2,1/3,1/4,1/6,1/8,1/9,1/12,1/16,1/18,1/24,1/32,1/48,1/64,1/96,1/128,1/192,1/256]:
            for b in [1/2,1/3,1/4,1/6,1/8,1/12,1/16,1/24,1/32,1/48,1/64,1/96,1/128,1/192,1/256]:
                check(a*x*(1+b*y), "%s·%s·(1+%s·%s)" % (a,kx,b,ky))
                check(a*x*(1-b*y), "%s·%s·(1-%s·%s)" % (a,kx,b,ky))

seen = set()
uniq = []
for expr, val, dev in hits:
    if expr not in seen:
        seen.add(expr); uniq.append((expr, val, dev))
uniq.sort(key=lambda t: abs(t[2]))

print("命中 %d 个（容差 %.0e）：" % (len(uniq), tol))
for expr, val, dev in uniq[:60]:
    print("  %-42s = %.8f（%+.4f%%）" % (expr, val, dev))
print()

json.dump([{"expr": e, "val": v, "dev_pct": d} for e,v,d in uniq],
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e37_me_refine.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("JSON 落盘 ✓（%d 命中）" % len(uniq))
print("exit 0")
