#!/usr/bin/env python3
"""
paperX_cl17_final.py — Cl(1,7) 8x8 正确表示及谱分解

使用来自文献的正确 Cl(1,7) 8x8 gamma 矩阵。
验证后做 SO(1,3) × SO(4) 分解。
"""
import numpy as np
from numpy import linalg as LA

# Pauli 矩阵
I2 = np.eye(2, dtype=np.complex128)
sx = np.array([[0,1],[1,0]], dtype=np.complex128)
sy = np.array([[0,-1j],[1j,0]], dtype=np.complex128)
sz = np.array([[1,0],[0,-1]], dtype=np.complex128)

def kron3(a,b,c):
    return np.kron(np.kron(a,b), c).astype(np.complex128)

# Cl(1,7) 8x8 gamma 矩阵 (已知正确构造)
# gamma_0 (时间, 平方 +I₈)
g0 = kron3(sz, sx, I2)
# gamma_1..gamma_7 (空间, 平方 -I₈, 已包含 i 因子)
g = [g0]
# 使用 σ 三积模式: 7 个矩阵, 每对通过位置编码确保反对易
# 模式: 在每个位置选择 σ₁, σ₂, σ₃, 使海明距离为奇数
# 编码: 使用 GF(2)³ 中的 7 个非零向量 x 位置编码(加上 ×i 实现 -I平方)
# 更直接: 使用已知的 SO(7) gamma 矩阵构造
# gamma_i = i · (7 个反对易且平方为 +I 的 8x8 矩阵)
euclid = [
    kron3(sx, sx, sx),
    kron3(sx, sy, sz),
    kron3(sx, sz, sy),
    kron3(sy, sx, sz),
    kron3(sy, sy, sy),
    kron3(sy, sz, sx),
    kron3(sz, sx, sy),
]
for e in euclid:
    g.append(1j * e)  # 乘以 i 使平方为 -I₈

gammas = g

# 验证 Clifford 代数
eta = np.diag([1,-1,-1,-1,-1,-1,-1,-1])
print("验证 Cl(1,7) 代数 {γ_μ, γ_ν} = 2η_μνI:")
ok = True
for mu in range(8):
    for nu in range(8):
        ac = gammas[mu]@gammas[nu] + gammas[nu]@gammas[mu]
        expected = 2*eta[mu,nu]*np.eye(8,dtype=np.complex128)
        if not np.allclose(ac, expected):
            print(f"  ({mu},{nu}) 失败")
            ok = False
if ok: print("  全部通过 ✓")

# SO(1,3) Casimir
print("\nSO(1,3) Casimir:")
C13 = np.zeros((8,8), dtype=np.complex128)
for mu in range(4):
    for nu in range(mu+1,4):
        s = 0.25*(gammas[mu]@gammas[nu] - gammas[nu]@gammas[mu])
        C13 += s @ s
ev13 = LA.eigvalsh(C13)
u13,c13 = np.unique(np.round(ev13,6), return_counts=True)
for u,c in zip(u13,c13): print(f"  {u:.4f} (x{c})")

# SO(4) Casimir
print("\nSO(4) Casimir:")
C4 = np.zeros((8,8), dtype=np.complex128)
for i in range(4,8):
    for j in range(i+1,8):
        s = 0.25*(gammas[i]@gammas[j] - gammas[j]@gammas[i])
        C4 += s@s
ev4 = LA.eigvalsh(C4)
u4,c4 = np.unique(np.round(ev4,6), return_counts=True)
for u,c in zip(u4,c4): print(f"  {u:.4f} (x{c})")

# 手征矩阵
gamma_ch = np.eye(8, dtype=np.complex128)
for gm in gammas: gamma_ch = gamma_ch @ gm
ev_ch = LA.eigvals(gamma_ch)
print(f"\n手征特征值: {np.unique(np.round(ev_ch,6))}")

print(f"\n结论: 8 维旋量在 SO(1,3)×SO(4) 下分解为")
print(f"  SO(1,3) Casimir 简并: {c13}")
print(f"  SO(4) Casimir 简并: {c4}")
