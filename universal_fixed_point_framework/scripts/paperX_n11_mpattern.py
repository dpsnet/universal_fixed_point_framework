# -*- coding: utf-8 -*-
"""M23：m-pattern 精细判别（M22 符号对相反的非充分性弥补）
- 每样本：m-pattern = 符号对相反成立的 m 集合（m=2..10，9 位）
- A=0 vs A≠0 的 m-pattern 分布对照 + 判别重叠
- 324 例外（无符号对相反 A=0）与 167 对照的邻近结构
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

    # m-pattern：m=2..10，每 m 两个因子 s{m}_{m+1} 与 s1_2..m
    ms = list(range(2, n))
    def m_pattern(full):
        pat = []
        for m in ms:
            v1 = full[name2idx[f"s{m}_{m+1}"]]
            v2 = full[name2idx[f"s1_{''.join(str(x) for x in range(2, m + 1))}"]]
            if v1 == 0 and v2 == 0:
                pat.append(m)
            elif v1 != 0 and v2 != 0 and v1 == -v2:
                pat.append(m)
        return frozenset(pat)

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    pat0 = defaultdict(int)   # A=0 的 m-pattern 分布
    pat1 = defaultdict(int)   # A≠0 的 m-pattern 分布
    n0 = n1 = 0
    for sd, data in datas.items():
        for full, a in data:
            p = m_pattern(full)
            if sign(a) == 0:
                pat0[p] += 1
                n0 += 1
            else:
                pat1[p] += 1
                n1 += 1
    print(f"A=0: {n0} / A≠0: {n1}")
    print(f"m-pattern 数：A=0 {len(pat0)} / A≠0 {len(pat1)}")

    # Top m-patterns 对照
    top0 = sorted(pat0.items(), key=lambda x: -x[1])[:12]
    top1 = sorted(pat1.items(), key=lambda x: -x[1])[:12]
    print("\nA=0 Top 12 m-pattern（freq, 占比）：")
    for p, c in top0:
        print(f"  m={sorted(p)}: {c} ({c/n0:.4f})")
    print("A≠0 Top 12 m-pattern（freq, 占比）：")
    for p, c in top1:
        print(f"  m={sorted(p)}: {c} ({c/n1:.4f})")

    # 判别：m-pattern 是否唯一判别（重叠模式）
    overlap = set(pat0) & set(pat1)
    print(f"\n重叠 m-pattern：{len(overlap)}（A=0 模式 {len(pat0)} / A≠0 {len(pat1)}）")
    # 若重叠为空 → m-pattern 完全判别
    if not overlap:
        print("★ m-pattern 完全判别 A=0 vs A≠0（无重叠）——解析判据 = m-pattern 分类！")
    else:
        # 重叠模式上的符号分裂（A=0 与 A≠0 共存）
        for p in sorted(overlap, key=lambda x: -pat0[x])[:10]:
            print(f"  重叠 m={sorted(p)}: A=0 {pat0[p]} vs A≠0 {pat1[p]}")

    # 324 例外（A=0 无符号对相反 = m-pattern 空）vs A≠0 m-pattern 空
    empty0 = pat0.get(frozenset(), 0)
    empty1 = pat1.get(frozenset(), 0)
    print(f"\n空 m-pattern（无符号对相反）：A=0 {empty0}（M22 报 324）/ A≠0 {empty1}（M22 报 167）")

    # m-pattern 大小分布（判别特征：A=0 是否 m 更多）
    size0 = defaultdict(int)
    size1 = defaultdict(int)
    for p, c in pat0.items():
        size0[len(p)] += c
    for p, c in pat1.items():
        size1[len(p)] += c
    print("\nm-pattern 大小分布：")
    for s in range(0, 10):
        if size0[s] or size1[s]:
            print(f"  |m|={s}: A=0 {size0[s]} ({size0[s]/n0:.4f}) / A≠0 {size1[s]} ({size1[s]/n1:.4f})")

    out = {"pat0_top": [(sorted(list(k)), v) for k, v in top0],
           "pat1_top": [(sorted(list(k)), v) for k, v in top1],
           "overlap": [sorted(list(k)) for k in overlap],
           "empty0": empty0, "empty1": empty1,
           "size0": dict(size0), "size1": dict(size1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_mpattern.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_mpattern.json")
