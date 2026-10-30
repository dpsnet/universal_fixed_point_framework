# -*- coding: utf-8 -*-
"""ins_104az174.py — 登记 104az-174（557731 梅森拆解判别：否 + 合并数梅森因子 + 53 身份单性确认）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **557731 梅森拆解判别 + 合并数梅森因子（2026-10-20，104az-174，脚本 chain_audit_174*）**："
    "**① 判别（否）**：557731 为纯素数——非梅森数（2^m−1 无解）、不被任何梅森素数整除（M_2..M_19 全查）、无梅森组合命中（M×q±r、2^m×q±r、梅森±框架量邻接全 0）、非安全/索菲热尔曼素数、≡3 mod 4；"
    "**② ★ 合并数含梅森因子**：1673193 = 3 × 557731（3 = M_2 梅森素数）——D 合并数素分解唯一梅森成分；"
    "**③ ★ A 分子 371 = 7×53，53 = b₀×静默+k_max = 45+8 框架身份（单身份确认——7²+4² = 65 ≠ 53，'双身份'假设证伪，65 属平方±1 家族 104az-156 非 53）**；"
    "**④ ★ D 双途径表达不依赖合并数**：D = A−17/40500 = B−2/3375 全框架化，557731 仅为中间计算值——框架身份由途径提供，合并数素数性不阻塞三角互锁结论；"
    "**⑤ 诚实边界**：557731 素数无框架身份维持（不要求中间值有身份）；53 单身份 45+8 登记（纠正 173 轮口头猜测）。"
)
a = "（三链互推 + F₂ 身份 + 点阵自洽），数值终判受观测精度阻塞。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 174 done; anchor:", cnt, "; len:", len(t), "; has174:", "104az-174" in t)
