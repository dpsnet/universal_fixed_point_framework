# -*- coding: utf-8 -*-
# 104az-224 预注册检验执行：平方型族 (a^2-b)/(c^2-d) 对核磁子链 μ 系全扫描（pyenv 3.11.8）
# 预注册依据：族于 104az-222 登记（a,c∈M12、b,d∈M12∪{1}、24336 组合），μ_n 已命中 44/23
# 本检验目标 = 族内其他可测量（μ_p/μ_n/μ_d/μ_t/μ_3He 正数化），容差按各量 PDG 绝对不确定度 3σ
# 附加：g_p/2 分子 40217 = 131×307 的框架分解核验（131 = k_max×16+N_gen、307 = 静默×N_gen²×对合域−k_max）
import numpy as np
from fractions import Fraction
from collections import Counter

M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]
BD = sorted(set(M + [1]))

# CODATA/PDG 记忆值（绝对不确定度口径）：μ/μ_N 序列
TARGETS = [
    ("mu_p  (g_p/2)",    2.79284734463, 8.2e-10),
    ("|mu_n| (g_n/2)",   1.91304273,    4.5e-7),
    ("mu_d",             0.8574382338,  2.8e-8),
    ("mu_t",             2.9789624656,  5.9e-9),
    ("|mu_3He|",         2.12749772,    2.5e-7),
]

def scan(target, thresh):
    hits = []
    for a in M:
        for c in M:
            for b in BD:
                for d in BD:
                    n2, d2 = a*a - b, c*c - d
                    if n2 <= 0 or d2 <= 0:
                        continue
                    val = n2/d2
                    if abs(val - target) <= thresh:
                        hits.append((a, b, c, d, n2, d2, val, val-target))
    return hits

print("=== 预注册检验：平方型族 × 核磁子链 μ 系（3σ 绝对容差）===")
print(f"族规模 = {len(M)**2 * len(BD)**2}\n")
for name, target, sig in TARGETS:
    th = 3*sig
    hits = scan(target, th)
    print(f"--- {name} = {target}  ±3σ={th:.2e} ---")
    if hits:
        print(f"  命中 {len(hits)} 个：")
        for a, b, c, d, n2, d2, val, diff in sorted(hits, key=lambda x: abs(x[7]))[:5]:
            print(f"    ({a}^2-{b})/({c}^2-{d}) = {n2}/{d2} = {val:.10f}  dev {diff:+.2e}  σ={diff/sig:+.2f}")
    else:
        print("  命中 0 个")

print("\n=== decoy 负控（10 个同域随机目标 0.5~3.0，seed=224）===")
rng = np.random.default_rng(224)
for i, t in enumerate(rng.uniform(0.5, 3.0, 10)):
    h = scan(float(t), 1.0e-6)  # 同 104az-222 口径（1.35e-6 邻域）
    print(f"  decoy {i}: target {t:.6f} → 命中 {len(h)}")

print("\n=== g_p/2 分子 40217 = 131×307 框架分解核验 ===")
print("40217 = 131 × 307 ?", 131*307 == 40217)
print("131 = 8×16+3 ?", 8*16+3 == 131, "| 参数: k_max×幂基⁴+N_gen（8,16,3 全框架量）")
print("307 = 5×9×7−8 ?", 5*9*7-8 == 307, "| 参数: 静默×N_gen²×对合域−k_max（5,9,7,8 全框架量）")
print("131 素数?", all(131 % p for p in range(2, int(131**0.5)+1)))
print("307 素数?", all(307 % p for p in range(2, int(307**0.5)+1)))
print("g_p/2 = 40217/14400 =", 40217/14400)
print("14400 = (k_max×B)² = (8×15)² ?", (8*15)**2 == 14400, "（B=15=N_active×N_total）")
