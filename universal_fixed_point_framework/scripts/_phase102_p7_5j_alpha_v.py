# -*- coding: utf-8 -*-
"""
Phase 102 P7-5j：α_v 框架身份搜索（v 框架化后的派生量重验）
==============================================================================
背景：α_v = 1.883（paper11 §8.4，由 v = m_t×c₁^{α_v−α_t} 反推，α_t = 1.945）
精确反推：α_v = α_t + ln(v/m_t)/ln(c₁)
   v = 246.11 GeV（P7-5i 框架）、m_t = 172.7 GeV（实验）、c₁ = e^{−(d_H+3)}（框架）
目标：α_v 的直接框架表达（两参数组合 + 单量×整数）
已知候选：ln7−Δλ_min/2 = 1.88490（+0.096% 边缘）、2−7σ/4 = 1.883333（2 无身份）
"""
import math, json, itertools

# 输入
V_FW = 246.11         # GeV（P7-5i 框架）
M_T = 172.7           # GeV 实验
ALPHA_T = 1.945       # paper11 用值
D_H = 2.7095
C1 = math.exp(-(D_H+3))   # 框架 c₁ = e^{−(d_H+3)}
SIGMA = 1/15.0
K_MAX = 8.0
N_GEN = 3.0
KAPPA = 6/math.pi
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
DL3 = math.sqrt(2)*DL_MIN

# 精确反推 α_v
alpha_v_exp = ALPHA_T + math.log(V_FW/M_T)/math.log(C1)
print("P7-5j：α_v 框架身份搜索")
print("="*72)
print("  反推：α_v = α_t + ln(v/m_t)/ln(c₁) = 1.945 + ln(%.2f/%.1f)/ln(%.6f)" % (V_FW, M_T, C1))
print("       = 1.945 + %.5f/%.5f = %.6f（paper11 用值 1.883）" % (math.log(V_FW/M_T), math.log(C1), alpha_v_exp))

# 已知候选
print("\n  [已知候选复核]")
c1_ = math.log(7) - DL_MIN/2
c2_ = 2 - 7*SIGMA/4
print("    ln7−Δλ_min/2 = %.6f（偏差 %+.4f%%）" % (c1_, (c1_/alpha_v_exp-1)*100))
print("    2−7σ/4 = %.6f（偏差 %+.4f%%）——2 无身份" % (c2_, (c2_/alpha_v_exp-1)*100))

# 系统搜索
pool = {
    "d_H": D_H, "ln15": math.log(15), "ln16": math.log(16), "ln7": math.log(7),
    "ln8": math.log(8), "σ": SIGMA, "1−σ": 1-SIGMA, "κ": KAPPA,
    "Δλ_min": DL_MIN, "Δλ3": DL3, "e": math.e, "π": math.pi,
    "√2": math.sqrt(2), "√3": math.sqrt(3), "√6": math.sqrt(6),
    "ln2": math.log(2), "ln3": math.log(3), "ln5": math.log(5),
    "2": 2.0, "3": 3.0, "5": 5.0, "7": 7.0, "8": 8.0, "16": 16.0,
}
coeffs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 0.5, 1/3, 1/4, 1/6, 1/15]
print("\n  [系统搜索] 两参数组合（目标 %.6f）" % alpha_v_exp)
hits = []
for (nx, X), (ny, Y) in itertools.combinations(pool.items(), 2):
    for a in coeffs:
        for b in coeffs:
            v = a*X + b*Y
            d = (v/alpha_v_exp - 1)*100
            if abs(d) < 0.12:
                hits.append((abs(d), d, "%.6f = %g·%s + %g·%s" % (v, a, nx, b, ny)))
hits.sort()
print("  <0.12%% 命中数：%d" % len(hits))
for ad, d, s in hits[:12]:
    print("    [%+.4f%%] %s" % (d, s))

# 单量×整数
print("\n  [单量×整数] n·X（目标 %.6f）" % alpha_v_exp)
hits1 = []
for nx, X in pool.items():
    for n in range(1, 21):
        v = n*X
        d = (v/alpha_v_exp - 1)*100
        if abs(d) < 0.3:
            hits1.append((abs(d), d, "%.6f = %d×%s" % (v, n, nx)))
hits1.sort()
for ad, d, s in hits1[:8]:
    print("    [%+.3f%%] %s" % (d, s))

# 三量（关键模式：A+B/C 或 A−B/C）
print("\n  [三量模式] A±B/C（目标 %.6f）" % alpha_v_exp)
hits3 = []
for (nx, X), (ny, Y) in itertools.combinations(pool.items(), 2):
    for nz, Z in pool.items():
        for a in [1, 2, 3, 4, 5, 6, 7, 8]:
            for b in [1, 2, 3, 4, 5, 6]:
                for c in [1, 2, 3, 4, 5, 6, 7, 8, 10, 16]:
                    for sign in [1, -1]:
                        v = sign*a*X + b*Y/c
                        d = (v/alpha_v_exp - 1)*100
                        if abs(d) < 0.05:
                            hits3.append((abs(d), d, "%.6f = %s%d·%s %d·%s/%d" % (v, "+" if sign>0 else "-", a, nx, b, ny, c)))
hits3.sort()
print("  <0.05%% 命中数：%d" % len(hits3))
for ad, d, s in hits3[:10]:
    print("    [%+.4f%%] %s" % (d, s))

print("\n  [判定]")
print("    已知候选 ln7−Δλ_min/2：%+.4f%%（0.1%% 边缘）" % ((math.log(7)-DL_MIN/2)/alpha_v_exp*100-100))
print("    2−7σ/4：%+.4f%%（2 无身份——待框架化）" % ((2-7*SIGMA/4)/alpha_v_exp*100-100))

result = {"alpha_v_exp": alpha_v_exp, "alpha_v_paper": 1.883,
          "ln7_minus_dl2": math.log(7)-DL_MIN/2, "two_minus_7sig4": 2-7*SIGMA/4}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5j_alpha_v.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
