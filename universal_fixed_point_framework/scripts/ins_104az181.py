# -*- coding: utf-8 -*-
"""ins_104az181.py — 登记 104az-181（k=13 ord 例外攻坚 + g 收缩因子框架化）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **k=13 ord 例外攻坚 + g 收缩因子框架化（2026-10-20，104az-181，脚本 chain_audit_181_k13ord.py）**："
    "**① k=13 ord 例外分解**：ord_67108913(4) = 322639 = 19×16981——**19 = 静默×不动点−1 = 5×4−1 框架身份**，16981 素数无框架身份；"
    "**② 奇部分结构**：p−1 奇部分 k=13 → 4194307 = 13×19×16981；k=7 → 1027 = 13×79（两者都含 13——'含 13'不是删除条件）；"
    "**③ ★ g 猜想**：g_k = k 当 k 整除 p−1 奇部分（k=13: 13|4194307 → g=13 ✓；k=7: 7∤1027 → g=1 ✓）——删除条件 = 'k 指标自身整除奇部分'；"
    "**④ ★★ g 收缩因子全框架量**：{k=1: g=2 = 幂基（v2 例外，p−1 = 4×13）｜k=3: g=8 = k_max（v2 收缩 16→2）｜k=7,9,11: g=1 完整｜k=13: g=13 = 幂基×N_gen²−静默}——ord 收缩因子 ∈ 框架量集；"
    "**⑤ 诚实边界**：g 猜想仅 2 例支撑（13/7），完整机制（为何 4 的阶跳过 k 因子）待数论深化——16981 无框架身份不要求（中间值）。"
)
a = "**⑤ 结构意义**：N(k) 素性谱 = mod 14 种子类选择 + 通道覆盖——家族从'数值巧合'升为'模结构分层'；k=5 唯一非种子类且被双框架量覆盖——与 53（k=1 种子）同为 m_t/m_b 观测锚的候选机制。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 181 done; anchor:", cnt, "; len:", len(t), "; has181:", "104az-181" in t)
