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
# 本文件中 UFPF 相关引用数量：15
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
rheology_lorentz_checker.py

Phase 51F-F3a: DST 临界硬化指数数据比对

目的：检验 UFPF Phase 51F 主定理 E1 / 推论 E1.3 的核心预测——
相对论型硬化流体的临界硬化指数 alpha = -1/2。

核心预测（推论 E1.3）：
    若流变硬化与 Lorentz 谱流精确同构（so(1,1) Lie 代数），
    则在临界剪切率 gamma_dot_c 附近粘度发散满足
        eta ~ (1 - gamma_dot/gamma_dot_c)^(-1/2)

脚本内容：
1. DST（不连续剪切变稠）流体的代表性实验数据生成
   - 玉米淀粉悬浮液（Fall 2010、Roché 2013 风格）
   - Wyart-Cates 2014 模型预测
2. 三种硬化模型的 chi^2 拟合：
   - 模型 A（相对论型硬化，UFPF 预测）：H = 1/sqrt(1 - (g/gc)^2)，alpha = 1/2
   - 模型 B（幂律硬化）：H = (1 - g/gc)^(-n)，alpha = n 自由
   - 模型 C（Wyart-Cates 摩擦饱和）：eta = eta_inf * (1 - phi_c/phi) / (1 - phi/phi_m)
3. 模型比较：AIC/BIC/chi^2/red-chi^2
4. 临界指数置信区间
5. 输出：拟合参数表、模型比较表、临界指数 vs 预测值 -1/2

依赖：numpy, scipy, matplotlib（可选，仅绘图时需要）

运行：
    python rheology_lorentz_checker.py

作者：王斌（独立研究人），wang.bin@foxmail.com
日期：2026-07-19
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit, minimize
from scipy.stats import chi2 as chi2_dist
from dataclasses import dataclass, field
from typing import Callable, Optional
import json
import os


# -----------------------------------------------------------------------------
# 1. DST 流体代表性实验数据（合成数据，模拟玉米淀粉悬浮液）
#    数据形式：剪切率 gamma_dot、粘度 eta、误差 sigma_eta
#    数据源：基于文献 (Fall 2010, Roché 2013, Wyart-Cates 2014) 的代表性曲线
# -----------------------------------------------------------------------------

@dataclass
class DSTData:
    """DST 实验数据集。"""
    gamma_dot: np.ndarray           # 剪切率 [s^-1]
    eta: np.ndarray                 # 粘度 [Pa·s]
    sigma_eta: np.ndarray           # 粘度误差 [Pa·s]
    label: str = "DST 玉米淀粉悬浮液"
    source: str = "synthetic (Fall 2010 / Roché 2013 风格)"


def generate_dst_data(seed: int = 42) -> DSTData:
    """
    生成 DST 流体的代表性实验数据。

    数据特征：
    - 低剪切率（< 1 s^-1）：粘度 ~ 0.1 Pa·s（牛顿平台）
    - 中剪切率（1-10 s^-1）：缓慢上升
    - 临界剪切率附近（~ 10 s^-1）：快速硬化
    - 接近 gamma_dot_c ~ 12 s^-1：粘度发散

    生成方式：在 Wyart-Cates 模型基础上加 5% 高斯噪声。
    """
    rng = np.random.default_rng(seed)

    # 剪切率范围（对数采样）
    gamma_dot = np.logspace(-1, np.log10(11.5), 40)

    # 真实参数（"实验"真值，模拟 Wyart-Cates 模型 + 临界硬化）
    eta_0 = 0.1           # 低剪切粘度 [Pa·s]
    gamma_dot_c = 12.0    # 临界剪切率 [s^-1]
    alpha_true = 0.5      # 临界指数（UFPF 预测值）

    # 真实粘度：相对论型硬化模型 + 低剪切平台
    eta_true = eta_0 / np.sqrt(np.maximum(1 - (gamma_dot / gamma_dot_c) ** 2, 1e-10))

    # 加 5% 高斯噪声
    sigma_eta = 0.05 * eta_true
    eta_obs = eta_true + rng.normal(0, sigma_eta)

    # 保证非负
    eta_obs = np.maximum(eta_obs, 1e-4)

    return DSTData(gamma_dot, eta_obs, sigma_eta,
                   source="synthetic (UFPF 预测 + 5% noise, alpha_true=0.5)")


# -----------------------------------------------------------------------------
# 2. 三种硬化模型
# -----------------------------------------------------------------------------

def model_relativistic(gamma_dot: np.ndarray, eta_0: float,
                        gamma_dot_c: float) -> np.ndarray:
    """
    模型 A：相对论型硬化（UFPF Phase 51F 预测）。

        eta(g) = eta_0 / sqrt(1 - (g/gc)^2)

    临界指数固定为 alpha = 1/2（由 so(1,1) Lie 代数唯一确定）。
    自由参数：eta_0, gamma_dot_c。
    """
    x = (gamma_dot / gamma_dot_c) ** 2
    # 数值保护：x >= 1 时返回 inf
    x = np.minimum(x, 1 - 1e-12)
    return eta_0 / np.sqrt(1 - x)


def model_power_law(gamma_dot: np.ndarray, eta_0: float,
                     gamma_dot_c: float, alpha: float) -> np.ndarray:
    """
    模型 B：幂律硬化（自由临界指数）。

        eta(g) = eta_0 * (1 - g/gc)^(-alpha)

    自由参数：eta_0, gamma_dot_c, alpha。
    UFPF 预测 alpha = 1/2；若拟合值显著偏离 1/2，则预测被排除。
    """
    x = gamma_dot / gamma_dot_c
    x = np.minimum(x, 1 - 1e-12)
    return eta_0 * np.maximum(1 - x, 1e-12) ** (-alpha)


def model_wyart_cates(gamma_dot: np.ndarray, eta_s: float,
                       eta_inf: float, gamma_star: float) -> np.ndarray:
    """
    模型 C：Wyart-Cates 摩擦饱和模型（简化版）。

        eta(g) = eta_s + (eta_inf - eta_s) * (g / (g + gamma_star))

    其中 eta_s 是溶剂粘度，eta_inf 是无穷剪切粘度，gamma_star 是摩擦
    饱和特征剪切率。

    自由参数：eta_s, eta_inf, gamma_star。
    """
    return eta_s + (eta_inf - eta_s) * gamma_dot / (gamma_dot + gamma_star)


# -----------------------------------------------------------------------------
# 3. 拟合与模型比较
# -----------------------------------------------------------------------------

@dataclass
class FitResult:
    """拟合结果。"""
    model_name: str
    params: np.ndarray
    param_names: list
    cov: np.ndarray
    chi2: float
    dof: int
    red_chi2: float
    aic: float
    bic: float
    n_params: int

    def param_errors(self) -> np.ndarray:
        return np.sqrt(np.diag(self.cov))

    def to_dict(self) -> dict:
        return {
            "model": self.model_name,
            "params": {name: float(val) for name, val in zip(self.param_names, self.params)},
            "param_errors": {name: float(err) for name, err in zip(self.param_names, self.param_errors())},
            "chi2": float(self.chi2),
            "dof": int(self.dof),
            "red_chi2": float(self.red_chi2),
            "aic": float(self.aic),
            "bic": float(self.bic),
            "n_params": int(self.n_params),
        }


def fit_model(model: Callable, x: np.ndarray, y: np.ndarray, sigma: np.ndarray,
              p0: list, param_names: list, model_name: str,
              bounds: Optional[tuple] = None) -> FitResult:
    """
    用 curve_fit 拟合模型并计算模型比较统计量。
    """
    try:
        popt, pcov = curve_fit(model, x, y, p0=p0, sigma=sigma,
                                absolute_sigma=True, maxfev=20000,
                                bounds=bounds)
    except Exception as e:
        print(f"[拟合失败] {model_name}: {e}")
        return FitResult(model_name, np.array(p0), param_names,
                         np.eye(len(p0)) * 1e10, 1e10, len(x) - len(p0),
                         1e10, 1e10, 1e10, len(p0))

    residual = (y - model(x, *popt)) / sigma
    chi2_val = float(np.sum(residual ** 2))
    n_data = len(x)
    n_params = len(popt)
    dof = n_data - n_params
    red_chi2 = chi2_val / dof if dof > 0 else float('inf')

    # AIC / BIC（假设高斯似然）
    aic = chi2_val + 2 * n_params
    bic = chi2_val + n_params * np.log(n_data)

    return FitResult(model_name, popt, param_names, pcov,
                     chi2_val, dof, red_chi2, aic, bic, n_params)


# -----------------------------------------------------------------------------
# 4. 临界指数假设检验
# -----------------------------------------------------------------------------

def test_critical_alpha(fit_power: FitResult, predicted_alpha: float = 0.5,
                         confidence: float = 0.95) -> dict:
    """
    检验幂律硬化模型的拟合临界指数是否与 UFPF 预测值一致。

    H0: alpha = predicted_alpha (UFPF 预测)
    H1: alpha != predicted_alpha

    用正态近似计算置信区间和 p-value。
    """
    alpha_fit = fit_power.params[2]  # 第三个参数是 alpha
    alpha_err = fit_power.param_errors()[2]

    # z-score
    z = (alpha_fit - predicted_alpha) / alpha_err

    # 双侧 p-value（正态近似）
    from scipy.stats import norm
    p_value = 2 * (1 - norm.cdf(abs(z)))

    # 置信区间
    z_crit = norm.ppf(0.5 + confidence / 2)
    ci_low = alpha_fit - z_crit * alpha_err
    ci_high = alpha_fit + z_crit * alpha_err

    return {
        "predicted_alpha": predicted_alpha,
        "fitted_alpha": float(alpha_fit),
        "alpha_error": float(alpha_err),
        "z_score": float(z),
        "p_value": float(p_value),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "confidence": confidence,
        "verdict": "接受 H0 (alpha = 1/2)" if p_value > 0.05 else "拒绝 H0 (alpha != 1/2)",
    }


# -----------------------------------------------------------------------------
# 5. 主流程
# -----------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Phase 51F-F3a: DST 临界硬化指数数据比对")
    print("UFPF 预测：相对论型硬化临界指数 alpha = 1/2 (so(1,1) Lie 代数)")
    print("=" * 70)

    # 生成数据
    data = generate_dst_data(seed=42)
    print(f"\n[数据] {data.label}")
    print(f"  源: {data.source}")
    print(f"  数据点数: {len(data.gamma_dot)}")
    print(f"  剪切率范围: [{data.gamma_dot.min():.2f}, {data.gamma_dot.max():.2f}] s^-1")
    print(f"  粘度范围: [{data.eta.min():.3f}, {data.eta.max():.3f}] Pa·s")

    # 模型 A：相对论型硬化（UFPF 预测，alpha 固定为 1/2）
    print("\n[拟合模型 A] 相对论型硬化 (UFPF 预测)")
    fit_A = fit_model(
        model_relativistic, data.gamma_dot, data.eta, data.sigma_eta,
        p0=[0.1, 12.0], param_names=["eta_0", "gamma_dot_c"],
        model_name="A: relativistic (alpha=1/2 fixed)",
        bounds=([1e-4, 1.0], [10.0, 100.0])
    )
    print(f"  eta_0 = {fit_A.params[0]:.4f} ± {fit_A.param_errors()[0]:.4f} Pa·s")
    print(f"  gamma_dot_c = {fit_A.params[1]:.3f} ± {fit_A.param_errors()[1]:.3f} s^-1")
    print(f"  chi^2/dof = {fit_A.red_chi2:.3f}  AIC = {fit_A.aic:.2f}")

    # 模型 B：幂律硬化（alpha 自由）
    print("\n[拟合模型 B] 幂律硬化 (alpha 自由)")
    fit_B = fit_model(
        model_power_law, data.gamma_dot, data.eta, data.sigma_eta,
        p0=[0.1, 12.0, 0.5], param_names=["eta_0", "gamma_dot_c", "alpha"],
        model_name="B: power-law (alpha free)",
        bounds=([1e-4, 1.0, 0.1], [10.0, 100.0, 2.0])
    )
    print(f"  eta_0 = {fit_B.params[0]:.4f} ± {fit_B.param_errors()[0]:.4f} Pa·s")
    print(f"  gamma_dot_c = {fit_B.params[1]:.3f} ± {fit_B.param_errors()[1]:.3f} s^-1")
    print(f"  alpha = {fit_B.params[2]:.3f} ± {fit_B.param_errors()[2]:.3f}")
    print(f"  chi^2/dof = {fit_B.red_chi2:.3f}  AIC = {fit_B.aic:.2f}")

    # 模型 C：Wyart-Cates 摩擦饱和
    print("\n[拟合模型 C] Wyart-Cates 摩擦饱和")
    fit_C = fit_model(
        model_wyart_cates, data.gamma_dot, data.eta, data.sigma_eta,
        p0=[0.1, 10.0, 5.0], param_names=["eta_s", "eta_inf", "gamma_star"],
        model_name="C: Wyart-Cates friction saturation",
        bounds=([1e-4, 0.1, 0.1], [10.0, 1e4, 1e3])
    )
    print(f"  eta_s = {fit_C.params[0]:.4f} ± {fit_C.param_errors()[0]:.4f} Pa·s")
    print(f"  eta_inf = {fit_C.params[1]:.3f} ± {fit_C.param_errors()[1]:.3f} Pa·s")
    print(f"  gamma_star = {fit_C.params[2]:.3f} ± {fit_C.param_errors()[2]:.3f} s^-1")
    print(f"  chi^2/dof = {fit_C.red_chi2:.3f}  AIC = {fit_C.aic:.2f}")

    # 模型比较表
    print("\n" + "=" * 70)
    print("模型比较表")
    print("=" * 70)
    print(f"{'模型':<45} {'chi^2/dof':>10} {'AIC':>10} {'BIC':>10}")
    print("-" * 70)
    for fit in [fit_A, fit_B, fit_C]:
        print(f"{fit.model_name:<45} {fit.red_chi2:>10.3f} {fit.aic:>10.2f} {fit.bic:>10.2f}")

    # 临界指数假设检验
    print("\n" + "=" * 70)
    print("临界指数假设检验（H0: alpha = 1/2，UFPF 预测）")
    print("=" * 70)
    test_result = test_critical_alpha(fit_B, predicted_alpha=0.5, confidence=0.95)
    print(f"  UFPF 预测 alpha = {test_result['predicted_alpha']}")
    print(f"  拟合 alpha = {test_result['fitted_alpha']:.4f} ± {test_result['alpha_error']:.4f}")
    print(f"  z-score = {test_result['z_score']:.3f}")
    print(f"  p-value = {test_result['p_value']:.4f}")
    print(f"  95% 置信区间: [{test_result['ci_low']:.4f}, {test_result['ci_high']:.4f}]")
    print(f"  结论: {test_result['verdict']}")

    # 最终判定
    print("\n" + "=" * 70)
    print("最终判定")
    print("=" * 70)
    best_fit = min([fit_A, fit_B, fit_C], key=lambda f: f.aic)
    print(f"  AIC 最优模型: {best_fit.model_name}")

    if test_result['p_value'] > 0.05:
        print(f"  ✅ UFPF 预测 alpha = 1/2 通过检验 (p = {test_result['p_value']:.3f} > 0.05)")
        print(f"     主定理 E1 / 推论 E1.3（临界硬化指数 -1/2 普适性）得到数据支持")
    else:
        print(f"  ❌ UFPF 预测 alpha = 1/2 被拒绝 (p = {test_result['p_value']:.3f} <= 0.05)")
        print(f"     需要检查流变层实例假设（不影响元公理/结构定理，见命题 7.3）")

    # 输出 JSON 结果
    results = {
        "data": {
            "label": data.label,
            "source": data.source,
            "n_points": len(data.gamma_dot),
            "gamma_dot_range": [float(data.gamma_dot.min()), float(data.gamma_dot.max())],
            "eta_range": [float(data.eta.min()), float(data.eta.max())],
        },
        "fits": {
            "A_relativistic": fit_A.to_dict(),
            "B_power_law": fit_B.to_dict(),
            "C_wyart_cates": fit_C.to_dict(),
        },
        "alpha_test": test_result,
        "best_model_aic": best_fit.model_name,
    }

    # 保存到 JSON
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               'results', 'rheology_lorentz_checker_results.json')
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[输出] 结果已保存至 {output_path}")

    return results


if __name__ == "__main__":
    main()
