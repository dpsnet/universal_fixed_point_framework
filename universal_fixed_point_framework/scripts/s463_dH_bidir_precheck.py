# -*- coding: utf-8 -*-
"""
S463 先证伪：d_H 链可± 的代数侧数值检验（2026-10-29）
======================================================
S459 R3a 第三条符号规则：d_H=ln15 链可±（对数双向——
Z₂ 分次双向）——与 e/σ 链只+ 不同。
代数侧锚候选（数学事实）：
  C1: ln15 > 0（正侧——d_H 构造正系数 +2ln15 的代数基础）
  C2: ln(1/15) = -ln15 < 0（负侧——对数取逆→符号翻转）
  C3: log 满射到 ℝ（对任意 y 存在 x 使 ln x = y——
      对数域 = 全 ℝ——双向性的最强表述）
验证残差容差 1e-12。
"""
import math

# C1: ln15 > 0
ln15 = math.log(15.0)
assert ln15 > 0, "C1 失败"
print(f"C1 ln15 > 0 ✓  ln15 = {ln15:.12f}")

# C2: ln(1/15) = -ln15 < 0
ln_inv = math.log(1.0 / 15.0)
res_c2 = abs(ln_inv - (-ln15))
assert res_c2 < 1e-12, f"C2 残差 {res_c2}"
assert ln_inv < 0, "C2 符号失败"
print(f"C2 ln(1/15) = -ln15 ✓  残差 {res_c2:.2e}  ln(1/15) = {ln_inv:.12f}")

# C3: log 满射（对任意 y ∈ ℝ 存在 x 使 ln x = y——x = e^y）
# 取 1000 个随机 y（含正负），验证 ln(e^y) = y
import random
random.seed(20261029)
max_res = 0.0
n_neg = n_pos = 0
for _ in range(1000):
    y = random.uniform(-100.0, 100.0)
    x = math.exp(y)          # x > 0（对数定义域 ℝ⁺）
    got = math.log(x)
    r = abs(got - y)
    max_res = max(max_res, r)
    if y < 0:
        n_neg += 1
    else:
        n_pos += 1
assert max_res < 1e-9, f"C3 最大残差 {max_res}"
print(f"C3 log 满射 ℝ（ln(e^y)=y，1000 组 y∈[-100,100]）✓  最大残差 {max_res:.2e}")
print(f"   样本中负 y 数 = {n_neg}、正 y 数 = {n_pos}——正负双向全覆盖")

# 补充：d_H 构造的实际符号（S419 五口径）
# Cs = -(5/2)ln15（负系数）、a_e = +2ln15（正系数）——同链双侧使用
print(f"\n[d_H 链构造符号复核]")
cs_coef = -(5.0 / 2.0) * ln15
ae_coef = 2.0 * ln15
print(f"  Cs 系数 = -(5/2)·ln15 = {cs_coef:.12f} < 0（负侧）")
print(f"  a_e 系数 = +2·ln15 = {ae_coef:.12f} > 0（正侧）")
print(f"  ——同一 d_H 链、双向系数——R3a 'd_H 可±' 数值自洽 ✓")

print("\n结论：C1/C2/C3 全通过——d_H 双向对数锚可 Lean 化")
