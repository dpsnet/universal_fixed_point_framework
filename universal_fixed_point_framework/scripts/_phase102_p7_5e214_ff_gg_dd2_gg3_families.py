# -*- coding: utf-8 -*-
"""
P7-5e-214 FF: DD2-family n structure (silent class, 585=9*65)
        GG: CC3-family silent-family index m = n+3k
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e214_ff_gg_dd2_gg3_families.json"

def Dn(n):
    return n * 7 * 2 ** (n - 1) + 2 ** n + 1

# ---------- FF: DD2 family ----------
FF_rows = []
for j in [1, 4, 7]:
    n = (2 ** (2 * j + 4) - 1) // 7
    FF_rows.append({"j": j, "n": n, "linear": 7 * n + 2,
                    "b_j^2+1": 2 ** (2 * j + 4) + 1,
                    "n_mod8": n % 8,
                    "silent_class": n % 8 == 1})

FF1 = {"check": "★ FF1: DD2 族 n 全 ≡ 1 mod 8（静默类）——7n ≡ 7 mod 8 ⇔ n ≡ 1 mod 8（2^{2j+4}−1 ≡ 7 mod 8，2^{≥3}≡0）",
       "all_silent": all(r["silent_class"] for r in FF_rows), "rows": FF_rows}
FF2 = {"check": "★ FF2: n=585 = 9·65（静默单元 × 修正锚点）——585=9·65=3²·5·13；n=9=8+1 静默类；n=37449=27·19·73（73=8·9+1 静默类）",
       "n585": 585, "factor": "9·65", "ok": 585 == 9 * 65,
       "n37449_check": 37449 % 8 == 1, "n37449_factors": "27·19·73"}
FF3 = {"check": "FF3: 4097 = b_4²+1 = 2^12+1 = F_2·D(4)（207 已登记，n=585 线性因子再现）",
       "ok": 4097 == 2 ** 12 + 1 == 17 * 241}

# ---------- GG: CC3 family ----------
GG_rows = []
for k in range(1, 6):
    a = 3 * k + 1
    v = 2 ** a
    n = (v - 2) // 7
    m = n + 3 * k
    GG_rows.append({"k": k, "a": a, "2^a": v, "n": n, "m": m,
                    "n_even": n % 2 == 0, "m_parity_k": (m % 2) == (k % 2),
                    "D_silent": "2^%d+1" % m})

GG1 = {"check": "GG1: 静默家族下标 m = n+3k（k=1: m=5、k=2: m=24、k=3: m=155、k=4: m=1182、k=5: m=9377）——D(n) = 2^m+1",
       "rows": GG_rows}
GG2 = {"check": "★ GG2: CC3 族 n 恒偶（2^a−2 ≡ 0 mod 14 ⇔ 2^a ≡ 2 mod 14，a ≡ 1 mod 3）；m = n+3k ⇒ m ≡ k mod 2（k 奇 → m 奇、k 偶 → m 偶）",
       "all_n_even": all(r["n_even"] for r in GG_rows),
       "all_m_parity": all(r["m_parity_k"] for r in GG_rows)}
GG3 = {"check": "GG3: D(n) = 2^m+1 静默家族成员 = 186 '2 进幂集组织' 的直接体现——特定 n（7n+2=2 的幂）的 B*(n) 分母恰为 2^m+1 家族成员（m 随 k 增长 ~2^{3k}/7）"}

conclusion = {
    "verdict": "FF（DD2 族结构）：DD2 族 n 全 ≡ 1 mod 8（静默类，7n≡7 mod 8 ⇔ n≡1 mod 8——2^{2j+4}−1≡7 mod 8）；★ n=585 = 9·65（静默单元 × 修正锚点，585=3²·5·13）；n=37449 ≡ 1 mod 8（3³·19·73，73=8·9+1 静默类）；4097=b_4²+1=F_2·D(4) 为 207 已知再现。GG（CC3 族下标）：静默家族下标 m=n+3k（k=1..5: m=5/24/155/1182/9377——D(n)=2^m+1）；★ n 恒偶（2^a≡2 mod 14，a≡1 mod 3）；m ≡ k mod 2；D(n)=2^m+1 是 186 '2 进幂集组织' 的直接体现（特定 n 的分母恰为静默家族成员）。",
    "FF": {"FF1": FF1, "FF2": FF2, "FF3": FF3},
    "GG": {"GG1": GG1, "GG2": GG2, "GG3": GG3},
    "honest_limits": [
        "FF1 是模算术（2^{2j+4}≡0 mod 8）",
        "FF2 的 585=9·65 是分解核对；n=37449 分解不漂亮（3³·19·73）",
        "FF3 是 207 已知再现",
        "GG1/GG2 是代数恒等（下标定义 + 奇偶判别）",
        "GG3 是语义连接（186 体现）",
        "继承 187-213 候选层",
    ],
    "next_candidates": [
        "检验 HH：DD2 族 n 序列 9,585,37449 的增长律（n ≈ 2^{2j}/7——j 每 +3 时 n 乘 2^6=64？n_{j+3}/n_j 检查）",
        "检验 II：GG 族 m 序列 5,24,155,1182,9377 的 mod 8 类（静默家族下标自身的类归属）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-215",
    ],
}

result = {
    "title": "P7-5e-214 FF: DD2-family n structure; GG: CC3-family silent index m=n+3k",
    "date": "2026-10-16",
    "FF": {"rows": FF_rows, "FF1": FF1, "FF2": FF2, "FF3": FF3},
    "GG": {"rows": GG_rows, "GG1": GG1, "GG2": GG2, "GG3": GG3},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-214 FF/GG: DD2-family n & CC3-family silent index")
print("=" * 76)
print("[FF DD2 family]")
for r in FF_rows:
    print("  j=%d n=%7d linear=%7d n_mod8=%d silent=%s" % (r["j"], r["n"], r["linear"], r["n_mod8"], r["silent_class"]))
print("[FF1]", FF1["check"], "-> all_silent=%s" % FF1["all_silent"])
print("[FF2]", FF2["check"], "-> 585=9*65 ok=%s n37449 mod8 ok=%s" % (FF2["ok"], FF2["n37449_check"]))
print("[FF3]", FF3["check"], "-> ok=%s" % FF3["ok"])
print("[GG CC3 family]")
for r in GG_rows:
    print("  k=%d 2^%d=%7d n=%6d m=%6d n_even=%s m%%2==k%%2=%s D=2^%d+1" % (
        r["k"], r["a"], r["2^a"], r["n"], r["m"], r["n_even"], r["m_parity_k"], r["m"]))
print("[GG2]", GG2["check"], "-> all_n_even=%s all_m_parity=%s" % (GG2["all_n_even"], GG2["all_m_parity"]))
print("[GG3]", GG3["check"])
print("[Conclusion]", conclusion["verdict"])
