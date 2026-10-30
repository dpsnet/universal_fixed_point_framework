# -*- coding: utf-8 -*-
"""
P7-5e-202 · 窗口平移语义与 F_4 预言判别（201 的检验 FF + GG）
用户推进（2026-10-15）。

检验 FF 设计（周期映射 M(x) = 256x - 255 的窗口语义，k=3 映射）：
FF1. M(a_j) = a_{j+8}（起边界平移 8）
FF2. M(c_j) = c_{j+8}（对合常数平移 8，k -> 256k = k_{j+8}）
FF3. M(b_j) = b_{j+8} - 255 = 静默单元（8·32·(2^{j+2}-1)+1）——终边界位型变换非平移
FF4. M(2^m+1) = 2^{m+8}+1（家族 m -> m+8，188 已知）
FF5. ★ 窗口平移-宽度分离：起边界与对合常数平移（形式保持）、终边界减宽度（位型变换）
FF6. 静默余数守恒：M 保持 8k+1 位型（a_j/c_j 静默保持；b_j 非静默 -> 静默）

检验 GG 设计（F_4 = 65537 窗口外预言）：
GG1. 周期映射 k=4：2^{m+16}+1 = 65536·(2^m+1) - 65535
GG2. 缩放 b_{2^4-2} = b_14 = 2^16 = 65536
GG3. 平移 65535 = F_4 - 2 = 2^16 - 1
GG4. F_4 = a_15（a_j = 2^{j+1}+1，j=15 -> 2^16+1）
GG5. F_4 = 65537 素数（经典 Fermat 素数，m=16 = 2 的幂）
GG6. ★ F_5 = 2^32+1 合数（= 641 × 6700417）——Fermat 素数骨架在 m=16 截止
GG7. 框架外预言：家族素数成员有限（m=1,2,4,8,16），m=32 起合数；2 进组织无限 vs 素数骨架有限
"""
import json

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e202_window_shift_fermat4.json"

# ---------- FF1/FF2/FF3 ----------
def M(x):
    return 256 * x - 255

FF1_rows = []
for j in range(0, 8):
    a_j = 2 ** (j + 1) + 1
    a_j8 = 2 ** (j + 9) + 1
    FF1_rows.append({"j": j, "a_j": a_j, "M(a_j)": M(a_j), "a_{j+8}": a_j8,
                     "ok": M(a_j) == a_j8})

FF2_rows = []
for j in range(1, 7):
    a_j = 2 ** (j + 1) + 1
    b_j = 2 ** (j + 2)
    c_j = a_j + b_j
    k_j = (c_j - 1) // 8
    k_j8 = 256 * k_j
    c_j8 = 8 * k_j8 + 1
    FF2_rows.append({"j": j, "c_j": c_j, "k_j": k_j, "M(c_j)": M(c_j),
                     "c_{j+8}": c_j8, "k_j8": k_j8, "ok": M(c_j) == c_j8})

FF3_rows = []
for j in range(1, 7):
    b_j = 2 ** (j + 2)
    b_j8 = 2 ** (j + 10)
    Mb = M(b_j)
    silent_k = (Mb - 1) // 8
    FF3_rows.append({"j": j, "b_j": b_j, "M(b_j)": Mb,
                     "b_{j+8}": b_j8, "diff_255": b_j8 - Mb == 255,
                     "M_silent": Mb % 8 == 1, "k": silent_k})

FF4 = {
    "check": "M(2^m+1) = 256·(2^m+1) − 255 = 2^{m+8}+1（家族 m → m+8）",
    "ok_m1to5": all(256 * (2 ** m + 1) - 255 == 2 ** (m + 8) + 1 for m in range(1, 6)),
}

# ---------- GG1..GG5 ----------
GG1_rows = []
for m in range(1, 6):
    GG1_rows.append({"m": m, "lhs": 2 ** (m + 16) + 1,
                     "rhs": 65536 * (2 ** m + 1) - 65535,
                     "ok": 2 ** (m + 16) + 1 == 65536 * (2 ** m + 1) - 65535})

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

GG2 = {
    "scale_b14": 2 ** 16,
    "ok": 2 ** 16 == 2 ** (2 ** 4 - 2 + 2),
}
GG3 = {"shift": 2 ** 16 - 1, "F4_minus_2": (2 ** 16 + 1) - 2, "ok": 2 ** 16 - 1 == (2 ** 16 + 1) - 2}
GG4 = {"F4": 2 ** 16 + 1, "a15": 2 ** 16 + 1, "ok": 2 ** 16 + 1 == 2 ** 16 + 1}
GG5 = {"F4_prime": is_prime(2 ** 16 + 1)}
GG6 = {
    "F5": 2 ** 32 + 1,
    "F5_prime": is_prime(2 ** 32 + 1),
    "F5_factor": "641 × 6700417",
    "ok": 2 ** 32 + 1 == 641 * 6700417,
}
GG7 = {
    "check": "Fermat 素数仅 F_0..F_4（m=1,2,4,8,16），F_5=4294967297 合数——家族素数成员有限（m=32 起合数）；2 进组织无限 vs 素数骨架有限（框架外预言）",
}

# ---------- 结论 ----------
conclusion = {
    "verdict": "FF：★ 窗口平移-宽度分离——M(a_j)=a_{j+8}（起边界平移）、M(c_j)=c_{j+8}（对合常数平移，k→256k=k_{j+8}）、M(b_j)=b_{j+8}−255=静默单元（终边界位型变换非平移）；静默余数守恒（M 保持 8k+1 位型）。GG：周期映射 k=4 验证（65536·x−65535）；F_4=65537=a_15 素数（m=16=2 的幂）；★ F_5=4294967297=641×6700417 合数——Fermat 素数骨架在 m=16 截止；2 进组织无限 vs 素数骨架有限（框架外预言）",
    "FF": {
        "FF1": "M(a_j) = a_{j+8}（起边界平移 8，全验证）",
        "FF2": "M(c_j) = c_{j+8}（对合常数平移，k → 256k = k_{j+8}）",
        "FF3": "M(b_j) = b_{j+8} − 255 = 8·32·(2^{j+2}−1)+1（终边界 → 静默单元）",
        "FF5": "窗口平移-宽度分离：起边界/对合常数平移保持形式、终边界减 Fermat 窗口宽度",
        "FF6": "静默余数守恒：a_j/c_j 静默保持、b_j 非静默 → 静默",
    },
    "GG": {
        "GG1": "周期映射 k=4：2^{m+16}+1 = 65536·(2^m+1) − 65535 ✓",
        "GG4": "F_4 = 65537 = a_15",
        "GG5": "F_4 素数（m=16 = 2 的幂）",
        "GG6": "F_5 = 4294967297 合数（641×6700417）——素数骨架 m=16 截止",
        "GG7": "框架外预言：家族素数有限、2 进组织无限",
    },
    "honest_limits": [
        "FF1/FF2 是代数恒等（M 定义直接推出），'平移-宽度分离'为语义指认",
        "GG6 的 F_5 合数是经典数论事实（Euler 1732）",
        "GG7 的'组织无限 vs 骨架有限'为登记级观察",
        "继承 187-201 候选层",
    ],
    "next_candidates": [
        "检验 HH：窗口平移 8 的物理语义——m→m+8 把通道送到下一 Bott 周期（188），与静默余数守恒 1/8 的结合（窗口平移 = Bott 周期步进）",
        "检验 II：M(b_j) 的静默 k = 32(2^{j+2}−1) 序列与窗口常数 k_j = 3·2^{j−2} 的对照（终边界静默化与起边界对合的双族结构）",
        "窗口 2 家族段判据（若框架层扩展）",
    ],
}

result = {
    "title": "P7-5e-202 window-shift semantics & F_4 prediction",
    "date": "2026-10-15",
    "FF1_rows": FF1_rows, "FF2_rows": FF2_rows, "FF3_rows": FF3_rows, "FF4": FF4,
    "GG1_rows": GG1_rows, "GG2": GG2, "GG3": GG3, "GG4": GG4, "GG5": GG5, "GG6": GG6, "GG7": GG7,
    "conclusion": conclusion,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("=" * 72)
print("P7-5e-202 window-shift semantics & F_4 prediction")
print("=" * 72)
print("\n[FF1 M(a_j) = a_{j+8}]")
for r in FF1_rows:
    print(f"  j={r['j']}: a_j={r['a_j']:<5} M={r['M(a_j)']:<6} a_{{j+8}}={r['a_{j+8}']:<6} ok={r['ok']}")
print("\n[FF2 M(c_j) = c_{j+8}]")
for r in FF2_rows:
    print(f"  j={r['j']}: c_j={r['c_j']:<4} k_j={r['k_j']:<3} M={r['M(c_j)']:<5} c_{{j+8}}={r['c_{j+8}']:<6} k_{{j+8}}={r['k_j8']} ok={r['ok']}")
print("\n[FF3 M(b_j)]")
for r in FF3_rows:
    print(f"  j={r['j']}: b_j={r['b_j']:<4} M={r['M(b_j)']:<7} diff_255={r['diff_255']} silent={r['M_silent']} k={r['k']}")
print(f"\n[FF4] {FF4['check']} (ok={FF4['ok_m1to5']})")
print("\n[GG1 period map k=4]")
for r in GG1_rows:
    print(f"  m={r['m']}: 2^(m+16)+1 == 65536·(2^m+1)−65535? {r['ok']}")
print(f"\n[GG4] F_4 = {GG4['F4']} = a_15? {GG4['ok']}")
print(f"[GG5] F_4 prime? {GG5['F4_prime']}")
print(f"[GG6] F_5 = {GG6['F5']} prime? {GG6['F5_prime']}  = {GG6['F5_factor']}? {GG6['ok']}")
print(f"[GG7] {GG7['check']}")
print("\n[Conclusion]", conclusion["verdict"])
print("  next:", conclusion["next_candidates"][0])
