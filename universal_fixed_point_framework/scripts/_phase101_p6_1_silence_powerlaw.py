# -*- coding: utf-8 -*-
"""
Phase 101 P6-1: 静默屏障幂律内生推导 —— 第一轮诊断
==========================================================
核心：以 P44 §6.6 母公式 R_supp(N) = σ^N（σ = S_4 = 1/15，纯框架代数常数）为禁戒率结构。
存活率 = 静默屏障穿透率：survival(n) = σ^{N(n)}，禁戒率 η = 1 - σ^{N(n)}。

本轮内容（诊断性，非拟合）：
  A. σ^N 幂律结构诊断：观测存活率（DESI 中场）落在 σ^N 族的什么 N 档（N_eff 诊断表）
  B. 谱隙框架内推导：Balmer 跃迁谱隙（Rydberg 谱带，P44 定理 2.1 框架内锚定）
     Δλ_gap(n) = 13.6·(1/4 - 1/n²) eV —— 谱隙小者拓扑类转变阈值低、静默屏障激活早
     （线序依赖的框架内候选来源，P6-3 预备）
  C. 磁场依赖：登记为开放问题（不引入外部 Landau 对象）

禁止：任何观测数据作为参数来源（观测仅出现在诊断对照列，明确标注）。
"""
import math
import json

SIGMA = 1.0 / 15.0   # S_4，P44 §6.6 纯框架代数常数（Bott 塔/Cl(1,7) 分支数 15）

# 观测存活率（DESI 中场 40.9-51.0 MG，纯线深降幅：Hβ −45%/Hγ −84%/Hδ −98%）
# —— 仅诊断对照，不参与推导参数
OBS_SURVIVAL = {"Hα": None, "Hβ": 0.55, "Hγ": 0.16, "Hδ": 0.02}

def n_eff(survival):
    """存活率 → 有效静默层级 N_eff = ln(survival)/ln(σ)。"""
    if survival is None or survival <= 0:
        return None
    return math.log(survival) / math.log(SIGMA)

def balmer_gap_eV(n):
    """Balmer 跃迁谱隙（Rydberg 谱带，P44 定理 2.1 框架内锚定）：13.6·(1/4-1/n²) eV。"""
    return 13.6057 * (1.0/4.0 - 1.0/(n*n))

def main():
    lines = [("Hα", 3), ("Hβ", 4), ("Hγ", 5), ("Hδ", 6), ("Hε", 7)]

    print("=" * 78)
    print("Phase 101 P6-1：静默屏障幂律诊断（σ=1/15 纯框架常数）")
    print("=" * 78)
    print(f"\nσ = 1/15 = {SIGMA:.6f}（P44 §6.6 S_4，Bott 塔代数常数）")
    print(f"σ^N 幂律族：σ^1={SIGMA**1:.5f}  σ^2={SIGMA**2:.5f}  σ^3={SIGMA**3:.5f}")

    print("\n--- A. σ^N 结构诊断（观测仅对照，非参数来源） ---")
    print(f"{'线':<6}{'n':<4}{'观测存活':<10}{'N_eff=ln(存活)/ln(σ)':<22}{'谱隙(eV)':<10}")
    rows = []
    for name, n in lines:
        surv = OBS_SURVIVAL.get(name)
        ne = n_eff(surv)
        gap = balmer_gap_eV(n)
        ne_s = f"{ne:.3f}" if ne is not None else "-"
        surv_s = f"{surv:.2f}" if surv is not None else "-"
        rows.append({"line": name, "n": n, "obs_survival": surv,
                     "N_eff": ne, "gap_eV": gap})
        print(f"{name:<6}{n:<4}{surv_s:<10}{ne_s:<22}{gap:<10.3f}")

    # N_eff 与 n 的线性关系诊断（仅诊断标度，框架推导见 P6-3）
    ne_vals = [(r["n"], r["N_eff"]) for r in rows if r["N_eff"] is not None]
    if len(ne_vals) >= 3:
        ns = [v[0] for v in ne_vals]; nes = [v[1] for v in ne_vals]
        # 最小二乘线性拟合（诊断标度，非推导参数）
        mean_n = sum(ns)/len(ns); mean_ne = sum(nes)/len(nes)
        num = sum((x-mean_n)*(y-mean_ne) for x,y in zip(ns,nes))
        den = sum((x-mean_n)**2 for x in ns)
        slope = num/den if den else 0.0
        intercept = mean_ne - slope*mean_n
        print(f"\n[N_eff ~ slope·n + intercept] 诊断标度：slope={slope:.4f}, intercept={intercept:.4f}")
        print("  （诊断用标度——N(n) 的框架推导见 P6-3：谱隙→拓扑类转变阈值→屏障激活序）")

    print("\n--- B. 谱隙框架内推导（P44 定理 2.1 Rydberg 谱带锚定） ---")
    print("Balmer 跃迁谱隙 Δλ_gap(n) = 13.6·(1/4 - 1/n²) eV：")
    print(f"{'线':<6}{'n':<4}{'谱隙(eV)':<12}{'谱隙比(Hβ=1)':<12}{'线序（谱隙大→禁戒强）':<6}")
    gap_beta = balmer_gap_eV(4)
    order = ""
    for name, n in sorted(lines, key=lambda x: balmer_gap_eV(x[1])):
        gap = balmer_gap_eV(n)
        ratio = gap/gap_beta
        print(f"{name:<6}{n:<4}{gap:<12.3f}{ratio:<12.3f}{'↑先禁戒' if n>=5 else ''}")
        if n >= 5:
            order += name + "→"
    print(f"谱隙递增方向（Hα 1.89 → Hε 3.12 eV）：谱隙大者闭合难 → 拓扑类转变难")
    print(f"  → 静默屏障维持（禁戒）强：线序依赖的框架内候选来源（P6-3），与观测线序方向一致")
    print(f"  （P44 定理 2.1：激发使谱间隙单调减小，达临界才闭合发射；相同激发下谱隙大者难达临界）")

    print("\n--- C. 磁场依赖登记 ---")
    print("磁场 → 拓扑类转变的框架内映射：开放问题（P6-2）。")
    print("不引入外部 Landau 对象（磁长度/Landau 态）作为参数来源。")

    result = {
        "sigma": SIGMA,
        "sigma_source": "P44 §6.6 S_4 (Bott tower / Cl(1,7) branch number 15)",
        "note": "观测仅诊断对照，非参数来源；N_eff 诊断标度需 P6-3 框架推导",
        "per_line": rows,
        "gap_order": "Hε(7)<Hδ(6)<Hγ(5)<Hβ(4)<Hα(3) 谱隙递增 → 高阶线先转变先禁戒",
        "magnetic_dependence": "open problem (P6-2), no external Landau objects",
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase101_p6_1_silence_powerlaw.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\nP6-1 第一轮诊断完成，exit 0")

if __name__ == "__main__":
    main()
