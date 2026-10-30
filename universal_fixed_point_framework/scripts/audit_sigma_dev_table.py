# -*- coding: utf-8 -*-
"""P1 sigma_dev 回填计算（104az-200 §10 P1 落地，2026-10-21）
口径：sigma_dev = dev_rel / sigma_obs_rel
观测不确定度来源：CODATA 2018 / PDG（与生成链表 §6 表口径一致）
"""
import json

def grade(s, dev_rel):
    if dev_rel == 0:
        return "判定级(精确恒等命中)"
    a = abs(s)
    if a < 0.5: return "兼容无分辨力"
    if a < 3.0: return "候选级"
    if a < 5.0: return "强候选级"
    return "判定级(命中/排除)"

def sigma_dev(fw_val, obs_val, obs_abs_err, note=""):
    dev_abs = fw_val - obs_val
    dev_rel = dev_abs / obs_val
    sig_rel = abs(obs_abs_err) / abs(obs_val)
    s = dev_rel / sig_rel
    return {"fw": fw_val, "obs": obs_val, "obs_abs_err": obs_abs_err,
            "dev_abs": dev_abs, "dev_rel": dev_rel, "sig_rel": sig_rel,
            "sigma_dev": s, "grade": grade(s, dev_rel), "note": note}

rows = []

# 1. kappaLambda：框架 92800/231 vs 定义值 401.73304855（104az-103）；观测侧 Lambda_QCD 0.14% 摆动（104az-106）
rows.append(dict(name="kappaLambda", **sigma_dev(
    92800/231, 401.73304855, 401.73304855*1.4e-3,
    "对定义值 401.73304855(104az-103)；观测侧 Λ_QCD=210.0/210.3 摆动 0.14%(104az-106)")))

# 2. g_p/2：40217/14400 vs CODATA 2018 mu_p/mu_N
rows.append(dict(name="g_p/2", **sigma_dev(
    40217/14400, 2.79284734463, 8.2e-8,
    "CODATA 2018 μ_p/μ_N = 2.79284734463(82)")))

# 3. m_t/m_b：D 三角互锁闭式 41.3134074 vs PDG 中心口径 41.284±0.237（104az-169 登记）
rows.append(dict(name="m_t/m_b", **sigma_dev(
    41.3134074, 41.284, 0.237,
    "PDG 中心口径比值 41.284±0.237（104az-169 登记）")))

# 4. 1/alpha 路径A：d_H=16259/6000 → 24(d_H+3)=137.0360 vs CODATA 2018 alpha^-1
rows.append(dict(name="1/α 路径A", **sigma_dev(
    24*(16259/6000 + 3), 137.035999084, 2.1e-8,
    "CODATA 2018 α⁻¹=137.035999084(21)；d_H=16259/6000 跨链最优(152)，d_H 为自由参数非预言")))

# 5. 1/alpha 路径B：d_H=65/24 → 24(d_H+3)=137 整数
rows.append(dict(name="1/α 路径B", **sigma_dev(
    24*(65/24 + 3), 137.035999084, 2.1e-8,
    "d_H=65/24 → 137 整数（§4 条目2 登记；§6 旧表 137.028 口径废止）")))

# 6. g_n/2：44/23 vs CODATA 2018 mu_n/mu_N（绝对值比）
rows.append(dict(name="g_n/2", **sigma_dev(
    44/23, 1.91304273, 4.5e-7,
    "CODATA 2018 μ_n/μ_N = −1.91304273(45)（绝对值口径）")))

# 7. 21/100：Hγ 理论精确值（巴耳末 1/4−1/25），R∞ CODATA 2018 相对 1.9e-12
rows.append(dict(name="21/100", **sigma_dev(
    0.21, 0.21, 0.21*1.9e-12,
    "巴耳末 1/4−1/25 精确恒等；R∞ CODATA 2018 相对不确定度 1.9e-12")))

print("=" * 120)
print(f"{'名称':>12} | {'dev_rel':>12} | {'sig_rel':>10} | {'sigma_dev':>10} | 等级 | 口径")
print("-" * 120)
for r in rows:
    print(f"{r['name']:>12} | {r['dev_rel']:+.3e} | {r['sig_rel']:.3e} | {r['sigma_dev']:+.3f} | {r['grade']:<12} | {r['note']}")
print("=" * 120)

with open("audit_sigma_dev_table.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print("已输出 audit_sigma_dev_table.json")
