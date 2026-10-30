# -*- coding: utf-8 -*-
"""
P7-5e-210 D(n) silent-class membership & 2-power-set organization (P7-5e-186) connection
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e210_dn_silent_class_binary.json"

def Dn(n):
    return n * 7 * 2 ** (n - 1) + 2 ** n + 1

def silent_family_members():
    return {2 ** m + 1: m for m in range(3, 12)}  # 9,17,33,65,129,257,513,1025,2049

SILENT = silent_family_members()

# ---------- ZZ1: D(n) mod 8 ----------
ZZ1_rows = []
for n in range(2, 17):
    d = Dn(n)
    ZZ1_rows.append({"n": n, "D(n)": d, "mod8": d % 8,
                     "silent_class": (d % 8) == 1,
                     "exception": n == 3 and (d % 8) == 5})
ZZ1 = {"check": "D(n) ≡ 1 mod 8（静默单元类 8k+1，n≥2, n≠3）；D(3)=93≡5 例外（8k+5）——196 U2 复验 + 归因：n≥4 时 2^{n−1} 含 2³ 因子 ⇒ 2^{n−1}(7n+2)≡0 mod 8",
       "all_silent_except3": all(r["silent_class"] or r["exception"] for r in ZZ1_rows)}

# ---------- ZZ2: D(n) = 8*2^{n-4}(7n+2)+1 ----------
ZZ2_rows = []
for n in range(4, 17):
    d = Dn(n)
    kn = 2 ** (n - 4) * (7 * n + 2)
    ZZ2_rows.append({"n": n, "D(n)": d, "k_n": kn,
                     "ok": d == 8 * kn + 1})
ZZ2 = {"check": "★ D(n) = 8·2^{n−4}(7n+2) + 1（n≥4）——k_n = 2^{n−4}(7n+2) 显式（静默单元类 k 参数）",
       "rows": ZZ2_rows}

# ---------- ZZ3: D(2)=33 silent family member; D(9)=129^2 ----------
ZZ3 = {
    "check": "★ D(2) = 33 = 2^5+1 是静默单元家族成员（m=5）；D(9) = 16641 = 129² = (2^7+1)² 家族平方（207 UU 再现）",
    "D2": Dn(2), "in_family": Dn(2) in SILENT, "family_m": SILENT.get(Dn(2)),
    "D9_square": Dn(9) == 129 ** 2, "D9_family_base": 129 == 2 ** 7 + 1,
}

# ---------- ZZ4: k_n 2-adic organization ----------
ZZ4_rows = []
for n in range(4, 17):
    kn = 2 ** (n - 4) * (7 * n + 2)
    # largest 2-power factor
    v2 = 0
    kk = kn
    while kk % 2 == 0:
        kk //= 2
        v2 += 1
    ZZ4_rows.append({"n": n, "k_n": kn, "2^v2": 2 ** v2, "odd_part": kk,
                     "note": "2^{n-4}·(7n+2)" if v2 == n - 4 else "extra 2 from 7n+2"})
ZZ4 = {"check": "k_n 的 2 进组织：k_n = 2^{n−4}(7n+2)——2 进幂 × 线性因子；k_4=30=2·15、k_9=2080=2^5·65（65 修正锚点出现于 k_9）；n=2,4,5,9 时 7n+2 偶 ⇒ k_n 含额外 2 因子",
       "rows": ZZ4_rows}

# ---------- Connection to P7-5e-186 ----------
CONN = {
    "check": "★ 连接 186 '2 进幂集组织'：1/B*(n) = D(n)/(7·2^n) = (8k_n+1)/(7·2^n)——分子落静默单元类（8k+1）、分母 = 7×2^n（Mersenne_3 × 2 进幂）——临界场强分母的类归属由静默类组织，是 186 在 B*(n) 分母层面的投影；但 k_n=2^{n−4}(7n+2) 仅少数为纯 2 进子集成员（D(2)=33 纯家族、D(9)=129² 家族平方），其余为 2 进幂×线性——类归属连接成立、成员级连接受限",
    "molecule_class": "8k+1 静默类（n≠3），n=3 例外 8k+5",
    "denominator": "7·2^n = M_3 × 2^n",
    "pure_members": {"D(2)": "33 = 2^5+1", "D(9)": "129² = (2^7+1)²"},
}

conclusion = {
    "verdict": "ZZ（★ 静默类归属闭合 + 186 连接）：D(n) ≡ 1 mod 8（n≥2, n≠3，静默单元类 8k+1）、D(3)=93≡5 例外（196 U2 复验成立，归因 n≥4 含 2³ 因子）；★ D(n) = 8·2^{n−4}(7n+2)+1（n≥4 全 True）——k_n=2^{n−4}(7n+2) 显式；★ D(2)=33=2^5+1 是静默单元家族成员（m=5）、D(9)=129²=(2^7+1)² 家族平方（207 UU 再现）；k_n 2 进组织 = 2 进幂 × (7n+2) 线性因子（k_9=2^5·65 出现修正锚点）。连接 186：1/B*(n)=(8k_n+1)/(7·2^n)——分子落静默类、分母=M_3×2^n，临界场强分母的类归属由静默类组织（186 在 B*(n) 分母层面的投影）；成员级连接受限（仅 D(2)/D(9) 纯家族）。",
    "ZZ1": ZZ1,
    "ZZ2": ZZ2,
    "ZZ3": ZZ3,
    "ZZ4": ZZ4,
    "connection": CONN,
    "honest_limits": [
        "ZZ1 是 196 U2 复验（n≥4 归因是 2 进平凡论证）",
        "ZZ2 是代数恒等（D(n) 定义展开）",
        "ZZ3 是 D(2)/D(9) 家族成员核对（已知：207 UU）",
        "ZZ4 是枚举 + 2 进分解",
        "CONN 为语义连接（候选层→定案层桥）：'类归属'层面成立，'成员级'受限",
        "继承 187-209 候选层",
    ],
    "next_candidates": [
        "检验 YY（补完 208 遗留）：k_{2j+3}=6·4^j 与窗口常数组 k_j=3·2^{j−2} 的并集",
        "检验 AA：D(n) 的 k_n 序列 2^{n−4}(7n+2) 与种子代数 {2,3,5,8} 的交集核对（n=9: 2^5·65=2^5·(8²+1)）",
        "回主线：P7-5e 候选层系列暂止或转 P7-5e-211",
    ],
}

result = {
    "title": "P7-5e-210 D(n) silent-class membership & 2-power-set connection",
    "date": "2026-10-16",
    "ZZ1": ZZ1,
    "ZZ2": {"rows": ZZ2_rows},
    "ZZ3": ZZ3,
    "ZZ4": {"rows": ZZ4_rows},
    "connection": CONN,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 76)
print("P7-5e-210 D(n) silent-class membership & 2-power-set connection")
print("=" * 76)
print("[ZZ1 D(n) mod 8]")
for r in ZZ1_rows:
    print("  n=%2d D=%9d mod8=%d silent=%s exception=%s" % (
        r["n"], r["D(n)"], r["mod8"], r["silent_class"], r["exception"]))
print("[ZZ2 D(n) = 8*2^{n-4}(7n+2)+1]")
for r in ZZ2["rows"]:
    print("  n=%2d D=%9d k_n=%8d ok=%s" % (r["n"], r["D(n)"], r["k_n"], r["ok"]))
print("[ZZ3]", ZZ3["check"], "-> in_family=%s m=%s square=%s base=%s" % (
    ZZ3["in_family"], ZZ3["family_m"], ZZ3["D9_square"], ZZ3["D9_family_base"]))
print("[ZZ4 k_n 2-adic]")
for r in ZZ4["rows"]:
    print("  n=%2d k=%8d = 2^%d × %s" % (r["n"], r["k_n"], r["2^v2"].bit_length() - 1, r["odd_part"]))
print("[Connection]", CONN["check"])
print("[Conclusion]", conclusion["verdict"])
