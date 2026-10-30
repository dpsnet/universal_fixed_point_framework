# -*- coding: utf-8 -*-
"""M29：最小完备子集搜索（定向补集——8 冲突组的 220 区分因子）
- 从缓存找 50 基座冲突组（同 50 模式不同 A）——8 组
- 对每组：组内样本 A≠0 vs A=0 的 220 因子符号差异 → 区分因子候选 C
- 检验 50+C 全样本 0 冲突？→ 尝试删减 C → 最小补集（判据工程最优基座线索）
"""
import os, json, pickle, sys, time
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


def conflict_count(pats):
    c = 0
    for p, vals in pats.items():
        if len({sg(v) for v in vals}) > 1:
            c += 1
    return c


if __name__ == "__main__":
    factors = adj_partition_factors(11)
    NAMES = [factor_name(a, b) for a, b in factors]
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [NAMES.index(x) for x in basis50]
    print(f"50 基座 {len(idx50)} 因子")

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)
    samples = [(facs, a) for sd, data in datas.items() for facs, a in data]
    print(f"总样本 {len(samples)}")

    # 50 冲突组
    pat50 = defaultdict(list)
    for facs, a in samples:
        pat50[tuple(facs[i] for i in idx50)].append((facs, a))
    conf_groups = [(p, vals) for p, vals in pat50.items() if len({sg(v) for _, v in vals}) > 1]
    print(f"50 冲突组：{len(conf_groups)}")

    # 对每组：区分因子（A≠0 样本与 A=0 样本的 220 因子符号差异）
    cand = set()
    for gi, (p, vals) in enumerate(conf_groups):
        pos = [f for f, a in vals if sg(a) != 0]
        zero = [f for f, a in vals if sg(a) == 0]
        if not pos or not zero:
            continue
        diffs = set()
        for f1 in pos:
            for f2 in zero:
                for i in range(220):
                    if f1[i] != f2[i]:
                        diffs.add(i)
        cand |= diffs
        print(f"  组{gi}: 样本 {len(vals)}（A≠0 {len(pos)} / A=0 {len(zero)}）——区分因子候选 {len(diffs)}")

    cand_list = sorted(cand - set(idx50))
    print(f"\n候选补集（220 中非 50 基座的区分因子）：{len(cand_list)} 个")
    print("名字:", [NAMES[i] for i in cand_list][:20])

    # 检验 50 + 候选 冲突
    full = idx50 + cand_list
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in full)].append(a)
    c = conflict_count(pat)
    print(f"50+候选（{len(full)} 因子）：冲突 {c}")

    # 贪心删减候选（每因子删后仍 0 冲突则删）
    cur = set(cand_list)
    t0 = time.time()
    for f in list(cur):
        trial = idx50 + sorted(cur - {f})
        patt = defaultdict(list)
        for facs, a in samples:
            patt[tuple(facs[i] for i in trial)].append(a)
        if conflict_count(patt) == 0:
            cur.remove(f)
    print(f"贪心删减后补集：{len(cur)} 个（用时 {time.time()-t0:.0f}s）")
    final = idx50 + sorted(cur)
    print(f"最终基座：{len(final)} 因子")

    patf = defaultdict(list)
    for facs, a in samples:
        patf[tuple(facs[i] for i in final)].append(a)
    cf = conflict_count(patf)
    print(f"最终基座冲突：{cf}")
    print("补集名字:", [NAMES[i] for i in sorted(cur)])

    out = {"basis50": basis50, "cand": len(cand_list), "final_size": len(final),
           "final_conflict": cf, "added": [NAMES[i] for i in sorted(cur)]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m29_minimal.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m29_minimal.json")
