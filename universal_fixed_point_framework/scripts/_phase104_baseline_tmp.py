# -*- coding: utf-8 -*-
"""Phase 104az-56：基线模型无效的正面解决——中场判别域验证
判别：归因裁决的判别域是否落在标准强场物理未开动区（B < B_ion 全线）"""
import json, statistics

# B_th(n) = 2352.7/n² MG（论文闭式）
B_TH = {3: 2352.7/9, 4: 2352.7/16, 5: 2352.7/25, 6: 2352.7/36, 7: 2352.7/49}
print("B_ion 阈值（MG）：Hα %.1f / Hβ %.1f / Hγ %.1f / Hδ %.1f / Hε %.1f" % (
    B_TH[3], B_TH[4], B_TH[5], B_TH[6], B_TH[7]))

base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
for fname, key, label in [
    ("paperX_wd_linelevel_mid_full_snr.json", "mid_full", "DESI mid_full"),
    ("paperX_lamost_linelevel_raw.json", "mid", "LAMOST mid"),
]:
    with open(base + "\\" + fname, encoding="utf-8") as f:
        data = json.load(f)
    recs = data if isinstance(data, list) else data.get(key, [])
    Bs = [r["B_MG"] for r in recs if r.get("B_MG") is not None]
    print("\n=== %s（n=%d）===" % (label, len(Bs)))
    if not Bs:
        continue
    Bs_sorted = sorted(Bs)
    print("  B 分布：min %.1f / p25 %.1f / 中位 %.1f / p75 %.1f / max %.1f" % (
        Bs_sorted[0], Bs_sorted[len(Bs_sorted)//4], Bs_sorted[len(Bs_sorted)//2],
        Bs_sorted[3*len(Bs_sorted)//4], Bs_sorted[-1]))
    # 每线：样本中 B < B_ion 的比例（标准 Landau 电离未开动区）
    for n in (3,4,5,6,7):
        frac_below = sum(1 for b in Bs if b < B_TH[n]) / len(Bs)
        frac_above = sum(1 for b in Bs if b >= B_TH[n]) / len(Bs)
        print("  B_ion(H%s)=%.1f MG：未开动区(B<B_ion) %.1f%% / 已开动区(B>=B_ion) %.1f%%" % (
            {3:"α",4:"β",5:"γ",6:"δ",7:"ε"}[n], B_TH[n], 100*frac_below, 100*frac_above))
