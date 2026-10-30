# -*- coding: utf-8 -*-
"""M21：含零块区精确退化判据
- A≠0 中含零块比例（对照 M19：A=0 含零块 73.5%）
- 粒子 1 长块过零子样本内：区分 A=0 vs A≠0 的最小因子集
- 检验 T1 精确化：退化 ⟺ 长块过零 + 额外条件？
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
    # 粒子 1 相关长块（≥8 粒子，含粒子 1）
    p1_long_idx = [k for k in range(len(factors))
                   if (0 in factors[k][0] or 0 in factors[k][1])
                   and len(factors[k][0]) + len(factors[k][1]) >= 8]
    p1_long = set(NAMES[k] for k in p1_long_idx)

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    zero = []   # A=0
    nz = []     # A≠0
    for sd, data in datas.items():
        for full, a in data:
            (zero if sign(a) == 0 else nz).append((full, sd))
    print(f"A=0: {len(zero)} / A≠0: {len(nz)}")

    # 1) A≠0 含零块统计
    nz_has_zero = sum(1 for full, sd in nz if any(abs(v) < 1e-9 for v in full))
    nz_has_p1long = sum(1 for full, sd in nz
                        if any(NAMES[k] in p1_long and abs(full[k]) < 1e-9 for k in range(len(factors))))
    print(f"A≠0 中含任意零块: {nz_has_zero} ({nz_has_zero/len(nz):.3f}) / 含粒子1长零块: {nz_has_p1long} ({nz_has_p1long/len(nz):.3f})")
    # A=0 中含零块/含粒子1长零块
    z_has_zero = sum(1 for full, sd in zero if any(abs(v) < 1e-9 for v in full))
    z_has_p1long = sum(1 for full, sd in zero
                       if any(NAMES[k] in p1_long and abs(full[k]) < 1e-9 for k in range(len(factors))))
    print(f"A=0 中含任意零块: {z_has_zero} ({z_has_zero/len(zero):.3f}) / 含粒子1长零块: {z_has_p1long} ({z_has_p1long/len(zero):.3f})")

    # 2) 粒子 1 长块过零子样本内：区分 A=0 vs A≠0
    z_sub = [x for x in zero if any(NAMES[k] in p1_long and abs(x[0][k]) < 1e-9 for k in range(len(factors)))]
    nz_sub = [x for x in nz if any(NAMES[k] in p1_long and abs(x[0][k]) < 1e-9 for k in range(len(factors)))]
    print(f"\n粒子1长块过零子样本：A=0 {len(z_sub)} / A≠0 {len(nz_sub)}")

    # 3) 该子样本内因子判别率（排除恒零的粒子 1 长块本身——它们全为 0 无判别力）
    disc = []
    for k, name in enumerate(NAMES):
        d0 = defaultdict(int)
        d1 = defaultdict(int)
        for full, sd in z_sub:
            d0[full[k]] += 1
        for full, sd in nz_sub:
            d1[full[k]] += 1
        tvd = sum(abs(d0[v] / len(z_sub) - d1.get(v, 0) / len(nz_sub)) for v in (-1, 0, 1))
        disc.append((tvd, k))
    disc.sort(reverse=True)
    print("\n子样本内 Top 10 判别因子：")
    for tvd, k in disc[:10]:
        print(f"  {NAMES[k]}: TVD={tvd:.4f}")

    # 4) 贪心：在子样本内找最小判别基座
    sel = []
    cand_order = [k for _, k in disc]
    for k in cand_order:
        trial = sel + [k]
        p0 = set(tuple(full[i] for i in trial) for full, sd in z_sub)
        p1 = set(tuple(full[i] for i in trial) for full, sd in nz_sub)
        if len(p0 & p1) == 0:
            sel = trial
            changed = True
            while changed:
                changed = False
                for j in range(len(sel)):
                    sub = [sel[x] for x in range(len(sel)) if x != j]
                    q0 = set(tuple(full[i] for i in sub) for full, sd in z_sub)
                    q1 = set(tuple(full[i] for i in sub) for full, sd in nz_sub)
                    if len(q0 & q1) == 0:
                        sel = sub
                        changed = True
                        break
            if len(sel) <= 60:
                pass
            else:
                continue
    print(f"\n粒子1长块过零子样本内判别基座：{len(sel)} 因子")
    print("  ", ", ".join(NAMES[k] for k in sel))

    out = {"nz_has_zero": nz_has_zero, "nz_has_p1long": nz_has_p1long,
           "z_has_zero": z_has_zero, "z_has_p1long": z_has_p1long,
           "z_sub": len(z_sub), "nz_sub": len(nz_sub),
           "sub_top10": [(NAMES[k], round(tvd, 4)) for tvd, k in disc[:10]],
           "sub_basis": [NAMES[k] for k in sel]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_precise_deg.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_precise_deg.json")
