# -*- coding: utf-8 -*-
"""ins_104az164.py — 登记 104az-164（织生成链闭合 + 差 1 链家族扩展）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **织 生成链闭合 + 差 1 链家族扩展判别（2026-10-20，104az-164，脚本 chain_audit_164_weave_chain.py）**："
    "**① 织 生成链闭合**：织 = b₀/(幂基×静默) = N_gen²/(幂基×静默) = 9/10——分子同 L1 b₀（β 一阶系数 = 代数量平方，LambdaGapIdentity.b0_eq_Ngen_sq）、分母同 D1 双身份（N_gen+k_max−1 = 幂基×静默 = 10，104az-163 机器证明）——**织 的机制动机闭合：缺口因子 = 代数量平方 / 对偶网络加法-乘法桥恒等**；"
    "**② ★ 差 1 链家族扩展**：织 = 1−1/(幂基·静默) = 1−1/10 加入 16/15 = 1+1/(N_gen·静默) = 1+1/15 的差 1 链——**家族 1±1/(a×静默) 六成员扫描**：16/15（+N_gen，104az-159 三扇区锁定）、9/10（−幂基，织）、41/40（+k_max，41 = 静默单元+1）、39/40（−k_max，39 = 静默单元−1）、21/20（+不动点，21 = N_gen×对合域 = 4.2 分子同源）、4/5（−静默单元，B_th 0.8 双身份）——**4/6 成员有框架身份**；"
    "**③ 符号-因子配对观察**：+ ↔ N_gen（16/15）、− ↔ 幂基（9/10）与 A2 修正符号族（104az-145：κΛ 加性/g_p/2 减性）同构模式——但 41/40 与 39/40 同因子异符号，配对规律非严格——**观察级不升格**；"
    "**④ 结构意义**：织 = 差 1 链唯一减性成员（与 16/15 加性互补）——L6 差 1 链结构常数家族从单成员（16/15）扩展为双成员（16/15、9/10），两成员共享静默因子、符号与配对因子互补；"
    "**⑤ 主线 B 判别层维持**：织³ = 729/1000 纯素基主导候选不动摇；F_np = 4.2187（观测 4.220 dev −0.0308%）维持。"
)
a = "供主线 B 42 锚定机制解释参考）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 164 done; anchor:", cnt, "; len:", len(t), "; has164:", "104az-164" in t)
