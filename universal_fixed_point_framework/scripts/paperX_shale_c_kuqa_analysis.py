# -*- coding: utf-8 -*-
"""
c 项线：库车端元（Zhang 2026, Sci Rep 16:14334）逐油样分析
============================================================
数据源：Kuqa Depression 13 地区 60 轻油样品（Wushi/Bozi/Dabei/Keshen/Kela/Dina/
        Dibei/Tuzi/Tudong/Yangtake/Yingmai/Hongqi/Yaha）
  - Table 1: 区域/样品/层位/深度/族组分/C29甾烷
  - Table 2: 金刚烷浓度（As/Ds/Ts/Total/4+3-MDs）+ 10 异构化比值（MAI/EAI/DMAI1/2/
             TMAI1/2/MDI/DMDI1/2/MTI）+ MAs/MDs + %Rc(=2.4389·MDI+0.4363) + EASY%Ro
             + 源相判别（Jiang 模型）
端元分组（正文 §Source facies）：湖相 II = {Kela,Keshen,Yangtake,Yaha}；
煤系 III = {Wushi,Bozi,Dabei,Dina,Tuzi,Yingmai,Hongqi}；混合 = {Dibei,Tudong}
分析设计：
  G. 库车 MDI-EASY%Ro 同步性（OLS+Spearman，源相分组）——源相影响随成熟度检验
  H. 跨源相桥：古龙校准线（原位湖相页岩油）外推库车 60 样品 MDI -> 外推 Ro vs EASY%Ro
     偏差分布（源相影响上界的独立批量复现，vs 乌马营 3 井锚点）
  I. 库车 vs STGL 金刚烷指标变异度对比——混源/成熟度跨度大体系的均一化对照
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

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
    df["MDI"] = df["MD4"] / (df["MD1"] + df["MD3"] + df["MD4"])
    df["MAI"] = df["MA1"] / (df["MA1"] + df["MA2"])
    return df

# 样品 -> 区域（表 1 rowspan 合并单元格，Region 以论文表 1 顺序为准）
SAMPLE_REGION = {
    "SM1": "Wushi", "SM2": "Wushi", "WC1-1": "Wushi", "WC1-2": "Wushi",
    "AW3": "Bozi", "BZ1": "Bozi", "BZ102": "Bozi", "BZ104": "Bozi", "BZ3": "Bozi",
    "DB101": "Dabei", "DB101-1": "Dabei", "DB1": "Dabei", "DB11": "Dabei",
    "DB2": "Dabei", "DB201": "Dabei", "DB208": "Dabei", "DB301": "Dabei",
    "KS102": "Keshen", "KS103": "Keshen", "KS204": "Keshen",
    "KL201-1": "Kela", "KL201-2": "Kela", "KL201-3": "Kela", "KL203": "Kela", "KL3": "Kela",
    "DN102": "Dina", "DN11": "Dina", "DN2": "Dina", "DN201": "Dina",
    "DN202": "Dina", "DN204": "Dina", "DN22": "Dina",
    "DX1": "Dibei", "Y603": "Dibei", "YN2-1": "Dibei", "YN2-2": "Dibei", "YN5": "Dibei",
    "TZ1": "Tuzi", "TZ3": "Tuzi",
    "TD2": "Tudong", "TD201": "Tudong",
    "QL1": "Yangtake", "YT1T": "Yangtake", "YT2": "Yangtake", "YT101": "Yangtake",
    "YM7": "Yingmai", "YM9": "Yingmai", "YM16": "Yingmai", "YM17": "Yingmai",
    "YM19": "Yingmai", "YM21": "Yingmai", "YM35": "Yingmai", "YM41": "Yingmai",
    "HQ1": "Hongqi", "HQ2": "Hongqi",
    "YH5-1": "Yaha", "YH5-2": "Yaha", "YH701-1": "Yaha", "YH701-2": "Yaha", "YH7x-1": "Yaha",
}

def load_kuqa():
    t2 = pd.read_csv(os.path.join(DATA, "kuqa_zhang2026", "zhang2026_kuqa_table2.csv"))
    colmap = {
        "1": "As_ppm", "2": "Ds_ppm", "3": "Ts_ppm", "4": "Total_ppm", "5": "MD4_3_ppm",
        "6": "MAI", "7": "EAI", "8": "DMAI1", "9": "DMAI2", "10": "TMAI1",
        "11": "TMAI2", "12": "MDI", "13": "DMDI1", "14": "DMDI2", "15": "MTI",
        "16": "MAs_MDs", "17": "Rc_pct", "18": "EASY_Ro", "19": "Facies",
    }
    t2 = t2.rename(columns=colmap)
    for c in colmap.values():
        if c != "Facies":
            t2[c] = pd.to_numeric(t2[c], errors="coerce")
    df = t2.copy()
    df["region"] = df["Sample"].map(SAMPLE_REGION)
    # 端元分组（论文正文 §Source facies）
    LACU = ["Kela", "Keshen", "Yangtake", "Yaha"]
    COAL = ["Wushi", "Bozi", "Dabei", "Dina", "Tuzi", "Yingmai", "Hongqi"]
    df["endmember"] = df["region"].map(
        lambda r: ("lacustrine-II" if r in LACU else ("coaly-III" if r in COAL else "mixed")))
    df["system"] = "Kuqa(high-maturity light oil)"
    return df

G = load_gulong()
K = load_kuqa()

lines = []
def log(s=""):
    print(s)
    lines.append(s)

log("=" * 78)
log("c 项线：库车端元（Zhang 2026, Sci Rep 16:14334）逐油样分析")
log(f"库车：{len(K)} 样品 / {K['region'].nunique()} 地区；EASY%Ro {K['EASY_Ro'].min():.2f}-{K['EASY_Ro'].max():.2f}")
log("=" * 78)

# ---------------- G. 库车 MDI-EASY%Ro 同步性 ----------------
log("\n[G] 库车 MDI-EASY%Ro 同步性（源相分组）")
gv = K.dropna(subset=["MDI", "EASY_Ro"])
rho, p = stats.spearmanr(gv["EASY_Ro"], gv["MDI"])
slope, intercept, r_val, p_val, se = stats.linregress(gv["EASY_Ro"], gv["MDI"])
log(f"    全体 n={len(gv)}: Spearman rho(MDI, EASY%Ro)={rho:.3f} (p={p:.2e})")
log(f"    OLS: MDI = {slope:.4f}*EASY%Ro + {intercept:.4f}  (R2={r_val**2:.3f})")
for em in ["lacustrine-II", "coaly-III", "mixed"]:
    sub = gv[gv["endmember"] == em]
    if len(sub) >= 4:
        rs, ps = stats.spearmanr(sub["EASY_Ro"], sub["MDI"])
        log(f"    {em} (n={len(sub)}): rho={rs:.3f} (p={ps:.3f})  "
            f"MDI 中位={sub['MDI'].median():.3f}  EASY%Ro 中位={sub['EASY_Ro'].median():.2f}")
log("    -> 库车（高熟轻油/混源）MDI-成熟度同步弱于古龙原位？= 混源/蒸发分馏调制")

# ---------------- H. 跨源相桥 ----------------
log("\n[H] 跨源相桥：古龙原位校准线外推库车 MDI vs 库车 EASY%Ro")
gcal = G.dropna(subset=["MDI", "Ro_pct"])
log(f"    古龙校准线：n={len(gcal)}，Ro 窗 {gcal['Ro_pct'].min():.2f}-{gcal['Ro_pct'].max():.2f}%，"
    f"MDI 窗 {gcal['MDI'].min():.3f}-{gcal['MDI'].max():.3f}")
bridge = endpoint_bridge(
    cal_maturity=gcal["Ro_pct"], cal_index=gcal["MDI"],
    target_index=K.dropna(subset=["MDI", "EASY_Ro"])["MDI"].values,
    target_maturity=K.dropna(subset=["MDI", "EASY_Ro"])["EASY_Ro"].values,
    index_name="MDI", maturity_name="Ro(%)",
    mode="inverse", n_boot=500, seed=0,
)
for _l in bridge["summary"].split("\n"):
    log("    " + _l)
log("    -> 全样品偏差 = 库车（高熟混源轻油）源相+混源影响上界，独立批量复现")

# 分源相组偏差
gv2 = K.dropna(subset=["MDI", "EASY_Ro"]).copy()
slope_c, int_c, _, _, _ = stats.linregress(gcal["Ro_pct"], gcal["MDI"])
gv2["pred_Ro"] = (gv2["MDI"] - int_c) / slope_c
gv2["dev"] = gv2["pred_Ro"] - gv2["EASY_Ro"]
for em in ["lacustrine-II", "coaly-III", "mixed"]:
    sub = gv2[gv2["endmember"] == em]
    if len(sub) >= 4:
        log(f"    {em} (n={len(sub)}): 偏差 中位={sub['dev'].median():+.2f} "
            f"IQR=[{sub['dev'].quantile(0.25):+.2f},{sub['dev'].quantile(0.75):+.2f}] "
            f"|pred|中位={sub['pred_Ro'].median():.2f} vs EASY 中位={sub['EASY_Ro'].median():.2f}")

# ---------------- I. 变异度/浓度对照 ----------------
log("\n[I] 库车 vs 古龙/STGL 金刚烷指标对照")
for idx in ["MDI", "MAI"]:
    kv = K.dropna(subset=[idx])[idx]
    gv_ = G.dropna(subset=[idx])[idx]
    log(f"    {idx}: 库车 std={kv.std():.3f} (n={len(kv)}, 中位={kv.median():.3f}) "
        f"vs 古龙 std={gv_.std():.3f} (n={len(gv_)}, 中位={gv_.median():.3f})")
log(f"    库车 MDI 全距：{K['MDI'].min():.3f}-{K['MDI'].max():.3f}（EASY%Ro 0.81-2.44，成熟度跨度驱动的变异，非混合均一化）")
log(f"    库车总金刚烷浓度：{K['Total_ppm'].min():.0f}-{K['Total_ppm'].max():.0f} ppm（vs 古龙 {G['tot_diamondoid'].min():.0f}-{G['tot_diamondoid'].max():.0f} µg/g）")

# 输出
K.to_csv(os.path.join(OUT, "paired_kuqa_samples.csv"), index=False, encoding="utf-8-sig")
with open(os.path.join(OUT, "paired_kuqa_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
log("\n[输出] " + OUT)
log("        paired_kuqa_samples.csv / paired_kuqa_report.txt")

# ---------------- 图 ----------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    # 左：MDI vs EASY%Ro 分源相
    colors = {"lacustrine-II": "#1f77b4", "coaly-III": "#d62728", "mixed": "#9467bd"}
    for em, c in colors.items():
        sub = gv2[gv2["endmember"] == em]
        ax1.scatter(sub["EASY_Ro"], sub["MDI"], c=c, s=36, alpha=0.85, label=em)
    ax1.plot(gcal["Ro_pct"], slope_c * gcal["Ro_pct"] + int_c, "k--",
             label=f"Gulong cal line (in-situ)")
    ax1.set_xlabel("EASY%Ro (Kuqa) / Ro (Gulong)")
    ax1.set_ylabel("MDI")
    ax1.set_title("(a) Kuqa MDI vs maturity by source facies")
    ax1.legend(fontsize=8)
    # 右：偏差 vs EASY%Ro
    ax2.scatter(gv2["EASY_Ro"], gv2["dev"], c=gv2["endmember"].map(colors), s=36, alpha=0.85)
    ax2.axhline(0, color="k", lw=0.8)
    ax2.axhspan(0.5, 0.6, color="#2ca02c", alpha=0.15, label="Wumaying +0.5~0.6% (3 wells)")
    ax2.set_xlabel("EASY%Ro")
    ax2.set_ylabel("predicted Ro - EASY%Ro")
    ax2.set_title("(b) Cross-source bridge deviation (Kuqa 60)")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "c_kuqa_endpoint_bridge.png"), dpi=150)
    log("[图] c_kuqa_endpoint_bridge.png")
except Exception as e:
    log(f"[图] 生成失败（{e}）")
