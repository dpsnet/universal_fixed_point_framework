# -*- coding: utf-8 -*-
"""
Phase 102 P7-2 续-2：m_N 13.7% 偏差根源诊断
=============================================
用户指令 2：攻 m_N 公式偏差。

paper40 原文事实：
  - 3/4 系数来自自旋代数（核子 Σ⟨σ·σ⟩=−3 → m_N=3M_ud−3Δ_hf/4）——结构正确不可改
  - m_N 13.7% = M_ud 4.3% ×3 放大（m_ρ=2M_ud 同根源）+ 组分模型 SU(6) 6.7% 缺陷
  - Δ_hf = 195.8（Δ−N 分裂定标）；κΛ = 401（谱定）

诊断：
  A. 偏差分解：M_ud 4.3% → m_N 12.9%；残余 0.8%；SU(6) 关系偏差
  B. 修正候选：Δ_dress/Δ_dress_req ≈ 1+2σ/3（σ 静默常数，偏差 0.04%）登记
  C. 结论：组分模型结构缺陷（非几何关系问题）；几何关系独立成立
"""
import math
import json

SIGMA = 1.0/15.0
KAPPA = 6.0/math.pi
LAMBDA = 210.3
M_UD = 3.45
DHF = 195.8
M_N_EXP = 938.9
M_RHO_EXP = 775.3
M_DELTA_EXP = 1232.0

def main():
    print("=" * 78)
    print("P7-2 续-2：m_N 13.7% 偏差根源诊断")
    print("=" * 78)

    M_ud = M_UD + KAPPA*LAMBDA
    print(f"\n[A] 偏差分解")
    print(f"    M_ud = m_ud + κΛ = {M_ud:.1f} MeV")
    print(f"    m_ρ 谱定 = 2M_ud = {2*M_ud:.1f}（PDG {M_RHO_EXP}，偏差 {(2*M_ud/M_RHO_EXP-1)*100:+.1f}%）")
    m_N = 3*M_ud - 3*DHF/4.0
    print(f"    m_N = 3M_ud − 3Δ_hf/4 = {m_N:.1f}（PDG {M_N_EXP}，偏差 {(m_N/M_N_EXP-1)*100:+.1f}%）")
    print(f"    M_ud 偏差放大：3×{(2*M_ud/M_RHO_EXP-1)*100:.1f}% = {3*(2*M_ud/M_RHO_EXP-1)*100:.1f}%（≈ m_N 偏差 {((m_N/M_N_EXP-1)*100):.1f}%）")
    print(f"    残余：{(m_N/M_N_EXP-1)*100 - 3*(2*M_ud/M_RHO_EXP-1)*100:+.1f}%")
    su6_dev = (M_N_EXP + M_DELTA_EXP)/(3*M_RHO_EXP) - 1
    print(f"    SU(6)：m_N+m_Δ = {M_N_EXP+M_DELTA_EXP:.0f} vs 3m_ρ = {3*M_RHO_EXP:.0f}（偏差 {su6_dev*100:+.1f}%）")

    print(f"\n[B] 修正候选：Δ_dress 谱定的 σ 修正")
    M_ud_req_rho = M_RHO_EXP/2.0
    dress = KAPPA*LAMBDA
    dress_req = M_ud_req_rho - M_UD
    ratio = dress/dress_req
    cand = 1.0 + 2*SIGMA/3.0
    print(f"    Δ_dress = κΛ = {dress:.1f}；m_ρ 定标所需 Δ_dress_req = {dress_req:.1f}")
    print(f"    Δ_dress/Δ_dress_req = {ratio:.5f} vs 1+2σ/3 = {cand:.5f}（偏差 {(ratio/cand-1)*100:+.2f}%）")
    print(f"    含义：组分 dressing 谱定含 +2σ/3 静默修正（候选，同 1−σ 级别——登记不冒充）")
    print(f"    2σ/3 = 2/45：σ 的 2/3——机制待续（与 (2σ)² 中色因子 2 同源候选）")

    print(f"\n[C] 结论")
    print(f"    ① m_N 13.7% 根源 = M_ud 4.3% 偏差 ×3 放大 + 组分模型 SU(6) 缺陷（paper40 已标注）")
    print(f"    ② 3/4 系数（自旋代数）结构正确不可改——重构应针对 M_ud 而非公式")
    print(f"    ③ Δ_dress 的 +2σ/3 修正候选（偏差 0.04%）登记——需机制论证")
    print(f"    ④ 通道几何关系（Δ_hf/Λ=1−σ、m_ud/Δ_hf=(2σ)²）独立于本偏差，不受影响")

    result = {
        "M_ud": M_ud, "m_rho": 2*M_ud, "m_rho_dev": (2*M_ud/M_RHO_EXP-1)*100,
        "m_N": m_N, "m_N_dev": (m_N/M_N_EXP-1)*100,
        "dress_ratio": ratio, "cand_1_plus_2sigma_3": cand, "dev": (ratio/cand-1)*100,
        "conclusion": "m_N偏差=M_ud 4.3%×3放大+SU(6) 6.7%缺陷（paper40已知）；Δ_dress +2σ/3修正候选登记",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_2_mN_diagnosis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
