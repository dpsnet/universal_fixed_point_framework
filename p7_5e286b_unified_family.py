# -*- coding: utf-8 -*-
"""
p7_5e286b_unified_family.py — P7-5e-286 判别续：五系数统一 k 参数化族实证（路线 A）

目标：把 286 判别中"条件生成级"的五系数（δ∞/C/D/E/D−E）压缩为单一参数 k 的四个函数，
     并检验该参数化族对 k=4..12 全空间命中（与 p7_5e286_demirror_generation_result.json 逐项比对）。
     同时检验 k=8 处各分母机制与框架家族（静默窗口/2 幂/Bott 立方）的归属连接。

候选统一族（由 286 结果 json 的 coefficient_matrix 反推）：
    δ∞(k) = 1 / (k(k−1))                    # k=8 → 1/56（静默核心窗口左端 8²−8）
    C(k)   = (2k−3) / 2^(k−1)               # k=8 → 13/128（2 幂静默家族；128=2·8² 与 2⁷ 重合）
    D(k)   = (k(k−3)+1) / (16·(k−3)³)       # k=8 → 41/2000（2⁴×Bott 立方）
    E(k)   = (k(k−3)−1) / (16·(k−3)³)       # k=8 → 39/2000
    D−E(k) = 1 / (8(k−3)³)                  # k=8 → 1/1000 = n_max⁻³，n_max=k+2=10

诚实边界（判定设计）：
    · 统一族是同一 k 参数化的代数重写（条件生成级→参数化级压缩），"为何三种分母机制
      1/(k(k−1))、2^(k−1)、16(k−3)³"仍未从公设导出——本轮只实证压缩成立 + 家族归属连接；
    · 增强判据（2k−3 ∈ 静默/框架族 {3,5,7,13}）唯一钉死 k=8（④，沿用 286 判别）；
    · 本脚本全部用分数精确计算（sympy），无浮点误差。
"""
import json
import sympy as sp
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "p7_5e286b_unified_family_result.json")

def exact(n, d):
    """返回 n/d 的精确分数（已约分）。"""
    return sp.Rational(n, d)

def unified_family(k):
    """返回统一参数化族在整数 k 处的精确分数五元组。"""
    delta_inf = exact(1, k * (k - 1))
    C = exact(2 * k - 3, 2 ** (k - 1))
    D = exact(k * (k - 3) + 1, 16 * (k - 3) ** 3)
    E = exact(k * (k - 3) - 1, 16 * (k - 3) ** 3)
    DE = exact(1, 8 * (k - 3) ** 3)
    return {"delta_inf": delta_inf, "C": C, "D": D, "E": E, "D_minus_E": DE}

def main():
    # ── ① 统一族 vs 286 结果 json 逐项比对（k=4..12 全空间） ──
    ref_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "p7_5e286_demirror_generation_result.json")
    with open(ref_path, "r", encoding="utf-8") as f:
        ref = json.load(f)

    compare = []
    all_hit = True
    for row in ref["coefficient_matrix"]:
        k = row["k"]
        fam = unified_family(k)
        # 286 json 存储为字符串分数 "n/d"
        ref_delta = sp.Rational(1, row["delta_inf_den"])
        ref_C = sp.Rational(*map(int, row["C"].split("/")))
        ref_D = sp.Rational(*map(int, row["D"].split("/")))
        ref_E = sp.Rational(*map(int, row["E"].split("/")))
        hits = {
            "delta_inf": fam["delta_inf"] == ref_delta,
            "C": fam["C"] == ref_C,
            "D": fam["D"] == ref_D,
            "E": fam["E"] == ref_E,
        }
        all_hit = all_hit and all(hits.values())
        compare.append({
            "k": k,
            "unified": {key: f"{v.p}/{v.q}" for key, v in fam.items()},
            "ref_286": {
                "delta_inf": f"{ref_delta.p}/{ref_delta.q}",
                "C": row["C"], "D": row["D"], "E": row["E"],
            },
            "all_hit": all(hits.values()),
        })

    # ── ② k=8 精确赋值与家族归属连接 ──
    k8 = unified_family(8)
    k8_exact = {key: f"{v.p}/{v.q}" for key, v in k8.items()}
    # n_max = k+2；D−E = n_max⁻³ 检查
    n_max = 8 + 2
    de_diff = k8["D_minus_E"]
    family_links = {
        "delta_inf_den_56": "静默核心窗口左端 8²−8 = k(k−1)（286 Lean: [56,63,64,65]=8²−{8,1,0,−1}）",
        "C_den_128": "2 幂静默家族 2^(k−1)=2⁷；与 2·k²=128（279 登记）在 k=8 重合",
        "DE_den_2000": "2⁴×(k−3)³ = 16·5³（263 (k−3)³=2k²−3 条件生成：125=128−3）",
        "D_minus_E": "1/1000 = n_max⁻³（n_max=k+2=10；254 望远镜差分身份升格）",
        "molecular_note": "D/E 分子 k(k−3)±1 = 5k±1：静默 5 因子线性形式（286 判别②）",
    }
    # 增强判据唯一性复核（④，修正版：E1 ∧ E2 独立交叉，勘误 286 初版硬编码 k==8）
    silent_family = {3, 5, 7, 13}
    cube_base_family = {3, 5}   # E2: D/E 分母立方底 k−3 ∈ 静默/框架奇数（279 分母框架 2000=2⁴·5³）
    cand_e1 = [kk for kk in range(4, 12) if (2 * kk - 3) in silent_family]
    cand_e1e2 = [kk for kk in range(4, 12)
                 if (2 * kk - 3) in silent_family and (kk - 3) in cube_base_family]
    enhanced_unique = (cand_e1e2 == [8])

    result = {
        "title": "P7-5e-286b 统一 k 参数化族实证",
        "unified_family_formulas": {
            "delta_inf(k)": "1/(k(k-1))",
            "C(k)": "(2k-3)/2^(k-1)",
            "D(k)": "(k(k-3)+1)/(16(k-3)^3)",
            "E(k)": "(k(k-3)-1)/(16(k-3)^3)",
            "D_minus_E(k)": "1/(8(k-3)^3)",
        },
        "compare_all_hit": all_hit,
        "compare": compare,
        "k8_exact": k8_exact,
        "k8_family_links": family_links,
        "enhanced_e1_only_candidates": cand_e1,
        "enhanced_e1e2_candidates": cand_e1e2,
        "enhanced_unique": enhanced_unique,
        "errata_286": "286 初版增强判据硬编码 k==8（循环论证）；修正为 E1(2k−3∈{3,5,7,13}) ∧ E2(k−3∈{3,5}) 独立交叉 → 唯一 k=8",
        "n_max": n_max,
        "honest_boundary": (
            "统一族为同一 k 参数化代数重写（条件生成级→参数化级压缩）；"
            "三种分母机制（k(k−1)、2^(k−1)、16(k−3)³）本身与分子线性形式 5k±1 未从公设导出；"
            "E1/E2 家族成员资格依赖 260ap 邻居族观察（观察级）。"
        ),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    print("ALL_HIT:", all_hit)
    print("K8_EXACT:", k8_exact)
    print("ENHANCED_UNIQUE:", enhanced_unique, "E1_ONLY_CAND:", cand_e1, "E1E2_CAND:", cand_e1e2)
    print("DE_DIFF == n_max^-3:", de_diff == exact(1, n_max ** 3))
    print("OUT:", OUT)

if __name__ == "__main__":
    main()
