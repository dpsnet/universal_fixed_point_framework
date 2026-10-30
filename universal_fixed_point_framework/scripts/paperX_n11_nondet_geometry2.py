# -*- coding: utf-8 -*-
"""n=11 非决定模式深度画像：符号翻转 vs 长块过零的对应验证
- 全部非决定模式（非前 3）：零块统计、最小块和、A 值对、补因子区分
- 验证假设：A 符号翻转 ⟺ 长块和过零
"""
import os, pickle, json, sys, math
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

CACHE = os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl")


def adj_partition_factors(n):
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                names.append((a, b))
    return names


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    j46 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill45.json"), encoding="utf-8"))
    basis46 = list(j46["final_set"])
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    extra50 = list(j50.get("added", []))
    idx46 = [NAMES.index(x) for x in basis46]
    idx50 = [NAMES.index(x) for x in basis50]
    idx_extra = [NAMES.index(x) for x in extra50]

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    stats = {"total_pats": 0, "sign_flip_pats": 0, "same_sign_pats": 0,
             "has_long_zero": 0, "no_zero_block": 0, "multi_long_zero": 0,
             "flip_has_long_zero": 0}
    per_seed = {}
    for sd, data in datas.items():
        pat_a = defaultdict(list)
        for full, a in data:
            pat = tuple(full[i] for i in idx46)
            pat_a[pat].append((full, a))
        nd = {p: v for p, v in pat_a.items() if len(set(x[1] for x in v)) > 1}
        sd_detail = []
        for p, samples in nd.items():
            # A 值对与符号对
            avals = sorted(set(x[1] for x in samples))
            signs = sorted(set(sign(x[1]) for x in samples))
            is_flip = len(signs) > 1 or 0 in signs and len(signs) == 2
            flip = len(set(sign(x[1]) for x in samples)) > 1
            # 零块（任一样本中 < 1e-9 的块和）
            zero_all = set()
            minabs_all = []
            for full, a in samples:
                zs = [NAMES[k] for k, v in enumerate(full) if abs(v) < 1e-9]
                zero_all.update(zs)
                minabs_all.append(min(abs(v) for v in full))
            long_zero = [z for z in zero_all if len(z.split("_")[0]) + len(z.split("_")[1]) >= 8]
            # 补因子区分
            extra_vals = {}
            for k in idx_extra:
                extra_vals[NAMES[k]] = sorted(set(x[0][k] for x in samples))
            # 过零候选块（样本对之间符号变化的块）
            flip_blocks = []
            s0 = samples[0][0]
            s1 = samples[1][0]
            for k in range(len(factors)):
                if sign(s0[k]) != sign(s1[k]):
                    flip_blocks.append(NAMES[k])
            info = {"A_vals": avals, "signs": signs, "sign_flip": flip,
                    "n_zero_blocks": len(zero_all),
                    "zero_blocks": sorted(zero_all)[:10],
                    "long_zero": sorted(long_zero),
                    "min_abs_across_samples": round(min(minabs_all), 6),
                    "extra50_vals": extra_vals,
                    "flip_blocks_between_samples": flip_blocks[:8],
                    "n_flip_blocks": len(flip_blocks)}
            sd_detail.append(info)
            stats["total_pats"] += 1
            if flip:
                stats["sign_flip_pats"] += 1
                if long_zero:
                    stats["flip_has_long_zero"] += 1
            else:
                stats["same_sign_pats"] += 1
            if long_zero:
                stats["has_long_zero"] += 1
                if len(long_zero) >= 2:
                    stats["multi_long_zero"] += 1
            elif not zero_all:
                stats["no_zero_block"] += 1
        per_seed[sd] = {"n_pats": len(nd), "detail": sd_detail[:5]}
        print(f"seed {sd}: {len(nd)} 非决定模式", flush=True)

    print("\n=== 汇总统计 ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    # 符号翻转模式是否全含长零块
    if stats["sign_flip_pats"] > 0:
        print(f"  符号翻转中长零块占比: {stats['flip_has_long_zero']}/{stats['sign_flip_pats']}")

    with open(os.path.join(SCRIPT_DIR, "paperX_n11_nondet_geometry2.json"), "w", encoding="utf-8") as f:
        json.dump({"stats": stats, "per_seed": per_seed}, f, ensure_ascii=False, indent=1)
    print("DONE -> paperX_n11_nondet_geometry2.json")
