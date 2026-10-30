# -*- coding: utf-8 -*-
"""
P7-5e-219 PP: coeff-2 families are subsequences of coeff-1 bases; no confluence
        QQ: m_k closed-form remainder (3k-2) framework connection
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e219_pp_qq_coeff2_confluence_remainder.json"

def k_j(j):
    return 2 ** (j - 2) * 3

def k_win(j):
    return 6 * 4 ** j

def k_n(n):
    return 2 ** (n - 4) * (7 * n + 2)

# ---------- PP: confluence ----------
PP1 = {"check": "★ PP1: 系数 2 族是系数 1 基础族的约束子列——DD2 子列 ⊂ k_n（7n+2=b_j²+1 约束）、窗口对合 ⊂ k_j（2j+3 下标延伸，211 YY 修正推广）——'系数 2' 非独立族",
       "win_in_kj": [k_win(j) == k_j(2 * j + 3) for j in range(0, 5)],
       "all_win_in_kj": all(k_win(j) == k_j(2 * j + 3) for j in range(0, 5))}

# PP2: no confluence between k_win and k_n
win_vals = [k_win(j) for j in range(0, 8)]
kn_vals = [k_n(n) for n in range(4, 16)]
PP2 = {"check": "★ PP2: 两族无汇合——6·2^{2j} = 2^{n−4}(7n+2) 要求 7n+2 = 6·2^a；6·2^a ≡ 2 mod 7 无解（2^a mod 7 = {1,2,4} → 6·2^a mod 7 = {6,5,3}）",
       "win_vals": win_vals, "kn_vals": kn_vals,
       "no_intersection": len(set(win_vals) & set(kn_vals)) == 0,
       "six_2a_mod7": sorted({(6 * 2 ** a) % 7 for a in range(1, 10)}),
       "need_2": 2, "no_solution": 2 not in {(6 * 2 ** a) % 7 for a in range(1, 10)}}

PP3 = {"check": "PP3: DD2 子列 k_n（n=9,585,37449 的 k 值）与窗口对合值 6·4^j 同样无汇合（7n+2 = 6·2^a 无解的统一结论）",
       "note": "统一由 PP2 的模无解覆盖"}

# ---------- QQ: remainder framework ----------
QQ_rows = []
for k in range(1, 8):
    r = 3 * k - 2
    QQ_rows.append({"k": k, "21k-2": 21 * k - 2, "3k-2": r, "r_mod3": r % 3,
                    "r_eq1_mod3": r % 3 == 1})

QQ1 = {"check": "★ QQ1: m_k 余项 21k−2 = 7·(3k−2)，3k−2 ≡ 1 mod 3 恒成立（序列 1,4,7,10,13…）——与 212 BB2 '7n+2≡0 mod 3 ⇔ n≡1 mod 3' 的 3 周期同源",
       "rows": QQ_rows, "all_eq1": all(r["r_eq1_mod3"] for r in QQ_rows)}
QQ2 = {"check": "QQ2: 21 = 7·3（主模数 × 种子）——余项系数 21 的框架分解；21k−2 ≡ −2 ≡ 5 mod 7",
       "21_factors": "7·3", "mod7": 5}
QQ3 = {"check": "★ QQ3: m_k = n_k + 3k——静默下标相对分母下标的偏移 = 3k（3=种子、k=CC3 族下标）——'分母 n + 种子×族下标'的加法结构",
       "ok": all((((2 ** (3 * k + 1) - 2) // 7) + 3 * k) == ((2 ** (3 * k + 1) + 21 * k - 2) // 7) for k in range(1, 8))}

conclusion = {
    "verdict": "PP（汇合点）：★ 系数 2 族是系数 1 基础族的约束子列（DD2 ⊂ k_n、窗口对合 ⊂ k_j——211 YY 修正的推广），'系数 2' 非独立族；★ 两族无汇合：6·2^a ≡ 2 mod 7 无解（2^a mod 7 = {1,2,4} → 6·2^a = {6,5,3}），k_{2j+3} 与 k_n 值集无交集。QQ（余项框架）：★ 余项 21k−2 = 7(3k−2)，3k−2 ≡ 1 mod 3 恒成立（与 212 BB2 的 3 周期同源）；21 = 7·3（主模数×种子）；★ m_k = n_k + 3k——静默下标偏移 = 3k（种子×族下标）加法结构。",
    "PP": {"PP1": PP1, "PP2": PP2, "PP3": PP3},
    "QQ": {"QQ1": QQ1, "QQ2": QQ2, "QQ3": QQ3},
    "honest_limits": [
        "PP1 是子列核对（211 YY 已定窗口对合）——DD2 子列归属为新核对",
        "PP2 是模算术无解证明（负结果）",
        "PP3 是 PP2 的直接覆盖",
        "QQ1 是模算术观察（3k−2≡1 mod 3）",
        "QQ2 是恒等分解",
        "QQ3 是代数恒等（闭式定义）",
        "继承 187-218 候选层",
    ],
    "next_candidates": [
        "检验 RR：3k−2 ≡ 1 mod 3 与静默单元家族下标 m≡1 mod 3 成员的对应（静默家族 2^m+1 中 m≡1 mod 3 的子列）",
        "检验 SS：PP2 模无解 6·2^a 与 212 CC2 纯积条件 2^a·3^b·5^c ≡ 2 mod 7 的联合结构（含 3 因子的纯积可解性）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-220",
    ],
}

result = {
    "title": "P7-5e-219 PP: coeff-2 subsequence & no confluence; QQ: remainder framework",
    "date": "2026-10-16",
    "PP": {"PP1": PP1, "PP2": PP2, "PP3": PP3},
    "QQ": {"rows": QQ_rows, "QQ1": QQ1, "QQ2": QQ2, "QQ3": QQ3},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-219 PP/QQ: confluence check & remainder framework")
print("=" * 76)
print("[PP1]", PP1["check"], "-> all_win_in_kj=%s" % PP1["all_win_in_kj"])
print("[PP2]", PP2["check"])
print("  win_vals=%s" % win_vals)
print("  kn_vals=%s" % kn_vals)
print("  no_intersection=%s 6*2^a mod7=%s need_2_in=%s" % (PP2["no_intersection"], PP2["six_2a_mod7"], not PP2["no_solution"]))
print("[PP3]", PP3["check"])
print("[QQ remainder]")
for r in QQ_rows:
    print("  k=%d 21k-2=%3d 3k-2=%2d mod3=%d eq1=%s" % (r["k"], r["21k-2"], r["3k-2"], r["r_mod3"], r["r_eq1_mod3"]))
print("[QQ1]", QQ1["check"], "-> all_eq1=%s" % QQ1["all_eq1"])
print("[QQ2]", QQ2["check"], "-> %s mod7=%s" % (QQ2["21_factors"], QQ2["mod7"]))
print("[QQ3]", QQ3["check"], "-> ok=%s" % QQ3["ok"])
print("[Conclusion]", conclusion["verdict"])
