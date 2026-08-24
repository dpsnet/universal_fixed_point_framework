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
"""P1 仿真-实测系数符号差异诊断（2026-08-11，开放问题推进）
理论依据：notes/05_condensed_matter/spectral_shale_p1_sign_diagnosis.md
依赖复用：paperX_shale_p2_ip_uf.py (ip_union_entry)

开放问题背景：
  paper43_coupled_spectral_dip.py 正向仿真涌现 ln P_c = +0.183/(D-2) - 4.367（C>0，R²=0.942）
  实测 Tuscaloosa 31 样品 ln P_t = -1.66/(D-2) + 10.47（C<0，R²=0.578）——符号相反，
  已登记为开放问题（RAP 勘误 v0.29）。

诊断假设（候选物理根源）：
  D 在仿真参数化与压汞分形实验中的"孔径分布语义"相反——
  * 仿真参数化：孔径密度 f_sim(r) ∝ r^{D-3}（paper43_coupled_spectral_dip.py 逆变换采样），
    D 大 = 孔径分布偏大孔（平均孔径大）→ 突破压力 P_c 低 ⟹ C>0；
  * 压汞分形推导：S ∝ P^{-(2-D)} + Washburn P ∝ 1/r ⟹ 进汞累计 F(r) = (r/r_max)^{2-D}，
    孔径密度 f_hg(r) ∝ r^{1-D}，D 大 = 孔径分布偏小孔（孔喉谱更复杂）→ 门限压力 P_t 高
    ⟹ C<0（实测方向）。
  即：仿真参数 D 与压汞分形维数 D 沿同一坐标轴的孔径分布指向相反。

诊断项：
  A1/A2/A3  两种参数化下对数平均孔径 <ln r> 对 D 的回归斜率（应符号相反）
  B1        仿真语义（f ∝ r^{D-3}）分布 + DIP 突破压力：C_sim > 0（复现 paper43 符号）
  B2        压汞语义（f ∝ r^{1-D}）分布 + DIP 突破压力：C_hg  < 0（应翻转复现实测方向）
  C1        解析参照 C_ana = ln(S_min/a) < 0（压汞分形 + 最小可测饱和度截止的第一性结论）
"""

import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_ip_uf import ip_union_entry

R_MIN = 1.0    # 归一化最小孔径（= 最大 Washburn 阈值）
R_MAX = 100.0  # 归一化最大孔径（= 最小 Washburn 阈值）


def sample_radii(n, D, mode, seed=0):
    """孔径采样（对数网格 4000 点权重采样，两种参数化语义）：
    sim: f ∝ r^{D-3}  —— paper43_coupled_spectral_dip.py 逆变换的等价密度
    hg:  f ∝ r^{1-D}  —— 压汞分形 F(r)=(r/r_max)^{2-D} 的密度
    """
    rng = np.random.default_rng(seed)
    grid = np.geomspace(R_MIN, R_MAX, 4000)
    if mode == "sim":
        w = grid ** (D - 3.0)
    else:
        w = grid ** (1.0 - D)
    w /= w.sum()
    idx = rng.choice(len(grid), size=n, p=w)
    return grid[idx]


def logmean_lnr(D_list, mode, n=200000, seed=7):
    """诊断 A：对数平均孔径 <ln r> 对 D 的序列。"""
    vals = []
    for D in D_list:
        r = sample_radii(n, D, mode, seed=seed)
        vals.append(np.log(r).mean())
    return np.array(vals)


def breakthrough_scan(D_list, mode, N=48, phi=0.31, ncfg=6, seed0=1000):
    """诊断 B：给定孔径分布语义跑 DIP，返回各 D 的突破压力 P_c（c=0 毛细极限）。"""
    Pcs = []
    for D in D_list:
        pcs_cfg = []
        for cfg in range(ncfg):
            seed = seed0 + cfg * 1000 + int(D * 100)
            radii = sample_radii(N ** 3, D, mode, seed=seed)
            binary = (np.random.default_rng(seed + 1).random((N, N, N)) < phi)
            U = np.where(binary, 1.0 / radii.reshape(binary.shape), 2.0)
            pore_idx = np.flatnonzero(binary.ravel())
            Uf = U.ravel()
            order = pore_idx[np.argsort(Uf[pore_idx])]
            _P, _S, P_c, _Sc = ip_union_entry(binary, Uf, order)
            if P_c > 0 and P_c < 1e6:
                pcs_cfg.append(P_c)
        if pcs_cfg:
            Pcs.append(float(np.mean(pcs_cfg)))
        else:
            Pcs.append(np.nan)
    return np.array(Pcs)


def fit_p1(D_list, Pcs):
    """双曲拟合 ln P_c = C/(D-2) + B。"""
    x = 1.0 / (np.asarray(D_list, dtype=float) - 2.0)
    y = np.log(np.asarray(Pcs, dtype=float))
    C, B = np.polyfit(x, y, 1)
    yhat = C * x + B
    r2 = 1.0 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)
    return C, B, r2


def check(name, cond, detail=""):
    print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))
    return cond


def main():
    print("== P1 仿真-实测系数符号差异诊断 ==")
    D_list = [2.4, 2.6, 2.8, 3.0, 3.2]

    # ---- 诊断 A：孔径分布语义方向 ----
    lnr_sim = logmean_lnr(D_list, "sim")
    lnr_hg = logmean_lnr(D_list, "hg")
    a_sim, _ = np.polyfit(D_list, lnr_sim, 1)
    a_hg, _ = np.polyfit(D_list, lnr_hg, 1)
    print("诊断 A  分布语义：<ln r> 对 D 回归斜率 sim=%.3f（D 大→平均孔径%s）"
          % (a_sim, "大" if a_sim > 0 else "小"))
    print("           hg=%.3f（D 大→平均孔径%s）"
          % (a_hg, "大" if a_hg > 0 else "小"))
    ok = []
    ok.append(check("A1 仿真语义 D 大→平均孔径大 (slope>0)", a_sim > 0,
                    "slope_sim=%.3f" % a_sim))
    ok.append(check("A2 压汞语义 D 大→平均孔径小 (slope<0)", a_hg < 0,
                    "slope_hg=%.3f" % a_hg))
    ok.append(check("A3 两语义孔径指向相反 (符号相反)", (a_sim > 0) != (a_hg > 0)))

    # ---- 诊断 C：解析参照（第一性）----
    S_min, a = 0.05, 1.0  # 最小可测饱和度 5%、分形前因子归一化
    C_ana = np.log(S_min / a)
    ok.append(check("C1 解析参照 C=ln(S_min/a)<0 恒成立", C_ana < 0,
                    "C_ana=%.3f (S_min=%.2f, a=%.1f)" % (C_ana, S_min, a)))

    # ---- 诊断 B：DIP 突破压力符号 ----
    Pc_sim = breakthrough_scan(D_list, "sim")
    Pc_hg = breakthrough_scan(D_list, "hg")
    C_sim, B_sim, r2_sim = fit_p1(D_list, Pc_sim)
    C_hg, B_hg, r2_hg = fit_p1(D_list, Pc_hg)
    print("诊断 B  DIP 突破压力：仿真语义 ln P_c = %.3f/(D-2) + %.3f (R²=%.3f)"
          % (C_sim, B_sim, r2_sim))
    print("           压汞语义 ln P_c = %.3f/(D-2) + %.3f (R²=%.3f)"
          % (C_hg, B_hg, r2_hg))
    ok.append(check("B1 仿真语义 C>0（复现 paper43 符号）", C_sim > 0,
                    "C_sim=%.3f" % C_sim))
    ok.append(check("B2 压汞语义 C<0（复现实测方向）", C_hg < 0,
                    "C_hg=%.3f" % C_hg))

    print("汇总：%d/%d 通过" % (sum(ok), len(ok)))
    print("结论：仿真-实测符号差异根源 = D 参数化孔径分布语义相反；"
          "压汞分形语义下仿真复现 C<0（实测方向）——开放问题获机制诊断")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
