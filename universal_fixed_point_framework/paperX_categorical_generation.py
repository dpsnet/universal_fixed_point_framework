"""
范畴框架 → 三代收缩因子 {c₁,c₂,c₃} 第一原理推导
===============================================
核心思想：三代对应 Rec 范畴中 IFS 的三个不同递归深度，
收缩因子由多重静默的层级压制决定。
"""
import numpy as np

# ============================================================
# 核心范畴思想
# ============================================================
# 在 4-范畴 Spec 中，IFS 有三层递归深度：
#   深度 0: 不动点本身 (f_3) — 无压制 → c₃ ≈ 1
#   深度 1: 一次递归 (f_2) — 受 S₄ (辫子静默) 压制
#   深度 2: 二次递归 (f_1) — 受 S₃·S₄ 联合压制
#
# 多重静默因子 (Paper IX §6):
#   S₃ (对象静默) = e^{-N_gen} = e^{-3} ≈ 0.0498
#   S₄ (辫子静默) = e^{-d_H} = e^{-2.7095} ≈ 0.0664
#   d_H = 2.7095 (来自 D-C 定理 + ρ=0)

print("=" * 65)
print("范畴递归深度模型：三代质量层级的第一原理推导")
print("=" * 65)

# ============================================================
# 静默因子
# ============================================================
N_gen = 3
d_H = 2.7095  # Hausdorff dimension from D-C theorem + ρ=0

S3 = np.exp(-N_gen)     # 对象静默: e^{-3}
S4 = np.exp(-d_H)       # 辫子静默: e^{-d_H}

print(f"\nS₃ (对象静默) = e^(-{N_gen}) = {S3:.6f}")
print(f"S₄ (辫子静默) = e^(-{d_H}) = {S4:.6f}")
print(f"S₃·S₄ = {S3*S4:.6f}")

# ============================================================
# 深度压制
# ============================================================
# 在 Rec 范畴中，递归系统 R = (X, F) 的谱像 
# D(R) = (ℋ, A, σ(A)) 具有三层不动点子结构。
#
# 第 k 层深度对应的压制因子 = ∏ (第 j 层静默) for j < k
#
# 设三个递归深度对应的原始收缩因子未经压制的比例为 1:1:1
# (Cl(1,7) 代数简并，之前已确认),
# 压制后:
#   深度 0 (第三代): c₃₀ = 1       — 无压制
#   深度 1 (第二代): c₂₀ = S₄      — 一次辫子压制
#   深度 2 (第一代): c₁₀ = S₃·S₄  — 对象+辫子联合压制

c_raw = np.array([S3 * S4, S4, 1.0])
print(f"\n未归一化收缩因子比 c₁₀:c₂₀:c₃₀ = {np.round(c_raw, 6)}")

# ============================================================
# Moran 方程确定绝对标度
# ============================================================
# Σ(c_i)^d = 1, 其中 c_i = k · c_i₀

sum_c_raw_d = np.sum(c_raw ** d_H)
k = sum_c_raw_d ** (-1.0/d_H)
c = k * c_raw

print(f"\nMoran 标度因子 k = {k:.6f}")
print(f"\n--- 第一原理收缩因子 ---")
for i, ci in enumerate(c):
    print(f"  c_{i+1} = {ci:.6f}")

moran_check = np.sum(c ** d_H)
print(f"Moran 方程验证 Σc_i^d = {moran_check:.8f} (应为 1)")

# ============================================================
# 质量预测
# ============================================================
# 在 IFS 中，质量 m_i ∝ c_i^α
# α 由 IFS 的几何结构决定: α = d_H (对点状吸引子)
# 或 α = 4 (对 4D 时空传播子)

print(f"\n" + "-" * 65)
print("质量比预测 (m₁=m_u, m₂=m_c, m₃=m_t)")
print("-" * 65)

# 实验值 (归一化到 m_t)
exp_mass = np.array([2.2e-3, 1.27, 172.69])  # MeV, GeV, GeV
exp_ratios = exp_mass / exp_mass[2]
print(f"实验值: m_u/m_t={exp_ratios[0]:.6e}, m_c/m_t={exp_ratios[1]:.6f}")

c_norm = c / c[2]  # normalize to heaviest

# 尝试不同的 α 值
print(f"\n不同 α 的预测:")
for alpha in [d_H, 4.0, 5.0, 6.0, 3.0]:
    pred = c_norm ** alpha
    print(f"  α={alpha:.1f}: m_u/m_t={pred[0]:.6e}, m_c/m_t={pred[1]:.6f}")

# 扫描最佳 α
best_alpha = None
best_err = float('inf')
for alpha in np.linspace(0.1, 15.0, 1491):
    pred = c_norm ** alpha
    # 对数空间误差 (mass hierarchy is logarithmic)
    err = np.sum((np.log10(pred) - np.log10(exp_ratios))**2)
    if err < best_err:
        best_err = err
        best_alpha = alpha

print(f"\n最佳 α = {best_alpha:.2f} (对数空间 RMSE = {np.sqrt(best_err/3):.4f})")
pred_best = c_norm ** best_alpha
print(f"  m_u/m_t = {pred_best[0]:.6e} (exp={exp_ratios[0]:.6e})")
print(f"  m_c/m_t = {pred_best[1]:.6f} (exp={exp_ratios[1]:.6f})")

# ============================================================
# 方案二：使用谱动力学中谱流方程的不动点结构
# ============================================================
# 谱流方程 dA_t/dt = [G, A_t] 在三种力下的三个不同不动点
# 分别对应三代质量。
#
# A_GR (引力) → 第三代质量标度 (Planck scale)
# A_EM (电磁) → 第二代质量标度 (electroweak scale)
# A_weak (弱力) → 第一代质量标度 (QCD scale)
#
# 质量比 = 谱生成元的 Hilbert-Schmidt 范数比

print(f"\n" + "=" * 65)
print("方案二：谱流不动点层级")
print("=" * 65)

# 四个力的谱间隙 (Paper XI 附录 C):
# Δλ_GR = 0.122 M_Pl
# Δλ_EM = Δλ_GR · √(2/3) ≈ 0.0996 M_Pl
# Δλ_strong = Δλ_GR · √2 ≈ 0.1725 M_Pl
# Δλ_weak = Δλ_GR (参考)
#
# 三代对应三个力的谱间隙在电弱标度的投影

dl_GR = 0.122
dl_EM = dl_GR * np.sqrt(2/3)
dl_strong = dl_GR * np.sqrt(2)
dl_weak = dl_GR * 1.0

# 质量 ∝ 谱间隙^β
print(f"\n谱间隙:")
print(f"  Δλ_GR = {dl_GR:.4f}")
print(f"  Δλ_EM = {dl_EM:.4f}")
print(f"  Δλ_strong = {dl_strong:.4f}")

# 将三代与三个力的谱间隙关联
# 第三代 (顶) ∝ Δλ_GR (最强)
# 第二代 (粲) ∝ Δλ_EM (中等)  
# 第一代 (上) ∝ Δλ_weak (最弱)

c_force = np.array([dl_weak, dl_EM, dl_GR])
c_force_norm = c_force / c_force[2]

print(f"\n力的谱间隙比 (归一化到 GR):")
print(f"  Δλ_weak/Δλ_GR = {c_force_norm[0]:.4f}")
print(f"  Δλ_EM/Δλ_GR = {c_force_norm[1]:.4f}")
print(f"  Δλ_GR/Δλ_GR = {c_force_norm[2]:.4f}")

print(f"\n质量预测 (m ∝ Δλ^β):")
for beta in [1.0, 2.0, 3.0, d_H]:
    pred = c_force_norm ** beta
    print(f"  β={beta:.1f}: m_u/m_t={pred[0]:.4e}, m_c/m_t={pred[1]:.4f}")

print(f"实验: m_u/m_t={exp_ratios[0]:.4e}, m_c/m_t={exp_ratios[1]:.4f}")

# ============================================================
# 方案三：复合模型 — 递归深度 × 谱间隙
# ============================================================
# 三代 = 递归深度压制 (方案一) × 力的谱间隙 (方案二)
# 物理图像: 每代 IFS 吸引子由不同力驱动

print(f"\n" + "=" * 65)
print("方案三：复合模型 — 递归深度 × 谱间隙")
print("=" * 65)

c_composite = c_force * c_raw  # element-wise product
c_composite_norm = c_composite / c_composite[2]

print(f"\n复合收缩因子比:")
for i, ci in enumerate(c_composite_norm):
    print(f"  c_{i+1}/c₃ = {ci:.6e}")

for alpha in [1.0, 2.0, 3.0, 4.0]:
    pred = c_composite_norm ** alpha
    print(f"  α={alpha:.1f}: m_u/m_t={pred[0]:.4e}, m_c/m_t={pred[1]:.4f}")

print(f"实验: m_u/m_t={exp_ratios[0]:.4e}, m_c/m_t={exp_ratios[1]:.4f}")

# ============================================================
# 方案四：BCH 展开高阶效应
# ============================================================
# 谱流对易子 [A_GR, A_SM] 的 BCH 展开产生层级。
# 三代对应 BCH 展开的不同阶:
#   Generation 3: 0 阶 (A_GR 本身)
#   Generation 2: 1 阶 [A_GR, A_EM]  
#   Generation 1: 2 阶 [A_GR, [A_GR, A_EM]]

print(f"\n" + "=" * 65)
print("方案四：BCH 展开高阶效应")
print("=" * 65)

# BCH 展开: e^X e^Y = e^{X+Y+[X,Y]/2+...}
# 收缩因子 ∝ 1/n! 或 ∝ ||[A,...]||_HS

# 在 Spec 中，对易子范数 ∝ 谱间隙
# ||[A_GR, A_EM]||_HS ∝ Δλ_GR · Δλ_EM
bch_0 = dl_GR
bch_1 = dl_GR * dl_EM
bch_2 = dl_GR**2 * dl_EM

c_bch = np.array([bch_2, bch_1, bch_0])
c_bch_norm = c_bch / c_bch[2]

print(f"\nBCH 层级比:")
for i, ci in enumerate(c_bch_norm):
    print(f"  c_{i+1}/c₃ = {ci:.6e}")

for alpha in [0.5, 1.0, 2.0, d_H/2]:
    pred = c_bch_norm ** alpha
    print(f"  α={alpha:.1f}: m_u/m_t={pred[0]:.4e}, m_c/m_t={pred[1]:.4f}")

print(f"实验: m_u/m_t={exp_ratios[0]:.4e}, m_c/m_t={exp_ratios[1]:.4f}")

# ============================================================
# 总结
# ============================================================
print(f"\n" + "=" * 65)
print("综合比较")
print("=" * 65)

results = {}
# 方案一：递归深度
pred1 = (c / c[2]) ** best_alpha
results['递归深度 (静默层级)'] = {'mc_mt': pred1[1], 'mu_mt': pred1[0], 'α': best_alpha}

# 方案二：谱间隙
best_beta = None
best_err = float('inf')
for beta in np.linspace(0.1, 15, 1491):
    pred = c_force_norm ** beta
    err = np.sum((np.log10(pred) - np.log10(exp_ratios))**2)
    if err < best_err:
        best_err = err
        best_beta = beta
pred2 = c_force_norm ** best_beta
results['谱流不动点 (力的层级)'] = {'mc_mt': pred2[1], 'mu_mt': pred2[0], 'β': best_beta}

# 方案三：复合
best_alpha3 = None
best_err = float('inf')
for alpha in np.linspace(0.1, 15, 1491):
    pred = c_composite_norm ** alpha
    err = np.sum((np.log10(pred) - np.log10(exp_ratios))**2)
    if err < best_err:
        best_err = err
        best_alpha3 = alpha
pred3 = c_composite_norm ** best_alpha3
results['复合 (深度×谱间隙)'] = {'mc_mt': pred3[1], 'mu_mt': pred3[0], 'α': best_alpha3}

# 方案四：BCH
best_alpha4 = None
best_err = float('inf')
for alpha in np.linspace(0.1, 15, 1491):
    pred = c_bch_norm ** alpha
    err = np.sum((np.log10(pred) - np.log10(exp_ratios))**2)
    if err < best_err:
        best_err = err
        best_alpha4 = alpha
pred4 = c_bch_norm ** best_alpha4
results['BCH 展开 (对易子层级)'] = {'mc_mt': pred4[1], 'mu_mt': pred4[0], 'α': best_alpha4}

print(f"\n{'方案':<25} {'m_c/m_t':<15} {'m_u/m_t':<15} {'最佳指数':<10}")
print("-" * 65)
for name, vals in results.items():
    print(f"{name:<25} {vals['mc_mt']:<15.6f} {vals['mu_mt']:<15.2e} {vals.get('α', vals.get('β', 0)):<10.2f}")
print(f"{'实验值':<25} {exp_ratios[1]:<15.6f} {exp_ratios[0]:<15.2e} {'—':<10}")
