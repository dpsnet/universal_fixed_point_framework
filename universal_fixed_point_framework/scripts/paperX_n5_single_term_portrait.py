# -*- coding: utf-8 -*-
"""
paperX_n5_single_term_portrait.py
困难模式"单非零项"机制的完整画像：
枚举 n=5 的 8 个 BG 分割，对每个分割定位死亡原因：
  - PT̂=0（1 块分割）
  - ∏Ā=0：具体哪块 Ā=0（2 元素块 Ā=0 / 3 元素块 Ā=0）
  - V theta 死：具体哪对相邻块 theta=0（sign=+1 时 −ratio<0 失败）
输出：每分割死亡频率 + 死亡原因模式（是否结构性恒死）
"""
import sys
import itertools
import random
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_bg_recursion import bracket, compositions, split_into_blocks, V_fn, preamplitude, _preamplitude_memo
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}


def analyze(n, omega, zbar):
    """返回每分割的 (PT̂, ∏Ā, 项值, 死亡原因)"""
    _preamplitude_memo.clear()
    elems = tuple(range(1, n))
    out = {}
    for cuts in compositions(n - 1, min_parts=1):
        blocks = split_into_blocks(elems, cuts)
        lbl = "|".join("".join(str(x) for x in b) for b in blocks)
        pt = V_fn(blocks, omega, zbar, 1.0) - V_fn(blocks, omega, zbar, -1.0)
        # 定位 V 的 theta 死亡（sign=+1）
        v_theta_dead = []
        A_ = len(blocks)
        for k in range(A_ - 1):
            Sk = blocks[k]; Sk1 = blocks[k + 1]
            d = bracket(Sk, Sk1, omega, zbar)
            K1 = tuple(itertools.chain.from_iterable(blocks[:k + 1]))
            K2 = tuple(itertools.chain.from_iterable(blocks[k + 1:]))
            num = bracket(K1, K2, omega, zbar)
            ratio = num / d if d != 0 else 0.0
            theta = 1.0 if 1.0 * (-ratio) > 0 else 0.0
            if theta == 0:
                v_theta_dead.append(k)
        # ∏Ā 与死亡块
        prod = 1.0
        dead_blocks = []
        for b in blocks:
            a = preamplitude(b, omega, zbar)
            prod *= a
            if a == 0 and len(b) > 1:
                dead_blocks.append("".join(str(x) for x in b))
        # PT̂ 是否为零（直接判定，不依赖 V 的 theta——Ṽ 可能活）
        if pt == 0:
            cause = "PT̂=0"
        elif prod == 0:
            cause = f"Ā=0({','.join(dead_blocks)})"
        else:
            cause = "活"
        out[lbl] = {"PT": round(pt, 6), "prod": round(prod, 6),
                    "term": round(pt * prod, 6), "cause": cause,
                    "theta_dead": v_theta_dead}
    return out


def bs(A, B, omega, zbar):
    from paperX_single_minus_numerics import sg_block
    A = tuple(a - 1 for a in A); B = tuple(b - 1 for b in B)
    return sg_block(omega, zbar, A, B)


def portrait(n_samples=60000, seed=419, condition_nonzero=True):
    """condition_nonzero=True：只统计 A_BG≠0（E6=E7=c）的困难模式样本"""
    rng = random.Random(seed)
    stat = {}
    cause_detail = {}
    n_hard = 0
    n_nonzero = 0
    for _ in range(n_samples):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in HARD:
            continue
        n_hard += 1
        e6 = bs((1, 2), (1, 2, 3), omega, zbar)
        e7 = bs((1, 2), (1, 2, 3, 4), omega, zbar)
        nonzero = (e6 == e7 and e6 != 0)
        if condition_nonzero and not nonzero:
            continue
        n_nonzero += 1
        r = analyze(5, omega, zbar)
        for lbl, info in r.items():
            if lbl not in stat:
                stat[lbl] = {"dead": 0, "alive": 0}
                cause_detail[lbl] = {}
            if info["cause"] == "活":
                stat[lbl]["alive"] += 1
            else:
                stat[lbl]["dead"] += 1
                cause_detail[lbl][info["cause"]] = cause_detail[lbl].get(info["cause"], 0) + 1
    print(f"困难模式样本数: {n_hard}，计入统计: {n_nonzero}{'(非零条件)' if condition_nonzero else ''}")
    print(f"{'分割':<22}{'死亡':>8}{'存活':>8}   死亡原因分布")
    for lbl in sorted(stat, key=lambda s: (-stat[s]['dead'], s)):
        s = stat[lbl]
        detail = sorted(cause_detail[lbl].items(), key=lambda x: -x[1])
        dstr = ", ".join(f"{k}×{v}" for k, v in detail)
        print(f"{lbl:<22}{s['dead']:>8}{s['alive']:>8}   {dstr}")
    # 每分割死亡是否结构性（100%）
    print("\n结构性恒死（死亡=100% 且原因单一）:")
    for lbl in sorted(stat):
        s = stat[lbl]
        if s["alive"] == 0 and len(cause_detail[lbl]) == 1:
            print(f"  {lbl}: {list(cause_detail[lbl].items())}")
    import json
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_single_term_results.json", "w", encoding="utf-8") as f:
        json.dump({"n_hard": n_hard, "n_counted": n_nonzero,
                   "stat": {k: v for k, v in stat.items()},
                   "causes": cause_detail}, f, ensure_ascii=False, indent=2)
    print("\nDONE -> paperX_n5_single_term_results.json")


if __name__ == "__main__":
    portrait()
