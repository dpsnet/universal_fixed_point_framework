# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99h：c1/c2 残余修正项系统搜索
================================================================
定案值：c1(0) = 0.30598857、c2(0) = 0.04490656（同窗口 dr→0 外推）
目标形式：
  c1×49 = 14.993440（候选 15 = 1/σ——差 0.044%——搜 15−ε 的 ε）
  c2×200 = 8.981312（候选 9−(1/65) = 8.984615——差 0.037%——也搜 9−ε 的 ε）
框架量集合两/三参数四则组合搜索
"""
import json, os, itertools, math

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# 框架量集合
sig = 1.0/15.0
Q = {
    "sigma": sig, "1/sigma": 15.0, "k_max": 8.0, "N_gen": 3.0, "N_Weyl": 4.0,
    "N'": 5.0, "N'2": 25.0, "alpha0": 0.5, "C": 3.034854, "C2": 9.210340,
    "dH": 2.708050, "kappa": 6.0/math.pi, "CF": 4.0/3.0, "alpha_v": 1.883167,
    "alpha_t": 1.94591, "inv_aEM": 137.028, "Lambda": 210.292, "kL": 401.629,
    "dlam_EM": 0.0229325, "dlam_P20": 0.1220085, "e": math.e, "pi": math.pi,
    "ln2": math.log(2), "ln7": math.log(7), "ln15": math.log(15),
    "40": 40.0, "49": 49.0, "52": 52.0, "64": 64.0, "65": 65.0,
    "3": 3.0, "4": 4.0, "5": 5.0, "7": 7.0, "8": 8.0, "9": 9.0,
    "13": 13.0, "15": 15.0, "16": 16.0, "24": 24.0, "25": 25.0,
    "30": 30.0, "45": 45.0, "60": 60.0, "90": 90.0, "120": 120.0,
    "137": 137.0, "180": 180.0, "200": 200.0, "225": 225.0,
    "2": 2.0, "1": 1.0, "0.5": 0.5, "1/3": 1.0/3.0, "1/7": 1.0/7.0,
    "1/15": sig, "1/40": 0.025, "1/65": 1.0/65.0, "1/52": 1.0/52.0,
    "1/49": 1.0/49.0, "1/25": 0.04, "1/16": 0.0625, "1/8": 0.125,
    "1/200": 0.005, "1/180": 1.0/180.0, "1/137": 1.0/137.028,
}

def search(target, names, tol=2e-5):
    """两参数 + 三参数四则组合搜索命中"""
    hits = []
    items = list(Q.items())
    # 两参数
    for (n1, v1), (n2, v2) in itertools.combinations(items, 2):
        cands = {
            f"{n1}+{n2}": v1+v2, f"{n1}-{n2}": v1-v2, f"{n2}-{n1}": v2-v1,
            f"{n1}*{n2}": v1*v2,
        }
        if v2 != 0: cands[f"{n1}/{n2}"] = v1/v2
        if v1 != 0: cands[f"{n2}/{n1}"] = v2/v1
        for nm, v in cands.items():
            if abs(v-target) < tol*abs(target):
                hits.append((nm, v, (v-target)/target*100))
    # 三参数：a ± b/c 与 a*b/c
    items3 = list(Q.items())
    for (n1, v1), (n2, v2), (n3, v3) in itertools.combinations(items3, 3):
        if abs(v3) > 1e-12:
            cands = {
                f"{n1}+{n2}/{n3}": v1+v2/v3, f"{n1}-{n2}/{n3}": v1-v2/v3,
                f"{n2}-{n1}/{n3}": v2-v1/v3,
            }
            for nm, v in cands.items():
                if abs(v-target) < tol*abs(target):
                    hits.append((nm, v, (v-target)/target*100))
    hits.sort(key=lambda h: abs(h[2]))
    return hits[:15]

print("="*104)
print("P7-5e-99h：c1/c2 残余修正项搜索")
print("="*104)

t_c2 = 8.981312   # c2(0)×200
t_c1 = 14.993440  # c1(0)×49

print("\n★ 目标 c2×200 = %.8f（候选 9−1/65 = 8.984615——差 %.4f%%）" % (t_c2, (8.984615-t_c2)/t_c2*100))
print("  搜索（容差 0.002%）：")
h2 = search(t_c2, "c2", tol=2e-5)
if h2:
    for nm, v, d in h2:
        print("    %s = %.8f——差 %+.6f%%" % (nm, v, d))
else:
    print("    两/三参数组合零命中")

print("\n★ 目标 c1×49 = %.8f（候选 15 = 15.000000——差 %.4f%%）" % (t_c1, (15.0-t_c1)/t_c1*100))
print("  搜索（容差 0.002%）：")
h1 = search(t_c1, "c1", tol=2e-5)
if h1:
    for nm, v, d in h1:
        print("    %s = %.8f——差 %+.6f%%" % (nm, v, d))
else:
    print("    两/三参数组合零命中")

# 反向：c2 的 1/(9−8.981312) 与 c1 的 1/(15−14.99344)
print("\n★ 反向直觉：")
print("  9 − c2×200 = %.8f——1/此值 = %.3f" % (9.0-t_c2, 1.0/(9.0-t_c2)))
print("  15 − c1×49 = %.8f——1/此值 = %.3f" % (15.0-t_c1, 1.0/(15.0-t_c1)))
print("  （若反值接近框架量整数——形式为 9−1/N 或 15−1/N）")

json.dump({"t_c2x200": t_c2, "t_c1x49": t_c1, "hits_c2": h2, "hits_c1": h1},
          open(os.path.join(BASE, "_phase102_p7_5e99h_residual_search.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
