# -*- coding: utf-8 -*-
"""M2：符号保持局域扰动采样——验证 4 个冲突模式在模式内是否多值
- 种子：4 冲突实例 (omega, zbar)
- 扰动：ω0..ω8 乘性 (1+u)、z0..z8 加性扰动，ω9/z9 按动量守恒重算；保持 R1 符号
- 投影校验：50 维 sg_block 与种子逐位相同（符号保持）
- 尺度 r ∈ {1e-5,1e-4,1e-3,1e-2,1e-1}，每尺度每种子 20000 有效点
- 输出：每种子每尺度 A_BG 分布；多值 → 模式内多值实证
"""
import json, math, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_n10_criterion import adj_partition_factors


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_conflict_vectors.json"), encoding="utf-8") as f:
        cv = json.load(f)
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    base_names = cv["base"]
    idx = [NAMES.index(x) for x in base_names]

    def pattern_on(omega, zbar):
        return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)

    scales = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    per_scale = 20000
    out = {}
    for ci, inst in enumerate(cv["detail"]):
        omega0 = list(inst["omega"])
        zbar0 = list(inst["zbar"])
        pat0 = pattern_on(omega0, zbar0)
        rng = random.Random(1000 + ci)
        dist = defaultdict(Counter)
        jumps = []
        for r in scales:
            ok = 0
            while ok < per_scale:
                # 扰动 ω
                w = [omega0[0] * (1.0 + rng.uniform(-r, r))]
                for a in range(1, 9):
                    w.append(omega0[a] * (1.0 + rng.uniform(-r, r)))
                w.append(-sum(w[:9]))
                if w[9] >= 0:  # R1：ω9<0
                    continue
                # 扰动 z
                z = [zbar0[i] + rng.uniform(-3.0 * r, 3.0 * r) for i in range(9)]
                s = sum(w[:9])
                z.append(sum(w[i] * z[i] for i in range(9)) / s)
                # 投影校验（符号保持）
                pat = pattern_on(w, z)
                if pat != pat0:
                    continue
                v = round(A_BG(10, w, z), 6)
                dist[ci][v] += 1
                ok += 1
                # 跳变记录：与主表值不同
                if abs(v - inst["main"]) > 1e-9 and len(jumps) < 50:
                    jumps.append({"scale": r, "omega": w, "zbar": z, "v": v})
            print(f"instance {ci} r={r}: {dict(dist[ci])}", flush=True)
        out[ci] = {
            "seed": inst["seed"], "sample": inst["sample"], "main": inst["main"],
            "indep": inst["indep"], "dist": {str(k): int(v) for k, v in dist[ci].items()},
            "multi_valued": len(dist[ci]) > 1,
            "jumps": jumps,
        }

    with open(os.path.join(SCRIPT_DIR, "paperX_n10_local_scan.json"), "w", encoding="utf-8") as f:
        json.dump({"instances": out, "base": base_names}, f, ensure_ascii=False, indent=1)
    for ci, o in out.items():
        print(f"instance {ci}: multi={o['multi_valued']} dist={ {k: dict(v) for k, v in o['dist'].items()} }")
    print("DONE")
