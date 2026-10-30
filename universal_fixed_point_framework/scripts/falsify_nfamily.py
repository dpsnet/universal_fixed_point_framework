# -*- coding: utf-8 -*-
"""falsify_nfamily.py — NFamilyTheorems.lean 先证伪：53 三身份 + 371 立方 + 模5恒等 全样本数值检验"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

fails = 0
# I1：b₀×静默 + k_max = 对合域² + 幂基²（45+8 = 49+4）
if 9*5+8 != 7**2+2**2: fails += 1; print("I1 FAIL")
# I2：对合域×k_max − N_gen = 对合域² + 幂基²（56−3 = 49+4）
if 7*8-3 != 7**2+2**2: fails += 1; print("I2 FAIL")
# I3：371 = 对合域³ + 对合域×幂基²（343+28）
if 7**3+7*2**2 != 371: fails += 1; print("I3 FAIL")
# I4：53 = 对合域² + 幂基²
if 7**2+2**2 != 53: fails += 1; print("I4 FAIL")
# I5：A 分子 371 = 对合域×53
if 7*53 != 371: fails += 1; print("I5 FAIL")

# 模 5 恒等：∀ k 偶 → 5 | (49 + 4^k)，k=0..2000
bad = 0
for k in range(0, 2001):
    v = 49 + 4**k
    if k % 2 == 0 and v % 5 != 0: bad += 1; print(f"even FAIL k={k} v%5={v%5}")
    if k % 2 == 1 and v % 5 == 0: bad += 1; print(f"odd FAIL k={k} v%5={v%5}")
print(f"模5恒等 k=0..2000 全部一致：{bad == 0}（{bad} 个不一致）")
print(f"恒等 I1~I5 全部通过：{fails == 0}（{fails} 个失败）")
sys.exit(0 if fails == 0 and bad == 0 else 1)
