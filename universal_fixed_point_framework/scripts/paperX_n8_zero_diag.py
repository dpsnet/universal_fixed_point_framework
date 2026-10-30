# -*- coding: utf-8 -*-
"""n=8 零恒等式诊断：s1_2345678 = sg(omega0 * S)，S = sum_{j=1..7} omega_j (zbar_0 - zbar_j)。
理论：动量守恒（Σω=0, Σωz̄=0）⇒ S = 0。检查 S 的实际数值分布 + sg 判零阈值。
"""
import os, random, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg
from paperX_degenerate_family_scan import gen_partial_collinear


def sg_raw(omega, zbar, A, B):
    s = 0.0
    for i in A:
        for j in B:
            s += omega[i] * omega[j] * (zbar[i] - zbar[j])
    return s


def main(n=2000, seed=101):
    rng = random.Random(seed)
    vals = []
    sums = []
    mom2 = []  # 动量守恒第二式 Σωz̄ 的残差
    mom1 = []
    for _ in range(n):
        omega, zbar, _ = gen_partial_collinear(8, 0, r1=True, momentum=True, rng=rng)
        s = sg_raw(omega, zbar, (0,), (1, 2, 3, 4, 5, 6, 7))
        vals.append(sg(s))
        sums.append(s)
        mom1.append(sum(omega))
        mom2.append(sum(omega[i] * zbar[i] for i in range(8)))
    print(f"Σω 残差: min={min(mom1):.3e} max={max(mom1):.3e}")
    print(f"Σωz̄ 残差: min={min(mom2):.3e} max={max(mom2):.3e}")
    nz = sum(1 for v in vals if v != 0)
    print(f"sg 非零: {nz}/{n}")
    big = [x for x in sums if abs(x) > 1e-9]
    print(f"S 值: min={min(sums):.3e} max={max(sums):.3e}  |S|>1e-9 的样本: {len(big)}")
    if big:
        print(f"  示例大 S: {big[:5]}")
    # 大 S 样本的 ω 结构
    rng2 = random.Random(seed)
    for _ in range(n):
        omega, zbar, _ = gen_partial_collinear(8, 0, r1=True, momentum=True, rng=rng2)
        s = sg_raw(omega, zbar, (0,), (1, 2, 3, 4, 5, 6, 7))
        if abs(s) > 1e-9:
            print(f"  大S样本: omega={[round(w, 3) for w in omega]} zbar={[round(z, 3) for z in zbar]} S={s:.4f}")
            break
    # 检查 sg 判零阈值
    print(f"sg 定义检查: sg(1e-16)={sg(1e-16)} sg(1e-10)={sg(1e-10)} sg(1e-8)={sg(1e-8)}")


if __name__ == "__main__":
    main()
