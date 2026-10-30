# -*- coding: utf-8 -*-
"""M39：全补恒 0 因子排查 + 阈值化谱维数重估
- 全补块（a∪b = 全粒子）动量恒等 0——浮点噪声给 ±1 伪符号
- 排查 44 名单中的全补因子 + 删除后冲突 + 阈值化重采样重做极小化
"""
import os, sys, json, pickle, random, time
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_single_minus_numerics import sg_block


def sg_thr(x, thr=1e-6):
    if x > thr:
        return 1
    if x < -thr:
        return -1
    return 0


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len({sg_thr(v) for v in vals}) > 1)


def group(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return pat


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    m34c = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m34c_minimal.json"), encoding="utf-8"))
    names44 = m34c["final_names"]

    # 全补块识别：a∪b = 全粒子集 {0..10}（用原始 (a,b)——按名字反查）
    fullset = set(range(n))
    fullcomp = []
    for nm in names44:
        a, b = factors[NAMES.index(nm)]
        if set(a) | set(b) == fullset:
            fullcomp.append(nm)
    print(f"44 名单中全补块（数学恒 0）：{len(fullcomp)} 个 -> {fullcomp}")

    # 全 220 中全补块数量
    all_fullcomp = []
    for a, b in factors:
        if set(a) | set(b) == fullset:
            all_fullcomp.append(factor_name(a, b))
    print(f"220 全因子中全补块：{len(all_fullcomp)} 个")

    # 缓存重采样：高精度判零（阈值化符号）→ 全补块分布验证
    rng = random.Random(77)
    thr_cnt = Counter()
    for i in range(5000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        for a, b in factors:
            if set(a) | set(b) == fullset:
                v = 0.0
                for x in a:
                    for y in b:
                        v += omega[x] * omega[y] * (zbar[x] - zbar[y])
                thr_cnt[sg_thr(v)] += 1
    print(f"全补块阈值化符号分布（5000 样本×{len(all_fullcomp)} 因子）：{dict(thr_cnt)}")
