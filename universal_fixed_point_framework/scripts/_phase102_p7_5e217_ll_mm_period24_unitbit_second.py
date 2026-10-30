# -*- coding: utf-8 -*-
"""
P7-5e-217 LL: step-3 vs Bott period 8 -> lcm(3,8)=24 full cycle
        MM: GG m in m<129 window vs silent family second intersection
"""
import json
import math

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e217_ll_mm_period24_unitbit_second.json"

def n_j(j):
    return (2 ** (2 * j + 4) - 1) // 7

def n_gg(k):
    return (2 ** (3 * k + 1) - 2) // 7

# ---------- LL: step 3 vs Bott period 8 ----------
LL1 = {"check": "★ LL1: 3 与 8 互质——j 步进 3（DD2 族下标步进）在 8 步内遍历全部 mod 8 类；完整周期 lcm(3,8)=24；指数步进 6 与 8 的 lcm(6,8)=24 同样",
       "gcd38": math.gcd(3, 8), "lcm38": 3 * 8 // math.gcd(3, 8),
       "lcm68": 6 * 8 // math.gcd(6, 8),
       "j_mod8_traversal": sorted({j % 8 for j in [1, 4, 7, 10, 13, 16, 19, 22]}),
       "all8classes": len({j % 8 for j in [1, 4, 7, 10, 13, 16, 19, 22]}) == 8}

LL2_rows = []
for j in [1, 4, 7, 10, 13]:
    e = 2 * j + 4
    n = n_j(j)
    LL2_rows.append({"j": j, "exp": e, "exp_mod8": e % 8, "n": n, "n_mod8": n % 8,
                     "n_silent": n % 8 == 1})
LL2 = {"check": "★ LL2: 指数 mod 8 遍历 4 类（6,4,2,0）但 n 恒 ≡ 1 mod 8——7n = 2^e−1 ≡ 7 mod 8（2^e ≡ 0 mod 8，e≥3），n 静默类与指数类无关",
       "rows": LL2_rows, "all_n_silent": all(r["n_silent"] for r in LL2_rows),
       "exp_classes": sorted({r["exp_mod8"] for r in LL2_rows})}

LL3 = {"check": "LL3: 两族步进对比——Bott 步进 8（窗口对合 k_{2j+3}=6·4^j 每步 ×4）vs DD2 步进 3（指数每步 ×2^6=64）——lcm(8,3)=24 为共同完整周期",
       "bott_step": 8, "dd2_step": 3, "lcm": 24,
       "note": "24 = 8·3 = 满格 × 下标步进（Bott 周期 8 的 3 倍）"}

# ---------- MM: GG m vs silent family second intersection ----------
unit_m = list(range(3, 9))            # 190 unit-bit m=3..8
unit_vals = [2 ** m + 1 for m in unit_m]

gg_ms_small = []
for k in range(1, 20):
    m = n_gg(k) + 3 * k
    if m < 129:
        gg_ms_small.append({"k": k, "m": m})
    else:
        break

inter = [r["m"] for r in gg_ms_small if r["m"] in unit_m]
MM1 = {"check": "★ MM1: m<129 窗口内 GG 族 = {5, 24}——与单位位家族交集仍 {5}（无第二交集；2^24+1 巨大非单位位）",
       "gg_small": [r["m"] for r in gg_ms_small], "intersection": inter,
       "no_second": inter == [5]}
MM2 = {"check": "MM2: GG 族 m 从 5 起步，跳过单位位 m=6,7,8（24 之后直接 155）——单位位家族是静默家族 2^m+1 的 m≤8 段",
       "gg_first": 5, "unit_tail": [6, 7, 8], "skip": "GG m=24 跳过 6,7,8",
       "ok": 24 > 8}
MM3 = {"check": "MM3: GG 族是静默家族 2^m+1 的 m≥5 稀疏子列（5,24,155,1182,9377,…——m 增长 ~2^{3k}/7），单位位段（m=3..8）仅 m=5 共享",
       "sparse": True}

conclusion = {
    "verdict": "LL（周期联结）：★ 3 与 8 互质——DD2 族下标步进 3 在 8 步内遍历全部 mod 8 类（1,4,7,2,5,0,3,6）；完整周期 lcm(3,8)=24=lcm(6,8)（下标步进 3 与指数步进 6 均与 Bott 周期 8 的 lcm 为 24）；★ 指数 mod 8 遍历 4 类但 n 恒 ≡ 1 mod 8（7n≡7 mod 8 与指数类无关，e≥3 时 2^e≡0）；Bott 步进 8 与 DD2 步进 3 的 lcm=24（=8·3）。MM（第二交集）：★ m<129 窗口内 GG 族 {5,24} 与单位位交集仍 {5}（无第二交集）；GG 族 m 从 5 起步跳过单位位 m=6,7,8（24 之后直接 155）；单位位家族是静默家族 m≤8 段，GG 族是 m≥5 稀疏子列。",
    "LL": {"LL1": LL1, "LL2": LL2, "LL3": LL3},
    "MM": {"MM1": MM1, "MM2": MM2, "MM3": MM3},
    "honest_limits": [
        "LL1 是数论恒等（互质/lcm）",
        "LL2 是模算术（2^e≡0 mod 8 for e≥3）",
        "LL3 是步进对比观察（8 vs 3）",
        "MM1/MM2/MM3 是枚举与窗口观察（无第二交集 = 负结果）",
        "继承 187-216 候选层",
    ],
    "next_candidates": [
        "检验 NN：Bott 步进 8 与 DD2 步进 3 是否在窗口对合 k_{2j+3} 与 k_n 之间呈现 8/3 互换（两 k 序列的步进比）",
        "检验 OO：GG 族 m 序列（5,24,155,1182,…）与 2^m 家族（m 全 ≡ 5·3^{k-1} mod ?）的增长律闭式（m_k ≈ 2^{3k}/7 精确式）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-218",
    ],
}

result = {
    "title": "P7-5e-217 LL: lcm(3,8)=24 cycle; MM: no second unit-bit intersection",
    "date": "2026-10-16",
    "LL": {"LL1": LL1, "LL2": {"rows": LL2_rows}, "LL3": LL3},
    "MM": {"MM1": MM1, "MM2": MM2, "MM3": MM3},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-217 LL/MM: period-24 link & second intersection")
print("=" * 76)
print("[LL1]", LL1["check"])
print("  gcd(3,8)=%d lcm(3,8)=%d lcm(6,8)=%d j_mod8_traversal=%s all8=%s" % (
    LL1["gcd38"], LL1["lcm38"], LL1["lcm68"], LL1["j_mod8_traversal"], LL1["all8classes"]))
print("[LL2]")
for r in LL2_rows:
    print("  j=%d exp=%d exp%%8=%d n=%d n%%8=%d silent=%s" % (r["j"], r["exp"], r["exp_mod8"], r["n"], r["n_mod8"], r["n_silent"]))
print("[LL2]", LL2["check"], "-> all_n_silent=%s exp_classes=%s" % (LL2["all_n_silent"], LL2["exp_classes"]))
print("[LL3]", LL3["check"], "-> %s" % LL3["note"])
print("[MM1]", MM1["check"], "-> gg_small=%s intersection=%s no_second=%s" % (
    MM1["gg_small"], MM1["intersection"], MM1["no_second"]))
print("[MM2]", MM2["check"], "-> ok=%s" % MM2["ok"])
print("[MM3]", MM3["check"])
print("[Conclusion]", conclusion["verdict"])
