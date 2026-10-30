# -*- coding: utf-8 -*-
"""ins_104az167.py — 登记 104az-167（层级规则第四实例搜索判别）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **层级规则第四实例搜索判别（2026-10-20，104az-167，脚本 chain_audit_167_fourth_instance.py）**："
    "**① 候选 A（m_t/m_b 41 骨架，104az-101 点名）**：m_t/m_b = 41.3134；主结构 41×(1±1/675|320|231) dev +0.33%~+0.62%——**m_b MS-bar 口径不确定度 ~0.5% >> 判别差 0.01% 级，不可判别**；"
    "**② 候选 B/C**：m_τ/m_b = 0.4251 对 3/7 骨架 dev −0.81%（0.8% 级无修正判别）；m_c = 1.27 GeV 无 k_max 家族骨架——**均不可判别**；"
    "**③ ★ 修正来源两分观察**：κΛ 修正 1/231 = S(8) 塔 {3,7,11}——检验假设 1+1/675 dev +0.284%、1+1/320 dev +0.120%（**非 675/320 族**）——κΛ 的 231 修正为**代数推导修正**（T1–T6 机器证明，无判别自由度），层级规则 675/320 判别针对**锚定拟合修正**（有判别自由度）——**两类修正不同层**：代数修正（S(8) 塔 / δ∞=1/56 等结构常数）vs 拟合修正（675/320 族匹配）；"
    "**④ 其余框架量扫描**（g_p/2、g_n/2、μ_t、E、Δλ₃）：无 41/40 主结构×675/320 修正形式；"
    "**⑤ 结论**：第四实例（拟合修正族）现有候选均不可达（精度受限登记）；κΛ 231 为代数修正非拟合修正——**层级规则两族语义判据仍待第四实例（需更高精度新观测锚或新结构候选）**；修正来源两分（代数/拟合）为新结构观察（登记）。"
)
a = "供主线 B 42 锚定机制解释参考）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 167 done; anchor:", cnt, "; len:", len(t), "; has167:", "104az-167" in t)
