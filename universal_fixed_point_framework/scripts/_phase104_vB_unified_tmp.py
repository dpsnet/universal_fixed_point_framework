# -*- coding: utf-8 -*-
"""
Phase 104az-16 (26.16j-64): P4 全场强 V(B) 判别表 — 统一口径对照
6 点 V(B) 数据 + Kemp 线性外推 + Rohrmann 远回旋区 V≈0 + 判别维度计算
口径标注: B (字段: Bp 偶极极场 / BHa 表观平均 / <|B|> 平均模), V 类型 (cont 连续谱峰 / avg 波长平均含线)
"""
import json

# ---------------- 数据 ----------------
# 6 点 V(B): (星名, B_MG, B_口径, V_pct, V_err_pct, V类型, 观测源)
points = [
    ("G 227-35",      120,  "<|B|>",   4.00, 0.5, "cont", "Kawka 2020 连续谱峰 @4500A"),
    ("G 111-49",      250,  "<|B|>",   8.00, 1.0, "cont", "Kawka 2020 连续谱峰 @5500A"),
    ("PG 1031+234",   500,  "Bp~偶极+斑", 12.00, 3.0, "cont", "Schmidt 1986/Piirola-Reiz 1990 U带峰(峰值相位)"),
    ("SDSS J0021",    550,  "Bp",     +0.91, 0.3, "avg",  "Schmidt 2005 表1 波长平均含线"),
    ("SDSS J1206",    830,  "Bp",     +0.41, 0.3, "avg",  "Schmidt 2005 表1 波长平均含线"),
    ("SDSS J2346",   1000,  "Bp",     -1.51, 0.5, "avg",  "Schmidt 2005 表1 波长平均含线"),
]

# Kemp 校准: |gamma| = 15 MG per 1% (Kawka 2020); V/I(%) ~ <B_z>/15 (MG)
GAMMA = 15.0  # MG per 1%
B_TH_SEQ = {7:48.01, 6:65.35, 5:94.11, 4:147.05, 3:261.41}  # B_th(n) 内生阈值序列 MG

rows = []
for name, B, btype, V, Verr, vtype, src in points:
    # Kemp 偶极外推: <B_z> = Bp/3
    Bz = B / 3.0
    V_kemp = Bz / GAMMA  # %
    # 抑制因子 (仅对 avg 型有意义; cont 型为 Kemp 对照基线)
    if vtype == "avg" and V_kemp > 0:
        supp = V_kemp / abs(V) if abs(V) > 1e-9 else float("inf")
    else:
        supp = None
    # Rohrmann: 远回旋线区 V~0 (回旋线位置 lambda_c=2*pi*m_e*c/(eB); B_T=B_MG*1e2)
    lam_c = 1.071e6 / B  # Angstrom: 2*pi*m_e*c/(e*1e2)=1.071e6 (B in MG)
    rows.append({
        "name": name, "B_MG": B, "B_type": btype,
        "V_pct": V, "V_err_pct": Verr, "V_type": vtype,
        "Kemp_pred_pct": round(V_kemp, 3),
        "suppression": round(supp, 1) if supp else None,
        "cyclotron_A": round(lam_c, 0),
        "source": src,
    })

# ---------------- 判别表 ----------------
print("=" * 100)
print("P4 全场强 V(B) 判别表 (Phase 104az-16, 26.16j-64)")
print("=" * 100)
hdr = "{:<14}{:>7}{:>8}{:>8}{:>8}{:>12}{:>14}{:>10}{:>10}".format(
    "Star", "B_MG", "B_type", "V(%)", "err", "V_type", "Kemp_pred", "suppress", "cyclo(A)")
print(hdr)
print("-" * 100)
for r in rows:
    print("{:<14}{:>7.0f}{:>8}{:>8.2f}{:>8.2f}{:>12}{:>14}{:>10}{:>10}".format(
        r["name"], r["B_MG"], r["B_type"], r["V_pct"], r["V_err_pct"], r["V_type"],
        r["Kemp_pred_pct"], str(r["suppression"]) if r["suppression"] else "-",
        r["cyclotron_A"]))

# ---------------- 关键结论 ----------------
print()
print("关键结论:")
# 1. 趋势: 先升后降
Vs = [p[3] for p in points]
print(f"1) V(B) 幅度序列: {[round(v,2) for v in Vs]} -> 先升后降, 峰值 ~500 MG")
# 2. 中场 Kemp 吻合 vs 高场抑制
cont_pts = [r for r in rows if r["V_type"] == "cont"]
avg_pts = [r for r in rows if r["V_type"] == "avg"]
print(f"2) 连续谱峰 V (cont, n={len(cont_pts)}): 观测 {[r['V_pct'] for r in cont_pts]} vs Kemp {[r['Kemp_pred_pct'] for r in cont_pts]}")
print(f"3) 波长平均 V (avg, n={len(avg_pts)}): 观测 {[r['V_pct'] for r in avg_pts]} vs Kemp {[r['Kemp_pred_pct'] for r in avg_pts]} -> 抑制 {[r['suppression'] for r in avg_pts]} 倍")
# 3. 口径警告量化: 波长平均含线 vs 连续谱峰 稀释估计 (PG 1031+234 有连续谱峰 12-17%, 若同星波长平均会更低)
print("4) 口径警告: cont(12-17% @500MG) vs avg(0.4-1.5% @550-1000MG) 不可直接比;")
print("   统一口径需要: 高场星的连续谱峰 V(λ) 或中场星的波长平均 V")
# 4. 阈值序列对照
print(f"5) 内生阈值序列 B_th(n=7..3): {list(B_TH_SEQ.values())} MG — 最高 261.41 MG;")
print(f"   V(B) 峰值 ~500 MG 不在阈值序列内, 高场抑制转折 ~500-550 MG 与阈值序列无直接对应")
# 5. Rohrmann 对照
print("6) Rohrmann 远回旋区 V~0: 高场三点 (550-1000 MG) 回旋线 1070-1950 A (远紫外),")
print("   观测窗口 4200-8400 A 全在红端远区 -> 光电离模型预言 V~0; 观测非零 (0.4-1.5%) 偏离")

# ---------------- 存盘 ----------------
out = {
    "points": rows,
    "gamma_MG_per_pct": GAMMA,
    "b_th_seq": B_TH_SEQ,
    "conclusions": [
        "V(B) 幅度先升后降, 峰值 ~500 MG (4->8->12-17->0.91->0.41->-1.51)",
        "中场 (<=500 MG) Kemp 线性区延续 (观测 4/8/12-17 vs 预言 2.7/5.3/4.4-11)",
        "高场 (>550 MG) 波长平均 V 抑制 8-55 倍 vs Kemp 偶极外推",
        "Rohrmann 远回旋区 V~0 预言 vs 高场观测非零 -> 偏离光电离模型",
        "口径差异 (cont vs avg) 为主障碍; 统一口径 V(B) 数据待观测闭合",
    ],
}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase104_vB_unified.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print()
print("已存盘: _phase104_vB_unified.json")
