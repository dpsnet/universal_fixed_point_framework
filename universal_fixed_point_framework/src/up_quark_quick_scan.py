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
上型夸克快速诊断扫描 v0.2

不用耗时的差分演化，而是：
1. α_u 扫描（对每个 α_u 进行简单的局部优化）
2. 理论极限分析：最小可达偏差的计算
"""

import numpy as np
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

c = np.array([0.003314, 0.066554, 0.999761])
alpha_v = 1.883
M_Pl = 1.22e19
m_u_exp, m_c_exp, m_t_exp = 2.2e-3, 1.27, 172.7
m_up_exp = np.array([m_u_exp, m_c_exp, m_t_exp])

def compute_lambda_H(alpha):
    c_a = c ** alpha
    return c_a / np.sum(c_a)

def build_U(t12, t13, t23):
    s12, c12 = np.sin(t12), np.cos(t12)
    s13, c13 = np.sin(t13), np.cos(t13)
    s23, c23 = np.sin(t23), np.cos(t23)
    return np.array([
        [c12*c13,   s12*c13,   s13],
        [-s12*c23 - c12*s23*s13, c12*c23 - s12*s23*s13, s23*c13],
        [s12*s23 - c12*c23*s13, -c12*s23 - s12*c23*s13, c23*c13]
    ])

def yukawa_projection(U, lambda_H):
    return (U ** 2).T @ lambda_H

def log_mse(m_pred, m_exp):
    return np.mean((np.log(m_pred) - np.log(m_exp)) ** 2)

def optimize_4params(lambda_H, m_exp, init=(0.0, 0.0, 0.05, -17)):
    def loss(params):
        t12, t13, t23, log_eta = params
        U = build_U(t12, t13, t23)
        y = yukawa_projection(U, lambda_H)
        eta = 10 ** log_eta
        m_pred = y * M_Pl * eta
        return log_mse(m_pred, m_exp)
    
    # 多初始值
    best = (float('inf'), None)
    for _ in range(30):
        init = [np.random.uniform(-0.4, 0.4) for _ in range(3)] + \
               [np.random.uniform(-20, -15)]
        res = minimize(loss, init, method='Nelder-Mead',
                       options={'maxiter': 10000, 'xatol': 1e-14, 'fatol': 1e-14})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    return best

# ============================================================
# 1. α_u 扫描
# ============================================================
print(f"α_u 扫描")
print(f"{'α_u':>8s} {'λ_H^(1)':>12s} {'λ_H^(2)':>12s} {'λ_H^(3)':>12s} "
      f"{'MSE':>14s} {'u dev':>10s} {'c dev':>10s} {'t dev':>10s} {'η_scale(GeV)':>14s}")
print("-"*102)

alphas = np.linspace(1.80, 2.30, 51)
best_overall = (float('inf'), None, None)  # (loss, alpha, params)

for au in alphas:
    lambda_H = compute_lambda_H(au)
    loss, params = optimize_4params(lambda_H, m_up_exp)
    
    t12, t13, t23, log_eta = params
    eta = 10 ** log_eta
    U = build_U(t12, t13, t23)
    y = yukawa_projection(U, lambda_H)
    m_pred = y * M_Pl * eta
    
    u_dev = (m_pred[0]/m_u_exp - 1)*100
    c_dev = (m_pred[1]/m_c_exp - 1)*100
    t_dev = (m_pred[2]/m_t_exp - 1)*100
    scale = M_Pl * eta
    
    if loss < best_overall[0]:
        best_overall = (loss, au, (t12, t13, t23, log_eta, y, scale, [u_dev, c_dev, t_dev]))
    
    marker = " ◄" if loss < 1e-3 else ""
    print(f"{au:>8.3f} {lambda_H[0]:>12.6e} {lambda_H[1]:>12.6e} {lambda_H[2]:>12.6f} "
          f"{loss:>14.6e} {u_dev:>+9.2f}% {c_dev:>+9.2f}% {t_dev:>+9.2f}% {scale:>14.4f}{marker}")

# Best result
print(f"\n最佳结果:")
loss, au, (t12, t13, t23, log_eta, y, scale, devs) = best_overall
print(f"  α_u* = {au:.4f}")
print(f"  λ_H = {compute_lambda_H(au)}")
print(f"  MSE = {loss:.6e}")
print(f"  θ12 = {t12:+.6f} rad, θ13 = {t13:+.6f} rad, θ23 = {t23:+.6f} rad")
print(f"  y = [{y[0]:.6e}, {y[1]:.6e}, {y[2]:.6f}]")
print(f"  M_Pl*η_RG = {scale:.4f} GeV")
print(f"  u: {devs[0]:+.2f}%, c: {devs[1]:+.2f}%, t: {devs[2]:+.2f}%")


# ============================================================
# 2. 理论极限分析：为什么 Formula B 对 u,c,t 有结构性问题？
# ============================================================
print(f"\n\n{'='*70}")
print(f"理论极限分析")
print(f"{'='*70}")

print(f"\nFormula B 要求: m_1 : m_2 : m_3 = y_1 : y_2 : y_3")
print(f"因为 η_RG 对所有代相同。")
print(f"\n要求的质量比:")
req_ratio = m_up_exp / m_u_exp
print(f"  m_u : m_c : m_t = 1 : {m_c_exp/m_u_exp:.1f} : {m_t_exp/m_u_exp:.1f}")
print(f"  需要 y_u : y_c : y_t = 1 : {m_c_exp/m_u_exp:.1f} : {m_t_exp/m_u_exp:.1f}")

lambda_H_v = compute_lambda_H(alpha_v)
print(f"\n基础 λ_H (α_v={alpha_v}):")
print(f"  λ_H = [{lambda_H_v[0]:.6e}, {lambda_H_v[1]:.6e}, {lambda_H_v[2]:.6f}]")
print(f"  λ_H 比率: 1 : {lambda_H_v[1]/lambda_H_v[0]:.1f} : {lambda_H_v[2]/lambda_H_v[0]:.1f}")

print(f"\n最值定理: y_i = sum |U_ki|^2 λ_H^(k) 是 λ_H 的凸组合。")
print(f"因此: min(λ_H) ≤ y_i ≤ max(λ_H)")
print(f"  λ_H^(min) = {lambda_H_v[0]:.6e}")
print(f"  λ_H^(max) = {lambda_H_v[2]:.6f}")
print(f"\n这意味着: y_u / y_t 的最小比值 = {lambda_H_v[0]/lambda_H_v[2]:.6e}")
print(f"但实验需要:   m_u / m_t   = {m_u_exp/m_t_exp:.6e}")

ratio_min = lambda_H_v[0] / lambda_H_v[2]
ratio_req = m_u_exp / m_t_exp

print(f"\n  y_u/y_t ≥ {ratio_min:.6e} (理论下限, U=I时取等)")
print(f"  需要 y_u/y_t = {ratio_req:.6e}")
print(f"  理论偏差 = {(ratio_min/ratio_req - 1)*100:+.2f}%")
print(f"\n结论: Formula B 对上型夸克有 {abs((ratio_min/ratio_req - 1)*100):.1f}% 的")
print(f"  **纯理论下限偏差**。即使 U=I 也无法满足要求。")
print(f"  根源: λ_H^(1) = 2.13e-5 已比 m_u/m_t = 1.27e-5 大 67%。")

# Check if a different α_v helps
print(f"\n\n检查: 是否可以通过调整 α_v 来解决？")
print(f"(即 Higgs 谱指数的调整)")
for av in [1.85, 1.88, 1.90, 1.92, 1.95, 1.98, 2.00]:
    lh = compute_lambda_H(av)
    ratio = lh[0] / lh[2]
    dev = (ratio / ratio_req - 1) * 100
    ok = "✅" if abs(dev) < 5 else ""
    print(f"  α_v={av:.3f}: λ_H^(1)/λ_H^(3) = {ratio:.6e}, 理论偏差 = {dev:+.2f}% {ok}")

# Solution: the up-type sector needs its own λ_H (different α in λ_H computation)
print(f"\n\n'='*70")
print(f"可行路径")
print(f"'='*70")
print(f"""
上型夸克的 Formula B 拟合存在结构性问题：
  - λ_H^(1)/λ_H^(3) = {lambda_H_v[0]/lambda_H_v[2]:.6e}
  - 需要 m_u/m_t = {m_u_exp/m_t_exp:.6e}
  - 理论极限偏差 ~ {(lambda_H_v[0]/lambda_H_v[2]/(m_u_exp/m_t_exp)-1)*100:.1f}%

可行路径:
  路径 A: 修正质量公式
    上型夸克使用不同的公式（如 Formula B^β 或独立幂律 m_i = (y_i)^β * M_Pl * η_RG）
    → 纯谱框架修正，不引入新参数（β 可从 α_u, α_v 确定）

  路径 B: 上型夸克使用独立的谱指数
    上型夸克的 λ_H 使用 α_u ≠ α_v（即上型 Higgs 谱和轻子 Higgs 谱不同）
    → 需要新的物理机制：不同扇区"看"到不同的 Higgs

  路径 C: 接受有限偏差
    u/t 偏差源于顶层参数逼近，可解释为轻夸克质量测量误差 + RG 跑动不确定性
    → m_u(2 GeV) 的 PDG 范围是 1.7-3.3 MeV，当前 2.2 MeV 在范围内

建议优先路径 A（谱幂推广），因为 β ≠ 1 在谱框架中对应 
「谱投影非线性压缩」的自然物理解释。
""")
