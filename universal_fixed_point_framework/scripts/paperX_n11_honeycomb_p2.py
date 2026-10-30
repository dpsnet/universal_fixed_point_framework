# -*- coding: utf-8 -*-
"""Phase 78 P2：符号翻转的蜂壁结构（P2a-d）
- P2a: 31 非决定模式的翻转对 220 因子 Hamming 距离（蜂壁厚度）
- P2b: 壁因子识别（翻转对变化因子 Top）vs 符号对因子（18 个）对照
- P2c: 跨 seed 8 冲突的壁位置
- P2d: 4 长块补因子（54 因子）切壁作用——31 非决定是否消除
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
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                name = "s" + "".join(str(x + 1) for x in a) + "_" + "".join(str(x + 1) for x in b)
                name2idx[name] = len(name2idx)
    NAMES = list(name2idx)

    # 符号对因子（M22：18 个）
    pair_factors = set()
    for m in range(2, n):
        pair_factors.add(f"s{m}_{m+1}")
        pair_factors.add(f"s1_{''.join(str(x) for x in range(2, m + 1))}")

    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    added4 = list(j50["added"])
    idx50 = [name2idx[x] for x in basis50]
    idx54 = [name2idx[x] for x in basis50 + added4]
    print(f"50 基座 {len(idx50)} / +4 长块 {len(added4)} = {len(idx54)} 因子")
    print(f"符号对因子 {len(pair_factors)} 个：{sorted(pair_factors)}")

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    # 收集样本（seed 记录）
    # pat50 -> [(A, full, sd)]  非决定检测用 50 基座模式
    pat_samples = defaultdict(list)
    for sd, data in datas.items():
        for full, a in data:
            t = tuple(full[i] for i in idx50)
            pat_samples[t].append((sign(a), full, sd))

    # P2a：非决定模式
    nondet = {t: samples for t, samples in pat_samples.items()
              if len({s[0] for s in samples}) > 1}
    print(f"\n[P2a] 50 基座非决定模式数：{len(nondet)}（M14 报 31——3 seed 合并口径）")

    # 翻转对距离：每模式取 A=0 代表 与 A≠0 代表（对每个符号值），算 220 因子 Hamming
    dist_hist = defaultdict(int)
    flip_pairs = []
    wall_factor_cnt = defaultdict(int)
    for t, samples in nondet.items():
        syms = {}
        for a, full, sd in samples:
            syms.setdefault(a, (full, sd))
        zero_full = syms.get(0)
        for a2 in (-1, 1):
            if a2 in syms and zero_full is not None:
                f2, sd2 = syms[a2]
                f0, sd0 = zero_full
                d = sum(1 for k in range(len(NAMES)) if sign(f2[k]) != sign(f0[k]))
                dist_hist[d] += 1
                flip_pairs.append((d, a2, sd2, sd0))
                # 壁因子：变化的因子
                for k in range(len(NAMES)):
                    if sign(f2[k]) != sign(f0[k]):
                        wall_factor_cnt[NAMES[k]] += 1
    print(f"翻转对总数：{len(flip_pairs)}")
    print("Hamming 距离分布：")
    for d in sorted(dist_hist):
        print(f"  d={d}: {dist_hist[d]}")

    # P2b：壁因子 Top 15 vs 符号对因子
    print(f"\n[P2b] 壁因子 Top 15（变化次数）：")
    wall_top = sorted(wall_factor_cnt.items(), key=lambda x: -x[1])[:15]
    for fac, c in wall_top:
        in_pair = "★符号对因子" if fac in pair_factors else ""
        print(f"  {fac}: {c} {in_pair}")
    # 壁因子集合与符号对因子重合率
    wall_set = set(wall_factor_cnt)
    overlap = wall_set & pair_factors
    print(f"壁因子总数 {len(wall_set)} / 与符号对因子重合 {len(overlap)}/{len(pair_factors)}")

    # P2c：跨 seed 8 冲突
    print(f"\n[P2c] 跨 seed 冲突模式（同模式不同 seed 不同符号）：")
    cross = {}
    for t, samples in pat_samples.items():
        seed_sym = {}
        for a, full, sd in samples:
            if a not in seed_sym:
                seed_sym[a] = set()
            seed_sym[a].add(sd)
        # 不同 seed 不同符号
        flags = {}
        for a, sds in seed_sym.items():
            for s in sds:
                flags.setdefault(s, set()).add(a)
        if len({frozenset(v) for v in flags.values()}) > 1:
            cross[t] = flags
    print(f"跨 seed 冲突模式数：{len(cross)}")
    for t, flags in list(cross.items())[:8]:
        p = "".join("-" if v < 0 else ("+" if v > 0 else "0") for v in t)
        print(f"  {p}: seed 符号 { {sd: sorted(v) for sd, v in flags.items()} }")

    # P2d：54 因子（+4 长块）下非决定是否消除
    pat54_samples = defaultdict(list)
    for sd, data in datas.items():
        for full, a in data:
            t = tuple(full[i] for i in idx54)
            pat54_samples[t].append(sign(a))
    nondet54 = {t for t, vals in pat54_samples.items() if len(set(vals)) > 1}
    print(f"\n[P2d] 54 因子（50+4 长块）下非决定模式数：{len(nondet54)}（对照 50 基座 {len(nondet)}）")
    # 50 基座非决定模式在 54 因子下是否仍非决定
    still = 0
    for t in nondet:
        for k54 in nondet54:
            # t 是 50 基座子串——需映射：同一 50 模式 → 54 模式族
            pass
    # 直接：对每个 50 非决定模式 t，找同样本的 54 模式
    rec = {}
    for sd, data in datas.items():
        for full, a in data:
            t50 = tuple(full[i] for i in idx50)
            t54 = tuple(full[i] for i in idx54)
            if t50 in nondet:
                rec.setdefault((t50, t54), set()).add(sign(a))
    nondet54_same = defaultdict(set)
    for (t50, t54), vals in rec.items():
        if len(vals) > 1:
            nondet54_same[t50].add(t54)
    print(f"50 非决定模式中 54 因子下仍非决定：{len(nondet54_same)}/{len(nondet)}（其余被 4 长块切开）")

    out = {"nondet50": len(nondet), "flip_pairs": len(flip_pairs),
           "dist_hist": dict(dist_hist), "wall_top15": [(k, v) for k, v in wall_top],
           "wall_overlap_pair": [len(overlap), len(pair_factors)],
           "cross_seed": len(cross), "nondet54": len(nondet54),
           "nondet50_still54": len(nondet54_same)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_honeycomb_p2.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_honeycomb_p2.json")
