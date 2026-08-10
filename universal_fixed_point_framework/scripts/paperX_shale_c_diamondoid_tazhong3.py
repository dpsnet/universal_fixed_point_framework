# -*- coding: utf-8 -*-
"""
c 项指纹判别复现：塔中Ⅲ区（赵星星等 2022，天然气地球科学 33(1): 36-48）
================================================================
目的：以塔中Ⅲ区奥陶系原油为体系级载体，复现陈中红式"参数间解耦"判别
（金刚烷成熟度 vs 芳烃成熟度系统性差异 = 多期充注/运移烃背景 c 项指纹）。

数据来源（PDF 转录，Temp/tazhong3_full.txt）：
- 表 3 金刚烷质量色谱分析（5 井逐井 AS/AD 含量）
- 正文：芳烃成熟度 Rc1（MPI1）、Rc2（DBT 2,4-DMDBT/1,4-DMDBT）分区区间
- 正文：金刚烷 MAI/MDI 交会图成熟度区间（1.3%~1.6%，ZG15 井 >1.9%）
- 正文：4-MDBT/1-MDBT 与金刚烷含量 R^2=0.9967（图 9a）

判定逻辑：
- 若金刚烷成熟度(高熟窗) 系统性高于 芳烃成熟度(成熟窗) → 参数间解耦成立
  → 多期/混源充注指纹（晚期高熟气侵叠加早期成熟油）→ c 项（运移烃背景）分子层证据
- 须诚实登记：体系级区间对比（非逐油样成对），换算锚点差异（Chen 1996 vs Radke）为系统误差来源
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = r"e:\workspace\hyper-resolution\Temp\fig"
os.makedirs(OUT, exist_ok=True)

# ---------- 表 3：金刚烷质量色谱（μg/g） ----------
# 井号, 相态, AS(单金刚烷), AD(双金刚烷)
diam = [
    ("ZG14-1",   "凝析油", 132.78,  51.47),
    ("ZG14-H7",  "凝析油", 138.66,  36.15),
    ("ZG15",     "挥发油", 1217.10, 643.70),
    ("ZG27C",    "轻质油", 91.84,  107.83),
    ("ZG291-H12","轻质油", 42.47,   18.87),
]
wells = [d[0] for d in diam]
phase = [d[1] for d in diam]
AS = np.array([d[2] for d in diam])
AD = np.array([d[3] for d in diam])
total = AS + AD

# ---------- 芳烃成熟度 Rc1/Rc2（正文区间，按相态） ----------
# Rc1（MPI1 拟合）：凝析油 0.78~1.1%，挥发油 0.81~0.83%，轻质油 0.74~0.81%
# Rc2（DBT 2,4/1,4-DMDBT）：凝析油 0.8~1.4%，挥发油 0.74~1.49%，轻质油 0.72~1.0%
arom_Rc1 = {"凝析油": (0.78, 1.10), "挥发油": (0.81, 0.83), "轻质油": (0.74, 0.81)}
arom_Rc2 = {"凝析油": (0.80, 1.40), "挥发油": (0.74, 1.49), "轻质油": (0.72, 1.00)}

# ---------- 金刚烷 MAI/MDI 成熟度（图 9b 交会图，正文） ----------
# "原油成熟度大多集中于 1.3%~1.6% 之间，轻质油成熟度较低，ZG15 井原油成熟度最高，超过 1.9%"
diam_mat = {"凝析油": (1.30, 1.60), "挥发油": (1.30, 1.90), "轻质油": (1.20, 1.60)}  # 轻质油较低(未给精确区间，保守取 1.2~1.6)
zg15_mat = 1.9

# ---------- 表 3 输出 ----------
print("=" * 70)
print("表 3 转录：塔中Ⅲ区奥陶系原油金刚烷质量色谱（赵星星等 2022）")
print("=" * 70)
print(f"{'井号':<12}{'相态':<6}{'AS(μg/g)':>10}{'AD(μg/g)':>10}{'总计':>10}")
for i, w in enumerate(wells):
    print(f"{w:<12}{phase[i]:<6}{AS[i]:>10.2f}{AD[i]:>10.2f}{total[i]:>10.2f}")
print(f"\n4-MDBT/1-MDBT 与金刚烷含量正相关 R^2 = 0.9967（图 9a，正文）")

# ---------- 参数间解耦判别 ----------
print("\n" + "=" * 70)
print("参数间解耦判别：金刚烷(高熟窗) vs 芳烃(成熟窗) 成熟度")
print("=" * 70)
print(f"{'相态':<8}{'芳烃Rc1(%)':>12}{'芳烃Rc2(%)':>12}{'金刚烷MDI/MAI(%)':>20}{'解耦Δ(%)':>12}")
decoupling = {}
for ph in ["凝析油", "挥发油", "轻质油"]:
    r1 = arom_Rc1[ph]
    r2 = arom_Rc2[ph]
    dm = diam_mat[ph]
    # 解耦量 = 金刚烷成熟度区间中点 - 芳烃成熟度区间中点（取 Rc1 与 Rc2 并集的中点近似）
    arom_mid = (min(r1[0], r2[0]) + max(r1[1], r2[1])) / 2.0
    diam_mid = (dm[0] + dm[1]) / 2.0
    decoupling[ph] = diam_mid - arom_mid
    print(f"{ph:<8}{f'{r1[0]}~{r1[1]}':>12}{f'{r2[0]}~{r2[1]}':>12}"
          f"{f'{dm[0]}~{dm[1]}':>20}{decoupling[ph]:>12.2f}")

print(f"\nZG15 井（挥发油）金刚烷成熟度 >1.9%，为全区最高；其 AS+AD=1861.07 μg/g 亦为全区最高。")
print(f"结论：金刚烷成熟度(1.3~1.9%) 系统性高于 芳烃成熟度(0.72~1.49%) → 参数间解耦成立。")
print(f"解耦成因（原文归因）：底部晚期高熟油气充注叠加早期成熟油 = 多源多期混合充注。")
print(f"→ 与李宗亮 2025 教训互补：成熟窗经典甾萜比值（C29 20S 等）近平衡失效，")
print(f"   金刚烷(高熟窗单调) + 芳烃(成熟窗) 的跨窗组合不受平衡限制 → c 项指纹判别可行。")

# ---------- 诚实登记 ----------
print("\n" + "=" * 70)
print("诚实登记（适用域显式化）")
print("=" * 70)
print("1. 体系级对比：金刚烷成熟度为图 9b 交会图读数的区间估计，非逐油样成对值；")
print("   芳烃 Rc1/Rc2 为按相态分区区间，非逐井成对。")
print("2. 换算锚点差异：金刚烷成熟度（Chen et al. 1996 换算）与芳烃成熟度（Radke/DBT 换算）")
print("   锚点系统不同，解耦幅度可能部分含锚点系统差——陈中红 2022 原方法要求同一样品") 
print("   轻烃/金刚烷 vs 甾萜/芳烃的成对比较，本载体为体系级近似。")
print("3. 数据缺口：MAI/MDI 逐井数值未发表（仅交会图），4-MDBT/1-MDBT 逐井值未发表（仅 R^2）。")
print("4. 意义：本载体证明【高熟窗金刚烷+成熟窗芳烃】跨窗组合天然存在于塔里木超深层体系，")
print("   构成 c 项分子指纹判别的体系级可行性证据，逐油样成对定量待新载体。")

# ---------- 图 ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左：金刚烷含量（AS/AD 堆叠）
ax = axes[0]
idx = np.arange(len(wells))
ax.bar(idx, AS, label="AS 单金刚烷", color="#4C72B0")
ax.bar(idx, AD, bottom=AS, label="AD 双金刚烷", color="#DD8452")
ax.set_xticks(idx)
ax.set_xticklabels(wells, rotation=30)
ax.set_ylabel("含量 (μg/g)")
ax.set_title("金刚烷含量（表 3，赵星星等 2022）")
ax.legend()

# 右：参数间解耦（区间条）
ax = axes[1]
labels = ["凝析油", "挥发油", "轻质油"]
ypos = np.arange(len(labels))
for i, ph in enumerate(labels):
    r1 = arom_Rc1[ph]; r2 = arom_Rc2[ph]
    dm = diam_mat[ph]
    ax.barh(ypos[i] + 0.15, r1[1] - r1[0], left=r1[0], height=0.25, color="#8DA0CB", label="芳烃 Rc1" if i == 0 else None)
    ax.barh(ypos[i] - 0.15, r2[1] - r2[0], left=r2[0], height=0.25, color="#A6D854", label="芳烃 Rc2" if i == 0 else None)
    ax.barh(ypos[i] + 0.15 + 0.4, dm[1] - dm[0], left=dm[0], height=0.25, color="#E78AC3", label="金刚烷 MAI/MDI" if i == 0 else None)
ax.axvline(1.9, color="red", ls="--", lw=1, label="ZG15 >1.9%")
ax.set_yticks(ypos + 0.4)
ax.set_yticklabels(labels)
ax.set_xlabel("等效成熟度 Ro (%)")
ax.set_title("参数间解耦：金刚烷(高熟窗) >> 芳烃(成熟窗)")
ax.legend(fontsize=8)
ax.set_xlim(0.5, 2.1)

fig.suptitle("c 项指纹判别：塔中Ⅲ区奥陶系原油参数间解耦（体系级载体）", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(os.path.join(OUT, "tazhong3_diamondoid_decoupling.png"), dpi=150)
print(f"\n图已保存：{os.path.join(OUT, 'tazhong3_diamondoid_decoupling.png')}")
