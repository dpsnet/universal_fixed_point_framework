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
"""t5-1 闭环验证：东营孔径分布 → Young-Laplace → IP 阈值 → 朗缪尔 ν=1 复现。

数学同构（无截断）：朗缪尔累积 F(P)=P/(P+a) ⇔ 体积加权孔径分布
f_v(r) = C/(r+C)^2（r>0，1/r^2 尾）＋ Young-Laplace 毛细阈 U(r)=A/r，A=a·C
⇒ F_U(u) = u/(u+a)（精确朗缪尔）。见 P2-6f。

本脚本检验同构在有限孔径截断 [r_min, r_max]（NMR/压汞实测范围）＋
渗流几何（IP 突破暂态抑制）下的存活：
  - r_max 截断 → 高压端饱和提前（F_U 提前到 1，朗缪尔尾被切断）
  - r_min 截断 → 低压端（大孔）缺失
  - 两者 + IP 几何 → P2 型 ν 是否仍 ≈1、双倒数线性 R² 是否仍 ≈0.93–0.99

采样：F_v(r)=[1/(r_min+C)−1/(r+C)]/[1/(r_min+C)−1/(r_max+C)] 反变换
      r(T)=1/[1/(r_min+C)−T·D]−C，D=1/(r_min+C)−1/(r_max+C)
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_ip_uf import ip_union_entry

A_DP = 1.09  # 东营 ΔP_L (MPa)
PCAP = 3.01   # 东营窗口上限 (MPa)

def sample_pore_radii(n, r_min, r_max, C, seed):
    """f_v(r)∝(r+C)^(-2) 反变换采样，r∈[r_min,r_max] 有限截断。"""
    rng = np.random.default_rng(seed)
    T = rng.random(n)
    D = 1.0/(r_min + C) - 1.0/(r_max + C)
    r = 1.0/(1.0/(r_min + C) - T*D) - C
    return r

def pore_thresholds(binary, r_min, r_max, C, a=A_DP, seed=0):
    """孔径采样 → 毛细阈 U=a·C/r（Young-Laplace，大孔低阈先侵入）。"""
    n_pore = binary.sum()
    r = sample_pore_radii(n_pore, r_min, r_max, C, seed)
    U_pore = a * C / r
    U3d = np.full(binary.shape, 2.0)
    U3d[binary] = U_pore
    return U3d

def run_ip_pores(binary, r_min, r_max, C, a=A_DP, seed=0):
    U3d = pore_thresholds(binary, r_min, r_max, C, a, seed)
    pore_idx = np.flatnonzero(binary.ravel())
    Uf = U3d.ravel()
    order = pore_idx[np.argsort(Uf[pore_idx])]
    return ip_union_entry(binary, Uf, order)

def langmuir_fit(P, S, Pc):
    """双倒数线性化 1/S=1/R_f+(a/R_f)(1/P)，窗口 P∈(P_c, 3.01]。返回 R_f,a,R²。"""
    m = (P > Pc) & (P <= PCAP) & (S > 1e-3) & (S < 0.999)
    if m.sum() < 5:
        return None
    X = 1.0/P[m]; Y = 1.0/S[m]
    A_ = np.vstack([X, np.ones_like(X)]).T
    k, b = np.linalg.lstsq(A_, Y, rcond=None)[0]
    pred = k*X + b
    r2 = 1 - np.sum((Y-pred)**2)/np.sum((Y-Y.mean())**2)
    if k <= 0 or b <= 0:
        return None
    return 1.0/b, k/b, r2

def p2nu(P, S, Pc):
    """P2 型 ν：log P vs log(1−S)，窗口 P∈(P_c, 3.01]。"""
    resid = 1.0 - S
    m2 = (resid > 0.01) & (P > Pc) & (P <= PCAP)
    if m2.sum() < 10:
        return None
    X = np.log(resid[m2]); Y = np.log(P[m2])
    A_ = np.vstack([X, np.ones_like(X)]).T
    k, b = np.linalg.lstsq(A_, Y, rcond=None)[0]
    pred = k*X + b
    r2 = 1 - np.sum((Y-pred)**2)/np.sum((Y-Y.mean())**2)
    return -k, r2

def truncated_F(U, r_min, r_max, C, a=A_DP):
    """截断孔径分布的直接累积 F_U(u)=P(U≤u)（无几何对照）。"""
    if U >= a*C/r_min:
        return 1.0
    if U <= a*C/r_max:
        return 0.0
    r = a*C/U
    # F_v(r) 截断 CDF
    D = 1.0/(r_min+C) - 1.0/(r_max+C)
    return (1.0/(r_min+C) - 1.0/(r+C)) / D

if __name__ == "__main__":
    n = 96
    ncfg = 8
    r_min = 1.0
    print(f"t5-1 闭环：孔径 f_v∝(r+C)^-2 → U=a·C/r → IP（{n}³ ncfg={ncfg}，a={A_DP}，r_min={r_min}nm）")
    print("=" * 100)
    for phi in (0.31, 0.40):
        for C in (30.0, 100.0, 300.0):
            print(f"\n--- φ={phi:.2f} C={C:.0f}nm (U=1.09·{C:.0f}/r MPa) ---")
            print(f"{'r_max(nm)':>10} {'P_c':>7} {'S_c':>6} {'P2型ν':>7} {'R²ν':>6} "
                  f"{'双倒数R²':>8} {'R_f':>6} {'a_eff':>6} {'无几何R²':>8} {'S顶':>5}")
            for r_max in (100.0, 300.0, 1000.0, 1e6):
                Pcs, Scs, nus, r2nus, lfs, tr2s = [], [], [], [], [], []
                for cfg in range(ncfg):
                    rng = np.random.default_rng(cfg)
                    binary = rng.random((n, n, n)) < phi
                    P, S, Pc, Sc = run_ip_pores(binary, r_min, r_max, C, seed=cfg)
                    if Pc < 0:
                        continue
                    nu = p2nu(P, S, Pc)
                    lf = langmuir_fit(P, S, Pc)
                    if nu:
                        Pcs.append(Pc); Scs.append(Sc)
                        nus.append(nu[0]); r2nus.append(nu[1])
                    if lf:
                        lfs.append(lf)
                    # 无几何对照：截断 F_U vs 精确朗缪尔 F=U/(U+a)，同窗口
                    Uvals = P[(P > Pc) & (P <= PCAP) & (S > 1e-3) & (S < 0.999)]
                    if Uvals.size >= 5:
                        F_t = np.array([truncated_F(u, r_min, r_max, C) for u in Uvals])
                        F_l = Uvals/(Uvals + A_DP)
                        m_ = (F_t > 1e-3) & (F_t < 0.999) & (F_l > 1e-3) & (F_l < 0.999)
                        if m_.sum() >= 5:
                            X = 1.0/Uvals[m_]; Yt = 1.0/F_t[m_]
                            A_ = np.vstack([X, np.ones_like(X)]).T
                            k, b = np.linalg.lstsq(A_, Yt, rcond=None)[0]
                            pred = k*X + b
                            tr2 = 1 - np.sum((Yt-pred)**2)/np.sum((Yt-Yt.mean())**2)
                            tr2s.append(tr2)
                if not nus:
                    print(f"{r_max:10.0f} 无突破/窗口")
                    continue
                Pc_ = np.mean(Pcs); Sc_ = np.mean(Scs)
                nu_ = np.mean(nus); r2n_ = np.mean(r2nus)
                if lfs:
                    Rf_ = np.mean([x[0] for x in lfs])
                    a_ = np.mean([x[1] for x in lfs])
                    r2l_ = np.mean([x[2] for x in lfs])
                else:
                    Rf_ = a_ = r2l_ = float("nan")
                tr2_ = np.mean(tr2s) if tr2s else float("nan")
                # S 顶（窗口内最大 S）
                Stop = float("nan")
                print(f"{r_max:10.0f} {Pc_:7.3f} {Sc_*100:5.1f}% {nu_:7.3f} {r2n_:6.3f} "
                      f"{r2l_:8.3f} {Rf_:6.2f} {a_:6.1f} {tr2_:8.3f}")
