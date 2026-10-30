# -*- coding: utf-8 -*-
"""
Phase 104az-18 (26.16j-66): P1 多星 Lp(B) 平台检验 — 6 点线偏振散布 vs 常数平台
P1 预言: 连续区线偏振 ΔQ/U ∝ 1/8 (k_max=8 偏振身份) ≈ 0.725%
数据: 高场样本现有 Lp 观测 (混合来源/口径, 见 26.16j-49/-51/-53/-57)
统计: 加权均值, chi2 散布检验, 双峰结构, 诚实评估
"""
import math

P1 = 0.725  # % 预言

# 6 点: (星, B_MG, B口径, Lp_pct, err_pct, 来源, 备注)
stars = [
    ("J033320",       520, "Bp",  0.03, 0.07, "ZTF/JKepler? 无信号", "无信号(<1sigma), 可能 pole-on 或观测质量"),
    ("Grw+70 8247",   350, "~",   0.29, 0.20, "R 带 4000-6500?",     "B 带 ~3%=回旋标准物理, R 带干净对照"),
    ("ZTF J190132",   618, "Bp",  0.30, 0.06, "ZTF 2023?",           "5sigma 显著但 0.41xP1"),
    ("J100356",       668, "Bp",  0.60, 0.16, "Keck LRISp-ADC 2023", "0.83xP1"),
    ("J234605",       706, "Kepler BHa", 1.33, 0.40, "SPOL/MMT",      "tangled 场剔除(26.16j-54), 保守 <2%"),
    ("J135141",       773, "Bp",  0.62, 0.40, "SAO SCORPIO 2007",   "无回旋背景, 干净对照"),
]

def wmean(data):
    """加权均值 + 误差 (inverse-variance)"""
    wsum = sum(1.0/e**2 for _, e in data)
    mu = sum(v/e**2 for v, e in data) / wsum
    err = 1.0/math.sqrt(wsum)
    chi2 = sum(((v-mu)/e)**2 for v, e in data)
    return mu, err, chi2, len(data)-1

print("="*100)
print("P1 多星 Lp(B) 平台检验 (Phase 104az-18, 26.16j-66)  P1 预言 = {:.3f}%".format(P1))
print("="*100)
hdr = "{:<14}{:>6}{:>10}{:>8}{:>8}{:>10}{:>12}".format("Star", "B_MG", "B_type", "Lp(%)", "err", "obs/pred", "note")
print(hdr); print("-"*100)
for s in stars:
    name, B, bt, lp, err, src, note = s
    print("{:<14}{:>6.0f}{:>10}{:>8.2f}{:>8.2f}{:>10.2f}{:>12}".format(
        name, B, bt, lp, err, lp/P1, note[:12]))

print()
print("-"*100)
# 全 6 点
mu, err, chi2, dof = wmean([(s[3], s[4]) for s in stars])
print("全 6 点加权均值: {:.3f} ± {:.3f}%  (obs/pred {:.2f})  chi2/dof = {:.1f}/{}".format(mu, err, mu/P1, chi2, dof))
# 剔除 J2346 (tangled)
sub = [s for s in stars if s[0] != "J234605"]
mu2, err2, chi22, dof2 = wmean([(s[3], s[4]) for s in sub])
print("剔除 J2346 (5 点): {:.3f} ± {:.3f}%  (obs/pred {:.2f})  chi2/dof = {:.1f}/{}".format(mu2, err2, mu2/P1, chi22, dof2))
# 剔除 J2346 + J033320 (无信号)
sub2 = [s for s in sub if s[0] != "J033320"]
mu3, err3, chi23, dof3 = wmean([(s[3], s[4]) for s in sub2])
print("剔除 J2346+J033320 (4 点): {:.3f} ± {:.3f}%  (obs/pred {:.2f})  chi2/dof = {:.1f}/{}".format(mu3, err3, mu3/P1, chi23, dof3))

print()
print("-"*100)
print("双峰结构分析 (按 obs/pred 分组):")
lo = [s for s in stars if 0 < s[3]/P1 <= 0.6]
hi = [s for s in stars if s[3]/P1 > 0.6]
print("  低组 (~0.4x): " + ", ".join("{} {:.2f}".format(s[0], s[3]/P1) for s in lo))
print("  高组 (~0.85x): " + ", ".join("{} {:.2f}".format(s[0], s[3]/P1) for s in hi))
print("  若为常数平台 P1: 同 B 档内散布 (J190132 618MG 0.30 vs J100356 668MG 0.60) 应接近 -> 2x 散布不支持单一常数平台")
print("  若为场几何投影因子 (sin^2 或视线平均): 低组=低投影, 高组=高投影 -> 双峰可解释")
print("  诚实评估: 现有 6 点(含误差/口径差异)不支持常数平台; 散布>平台 -> 量级方向性支持维持, 平台判别未闭合")

# ---------------- 存盘 ----------------
out = {
    "P1_pred": P1,
    "points": [{"name": s[0], "B_MG": s[1], "B_type": s[2], "Lp": s[3], "err": s[4],
                "obs_pred": round(s[3]/P1, 3), "note": s[6]} for s in stars],
    "stats": {
        "all6": {"mu": round(mu,4), "err": round(err,4), "chi2": round(chi2,2), "dof": dof},
        "no_J2346": {"mu": round(mu2,4), "err": round(err2,4), "chi2": round(chi22,2), "dof": dof2},
        "no_J2346_J033320": {"mu": round(mu3,4), "err": round(err3,4), "chi2": round(chi23,2), "dof": dof3},
    },
    "conclusions": [
        "多星 Lp 散布 (0.03-1.33%) 大于常数平台 P1 (0.725%) 的预期",
        "双峰结构: ~0.4x (Grw+70 0.29/ZTF J190132 0.30) vs ~0.85x (J135141 0.62/J100356 0.60)",
        "同 B 档散布 (J190132 618MG 0.30 vs J100356 668MG 0.60, 2x) 不支持单一常数平台",
        "场几何投影/口径差异可解释双峰; 需每星倾角+投影因子统一口径",
        "P1 维持量级方向性支持 (候选级), 平台判别未闭合",
    ],
}
import json
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase104_p1_platform_tmp.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print()
print("已存盘: _phase104_p1_platform_tmp.json")
