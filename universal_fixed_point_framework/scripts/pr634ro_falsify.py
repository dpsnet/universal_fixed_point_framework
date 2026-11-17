# -*- coding: utf-8 -*-
"""第 63 批数值先证伪：层标号有限性 + B = 3×5 的交叉项解剖。
纯标准库，按 Lean 定义逐字翻译。"""
import sys

ACTIVE = 3          # ActiveLayers.card（one/two/three）
NON_ACTIVE = 2      # obj + four
N_TOTAL = 5         # Fintype.card LayerIndex / N_total
B = ACTIVE * N_TOTAL

ok = True
def chk(name, cond, val):
    global ok
    if not cond:
        ok = False
    print(name, val)

# A 划分完整
chk("A_PARTITION_OK", ACTIVE + NON_ACTIVE == N_TOTAL,
    "[(active,%d),(non_active,%d),(total,%d)]" % (ACTIVE, NON_ACTIVE, N_TOTAL))

# B 交叉项分解
chk("B_DECOMP_OK", B == ACTIVE * ACTIVE + ACTIVE * NON_ACTIVE,
    "[%d = %d + %d]" % (B, ACTIVE * ACTIVE, ACTIVE * NON_ACTIVE))

# C 四读数互异
readouts = [B, ACTIVE * (N_TOTAL - 1), ACTIVE * ACTIVE, ACTIVE * NON_ACTIVE]
chk("C_READOUTS_DISTINCT", len(set(readouts)) == 4, str(readouts))

# D 去掉对象层
chk("D_OBJECT_REMOVED", ACTIVE * (N_TOTAL - 1) == 12,
    "[%d]" % (ACTIVE * (N_TOTAL - 1)))

# E 换基数给不出 15
bad = [n for n in range(2, 21) if n != 5 and ACTIVE * n == 15]
chk("E_NO_OTHER_CARD", bad == [], "[n=2..20 异常项 %s]" % bad)

# F 有限标号不能封顶（对四个候选读数都取 k > N）
caps = [N_TOTAL, ACTIVE * (N_TOTAL - 1), ACTIVE * ACTIVE, ACTIVE * NON_ACTIVE]
breaks = [(N, max(2, N + 1)) for N in caps]
chk("F_NO_CAP", all(k > N for N, k in breaks), str(breaks))

# G 读数两两差：15-12=3, 15-9=6, 15-6=9, 12-9=3, 12-6=6, 9-6=3
diffs = [(a, b, a - b) for i, a in enumerate(readouts) for b in readouts[i + 1:]]
chk("G_DIFFS_OK", all(d > 0 for _, _, d in diffs), str(diffs))

print("VERDICT_ALL_OK", ok)
sys.exit(0 if ok else 1)
