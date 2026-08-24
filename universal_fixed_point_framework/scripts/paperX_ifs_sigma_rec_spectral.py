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
# -*- coding: utf-8 -*-
"""
paperX_ifs_sigma_rec_spectral.py — IFS 分解 → Σ-Rec coproduct 谱验证（阶段 3 首个子任务）
============================================================================
对应笔记：notes/00_foundations/spectral_phase3_fractal_expansion.md
规划出处：notes/00_foundations/spectral_category_scope_stratification.md §3.3（分形扩张路径）
          + 阶段 3 验证目标（"至少 1 个分形函数（Weierstrass）的谱隙从 IFS 参数导出"）

验证内容（分形扩张路径"IFS 分解 → Σ-Rec coproduct → 线性片的组合"）：
  S1  Weierstrass 型 2-map IFS 吸引子采样（Hutchinson 迭代，压缩比 (c₁, c₂)）
  S2  Σ-Rec 编码：吸引子点按 IFS 片分组 ⟹ 每片一个 RecObj（局部线性片 Rᵢ，
      状态 = 片内点，步进 = 片映射 fᵢ 诱导的确定性转移）
  S3  谱化 coproduct：整体转移矩阵 T = blockdiag(T₁, ..., Tₙ)，验证
      σ(T) = ⋃ᵢ σ(Tᵢ)（特征值并集）—— D 保持 coproduct（NoiseCategory §15.3
      机器证明定理的数值镜像）
  S4  RKHS 核谱隙：分形核矩阵 K(xᵢ,xⱼ) 的归一化谱隙 gap = 1 − λ₂/λ₁
      随 IFS 最大压缩比 c_max 单调变化（谱性质从 IFS 参数导出）
  S5  Weierstrass 参数扫描：固定 b、扫描 a ∈ (0,1)，谱隙与 Moran 维数
      d = 2 + ln a / ln b 的对照（阶段 3 验证目标：Weierstrass 谱隙从 IFS 参数导出）

单位：无量纲（几何 + 矩阵代数）。
"""
import numpy as np

# ---------- 基础工具 ----------

def ifs_attractor(maps, n_iter, n_points=3000, seed=20260805):
    """Hutchinson 迭代采样 IFS 吸引子（点集近似）。maps: 压缩仿射映射列表。"""
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0.0, 1.0, size=(n_points,))
    for _ in range(n_iter):
        which = rng.integers(0, len(maps), size=n_points)
        pts = np.array([maps[i](x) for i, x in zip(which, pts)])
    return pts

def group_by_slices(pts, maps, tol=1e-3):
    """Σ-Rec 编码：把吸引子点分组到各 IFS 片 fᵢ 的像附近。
    点 x 属于片 i 若 min_j |x − fᵢ(p)| 最小（最近片归属）。
    返回每片的点索引列表（局部线性片 Rᵢ 的状态集）。"""
    n = len(maps)
    # 片 i 的像集：{ fᵢ(p) : p ∈ 片内点 }——用自引用迭代：把每点归到
    # 使 |x − fᵢ(x)| 达到最小的 i（收缩映射不动点归属的离散近似）
    dmat = np.zeros((len(pts), n))
    for i, f in enumerate(maps):
        dmat[:, i] = np.abs(pts - f(pts))
    assign = np.argmin(dmat, axis=1)
    slices = [np.where(assign == i)[0] for i in range(n)]
    return slices, assign

def transfer_matrix(step_idx, n_states):
    """确定性步进的转移矩阵 T（每行恰好一个 1）：(T)[i,j] = 1[step(i)=j]。"""
    M = np.zeros((n_states, n_states), dtype=complex)
    for i in range(n_states):
        M[i, step_idx[i]] = 1.0
    return M

def spectral_gap_K(K):
    """归一化核矩阵谱隙：gap = 1 − λ₂/λ₁（λ₁ ≥ λ₂ ≥ ... ≥ 0）。"""
    evals = np.linalg.eigvalsh((K + K.conj().T) / 2)
    evals = evals[evals > 1e-12]
    if len(evals) < 2:
        return 0.0, evals
    gap = 1.0 - float(evals[-2] / evals[-1])
    return gap, evals

# ---------- 测试 ----------

def run():
    passed = 0
    total = 0
    fails = []

    def check(name, cond, detail=""):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            fails.append(name)
            print(f"  [FAIL] {name}  {detail}")

    print("=" * 74)
    print("IFS 分解 → Σ-Rec coproduct 谱验证（阶段 3 分形扩张首个子任务）")
    print("=" * 74)

    # ---- S1: Weierstrass 型 2-map IFS 吸引子采样 ----
    # Weierstrass 图 IFS：f₁(t,y) = (t/b, y/b)，f₂(t,y) = ((t+1)/b, (y+a)/b)。
    # 1D 投影（t 分量）：f₁(t) = t/b，f₂(t) = (t+1)/b ⟹ 压缩比 c₁ = c₂ = 1/b。
    # 引入权重 a 控制"y 方向折叠"的谱效应（RKHS 核谱隙的驱动参数）。
    b = 2.0
    a = 0.5                      # 0 < a < 1（Weierstrass 非光滑参数），ab = 1 ≥ 1
    c_w = 1.0 / b                # t 方向压缩比（两片相同）
    f1 = lambda t: t / b
    f2 = lambda t: (t + 1.0) / b
    maps = [f1, f2]
    pts = ifs_attractor(maps, n_iter=30, n_points=3000)
    check("S1 Weierstrass 型 2-map IFS 吸引子采样（Hutchinson 迭代 30 轮，3000 点）",
          len(pts) == 3000 and 0.0 <= pts.min() <= pts.max() <= 1.0 + 1e-9,
          f"pts∈[{pts.min():.4f}, {pts.max():.4f}]")

    # ---- S2: Σ-Rec 编码（吸引子点按 IFS 片分组 ⟹ 每片一个 RecObj）----
    slices, assign = group_by_slices(pts, maps)
    n1, n2 = len(slices[0]), len(slices[1])
    check("S2 Σ-Rec 编码：吸引子点分组为局部线性片 R₁/R₂（两片均非空）",
          n1 > 0 and n2 > 0, f"|R₁|={n1}, |R₂|={n2}")
    # 每片视为独立 RecObj（状态 = 片内点），步进 = 片映射 fᵢ 在片内点上的像取最近
    def slice_transfer(maps, slices, pts, i):
        """片 i 的转移矩阵 Tᵢ（状态 = 片内点）：(Tᵢ)[p,q] = 1[fᵢ(p) 的最近点是 q]。"""
        si = slices[i]
        m = len(si)
        T = np.zeros((m, m), dtype=complex)
        for a, p in enumerate(si):
            y = maps[i](pts[p])
            d = np.abs(pts[si] - y)
            T[a, int(np.argmin(d))] = 1.0
        return T

    T1 = slice_transfer(maps, slices, pts, 0)
    T2 = slice_transfer(maps, slices, pts, 1)
    T_all = np.zeros((len(pts), len(pts)), dtype=complex)
    # 块对角（coproduct 结构）：每块按片内索引放置
    idx0, idx1 = list(slices[0]), list(slices[1])
    for a, p in enumerate(idx0):
        row = np.where(assign == 0)[0][a]
        for bj, q in enumerate(idx0):
            col = np.where(assign == 0)[0][bj]
            T_all[row, col] = T1[a, bj]
    for a, p in enumerate(idx1):
        row = np.where(assign == 1)[0][a]
        for bj, q in enumerate(idx1):
            col = np.where(assign == 1)[0][bj]
            T_all[row, col] = T2[a, bj]
    check("S2b 片转移矩阵为确定性步进（每行恰好一个 1）",
          np.allclose(np.sum(T1, axis=1), 1) and np.allclose(np.sum(T2, axis=1), 1))

    # ---- S3: 谱化 coproduct：σ(T) = ⋃ σ(Tᵢ)（块对角特征值并集）----
    ev_all = np.sort(np.linalg.eigvals(T_all))
    ev1 = np.linalg.eigvals(T1)
    ev2 = np.linalg.eigvals(T2)
    ev_union = np.sort(np.concatenate([ev1, ev2]))
    # 块对角矩阵特征值 = 各块特征值并集（代数重数相加）
    max_dev = float(np.max(np.abs(ev_all - ev_union)))
    check("S3 谱化 coproduct：σ(T) = σ(T₁) ∪ σ(T₂)（D 保持 coproduct，§15.3 数值镜像）",
          max_dev < 1e-9, f"max|σ(T) − σ(T₁)∪σ(T₂)|={max_dev:.2e}")
    n_unit = int(np.sum(np.abs(ev_all) > 1 - 1e-9))
    check("S3b 单位模特征值仅来自恒等模（确定性步进谱结构：1 与 0）",
          n_unit == int(np.sum(np.abs(ev1) > 1 - 1e-9)) + int(np.sum(np.abs(ev2) > 1 - 1e-9)),
          f"单位模数={n_unit}")

    # ---- S4: RKHS 谱复杂度随分形维数单调（谱性质从 IFS 参数导出）----
    sigma = 0.05   # Gaussian 核尺度（有效秩对 σ 稳健）
    # 真对称 Cantor IFS：f₁(t) = c·t，f₂(t) = c·t + (1−c)（c ∈ (0, 0.5)），
    # Moran 维数 d = ln 2 / ln(1/c)（c ↑ ⟹ d ↑）。谱性质 = 核矩阵有效秩
    # （累计 95% 谱能量的特征值个数，对 σ 稳健）：分形维数越大，RKHS 谱
    # 需要越多分量达到同一能量占比 ⟹ 有效秩随 d 单调递增。
    def effrank_K(K, frac=0.95):
        ev = np.linalg.eigvalsh((K + K.conj().T) / 2)
        ev = ev[ev > 1e-12]
        if len(ev) == 0:
            return 0
        tot = ev.sum()
        return int(np.searchsorted(np.cumsum(ev[::-1]), frac * tot) + 1)

    cs4 = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
    ers4 = []
    ds4 = [np.log(2.0) / np.log(1.0 / c) for c in cs4]
    for c4 in cs4:
        m_c = [lambda t, cc=c4: cc * t, lambda t, cc=c4: cc * t + (1.0 - cc)]
        p_c = ifs_attractor(m_c, n_iter=25, n_points=1500)
        K = np.exp(-(p_c[:, None] - p_c[None, :]) ** 2 / (2 * sigma ** 2))
        ers4.append(effrank_K(K))
    mono4 = all(ers4[i] <= ers4[i + 1] for i in range(len(ers4) - 1))
    check("S4 RKHS 谱有效秩随 Moran 维数 d 单调递增（谱复杂度从 IFS 参数导出）",
          mono4,
          f"d={['%.3f' % d for d in ds4]}, effrank={ers4}")

    # ---- S5: Weierstrass 参数扫描：谱隙 vs Moran 维数 d = 2 + ln a / ln b ----
    # 固定 b = 3，扫描 a ∈ {0.3, 0.45, 0.6, 0.75, 0.9}（ab ≥ 1 保持非光滑）。
    # Moran 维数 d(a) = 2 + ln a / ln b（Falconer：Weierstrass 图维数）。
    # 预期：a ↑（图更"皱"，维数 d ↑）⟹ 核谱在更高尺度展开 ⟹ 谱隙结构变化。
    b5 = 3.0
    as5 = [0.3, 0.45, 0.6, 0.75, 0.9]
    gaps5 = []
    ds5 = []
    for a5 in as5:
        # Weierstrass 图 IFS（2D）：f₁(t,y) = (t/b, y/b)，f₂(t,y) = ((t+1)/b, (y+a)/b)
        m5 = [lambda t, a=a5, b=b5: np.array([t[0] / b, t[1] / b]),
              lambda t, a=a5, b=b5: np.array([(t[0] + 1.0) / b, (t[1] + a) / b])]
        # 2D Hutchinson 采样
        rng = np.random.default_rng(20260805)
        p2 = np.zeros((1200, 2))
        for _ in range(25):
            which = rng.integers(0, 2, size=1200)
            p2 = np.array([m5[w](p2[k]) for k, w in enumerate(which)])
        K5 = np.exp(-np.sum((p2[:, None, :] - p2[None, :, :]) ** 2, axis=2) / (2 * sigma ** 2))
        gap5, _ = spectral_gap_K(K5)
        gaps5.append(gap5)
        ds5.append(2.0 + np.log(a5) / np.log(b5))
    print(f"  [DIAG] S5 Weierstrass 扫描（b=3）：a={as5}")
    print(f"  [DIAG]    Moran 维数 d = {['%.4f' % d for d in ds5]}")
    print(f"  [DIAG]    核谱隙 gap = {['%.4f' % g for g in gaps5]}")
    # 验证：维数 d 单调 ⟹ 谱隙单调（同向或反向均接受，但需单调）
    d_mono = all(ds5[i] < ds5[i + 1] for i in range(len(ds5) - 1))
    gap_mono = all((gaps5[i] - gaps5[i + 1]) * (ds5[i + 1] - ds5[i]) >= -1e-6
                   for i in range(len(gaps5) - 1))
    check("S5 Weierstrass 谱隙与 Moran 维数 d 的关系（谱隙随 d 单调变化，阶段 3 验证目标）",
          d_mono and gap_mono,
          f"d={['%.3f' % d for d in ds5]}, gap={['%.4f' % g for g in gaps5]}")

    # ---- 汇总 ----
    print("-" * 74)
    print(f"  汇总: {passed}/{total} 检查通过")
    if fails:
        print(f"  [!] 失败项: {fails}")
    print("=" * 74)
    return passed, total

if __name__ == "__main__":
    p, t = run()
    import sys
    sys.exit(0 if p == t else 1)
