"""
非局域相关时间（Non-local Correlation Time, NLCT）精确标度方程数值验证
（论文 5.5 节理论延伸）

理论预言（奇异连续谱测度驱动的非马尔可夫线型，α=1-D）：
  (1) 线型尾区中间渐近：S(δ) ~ δ^{-(2+D)}，即尾区对数斜率 β = 2 + D
      （奇异通道主导区 δ ∈ [10², 10⁶]，区别于纯洛伦兹 δ^{-4}）
  (2) 截断非局域相关时间：记忆核/关联函数 C(t) ~ t^{-α} 时，
      τ_NL(T) = [∫_0^T t C(t) dt] / [∫_0^T C(t) dt] = D/(1+D) · T
      非局域相关时间随观测窗口 T 线性增长、无有限极限 —— 幂律记忆的精确标志
      （对照：指数衰减 e^{-t/τ} 时 τ_NL 收敛到有限 τ）

验证方法：
  A. 线型尾区：论文 5.5 节混合谱线型 total_lineshape，奇异通道主导区
     δ ∈ [10², 10⁶] 拟合对数斜率，对照理论值 β = 2+D
  B. 独立数值验证：三进制 Cantor 测度傅里叶变换 |μ̂(t)| ~ t^{-α}（limsup 包络），
     数值积分截断一阶矩 τ_NL(T)，拟合 T 线性斜率，
     对照解析系数 D/(1+D)（对 C(t) ~ t^{-α}）
"""

import numpy as np
from scipy.special import gamma as gamma_func

# 论文 5.5 节参数
ALPHA = 1 - np.log(2) / np.log(3)      # α = 1-D = 0.3691
D_THEO = np.log(2) / np.log(3)         # Cantor 测度维数 = 0.6309
KAPPA = 0.5
GAMMA = 0.05
ETA = 0.8


# ---------------------------------------------------------------
# A. 线型尾区中间渐近斜率 β = 2 + D
# ---------------------------------------------------------------
def total_lineshape(delta, alpha=ALPHA, kappa=KAPPA, gamma=GAMMA, eta=ETA):
    """论文 5.5 节混合谱线型（洛伦兹光滑分量 + 奇异连续谱分量）。"""
    s = 1e-12 + 1j * delta
    KL = gamma ** 2 / (s + gamma)
    Ksc = kappa * gamma_func(1 - alpha) * s ** (alpha - 1.0)
    A = 1.0 / (s + (1 - eta) * KL + eta * Ksc)
    return np.real(A) / np.pi


def tail_slope_in_dominant_region():
    """奇异通道主导的中间渐近区 δ ∈ [10², 10⁶] 的尾区对数斜率。"""
    d = np.logspace(2.0, 6.0, 200)
    S = total_lineshape(d)
    slope, _ = np.polyfit(np.log(d), np.log(S), 1)
    return slope, 2 + D_THEO


# ---------------------------------------------------------------
# B. 截断非局域相关时间 τ_NL(T) —— Cantor 测度独立数值验证
# ---------------------------------------------------------------
def cantor_points(k):
    """k 级 Cantor 集：2^k 个等长区间内的中心点。"""
    idx = np.arange(2 ** k)
    pos = np.zeros(2 ** k)
    for j in range(k):
        bit = (idx >> (k - 1 - j)) & 1
        pos += bit * 2.0 * (3.0 ** (-(j + 1)))
    return pos + 0.5 * 3.0 ** (-k)


def correlation_envelope(T, k=14, nb=40):
    """Cantor 测度傅里叶变换模 |μ̂(t)| 的 limsup 对数分箱包络（抑制自相似振荡）。
    t ∈ [3, T]，返回 (t 格点, 包络值)。"""
    x = cantor_points(k)
    w = np.full(2 ** k, 1.0 / 2 ** k)
    t = np.geomspace(3.0, T, 2000)
    muhat = np.abs(np.exp(-1j * np.outer(t, x)).dot(w))
    log_t = np.log(t)
    edges = np.linspace(log_t.min(), log_t.max(), nb + 1)
    lt_m, lm_m = [], []
    for i in range(nb):
        m = (log_t >= edges[i]) & (log_t < edges[i + 1])
        if m.sum() > 1:
            lt_m.append(log_t[m].mean())
            lm_m.append(np.max(np.log(muhat[m])))
    return np.exp(np.array(lt_m)), np.exp(np.array(lm_m))


def truncated_correlation_time_numeric(T):
    """数值积分：C(t) = Cantor 测度 |μ̂(t)| 的 limsup 包络（梯形积分），
    τ_NL(T) = ∫₀^T t·C(t) dt / ∫₀^T C(t) dt。
    纯数值、不依赖幂律拟合，独立验证线性标度。"""
    t_env, c_env = correlation_envelope(T)
    t_all = np.concatenate(([0.0], t_env))
    c_all = np.concatenate(([1.0], c_env))
    num = np.trapz(t_all * c_all, t_all)
    den = np.trapz(c_all, t_all)
    return num / den


def verify_nlct_scaling(T_list=(1e2, 1e3, 1e4, 1e5, 1e6)):
    """拟合 τ_NL(T) 对 T 的对数斜率（应 ≈ 1），并对照解析系数 D/(1+D)。"""
    taus = []
    for T in T_list:
        taus.append(np.log(truncated_correlation_time_numeric(T)))
    taus = np.array(taus)
    slope_T, _ = np.polyfit(np.log(np.array(T_list)), taus, 1)
    return slope_T, taus


def main():
    print("=" * 66)
    print("NLCT 精确标度方程数值验证（论文 5.5 节理论延伸）")
    print("=" * 66)
    print(f"参数：α = 1-D = {ALPHA:.4f}，D = ln2/ln3 = {D_THEO:.4f}，κ={KAPPA}，γ={GAMMA}，η={ETA}")

    # A. 线型尾区中间渐近斜率
    slope, beta_theo = tail_slope_in_dominant_region()
    print(f"\n[A] 线型尾区中间渐近（奇异通道主导区 δ∈[10²,10⁶]）:")
    print(f"    拟合尾区对数斜率 β = {slope:.4f} vs 理论 β = 2+D = {beta_theo:.4f}")
    print(f"    对照纯洛伦兹尾区 β = 4（δ^{-4}）")

    # B. 非局域相关时间标度（Cantor 测度独立数值积分验证）
    T_list = (1e2, 1e3, 1e4, 1e5, 1e6)
    slope_T, taus = verify_nlct_scaling(T_list)
    print(f"\n[B] 截断非局域相关时间 τ_NL(T)（Cantor 测度 |μ̂| limsup 包络数值积分）:")
    print(f"    T       τ_NL(T) 数值        解析对照 D/(1+D)·T")
    coeff_theo = D_THEO / (1 + D_THEO)
    for T, t in zip(T_list, np.exp(taus)):
        print(f"    {T:>6.0e}   {t:>12.4e}   {coeff_theo * T:>12.4e}")
    print(f"    τ_NL(T) 对 T 的对数斜率 = {slope_T:.4f} vs 理论 1.0（线性增长、无有限极限）")
    print(f"    -> 幂律记忆（奇异连续谱）的精确标志；指数衰减对照：τ_NL 收敛于有限 τ=1/γ")


if __name__ == "__main__":
    main()
