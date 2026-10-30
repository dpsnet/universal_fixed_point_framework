# -*- coding: utf-8 -*-
"""M19：A=0 退化机制图谱（解析完全闭合第二块基石）
- A=0 样本分类：含零块 vs 无零块
- 含零块：检验"第一级递归分母过零主导"假设（含 1 号粒子的块和）
- 无零块：翻转块模式分析（A=0 的第二机制候选）
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
    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    # 收集 A=0 样本（3 seed 合并）
    zero_samples = []
    nz_samples = []
    for sd, data in datas.items():
        for full, a in data:
            if sign(a) == 0:
                zero_samples.append((full, sd))
            else:
                nz_samples.append((full, sd))
    print(f"A=0 样本 {len(zero_samples)} / A≠0 {len(nz_samples)}")

    # 1) 分类：含零块 vs 无零块
    has_zero = []
    no_zero = []
    for full, sd in zero_samples:
        zs = [NAMES[k] for k, v in enumerate(full) if abs(v) < 1e-9]
        if zs:
            has_zero.append((full, sd, zs))
        else:
            no_zero.append((full, sd))
    print(f"含零块 {len(has_zero)} ({len(has_zero)/len(zero_samples):.3f}) / 无零块 {len(no_zero)} ({len(no_zero)/len(zero_samples):.3f})")

    # 2) 含零块：是否含"粒子 1 相关长块"（递归分母候选）
    p1_blocks = [NAMES[k] for k in range(len(factors)) if 0 in factors[k][0] or 0 in factors[k][1]]
    p1_long = [b for b in p1_blocks if len(b.split("_")[0]) + len(b.split("_")[1]) >= 8]
    has_p1 = 0
    has_p1_long = 0
    zero_blocks_set = set()
    for full, sd, zs in has_zero:
        if any(z in p1_blocks for z in zs):
            has_p1 += 1
        if any(z in p1_long for z in zs):
            has_p1_long += 1
        zero_blocks_set.update(zs)
    print(f"含零块中：含粒子1相关零块 {has_p1} ({has_p1/len(has_zero):.3f}) / 含粒子1长零块 {has_p1_long} ({has_p1_long/len(has_zero):.3f})")

    # 3) 无零块样本：块和离散值分布（确认 ±1）+ A=0 的第二机制
    #    检查：无零块样本中是否存在"块符号全部相同于某个 A≠0 模式"的对照
    #    ——即同一符号模式既有 A=0 又有 A≠0（这是退化判据失败——长块解决）
    #    更直接：无零块 A=0 样本的"翻转块"（相对 A≠0 近邻）——用与 50 补入长块的
    #    关系分析已在 M18 做过（3/31 非决定模式无零块但长块翻转）
    #    这里统计：无零块 A=0 样本中，粒子 1 相关长块的取值分布
    p1_long_idx = [NAMES.index(b) for b in p1_long]
    nozero_p1long_signs = defaultdict(int)
    for full, sd in no_zero[:5000]:  # 采样 5000 个（统计足够）
        for k in p1_long_idx:
            nozero_p1long_signs[NAMES[k]] += full[k]
    print("\n无零块 A=0 样本（前 5000）的粒子 1 长块符号和（≈0 表示均匀分布）：")
    top = sorted(nozero_p1long_signs.items(), key=lambda x: -abs(x[1]))[:8]
    for b, ssum in top:
        print(f"  {b}: 和 {ssum}")

    # 4) 关键对照：无零块 A=0 样本 vs A≠0 样本的 50 基座模式重叠度
    #    —— 退化判据失败的模式 = 无零块 A=0 与 A≠0 共享 50 模式？
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [NAMES.index(x) for x in basis50]
    pat_zero = set()
    pat_nz = set()
    for full, sd in zero_samples:
        pat_zero.add(tuple(full[i] for i in idx50))
    for full, sd in nz_samples:
        pat_nz.add(tuple(full[i] for i in idx50))
    overlap = pat_zero & pat_nz
    print(f"\n50 基座模式重叠（退化判据失败）：{len(overlap)}/{len(pat_zero)} A=0 模式与 A≠0 共享")
    print(f"  （跨 seed 合并口径 8 冲突 = 这类重叠的子集）")

    out = {"n_zero": len(zero_samples), "has_zero_block": len(has_zero),
           "no_zero_block": len(no_zero), "has_p1_zero": has_p1,
           "has_p1_long_zero": has_p1_long,
           "nozero_p1long_top": top, "overlap_50": len(overlap)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_degen_mechanism.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_degen_mechanism.json")
