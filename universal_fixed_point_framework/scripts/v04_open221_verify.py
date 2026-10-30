# -*- coding: utf-8 -*-
# 104az-221/222 事实基础验证（pyenv 3.11.8）
# ① d_H = ln15 路径（BranchCounting.lean 条件定理）→ 1/α 判别
# ② g_n/2 44/23 平方型身份 (7²-5)/(5²-2)
# ③ g_p/2 分母 14400 = (k_max×B)² 交叉锁定（B = N_active×N_total = 15）
import numpy as np
from fractions import Fraction

print("=== ① d_H = ln15 路径判别 ===")
ln15 = np.log(15.0)
print("ln15 =", repr(ln15), "(精确", repr(Fraction(15)), "的 log)")
alpha_inv_ln15 = 24.0 * (ln15 + 3.0)
alpha_inv_obs = 137.035999084
dev = (alpha_inv_ln15 - alpha_inv_obs) / alpha_inv_obs
sigma_obs_alpha = 2.1e-8  # 104az-201 登记：1/α 相对不确定度
print("24(ln15+3) =", repr(alpha_inv_ln15))
print("dev vs 137.035999084 =", f"{dev*100:.6f}%")
print("sigma_dev =", f"{dev/sigma_obs_alpha:.1f}")
print("BranchCounting d_H_fit = 2.7095 → 24(2.7095+3) =", 24.0*(2.7095+3.0))
print("路径A 16259/6000 → 24(dH+3) =", 24.0*(16259/6000+3))
print("路径B 65/24 → 24(dH+3) =", 24.0*(65/24+3))

print()
print("=== ② g_n/2 44/23 平方型身份 ===")
print("7^2-5 =", 49-5, "| 5^2-2 =", 25-2)
print("(7^2-5)/(5^2-2) =", Fraction(44,23), "= 44/23")
gn2_obs = 1.91304273
dev_gn2 = (44/23 - gn2_obs)/gn2_obs
sigma_obs_gn2 = 4.5e-7  # 104az-201 登记
print("dev vs |g_n/2| =", f"{dev_gn2*100:.5f}%", "| sigma_dev =", f"{dev_gn2/sigma_obs_gn2:.3f}")

print()
print("=== ③ g_p/2 分母 14400 交叉锁定 ===")
print("k_max×B = 8×15 =", 8*15, "| (8×15)^2 =", (8*15)**2)
print("14400 =", 14400, "| 2^6·3^2·5^2 =", 2**6*3**2*5**2)
print("40217 = 131×307 ?", 131*307)
print("131 = 8·16+3 ?", 8*16+3, "| 307 = 45·7−8 ?", 45*7-8, "| 45 = 5·9 ?", 5*9)
print("14400/40217 =", 14400/40217)

print()
print("=== 交叉核对：44/23 vs T4 主结构 (对合域,静默,幂基) ===")
print("(7,5,2) =", (7,5,2), "— T4 主结构同参数集")
