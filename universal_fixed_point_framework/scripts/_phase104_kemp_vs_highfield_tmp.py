# -*- coding: utf-8 -*-
"""Kemp 线性外推 vs 高场观测 V 对照（P4 判别：量化高场 V 抑制因子）
口径警告：低场锚为连续谱峰 V（G 227-35 4500Å / G 111-49 5500Å），高场三点为波长平均含线 V（Schmidt 4200-8400Å）。
Kemp: V/I(%) ~ <B_z>/(15 MG/%)  ->  V/I(%) ≈ <B_z>_MG / 15
<B_z> 估算：偶极近似 <B_z> ~ Bp/3（视线与磁轴任意角平均）；G 227-35/G 111-49 用 Kawka 的 <B_z> 估计。
"""
stars = [
    # name, B_MG(口径), V_obs(%), V_obs_type, Bz_est_MG, Bz_src
    ("G 227-35 (WD1829+547)", 120, 4.0, "cont_peak_4500", 40, "LOS对齐 30-50MG Kawka"),
    ("G 111-49 (WD0756+427)", 250, 8.0, "cont_peak_5500", 80, "LOS近平行 或达80MG Kawka"),
    ("SDSS J002129", 550, 0.91, "wavavg_4200-8400", 183.3, "Bp/3 偶极近似"),
    ("SDSS J120609", 830, 0.41, "wavavg_4200-8400", 276.7, "Bp/3 偶极近似"),
    ("SDSS J234605", 1000, -1.51, "wavavg_4200-8400", 333.3, "Bp/3 偶极近似"),
]

print("="*100)
print("Kemp 线性外推 (V/I% ≈ <B_z>/15) vs 观测 V 对照")
print("="*100)
print(f"{'星':<28}{'B(MG)':>7}{'观测V(%)':>10}{'类型':<20}{'<Bz>估':>8}{'Kemp预测%':>10}{'抑制因子':>10}")
for name, B, Vobs, vtype, Bz, src in stars:
    Vkemp = Bz / 15.0
    suppress = abs(Vobs) / Vkemp if Vkemp > 0 else float('inf')
    flag = "  << 抑制" if suppress < 0.5 else ("  ~吻合" if 0.5 <= suppress <= 2.0 else "  高于预测")
    print(f"{name:<28}{B:>7.0f}{Vobs:>10.2f}{vtype:<20}{Bz:>8.1f}{Vkemp:>10.2f}{suppress:>10.2f}{flag}")

print()
print("关键观察：")
print("- 低场锚（120-250 MG）：Kemp 预测 2.7-5.3%，观测 4-8% —— 量级吻合（γ=10-16 校准内）")
print("- 高场三点（550-1000 MG）：Kemp 线性外推预测 12-22%，观测仅 0.4-1.5% —— 抑制 8-55 倍")
print("- 口径注意：高场 v 为波长平均含线（Zeeman 分裂稀释 V），低场为连续谱峰 —— 不可直接比量级")
print("- 即使按最保守 <Bz> = Bp/3（偶极平均），高场抑制仍 >8 倍 —— 若 <Bz> 更小抑制更大")
print()
print("标准物理解释候选：")
print("  (1) 强场 Zeeman 分裂 > 线宽 → 波长平均 V 谱稀释（σ 分量 V 符号交错抵消）")
print("  (2) 高场连续谱偏振偏离 Kemp 线性（饱和/非线性 —— Kemp 校准仅对 ~几十 MG 有效）")
print("  (3) 场几何：高场星 <Bz> 实际远小于 Bp/3（如 i~90° 视线垂直磁轴）")
print()
print("P4 判别意义：")
print("  - 标准物理（1）+（3）可解释量级下降；符号翻转（J2346 -1.51%）标准物理不解释（符号随 <Bz>）")
print("  - 判别需：统一口径（连续谱窗口 V）+ 分波长 V(λ) + 中间场强点 —— 现有数据候选级")
