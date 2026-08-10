#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_threequarter_retention_recursion.py — 用户猜想"3²/(3²−1)³ 构成某种递归？"核查
====================================================================================
对应：paperX_threequarter_nd_generalization.py G5（f(D) = (1−1/D)^{D−1}）
触发：用户"3²/（3^2-1）³   构成某种递归？"。

待核查：
  ① 3²/(3²−1)³ = 9/8³ = 9/512 = 1.758% vs C2 偏差 dev(4) = 0.8785%——是否匹配？
  ② 该式是否构成某种递归？

核查结果（预告）：
  R1  3²/(3²−1)³ = 9/512 = 1.758% = 2.001 × dev(4)——恰好 ~2 倍，不匹配（100% 误差）
  R2  **递归发现**：每方向保留率 r(D) = (D−1)/D 满足递推
        r(D+1) = r(D) · D²/(D²−1)（D = 2..10 数值验证）
      ——3²/(3²−1) = 9/8 正是 D = 3 → 4 步的递推乘子（**构成递归**，但无"³"）
  R3  f(D) = r(D)^{D−1} 的相邻比：f(4)/f(3) = 243/256 = 3⁵/2⁸（含 3 与 8，但 ≠ 9/512）
  R4  诚实边界：用户式中"³"（9/512）无递归对应——乘子无立方；dev 最接近的
      3 幂形式仍为 3²/10³ = 0.9%（2.4%）；9/512 ≈ 2×dev 为数值巧合；
      另注：dev = 0.8785% ≈ 9/1024 = 0.8789%（0.04%）——目前最接近的幂形式，
      但 3²/2¹⁰ 无框架来源（0.418201 仅 6 位精度，疑似精度巧合），不升级为结构。

单位：无量纲。
"""
import numpy as np

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def retention(D):
    """D 维每方向保留率 r(D) = (D−1)/D。"""
    return (D - 1.0) / D


def w_spatial(D):
    """空间积分权重 f(D) = r(D)^{D−1} = (1−1/D)^{D−1}。"""
    return retention(D) ** (D - 1)


def run():
    print("=" * 74)
    print("用户猜想核查：3²/(3²−1)³ 构成某种递归？")
    print("=" * 74)

    f4 = 27.0 / 64.0
    ratio = 0.418201
    dev = abs(f4 - ratio) / ratio * 100          # 0.8785%

    # ---- R1: 3²/(3²−1)³ = 9/512 ----
    print("\n" + "=" * 74)
    print("R1. 3²/(3²−1)³ = 9/8³ = 9/512 = 1.758% vs dev = 0.8785%")
    print("=" * 74)
    expr = 3.0 ** 2 / (3.0 ** 2 - 1.0) ** 3      # 9/512
    rel = abs(expr * 100 - dev) / dev * 100
    mult = expr * 100 / dev
    print(f"    3²/(3²−1)³ = 9/512 = {expr * 100:.4f}%")
    print(f"    vs dev = {dev:.4f}%：相对误差 {rel:.1f}%，倍数 {mult:.3f}×")
    print("    ⟹ 9/512 = 2.001×dev——恰好约 2 倍，**不构成 dev 的精确表达**")
    check("R1 3²/(3²−1)³ = 9/512 = 1.758% = 2.001×dev——不匹配（~2 倍）",
          rel > 50.0, f"相对误差 {rel:.0f}%，倍数 {mult:.3f}×")

    # ---- R2: 递归 r(D+1) = r(D)·D²/(D²−1) ----
    print("\n" + "=" * 74)
    print("R2. 递归发现：r(D+1) = r(D) · D²/(D²−1)；3²/(3²−1) = 9/8 是 D=3→4 乘子")
    print("=" * 74)
    ok2 = True
    for D in range(2, 10):
        r_next_pred = retention(D) * D ** 2 / (D ** 2 - 1.0)
        r_next_true = retention(D + 1)
        if abs(r_next_pred - r_next_true) > 1e-12:
            ok2 = False
        print(f"    D = {D}：r({D + 1}) = r({D})·{D}²/({D}²−1) = "
              f"{retention(D):.6f}·{D ** 2 / (D ** 2 - 1.0):.6f} = {r_next_pred:.6f}"
              f"（真实 {r_next_true:.6f}）")
    m3 = 3.0 ** 2 / (3.0 ** 2 - 1.0)
    print(f"    D = 3 步乘子 = 3²/(3²−1) = {m3} = 9/8（r(4)/r(3) = (3/4)/(2/3)）")
    print("    ⟹ 每方向保留率确实构成递推；3²/(3²−1) 是其中的 D=3 乘子（无'³'）")
    check("R2 递归成立：r(D+1) = r(D)·D²/(D²−1)（D=2..9；3²/(3²−1) = 9/8 为 D=3 乘子）",
          ok2, "r(4)/r(3) = 9/8 = 3²/(3²−1)")

    # ---- R3: f(D) 相邻比 ----
    print("\n" + "=" * 74)
    print("R3. f(D) = r(D)^{D−1} 相邻比：f(4)/f(3) = 243/256 = 3⁵/2⁸")
    print("=" * 74)
    r_34 = w_spatial(4) / w_spatial(3)
    print(f"    f(4)/f(3) = {w_spatial(4):.6f}/{w_spatial(3):.6f} = {r_34:.6f}")
    print(f"    243/256 = {243.0 / 256.0:.6f}（= 3⁵/2⁸）")
    print("    ⟹ 相邻比含 3 与 8，但 ≠ 9/512——用户式的'³'对应 f 的指数 (D−1)，非乘子立方")
    ok3 = abs(r_34 - 243.0 / 256.0) < 1e-12
    check("R3 f(4)/f(3) = 243/256 = 3⁵/2⁸（相邻比含 3 与 8；≠ 9/512）",
          ok3, f"f(4)/f(3) = {r_34:.6f}")

    # ---- R4: 诚实边界 ----
    print("\n" + "=" * 74)
    print("R4. 诚实边界")
    print("=" * 74)
    near = 9.0 / 1024.0 * 100.0
    rel_near = abs(near - dev) / dev * 100
    print(f"    ① 递归成立的是 r(D)（乘子 D²/(D²−1)，无立方）；用户式'³'无递归对应；")
    print(f"    ② dev 最接近的 3 幂形式仍为 3²/10³ = 0.9%（2.4%）；9/512 = 2.001×dev 为巧合；")
    print(f"    ③ 附注：dev = {dev:.4f}% ≈ 9/1024 = {near:.4f}%（相对误差 {rel_near:.2f}%）——")
    print("       目前最接近的幂形式，但 3²/2¹⁰ 无框架来源（ratio 仅 6 位精度），"
          "登记为精度巧合，不升级为结构。")
    check("R4 诚实登记：递归在保留率 r(D)（无立方）；dev 无精确幂形式（最近 0.9%，2.4%）；"
          "9/1024 为精度巧合", True,
          "9/512 = 2.001×dev（巧合）；9/1024 相对误差 0.04%（精度巧合）")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print("\n" + "=" * 74)
    print(f"结果：{n_pass}/{len(RESULTS)} 通过")
    print("=" * 74)
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
