# -*- coding: utf-8 -*-
"""ins_104az163.py — 登记 104az-163（恒等 N_gen+k_max−1 = 幂基·静默 Lean 形式化）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **恒等 N_gen+k_max−1 = 幂基·静默 Lean 形式化（2026-10-20，104az-163，NGKMOneIdentity.lean，lake build 3048 jobs 零 sorry 零 axiom 构建通过）**："
    "**① 四定理清单**：I1 ngkm1_eq_powers_silence（N_gen+k_max−1 = 幂基×静默单元 = 10，norm_num 闭合）、I2 weave_eq_nine_tenths（织 = N_gen²/(幂基·静默) = 9/10）+ weave_ngkm1_equiv（N_gen²/(N_gen+k_max−1) ≡ N_gen²/(幂基·静默) 两形式等价，经 I1 congr 1 闭合）、I3 weave_cubed_rational（织³ = 729/1000，729 = 3⁶、1000 = 2³·5³ 纯素基 {2,3,5}）、I4 weave_cubed_decomposed（织³ = N_gen⁶/(幂基³·静默³)——纯素基幂展开）；"
    "**② 跨模块同构**：I4 与 LambdaGapIdentity.L3 fnp_base_Ngen_power（Λ 缺口因子 N_gen⁶/10³）同构——织³ 的幂展开是 Λ 缺口分子的同族表达（分母 10³ vs 幂基³·静默³，因 10 = 幂基·静默 机器证明等价）；"
    "**③ 先证伪记录**：scripts/falsify_ngkm1.py Fraction 精确检验全部通过（LHS=RHS=10、织=9/10、织³=729/1000、3⁶/(2³·5³)=729/1000，非浮点）；"
    "**④ 地位**：纯代数恒等——织³ 全素基表达 + 恒等 10 = N_gen+k_max−1 = 幂基·静默 升『机器证明的框架恒等』；主线 B 判别层状态不变（织³ 主导候选维持）。"
)
a = "供主线 B 42 锚定机制解释参考）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 163 done; anchor:", cnt, "; len:", len(t), "; has163:", "104az-163" in t)
