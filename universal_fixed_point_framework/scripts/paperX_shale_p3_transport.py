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
"""P3 突破通道维数-输运量耦合检验（2026-08-11，开放问题推进）
理论依据：notes/05_condensed_matter/spectral_shale_accumulation.md（P3 输运耦合开放项登记）
依赖复用：paper43_coupled_spectral_dip.py

开放问题（笔记 L225 登记）：
  "输运耦合为开放项：D_b 与输运量（泄压时间 τ、饱和度剖面推进）的显式耦合未展开，
   '维数-输运无关'零假设未检验。"

零假设 H0："维数-输运无关"——突破通道盒计数维数 D_b(red)（s-t 路径拓扑不变量）与
输运量（突破后饱和度推进的激活事件数 τ_tr）不相关。

物理预期（红键为拓扑不变量，D 无关）：
  * D_b(red) 与 D 无关（已建立，理论 0.854）
  * 输运量 τ_tr 由孔径分布/连通度决定 → 应与 D 相关
  若 ρ(τ_tr, D_b(red)) ≈ 0 而 ρ(τ_tr, D) ≠ 0 ⟹ 零假设成立：输运不由通道维数决定
  （维数刻画"路径拓扑结构"，输运由"分布+连通度"决定，二者解耦）

输运量定义（IP 时间代理）：
  τ_tr = 突破后至饱和度 0.5 的激活事件数（每孔激活一步=时间单位；事件少=大跳跃快输运）
  avg_jump = 突破后平均每事件饱和度增量（快输运 = 大跳跃）
"""

import numpy as np
import os
import sys
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper43_coupled_spectral_dip import (
    fractal_pore_network,
    run_fractal_dip,
    spectral_band_mapping,
    extract_p3,
)


def transport_metrics(S_arr, S_c, target=0.5):
    """输运量：突破后至 target 饱和度的激活事件数（时间代理）+ 平均跳跃。"""
    events_after = S_arr[S_arr > S_c + 1e-9]
    sub = events_after[events_after <= target + 1e-9]
    tau_tr = float(len(sub))
    if len(sub) > 0:
        avg_jump = float((sub[-1] - S_c) / len(sub))
    else:
        avg_jump = np.nan
    return tau_tr, avg_jump


def run_config(N, phi, D, c, seed):
    binary, radii, lambdas, U = fractal_pore_network(N, phi, D, seed=seed)
    P_arr, S_arr, P_c, S_c, order, Uf = run_fractal_dip(binary, U, c=c, seed=seed)
    if P_c < 0 or P_c > 1e6:
        return None
    pressures, A_t, lam_edges, snapshots = spectral_band_mapping(binary, lambdas, P_arr, P_c, Uf)
    Db_c, r2_c, Db_b, r2_b, Db_b1, r2_b1, Db_rd, r2_rd = extract_p3(snapshots, pressures, P_c)
    if np.isnan(Db_rd):
        return None
    tau_tr, avg_jump = transport_metrics(S_arr, S_c)
    return dict(D=D, P_c=P_c, S_c=S_c, tau_tr=tau_tr, avg_jump=avg_jump, Db_red=Db_rd, r2_rd=r2_rd)


def main():
    print("== P3 突破通道维数-输运量耦合检验（零假设 H0：维数-输运无关） ==")
    N, PHI, C, NCFG = 48, 0.31, 0.0, 12
    D_LIST = [2.4, 2.8, 3.2]

    rows = []
    for D in D_LIST:
        for cfg in range(NCFG):
            seed = cfg * 1000 + int(D * 100)
            r = run_config(N, PHI, D, C, seed)
            if r is not None and np.isfinite(r["avg_jump"]):
                rows.append(r)

    D_arr = np.array([r["D"] for r in rows])
    Pc_arr = np.array([r["P_c"] for r in rows])
    Sc_arr = np.array([r["S_c"] for r in rows])
    tau_arr = np.array([r["tau_tr"] for r in rows])
    jump_arr = np.array([r["avg_jump"] for r in rows])
    Db_arr = np.array([r["Db_red"] for r in rows])

    print("有效配置 n=%d（D∈%s, c=0, N=%d, φ=%.2f）" % (len(rows), D_LIST, N, PHI))
    print("分组均值表（D | τ_tr | avg_jump | D_b(red) | P_c | S_c）")
    for D in D_LIST:
        m = rows and [r for r in rows if r["D"] == D] or []
        if not m:
            continue
        print("  D=%.1f：τ_tr=%.0f±%.0f，avg_jump=%.4f±%.4f，D_b(red)=%.3f±%.3f，P_c=%.4f，S_c=%.2f"
              % (D, np.mean([r["tau_tr"] for r in m]), np.std([r["tau_tr"] for r in m]),
                 np.mean([r["avg_jump"] for r in m]), np.std([r["avg_jump"] for r in m]),
                 np.mean([r["Db_red"] for r in m]), np.std([r["Db_red"] for r in m]),
                 np.mean([r["P_c"] for r in m]), np.mean([r["S_c"] for r in m])))

    # Spearman 相关矩阵
    print("Spearman 相关矩阵（n=%d）" % len(rows))
    names = ["D", "P_c", "S_c", "tau_tr", "avg_jump", "Db_red"]
    vals = [D_arr, Pc_arr, Sc_arr, tau_arr, jump_arr, Db_arr]
    corr = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            rho, p = stats.spearmanr(vals[i], vals[j])
            corr[(names[i], names[j])] = (rho, p)
            star = "**" if p < 0.01 else ("*" if p < 0.05 else "")
            print("  ρ(%s, %s)=%+.3f (p=%.3f)%s" % (names[i], names[j], rho, p, star))

    rho_tau_db, p_tau_db = corr[("tau_tr", "Db_red")]
    rho_tau_D, _ = corr[("D", "tau_tr")]
    rho_Db_D, _ = corr[("D", "Db_red")]
    rho_tau_Pc, _ = corr[("P_c", "tau_tr")]

    print("结论：")
    print("  ρ(τ_tr, D_b(red))=%+.3f（p=%.3f）——零假设" % (rho_tau_db, p_tau_db))
    if abs(rho_tau_db) < 0.3:
        print("  ⟹ H0 '维数-输运无关' 支持：输运量 τ_tr 与通道维数 D_b(red) 无显著相关")
    else:
        print("  ⟹ H0 被否：输运量与通道维数存在耦合")
    print("  旁证：ρ(τ_tr, D)=%+.3f，ρ(D_b(red), D)=%+.3f（红键拓扑不变量），ρ(τ_tr, P_c)=%+.3f"
          % (rho_tau_D, rho_Db_D, rho_tau_Pc))
    if abs(rho_tau_db) < 0.3 and abs(rho_tau_D) > 0.3 and abs(rho_Db_D) < 0.3:
        print("  结构：输运由 D 决定而通道维数 D_b(red) 与 D 无关 ⟹ 维数与输运解耦（输运由分布/连通度主导）")

    ok = [abs(rho_tau_db) < 0.3]
    print("[%s] 判定：ρ(τ_tr, D_b(red)) 弱（|ρ|<0.3）" % ("PASS" if ok[0] else "FAIL"))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
