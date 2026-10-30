# -*- coding: utf-8 -*-
"""
p7_5e286c_unified_origin.py — 统一族生成链连接判别（P7-5e-286c，2026-10-30）

承接 286b（统一 k 参数化族实证 ALL_HIT），攻坚 286b 诚实边界三项"未从公设导出"：
  M1 分子线性形式 5k±1 的代数升格：D/E 定义 k(k-3)±1 在 k=8 退化为 5k±1 的判别
     （k(k-3)+1-(5k+1)=k(k-8)，唯一正整数根 k=8 —— 5k±1 是 D/E 定义∧k=8 的推论，
       由 E2 立方底 k-3=5 驱动；非独立观察）
  M2 分母三机制生成链连接判别（观察级连接登记 + 数值判别）：
     · δ∞ 分母 k(k-1) = 静默核心窗口左端 k²-k（[56,63,64,65] 之 56）
     · C 分母 2^(k-1) = 窗口和 2k² 的重合点判别（2^(k-2)=k² 枚举唯一 k=8；
       289 vv_sumB：63+65=128=b₅）
     · D/E 分母 16(k-3)³ = 279 分母框架 2000=2⁴·5³；5³=125=128-3（263 条件
       (k-3)³=2k²-3 唯一整数解判别）
     · D-E=1/1000=n_max⁻³（n_max=k+2=10，286③ 代数已证，复核恒等）
  M3 一致性复核：统一族五公式 k=4..12 与 286 coefficient_matrix 逐项比对（继承 286b）

输出：p7_5e286c_unified_origin_result.json
"""
import json
import sympy as sp

k = sp.Symbol("k", integer=True)

# ---------- M1 分子线性化代数升格 ----------
roots_plus = sp.solve(sp.Eq(k * (k - 3) + 1, 5 * k + 1), k)
roots_minus = sp.solve(sp.Eq(k * (k - 3) - 1, 5 * k - 1), k)


def pos_unique(roots):
    return sorted({int(r) for r in roots if r >= 1})


M1 = {
    "plus_equation": "k(k-3)+1 = 5k+1  <=>  k^2-8k = k(k-8) = 0",
    "plus_all_roots": sorted(int(r) for r in roots_plus),
    "plus_unique_pos": pos_unique(roots_plus),
    "minus_equation": "k(k-3)-1 = 5k-1  <=>  k^2-8k = k(k-8) = 0",
    "minus_all_roots": sorted(int(r) for r in roots_minus),
    "minus_unique_pos": pos_unique(roots_minus),
    "interpretation": (
        "5k±1 线性化不是独立观察：D/E 定义 k(k-3)±1 与 k=8 的代数推论"
        "（k(k-3)±1-(5k±1)=k(k-8)，k≥1 唯一根 8；由 E2 立方底 k-3=5 驱动）。"
        "286b 诚实边界『分子线性形式 5k±1 未从公设导出』降级为：未导出的仅是 D/E 二次形式本身。"
    ),
}

# ---------- M2 分母三机制生成链连接判别 ----------
# (a) δ∞ 分母 k(k-1) = 窗口左端 k²-k（286 核心常数窗口 [56,63,64,65]，k=8 取 56）
k8 = 8
window = {"left": k8 * k8 - k8, "m1": k8 * k8 - 1, "center": k8 * k8, "plus1": k8 * k8 + 1}
M2a = {
    "k=8_window": window,
    "delta_den": k8 * (k8 - 1),
    "window_left_hit": k8 * (k8 - 1) == window["left"],
    "identity": "k(k-1) = k^2 - k（一般化：δ∞ 分母 = 静默核心窗口左端）",
}

# (b) C 分母 2^(k-1) = 窗口和 2k² 重合点判别：2^(k-1)=2k² <=> 2^(k-2)=k²，枚举 k=2..20
pow_sq_sol = [kk for kk in range(2, 21) if 2 ** (kk - 2) == kk * kk]
M2b = {
    "equation": "2^(k-1) = 2k^2  <=>  2^(k-2) = k^2",
    "solutions_k2_20": pow_sq_sol,
    "k8_check": 2 ** (8 - 2) == 8 * 8,
    "window_sum_289": {
        "b5": "63+65 = 128 = b_5（289 vv_sumB：b²-1 + b²+1 = 2b²，b=8）",
        "window_sum": window["m1"] + window["plus1"],
        "C_den": 2 ** (8 - 1),
        "hit": window["m1"] + window["plus1"] == 2 ** (8 - 1),
    },
    "note": "C 分母 2^(k-1) 与窗口和 2k² 的唯一重合点 k=8（枚举判别，观察级登记）",
}

# (c) D/E 分母 16(k-3)³ = 279 分母框架 2000 = 2⁴·5³；263 条件 (k-3)³=2k²-3 唯一整数解
cond263_sol = [kk for kk in range(1, 21) if (kk - 3) ** 3 == 2 * kk * kk - 3]
M2c = {
    "DE_den_k8": 16 * (8 - 3) ** 3,
    "factor_2000": "16·5³ = 2⁴·5³ = 2000",
    "hit_2000": 16 * (8 - 3) ** 3 == 2000,
    "c263_equation": "(k-3)^3 = 2k^2 - 3",
    "c263_solutions_k1_20": cond263_sol,
    "c263_k8_check": (8 - 3) ** 3 == 2 * 8 * 8 - 3,
    "note": "5³=125=128-3=2·8²-3（263 条件 (k-3)³=2k²-3 的唯一整数解 k=8，枚举判别）",
}

# (d) D-E = 1/1000 = n_max⁻³（n_max=k+2=10）
DminusE = sp.Rational(1, 8 * (8 - 3) ** 3)
nmax_cube = sp.Rational(1, (8 + 2) ** 3)
M2d = {
    "D_minus_E_exact": str(DminusE),
    "nmax_cube": str(nmax_cube),
    "hit": DminusE == nmax_cube,
    "n_max": 8 + 2,
    "note": "286③ 代数已证（8(k-3)³=(k+2)³ ⟺ k=8）；此处复核统一族恒等 D-E=1/[8(k-3)³]=1/(k+2)³ 于 k=8",
}

M2 = {"delta_den_window": M2a, "C_pow_square": M2b, "DE_den_279": M2c, "DE_nmax": M2d}

# ---------- M3 一致性复核：统一族五公式 vs 286 coefficient_matrix ----------
with open(r"E:\workspace\hyper-resolution\p7_5e286_demirror_generation_result.json",
          encoding="utf-8") as f:
    matrix = json.load(f)["coefficient_matrix"]


def unified(kk):
    return {
        "delta_inf_den": kk * (kk - 1),
        "C": sp.Rational(2 * kk - 3, 2 ** (kk - 1)),
        "D": sp.Rational(kk * (kk - 3) + 1, 16 * (kk - 3) ** 3),
        "E": sp.Rational(kk * (kk - 3) - 1, 16 * (kk - 3) ** 3),
    }


M3 = {"ALL_HIT": True, "mismatches": []}
for row in matrix:
    kk = row["k"]
    u = unified(kk)
    checks = {
        "delta_inf_den": row["delta_inf_den"] == u["delta_inf_den"],
        "C": row["C"] == str(u["C"]),
        "D": row["D"] == str(u["D"]),
        "E": row["E"] == str(u["E"]),
    }
    if not all(checks.values()):
        M3["ALL_HIT"] = False
        M3["mismatches"].append({"k": kk, "expected": row, "unified": {kk_: str(v) for kk_, v in u.items()}, **checks})

# ---------- 结论与落盘 ----------
M1_PASS = M1["plus_unique_pos"] == [8] and M1["minus_unique_pos"] == [8]
M2_PASS = (
    M2a["window_left_hit"] and M2b["k8_check"] and M2b["window_sum_289"]["hit"]
    and M2c["hit_2000"] and M2c["c263_k8_check"] and M2d["hit"]
    and pow_sq_sol == [8] and cond263_sol == [8]
)
M3_PASS = M3["ALL_HIT"]

result = {
    "title": "P7-5e-286c 统一族生成链连接判别",
    "M1_molecular_linearization": M1,
    "M2_denominator_links": M2,
    "M3_consistency": M3,
    "M1_PASS": M1_PASS,
    "M2_PASS": M2_PASS,
    "M3_PASS": M3_PASS,
    "ALL_PASS": M1_PASS and M2_PASS and M3_PASS,
}

out = r"E:\workspace\hyper-resolution\p7_5e286c_unified_origin_result.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print("M1_PASS =", M1_PASS)
print("M2_PASS =", M2_PASS)
print("M3_PASS =", M3_PASS)
print("ALL_PASS =", result["ALL_PASS"])
print("M1 plus_unique_pos =", M1["plus_unique_pos"], "| minus_unique_pos =", M1["minus_unique_pos"])
print("M2b 2^(k-2)=k^2 solutions(k=2..20) =", pow_sq_sol)
print("M2c 263 cond (k-3)^3=2k^2-3 solutions(k=1..20) =", cond263_sol)
print("result json ->", out)
