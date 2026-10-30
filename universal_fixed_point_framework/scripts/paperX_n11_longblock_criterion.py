# -*- coding: utf-8 -*-
"""n=11 长块判据全局验证（解析完全闭合第二步）
- 检验：4 个补入长块（extra50）符号模式 → A 符号是否单值（全局，80000×3）
- 检验：A 符号翻转配置是否全部伴随某补入长块符号翻转
- 对照：46 基座符号模式 → A 符号（应该多值——非决定模式）
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

    total = 0
    for sd, data in datas.items():
        total += len(data)
    print(f"总样本: {total}")

    # 1) 4 长块符号模式 → A 符号 单值性
    extra_pat_a = defaultdict(set)
    # 2) 46 基座符号模式 → A 符号 单值性（对照）
    b46_pat_a = defaultdict(set)
    # 3) 50 基座符号模式 → A 符号（对照组）
    b50_pat_a = defaultdict(set)
    # 4) A 符号翻转伴随长块翻转：相邻样本对检验（同一 seed 内按序）
    flip_total = 0
    flip_with_extra_flip = 0

    for sd, data in datas.items():
        # 用符号化模式（比 float 模式更稳）
        for full, a in data:
            se = tuple(sign(full[k]) for k in idx_extra)
            extra_pat_a[se].add(sign(a))
            s46 = tuple(sign(full[k]) for k in idx46)
            b46_pat_a[s46].add(sign(a))
            s50 = tuple(sign(full[k]) for k in idx50)
            b50_pat_a[s50].add(sign(a))
        # 相邻样本 A 符号翻转
        for i in range(len(data) - 1):
            f0, a0 = data[i]
            f1, a1 = data[i + 1]
            if sign(a0) != sign(a1):
                flip_total += 1
                # 长块符号是否也翻转
                any_extra_flip = any(sign(f0[k]) != sign(f1[k]) for k in idx_extra)
                if any_extra_flip:
                    flip_with_extra_flip += 1
        print(f"seed {sd} done", flush=True)

    # 汇总
    multi_extra = sum(1 for v in extra_pat_a.values() if len(v) > 1)
    multi_46 = sum(1 for v in b46_pat_a.values() if len(v) > 1)
    multi_50 = sum(1 for v in b50_pat_a.values() if len(v) > 1)
    print("\n=== 符号模式 → A 符号 单值性（全局）===")
    print(f"4 长块符号模式: {len(extra_pat_a)} 种, 多符号 {multi_extra} ({'FAIL' if multi_extra else '单值 ✓'})")
    print(f"46 基座符号模式: {len(b46_pat_a)} 种, 多符号 {multi_46} ({'FAIL' if multi_46 else '单值 ✓'})")
    print(f"50 基座符号模式: {len(b50_pat_a)} 种, 多符号 {multi_50} ({'FAIL' if multi_50 else '单值 ✓'})")
    print(f"\n=== A 符号翻转与长块翻转共现（相邻样本对）===")
    print(f"A 翻转对: {flip_total}, 伴随长块翻转: {flip_with_extra_flip} ({flip_with_extra_flip/max(flip_total,1):.3f})")

    res = {"n": n, "total_samples": total,
           "extra4_patterns": len(extra_pat_a), "extra4_multi_sign": multi_extra,
           "b46_patterns": len(b46_pat_a), "b46_multi_sign": multi_46,
           "b50_patterns": len(b50_pat_a), "b50_multi_sign": multi_50,
           "adj_flip_total": flip_total, "adj_flip_with_extra": flip_with_extra_flip,
           "extra50": extra50}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_longblock_criterion.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("DONE -> paperX_n11_longblock_criterion.json")
