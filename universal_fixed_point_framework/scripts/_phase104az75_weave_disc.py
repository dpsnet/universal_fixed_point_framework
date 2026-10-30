# -*- coding: utf-8 -*-
"""
Phase 104az-75: 三织因子口径判别性预言 —— 闭合 104az-72 开放项
三口径：0.729000（登记 (b₀/10)³ = N_gen⁶/10³）/ 0.729135（paper17 a₀）/ 0.728234（不动点 a*）
判别维度：F_np 命中、m_s/T_c 自洽、d_eff 代数身份
关键检验：d_eff = (k_max²−2)/3 = 62/3 是否是代数身份？a₀(62/3) 是否 = 0.729135？
"""
import math

Nc = 3; Nf = 3; Ngen = 3; kmax = 8
sigma = 1/15
CF = (Nc**2 - 1)/(2*Nc)          # 4/3
delta = sigma**2 * CF / 4        # 1/675
dlmin = (math.sqrt(3) - 1) / 6   # 0.12200847
dl3 = math.sqrt(2) * dlmin       # 0.17254603
M_Pl_MeV = 1.2209e22
B0 = (Nc/2)**2                   # 9/4
rge3 = math.exp(-math.pi**2 * 2**B0)
rge3_Mpl = rge3 * M_Pl_MeV       # Λ 缺口的"基底"（F 的归一）
print(f"rge3·M_Pl = {rge3_Mpl:.4f} MeV")

# F 目标（Λ 双口径反推）
F_target_lo = 210.0 / rge3_Mpl
F_target_hi = 210.3 / rge3_Mpl
print(f"F 目标(Λ=210.0) = {F_target_lo:.5f}；F 目标(Λ=210.3) = {F_target_hi:.5f}")
print(f"登记目标 4.220 对应 Λ = {4.220*rge3_Mpl:.2f} MeV")

# ===== 三口径 =====
a_reg   = (9/10)**3                      # 0.729000 (b₀/10)³
a_p17   = 0.729135                       # paper17
a_fp    = 0.7282337805                   # 不动点
print(f"\n=== 三口径 a 值 ===")
print(f"登记 (b₀/10)³   = {a_reg:.9f}")
print(f"paper17 a₀      = {a_p17:.9f}  (vs 登记: {(a_p17/a_reg-1)*100:+.4f}%)")
print(f"不动点 a*       = {a_fp:.9f}  (vs 登记: {(a_fp/a_reg-1)*100:+.4f}%)")

def F_np(a): return a * (1-delta) / dl3
def msTc(a): return (CF/2)**2 / a

print(f"\n=== F_np 与 m_s/T_c 双检验 ===")
print(f"{'口径':<14}{'F_np':<12}{'F dev(210.0)':<14}{'F dev(4.220)':<14}{'m_s/T_c':<12}{'T_c dev(0.61)'}")
for name, a in [("登记", a_reg), ("paper17", a_p17), ("不动点", a_fp)]:
    F = F_np(a); ms = msTc(a)
    print(f"{name:<14}{F:<12.7f}{(F/F_target_lo-1)*100:+.4f}%      {(F/4.220-1)*100:+.4f}%      {ms:<12.6f}{(ms/0.61-1)*100:+.4f}%")

# ===== d_eff 代数身份检验 =====
print(f"\n=== d_eff 代数身份检验 ===")
# 反推各口径隐含的 d_eff：d_eff = 4πN_c·(Δλ₃/Δλ_min)·a³ = 12π·√2·a³
def d_implied(a): return 4*math.pi*Nc * (dl3/dlmin) * a**3
d_id = (kmax**2 - 2)/3                    # 62/3
print(f"代数身份 d_eff = (k_max²−2)/3 = {d_id:.6f}  [62 = 8²−2 = k_max²−2]")
for name, a in [("登记", a_reg), ("paper17", a_p17), ("不动点", a_fp)]:
    d = d_implied(a)
    print(f"  {name:<10} a={a:.6f} → d_eff = {d:.6f}  (vs 62/3: {(d/d_id-1)*100:+.4f}%)")

# 代数正推：a₀ = [(62/3)/(12π√2)]^(1/3)
a_from_id = ((d_id)/(4*math.pi*Nc) * (dlmin/dl3))**(1/3)
print(f"\n代数正推 a₀(62/3) = [(62/3)/(12π√2)]^(1/3) = {a_from_id:.9f}")
print(f"  vs paper17 0.729135: {(a_from_id/0.729135-1)*100:+.5f}%")
print(f"  vs 登记 0.729000:    {(a_from_id/a_reg-1)*100:+.5f}%")

# ===== 结构分解：为什么不动点偏离代数身份？ =====
print(f"\n=== 不动点偏离归因（结构 vs 身份） ===")
# 不动点处 d_eff(a*) 的组件（104az-72 结构）
Z2 = 1.44
dq_main = Nf*Nc*(CF/2)*math.sqrt(dlmin/dl3)*(1/Z2)
dds_fp = (CF/2) * math.exp(-msTc(a_fp)) * Nc
d_fp_struct = 16 + dq_main + dds_fp
print(f"不动点结构：16 + {dq_main:.6f}(d_q主项) + {dds_fp:.6f}(δd_s) = {d_fp_struct:.6f}")
print(f"  身份要求：{d_id:.6f} —— 差 {(d_fp_struct/d_id-1)*100:+.4f}%")
print(f"  若 δd_(s) 忽略且 d_q 主项取 paper17 近似 14/3：16 + {14/3:.4f} = {16+14/3:.4f} = 62/3 ✓（paper17 口径）")
print(f"  精确 d_q 主项 = {dq_main:.6f} ≠ 14/3（差 {(dq_main/(14/3)-1)*100:+.4f}%）——paper17 的 14/3 是近似")

# ===== m_s/T_c 自洽性"独立 vs 构造"判别 =====
print(f"\n=== m_s/T_c 自洽性性质判别 ===")
print(f"不动点方程构造：指数项 e^{{−(C_F/2)²/a}} 把 a 拉向使 m_s/T_c ≈ 0.61 的值——")
print(f"  不动点处 m_s/T_c = {msTc(a_fp):.6f}（+0.050%）→ 构造性自洽，非独立验证")
print(f"  代数口径 m_s/T_c = {msTc(a_reg):.6f}（{(msTc(a_reg)/0.61-1)*100:+.4f}%）→ 非构造，独立预言同样达标")

# ===== Λ 预测汇总 =====
print(f"\n=== Λ 预测（rge3·F·M_Pl）===")
for name, a in [("登记", a_reg), ("paper17", a_p17), ("不动点", a_fp)]:
    Lam = rge3_Mpl * F_np(a)
    print(f"  {name:<10} Λ_pred = {Lam:.3f} MeV (目标 210.0/210.3, dev {(Lam/210.0-1)*100:+.4f}%)")
