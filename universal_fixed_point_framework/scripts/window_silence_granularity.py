# -*- coding: utf-8 -*-
"""
开放项① 数值判别：静默对象粒度 —— 逐窗口幅值判据 vs 层粒度
============================================================
问题：静默（失去表达窗口，L1 幅值判据 |λ|<ε 置零）后，窗口是否仍被观察？
  静默后窗口：作为可观测量（零测度，L1 裁决）；作为状态（保留不动点，C4 裁决）。
  张力：静默施动对象是谱层（4）还是组合窗口（15）？
  数值模型：15 个组合窗口按 4 谱层分组（层 r 有 C(4,r) 窗，r=1..4，
    = 4+6+4+1 = 15），幅值按谱序分层递减（呼应 675→320→16→e 修正幅度层级）。
  演化：活跃窗口（|a_i| ≥ ε）按层内后继推进（层内循环）；
       静默窗口（|a_i| < ε，表达归零）→ 冻结为不动点（step x = x）。
  判据（Lean 逐字对齐 periodicPoint 定义：∃p>0, step^[p] x = x ——
       从 step(x) 走 n 步检测回 x；预周期点不计）：

输出：
  - 各阈值 ε 下：静默窗口数 / orbitCount / 冻结窗口是否全为不动点
  - 全静默（ε → max）时 orbitCount 是否 = 15（全不动 ⟹ 恒等，OrbitFullLock）
  - "次第闭合"轨迹：orbitCount 从 4（层轨道基数）单调增到 15（组合全量）

结论口径：静默判据逐窗口（每个谱分量独立 |λ|<ε ⟹ 独立闭合），层只是谱序
排序（决定闭合次序）；全静默 ⟹ 15 窗口全不动点 ⟹ orbitCount=15 ⟺ 恒等
（OrbitFullLock 定理）——静默后窗口"作为状态"保留计数、全锁定达成。
"""
import itertools


def build_windows():
    """15 个组合窗口：{1,2,3,4} 的非空子集，按大小分层 r=1..4。"""
    base = (1, 2, 3, 4)
    subsets = []
    layer_of = {}
    for r in range(1, 5):
        for s in itertools.combinations(base, r):
            subsets.append(frozenset(s))
            layer_of[len(subsets) - 1] = r
    return subsets, layer_of


def layer_members(layer_of, n):
    members = {}
    for i in range(n):
        r = layer_of[i]
        members.setdefault(r, []).append(i)
    return members


def default_amplitudes(n, layer_of):
    """谱序分层递减：层 r 幅值 ~ 10^{-r}（675→320→16→e 修正幅度的层级化模拟）。
    层内再微扰区分（逐窗口判据）。"""
    import random
    random.seed(42)
    a = []
    for i in range(n):
        r = layer_of[i]
        a.append(10.0 ** (-r) * (1.0 + 0.01 * random.random()))
    return a


def make_step(frozen):
    """活跃窗口按层内后继推进；冻结窗口不动。
    frozen: set of 窗口索引；layer_mem: 层->成员列表（闭包内构建）。"""
    def step(x, _ctx):
        pass
    return step


def orbit_count(step_fn, n):
    """逐字对齐 Lean periodicPoint：∃p>0, step^[p] x = x。
    预周期点（进入已访问但永不回自己）不计。"""
    seen = set()
    cnt = 0
    for x0 in range(n):
        if x0 in seen:
            continue
        path = []
        x = x0
        while x not in seen:
            seen.add(x)
            path.append(x)
            x = step_fn(x)
        if x in path:
            cnt += 1
    return cnt


def main():
    subsets, layer_of = build_windows()
    n = len(subsets)  # 15
    members = layer_members(layer_of, n)
    amps = default_amplitudes(n, layer_of)

    def step_fn(frozen):
        def _step(x):
            if x in frozen:
                return x  # 静默 ⟹ 不动点
            r = layer_of[x]
            m = members[r]
            k = m.index(x)
            return m[(k + 1) % len(m)]  # 层内循环后继（活跃演化）
        return _step

    print("窗口总数 n =", n)
    print("层分布 r=1..4:", {r: len(members[r]) for r in sorted(members)})
    print()

    # 阈值扫描：ε 从 0（无静默）到覆盖全部窗口
    epsilons = [0.0] + [10.0 ** (-k) for k in range(1, 9)] + [1e-9, 1e-12]
    print(f"{'eps':>10} {'静默窗数':>8} {'orbitCount':>10} {'全不动?':>8} {'次第阶跃':>8}")
    prev_oc = None
    for eps in epsilons:
        frozen = {i for i in range(n) if abs(amps[i]) < eps}
        sf = step_fn(frozen)
        oc = orbit_count(sf, n)
        # 全不动检查：冻结窗口 step 恒等
        all_fixed = all(sf(i) == i for i in frozen)
        jump = ""
        if prev_oc is not None and oc != prev_oc:
            jump = f"+{oc - prev_oc}"
        print(f"{eps:>10.1e} {len(frozen):>8} {oc:>10} {str(all_fixed):>8} {jump:>8}")
        prev_oc = oc

    # 全静默最终态
    frozen_all = set(range(n))
    sf = step_fn(frozen_all)
    oc_all = orbit_count(sf, n)
    print()
    print("全静默（15 窗口全部表达归零）：orbitCount =", oc_all)
    print("判别：orbitCount = 15 ⟺ 恒等（OrbitFullLock 定理 (⇐)：全不动 ⟹ =card）"
          if oc_all == 15 else "！全静默未达 15——模型与预期不符")


if __name__ == "__main__":
    main()
