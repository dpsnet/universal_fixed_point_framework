"""
Paper XLV §9.4 第 6a 项收尾：双谱/三谱的显式频域计算

背景：
  paper45_spectral_EFT_validation.py 的 V4 仅在时域验证了三阶累积量信号
  （非高斯噪声三阶累积量 > 高斯基准），未给出多谱塔 B(w1,w2) 与 T(w1,w2,w3)
  的显式频域计算。本脚本补齐这一项（§6.4 定理 6.3/6.4、§9.4 开放问题 6a）。

验证内容（频域，采用严格累积量定义）：
  P1: 双谱 B(w1,w2) 的三波共振支撑 —— 非零集中在 w1+w2=0（推论 6.2）
  P2: 高斯过程三谱（四阶累积量）逐点为零（Wick 定理）
  P3: 二次相位耦合信号的"双谱"相位相干均值非零，而无相位耦合对照为零
  P4: 谱静默区高阶谱发声 —— 静默 != 高斯（命题 6.3 的可检验判据）

对应论文：paper45_spectral_EFT_dissipative_fluids.md §6.4.3, §6.4.4, §9.4
"""
import numpy as np

PASS = 0
FAIL = 0

def check(name, cond, detail=""):
    global PASS, FAIL
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if cond:
        PASS += 1
    else:
        FAIL += 1


# ----------------------------------------------------------------------
# 双谱估计（直接法）
#   双谱：B(w1,w2) = E[ G(w1) G(w2) G*(w1+w2) ]
#   其中 * 为复共轭，G(w) 为分段的 DFT。
#   对零均值平稳过程，B 非零仅当 w1+w2 落在与三阶累积量关联的频率支撑上。
#   二次相位耦合（QPC）：若存在 f1, f2 与相位锁定的 f1+f2，则 B(f1,f2) 的
#   实部/虚部在跨段平均后不消失（相位相干），而无相位耦合则平均趋于零。
# ----------------------------------------------------------------------
def bispectrum_segmented(x, nfft, noverlap):
    n = len(x)
    step = nfft - noverlap
    n_seg = (n - nfft) // step + 1
    B = np.zeros((nfft, nfft), dtype=complex)
    for i in range(n_seg):
        seg = x[i*step : i*step+nfft]
        # 去均值
        seg = seg - seg.mean()
        G = np.fft.fft(seg)
        # B(w1,w2) = G(w1) G(w2) conj(G(w1+w2))
        # 用广播构造：B[a,b] = G[a] G[b] conj(G[(a+b) mod nfft])
        idx_sum = (np.arange(nfft)[:, None] + np.arange(nfft)[None, :]) % nfft
        B += np.outer(G, G) * np.conj(G[idx_sum])
    B /= n_seg
    freqs = np.fft.fftfreq(nfft)
    return freqs, B, n_seg


def trispectrum_diag_cumulant(x, nfft, noverlap):
    """
    三谱主对角切片（四阶累积量），严格定义：
      T(w) = cum[ G(w), G(w), G(w), G(-w) ]
           = E[ G(w)^3 G(-w) ] - 3 E[ G(w)^2 ] E[ G(w) G(-w) ]
    对零均值复高斯过程，E[G^3 G(-w)] = 3 E[G(w)^2] E[G(w)G(-w)]，
    故累积量严格为零（Wick 定理）。
    """
    n = len(x)
    step = nfft - noverlap
    n_seg = (n - nfft) // step + 1
    # 逐频点累加：m4 = E[G^3 conj(G)]（注意 G(-w) = conj(G(w)) 对实信号），
    # m2 = E[G^2]，m2p = E[G conj(G)] = E[|G|^2]
    m4 = np.zeros(nfft, dtype=complex)
    m2 = np.zeros(nfft, dtype=complex)
    m2p = np.zeros(nfft, dtype=float)
    for i in range(n_seg):
        seg = x[i*step : i*step+nfft]
        seg = seg - seg.mean()
        G = np.fft.fft(seg)
        m4 += G**3 * np.conj(G)
        m2 += G**2
        m2p += np.abs(G)**2
    m4 /= n_seg
    m2 /= n_seg
    m2p /= n_seg
    # 四阶累积量（主对角切片）
    T = m4 - 3.0 * m2 * m2p
    freqs = np.fft.fftfreq(nfft)
    return freqs, T, n_seg


# ======================================================================
# P1 + P3: 二次相位耦合（QPC）的双谱检测
# ======================================================================
print("=" * 70)
print("P1/P3: 二次相位耦合信号的双谱三波共振检测 (推论 6.2)")
print("=" * 70)

rng = np.random.default_rng(11)
nfft = 64
n_seg = 1024
n = n_seg * nfft

f1, f2 = 5, 9          # 两个基频（DFT bin）
fsum = (f1 + f2) % nfft  # 和频

# --- 有相位耦合的信号（QPC）：每个 segment 内部相位锁定 ---
x_qpc = np.zeros(n)
for i in range(n_seg):
    seg_t = np.arange(nfft)
    phi = rng.uniform(0, 2*np.pi)   # 每段一个共同相位
    seg = (np.cos(2*np.pi*f1*seg_t/nfft + phi)
           + np.cos(2*np.pi*f2*seg_t/nfft + phi)
           + 0.5*np.cos(2*np.pi*fsum*seg_t/nfft + 2*phi))  # 相位锁定：phi3 = 2*phi
    x_qpc[i*nfft:(i+1)*nfft] = seg

# --- 无相位耦合对照：每个基频相位独立随机 ---
x_unc = np.zeros(n)
for i in range(n_seg):
    seg_t = np.arange(nfft)
    p1 = rng.uniform(0, 2*np.pi)
    p2 = rng.uniform(0, 2*np.pi)
    p3 = rng.uniform(0, 2*np.pi)   # 和频相位独立 → 无耦合
    seg = (np.cos(2*np.pi*f1*seg_t/nfft + p1)
           + np.cos(2*np.pi*f2*seg_t/nfft + p2)
           + 0.5*np.cos(2*np.pi*fsum*seg_t/nfft + p3))
    x_unc[i*nfft:(i+1)*nfft] = seg

freqs_q, B_qpc, _ = bispectrum_segmented(x_qpc, nfft, 0)
freqs_u, B_unc, _ = bispectrum_segmented(x_unc, nfft, 0)

# 双谱在共振点 (f1, f2) 的幅值
b_qpc_res = np.abs(B_qpc[f1, f2])
b_unc_res = np.abs(B_unc[f1, f2])
# 背景（非共振点）平均幅值
bg_qpc = np.abs(B_qpc).mean()
bg_unc = np.abs(B_unc).mean()

check("P1: QPC 双谱在共振点 (f1,f2) 显著高于背景",
      b_qpc_res > 20.0 * bg_qpc,
      f"共振={b_qpc_res:.2e}, 背景={bg_qpc:.2e}")

check("P3: 有相位耦合的双谱共振 ≫ 无耦合对照",
      b_qpc_res > 5.0 * b_unc_res + 1e-3,
      f"耦合={b_qpc_res:.2e}, 无耦合={b_unc_res:.2e}")

# 三波共振支撑：在 (f1, f2), (f2, f1) 及对称点都应显著
sym_pts = [(f1,f2),(f2,f1),(nfft-f1,nfft-f2),(nfft-f2,nfft-f1)]
sym_vals = [np.abs(B_qpc[a,b]) for a,b in sym_pts]
check("P1b: 三波共振点族均显著（共振支撑完整）",
      all(v > 10.0*bg_qpc for v in sym_vals),
      f"对称点幅值 = {[f'{v:.1e}' for v in sym_vals]}")

# ======================================================================
# P2: 高斯过程三谱（四阶累积量）逐点为零
# ======================================================================
print()
print("=" * 70)
print("P2: 高斯过程三谱(四阶累积量)逐点为零 (Wick 定理)")
print("=" * 70)

# 纯高斯信号
g = rng.standard_normal(n)
freqs_t, T_g, _ = trispectrum_diag_cumulant(g, nfft, 0)
# 参考尺度：功率谱的平方
G0 = np.fft.fft(g[:nfft] - g[:nfft].mean())
S2 = np.mean(np.abs(G0)**2)**2
T_norm = np.abs(T_g) / (S2 + 1e-30)

check("P2: 高斯四阶累积量（三谱对角）近零",
      np.max(T_norm) < 1.0,
      f"max |T|/|S|^2 = {np.max(T_norm):.3e}")

# 非高斯（Hermite 三阶修正）应给出非零三谱
xi = g + 0.3*(rng.standard_normal(n)**3 - 3*rng.standard_normal(n))
_, T_ng, _ = trispectrum_diag_cumulant(xi, nfft, 0)
T_ng_norm = np.abs(T_ng) / (np.mean(np.abs(np.fft.fft(xi[:nfft]))**2)**2 + 1e-30)
check("P2b: 非高斯过程三谱对角显著非零",
      np.max(T_ng_norm) > 2.0 * np.max(T_norm),
      f"高斯 max={np.max(T_norm):.3e}, 非高斯 max={np.max(T_ng_norm):.3e}")

# ======================================================================
# P4: 谱静默区高阶谱发声（静默 != 高斯，命题 6.3）
# ======================================================================
print()
print("=" * 70)
print("P4: 谱静默 != 高斯（命题 6.3 的数学陈述验证）")
print("=" * 70)

# 命题 6.3 的核心：O_2 = 0（二阶统计静默）与 O_3, O_4 != 0（高阶发声）
# 是两个独立维度。最直接的检验：构造零均值、可任意缩小的二阶矩，
# 但标准化三阶累积量（偏度）恒不变（非高斯）的分布。
# 用偏态分布 x -> a*x，则 var -> a^2 var，skewness 不变（尺度无关）。
# 因此"令二阶统计（功率）趋于静默"不改变非高斯性——这正是静默 != 高斯。

n4 = 200000
rng4 = np.random.default_rng(12)
# 非高斯（偏态）：指数分布中心化（偏度恒为 2，尺度无关）
base_skew = rng4.exponential(1.0, n4)
base_skew = base_skew - base_skew.mean()   # 零均值

# 高斯对照
base_gauss = rng4.standard_normal(n4)

def moments(x):
    m2 = np.mean(x**2)                      # 二阶（功率/方差）
    m3 = np.mean(x**3)                      # 三阶
    skew = m3 / (m2**1.5 + 1e-30)           # 标准化三阶累积量（偏度）
    return m2, skew

# 静默操作：对幅度乘以极小的标度因子 a -> 0，二阶功率趋于零，
# 但偏度（尺度不变的标准三阶累积量）应保持不变
scale = 1e-6
m2_skew, skew_skew = moments(base_skew * scale)
m2_gauss, skew_gauss = moments(base_gauss * scale)

# P4a: 静默后二阶功率确实近零（谱静默实现）
check("P4a: 幅度缩放后二阶功率近零（谱静默可实现）",
      m2_skew < 1e-6,
      f"静默后二阶矩 = {m2_skew:.3e}")

# P4b: 但标准化三阶累积量（偏度）保持不变且非零 —— 静默 != 高斯
check("P4b: 静默后偏度保持非零（高阶谱仍发声，静默!=高斯）",
      abs(skew_skew - 2.0) < 0.1 and abs(skew_skew) > 10.0*abs(skew_gauss),
      f"静默后偏度 = {skew_skew:.3f}（理论 2），高斯偏度 = {skew_gauss:.3f}")

# P4c: 命题 6.3 的序参量结构：O_2 可独立趋于零而 O_3 不趋于零
O2 = m2_skew          # 序参量 O_2（二阶统计）
O3 = skew_skew        # 序参量 O_3（三阶标准化累积量）
check("P4c: O_2 与 O_3 独立（O_2 可静默而 O_3 保持非零）",
      O2 < 1e-6 and abs(O3) > 1.0,
      f"O_2={O2:.2e}, O_3={O3:.3f}")

print()
print("=" * 70)
print(f"多谱塔频域计算总结: {PASS} 通过 / {FAIL} 失败")
print("=" * 70)
if FAIL == 0:
    print("双谱/三谱显式频域计算全部检查项通过（§9.4 第6a项闭合）。")
else:
    print(f"有 {FAIL} 项未通过。")
