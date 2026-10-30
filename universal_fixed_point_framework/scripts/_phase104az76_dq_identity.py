# -*- coding: utf-8 -*-
"""
Phase 104az-76: d_eff 结构组件身份化 —— 攻"为何 14/3"公理级推导
目标：d_q 主项与 δd_(s) 是否有精确框架身份，使结构组件之和的身份闭合
候选线索：d_q 主项 = 6·2^(−1/4)·(1/Z2) = 3.503735 vs (k_max−1)/2 + σ²·√(dlmin/dl3) = ?
"""
import math

Nc = 3; Nf = 3; Ngen = 3; kmax = 8
sigma = 1/15
CF = (Nc**2 - 1)/(2*Nc)
delta = sigma**2 * CF / 4
dlmin = (math.sqrt(3) - 1) / 6
dl3 = math.sqrt(2) * dlmin
Z2 = 1.44

# ===== 1) d_q 主项身份检验 =====
print("=== 1) d_q 主项框架身份 ===")
dq = Nf*Nc*(CF/2)*math.sqrt(dlmin/dl3)*(1/Z2)
print(f"d_q 主项 = Nf·Nc·(C_F/2)·√(dlmin/dl3)·(1/Z2) = {dq:.9f}")
print(f"  展开 = 6·2^(−1/4)·(25/36) = (25/6)·2^(−1/4) = {(25/6)*2**(-0.25):.9f}")

# 候选身份 A: (k_max−1)/2 + σ²·√(dlmin/dl3)
candA = (kmax-1)/2 + sigma**2 * math.sqrt(dlmin/dl3)
print(f"候选A (k_max−1)/2 + σ²·√(dlmin/dl3) = {candA:.9f}  dev {(dq/candA-1)*100:+.6f}%")
# 候选身份 B: 7/2 + σ²/15² 版本（σ²·2^(−1/4)）
candB = 7/2 + sigma**2 * 2**(-0.25)
print(f"候选B 7/2 + σ²·2^(−1/4) = {candB:.9f}  dev {(dq/candB-1)*100:+.6f}%")

# ===== 2) 反推 Z2*：若 d_q 身份 = 候选A，Z2 应为多少 =====
print(f"\n=== 2) Z2 身份互锁检验 ===")
Z2_star = 6*2**(-0.25)/candA
print(f"若 d_q = 候选A：Z2* = 6·2^(−1/4)/候选A = {Z2_star:.9f}")
print(f"  vs (6/5)² = {Z2:.9f}：dev {(Z2_star/Z2-1)*100:+.6f}%")
# 用 Z2 = (6/5)² 精确反推 d_q 与候选A 的残差
resid = (25/6)*2**(-0.25) - candA
print(f"(25/6)·2^(−1/4) − 候选A = {resid:.3e}（绝对）；相对 {(resid/candA)*100:+.6f}%")

# ===== 3) δd_(s) 身份候选 =====
print(f"\n=== 3) δd_(s) 身份候选（a₀ = 0.729135 处） ===")
a0 = 0.729135
dds = (CF/2)*math.exp(-(CF/2)**2/a0)*Nc
print(f"δd_(s) = 2·e^{{−4/(9a₀)}} = {dds:.9f}（m_s/T_c = {(CF/2)**2/a0:.6f}）")
cands_dds = {
    "1 + 5Δλ_min/7": 1 + 5*dlmin/7,
    "1 + Δλ_min·√3/2": 1 + dlmin*math.sqrt(3)/2,
    "1 + σ·4/3": 1 + sigma*4/3,
    "13/12": 13/12,
    "1 + (√3−1)/15": 1 + (math.sqrt(3)-1)/15,
    "1 + 2^(−1/4)/10": 1 + 2**(-0.25)/10,
}
for name, v in cands_dds.items():
    print(f"  候选 {name:<18} = {v:.9f}  dev {(dds/v-1)*100:+.4f}%")

# ===== 4) d_q + δd_(s) 联合身份判别 =====
print(f"\n=== 4) 非胶子部分联合身份判别 ===")
sum_dq_dds = dq + dds
print(f"d_q + δd_(s) = {sum_dq_dds:.9f}")
# 候选 1: 14/3（paper17 身份分解）
c1 = 14/3
# 候选 2: N_gen²/2 + 3Δλ_min/4
c2 = Ngen**2/2 + 3*dlmin/4
# 候选 3: (k_max²−2)/3 − 16（= 14/3 同）
print(f"  vs 14/3（paper17 身份分解）        = {c1:.9f}  dev {(sum_dq_dds/c1-1)*100:+.4f}%")
print(f"  vs N_gen²/2 + 3Δλ_min/4            = {c2:.9f}  dev {(sum_dq_dds/c2-1)*100:+.4f}%")
print(f"  vs 2(k_max−1)/3                    = {2*(kmax-1)/3:.9f}  dev {(sum_dq_dds/(2*(kmax-1)/3)-1)*100:+.4f}%")

# ===== 5) d_eff 结构 vs 身份张力 =====
print(f"\n=== 5) d_eff 结构身份 vs 62/3 身份 ===")
d_struct = 16 + dq + dds
d_id = (kmax**2 - 2)/3
print(f"结构 d_eff = 16 + {dq:.6f} + {dds:.6f} = {d_struct:.9f}")
print(f"身份 d_eff = (k_max²−2)/3 = {d_id:.9f}")
print(f"张力 = {(d_struct/d_id-1)*100:+.4f}%（若组件全精确身份化→0）")
# 若 d_q 用候选A、δd_(s) 保持：张力变化
d_struct2 = 16 + candA + dds
print(f"若 d_q 用候选A：d_eff = {d_struct2:.9f}  dev {(d_struct2/d_id-1)*100:+.4f}%")
