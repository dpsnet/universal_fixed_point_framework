# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-65：束缚态谱 = 框架量序列（溶解量子化假说检验）
================================================================
数据：paperX_eta_sc_B_bound.json（B_au → n_bound 全曲线）
检验1：溶解步进序列——9 = N_gen² 只出现在 11.8→23.5 一步（单点巧合——假说不稳健）
检验2：残余束缚态数 = 框架量序列（后验身份对照——85% 命中候选）
"""
import json, io, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
d = json.load(io.open(os.path.join(BASE, "_gaia_abs", "paperX_eta_sc_B_bound.json"), encoding="utf-8"))
Bs = [r["B_au"]*2350 for r in d]
Ns = [r["n_bound"] for r in d]

print("="*104)
print("P7-5e-65：束缚态谱 = 框架量序列（溶解量子化假说检验）")
print("="*104)

print()
print("【数据全曲线】")
print("-"*104)
for b, n in zip(Bs, Ns):
    print("  B=%6.1f MG  n_bound=%d" % (b, n))

print()
print("【检验1：溶解步进序列——9 步进不稳健】")
print("-"*104)
steps = [Ns[i]-Ns[i+1] for i in range(len(Ns)-1)]
print("溶解步进：%s" % steps)
print("→ 9 = N_gen² 只在 11.8→23.5 出现一次——其余步进 {4,10,7,3,2,2,3,1,0,1,4,2} 无 9 模式")
print("→ ★ 溶解量子化（9 步进）假说：单点巧合——不稳健——撤回（P7-5e-64 结论3 修正）")
print()
print("【★★ 检验2：残余束缚态数 = 框架量序列（后验身份对照）】")
print("-"*104)
ids = {
 53: "？无干净",
 49: "★ 静默单元 7² = (k_max−1)²",
 40: "★ 静默家族 X=40（41−1——P7-5e-39）",
 30: "★ N_gen×10 = 3×10",
 23: "？无干净",
 20: "★ (k_max−N_gen)(N_gen+1) = 5×4",
 18: "★ 2·N_gen² = 2×9",
 16: "★ 2^{N_gen+1} = 2⁴（幂家族）",
 13: "★ 静默单元 13（N_gen·k_max/2+1——P7-5e-43）",
 12: "★ N_gen·k_max/2 = 12",
 11: "★ k_max+N_gen = 11",
 7:  "★ k_max−1 = 7",
 5:  "★ k_max−N_gen = 5",
}
hit = 0
for n in Ns:
    mark = ids.get(n, "？")
    if "★" in mark:
        hit += 1
    print("  n_bound=%d → %s" % (n, mark))
print("→ ★★ %d 个数据点中 %d 个有框架身份（53、23 除外）——%d/%d = %.0f%% 命中候选" % (len(Ns), hit, hit, len(Ns), 100*hit/len(Ns)))
print("→ 诚实：后验拼凑风险——但可检验预言方向：新场强束缚态数应落入框架量序列")
print()
print("【可检验预言候选】")
print("-"*104)
print("序列 {49, 40, 30, 23, 20, 18, 16, 13, 12, 11, 7, 5} 中缺 15/14/10/9/8/6/4/3/2/1")
print("→ 预言：适当场强下束缚态数应出现 15（？）、14（？）、10（k_max+N_gen−1 = 10）等框架量")
print("→ 尤其 10 = 配置基数——某场强下束缚态数 = 10 可检验")
print()
print("【结论】")
print("-"*104)
print("1. ★ 溶解量子化 9 步进假说撤回（单点巧合——不稳健）——P7-5e-64 结论3 修正")
print("2. ★★ 残余束缚态数 = 框架量序列（85% 命中候选——静默/幂家族/组合身份）")
print("3. ★ 可检验预言：新场强束缚态数应落入框架量序列（如 10 = 配置基数）")
print("4. 诚实边界：身份为后验对照（非先验预测）；53/23 无身份；序列的场强-身份对应规则开放")
print()
json.dump({"steps": steps, "n_seq": Ns, "hit": hit, "total": len(Ns)},
          open(os.path.join(BASE, "_phase102_p7_5e65_bound_spectrum.json"), "w", encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
