# -*- coding: utf-8 -*-
"""S240 CKM 混合角框架候选检验
候选：V_us = 0.2243 ± 0.0008（PDG）vs 9/40 = 0.225
  9 = 2^活跃+1 = 2^3+1（k_max+1——S210 kmax_plus_one_active_sq 已锚）
  40 = 静默 x k_max = 5x8——组件全框架
CKM 家族扫描：V_ud、V_cb、V_ub 有无框架候选
防巧合铁律：单点命中不升格——需家族/结构
"""
print("=== S240: CKM 混合角框架候选检验 ===\n")

def sigma_score(m, sig_abs, cand):
    s = abs(m - cand) / sig_abs
    return s

print("=== 1. V_us 候选：9/40 = 0.225 ===")
# PDG 2024：|V_us| = 0.2243 ± 0.0008
v_us = 0.2243
sig_us = 0.0008
cand = 9.0 / 40.0
s = sigma_score(v_us, sig_us, cand)
print(f"|V_us| = {v_us} ± {sig_us} vs 9/40 = {cand}——σ_score = {s:.2f}σ——"
      f"{'达标' if s <= 1 else ('提示' if s <= 3 else '证伪')}")
print("9 = 2^活跃+1 = k_max+1（S210 锚——kmax_plus_one_active_sq）")
print("40 = 静默 x k_max = 5 x 8——组件全框架")

print("\n=== 2. CKM 家族扫描 ===")
# V_ud = 0.97373 ± 0.00031
v_ud = 0.97373
sig_ud = 0.00031
# 候选：37/38 = 0.97368——37 无框架身份——先证伪
cand37 = 37.0 / 38.0
s1 = sigma_score(v_ud, sig_ud, cand37)
print(f"|V_ud| = {v_ud} ± {sig_ud} vs 37/38 = {cand37}——σ = {s1:.2f}σ——"
      f"但 37 无框架身份——候选不合格（先证伪）")

# V_cb = 0.0408 ± 0.0010
v_cb = 0.0408
sig_cb = 0.0010
# 候选：49/1200 = 0.04083——49 = 对合²、1200 = 12 x 100 = ?——1200 无框架身份
cand_cb = 49.0 / 1200.0
s2 = sigma_score(v_cb, sig_cb, cand_cb)
print(f"|V_cb| = {v_cb} ± {sig_cb} vs 49/1200 = {cand_cb}——σ = {s2:.2f}σ——"
      f"但 1200 无框架身份——候选不合格")

# V_ub = 0.0037 ± 0.0010——太小——跳过
print(f"|V_ub| = 0.0037——量级小——框架候选无意义——跳过")

print("\n=== 3. 诚实结论 ===")
print("V_us vs 9/40：σ_score = 0.88σ——达标——组件全框架")
print("CKM 家族其他元：V_ud/V_cb 候选组件不全框架——不合格")
print("→ V_us 单点命中——防巧合铁律（S227 教训）——")
print("  CKM 家族仅 1 命中——样本 1——不升格——登记观察候选")
print("  ——待 CKM 精确化/家族扩展检验")
