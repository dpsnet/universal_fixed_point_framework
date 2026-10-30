# -*- coding: utf-8 -*-
"""
e 内生化桥 · 路径②独立预言检验 + Bott 塔层累加判别（2026-10-21 本地）
A 独立预言：若『框架代数阶内 exp 截断』普适，各超越常数的自然级数在框架量阶截断的精度对照
   预言：只有 exp 型（e / 1/e / e^{−3}）在 K=8 达 1e-6/1e-5 级；π/γ/ln2 无此形态
B Bott 塔判别：层节点子列 Σ 1/(8m)! vs e（预期不收敛）；全层和 Σ_{k≤8m} 1/k!（→e 平凡极限）
运行：D:\\pyenv\\pyenv-win\\versions\\3.11.8\\python.exe scripts\\e_internalization_independent_prediction.py
"""
from math import factorial, e, pi, log, gamma, exp

print("=" * 78)
print("A 独立预言：自然级数在框架量阶 {4,5,7,8,15,42} 截断的精度对照")
print("=" * 78)
print("常数 | 级数形态 | 截断误差（相对）")
print("-" * 78)

# e 型：Σ 1/k! → e（主候选）
def err_e(K):
    return sum(1.0 / factorial(k) for k in range(K + 1)) / e - 1

# 1/e 型（交替）：Σ (−1)^k/k! → 1/e
def err_inv_e(K):
    return sum((-1.0) ** k / factorial(k) for k in range(K + 1)) * e - 1

# e^{−3} 型（P7-4d 框架量！）：Σ (−1)^k 3^k/k! → e^{−3}
def err_e3(K):
    return sum((-3.0) ** k / factorial(k) for k in range(K + 1)) / exp(-3) - 1

# ln2 型：Σ_{k=1}^{K} 1/(k·2^k) → ln2（2 幂分母，幂基连接）
def err_ln2(K):
    return sum(1.0 / (k * 2 ** k) for k in range(1, K + 1)) / log(2) - 1

# π 型 1：Σ 1/k² → π²/6（ζ(2)，幂型）
def err_zeta2(K):
    return (sum(1.0 / k ** 2 for k in range(1, K + 1)) * 6) / (pi ** 2) - 1

# π 型 2：4Σ (−1)^k/(2k+1) → π（Leibniz，交替奇次）
def err_leibniz(K):
    return (4 * sum((-1.0) ** k / (2 * k + 1) for k in range(K + 1))) / pi - 1

# γ 型：γ 无自然级数截断（对数型定义）——登记为『形态缺失』
for K in [4, 5, 7, 8, 15, 42]:
    print(" e     | Σ 1/k!                | %+12.2e  K=%2d" % (err_e(K), K))
    print(" 1/e   | Σ (−1)^k/k!           | %+12.2e  K=%2d" % (err_inv_e(K), K))
    print(" e^{−3}| Σ (−1)^k 3^k/k!       | %+12.2e  K=%2d" % (err_e3(K), K))
    print(" ln2   | Σ 1/(k·2^k)           | %+12.2e  K=%2d" % (err_ln2(K), K))
    print(" π(ζ2) | Σ 1/k²·6              | %+12.2e  K=%2d" % (err_zeta2(K), K))
    print(" π(Lb) | 4Σ (−1)^k/(2k+1)      | %+12.2e  K=%2d" % (err_leibniz(K), K))
    print("-" * 78)
print(" γ     | 无幂/阶乘型级数形态（对数定义 γ = lim(H_n−ln n)）→ 截断表达先天缺失")

print()
print("=" * 78)
print("B Bott 塔判别：层数无限累加能否逼近 e")
print("=" * 78)
# B1：层节点子列——塔层 m 对应『第 8m 个对象』，每层一个项 Σ_{m} 1/(8m)!
s_node = 0.0
print("B1 层节点子列 Σ_{m≥0} 1/(8m)!（每 Bott 层贡献一个项）:")
for m in range(0, 8):
    t = 1.0 / factorial(8 * m)
    s_node += t
    print("   m=%d: +1/%d! = %.6e  → 累计 %.10f  (对 e 偏差 %+.4f)" % (m, 8 * m, t, s_node, s_node / e - 1))
print("   极限 Σ_{m≥0} 1/(8m)! = %.10f ≠ e = %.10f（残差 ≈ e−1 = %.6f）" % (s_node, e, e - s_node))
print("   → Bott 层节点不产生 e 收敛子列（层是周期结构，非对象数累加）")

# B2：全层和——塔层 m 对应『对象总数 = 8m』，Σ_{k≤8m} 1/k!
print("B2 全层和 Σ_{k=0}^{8m} 1/k!（对象总数 = 8m 的 exp 截断）:")
for m in [1, 2, 3, 4, 10]:
    K = 8 * m
    s = sum(1.0 / factorial(k) for k in range(K + 1))
    print("   m=%2d: K=%3d  Σ = %.10f  (err %+.3e)" % (m, K, s, s / e - 1))
print("   极限 = e（级数定义，平凡收敛）——但要求对象数 → ∞，与 k_max=8 公设（104az-264 代数必然）冲突")
print("   → 全层和逼近 e 在框架内非法：框架无第 9 对象，遑论无限对象")

# B3：Bott 周期 8 的代数维度增长 vs 阶乘项增长
print("B3 Bott 周期 8 维度增长 vs 阶乘项增长：")
print("   Cl_{8m+j} 维度 = 2^{8m+j}（2 幂型），塔层间维度翻 2^8 = 256 倍")
print("   Σ 1/k! 项增长 = 阶乘型（k! 超指数）——两族不同：2 幂型项 Σ 1/2^{8m} = 1/(1−1/256) ≈ 1.0039 ≠ e")
s_pow = sum(1.0 / 2 ** (8 * m) for m in range(0, 50))
print("   Σ_{m≥0} 1/2^{8m} = %.10f（≠ e，残差 %.4f）" % (s_pow, e - s_pow))
print("   → Bott 塔维度（2 幂）不产生 1/k! 项——两者机制不同族")

print()
print("判别结论：")
print("A：K=8 达 1e-6 级的只有 e（a=1 正和 1.1e-6）与 1/e（a=1 交替 6.8e-6）——λ=1 单位事件率唯一性被数据支持；")
print("   e^{−3}（a=3）K=8 仅 83%（交替级数需 k>|a| 才进收敛区，K≥15 才达 1e-5）——a≠1 全败；")
print("   ln2（2 幂分母）K=8 最佳 5.7e-4、π 全部 ≥1e-2、γ 形态缺失。")
print("   → 独立预言：『代数阶 8 内 exp 截断达 1e-6』为 e/1/e（a=1）独有——不是普适现象，λ=1=单位元候选获支持。")
print("B：Bott 塔层无限累加不产生框架内合法的 e 锁定——层节点子列 ≠ e（残差 e−1）、全层和需对象数无限（违公设）、")
print("   2 幂维度与阶乘项不同族。e 的 1e-6 呈现（Σ_{k≤8} 1/k!）是单塔单层截断的框架必然，环 3（有理 vs 超越）不受塔层影响。")
