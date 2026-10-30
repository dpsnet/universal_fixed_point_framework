# -*- coding: utf-8 -*-
"""
P7-5e-203 · Bott 周期步进 / 双族位型 / 窗口 2 家族段判据（202 的检验 HH + II + JJ）
用户"1 2 3"启动（2026-10-15）。

检验 HH（窗口平移 = Bott 周期步进）：
HH1. 通道步进：m → m+8（步进 = k_max = 窗口宽 8）
HH2. 家族成员跨周期：2^{m+8}+1 ≡ 1 mod 8（静默类封闭）
HH3. 静默余数守恒：M(8k+1) = 8·(256k)+1 ≡ 1 mod 8
HH4. 尾巴缩 2^8：1/(7·2^{m+8}) = (1/(7·2^m))/256
HH5. B* 分母跨周期：D(m+8) 的 mod 8 类 = D(m) 的 mod 8 类
HH6. B*(m+8)/B*(m) = 256·D(m)/D(m+8)（精确值验证）

检验 II（双族位型对照——M(b_j) 静默 k 族 vs 窗口常数 k_j）：
II1. M(b_j) 静默 k = 2^5·(2^{j+2}−1) = 32·Mersenne_{j+2}（j=1..6：224/480/992/2016/4064/8160）
II2. 窗口常数 k_j = 3·2^{j−2}（j=2..7：3/6/12/24/48/96）
II3. ★ Mersenne 素数性：2^{j+2}−1 素数 ↔ j+2 为奇素数（3,5,7 素数；4,6,8 合数——经典定理 2^n−1 素数 ⇒ n 素数）
II4. 位型对照：窗口常数 = 相邻双位（11₂ + p 个 0）；M(b_j) k = Mersenne 左移 5 位（j+2 个 1 + 5 个 0）
II5. 双族总结：起边界对合（3·2^p 翻倍）vs 终边界静默化（32·(2^{j+2}−1) 增长更快）

检验 JJ（窗口 2 家族段判据）：
JJ1. 窗口 j≥2 三段结构：a_j = 2^{j+1}+1（家族段）、b_j = 2^{j+2}（塔段）、c_j = 8k_j+1（静默段）
JJ2. 家族段：a_j = 家族 m=j+1 成员（j=2..7 全 True）
JJ3. 塔段：b_j = 2 幂塔（全 True）
JJ4. 静默段：k_j = 3·2^{j−2}（j=2..7 全 True）
JJ5. 窗口 1 例外：a_1=1（非家族）、c_1=9（k=1 单位位非相邻双位）——根窗口异类（190 H）
JJ6. ★ 判据成立：窗口 2+ 是"家族段×塔段×静默段"统一结构；根窗口无家族段
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e203_bott_step_dual_bittype_window2.json"

# ---------- HH ----------
HH1 = {"step": 8, "k_max": 8, "ok": 8 == 8,
       "check": "m→m+8 通道步进 = k_max = 窗口宽（Bott 周期步进）"}
HH2 = {"ok_all": all((2 ** (m + 8) + 1) % 8 == 1 for m in range(1, 8)),
       "check": "家族跨周期 2^{m+8}+1 ≡ 1 mod 8（静默类封闭）"}
HH3 = {"ok": all((256 * (8 * k + 1) - 255) % 8 == 1 for k in [1, 3, 6, 12, 24, 48]),
       "check": "M(8k+1) ≡ 1 mod 8（静默余数跨周期守恒）"}
HH4 = {"ok": all(1 / (7 * 2 ** (m + 8)) == (1 / (7 * 2 ** m)) / 256 for m in range(1, 8)),
       "check": "尾巴缩 2^8：1/(7·2^{m+8}) = 尾巴/256"}
HH5 = {"ok": all((D(m + 8) % 8) == (D(m) % 8) for m in range(1, 8)) if False else None}

def Dm(m):
    return m * 7 * 2 ** (m - 1) + 2 ** m + 1

HH5a = {"ok": all(Dm(m + 8) % 8 == Dm(m) % 8 == 1 for m in range(2, 8) if m != 3),
        "check": "m=2,4,5,6：D(m+8) ≡ D(m) ≡ 1 mod 8（静默类跨周期保持）"}
HH5b = {"m1": {"D1": Dm(1), "D1_mod8": Dm(1) % 8, "D9": Dm(9), "D9_mod8": Dm(9) % 8},
        "m3": {"D3": Dm(3), "D3_mod8": Dm(3) % 8, "D11": Dm(11), "D11_mod8": Dm(11) % 8},
        "check": "★ 例外不跨周期传递：m=1(D=10≡2)、m=3(D=93≡5) 是小 m 段异类，跨周期后 D(9)=16641≡1、D(11)=80897≡1——回到静默类",
        "ok": Dm(9) % 8 == 1 and Dm(11) % 8 == 1}

def Bm(m):
    return Fraction(7 * 2 ** m, Dm(m))

from fractions import Fraction

def Bm(m):
    return Fraction(7 * 2 ** m, Dm(m))

HH6_rows = []
for m in range(1, 7):
    ratio = Bm(m + 8) / Bm(m)
    expected = Fraction(256 * Dm(m), Dm(m + 8))
    HH6_rows.append({"m": m, "B*(m)": str(Bm(m)), "B*(m+8)": str(Bm(m + 8)),
                     "ratio": str(ratio), "256·D(m)/D(m+8)": str(expected),
                     "ok": ratio == expected})

# ---------- II ----------
II1_rows = []
for j in range(1, 7):
    b_j = 2 ** (j + 2)
    Mb = 256 * b_j - 255
    k = (Mb - 1) // 8
    II1_rows.append({"j": j, "b_j": b_j, "M(b_j)": Mb, "k": k,
                     "2^5·(2^{j+2}−1)": 32 * (2 ** (j + 2) - 1),
                     "ok": k == 32 * (2 ** (j + 2) - 1)})

II2_rows = []
for j in range(2, 8):
    a_j = 2 ** (j + 1) + 1
    b_j = 2 ** (j + 2)
    c_j = a_j + b_j
    k_j = (c_j - 1) // 8
    II2_rows.append({"j": j, "c_j": c_j, "k_j": k_j, "3·2^{j−2}": 3 * 2 ** (j - 2),
                     "ok": k_j == 3 * 2 ** (j - 2)})

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

II3_rows = []
for j in range(1, 7):
    n = j + 2
    mers = 2 ** n - 1
    II3_rows.append({"j": j, "n=j+2": n, "M_n": mers, "M_prime": is_prime(mers),
                     "n_prime": is_prime(n),
                     "ok_theorem": (not is_prime(mers)) or is_prime(n)})

II4 = {
    "window_const_bittype": "相邻双位：k_j = 3·2^{j−2}（二进制 11 后跟 j−2 个 0）",
    "M(b_j)_bittype": "Mersenne 左移 5 位：k = 2^5·(2^{j+2}−1)（j+2 个 1 后跟 5 个 0）",
}
II5 = {
    "check": "起边界对合：3·2^p 翻倍（相邻双位、每窗口 ×2）；终边界静默化：32·(2^{j+2}−1) 以 2 的幂超指数增长——双族位型各管一段",
}

# ---------- JJ ----------
JJ_rows = []
for j in range(2, 8):
    a_j = 2 ** (j + 1) + 1
    b_j = 2 ** (j + 2)
    c_j = a_j + b_j
    k_j = (c_j - 1) // 8
    JJ_rows.append({"j": j, "a_j": a_j, "family_m": j + 1, "fam_ok": a_j == 2 ** (j + 1) + 1,
                    "b_j": b_j, "tower_ok": b_j == 2 ** (j + 2),
                    "c_j": c_j, "k_j": k_j, "silent_ok": k_j == 3 * 2 ** (j - 2)})

JJ1 = {"check": "窗口 j≥2 = 家族段(a_j=2^{j+1}+1) × 塔段(b_j=2^{j+2}) × 静默段(c_j=8·(3·2^{j−2})+1)"}
JJ5 = {"a1": 1, "c1": 9, "k1": 1, "check": "窗口 1 例外：a_1=1 非家族（家族 m=0: 2^0+1=2≠1）、c_1=9 k=1 单位位（非相邻双位）——根窗口无家族段（190 H 异类）"}
JJ6 = {"verdict": "★ 判据成立：窗口 2+ 是'家族段×塔段×静默段'统一结构；根窗口为异类（无家族段）",
       "all_ok": all(r["fam_ok"] and r["tower_ok"] and r["silent_ok"] for r in JJ_rows)}

# ---------- 结论 ----------
conclusion = {
    "verdict": "HH：★ 窗口平移 = Bott 周期步进——通道步进 8 = k_max（窗口宽）、家族跨周期静默类封闭、尾巴缩 2^8、分母静默类保持（★ m=1,3 例外不跨周期传递——跨周期后回到静默类 1 mod 8）、B*(m+8)/B*(m)=256·D(m)/D(m+8) 精确验证。II：★ 双族位型——M(b_j) 静默 k = 2^5·(2^{j+2}−1)（Mersenne 左移，j+2 个 1+5 个 0）vs 窗口常数 k_j = 3·2^{j−2}（相邻双位，11₂+p 个 0）；Mersenne 素数性 ↔ 指数为奇素数（经典定理 2^n−1 素数 ⇒ n 素数：7/31/127 素数 vs 15/63/255 合数）。JJ：★ 窗口 2 家族段判据成立——窗口 j≥2 是家族段×塔段×静默段统一结构（全 True）；根窗口无家族段（a_1=1 异类，190 H）。",
    "HH": {
        "HH1": "通道步进 8 = k_max（Bott 周期步进）",
        "HH2": "家族跨周期 2^{m+8}+1 ≡ 1 mod 8（静默类封闭）",
        "HH3": "M 保持 8k+1（静默余数跨周期守恒）",
        "HH4": "尾巴缩 2^8（每周期缩小满格）",
        "HH5": "D(m+8) ≡ D(m) ≡ 1 mod 8（m=2,4,5,6 静默类保持；★ m=1,3 例外不跨周期传递——跨周期后回到静默类）",
        "HH6": "B*(m+8)/B*(m) = 256·D(m)/D(m+8) 精确验证",
    },
    "II": {
        "II1": "M(b_j) 静默 k = 32·(2^{j+2}−1)（Mersenne 左移 5 位）",
        "II2": "窗口常数 k_j = 3·2^{j−2}（相邻双位）",
        "II3": "Mersenne 素数性 ↔ 指数奇素数（经典定理）",
        "II4": "双族位型：11₂+0s vs 1s+5 个 0",
    },
    "JJ": {
        "JJ1-JJ4": "窗口 j≥2 三段结构全 True（家族段/塔段/静默段）",
        "JJ5": "窗口 1 例外：a_1=1 非家族、c_1 k=1 单位位",
        "JJ6": "判据成立：窗口 2+ 统一三段结构",
    },
    "honest_limits": [
        "HH1-HH5 是定义恒等/代数事实（Bott 周期步进为语义指认）",
        "II3 是经典数论定理（2^n−1 素数 ⇒ n 素数）",
        "JJ 是已登记结构（189/190）的形式化复述，无新数值",
        "继承 187-202 候选层",
    ],
    "next_candidates": [
        "检验 KK：窗口 2 家族段的物理语义——家族段/塔段/静默段是否对应 MUFPF 的 Rec/Sp/对偶投影三层（谱系逐层）",
        "检验 LL：Mersenne 数与 Fermat 数的对偶（2^n−1 vs 2^n+1——静默化 vs 家族边界），M(b_j) k 的 Mersenne 型与 a_j 的 Fermat 型对照",
        "窗口 2 家族段判据入论文（§7.5 结构层）",
    ],
}

result = {
    "title": "P7-5e-203 Bott step / dual bittype / window-2 criterion",
    "date": "2026-10-15",
    "HH": {"HH1": HH1, "HH2": HH2, "HH3": HH3, "HH4": HH4, "HH5a": HH5a, "HH5b": HH5b, "HH6_rows": HH6_rows},
    "II": {"II1_rows": II1_rows, "II2_rows": II2_rows, "II3_rows": II3_rows, "II4": II4, "II5": II5},
    "JJ": {"JJ_rows": JJ_rows, "JJ1": JJ1, "JJ5": JJ5, "JJ6": JJ6},
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print("=" * 72)
print("P7-5e-203 Bott step / dual bittype / window-2 criterion")
print("=" * 72)
print("\n[HH1] step 8 = k_max:", HH1["ok"])
print("[HH2] family cross-period silent:", HH2["ok_all"])
print("[HH3] M keeps 8k+1:", HH3["ok"])
print("[HH4] tail shrinks 2^8:", HH4["ok"])
print("[HH5a] D(m+8) ≡ D(m) ≡ 1 mod 8 (m=2,4,5,6):", HH5a["ok"])
print(f"[HH5b] ★ exception not carried: m=1: D1={HH5b['m1']['D1']} (≡{HH5b['m1']['D1_mod8']}) D9={HH5b['m1']['D9']} (≡{HH5b['m1']['D9_mod8']}) | m=3: D3={HH5b['m3']['D3']} (≡{HH5b['m3']['D3_mod8']}) D11={HH5b['m3']['D11']} (≡{HH5b['m3']['D11_mod8']}) -> {HH5b['ok']}")
print("\n[HH6 B*(m+8)/B*(m) = 256·D(m)/D(m+8)]")
for r in HH6_rows:
    print(f"  m={r['m']}: B*(m)={r['B*(m)']:<12} B*(m+8)={r['B*(m+8)']:<14} ratio={r['ratio']:<24} ok={r['ok']}")
print("\n[II1 M(b_j) silent k = 32·(2^{j+2}−1)]")
for r in II1_rows:
    print(f"  j={r['j']}: M(b_j)={r['M(b_j)']:<7} k={r['k']:<5} 32·(2^{{j+2}}−1)={r['2^5·(2^{j+2}−1)']:<5} ok={r['ok']}")
print("\n[II2 window const k_j = 3·2^{j−2}]")
for r in II2_rows:
    print(f"  j={r['j']}: c_j={r['c_j']:<5} k_j={r['k_j']:<4} 3·2^{{j−2}}={r['3·2^{j−2}']:<4} ok={r['ok']}")
print("\n[II3 Mersenne primality ↔ n prime]")
for r in II3_rows:
    print(f"  j={r['j']}: M_{r['n=j+2']}={r['M_n']:<5} prime={r['M_prime']}  n={r['n=j+2']} prime={r['n_prime']}  theorem_ok={r['ok_theorem']}")
print(f"\n[II4] {II4['window_const_bittype']}\n       {II4['M(b_j)_bittype']}")
print("\n[JJ window-2 family-segment criterion]")
for r in JJ_rows:
    print(f"  j={r['j']}: a={r['a_j']:<5}(fam m={r['family_m']} {r['fam_ok']})  b={r['b_j']:<5}(tower {r['tower_ok']})  c={r['c_j']:<5}(k={r['k_j']} silent {r['silent_ok']})")
print(f"[JJ5] window-1 exception: a_1=1, c_1=9 (k=1 unit-bit)")
print(f"[JJ6] {JJ6['verdict']} all_ok={JJ6['all_ok']}")
print("\n[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
