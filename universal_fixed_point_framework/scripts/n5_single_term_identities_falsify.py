# -*- coding: utf-8 -*-
"""
n5_single_term_identities_falsify.py
ENV_GUIDE 模式 8：先证伪再证明。
验证单非零项解析闭合的 3 条新恒等式（数值残差，容差 1e-8）：
  E-a: [λ₂,λ₃₄₅] = [λ₁,λ₂]        （bk{1}{234} = bk{0}{1}）
  E-b: [λ₂₃,λ₄₅] = [λ₁,λ₂₃]       （bk{12}{34} = bk{0}{12}）
  E-c: [λ₂₃₄,λ₅] = [λ₅,λ₁]        （bk{123}{4} = bk{4}{0}）
  Z:  bk A univ = 0（动量守恒一般引理）
随机 6+ 组（R1+动量守恒），残差全部 0 才可投入 Lean 证明。
"""
import sys
import random
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_degenerate_family_scan import gen_partial_collinear


def bk(omega, zbar, A, B):
    return sum(omega[i] * omega[j] * (zbar[i] - zbar[j]) for i in A for j in B)


def check(n=2000, seed=997):
    rng = random.Random(seed)
    worst = 0.0
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        # E-a: bk{1}{234} vs bk{0}{1}
        r1 = bk(omega, zbar, (1,), (2, 3, 4)) - bk(omega, zbar, (0,), (1,))
        # E-b: bk{12}{34} vs bk{0}{12}
        r2 = bk(omega, zbar, (1, 2), (3, 4)) - bk(omega, zbar, (0,), (1, 2))
        # E-c: bk{123}{4} vs bk{4}{0}
        r3 = bk(omega, zbar, (1, 2, 3), (4,)) - bk(omega, zbar, (4,), (0,))
        # Z: bk A univ = 0（A={1,2} 抽样）
        r4 = bk(omega, zbar, (1, 2), (0, 1, 2, 3, 4))
        worst = max(worst, abs(r1), abs(r2), abs(r3), abs(r4))
        if worst > 1e-8:
            print(f"FAIL @ {_}: r1={r1} r2={r2} r3={r3} r4={r4}")
            return False
    print(f"PASS：{n} 样本全部残差 0（最差 {worst:.2e}）")
    return True


if __name__ == "__main__":
    check()
