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
"""
P3 实际成像数据盒计数检验：DPMP DRP-374 裂缝介质（Santos et al., 2022, Data in Brief 40:107797）
数据：374_05_00_256.mat（Fractured Carbonate）/ 374_08_00_256.mat（Realistic Fracture）
     256^3 二值体，相 0 = 裂缝/孔隙（单一贯通连通域，= 渗流骨架/贯通通道）

协议（对应论文 P3 检验协议）：
  (1) 识别贯通通道：相 0 中最大的单连通域（已由 prelim 脚本确认全贯通）；
  (2) 3D 盒计数贯通通道 → D_3d（对照"裂缝网络 D∈(2,3)"类别，不应与 0.6309 直接比较）；
  (3) 中心线（每层质心）提取 → 骨架 3D 盒计数 → D_skel（准一维通道，D∈(1,2)）；
  (4) 中心线沿 x/y 的 1D 投影盒计数 → D_1d（Cantor 型截面检验，与 ln2/ln3≈0.6309 对比）；
  (5) 中心线在 x-y 截面 2D 盒计数 → D_2d。

诚实声明：数据为合成裂缝介质（非页岩真实微 CT），结果作方法学/结构演示与初始检验，
      不能替代真实页岩 FMI/微 CT 检验。
"""
import sys
import h5py
import numpy as np


def load(path):
    with h5py.File(path, "r") as f:
        return f["bin"][()]


def boxcount_3d(mask, eps_list):
    """3D 盒计数：N(eps) = 含占据体元的 (eps)^3 盒数。"""
    res = []
    for eps in eps_list:
        nb = 0
        for i in range(0, mask.shape[0], eps):
            for j in range(0, mask.shape[1], eps):
                for k in range(0, mask.shape[2], eps):
                    if mask[i:i + eps, j:j + eps, k:k + eps].any():
                        nb += 1
        res.append((eps, nb))
    return res


def boxcount_1d(pts, span, eps_list):
    """1D 盒计数：覆盖 pts（0..span 的位置集合）的 eps 区间数。"""
    res = []
    for eps in eps_list:
        covered = np.zeros(span // eps + 1, dtype=bool)
        for p in pts:
            covered[int(p // eps)] = True
        res.append((eps, int(covered.sum())))
    return res


def boxcount_2d(pts, span, eps_list):
    """2D 盒计数：覆盖 pts（平面点集）的 eps^2 盒数。"""
    res = []
    m = span // eps_list[0] + 1
    for eps in eps_list:
        covered = np.zeros((span // eps + 1, span // eps + 1), dtype=bool)
        for (px, py) in pts:
            covered[int(px // eps), int(py // eps)] = True
        res.append((eps, int(covered.sum())))
    return res


def fit_dim(eps_list, counts, lo_idx=0, hi_idx=None):
    lx = np.log(np.asarray(eps_list[lo_idx:hi_idx], dtype=float))
    ly = np.log(np.asarray(counts[lo_idx:hi_idx], dtype=float))
    k, b = np.polyfit(lx, ly, 1)
    # 拟合优度（决定系数）
    yhat = k * lx + b
    ss_res = ((ly - yhat) ** 2).sum()
    ss_tot = ((ly - ly.mean()) ** 2).sum()
    return -k, 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def analyze(path, label):
    d = load(path)
    frac = (d == 0)
    print("=" * 70)
    print("FILE:", label)
    print("  裂缝相（相 0）：%d 体元，占比 %.4f" % (frac.sum(), frac.mean()))

    # (2) 3D 盒计数（裂缝网络类别）
    eps3 = [2, 4, 8, 16, 32, 64, 128]
    bc3 = boxcount_3d(frac, eps3)
    d3, r3 = fit_dim(eps3, [n for _, n in bc3])
    print("  [2] 3D 盒计数（裂缝网络）：D_3d = %.3f（R²=%.4f）" % (d3, r3))
    print("       逐尺度 N(eps):", [(e, n) for e, n in bc3])

    # (3) 中心线（沿 z 每层质心，仅裂缝占据层）
    zs, xs, ys = [], [], []
    for z in range(frac.shape[2]):
        sl = frac[:, :, z]
        if sl.any():
            ys_, xs_ = np.where(sl)
            xs.append(xs_.mean()); ys.append(ys_.mean()); zs.append(z)
    n_occ = len(zs)
    print("  中心线：%d/256 层有裂缝占据" % n_occ)
    if n_occ < 8:
        print("  !! 裂缝层过少，骨架盒计数不可靠，跳过")
        return

    # 中心线 3D 盒计数（准一维通道）
    skel = np.zeros_like(frac, dtype=bool)
    for z, x, y in zip(zs, xs, ys):
        skel[int(x), int(y), z] = True
    bcsk = boxcount_3d(skel, eps3)
    dsk, rsk = fit_dim(eps3, [n for _, n in bcsk])
    print("  [3] 中心线骨架 3D 盒计数：D_skel = %.3f（R²=%.4f）" % (dsk, rsk))

    # (4) 中心线 1D 投影盒计数（Cantor 型检验，与 0.6309 对比）
    span = frac.shape[0]
    eps1 = [2, 4, 8, 16, 32, 64, 128]
    bcx = boxcount_1d(xs, span, eps1)
    bcy = boxcount_1d(ys, span, eps1)
    dx, rx = fit_dim(eps1, [n for _, n in bcx])
    dy, ry = fit_dim(eps1, [n for _, n in bcy])
    print("  [4] 中心线 1D 投影盒计数：")
    print("       沿 x 投影：D_1d,x = %.4f（R²=%.4f）  vs  P3 理论 0.6309" % (dx, rx))
    print("       沿 y 投影：D_1d,y = %.4f（R²=%.4f）  vs  P3 理论 0.6309" % (dy, ry))
    for nm, dd in [("x", dx), ("y", dy)]:
        rel = (dd - 0.6309) / 0.6309
        verdict = "偏离 %.1f%%（>10%%，不直接支持）" % (rel * 100)
        if abs(rel) <= 0.10:
            verdict = "偏差 %.1f%%（≤10%%，与 P3 同量级）" % (rel * 100)
        print("       → %s：%s" % (nm, verdict))

    # (5) 中心线 x-y 截面 2D 盒计数
    bcxy = boxcount_2d(list(zip(xs, ys)), span, eps1)
    dxy, rxy = fit_dim(eps1, [n for _, n in bcxy])
    print("  [5] 中心线 x-y 截面 2D 盒计数：D_2d = %.4f（R²=%.4f）" % (dxy, rxy))

    print("  [汇总] D_3d=%.3f（裂缝网络，D∈(2,3) 类别）｜D_skel=%.3f（骨架）｜"
          "D_1d={x:%.3f,y:%.3f}（Cantor 截面检验）｜D_2d=%.3f" % (d3, dsk, dx, dy, dxy))
    print("        P3 理论 0.6309 属 1D 截面 Cantor 类别，仅与 D_1d 比较；D_3d/D_skel/D_2d 为类别对照。")
    print()


def main():
    import glob
    import os
    db = np.log(2) / np.log(3)
    print("P3 理论值 D_b = ln2/ln3 = %.4f" % db)
    files = []
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            if os.path.isdir(a):
                files.extend(sorted(glob.glob(os.path.join(a, "*.mat"))))
            else:
                files.append(a)
    else:
        files = sorted(glob.glob(
            "/mnt/e/workspace/hyper-resolution/universal_fixed_point_framework/scripts/data/dpmp_drp374/*.mat"))
    for p in files:
        analyze(p, os.path.basename(p))


if __name__ == "__main__":
    main()
