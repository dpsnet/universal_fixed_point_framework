# -*- coding: utf-8 -*-
"""S420 扫描精细度-中心值漂移规律检验（2026-10-29）
用户直觉：实验精度提高（u 减小）→ α⁻¹ 中心值漂移——
是否'有规律'（不确定度-中心值关联）？规律指向哪里
（外推 u→0 是否收敛到 MUFPF 基底 137.035999083426）？
纯通道三点（Cs/a_e/Rb）+ 总平均四点两种拟合
"""
import numpy as np

alpha_base = 137.035999083426

# 数据：名称, α⁻¹, 不确定度 u（相对）
data_chan = [
    ("Cs (Parker 2018)", 137.035999046, 2.7e-8),
    ("a_e (Fan 2023)",   137.035999166, 1.6e-8),
    ("Rb (Morel 2020)",  137.035999206, 1.1e-8),
]
data_all = [
    ("Cs (Parker 2018)", 137.035999046, 2.7e-8),
    ("2018 总平均",      137.035999084, 2.1e-8),
    ("a_e (Fan 2023)",   137.035999166, 1.6e-8),
    ("Rb (Morel 2020)",  137.035999206, 1.1e-8),
]

print("=== S420 扫描精细度-中心值漂移规律 ===")
print(f"MUFPF 基底 = {alpha_base}")
print()

for tag, rows in [("纯通道三点", data_chan), ("含总平均四点", data_all)]:
    print(f"◆ {tag}：")
    for n, v, u in rows:
        d = v - alpha_base
        print(f"  {n}：{v}（u={u:.1e}，相对基底 {d:+.2e}）")
    x = np.array([r[2] for r in rows])
    y = np.array([r[1] for r in rows])
    # 最小二乘线性拟合
    b, a = np.polyfit(x, y, 1)
    y_pred = a + b * x
    res = y - y_pred
    # 不确定度加权残差
    u_arr = np.array([r[2] for r in rows])
    chi2 = np.sum((res / u_arr) ** 2)
    ndof = len(rows) - 2
    # 截距 = u→0 外推
    intercept = a
    sigma_int = np.sqrt(chi2 / ndof) * np.sqrt(
        np.sum(x**2) / (len(rows) * np.sum((x - x.mean())**2)))
    # 简化：截距不确定度 = sqrt(Σ(y-ŷ)²/(n-2)) × sqrt(Σx²/(n·Σ(x-x̄)²))
    # 用严格公式
    Sxx = np.sum((x - x.mean())**2)
    xbar = x.mean()
    s2 = np.sum(res**2) / ndof
    sigma_a = np.sqrt(s2 * np.sum(x**2) / (len(rows) * Sxx))
    print(f"  拟合：α⁻¹ = {a:.12f} + ({b:.1f})·u")
    print(f"  斜率 b = {b:.1f}（u 减小 → 值 {'增加' if b < 0 else '减少'}）")
    print(f"  外推 u→0 截距 = {intercept:.12f} ± {sigma_a:.2e}")
    print(f"  截距 vs MUFPF 基底：差 {intercept - alpha_base:+.2e}"
          f"——σ_score = {abs(intercept - alpha_base)/sigma_a:.2f}")
    print(f"  χ²/ndof = {chi2:.2f}/{ndof}")
    # 单调性检查
    order = np.argsort(x)
    mono = all(y[order[i]] <= y[order[i+1]] for i in range(len(rows)-1))
    print(f"  单调性（u 升序 → 值升序）：{'成立' if mono else '不成立'}")
    print()

print("[解读]：")
print("  · 若截距 ≈ 基底：高精度极限收敛到 MUFPF 预言——")
print("    '扫描精细度→投影结构'直觉获数值支撑")
print("  · 若截距 ≠ 基底：漂移规律存在但指向别处——")
print("    需解释规律指向（真值不在基底？）")
print()
print("[诚实]：仅 3-4 个数据点——线性模型是工作假设——")
print("  统计功效低——结论为'提示'级非定案——")
print("  待更多通道/CODATA 2026 检验")
