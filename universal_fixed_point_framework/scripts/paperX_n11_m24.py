# -*- coding: utf-8 -*-
"""M24：重叠/例外区的完备判据检验
- 重叠 153 m-pattern 区：A=0 vs A≠0 是否可用附加因子 100% 判别
- 空 m-pattern 区：A=0（324）vs A≠0（167）判别
- 结论：若判别基座 >0 → m-pattern + 附加因子完备；若 0 → m-pattern 是块和层最细粒度（完备判据不存在于块和层）
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


def greedy_basis(grp0, grp1, idx_cand, NAMES):
    """贪心：用候选因子索引集找最小判别基座（两样本组 100% 可分）"""
    sel = []
    for k in idx_cand:
        trial = sel + [k]
        p0 = set(tuple(g[i] for i in trial) for g in grp0)
        p1 = set(tuple(g[i] for i in trial) for g in grp1)
        if len(p0 & p1) == 0:
            sel = trial
            # 最小化
            changed = True
            while changed:
                changed = False
                for j in range(len(sel)):
                    sub = [sel[x] for x in range(len(sel)) if x != j]
                    q0 = set(tuple(g[i] for i in sub) for g in grp0)
                    q1 = set(tuple(g[i] for i in sub) for g in grp1)
                    if len(q0 & q1) == 0:
                        sel = sub
                        changed = True
                        break
        if len(sel) > 0 and len(p0) < 500:
            pass
    return sel


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
    ms = list(range(2, n))
    pair_idx = []
    for m in ms:
        pair_idx.append(name2idx[f"s{m}_{m+1}"])
        pair_idx.append(name2idx[f"s1_{''.join(str(x) for x in range(2, m + 1))}"])

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

    # 样本按 (m-pattern, A符号) 分类
    by_pat = defaultdict(lambda: defaultdict(list))  # pat -> A -> [full]
    for sd, data in datas.items():
        for full, a in data:
            by_pat[m_pattern(full)][sign(a)].append(full)

    # 重叠模式
    overlap = [p for p, d in by_pat.items() if len(d) > 1]
    print(f"重叠 m-pattern：{len(overlap)}（M23 报 153——含 A=-1/A=+1/A=0 分裂的合计）")

    # 每个重叠模式：A=0 vs A≠0（A≠0 合并 -1/+1）
    results = []
    for p in overlap:
        d = by_pat[p]
        grp0 = d.get(0, [])
        grp1 = d.get(-1, []) + d.get(1, [])
        if grp0 and grp1:
            results.append((p, grp0, grp1))
    print(f"含 A=0 与 A≠0 的重叠模式：{len(results)}")
    # 样本计数
    tot0 = sum(len(g0) for _, g0, _ in results)
    tot1 = sum(len(g1) for _, _, g1 in results)
    print(f"  重叠区样本：A=0 {tot0} / A≠0 {tot1}")

    # 判别分析（每模式内）：用 m-pattern 因子之外的全部因子（220-18 = 202 候选）
    nonpair_idx = [k for k in range(len(NAMES)) if k not in pair_idx]
    basis_sizes = []
    fail_modes = 0
    for p, grp0, grp1 in results:
        sel = greedy_basis(grp0, grp1, nonpair_idx, NAMES)
        basis_sizes.append(len(sel))
        if len(sel) == 0:
            fail_modes += 1
    from collections import Counter
    sz_hist = Counter(basis_sizes)
    print(f"\n重叠模式内判别基座大小分布（202 附加因子）：")
    for sz in sorted(sz_hist):
        print(f"  |基座|={sz}: {sz_hist[sz]} 个模式")
    print(f"不可判模式（基座 0）：{fail_modes}/{len(results)}")

    # 空模式区：A=0 324 vs A≠0 167
    empty0 = by_pat[frozenset()].get(0, [])
    empty1 = by_pat[frozenset()].get(-1, []) + by_pat[frozenset()].get(1, [])
    print(f"\n空模式区：A=0 {len(empty0)} / A≠0 {len(empty1)}")
    if empty0 and empty1:
        sel_e = greedy_basis(empty0, empty1, nonpair_idx, NAMES)
        print(f"空模式区判别基座（202 附加因子）：{len(sel_e)} 因子")
        if sel_e:
            print("  ", ", ".join(NAMES[k] for k in sel_e[:15]))

    out = {"overlap_modes": len(overlap), "with_both": len(results),
           "tot0": tot0, "tot1": tot1, "basis_hist": dict(sz_hist),
           "fail_modes": fail_modes, "empty0": len(empty0), "empty1": len(empty1),
           "empty_basis": len(sel_e) if (empty0 and empty1) else -1}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m24_complete.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m24_complete.json")
