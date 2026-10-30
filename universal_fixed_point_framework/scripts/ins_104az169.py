# -*- coding: utf-8 -*-
"""ins_104az169.py — 登记 104az-169（m_b 推进：误差传播 + 全框架闭式闭合）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **m_b 推进：误差传播统计兼容 + 全框架闭式闭合（2026-10-20，104az-169，脚本 chain_audit_169_mb.py）**："
    "**① ★ 统计兼容升级**：闭式 41.3138 vs PDG 中心口径比值 R = m_t/m_b = 41.284±0.237（m_t 172.69±0.30、m_b 4.183±0.023 误差传播）**Δ = +0.13σ——统计完全兼容**（此前 4.18 舍入口径 dev 0.001% 为口径巧合，误差传播下中心口径亦不排斥）；"
    "**② ★★ m_b 全框架闭式闭合**：**m_b = v×(1−Δλ_min/16)×4050/(√2×371×451) = 4.180165 GeV**（对 4.18 dev +0.0039% 0.01% 级内；对 PDG 中心 4.183 dev −0.0678%）——**三代连锁生成链无外部常数：根集 → m_τ → v(3⁴·∛5，104az-5h) → m_t((1−Δλ_min/16)/√2，104az-5m，框架 v 口径 dev +0.0050%) → m_b(371 骨架，104az-168)**——m_t/m_b 比值闭式与 m_t 闭式两条链在 m_b 汇合；"
    "**③ 口径归属**：m_b* = 4.1800 为 MS-bar 型（pole 4.78 差 14% 排除）；在 PDG [4.160,4.206] 误差带内（−0.13σ）；"
    "**④ 诚实边界**：m_b 不确定度 ±0.55%（±0.023）使『0.01% 数值命中』判据受观测精度阻塞——闭式以『框架身份/结构闭合』判据成立（结构层），数值层仅统计兼容声明；∛5 为代数数非有理（框架可接受，无有理分数身份）；v 用框架候选（m_τ×3⁴·∛5）时 m_t dev +0.0050%（104az-5m 用 PDG v 时 −0.0008%——框架自洽链在 0.01% 级内维持）。"
)
a = "供主线 B 42 锚定机制解释参考）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 169 done; anchor:", cnt, "; len:", len(t), "; has169:", "104az-169" in t)
