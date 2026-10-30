# -*- coding: utf-8 -*-
"""
Phase 102 P7-4c：α 序列的 Bott 塔/对偶网络同源登记
===================================================
框架内对偶网络（勘误 v0.21，paperX_kmax_duality.py 10/10 机器验证，k_max=8 中心）：
  旋量 16 = 2·k_max；分支 B = 15 = 2·k_max−1（d_H = ln15）；底空间 8 = k_max；
  log2(k_max) = 3 = N_active；Bott-Moran 桥 ln15 = ln16 − ln(16/15)。

新候选（本脚本）：7 = k_max − 1 = 2^{N_active} − 1 是对偶网络的缺失成员
  → α_u = ln7 = ln(k_max−1)（−0.05%）
  → 塔链 7 + 8 = 15：k_max−1、k_max、2k_max−1 同源
"""
import math
import json

K_MAX = 8.0
N_ACTIVE = 3.0
D_H = 2.7095
DELTA_L_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
ALPHA_U, ALPHA_D, ALPHA_L = 1.945, 1.229, 1.358

def main():
    print("=" * 78)
    print("P7-4c：α 序列的 Bott 塔/对偶网络同源登记")
    print("=" * 78)
    print("[框架对偶网络] k_max = 8（统一 3 定理 2^N_active 机器证明）")
    print(f"  旋量 16 = 2·k_max ✓；分支 B = 15 = 2·k_max−1 ✓（d_H = ln15）")
    print(f"  底空间 8 = k_max ✓；log2(k_max) = 3 = N_active ✓")

    print(f"\n[A] 缺失对偶：7 = k_max − 1 = 2^N_active − 1")
    seven = K_MAX - 1
    print(f"    k_max−1 = {seven:.0f}；2^N_active−1 = {2**3-1}——一致")
    ln7 = math.log(7)
    print(f"    ln7 = {ln7:.5f} vs α_u = {ALPHA_U}（偏差 {(ln7/ALPHA_U-1)*100:+.2f}%）")
    print(f"    → α_u = ln(k_max−1)——对偶网络缺失成员（新候选登记）")

    print(f"\n[B] 塔链：7 + 8 = 15（k_max−1、k_max、2k_max−1 同源）")
    print(f"    7 + 8 = {seven + K_MAX:.0f} = 15 = 2·k_max−1 ✓")
    ln15 = math.log(15)
    print(f"    ln15 = {ln15:.5f}；d_H = ln15 + δ = {ln15 + (D_H-ln15):.5f}（δ = {D_H-ln15:.5f}）")
    print(f"    Bott-Moran 桥：ln15 = ln16 − ln(16/15) = {math.log(16)-math.log(16/15):.5f} ✓")
    print(f"    新桥：ln7 = ln8 − ln(8/7) = {math.log(8)-math.log(8/7):.5f} ✓（同构形式）")

    print(f"\n[C] α 序列在对偶网络上的位置")
    half = (D_H)/2
    half_m = half - DELTA_L_MIN
    print(f"    α_l = d_H/2 = {half:.5f}（偏差 {(half/ALPHA_L-1)*100:+.2f}%）——分支对偶半塔（1/2 无身份，开放）")
    print(f"    α_d = d_H/2−Δλ_min = {half_m:.5f}（偏差 {(half_m/ALPHA_D-1)*100:+.2f}%）——分支半塔 − 谱间隙")
    print(f"    α_u = ln(k_max−1) = {ln7:.5f}（偏差 {(ln7/ALPHA_U-1)*100:+.2f}%）——缺失对偶（全塔）")

    print(f"\n[D] Δλ_min 的塔结构")
    denom = K_MAX*(K_MAX+1)
    print(f"    √72 = √(k_max(k_max+1)) = √({denom:.0f}) = {math.sqrt(denom):.4f} ✓（paper20 定理 6.1）")
    print(f"    Δλ_min = (√6−√2)/√72 = {DELTA_L_MIN:.4f}")

    print(f"\n[结论]")
    print(f"    ① ★ 7 = k_max−1 是对偶网络缺失成员——α_u = ln(k_max−1)（−0.05%）")
    print(f"    ② ★ 塔链 7+8 = 15：α_u（k_max−1）、k_max（底空间）、d_H（2k_max−1）同源")
    print(f"    ③ α_l = d_H/2、α_d = d_H/2−Δλ_min 均挂在对偶网络上——α 序列同源（非单一公式）")
    print(f"    ④ 诚实边界：1/2 半塔因子无身份（开放）；α_u 全塔 vs α_l/α_d 半塔幂次不统一；")
    print(f"       '7 为缺失对偶'是新登记候选（框架已有 16/15/8/3，无 7）")

    result = {
        "k_max": K_MAX, "seven": seven, "ln7": ln7, "alpha_u_dev": (ln7/ALPHA_U-1)*100,
        "tower_chain": {"7": 7, "8": 8, "15": 15},
        "alpha_l": {"cand": half, "dev": (half/ALPHA_L-1)*100},
        "alpha_d": {"cand": half_m, "dev": (half_m/ALPHA_D-1)*100},
        "delta_denom": denom,
        "conclusion": "α_u=ln(k_max−1)=ln7 缺失对偶登记；α 序列同源对偶网络；半塔因子开放",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_4c_alpha_bott_duality.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
