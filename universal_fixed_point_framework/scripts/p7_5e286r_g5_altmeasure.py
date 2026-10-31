# -*- coding: utf-8 -*-
# p7_5e286r_g5_altmeasure.py
# G5 替代测量路径判别：E=39/2000 无独立直接测量，找组合不变量/间接锚定链
# 全部纯内生（闭式系数为框架量）；外部数据仅作对照通道不入本脚本。
# pyenv 精确分数（Fraction），无浮点。
from fractions import Fraction as F

# 闭式系数（框架量，62281e7/286r 已判别）
A = F(1, 2)      # m/2
B = F(1, 8)      # 1/8
C = F(13, 128)   # 13/(128m)
D = F(41, 2000)  # 41/2000 m^-2
E = F(-39, 2000) # -39/2000 m^-3  （G5 本体：待测 E 之绝对值 39/2000）

def invB(m):
    return A * m + B + C / m + D / (m * m) + E / (m * m * m)

def bval(m):
    return F(1, 1) / invB(m)

print('=== I1 谱形比（B0 无关纯谱形，替代测量目标） ===')
for (m, n) in [(1, 2), (2, 3), (1, 3), (3, 4)]:
    r = invB(m) / invB(n)
    print('1/B*(%d)/1/B*(%d) = %s = %.10f' % (m, n, r, float(r)))

print()
print('=== I2 两点可分离性：谱内两点精确重构 {D,E}（a,b,c 框架已知） ===')
# 方程：1/B*(1)=A+B+C+D+E ; 1/B*(2)=2A+B+C/2+D/4+E/8
s1 = invB(1)
s2 = invB(2)
# 移项：D+E = s1-(A+B+C) ; D/4+E/8 = s2-(2A+B+C/2)
rhs1 = s1 - (A + B + C)
rhs2 = s2 - (2 * A + B + C / 2)
# 解线性方程组 D+E=rhs1 ; D/4+E/8=rhs2  -> D = 8*rhs2-2*rhs1 ? 验算：
# 4*(D/4+E/8)=D+E/2=4*rhs2 ; D+E/2=4rhs2 ; (D+E)-(D+E/2)=E/2=rhs1-4rhs2 -> E=2(rhs1-4rhs2)
E_sol = 2 * (rhs1 - 4 * rhs2)
D_sol = rhs1 - E_sol
print('D_sol=%s vs D=%s  match=%s' % (D_sol, D, D_sol == D))
print('E_sol=%s vs E=%s  match=%s' % (E_sol, E, E_sol == E))
print('|E| 重构 = %s （39/2000）' % (-E_sol))
# 雅可比（非退化性）：det [[1,1],[1/4,1/8]]=1/8-1/4=-1/8 !=0
det = F(1, 1) * F(1, 8) - F(1, 1) * F(1, 4)
print('det(雅可比)=%s （非零=>两点测量可解 D/E）' % det)

print()
print('=== I3 E 敏感度：端点测量对 E 的约束强度 ===')
s1_e0 = A + B + C + D            # 1/B*(1) 去掉 E 项
print('1/B*(1) 中 E 项贡献 = %s = %.6f' % (E, float(E)))
print('1/B*(1) 总值 = %s = %.6f' % (s1, float(s1)))
print('E 项在端点占比 = %.4f%%' % (100.0 * float(-E) / float(s1)))
# γ*(1)=1/1/B*(1)：E 扰动 dE -> dγ*
import sympy as sp
mm, e = sp.symbols('mm e')
g = 1 / (mm / 2 + F(1, 8) + C / mm + D / (mm * mm) + e / (mm ** 3))
dgdE = sp.diff(g, e)
print('∂γ*/∂E (m=1) = %s = %.6f' % (sp.nsimplify(dgdE.subs({mm: 1, e: E})), float(dgdE.subs({mm: 1, e: E}))))

print()
print('=== I4 i(2) 间接锚定链：E=i(2)·(N_gen/2)^3（286s 判别） ===')
i2 = F(13, 2250)
N_gen = F(3, 1)
print('i(2) = %s ; (N_gen/2)^3 = %s ; 积 = %s == |E| %s'
      % (i2, (N_gen / 2) ** 3, i2 * (N_gen / 2) ** 3, -E))
# 候选同构可测体：h'(2)=13/600（碗形链层2）——i(2)/h'(2)=15/4=N_gen*N'/2^2（286r）
hp2 = F(13, 600)
print('同构链：i(2)/h\'(2)=%s （=N_gen·N\') 可测 h\'(2) 则锚 i(2) 再锚 E' % (i2 / hp2))

print()
print('=== I5 三阶差分不变量：Δ³ 分离三系数（三通道连续测量） ===')
d1 = invB(2) - invB(1)
d2 = invB(3) - invB(2)
d3 = invB(4) - invB(3)
dd1 = d2 - d1
dd2 = d3 - d2
ddd = dd2 - dd1
# Δ³ 理论：线性项 A 在 Δ 即消；B 常数为 0；C/m 一阶差分留 1/m 项... 直接算精确
print('Δ³(1) = %s = %.12f' % (ddd, float(ddd)))
print('（Δ³ 中 a·m、b 全消：仅 {C,D,E} 贡献——三通道测 Δ³ 得三系数组合约束）')

print()
print('=== I6 大 m 极限测量：B*(m)·m -> 2B0（G2 线性系数通道；E 不可达） ===')
for m in [6, 12]:
    p = bval(m) * m
    print('m=%d: B*(m)·m/B0 = %s = %.6f （→2）' % (m, p, float(p)))

print()
print('=== 外部对照通道登记（σ_score 对照验证通道，非生成源） ===')
# S1=arXiv physics/0003043v1 表 2/4：γ=1000 处 ¹(-1) 与 ¹(-3) 脱附能（a.u.）
I_m1 = F(33164, 100000)
I_m3 = F(19020, 100000)
print('S1 γ=1000: I(¹(-1))=%s I(¹(-3))=%s 比值=%.4f'
      % (I_m1, I_m3, float(I_m1 / I_m3)))
# physics/0006016v1 (39) 式：−ε_s = 2.453 B³ δ_s² ；大 s 渐近 −ε_s ∝ s⁻³
print('0006016: −ε_s=2.453B³δ_s²；大 s 渐近 −ε_s∝s⁻³ —— 与 E 项 1/m³ 同负幂 3（结构级同现，登记不升格）')
# 结构同现判别：s⁻³ 与 m⁻³ 同为"纵向激发通道负三次幂渐近"
print('结构对照：MUFPF E 项 1/m³（闭式负三次项）↔ 磁诱导阴离子大 s 渐近 s⁻³ —— 负幂 3 结构同现')

print()
print('=== 判别汇总 ===')
print('P1 谱形比（B0 无关）：R(1,2)=%s 可判别的精确谱形目标' % (invB(1) / invB(2)))
print('P2 两点重构：谱内任意两点即可精确解 {D,|E|}（a,b,c 框架已知，det=-1/8≠0）')
print('P3 端点敏感：E 项在 1/B*(1) 中占比 %.2f%%，低 m 端约束最强' % (100.0 * float(-E) / float(s1)))
print('P4 i(2) 锚定链：测 h\'(2)→i(2)/h\'(2)=15/4（框架比）→E=i(2)·27/8')
print('P5 Δ³ 三系数分离：三通道连续测量可分离 {13/128,41/2000,39/2000}')
