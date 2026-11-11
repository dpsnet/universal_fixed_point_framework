# -*- coding: utf-8 -*-
"""
pr634ob_falsify.py  --  第 27 批模式 8 数值先证伪
问题：A（RecSpOverlap: 2^(k-2) = k^2）的候选空间是否能被
      sigma_intersection_closed 的封闭层枚举（k_max in {2,4,8}）限住？
      A 是否只在 k_max = 8 处成立？
"""

def recsp(k):
    return 2 ** (k - 2) if k >= 2 else None

def a_holds(k):
    if k < 2:
        return (2 ** 0 == 1) if False else None   # k=1 退化，单独看
    return recsp(k) == k * k

def sigma_solutions(kmax_max=64):
    """交汇方程 N*(2j-N) = 2^j - 1，k_max = 2j"""
    sols = []
    for j in range(1, kmax_max // 2 + 1):
        kmax = 2 * j
        for N in range(1, 2 * j):
            if N * (2 * j - N) == 2 ** j - 1:
                sols.append((j, kmax, N))
                break
    return sols

def bound_prod_identity(j, N):
    """N*(2j-N) = j^2 - (N-j)^2"""
    return N * (2 * j - N), j ** 2 - (N - j) ** 2

print("=" * 60)
print("[1] 交汇方程解集（N*(2j-N)=2^j-1）")
sols = sigma_solutions()
for (j, kmax, N) in sols:
    print("   j={0:2d}  k_max={1:3d}  N={2}".format(j, kmax, N))
print("   => k_max 集合 =", sorted(set(s[1] for s in sols)))

print()
print("[2] A 在 k=1..16 的成立情况")
ok = []
for k in range(1, 17):
    if k == 1:
        # Nat 截断：1-2=0，2^0=1，1^2=1  => 成立
        v = (2 ** 0 == 1 * 1)
    else:
        v = (2 ** (k - 2) == k * k)
    ok.append((k, v))
print("   ", ok)
print("   => A 成立的 k =", [k for (k, v) in ok if v])

print()
print("[3] A 只在封闭层集合 {2,4,8} 中的哪一个成立？")
closed = sorted(set(s[1] for s in sols))
for k in closed:
    v = (2 ** (k - 2) == k * k)
    print("   k_max={0:2d}: A = {1}".format(k, v))

print()
print("[4] bound_prod 恒等式 N*(2j-N) = j^2-(N-j)^2 抽查")
for (j, N) in [(2, 1), (2, 3), (4, 3), (4, 5), (3, 2), (5, 3)]:
    lhs, rhs = bound_prod_identity(j, N)
    print("   j={0} N={1}: lhs={2} rhs={3}  match={4}".format(j, N, lhs, rhs, lhs == rhs))

print()
print("[5] 交汇取 N = j±1 时是否给出 j^2 = 2^j")
for (j, kmax, N) in sols:
    if abs(N - j) == 1:
        print("   j={0}: |N-j|=1, (j-1)(j+1)={1}, 2^j-1={2}, j^2={3}, 2^j={4}  j^2==2^j ? {5}"
              .format(j, (j - 1) * (j + 1), 2 ** j - 1, j ** 2, 2 ** j, j ** 2 == 2 ** j))
    else:
        print("   j={0}: |N-j|={1} (不等于 1)".format(j, abs(N - j)))

print()
print("[6] j^2 = 2^j 在 j=1..32 的解")
jsol = [j for j in range(1, 33) if j ** 2 == 2 ** j]
print("   => ", jsol)

print()
print("[7] A 的半指数形式：k=2j 时 2^(2j-2) = 4j^2 即 j^2 = 2^(2j-4)")
for j in range(2, 9):
    lhs = j ** 2
    rhs = 2 ** (2 * j - 4)
    print("   j={0}: j^2={1:6d}  2^(2j-4)={2:6d}  match={3}   (k=2j={4})"
          .format(j, lhs, rhs, lhs == rhs, 2 * j))

VERDICT = (
    sorted(set(s[1] for s in sols)) == [2, 4, 8]
    and [k for (k, v) in ok if v] == [1, 8]
    and (2 ** 6 == 8 * 8)
    and (2 ** 0 != 2 * 2)
    and (2 ** 2 != 4 * 4)
    and jsol == [2, 4]
)
print()
print("=" * 60)
print("VERDICT_ALL_OK =", VERDICT)
