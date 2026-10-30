# -*- coding: utf-8 -*-
"""
S570 先证伪预检：freezeClosure 态射 Lean 锚的数值真值检验
按 Lean 定义逐字翻译：
  sigma = 1/15
  freezeClosure x = sigma * x
定理候选：
  A freezeClosure_unit : freezeClosure 1 = sigma
  B freezeClosure_cascade : (freezeClosure^[n]) 1 = sigma^n
    ——n 次函数迭代作用于 1
  C freezeClosure_linear : freezeClosure (a * b) = sigma * (a * b)
    ——σ 乘子线性性（乘法保持）
容差 1e-12——n = 0..12 全样本。
"""
sigma = 1 / 15

def freezeClosure(x):
    return sigma * x

def iterate(f, n, x):
    for _ in range(n):
        x = f(x)
    return x

print("S570 freezeClosure 先证伪预检")
print("=" * 60)

# A: freezeClosure 1 = sigma
a_ok = abs(freezeClosure(1) - sigma) < 1e-12
print(f"A freezeClosure 1 = sigma: {a_ok}  (resid={abs(freezeClosure(1)-sigma):.2e})")

# B: iterate n 次 = sigma^n（n = 0..12）
b_ok = True
for n in range(13):
    lhs = iterate(freezeClosure, n, 1)
    rhs = sigma ** n
    res = abs(lhs - rhs)
    if res >= 1e-12:
        b_ok = False
        print(f"  n={n}: FAIL res={res:.2e}")
print(f"B (freezeClosure^[n]) 1 = sigma^n: {b_ok}  (n=0..12 全样本)")

# C: 线性性
c_ok = True
for a, b in [(3.0, 2.0), (1.0, 15.0), (0.5, 7.0), (2.0, 0.1)]:
    lhs = freezeClosure(a * b)
    rhs = sigma * (a * b)
    if abs(lhs - rhs) >= 1e-12:
        c_ok = False
print(f"C freezeClosure 乘法保持: {c_ok}  (4 组样本)")

print()
print(f"结论: {'A/B/C 全 PASS——可投入 Lean 证明' if (a_ok and b_ok and c_ok) else '有 FAIL——需勘误'}")
