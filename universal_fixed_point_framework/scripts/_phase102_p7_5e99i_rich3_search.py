# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99i：三阶 Richardson + 收紧容差精确身份搜索
================================================================
四档 dr 数据（99g）：c1 = 0.30585653/0.30595380/0.30597971/0.30598653
                        c2 = 0.04487366/0.04489789/0.04490434/0.04490606
三阶 Richardson（c = c0 + a·dr² + b·dr⁴）确认外推饱和
再用 c1(0)/c2(0) 三阶值做容差 5e-6 搜索
"""
import json, os, itertools, math

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

c1s = [0.30585653, 0.30595380, 0.30597971, 0.30598653]
c2s = [0.04487366, 0.04489789, 0.04490434, 0.04490606]
drs = [0.02, 0.01, 0.005, 0.0025]

def rich3(vals):
    """四档 dr 的三阶 Richardson（消去 dr² 与 dr⁴）"""
    # 二阶一次：v1_i = (4·v_{i+1} − v_i)/3
    v1 = [(4*vals[i+1]-vals[i])/3 for i in range(3)]
    # 二阶二次（dr 减半）：v2_i = (16·v1_{i+1} − v1_i)/15
    v2 = [(16*v1[i+1]-v1[i])/15 for i in range(2)]
    # 三阶：v3 = (64·v2_1 − v2_0)/63
    v3 = (64*v2[1]-v2[0])/63
    return v1, v2, v3

c1_1, c1_2, c1_3 = rich3(c1s)
c2_1, c2_2, c2_3 = rich3(c2s)

print("="*104)
print("P7-5e-99i：三阶 Richardson 外推 + 收紧搜索")
print("="*104)
print("\n★ c1 外推链：二阶1 = %.9f、二阶2 = %.9f、三阶 = %.9f" % (c1_1[1], c1_2[0], c1_3))
print("  c1(0) 定案 = %.9f（三阶）——vs 二阶 0.30598857：差 %+.7f%%" % (c1_3, (c1_3-0.30598857)/0.30598857*100))
print("\n★ c2 外推链：二阶1 = %.9f、二阶2 = %.9f、三阶 = %.9f" % (c2_1[1], c2_2[0], c2_3))
print("  c2(0) 定案 = %.9f（三阶）——vs 二阶 0.04490656：差 %+.7f%%" % (c2_3, (c2_3-0.04490656)/0.04490656*100))

# 收紧容差搜索
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
    "137": 137.0, "150": 150.0, "180": 180.0, "200": 200.0, "225": 225.0,
    "2": 2.0, "1": 1.0, "0.5": 0.5, "1/3": 1.0/3.0, "1/7": 1.0/7.0,
    "1/15": sig, "1/40": 0.025, "1/65": 1.0/65.0, "1/52": 1.0/52.0,
    "1/49": 1.0/49.0, "1/25": 0.04, "1/16": 0.0625, "1/8": 0.125,
    "1/150": 1.0/150.0, "1/200": 0.005, "1/180": 1.0/180.0, "1/137": 1.0/137.028,
    "2/3": 2.0/3.0, "3/4": 0.75, "4/3": 4.0/3.0,
}

def search(target, tol=5e-6):
    hits = []
    items = list(Q.items())
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
    for (n1, v1), (n2, v2), (n3, v3) in itertools.combinations(items, 3):
        if abs(v3) > 1e-12:
            cands = {
                f"{n1}+{n2}/{n3}": v1+v2/v3, f"{n1}-{n2}/{n3}": v1-v2/v3,
                f"{n2}-{n1}/{n3}": v2-v1/v3,
            }
            for nm, v in cands.items():
                if abs(v-target) < tol*abs(target):
                    hits.append((nm, v, (v-target)/target*100))
    hits.sort(key=lambda h: abs(h[2]))
    return hits[:12]

t_c1 = c1_3*49  # c1×49 目标
t_c2 = c2_3*200  # c2×200 目标

print("\n★ 目标 c2×200 = %.7f（三阶）" % t_c2)
print("  搜索（容差 0.0005%）：")
h2 = search(t_c2)
if h2:
    for nm, v, d in h2:
        print("    %s = %.7f——差 %+.6f%%" % (nm, v, d))
else:
    print("    零命中")

print("\n★ 目标 c1×49 = %.7f（三阶）" % t_c1)
print("  搜索（容差 0.0005%）：")
h1 = search(t_c1)
if h1:
    for nm, v, d in h1:
        print("    %s = %.7f——差 %+.6f%%" % (nm, v, d))
else:
    print("    零命中")

print("\n★ 候选命中回顾（三阶值）：")
cands1 = {"15/49": 15.0/49.0, "(15-1/150)/49": (15.0-1.0/150.0)/49.0,
          "(15-1/152.4)/49": (15.0-1.0/152.4)/49.0}
for nm, v in cands1.items():
    print("  c1: %s = %.8f——vs %.8f：差 %+.6f%%" % (nm, v, c1_3, (v-c1_3)/c1_3*100))
cands2 = {"(9-1/65)/200": (9.0-1.0/65.0)/200.0, "(k_max+kappa/ln7)/200": (8.0+6.0/math.pi/math.log(7))/200.0,
          "9/200": 9.0/200.0, "(9-1/52)/200": (9.0-1.0/52.0)/200.0}
for nm, v in cands2.items():
    print("  c2: %s = %.8f——vs %.8f：差 %+.6f%%" % (nm, v, c2_3, (v-c2_3)/c2_3*100))

json.dump({"c1_rich3": c1_3, "c2_rich3": c2_3, "hits_c2": h2, "hits_c1": h1},
          open(os.path.join(BASE, "_phase102_p7_5e99i_rich3_search.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
