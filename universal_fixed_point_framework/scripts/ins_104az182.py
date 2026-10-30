# -*- coding: utf-8 -*-
"""ins_104az182.py — 登记 104az-182（v2 收缩通道解析机制 + 两通道分离 + ord(2) 奇偶修正）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **104az-182（§8 ★★ v2 收缩通道解析机制 + 两通道分离，脚本 chain_audit_182_powerres/182b/182c）**："
    "ord_p(4) = (p−1)/(S_v2 × g_odd) 双通道分解；"
    "**① S_v2 2 进收缩 ∈ {2 = 幂基（k=1）、8 = k_max（k=3）、16 = 不动点²（k≥7）} 全框架量**；"
    "**② k=1 解析闭合**：p = 53 ≡ 5 mod 8 → Legendre(2/53) = −1 → 2 本原根（ord = 52 = p−1）→ ord(4) = 26 → 收缩 2；"
    "**③ ord(2) 奇偶判别**：2^ord(4) ≡ −1（k=1,3,7,11 → ord(2) = 2×ord(4) 偶）vs ≡ +1（k=9,13 → ord(2) = ord(4) 奇，v2(ord(2)) = 0）；"
    "2 进深度 {0,2,3,4,3,4}（k=1: 0、k=3: 2、k=7,11: 3、k=9,13: 4）；"
    "**④ 182b 硬编码修正**：k=9,13 的 v2(ord(2)) 实际为 0 非 1（182b 曾误记 ord(2)=2×ord(4)）——S_v2 结论不变（稳健）；"
    "**⑤ g 表口径分离**：104az-181 的 g = {2,8,1,1,1,13} 混合两通道——2/8 实为 S_v2（v2 收缩）、13 为 g_odd（奇删除）、1 为完整；"
    "**⑥ 奇删除通道**：仅 k=13（g_odd = 13，ord(2) 奇且删奇因子 13）；k=7,9,11 奇部分完整保留；"
    "诚实边界：深度 2/3/4 分界为数值观察（四次/八次幂剩余符号），非解析证明；g_odd 在家族内无第三例可测（素性谱仅 6 成员、5 奇 k 中仅 k=13 满足整除）。"
)
a = "**⑤ 诚实边界**：g 猜想仅 2 例支撑（13/7），完整机制（为何 4 的阶跳过 k 因子）待数论深化——16981 无框架身份不要求（中间值）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 182 done; anchor:", cnt, "; len:", len(t), "; has182:", "104az-182" in t)
