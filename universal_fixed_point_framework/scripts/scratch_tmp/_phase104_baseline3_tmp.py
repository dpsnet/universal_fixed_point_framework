# -*- coding: utf-8 -*-
"""Phase 104az-58：标准束缚态溶解量级检验——by_n 存活率 vs 观测缺失
问题：KIMI 断言标准 l-混合/溶解可解释中场缺失——用论文已有 3D by_n 数据对照
注意：by_n 是态计数（束缚 vs 非束缚二元），非振子强度损失——给"溶解=全损失"上界
"""
import json

base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
with open(base + r"\paperX_eta_sc_n.json", encoding="utf-8") as f:
    data = json.load(f)
raw = data["raw"]
# B 网格：0.005=11.75, 0.01=23.5, 0.02=47, 0.05=117.5, 0.1=235 MG
# 零场参考态数（B=0.005 最低场近似）：n=3:6, n=4:9, n=5:7, n=6:8, n=7:2
ref = {3: 6, 4: 9, 5: 7, 6: 8, 7: 2}
obs_mid = {3: 0.0, 4: 0.27, 5: 0.41, 6: 0.12, 7: 0.02}  # 观测变浅序（41MG 分档近似）
obs_hi  = {3: 0.02, 4: 0.27, 5: 0.41, 6: 0.12, 7: 0.02}

print("=== 标准束缚态溶解率（by_n 态计数，溶解=全损失上界） vs 观测缺失 ===")
print("B(MG) |  n=3(Hα)  n=4(Hβ)  n=5(Hγ)  n=6(Hδ)  n=7(Hε)")
prev = raw[0]["by_n"]
for rec in raw:
    B_mg = rec["B"] * 2350
    by = rec["by_n"]
    print("B=%6.1f |" % B_mg, end="")
    for n in (3,4,5,6,7):
        cur = by.get(str(n), 0)
        r = ref[n]
        loss = 1.0 - cur/r if r > 0 else 1.0
        print("  %5.1f%%" % (100*loss), end="")
    print()

print("\n观测（41MG 分档近似变浅序）：Hα 0-2% / Hβ 27% / Hγ 41% / Hδ 12% / Hε 2%")
print("\n=== 量级对照（中场中位 22.8 MG ≈ B=0.01，溶解率） ===")
rec_mid = [r for r in raw if abs(r["B"]-0.01) < 1e-6][0]
by = rec_mid["by_n"]
for n in (3,4,5,6,7):
    r = ref[n]
    loss = 1.0 - by.get(str(n),0)/r
    print("  n=%d(%s)：溶解 %.0f%% vs 观测缺失 %.0f%% → %s" % (
        n, {3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ",7:"Hε"}[n], 100*loss, 100*obs_mid[n],
        "标准溶解可解释/过解释" if 100*loss >= 100*obs_mid[n]*0.8 else "标准溶解不足"))
print("\n注意：by_n 是态计数非振子强度；溶解≠强度全失；n 在强场非好量子数（归类有噪声）——")
print("此表为量级上界，决定性定量需从混合态本征解算振子强度分布（KIMI 建议）")
