# -*- coding: utf-8 -*-
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()
edits = 0
def rep(old, new, tag):
    global s, edits
    assert old in s, tag + " anchor not found"
    s = s.replace(old, new, 1)
    edits += 1

# 1. 版本行
rep("**版本**：v0.22（2026-10-02）", "**版本**：v0.23（2026-10-02）", "version")

# 2. §9 标题
rep("## 9 Lean 形式化（n=4 / n=5 / n=6 / n=7 / n=8）",
    "## 9 Lean 形式化（n=4–n=9：级联机制 + 判定表可执行编码）", "sec9 title")

# 3. §9 N7 段诚实定位更新（判定表已 Lean 化）
old_n7 = "- 诚实定位：级联恒等式为**解析定理**（值级 + 符号级 Lean 机器证明，仅需动量守恒，无需 R₁ 半共线）；n=7 判定表 2577 条未 Lean 化（参照 N6Table 位编码 + List 查表方案，候选下一步）"
new_n7 = "- 诚实定位：级联恒等式为**解析定理**（值级 + 符号级 Lean 机器证明，仅需动量守恒，无需 R₁ 半共线）；**n=7 判定表已 Lean 化（N7Table，2577 条，2026-10-02 回溯补，见下文“判定表 Lean 化”小节）**"
rep(old_n7, new_n7, "sec9 n7 honesty")

# 4. §9 追加"判定表 Lean 化"小节：插在 N6Table 条目（398 行）后
anchor_n6t = "- **`N6Table.lean`（判定表可执行编码）**：609 条\"12 因子模式 → A_BG\"表编码为 Lean 可执行查表函数（位编码键 + List 线性查找——规避 609 层嵌套 if 的 Decidable 递归深度超限）；`example + native_decide` 抽查定理 6 条机器验证通过；生成器 `paperX_n6_gen_lean_table.py`（json → Lean 文件）可复现"
tables_sec = anchor_n6t + r"""

- **判定表 Lean 化扩展（2026-10-02 回溯补：N7Table / N8Table / N9Table，全零 sorry，lake build 通过）**：
  - **`N7Table.lean`**：2577 条"16 因子模式 → A_BG"（16 因子位编码键，权重 2^i）；**3 块定义 + `++` 拼接**（2577 层 List cons 嵌套触发递归深度超限，分块 <900/块规避）——首个分块模板。
  - **`N8Table.lean`**：6253 条"23 因子模式 → A_BG"（23 因子位编码键）；8 块拼接（860×7 + 233）。
  - **`N9Table.lean`**：15212 条"27 因子模式 → A_BG"；**三进制编码**（-1→0、0→1、1→2，权重 3^i——n=9 键第 27 位可取 0，位编码失效）；18 块拼接（860×17 + 592）。
  - 技术要点：每项整体类型标注 `((k, v) : Nat × ℤ)` 防 MVar 合成超时；`example + native_decide` 抽查定理各 6 条机器验证通过；通用生成器 `paperX_gen_lean_table.py`（bit/ternary 两模式 + 分块参数）可复现。"""
rep(anchor_n6t, tables_sec, "sec9 tables")

# 5. 附录 A：N6Table 行后插 3 行 + 生成器行
anchor_app = "| `formal_proof/MUFPFormalization/src/MUFPFormalization/N6Table.lean` | Lean n=6 判定表可执行编码（609 条 + native_decide 抽查定理 6 条，零 sorry） | lake build 通过 |"
app_new = anchor_app + r"""
| `formal_proof/MUFPFormalization/src/MUFPFormalization/N7Table.lean` | Lean n=7 判定表可执行编码（2577 条 16 因子位编码键、3 块拼接 + native_decide 抽查 6 条，零 sorry） | lake build 通过（148s） |
| `formal_proof/MUFPFormalization/src/MUFPFormalization/N8Table.lean` | Lean n=8 判定表可执行编码（6253 条 23 因子位编码键、8 块拼接 + native_decide 抽查 6 条，零 sorry） | lake build 通过（154s） |
| `formal_proof/MUFPFormalization/src/MUFPFormalization/N9Table.lean` | Lean n=9 判定表可执行编码（15212 条 27 因子三进制编码键、18 块拼接 + native_decide 抽查 6 条，零 sorry） | lake build 通过（206s） |
| `scripts/paperX_gen_lean_table.py` | 判定表 → Lean 通用生成器（bit/ternary 两模式 + 分块参数，N7/N8/N9 复用） | — |"""
rep(anchor_app, app_new, "appendix A tables")

# 6. 结论 8 更新
old_c8 = "8. 形式化（第9节）：n=4 恒等式 Lean 证明零 sorry；**n=5 判据 14 模式定理全部机器证明零 sorry（依赖链 N5Criterion→…→N5SingleLemmas→14 模式定理）；n=6 括号代数底座（N6Criterion，5 条动量守恒零恒等式）+ 判定表可执行编码（N6Table，609 条 + native_decide 抽查）零 sorry**。"
new_c8 = "8. 形式化（第9节）：n=4 恒等式 Lean 证明零 sorry；**n=5 判据 14 模式定理全部机器证明零 sorry（依赖链 N5Criterion→…→N5SingleLemmas→14 模式定理）；n=6 括号代数底座（N6Criterion，5 条动量守恒零恒等式）+ 判定表可执行编码（N6Table，609 条）零 sorry；n=7/8/9 级联机制 Lean 化（N7/N8/N9Criterion，零 sorry，级联机制机器证明链 n=5→n=9 完整）+ 判定表回溯补（N7Table 2577 条 / N8Table 6253 条 / N9Table 15212 条，分块 + 位/三进制编码，native_decide 抽查全过，零 sorry）**。"
rep(old_c8, new_c8, "conclusion 8")

# 7. 稿态尾部 Lean 形式化句更新
old_abs_tail = "Lean 形式化：n=4 恒等式完成（零 sorry），n=5 判据 14 模式定理完成（零 sorry），n=6 括号代数 + 判定表完成（零 sorry）。"
new_abs_tail = "Lean 形式化：n=4 恒等式完成（零 sorry），n=5 判据 14 模式定理完成（零 sorry），n=6 括号代数 + 判定表完成（零 sorry），n=7/8/9 级联机制 Lean 化（N7/N8/N9Criterion 零 sorry，机器证明链 n=5→n=9 完整）+ 判定表回溯补 Lean 化（N7Table 2577 条 / N8Table 6253 条 / N9Table 15212 条，分块拼接 + 位/三进制编码，native_decide 抽查全过，零 sorry）。"
rep(old_abs_tail, new_abs_tail, "abstract tail")

# 8. 变更记录 v0.23
anchor_log = "| v0.22 | 2026-10-02 |"
new_log = r"""| v0.23 | 2026-10-02 | **判定表 Lean 化回溯补（§9 扩展）**：新增 **N7Table.lean**（2577 条 16 因子位编码、3 块拼接）、**N8Table.lean**（6253 条 23 因子位编码、8 块拼接）、**N9Table.lean**（15212 条 27 因子**三进制编码**——n=9 键第 27 位可取 0、18 块拼接），全部 lake build 通过 + native_decide 抽查 6 条零 sorry；通用生成器 `paperX_gen_lean_table.py`（bit/ternary + 分块）；技术要点：分块定义防 List cons 递归深度超限、每项整体类型标注防 MVar 超时。§9 标题更新（n=4–n=9）、N7 段诚实定位更新、结论 8、稿态、附录 A（+3 Lean 模块 + 1 生成器）、变更记录同步。 |
| v0.22 | 2026-10-02 |"""
rep(anchor_log, new_log, "changelog")

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.23 written, edits:", edits)
