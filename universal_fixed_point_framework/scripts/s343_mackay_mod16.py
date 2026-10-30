# -*- coding: utf-8 -*-
"""S343 Mackay 标准序列 mod 16 系统性检验
S342 用 Māyā 给的序列（1,13,55,147,339,561——339 疑为 309 之误）——
标准 Mackay 二十面体壳配位数：shell_k = 10k²+2（k=1,2,...）
累计配位数 S_n = 1 + Σ(10k²+2)——检验 mod 16 是否全 ∈ 奇数框架常数
奇数框架常数 = {1, 3, 5, 7, 11, 13}（单位/活跃/静默/对合/显态/−活跃）
"""
import math

print("=== S343 Mackay 标准序列 mod 16 系统性检验 ===\n")

ODD_FW = {1, 3, 5, 7, 11, 13}
labels = {1: "单位", 3: "活跃", 5: "静默", 7: "对合", 11: "显态", 13: "-活跃(=13)"}

print(f"[1] 标准 Mackay 壳配位数 shell_k = 10k²+2")
shells = [10*k*k + 2 for k in range(1, 13)]
print(f"    shell: {shells}")

print(f"\n[2] 累计配位数 S_n = 1 + Σ shell_k")
cum = []
s = 1
for shell in shells:
    s += shell
    cum.append(s)
print(f"    累计: {cum}")

print(f"\n[3] mod 16 检验")
print(f"    n | S_n   | mod16 | 身份")
all_pass = True
for i, n in enumerate(cum, start=1):
    r = n % 16
    # 负表示（>8 时）
    rn = r if r <= 8 else r - 16
    ok = r in ODD_FW
    if not ok:
        all_pass = False
    lbl = labels.get(r, f"?({rn})")
    mark = "OK" if ok else "MISS"
    print(f"    {i:2} | {n:4} | {r:3} ({rn:>2}) | {lbl:<10} {mark}")

print(f"\n[4] 结论")
print(f"    12 个点全部 ∈ 奇数框架常数 {{1,3,5,7,11,13}}？——{all_pass}")
if all_pass:
    print(f"    ★ 系统性模式：Mackay 累计配位数 mod 16 ≡ 奇数框架常数")
    print(f"      ——12/12 命中——非 5 样本后验（Māyā 序列含 339 疑误——")
    print(f"        标准序列更完整更强）")

print(f"\n[5] 数学规律")
print(f"    shell_k = 10k²+2——Σshell = 10·Σk²+2n——Σk² = n(n+1)(2n+1)/6")
print(f"    S_n = 1 + 10·n(n+1)(2n+1)/6 + 2n")
print(f"    验证 n=6：S_6 = 1+10×91+12 = 923？——{1+10*91+12}≠561——重算")
print(f"    实际 S_6 = 561——公式检查：Σk²(1..6) = {sum(k*k for k in range(1,7))}")
s6 = 1 + 10*sum(k*k for k in range(1,7)) + 2*6
print(f"    1+10×{sum(k*k for k in range(1,7))}+12 = {s6}——不符（561）——")
print(f"    shell_k 非 10k²+2？——实际差分验证")

print(f"\n[6] 差分分析（shell 实际值）")
diff = [cum[0]-1] + [cum[i]-cum[i-1] for i in range(1, len(cum))]
print(f"    shell 实际 = {diff}")
print(f"    与 10k²+2 比较：{shells}")
print(f"    ——shell = 10k²+2 对于 k=1..4 成立（12,42,92,162）——")
print(f"    k=5：实际 {diff[4]} vs 252——不符？——{diff[4]}")

print(f"\n[7] 结论修正")
print(f"    标准 Mackay 壳（10k²+2）：12,42,92,162,252,362...")
print(f"    累计：1,13,55,147,309,561,923,1415,1907,2509...")
print(f"    这些的 mod 16 序列：")
cum2 = []
s = 1
for k in range(1, 13):
    s += 10*k*k + 2
    cum2.append(s)
    r = s % 16
    rn = r if r <= 8 else r-16
    print(f"      S_{k:2} = {s:4}——mod16 = {r:2}（{rn:>2}）——{'OK' if r in ODD_FW else 'MISS'}")
allpass2 = all((x % 16) in ODD_FW for x in cum2)
print(f"    12/12 ∈ 奇数框架常数？——{allpass2}")
