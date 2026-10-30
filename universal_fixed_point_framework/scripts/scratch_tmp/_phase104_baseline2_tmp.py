# -*- coding: utf-8 -*-
"""Phase 104az-57：基线模型无效的深度核验——KIMI 辩解三点
1. σ 位移量级复核（KIMI 公式 4.67e-13 λ²B——@51MG Hγ 他给 ±45 Å，疑似差 10 倍）
2. 位移线序 vs 观测变浅序（Zeeman λ² 标度→Hα 最优先移出；观测 Hα 最后缺失——方向性检验）
3. l-混合重整 B_mix(n) ~ B_0/n³ 与中场样本对照（KIMI 核心论点）
"""
import math

# Zeeman 位移：Δλ[Å] = 4.67e-13 × λ[Å]² × B[G]（玻尔磁子验算：Hα @1MG = 20.1 Å ✓）
def dz(lambda_a, B_g):
    return 4.67e-13 * lambda_a**2 * B_g

LAM = {3: 6563.0, 4: 4861.0, 5: 4340.0, 6: 4102.0, 7: 3970.0}
print("=== 1. σ 位移量级复核（中场样本上限 51 MG） ===")
print("线    λ(Å)   @10MG    @22.8MG(中位)  @51MG(上限)  vs 论文 EW 窗口 ±80Å")
for n in (3,4,5,6,7):
    l = LAM[n]
    d10  = dz(l, 1e7)
    dmid = dz(l, 2.28e7)
    d51  = dz(l, 5.1e7)
    flag = "移出" if d51 > 80 else "窗内"
    print("H%s %6.1f  %7.1f  %8.1f  %9.1f  %s" % ({3:"α",4:"β",5:"γ",6:"δ",7:"ε"}[n], l, d10, dmid, d51, flag))

print("\n=== 2. 位移线序 vs 观测变浅序（方向性检验） ===")
print("Zeeman 位移线序（@51MG，λ² 标度→Hα 最大）：")
order_z = sorted((3,4,5,6,7), key=lambda n: -dz(LAM[n], 5.1e7))
print("  位移降序：", " > ".join("H"+{3:"α",4:"β",5:"γ",6:"δ",7:"ε"}[n] for n in order_z))
print("观测变浅序（论文）：Hγ −41% > Hβ −27% > Hδ −12% > Hε −2%（Hα 41MG 不变浅 η_comp≈0.009）")
print("→ Zeeman 截断预测 Hα 最先移出（位移最大），观测 Hα 缺失最少——方向相反——Zeeman 截断排除")

print("\n=== 3. l-混合重整 B_mix(n) ~ B_0/n³（KIMI 核心论点核验） ===")
B0 = 235.0
print("B_mix(n) = B0/n³（MG）：")
for n in (3,4,5,6,7):
    bm = B0/n**3
    print("  H%s 上态n=%d  B_mix=%.1f MG" % ({3:"α",4:"β",5:"γ",6:"δ",7:"ε"}[n], n, bm))
print("\nDESI mid_full B：中位 22.8 / p75 37.7 / max 91.6 MG")
print("LAMOST mid B：中位 12.9 / max 91.6 MG")
print("→ 对 Hγ/Hδ/Hε（B_mix 1-3 MG）样本几乎全部深在强混合区（KIMI 论点成立）")
print("→ 对 Hβ（4 MG）大部分跨越；Hα（9 MG）中位以上也进入混合区")

print("\n=== 4. l-混合重整与 EW 缺失的关系（关键） ===")
print("l-混合重整振子强度分布（分量位移但窗口内）→ EW 守恒（积分量守恒——论文已用）")
print("观测 EW 缺失 46.9%——若分量留窗口内，EW 不缺失——需振子强度真正消失或移出窗口")
print("中场 @51MG：全部线 σ 位移 >80Å 窗口（375-1025Å）→ 分量移出 ±80Å 但可能留 ±160/320Å 窗")
print("→ 需核验论文窗口扫描（80/160/320Å）对中场高 B 端 σ 位移的覆盖")
