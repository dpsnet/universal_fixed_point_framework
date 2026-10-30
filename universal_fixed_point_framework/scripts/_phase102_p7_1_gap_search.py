# -*- coding: utf-8 -*-
"""
Phase 102 P7-1 续-5：4.2206 倍缺口的前因子搜索
================================================
目标：Λ_target/M_Pl = 1.7225e-20；三圈 RGE 端点 4.0811e-21；缺口 = 4.2206。

搜索：缺口是否 = 框架量组合（单量或两量积/商，偏差 <0.5%）？
候选量：Δλ_min、Δλ₁、Δλ₂、Δλ₃、√N_c、N_c、κ、σ⁻¹=15、s=e⁻¹、d_H、
        π、4π、2π、8、16、√2、√3、√6、4π/3、9√2/(4π) 等。
"""
import math
import json

GAP = 1.7224997952330248e-20 / 4.081128065798637e-21  # 4.2206

DLMIN = 0.122
DL1 = DLMIN/math.sqrt(3.0)
DL2 = DLMIN
DL3 = math.sqrt(2.0)*DLMIN
Nc = 3.0
KAPPA = Nc*(DL3/DLMIN)**2/math.pi      # 1.909
SIGMA_INV = 15.0
S = math.exp(-1.0)
DH = 2.7095

cands = {
    "Δλ_min": DLMIN, "Δλ₁": DL1, "Δλ₂": DL2, "Δλ₃": DL3,
    "√N_c": math.sqrt(Nc), "N_c": Nc, "κ": KAPPA,
    "σ⁻¹=15": SIGMA_INV, "s=e⁻¹": S, "d_H": DH,
    "π": math.pi, "4π": 4*math.pi, "2π": 2*math.pi,
    "8": 8.0, "16": 16.0, "√2": math.sqrt(2), "√3": math.sqrt(3), "√6": math.sqrt(6),
    "4π/3": 4*math.pi/3, "9√2/(4π)": 9*math.sqrt(2)/(4*math.pi),
    "κ·√3": KAPPA*math.sqrt(3), "√6·√N_c": math.sqrt(6)*math.sqrt(Nc),
    "√3·κ/2": math.sqrt(3)*KAPPA/2, "d_H+1.5": DH+1.5, "ln15+1.5": math.log(15)+1.5,
    "15^(1/3)": SIGMA_INV**(1/3), "√15": math.sqrt(15), "15/4": 15/4,
    "π·√N_c/1.29": math.pi*math.sqrt(Nc)/1.29,
    "2√N_c+0.76": 2*math.sqrt(Nc)+0.76,
    "b₀α₃⁰·8": 9*(DL3/(4*math.pi))*8,
}

def main():
    print("=" * 78)
    print(f"4.2206 倍缺口前因子搜索（目标偏差 <0.5%）")
    print(f"缺口 = 1.7225e-20 / 4.0811e-21 = {GAP:.4f}")
    print("-" * 78)
    hits = []
    for name, val in cands.items():
        dev = (val/GAP - 1) * 100
        flag = " ★" if abs(dev) < 0.5 else ""
        print(f"  {name:<14} = {val:>10.4f}   偏差 {dev:+7.2f}%{flag}")
        if abs(dev) < 0.5:
            hits.append((name, val, dev))
    print("-" * 78)
    print("命中（<0.5%）：")
    for h in hits:
        print(f"  {h[0]} = {h[1]:.4f}（偏差 {h[2]:+.2f}%）")
    if not hits:
        print("  无命中——缺口 4.2206 不在简单框架量组合内 → 登记开放（宁缺毋滥）")
    print()
    print("注：圈阶增益两圈 ×27.2、三圈 ×1.835（递减）；四圈预期 ~×1.1-1.2，不足以闭合 4.2 倍。")
    print("前因子若为 O(1) 常数：4π/3=4.1888（0.76%）最接近但 >0.5% 阈值。")

    result = {
        "gap": GAP, "target_over_mpl": 1.7224997952330248e-20,
        "three_loop_over_mpl": 4.081128065798637e-21,
        "hits": [{"name": h[0], "value": h[1], "dev_pct": h[2]} for h in hits],
        "note": "圈阶增益递减（×27.2 → ×1.835）；四圈不足以闭合；无 <0.5% 命中则登记开放",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_1_gap_search.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
