# -*- coding: utf-8 -*-
"""
Phase 104az-74: m_s 候选强子链交叉验证 —— 重子族 Σ/Ξ/Ω 质量判别
背景：note L2874 条件登记"m_s 框架化后重子族缺口判别可复用"；
104az-72 已框架化 m_s = Λ·4/9 = 93.431 MeV（+0.033% 候选）。
本脚本定向检验：重子质量差（八重态/十重态）与框架常数的对照，
确定重子族判别能达到的精度层级（模型天花板判定）。
"""
import math

# ===== 框架常数（KEY_FACTS） =====
Nc = 3; Nf = 3; Ngen = 3; kmax = 8
sigma = 1/15
CF = (Nc**2 - 1)/(2*Nc)        # 4/3
kappa = 6/math.pi
Lambda_lo, Lambda_hi = 210.0, 210.3   # 双口径
delta = sigma**2 * CF / 4      # 1/675
dlmin = (math.sqrt(3)-1)/6     # Δλ_min

# 框架质量
m_ud_fw = 3.44924              # 谱隙链框架值（note L493）
m_s_fw = Lambda_lo * 4/9       # m_s = Λ·(C_F/2)² 候选（Λ=210.0 口径）
m_s_fw_hi = Lambda_hi * 4/9    # Λ=210.3 口径
print(f"m_s 框架值 = Λ·4/9 = {m_s_fw:.4f} MeV（Λ=210.0）/ {m_s_fw_hi:.4f}（Λ=210.3）")
print(f"m_ud 框架值 = {m_ud_fw:.4f} MeV")
print(f"m_s/m_ud（框架） = {m_s_fw/m_ud_fw:.4f}")
print(f"  PDG 流质量比 93.4/3.45 = {93.4/3.45:.4f}")

# M_ud_eff（强子端有效 ud 质量）= m_ud + κΛ(1−2σ/3)
M_ud_eff = m_ud_fw + kappa*Lambda_lo*(1-2*sigma/3)
print(f"\nM_ud_eff = m_ud + κΛ(1−2σ/3) = {M_ud_eff:.3f} MeV（Λ=210.0）")

# ===== PDG 重子质量（2024） =====
M_N   = 938.92    # 核子平均 (p 938.272 + n 939.565)/2
M_Lam = 1115.683  # Λ
M_Sig = 1192.642  # Σ⁰
M_Xi  = 1314.86   # Ξ⁰
M_Om  = 1672.45   # Ω⁻
# 十重态
M_Del = 1232.0    # Δ
M_SigS= 1383.7    # Σ*(1385)
M_XiS = 1531.8    # Ξ*(1530)
print(f"\nPDG: N={M_N}, Λ={M_Lam}, Σ⁰={M_Sig}, Ξ⁰={M_Xi}, Ω⁻={M_Om}")
print(f"PDG 十重态: Δ={M_Del}, Σ*={M_SigS}, Ξ*={M_XiS}, Ω={M_Om}")

# ===== 1) 八重态质量差 vs 框架常数 =====
print("\n=== 1) 八重态质量差定向对照 ===")
# Σ−Λ 分裂（纯超精细，uds 组分相同——不含 s 流质量差）
d_SigLam = M_Sig - M_Lam
# m_N 缺口候选 κΛ(1−2σ/3)/5（P7-6d 倾向）
gap5 = kappa*Lambda_lo*(1-2*sigma/3)/5
print(f"Σ−Λ 分裂 = {d_SigLam:.3f} MeV（纯自旋超精细，与 m_s 无关）")
print(f"  vs κΛ(1−2σ/3)/5 = {gap5:.3f}：偏差 {(d_SigLam/gap5-1)*100:+.3f}%")

# Ξ−Σ 差（一个 s 替换 u，同超精细结构类）
d_XiSig = M_Xi - M_Sig
print(f"\nΞ−Σ = {d_XiSig:.3f} MeV（s 替换 u，八重态内）")
print(f"  vs m_s_fw = {m_s_fw:.3f}：偏差 {(d_XiSig/m_s_fw-1)*100:+.3f}%")
print(f"  vs m_s_fw·(1+2σ/3) = {m_s_fw*(1+2*sigma/3):.3f}：偏差 {(d_XiSig/(m_s_fw*(1+2*sigma/3))-1)*100:+.3f}%")

# Σ−N 差（一个 s 替换 u，但 Σ 与 N 超精细结构近似——八重态顶层）
d_SigN = M_Sig - M_N
print(f"\nΣ−N = {d_SigN:.3f} MeV")
print(f"  vs 2·κΛ(1−2σ/3)/5 = {2*gap5:.3f}：偏差 {(d_SigN/(2*gap5)-1)*100:+.3f}%")
print(f"  vs m_s_fw·(C_F/2)·3/2 = {m_s_fw*(CF/2)*1.5:.3f}：偏差 {(d_SigN/(m_s_fw*(CF/2)*1.5)-1)*100:+.3f}%")

# ===== 2) 十重态等间隔（经典组分质量差探针） =====
print("\n=== 2) 十重态等间隔 ===")
gaps = [M_SigS-M_Del, M_XiS-M_SigS, M_Om-M_XiS]
print(f"十重态间隔: Σ*−Δ={gaps[0]:.1f}, Ξ*−Σ*={gaps[1]:.1f}, Ω−Ξ*={gaps[2]:.1f} MeV")
print(f"平均间隔 = {sum(gaps)/3:.1f} MeV（= 组分质量差 m_s_eff−m_ud_eff 经典估计）")
print(f"流质量差 m_s−m_ud = {m_s_fw-m_ud_fw:.3f} MeV（dressing 味无关假设下的预言）")
print(f"→ 偏差 {(sum(gaps)/3)/(m_s_fw-m_ud_fw)-1:+.1%}：组分 dressing 强味相关（已知事实）")

# ===== 3) Ω 与框架组合 =====
print("\n=== 3) Ω/Ξ 与框架组合定向 ===")
# Ω−Ξ = 357.59：十重态与八重态间（含超精细结构差）
d_OmXi = M_Om - M_Xi
print(f"Ω−Ξ = {d_OmXi:.3f} MeV")
print(f"  vs m_s_fw·4 = {m_s_fw*4:.3f}：偏差 {(d_OmXi/(m_s_fw*4)-1)*100:+.3f}%")
print(f"  vs 2·(Σ*−Δ) = {2*gaps[0]:.1f}：偏差 {(d_OmXi/(2*gaps[0])-1)*100:+.3f}%")

# ===== 4) 模型天花板判定 =====
print("\n=== 4) 判别结论 ===")
print(f"Σ−Λ 分裂 vs 框架 gap5: {abs((d_SigLam/gap5-1)*100):.3f}% —— 方向性支持但超 0.1% 标准")
print(f"十重态等间隔平均 {sum(gaps)/3:.1f} vs 流质量差 {m_s_fw-m_ud_fw:.1f}：{abs(sum(gaps)/3/(m_s_fw-m_ud_fw)-1)*100:.0f}% —— 组分 dressing 味相关，非流质量直接探针")
print("→ 重子族在组分模型层面积累 ~1% 级破缺（GMO 破缺、超精细结构差），"
      "无法达到 0.1% 框架标准——模型天花板判定")
print("→ m_s 候选的强子链交叉验证：组分路径天花板限制，改由 m_s/T_c 自洽性（104az-72 +0.050%）"
      "与 m_s/m_ud 比值链（L782 +0.0186%）承担")
