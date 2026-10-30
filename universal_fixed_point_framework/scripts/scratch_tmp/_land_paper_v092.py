# -*- coding: utf-8 -*-
"""M81b：Paper 58 第 9 章 Lean 引用补全（n=11 三模块）"""
import io

p3 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
s = io.open(p3, "r", encoding="utf-8").read()

# 1. 标题更新
s = s.replace("## 9 Lean 形式化（n=4–n=9：级联机制 + 判定表可执行编码）",
              "## 9 Lean 形式化（n=4–n=11：级联机制 + 判定表可执行编码 + 动量双守恒恒等式）", 1)

# 2. 在 n=9 末尾（诚实定位段）后插入 n=11 小节
old9 = "* 诚实定位：与 n=6/7/8 判定表同 —— 数值闭合经验判据（Python 层 vs BG 递归 0 冲突）；\"纯尾部主导回归 + 2 补因子\" 结构未获解析解释（补因子 s1\\_2345 的 \"级联目标缺失→补左块\" 变体仅部分成立，s123\\_456789 为非级联因子 —— 补因子本质 = 退化区分，n=8 的级联覆盖度对应为该阶特异）"

add11 = old9 + """

**n=11 动量双守恒恒等式（Phase 77，2026-10-05，零 sorry）**——谱维数链的守恒约束代数化：

* `SingleMinusFullCompZero.lean`**（全补块恒 0）**：$a\\cup b=\\{1..n\\}$ ⇒ $[\\Sigma\\lambda_a,\\Sigma\\lambda_b]=0$——全补块因子数学恒零（M39 污染发现的 Lean 确证——浮动符号判 ±1 是浮点伪符号）；任意 n 的补块结构统一。

* `SingleMinusAnchorSum.lean`**（恒等式 A）**：$\\Sigma_{j\\neq k}P[k][j]=0$（任何锚 k——锚行之和恒零）——锚前缀括号的全局守恒约束。

* `SingleMinusAnchorPair.lean`**（恒等式 B）**：$P[k][p]=-\\Sigma_{j\\neq k,p}P[k][j]$（跨区间单对 = 其余锚对之和的负值）——s61 展开的机制内核——锚对分解的代数闭合。

* 诚实定位：三模块均为**动量双守恒（$\\Sigma\\omega=0$、$\\Sigma\\omega\\tilde z=0$）的代数推论**（Finset 求和 + ring，lake build 3049 jobs 全过，零 sorry）——不是判据完备性的机器证明（完备性仍为采样级数值事实 + Φ 解析形式）；恒等式 B 为 "锚 1 前缀携带符号信息主体"（M60/M82a）的守恒代数根。"""

assert old9 in s
s = s.replace(old9, add11, 1)

# 3. 版本 + 变更记录
s = s.replace("**版本**：v0.91（2026-10-07）", "**版本**：v0.92（2026-10-07）", 1)
old_vlog = "| v0.91 | 2026-10-07 | **M81a 推论 5.9 完整升级（P81 终稿化）**"
add_vlog = "| v0.92 | 2026-10-07 | **M81b 第 9 章补全（P81 终稿化）**：n=11 动量双守恒恒等式小节（FullCompZero/AnchorSum/AnchorPair 三 Lean 模块——零 sorry）+ 标题更新。 |\n| v0.91 | 2026-10-07 | **M81a 推论 5.9 完整升级（P81 终稿化）**"
assert old_vlog in s
s = s.replace(old_vlog, add_vlog, 1)

io.open(p3, "w", encoding="utf-8").write(s)
print("M81b 完成（第 9 章补全——Paper 58 v0.92）")
