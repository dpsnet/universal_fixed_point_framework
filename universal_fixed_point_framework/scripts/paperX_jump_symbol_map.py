# -*- coding: utf-8 -*-
"""
Phase 71 待办4：跳变点解析判定——ω 符号组合 → A_BG 取值映射（n=5,6）
====================================================================
目标：
  1. 验证显式公式(31)(32)（A5/A6）在 generic z（非半共线）+ R1 + 动量守恒下
     是否仍与 BG 递归(21) 一致——论文只声明 R1 半共线区通式(39)，(31)(32) 的
     适用域是否更广（配合论文"R1 外通式 will appear elsewhere"留白）。
  2. 归纳 A_BG(5) ≠ 0 的符号判据：哪些 sg 组合模式给出非零（与 Lean 的
     r1_momentum_sign_identity 同类恒等式候选，n=5 版本）。
  3. 记录跳变点的符号结构（跳变 = ω/z̃ 符号格点变化驱动，S2/S4 已证）。
"""
import random
import json
import sys
from collections import Counter

sys.path.insert(0, "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts")
from paperX_single_minus_numerics import sg, sg_pair, sg_block, A5, A6, EXPLICIT
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear, _gen_momentum_r1

SEED = 20260930
random.seed(SEED)


def sg_pattern5(omega, zbar):
    """n=5 的 8 个 sg 因子（(31) 用）：s12,s23,s34,s45,s51,s123,s234,s1234"""
    w, z = omega, zbar
    return (
        sg_pair(w, z, 0, 1), sg_pair(w, z, 1, 2), sg_pair(w, z, 2, 3),
        sg_pair(w, z, 3, 4), sg_block(w, z, (4,), (0,)),
        sg_block(w, z, (0,), (1, 2)), sg_block(w, z, (1,), (2, 3)),
        sg_block(w, z, (0,), (1, 2, 3)),
    )


def scan_n5(n_samples=20000):
    """generic z + R1 + momentum：A5(31) vs A_BG，符号模式归纳"""
    n_agree = 0
    nonzero = 0
    zero = 0
    pat_count = Counter()      # (sg 8 元组) -> A5 值
    pat_nonzero = Counter()
    disagree = 0
    examples = []
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True)
        a_bg = A_BG(5, omega, zbar)
        a5 = A5(omega, zbar)
        if abs(a_bg - a5) < 1e-9:
            n_agree += 1
        else:
            disagree += 1
            if len(examples) < 3:
                examples.append({"a_bg": a_bg, "a5": a5, "omega": omega, "zbar": zbar})
        if a_bg != 0.0:
            nonzero += 1
        else:
            zero += 1
        pat = sg_pattern5(omega, zbar)
        pat_count[pat] += 1
        if a_bg != 0.0:
            pat_nonzero[pat] += 1
    # 归纳：非零率最高的模式 vs 全模式
    total_pats = len(pat_count)
    nonzero_pats = len(pat_nonzero)
    # 每种模式是否"确定性"给出同一值？
    deterministic = 0
    for pat, cnt in pat_count.items():
        vals = set()
        # 无法从 pat_count 直接得值分布，需重扫——用近似：统计模式的 A5 值
        # 简化：重新采样记录 (pat -> set of A5)
    return {
        "samples": n_samples,
        "agree_A5_vs_BG": n_agree,
        "disagree": disagree,
        "nonzero": nonzero,
        "nonzero_rate": round(nonzero / n_samples, 4),
        "total_patterns": total_pats,
        "nonzero_patterns": nonzero_pats,
        "nonzero_pattern_rate": round(nonzero_pats / total_pats, 4) if total_pats else None,
        "disagree_examples": examples,
    }


def scan_n6(n_samples=5000):
    """generic z + R1 + momentum：A6(32) vs A_BG"""
    n_agree = 0
    nonzero = 0
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True)
        a_bg = A_BG(6, omega, zbar)
        a6 = A6(omega, zbar)
        if abs(a_bg - a6) < 1e-9:
            n_agree += 1
        if a_bg != 0.0:
            nonzero += 1
    return {
        "samples": n_samples,
        "agree_A6_vs_BG": n_agree,
        "disagree": n_samples - n_agree,
        "nonzero": nonzero,
        "nonzero_rate": round(nonzero / n_samples, 4),
    }


def scan_n5_value_map(n_samples=60000):
    """精确：模式 → A5 值分布（决定论检验）"""
    pat_vals = {}
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True)
        pat = sg_pattern5(omega, zbar)
        a = A_BG(5, omega, zbar)
        pat_vals.setdefault(pat, set()).add(round(a, 6))
    # 确定性模式比例
    det = sum(1 for p, v in pat_vals.items() if len(v) == 1)
    nondet = {p: v for p, v in pat_vals.items() if len(v) > 1}
    # 非零判定：找"某模式总是非零"或"某模式总为零"
    always_nonzero = [p for p, v in pat_vals.items() if 0.0 not in v]
    always_zero = [p for p, v in pat_vals.items() if v == {0.0}]
    return {
        "samples": n_samples,
        "patterns_seen": len(pat_vals),
        "deterministic_patterns": det,
        "nondeterministic_count": len(nondet),
        "nondeterministic_examples": list(nondet.items())[:5],
        "always_nonzero_count": len(always_nonzero),
        "always_zero_count": len(always_zero),
    }


def main():
    print("=" * 72)
    print("Phase 71 待办4：符号模式 → A_BG 取值映射（n=5,6，generic z + R1 + momentum）")
    print("=" * 72)

    print("\n[N1] n=5：A5(31) vs BG 递归（generic z）")
    n1 = scan_n5()
    print(f"  agree={n1['agree_A5_vs_BG']}/{n1['samples']}, disagree={n1['disagree']}")
    print(f"  非零率={n1['nonzero_rate']}, 模式数={n1['total_patterns']}, "
          f"非零模式数={n1['nonzero_patterns']}（{n1['nonzero_pattern_rate']}）")
    for e in n1["disagree_examples"]:
        print(f"  不一致例: a_bg={e['a_bg']}, a5={e['a5']}")

    print("\n[N2] n=5：模式决定论检验（60000 采样）")
    n2 = scan_n5_value_map()
    print(f"  模式数={n2['patterns_seen']}, 决定性模式={n2['deterministic_patterns']}, "
          f"非决定性={n2['nondeterministic_count']}")
    print(f"  恒非零模式={n2['always_nonzero_count']}, 恒零模式={n2['always_zero_count']}")
    for p, v in n2["nondeterministic_examples"]:
        print(f"  非决定性例: sg={p}, vals={v}")

    print("\n[N3] n=6：A6(32) vs BG 递归（generic z）")
    n3 = scan_n6()
    print(f"  agree={n3['agree_A6_vs_BG']}/{n3['samples']}, disagree={n3['disagree']}")
    print(f"  非零率={n3['nonzero_rate']}")

    out = {"N1": n1, "N2": n2, "N3": n3}
    out_path = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_jump_symbol_map_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")


if __name__ == "__main__":
    main()
