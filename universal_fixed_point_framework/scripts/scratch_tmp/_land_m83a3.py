# -*- coding: utf-8 -*-
"""落盘 M83a-3：roadmap + 笔记 §75 追加"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase83_wd_ew_plan.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 里程碑"
add = """### M83a-3 ✅ 稳健性分析（2026-10-07）

**结果**：
- 置换检验（B 洗牌 10000 次）：p<1e-4（效应非随机——无一次达原始 rho=-0.301）
- 删极端 5%（B 和 R）：rho=-0.212, p=3.1e-3（仍显著）
- 删极端 10%：rho=-0.094, p=0.24（**秩相关不显著——尾部驱动**）
- 分档删极端后梯度保持：<1kT -0.241、1-3kT -0.361、3-10kT -0.767、10-100kT -0.505

**解读（诚实口径）**：① 效应真实（置换 p<1e-4）；② **分档中心趋势梯度稳健**（删极端后梯度保持）；③ **秩相关显著主要由尾部驱动**（删 10% 后 p=0.24——效应集中在大场强端）——表述修正：非"全 B 均匀梯度"，而是"场强极端端效应最强 + 分档中心梯度存在"。

**对 P83 推进**：统计口径需双轨报告（分档均值 + 秩相关）——模型大气升级后效应形态需复核。

## 里程碑
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
### 七十五补：M83a-3 稳健性（同日志）

- 置换检验 p<1e-4（效应非随机）
- 删 10% 极端后秩相关不显著（rho=-0.094, p=0.24）——尾部驱动
- 分档删极端后梯度保持（-0.24/-0.36/-0.77/-0.51）——中心趋势稳健
- 结论：效应真实但集中在大场强端——表述用"分档中心梯度 + 尾端增强"
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)
print("M83a-3 落盘完成")
