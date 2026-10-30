# -*- coding: utf-8 -*-
"""
P7-5e-232：高 m 段残留结构识别（512..1024 RMS 5.6e-7 来源）
====================================================================
数据：打靶 16 点（230c）+ N=1200 16 点（229/227）。
锁定模型：δ(m) = 1/56 + ε_w − C/m − D/m² + E/m³（ε_w=+0.215e-6 低 m 段打靶值，
  C=13/128、D=41/2000、E=39/2000）。
残差 r(m) 形态判别：常数偏移（δ∞ 漂移）/ 1/m（C 漂移）/ 1/m²（D 漂移）/ m 幂律（新项）。
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0
EPS_W = 0.215e-6

def load_points():
    j = json.load(open(os.path.join(BASE, "_phase102_p7_5e230c_shoot_full_chain.json"), encoding="utf-8"))
    shoot = {int(k): v["delta"] for k, v in j["out"].items()}
    j2 = json.load(open(os.path.join(BASE, "_phase102_p7_5e229_lowm_N1200.json"), encoding="utf-8"))
    j3 = json.load(open(os.path.join(BASE, "_phase102_p7_5e227_dinf_final_shoot_ext.json"), encoding="utf-8"))
    spec = {int(k): v["delta"] for k, v in j2["out"].items()}
    for mm in j3["ms"]:
        spec.setdefault(abs(mm), j3["spectral"][str(-mm)]["delta"])
    return shoot, spec

if __name__ == "__main__":
    shoot, spec = load_points()
    ms_all = sorted(shoot.keys())
    print("== P7-5e-232：高 m 段残留结构识别 ==", flush=True)
    print("  锁定模型：δ(m)=1/56+%+.3e −13/128/m −41/2000/m² +39/2000/m³" % EPS_W, flush=True)

    print("", flush=True)
    print("  m     | 打靶 δ        | 模型          | r(打靶)      | N=1200 r      | Δ(打靶-N1200)", flush=True)
    r_shoot = {}
    r_spec = {}
    for m in ms_all:
        mod = INV56 + EPS_W - C13/m - D41/m**2 + E39/m**3
        rs = shoot[m] - mod
        rp = spec[m] - mod
        r_shoot[m] = rs
        r_spec[m] = rp
        print("  %4d | %.10f | %.10f | %+.2e | %+.2e | %+.2e" %
              (m, shoot[m], mod, rs, rp, shoot[m]-spec[m]), flush=True)

    print("", flush=True)
    print("== 残差主导成分判别（高 m 段 m≥256）==", flush=True)
    for tag, r in [("打靶", r_shoot), ("N=1200", r_spec)]:
        print("---- %s ----" % tag, flush=True)
        for lo, hi, lab in [(256, 1024, "256..1024"), (512, 1024, "512..1024")]:
            msf = np.array([m for m in ms_all if lo <= m <= hi], dtype=float)
            rr = np.array([r[m] for m in ms_all if lo <= m <= hi])
            # 模型 A：常数
            cA = np.mean(rr); rA = np.sqrt(np.mean((rr-cA)**2))
            # 模型 B：常数 + a/m
            XB = np.vstack([np.ones_like(msf), 1.0/msf]).T
            cB = np.linalg.lstsq(XB, rr, rcond=None)[0]
            rB = np.sqrt(np.mean((XB@cB-rr)**2))
            # 模型 C：常数 + b/m²
            XC = np.vstack([np.ones_like(msf), 1.0/msf**2]).T
            cC = np.linalg.lstsq(XC, rr, rcond=None)[0]
            rC = np.sqrt(np.mean((XC@cC-rr)**2))
            # 模型 D：常数 + d·m（线性漂移）
            XD = np.vstack([np.ones_like(msf), msf]).T
            cD = np.linalg.lstsq(XD, rr, rcond=None)[0]
            rD = np.sqrt(np.mean((XD@cD-rr)**2))
            # 模型 E：常数 + a/m + b/m²
            XE = np.vstack([np.ones_like(msf), 1.0/msf, 1.0/msf**2]).T
            cE = np.linalg.lstsq(XE, rr, rcond=None)[0]
            rE = np.sqrt(np.mean((XE@cE-rr)**2))
            print("  [%s] N=%d" % (lab, len(msf)), flush=True)
            print("    const:        RMS=%.2e (均值 %+.2e)" % (rA, cA), flush=True)
            print("    const+a/m:    a=%+.3e RMS=%.2e (改善 %.1fx)" % (cB[1], rB, rA/rB if rB > 0 else float('inf')), flush=True)
            print("    const+b/m^2:  b=%+.3e RMS=%.2e (改善 %.1fx)" % (cC[1], rC, rA/rC if rC > 0 else float('inf')), flush=True)
            print("    const+d*m:    d=%+.2e RMS=%.2e (改善 %.1fx)" % (cD[1], rD, rA/rD if rD > 0 else float('inf')), flush=True)
            print("    const+a/m+b/m^2: a=%+.3e b=%+.3e RMS=%.2e" % (cE[1], cE[2], rE), flush=True)

    print("", flush=True)
    print("== C_eff(m) = (1/56+ε_w − δ(m))·m 收敛性 ==", flush=True)
    for tag, r in [("打靶", r_shoot), ("N=1200", r_spec)]:
        print("---- %s ----" % tag, flush=True)
        for m in ms_all:
            c_eff = (INV56 + EPS_W - shoot[m])*m
            print("  m=%4d C_eff=%.7f" % (m, c_eff), flush=True)
        break  # 打靶为主

    # 高 m 段 C_eff 平均 vs 低 m 段
    msf_l = np.array([m for m in ms_all if 33 <= m <= 129], dtype=float)
    msf_h = np.array([m for m in ms_all if 512 <= m <= 1024], dtype=float)
    ce_l = np.mean([(INV56 + EPS_W - shoot[m])*m for m in msf_l])
    ce_h = np.mean([(INV56 + EPS_W - shoot[m])*m for m in msf_h])
    print("  C_eff 低 m 段(33..129)=%.6f vs 高 m 段(512..1024)=%.6f（差 %+.3f pct）" %
          (ce_l, ce_h, (ce_h-ce_l)/ce_l*100), flush=True)

    json.dump({"base": "locked model 1/56+eps_w-C/D/E", "eps_w": EPS_W,
               "resid": {str(m): {"shoot": r_shoot[m], "spec": r_spec[m]} for m in ms_all}},
              open(os.path.join(BASE, "_phase102_p7_5e232_highm_residual.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
