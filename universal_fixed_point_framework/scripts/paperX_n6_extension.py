# -*- coding: utf-8 -*-
"""n=6 非决定性模式多值性结构分析 + 扩展因子候选检验。
多值性：A_BG 模式内取值集合结构（是否 0/±1 二分，或连续量依赖）。
扩展因子候选：所有连续块 vs 连续块的和序 sg（类似 n=5 的 E6/E7 候选集）。
"""
import json, os, random, sys
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_pair, sg_block, A6
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear

# 候选扩展因子：n=6 全部"连续块 vs 连续块"块和 sg（含单对）——按 (32) 的因子表
# 块区间用 0-based (start,len)；不交连续块对 (A,B)
BLOCKS6 = [(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),          # 单点
           (0,2),(1,2),(2,2),(3,2),(4,2),                # 长2
           (0,3),(1,3),(2,3),(3,3),                      # 长3
           (0,4),(1,4),(2,4),                            # 长4
           (0,5),(1,5)]                                  # 长5
# 连续块 = (start,len) 定义集合 {start..start+len-1}
def blockset(b):
    return frozenset(range(b[0], b[0] + b[1]))

# 候选扩展因子：全部不交连续块对（A∩B=∅），共 ~100 个
CANDIDATES = []
for i, ba in enumerate(BLOCKS6):
    for bb in BLOCKS6[i+1:]:
        if blockset(ba).isdisjoint(blockset(bb)):
            CANDIDATES.append((ba, bb))

def ext_signs(omega, zbar, cands=CANDIDATES):
    """计算全部候选扩展因子的 sg 值（三态 {-1,0,+1} 用 raw sign）"""
    w, z = omega, zbar
    return {c: sg_block(w, z, tuple(range(c[0][0], c[0][0]+c[0][1])),
                                tuple(range(c[1][0], c[1][0]+c[1][1]))) for c in cands}

def analyze(n_samples=30000, seed=7):
    rng = random.Random(seed)
    # 非决定性模式收集（12 因子基座）
    pat_a_bg = defaultdict(set)
    pat_cnt = Counter()
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern6(omega, zbar)
        pat_cnt[pat] += 1
        pat_a_bg[pat].add(round(A_BG(6, omega, zbar), 6))
    nondet = [p for p in pat_cnt if len(pat_a_bg[p]) > 1]
    print(f"样本 {n_samples}: 模式 {len(pat_cnt)} 非决定性 {len(nondet)}")
    # 多值性结构
    vc = Counter()
    for p in nondet:
        vc[len(pat_a_bg[p])] += 1
    print(f"非决定性模式按取值数分布: {dict(vc)}")
    # 取值集合形态（0 是否总在其中）
    withzero = sum(1 for p in nondet if 0.0 in pat_a_bg[p])
    print(f"含 0 的非决定性模式: {withzero}/{len(nondet)}")
    # 非零取值集合
    nz_sets = Counter()
    for p in nondet:
        nz = tuple(sorted(v for v in pat_a_bg[p] if abs(v) > 1e-9))
        nz_sets[nz] += 1
    print(f"非零取值集合形态: {dict(nz_sets)}")
    # 扩展因子检验：对每个非决定性模式，找"单因子闭合"候选（类似 n=5 的列 6/7）
    # 方法：重扫样本，记录 (模式, 各候选因子值) -> A_BG；看是否存在单个候选使模式内决定性
    # 为控制成本：只在 62 个非决定性模式的样本上统计（条件重扫）
    rng2 = random.Random(seed + 1)
    # (pat -> {ext_sign -> {A_BG val}})
    pat_ext_abg = defaultdict(lambda: defaultdict(set))
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng2)
        pat = sg_pattern6(omega, zbar)
        if pat not in set(nondet):
            continue
        a = round(A_BG(6, omega, zbar), 6)
        for c, s in ext_signs(omega, zbar).items():
            pat_ext_abg[pat][c].add((s, a))
    # 单因子闭合：存在候选 c 使 (s, a) 映射唯一（s 决定 a）
    single_closure = defaultdict(list)  # pat -> [候选名]
    for pat in nondet:
        for c, sa in pat_ext_abg[pat].items():
            by_s = defaultdict(set)
            for s, a in sa:
                by_s[s].add(a)
            if all(len(v) == 1 for v in by_s.values()):
                single_closure[pat].append(c)
    n_single = sum(1 for p in nondet if single_closure[p])
    print(f"单因子可闭合的非决定性模式: {n_single}/{len(nondet)}")
    # 无法单因子闭合的模式的候选数分布（需组合）
    no_single = [p for p in nondet if not single_closure[p]]
    print(f"无法单因子闭合: {len(no_single)} 个")
    # 保存摘要
    res = {
        "samples": n_samples,
        "nondet_count": len(nondet),
        "valcount_dist": dict(vc),
        "with_zero": withzero,
        "nonzero_sets": {str(k): v for k, v in nz_sets.items()},
        "single_closure_count": n_single,
        "no_single_count": len(no_single),
        "single_closure_candidates": {str(p): [str(c) for c in single_closure[p][:10]] for p in nondet if single_closure[p]},
    }
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_criterion_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")

if __name__ == "__main__":
    from paperX_n6_criterion import sg_pattern6
    analyze()
