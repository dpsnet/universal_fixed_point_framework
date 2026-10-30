# -*- coding: utf-8 -*-
"""模板身份示范核验：T(n) = 35*(2n-1)^2*((n-1)^2+2^3) 跨框架参数扫描（v0.4 立项准备）"""
from sympy import factorint

F_param = [1, 2, 3, 4, 5, 7, 8, 10, 15, 16, 21, 42, 49]  # 框架参数候选
F = {2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105, 231, 320, 675, 400}  # v0.3 框架量原子集

def T(n):
    return 35 * (2 * n - 1) ** 2 * ((n - 1) ** 2 + 8)

print("=== 模板 T(n) = 5·7·(2n−1)²·((n−1)²+2³) 跨框架参数分解 ===")
print("n\tT(n)\t素因子分解\t\t含105?\t含框架量因子?")
for n in F_param:
    v = T(n)
    fac = factorint(v)
    s = " * ".join("%d^%d" % (p, e) for p, e in sorted(fac.items()))
    div105 = v % 105 == 0
    divF = [f for f in sorted(F) if f > 1 and v % f == 0]
    print("%d\t%d\t%s\t%s\t%s" % (n, v, s, "✓" if div105 else "—", divF))

print("\n=== 对照：T(n) 对 1124315 的命中检查 ===")
for n in F_param:
    if T(n) == 1124315:
        print("n=%d 命中 1124315" % n)
print("（1124515 = T(10)，与 1124315 差 200 → 模板未命中 κΛ 的 d）")

print("\n=== 结构观察：两个结构因子在框架参数点的取值 ===")
for n in F_param:
    print("n=%2d: 2n−1=%-3d (n−1)²+8=%-3d" % (n, 2 * n - 1, (n - 1) ** 2 + 8))
