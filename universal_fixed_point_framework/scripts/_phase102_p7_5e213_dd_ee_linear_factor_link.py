# -*- coding: utf-8 -*-
"""
P7-5e-213 DD: 7n+2 vs b_j^2±1 interlock generalization
        EE: pure-seed-product solutions {30,72,100} in k_n
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e213_dd_ee_linear_factor_link.json"

def Dn(n):
    return n * 7 * 2 ** (n - 1) + 2 ** n + 1

def kn(n):
    return (Dn(n) - 1) // 8

def bj(j):
    return 2 ** (j + 2)

def odd_part(x):
    while x % 2 == 0:
        x //= 2
    return x

# ---------- DD ----------
# DD1: 212 BB3 = 206 b_1^2±1 pair reappearance (65=8²+1, 63=8²-1)
DD1 = {"check": "DD1: 212 BB3 的 65/63 互锁 = 206 b₁²±1 对的再现——65=8²+1、63=8²−1（b₁=8），差 2、和 2b₁²=128=2^7；65=7·9+2 是 8²+1 的展开（9=8+1）",
       "ok": (8 ** 2 + 1) == 7 * 9 + 2 == 65 and (8 ** 2 - 1) == 63 == 2 ** 6 - 1}

# DD2: 7n+2 = b_j^2+1 solutions (j ≡ 1 mod 3)
DD2_rows = []
for j in range(0, 10):
    if j % 3 != 1:
        continue
    v = bj(j) ** 2 + 1
    if (v - 2) % 7 == 0:
        n = (v - 2) // 7
        DD2_rows.append({"j": j, "b_j^2+1": v, "n": n,
                         "ok": 7 * n + 2 == v})
DD2 = {"check": "★ DD2: 7n+2 = b_j²+1 的解 j ≡ 1 mod 3——n = (2^{2j+4}−1)/7（j=1: n=9、j=4: n=585、j=7: n=37449…）；k_n 线性因子命中满格平方+1（k_9=2^5·65 已见、k_585 线性因子 4097=F_2·D(4)）",
       "rows": DD2_rows}

# DD3: CC3 family parity -> linear factor square
DD3_rows = []
for k in range(1, 6):
    a = 3 * k + 1
    v = 2 ** a
    if (v - 2) % 7 != 0:
        continue
    n = (v - 2) // 7
    # is 2^a a perfect square? a even and 2^{a/2} integer
    is_sq = (a % 2 == 0)
    j = (a - 4) // 2 if is_sq else None
    DD3_rows.append({"k": k, "a": a, "2^a": v, "n": n,
                     "is_square": is_sq, "b_j": ("b_%d²=2^%d" % (j, a)) if is_sq else "2^%d" % a,
                     "k_odd": k % 2 == 1})
DD3 = {"check": "★ DD3: CC3 族 7n+2=2^{3k+1} 中 k 奇 ⇒ 线性因子是满格平方 b_j²（j=3(k−1)/2：k=1 → b_0²=16、k=3 → b_3²=1024、k=5 → b_6²=65536…）；k 偶 ⇒ 非平方 2 幂（n=18: 2^7、n=1170: 2^13）",
       "rows": DD3_rows}

# ---------- EE ----------
SEED_PRIMES = [2, 3, 5]
def is_pure_seed(x):
    t = x
    for p in SEED_PRIMES:
        while t % p == 0:
            t //= p
    return t == 1

EE_rows = []
for n in [4, 10, 14]:
    lin = 7 * n + 2
    k = kn(n)
    o = odd_part(k)
    EE_rows.append({"n": n, "7n+2": lin, "k_n": k, "odd_part": o,
                    "lin_pure": is_pure_seed(lin), "odd_pure": is_pure_seed(o)})

EE1 = {"check": "★ EE1: 线性因子纯种子积（n=4,10,14）⇒ k_n 奇部纯种子积——k_4 奇部 15=3·5、k_10 奇部 9=3²、k_14 奇部 25=5²（k_n=2^{n−4}·线性因子，奇部=线性因子奇部）",
       "rows": EE_rows}
EE2 = {"check": "EE2: 纯积解 {30,72,100}——72=8·9 唯一'满格×静默单元'框架组合；30=2·3·5 纯种子积；100=(8+2)² 种子扩展平方",
       "30": "2·3·5", "72": "8·9 = 2³·3²", "100": "(8+2)² = 2²·5²"}
EE3 = {"check": "EE3: 纯积解的 n 分布 {4,10,14} 间隔 6,4——无等差规律（枚举）"}

conclusion = {
    "verdict": "DD（互锁推广）：212 BB3 的 65/63 互锁 = 206 b₁²±1 对再现（65=8²+1、63=8²−1、差 2、和 2b₁²=2^7）——非新结构；★ 7n+2 = b_j²+1 的解 j ≡ 1 mod 3（n=9, 585, 37449…，k_n 线性因子命中满格平方+1）；★ CC3 族 k 奇 ⇒ 线性因子 = b_j² 满格平方（k=1: b_0²=16、k=3: b_3²=1024、k=5: b_6²=65536）、k 偶 ⇒ 非平方 2 幂（2^7、2^13）——CC3 的 n=146 线性因子 1024 获得 b_3² 满格平方身份。EE（纯积角色）：线性因子纯种子积 ⇒ k_n 奇部纯种子积（3/13：15/9/25）；纯积解中 72=8·9 唯一框架组合、30 纯种子积、100=(8+2)²；n 分布无规律。",
    "DD": {"DD1": DD1, "DD2": DD2, "DD3": DD3},
    "EE": {"EE1": EE1, "EE2": EE2, "EE3": EE3},
    "honest_limits": [
        "DD1 是 206 恒等再现（重命名事实）",
        "DD2 是代数求解（同余条件 j≡1 mod 3）",
        "DD3 是奇偶判别（2^{3k+1} 平方 ⇔ a 偶 ⇔ k 奇）+ 满格平方身份",
        "EE1 是 CC1 直接推论（k_n=2^{n−4}·线性因子）",
        "EE2 是核对（72=8·9 已知）",
        "EE3 是枚举",
        "继承 187-212 候选层",
    ],
    "next_candidates": [
        "检验 FF：DD2 族 n=9,585,37449 的 k_n 2 进展开（k_585 含 F_2·D(4)=4097 的角色）",
        "检验 GG：CC3 族 k 奇的 D(n) 静默家族下标（n=146: m=n+3k=155 与 2^m 家族的关系）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-214",
    ],
}

result = {
    "title": "P7-5e-213 DD: 7n+2 vs b_j^2±1 interlock; EE: pure-seed solutions in k_n",
    "date": "2026-10-16",
    "DD": {"DD1": DD1, "DD2": {"rows": DD2_rows}, "DD3": {"rows": DD3_rows}},
    "EE": {"rows": EE_rows, "EE1": EE1, "EE2": EE2, "EE3": EE3},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-213 DD/EE: linear factor interlock & pure-seed roles")
print("=" * 76)
print("[DD1]", DD1["check"], "-> ok=%s" % DD1["ok"])
print("[DD2 7n+2 = b_j^2+1]")
for r in DD2_rows:
    print("  j=%d b_j²+1=%7d n=%5d ok=%s" % (r["j"], r["b_j^2+1"], r["n"], r["ok"]))
print("[DD3 CC3 parity]")
for r in DD3_rows:
    print("  k=%d 2^%d=%7d n=%5d square=%s %s" % (r["k"], r["a"], r["2^a"], r["n"], r["is_square"], r["b_j"]))
print("[EE1 pure-seed => odd pure-seed]")
for r in EE_rows:
    print("  n=%2d 7n+2=%3d k=%8d odd=%3d lin_pure=%s odd_pure=%s" % (
        r["n"], r["7n+2"], r["k_n"], r["odd_part"], r["lin_pure"], r["odd_pure"]))
print("[EE2]", EE2["check"])
print("[EE3]", EE3["check"])
print("[Conclusion]", conclusion["verdict"])
