# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
paperX_cl17_correct.py — Cl(1,7) 8x8 gamma 矩阵 (文献标准构造)

来源: Freedman & Van Proeyen, "Supergravity", Appendix C
使用 epsilon = i*sigma_2 的三重张量积构造。
"""
import numpy as np

I = np.eye(2, dtype=np.complex128)
s1 = np.array([[0,1],[1,0]], dtype=np.complex128)
s2 = np.array([[0,-1j],[1j,0]], dtype=np.complex128)
s3 = np.array([[1,0],[0,-1]], dtype=np.complex128)
eps = 1j * s2  # epsilon = i*sigma_2, 满足 eps^2 = -I_2

def k3(a, b, c):
    return np.kron(np.kron(a, b), c).astype(np.complex128)

# Cl(1,7) gamma 矩阵 (度规 +--- ----)
g0 = 1j * k3(eps, eps, eps)    # 时间, 平方 +I
g1 = k3(I, s1, eps)             # 空间, 平方 -I
g2 = k3(I, s3, eps)
g3 = k3(s1, eps, I)
g4 = k3(s3, eps, I)
g5 = k3(eps, I, s1)
g6 = k3(eps, I, s3)
g7 = k3(eps, s1, I)
gammas = [g0, g1, g2, g3, g4, g5, g6, g7]

# 验证 γ7
chk7 = gammas[1]@gammas[7] + gammas[7]@gammas[1]
if not np.allclose(chk7, np.zeros((8,8))):
    print("gamma_7 不满足反对易, 尝试用 gamma_7 = i * prod(gamma_0..gamma_6)")
    g7_new = 1j * np.eye(8, dtype=np.complex128)
    for mu in range(7):
        g7_new = g7_new @ gammas[mu]
    # 验证新 gamma_7
    sq7 = g7_new @ g7_new
    if np.allclose(sq7, -np.eye(8, dtype=np.complex128)):
        print("  gamma_7^2 = -I ✓")
        # 验证与其它反对易
        all_ac = True
        for mu in range(7):
            ac = gammas[mu]@g7_new + g7_new@gammas[mu]
            if not np.allclose(ac, np.zeros((8,8))):
                print(f"  {{gamma_{mu}, gamma_7}} != 0 ✗")
                all_ac = False
        if all_ac:
            print("  与 gamma_0..gamma_6 全部反对易 ✓")
            gammas[7] = g7_new

gammas = [g0, g1, g2, g3, g4, g5, g6, g7]

# 验证
eta = np.diag([1,-1,-1,-1,-1,-1,-1,-1])
ok = True
for mu in range(8):
    sq = gammas[mu] @ gammas[mu]
    expected = eta[mu,mu] * np.eye(8, dtype=np.complex128)
    if not np.allclose(sq, expected):
        print(f"gamma_{mu}^2 = {np.diag(sq)[0]:.1f} (should be {eta[mu,mu]}) FAIL")
        ok = False
for mu in range(8):
    for nu in range(mu+1, 8):
        ac = gammas[mu]@gammas[nu] + gammas[nu]@gammas[mu]
        if not np.allclose(ac, np.zeros((8,8), dtype=np.complex128)):
            print(f"{{gamma_{mu}, gamma_{nu}}} != 0 FAIL")
            ok = False
if ok:
    print("Cl(1,7): 全部 64 个关系通过 ✓")

# SO(1,3) × SO(4) Casimir 分解
from numpy import linalg as LA

def lorentz(mu, nu):
    return 0.25 * (gammas[mu]@gammas[nu] - gammas[nu]@gammas[mu])

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
for g in gammas: ch = ch @ g
print(f"\n手征特征值: {np.unique(np.round(LA.eigvals(ch), 6))}")

# 检查分解
print(f"\nCl(1,7) 8 维表示在 SO(1,3)xSO(4) 下的分解:")
print(f"  SO(1,3) 块: {c13}")
print(f"  SO(4) 块: {c4}")
if len(c13)==1:
    print(f"  → 所有维度在 SO(1,3) 下属于同一表示(8)")
elif len(c13)==2:
    print(f"  → 分裂为 {c13[0]}+{c13[1]} 维表示")
