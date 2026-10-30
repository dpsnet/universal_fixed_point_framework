# -*- coding: utf-8 -*-
"""
Phase 101 P6-1: C 第一性化 —— 3D Landau 态横向 p-包含半径直接计算
==============================================================
目标：用第一性量子计算（3D Landau 态径向波函数数值积分）确定 C_p = R_p / ell_B，
     替换 Phase 100 中 C=3.03 的"观测拟合（Hγ 缺口 0.005）"支撑。
方法：关联 Laguerre 多项式递推（不依赖 scipy.special），数值积分 CDF。
输出：C_p(N,m) 表 + tail 分数表。参数仅 (N, m, p) —— 纯量子计算，零观测拟合。

单位：磁长度 ell_B = sqrt(hbar/eB)，本脚本全部无量纲（以 ell_B 为单位）。
Landau 径向波函数（圆柱坐标，含 rho 权重归一化）：
  psi_{N,m}(rho) ∝ rho^|m| exp(-rho^2/2) L_N^|m|(rho^2),  ell_B=1
  P(rho) drho = |psi|^2 rho drho,  int_0^inf P = 1
"""
import numpy as np
import json

def gen_laguerre(n, a, x):
    """关联 Laguerre 多项式 L_n^a(x)，递推（numpy 向量化）。"""
    if n == 0:
        return np.ones_like(x)
    L_prev = np.ones_like(x)          # L_0^a
    L_cur = (1.0 + a - x)             # L_1^a
    for k in range(1, n):
        # (k+1) L_{k+1} = (2k+1+a-x) L_k - (k+a) L_{k-1}
        L_next = ((2.0*k + 1.0 + a - x) * L_cur - (k + a) * L_prev) / (k + 1.0)
        L_prev, L_cur = L_cur, L_next
    return L_cur

def landau_density(rho, N, m):
    """|psi_{N,m}(rho)|^2 * rho（未归一化），ell_B=1。"""
    a = abs(m)
    x = rho * rho
    L = gen_laguerre(N, a, x)
    # 未归一化振幅：rho^a exp(-rho^2/2) L_N^a(rho^2)
    psi2 = (rho ** (2*a)) * np.exp(-x) * (L ** 2) * rho   # *rho 权重
    return psi2

def normalize_density(rho, N, m):
    """数值归一化的密度 P(rho)，int P drho = 1。"""
    d = landau_density(rho, N, m)
    norm = np.trapezoid(d, rho)
    assert norm > 0, f"norm<=0 for N={N},m={m}"
    return d / norm

def containment_radius(rho, P, p):
    """p-包含半径 R_p：int_0^{R_p} P drho = p。二分求解。"""
    cdf = np.cumsum(P) * (rho[1] - rho[0])
    if cdf[-1] < p:
        return np.inf
    idx = np.searchsorted(cdf, p)
    idx = min(idx, len(rho) - 1)
    return float(rho[idx])

def tail_fraction(rho, P, r_c):
    """tail 分数：int_{r_c}^inf P drho。"""
    mask = rho >= r_c
    if not mask.any():
        return 0.0
    return float(np.trapezoid(P[mask], rho[mask]))

def main():
    rho = np.linspace(0.0, 40.0, 200001)   # 高分辨率（40 ell_B，尾部分辨）
    ps = [0.90, 0.95, 0.99, 0.999]
    rcs = [1.0, 2.0, 3.0, 4.0, 5.0]

    rows = []
    for N in range(0, 9):          # N=0..8
        for m in [0, 1, 2, 3]:
            P = normalize_density(rho, N, m)
            row = {"N": N, "m": m}
            for p in ps:
                R = containment_radius(rho, P, p)
                row[f"C_{p}"] = round(R, 4)
            row["tail"] = {f"rc_{int(rc)}": round(tail_fraction(rho, P, rc), 6)
                           for rc in rcs}
            rows.append(row)

    # 关键对照输出
    summary = {
        "method": "3D Landau radial wavefunction numerical integration (gen_laguerre recurrence)",
        "unit": "ell_B",
        "C_0.99_ground": next(r["C_0.99"] for r in rows if r["N"] == 0 and r["m"] == 0),
        "C_0.99_first_excited": next(r["C_0.99"] for r in rows if r["N"] == 1 and r["m"] == 0),
        "phase100_reference": {"C_3.03": "p=0.99 containment, phase100 (had H-gamma fit support)"},
        "table": rows,
    }
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase101_p6_1_landau_containment.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)

    # 控制台摘要
    print("=== P6-1: Landau transverse p-containment radii C_p = R_p/ell_B ===")
    print(f"{'N':>2} {'m':>2} " + " ".join(f"C_{p:<5}" for p in ps))
    for r in rows:
        print(f"{r['N']:>2} {r['m']:>2} " + " ".join(f"{r[f'C_{p}']:<8.4f}" for p in ps))
    print("\nGround state tail fractions (ell_B):")
    g = next(r for r in rows if r["N"] == 0 and r["m"] == 0)
    for k, v in g["tail"].items():
        print(f"  r>{k[3:]} ell_B: {v:.6f}")
    print("\nC_0.99(ground) =", summary["C_0.99_ground"])
    print("C_0.99(N=1,m=0) =", summary["C_0.99_first_excited"])
    print("P6-1 done, exit 0")

if __name__ == "__main__":
    main()
