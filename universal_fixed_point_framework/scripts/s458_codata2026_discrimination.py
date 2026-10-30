# -*- coding: utf-8 -*-
"""
S458: CODATA 2026 三方裁决判别图谱
====================================
目标：为 CODATA 2026 裁决点准备先验判读工具。
- 扫描 α⁻¹ 落点 x ∈ [137.03599900, 137.03599935]
- 三方框架各自 σ_score(x) = |x − 框架值| / 合成不确定度 σ_u
- 三方值差互斥结构量化（以 2022 合成不确定度 21e-9 为基准标尺）
- 三情景预测（Cs 主导 / Rb 主导 / 均衡）→ 2026 预测值 + 合成不确定度 → 三方 σ_score
- 分段判读：x 落哪个区间 → 谁是胜者（≤1σ 达标判据，σ_score 铁律）

框架值（已核验，S418-S457）：
  MUFPF 主构造   : 137.035999083426（2018=0 基底 + 机制构造）
  Nusbaumer π 链 : 137.035999216（纯几何）
  Kraemer        : 137.035999177001（c₄=e² 5 项）

实验通道（verbatim）：
  CODATA 2018 : 137.035999084(21)
  Parker Cs   : 137.035999046(27)
  Fan a_e     : 137.035999166(16)
  Morel Rb    : 137.035999206(11)
  CODATA 2022 : 137.035999177(21)
"""
import numpy as np

# ---------------- 框架值与实验值 ----------------
MUF = 137.035999083426
PI  = 137.035999216
KRA = 137.035999177001

EXP = {
    "CODATA2018": (137.035999084, 21e-9),
    "Cs2018":     (137.035999046, 27e-9),
    "a_e2023":    (137.035999166, 16e-9),
    "Rb2020":     (137.035999206, 11e-9),
    "CODATA2022": (137.035999177, 21e-9),
}
SU_2022 = 21e-9   # 基准标尺

def sigma_score(pred, exp_val, exp_err):
    """σ_score = |预测−实验|/合成不确定度（实验不确定度口径，理论精确）"""
    return abs(pred - exp_val) / exp_err

# ---------------- 1. 现有通道三方 σ_score 表 ----------------
print("=" * 78)
print("1) 现有通道 × 三方框架 σ_score 表（实验不确定度为分母）")
print("=" * 78)
print(f"{'通道':<12}{'实验值':<22}{'MUFPF σ':<10}{'π链 σ':<10}{'Kraemer σ':<10}{'最近'}")
rows = []
for name, (val, err) in EXP.items():
    s_m, s_p, s_k = sigma_score(MUF, val, err), sigma_score(PI, val, err), sigma_score(KRA, val, err)
    nearest = min([("MUFPF", s_m), ("π链", s_p), ("Kraemer", s_k)], key=lambda t: t[1])[0]
    rows.append((name, val, s_m, s_p, s_k, nearest))
    print(f"{name:<12}{val:<22.9f}{s_m:<10.3f}{s_p:<10.3f}{s_k:<10.3f}{nearest}")

# ---------------- 2. 三方互斥结构（以 21e-9 为基准标尺） ----------------
print()
print("=" * 78)
print("2) 三方互斥结构（基准标尺 σ_u = 21e-9 = CODATA 2022 合成不确定度）")
print("=" * 78)
pairs = [("MUFPF vs π链", MUF, PI), ("MUFPF vs Kraemer", MUF, KRA), ("Kraemer vs π链", KRA, PI)]
for label, a, b in pairs:
    d = abs(a - b)
    print(f"  {label:<18} |Δ| = {d:.3e} = {d/SU_2022:.2f} σ(基准)")

# 每个框架到 CODATA 2026 目标的不确定度要求（需 2026 σ_u 多小才能判别）
print()
print("  若 CODATA 2026 合成不确定度为 σ_u，三方判别要求：")
for label, a, b in pairs:
    d = abs(a - b)
    print(f"    {label:<18} 需 σ_u < {d/2:.3e}（两值在 2σ 外）——即相对精度 < {d/(2*a)*100:.2e}%")

# ---------------- 3. 判别图谱：扫描 x ----------------
print()
print("=" * 78)
print("3) 判别图谱：x 落点 → 三方 σ_score（以 σ_u = 21e-9 为 2026 假设不确定度）")
print("=" * 78)
x_lo, x_hi, n = 137.03599900, 137.03599935, 351  # 步长 1e-9
xs = np.linspace(x_lo, x_hi, n)
print(f"{'x(尾差 1e-9)':<16}{'MUFPF σ':<10}{'π链 σ':<10}{'Kraemer σ':<10}{'胜者(≤1σ)'}")
for x in xs:
    sm, sp, sk = sigma_score(MUF, x, SU_2022), sigma_score(PI, x, SU_2022), sigma_score(KRA, x, SU_2022)
    # 胜者判定：谁 ≤1σ 且最近；若均 >1σ 则记"三方全不达标"
    wins = []
    if sm <= 1.0: wins.append(("MUFPF", sm))
    if sp <= 1.0: wins.append(("π链", sp))
    if sk <= 1.0: wins.append(("Kraemer", sk))
    if not wins:
        winner = "全不达标"
    elif len(wins) == 1:
        winner = wins[0][0]
    else:
        winner = "".join(f"{w[0]}" for w in wins) + "并存"
    if int(round((x - x_lo) / 1e-9)) % 20 == 0 or (x - MUF) < 2e-9 or (x - PI) < 2e-9 or (x - KRA) < 2e-9:
        tail = (x - 137.03599900) * 1e9
        print(f"{tail:<16.1f}{sm:<10.2f}{sp:<10.2f}{sk:<10.2f}{winner}")

# ---------------- 4. 三方 1σ 命中带 ----------------
print()
print("=" * 78)
print("4) 三方 1σ 命中带（σ_u=21e-9 口径）")
print("=" * 78)
for label, v in [("MUFPF", MUF), ("π链", PI), ("Kraemer", KRA)]:
    lo, hi = v - SU_2022, v + SU_2022
    print(f"  {label:<8} 命中带 [{lo:.9f}, {hi:.9f}]  尾差 [{ (lo-137.03599900)*1e9:.1f}, {(hi-137.03599900)*1e9:.1f}] ×1e-9")

# ---------------- 5. 三情景 2026 预测 ----------------
print()
print("=" * 78)
print("5) CODATA 2026 三情景预测（基于 S455 漂移模式编码——构造差=实验差）")
print("=" * 78)
# 通道值（构造偏移已编码）：2018=0 基底；通道偏移构造（S419）
#   2018=0 → 137.035999083426
#   Cs = −(5/2)ln15·e⁻¹⁹ → 137.035999083426 − (5/2)*2.7080502011*e⁻¹⁹
#   a_e = +2ln15·e⁻¹⁸ → 137.035999083426 + 2*2.7080502011*e⁻¹⁸
#   Rb = +8e⁻¹⁸ → 137.035999083426 + 8*e⁻¹⁸
#   2022 = +16σ⁷ → 137.035999083426 + 16*(1/15)⁷
import math
ln15 = math.log(15.0)
e18 = math.exp(-18.0); e19 = math.exp(-19.0)
s7 = (1/15.0)**7
CONS = {
    "2018": MUF,
    "Cs":   MUF - (5.0/2.0)*ln15*e19,
    "a_e":  MUF + 2.0*ln15*e18,
    "Rb":   MUF + 8.0*e18,
    "2022": MUF + 16.0*s7,
}
# 构造 key → EXP key 映射
CONS2EXP = {"2018": "CODATA2018", "Cs": "Cs2018", "a_e": "a_e2023", "Rb": "Rb2020", "2022": "CODATA2022"}
print("  S419 构造值（框架量编码的通道值）：")
for k, v in CONS.items():
    print(f"    {k:<6} {v:.12f}  （实验差 {abs(v-EXP[CONS2EXP[k]][0])*1e9:.1f}e-9）")

# 三情景：以通道合成（加权）模拟 CODATA 合并
#   情景 A Cs 主导：权重 Cs 60% / 2018 40%（收敛至 2018-Cs 段）
#   情景 B Rb 主导：权重 Rb 60% / 2022 40%
#   情景 C 均衡（全通道等权：五通道平均）
scenarios = {
    "A Cs主导":  {"Cs2018": 0.60, "CODATA2018": 0.40, "a_e2023": 0.0, "Rb2020": 0.0, "CODATA2022": 0.0},
    "B Rb主导":  {"Cs2018": 0.0, "CODATA2018": 0.0, "a_e2023": 0.0, "Rb2020": 0.60, "CODATA2022": 0.40},
    "C 均衡":    {"Cs2018": 0.20, "CODATA2018": 0.20, "a_e2023": 0.20, "Rb2020": 0.20, "CODATA2022": 0.20},
}
for sname, w in scenarios.items():
    # 加权合成值（用实验值，权重归一）
    total_w = sum(w.values())
    v_comb = sum(w[k] * EXP[k][0] for k in w if w[k] > 0) / total_w
    # 合成不确定度：误差加权（独立测量假设：√(Σ(w_i·σ_i)²) / Σw）
    err_comb = math.sqrt(sum((w[k]*EXP[k][1])**2 for k in w if w[k] > 0)) / total_w
    sm, sp, sk = sigma_score(MUF, v_comb, err_comb), sigma_score(PI, v_comb, err_comb), sigma_score(KRA, v_comb, err_comb)
    nearest = min([("MUFPF", sm), ("π链", sp), ("Kraemer", sk)], key=lambda t: t[1])
    print(f"\n  [{sname}] 预测值 = {v_comb:.9f}（±{err_comb*1e9:.1f}e-9）")
    print(f"      MUFPF σ={sm:.2f} | π链 σ={sp:.2f} | Kraemer σ={sk:.2f} → 最近: {nearest[0]} ({nearest[1]:.2f}σ)")

# ---------------- 6. 漂移外推（S420 线性律）与框架值的关系 ----------------
print()
print("=" * 78)
print("6) 漂移线性律外推 vs 三情景（S420: α⁻¹ = 137.0359993220 − 10.1·u）")
print("=" * 78)
# S420 的 u 是"不确定度轴"——外推 u→0 得到 137.0359993220（18σ 距基底——证伪方向）
# S455 修正理解：漂移=测量代数变化——2026 值取决于测量代数组合，线性外推不是唯一通道
u_2022 = 21e-9
u_2018 = 21e-9
slope = 10.1
# 用 2018→2022 两点定斜率的实测版：Δα/Δu
d_val = EXP["CODATA2022"][0] - EXP["CODATA2018"][0]
d_u = (SU_2022 - 21e-9)  # 同一不确定度——线性斜率无法从等误差点估计
print("  2018/2022 同不确定度（21e-9）——线性斜率需新数据点才能更新")
print("  S420 线性律：α⁻¹(u) = 137.0359993220 − 10.1·u")
print(f"    u=0   → 137.0359993220（距 MUFPF 基底 {(137.0359993220-MUF)/SU_2022:.1f}σ——证伪方向已登记）")
print(f"    u=21e-9 → {137.0359993220 - 10.1*21e-9:.9f}（距 2022 实验 {(137.0359993220 - 10.1*21e-9 - EXP['CODATA2022'][0])/SU_2022:.1f}σ）")
print("  结论：线性外推（u→0 18σ 证伪）与漂移模式编码（S455 10/10 达标）并存——")
print("        2026 预测以情景加权（测量代数组合）为准，非线性外推")

# ---------------- 7. 汇总判读 ----------------
print()
print("=" * 78)
print("7) 判读规则（σ_score 铁律：≤1σ 达标、1-3σ 提示、>3σ 不达标）")
print("=" * 78)
print("  CODATA 2026 落点 → 裁决：")
print(f"    落 [083.4±21]（尾差 83-105）→ MUFPF 胜（2018 侧延续——Kraemer/π链 均 >4σ）")
print(f"    落 [177.0±21]（尾差 156-198）→ Kraemer 胜（12 位命中 2022 侧——MUFPF 4.5σ 需 S455 漂移论证应对）")
print(f"    落 [216.0±21]（尾差 195-237）→ π链 胜（LKB 侧——但 Cs/Rb 矛盾持续使单值判别失效——MUFPF 双构造唯一一致描述）")
print("  中间带（105-156 或 198-237 外）：三方全不达标 → 需更严判别（S455 构造差=实验差为唯一一致描述框架）")
