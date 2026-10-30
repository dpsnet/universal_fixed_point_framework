# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-41：m_τ/m_b 主结构比 3/7 + 静默单元家族第 4 实例搜索
================================================================
洞察：m_τ 主结构 192 = k_max²·N_gen、m_b 主结构 448 = k_max²·(k_max−1)——比值 = 3/7（k_max² 消去）
搜索：框架恒等式中的 X+1 / ×7 静默单元结构（家族第 4 实例）
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
alpha0 = 1/2
alpha0_3 = alpha0**3
N_total = kmax - Ngen

print("="*104)
print("P7-5e-41：m_τ/m_b 主结构比 3/7 + 家族第 4 实例搜索")
print("="*104)

print()
print("【m_τ/m_b 主结构比】")
print("-"*104)
main_tau = kmax**2*Ngen      # 192
main_b   = kmax**2*(kmax-1)  # 448
print("m_τ 主结构 = k_max²·N_gen = %d×%d = %d" % (kmax**2, Ngen, main_tau))
print("m_b 主结构 = k_max²·(k_max−1) = %d×%d = %d" % (kmax**2, kmax-1, main_b))
print("比值 = %d/%d = %.6f = N_gen/(k_max−1) = 3/7——k_max² 消去 ✓" % (main_tau, main_b, main_tau/main_b))
print()
m_t = (1-dlam_P20/16)*3**4*5**(1/3)*(193-3/40)/math.sqrt(2)
m_b = C2*(2**6*(kmax-1)+Ngen*alpha_t)
m_tau = C2*(193-3/40)
print("m_t/m_b 分解：= (1−Δλ_P20/16)·(3⁴·∛5/√2)·(m_τ/m_b)")
print("  m_τ/m_b = %.6f——骨架 = 3/7 = %.6f（差 %+.2f%%——修正扰动）" % (m_tau/m_b, 3/7, (m_tau/m_b)/(3/7)*100-100))
print("  m_t/m_b = %.6f vs 41.3165（%+.6f%%）" % (m_t/m_b, (m_t/m_b/41.3165-1)*100))
print("  ★ 主结构比 3/7 = N_gen/(k_max−1) 是 m_τ/m_b 骨架——k_max² 消去——纯代结构比")
print()
print("【静默单元家族第 4 实例搜索】")
print("-"*104)
# 框架量全集
F = {
    "k_max": kmax, "N_gen": Ngen, "k_max-1": kmax-1, "k_max-N_gen": N_total, "N_gen!": 6,
    "k_max·N_gen": kmax*Ngen, "k_max²": kmax**2, "k_max²·N_gen": kmax**2*Ngen,
    "k_max²·(k_max-1)": kmax**2*(kmax-1), "C²": C2, "1/α_EM": 24*(dH+3), "Λ": Lam, "κΛ": kL,
    "d_H": dH, "ln10": math.log(10), "ln7": alpha_t, "σ": sigma, "α_v": alpha_v,
    "Δλ_EM": dlam_EM, "Δλ_P20": dlam_P20, "π": math.pi, "e": math.e, "√2": math.sqrt(2), "√3": math.sqrt(3),
    "∛5": 5**(1/3), "3⁴·∛5": 81*5**(1/3), "41": 41, "49": 49, "193": 193, "40": 40, "48": 48, "192": 192,
}
print("X+1 结构（X 为框架组合）：")
hits_add = []
for name, v in F.items():
    if abs(v+1 - round(v+1)) < 1e-9 and v > 5:
        # 检查 v+1 是否接近某个整数（可能已有身份）
        hits_add.append((name, v, int(round(v+1))))
for name, v, n in hits_add:
    print("  %-22s = %d → %d+1 = %d" % (name, int(v), int(v), n))
print()
print("×7 结构（k_max−1 乘法静默）：")
hits_mul = []
for name, v in F.items():
    if v > 0 and abs(v/7 - round(v/7)) < 1e-9 and v != 7 and v != 49 and v != 448:
        hits_mul.append((name, v, int(round(v/7))))
for name, v, n in hits_mul:
    print("  %-22s = %d = 7×%d" % (name, int(v), n))
print("  （已有：7 本身、49 = 7²、448 = 64×7 = k_max²×7）")
print()
print("【家族第 4 实例候选评估】")
print("-"*104)
print("新 X+1 命中：")
for name, v, n in hits_add:
    print("  %s+1 = %d——身份？%s" % (name, n, "已有身份" if n in (41,49,193) else "新候选"))
print()
print("新 ×7 命中：")
for name, v, n in hits_mul:
    print("  %s = 7×%d——身份？%s" % (name, n, "已有身份" if v in (7,49,448) else "新候选"))
print()
print("【结论】")
print("-"*104)
print("1. ★ m_τ/m_b 主结构比 = 3/7 = N_gen/(k_max−1)——k_max² 消去——纯代结构比（修正扰动 0.8%）")
print("2. m_t/m_b 分解 = (1−Δλ_P20/16)·(3⁴·∛5/√2)·(m_τ/m_b)——主结构骨架 3/7 在比值层重现")
print("3. 家族第 4 实例：搜索命中登记（如有干净候选）")
print("4. 诚实边界：m_τ/m_b 数值非精确 3/7（修正扰动）——骨架是结构性观察非数值恒等")
print()
json.dump({"main_ratio": {"m_tau_main": main_tau, "m_b_main": main_b, "ratio": "3/7=Ngen/(kmax-1)"},
           "m_t_mb_decomp": m_t/m_b,
           "family4_add": [(n, v, int(round(v+1))) for n,v,x in hits_add],
           "family4_mul": [(n, v, int(round(v/7))) for n,v,x in hits_mul]},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e41_main_ratio37.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
