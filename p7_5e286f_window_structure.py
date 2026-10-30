# -*- coding: utf-8 -*-
"""
p7_5e286f_window_structure.py — 窗口结构判别 + δ∞ 左端落位 + n_max³ 窗口连接升格
（P7-5e-286f，2026-10-30）

承接 286e（五系数全窗口算术谱闭合），攻剩余观察级第一项：δ∞ 分母"为何窗口左端"。

  M1 窗口四元组结构判别：W(k)=[k(k−1), k²−1, k², k²+1] 中，
     ★ 唯一的连续整数乘积 = 左端 k(k−1)（(k−1)(k+1)=k²−1 因子差 2 非连续；
        k²=k·k 自乘非相邻；k²+1 一般非乘积形态）
     → δ∞（五系数中唯一"分母=乘积"形态 1/[k(k−1)]）唯一落位窗口左端
  M2 分母形态-来源-系数一一对应谱：乘积（δ∞）/2 幂（C）/2·立方（D/E）
     ↔ 窗口左端/窗口和/n_max³ ↔ 初等代数三种基本增长形态
  M3 ★ n_max³ 窗口连接代数升格：恒等 (k+2)³ − k(2k²−3) = (8−k)(k+1)²
     （n_max³ = k·(窗口和−3) ⟺ 1000=8·125=8·(2·64−3)，k=8 唯一因式分解）
  M4 E1/E2 引用 286e 证伪结论（素数性重述反例 k=10/16/20，维持观察级登记）

输出：p7_5e286f_window_structure_result.json
"""
import json
import sympy as sp

k = sp.Symbol("k", integer=True)

# ---------- M1 窗口四元组结构判别 ----------
def window(kk):
    return {"left": kk * kk - kk, "m1": kk * kk - 1, "center": kk * kk, "plus1": kk * kk + 1}

def is_consecutive_product(n):
    """n = m(m+1) 对某正整数 m？"""
    if n <= 0:
        return False
    d = sp.sqrt(1 + 4 * n)
    # m = (−1 + √(1+4n))/2 为整数
    return d.is_integer and sp.simplify((sp.sqrt(1 + 4 * n) - 1) / 2).is_integer

M1_rows = []
M1_pass = True
for kk in range(4, 13):
    w = window(kk)
    items = {"left": w["left"], "m1": w["m1"], "center": w["center"], "plus1": w["plus1"]}
    cons = {name: bool(is_consecutive_product(val)) for name, val in items.items()}
    unique_left = cons["left"] and not (cons["m1"] or cons["center"] or cons["plus1"])
    M1_pass = M1_pass and unique_left
    M1_rows.append({"k": kk, "window": items, "consecutive_product": cons,
                    "unique_consecutive_product_is_left": unique_left})

# 数学核验：m1=(k−1)(k+1) 因子差 2 非连续（k≥2）；center=k·k 差 0 非相邻；plus1=k²+1 一般非乘积
M1 = {
    "window_family": "W(k) = [k(k−1), k²−1, k², k²+1]",
    "structural_claims": {
        "left": "k(k−1) = (k−1)·k 连续整数乘积",
        "m1": "(k−1)(k+1) = k²−1 因子差 2，非连续乘积",
        "center": "k·k 自乘，非相邻整数乘积",
        "plus1": "k²+1 一般非乘积形态",
    },
    "k4_12_rows": M1_rows,
    "ALL_unique_left": bool(M1_pass),
    "interpretation": (
        "窗口四元组中唯一连续整数乘积 = 左端 k(k−1)；δ∞ 是五系数中唯一分母=乘积形态的系数"
        "（1/[k(k−1)]，其余为 2 幂/立方）→ δ∞ 唯一落位窗口左端 = 形态-位置唯一性判别。"
    ),
}

# ---------- M2 分母形态-来源-系数一一对应谱 ----------
M2 = {
    "spectrum": [
        {"form": "连续乘积 k(k−1)", "source": "窗口左端", "coef": "δ∞=1/56", "growth": "二次乘积"},
        {"form": "2 幂 2^(k−1)", "source": "窗口和 2k²（唯一重合点 k=8）", "coef": "C=13/128", "growth": "指数"},
        {"form": "2·立方 2(k+2)³", "source": "n_max³（16(k−3)³ 唯一重合）", "coef": "D/E=41,39/2000", "growth": "立方"},
    ],
    "one_to_one": "三种初等代数增长形态（乘积/指数/立方）各对应一个系数，来源窗口左端/窗口和/n_max³——一一对应",
}

# ---------- M3 ★ n_max³ 窗口连接代数升格 ----------
# 恒等：(k+2)³ − k(2k²−3) = (8−k)(k+1)²
lhs = sp.expand((k + 2) ** 3 - k * (2 * k * k - 3))
rhs = sp.expand((8 - k) * (k + 1) ** 2)
M3_identity = sp.simplify(lhs - rhs) == 0
factored = sp.factor((k + 2) ** 3 - k * (2 * k * k - 3))
# 唯一正整数解 k=8：枚举
sol_nmax_window = [kk for kk in range(2, 21) if (kk + 2) ** 3 == kk * (2 * kk * kk - 3)]
k8_check = {"nmax_cube": 10 ** 3, "k*(window_sum−3)": 8 * (2 * 64 - 3), "hit": 10 ** 3 == 8 * (2 * 64 - 3)}
M3 = {
    "identity": "(k+2)³ − k(2k²−3) = (8−k)(k+1)²",
    "identity_check": bool(M3_identity),
    "factored": str(factored),
    "solutions_k2_20": sol_nmax_window,
    "k8_check": k8_check,
    "interpretation": (
        "n_max³ = k·(窗口和−3) 的唯一正整数解 k=8（因式分解 (8−k)(k+1)²，(k+1)²>0 ∀k≥2）；"
        "k=8 处 1000=8·125=8·(2·64−3)——n_max³ 与窗口的代数连接升格（原 263 条件 5³=128−3 的乘积化表述）"
    ),
}

# ---------- M4 E1/E2 引用 286e 证伪 ----------
M4 = {
    "reference": "286e M5：E1 集合 {3,5,7,13} ≠ 『2k−3 为奇素数』判据（反例 k=10/16/20：17、7 均奇素但 17∉E1）",
    "status": "E1/E2 家族资格 = 判别设计（唯一性所需），维持观察级登记",
}

# ---------- PYCHECK 先证伪（对应 Lean §8 定理） ----------
pycheck = {
    "nmax_window_identity": {
        "claim": "∀k：(k+2)³ − k(2k²−3) = (8−k)(k+1)²",
        "sympy_pass": bool(M3_identity),
        "range_pass": all(
            (kk + 2) ** 3 - kk * (2 * kk * kk - 3) == (8 - kk) * (kk + 1) ** 2
            for kk in range(-20, 21)
        ),
    },
    "nmax_cube_unique": {
        "claim": "∀k≥2：(k+2)³ = k(2k²−3) → k=8",
        "enum_pass": sol_nmax_window == [8],
        "solutions": sol_nmax_window,
    },
    "window_adjacent_uniqueness": {
        "claim": "窗口四元组唯一连续乘积 = 左端（k=4..12 全验证）",
        "enum_pass": bool(M1_pass),
    },
}
PYCHECK_PASS = (
    pycheck["nmax_window_identity"]["sympy_pass"]
    and pycheck["nmax_window_identity"]["range_pass"]
    and pycheck["nmax_cube_unique"]["enum_pass"]
    and pycheck["window_adjacent_uniqueness"]["enum_pass"]
)

result = {
    "title": "P7-5e-286f 窗口结构判别 + δ∞ 左端落位 + n_max³ 窗口连接升格",
    "M1_window_structure": M1,
    "M2_form_source_coef_spectrum": M2,
    "M3_nmax_window_algebra": M3,
    "M4_E1E2_reference": M4,
    "PYCHECK": pycheck,
    "M1_PASS": M1_pass,
    "M3_PASS": bool(M3_identity) and sol_nmax_window == [8] and k8_check["hit"],
    "PYCHECK_PASS": PYCHECK_PASS,
    "ALL_PASS": M1_pass and bool(M3_identity) and sol_nmax_window == [8] and k8_check["hit"] and PYCHECK_PASS,
}

out = r"E:\workspace\hyper-resolution\p7_5e286f_window_structure_result.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print("M1_PASS =", M1_pass)
print("M3_PASS =", bool(M3_identity) and sol_nmax_window == [8] and k8_check["hit"])
print("PYCHECK_PASS =", PYCHECK_PASS)
print("ALL_PASS =", result["ALL_PASS"])
print("factored =", factored)
print("solutions k2_20 =", sol_nmax_window)
print("result json ->", out)
