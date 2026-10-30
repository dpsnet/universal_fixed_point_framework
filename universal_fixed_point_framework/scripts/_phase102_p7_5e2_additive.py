# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-2：10 = 3+7 加法机制的框架先例与分解枚举
==========================================================
问题：m_N 缺口 = κ²Λ/10，分母 10 = N_gen + (k_max−1) = 3+7（加法）。
深挖：
  A. 框架内"加性结构"先例清单（主导量 + 修正量）——P7-5c、P7-4d 等
  B. 10 的全部框架量分解枚举（已登记量 3/7/8/15/16 的两项组合）
  C. 加法 vs 减法族对照（15 = 16−1、7 = 8−1 是减法族；3+7 是加法）
"""
import json

# 已登记框架量（P7-4c 对偶网络 + 统一 3 定理）
F = {
    "N_gen": 3, "k_max": 8, "k_max_minus_1": 7,
    "two_k_max": 16, "two_k_max_minus_1": 15,
    "N_active": 3,
}
names = list(F.keys())

def main():
    print("=" * 78)
    print("P7-5e-2：10 = 3+7 加法机制——先例与分解枚举")
    print("=" * 78)

    print("\n[A] 框架加性结构先例（主导量 + 修正量）：")
    precedents = [
        ("P7-5c m_τ 锚定", "E_τ = 16·dH + ln(16/15)/3", "旋量塔×谱维 + 桥/代数", "+0.043% ✓"),
        ("P7-4d m_μ 间隔", "ln16 + e^{−3}", "旋量对偶 + 对象静默", "+0.002% ✓"),
        ("P7-4e 统一静默", "k=3e、k=e^{−3}（指数内组合）", "静默乘积", "+0.011%/−0.001% ✓"),
        ("P7-5e m_N 缺口", "κ²Λ/10 = κ²Λ/(3+7)", "胶子二阶 ÷ (代数+对偶缺口)", "−0.038% ✓"),
    ]
    for name, form, struct, status in precedents:
        print("  %-14s %-28s %-22s %s" % (name, form, struct, status))
    print("  → 加性结构（主导+修正）在轻子锚定/间隔有先例；m_N 缺口分母为同类加性")

    print("\n[B] 10 的全部两项分解（x,y ∈ 框架量；a,b ∈ {±1,±2}）：")
    decomps = {}
    for a in (-2, -1, 1, 2):
        for b in (-2, -1, 1, 2):
            if a == 0 and b == 0:
                continue
            for i, n1 in enumerate(names):
                for n2 in names[i:]:
                    v = a*F[n1] + b*F[n2]
                    if abs(v - 10) < 1e-9:
                        key = "%d·%s %+d·%s" % (a, n1, b, n2)
                        decomps[key] = True
    for k in sorted(decomps):
        print("    10 = %s" % k)
    print("  → 框架量两项组合给出 10 的分解数：%d" % len(decomps))

    print("\n[C] 自然性排序与对照：")
    candidates = [
        ("N_gen + (k_max−1)", "3+7", "代数+对偶缺口（P7-4c 7 登记）", "加性"),
        ("k_max + N_gen − 1", "8+3−1", "底空间+代数−1", "加减混合"),
        ("two_k_max − 2·N_gen", "16−6", "2×k_max − 2×N_gen", "减法"),
        ("2·(k_max−N_gen)", "2·5", "2×(底−代数)，5=k_max−N_gen", "乘法外衣"),
    ]
    for name, expr, struct, typ in candidates:
        print("    %-22s %-8s %-26s %s" % (name, expr, struct, typ))

    print("\n[D] 减法族对照（Mersenne 型）：")
    print("    15 = 2k_max − 1 = 16−1（d_H = ln15 机器证明）——减法")
    print("    7  = k_max − 1 = 8−1（P7-4c 登记）——减法")
    print("    10 = 3 + 7（加法）——若为 N_gen + (2^{N_active}−1)，则是'代数+减法族成员'")
    print("    → 3+7 的机制候选：代数与 Mersenne 缺口之和 = 总自由度？")

    print("\n[E] 判定：")
    print("    1. 加性先例存在（P7-5c/P7-4d）——10=3+7 可归入'框架加性修正模式'")
    print("    2. 10 多重分解（3+7、8+3−1、2×5）——最优候选：3+7（两组件均有登记身份）")
    print("    3. '为何加法'仍无推导——机制开放，候选身份维持'可分解、机制开放'")

    result = {"precedents": len(precedents), "decomps": len(decomps),
              "best": "N_gen + (k_max-1) = 3+7", "mechanism": "open"}
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e2_additive.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nexit 0")

if __name__ == "__main__":
    main()
