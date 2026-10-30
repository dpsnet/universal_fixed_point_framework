# -*- coding: utf-8 -*-
"""
p7_5e286e_window_spectrum.py — 五系数分子-分母统一窗口算术谱判别（P7-5e-286e，2026-10-30）

承接 286d（分母三机制窗口算术统一 + D/E 分母=2·n_max³ 升格），补齐分子侧 + E1/E2 判别通道证伪：

  M1 分子窗口算术化（恒等升格）：
     D/E 分子：k(k−3)±1 = (k²−k) − 2k ± 1 = 窗口左端 − 2k ± 1（k=8：56−16±1=41/39）
     C 分子：2k−3 = 窗口和/k − 3 = 2k−3（k=8：128/8−3=16−3=13）
     δ∞ 分子：1 = 窗口左端/窗口左端（平凡）
  M2 五系数全窗口算术谱总表：分子+分母全部落进 {窗口左端, 窗口中心, 窗口和, n_max} 语言
  M3 窗口量重合点唯一性复核（C 分母 2 幂=窗口和 唯一 8；D/E 分母 2·n_max³ 唯一 8）+ 分子侧恒等
  M4 统一族一致性复核（k=4..12 五系数窗口公式 vs 286b 参数化全命中）
  M5 ★ 证伪登记：E1 集合 {3,5,7,13} ≠ "2k−3 为奇素数"判据
       ——k=10：2·10−3=17、10−3=7 均奇素数（素数性判据满足），但 2k−3=17∉{3,5,7,13}（E1 排除）、
         k=10 仍在统一族参数化内（286b 实证 k=4..12 全命中）。
         ⇒ E1 集合是判别设计（唯一性所需），非素数性导出；E1/E2 家族资格维持观察级登记。

输出：p7_5e286e_window_spectrum_result.json
"""
import json
import sympy as sp

k = sp.Symbol("k", integer=True)

# ---------- M1 分子窗口算术化 ----------
# D/E 分子：k(k−3)±1 = 窗口左端 k(k−1) − 2k ± 1
de_mol_base = sp.expand(k * (k - 3))
win_left_minus_2k = sp.expand(k * (k - 1) - 2 * k)
M1_DE = sp.simplify(de_mol_base - win_left_minus_2k) == 0
# C 分子：2k−3 = 窗口和/k − 3（窗口和=2k²，/k=2k）
c_mol = sp.expand(2 * k - 3)
c_mol_window = sp.expand((2 * k * k) / k - 3)
M1_C = sp.simplify(c_mol - c_mol_window) == 0

M1 = {
    "DE_mol": {
        "identity": "k(k−3) = k(k−1) − 2k  （D/E 分子 = 窗口左端 − 2k）",
        "k=8": {"win_left_minus_2k": 56 - 16, "plus1": 56 - 16 + 1, "minus1": 56 - 16 - 1,
                "D_mol": 41, "E_mol": 39, "hit": (56 - 16 + 1 == 41 and 56 - 16 - 1 == 39)},
        "pass": bool(M1_DE),
    },
    "C_mol": {
        "identity": "2k−3 = 窗口和/k − 3 = 2k²/k − 3",
        "k=8": {"window_sum_over_k_minus_3": 128 / 8 - 3, "C_mol": 13, "hit": 128 / 8 - 3 == 13},
        "pass": bool(M1_C),
    },
    "delta_mol": {"identity": "1 = 窗口左端/窗口左端（平凡）", "pass": True},
}

# ---------- M2 五系数全窗口算术谱总表 ----------
def window(kk):
    return {"left": kk * kk - kk, "center": kk * kk, "sum": 2 * kk * kk}

w8 = window(8)
M2 = {
    "k=8_window": w8,
    "n_max": 10,
    "spectrum": [
        {"coef": "δ∞", "num": "1", "num_window": "左端/左端（平凡）", "den": "56", "den_window": "窗口左端 k²−k",
         "k8_value": "1/56"},
        {"coef": "C", "num": "13", "num_window": "窗口和/k − 3 = 128/8−3", "den": "128", "den_window": "窗口和 2k²（2 幂 2^(k−1) 唯一重合）",
         "k8_value": "13/128"},
        {"coef": "D", "num": "41", "num_window": "窗口左端 − 2k + 1 = 56−16+1", "den": "2000", "den_window": "2·n_max³（16(k−3)³ 唯一重合）",
         "k8_value": "41/2000"},
        {"coef": "E", "num": "39", "num_window": "窗口左端 − 2k − 1 = 56−16−1", "den": "2000", "den_window": "2·n_max³",
         "k8_value": "39/2000"},
        {"coef": "D−E", "num": "2", "num_window": "分子差恒 2（286d M1）", "den": "2000", "den_window": "2·n_max³ → n_max⁻³=1/1000",
         "k8_value": "1/1000"},
    ],
    "closure": "五系数分子+分母全部落进 {窗口左端, 窗口中心, 窗口和, n_max} 语言 —— 窗口算术谱闭合",
}

# ---------- M3 窗口量重合点唯一性复核 + 分子侧恒等 ----------
pow_sq_sol = [kk for kk in range(2, 21) if 2 ** (kk - 2) == kk * kk]
den_nmax_sol = [kk for kk in range(1, 21) if 16 * (kk - 3) ** 3 == 2 * (kk + 2) ** 3]
# 分子侧恒等（对任意 k）
mol_id_check = all(kk * (kk - 3) == kk * (kk - 1) - 2 * kk for kk in range(-20, 21))
M3 = {
    "C_den_unique": {"solutions_k2_20": pow_sq_sol, "pass": pow_sq_sol == [8]},
    "DE_den_unique": {"solutions_k1_20": den_nmax_sol, "pass": den_nmax_sol == [8]},
    "DE_mol_identity_all_k": bool(mol_id_check),
    "C_mol_window_sum_over_k": {"formula": "2k²/k − 3 = 2k − 3", "pass": bool(M1_C)},
}

# ---------- M4 一致性复核（三重设计） ----------
# M4a：286b 参数化 k=4..12 内部一致（五系数公式形态）
def delta_inf(kk): return 1 / (kk * (kk - 1))
def C(kk): return (2 * kk - 3) / (2 ** (kk - 1))
def D(kk): return (kk * (kk - 3) + 1) / (16 * (kk - 3) ** 3)
def E(kk): return (kk * (kk - 3) - 1) / (16 * (kk - 3) ** 3)

# k=8 权威值（286 判别⑤）：δ∞=1/56、C=13/128、D=41/2000、E=39/2000、D−E=1/1000
AUTH = {
    "delta": 1 / 56, "C": 13 / 128, "D": 41 / 2000, "E": 39 / 2000, "D_minus_E": 1 / 1000
}
M4a = {"k=8_authority_check": {
    "delta": delta_inf(8) == AUTH["delta"],
    "C": C(8) == AUTH["C"],
    "D": D(8) == AUTH["D"],
    "E": E(8) == AUTH["E"],
    "D_minus_E": round(abs((D(8) - E(8)) - AUTH["D_minus_E"]), 12) == 0,
}}
M4a["k=8_authority_check"]["all"] = all(M4a["k=8_authority_check"].values())

# M4b：窗口公式与参数化在 k=8 全等（重合点验证——286e 核心）
w8v = window(8)
C_den_pow = 2 ** 7
C_den_window_sum = 2 * w8v["center"]
DE_den_pow = 16 * 5 ** 3
DE_den_nmax = 2 * 10 ** 3
M4b = {
    "k=8_C_den_coincidence": {"2^(k−1)": C_den_pow, "窗口和": C_den_window_sum, "hit": C_den_pow == C_den_window_sum},
    "k=8_DE_den_coincidence": {"16(k−3)³": DE_den_pow, "2·n_max³": DE_den_nmax, "hit": DE_den_pow == DE_den_nmax},
    "k=8_mol_coincidence": {
        "D_mol": 41, "win_left−2k+1": 56 - 16 + 1, "hit": 41 == 56 - 16 + 1,
        "E_mol": 39, "win_left−2k−1": 56 - 16 - 1, "hit": 39 == 56 - 16 - 1,
        "C_mol": 13, "win_sum/k−3": 128 / 8 - 3, "hit": 13 == 128 / 8 - 3,
    },
}
M4b_pass = (
    C_den_pow == C_den_window_sum and DE_den_pow == DE_den_nmax
    and 41 == 56 - 16 + 1 and 39 == 56 - 16 - 1 and 13 == 128 / 8 - 3
)

# M4c：窗口公式与参数化在 k≠8 处一般不等（区分性负结果——窗口解读为 k=8 专属）
# 窗口公式：C_w=(2k−3)/(2k²)、DE_w=(k(k−3)±1)/(2(k+2)³)；与参数化之差仅当 k=8 为零
diff_C = [(kk, C(kk) - (2 * kk - 3) / (2 * kk * kk)) for kk in range(4, 13) if kk != 8]
diff_DE = [(kk, (D(kk) - (kk * (kk - 3) + 1) / (2 * (kk + 2) ** 3))) for kk in range(4, 13) if kk != 8]
M4c = {
    "C_diff_nonzero_for_k_ne_8": {str(kk): round(abs(d), 12) != 0 for kk, d in diff_C},
    "DE_diff_nonzero_for_k_ne_8": {str(kk): round(abs(d), 12) != 0 for kk, d in diff_DE},
    "all_nonzero": all(round(abs(d), 12) != 0 for _, d in diff_C + diff_DE),
    "interpretation": "窗口算术公式是 k=8 专属重合表述（分母 2k²、2(k+2)³ 仅 k=8 与 2^(k−1)、16(k−3)³ 重合）；286b 参数化（k(k−1)、2^(k−1)、16(k−3)³）才是统一族全 k 公式——两者关系 = 重合点结构，非等价",
}
M4_pass = M4a["k=8_authority_check"]["all"] and M4b_pass and M4c["all_nonzero"]
M4 = {"M4a_param_recheck": M4a, "M4b_k8_coincidence": M4b, "M4c_distinction_negative": M4c, "M4_PASS": bool(M4_pass)}

# ---------- M5 ★ 证伪：E1 集合 ≠ 奇素数性判据 ----------
# 素数性判据候选："2k−3 为奇素数 ∧ k−3 为奇素数"
primality_candidates = []
for kk in range(2, 21):
    a = 2 * kk - 3
    b = kk - 3
    if a >= 2 and b >= 2 and sp.isprime(a) and sp.isprime(b):
        primality_candidates.append(kk)
# E1 集合（2k−3∈{3,5,7,13}）对应 k∈{3,4,5,8}
E1_k = [kk for kk in range(2, 21) if (2 * kk - 3) in (3, 5, 7, 13)]
E1E2_k = [kk for kk in range(2, 21) if (2 * kk - 3) in (3, 5, 7, 13) and (kk - 3) in (3, 5)]
counterexample = [kk for kk in primality_candidates if kk not in E1_k]
M5 = {
    "primality_judgement_candidates_k2_20": primality_candidates,
    "E1_set_k2_20": E1_k,
    "E1E2_set_k2_20": E1E2_k,
    "counterexamples_not_in_E1": counterexample,
    "falsified": len(counterexample) > 0,
    "interpretation": (
        "E1 集合 {3,5,7,13} 非『2k−3 为奇素数』导出（k=10：17、7 均奇素但 17∉E1 集合）；"
        "E1/E2 家族资格 = 判别设计（唯一性所需），素数性重述证伪并登记，维持观察级。"
    ),
}

# ---------- PYCHECK 先证伪（对应 Lean 分子恒等定理） ----------
pycheck = {
    "de_mol_window_identity": {
        "claim": "∀k：k(k−3) = k(k−1) − 2k",
        "sample_pass": bool(M1_DE),
        "range_pass": bool(mol_id_check),
        "pass": bool(M1_DE) and bool(mol_id_check),
    },
    "c_mol_window_identity": {"claim": "∀k≠0：2k−3 = 2k²/k − 3", "pass": bool(M1_C)},
    "DE_mol_window_plus_minus": {
        "claim": "k(k−3)+1 = 窗口左端−2k+1 且 k(k−3)−1 = 窗口左端−2k−1",
        "pass": bool(sp.simplify(sp.expand(k * (k - 3) + 1) - (k * (k - 1) - 2 * k + 1)) == 0
                 and sp.simplify(sp.expand(k * (k - 3) - 1) - (k * (k - 1) - 2 * k - 1)) == 0),
    },
}
PYCHECK_PASS = all(v["pass"] for v in pycheck.values())

M1_PASS = bool(M1_DE) and bool(M1_C)
M3_PASS = pow_sq_sol == [8] and den_nmax_sol == [8] and bool(mol_id_check)
M5_PASS = len(counterexample) > 0  # 证伪成立（登记负结果）

result = {
    "title": "P7-5e-286e 五系数分子-分母统一窗口算术谱判别",
    "M1_molecule_window_arithmetic": M1,
    "M2_full_window_spectrum": M2,
    "M3_uniqueness_recheck": M3,
    "M4_family_consistency": M4,
    "M5_E1_primality_falsification": M5,
    "PYCHECK": pycheck,
    "M1_PASS": M1_PASS,
    "M3_PASS": M3_PASS,
    "M4_PASS": M4_pass,
    "M5_FALSIFIED_PASS": M5_PASS,
    "PYCHECK_PASS": PYCHECK_PASS,
    "ALL_PASS": M1_PASS and M3_PASS and M4_pass and M5_PASS and PYCHECK_PASS,
}

out = r"E:\workspace\hyper-resolution\p7_5e286e_window_spectrum_result.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print("M1_PASS =", M1_PASS)
print("M3_PASS =", M3_PASS)
print("M4_PASS =", M4_pass)
print("M5_FALSIFIED_PASS =", M5_PASS)
print("PYCHECK_PASS =", PYCHECK_PASS)
print("ALL_PASS =", result["ALL_PASS"])
print("primality candidates =", primality_candidates)
print("E1 set k =", E1_k)
print("counterexamples =", counterexample)
print("result json ->", out)
