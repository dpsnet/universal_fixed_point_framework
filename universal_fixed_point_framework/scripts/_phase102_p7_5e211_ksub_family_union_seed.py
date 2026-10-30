# -*- coding: utf-8 -*-
"""
P7-5e-211 YY: k-family union discrimination (k_{2j+3}=6*4^j vs k_j=3*2^{j-2})
        AA: k_n = 2^{n-4}(7n+2) vs seed algebra {2,3,5,8}
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e211_ksub_family_union_seed.json"

def kwin(w):
    """window involution constant k_j = 3*2^{j-2} (j>=2)"""
    return 3 * 2 ** (w - 2)

# ---------- YY: same-family discrimination ----------
YY_rows = []
for jp in range(1, 7):
    w = 2 * jp + 3
    YY_rows.append({"jp": jp, "window": w,
                    "k_{2j+3}=6*4^jp": 6 * 4 ** jp,
                    "k_j formula at w": kwin(w),
                    "same": 6 * 4 ** jp == kwin(w)})

YY = {
    "check": "★ YY 同族判别：k_{2j+3} = 6·4^j = 3·2^{2j+1} = 3·2^{(2j+3)−2} = k_j 公式在窗口下标 w=2j+3 的取值——'两族'是同一公式 k_j=3·2^{j−2} 的重命名；'并集' = 原族在奇窗口下标的值；重合窗口 {5,7} 在定义域内（j≤7）、{9,11,13,15} 是公式自然延伸",
    "overlap_in_domain": [w for r in YY_rows for w in [r["window"]] if r["same"] and r["window"] <= 7],
    "extended": [r["window"] for r in YY_rows if r["window"] > 7],
    "rows": YY_rows,
}

# ---------- AA: seed algebra intersection ----------
def Dn(n):
    return n * 7 * 2 ** (n - 1) + 2 ** n + 1

def kn(n):
    return (Dn(n) - 1) // 8

SEEDS = [2, 3, 5, 8]

def odd_part(x):
    while x % 2 == 0:
        x //= 2
    return x

def has_seed_factor(x):
    o = odd_part(x)
    for s in SEEDS:
        if o % s == 0:
            return True, s
    return False, None

AA_rows = []
for n in range(4, 17):
    k = kn(n)
    o = odd_part(k)
    hit, s = has_seed_factor(k)
    AA_rows.append({"n": n, "k_n": k, "odd": o, "seed_hit": hit, "seed": s,
                    "factor": "2^%d × %d" % (k.bit_length() - o.bit_length(), o)})

AA = {
    "check": "AA：k_n = 2^{n−4}(7n+2) 与种子代数 {2,3,5,8} 交集——★ k_4 = 30 = 2·3·5（纯种子积，三种子直接生成）；种子因子命中 7/13（n=4,7,9,10,13,14,16）但判据宽（奇部含任一种子因子）；核心命中与 210 一致（65/9/93/25/57）；k_9 = 2^5·65 = 2^5·5·(8+5)（65=5·(8+5) 的 195 身份再现于 k_n）",
    "rows": AA_rows,
    "hits": [r["n"] for r in AA_rows if r["seed_hit"]],
    "pure_seed_prod": {"k_4": kn(4), "factor": "2·3·5"},
    "core_hits_aligned_210": [9, 10, 13, 14, 16],
}

conclusion = {
    "verdict": "YY（★ 同族判别）：k_{2j+3} = 6·4^j 不是新族——6·4^j = 3·2^{2j+1} = k_j 公式在窗口下标 2j+3 的取值（j'=1..6 → 窗口 5,7,9,11,13,15），与 k_j=3·2^{j−2} 是同一公式；'并集' = 原族在奇窗口的值（24/96 重合于窗口 5,7 定义域内，384/1536/6144/24576 是公式自然延伸）——208 VV3 的'后移窗口对合常数族'应登记为原族的下标延伸而非独立族。AA（种子交集）：k_4 = 30 = 2·3·5 纯种子积（n=4 单点）；种子因子命中 7/13（n=4,7,9,10,13,14,16）但判据宽（含任一种子因子即命中，3 为常见因子）——核心命中 65/9/93/25/57 与 210 一致；k_9 = 2^5·65 = 2^5·5·(8+5) 再现 195 身份。",
    "YY": YY,
    "AA": AA,
    "honest_limits": [
        "YY 是代数恒等（6·4^j = 3·2^{2j+1} 展开）——'同族'是重命名事实",
        "AA 的 k_4=2·3·5 是单点命中",
        "AA 判据宽（奇部含任一种子因子）：7/13 有通胀，3 是常见因子",
        "核心命中 65/9/93/25/57 与 210 重复（非新证据）",
        "k_9=2^5·65 的 65=5·(8+5) 是 195 已知身份再现",
        "继承 187-210 候选层",
    ],
    "next_candidates": [
        "检验 BB：窗口对合常数 k_j=3·2^{j−2} 在 D(n) k_n=2^{n−4}(7n+2) 中的对照（k_9=2080=2^5·65 vs k_10=4608=2^9·9——两类 k 序列的连接）",
        "检验 CC：k_n 纯种子积条件（n 满足 7n+2 = 2^a·3^b·5^c 的枚举）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-212",
    ],
}

result = {
    "title": "P7-5e-211 k-family union discrimination & seed algebra intersection",
    "date": "2026-10-16",
    "YY": YY,
    "AA": AA,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-211 k-family union & seed intersection")
print("=" * 76)
print("[YY same-family discrimination]")
for r in YY_rows:
    print("  jp=%d window=%2d  6*4^jp=%6d  k_j formula at w=%6d  same=%s" % (
        r["jp"], r["window"], r["k_{2j+3}=6*4^jp"], r["k_j formula at w"], r["same"]))
print("[YY]", YY["check"])
print("  overlap_in_domain=%s  extended=%s" % (YY["overlap_in_domain"], YY["extended"]))
print("[AA seed intersection]")
for r in AA_rows:
    print("  n=%2d k=%8d = %-10s seed_hit=%s %s" % (
        r["n"], r["k_n"], r["factor"], r["seed_hit"], ("seed=" + str(r["seed"])) if r["seed_hit"] else ""))
print("[AA]", AA["check"])
print("  hits=%s  core_aligned_210=%s  k4=%d=%s" % (AA["hits"], AA["core_hits_aligned_210"], kn(4), AA["pure_seed_prod"]["factor"]))
print("[Conclusion]", conclusion["verdict"])
