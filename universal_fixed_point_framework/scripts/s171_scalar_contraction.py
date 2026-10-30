# -*- coding: utf-8 -*-
"""S171 先证伪：标量压缩性 exp(−t·a) < 1（a,t > 0）
"每步 e"的压缩层：谱流推进乘子 exp(−λ)——λ>0 时每步压缩——
对应静默冻结（每步荷衰减）——Koopman 压缩半群的标量核
"""
import math
import random

print("=== S171 先证伪：标量压缩 exp(-t·a) < 1（a,t>0） ===\n")

random.seed(42)
ok = True
for i in range(10):
    a = random.uniform(0.1, 5.0)
    t = random.uniform(0.1, 10.0)
    v = math.exp(-t * a)
    ok &= (v < 1.0) and (v > 0.0)
    print(f"  a={a:.4f} t={t:.4f} exp(-t·a)={v:.6f} < 1: {v < 1.0}")

print(f"\n10 组随机样本全部 exp(-t·a)<1 且 >0: {ok}")

# 极限行为：t→∞ 压缩到 0（静默冻结——零测度）
print("\n=== 极限行为（t→∞——静默冻结零测度） ===")
for t in [1, 10, 100, 1000]:
    print(f"  t={t}: exp(-t) = {math.exp(-t):.6e}")

print("\n=== 语义衔接 ===")
print("  exp(-t·a) < 1（每步压缩——Koopman 压缩半群标量核）")
print("  t→∞：exp(-t·a)→0（静默冻结——零测度——S151 闭合冻结）")
print("  → 静默机制的算子层：每步压缩 + 极限零测度")
print("  → '静默即不变且失去窗口'（用户裁决——2026-10-23）的")
print("    算子表述：窗口=exp 幅值——t→∞ 窗口→0（失去表达窗口）")
