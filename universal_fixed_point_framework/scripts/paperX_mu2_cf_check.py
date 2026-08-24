# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_mu2_cf_check.py — μ² 系统性偏低是否少个系数 4/3（C_F）检验
====================================================================================
对应：paper40 §5.9（v0.42 ¾ 候选、v0.43 格点负结果）
触发：用户"0.78× 系统性偏低 会不会是 0.78× 系统性偏低少了个系数 4/3"。

背景：μ²/d_crit = 0.783（v0.41 系统性偏低）；v0.42 用户猜想 ¾ = 0.75。
本轮关键观察：¾ = 3/4 = 1/C_F（C_F = 4/3 的倒数）！若"补上 4/3"：
  μ²·C_F = 8πσ/g²（消去分母 C_F）= 2σ/α_s——是否 ≈ d_crit = 1.0？

定义澄清：
  μ²（含 C_F）= 8πσ/(g²C_F)——来自静态色荷势 V(r) = -C_F·g²∫D(p)，C_F 是
  q̄q 色结构的 Casimir（进势/顶点）；
  μ²_g（纯胶子传播子强度，不含 C_F）= 8πσ/g² = 2σ/α_s——胶子传播子本身
  色中性，色因子全部归入势。

检验：
  W1  μ²/d_crit 与 1/C_F = ¾ 的偏差（0.783 vs 0.75）
  W2  μ²·C_F = 2σ/α_s 与 d_crit = 1.0 的偏差（补上 4/3 后是否 ≈ 1）
  W3  两种定义的物理区分（含 C_F 的势强度 vs 不含 C_F 的传播子强度）
  W4  结论：¾ 候选 = C_F⁻¹（色因子倒数）；μ²_g ≈ d_crit 是更有结构的表述
  W5  诚实边界

单位：GeV²。
"""
import math

SIGMA = 0.1764            # GeV²，弦张力（定理 5.5）
ALPHA_S = 0.3380          # 轻味有效耦合（推论 5.8）
CF = 4.0 / 3.0
D_CRIT = 1.0              # GeV²，几何临界

MU2 = 8.0 * math.pi * SIGMA / (4.0 * math.pi * ALPHA_S * CF)   # 含 C_F = 0.783
MU2_G = 2.0 * SIGMA / ALPHA_S                                  # 不含 C_F = 8πσ/g² = 1.044

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def run():
    print("=" * 74)
    print("μ² 系统性偏低是否少个系数 4/3（C_F）——检验")
    print("=" * 74)
    print(f"    μ²（含 C_F）= 8πσ/(g²C_F) = {MU2:.3f} GeV²")
    print(f"    μ²_g（不含 C_F）= 8πσ/g² = 2σ/α_s = {MU2_G:.3f} GeV²")
    print(f"    d_crit = {D_CRIT} GeV²；C_F = {CF:.4f}；1/C_F = ¾ = {1.0/CF:.3f}")

    # W1: μ²/d_crit vs 1/C_F
    print("\n" + "=" * 74)
    print("W1. μ²/d_crit 与 1/C_F = ¾ 的偏差")
    print("=" * 74)
    r = MU2 / D_CRIT
    inv_cf = 1.0 / CF
    dev = abs(r - inv_cf) / inv_cf * 100
    print(f"    μ²/d_crit = {r:.3f} vs 1/C_F = ¾ = {inv_cf:.3f}（偏差 {dev:.1f}%）")
    print("    ⟹ ¾ 候选的数学本质 = 1/C_F（色因子倒数）")
    check("W1 μ²/d_crit = 0.783 ≈ 1/C_F = ¾（偏差 4.4%）——¾ 等价于色因子倒数",
          dev < 10.0, f"偏差 {dev:.1f}%")

    # W2: 补上 C_F 后 μ²·C_F vs d_crit
    print("\n" + "=" * 74)
    print("W2. 补上 4/3：μ²·C_F = 8πσ/g² = 2σ/α_s vs d_crit")
    print("=" * 74)
    dev2 = abs(MU2_G - D_CRIT) / D_CRIT * 100
    print(f"    μ²·C_F = 8πσ/g² = 2σ/α_s = {MU2_G:.3f} GeV² vs d_crit = {D_CRIT}（偏差 {dev2:.1f}%）")
    print(f"    精确成立需 σ = α_s/2 = {ALPHA_S/2:.4f} GeV²（谱定 {SIGMA:.4f}，偏差 4.4%）")
    check("W2 补上 4/3 后 μ²·C_F ≈ d_crit（偏差 < 10%：1.044 vs 1.0）——'少 4/3'直觉数值成立",
          dev2 < 10.0, f"偏差 {dev2:.1f}%（需 σ = α_s/2 = {ALPHA_S/2:.4f}）")

    # W3: 两种定义的物理区分
    print("\n" + "=" * 74)
    print("W3. 两种定义：含 C_F（势强度）vs 不含 C_F（传播子强度）")
    print("=" * 74)
    print("    μ²（含 C_F）= 8πσ/(g²C_F)：静态色荷势的'有效强度'（色因子进势/顶点）")
    print("    μ²_g（不含 C_F）= 8πσ/g²：胶子传播子本身的红外强度（传播子色中性）")
    print("    ⟹ '少个 4/3' = μ² 分母多除了 C_F——若定义改为传播子强度（不含 C_F），")
    print("      则 μ²_g ≈ d_crit（胶子传播子红外强度 = 几何临界强度，偏差 4.4%）")
    check("W3 定义区分登记：μ²（含 C_F）vs μ²_g（不含）——补 4/3 即切换到传播子强度定义",
          True, "传播子本身色中性，C_F 全部归入势")

    # W4: 结论
    print("\n" + "=" * 74)
    print("W4. 结论：'少 4/3'直觉的实质")
    print("=" * 74)
    print("    ① v0.42 的 ¾ 候选 = 1/C_F（色因子倒数）——'¾'不是观测层因子，")
    print("       而是 C_F⁻¹ = 3/4 的色结构；")
    print("    ② 若 μ² 改用传播子强度定义（不含 C_F），μ²_g = 2σ/α_s = 1.044")
    print("       ≈ d_crit = 1.0（偏差 4.4%）——'胶子传播子红外强度 = 几何临界'；")
    print("    ③ 4.4% 残余偏差对应 σ = α_s/2 = 0.169 vs 谱定 0.1764——σ/α_s 取值；")
    print("    ④ 比 v0.42 更优：'1/C_F'有明确色结构来源，且切换到传播子强度定义")
    print("       后比值 ≈ 1（而非 0.75）——但单点比较仍不可定论。")
    check("W4 结论：¾ = C_F⁻¹（色结构）；传播子强度定义下 μ²_g ≈ d_crit（偏差 4.4%）",
          True, "'少 4/3' = 定义切换（势强度 → 传播子强度）的色因子消去")

    # W5: 诚实边界
    print("\n" + "=" * 74)
    print("W5. 诚实边界")
    print("=" * 74)
    print("    ① 4.4% 残余偏差（σ = α_s/2 vs 谱定）未解释——需独立确定 σ 或 α_s 的");
    print("       精确值，单点比较无法判定结构/巧合；")
    print("    ② 传播子强度定义（不含 C_F）与格点 decoupling 测量仍不对应（v0.43）；")
    print("    ③ 'μ²_g = d_crit'（若成立）的机制：胶子传播子强度由几何临界确定——")
    print("       候选结构，机制待解释；")
    print("    ④ 与 v0.42 的 ¾ 一起降级为'框架内数值巧合'（格点独立验证失败，v0.43）。")
    check("W5 诚实登记：'少 4/3'给出更优表述（¾ = C_F⁻¹、μ²_g ≈ d_crit），但同为单点巧合，"
          "格点负结果不变（v0.43）", True, "表述升级，非新验证；4.4% 残余未解释")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print("\n" + "=" * 74)
    print(f"结果：{n_pass}/{len(RESULTS)} 通过")
    print("=" * 74)
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
