# -*- coding: utf-8 -*-
"""chain_audit_192d_generator_scan_final.py — 104az-193 最终扫描（FW 表补全已登记身份）

FW 表口径（登记中明确身份值，非任意乘法闭包）：
基础：{1,2,3,4,5,7,8,15,16}；组合恒等（104az-192 等）：{6,9,10,11,12,13,14}；
已登记复合量：{20,21,28,29,30,31,32,35,40,42,44,45,46,48,49,56,58,60,61,63,64,65,
              84,98,100,105,125,210,253,320,675,729,1000}
"""
import io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FW = {
    1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 6, 10, 11, 12, 13, 14,
    20, 21, 28, 29, 30, 31, 32, 35, 40, 42, 44, 45, 46, 48, 49,
    56, 58, 60, 61, 63, 64, 65, 84, 98, 100, 105, 125, 210, 253,
    320, 675, 729, 1000,
}
FW_SUM = {v for v in FW if v <= 64} | {105, 125, 210, 253, 320, 675, 729}

def analyze(s):
    ss, pp = [], []
    for r in range(1, len(s) + 1):
        for c in itertools.combinations(s, r):
            ss.append(sum(c))
            pr = 1
            for x in c:
                pr *= x
            pp.append(pr)
    bad_s = sorted({v for v in ss if v not in FW_SUM})
    bad_p = sorted({v for v in pp if v not in FW})
    return bad_s, bad_p, sorted(set(ss)), sorted(set(pp))

print(f"FW 表 = {len(FW)} 个：{sorted(FW)}")
print(f"FW_SUM = {len(FW_SUM)} 个")

for size, rng in [(3, range(1, 17)), (4, range(1, 17)), (5, range(1, 17)), (4, range(1, 25))]:
    closed = []
    n = 0
    for s in itertools.combinations(rng, size):
        n += 1
        bad_s, bad_p, _, _ = analyze(s)
        if not bad_s and not bad_p:
            closed.append(s)
    print(f"\n[{size}-元 × {list(rng)[0]}..{list(rng)[-1]}] 候选 {n} → 闭包 {len(closed)} 个")
    for s in closed:
        _, _, ss, pp = analyze(s)
        pr = 1
        for x in s:
            pr *= x
        print(f"    {s}  全积={pr}  和谱={ss}  积谱={pp}")

# 不含 1 的 4 元闭包
print("\n=== 不含 1 的 4 元闭包 [1,16] ===")
for s in itertools.combinations(range(2, 17), 4):
    bad_s, bad_p, _, _ = analyze(s)
    if not bad_s and not bad_p:
        print(f"    {s}")
