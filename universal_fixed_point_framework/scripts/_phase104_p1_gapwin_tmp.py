# -*- coding: utf-8 -*-
"""
Phase 104az-30 (26.16j-78): 缺口窗口绝对宽身份候选 -- 高阶 Balmer 线带 (Hγ-Hε)
候选: 缺口窗口 = 高阶 Balmer 线带 (Hγ 4340 / Hδ 4102 / Hε 3970, 带宽 370 A)
      ~ Balmer 带 (3646 系限 -> Hα 6563) 的 1/8 = 364.6 A  (1.01x 命中)
关联: 缺口=1 基态 (带宽/8) -- 高阶线优先关闭 (§4.9: Hβ -45% -> Hδ -98%) -- 蓝端增强 (26.16j-77)
"""
import json, os

# ---- Balmer 带 8 等分 ----
balmer_low = 3646.0    # Balmer 系限 (跳变)
balmer_high = 6562.8   # Hα
band = balmer_high - balmer_low
seg = band / 8.0       # 每段宽

# 段边界
edges = [balmer_low + k*seg for k in range(9)]

# ---- 高阶 Balmer 线带 ----
lines = {'Hβ': 4861.3, 'Hγ': 4340.5, 'Hδ': 4101.7, 'Hε': 3970.1}
hi_band_lo, hi_band_hi = lines['Hε'], lines['Hγ']   # 3970.1 - 4340.5
hi_band_w = hi_band_hi - hi_band_lo

# ---- 对比 ----
res = {
    'balmer_band_A': round(band, 1),
    'segment_width_1of8_A': round(seg, 1),
    'hi_order_line_band_A': round(hi_band_w, 1),
    'ratio_hiline_seg': round(hi_band_w / seg, 4),
    'segment_edges': [round(e, 1) for e in edges],
}

# 高阶线带落在哪段?
seg_idx = None
for k in range(8):
    if edges[k] <= hi_band_lo and hi_band_hi <= edges[k+1]:
        seg_idx = k
    elif edges[k] <= hi_band_lo <= edges[k+1] or edges[k] <= hi_band_hi <= edges[k+1]:
        seg_idx = k  # 跨段
res['hi_line_band_in_segment'] = seg_idx

# 段中心 vs 线带中心
seg_center = (edges[seg_idx] + edges[seg_idx+1])/2 if seg_idx is not None else None
hi_center = (hi_band_lo + hi_band_hi)/2
res['segment_center'] = round(seg_center, 1) if seg_center else None
res['hi_band_center'] = round(hi_center, 1)
res['center_ratio'] = round(hi_center/seg_center, 4) if seg_center else None

# 观测窗口对照 (J135141 4000-6500)
obs_win = (4000.0, 6500.0)
res['obs_win_1of8'] = round((obs_win[1]-obs_win[0])/8, 1)

# 判定
res['verdict'] = (
    f'高阶线带 {hi_band_w:.0f} A vs Balmer 带 1/8 {seg:.1f} A: 比值 {hi_band_w/seg:.3f} '
    f'({"命中(1%内)" if abs(hi_band_w/seg-1)<0.05 else "不命中"}) -- 落在第 {seg_idx} 段'
    if seg_idx is not None else '不命中')

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_p1_gapwin_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print(f'Balmer 带: {band:.1f} A, 1/8 段宽: {seg:.1f} A')
print(f'高阶线带 (Hε {lines["Hε"]} -> Hγ {lines["Hγ"]}): {hi_band_w:.1f} A')
print(f'比值 (高阶线带/段宽): {hi_band_w/seg:.3f}')
print(f'段边界: {[round(e,1) for e in edges]}')
print(f'高阶线带落在段 {seg_idx}: 中心 {res["segment_center"]} vs 线带中心 {hi_center:.1f}')
print(f'观测窗口 4000-6500 的 1/8: {res["obs_win_1of8"]} A (对照)')
print(f'判定: {res["verdict"]}')
print(f'已存盘: {out}')
