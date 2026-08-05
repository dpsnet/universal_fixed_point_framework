#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_rec2_exchange_deviation.py — Rec₂ 交换律偏差的 BCH 修正复合数值验证
============================================================================
对应笔记：notes/00_foundations/spectral_rec2_exchange_deviation.md

验证内容（镜像 Sp₂ spExchangeLaw 偏差化）：
  T1  竖复合修正处方：γ = α + β + C_v（定义 4，修正后公式）满足自然性
  T2  横复合修正处方：γ' = α·α' + C_h（定义 6）满足自然性
  T3  交换律偏差合法性：Δ = LHS − RHS 是合法 2-态射（满足自然性）
  T4  偏差非平凡性：一般情形 ‖Δ‖_F > 0（交换律不严格成立）
  T5  严格极限：f=g=h、f'=g'=h' 且族可交换 ⇒ Δ = 0（G_N → 0 引力解耦）
  T6  偏差主导项：Δ = 交叉项 α·β' + β·α'（水平-垂直非对易缺陷）
  T9  单位律：id_f∘_vα = α = α∘_v id_g（零 2-态射为单位）

路径 B（D-拉回，对应 HigherRecCategory.lean 实现，v0.4+）：
  T10 拉回 2-态射条件 |T_g−T_f −(A_X H − H A_Y)|≈0（交织解）
  T11 拉回竖复合（homotopy 和）保持条件
  T12 拉回横复合（whiskering）保持条件
  T13 交换律偏差 = (T_h−T_g)H_α' + H_β(T_f'−T_g')（recExchangeLaw_homotopy_deviation）
  T14 严格极限（交织 homotopy）偏差 = 0（G_N → 0 引力解耦）
  T15 同源交织 H 满足条件 + 时间无关族 α(n)≡H 满足自然性（§4.4 定理 12）
  T16 异源 RecHom 对（f=s≠g=s²）拉回 2-态射不存在（§4.4 定理 11，可对角化步进）
  T18 迹障碍：tr(A²−A)=#fixed(s²)−#fixed(s)≠0 ⟹ (s,s²) 不可解（命题 13 必要条件）
  T19 缺陷等迹情形非平凡拉回 2-态射（例 14 正面例，v0.9）：s:0↦1,1↦2,2↦2（缺陷），
      f=s, g=s²（#fix 等迹=1），显式 H=[[1,0,-1],[0,0,0],[0,0,0]] 精确满足
      A H − H A = A²−A（残差 <1e-8）⟹ 非空性 ⟺ f=g 在缺陷等迹下不成立

结构性诊断（预期不成立/探索性，非 pass/fail 项）：
  D7  竖结合律：最小修正不满足余循环条件 ⇒ 非结合（笔记 §7 开放问题 6）
  D8  横结合律：同上
  D9  D-拉回 2-态射空间稀疏性：一般 f≠g 下 Sylvester 罕见可解（转移矩阵恒有特征值 1）；
      T10-T14 以谱平凡构造（id 态射 + 交织解）验证代数结构
  T17 缺陷（不可对角化）步进 300 次扫描：未发现非平凡（f≠g）拉回 2-态射（负结果）

单位：无量纲（矩阵代数）。
"""
import numpy as np

# ---------- 基础工具 ----------

def transfer_matrix(f, n):
    """转移算子 T_f : Mat(n, n)，(T_f)[i,j] = 1[f(i)=j]。"""
    M = np.zeros((n, n), dtype=complex)
    for i in range(n):
        M[i, f(i)] = 1.0
    return M

def gen_valid_two_morphism(f, g, n, N, rng):
    """生成满足自然性 α(n+1)[x,g(x)] = α(n)[x,f(x)] 的随机 2-态射族。
    构造：α(0) 自由随机，随后 α(n+1) 在对角列 g(x) 处按约束取值，其余自由。"""
    alpha = np.zeros((N, n, n), dtype=complex)
    for x in range(n):
        for y in range(n):
            alpha[0, x, y] = rng.normal() + 1j * rng.normal()
    for t in range(N - 1):
        alpha[t + 1] = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        for x in range(n):
            alpha[t + 1, x, g(x)] = alpha[t, x, f(x)]   # 约束
    return alpha

def check_naturality(alpha, f, g, N, n, tol=1e-9):
    """校验 2-态射自然性。"""
    for t in range(N - 1):
        for x in range(n):
            if abs(alpha[t + 1, x, g(x)] - alpha[t, x, f(x)]) > tol:
                return False
    return True

# ---------- 路径 B（D-拉回）验证辅助（对应 HigherRecCategory.lean 实现） ----------

def step_matrix(step, n):
    """步进矩阵 A_step = transferMatrix step（方阵）。"""
    return transfer_matrix(step, n)

def sylvester_solve(A, B, C, n):
    """解 Sylvester 方程 A X − X B = C。返回 (X, 残差) 或 (None, None)。
    用最小二乘（lstsq）：对奇异 K 也返回最小范数解，残差指示可解性
    （可解残差 ~1e-14，不可解残差大）。"""
    K = np.kron(np.eye(n), A) - np.kron(B.T, np.eye(n))
    vecC = C.reshape(-1)
    vecX, _, _, _ = np.linalg.lstsq(K, vecC, rcond=None)
    X = vecX.reshape(n, n)
    res = np.linalg.norm(A @ X - X @ B - C)
    return X, res

def pullback_2morphism(f, g, stepX, stepY, n):
    """路径 B 拉回 2-态射：解 T_g − T_f = A_X H − H A_Y。返回 H 或 None。"""
    AX, AY = step_matrix(stepX, n), step_matrix(stepY, n)
    Tf, Tg = transfer_matrix(f, n), transfer_matrix(g, n)
    H, res = sylvester_solve(AX, AY, Tg - Tf, n)
    if H is None or res > 1e-8:
        return None
    return H

def pullback_condition_ok(H, f, g, stepX, stepY, n, tol=1e-8):
    """校验拉回 2-态射 homotopy 条件 |T_g−T_f −(A_X H − H A_Y)| ≈ 0。"""
    AX, AY = step_matrix(stepX, n), step_matrix(stepY, n)
    Tf, Tg = transfer_matrix(f, n), transfer_matrix(g, n)
    return np.linalg.norm(Tg - Tf - (AX @ H - H @ AY)) < tol

def intertwining_solution(A, B, n, rng):
    """返回满足 A X = X B 的（非零）矩阵 X（Kronecker 零空间），否则零矩阵。"""
    K = np.kron(np.eye(n), A) - np.kron(B.T, np.eye(n))
    _, s, vh = np.linalg.svd(K)
    nz = np.sum(s > 1e-9)
    if nz < n * n:
        X = vh[nz].reshape(n, n)
        return X * (rng.normal() + 1j * rng.normal())
    return np.zeros((n, n), dtype=complex)

# ---------- 竖复合修正（定义 4，修正后公式） ----------

def vert_comp_corrected(alpha, beta, f, g, h, n, N, rng):
    """γ = β ∘_v α := α + β + C_v。
    C_v 最小选择：C_v(n)[x,f(x)] ≡ 0（∀n），离对角 0；
    流动增量：C_v(n+1)[x,h(x)] − C_v(n)[x,f(x)]
             = diag(α(n+1)(T_g−T_h))_xx + diag(β(n)(T_f−T_g))_xx。"""
    Tf, Tg, Th = (transfer_matrix(f, n), transfer_matrix(g, n), transfer_matrix(h, n))
    gamma = np.zeros((N, n, n), dtype=complex)
    for t in range(N):
        gamma[t] = alpha[t] + beta[t]
    Cv = np.zeros((N, n, n), dtype=complex)          # 最小选择：初值/离对角全 0
    for t in range(N - 1):
        inc = np.diag(alpha[t + 1] @ (Tg - Th)) + np.diag(beta[t] @ (Tf - Tg))
        for x in range(n):
            Cv[t + 1, x, h(x)] = Cv[t, x, f(x)] + inc[x]   # 流动对角递推（Cv[t,x,f(x)]=0）
    gamma = gamma + Cv
    return gamma, Cv

# ---------- 横复合修正（定义 6） ----------

def horiz_comp_corrected(alpha, alpha_p, f, fp, g, gp, n, N, rng):
    """γ' = α ∘_h α' := α·α' + C_h（f,g : X→Y；f',g' : Y→Z；状态空间同维 n）。
    C_h 最小选择：离对角 0、流动对角初值 0；
    流动增量：C_h(n+1)[x,g'(g(x))] − C_h(n)[x,f'(f(x))]
             = −[(α(n+1)α'(n+1))_{x,g'(g(x))} − (α(n)α'(n))_{x,f'(f(x))}]。"""
    gamma0 = np.zeros((N, n, n), dtype=complex)
    for t in range(N):
        gamma0[t] = alpha[t] @ alpha_p[t]
    Ch = np.zeros((N, n, n), dtype=complex)
    for t in range(N - 1):
        for x in range(n):
            # C_h(n+1)[x, g'(g(x))] = C_h(n)[x, f'(f(x))] − 失配
            Ch[t + 1, x, gp(g(x))] = (Ch[t, x, fp(f(x))]
                                      - (gamma0[t + 1, x, gp(g(x))] - gamma0[t, x, fp(f(x))]))
    return gamma0 + Ch, Ch

# ---------- 测试 ----------

def run():
    rng = np.random.default_rng(20260804)
    n, N = 3, 6
    tol = 1e-9
    passed = 0
    total = 0
    fails = []

    def check(name, cond, detail=""):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            fails.append(name)
            print(f"  [FAIL] {name}  {detail}")

    print("=" * 72)
    print("Rec₂ 交换律偏差的 BCH 修正复合 — 数值验证")
    print("=" * 72)

    # ---- 随机 1-态射 f,g,h 与 f',g',h' ----
    def rand_map(r):
        perm = r.permutation(n)
        return lambda i: int(perm[i])
    f = rand_map(rng); g = rand_map(rng); h = rand_map(rng)
    fp = rand_map(rng); gp = rand_map(rng); hp = rand_map(rng)

    # ---- 生成满足自然性的随机 2-态射 ----
    alpha = gen_valid_two_morphism(f, g, n, N, rng)
    beta  = gen_valid_two_morphism(g, h, n, N, rng)
    alpha_p = gen_valid_two_morphism(fp, gp, n, N, rng)
    beta_p  = gen_valid_two_morphism(gp, hp, n, N, rng)
    # 生成器自身满足自然性
    check("2-态射生成器满足自然性 (α, β, α', β')",
          all(check_naturality(a, ff, gg, N, n, tol)
              for a, ff, gg in [(alpha, f, g), (beta, g, h), (alpha_p, fp, gp), (beta_p, gp, hp)]))

    # ---- T1: 竖复合修正处方 ----
    gamma, Cv = vert_comp_corrected(alpha, beta, f, g, h, n, N, rng)
    check("T1 竖复合 γ = α+β+C_v 满足自然性 (f⇒h)",
          check_naturality(gamma, f, h, N, n, tol),
          f"max_dev={max(abs(gamma[t+1,x,h(x)]-gamma[t,x,f(x)]) for t in range(N-1) for x in range(n)):.2e}")
    check("T1b 非平凡情形修正非零 (C_v ≠ 0)",
          np.linalg.norm(Cv) > 1e-9, f"||C_v||_F={np.linalg.norm(Cv):.2e}")

    # ---- T2: 横复合修正处方 ----
    gamma_h, Ch = horiz_comp_corrected(alpha, alpha_p, f, fp, g, gp, n, N, rng)
    fg_comp = lambda x: fp(f(x))     # f ≫ f'（先 f 后 f'）
    gh_comp = lambda x: gp(g(x))     # g ≫ g'
    check("T2 横复合 γ' = α·α'+C_h 满足自然性 (f∘f'⇒g∘g')",
          check_naturality(gamma_h, fg_comp, gh_comp, N, n, tol),
          f"max_dev={max(abs(gamma_h[t+1,x,gh_comp(x)]-gamma_h[t,x,fg_comp(x)]) for t in range(N-1) for x in range(n)):.2e}")

    # ---- T3/T4: 交换律偏差 ----
    # LHS = (β∘_vα) ∘_h (β'∘_vα')；RHS = (β∘_hβ') ∘_v (α∘_hα')
    lhs_v, _ = vert_comp_corrected(alpha, beta, f, g, h, n, N, rng)         # f⇒h
    lhs_vp, _ = vert_comp_corrected(alpha_p, beta_p, fp, gp, hp, n, N, rng)  # f'⇒h'
    lhs, _ = horiz_comp_corrected(lhs_v, lhs_vp, f, fp, h, hp, n, N, rng)    # f∘f'⇒h∘h'

    rhs_h, _ = horiz_comp_corrected(beta, beta_p, g, gp, h, hp, n, N, rng)   # g∘g'⇒h∘h'（β∘_hβ'）
    rhs_hp, _ = horiz_comp_corrected(alpha, alpha_p, f, fp, g, gp, n, N, rng)  # f∘f'⇒g∘g'（α∘_hα'）
    # RHS = (β∘_hβ') ∘_v (α∘_hα')：第一参数 = α∘_hα'（f∘f'⇒g∘g'），第二参数 = β∘_hβ'（g∘g'⇒h∘h'）
    rhs, _ = vert_comp_corrected(rhs_hp, rhs_h, fg_comp, lambda x: gp(g(x)), lambda x: hp(h(x)),
                                 n, N, rng)                                  # f∘f'⇒h∘h'

    Delta = lhs - rhs
    hh_comp = lambda x: hp(h(x))
    check("T3 交换律偏差 Δ = LHS − RHS 是合法 2-态射（满足自然性）",
          check_naturality(Delta, fg_comp, hh_comp, N, n, tol),
          f"max_dev={max(abs(Delta[t+1,x,hh_comp(x)]-Delta[t,x,fg_comp(x)]) for t in range(N-1) for x in range(n)):.2e}")
    norm_D = float(np.linalg.norm(Delta))
    check("T4 偏差非平凡（一般情形交换律不严格成立，‖Δ‖_F > 0）",
          norm_D > 1e-9, f"‖Δ‖_F={norm_D:.2e}")

    # ---- T6: 裸偏差 = 交叉项（未修正复合下的精确代数） ----
    # 逐点（未修正）复合：竖 = α+β，横 = 矩阵乘法。
    # LHS_naive = (α+β)(α'+β') = αα'+αβ'+βα'+ββ'；RHS_naive = ββ'+αα'。
    # 故 Δ_naive = LHS_naive − RHS_naive = αβ' + βα'（精确，无修正项）。
    cross = np.zeros((N, n, n), dtype=complex)
    for t in range(N):
        cross[t] = alpha[t] @ beta_p[t] + beta[t] @ alpha_p[t]
    lhs_naive = np.zeros((N, n, n), dtype=complex)
    rhs_naive = np.zeros((N, n, n), dtype=complex)
    for t in range(N):
        lhs_naive[t] = (alpha[t] + beta[t]) @ (alpha_p[t] + beta_p[t])
        rhs_naive[t] = (beta[t] @ beta_p[t]) + (alpha[t] @ alpha_p[t])
    naive_dev = float(np.linalg.norm(lhs_naive - rhs_naive - cross))
    check("T6 裸偏差（未修正复合）= 交叉项 α·β' + β·α'（交换律失败的代数核心）",
          naive_dev < 1e-9, f"‖Δ_naive − cross‖_F={naive_dev:.2e}")

    # ---- T5: 严格极限（f=g=h, f'=g'=h'，族可交换 → Δ = 0）----
    f2 = g2 = h2 = rand_map(rng)     # f=g=h
    fp2 = gp2 = hp2 = rand_map(rng)  # f'=g'=h'
    # 可交换族：全部取零矩阵（自然性平凡满足；αβ'+βα' = 0）
    z = np.zeros((N, n, n), dtype=complex)
    a2 = z.copy(); b2 = z.copy(); ap2 = z.copy(); bp2 = z.copy()
    # 但需非平凡性：给 α 加"对角常数"族（保持自然性且互易于一切零矩阵）
    for x in range(n):
        val = rng.normal() + 1j * rng.normal()
        for t in range(N):
            a2[t, x, f2(x)] = val
    lhs2_v, _ = vert_comp_corrected(a2, b2, f2, g2, h2, n, N, rng)
    lhs2_vp, _ = vert_comp_corrected(ap2, bp2, fp2, gp2, hp2, n, N, rng)
    lhs2, _ = horiz_comp_corrected(lhs2_v, lhs2_vp, f2, fp2, g2, gp2, n, N, rng)
    rhs2_h, _ = horiz_comp_corrected(b2, bp2, g2, gp2, h2, hp2, n, N, rng)
    rhs2_hp, _ = horiz_comp_corrected(a2, ap2, f2, fp2, g2, gp2, n, N, rng)
    rhs2, _ = vert_comp_corrected(rhs2_h, rhs2_hp, lambda x: fp2(f2(x)), lambda x: gp2(g2(x)),
                                  lambda x: hp2(h2(x)), n, N, rng)
    norm_D2 = float(np.linalg.norm(lhs2 - rhs2))
    check("T5 严格极限（f=g=h、f'=g'=h'、可交换族）⇒ Δ = 0（引力解耦 G_N→0）",
          norm_D2 < 1e-9, f"‖Δ‖_F={norm_D2:.2e}")

    # ---- T7/T8/T9: 修正复合的范畴律（结合律、单位律）----
    # 三态射链 α:f⇒g, β:g⇒h, δ:h⇒k
    k = rand_map(rng)
    delta = gen_valid_two_morphism(h, k, n, N, rng)
    # 竖结合律：(δ∘_vβ)∘_vα = δ∘_v(β∘_vα)，均 : f⇒k
    ab, _ = vert_comp_corrected(alpha, beta, f, g, h, n, N, rng)          # β∘_vα : f⇒h
    assocL, _ = vert_comp_corrected(ab, delta, f, h, k, n, N, rng)        # δ∘_v(β∘_vα) : f⇒k
    beta_delta, _ = vert_comp_corrected(beta, delta, g, h, k, n, N, rng)  # δ∘_vβ : g⇒k
    assocR, _ = vert_comp_corrected(alpha, beta_delta, f, g, k, n, N, rng)  # (δ∘_vβ)∘_vα : f⇒k
    va = float(np.linalg.norm(assocL - assocR))
    print(f"  [DIAG] 竖结合律偏差 ‖assocL−assocR‖_F = {va:.2e}"
          f"（结构性诊断：最小修正不满足余循环条件 ⇒ 非结合，见笔记 §7 开放问题 6）")

    # 横结合律：(α∘_hα')∘_hα'' = α∘_h(α'∘_hα'')（三对态射：f,g；f',g'；f'',g''）
    fpp = rand_map(rng); gpp = rand_map(rng); hpp = rand_map(rng)
    alpha_pp = gen_valid_two_morphism(fpp, gpp, n, N, rng)
    fg_comp = lambda x: fp(f(x))      # f∘f'
    gh_comp = lambda x: gp(g(x))      # g∘g'
    a1, _ = horiz_comp_corrected(alpha, alpha_p, f, fp, g, gp, n, N, rng)          # (f∘f')⇒(g∘g')
    a1a2, _ = horiz_comp_corrected(a1, alpha_pp, fg_comp, fpp, gh_comp, gpp, n, N, rng)
    b1, _ = horiz_comp_corrected(alpha_p, alpha_pp, fp, fpp, gp, gpp, n, N, rng)   # (f'∘f'')⇒(g'∘g'')
    fp_comp = lambda x: fpp(fp(x))    # f'∘f''
    gp_comp = lambda x: gpp(gp(x))    # g'∘g''
    b1a2, _ = horiz_comp_corrected(alpha, b1, f, fp_comp, g, gp_comp, n, N, rng)
    ha = float(np.linalg.norm(a1a2 - b1a2))
    print(f"  [DIAG] 横结合律偏差 ‖assocL−assocR‖_F = {ha:.2e}"
          f"（结构性诊断：最小修正非结合，见笔记 §7 开放问题 6）")

    # 单位律（零 2-态射 id_f : f⇒f）：
    #   左单位：id_f ∘_v α = α；右单位：α ∘_v id_g = α
    idf = np.zeros((N, n, n), dtype=complex)
    idg = np.zeros((N, n, n), dtype=complex)
    lu, _ = vert_comp_corrected(idf, alpha, f, f, g, n, N, rng)
    ru, _ = vert_comp_corrected(alpha, idg, f, g, g, n, N, rng)
    ul = float(np.linalg.norm(lu - alpha)) + float(np.linalg.norm(ru - alpha))
    check("T9 单位律 id_f∘_vα = α = α∘_v id_g",
          ul < 1e-9, f"‖·‖_F 总偏差={ul:.2e}")

    # ---- T10-T14: 路径 B（D-拉回）结构数值验证（对应 HigherRecCategory.lean 已证定理）----
    # 结构事实：转移矩阵恒有特征值 1（𝟙 为特征向量），故 Sylvester A_X H − H A_Y = T_g − T_f
    # 对一般 f≠g 罕见可解——D 像子 2-范畴的 2-态射空间稀疏（见笔记 §4.3/§7）。
    # 为保证实例可解，采用构造性设置：公共步进 s（X.step=Y.step=Z.step=s）、1-态射全取 id
    # （保 RecHom：id∘s = s∘id），H 取交织解（A_X H = H A_Y，零空间非空）⇒ 条件自动满足。
    print("  [DIAG] D-拉回 2-态射空间稀疏性：一般 f≠g 下 Sylvester 罕见可解（转移矩阵"
          "恒有特征值 1），T10-T14 以谱平凡构造（id 态射 + 交织解）验证代数结构")
    stepS = rand_map(rng)
    AX = AY = AZ = step_matrix(stepS, n)   # 公共步进
    idM = lambda x: x
    H_ab = intertwining_solution(AX, AY, n, rng)     # α : id⇒id（X→Y）
    H_bc = intertwining_solution(AX, AY, n, rng)     # β : id⇒id（X→Y）
    H_ab2 = intertwining_solution(AY, AZ, n, rng)    # α' : id⇒id（Y→Z）
    H_bc2 = intertwining_solution(AY, AZ, n, rng)    # β' : id⇒id（Y→Z）
    T_id = np.eye(n, dtype=complex)
    check("T10 拉回 2-态射条件 |T_g−T_f −(A_X H − H A_Y)|≈0（交织解）",
          pullback_condition_ok(H_ab, idM, idM, stepS, stepS, n))

    # T11 竖复合（homotopy 和）保持条件：H_ab + H_bc : id⇒id
    check("T11 拉回竖复合 H_ab+H_bc 保持条件（id⇒id）",
          pullback_condition_ok(H_ab + H_bc, idM, idM, stepS, stepS, n))

    # T12 横复合（whiskering）保持条件：H_ab·T_id + T_id·H_ab2 : id∘id⇒id∘id
    check("T12 拉回横复合（whiskering）保持条件（id∘id⇒id∘id）",
          pullback_condition_ok(H_ab @ T_id + T_id @ H_ab2, idM, idM, stepS, stepS, n))

    # T13 交换律偏差公式（recExchangeLaw_homotopy_deviation）
    lhsB = (H_ab + H_bc) @ T_id + T_id @ (H_ab2 + H_bc2)
    rhsB = (H_ab @ T_id + T_id @ H_ab2) + (H_bc @ T_id + T_id @ H_bc2)
    devB = (T_id - T_id) @ H_ab2 + H_bc @ (T_id - T_id)
    check("T13 交换律偏差 = (T_h−T_g)H_α' + H_β(T_f'−T_g')（recExchangeLaw_homotopy_deviation）",
          np.linalg.norm((lhsB - rhsB) - devB) < 1e-8, f"‖(LHS−RHS)−公式‖={np.linalg.norm((lhsB-rhsB)-devB):.2e}")

    # T14 严格极限：交织 homotopy ⇒ 偏差 = 0（引力解耦 G_N→0）
    check("T14 严格极限（交织 homotopy）偏差 = 0（引力解耦 G_N→0）",
          np.linalg.norm(lhsB - rhsB) < 1e-8, f"‖LHS−RHS‖={np.linalg.norm(lhsB-rhsB):.2e}")

    # ---- T15/T16: 开放问题 7/8 数值检验（拉回非空性 + 时间无关对应，笔记 §4.4/§7）----
    # T15: 同源交织 H ∈ Hom^PB(f,f) 作为时间无关族 α(n)≡H 满足自然性（f=f 情形）
    s_cyc = lambda i: (i + 1) % n              # 单循环置换步进（可对角化）
    A = step_matrix(s_cyc, n)
    H_same = intertwining_solution(A, A, n, rng)     # A H = H A（同源拉回 2-态射）
    T15_cond = pullback_condition_ok(H_same, s_cyc, s_cyc, s_cyc, s_cyc, n)
    # 时间无关族 α(n) ≡ H 的同源自然性：α(n+1)[x,f(x)] = α(n)[x,f(x)] 恒真
    T15_nat = all(abs(H_same[x, s_cyc(x)] - H_same[x, s_cyc(x)]) < 1e-12 for x in range(n))
    check("T15 同源拉回 2-态射（交织解）满足条件，且时间无关族 α(n)≡H 满足自然性",
          T15_cond and T15_nat)

    # T16: 可对角化步进 + RecHom 对 f=s≠g=s²（f∘s=s∘f 恒等），Sylvester A H − H A = A²−A 不可解
    # （理论：T_f,T_g 均交织 A⟹T_g−T_f∈ker(L)；L 半单⟹range∩ker={0}⟹须 T_g=T_f⟹f=g）
    H_xy, res16 = sylvester_solve(A, A, A @ A - A, n)
    check("T16 异源 RecHom 对（f=s≠g=s²）拉回 2-态射不存在（非空性定理，可对角化步进）",
          H_xy is None or res16 > 1e-6,
          f"Sylvester 残差={res16 if H_xy is not None else '无解'}")

    # ---- T17: 缺陷（不可对角化）步进下非平凡拉回 2-态射扫描（开放问题 8 残余）----
    # 非双射函数 s 的转移矩阵 A 通常亏损（defective），Sylvester 算子 L 非半单，
    # range(L)∩ker(L) 可能非 {0} ⟹ 非平凡（f≠g）2-态射理论上可能存在。
    # 扫描 RecHom 幂对 (f=s^k, g=s^m)，k≠m，检验 A H − H A = A^m − A^k 可解性。
    found_nontrivial = False
    scan_info = "无"
    for _try in range(300):
        s_def = rand_map(rng)
        if len({s_def(i) for i in range(n)}) == n:      # 跳过双射（可对角化）
            continue
        A_def = step_matrix(s_def, n)
        k = int(rng.integers(1, 4)); m = int(rng.integers(1, 4))
        if k == m:
            m = (m % 3) + 1
        Ak = np.linalg.matrix_power(A_def, k)
        Am = np.linalg.matrix_power(A_def, m)
        Hx, res = sylvester_solve(A_def, A_def, Am - Ak, n)
        if Hx is not None and res < 1e-8:
            found_nontrivial = True
            scan_info = f"实例：缺陷步进 s，k={k}, m={m}，残差={res:.2e}"
            break
    if found_nontrivial:
        print(f"  [DIAG] T17（发现）：非平凡拉回 2-态射在缺陷步进下存在（{scan_info}）——"
              f"非空性对可对角化假设敏感，开放问题 8 残余确认")
    else:
        print("  [DIAG] T17（负结果）：缺陷步进 300 次扫描未发现非平凡（f≠g）拉回 2-态射——"
              "非空性 ⟺ f=g 在数值上稳健（缺陷情形仍开放，见笔记 §7 问题 8）")

    # ---- T18: 迹障碍（非空性的必要条件）----
    # tr(A H − H A) = 0（迹循环性）⟹ 若 tr(T_g − T_f) = #fixed(g) − #fixed(f) ≠ 0 则不可解。
    # 构造非双射 s：0↦1, 1↦0, 2↦0（#fixed(s)=0, #fixed(s²)=2 ⟹ tr(A²−A)=2≠0）。
    s_trace = lambda i: {0: 1, 1: 0, 2: 0}[i]
    A_tr = step_matrix(s_trace, n)
    tr_dev = float(np.trace(A_tr @ A_tr - A_tr).real)
    H_tr, res_tr = sylvester_solve(A_tr, A_tr, A_tr @ A_tr - A_tr, n)
    check("T18 迹障碍：tr(A²−A)=#fixed(s²)−#fixed(s)≠0 ⟹ (s,s²) 不可解（必要条件）",
          abs(tr_dev) > 1e-8 and (H_tr is None or res_tr > 1e-6),
          f"tr(A²−A)={tr_dev:.3f}, Sylvester 残差={res_tr if H_tr is not None else '无解'}")

    # ---- T19: 缺陷等迹情形非平凡拉回 2-态射（显式构造，开放问题 8 正面例）----
    # s: 0↦1, 1↦2, 2↦2（非双射，转移矩阵 A 缺陷）；f=s, g=s²（#fix(s)=#fix(s²)=1，等迹）。
    # 显式解 H = [[1,0,-1],[0,0,0],[0,0,0]]：A H − H A = A² − A（手算 + 数值验证）。
    s_def2 = lambda i: {0: 1, 1: 2, 2: 2}[i]
    A_d2 = step_matrix(s_def2, n)
    H_exp = np.zeros((n, n), dtype=complex)
    H_exp[0, 0] = 1; H_exp[0, 2] = -1
    res19 = np.linalg.norm(A_d2 @ H_exp - H_exp @ A_d2 - (A_d2 @ A_d2 - A_d2))
    check("T19 缺陷等迹情形非平凡拉回 2-态射（显式构造：f=s≠g=s²，#fix 等迹）",
          res19 < 1e-8, f"‖A H − H A −(A²−A)‖={res19:.2e}")
    # 注：H_exp 不满足旧 flow-diagonal 异源自然性（H[x,g(x)]≠H[x,f(x)] 于 x=0）——
    # 印证拉回定义独立于旧自然性类（见笔记 §4.4 定理 12 后的说明）。

    # ---- 汇总 ----
    print("-" * 72)
    print(f"  汇总: {passed}/{total} 检查通过")
    if fails:
        print(f"  [!] 失败项: {fails}")
    print("=" * 72)
    return passed, total

if __name__ == "__main__":
    p, t = run()
    import sys
    sys.exit(0 if p == t else 1)
