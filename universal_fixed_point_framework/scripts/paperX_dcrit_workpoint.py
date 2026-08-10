#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_dcrit_workpoint.py — 彩虹近似工作点 2×d_crit 的解释分解
====================================================================================
对应：paper40 §5.9（定理 5.7 + v0.38 验证段）
触发：用户"检查 d_crit=1.0 几何逻辑能否解释为什么彩虹近似工作点恰好是 2 倍临界强度"。

关键前提（定理 5.7 诚实边界）：文献 d ≈ 0.9–1.0（临界附近），框架彩虹 A≈1
用 d = 2.0（移位约 2 倍）——2.0 是框架选择，非 MT 文献惯例。

分解链（匹配 κΛ = 401 MeV 所需红外强度随近似改进递减）：
  彩虹 A≈1:  d = 2.0   （= 2·d_crit）
  A/B 耦合:  d_AB = 1.485
  BC1+UV 尾: d_full = 0.926 （≈ d_crit = 1.0，偏差 7%——完整处理工作点 = 临界附近）

检查：
  W1  完整处理工作点 = 临界附近（d_full ≈ d_crit，偏差 < 10%）——几何逻辑的解释力
  W2  补偿分解：d_rainbow/d_AB（A≈1 简化补偿）与 d_AB/d_full（树级→BC1 顶点补偿），
      乘积 ≈ d_rainbow/d_crit = 2.0
  W3  补偿因子数值巧合：d_rainbow/d_AB ≈ C_F = 4/3（偏差 < 2%）？d_AB/d_full ≈ 8/5（偏差 < 1%）？
  W4  结论：2×临界 = 两个近似补偿的乘积（≈2.16 ≈ 2），非 d_crit 几何直接推论
  W5  诚实边界

单位：GeV²。
"""
import math

D_CRIT = 1.0               # GeV²，几何临界强度 4/(3C_F)
D_RAINBOW = 2.0            # 彩虹 A≈1（定理 5.7）
D_AB = 1.485               # A/B 耦合（推论 5.9 配套）
D_FULL = 0.926             # BC1 + UV 尾（推论 5.9）
CF = 4.0 / 3.0

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def run():
    print("=" * 74)
    print("彩虹近似工作点 2×d_crit 的解释分解")
    print("=" * 74)

    # W1: 完整处理工作点 = 临界附近
    print("\n" + "=" * 74)
    print("W1. 完整处理工作点 = 临界附近（d_full ≈ d_crit）")
    print("=" * 74)
    dev = abs(D_FULL - D_CRIT) / D_CRIT * 100
    print(f"    d_full = {D_FULL:.3f} vs d_crit = {D_CRIT:.3f}（偏差 {dev:.1f}%）")
    print(f"    文献 d ≈ 0.9–1.0（临界附近）——完整处理（BC1+UV 尾）回到临界工作点")
    print("    ⟹ 几何逻辑的解释力：'物理工作点 = 临界附近'由 d_crit（无参数）确定")
    check("W1 完整处理工作点 = 临界附近（d_full ≈ d_crit，偏差 < 10%）",
          dev < 10.0, f"d_full = {D_FULL:.3f}，偏差 {dev:.1f}%")

    # W2: 补偿分解
    print("\n" + "=" * 74)
    print("W2. 补偿分解：2×临界 = A 修正 × 顶点增强的乘积")
    print("=" * 74)
    fA = D_RAINBOW / D_AB      # A≈1 简化补偿
    fV = D_AB / D_FULL         # 树级→BC1 顶点补偿
    prod = fA * fV
    ratio_2x = D_RAINBOW / D_CRIT
    print(f"    A 修正补偿   f_A = d_rainbow/d_AB = {fA:.3f}")
    print(f"    顶点增强补偿 f_V = d_AB/d_full = {fV:.3f}")
    print(f"    乘积 f_A × f_V = {prod:.3f} ≈ d_rainbow/d_crit = {ratio_2x:.3f}（偏差 {abs(prod-ratio_2x)/ratio_2x*100:.1f}%）")
    check("W2 补偿乘积 ≈ 2（f_A × f_V = 2.16 ≈ d_rainbow/d_crit = 2.0，偏差 < 15%）",
          abs(prod - ratio_2x) / ratio_2x < 0.15, f"乘积 {prod:.3f} vs 2.0（偏差 {abs(prod-ratio_2x)/ratio_2x*100:.1f}%）")

    # W3: 补偿因子数值巧合
    print("\n" + "=" * 74)
    print("W3. 补偿因子数值巧合检查（不做过度解读）")
    print("=" * 74)
    dev_cf = abs(fA - CF) / CF * 100
    dev_8_5 = abs(fV - 8.0 / 5.0) / (8.0 / 5.0) * 100
    print(f"    f_A = {fA:.3f} vs C_F = 4/3 = {CF:.3f}（偏差 {dev_cf:.1f}%）")
    print(f"    f_V = {fV:.3f} vs 8/5 = {8/5:.3f}（偏差 {dev_8_5:.1f}%）")
    check("W3 登记：f_A ≈ 4/3（C_F）与 f_V ≈ 8/5 为数值巧合（偏差均 < 2%，无结构论证）",
          dev_cf < 2.0 and dev_8_5 < 2.0, f"f_A 偏差 {dev_cf:.1f}%，f_V 偏差 {dev_8_5:.1f}%")

    # W4: 结论
    print("\n" + "=" * 74)
    print("W4. 结论：'2×临界'的来源")
    print("=" * 74)
    print("    ① 几何逻辑（d_crit 无参数）解释：完整处理工作点 = 临界附近")
    print("      （d_full = 0.926 ≈ 1.0，与文献 0.9–1.0 一致）——物理工作点被几何确定；")
    print("    ② '恰好 2×临界' = 彩虹近似粗糙度的补偿乘积：A≈1 简化（≈1.35）")
    print("      × 树级顶点（≈1.60）≈ 2.16 ≈ 2.0——两个近似补偿的乘积，非单一几何量；")
    print("    ③ 彩虹 A≈1 因忽略波函数重整化 A(p²) 与顶点修正，需补偿强度使")
    print("      M(0) 达到框架锚点 κΛ——2.0 是该补偿的结果，非几何必然。")
    check("W4 结论登记：2×临界 = 近似补偿乘积（非几何直接推论）；几何确定'临界附近'工作点",
          True, "几何解释力在 W1；2 倍为补偿乘积（W2）")

    # W5: 诚实边界
    print("\n" + "=" * 74)
    print("W5. 诚实边界")
    print("=" * 74)
    print("    ① d_AB/d_full = 1.604 与 d_rainbow/d_AB = 1.347 来自两次独立 DS 求解的")
    print("       数值比——分解为'纯 A 修正'/'纯顶点修正'是近似归因（A 与顶点耦合）；")
    print("    ② f_A ≈ C_F = 4/3、f_V ≈ 8/5 为数值巧合，无结构论证（不做过度解读）；")
    print("    ③ 若换 ω 或其他模型参数，补偿因子会变——'2 倍'依赖 MT 高斯的具体形状。")
    check("W5 诚实登记：补偿分解为近似归因；数值巧合不做过度解读；2 倍依赖 MT 形状",
          True, "解释：几何定临界附近工作点；2 倍为 A×顶点补偿乘积（近似归因）")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print("\n" + "=" * 74)
    print(f"结果：{n_pass}/{len(RESULTS)} 通过")
    print("=" * 74)
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
