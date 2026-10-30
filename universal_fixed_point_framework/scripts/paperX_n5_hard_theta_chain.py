# paperX_n5_hard_theta_chain.py
# Phase 72 阶段4：存活项完整 Θ 链追踪——建立 E6/E7 同号 <-> PT^[2]|[345] * A_345 存活条件的精确对应
import sys
import json
import random

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_bg_recursion import bracket, V_fn, PThat, preamplitude, _preamplitude_memo
from paperX_single_minus_numerics import sg_block
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


def v_chain(blocks, omega, zbar, sign, label):
    """V_fn 的完整 Θ 链：每 k 的 [S_k, S_{k+1}], [K_{1..k}, K_{k+1..A}], ratio, theta"""
    A = len(blocks)
    out = []
    val = 1.0
    for k in range(A - 1):
        Sk = blocks[k]
        Sk1 = blocks[k + 1]
        d = bracket(Sk, Sk1, omega, zbar)
        K1 = tuple(itertools.chain.from_iterable(blocks[: k + 1]))
        K2 = tuple(itertools.chain.from_iterable(blocks[k + 1:]))
        num = bracket(K1, K2, omega, zbar)
        ratio = num / d if d != 0 else None
        theta = 1.0 if (ratio is not None and sign * (-ratio) > 0) else 0.0
        sg_d = 1 if d > 0 else (-1 if d < 0 else 0)
        out.append({
            "k": k, "Sk": Sk, "Sk1": Sk1, "d_sg": sg_d,
            "K1": K1, "K2": K2, "num": num, "ratio": ratio, "theta": theta,
        })
        val *= sg_d * theta
    return val, out


def trace_one(omega, zbar):
    """对单样本打印：[2]|[345] 项 PT^ 与 A_345 的完整 Θ 链"""
    elems = (1, 2, 3, 4)  # 粒子 2,3,4,5
    blocks = ((1,), (2, 3, 4))
    v, vc = v_chain(blocks, omega, zbar, 1.0, "V")
    vt, vtc = v_chain(blocks, omega, zbar, -1.0, "Vt")
    pt = v - vt
    _preamplitude_memo.clear()
    prod = preamplitude((2, 3, 4), omega, zbar)
    # A_345 展开
    b345 = ((2,), (3,), (4,))
    v345, v345c = v_chain(b345, omega, zbar, 1.0, "V345")
    lines = []
    lines.append(f"  blocks=((2), (345)): PT^ = {pt:.3f}, A_345 = {prod:.3f}")
    lines.append(f"    V 链（sign=+1）: theta=1 iff sg(num)=-sg(d):")
    for c in vc:
        lines.append(f"      k={c['k']}: d=sg({c['d_sg']}) num={c['num']:.4f} ratio={c['ratio']:.4f} theta={c['theta']}")
    lines.append(f"    Vt 链（sign=-1）: theta=1 iff sg(num)=+sg(d):")
    for c in vtc:
        lines.append(f"      k={c['k']}: d=sg({c['d_sg']}) num={c['num']:.4f} ratio={c['ratio']:.4f} theta={c['theta']}")
    lines.append(f"    A_345 的 V 链 (blocks=(3),(4),(5)):")
    for c in v345c:
        lines.append(f"      k={c['k']}: d=sg({c['d_sg']}) num={c['num']:.4f} ratio={c['ratio']:.4f} theta={c['theta']}")
    return lines


def main(n_each=6, seed=293):
    rng = random.Random(seed)
    found = {p: {"same": None, "diff": None} for p in HARD}
    while any(v["same"] is None or v["diff"] is None for v in found.values()):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        exts = all_ext_sgs(omega, zbar)
        e6, e7 = exts[6][1], exts[7][1]
        _preamplitude_memo.clear()
        a = None  # 直接用展开项判定（trace 用）
        if found[pat]["same"] is None and e6 == e7:
            found[pat]["same"] = (e6, omega, zbar)
        if found[pat]["diff"] is None and e6 != e7:
            found[pat]["diff"] = (e6, e7, omega, zbar)
    for pat in HARD:
        print(f"pat={pat}:")
        s = found[pat]["same"]
        print(f"  [E6=E7={s[0]}] Θ 链:")
        for l in trace_one(s[1], s[2]):
            print(l)
        d = found[pat]["diff"]
        print(f"  [E6={d[0]},E7={d[1]}] Θ 链:")
        for l in trace_one(d[2], d[3]):
            print(l)


import itertools

if __name__ == "__main__":
    main()
