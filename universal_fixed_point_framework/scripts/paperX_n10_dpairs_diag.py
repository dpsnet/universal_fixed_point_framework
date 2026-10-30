# -*- coding: utf-8 -*-
"""M3 终轮：seed 77 冲突的 d-括号（相邻块对）区分者
- 收集全部 composition 的相邻块对 (Sk,Sk1)（d-括号全集，非前缀）
- 对 2 冲突做轻量分支采样（40 zero + 40 nz，r=0.05）→ flip 统计
"""
import json, os, random, sys, time
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG, bracket
from paperX_degenerate_family_scan import gen_partial_collinear
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

    # 冲突种子：seed 77（57 维下重捕获）
    rng = random.Random(131)
    pat_a = defaultdict(set)
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat_a[pattern_on(omega, zbar)].add(round(A_BG(10, omega, zbar), 6))
    rng = random.Random(77)
    seeds = []
    for k in range(15000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar)
        v = round(A_BG(10, omega, zbar), 6)
        if pat in pat_a and v not in pat_a[pat]:
            seeds.append({"omega": omega, "zbar": zbar, "main": list(pat_a[pat])[0], "indep": v})
    print(f"seed 77 冲突 {len(seeds)}", flush=True)

    # d-括号全集：全部 composition 的相邻块对（0-based）
    elems = tuple(range(1, 10))  # 粒子 2..10
    dpairs = set()
    for cuts in compositions(9, min_parts=1):
        blocks = split_into_blocks(elems, cuts)
        for k in range(len(blocks) - 1):
            dpairs.add((blocks[k], blocks[k + 1]))
    dpairs = sorted(dpairs, key=lambda p: (len(p[0]), p[0], p[1]))
    dnames = ["s" + "".join(str(x + 1) for x in a) + "_" + "".join(str(x + 1) for x in b) for a, b in dpairs]
    print(f"d-括号全集 {len(dpairs)}", flush=True)

    out = []
    for ci, sd in enumerate(seeds):
        omega0, zbar0 = list(sd["omega"]), list(sd["zbar"])
        pat0 = pattern_on(omega0, zbar0)
        rng = random.Random(30000 + ci)
        bins = defaultdict(list)
        n_hit = {"zero": 0, "nz": 0}
        tries = 0
        while (n_hit["zero"] < 40 or n_hit["nz"] < 40) and tries < 4000000:
            tries += 1
            w = [omega0[0] * (1.0 + rng.uniform(-0.05, 0.05))]
            for a in range(1, 9):
                w.append(omega0[a] * (1.0 + rng.uniform(-0.05, 0.05)))
            w.append(-sum(w[:9]))
            if w[9] >= 0:
                continue
            z = [zbar0[i] + rng.uniform(-0.15, 0.15) for i in range(9)]
            s = sum(w[:9])
            z.append(sum(w[i] * z[i] for i in range(9)) / s)
            if pattern_on(w, z) != pat0:
                continue
            v = round(A_BG(10, w, z), 6)
            key = "zero" if abs(v) < 1e-9 else "nz"
            if n_hit[key] < 50:
                bins[key].append((w, z))
                n_hit[key] += 1
        print(f"冲突 {ci}: zero={n_hit['zero']} nz={n_hit['nz']} tries={tries}", flush=True)
        flips = Counter()
        for w, z in bins["zero"]:
            sigz = tuple(1 if bracket(a, b, w, z) > 1e-9 else (-1 if bracket(a, b, w, z) < -1e-9 else 0) for a, b in dpairs)
            for w2, z2 in bins["nz"]:
                signz = tuple(1 if bracket(a, b, w2, z2) > 1e-9 else (-1 if bracket(a, b, w2, z2) < -1e-9 else 0) for a, b in dpairs)
                for j in range(len(dpairs)):
                    if signz[j] != sigz[j]:
                        flips[j] += 1
        top = flips.most_common(10)
        for j, f in top:
            print(f"  {dnames[j]} flip={f}", flush=True)
        out.append({"main": sd["main"], "indep": sd["indep"],
                    "top": [{"name": dnames[j], "K1": [int(x) for x in dpairs[j][0]],
                             "K2": [int(x) for x in dpairs[j][1]], "flip": f} for j, f in top]})
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_dpairs_diag.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("DONE")
