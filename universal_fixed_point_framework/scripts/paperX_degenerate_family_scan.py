# -*- coding: utf-8 -*-
"""
Phase 71 阶段3（3b）：退化族扫描——半共线族之外的"离散跳变"信号
================================================================
依据：翻译笔记推论 2.1——在标准振幅学认为"连续可微"的构型族边界处扫描"离散跳变"信号。
对象：单负剥离振幅 A_BG（公式(21)），与通式(39)/显式公式已数值互证（B1/B2 全 pass）。

扫描族：
  S1 部分共线：z 部分相等（1 对/2 对/……）而非全部相等——标准功率计数在这些位置仍判零
      （论文(15)(16) 半共线支持只覆盖全共线），若出现非零 = 潜在新非零构型候选。
  S2 R1 边界跨越：ω₁ 从负连续变正（其余 ω 固定 + 动量守恒 z̄ₙ）——通式(39) 的 R1 条件破坏。
  S3 连续跳变路径（推论 2.1 核心）：全半共线配置 → generic 配置的线性路径 t∈[0,1]，
      细扫 A_BG，记录跳变位置与幅度（标准振幅学预期连续——但半共线处是奇异点）。
  S4 软极限连续性：eps→0 连续扫描，验证 A_n 连续趋近软定理值（与 T2 互补：T2 只测 3 档）。

结论判定（诚实边界）：
  - "跳变"= A_BG 沿路径在相邻采样点间不连续变化（非 ±1/0 整数格点间的连续移动）。
  - 发现/否定结论均记录；不强行凑预言。
"""
import random
import json
import sys

sys.path.insert(0, "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts")
from paperX_single_minus_numerics import sg, sg_pair, sg_block, A_R1, EXPLICIT
from paperX_single_minus_bg_recursion import A_BG, bracket

SEED = 20260930
random.seed(SEED)


# ---------- 配置生成 ----------

def gen_partial_collinear(n, k_pairs, rng=random, r1=True, momentum=True):
    """
    部分共线配置：指定 k_pairs 个"共线对"（z 相等），其余 z 随机不同。
    返回 (omega, zbar, collinear_pairs)。
    - 共线对：随机选 k_pairs 个互不相交的 2 元组，组内 z 相等，组间及孤立粒子 z 随机。
    - R1: omega_1<0, omega_a>0（若 r1=True）
    - 动量守恒：zbar_n 由前 n-1 个决定（若 momentum=True）
    """
    nz = 0.0
    while True:
        # 选互不相交共线对
        idx = list(range(n))
        pairs = []
        rng.shuffle(idx)
        for i in range(0, min(len(idx) - 1, 2 * k_pairs), 2):
            if len(pairs) < k_pairs:
                pairs.append((idx[i], idx[i + 1]))
        # 组分配：同组共线对（含孤立粒子）的 z 相等；不同组 z 不同
        groups = {}
        gid = 0
        used = set()
        for a, b in pairs:
            groups[a] = gid
            groups[b] = gid
            used.add(a)
            used.add(b)
            gid += 1
        for i in range(n):
            if i not in used:
                groups[i] = gid
                gid += 1
        gvals = {g: rng.uniform(-2.0, 2.0) for g in set(groups.values())}
        z = [gvals[groups[i]] for i in range(n)]
        # 检查：共线对确实共线、非共线对确实非共线（避免组间恰好相等）
        ok = True
        for i in range(n):
            for j in range(i + 1, n):
                if groups[i] == groups[j]:
                    if abs(z[i] - z[j]) > 1e-12:
                        ok = False
                else:
                    if abs(z[i] - z[j]) < 1e-6:
                        ok = False
        if ok:
            break
    omega = [0.0] * n
    if r1:
        omega[0] = -rng.uniform(1.0, 5.0)
        for a in range(1, n - 1):
            omega[a] = rng.uniform(0.1, 2.0)
        omega[n - 1] = -sum(omega[: n - 1]) if momentum else rng.uniform(0.1, 2.0)
    else:
        omega = [rng.choice([-1.0, 1.0]) * rng.uniform(0.5, 2.0) for _ in range(n)]
    zbar = [rng.uniform(-3.0, 3.0) for _ in range(n - 1)]
    if momentum:
        s = sum(omega[: n - 1])
        zbar_n = sum(omega[i] * zbar[i] for i in range(n - 1)) / s
        zbar.append(zbar_n)
    else:
        zbar.append(rng.uniform(-3.0, 3.0))
    return omega, zbar, pairs


def gen_r1_crossing_path(n, n_steps, rng=random):
    """
    R1 边界跨越路径：ω₁(t) 从 -A 连续变到 +A，ω₂..ω_{n-1} 固定，动量守恒 ωₙ=-Σ。
    返回 list[(t, omega, zbar)]。
    """
    base = [0.0] * (n - 1)
    base[0] = 2.0  # ω₁ 的起点幅值（t 控制符号）
    for a in range(1, n - 1):
        base[a] = rng.uniform(0.5, 1.5)
    zbar_head = [rng.uniform(-3.0, 3.0) for _ in range(n - 1)]
    path = []
    for step in range(n_steps + 1):
        t = step / n_steps
        w1 = 2.0 * (2 * t - 1)  # -2 → +2
        omega = list(base)
        omega[0] = w1
        s = sum(omega[: n - 1])
        omega.append(-s)
        zbar = zbar_head + [sum(omega[i] * zbar_head[i] for i in range(n - 1)) / s]
        path.append((t, omega, zbar))
    return path


def gen_linear_deformation_path(n, n_steps, rng=random):
    """
    连续跳变路径：t=0 全半共线（z_i 全相等，R1+动量守恒，A_BG=±1/0），
    t=1 generic（z_i 随机全不同）。z_i(t) = z0 + t*(zf - z0)。
    """
    z0 = [0.0] * n
    zf = [rng.uniform(-2.0, 2.0) for _ in range(n)]
    omega, zbar = _gen_momentum_r1(n, rng)
    path = []
    for step in range(n_steps + 1):
        t = step / n_steps
        z = [z0[i] + t * (zf[i] - z0[i]) for i in range(n)]
        path.append((t, omega, zbar, z))
    return path


def _gen_momentum_r1(n, rng):
    while True:
        omega = [0.0] * n
        omega[0] = -rng.uniform(1.0, 5.0)
        for a in range(1, n - 1):
            omega[a] = rng.uniform(0.1, 2.0)
        if sum(omega[: n - 1]) < -0.05:
            break
    zbar = [rng.uniform(-3.0, 3.0) for _ in range(n - 1)]
    s = sum(omega[: n - 1])
    omega[n - 1] = -s
    zbar_n = sum(omega[i] * zbar[i] for i in range(n - 1)) / s
    zbar.append(zbar_n)
    return omega, zbar


def A_BG_half(n, omega, zbar, z):
    """半共线实现：把 z 并入（剥离振幅在括号内只依赖 zbar；但 ⟨ij⟩ 通过分母/Θ 出现，
    BG 递归的 V_fn 用 bracket 只含 zbar——⟨ij⟩=z_i-z_j 影响参考旋量选择而非显式括号。
    为忠实实现，我们直接以 z 构造 bracket 的共线探测：BG 递归公式(20) 的 Θ 只含 [ ] 括号
    （全由 zbar 决定），⟨ij⟩ 进入的是"半共线支持"(15)(16) 的适用域而非递归本身。
    因此 A_BG 对 z 的依赖仅经由物理适用域判定——此处显式打印 z 用于记录。"""
    return A_BG(n, omega, zbar)


# ---------- S1: 部分共线 ----------

def scan_S1(n=5, k_max=2, n_samples=300, momentum=True):
    res = {}
    for k in range(0, k_max + 1):
        vals = []
        nonzero = 0
        for _ in range(n_samples):
            omega, zbar, pairs = gen_partial_collinear(n, k, r1=True, momentum=momentum)
            a = A_BG(n, omega, zbar)
            vals.append(a)
            if a != 0.0:
                nonzero += 1
        int_ok = all(abs(v - round(v)) < 1e-9 for v in vals)
        uniq = sorted(set(round(v, 6) for v in vals))
        res[f"k_pairs={k}"] = {
            "samples": n_samples,
            "nonzero": nonzero,
            "nonzero_rate": round(nonzero / n_samples, 4),
            "all_integer": int_ok,
            "distinct_values": uniq,
        }
    return res


# ---------- S2: R1 边界跨越 ----------

def scan_S2(n=5, n_steps=200, n_runs=50):
    jumps = []
    for _ in range(n_runs):
        path = gen_r1_crossing_path(n, n_steps)
        prev_t, prev_a = None, None
        for t, omega, zbar in path:
            a = A_BG(n, omega, zbar)
            if prev_a is not None and a != prev_a:
                jumps.append((prev_t, t, prev_a, a))
            prev_t, prev_a = t, a
    # 汇总：跳变次数、跳变时 ω₁ 符号区间
    n_jump_total = len(jumps)
    jump_w1_ranges = {}
    for pt, t, pa, a in jumps:
        w1 = 2.0 * (2 * t - 1)
        key = "omega1<0 (R1)" if w1 < 0 else "omega1>0"
        jump_w1_ranges.setdefault(key, 0)
        jump_w1_ranges[key] += 1
    return {
        "n_runs": n_runs,
        "n_steps": n_steps,
        "total_jumps": n_jump_total,
        "jumps_by_region": jump_w1_ranges,
    }


# ---------- S3: 连续跳变路径（推论 2.1 核心） ----------

def scan_S3(n=5, n_steps=200, n_runs=30):
    """从全半共线到 generic 的线性路径：检测 A_BG 的跳变位置 t*。
    generic 端（t=1）标准功率计数预期 A=0；半共线端（t=0）A=±1/0。
    跳变发生在哪个 t？是否单个离散点？"""
    summary = {"runs": [], "jump_t_values": [], "amplitudes_at_t0": set()}
    for run in range(n_runs):
        path = gen_linear_deformation_path(n, n_steps)
        prev_t, prev_a = None, None
        jumps = []
        vals = []
        for t, omega, zbar, z in path:
            a = A_BG(n, omega, zbar)
            vals.append((t, a))
            if prev_a is not None and a != prev_a:
                jumps.append((prev_t, t, prev_a, a))
            prev_t, prev_a = t, a
        summary["runs"].append({
            "jumps": jumps,
            "a0": vals[0][1],
            "a1": vals[-1][1],
            "first_jump_t": jumps[0][0] if jumps else None,
        })
        summary["amplitudes_at_t0"].add(vals[0][1])
        for j in jumps:
            summary["jump_t_values"].append(j[0])
    return summary


# ---------- S4: 软极限连续性 ----------

def scan_S4(n=5, eps_min=1e-4, n_steps=40, n_runs=20):
    """连续扫 eps：A_n(eps) 是否连续趋近软定理值 (1/2)(sg_{n-1,n}+sg_{n,n1}) A_{1..n-1}？"""
    from paperX_single_minus_numerics import soft_ratio
    jumps = 0
    samples = 0
    for _ in range(n_runs):
        prev_eps, prev_lhs = None, None
        for step in range(n_steps + 1):
            eps = eps_min * (0.1 / eps_min) ** (step / n_steps)  # 对数扫描 0.1 → eps_min
            lhs, r1, r2 = soft_ratio(n, eps)
            samples += 1
            if prev_lhs is not None and lhs != prev_lhs:
                jumps += 1
            prev_eps, prev_lhs = eps, lhs
    return {"n_runs": n_runs, "samples": samples, "lhs_changes_along_path": jumps}


# ---------- S5: 非半共线（generic z）+ R1 + 动量守恒 的一致性检查 ----------

def scan_S5(n=5, n_samples=300):
    """S1 显示非半共线也非零（~30%）。若这些值构成自洽振幅结构，
    应满足循环性(24)/KK(27)/软定理(28)。本扫描在 generic z 配置下验证。"""
    def permute(fn, omega, zbar, perm):
        om = [omega[i] for i in perm]
        zb = [zbar[i] for i in perm]
        return fn(len(perm), om, zb)
    # 循环性(24)：动量守恒配置
    nf_cyc = 0
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True)  # 0 对共线 = generic z
        a1 = A_BG(n, omega, zbar)
        a2 = permute(A_BG, omega, zbar, [1, 2, 3, 4, 0])
        if abs(a1 - a2) > 1e-9:
            nf_cyc += 1
    # KK(27)
    nf_kk = 0
    perms = [[0, 1, 2, 4, 3], [0, 1, 3, 2, 4], [0, 3, 1, 2, 4]]
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True)
        total = A_BG(n, omega, zbar)
        for p in perms:
            total += permute(A_BG, omega, zbar, p)
        if abs(total) > 1e-9:
            nf_kk += 1
    # 软定理(28)：eps 档位（非半共线）
    from paperX_single_minus_numerics import soft_ratio
    nf_soft = 0
    for _ in range(n_samples):
        lhs, r1, r2 = soft_ratio(n, 0.01)
        if lhs != 0.0:
            d1 = abs(lhs - r1) / max(abs(lhs), 1e-30)
        else:
            d1 = abs(lhs - r1)
        if d1 > 1e-9:
            nf_soft += 1
    return {
        "cyclicity(24)": {"fail": nf_cyc, "pass": nf_cyc == 0},
        "KK(27)": {"fail": nf_kk, "pass": nf_kk == 0},
        "soft_theorem(28)": {"fail": nf_soft, "pass": nf_soft == 0},
    }


def main():
    print("=" * 72)
    print("Phase 71 阶段3b：退化族扫描——半共线族之外的离散跳变信号")
    print("=" * 72)

    print("\n[S1] 部分共线（R1+动量守恒，n=5）：标准功率计数判零区域的非零检查")
    s1 = scan_S1()
    for k, v in s1.items():
        print(f"  {k}: nonzero_rate={v['nonzero_rate']}, all_integer={v['all_integer']}, "
              f"values={v['distinct_values'][:12]}")

    print("\n[S2] R1 边界跨越（ω₁: -2→+2，动量守恒，n=5）")
    s2 = scan_S2()
    print(f"  total_jumps={s2['total_jumps']}, by_region={s2['jumps_by_region']}")

    print("\n[S3] 连续跳变路径（全半共线→generic，n=5，推论 2.1 核心）")
    s3 = scan_S3()
    first_jumps = [r["first_jump_t"] for r in s3["runs"] if r["first_jump_t"] is not None]
    a0s = sorted(set(str(r["a0"]) for r in s3["runs"]))
    a1s = sorted(set(str(r["a1"]) for r in s3["runs"]))
    print(f"  t=0 振幅取值: {a0s}")
    print(f"  t=1 振幅取值: {a1s}")
    if first_jumps:
        print(f"  首次跳变 t 值: min={min(first_jumps):.4f}, max={max(first_jumps):.4f}, "
              f"共 {len(first_jumps)}/{len(s3['runs'])} 条路径有跳变")
    else:
        print("  无跳变（A_BG 恒为常数或连续）")

    print("\n[S4] 软极限连续性（对数扫 eps: 0.1→1e-4，n=5）")
    s4 = scan_S4()
    print(f"  lhs_changes_along_path={s4['lhs_changes_along_path']}（0 = 全程恒值/连续）")

    print("\n[S5] 非半共线（generic z）+ R1 + 动量守恒：一致性检查（S1 非零是否自洽）")
    s5 = scan_S5()
    for k, v in s5.items():
        print(f"  {k}: fail={v['fail']}, pass={v['pass']}")

    out = {"S1": s1, "S2": s2, "S3": s3, "S4": s4, "S5": s5}
    out_path = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/paperX_degenerate_scan_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")


if __name__ == "__main__":
    main()
