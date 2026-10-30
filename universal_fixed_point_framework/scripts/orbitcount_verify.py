# -*- coding: utf-8 -*-
"""orbitCount 定义锚 · 数值证伪/验证（2026-10-23）
验证对象（Lean 定义的逐字翻译）：
  1. periodicPoint：∃ p>0, step^[p] x = x
  2. periodOrbitRel（同一循环）：x,y 均为周期点 且 ∃ n, step^[n] x = y
  3. 周期点可达性 = 等价关系（refl/symm/trans）
  4. orbitCount = 周期点商集大小 ≤ card X.T；有偏心 ⟹ orbitCount > 0
反例探测（诚实边界）：
  5. 可达性在非周期点（预周期尾巴）上不对称 —— 确认定义必须限制在周期点集
pyenv 3.11.8 运行。
"""
import random
from itertools import product

random.seed(20261023)

def orbits_of(step, n):
    """计算全部周期点、每个点的可达终点、循环数（并查集）"""
    periodic = []
    for x in range(n):
        p = 1
        cur = step[x]
        while cur != x and p <= n:
            cur = step[cur]
            p += 1
        if cur == x:
            periodic.append(x)
    P = set(periodic)
    # 周期点集上可达性（∃k, step^k x = y）
    def reach(x, y, limit=2 * n):
        seen = set()
        cur = x
        for _ in range(limit):
            if cur == y:
                return True
            if cur in seen:
                return False
            seen.add(cur)
            cur = step[cur]
        return False
    # 检查等价关系三性质（在 P 上）
    ok_refl = all(reach(x, x) for x in P)
    ok_symm = all((not reach(x, y)) or reach(y, x) for x in P for y in P)
    ok_trans = all((not (reach(x, y) and reach(y, z))) or reach(x, z) for x in P for y in P for z in P)
    # 循环数：P 的等价类数
    reps = []
    for x in P:
        if not any(reach(r, x) for r in reps):
            reps.append(x)
    orbit_count = len(reps)
    return P, orbit_count, (ok_refl, ok_symm, ok_trans)

def tail_asymmetry_example():
    """构造/寻找尾巴不对称实例：x（非周期点）可达 y（周期点），但 y 不可达 x"""
    for n in range(3, 12):
        for step in product(range(n), repeat=n):
            # step: 预周期尾巴 x0 -> x1 -> ... -> 循环
            if step[0] != 0 and step[1] == 1 and step[0] == 1:  # 0 -> 1 不动点
                P, _, _ = orbits_of(list(step), n)
                if 0 not in P and 1 in P:
                    return (n, step, 0, 1)
    return None

def main():
    worst_refl = worst_symm = worst_trans = 0.0
    max_cnt = max_card = 0
    trials = 5000
    fails = []
    for _ in range(trials):
        n = random.randint(2, 30)
        step = [random.randrange(n) for _ in range(n)]
        P, cnt, (r1, r2, r3) = orbits_of(step, n)
        if not (r1 and r2 and r3):
            fails.append((n, step, P, (r1, r2, r3)))
        worst_refl += 0 if r1 else 1
        worst_symm += 0 if r2 else 1
        worst_trans += 0 if r3 else 1
        max_cnt = max(max_cnt, cnt)
        max_card = max(max_card, n)
        # 基本性质：0 ≤ cnt ≤ |P| ≤ n
        assert 0 <= cnt <= len(P) <= n, (n, cnt, len(P))
        # 偏心 ⟹ orbitCount > 0
        eccentric = any(step[x] != x for x in range(n))
        if eccentric:
            assert cnt > 0, (n, step)
    print(f"trials={trials} n∈[2,30]")
    print(f"refl 违例 {worst_refl} / symm 违例 {worst_symm} / trans 违例 {worst_trans}")
    print(f"orbitCount 范围 [0,{max_cnt}] ≤ card X.T ≤ {max_card}")
    print("反例（尾巴不对称）示例：", tail_asymmetry_example())
    if fails:
        print("FAIL:", fails[:3])
    else:
        print("PASS：周期点可达性=等价关系；orbitCount ≤ |P| ≤ |X|；偏心 ⟹ orbitCount>0")

if __name__ == "__main__":
    main()
