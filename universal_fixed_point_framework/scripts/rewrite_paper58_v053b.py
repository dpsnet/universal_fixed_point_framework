# -*- coding: utf-8 -*-
"""Paper 58 v0.53 补：摘要压缩与更新（去滞后表述，细节归正文）"""
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()

# 定位摘要段（"## 摘要\n\n" 到 "\n\n**关键词**"）
i0 = s.find("## 摘要")
i1 = s.find("**关键词**")
assert 0 < i0 < i1, (i0, i1)
# 摘要段 = i0 之后到关键词前（含"本文基于..."）
seg = s[i0:i1]
j0 = seg.find("\n\n")
assert j0 > 0
new_abs = """## 摘要

本文基于外部基准 arXiv:2602.12176v2（Guevara 等，2026，“Single-minus gluon tree amplitudes are nonzero”）的单负剥离振幅 $A_{1\\cdots n}$（Berends-Giele 递归公式 (21)），在 MUFPF 框架内完成五件事：（1）**数值验证基座**——独立实现 BG 递归与通式 (39)、显式公式 (29)–(32)、五项一致性、软定理，通式覆盖 n=3–10 全 pass；（2）**通道分离**——数值确认剥离振幅对左旋量相位（$\\langle ij\\rangle$）零敏感，只依赖右旋量 $\\{\\tilde\\lambda_i\\}$，并升级为 n=3–6 数值定理（定理 7.1 解析化：BG 递归结构归纳证明，z 无关性）；（3）**R₁ 区之外符号结构测绘**——generic 运动学下非零率随 n 单调下降（n=3 恒非零 → n=8≈2.60%，约 ×0.5/步几何衰减），取值恒为 ±1/0 整数，满足循环性、Kleiss-Kuijf、软定理一致性；（4）**形变循环翻译**——双通道映射（取向/手性）、阿贝尔极限路径（SDYM→自对偶 Maxwell→手性锁定形变循环）获论文 SDYM 联系支撑；（5）**内生挂靠**——双向失效镜像挂靠 MUFPF 静默分层（S3 谱静默 / S4 辫子静默），非零率 ln2 衰减与 Bott-Moran 量子化形式对应；Sp 态射编码（B1'）显式声明为不可证明的映射约定。**符号判据闭合链 n=5→n=11 全阶完成**（推论 5.2–5.9）：各阶最小基座 **12/16/31/38/59/50**；**n=11 判据分层**——符号域（A≠0）46 基座 80000×3 闭合、退化域（A=0 判别）长块主导；**阶数规律反转严格确认 50<59**（同 80000 级比较）；跨 seed 合并口径下 50 仍 8 冲突（幂律尾部双重性——解析完全闭合为终极路径）。**Lean 形式化零 sorry**：n=4 动量守恒恒等式、n=5 判据 14 模式定理、n=6–9 级联机制与判定表可执行编码。

"""

new_s = s[:i0] + new_abs + s[i1:]
# 追加变更记录（v0.53 已有行，追加摘要说明）
old = "| v0.53 | 2026-10-06 | **推论 5.9 重写**"
add = "| v0.53 | 2026-10-06 | **摘要压缩与更新**（去“反转候选”滞后表述，判据链压缩为一句，细节归正文）+ **推论 5.9 重写**"
assert old in new_s
new_s = new_s.replace(old, add, 1)

with io.open(p, "w", encoding="utf-8") as f:
    f.write(new_s)
print(f"摘要压缩: 原 {i1-i0} 字符 → 新 {len(new_abs)} 字符")
print("v0.53 补丁 written")
