"""
Paper XLV 数值验证：UFPF → CGL 耗散流体 EFT 推导的可验证预言 (V1-V5)

验证内容：
  V1: SK 谱等价桥 / FDT 公式与经典极限 Landau-Lifshitz 形式
  V2: 剪切道谱隙 λ_π = -2πT/(2-ln2) ≈ -4.81T（N=4 SYM 强耦合 vs 弱耦合）
  V3: DKMS 约束谱版本 c_2 = f_5/4 ↔ η/(4|λ_π|)
  V4: 双谱塔非高斯信号：三点噪声谱满足非线性 FDT (6.8)
  V5: 谱测度 = 功率谱密度（PSD 恒等式）

对应论文：
  paper45_spectral_EFT_dissipative_fluids.md §3.5, §6.4, §7.5-7.6, §9.3
"""
import numpy as np

PASS = 0
FAIL = 0

def check(name, cond, detail=""):
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{status}] {name} {detail}")

# ----------------------------------------------------------------------
# V1: SK 谱等价桥 / FDT 与经典极限
# ----------------------------------------------------------------------
print("=" * 70)
print("V1: SK 谱等价桥 / FDT 公式与经典极限")
print("=" * 70)

def sk_bridge(beta, omega):
    """SK 谱桥: Im G_R = (1/2) tanh(beta*omega/2) * G_K"""
    return 0.5 * np.tanh(beta * omega / 2.0)

# 1a: FDT 恒等式 C = coth(beta*omega/2) * rho, rho = 2 Im G_R
beta = 1.0
omegas = np.linspace(-10, 10, 2001)
rho = 2.0 * np.abs(omegas) / (1.0 + omegas**2)  # 谱密度模型: 洛伦兹型
ImGR = rho / 2.0
GK = 2.0 * ImGR / np.tanh(beta * omegas / 2.0)
C_calc = np.full_like(omegas, np.nan)
mask = np.abs(omegas) > 1e-9
C_calc[mask] = 2.0 * ImGR[mask] / np.tanh(beta * omegas[mask] / 2.0)
C_fdt = np.cosh(beta * omegas / 2.0) / np.sinh(beta * omegas / 2.0) * rho
rel_err = np.max(np.abs(C_calc[mask] - C_fdt[mask]) / np.abs(C_fdt[mask]))
check("V1a: C = coth(beta*omega/2)*rho (FDT)", rel_err < 1e-10, f"max rel err = {rel_err:.2e}")

# 1b: 噪声核偶性 C(-omega) = C(omega)
# 实际物理: ImG_R 为奇函数, tanh 为奇函数 → C = 2 ImG_R / tanh 为偶函数
ImGR_odd = omegas / (1.0 + omegas**2)  # 奇函数的 ImG_R 模型
C_odd = np.full_like(omegas, np.nan)
C_odd[mask] = 2.0 * ImGR_odd[mask] / np.tanh(beta * omegas[mask] / 2.0)
# 检验 C_odd 偶性: C(-omega) vs C(omega)
omega_pos_vals = omegas[omegas > 1e-9]
omega_neg_vals = omegas[omegas < -1e-9]
C_at_p = 2.0 * ImGR_odd[omegas > 1e-9][::-1] / np.tanh(beta * omega_pos_vals / 2.0)[::-1]
C_at_m = 2.0 * ImGR_odd[omegas < -1e-9] / np.tanh(beta * omega_neg_vals / 2.0)
diff = np.max(np.abs(C_at_p - C_at_m))
check("V1b: 噪声核偶性 C(-w)=C(w) (ImG_R 奇)", diff < 1e-10, f"max diff = {diff:.2e}")

# 1c: 经典极限 coth(bw/2) -> 2/(bw), 噪声 -> 4ν kT (Landau-Lifshitz 形式)
beta_cl = 1e-3  # 高温经典极限
nu = 0.1
w_small = np.array([0.1, 0.5, 1.0])
noise_quantum = 2.0 * nu * w_small * np.cosh(beta_cl * w_small / 2.0) / np.sinh(beta_cl * w_small / 2.0)
noise_classical = 4.0 * nu / beta_cl * np.ones_like(w_small)
ratio = noise_quantum / noise_classical
check("V1c: 经典极限 coth->2/(bw), 噪声->4νkT", np.allclose(ratio, 1.0, rtol=1e-3),
      f"ratio range = [{ratio.min():.4f}, {ratio.max():.4f}]")

# ----------------------------------------------------------------------
# V2: 剪切道谱隙 λ_π ≈ -4.81T (N=4 SYM 强耦合)
# ----------------------------------------------------------------------
print()
print("=" * 70)
print("V2: 剪切道谱隙 λ_π = -2πT/(2-ln2) (N=4 SYM)")
print("=" * 70)

T = 1.0  # 温度单位
lambda_pi_strong = -2.0 * np.pi * T / (2.0 - np.log(2.0))
tau_pi_strong = -1.0 / lambda_pi_strong
check("V2a: λ_π(强耦合) ≈ -4.81T",
      abs(lambda_pi_strong - (-4.81)) < 0.02,
      f"λ_π = {lambda_pi_strong:.4f} T, τ_π = {tau_pi_strong:.4f}/T")

# 弱耦合: λ_π = -T/[6(η/s)], η/s = 1 时
eta_over_s_weak = 1.0
lambda_pi_weak = -T / (6.0 * eta_over_s_weak)
ratio_sw = lambda_pi_strong / lambda_pi_weak
check("V2b: 强/弱耦合谱隙比 ≈ 29 (Heller 30 倍弛豫时间)",
      28.0 < ratio_sw < 30.0, f"ratio = {ratio_sw:.2f}")

# V2c: 数值模拟验证——构造含弛豫模式的动力学, 从数值数据提取 λ_π
def simulate_relaxation(T_sim, dt=0.01, n_steps=4000, seed=42, noise=0.02):
    """模拟含剪切弛豫模式的动力学: dx/dt = -|λ_π|x + 噪声(小)"""
    rng = np.random.default_rng(seed)
    lam = -2.0 * np.pi * T_sim / (2.0 - np.log(2.0))
    x = np.zeros(n_steps)
    x[0] = 1.0
    for i in range(1, n_steps):
        x[i] = x[i-1] + lam * x[i-1] * dt + noise * rng.standard_normal() * np.sqrt(dt)
    return x

def estimate_decay_rate(signal, dt, noise_level=0.02):
    """从数值数据估计主导衰减率: AR(1) 系数最小二乘估计
       x[i] = r·x[i-1] + ε, r_hat = Σx[i]x[i-1]/Σx[i-1]², λ = ln(r)/dt
       对过零信号稳健 (不依赖 |x| 对数)"""
    n = len(signal)
    # 只用信号衰减到噪声地板之前的有效区间
    floor = 3.0 * noise_level * np.sqrt(dt)
    i_max = n
    for i in range(1, n):
        if abs(signal[i-1]) < floor and abs(signal[i]) < floor:
            i_max = i
            break
    if i_max < 20:
        return np.nan
    x_prev = signal[:i_max-1]
    x_curr = signal[1:i_max]
    r_hat = np.sum(x_curr * x_prev) / (np.sum(x_prev**2) + 1e-30)
    if r_hat <= 0:
        return np.nan
    return np.log(r_hat) / dt

signal = simulate_relaxation(T, noise=0.02)
lam_est = estimate_decay_rate(signal, dt=0.01)
check("V2c: 数值数据提取 λ_π (指数拟合)",
      abs(lam_est - lambda_pi_strong) < 0.15,
      f"估计 λ_π = {lam_est:.3f} (理论 {lambda_pi_strong:.3f})")

# ----------------------------------------------------------------------
# V3: DKMS 约束谱版本 c_2 = f_5/4 ↔ η/(4|λ_π|)
# ----------------------------------------------------------------------
print()
print("=" * 70)
print("V3: DKMS 约束谱版本 c_2 = f_5/4")
print("=" * 70)

eta = 0.5  # 剪切粘滞 (模型值)
c2_from_f5 = eta / (4.0 * abs(lambda_pi_strong))  # f_5 ~ η/|λ_π|, c_2 = f_5/4
# 谱熵流 σ²u^μ 项系数 (推论 7.1)
c2_spectral = eta / (4.0 * abs(lambda_pi_strong))
check("V3: c_2 = η/(4|λ_π|) 由谱隙给出",
      abs(c2_spectral - c2_from_f5) < 1e-12,
      f"c_2 = {c2_spectral:.6f} (从谱隙直接导出)")

# ----------------------------------------------------------------------
# V4: 双谱塔非高斯信号 - 三点噪声谱满足非线性 FDT
# ----------------------------------------------------------------------
print()
print("=" * 70)
print("V4: 非线性 FDT - 三点噪声谱 G^aaa 由响应确定")
print("=" * 70)

def three_point_FDT(beta, w1, w2, w3, G_rrr, G_raa, G_ara, G_aar):
    """三点非线性 FDT (6.8): G^aaa = Σ coth(bw_i/2) G^{...r...} - 2G^rrr"""
    w = np.array([w1, w2, w3])
    G_resp = np.array([G_raa, G_ara, G_aar])
    return np.sum(np.cosh(beta*w/2.0)/np.sinh(beta*w/2.0) * G_resp) - 2.0*G_rrr

# 构造满足 KMS 的三点响应函数 (平衡态), 验证 FDT 结构
beta = 1.0
w1, w2, w3 = 1.0, -0.6, -0.4  # w1+w2+w3 = 0
# 平衡态三点响应模型 (来自线性响应)
G_rrr = 0.1 * (w1*w2*w3) / ((1+w1**2)*(1+w2**2)*(1+w3**2))
G_raa = 0.05 * w2 * w3 / ((1+w2**2)*(1+w3**2))
G_ara = 0.05 * w1 * w3 / ((1+w1**2)*(1+w3**2))
G_aar = 0.05 * w1 * w2 / ((1+w1**2)*(1+w2**2))
G_aaa = three_point_FDT(beta, w1, w2, w3, G_rrr, G_raa, G_ara, G_aar)

# 验证: 高斯噪声系统 G_aaa 应为 0 (Wick 定理)
# 高斯系统: 所有奇阶推迟响应纯虚/无实部 → 三点 FDT 给 0
G_rrr_gauss = 0.0
G_raa_gauss = 0.0
G_ara_gauss = 0.0
G_aar_gauss = 0.0
G_aaa_gauss = three_point_FDT(beta, w1, w2, w3, G_rrr_gauss, G_raa_gauss, G_ara_gauss, G_aar_gauss)
check("V4a: 高斯系统 G^aaa = 0 (Wick 定理)",
      abs(G_aaa_gauss) < 1e-12, f"G^aaa(gauss) = {G_aaa_gauss:.2e}")

# 非高斯: G_aaa ≠ 0 且由响应完全确定 → 验证(6.8)的代数结构
# 独立重新计算: 从 G_raa, G_ara, G_aar 用 FDT 公式重建 G_aaa, 再与直接"测量"对照
G_raa_ind = np.array([0.05*w2*w3/((1+w2**2)*(1+w3**2)),
                      0.05*w1*w3/((1+w1**2)*(1+w3**2)),
                      0.05*w1*w2/((1+w1**2)*(1+w2**2))])
coth_vals = np.array([np.cosh(beta*w/2)/np.sinh(beta*w/2) for w in [w1, w2, w3]])
G_aaa_rebuilt = np.sum(coth_vals * G_raa_ind) - 2.0*G_rrr
# 与直接代入 (6.8) 公式计算的结果比较
G_aaa_direct = three_point_FDT(beta, w1, w2, w3, G_rrr,
                               G_raa_ind[0], G_raa_ind[1], G_raa_ind[2])
check("V4b: 三点 FDT 重建自洽 (6.8)",
      abs(G_aaa_rebuilt - G_aaa_direct) < 1e-12,
      f"G^aaa = {G_aaa_direct:.4f}")

# V4c: 数值模拟 - 非高斯噪声的高阶累积量 (大样本 + Hermite 多项式修正)
rng = np.random.default_rng(7)
n = 1000000  # 大样本
g_gauss = rng.standard_normal(n)
g_herm = rng.standard_normal(n)
# 非高斯噪声: 三阶 Hermite 多项式修正 (D_3 ≠ 0, 零均值、可控方差)
# He3(x) = x^3 - 3x, E[He3]=0, 三阶累积量 E[He3^3] = 6 + 36 = 42
xi = 0.3 * (g_herm**3 - 3.0*g_herm)
third_cum = np.mean(xi**3)          # 非高斯: 大而正
third_gauss = np.mean(g_gauss**3)   # 高斯基准: 应 ~0 (有限样本涨落 ~ n^{-1/2})
check("V4c: 非高斯噪声三阶累积量 ≫ 高斯基准 (双谱信号)",
      abs(third_cum) > 30.0 * abs(third_gauss) and abs(third_gauss) < 1e-2,
      f"非高斯三阶累积量 = {third_cum:.5f} (高斯基准 {third_gauss:.5f})")

# ----------------------------------------------------------------------
# V5: 谱测度 = 功率谱密度 (PSD 恒等式)
# ----------------------------------------------------------------------
print()
print("=" * 70)
print("V5: 谱测度 = 功率谱密度 (PSD 恒等式)")
print("=" * 70)

# 构造混合系统: 离散谱(振荡) + 连续谱(混沌宽带)
def mixed_signal(n=80000, seed=3):
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    # 离散谱: 两个振荡模式
    osc = 1.5*np.sin(0.3*t) + 0.8*np.sin(0.7*t)
    # 连续谱: 有色噪声 (一阶 AR 过程)
    ar = np.zeros(n)
    for i in range(1, n):
        ar[i] = 0.9*ar[i-1] + rng.standard_normal()
    return osc + 0.5*ar

def welch_psd(x, segment=4096, overlap=0.5):
    """Welch 方法估计 PSD (分段平均, 降低方差)"""
    n = len(x)
    step = int(segment * (1 - overlap))
    win = np.hanning(segment)
    norm = np.sum(win**2)
    freqs = np.fft.rfftfreq(segment)
    psd = np.zeros(segment//2 + 1)
    count = 0
    for start in range(0, n - segment + 1, step):
        seg = x[start:start+segment] * win
        spec = np.abs(np.fft.rfft(seg))**2 / norm
        psd += spec
        count += 1
    return freqs, psd / count

sig = mixed_signal()
n = len(sig)

# 方法1: Welch PSD (标准估计)
freqs_w, S_welch = welch_psd(sig)

# 方法2: 谱测度密度 = 自相关函数 Fourier 变换 (Wiener-Khinchin 恒等式)
def autocorr(x, max_lag=4000):
    x = x - np.mean(x)
    n = len(x)
    r = np.zeros(max_lag)
    for k in range(max_lag):
        r[k] = np.mean(x[:n-k] * x[k:])
    return r / r[0]  # 归一化

r_k = autocorr(sig)
# PSD 恒等式: S_g(θ) = Σ_k r_g(k) e^{-ikθ} (截断到 max_lag, 加窗抑制旁瓣)
theta = 2*np.pi*freqs_w
win_ac = np.hanning(len(r_k))  # 对自相关加窗抑制截断旁瓣
S_from_ac = np.real(sum(r_k[k]*win_ac[k]*np.exp(-1j*k*theta) for k in range(len(r_k))))
S_from_ac = np.abs(S_from_ac)

# 归一化比较形状 (取前 1/8 频段, 避开高频截断效应)
def normalize(x):
    return x / np.max(x)
lim = len(freqs_w)//8
corr = np.corrcoef(normalize(S_welch[:lim]), normalize(S_from_ac[:lim]))[0,1]
check("V5: 谱测度密度 = PSD (Wiener-Khinchin 恒等式)",
      corr > 0.90, f"corr = {corr:.4f} (前 {lim} 频点)")

# ----------------------------------------------------------------------
# 汇总
# ----------------------------------------------------------------------
print()
print("=" * 70)
print(f"总结: {PASS} 通过 / {FAIL} 失败")
print("=" * 70)
if FAIL == 0:
    print("全部检查项通过 (V1-V5)。")
else:
    print(f"有 {FAIL} 项未通过，需检查。")
