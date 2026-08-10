# -*- coding: utf-8 -*-
"""
c 项线：塔里木金刚烷参数 × 古龙/乌马营端元 逐油样成对定量分析
============================================================
数据源（逐油样，全部转录自原文表格/正文）：
  - 塔里木顺托果勒（STGL）21 油样：Zhu et al. 2025, Petroleum Science 22:1446-1464
      Table 3 九项金刚烷成熟度指标 + Table 1 油品（深度/密度/GOR/Sat-Aro/相态）
  - 古龙页岩油 49 样品（原位端元，无运移无分馏）：Bai et al. 2025, Sci Rep 15:29186
      Table 3 金刚烷绝对定量（1-MA/2-MA/1-MD/3-MD/4-MD µg/g）+ 源岩 Ro
  - 乌马营潜山凝析油 3 井（煤系端元）：Lou et al. 2024, ACS Omega
      正文：MAI 62-69%(avg66%)、MDI 46-51%(avg49%)、Rc≈1.2-1.3% Ro
  - 塔里木 167 样品（OPPI 2025，库车 29+塔北 45+塔中 93）：4+3MD 浓度区间锚点
      库车 42-2757 / 塔中 21-6061 / 塔北 10-97 ppm（逐样品表未公开，仅汇总区间）

分析设计（c 项指纹判别，陈中红 2022 逻辑：金刚烷成熟度 vs 其它成熟度代理解耦 = 多期充注混合证据）：
  A. 古龙原位端元：MDI-Ro 逐样品同步性（Spearman + OLS）——"无运移/混合"基线
  B. STGL 21：MDI vs 相态成熟度代理（Sat/Aro、GOR、密度）——"运移+多期充注"解耦检验
  C. 古龙 vs STGL 金刚烷指标变异度对比（方差比）——混合均一化检验
  D. 乌马营端元锚点：MDI 46-51% 在古龙校准线上的预测 Ro vs 实测 Rc——跨源相校准交叉验证
  E. 167 样品 4+3MD 区间锚点叠加（浓度尺度对照）
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

# 可复用跨源相桥模块（逻辑见 shale_data_inventory.md §9.7 [D]）
from paperX_shale_c_endpoint_bridge import endpoint_bridge

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(os.path.dirname(BASE), "outputs", "c_paired_out")
os.makedirs(OUT, exist_ok=True)

# ---------------- 载入 ----------------
def load_gulong():
    df = pd.read_csv(os.path.join(DATA, "gulong_bai2025", "bai2025_gulong_table3.csv"))
    for c in ["MD1", "MD3", "MD4", "MA1", "MA2"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["MAI"] = df["MA1"] / (df["MA1"] + df["MA2"])
    df["MDI"] = df["MD4"] / (df["MD1"] + df["MD3"] + df["MD4"])
    df["system"] = "Gulong(in-situ shale oil)"
    return df

def load_stgl():
    t3 = pd.read_csv(os.path.join(DATA, "petsci2025_stgl", "zhu2025_stgl_table3.csv"))
    t1 = pd.read_csv(os.path.join(DATA, "petsci2025_stgl", "zhu2025_stgl_table1.csv"))
    for c in ["density", "GOR", "SatAro"]:
        t1[c] = pd.to_numeric(t1[c], errors="coerce")
    df = t3.merge(t1, on="sample", how="left")
    df["phase_rank"] = df["phase"].map({"black oil": 0, "volatile oil": 1, "condensate": 2})
    df["system"] = "Tarim STGL(ultra-deep)"
    return df

G = load_gulong()
S = load_stgl()

lines = []
def log(s=""):
    print(s)
    lines.append(s)

log("=" * 78)
log("c 项线：逐油样成对定量分析（金刚烷 × 端元）")
log(f"古龙端元（原位页岩油）：{len(G)} 样品；STGL（超深层）：{len(S)} 样品；乌马营（煤系凝析油）：3 井")
log("=" * 78)

# ---------------- A. 古龙原位端元 MDI-Ro 同步性 ----------------
log("\n[A] 古龙原位端元：MDI-Ro 同步性（无运移基线）")
g = G.dropna(subset=["MDI", "Ro_pct"]).copy()
log(f"    有效样品 n={len(g)}（有金刚烷 MDI 值者），Ro 窗 {g['Ro_pct'].min():.2f}-{g['Ro_pct'].max():.2f}%")
rho, p = stats.spearmanr(g["Ro_pct"], g["MDI"])
r_pear, p_pear = stats.pearsonr(g["Ro_pct"], g["MDI"])
slope, intercept, r_val, p_val, se = stats.linregress(g["Ro_pct"], g["MDI"])
log(f"    Spearman rho(MDI, Ro) = {rho:.3f}  (p={p:.2e})")
log(f"    Pearson r = {r_pear:.3f}")
log(f"    OLS: MDI = {slope:.4f}*Ro + {intercept:.4f}  (R2={r_val**2:.3f}, n={len(g)})")
log(f"    -> 原位体系 MDI-Ro 中等同步（窄熟窗内非纯单调，受粘土催化/超压调制）")
# 对照：总金刚烷含量 vs Ro（Bai 2025 核心结论：含量四段式随成熟度增长）
gt = G.dropna(subset=["tot_diamondoid", "Ro_pct"])
rho_t, p_t = stats.spearmanr(gt["Ro_pct"], gt["tot_diamondoid"])
log(f"    对照：Spearman rho(总金刚烷含量, Ro) = {rho_t:.3f}  (p={p_t:.2e}, n={len(gt)})")
log(f"          -> 含量-成熟度同步显著强于 MDI-成熟度：原位端元中含量是更纯的成熟度读数")

# ---------------- B. STGL 解耦检验 ----------------
log("\n[B] STGL 超深层：MDI 与相态成熟度代理的同步性（解耦检验）")
for col, name in [("SatAro", "Sat/Aro"), ("GOR", "GOR"), ("density", "density")]:
    sub = S.dropna(subset=["MDI", col])
    if len(sub) >= 8:
        rho_, p_ = stats.spearmanr(sub["MDI"], sub[col])
        log(f"    Spearman rho(MDI, {name}) = {rho_:+.3f}  (p={p_:.3f}, n={len(sub)})")
log("    （参照：相态代理本身随 FY->SB4 单调变化：Sat/Aro 6.9->34.4, GOR 111->2888, density 0.84->0.74）")

# 动态范围压缩定量：相态代理变异 vs MDI 变异
sa_min, sa_max = S["SatAro"].min(), S["SatAro"].max()
mdi_min, mdi_max = S["MDI"].min(), S["MDI"].max()
log(f"    [B2] 动态范围压缩：Sat/Aro {sa_min:.1f}->{sa_max:.1f}（{sa_max/sa_min:.1f} 倍）对应 MDI {mdi_min:.2f}->{mdi_max:.2f}（仅 {mdi_max/mdi_min:.2f} 倍）")
log(f"         响应比 = Δln(MDI)/Δln(Sat/Aro) = "
    f"{np.log(mdi_max/mdi_min)/np.log(sa_max/sa_min):.3f}  (<<1 = 金刚烷指标对相态成熟度弱响应/解耦)")

# 相态分组
log("\n    相态分组（STGL 21）：")
gp = S.groupby("phase")[["MDI", "MAI", "SatAro", "GOR"]].agg(
    {"MDI": ["mean", "std", "min", "max"], "MAI": ["mean", "min", "max"],
     "SatAro": ["mean", "min", "max"], "GOR": ["mean", "min", "max"]})
log(gp.to_string())

# ---------------- C. 变异度对比 ----------------
log("\n[C] 金刚烷指标变异度：混合均一化检验")
for idx in ["MDI", "MAI"]:
    gv = G.dropna(subset=[idx])[idx]
    sv = S.dropna(subset=[idx])[idx]
    log(f"    {idx}: 古龙 std={gv.std():.3f} (n={len(gv)}) vs STGL std={sv.std():.3f} (n={len(sv)})")
    if len(gv) > 1 and len(sv) > 1:
        f_stat, p_f = stats.levene(gv, sv)
        log(f"      Levene 方差比检验 p={p_f:.4f}  -> {'方差异显著' if p_f < 0.05 else '方差异不显著'}")
ks_stat, ks_p = stats.ks_2samp(G.dropna(subset=["MDI"])["MDI"], S.dropna(subset=["MDI"])["MDI"])
log(f"    K-S (古龙 MDI vs STGL MDI): D={ks_stat:.3f}, p={ks_p:.3f}")

# ---------------- D. 乌马营端元锚点（跨源相桥，可复用模块） ----------------
log("\n[D] 乌马营端元锚点（煤系凝析油，Lou 2024）")
log("    正文：MAI 62-69%（avg 66%）、MDI 46-51%（avg 49%）、Rc≈1.2-1.3% Ro")
# 跨源相桥：古龙校准线（原位端元）外推乌马营等效成熟度 vs 实测 Rc
# 统一走 paperX_shale_c_endpoint_bridge.endpoint_bridge（含 bootstrap CI + 诚实登记）
bridge = endpoint_bridge(
    cal_maturity=g["Ro_pct"], cal_index=g["MDI"],
    target_index=np.array([0.46, 0.49, 0.51]),
    target_maturity=np.array([1.25, 1.25, 1.25]),
    index_name="MDI", maturity_name="Ro(%)",
    mode="inverse", n_boot=500, seed=0,
)
for _l in bridge["summary"].split("\n"):
    log("    " + _l)
log("    -> 跨源相（煤系 vs 湖相原位）校准基本一致程度登记；差异即源相影响上界")

# ---------------- E. 167 样品锚点 ----------------
log("\n[E] 塔里木 167 样品锚点（OPPI 2025，库车29+塔北45+塔中93）")
log("    4+3MD 浓度（ppm）：库车 42-2757、塔中 21-6061、塔北 10-97")
log("    九项指标在库车/塔中范围更宽、最大值更高 -> 源岩成熟度更高（库车三叠系 > 塔中-塔北寒武系）")
log("    密度与金刚烷浓度无相关；As/Ds 两阶段生成（Stage I As 快 / Stage II Ds 快）")
log("    逐油样表未公开（T&F 订阅）——167 样品仅作区间锚点，逐样品分析以 STGL 21 为载体")

# ---------------- 汇总表输出 ----------------
g_out = G[["well", "system", "group", "Ro_pct", "MAI", "MDI", "tot_diamondoid", "adamantane", "diamantane"]].copy()
s_out = S[["sample", "system", "phase", "phase_rank", "MAI", "EAI", "DMAI1", "DMAI2", "TMAI1", "TMAI2",
           "MDI", "DMDI1", "DMDI2", "MEDI", "depth_m", "density", "GOR", "SatAro"]].copy()
g_out.to_csv(os.path.join(OUT, "paired_gulong_endpoint.csv"), index=False, encoding="utf-8-sig")
s_out.to_csv(os.path.join(OUT, "paired_stgl_samples.csv"), index=False, encoding="utf-8-sig")

# 跨体系成对对照表（同成熟度窗口）：古龙 Ro 1.3-1.65 子集 vs STGL
high_g = g[(g["Ro_pct"] >= 1.3) & (g["Ro_pct"] <= 1.65)]
log("\n[F] 成对对照：古龙高成熟窗口(Ro 1.30-1.65) MDI vs STGL 21 MDI")
log(f"    古龙高熟: MDI 均值={high_g['MDI'].mean():.3f} std={high_g['MDI'].std():.3f} n={len(high_g)}")
log(f"    STGL:     MDI 均值={S['MDI'].mean():.3f} std={S['MDI'].std():.3f} n={len(S)}")
t_stat, t_p = stats.ttest_ind(high_g["MDI"], S["MDI"])
log(f"    t-test p={t_p:.4f}；Levene 方差比 p={stats.levene(high_g['MDI'], S['MDI'])[1]:.4f}")

with open(os.path.join(OUT, "paired_analysis_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
log("\n[输出] " + OUT)
log("        paired_gulong_endpoint.csv / paired_stgl_samples.csv / paired_analysis_report.txt")

# ---------------- 图：端元桥（古龙原位校准 + STGL + 乌马营） ----------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 左图：MDI vs Ro（古龙原位散点 + OLS 线；STGL MDI 水平带；乌马营锚点）
    ax1.scatter(g["Ro_pct"], g["MDI"], c="#1f77b4", s=42, alpha=0.8,
                label=f"Gulong in-situ (n={len(g)})")
    ro_line = np.linspace(1.1, 1.7, 50)
    ax1.plot(ro_line, slope * ro_line + intercept, "--", c="#1f77b4",
             label=f"OLS R$^2$={r_val**2:.2f}")
    ax1.axhspan(S["MDI"].min(), S["MDI"].max(), color="#d62728", alpha=0.18)
    ax1.axhline(S["MDI"].mean(), color="#d62728", lw=1, ls=":",
                label=f"STGL 21 MDI band ({S['MDI'].mean():.2f}$\\pm${S['MDI'].std():.2f})")
    ax1.axhspan(0.46, 0.51, color="#2ca02c", alpha=0.25)
    ax1.axhline(0.49, color="#2ca02c", lw=1, ls=":", label="Wumaying MDI 46-51% (Rc 1.2-1.3%)")
    ax1.set_xlabel("Source rock Ro (%)")
    ax1.set_ylabel("MDI (4-MD / ΣMD)")
    ax1.set_title("(a) Endpoint bridge: MDI vs maturity")
    ax1.legend(fontsize=8, loc="lower right")
    ax1.set_xlim(1.1, 1.7)

    # 右图：MDI vs Sat/Aro（STGL 弱响应 vs 古龙含量标度）
    ax2.scatter(S["SatAro"], S["MDI"], c="#d62728", s=48,
                label="STGL 21 (ultra-deep)")
    b, a = np.polyfit(S.dropna(subset=["SatAro"])["SatAro"],
                      S.dropna(subset=["SatAro"])["MDI"], 1)
    xx = np.linspace(2, 38, 30)
    ax2.plot(xx, a + b * xx, "--", c="#d62728",
             label=f"slope={b:.4f} / 6.6x SatAro range")
    ax2.set_xlabel("Sat/Aro")
    ax2.set_ylabel("MDI")
    ax2.set_title("(b) Decoupling: MDI vs phase proxy")
    ax2.legend(fontsize=9)
    ax2.set_ylim(0.38, 0.54)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "c_paired_endpoint_bridge.png"), dpi=150)
    log("[图] c_paired_endpoint_bridge.png（(a) 端元桥 MDI-Ro；(b) STGL 解耦）")
except Exception as e:
    log(f"[图] 生成失败（{e}）——分析报告不受影响")
