# -*- coding: utf-8 -*-
"""
P7-5e-229b：合并干净数据（33..1024，16 点）四参/五参判别——E 干净值 / C / D / ε
====================================================================
背景（229）：C=13/128 低 m 段精确命中（+0.03%）；D −2~−3%；ε 低 m 段 +0.16e-6 vs
  高 m 段 +1.4~3.4e-6 不一致；E 两参低 m 段 +0.015（−24% vs 39/2000）。
  本脚本用全链干净数据（N=1200 16 点）做四参/五参，确认 E 真实值、C/D/ε 稳定性。
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0

if __name__ == "__main__":
    j = json.load(open(os.path.join(BASE, "_phase102_p7_5e229_lowm_N1200.json"), encoding="utf-8"))
    out = {int(k): v for k, v in j["out"].items()}
    ms_all = sorted(out.keys())
    print("== P7-5e-229b：合并干净数据 16 点（33..1024）四参/五参判别 ==", flush=True)

    def show(tag, lo, hi, cols, labels, Efix=None, Dfix=None, Cfix=None):
        msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
        ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
        y = ds.copy()
        if Efix is not None:
            y = y + Efix/msf**3
        if Dfix is not None:
            y = y + Dfix/msf**2
        if Cfix is not None:
            y = y + Cfix/msf
        X = np.vstack(cols(msf)).T
        c = np.linalg.lstsq(X, y, rcond=None)[0]
        r = y - X@c
        rms = float(np.sqrt(np.mean(r**2)))
        parts = ["  %s [%s] N=%d RMS=%.2e" % (tag, lab, len(msf), rms)]
        for name, val in zip(labels, c):
            parts.append("%s=%+.6g" % (name, val))
        print(" ".join(parts), flush=True)
        return c, rms

    for lo, hi, lab in [(33, 129, "33..129"), (33, 256, "33..256"), (33, 512, "33..512"), (33, 1024, "33..1024")]:
        print("", flush=True)
        # 四参 {δ∞,C,D,E} 全自由
        c4, r4 = show("四参{δ∞,C,D,E}", lo, hi,
                      lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3],
                      ["δ∞", "C", "D", "E"])
        print("    δ∞ dev=%+.5f pct  C vs13/128=%+.3f pct  D vs41/2000=%+.3f pct  E vs39/2000=%+.2f pct" %
              ((c4[0]-INV56)/INV56*100, (c4[1]-C13)/C13*100, (c4[2]-D41)/D41*100, (c4[3]-E39)/E39*100), flush=True)
        # 五参 {δ∞,C,D,E,F}
        c5, r5 = show("五参{δ∞,C,D,E,F}", lo, hi,
                      lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3, 1.0/m**4],
                      ["δ∞", "C", "D", "E", "F"])
        # 固定 C=13/128：{δ∞,D,E} 三参
        c3, r3 = show("三参{δ∞,D,E} C固定", lo, hi,
                      lambda m: [np.ones_like(m), 1.0/m**2, 1.0/m**3],
                      ["δ∞", "D", "E"], Cfix=C13)
        print("    D vs41/2000=%+.3f pct  E vs39/2000=%+.2f pct" % ((c3[1]-D41)/D41*100, (c3[2]-E39)/E39*100), flush=True)

    # ε 全链一致性（{δ∞} 单参 + 三参 C/D 固定）
    print("", flush=True)
    print("== ε 全链（{δ∞} 单参，C/D/E 锁定）==", flush=True)
    for lo, hi, lab in [(33, 129, "33..129"), (33, 256, "33..256"), (33, 512, "33..512"), (33, 1024, "33..1024"),
                        (128, 1024, "128..1024"), (512, 1024, "512..1024")]:
        msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
        ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
        tgt = ds + C13/msf + D41/msf**2 - E39/msf**3
        d1 = float(np.mean(tgt))
        r1 = float(np.sqrt(np.mean((tgt-d1)**2)))
        print("  [%s] ε=δ∞−1/56=%+.3e (dev %+.5f pct) RMS=%.2e" % (lab, d1-INV56, (d1-INV56)/INV56*100, r1), flush=True)

    json.dump({"base": "229+227 spectral N=1200", "points": ms_all},
              open(os.path.join(BASE, "_phase102_p7_5e229b_clean_full_fits.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
