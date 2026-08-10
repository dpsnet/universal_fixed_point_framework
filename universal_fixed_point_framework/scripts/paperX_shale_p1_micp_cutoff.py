# -*- coding: utf-8 -*-
"""
P1 门限压力提取：Tuscaloosa MICP 原始曲线低饱和端截止压（2026-08-10）
================================================================
目的：从原始 MICP 曲线提取样品级"整体 D + 对应门限压力 P_t"成对数据，
     闭合 P1 双曲标度 ln P_t = C/(D-2)+B 的样品级成对检验，并测试
     P_t 定义（截止饱和度阈值/膝点）对拟合与 D→2 预言的稳健性。

物理定义（低饱和端截止压）：
- S_pseudo = 伪润湿饱和度（未被汞占据的孔隙比例），自 1.0 随压力单调递减
- 汞饱和度 S_Hg = 1 - S_pseudo
- 定义 A（固定阈值）：P_t(S_c) = 汞饱和度首次达到 S_c 的压力，S_c ∈ {1%, 2%, 5%, 10%}
- 定义 B（膝点检测，阈值无关）：ln S_pseudo vs ln P 曲线距弦最大距离点对应压力
  （经典"门限压力/阈压"操作化：曲线从平缓端转入陡峭充填段的转折点）
D（整体分形维数）：ln S vs ln P 回归斜率 a，D = 2 - a（与原论文 §4.1 口径一致）

检验：
1. 每种 P_t 定义重拟合双曲 ln Pt = C/(D-2)+B vs 线性，比较 R² 与 C 符号/量级
2. D→2 端预言稳健性：C<0（P_t→0 弱封堵）是否对 P_t 定义不敏感
3. 输出成对 CSV 供后续低 D 端外推判定
"""
import csv
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data", "tuscaloosa_micp")
OUT = os.path.join(BASE, "data", "tuscaloosa_micp", "p1_paired_pairs.csv")

THRESHOLDS = [0.01, 0.02, 0.05, 0.10]   # S_Hg 截止饱和度（定义 A）


def r2(y, yp):
    return 1.0 - np.sum((y - yp) ** 2) / np.sum((y - y.mean()) ** 2)


def elbow_index(x, y):
    """膝点检测：曲线 (x,y) 上距首尾弦垂直距离最大的点索引（阈值无关）。"""
    x0, y0 = x[0], y[0]
    x1, y1 = x[-1], y[-1]
    vx, vy = x1 - x0, y1 - y0
    denom = np.hypot(vx, vy)
    if denom == 0:
        return len(x) // 2
    dist = np.abs(vy * (x - x0) - vx * (y - y0)) / denom
    return int(np.argmax(dist))


def load():
    with open(os.path.join(DATA, "MICPAirHgInjPress_psia.csv")) as f:
        Pc = np.array(list(csv.reader(f))[1:], dtype=float)
    with open(os.path.join(DATA, "MICP_PseudoWettingSaturation.csv")) as f:
        S = np.array(list(csv.reader(f))[1:], dtype=float)
    return Pc, S


def main():
    Pc, S = load()
    n_samp = Pc.shape[1]
    samples = []
    for j in range(n_samp):
        pc, s = Pc[:, j], S[:, j]
        m = (s > 0.05) & (s < 0.98) & (pc > 0) & np.isfinite(s)
        if m.sum() < 5:
            continue
        x, y = np.log(pc[m]), np.log(s[m])
        a, _ = np.polyfit(x, y, 1)
        D = 2.0 - a
        # 定义 A：固定汞饱和度阈值首次穿越压力
        pt_A = {}
        for sc in THRESHOLDS:
            s_target = 1.0 - sc            # 对应伪润湿饱和度
            idx = int(np.argmax(s < s_target))
            pt_A[sc] = pc[idx] if idx > 0 and s[idx] < s_target else np.nan
        # 定义 B：膝点压力（阈值无关）
        k = elbow_index(x, y)
        pt_B = pc[m][k]
        samples.append(dict(D=D, S_Hg_min=s[m].min(), S_Hg_max=1.0 - s[m].max(),
                            knee=pt_B, **{("Pt_%d%%" % int(100 * sc)): pt_A[sc]
                                          for sc in THRESHOLDS}))
    if not samples:
        print("无有效样品")
        return

    # ---- 汇总表 ----
    print("=" * 78)
    print("Tuscaloosa 31 样品 MICP：低饱和端截止压提取（样品级成对）")
    print("=" * 78)
    hdr = ["样品", "D", "膝点P_t/psia"] + ["P_t(%d%%)/psia" % int(100 * sc) for sc in THRESHOLDS]
    print(f"{hdr[0]:>4}{hdr[1]:>8}{hdr[2]:>14}" + "".join(f"{h:>14}" for h in hdr[3:]))
    for i, r in enumerate(samples):
        vals = [i + 1, f"{r['D']:.3f}", f"{r['knee']:.1f}"]
        vals += [f"{r['Pt_%d%%' % int(100 * sc)]:.1f}" if np.isfinite(r['Pt_%d%%' % int(100 * sc)])
                 else "n/a" for sc in THRESHOLDS]
        print(f"{vals[0]:>4}{vals[1]:>8}{vals[2]:>14}" + "".join(f"{v:>14}" for v in vals[3:]))

    # ---- 保存 CSV ----
    fields = ["sample", "D"] + ["knee_Pt_psia"] + ["Pt_%d%%_psia" % int(100 * sc) for sc in THRESHOLDS]
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(samples):
            row = {"sample": "S%d" % (i + 1), "D": r["D"], "knee_Pt_psia": r["knee"]}
            for sc in THRESHOLDS:
                row["Pt_%d%%_psia" % int(100 * sc)] = r["Pt_%d%%" % int(100 * sc)]
            w.writerow(row)

    # ---- 每种定义重拟合 P1 双曲 vs 线性 ----
    print("\n" + "=" * 78)
    print("P1 双曲标度重拟合（ln Pt = C/(D-2)+B vs 线性 ln Pt = A·D+B'）")
    print("=" * 78)
    Ds = np.array([r["D"] for r in samples])
    defs = [("knee", "膝点(阈值无关)")] + [("Pt_%d%%" % int(100 * sc), "截止S_Hg=%d%%" % int(100 * sc))
                                          for sc in THRESHOLDS]
    print(f"{'P_t 定义':<22}{'C':>8}{'B':>8}{'R²双曲':>8}{'R²线性':>8}{'ΔR²':>7}")
    results = {}
    for key, lbl in defs:
        Pt = np.array([r[key] for r in samples], dtype=float)
        m = np.isfinite(Pt) & (Pt > 0) & (Ds > 2)
        if m.sum() < 8:
            print(f"{lbl:<22} 有效样品 {m.sum()} < 8，跳过")
            continue
        lp = np.log(Pt[m])
        dd = Ds[m]
        C, B1 = np.polyfit(1.0 / (dd - 2), lp, 1)
        A, B0 = np.polyfit(dd, lp, 1)
        r2h = r2(lp, C / (dd - 2) + B1)
        r2l = r2(lp, A * dd + B0)
        results[key] = dict(C=C, B=B1, R2h=r2h, R2l=r2l, n=int(m.sum()),
                            rho=np.corrcoef(dd, lp)[0, 1])
        print(f"{lbl:<22}{C:>8.3f}{B1:>8.3f}{r2h:>8.3f}{r2l:>8.3f}{r2h - r2l:>7.3f}  (n={m.sum()})")

    # ---- D→2 端预言（对每种定义） ----
    print("\n" + "=" * 78)
    print("D→2 端外推预言（检验 C<0 → P_t→0 弱封堵对定义的稳健性）")
    print("=" * 78)
    print(f"{'P_t 定义':<22}{'C 符号':>8}{'lnPt(D=2.53)':>14}{'lnPt(D=2.09)':>14}{'预言方向':>12}")
    for key, lbl in defs:
        if key not in results:
            continue
        r = results[key]
        p253 = r["C"] / (2.53 - 2) + r["B"]
        p209 = r["C"] / (2.09 - 2) + r["B"]
        direction = "P_t→0 弱封堵" if r["C"] < 0 else "P_t→∞ 强封堵"
        print(f"{lbl:<22}{'C<0' if r['C'] < 0 else 'C>0':>8}{p253:>14.3f}{p209:>14.3f}{direction:>12}")

    # ---- 与黔北低 D 端衔接 ----
    print("\n" + "=" * 78)
    print("低 D 端衔接（黔北 D_Hg=2.0904 为当前最强 D→2 证据，预测其截止压）")
    print("=" * 78)
    for key, lbl in defs:
        if key not in results:
            continue
        r = results[key]
        lnp = r["C"] / (2.0904 - 2) + r["B"]
        print(f"{lbl:<22}: ln Pt = {lnp:.3f} → Pt = {np.exp(lnp):.3f} psia = {np.exp(lnp) * 0.00689476:.5f} MPa"
              f"（若实测截止压量级远小于此 → 与 P1 预言一致）")
    print("\nCSV 已保存：%s" % OUT)


if __name__ == "__main__":
    main()
