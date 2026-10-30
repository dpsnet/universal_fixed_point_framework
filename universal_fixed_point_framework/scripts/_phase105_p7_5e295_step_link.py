# -*- coding: utf-8 -*-
"""P7-5e-295 数值先证伪：216 JJ/KK（增长递推步进联结与单位位交集）

直接 Python 翻译 Lean 目标恒等：
  JJ1 : 分子层增长恒等 2^(2(j+3)+4)-1 = 64*(2^(2j+4)-1)+63（指数步进 6 ↔ 增长 2^6=64=b_1^2）
        + 2^6 = 8^2 = 64（b_1=8, 64=b_1^2 框架量）
  JJ2 : j%3=1 → 6 | (2j+4)（DD2 指数 ≡0 mod 6）；e=2j+4 mod 8 对 j=1,4,7,10 = 6,4,2,0
  JJ3 : HH 递推系数全框架量 64=8^2、9=8+1=静默单元、63=8^2-1=窗口宽度
  KK1 : GG 族 m_k 与单位位指数集 {3..8} 交集 = {5}（m_1=5∈、m_2=24∉、m_3=155∉；∀k≥2 m_k>8）
  KK2 : 2^m+1 ≡ 1 mod 8（m≥3，值类恒静默——下标类与值类脱钩）
运行: D:\pyenv\pyenv-win\versions\3.11.8\python.exe scripts\_phase105_p7_5e295_step_link.py
"""
import json

def gg_m(k: int) -> int:
    """GG 族 m_k = (2^(3k+1)+21k-2)/7（290 OO1 闭式）"""
    return (2 ** (3 * k + 1) + 21 * k - 2) // 7

def unit_members() -> list:
    """单位位家族指数集 {3,4,5,6,7,8}"""
    return list(range(3, 9))

checks = []
fails = 0

# ---- JJ1: 分子层增长恒等（指数步进 6 ↔ 增长因子 2^6=64）----
for j in range(0, 11):
    lhs = 2 ** (2 * (j + 3) + 4) - 1
    rhs = 64 * (2 ** (2 * j + 4) - 1) + 63
    ok = (lhs == rhs)
    checks.append({"id": f"jj1_mol_j{j}", "lhs": lhs, "rhs": rhs, "ok": ok})
    fails += (not ok)

ok = (2 ** 6 == 64) and (8 ** 2 == 64)
checks.append({"id": "jj1_pow64", "ok": ok})
fails += (not ok)

# ---- JJ2: j%3=1 → 6 | (2j+4)；e=2j+4 mod 8 ----
for j in [1, 4, 7, 10, 13]:
    ok = ((2 * j + 4) % 6 == 0) and (j % 3 == 1)
    checks.append({"id": f"jj2_dvd6_j{j}", "mod6": (2*j+4) % 6, "ok": ok})
    fails += (not ok)

exp_expect = [6, 4, 2, 0]
evals = [(2 * j + 4) % 8 for j in [1, 4, 7, 10]]
ok = (evals == exp_expect)
checks.append({"id": "jj2_mod8", "vals": evals, "expect": exp_expect, "ok": ok})
fails += (not ok)

# ---- JJ3: HH 递推系数全框架量 ----
ok = (64 == 8 ** 2) and (9 == 8 + 1) and (63 == 8 ** 2 - 1)
checks.append({"id": "jj3_consts", "ok": ok})
fails += (not ok)

# ---- KK1: GG 族 ∩ 单位位 = {5} ----
gg_vals = [gg_m(k) for k in range(1, 4)]
ok = (gg_vals == [5, 24, 155])
checks.append({"id": "kk1_gg_vals", "vals": gg_vals, "ok": ok})
fails += (not ok)
unit = unit_members()
ok = (5 in unit) and (24 not in unit) and (155 not in unit)
checks.append({"id": "kk1_membership", "unit": unit, "ok": ok})
fails += (not ok)
ok = all(gg_m(k) > 8 for k in range(2, 20))
checks.append({"id": "kk1_beyond8", "ok": ok})
fails += (not ok)

# ---- KK2: 2^m+1 ≡ 1 mod 8（m≥3）----
for m in [3, 4, 5, 6, 7, 8, 9, 12, 15, 20]:
    ok = ((2 ** m + 1) % 8 == 1)
    checks.append({"id": f"kk2_val_mod8_m{m}", "mod8": (2**m + 1) % 8, "ok": ok})
    fails += (not ok)

total = len(checks)
result = {
    "phase": "P7-5e-295",
    "title": "216 JJ/KK 增长递推步进联结与单位位交集 数值先证伪",
    "total": total,
    "fails": fails,
    "all_pass": fails == 0,
    "checks": checks,
}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase105_p7_5e295_step_link.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print(f"total={total} fails={fails} all_pass={fails == 0}")
if fails:
    for c in checks:
        if not c["ok"]:
            print("FAIL:", c)
