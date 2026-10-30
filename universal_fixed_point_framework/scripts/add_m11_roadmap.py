# -*- coding: utf-8 -*-
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase72_n5_symbol_criterion.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

m11 = "| M11 | n=7 级联机制论证（2026-10-01 完成） | 动量守恒三分割恒等式 + Lean 化 | ✅ **级联机制闭合**：λ1+λ_A+λ_B=0 ⇒ [λ1,λ_A]=[λ_A,λ_B]（双线性+自零+反对称，仅动量守恒）；6 条级联恒等式数值 40000 样本 0 违反（paperX_n7_identities.py，修正 lhs=[λ1,λ_A] 后）；**N7Criterion.lean 零 sorry**（Fin 7 括号代数 + bk_1_234567_zero + 5 级联恒等式 + 2 sgn 定理，ZA/B 块积模式，lake build 通过）——\"尾部主导\"获解析解释：s1_A 被基座内尾部链块完全决定 |\n"

anchor = "| M10 | n=7 判据外推（2026-10-01 完成） | 56 因子相邻分割全集决定性 + 最小充分基座 + 阶数对照 | ✅ **n=7 判据数值闭合**：56 因子全集 26805 模式全决定性（30000 样本）；**16 因子最小充分基座**（贪心删除不动点，80000 主 + 2×20000 独立复核 0 真违反）；判定表 2577 条导出；**阶数 12→16（+4/级）持续**（n=5 需 8+2 扩展、n=6 需 12、n=7 需 16）；16 因子尾部主导（无 s1_2 单对——符号级联强证据）；单因子非零率平坦 ≈0.078（无单因子判据，与 n=6 一致）|\n"

assert anchor in s, "M10 anchor not found"
if "M11" in s:
    print("M11 already exists")
else:
    s = s.replace(anchor, anchor + m11)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(s)
    print("M11 added")
