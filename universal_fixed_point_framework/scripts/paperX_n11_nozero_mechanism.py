# -*- coding: utf-8 -*-
"""M20：无零块 A=0 的判别因子分析（第二机制画像）
- 类别：无零块 A=0（63026）vs A≠0（2292）
- 判别率：220 全因子逐一（取值分布差异）
- 贪心构建区分两类的因子基座
- 输出：第二机制（分子相消）的因子画像
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
    return "s" + "".join(str(x + 1) for x in a) + "_" + "".join(str(x + 1) for x in b)


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

    nozero = []   # (full, sd)：无零块 A=0
    nz = []       # (full, sd)：A≠0
    for sd, data in datas.items():
        for full, a in data:
            if sign(a) == 0:
                if all(abs(v) > 1e-9 for v in full):
                    nozero.append((full, sd))
            else:
                nz.append((full, sd))
    print(f"无零块 A=0: {len(nozero)} / A≠0: {len(nz)}")

    # 1) 220 因子判别率：两类取值分布差异（用方差归一的距离）
    #    每因子取值 {−1,0,+1}（无零块类别里 0 也出现在非零块? 无零块定义=无零块，所以全部 ±1）
    #    对 A≠0 类别，因子可能有 0。
    disc = []
    for k, name in enumerate(NAMES):
        # 分布
        dist0 = defaultdict(int)  # nozero
        dist1 = defaultdict(int)  # nz
        for full, sd in nozero:
            dist0[full[k]] += 1
        for full, sd in nz:
            dist1[full[k]] += 1
        n0, n1 = len(nozero), len(nz)
        # 总变差距离 TVD
        tvd = sum(abs(dist0[v] / n0 - dist1.get(v, 0) / n1) for v in (-1, 0, 1))
        disc.append((tvd, name, dict(dist0), dict(dist1)))
    disc.sort(reverse=True)
    print("\nTop 12 判别因子（TVD 越大越能区分两类）：")
    for tvd, name, d0, d1 in disc[:12]:
        print(f"  {name}: TVD={tvd:.4f}  nozero={{-1:{d0.get(-1,0)/len(nozero):.3f}, +1:{d0.get(1,0)/len(nozero):.3f}}}  nz={{-1:{d1.get(-1,0)/len(nz):.3f}, 0:{d1.get(0,0)/len(nz):.3f}, +1:{d1.get(1,0)/len(nz):.3f}}}")

    # 2) 贪心构建判别基座：按 TVD 降序，逐因子补入直到两类 100% 可分
    picked = []
    remaining = list(range(len(NAMES)))
    # 排序后的候选
    cand_order = [k for _, name, _, _ in disc]
    pat0 = set()
    for full, sd in nozero:
        pat0.add(tuple(full[i] for i in []))
    # 逐层
    sel = []
    for k in cand_order:
        if len(sel) >= 60:
            break
        # 试加 k
        trial = sel + [k]
        p0 = set()
        p1 = set()
        overlap = set()
        for full, sd in nozero:
            t = tuple(full[i] for i in trial)
            if t in p1:
                overlap.add(t)
            p0.add(t)
        for full, sd in nz:
            t = tuple(full[i] for i in trial)
            if t in p0:
                overlap.add(t)
            p1.add(t)
        if len(overlap) == 0:
            sel = trial
            # 更新：还能否再删？
            changed = True
            while changed:
                changed = False
                for j in range(len(sel)):
                    sub = [sel[x] for x in range(len(sel)) if x != j]
                    q0 = set(tuple(full[i] for i in sub) for full, sd in nozero)
                    q1 = set(tuple(full[i] for i in sub) for full, sd in nz)
                    if len(q0 & q1) == 0:
                        sel = sub
                        changed = True
                        break
            if len(sel) >= 8 and len(p0) < 2000:
                # 已经可分且样本模式较少——记录当前最优并继续尝试更小
                pass
    print(f"\n贪心判别基座大小（第 2 机制）：{len(sel)} 因子")
    print("  因子：", ", ".join(NAMES[k] for k in sel))
    # 核验：最终 sel 是否仍可分
    q0 = set(tuple(full[i] for i in sel) for full, sd in nozero)
    q1 = set(tuple(full[i] for i in sel) for full, sd in nz)
    print(f"  核验：两类模式重叠 {len(q0 & q1)}（应为 0）")

    # 3) 与 50 基座重叠：第二机制判别因子中哪些已在 50 基座
    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    in50 = [NAMES[k] for k in sel if NAMES[k] in basis50]
    print(f"  判别因子中已在 50 基座：{len(in50)}/{len(sel)} -> {in50}")

    out = {"nozero_n": len(nozero), "nz_n": len(nz), "top12": [(x[1], x[0]) for x in disc[:12]],
           "greedy_basis": [NAMES[k] for k in sel], "basis_in50": in50}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_nozero_mechanism.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_nozero_mechanism.json")
