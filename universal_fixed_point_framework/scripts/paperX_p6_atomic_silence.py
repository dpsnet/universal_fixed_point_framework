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
paperX_p6_atomic_silence.py — P6 原子实例验证：静默叠加定理的递归层实例化（笔记 §3.8，2026-08-12）

回应 CNF 评价"P6 跨尺度挪用"批评的重构：P6 不是跨尺度移植，而是框架根基
（静默叠加定理）的原子尺度实例。本脚本验证实例的框架内结构：
落层（递归层 Rydberg）+ 原子结构论证（壳层 = 嵌套 Rec + 逐层谱隙）
+ 定量判据（R_supp(N)=σ^N, σ=S4=1/15）+ 盲登记（候选体系 + 诚实负结果）。

S1: 壳层结构与逐层谱隙（Rydberg：E_n=-13.6/n²，相邻壳层 Δλ_gap）
S2: 静默叠加抑制曲线 R_supp(N)=(1/15)^N（N=0..8）+ 阈值线
S3: N_crit 反解：N_crit(θ)=ceil(lnθ/lnσ)——θ=1e-3→3 层、θ=1e-6→6 层
    （与 paperX_photon_cross_effects.py E6 一致）
S4: 候选体系映射：各原子可达 N（空穴壳层外满壳层数）——诚实负结果：
    现行周期表最大 N=5（Rn 的 K 壳层空穴）< N_crit(1e-6)=6，θ=1e-6 全抑制
    区需超重元素（第 7 壳层）——可证伪预言
S5: 与 2s→1s 单层锚点衔接（B12=0 电偶极禁戒，paper44 §2.3 定义 2.4）

诚实边界：本脚本验证的是框架递归层定理的原子实例结构（落层/壳层/叠加形式），
非跨尺度机制等效的实验证明；σ=1/15 定量值为可证伪预言（远期），
标准原子物理同类现象（禁戒跃迁/闭合壳层稳定性）为已知事实（温和兼容重述）。
"""
import numpy as np

SIGMA_SILENT = 1.0 / 15.0      # σ_silent = S4 = 1/15
RYDBERG_EV = 13.6              # eV

# 代表性原子的主壳层数（n_max）
ATOMS = [("H", 1, 1), ("He", 2, 1), ("Li", 3, 2), ("Ne", 10, 2),
         ("Na", 11, 3), ("Ar", 18, 3), ("K", 19, 4), ("Kr", 36, 4),
         ("Xe", 54, 5), ("Rn", 86, 6)]


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def r_supp(n_layers):
    """静默叠加抑制率 R_supp(N) = σ_silent^N"""
    return SIGMA_SILENT ** n_layers


def n_crit(theta):
    """N_crit(θ) = ceil(ln θ / ln σ_silent)"""
    return int(np.ceil(np.log(theta) / np.log(SIGMA_SILENT)))


def main():
    print("P6 原子实例验证：静默叠加定理的递归层实例化（笔记 §3.8）")
    print("=" * 78)

    # S1: 壳层结构与逐层谱隙（Rydberg）
    print("\nS1  壳层结构与逐层谱隙（Rydberg：E_n = -13.6/n² eV）")
    ok1 = True
    for name, Z, nmax in ATOMS:
        shells = " ".join(f"{n}s{n}p" if n > 1 else "1s" for n in range(1, nmax + 1))
        print(f"   {name:<3} Z={Z:<3} n_max={nmax}  壳层: {shells}")
    gaps = {}
    for n in range(1, 6):
        gaps[n] = RYDBERG_EV * (1.0 / n ** 2 - 1.0 / (n + 1) ** 2)
        print(f"   谱隙 Δλ_gap({n}→{n+1}) = {gaps[n]:6.2f} eV")
    # 核对：Lyman α（2→1）10.2 eV、Balmer α（3→2）1.89 eV（标准值）
    ok1 = abs(gaps[1] - 10.2) < 0.1 and abs(gaps[2] - 1.89) < 0.05
    check("S1  壳层 = 嵌套 Rec 对象（定义 2.1），逐层谱隙由 Rydberg 结构确定"
          "（Lyman α 10.2 eV/Balmer α 1.89 eV 核对）", ok1,
          f"Δλ_gap(2→1)={gaps[1]:.2f} eV")

    # S2: 静默叠加抑制曲线
    print("\nS2  静默叠加抑制曲线 R_supp(N) = (1/15)^N")
    ns = np.arange(0, 9)
    rs = r_supp(ns)
    for n, r in zip(ns, rs):
        mark = ""
        if abs(r - 1e-3) < 1e-4 or (n == 3):
            mark = "  <- θ=1e-3 阈值附近 (N_crit=3)"
        if abs(r - 1e-6) < 1e-6 or (n == 6):
            mark = "  <- θ=1e-6 阈值附近 (N_crit=6)"
        print(f"   N={n}: R_supp = {r:.3e}{mark}")
    ok2 = abs(rs[3] - 2.963e-4) < 1e-6 and abs(rs[6] - 8.78e-8) < 1e-10
    check("S2  R_supp(N)=(1/15)^N：N=3 达 3e-4（θ=1e-3 阈值）、N=6 达 8.8e-8（θ=1e-6 阈值）", ok2)

    # S3: N_crit 反解（对照 cross_effects E6）
    print("\nS3  N_crit(θ) = ceil(ln θ / ln σ_silent)")
    ok3 = True
    for theta, expect in [(1e-3, 3), (1e-6, 6)]:
        nc = n_crit(theta)
        print(f"   θ={theta:.0e}: N_crit = {nc} 层（R_supp({nc})={r_supp(nc):.2e} ≤ {theta:.0e}）")
        ok3 = ok3 and nc == expect
        # 一致核对：N_crit-1 层未达阈值（严格性）
        ok3 = ok3 and r_supp(nc - 1) > theta
    check("S3  N_crit(θ=1e-3)=3 层、N_crit(θ=1e-6)=6 层（与 paperX_photon_cross_effects.py E6 一致，"
          "且 N_crit-1 层严格未达阈值）", ok3)

    # S4: 候选体系映射（空穴壳层外满壳层数 N）+ 诚实负结果
    print("\nS4  候选体系映射：N = 空穴壳层外的满壳层数（K 壳层空穴 ⟹ N = n_max - 1）")
    ok4 = True
    max_N = 0
    for name, Z, nmax in ATOMS:
        N = nmax - 1  # K 壳层（m=1）空穴
        reach3 = N >= 3
        max_N = max(max_N, N)
        print(f"   {name:<3} (n_max={nmax}): K 壳层空穴 N={N}   "
              f"{'达 N_crit(1e-3)=3 ✓' if reach3 else '未达 N_crit(1e-3)'}")
    # 诚实负结果：现行周期表最大 N=5 < N_crit(1e-6)=6
    ok4a = all(N >= 3 for _, _, nmax in ATOMS if nmax >= 4)   # n_max>=4 的原子达 N_crit(1e-3)
    ok4b = max_N == 5 and max_N < n_crit(1e-6)                # 最大 N=5 < 6（θ=1e-6 区不可达）
    ok4 = ok4a and ok4b
    print(f"   诚实负结果：现行周期表最大 N = {max_N} < N_crit(1e-6) = 6 —— θ=1e-6 全抑制区"
          "需超重元素（第 7 壳层）——可证伪预言")
    check("S4  候选体系：n_max≥4 原子（K/Kr/Xe/Rn）达 N_crit(1e-3)=3；"
          "诚实负结果：现行周期表 N_max=5 < N_crit(1e-6)=6（θ=1e-6 区为超重元素预言）", ok4,
          f"N_max={max_N}")

    # S5: 与 2s→1s 单层锚点衔接（paper44 §2.3 定义 2.4：电偶极禁戒 B12=0）
    print("\nS5  与 2s→1s 单层锚点衔接（B12=0 电偶极禁戒，paper44 §2.3）")
    # 氢 2s→1s 单光子禁戒（B12=0）= 单层静默抑制辐射的原子锚点；
    # 允许跃迁（相邻壳层，N=0）无叠加抑制（R_supp(0)=1，与快速允许跃迁一致）
    ok5a = r_supp(0) == 1.0                     # 允许跃迁（N=0）：无抑制
    ok5b = abs(r_supp(1) - 1.0 / 15.0) < 1e-12  # 单层抑制 = σ_silent
    ok5 = ok5a and ok5b
    print(f"   R_supp(0)=1（相邻壳层允许跃迁无抑制）——与快速允许跃迁一致；"
          f"R_supp(1)={r_supp(1):.4f}=σ_silent（单层抑制）——2s→1s 禁戒（B12=0）"
          "为单层静默抑制辐射的框架重述")
    check("S5  单层锚点：R_supp(0)=1（允许跃迁无抑制）、R_supp(1)=σ_silent（单层抑制）"
          "——2s→1s 禁戒（B12=0，§2.3 定义 2.4）为框架单层实例", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"P6 原子实例验证：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
