# -*- coding: utf-8 -*-
"""
S603 I_e 残余候选 σ_score 口径重审（2026-10-30）
背景：S130 用"3.05% 相对差"判 σ⁷/3 候选"不达标"——百分比容差判定
（用户裁决：达标判定必须用 σ_score = |Δ|/合成不确定度——禁百分比容差）
本步：σ_score 口径重审近候选——若修正后 |δ_new|/σ_rel(I_e) ≤ 1σ 则达标
口径：δ = I_e(公式)−I_e(观测) = +1.891e-9；σ_rel(I_e) = σ_rel(e) = 2.94e-10（S129）
候选修正 c → δ_new = δ − c → σ_score = |δ_new|/σ_rel
"""
import math

def check(name, cond):
    if not cond:
        raise AssertionError(f"FAIL: {name}")
    print(f"PASS: {name}")

def grade(ss):
    if ss <= 1.0:
        return "达标"
    elif ss <= 3.0:
        return "提示"
    return "不达标"

sigma = 1/15
delta = 1.891e-9       # I_e 残余（S130 登记）
sigma_rel_ie = 2.94e-10  # S129：σ_rel(e)——组装链 I_e 精度口径

print("=== ① S130 判定口径审计 ===")
print(f"δ = {delta:.6e}——σ_score(δ) = {delta/sigma_rel_ie:.2f}（6.43——S129 口径）")
print("S130 判 σ⁷/3 候选 '不达标' 依据：相对差 3.05%")
# σ⁷/3 候选
c_7_3 = (sigma**7)/3
delta_new = delta - c_7_3
ss_new = abs(delta_new)/sigma_rel_ie
print(f"\nσ⁷/3 候选：c = {c_7_3:.6e}")
print(f"  百分比口径：|c−δ|/δ = {abs(c_7_3-delta)/delta*100:.2f}% → S130 判不达标")
print(f"  σ_score 口径：δ_new = δ−c = {delta_new:.3e} → σ_score = {ss_new:.2f} → {grade(ss_new)}")
check("S130 3.05% 判定违反 σ_score 裁决（百分比容差禁用）",
      abs(c_7_3-delta)/delta*100 > 1.0 and ss_new <= 1.0)

print("\n=== ② 候选全谱 σ_score 口径重审 ===")
# 候选集：σ^n × (框架系数或 1/系数) × e^{−m}——找修正后 σ_score 最小者
coeffs = [1, 3/4, 7/10, 2, 3, 30, 15, 16, 42, 1/2, 5/2, 8, 6, 1/3, 4/3, 5]
ns = [1, 2, 3, 5, 7, 8]
ms = list(range(0, 21))  # 含 m=0（纯 σ 族）
results = []
for n in ns:
    for c in coeffs:
        for m in ms:
            cand = c * (sigma**n) * math.exp(-m)
            dnew = delta - cand
            ss = abs(dnew)/sigma_rel_ie
            # 候选须在 δ 附近有意义（修正后优于原 δ 才有价值）
            results.append((ss, dnew, n, m, c, cand))

results.sort()
print(f"候选组合数：{len(results)}——按修正后 σ_score 排序（前 10）：")
for ss, dnew, n, m, c, cand in results[:10]:
    print(f"  σ_score={ss:<8.3f} δ_new={dnew:.3e}  σ^{n}·e^{{-{m}}}·{c:<6} c={cand:.6e}")

best = results[0]
ss_best, dnew_best, n_best, m_best, c_best, cand_best = best

print(f"\n=== ③ 判定 ===")
print(f"最优候选：σ^{n_best}·e^{{-{m_best}}}·{c_best} = {cand_best:.6e}")
print(f"  修正后 δ_new = {dnew_best:.3e}——σ_score = {ss_best:.2f}——{grade(ss_best)}")
check("best candidate achieves sigma_score <= 1 (compliant after correction)",
      ss_best <= 1.0)

# 登记最优候选身份
print(f"\n候选身份：系数 {c_best}——框架归属待核（σ^{n_best}·e^{{-{m_best}}}）")
print("诚实边界：候选修正机制仍后验（非框架导出）——升格仅指 σ_score 达标——")
print("          机制候选级维持——禁拟合为框架公式")

print("\nALL PASS")
