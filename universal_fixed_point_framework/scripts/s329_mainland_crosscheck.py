# -*- coding: utf-8 -*-
"""S329 Mainland & Mulligan 1705.11068 交叉对照审计
真空介电方法：α⁻¹ ≅ 8²√(3π/2) ≅ 138.93（一阶完全屏蔽——轻子真空涨落）
对照点：8³ 波包因子 vs k_max=8；3 代因子 vs 活跃=3；主项精度 vs MUFPF
"""
import math

print("=== S329 Mainland & Mulligan 1705.11068 对照 ===\n")

# 1) Mainland 主项复算
print("[1] Mainland 一阶结果复算")
mainland = 8**2*math.sqrt(3*math.pi/2)
print(f"    α⁻¹ ≅ 8²√(3π/2) = {mainland:.6f}")
print(f"    实验值         = 137.035999084")
print(f"    相对偏差       = {(mainland-137.035999084)/137.035999084*100:.3f}%——粗（1.4%）")
print(f"    ε₀ = 3·8³αe²/ℏc——8³ 波包立方 ansatz——3 代轻子贡献相同（质量消去）")

# 2) 数值同现检查
print(f"\n[2] 数值同现（8/3——弱——机制不同）")
print(f"    Mainland 8³：立方波包 ansatz（1/L³ 数密度——L = ℏ/4m_ec）——几何构造")
print(f"    MUFPF k_max = 8：谱层上限——框架常数")
print(f"    ——数值同现但机制完全不同——弱同现（8 是常用数）")
print(f"    Mainland 3：三代轻子（e/μ/τ）——粒子物理事实")
print(f"    MUFPF 活跃 = 3：2²−1——框架常数")
print(f"    ——数值同现但机制完全不同——弱同现")

# 3) 主项精度对照
print(f"\n[3] 主项精度对照（四框架）")
SIGMA = 1/15
dv3 = 6*SIGMA**3 + 4*SIGMA**5 + 8*SIGMA**7 + 5*SIGMA**8
mufpf_main = 72 + 24*math.log(15)
phi = (1+math.sqrt(5))/2
kraemer_maya = 360/phi**2
rows = [
    ("Kraemer/Māyā", kraemer_maya, 137.507764050038),
    ("MUFPF", mufpf_main, 136.993204826453),
    ("Mainland", mainland, 138.93),
]
exp = 137.035999084
print(f"{'框架':<14}{'主项':<18}{'偏离实验':<12}{'相对'}")
for name, val, shown in rows:
    dev = (val-exp)/exp*100
    print(f"{name:<14}{shown:<18.6f}{abs(dev):<12.4f}%")
print(f"    ——MUFPF 主项 0.031%——比 Kraemer/Māyā 0.37% 小 12×——比 Mainland 1.4% 小 46×")

# 4) 结构对照定位
print(f"\n[4] 结构对照定位")
print(f"    Mainland：一阶主项（无修正系列——作者自述精度受限'include only the most")
print(f"      significant interactions'）——'主项+修正'结构缺失（无高阶系列）")
print(f"    ——结构同构性弱（无修正层级）——数值粗（1.4%）——不达标")
print(f"    ——物理动机有意义（真空涨落屏蔽 ε₀）——方法学诚实（自述近似）")
print(f"    ——与 Kraemer/Māyā（精确到 1e-8 级）不同量级——属'物理思路+粗数值'类")

# 5) 结论
print(f"\n[5] 结论")
print(f"    ✓ Mainland 审阅完成——真空介电方法——一阶 138.93——1.4% 偏差（不达标）")
print(f"    ✓ 8/3 数值同现登记（弱——机制不同：波包/代数 vs 框架常数）")
print(f"    ✓ MUFPF 主项精度优势量化：0.03% vs Kraemer/Māyā 0.37% vs Mainland 1.4%")
print(f"    △ 无修正系列——结构同构性弱——不进入结构同构比较")
print(f"    △ Grant PDF 链接失效——民间物理——登记为未审阅（低优先级）")
print(f"    △ 物理动机参考价值保留（真空涨落→ε₀→α 的因果链思想——与 MUFPF")
print(f"      静默窗口机制无直接对照——不升格）")
