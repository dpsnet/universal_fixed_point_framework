# -*- coding: utf-8 -*-
"""
Phase 102 P7-3：p/n 质量差 Δm_pn/M_Pl
========================================
目标对照：Δm_pn = m_n − m_p = 1.2933 MeV；Δm_pn/M_Pl = 1.059e−22

推导链（同位旋破缺）：
  m_n − m_p = (m_d − m_u) − (EM_p − EM_n)
  A. Yukawa 项 (m_d − m_u)：两条路径
     A1. paper11 §8.4 谱框架直接构造（u/t=1.5e−5、d/b=9.0e−4 × 谱定 m_t/m_b）
     A2. 几何候选：Δm_ud = m_ud×(C_F/2)(1+2σ/3)（复用 P7-2b 色因子体系）
  B. 电磁项 EM_pn = (m_d−m_u) − 1.2933（反推）——框架量搜索
"""
import math
import json

SIGMA = 1.0/15.0
LAMBDA = 210.3
M_UD = 3.45
DHF = 195.8
M_N_MINUS_P = 1.2933
M_PL = 1.221e22
N_C = 3.0

def main():
    print("=" * 78)
    print("P7-3：p/n 质量差 Δm_pn/M_Pl")
    print("=" * 78)
    print(f"[框架] σ = 1/15；Λ = {LAMBDA}；m_ud = {M_UD}；Δ_hf = {DHF}")

    print(f"\n[A] Yukawa 项 (m_d − m_u) 两条路径")
    # A1: paper11 谱框架直接构造（m_t/m_b 转 MeV）
    m_t = 0.994*246.0/math.sqrt(2.0)*1000.0   # y_t·v_Sp/√2（谱定 v=246，GeV→MeV）
    m_b = 0.024*246.0/math.sqrt(2.0)*1000.0   # y_b·v_Sp/√2
    m_u_p11 = m_t*1.5e-5
    m_d_p11 = m_b*9.0e-4
    dm_p11 = m_d_p11 - m_u_p11
    print(f"    A1 paper11 直接构造：m_t = {m_t:.1f}、m_b = {m_b:.2f}（谱定）")
    print(f"       m_u = {m_u_p11:.2f}、m_d = {m_d_p11:.2f} → Δm_ud = {dm_p11:.2f} MeV")
    print(f"       实验 (m_d−m_u) ≈ 2.4 MeV——偏差 ×{2.4/dm_p11:.1f}（继承 paper11 平均偏差 ×1.37）")
    # A2: 几何候选
    CF2 = (N_C**2 - 1.0)/(4.0*N_C)     # C_F/2 = 2/3
    geo = CF2*(1.0 + 2*SIGMA/3.0)      # (C_F/2)(1+2σ/3)
    dm_geo = M_UD*geo
    print(f"    A2 几何候选：Δm_ud = m_ud×(C_F/2)(1+2σ/3) = {M_UD:.2f}×{geo:.6f} = {dm_geo:.3f} MeV")
    print(f"       实验 2.4 MeV——偏差 {(dm_geo/2.4-1)*100:+.2f}%（P7-2b 色因子体系复用）")
    print(f"       结构：(2/3)(29/30) = 2/3 + 4σ/9——C_F/2（色磁 Casimir 半）×Δ_dress 修正因子")

    print(f"\n[B] 电磁项 EM_pn（由观测反推）")
    EM = dm_geo - M_N_MINUS_P
    print(f"    EM_pn = (m_d−m_u) − Δm_pn = {dm_geo:.3f} − {M_N_MINUS_P} = {EM:.3f} MeV")
    print(f"    （BMW 2020 口径 EM_pn ≈ +1.11 MeV——质子自能>中子自能）")
    print(f"    框架量搜索：")
    cands = [
        ("α_EM×Λ", 0.0073*LAMBDA), ("α_EM×Δ_hf", 0.0073*DHF),
        ("α_EM×m_N", 0.0073*938.9), ("Λ×(1−σ)/151.9", LAMBDA*(1-SIGMA)),
        ("Δ_hf×σ", DHF*SIGMA), ("Δ_hf×σ/1.18", DHF*SIGMA/1.18),
        ("m_ud×σ", M_UD*SIGMA),
    ]
    for name, v in cands:
        print(f"       {name:24s} = {v:.3f} MeV（EM 目标 {EM:.3f}，偏差 {(v/EM-1)*100:+.1f}%）")
    print(f"    → 无 <1% 干净框架量命中——EM_pn 框架构造登记开放（同 P7-1 缺口处理）")

    print(f"\n[C] Δm_pn/M_Pl 对照")
    print(f"    Δm_pn/M_Pl = {M_N_MINUS_P}/{M_PL:.3e} = {M_N_MINUS_P/M_PL:.3e}")

    print(f"\n[结论]")
    print(f"    ① Yukawa 项几何候选：Δm_ud = m_ud×(C_F/2)(1+2σ/3) = {dm_geo:.3f} MeV（实验 2.4，偏差 {(dm_geo/2.4-1)*100:+.2f}%）——")
    print(f"       复用 P7-2b 色因子体系（C_F/2）×Δ_dress 修正（1+2σ/3）——框架内组合（候选）")
    print(f"    ② paper11 直接构造偏差 ×2.1——几何路径显著优于直接构造")
    print(f"    ③ EM_pn = {EM:.3f} MeV 无干净框架量——登记开放")
    print(f"    ④ Δm_pn/M_Pl = 1.059e−22 对照值登记")

    result = {
        "A1_p11": {"m_u": m_u_p11, "m_d": m_d_p11, "dm": dm_p11, "factor_vs_exp": 2.4/dm_p11},
        "A2_geo": {"dm": dm_geo, "dev": (dm_geo/2.4-1)*100, "structure": "(C_F/2)(1+2σ/3)"},
        "EM_pn": EM, "EM_open": True,
        "target": {"dm_pn": M_N_MINUS_P, "dm_pn_over_MPl": M_N_MINUS_P/M_PL},
        "conclusion": "Yukawa项几何候选 2.402 MeV（0.1%）；EM_pn 1.109 MeV 框架量开放；直接构造 ×2.1",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_3_pn_mass_diff.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
