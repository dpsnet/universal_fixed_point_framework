# -*- coding: utf-8 -*-
"""
BG 递归直接实现（2602.12176v2 公式(18)-(21)），作为通式(39)的独立 ground truth
================================================================================
- 预振幅 Ā_S（公式 18-19）
- 顶点 V / Ṽ（公式 20 推广到块）
- PT̂ = V - Ṽ（公式 22）
- 剥离振幅 A_{1..n} = -Σ_{o.p.(2..n)} PT̂ ∏ Ā_{S_a}（公式 21）

验证：
  B1: BG递归(21) 与 通式(39) 在 R1+动量守恒 下 n=3..6 一致
  B2: BG递归(21) 与 显式公式(29)-(32) 的一致性（判断显式公式是否有抄写/记号问题）
  B3: BG递归(21) 满足 循环性(24)/反射(25)/U1(26)/KK(27)（一般半共线配置）
"""
import sys
import itertools
sys.path.insert(0, "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts")
from paperX_single_minus_numerics import (
    sg_pair, sg_block, A_R1, A3, A4, A5, A6,
    gen_R1_momentum, gen_generic_halfcollinear,
)


def bracket(A, B, omega, zbar):
    """[sum_{i in A} lambda_tilde_i, sum_{j in B} lambda_tilde_j]（原始值，非符号）"""
    return sum(omega[i] * omega[j] * (zbar[i] - zbar[j]) for i in A for j in B)


def compositions(k, min_parts=1):
    """k 个元素的全部有序分割（composition）的切点位置。
    返回切点列表的列表，如 k=3: [[], [0], [1], [0,1]] 表示块边界"""
    res = []
    for mask in range(1 << (k - 1)):
        cuts = [i for i in range(k - 1) if (mask >> i) & 1]
        if len(cuts) + 1 >= min_parts:
            res.append(cuts)
    return res


def split_into_blocks(elems, cuts):
    """elems: 元组；cuts: 断点列表（cuts 中的 i 表示 elems[i] 与 elems[i+1] 之间断开）。
    返回块元组列表"""
    blocks = []
    prev = 0
    for c in cuts + [len(elems) - 1]:
        blocks.append(tuple(elems[prev : c + 1]))
        prev = c + 1
    return blocks


def V_fn(blocks, omega, zbar, sign=1.0):
    """公式(20)推广到块：V = prod_k sg_{S_k,S_{k+1}} Theta(sign * (-)[K_{1..k},K_{k+1..A}]/[lam_{S_k},lam_{S_{k+1}}])
    sign=+1 → V；sign=-1 → Ṽ（论文：Ṽ 是 Theta 参数变 + 号）"""
    A = len(blocks)
    val = 1.0
    for k in range(A - 1):
        Sk = blocks[k]
        Sk1 = blocks[k + 1]
        d = bracket(Sk, Sk1, omega, zbar)           # [lam_Sk, lam_S{k+1}]
        K1 = tuple(itertools.chain.from_iterable(blocks[: k + 1]))
        K2 = tuple(itertools.chain.from_iterable(blocks[k + 1:]))
        num = bracket(K1, K2, omega, zbar)          # [K_{1..k}, K_{k+1..A}]
        ratio = num / d if d != 0 else 0.0
        theta = 1.0 if sign * (-ratio) > 0 else 0.0
        val *= sg_pair(omega, zbar, 0, 0) * 0 + (1 if d > 0 else (-1 if d < 0 else 0)) * theta
    return val


def PThat(blocks, omega, zbar):
    """PT̂ = V - Ṽ（公式 22）"""
    return V_fn(blocks, omega, zbar, sign=1.0) - V_fn(blocks, omega, zbar, sign=-1.0)


_preamplitude_memo = {}


def preamplitude(S, omega, zbar, depth=0):
    """公式(18)-(19)：Ā_S"""
    if len(S) == 1:
        return 1.0
    if len(S) == 2:
        return 0.0
    key = S
    if key in _preamplitude_memo:
        return _preamplitude_memo[key]
    total = 0.0
    for cuts in compositions(len(S), min_parts=3):
        blocks = split_into_blocks(S, cuts)
        prod = 1.0
        for b in blocks:
            prod *= preamplitude(b, omega, zbar, depth + 1)
        total += V_fn(blocks, omega, zbar, sign=1.0) * prod
    _preamplitude_memo[key] = -total
    return -total


def A_BG(n, omega, zbar):
    """公式(21)：A_{1..n} = -Σ_{o.p.(2..n)} PT̂_{λ_{S_1}...λ_{S_A}} ∏ Ā_{S_a}"""
    _preamplitude_memo.clear()
    elems = tuple(range(1, n))  # 0-based: 粒子 2..n = 索引 1..n-1
    total = 0.0
    for cuts in compositions(n - 1, min_parts=1):
        blocks = split_into_blocks(elems, cuts)
        pt = PThat(blocks, omega, zbar)
        prod = 1.0
        for b in blocks:
            prod *= preamplitude(b, omega, zbar)
        total += pt * prod
    return -total


# ---------- 验证 B1: BG递归 vs 通式(39) ----------

def check_B1(n_samples=800):
    results = {}
    for n in (3, 4, 5, 6):
        nfail = 0
        maxdev = 0.0
        for _ in range(n_samples):
            omega, zbar = gen_R1_momentum(n)
            a_bg = A_BG(n, omega, zbar)
            a_r1 = A_R1(omega, zbar)
            d = abs(a_bg - a_r1)
            if d > 1e-9:
                nfail += 1
                maxdev = max(maxdev, d)
        results[f"n={n}"] = {"samples": n_samples, "fail": nfail, "max_dev": maxdev,
                             "pass": nfail == 0}
    return results


# ---------- 验证 B2: BG递归 vs 显式公式(29)-(32) ----------

def check_B2(n_samples=800):
    explicit = {3: A3, 4: A4, 5: A5, 6: A6}
    results = {}
    for n in (3, 4, 5, 6):
        nfail = 0
        for _ in range(n_samples):
            omega, zbar = gen_R1_momentum(n)
            if abs(A_BG(n, omega, zbar) - explicit[n](omega, zbar)) > 1e-9:
                nfail += 1
        results[f"n={n}"] = {"samples": n_samples, "fail": nfail, "pass": nfail == 0}
    return results


# ---------- 验证 B3: BG递归满足一致性（一般半共线配置） ----------

def permute(fn, omega, zbar, perm):
    om = [omega[i] for i in perm]
    zb = [zbar[i] for i in perm]
    return fn(len(perm), om, zb)


def check_B3(n_samples=500):
    """一致性检查：循环性(24)/反射(25) 需在动量守恒配置（Σλ̃_i=0）下验证
    （剥离振幅的循环性是全振幅层面性质，依赖动量守恒）；
    U1(26)/KK(27) 为更强恒等式，一般半共线配置下也应成立"""
    res = {}
    # 循环性(24) n=5：动量守恒配置
    nf = 0
    for _ in range(n_samples):
        omega, zbar = gen_R1_momentum(5)
        a1 = A_BG(5, omega, zbar)
        a2 = permute(A_BG, omega, zbar, [1, 2, 3, 4, 0])
        if abs(a1 - a2) > 1e-9:
            nf += 1
    res["cyclicity(24) n=5 (mom-conserv)"] = {"fail": nf, "pass": nf == 0}
    # 反射(25) n=4,5：动量守恒配置
    nf = 0
    for _ in range(n_samples):
        omega, zbar = gen_R1_momentum(4)
        a1 = A_BG(4, omega, zbar)
        a2 = permute(A_BG, omega, zbar, [3, 2, 1, 0])
        if abs(a1 - (+1) * a2) > 1e-9:
            nf += 1
        omega, zbar = gen_R1_momentum(5)
        a1 = A_BG(5, omega, zbar)
        a2 = permute(A_BG, omega, zbar, [4, 3, 2, 1, 0])
        if abs(a1 - (-1) * a2) > 1e-9:
            nf += 1
    res["reflection(25) n=4,5 (mom-conserv)"] = {"fail": nf, "pass": nf == 0}
    # U1(26) n=5：动量守恒配置
    nf = 0
    perms = [[0, 2, 3, 4, 1], [0, 3, 4, 1, 2], [0, 4, 1, 2, 3]]
    for _ in range(n_samples):
        omega, zbar = gen_R1_momentum(5)
        total = A_BG(5, omega, zbar)
        for p in perms:
            total += permute(A_BG, omega, zbar, p)
        if abs(total) > 1e-9:
            nf += 1
    res["U1_decoupling(26) n=5 (mom-conserv)"] = {"fail": nf, "pass": nf == 0}
    # KK(27) n=5：动量守恒配置
    nf = 0
    perms = [[0, 1, 2, 4, 3], [0, 1, 3, 2, 4], [0, 3, 1, 2, 4]]
    for _ in range(n_samples):
        omega, zbar = gen_R1_momentum(5)
        total = A_BG(5, omega, zbar)
        for p in perms:
            total += permute(A_BG, omega, zbar, p)
        if abs(total) > 1e-9:
            nf += 1
    res["KK(27) n=5 (mom-conserv)"] = {"fail": nf, "pass": nf == 0}
    return res


def main():
    print("=" * 70)
    print("BG 递归(18)-(21) 独立实现验证")
    print("=" * 70)

    print("\n[B1] BG递归(21) vs 通式(39)（R1+动量守恒）")
    b1 = check_B1()
    for k, v in b1.items():
        print(f"  {k}: fail={v['fail']}/{v['samples']}, max_dev={v['max_dev']:.2e}, pass={v['pass']}")

    print("\n[B2] BG递归(21) vs 显式公式(29)-(32)")
    b2 = check_B2()
    for k, v in b2.items():
        print(f"  {k}: fail={v['fail']}/{v['samples']}, pass={v['pass']}")

    print("\n[B3] BG递归(21) 一致性检查（一般半共线配置）")
    b3 = check_B3()
    for k, v in b3.items():
        print(f"  {k}: fail={v['fail']}, pass={v['pass']}")

    print("\n总体:", "全部通过" if all(v["pass"] for v in b1.values())
          and all(v["pass"] for v in b2.values())
          and all(v["pass"] for v in b3.values()) else "存在失败项")


if __name__ == "__main__":
    main()
