# -*- coding: utf-8 -*-
"""P7-5e-292 数值先证伪：GG 族模 8 结构与 CC3 族模类（215 II1/II2 + 218 OO1 核对）

定理清单（按 Lean 陈述逐字翻译）：
- cc3_n_mod8 : 1<=k, 7n+2=2^(3k+1) -> n % 8 = 2   （CC3 族 n≡2 mod 8，II1）
- gm_mod8    : 1<=k, 7n+2=2^(3k+1) -> (n+3k) % 8 = (3k+2) % 8   （GG 族 m≡3k+2 mod 8，II2）
- gm_traverse: k=1..8 的 m_k = Gm(k) = (2^(3k+1)-2)/7 + 3k 满足
               m mod 8 = 5,0,3,6,1,4,7,2 （遍历 8 类，II2 实证）
- gm_instances: Gm(k) 数值 k=1..7 = 5,24,155,1182,9377,74916,599207 （OO1 核对）
- gm_diff_exact: Gm(k+1) - Gm(k) = 2^(3k+1) + 3 （相邻差精确闭式，II2）
容差 1e-8（全整数恒等，要求残差 0）。
"""
import json

def Gm(k):
    return (2**(3*k+1) - 2) // 7 + 3*k

results = []
total = 0
fails = 0

# cc3_n_mod8: CC3 族实例 n=2,18,146,1170 (k=1..4)
cc3_ns = [(2,1),(18,2),(146,3),(1170,4)]
for n, k in cc3_ns:
    total += 1
    ok = (7*n + 2 == 2**(3*k+1)) and (n % 8 == 2)
    fails += (not ok)
    results.append({"thm": "cc3_n_mod8", "n": n, "k": k, "7n+2": 7*n+2,
                    "n_mod8": n % 8, "ok": ok, "residual": 0 if ok else 1})

# gm_mod8: k=1..30
for k in range(1, 31):
    n = (2**(3*k+1) - 2) // 7
    lhs = (n + 3*k) % 8
    rhs = (3*k + 2) % 8
    total += 1
    ok = (lhs == rhs)
    fails += (not ok)
    results.append({"thm": "gm_mod8", "k": k, "n": n, "m": n+3*k,
                    "lhs": lhs, "rhs": rhs, "ok": ok, "residual": lhs-rhs if not ok else 0})

# gm_traverse: k=1..8
expected = [5, 0, 3, 6, 1, 4, 7, 2]
for k in range(1, 9):
    total += 1
    ok = (Gm(k) % 8 == expected[k-1])
    fails += (not ok)
    results.append({"thm": "gm_traverse", "k": k, "Gm": Gm(k),
                    "mod8": Gm(k) % 8, "expect": expected[k-1],
                    "ok": ok, "residual": 0 if ok else Gm(k)%8 - expected[k-1]})

# gm_instances: k=1..7
expected_vals = [5, 24, 155, 1182, 9377, 74916, 599207]
for k in range(1, 8):
    total += 1
    ok = (Gm(k) == expected_vals[k-1])
    fails += (not ok)
    results.append({"thm": "gm_instances", "k": k, "Gm": Gm(k),
                    "expect": expected_vals[k-1], "ok": ok,
                    "residual": Gm(k)-expected_vals[k-1] if not ok else 0})

# gm_diff_exact: k=1..12
for k in range(1, 13):
    lhs = Gm(k+1) - Gm(k)
    rhs = 2**(3*k+1) + 3
    total += 1
    ok = (lhs == rhs)
    fails += (not ok)
    results.append({"thm": "gm_diff_exact", "k": k, "lhs": lhs, "rhs": rhs,
                    "ok": ok, "residual": lhs-rhs if not ok else 0})

# 联合判定：II1×II2×OO1 并置
joint = all(r["ok"] for r in results)
total += 1
fails += (not joint)
results.append({"thm": "ii_judgement", "ok": joint, "residual": 0 if joint else 1})

summary = {
    "layer": "P7-5e-292",
    "total": total,
    "fails": fails,
    "all_pass": fails == 0,
    "results": results,
}
with open("E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/_phase102_p7_5e292_gg_mod8.py.json".replace(".py.json", ".json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"total={total} fails={fails} all_pass={fails == 0}")
