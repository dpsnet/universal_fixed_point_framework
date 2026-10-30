# -*- coding: utf-8 -*-
"""部分商 = 框架量平方加减构造？——系统扫描 + 对照（2026-10-26 用户直觉）

用户直觉：某些值 = 多个框架量构造的相加。
框架量平方：2²=4、3²=9、4²=16、5²=25、7²=49、8²=64、16²=256
（幂基、活跃、不动点、静默、对合域、k_max、全态）
检验：π 的部分商（≥3）能否表示为这些平方的加减组合？
对照：随机无理数的部分商呢？
"""
import mpmath as mp
import random, math
mp.mp.dps = 80

FW_SQS = {4: "幂基²", 9: "活跃²", 16: "不动点²", 25: "静默²", 49: "对合域²", 64: "k_max²", 256: "全态²"}
# 还有加单位项的组合（±1、±2、±3、±4、±5、±7、±8 等框架量）
FW_SMALL = {1: "单位", 2: "幂基", 3: "活跃", 4: "不动点", 5: "静默", 7: "对合域", 8: "k_max", 16: "全态", 42: "覆盖域"}

def cf_parts(x, n):
    parts = []
    for _ in range(n):
        a = int(x)
        parts.append(a)
        x = 1 / (x - a)
    return parts

def sq_framework_decomp(v):
    """尝试 v = a²±b²（a,b 为框架量）或 v = a²±c（c 为小框架量）"""
    results = []
    sq_keys = sorted(FW_SQS.keys())
    for a in sq_keys:
        for b in sq_keys:
            if a + b == v:
                results.append(f"{FW_SQS[a]}+{FW_SQS[b]}")
            if a - b == v and a > b:
                results.append(f"{FW_SQS[a]}−{FW_SQS[b]}")
    # a² ± c
    for a in sq_keys:
        for c, cn in FW_SMALL.items():
            if a + c == v:
                results.append(f"{FW_SQS[a]}+{cn}")
            if a - c == v:
                results.append(f"{FW_SQS[a]}−{cn}")
            if c - a == v:
                results.append(f"{cn}−{FW_SQS[a]}")
    return results

def add_framework_decomp(v):
    """尝试 v = 两个小框架量相加"""
    results = []
    ks = sorted(FW_SMALL.keys())
    for i, a in enumerate(ks):
        for b in ks[i:]:
            if a + b == v:
                results.append(f"{FW_SMALL[a]}+{FW_SMALL[b]}")
    return results

print("=== ① π 部分商（≥3）的框架量平方加减构造 ===")
parts_pi = cf_parts(mp.pi, 60)
nontriv = [a for a in parts_pi if a >= 3]
# 去重保持顺序
seen = set()
uniq = [a for a in nontriv if not (a in seen or seen.add(a))]
print(f"π 非平凡部分商（去重）: {uniq}")
for v in uniq:
    sq = sq_framework_decomp(v)
    ad = add_framework_decomp(v)
    tags = []
    if sq: tags.append("平方加减: " + "; ".join(sq[:3]))
    if ad: tags.append("框架量和: " + "; ".join(ad[:3]))
    print(f"  {v:>3}: {' | '.join(tags) if tags else '（无简单分解）'}")

print("\n=== ② 对照：随机无理数部分商（≥3，去重）===")
random.seed(42)
r = random.random() + 1.0
val = mp.mpf(str(r)) + mp.mpf(str(random.random())) * mp.mpf("1e-30")
parts_rnd = cf_parts(val, 60)
nr = [a for a in parts_rnd if a >= 3]
seen = set()
uniq_r = [a for a in nr if not (a in seen or seen.add(a))]
print(f"随机无理数非平凡部分商（去重）: {uniq_r}")
for v in uniq_r:
    sq = sq_framework_decomp(v)
    ad = add_framework_decomp(v)
    tags = []
    if sq: tags.append("平方加减: " + "; ".join(sq[:3]))
    if ad: tags.append("框架量和: " + "; ".join(ad[:3]))
    print(f"  {v:>3}: {' | '.join(tags) if tags else '（无简单分解）'}")

print("\n=== ③ 判别 ===")
print("比较 π 与随机数的分解覆盖——若 π 显著更'干净'则信号成立，否则为普遍现象")
