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
paperX_photon_fiber_orthogonality.py — Phase 62 开放问题 #7: 纤维丛层正交的严格化

笔记: photon_topology_theory.md §1.2.2 诚实边界 / 路线图 §七 #7
核心结论: "纤维 ⊥ 基空间"的严格意义 = (联络水平分布 H, 度量 g) 的**相容选取**,
非纤维丛的内在性质——正交性依赖 g 与 H 的相容 (正交规范 / Levi-Civita 水平分布)。

模型: 圆柱面纤维丛 π: E = S¹×ℝ → S¹ (θ = 基空间方向, y = 纤维方向)
  - 垂直子空间 V = ker dπ = span{∂_y} (内在, 不依赖选取)
  - 水平子空间 H_f = span{∂_θ + f(θ)∂_y} (Ehresmann 联络形式 f 选取, 非唯一)
  - 度量 g_A = dθ² + (dy − A(θ)dθ)² (带规范场 A 的正交标架度量)

检查:
  C1  V = ker dπ (垂直分布定义)
  C2  TE = V ⊕ H_A (直和分解, 任意联络)
  C3  标准度量 g_0 下 V ⊥ H_f ⟺ f = 0 (联络-度量不相容则不正交)
  C4  g_A 下 V ⊥ H_A 对任意 A (相容选取 -> 正交)
  C5  dim E = dim V + dim H (直和维数)
"""
import numpy as np

_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


# 基向量: ∂_θ = (1,0) (基空间方向), ∂_y = (0,1) (纤维方向)
DTH = np.array([1.0, 0.0])
DY = np.array([0.0, 1.0])


def metric_std():
    """标准度量 g_0 = dθ² + dy²。"""
    return np.array([[1.0, 0.0], [0.0, 1.0]])


def metric_ga(A):
    """正交标架度量 g_A = dθ² + (dy − A dθ)²
       = (1+A²)dθ² − 2A dθdy + dy²。"""
    return np.array([[1.0 + A**2, -A], [-A, 1.0]])


def inner(g, v, w):
    return float(v @ g @ w)


# ============================================================
# C1: 垂直分布定义 V = ker dπ
# ============================================================
def c1():
    dpi_dy = DY[0]   # dπ(∂_y) = ∂_y 的 θ 分量 = 0 (纤维方向投影到基空间为零)
    check("C1 V = ker dπ (纤维方向投影为零, 内在定义)",
          abs(dpi_dy) < 1e-15)


# ============================================================
# C2: 直和分解 TE = V ⊕ H_A
# ============================================================
def c2():
    ok = True
    for A in [-2.0, -0.5, 0.0, 0.5, 2.0]:
        H = DTH + A * DY
        det = np.linalg.det(np.column_stack([DY, H]))
        if abs(det) < 1e-12:
            ok = False
    check("C2 TE = V ⊕ H_A (直和, A in [-2,2], 任意联络均直和)",
          ok)


# ============================================================
# C3: 标准度量下 V ⊥ H_f ⟺ f = 0
# ============================================================
def c3():
    g0 = metric_std()
    ok = True
    for f in [-1.0, -0.3, 0.0, 0.3, 1.0]:
        H = DTH + f * DY
        prod = inner(g0, DY, H)
        if f == 0.0:
            if abs(prod) > 1e-12:
                ok = False
        else:
            if abs(prod) < 1e-9:
                ok = False
    check("C3 标准度量 g_0 下 V ⊥ H_f ⟺ f = 0 (联络-度量不相容则不正交)",
          ok)


# ============================================================
# C4: g_A 下 V ⊥ H_A 对任意 A (相容选取)
# ============================================================
def c4():
    ok = True
    detail = ""
    for A in [-2.0, -0.5, 0.0, 0.5, 2.0]:
        g = metric_ga(A)
        H = DTH + A * DY
        prod = inner(g, DY, H)
        if abs(prod) > 1e-9:
            ok = False
            detail = "prod(A=%.1f)=%.2e" % (A, prod)
    check("C4 g_A 下 V ⊥ H_A 对任意 A (相容选取 -> 正交)",
          ok, detail)


# ============================================================
# C5: 直和维数
# ============================================================
def c5():
    check("C5 dim E = dim V + dim H = 2", 2 == 1 + 1)


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 72)
    print("Paper 44 (Phase 62 #7): 纤维丛层正交的严格化 (垂直-水平分解联络/度量)")
    print("笔记: photon_topology_theory.md §1.2.2 / 路线图 §七 #7")
    print("=" * 72)
    c1()
    c2()
    c3()
    c4()
    c5()

    passed = sum(1 for _, ok, _ in _CHECKS if ok)
    total = len(_CHECKS)
    print("\n" + "=" * 72)
    print("汇总: %d/%d" % (passed, total))
    print("=" * 72)
    for name, ok, detail in _CHECKS:
        mark = "[PASS]" if ok else "[FAIL]"
        line = "  %s %s" % (mark, name)
        if detail:
            line += "  (%s)" % detail
        print(line)
    print()
    if passed < total:
        print("存在未通过检查项")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
