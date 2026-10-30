# -*- coding: utf-8 -*-
"""M36：n=10 谱维数对照（跨 n 标度——1-锚定结构验证）
- 缓存 cache_n10_3x80000.pkl（3 seed × 80000 = 240000）
- 全因子 → 正确极小化（固定序 + 随机序）→ n=10 谱维数 + 结构
- 与 n=11 的 44 对比——维数标度律
"""
import os, json, pickle, sys, random, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len({sg(v) for v in vals}) > 1)


def group(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return pat


def minimize(samples, start_idx, seed):
    """正确极小化：逐因子立即删 + 每步验证 0 冲突——到不动点"""
    random.seed(seed)
    cur = list(start_idx)
    random.shuffle(cur)
    while True:
        removed_any = False
        for i in list(cur):
            trial = [x for x in cur if x != i]
            if conflict_count(group(samples, trial)) == 0:
                cur = trial
                removed_any = True
        if not removed_any:
            break
    return cur


if __name__ == "__main__":
    n = 10
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    print(f"n={n} 全因子数：{len(factors)}")

    with open(os.path.join(SCRIPT_DIR, "cache_n10_3x80000.pkl"), "rb") as f:
        d = pickle.load(f)
    all_samples = []
    for sd in d:
        all_samples.extend(d[sd])
    print(f"样本 {len(all_samples)}，facs 长度 {len(all_samples[0][0])}")

    # 基线：全因子 0 冲突
    full = list(range(len(factors)))
    c0 = conflict_count(group(all_samples, full))
    print(f"全因子基线冲突：{c0}")

    t0 = time.time()
    cur = minimize(all_samples, full, 20261006)
    print(f"轮 1（随机序）终局：{len(cur)}（{time.time()-t0:.0f}s）——冲突 {conflict_count(group(all_samples, cur))}")
    # 再跑一轮不同随机序（换路径确认）
    t0 = time.time()
    cur2 = minimize(all_samples, full, 20261007)
    print(f"轮 2（另一随机序）终局：{len(cur2)}（{time.time()-t0:.0f}s）——冲突 {conflict_count(group(all_samples, cur2))}")

    best = cur if len(cur) <= len(cur2) else cur2
    names = [NAMES[i] for i in sorted(best)]
    c_f = conflict_count(group(all_samples, best))
    print(f"\nn=10 谱维数：{len(best)}（冲突 {c_f} 实测）")
    print("  名单:", names)
    # 1-锚定检查：是否含粒子 1 前缀块（s1_23, s1_234, ..., s1_2..9）
    anchors = [nm for nm in names if nm.startswith("s1_")]
    print(f"  粒子 1 前缀块（1-锚）：{len(anchors)} 个 -> {anchors}")

    out = {"n": n, "full": len(factors), "spectral_dim": len(best), "conflict": c_f,
           "round1_size": len(cur), "round2_size": len(cur2), "final_names": names,
           "anchors": anchors}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_m36_spectral.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n10_m36_spectral.json")
