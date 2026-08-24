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
paperX_p6_fluorescence_yield.py — B 类静默抑制预言 vs 标准 X 射线荧光产额对照（诚实张力登记）

笔记来源: notes/06_photon_topology/photon_topology_theory.md §6.6.1（2026-08-14 深化）
衔接: paperX_p6_atomic_silence.py（P6 候选体系）+ paperX_channel_quantum_yield.py
      （量子产率框架 Phi = A_eff/(A_eff+k_nr)）

P6 B 类预言（静默屏障抑制）：内壳层跃迁（K 壳层空穴）辐射须穿越 N 层满壳层静默屏障，
有效辐射速率 A_eff = A*(1/15)^N，量子产率 Phi(N) = R_supp(N)/(R_supp(N)+r)。

本脚本把 B 类预言映射到候选体系（K/Kr/Xe/Rn，K 壳层空穴，N = n_max-1），
并与标准 X 射线 K 荧光产额 w_K（文献量级，Krause 1979 类数据，随 Z 单调增）对照。

核心检查（诚实张力）：
  · 框架预言：Phi 随 N（=壳层数）单调降 —— K(2.96e-4) > Xe(1.97e-5) > Rn(1.3e-6)
  · 标准数据：w_K 随 Z 单调增 —— K(0.12) < Kr(0.64) < Xe(0.87) < Rn(0.96)
  · 方向完全相反 → 若以 K 壳层荧光产额为检验对象，B 类叠加抑制假设被标准数据排除
    （盲登记排除线）；可能的适用域限定：静默屏障抑制不适用于内壳层 X 射线
    （高能光子穿透外层电子云无阻碍），作用域或限于光学/价层跃迁（候选修正）。

诚实边界: w_K 为文献量级近似（Krause 1979 类数据，标注量级非精确）；Phi 取 r=1
（无辐射竞争与辐射同率）基准；本脚本为**张力登记**（负结果/登记项），非新预言。
"""
import numpy as np

SIGMA_SILENT = 1.0 / 15.0

# 候选体系：K 壳层空穴（N = n_max - 1）
# w_K：标准 K 荧光产额（文献量级，Krause 1979 类数据——标注量级，非精确）
CANDIDATES = [
    ("K",  19, 4, 0.12),
    ("Kr", 36, 4, 0.64),
    ("Xe", 54, 5, 0.87),
    ("Rn", 86, 6, 0.96),
]


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def r_supp(n_layers):
    return SIGMA_SILENT ** n_layers


def main():
    print("B 类静默抑制预言 vs 标准 X 射线荧光产额对照（诚实张力登记）")
    print("=" * 78)

    # S1: 候选体系 B 类预言 Phi(N)（r=1 基准）
    print("\nS1  候选体系 B 类预言 Phi(N) = R_supp(N)/(R_supp(N)+r)，r=1")
    ok1 = True
    preds = {}
    for name, Z, nmax, _w in CANDIDATES:
        N = nmax - 1
        R = r_supp(N)
        phi = R / (R + 1.0)          # r=1
        preds[name] = phi
        print(f"   {name:<3} (Z={Z:<3}, N={N}): R_supp={R:.3e}  Phi_pred={phi:.3e}")
        ok1 = ok1 and phi > 0.0
    # 单调性：N 越大 Phi 越低
    ok1 = ok1 and preds["K"] > preds["Xe"] > preds["Rn"]
    check("S1  框架预言：Phi 随 N（壳层数）单调降（K>Xe>Rn，R_supp 叠加抑制）", ok1)

    # S2: 标准 K 荧光产额 w_K（文献量级）
    print("\nS2  标准 K 荧光产额 w_K（文献量级，Krause 1979 类数据）")
    ok2 = True
    stds = {}
    for name, Z, nmax, w in CANDIDATES:
        stds[name] = w
        print(f"   {name:<3} (Z={Z:<3}): w_K(标准) = {w:.2f}")
    ok2 = ok2 and stds["K"] < stds["Kr"] < stds["Xe"] < stds["Rn"]
    check("S2  标准数据：w_K 随 Z 单调增（K<Kr<Xe<Rn，原子序数增大荧光产额升高）", ok2)

    # S3: 方向性对照——框架预言 vs 标准数据的单调方向
    print("\nS3  方向性对照（核心张力检查）")
    print("   框架预言 Phi：  K(2.96e-4) > Xe(1.97e-5) > Rn(1.3e-6)   —— 随原子变重单调降")
    print("   标准数据 w_K：  K(0.12)     < Xe(0.87)     < Rn(0.96)   —— 随原子变重单调升")
    # 方向：轻→重（K→Rn）预言降 vs 标准升 ⟹ 端点方向相反
    # （K/Kr 同为 N=3 预言平级，故用端点 K vs Rn 而非逐配对）
    direction_opposite = (preds["K"] > preds["Rn"]) and (stds["K"] < stds["Rn"])
    ok3 = direction_opposite
    check("S3  框架预言与标准数据方向**完全相反**（Phi 随 Z 降、w_K 随 Z 升）——"
          "B 类叠加抑制假设与内壳层荧光产额实测方向冲突", ok3)

    # S4: 张力量化（Phi_pred / w_K_std 比值，量级差）
    print("\nS4  张力量化：Phi_pred / w_K_std（B 类预言相对标准数据的偏离量级）")
    ok4 = True
    for name, Z, nmax, w in CANDIDATES:
        ratio = preds[name] / w
        print(f"   {name:<3}: Phi_pred={preds[name]:.2e} / w_K={w:.2f} = {ratio:.1e}"
              f"（低 {1.0/ratio:.0e} 倍）")
        ok4 = ok4 and ratio < 1e-2          # 全部低 2 个量级以上
    check("S4  B 类预言低于标准 w_K 全部 2 个量级以上（K 低 400 倍至 Rn 低 7e5 倍）"
          "——预言与实测量级严重不符", ok4)

    # S5: 盲登记排除线 + 适用域限定候选（诚实负结果/登记项）
    print("\nS5  盲登记排除线 + 适用域限定候选（诚实负结果）")
    print("   排除线：若以 K 壳层荧光产额为检验对象，B 类叠加抑制假设被标准数据排除")
    print("   适用域限定候选：静默屏障抑制或限于光学/价层跃迁（低能光子），")
    print("   不适用于内壳层 X 射线（高能光子穿透外层电子云无阻碍）——R_supp 作用域待限定")
    ok5 = True   # 排除线登记为负结果（脚本 exit 0 即完成，run_all_tests 规则：负结果登记项）
    check("S5  排除线登记：B 类以 K 荧光产额检验则被排除（方向相反+量级差≥2 个量级）；"
          "适用域限定候选登记（R_supp 作用域或限光学/价层跃迁）——负结果/登记项", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"B 类张力对照：{sum(results)}/5 通过（S5 为负结果登记，非新预言）")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
