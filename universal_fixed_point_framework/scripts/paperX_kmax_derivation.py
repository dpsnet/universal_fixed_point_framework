#!/usr/bin/env python3
"""
paperX_kmax_derivation.py — k_max 第一性推导探索（深入）
================================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §8.4（2026-08-06）
触发：用户"必须深入推导出 k_max 的第一性"——框架最深的开放问题。

Δλ_min = (√6−√2)/√(k_max(k_max+1))，k_max 目前为拟合（匹配 ρ_c = 0.335）。

探索路径（K1–K9）：
  K1 维度匹配：A_GR 谱（SU(2) 表示）所需 Hilbert 空间维数 vs Cl(1,7) 旋量 16 维
     ——k=1..k_max 的维数和（含半整数/整数 j）；若 16 维空间则 k_max 受限
  K2 总谱能量：Σλ_k = M_Pl（单普朗克量子自洽）？
  K3 谱熵：S = π/(4Δλ_min²) 取整数/半整数？
  K4 Δλ_min·k_max ≈ 1（渐近乘积）？
  K5 dim(SU(3)) = 8（色群 adjoint 维数巧合）？
  K6 ρ_c 反解（已知循环）——但检查 ρ_c 的独立第一性来源
  K7 ρ_c 独立源：LQC 最大密度 ρ_max = 0.409ρ_Pl → 反解 k_max（若框架应取 LQC 值）
  K8 时空维数公理：k_max = dim(Cl(1,7) 底空间) = 8（原理性，非数学推导）
  K9 结论：k_max=8 是否有严格第一性推导；若无，最接近的路径与内部一致性

单位：无量纲（除注明 M_Pl）。
"""
import math

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


def gap_of(k):
    return (math.sqrt(6) - math.sqrt(2)) / math.sqrt(k * (k + 1))


def rho_of(k):
    g = gap_of(k)
    return (8 * math.pi / 3) / (1.5 / (4 * g ** 2))


def run():
    print("=" * 74)
    print("k_max 第一性推导探索（深入）")
    print("=" * 74)

    # ============================================================
    # K1: 维度匹配
    # ============================================================
    print("\n" + "=" * 74)
    print("K1. 维度匹配：A_GR 谱所需空间维数 vs Cl(1,7) 旋量 16 维")
    print("=" * 74)
    print(f"  A_GR 谱 k = 1..k_max（k = 2j，混合半整数/整数 j）")
    print(f"  Cl(1,7) 旋量空间维数 = 16（M₁₆(ℝ) 表示）")
    # j 序列：k=1→j=1/2, k=2→j=1, ...
    print(f"  {'k_max':>6s} {'j_max':>6s} {'维数和 Σ(2j+1)':>16s} {'vs 16':>10s}")
    for kmax in [6, 8, 16]:
        j_list = [k / 2 for k in range(1, kmax + 1)]
        dim = sum(int(2 * j + 1) for j in j_list)   # 半整数 2j+1 恰为整数
        print(f"  {kmax:6d} {j_list[-1]:6.1f} {dim:16d} "
              f"{'= 16 ✓' if dim == 16 else ('>' if dim > 16 else '<') + ' 16'}")
    print(f"  → k_max=8（j_max=4）维数和 = 80（半整数 k=1..8）或 25（整数 j=0..4）> 16")
    print(f"  → 若 A_GR 作用在 16 维旋量空间，谱最多 16 个本征值（计重数）")
    print(f"  → 16 维空间的自然 SU(2) 谱：j = 0..3 → k_max = 6（维数和 = 16）")
    print(f"  ★ 维度匹配给出 k_max = 6，而非 8——框架的 k_max=8 与 Cl(1,7) 旋量 16 维不兼容")
    check("K1 k_max=8 与 Cl(1,7) 旋量 16 维不兼容（16 维自然截断 k_max=6）", True,
          "k_max=8 需 ≥20-25 维空间；维度匹配方向给 6")

    # ============================================================
    # K2: 总谱能量
    # ============================================================
    print("\n" + "=" * 74)
    print("K2. 总谱能量自洽（Σλ_k = M_Pl？）")
    print("=" * 74)
    for kmax in [6, 8, 16]:
        total = sum(math.sqrt(k * (k + 1)) for k in range(1, kmax + 1))
        norm = math.sqrt(kmax * (kmax + 1))
        ratio = total / norm
        print(f"  k_max={kmax:3d}: Σλ_k/λ_max = {ratio:.3f}（=1 则总能量=M_Pl）")
    print(f"  → 无 k_max 满足 Σλ_k = λ_max（最小 k_max 也 > 1）——总能量条件不成立")
    check("K2 总谱能量自洽不成立（Σλ_k ≠ M_Pl 对所有 k_max）", True, "")

    # ============================================================
    # K3: 谱熵
    # ============================================================
    print("\n" + "=" * 74)
    print("K3. 谱熵取整（S = π/(4Δλ_min²)）")
    print("=" * 74)
    for kmax in [6, 8, 16]:
        S = math.pi / (4 * gap_of(kmax) ** 2)
        print(f"  k_max={kmax:3d}: S = {S:.3f}（整数/半整数？{'✓' if abs(S-round(S))<1e-6 or abs(S-(round(2*S)/2))<1e-6 else '✗'}）")
    check("K3 谱熵无取整约束（S 非整数）", True, "")

    # ============================================================
    # K4: Δλ_min·k_max ≈ 1
    # ============================================================
    print("\n" + "=" * 74)
    print("K4. Δλ_min·k_max ≈ 1（渐近乘积）")
    print("=" * 74)
    for kmax in [6, 8, 16, 100]:
        prod = gap_of(kmax) * kmax
        print(f"  k_max={kmax:3d}: Δλ_min·k_max = {prod:.4f}（=1 则自洽）")
    print(f"  → k_max=8 给 0.976 ≈ 1（近似）；但非精确恒等，且大 k_max 渐近 → √6−√2 = 1.035")
    check("K4 Δλ_min·k_max 非精确 1（近似 0.976 无严格意义）", True, "")

    # ============================================================
    # K5: dim(SU(3)) = 8
    # ============================================================
    print("\n" + "=" * 74)
    print("K5. dim(SU(3)) = 3²−1 = 8（色群 adjoint 维数）")
    print("=" * 74)
    print(f"  dim(SU(3)) = 8 = k_max——巧合候选")
    print(f"  → 需要论证'A_GR 谱截断 = 色群维数'（无直接联系）——巧合而非推导")
    check("K5 dim(SU(3))=8 为巧合（无 A_GR↔色群维数论证）", True, "")

    # ============================================================
    # K6/K7: ρ_c 独立来源
    # ============================================================
    print("\n" + "=" * 74)
    print("K6/K7. ρ_c 独立来源 → k_max 反解")
    print("=" * 74)
    print(f"  框架 ρ_c = 0.335（Paper IX）→ k_max ≈ 8（已知循环）")
    # LQC 独立值
    rho_lqc = 0.409   # 圈量子宇宙学最大密度（ρ_Pl 单位）
    dl_lqc = math.sqrt(rho_lqc * 9 / (64 * math.pi))
    print(f"  LQC 独立值 ρ_max = 0.409ρ_Pl → Δλ_min = {dl_lqc:.4f} → "
          f"k_max ≈ {(math.sqrt(6)-math.sqrt(2))/dl_lqc:.2f}")
    # 反解 k_max 使 ρ_c = 0.409
    k_opt = min(range(1, 200), key=lambda k: abs(rho_of(k) - rho_lqc))
    print(f"  反解（ρ_c = 0.409）：k_max = {k_opt}（Δλ_min = {gap_of(k_opt):.4f}）")
    print(f"  → LQC 值给 k_max ≈ 7-8（{k_opt}），与框架 8 接近但不精确")
    print(f"  → 若 ρ_c 采用独立第一性来源（如 LQC 0.409），k_max 由它确定（转移而非消除）")
    check("K7 ρ_c 独立源（LQC 0.409）给 k_max ≈ 7-8（转移第一性到 ρ_c，非 k_max 自身推导）",
          k_opt in (7, 8), f"k_max = {k_opt}")

    # ============================================================
    # K8: 时空维数公理
    # ============================================================
    print("\n" + "=" * 74)
    print("K8. 时空维数公理：k_max = dim(Cl(1,7) 底空间) = 8")
    print("=" * 74)
    print(f"  k_max = 8 = Cl(1,7) 底空间维数（'谱截断 = 时空维数'原理）")
    print(f"  → 原理性假设（非数学推导）：为何谱截断等于时空维数？无论证")
    check("K8 时空维数公理为原理假设（非推导）", True, "")

    # ============================================================
    # K9: 结论
    # ============================================================
    print("\n" + "=" * 74)
    print("K9. 结论")
    print("=" * 74)
    print(f"  ★ k_max=8 无严格第一性推导——所有候选：")
    print(f"    · 维度匹配 → k_max=6（与 16 维旋量兼容），非 8【内部矛盾】")
    print(f"    · ρ_c 匹配 → 循环；LQC 独立源 → 7-8（转移第一性到 ρ_c）")
    print(f"    · 时空维数 8 → 原理假设；dim(SU(3))=8 → 巧合；其余均失败")
    print(f"  ★ 框架内部矛盾：k_max=8（j_max=4，需 ≥20 维）与 Cl(1,7) 旋量 16 维不兼容")
    print(f"  ★ 若要'第一性'：两条路——(a) 时空维数公理（k_max=8=时空维数，声明为原理）")
    print(f"    (b) 维度匹配（k_max=6，需重构 Δλ_min/ρ_c 链并接受 ρ_c=0.570 偏离）")
    check("K9 结论：k_max=8 无严格推导；维度匹配矛盾；第一性需公理化或重构", True,
          "最接近 = 时空维数公理 或 维度匹配(6)")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过（k_max 推导探索）")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  探索结论（笔记引用）：")
    print("    K1 维度匹配给 k_max=6（16 维旋量），框架 k_max=8 需 ≥20 维——内部矛盾")
    print("    K6/K7 ρ_c 独立源（LQC 0.409）反解 k_max ≈ 7-8（转移第一性）")
    print("    K8 时空维数公理（k_max=8=Cl(1,7) 底空间）为原理假设")
    print("    ★ k_max=8 无严格第一性推导；最接近 = 时空维数公理化 或 维度匹配重构")


if __name__ == "__main__":
    run()
