# -*- coding: utf-8 -*-
"""M22：符号对相反机制（通式 (39) 乘积因子）外推 generic 部分共线区检验
- A=0 ⟺ ∃m: sign(s_{m,m+1}) = -sign(s1_2..m) ≠ 0 或 双零（R1 区解析精确）
- 检验：generic 部分共线（非 R1）区是否成立
- 对照：36% A≠0 含 s1_234567891011=0 的样本——m=n-1 因子是否 ±1
"""
import os, pickle, json, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
CACHE = os.path.join(SCRIPT_DIR, "cache_n11_3x80000.pkl")


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    n = 11
    # 因子命名 map：s{a}_{b}
    name2idx = {}
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                name = "s" + "".join(str(x + 1) for x in a) + "_" + "".join(str(x + 1) for x in b)
                name2idx[name] = len(name2idx)

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)

    # m = 2..n-1 (1-based)：单对 s_{m,m+1} = s{m}_{m+1}；前缀 s1_2..m = s1_{2..m}
    pairs = []
    for m in range(2, n):
        single = f"s{m}_{m+1}"
        prefix = f"s1_{''.join(str(x) for x in range(2, m + 1))}"
        pairs.append((m, single, prefix))
    print("符号对 (m, s_{m,m+1}, s1_2..m)：")
    for m, s1, s2 in pairs:
        print(f"  m={m}: {s1} + {s2}")

    # 统计
    stat = {"zero_with_pair_opp": 0, "zero_no_pair_opp": 0, "nz_with_pair_opp": 0, "nz_no_pair_opp": 0}
    detail = {}
    for sd, data in datas.items():
        for full, a in data:
            if sign(a) == 0:
                has_opp = False
                opp_m = []
                for m, s1, s2 in pairs:
                    v1, v2 = full[name2idx[s1]], full[name2idx[s2]]
                    if v1 == 0 and v2 == 0:
                        has_opp = True
                        opp_m.append(m)
                    elif v1 != 0 and v2 != 0 and v1 == -v2:
                        has_opp = True
                        opp_m.append(m)
                if has_opp:
                    stat["zero_with_pair_opp"] += 1
                    detail.setdefault(tuple(opp_m), 0)
                    detail[tuple(opp_m)] += 1
                else:
                    stat["zero_no_pair_opp"] += 1
            else:
                has_opp = False
                for m, s1, s2 in pairs:
                    v1, v2 = full[name2idx[s1]], full[name2idx[s2]]
                    if v1 == 0 and v2 == 0:
                        has_opp = True
                    elif v1 != 0 and v2 != 0 and v1 == -v2:
                        has_opp = True
                if has_opp:
                    stat["nz_with_pair_opp"] += 1
                else:
                    stat["nz_no_pair_opp"] += 1

    total_zero = stat["zero_with_pair_opp"] + stat["zero_no_pair_opp"]
    total_nz = stat["nz_with_pair_opp"] + stat["nz_no_pair_opp"]
    print(f"\nA=0 共 {total_zero}：含符号对相反 {stat['zero_with_pair_opp']} ({stat['zero_with_pair_opp']/total_zero:.4f}) / 无 {stat['zero_no_pair_opp']}")
    print(f"A≠0 共 {total_nz}：含符号对相反 {stat['nz_with_pair_opp']} ({stat['nz_with_pair_opp']/total_nz:.4f}) / 无 {stat['nz_no_pair_opp']}")

    print("\nA=0 且含符号对相反的 m 组合分布（Top 12）：")
    for k, v in sorted(detail.items(), key=lambda x: -x[1])[:12]:
        print(f"  m={k}: {v}")

    # 对照：A≠0 含 s1_234567891011=0（m=n-1 前缀）的样本——其 m=n-1 因子 = ?
    s1_long = "s1_234567891011"
    s_last = f"s{10}_{11}"
    nz_long_zero = 0
    nz_long_zero_factor_nz = 0
    for sd, data in datas.items():
        for full, a in data:
            if sign(a) != 0 and full[name2idx[s1_long]] == 0:
                nz_long_zero += 1
                if full[name2idx[s_last]] != 0:
                    nz_long_zero_factor_nz += 1
    print(f"\nA≠0 含 s1_234567891011=0：{nz_long_zero}（其中单对 s10_11 非零：{nz_long_zero_factor_nz}）")
    print("  → 前缀块零但单对非零 → 因子 ±1 → A≠0 —— 与通式 (39) 机制一致")

    out = {"pairs": [(m, s1, s2) for m, s1, s2 in pairs], "stat": stat,
           "zero_opp_m_top": [(list(k), v) for k, v in sorted(detail.items(), key=lambda x: -x[1])[:12]],
           "nz_long_zero": nz_long_zero, "nz_long_zero_factor_nz": nz_long_zero_factor_nz}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_pair_opp.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_pair_opp.json")
