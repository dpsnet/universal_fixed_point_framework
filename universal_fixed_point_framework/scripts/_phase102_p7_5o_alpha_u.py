# -*- coding: utf-8 -*-
"""
Phase 102 P7-5o：α_u^eff = 1.983 框架化（Formula B^β 修复项）
==============================================================================
paper17 §5.3（L325）：β_u = α_u^eff/α_v = 1.983/1.883 ≈ 1.0531（Sp 谱流合成律 定理 4.3）
§5.2：α_u^eff = 1.983 是扫描优化值（[1.80,2.30] 内 MSE < 1e−30 精确拟合）
粗查候选：α_v + 1/(N_gen+k_max−1) = 1.883163+0.1 = 1.983163（+0.008%）——10 = N_gen+k_max−1（m_N 候选 κ²Λ/10 同源）
          2−σ/4 = 1.983333（+0.017%）——松散
"""
import math, json, itertools

D_H = 2.7095
SIGMA = 1/15.0
K_MAX = 8.0
N_GEN = 3.0
KAPPA = 6/math.pi
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
ALPHA_V_FW = 16/15 + math.sqrt(2/N_GEN)   # P7-5j 框架 α_v

def dev(f, e): return (f/e-1)*100

print("P7-5o：α_u^eff = 1.983 框架化")
print("="*74)
print("  语境：β_u = α_u^eff/α_v = 1.983/1.883 = 1.0531（paper17 §5.3，Sp 谱流合成律）")
print("  α_u^eff = 1.983 是扫描优化值——框架化后从'拟合参数'升格'框架量'")

print("\n[预检] 候选：")
c1 = ALPHA_V_FW + 1/(N_GEN+K_MAX-1)
print("  α_v+1/(N_gen+k_max−1) = %.6f+%.4f = %.6f（偏差 %+.4f%%）——10=N_gen+k_max−1 与 m_N 候选同源" % (ALPHA_V_FW, 1/(N_GEN+K_MAX-1), c1, dev(c1, 1.983)))
c2 = 2 - SIGMA/4
print("  2−σ/4 = %.6f（偏差 %+.4f%%）——σ/4=1/60 松散" % (c2, dev(c2, 1.983)))
c3 = ALPHA_V_FW + N_GEN*SIGMA/2
print("  α_v+N_gen·σ/2 = %.6f（偏差 %+.4f%%）——同 1/10 式" % (c3, dev(c3, 1.983)))
beta = c1/ALPHA_V_FW
print("  β_u = α_u^eff/α_v = %.6f（paper17 用 1.0531——偏差 %+.4f%%）" % (beta, dev(beta, 1.0531)))

print("\n[系统搜索] 两参数 a·X ± b·Y（目标 1.983）")
pool = {"d_H": D_H, "ln15": math.log(15), "ln16": math.log(16), "ln7": math.log(7),
        "κ": KAPPA, "π": math.pi, "e": math.e, "Δλ_min": DL_MIN, "σ": SIGMA,
        "√2": math.sqrt(2), "√3": math.sqrt(3), "√6": math.sqrt(6),
        "ln2": math.log(2), "ln3": math.log(3), "ln5": math.log(5),
        "2": 2.0, "3": 3.0, "5": 5.0, "7": 7.0, "8": 8.0, "16": 16.0,
        "α_v": ALPHA_V_FW}
coeffs = list(range(1, 21)) + [0.5, 1/3, 1/4, 1/6]
hits = []
for (nx, X), (ny, Y) in itertools.combinations(pool.items(), 2):
    for a in coeffs:
        for b in coeffs:
            for sign in [1, -1]:
                v = sign*a*X + b*Y
                d = dev(v, 1.983)
                if abs(d) < 0.05:
                    hits.append((abs(d), d, "%s%d·%s %s%d·%s" % ("+" if sign>0 else "-", a, nx, "+" if b>0 else "", b, ny)))
hits.sort()
print("  <0.05%% 命中数：%d" % len(hits))
for ad, d, s in hits[:12]:
    print("    [%+.4f%%] %s" % (d, s))

print("\n[判定]")
print("  ★ 候选：α_u^eff = α_v + 1/(N_gen+k_max−1) = 1.883163+0.1 = %.6f（+0.0082%%）——全框架" % c1)
print("    结构：α_v（P7-5j 框架）+ 1/10（10 = N_gen+k_max−1，与 m_N 候选 κ²Λ/10 同源）")
print("    β_u = %.5f（paper17 用 1.0531——偏差 +0.0002%% 一致）——Formula B^β 修复链闭合" % beta)
print("  诚实边界：① α_u^eff = 1.983 本身是扫描优化值（非解析输入）——目标精度口径软 ② 1/10 修正的物理意义（为何上型夸克比 v 多 1/10）未推导 ③ 候选级达标")

result = {"alpha_u_cand": c1, "dev": dev(c1, 1.983), "beta_u": beta, "beta_u_dev": dev(beta, 1.0531)}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5o_alpha_u.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
