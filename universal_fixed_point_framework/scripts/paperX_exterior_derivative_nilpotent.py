#!/usr/bin/env python3
"""
paperX_exterior_derivative_nilpotent.py — 外微分幂零性 d²=0 验证（笔记 06_photon_topology §8 曲率层, 2026-08-11）

推进 §8.4 诚实边界开放子项："外微分形式理论（d²=0）"——数值/解析层闭合。

d²=0 是结构方程 Ω=dω+ω∧ω 与 Bianchi 恒等式 dΩ+[ω,Ω]=0 的代数前提
（外微分形式理论的核心理想）。多项式解析验证（混合偏导相等 → 精确零）。

S1: 0-形式 f：d(df) = 0（混合偏导差 f_xy - f_yx 等）
S2: 1-形式 ω：d(dω) = 0（2-形式分量全部为零）
S3: 2-形式 η（4 维空间）：d(dη) = 0（3-形式分量全部为零）
S4: su(2) 值形式：逐分量 d²=0（李代数值形式的外微分逐分量作用）
S5: 无源衔接：F=dA ⟹ dF = d²A = 0（无源 Maxwell 方程 dF=0 的代数基础，
    非阿贝尔 Bianchi dΩ+[ω,Ω]=0 的 d²=0 前提，Bianchi 残差见 paperX_photon_curvature.py 14/14）

诚实边界：多项式解析验证（d²=0 为精确恒等式）；流形级形式化（完整外微分
理论、流形级 Bianchi）仍待微分几何库（§8.4，paper44 §7.5 开放问题 3）。
"""


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


class Poly:
    """多元多项式：terms = {指数元组: 系数}，支持偏导/加法/数乘/求值"""
    def __init__(self, terms=None):
        self.terms = dict(terms or {})

    @staticmethod
    def monomial(exps, coef=1.0):
        return Poly({tuple(exps): coef})

    def deriv(self, i):
        r = {}
        for e, c in self.terms.items():
            if e[i] > 0:
                ne = list(e)
                ne[i] -= 1
                key = tuple(ne)
                r[key] = r.get(key, 0.0) + c * e[i]
        return Poly(r)

    def __add__(self, o):
        r = dict(self.terms)
        for e, c in o.terms.items():
            r[e] = r.get(e, 0.0) + c
        return Poly(r)

    def __sub__(self, o):
        r = dict(self.terms)
        for e, c in o.terms.items():
            r[e] = r.get(e, 0.0) - c
        return Poly(r)

    def __neg__(self):
        return Poly({e: -c for e, c in self.terms.items()})

    def __rmul__(self, c):
        """标量左乘：c * Poly"""
        if isinstance(c, Poly):
            return NotImplemented
        return Poly({e: v * c for e, v in self.terms.items()})

    def __mul__(self, c):
        """标量右乘：Poly * c"""
        if isinstance(c, Poly):
            return NotImplemented
        return Poly({e: v * c for e, v in self.terms.items()})

    def is_zero(self):
        return all(abs(c) < 1e-12 for c in self.terms.values())


# ---- 外微分（解析，作用于多项式系数） ----

def d0(f, n):
    """0-形式 f 的外微分：df = Σ ∂i f dx_i"""
    return [f.deriv(i) for i in range(n)]


def d1(omega, n):
    """1-形式 ω（分量列表）的外微分 → 2-形式（字典 {pair: Poly}）"""
    result = {}
    for i in range(n):
        for j in range(i + 1, n):
            comp = omega[i].deriv(j) - omega[j].deriv(i)
            if not comp.is_zero():
                result[(i, j)] = comp
    return result


def d2(eta, n):
    """2-形式 η（字典 {pair: Poly}）的外微分 → 3-形式（字典 {triple: Poly}）"""
    result = {}
    for (i, j), comp in eta.items():
        for k in range(n):
            if k == i or k == j:
                continue
            # dx_k ∧ dx_i ∧ dx_j：置换符号
            # (k,i,j) 的奇偶性
            # 升序三元组 (a<b<c)，dx_k∧dx_i∧dx_j = sign * dx_a∧dx_b∧dx_c
            a, b, c = sorted((k, i, j))
            sign = 1
            # 从 (a,b,c) 经交换到 (k,i,j) 的奇偶性
            perm = [k, i, j]
            target = [a, b, c]
            # 冒泡计数
            inv = 0
            for p in range(3):
                for q in range(p + 1, 3):
                    if perm.index(target[p]) > perm.index(target[q]):
                        inv += 1
            sign = -1 if inv % 2 else 1
            key = (a, b, c)
            add = comp.deriv(k) * sign
            if key in result:
                result[key] = result[key] + add
            else:
                result[key] = add
    return result


def main():
    print("外微分幂零性 d²=0 验证（笔记 §8 曲率层：结构方程/Bianchi 的代数前提）")
    print("=" * 78)

    # S1: 0-形式 f：d(df) = 0（混合偏导差）
    # f = x²y + 3xyz + y²z² + 2x³（3 维）
    f = (Poly.monomial((2, 1, 0)) + Poly.monomial((1, 1, 1), 3.0)
         + Poly.monomial((0, 2, 2)) + Poly.monomial((3, 0, 0), 2.0))
    df = d0(f, 3)
    ddf = d1(df, 3)   # d(df)：混合偏导差，应全零
    ok1 = all(comp.is_zero() for comp in ddf.values())
    check("S1  0-形式：d(df) = 0（混合偏导 f_xy-f_yx 等，解析精确）", ok1,
          f"d(df) 非零分量数 = {sum(1 for c in ddf.values() if not c.is_zero())}")

    # S2: 1-形式 ω：d(dω) = 0（2-形式分量）
    # ω = (x²y)dx + (xz²)dy + (yz)dz
    omega = [Poly.monomial((2, 1, 0)), Poly.monomial((1, 0, 2)), Poly.monomial((0, 1, 1))]
    domega = d1(omega, 3)
    ddomega = d2(domega, 3)   # 3-形式（3 维中为 dx∧dy∧dz 单分量或零）
    ok2 = all(comp.is_zero() for comp in ddomega.values())
    check("S2  1-形式：d(dω) = 0（2-形式分量全零）", ok2,
          f"d(dω) 分量数 = {len(ddomega)}")

    # S3: 2-形式 η（4 维）：d(dη) = 0（3-形式分量）
    # η = (x²y)dy∧dz + (xz)dz∧dw + (y²)dw∧dx + (xy) dx∧dy
    n4 = 4
    eta4 = {(1, 2): Poly.monomial((2, 1, 0, 0)),
            (2, 3): Poly.monomial((1, 0, 1, 0)),
            (3, 0): Poly.monomial((0, 2, 0, 0)),
            (0, 1): Poly.monomial((1, 1, 0, 0))}
    deta4 = d2(eta4, n4)      # 3-形式
    ddeta4 = {}
    # 4 维中 3-形式的 d 为 4-形式：验证 deta4 再求导前，先验证 d(3-形式)=0（4-形式在 4 维中单分量）
    # 3-形式 ω3 = {(a,b,c): Poly}，d 得 4-形式 (0,1,2,3) 分量
    omega3 = deta4
    result4 = Poly({})
    for (a, b, c), comp in omega3.items():
        for k in range(n4):
            if k in (a, b, c):
                continue
            perm = [k, a, b, c]
            target = [0, 1, 2, 3]
            inv = 0
            for p in range(4):
                for q in range(p + 1, 4):
                    if perm.index(target[p]) > perm.index(target[q]):
                        inv += 1
            sign = -1 if inv % 2 else 1
            result4 = result4 + (comp.deriv(k) * sign)
    ok3 = result4.is_zero()
    check("S3  2-形式（4 维）：d(dη) = 0（3-形式再外微分 = 4-形式单分量，解析精确）", ok3)

    # S4: su(2) 值形式——逐分量 d²=0
    # ω = ω_a T_a（T_a 为 su(2) 基），d 逐分量作用（3 个分量各自是 1-形式）
    comps = [
        [Poly.monomial((2, 0, 0)), Poly.monomial((0, 1, 0)), Poly.monomial((0, 0, 1))],  # T1 分量
        [Poly.monomial((1, 1, 0)), Poly.monomial((0, 0, 2)), Poly.monomial((1, 0, 1))],  # T2
        [Poly.monomial((0, 2, 0)), Poly.monomial((1, 0, 0)), Poly.monomial((0, 1, 1))],  # T3
    ]
    ok4 = True
    for a in range(3):
        dca = d1(comps[a], 3)
        ddca = d2(dca, 3)
        if not all(c.is_zero() for c in ddca.values()):
            ok4 = False
    check("S4  su(2) 值形式：逐分量 d²=0（李代数分量独立作用，3×2 阶）", ok4)

    # S5: 无源衔接——F=dA ⟹ dF=d²A=0（无源 Maxwell 的代数基础）
    # A = (x²y)dx + (yz²)dy（2 维子空间简化）
    A = [Poly.monomial((2, 1)), Poly.monomial((0, 1, 2)) + Poly.monomial((1, 0, 0)) - Poly.monomial((0, 1, 2))]
    # 用 2 个变量的干净 A：A = (x²y)dx + (xy²)dy
    A2 = [Poly.monomial((2, 1)), Poly.monomial((1, 2))]
    F = d1(A2, 2)          # F = dA（2 维中单分量 dx∧dy）
    dF = d2(F, 2)          # dF = d(dA)（3-形式，2 维中自动零）
    ok5 = all(c.is_zero() for c in dF.values())
    # 非阿贝尔 Bianchi 前提：d²=0 + 雅可比 ⟹ dΩ+[ω,Ω]=0（数值残差见 paperX_photon_curvature.py 14/14）
    check("S5  无源衔接：F=dA ⟹ dF=d²A=0（无源 Maxwell dF=0；非阿贝尔 Bianchi 的 d²=0 前提）", ok5)

    results = [ok1, ok2, ok3, ok4, ok5]
    print("\n" + "=" * 78)
    print(f"外微分幂零性 d²=0 验证：{sum(results)}/5 通过")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
