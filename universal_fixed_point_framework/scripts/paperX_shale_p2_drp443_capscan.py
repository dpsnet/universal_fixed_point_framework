#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2 压力-饱和度成对数据数值构造：DRP-443 真实岩石诱导裂缝网络准静态侵入扫描
（Paper XLIII 研究推进 P2-6，2026-08-09）

背景：MICP 压汞代理裁决为诚实负结果（ν_free≡D-2 为几何恒等，测不到临界动力学，
见 paperX_shale_p2_micp_sat_scaling.py）。ν 裁决须转向动力学数据。本脚本为
"LBM 前置"的准静态数值毛管压力扫描：

方法（入侵渗透的确定性简化版）：
  (1) 裂缝相 = 相 0（16.5%）；距离变换 dist = EDT(mask) 作局部孔径代理（体素单位）；
  (2) Washburn 代理：P(r) = 1/r（常数因子 2γcosθ 不影响幂律指数检验）；
  (3) 压力台阶 P 递增 ⇔ 阈值孔径 r_thr 递减：保留 dist>=r_thr 的裂缝相体素，
      从入口面（x=0）沿 26-连通注入，标记注入集；
  (4) 每台阶记录 (P, S_inj)，S_inj = 注入集体积/裂缝相总体积；
  (5) 贯通台阶（注入集到达出口面 x=nx-1）= 突破点 (P_c, S_c)；
  (6) 临界检验：在 S<S_c 窗口内，ln P vs ln(S_c - S) 线性斜率 = -ν（若 P2 成立）。

诚实边界：
  - 该扫描仍为准静态（无时间演化），产出的"压力-饱和度"曲线承载几何-拓扑
    响应；与 MICP 的差别在于"从入口面注入+贯通判据"更接近突破物理；
  - 距离变换为孔径代理，非真实孔径分布——仅用于临界幂律形式检验，
    不做定量孔径标定；
  - 若临界端亦无幂律（同 MICP 窄窗），则确认准静态几何路径无法裁决 ν，
    必须转向真动力学（LBM/泄压模拟）。
"""
import os
import numpy as np
import scipy.ndimage as ndi

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "data", "drp443_ifn", "IFN.raw")
SHAPE = (550, 550, 500)  # (nx, ny, nz)


def load(path, shape):
    a = np.memmap(path, dtype=np.uint8, mode="r", shape=shape)
    return np.asarray(a, dtype=np.uint8)


def main():
    if not os.path.exists(RAW):
        print("数据缺失：%s" % RAW)
        return
    vol = load(RAW, SHAPE)
    mask = (vol == 0)                      # 相 0 = 诱导裂缝网络（孔隙相）
    nx, ny, nz = mask.shape
    frac_total = int(mask.sum())
    print("DRP-443 IFN.raw：shape=%s，裂缝相体素=%d（%.1f%%）"
          % (str(mask.shape), frac_total, 100.0 * frac_total / mask.size))

    # 距离变换（欧氏，体素单位）作局部孔径代理
    print("计算距离变换（EDT，孔径代理）...")
    dist = ndi.distance_transform_edt(mask)
    dmax = float(dist.max())
    print("  孔径代理范围：[0, %.1f] 体素" % dmax)

    # 压力台阶：r_thr 从大孔径到小孔径（对数等距 40 台阶，下探到单体素裂缝 1.0）
    r_thr_list = np.geomspace(dmax, 1.0, 40)
    # 入口面：x=0 面上 dist>=r_thr 的裂缝体素（种子），出口面 x=nx-1
    results = []
    prev_mask = None
    prev_res = None
    print("逐压力台阶注入扫描（26-连通）...")
    for i, rthr in enumerate(r_thr_list):
        acc = dist >= rthr               # 该压力下可进入的裂缝体素（几何可达）
        # 若与上一台阶相同则复用（避免重复 label）
        if prev_mask is not None and np.array_equal(acc, prev_mask) and prev_res is not None:
            P_prev, S_inj, S_tot, perc = prev_res
            results.append((1.0 / rthr, S_inj, S_tot, perc))
            continue
        prev_mask = acc
        lab, nl = ndi.label(acc, structure=np.ones((3, 3, 3)))
        if nl == 0:
            results.append((1.0 / rthr, 0.0, 0.0, False))
            prev_res = (1.0 / rthr, 0.0, 0.0, False)
            continue
        # 注入集：与入口面种子 26-连通的所有标签
        seeds = np.unique(lab[0, :, :])
        seeds = seeds[seeds > 0]
        if len(seeds) == 0:
            results.append((1.0 / rthr, 0.0, 0.0, False))
            prev_res = (1.0 / rthr, 0.0, 0.0, False)
            continue
        inj = np.isin(lab, seeds)
        # 贯通判据：注入集触及出口面 x=nx-1
        perc = bool(inj[nx - 1, :, :].any())
        S_inj = float(inj.sum()) / frac_total          # 注入集体积比（相对总裂缝相）
        S_tot = float(acc.sum()) / frac_total          # 几何可达比（忽略连通性）
        results.append((1.0 / rthr, S_inj, S_tot, perc))
        prev_res = (1.0 / rthr, S_inj, S_tot, perc)
        print("  r_thr=%-6.2f P=%-8.4f S_inj=%.4f S_tot=%.4f 贯通=%s"
              % (rthr, 1.0 / rthr, S_inj, S_tot, perc))

    # 突破点：首个贯通台阶
    P_arr = np.array([r[0] for r in results])
    S_arr = np.array([r[1] for r in results])
    Stot = np.array([r[2] for r in results])
    perc_arr = np.array([r[3] for r in results])
    if not perc_arr.any():
        print("警告：未形成贯通通道（台阶不足或网络不连通）")
        return
    idx_c = int(np.argmax(perc_arr))
    Pc, Sc = P_arr[idx_c], S_arr[idx_c]
    print("突破点：P_c=%.4f（r_thr=%.2f），S_c=%.4f（台阶 %d/%d）"
          % (Pc, 1.0 / Pc, Sc, idx_c, len(P_arr)))
    print("S_c 对照：裂缝相贯通时的注入饱和度（S_c<1 即注入不足全相）")

    # 临界幂律检验：ln P vs ln(S_c - S)，S < S_c 窗口
    print("\n临界幂律检验（P2：Δp ∝ (S_c - S)^{-ν}，即 ln P = ln K - ν·ln(S_c-S)）")
    for wmin in (0.02, 0.05, 0.10):
        m = (S_arr < Sc - wmin) & (S_arr > 0.005)
        if m.sum() < 4:
            print("  窗口 S_c-S>=%.2f：点数不足" % wmin)
            continue
        x = np.log(Sc - S_arr[m])
        y = np.log(P_arr[m])
        a, b = np.polyfit(x, y, 1)
        yp = a * x + b
        r2 = 1.0 - np.sum((y - yp) ** 2) / np.sum((y - y.mean()) ** 2)
        print("  窗口 S_c-S>=%.2f（n=%d）：斜率 %.3f -> ν=%.3f，R²=%.3f"
              % (wmin, m.sum(), a, -a, r2))
    print("\n解读：若临界端 (S_c-S→0) 出现稳定幂律且 ν 一致 -> 准静态几何路径")
    print("      亦可见临界标度（支持 P2 形式，但仍非动力学 ν）；")
    print("      若无稳定幂律 -> 与 MICP 一致，确认须转向真动力学模拟。")


if __name__ == "__main__":
    main()
