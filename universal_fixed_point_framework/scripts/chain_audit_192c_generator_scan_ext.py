# -*- coding: utf-8 -*-
"""chain_audit_192c_generator_scan_ext.py — 104az-193 扩展扫描：3/4/5 元 × [1,16] + 4 元 × [1,24]

口径：与 chain_audit_192b_generator_scan.py 相同（保守 FW 表，不扩张乘法闭包）。
目标：确认闭包生成集家族结构（(1,2,3,7)/(1,3,5,7) 是否家族完备、是否有更大成员）。
"""
import io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FW = {
    1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 21, 31, 35, 42,
    56, 60, 61, 63, 64, 65, 105, 125, 210, 253, 320, 675, 729, 1000,
    6, 10, 11, 12, 13, 14,
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

print("=== 104az-193 扩展扫描 ===")

for size, rng in [(3, range(1, 17)), (4, range(1, 17)), (5, range(1, 17)), (4, range(1, 25))]:
    closed = []
    n = 0
    for s in itertools.combinations(rng, size):
        n += 1
        bad_s, bad_p, _, _ = analyze(s)
        if not bad_s and not bad_p:
            closed.append(s)
    print(f"\n[{size}-元 × {list(rng)[0]}..{list(rng)[-1]}] 候选 {n} 个 → 联合闭包 {len(closed)} 个")
    for s in closed:
        _, _, ss, pp = analyze(s)
        print(f"    {s}  和谱={ss}  积谱={pp}  全积={s[-1] if False else (lambda x: 1 if not x else eval('*'.join(str(v) for v in x)))(s)}")

# 特殊检查：不含 1 的闭包
print("\n=== 不含单位元 1 的闭包（4 元 [1,16]）===")
for s in itertools.combinations(range(2, 17), 4):
    bad_s, bad_p, _, _ = analyze(s)
    if not bad_s and not bad_p:
        print(f"    {s}")

# 特殊检查：5 元含 {1,2,3,5,7}
for s in [(1,2,3,5,7), (1,2,3,7), (1,3,5,7), (3,5,7), (2,3,7), (1,3,7)]:
    bad_s, bad_p, ss, pp = analyze(s)
    print(f"\n检查 {s}：和未命中 {bad_s}；积未命中 {bad_p}")
    if not bad_s and not bad_p:
        print(f"    ✓ 闭包  和谱={ss}  积谱={pp}")
