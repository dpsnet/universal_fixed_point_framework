# -*- coding: utf-8 -*-
"""n=6 判据闭合深化：单因子闭合的最小候选统计 + 29 个难模式双因子闭合检验。
方法：对每个非决定性模式，(候选因子sg) → A_BG 映射唯一性；
双因子：候选对 (c1,c2) 的联合 sg 决定 A_BG。
输出：常用闭合因子频次、难模式双因子闭合率。
"""
import json, os, random, sys
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_criterion import sg_pattern6
from paperX_n6_extension import CANDIDATES, ext_signs

def scan_closure(n_samples=40000, seed=11):
    rng = random.Random(seed)
    pat_a_bg = defaultdict(set)
    pat_cnt = Counter()
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern6(omega, zbar)
        pat_cnt[pat] += 1
        pat_a_bg[pat].add(round(A_BG(6, omega, zbar), 6))
    nondet = [p for p in pat_cnt if len(pat_a_bg[p]) > 1]
    ndset = set(nondet)
    print(f"样本 {n_samples}: 模式 {len(pat_cnt)} 非决定性 {len(nondet)}")

    # 重扫：只收集非决定性模式的 (模式, 候选sg, A_BG)
    rng2 = random.Random(seed + 1)
    data = defaultdict(list)  # pat -> [(ext_signs_tuple_dict, a)]
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng2)
        pat = sg_pattern6(omega, zbar)
        if pat not in ndset:
            continue
        a = round(A_BG(6, omega, zbar), 6)
        data[pat].append((ext_signs(omega, zbar), a))

    # 单因子闭合：候选 c 的 sg 决定 a
    single_freq = Counter()  # c -> 闭合的模式数
    single_closure = {}
    for pat in nondet:
        closes = []
        for c in CANDIDATES:
            by_s = defaultdict(set)
            for es, a in data[pat]:
                by_s[es[c]].add(a)
            if all(len(v) == 1 for v in by_s.values()):
                closes.append(c)
        single_closure[pat] = closes
        for c in closes:
            single_freq[c] += 1
    n_single = sum(1 for p in nondet if single_closure[p])
    print(f"单因子闭合: {n_single}/{len(nondet)}")
    hard = [p for p in nondet if not single_closure[p]]
    print(f"难模式: {len(hard)}")

    top = single_freq.most_common(15)
    print("最常用单闭合因子:")
    for c, k in top:
        print(f"  {c}: 闭合 {k} 个模式")

    # 双因子闭合（难模式）：候选对 sg 联合决定 a
    # 候选约 100 个 → 对约 5000；每对检查所有样本，成本高。剪枝：先取高频单因子
    # 列表（top 30）两两组合 + 每个难模式专属尝试
    top_cands = [c for c, _ in single_freq.most_common(30)]
    pairs_res = {}
    for pat in hard:
        closed_by = []
        # 尝试 top 候选两两组合
        for i in range(len(top_cands)):
            for j in range(i + 1, len(top_cands)):
                c1, c2 = top_cands[i], top_cands[j]
                by_pair = defaultdict(set)
                for es, a in data[pat]:
                    by_pair[(es[c1], es[c2])].add(a)
                if all(len(v) == 1 for v in by_pair.values()):
                    closed_by.append((c1, c2))
        pairs_res[pat] = closed_by
    n_pair = sum(1 for p in hard if pairs_res[p])
    print(f"难模式双因子闭合(top30 候选): {n_pair}/{len(hard)}")
    # 未闭合的
    still_hard = [p for p in hard if not pairs_res[p]]
    print(f"仍无法闭合: {len(still_hard)}")

    # 保存
    def cstr(c):
        return f"{c[0]}vs{c[1]}"
    res = {
        "samples": n_samples,
        "nondet": len(nondet),
        "single_closed": n_single,
        "hard": len(hard),
        "top_single_factors": [{"cand": cstr(c), "closed": k} for c, k in top],
        "hard_pair_closed": n_pair,
        "hard_pair_examples": {str(p): [f"{cstr(a)}&{cstr(b)}" for a, b in pairs_res[p][:8]] for p in hard if pairs_res[p]},
        "still_hard": [str(p) for p in still_hard],
    }
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_closure_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n6_closure_results.json")

if __name__ == "__main__":
    scan_closure()
