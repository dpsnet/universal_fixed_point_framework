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
"""DRP-374 颗粒堆积介质毛管扫描（离心实验合成孪生）——P2 ν 裁决前置。

物理：离心实验 = 逐级增大离心力，油从越来越小的孔排出（准静态毛管驱替）。
      EDT 孔径代理 + 阈值注入 = 同一物理的数值实现。
      P  ∝ 1/r_thr，S(P) = 注入连通体积分数。

产出：高分辨率 S(P) → 形态判定（饱和型 Langmuir ν=1 vs 幂律临界 ν=1/2）。
"""
import sys
import numpy as np
from scipy import ndimage
import h5py

DATA = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\dpmp_drp374"

def load_mat(path, key="bin"):
    with h5py.File(path, "r") as f:
        return f[key][()]

def edt_pore_saturation(binary, pmin=1.0, nsteps=400, scale="log", axis=2):
    """逐级毛管注入扫描。binary: 1=孔隙, 0=固体。返回 (P_grid, S_grid)。
    P ∝ 1/r，r 从大到小（先注入大孔）。
    """
    # 距离变换（孔隙到固体边界的距离，单位体素）
    dt = ndimage.distance_transform_edt(binary)
    rmax, rmin = dt.max(), pmin
    if scale == "log":
        rs = np.geomspace(rmax, rmin, nsteps)
    else:
        rs = np.linspace(rmax, rmin, nsteps)
    # 注入连通标记：从入口面 (z=axis) 26-连通
    nz, ny, nx = binary.shape
    slices = [slice(None)] * 3
    S = np.zeros_like(rs)
    P = 1.0 / rs
    prev = np.zeros_like(binary, dtype=bool)
    for i, r in enumerate(rs):
        mask = (dt >= r) & binary
        # 入口面种子
        sl = slices.copy()
        sl[axis] = 0
        seed = mask.copy()
        seed[tuple(sl)] = mask[tuple(sl)]
        # 连通域（用 mask 限制，上次结果作初始可加速）
        lab, _ = ndimage.label(seed, structure=np.ones((3, 3, 3)))
        S[i] = (lab > 0).sum() / max(binary.sum(), 1)
        prev = seed
    return P, S

def analyze(P, S, name, S_c=None):
    """形态判定：Langmuir (ν=1, 饱和型) vs 幂律临界 (ν=1/2)。"""
    print(f"\n===== {name}  n={len(S)} =====")
    print(f"   P 范围 [{P.min():.3f}, {P.max():.3f}]  S 范围 [{S.min()*100:.1f}%, {S.max()*100:.1f}%]")
    # 1) 阶梯数（注入台阶 = 有效离散孔隙尺寸族）
    dS = np.diff(S)
    steps = (np.abs(dS) > 1e-4).sum()
    print(f"   有效注入台阶数: {steps} / {len(S)-1}")
    # 2) Langmuir 双倒数线性化：1/S vs 1/P
    m = S > 0.01
    if m.sum() >= 4:
        X = 1.0 / P[m]
        Y = 1.0 / S[m]
        A = np.vstack([X, np.ones_like(X)]).T
        k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
        pred = k * X + b
        r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
        print(f"   Langmuir 双倒数 1/S vs 1/P: R²={r2:.4f}  (k={k:.4f}, b={b:.4f})")
    # 3) 幂律临界：log P vs log(S_c - S)
    if S_c is not None:
        resid = S_c - S
        m2 = (resid > 1e-3) & (S > 0.01)
        if m2.sum() >= 4:
            X = np.log(resid[m2])
            Y = np.log(P[m2])
            A = np.vstack([X, np.ones_like(X)]).T
            k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
            pred = k * X + b
            r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
            print(f"   幂律临界 log P vs log(S_c−S): 斜率={k:.3f} → ν={-k:.3f}  R²={r2:.4f}")

if __name__ == "__main__":
    # 候选介质（颗粒堆积 / 球堆积 / 裂缝化）
    candidates = {
        "374_02_00 (颗粒堆积-00)": "374_02_00_256.mat",
        "374_02_04 (颗粒堆积-04)": "374_02_04_256.mat",
        "374_09_01 (裂缝化球堆积)": "374_09_01_256.mat",
        "374_05_00 (Fractured Carbonate)": "374_05_00_256.mat",
    }
    for name, fn in candidates.items():
        try:
            import os
            p = os.path.join(DATA, fn)
            if not os.path.exists(p):
                print(f"缺文件: {fn}")
                continue
            vol = load_mat(p)
            print(f"\n# {name}: {vol.shape}, 孔隙率 φ={vol.mean()*100:.1f}%")
            # 中心 96³ 子块
            c = np.array(vol.shape) // 2
            h = 48
            sub = vol[c[0]-h:c[0]+h, c[1]-h:c[1]+h, c[2]-h:c[2]+h]
            print(f"  子块 96³ 孔隙率={sub.mean()*100:.1f}%")
            # 检查三向连通
            P, S = edt_pore_saturation(sub)
            analyze(P, S, name, S_c=1.0)
        except Exception as e:
            print(f"#{name} 失败: {e}")
