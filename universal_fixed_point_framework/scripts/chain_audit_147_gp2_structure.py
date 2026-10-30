# -*- coding: utf-8 -*-
"""
chain_audit_147_gp2_structure.py — v2：扩展候选空间 + 修正结构判据
判据修正（对齐 104az-146 口径）：分母素因子 ⊂ {2,3,5,7}（平滑）；分子 = 框架量组合（307=45·7−8, 131=128+3）
"""
from fractions import Fraction as F
import itertools, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TARGET = 2.79284734463
FRAME = {2, 3, 4, 5, 7, 8, 16, 25, 49, 64}
D_FAMILY = {45, 231, 320, 675, 65, 256, 14400, 16, 25, 64, 40, 100}

# ---- 扩展候选空间：a,b 均允许 k/d, k∈框架量, d∈D_FAMILY 任意组合 ----
def build_space():
    S = set()
    for k in FRAME:
        for d in D_FAMILY:
            S.add(F(k, d))
    return S

A, B = build_space(), build_space()
print(f"A 空间 = {len(A)} 元素, B 空间 = {len(B)} 元素, 组合 = {len(A)*len(B)}")
assert F(8, 45) in A and F(3, 64) in B

# ---- 枚举 ----
hits = []
for a, b in itertools.product(A, B):
    val = (F(7,1) - a) / (F(5,1) / (F(2,1) + b))
    err = abs(float(val) - TARGET)
    if err < 1e-6:
        hits.append((err, a, b, val))
hits.sort()
print(f"\n=== 命中（err<1e-6）：{len(hits)} 个 ===")
for err, a, b, val in hits:
    print(f"  a={a} b={b}  val={float(val):.12f}  err={err:.3e}")

# ---- 结构判据（对齐 146）：分母素因子⊂{2,3,5,7}；分子为框架量组合（307=45·7−8, 131=128+3 型）----
def den_ok(n):
    for p in (2, 3, 5, 7):
        while n % p == 0: n //= p
    return n == 1

# 分子框架表达词典（先定规则：分子 ∈ 框架量线性组合 {±k, ±k·静默, ±N_gen, ±k_max...} 生成数）
def num_ok(n):
    """分子可写为 45·7−8=307 或 128+3=131 型：即 n ∈ {k·d ± k', k·d² ± k'...}"""
    for k in FRAME:
        for kp in FRAME:
            if n == k * 45 - kp or n == k * 64 + kp or n == k * 45 + kp or n == k * 64 - kp:
                return True
    return False

print("\n=== 结构达标（分母平滑 + 分子框架表达）===")
struct = []
for err, a, b, val in hits:
    if den_ok(val.denominator) and num_ok(val.numerator):
        struct.append((err, a, b, val))
for err, a, b, val in struct:
    print(f"  a={a} b={b}  val={val}  err={err:.3e}  已知={'★' if val==F(40217,14400) else ''}")

print(f"\n结论：扩展空间 {len(A)*len(B)} 组合 → 数值命中 {len(hits)}；结构达标 {len(struct)}；已知 40217/14400 达标={any(v==F(40217,14400) for _,_,_,v in struct)}")
