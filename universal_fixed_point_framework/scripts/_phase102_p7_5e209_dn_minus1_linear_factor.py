# -*- coding: utf-8 -*-
"""
P7-5e-209 D(n) denominator primacy: D(n)-1 = 2^{n-1}(7n+2) & 1/B*(n) = D(n)/(7*2^n)
"""
import json
from fractions import Fraction

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e209_dn_minus1_linear_factor.json"

def Dn(n):
    return n * 7 * 2 ** (n - 1) + 2 ** n + 1

def Bstar_inv_closed(n):
    """closed form 129: 1/B*(n) = n/2 + 1/7 + 1/(7*2^n) + [n=1: +1/65]"""
    val = Fraction(n, 2) + Fraction(1, 7) + Fraction(1, 7 * 2 ** n)
    if n == 1:
        val += Fraction(1, 65)
    return val

# ---------- XX1: D(n)-1 = 2^{n-1}(7n+2) ----------
XX1_rows = []
for n in range(9, 17):
    d = Dn(n)
    lhs = d - 1
    rhs = 2 ** (n - 1) * (7 * n + 2)
    XX1_rows.append({"n": n, "D(n)-1": lhs, "2^{n-1}(7n+2)": rhs,
                     "ok": lhs == rhs, "7n+2": 7 * n + 2,
                     "7n+2 mod8": (7 * n + 2) % 8})

# ---------- XX2: 1/B*(n) = D(n)/(7*2^n) for n>=2 ----------
XX2_rows = []
for n in range(2, 17):
    invB = Bstar_inv_closed(n)
    d_den = Dn(n) / (7 * 2 ** n)
    ok = Fraction(invB) == Fraction(Dn(n), 7 * 2 ** n)
    XX2_rows.append({"n": n, "1/B* closed": str(invB), "D(n)/(7*2^n)": str(Fraction(Dn(n), 7 * 2 ** n)),
                     "ok": ok})

# ---------- XX3: n=1 exception ----------
n1 = Fraction(332, 455)
den_plain = 7 * 2 ** 1          # 14
den_corrected = 7 * 65          # 455
base_n1 = Fraction(1, 2) + Fraction(1, 7) + Fraction(1, 14)  # 5/7
XX3 = {
    "check": "n=1 例外：1/B*(1) = 332/455 = 332/(7·65)——分母从 7·2=14 放大到 7·65=455（+1/65 修正的机制 = 分母放大）",
    "1/B*(1)": "332/455", "base": str(base_n1), "den_plain": den_plain,
    "den_corrected": den_corrected,
    "ok_base_5of7": base_n1 == Fraction(5, 7),
    "ok_full": base_n1 + Fraction(1, 65) == n1,
}

# ---------- XX4: 7n+2 hits framework quantities ----------
XX4_hits = {"n=9": 65, "n=10": 72}
XX4 = {
    "check": "7n+2 命中框架量仅 n=9（65=7·9+2=修正锚点）、n=10（72=7·10+2=8·9 满格×静默单元）；n=11..16（79/86/93/100/107/114）非框架量",
    "n=9": 7 * 9 + 2, "n=10": 7 * 10 + 2,
    "ok65": (7 * 9 + 2) == 65, "ok72": (7 * 10 + 2) == 8 * 9,
    "non_hits": [7 * n + 2 for n in range(11, 17)],
}

# ---------- XX5: 65 triple identity ----------
XX5 = {
    "check": "65 三重身份核对：8²+1 = 7·8+9 = 5·13——7·8+9 是 8²+1 的展开（9=8+1 ⇒ 7·8+9=8·8+1），非新身份；65=7·9+2（XX1 线性因子身份）同样归约",
    "8^2+1": 8 ** 2 + 1, "7*8+9": 7 * 8 + 9, "5*13": 5 * 13,
    "ok_algebraic_same": (7 * 8 + 9) == (8 ** 2 + 1),
    "note": "7·9+2 = 63+2 = 65 = 8²+1 代数等价（n=9 时 7n+2 = 7(n+1)-5 = ... 直接展开）",
}

# ---------- Connection to closed form 129 ----------
CONN = {
    "check": "分母第一性：闭式 129 的 1/B*(n)（n≥2）合并为单分数 = D(n)/(7·2^n)——D(n)=2^{n-1}(7n+2)+1 是闭式分母的精确分解；n=1 例外分母 7·2→7·65（+1/65 修正 = 分母放大机制）",
    "closed_form": "1/B*(n) = n/2 + 1/7 + 1/(7·2^n) + [n=1:+1/65]",
    "merged": "1/B*(n) = D(n)/(7·2^n)  (n≥2),  1/B*(1) = 332/(7·65)",
    "Dn": "D(n) = 2^{n-1}(7n+2) + 1",
}

conclusion = {
    "verdict": "XX（★ 分母第一性闭合）：D(n)−1 = 2^{n−1}(7n+2) 以 D 下标 n 重写（比 m 版本 2^{m+7}(7m+58) 更干净）；★ 1/B*(n) = D(n)/(7·2^n)（n=2..16 全 True）——D(n) = 2^{n−1}(7n+2)+1 是闭式 129 的精确分母分解（合并 n/2+1/7+1/(7·2^n) 即得）；n=1 例外：1/B*(1)=332/455=332/(7·65)——+1/65 修正的机制 = 分母从 7·2 放大到 7·65；7n+2 命中框架量仅 n=9（65）、n=10（72=8·9）；65 的 7·9+2 / 7·8+9 表达与 8²+1 代数等价（非新身份）。208 的 D(m+8) 讨论由此归约到闭式分母第一性——D(n) 的 '−1 结构' = 2 的幂 × (7n+2) 线性因子，n 依赖完全显式。",
    "XX1": {"check": "★ D(n)−1 = 2^{n−1}(7n+2)（D 下标 n 重写）", "rows": XX1_rows},
    "XX2": {"check": "★ 1/B*(n) = D(n)/(7·2^n)（n≥2 闭式合并）", "rows": XX2_rows},
    "XX3": XX3,
    "XX4": XX4,
    "XX5": XX5,
    "connection": CONN,
    "honest_limits": [
        "XX1/XX2 是代数恒等（闭式展开/合并直接给出）",
        "XX3 是闭式 129 定义的直接结果（+1/65 修正已知）",
        "XX4 是枚举事实（n=9,10 命中）",
        "XX5 确认 65 表达代数等价（无新身份）",
        "继承 187-208 候选层",
    ],
    "next_candidates": [
        "检验 YY：k_{2j+3}=6·4^j 族与窗口常数组 k_j=3·2^{j−2} 的并集（含 24/96 交叠核对）",
        "检验 ZZ：D(n)/(7·2^n) 分母结构与 P7-5e-186 '2 进幂集组织' 的连接（D(n) 分母的 2 进展开）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-210",
    ],
}

result = {
    "title": "P7-5e-209 D(n) denominator primacy: D(n)-1 = 2^{n-1}(7n+2) & 1/B*(n) = D(n)/(7*2^n)",
    "date": "2026-10-16",
    "XX1": {"rows": XX1_rows},
    "XX2": {"rows": XX2_rows},
    "XX3": XX3,
    "XX4": XX4,
    "XX5": XX5,
    "connection": CONN,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-209 D(n) denominator primacy")
print("=" * 76)
print("[XX1 D(n)-1 = 2^{n-1}(7n+2)]")
for r in XX1_rows:
    print("  n=%2d  D-1=%9d == 2^{n-1}(7n+2)=%9d? %s   7n+2=%3d mod8=%d" % (
        r["n"], r["D(n)-1"], r["2^{n-1}(7n+2)"], r["ok"], r["7n+2"], r["7n+2 mod8"]))
print("[XX2 1/B*(n) = D(n)/(7*2^n)]")
for r in XX2_rows:
    print("  n=%2d  1/B*=%s  D(n)/(7*2^n)=%s  ok=%s" % (r["n"], r["1/B* closed"], r["D(n)/(7*2^n)"], r["ok"]))
print("[XX3]", XX3["check"], "-> base=5/7? %s full ok? %s" % (XX3["ok_base_5of7"], XX3["ok_full"]))
print("[XX4]", XX4["check"], "-> n=9: %d n=10: %d ok65=%s ok72=%s" % (XX4["n=9"], XX4["n=10"], XX4["ok65"], XX4["ok72"]))
print("[XX5]", XX5["check"], "-> same=%s" % XX5["ok_algebraic_same"])
print("[Connection]", CONN["check"])
print("[Conclusion]", conclusion["verdict"])
