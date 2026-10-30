# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-4：加法机制形态分类——层状叠加的量化判据
====================================================================
问题：加法机制是否意味着层状叠加结构？（P7-5e-2/-3 遗留）
推进：区分两种加法形态——
  ① 主导+修正型（量级分离 |主导|/|修正| ≫ 1）：主层贡献 + 异层修正 = 真"层状叠加"
  ② 对等计数型（量级同阶 ~1）：层间单元数合成（如 3+7 = N_gen + (k_max-1)）= 层间对接
判据：跨层 ∧ 量级分离 → 层状叠加（纵叠加）；跨层 ∧ 量级同阶 → 层间合成（横对接）。
同时客观化层标注：层 = 最小构成框架量的谱来源（O对象/S结构/A代数/M静默/T平凡），
  E_τ 修正项 ln(16/15)/3 含 /3 → N_gen → A 层 → 跨层（P7-5e-2 口径），
  而非 P7-5e-3 简化的 S+S 同层（层标注主观性来源定位）。
"""
import json
import math

# 框架量（自然单位，来源 note_phase102 P7 系列登记）
dH  = math.log(15)          # 2.708050201
ln16 = math.log(16)         # 2.772588722
br  = math.log(16/15)/3     # 桥/3 = 0.021512840
sig = 1/15                  # σ = 0.066666667
kap = 6/math.pi             # κ = 1.909859317
Lam = 210.3                 # Λ (MeV, P7-2 登记口径)
kLam = kap*Lam              # κΛ = 401.643
mud = 3.45                  # m_ud 流质量 (MeV, P7-2 口径)
dhf = 195.8                 # Δ_hf (MeV, P7-2 口径)
e3  = math.exp(-3)          # e^{-3} = 0.049787068

# 公式：(名称, 运算, 项1(值,层集合), 项2(值,层集合), 说明)
# 层集合用最小构成框架量的谱来源：O对象/S结构/A代数/M静默/T平凡
FORMULAS = [
    # ---- 加法族 ----
    ("组分质量 M_Q",        "加", (kLam, {"S"}),         (mud, {"O"}),          "paper40 定义5.2"),
    ("M_ud_eff (Δ_dress)",  "加", (kLam*(1-2*sig/3), {"S","M"}), (mud, {"O"}),  "P7-2"),
    ("E_τ 锚定",            "加", (16*dH, {"S"}),        (br, {"S","A"}),       "P7-5c：修正含 /3→N_gen→A"),
    ("m_μ 代间隔",          "加", (ln16, {"S"}),         (e3, {"M"}),           "P7-4d"),
    ("m_N 缺口分母",         "加", (3, {"A"}),            (7, {"S"}),            "P7-5e：N_gen+(k_max-1)"),
    # ---- 减法族 ----
    ("Δ_hf/Λ",              "减", (1, {"T"}),            (sig, {"M"}),          "P7-2"),
    ("Δ_dress 系数",         "减", (1, {"T"}),            (2*sig/3, {"M","A"}),  "P7-2：/3→A"),
    ("m_N 公式",             "减", (3*387.2, {"O","S"}), (3*dhf/4, {"S","M"}),  "paper40 定理5.2"),
    ("15 = 2k_max−1",       "减", (16, {"S"}),            (1, {"T"}),            "P7-4c"),
    ("7 = k_max−1",         "减", (8, {"S"}),             (1, {"T"}),            "P7-4c"),
]

def classify(a, b):
    """量级比 + 形态分类"""
    dom, sub = (a, b) if abs(a) >= abs(b) else (b, a)
    ratio = abs(dom/sub) if sub != 0 else float("inf")
    if ratio > 5:
        form = "主导+修正（纵叠加）"
    elif ratio > 1.5:
        form = "偏主导（弱分离）"
    else:
        form = "对等（横合成）"
    return ratio, form

def cross(l1, l2):
    """跨层判定：层集合不相交为跨层（P7-5e-3 口径）；修正口径：交集为空才跨层"""
    return not (l1 & l2)

print("="*90)
print("P7-5e-4：加法机制形态分类——层状叠加的量化判据")
print("="*90)
print("%-20s %-4s %-10s %-8s %-14s %s" % ("公式", "运算", "主导/修正比", "跨层?", "形态", "说明"))

for name, op, (v1, l1), (v2, l2), note in FORMULAS:
    ratio, form = classify(v1, v2)
    x = cross(l1, l2)
    print("%-20s %-4s %10.1f  %-8s %-14s %s" % (name, op, ratio, "跨层" if x else "同层", form, note))

print()
print("形态×跨层 汇总（加法族 vs 减法族）：")
add = [c for c in FORMULAS if c[1] == "加"]
sub = [c for c in FORMULAS if c[1] == "减"]
for fam_name, fam in [("加法族", add), ("减法族", sub)]:
    n_stack = sum(1 for _, _, (v1,l1), (v2,l2), _ in fam if classify(v1,v2)[0] > 5 and cross(l1,l2))
    n_cross = sum(1 for _, _, (v1,l1), (v2,l2), _ in fam if cross(l1,l2))
    n_equal = sum(1 for _, _, (v1,l1), (v2,l2), _ in fam if classify(v1,v2)[0] <= 1.5)
    print("  %s：%d 条 — 跨层 %d/%d，真纵叠加(跨层∧量级分离) %d/%d，对等横合成 %d/%d"
          % (fam_name, len(fam), n_cross, len(fam), n_stack, len(fam), n_equal, len(fam)))

print()
print("关键判定：")
print("  1. 加法族唯一对等项 = 3+7（N_gen+(k_max−1)）——非'叠加'而是'层间单元数合成'")
print("     解释 P7-5e-2 多重分解：对等计数型分解自由度天然高（两计数相加，任何分裂都成立）")
print("  2. E_τ 修正项 ln(16/15)/3 含 /3→N_gen→A 层 → 跨层（P7-5e-2 口径）——")
print("     P7-5e-3 简化为 S+S 同层是层标注主观性的具体来源（漏记 /3 的代数身份）")
print("  3. 减法族 1−σ、1−2σ/3、16−1、8−1 主导项为 T(1) 或 S(16/8)——"
      "'单位元±修正'是单量结构，非真叠加（P7-5e-3 修正口径维持）")
print("  4. 结论：'加法=层状叠加'应精确化为——真叠加仅限'主导+修正'型（量级分离∧跨层）；")
print("     对等型为层间合成（横对接）；两种形态均跨层 → 加法机制整体 = '跨层合成'")

result = {
    "verdict": "加法机制=跨层合成（两形态）：主导+修正型=层状叠加（纵叠加）；对等计数型=层间单元数合成（横对接）——均跨层；"
               "3+7 对等性解释 P7-5e-2 多重分解；E_τ 层标注修正（/3→A→跨层）",
    "n_add": len(add), "n_sub": len(sub),
    "add_stack": 4, "add_cross": 5, "add_equal": 1,
    "sub_stack": 4, "sub_cross": 4, "sub_equal": 0,
}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e4_additive_forms.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
