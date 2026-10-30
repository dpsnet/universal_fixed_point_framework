# -*- coding: utf-8 -*-
"""M26b：n=11 环向因子独立性（50 基座模式分组检验）
- 采样含环向因子 s11_1/s11_12/s11_123
- 按 50 基座模式分组：重复模式组内环向符号一致性
- 若重复组内环向分裂 → 环向独立于 50 基座 → 8 冲突机制支持
"""
import os, json, sys, random
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_single_minus_numerics import sg_block


def sg(x):
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

    j50 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_fill46_80000.json"), encoding="utf-8"))
    basis50 = list(j50["final_set"])
    idx50 = [name2idx[x] for x in basis50]
    print(f"50 基座 {len(idx50)} 因子")

    N_PER = 40000
    sd = 77
    rng = random.Random(sd)
    groups = defaultdict(list)
    cnt = 0
    while cnt < N_PER:
        omega, zbar, _ = gen_partial_collinear(n, 0, rng=rng, r1=True, momentum=True)
        # 50 基座 + 环向
        key50 = tuple(sg_block(omega, zbar, tuple(range(i, k + 1)), tuple(range(k + 1, j + 1)))
                      for i, j, k in [(int(x.split("_")[0][1:]) - 1 if False else None) for x in []]) if False else None
        # 直接按索引算
        facs = []
        for ii, jj in [(int(x.split("_")[0][1:]) - 1, int(x.split("_")[1][0:])) for x in basis50]:
            pass
        # 简化：用 name2idx 直接
        v50 = tuple(sg_block(omega, zbar,
                             tuple(range(int(b[1:].split("_")[0]) - 1, int(b.split("_")[0][1:])) if False else ()))
                    for b in basis50) if False else None
        # 直接手工
        vals50 = []
        for b in basis50:
            a_part, b_part = b.split("_")
            a = tuple(int(c) - 1 for c in a_part[1:])
            bb = tuple(int(c) - 1 for c in b_part)
            vals50.append(sg_block(omega, zbar, a, bb))
        s11_1 = sg_block(omega, zbar, (10,), (0,))
        s11_12 = sg_block(omega, zbar, (10,), (0, 1))
        s11_123 = sg_block(omega, zbar, (10,), (0, 1, 2))
        groups[tuple(vals50)].append((s11_1, s11_12, s11_123))
        cnt += 1
    print(f"seed {sd}: {N_PER} 样本 / {len(groups)} 个 50 模式")

    # 重复模式组
    reps = {p: lst for p, lst in groups.items() if len(lst) > 1}
    print(f"重复模式组：{len(reps)}（组内样本 {sum(len(v) for v in reps.values())}）")
    # 组内环向一致性
    split1 = sum(1 for lst in reps.values() if len({x[0] for x in lst}) > 1)
    split2 = sum(1 for lst in reps.values() if len({x[1] for x in lst}) > 1)
    split3 = sum(1 for lst in reps.values() if len({x[2] for x in lst}) > 1)
    print(f"组内环向分裂：s11_1 {split1} / s11_12 {split2} / s11_123 {split3}（共 {len(reps)} 组）")

    out = {"n": N_PER, "patterns": len(groups), "reps": len(reps),
           "split1": split1, "split2": split2, "split3": split3}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_cyclic_factor.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_cyclic_factor.json")
