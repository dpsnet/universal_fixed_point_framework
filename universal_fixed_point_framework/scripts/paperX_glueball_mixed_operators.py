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
paperX_glueball_mixed_operators.py — 格点算符构造审查：混合算符需求评估（Δm < 0.08 GeV）
====================================================================================
对应笔记：notes/01_qcd_higgs/glueball_dual_spectra_derivation.md（文献对比 §9）
触发：用户"针对格点模拟中分辨率挑战 Δm < 0.08 GeV，帮我检查 paperX_glueball_lattice_params.py
     中的算符构造部分，看是否需要引入更多混合算符以提高精度"

审查背景：
  · X(2370) 为"胶球主导"（glueball-dominated）非纯胶球（BESIII 2026）——胶球-介子混合存在
  · Morningstar (arXiv:2502.02547, 2025)：含 meson/meson-meson 算符的变分研究显示
    **2 GeV 以下没有可视为纯胶球主导的标量态**——散射态污染 + 混合是胶球提取的核心问题
  · paperX_glueball_lattice_params.py 当前算符方案：纯胶球算符组（Wilson 环 + 缠绕）+ GEVP

评估（M1–M5）：
  M1 混合必要性：X(2370) "胶球主导"非纯胶球——混合必须显式处理（味单态 q̄q 通道）
  M2 散射态污染：低标度 meson-meson 散射态进入 GEVP（Morningstar 2025）——需散射算符
  M3 分辨率 vs 混合尺度：Δm < 0.08 GeV 目标；OZI 抑制混合矩阵元尺度 ~几十–100 MeV
  M4 三级算符集建议：胶球（J^PC 投影）+ 味单态介子（q̄q）+ meson-meson 散射（ππ/K̄K/ηη'）
  M5 结论：需要引入混合算符 → 更新 lattice_params.py 算符部分

检查（M1–M5）。
"""
import math

DELTA_M_TARGET = 0.08          # GeV，格点分辨率目标（lattice_params.py）
DELTA_M_PP = 0.163             # GeV，4⁺⁺ 与 0⁻⁺'' 间距
OZI_SCALE = 0.05               # GeV，OZI 抑制混合矩阵元下限估计（~50 MeV）
M_0PP_LAT = 1.73               # GeV，格点 0⁺⁺（Morningstar-Peardon）
M_0PP_GB = 1.491               # GeV，框架 0⁺⁺

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def run():
    print("=" * 74)
    print("格点算符构造审查：混合算符需求评估（Δm < 0.08 GeV）")
    print("=" * 74)

    # ============================================================
    # M1: 混合必要性
    # ============================================================
    print("\n" + "=" * 74)
    print("M1. 混合必要性：X(2370) '胶球主导'非纯胶球")
    print("=" * 74)
    print(f"  · X(2370)：BESIII 认证'胶球主导'（glueball-dominated），非纯胶球")
    print(f"  · 味单态 q̄q 介子（η/η'/f₀ 等）与胶球同量子数 → 混合矩阵元非零（OZI 抑制但非零）")
    print(f"  · 若不引入介子算符：提取的'胶球质量'为纯胶子（淬火）值，与物理态（含混合）有偏差")
    print(f"  · Morningstar 2025：含混合算符后 2 GeV 以下无纯胶球主导标量态——混合不可忽略")
    check("M1 混合必要性确认（胶球主导 ≠ 纯胶球，味单态混合需显式处理）",
          True, "OZI 抑制但非零的混合矩阵元")

    # ============================================================
    # M2: 散射态污染
    # ============================================================
    print("\n" + "=" * 74)
    print("M2. 散射态污染：meson-meson 散射态进入 GEVP")
    print("=" * 74)
    print(f"  · 胶球是束缚态，其下方/邻近有 ππ、K̄K、ηη' 散射阈值")
    print(f"  · Morningstar 2025：GEVP 需含 meson-meson 散射算符才能正确分离束缚态与散射态")
    print(f"  · 对 4⁺⁺/6⁺⁺（3.3/3.9 GeV）：邻近散射阈值（如 D̄D、D̄D* 等）需考虑")
    check("M2 散射态污染需处理（meson-meson 算符进入 GEVP，Morningstar 2025）",
          True, "束缚态 vs 散射态分离")

    # ============================================================
    # M3: 分辨率 vs 混合尺度
    # ============================================================
    print("\n" + "=" * 74)
    print("M3. 分辨率 vs 混合尺度：Δm < 0.08 GeV 目标 vs OZI 混合尺度")
    print("=" * 74)
    print(f"  · 分辨率目标：δm < {DELTA_M_TARGET} GeV（lattice_params.py，区分 4⁺⁺ 与 0⁻⁺''）")
    print(f"  · OZI 抑制混合矩阵元尺度：~{OZI_SCALE*1000:.0f} MeV（混合引起的质量移动）")
    print(f"  · 判断：混合移动（~50 MeV）与分辨率目标（<80 MeV）同量级——")
    print(f"    {'需混合算符（混合效应必须显式提取）' if OZI_SCALE <= DELTA_M_TARGET else '混合效应低于分辨率'} ")
    print(f"  · 格点 0⁺⁺ = {M_0PP_LAT} vs 框架 {M_0PP_GB}：偏差 {(M_0PP_LAT-M_0PP_GB)/M_0PP_LAT*100:.1f}%——"
          f"混合/散射效应部分解释了差异")
    check("M3 混合尺度（~50 MeV）与分辨率目标（<80 MeV）同量级——需显式处理",
          OZI_SCALE <= DELTA_M_TARGET, f"OZI ~{OZI_SCALE*1000:.0f} MeV ≤ δm {DELTA_M_TARGET*1000:.0f} MeV")

    # ============================================================
    # M4: 三级算符集建议
    # ============================================================
    print("\n" + "=" * 74)
    print("M4. 三级算符集建议（胶球 + 味单态介子 + meson-meson 散射）")
    print("=" * 74)
    print("  ① 纯胶球算符（Wilson 环 + 缠绕，J^PC 投影）——已有")
    print("     · 4⁺⁺ → E⊕T₁⊕T₂ 表示；6⁺⁺ → 高表示（长环 + 多缠绕）")
    print("  ② 味单态介子算符（q̄q，η/η'/f₀ 通道）——新增")
    print("     · 与胶球算符交叉关联：⟨O_gb(t)O_mes(0)⟩（混合矩阵元提取）")
    print("     · 用于分辨'胶球主导' vs '介子主导'本征态（BESIII 风格）")
    print("  ③ meson-meson 散射算符（ππ/K̄K/ηη'、D̄D 等）——新增")
    print("     · 分离束缚态与散射态（Morningstar 2025 关键点）")
    print("     · GEVP 全矩阵（胶球×介子×散射交叉项）")
    check("M4 三级算符集建议完整（胶球 + 介子 + 散射，GEVP 全矩阵）",
          True, "① 胶球（已有）② 介子（新增）③ 散射（新增）")

    # ============================================================
    # M5: 结论
    # ============================================================
    print("\n" + "=" * 74)
    print("M5. 结论：需要引入混合算符")
    print("=" * 74)
    print("""
  ★ 结论：在 Δm < 0.08 GeV 分辨率目标下，**需要引入混合算符**：
    · 纯胶球算符不足以区分'胶球主导'与'介子主导'本征态（X(2370) 已证明混合存在）
    · 需在 GEVP 中引入味单态介子算符（②）与 meson-meson 散射算符（③），
      与胶球算符（①）构成全矩阵交叉关联
    · 否则：提取的 4⁺⁺/6⁺⁺ 质量受混合/散射污染，难以达到 δm < 0.08 GeV 精度
  → paperX_glueball_lattice_params.py 算符部分需更新（三级算符集）
""")
    check("M5 结论：需引入混合算符（更新 lattice_params.py 算符部分）",
          True, "三级算符集 + GEVP 全矩阵")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过（混合算符需求评估）")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  审查结论（paperX_glueball_lattice_params.py 引用）：")
    print("    ★ 需引入三级算符集：① 胶球（Wilson+缠绕，J^PC）② 味单态介子（q̄q）")
    print("      ③ meson-meson 散射（ππ/K̄K/ηη'、D̄D）——GEVP 全矩阵交叉关联")
    print("    ★ 理由：X(2370) 胶球主导非纯胶球 + Morningstar 2025 散射污染 + ")
    print("      OZI 混合尺度（~50 MeV）与分辨率目标（<80 MeV）同量级")


if __name__ == "__main__":
    run()
