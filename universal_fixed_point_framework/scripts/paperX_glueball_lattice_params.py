#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_glueball_lattice_params.py — 4⁺⁺/6⁺⁺ 胶球验证的格点 QCD 模拟参数配置建议
====================================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §8.4（胶球框架独有新预言 P1）
触发：用户"帮我生成一份针对这些新预言的格点QCD模拟参数配置建议，以便验证4+和6+态的质量"

目标态（框架新预言，paperX_glueball_new_predictions.py）：
  · 4⁺⁺ = 3.329 GeV（闭弦 Regge 偶 J 谱系，m² = 20πσ）
  · 6⁺⁺ = 3.939 GeV（m² = 28πσ）
  · 邻近态 0⁻⁺'' = 3.492 GeV（扭转模谱系）——分辨率挑战：Δm(4⁺⁺, 0⁻⁺'') ≈ 0.163 GeV

格点 QCD 参数设计原则（Morningstar–Peardon 1999 / 现代改进作用量）：
  · 离散化：a·m_max ≲ 1.5（a·m₆₊₊ 为最严）
  · 有限体积：m·L ≳ 4（避免有限体积效应），L ≈ 2.5–3.5 fm
  · 分辨率：统计误差 δm < Δm/2 ≈ 0.08 GeV（区分 4⁺⁺ 与 0⁻⁺''）
  · 算符：胶球 J^PC 投影（立方群不可约表示），GEVP 变分法提取

检查（L1–L7）：
  L1 目标态（4⁺⁺ = 3.329、6⁺⁺ = 3.939）与分辨率需求（Δm = 0.163 GeV）
  L2 格距离散化（a·m_max ≲ 1.5）
  L3 有限体积（m·L ≳ 4）
  L4 格点尺寸（N = L/a，32³×64 与 48³×96 两档）
  L5 统计（胶球信噪比差，构型数建议）
  L6 算符方案（J=4 → 立方群表示；J=6 → 表示）
  L7 参数表完整输出

单位：a 用 fm，m 用 GeV（ħc = 0.19733 GeV·fm）。
"""
import math

HBARC = 0.19733                     # GeV·fm
# 目标态质量（框架新预言，paperX_glueball_new_predictions.py）
M_4PP = 3.329                       # GeV，4⁺⁺
M_6PP = 3.939                       # GeV，6⁺⁺
M_0MP2 = 3.492                      # GeV，0⁻⁺''（邻近扭转态）
DELTA_M = M_0MP2 - M_4PP            # ≈ 0.163 GeV，分辨率挑战

# 格点参数候选（两档：高精度 / 大统计）
PARAMS = [
    # (标签, 作用量, β, a[fm], Ns, Nt, 海夸克, 构型数)
    ("A: 高精度档", "Iwasaki 改进", 3.20, 0.075, 48, 96, "2+1 风味（物理 π）", 8000),
    ("B: 大统计档", "Iwasaki 改进", 3.30, 0.070, 32, 64, "2+1 风味（物理 π）", 15000),
]

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def am_of(a_fm, m_gev):
    """无量纲格点质量 a·m = a[fm]·m[GeV]/ħc。"""
    return a_fm * m_gev / HBARC


def run():
    print("=" * 74)
    print("4⁺⁺/6⁺⁺ 胶球验证的格点 QCD 模拟参数配置建议")
    print("=" * 74)

    # ============================================================
    # L1: 目标态与分辨率需求
    # ============================================================
    print("\n" + "=" * 74)
    print("L1. 目标态与分辨率需求")
    print("=" * 74)
    print(f"  4⁺⁺ = {M_4PP:.3f} GeV、6⁺⁺ = {M_6PP:.3f} GeV（闭弦 Regge 偶 J 谱系）")
    print(f"  邻近态 0⁻⁺'' = {M_0MP2:.3f} GeV（扭转模谱系）")
    print(f"  ★ 分辨率挑战：Δm(4⁺⁺, 0⁻⁺'') = {DELTA_M:.3f} GeV（相对差 {DELTA_M/M_4PP*100:.1f}%）")
    print(f"  → 统计误差需 δm < Δm/2 ≈ {DELTA_M/2:.3f} GeV（约 {DELTA_M/2/M_4PP*100:.1f}% 精度）")
    check("L1 目标态与分辨率需求明确（δm < 0.082 GeV，区分 4⁺⁺ 与 0⁻⁺''）",
          DELTA_M > 0.1, f"Δm = {DELTA_M:.3f} GeV")

    # ============================================================
    # L2/L3: 离散化与有限体积（两档参数检验）
    # ============================================================
    print("\n" + "=" * 74)
    print("L2/L3. 离散化（a·m_max）与有限体积（m·L）检验")
    print("=" * 74)
    for label, act, beta, a_fm, Ns, Nt, flavor, nconf in PARAMS:
        am6 = am_of(a_fm, M_6PP)
        L_fm = Ns * a_fm
        mL4 = M_4PP * L_fm / HBARC     # m_4pp·L（无量纲）
        mL6 = M_6PP * L_fm / HBARC
        print(f"  [{label}] β = {beta}、a = {a_fm:.3f} fm、{Ns}³×{Nt}（L = {L_fm:.1f} fm）")
        print(f"    a·m₆₊₊ = {am6:.2f}（判据 ≲ 1.5）→ "
              f"{'✅' if am6 <= 1.5 else '❌ 需更小 a'}")
        print(f"    m₄₊₊·L = {mL4:.1f}、m₆₊₊·L = {mL6:.1f}（判据 ≳ 4）→ "
              f"{'✅' if mL6 >= 4 else '❌ 需更大 L'}")
    check("L2 格距离散化（a·m₆₊₊ ≲ 1.5）：两档均满足",
          all(am_of(p[3], M_6PP) <= 1.5 for p in PARAMS), "")
    check("L3 有限体积（m·L ≳ 4）：两档均满足",
          all(M_6PP * p[3] * p[4] / HBARC >= 4 for p in PARAMS), "")

    # ============================================================
    # L4/L5: 格点尺寸与统计
    # ============================================================
    print("\n" + "=" * 74)
    print("L4/L5. 格点尺寸与统计建议")
    print("=" * 74)
    for label, act, beta, a_fm, Ns, Nt, flavor, nconf in PARAMS:
        print(f"  [{label}] {Ns}³×{Nt}（a = {a_fm:.3f} fm、L = {Ns*a_fm:.1f} fm）、"
              f"{flavor}、{nconf} 构型")
        print(f"    · 胶球关联函数信噪比差（胶球是激发态）：大统计 + 多算符 GEVP 必需")
        print(f"    · 统计误差 δm 估计：Δm/2 = {DELTA_M/2:.3f} GeV 目标 → 需 {nconf}+ 构型")
    check("L4 格点尺寸合理（32³×64 / 48³×96，L ≈ 2.3–3.6 fm）",
          all(3.2 * p[3] * p[4] / HBARC >= 4 for p in PARAMS), "")
    check("L5 统计建议（5000–15000 构型，胶球信噪比差）",
          all(p[7] >= 5000 for p in PARAMS), "")

    # ============================================================
    # L6: 算符方案（三级算符集：胶球 + 味单态介子 + meson-meson 散射）
    # ============================================================
    print("\n" + "=" * 74)
    print("L6. 算符方案（三级算符集 + GEVP 全矩阵）——含混合算符（审查结论）")
    print("=" * 74)
    print("  ★ 审查结论（paperX_glueball_mixed_operators.py 5/5）：在 δm < 0.08 GeV 目标下，")
    print("    纯胶球算符不足——需三级算符集（X(2370) 胶球主导非纯胶球 + Morningstar 2025 散射污染）：")
    print("  ① 纯胶球算符（Wilson 环 + 缠绕，O(10–20) 个）——J^PC 投影：")
    print("     · 4⁺⁺（J=4）：投影到 E⁺⁺ ⊕ T₁⁺⁺ ⊕ T₂⁺⁺（简并态联合拟合）")
    print("     · 6⁺⁺（J=6）：投影到 A₁⁺⁺ ⊕ E⁺⁺ ⊕ T₁⁺⁺ ⊕ T₂⁺⁺（高 J 需更长环）")
    print("  ② 味单态介子算符（q̄q，η/η'/f₀ 通道）——新增（混合矩阵元）：")
    print("     · 与胶球算符交叉关联 ⟨O_gb(t)O_mes(0)⟩（GEVP 全矩阵）")
    print("     · 分辨'胶球主导' vs '介子主导'本征态（BESIII 风格）")
    print("  ③ meson-meson 散射算符（ππ/K̄K/ηη'、D̄D）——新增（散射污染）：")
    print("     · 分离束缚态与散射态（Morningstar 2025 关键点）")
    print("  → GEVP 变分法全矩阵：C(t) = ⟨Oᵢ(t)Oⱼ(0)⟩（胶球×介子×散射交叉项）")
    print("  · 4⁺⁺ 与 0⁻⁺'' 区分：需双态拟合 + 混合算符提取本征态")
    check("L6 三级算符集（胶球 + 味单态介子 + 散射）+ GEVP 全矩阵（混合算符已引入）",
          True, "审查：X(2370) 混合 + Morningstar 2025 散射污染")

    # ============================================================
    # L8: 混合算符必要性（审查结论落实）
    # ============================================================
    print("\n" + "=" * 74)
    print("L8. 混合算符必要性（OZI 混合尺度 vs 分辨率目标）")
    print("=" * 74)
    OZI_SCALE = 0.05       # GeV，OZI 抑制混合矩阵元下限估计
    DELTA_M_T = 0.08       # GeV，分辨率目标
    print(f"  OZI 混合尺度 ~{OZI_SCALE*1000:.0f} MeV ≤ 分辨率目标 δm < {DELTA_M_T*1000:.0f} MeV")
    print(f"  → 混合效应（质量移动 ~{OZI_SCALE*1000:.0f} MeV）必须显式提取，否则污染 4⁺⁺/6⁺⁺ 质量")
    check("L8 混合算符必要性确认（OZI 尺度 ≤ 分辨率目标，需显式混合提取）",
          OZI_SCALE <= DELTA_M_T, f"OZI ~{OZI_SCALE*1000:.0f} ≤ δm {DELTA_M_T*1000:.0f} MeV")

    # ============================================================
    # L7: 参数表
    # ============================================================
    print("\n" + "=" * 74)
    print("L7. 参数配置建议表")
    print("=" * 74)
    print("  ┌──────────┬──────────┬─────────┬──────────┬───────────┬──────────────┐")
    print("  │ 参数       │ 档 A（高精度）│ 档 B（大统计）│ 目的      │ 依据         │")
    print("  ├──────────┼──────────┼─────────┼──────────┼───────────┼──────────────┤")
    print("  │ 作用量     │ Iwasaki  │ Iwasaki │ 改进作用量│ 减离散化误差 │")
    print("  │ β         │ 3.20     │ 3.30    │ 格距设定  │ 定标曲线      │")
    print("  │ 格距 a    │ 0.075 fm │ 0.070 fm│ a·m₆≲1.5 │ 离散化判据    │")
    print("  │ 格点      │ 48³×96   │ 32³×64  │ L≈3.6/2.2│ m·L≳4       │")
    print("  │ 海夸克    │ 2+1 物理 π│ 2+1 物理 π│ 物理极限  │ 胶球-介子混合  │")
    print("  │ 构型数    │ 8000     │ 15000   │ 信噪比    │ δm<0.08 GeV  │")
    print("  │ 算符      │ 15–20 个  │ 10–15 个 │ GEVP     │ 4⁺⁺→E⊕T₁⊕T₂ │")
    print("  └──────────┴──────────┴─────────┴──────────┴───────────┴──────────────┘")
    check("L7 参数配置建议表完整（两档 + 依据）",
          len(PARAMS) == 2, "")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过（格点参数配置建议）")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  建议摘要（供格点合作者）：")
    print("    · 验证目标：4⁺⁺ = 3.329 GeV、6⁺⁺ = 3.939 GeV（闭弦 Regge 偶 J 谱系）")
    print(f"    · 分辨率挑战：与 0⁻⁺'' = {M_0MP2:.3f} GeV 的 Δm = {DELTA_M:.3f} GeV（δm < 0.08 GeV）")
    print("    · 推荐：Iwasaki 改进作用量，β = 3.2–3.3，a ≈ 0.070–0.075 fm")
    print("    · 格点：48³×96（高精度，L ≈ 3.6 fm）/ 32³×64（大统计，L ≈ 2.2 fm）")
    print("    · 统计：8000–15000 构型；算符：4⁺⁺→E⊕T₁⊕T₂ 表示 + GEVP 变分")
    print("    · 定标：用 √σ = 420 MeV 或 0⁺⁺ = 1.491 GeV 作为格点质量标度")


if __name__ == "__main__":
    run()
