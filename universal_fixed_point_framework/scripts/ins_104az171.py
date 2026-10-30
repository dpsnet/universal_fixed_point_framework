# -*- coding: utf-8 -*-
"""ins_104az171.py — 登记 104az-171（m_t/m_b 双闭式精确互锁 + 框架互锁谱系新实例）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **m_t/m_b 双闭式精确互锁核验（2026-10-20，104az-171，脚本 chain_audit_171_interlock.py）**："
    "**① ★★ 精确代数恒等**：A（乘法闭式 371×451/4050 = 167321/4050）与 B（减法闭式 42−343/500 = 20657/500）满足 **A = B − 7/40500**（精确有理恒等，非数值巧合）——**7/40500 = 对合域/(幂基²×N_gen⁴×静默³)，纯素基 {2,3,5}**：两计算链路输出被框架量钉在固定距离；"
    "**② ★ 互锁轴 = 对合域幂谱**：A = 7×23903/4050（7¹，23903 = 53×451 = (45+8)×(k_max+3)×(静默单元+1)）、B = 对合域×[N_gen×幂基 − 对合域²/(幂基²×静默³)] = 7×(6−49/500)（7¹ 减 7³）——两链共享对合域 7 因子；Q 双表达 Q_A−Q_B = 1/40500；"
    "**③ 框架互锁谱系再添新实例**：Rec/Sp 语义双通道、P20/EM（计数平方 7² vs 对数平方 C²=4ln10，Δλ_P20/Δλ_EM = 7²/C²）、打靶/谱方法（二阶差分 vs Chebyshev 谱微分）、307/371 镜像（(45,8,7) 生成块）——m_t/m_b 乘法/减法双链为新投影；"
    "**④ 诚实边界**：B 合并分子 20657 = 7×13×227（13、227 无框架身份）——B 结构层有身份、数层无，弱于全因子框架化 A；三角互锁测试（第三独立链路）未成形——41+π/10 dev −0.0018% 但 π 无代数身份不立（104az-166 判别规则维持），其余候选为编造除数不立；"
    "**⑤ 可 Lean 化**：恒等 A = B − 7/40500 为框架有理数环内简短代数恒等。"
)
a = "供主线 B 42 锚定机制解释参考）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 171 done; anchor:", cnt, "; len:", len(t), "; has171:", "104az-171" in t)
