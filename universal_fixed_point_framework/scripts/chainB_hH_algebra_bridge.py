"""
chainB_hH_algebra_bridge.py — 路径1 探查：ℍ⊗_ℝℍ = M₄(ℝ) 与 Cl(1,7) 旋量16 的代数桥
RN-ENDO-010 §8.17/§8.18 后续。待验：Chain B 的『16』是否 = dim_ℝℍ²=16 的物理内源。

候选桥（用户指定路径1，2026-09-18）：
    16 = dim_ℝℍ²  ⟵  ℍ⊗_ℝℍ ≅ M₄(ℝ)（真实代数，实维 16）
    ℍ = Cl(0,3)^0（Chain A 缝合定理，机器证明）
    Chain-B 宿主的 16 = spinorDim(Cl(1,7)) = 2^⌊8/2⌋ = 2·k_max = 16（paper33/06_bott_tower 机器封闭）

探查问题（纪律 VII 要为『恒等 vs 结构』给出可判定判据）：
  (Q1) ℍ 是否真是四元数代数、dim_ℝℍ 是否 = 4？          → [V1]
  (Q2) ℍ⊗_ℝℍ 是否 ≅ M₄(ℝ)（实维 16，矩阵级 4×4）？      → [V2]
  (Q3) Cl(1,7) 的对象级：M₁₆(ℝ)，最小实模 16。           → [V3]（框架已机器封闭，此处列级核对）
  (Q4) 16 的两个来源（M₄(ℝ)-张量面 vs M₁₆(ℝ)-旋量宿主）是否同对象？→ [V4] 对象级（矩阵尺寸）判别
  (Q5) 旋量模的 ℍ-模结构：ℝ¹⁶ = ℍ^4（多重度 4）。        → [V5] 多重度来源
"""
import numpy as np

I2 = np.eye(2, dtype=complex)
s1 = np.array([[0,1],[1,0]], dtype=complex)
s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
s3 = np.array([[1,0],[0,-1]], dtype=complex)

def anticomm(A, B, tol=1e-9):
    return np.allclose(A@B + B@A, 0, atol=tol)
def commute(A, B, tol=1e-9):
    return np.allclose(A@B - B@A, 0, atol=tol)

print("=" * 78)
print("路径1 探查：ℍ⊗_ℝℍ = M₄(ℝ) 与 Cl(1,7) 旋量16 的代数桥")
print("=" * 78)

# ---------------- [V1] Cl(0,3)^0 ≅ ℍ ----------------
print("\n[V1] Cl(0,3)^0 ≅ ℍ：γᵢ = iσᵢ（空间型, 平方 −I, 反交换）")
g1, g2, g3 = 1j*s1, 1j*s2, 1j*s3
pair_ok = all(anticomm(a, b) for a, b in [(g1,g2),(g1,g3),(g2,g3)])
sq_ok = all(np.allclose(a@a, -I2) for a in [g1,g2,g3])
# 偶部生成元：{1, γ₁γ₂, γ₁γ₃, γ₂γ₃}
Ie = g1@g2; Je = g1@g3; Ke = g2@g3
rel_I = np.allclose(Ie@Ie, -I2) and np.allclose(Je@Je, -I2) and np.allclose(Ke@Ke, -I2)
rel_ijk = np.allclose(Ie@Je@Ke, -I2)
# 真实维度：span{1,Ie,Je,Ke} 的实线性无关（8 个实分量）
span = np.stack([e.flatten() for e in [I2, Ie, Je, Ke]])  # 4×4 复, 8 实列
real8 = np.concatenate([span.real, span.imag], axis=1)     # 4×8
import numpy.linalg as la
rdim = np.linalg.matrix_rank(real8, tol=1e-9)
print(f"     γᵢ 反交换 = {pair_ok};  γᵢ² = −I = {sq_ok}")
print(f"     偶部 {1,Ie,Je,Ke}:  I²=J²=K²=−1 = {rel_I};  IJK=−1 = {rel_ijk}")
print(f"     dim_ℝ span{{1,I,J,K}} = {rdim}  (应 4)")
print(f"     → {'✓ Cl(0,3)^0 ≅ ℍ, dim_ℝℍ = 4（与 QuaternionSpinOrigin.lean 一致）' if pair_ok and sq_ok and rel_I and rel_ijk and rdim==4 else '✗'}")

# ---------------- [V2] ℍ⊗_ℝℍ ≅ M₄(ℝ) ----------------
print("\n[V2] ℍ⊗_ℝℍ：左乘 L(a) 与右乘 R(b) 作用在实 4 维空间 ℍ 上")
# 用哈密顿乘法表自洽生成 L(a)v=a⊗v 与 R(b)v=v⊗b（避免手写矩阵错误）
def hmul(a, b):
    a0,a1,a2,a3 = a; b0,b1,b2,b3 = b
    return np.array([
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0,
    ])
E = np.eye(4)
def leftmul(a):
    return np.column_stack([hmul(a, E[:,k]) for k in range(4)])
def rightmul(b):
    return np.column_stack([hmul(E[:,k], b) for k in range(4)])
iM = np.array([0,1,0,0.]); jM = np.array([0,0,1,0.]); kM = np.array([0,0,0,1.])
L = [np.eye(4), leftmul(iM), leftmul(jM), leftmul(kM)]
R = [np.eye(4), rightmul(iM), rightmul(jM), rightmul(kM)]
# 验证 L 均对应四元数（左表示=同态: L_i L_j L_k = −I; 右表示=反同态: R_i R_j R_k = +I）
Lq = np.allclose(L[1]@L[2]@L[3], -np.eye(4)) and np.allclose(L[1]@L[2], L[3]) and np.allclose(L[1]@L[1], -np.eye(4))
# 右表示 R(b): v→v·b, 满足 R_a R_b = R_{ba}（反同态）⟹ R_i R_j = R(ji)=−R_k, R_i R_j R_k = +I
Rq = np.allclose(R[1]@R[2], -R[3]) and np.allclose(R[1]@R[2]@R[3], np.eye(4)) and np.allclose(R[1]@R[1], -np.eye(4))
comm_ok = all(commute(L[a], R[b]) for a in range(4) for b in range(4))  # 结合律⇒左右作用可交换
# 16 个乘积 L(a)·R(b) 是否实线性独立（张成整个 16 维 M₄(ℝ)）—— 决定性判据
prods = [L[a]@R[b] for a in range(4) for b in range(4)]
flat = np.stack([p.reshape(16) for p in prods])   # 16×16 实矩阵
rk = np.linalg.matrix_rank(flat, tol=1e-9)
print(f"     L 同态四元数={Lq};  R 反同态四元数={Rq};  L(a) 与 R(b) 全可交换={comm_ok}")
print(f"     16 个 L(a)R(b) 实线性独立秩 = {rk}  (应 16 = dim_ℝ M₄(ℝ))")
print(f"     → {'✓ ℍ⊗_ℝℍ ≅ M₄(ℝ)：张量积=4×4 实矩阵代数, 实维 16' if Lq and Rq and comm_ok and rk==16 else '✗ 异常, 需复查'}")

# ---------------- [V3] Cl(1,7) 宿主级核对（框架已机器封闭） ----------------
print("\n[V3] Chain-B 宿主的 16：Cl(1,7) 对象级")
print("     事实(机器封闭, paper33/06_bott_tower_unification.md F5):")
print("       Cl(1,7) ≅ M₁₆(ℝ)     （16×16 实矩阵代数, 实维 2^8 = 256）")
print("       spinorDim = 2^⌊8/2⌋ = 16 = 2·k_max（k_max=8, 统一3定理）")
print("       最小忠实实模 = ℝ¹⁶")
print("     路径1 的 16 = dim_ℝℍ² 对应对象:")
print("       ℍ⊗_ℝℍ ≅ M₄(ℝ)       （4×4 实矩阵代数, 实维 16）")
print("       （M₄(ℝ) ≅ Cl(2,2), 签名(2,2), 4 生成元, 与宿主 Cl(1,7)=M₁₆(ℝ) 不同级）")

# ---------------- [V4] 对象级（矩阵尺寸）判别 ----------------
print("\n[V4] 对象级判别：M₄(ℝ)（张量面） vs M₁₆(ℝ)（旋量宿主）")
print("     矩阵尺寸:  M₄(ℝ) = 4×4   vs   M₁₆(ℝ) = 16×16")
print("     实维:      16           vs   256")
print("     生成元数:  Cl(2,2) n=4  vs   Cl(1,7) n=8")
print("     → 两者同为『实维 16』仅数值相等; 代数尺寸不同(4 vs 16) → 非同对象")
print("     → '16 = dim_ℝℍ²' 作为维数恒等成立, 作为代数同构不成立（宿主是 M₁₆ 不是 M₄）")

# ---------------- [V5] 旋量模的 ℍ-模结构 ----------------
print("\n[V5] 旋量模结构：ℝ¹⁶ 作 ℍ-模")
d = 16          # spinorDim(Cl(1,7)) 实维
dimH = 4        # dim_ℝℍ
mult = d // dimH
print(f"     spinor(Cl(1,7)) 实维 = 16;  dim_ℝℍ = 4;  多重度 = 16/4 = {mult}")
print(f"     → ℝ¹⁶ = ℍ^{mult}（ℍ-模直和）:  16 = dim_ℝℍ × 多重度 = 4 × 4")
print(f"     → 结构性诚实：第一因子 4 = dim_ℝℍ（真，Chain A 同源）;")
print(f"       第二因子 4 = 模多重度（= 16/dim_ℝℍ，并非独立的第二个 dim_ℝℍ）")

print("\n" + "=" * 78)
print("诚实判定（路径1）:")
print("  [V1] Cl(0,3)^0 ≅ ℍ, dim_ℝℍ = 4          — 机器一致(su2_fundamental_rep_dim_two)")
print("  [V2] ℍ⊗_ℝℍ ≅ M₄(ℝ), 实维 16            — 结构真同构, 但对象是 4×4 级")
print("  [V3] Chain-B 宿主 16 = spinorDim(C1,7)=M₁₆(ℝ)模, 实维16 — 框架机器封闭")
print("  [V4] 对象级: M₄(ℝ)(4×4) ≠ M₁₆(ℝ)(16×16)  → dim_ℝℍ² 是维数恒等, 非代数同构")
print("  [V5] 旋量模 = ℍ^4: 16 = 4(dim_ℝℍ) × 4(多重度); 多重度非独立内源")
print("  结论: 路径1 的『16 = dim_ℝℍ²』成立但仅为维数恒等/模结构;")
print("        宿主 16 的既有内源是 2·k_max(spinor), 与 dim_ℝℍ² 是两条不同级路径.")
print("  纪律(VII)遵守: 不把『数值相等』升级为『物理内源』; 16 采用 2·k_max 宿主,")
print("        dim_ℝℍ² 候选登记为『模分解巧合, 非同构内源』, 交台账开放. ")
print("=" * 78)