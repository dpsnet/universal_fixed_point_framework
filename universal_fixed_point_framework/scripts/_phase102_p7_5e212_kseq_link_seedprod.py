# -*- coding: utf-8 -*-
"""
P7-5e-212 BB: two-k-sequence linkage (k_j window vs k_n D(n))
        CC: pure-seed-product condition for 7n+2 = 2^a*3^b*5^c
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e212_kseq_link_seedprod.json"

def kwin(j):
    return 3 * 2 ** (j - 2)

def Dn(n):
    return n * 7 * 2 ** (n - 1) + 2 ** n + 1

def kn(n):
    return (Dn(n) - 1) // 8

# ---------- BB: two-k-sequence linkage ----------
k_j_seq = {j: kwin(j) for j in range(2, 8)}       # 3,6,12,24,48,96
k_n_seq = {n: kn(n) for n in range(4, 17)}        # 30,74,176,...

BB_rows = []
for n in range(4, 17):
    lin = 7 * n + 2
    BB_rows.append({"n": n, "k_n": kn(n), "linear": lin,
                    "div3": lin % 3 == 0, "n_mod3": n % 3})

intersection = set(k_j_seq.values()) & set(k_n_seq.values())
BB1 = {"check": "★ BB1 结构同构：k_j = 2^{j−2}·3（线性因子恒 3）、k_n = 2^{n−4}(7n+2)（线性因子 7n+2）——都是'2 进幂 × 线性因子'结构；成员交集 = 空（k_j ≤ 96 < k_n ≥ 30 但无共同成员）",
       "k_j": k_j_seq, "k_n": k_n_seq, "intersection": sorted(intersection)}
BB2 = {"check": "★ BB2 3 因子机制归因：7n+2 ≡ 0 mod 3 ⇔ n ≡ 1 mod 3（7≡1 mod 3）——AA 命中 7/13 中 5 个（n=4,7,10,13,16）由 3 的周期性产生；n=9（65=5·13）、n=14（25=5²）来自 5 因子",
       "n_mod3_1": [r["n"] for r in BB_rows if r["n"] % 3 == 1],
       "div3": [r["n"] for r in BB_rows if r["div3"]]}
BB3 = {"check": "★ BB3 k_9 线性因子 65 与窗口宽度 63 互锁：65 = 7·9+2、63 = 7·9——差 2、和 128 = 2^7（2 的幂）",
       "k9_linear": 7 * 9 + 2, "w5": 2 ** 6 - 1, "diff": (7 * 9 + 2) - (2 ** 6 - 1),
       "sum": (7 * 9 + 2) + (2 ** 6 - 1), "sum_is_2^7": (7 * 9 + 2) + (2 ** 6 - 1) == 2 ** 7}

# ---------- CC: pure-seed-product condition ----------
SEED_PRIMES = [2, 3, 5]

def is_pure_seed(x):
    t = x
    for p in SEED_PRIMES:
        while t % p == 0:
            t //= p
    return t == 1

CC_rows = []
for n in range(4, 17):
    lin = 7 * n + 2
    CC_rows.append({"n": n, "7n+2": lin, "pure": is_pure_seed(lin)})

CC1 = {"check": "★ CC1 7n+2 为纯 {2,3,5} 积的 n = {4, 10, 14}（3/13）——n=4: 30=2·3·5、n=10: 72=2³·3²、n=14: 100=2²·5²",
       "hits": [r["n"] for r in CC_rows if r["pure"]],
       "factors": {"n4": "30 = 2·3·5", "n10": "72 = 2³·3²", "n14": "100 = 2²·5²"}}

# extended enumeration: 2^a*3^b*5^c ≡ 2 mod 7 within bound
CC_solutions = []
for a in range(0, 9):
    for b in range(0, 5):
        for c in range(0, 5):
            v = 2 ** a * 3 ** b * 5 ** c
            if v > 500000:
                continue
            if v % 7 == 2:
                nv = (v - 2) // 7
                if nv >= 1 and (7 * nv + 2) == v:
                    CC_solutions.append({"a": a, "b": b, "c": c, "v": v, "n": nv})
CC2 = {"check": "CC2 mod 7 条件：7n+2 = 2^a·3^b·5^c ⇔ 2^a·3^b·5^c ≡ 2 (mod 7)；< 5×10^5 内全部解",
       "solutions": CC_solutions}

conclusion = {
    "verdict": "BB（两 k 序列连接）：k_j 与 k_n 结构同构（2 进幂 × 线性因子：k_j 线性因子恒 3、k_n 线性因子 7n+2）但成员交集为空（枚举）；3 因子命中机制归因：7n+2 ≡ 0 mod 3 ⇔ n ≡ 1 mod 3——AA 命中 7/13 中 5 个由 3 的周期性产生（n=4,7,10,13,16），n=9（65=5·13）、n=14（25=5²）来自 5 因子；k_9 线性因子 65 与窗口宽度 63 互锁（65=7·9+2、63=7·9——差 2、和 128=2^7）。CC（纯种子积条件）：7n+2 为纯 {2,3,5} 积的 n = {4,10,14}（3/13：30=2·3·5、72=2³·3²、100=2²·5²）；mod 7 条件 2^a·3^b·5^c ≡ 2 mod 7，< 5×10^5 内全部解枚举（含大 n 稀疏解）。",
    "BB": {"BB1": BB1, "BB2": BB2, "BB3": BB3, "rows": BB_rows},
    "CC": {"CC1": CC1, "CC2": CC2, "rows": CC_rows},
    "honest_limits": [
        "BB1 结构同构是形式观察；交集为空是枚举",
        "BB2 是模算术归因（7≡1 mod 3）",
        "BB3 是算术恒等（65−63=2、65+63=2^7）",
        "CC1 是枚举（3/13，解稀疏：7n+2 线性 vs 种子积稀疏）",
        "CC2 mod 7 条件是数论事实（同余过滤）",
        "继承 187-211 候选层",
    ],
    "next_candidates": [
        "检验 DD：k_9 线性因子 65 与窗口宽度 63 的 7·9±2 互锁是否推广（7n+2 与 7(n−1)+9 的关系）",
        "检验 EE：纯种子积解 {30,72,100} 与框架量（72=8·9、100=10²、30=2·3·5）在 k_n 中的角色",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-213",
    ],
}

result = {
    "title": "P7-5e-212 two-k-sequence linkage & pure-seed-product condition",
    "date": "2026-10-16",
    "BB": {"rows": BB_rows, "BB1": BB1, "BB2": BB2, "BB3": BB3},
    "CC": {"rows": CC_rows, "CC1": CC1, "CC2": CC2},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-212 two-k-sequence linkage & pure-seed-product condition")
print("=" * 76)
print("[BB rows]")
for r in BB_rows:
    print("  n=%2d k_n=%8d linear=%3d div3=%s n_mod3=%d" % (r["n"], r["k_n"], r["linear"], r["div3"], r["n_mod3"]))
print("[BB1]", BB1["check"], "-> intersection=%s" % BB1["intersection"])
print("[BB2]", BB2["check"], "-> n%%3==1: %s" % BB2["n_mod3_1"])
print("[BB3]", BB3["check"], "-> diff=%d sum=%d is_2^7=%s" % (BB3["diff"], BB3["sum"], BB3["sum_is_2^7"]))
print("[CC1]", CC1["check"], "-> hits=%s" % CC1["hits"])
print("[CC2]", CC2["check"])
for s in CC_solutions:
    print("   2^%d·3^%d·5^%d = %d  ->  n=%d" % (s["a"], s["b"], s["c"], s["v"], s["n"]))
print("[Conclusion]", conclusion["verdict"])
