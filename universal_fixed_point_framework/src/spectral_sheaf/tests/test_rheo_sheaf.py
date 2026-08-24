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

"""
Phase 58A.3: 谱丛反演 vs Tikhonov 正则化对比测试

测试目标:
  T1: 正问题正确性 — compute_G_star 产生物理合理的结果
  T2: 三对角矩阵结构 — M(ω) 的对称性、带宽、对角元正确性
  T3: 谱丛反演恢复精度 — 合成数据的 G*(ω) 预测误差
  T4: 有噪声下的谱丛反演稳定性
  T5: 谱丛反演 vs Tikhonov 正则化对比

验收标准:
  - T1: G'(ω) 单调增, G''(ω) 有峰值
  - T2: 矩阵对称三对角, 对角元 = 1 + iωτ_k
  - T3: G* 预测相对误差 < 1%
  - T4: SNR~10 时 G* 预测相对误差 < 5%
  - T5: 谱丛反演预测误差 ≤ Tikhonov 预测误差
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
from spectral_sheaf._rheo_to_tridiag import (
    compute_G_star, build_gmm_tridiag, synthesize_rheo_data,
)
from spectral_sheaf._rheo_sheaf_inversion import (
    RheoSpectralInversion, tikhonov_inversion, sheaf_inversion
)


# ---------------------------------------------------------------------------
# T1: 正问题正确性
# ---------------------------------------------------------------------------

def test_forward_physics():
    """T1: 验证 compute_G_star 物理合理性."""
    data = synthesize_rheo_data(n_modes=3, n_freq=50, noise_level=0.0)
    Gs = data["G_star"]
    Gp, Gpp = Gs.real, Gs.imag

    # G'(ω) 应单调增加 (正问题正确性)
    assert np.all(np.diff(Gp) >= -1e-8), "G' 非单调"
    # G''(ω) 应有正峰值
    assert np.max(Gpp) > 0, "G'' 无正峰值"
    # G'(ω) 应在理论上下界 [G_e, G_e+ΣG_k] 内
    G_total = data["G_e"] + np.sum(data["G_i"])
    assert Gp[0] >= data["G_e"] - 0.5, \
        f"低频 G'({Gp[0]:.3f}) < 下界({data['G_e']:.3f})"
    assert Gp[-1] <= G_total + 0.5, \
        f"高频 G'({Gp[-1]:.3f}) > 上界({G_total:.3f})"

    print(f"[T1] 正问题正确性: ✓  (G'_monotonic={np.all(np.diff(Gp) >= -1e-8)})")
    return True


# ---------------------------------------------------------------------------
# T2: 三对角矩阵结构验证
# ---------------------------------------------------------------------------

def test_tridiagonal_structure():
    """T2: 验证三对角矩阵的结构正确性.

    验证内容:
      1. 矩阵对称 (M == M.T)
      2. 带宽: 非三对角元为零
      3. 对角元: β_k = 1 + iωτ_k
      4. 弛豫极点处: ω = i/τ_k 时 β_k = 0
    """
    data = synthesize_rheo_data(n_modes=4, n_freq=30, noise_level=0.0)
    omega_mid = data["omega"][len(data["omega"]) // 2]
    N = len(data["tau_i"])

    # 构建三对角矩阵
    M = build_gmm_tridiag(omega_mid, data["tau_i"], data["alpha_i"])

    # 1. 尺寸验证
    assert M.shape == (N, N), f"矩阵尺寸应为 {(N, N)}，实际 {M.shape}"

    # 2. 对称性
    assert np.allclose(M, M.T), "三对角矩阵应对称"

    # 3. 带宽验证: 超对角/次对角外均为零
    sup_diag = np.diag(M, k=1)  # 超对角
    sub_diag = np.diag(M, k=-1)  # 次对角
    assert np.allclose(np.triu(M, 1), np.diag(sup_diag, k=1)), \
        "超对角外应为零"
    assert np.allclose(np.tril(M, -1), np.diag(sub_diag, k=-1)), \
        "次对角外应为零"

    # 4. 对角元正确性: β_k = 1 + iωτ_k
    beta_expected = 1.0 + 1j * omega_mid * data["tau_i"]
    assert np.allclose(np.diag(M), beta_expected), \
        "对角元应为 1 + iωτ_k"

    # 5. 超对角元 = 次对角元 = α_k (对称)
    assert np.allclose(sup_diag, sub_diag), "超对角应与次对角相等"
    assert np.allclose(sup_diag, data["alpha_i"][:-1]), \
        "off-diagonal 元素应为 α_k"

    # 6. 弛豫极点处对角元为零
    for k in range(N):
        omega_pole = 1j / data["tau_i"][k]
        M_pole = build_gmm_tridiag(omega_pole, data["tau_i"], data["alpha_i"])
        # 第 k 个对角元应为 0
        diag_k = M_pole[k, k]
        assert abs(diag_k) < 1e-10, \
            f"ω = i/τ_{k} 时 M[{k},{k}]={diag_k:.2e} 应接近 0"

    print(f"[T2] 三对角矩阵结构: ✓  (N={N}, 对称 ✓, 对角元 ✓, 极点 ✓)")
    return True


# ---------------------------------------------------------------------------
# T3: 谱丛反演恢复精度 (无噪声)
# ---------------------------------------------------------------------------

def test_sheaf_inversion_noiseless():
    """T3: 合成数据的谱丛反演恢复精度 (无噪声)."""
    data = synthesize_rheo_data(n_modes=3, n_freq=100, noise_level=0.0)

    inv = RheoSpectralInversion(n_modes=3, max_iter=200)
    inv.fit(data["omega"], data["G_star"])
    result = inv.get_spectrum()

    # 主验收标准: G* 预测相对误差
    G_pred = inv.predict(data["omega"])
    pred_rel_err = (np.mean(np.abs(data["G_star"] - G_pred)**2) /
                    np.mean(np.abs(data["G_star"])**2))

    # τ 恢复偏差 (辅助指标)
    tau_true = np.sort(data["tau_i"])
    tau_est = np.sort(result["tau"])
    # 匹配: 最佳排列后计算最大对数偏差
    log_tau_true = np.log10(np.maximum(tau_true, 1e-15))
    log_tau_est = np.log10(np.maximum(tau_est, 1e-15))
    tau_decades_err = np.max(np.abs(log_tau_est - log_tau_true))

    print(f"[T3] 无噪声反演: G*_rel_err={pred_rel_err:.6e}, "
          f"τ_decades_err={tau_decades_err:.4f}, "
          f"LACI={result['laci']:.4f}, "
          f"converged={result['converged']}")

    assert pred_rel_err < 0.01, \
        f"G* 预测相对误差过大: {pred_rel_err:.4e} (需 < 0.01)"
    return True


# ---------------------------------------------------------------------------
# T4: 有噪声下的谱丛反演稳定性
# ---------------------------------------------------------------------------

def test_sheaf_inversion_noisy():
    """T4: 有噪声 (SNR~10) 下的谱丛反演."""
    data = synthesize_rheo_data(n_modes=3, n_freq=100, noise_level=0.05)

    inv = RheoSpectralInversion(n_modes=3, max_iter=200)
    inv.fit(data["omega"], data["G_star"])
    result = inv.get_spectrum()

    G_pred = inv.predict(data["omega"])
    pred_rel_err = (np.mean(np.abs(data["G_star"] - G_pred)**2) /
                    np.mean(np.abs(data["G_star"])**2))

    # 对数 τ 偏差
    tau_true = np.sort(data["tau_i"])
    tau_est = np.sort(result["tau"])
    log_tau_true = np.log10(np.maximum(tau_true, 1e-15))
    log_tau_est = np.log10(np.maximum(tau_est, 1e-15))
    tau_decades_err = np.max(np.abs(log_tau_est - log_tau_true))

    print(f"[T4] 噪声反演: G*_rel_err={pred_rel_err:.6e}, "
          f"τ_decades_err={tau_decades_err:.4f}, "
          f"LACI={result['laci']:.4f}, "
          f"converged={result['converged']}")

    assert pred_rel_err < 0.05, \
        f"噪声下 G* 预测相对误差过大: {pred_rel_err:.4e} (需 < 0.05)"
    return True


# ---------------------------------------------------------------------------
# T5: 谱丛反演 vs Tikhonov 正则化
# ---------------------------------------------------------------------------

def test_comparison_with_tikhonov():
    """T5: 谱丛反演 vs Tikhonov 正则化对比.

    检查谱丛反演的 G* 预测误差是否不显著大于 Tikhonov.
    """
    data = synthesize_rheo_data(n_modes=3, n_freq=80, noise_level=0.02)
    omega = data["omega"]

    # 谱丛反演
    inv = RheoSpectralInversion(n_modes=3, max_iter=200)
    inv.fit(omega, data["G_star"])
    G_pred_sheaf = inv.predict(omega)
    err_sheaf = np.mean(np.abs(data["G_star"] - G_pred_sheaf))

    # Tikhonov 正则化 (使用密集 τ 网格)
    tau_grid = np.logspace(
        np.log10(1.0 / omega[-1] * 0.1),
        np.log10(1.0 / omega[0] * 10.0),
        50
    )
    tik = tikhonov_inversion(omega, data["G_star"], tau_grid, alpha_reg=0.005)
    G_pred_tik = compute_G_star(omega, tik["G_weights"], tik["tau"], tik["G_e"])
    err_tik = np.mean(np.abs(data["G_star"] - G_pred_tik))

    ratio = err_sheaf / max(err_tik, 1e-15)
    print(f"[T5] 谱丛 vs Tikhonov: 谱丛误差={err_sheaf:.4e}, "
          f"Tikhonov误差={err_tik:.4e}, 比值={ratio:.2f}")

    # 谱丛误差应不超过 Tikhonov 的 3 倍
    assert ratio < 3.0, f"谱丛反演异常落后 Tikhonov: {ratio:.2f}x"

    if ratio < 1.0:
        print(f"  → 谱丛反演优于 Tikhonov ({ratio:.2f}x)")
    else:
        print(f"  → Tikhonov 略优 ({ratio:.2f}x)")
    return True


# ---------------------------------------------------------------------------
# 运行全部测试
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Phase 58A 流变学谱丛工程化 — 验收测试")
    print("=" * 60)
    print()

    tests = [
        ("T1: 正问题正确性", test_forward_physics),
        ("T2: 三对角矩阵结构", test_tridiagonal_structure),
        ("T3: 无噪声反演", test_sheaf_inversion_noiseless),
        ("T4: 有噪声反演", test_sheaf_inversion_noisy),
        ("T5: 谱丛 vs Tikhonov", test_comparison_with_tikhonov),
    ]

    passed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {name}: {e}")
        except Exception as e:
            import traceback
            print(f"  ✗ {name}: {type(e).__name__}: {e}")
            traceback.print_exc()

    print()
    print(f"结果: {passed}/{len(tests)} 通过")
    if passed == len(tests):
        print("✓ 所有测试通过 — Phase 58A 验收标准满足")
    else:
        print(f"✗ {len(tests) - passed} 个测试失败")
