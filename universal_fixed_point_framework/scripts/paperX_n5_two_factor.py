# paperX_n5_two_factor.py
# Phase 72 阶段4 简化验证：困难模式双列规则 (列6, 列7) 独立大样本验证
# 若通过 -> n=5 判据 = 8 sg + 2 扩展因子（列6=sg([λ12,λ123])、列7=sg([λ12,λ1234])）
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}


def all_ext_sgs(omega, zbar):
    n = len(omega)
    labels = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            labels.append((i + 1, j))
    out = []
    for a in labels:
        for b in labels:
            ia, ja = a
            ib, jb = b
            if ja <= ib or jb <= ia:
                continue
            va = sg_block(omega, zbar, tuple(range(ia - 1, ja - 1)), tuple(range(ib - 1, jb - 1)))
            out.append(((a, b), va))
    return out


def hard_two_factor_verify(n_target=2000, seeds=(167, 211)):
    """困难模式双列规则 (列6,列7) 独立验证：两组不同 seed"""
    results = {}
    for seed in seeds:
        rng = random.Random(seed)
        counts = defaultdict(int)
        combo_vals = defaultdict(lambda: defaultdict(set))  # 模式 -> (c6,c7) -> A_BG 值集
        while min(counts.get(p, 0) for p in HARD) < n_target:
            omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
            pat = sg_pattern5(omega, zbar)
            if pat not in HARD:
                continue
            counts[pat] += 1
            exts = all_ext_sgs(omega, zbar)
            c6, c7 = exts[6][1], exts[7][1]
            a = A_BG(5, omega, zbar)
            combo_vals[pat][(c6, c7)].add(round(a, 6))
        viol = {}
        for pat, combos in combo_vals.items():
            for combo, vals in combos.items():
                if len(vals) > 1:
                    viol[(pat, combo)] = sorted(vals)
        print(f"seed={seed}: 困难模式样本 {dict(counts)}")
        print(f"  (列6,列7) 组合非决定性: {len(viol)}（应为 0）")
        for k, v in list(viol.items())[:3]:
            print(f"    {k} -> {v}")
        results[seed] = {"counts": {str(k): v for k, v in counts.items()}, "violations": {str(k): v for k, v in viol.items()}}
    return results


def single_rule_recheck(n_samples=60000, seed=199):
    """14 个单因子模式 + 36 决定性模式：列6/7 复核（8 sg + 单因子 -> A_BG 唯一）"""
    rng = random.Random(seed)
    nondet = {}
    total = 0
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        exts = all_ext_sgs(omega, zbar)
        key = pat + (exts[6][1], exts[7][1])
        a = A_BG(5, omega, zbar)
        vals = nondet.setdefault(key, set())
        vals.add(round(a, 6))
        total += 1
    viol = {k: sorted(v) for k, v in nondet.items() if len(v) > 1}
    print(f"全局复核: {total} 样本, 8sg+2因子 非决定性键: {len(viol)}（应为 0——除困难模式双列组合）")
    return total, viol


def main():
    print("=== 困难模式双列规则独立验证 ===", flush=True)
    hard_res = hard_two_factor_verify()
    print("=== 全局复核（8 sg + 列6/列7）===", flush=True)
    total, viol = single_rule_recheck()
    for k, v in list(viol.items())[:8]:
        print(f"  反例键: 模式 {k[:8]} (c6,c7)={k[8:]} -> A_BG={v}")
    res = {
        "hard_two_factor": hard_res,
        "global_recheck_samples": total,
        "global_recheck_nondet_keys": len(viol),
        "global_recheck_violations": {str(k): v for k, v in list(viol.items())[:10]},
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_two_factor_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> scripts/paperX_n5_two_factor_results.json")


if __name__ == "__main__":
    main()
