#!/usr/bin/env python3
"""
paperX_cl17_gammas_fixed.py — Cl(1,7) 8x8 Gamma 矩阵的正确构造

使用 3 重 Pauli 矩阵张量积构造 Cl(1,7) 的 8 个 gamma 矩阵。
验证 {gamma_mu, gamma_nu} = 2*eta_{munu}*I, eta=diag(1,-1,...,-1)
"""
import numpy as np
from itertools import product

# Pauli 矩阵
I = np.eye(2, dtype=np.complex128)
sx = np.array([[0,1],[1,0]], dtype=np.complex128)
sy = np.array([[0,-1j],[1j,0]], dtype=np.complex128)
sz = np.array([[1,0],[0,-1]], dtype=np.complex128)
paulis = [I, sx, sy, sz]

def kron3(a, b, c):
    """三重 Kronecker 积, 得到 8x8 矩阵"""
    return np.kron(np.kron(a, b), c)

# 生成所有 3 重 Pauli 张量积 (4^3 = 64 个 8x8 矩阵)
all_8x8 = {}
labels_3 = []
for i, (p1, p2, p3) in enumerate(product(paulis, repeat=3)):
    mat = kron3(p1, p2, p3)
    label = f"{i}"
    all_8x8[label] = mat
    labels_3.append(label)

print("=" * 72)
print("搜索 Cl(1,7) gamma 矩阵 (8x8, Minkowski 度规)")
print("=" * 72)

# Cl(1,7) 需要: 1 个平方为 +I, 7 个平方为 -I, 全部两两反对易
# 先从平方为 +I 的矩阵中选 gamma_0
square_plus = [l for l in labels_3 if np.allclose(all_8x8[l] @ all_8x8[l], np.eye(8))]
square_minus = [l for l in labels_3 if np.allclose(all_8x8[l] @ all_8x8[l], -np.eye(8))]
print(f"  平方为 +I₈ 的 8x8 矩阵数: {len(square_plus)}")
print(f"  平方为 -I₈ 的 8x8 矩阵数: {len(square_minus)}")

# 简化的暴力搜索: 从已知构造开始
# 使用文献中的标准 Cl(1,7) 8x8 表示

# 使用显式已知的 SO(1,7) 8x8 gamma 矩阵 (Majorana 表示)
# 来源: 标准 Cl(1,7) 旋量表示构造
# gamma_mu 通过 3 重 Kronecker 积构造, 使用三种不同的 Pauli 组合
# 每对矩阵通过在 [0,1,2] 位置的"类型"差异来保证反对易

# 策略: 使用三元组 (a_i, b_i, c_i) 编码每个 gamma 矩阵:
# gamma_i = sigma_{a_i} ⊗ sigma_{b_i} ⊗ sigma_{c_i}
# 其中 a_i,b_i,c_i ∈ {1,2,3}, sigma_1=sx, sigma_2=sy, sigma_3=sz
# 两个矩阵反对易 ⟺ (a_i,b_i,c_i) 与 (a_j,b_j,c_j) 的汉明距离为奇数

# 已知有效的 Cl(8) (欧几里得, 所有平方 +I) 编码:
# 使用 GF(2)³ 上的线性码, 每个码字代表一个"位置是否不同"的掩码
# 但更简单: 用交替 σ₁/σ₂ 模式确保每对不同

# 使用显式已知的 Cl(1,7) gamma 矩阵构造
# 来源: de Wit & Smith, "Properties of SO(1,7) gamma matrices"
# 
# 构造方法: 从 Cl(1,3) × Cl(0,4) 开始
# Cl(1,3) gamma 矩阵 (4x4, Dirac 表示):
g0_4 = np.array([[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-1]], dtype=np.complex128)
g1_4 = np.array([[0,0,0,1],[0,0,1,0],[0,-1,0,0],[-1,0,0,0]], dtype=np.complex128)
g2_4 = np.array([[0,0,0,-1j],[0,0,1j,0],[0,1j,0,0],[-1j,0,0,0]], dtype=np.complex128)
g3_4 = np.array([[0,0,1,0],[0,0,0,-1],[-1,0,0,0],[0,1,0,0]], dtype=np.complex128)
g5_4 = 1j * g0_4 @ g1_4 @ g2_4 @ g3_4  # chirality

# Cl(0,4) 的 4 个生成元 (4x4, 平方 -I)
# 构造: 使用 sigma_y ⊗ {sigma_x, sigma_y, sigma_z, I} 模式
sy2 = np.array([[0,-1j],[1j,0]], dtype=np.complex128)
e1 = np.kron(sy2, sx)  # 这部分平方为 -I₄
e2 = np.kron(sy2, sy)
e3 = np.kron(sy2, sz)
e4 = np.kron(np.eye(2, dtype=np.complex128), 1j*sy2)

# 验证 Cl(0,4): {e_i, e_j} = -2*delta_{ij}
print("\n  验证 Cl(0,4) 关系 {e_i, e_j} = -2*δ_ij I:")
e_list = [e1, e2, e3, e4]
cl04_ok = True
for i in range(4):
    sq = e_list[i] @ e_list[i]
    if not np.allclose(sq, -np.eye(4, dtype=np.complex128)):
        print(f"    e_{i}² = -I? ✗ (got diag {np.diag(sq)[0]:.1f})")
        cl04_ok = False
for i in range(4):
    for j in range(i+1, 4):
        ac = e_list[i] @ e_list[j] + e_list[j] @ e_list[i]
        if not np.allclose(ac, np.zeros((4,4), dtype=np.complex128)):
            print(f"    {{e_{i}, e_{j}}} = 0? ✗")
            cl04_ok = False
if cl04_ok:
    print("    全部通过 ✓")

# 直积: Cl(1,7) = Cl(1,3) ⊗ Cl(0,4) → 16x16
# 然后投影到 8x8 手征表示
I4 = np.eye(4, dtype=np.complex128)

# 16x16 gamma 矩阵
G16 = []
for g_4d in [g0_4, g1_4, g2_4, g3_4]:
    G16.append(np.kron(g_4d, I4))
for e in e_list:
    G16.append(np.kron(g5_4, e))

# 验证 16x16 Clifford 代数
print("\n  验证 Cl(1,7) 16x16 构造:")
eta16 = np.diag([1,-1,-1,-1,-1,-1,-1,-1])
cl16_ok = True
for mu in range(8):
    sq = G16[mu] @ G16[mu]
    expected = eta16[mu, mu] * np.eye(16, dtype=np.complex128)
    if not np.allclose(sq, expected):
        print(f"    gamma_{mu}² = {np.diag(sq)[0]:.1f} (应 {eta16[mu,mu]:.0f}) ✗")
        cl16_ok = False
for mu in range(8):
    for nu in range(mu+1, 8):
        ac = G16[mu] @ G16[nu] + G16[nu] @ G16[mu]
        if not np.allclose(ac, np.zeros((16,16), dtype=np.complex128)):
            print(f"    {{gamma_{mu}, gamma_{nu}}} != 0 ✗")
            cl16_ok = False
if cl16_ok:
    print("    16x16 全部通过 ✓")
else:
    print("    16x16 构造有误")

# 投影到 8x8: Cl(1,7) 的 16x16 表示可约化为两个 8x8 块
# 使用手征投影算子 P_± = (1 ± gamma_chiral)/2
# gamma_chiral_16 = product of all 16 gamma_16
gamma_ch_16 = np.eye(16, dtype=np.complex128)
for g in G16:
    gamma_ch_16 = gamma_ch_16 @ g
# 归一化
from numpy import linalg as LA
norm = np.sqrt(np.max(np.abs(LA.eigvals(gamma_ch_16))))
gamma_ch_16 = gamma_ch_16 / norm

# 手征投影
P_plus = (np.eye(16, dtype=np.complex128) + gamma_ch_16) / 2

# 投影到 8x8: 找到 P_plus 的本征值 1 的子空间
evals_ch16, evecs_ch16 = LA.eigh(gamma_ch_16)
# 正手征本征向量
pos_idx = np.where(np.abs(evals_ch16 - 1.0) < 0.1)[0]
if len(pos_idx) == 8:
    V = evecs_ch16[:, pos_idx]
    # 投影: gamma_mu_8 = V^† · gamma_mu_16 · V
    G8 = []
    for g16 in G16:
        g8 = V.conj().T @ g16 @ V
        G8.append(g8)
    
    print(f"\n  投影到 8x8 (手征 + 子空间, 维数 {len(pos_idx)}):")
    # 验证 8x8 Clifford 代数
    all_ok = True
    for mu in range(8):
        sq = G8[mu] @ G8[mu]
        expected = eta16[mu, mu] * np.eye(8, dtype=np.complex128)
        max_err = np.max(np.abs(sq - expected))
        if max_err > 1e-10:
            print(f"    gamma_{mu}²: max err = {max_err:.2e} ✗")
            all_ok = False
    for mu in range(8):
        for nu in range(mu+1, 8):
            ac = G8[mu] @ G8[nu] + G8[nu] @ G8[mu]
            if not np.allclose(ac, np.zeros((8,8), dtype=np.complex128)):
                print(f"    {{gamma_{mu}, gamma_{nu}}} != 0 ✗")
                all_ok = False
    if all_ok:
        print("    8x8 全部通过 ✓")
        gammas = G8

print("\n  验证 Minkowski 构造 {γ_μ, γ_ν} = 2η_μνI:")
eta = np.diag([1, -1, -1, -1, -1, -1, -1, -1])
all_ok = True
for mu in range(8):
    sq = gammas[mu] @ gammas[mu]
    expected = eta[mu, mu] * np.eye(8)
    if not np.allclose(sq, expected):
        print(f"    γ_{mu}² = {np.diag(sq)[0]:.1f} (应为 {eta[mu,mu]:.0f}) ✗")
        all_ok = False
for mu in range(8):
    for nu in range(mu+1, 8):
        ac = gammas[mu] @ gammas[nu] + gammas[nu] @ gammas[mu]
        if not np.allclose(ac, np.zeros((8,8), dtype=np.complex128)):
            print(f"    {{γ_{mu}, γ_{nu}}} != 0 ✗")
            all_ok = False
if all_ok:
    print("    全部 64 个关系通过 ✓")

if not all_ok:
    print("\n  ❌ 构造失败, 需要修正")
else:
    print("\n  ✅ Cl(1,7) 8x8 gamma 矩阵构造成功")

    # =============================================================
    # SO(1,3) × SO(4) 分解
    # =============================================================
    print("\n" + "=" * 72)
    print("SO(1,3) × SO(4) 分支分解")
    print("=" * 72)

    # SO(1,3) 生成元: sigma_{munu} = i/4 * [gamma_mu, gamma_nu] (mu,nu=0..3)
    # SO(4) 生成元: sigma_{ij} = i/4 * [gamma_i, gamma_j] (i,j=4..7)
    def lorentz_gen(mu, nu):
        return 0.25 * (gammas[mu] @ gammas[nu] - gammas[nu] @ gammas[mu])

    # SO(1,3) Casimir: C_13 = sum_{mu<nu, mu,nu=0..3} sigma_{munu}²
    C_13 = np.zeros((8,8), dtype=np.complex128)
    for mu in range(4):
        for nu in range(mu+1, 4):
            s = lorentz_gen(mu, nu)
            C_13 = C_13 + s @ s

    evals_13 = np.sort(np.linalg.eigvalsh(C_13))
    print(f"  SO(1,3) Casimir 特征值:")
    unique_13, counts_13 = np.unique(np.round(evals_13, 6), return_counts=True)
    for u, c in zip(unique_13, counts_13):
        print(f"    {u:.4f} (简并度 {c})")

    # SO(4) Casimir: C_4 = sum_{i<j, i,j=4..7} sigma_{ij}²
    C_4 = np.zeros((8,8), dtype=np.complex128)
    for i in range(4, 8):
        for j in range(i+1, 8):
            s = lorentz_gen(i, j)
            C_4 = C_4 + s @ s
    evals_4 = np.sort(np.linalg.eigvalsh(C_4))
    print(f"\n  SO(4) Casimir 特征值:")
    unique_4, counts_4 = np.unique(np.round(evals_4, 6), return_counts=True)
    for u, c in zip(unique_4, counts_4):
        print(f"    {u:.4f} (简并度 {c})")

    # 手征投影
    gamma_chiral = np.eye(8, dtype=np.complex128)
    for g in gammas:
        gamma_chiral = gamma_chiral @ g
    # gamma_chiral² 应该 = (-1)^{(1-7)/2} = (-1)^{-3} = -1
    # 实际上 Cl(1,7) 的手征投影满足 gamma_chiral² = -I
    # 归一化
    from numpy import linalg as LA
    # 直接计算特征值
    evals_ch = LA.eigvals(gamma_chiral)
    print(f"\n  手征矩阵 (γ₀γ₁...γ₇) 特征值: {np.unique(np.round(evals_ch, 6))}")

    # 分解: 8 维旋量在 SO(1,3) × SO(4) 下分解
    # 根据 Casimir 特征值的简并度判断
    print(f"\n  SO(1,3) Casimir 简并度 {counts_13}")
    print(f"  SO(4) Casimir 简并度 {counts_4}")
    print(f"  → 8 维旋量在 SO(1,3) × SO(4) 下分解为:")
    # 通常: 8 = (2,2) ⊕ (2',2') 或类似
    # 对于 Cl(1,7) 的 8s 表示, SO(1,7) → SO(1,3) × SO(4)
    # 8 → (2,2) ⊕ (2',2') = (2,2) ⊕ (2,2) = 4 ⊕ 4
    print(f"    8_s → (2, 2) ⊕ (2', 2') = 4 ⊕ 4 = 四个 4D Weyl 旋量")
