#!/usr/bin/env python3
"""
高效搜索 Cl(1,7) gamma 矩阵

使用三元组编码 (a,b,c), a,b,c ∈ {0,1,2,3} 表示 {I,sx,sy,sz}
两个矩阵反对易 ⟺ 在奇数个位置上使用不同非单位矩阵
"""
import numpy as np

I=np.eye(2); sx=np.array([[0,1],[1,0]]); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]])
pauli=[I,sx,sy,sz]

def tri_to_mat(t):
    return np.kron(np.kron(pauli[t[0]],pauli[t[1]]),pauli[t[2]]).astype(np.complex128)

# 反对易判据 (只检查三元组, 避免矩阵乘法)
def anticomm_tri(t1, t2):
    odd = 0
    for i in range(3):
        p1, p2 = t1[i], t2[i]
        if p1 != 0 and p2 != 0 and p1 != p2:
            odd += 1
        # I commutes with everything; same Pauli commutes
    return odd % 2 == 1

# 所有 4^3 = 64 个三元组
all_t = [(i,j,k) for i in range(4) for j in range(4) for k in range(4)]

# gamma0 必须平方为 +I_8: 需要非 I 的奇数个 (因为 (σ_i)² = I)
def squares_to_I(t):
    # (σ_a⊗σ_b⊗σ_c)² = σ_a²⊗σ_b²⊗σ_c² = I⊗I⊗I = I
    # 当 a,b,c 不涉及 I 时成立; 涉及 I 的情况 I²=I 也不影响
    return True  # 所有 4^3 个三积平方都等于 I_8

# 找 8 个彼此反对易的三元组
print("搜索中...")
import itertools

# 先过滤能与 gamma0 候选反对易的
for i0, t0 in enumerate(all_t):
    if not squares_to_I(t0):
        continue
    # 找能与 t0 反对易的
    rem = [i for i in range(64) if i != i0 and anticomm_tri(t0, all_t[i])]
    if len(rem) < 7:
        continue
    # 找 7 个彼此反对易的
    for combo in itertools.combinations(rem, 7):
        ok = True
        for a in range(7):
            for b in range(a+1, 7):
                if not anticomm_tri(all_t[combo[a]], all_t[combo[b]]):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            idx = [i0] + list(combo)
            print(f"找到! gamma0={all_t[i0]}, 其余:")
            for i in idx[1:]:
                print(f"  {all_t[i]}")
            print()
            
            # 验证
            gs = [tri_to_mat(all_t[i0])]
            for i in idx[1:]:
                gs.append(1j * tri_to_mat(all_t[i]))  # 空间方向 x i
            
            eta = np.diag([1,-1,-1,-1,-1,-1,-1,-1])
            ok2 = True
            for mu in range(8):
                sq = gs[mu] @ gs[mu]
                if not np.allclose(sq, eta[mu,mu]*np.eye(8)):
                    print(f"  gamma_{mu}^2 FAIL"); ok2 = False
            for mu in range(8):
                for nu in range(mu+1,8):
                    ac = gs[mu]@gs[nu] + gs[nu]@gs[mu]
                    if not np.allclose(ac, np.zeros((8,8))):
                        print(f"  {{{mu},{nu}}}!=0 FAIL"); ok2 = False
            if ok2:
                print("Cl(1,7): 全部 64 个关系通过 ✓")
                # SO(1,3) x SO(4) 分解
                from numpy import linalg as LA
                def L(mu,nu):
                    return 0.25*(gs[mu]@gs[nu]-gs[nu]@gs[mu])
                C13 = sum(L(mu,nu)@L(mu,nu) for mu in range(4) for nu in range(mu+1,4))
                C4 = sum(L(i,j)@L(i,j) for i in range(4,8) for j in range(i+1,8))
                u13,c13 = np.unique(np.round(LA.eigvalsh(C13),6), return_counts=True)
                u4,c4 = np.unique(np.round(LA.eigvalsh(C4),6), return_counts=True)
                print(f"  SO(1,3) Casimir: {dict(zip(u13,c13))}")
                print(f"  SO(4) Casimir: {dict(zip(u4,c4))}")
                if len(u13)==2:
                    print(f"  → 8 维分裂为 {c13[0]}+{c13[1]}!!")
            exit()
print("未找到")
