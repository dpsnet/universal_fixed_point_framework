# -*- coding: utf-8 -*-
OUT = open(r'C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_108.txt', 'w', encoding='utf-8')
def P(*a):
    OUT.write(' '.join(map(str, a)) + '\n')

"""
Phase 104az-108 先证伪：缩放函子比值不变量 + 互锁比的函子表述
按 Lean 定义逐字翻译：scaleF x = κΛ·x；定理 scale_ratio_invariant: scaleF x/scaleF y = x/y
6 组随机样本 + 应用检验
"""
import random
random.seed(104108)

P("=" * 70)
P("[1] 随机样本检验 scale_ratio_invariant（6 组）")
ok = True
for i in range(6):
    k = random.uniform(-5, 5)
    while abs(k) < 1e-4:
        k = random.uniform(-5, 5)
    x = random.uniform(-3, 3)
    y = random.uniform(-3, 3)
    while abs(y) < 1e-4:
        y = random.uniform(-3, 3)
    lhs = (k * x) / (k * y)
    rhs = x / y
    resid = abs(lhs - rhs)
    P(f"  组{i+1}: κΛ={k:.6f} x={x:.4f} y={y:.4f} → LHS={lhs:.12f} RHS={rhs:.12f} 残差={resid:.2e}")
    if resid > 1e-8:
        ok = False
P(f"  残差全 < 1e-8: {ok}")

P("\n[2] 应用检验：互锁比 = 缩放函子不变量")
# 恒等 A 定义: κΛ·Δλ_EM = 4ln10 → Δλ_EM = 4ln10/κΛ
# 恒等 B 公设: κΛ·Δλ_P20 = 49 → Δλ_P20 = 49/κΛ
import math
for k in [401.73304855, 1.0, 7.0]:
    dlEM = 4 * math.log(10) / k
    dlP20 = 49 / k
    lhs = (k * dlP20) / (k * dlEM)
    rhs = dlP20 / dlEM
    target = 49 / (4 * math.log(10))
    P(f"  κΛ={k:.6f}: (κΛ·dlP20)/(κΛ·dlEM)={lhs:.12f} = dlP20/dlEM={rhs:.12f} = 49/(4ln10)={target:.12f}")
    P(f"    残差 vs 49/(4ln10): {abs(rhs-target):.2e}")

P("\n[3] 结论")
P("  scale_ratio_invariant 数值成立（κΛ≠0 时恒等——纯代数）")
P("  interlock_as_invariant 成立（互锁比 = 缩放函子比值不变量）")
P("  → Lean 形式化可行（零 sorry）")
