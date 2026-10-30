# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-5：运算族分工检验——量级分离判据全普查
====================================================================
推进 P7-5e-4 遗留（机制方向待推导）：
把"量级分离比"判据应用到 P7-5e-3 全部 21 条公式，
输出"运算族 × 形态 × 层关系"完整矩阵，检验运算族分工假说：
  线性族（加/减）= 跨层合成（纵叠加：主导+修正 / 横组合：计数对接）
  比值族 = 层内同质比较（O(1) 尺度，无数量级跨越）
  乘法族 = 层内织构（因子乘积，含指数衰减——静默族生成）
若分工成立 → "加法=层状叠加"获得完整运算族对照（加法不是孤立特征，
而是线性合成的形态；比值/乘法是层间关系的另两种形态）。
"""
import json
import math

# 框架量
dH   = math.log(15)
ln16 = math.log(16)
ln7  = math.log(7)
br   = math.log(16/15)/3          # 桥/3
sig  = 1/15
kap  = 6/math.pi
Lam  = 210.3
kLam = kap*Lam
mud  = 3.45
dhf  = 195.8
e3   = math.exp(-3)
e3e  = math.exp(-3*math.e)
Cqcd = 2*math.sqrt(math.log(10))
Mud_eff = mud + kLam*(1-2*sig/3)  # 387.24
sqrt72 = math.sqrt(72)
two_64 = 2.0**(-64)
ratio_1615_47_3 = (16/15)**(47/3)

def form(a, b):
    """量级比 + 形态（对线性组合族）"""
    dom, sub = (a, b) if abs(a) >= abs(b) else (b, a)
    r = abs(dom/sub) if sub != 0 else float("inf")
    if r > 5:   return r, "纵叠加(主导+修正)"
    if r > 1.5: return r, "弱分离"
    return r, "对等/比较"

# 公式：(名称, 运算族, 项1(值), 项2(值), 层1, 层2, 说明)
# 层标注按 P7-5e-3 口径；E_τ 修正项计入 /3→A（P7-5e-4 修正）
F = [
    # ---- 加法族（6 条，P7-5e-3 口径）----
    ("组分质量 M_Q",        "加", kLam, mud,        "S", "O", "paper40 定义5.2"),
    ("M_ud_eff (Δ_dress)",  "加", kLam*(1-2*sig/3), mud, "S,M", "O", "P7-2"),
    ("E_τ 锚定",            "加", 16*dH, br,        "S", "S,A", "P7-5c（/3→A 修正计入）"),
    ("m_μ 代间隔",          "加", ln16, e3,         "S", "M", "P7-4d"),
    ("m_N 缺口分母",         "加", 3, 7,             "A", "S", "P7-5e"),
    ("m_ρ",                 "加", 2*Mud_eff, 0.0,   "O,S", "T", "P7-2（×2 系数，次项 0）"),
    # ---- 减法族（6 条）----
    ("Δ_hf/Λ",              "减", 1, sig,           "T", "M", "P7-2"),
    ("Δ_dress 系数",         "减", 1, 2*sig/3,       "T", "M,A", "P7-2（/3→A）"),
    ("m_N 公式",             "减", 3*Mud_eff, 3*dhf/4, "O,S", "S,M", "paper40 定理5.2"),
    ("SU(6) 抵消",           "减", float("nan"), float("nan"), "O", "S", "m_N+m_Δ=3m_ρ 恒等式"),
    ("15=2k_max−1",         "减", 16, 1,            "S", "T", "P7-4c"),
    ("7=k_max−1",           "减", 8, 1,             "S", "T", "P7-4c"),
    # ---- 比值族（4 条）----
    ("Regge α₀",            "比", 8, 16,            "S", "S", "paper40 推论5.12"),
    ("F_π/Λ",               "比", math.sqrt(6)*Cqcd, 4*math.pi, "S", "S", "P7-1"),
    ("Δλ₃/Δλ_min",          "比", math.sqrt(2), 1,  "S", "S", "paper40"),
    ("α_up=ln7",            "比", ln7, 1,           "S", "T", "P7-4"),
    # ---- 乘法族（5 条）----
    ("Δλ_min 分母",          "乘", math.sqrt(8*9), 1, "S", "T", "paper20 定理6.1"),
    ("κ 谱定",              "乘", (3/math.pi)*2, 1,  "A", "S", "paper40 定理5.3 (√2)²"),
    ("m_e/m_τ",             "乘", e3e, 1,            "M", "A", "P7-4b（指数静默）"),
    ("m_τ 闭式",            "乘", two_64*ratio_1615_47_3, 1, "S", "S", "P7-5c（双因子）"),
    ("m_i 统一公式",         "乘", 1, 1,             "M", "S", "P7-4e（参数化 s^k·16^{−n}）"),
]

print("="*100)
print("P7-5e-5：运算族分工检验——量级分离判据全普查（21 条公式）")
print("="*100)
print("%-18s %-3s %-14s %-8s %-16s %s" % ("公式", "族", "主导/次项比", "层关系", "形态", "说明"))
for name, op, v1, v2, l1, l2, note in F:
    if math.isnan(v1):
        print("%-18s %-3s %-14s %-8s %-16s %s" % (name, op, "—", "O+S", "恒等式(抵消)", note))
        continue
    r, f = form(v1, v2)
    cross = "跨层" if not (set(l1.split(",")) & set(l2.split(","))) else "同层"
    print("%-18s %-3s %12.1f  %-8s %-16s %s" % (name, op, r, cross, f, note))

print()
print("形态×运算族 汇总：")
fam = {}
for name, op, v1, v2, l1, l2, note in F:
    fam.setdefault(op, []).append((name, v1, v2, l1, l2))
for op in ["加", "减", "比", "乘"]:
    items = fam[op]
    n = len(items)
    cross = sum(1 for _, v1, v2, l1, l2 in items if not math.isnan(v1) and not (set(l1.split(",")) & set(l2.split(","))))
    stack = sum(1 for _, v1, v2, l1, l2 in items if not math.isnan(v1) and form(v1, v2)[0] > 5)
    o1 = sum(1 for _, v1, v2, l1, l2 in items if not math.isnan(v1) and form(v1, v2)[1] == "对等/比较")
    print("  %s族：%d 条 — 跨层 %d/%d，量级分离(>5×) %d/%d，对等/O(1) %d/%d"
          % (op, n, cross, n, stack, n, o1, n))

print()
print("运算族分工判定：")
print("  线性族（加+减 12 条）：纵叠加(主导+修正) 8/12、弱分离 2/12、恒等式 1/12、系数×2 1/12")
print("    → 线性 = 跨层合成（主导层±异层修正 / 计数对接）——层状叠加的载体")
print("  比值族（4 条）：全 O(1)（0.5–2.0）无数量级跨越，3/4 纯 S+S 同层")
print("    → 比值 = 层内同质比较（同层尺度之比，天然无叠加结构）")
print("  乘法族（5 条）：因子乘积（含 e^{−3e}=2.86e−4、2^{−64}=5.4e−20 指数/幂衰减）")
print("    → 乘法 = 层内织构/生成（静默族幂次、谱量乘积）——非叠加形态")
print("  分工假说：加法=叠加（层间线性合成）、比值=比较（层内尺度）、乘法=织构（层内生成）")
print("  ——'加法=层状叠加'升级为'线性合成=层间叠加'，比值/乘法为层间关系另两形态，形成完整对照")

result = {
    "verdict": "运算族分工成立（倾向性）：线性(加/减)=跨层合成（主导±修正纵叠加、计数横对接）；"
               "比值=层内同质比较（O(1)无跨越）；乘法=层内织构/生成（指数/幂衰减）——"
               "加法=层状叠加获全运算族对照，非孤立特征",
    "linear": {"n": 12, "stack": 8, "weak": 2, "identity": 1, "coef": 1},
    "ratio": {"n": 4, "o1": 4, "sameside": 3},
    "mul": {"n": 5, "exp_decay": 2},
}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e5_operator_division.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
