# -*- coding: utf-8 -*-
"""P7-5e-293 数值先证伪：211 YY/AA（k 族同族判别 + 种子交集）

直接 Python 翻译 Lean 目标恒等（kj/kn 定义逐字翻译）：
  YY1 : kj (2*j+3) = 6*4^j           (后移窗口对合常数 = 6·4^j)
  YY2 : 6*4^j = 3*2^(2*j+1)          (同一族两种表达)
  YY3 : kj (2*j+3) = 3*2^(2*j+1)     (YY1+YY2 合成 = k_j 公式在下标 2j+3 的取值)
  AA1 : kn(4) = 30 = 2*3*5           (纯种子积)
  AA2 : kn(9) = 2^5*65 = 2080        (65 = 7*9+2 线性因子核对)
  AA3 : D(n)-1 = 8*kn(n)             (291 zz2_decomp 交叉: n>=4)
运行: D:\pyenv\pyenv-win\versions\3.11.8\python.exe scripts\_phase103_p7_5e293_family_index.py
"""
import json

def kj(j: int) -> int:
    """窗口对合常数族 k_j = 3·2^(j-2)（Nat 语义: j<2 时 j-2=0 仍定义）"""
    return 3 * (2 ** (j - 2)) if j >= 2 else 3 * (2 ** 0)  # Lean Nat: j-2 对 j<2 钳为 0

def kn(n: int) -> int:
    """D(n) 的 k_n = 2^(n-4)(7n+2)（n>=4）"""
    return (2 ** (n - 4) if n >= 4 else 2 ** 0) * (7 * n + 2)

def Dn(n: int) -> int:
    """D(n) = 2^(n-1)(7n+2)+1（209 闭式分母分解）"""
    return 2 ** (n - 1) * (7 * n + 2) + 1

checks = []
fails = 0

# ---- YY1: kj(2j+3) = 6·4^j, j=1..10（窗口 5,7,9,11,13,15,...）----
for j in range(1, 11):
    lhs = kj(2 * j + 3)
    rhs = 6 * (4 ** j)
    ok = (lhs == rhs)
    checks.append({"id": f"yy1_j{j}", "lhs": lhs, "rhs": rhs, "ok": ok})
    fails += (not ok)

# ---- YY2: 6·4^j = 3·2^(2j+1), j=1..10 ----
for j in range(1, 11):
    lhs = 6 * (4 ** j)
    rhs = 3 * (2 ** (2 * j + 1))
    ok = (lhs == rhs)
    checks.append({"id": f"yy2_j{j}", "lhs": lhs, "rhs": rhs, "ok": ok})
    fails += (not ok)

# ---- YY3: kj(2j+3) = 3·2^(2j+1)（合成, 同族恒等直接形式）----
for j in range(1, 11):
    lhs = kj(2 * j + 3)
    rhs = 3 * (2 ** (2 * j + 1))
    ok = (lhs == rhs)
    checks.append({"id": f"yy3_j{j}", "lhs": lhs, "rhs": rhs, "ok": ok})
    fails += (not ok)

# ---- kj 序列 j=2..16（窗口对合常数族全值）----
seq_expect = [3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072, 6144, 12288, 24576, 49152]
for idx, j in enumerate(range(2, 17)):
    val = kj(j)
    ok = (val == seq_expect[idx])
    checks.append({"id": f"kj_j{j}", "val": val, "expect": seq_expect[idx], "ok": ok})
    fails += (not ok)

# ---- 窗口 {5,7,9,11,13,15} 后移对合常数值 = 6·4^j, j=1..6 ----
win_expect = [24, 96, 384, 1536, 6144, 24576]
for idx, j in enumerate(range(1, 7)):
    w = 2 * j + 3
    val = kj(w)
    ok = (val == 6 * (4 ** j) == win_expect[idx])
    checks.append({"id": f"win_w{w}", "val": val, "expect": win_expect[idx], "ok": ok})
    fails += (not ok)

# ---- AA1: kn(4) = 30 = 2·3·5 ----
val = kn(4)
ok = (val == 30 == 2 * 3 * 5)
checks.append({"id": "aa1_seed4", "val": val, "ok": ok})
fails += (not ok)

# ---- AA2: kn(9) = 2^5·65 = 2080 ----
val = kn(9)
ok = (val == (2 ** 5) * 65 == 2080)
checks.append({"id": "aa2_k9", "val": val, "ok": ok})
fails += (not ok)

# ---- AA3: D(n)-1 = 8·kn(n), n=4..16（291 zz2_decomp 交叉）----
for n in range(4, 17):
    lhs = Dn(n) - 1
    rhs = 8 * kn(n)
    ok = (lhs == rhs)
    checks.append({"id": f"aa3_n{n}", "lhs": lhs, "rhs": rhs, "ok": ok})
    fails += (not ok)

total = len(checks)
result = {
    "phase": "P7-5e-293",
    "title": "211 YY/AA k 族同族判别与种子交集 数值先证伪",
    "total": total,
    "fails": fails,
    "all_pass": fails == 0,
    "checks": checks,
}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase103_p7_5e293_family_index.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)

print(f"total={total} fails={fails} all_pass={fails == 0}")
if fails:
    for c in checks:
        if not c["ok"]:
            print("FAIL:", c)
