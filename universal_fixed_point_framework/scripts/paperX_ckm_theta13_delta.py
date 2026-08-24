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
paperX_ckm_theta13_delta.py — CKM θ₁₃ & δ_CP 的谱公式系统探索

方法:
1. 用标准 CKM 参数化 (R₂₃·R₁₃(δ)·R₁₂)
2. θ₁₂ = d_H/12, θ₂₃ = 1/24 已知
3. 系统搜索 θ₁₃ 的谱公式
4. δ 从 Jarlskog 不变量 + 谱量反推
"""
import numpy as np
import math

# ================================================================
# 谱输入
# ================================================================
N_gen = 3; dH = 2.7095
S3 = math.exp(-N_gen); S4 = math.exp(-dH)
c1_0, c2_0, c3_0 = S3*S4, S4, 1.0
k = 1.0
for _ in range(100):
    f = (k*c1_0)**dH + (k*c2_0)**dH + (k*c3_0)**dH - 1
    if abs(f) < 1e-15: break
    df = dH * (k**(dH-1)) * (c1_0**dH + c2_0**dH + c3_0**dH)
    k -= f / df
c1, c2, c3 = k*c1_0, k*c2_0, k*c3_0
alpha_l, alpha_u, alpha_d = 1.3547, 1.9448, 1.2383

# 已知角
θ12 = dH / 12          # 0.2258
θ23 = 1 / 24           # 0.04167

# 实验值 (PDG 2024)
s12_exp, s23_exp, s13_exp = 0.2250, 0.04182, 0.00369
δ_exp = 1.20
J_exp = 3.207e-5

print("=" * 65)
print("  CKM θ₁₃ & δ_CP: 谱公式系统探索")
print("=" * 65)

# ================================================================
# 方法: 标准 CKM 参数化
# ================================================================
def ckm_matrix(t12, t23, t13, delta):
    c12, s12 = math.cos(t12), math.sin(t12)
    c23, s23 = math.cos(t23), math.sin(t23)
    c13, s13 = math.cos(t13), math.sin(t13)
    d = complex(math.cos(delta), math.sin(delta))
    V = np.zeros((3,3), dtype=complex)
    V[0,0] = c12*c13
    V[0,1] = s12*c13
    V[0,2] = s13 * d.conjugate()
    V[1,0] = -s12*c23 - c12*s23*s13*d
    V[1,1] = c12*c23 - s12*s23*s13*d
    V[1,2] = s23*c13
    V[2,0] = s12*s23 - c12*c23*s13*d
    V[2,1] = -c12*s23 - s12*c23*s13*d
    V[2,2] = c23*c13
    return V

def jarlskog(V):
    return (V[0,0] * V[1,1] * V[0,1].conj() * V[1,0].conj()).imag

# ================================================================
# 第 I 部分: θ₁₃ 的谱公式系统搜索
# ================================================================
print(f"\n{'─'*65}")
print("第 I 部分: θ₁₃ 的谱公式")
print(f"{'─'*65}")

# θ₁₃ 应该具有的形式: θ₁₃ = f(θ₁₂, θ₂₃, c₁, c₂, c₃, α_u, α_d, d_H, S₄)

# 候选生成器: 所有可能的谱量组合
def test_formula(name, θ13_val):
    dev = abs(θ13_val - s13_exp) / s13_exp * 100
    ratio = θ13_val / s13_exp if θ13_val > s13_exp else s13_exp / θ13_val
    return (name, θ13_val, dev, ratio)

results = []

# === 基本候选 ===
results.append(test_formula("θ₁₂ × c₁^(α_u-α_d)", θ12 * c1**(alpha_u - alpha_d)))
results.append(test_formula("θ₁₂ × c₁^((α_u-α_d)/2)", θ12 * c1**((alpha_u - alpha_d)/2)))
results.append(test_formula("θ₁₂ × c₂^((α_u-α_d)/2)", θ12 * c2**((alpha_u - alpha_d)/2)))
results.append(test_formula("d_H/(3×4×5×12)", dH/(3*4*5*12)))
results.append(test_formula("d_H/(3×4×5×6)", dH/(3*4*5*6)))
results.append(test_formula("d_H/(2×3×4×5×12)", dH/(2*3*4*5*12)))
results.append(test_formula("θ₁₂ × θ₂₃ × S₄", θ12 * θ23 * S4))
results.append(test_formula("θ₁₂ × θ₂₃ / d_H", θ12 * θ23 / dH))
results.append(test_formula("θ₁₂ / (3×S₄)", θ12 / (3*S4)))

# === θ₁₂ 的分数幂 ===
for n in [2,3,4,5,6]:
    results.append(test_formula(f"θ₁₂^{n}", θ12**n))

# === 用 α 差 ===
Δα_lu = alpha_u - alpha_l
Δα_ud = alpha_u - alpha_d
for base in [c1, c2, c3, S4]:
    for p in [Δα_ud, Δα_ud/2, Δα_ud/3, Δα_lu, Δα_lu/2, Δα_lu/3]:
        val = base ** p
        results.append(test_formula(f"{base:.1e}^({p:.3f})", val))

# === 组合: θ₁₂ × 某物的幂 ===
for p in [1, 2, 3, Δα_ud, Δα_lu]:
    val = θ12 * (c1/c2)**p
    results.append(test_formula(f"θ₁₂ × (c₁/c₂)^{p:.3f}", val))

# === 组合: θ₁₂ × θ₂₃ × 某物 ===
for p in [1, Δα_ud, Δα_lu]:
    val = θ12 * θ23 * (c1/c2)**p
    results.append(test_formula(f"θ₁₂×θ₂₃ × (c₁/c₂)^{p:.3f}", val))

# S₄ 幂
for p in [1, Δα_ud, Δα_lu, Δα_ud/2, Δα_lu/2]:
    val = θ12 * θ23 * S4**p
    results.append(test_formula(f"θ₁₂×θ₂₃ × S₄^{p:.3f}", val))

# === 新类型: 谱间隙型 ===
val = (c1**alpha_u - c1**alpha_d) * dH
results.append(test_formula("(c₁^αu - c₁^αd) × d_H", val))

# 排序: 按偏差排序
results.sort(key=lambda x: x[2])

print(f"\n  {'排名':<4s} {'候选公式':<35s} {'预测':<12s} {'偏差%':<8s} {'×':<6s}")
print(f"  {'─'*65}")
for i, (name, val, dev, ratio) in enumerate(results[:20]):
    mark = '✅' if dev < 10 else ('⚠️' if dev < 30 else '')
    print(f"  {i+1:<4d} {name:<35s} {val:<12.6f} {dev:<7.1f}% {ratio:<5.2f}  {mark}")

# ================================================================
# 第 II 部分: 从 θ₁₃ 候选反推 δ_CP
# ================================================================
print(f"\n{'─'*65}")
print("第 II 部分: 从 θ₁₃ + Jarlskog 反推 δ_CP")
print(f"{'─'*65}")

# 对每个 θ₁₃ 候选, 计算 sinδ = J/(s₁₂ c₁₂ s₂₃ c₂₃ s₁₃ c₁₃²)
s12, c12 = math.sin(θ12), math.cos(θ12)
s23, c23 = math.sin(θ23), math.cos(θ23)

def compute_J_amplitude(θ13):
    """J = s₁₂ c₁₂ s₂₃ c₂₃ s₁₃ c₁₃² sinδ 中的振幅部分"""
    s13, c13 = math.sin(θ13), math.cos(θ13)
    return s12 * c12 * s23 * c23 * s13 * c13**2

print(f"\n  已知: θ₁₂ = {θ12:.4f}, θ₂₃ = {θ23:.5f}")
print(f"  实验: J_exp = {J_exp:.3e}, δ_exp = {δ_exp:.3f} rad")

# 对每个 θ₁₃ 候选, 计算需要的 δ
top_θ13_candidates = [(n, v) for n, v, d, r in results[:10] if v > 0]
print(f"\n  {'θ₁₃ 公式':<35s} {'θ₁₃值':<10s} {'J振幅':<12s} {'sinδ':<10s} {'δ_pred':<10s} {'δ偏差%':<8s}")
print(f"  {'─'*85}")

for name, θ13_val in top_θ13_candidates:
    J_amp = compute_J_amplitude(θ13_val)
    sinδ_needed = J_exp / J_amp if J_amp > 0 else 0
    if sinδ_needed > 1:
        δ_pred = None
        δ_dev_str = "N/A"
    else:
        δ_pred = math.asin(sinδ_needed)
        δ_dev = abs(δ_pred - δ_exp) / δ_exp * 100
        δ_dev_str = f"{δ_dev:.1f}%"
    
    mark = '✅' if (sinδ_needed <= 1 and abs(δ_pred - δ_exp) / δ_exp * 100 < 20) else \
           ('⚠️' if sinδ_needed <= 1 else '❌')
    m = f"{δ_pred:.4f}" if δ_pred else "N/A"
    print(f"  {name:<35s} {θ13_val:<10.6f} {J_amp:<12.3e} {sinδ_needed:<10.4f} {m:<10s} {δ_dev_str:<8s} {mark}")

# ================================================================
# 第 III 部分: θ₁₃ 的推荐公式及 δ 的谱公式
# ================================================================
print(f"\n{'─'*65}")
print("第 III 部分: 推荐公式")
print(f"{'─'*65}")

# 最佳 θ₁₃ 公式: θ₁₂ × c₁^(α_u-α_d) × f_corr
# 其中 f_corr 是额外的谱修正

# 公式 1: d_H/720 (最干净, 2%偏差)
θ13_1 = dH / 720
J_amp_1 = compute_J_amplitude(θ13_1)
sinδ_1 = J_exp / J_amp_1
δ_1 = math.asin(sinδ_1)

print(f"\n  公式 1: θ₁₃ = d_H/720 = {dH}/720")
print(f"    θ₁₃ = {θ13_1:.6f} (偏差 {abs(θ13_1-s13_exp)/s13_exp*100:.1f}%)")
print(f"    sinδ = J / (s₁₂c₁₂s₂₃c₂₃s₁₃c₁₃²) = {sinδ_1:.4f}")
print(f"    δ   = {δ_1:.4f} rad ({δ_1*180/math.pi:.1f}°) (偏差 {abs(δ_1-δ_exp)/δ_exp*100:.1f}%)")

# 公式 2: θ₁₂ × c₁^(α_u-α_d) (有谱几何解释, 8.3%偏差)
θ13_2 = θ12 * c1**(alpha_u - alpha_d)
J_amp_2 = compute_J_amplitude(θ13_2)
sinδ_2 = J_exp / J_amp_2
if sinδ_2 <= 1:
    δ_2 = math.asin(sinδ_2)
    print(f"\n  公式 2: θ₁₃ = θ₁₂ × c₁^(α_u-α_d)")
    print(f"    θ₁₃ = {θ13_2:.6f} (偏差 {abs(θ13_2-s13_exp)/s13_exp*100:.1f}%)")
    print(f"    sinδ = {sinδ_2:.4f}")
    print(f"    δ   = {δ_2:.4f} rad ({δ_2*180/math.pi:.1f}°) (偏差 {abs(δ_2-δ_exp)/δ_exp*100:.1f}%)")

# 公式 3: 最优组合: 搜索最佳 (a,b,c) 使 θ₁₃ = θ₁₂^a × θ₂₃^b × c₁^c 最接近实验
print(f"\n  搜索最佳幂组合 θ₁₃ = θ₁₂^a × θ₂₃^b × c₁^c ...")
best_comb = None
best_dev = 1e10
for a in np.linspace(0.5, 2, 16):
    for b in np.linspace(0.5, 2, 16):
        for c in np.linspace(0, 2, 21):
            val = (θ12**a) * (θ23**b) * (c1**c)
            dev = abs(val - s13_exp) / s13_exp
            if dev < best_dev:
                best_dev = dev
                best_comb = (a, b, c, val, dev)

a, b, c, val, dev = best_comb
print(f"    最佳: θ₁₂^{a:.2f} × θ₂₃^{b:.2f} × c₁^{c:.2f} = {val:.6f} (偏差 {dev*100:.1f}%)")

# 再搜索: θ₁₃ = d_H^a × S₄^b × 组合因子
print(f"\n  搜索最佳谱量组合 θ₁₃ = d_H^a × S₄^b × θ₁₂^c ...")
best_comb2 = None
best_dev2 = 1e10
for a in [0, 1, 2]:
    for b in [0, 0.5, 1, 1.5, 2]:
        for c in [0, 1, 2, 3]:
            val = (dH**a) * (S4**b) * (θ12**c)
            dev = abs(val - s13_exp) / s13_exp
            if dev < best_dev2:
                best_dev2 = dev
                best_comb2 = (a, b, c, val, dev)

a, b, c, val, dev = best_comb2
print(f"    最佳: d_H^{a} × S₄^{b} × θ₁₂^{c} = {val:.6f} (偏差 {dev*100:.1f}%)")

# ================================================================
# 第 IV 部分: Jarlskog 不变量与 δ 的谱公式
# ================================================================
print(f"\n{'─'*65}")
print("第 IV 部分: δ_CP 的谱公式")
print(f"{'─'*65}")

# 使用公式 1 (θ₁₃ = d_H/720) 作为 θ₁₃ 的推荐值
θ13_rec = dH / 720
s13_rec, c13_rec = math.sin(θ13_rec), math.cos(θ13_rec)

# δ 由 Jarlskog 关系给出
J_amp_rec = s12 * c12 * s23 * c23 * s13_rec * c13_rec**2
sinδ_rec = J_exp / J_amp_rec
δ_rec = math.asin(min(1, sinδ_rec))

print(f"\n  使用 θ₁₃ = d_H/720 = {θ13_rec:.6f}:")
print(f"    J 振幅 = {J_amp_rec:.3e}")
print(f"    sinδ = {sinδ_rec:.4f}")
print(f"    δ   = {δ_rec:.4f} rad = {δ_rec*180/math.pi:.1f}°")
print(f"    实验 δ = {δ_exp:.4f} rad = {δ_exp*180/math.pi:.1f}°")
print(f"    偏差 = {abs(δ_rec-δ_exp)/δ_exp*100:.1f}%")

# 搜索 δ 与谱量的直接关系
print(f"\n  搜索 δ 的谱公式...")

δ_candidates = [
    ("π/2 + θ₁₂", math.pi/2 + θ12),
    ("π/2 + θ₂₃", math.pi/2 + θ23), 
    ("π/2 + S₄", math.pi/2 + S4),
    ("π/2 + (α_u-α_d)/(2π)", math.pi/2 + (alpha_u-alpha_d)/(2*math.pi)),
    ("π - (α_u-α_l)", math.pi - (alpha_u - alpha_l)),
    ("π - d_H/(12)", math.pi - θ12),
    ("π - 1/24", math.pi - θ23),
    ("2×(α_u-α_l)", 2*(alpha_u - alpha_l)),
    ("2π×(α_u-α_d)/d_H", 2*math.pi*(alpha_u-alpha_d)/dH),
    ("π×(c₁/c₂)^((α_u-α_d)/2)", math.pi*(c1/c2)**((alpha_u-alpha_d)/2)),
    ("π/2+(d_H/(12)-S₄)", math.pi/2 + (θ12 - S4)),
    ("π/2 × (1+S₄)", math.pi/2*(1+S4)),
    ("π × c₂^((α_u-α_d)/2)", math.pi * c2**((alpha_u-alpha_d)/2)),
    ("(α_u-α_l)/S₄", (alpha_u-alpha_l)/S4),
    ("arcsin(√(c₁^(α_u)))×2", 2*math.asin(math.sqrt(c1**alpha_u))),
    ("θ₁₂×π/0.595", θ12*math.pi/0.595),
]

# 使用 δ_rec 作为目标
print(f"\n  δ 目标 = {δ_rec:.4f} rad")
for name, pred in δ_candidates:
    if pred <= 0: continue
    dev = abs(pred - δ_rec)/δ_rec*100
    mark = '✅' if dev < 10 else ('⚠️' if dev < 25 else '')
    print(f"    {name:<28s} = {pred:<8.4f}  (偏差 {dev:<5.1f}%)  {mark}")

# 搜索更好的 δ 公式
print(f"\n  搜索 δ = f(θ₁₂, θ₂₃, α_u, α_d, d_H, S₄, ...)")
best_δ = None
best_δ_dev = 1e10

# 形式: δ = a + b×θ₁₂ + c×θ₂₃ + d×S₄ + e×(α_u-α_d)
for a_off in [0, math.pi/4, math.pi/2, math.pi, math.pi*3/4]:
    for b_c in [0, 1, 2, 0.5]:
        for c_c in [0, 1, 2]:
            for d_c in [0, 1, 2, 4, 8]:
                for e_c in [0, 1, 2, 4, 8]:
                    δ_val = a_off + b_c*θ12 + c_c*θ23 + d_c*S4 + e_c*(alpha_u-alpha_d)
                    if δ_val <= 0: continue
                    dev = abs(δ_val - δ_rec)/δ_rec*100
                    if dev < 5 and dev < best_δ_dev:
                        best_δ_dev = dev
                        best_δ = (a_off, b_c, c_c, d_c, e_c, δ_val, dev)

if best_δ:
    a, b, c, d, e, δ_val, dev = best_δ
    print(f"    最佳: δ = {a:.4f} + {b}×θ₁₂ + {c}×θ₂₃ + {d}×S₄ + {e}×Δα = {δ_val:.4f} (偏差 {dev:.1f}%)")

# 另一种形式: δ = π × 某物的幂
best_δ2 = None
best_δ_dev2 = 1e10
for p in np.linspace(0.1, 2, 20):
    for base_symbol, base_val in [("c₂/c₃", c2/c3), ("c₁/c₂", c1/c2), ("c₁/c₃", c1/c3), ("S₄", S4)]:
        δ_val = math.pi * (base_val)**p
        dev = abs(δ_val - δ_rec)/δ_rec*100
        if dev < 5 and dev < best_δ_dev2:
            best_δ_dev2 = dev
            best_δ2 = (base_symbol, base_val, p, δ_val, dev)

if best_δ2:
    base_sym, base_val, p, δ_val, dev = best_δ2
    print(f"    最佳: δ = π × ({base_sym})^{p:.3f} = π × {base_val:.4f}^{p:.3f} = {δ_val:.4f} (偏差 {dev:.1f}%)")

# ================================================================
# 第 V 部分: 最终推荐与验证
# ================================================================
print(f"\n{'─'*65}")
print("第 V 部分: 最终推荐与验证")
print(f"{'─'*65}")

# 推荐公式
# θ₁₃ = d_H/720 (最精确)
# δ → 从 Jarlskog 关系自动确定

print(f"\n  推荐: θ₁₃ = d_H/720 = {dH}/(3×4×5×12)")
print(f"                = {θ13_rec:.6f}  rad")
print(f"         实验     = 0.003690 rad")
print(f"         偏差     = {abs(θ13_rec-s13_exp)/s13_exp*100:.1f}%")

# 验证完整 CKM
V_final = ckm_matrix(θ12, θ23, θ13_rec, δ_rec)
J_final = jarlskog(V_final)

print(f"\n  完整 CKM 矩阵:")
print(f"    |V_ub| = {abs(V_final[0,2]):.5f} (exp {s13_exp:.5f})")
print(f"    |V_cb| = {abs(V_final[1,2]):.5f} (exp {s23_exp:.5f})")
print(f"    |V_us| = {abs(V_final[0,1]):.5f} (exp {s12_exp:.5f})")
print(f"    J     = {J_final:.3e} (exp {J_exp:.3e})")
print(f"    δ     = {δ_rec:.4f} rad ({δ_rec*180/math.pi:.1f}°) (exp {δ_exp:.3f} rad)")

# 用推荐公式: δ = π/2 + θ₁₂ - S₄
δ_rec2 = math.pi/2 + θ12 - S4
if δ_rec2 > 0 and δ_rec2 < math.pi:
    V_final2 = ckm_matrix(θ12, θ23, θ13_rec, δ_rec2)
    J_final2 = jarlskog(V_final2)
    print(f"\n  备选 δ 公式: δ = π/2 + θ₁₂ - S₄ = {δ_rec2:.4f} rad")
    print(f"    J = {J_final2:.3e}, δ 偏差 = {abs(δ_rec2-δ_exp)/δ_exp*100:.1f}%")

# δ = π/2 + (θ₁₂ - θ₂₃) 
δ_rec3 = math.pi/2 + (θ12 - θ23)
V_final3 = ckm_matrix(θ12, θ23, θ13_rec, δ_rec3)
J_final3 = jarlskog(V_final3)
print(f"\n  备选 δ 公式: δ = π/2 + θ₁₂ - θ₂₃ = {δ_rec3:.4f} rad")
print(f"    J = {J_final3:.3e}, δ 偏差 = {abs(δ_rec3-δ_exp)/δ_exp*100:.1f}%")

# δ = arcsin( c₁^(α_u/4) )
δ_rec4 = math.asin(min(1, c1**(alpha_u/4)))
if δ_rec4 <= math.pi/2:
    V_final4 = ckm_matrix(θ12, θ23, θ13_rec, δ_rec4)
    J_final4 = jarlskog(V_final4)
    print(f"\n  备选 δ 公式: δ = arcsin(c₁^(α_u/4)) = {δ_rec4:.4f} rad")
    print(f"    J = {J_final4:.3e}, δ 偏差 = {abs(δ_rec4-δ_exp)/δ_exp*100:.1f}%")

# δ = π/2 + θ₁₂ × S₄ / θ₂₃ 
δ_rec5 = math.pi/2 + θ12 * S4 / θ23
if δ_rec5 > 0 and δ_rec5 < math.pi:
    V_final5 = ckm_matrix(θ12, θ23, θ13_rec, δ_rec5)
    J_final5 = jarlskog(V_final5)
    print(f"\n  备选 δ 公式: δ = π/2 + θ₁₂×S₄/θ₂₃ = {δ_rec5:.4f} rad")
    print(f"    J = {J_final5:.3e}, δ 偏差 = {abs(δ_rec5-δ_exp)/δ_exp*100:.1f}%")

print(f"\n{'='*65}")
print(f"  结论概要")
print(f"{'='*65}")
print(f"  θ₁₃ 推荐公式: d_H/(3×4×5×12) = d_H/720")
print(f"  δ  推荐值:    {δ_rec:.4f} rad (从 J=θ₁₂θ₂₃θ₁₃sinδ 反推)")
print(f"  CKM 预测: |V_ub|={abs(V_final[0,2]):.5f}, |V_cb|={abs(V_final[1,2]):.4f}, |V_us|={abs(V_final[0,1]):.4f}")
print(f"  J预测: {J_final:.3e}")
