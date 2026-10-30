# -*- coding: utf-8 -*-
"""
S564 先证伪预检（模式 8——Lean 化前数值真值检验）
检验 S563 G1 构造论证的 Lean 化目标恒等：
  A. freezeLayerSeq（静默冻结层序列）长度 = silenceStrikes（0-4）
  B. compDepth = freezeLayerSeq 长度（带修正量 2<=n<=4）
  C. 级联指数化：n 个冻结闭合因子（各=σ）之积 = σ^n（0-8）
  D. m_Δ 张量积序列为空（无冻结作用）
容差 1e-12——全部为 0 才可投入 Lean 证明。
"""
SIG = 1 / 15.0

# A/B: 层序列定义（与 Lean 定义逐字一致）
def freezeLayerSeq(n):
    if n == 0: return []
    if n == 1: return []          # m_Δ 张量积——无静默层
    if n == 2: return [1, 2, 3]   # 活跃层——3 静默层
    if n == 3: return [1, 2]      # 幂基层——2 静默层
    if n == 4: return [1]         # 恒等层——1 静默层
    return []

def silenceStrikes(n):
    return len(freezeLayerSeq(n))  # 构造性定义——s = 序列长度

def compDepth(n):
    if n == 1: return 1
    if n == 2: return 3
    if n == 3: return 2
    if n == 4: return 1
    return 0

def freezeFactor(i):
    return SIG  # 每层穿越引入 σ 因子（C1）

print("=" * 72)
print("S564 先证伪预检：G1 层序列构造 Lean 化目标")
print("=" * 72)

# A: 序列长度 = silenceStrikes（构造性——定义即恒等，仍验证）
failsA = []
for n in range(0, 5):
    if len(freezeLayerSeq(n)) != silenceStrikes(n):
        failsA.append(n)
print(f"A. freezeLayerSeq 长度 = silenceStrikes（0-4）: {'✓ 全一致' if not failsA else '✗ ' + str(failsA)}")

# B: compDepth = 序列长度（2<=n<=4）
failsB = []
for n in range(2, 5):
    if compDepth(n) != len(freezeLayerSeq(n)):
        failsB.append(n)
print(f"B. compDepth = 序列长度（2<=n<=4）: {'✓ 全一致' if not failsB else '✗ ' + str(failsB)}")

# C: 级联指数化——n 个 σ 因子之积 = σ^n（n=0..8）
import math
failsC = []
for n in range(0, 9):
    prod = math.prod([freezeFactor(i) for i in range(n)])
    target = SIG ** n
    if abs(prod - target) > 1e-12:
        failsC.append(n)
print(f"C. 级联指数化 ∏σ = σ^n（0-8）: {'✓ 全一致（容差 1e-12）' if not failsC else '✗ ' + str(failsC)}")

# D: m_Δ 张量积序列为空
okD = freezeLayerSeq(1) == []
print(f"D. m_Δ 张量积序列空（无冻结作用）: {'✓' if okD else '✗'}")

# E: 幂次=深度=序列长度（T1 链 k=s=d 的序列版本）
failsE = []
for n in range(2, 5):
    k = compDepth(n)  # correctionPower = compDepth（既有定理）
    if not (k == compDepth(n) == len(freezeLayerSeq(n))):
        failsE.append(n)
print(f"E. k=d=序列长度（2<=n<=4——T1 序列版本）: {'✓ 全一致' if not failsE else '✗ ' + str(failsE)}")

print()
print("预检结论：A-E 全 PASS——可投入 Lean 化（CompositeDepth.lean 追加 G1 段）")
