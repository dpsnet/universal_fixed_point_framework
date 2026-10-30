# -*- coding: utf-8 -*-
"""M3 验证：0 分支 ↔ 跨块合并括号 bracket(K1,K2) 符号翻转
- 对 instance 1/2 重采样（r=0.1 符号保持扰动），分箱：0 分支 vs ±1 分支
- 计算每个样本的全部跨块合并括号 bracket(K1,K2)（K1=前 k 块并集，遍历所有 composition）
- 找"分支间符号/近零状态不同的括号" → 候选连续量 Q（模式外因子）
"""
import json, os, random, sys, time
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG, V_fn, preamplitude, PThat, bracket
from paperX_n10_criterion import adj_partition_factors
import itertools


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def compositions(n, min_parts=1):
    # 复刻 paperX_single_minus_bg_recursion 的 composition（有序分割）
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
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_conflict_vectors.json"), encoding="utf-8") as f:
        cv = json.load(f)
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    base_names = cv["base"]
    idx = [NAMES.index(x) for x in base_names]

    def pattern_on(omega, zbar):
        return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)

    # 目标实例：1（−1 分支 + 0 分支）、2（+1 分支 + 0 分支）
    for ci in (1, 2):
        inst = cv["detail"][ci]
        omega0 = list(inst["omega"])
        zbar0 = list(inst["zbar"])
        pat0 = pattern_on(omega0, zbar0)
        rng = random.Random(5000 + ci)
        bins = defaultdict(list)
        r = 0.1
        n_hit = {"zero": 0, "nz": 0}
        # 采样直到 0 分支 200 个、非零分支 200 个
        while n_hit["zero"] < 200 or n_hit["nz"] < 200:
            w = [omega0[0] * (1.0 + rng.uniform(-r, r))]
            for a in range(1, 9):
                w.append(omega0[a] * (1.0 + rng.uniform(-r, r)))
            w.append(-sum(w[:9]))
            if w[9] >= 0:
                continue
            z = [zbar0[i] + rng.uniform(-3.0 * r, 3.0 * r) for i in range(9)]
            s = sum(w[:9])
            z.append(sum(w[i] * z[i] for i in range(9)) / s)
            if pattern_on(w, z) != pat0:
                continue
            v = round(A_BG(10, w, z), 6)
            key = "zero" if abs(v) < 1e-9 else "nz"
            if n_hit[key] < 300:
                bins[key].append((w, z))
                n_hit[key] += 1
        print(f"instance {ci}: zero={n_hit['zero']} nz={n_hit['nz']}", flush=True)

        # 遍历全部 composition，收集 (K1,K2) 对
        elems = tuple(range(1, 10))  # 粒子 2..10 (0-based 1..9)
        k12s = set()
        for cuts in compositions(9, min_parts=1):
            blocks = split_into_blocks(elems, cuts)
            for k in range(len(blocks) - 1):
                K1 = tuple(itertools.chain.from_iterable(blocks[:k + 1]))
                K2 = tuple(itertools.chain.from_iterable(blocks[k + 1:]))
                k12s.add((K1, K2))
        k12s = sorted(k12s, key=lambda p: (len(p[0]), p[0], p[1]))
        print(f"K1/K2 对总数 {len(k12s)}", flush=True)

        # 每样本算全部 bracket(K1,K2)，按分支统计符号签名
        zsig = Counter()
        nzsig = Counter()
        for w, z in bins["zero"]:
            zsig[tuple(1 if bracket(a, b, w, z) > 1e-9 else (-1 if bracket(a, b, w, z) < -1e-9 else 0) for a, b in k12s)] += 1
        for w, z in bins["nz"]:
            nzsig[tuple(1 if bracket(a, b, w, z) > 1e-9 else (-1 if bracket(a, b, w, z) < -1e-9 else 0) for a, b in k12s)] += 1

        # 找区分量：某 K1/K2 对在 zero 与 nz 分支符号/零状态不同的频率
        flips = Counter()
        for sig, cnt in zsig.items():
            for j, v in enumerate(sig):
                for sig2, cnt2 in nzsig.items():
                    if sig2[j] != v:
                        flips[j] += cnt * cnt2
        top = flips.most_common(10)
        print(f"instance {ci}: 区分括号 Top10", flush=True)
        for j, f in top:
            K1, K2 = k12s[j]
            print(f"  ({','.join(str(x+1) for x in K1)})|({','.join(str(x+1) for x in K2)}) flip={f}", flush=True)
        # 保存 top 候选
        with open(os.path.join(SCRIPT_DIR, f"paperX_n10_branch_flips_i{ci}.json"), "w", encoding="utf-8") as f:
            json.dump({"instance": ci, "top": [{"K1": [int(x) for x in k12s[j][0]],
                                                "K2": [int(x) for x in k12s[j][1]], "flip": fl} for j, fl in top[:20]],
                       "zero_sigs": len(zsig), "nz_sigs": len(nzsig)}, f, ensure_ascii=False, indent=1)
    print("DONE")
