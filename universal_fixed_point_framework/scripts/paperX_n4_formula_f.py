# -*- coding: utf-8 -*-
"""M25a：n=4 符号公式 F 验证（判据映射完备性的解析检查）
- 恒等式：动量守恒下 sg_41 = sg_12 - sg_23 + sg_34（括号值）
- 检验：A4 符号是否可由 (sg_12, sg_23, sg_34) 符号唯一决定
- 反例（同三符号不同 A4）→ |sg_41| 分布（环向因子近零假说）
"""
import os, json, sys, random
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import gen_R1_momentum, sg_pair, sg_block, A4


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    rng = random.Random(20261006)
    N = 200000
    ident_fail = 0
    pat_a4 = defaultdict(list)   # (s12,s23,s34) -> [a4 值]
    pat_s41 = defaultdict(list)  # (s12,s23,s34) -> [s41 值]
    pat_s41mag = defaultdict(list)
    for _ in range(N):
        omega, zbar = gen_R1_momentum(4, rng=rng)
        w, z = omega, zbar
        v12 = w[0] * w[1] * (z[0] - z[1])
        v23 = w[1] * w[2] * (z[1] - z[2])
        v34 = w[2] * w[3] * (z[2] - z[3])
        v41 = w[3] * w[0] * (z[3] - z[0])
        # 恒等式检查：v41 = v12 - v23 + v34
        if abs((v41) - (v12 - v23 + v34)) > 1e-6 * max(1.0, abs(v41)):
            ident_fail += 1
        a = A4(omega, zbar)
        t = (sg(v12), sg(v23), sg(v34))
        pat_a4[t].append(a)
        pat_s41[t].append(v41)
        pat_s41mag[t].append(abs(v41))
    print(f"恒等式失败（|v41 - (v12-v23+v34)| 超容差）：{ident_fail}/{N}")
    if ident_fail == 0:
        print("✓ 动量守恒恒等式 sg_41 = sg_12 - sg_23 + sg_34 精确成立（括号值）")

    # A4 符号唯一性
    ambig = 0
    n_sym = 0
    for t, vals in pat_a4.items():
        syms = {sg(v) for v in vals}
        n_sym += 1
        if len(syms) > 1:
            ambig += 1
            # 该模式的 s41 幅度 vs 全体
            mags = pat_s41mag[t]
            med = sorted(mags)[len(mags) // 2]
            print(f"  非决定三符号组合 {t}: A4 符号 {sorted(syms)}——样本数 {len(vals)}——|s41| 中位 {med:.4f}")
    print(f"\n三符号组合数 {n_sym} / 非决定（同组合不同 A4 符号）：{ambig}")

    # 反例计数（样本级）：同三符号出现不同 A4 的样本
    ambig_samples = 0
    for t, vals in pat_a4.items():
        if len({sg(v) for v in vals}) > 1:
            ambig_samples += len(vals)
    print(f"非决定组合内样本数：{ambig_samples}/{N} = {ambig_samples/N:.6f}")

    # 对照：|s41| 幅度（非决定组合 vs 全体）
    all_mag = [abs(v) for vals in pat_s41.values() for v in vals]
    all_med = sorted(all_mag)[len(all_mag) // 2]
    print(f"全体 |s41| 中位：{all_med:.4f}")

    out = {"ident_fail": ident_fail, "n_patterns": n_sym, "ambig_patterns": ambig,
           "ambig_samples": ambig_samples, "all_s41_med": all_med}
    with open(os.path.join(SCRIPT_DIR, "paperX_n4_formula_f.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n4_formula_f.json")
