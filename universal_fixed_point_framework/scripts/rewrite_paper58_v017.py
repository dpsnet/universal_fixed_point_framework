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
rep("**版本**：v0.16（2026-10-01）", "**版本**：v0.17（2026-10-01）", "version")

# 2. 摘要尾部（级联句后加 Lean）
old_abs = "\"补因子 = 级联目标缺失的粒子 1 因子\"解析解释）**。"
new_abs = "\"补因子 = 级联目标缺失的粒子 1 因子\"解析解释 + **N8Criterion.lean 零 sorry（Fin 8 括号代数 + 2 零恒等式 + 11 级联恒等式 + 4 sgn 定理）**）**。"
rep(old_abs, new_abs, "abstract")

# 3. 稿态
old_st = "s12_34/s12_345/s12_34567 的级联目标不在 20 尾部基座内）**；形变循环翻译完成"
new_st = "s12_34/s12_345/s12_34567 的级联目标不在 20 尾部基座内，N8Criterion.lean 零 sorry：Fin 8 括号代数 + 2 零恒等式 + 11 级联恒等式 + 4 sgn 定理）**；形变循环翻译完成"
rep(old_st, new_st, "draft status")

# 4. §9 n=8 段 Lean 状态更新
old_sec9 = "- **Lean 状态**：未启动——判定表 6253 条（23 因子位编码键需 2^23 上限，List 查表可行但条目量大；参照 N6Table 方案改参，候选下一步）；n=8 级联恒等式族数值已验证（13 条 0 违反，`paperX_n8_cascade.py`），Lean 化（N8Criterion：s1_A/s12_X 双家族 ZA/B 块积模式推广）为候选下一步"
new_sec9 = "- **Lean 状态**：**N8Criterion.lean 零 sorry（2026-10-01，lake build 通过）**——Fin 8 括号代数（br/bk + 反对称/自零/双线性 6 引理）+ **2 零恒等式**（bk_1_2345678_zero 1-7 分割、bk_12_345678_zero 2-6 分割）+ **11 条级联恒等式**（s1_A 家族 6 条 W0=w0 + s12_X 家族 5 条 W0=w0+w1 双元素块，ZA/B 块积模式）+ 4 条 sgn 定理（congrArg）；**双元素块块积模式验证可直接复用**（Z0·WA−W0·ZA = WB·ZA−ZB·WA 对任意 W0/Z0 成立，动量守恒三分割）——n=8 级联机制完成机器证明；判定表 6253 条未 Lean 化（参照 N6Table 方案改参，候选下一步）"
rep(old_sec9, new_sec9, "sec9 n8 lean")

# 5. 附录 A：N8Criterion 行（插在 N7Criterion 行后）
anchor_app = "| `formal_proof/MUFPFormalization/src/MUFPFormalization/N7Criterion.lean` | Lean n=7 级联机制证明（Fin 7 括号代数 + 1-6 分割零恒等式 + 5 条级联恒等式 + 2 条 sgn 定理，零 sorry） | lake build 通过 |"

app8l = r"""| `formal_proof/MUFPFormalization/src/MUFPFormalization/N7Criterion.lean` | Lean n=7 级联机制证明（Fin 7 括号代数 + 1-6 分割零恒等式 + 5 条级联恒等式 + 2 条 sgn 定理，零 sorry） | lake build 通过 |
| `formal_proof/MUFPFormalization/src/MUFPFormalization/N8Criterion.lean` | Lean n=8 级联机制证明（Fin 8 括号代数 + 2 零恒等式 [1-7 分割/2-6 分割] + 11 条级联恒等式 [s1_A 家族 6 条 + s12_X 家族 5 条双元素块] + 4 条 sgn 定理，零 sorry） | lake build 通过 |"""

rep(anchor_app, app8l, "appendix A N8Criterion")

# 6. 变更记录 v0.17 行（加在 v0.16 前）
anchor_log = "| v0.16 | 2026-10-01 | **n=8 级联机制论证**：推论 5.6 增补级联机制——s1_A/s12_X 双家族 **13 条动量守恒三分割恒等式** 40000 样本 **0 违反**（原始值残差判据 <1e-9，max|dev|≤5.7e-14）；**\"补因子 = 级联目标缺失的粒子 1 因子\"解析解释**（3 补因子的级联目标 s34_5678/s345_678/s34567_8 不在 20 尾部基座内；7 条级联目标在基座内被吸收；s1_23456 目标缺失但信息对 A_BG 冗余）；零恒等式 sg 级\"伪违反\"归因浮点噪声（sg 判零阈值过严，动量守恒残差 ~1e-15 精确，改用原始值判据）；诚实标注③/⑧、§9 n=8 段、结论 11、诚实边界 n=8 条、附录 A（+2 脚本）、摘要/稿态/版本行同步更新。 |"

log17 = r"""| v0.17 | 2026-10-01 | **n=8 级联机制 Lean 化**：新增 **N8Criterion.lean 零 sorry**（lake build 通过，3049 jobs）——Fin 8 括号代数（br/bk + 反对称/自零/双线性 6 引理）+ **2 零恒等式**（bk_1_2345678_zero 1-7 分割、bk_12_345678_zero 2-6 分割）+ **11 条级联恒等式**（s1_A 家族 6 条 W0=w0 + s12_X 家族 5 条 W0=w0+w1 双元素块，ZA/B 块积模式）+ 4 条 sgn 定理（congrArg）；**双元素块块积模式验证可直接复用**（Z0·WA−W0·ZA = WB·ZA−ZB·WA 对任意 W0/Z0 成立）——n=8 级联机制完成机器证明。§9 n=8 段 Lean 状态更新、附录 A（+1 Lean 模块）、摘要/稿态/版本行同步更新。 |
| v0.16 | 2026-10-01 | **n=8 级联机制论证**：推论 5.6 增补级联机制——s1_A/s12_X 双家族 **13 条动量守恒三分割恒等式** 40000 样本 **0 违反**（原始值残差判据 <1e-9，max|dev|≤5.7e-14）；**"补因子 = 级联目标缺失的粒子 1 因子"解析解释**（3 补因子的级联目标 s34_5678/s345_678/s34567_8 不在 20 尾部基座内；7 条级联目标在基座内被吸收；s1_23456 目标缺失但信息对 A_BG 冗余）；零恒等式 sg 级"伪违反"归因浮点噪声（sg 判零阈值过严，动量守恒残差 ~1e-15 精确，改用原始值判据）；诚实标注③/⑧、§9 n=8 段、结论 11、诚实边界 n=8 条、附录 A（+2 脚本）、摘要/稿态/版本行同步更新。 |"""

rep(anchor_log, log17, "changelog v0.17")

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.17 written, edits:", edits)
