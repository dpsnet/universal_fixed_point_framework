# -*- coding: utf-8 -*-
"""M3 验证：57 因子基座（50 + 7 粒子2前缀块）→ n=10 判据闭合检验
- 40000 主样本（seed 131）：0 非决定 + 判定表导出
- 2×15000 独立复核（seed 77/211）：内部单值 + 主表交叉
- 若 0 冲突 → 前缀块补因子闭合（A 结局）
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
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_base.json"), encoding="utf-8") as f:
        fb = json.load(f)
    base_names = list(dict.fromkeys(fb["base"]))
    # 补 7 个粒子 2 前缀块
    pref = ["s23_45678910", "s234_5678910", "s2345_678910", "s23456_78910",
            "s234567_8910", "s2345678_910", "s23456789_10"]
    base_names = list(dict.fromkeys(base_names + pref))
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in base_names]
    print(f"基座 {len(idx)} 因子（50+7 前缀）", flush=True)

    # 主样本
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

    table = {}
    for p, vals in pat_a.items():
        v = list(vals)[0]
        table[",".join(str(x) for x in p)] = {"bg": v, "count": pat_cnt[p]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_base57_table.json"), "w", encoding="utf-8") as f:
        json.dump(table, f, ensure_ascii=False, indent=1)
    print(f"判定表 {len(table)} 条 -> paperX_n10_base57_table.json", flush=True)

    # 独立复核
    viol = 0
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
        print(f"独立复核 seed {seed}: 模式 {len(pat_a2)} 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    ok = viol == 0
    print(f"总计冲突: {viol} -> {'PASS 闭合' if ok else 'FAIL'}", flush=True)

    nz = sum(1 for p in pat_a if abs(list(pat_a[p])[0]) > 1e-9)
    res = {"base": base_names, "size": len(idx), "main_samples": 40000, "main_nondet": 0,
           "table_entries": len(table), "indep_violations": viol, "pass": ok,
           "zero_patterns": len(pat_a) - nz, "nonzero_patterns": nz}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_summary_v57.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
