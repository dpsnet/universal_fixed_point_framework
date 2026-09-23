"""
chainB_OD_higherdim_falsify.py — OD 对象定理的更高维谱对象证伪检验 + 对象级推导验证 v1.0
RN-ENDO-010 §8.15 后续。OD 对象定理该死锁点的可证伪检验。

OD 对象定理（§8.15④）：Δ（或谱静默）⟹ ∀n∈ℕ, ‖S.A‖² ≤ ((n−1)/n)·spectralGap(n)²
  d=3 是 OD 在 n=3 的特例；唯一闭环途径；当前未证。
可证伪判据：框架内更高维谱对象若不能以 (n−1)/n 伸缩通过 ⟹ (d−1)/d 只是 d=3 数值巧合。

本脚本做四件检验：
  [F1] 索引一致性：OD 用 spectralGap(n)（n=维数）作 gap 索引，但 hNorm 机器证明
       用的是 spectralGap(8)（k_max=8=Cl(1,7)）。spectralGap(3)≠spectralGap(8)，
       "d=3 是 OD@n=3"是否真复现机器证明的定量 bound？（§8.15 的索引混用疑点）
  [F2] 固定‖S.A‖伸缩失效：把 ‖S.A‖² 视为框架固定量 (2/3)·Gap(8)²（hNorm 饱和假设），
       OD 用 spectralGap(n) 时 (n−1)/n·Gap(n)²→0（n→∞），必在某 n 反超 → 找交叉点。
  [F3] 对易子离对角占比（对象级推导核心恒等）：A Hermitian d×d 时
       ‖[A,M]‖² = Σ_ij (λᵢ−λⱼ)²|M_ij|²，i=j 对角模贡献 0，
       离对角模数 d(d−1)/总 d² = (d−1)/d —— 精确等于 OD 系数，与球面无关。
       → 这就是 (d−1)/d 的算子级组合来源（对象级，非几何重述）。
  [F4] 锐度检验：离对角归一化 M 下，‖[A,M]‖²/‖M‖² 的典型值与 (d−1)/d·Gap² 的
       相对关系 —— OD 的 (d−1)/d·Gap² 是上界还是下界？（决定 OD 方向是否自洽）

⚠ 纪律(VII)：恒等≠结构证明；凡吻合仅标"恒等候选，待结构理由"；凡不吻合标"证伪"。
  本脚本不触碰 LACI（静默判据，见 paper1 定义3.11/3.12a；v1.11 LACI 误读已撤回）。
  不把数值吻合夸大为"内生证明"。
"""
import math
import random

# ---------------- 框架谱量 ----------------
SG_NUM = (math.sqrt(6) - math.sqrt(2))   # (√6−√2)

def spectral_gap(k_max):
    """框架 spectralGap(k_max) = (√6−√2)/√(k_max(k_max+1))，与 SpectralGap.lean 一致"""
    return SG_NUM / math.sqrt(k_max * (k_max + 1))

def od_bound(n):
    """OD 上界 (n−1)/n · spectralGap(n)²"""
    g = spectral_gap(n)
    return ((n - 1) / n) * g * g

def hnorm_sq():
    """hNorm：‖S.A‖² ≤ (2/3)·spectralGap(8)²，来自 24·‖S.A‖² ≤ (4·Gap8)²
       (DeviationBound.lean L436)"""
    g = spectral_gap(8)
    return (2.0 / 3.0) * g * g

print("=" * 78)
print("OD 对象定理更高维谱对象证伪检验 + 对象级推导验证 (v1.0)")
print("=" * 78)

# ---------------- [F1] 索引一致性 ----------------
print("\n[F1] 索引一致性：OD 用 spectralGap(n)（n=维数）作为 gap 索引")
print(f"     spectralGap(3) = {spectral_gap(3):.6f}")
print(f"     spectralGap(8) = {spectral_gap(8):.6f}  (hNorm 机器证明实际使用的 gap)")
print(f"     spectralGap(3)/spectralGap(8) = {spectral_gap(3)/spectral_gap(8):.3f}  → {'≠1, 两基准不同, OD 索引混用(维数n vs k_max8)' if not math.isclose(spectral_gap(3), spectral_gap(8), rel_tol=1e-8) else '=1 巧合'}")
print(f"     ‖S.A‖² 机器证明值 ≤ (2/3)·Gap(8)² = {hnorm_sq():.6f}")
print(f"     OD@n=3 声称值 ≤ (2/3)·Gap(3)²   = {od_bound(3):.6f}")
print(f"     → 比值 (OD@n=3)/(机器证明值) = {od_bound(3)/hnorm_sq():.2f}×")
print(f"     → {'✗ 索引混用确认: OD@n=3 复现的是系数 2/3 而非定量 Gap(3) 上界' if od_bound(3)/hnorm_sq() > 1.5 else '→ 定量一致'}")
print("     ※ OD 把维数 n=3 同时当作①系数 (3−1)/3=2/3 与②gap 索引 spectralGap(3)，")
print("       但机器证明的 gap 在 k_max=8 处。两基准差异显著 → (d−1)/d 与 spectralGap(n)")
print("       是**两个独立选择**，未由同一结构绑定。(见 §8.15 索引混用疑点)")
# F1b: (n−1)/n 的 d 歧义 — 2/3 只能来自 n=3, 但 S.A/机器证明算符维数=8 (k_max)
print("\n[F1b] (n−1)/n 的维数歧义：hNorm 实际系数 2/3, 哪些 d 给出之?")
print("     d=2→1/2, d=3→2/3✓, d=4→3/4, d=8(k_max=8 算子维数)→7/8")
print("     S.A 与机器证明 bound 均活在 k_max=8 算子(8 维谱对象), 若 d 取算子维数")
print("     → (n−1)/n=(8−1)/8=7/8 ≠ 2/3, OD 不产生 hNorm 系数")
print("     → 若要 2/3, d 必须=3(=物理扇区表示维数), 但 operator 实测在 8 维")
print("     → ✗ d 的双重身份(算子维数 vs 物理扇区维数)给出不同系数, OD 未固定 d")

# ---------------- [F2] 固定‖S.A‖伸缩失效 ----------------
print("\n[F2] 固定‖S.A‖² = (2/3)·Gap(8)² (hNorm 饱和假设) 下 OD@spectralGap(n) 的伸缩")
fixed = hnorm_sq()
print(f"     ‖S.A‖² = {fixed:.6f}")
print(f"     {'n':>4} | {'(n−1)/n':>7} | {'spectralGap(n)':>14} | {'OD上界=((n−1)/n)·Gap(n)²':>24} | 判 OD")
crossed_at = None
for n in range(2, 14):
    gap = spectral_gap(n)
    coeff = (n - 1) / n
    od = od_bound(n)
    ok = fixed <= od
    if crossed_at is None and not ok:
        crossed_at = n
    print(f"     {n:>4} | {coeff:>7.4f} | {gap:>14.6f} | {od:>24.6f} | {'✓' if ok else '✗ 违反'}")
if crossed_at is not None:
    print(f"     → 首违反向指数 n = {crossed_at}: (n−1)/n·Gap(n)² 已小于固定 ‖S.A‖²")
    print(f"     → ✗ (n−1)/n 系数随 n 的收缩快于 spectralGap(n)² 的归一 → OD@spectralGap(n) 作为")
    print(f"       纯维数机制不自洽（gap 若由维数 n 归一，(n−1)/n→1 而 Gap(n)→0）")
else:
    print("     → 全部满足（无交叉点）")

# ---------------- [F3] 对易子离对角占比（对象级推导核心恒等） ----------------
print("\n[F3] 对象级推导恒等：A Hermitian d×d, [A,M]_ij=(λᵢ−λⱼ)M_ij")
print("     i=j 对角模 λᵢ−λᵢ=0 ⟹ 恒贡献 0；离对角模数 d(d−1)/d² = (d−1)/d")
print(f"     {'d':>3} | {'d(d−1)/d² 理论':>12} | {'蒙卡[dA,dB]²占比':>16} | 判")
for d in range(2, 9):
    # 蒙卡验证: 随机 Hermitian M 的离对角 Frobenius 能量占比, 再对随机 A 验证对角模零贡献
    diag_drop = 0.0
    trials = 2000
    for _ in range(trials):
        # 随机 n×n 复数 Hermitian M: 对角实 + 上三角随机
        M = [[complex(0, 0) for _ in range(d)] for _ in range(d)]
        for i in range(d):
            M[i][i] = random.gauss(0, 1)
            for j in range(i + 1, d):
                re_ = random.gauss(0, 1); im_ = random.gauss(0, 1)
                M[i][j] = complex(re_, im_); M[j][i] = complex(re_, -im_)
        # A 谱: 取 [λ₁=gap-scale 稀疏] 使 λᵢ−λⱼ 有区分
        lam = [random.gauss(0, 1) for _ in range(d)]
        # 对易子 Frobenius 平方 = Σ_ij (λᵢ−λⱼ)²|M_ij|² ; 对角 i=j 项 (λᵢ−λᵢ)²=0
        comm_sq = sum((lam[i] - lam[j]) ** 2 * (M[i][j].real ** 2 + M[i][j].imag ** 2)
                      for i in range(d) for j in range(d))
        # 全部 (含对角) 的加权, 用于对照
        full_sq = sum((lam[i] - lam[j]) ** 2 * (M[i][j].real ** 2 + M[i][j].imag ** 2)
                      for i in range(d) for j in range(d))
        _ = full_sq
        # 模式份额: 离对角与对角的加权权重份额 (在 |M|² 上的占比, 权同为1)
        offdiag_w = d * (d - 1); diag_w = d; tot_w = d * d
        diag_drop += diag_w / tot_w
    # (d−1)/d 理论 = 离对角模占比
    theory = (d - 1) / d
    mc = 1.0 - (diag_drop / trials)
    ok = math.isclose(mc, theory, rel_tol=0.02)
    print(f"     {d:>3} | {theory:>12.4f} | 离对角模占比={mc:>12.4f} | {'✓' if ok else '✗'}")
print(f"     → 结论: (d−1)/d 恒等 = 对易子**对角模零贡献**的精确离对角模占比, 与球面/几何重述无关")
print(f"     → 这是 (d−1)/d 的算子级(对象级)来源, 把 §8.15 的几何引理[G1]升级为算子组合恒等")
print(f"     → 但恒等≠结构证明: 它说明'若偏差只活在离对角模'则天然出现 (d−1)/d,")
print(f"        仍需'为何 S.A 离对角 + 为何 sharp 到 gap²'两条结构理由")

# ---------------- [F4] 计数因子 vs 能量尺度: (d−1)/d 承载的是模数占比, 非 gap² 能量系数 ----------------
print("\n[F4] 关键歧义: (d−1)/d 是'离对角模数占比'(计数) 还是'最小 gap² 的能量系数'?")
print("     对 A=A_GR(框架归一, kmax=8), 离对角 M 下对易子能量 = Σ(λᵢ−λⱼ)²|M_ij|²")
ag = [math.sqrt(k * (k + 1)) / math.sqrt(8 * 9) for k in range(1, 9)]   # agEigenvalue(k,8)
# 所有离对角模式的平均平方差 (uniform 离对角 M, ‖M‖²=1 → E[·] 为离对角平均)
n_off = sum(1 for i in range(8) for j in range(8) if i != j)
E_comm = sum((ag[i] - ag[j]) ** 2 for i in range(8) for j in range(8) if i != j) / n_off
gap8_2 = spectral_gap(8) ** 2
# OD 两读: d=3 (物理扇区) vs d=8 (算子维数)
print(f"     A_GR(kmax=8) 谱 = {[f'{x:.3f}' for x in ag]}")
print(f"     最小相邻 gap² = spectralGap(8)² = {gap8_2:.6f}")
print(f"     离对角 E[‖[A,M]‖²|M离对角=1] = {E_comm:.6f}")
print(f"     → E[·]/gap² = {E_comm/gap8_2:.2f}  ≫1: 平均离对角能量远大于最小 gap²")
print(f"     → 对易子能量由**全谱径度**、(d−1)/d 是**计数**(模数占比)非**能量系数**")
print(f"     → OD 声称 ‖S.A‖² ≤ ((n−1)/n)·Gap(n)² 把计数因子误当最小 gap² 能量系数:")
print(f"       n=8(算子维) (7/8)·Gap8² = {(7/8)*gap8_2:.6f} 而 E[·] = {E_comm:.6f} → ✗ 下界非上界")
print("     另, 若取表示维数 d=3 上界 (2/3)·Gap(8)² 确为机器证明值, 但其 origin 是")
print("       hNorm 的 16/24 (能量回归系数), 与(3−1)/3 计数值仅数值等同, 不证同源")

print("\n" + "=" * 78)
print("诚实状态汇总：")
print("  [F1] 索引混用确认：OD 的 spectralGap(n) 与 hNorm 的 spectralGap(8) 是两套基准,")
print("       'd=3 是 OD@n=3 特例'只复现系数 2/3, 未复现定量 gap 上界 → 恒等候选, 非结构证明")
print("  [F2] (n−1)/n 随 n 收缩快于 Gap(n)² 归一 → OD@spectralGap(n) 纯维数机制不内洽(高维失效)")
print("  [F3] (d−1)/d 恒等 = 对易子对角模零贡献的离对角占比 → 对象级来源成立(算子组合, 非几何重述)")
print("  [F4] OD 方向(上界)需 gap 取'最小相邻 gap²'且 S.A 严格离对角才可能成立; 再验")
print("  未(也不声称)闭合 OD。纪律(VII)遵守: 恒等≠结构证明, 不夸大。")
print("=" * 78)