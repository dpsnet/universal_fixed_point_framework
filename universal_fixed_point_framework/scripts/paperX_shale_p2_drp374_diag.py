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
"""DRP-374 毛管扫描诊断：连通性效应 vs 几何孔径分布退化。

判定：S_conn(P)（连通注入）与 S_global(P)（忽略连通、全部≥r 孔隙体积）
是否差异显著。
- 若 S_conn ≈ S_global → 指数为孔径分布几何形态（退化，无裁决力，P2-0 教训）
- 若 S_conn 明显滞后且存在 S_c<1 渐近 → 连通/临界效应显著（值得 LBM 动力学）
"""
import os
import numpy as np
from scipy import ndimage
import h5py

DATA = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\dpmp_drp374"

def load_mat(path):
    with h5py.File(path, "r") as f:
        return f["bin"][()]

def scan(binary, axis=2, nsteps=300):
    dt = ndimage.distance_transform_edt(binary)
    rmax, rmin = dt.max(), 0.5
    rs = np.geomspace(rmax, rmin, nsteps)
    S_conn = np.zeros(nsteps)
    S_glob = np.zeros(nsteps)
    total_pore = max(binary.sum(), 1)
    sl = [slice(None)] * 3
    sl[axis] = 0
    for i, r in enumerate(rs):
        mask = (dt >= r) & binary
        # 全局（忽略连通）
        S_glob[i] = mask.sum() / total_pore
        # 连通注入（入口面种子 26-连通）
        seed = mask.copy()
        seed[tuple(sl)] = mask[tuple(sl)]
        lab, _ = ndimage.label(seed, structure=np.ones((3, 3, 3)))
        S_conn[i] = (lab > 0).sum() / total_pore
    P = 1.0 / rs
    return P, S_conn, S_glob

def diagnose(P, S_conn, S_glob, name):
    print(f"\n===== {name} =====")
    # 渐进值
    print(f"  P 末端: S_conn→{S_conn[-1]*100:.1f}%, S_glob→{S_glob[-1]*100:.1f}% (φ={S_glob[-1]:.3f})")
    # 连通滞后区（S_conn < S_glob 显著 1% 以上）
    lag = (S_glob - S_conn) > 0.01
    if lag.sum():
        print(f"  连通滞后区: P ∈ [{P[lag].min():.3f}, {P[lag].max():.3f}], "
              f"S_conn 滞后幅度 max {np.max(S_glob-S_conn)*100:.1f}%")
    else:
        print("  无显著连通滞后 —— S_conn≈S_glob，指数为几何退化")
    # S_conn 的临界渐近（最后 30% 台阶增量）
    n = len(S_conn)
    tail = slice(int(0.7*n), n)
    dS = np.diff(S_conn)[int(0.7*n)-1:]
    print(f"  高压端(后30%)台阶数: {(np.abs(dS) > 1e-4).sum()}  S_conn 增量累计 {S_conn[n-1]-S_conn[int(0.7*n)]:.3f}")
    # 幂律拟合（数据驱动 S_c = S_conn[-1]）
    Sc = S_conn[-1]
    resid = Sc - S_conn
    m = (resid > 1e-3) & (S_conn > 0.02)
    if m.sum() >= 5:
        X = np.log(resid[m]); Y = np.log(P[m])
        A = np.vstack([X, np.ones_like(X)]).T
        k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
        pred = k * X + b
        r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
        print(f"  幂律(S_c={Sc:.3f}): ν={-k:.3f}  R²={r2:.4f}")

if __name__ == "__main__":
    for name, fn in [
        ("374_02_00 颗粒堆积", "374_02_00_256.mat"),
        ("374_09_01 裂缝化球堆积", "374_09_01_256.mat"),
    ]:
        p = os.path.join(DATA, fn)
        vol = load_mat(p)
        c = np.array(vol.shape) // 2; h = 48
        sub = vol[c[0]-h:c[0]+h, c[1]-h:c[1]+h, c[2]-h:c[2]+h]
        P, Sc_, Sg = scan(sub)
        diagnose(P, Sc_, Sg, f"{name} (96³, φ={sub.mean()*100:.1f}%)")
