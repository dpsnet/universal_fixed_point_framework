# -*- coding: utf-8 -*-
"""n=6 判据闭合确认 + 完整判定表导出（80000 样本）：
1. 12 因子基座 → A 全决定性（含 0/±1 值）
2. 判定表导出（模式 → A 值）
3. 独立样本复核（防过拟合：新 seed 20000）
"""
import json, os, random, sys
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_fullbasis import sg_pattern6_full
from paperX_n6_base12 import BASE12

def cache(n, seed):
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        full = sg_pattern6_full(omega, zbar)
        base = tuple(full[i] for i in BASE12)
        data.append((base, round(A_BG(6, omega, zbar), 6)))
    return data

if __name__ == "__main__":
    data = cache(80000, 91)
    pat_a = {}
    for b, a in data:
        if b not in pat_a:
            pat_a[b] = a
        else:
            assert abs(pat_a[b] - a) < 1e-9, f"模式内不一致: {b}"
    print(f"主样本: 模式 {len(pat_a)}  全决定性 {all(len(v)==1 for v in [set([pat_a[b]]) for b in pat_a])}")

    # 独立复核
    data2 = cache(20000, 911)
    violations = 0
    for b, a in data2:
        if b not in pat_a:
            violations += 1  # 新模式（稀有）——不是违反，但记录
        elif abs(pat_a[b] - a) > 1e-9:
            violations += 1
            print(f"违反: {b} 表值 {pat_a[b]} 实测 {a}")
    new_modes = sum(1 for b, a in data2 if b not in pat_a)
    print(f"独立复核: 违反 {violations}, 新稀有模式 {new_modes}")

    # 判定表导出
    table = {",".join(map(str, b)): int(pat_a[b]) for b in pat_a}
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_base12_table.json"), "w", encoding="utf-8") as f:
        json.dump(table, f, ensure_ascii=False, indent=1)
    # 汇总
    valcnt = Counter(pat_a.values())
    print(f"判定表 {len(table)} 条: 值分布 {dict(valcnt)}")
    res = {"patterns": len(pat_a), "values": dict(valcnt),
           "verify_violations": violations, "verify_new_modes": new_modes}
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_final_summary.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n6_base12_table.json + paperX_n6_final_summary.json")
