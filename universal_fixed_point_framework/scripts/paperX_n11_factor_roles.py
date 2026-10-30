# -*- coding: utf-8 -*-
"""判据分层结构分析（解析完全闭合深化）
1. 50 基座因子角色分类：符号因子（A≠0 域内必要）vs 退化因子（A=0 判别必要）
2. A=0 退化机制：A=0 样本的零块/长块特征（验证"退化 ⟺ 长块过零/翻转"）
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
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    extra50 = list(j50.get("added", []))
    idx50 = [NAMES.index(x) for x in basis50]

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    # A≠0 域 / 全域样本收集（3 seed 合并）
    nz_samples = []   # (full, a) A≠0
    all_samples = []  # (full, a)
    for sd, data in datas.items():
        for full, a in data:
            all_samples.append((full, a))
            if sign(a) != 0:
                nz_samples.append((full, a))
    print(f"全样本 {len(all_samples)} / 非零 {len(nz_samples)} / 零 {len(all_samples)-len(nz_samples)}")

    # 1) 因子角色分类：逐一从 50 基座删除，测域内/域外非决定增量
    role = {}
    # 符号角色：A≠0 域内，删掉该因子后是否引入多符号模式
    base_pat_nz = defaultdict(set)
    for full, a in nz_samples:
        pat = tuple(sign(full[k]) for k in idx50)
        base_pat_nz[pat].add(sign(a))
    base_multi_nz = sum(1 for v in base_pat_nz.values() if len(v) > 1)
    # 退化角色：全域内（A 三值），删掉该因子后是否引入多值模式
    base_pat_all = defaultdict(set)
    for full, a in all_samples:
        pat = tuple(sign(full[k]) for k in idx50)
        base_pat_all[pat].add(a)
    base_multi_all = sum(1 for v in base_pat_all.values() if len(v) > 1)
    print(f"50 基座基线: 非零域多符号 {base_multi_nz} / 全域多值 {base_multi_all}")

    for j, fn in enumerate(basis50):
        rem = [k for i, k in enumerate(idx50) if i != j]
        # 符号角色
        pat_nz = defaultdict(set)
        for full, a in nz_samples:
            pat = tuple(sign(full[k]) for k in rem)
            pat_nz[pat].add(sign(a))
        m_nz = sum(1 for v in pat_nz.values() if len(v) > 1)
        # 退化角色
        pat_all = defaultdict(set)
        for full, a in all_samples:
            pat = tuple(sign(full[k]) for k in rem)
            pat_all[pat].add(a)
        m_all = sum(1 for v in pat_all.values() if len(v) > 1)
        role[fn] = {"del_nz_multi": m_nz, "del_all_multi": m_all,
                    "sign_needed": m_nz > base_multi_nz,
                    "degen_needed": m_all > base_multi_all,
                    "is_extra50": fn in extra50}
    # 分类汇总
    sign_only, degen_only, both, neither = [], [], [], []
    for fn, r in role.items():
        if r["sign_needed"] and r["degen_needed"]:
            both.append(fn)
        elif r["sign_needed"]:
            sign_only.append(fn)
        elif r["degen_needed"]:
            degen_only.append(fn)
        else:
            neither.append(fn)
    print(f"\n=== 50 基座因子角色 ===")
    print(f"双重必要 {len(both)}: {both[:6]}...")
    print(f"仅符号必要 {len(sign_only)}: {sign_only}")
    print(f"仅退化必要 {len(degen_only)}: {degen_only}")
    print(f"两者皆非(单样本下) {len(neither)}: {neither[:6]}...")
    print(f"\n4 补入长块角色:")
    for fn in extra50:
        r = role.get(fn, {})
        print(f"  {fn}: 符号必要 {r.get('sign_needed')} / 退化必要 {r.get('degen_needed')}")

    # 2) A=0 退化机制：A=0 样本中零块/长块统计
    zero_block_count = defaultdict(int)
    n_zero = 0
    for full, a in all_samples:
        if sign(a) != 0:
            continue
        n_zero += 1
        zs = [NAMES[k] for k, v in enumerate(full) if abs(v) < 1e-9]
        for z in zs:
            zero_block_count[z] += 1
    print(f"\n=== A=0 样本 {n_zero} 个的零块统计（Top10）===")
    for b, c in sorted(zero_block_count.items(), key=lambda x: -x[1])[:10]:
        print(f"  {b}: {c} ({c/max(n_zero,1):.3f})")
    # 无任何零块的 A=0 样本比例
    no_zero = 0
    for full, a in all_samples:
        if sign(a) != 0:
            continue
        if not any(abs(v) < 1e-9 for v in full):
            no_zero += 1
    print(f"无零块的 A=0 样本: {no_zero}/{n_zero}")

    out = {"baseline": {"nz_multi": base_multi_nz, "all_multi": base_multi_all},
           "role": role, "summary": {"both": len(both), "sign_only": len(sign_only),
                                      "degen_only": len(degen_only), "neither": len(neither)},
           "zero_block_top": sorted(zero_block_count.items(), key=lambda x: -x[1])[:15],
           "n_A_zero": n_zero, "n_A_zero_no_zero_block": no_zero}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_factor_roles.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_factor_roles.json")
