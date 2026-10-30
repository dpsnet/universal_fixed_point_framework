# -*- coding: utf-8 -*-
"""
p7_5e286d_denominator_origin.py — 分母三机制形态溯源判别（P7-5e-286d，2026-10-30）

承接 286c（分子线性化升格 + 分母连接登记），攻坚 286b 诚实边界剩余项：
"三种分母机制（k(k-1)、2^(k-1)、16(k-3)³）为何形态未从公设导出"。

  M1 D/E 分母形态代数升格：D/E 分子差恒 2（无条件恒等）→ 若 D−E 要求 = n_max⁻³
     （n_max=k+2），分母必须 = 2·n_max³ = 2(k+2)³。判别：
     16(k-3)³ = 2(k+2)³  ⟺  8(k-3)³ = (k+2)³ ⟺ k=8 唯一（286③/T4 已证）。
     结论：D/E 分母 16(k-3)³ 的形态 = "分子差 2" ∧ "D−E=n_max⁻³ 要求" 的代数推论
       （k=8 处 16·5³=2000=2·10³），非独立观察。286b 诚实边界三项 → 仅剩
       δ∞/C 分母形态与 E1/E2 家族资格为观察级。
  M2 三分母统一为窗口算术量：δ∞ 分母 = 窗口左端 k²−k；C 分母 = 窗口和 2k²
     （与 2 幂 2^(k-1) 唯一重合 k=8）；D/E 分母 = 2·n_max³（n_max=k+2）。
     k=8 数值表：56=窗口左端、128=2·窗口中心=2·8²、2000=2·n_max³=2·10³。
  M3 重合点唯一性 + 负结果：2^(k-2)=k² 枚举唯一 8；16(k-3)³=2(k+2)³ 枚举唯一 8；
     ★ 负结果：窗口左端 k(k-1) 与窗口和 2k² 无正整数交点（k(k+1)=0，根 {0,-1}）
       ——δ∞ 与 C 的窗口身份不同源（只有 C 的 2 幂形态在 k=8 落入窗口和）。
  PYCHECK 先证伪（先证伪再证明，模式 8）：mol_diff_two（分子差恒 2）、
     de_den_nmax_unique（16(k-3)³=2(k+2)³→k=8）、window_left_ne_sum（k(k-1)≠2k² ∀k≥1）。

输出：p7_5e286d_denominator_origin_result.json
"""
import json
import sympy as sp

k = sp.Symbol("k", integer=True)

# ---------- M1 D/E 分母 = 2·n_max³ 代数必然 ----------
# 分子差恒 2（无条件恒等）
diff = sp.expand((k * (k - 3) + 1) - (k * (k - 3) - 1))
diff_check = sp.simplify(diff - 2) == 0

# 16(k-3)³ = 2(k+2)³ 整数解（等价 8(k-3)³=(k+2)³）
sol_den_nmax = [kk for kk in range(1, 21) if 16 * (kk - 3) ** 3 == 2 * (kk + 2) ** 3]
k8_de_den = 16 * (8 - 3) ** 3
k8_two_nmax = 2 * (8 + 2) ** 3

M1 = {
    "mol_diff": {"formula": "(k(k-3)+1) - (k(k-3)-1)", "value": str(diff), "always_two": bool(diff_check)},
    "requirement": "D-E = 2/[16(k-3)³] = 1/[8(k-3)³]；要求 = n_max⁻³ = 1/(k+2)³",
    "den_equation": "16(k-3)³ = 2(k+2)³  <=>  8(k-3)³ = (k+2)³",
    "den_solutions_k1_20": sol_den_nmax,
    "k8_check": {"16*5³": k8_de_den, "2*10³": k8_two_nmax, "hit": k8_de_den == k8_two_nmax},
    "interpretation": (
        "D/E 分母 16(k-3)³ 形态 = 分子差恒 2 ∧ D−E=n_max⁻³ 要求的代数推论（k=8 处 2000=2·10³）；"
        "非独立观察。286b 诚实边界三项 → 仅剩 δ∞/C 分母形态与 E1/E2 家族资格为观察级。"
    ),
}

# ---------- M2 三分母统一为窗口算术量 ----------
def window(kk):
    return {"left": kk * kk - kk, "m1": kk * kk - 1, "center": kk * kk, "plus1": kk * kk + 1}

w8 = window(8)
M2 = {
    "k=8_window": w8,
    "n_max": 8 + 2,
    "delta_den": {"k(k-1)": 8 * 7, "window_left": w8["left"], "hit": 8 * 7 == w8["left"]},
    "C_den": {
        "2^(k-1)": 2 ** 7,
        "window_sum_2center": 2 * w8["center"],
        "hit": 2 ** 7 == 2 * w8["center"],
        "identity": "2^(k-1) = 2k²  <=>  2^(k-2) = k²（唯一重合点 k=8，M3 复核）",
    },
    "DE_den": {
        "16(k-3)³": 16 * 5 ** 3,
        "2*n_max³": 2 * 10 ** 3,
        "hit": 16 * 5 ** 3 == 2 * 10 ** 3,
    },
    "summary": {
        "delta": "δ∞ 分母 = 窗口左端 k²−k",
        "C": "C 分母 = 窗口和 2k²（=2·窗口中心；与 2 幂 2^(k−1) 唯一重合 k=8）",
        "DE": "D/E 分母 = 2·n_max³（n_max=k+2）",
    },
}

# ---------- M3 重合点唯一性 + 负结果 ----------
pow_sq_sol = [kk for kk in range(2, 21) if 2 ** (kk - 2) == kk * kk]
den_nmax_sol = sol_den_nmax  # 同上
# 负结果：窗口左端 = 窗口和 无正整数解
roots_left_sum = sp.solve(sp.Eq(k * (k - 1), 2 * k * k), k)
ne_check = all(r < 1 for r in roots_left_sum) and (len(roots_left_sum) >= 1)
M3 = {
    "C_pow_square_solutions_k2_20": pow_sq_sol,
    "DE_den_nmax_solutions_k1_20": den_nmax_sol,
    "window_left_eq_sum": {
        "equation": "k(k-1) = 2k²  <=>  k(k+1) = 0",
        "roots": sorted(int(r) for r in roots_left_sum),
        "no_positive_solution": bool(ne_check),
        "interpretation": "δ∞（窗口左端）与 C（窗口和）作为窗口量永不相交——不同源；仅 C 的 2 幂形态在 k=8 落入窗口和",
    },
}

# ---------- PYCHECK 先证伪（对应 Lean 三定理） ----------
pycheck = {
    "mol_diff_two": {"claim": "∀k：(k(k-3)+1)−(k(k-3)−1)=2", "pass": bool(diff_check)},
    "de_den_nmax_unique": {
        "claim": "∀k≥1：16(k-3)³=2(k+2)³ → k=8",
        "enum_pass": sol_den_nmax == [8],
        "solutions": sol_den_nmax,
    },
    "window_left_ne_sum": {
        "claim": "∀k≥1：k(k-1) ≠ 2k²",
        "enum_pass": all(kk * (kk - 1) != 2 * kk * kk for kk in range(1, 21)),
    },
}
PYCHECK_PASS = pycheck["mol_diff_two"]["pass"] and pycheck["de_den_nmax_unique"]["enum_pass"] and pycheck["window_left_ne_sum"]["enum_pass"]

# ---------- 结论 ----------
M1_PASS = bool(diff_check) and sol_den_nmax == [8] and k8_de_den == k8_two_nmax
M2_PASS = (
    8 * 7 == w8["left"] and 2 ** 7 == 2 * w8["center"] and 16 * 5 ** 3 == 2 * 10 ** 3
)
M3_PASS = pow_sq_sol == [8] and den_nmax_sol == [8] and bool(ne_check)

result = {
    "title": "P7-5e-286d 分母三机制形态溯源判别",
    "M1_DE_den_2nmax": M1,
    "M2_denominator_window_arithmetic": M2,
    "M3_uniqueness_and_negative": M3,
    "PYCHECK": pycheck,
    "M1_PASS": M1_PASS,
    "M2_PASS": M2_PASS,
    "M3_PASS": M3_PASS,
    "PYCHECK_PASS": PYCHECK_PASS,
    "ALL_PASS": M1_PASS and M2_PASS and M3_PASS and PYCHECK_PASS,
}

out = r"E:\workspace\hyper-resolution\p7_5e286d_denominator_origin_result.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print("M1_PASS =", M1_PASS)
print("M2_PASS =", M2_PASS)
print("M3_PASS =", M3_PASS)
print("PYCHECK_PASS =", PYCHECK_PASS)
print("ALL_PASS =", result["ALL_PASS"])
print("mol_diff =", diff)
print("den_nmax solutions =", sol_den_nmax)
print("window_left_eq_sum roots =", sorted(int(r) for r in roots_left_sum))
print("result json ->", out)
