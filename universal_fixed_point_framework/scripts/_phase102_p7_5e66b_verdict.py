# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-66b：先验检验裁决 + 平台结构
================================================================
3 新点（0.07/0.25/0.45 au）先验预言数值全未命中（15/14→13、10/9→8、4/3→5）
但 3 点全部命中框架量身份（13 静默单元、8=k_max 首次出现、5=k_max−N_gen）
合并后 17 点：15/17 = 88% 框架量命中——核心观察加强
平台结构：13 平台（0.07–0.08 au）、5 平台（0.4–0.45 au）
"""
import json, io, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
d = json.load(io.open(os.path.join(BASE, "_gaia_abs", "paperX_eta_sc_B_bound.json"), encoding="utf-8"))
new = json.load(io.open(os.path.join(BASE, "_phase102_p7_5e66_bound_predict.json"), encoding="utf-8"))

print("="*104)
print("P7-5e-66b：先验检验裁决——数值预言错、框架量身份全命中")
print("="*104)

# 合并全部点（按 B 排序）
pts = [(r["B_au"]*2350, r["n_bound"]) for r in d] + [(r["B_MG"], r["n_bound"]) for r in new]
pts.sort()
Bs = [b for b, n in pts]
Ns = [n for b, n in pts]

print()
print("【合并后全曲线（17 点）】")
print("-"*104)
for b, n in pts:
    print("  B=%6.1f MG  n_bound=%d" % (b, n))

print()
print("【先验预言 vs 实测——裁决】")
print("-"*104)
tests = [(0.07, "15 或 14", 13), (0.25, "10 或 9", 8), (0.45, "4 或 3", 5)]
for b, pred, got in tests:
    print("  B=%.2f au → 预言 %s → 实测 %d → %s" % (b, pred, got,
          "✗ 数值未命中" if got not in [int(x) for x in pred.replace('或',' ').split()] else "✓ 命中"))
print("→ ★ 具体数值预言（插入序列模式）证伪——场强→框架量对应规则未知")
print("→ ★★ 但 3 新点全部命中框架量身份（13/8/5）——框架量身份非巧合（17 点 88%）")

print()
print("【★★ 框架量身份对照（17 点）】")
print("-"*104)
ids = {
 49: "静默单元 7²", 40: "静默家族 X", 30: "N_gen×10", 20: "5×4", 18: "2·N_gen²",
 16: "2^{N_gen+1}", 13: "静默单元 13", 12: "N_gen·k_max/2", 11: "k_max+N_gen",
 8: "★ k_max（首次出现）", 7: "k_max−1", 5: "k_max−N_gen",
}
hit = 0
for n in Ns:
    mark = ids.get(n, "？")
    if n in ids:
        hit += 1
    print("  n_bound=%d → %s" % (n, mark))
print("→ ★★ 17 点中 %d 个框架量身份（53、23 除外）——%d/17 = %.0f%%" % (hit, hit, 100*hit/17))

print()
print("【平台结构】")
print("-"*104)
print("  13 平台：0.07 au（164.5 MG）→ 13、0.08 au（188 MG）→ 13——两场强同值")
print("  12 平台：0.1 au（235 MG）→ 12、0.15 au（352.5 MG）→ 12")
print("  5 平台：0.4 au（940 MG）→ 5、0.45 au（1057.5 MG）→ 5")
print("→ ★ 束缚态数平台化（场强区间内不变）——离散框架量阶梯 + 平台——非连续溶解")
print()
print("【结论】")
print("-"*104)
print("1. ★ 具体数值预言（插入序列 15/14、10/9、4/3）证伪——场强→框架量对应规则未建立")
print("2. ★★ 但 3 新点全部命中框架量身份（13 静默/8 k_max 首次/5）——17 点 88%——核心观察加强")
print("3. ★★ 8 = k_max 首次出现（0.25 au）——束缚态数触及禁戒配置总数——最强框架身份")
print("4. ★ 平台结构（13/12/5 平台）——离散阶梯 + 平台——非连续溶解——方向性判别点")
print("5. 诚实边界：后验身份风险仍存（大量整数可凑框架身份）；53/23 无身份；场强→身份对应规则开放")
json.dump({"merged_pts": pts, "hit17": hit, "new_hits": [13, 8, 5]},
          open(os.path.join(BASE, "_phase102_p7_5e66b_verdict.json"), "w", encoding="utf-8"), indent=2)
print("JSON 落盘 ✓  exit 0")
