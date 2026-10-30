# -*- coding: utf-8 -*-
"""
p7_5e286b_pycheck.py — P7-5e-286b Lean 形式化先证伪（模式 8，逐字翻译）

拟形式化定理（DemirrorUniquenessIdentities.lean，承接 274 MirrorPairIdentities 链）：
  T1 axis_unique    : ∀ k : ℤ, k ≥ 1 → k*k - 3*k - 40 = 0 → k = 8
  T2 mol41_unique   : ∀ k : ℤ, k ≥ 1 → k*(k-3)+1 = 41 → k = 8
  T3 mol39_unique   : ∀ k : ℤ, k ≥ 1 → k*(k-3)-1 = 39 → k = 8
  T4 de_diff_unique : ∀ k : ℤ, k ≥ 1 → 8*(k-3)^3 = (k+2)^3 → k = 8
  T5 enhanced_unique: ∀ k : ℤ, 4 ≤ k → k ≤ 11 →
                        (2k-3=3 ∨ 2k-3=5 ∨ 2k-3=7 ∨ 2k-3=13) →
                        (k-3=3 ∨ k-3=5) → k = 8
  T6 k8_exact（统一族 k=8 特例，ℚ 分数恒等）

全部用 sympy 精确代数验证；残差 0 才投入证明。
"""
import sympy as sp

k = sp.symbols("k", integer=True)

results = {}

# ── T1/T2/T3：共同方程 k²−3k−40=0 的整数根 ──
roots = sp.solve(sp.Eq(k**2 - 3*k - 40, 0), k)
pos_roots = [r for r in roots if r >= 1]
results["T1_axis_unique"] = {
    "all_roots": [int(r) for r in roots],
    "pos_unique_8": pos_roots == [8],
}

# T2: k(k-3)+1 = 41 ⟺ k²−3k−40=0（sympy 展开验证）
expr2 = sp.expand(k * (k - 3) + 1 - 41)
results["T2_mol41_reduce"] = {"expanded_eq": str(expr2), "equals_quad": expr2 == k**2 - 3*k - 40}
# T3: k(k-3)-1 = 39 同理
expr3 = sp.expand(k * (k - 3) - 1 - 39)
results["T3_mol39_reduce"] = {"expanded_eq": str(expr3), "equals_quad": expr3 == k**2 - 3*k - 40}

# 数值枚举补充（k=1..2000 全扫描，直接验证蕴含式）
bad_t1 = [kk for kk in range(1, 2001) if kk**2 - 3*kk - 40 == 0 and kk != 8]
bad_t2 = [kk for kk in range(1, 2001) if kk*(kk-3)+1 == 41 and kk != 8]
bad_t3 = [kk for kk in range(1, 2001) if kk*(kk-3)-1 == 39 and kk != 8]
results["T1_T2_T3_enum_no_counterexample"] = (bad_t1 == [] and bad_t2 == [] and bad_t3 == [])

# ── T4：8(k−3)³ = (k+2)³ 唯一整数解 k=8 ──
poly4 = sp.expand(8*(k-3)**3 - (k+2)**3)
roots4 = sp.solve(sp.Eq(poly4, 0), k)
pos4 = [r for r in roots4 if r >= 1]
results["T4_de_diff"] = {
    "expanded": str(sp.expand(poly4)),
    "factor": str(sp.factor(poly4)),
    "all_roots": [int(r) for r in roots4],
    "pos_unique_8": pos4 == [8],
}
# 数值枚举 k∈[-200, 200]
bad_t4 = [kk for kk in range(-200, 201) if 8*(kk-3)**3 == (kk+2)**3 and kk != 8]
results["T4_enum_no_counterexample"] = (bad_t4 == [])

# ── T5：修正增强判据 E1∧E2 唯一 k=8 ──
E1 = lambda kk: 2*kk - 3 in (3, 5, 7, 13)
E2 = lambda kk: kk - 3 in (3, 5)
cand_e1 = [kk for kk in range(4, 12) if E1(kk)]
cand_e1e2 = [kk for kk in range(4, 12) if E1(kk) and E2(kk)]
results["T5_enhanced"] = {
    "E1_only": cand_e1,
    "E1_and_E2": cand_e1e2,
    "unique_8": cand_e1e2 == [8],
}

# ── T6：k=8 统一族精确赋值（ℚ 分数恒等）──
from fractions import Fraction as F
t6 = {
    "delta": F(1, 8*(8-1)) == F(1, 56),
    "C": F(2*8-3, 2**(8-1)) == F(13, 128),
    "D": F(8*(8-3)+1, 16*(8-3)**3) == F(41, 2000),
    "E": F(8*(8-3)-1, 16*(8-3)**3) == F(39, 2000),
    "DE": F(1, 8*(8-3)**3) == F(1, 1000),
    "nmax": F(1, (8+2)**3) == F(1, 1000),
}
results["T6_k8_exact"] = {"all_true": all(t6.values()), "items": t6}

all_pass = (
    results["T1_axis_unique"]["pos_unique_8"]
    and results["T2_mol41_reduce"]["equals_quad"]
    and results["T3_mol39_reduce"]["equals_quad"]
    and results["T1_T2_T3_enum_no_counterexample"]
    and results["T4_de_diff"]["pos_unique_8"]
    and results["T4_enum_no_counterexample"]
    and results["T5_enhanced"]["unique_8"]
    and results["T6_k8_exact"]["all_true"]
)
results["ALL_PASS"] = all_pass

print("T1 roots:", results["T1_axis_unique"])
print("T2/T3 reduce:", results["T2_mol41_reduce"]["equals_quad"], results["T3_mol39_reduce"]["equals_quad"])
print("T4 factor:", results["T4_de_diff"]["factor"], "roots:", results["T4_de_diff"]["all_roots"])
print("T5 E1:", cand_e1, "E1∧E2:", cand_e1e2)
print("T6:", t6)
print("ALL_PASS:", all_pass)

import json, os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "p7_5e286b_pycheck_result.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump({"results": {k2: v2 for k2, v2 in results.items()
                           if not isinstance(v2, dict) or "items" not in v2},
               "ALL_PASS": all_pass}, f, ensure_ascii=False, indent=1, default=str)
print("OUT:", out)
