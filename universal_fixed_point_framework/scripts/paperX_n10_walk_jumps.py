# -*- coding: utf-8 -*-
"""Phase 73 闭合推进：随机游走 + 同模式跳变检测
- 种子：seed 77 冲突样本（conflict_vectors instance 0/1 几何，57 维下仍冲突）
- 大步随机游走（r=0.3，动量守恒），不 reject：记录 (57 基座投影, A_BG, 120 d-括号)
- 同模式跳变：相邻步 bg 变且基座投影不变 → 检查该段 d-括号变号集合 → 区分者
"""
import json, os, random, sys, time
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG, bracket
from paperX_n10_criterion import adj_partition_factors


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def compositions(n, min_parts=1):
    def rec(rem, parts):
        if rem == 0:
            if len(parts) >= min_parts:
                yield tuple(parts)
            return
        for k in range(1, rem + 1):
            yield from rec(rem - k, parts + [k])
    yield from rec(n, [])


def split_into_blocks(elems, cuts):
    blocks, i = [], 0
    for c in cuts:
        blocks.append(tuple(elems[i:i + c]))
        i += c
    return blocks


if __name__ == "__main__":
    # 57 因子基座
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_base.json"), encoding="utf-8") as f:
        fb = json.load(f)
    base_names = list(dict.fromkeys(fb["base"] + ["s23_45678910", "s234_5678910", "s2345_678910",
                                                  "s23456_78910", "s234567_8910", "s2345678_910",
                                                  "s23456789_10"]))
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in base_names]

    def pattern_on(omega, zbar):
        return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)

    # 冲突种子：conflict_vectors instance 0/1（seed 77）
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_conflict_vectors.json"), encoding="utf-8") as f:
        cv = json.load(f)
    seeds = [cv["detail"][0], cv["detail"][1]]  # seed 77 sample 597/13207

    # d-括号全集（0-based 相邻块对）
    elems = tuple(range(1, 10))
    dpairs = set()
    for cuts in compositions(9, min_parts=1):
        blocks = split_into_blocks(elems, cuts)
        for k in range(len(blocks) - 1):
            dpairs.add((blocks[k], blocks[k + 1]))
    dpairs = sorted(dpairs, key=lambda p: (len(p[0]), p[0], p[1]))
    dnames = ["s" + "".join(str(x + 1) for x in a) + "_" + "".join(str(x + 1) for x in b) for a, b in dpairs]
    print(f"d-括号全集 {len(dpairs)}", flush=True)

    def d_sig(omega, zbar):
        return tuple(1 if bracket(a, b, omega, zbar) > 1e-9 else (-1 if bracket(a, b, omega, zbar) < -1e-9 else 0) for a, b in dpairs)

    out = []
    for si, sd in enumerate(seeds):
        omega0, zbar0 = list(sd["omega"]), list(sd["zbar"])
        pat0 = pattern_on(omega0, zbar0)
        rng = random.Random(70000 + si)
        N = 60000
        prev = None
        same_mode_jumps = []       # 同模式跳变：bg 变、投影不变
        mode_jumps = 0
        t0 = time.time()
        for k in range(N):
            w = [omega0[0] * (1.0 + rng.uniform(-0.3, 0.3))]
            for a in range(1, 9):
                w.append(omega0[a] * (1.0 + rng.uniform(-0.3, 0.3)))
            w.append(-sum(w[:9]))
            if w[9] >= 0:
                continue
            z = [zbar0[i] + rng.uniform(-0.9, 0.9) for i in range(9)]
            s = sum(w[:9])
            z.append(sum(w[i] * z[i] for i in range(9)) / s)
            pat = pattern_on(w, z)
            bg = round(A_BG(10, w, z), 6)
            if prev is not None:
                pbg, ppat, psig = prev
                if abs(bg - pbg) > 1e-9:
                    if pat == ppat:
                        # 同模式跳变：查 d 变号
                        sig = d_sig(w, z)
                        diffs = [j for j in range(len(dpairs)) if sig[j] != psig[j]]
                        same_mode_jumps.append({"bg_from": pbg, "bg_to": bg, "d_flips": diffs})
                    else:
                        mode_jumps += 1
            prev = (bg, pat, d_sig(w, z))
        print(f"种子 {si} ({N} 步 {time.time()-t0:.0f}s): 同模式跳变 {len(same_mode_jumps)} 跨模式跳变 {mode_jumps}", flush=True)
        # 汇总 d 变号
        flipcnt = Counter()
        for jm in same_mode_jumps:
            for j in jm["d_flips"]:
                flipcnt[j] += 1
        top = flipcnt.most_common(12)
        for j, f in top:
            print(f"  {dnames[j]} flip={f} (bg {jm['bg_from']}->{jm['bg_to']})", flush=True)
        out.append({"seed": sd["seed"], "sample": sd["sample"], "main": sd["main"], "indep": sd["indep"],
                    "same_mode_jumps": len(same_mode_jumps),
                    "top": [{"name": dnames[j], "K1": [int(x) for x in dpairs[j][0]],
                             "K2": [int(x) for x in dpairs[j][1]], "flip": f} for j, f in top],
                    "samples": same_mode_jumps[:10]})
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_walk_jumps.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("DONE")
