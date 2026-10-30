# -*- coding: utf-8 -*-
"""
P7-5e-205 Mersenne role in D(m) & 63/65 identity (NN + OO)
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e205_mersenne_dm_identity.json"

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

# ---------- NN ----------
def is_nontrivial_mersenne_prime(n):
    # Mersenne prime 2^k - 1 with k >= 3 (exclude trivial M_2 = 3)
    if not is_prime(n):
        return False
    return n + 1 in [2 ** k for k in range(3, 10)]

NN1_rows = []
for m in range(1, 17):
    d = Dm(m)
    fs = factors(d)
    non_triv = [f for f in fs if is_nontrivial_mersenne_prime(f)]
    NN1_rows.append({"m": m, "D": d, "factors": fs,
                     "nontrivial_mersenne_factors": non_triv})

NN2 = {"D9": Dm(9), "a6": 2 ** 7 + 1, "D9_is_a6_square": Dm(9) == (2 ** 7 + 1) ** 2,
       "check": "★ D(9) = 16641 = 129^2 = a_6^2（窗口 6 起边界 = 家族 m=7 成员的平方）"}
NN3 = {"check": "D(m+8) 序列因子结构：D(9)=129^2（家族平方）、D(10)=5*73*101、D(11)=80897 素数——平方化仅 m=9"}
NN4 = {"check": "★ 非平凡 Mersenne 素数因子唯一出现在 m=3：D(3)=93=3·31=3·M_5（M_2=3 平凡，出现在 m=2,3,8,9,14,15）——与 D(3)≡5 mod 8 例外（196 U2）同位",
       "nontrivial_count": sum(1 for r in NN1_rows if r["nontrivial_mersenne_factors"])}

# ---------- OO ----------
OO1 = {"prod": 65 * 63, "M12": 2 ** 12 - 1, "ok": 65 * 63 == 2 ** 12 - 1,
       "check": "65*63 = 4095 = M_12（±1 对积 = Mersenne 平方差，LL3 特例 n=6）"}
OO2 = {"w5": 63, "w5_decomp": "7*9 = 域宽 7 × 静默单元 9（家族 m=3 / 根对合常数 c_1 / 静默 k=1）",
       "dinf_denom": 56, "dinf_decomp": "7*8 = 域宽 7 × 满格 8",
       "ok": 63 == 7 * 9 and 56 == 7 * 8,
       "check": "★ 63 = 7*9（域宽×静默单元 9）vs 56 = 7*8（域宽×满格）——δ∞=1/56 与窗口宽度 63 构成 7*(8±1) 对偶"}
OO3 = {"diff": "1/65 - 1/63 = -2/4095 = -2/M_12",
       "check": "修正锚点 1/65 与 Mersenne 侧 1/63 之差落在 M_12"}
OO4 = {"check": "63 的框架分解 = 域宽 × 根对合常数（9 = 2^3+1 = 家族 m=3、c_1、静默 k=1 三重身份）",
       "ok": 9 == 2 ** 3 + 1 and (9 - 1) % 8 == 0 and 9 == 8 * 1 + 1}
OO5 = {"verdict": "★ 65 的 Mersenne 侧新身份：65 = 2^6+1 的 −1 对 63 = 7·9（域宽×静默单元）落在 δ∞ 分母结构（1/56 = 1/(7·8)）——修正锚点与 δ∞ 通过 7×(8±1) 对偶互锁：1/65（加 1 侧，m=6 家族/窗口 5 起边界/修正）↔ 1/63（减 1 侧，域宽×静默单元）↔ 1/56（静默分母，域宽×满格）",
       "check": "65 的 ±1 对偶两侧：+1 侧 65=2^6+1（家族/修正锚点）、−1 侧 63=7·9（域宽×静默单元）——δ∞ 分母 56=7·8 是 +1/−1 之间的静默基准"}

OO6 = {"check": "★ 核心常数连续窗口 [56,63,64,65]：56=7·8（δ∞ 分母）、63=7·9（窗口 5 宽度 M_6）、64=8²（满格平方 b_1²）、65=8²+1（修正锚点 b_1²+1）——十个数窗口内集中 δ∞/宽度/满格平方/修正锚点四常数",
       "ok": 56 == 7 * 8 and 63 == 7 * 9 and 64 == 8 ** 2 and 65 == 8 ** 2 + 1}

conclusion = {
    "verdict": "NN：★ D(9) = 16641 = 129^2 = a_6^2（家族 m=7 成员平方——D(m+8) 序列的家族平方化）；D(3) = 93 = 3·31 = 3·M_5（唯一 Mersenne 素数因子——窗口宽度 Mersenne 不延伸到 D(m) 主体）。OO：★ 63 给 1/65 提供 Mersenne 侧身份——65·63 = 4095 = M_12；63 = 7·9（域宽 × 静默单元 9）vs 56 = 7·8（域宽 × 满格）——δ∞ = 1/56 与窗口宽度 63 构成 7×(8±1) 对偶；1/65 的 ±1 对两侧落在家族侧（65=2^6+1）与域宽侧（63=7·9）。",
    "NN": {
        "NN1": "D(m) 因子扫描 m=1..16",
        "NN2": "★ D(9) = a_6^2 = 129^2",
        "NN3": "D(m+8) 因子结构：平方化仅 m=9",
        "NN4": "Mersenne 素数因子仅 D(3)=3·M_5（稀疏）",
    },
    "OO": {
        "OO1": "65·63 = M_12",
        "OO2": "★ 63 = 7·9 vs 56 = 7·8（7×(8±1) 对偶）",
        "OO3": "1/65 − 1/63 = −2/M_12",
        "OO4": "63 = 域宽 × 根对合常数 9（三重身份）",
        "OO5": "★ 65 的 ±1 对偶两侧互锁 δ∞",
    },
    "honest_limits": [
        "NN2 的 D(9)=129^2 是代数恒等（直接验证）；'家族平方化'为描述性观察（仅 m=9 单例）",
        "NN4 Mersenne 因子稀疏是枚举事实（m=1..16 仅 1 例）",
        "OO1/OO3 是代数恒等；OO2 的 7×(8±1) 对偶为语义指认",
        "OO5 '互锁'为候选主张（65 与 1/56 的 ±1 联系是描述性）",
        "继承 187-204 候选层",
    ],
    "next_candidates": [
        "检验 PP：P7-5e 候选层汇总 + 论文 §7.5 第 11 项整合终稿（本轮③）",
        "检验 QQ：D(9)=a_6^2 是否预示 D(m+8) 序列的一般结构（家族成员幂）——D(17)=? 检查 a_8^2 型",
        "检查 7×(8±1) 对偶在框架常数层的延伸（56=δ∞ 分母、63=宽度、64=满格、65=修正锚点——[56,64,65] 连续窗口）",
    ],
}

result = {
    "title": "P7-5e-205 Mersenne role in D(m) & 63/65 identity",
    "date": "2026-10-15",
    "NN": {"NN1_rows": NN1_rows, "NN2": NN2, "NN3": NN3, "NN4": NN4},
    "OO": {"OO1": OO1, "OO2": OO2, "OO3": OO3, "OO4": OO4, "OO5": OO5, "OO6": OO6},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 72)
print("P7-5e-205 Mersenne role in D(m) & 63/65 identity")
print("=" * 72)
print("[NN D(m) factor scan]")
for r in NN1_rows:
    print("  m=%2d: D=%7d factors=%s nontrivial_mersenne=%s" % (
        r["m"], r["D"], r["factors"], r["nontrivial_mersenne_factors"]))
print("[NN2] D(9)=%d  a_6=129  D9==129^2? %s" % (NN2["D9"], NN2["D9_is_a6_square"]))
print("[NN4] nontrivial Mersenne prime factor count (m=1..16): %d" % NN4["nontrivial_count"])
print("[OO1] 65*63=%d == M_12=%d? %s" % (OO1["prod"], OO1["M12"], OO1["ok"]))
print("[OO2] %s" % OO2["check"])
print("[OO4] 9 triple identity (family m=3 / c_1 / silent k=1): %s" % OO4["ok"])
print("[OO6] core-constant window [56,63,64,65]: %s" % OO6["ok"])
print("[OO5] %s" % OO5["verdict"])
print("[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
