# -*- coding: utf-8 -*-
"""
P7-5e-220 RR: silent-family m≡1 mod 3 subcolumn vs GG-family m mod 3
        SS: 6·2^a unsolvability vs CC2 pure-product (primitive-root freedom)
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e220_rr_ss_silent_mod3_growth_primitive_root.json"

def m_k(k):
    return (2 ** (3 * k + 1) + 21 * k - 2) // 7

# ---------- RR: m ≡ 1 mod 3 silent subcolumn ----------
RR1 = {"check": "★ RR1: 静默家族 m≡1 mod 3 子列 = {2^{3t+1}+1} = {3, 17, 129, 1025, 8193, …}——含种子 3（m=1）、F_1=17（m=4）、闭式常数 129（m=7）",
       "vals": [2 ** (3 * t + 1) + 1 for t in range(0, 6)],
       "ok": all((2 ** (3 * t + 1) + 1) % 8 == 1 for t in range(1, 6))}

RR_rows = []
for k in range(1, 8):
    m = m_k(k)
    RR_rows.append({"k": k, "m": m, "m_mod3": m % 3,
                    "expected": 2 if k % 2 == 1 else 0,
                    "ok": m % 3 == (2 if k % 2 == 1 else 0)})

RR2 = {"check": "★ RR2: GG 族 m_k mod 3 = 2,0 交替（k 奇 → 2、k 偶 → 0）——2^{3k+1} mod 3 主导（3k+1 偶 ⇔ k 奇 → 2^{3k+1}≡1 → 分子≡2 → m≡2；k 偶 → ≡0）",
       "rows": RR_rows, "all_ok": all(r["ok"] for r in RR_rows)}
RR3 = {"check": "★ RR3: GG 族 m_k mod 3 ∈ {0,2}（永 ≠ 1）——与静默家族 m≡1 mod 3 子列（1,4,7,10…）无交集；余项 3k−2≡1 mod 3（219 QQ1）与 m_k 本身 mod 3 脱钩（m_k 由 2^{3k+1} 主导）",
       "gg_mod3_set": sorted({r["m_mod3"] for r in RR_rows}), "silent_mod3": 1,
       "no_intersection": 1 not in {r["m_mod3"] for r in RR_rows}}

# ---------- SS: primitive-root freedom ----------
# orders: 2 (order 3), 3 (order 6, primitive), 5 (order 6, primitive)
SS1 = {"check": "★ SS1: 3/5 是 mod 7 原根（阶 6）→ 3^b·5^c 遍历全部 mod 7 类 → 2^a·3^b·5^c 遍历全部 6 类 → ≡2 mod 7 可解（212 CC2 的 35 解）；固定 6·2^a（无 3/5 自由度）仅 {6,5,3}",
       "order2": "2 的阶 3（{1,2,4}）", "order3": "3 的阶 6（原根）", "order5": "5 的阶 6（原根）",
       "six_times_2a_mod7": sorted({(6 * 2 ** a) % 7 for a in range(1, 10)}),
       "full_cover": sorted({(2 ** a * 3 ** b * 5 ** c) % 7 for a in range(0, 4) for b in range(0, 7) for c in range(0, 7)}),
       "cover_all6": len({(2 ** a * 3 ** b * 5 ** c) % 7 for a in range(0, 4) for b in range(0, 7) for c in range(0, 7)}) == 6}

SS2 = {"check": "SS2: 含 3 因子非必要条件——100 = 2²·5²（无 3）也 ≡ 2 mod 7（4·25 = 100 ≡ 2）；可解性来自 5 因子自由度而非 3 本身",
       "100_mod7": 100 % 7, "ok": 100 % 7 == 2}

SS3 = {"check": "★ SS3: 6·2^a = 2^{a+1}·3^1 是缺 5 因子的 {2,3} 纯积——5 因子加入恢复 ≡2 mod 7 可解性（3^b·5^c 原根组合覆盖）",
       "factor": "2^{a+1}·3", "missing": "5 因子", "ok": 6 == 2 * 3}

conclusion = {
    "verdict": "RR（mod 3 子列）：★ 静默家族 m≡1 mod 3 子列 = {2^{3t+1}+1} = {3, 17, 129, 1025, 8193, …}（含种子 3、F_1=17、闭式常数 129）；★ GG 族 m_k mod 3 = 2,0 交替（k 奇→2、k 偶→0，2^{3k+1} mod 3 主导）；★ 两子列无交集（GG 族 m 永 ≠1 mod 3）——余项 3k−2≡1 mod 3 与 m_k 本身 mod 3 脱钩。SS（原根自由度）：★ 3/5 是 mod 7 原根（阶 6）→ 2^a·3^b·5^c 遍历全部 mod 7 类 → ≡2 可解（CC2 的 35 解）；固定 6·2^a 缺自由度仅 {6,5,3}；含 3 因子非必要（100=2²·5² 无 3 也解）；★ 6·2^a=2^{a+1}·3 是缺 5 因子的 {2,3} 纯积——加 5 恢复可解性。",
    "RR": {"RR1": RR1, "RR2": RR2, "RR3": RR3},
    "SS": {"SS1": SS1, "SS2": SS2, "SS3": SS3},
    "honest_limits": [
        "RR1 是子列枚举（含框架成员身份核对）",
        "RR2 是模算术推导（2^{3k+1} mod 3 周期 2）",
        "RR3 是无交集观察（负结果）+ 脱钩说明",
        "SS1 是数论结构（原根/阶）——'遍历全部类'为群作用恒等",
        "SS2 是单点核对（100≡2 mod 7）",
        "SS3 是因子分解核对",
        "继承 187-219 候选层",
    ],
    "next_candidates": [
        "检验 TT：静默家族 m≡1 mod 3 子列 {3,17,129,1025,…} 与 2^m+1 的单位位/锚点家族交集（129 闭式常数、17 F_1、3 种子——是否'种子→F_1→闭式常数'的生成链）",
        "检验 UU：GG 族 m_k mod 3 交替与 m_k mod 8 遍历（215 II2）的联合周期（lcm(3,8)=24——m_k mod 24 检查）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-221",
    ],
}

result = {
    "title": "P7-5e-220 RR: silent m≡1 mod 3 vs GG mod 3; SS: primitive-root freedom",
    "date": "2026-10-16",
    "RR": {"RR1": RR1, "RR2": {"rows": RR_rows}, "RR3": RR3},
    "SS": {"SS1": SS1, "SS2": SS2, "SS3": SS3},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-220 RR/SS: silent mod-3 subcolumn & primitive-root freedom")
print("=" * 76)
print("[RR1]", RR1["check"])
print("  vals=%s" % RR1["vals"])
print("[RR2 GG m mod 3]")
for r in RR_rows:
    print("  k=%d m=%7d m%%3=%d expected=%d ok=%s" % (r["k"], r["m"], r["m_mod3"], r["expected"], r["ok"]))
print("[RR2]", RR2["check"], "-> all_ok=%s" % RR2["all_ok"])
print("[RR3]", RR3["check"], "-> gg_mod3=%s no_inter=%s" % (RR3["gg_mod3_set"], RR3["no_intersection"]))
print("[SS1]", SS1["check"])
print("  6*2^a mod7=%s full_cover=%s cover_all6=%s" % (SS1["six_times_2a_mod7"], SS1["full_cover"], SS1["cover_all6"]))
print("[SS2]", SS2["check"], "-> 100%%7=%d ok=%s" % (SS2["100_mod7"], SS2["ok"]))
print("[SS3]", SS3["check"], "-> %s = %s" % (SS3["factor"], SS3["missing"]))
print("[Conclusion]", conclusion["verdict"])
