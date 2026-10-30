# -*- coding: utf-8 -*-
"""静默投影权重形态数值探索（先证伪，2026-10-24）

目标：
1. 验证 von Neumann 等权极大性：任意权重 p 下 S = -Σp log p <= ln 15（等权取最大）
2. 量化静默投影"不均匀"的量度：不均匀权重下的熵 vs 等权熵 ln 15 的落差
3. 谱隙谱定值 Δλ_min = (√3-1)/6 ≈ 0.122 与等权权重 1/15 ≈ 0.0667 的对比
   ——若权重形态与谱相关，等权假设无支撑（谱隙 >> 1/15 反映强不均匀）

运行：D:\\pyenv\\pyenv-win\\versions\\3.11.8\\python.exe silence_weight_entropy_probe.py
"""
import numpy as np
import math

N = 15
lnN = math.log(N)

print("=" * 60)
print("1. 等权熵（上界）：S_A = ln 15")
S_eq = lnN
print(f"   ln 15 = {S_eq:.10f}")

print("=" * 60)
print("2. 等权极大性数值验证：随机权重熵 <= ln 15")
rng = np.random.default_rng(42)

# 2a) Dirichlet(1)：均匀单纯形上的随机权重（一般权重）
n = 200000
p = rng.dirichlet(np.ones(N), size=n)
S = -(p * np.log(p)).sum(axis=1)
print(f"   Dirichlet(1) 200k 样本：max={S.max():.10f}  mean={S.mean():.6f}  min={S.min():.6f}")
print(f"   等权上界 ln 15 = {S_eq:.10f}  |  超过上界比例 = {(S > S_eq + 1e-9).sum()}/{n}")

# 2b) Dirichlet(0.3)：集中型权重（静默投影不均匀的候选形态）
p2 = rng.dirichlet(np.full(N, 0.3), size=n)
S2 = -(p2 * np.log(p2)).sum(axis=1)
print(f"   Dirichlet(0.3) 200k 样本：max={S2.max():.10f}  mean={S2.mean():.6f}  min={S2.min():.6f}")
print(f"   超过上界比例 = {(S2 > S_eq + 1e-9).sum()}/{n}")

# 2c) 极端集中：Dirichlet(0.05)（接近单态主导；p log p 在 p=0 处取约定 0）
with np.errstate(divide="ignore", invalid="ignore"):
    p3 = rng.dirichlet(np.full(N, 0.05), size=n)
    S3 = -np.where(p3 > 0, p3 * np.log(p3), 0.0).sum(axis=1)
print(f"   Dirichlet(0.05) 200k 样本：max={S3.max():.10f}  mean={S3.mean():.6f}  min={S3.min():.6f}")
print(f"   超过上界比例 = {(S3 > S_eq + 1e-9).sum()}/{n}")

print("=" * 60)
print("3. 不均匀性量度：谱隙谱定值 vs 等权权重")
dl = (math.sqrt(3) - 1) / 6
print(f"   1/15 (等权权重)   = {1/15:.10f}")
print(f"   Δλ_min (谱隙谱定) = {dl:.10f}")
print(f"   比值 Δλ_min/(1/15) = {dl / (1/15):.4f}  —— 谱隙约为等权权重的 {dl * 15:.3f} 倍")
print(f"   含义：谱隙量级 >> 等权权重 ⟹ 若权重与谱相关，等权假设 (p=1/15) 无支撑")

print("=" * 60)
print("4. 结论登记")
viol = (S > S_eq + 1e-9).sum()
print(f"   等权极大性 S <= ln 15 数值验证：{viol == 0}（无违反）")
print(f"   均匀权重的熵均值 {S.mean():.6f} vs 集中权重 {S2.mean():.6f}/{S3.mean():.6f}")
print(f"   等权熵 ln 15 = {S_eq:.6f} 为全局上界；不均匀权重熵显著低于上界")
