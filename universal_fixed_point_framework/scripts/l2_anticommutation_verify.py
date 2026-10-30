# -*- coding: utf-8 -*-
"""L2 先证伪：反对易构造的可达性（2026-10-23）
候选 v2 第②步：三层投影 P₁,P₂,P₃ → 对合 σᵢ=2Pᵢ−1，反对易 σᵢσⱼ=−σⱼσᵢ ⟹ Cℓ(3,0)。
核心问题：反对易在哪些投影构造下可达？随机三层投影族是否是 Cℓ(3,0) 生成元？

数学预备（核对用）：
- σᵢ=2Pᵢ−1（Pᵢ 正交投影）⟹ 反对易 {σᵢ,σⱼ}=0 ⟺ PᵢPⱼ+PⱼPᵢ = Pᵢ+Pⱼ − 1/2·1
  （Pauli 条件：Pᵢ = (1+σᵢ)/2 时成立）
- Cℓ(3,0) 生成元 = Pauli 矩阵 σx,σy,σz，各 = 2P−1（秩 1 复投影）
- 实秩 1 投影对合 = 超平面反射；反射 r_u r_v = r_v r_u ⟺ 交换；r_u r_v = −r_v r_u 恒不可达
  （实反射不反对易）——反对易需要复结构（−1 相位=i²）
- 反对易是 U 共轭不变：随机族若 {σ,σ}=0 则是 Clifford 的共轭，否则线性组合/复化也救不了
  （除非张量积扩展空间）

检验：
  A. Pauli 基准（ℂ²）：反对易残差 ~0（模型自校验，证明 2P−1 语言可产生 Cℓ(3,0)）
  B. 随机投影族（实 ℝ^n / 复 ℂ^n，秩 1）：反对易残差分布（预期全部非零=反例）
  C. 实反射：两两反对易不可达（数值 + 理论核验）
  D. 张量积提升（Pauli 嵌入更大空间）：反对易保持（PASS，指明 −1 相位的层结构来源）
pyenv 3.11.8 运行。
"""
import numpy as np

rng = np.random.default_rng(20261023)

def random_unit(n, complex_=False):
    if complex_:
        z = rng.normal(0, 1, n) + 1j * rng.normal(0, 1, n)
        return z / np.linalg.norm(z)
    v = rng.normal(0, 1, n)
    return v / np.linalg.norm(v)

def proj(u):
    """秩 1 正交投影"""
    return np.outer(u, u.conj())

def involution(P):
    """σ = 2P − 1"""
    return 2 * P - np.eye(P.shape[0], dtype=P.dtype)

def anticomm_residual(sigs):
    """max_{i≠j} ‖{σᵢ,σⱼ}‖_F / (‖σᵢ‖_F ‖σⱼ‖_F)"""
    mx = 0.0
    for i in range(len(sigs)):
        for j in range(i + 1, len(sigs)):
            ac = sigs[i] @ sigs[j] + sigs[j] @ sigs[i]
            r = np.linalg.norm(ac, ord="fro") / (np.linalg.norm(sigs[i], ord="fro") * np.linalg.norm(sigs[j], ord="fro"))
            mx = max(mx, r)
    return mx

def pauli_family():
    """Pauli 投影族（ℂ²，秩 1）：P = (1+σ)/2 的反解，直接给投影"""
    # σx = 2Px−1: Px = [[.5,.5],[.5,.5]]；σy: Py = [[.5,−.5i],[.5i,.5]]；σz = 2Pz−1: Pz = [[1,0],[0,0]]
    Px = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
    Py = np.array([[0.5, -0.5j], [0.5j, 0.5]], dtype=complex)
    Pz = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    return [involution(Px), involution(Py), involution(Pz)]

def run():
    print("L2 反对易先证伪：{σᵢ,σⱼ}=0 的可达性（σᵢ=2Pᵢ−1）")
    print("=" * 78)

    # A. Pauli 基准（模型自校验）
    sigs = pauli_family()
    r = anticomm_residual(sigs)
    print(f"A. Pauli 基准（ℂ²，3 投影）：反对易残差 = {r:.3e}  {'PASS' if r < 1e-12 else 'FAIL(模型错误!)'}")

    # B. 随机投影族：残差分布
    print("\nB. 随机投影族（秩 1，200 trials）：反对易残差分布")
    for dim, cx in ((2, False), (3, False), (4, False), (8, False), (2, True), (4, True), (8, True)):
        rs = []
        for _ in range(200):
            sigs = [involution(proj(random_unit(dim, cx))) for _ in range(3)]
            rs.append(anticomm_residual(sigs))
        print(f"  {'ℂ' if cx else 'ℝ'}^{dim}: min {min(rs):.3e} / med {np.median(rs):.3e} / max {max(rs):.3e}")

    # C. 实反射：两两反对易不可达（理论核验：{r_u,r_v} = 2⟨u,v⟩(2uu†+2vv†... ) 非零一般）
    print("\nC. 实秩 1 投影对合（反射）：反对易残差（正交方向特例）")
    # 正交方向 u₁⊥u₂：r_{u1} r_{u2} = −r_{u2} r_{u1}? 验证
    u1 = np.array([1.0, 0, 0]); u2 = np.array([0, 1.0, 0]); u3 = np.array([0, 0, 1.0])
    sigs = [involution(proj(u1)), involution(proj(u2)), involution(proj(u3))]
    r_orth = anticomm_residual(sigs)
    print(f"  标准正交基方向（u₁,u₂,u₃ 正交）：残差 = {r_orth:.3e}（{r_orth < 1e-12 and '反对易' or '非反对易'}）")
    # 理论：σᵢσⱼ+σⱼσᵢ = 4(PᵢPⱼ+PⱼPᵢ) − 4(Pᵢ+Pⱼ) + 2；u⊥v 时 PᵢPⱼ=0 → 残差 = ‖−4(Pᵢ+Pⱼ)+2‖ ≠ 0
    print(f"  理论核验：u⊥v 时 {{σᵢ,σⱼ}} = −4(Pᵢ+Pⱼ)+2·1 ≠ 0（秩 1 反射绝不反对易，除非退化）")

    # D. 张量积提升：Pauli 嵌入 4 维/8 维，反对易保持
    print("\nD. 张量积提升（Pauli 族 ⊗ 单位阵/新因子）：反对易保持")
    Px = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
    Py = np.array([[0.5, -0.5j], [0.5j, 0.5]], dtype=complex)
    Pz = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    # 8 维：σᵢ ⊗ 1（同一因子内 Pauli 反对易 → 张量保持）
    sigs8 = [involution(np.kron(Px, I2)), involution(np.kron(Py, I2)), involution(np.kron(Pz, I2))]
    r8 = anticomm_residual(sigs8)
    print(f"  σᵢ⊗1₂（ℂ⁸）：残差 = {r8:.3e}  {'PASS 反对易保持' if r8 < 1e-12 else 'FAIL'}")
    # 混合：γ₁=σx⊗1, γ₂=σy⊗1 反对易 ✓；γ₁=σz⊗σz?（{σz⊗σz, σy⊗1} = {σz,σy}⊗σz + ... = 0 ✓?）
    sigsM = [involution(np.kron(Px, I2)), involution(np.kron(Py, I2)), involution(np.kron(Pz, Pz))]
    rM = anticomm_residual(sigsM)
    print(f"  混合（σz⊗σz 在第三位）：残差 = {rM:.3e}  {'PASS' if rM < 1e-12 else 'FAIL'}")

    # E. −1 相位机制缺口核验：复相位 u→e^{iθ}u 不改变投影（uu† 不变）→ 复化不能产生新反对易
    print("\nE. 机制缺口核验：复相位不改变秩 1 投影（uu† 不变），故 −1 相位不能来自单层复化")
    u = random_unit(4, True)
    P0 = proj(u)
    Ph = proj(u * np.exp(1j * rng.uniform(0, 2 * np.pi)))
    print(f"  ‖P(e^{{iθ}}u) − P(u)‖_F = {np.linalg.norm(P0 - Ph, ord='fro'):.3e}（应为 0：投影相位不变）")

if __name__ == "__main__":
    run()
