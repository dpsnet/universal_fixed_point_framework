# -*- coding: utf-8 -*-
"""n=7 级联机制诊断：被删因子 vs 16 因子基座的决定关系。
问题：16 基座不含 s1_2 / s7_1 等 40 个相邻分割因子，但 A_BG 全决定性。
两种可能：
(a) 级联决定：同 16 基座模式 → 被删因子值唯一（被基座因子代数决定）
(b) 冗余不敏感：同基座模式 → 被删因子值可变，但 A_BG 对之不变
诊断：对每个被删因子，统计"同基座模式内取值唯一"的样本覆盖率。
"""
import json, os, random, sys, time
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n7_criterion import adj_partition_factors, sg_pattern7
from paperX_n7_minbasis import factor_name

N7 = 7


def run(n_samples=40000, seed=41):
    factors = adj_partition_factors(N7)
    names = [factor_name(a, b) for a, b in factors]
    with open(os.path.join(SCRIPT_DIR, "paperX_n7_minbasis_results.json"), encoding="utf-8") as f:
        res = json.load(f)
    basis_names = res["remove_set"]
    basis_idx = [names.index(x) for x in basis_names]
    deleted = [i for i in range(len(factors)) if i not in basis_idx]
    print(f"基座 {len(basis_idx)} 因子，被删 {len(deleted)} 因子")

    rng = random.Random(seed)
    # base_mode -> {deleted_idx: set of values}
    base_val = defaultdict(lambda: defaultdict(set))
    base_cnt = Counter()
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(N7, 0, r1=True, momentum=True, rng=rng)
        full = sg_pattern7(omega, zbar, factors)
        key = tuple(full[i] for i in basis_idx)
        base_cnt[key] += 1
        for j in deleted:
            base_val[key][j].add(full[j])
    dt = time.time() - t0
    print(f"样本 {n_samples} ({dt:.0f}s), 基座模式 {len(base_cnt)}")

    # 对每个被删因子：同基座模式内取值唯一的覆盖率
    print("\n被删因子的级联决定率（同基座模式 → 值唯一）:")
    results = {}
    for j in deleted:
        uniq = 0
        mult = 0
        for key, dm in base_val.items():
            v = dm[j]
            n = base_cnt[key]
            if len(v) == 1:
                uniq += n
            else:
                mult += n
        rate = uniq / (uniq + mult) if (uniq + mult) else 0
        results[names[j]] = {"unique_samples": uniq, "multi_samples": mult, "cascade_rate": round(rate, 4)}
        print(f"  {names[j]:12s} 唯一 {uniq:6d}  多值 {mult:6d}  级联率 {rate:.3f}")

    # 特写：s1_2 与 s7_1 在多值模式里的取值分布 + A_BG 是否变化
    print("\ns1_2 / s7_1 多值模式内 A_BG 检查（若 A_BG 不变 → 冗余不敏感；若变 → 基座缺陷）:")
    j12 = names.index("s1_2")
    j71 = names.index("s7_1")
    # 重新采样记录 (基座模式, s1_2, s7_1, A_BG)
    rng2 = random.Random(seed + 1)
    pat_a = defaultdict(set)
    pat_v12 = defaultdict(set)
    pat_v71 = defaultdict(set)
    for _ in range(20000):
        omega, zbar, _ = gen_partial_collinear(N7, 0, r1=True, momentum=True, rng=rng2)
        full = sg_pattern7(omega, zbar, factors)
        key = tuple(full[i] for i in basis_idx)
        a = round(A_BG(N7, omega, zbar), 6)
        pat_a[key].add(a)
        pat_v12[key].add(full[j12])
        pat_v71[key].add(full[j71])
    n_abg_mult = sum(1 for k in pat_a if len(pat_a[k]) > 1)
    n_v12_mult = sum(1 for k in pat_v12 if len(pat_v12[k]) > 1)
    n_v71_mult = sum(1 for k in pat_v71 if len(pat_v71[k]) > 1)
    print(f"  A_BG 多值模式: {n_abg_mult}  s1_2 多值模式: {n_v12_mult}  s7_1 多值模式: {n_v71_mult}")
    # 多值模式里 A_BG 是否仍单值
    conflict = 0
    for k in pat_v12:
        if len(pat_v12[k]) > 1:
            if len(pat_a[k]) > 1:
                conflict += 1
    print(f"  s1_2 可变但 A_BG 仍单值的模式数（冗余型证据）: {n_v12_mult - conflict}  （A_BG 也变的: {conflict}）")

    out = {"n_samples": n_samples, "deleted": results, "s1_2_mult": n_v12_mult,
           "s7_1_mult": n_v71_mult, "a_bg_mult": n_abg_mult,
           "s1_2_var_but_abg_single": n_v12_mult - conflict}
    with open(os.path.join(SCRIPT_DIR, "paperX_n7_cascade_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n7_cascade_results.json")


if __name__ == "__main__":
    run()
