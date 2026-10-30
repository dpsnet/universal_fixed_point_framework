# -*- coding: utf-8 -*-
"""
Phase 102 P7-1 续-7：Λ/M_Pl 缺口 4.22× 框架身份搜索
==============================================================================
P7-1 已登记：Λ_pert/M_Pl = exp(−8π²/(b_0Δλ_3))，b_0=(11N_c−2N_f)/3=9（标准 RG 系数）
3圈口径精确缺口 = 1.7224e−20 / 4.0811e−21 = 4.220（目标 210.3 MeV = F_π 定标有效值）
4圈+√N_c 后 1.86×（但 b3 外部、√N_c 已用于 ξ——不优先）
攻点：4.220 的框架身份——若命中，Λ 从"实验定标"升格"框架量"
"""
import math, json, itertools

D_H = 2.7095
SIGMA = 1/15.0
K_MAX = 8.0
N_GEN = 3.0
KAPPA = 6/math.pi
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
DL3 = math.sqrt(2)*DL_MIN

def dev(f, e): return (f/e-1)*100

print("P7-1 续-7：Λ/M_Pl 缺口 4.220 框架身份搜索")
print("="*74)
print("  目标 4.220（3圈口径，全框架）；Λ_eff = 210.3 MeV 是 F_π 定标有效值")

print("\n[预检] 候选结构：")
cands = {
    "3√2·(1−Δλ_min/5.4)": 3*math.sqrt(2)*(1-DL_MIN/5.4),
    "ξ²×√2": 3*math.sqrt(2),
    "κ²+ln2": 3.6476+0.6931,
    "2π/1.489": 2*math.pi/1.489,
    "√6+√3": math.sqrt(6)+math.sqrt(3),
    "2√3+σ": 2*math.sqrt(3)+SIGMA,
}
for name, v in cands.items():
    print("  %s = %.5f（偏差 %+.3f%%）" % (name, v, dev(v, 4.22)))

print("\n[系统搜索] 两参数 a·X ± b·Y（目标 4.220，容差 <0.5%%）")
pool = {"d_H": D_H, "ln15": math.log(15), "ln16": math.log(16), "ln7": math.log(7),
        "κ": KAPPA, "π": math.pi, "e": math.e, "Δλ_min": DL_MIN, "Δλ₃": DL3, "σ": SIGMA,
        "√2": math.sqrt(2), "√3": math.sqrt(3), "√6": math.sqrt(6),
        "ln2": math.log(2), "ln3": math.log(3), "ln5": math.log(5),
        "2": 2.0, "3": 3.0, "5": 5.0, "7": 7.0, "8": 8.0, "16": 16.0,
        "N_c": 3.0, "ξ=√N_c": math.sqrt(3.0), "κ²": KAPPA**2}
coeffs = list(range(1, 21)) + [0.5, 1/3, 1/4, 1/6, 1/8, 1/16]
hits = []
for (nx, X), (ny, Y) in itertools.combinations(pool.items(), 2):
    for a in coeffs:
        for b in coeffs:
            for sign in [1, -1]:
                v = sign*a*X + b*Y
                d = dev(v, 4.22)
                if abs(d) < 0.5:
                    hits.append((abs(d), d, "%s%d·%s + %d·%s" % ("−" if sign<0 else "+", a, nx, b, ny)))
hits.sort()
print("  <0.5%% 命中数：%d" % len(hits))
for ad, d, s in hits[:15]:
    print("    [%+.4f%%] %s" % (d, s))

print("\n[判定]")
print("  4.220 框架身份：若上表无全框架干净命中——缺口 4.22 维持开放（登记：圈阶通道穷尽）")
print("  候选注意：ξ²×√2 = 4.2426（+0.54%%——边缘外）；√6+√3 = 4.1813（−0.92%%）")

result = {"gap": 4.220, "hits": len(hits), "best": hits[0] if hits else None}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_1_gap422.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
