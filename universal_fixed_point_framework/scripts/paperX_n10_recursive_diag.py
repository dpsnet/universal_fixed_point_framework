# -*- coding: utf-8 -*-
"""M3 递归诊断：57 因子基座下 seed 77 冲突模式的区分因子
- 独立复核（seed 77）捕获冲突模式（57 维投影 + 值）
- 符号保持分支采样（zero/nz）+ 165 全集括号 flip 统计 → 缺失因子
"""
import json, os, random, sys, time
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG, bracket
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors
import itertools


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

    def pattern_on(omega, zbar, ix=idx):
        return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in ix)

    # 主表（57 维）
    rng = random.Random(131)
    pat_a = defaultdict(set)
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat_a[pattern_on(omega, zbar)].add(round(A_BG(10, omega, zbar), 6))
    print(f"主表 {len(pat_a)} 模式", flush=True)

    # seed 77 捕获冲突
    rng = random.Random(77)
    conflicts = []
    for k in range(15000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar)
        v = round(A_BG(10, omega, zbar), 6)
        if pat in pat_a and v not in pat_a[pat]:
            conflicts.append({"sample": k, "main": list(pat_a[pat])[0], "indep": v,
                              "omega": omega, "zbar": zbar, "pat": pat})
    print(f"seed 77 冲突 {len(conflicts)}", flush=True)

    # 对每个冲突：分支采样 + flip 统计
    elems = tuple(range(1, 10))
    k12s = set()
    for cuts in compositions(9, min_parts=1):
        blocks = split_into_blocks(elems, cuts)
        for k in range(len(blocks) - 1):
            K1 = tuple(itertools.chain.from_iterable(blocks[:k + 1]))
            K2 = tuple(itertools.chain.from_iterable(blocks[k + 1:]))
            k12s.add((K1, K2))
    k12s = sorted(k12s, key=lambda p: (len(p[0]), p[0], p[1]))
    print(f"K1/K2 候选 {len(k12s)}", flush=True)

    out = []
    for ci, c in enumerate(conflicts):
        omega0, zbar0, pat0 = list(c["omega"]), list(c["zbar"]), c["pat"]
        rng = random.Random(9000 + ci)
        bins = defaultdict(list)
        n_hit = {"zero": 0, "nz": 0}
        target_zero = "zero" if abs(c["main"]) < 1e-9 else "nz"
        target_nz = "nz" if abs(c["main"]) < 1e-9 else "zero"
        tries = 0
        while (n_hit["zero"] < 150 or n_hit["nz"] < 150) and tries < 3000000:
            tries += 1
            w = [omega0[0] * (1.0 + rng.uniform(-0.1, 0.1))]
            for a in range(1, 9):
                w.append(omega0[a] * (1.0 + rng.uniform(-0.1, 0.1)))
            w.append(-sum(w[:9]))
            if w[9] >= 0:
                continue
            z = [zbar0[i] + rng.uniform(-0.3, 0.3) for i in range(9)]
            s = sum(w[:9])
            z.append(sum(w[i] * z[i] for i in range(9)) / s)
            if pattern_on(w, z) != pat0:
                continue
            v = round(A_BG(10, w, z), 6)
            key = "zero" if abs(v) < 1e-9 else "nz"
            if n_hit[key] < 200:
                bins[key].append((w, z))
                n_hit[key] += 1
        print(f"冲突 {ci}: zero={n_hit['zero']} nz={n_hit['nz']} tries={tries}", flush=True)
        # flip 统计
        flips = Counter()
        for w, z in bins["zero"]:
            sigz = tuple(1 if bracket(a, b, w, z) > 1e-9 else (-1 if bracket(a, b, w, z) < -1e-9 else 0) for a, b in k12s)
            for w2, z2 in bins["nz"]:
                signz = tuple(1 if bracket(a, b, w2, z2) > 1e-9 else (-1 if bracket(a, b, w2, z2) < -1e-9 else 0) for a, b in k12s)
                for j in range(len(k12s)):
                    if signz[j] != sigz[j]:
                        flips[j] += 1
        top = flips.most_common(8)
        print(f"  Top: {[( (','.join(str(x+1) for x in k12s[j][0]), ','.join(str(x+1) for x in k12s[j][1])), f) for j, f in top]}", flush=True)
        out.append({"main": c["main"], "indep": c["indep"],
                    "top": [{"K1": [int(x) for x in k12s[j][0]], "K2": [int(x) for x in k12s[j][1]],
                             "flip": f, "name": "s" + "".join(str(x + 1) for x in k12s[j][0]) + "_" + "".join(str(x + 1) for x in k12s[j][1])} for j, f in top]})
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_recursive_diag.json"), "w", encoding="utf-8") as f:
        json.dump({"base": base_names, "conflicts": out}, f, ensure_ascii=False, indent=1)
    print("DONE")
