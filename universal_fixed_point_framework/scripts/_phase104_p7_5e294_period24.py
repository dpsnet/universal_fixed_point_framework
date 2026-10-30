# -*- coding: utf-8 -*-
"""P7-5e-294 数值先证伪：217 LL/MM（周期 24 联结与第二交集检查）

直接 Python 翻译 Lean 目标恒等：
  LL1 : Nat.Coprime 3 8 ∧ Nat.lcm 3 8 = 24
        DD2 族下标 j_t = 1+3t（t=0..7）mod 8 = [1,4,7,2,5,0,3,6]（遍历 8 类）
  LL2 : DD2 族 2 进指数 e_t = 2j+4 = 6t+6（t=0..3）mod 8 = [6,4,2,0]
        n 恒 ≡1 mod 8（7n+2=2^e+1 且 e>=4 ⇒ n%8=1，与指数类脱钩）
  MM1 : GG 族 m<129 窗口内 {5,24} ∩ 单位位指数集 {3,4,5,6,7,8} = {5}
  KK3 : 单位位家族 {9,17,33,65,129,257}，65=2^6+1 修正锚点、129=2^7+1 闭式常数
运行: D:\pyenv\pyenv-win\versions\3.11.8\python.exe scripts\_phase104_p7_5e294_period24.py
"""
import json

def gg_m(k: int) -> int:
    """GG 族 m_k = (2^(3k+1)+21k-2)/7（290 OO1 闭式）"""
    return (2 ** (3 * k + 1) + 21 * k - 2) // 7

def unit_members() -> list:
    """单位位家族指数集 {3,4,5,6,7,8}（值 2^m+1 = {9,17,33,65,129,257}）"""
    return list(range(3, 9))

checks = []
fails = 0

# ---- LL1: 互质 + lcm ----
import math
ok = (math.gcd(3, 8) == 1)
checks.append({"id": "ll1_coprime", "gcd": math.gcd(3, 8), "ok": ok})
fails += (not ok)
ok = (math.lcm(3, 8) == 24)
checks.append({"id": "ll1_lcm", "lcm": math.lcm(3, 8), "ok": ok})
fails += (not ok)

# ---- LL1: DD2 族下标 j_t = 1+3t（t=0..7）mod 8 遍历 8 类 ----
traverse_expect = [1, 4, 7, 2, 5, 0, 3, 6]
vals = [(1 + 3 * t) % 8 for t in range(8)]
ok = (vals == traverse_expect) and (len(set(vals)) == 8)
checks.append({"id": "ll1_traverse", "vals": vals, "expect": traverse_expect, "ok": ok})
fails += (not ok)

# ---- LL2: 指数 e_t = 6t+6（t=0..3）mod 8 = [6,4,2,0] ----
exp_expect = [6, 4, 2, 0]
evals = [(6 * t + 6) % 8 for t in range(4)]
ok = (evals == exp_expect)
checks.append({"id": "ll2_exp_mod8", "vals": evals, "expect": exp_expect, "ok": ok})
fails += (not ok)

# ---- LL2: n 恒 ≡1 mod 8（DD2 族 n = {9,585,37449}，直接核对）----
for n in [9, 585, 37449]:
    ok = (n % 8 == 1)
    checks.append({"id": f"ll2_n{n}", "n_mod8": n % 8, "ok": ok})
    fails += (not ok)

# ---- LL2: 7n+2=2^e+1 且 e>=4 ⇒ n%8=1（一般化验证：e=6,9,12,...,24 的整数解 n=(2^e-1)/7）----
for e in [6, 9, 12, 15, 18, 21, 24]:
    n = (2 ** e - 1) // 7
    lhs = 7 * n + 2
    rhs = 2 ** e + 1
    eq = (lhs == rhs)
    ok = eq and (n % 8 == 1)
    checks.append({"id": f"ll2_gen_e{e}_n{n}", "eq": eq, "n_mod8": n % 8, "ok": ok})
    fails += (not ok)

# ---- MM1: GG 族 m<129 窗口内 {5,24} ∩ 单位位 {3..8} = {5} ----
gg_lt129 = [gg_m(k) for k in range(1, 8) if gg_m(k) < 129]
ok = (gg_lt129 == [5, 24])
checks.append({"id": "mm1_gg_lt129", "gg": gg_lt129, "ok": ok})
fails += (not ok)
unit = unit_members()
intersect = [m for m in gg_lt129 if m in unit]
ok = (intersect == [5])
checks.append({"id": "mm1_intersect", "intersect": intersect, "ok": ok})
fails += (not ok)

# ---- MM2: GG 族 m 从 5 起步跳过单位位 m=6,7,8 ----
ok = all(m not in [6, 7, 8] for m in gg_lt129)
checks.append({"id": "mm2_skip", "ok": ok})
fails += (not ok)

# ---- KK3: 单位位家族值 = 2^m+1, m=3..8 = {9,17,33,65,129,257} ----
unit_vals = [2 ** m + 1 for m in unit_members()]
expect_vals = [9, 17, 33, 65, 129, 257]
ok = (unit_vals == expect_vals)
checks.append({"id": "kk3_unit_vals", "vals": unit_vals, "expect": expect_vals, "ok": ok})
fails += (not ok)
ok = (65 == 2 ** 6 + 1) and (129 == 2 ** 7 + 1)
checks.append({"id": "kk3_65_129", "ok": ok})
fails += (not ok)

# ---- 核对: 单位位家族含修正锚点 65（m=6）与闭式常数 129（m=7）----
ok = (65 in unit_vals) and (129 in unit_vals)
checks.append({"id": "kk3_contains", "ok": ok})
fails += (not ok)

total = len(checks)
result = {
    "phase": "P7-5e-294",
    "title": "217 LL/MM 周期 24 联结与单位位交集 数值先证伪",
    "total": total,
    "fails": fails,
    "all_pass": fails == 0,
    "checks": checks,
}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase104_p7_5e294_period24.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print(f"total={total} fails={fails} all_pass={fails == 0}")
if fails:
    for c in checks:
        if not c["ok"]:
            print("FAIL:", c)
