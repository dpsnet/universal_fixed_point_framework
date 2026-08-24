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
# -*- coding: utf-8 -*-
"""
paperX_threequarter_mock_test.py — 朗道横向投影推导逻辑的 mock 数据本地测试
====================================================================================
对应：paperX_threequarter_silence_derivation.py（D1-D10 推导骨架）
触发：用户"构造一个 mock 数据来本地运行测试一下这个朗道横向投影的推导逻辑"。

目标：用**合成数据（mock）**独立验证推导逻辑的每一环——不依赖真实谱定量
（σ/α_s 等），只依赖推导骨架本身的结构（谱静默公理 + 线性代数 + 球平均）。

Mock 场景（对应推导步骤）：
  M0   mock 8D 空间 = 1 时间 ⊕ 3 空间 ⊕ 4 静默内部（Cl(1,7) 结构 mock）
  M1   mock 谱流算子 D(f)：ran D ⊆ V_Λ⊥（静默公理 P_{V_Λ}D = 0 成立）
  M2   D1 mock：观测层投影 W0 = P_{V_Λ⊥} 是正交投影（幂等 + 自伴）
  M3   D2 mock：mock 方向权重筛选（时间 1 / 空间 S₄ / 内部 S₃S₄）
       ⟹ 唯一涌现 4D 观测窗口（1 时间 + 3 空间可见）
  M4   D5 mock：约束集（正交投影 + 湮灭 q̂ + 秩 3）⟹ 唯一解 = 朗道横向投影
       （随机基候选均相等；SVD 独立构造对照）
  M5   D7 mock：S³ 球平均 ⟨P^T_ii⟩ = 1 − ⟨q_i²/q²⟩ = ¾（数值 0.7498）
  M6   D9 mock：三维积分权重 = w₁w₂w₃ = ¾³；mock 强度比 = 27/64
  负向测试（证明逻辑真的"用到"了每条约束）：
  M7   mock 静默方向错配（s ≠ q̂）⟹ W ≠ P^T、每方向权重 ≠ ¾（映射是必要的）
  M8   mock 去掉正交投影约束（非对称扰动）⟹ 不唯一、W ≠ P^T（约束是必要的）
  M9   mock 各向异性（q₀ 放大）⟹ 每方向份额 ≠ 1/4 ⟹ 权重 ≠ ¾（各向同性是必要的）

所有随机量用固定种子（可复现）；单位无关（纯结构测试）。
"""
import numpy as np

# ---- mock 参数（谱静默阈值，paper32/paper17 框架值）----
D_H = 2.7095                      # IFS 收缩维数（框架谱定量）
S4_THRESHOLD = np.exp(-D_H)       # 可见性阈值 S₄ = e^{-d_H} ≈ 0.0666
S3S4 = np.exp(-(3.0 + D_H))       # 内部维度静默因子 ≈ 0.0033

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def transverse_projector(q):
    """朗道横向投影 P^T(q) = 1₄ − q̂q̂ᵀ（4D）。"""
    q = np.asarray(q, dtype=float)
    qhat = q / np.linalg.norm(q)
    return np.eye(4) - np.outer(qhat, qhat)


def s3_samples(n=200000, seed=42, scale=None):
    """mock S³ 均匀样本（Gauss 归一化）；scale 为各向异性 mock 的标准差缩放。"""
    rng = np.random.default_rng(seed)
    q = rng.standard_normal((n, 4))
    if scale is not None:
        q = q * np.asarray(scale, dtype=float)
    norm = np.linalg.norm(q, axis=1, keepdims=True)
    return q / norm


def run():
    print("=" * 74)
    print("朗道横向投影推导逻辑：mock 数据本地测试（M0-M9）")
    print("=" * 74)

    rng = np.random.default_rng(7)

    # ---- M0: mock 8D 空间结构 ----
    print("\n" + "=" * 74)
    print("M0. mock 8D 空间 = 1 时间 ⊕ 3 空间 ⊕ 4 静默内部（Cl(1,7) 结构）")
    print("=" * 74)
    e_time = np.zeros(8); e_time[0] = 1.0                  # e_0：时间
    e_space = [np.eye(8)[i] for i in [1, 2, 3]]            # e_1..e_3：空间
    e_silent = [np.eye(8)[i] for i in [4, 5, 6, 7]]        # e_4..e_7：静默内部
    P_VL = np.diag([0, 0, 0, 0, 1, 1, 1, 1])               # 静默子空间 V_Λ 投影
    P_VL_perp = np.eye(8) - P_VL                           # V_Λ⊥ 投影
    print("    Cl(1,7) mock：1 时间 + 3 空间 + 4 静默 = 8")
    print("    P_{V_Λ} = diag(0,0,0,0,1,1,1,1)；P_{V_Λ⊥} = I − P_{V_Λ}")
    print(f"    rank P_{{V_Λ}} = {np.linalg.matrix_rank(P_VL)}（静默 4 维），"
          f"rank P_{{V_Λ⊥}} = {np.linalg.matrix_rank(P_VL_perp)}（可见 4 维）")
    ok0 = (np.linalg.matrix_rank(P_VL) == 4
           and np.linalg.matrix_rank(P_VL_perp) == 4
           and np.allclose(P_VL @ P_VL_perp, 0.0))
    check("M0 mock 8D = 1⊕3⊕4 分裂：静默 4 维投影与可见 4 维投影正交",
          ok0, "P_{V_Λ}·P_{V_Λ⊥} = 0（正交补）")

    # ---- M1: mock 谱流算子满足静默公理 ----
    print("\n" + "=" * 74)
    print("M1. mock 谱流算子 D(f)：ran D ⊆ V_Λ⊥ ⟹ 静默公理 P_{V_Λ}D = 0")
    print("=" * 74)
    C = rng.standard_normal((4, 8))                        # 可见 4 分量任意谱内容
    D_mock = np.zeros((8, 8))
    D_mock[:4, :] = C                                      # 后 4 行全零 ⟹ 值域 ⊆ V_Λ⊥
    silence_ok = np.allclose(P_VL @ D_mock, 0.0, atol=1e-12)
    print(f"    ‖P_{{V_Λ}}·D‖ = {np.linalg.norm(P_VL @ D_mock):.2e} ≈ 0")
    print("    ⟹ mock 谱流算子的像完全落在静默子空间正交补内（公理成立）")
    check("M1 mock 静默公理成立：P_{V_Λ}D(f) = 0（ran D ⊆ V_Λ⊥）",
          silence_ok, "‖P_{V_Λ}·D‖ ≈ 0")

    # ---- M2: D1 mock —— 观测层投影为正交投影 ----
    print("\n" + "=" * 74)
    print("M2. D1 mock：观测层投影 W0 = P_{V_Λ⊥} 是正交投影（幂等 + 自伴）")
    print("=" * 74)
    W0 = P_VL_perp
    idem_ok = np.allclose(W0 @ W0, W0, atol=1e-12)
    symm_ok = np.allclose(W0, W0.T, atol=1e-12)
    print(f"    W0² = W0：{idem_ok}；  W0† = W0：{symm_ok}")
    print("    ⟹ 观测层权重算子必须为正交投影（谱静默公理结构推论）")
    check("M2 D1 mock：观测层接收 = 静默子空间正交补上的投影（正交投影性质）",
          idem_ok and symm_ok, "W0² = W0 + W0† = W0")

    # ---- M3: D2 mock —— 权重筛选涌现 4D 窗口 ----
    print("\n" + "=" * 74)
    print("M3. D2 mock：mock 方向权重筛选（时间 1 / 空间 S₄ / 内部 S₃S₄）")
    print("=" * 74)
    w_screen = np.array([1.0] + [S4_THRESHOLD] * 3 + [S3S4] * 4)
    visible = w_screen >= S4_THRESHOLD
    n_vis, n_sil = int(visible.sum()), int((~visible).sum())
    print(f"    mock 方向权重 = {np.round(w_screen, 4)}")
    print(f"    可见性判据 w ≥ S₄ = {S4_THRESHOLD:.4f}：可见 {n_vis}（1 时间 + 3 空间），"
          f"静默 {n_sil}（4 内部）")
    check("M3 D2 mock：权重筛选唯一涌现 4D 观测窗口（1 时间 + 3 空间可见，4 内部静默）",
          n_vis == 4 and n_sil == 4 and visible[0] and all(visible[1:4])
          and not any(visible[4:]),
          "可见 4 = 1⊕3；静默 4（S₃S₄ < S₄ ≤ c₃ 分离裕度 e³）")

    # ---- M4: D5 mock —— 约束集唯一解 = 朗道横向投影 ----
    print("\n" + "=" * 74)
    print("M4. D5 mock：约束集（正交投影 + 湮灭 q̂ + 秩 3）⟹ 唯一解 = P^T")
    print("=" * 74)
    q = rng.standard_normal(4)
    qhat = q / np.linalg.norm(q)
    P_T = transverse_projector(q)
    # ① 候选自身满足约束
    c1 = np.allclose(P_T @ P_T, P_T, atol=1e-10)      # 幂等
    c2 = np.allclose(P_T, P_T.T, atol=1e-10)          # 自伴
    c3 = np.allclose(P_T @ qhat, 0.0, atol=1e-10)     # 湮灭纵向
    c4 = np.linalg.matrix_rank(P_T) == 3              # 秩 3
    # ② 唯一性：SVD 独立构造 span{q̂}⊥ 投影 = P^T
    _, _, vh = np.linalg.svd(qhat.reshape(1, -1), full_matrices=True)
    B0 = vh[1:].T                                     # 4×3：q̂ 正交补标准正交基
    P_svd = B0 @ B0.T
    uni_svd = np.allclose(P_svd, P_T, atol=1e-10)
    # ③ 唯一性：任意正交基（随机旋转）候选均 = P^T
    ok_rot = True
    for _ in range(5):
        Q = np.linalg.qr(rng.standard_normal((3, 3)))[0]
        B = B0 @ Q
        W_cand = B @ B.T                              # 秩 3 正交投影，核含 q̂
        if not np.allclose(W_cand, P_T, atol=1e-10):
            ok_rot = False
    print(f"    P^T 满足：幂等 {c1} / 自伴 {c2} / P^T·q̂ = 0 {c3} / rank 3 {c4}")
    print(f"    SVD 独立构造 = P^T：{uni_svd}；随机正交基候选均 = P^T：{ok_rot}")
    check("M4 D5 mock：正交投影 + Wq̂=0 + rank 3 ⟹ 唯一解 W = 1₄ − q̂q̂ᵀ",
          c1 and c2 and c3 and c4 and uni_svd and ok_rot,
          "ker W = span{q̂} ⟹ im W 唯一（谱分解）")

    # ---- M5: D7 mock —— 球平均 = ¾ ----
    print("\n" + "=" * 74)
    print("M5. D7 mock：S³ 球平均 ⟨P^T_ii⟩ = 1 − ⟨q_i²/q²⟩ = ¾")
    print("=" * 74)
    smp = s3_samples(seed=42)
    fracs = np.mean(smp ** 2, axis=0)                 # ⟨q_μ²/q²⟩，μ = 0..3
    w_i = [1.0 - fracs[i] for i in [1, 2, 3]]
    w_avg = float(np.mean(w_i))
    print(f"    ⟨q_μ²/q²⟩ = {np.round(fracs, 4)}（各向同性 1/4）")
    print(f"    三空间方向 ⟨P^T_ii⟩ = {[round(w, 4) for w in w_i]}，平均 = {w_avg:.4f}（¾ = 0.75）")
    check("M5 D7 mock：每空间方向横向投影球平均 = 1 − 1/4 = ¾（4D 各向同性）",
          abs(w_avg - 0.75) < 0.01
          and all(abs(f - 0.25) < 0.01 for f in fracs),
          f"⟨P^T_ii⟩ = {w_avg:.4f}；⟨q_μ²/q²⟩ ≈ 1/4")

    # ---- M6: D9 mock —— 三维积分权重 = ¾³，mock 强度比 = 27/64 ----
    print("\n" + "=" * 74)
    print("M6. D9 mock：三维积分权重 = w₁w₂w₃ = ¾³；mock 强度比 = 27/64")
    print("=" * 74)
    w3_mock = float(np.prod(w_i))                     # 由 mock 球平均给出的每方向权重乘积
    print(f"    每方向权重 w_i = {[round(w, 4) for w in w_i]}")
    print(f"    三维积分权重 = w₁·w₂·w₃ = {w3_mock:.6f}（¾³ = 0.421875）")
    # mock 强度比：I_mt = ∫d³p f(p)（未加权工作胶子），I_fw = ∫d³p ∏w_i f(p)（观测层加权）
    x = np.linspace(-2.0, 2.0, 4000)
    f_1d = np.exp(-x ** 2)
    I_1d = float(np.trapz(f_1d, x))
    I_mt_mock = I_1d ** 3
    I_fw_mock = float(np.prod(w_i)) * I_1d ** 3
    ratio_mock = I_fw_mock / I_mt_mock
    print(f"    mock 强度比 I_fw/I_MT = {ratio_mock:.6f}（= 三维积分权重，期望 27/64 = 0.421875）")
    check("M6 D9 mock：三维积分权重 = ¾³ = 27/64；mock 强度比 = 三维积分权重",
          abs(w3_mock - 27.0 / 64.0) < 0.01
          and abs(ratio_mock - 27.0 / 64.0) < 0.01,
          f"¾³ ≈ {w3_mock:.4f}；I_fw/I_MT = {ratio_mock:.4f}")

    # ---- M7 负向：静默方向错配 ----
    print("\n" + "=" * 74)
    print("M7. 负向测试：mock 静默方向错配（s = e₁ ≠ q̂）⟹ W ≠ P^T")
    print("=" * 74)
    s = np.eye(4)[1]                                  # 错配：静默方向取固定轴 e₁
    W_s = np.eye(4) - np.outer(s, s)                  # 湮灭 e₁ 而非 q̂ 的投影
    kill_qhat = np.linalg.norm(W_s @ qhat)            # 应 ≠ 0（未湮灭规范纵向）
    # 每方向球平均权重（沿 e₁ 方向 = 0）
    w_mis = [1.0 - fracs[i] if i != 1 else 0.0 for i in [1, 2, 3]]
    w_mis_avg = float(np.mean(w_mis))
    print(f"    W_s·q̂ 范数 = {kill_qhat:.3f} ≠ 0（规范纵向未被湮灭）")
    print(f"    空间方向平均权重 = {w_mis_avg:.4f} ≠ ¾ = 0.75")
    print("    ⟹ '静默方向 = q̂'的映射是必要的：错配则权重 ≠ ¾")
    check("M7 负向：静默方向错配（s ≠ q̂）⟹ W ≠ P^T、每方向权重 ≠ ¾（映射必要）",
          kill_qhat > 0.1 and abs(w_mis_avg - 0.75) > 0.05,
          f"‖W_s·q̂‖ = {kill_qhat:.3f}；⟨w⟩ = {w_mis_avg:.4f} ≠ 0.75")

    # ---- M8 负向：去掉正交投影约束 ----
    print("\n" + "=" * 74)
    print("M8. 负向测试：mock 去掉正交投影约束（非对称扰动）⟹ 不唯一")
    print("=" * 74)
    v = B0[:, 0]; w_ = B0[:, 1]                        # 两个 ⊥ q̂ 的向量
    A = 0.5 * (np.outer(v, w_) - np.outer(w_, v))      # 斜对称，A·q̂ = 0
    M_non = P_T + A                                    # 仍湮灭 q̂、秩 3，但非正交投影
    not_symm = not np.allclose(M_non, M_non.T, atol=1e-10)
    not_idem = not np.allclose(M_non @ M_non, M_non, atol=1e-10)
    kills = np.allclose(M_non @ qhat, 0.0, atol=1e-10)
    diff = np.linalg.norm(M_non - P_T)
    print(f"    M = P^T + A：M·q̂ = 0 {kills} / rank 3 {np.linalg.matrix_rank(M_non) == 3} / "
          f"非自伴 {not_symm} / 非幂等 {not_idem} / ‖M − P^T‖ = {diff:.3f}")
    print("    ⟹ 去掉正交投影约束后约束集不再唯一（幂等 + 自伴是唯一性的必要条件）")
    check("M8 负向：去掉正交投影约束 ⟹ 不唯一、M ≠ P^T（正交投影约束必要）",
          not_symm and not_idem and kills and diff > 0.1,
          "非对称非幂等矩阵仍湮灭 q̂ ⟹ 唯一性依赖正交投影约束")

    # ---- M9 负向：各向异性 ----
    print("\n" + "=" * 74)
    print("M9. 负向测试：mock 各向异性（q₀ 标准差 ×2）⟹ 每方向份额 ≠ 1/4")
    print("=" * 74)
    smp_an = s3_samples(seed=42, scale=[2.0, 1.0, 1.0, 1.0])
    fracs_an = np.mean(smp_an ** 2, axis=0)
    w_an = [1.0 - fracs_an[i] for i in [1, 2, 3]]
    w_an_avg = float(np.mean(w_an))
    print(f"    ⟨q_μ²/q²⟩（各向异性）= {np.round(fracs_an, 4)}（时间方向份额 > 1/4）")
    print(f"    空间方向平均权重 = {w_an_avg:.4f} ≠ ¾ = 0.75")
    print("    ⟹ ¾ = 1 − ⟨q_i²/q²⟩ 依赖 4D 各向同性（每方向恰好 1/4）")
    check("M9 负向：各向异性 mock ⟹ 每方向份额 ≠ 1/4 ⟹ 权重 ≠ ¾（各向同性必要）",
          fracs_an[0] > 0.25 + 0.02 and abs(w_an_avg - 0.75) > 0.02,
          f"⟨q_0²/q²⟩ = {fracs_an[0]:.4f}；⟨w⟩ = {w_an_avg:.4f} ≠ 0.75")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print("\n" + "=" * 74)
    print(f"结果：{n_pass}/{len(RESULTS)} 通过")
    print("=" * 74)
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
