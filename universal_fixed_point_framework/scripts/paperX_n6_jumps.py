# -*- coding: utf-8 -*-
"""
Phase 71 待办：n=6 跳变测绘（S2/S4 的 n=6 版本，补全 3b 数据）
================================================================
S2_n6: R1 边界跨越（ω₁: -2→+2，动量守恒，n=6）——跳变位置/区域
S4_n6: 软极限连续性（对数扫 eps: 0.1→1e-4，n=6）
N4:    n=6 部分共线（S1 的 n=6 版）——非零率随 n 的标度
"""
import random
import sys

sys.path.insert(0, "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts")
from paperX_single_minus_numerics import sg_pair, sg_block, A_R1, soft_ratio
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear, gen_r1_crossing_path

SEED = 20260930
random.seed(SEED)


def scan_S2_n6(n=6, n_steps=200, n_runs=30):
    jumps = []
    for _ in range(n_runs):
        path = gen_r1_crossing_path(n, n_steps)
        prev_t, prev_a = None, None
        for t, omega, zbar in path:
            a = A_BG(n, omega, zbar)
            if prev_a is not None and a != prev_a:
                jumps.append((prev_t, t, prev_a, a))
            prev_t, prev_a = t, a
    n_jump_total = len(jumps)
    by_region = {}
    for pt, t, pa, a in jumps:
        w1 = 2.0 * (2 * t - 1)
        key = "omega1<0 (R1)" if w1 < 0 else "omega1>0"
        by_region[key] = by_region.get(key, 0) + 1
    return {"n_runs": n_runs, "n_steps": n_steps, "total_jumps": n_jump_total,
            "jumps_by_region": by_region}


def scan_S4_n6(n=6, eps_min=1e-4, n_steps=40, n_runs=10):
    jumps = 0
    samples = 0
    for _ in range(n_runs):
        prev_lhs = None
        for step in range(n_steps + 1):
            eps = 0.1 * (eps_min / 0.1) ** (step / n_steps)
            lhs, r1, r2 = soft_ratio(n, eps)
            samples += 1
            if prev_lhs is not None and lhs != prev_lhs:
                jumps += 1
            prev_lhs = lhs
    return {"n_runs": n_runs, "samples": samples, "lhs_changes_along_path": jumps}


def scan_S1_n6(n=6, k_max=2, n_samples=200):
    res = {}
    for k in range(0, k_max + 1):
        nonzero = 0
        vals = set()
        for _ in range(n_samples):
            omega, zbar, pairs = gen_partial_collinear(n, k, r1=True, momentum=True)
            a = A_BG(n, omega, zbar)
            if a != 0.0:
                nonzero += 1
            vals.add(round(a, 6))
        res[f"k_pairs={k}"] = {
            "samples": n_samples,
            "nonzero": nonzero,
            "nonzero_rate": round(nonzero / n_samples, 4),
            "distinct_values": sorted(vals),
        }
    return res


def main():
    print("=" * 72)
    print("Phase 71 n=6 跳变测绘（S2/S4/S1 的 n=6 版本）")
    print("=" * 72)

    print("\n[S2_n6] R1 边界跨越（n=6）")
    s2 = scan_S2_n6()
    print(f"  total_jumps={s2['total_jumps']}, by_region={s2['jumps_by_region']}")

    print("\n[S4_n6] 软极限连续性（n=6）")
    s4 = scan_S4_n6()
    print(f"  lhs_changes={s4['lhs_changes_along_path']}/{s4['samples']} 采样")

    print("\n[S1_n6] 部分共线（n=6，R1+动量守恒）")
    s1 = scan_S1_n6()
    for k, v in s1.items():
        print(f"  {k}: nonzero_rate={v['nonzero_rate']}, values={v['distinct_values']}")

    # 标度对比（n=5 vs n=6）
    print("\n[标度] 非零率 n=5 vs n=6（generic z，R1+动量守恒）")
    print("  n=5: ~30.9%（N1）;  n=6: ~15.5%（N3）;  S1_n6 k=0 独立样本确认中")

    out = {"S2_n6": s2, "S4_n6": s4, "S1_n6": s1}
    out_path = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_n6_jump_results.json"
    import json
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")


if __name__ == "__main__":
    main()
