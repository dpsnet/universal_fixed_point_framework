# -*- coding: utf-8 -*-
"""ins_104az183.py — 登记 104az-183（互反律深度判别：四次解析闭合 + 深度4 ⟺ a²+128b²）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **104az-183（§8 ★ 互反律深度判别：四次解析闭合 + 128 判别，脚本 chain_audit_183_quartic）**："
    "**① 四次剩余解析闭合（家族结构自证）**：N(k) = 7²+(2^k)² = 7²+64×(2^(k−3))²（k≥3）恰为四次互反律判据形式（p = a²+64b²，a=7 奇）→ 2 四次剩余 → d2 ≥ 2 对所有 k≥3 成立——非观察、是 N(k) 定义恒等的直接推论；k=1（p≡5 mod 8）无表示 ✓ 非四次（Legendre 解析闭合，见 104az-182）；"
    "**② 深度判别链**：d2≥2 ⟺ 四次剩余（解析）；d2≥3 ⟺ 八次剩余——k≥7 自动成立（ord(2) | (p−1)/8 恒整除：ord(2) = 2×奇 或 奇）；d2=4 ⟺ 十六次剩余 ⟺ ord(2) | (p−1)/16；"
    "**③ 深度4 ⟺ p = a²+128b² 可表示（6/6 精确对应）**：k=9 = 441²+128×23²、k=13 = 7929²+128×182²（非平凡表示，a≠7）；k=7,11,3 无表示 ✓（深度 3/2）；a²+256b² 对 k≥7 恒存在（又是恒等 N(k)=7²+256×(2^(k−4))²）无判别力；"
    "**④ 深度取值 {2,3,4}**：k=3→2、k=7,11→3、k=9,13→4；k≡1 mod 4 → 深度4（k=9,13）、k≡3 mod 4 → 深度 2/3（k=3 vs k=7,11 分界未解）；"
    "诚实边界：a²+128b² ⟺ 深度4 为观察级（引用的八次/十六次互反律形式需文献核实，经典形式记忆存疑——16433 八次剩余但无 a²+128b² 表示，故 128 判别对应十六次而非八次）；k≡3 mod 4 内 2 vs 3 分界开放。"
)
a = "诚实边界：深度 2/3/4 分界为数值观察（四次/八次幂剩余符号），非解析证明；g_odd 在家族内无第三例可测（素性谱仅 6 成员、5 奇 k 中仅 k=13 满足整除）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 183 done; anchor:", cnt, "; len:", len(t), "; has183:", "104az-183" in t)
