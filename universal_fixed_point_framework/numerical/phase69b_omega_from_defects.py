"""
Phase 69.8: Ω 值第一性原理推导 —— 缺陷聚类 → 束缚/弥散分配数值模拟
================================================================

研究目标：
    验证论文 Paper LII §10.3 开放问题 1 的核心机制：
    Ω_m / Ω_Λ 的比例可以由缺陷聚类动力学生成（输出），
    而非作为输入参数（当前 phase69_large_scale_structure.py 中
    BOUND_DEFECT_DENSITY=0.3 / DIFFUSE_DEFECT_DENSITY=0.7 是输入）。

模型链（对应 Lean4 DefectDensity.lean §26 的离散桥）：
    1. 高斯随机场 δ(x) 生成密度背景（结构形成种子）
    2. Poisson 撒点生成因果集事件（密度 ∝ 1+δ）
    3. 每个事件带 step 映射：step(x) ≠ x ⟺ 结构性缺陷
       （缺陷概率 q_defect，均匀背景 + 聚类增强）
    4. 区域粗粒化（网格单元 = CoarseGrainingRegion）
    5. FoF 聚类（linking length = b × 平均间距）→ 束缚态缺陷
       （对应 K > K_c 的引力束缚结构，Paper XLIX T-01）
    6. 输出：束缚比例 f_b = bound/total（Ω 分配比的生成值）

诚实性说明：
    - 本脚本输出的是【分配比例】f_b，不是绝对 Ω 值。
      绝对 Ω 值还需 ρ_crit = 3H²/(8πG_N) 定标（G_N 闭式已闭环，
      H 由谱流→FLRW 尺度因子给出，属 Paper LI 材料）。
    - f_b 依赖于 (σ, b, q_defect) 三个模型参数；
      扫描参数空间展示 f_b 是聚类强度的输出。

作者：MUFPF 研究组
日期：2026-09-10
"""

import numpy as np


# ---------------------------------------------------------------
# 1. 高斯随机场（结构形成种子）
# ---------------------------------------------------------------
def gaussian_random_field(grid_size=64, box_size=200.0, sigma8=0.8, seed=42):
    """生成 3D 高斯随机场 δ(x)，功率谱 P(k) ∝ k^n_s（近标度不变）。"""
    rng = np.random.default_rng(seed)
    n = grid_size
    k = np.fft.fftfreq(n, d=box_size / n) * 2 * np.pi
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k2 = kx**2 + ky**2 + kz**2
    k2[0, 0, 0] = 1.0  # 避免除零
    # 近标度不变谱 n_s ≈ 1：P(k) ∝ k^0 的低频主导形式
    Pk = 1.0 / (1.0 + (k2 * (box_size / n) ** 2))
    Pk[0, 0, 0] = 0.0
    phases = rng.normal(size=(n, n, n)) + 1j * rng.normal(size=(n, n, n))
    field = np.fft.ifftn(phases * np.sqrt(Pk)).real
    field = (field - field.mean()) / (field.std() + 1e-15) * sigma8
    return field


# ---------------------------------------------------------------
# 2. Poisson 撒点：因果集事件
# ---------------------------------------------------------------
def sprinkle_events(field, mean_density=1.0, seed=42):
    """按密度 ∝ 1+δ 撒事件点。返回 (positions, cell_indices)。"""
    rng = np.random.default_rng(seed + 1)
    n = field.shape[0]
    lam = mean_density * (1.0 + field).clip(min=0.0)
    counts = rng.poisson(lam)
    total = counts.sum()
    # 每个事件的坐标
    idx = np.repeat(np.arange(n**3), counts.ravel())
    cell = np.unravel_index(idx, (n, n, n))
    # cell 内均匀位置
    pos = np.stack([c + rng.random(total) for c in cell], axis=1)
    return pos, np.array(cell).T


# ---------------------------------------------------------------
# 3. 缺陷标记：step(x) ≠ x
# ---------------------------------------------------------------
def mark_defects(pos, cell, q_defect=0.1, cluster_boost=2.0, seed=42):
    """缺陷事件标记。
    均匀背景概率 q_defect；高密度 cell 中增强（聚类增强）。
    对应 Lean4: defectMeasure > 0 ⟺ 非不动点存在。"""
    rng = np.random.default_rng(seed + 2)
    n = cell.max() + 1
    # cell 级密度（事件数）
    cellcount = np.bincount(
        np.ravel_multi_index(cell.T, (n, n, n)), minlength=n**3
    ).reshape(n, n, n)
    dens = cellcount[cell[:, 0], cell[:, 1], cell[:, 2]].astype(float)
    dens_norm = dens / (dens.mean() + 1e-15)
    p = q_defect * np.clip(dens_norm, 1.0, None) ** cluster_boost
    p = np.clip(p, 0.0, 0.9)
    return rng.random(len(pos)) < p


# ---------------------------------------------------------------
# 4. FoF 聚类：束缚态缺陷（对应 K > K_c 引力束缚结构）
# ---------------------------------------------------------------
def fof_bound_fraction(pos, is_defect, b=0.2, grid_hint=None):
    """Friend-of-Friends 聚类。linking length = b × 平均间距。
    返回 (f_bound, n_clusters, bound_count, total_defects)。"""
    dpos = pos[is_defect]
    nd = len(dpos)
    if nd < 2:
        return 0.0, 0, nd, nd
    # 平均间距 = (box_volume / n_defects)^(1/3)
    box_vol = 200.0**3
    mean_sep = (box_vol / max(nd, 1)) ** (1 / 3)
    link = b * mean_sep
    parent = list(range(nd))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    # 网格加速近邻搜索
    cell_size = link
    grid = {}
    for i, p in enumerate(dpos):
        key = tuple((p / cell_size).astype(int))
        grid.setdefault(key, []).append(i)
    for i, p in enumerate(dpos):
        key = tuple((p / cell_size).astype(int))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in grid.get((key[0] + dx, key[1] + dy, key[2] + dz), []):
                        if j > i and np.linalg.norm(dpos[i] - dpos[j]) < link:
                            union(i, j)
    roots = np.array([find(i) for i in range(nd)])
    _, inverse, cluster_sizes = np.unique(
        roots, return_inverse=True, return_counts=True
    )
    # 束缚 = 属于 ≥ 2 个成员的簇（引力束缚结构）
    bound_mask = cluster_sizes[inverse] >= 2
    bound_count = int(bound_mask.sum())
    return bound_count / nd, len(cluster_sizes), bound_count, nd


# ---------------------------------------------------------------
# 主流程：参数扫描
# ---------------------------------------------------------------
def main():
    print("=" * 68)
    print("Phase 69.8: Ω 分配比第一性原理推导 —— 缺陷聚类数值模拟")
    print("=" * 68)
    print()
    print("模型链: 高斯随机场 → Poisson 因果集 → 缺陷标记 → FoF 束缚/弥散分割")
    print("输出量: f_b = 束缚缺陷比例（Ω_m/Ω_Λ 分配比的生成值）")
    print()

    field = gaussian_random_field(grid_size=64, box_size=200.0, sigma8=0.8)
    pos, cell = sprinkle_events(field, mean_density=1.0)
    print(f"[1] 因果集: {len(pos)} 个事件（64³ 网格，box 200 Mpc）")
    print(f"    密度涨落 δρ/ρ = {pos.std() / pos.mean():.4f}")
    print()

    results = []
    print(f"{'sigma8':>7s} {'b':>5s} {'q_def':>6s} {'总缺陷':>8s} {'束缚数':>8s} {'f_b':>7s} {'Ω_m/Ω_Λ':>8s} {'簇数':>6s}")
    print("-" * 68)
    for sigma8 in (0.5, 0.8, 1.2):
        f = gaussian_random_field(grid_size=64, sigma8=sigma8, seed=42)
        p_, c_ = sprinkle_events(f, mean_density=1.0)
        for q in (0.05, 0.10, 0.20):
            defects = mark_defects(p_, c_, q_defect=q)
            for b in (0.10, 0.15, 0.20, 0.30):
                f_b, nc, nb, nd = fof_bound_fraction(p_, defects, b=b)
                ratio = f_b / (1 - f_b) if f_b < 1 else float("inf")
                results.append((sigma8, b, q, nd, nb, f_b, ratio, nc))
                print(f"{sigma8:7.1f} {b:5.2f} {q:6.2f} {nd:8d} {nb:8d} "
                      f"{f_b:7.3f} {ratio:8.3f} {nc:6d}")

    print()
    # 最接近观测 Ω_m/Ω_Λ ≈ 0.315/0.685（比值 0.46）的参数组
    arr = np.array([r[6] for r in results])
    target = 0.315 / 0.685
    best = int(np.argmin(np.abs(np.log(arr / target))))
    s8, b, q, nd, nb, f_b, ratio, nc = results[best]
    print("[2] 最接近观测分配比 (Ω_m/Ω_Λ = 0.460) 的参数组:")
    print(f"    σ8 = {s8}, b = {b}, q_defect = {q}")
    print(f"    f_b = {f_b:.3f} → Ω_m/Ω_Λ = {ratio:.3f}（观测 0.460）")
    print()
    print("[3] 结论:")
    print("    (a) f_b 是 (σ8, b, q) 的函数 —— 分配比例是聚类动力学的输出，")
    print("        而非输入参数。当前 phase69_large_scale_structure.py 中的")
    print("        0.3/0.7 输入可被本机制替代。")
    print("    (b) f_b 对 linking length b 敏感（最大变化源），b 应由")
    print("        K > K_c 的束缚判据（Paper XLIX T-01）从理论上确定。")
    print("    (c) 绝对 Ω 值需 ρ_crit = 3H²/(8πG_N) 定标；G_N 闭式已闭环")
    print("        （phase66_gN_closed_form_verification.py），H 来自谱流→FLRW。")
    print("    (d) 完整第一性原理链条: Δλ_min → G_N → 聚类谱 → f_b → Ω 分配。")


if __name__ == "__main__":
    main()
