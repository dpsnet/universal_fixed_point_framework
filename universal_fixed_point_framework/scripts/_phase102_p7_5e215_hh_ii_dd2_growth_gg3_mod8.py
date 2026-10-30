# -*- coding: utf-8 -*-
"""
P7-5e-215 HH: DD2-family growth law n_{j+3} = 64*n_j + 9
        II: GG-family mod-8 classes (n ≡ 2, m ≡ 3k+2 mod 8)
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e215_hh_ii_dd2_growth_gg3_mod8.json"

# ---------- HH: DD2 growth ----------
# n_j = (2^(2j+4)-1)/7 for j ≡ 1 mod 3; l_j = 7n_j+2 = 2^(2j+4)+1
def n_j(j):
    return (2 ** (2 * j + 4) - 1) // 7

def l_j(j):
    return 7 * n_j(j) + 2

HH_rows = []
js = [1, 4, 7, 10]
for i in range(len(js) - 1):
    j, jp = js[i], js[i + 1]
    HH_rows.append({"j": j, "n_j": n_j(j), "n_jp3": n_j(jp),
                    "64nj+9": 64 * n_j(j) + 9,
                    "ok_n": n_j(jp) == 64 * n_j(j) + 9,
                    "l_j": l_j(j), "l_jp3": l_j(jp),
                    "ok_l": l_j(jp) == 64 * l_j(j) - 63})

HH1 = {"check": "★ HH1: DD2 族 n 增长律 n_{j+3} = 64·n_j + 9——64 = b_1²（满格平方 8²）、9 = 静默单元（2^3+1）——框架量族内递推闭合（(64A−1)/7 与 (A−1)/7 的关系）",
       "all_ok": all(r["ok_n"] for r in HH_rows), "rows": HH_rows}
HH2 = {"check": "★ HH2: 线性因子增长律 l_{j+3} = 64·l_j − 63——63 = 窗口宽度 w_5 = b_1²−1（8²−1）——满格平方×线性因子 − 窗口宽度",
       "all_ok": all(r["ok_l"] for r in HH_rows)}
HH3 = {"check": "HH3: 递推在族内闭合（j ≡ 1 mod 3 保持 +3 不变量）——增长因子 64 = 2^6（8²）非 2^6=64 的幂集步进（步进 8 = k_max 的平方）",
       "growth": 64, "note": "64 = 8²（满格平方 b_1²）且 2^6（6 个 2 进单元）"}

# ---------- II: GG mod 8 ----------
GG_rows = []
for k in range(1, 8):
    a = 3 * k + 1
    n = (2 ** a - 2) // 7
    m = n + 3 * k
    GG_rows.append({"k": k, "n": n, "n_mod8": n % 8, "m": m, "m_mod8": m % 8,
                    "n_ok": n % 8 == 2, "m_ok": m % 8 == (3 * k + 2) % 8})

II1 = {"check": "★ II1: CC3 族 n ≡ 2 mod 8 恒成立——7n = 2^{3k+1}−2 ≡ 6 mod 8（2^{≥3}≡0）⇒ n ≡ 6·7^{-1} ≡ 42 ≡ 2 mod 8",
       "all_ok": all(r["n_ok"] for r in GG_rows)}
II2 = {"check": "★ II2: m = n+3k ≡ 3k+2 mod 8——相邻差 m_{k+1}−m_k = 2^{3k+1}+3 ≡ 3 mod 8（周期 8，遍历 8 类）",
       "all_ok": all(r["m_ok"] for r in GG_rows)}
II3 = {"check": "II3: D(n)=2^m+1 下标 m 无 mod 8 约束（任何 m 均可）；m ≥ 3 自动满足 D ≡ 1 mod 8（210 已知核对）——GG 族 m 全 ≥ 5",
       "all_m_ge3": all(r["m"] >= 3 for r in GG_rows)}

conclusion = {
    "verdict": "HH（DD2 增长律）：★ n_{j+3} = 64·n_j + 9（64=b_1² 满格平方、9=静默单元）——n=9→585→37449→2396745 精确递推；★ 线性因子 l_{j+3} = 64·l_j − 63（63=窗口宽度 b_1²−1）——65→4097→262145 精确递推；增长因子 64 = 8²（满格平方）且 = 2^6。II（GG 模类）：★ CC3 族 n ≡ 2 mod 8 恒成立（7n≡6 mod 8）；★ m = n+3k ≡ 3k+2 mod 8（相邻差 3 mod 8，遍历 8 类：5,0,3,6,1,4,7,2）；D(n)=2^m+1 下标无 mod 8 约束（m≥3 自动满足 D≡1 mod 8）。",
    "HH": {"HH1": HH1, "HH2": HH2, "HH3": HH3},
    "II": {"II1": II1, "II2": II2, "II3": II3},
    "honest_limits": [
        "HH1/HH2 是代数递推（恒等化简，非独立机制）",
        "HH3 的 64=8² 是身份核对（满格平方）",
        "II1/II2 是模算术（2^{≥3}≡0 mod 8）",
        "II3 是已知核对（210）",
        "继承 187-214 候选层",
    ],
    "next_candidates": [
        "检验 JJ：HH 递推的 j 每 +3 是否对应框架 2^6 幂集步进（步进 8 的平方）——与 Bott 周期 8 的联结",
        "检验 KK：II 的 m ≡ 3k+2 mod 8 与静默单元家族 2^m+1 的单位位 m 序列（m=3,4,5,6,7,8）的交集（m=5 已见）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-216",
    ],
}

result = {
    "title": "P7-5e-215 HH: DD2 growth n_{j+3}=64n_j+9; II: GG mod-8 classes",
    "date": "2026-10-16",
    "HH": {"rows": HH_rows, "HH1": HH1, "HH2": HH2, "HH3": HH3},
    "II": {"rows": GG_rows, "II1": II1, "II2": II2, "II3": II3},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-215 HH/II: DD2 growth & GG mod-8 classes")
print("=" * 76)
print("[HH DD2 growth]")
for r in HH_rows:
    print("  j=%d n=%7d -> n+3=%7d 64n+9=%7d ok=%s | l=%7d -> %7d 64l-63=%7d ok=%s" % (
        r["j"], r["n_j"], r["n_jp3"], r["64nj+9"], r["ok_n"], r["l_j"], r["l_jp3"], r["64nj+9"], r["ok_l"]))
print("[HH1]", HH1["check"], "-> all_ok=%s" % HH1["all_ok"])
print("[HH2]", HH2["check"], "-> all_ok=%s" % HH2["all_ok"])
print("[II GG mod8]")
for r in GG_rows:
    print("  k=%d n=%6d n%%8=%d ok=%s m=%7d m%%8=%d ok=%s" % (
        r["k"], r["n"], r["n_mod8"], r["n_ok"], r["m"], r["m_mod8"], r["m_ok"]))
print("[II1]", II1["check"], "-> all_ok=%s" % II1["all_ok"])
print("[II2]", II2["check"], "-> all_ok=%s" % II2["all_ok"])
print("[II3]", II3["check"], "-> all_m_ge3=%s" % II3["all_m_ge3"])
print("[Conclusion]", conclusion["verdict"])
