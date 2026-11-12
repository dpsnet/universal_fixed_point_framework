# -*- coding: utf-8 -*-
"""第 52 批 模式 8 数值先证伪：
   命题 A：NoNontrivialCycle + 唯一不动点 => 存在 DepthData（显式编码构造）
   命题 B：DepthData 存在 => 唯一不动点（必要性）
   编码：rho x = (n - h x)*(n+1) + idx x，M = rho m，h x = 到不动点所需步数
"""

def orbits(step, n):
    res = []
    for x in range(n):
        seq = [x]
        for _ in range(n + 2):
            seq.append(step[seq[-1]])
        res.append(seq)
    return res

def nnc(step, n):
    """NoNontrivialCycle: step^[k] x = x (k>=2) 只能因 step x = x"""
    for x in range(n):
        y = x
        for k in range(1, n + n + 3):
            y = step[y]
            if y == x and k >= 2:
                if step[x] != x:
                    return False, (x, k)
    return True, None

def fixcount(step, n):
    return sum(1 for x in range(n) if step[x] == x)

def hfun(step, n, m):
    """到不动点所需步数（前提：唯一不动点 m，且 NNC）"""
    h = {}
    for x in range(n):
        y, t = x, 0
        while y != m:
            y = step[y]
            t += 1
            if t > n + 1:
                return None
        h[x] = t
    return h

def build(step, n, m):
    h = hfun(step, n, m)
    if h is None:
        return None, "h_undefined"
    idx = {x: x for x in range(n)}       # e = 恒等编号（idx < n）
    c = n + 1
    rho = {x: (n - h[x]) * c + idx[x] for x in range(n)}
    M = rho[m]
    return (rho, M, h), None

def check_depthdata(step, n, m, data):
    rho, M, h = data
    # hinj
    if len(set(rho.values())) != n:
        return "HINJ_FAIL"
    # hmax
    if any(rho[x] > M for x in range(n)):
        return "HMAX_FAIL"
    # htop
    if rho[m] != M:
        return "HTOP_FAIL"
    # hprog
    for x in range(n):
        if rho[x] != M and not (rho[x] < rho[step[x]]):
            return "HPROG_FAIL@%d" % x
    # hstep
    for x in range(n):
        if not (rho[x] < rho[step[x]] or step[x] == x):
            return "HSTEP_FAIL@%d" % x
    return None

# 主扫描：n = 1..5 全部映射
TOTAL = 0
NNC_AND_UNIQ = 0
BUILD_OK = 0
FAILS = []
NECESSITY_FAILS = []
for n in range(1, 6):
    for code in range(n ** n):
        step = []
        v = code
        for _ in range(n):
            step.append(v % n)
            v //= n
        TOTAL += 1
        ok, _ = nnc(step, n)
        f = fixcount(step, n)
        if not ok:
            continue
        # NNC 成立的对象：DepthData 存在 => f == 1（必要性）
        if f != 1:
            # 由必要性判据，这些对象不应能构造 DepthData；
            # 但构造算法需要唯一 m，跳过并记录
            NECESSITY_NOTES = True
            continue
        NNC_AND_UNIQ += 1
        m = [x for x in range(n) if step[x] == x][0]
        data, err = build(step, n, m)
        if err:
            FAILS.append((n, step, err))
            continue
        ck = check_depthdata(step, n, m, data)
        if ck:
            FAILS.append((n, step, ck))
        else:
            BUILD_OK += 1
        # 必要性：f == 1 且能构造，从未出现 f != 1 而构造成功
        if f != 1:
            NECESSITY_FAILS.append((n, step))

print("TOTAL_MAPS", TOTAL)
print("NNC_AND_UNIQUE_FIX", NNC_AND_UNIQ)
print("BUILD_OK", BUILD_OK)
print("BUILD_FAILS", len(FAILS))
if FAILS[:6]:
    print("FAIL_SAMPLES", FAILS[:6])
print("VERDICT_A", BUILD_OK == NNC_AND_UNIQ)
print("VERDICT_B", len(NECESSITY_FAILS) == 0)

# 反例对象：twofix 型（n=4: 0->1->1, 2->3->3）
step_twofix = [1, 1, 3, 3]
n2 = 4
ok2, _ = nnc(step_twofix, n2)
f2 = fixcount(step_twofix, n2)
print("TWOFIX_NNC", ok2, "FIX", f2)
# 必要性：f2 == 2 => 无 DepthData（由 top_is_fixpoint + eq_top_of_fixpoint 强制 f==1）
print("TWOFIX_NO_DEPTHDATA", ok2 and f2 != 1)

# 反例对象：loopOne（0->1->0, 2->3->3）不满足 NNC
step_loop = [1, 0, 3, 3]
ok3, wit = nnc(step_loop, 4)
print("LOOPONE_NNC", ok3, "WITNESS", wit, "FIX", fixcount(step_loop, 4))

# chain4 型：0->1->2->3->3
step_chain = [1, 2, 3, 3]
ok4, _ = nnc(step_chain, 4)
data4, err4 = build(step_chain, 4, 3)
print("CHAIN4_NNC", ok4, "FIX", fixcount(step_chain, 4),
      "CHECK", check_depthdata(step_chain, 4, 3, data4) if data4 else err4,
      "RHO", data4[0] if data4 else None, "M", data4[1] if data4 else None)

# 大样本随机（n = 6..9，只测 NNC + 唯一不动点）
import random
random.seed(20261112)
R_TOTAL = 0
R_OK = 0
R_FAIL = []
for trial in range(4000):
    n = random.randint(6, 9)
    step = [random.randrange(n) for _ in range(n)]
    ok, _ = nnc(step, n)
    f = fixcount(step, n)
    if not (ok and f == 1):
        continue
    R_TOTAL += 1
    m = [x for x in range(n) if step[x] == x][0]
    data, err = build(step, n, m)
    if err or check_depthdata(step, n, m, data):
        R_FAIL.append((n, step, err or check_depthdata(step, n, m, data)))
    else:
        R_OK += 1
print("RANDOM_NNC_UNIQ", R_TOTAL)
print("RANDOM_OK", R_OK)
print("RANDOM_FAILS", len(R_FAIL))
print("VERDICT_ALL_OK", BUILD_OK == NNC_AND_UNIQ and len(FAILS) == 0
      and len(NECESSITY_FAILS) == 0 and R_OK == R_TOTAL and len(R_FAIL) == 0
      and ok4 and ok2 and f2 == 2 and not ok3)
