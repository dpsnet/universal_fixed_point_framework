# -*- coding: utf-8 -*-
"""
P7-5e-232e：纯求根通道（Newton 细化）数据重拟合判别
====================================================================
232/232b/232d 判别：三次拟合求根的高 m 段线性残差（+2.4~2.9e-9·m）与
  ε 窗口漂移（+0.2~2.0e-6）= 三次拟合外推系统残差伪影；
  纯求根通道（Newton 细化）残差全程平坦 ≈ −ε_w → ε→0、δ∞=1/56 候选精确。
本脚本用纯求根数据（N=1200 Newton 9 点 232b + 打靶 Newton 3 点 232d）重拟合：
  P1 ε(单参)≈0 → δ∞=1/56 精确候选确认；
  P2 C 仍 ≈13/128（±0.2%）→ C 锁定在纯求根通道维持；
  P3 D 变化 → 三次拟合版 D 含 ε 污染，需更新；
  P4 E 不可辨（同 232c）→ 维持结构性不可分。
"""
import numpy as np

C13 = 13.0/128.0
D41 = 41.0/2000.0
E39 = 39.0/2000.0
INV56 = 1.0/56.0

# 纯求根数据：N=1200 Newton（232b 9 点）+ 打靶 Newton（232d 3 点）
data = {
    # m: (delta_N1200_newton, delta_shoot_newton)
    33: (0.0147612114, 0.0147612124),
    129: (0.0170686135, 0.0170686256),
    256: (0.0174601028, 0.0174601188),
    512: (0.0176587002, None),
    513: (0.0176590879, None),
    640: (0.0176984059, None),
    768: (0.0177248656, None),
    896: (0.0177437580, None),
    1024: (0.0177579553, None),
}

def fit(ms, ds, cols, y_shift=None):
    msf = np.array(ms, dtype=float)
    y = np.array(ds, dtype=float)
    if y_shift is not None:
        y = y + y_shift(msf)
    X = np.vstack(cols(msf)).T
    c = np.linalg.lstsq(X, y, rcond=None)[0]
    rms = float(np.sqrt(np.mean((y - X@c)**2)))
    return c, rms

if __name__ == "__main__":
    print("== P7-5e-232e：纯求根通道数据重拟合 ==", flush=True)
    for tag, pick in [("N=1200 Newton", lambda v: v[0]), ("打靶 Newton(3点)", lambda v: v[1])]:
        ms_all = [m for m in sorted(data) if pick(data[m]) is not None]
        ds_all = [pick(data[m]) for m in ms_all]
        print("", flush=True)
        print("---- %s（%d 点 %s..%d）----" % (tag, len(ms_all), ms_all[0], ms_all[-1]), flush=True)
        # ε 单参（C/D/E 锁定）
        c, r = fit(ms_all, ds_all, lambda m: [np.ones_like(m)],
                   lambda m: C13/m + D41/m**2 - E39/m**3)
        print("  ε单参: ε=δ∞−1/56=%+.3e（dev %+.6f pct）RMS=%.2e" % (c[0]-INV56, (c[0]-INV56)/INV56*100, r), flush=True)
        # 三参 {δ∞,C,D} E 固定
        c, r = fit(ms_all, ds_all, lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2],
                   lambda m: -E39/m**3)
        print("  三参: δ∞ dev %+.5f pct C=%.7f(vs13/128 %+.3f pct) D=%.6f(vs41/2000 %+.2f pct) RMS=%.2e" %
              ((c[0]-INV56)/INV56*100, c[1], (c[1]-C13)/C13*100, c[2], (c[2]-D41)/D41*100, r), flush=True)
        # 四参 {δ∞,C,D,E}
        c, r = fit(ms_all, ds_all, lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2, 1.0/m**3])
        print("  四参: δ∞ dev %+.5f pct C=%.7f D=%.6f E=%+.6f RMS=%.2e" %
              ((c[0]-INV56)/INV56*100, c[1], c[2], c[3], r), flush=True)
        # 低 m 段三参 [33..129/256]
        for lo, hi, lab in [(33, 129, "33..129"), (33, 256, "33..256")]:
            ms_l = [m for m in ms_all if lo <= m <= hi]
            ds_l = [pick(data[m]) for m in ms_l]
            c, r = fit(ms_l, ds_l, lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2],
                       lambda m: -E39/m**3)
            print("  [%s] 三参: δ∞ dev %+.5f pct C=%.7f(vs13/128 %+.3f pct) D=%.6f(vs41/2000 %+.2f pct) RMS=%.2e" %
                  (lab, (c[0]-INV56)/INV56*100, c[1], (c[1]-C13)/C13*100, c[2], (c[2]-D41)/D41*100, r), flush=True)

    # 三次拟合版对比（230c/229b 数据）
    import json, os
    BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
    j = json.load(open(os.path.join(BASE, "_phase102_p7_5e230c_shoot_full_chain.json"), encoding="utf-8"))
    ms_all = [int(k) for k in j["out"]]
    ds_all = [j["out"][k]["delta"] for k in sorted(j["out"], key=int)]
    ms_all = sorted(j["out"], key=int)
    ds_all = [j["out"][k]["delta"] for k in ms_all]
    print("", flush=True)
    print("---- 打靶三次拟合版（230c 全链 %d 点）对比 ----" % len(ms_all), flush=True)
    for lo, hi, lab in [(33, 129, "33..129"), (33, 1024, "33..1024")]:
        ms_l = [m for m in ms_all if lo <= m <= hi]
        ds_l = [ds_all[ms_all.index(m)] for m in ms_l]
        c, r = fit(ms_l, ds_l, lambda m: [np.ones_like(m), 1.0/m, 1.0/m**2],
                   lambda m: -E39/m**3)
        print("  [%s] 三参: δ∞ dev %+.5f pct C=%.7f(vs13/128 %+.3f pct) D=%.6f(vs41/2000 %+.2f pct) RMS=%.2e" %
              (lab, (c[0]-INV56)/INV56*100, c[1], (c[1]-C13)/C13*100, c[2], (c[2]-D41)/D41*100, r), flush=True)
    print("", flush=True)
    print("== 判别汇总 ==", flush=True)
    print("  P1 ε(纯求根单参)≈0 → δ∞=1/56 精确候选（三次拟合版 ε=+0.2~2.0e-6 为伪影）", flush=True)
    print("  P2 C 纯求根 vs 13/128 → 偏差量级", flush=True)
    print("  P3 D 纯求根 vs 41/2000 → 偏差量级", flush=True)
