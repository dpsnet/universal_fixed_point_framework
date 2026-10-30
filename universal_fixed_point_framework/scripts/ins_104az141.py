# -*- coding: utf-8 -*-
# ins_104az141.py — 登记生成链图谱产物
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
with io.open(p, encoding="utf-8") as f:
    t = f.read()

seg = """- **★ 生成链图谱落盘——数值溯源体系（2026-10-20，Phase 104az-141，产物 `notes/generative_chain_map.md`）**：**① 目的宣言登记**：用户核心目标——"用纯内生的方法，衍生出物理上需要的所有数值"，每个数值须可溯源到明确生成链（可溯源 ≠ 黑箱铺出）；**② 14 条生成链全集**：L1 通道分流（Rec/Sp）、L2a 静默系修正（675 族）、L2b 谱隙系修正（320 族）、L3 Bott 修正（16 系）、L4 指数修正（e 系）、L5 对合折叠、L6 Pell/差1、L7 平方差闭包、L8 Mersenne 家族、L9 观测分子（DESI/Hγ）、L10 线频率比、L11 B_th、L12 深阶碗形（1/m 渐近）、L13 质量扇区、L14 κΛ 链；**③ 数值→链映射全表**（κΛ/231/49/16/675/320/5800/Δλ₁₆/41MG/δ∞/C/D/E/65/5040/127/m_t/m_e 族/m_s/F_np/1/α_EM 等 22 项）：每项标注主链、因素依赖、歧义状态；**④ 歧义检测**：**唯一红灯 = κΛ 的 230/232 竞争（104az-131）——链溯源裁决路径确立（230/232 是否同链；不同链→231 链内唯一→结构唯一性升格）**；231 三身份/65 双解读/i'(2)/j(2) 竞争均已判为同源自洽或已判别；指数链含 e、ln10、√3、d_H 为**纯内生目标真实张力点**（黑箱铺出残留）；**⑤ 审计结论**：8/14 条链有 Lean 锚点；竞争红灯唯一一处即 κΛ——生成链图谱第一次实战检验对象；**⑥ 待办**：κΛ 230/232 链溯源、空白项补链（√3/d_H/e/N_active=3 范畴推导）、图谱随研究同步更新。"""

a = "Mordell 唯一性开放。"
c = t.count(a)
print("anchor count:", c)
assert c >= 1, "anchor not found"
# 用 140 段末句更精确锚
a2 = "宿主物理观测量（Hγ 线宽/断裂间隔/Zeeman 间隔）待观测端锁定（104az-111/114 已排除 B_th 链与 η_comp 交叉）；Mordell 唯一性开放。"
c2 = t.count(a2)
print("a2 count:", c2)
assert c2 == 1, "anchor not unique"
t2 = t.replace(a2, a2 + "\n" + seg, 1)
with io.open(p, "w", encoding="utf-8") as f:
    f.write(t2)
print("RS new len:", len(t2))
print("done")
