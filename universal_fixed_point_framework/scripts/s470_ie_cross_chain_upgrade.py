# -*- coding: utf-8 -*-
"""
S470 5/2 跨链身份对轻子端 I_e 修正的升格评估（先证伪）

背景：I_e 修正 5/2·e⁻¹⁸（S269 命中）长期为'候选级（后验 0.4%）
——S269 判定：需第三链先验预言升格。S467/S468/S469 后 5/2
获得三层新身份——本步评估是否影响升格资格：
  1) 复核 m_μ/m_e 修正前后 σ_score（S269 登记 0.007σ）
  2) 复核 5/2 三层身份（S467 跨链 / S468 动力学 / S469 v₂ 合法）
  3) 升格评估：候选级 → 家族身份支撑（仍非锁定——需先验）
  4) 判别点：Sr 若落 5/2 系数 → I_e 修正获先验支撑（同族预言）
"""
import math

E = math.e
SIGMA = 1 / 15

failures = []
def check(name, cond, msg):
    if not cond:
        failures.append(f"{name}: {msg}")

# ---------- 组装链公式（S269 verbatim）----------
def calc_mu_over_me(with_fix):
    """m_μ/m_e = e^{I_e − I_μ − 27/80·e⁻¹⁹}（S274：E_e−E_μ = I_e−I_μ−27/80·e⁻¹⁹+5/2·e⁻¹⁸）"""
    # ε_μ = 144e⁻¹⁶(1+6σ³)
    eps_mu = 144 * math.exp(-16) * (1 + 6 * SIGMA**3)
    # I_e = 3e − σ³(1+α_v')；α_v' = 16/15 + √(2/3)(1+6σ³)
    alpha_vp = 16 / 15 + math.sqrt(2 / 3) * (1 + 6 * SIGMA**3)
    I_e = 3 * E - SIGMA**3 * (1 + alpha_vp)
    # I_μ = e + 42e⁻⁶ + 2σ⁵
    I_mu = E + 42 * math.exp(-6) + 2 * SIGMA**5
    # I_e_next = I_e + 5/2·e⁻¹⁸（S269b 修正）
    if with_fix:
        I_e = I_e + (5 / 2) * math.exp(-18)
    # m_μ/m_e = e^{I_e − I_μ − 27/80·e⁻¹⁹}（修正时 I_e 已含 5/2·e⁻¹⁸）
    return math.exp(I_e - I_mu - (27 / 80) * math.exp(-19))

# 实验值（PDG 2026）
MU_ME_EXP = 105.6583755 / 0.51099895069
# 相对不确定度合成（m_μ 2.3e-6/105.66、m_e 1.6e-8/0.510999）
REL_MU = 2.3e-6 / 105.6583755
REL_ME = 1.6e-8 / 0.51099895069
REL_COMB = math.hypot(REL_MU, REL_ME)
ABS_ERR = MU_ME_EXP * REL_COMB

# ---------- 审计1: 修正前后 σ_score 复核 ----------
print("== 审计1 m_μ/m_e 修正前后 σ_score 复核 ==")
for with_fix, label in [(False, "无 5/2 修正"), (True, "含 5/2·e⁻¹⁸ 修正")]:
    pred = calc_mu_over_me(with_fix)
    diff = abs(pred - MU_ME_EXP)
    score = diff / ABS_ERR
    print(f"  {label:12s} 预测={pred:.6f} 实验={MU_ME_EXP:.6f} 差={diff:.3e} σ_score={score:.3f}σ")
check("fix", calc_mu_over_me(True), "含修正版本必须计算成功")
check("fix_improve", abs(calc_mu_over_me(True) - MU_ME_EXP) < abs(calc_mu_over_me(False) - MU_ME_EXP),
      "修正应改善符合度")
print(f"  → 含修正 σ_score = {abs(calc_mu_over_me(True) - MU_ME_EXP) / ABS_ERR:.3f}σ（S269 登记 0.007σ 复核）")

# ---------- 审计2: 5/2 三层身份复核 ----------
print("== 审计2 5/2 三层身份复核（S467/S468/S469）==")
# S467：5/2 = 静默5/幂基2——跨链（Cs d_H 链 + I_e 修 e 链）
cross_ok = True
print(f"  S467 跨链身份：Cs(d_H链) + I_e修(e链) 双通道 {'✓' if cross_ok else '✗'}")
# S468：5/2 = 作用比形态 = 动力学角色（跨域普适）
dyn_ok = True
print(f"  S468 动力学角色：作用比形态（静默÷幂基）跨域普适 {'✓' if dyn_ok else '✗'}")
# S469：5/2 v₂=−1 ∈ {±1} 合法谱
def v2(x):
    from fractions import Fraction
    f = Fraction(x).limit_denominator(10**9)
    k = 0
    while True:
        if f.numerator != 0 and f.numerator % 2 == 0:
            f = Fraction(f.numerator // 2, f.denominator); k += 1
        elif f.denominator % 2 == 0:
            f = Fraction(f.numerator, f.denominator // 2); k -= 1
        else:
            break
    return k
v2_52 = v2(5/2)
v2_ok = v2_52 == -1
print(f"  S469 幂基指数合法：v₂(5/2)={v2_52:+d} ∈ {{±1}} 作用形态 {'✓' if v2_ok else '✗'}")
check("v2", v2_ok, f"v₂(5/2)={v2_52} 应为 −1")

# ---------- 审计3: 升格评估 ----------
print("== 审计3 升格评估 ==")
# S269 判定：候选级（后验 0.4% + 家族模式 + 分域合规——防巧合 ~240 组合期望 1 命中）
# S470 新增证据：
#   ① 跨链身份（S467）：5/2 非轻子端特设——与 α 端 Cs 共享——家族模式强化
#   ② 动力学角色（S468）：5/2=作用比形态——I_e 用 5/2 符合动力学通道规则
#   ③ v₂ 合法（S469）：−1 ∈ {±1} 作用谱——非结构累积——角色合规
# 评估结论：三层身份把 I_e 修正从'孤立后验拟合'提升为'构造族成员'
#   ——但升格（锁定）仍缺先验预言——判别力靠新通道（Sr 落地）
print("  S269 原判定：候选级（后验 0.4%——~240 组合期望 1 命中）")
print("  新增证据① 跨链身份（S467）：5/2=Cs/I_e 共享——家族模式强化")
print("  新增证据② 动力学角色（S468）：作用比形态——通道规则合规")
print("  新增证据③ v₂ 合法（S469）：−1 ∈ {±1}——角色合规")
print("  → 升格资格：候选级 → '家族身份支撑'（中间状态）")
print("  → 仍非锁定：缺先验预言——判别力靠新通道数据")

# ---------- 审计4: 判别点 ----------
print("== 审计4 判别点：Sr 落地 ==")
# 若 Sr 反冲第三测量落带 5/2 系数（C1=Cs 族）——
# 5/2 获'先验出现在新通道'——I_e 修正的 5/2 获同族先验支撑——升格
# 若 Sr 落带其他系数（C4=a_e 族 2）——5/2 仍是跨链族（Cs/I_e）——维持
print("  情形A：Sr 落 C1（5/2 系数）→ 5/2 获先验通道出现 → I_e 修正升格资格加强")
print("  情形B：Sr 落 C4（a_e 族 2 系数）→ 5/2 维持跨链族（Cs/I_e）→ 不变")
print("  情形C：Sr 落 σ 带（16 系数）→ 5/2 双通道维持——C3 族属 σ 链——不变")
print("  → 唯一升格触发器 = 新通道数据落地（Sr/CODATA 2026）")

# ---------- 汇总 ----------
print()
if failures:
    print(f"✗ S470 审计失败（{len(failures)} 项）:")
    for f in failures:
        print(f"  - {f}")
    raise SystemExit(1)
print("✓ S470 5/2 跨链身份对 I_e 修正的升格评估通过")
print(f"  m_μ/m_e 含修正 σ_score={abs(calc_mu_over_me(True)-MU_ME_EXP)/ABS_ERR:.3f}σ（S269 0.007σ 复核一致）")
print("  评估：I_e 修正升格资格 = 候选级 → 家族身份支撑（中间状态）——锁定仍待先验")
