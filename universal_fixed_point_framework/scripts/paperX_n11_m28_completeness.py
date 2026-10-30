# -*- coding: utf-8 -*-
"""M28 核心：判据映射完备性（缓存复用——无需重采样）
- 缓存 cache_n11_3x80000.pkl：240000 样本（220 因子符号 + A 值）
- 对照：50 贪心基座模式 vs 220 全因子模式 → A 符号唯一性（合并口径）
- 期望：50 冲突 ~8（复现 M18）；220 冲突 0（若判据映射完备性定理成立）
"""
import os, json, pickle, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name

CACHE = os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl")


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    factors = adj_partition_factors(11)
    NAMES = [factor_name(a, b) for a, b in factors]
    print(f"220 因子命名：{len(NAMES)} 个")

    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [NAMES.index(x) for x in basis50]
    print(f"50 基座：{len(idx50)} 因子")

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    pat50 = defaultdict(list)
    pat220 = defaultdict(list)
    tot = 0
    for sd, data in datas.items():
        for facs, a in data:
            k50 = tuple(facs[i] for i in idx50)
            pat50[k50].append(a)
            pat220[facs].append(a)
            tot += 1
    print(f"总样本：{tot}")

    def conflict(pats):
        c = 0
        t = 0
        for p, vals in pats.items():
            syms = {sg(v) for v in vals}
            t += len(vals)
            if len(syms) > 1:
                c += 1
        return c, t

    c50, t50 = conflict(pat50)
    c220, t220 = conflict(pat220)
    print(f"\n50 基座：冲突模式 {c50} / 样本 {t50}（率 {c50/t50:.3e}）")
    print(f"220 全因子：冲突模式 {c220} / 样本 {t220}（率 {c220/t220:.3e}）")

    # 220 冲突样本明细（若存在）
    if c220 > 0:
        print("\n220 冲突模式（前 5 个）:")
        shown = 0
        for p, vals in pat220.items():
            if len({sg(v) for v in vals}) > 1:
                print("  样本数", len(vals), "A 符号", sorted({sg(v) for v in vals}))
                shown += 1
                if shown >= 5:
                    break

    out = {"c50": c50, "t50": t50, "c220": c220, "t220": t220,
           "n_patterns_50": len(pat50), "n_patterns_220": len(pat220)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m28_completeness.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m28_completeness.json")
