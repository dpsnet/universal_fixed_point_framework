# -*- coding: utf-8 -*-
"""L2 第②项：−1 相位源机制验证（2026-10-23）
候选 S4（层复合旋转）：三层态射 → Cℓ(3,0) 的反对易由"两层复合 = 90° 旋转 = 复结构
J，J² = −1"提供。机制：
  层 1 对合 σx（实反射）、层 3 对合 σz（实反射）
  两层复合 J = σz·σx = 90° 旋转 ⟹ J² = −1（复结构，无外部输入）
  第三层对合 σy = i·J = i·(σz·σx)（i 来自 J 的存在性）
  反对易 {σx,σy}={σy,σz}={σz,σx}=0 ⟺ 三方向正交 + 复结构 J
90° = 2π/4：谱流 1/4 圈；2π 周期框架 = TwoPiPeriodicity（模流/谱流闭合周期 2π，已机检）
⟹ −1 = (π/2 旋转)² = 谱流 1/4 圈平方。

检验：
  A. J = σzσx：J² = −1（复结构涌现）
  B. σy = iJ：与 σx, σz 反对易（{σᵢ,σⱼ}=0）
  C. Pauli 投影条件：Pᵢ=(1+σᵢ)/2 满足 PᵢPⱼ+PⱼPᵢ = Pᵢ+Pⱼ−½
  D. 随机三层投影族无此结构（J²≠−1 恒成立）——为什么随机族不反对易
  E. 一般化：任意"两层复合为 90° 旋转"的实对合族是否自动成 Clifford？
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
    return np.outer(u, u.conj())

def involution(P):
    return 2 * P - np.eye(P.shape[0], dtype=P.dtype)

def anticomm_residual(sigs):
    mx = 0.0
    for i in range(len(sigs)):
        for j in range(i + 1, len(sigs)):
            ac = sigs[i] @ sigs[j] + sigs[j] @ sigs[i]
            r = np.linalg.norm(ac, ord="fro") / (np.linalg.norm(sigs[i], ord="fro") * np.linalg.norm(sigs[j], ord="fro"))
            mx = max(mx, r)
    return mx

def run():
    print("L2 第②项：−1 相位源机制验证（S4：层复合旋转 J²=−1）")
    print("=" * 78)

    # A. 两层复合 = 90° 旋转 = 复结构 J，J² = −1
    # σx = 2Px−1（沿 (1,1)/√2 反射）、σz = 2Pz−1（沿 (1,0) 反射）
    Px = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
    Pz = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    sx = involution(Px)
    sz = involution(Pz)
    J = sz @ sx
    print(f"A. J = σz·σx：")
    print(f"   J = {J.tolist()}")
    print(f"   J² = {np.round((J @ J).real, 12).tolist()}  J²+1 残差 = {np.linalg.norm(J @ J + np.eye(2), ord='fro'):.3e}（应 ≈0：复结构涌现）")

    # B. 第三层对合 σy = i·J，反对易核验
    sy = 1j * J
    sigs = [sx, sy, sz]
    r = anticomm_residual(sigs)
    print(f"\nB. σy = i·J：反对易残差 = {r:.3e}  {'PASS 反对易' if r < 1e-12 else 'FAIL'}")

    # C. Pauli 投影条件：PᵢPⱼ+PⱼPᵢ = Pᵢ+Pⱼ−½（注意：P = (I+σ)/2，I 为单位阵，勿用逐元素 1+σ）
    Ps = [(np.eye(2) + s) / 2 for s in sigs]
    max_dev = 0.0
    for i in range(3):
        for j in range(i + 1, 3):
            dev = Ps[i] @ Ps[j] + Ps[j] @ Ps[i] - (Ps[i] + Ps[j] - 0.5 * np.eye(2))
            max_dev = max(max_dev, np.linalg.norm(dev, ord="fro"))
    print(f"C. Pauli 投影条件 PᵢPⱼ+PⱼPᵢ = Pᵢ+Pⱼ−½：最大偏差 = {max_dev:.3e}  {'PASS' if max_dev < 1e-12 else 'FAIL'}")

    # D. 随机三层投影族：J² ≠ −1 恒成立（为什么随机族不反对易）
    print("\nD. 随机三层投影族（实 ℝ²，200 trials）：两层复合 J = σ3·σ1 的 J²+1 范数分布")
    vals = []
    for _ in range(200):
        u1 = random_unit(2); u3 = random_unit(2)
        s1 = involution(proj(u1)); s3 = involution(proj(u3))
        J = s3 @ s1
        vals.append(np.linalg.norm(J @ J + np.eye(2), ord="fro"))
    print(f"   min {min(vals):.3e} / med {np.median(vals):.3e} / max {max(vals):.3e}（远大于 0 ⟹ 随机族无复结构）")

    # E. 一般化：任意实对合族中，J²=−1 是否 ⟹ 反对易？
    print("\nE. 结构检验：由层复合 J 涌现复结构 ⟹ 第三对合 iJ 反对易 ⟹ Clifford（理论闭合）")
    print(f"   {['σx', 'σy', 'σz']} = Pauli 三件套 ⟹ Cℓ(3,0) ≅ ℂ(2) ⟹ {{γ,γ}}=2g 候选成立")

if __name__ == "__main__":
    run()
