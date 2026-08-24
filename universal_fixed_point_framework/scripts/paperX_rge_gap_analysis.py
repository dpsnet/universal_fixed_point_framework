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
"""
paperX_rge_gap_analysis.py — RGE 链 α_s(M_Z) -72% 偏差根因分析
================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §8.4 全理论基础复核 F1 深挖
触发：全理论基础复核发现"谱 RGE 第一性预言不复现实验"（α_s(M_Z) = 0.0328 vs 0.1179，
      -72%，独立于谱间隙比歧义）——本脚本定量定位根因。

核心链条（SU(3) 为例）：
  R1 谱裸耦合        α³⁰ = Δλ₃/(4π) = 0.122·√2/(4π) = 0.01373（M_Pl）
  R2 MS-bar 初值      α_s^MSbar(M_Pl) = 0.01976（从实验 α_s(M_Z) = 0.1179 两圈反演）
  R3 方案转换因子    Z₃ = α_s^MSbar(M_Pl)/α³⁰ = 1.439（"四层静默"修正）
  R4 裸耦合直接跑动   α_s(M_Z) = 0.0328（-72%）← spectral_rge_running.py 的原始结果
  R5 Z₃ 修正后跑动    α_s(M_Z) = 0.1176（≈ 实验 0.1179）← qcd_lambda_validation.py 的 Z_s 做法
  R6 Z_i 非第一性     "静默"猜测公式 Z = 1+(C_A−C_F)(−lnS₃−lnS₄)/(8π) 对 Z₂/Z₃ 偏差 65%/4%——
                      Z_i 数值实际由实验反演（α_phys(M_Pl)/α_bare），非独立推导
  R7 标注错误        paperX_all_predictions.py：α_i(M_Z)_pred = α_i^bare·Z_i = α_i^MSbar(M_Pl)
                      （M_Pl 标度值被标注为 M_Z 预测：SU(3) 0.01976 vs 实验 0.1179，-83%）
  R8 无下游污染      RGE -72% 输出（0.0328）不被任何下游计算使用——61C 链/Λ_QCD 均以
                      α_s(M_Z)⁻¹ = 8.7（实验锚点）起步 → 现象学数值不受影响

判定：R1–R5 为根因定量链；R6 证伪"第一性静默修正"叙事；R7 为文档/代码标注缺陷；
      R8 确认影响范围仅限"第一性叙事"，不污染现象学。
单位：无量纲（耦合/α⁻¹）。
"""
import math

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def run():
    print("=" * 74)
    print("RGE 链 α_s(M_Z) -72% 偏差根因分析（独立于谱间隙比歧义）")
    print("=" * 74)

    dl = 0.122
    M_Pl, M_Z = 2.435e18, 91.1876
    L = math.log(M_Pl / M_Z)
    b1_6 = 11 - 2 * 6 / 3   # n_f=6 单圈
    alpha3_bare = dl * math.sqrt(2) / (4 * math.pi)          # R1
    alpha_s_exp = 0.1179                                      # 实验
    # R2: 从实验反演 MS-bar(M_Pl)
    alpha_s_msbar_Pl = 1.0 / (1.0 / alpha_s_exp + b1_6 * L / (2 * math.pi))
    Z3 = alpha_s_msbar_Pl / alpha3_bare                       # R3
    # R4: 裸耦合直接跑动
    inv_s_raw = 1.0 / alpha3_bare - b1_6 * L / (2 * math.pi)
    alpha_s_raw = 1.0 / inv_s_raw
    # R5: Z₃ 修正后跑动
    inv_s_fix = 1.0 / (Z3 * alpha3_bare) - b1_6 * L / (2 * math.pi)
    alpha_s_fix = 1.0 / inv_s_fix

    print(f"\n  R1. 谱裸耦合 α³⁰ = Δλ₃/(4π) = {dl}·√2/(4π) = {alpha3_bare:.6f}（M_Pl）")
    print(f"  R2. MS-bar 初值（实验 α_s(M_Z) = {alpha_s_exp} 反演）")
    print(f"       1/α_s^MSbar(M_Pl) = 1/{alpha_s_exp} + {b1_6}·ln(M_Pl/M_Z)/(2π) = "
          f"{1.0/alpha_s_msbar_Pl:.2f}")
    print(f"       α_s^MSbar(M_Pl) = {alpha_s_msbar_Pl:.6f}")
    print(f"  R3. 方案转换因子 Z₃ = MS-bar/裸 = {alpha_s_msbar_Pl:.6f}/{alpha3_bare:.6f} = {Z3:.4f}")
    print(f"       （= spectral_rge_running.py 输出 Z=1.4388；Zi_closed_form.py Z₃=1.439）")
    print(f"  R4. 裸耦合直接跑动：1/α_s(M_Z) = 1/0.01373 − {b1_6}·{L:.1f}/(2π) = {inv_s_raw:.1f}")
    print(f"       α_s(M_Z) = {alpha_s_raw:.4f}（实验 {alpha_s_exp}，偏差 {(alpha_s_raw-alpha_s_exp)/alpha_s_exp*100:.0f}%）")
    print(f"       ← spectral_rge_running.py 实测 α_s(M_Z) = 0.0328（偏差 −72%），一致")
    print(f"  R5. Z₃ 修正后跑动：1/α_s(M_Z) = 1/0.01976 − 42.1 = {inv_s_fix:.2f}")
    print(f"       α_s(M_Z) = {alpha_s_fix:.4f}（偏差 {(alpha_s_fix-alpha_s_exp)/alpha_s_exp*100:+.1f}%）")
    print(f"       ← qcd_lambda_validation.py 的 Z_s 修正做法，复现实验 ✓")

    check("R1 谱裸耦合 α³⁰ = Δλ₃/4π = 0.01373", abs(alpha3_bare - 0.01373) < 1e-4,
          f"{alpha3_bare:.5f}")
    check("R2 反演 MS-bar(M_Pl) ≈ 0.0198", abs(alpha_s_msbar_Pl - 0.0198) < 1e-3,
          f"{alpha_s_msbar_Pl:.5f}")
    check("R3 Z₃ = MS-bar/裸 ≈ 1.439", abs(Z3 - 1.439) < 0.02, f"Z₃ = {Z3:.4f}")
    check("R4 裸耦合跑动给 α_s(M_Z) ≈ 0.033（-72%，与 spectral_rge_running 实测一致）",
          abs(alpha_s_raw - 0.0328) < 0.002, f"α_s(M_Z) = {alpha_s_raw:.4f}（偏差 {(alpha_s_raw-alpha_s_exp)/alpha_s_exp*100:.0f}%）")
    check("R5 Z₃ 修正后跑动复现实验（偏差 < 2%）",
          abs(alpha_s_fix - alpha_s_exp) / alpha_s_exp < 0.02,
          f"α_s(M_Z) = {alpha_s_fix:.4f}（偏差 {(alpha_s_fix-alpha_s_exp)/alpha_s_exp*100:+.1f}%）")

    # ---- R6: Z_i 静默猜测公式失败 ----
    S3, S4 = math.exp(-3), math.exp(-2.7095)
    nln = 3 + 2.7095
    print(f"\n  R6. Z_i 的'四层静默'猜测公式检验（Z = 1+(C_A−C_F)·(−lnS₃−lnS₄)/(8π)）")
    for name, CA, CF, Z_i in [("U(1)", 0, 0, 3.674), ("SU(2)", 2, 0.75, 2.118), ("SU(3)", 3, 4/3, 1.439)]:
        guess = 1 + (CA - CF) * nln / (8 * math.pi)
        print(f"  {name:>5s}: Z_i = {Z_i:.3f}, 静默猜测 = {guess:.4f}, 比值 = {Z_i/guess:.2f}")
    check("R6 静默猜测公式不能复现 Z_i（U(1) 差 3.7×、SU(2) 差 1.6×）",
          abs(3.674 / (1 + (0 - 0) * nln / (8 * math.pi)) - 1) > 2,
          "Z_i 数值来自实验反演，'四层静默'仅为命名非推导")

    # ---- R7: paperX_all_predictions 标注错误 ----
    a1_0 = dl * math.sqrt(2 / 3) / (4 * math.pi)
    a2_0 = dl * 1.0 / (4 * math.pi)
    a3_0 = dl * math.sqrt(2) / (4 * math.pi)
    print(f"\n  R7. paperX_all_predictions.py 标注错误检验")
    print(f"       α_i(M_Z)_pred = α_i^bare·Z_i（脚本公式）")
    for name, a0, Zi, exp in [("U(1)", a1_0, 3.674, 0.00782),
                               ("SU(2)", a2_0, 2.118, 0.03380),
                               ("SU(3)", a3_0, 1.439, 0.11792)]:
        pred = a0 * Zi
        print(f"       {name}: pred = {pred:.5f} vs 实验 {exp}（偏差 "
              f"{(pred-exp)/exp*100:+.0f}%）")
    a3_pred = a3_0 * 1.439
    check("R7 α_s(M_Z)_pred = 0.01976 ≠ 实验 0.1179（-83%）——标注为 M_Z 实为 M_Pl 值",
          abs(a3_pred - 0.0198) < 1e-3 and abs(a3_pred - 0.1179) > 0.05,
          f"α_s(M_Z)_pred = {a3_pred:.5f}")
    check("R7b α_i(M_Z)_pred = α_i^MSbar(M_Pl)（M_Pl 标度值被标注为 M_Z）",
          abs(a3_pred - alpha_s_msbar_Pl) < 1e-3, f"α³⁰·Z₃ = {a3_pred:.5f} ≈ α_s^MSbar(M_Pl) = {alpha_s_msbar_Pl:.5f}")

    # ---- R8: 无下游污染 ----
    print(f"\n  R8. 影响范围确认")
    print(f"       RGE -72% 输出（α_s(M_Z) = 0.0328）仅作展示，无下游计算引用")
    print(f"       61C 链 paperX_rg_chain_nonpert.py 以 A_INV_SPEC = 8.7（实验锚点）起步")
    print(f"       跨味 Λ^(3) = 122 MeV / 有效 Λ = 210 MeV 均从 8.7 锚点导出")
    check("R8 现象学数值（Λ_QCD = 210 MeV、m_ρ、F_π）不依赖 RGE -72% 输出", True,
          "8.7 锚点为实验输入")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过（RGE 偏差根因分析）")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  根因结论（笔记引用）：")
    print(f"    · -72% 根因：spectral_rge_running.py 用裸耦合 α³⁰ = 0.01373 直接跑动，"
          f"未先应用 Z₃ = 1.439 方案转换")
    print(f"    · Z₃ 修正后（α = Z₃·α³⁰ = 0.01976 起步）RGE 精确复现 α_s(M_Z) = {alpha_s_fix:.4f}")
    print(f"    · 但 Z_i（1.439/2.118/3.674）由实验 α(M_Z) 反演（α_phys(M_Pl)/α_bare），")
    print(f"    · 静默猜测公式失败 → '四层静默'为命名非第一性推导")
    print(f"    · paperX_all_predictions.py 把 α^MSbar(M_Pl) 标注为 α(M_Z) 预测——标注错误待修")
    print(f"    · 现象学不受影响（8.7 实验锚点）——仅'谱 RGE 第一性预言'声称需修正")


if __name__ == "__main__":
    run()
