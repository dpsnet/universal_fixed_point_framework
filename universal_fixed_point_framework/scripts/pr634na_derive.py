# -*- coding: utf-8 -*-
"""模式 8 先证伪：N_active = 3 的代数唯一性来由

链：
  A  2^(k-2) = k^2        （Rec 侧 2 幂 与 Sp 侧平方 在截断处重合）
  B  k = 2^m              （Bott 塔翻倍，m = 翻倍步数）
  => m = 3

本脚本穷举 k, m 检验：
  1) A 在 k=2..64 的唯一解
  2) 2^m = 2m+2 在 m=1..32 的唯一解
  3) A 与 B 同时成立时 m 的取值集合
  4) 若把 A 放宽（改成 4 k^2 = 2^k 的等价形式）结果是否一致
"""
import math

print("=" * 60)
print("[1] 2^(k-2) = k^2 的解（k = 2..64）")
sols_a = [k for k in range(2, 65) if 2 ** (k - 2) == k ** 2]
print("  解 =", sols_a)

print("[2] 2^m = 2m+2 的解（m = 1..32）")
sols_b = [m for m in range(1, 33) if 2 ** m == 2 * m + 2]
print("  解 =", sols_b)

print("[3] A ∧ (k = 2^m) 同时成立时 m 的取值")
pairs = []
for k in range(2, 65):
    if 2 ** (k - 2) != k ** 2:
        continue
    # 求 m 使 2^m = k
    mm = math.log2(k)
    if abs(mm - round(mm)) < 1e-12:
        pairs.append((k, int(round(mm))))
    else:
        pairs.append((k, None))
print("  (k, m) =", pairs)

print("[4] 等价形式 4 k^2 = 2^k（k = 2..64）")
sols_c = [k for k in range(2, 65) if 4 * k ** 2 == 2 ** k]
print("  解 =", sols_c)

print("[5] 反证：若 A 不成立的邻近 k，是否还能给出 m=3")
for k in [7, 9, 16, 32]:
    print("   k=%2d  ->  2^(k-2)=%s   k^2=%s   equal=%s" % (
        k, 2 ** (k - 2), k ** 2, 2 ** (k - 2) == k ** 2))

print("[6] 交叉：m 的唯一性与 k 的唯一性是否互推")
print("   A 唯一解 k =", sols_a, "  log2 =>", [math.log2(k) for k in sols_a])
print("   B 唯一解 m =", sols_b)

ok = (sols_a == [8]) and (sols_b == [3]) and (sols_c == [8]) and (pairs == [(8, 3)])
print("=" * 60)
print("VERDICT_ALL_OK =", ok)
