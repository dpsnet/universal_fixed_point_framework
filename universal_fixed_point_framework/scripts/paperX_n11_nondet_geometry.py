# -*- coding: utf-8 -*-
"""n=11 非决定模式几何画像（解析完全闭合第一步）
- 从 cache_n11_3x80000.pkl 提取 46 基座非决定样本对
- 分析每个非决定样本的几何特征：零块结构、粒子分布、补因子长块区分能力
"""
import os, pickle, json, sys
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


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    # 从 json 精确取 46/50 构成
    j46 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill45.json"), encoding="utf-8"))
    basis46 = list(j46["final_set"])
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    extra50 = list(j50.get("added", []))
    print(f"46 基座 {len(basis46)} 因子, 50 基座 {len(basis50)} 因子, 补入 {len(extra50)}")

    idx46 = [NAMES.index(x) for x in basis46 if x in NAMES]
    idx50 = [NAMES.index(x) for x in basis50 if x in NAMES]
    print(f"索引: 46={len(idx46)}, 50={len(idx50)}")

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    report = {}
    for sd, data in datas.items():
        # 46 基座非决定模式
        pat_a = defaultdict(set)
        for full, a in data:
            pat = tuple(full[i] for i in idx46)
            pat_a[pat].add(a)
        nd_pats = [(p, sorted(v)) for p, v in pat_a.items() if len(v) > 1]
        # 50 基座是否区分
        pat50_a = defaultdict(set)
        for full, a in data:
            pat = tuple(full[i] for i in idx50)
            pat50_a[pat].add(a)
        nd50 = sum(1 for v in pat50_a.values() if len(v) > 1)

        # 对每个非决定模式：取代表样本对 (mode, A符号对)，分析几何
        geo = []
        for p, avals in nd_pats[:3]:  # 每 seed 最多取 3 个模式
            # 找该模式的两个样本（A 符号不同的两个具体样本）
            samples = []
            for full, a in data:
                if tuple(full[i] for i in idx46) == p:
                    samples.append((full, a))
                    if len(set(x[1] for x in samples)) >= 2 and len(samples) >= 2:
                        break
            if len(samples) < 2:
                continue
            # 第一个样本的几何：零块清单（块和接近 0 的因子）
            full0, a0 = samples[0]
            zero_blocks = [NAMES[k] for k, v in enumerate(full0) if abs(v) < 1e-9]
            # 补因子在区分上的作用：46 模式 p 的两样本在 50 补因子上的值
            diff_extra = []
            for x in extra50:
                if x in NAMES:
                    k = NAMES.index(x)
                    v0 = full0[k]
                    geo_info = {"pat_len": len(p), "A_vals": avals[:3],
                                "n_zero_blocks": len(zero_blocks),
                                "zero_blocks_sample": zero_blocks[:8],
                                "extra50_values": {x: round(v0, 6)}}
                    diff_extra.append(x)
            geo.append(geo_info)
        report[sd] = {"nd_pats_46": len(nd_pats), "nd_50": nd50,
                      "geo_samples": geo,
                      "extra50": extra50}
        print(f"seed {sd}: 46 基座非决定模式 {len(nd_pats)} / 50 基座 {nd50}", flush=True)

    with open(os.path.join(SCRIPT_DIR, "paperX_n11_nondet_geometry.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print("DONE -> paperX_n11_nondet_geometry.json")
