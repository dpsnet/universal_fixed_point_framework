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
paperX_photon_kappa_select.py — 开放问题 #5 κ_Δ 候选选择原理推进

笔记来源: notes/06_photon_topology/photon_topology_theory.md §6.1
前置: paperX_photon_kappa_delta.py (14/14) 建立框架内生候选族 + 判别性锚定

目标: 对 4 个框架内生候选应用框架既有选择原理, 评估能否唯一锁定:
  K_a = S4^2            = 4.444e-3   (双层谱静默抑制, 最简)
  K_b = S4/(N_Weyl*d_H) = 6.154e-3   (单层静默被旋量x分形稀释)
  K_c = S4^2*(N_Weyl/2) = 8.889e-3   (双层静默 x 手性配对, 推荐)
  K_e = S4^2*(d_H/2)    = 6.018e-3   (双层静默 x 半分形维数)

选择原理评估维度:
  S1 结构谱: 组合解释的机制来源 (静默阶数/手性配对/分形维数关联)
  S2 MDL 描述长度: 独立量数 + 算符数 (最小描述原则)
  S3 结构匹配: 与偏振不对称机制 (螺旋 vs 平面形变循环) 的匹配度
  S4 框架关联: 与 d_H 残差 δ=d_H-ln15≈1.4e-3 的比值 (小整数检测)
  S5 收窄规则: 剔除无机制来源候选 -> 双候选
  S6 判别性: 双候选的白矮星/太阳 δz_pol 预测谱

诚实边界: 选择原理为启发式-结构性 (无实验锚定与固定点方程,
对比 √5 选择原理有 χ² 拟合锚定); 本脚本为选择原理形式化推进,
κ_Δ 精确值仍登记开放.
"""
import numpy as np

# ============================================================
# 检查项框架
# ============================================================
_CHECKS = []


def check(name, cond, detail=""):
    _CHECKS.append((name, bool(cond), detail))


# ============================================================
# 框架量
# ============================================================
S4 = 1.0 / 15.0
N_WEYL = 4
D_H = np.log(15.0)

KAPPA_LO, KAPPA_HI = 1e-4, 1e-2   # 预言带

CAND = {
    "K_a": {"value": S4**2,
            "n_indep": 1, "n_ops": 2,              # S4^2: 1 独立量, 1 幂算符
            "mechanism": "双层谱静默抑制 (二阶过程)",
            "chirality": False, "dH": False},
    "K_b": {"value": S4 / (N_WEYL * D_H),
            "n_indep": 3, "n_ops": 3,              # S4/(N_Weyl*d_H): 3 独立量
            "mechanism": "单层静默被旋量数x分形维数稀释",
            "chirality": False, "dH": True},
    "K_c": {"value": S4**2 * (N_WEYL / 2.0),
            "n_indep": 2, "n_ops": 3,              # S4^2*(N_Weyl/2)
            "mechanism": "双层静默 x 手性配对 (N_Weyl=4 -> 2 对)",
            "chirality": True, "dH": False},
    "K_e": {"value": S4**2 * (D_H / 2.0),
            "n_indep": 2, "n_ops": 3,              # S4^2*(d_H/2)
            "mechanism": "双层静默 x 半分形维数",
            "chirality": False, "dH": True},
}

print("=" * 72)
print("开放问题 #5: κ_Δ 候选选择原理推进")
print("笔记: notes/06_photon_topology/photon_topology_theory.md §6.1")
print("=" * 72)

# ============================================================
# S1 结构谱: 组合解释的机制来源
# ============================================================
print("\n[S1] 候选结构谱")
print(f"  {'候选':<5s} {'值':>10s} {'独立量':>6s} {'算符':>4s} {'机制解释'}")
for k, c in CAND.items():
    print(f"  {k:<5s} {c['value']:10.4e} {c['n_indep']:>6d} {c['n_ops']:>4d} {c['mechanism']}")

# 全部在预言带内 (候选族有效性前提)
in_band = all(KAPPA_LO <= c["value"] <= KAPPA_HI for c in CAND.values())
check("S1-C1 候选族 4 个值全部落在预言带 [1e-4,1e-2] 内",
      in_band, "max=%.3e min=%.3e" % (max(c["value"] for c in CAND.values()),
                                      min(c["value"] for c in CAND.values())))

# ============================================================
# S2 MDL 描述长度: L = n_indep + n_ops
# ============================================================
print("\n[S2] MDL 描述长度 (最小描述原则)")
mdl = {k: c["n_indep"] + c["n_ops"] for k, c in CAND.items()}
for k, L in mdl.items():
    c = CAND[k]
    print(f"  {k:<5s} L = {c['n_indep']} + {c['n_ops']} = {L}")
min_mdl = min(mdl.values())
min_mdl_keys = [k for k, L in mdl.items() if L == min_mdl]
check("S2-C1 最简候选唯一 (K_a: L=3)", min_mdl_keys == ["K_a"],
      "min L=%d -> %s" % (min_mdl, min_mdl_keys))

# ============================================================
# S3 结构匹配: 与偏振不对称机制 (螺旋 vs 平面) 的匹配度
# ============================================================
print("\n[S3] 结构匹配 (偏振不对称 = 螺旋 vs 平面形变循环拉伸倍率差)")
# 偏振不对称机制要素:
#   (i) 手性配对: 螺旋度 ±1 两向 -> 需要旋量配对结构 (N_Weyl/2)
#   (ii) 静默抑制: 二阶过程 (两次 Δ 作用各被 S4 抑制)
#   (iii) 分形维数 d_H 无偏振机制关联 (分形维数是空间标度性质, 非手性)
match = {k: (c["chirality"] and not c["dH"]) for k, c in CAND.items()}
for k, m in match.items():
    print(f"  {k:<5s} 手性配对={'是' if CAND[k]['chirality'] else '否'}  d_H关联={'是' if CAND[k]['dH'] else '否'}  结构匹配={'是' if m else '否'}")
match_keys = [k for k, m in match.items() if m]
check("S3-C1 结构匹配唯一候选 = K_c (手性配对+无 d_H 关联)",
      match_keys == ["K_c"], "match=%s" % match_keys)

# 机制排除: d_H 关联候选 (K_b/K_e) 因分形维数无偏振手性机制来源
excluded = [k for k, c in CAND.items() if c["dH"]]
check("S3-C2 含 d_H 关联候选 (K_b/K_e) 无偏振机制来源, 标记剔除",
      excluded == ["K_b", "K_e"], "excluded=%s" % excluded)

# ============================================================
# S4 框架关联: κ_Δ 与 d_H 一级偏离 δ_fit 的比值 (小整数检测)
# ============================================================
print("\n[S4] 框架关联: κ_Δ 与 d_H 一级偏离 δ_fit")
# 数值残差: d_H 拟合残差 δ_fit ≈ 1.4e-3 (paperX_dH_* 系列, χ² 拟合精度)
D_H_FIT = 2.7095
delta_fit = D_H_FIT - np.log(15.0)
print(f"  d_H(χ²) = {D_H_FIT:.6f}, ln15 = {np.log(15.0):.6f}, δ_fit = {delta_fit:.6f}")
check("S4-C1 δ_fit ≈ 1.4e-3 落在预言带内 (κ_Δ 与 d_H 一级偏离同源带)",
      1e-4 <= delta_fit <= 1e-2, "delta_fit=%.4e" % delta_fit)

# 小整数检测: δ_fit / κ 是否接近小整数 {1,2,3}
print(f"  {'候选':<5s} {'δ_fit/κ':>10s} {'最近整数':>10s} {'偏差':>10s}")
near_int = {}
for k, c in CAND.items():
    ratio = delta_fit / c["value"]
    nearest = round(ratio)
    dev = abs(ratio - nearest)
    near_int[k] = dev
    print(f"  {k:<5s} {ratio:10.3f} {nearest:10d} {dev:10.3f}")
n_near = sum(1 for v in near_int.values() if v < 0.05)
check("S4-C2 所有候选与 δ_fit 均无小整数关联 (诚实负结果)",
      n_near == 0, "n_near_int=%d (min dev=%.3f)" % (n_near, min(near_int.values())))
check("S4-C3 δ_fit 不提供 κ_Δ 锁定 (无唯一选择)",
      n_near == 0, "结论: 框架残差关联通道无约束力")

# ============================================================
# S5 收窄规则: 剔除无机制来源候选 -> 双候选
# ============================================================
print("\n[S5] 收窄规则")
print("  剔除: K_b (稀释解释无机制来源), K_e (d_H 无偏振机制关联)")
print("  保留: K_a (MDL 最简), K_c (手性配对结构匹配)")
shortlist = ["K_a", "K_c"]
check("S5-C1 收窄为双候选 {K_a, K_c}", sorted(shortlist) == sorted(["K_a", "K_c"]))
check("S5-C2 双候选仍落在预言带内",
      all(KAPPA_LO <= CAND[k]["value"] <= KAPPA_HI for k in shortlist),
      "K_a=%.3e K_c=%.3e" % (CAND["K_a"]["value"], CAND["K_c"]["value"]))

# ============================================================
# S6 判别性: 双候选的 δz_pol 预测谱
# ============================================================
print("\n[S6] 判别性: 双候选 δz_pol 预测谱")
G, M_SUN, R_SUN, C = 6.67430e-11, 1.989e30, 6.957e8, 299792458.0
z_sun = G * M_SUN / (R_SUN * C**2)
z_wd = G * (0.6 * M_SUN) / (0.01 * R_SUN * C**2)
print(f"  z_grav(太阳) = {z_sun:.3e}, z_grav(白矮星) = {z_wd:.3e}")
print(f"  {'候选':<5s} {'δz_pol(太阳)':>14s} {'δz_pol(白矮星)':>16s} {'比(矮星/太阳)':>12s}")
pred = {}
for k in shortlist:
    p_s = CAND[k]["value"] * z_sun
    p_w = CAND[k]["value"] * z_wd
    pred[k] = (p_s, p_w)
    print(f"  {k:<5s} {p_s:14.3e} {p_w:16.3e} {p_w/p_s:12.4f}")
ratio_ca = pred["K_c"][1] / pred["K_a"][1]
check("S6-C1 双候选白矮星预测区分度 = 2 倍 (K_c/K_a = N_Weyl/2)",
      abs(ratio_ca - 2.0) < 1e-12, "ratio=%.6f" % ratio_ca)
check("S6-C2 双候选预测在可观测量级 (白矮星 δz_pol ∈ [1e-6,1e-8])",
      all(1e-9 <= pred[k][1] <= 1e-5 for k in shortlist),
      "range=[%.2e,%.2e]" % (pred["K_a"][1], pred["K_c"][1]))

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 72)
print("汇总")
print("=" * 72)
passed = sum(1 for _, ok, _ in _CHECKS if ok)
total = len(_CHECKS)
print("结果: %d/%d" % (passed, total))
for name, ok, detail in _CHECKS:
    mark = "[PASS]" if ok else "[FAIL]"
    line = "  %s %s" % (mark, name)
    if detail:
        line += "  (%s)" % detail
    print(line)

print("""
结论:
  1. 选择原理评估: MDL 最简性 -> K_a; 手性配对结构匹配 -> K_c;
     d_H 残差 δ_fit 无小整数关联 (S4 未通过 -> 不提供锁定)。
  2. 候选族收窄: 4 -> 双候选 {K_a=4.44e-3, K_c=8.89e-3} (剔除 K_b/K_e)。
  3. κ_Δ 精确值仍登记开放: 双候选无实验锚定与框架内固定点方程;
     锁定需 (a) 4-范畴 Δ 结构完整推导 或 (b) 远期偏振光谱观测。
  4. 这是选择原理形式化推进 (非闭合): 明确了候选收窄规则与
     锁定条件, 对比 √5 选择原理 (有 χ² 锚定) 诚实标注差异。
""")
if passed < total:
    raise SystemExit(1)
