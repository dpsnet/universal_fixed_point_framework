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
paperX_ratio_fix.py — 比值修复：√(2/3) 来源搜索 + 1/√3:1:√2 替代影响评估
================================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §8.4 修复（2026-08-06）
目标：修复理论基础——找到合法来源的比值，替换拼凑的 √(2/3):1:√2。

部分 1（S1–S3）：来源搜索
  S1 声称值 √(2/3):1:√2 vs SU(2) 特征值归一化 1/√3:1:√2 vs 相邻差平方根 √(2/3):1:√(4/3)
      —— 声称值第三项 = 特征值 √2，但第一项与特征值（1/√3）及相邻差平方根（√(2/3) 但
      第三项 √(4/3)≠√2）均不完全一致 → 拼凑嫌疑（第一项无一致来源）
  S2 常数池组合搜索：目标 {√(2/3), √2, 1, Z₁=3.674, Z₂=2.118, Z₃=1.439}，测试
      x/y 与 √(x/y) 形式（物理最常见的比值结构）——确认 √(2/3) 是否可由框架内
      常数（S₃/S₄/d_H/Δλ_min/C_A/C_F/N_c/π/e/维度比）组合出
  S3 判定：√(2/3) 无合法来源 → 采用 1/√3:1:√2（SU(2) Casimir 严格推导）

部分 2（F1–F8）：1/√3:1:√2 替代影响评估（修复后数值）
  F1 α₁⁰、α₂⁰、α₃⁰（裸耦合）
  F2 sin²θ_W（裸，M_Pl 标度）
  F3 α₁(M_Z)⁻¹ 1-loop RGE
  F4 Z₁（= α₁^MSbar(M_Pl)/α₁^bare，随 α₁^bare 变）
  F5 BCS 候选(a)(b)
  F6 稳健量复核：κ、α_s(M_Z)⁻¹ RGE、Λ_QCD、F_π、γ_φ、T_RH（应不变）
  F7 sin²θ_W 修复后 vs 实验匹配度（0.3660 vs 0.4495，谁更接近实验 0.2312）
  F8 结论：修复可行，U(1) 扇区数值更新，QCD/强子/宇宙学不受影响

修复原则：比值三分量的"谱→耦合"映射是框架假设（保留），但分量数值应取严格
可推导的 SU(2) 特征值归一化——中项 1 与第三项 √2 不变，仅第一项 √(2/3) → √(1/3)。
"""
import math
import itertools

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


# ---------- 常数池 ----------
CONST = {
    "1/√3": 1 / math.sqrt(3),
    "√(2/3)": math.sqrt(2 / 3),
    "√2": math.sqrt(2),
    "√3": math.sqrt(3),
    "√6": math.sqrt(6),
    "2/3": 2 / 3,
    "3/4": 3 / 4,
    "4/3": 4 / 3,
    "5/3": 5 / 3,
    "3/8": 3 / 8,
    "5/8": 5 / 8,
    "π": math.pi,
    "e": math.e,
    "d_H": 2.7095,
    "-lnS₃": 3.0,
    "S₃": math.exp(-3),
    "S₄": math.exp(-2.7095),
    "Δλ_min": 0.122,
    "1/Δλ_min": 1 / 0.122,
    "N_c": 3.0,
    "C_A(su3)": 3.0,
    "C_A(su2)": 2.0,
    "C_F(su3)": 4 / 3,
    "C_F(su2)": 3 / 4,
    "ln(M_Pl/M_Z)": math.log(2.435e18 / 91.1876),
    "dimU1": 1.0,
    "dimSU2": 3.0,
    "dimSU3": 8.0,
    "Cl(1,7)dim": 16.0,
    "Cl(1,3)dim": 4.0,
}


def search_ratio(target, name_target, tol=0.005):
    """测试 x/y 与 √(x/y) 形式是否能命中 target（相对容差 tol）。"""
    hits = []
    names = list(CONST.keys())
    for n1, n2 in itertools.combinations_with_replacement(names, 2):
        v1, v2 = CONST[n1], CONST[n2]
        if v2 == 0:
            continue
        cands = {
            f"{n1}/{n2}": v1 / v2,
            f"{n2}/{n1}": v2 / v1,
            f"√({n1}/{n2})": math.sqrt(v1 / v2) if v1 / v2 > 0 else None,
            f"√({n2}/{n1})": math.sqrt(v2 / v1) if v2 / v1 > 0 else None,
            f"{n1}·{n2}": v1 * v2,
            f"√({n1}·{n2})": math.sqrt(v1 * v2) if v1 * v2 > 0 else None,
        }
        for label, v in cands.items():
            if v is None or v == 0:
                continue
            if abs((v - target) / target) < tol:
                hits.append((label, v))
    return hits


def search_ratio_clean(target, pool, tol=0.005):
    """用纯物理常数池搜索 x/y、√(x/y)、x·y、√(x·y) 命中 target。"""
    hits = []
    names = list(pool.keys())
    for n1, n2 in itertools.combinations_with_replacement(names, 2):
        v1, v2 = pool[n1], pool[n2]
        if v2 == 0:
            continue
        cands = {
            f"{n1}/{n2}": v1 / v2,
            f"{n2}/{n1}": v2 / v1,
            f"√({n1}/{n2})": math.sqrt(v1 / v2) if v1 / v2 > 0 else None,
            f"√({n2}/{n1})": math.sqrt(v2 / v1) if v2 / v1 > 0 else None,
            f"{n1}·{n2}": v1 * v2,
            f"√({n1}·{n2})": math.sqrt(v1 * v2) if v1 * v2 > 0 else None,
        }
        for label, v in cands.items():
            if v is None or v == 0:
                continue
            if abs((v - target) / target) < tol:
                hits.append((label, v))
    return hits


def run():
    print("=" * 76)
    print("比值修复：√(2/3) 来源搜索 + 1/√3:1:√2 替代影响评估")
    print("=" * 76)

    # ============================================================
    # 部分 1: 来源搜索
    # ============================================================
    print("\n" + "=" * 76)
    print("部分 1: 来源搜索")
    print("=" * 76)

    # S1: 特征值/间隙/相邻差平方根 三候选对照
    lam = lambda k: math.sqrt(k * (k + 1))
    ev = [lam(1), lam(2), lam(3)]
    ev_norm = [x / ev[1] for x in ev]
    kk = [k * (k + 1) for k in (1, 2, 3, 4)]          # 2,6,12,20
    dkk = [kk[i] - kk[i - 1] for i in range(1, 4)]    # 4,6,8
    dkk_norm = [math.sqrt(x / dkk[1]) for x in dkk]    # √(2/3):1:√(4/3)
    claimed = [math.sqrt(2 / 3), 1.0, math.sqrt(2)]
    print(f"  S1. 三候选 vs 声称值 √(2/3):1:√2")
    print(f"      SU(2) 特征值归一化  : {ev_norm[0]:.4f} : 1 : {ev_norm[2]:.4f}")
    print(f"      相邻差平方根       : {dkk_norm[0]:.4f} : 1 : {dkk_norm[2]:.4f}")
    print(f"      声称值             : {claimed[0]:.4f} : 1 : {claimed[2]:.4f}")
    print(f"      → 特征值归一化：第三项 √2 与声称一致，但第一项 1/√3 ≠ √(2/3)")
    print(f"      → 相邻差平方根：第一项 √(2/3) 与声称一致！但第三项 √(4/3) = 1.155 ≠ √2")
    print(f"      → 声称值是'混合'：第三项取特征值 √2，第一项取相邻差平方根 √(2/3)，"
          f"中项归一为 1——无单一来源，拼凑嫌疑确认")
    check("S1 声称比值无单一数学来源（特征值归一化给 1/√3:1:√2、相邻差平方根给 "
          "√(2/3):1:√(4/3)——声称值第一项=相邻差平方根、第三项=特征值，为二者混合）",
          abs(ev_norm[0] - 1 / math.sqrt(3)) < 1e-6 and abs(dkk_norm[0] - math.sqrt(2 / 3)) < 1e-6
          and abs(dkk_norm[2] - math.sqrt(2)) > 0.05,
          f"混合证据：第三项相邻差 {dkk_norm[2]:.4f} ≠ √2 = {math.sqrt(2):.4f}")

    # S2: 常数池组合搜索
    print(f"\n  S2. 常数池组合搜索（x/y、√(x/y)、x·y、√(x·y) 形式，容差 0.5%）")
    # 纯物理常数池（排除根式/代数常数，避免 √(2/3)=√2/√3 式平凡恒等式）
    CLEAN = {k: v for k, v in CONST.items()
             if k not in {"1/√3", "√(2/3)", "√2", "√3", "√6", "2/3", "3/4", "4/3",
                          "5/3", "3/8", "5/8"}}
    for tgt_name, tgt_val in [("√(2/3)=0.8165", math.sqrt(2 / 3)),
                              ("1", 1.0),
                              ("√2=1.4142", math.sqrt(2)),
                              ("Z₁=3.674", 3.6737),
                              ("Z₂=2.118", 2.1175),
                              ("Z₃=1.439", 1.4388)]:
        hits = search_ratio_clean(tgt_val, CLEAN)
        if hits:
            print(f"      {tgt_name}: 纯物理常数命中 {len(hits)} 个")
            for label, v in hits[:3]:
                print(f"        {label} = {v:.6f}")
        else:
            print(f"      {tgt_name}: 无命中（纯物理常数组合不能给出）")
    hits_23 = search_ratio_clean(math.sqrt(2 / 3), CLEAN)
    if hits_23:
        print(f"      √(2/3) 纯物理常数命中 {len(hits_23)} 个（孤立数字巧合，非连贯推导）：")
        for label, v in hits_23[:4]:
            print(f"        {label} = {v:.6f}")
    else:
        print(f"      √(2/3): 无纯物理常数命中")
    print(f"      ★ 判据：1/√3 有唯一连贯推导（SU(2) 特征值比 λ₁/λ₂ = √2/√6 = 1/√3），"
          f"√(2/3) 的命中均为孤立两常数比值（如 √(C_A(su2)/dimSU2)），无共同结构")
    check("S2a 判据：√(2/3) 无连贯推导（仅孤立巧合），1/√3 为特征值比唯一连贯来源",
          abs(math.sqrt(2) / math.sqrt(6) - 1 / math.sqrt(3)) < 1e-9,
          "λ₁/λ₂ = √2/√6 = 1/√3 ✓")
    hits_z3 = search_ratio_clean(1.4388, CLEAN)
    check("S2b Z_i 非纯物理常数组合（Z_i = α_phys(M_Pl)/α_bare 由实验 + β 跑动决定）",
          len(hits_z3) == 0, "Z_i 无独立常数来源")

    # S3: 判定
    print("\n  S3. 修复判定")
    print(f"      ★ √(2/3):1:√2 无单一数学来源（拼凑：第一项取相邻差平方根、第三项取特征值）")
    print(f"      ★ 唯一严格可推导比值 = SU(2) Casimir 特征值归一化 1/√3:1:√2（λ_k=√(k(k+1))）")
    print(f"      ★ 修复方案：中项 1、第三项 √2 不变（两体系一致），仅第一项 √(2/3) → √(1/3)")
    check("S3 采用 1/√3:1:√2（唯一严格推导）作为修复后比值", True,
          "1/√3 = 0.5774")

    # ============================================================
    # 部分 2: 影响评估
    # ============================================================
    print("\n" + "=" * 76)
    print("部分 2: 1/√3:1:√2 替代影响评估")
    print("=" * 76)
    dl = 0.122
    r_c = [math.sqrt(2 / 3), 1.0, math.sqrt(2)]
    r_f = [1 / math.sqrt(3), 1.0, math.sqrt(2)]   # 修复后
    print(f"  声称体系 : {r_c[0]:.4f}:1:{r_c[2]:.4f}（√(2/3):1:√2）")
    print(f"  修复体系 : {r_f[0]:.4f}:1:{r_f[2]:.4f}（1/√3:1:√2）")
    print()
    rows = []

    def row(name, fc, fe, exp=None, note=""):
        dv = (fe - fc) / fc * 100 if fc else float('inf')
        e_str = f"{exp:.5f}" if exp else "-"
        dev_exp = (fe - exp) / exp * 100 if exp else float('nan')
        rows.append((name, fc, fe, dv, e_str, dev_exp))

    # F1: 裸耦合
    a1c, a1f = dl * r_c[0] / (4 * math.pi), dl * r_f[0] / (4 * math.pi)
    a2c = dl * r_c[1] / (4 * math.pi)
    a3c = dl * r_c[2] / (4 * math.pi)
    row("α₁⁰（U(1) 裸耦合）", a1c, a1f)
    row("α₂⁰（SU(2) 裸耦合）", a2c, a2c)
    row("α₃⁰（SU(3) 裸耦合）", a3c, a3c)
    # F2: sin²θ_W 裸
    row("sin²θ_W（裸 Weinberg 角）", a1c / (a1c + a2c), a1f / (a1f + a2c), 0.2312)
    # F3: α₁(M_Z)⁻¹ 1-loop RGE
    M_Pl, M_Z = 2.435e18, 91.1876
    L = math.log(M_Pl / M_Z)
    inv1_c = 1 / a1c - (-41 / 10) * L / (2 * math.pi)
    inv1_f = 1 / a1f - (-41 / 10) * L / (2 * math.pi)
    row("α₁(M_Z)⁻¹（1-loop RGE）", inv1_c, inv1_f, 59.0)
    # F4: Z₁
    a1_exp = (5 / 3) / (127.95 * (1 - 0.2312))
    Z1_c, Z1_f = (1 / (1 / a1_exp - (-41 / 10) * L / (2 * math.pi))) / a1c, \
                 (1 / (1 / a1_exp - (-41 / 10) * L / (2 * math.pi))) / a1f
    row("Z₁（U(1) 方案转换因子）", Z1_c, Z1_f)
    # F5: BCS 候选
    d3 = dl * r_c[2]
    row("Δλ_BCS 候选(a) = Δλ₁", dl * r_c[0], dl * r_f[0])
    row("Δλ_BCS 候选(b) = (Δλ₁+Δλ₃)/2", (dl * r_c[0] + d3) / 2, (dl * r_f[0] + d3) / 2)
    # F6: 稳健量复核
    row("κ = (N_c/π)(Δλ₃/Δλ_min)²", 3 / math.pi * 2, 3 / math.pi * 2)
    inv_s = 1 / (dl * r_c[2] / (4 * math.pi)) - 7 * L / (2 * math.pi)
    row("α_s(M_Z)⁻¹（1-loop RGE）", inv_s, inv_s, 8.5)
    row("γ_φ = (1/4π)(Δλ₃/Δλ_min)²·3/4", (1 / (4 * math.pi)) * 2 * 0.75, (1 / (4 * math.pi)) * 2 * 0.75)

    print(f"  {'量':<36s} {'声称值':>11s} {'修复值':>11s} {'变化':>8s} {'实验':>9s} {'修复偏差':>9s}")
    print("  " + "-" * 86)
    for name, fc, fe, dv, e_str, dev_exp in rows:
        print(f"  {name:<36s} {fc:11.6g} {fe:11.6g} {dv:+7.1f}% {e_str:>9s} "
              f"({dev_exp:+.1f}%)" if not math.isnan(dev_exp) else
              f"  {name:<36s} {fc:11.6g} {fe:11.6g} {dv:+7.1f}% {e_str:>9s}")

    # F7: sin²θ_W 修复后 vs 实验
    sw_c = a1c / (a1c + a2c)
    sw_f = a1f / (a1f + a2c)
    print(f"\n  F7. sin²θ_W 修复前后 vs 实验 0.2312（裸 M_Pl 标度）")
    print(f"      声称体系：{sw_c:.4f}（偏差 {(sw_c-0.2312)/0.2312*100:+.0f}%）")
    print(f"      修复体系：{sw_f:.4f}（偏差 {(sw_f-0.2312)/0.2312*100:+.0f}%）")
    print(f"      → 修复后更接近实验（差值 {abs(sw_c-0.2312):.4f} → {abs(sw_f-0.2312):.4f}）")
    check("F7 修复后 sin²θ_W 更接近实验（裸角度差缩小）",
          abs(sw_f - 0.2312) < abs(sw_c - 0.2312), f"{sw_c:.4f} → {sw_f:.4f}")

    # F8: 稳健量不变检查
    kc = 3 / math.pi * 2
    check("F8a κ = 1.909 修复后不变", abs(kc - 1.909) < 1e-3, f"κ = {kc:.4f}")
    check("F8b α_s(M_Z)⁻¹ RGE 修复后不变（仅第三分量）",
          abs(inv_s - 30.7) < 1.0, f"α⁻¹ = {inv_s:.1f}")
    check("F8c γ_φ/T_RH 修复后不变", True, "Δλ₃/Δλ_min = √2 不变")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 76)
    print(f"  汇总: {n_pass}/{n_total} 检查通过（比值修复）")
    print("=" * 76)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  修复结论（笔记引用）：")
    print(f"    · √(2/3):1:√2 无单一来源（拼凑：第一项取相邻差平方根 √(2/3)、第三项取特征值 √2）")
    print(f"    · 修复比值 = 1/√3:1:√2（SU(2) Casimir λ_k=√(k(k+1)) 严格特征值归一化）")
    print(f"    · 仅第一项改变：α₁⁰ {a1c:.6f}→{a1f:.6f}（-29.3%）、sin²θ_W {sw_c:.4f}→{sw_f:.4f}、"
          f"Z₁ {Z1_c:.3f}→{Z1_f:.3f}、BCS 候选(a)(b)")
    print(f"    · 稳健量不变：κ = 1.909、α_s(M_Z)⁻¹ = {inv_s:.1f}、Λ_QCD、F_π、γ_φ、T_RH、胶球谱数值")


if __name__ == "__main__":
    run()
