# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-32：m_τ 193 系数精化搜索
================================================================
目标：m_τ = 1776.86 MeV——C²×193 = 1777.60（+0.0414%）——需要系数 192.925
系统搜索：框架量两参数组合能否干净命中 192.925（容差 3e-4，即 0.03% 内）
若命中 → 谱隙链最大偏差消解 + v/m_t 链（现依赖 PDG m_τ）内生闭合候选
"""
import math, itertools

# 框架量基础
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

m_tau_pdg = 1776.86
target = m_tau_pdg/C2        # 需要的系数 = 192.925
print("="*104)
print("P7-5e-32：m_τ 193 系数精化搜索（目标系数 = %.6f）" % target)
print("="*104)
print("  C²×193 = %.4f（%+.4f%%）——193 = 2⁶·3¹+1 偏差来源" % (C2*193, (C2*193/m_tau_pdg-1)*100))
print()

# 基础量集合（含组合）
base = {
    "1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "5": 5.0, "6": 6.0, "7": 7.0, "8": 8.0,
    "kmax": kmax, "Ngen": Ngen, "kmax-1": kmax-1, "kmax-2": kmax-2,
    "Ngen!": math.factorial(Ngen),
    "dH": dH, "ln10": math.log(10), "ln2": math.log(2), "ln3": math.log(3),
    "ln15": dH, "pi": math.pi, "e": math.e,
    "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3), "sqrt5": math.sqrt(5),
    "sqrt10": math.sqrt(10), "sqrt(C_F/2)": math.sqrt(4/3/2),
    "C": C, "C2": C2, "kappa": kappa, "Lam": Lam, "kL": kL,
    "sigma": sigma, "sigma^2": sigma*sigma, "sigma^3": sigma**3,
    "alpha_v": alpha_v, "alpha_t": alpha_t,
    "dlam_EM": dlam_EM, "dlam_P20": dlam_P20,
    "dlam_EM/16": dlam_EM/16, "dlam_P20/16": dlam_P20/16,
}

# 两参数组合搜索：a·x + b·y 和 a·x·y 和 a·x/y（x,y 取自 base，a 取自小整数/倒数集）
multipliers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 32, 48, 64, 96, 128, 192, 193,
               1/2, 1/3, 1/4, 1/6, 1/8, 1/12, 1/16, 1/24, 1/32, 1/48, 1/64, 1/96, 1/128, 1/192, 1/193]
keys = list(base.keys())
hits = []
tol = 3e-4

def check(val, expr):
    global hits
    if abs(val-target)/target < tol:
        hits.append((expr, val, (val/target-1)*100))

# 形式 1：a·x + b·y（b 也取小乘数）
for kx in keys:
    for ky in keys:
        if kx == ky: continue
        x, y = base[kx], base[ky]
        for a in [1,2,3,4,5,6,7,8,9,10,12,16,24,32,48,64,96,128,192]:
            for b in [1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8,9,-9,10,-10,12,-12,16,-16,24,-24,32,-32,48,-48,64,-64,96,-96]:
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

# 形式 4：a·(x ± b·y)——括号形式（谱隙修正风格）
for kx in keys:
    for ky in keys:
        if kx == ky: continue
        x, y = base[kx], base[ky]
        for a in multipliers:
            for b in [1/2,1/3,1/4,1/6,1/8,1/12,1/16,1/24,1/32,1/48,1/64,1/96,1/128,1/192,1/193]:
                check(a*x*(1+b*y), "%s·%s·(1+%s·%s)" % (a,kx,b,ky))
                check(a*x*(1-b*y), "%s·%s·(1-%s·%s)" % (a,kx,b,ky))

# 去重排序
seen = set()
uniq = []
for expr, val, dev in hits:
    if expr not in seen:
        seen.add(expr); uniq.append((expr, val, dev))
uniq.sort(key=lambda t: abs(t[2]))

print("命中 %d 个（容差 %.0e，目标 %.6f）：" % (len(uniq), tol, target))
for expr, val, dev in uniq[:40]:
    print("  %-34s = %.6f（%+.4f%%）" % (expr, val, dev))
print()

# 输出所有命中到 JSON
import json
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e32_mtau_refine.json", "w", encoding="utf-8") as f:
    json.dump([{"expr": e, "val": v, "dev_pct": d} for e,v,d in uniq], f, ensure_ascii=False, indent=2)
print("JSON 落盘：scripts/_phase102_p7_5e32_mtau_refine.json（%d 命中）" % len(uniq))
print()
print("exit 0")
