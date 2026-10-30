# -*- coding: utf-8 -*-
"""
P7-5e-232c：C/D 联合四参低 m 复核（打靶 + N=1200 双通道）
====================================================================
四参 {δ∞,C,D,E} 在低 m 段（33..129/33..256/33..512）——解 C/D/E 相关，
  判 C=13/128、D≈0.01985 在 E 自由下是否稳定；E 是否收敛到可信值。
先验：P1 四参 C 仍在 13/128 ±0.5% → C 锁定加强；P2 D 在 ~0.0199 ±5% → D 真实值确认；
  P3 E 收敛（窗口间 <30%）→ E 候选身份可搜；P4 E 发散 → E 结构性不可分维持。
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0

def load():
    j = json.load(open(os.path.join(BASE, "_phase102_p7_5e230c_shoot_full_chain.json"), encoding="utf-8"))
    shoot = {int(k): v["delta"] for k, v in j["out"].items()}
    j2 = json.load(open(os.path.join(BASE, "_phase102_p7_5e229_lowm_N1200.json"), encoding="utf-8"))
    j3 = json.load(open(os.path.join(BASE, "_phase102_p7_5e227_dinf_final_shoot_ext.json"), encoding="utf-8"))
    spec = {int(k): v["delta"] for k, v in j2["out"].items()}
    for mm in j3["ms"]:
        spec.setdefault(abs(mm), j3["spectral"][str(-mm)]["delta"])
    return shoot, spec

if __name__ == "__main__":
    shoot, spec = load()
    print("== P7-5e-232c：C/D 联合四参低 m 复核 ==", flush=True)
    for tag, data in [("打靶", shoot), ("N=1200", spec)]:
        print("", flush=True)
        print("---- %s ----" % tag, flush=True)
        for lo, hi, lab in [(33, 129, "33..129"), (33, 161, "33..161"), (33, 256, "33..256"), (33, 512, "33..512")]:
            msf = np.array([m for m in data if lo <= m <= hi], dtype=float)
            ds = np.array([data[m] for m in data if lo <= m <= hi])
            # 四参 {δ∞,C,D,E}
            X4 = np.vstack([np.ones_like(msf), 1.0/msf, 1.0/msf**2, 1.0/msf**3]).T
            c4 = np.linalg.lstsq(X4, ds, rcond=None)[0]
            r4 = float(np.sqrt(np.mean((X4@c4-ds)**2)))
            # 三参 {δ∞,C,D} E 固定
            X3 = np.vstack([np.ones_like(msf), 1.0/msf, 1.0/msf**2]).T
            c3 = np.linalg.lstsq(X3, ds - E39/msf**3, rcond=None)[0]
            r3 = float(np.sqrt(np.mean((X3@c3-(ds-E39/msf**3))**2)))
            print("  [%s] N=%d" % (lab, len(msf)), flush=True)
            print("    四参: δ∞ dev %+.5f pct C=%.7f(vs13/128 %+.3f pct) D=%.6f(vs41/2000 %+.2f pct) E=%+.6f RMS=%.2e" %
                  ((c4[0]-INV56)/INV56*100, c4[1], (c4[1]-C13)/C13*100, c4[2], (c4[2]-D41)/D41*100, c4[3], r4), flush=True)
            print("    三参(E39): δ∞ dev %+.5f pct C=%.7f(vs13/128 %+.3f pct) D=%.6f(vs41/2000 %+.2f pct) RMS=%.2e" %
                  ((c3[0]-INV56)/INV56*100, c3[1], (c3[1]-C13)/C13*100, c3[2], (c3[2]-D41)/D41*100, r3), flush=True)

    json.dump({"base": "4-param C/D/E recheck low-m (shoot+spec)",
               "note": "C/D stability under E free"},
              open(os.path.join(BASE, "_phase102_p7_5e232c_4param_lowm.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)
    print("JSON 落盘 OK exit 0", flush=True)
