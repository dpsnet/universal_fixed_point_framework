# paperX_n5_equivalence_probe.py
# Phase 72 阶段4：存活条件 <-> E6=E7 等价的数值穷举验证 + 决定关系发现
# 目标：
# 1. 验证 C0∧C1 <-> (E6=E7=c) 100% 成立（模式 A/B 各采样）
# 2. 发现 C0/C1 与 E6/E7/8sg 的决定关系（C0 ⟺ ?、C1 ⟺ ?），为括号代数严格化铺路
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_bg_recursion import bracket
from paperX_single_minus_numerics import sg_block, sg_pair
from paperX_single_minus_bg_recursion import A_BG, _preamplitude_memo
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}


def signs(omega, zbar):
    """收集 8 sg + 相关块和括号符号"""
    out = {}
    # 单块括号
    for i in range(1, 6):
        for j in range(i + 1, 6):
            out[f"s{i}{j}"] = sg_pair(omega, zbar, i - 1, j - 1)
    # 块和括号
    def bs(A, B):
        A = tuple(a - 1 for a in A)
        B = tuple(b - 1 for b in B)
        return sg_block(omega, zbar, A, B)
    out["E6"] = bs((1, 2), (1, 2, 3))       # sg([λ12, λ123])
    out["E7"] = bs((1, 2), (1, 2, 3, 4))    # sg([λ12, λ1234])
    out["C0"] = bs((3,), (3, 4, 5))         # sg([λ3, λ345]) = sg([λ3, λ45])
    out["C1"] = bs((3, 4), (5,))            # sg([λ34, λ5])
    out["X0"] = bs((1, 2), (4, 5))          # sg([λ12, λ45])
    out["X1"] = bs((1, 2), (5,))            # sg([λ12, λ5])
    out["s35"] = sg_pair(omega, zbar, 2, 4)
    out["s24"] = sg_pair(omega, zbar, 1, 3)
    out["s14"] = sg_pair(omega, zbar, 0, 3)
    out["s25"] = sg_pair(omega, zbar, 1, 4)
    out["s15"] = sg_pair(omega, zbar, 0, 4)
    out["s12345"] = sg_block(omega, zbar, (0,), (1, 2, 3, 4))  # sg([λ1, λ2345])
    return out


def probe(n_samples=60000, seed=307):
    rng = random.Random(seed)
    stats = {p: defaultdict(int) for p in HARD}
    combos = {p: defaultdict(set) for p in HARD}
    equiv_viol = {p: 0 for p in HARD}
    total = {p: 0 for p in HARD}
    c_decided = {p: defaultdict(int) for p in HARD}  # (C0,C1) -> 是否由 (E6,E7) 决定
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        sg = signs(omega, zbar)
        e6, e7, c0, c1 = sg["E6"], sg["E7"], sg["C0"], sg["C1"]
        total[pat] += 1
        stats[pat][(e6, e7, c0, c1)] += 1
        _preamplitude_memo.clear()
        a = A_BG(5, omega, zbar)
        combos[pat][(e6, e7, c0, c1)].add(round(a, 6))
        # 等价检验：C0∧C1 <-> E6=E7=c
        c_ok = (c0 == -pat[2] and c1 == -pat[3])  # C0=-s34, C1=-s45（s34=pat[2], s45=pat[3]）
        e_ok = (e6 == e7)
        # 模式 A: c=-1, B: c=+1
        expected_c = -1 if pat == (-1, -1, 1, 1, -1, 1, 1, -1) else 1
        e_ok2 = (e6 == e7 == expected_c)
        if c_ok != e_ok2:
            equiv_viol[pat] += 1
    print("等价检验（C0∧C1 <-> E6=E7=c，c=模式期望值）：")
    for p in HARD:
        print(f"  pat={p}: 违反 {equiv_viol[p]}/{total[p]}（应为 0）")
    print("(E6,E7) -> (C0,C1) 决定关系：")
    for p in HARD:
        print(f"  pat={p}:")
        by_ee = defaultdict(set)
        for (e6, e7, c0, c1), n in stats[p].items():
            by_ee[(e6, e7)].add((c0, c1))
        for ee, cc in sorted(by_ee.items(), key=str):
            print(f"    (E6,E7)={ee} -> (C0,C1)集合={sorted(cc)}")
    # 汇总 A_BG 判定（可选）
    res = {"violations": {str(p): v for p, v in equiv_viol.items()}, "totals": {str(p): v for p, v in total.items()}}
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_equivalence_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n5_equivalence_results.json")


if __name__ == "__main__":
    probe()
