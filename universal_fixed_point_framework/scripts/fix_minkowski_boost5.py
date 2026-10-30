# -*- coding: utf-8 -*-
"""第五轮修复 v3：修正 count 语义（-1=全部），对当前文件应用剩余替换。"""
import io

path = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\MinkowskiBoost.lean"
with io.open(path, encoding='utf-8') as f:
    src = f.read()

def rep(old, new, tag="", expect=None):
    global src
    n = src.count(old)
    if expect is not None:
        assert n >= expect, f"MISS[{tag}]: {old[:90]!r} found={n} want>={expect}"
    if n > 0:
        src = src.replace(old, new)  # 全部
        print(f"OK[{tag}] x{n}")
    else:
        print(f"SKIP[{tag}] x0")

# ---- 1. 全部 4 空格 ring_nf → try ring_nf ----
rep("    ring_nf", "    try ring_nf", tag="try_ring_nf_all", expect=1)

# ---- 2. 全部 4 空格裸 norm_num → try ----
rep("    norm_num\n", "    try norm_num\n", tag="try_norm_num_all", expect=1)

# ---- 3. 剩余 DiracOp4Full simp 行加 Fin.sum_univ_succ ----
rep("    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply]",
    "    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]",
    tag="DiracFull_sum", expect=1)

with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(src)
print("WROTE")
