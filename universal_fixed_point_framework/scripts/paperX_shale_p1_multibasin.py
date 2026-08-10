# -*- coding: utf-8 -*-
"""
P1 双曲标度多盆地扩展（2026-08-10，数据转录首轮）
==================================================
目的：评估新增低维分形体系对 P1 双曲标度 ln P_t = C/(D-2)+B 的推进性。
数据：
- Tuscaloosa 31 样品（MICP 分形 D 2.53-3.87 + P_t 成对，主检验）
- 黔北五峰组-龙马溪 8 样品（D_Hg 2.0904-2.3736，逐样品 D 已转录，无 P_t）
- 玛湖风城组 20 样品（MICP Df1 高压段 2.548-2.7575 / Df2 低压段 2.9942-2.9955，无 P_t）
诚实结论：成对"低 D + P_t"仍缺；本脚本量化各盆地 D 分布 + 双曲外推的 D→2 端预言，
为后续获得 P_t 提供判定标尺。
"""
import numpy as np
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# 中文字体
for f in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
    if os.path.exists(f):
        font_manager.fontManager.addfont(f)
        plt.rcParams["font.family"] = f.split("\\")[-1].split(".")[0]
        break
plt.rcParams["axes.unicode_minus"] = False

OUT = r"e:\workspace\hyper-resolution\Temp\fig"
os.makedirs(OUT, exist_ok=True)

# ---------- Tuscaloosa：加载真实 MICP 成对数据 ----------
base = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\tuscaloosa_micp"
# 从历史脚本逻辑：整体 D + 门限压力（低饱和端截止压）成对已在论文复现中计算。
# 这里用已登记的论文级结果（§4.1）：拟合 ln P_t = -1.66/(D-2) + 10.47，R²=0.578
C_fit, B_fit, R2_hyper, R2_lin = -1.66, 10.47, 0.578, 0.450
D_tus, Pt_tus = None, None  # 逐样品数组在 paperX_shale_p1 脚本中，此处引用拟合常量

# ---------- 黔北（李一鸣 2024 表 4 转录） ----------
# 样品, 岩相, 孔隙度%, 渗透率mD, 孔体积cm3/g, 比表面m2/g, 平均孔径nm, 最大进汞饱和度%, R2, D_Hg
qianbei = [
    ("USS-17", "极富有机质硅质", 1.6256, 2.1975, 0.0065, 2.735, 9.51, 16.00, 0.9942, 2.2198),
    ("RSS-11", "富有机质硅质", 2.1780, 0.1582, 0.0087, 3.133, 11.10, 15.95, 0.9006, 2.2978),
    ("RMS-1", "富有机质混合质", 1.6459, 2.1254, 0.0063, 1.773, 14.11, 14.55, 0.9196, 2.1404),
    ("MSS-1", "中等有机质硅质", 1.0814, 1.2244, 0.0041, 1.112, 14.59, 14.22, 0.9753, 2.1230),
    ("MMS-13", "中等有机质混合质", 2.7113, 6.0540, 0.0107, 2.964, 14.45, 15.59, 0.9656, 2.0904),
    ("LSS-15", "贫有机质硅质", 1.7096, 0.5540, 0.0064, 0.768, 33.27, 13.99, 0.9811, 2.3736),
    ("LMS-1", "贫有机质混合质", 3.1702, 15.4231, 0.0118, 1.513, 31.12, 13.82, 0.9966, 2.1320),
    ("LCS-25", "贫有机质黏土质", 3.0875, 2.8005, 0.0115, 4.249, 10.78, 13.81, 0.9786, 2.1037),
]
D_qb = np.array([r[9] for r in qianbei])

# ---------- 玛湖（MOESM4 Table 3 转录） ----------
mahu_csv = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\jes_mahu_fengcheng\moesm4_fractal_dimensions.csv"
rows_m = []
with open(mahu_csv, encoding="utf-8-sig") as f:
    rd = csv.DictReader(f)
    for r in rd:
        rows_m.append(r)
Df1_m = np.array([float(r["MICP_Df1_highP"]) for r in rows_m])
Df2_m = np.array([float(r["MICP_Df2_lowP"]) for r in rows_m])

# ---------- 分析 ----------
print("=" * 74)
print("P1 多盆地扩展：分形维数分布对比（无 P_t 缺口显式化）")
print("=" * 74)
print(f"Tuscaloosa（成对）: D ∈ [2.53, 3.87]，中位 2.862（论文登记），双曲拟合 ln Pt = {C_fit}/(D-2) + {B_fit}，R²={R2_hyper}")
print(f"黔北（无 Pt）     : D_Hg ∈ [{D_qb.min():.4f}, {D_qb.max():.4f}]，均值 {D_qb.mean():.4f}，n=8，最大进汞饱和度 13.8-16.0%")
print(f"玛湖高压段 Df1（无 Pt）: D ∈ [{Df1_m.min():.4f}, {Df1_m.max():.4f}]，均值 {Df1_m.mean():.4f}，n=20")
print(f"玛湖低压段 Df2（无 Pt）: D ∈ [{Df2_m.min():.4f}, {Df2_m.max():.4f}]，均值 {Df2_m.mean():.4f}（≈3 高复杂度端）")

# D→2 双曲外推判定标尺
print("\n双曲外推标尺（Tuscaloosa 拟合 ln Pt = -1.66/(D-2) + 10.47，Pt 单位 psi）：")
print(f"{'D':>6}{'D-2':>8}{'ln Pt 预言':>12}{'Pt 预言/psi':>14}")
for D in [2.09, 2.12, 2.14, 2.20, 2.25, 2.37, 2.53, 2.86, 3.87]:
    lnpt = C_fit / (D - 2) + B_fit
    pt = np.exp(lnpt)
    print(f"{D:>6.2f}{D-2:>8.3f}{lnpt:>12.3f}{pt:>14.4f}")

print("\n关键内禀预言：C=-1.66<0（因 C=ln(S_min/a)<0，S_min 最小可测饱和度 < 标度常数 a）")
print("→ D→2^+ 时 ln Pt → -∞，即 **Pt → 0（弱封堵）**，而非强封堵。")
print("物理诠释：D→2 = 孔隙谱均匀（无孔喉阈值分布）→ 谱隙趋零 → 门限压力趋零。")
print("可证伪检验：低 D 样品（黔北 D_Hg=2.09）若实测低饱和端截止压很小 → 支持；")
print("若实测截止压很大（发散）→ 证伪 P1 双曲形式。")
print("（注：黔北正文'排驱压力<0.5 MPa'为大孔端入口压，口径不同，但方向一致地小。）")
print("P_t 缺口即为当前阻断点：需 MICP 原始曲线提取低饱和端截止压，或 JES 主文 3.3.2 节 Pt 值。")

# ---------- 图：三盆地 D 分布 + 双曲外推 ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

# 左：D 分布箱线/散点
ax = axes[0]
tus_med = 2.862
ax.barh(0, 1.34, left=2.53, height=0.5, color="#8DA0CB", alpha=0.5)
ax.plot([2.53, 3.87], [0, 0], color="#4C72B0", lw=2)
ax.plot([tus_med], [0], "o", color="#4C72B0")
ax.text(tus_med, 0.12, f"中位 {tus_med}", ha="center", fontsize=8)
ybins = 0
for i, (D, lbl) in enumerate([(D_qb, "黔北 D_Hg"), (Df1_m, "玛湖 Df1(高P)"), (Df2_m, "玛湖 Df2(低P)")]):
    y = -(i + 1)
    ax.plot([D.min(), D.max()], [y, y], color="#C44E52", lw=2)
    ax.plot(D, np.full_like(D, y) + 0.02, "o", color="#C44E52", ms=4, alpha=0.6)
    ax.text((D.min()+D.max())/2, y + 0.13, f"{lbl}: {D.min():.3f}-{D.max():.3f}", ha="center", fontsize=8)
ax.axvline(2.0, color="red", ls="--", lw=1)
ax.set_yticks([])
ax.set_xlim(1.9, 4.0)
ax.set_xlabel("分形维数 D")
ax.set_title("多盆地 D 分布（缺口：无成对 P_t）")

# 右：双曲外推曲线
ax = axes[1]
Dgrid = np.linspace(2.05, 3.9, 200)
lnpt = C_fit / (Dgrid - 2) + B_fit
ax.plot(Dgrid, lnpt, color="#4C72B0", lw=2, label="双曲拟合 ln Pt=C/(D-2)+B")
ax.axvline(2.0, color="red", ls="--", lw=1, label="D→2 发散")
# 黔北 D 位置标注（无 P_t，只能标 D 轴位置）
for D in D_qb:
    ax.plot([D, D], [min(lnpt) - 2, min(lnpt) + 20], color="#C44E52", alpha=0.25, lw=0.8)
ax.text(2.15, max(lnpt) - 2, "黔北 D_Hg=2.09-2.37 垂线", color="#C44E52", fontsize=8)
ax.set_xlim(2.02, 3.9)
ax.set_ylim(-5, 45)
ax.set_xlabel("D")
ax.set_ylabel("ln P_t")
ax.set_title("P1 双曲外推：D→2 端预言标尺")
ax.legend(fontsize=8)

fig.suptitle("P1 多盆地扩展（2026-08-10 转录）：D 分布与双曲外推标尺", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(os.path.join(OUT, "p1_multibasin_extension.png"), dpi=150)
print(f"\n图已保存：{os.path.join(OUT, 'p1_multibasin_extension.png')}")
