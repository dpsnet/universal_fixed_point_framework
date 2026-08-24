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
验证 Leaver 1991 年论文中的 Schwarzschild 连分数系数。

根据 Leaver (1991) "Remarks on the continued-fraction method..."
在单位制 c=G=2M=1 下：
  αₙ = n² + (2ρ+2)n + 2ρ+1
  βₙ = -[2n² + (8ρ+2)n + 8ρ² + 4ρ + l(l+1) - ε]
  γₙ = n² + 4ρ n + 4ρ² - ε - 1

其中 ρ = -iω，ε = 3（引力扰动）。
"""

import numpy as np
import cmath


def leaver_1991_schwarzschild(omega, l, s=-2, max_iter=300):
    """使用 Leaver 1991 公式计算 Schwarzschild 连分数残差。
    
    单位制: G=c=M=1
    """
    # Leaver 1991 使用单位制 c=G=2M=1, 我们需要转换
    # 在 c=G=2M=1 中, ω_Leaver = ω_std * 2M
    # ρ = -i * ω_Leaver
    omega_leaver = 2.0 * omega  # 转换到 2M=1 单位制
    rho = -1j * omega_leaver
    
    epsilon = 3.0  # 引力扰动
    
    def alpha_n(n):
        return n**2 + (2.0 * rho + 2.0) * n + 2.0 * rho + 1.0
    
    def beta_n(n):
        return -(2.0 * n**2 + (8.0 * rho + 2.0) * n + 8.0 * rho**2 + 4.0 * rho + l * (l + 1.0) - epsilon)
    
    def gamma_n(n):
        return n**2 + 4.0 * rho * n + 4.0 * rho**2 - epsilon - 1.0
    
    # 连分数形式: F(ρ) = -γ₁/(β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))
    # 特征方程: β₀/α₀ + F(ρ) = 0
    # 即: β₀ + α₀ * F(ρ) = 0
    
    cf = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        # cf_n = αₙ * γₙ₊₁ / (βₙ - cfₙ₊₁)
        denom = beta_n(n) - cf
        if abs(denom) < 1e-30:
            denom = complex(1e-30, 0.0)
        cf = alpha_n(n) * gamma_n(n + 1) / denom
    
    # F(ρ) = -γ₁ / (β₁ - α₁γ₂/(β₂ - ...))
    # 但我们的 cf 是 α₁γ₂/(β₁ - ...) 的形式
    # 让我们重新考虑...
    
    # 实际上, 从递推关系 αₙ aₙ₊₁ + βₙ aₙ + γₙ aₙ₋₁ = 0
    # 得: aₙ₊₁/aₙ = -(βₙ + γₙ aₙ₋₁/aₙ) / αₙ
    # 定义 rₙ = aₙ/aₙ₋₁, 则 rₙ₊₁ = -γₙ / (βₙ + αₙ rₙ)
    # 连分数: r₁ = -γ₁/(β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))
    
    # 从 n=max_iter 开始向下迭代
    # 对于大 n, rₙ ≈ -γₙ/βₙ 或 -βₙ₋₁/αₙ₋₁ (minimal solution)
    
    # 用另一种方式计算: 从大 n 开始, 计算 R_n = a_{n+1}/a_n
    # 对于 minimal solution, R_n ~ γ_n/β_n 对于大 n?
    
    # 让我们使用 Leaver 论文中的形式:
    # F(ρ) = -γ₁ / (β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))
    
    # 从右向左计算: 定义 f_n = α_n γ_{n+1} / (β_n - f_{n+1})
    # 则 F(ρ) = -γ₁ / (β₁ - f₁) ? 不对
    
    # 让我们用标准的三-term recurrence 连分数形式
    # 比值 r_n = a_n / a_{n-1} 满足: α_{n-1} r_n + β_{n-1} + γ_{n-1}/r_{n-1} = 0
    # 即: r_n = -γ_{n-1} / (α_{n-1} r_{n-1} + β_{n-1})
    
    # 从 n=1 开始: α₀ a₁ + β₀ a₀ = 0 => a₁/a₀ = -β₀/α₀
    # 对于 n>=1: αₙ aₙ₊₁ + βₙ aₙ + γₙ aₙ₋₁ = 0
    
    # QNM 条件: 级数在无穷远收敛 (minimal solution)
    # 即: lim_{n->∞} a_{n+1}/a_n = 0 ? 不, 是级数收敛
    
    # Leaver 的方法: 连分数 F(ρ) = a₁/a₀ (对于 QNM 频率)
    # 且 F(ρ) = -γ₁/(β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))
    
    # 特征方程: β₀/α₀ + F(ρ) = 0
    # 即 residual = β₀ + α₀ * F(ρ) = 0
    
    # 让我们用反向迭代计算 F(ρ)
    # F(ρ) = -γ₁ / (β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))
    
    # 计算: f_n = α_n γ_{n+1} / (β_n - f_{n+1})
    # 从 N 到 1: f_N ≈ 0 (对于大 N, 近似)
    # 然后 F(ρ) = -γ₁ / (β₁ - f₁) ? 不对
    
    # 等等, 让我们重新推导:
    # 连分数形式: α₁γ₂ / (β₁ - α₂γ₃/(β₂ - ...))
    # 这是标准的连分数形式
    
    # 实际上，更简单的方法是使用最小解的 Pincherle 定理
    # 但让我们先用一个简单的验证方法
    
    # 让我们使用另一种迭代: 
    # 从 n=0 开始, 用 α₀ a₁ + β₀ a₀ = 0 (取 a₀=1, a₁ = -β₀/α₀)
    # 然后向前递推: a_{n+1} = -(βₙ aₙ + γₙ a_{n-1}) / αₙ
    # 如果级数收敛, 则 a_n 应该增长不能太快
    
    # 但 QNM 条件是用连分数表示的:
    # 当频率为 QNM 频率时, 两个连分数相等
    # (一个从 n=0 向右, 一个从 n=∞ 向左)
    
    # 让我们尝试 Leaver 1985 论文中的形式
    # 残差 = β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...))
    
    # 计算连分数部分: cf = α₁γ₂/(β₁ - α₂γ₃/(β₂ - ...))
    # 从 n=N 到 1:
    cf_val = 0.0j
    for n in range(max_iter, 0, -1):
        numer = alpha_n(n) * gamma_n(n + 1)
        denom = beta_n(n) - cf_val
        if abs(denom) < 1e-30:
            denom = 1e-30
        cf_val = numer / denom
    
    # 残差 = β₀ - α₀γ₁ / (β₁ - α₁γ₂/(...)) ?
    # 不对, 应该是 β₀ - α₀γ₁/(β₁ - cf_1), 而 cf_1 = α₁γ₂/(β₂ - ...)
    
    # 让我们重新考虑: 上面的循环计算的是
    # 当 n=N 时: cf = α_N γ_{N+1} / β_N
    # 当 n=N-1 时: cf = α_{N-1} γ_N / (β_{N-1} - α_N γ_{N+1}/β_N)
    # 所以最终 cf (n=1 时) = α₁ γ₂ / (β₁ - α₂ γ₃ / (β₂ - ...))
    
    # 那么完整的连分数应该是: α₀γ₁ / (β₀ - α₁γ₂/(β₁ - ...)) = ?
    
    # 等等, 让我们看标准的连分数量子化条件
    # 对于递推关系 αₙ a_{n+1} + βₙ aₙ + γₙ a_{n-1} = 0
    # 最小解存在的条件是连分数收敛
    # 量子化条件通常写为:
    # β₀ = α₀γ₁ / (β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))
    
    # 所以残差 = β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...))
    
    # 我们上面计算的 cf_val = α₁γ₂/(β₁ - α₂γ₃/(β₂ - ...))
    # 所以完整连分数 = α₀γ₁ / (β₁ - cf_val) ? 不对
    
    # 让我们更仔细地推导:
    # 定义 f_n = α_n γ_{n+1} / (β_n - f_{n+1})
    # 则 f_0 = α₀γ₁ / (β₀ - f₁)
    # f_1 = α₁γ₂ / (β₁ - f₂)
    # ...
    
    # 量子化条件通常是关于比值 r_n = a_n / a_{n-1} 的
    # 从递推: α_{n-1} a_n + β_{n-1} a_{n-1} + γ_{n-1} a_{n-2} = 0
    # α_{n-1} (a_n/a_{n-1}) + β_{n-1} + γ_{n-1} (a_{n-2}/a_{n-1}) = 0
    # α_{n-1} r_n + β_{n-1} + γ_{n-1}/r_{n-1} = 0
    # r_n = -γ_{n-1} / (α_{n-1} r_{n-1} + β_{n-1})
    
    # 对于 n=0: α₀ a₁ + β₀ a₀ = 0 => r₁ = a₁/a₀ = -β₀/α₀
    
    # 最小解的条件: 当 n→∞ 时, r_n 趋向于对应最小解的那个根
    # (递推有两个线性独立解, 一个增长, 一个衰减; 最小解是衰减的那个)
    
    # Leaver 的方法: 从大 n 开始, 用连分数计算 r_n
    # r_n = -γ_{n-1} / (β_{n-1} - α_{n-1} α_{n-2} ... )
    # 不对, 应该是 r_n = -γ_{n-1} / (β_{n-1} + α_{n-1} r_{n-1})
    
    # 这是一个向右递推的式子, 但我们需要的是向左的连分数
    # (从大 n 开始)
    
    # 让我们换一种方式: 从递推关系解出 a_{n-1}/a_n
    # αₙ a_{n+1} + βₙ aₙ + γₙ a_{n-1} = 0
    # γₙ (a_{n-1}/a_n) + βₙ + αₙ (a_{n+1}/a_n) = 0
    # 设 s_n = a_n / a_{n+1}, 则:
    # γₙ s_n s_{n+1} + βₙ s_{n+1} + αₙ = 0
    # s_{n+1} = -αₙ / (βₙ + γₙ s_n)
    
    # 对于大 n, 最小解的 s_n 行为?
    # αₙ ~ n², βₙ ~ -2n², γₙ ~ n²
    # 所以 s_{n+1} ~ -n² / (-2n² + n² s_n) = -1 / (-2 + s_n)
    # 不动点: s = -1/(-2+s) => s(s-2) = -1 => s²-2s+1=0 => s=1 (二重根)
    
    # 不管怎样, 让我们尝试用 Leaver 1991 论文中的特征方程形式
    # 论文中说: β₀(ρ)/α₀(ρ) + F(ρ) = 0
    # 其中 F(ρ) = -γ₁/(β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))
    
    # 计算 F(ρ):
    # 令 f_n = α_n γ_{n+1} / (β_n - f_{n+1})
    # 则 F = -γ₁ / (β₁ - f₁) ? 不对
    
    # 让我们直接看 F 的展开:
    # F = -γ₁ / [β₁ - α₁γ₂ / [β₂ - α₂γ₃ / [β₃ - ...]]]
    
    # 定义 g_n = α_n γ_{n+1} / (β_n - g_{n+1})
    # 那么 g_1 = α₁ γ₂ / (β₁ - g_2)
    # β₁ - g_1 = β₁ - α₁γ₂/(β₂ - ...)
    # 所以 F = -γ₁ / (β₁ - g_1)
    
    # 但从 n=N 向下迭代 g_n:
    # g_N ≈ α_N γ_{N+1} / β_N (假设 g_{N+1} ≈ 0)
    # 然后 g_{N-1} = α_{N-1} γ_N / (β_{N-1} - g_N)
    # ... 直到 g_1
    
    # 计算 g_n (从 n=N 到 1):
    g = 0.0j
    for n in range(max_iter, 0, -1):
        numer = alpha_n(n) * gamma_n(n + 1)
        denom = beta_n(n) - g
        if abs(denom) < 1e-30:
            denom = 1e-30
        g = numer / denom
    
    # 现在 g = g_1 = α₁γ₂/(β₁ - α₂γ₃/(β₂ - ...))
    
    # 计算 F = -γ₁ / (β₁ - g)
    F = -gamma_n(1) / (beta_n(1) - g)
    
    # 特征方程: β₀/α₀ + F = 0
    residual = beta_n(0) / alpha_n(0) + F
    
    return residual


def test_schwarzschild():
    M = 1.0
    l = 2
    s = -2
    
    # 参考值 (标准单位制 G=c=M=1)
    ref_omega = complex(0.373672, -0.088962)
    
    print("=" * 60)
    print("Leaver 1991 Schwarzschild 连分数验证")
    print("=" * 60)
    print(f"参考频率: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
    print(f"l = {l}, s = {s}")
    print()
    
    # 测试参考频率处的残差
    res = leaver_1991_schwarzschild(ref_omega, l, s)
    print(f"参考频率处的残差: {abs(res):.6e}")
    print(f"  (复数值: {res.real:.6e} {res.imag:.6e}i)")
    print()
    
    # 用 Newton 法找根
    print("用 Newton 法寻找根...")
    omega = complex(ref_omega)
    eps = 1e-7
    
    for i in range(20):
        f = leaver_1991_schwarzschild(omega, l, s)
        res = abs(f)
        print(f"  迭代 {i}: ω = {omega.real:.8f} {omega.imag:.8f}i, 残差 = {res:.2e}")
        
        if res < 1e-10:
            break
        
        f_re = leaver_1991_schwarzschild(omega + eps, l, s)
        f_im = leaver_1991_schwarzschild(omega + 1j * eps, l, s)
        df_dre = (f_re - f) / eps
        df_dim = (f_im - f) / eps
        
        jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
        rhs = -np.array([f.real, f.imag])
        
        try:
            delta = np.linalg.solve(jacobian, rhs)
            omega += complex(delta[0], delta[1])
        except np.linalg.LinAlgError:
            omega -= 0.01 * f
    
    print()
    print(f"最终: ω = {omega.real:.8f} {omega.imag:.8f}i")
    print(f"参考: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
    print(f"偏差: ΔRe = {abs(omega.real - ref_omega.real):.2e}, ΔIm = {abs(omega.imag - ref_omega.imag):.2e}")
    
    return omega


if __name__ == "__main__":
    test_schwarzschild()
