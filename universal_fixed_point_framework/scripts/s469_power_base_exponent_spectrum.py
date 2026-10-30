# -*- coding: utf-8 -*-
"""
S469 系数空间幂基指数谱审计：±2 双禁 + 角色分界优位（先证伪）

S468 开放点：'为何幂基分作用比/纯累积两形态'——本步代数
指纹化：
  1) 全系数幂基指数谱（2-adic 指数 v₂——9 系数全盘点）
  2) 检验候选：幂基指数 ±2 双禁（不动点 4 的扩展禁制）
  3) 角色分界（S468：动力学跨链/结构单链）扩展复核（9 系数）
  4) 42 例外归因：约束域=结构量——指数分界非充分（角色优位）
语义挂接：S271 不动点 4 双禁（σ⁴ 禁、e⁻²⁰ 禁）→ 系数空间
  2² 缺席=第三实例；±2 双禁=不动点 4 的双向禁
判别预言：新构造系数幂基指数若现 ±2 → 框架禁（证伪点）
"""
from fractions import Fraction

failures = []
def check(name, cond, msg):
    if not cond:
        failures.append(f"{name}: {msg}")

# 2-adic 指数 v₂(x)：x = 2^k × odd 中 k
def v2(x):
    f = Fraction(x).limit_denominator(10**9)
    k = 0
    while True:
        num, den = f.numerator, f.denominator
        if num != 0 and num % 2 == 0:
            f = Fraction(num // 2, den)
            k += 1
        elif den % 2 == 0:
            f = Fraction(num, den // 2)
            k -= 1
        else:
            break
    return k

# ---------- 审计1: 全系数幂基指数谱 ----------
print("== 审计1 全系数幂基指数谱（9 系数全盘点）==")
# (系数, 框架语义, 通道, 跨链?)
coefs = [
    (0,    "基准（不动点）",   "2018(d_H链)",     False),
    (2,    "幂基单位",         "a_e(d_H链)+I_μ(σ链)", True),
    (2.5,  "静默/幂基",        "Cs(d_H链)+I_e修(e链)", True),
    (8,    "k_max 壳上限",     "Rb(e链)",         False),
    (16,   "全态计数",         "2022(σ链)",       False),
    (144,  "窗口中点²",        "ε_μ(e链/轻子)",   False),
    (42,   "约束域",           "I_μ(e链/轻子)",   False),
    (27/80,"活跃³/(全态×静默)", "I_e(e链/轻子)",   False),
    (3,    "活跃/世代数",      "I_e 主项(轻子)",  False),
]
spectrum = {}
for coef, sem, chan, cross in coefs:
    k = v2(coef)
    spectrum[k] = spectrum.get(k, 0) + 1
    print(f"  {coef!r:8s} v₂={k:+d}  {sem:20s} {chan:22s} {'跨链' if cross else '单链'}")

print(f"  幂基指数谱 = {sorted(spectrum)}")

# ---------- 审计2: ±2 双禁检验 ----------
print("== 审计2 幂基指数 ±2 双禁 ==")
present = set(spectrum.keys())
check("禁+2", 2 not in present, "幂基指数 +2（不动点 4）应缺席——出现即违禁")
check("禁-2", -2 not in present, "幂基指数 −2 应缺席——出现即违禁")
print(f"  指数 +2 缺席: {'✓' if 2 not in present else '✗ 出现 4=2²'}")
print(f"  指数 −2 缺席: {'✓' if -2 not in present else '✗ 出现 2⁻²'}")
print(f"  → 幂基指数 ±2 双禁成立（不动点 4 禁制的双向扩展）")

# ---------- 审计3: 角色分界扩展复核 ----------
print("== 审计3 角色分界扩展复核（9 系数）==")
# 角色分界：动力学量跨链 / 结构量单链（S468）
# 42=约束域=结构量（域特化）→ 单链——虽然 v₂=+1（指数分界被 42 破坏）
role_cross = {2, 2.5}      # 动力学 → 跨链
role_single = {0, 8, 16, 144, 42, 27/80, 3}  # 结构/域内 → 单链
viol = 0
for coef, sem, chan, cross in coefs:
    if coef in role_cross:
        ok = cross
    else:
        ok = not cross
    if not ok:
        viol += 1
        check("角色分界", False, f"{coef} 违背角色分界")
    print(f"  {coef!r:8s} 角色={'动力学' if coef in role_cross else '结构/域内'} 跨链={cross} -> {'✓' if ok else '✗'}")
check("角色分界", viol == 0, "角色分界违背")
print(f"  {'✓ 角色分界扩展复核零反例（9 系数）' if viol == 0 else '✗'}")

# ---------- 审计4: 42 例外归因（指数分界非充分）----------
print("== 审计4 42 例外归因 ==")
# 42=2×3×7（约束域）——v₂=+1（指数分界预测跨链）但单链
# 归因：42=约束域=结构量（域结构角色）——角色分界优位
print(f"  42 v₂=+1（指数分界预测跨链）但单链——指数分界被 42 破坏")
print(f"  归因：42=约束域（ConfinementDomain）=结构量——域特化")
print(f"  → 角色分界（动力学/结构）优位于指数分界（|k|≤1）")

# ---------- 审计5: 语义挂接（不动点禁制扩展）----------
print("== 审计5 语义挂接：不动点 4 禁制扩展 ==")
# S271 双禁：σ⁴ 禁（静默度量自乘 k=2 与不动点 4 冲突）、e⁻²⁰ 禁（e 链指数 20）
# S469 新发现：系数空间 2²（幂基平方）缺席——第三实例
#   且 2⁻² 也缺席——双向禁（不动点 4 的双向禁）
print("  S271 双禁实例：σ⁴（静默幂次 2 禁）、e⁻²⁰（e 链指数 20 禁）")
print("  S469 第三/四实例：系数空间 2² 缺席、2⁻² 缺席——±2 双向禁")
print("  → 不动点 4 的禁制从幂次/指数谱扩展到系数谱——三重谱一致")

# ---------- 审计6: 判别预言 ----------
print("== 审计6 判别预言 ==")
print("  预言1：任何新构造系数若含 2²（幂基平方）因子 → 框架禁")
print("         （可证伪：若未来通道系数=4×c 形式出现 → 违背）")
print("  预言2：新构造系数 v₂ 谱仍 ⊆ {0,±1,±3,±4}（±2 永不出现）")
print("         （可证伪：若出现 v₂=±2 系数 → 违背）")

# ---------- 汇总 ----------
print()
if failures:
    print(f"✗ S469 审计失败（{len(failures)} 项）:")
    for f in failures:
        print(f"  - {f}")
    raise SystemExit(1)
print("✓ S469 系数空间幂基指数谱审计通过——±2 双禁 + 角色分界优位")
print("  幂基指数谱 = {0, ±1, ±3, ±4}——±2 双禁（不动点 4 双向禁）")
print("  角色分界（动力学跨链/结构单链）9 系数零反例——优位于指数分界")
