#!/usr/bin/env python3
"""
paperX_cl17_weyl.py — Cl(1,7) 8x8 Gamma 矩阵 (Weyl 表示)

构造: gamma_mu = [[0, sigma_mu], [sigma_mu_bar, 0]]
sigma_0 = I_4, sigma_i_bar = -sigma_i (for i=1..7)
sigma_i = i * (Kronecker product of Pauli matrices)
"""
import numpy as np
from numpy import linalg as LA

I2 = np.eye(2, dtype=np.complex128)
sx = np.array([[0,1],[1,0]], dtype=np.complex128)
sy = np.array([[0,-1j],[1j,0]], dtype=np.complex128)
sz = np.array([[1,0],[0,-1]], dtype=np.complex128)

def kron2(a,b):
    return np.kron(a,b).astype(np.complex128)

# 4x4 sigma_i 块 (i=1..7), 平方为 +I_4 (以便 gamma_i 平方为 -I_8)
# 注意: 与 AI 给出的不同, 去掉 i 因子——因为 Weyl 块结构自带-i²
sigma = [None]  # sigma[0] placeholder
sigma.append(kron2(sx, sx))   # sigma_1
sigma.append(kron2(sx, sy))   # sigma_2
sigma.append(kron2(sx, sz))   # sigma_3
sigma.append(kron2(sy, I2))   # sigma_4
sigma.append(kron2(sz, sx))   # sigma_5
sigma.append(kron2(sz, sy))   # sigma_6
sigma.append(kron2(sz, sz))   # sigma_7

# 验证 sigma_i 平方 = -I_4
print("验证 4x4 sigma_i 块:")
for i in range(1,8):
    sq = sigma[i] @ sigma[i]
    ok = np.allclose(sq, -np.eye(4, dtype=np.complex128))
    print(f"  sigma_{i}^2 = -I_4? {ok}")

# 构造 8x8 gamma 矩阵
I4 = np.eye(4, dtype=np.complex128)
Z = np.zeros((4,4), dtype=np.complex128)

g = []
# gamma_0: [[0, I], [I, 0]]
g0 = np.block([[Z, I4], [I4, Z]])
g.append(g0)

# gamma_i: [[0, sigma_i], [-sigma_i, 0]] (i=1..7)
for i in range(1,8):
    gi = np.block([[Z, sigma[i]], [-sigma[i], Z]])
    g.append(gi)

gammas = g

# 验证 Clifford 代数
print("\n验证 Cl(1,7) 代数 {γ_μ, γ_ν} = 2η_μνI:")
eta = np.diag([1,-1,-1,-1,-1,-1,-1,-1])
ok = True
for mu in range(8):
    sq = gammas[mu] @ gammas[mu]
    if not np.allclose(sq, eta[mu,mu]*np.eye(8)):
        print(f"  γ_{mu}^2 FAIL (got diag {np.diag(sq)[0]:.1f}, expected {eta[mu,mu]})")
        ok = False
for mu in range(8):
    for nu in range(mu+1,8):
        ac = gammas[mu]@gammas[nu] + gammas[nu]@gammas[mu]
        if not np.allclose(ac, np.zeros((8,8))):
            print(f"  {{γ_{mu},γ_{nu}}} != 0 FAIL")
            ok = False
if ok: print("  全部 64 个关系通过 ✓")

# SO(1,3) x SO(4) 分解
def lorentz(mu,nu):
    return 0.25*(gammas[mu]@gammas[nu]-gammas[nu]@gammas[mu])

C13 = sum(lorentz(mu,nu)@lorentz(mu,nu) for mu in range(4) for nu in range(mu+1,4))
C4  = sum(lorentz(i,j)@lorentz(i,j) for i in range(4,8) for j in range(i+1,8))

print(f"\nSO(1,3) Casimir:")
u13,c13 = np.unique(np.round(LA.eigvalsh(C13),6), return_counts=True)
for u,c in zip(u13,c13): print(f"  {u:.4f} (x{c})")

print(f"\nSO(4) Casimir:")
u4,c4 = np.unique(np.round(LA.eigvalsh(C4),6), return_counts=True)
for u,c in zip(u4,c4): print(f"  {u:.4f} (x{c})")

# 手征矩阵
ch = np.eye(8, dtype=np.complex128)
for gm in gammas: ch = ch @ gm
print(f"\n手征特征值: {np.unique(np.round(LA.eigvals(ch), 6))}")

print(f"\n分解结论:")
if len(u13)==2:
    print(f"  SO(1,3): 8 维分裂为 {c13[0]}+{c13[1]}")
    print(f"  → 4 + 4 = 8 旋量在 4D 时空中分解为两个 4 维 Weyl 旋量 ✓")
if len(u4)==2:
    print(f"  SO(4): 8 维分裂为 {c4[0]}+{c4[1]}")
    print(f"  → 4 + 4 = 8 旋量在内部空间中也有分裂")
print(f"  【2026-08-07 勘误：本脚本基于旧框架 Cl(1,7) ≅ M₈(ℝ) 的 8 维旋量构造（历史探索脚本，未注册 run_all_tests.py）；")
print(f"   标准 Cl(1,7) ≅ M₁₆(ℝ) 旋量 16 维（paper20 权威），4D 分解为 4 个 Weyl（RAP3 机器证明）。")
    
print(f"\n谱静默检查:")
S4 = np.exp(-2.7095)
# gamma_0 特征值: +/-1 (时间)
# gamma_i 特征值: +/-i (空间, 反 Hermite)
# 谱权重 = |特征值| = 1 全部可见
# 但谱静默更相关的是 chirality 分裂
ch_ev = LA.eigvalsh(ch)
n_chir_plus = np.sum(ch_ev > 0)
n_chir_minus = np.sum(ch_ev < 0)
print(f"  正手征维数: {n_chir_plus}")
print(f"  负手征维数: {n_chir_minus}")
print(f"  → 8 维旋量按手征分裂为 {n_chir_plus}+{n_chir_minus}【2026-08-07 勘误：旧 8 维旋量构造；标准旋量 16 维，见上】")
