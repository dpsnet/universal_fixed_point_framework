# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
paperX_z2_topological_charge.py — Z₂ 值拓扑荷公理化的代数结构验证（笔记 06_photon_topology 方向 5 §6.9, 2026-08-11）

推进开放问题：统一"自旋 = 拓扑荷"语言（§6.6② / §6.8③ 的共同底层）——Z₂ 值拓扑荷的公理化。

候选公理化（框架内尝试，非定理）：设 X 为 Rec/Sp 谱对象，其 Z₂ 值拓扑荷为
σ: Obj(Sp) → Z₂ = {+1,-1}，满足：
  (A1) 离散性：σ 为连续形变/谱流不变量（同伦不变量）；
  (A2) 张量性：σ(X⊗Y) = σ(X)·σ(Y)（谱对象复合时 Z₂ 值相乘）；
  (A3) 核结构：σ 的核对应双覆盖纤维（每取值恰 2 提升，覆盖空间结构）；
  (A4) 外显性：Z₂ 值拓扑荷的"外显"（可观测自旋）由与时间的关系决定（§6.7 作用角度×作用点数量）。

S1: Z₂ 群结构——{+1,-1} 乘法与模 2 加法同构（费米子×费米子=玻色子等组合规则）
S2: 对称群符号同态 sign: S_N → Z₂——排列奇偶性满足 sign(σ∘τ)=sign(σ)sign(τ)（A2 张量性的实例）
S3: N 粒子交换符号 (-1)^{N(N-1)/2} 与 Z₂ 值自洽（自旋-统计组合规则）
S4: Levi-Civita ε = Z₂ 值——三粒子反对称张量（偶/奇置换 ±1）
S5: 张量性候选实例——双粒子组合 σ(X⊗Y)=σ(X)σ(Y) 在光子螺旋度与费米子符号上的自洽

诚实边界：对称群符号同态/Levi-Civita 为标准代数事实；"Z₂ 值拓扑荷公理化"
为框架内尝试性定义（非定理），脚本仅验证 Z₂ 值代数结构的自洽性，不构成新物理预言。
"""
import itertools

import numpy as np


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def perm_sign(p):
    """排列奇偶性：逆序对数的奇偶 → +1（偶）/ -1（奇）"""
    n = len(p)
    inv = 0
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                inv += 1
    return 1 if inv % 2 == 0 else -1


def main():
    print("Z₂ 值拓扑荷公理化——代数结构验证（笔记方向 5 §6.9）")
    print("=" * 78)

    # S1: Z₂ 群结构——{+1,-1} 乘法与模 2 加法同构
    elems = [1, -1]
    ok1 = True
    for a in elems:
        for b in elems:
            m = a * b
            # 模 2 加法：0↔+1, 1↔-1；加法结果 ↔ 乘法结果
            mod2_sum = 1 if ((a == -1) + (b == -1)) % 2 == 0 else -1
            if m != mod2_sum:
                ok1 = False
    # 乘法表检查：(-1)·(-1)=+1（费米子×费米子=玻色子）、(+1)·(-1)=-1
    ok1 = ok1 and (-1) * (-1) == 1 and 1 * (-1) == -1
    check("S1  Z₂ 群结构：{+1,-1} 乘法 ≅ 模 2 加法（(-1)²=+1：费米子×费米子=玻色子）", ok1)

    # S2: 对称群符号同态 sign: S_N → Z₂（A2 张量性的实例）
    N = 4
    perms = list(itertools.permutations(range(N)))
    ok2 = True
    for sig in perms:
        for tau in perms:
            comp = tuple(sig[tau[i]] for i in range(N))
            if perm_sign(comp) != perm_sign(sig) * perm_sign(tau):
                ok2 = False
    check("S2  sign: S_N → Z₂ 群同态（sign(σ∘τ)=sign(σ)sign(τ)，S₄ 全体 24² 组合）", ok2,
          f"|S₄|={len(perms)}")

    # S3: N 粒子交换符号 (-1)^{N(N-1)/2} 与 Z₂ 值自洽（自旋-统计组合规则）
    ok3 = True
    for n in range(1, 11):
        sgn = (-1) ** (n * (n - 1) // 2)
        # 对交换次数 N(N-1)/2 的奇偶性
        parity = (n * (n - 1) // 2) % 2
        if sgn != (1 if parity == 0 else -1):
            ok3 = False
    check("S3  N 粒子交换符号 (-1)^{N(N-1)/2}（交换数奇偶性 ↔ Z₂ 值）", ok3)

    # S4: Levi-Civita ε = Z₂ 值——三粒子反对称张量（偶/奇置换 ±1）
    base = (0, 1, 2)
    # 偶置换 +1：(012),(120),(201)；奇置换 -1：(102),(021),(210)
    eps = {(0, 1, 2): 1, (1, 2, 0): 1, (2, 0, 1): 1,
           (1, 0, 2): -1, (0, 2, 1): -1, (2, 1, 0): -1}
    ok4 = all(eps[p] == perm_sign(p) for p in eps)
    check("S4  Levi-Civita ε = Z₂ 值（三粒子反对称张量：偶置换 +1、奇置换 -1）", ok4)

    # S5: 张量性候选实例——双粒子组合 σ(X⊗Y)=σ(X)σ(Y)
    # 光子：s=±1（螺旋度）；费米子：Z₂=-1；玻色子：Z₂=+1
    # 组合：光子⊗光子 (s₁s₂)、费米子⊗费米子 ((−1)·(−1)=+1 玻色子型)、费米子⊗玻色子 (−1)
    photon = [1, -1]
    ok5 = True
    for s1 in photon:
        for s2 in photon:
            if s1 * s2 not in photon:   # 光子螺旋度组合封闭于 Z₂
                ok5 = False
    if (-1) * (-1) != 1 or (-1) * 1 != -1 or 1 * 1 != 1:
        ok5 = False
    check("S5  张量性候选：σ(X⊗Y)=σ(X)σ(Y) 自洽（光子 s₁s₂ 封闭于 Z₂、费米子⊗费米子=玻色子型）", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"Z₂ 值拓扑荷代数结构验证：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
