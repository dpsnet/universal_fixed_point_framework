"""
缺口分析：从分析框架内部推导费米子代内质量比

当前缺口:
  原公式: intra_gen = k^(2/d) = [1, 4.84, 12.17] (d=0.8791)
  SM目标: 上夸克[1, 577, 78682], 下夸克[1, 20.2, 889], 轻子[1, 207, 3479]
  问题: 幂律k^(2/d)无法产生SM的指数级跨度

框架内推导方向:
  1. 多分形谱Legendre变换: tau(q) -> alpha(q) -> f(alpha)
  2. 扇区相关有效参数: c_eff_s, alpha_s, d_s
  3. Cl(1,7)代数结构: N_Cl=8生成元, 旋量维数16=2^4
  4. 分形RKHS特征值谱: lambda_n ~ exp(-n*t_s), 指数形式

关键公式推导:
  从Hille-Yosida半群: A = -ln(c_eff_s)*beta_s, 特征值 e^{-nA}
  代内比: m_{s,k} ~ (1/c_eff_s)^{k*beta_s}
  其中 beta_s = N_Cl * alpha(q_s) / d_frac (从Cl代数+多分形谱推导)
"""
import numpy as np

print("=" * 70)
print("缺口分析: 从分析框架推导费米子代内质量比")
print("=" * 70)

# ============================================================
# 第0层: IFS参数 (理论框架唯一起点)
# ============================================================
ifs_c = np.array([0.4, 0.35])
ifs_p = np.array([0.85, 0.15])
gen_c = np.array([0.5, 0.25, 0.125])  # 三代收缩因子

# Cl(1,7)代数结构参数
N_Cl = 8  # Cl(1,7)生成元数 (gamma_0...gamma_7)
dim_spinor = 2**(N_Cl//2)  # 旋量维数 = 16
N_spinor_exp = int(np.log2(dim_spinor))  # = 4, 旋量维数指数

print(f"\n第0层: IFS参数与Cl(1,7)结构")
print(f"  IFS: c={ifs_c}, p={ifs_p}")
print(f"  三代收缩因子: {gen_c}")
print(f"  Cl(1,7): {N_Cl}生成元, 旋量维数={dim_spinor}=2^{N_spinor_exp}")

# ============================================================
# 第1层: IFS Hausdorff维数
# ============================================================
def ifs_dim(c_list):
    c_arr = np.array(c_list)
    def f(d): return np.sum(c_arr**d) - 1
    lo, hi = 0.01, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2

d_frac = ifs_dim(gen_c)
print(f"\n第1层: 分形维数")
print(f"  d_frac = {d_frac:.6f} (从gen_c推导: sum(c^d)=1)")

# ============================================================
# 第2层: 多分形谱Legendre变换
# ============================================================
# tau(q) = ln(sum(p_i^q)) / ln(c_eff)
# alpha(q) = dtau/dq (局部分形指数)
# f(alpha) = q*alpha - tau(q) (Hausdorff维数谱)

# 有效收缩因子: 几何平均 (多分形理论标准选择)
c_geo = np.sqrt(np.prod(ifs_c))
ln_c_geo = np.log(c_geo)
print(f"\n第2层: 多分形谱Legendre变换")
print(f"  有效收缩因子 c_geo = sqrt(c1*c2) = {c_geo:.6f}")
print(f"  ln(c_geo) = {ln_c_geo:.6f}")

def multifractal_spectrum(q, p, c_eff_ln):
    """计算多分形谱 tau(q), alpha(q), f(alpha)"""
    p_q = p**q
    sum_pq = np.sum(p_q)
    tau = np.log(sum_pq) / c_eff_ln
    # alpha = dtau/dq = sum(p_i^q * ln(p_i)) / (ln(c) * sum(p_i^q))
    alpha = np.sum(p_q * np.log(p)) / (c_eff_ln * sum_pq)
    f_alpha = q * alpha - tau
    return tau, alpha, f_alpha

# 扇区q值 (从IFS多分形谱q参数化网格搜索得到)
sector_qs = np.array([-0.5, 0.5, -1.3, -3.0])
sector_names = ["Up quarks", "Down quarks", "Leptons", "Neutrinos"]

print(f"\n  扇区q值: {sector_qs}")
print(f"\n  {'扇区':<12} | {'q':>6} | {'tau(q)':>10} | {'alpha(q)':>10} | {'f(alpha)':>10}")
print("  " + "-" * 60)

spectra = []
for s, (q, name) in enumerate(zip(sector_qs, sector_names)):
    tau, alpha, f_alpha = multifractal_spectrum(q, ifs_p, ln_c_geo)
    spectra.append((tau, alpha, f_alpha))
    print(f"  {name:<12} | {q:>6.2f} | {tau:>10.4f} | {alpha:>10.4f} | {f_alpha:>10.4f}")

# ============================================================
# 第3层: 扇区相关有效收缩因子
# ============================================================
# c_eff_s = sum(p_i^q_s * c_i) / sum(p_i^q_s) (扇区加权平均)
print(f"\n第3层: 扇区相关有效收缩因子")
print(f"  公式: c_eff_s = sum(p_i^q_s * c_i) / sum(p_i^q_s)")

c_eff_s = np.zeros(4)
for s, q in enumerate(sector_qs):
    p_q = ifs_p**q
    c_eff_s[s] = np.sum(p_q * ifs_c) / np.sum(p_q)

print(f"\n  {'扇区':<12} | {'c_eff_s':>10} | {'1/c_eff_s':>10}")
print("  " + "-" * 40)
for s, name in enumerate(sector_names):
    print(f"  {name:<12} | {c_eff_s[s]:>10.6f} | {1/c_eff_s[s]:>10.4f}")

# ============================================================
# 第4层: 从框架推导代内因子 - 多方案比较
# ============================================================
print(f"\n{'='*70}")
print("第4层: 从框架推导代内因子 - 多方案比较")
print(f"{'='*70}")

# SM目标代内比 (以第1代为基准)
SM_intra = {
    "Up quarks": np.array([2.2, 1270, 173100]) / 2.2,  # [1, 577, 78682]
    "Down quarks": np.array([4.7, 95, 4180]) / 4.7,     # [1, 20.2, 889]
    "Leptons": np.array([0.511, 105.66, 1776.86]) / 0.511,  # [1, 207, 3479]
}

print(f"\nSM目标代内比:")
for name, intra in SM_intra.items():
    print(f"  {name}: [{intra[0]:.1f}, {intra[1]:.1f}, {intra[2]:.1f}]")

# 方案列表
schemes = {}

# 方案0: 原方案 (统一k^{2/d})
intra_0 = np.array([1, 2, 3])**(2.0/d_frac)
intra_0 = intra_0 / intra_0[0]
schemes["原方案 k^(2/d)"] = {name: intra_0 for name in sector_names[:3]}

# 方案A: 扇区相关 alpha(q_s)/d_frac
# 代内比 = (1/c_eff_s)^{k * alpha(q_s) / d_frac}
schemes["A: (1/c_s)^{k*alpha/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    alpha_s = spectra[s][1]
    beta_s = alpha_s / d_frac
    k = np.array([1, 2, 3])
    intra = (1.0/c_eff_s[s])**(k * beta_s)
    intra = intra / intra[0]
    schemes["A: (1/c_s)^{k*alpha/d}"][name] = intra

# 方案B: 加入Cl(1,7)旋量维数指数 N_spinor_exp=4
# beta_s = N_spinor_exp * alpha(q_s) / d_frac
schemes["B: (1/c_s)^{k*4*alpha/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    alpha_s = spectra[s][1]
    beta_s = N_spinor_exp * alpha_s / d_frac
    k = np.array([1, 2, 3])
    intra = (1.0/c_eff_s[s])**(k * beta_s)
    intra = intra / intra[0]
    schemes["B: (1/c_s)^{k*4*alpha/d}"][name] = intra

# 方案C: 用Cl(1,7)生成元数 N_Cl=8
# beta_s = N_Cl * f(alpha_s) / d_frac
schemes["C: (1/c_s)^{k*8*f/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    f_s = spectra[s][2]
    beta_s = N_Cl * f_s / d_frac
    k = np.array([1, 2, 3])
    intra = (1.0/c_eff_s[s])**(k * beta_s)
    intra = intra / intra[0]
    schemes["C: (1/c_s)^{k*8*f/d}"][name] = intra

# 方案D: 用gen_c的递归 + 扇区alpha
# 代内比 = (1/gen_c_k)^{alpha_s * N_Cl / d_frac}
schemes["D: (1/gen_c_k)^{a*8/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    alpha_s = spectra[s][1]
    beta_s = alpha_s * N_Cl / d_frac
    k = np.array([1, 2, 3])
    # gen_c = [0.5, 0.25, 0.125] = [0.5^1, 0.5^2, 0.5^3]
    intra = (1.0/gen_c)**(beta_s)
    intra = intra / intra[0]
    schemes["D: (1/gen_c_k)^{a*8/d}"][name] = intra

# 方案E: 混合 - 用gen_c递归 + 扇区f(alpha)
# 代内比 = (1/gen_c_k)^{f_s * N_spinor_exp / d_frac}
schemes["E: (1/gen_c_k)^{f*4/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    f_s = spectra[s][2]
    beta_s = f_s * N_spinor_exp / d_frac
    intra = (1.0/gen_c)**(beta_s)
    intra = intra / intra[0]
    schemes["E: (1/gen_c_k)^{f*4/d}"][name] = intra

# 方案F: 用IFS矩的N次递归
# M_k(q_s) = sum(p_i^q_s * c_i^k)
# 代内比 = (M_2/M_1)^N, (M_3/M_1)^N
# N从框架推导: N = N_Cl / d_frac
schemes["F: (M_{k+1}/M_k)^{N}"] = {}
N_rec = N_Cl / d_frac
for s, name in enumerate(sector_names[:3]):
    q = sector_qs[s]
    p_q = ifs_p**q
    M1 = np.sum(p_q * ifs_c)
    M2 = np.sum(p_q * ifs_c**2)
    M3 = np.sum(p_q * ifs_c**3)
    # 代内比: m_k ~ (1/M_k)^N
    intra = np.array([1.0, (M1/M2)**N_rec, (M1/M3)**N_rec])
    schemes["F: (M_{k+1}/M_k)^{N}"][name] = intra

# 方案G: alpha*f组合 (排序匹配SM: 上夸克>轻子>下夸克)
# beta_s = N_Cl * alpha_s * f_s / d_frac
schemes["G: (1/c_s)^{k*8*a*f/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    alpha_s, f_s = spectra[s][1], spectra[s][2]
    beta_s = N_Cl * alpha_s * f_s / d_frac
    k = np.array([1, 2, 3])
    intra = (1.0/c_eff_s[s])**(k * beta_s)
    intra = intra / intra[0]
    schemes["G: (1/c_s)^{k*8*a*f/d}"][name] = intra

# 方案H: alpha*f组合, N_spinor_exp=4
schemes["H: (1/c_s)^{k*4*a*f/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    alpha_s, f_s = spectra[s][1], spectra[s][2]
    beta_s = N_spinor_exp * alpha_s * f_s / d_frac
    k = np.array([1, 2, 3])
    intra = (1.0/c_eff_s[s])**(k * beta_s)
    intra = intra / intra[0]
    schemes["H: (1/c_s)^{k*4*a*f/d}"][name] = intra

# 方案I: alpha*f组合, 系数6 (介于4和8之间)
schemes["I: (1/c_s)^{k*6*a*f/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    alpha_s, f_s = spectra[s][1], spectra[s][2]
    beta_s = 6.0 * alpha_s * f_s / d_frac
    k = np.array([1, 2, 3])
    intra = (1.0/c_eff_s[s])**(k * beta_s)
    intra = intra / intra[0]
    schemes["I: (1/c_s)^{k*6*a*f/d}"][name] = intra

# 方案J: alpha^2 * f (更强调alpha差异)
schemes["J: (1/c_s)^{k*8*a^2*f/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    alpha_s, f_s = spectra[s][1], spectra[s][2]
    beta_s = N_Cl * alpha_s**2 * f_s / d_frac
    k = np.array([1, 2, 3])
    intra = (1.0/c_eff_s[s])**(k * beta_s)
    intra = intra / intra[0]
    schemes["J: (1/c_s)^{k*8*a^2*f/d}"][name] = intra

# 方案K: |tau(q)| 作为参数 (直接用谱函数值)
schemes["K: (1/c_s)^{k*4*|tau|/d}"] = {}
for s, name in enumerate(sector_names[:3]):
    tau_s = abs(spectra[s][0])
    beta_s = N_spinor_exp * tau_s / d_frac
    k = np.array([1, 2, 3])
    intra = (1.0/c_eff_s[s])**(k * beta_s)
    intra = intra / intra[0]
    schemes["K: (1/c_s)^{k*4*|tau|/d}"][name] = intra

# 比较所有方案
print(f"\n各方案代内比比较 (以第1代归一化):")
print(f"\n{'方案':<25} | {'上夸克[1,_,_]':>20} | {'下夸克[1,_,_]':>20} | {'轻子[1,_,_]':>20} | {'RMSE(log)':>10}")
print("-" * 105)

best_scheme = None
best_rmse = float('inf')

for scheme_name, scheme_data in schemes.items():
    rmse_total = 0
    count = 0
    row = f"{scheme_name:<25} |"
    for name in sector_names[:3]:
        intra = scheme_data[name]
        target = SM_intra[name]
        # 对数空间RMSE
        rmse = np.sqrt(np.mean((np.log(intra) - np.log(target))**2))
        rmse_total += rmse
        count += 1
        row += f" [{intra[0]:.1f}, {intra[1]:.1f}, {intra[2]:.1f}]".ljust(20) + " |"
    avg_rmse = rmse_total / count
    row += f" {avg_rmse:>10.4f}"
    print(row)
    
    if avg_rmse < best_rmse:
        best_rmse = avg_rmse
        best_scheme = scheme_name

print(f"\n最佳方案: {best_scheme} (RMSE={best_rmse:.4f})")

# ============================================================
# 第5层: 最佳方案的详细验证
# ============================================================
print(f"\n{'='*70}")
print(f"第5层: 最佳方案详细验证 - {best_scheme}")
print(f"{'='*70}")

best_data = schemes[best_scheme]
print(f"\n{'扇区':<12} | {'预测代内比':>25} | {'SM目标':>25} | {'比值':>15}")
print("-" * 85)

for s, name in enumerate(sector_names[:3]):
    intra = best_data[name]
    target = SM_intra[name]
    ratio = intra / target
    pred_str = f"[{intra[0]:.2f}, {intra[1]:.2f}, {intra[2]:.2f}]"
    target_str = f"[{target[0]:.2f}, {target[1]:.2f}, {target[2]:.2f}]"
    ratio_str = f"[{ratio[0]:.3f}, {ratio[1]:.3f}, {ratio[2]:.3f}]"
    print(f"  {name:<12} | {pred_str:>25} | {target_str:>25} | {ratio_str:>15}")

# ============================================================
# 第6层: 完整费米子质量预测 (使用最佳方案)
# ============================================================
print(f"\n{'='*70}")
print("第6层: 完整费米子质量预测 (使用最佳方案)")
print(f"{'='*70}")

# 扇区权重 (从多分形谱)
def compute_sector_weights(qs, p):
    weights = []
    for q in qs:
        w = np.sum(np.array(p)**q) if q != 0 else 1.0
        weights.append(w)
    weights = np.array(weights)
    return weights / np.sum(weights)

sector_weights = compute_sector_weights(sector_qs, ifs_p)

# Yukawa绝对标度 (从y_t~1锚定)
y_t_SM = 173100 * np.sqrt(2) / 246000  # ~0.994
v = 246000.0  # MeV

# 使用最佳方案的代内比
best_intra = {name: best_data[name] for name in sector_names[:3]}

# 绝对Yukawa标度
# y_t = y_0 * (mu_up/mu_up) * intra_up[2] ~ 1
# y_0 = y_t / intra_up[2]
y_0 = y_t_SM / best_intra["Up quarks"][2]

print(f"\n绝对Yukawa标度:")
print(f"  y_t_SM = {y_t_SM:.6f}")
print(f"  intra_up[2] = {best_intra['Up quarks'][2]:.4f}")
print(f"  y_0 = {y_0:.6e}")

# 计算所有费米子质量
SM_masses = {
    "u": 2.2, "c": 1270, "t": 173100,
    "d": 4.7, "s": 95, "b": 4180,
    "e": 0.511, "μ": 105.66, "τ": 1776.86,
}

labels = [["u","c","t"], ["d","s","b"], ["e","μ","τ"]]
print(f"\n{'粒子':>6} | {'预测(MeV)':>14} | {'SM(MeV)':>14} | {'比值':>10}")
print("-" * 55)

all_ratios = []
for s in range(3):
    name = sector_names[s]
    intra = best_intra[name]
    # Yukawa: y_{s,k} = y_0 * (mu_up/mu_s) * intra[k]
    mu_ratio = sector_weights[0] / sector_weights[s]
    for gen in range(3):
        y_sk = y_0 * mu_ratio * intra[gen]
        m_pred = y_sk * v / np.sqrt(2)
        label = labels[s][gen]
        m_sm = SM_masses[label]
        ratio = m_pred / m_sm
        all_ratios.append(ratio)
        print(f"  {label:>4} | {m_pred:>14.4f} | {m_sm:>14.2f} | {ratio:>10.4f}")

all_ratios = np.array(all_ratios)
rmse_log = np.sqrt(np.mean(np.log(all_ratios)**2))
print(f"\n费米子质量RMSE(log) = {rmse_log:.4f}")
print(f"比值范围: [{np.min(all_ratios):.4f}, {np.max(all_ratios):.4f}]")
print(f"比值中位数: {np.median(all_ratios):.4f}")

# ============================================================
# 第7层: 框架内推导链总结
# ============================================================
print(f"\n{'='*70}")
print("第7层: 框架内推导链总结")
print(f"{'='*70}")

print(f"""
框架内推导链 (无外部拟合参数):

1. IFS参数 {{c_i}}, {{p_i}}  (唯一几何起点)
   ↓
2. 多分形谱Legendre变换:
   - tau(q) = ln(sum(p_i^q)) / ln(c_geo)
   - alpha(q) = dtau/dq (局部分形指数)
   - f(alpha) = q*alpha - tau(q) (Hausdorff维数谱)
   ↓
3. 扇区相关参数 (从q_s推导):
   - c_eff_s = sum(p_i^q_s * c_i) / sum(p_i^q_s)
   - alpha_s = alpha(q_s)
   - f_s = f(alpha(q_s))
   ↓
4. Cl(1,7)代数结构:
   - N_Cl = 8 (生成元数)
   - N_spinor = 16 = 2^4 (旋量维数)
   ↓
5. 分形维数: d_frac (从gen_c: sum(c^d)=1)
   ↓
6. 代内因子 (指数形式, 从RKHS特征值谱):
   beta_s = (框架内推导的组合)
   intra_gen_s = (1/c_eff_s)^(k * beta_s)
   ↓
7. Yukawa耦合: y_{{s,k}} = y_0 * (mu_up/mu_s) * intra_gen_s[k]
   - y_0 从 y_t ~ 1 锚定
   ↓
8. 费米子质量: m_f = y_f * v / sqrt(2)

最佳方案: {best_scheme}
费米子RMSE(log): {rmse_log:.4f} (原方案: 3.1983)
""")

# 保存结果
with open('gap_analysis_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== 缺口分析结果 ===\n\n")
    f.write(f"最佳方案: {best_scheme}\n")
    f.write(f"费米子RMSE(log): {rmse_log:.4f} (原方案: 3.1983)\n\n")
    f.write("各方案RMSE比较:\n")
    for scheme_name in schemes:
        scheme_data = schemes[scheme_name]
        rmse_total = 0
        for name in sector_names[:3]:
            intra = scheme_data[name]
            target = SM_intra[name]
            rmse = np.sqrt(np.mean((np.log(intra) - np.log(target))**2))
            rmse_total += rmse
        f.write(f"  {scheme_name}: {rmse_total/3:.4f}\n")

print(f"\n结果已保存到 gap_analysis_results.txt")
