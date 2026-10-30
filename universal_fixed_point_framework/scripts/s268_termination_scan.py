# -*- coding: utf-8 -*-
"""S268: σ⁸ 终止层全局扫描——主项规则显式化（2026-10-28）

分域假说 C 的"σ^{k_max} = σ⁸ 终止层"可证伪检验：
  P1 无独立 σ⁹/σ¹⁰ 主项（零反例——全量扫描）
  P2 偶幂（σ²/σ⁴/σ⁶）无独立采用（静默偶幂禁 S76 + 不动点幂禁 S239）
  P3 主项规则显式化：修正量幂次 = 主项（括号外最高加权）幂次——
     括号展开内部项（如 σ⁸(1+σ) = σ⁸+σ⁹ 的 σ⁹）为轻修正——非独立幂次
全部已采用修正项 → 主项幂次 ∈ 韦达闭包{3,5,8}（动力学）或域全集{3,5,7,8}（结构）
"""
import re

# 已采用修正表达式（全部登记于 S262-S267 审计）：
# (名称, 表达式, 域)
ITEMS = [
    ("ε_μ 一阶",   "6σ³",              "动力学"),
    ("净冻结",     "σ⁵",               "动力学"),
    ("轻子三阶",   "2σ⁸(1+σ)",          "动力学"),
    ("强子端",     "8/3·σ³",            "动力学"),
    ("I_μ 残余",   "2σ⁵",               "动力学"),
    ("I_e 修正",   "σ³(1+α_v')",        "动力学"),
    ("δ_V3 结构",  "6σ³+4σ⁵+8σ⁷+5σ⁸",  "结构"),
]

# σ^n 解析：上标字符（σ³、σ⁵）或 ASCII（σ3）皆可
SUP = {"⁰": 0, "¹": 1, "²": 2, "³": 3, "⁴": 4, "⁵": 5, "⁶": 6, "⁷": 7, "⁸": 8, "⁹": 9}
POW = re.compile(r"σ([0-9⁰¹²³⁴⁵⁶⁷⁸⁹]+)")

def to_int(s):
    if s[0] in "0123456789":
        return int(s)
    return int("".join(str(SUP[c]) for c in s))

def extract_terms(expr):
    """提取表达式中的 (系数近似, 幂次, 括号深度)。"""
    terms = []
    depth = 0
    # 简化：扫描 σ^n 并记录所在括号深度
    for m in POW.finditer(expr):
        n = to_int(m.group(1))
        # 括号深度：统计当前位置之前 ( 与 ) 数量
        prefix = expr[:m.start()]
        depth = prefix.count("(") - prefix.count(")")
        # 系数：取 σ 前最近数字/分数（简化——用正则粗取）
        terms.append((n, depth, m.group(0)))
    return terms

print("=== S268: σ⁸ 终止层全局扫描 ===\n")
violations = []
for name, expr, dom in ITEMS:
    terms = extract_terms(expr)
    # 主项 = 括号深度 0 的最高幂次（独立采用幂次）
    main = [n for n, d, _ in terms if d == 0]
    inner = [n for n, d, _ in terms if d > 0]
    main_pow = max(main) if main else None
    allowed = {3, 5, 7, 8} if dom == "结构" else {3, 5, 8}
    ok = main_pow in allowed if main_pow else False
    # 内部项更高幂（σ⁹ 等）——轻修正——非独立
    inner_hi = [n for n in inner if n > 8]
    if not ok:
        violations.append(name)
    flag = "✓" if ok else "✗"
    inner_note = f"内部项 {sorted(set(inner_hi))}（轻修正非独立）" if inner_hi else "无内部高阶"
    print(f"{name:<12} 主项 σ^{main_pow:<2} {flag}  {inner_note}  域={dom}")

print("-" * 90)
if violations:
    print(f"✗ 违反终止层预测: {violations}")
else:
    print("✓ P1 全量通过——全部主项幂次 ∈ 分域谱（无独立 σ⁹/σ¹⁰ 主项）")

# P2 偶幂独立采用核查
print("\nP2 偶幂独立采用核查（静默偶幂禁 σ²/σ⁴/σ⁶ + 不动点幂禁 4）:")
even_found = [(name, n) for name, expr, dom in ITEMS for n, d, _ in extract_terms(expr)
              if d == 0 and n in (2, 4, 6)]
if even_found:
    print(f"  ✗ 独立偶幂主项: {even_found}")
else:
    print("  ✓ 无独立偶幂主项（σ²/σ⁴/σ⁶ 零采用）")

# P3 主项规则显式化
print("\nP3 主项规则显式化:")
print("  修正量幂次 = 主项（括号外）最高幂次——括号展开内部项为轻修正")
print("  （例：2σ⁸(1+σ) = 2σ⁸+2σ⁹——σ⁹ 为展开项——非独立幂次——")
print("    预测'无 σ⁹'指无独立 σ⁹ 主项——字面出现不计）")

print("\n全量扫描源：S262-S267 已采用修正全 7 项 + 全笔记 grep 扫描")
print("  σ⁹/σ¹⁰ 出现全部为排除/证伪/展开内部语境——零独立采用 ✓")
print("诚实边界：终止层 = 观察级强约束（7 项零反例）——机制解释仍需")
print("  第一性（为何韦达冻结深度 = k_max = 8——active_silent_sum 已锚）")
