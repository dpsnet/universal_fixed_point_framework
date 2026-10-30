# -*- coding: utf-8 -*-
"""n=9 25 因子尾部基座大样本验证（n=8 教训：30000+10000 缓存会漏稀有非决定性）：
- 40000 主样本：模式全决定性 + 判定表导出
- 2×15000 独立复核（不同 seed）：0 真违反
失败 → 非决定性模式诊断（最小补因子）。
"""
import json, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n9_criterion import adj_partition_factors, sg_pattern9

BASE = ['s2_3', 's2_3456789', 's23_456789', 's234_56789', 's2345678_9',
        's3_4', 's3_456789', 's34_56789', 's345_6789',
        's4_5', 's4_56789', 's45678_9',
        's5_6', 's5_678', 's56_78', 's5_6789', 's5678_9',
        's6_7', 's67_8', 's6_789', 's678_9',
        's7_8', 's7_89', 's78_9', 's8_9']


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def pattern_on(omega, zbar, factors, idx):
    return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)


def scan(n_samples, seed, factors, idx, n=9):
    rng = random.Random(seed)
    pat_a = defaultdict(set)
    pat_cnt = Counter()
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar, factors, idx)
        pat_cnt[pat] += 1
        pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
    dt = time.time() - t0
    nondet = [p for p in pat_cnt if len(pat_a[p]) > 1]
    print(f"seed {seed} 样本 {n_samples} ({dt:.0f}s): 模式 {len(pat_cnt)} 决定性 {len(pat_cnt)-len(nondet)} 非决定性 {len(nondet)}", flush=True)
    if nondet:
        for p in nondet[:5]:
            print(f"  NON-DET {sorted(pat_a[p])} 频次 {pat_cnt[p]}", flush=True)
    return pat_a, pat_cnt, nondet


if __name__ == "__main__":
    factors = adj_partition_factors(9)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in BASE]
    assert len(idx) == 25
    print(f"基座 {len(idx)} 因子: {BASE}", flush=True)

    # 40000 主样本
    pat_a, pat_cnt, nondet = scan(40000, 131, factors, idx)
    if nondet:
        print("主样本失败——诊断非决定性模式的最小补因子（后续脚本）")
        sys.exit(1)

    # 判定表导出：模式 → 唯一值
    table = {}
    for p, vals in pat_a.items():
        v = list(vals)[0]
        table["".join(str((x >> 1) & 1) for x in p)] = v  # 位编码近似（±1 符号位）
    # 用原始 tuple 作键更可靠
    table2 = {}
    for p, vals in pat_a.items():
        v = list(vals)[0]
        table2[",".join(str(x) for x in p)] = {"bg": v, "count": pat_cnt[p]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n9_base25_table.json"), "w", encoding="utf-8") as f:
        json.dump(table2, f, ensure_ascii=False, indent=1)
    print(f"判定表 {len(table2)} 条 -> paperX_n9_base25_table.json", flush=True)

    # 2×15000 独立复核
    v1 = 0
    for seed in (77, 211):
        rng = random.Random(seed)
        bad = 0
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(9, 0, r1=True, momentum=True, rng=rng)
            pat = pattern_on(omega, zbar, factors, idx)
            a = round(A_BG(9, omega, zbar), 6)
            if a not in pat_a[pat]:
                bad += 1
        v1 += bad
        print(f"独立复核 seed {seed}: 违反 {bad}", flush=True)
    ok = v1 == 0
    print(f"2×15000 独立复核总计违反: {v1}  -> {'PASS' if ok else 'FAIL'}", flush=True)

    res = {"base": BASE, "size": len(BASE), "main_samples": 40000, "main_det": True,
           "table_entries": len(table2), "indep_violations": v1, "pass": ok}
    with open(os.path.join(SCRIPT_DIR, "paperX_n9_final_summary.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
