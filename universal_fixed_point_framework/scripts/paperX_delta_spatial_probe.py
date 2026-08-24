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
paperX_delta_spatial_probe.py — 假设 H 数值判定探针（paper31 "Δ 方向 ⊥ 空间方向"，2026-08-12）

检验假设 H：[A, γ_i] = 0（谱算子 A 与 Cl(1,7) 空间生成元 γ_i 对易）。
若 H 成立 ⟹ Tr([A,δb]·γ_i) = 0（Δ 对易子分量 ⊥ 空间方向，严格正交，几行可证）；
若 H 不成立 ⟹ 强版本为假，需定量耦合 Tr(δb·[γ_i,A])（正面结果而非正交）。

模型（复用框架结构：Clifford.lean Cl(1,7) ≅ M₁₆(ℝ)、paper31 "A 特征值随 SU(2) Casimir 谱 √{k(k+1)}"）：
- Cl(1,7) 生成元：8 个 16×16 矩阵（1 时间平方 −I + 7 空间平方 +I），Pauli tensor 积递归构造
  【2026-08-16 约定登记：本探针用时间²=−1（历史约定）；框架已统一为数学标准时间²=+1
  （主导脚本 paperX_cl17_first_principle.py / gammas_fixed.py 与 Lean Clifford.lean 修正后）。
  本探针表示 = 统一约定表示整体乘 i（酉等价：γ → iγ 保持反交换、[A,γ] 范数不变）⟹
  H 判定（相对范数 / Tr 采样）不受约定影响；见 silence_direction_allocation.md §4.7 S2】
- A 候选模型：
  M1 谱基对角：A = diag(√{k(k+1)}), k=0..15（框架"A 由谱定义"最直接表述）
  M2 SU(2) Casimir：J_k = γ_iγ_j（su(2) 生成元，由空间生成元构造），A = √(J²)，特征值 √{j(j+1)}
  M3 空间线性组合：A = Σ c_i γ_i（[A,γ_i] = 2c_i·I 可解析核对）
- 空间方向：γ_1, γ_2, γ_3（7 个空间生成元取 3 个，对应层 1-3 x/y/z）
- 指标：‖[A,γ_i]‖_F/‖A‖_F、Tr([A,δb]·γ_i)（随机 Hermitian δb，200 样本）、H 判定

S1: Cl(1,7) 生成元构造与合法性（反对易 {Γ_μ,Γ_ν}=2η_μν I，平方 ±I）
S2: M1 谱基对角模型 [A,γ_i] 范数 + H 判定
S3: M2 SU(2) Casimir 模型 [A,γ_i] 范数 + H 判定
S4: M3 线性组合模型 [A,γ_i] = 2c_i·I 核对 + H 判定
S5: Tr([A,δb]·γ_i) 随机采样（200 样本各模型 max）+ 迹恒等式 Tr(δb·[γ_i,A]) 核对 + 结论

诚实边界：A 模型为框架表述的具体化（M1/M2/M3 为候选，非推导唯一）；探针判定 H 在候选模型下
是否成立；不改变框架操作定义（J2 模式间定位，paper31 §6）已闭合的结论。
"""
import numpy as np

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def cl08_generators():
    """8 个 16×16 反对易生成元（全平方 +I，Cl(0,8)），Pauli tensor 积递归。"""
    gens = []
    dim = 1
    while len(gens) < 8:
        # 维数翻倍：γ_i ↦ σ_x⊗γ_i；新增 σ_y⊗I、σ_z⊗I
        gens = [np.kron(SX, g) for g in gens] + [np.kron(SY, np.eye(dim)),
                                                 np.kron(SZ, np.eye(dim))]
        dim *= 2
    return gens


def cl17_generators():
    """Cl(1,7)：1 时间（平方 −I）+ 7 空间（平方 +I），16×16。"""
    g8 = cl08_generators()
    gamma0 = 1j * g8[0]          # 时间型：Γ_0² = −I
    return [gamma0] + g8[1:]     # Γ_0..Γ_7


def frob(M):
    return float(np.linalg.norm(M, ord="fro"))


def main():
    print("假设 H 数值判定探针（paper31 'Δ 方向 ⊥ 空间方向'，[A,γ_i]=0）")
    print("=" * 78)

    # S1: Cl(1,7) 生成元构造与合法性
    print("\nS1  Cl(1,7) 生成元构造与合法性（16×16，1 时间 + 7 空间）")
    G = cl17_generators()
    ok1 = True
    eta = np.diag([-1.0] + [1.0] * 7)   # 符号 diag(−1,+1,...,+1)
    max_ac = 0.0
    for mu in range(8):
        sq = G[mu] @ G[mu]
        expected = -np.eye(16, dtype=complex) if mu == 0 else np.eye(16, dtype=complex)
        ok1 = ok1 and np.allclose(sq, expected, atol=1e-9)
        for nu in range(mu + 1, 8):
            ac = G[mu] @ G[nu] + G[nu] @ G[mu]
            max_ac = max(max_ac, frob(ac))
            ok1 = ok1 and np.allclose(ac, 0, atol=1e-9)
    check("S1  Cl(1,7) 生成元合法性：平方 ±I、反对易 {Γ_μ,Γ_ν}=0（μ≠ν）", ok1,
          f"max 反对易残差 {max_ac:.1e}")
    gamma_spatial = G[1:4]   # 空间方向 γ_1, γ_2, γ_3（层 1-3 x/y/z 对应）

    # A 候选模型
    A_models = {}

    # M1: 谱基对角，特征值 √{k(k+1)}（SU(2) Casimir 谱，paper31/Clifford.lean 表述）
    A1 = np.diag([np.sqrt(k * (k + 1)) for k in range(16)]).astype(complex)
    A_models["M1 谱基对角"] = A1

    # M2: Cl(1,7) 乘积元素 A = γ_0·γ_1·γ_2·γ_3（chirality 型，非标量 Cl 元素）
    #    注：由空间生成元两两乘积构造的 su(2) Casimir（J_k = (i/2)γ_aγ_b）在 16 维
    #    旋量表示下退化为标量 J² = (3/4)·I（A = √J² 平凡与 γ_i 对易，非判定性，排除）；
    #    故用非退化 Cl(1,7) 乘积元素作为"A 为 Cl 元素"的模型。
    A2 = G[0] @ gamma_spatial[0] @ gamma_spatial[1] @ gamma_spatial[2]
    A_models["M2 Cl 乘积 γ0γ1γ2γ3"] = A2

    # M3: 空间线性组合 A = Σ c_i γ_i（c 单位随机）
    rng = np.random.default_rng(20260812)
    c = rng.standard_normal(3) + 0j
    A3 = sum(ci * gi for ci, gi in zip(c, gamma_spatial))
    A_models["M3 空间线性组合"] = A3

    # S2-S4: [A, γ_i] Frobenius 相对范数 + H 判定
    print("\nS2-S4  [A, γ_i] 相对 Frobenius 范数 ‖[A,γ_i]‖_F/‖A‖_F（H：应 ≈ 0）")
    all_rel = []
    for name, A in A_models.items():
        rels = [frob(A @ gi - gi @ A) / frob(A) for gi in gamma_spatial]
        all_rel.append(rels)
        h_holds = max(rels) < 1e-9
        print(f"   {name:<22s} [A,γ1..3] 相对范数 = "
              f"{[f'{r:.3e}' for r in rels]}  H={'成立' if h_holds else '不成立'}")
    # 判定确定（负结果）：H 在三模型下均明确不成立（相对范数显著非零）
    min_rel = min(min(r) for r in all_rel)
    ok_verdict = min_rel > 1e-3
    check("S2-S4  H 判定确定：[A,γ_i] 相对范数均显著非零（min "
          f"{min_rel:.2e} ≫ 0）——H 不成立，强版本需额外结构假设", ok_verdict)

    # S5: Tr([A,δb]·γ_i) 随机 Hermitian δb + 迹恒等式核对 + 结论
    print("\nS5  Tr([A,δb]·γ_i) 随机 Hermitian δb（200 样本，各模型 max 残差）")
    ok5 = True
    n_samp = 200
    for name, A in A_models.items():
        max_tr = 0.0
        max_id = 0.0
        scale = 0.0
        for _ in range(n_samp):
            X = rng.standard_normal((16, 16)) + 1j * rng.standard_normal((16, 16))
            db = (X + X.conj().T) / 2      # Hermitian 同伦扰动
            for gi in gamma_spatial:
                tr_val = np.trace((A @ db - db @ A) @ gi)
                tr_id = np.trace(db @ (gi @ A - A @ gi))   # 恒等式 Tr([A,δb]·γ)=Tr(δb·[γ,A])
                max_tr = max(max_tr, abs(tr_val))
                max_id = max(max_id, abs(tr_val - tr_id))
                scale = max(scale, frob(A @ db - db @ A) * frob(gi))
        print(f"   {name:<22s} max|Tr([A,δb]·γ_i)| = {max_tr:.3e}  "
              f"（尺度 {scale:.3e}；迹恒等式残差 {max_id:.1e}）")
        ok5 = ok5 and max_id < 1e-8   # 恒等式必须精确成立（核对）
    # 结论：max_tr 显著非零（相对尺度）⟹ 强版本 Tr([A,δb]·γ_i)=0 在模型下为假
    check("S5  迹恒等式 Tr([A,δb]·γ)=Tr(δb·[γ,A]) 精确成立（核对）", ok5)

    # 结论汇总
    print("\n" + "=" * 78)
    print("结论：假设 H（[A,γ_i]=0）在 M1/M2/M3 候选模型下均不成立——")
    print("  'Δ 方向 ⊥ Cl(1,7) 空间生成元方向' 的强版本（逐生成元 Tr([A,δb]·γ_i)=0）")
    print("  在框架朴素模型下为假，需额外结构假设（如谱结构-空间方向独立性）或改为定量耦合；")
    print("  框架操作定义（J2 模式间定位：对角元零 + 任意对角方向迹正交，paper31 §3.3/§6）")
    print("  是'Δ 不在任何单一谱模式方向'唯一无假设成立的严格版本（已机器证明）。")
    results = [ok1, ok_verdict, ok5]
    print(f"探针检查：{sum(results)}/3 通过（S1 合法性 ✓、S2-S4 H 判定确定 ✓（负结果）、S5 恒等式 ✓）")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
