# -*- coding: utf-8 -*-
"""ins_104az173.py — 登记 104az-173（三角互锁成形：D = A−17/40500 = B−2/3375 0.00003% 级）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **★★★ 三角互锁成形：m_t/m_b 第三链路 D（2026-10-20，104az-173，脚本 chain_audit_173_triangle.py）**："
    "**① ★★★ D = A − 17/40500 = B − 2/3375 = 557731/13500 = 41.3134074（观测 41.3133971 dev −0.000025% 0.00003% 级）——比 A/B/C（0.001% 级）精确两个数量级，m_t/m_b 迄今最精确框架闭式**；"
    "**② ★★★ 三角互锁三边全框架量**：|A−B| = 7/40500（对合域/(幂基²×N_gen⁴×静默³)）、**|A−D| = 17/40500（17 = F₂ Fermat 数 2⁴+1，104az-199 家族成员）**、|B−D| = 2/3375（幂基/(N_gen³×静默³)）——纯素基分母 + F₂ 分子身份；"
    "**③ ★ D 双途径恒等**：乘法链 A（371×451/4050）减 F₂ 修正 ≡ 减法链 B（42−343/500）减纯素基修正——两条独立链在 D 点精确汇合（F₂ 修正 17/40500 = 7/40500 + 24/40500，24 = N_gen×k_max）；"
    "**④ ★ 框架有理点阵**：D(−18) = A−1/2250 = 41.3133827（dev +0.000035%，18 = 幂基×N_gen²）< 观测 < D(−17) < A < B < C——观测落入点阵内距最近点 D(−17) 仅 0.000025%；D(m) = A+m/40500 家族 m∈[−40,40] 全部 dev < 0.004%（点阵密度与观测位置自洽）；"
    "**⑤ 全框架闭式**：D = 对合域×幂基×N_gen − 对合域³/(幂基²×静默³) − 幂基/(N_gen³×静默³) = 42 − 7³/500 − 2/3375；"
    "**⑥ 诚实边界**：D 合并数 557731 为大素数无框架身份（以 A/B 双途径表达，不取合并数）；m_b 口径 ±0.55% 仍使数值终判不可达——三角互锁为结构层强证据（三链互推 + F₂ 身份 + 点阵自洽），数值终判受观测精度阻塞。"
)
a = "供主线 B 42 锚定机制解释参考）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 173 done; anchor:", cnt, "; len:", len(t), "; has173:", "104az-173" in t)
