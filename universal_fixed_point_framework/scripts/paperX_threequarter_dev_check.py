#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_threequarter_dev_check.py — 用户猜想"0.88% ≈ 3³/10³"的数值核查
====================================================================================
对应：paperX_threequarter_fD_chart.py C2（D=4 偏差 0.88%）
触发：用户"0.88% 约为 3^3/10^3"。

待核查：
  偏差 dev(4) = |f(4) − ratio| / ratio = 0.8786%
  用户猜想：dev ≈ 3³/10³ = 27/1000 = 2.7%

核查结果（预告）：
  V1  3³/10³ = 2.7% vs 0.8786%：偏差 207%（差 ~3.07 倍）——**不成立**
  V2  最接近的 3 幂形式：3²/10³ = 9/1000 = 0.9% vs 0.8786%：相对误差 2.4%（接近非精确）
  V3  用户公式的三分之一：(3³/10³)/3 = 3²/10³ = 0.9%（与 V2 同——"0.88% ≈ 3³/10³
      再除以 3"即 3²/10³）；3×(0.88%) = 2.64% vs 2.7%：相对误差 2.2%
  V4  诚实边界：单点比较内 0.9% vs 0.88% 的 2.4% 差异无机制来源——登记为数值巧合

单位：无量纲（偏差百分比）。
"""
import numpy as np

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def run():
    print("=" * 74)
    print("用户猜想核查：0.88% ≈ 3³/10³")
    print("=" * 74)

    # 精确偏差（paperX_threequarter_fD_chart.py H2：D=4）
    f4 = 27.0 / 64.0                     # f(4) = ¾³ = 0.421875
    ratio = 0.418201                     # I_fw/I_MT（g_int 数值积分）
    dev = abs(f4 - ratio) / ratio * 100  # 0.8786%
    print(f"    dev(4) = |{f4:.6f} − {ratio:.6f}| / {ratio:.6f} × 100 = {dev:.4f}%")

    # ---- V1: 3³/10³ = 2.7% ----
    print("\n" + "=" * 74)
    print("V1. 3³/10³ = 27/1000 = 2.7% vs 0.8786%")
    print("=" * 74)
    c1_pct = 3.0 ** 3 / 10.0 ** 3 * 100.0      # 3³/10³ 换算为百分数 = 2.7%
    rel = abs(c1_pct - dev) / dev * 100
    factor = c1_pct / dev
    print(f"    3³/10³ = 27/1000 = {c1_pct:.1f}%")
    print(f"    vs dev = {dev:.2f}%：相对误差 {rel:.0f}%，比值 {factor:.2f}×")
    print("    ⟹ 3³/10³ = 2.7% 与 0.88% 相差 ~3.07 倍——**猜想不成立**")
    check("V1 3³/10³ = 2.7% ≠ 0.88%（差 3.07 倍）——猜想不成立",
          rel > 50.0, f"相对误差 {rel:.0f}%")

    # ---- V2: 网格扫描 3^a/10^b 候选（含 3⁴/10⁴）----
    print("\n" + "=" * 74)
    print("V2. 网格扫描 3^a/10^b（a=1..5，b=2..5）：3⁴/10⁴ = 0.81% 排名")
    print("=" * 74)
    c4_pct = 3.0 ** 4 / 10.0 ** 4 * 100.0      # 3⁴/10⁴ = 81/10000 = 0.81%
    rel4 = abs(c4_pct - dev) / dev * 100
    print(f"    3⁴/10⁴ = 81/10000 = {c4_pct:.2f}% vs dev = {dev:.2f}%：相对误差 {rel4:.2f}%")
    cands = []
    for a in range(1, 6):
        for b in range(2, 6):
            v = 3.0 ** a / 10.0 ** b * 100.0
            cands.append((abs(v - dev) / dev * 100, a, b, v))
    cands.sort()
    best = cands[0]
    print(f"    网格最优：3^{best[1]}/10^{best[2]} = {best[3]:.3f}%（相对误差 {best[0]:.2f}%）")
    for i, (rel, a, b, v) in enumerate(cands[:4], 1):
        print(f"      第 {i}：3^{a}/10^{b} = {v:.3f}% （相对误差 {rel:.2f}%）")
    # 3⁴/10⁴ 的排名
    rank4 = [i for i, (rel, a, b, v) in enumerate(cands) if a == 4 and b == 4][0] + 1
    print(f"    3⁴/10⁴ = 0.81% 排名第 {rank4}（相对误差 {rel4:.2f}%），"
          f"差于 3²/10³ = 0.9%（{cands[0][0]:.2f}%）")
    ok2 = best[0] < 10.0 and rel4 < 10.0 and abs(c4_pct - 0.81) < 1e-12 \
        and cands[0][1] == 2 and cands[0][2] == 3
    check("V2 网格扫描：3²/10³ = 0.9% 最优（2.4%）；3⁴/10⁴ = 0.81% 次之（7.8%）",
          ok2, f"3⁴/10⁴ 相对误差 {rel4:.2f}%（最优 3²/10³ {cands[0][0]:.2f}%）")

    # ---- V3: 解释 '3³/10³ ÷ 3' ----
    print("\n" + "=" * 74)
    print("V3. 两种等价读法：(3³/10³)/3 = 3²/10³；3×dev = 2.64% vs 2.7%")
    print("=" * 74)
    c3a_pct = c1_pct / 3.0                     # (3³/10³)/3 = 3²/10³ = 0.9%
    c3b_pct = dev * 3.0                        # 3 × 0.88% = 2.64%
    rel3b = abs(c3b_pct - c1_pct) / c1_pct * 100
    print(f"    (3³/10³)/3 = {c3a_pct:.2f}%（= 3²/10³，与 V2 最优相同）")
    print(f"    3 × dev = {c3b_pct:.2f}% vs 3³/10³ = {c1_pct:.1f}%：相对误差 {rel3b:.1f}%")
    print("    ⟹ '0.88% ≈ 3³/10³'仅在除以 3（即 3²/10³）后才接近")
    check("V3 (3³/10³)/3 = 3²/10³ = 0.9%≈0.88%；3×0.88% = 2.64% ≈ 2.7%（2.2%）",
          rel3b < 5.0, f"相对误差 {rel3b:.1f}%")

    # ---- V4: 诚实边界 ----
    print("\n" + "=" * 74)
    print("V4. 诚实边界")
    print("=" * 74)
    print("    ① 0.88% ≠ 3³/10³ = 2.7%（差 3.07 倍）；最接近的 3 幂形式为")
    print("       3²/10³ = 0.9%（相对误差 2.4%）——接近但不精确；")
    print("    ② dev 为单点比较（截断/UV 尾数值选择内），0.9% vs 0.88% 的 2.4% 差异")
    print("       无机制来源——登记为**数值巧合**，无结构证据；")
    print("    ③ 与 C1（代数严格：统一恒等 ⟹ D=4 唯一）不同——C1 是精确等式，")
    print("       此处 0.9% ≈ 0.88% 是近似。")
    check("V4 诚实登记：'0.88% ≈ 3³/10³'不成立（2.7% vs 0.88%）；"
          "修正版 3²/10³ = 0.9% 接近但为数值巧合", True,
          "无结构证据，C1 代数严格不变")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print("\n" + "=" * 74)
    print(f"结果：{n_pass}/{len(RESULTS)} 通过")
    print("=" * 74)
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
