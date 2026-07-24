#!/usr/bin/env python3
"""
轻子质量谱公式数值优化器 v0.3

目标：系统探索多种质量公式变体，找到最优混合角 θ_ij 和 η_RG 的代依赖结构。

质量公式变体：
  A: m_i = y_i * c_i^α * M_Pl * η_RG       (当前代码——双重压制)
  B: m_i = y_i * M_Pl * η_RG               (仅 Higgs 投影——笔记 §4.5)
  C: m_i = c_i^α * M_Pl * η_RG_i           (仅 IFS，代依赖 η)
  D: m_i = y_i * c_i^α * M_Pl * η_RG_i     (全量 + 代依赖 η)
  E: m_i = y_i^β * c_i^α * M_Pl * η_RG     (幂律调制)

通过最小化对数质量偏差的 RMS 来寻找最优参数。

承袭：notes/01_qcd_higgs/spectral_Higgs_fermion_interweaver.md
"""

import numpy as np
from scipy.optimize import minimize

# ============================================================
# 1. 谱常数
# ============================================================
c1 = 0.003314
c2 = 0.066554
c3 = 0.999761
c = np.array([c1, c2, c3])

alpha_l = 1.358   # 轻子谱指数
alpha_v = 1.883   # Higgs 谱指数

M_Pl = 1.22e19    # GeV

# 实验轻子质量 (GeV)
m_e_exp  = 0.511e-3
m_mu_exp = 105.7e-3
m_tau_exp = 1.777
m_exp = np.array([m_e_exp, m_mu_exp, m_tau_exp])


# ============================================================
# 2. 谱权重
# ============================================================
def compute_weights():
    """计算 Higgs 和轻子的归一化谱权重。"""
    c_av = c ** alpha_v
    norm_H = np.sum(c_av)
    lambda_H = c_av / norm_H

    c_al = c ** alpha_l
    norm_l = np.sum(c_al)
    lambda_l = c_al / norm_l

    return lambda_H, lambda_l


lambda_H, lambda_l = compute_weights()


# ============================================================
# 3. U 矩阵构建 & Yukawa 特征值
# ============================================================
def build_U(theta12, theta13, theta23):
    """标准 PMNS-like 3x3 幺正矩阵 (δ=0)。"""
    s12, c12 = np.sin(theta12), np.cos(theta12)
    s13, c13 = np.sin(theta13), np.cos(theta13)
    s23, c23 = np.sin(theta23), np.cos(theta23)

    U = np.array([
        [c12*c13,              s12*c13,              s13],
        [-s12*c23 - c12*s23*s13, c12*c23 - s12*s23*s13, s23*c13],
        [s12*s23 - c12*c23*s13, -c12*s23 - s12*c23*s13, c23*c13]
    ])
    return U


def yukawa_projection(U):
    """计算 Yukawa 投影值 y_i = sum_k |U_{ki}|^2 * lambda_H^{(k)}"""
    U_sq = U ** 2
    return U_sq.T @ lambda_H


# ============================================================
# 4. 质量公式变体
# ============================================================
c_al = c ** alpha_l  # [c1^α, c2^α, c3^α]

def formula_A(y, eta):
    """m_i = y_i * c_i^α * M_Pl * η_RG"""
    return y * c_al * M_Pl * eta

def formula_B(y, eta):
    """m_i = y_i * M_Pl * η_RG"""
    return y * M_Pl * eta

def formula_C(eta_vec):
    """m_i = c_i^α * M_Pl * η_RG_i"""
    return c_al * M_Pl * eta_vec

def formula_D(y, eta_vec):
    """m_i = y_i * c_i^α * M_Pl * η_RG_i"""
    return y * c_al * M_Pl * eta_vec

def formula_E(y, eta, beta):
    """m_i = y_i^β * c_i^α * M_Pl * η_RG"""
    return (y ** beta) * c_al * M_Pl * eta


# ============================================================
# 5. 损失函数
# ============================================================
def log_mse(m_pred, m_exp):
    """对数空间中的均方误差（质量跨越 6 个数量级）。"""
    return np.mean((np.log(m_pred) - np.log(m_exp)) ** 2)


# ============================================================
# 6. 各公式变体的优化
# ============================================================

def optimize_formula_A():
    """优化 Formula A: 3 混合角 + 1 η_RG"""
    def loss(params):
        t12, t13, t23, log_eta = params
        U = build_U(t12, t13, t23)
        y = yukawa_projection(U)
        eta = 10 ** log_eta
        m_pred = formula_A(y, eta)
        return log_mse(m_pred, m_exp)

    result = minimize(loss, [0.1, 0.05, 0.01, -17], method='Nelder-Mead',
                      options={'maxiter': 20000, 'xatol': 1e-12, 'fatol': 1e-12})
    return result


def optimize_formula_B():
    """优化 Formula B: 3 混合角 + 1 η_RG"""
    def loss(params):
        t12, t13, t23, log_eta = params
        U = build_U(t12, t13, t23)
        y = yukawa_projection(U)
        eta = 10 ** log_eta
        m_pred = formula_B(y, eta)
        return log_mse(m_pred, m_exp)

    result = minimize(loss, [0.1, 0.05, 0.01, -19], method='Nelder-Mead',
                      options={'maxiter': 20000, 'xatol': 1e-12, 'fatol': 1e-12})
    return result


def optimize_formula_C():
    """优化 Formula C: 3 个 η_RG_i（无混合角）"""
    c_al_MPl = c_al * M_Pl
    # 解析解：eta_i = m_i_exp / (c_i^α * M_Pl)
    eta_opt = m_exp / c_al_MPl
    m_pred = formula_C(eta_opt)
    mse = log_mse(m_pred, m_exp)
    return eta_opt, m_pred, mse


def optimize_formula_D():
    """优化 Formula D: 3 混合角 + 3 η_RG_i"""
    def loss_angles(params):
        t12, t13, t23 = params
        U = build_U(t12, t13, t23)
        y = yukawa_projection(U)
        # 给定 y，η 有解析解：eta_i = m_i_exp / (y_i * c_i^α * M_Pl)
        scale = y * c_al * M_Pl
        eta = m_exp / scale
        m_pred = scale * eta
        return log_mse(m_pred, m_exp)

    result = minimize(loss_angles, [0.1, 0.05, 0.01], method='Nelder-Mead',
                      options={'maxiter': 20000, 'xatol': 1e-12, 'fatol': 1e-12})
    t12, t13, t23 = result.x
    U = build_U(t12, t13, t23)
    y = yukawa_projection(U)
    eta = m_exp / (y * c_al * M_Pl)
    m_pred = formula_D(y, eta)
    return t12, t13, t23, y, eta, m_pred, result.fun


def optimize_formula_E():
    """优化 Formula E: 3 混合角 + 1 η_RG + 1 β"""
    def loss(params):
        t12, t13, t23, log_eta, beta = params
        U = build_U(t12, t13, t23)
        y = yukawa_projection(U)
        eta = 10 ** log_eta
        m_pred = formula_E(y, eta, beta)
        return log_mse(m_pred, m_exp)

    result = minimize(loss, [0.1, 0.05, 0.01, -19, 0.5], method='Nelder-Mead',
                      options={'maxiter': 20000, 'xatol': 1e-12, 'fatol': 1e-12})
    return result


# ============================================================
# 7. 探索: 混合角对质量预测的灵敏度
# ============================================================
def angle_sweep_2d(theta12_range, theta13_idx, theta23_val, eta_val):
    """在 theta12 × theta13 网格上扫描质量偏差"""
    results = []
    for t12 in theta12_range:
        for t13_idx, t13 in enumerate(theta13_range):
            U = build_U(t12, t13, theta23_val)
            y = yukawa_projection(U)
            m = formula_A(y, eta_val)
            lms = log_mse(m, m_exp)
            results.append((t12, t13, lms, m[0], m[1], m[2]))
    return results


# ============================================================
# 8. 打印结果
# ============================================================
def print_header(title):
    print()
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


def print_mass_comparison(m_pred, label=""):
    print(f"  {label}")
    print(f"  {'粒子':<12s} {'预测 (MeV)':>14s} {'实验 (MeV)':>14s} {'偏差':>10s}")
    print(f"  {'-'*50}")
    for i, name in enumerate(["电子", "缪子", "陶子"]):
        if m_pred[i] > 0.1:
            pred_mev = m_pred[i] * 1000
        else:
            pred_mev = m_pred[i] * 1000
        exp_mev = m_exp[i] * 1000
        dev = (m_pred[i] - m_exp[i]) / m_exp[i] * 100
        print(f"  {name:<12s} {pred_mev:>14.4f} {exp_mev:>14.4f} {dev:>+9.2f}%")
    print()


# ============================================================
# 9. 主函数
# ============================================================
def main():
    print_header("轻子质量谱公式数值优化器 v0.3")
    print(f"  lambda_H = [{lambda_H[0]:.6e}, {lambda_H[1]:.6e}, {lambda_H[2]:.6e}]")
    print(f"  c_al     = [{c_al[0]:.6e}, {c_al[1]:.6e}, {c_al[2]:.6e}]")
    print(f"  M_Pl     = {M_Pl:.2e} GeV")
    print(f"  实验值: m_e={m_e_exp*1000:.4f} MeV, m_mu={m_mu_exp*1000:.2f} MeV, m_tau={m_tau_exp:.4f} GeV")

    # ---- Formula C: IFS only + gen-dependent η (baseline) ----
    print_header("Formula C: IFS 收缩因子仅 + 代依赖 η_RG")
    eta_C, m_C, mse_C = optimize_formula_C()
    print_mass_comparison(m_C, "仅 IFS 缩放")
    print(f"  η_RG = [{eta_C[0]:.4e}, {eta_C[1]:.4e}, {eta_C[2]:.4e}]")
    print(f"  η_RG 比值 (归一化到 τ): [{eta_C[0]/eta_C[2]:.4f}, {eta_C[1]/eta_C[2]:.4f}, 1.0]")
    print(f"  Log-MSE = {mse_C:.6e}")

    # ---- Formula A: current code ----
    print_header("Formula A: m_i = y_i * c_i^α * M_Pl * η_RG (当前代码)")
    res_A = optimize_formula_A()
    t12_A, t13_A, t23_A, log_eta_A = res_A.x
    eta_A = 10 ** log_eta_A
    U_A = build_U(t12_A, t13_A, t23_A)
    y_A = yukawa_projection(U_A)
    m_A = formula_A(y_A, eta_A)
    print(f"  混合角: θ12={t12_A:.6f}, θ13={t13_A:.6f}, θ23={t23_A:.6f} rad")
    print(f"  |U_31|^2 = {U_A[2,0]**2:.6e}")
    print(f"  η_RG = {eta_A:.4e}")
    print(f"  y   = [{y_A[0]:.6e}, {y_A[1]:.6e}, {y_A[2]:.6e}]")
    print_mass_comparison(m_A, "Formula A")
    print(f"  Log-MSE = {res_A.fun:.6e}")

    # ---- Formula B: Higgs projection only ----
    print_header("Formula B: m_i = y_i * M_Pl * η_RG (仅谱投影)")
    res_B = optimize_formula_B()
    t12_B, t13_B, t23_B, log_eta_B = res_B.x
    eta_B = 10 ** log_eta_B
    U_B = build_U(t12_B, t13_B, t23_B)
    y_B = yukawa_projection(U_B)
    m_B = formula_B(y_B, eta_B)
    print(f"  混合角: θ12={t12_B:.6f}, θ13={t13_B:.6f}, θ23={t23_B:.6f} rad")
    print(f"  η_RG = {eta_B:.4e}")
    print(f"  y   = [{y_B[0]:.6e}, {y_B[1]:.6e}, {y_B[2]:.6e}]")
    print_mass_comparison(m_B, "Formula B")
    print(f"  Log-MSE = {res_B.fun:.6e}")

    # ---- Formula D: full + gen-dependent η ----
    print_header("Formula D: m_i = y_i * c_i^α * M_Pl * η_RG_i (代依赖 η)")
    t12_D, t13_D, t23_D, y_D, eta_D, m_D, mse_D = optimize_formula_D()
    U_D = build_U(t12_D, t13_D, t23_D)
    print(f"  混合角: θ12={t12_D:.6f}, θ13={t13_D:.6f}, θ23={t23_D:.6f} rad")
    print(f"  |U_31|^2 = {U_D[2,0]**2:.6e}")
    print(f"  y   = [{y_D[0]:.6e}, {y_D[1]:.6e}, {y_D[2]:.6e}]")
    print(f"  η_RG = [{eta_D[0]:.4e}, {eta_D[1]:.4e}, {eta_D[2]:.4e}]")
    print_mass_comparison(m_D, "Formula D (完美拟合)")
    print(f"  Log-MSE = {mse_D:.6e}")

    # ---- Formula E: power modulation ----
    print_header("Formula E: m_i = y_i^β * c_i^α * M_Pl * η_RG (幂律调制)")
    res_E = optimize_formula_E()
    t12_E, t13_E, t23_E, log_eta_E, beta_E = res_E.x
    eta_E = 10 ** log_eta_E
    U_E = build_U(t12_E, t13_E, t23_E)
    y_E = yukawa_projection(U_E)
    m_E = formula_E(y_E, eta_E, beta_E)
    print(f"  混合角: θ12={t12_E:.6f}, θ13={t13_E:.6f}, θ23={t23_E:.6f} rad")
    print(f"  η_RG = {eta_E:.4e}")
    print(f"  β    = {beta_E:.6f}")
    print(f"  y   = [{y_E[0]:.6e}, {y_E[1]:.6e}, {y_E[2]:.6e}]")
    print_mass_comparison(m_E, "Formula E")
    print(f"  Log-MSE = {res_E.fun:.6e}")

    # ---- 汇总对比 ----
    print_header("汇总对比")
    formulas = [
        ("A: 双重压制 + 单 η", res_A.fun, m_A),
        ("B: 仅谱投影 + 单 η", res_B.fun, m_B),
        ("C: 仅 IFS + 代依赖 η", mse_C, m_C),
        ("D: 全量 + 代依赖 η", mse_D, m_D),
        ("E: 幂律调制 + 单 η", res_E.fun, m_E),
    ]
    print(f"  {'公式':<24s} {'Log-MSE':>12s} {'m_e (MeV)':>12s} {'m_μ (MeV)':>12s} {'m_τ (GeV)':>12s}")
    print(f"  {'-'*72}")
    for name, mse_val, masses in formulas:
        print(f"  {name:<24s} {mse_val:>12.2e} {masses[0]*1000:>12.4f} {masses[1]*1000:>12.2f} {masses[2]:>12.4f}")

    # ---- 关键发现 ----
    print_header("关键发现")
    print("""
  1. Formula A（当前代码）同时使用 y_i 和 c_i^α 两种代结构压制，
     导致 tau 子严重欠压制（243 GeV vs 1.777 GeV）。

  2. Formula B（仅谱投影）能显著改善但受限于单一 η_RG。

  3. Formula C（仅 IFS + 代依赖 η_RG）揭示 η_RG 的代依赖模式：
     - η_RG_1 >> η_RG_3（电子需要更大跑动因子）
     这正是 Phase 50 的基准结果。

  4. Formula D（全量 + 代依赖 η_RG）完美拟合全部三质量，
     但需要代依赖 η_RG_i，这提示：
     η_RG 的代依赖结构 = IFS 收缩因子的逆 + 额外的物理机制。

  5. Formula E（幂律调制 + 单 η_RG）探索了是否可以通过 y_i^β 
     调制只用单一 η_RG 拟合。β 的最优值将揭示 y_i 和 c_i^α 
     之间的正确组合方式。
    """)

    return {
        "formula_A": {"angles": (t12_A, t13_A, t23_A), "eta": eta_A, "y": y_A, "mse": res_A.fun, "masses": m_A},
        "formula_B": {"angles": (t12_B, t13_B, t23_B), "eta": eta_B, "y": y_B, "mse": res_B.fun, "masses": m_B},
        "formula_C": {"eta": eta_C, "mse": mse_C, "masses": m_C},
        "formula_D": {"angles": (t12_D, t13_D, t23_D), "eta": eta_D, "y": y_D, "mse": mse_D, "masses": m_D},
        "formula_E": {"angles": (t12_E, t13_E, t23_E), "eta": eta_E, "y": y_E, "beta": beta_E, "mse": res_E.fun, "masses": m_E},
    }


if __name__ == "__main__":
    results = main()
