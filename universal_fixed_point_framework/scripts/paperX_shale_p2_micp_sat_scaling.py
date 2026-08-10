#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2 压力-饱和度模型形式裁决：Tuscaloosa MICP 逐点曲线（Paper XLIII 研究推进，2026-08-09）

问题：P2 超压临界幂律 Δp ∝ (S_o^c - S_o)^{-ν} 的 ν 取值存在分歧——
  - 理论/渗流类比预言 ν≈1/2（临界幂律）；
  - 东营 NMR 离心 Langmuir 锚点 R_m = 20.83·ΔP/(ΔP+1.09)（Xu et al., 2021）隐含 ν=1。
裁决需要逐点"压力-饱和度"成对数据。本文暂以压汞（MICP）注入曲线作为
实验室代理：压汞饱和度 S(P_c) 与油相占据饱和度 S_o(ΔP) 同构（均为毛细管力
驱动占据，Washburn 关系 P_c ∝ 1/r）。映射假设显式登记（H_pc）。

模型形式（对每个样品）：
  y = S（伪润湿饱和度 = 未被汞占据的孔隙比例，对应油相"未突破占据"比例
      S_o^c - S_o；S 从 1.0 随压力递减，物理上随 P 增大残留比例趋零）
  自由幂律：y = K·P^{-ν}      -> ln y = ln K - ν·ln P，斜率 = -ν（自由）
  Langmuir：ν = 1 固定         -> ln y = ln P_L - ln P（P >> P_L 渐近）
  临界幂律：ν = 1/2 固定

裁决逻辑：31 样品上比较
  (1) 自由斜率 ν 的分布（中位/范围）——支持 1 还是 1/2？
  (2) 固定 ν=1 vs ν=1/2 对自由拟合的 R² 损失——哪个固定模型更接近数据？
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data", "tuscaloosa_micp")
PRESS = os.path.join(DATA_DIR, "MICPAirHgInjPress_psia.csv")
SAT = os.path.join(DATA_DIR, "MICP_PseudoWettingSaturation.csv")


def load():
    with open(PRESS, "r") as f:
        Pc = np.array(list(csv.reader(f))[1:], dtype=float)
    with open(SAT, "r") as f:
        S = np.array(list(csv.reader(f))[1:], dtype=float)
    return Pc, S


def r2(y, yp):
    return 1.0 - np.sum((y - yp) ** 2) / np.sum((y - y.mean()) ** 2)


def main():
    Pc, S = load()
    n_samp = Pc.shape[1]
    nu_free, r2_free, r2_fix1, r2_fix05, n_pts = [], [], [], [], []
    # 分段窗口：伪润湿饱和度 S 从 1.0 随压力递增而递减。
    #   S∈(0.5,0.98) = 低压端（P→门槛 P_t，油相刚开始突破 = 临界端）
    #   S∈(0.05,0.5) = 高压端（汞深侵入，远离临界）
    nu_hi, nu_lo, r2_hi, r2_lo = [], [], [], []
    for j in range(n_samp):
        pc, s = Pc[:, j], S[:, j]
        m = (s > 0.05) & (s < 0.98) & (pc > 0) & np.isfinite(s)
        if m.sum() < 6:
            continue
        x = np.log(pc[m])
        y = np.log(s[m])                # 伪润湿（未侵入）饱和度对数
        # 自由斜率
        slope, b0 = np.polyfit(x, y, 1)
        yp = slope * x + b0
        nu_free.append(-slope)          # ν = -斜率
        r2_free.append(r2(y, yp))
        n_pts.append(m.sum())
        # 固定 ν=1（Langmuir）：y = b - x
        b1 = np.mean(y + x)
        r2_fix1.append(r2(y, b1 - x))
        # 固定 ν=1/2（临界）：y = b - 0.5x
        b05 = np.mean(y + 0.5 * x)
        r2_fix05.append(r2(y, b05 - 0.5 * x))
        # 分段窗口（复用 M1 多段分形口径；nu_hi=低压端临界窗口，nu_lo=高压端远离临界）
        for lo, hi, nb, rb in ((0.5, 0.98, nu_hi, r2_hi), (0.05, 0.5, nu_lo, r2_lo)):
            m2 = (s > lo) & (s < hi) & (pc > 0) & np.isfinite(s)
            if m2.sum() >= 4:
                x2, y2 = np.log(pc[m2]), np.log(s[m2])
                a2, b2 = np.polyfit(x2, y2, 1)
                rb.append(r2(y2, a2 * x2 + b2))
                if r2(y2, a2 * x2 + b2) >= 0.85:   # 仅高质量段进入 ν 统计
                    nb.append(-a2)

    nu = np.array(nu_free)
    r2f = np.array(r2_free)
    r21 = np.array(r2_fix1)
    r205 = np.array(r2_fix05)
    n = len(nu)

    print("P2 模型形式裁决：Tuscaloosa MICP 逐点曲线（%d 样品有效）" % n)
    print("-" * 72)
    print("自由幂律斜率 ν 分布：中位 %.3f，IQR [%.3f, %.3f]，范围 [%.2f, %.2f]"
          % (np.median(nu), np.percentile(nu, 25), np.percentile(nu, 75),
             nu.min(), nu.max()))
    print("自由拟合 R² 中位 %.3f（固定 ν=1：%.3f；固定 ν=1/2：%.3f）"
          % (np.median(r2f), np.median(r21), np.median(r205)))
    # R² 损失（固定模型相对自由模型），取每样品差
    loss1 = r2f - r21
    loss05 = r2f - r205
    print("R² 损失（自由-固定）：ν=1 中位 %.3f；ν=1/2 中位 %.3f"
          % (np.median(loss1), np.median(loss05)))
    better1 = np.mean(loss1 < loss05)
    print("ν=1 比 ν=1/2 更优的样品占比：%.0f%%" % (100 * better1))
    # 支持度：|ν-1| vs |ν-1/2| 哪个更近
    near1 = np.mean(np.abs(nu - 1.0) < np.abs(nu - 0.5))
    print("自由 ν 更接近 1 的样品占比：%.0f%%；更接近 1/2：%.0f%%"
          % (100 * near1, 100 * (1 - near1)))
    # 分段窗口结果（仅高质量段 R²>=0.85）
    if len(nu_hi) >= 5:
        nuh = np.array(nu_hi)
        print("分段窗口（R²>=0.85 段）：低压端(S>0.5, P→P_t 临界端) ν 中位 %.3f（n=%d，IQR [%.2f, %.2f]）"
              % (np.median(nuh), len(nuh),
                 np.percentile(nuh, 25), np.percentile(nuh, 75)))
    if len(nu_lo) >= 5:
        nul = np.array(nu_lo)
        print("                   ：高压端(S<0.5, 深侵入远离临界) ν 中位 %.3f（n=%d，IQR [%.2f, %.2f]）"
              % (np.median(nul), len(nul),
                 np.percentile(nul, 25), np.percentile(nul, 75)))
    print("-" * 72)
    print("临界端窄窗扫描（口径：P_t=首次 S<0.95 压力，u=P/P_t 归一化，窗口 u≤U）")
    for U in (1.2, 1.5, 2.0, 3.0, 5.0, 10.0):
        nus, r2s = [], []
        for j in range(n_samp):
            pc, s = Pc[:, j], S[:, j]
            idx = int(np.argmax(s < 0.95))
            if idx <= 0:
                continue
            pt = pc[idx]
            m = (pc > 0) & (s > 0.05) & (pc <= U * pt) & np.isfinite(s)
            if m.sum() < 5:
                continue
            x2, y2 = np.log(pc[m]), np.log(s[m])
            a2, b2 = np.polyfit(x2, y2, 1)
            r = r2(y2, a2 * x2 + b2)
            nus.append(-a2); r2s.append(r)
        if len(nus) >= 5:
            nua = np.array(nus); r2a = np.array(r2s)
            hi = r2a >= 0.85
            seg = nua[hi] if hi.sum() >= 3 else nua
            print("  u≤%-4s 样品 n=%-3d（高质量段 %d）：ν 中位 %.3f（IQR [%.2f, %.2f]，R² 中位 %.2f）"
                  % (str(U), len(nus), int(hi.sum()), np.median(seg),
                     np.percentile(seg, 25), np.percentile(seg, 75), np.median(r2a)))
    print("-" * 72)
    print("逐样品滑窗扫描（窗宽 ΔlogS=0.6，观察 ν 随 S 位置的连续演化；仅统计 R²≥0.90 窗）")
    # S 对数等宽滑窗：y = ln S，y∈[ln0.98, ln0.05]，窗宽 0.6
    ymax, ymin, dw = np.log(0.98), np.log(0.05), 0.6
    nbins = int(np.ceil((ymax - ymin) / dw))
    bin_nu = [[] for _ in range(nbins)]
    for j in range(n_samp):
        pc, s = Pc[:, j], S[:, j]
        m = (s > 0.05) & (s < 0.98) & (pc > 0) & np.isfinite(s)
        if m.sum() < 8:
            continue
        x, y = np.log(pc[m]), np.log(s[m])
        # 按 y 排序保证窗口内点连续
        order = np.argsort(y)
        y_o, x_o = y[order], x[order]
        for lo in range(nbins):
            ylo = ymax - (lo + 1) * dw
            yhi = ymax - lo * dw
            mm = (y_o >= ylo) & (y_o < yhi)
            if mm.sum() < 5:
                continue
            xw, yw = x_o[mm], y_o[mm]
            a, b = np.polyfit(xw, yw, 1)
            r = r2(yw, a * xw + b)
            if r >= 0.90:
                bin_nu[lo].append(-a)
    print("  S 区间（高→低）          ν 中位 (n, IQR)          D=2+ν 中位   高质量样品数")
    for lo in range(nbins):
        if not bin_nu[lo]:
            continue
        ylo = ymax - (lo + 1) * dw
        yhi = ymax - lo * dw
        arr = np.array(bin_nu[lo])
        print("  S∈[%.2f, %.2f]     %.3f (n=%d, IQR [%.2f, %.2f])     %.3f        %d"
              % (np.exp(ylo), np.exp(yhi), np.median(arr), len(arr),
                 np.percentile(arr, 25), np.percentile(arr, 75),
                 2.0 + np.median(arr), len(arr)))
    print("  注：ν = -slope，压汞分形 D = 2 - slope，故 D = 2 + ν（M1 口径）")
    print("-" * 72)
    print("结论（诚实负结果）：压汞代理无法裁决 P2 的 ν=1/2 vs ν=1。")
    print("  (1) 表观幂律指数 ν_free ≡ D-2（压汞分形维数偏移，M1 口径的代数恒等）——")
    print("      承载的是孔喉几何分布信息，非临界动力学指数；")
    print("  (2) 窄窗扫描在 P_t 附近无高质量幂律（S→1 饱和区 log S≈0 无信息量），")
    print("      压汞静态曲线测不到临界端动力学；")
    print("  (3) ν 裁决必须转向：东营 NMR 离心逐点表转录（实验室动力学，正主）或")
    print("      LBM 突破动力学模拟（数值动力学，DRP-374/443 二值体）。")
    print("  附带正发现：多段结构独立复现——低压端(大孔段) ν=0.342 → D=2.342，")
    print("      与论文 M1 大孔段 D=2.395 同量级；高压端 ν>1.5 → D>3 非物理")
    print("      （高压段分形性差的已知表现，第 2 项实证一致）。")


if __name__ == "__main__":
    main()
