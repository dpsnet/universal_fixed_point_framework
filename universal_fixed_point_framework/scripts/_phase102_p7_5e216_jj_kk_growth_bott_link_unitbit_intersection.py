# -*- coding: utf-8 -*-
"""
P7-5e-216 JJ: DD2 growth recurrence vs 2^6 power-set step / Bott period 8
        KK: GG-family m vs unit-bit silent family intersection
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e216_jj_kk_growth_bott_link_unitbit_intersection.json"

# ---------- JJ: recurrence vs power-set step ----------
def n_j(j):
    return (2 ** (2 * j + 4) - 1) // 7

# JJ1: j step +3 <=> binary exponent step +6 (2*3); growth factor 2^6=64=b_1^2
JJ1_rows = []
for j in [1, 4, 7]:
    e = 2 * j + 4
    ep = 2 * (j + 3) + 4
    JJ1_rows.append({"j": j, "exp": e, "exp_next": ep, "step": ep - e,
                     "ok_step6": ep - e == 6,
                     "factor_2^6": 2 ** (ep - e), "is_64": 2 ** (ep - e) == 64})

JJ1 = {"check": "★ JJ1: j 步进 3 ⇔ 2 进指数步进 6 = 2·3——n 增长因子 2^6 = 64 = b_1²（满格平方 8²）：'下标步进 3 ↔ 指数步进 6' 的 2 进幂集步进结构",
       "all_ok": all(r["ok_step6"] for r in JJ1_rows), "rows": JJ1_rows}

# JJ2: binary exponents 2j+4 (j≡1 mod 3) all ≡ 0 mod 6; mod-8 cycle 6,4,2,0 period 4
JJ2_exps = [2 * j + 4 for j in [1, 4, 7, 10, 13]]
JJ2 = {"check": "★ JJ2: DD2 族 2 进指数 ≡ 0 mod 6；mod 8 循环 6,4,2,0（指数步进 6 ≡ −2 mod 8，周期 4）",
       "exps": JJ2_exps,
       "mod6_all0": all(e % 6 == 0 for e in JJ2_exps),
       "mod8_seq": [e % 8 for e in JJ2_exps]}

# JJ3: recurrence constants/coefficients all framework quantities
JJ3 = {"check": "★ JJ3: HH 递推系数与常数全框架量——乘数 64=b_1²、加法项 9=静默单元（2^3+1）、减法项 63=b_1²−1 窗口宽度——206 b₁²±1 对的动力学化（递推形式）",
       "64_is_b1sq": 64 == 8 ** 2, "9_is_silent": 9 == 2 ** 3 + 1,
       "63_is_w": 63 == 2 ** 6 - 1 == 8 ** 2 - 1}

# ---------- KK: GG m vs unit-bit silent family ----------
# unit-bit family 2^m+1, m=3..8 (190: {9,17,33,65,129,257})
unit_m = list(range(3, 9))
unit_vals = [2 ** m + 1 for m in unit_m]

# GG family m = n+3k, n=(2^(3k+1)-2)/7
GG_ms = []
for k in range(1, 8):
    n = (2 ** (3 * k + 1) - 2) // 7
    GG_ms.append({"k": k, "m": n + 3 * k})

inter = [r["m"] for r in GG_ms if r["m"] in unit_m]
KK1 = {"check": "★ KK1: GG 族与单位位静默家族交集 = {m=5}（仅 k=1）——m=5 → D(2)=2^5+1=33 单位位成员（190 家族）",
       "unit_m": unit_m, "unit_vals": unit_vals, "gg_ms": [r["m"] for r in GG_ms],
       "intersection": inter, "only_m5": inter == [5]}

KK2 = {"check": "KK2: 下标类与值类脱钩——D(n)=2^m+1 恒 ≡ 1 mod 8（m≥3，2^m≡0 mod 8）不随 m mod 8 类变化（215 II2 m 遍历 8 类）",
       "all_D_mod8_1": all((2 ** m + 1) % 8 == 1 for m in unit_m + [5, 24, 155])}

KK3 = {"check": "★ KK3: 单位位家族 {9,17,33,65,129,257} 含修正锚点 65（m=6，闭式 129 的 1/65 项）与闭式常数 129（m=7）——GG 族 m 序列仅 m=5 命中（33），其余超出",
       "65_in": 65 in unit_vals, "129_in": 129 in unit_vals,
       "m_of_65": unit_m[unit_vals.index(65)] if 65 in unit_vals else None,
       "m_of_129": unit_m[unit_vals.index(129)] if 129 in unit_vals else None}

conclusion = {
    "verdict": "JJ（增长递推联结）：★ j 步进 3 ⇔ 2 进指数步进 6=2·3——n 增长因子 2^6=64=b_1² 满格平方（'下标步进 3 ↔ 指数步进 6'）；★ 2 进指数 2j+4 ≡ 0 mod 6、mod 8 循环 6,4,2,0（周期 4，步进 −2）；★ 递推系数/常数全框架量（64=b₁²、9=静默单元、63=b₁²−1 窗口）——206 b₁²±1 对的动力学化。KK（单位位交集）：★ GG 族与单位位静默家族交集={m=5}（仅 k=1，D(2)=2^5+1=33）；m 下标类与值类脱钩（2^m+1 恒 ≡1 mod 8 不随下标类变）；单位位家族含修正锚点 65（m=6）与闭式常数 129（m=7），GG 族仅 m=5 命中。",
    "JJ": {"JJ1": JJ1, "JJ2": JJ2, "JJ3": JJ3},
    "KK": {"KK1": KK1, "KK2": KK2, "KK3": KK3},
    "honest_limits": [
        "JJ1 是指数算术（2 进指数线性步进）",
        "JJ2 是模 6/模 8 核对（周期 4 观察）",
        "JJ3 是身份核对（系数/常数命中框架量）+ 语义命名'动力学化'",
        "KK1 是枚举交集（{m=5}）",
        "KK2 是模算术核对（值类与下标类脱钩）",
        "KK3 是身份核对（65/129 已在 190 登记）",
        "继承 187-215 候选层",
    ],
    "next_candidates": [
        "检验 LL：'下标步进 3 ↔ 指数步进 6' 与 Bott 周期 8（k_max）的联结——3 与 8 互质，周期最小公倍数 24？2 进指数周期 24 检查",
        "检验 MM：GG 族 m 序列与静默家族 a_j=2^{j+1}+1 下标（j=2..7：m=3..8）之外的第二交集窗口（m≡3k+2 mod 8 中 m<129 的值）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-217",
    ],
}

result = {
    "title": "P7-5e-216 JJ: growth recurrence step link; KK: unit-bit intersection",
    "date": "2026-10-16",
    "JJ": {"rows": JJ1_rows, "JJ1": JJ1, "JJ2": JJ2, "JJ3": JJ3},
    "KK": {"KK1": KK1, "KK2": KK2, "KK3": KK3},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-216 JJ/KK: growth step link & unit-bit intersection")
print("=" * 76)
print("[JJ1 exp step]")
for r in JJ1_rows:
    print("  j=%d exp %d -> %d step=%d ok=%s factor=2^%d" % (r["j"], r["exp"], r["exp_next"], r["step"], r["ok_step6"], r["step"]))
print("[JJ1]", JJ1["check"], "-> all_ok=%s" % JJ1["all_ok"])
print("[JJ2]", JJ2["check"], "-> mod6_all0=%s mod8_seq=%s" % (JJ2["mod6_all0"], JJ2["mod8_seq"]))
print("[JJ3]", JJ3["check"], "-> %s" % (JJ3["64_is_b1sq"] and JJ3["9_is_silent"] and JJ3["63_is_w"]))
print("[KK1 intersection]")
print("  unit_m=%s unit_vals=%s" % (unit_m, unit_vals))
print("  gg_m=%s intersection=%s only_m5=%s" % ([r["m"] for r in GG_ms], inter, KK1["only_m5"]))
print("[KK2]", KK2["check"], "-> all_D_mod8_1=%s" % KK2["all_D_mod8_1"])
print("[KK3]", KK3["check"], "-> 65_in=%s 129_in=%s m65=%s m129=%s" % (KK3["65_in"], KK3["129_in"], KK3["m_of_65"], KK3["m_of_129"]))
print("[Conclusion]", conclusion["verdict"])
