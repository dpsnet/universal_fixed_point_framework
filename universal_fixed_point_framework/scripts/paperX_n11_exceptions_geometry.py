# -*- coding: utf-8 -*-
"""Phase 78 P1：324 例外的几何定位（50 基座模式聚集度）
- A=0 无符号对相反（324）vs A≠0 无符号对相反（167）
- 例外样本在 50 基座模式空间的分布：模式数、聚集度
- 验收：模式 <10 = 奇异胞腔假说成立；>50 = 例外散开
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

    pairs = []
    for m in range(2, n):
        single = f"s{m}_{m+1}"
        prefix = f"s1_{''.join(str(x) for x in range(2, m + 1))}"
        pairs.append((m, single, prefix))

    def has_opp(full):
        for m, s1, s2 in pairs:
            v1, v2 = full[name2idx[s1]], full[name2idx[s2]]
            if v1 == 0 and v2 == 0:
                return True
            if v1 != 0 and v2 != 0 and v1 == -v2:
                return True
        return False

    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [name2idx[x] for x in basis50]

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    exc0 = []   # A=0 无符号对相反
    exc1 = []   # A≠0 无符号对相反
    for sd, data in datas.items():
        for full, a in data:
            if not has_opp(full):
                if sign(a) == 0:
                    exc0.append((full, sd))
                else:
                    exc1.append((full, sd))
    print(f"A=0 无符号对相反: {len(exc0)} / A≠0 无符号对相反: {len(exc1)}")

    # 50 基座模式分布
    pat0 = defaultdict(int)
    pat1 = defaultdict(int)
    sd0 = defaultdict(lambda: defaultdict(int))
    for full, sd in exc0:
        pat0[tuple(full[i] for i in idx50)] += 1
        sd0[tuple(full[i] for i in idx50)][sd] += 1
    for full, sd in exc1:
        pat1[tuple(full[i] for i in idx50)] += 1

    print(f"\nA=0 例外: {len(pat0)} 个不同 50 模式（聚集度：样本/模式 = {len(exc0)}/{len(pat0)})")
    top0 = sorted(pat0.items(), key=lambda x: -x[1])[:8]
    for pat, c in top0:
        p = "".join("-" if v < 0 else ("+" if v > 0 else "0") for v in pat)
        seeds = {sd: sd0[pat][sd] for sd in sd0[pat]}
        print(f"  {p}: {c} 个样本（seed 分布 {seeds}）")
    print(f"A≠0 例外: {len(pat1)} 个不同 50 模式（样本/模式 = {len(exc1)}/{len(pat1)})")
    top1 = sorted(pat1.items(), key=lambda x: -x[1])[:5]
    for pat, c in top1:
        p = "".join("-" if v < 0 else ("+" if v > 0 else "0") for v in pat)
        print(f"  {p}: {c}")

    # 对照：A=0 全体的 50 模式数（总胞腔结构）
    pat_all0 = set()
    for sd, data in datas.items():
        for full, a in data:
            if sign(a) == 0:
                pat_all0.add(tuple(full[i] for i in idx50))
    print(f"\n对照：A=0 全体 50 模式数 {len(pat_all0)}（例外占 {len(pat0)}）")

    out = {"exc0_n": len(exc0), "exc0_pat": len(pat0), "exc0_top": [(list(k), v) for k, v in top0],
           "exc1_n": len(exc1), "exc1_pat": len(pat1), "exc1_top": [(list(k), v) for k, v in top1],
           "all0_pat": len(pat_all0)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_exceptions_geometry.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_exceptions_geometry.json")
