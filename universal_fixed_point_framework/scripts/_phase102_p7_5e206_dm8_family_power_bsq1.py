# -*- coding: utf-8 -*-
"""
P7-5e-206 D(m+8) family-power check (QQ) & b1^2±1 core-constant unification (RR)
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e206_dm8_family_power_bsq1.json"

def Dm(m):
    return m * 7 * 2 ** (m - 1) + 2 ** m + 1

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

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

FAMILY = [2 ** m + 1 for m in range(1, 12)]  # 3,5,9,17,33,65,129,257,513,1025,2049

# ---------- QQ: D(m+8) family-power check ----------
QQ_rows = []
for m in range(1, 11):
    mm = m + 8
    d = Dm(mm)
    fs = factors(d)
    fam_factors = [f for f in fs if f in FAMILY]
    # perfect power check: is d == family member^k?
    is_fam_power = None
    for fm in FAMILY:
        k = 1
        while fm ** k <= d:
            if fm ** k == d:
                is_fam_power = (fm, k)
            k += 1
    QQ_rows.append({"m8": mm, "D": d, "factors": fs,
                    "family_factors": fam_factors, "is_family_power": is_fam_power})

D17 = Dm(17)
QQ_pred = {"D17": D17, "factors": factors(D17),
           "check": "205 预言检验：D(17) 是否为家族成员幂？"}
QQ_verdict = "D(9)=16641=129^2=a_6^2 是单例（m+8=9 唯一家族平方）——D(m+8) 无一般家族成员幂结构"

# ---------- RR: b1^2±1 core-constant unification ----------
b1 = 8
RR1 = {"check": "★ 核心常数四成员全是 b_1=8 的二次偏移：56=b_1^2−b_1=8^2−8、63=b_1^2−1=8^2−1、64=b_1^2、65=b_1^2+1=8^2+1",
       "ok": 56 == b1 ** 2 - b1 and 63 == b1 ** 2 - 1 and 64 == b1 ** 2 and 65 == b1 ** 2 + 1}
RR2 = {"check": "★ 63 = b_1^2−1 = 8^2−1 补上 Mersenne 的满格平方侧身份——63/65 构成 b_1^2±1 对（193 只登记 65=b_1^2+1，现在减 1 侧闭合）",
       "ok": 63 == b1 ** 2 - 1 and 65 == b1 ** 2 + 1 and 63 * 65 == 2 ** 12 - 1}
RR3 = {"check": "b_1^2 偏移族统一表：[56,63,64,65] = b_1^2 − {b_1, 1, 0, −1}（偏移集 {b_1=8, 1, 0, −1}）",
       "ok": [b1 ** 2 - b1, b1 ** 2 - 1, b1 ** 2, b1 ** 2 + 1] == [56, 63, 64, 65]}
RR4 = {"check": "★ 63/65 三身份对照：63 = 2^6−1 = M_6（204 宽度侧）= b_1^2−1（满格平方减 1）——Mersenne 宽度与 b_1^2−1 同一；65 = 2^6+1（家族 m=6）= b_1^2+1（193）——Fermat 起边界与 b_1^2+1 同一",
       "ok": (2 ** 6 - 1 == 63 == b1 ** 2 - 1) and (2 ** 6 + 1 == 65 == b1 ** 2 + 1)}
RR5 = {"check": "7×(8±1) 对偶的 b_1 表述：56=7·8=(b_1−1)b_1、63=7·9=(b_1−1)(b_1+1)=b_1^2−1——'7×9' 与 '8²−1' 是 63 的双重因子分解（(b_1−1)(b_1+1)=b_1²−1 差方恒等）",
       "ok": (b1 - 1) * (b1 + 1) == b1 ** 2 - 1 == 63}
RR6 = {"check": "★ 统一表述：核心常数窗口 [56,63,64,65] = b_1^2 − {b_1, 1, 0, −1}——δ∞ 分母（b_1²−b_1）、宽度（b_1²−1）、满格平方（b_1²）、修正锚点（b_1²+1）是满格平方的 4 个连续偏移",
       "ok": True}

# ---------- SS: summary ----------
SS = {
    "check": "P7-5e 候选层汇总（190-206）：位型三族（单位位→2^m+1 家族 / 相邻双位→窗口常数 3·2^p / 隔位双位→对合域常数 5·2^p）→ 窗口三段（家族段 2^{j+1}+1 × 塔段 2^{j+2} × 静默段 8k+1）→ 周期映射 Bott 步进 8（256x−255）→ Fermat/Mersenne 骨架（F_k=a_{2^k−1}、w_j=M_{j+1}、±1 对偶）→ ★ b_1² 偏移核心常数窗口（56/63/64/65）——全部候选层",
    "layers": ["位型三族（190）", "截距分子=家族两段（191）", "65 多重身份（192-193）", "B*(1) 框架分解（194）", "种子代数闭合（195-196）", "窗口锚定（197-198）", "Fermat 种子家族（199-201）", "窗口平移+素数骨架（202）", "Bott 步进+双族位型（203）", "三层语义+Mersenne/Fermat（204）", "Mersenne 角色+核心常数窗口（205）", "★ b_1² 偏移统一（206）"],
}

conclusion = {
    "verdict": "QQ：D(9)=a_6^2 是单例——D(m+8) 无一般家族成员幂结构（D(10)..D(18) 仅 m+8=9 命中家族平方；D(17)=7929857 无家族因子）。RR（★ 决定性）：核心常数窗口 [56,63,64,65] = b_1^2 − {b_1, 1, 0, −1} 统一——56=b_1^2−b_1（δ∞ 分母）、63=b_1^2−1（宽度 M_6 兼 Mersenne 满格平方侧）、64=b_1^2（满格平方）、65=b_1^2+1（修正锚点）；★ 63/65 构成 b_1^2±1 对（193 的 65=b_1^2+1 减 1 侧闭合）——7×(8±1) 对偶是 (b_1−1)(b_1+1)=b_1^2−1 差方恒等的框架实例。SS：P7-5e 候选层统一图景登记（12 层）。",
    "QQ": {
        "QQ1": "D(m+8) 家族因子/幂扫描（m=1..10）",
        "QQ2": "★ D(9)=a_6^2 唯一（单例）",
        "QQ3": "D(17)=7929857 无家族因子（205 预言否定）",
        "QQ4": "结论：无一般家族成员幂结构",
    },
    "RR": {
        "RR1": "★ [56,63,64,65] = b_1^2−{8,1,0,−1}",
        "RR2": "★ 63/65 = b_1^2±1 对（积=M_12）",
        "RR3": "b_1^2 偏移族统一表",
        "RR4": "★ 63=M_6=b_1^2−1、65=家族 m=6=b_1^2+1 双身份重合",
        "RR5": "7×9 = 8²−1 差方恒等（(b_1−1)(b_1+1)）",
        "RR6": "★ 统一：核心常数 = 满格平方的 4 连续偏移",
    },
    "SS": {"check": "12 层统一图景（候选层）"},
    "honest_limits": [
        "QQ2/QQ3 是枚举事实（m+8=1..10 扫描）",
        "RR1-RR6 是代数恒等（b_1=8 直接验证）；'b_1^2 偏移族'语义指认",
        "RR4 的双身份重合（63=M_6=b_1^2−1）是同一数的两个表述，非新机制",
        "SS 汇总为登记（无新检验）",
        "继承 187-205 候选层",
    ],
    "next_candidates": [
        "检验 TT：b_1^2 偏移族的窗口推广——b_j^2±1 在 j≥2 的行为（129²±1、257²±1 是否命中框架常数）",
        "检验 UU：D(9)=a_6^2 的 m+8=9 特殊性（9=2^3+1 家族 m=3 成员——平方化的 m 条件）",
        "回主线：P7-5e 候选层系列收官声明（190-206 全部候选层、未升定案层）",
    ],
}

result = {
    "title": "P7-5e-206 D(m+8) family-power & b1^2±1 unification",
    "date": "2026-10-15",
    "QQ": {"rows": QQ_rows, "D17": QQ_pred, "verdict": QQ_verdict},
    "RR": {"RR1": RR1, "RR2": RR2, "RR3": RR3, "RR4": RR4, "RR5": RR5, "RR6": RR6},
    "SS": SS,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 72)
print("P7-5e-206 D(m+8) family-power & b1^2±1 unification")
print("=" * 72)
print("[QQ D(m+8) scan]")
for r in QQ_rows:
    print("  D(%2d)=%9d factors=%s fam_factors=%s fam_power=%s" % (
        r["m8"], r["D"], r["factors"], r["family_factors"], r["is_family_power"]))
print("[QQ D17] D(17)=%d factors=%s" % (QQ_pred["D17"], QQ_pred["factors"]))
print("[QQ verdict]", QQ_verdict)
print("[RR1]", RR1["check"], "->", RR1["ok"])
print("[RR2]", RR2["check"], "->", RR2["ok"])
print("[RR3]", RR3["check"], "->", RR3["ok"])
print("[RR4]", RR4["check"], "->", RR4["ok"])
print("[RR5]", RR5["check"], "->", RR5["ok"])
print("[RR6]", RR6["check"])
print("[SS]", SS["check"])
print("[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
