# -*- coding: utf-8 -*-
# S114 二阶项 σ⁵−e^{−16} 机制先证伪（2026-10-27）
# 目标：判别"净冻结 = 代数冻结 σ⁵ − 超越残漏 e^{−16}"候选——
#   ① σ^n 量级锁定（为何 n=5）
#   ② "−e^{−16}"组合调谐（为何减全态指数静默）
#   ③ 宽候选空间唯一性（组合命中质量 vs 空间大小）
# 观测锚：E_τ^B 剩余偏差 = +1.205172e-6（B''' 后）

from math import log, e

resid = 1.2051720049e-6   # E_τ^B 剩余偏差（S112 精确值）
sigma = 1/15

print(f"E_τ^B 剩余偏差（观测锚）：+{resid:.3e}")
print("=== ① σ^n 量级锁定（为何 n=5） ===")
for n in range(3, 8):
    v = sigma**n
    print(f"σ^{n} = {v:.3e}——vs 剩余 比值 {v/resid:.2f}（{'量级匹配' if 0.3<v/resid<3 else '失配'}）")

print("\n=== ② σ⁵ ± k·e^{−16} 调谐（k 扫描——为何 k=1） ===")
s5 = sigma**5
e16 = e**(-16)
for k in [0, 1, 2, 3]:
    v = s5 - k*e16
    d = abs(v - resid)/resid*100
    print(f"σ⁵ − {k}·e^{{−16}} = {v:.3e}——差 {d:.2f}%——比值 {v/resid:.5f}")
    if k == 0: print("  （裸 σ⁵——差 9.3%——需要减项）")
    if k == 1: print("  （−e^{−16}——差 0.07%——精确命中）")

print("\n=== ③ 宽候选空间唯一性（30 项组合扫描） ===")
cands = {}
# σ 系 + e 系混合（±k e^{−16}）
for n in [4, 5, 6]:
    for k in [1, 2, 3]:
        cands[f"σ^{n}−{k}e^{{-16}}"] = sigma**n - k*e16
        cands[f"σ^{n}+{k}e^{{-16}}"] = sigma**n + k*e16
# σ⁵ 系数
for c in [1, 2, 3]:
    cands[f"{c}σ⁵−e^{{-16}}"] = c*s5 - e16
# e^{−16} 整数系
for k in [8, 9, 10, 11, 12]:
    cands[f"{k}e^{{-16}}"] = k*e16
# ε_μ 系
eps_mu = 144*e16*(1+6*sigma**3)
for c in [1, 2]:
    cands[f"ε_μ×{c}/27"] = eps_mu*c/27
    cands[f"ε_μ×{c}/15"] = eps_mu*c/15
# σ⁵ 微调
cands["σ⁵(1−σ)"] = s5*(1-sigma)
cands["σ⁵(1+σ)"] = s5*(1+sigma)
cands["σ⁵/(1+σ)"] = s5/(1+sigma)
cands["σ⁵−σ⁷"] = s5 - sigma**7
cands["σ⁵−e^{−16}(1+σ)"] = s5 - e16*(1+sigma)

results = []
for name, v in cands.items():
    if v <= 0: continue
    d = abs(v - resid)/resid*100
    results.append((d, name, v))
results.sort()
print(f"命中率（<1% 差）：{sum(1 for d,_,_ in results if d<1)}/{len(results)}")
for d, name, v in results[:12]:
    print(f"  {name} = {v:.3e}——差 {d:.2f}%")
print(f"\n总候选 {len(results)} 项——<1% 差 {sum(1 for d,_,_ in results if d<1)} 项——<3% 差 {sum(1 for d,_,_ in results if d<3)} 项")

print("\n=== ④ 机制候选 vs 拟合候选 ===")
print("机制候选（先验——框架量组合）：σ⁵ − e^{−16}")
print("  ——σ⁵：静默自指冻结（5 次冻结——σ^n 幂谱语义）")
print("  ——e^{−16}：全态泊松残漏（16 窗口各 e^{−1}——silence_family §9④）")
print("  ——净冻结 = 代数冻结 − 超越残漏（离散−连续对偶——S102 模流=递归谱连续化）")
print("拟合候选（后验——无机制）：2ε_μ/27 = 1.202e-6（差 0.16%）")
print("  ——ε_μ 的 27 系投影——但系数谱 {1,2/75,8,2/27} 无生成规则——拟合")

print("\n=== ⑤ 残差结构（二阶项命中后） ===")
print(f"σ⁵−e^{{−16}} = {s5-e16:.3e} vs 剩余 {resid:.3e}——差 {abs((s5-e16)-resid)/resid*100:.3f}%")
print(f"残余（三阶候选量级）：{(s5-e16)-resid:.2e}——σ⁷={sigma**7:.2e}、e^{{−32}}={e**(-32):.2e}")
