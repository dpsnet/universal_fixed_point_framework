# 数值先证伪：e 的 8 阶截断余项界 |e - Σ_{k=0}^8 1/k!| <= 10/(9*9!)
# 依据 Lean 定义逐字翻译：eTrunc K = Σ_{k=0}^K 1/k!（有理数），kMax = 8
import math

K = 8
eTrunc = sum(1.0 / math.factorial(k) for k in range(0, K + 1))
e_true = math.e
rem = abs(e_true - eTrunc)
bound = 10.0 / (9 * math.factorial(9))
resid = rem - bound  # 目标：resid <= 0 对所有样本成立

# 再验中间量：9! = 362880, 9*9! = 3265920
print(f"eTrunc(8)  = {eTrunc:.12f}  ({eTrunc})")
print(f"e          = {e_true:.12f}")
print(f"余项 |e - eTrunc| = {rem:.12e}")
print(f"界 10/(9*9!)      = {bound:.12e}")
print(f"界 - 余项         = {bound - rem:.12e}  (需 >= 0)")
print(f"残差 (resid<=0)   = {resid:.12e}")
print(f"8! = {math.factorial(8)}, 9! = {math.factorial(9)}, 9*9! = {9*math.factorial(9)}")

# 额外抽样：不同 K（K>=9 时余项也应被同一几何界夹逼——单调性检查）
for K2 in [9, 10, 12, 20]:
    t = sum(1.0 / math.factorial(k) for k in range(0, K2 + 1))
    r2 = abs(e_true - t)
    print(f"K={K2}: |e - eTrunc({K2})| = {r2:.12e}  (随 K 增大递减: {r2 < rem if K2 > K else '-'})")

# 关键不等式检查：k! >= 9! * 10^(k-9) 对 k>=9（几何夹逼基础）
ok = True
for k in range(9, 30):
    lhs = math.factorial(k)
    rhs = math.factorial(9) * (10 ** (k - 9))
    if lhs < rhs:
        ok = False
        print(f"  违反: k={k}  {lhs} < {rhs}")
print(f"k! >= 9!*10^(k-9) 对 9<=k<=29 全部成立: {ok}")
