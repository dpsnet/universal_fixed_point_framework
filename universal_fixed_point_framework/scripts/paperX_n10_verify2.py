# -*- coding: utf-8 -*-
"""n=10 最终验证：N 因子基座（尾部 + 补因子，由 nondet_diag/minbasis 决定）
- 40000 主样本：0 非决定性 + 判定表导出
- 2×15000 独立复核（seed 77/211）：函数性验证（内部单值 + 主表交叉）
"""
import json, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def pattern_on(omega, zbar, factors, idx):
    return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)


if __name__ == "__main__":
    # 基座来源：优先 final_base（诊断终版），再 nondet_diag，再 indep_check，再 minbasis
    final_path = os.path.join(SCRIPT_DIR, "paperX_n10_final_base.json")
    if os.path.exists(final_path):
        with open(final_path, encoding="utf-8") as f:
            fb = json.load(f)
        base_names = fb["base"]
    elif os.path.exists(os.path.join(SCRIPT_DIR, "paperX_n10_nondet_diag.json")):
        with open(os.path.join(SCRIPT_DIR, "paperX_n10_nondet_diag.json"), encoding="utf-8") as f:
            diag = json.load(f)
        base_names = diag["base"] + diag.get("chosen_complements", [])
    elif os.path.exists(os.path.join(SCRIPT_DIR, "paperX_n10_indep_check_results.json")):
        with open(os.path.join(SCRIPT_DIR, "paperX_n10_indep_check_results.json"), encoding="utf-8") as f:
            indep = json.load(f)
        base_names = indep["base"] + indep.get("chosen_complements", [])
    else:
        with open(os.path.join(SCRIPT_DIR, "paperX_n10_minbasis_results.json"), encoding="utf-8") as f:
            mb = json.load(f)
        base_names = mb["remove_set"]
    base_names = list(dict.fromkeys(base_names))  # 去重保序

    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in base_names]
    print(f"基座 {len(idx)} 因子: {base_names}", flush=True)

    # 40000 主样本
    rng = random.Random(131)
    pat_a = defaultdict(set)
    pat_cnt = Counter()
    t0 = time.time()
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar, factors, idx)
        pat_cnt[pat] += 1
        pat_a[pat].add(round(A_BG(10, omega, zbar), 6))
    nondet = [p for p in pat_a if len(pat_a[p]) > 1]
    print(f"主样本 40000 ({time.time()-t0:.0f}s): 模式 {len(pat_a)} 非决定性 {len(nondet)}", flush=True)
    if nondet:
        print("主样本失败", flush=True)
        sys.exit(1)

    # 判定表导出（原始 tuple 键 → 唯一值）
    table = {}
    for p, vals in pat_a.items():
        v = list(vals)[0]
        table[",".join(str(x) for x in p)] = {"bg": v, "count": pat_cnt[p]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_base_table.json"), "w", encoding="utf-8") as f:
        json.dump(table, f, ensure_ascii=False, indent=1)
    print(f"判定表 {len(table)} 条 -> paperX_n10_base_table.json", flush=True)

    # 2×15000 独立复核（函数性验证：内部单值 + 主表交叉）
    viol = 0
    indep_tables = []
    for seed in (77, 211):
        rng = random.Random(seed)
        pat_a2 = defaultdict(set)
        bad = 0
        t0 = time.time()
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
            pat = pattern_on(omega, zbar, factors, idx)
            pat_a2[pat].add(round(A_BG(10, omega, zbar), 6))
        for p, vals in pat_a2.items():
            if len(vals) > 1:
                bad += 1
            if p in pat_a and not vals <= pat_a[p]:
                bad += 1
        viol += bad
        indep_tables.append((len(pat_a2), bad))
        print(f"独立复核 seed {seed}: 模式 {len(pat_a2)} 内部非决定+主表冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    ok = viol == 0
    print(f"2×15000 独立复核总计冲突: {viol} -> {'PASS' if ok else 'FAIL'}", flush=True)

    nz = sum(1 for p in pat_a if abs(list(pat_a[p])[0]) > 1e-9)
    zero = len(pat_a) - nz
    print(f"取值分布: 零模式 {zero}  非零模式 {nz} ({nz*100.0/len(pat_a):.1f}%)", flush=True)

    res = {"base": base_names, "size": len(idx), "main_samples": 40000, "main_nondet": 0,
           "table_entries": len(table), "indep_violations": viol, "pass": ok,
           "zero_patterns": zero, "nonzero_patterns": nz}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_summary.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
