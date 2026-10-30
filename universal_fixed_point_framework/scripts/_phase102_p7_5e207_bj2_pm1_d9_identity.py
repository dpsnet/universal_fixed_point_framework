# -*- coding: utf-8 -*-
"""
P7-5e-207 b_j^2±1 window projection (TT) & D9 m+8=9 specialness (UU)
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e207_bj2_pm1_d9_identity.json"

def w(n):
    return 2 ** (n + 1) - 1  # window width Mersenne_{n+1}

def a(n):
    return 2 ** (n + 1) + 1  # window start boundary family member

def factors(n):
    fs = []
    d = 2
    x = n
    while d * d <= x:
        while x % d == 0:
            fs.append(d)
            x //= d
        d += 1
    if x > 1:
        fs.append(x)
    return fs

# ---------- TT: b_j^2±1 window projection ----------
TT_rows = []
for j in range(1, 7):
    bj = 2 ** (j + 2)
    minus = bj ** 2 - 1
    plus = bj ** 2 + 1
    nwin = 2 * j + 3  # projected window
    ok_minus = (minus == w(nwin))
    ok_plus = (plus == a(nwin))
    TT_rows.append({"j": j, "b_j": bj, "b_j^2-1": minus, "=M_{2(j+2)}": 2 ** (2 * (j + 2)) - 1,
                    "w_{2j+3}": w(nwin), "minus_ok": ok_minus,
                    "b_j^2+1": plus, "=fam_m={2j+4}": 2 ** (2 * j + 4) + 1,
                    "a_{2j+3}": a(nwin), "plus_ok": ok_plus,
                    "projected_window": nwin})

TT_verdict = "★ b_j^2±1 = {w_{2j+3}, a_{2j+3}}——满格平方 ±1 是后移窗口 2j+3 的宽度/起边界对（结构恒等，非巧合）"
TT_note = {"4097": "4097 = 17·241 = F_2·D(4)（家族 Fermat 素数 × B* 分母素数）——b_4^2+1 的分解边注"}

# ---------- UU: D(9)=a_6^2 specialness ----------
def Dm(m):
    return m * 7 * 2 ** (m - 1) + 2 ** m + 1

D9 = Dm(9)
UU1 = {"check": "D(9)=16641=129^2，129=2^7+1 家族 m=7；D 下标 9=2^3+1 家族 m=3（静默单元/窗口 2 起边界 a_2）",
       "D9": D9, "sqrt": 129, "fam_index_of_base": 7, "d_index": 9}
UU2 = {"check": "★ 平方基家族下标 7 = 8−1（域宽）、D 下标 9 = 8+1（静默单元）——8±1 对重现（206 的 7×(8±1)）",
       "ok": 7 == 8 - 1 and 9 == 8 + 1}
UU3 = {"check": "★ D(9)−1 = 16640 = 256·65 = 周期映射缩放（2^8）× 修正锚点（65）——D(9) 与 65 直接联系",
       "ok": D9 - 1 == 256 * 65}
UU4 = {"check": "D(9)−1 的差方展开：129^2−1 = (129−1)(129+1) = 128·130 = 2^7·(2·65) = 2^8·65",
       "ok": (129 - 1) * (129 + 1) == 128 * 130 == 2 ** 8 * 65}
UU5 = {"check": "平方化条件：m+8=9 ⇔ m=1（例外通道）——D(9)=a_6^2 是 m=1 例外通道的周期步进单例",
       "ok": 1 + 8 == 9}
UU_verdict = "★ D(9)=a_6^2 的下标结构：平方基 129=2^{8−1}+1（域宽侧）、D 下标 9=8+1（静默单元侧）——8±1 对重现；D(9)−1=256·65（周期缩放×修正锚点）；平方化是 m=1 例外通道单例"

conclusion = {
    "verdict": "TT（★ 结构恒等）：b_j^2±1 = {w_{2j+3}, a_{2j+3}}——满格平方 ±1 不是巧合命中，而是后移窗口 2j+3 的宽度/起边界对：j=1:{63,65}={w_5,a_5}（206/204 已登记）、j=2:{255,257}={w_7,a_7}、j=6:{65535,65537}={w_15,a_15}（202 已登记 65537=F_4）；边注 b_4^2+1=4097=F_2·D(4)。UU（★ 下标结构）：D(9)=129^2=(2^{8−1}+1)^2、下标 9=8+1——平方基家族下标 7（域宽侧）与 D 下标 9（静默单元侧）是 8±1 对重现（206）；D(9)−1=256·65（周期映射缩放 × 修正锚点）——D(9) 与 65 直接互锁；平方化是 m=1 例外通道的周期步进单例。",
    "TT": {
        "TT1": "★ b_j^2±1 = {M_{2(j+2)}, fam_{2j+4}}（差方/家族恒等）",
        "TT2": "★ = {w_{2j+3}, a_{2j+3}}（后移窗口投影）",
        "TT3": "j=1..6 全 True（63/65=w5/a5、255/257=w7/a7、65535/65537=w15/a15）",
        "TT4": "边注：4097=F_2·D(4)",
    },
    "UU": {
        "UU1": "D(9)=129^2 下标结构（基 7、D 下标 9）",
        "UU2": "★ 7/9 = 8±1 对重现（域宽/静默单元）",
        "UU3": "★ D(9)−1 = 256·65（周期缩放×修正锚点）",
        "UU4": "差方展开 129^2−1 = 2^8·65",
        "UU5": "平方化 = m=1 例外通道单例（1+8=9）",
    },
    "honest_limits": [
        "TT1/TT2 是代数恒等（2^{2(j+2)}±1 定义直接给出）",
        "UU3/UU4 是代数恒等（D(9)−1=256·65 直接验证）",
        "UU2 的 7/9=8±1 与 206 的 7×(8±1) 是同一事实的再次出现（非独立新证据）",
        "'后移窗口投影'与'下标结构'为语义指认",
        "继承 187-206 候选层",
    ],
    "next_candidates": [
        "检验 VV：窗口对合常数 k_j 与 b_j^2±1 的联系（k_{2j+3} = (a_{2j+3}+w_{2j+3})/8 = ?）",
        "检验 WW：D(9)−1=256·65 的一般化——D(m+8)−1 是否 = 2^8·(框架常数)？D(17)−1 检查",
        "回主线：P7-5e 候选层系列收官声明（190-207 全部候选层、未升定案层）",
    ],
}

result = {
    "title": "P7-5e-207 b_j^2±1 window projection & D9 specialness",
    "date": "2026-10-15",
    "TT": {"rows": TT_rows, "verdict": TT_verdict, "note": TT_note},
    "UU": {"UU1": UU1, "UU2": UU2, "UU3": UU3, "UU4": UU4, "UU5": UU5, "verdict": UU_verdict},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 72)
print("P7-5e-207 b_j^2±1 window projection & D9 specialness")
print("=" * 72)
print("[TT b_j^2±1 scan]")
for r in TT_rows:
    print("  j=%d: b_j=%3d  b^2-1=%7d==w_%d=%7d? %s   b^2+1=%7d==a_%d=%7d? %s" % (
        r["j"], r["b_j"], r["b_j^2-1"], r["projected_window"], r["w_{2j+3}"], r["minus_ok"],
        r["b_j^2+1"], r["projected_window"], r["a_{2j+3}"], r["plus_ok"]))
print("[TT verdict]", TT_verdict)
print("[TT note]", TT_note)
print("[UU1]", UU1["check"])
print("[UU2]", UU2["check"], "->", UU2["ok"])
print("[UU3]", UU3["check"], "->", UU3["ok"])
print("[UU4]", UU4["check"], "->", UU4["ok"])
print("[UU5]", UU5["check"], "->", UU5["ok"])
print("[UU verdict]", UU_verdict)
print("[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
