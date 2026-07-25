#!/usr/bin/env python3
"""
上型夸克深度优化 v0.2

诊断并尝试解决 u/c/t 夸克的质量拟合问题。
核心问题：α_u ≈ α_v → U 矩阵几乎单位阵 → y_u ≈ λ_H^(1) 已超过 m_u 需求

策略：
  1. 差分演化全局优化（不依赖初始猜测）
  2. 包含 CP 相位 δ 作为第4角自由度的5参数优化
  3. α_u 扫描：验证 α_u 微小调整能否解决比率问题
  4. Formula B 推广：测试 m_i = (y_i)^β * M_Pl * η_RG
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. 谱常数
# ============================================================
c1, c2, c3 = 0.003314, 0.066554, 0.999761
c = np.array([c1, c2, c3])

alpha_v = 1.883   # Higgs
alpha_u = 1.945   # 上型夸克（基线）
alpha_d = 1.229   # 下型夸克（对比）

M_Pl = 1.22e19

# 实验质量 (GeV)
m_u_exp, m_c_exp, m_t_exp = 2.2e-3, 1.27, 172.7
m_up_exp = np.array([m_u_exp, m_c_exp, m_t_exp])

# 轻子参考
eta_RG_l_ref = 1.5436e-19


def compute_lambda_H(alpha=alpha_v):
    """Higgs 谱权重 λ_H^{(k)} = c_k^α / Σ c_k^α"""
    c_a = c ** alpha
    return c_a / np.sum(c_a)


lambda_H_base = compute_lambda_H()
print(f"λ_H (α_v={alpha_v}) = [{lambda_H_base[0]:.6e}, {lambda_H_base[1]:.6e}, {lambda_H_base[2]:.6f}]")


# ============================================================
# 2. U 矩阵（含 δ 相位）
# ============================================================
def build_U_cp(t12, t13, t23, delta):
    """3x3 幺正矩阵，含 CP 相位 δ。标准参数化。"""
    s12, c12 = np.sin(t12), np.cos(t12)
    s13, c13 = np.sin(t13), np.cos(t13)
    s23, c23 = np.sin(t23), np.cos(t23)
    cp = np.exp(1j * delta)

    return np.array([
        [c12*c13,              s12*c13,              s13*np.conj(cp)],
        [-s12*c23 - c12*s23*s13*cp, c12*c23 - s12*s23*s13*cp, s23*c13],
        [s12*s23 - c12*c23*s13*cp, -c12*s23 - s12*c23*s13*cp, c23*c13]
    ])


def yukawa_projection(U):
    """y_i = sum_k |U_{ki}|^2 * lambda_H^{(k)}"""
    U_sq = np.abs(U) ** 2
    return U_sq.T @ lambda_H_base


def formula_B(y, eta):
    return y * M_Pl * eta


def log_mse(m_pred, m_exp):
    return np.mean((np.log(m_pred) - np.log(m_exp)) ** 2)


# ============================================================
# 3. 策略1: 差分演化全局优化（4参数：θ12,θ13,θ23,log_η）
# ============================================================
print(f"\n{'='*70}")
print(f"  策略1: 差分演化全局优化 (4参数)")
print(f"{'='*70}")

bounds_4 = [(-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), (-20, -15)]

def loss_4(params):
    t12, t13, t23, log_eta = params
    U = build_U_cp(t12, t13, t23, 0.0)
    y = yukawa_projection(U)
    eta = 10 ** log_eta
    m_pred = formula_B(y, eta)
    return log_mse(m_pred, m_up_exp)

result_de = differential_evolution(loss_4, bounds_4, seed=42, maxiter=5000,
                                   tol=1e-12, popsize=30, mutation=(0.5, 1.5),
                                   recombination=0.9)
t12, t13, t23, log_eta = result_de.x
eta = 10 ** log_eta
U = build_U_cp(t12, t13, t23, 0.0)
y = yukawa_projection(U)
m_pred = formula_B(y, eta)

print(f"  最佳 MSE = {result_de.fun:.6e}")
print(f"  θ12 = {t12:+.6f} rad ({np.degrees(t12):+.2f}°)")
print(f"  θ13 = {t13:+.6f} rad ({np.degrees(t13):+.2f}°)")
print(f"  θ23 = {t23:+.6f} rad ({np.degrees(t23):+.2f}°)")
print(f"  log10(η_RG) = {log_eta:.4f}")
print(f"  M_Pl*η_RG = {M_Pl*eta:.4f} GeV")
for i, nm in enumerate(['u','c','t']):
    dev = (m_pred[i] - m_up_exp[i]) / m_up_exp[i] * 100
    print(f"  {nm}: pred={m_pred[i]*1000:.4f} MeV, exp={m_up_exp[i]*1000:.1f} MeV, dev={dev:+.2f}%")


# ============================================================
# 4. 策略2: 含 CP 相位 δ 的优化（5参数）
# ============================================================
print(f"\n{'='*70}")
print(f"  策略2: 含 δ 相位的5参数优化")
print(f"{'='*70}")

bounds_5 = [(-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), (-20, -15), (-np.pi, np.pi)]

def loss_5(params):
    t12, t13, t23, log_eta, delta = params
    U = build_U_cp(t12, t13, t23, delta)
    y = yukawa_projection(U)
    eta = 10 ** log_eta
    m_pred = formula_B(y, eta)
    return log_mse(m_pred, m_up_exp)

# 先试 Nelder-Mead 从多个初始值
best_loss = float('inf')
best_params = None
for _ in range(20):
    init = [np.random.uniform(-0.3, 0.3) for _ in range(3)] + \
           [np.random.uniform(-20, -15)] + [np.random.uniform(-np.pi, np.pi)]
    res = minimize(loss_5, init, method='Nelder-Mead',
                   options={'maxiter': 20000, 'xatol': 1e-12, 'fatol': 1e-12})
    if res.fun < best_loss:
        best_loss = res.fun
        best_params = res.x

print(f"  Nelder-Mead 最佳: MSE = {best_loss:.6e}")
t12, t13, t23, log_eta, delta = best_params
eta = 10 ** log_eta
U = build_U_cp(t12, t13, t23, delta)
y = yukawa_projection(U)
m_pred = formula_B(y, eta)
print(f"  θ12 = {t12:+.6f} rad, θ13 = {t13:+.6f} rad, θ23 = {t23:+.6f} rad")
print(f"  δ = {delta:+.6f} rad ({np.degrees(delta):+.2f}°)")
print(f"  M_Pl*η_RG = {M_Pl*eta:.4f} GeV")
for i, nm in enumerate(['u','c','t']):
    dev = (m_pred[i] - m_up_exp[i]) / m_up_exp[i] * 100
    print(f"  {nm}: pred={m_pred[i]*1000:.4f} MeV, exp={m_up_exp[i]*1000:.1f} MeV, dev={dev:+.2f}%")

# 再用差分演化
print(f"\n  差分演化5参数:")
res_de5 = differential_evolution(loss_5, bounds_5, seed=42, maxiter=5000,
                                  tol=1e-12, popsize=40, mutation=(0.5, 1.5),
                                  recombination=0.9)
t12, t13, t23, log_eta, delta = res_de5.x
eta = 10 ** log_eta
U = build_U_cp(t12, t13, t23, delta)
y = yukawa_projection(U)
m_pred = formula_B(y, eta)
print(f"  MSE = {res_de5.fun:.6e}")
print(f"  θ12 = {t12:+.6f} rad, θ13 = {t13:+.6f} rad, θ23 = {t23:+.6f} rad")
print(f"  δ = {delta:+.6f} rad")
print(f"  M_Pl*η_RG = {M_Pl*eta:.4f} GeV")
for i, nm in enumerate(['u','c','t']):
    dev = (m_pred[i] - m_up_exp[i]) / m_up_exp[i] * 100
    print(f"  {nm}: pred={m_pred[i]*1000:.4f} MeV, exp={m_up_exp[i]*1000:.1f} MeV, dev={dev:+.2f}%")


# ============================================================
# 5. 策略3: α_u 扫描
# ============================================================
print(f"\n{'='*70}")
print(f"  策略3: α_u 扫描（允许 α_u 偏离 1.945）")
print(f"{'='*70}")

# 对每个 α_u，用差分演化找最佳 4参数匹配
alpha_range = np.linspace(1.8, 2.3, 51)
best_alpha = None
best_alpha_loss = float('inf')
alpha_results = []

for au in alpha_range:
    lambda_H_au = c ** au / np.sum(c ** au)
    
    def loss_for_alpha(params):
        t12, t13, t23, log_eta = params
        U = build_U_cp(t12, t13, t23, 0.0)
        U_sq = np.abs(U) ** 2
        y_local = U_sq.T @ lambda_H_au
        eta = 10 ** log_eta
        m_pred = formula_B(y_local, eta)
        return log_mse(m_pred, m_up_exp)
    
    res = differential_evolution(loss_for_alpha, bounds_4, seed=42,
                                  maxiter=2000, tol=1e-12, popsize=20)
    alpha_results.append((au, res.fun, res.x))
    if res.fun < best_alpha_loss:
        best_alpha_loss = res.fun
        best_alpha = au

print(f"\n  最佳 α_u = {best_alpha:.4f}, 最小 MSE = {best_alpha_loss:.6e}")

for au, loss, params in alpha_results:
    if loss < 0.01 or abs(au - best_alpha) < 0.01:
        t12, t13, t23, log_eta = params
        eta = 10 ** log_eta
        U = build_U_cp(t12, t13, t23, 0.0)
        U_sq = np.abs(U) ** 2
        lambda_H_au = c ** au / np.sum(c ** au)
        y_local = U_sq.T @ lambda_H_au
        m_pred = formula_B(y_local, eta)
        devs = [f"{nm}:{(mp-me)/me*100:+.1f}%" for nm,mp,me in 
                [('u',m_pred[0],m_u_exp),('c',m_pred[1],m_c_exp),('t',m_pred[2],m_t_exp)]]
        print(f"  α_u={au:.4f}: MSE={loss:.6e}, η_scale={M_Pl*eta:.2f} GeV, {' '.join(devs)}")

# 打印扫描概览
print(f"\n  α_u 扫描 MSE 概览:")
for au, loss, _ in alpha_results:
    marker = " <--" if abs(au - best_alpha) < 0.001 else ""
    if loss < 0.1 or (au >= best_alpha - 0.05 and au <= best_alpha + 0.05):
        print(f"    α_u={au:.3f}: MSE={loss:.4e}{marker}")


# ============================================================
# 6. 策略4: Formula B^β — 推广质量公式
# ============================================================
print(f"\n{'='*70}")
print(f"  策略4: 谱幂推广 m_i = (y_i)^β * M_Pl * η_RG")
print(f"{'='*70}")

def formula_B_beta(y, eta, beta):
    return (y ** beta) * M_Pl * eta

bounds_5b = [(-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), (-20, -15), (0.5, 2.0)]

def loss_5b(params):
    t12, t13, t23, log_eta, beta = params
    U = build_U_cp(t12, t13, t23, 0.0)
    y = yukawa_projection(U)
    eta = 10 ** log_eta
    m_pred = formula_B_beta(y, eta, beta)
    return log_mse(m_pred, m_up_exp)

res_de_beta = differential_evolution(loss_5b, bounds_5b, seed=42, maxiter=5000,
                                      tol=1e-12, popsize=40, mutation=(0.5, 1.5),
                                      recombination=0.9)
t12, t13, t23, log_eta, beta = res_de_beta.x
eta = 10 ** log_eta
U = build_U_cp(t12, t13, t23, 0.0)
y = yukawa_projection(U)
m_pred = formula_B_beta(y, eta, beta)

print(f"  最佳 β = {beta:.6f}")
print(f"  MSE = {res_de_beta.fun:.6e}")
print(f"  θ12 = {t12:+.6f} rad, θ13 = {t13:+.6f} rad, θ23 = {t23:+.6f} rad")
print(f"  M_Pl*η_RG = {M_Pl*eta:.4f} GeV")
for i, nm in enumerate(['u','c','t']):
    dev = (m_pred[i] - m_up_exp[i]) / m_up_exp[i] * 100
    print(f"  {nm}: pred={m_pred[i]*1000:.4f} MeV, exp={m_up_exp[i]*1000:.1f} MeV, dev={dev:+.2f}%")
print(f"  y_i = [{y[0]:.6e}, {y[1]:.6e}, {y[2]:.6f}]")
print(f"  y_i^β = [{(y[0]**beta):.6e}, {(y[1]**beta):.6e}, {(y[2]**beta):.6f}]")


# ============================================================
# 7. 汇总对比
# ============================================================
print(f"\n{'='*70}")
print(f"  汇总对比")
print(f"{'='*70}")
print(f"\n  {'策略':<30s} {'u偏差':>10s} {'c偏差':>10s} {'t偏差':>10s} {'MSE':>12s}")
print(f"  {'-'*72}")
print(f"  {'v0.1 原结果':<30s} {'+30.08%':>10s} {'-0.25%':>10s} {'-22.94%':>10s} {'4.57e-02':>12s}")
print(f"  {'DE全局(4参数)':<30s} {'':>10s} {'':>10s} {'':>10s} {'':>12s}")
print(f"  {'δ相位(5参数)':<30s} {'':>10s} {'':>10s} {'':>10s} {'':>12s}")
print(f"  {'α_u扫描最佳':<30s} {'':>10s} {'':>10s} {'':>10s} {'':>12s}")
print(f"  {'谱幂β推广':<30s} {'':>10s} {'':>10s} {'':>10s} {'':>12s}")
