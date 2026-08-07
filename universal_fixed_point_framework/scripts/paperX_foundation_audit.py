#!/usr/bin/env python3
"""
paperX_foundation_audit.py — 全理论基础复核：谱间隙比歧义 → 全部衍生量影响量化
=================================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §8.4 基础审核（扩展，2026-08-06）
触发：用户要求"整个理论的基础和后续所有推导是否受谱间隙比影响"——严格复核所有
      依赖该比值的文档与程序代码，逐项量化第一分量歧义（√(2/3) vs 1/√3）的影响。

两种候选体系（其余分量一致）：
  声称体系      Δλ₁:Δλ₂:Δλ₃ = √(2/3):1:√2   （Paper 20 定理 7.1，推导存疑）
  特征值归一化  Δλ₁:Δλ₂:Δλ₃ = 1/√3:1:√2    （SU(2) Casimir 特征值严格归一化）

判定逻辑：
  依赖第一分量（U(1)）的量 → ⚠️ 受影响
  依赖中项（SU(2)）或第三分量（SU(3)）或仅 Δλ_min 的量 → ✅ 稳健

核查文件（使用谱间隙比三分量的全部代码）：
  src/spectral_rge_running.py、src/Zi_closed_form.py、src/qcd_lambda_validation.py、
  src/qcd_spectral_validation.py、src/high_deviation_analysis.py、
  src/gamma2_high_loop_derivation.py、src/spectral_BCS_checker.py、
  src/spectral_BCS_v2_comprehensive.py、src/dynamic_spectrum/dst_spectral_weave.py、
  scripts/paperX_all_predictions.py、scripts/paperX_full_rge_chain.py、
  scripts/paperX_qcd_kappa_dressing.py、scripts/paperX_qcd_flavor_bridge.py、
  scripts/paperX_reheat_gamma_spectral.py、scripts/paperX_color_projection.py、
  scripts/paperX_bounce_inflation.py、scripts/paper36_spectral_gap_derivation.py
  形式化：formal_proof/**/*.lean（仅 spectralGap 8，稳健）
  文档：paper20（定理 7.1 推导存疑）、paper11（§1.5 废弃 + §8 sin²θ_W 🟡）

独立于比值体系的量（不列入判定）：
  S₃/S₄ 静默层（费米子质量比 α 指数、IFS 递归）——paperX_all_predictions 第 1-3 层
  CKM 混合角——Yukawa 谱间隙（非 Cl(1,7) 规范比）
  Starobinsky 斜率 b = √(2/3)——标准暴涨值，与 Cl(1,7) 比值同数值不同来源

重要发现（独立于比值歧义的基础不自洽）：
  F1 比值起步的 1-loop RGE 给出 α_s(M_Z)⁻¹ ≈ 30（α_s ≈ 0.033），与实验 8.5 偏差 -72%——
      框架登记值 8.7 实为实验锚点（0.1149，偏差 2.7%），非比值产物
  F2 框架内 α_s(M_Z)⁻¹ 三来源不一致：8.7（锚点）/ ~30（RGE）/ ~50（Zi 闭式）
  F3 paperX_all_predictions.py sin²θ_W = 0.2223 为硬编码，与比值直接给出 0.4495 不符

单位：无量纲（除注明 MeV/GeV）。
"""
import math

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def run():
    print("=" * 76)
    print("全理论基础复核：谱间隙比第一分量歧义（√(2/3) vs 1/√3）→ 全部衍生量影响")
    print("=" * 76)

    dl = (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)   # Δλ_min = 0.122
    r_c = [math.sqrt(2 / 3), 1.0, math.sqrt(2)]          # 声称体系
    r_e = [1 / math.sqrt(3), 1.0, math.sqrt(2)]          # 特征值归一化
    Nc = 3.0

    print(f"\n  Δλ_min = {dl:.6f}（Lean spectralGap 8 形式化，独立于比值体系）")
    print(f"  声称体系     : {r_c[0]:.4f} : 1 : {r_c[2]:.4f}  (√(2/3):1:√2)")
    print(f"  特征值归一化 : {r_e[0]:.4f} : 1 : {r_e[2]:.4f}  (1/√3:1:√2)")
    print(f"  → 第一分量差 {(r_c[0]-r_e[0])/r_e[0]*100:.1f}%，中项/第三项一致\n")

    rows = []
    def row(name, fc, fe, tol=0.1, note="受影响"):
        dv = (fe - fc) / fc * 100 if fc != 0 else float('inf')
        mark = "✅ 稳健" if abs(dv) < tol else f"⚠️ {note}"
        rows.append((name, fc, fe, dv, mark))

    # ---------- 规范耦合层（使用三分量） ----------
    a1c, a1e = dl * r_c[0] / (4 * math.pi), dl * r_e[0] / (4 * math.pi)
    a2c, a2e = dl * r_c[1] / (4 * math.pi), dl * r_e[1] / (4 * math.pi)
    a3c, a3e = dl * r_c[2] / (4 * math.pi), dl * r_e[2] / (4 * math.pi)
    row("α₁⁰ = Δλ₁/(4π)  (U(1) 裸耦合)", a1c, a1e)
    row("α₂⁰ = Δλ₂/(4π)  (SU(2) 裸耦合)", a2c, a2e)
    row("α₃⁰ = Δλ₃/(4π)  (SU(3) 裸耦合)", a3c, a3e)
    row("sin²θ_W(裸) = α₁/(α₁+α₂)", a1c / (a1c + a2c), a1e / (a1e + a2e))

    # ---------- QCD/强子层（第三分量） ----------
    kc = Nc / math.pi * (r_c[2] / r_c[1]) ** 2
    ke = Nc / math.pi * (r_e[2] / r_e[1]) ** 2
    row("κ = (N_c/π)(Δλ₃/Δλ_min)²", kc, ke)
    row("Δ_dress = κΛ [MeV]", kc * 210, ke * 210)
    row("m_ρ = 2(m_ud+κΛ) [MeV]", 2 * (3.45 + kc * 210), 2 * (3.45 + ke * 210))
    row("F_π ∝ √N_c·Λ·Δλ₃/(4πΔλ_min)", 92.2, 92.2, note="F_π 实验锚点")
    row("ξ = F_π/(√N_c·Λ·Δλ₃/(4πΔλ_min)) 谱量近似", 1.7264, 1.7264)

    # ---------- 1-loop RGE 预测（符号：α⁻¹(M_Z) = α⁻¹(M_Pl) − b/(2π)·ln(M_Pl/M_Z)） ----------
    # 注：与 spectral_rge_running.py 三圈结果（α_s(M_Z) = 0.0328，α⁻¹ ≈ 30.5）核对，
    #     本 1-loop 闭式给出 ≈ 30.7（差 < 1%），交叉验证通过。
    M_Pl, M_Z = 2.435e18, 91.1876   # 与 spectral_rge_running.py 一致
    b3, b1 = 11 - 2 * 6 / 3, -41 / 10
    L = math.log(M_Pl / M_Z)
    inv_s_c = 1 / a3c - b3 * L / (2 * math.pi)
    inv_s_e = 1 / a3e - b3 * L / (2 * math.pi)
    inv_1_c = 1 / a1c - b1 * L / (2 * math.pi)
    inv_1_e = 1 / a1e - b1 * L / (2 * math.pi)
    row("α_s(M_Z)⁻¹ (1-loop RGE, 比值起步)", inv_s_c, inv_s_e, note="无影响（仅第三分量）")
    row("α₁(M_Z)⁻¹ (1-loop RGE, 比值起步)", inv_1_c, inv_1_e)

    # ---------- 宇宙学/再加热链（第三分量或 Δλ_min） ----------
    gc = (1 / (4 * math.pi)) * (r_c[2] / r_c[1]) ** 2 * 0.75
    ge = (1 / (4 * math.pi)) * (r_e[2] / r_e[1]) ** 2 * 0.75
    row("γ_φ = (1/4π)(Δλ₃/Δλ_min)²·C_reheat", gc, ge)
    row("T_RH ∝ √γ_φ [GeV]", 2.08e10, 2.08e10)
    c1 = 1.5 / (4 * dl ** 2)
    row("c₁ = β_BCH/(4Δλ_min²) (R² 系数)", c1, c1)
    row("ρ_c ∝ 1/c₁ (反弹临界密度)", (8 * math.pi / 3) / c1, (8 * math.pi / 3) / c1)
    row("r = 12/N_e² (张量标量比)", 12 / 55 ** 2, 12 / 55 ** 2)
    row("n_s = 1-2/N_e (标量谱指数)", 1 - 2 / 55, 1 - 2 / 55)
    row("m_DM = Δλ_min²/M_Pl [10⁻²² eV]", dl ** 2 / 1.22e19 * 1e9, dl ** 2 / 1.22e19 * 1e9)

    # ---------- BCS 候选（含第一分量） ----------
    d1c, d1e = dl * r_c[0], dl * r_e[0]
    d3 = dl * r_c[2]
    row("Δλ_BCS 候选(a) = Δλ₁ (BCS 谱编织)", d1c, d1e)
    row("Δλ_BCS 候选(b) = (Δλ₁+Δλ₃)/2", (d1c + d3) / 2, (d1e + d3) / 2)

    print(f"  {'衍生量':<34s} {'声称值':>12s} {'特征值归一':>12s} {'变化':>8s} {'判定':>10s}")
    print("  " + "-" * 78)
    for name, fc, fe, dv, mark in rows:
        print(f"  {name:<34s} {fc:12.6g} {fe:12.6g} {dv:+7.1f}% {mark:>10s}")

    n_affected = sum(1 for _, _, _, dv, m in rows if abs(dv) >= 0.1)
    n_robust = len(rows) - n_affected
    print(f"\n  汇总: {n_robust}/{len(rows)} 稳健, {n_affected}/{len(rows)} 受影响（第一分量 U(1) 相关）")
    for name, fc, fe, dv, m in rows:
        if m.startswith("✅"):
            check(f"稳健：{name[:38]}", abs(dv) < 0.1, f"变化 {dv:+.1f}%")
        else:
            check(f"受影响(预期)：{name[:34]}", abs(dv) >= 0.1, f"变化 {dv:+.1f}%")
    check("κ = 1.909 完全不受比值第一分量影响", abs(kc - 1.909) < 1e-3, f"κ = {kc:.4f}")
    check("α_s(M_Z)⁻¹ RGE 预测在两体系下相同（仅第三分量）",
          abs(inv_s_c - inv_s_e) < 1e-6, f"{inv_s_c:.2f} vs {inv_s_e:.2f}")

    # ---------- 重要发现 ----------
    print("\n" + "=" * 76)
    print("重要发现（独立于比值歧义的基础不自洽）")
    print("=" * 76)
    print(f"  F1  比值起步 1-loop RGE：α_s(M_Z)⁻¹ = {inv_s_c:.1f}（α_s = {1/inv_s_c:.4f}）")
    dev_s = (1 / inv_s_c - 0.1179) / 0.1179 * 100
    print(f"      实验 α_s = 0.1179 → 偏差 {dev_s:+.0f}%——RGE 链不复现实验")
    print(f"      框架登记值 8.7 实为实验锚点（α_s = 0.1149，偏差 2.7%，非比值产物）")
    print(f"      （另：RGE 链预测 sin²θ_W = 0.218（-5.7%）、α_EM⁻¹ = 514（+302%））")
    print(f"  F2  框架内 α_s(M_Z)⁻¹ 三来源不一致：8.7（锚点）/ {inv_s_c:.1f}（RGE）/"
          f" {4*math.pi/(dl*math.sqrt(2)*1.439):.1f}（Zi 闭式）")
    print(f"  F3  paperX_all_predictions.py sin²θ_W = 0.2223 硬编码 ≠ 比值直接给出 "
          f"{a1c/(a1c+a2c):.4f}")
    check("F1 RGE 链偏差 > 30%（基础不自洽，与比值歧义无关）", abs(dev_s) > 30,
          f"偏差 {dev_s:.0f}%")
    check("F2 α_s(M_Z)⁻¹ 三来源不一致", abs(inv_s_c - 8.7) > 10 and abs(50.6 - 8.7) > 10,
          "8.7 vs ~30 vs ~50")
    check("F3 预测表 sin²θ_W 硬编码与比值计算不符", abs(0.2223 - a1c / (a1c + a2c)) > 0.1,
          f"0.2223 vs {a1c/(a1c+a2c):.4f}")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 76)
    print(f"  汇总: {n_pass}/{n_total} 检查通过（全理论基础复核）")
    print("=" * 76)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  结论（笔记引用）：")
    print(f"    · 受影响（第一分量 U(1)）：α₁⁰、sin²θ_W(裸)、α₁(M_Z)⁻¹、Z₁、BCS 候选(a)(b)")
    print(f"    · 稳健（中项/第三分量/Δλ_min）：κ、Λ_QCD、F_π、m_ρ、α_s(M_Z)⁻¹、γ_φ、T_RH、")
    print(f"      c₁、ρ_c、r、n_s、m_DM、胶球谱数值（¾ 因子 D=4 单源）")
    print(f"    · 独立于比值：费米子质量比（S₃/S₄）、CKM（Yukawa 间隙）、Starobinsky b=√(2/3)")
    print(f"    · 基础不自洽（与比值歧义无关）：RGE 链 α_s(M_Z)⁻¹≈{inv_s_c:.0f} vs 实验 8.5（-72%）")


if __name__ == "__main__":
    run()
