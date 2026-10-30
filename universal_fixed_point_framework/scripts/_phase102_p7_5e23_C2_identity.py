# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-23：C² 深层身份分解 + m_c 候选检验
================================================================
① C² = 4·ln10 的组件化分解：C² = (k_max/2)·ln(N_gen+k_max−1)
   ——组件 (k_max/2, N_gen+k_max−1) 全框架量，比"4ln10"更显式
② C² 其他候选分解扫描（找更优谱语言身份）
③ m_c = 138·C² 候选（138 = 2·3·(3k_max−1)）——统一形式破坏确认
"""
import math

kmax, Ngen = 8, 3
dH   = math.log(15)
dlam = math.pi/(24*dH+72)
sigma = 1/15

C  = 2*math.sqrt(math.log(10))
C2 = C*C

print("="*104)
print("P7-5e-23：C² 深层身份分解 + m_c 候选检验")
print("="*104)

print("① C² 组件化分解：")
print("  C² = 4·ln10 = %.10f" % C2)
print("  候选 A：C² = (k_max/2)·ln(N_gen+k_max−1) = 4·ln10 = %.10f" % ((kmax/2)*math.log(Ngen+kmax-1)))
print("    组件身份：k_max/2 = 4（半旋量对偶？P7-5c 用 2k_max=16 为旋量对偶）、N_gen+k_max−1 = 3+7 = 10")
print("  候选 B：C² = ln[(N_gen+k_max−1)^(k_max/2)] = ln(10^4)（'计数对数幂'重述）")
print()

print("② C² 其他候选分解扫描（a·d_H+b、ln 组合、√ 组合）：")
cands = []
# a·d_H + b
for a in [1,2,3,4,5,6]:
    for b in [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6]:
        v = a*dH + b
        cands.append(("a·dH+b = %d·dH%+d" % (a,b), v, abs(v/C2-1)))
# (a·dH)/b
for a in range(1,13):
    for b in [2,3,4,5,6,8]:
        v = a*dH/b
        cands.append(("a·dH/b = %d·dH/%d" % (a,b), v, abs(v/C2-1)))
# 对数组合
for n in range(2,16):
    v = math.log(n**4)
    cands.append(("ln(n^4), n=%d" % n, v, abs(v/C2-1)))
cands.sort(key=lambda t: t[2])
print("  前 8 优候选：")
for name, v, rel in cands[:8]:
    print("    %-22s = %.6f（相对偏差 %+.4f%%）" % (name, v, rel*100))
print()

print("③ m_c 候选检验：")
mc_pdg = 1270.0
mc_138 = 138*C2
print("  m_c/(C²) = %.4f" % (mc_pdg/C2))
print("  候选 138·C² = %.2f vs PDG 1270（%+.4f%%）" % (mc_138, (mc_138/mc_pdg-1)*100))
print("  138 = 2·3·(3k_max−1) = 2·3·23——破坏 2^a·3^b±1 统一形式（23 非 2^a·3^b±1）")
print("  138±1 = 137/139 均非 2^a·3^b±1 族（2⁴·3²=144 距 6）")
print("  → m_c 谱隙候选不采用（统一形式破坏，诚实排除）")
print()

print("④ 判定：")
print("  C² = (k_max/2)·ln(N_gen+k_max−1)——组件全框架量，谱语言身份比 4ln10 更显式")
print("  C² = ln(10⁴)：'计数对数幂'重述——10 = N_gen+k_max−1、4 = k_max/2")
print("  m_c：0.08% 数值命中但统一形式破坏——不升格谱隙链（诚实排除登记）")
print("  → m_c/m_u 分工保持开放（上型第一/二代不走谱隙链——v 链候选 m_t 已闭合）")
print()
print("exit 0")
