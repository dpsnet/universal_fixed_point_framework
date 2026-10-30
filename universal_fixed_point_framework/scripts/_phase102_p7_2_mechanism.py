# -*- coding: utf-8 -*-
"""
Phase 102 P7-2 续-1：(1−σ) 与 (2σ)² 机制论证
==============================================
用户指令 1：论证为何静默层级以 1−σ 与 (2σ)² 组合进入通道比值。

  A. σ 幂次系统扫描：确认 1−σ（Δ_hf/Λ）与 (2σ)²（m_ud/Δ_hf）是最优选择
  B. 机制候选：静默层级 R_supp(N) = σ^N（paper44 母公式）→
     1−σ = 通道活跃份额（15 分支 1 静默）；(2σ)² = 两级静默 × 色因子 2²
  C. 交叉验证：m_s/Λ、m_s/Δ_hf 是否也有几何结构（s 夸克通道）
"""
import math
import json

SIGMA = 1.0/15.0
LAMBDA = 210.3
M_UD = 3.45
DHF = 195.8
M_S = 95.0

def main():
    print("=" * 78)
    print("P7-2 续-1：(1−σ) 与 (2σ)² 机制论证")
    print("=" * 78)
    print(f"[框架] σ = 1/15 = {SIGMA:.6f}；Λ = {LAMBDA} MeV")

    print(f"\n[A] σ 幂次扫描（确认最优选择）")
    print(f"    Δ_hf/Λ = {DHF/LAMBDA:.5f}（实验定标 195.8）")
    best = []
    for k in (1, 2, 3, 4):
        v = 1.0 - SIGMA**k
        dev = ((DHF/LAMBDA)/v - 1)*100
        print(f"      1−σ^{k} = {v:.6f}   偏差 {dev:+.2f}%{'  ★' if abs(dev)<0.5 else ''}")
        if abs(dev) < 0.5: best.append(("1−σ^%d"%k, dev))
    for a in (1, 2, 3, 4):
        for k in (1, 2):
            v = (a*SIGMA)**k
            dev = ((M_UD/DHF)/v - 1)*100
            if abs(dev) < 2.0:
                print(f"      m_ud/Δ_hf vs ({a}σ)^{k} = {v:.6f}   偏差 {dev:+.2f}%{'  ★' if abs(dev)<0.5 else ''}")
                if abs(dev) < 0.5: best.append(("(%dσ)^%d"%(a,k), dev))

    print(f"\n[B] 机制候选（静默层级 R_supp(N) = σ^N，paper44 母公式）")
    print(f"    ① 1−σ = 14/15：色磁超精细通道活跃份额")
    print(f"       ——15 分支中 1 支静默（σ），14 支活跃参与色磁耦合")
    print(f"       ——与 paper44 命题 2.5 '静默驻留=禁闭' 同构：静默是谱结构内生性质")
    print(f"    ② (2σ)² = 4/225：Yukawa 通道两级静默 × 色因子 2²")
    print(f"       ——2 的来源候选：SU(3) 轻夸克双重态 (u,d) 的 2 个独立静默方向")
    print(f"       ——或：两级独立静默（每级 σ），色单态投影给 2²")
    print(f"       ——需进一步机制锁定（登记为开放）")

    print(f"\n[C] 交叉验证：s 夸克通道")
    print(f"    m_s/Λ = {M_S/LAMBDA:.4f}；m_s/Δ_hf = {M_S/DHF:.4f}")
    print(f"    m_s/m_ud = {M_S/M_UD:.1f} ≈ 27.5（非 σ 幂次组合；s 通道几何待续）")

    print(f"\n[结论]")
    print(f"    ① 1−σ（14/15）与 (2σ)²（4/225）经幂次扫描确认为最优（偏差 0.24%/0.89%）")
    print(f"    ② 机制解释：通道活跃份额（1−σ）与两级静默×色因子（(2σ)²）——")
    print(f"       静默层级 R_supp(N)=σ^N 的幂次组合（paper44 母公式），")
    print(f"       与 P7-1 的谱间隙比（Δλ₂/Δλ₁）并列，为框架内第二类通道几何")
    print(f"    ③ 2 的来源（色双重态静默方向）登记开放；s 通道几何待续")

    result = {
        "scan_1_minus_sigma_k": {k: {"val": 1-SIGMA**k, "dev": ((DHF/LAMBDA)/(1-SIGMA**k)-1)*100} for k in (1,2,3,4)},
        "scan_2sigma_sq": {"val": (2*SIGMA)**2, "dev": ((M_UD/DHF)/(2*SIGMA)**2-1)*100},
        "mechanism": "1−σ=通道活跃份额(15分支1静默)；(2σ)²=两级静默×色因子2²；静默层级R_supp(N)=σ^N幂次组合",
        "s_quark": {"m_s_over_lam": M_S/LAMBDA, "m_s_over_dhf": M_S/DHF, "note": "几何待续"},
        "conclusion": "1−σ与(2σ)²确认为最优几何组合（机制：静默层级幂次组合，paper44母公式）；2的来源开放",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_2_mechanism.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
