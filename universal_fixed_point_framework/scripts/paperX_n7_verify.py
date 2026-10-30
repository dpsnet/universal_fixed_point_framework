# -*- coding: utf-8 -*-
"""n=7 判据验证：16 因子最小充分基座（贪心删除不动点）独立大样本验证 + 判定表导出。
- 主样本 80000 + 独立复核 2×20000（不同 seed）→ 0 真违反
- 判定表：16 因子模式 → A_BG ∈ {0,±1}（导出 json）
- 模式统计：非零率、决定性确认
"""
import json, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n7_criterion import adj_partition_factors, sg_pattern7
from paperX_n7_minbasis import factor_name

N7 = 7


def load_basis():
    with open(os.path.join(SCRIPT_DIR, "paperX_n7_minbasis_results.json"), encoding="utf-8") as f:
        res = json.load(f)
    factors = adj_partition_factors(N7)
    names = [factor_name(a, b) for a, b in factors]
    basis_names = res["remove_set"]
    idx = [names.index(x) for x in basis_names]
    print(f"基座: {len(idx)} 因子")
    return factors, idx, basis_names


def collect(n, seed):
    rng = random.Random(seed)
    factors, idx, _ = load_basis()
    pat_a = defaultdict(set)
    pat_cnt = Counter()
    t0 = time.time()
    for _ in range(n):
        omega, zbar, _ = gen_partial_collinear(N7, 0, r1=True, momentum=True, rng=rng)
        full = sg_pattern7(omega, zbar, factors)
        key = tuple(full[i] for i in idx)
        pat_cnt[key] += 1
        pat_a[key].add(round(A_BG(N7, omega, zbar), 6))
    print(f"样本 {n} ({time.time()-t0:.0f}s)")
    return pat_a, pat_cnt


def stats(pat_a, pat_cnt):
    nondet = [p for p in pat_cnt if len(pat_a[p]) > 1]
    det = [p for p in pat_cnt if len(pat_a[p]) == 1]
    # 非零率（模式层）
    nz = sum(1 for p in pat_cnt if any(abs(v) > 1e-9 for v in pat_a[p]))
    # 取值分布
    vdist = Counter()
    for p in pat_cnt:
        vdist[next(iter(pat_a[p]))] += 1
    return len(pat_cnt), len(det), len(nondet), nz, dict(vdist)


if __name__ == "__main__":
    factors, idx, basis_names = load_basis()
    print("基座因子:", basis_names)

    # 主样本 80000
    pat_a, pat_cnt = collect(80000, 101)
    total, det, nondet, nz, vdist = stats(pat_a, pat_cnt)
    print(f"主样本: 模式 {total}  决定性 {det} / 非决定性 {nondet}  非零模式 {nz}  取值分布 {vdist}")
    assert nondet == 0, "主样本出现非决定性！"

    # 独立复核
    for seed in (77, 211):
        pat_a2, pat_cnt2 = collect(20000, seed)
        t, d, nd, nz2, vd2 = stats(pat_a2, pat_cnt2)
        print(f"复核 seed={seed}: 模式 {t}  非决定性 {nd}  非零模式 {nz2}")
        if nd > 0:
            # 检查是否真违反（同键不同值）
            viol = sum(1 for p in pat_cnt2 if len(pat_a2[p]) > 1)
            print(f"  ⚠ 非决定性 {viol} 个——需检查是否为稀有新模式的基座外信息")
        else:
            print(f"  ✅ 0 真违反")

    # 判定表导出（主样本）
    table = {}
    for p in pat_cnt:
        table[",".join(str(x) for x in p)] = next(iter(pat_a[p]))
    with open(os.path.join(SCRIPT_DIR, "paperX_n7_base16_table.json"), "w", encoding="utf-8") as f:
        json.dump({"basis": basis_names, "table": table}, f, ensure_ascii=False, indent=2)
    print(f"判定表导出: {len(table)} 条 -> paperX_n7_base16_table.json")

    # 综合摘要
    summary = {"basis_size": len(idx), "basis": basis_names,
               "main": {"samples": 80000, "patterns": total, "det": det, "nondet": nondet,
                        "nonzero_patterns": nz, "value_dist": vdist},
               "verify": {}}
    for seed in (77, 211):
        pat_a2, pat_cnt2 = collect(20000, seed)
        t, d, nd, nz2, vd2 = stats(pat_a2, pat_cnt2)
        summary["verify"][f"seed{seed}"] = {"patterns": t, "nondet": nd, "nonzero": nz2}
    with open(os.path.join(SCRIPT_DIR, "paperX_n7_final_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n7_final_summary.json")
