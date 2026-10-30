# -*- coding: utf-8 -*-
"""M34：R1 通式 18 因子符号层完备性（直接连接通式 (39)）
- R1 通式：A_R1 = 2^{2-n} ∏_{m=2}^{n-1} (sg_{m,m+1} + sg_{1,2..m})
- 因子族 18 个：{s{m}_{m+1}: m=2..10} + {s1_2..m: m=2..10}
- 检验：18 因子符号模式 → A 符号唯一性（280000 8seed）
- 预期：括号和符号由数值决定——符号层有损失——冲突率量化
"""
import os, json, pickle, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len({sg(v) for v in vals}) > 1)


def group(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return pat


if __name__ == "__main__":
    factors = adj_partition_factors(11)
    NAMES = [factor_name(a, b) for a, b in factors]
    # R1 通式 18 因子：s{m}_{m+1}（m=2..10）+ s1_2..m（m=2..10）
    r1 = []
    for m in range(2, 11):
        r1.append("s%d_%d" % (m, m + 1))
    for m in range(2, 11):
        r1.append("s1_" + "".join(str(x) for x in range(2, m + 1)))
    idx18 = [NAMES.index(x) for x in r1]
    print(f"R1 通式 18 因子：{r1}")

    with open(os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl"), "rb") as f:
        d3 = pickle.load(f)
    with open(os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl"), "rb") as f:
        d5 = pickle.load(f)
    all_samples = []
    for sd in ['77', '331', '777']:
        all_samples.extend(d3[sd])
    for sd in ['211', '555']:
        all_samples.extend(d5[sd])
    print(f"样本 {len(all_samples)}")

    # 18 因子符号冲突
    t0 = time.time()
    c18 = conflict_count(group(all_samples, idx18))
    print(f"[M34a] R1 通式 18 因子符号：冲突模式 {c18}（{time.time()-t0:.0f}s）")

    # 34 对照（谱维数）
    m32 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m32_minimal2.json"), encoding="utf-8"))
    idx34 = [NAMES.index(x) for x in m32["final_names"]]
    c34 = conflict_count(group(all_samples, idx34))
    print(f"[M34b] 34 谱维数：冲突 {c34}")

    # R1 通式 18 + 部分共线额外 16 个（34-18）对照——18+16 = 34 已 0
    # 交集：34 ∩ R1 18
    inter = set(idx34) & set(idx18)
    print(f"34 ∩ R1 18：{len(inter)} 个 -> {[NAMES[i] for i in sorted(inter)]}")
    only34 = [NAMES[i] for i in sorted(set(idx34) - set(idx18))]
    only18 = [NAMES[i] for i in sorted(set(idx18) - set(idx34))]
    print(f"34 独有（R1 18 之外）：{len(only34)} 个 -> {only34}")
    print(f"R1 18 独有（34 之外）：{len(only18)} 个 -> {only18}")

    # 冲突样本的 A 分布（若 c18 > 0——冲突组内 A 符号构成）
    if c18 > 0:
        pat18 = group(all_samples, idx18)
        n_c = 0
        for p, vals in pat18.items():
            if len({sg(v) for v in vals}) > 1:
                print("  冲突模式 A 符号:", sorted({sg(v) for v in vals}), "样本数", len(vals))
                n_c += 1
                if n_c >= 5:
                    break

    out = {"r1_factors": r1, "c18": c18, "c34": c34, "inter": len(inter),
           "only34": only34, "only18": only18}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m34_r1.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m34_r1.json")
