"""第 57 批模式 8 数值先证伪：StrictLayer 是否蕴含层函数无界，
以及它能否作为 timeLayerDim = 1 的依据。

按 Lean 定义逐字翻译：
  recStep ev 0 r = r ; recStep ev (n+1) r = ev (recStep ev n r)
  StrictLayer ev layerOf  :=  ∀ r, layerOf (ev r) = layerOf r + 1

纯标准库，无 numpy。
"""
import sys

def recStep(ev, k, r):
    for _ in range(k):
        r = ev(r)
    return r

def strictLayer(ev, layerOf, sample):
    return all(layerOf(ev(r)) == layerOf(r) + 1 for r in sample)

# ---- 系统 S：Nat 上后继推进，层函数取恒等 ----
R = list(range(0, 41))
ev = lambda n: n + 1
layerOf = lambda n: n

A_STRICT = strictLayer(ev, layerOf, R)
print("A_STRICTLAYER_NAT_SUCC", A_STRICT)

# ---- A：StrictLayer ⇒ 从任一元素出发 N 步到达 layerOf r + N 层 ----
r0 = 0
hits = []
for N in range(0, 21):
    s = recStep(ev, N, r0)
    hits.append((N, layerOf(s), layerOf(r0) + N))
A_OK = all(h[1] == h[2] for h in hits)
print("A_UNBOUNDED_OK", A_OK)
print("A_SAMPLES", hits[:6])
print("A_LAST", hits[-1])

# ---- B：反例——同一系统里层函数既取到 5 也取到 10 ----
B_5 = layerOf(5) == 5
B_10 = layerOf(10) == 10
print("B_LAYER_5", B_5, "B_LAYER_10", B_10)
print("B_BOTH_IN_ONE_SYSTEM", B_5 and B_10)

# ---- C：spaceLayerDim + q = 4 ⇒ q 唯一为 1 ----
forced = [q for q in range(0, 30) if 3 + q == 4]
print("C_Q_SET", forced)
print("C_UNIQUE", forced == [1])

# ---- D：catOrderOfTime 3 t = 3 + t，扫 t = 0..10 ----
rows = [(t, 3 + t) for t in range(0, 11)]
print("D_ROWS", rows)
print("D_AT_T1", 3 + 1 == 4)
D_OK = all(rows[t][1] == 3 + t for t in range(0, 11))
print("D_OK", D_OK)

# ---- E：该系统的「时间坐标唯一」——步数相等 ⇔ 步数相同 ----
E_OK = True
for k1 in range(0, 9):
    for k2 in range(0, 9):
        for r in range(0, 9):
            if recStep(ev, k1, r) == recStep(ev, k2, r) and k1 != k2:
                E_OK = False
print("E_COORD_UNIQUE_OK", E_OK)

# ---- F：单步必升层 ----
print("F_STEP_RAISES", all(layerOf(ev(r)) != layerOf(r) for r in R))

# ---- G：从 r0 出发 N 步轨道的层集大小与跨度 ----
for N in [1, 2, 5, 10, 20]:
    orb = [recStep(ev, k, 0) for k in range(0, N + 1)]
    im = set(layerOf(x) for x in orb)
    print("G_ORBIT N=%d IMG_SIZE=%d SPAN=%d" % (N, len(im), max(im) - min(im)))

# ---- H：StrictLayer 排除单元集层集——只要有两个可达点，层就不同 ----
H_OK = len(set(layerOf(x) for x in [0, 1])) >= 2
print("H_MIN_IMG_2", H_OK)

# ---- I：若把 timeLayerDim = 1 读作「层集为单元集」，该断言在系统 S 上为假 ----
I_SINGLETON = len(set(layerOf(x) for x in [0, 1])) == 1
print("I_SINGLETON_CLAIM_ON_S", I_SINGLETON)

VERDICT = all([A_STRICT, A_OK, B_5, B_10, forced == [1], D_OK, E_OK, H_OK])
print("VERDICT_ALL_OK", VERDICT)
sys.stdout.flush()
