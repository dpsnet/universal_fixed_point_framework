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
"""动态侵入渗流（DIP）：粘性-毛细竞争对 P2 型 ν 的影响（t4c）。

物理（Wilkinson 1984 梯度 IP 的简化闭合形式）：恒定注入速率下，前沿孔隙 i 的
局部有效压力 = 注入压 − 粘性压降，侵入判据 U_i + c·R_path(i) ≤ P_drive。
即动态 IP ≈ 用"有效阈值" U_eff(i) = U_i + c·R_path(i) 的准静态 IP：
  - c → 0（毛细极限）：按裸朗缪尔阈值排序 → P2-6f 的 ν=1 支
  - c 大（粘性极限）：按阻力路径排序（孔径主导）→ ν 是否被改写
  - c = Ca 数代理（粘性力/毛细力）

R_path(i) = 孔隙 i 到入口面(x=0) 的最小累积阻力路径（Bellman-Ford 松弛）。
阻力模型：r_i = 1（均匀）或 r_i ∝ U_i（小孔高阻，毛细阈与阻力相关）。

输出：各 c 的 P_c、S_c、P2 型 ν（突破后窗口），判定动态是否改写 ν。
"""
import numpy as np
from numba import njit
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_ip_uf import ip_union_entry

A = 1.09  # 东营 ΔP_L (MPa)

@njit
def bellman_ford_path_resistance(binary, r, nx, ny, nz):
    """多源松弛：R[i] = 孔隙 i 到入口面 (z=0 孔隙，与 ip_union_entry 一致) 的最小累积阻力路径。
    返回 R（未连通孔隙保持大值）。"""
    n = nx * ny * nz
    R = np.full(n, 1e12)
    # 入口面 z=0（flat 索引 = y*nx + x）
    for y in range(ny):
        for x in range(nx):
            idx = y * nx + x
            if binary[idx]:
                R[idx] = r[idx]
    # 松弛（Bellman-Ford：2·nz 轮覆盖 26 邻连通域直径，changed 提前终止）
    for _ in range(2 * nz):
        changed = False
        for z in range(nz):
            for y in range(ny):
                for x in range(nx):
                    idx = z*ny*nx + y*nx + x
                    if not binary[idx]:
                        continue
                    base = R[idx]
                    if base >= 1e11:
                        continue
                    # 26 邻（与 ip_union_entry 的邻居集合严格一致）
                    for dz in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            for dx in (-1, 0, 1):
                                if dz == 0 and dy == 0 and dx == 0:
                                    continue
                                zz, yy, xx = z+dz, y+dy, x+dx
                                if 0 <= zz < nz and 0 <= yy < ny and 0 <= xx < nx:
                                    j = zz*ny*nx + yy*nx + xx
                                    if binary[j]:
                                        cand = base + r[j]
                                        if cand < R[j]:
                                            R[j] = cand
                                            changed = True
        if not changed:
            break
    return R

def langmuir_thresholds(binary, seed=0, a=A):
    """每孔隙朗缪尔隐含阈值 U=a·T/(1−T)。固体处 2.0（占位）。"""
    rng = np.random.default_rng(seed + 1000)
    T = rng.random(binary.shape)
    U = a * T / (1.0 - T)
    return np.where(binary, U, 2.0)

def run_dip(binary, c, seed=0, res_model=0):
    """动态 IP：有效阈值 U_eff = U + c·R_path，按 U_eff 排序的标准 IP。
    res_model=0：均匀阻力；1：阻力∝阈值（小孔高阻）。"""
    U3d = langmuir_thresholds(binary, seed=seed)
    if res_model == 0:
        r = np.ones(binary.shape)
    else:
        r = 0.5 + U3d  # 阈值越大（孔越小）阻力越大
    nz, ny, nx = binary.shape
    R = bellman_ford_path_resistance(binary.ravel(), r.ravel(), nx, ny, nz).reshape(binary.shape)
    Ueff = U3d + c * R
    pore_idx = np.flatnonzero(binary.ravel())
    Uf = Ueff.ravel()
    order = pore_idx[np.argsort(Uf[pore_idx])]
    return ip_union_entry(binary, Uf, order)

def p2nu(P, S, Pc, Pmax=None):
    """P2 型 ν：log P vs log(1−S)，限突破后窗口 P∈(P_c, Pmax]。
    Pmax=None → 自适应取模拟压力上限（粘性极限 P_c 远超东营 3.01 窗口）。"""
    resid = 1.0 - S
    if Pmax is None:
        Pmax = P.max()
    m2 = (resid > 0.01) & (P > Pc) & (P <= Pmax)
    if m2.sum() < 10:
        return None
    X = np.log(resid[m2]); Y = np.log(P[m2])
    A_ = np.vstack([X, np.ones_like(X)]).T
    k, b = np.linalg.lstsq(A_, Y, rcond=None)[0]
    pred = k * X + b
    r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
    return -k, r2

def p2nu_split(P, S, Pc, Pmax=None):
    """P2 型 ν 分支验证：突破后窗口按 log P 中位分两段。
    低段=突破暂态（P 近 P_c）、高段=饱和趋近（P 远 P_c）；
    ν_lo≠ν_hi 且各自 R² 高 → 两段幂律分支（S(P) 非单幂律）。
    返回 (整体ν, 整体R², ν_lo, R²_lo, ν_hi, R²_hi)。"""
    resid = 1.0 - S
    if Pmax is None:
        Pmax = P.max()
    m2 = (resid > 0.01) & (P > Pc) & (P <= Pmax)
    if m2.sum() < 20:
        return None
    X = np.log(resid[m2]); Y = np.log(P[m2])
    A_ = np.vstack([X, np.ones_like(X)]).T
    k, b = np.linalg.lstsq(A_, Y, rcond=None)[0]
    r2 = 1 - np.sum((Y - (k*X + b)) ** 2) / np.sum((Y - Y.mean()) ** 2)

    def fit(mask):
        Xs, Ys = X[mask], Y[mask]
        if Xs.size < 8:
            return np.nan, np.nan
        As = np.vstack([Xs, np.ones_like(Xs)]).T
        ks, bs = np.linalg.lstsq(As, Ys, rcond=None)[0]
        r2s = 1 - np.sum((Ys - (ks*Xs + bs)) ** 2) / np.sum((Ys - Ys.mean()) ** 2)
        return -ks, r2s

    med = np.median(Y)
    nlo, r2lo = fit(Y <= med)
    nhi, r2hi = fit(Y > med)
    return -k, r2, nlo, r2lo, nhi, r2hi

if __name__ == "__main__":
    n = 64
    ncfg = 8
    PC_CAP = 1e6  # 真突破判据：入口-出口存在有效路径时 P_c~c·R_max(≤211·10)+U_max；1e12 为无路径伪突破
    for phi in (0.31, 0.40):
        print(f"\n动态 IP（DIP）: {n}³ φ={phi} ncfg={ncfg} 朗缪尔阈值 a={A}（真突破判据 P_c<{PC_CAP:.0e}）")
        print("=" * 78)
        for res_model, rlabel in ((0, "均匀阻力"), (1, "阻力∝阈值")):
            print(f"\n--- 阻力模型：{rlabel} ---")
            print(f"{'c(Ca代理)':>10} {'P_c':>8} {'S_c':>7} {'P2型ν':>8} {'ν R²':>7} {'真突破':>5}  {'ν(c)/ν(0)':>9}")
            nu0 = None
            for c in (0.0, 0.3, 1.0, 3.0, 10.0):
                Pcs, Scs, nus, r2s = [], [], [], []
                nbreak = 0
                for cfg in range(ncfg):
                    rng = np.random.default_rng(cfg)
                    binary = rng.random((n, n, n)) < phi
                    P, S, Pc, Sc = run_dip(binary, c, seed=cfg, res_model=res_model)
                    if Pc < 0 or Pc > PC_CAP:
                        continue  # 无贯通路径 → 伪突破
                    nbreak += 1
                    nu = p2nu(P, S, Pc)
                    if nu:
                        Pcs.append(Pc); Scs.append(Sc)
                        nus.append(nu[0]); r2s.append(nu[1])
                if not Pcs:
                    print(f"{c:10.1f} 无真突破")
                    continue
                Pc_ = np.mean(Pcs); Sc_ = np.mean(Scs)
                nu_ = np.mean(nus); r2_ = np.mean(r2s)
                if c == 0.0:
                    nu0 = nu_
                ratio = nu_ / nu0 if (nu0 and nu0 > 0) else float("nan")
                tag = "" if r2_ > 0.7 else "  ← 无幂律"
                print(f"{c:10.1f} {Pc_:8.3f} {Sc_*100:6.1f}% {nu_:8.3f} {r2_:7.3f} {nbreak:5d}  {ratio:9.3f}{tag}")

    # ========== c=1 分支行为验证（用户指定项） ==========
    print("\n" + "=" * 78)
    print(f"c=1 分支行为验证（{n}³ ncfg=16）：突破后窗口按 log P 中位分两段")
    print("  低段=突破暂态(P→P_c) / 高段=饱和趋近(P远) ；ν_lo≠ν_hi → 两段幂律分支")
    print("=" * 78)
    for res_model, rlabel in ((0, "均匀阻力"), (1, "阻力∝阈值")):
        for phi in (0.31, 0.40):
            rows = []
            for cfg in range(16):
                rng = np.random.default_rng(cfg)
                binary = rng.random((n, n, n)) < phi
                P, S, Pc, Sc = run_dip(binary, 1.0, seed=cfg, res_model=res_model)
                if Pc < 0 or Pc > PC_CAP:
                    continue
                r_ = p2nu_split(P, S, Pc)
                if r_:
                    rows.append(r_)
            if not rows:
                print(f"[{rlabel} φ={phi}] 无真突破")
                continue
            rows = np.array(rows)
            nu, r2, nlo, r2lo, nhi, r2hi = rows.mean(0)
            tag = "** 两段分支 **" if (abs(nlo - nhi) > 0.15 and r2lo > 0.8 and r2hi > 0.8) else ""
            print(f"[{rlabel} φ={phi} n={len(rows)}] 整体ν={nu:.3f}(R²{r2:.3f}) | "
                  f"低段ν_lo={nlo:.3f}(R²{r2lo:.3f}) 高段ν_hi={nhi:.3f}(R²{r2hi:.3f}) | 差={nlo-nhi:+.3f} {tag}")
