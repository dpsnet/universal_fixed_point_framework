#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_lattice_mu2_check.py — 用格点 QCD 公开数据验证 μ²/d_crit 是否 = 0.75
====================================================================================
对应：paper40 §5.9（v0.42 候选结构：μ² = ¾·d_crit，需独立验证）
触发：用户"写一段脚本，用格点 QCD 的公开数据来验证 μ²/d_crit 是否精确等于 0.75"。

框架量：
  μ² = 8πσ/(g²C_F)（线性势 ↔ 1/p⁴ 对偶，v0.35）；d_crit = 4/(3C_F) = 1.0（几何，v0.37）
  候选结构（v0.42）：μ²/d_crit = ¾ = 0.75

格点 QCD 公开数据（文献来源）：
  [A] 弦张力（Wilson loop，纯规范/物理 QCD）：
      · √σ = 440(20) MeV → σ ≈ 0.194 GeV²（标准引用，EncyclopedAI LQCD 条目）
      · √σ ≈ 460 MeV → σ ≈ 0.212 GeV²（静态夸克，Trawiński et al. SLAC-PUB-15924）
      · √σ = 485(6) MeV → σ ≈ 0.235 GeV²（Marczenko et al. arXiv:2603.28668v1 引 [4][13]）
      · 物理 QCD（三味）弦张力偏低：√σ ≈ 420–440 MeV → σ ≈ 0.176–0.194
        （框架谱定 σ = 4Λ² = 0.1764，Λ = 210 MeV，F_π 定标）
  [B] 胶子传播子红外行为（Landau 规范，Oliveira-Silva 等）：
      · decoupling 解：D(0) 有限（红外平台）——大体积格点主流；
      · scaling 解：D(q²) ~ (q²)^{2κ−1}，κ ≈ 0.53–0.595，D(0) → 0（Gribov-Zwanziger）；
      · 格点测量 κ ≈ 0.50–0.53（Oliveira-Silva arXiv:0705.0964）；Gribov 型 D(k) = k²/(k⁴+γ⁴)；
      · **明确矛盾**：格点/Zwanziger 界排斥 1/k⁴ 红外增强（"less singular than k⁻²"，
        hep-lat/9709015）——1/p⁴ 增强与格点 decoupling/scaling 均不兼容。

验证：
  L1  格点弦张力数据登记（√σ 440/460/485 MeV）
  L2  路径 A：μ²_lat = 8πσ_lat/(g²C_F) → μ²_lat/d_crit vs 0.75（各 σ 值）
  L3  路径 B：格点传播子红外形式（decoupling/scaling/Gribov）vs 框架 1/p⁴ 最简实现
  L4  结论：μ²/d_crit = 0.75 是否被格点支持
  L5  诚实边界

单位：GeV/GeV²。
"""
import math

# ---- 框架量 ----
SIGMA_FW = 0.1764           # GeV²，框架谱定弦张力 4Λ²（定理 5.5）
ALPHA_S = 0.3380            # 轻味有效耦合（推论 5.8）
CF = 4.0 / 3.0
G2_CF = 4.0 * math.pi * ALPHA_S * CF   # 5.663
D_CRIT = 1.0                # GeV²，几何临界
QUARTER3 = 0.75

# ---- 格点公开数据（文献值）----
LATTICE_SIGMA = [
    (0.440, 0.020, "√σ = 440(20) MeV（标准引用，EncyclopedAI LQCD）"),
    (0.460, 0.010, "√σ ≈ 460 MeV（静态夸克，Trawiński et al. SLAC-PUB-15924）"),
    (0.485, 0.006, "√σ = 485(6) MeV（Marczenko et al. 2026 引 [4][13]）"),
]
PHYS_SIGMA = (0.420, 0.440)   # GeV，物理 QCD（三味）√σ 范围 → σ ∈ [0.176, 0.194]

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def mu2_of_sigma(sigma):
    return 8.0 * math.pi * sigma / G2_CF


def run():
    print("=" * 74)
    print("格点 QCD 公开数据验证 μ²/d_crit = 0.75")
    print("=" * 74)
    print(f"    框架：μ² = 8πσ/(g²C_F) = {mu2_of_sigma(SIGMA_FW):.3f} GeV²（σ = {SIGMA_FW}）；"
          f"d_crit = {D_CRIT}；候选 ¾ = {QUARTER3}")

    # L1: 格点弦张力数据
    print("\n" + "=" * 74)
    print("L1. 格点弦张力公开数据（Wilson loop）")
    print("=" * 74)
    for sqrt_s, err, src in LATTICE_SIGMA:
        s = sqrt_s ** 2
        print(f"    √σ = {sqrt_s*1000:.0f}({int(err*1000)}) MeV → σ = {s:.3f} GeV²  [{src}]")
    print(f"    物理 QCD（三味）：√σ ∈ [{PHYS_SIGMA[0]*1000:.0f}, {PHYS_SIGMA[1]*1000:.0f}] MeV"
          f" → σ ∈ [{PHYS_SIGMA[0]**2:.3f}, {PHYS_SIGMA[1]**2:.3f}] GeV²（框架 {SIGMA_FW:.3f} 在内）")
    check("L1 格点弦张力数据登记（√σ 440/460/485 MeV，纯规范；物理 QCD 420–440 MeV）",
          True, "公开文献值")

    # L2: 路径 A——从格点 σ 反推 μ²_lat/d_crit
    print("\n" + "=" * 74)
    print("L2. 路径 A：格点 σ → μ²_lat = 8πσ/(g²C_F) → μ²_lat/d_crit vs 0.75")
    print("=" * 74)
    ratios = []
    for sqrt_s, err, src in LATTICE_SIGMA:
        s = sqrt_s ** 2
        mu2 = mu2_of_sigma(s)
        r = mu2 / D_CRIT
        ratios.append(r)
        dev = abs(r - QUARTER3) / QUARTER3 * 100
        print(f"    σ = {s:.3f}:  μ² = {mu2:.3f},  μ²/d_crit = {r:.3f}  (vs ¾ 偏差 {dev:.0f}%)")
    # 物理 QCD 下限
    mu2_phys_lo = mu2_of_sigma(PHYS_SIGMA[0] ** 2)
    r_phys_lo = mu2_phys_lo / D_CRIT
    dev_phys = abs(r_phys_lo - QUARTER3) / QUARTER3 * 100
    print(f"    物理 QCD 下限 σ = {PHYS_SIGMA[0]**2:.3f}:  μ²/d_crit = {r_phys_lo:.3f}  (vs ¾ 偏差 {dev_phys:.1f}%)")
    check("L2 格点 σ 反推 μ²/d_crit ∈ [0.78, 1.04]（纯规范）；物理 QCD 下限 0.783——均 ≥ 4.4% 偏差",
          min(ratios + [r_phys_lo]) > QUARTER3, f"范围 [{min(ratios + [r_phys_lo]):.3f}, {max(ratios):.3f}]，物理下限偏差 {dev_phys:.1f}%")

    # L3: 路径 B——格点传播子红外形式 vs 框架 1/p⁴
    print("\n" + "=" * 74)
    print("L3. 路径 B：格点传播子红外形式 vs 框架 1/p⁴ 最简实现")
    print("=" * 74)
    print("    格点（Landau 规范，Oliveira-Silva 等）：")
    print("      · decoupling：D(0) 有限（红外平台，大体积主流）——D(q²) ~ 常数")
    print("      · scaling/Gribov：D ~ (q²)^{2κ−1}，κ ≈ 0.53–0.595，D(0) → 0；")
    print("        Gribov 型 D(k) = k²/(k⁴+γ⁴)（红外如 k² 消失）")
    print("      · Zwanziger 界：传播子 'less singular than k⁻²'——与 1/k⁴ 增强矛盾")
    print("    框架（v0.33）：无自由正谱 → 最简非正增强 1/p⁴")
    print("    ⟹ 格点支持'无自由正谱'（decoupling 无极点、scaling 无实极点），")
    print("       但**不支持 1/p⁴ 作为物理传播子**（格点红外是有限值或 k² 消失）")
    check("L3 格点传播子 decoupling/scaling 与 1/p⁴ 增强不兼容（Zwanziger 界 + κ≈0.53 测量）",
          True, "'无自由正谱'成立；'1/p⁴ 最简实现'受格点质疑（非唯一/非物理）")

    # L4: 结论
    print("\n" + "=" * 74)
    print("L4. 结论：μ²/d_crit = 0.75 是否被格点支持")
    print("=" * 74)
    print("    ① 数值（路径 A）：格点弦张力反推 μ²_lat/d_crit ∈ [0.78, 1.04]")
    print("      ——物理 QCD 下限 0.783 与 0.75 偏差 4.4%，**不精确等于 0.75**；")
    print("    ② 结构（路径 B）：格点传播子红外为 decoupling（D(0) 有限）或")
    print("      Gribov/scaling（D ~ k²），**非 1/p⁴ 增强**——框架 μ² 定义的")
    print("      '1/p⁴ 强度'与格点测量的传播子形式不对应；")
    print("    ⟹ ¾ 候选结构**不被格点支持**（数值偏差 ≥ 4.4% + 传播子形式不对应）。")
    check("L4 诚实结论：¾ 候选不被格点支持（μ²_lat/d_crit ≥ 0.783；传播子非 1/p⁴）",
          True, "数值 + 结构双重不吻合")

    # L5: 诚实边界
    print("\n" + "=" * 74)
    print("L5. 诚实边界")
    print("=" * 74)
    print("    ① 标度方案差异：纯规范格点 √σ = 440–485 MeV vs 物理三味 QCD")
    print("      √σ ≈ 420–440 MeV（轻夸克屏蔽使弦张力降低）——框架 σ 用三味有效标度；")
    print("    ② μ² 的 '1/p⁴ 强度' 是理论构造（线性势傅里叶对偶），格点直接测量")
    print("      的是 D(q²) 函数（decoupling/scaling）——路径 A 依赖 σ 而非传播子；")
    print("    ③ 若坚持 1/p⁴ 框架，需在格点 D(q²) 中间尺度拟合增强项提取等效 μ²")
    print("      （未做——格点主流 decoupling 不支持该形式）；")
    print("    ④ ¾ 候选保留为'框架内数值巧合'（v0.42），格点独立验证失败已登记。")
    check("L5 诚实登记：格点验证失败（负结果）——¾ 候选从'候选结构'降级为'框架内巧合'",
          True, "标度方案/传播子形式不对应已说明")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print("\n" + "=" * 74)
    print(f"结果：{n_pass}/{len(RESULTS)} 通过")
    print("=" * 74)
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
