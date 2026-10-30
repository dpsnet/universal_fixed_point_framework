# -*- coding: utf-8 -*-
"""M-P2b：翻转壁中块 = BG 递归分母候选假说检验
- BG 递归分母候选：顶层 (2..n) 分割的相邻块对括号 [Sk,Sk1] + 前缀括号 [K1..k, Kk+1..A]
- 壁因子（P2 的 103 个）∩ 递归分母候选 比例 vs 全体 220 因子 ∩ 候选 比例
- 另：壁因子块长分布 vs 全体因子块长分布
"""
import os, pickle, json, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
CACHE = os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl")


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    n = 11
    name2idx = {}
    fac_len = {}
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                name = "s" + "".join(str(x + 1) for x in a) + "_" + "".join(str(x + 1) for x in b)
                name2idx[name] = len(name2idx)
                fac_len[name] = (len(a), len(b))
    NAMES = list(name2idx)

    # ---- BG 递归分母候选 ----
    # 顶层：A(1, P, n)，P = (2..n)。blocks = P 的分割（compositions）。
    # V_fn 分母：[Sk, Sk1]（相邻块对）+ 前缀括号 [K1..k, Kk+1..A]（num——分母的分子，但它本身是块和）
    # 我们关心"块和因子"的候选集：所有 (2..n) 分割的相邻块对 + 前缀/后缀对
    cand = set()
    elems = list(range(2, n + 1))  # 1-based: 2..n
    # 分割：枚举切点
    cuts_all = []
    for mask in range(1 << (len(elems) - 1)):
        cuts = [i for i in range(len(elems) - 1) if (mask >> i) & 1]
        cuts_all.append(cuts)
    for cuts in cuts_all:
        blocks = []
        prev = 0
        for c in cuts + [len(elems) - 1]:
            blocks.append(elems[prev : c + 1])
            prev = c + 1
        # 相邻块对 [Sk, Sk1]
        for t in range(len(blocks) - 1):
            a, b = blocks[t], blocks[t + 1]
            name = "s" + "".join(str(x) for x in a) + "_" + "".join(str(x) for x in b)
            cand.add(name)
        # 前缀/后缀 [K1..k, Kk+1..A]
        for t in range(len(blocks) - 1):
            k1 = [x for b in blocks[: t + 1] for x in b]
            k2 = [x for b in blocks[t + 1 :] for x in b]
            name = "s" + "".join(str(x) for x in k1) + "_" + "".join(str(x) for x in k2)
            cand.add(name)
    print(f"BG 递归分母候选块（不含 1 号）：{len(cand)}")
    # 含 1 号的变体（子振幅可含 1？——preamplitude 从 (2..n) 子区间，不含 1；但显式公式含）
    # 我们聚焦纯 BG 递归候选（不含 1）——与壁因子对照

    # 壁因子（从 P2 的 json 读）
    p2 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_honeycomb_p2.json"), encoding="utf-8"))
    wall_top15 = dict(p2["wall_top15"])
    # 重新完整计算壁因子集（P2 输出只存了 top15）——重跑翻转对
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [name2idx[x] for x in basis50]
    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    pat_samples = defaultdict(list)
    for sd, data in datas.items():
        for full, a in data:
            pat_samples[tuple(full[i] for i in idx50)].append((sign(a), full, sd))

    wall_factor_cnt = defaultdict(int)
    flip_pairs = []
    for t, samples in pat_samples.items():
        syms = {}
        for a, full, sd in samples:
            syms.setdefault(a, (full, sd))
        zero_full = syms.get(0)
        for a2 in (-1, 1):
            if a2 in syms and zero_full is not None:
                f2, sd2 = syms[a2]
                f0, sd0 = zero_full
                flip_pairs.append((a2, sd2, sd0))
                for k in range(len(NAMES)):
                    if sign(f2[k]) != sign(f0[k]):
                        wall_factor_cnt[NAMES[k]] += 1
    wall_set = set(wall_factor_cnt)
    print(f"翻转对 {len(flip_pairs)} / 壁因子 {len(wall_set)}")

    # 壁因子 ∩ 递归候选
    wall_in_cand = wall_set & cand
    all_in_cand = set(NAMES) & cand
    print(f"\n壁因子 ∩ 递归分母候选：{len(wall_in_cand)}/{len(wall_set)} = {len(wall_in_cand)/len(wall_set):.3f}")
    print(f"全体因子 ∩ 递归分母候选：{len(all_in_cand)}/{len(NAMES)} = {len(all_in_cand)/len(NAMES):.3f}")
    print(f"富集比：{(len(wall_in_cand)/len(wall_set)) / (len(all_in_cand)/len(NAMES)):.2f}x")

    # 块长画像
    def blen(fac):
        la, lb = fac_len[fac]
        return la + lb
    wall_len = defaultdict(int)
    all_len = defaultdict(int)
    for f in wall_set:
        wall_len[blen(f)] += 1
    for f in NAMES:
        all_len[blen(f)] += 1
    print("\n壁因子块长分布 vs 全体因子块长分布：")
    for L in range(2, 12):
        if all_len[L] > 0:
            print(f"  块长 {L}: 壁 {wall_len[L]} ({wall_len[L]/len(wall_set):.3f}) / 全体 {all_len[L]} ({all_len[L]/len(NAMES):.3f})")

    # 壁因子中"符号对因子"与"递归候选"的分层
    pair_factors = set()
    for m in range(2, n):
        pair_factors.add(f"s{m}_{m+1}")
        pair_factors.add(f"s1_{''.join(str(x) for x in range(2, m + 1))}")
    wall_pair = wall_set & pair_factors
    print(f"\n壁因子中：符号对因子 {len(wall_pair)} / 递归候选（非符号对）{len(wall_in_cand - wall_pair)} / 其他 {len(wall_set - wall_in_cand - wall_pair)}")

    out = {"cand_n": len(cand), "wall_n": len(wall_set),
           "wall_in_cand": len(wall_in_cand), "all_in_cand": len(all_in_cand),
           "wall_len": dict(wall_len), "all_len": dict(all_len),
           "wall_pair": len(wall_pair), "wall_cand_nonpair": len(wall_in_cand - wall_pair)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_honeycomb_p2b.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_honeycomb_p2b.json")
