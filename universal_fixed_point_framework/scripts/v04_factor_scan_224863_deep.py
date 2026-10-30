# -*- coding: utf-8 -*-
"""104az-210 扩展扫描：224863 的深层框架量组合（三因子乘 ± 修正、A²×B±C、A^k±B）
值域覆盖：A×B×C±D 最大 105³+105 ≈ 1.16e6 > 224863 ✓
输出以观察级登记，不升格（v0.4 判据）。
"""
F = sorted(set([2, 3, 4, 5, 7, 8, 11, 13, 15, 16, 21, 29, 42, 49, 105]))
F_NAME = {2:"幂基−N_gen", 3:"N_gen", 4:"不动点", 5:"幂基/静默(5)", 7:"对合域/静默(7)",
          8:"k_max", 11:"素域", 13:"素域", 15:"N_gen×幂基", 16:"不动点²", 21:"N_gen×对合域",
          29:"素域", 42:"禁闭域", 49:"对合域²", 105:"N_gen×幂基×对合域"}
T = 224863

def show(kind, A, B, C, s, D=None):
    if D is None:
        print("  224863 = %s：%s^%d %s %d（%s %s %s）" % (
            kind, A, B, s, C, F_NAME.get(A, str(A)), s, F_NAME.get(C, str(C))), flush=True)
    else:
        print("  224863 = %s：%d×%d×%d %s %d（%s×%s×%s %s %s）" % (
            kind, A, B, C, s, D, F_NAME.get(A, str(A)), F_NAME.get(B, str(B)),
            F_NAME.get(C, str(C)), s, F_NAME.get(D, str(D))), flush=True)

print("===== ① A×B×C ± D（15⁴=50625 组合）=====", flush=True)
n1 = 0
for A in F:
    for B in F:
        for C in F:
            abc = A * B * C
            if abc < T - 110 or abc > T + 110:
                continue
            for D in F:
                if abc - D == T:
                    show("ABC±D", A, B, C, "-", D); n1 += 1
                if abc + D == T:
                    show("ABC±D", A, B, C, "+", D); n1 += 1
print("A×B×C±D 精确命中：%d" % n1, flush=True)

print("\n===== ② A²×B ± C（15³=3375 组合）=====", flush=True)
n2 = 0
for A in F:
    a2 = A * A
    for B in F:
        ab = a2 * B
        if ab < T - 110 or ab > T + 110:
            continue
        for C in F:
            if ab - C == T:
                show("A²×B±C", A, B, "-", C); n2 += 1
            if ab + C == T:
                show("A²×B±C", A, B, "+", C); n2 += 1
print("A²×B±C 精确命中：%d" % n2, flush=True)

print("\n===== ③ A^k ± B（k=2..6，15²=225 组合）=====", flush=True)
n3 = 0
for A in F:
    for k in range(2, 7):
        ak = A ** k
        if ak < T - 110 or ak > T + 110:
            continue
        for B in F:
            if ak - B == T:
                show("A^k±B", A, k, "-", B); n3 += 1
            if ak + B == T:
                show("A^k±B", A, k, "+", B); n3 += 1
print("A^k±B 精确命中：%d" % n3, flush=True)

print("\n===== ④ 224861/224903 邻域差框架量核验 =====", flush=True)
# 224863 = 7²×13×353 + 2（用户分解2 邻域）；224903 = 7²×13×353 + 42（禁闭域）
print("224863 − 7²×13×353 = %d（= 幂基−N_gen = 5−3）" % (T - 49*13*353), flush=True)
print("224903 − 7²×13×353 = %d（= 禁闭域 42 = (幂基−N_gen)+(幂基×k_max)）" % (224903 - 49*13*353), flush=True)
print("7²×13×353 + 42 = %d = 7×19²×89（用户分解1 目标）✓" % (49*13*353 + 42), flush=True)
print("42 = 2+40 = (5−3)+(5×8) = 幂基−N_gen + 幂基×k_max ✓", flush=True)

print("\n===== ⑤ 89 的框架量组合（新标注核验）=====", flush=True)
for expr, name in [
    (5*16+9, "幂基×不动点²+N_gen²"),
    (7*7+5*8, "对合域²+幂基×k_max"),
    (8*11+1, "k_max×素域11+单位元"),
    (2*42+5, "幂基−N_gen×禁闭域+幂基"),
    (15*6-1, "N_gen×幂基×(幂基+1)−1"),
]:
    print("  89 = %d（%s）%s" % (expr, name, "✓" if expr == 89 else "✗"), flush=True)
