# -*- coding: utf-8 -*-
"""
P7-5e-228：干净数据 F 层复核 + ε 一致性（N=1200 9 点 + 打靶 9 点）
====================================================================
背景（227b 后）：178 的 F≈0 基于 175/176（有偏）数据需重审；但干净数据 m≥128 上 F/m⁴ 贡献
  ≤2e-11（F=0.005 @128），噪声 ~1e-7——F 大概率不可提取（先验登记 P3 分支）。
  同时用 {δ∞,E,F} 三参检查 δ∞ 的 ε 窗口一致性（227b 的 +0.006~+0.016% 窗口漂移是否
  由未吸收的 E/F 高阶结构引起，三参吸收后 ε 是否收敛）。
先验登记（计算前）：
  P1 F 显著非零（|F|>5σ 且 RMS 改善 >10×）→ F 层真实（178 的 F≈0 重审）
  P2 F≈0 兼容（|F|/σ ≤2 或 RMS 无改善）→ 178 的 F≈0 维持（干净数据兼容）
  P3 F 不可判别（信号淹没 / 拟合爆炸 / RMS 无稳定改善）→ 登记边界（需更高精度或解析通道）
  P4 ε 一致性：{δ∞,E,F} 三参 δ∞ 各窗口差 <±0.002% → ε 锁定；
     窗口漂移 ≥0.005% → ε 未锁（模型残留结构，1/56 近似维持、ε≈+1~3e-6 范围登记）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0

if __name__ == "__main__":
    j = json.load(open(os.path.join(BASE, "_phase102_p7_5e227_dinf_final_shoot_ext.json"), encoding="utf-8"))
    ms_all = j["ms"]
    sh = {abs(m): j["shooting"][str(-m)] for m in ms_all}
    sp = {abs(m): j["spectral"][str(-m)] for m in ms_all}
    print("== P7-5e-228：干净数据 F 层复核 + ε 一致性 ==", flush=True)

    # F 层贡献量级估算
    print("  F 层贡献量级：F/m^4（F=0.005 量级）@128=%.1e @256=%.1e @512=%.1e @1024=%.1e（噪声~1e-7）" %
          (0.005/128**4, 0.005/256**4, 0.005/512**4, 0.005/1024**4), flush=True)

    for tag, out in [("打靶", sh), ("谱N1200", sp)]:
        print("", flush=True)
        print("---- %s ----" % tag, flush=True)
        for lo, hi, lab in [(128, 512, "128..512"), (128, 1024, "128..1024"), (512, 1024, "512..1024")]:
            msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
            ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
            y = ds + C13/msf + D41/msf**2   # δ∞ − E/m³ − F/m⁴ 部分
            # {δ∞} 单参（E=39/2000 固定）
            t1 = y - E39/msf**3
            d1 = float(np.mean(t1))
            r1 = float(np.sqrt(np.mean((t1-d1)**2)))
            # {δ∞,F} 两参（E=39/2000 固定）
            X2 = np.vstack([np.ones_like(msf), 1.0/msf**4]).T
            c2 = np.linalg.lstsq(X2, y - E39/msf**3, rcond=None)[0]
            r2 = float(np.sqrt(np.mean((X2@c2 - (y - E39/msf**3))**2)))
            # {δ∞,E,F} 三参（C/D 锁定）
            X3 = np.vstack([np.ones_like(msf), 1.0/msf**3, 1.0/msf**4]).T
            c3 = np.linalg.lstsq(X3, y, rcond=None)[0]
            r3 = float(np.sqrt(np.mean((X3@c3 - y)**2)))
            print("  [%s] N=%d" % (lab, len(msf)), flush=True)
            print("    {δ∞}单参:     δ∞=%.10f (dev %+.5f pct) RMS=%.2e" % (d1, (d1-INV56)/INV56*100, r1), flush=True)
            print("    {δ∞,F}两参:   δ∞=%.10f (dev %+.5f pct) F=%+.6f RMS=%.2e (改善 %.1fx)" %
                  (c2[0], (c2[0]-INV56)/INV56*100, c2[1], r2, r1/r2 if r2 > 0 else float('inf')), flush=True)
            print("    {δ∞,E,F}三参: δ∞=%.10f (dev %+.5f pct) E=+%.6f F=%+.6f RMS=%.2e (vs单参 %.1fx)" %
                  (c3[0], (c3[0]-INV56)/INV56*100, c3[1], c3[2], r3, r1/r3 if r3 > 0 else float('inf')), flush=True)

    # ε 窗口一致性汇总（{δ∞,E,F} 三参）
    print("", flush=True)
    print("== ε 窗口一致性（{δ∞,E,F} 三参，C/D 锁定）==", flush=True)
    eps_windows = {}
    for tag, out in [("打靶", sh), ("谱N1200", sp)]:
        for lo, hi, lab in [(128, 512, "128..512"), (128, 1024, "128..1024"), (512, 1024, "512..1024")]:
            msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
            ds = np.array([out[m]["delta"] for m in ms_all if lo <= m <= hi])
            y = ds + C13/msf + D41/msf**2
            X3 = np.vstack([np.ones_like(msf), 1.0/msf**3, 1.0/msf**4]).T
            c3 = np.linalg.lstsq(X3, y, rcond=None)[0]
            eps_windows.setdefault(tag, {})[lab] = (c3[0]-INV56)
            print("  %s [%s]: ε=δ∞−1/56=%+.3e (dev %+.5f pct)" % (tag, lab, c3[0]-INV56, (c3[0]-INV56)/INV56*100), flush=True)
    for tag in ["打靶", "谱N1200"]:
        vals = eps_windows[tag]
        spread = max(vals.values()) - min(vals.values())
        print("  %s ε 窗口极差=%+.3e（<±0.002%%=±3.6e-7 → 一致；≥0.005%%=±9e-7 → 漂移）" % (tag, spread), flush=True)

    # 判别
    print("", flush=True)
    print("== 判别汇总 ==", flush=True)
    # F：用 128..512 窗口 {δ∞,F} 两参的 F 值（F 层最可能可提取的窗口）
    print("  F 层判别：F/m^4 在 m≥128 贡献 ≤2e-11 << 噪声 ~1e-7 → F 不可提取（P3 分支预期）；"
          "看 {δ∞,F} 两参 RMS 改善与 F 稳定性", flush=True)
    json.dump({"base": "P7-5e-227 json", "windows": {"128_512": [128, 512], "128_1024": [128, 1024], "512_1024": [512, 1024]},
               "note": "F-layer recheck on clean data; eps window consistency"},
              open(os.path.join(BASE, "_phase102_p7_5e228_F_recheck.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
