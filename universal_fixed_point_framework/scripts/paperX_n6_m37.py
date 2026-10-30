# -*- coding: utf-8 -*-
"""M37：n=6 判据解析化——A6 显式公式 → Φ 的解析形式
- A6 公式 32 项、20 个 sg 因子——仅 s61（[λ6,λ1] 环向单对）跨区间（不在 35 相邻区间）
- M28 实证 35 相邻区间 0 冲突 → s61 被 35 隐含决定——解析机制 = 动量守恒展开
- 目标：s61 动量展开恒等式（数值验证）+ s61 符号在 35 模式内单值（量化）+ F6 解析判据结构
"""
import os, sys, random, time, json
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg, sg_pair, sg_block, A6


def adj_factors_names(n):
    """35 相邻区间因子名（n=6）：[i..k]|[k+1..j]"""
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                A = "".join(str(x + 1) for x in range(i, k + 1))
                B = "".join(str(x + 1) for x in range(k + 1, j + 1))
                names.append("s%s_%s" % (A, B))
    return names


def adj_factors_vals(omega, zbar):
    """35 相邻区间因子值（n=6）"""
    n = len(omega)
    w = n
    P = [[0.0] * w for _ in range(w)]
    for i in range(w):
        wi = omega[i]
        zi = zbar[i]
        for j in range(i + 1, w):
            v = wi * omega[j] * (zi - zbar[j])
            P[i][j] = v
            P[j][i] = -v
    vals = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                A = tuple(range(i, k + 1))
                B = tuple(range(k + 1, j + 1))
                v = 0.0
                for x in A:
                    row = P[x]
                    for y in B:
                        v += row[y]
                vals.append(v)  # 数值（非符号）——供恒等式验证
    return vals, P


def gen(n, rng, r1=True, momentum=True):
    """部分共线采样（与既有脚本一致）——此处用 A6 显式（无需 BG）"""
    from paperX_degenerate_family_scan import gen_partial_collinear
    return gen_partial_collinear(n, 0, rng=rng, r1=r1, momentum=momentum)


if __name__ == "__main__":
    n = 6
    NAMES35 = adj_factors_names(n)
    print(f"35 相邻区间因子（n=6）：{len(NAMES35)}")
    # A6 公式 20 因子检查哪些不在 35
    used = ["s1_23", "s12_3", "s123_4", "s5_6", "s2_3", "s1_234", "s12_34", "s3_4",
            "s2_34", "s23_4", "s1_2", "s345_6", "s45_6", "s4_5", "s3_45", "s34_5",
            "s234_5", "s6_1", "s2_345", "s23_45"]
    missing = [u for u in used if u not in NAMES35]
    print(f"A6 用 20 因子中不在 35 的（跨区间）：{missing}")

    N = 200000
    rng = random.Random(20261006)
    t0 = time.time()
    samples = []
    for _ in range(N):
        omega, zbar, pairs = gen(n, rng)
        vals35, P = adj_factors_vals(omega, zbar)
        s35 = tuple(sg(v) for v in vals35)
        a6 = A6(omega, zbar)
        s61 = sg(P[5][0])
        s61v = P[5][0]
        samples.append((s35, s61, s61v, a6, omega, zbar))
    print(f"采样 {N}（{time.time()-t0:.0f}s）")

    # 1) 35 模式 → A6 符号冲突（复现 M28）
    pat35 = defaultdict(list)
    for s35, s61, s61v, a6, _, _ in samples:
        pat35[s35].append(a6)
    c35 = sum(1 for vals in pat35.values() if len({sg(v) for v in vals}) > 1)
    print(f"[1] 35 相邻区间 → A6 符号：冲突 {c35}/{N}（率 {c35/N:.3e}）")

    # 2) s61 在 35 模式内分裂
    pat61 = defaultdict(set)
    for s35, s61, s61v, a6, _, _ in samples:
        pat61[s35].add(s61)
    split61 = sum(1 for v in pat61.values() if len(v) > 1)
    print(f"[2] s61 在 35 模式内分裂：{split61}/{len(pat61)} 模式")

    # 3) 动量双守恒括号恒等式：P[k][0] = -Σ_{j≠0,k} P[k][j]（任何 k 可作锚）
    #    推导：Σ_{全} ω=0 + Σ_{全} ωz=0 → ω_k[z_k Σ_{j≠k}ω_j - Σ_{j≠k}ω_j z_j] = ω_k[-ω_k z_k + ω_k z_k] = 0
    bad = 0
    total = 0
    for s35, s61, s61v, a6, omega, zbar in samples[:10000]:
        for k in range(n):
            lhs = 0.0
            for j in range(n):
                if j != k:
                    lhs += omega[k] * omega[j] * (zbar[k] - zbar[j])
            if abs(lhs) > 1e-9:
                bad += 1
            total += 1
    print(f"[3] 双守恒括号恒等式（Σ_{{j≠k}} s_{{kj}} = 0，任何 k）：{bad}/{total} 偏差")

    # 4) 跨区间单对展开律：s61 = -Σ_{j=2..5} s_{6j}（j=1..4 0-based——[3] k=5 特例）
    bad4 = 0
    for s35, s61, s61v, a6, omega, zbar in samples[:10000]:
        rhs = 0.0
        for j in range(1, n - 1):  # 0-based 1..4
            rhs += omega[5] * omega[j] * (zbar[5] - zbar[j])
        if abs(s61v + rhs) > 1e-9:
            bad4 += 1
    print(f"[4] s61 = -(s62+s63+s64+s65) 展开律：{bad4}/10000 偏差")

    # 5) 级联展开：s61 = -Σ_{j=1..4} Σ_{i≠5,j} s_{ji}（[3] 恒等式 P[5][j] = Σ_{i≠5,j} P[j][i]）
    bad5 = 0
    for s35, s61, s61v, a6, omega, zbar in samples[:10000]:
        rhs = 0.0
        for j in range(1, n - 1):
            for i in range(n):
                if i != 5 and i != j:
                    rhs += omega[j] * omega[i] * (zbar[j] - zbar[i])
        if abs(s61v + rhs) > 1e-9:
            bad5 += 1
    print(f"[5] 级联展开（s61 + Σ Σ s_ji = 0）：{bad5}/10000 偏差")

    # 6) F6 候选：s61 符号 = -sg(级联展开和) —— 若数值恒等则符号恒等（除 0）
    agree = 0
    for s35, s61, s61v, a6, omega, zbar in samples[:100000]:
        rhs = 0.0
        for j in range(1, n - 1):
            for i in range(n):
                if i != 5 and i != j:
                    rhs += omega[j] * omega[i] * (zbar[j] - zbar[i])
        if sg(s61v) == sg(rhs) or (s61v == 0 and rhs == 0):
            agree += 1
    print(f"[6] s61 符号 vs (-1)×级联展开和符号：{agree}/100000")

    out = {"n": n, "c35": c35, "N": N, "split61": split61,
           "id_s61_neg_sum": bad == 0, "id_sk1_neg_sum": bad4 == 0,
           "id_s61_pair_sum": bad5 == 0, "sign_agree": agree}
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_m37_analytic.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n6_m37_analytic.json")
