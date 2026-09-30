# -*- coding: utf-8 -*-
"""
Phase 71 阶段1：单负胶子剥离振幅数值验证 (arXiv:2602.12176v2)
=============================================================
验证目标：
  T1: n=3..6 显式公式(29)-(32) 与 R1区域通式(39) 数值一致（半共线+R1+动量守恒配置）
  T2: 软定理(28)：(39) 生成的 A_{1..n} 在 omega_n->0 极限满足 lim = (1/2)(sg_{n-1,n}+sg_{n,n1}) A_{1..n-1}
  T3: 一致性检查：循环性(24)、反射(25)、U(1)解耦(26)、KK(27)（一般半共线配置，(29)-(31)）
  T4: R1 化简式(35)-(38) 与通式(39) 完全一致（防抄写错误）

记号（论文 frame (2)）：
  |i> = lambda_i = (1, z_i),  |i] = tilde_lambda_i = omega_i (1, zbar_i)
  半共线: <ij> = z_ij = 0 (z_i 全相等)
  R1:     omega_1 < 0, omega_a > 0 (a=2..n)
  动量守恒(右旋量): tilde_lambda_n = -sum_{i<n} tilde_lambda_i
  sg_{A,B} = sg([sum tilde_lambda_A, sum tilde_lambda_B])
           = sg( sum_{i in A, j in B} omega_i omega_j (zbar_i - zbar_j) )
  无逗号 sg_{i1...ik} (递增) = sg([tilde_lambda_{i1}, tilde_lambda_{i2}+...+tilde_lambda_{ik}])
"""
import json
import random

SEED = 20260930
random.seed(SEED)


def sg(x):
    """sign 函数：论文 sg(x)=2Theta(x)-1；x=0 时取 0（随机采样避免恰好为 0）"""
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def sg_pair(omega, zbar, i, j):
    """sg_{ij} = sg([tilde_lambda_i, tilde_lambda_j]) = sg(omega_i omega_j (zbar_i - zbar_j))"""
    return sg(omega[i] * omega[j] * (zbar[i] - zbar[j]))


def sg_block(omega, zbar, A, B):
    """sg_{A,B} = sg([sum_{i in A} tilde_lambda_i, sum_{j in B} tilde_lambda_j])"""
    s = 0.0
    for i in A:
        for j in B:
            s += omega[i] * omega[j] * (zbar[i] - zbar[j])
    return sg(s)


# ---------- 显式公式 (29)-(32)，0-based 下标 ----------

def A3(omega, zbar):
    """(29) A_123 = sg_12"""
    return sg_pair(omega, zbar, 0, 1)


def A4(omega, zbar):
    """(30) A_1234 = 1/2 [sg_23 sg_41 + sg_12 sg_34]"""
    return 0.5 * (
        sg_pair(omega, zbar, 1, 2) * sg_pair(omega, zbar, 3, 0)
        + sg_pair(omega, zbar, 0, 1) * sg_pair(omega, zbar, 2, 3)
    )


def A5(omega, zbar):
    """(31) A_12345，8 项（2026-09-30 修正：项1= sg_51【第1版OCR】，首索引规则
    sg_{abc...} = sg([λ_a, λ_b+λ_c+...])；项4/5/7/8 原实现用错 sg 级联记号，已修正）
    注：generic 配置下与 (21)/(39) 完全一致；剥离振幅=0 的退化配置（预振幅 Θ 消失）
    下存在残余不一致（≈0.6%），疑似论文印刷级问题，待 paperX 验证小结记录。
    """
    w, z = omega, zbar
    s51 = sg_block(w, z, (4,), (0,))
    s12 = sg_pair(w, z, 0, 1)
    s23 = sg_pair(w, z, 1, 2)
    s34 = sg_pair(w, z, 2, 3)
    s45 = sg_pair(w, z, 3, 4)
    s234 = sg_block(w, z, (1,), (2, 3))
    s123 = sg_block(w, z, (0,), (1, 2))
    s1234 = sg_block(w, z, (0,), (1, 2, 3))
    return 0.25 * (
        s51 * s34 * s234
        + s51 * s23 * s234
        - s51 * s234 * s234
        + s45 * s23 * s123
        + s45 * s12 * s123
        - s45 * s123 * s123
        + s51 * s45 * s1234
        + s12 * s34 * s1234
    )


def A6(omega, zbar):
    """(32) A_123456，32 项（2026-09-30 依据放大OCR：显式逗号，块和|块和规则
    sg_{A,B} = sg([Σλ_A, Σλ_B])；与 BG 递归(21) 3000/3000 一致）
    """
    w, z = omega, zbar
    s1_23  = sg_block(w, z, (0,), (1, 2))
    s12_3  = sg_block(w, z, (0, 1), (2,))
    s123_4 = sg_block(w, z, (0, 1, 2), (3,))
    s56    = sg_pair(w, z, 4, 5)
    s23    = sg_pair(w, z, 1, 2)
    s1_234 = sg_block(w, z, (0,), (1, 2, 3))
    s12_34 = sg_block(w, z, (0, 1), (2, 3))
    s34    = sg_pair(w, z, 2, 3)
    s2_34  = sg_block(w, z, (1,), (2, 3))
    s23_4  = sg_block(w, z, (1, 2), (3,))
    s12    = sg_pair(w, z, 0, 1)
    s345_6 = sg_block(w, z, (2, 3, 4), (5,))
    s45_6  = sg_block(w, z, (3, 4), (5,))
    s45    = sg_pair(w, z, 3, 4)
    s3_45  = sg_block(w, z, (2,), (3, 4))
    s34_5  = sg_block(w, z, (2, 3), (4,))
    s234_5 = sg_block(w, z, (1, 2, 3), (4,))
    s61    = sg_block(w, z, (5,), (0,))
    s2_345 = sg_block(w, z, (1,), (2, 3, 4))
    s23_45 = sg_block(w, z, (1, 2), (3, 4))
    return 1.0 / 8.0 * (
        -s1_23 * s12_3 * s123_4 * s56
        + s1_23 * s123_4 * s23 * s56
        + s1_234 * s12_34 * s123_4 * s56
        - s1_234 * s12_34 * s34 * s56
        - s1_234 * s123_4 * s23 * s56
        - s1_234 * s2_34 * s23_4 * s56
        + s1_234 * s2_34 * s34 * s56
        + s1_234 * s23 * s23_4 * s56
        + s12 * s12_3 * s123_4 * s56
        - s12 * s12_34 * s123_4 * s56
        + s12 * s12_34 * s34 * s56
        + s12 * s345_6 * s45_6 * s56
        - s1_23 * s12_3 * s45 * s45_6
        + s1_23 * s23 * s45 * s45_6
        + s12 * s12_3 * s45 * s45_6
        - s12 * s3_45 * s34_5 * s345_6
        + s12 * s3_45 * s345_6 * s45
        + s12 * s34 * s34_5 * s345_6
        - s2_34 * s23_4 * s234_5 * s61
        + s2_34 * s234_5 * s34 * s61
        + s2_345 * s23_45 * s234_5 * s61
        - s2_345 * s23_45 * s45 * s61
        - s2_345 * s234_5 * s34 * s61
        - s2_345 * s3_45 * s34_5 * s61
        + s2_345 * s3_45 * s45 * s61
        + s2_345 * s34 * s34_5 * s61
        + s23 * s23_4 * s234_5 * s61
        - s23 * s23_45 * s234_5 * s61
        + s23 * s23_45 * s45 * s61
        + s345_6 * s45 * s45_6 * s61
        + s23 * s45_6 * s56 * s61
        + s34 * s345_6 * s56 * s61
    )


EXPLICIT = {3: A3, 4: A4, 5: A5, 6: A6}


def A_R1(omega, zbar):
    """通式(39): A_{1..n}|R1 = 2^{2-n} prod_{m=2}^{n-1} (sg_{m,m+1} + sg_{1,2..m})"""
    n = len(omega)
    val = 1.0
    for m in range(2, n):  # m = 2..n-1 (1-based); 0-based: 因子 (m-1,m) 与 (0, 1..m-1)
        fac = sg_pair(omega, zbar, m - 1, m) + sg_block(omega, zbar, (0,), tuple(range(1, m)))
        val *= fac
    return val / (2 ** (n - 2))


def r1_reduced(omega, zbar):
    """R1 化简式(35)-(38)，n=3..6（应等于(39)）"""
    n = len(omega)
    w, z = omega, zbar
    s12 = sg_pair(w, z, 0, 1)
    s23 = sg_pair(w, z, 1, 2)
    if n == 3:
        return 0.5 * (s12 + s23)
    s34 = sg_pair(w, z, 2, 3)
    if n == 4:
        return 0.25 * (s12 + s23) * (s34 + sg_pair(w, z, 3, 0))
    s123 = sg_block(w, z, (0,), (1, 2))
    s45 = sg_pair(w, z, 3, 4)
    s51 = sg_block(w, z, (4,), (0,))
    if n == 5:
        return 1.0 / 8.0 * (s12 + s23) * (s34 + s123) * (s45 + s51)
    s1234 = sg_block(w, z, (0,), (1, 2, 3))
    s56 = sg_pair(w, z, 4, 5)
    s61 = sg_block(w, z, (5,), (0,))
    return 1.0 / 16.0 * (s12 + s23) * (s34 + s123) * (s45 + s1234) * (s56 + s61)


# ---------- 运动学配置生成 ----------

def gen_R1_momentum(n, rng=random):
    """
    半共线 + R1 + 右旋量动量守恒配置：
      半共线: z_i = 0 (取 zbar 随机)
      R1:     omega_1 < 0, omega_a > 0 (a=2..n)
      动量守恒: tilde_lambda_n = -sum_{i<n} tilde_lambda_i
              -> omega_n = -sum_{i<n} omega_i,  zbar_n = sum_{i<n} omega_i zbar_i / sum_{i<n} omega_i
      要求: sum_{i<n} omega_i < 0  (保证 omega_n > 0)
    """
    while True:
        omega = [0.0] * n
        omega[0] = -rng.uniform(1.0, 5.0)
        for a in range(1, n - 1):
            omega[a] = rng.uniform(0.1, 2.0)
        if sum(omega[: n - 1]) < -0.05:   # omega_n = -sum > 0
            break
    zbar = [rng.uniform(-3.0, 3.0) for _ in range(n - 1)]
    s = sum(omega[: n - 1])
    omega[n - 1] = -s
    zbar_n = sum(omega[i] * zbar[i] for i in range(n - 1)) / s
    zbar.append(zbar_n)
    return omega, zbar


def gen_generic_halfcollinear(n, rng=random):
    """一般半共线配置（无 R1、无动量守恒）：z_i=0, zbar 随机, omega 随机非零"""
    omega = [rng.choice([-1.0, 1.0]) * rng.uniform(0.5, 2.0) for _ in range(n)]
    zbar = [rng.uniform(-3.0, 3.0) for _ in range(n)]
    return omega, zbar


# ---------- 验证 T1: 显式公式 vs 通式(39) ----------

def check_T1(n_samples=2000):
    results = {}
    for n in (3, 4, 5, 6):
        nfail = 0
        maxdev = 0.0
        for _ in range(n_samples):
            omega, zbar = gen_R1_momentum(n)
            a_exp = EXPLICIT[n](omega, zbar)
            a_r1 = A_R1(omega, zbar)
            if abs(a_exp - a_r1) > 1e-12:
                nfail += 1
                maxdev = max(maxdev, abs(a_exp - a_r1))
        results[f"n={n}"] = {
            "samples": n_samples,
            "fail": nfail,
            "max_dev": maxdev,
            "pass": nfail == 0,
        }
    return results


# ---------- 验证 T4: R1化简式(35)-(38) vs 通式(39) ----------

def check_T4(n_samples=2000):
    results = {}
    for n in (3, 4, 5, 6):
        nfail = 0
        for _ in range(n_samples):
            omega, zbar = gen_R1_momentum(n)
            if abs(r1_reduced(omega, zbar) - A_R1(omega, zbar)) > 1e-12:
                nfail += 1
        results[f"n={n}"] = {"samples": n_samples, "fail": nfail, "pass": nfail == 0}
    return results


# ---------- 验证 T2: 软定理(28) ----------
# lim_{omega_n->0} A_{1..n} = (1/2)(sg_{n-1,n} + sg_{n,n1}) A_{1..n-1}

def soft_ratio(n, eps, rng=random):
    """
    构造满足动量守恒的配置，omega_n = eps（R1 要求 eps>0），
    比较 A_{1..n}(39) 与 (1/2)(sg_{n-1,n}+sg_{n,n1}) A_{1..n-1}(39)
    sg_{n,n1} 取两种解释：E1 = sg([lam_n, lam_n+lam_1])，E2 = sg([lam_n, lam_1])
    """
    # 前 n-1 个：omega_1<0, omega_2..n-1>0；动量守恒给 omega_n = -sum_{i<n} omega_i
    # 要求 omega_n = eps（软极限：让 omega_n = eps，则 sum_{i<n} omega_i = -eps）
    while True:
        omega_head = [0.0] * (n - 1)
        omega_head[0] = -rng.uniform(1.0, 5.0)
        for a in range(1, n - 2):
            omega_head[a] = rng.uniform(0.1, 2.0)
        # sum_{i<n} omega_i = -eps：最后一个头部 omega 由它决定
        # 需 omega_{n-2} 的取值使总和无解 -> 直接设 omega_{n-2} = -eps - sum(其它)
        s_other = sum(omega_head[: n - 2])
        omega_head[n - 2] = -eps - s_other
        if omega_head[n - 2] > 0.05:  # R1 要求 omega_{n-1} > 0
            break
    omega = omega_head + [eps]
    zbar_head = [rng.uniform(-3.0, 3.0) for _ in range(n - 1)]
    s = sum(omega_head)
    zbar = zbar_head + [sum(omega_head[i] * zbar_head[i] for i in range(n - 1)) / s]
    a_n = A_R1(omega, zbar)
    a_nm1 = A_R1(omega_head, zbar_head)
    s_nm1n = sg_pair(omega, zbar, n - 2, n - 1)
    # E1: sg([lam_n, lam_n+lam_1])
    s_nn1_E1 = sg_block(omega, zbar, (n - 1,), (n - 1, 0))
    # E2: sg([lam_n, lam_1])
    s_nn1_E2 = sg_pair(omega, zbar, n - 1, 0)
    lhs = a_n
    rhs_E1 = 0.5 * (s_nm1n + s_nn1_E1) * a_nm1
    rhs_E2 = 0.5 * (s_nm1n + s_nn1_E2) * a_nm1
    # 动量守恒下 sg_{n,n1} 理论值：lam_n = -sum_{i<n} lam_i
    # [lam_n, lam_n+lam_1] = [lam_n, lam_1]（自括号为零）
    return lhs, rhs_E1, rhs_E2


def check_T2(eps_list=(0.1, 0.01, 0.001), n_samples=400):
    results = {}
    for n in (4, 5, 6, 7, 8):
        for eps in eps_list:
            nf_E1 = nf_E2 = 0
            worst_E1 = worst_E2 = 0.0
            for _ in range(n_samples):
                lhs, r1, r2 = soft_ratio(n, eps)
                if lhs != 0.0:
                    d1 = abs(lhs - r1) / max(abs(lhs), 1e-30)
                    d2 = abs(lhs - r2) / max(abs(lhs), 1e-30)
                else:
                    d1 = abs(lhs - r1)
                    d2 = abs(lhs - r2)
                if d1 > 1e-9:
                    nf_E1 += 1
                    worst_E1 = max(worst_E1, d1)
                if d2 > 1e-9:
                    nf_E2 += 1
                    worst_E2 = max(worst_E2, d2)
            results[f"n={n},eps={eps}"] = {
                "fail_E1(sg_n,n1=sg([n,n1]))": nf_E1,
                "fail_E2(sg_n,n1=sg([n,1]))": nf_E2,
                "worst_E1": worst_E1,
                "worst_E2": worst_E2,
                "pass_E1": nf_E1 == 0,
                "pass_E2": nf_E2 == 0,
            }
    return results


# ---------- 验证 T3: 循环性/反射/U(1)/KK（一般半共线，(29)-(31)） ----------

def permute_args(fn, omega, zbar, perm):
    """按 perm（0-based 新序 = [旧索引]）重排 omega,zbar 并调用 fn"""
    om = [omega[i] for i in perm]
    zb = [zbar[i] for i in perm]
    return fn(om, zb)


def check_cyclicity(n_samples=2000):
    nfail = 0
    for _ in range(n_samples):
        omega, zbar = gen_generic_halfcollinear(5)
        a1 = A5(omega, zbar)                          # A_12345
        a2 = permute_args(A5, omega, zbar, [1, 2, 3, 4, 0])  # A_23451
        if abs(a1 - a2) > 1e-12:
            nfail += 1
    return {"samples": n_samples, "fail": nfail, "pass": nfail == 0}


def check_reflection(n_samples=2000):
    nfail = 0
    for _ in range(n_samples):
        omega, zbar = gen_generic_halfcollinear(4)
        a1 = A4(omega, zbar)                          # A_1234
        a2 = permute_args(A4, omega, zbar, [3, 2, 1, 0])   # A_4321
        if abs(a1 - (-1) ** 4 * a2) > 1e-12:          # (25): A_1234 = (+1) A_4321
            nfail += 1
        omega, zbar = gen_generic_halfcollinear(5)
        a1 = A5(omega, zbar)
        a2 = permute_args(A5, omega, zbar, [4, 3, 2, 1, 0])  # A_54321
        if abs(a1 - (-1) ** 5 * a2) > 1e-12:          # (25): A_12345 = (-1) A_54321
            nfail += 1
    return {"samples": n_samples, "fail": nfail, "pass": nfail == 0}


def check_U1_decoupling(n_samples=2000):
    """(26) n=5: A_12345 + A_13452 + A_14523 + A_15234 = 0"""
    nfail = 0
    perms = [[0, 2, 3, 4, 1], [0, 3, 4, 1, 2], [0, 4, 1, 2, 3]]  # 13452, 14523, 15234
    for _ in range(n_samples):
        omega, zbar = gen_generic_halfcollinear(5)
        total = A5(omega, zbar)
        for p in perms:
            total += permute_args(A5, omega, zbar, p)
        if abs(total) > 1e-12:
            nfail += 1
    return {"samples": n_samples, "fail": nfail, "pass": nfail == 0}


def check_KK(n_samples=2000):
    """(27) n=5: A_12345 + A_12354 + A_12435 + A_14235 = 0"""
    nfail = 0
    perms = [[0, 1, 2, 4, 3], [0, 1, 3, 2, 4], [0, 3, 1, 2, 4]]  # 12354, 12435, 14235
    for _ in range(n_samples):
        omega, zbar = gen_generic_halfcollinear(5)
        total = A5(omega, zbar)
        for p in perms:
            total += permute_args(A5, omega, zbar, p)
        if abs(total) > 1e-12:
            nfail += 1
    return {"samples": n_samples, "fail": nfail, "pass": nfail == 0}


def check_T3():
    return {
        "cyclicity(24)": check_cyclicity(),
        "reflection(25)": check_reflection(),
        "U1_decoupling(26)": check_U1_decoupling(),
        "KK(27)": check_KK(),
    }


# ---------- 主流程 ----------

def main():
    print("=" * 70)
    print("Phase 71 阶段1: 单负剥离振幅数值验证 (2602.12176v2)")
    print("=" * 70)

    print("\n[T1] 显式公式(29)-(32) vs 通式(39)（半共线+R1+动量守恒）")
    t1 = check_T1()
    for k, v in t1.items():
        print(f"  {k}: samples={v['samples']}, fail={v['fail']}, max_dev={v['max_dev']:.2e}, pass={v['pass']}")

    print("\n[T4] R1化简式(35)-(38) vs 通式(39)")
    t4 = check_T4()
    for k, v in t4.items():
        print(f"  {k}: samples={v['samples']}, fail={v['fail']}, pass={v['pass']}")

    print("\n[T2] 软定理(28)（eps->0 极限，n=4..8）")
    t2 = check_T2()
    for k, v in t2.items():
        print(f"  {k}: fail_E1={v['fail_E1(sg_n,n1=sg([n,n1]))']}, "
              f"fail_E2={v['fail_E2(sg_n,n1=sg([n,1]))']}, pass_E1={v['pass_E1']}, pass_E2={v['pass_E2']}")

    print("\n[T3] 一致性检查（一般半共线配置，n=4,5）")
    t3 = check_T3()
    for k, v in t3.items():
        print(f"  {k}: samples={v['samples']}, fail={v['fail']}, pass={v['pass']}")

    # 保存结果
    results = {"T1": t1, "T2": t2, "T3": t3, "T4": t4,
               "config": "z_i=0 (half-collinear); R1: omega1<0, omega_a>0; momentum: tilde_lambda_n=-sum_{i<n}",
               "seed": SEED}
    out_path = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_single_minus_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n结果已保存: {out_path}")

    allpass = all(v["pass"] for v in t1.values()) and all(v["pass"] for v in t4.values()) \
        and all(v["pass_E1"] or v["pass_E2"] for v in t2.values()) \
        and all(v["pass"] for v in t3.values())
    print("\n总体结论:", "全部通过" if allpass else "存在失败项（见上）")
    return allpass


if __name__ == "__main__":
    main()
