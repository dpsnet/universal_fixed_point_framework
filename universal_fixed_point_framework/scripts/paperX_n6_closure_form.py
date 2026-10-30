# -*- coding: utf-8 -*-
"""n=6 闭式归纳：
1. 检验 generic 区乘积型闭式：(39) 的 R1 结构推广 A = c·∏(s_i + s_j)？
2. 检验"相邻对-累积对"乘积候选：6 个单对 + 4 首链 + 2 尾链 的哪些组合成闭式
3. 12 基座 → A_BG 规则性归纳：A=±1 模式的结构特征（非零判据）
"""
import json, os, random, sys
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_pair, sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_fullbasis import sg_pattern6_full

# 12 基座命名（0-based 下标 → 1-based 记号）
B12 = {
    0: "s1_23", 1: "s12_3", 2: "s123_4", 3: "s56", 4: "s23",
    5: "s1_234", 7: "s34", 10: "s12", 11: "s345_6", 12: "s45_6",
    13: "s45", 17: "s61",
}
BIDX = list(B12.keys())

def cache(n=50000, seed=51):
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        data.append((sg_pattern6_full(omega, zbar), round(A_BG(6, omega, zbar), 6)))
    return data

if __name__ == "__main__":
    data = cache(50000)
    base_to_a = {}
    for full, a in data:
        base = tuple(full[i] for i in BIDX)
        base_to_a[base] = a
    print(f"12 基座模式: {len(base_to_a)}")
    nonzero = {b: a for b, a in base_to_a.items() if abs(a) > 1e-9}
    print(f"非零模式: {len(nonzero)}  A=+1: {sum(1 for a in nonzero.values() if a > 0)}  A=-1: {sum(1 for a in nonzero.values() if a < 0)}")

    # 候选 1：乘积型闭式（(39) 推广）
    # 候选 2：R1 通式(39) 在 generic 区直接用？（4 个和因子）
    #   因子: (s23+s123),(s34+s1234),(s45+s12345),(s56+s123456)
    #   1-based: s123=sg({1},{2,3})=s1_23; s1234=s1_234; s12345=sg({1},{2,3,4,5});
    #   s123456=sg({1},{2..6})——generic 需要这些额外因子，先测 R1 型 4 因子
    # 用数据检验：对每个模式，A 是否 = c·∏(sg_i+sg_j)（c=1/16）

    # 候选 2 检验：(39) 4 和因子乘积符号 vs A 符号
    agree = 0
    fail = 0
    ex = []
    for b, a in nonzero.items():
        # 从 base tuple 恢复因子值（按 BIDX 顺序）
        d = dict(zip(BIDX, b))
        s23 = d[4]; s1_23 = d[0]
        s34 = d[7]; s1_234 = d[5]
        s45 = d[13]; s345_6 = d[11]  # s12345 不在基座 → 近似用 s345_6？不对
        s56 = d[3]
        # 检验 R1 因子 (s23+s1_23)(s34+s1_234)(s45+?)(s56+?)
        f1 = (s23 + s1_23) / 2.0  # 0/±1
        f2 = (s34 + s1_234) / 2.0
        f3 = (s45 + 0) / 2.0
        f4 = (s56 + 0) / 2.0
        # 粗糙：仅用 f1*f2 符号检验
        prod12 = f1 * f2
        if abs(prod12) > 1e-9:
            if (prod12 > 0) == (a > 0):
                agree += 1
            else:
                fail += 1
                if len(ex) < 3:
                    ex.append({"base": b, "a": a, "f1": f1, "f2": f2})
        else:
            # prod12=0 而 A≠0 → 一定失败（A 非零）
            fail += 1
            if len(ex) < 3:
                ex.append({"base": b, "a": a, "f1": f1, "f2": f2})
    print(f"候选2(R1 型 f1*f2 符号): 一致 {agree} 失败 {fail}")
    for e in ex[:3]:
        print("  ", e)

    # 候选 3：非零判据——A≠0 的模式结构归纳
    # 统计：非零模式里 12 因子的"和值"分布、模式是否有公共结构
    # 例如：A≠0 ⟺ 某 2-3 个因子的模式条件（类似 n=5 的 E6/E7 判据）
    # 尝试单因子判据：某个因子=固定值时 A≠0？
    zero_pats = {b: a for b, a in base_to_a.items() if abs(a) < 1e-9}
    nz = set(nonzero.keys())
    z = set(zero_pats.keys())
    # 对每个因子位置，检查 A≠0 是否与该因子值相关（信息增益）
    for pos, name in B12.items():
        # 分割：pos=+1 vs -1 下非零率
        sub_nz = Counter()
        sub_z = Counter()
        for b in nz:
            sub_nz[b[pos]] += 1
        for b in z:
            sub_z[b[pos]] += 1
        total_nz = len(nz)
        total_z = len(z)
        rate = {}
        for v in (-1, 1):
            n_nz = sub_nz[v]
            n_z = sub_z[v]
            rate[v] = (n_nz / (n_nz + n_z)) if (n_nz + n_z) else None
        print(f"  因子 {name}: 非零率 s=+1: {rate.get(1)}  s=-1: {rate.get(-1)}  (总非零率 {total_nz/(total_nz+total_z):.3f})")
    print("DONE")
