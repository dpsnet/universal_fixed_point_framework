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
P3 真实岩石成像检验：DRP-443 Induced Fracture Network（IFN.raw）
Web Corral 匿名镜像：https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-443/
数据：550 x 550 x 500 uint8 二值体；相 0（16.5%）= 诱导裂缝网络，255 = 岩石基质。
     真实岩石（诱导裂缝网络）三维 CT 数据 —— P3 首次真实岩石检验（非合成）。

协议（与 DPMP DRP-374 脚本一致，保证可比性）：
  (1) 裂缝网络 = 相 0；
  (2) 3D 盒计数裂缝网络 → D_3d（D∈(2,3) 类别对照，不与 0.6309 直接比较）；
  (3) 中心线（沿 z 每层质心）→ 骨架 3D 盒计数 → D_skel（准一维通道，D∈(1,2)）；
  (4) 中心线沿 x/y 1D 投影盒计数 → D_1d（Cantor 截面检验，与 ln2/ln3≈0.6309 对比）；
  (5) 中心线 x-y 截面 2D 盒计数 → D_2d。

诚实声明：IFN 为真实岩石（Berea/同类砂岩）诱导裂缝网络的三维 CT 二值分割，
      但非页岩贯通突破通道成像；结果作为 P3 真实岩石裂缝网络类别检验。
"""
import os
import sys
import numpy as np

RAW = "/mnt/e/workspace/hyper-resolution/universal_fixed_point_framework/scripts/data/drp443_ifn/IFN.raw"
SHAPE = (550, 550, 500)  # (nx, ny, nz)


def load(path, shape):
    a = np.memmap(path, dtype=np.uint8, mode="r", shape=shape)
    return np.asarray(a, dtype=np.uint8)


def boxcount_3d(mask, eps_list):
    """3D 盒计数（向量化：逐层 grid id 去重）。"""
    res = []
    ny, nx, nz = mask.shape
    for eps in eps_list:
        hx = nx // eps + 1
        total = set()
        for z in range(nz):
            sl = mask[:, :, z]
            ys, xs = np.where(sl)
            if len(xs) == 0:
                continue
            gx = xs // eps
            gy = ys // eps
            ids = np.unique(gx * hx + gy)
            zb = z // eps
            for idv in ids:
                total.add((idv, zb))
        res.append((eps, len(total)))
    return res


def boxcount_3d_small(mask, eps_list):
    """3D 盒计数（小体素集，如骨架点）。"""
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
    res = []
    for eps in eps_list:
        covered = np.zeros(span // eps + 1, dtype=bool)
        for p in pts:
            covered[int(p // eps)] = True
        res.append((eps, int(covered.sum())))
    return res


def boxcount_2d(pts, span, eps_list):
    res = []
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
    yhat = k * lx + b
    ss_res = ((ly - yhat) ** 2).sum()
    ss_tot = ((ly - ly.mean()) ** 2).sum()
    return -k, 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")


def analyze(d, label):
    frac = (d == 0)
    print("=" * 70)
    print("FILE:", label, " shape:", d.shape)
    print("  裂缝相（相 0）：%d 体元，占比 %.4f" % (frac.sum(), frac.mean()))

    # (2) 3D 盒计数（裂缝网络类别）
    eps3 = [2, 4, 8, 16, 32, 64, 128]
    bc3 = boxcount_3d(frac, eps3)
    d3, r3 = fit_dim(eps3, [n for _, n in bc3])
    print("  [2] 3D 盒计数（裂缝网络）：D_3d = %.3f（R²=%.4f）" % (d3, r3))
    print("       逐尺度 N(eps):", [(e, n) for e, n in bc3])

    # (3) 中心线（沿 z 每层质心）
    zs, xs, ys = [], [], []
    nz = frac.shape[2]
    for z in range(nz):
        sl = frac[:, :, z]
        if sl.any():
            ys_, xs_ = np.where(sl)
            xs.append(xs_.mean())
            ys.append(ys_.mean())
            zs.append(z)
    n_occ = len(zs)
    print("  中心线：%d/%d 层有裂缝占据" % (n_occ, nz))
    if n_occ < 8:
        print("  !! 裂缝层过少，骨架盒计数不可靠，跳过")
        return

    skel = np.zeros_like(frac, dtype=bool)
    for z, x, y in zip(zs, xs, ys):
        skel[int(x), int(y), z] = True
    bcsk = boxcount_3d_small(skel, eps3)
    dsk, rsk = fit_dim(eps3, [n for _, n in bcsk])
    print("  [3] 中心线骨架 3D 盒计数：D_skel = %.3f（R²=%.4f）" % (dsk, rsk))

    # (4) 中心线 1D 投影（Cantor 检验）
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
    print("        P3 理论 0.6309 属 1D 截面 Cantor 类别，仅与 D_1d 比较。")

    # (6) 连通域 + 贯通性 + 投影占据集 1D 盒计数（体积网络正确口径）
    # 连通性定义：26-连通（全邻域）。裂缝薄至 1–2 体素宽时对角线接触在物理上连通，
    # 6-连通（仅面接触）将网络切碎（对照：6-连通最大域仅 1.7%）。
    try:
        from scipy import ndimage
        lab, nlab = ndimage.label(frac, structure=np.ones((3, 3, 3), dtype=bool))
        sizes = ndimage.sum(frac, lab, index=range(1, nlab + 1))
        sizes = np.asarray(sizes, dtype=np.int64)
        big = int(np.argmax(sizes)) + 1
        main = lab == big
        print("  [6] 连通域（26-连通全邻域）：%d 个；最大域占裂缝相 %.1f%%" % (nlab, 100 * sizes[big - 1] / frac.sum()))
        # 6-连通对照（诚实登记定义依赖）
        struct6 = np.zeros((3, 3, 3), dtype=bool)
        struct6[1, 1, :] = True
        struct6[1, :, 1] = True
        struct6[:, 1, 1] = True
        lab6, nlab6 = ndimage.label(frac, structure=struct6)
        sizes6 = np.asarray(ndimage.sum(frac, lab6, index=range(1, nlab6 + 1)), dtype=np.int64)
        big6 = int(np.argmax(sizes6)) + 1
        print("       6-连通对照：域数=%d，最大域占裂缝相 %.1f%%（对角线接触主导 → 定义依赖显式登记）"
              % (nlab6, 100 * sizes6[big6 - 1] / frac.sum()))
        for ax, nm in [(0, "x"), (1, "y"), (2, "z")]:
            sl0 = [slice(None)] * 3
            sl1 = [slice(None)] * 3
            sl0[ax] = 0
            sl1[ax] = -1
            print("       最大域沿 %s 两端连通（贯通）: %s" % (nm, bool((main[tuple(sl0)] & main[tuple(sl1)]).any())))
        # 投影占据集 1D 盒计数
        eps1 = [2, 4, 8, 16, 32, 64, 128]
        for nm, axis in [("x", (1, 2)), ("y", (0, 2)), ("z", (0, 1))]:
            occ = main.any(axis=axis)
            bc = boxcount_1d(np.where(occ)[0], len(occ), eps1)
            dd, rr = fit_dim(eps1, [n for _, n in bc])
            rel = (dd - 0.6309) / 0.6309
            print("       投影占据 %s：D_1d=%.4f（R²=%.4f） vs 0.6309 → 偏离 %+.1f%%"
                  % (nm, dd, rr, rel * 100))
    except ImportError:
        print("  [6] scipy 不可用，跳过连通域分析")
    print()


def main():
    db = np.log(2) / np.log(3)
    print("P3 理论值 D_b = ln2/ln3 = %.4f" % db)
    d = load(RAW, SHAPE)
    analyze(d, "DRP-443 IFN.raw (550^2 x 500, real induced fracture network)")


if __name__ == "__main__":
    main()
