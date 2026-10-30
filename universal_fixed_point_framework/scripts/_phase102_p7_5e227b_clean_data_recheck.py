# -*- coding: utf-8 -*-
"""
P7-5e-227b：干净数据重审（N=1200 9 点 + 打靶 9 点）——E 真实值 / δ∞ / F 层
====================================================================
背景（227 定案后）：
  175/176（N=600）数据源有 ~1.3e-6 系统差（@513 实测 1.255e-6）→ 225/226 的 E=39/2000 判别基于有偏数据。
  227 还发现：完整模型 δ∞ 自由单参，打靶/谱 N=1200 高 m 段一致 dev +0.010~+0.011%（ε≈+2.0e-6），
    且 E 单参（δ∞=1/56 固定）爆炸——δ∞=1/56 固定模型与高精度数据不一致。
  本脚本用干净数据（N=1200 9 点 + 打靶 9 点，来自 227 json）重做判别。
先验登记（计算前）：
  P1 E 干净值：δ∞ 自由 + E 自由（两参，C/D 锁定；另四参全自由对照）→
     |E_opt − 39/2000| < 1% → ★★★ 39/2000 获干净数据支撑（225/226 结论获救，非 175/176 伪影）
     |E_opt − 39/2000| ≥ 5% → ★ E=39/2000 是 175/176 数据源伪影（225/226 重审）
  P2 δ∞ 真实值：两参/四参/五参 δ∞_fit 一致收敛 →
     |dev vs 1/56| < 0.003% → ★★★ δ∞=1/56 精确终判
     |dev| ≥ 0.008% → 1/56 有真实微修正（ε≈+2e-6 量级，227 初步）
  P3 F 层：五参 F 与 0 距离（|F|/σ）→ 显著非零则 F 层真实（178 的 F≈0 需重审）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0

def fit(ms, ds, cols):
    A = np.vstack(cols(ms)).T
    c, _, _, _ = np.linalg.lstsq(A, ds, rcond=None)
    r = ds - A@c
    return c, float(np.sqrt(np.mean(r**2))), r

if __name__ == "__main__":
    j = json.load(open(os.path.join(BASE, "_phase102_p7_5e227_dinf_final_shoot_ext.json"), encoding="utf-8"))
    ms_all = j["ms"]
    sh = {abs(m): j["shooting"][str(-m)] for m in ms_all}
    sp = {abs(m): j["spectral"][str(-m)] for m in ms_all}
    print("== P7-5e-227b：干净数据重审（N=1200 9 点 + 打靶 9 点）==", flush=True)

    for tag, out in [("打靶", sh), ("谱N1200", sp)]:
        print("", flush=True)
        print("---- %s ----" % tag, flush=True)
        for lo, hi, lab in [(512, 1024, "512..1024"), (128, 1024, "128..1024"), (128, 512, "128..512")]:
            msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
            ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
            # 两参 {δ∞, E}，C/D 锁定：δ = δ∞ − C/m − D/m² + E/m³
            X2 = np.vstack([np.ones_like(msf), 1.0/msf**3]).T
            c2 = np.linalg.lstsq(X2, ds + C13/msf + D41/msf**2, rcond=None)[0]
            r2 = (ds + C13/msf + D41/msf**2) - X2@c2
            rms2 = float(np.sqrt(np.mean(r2**2)))
            dev2 = (c2[0]-INV56)/INV56*100
            devE = (c2[1]-E39)/E39*100
            print("  两参{δ∞,E} [%s]: N=%d δ∞=%.10f(dev %+.5f pct) E=+%.6f(vs39 %+.2f pct) RMS=%.2e" %
                  (lab, len(msf), c2[0], dev2, c2[1], devE, rms2), flush=True)
            # 四参 {δ∞,C,D,E}
            X4 = np.vstack([np.ones_like(msf), 1.0/msf, 1.0/msf**2, 1.0/msf**3]).T
            c4, _, _, _ = np.linalg.lstsq(X4, ds, rcond=None)
            r4 = float(np.sqrt(np.mean((X4@c4 - ds)**2)))
            print("  四参{δ∞,C,D,E} [%s]: δ∞=%.10f(%+.5f pct) C=%.7f D=%.6f E=+%.6f RMS=%.2e" %
                  (lab, c4[0], (c4[0]-INV56)/INV56*100, c4[1], c4[2], c4[3], r4), flush=True)
            # 五参 {δ∞,C,D,E,F}
            X5 = np.vstack([np.ones_like(msf), 1.0/msf, 1.0/msf**2, 1.0/msf**3, 1.0/msf**4]).T
            c5, _, _, _ = np.linalg.lstsq(X5, ds, rcond=None)
            r5 = float(np.sqrt(np.mean((X5@c5 - ds)**2)))
            print("  五参{δ∞,C,D,E,F} [%s]: δ∞=%.10f(%+.5f pct) C=%.7f D=%.6f E=+%.6f F=%+.6f RMS=%.2e" %
                  (lab, c5[0], (c5[0]-INV56)/INV56*100, c5[1], c5[2], c5[3], c5[4], r5), flush=True)

    # 判别（打靶 + 谱 高 m 段两参）
    print("", flush=True)
    print("== 判别汇总 ==", flush=True)
    for tag, out in [("打靶", sh), ("谱N1200", sp)]:
        msf = np.array([m for m in ms_all if 512 <= m <= 1024], dtype=float)
        ds = np.array([out[m]["delta"] for m in ms_all if 512 <= m <= 1024])
        X2 = np.vstack([np.ones_like(msf), 1.0/msf**3]).T
        c2 = np.linalg.lstsq(X2, ds + C13/msf + D41/msf**2, rcond=None)[0]
        print("  %s 两参[512..1024]: δ∞=%+.6f(dev %+.5f pct) E=+%.6f(vs39 %+.2f pct)" %
              (tag, c2[0], (c2[0]-INV56)/INV56*100, c2[1], (c2[1]-E39)/E39*100), flush=True)

    # 175/176 系统差全貌：对 δ∞ 自由两参模型（δ∞+E，C/D 锁定）的残差形态
    print("", flush=True)
    print("== 175/176 系统差全貌：对 {δ∞,E} 两参模型的残差（δ∞ 自由） ==", flush=True)
    j175 = json.load(open(os.path.join(BASE, "_phase102_p7_5e175_delta63.json"), encoding="utf-8"))
    j176 = json.load(open(os.path.join(BASE, "_phase102_p7_5e176_delta_lowm.json"), encoding="utf-8"))
    m175 = np.array(j175["m"]); d175 = np.array(j175["delta"])
    m176 = np.array(j176["m"]); d176 = np.array(j176["delta"])
    for tag, ms, ds in [("175(N=600)", m175, d175), ("176(N=600)", m176, d176)]:
        X2 = np.vstack([np.ones_like(ms), 1.0/ms**3]).T
        c2 = np.linalg.lstsq(X2, ds + C13/ms + D41/ms**2, rcond=None)[0]
        r = ds - (c2[0] - C13/ms - D41/ms**2 + c2[1]/ms**3)
        print("  %s {δ∞,E}两参: δ∞=%.10f(dev %+.5f pct) E=+%.6f(vs39 %+.2f pct) RMS=%.2e" %
              (tag, c2[0], (c2[0]-INV56)/INV56*100, c2[1], (c2[1]-E39)/E39*100, float(np.sqrt(np.mean(r**2)))), flush=True)
        # 分段残差（低/中/高 m）
        for lo, hi, lab in [(17, 63, "17..63"), (65, 255, "65..255"), (257, 1009, "257..1009")]:
            sel = (ms >= lo) & (ms <= hi)
            if sel.sum() > 0:
                rr = r[sel]
                print("    [%s]: N=%d RMS=%.2e max|r|=%.2e mean=%+.2e" %
                      (lab, len(rr), float(np.sqrt(np.mean(rr**2))), float(max(abs(rr))), float(np.mean(rr))), flush=True)

    json.dump({"base": "P7-5e-227 json (9+9 pts)",
               "note": "clean-data recheck: 2-param/4-param/5-param fits"},
              open(os.path.join(BASE, "_phase102_p7_5e227b_clean_data_recheck.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
