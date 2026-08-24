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
"""3D 随机侵入渗流（IP）在 DRP-374 颗粒堆积上——P2 ν 裁决对照。

标准 IP：孔隙阈值 U~U(0,1) 随机，从入口面逐级注入（占领 U≤P 且与入口连通的孔）。
S(P) = 被占领孔隙分数。3D 站点渗流 P_c≈0.31，突破时占领 n_c≈0.146。
对照：P2 预测 ν=1/2；Langmuir ν=1；IP 理论 ν=1/β≈2.4(若映射 1/β) 或相关长度 ν_p=0.88。
"""
import os
import numpy as np
from scipy import ndimage
import h5py

DATA = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\dpmp_drp374"

def load_mat(path):
    with h5py.File(path, "r") as f:
        return f["bin"][()]

def random_ip(binary, seed=0, axis=2, P_steps=200):
    """随机阈值 IP。返回 (P, S, P_c, S_c)。"""
    rng = np.random.default_rng(seed)
    nz, ny, nx = binary.shape
    U = rng.random((nz, ny, nx))
    U = np.where(binary, U, 1.0)   # 固体阈值 1（不可占）
    pore = binary.sum()
    # 阈值分桶扫描
    Ps = np.linspace(0.05, 1.0, P_steps)
    S = np.zeros(P_steps)
    sl = [slice(None)] * 3
    sl[axis] = 0
    P_c = None; S_c = None
    for i, P in enumerate(Ps):
        mask = (U <= P) & binary
        seed_m = mask.copy()
        seed_m[tuple(sl)] = mask[tuple(sl)]
        lab, _ = ndimage.label(seed_m, structure=np.ones((3, 3, 3)))
        occupied = (lab > 0).sum()
        S[i] = occupied / pore
        # 突破检测：出口面有占领
        sl2 = [slice(None)] * 3
        sl2[axis] = nz - 1
        if P_c is None and (lab[tuple(sl2)] > 0).any():
            P_c = P; S_c = S[i]
    return Ps, S, P_c, S_c

def fit_nu(P, S, S_c, name):
    """P2 形式：ΔP ∝ (S_c − S)^{−ν} → log P vs log(S_c−S)，斜率 −ν。"""
    print(f"\n===== {name} =====")
    print(f"  P_c(突破)={P_c if False else '见上'}")
    for label, lo, hi in [("全段", 0.0, 1.0), ("临界段", 0.75, 1.0)]:
        pass
    # 用数据：找 S_c 渐近（取 S 最大值或突破点）
    Sc_est = max(S_c, S[-1]) if S_c else S[-1]
    resid = Sc_est - S
    m = (resid > 0.005) & (S > 0.02)
    if m.sum() >= 6:
        X = np.log(resid[m]); Y = np.log(P[m])
        A = np.vstack([X, np.ones_like(X)]).T
        k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
        pred = k * X + b
        r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
        print(f"  幂律(S_c={Sc_est:.3f}): log P vs log(S_c−S) 斜率={k:.3f} → ν={-k:.3f}  R²={r2:.4f}")
    # 临界段（突破前 25%）
    if P_c:
        m2 = (P < P_c) & (S > 0.01)
        if m2.sum() >= 4:
            resid = S_c - S[m2]
            m3 = resid > 0.005
            if m3.sum() >= 4:
                X = np.log(resid[m3]); Y = np.log(P[m2][m3])
                A = np.vstack([X, np.ones_like(X)]).T
                k, b = np.linalg.lstsq(A, Y, rcond=None)[0]
                pred = k * X + b
                r2 = 1 - np.sum((Y - pred) ** 2) / np.sum((Y - Y.mean()) ** 2)
                print(f"  突破前段: ν={-k:.3f}  R²={r2:.4f}")

if __name__ == "__main__":
    for name, fn in [
        ("374_02_00 颗粒堆积", "374_02_00_256.mat"),
        ("374_09_01 裂缝化球堆积", "374_09_01_256.mat"),
    ]:
        p = os.path.join(DATA, fn)
        vol = load_mat(p)
        c = np.array(vol.shape) // 2; h = 48
        sub = vol[c[0]-h:c[0]+h, c[1]-h:c[1]+h, c[2]-h:c[2]+h]
        print(f"\n# {name}: 96³ 孔隙率 φ={sub.mean()*100:.1f}%")
        # 多随机种子统计
        for seed in (0, 1, 2):
            Ps, S, P_c, S_c = random_ip(sub, seed=seed)
            print(f"  种子{seed}: 突破 P_c={P_c:.3f}, S_c(突破)={S_c*100:.1f}%  "
                  f"S末={S[-1]*100:.1f}%  S(P=0.5)={S[100]*100:.1f}%")
            if seed == 0:
                fit_nu(Ps, S, S_c, f"{name} seed0")
